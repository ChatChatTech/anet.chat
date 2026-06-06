# Nonthreshold-Based Event Detection for 3D Environment Monitoring in Sensor Networks

Mo Li, Member, IEEE, Yunhao Liu, Senior Member, IEEE, and Lei Chen, Member, IEEE

Abstract—Event detection is a crucial task for wireless sensor network applications, especially environment monitoring. Existing approaches for event detection are mainly based on some predefined threshold values and, thus, are often inaccurate and incapable of capturing complex events. For example, in coal mine monitoring scenarios, gas leakage or water osmosis can hardly be described by the overrun of specified attribute thresholds but some complex pattern in the full-scale view of the environmental data. To address this issue, we propose a nonthreshold-based approach for the real 3D sensor monitoring environment. We employ energy-efficient methods to collect a time series of data maps from the sensor network and detect complex events through matching the gathered data to spatiotemporal data patterns. Finally, we conduct trace-driven simulations to prove the efficacy and efficiency of this approach on detecting events of complex phenomena from real-life records.

Index Terms—Distributed applications, data compaction and compression, query processing, wireless sensor networks.

# 1 INTRODUCTION

WIRELESS sensor networks (WSNs) have been widely studied for environment monitoring. In such monitoring applications, automatically detecting events is quite essential, e.g., for detecting vehicles or forest fires. Currently, the typical event detection method [12] relies on decisions made at the sensor node(s) based on predefined data thresholds for normal environments. The rationale behind such threshold-based approaches is that when events occur, there will be detectable changes in environmental data. Thus, an event can be captured once the observed sensory data exceed the predefined thresholds.

Our motivating scenario comes from the field study in a coal mine [15], where environment surveillance is carried out to ensure miners’ safety. The amount of oxygen, gas, dust, temperature, humidity, and watery regions are monitored in a 3D space of underground tunnels in the mine. Several event detection tasks are essential to secure the safety of the miners, such as detecting gas leakage, oxygen-enriched spots, and water seepage. Gas leakage often occurs when the digging machines expose a source of gas in the mining process, and it often leads to a local increase in gas density. If a certain district of gas accumulates to critical explosive density, explosions could occur. Oxygen-enriched spots exist at the ventilative places where high oxygen density creates healthy environmental conditions for human beings. Indicating such areas provides important guidelines for the miners patrolling in the coal mine. Water seepage brings water into the coal mine tunnels, which corrodes the tunnel surfaces and threatens the tunnel’s structural integrity.

The events described above share the common characteristics that their occurrence results in trends in the development of environmental data rather than some instantaneous overrun of specified thresholds in individual sensor nodes. Hence, the threshold-based approaches work well for detecting simple events, but the complex events with spatiotemporal variety in the environment can hardly be captured by a simple cutoff method. An integrative view of the environment has to be established to extract the features of such events. For example, gas leakage usually leads to an expanding area of high gas density over time, which spatially follows a degrading form where the gas density decreases from the source of the leak. The water seepage can be categorized as a “fault event” with an apparent observation on the advances of the frontier between the dry area and the flooded area.

In order to accurately detect complicated events, we need a nonthreshold-based event detection approach. We intend to describe complex phenomena with certain spatiotemporal data patterns and detect events through matching the gathered data to such data patterns. The challenges for such a design are as follows: First, differing from threshold-based approaches, the environment data map has to be continuously maintained from real-time sensor readings, while conserving energy for battery-powered sensors [5], [6], [23], [25], [27] is a very critical issue. We need to restrain the data traffic and maintain the data map in an energy-efficient manner. Second, the communication quality of WSNs is poor, especially in the underground monitoring environments, such as a coal mine. We have to develop robust methods of data map construction so that the accuracy of the obtained data map could be preserved in a high loss rate network. Third, the 3D monitoring field raises nontrivial issues in abstracting the environment, which are not faced by previous works in 2D cases. Efficient data structures and modeling methods are required in a point of 3D view.

In this paper, we propose a 3D gradient data map using the space orthogonal polyhedra (OP) model. We build a multipath routing architecture to provide robust data delivery for the map construction. Instead of directly routing raw data to the sink before processing, a novel 3D aggregation algorithm is designed for map construction and update. We demonstrate the efficacy and efficiency of the proposed approach in trace-driven simulations using synthetic data sets derived from the raw data collected in our study in the real coal mine environment.

The rest of this paper is organized as follows: We briefly review the related work in Section 2. In Section 3, we describe the network architecture and construction of the gradient data map. The aggregation criteria and incremental data map construction techniques are also introduced. In Section 4, we describe the event feature patterns and illustrate how pattern-based event detection is performed on the data map. Experimental studies of our approach are given in Section 5. Finally, we conclude this work in Section 6.

# 2 RELATED WORK

Event detection remains an essential task in various WSN applications. There are a number of recent works on eventoriented query processing in sensor networks. The COUGAR project [3] introduces a sensor database system and deals with three types of event queries: historical queries, snapshot queries, and long-running queries. The system employs threshold-based detection logic and encapsulates it into a set of asynchronous functions provided for users. Directed Diffusion [14] aims at addressing the event-based real-time queries by diffusing different event interests into the monitoring network and letting sensors report when occurrences of some specified events are detected. The Directed Diffusion approach does not explore the spatial or temporal correlations among the sensory data, and it relies on individual reports of sensor nodes according to the disseminated event interests. TinyDB [12] defines the event by a composition of various specified attribute thresholds. The event detection is carried out by comparing sensory readings of attributes with predetermined threshold values. TinyDB provides a distributed mapping method to construct contour maps of sensor network readings. Differing from our approach, the mapping process in TinyDB is only done in 2D fields and their work does not aim to provide event detection based on the data spatiotemporal patterns. DSWare [16] explores the correlation among different sensor observations for event detection. Events are grouped into two different types: atomic events and compound events. Confidence functions are employed to address compound events. Above works all focus on 2D scenarios.

In-network data aggregation has been intensively studied as an effective method to provide energy-efficient data collection [4], [17], [18], [19], [21]. LEACH [11] protocol constructs clustering hierarchy on the network and achieves data fusion at the cluster heads to reduce transmitted information. By rotating the cluster heads, energy dissipation is evenly distributed over the network. The TAG approach [19] builds a routing tree in the sensor network and statistical data are aggregated in the intermediate nodes. In [17], network tomography techniques have been applied to solve the problem of loss inference in data aggregation. Different from the approaches above, our approach explores the spatial correlations on the sensory data and achieves data aggregation through the combination of OP in the gradient data maps. Recently proposed contour mapping methods [12], [20], [24] share similar ideas with this work in visualizing the monitored fields for event detection. While those works utilize aggregation-based approaches to efficiently approximate the 2D field in contour maps, they provide no means to extend for 3D scenarios.

The multipath routing strategy has recently been suggested to provide robust data deliveries in sensor networks. Robust aggregation on it needs duplicate-insensitive data structures to carry information [7], [22]. In our work, we propose the space OP model as such a duplicateinsensitive data structure.

# 3 THREE-DIMENSIONAL GRADIENT DATA MAP CONSTRUCTION

This section is organized as follows: In Section 3.1, we briefly describe the sensor network architecture and deployment of sensors in a 3D space. Then, in Section 3.2, we present the concept of 3D gradient data map. In Section 3.3, we introduce the OP and describe how to achieve in-network construction of the gradient data map by the space OP model. Sections 3.4 and 3.5 describe the aggregation criteria for the gradient data map construction and its incremental update. Finally, in Section 3.6, we extend our algorithm for random sensor deployments.

# 3.1 Network Architecture

In our coal mine monitoring scenario, sensor nodes are assumed uniformly deployed in 3D monitoring space with measured location information (later, we will release this constraint to extend our work into random deployments). This could be easily achieved by placing sensors along the safety props in the tunnel. Fig. 1 shows the environment in underground coal mine tunnels and the placement of sensors in our underground prototype system previously reported in [15]. A cubic grid can be established on this network and each sensor node accounts for the environment sensing in the cubic cell it resides in (as shown in Fig. 2a). The grid information is created at sink and disseminated throughout the network. Each sensor node, based on its location information, calculates the dimension and coordinates of the cubic cell it resides in.

The whole network is organized into multipath routing architecture. Sensor nodes are divided into different levels from the sink. The sensor nodes closer to the sink have lower levels. For each sensor node, the one level lower nodes are considered as parent neighbors, and the one level higher nodes are treated as child neighbors. Each node forwards the query messages originated in the sink to its child neighbors and sends the report messages to its parent neighbors. Thus, in the message relay process at each node, multirelayers are triggered for message forwarding. By the means of multipath routing, message redundancy is provided to ensure a more reliable message delivery in the lossy sensor network.

![](images/b432fed3721e2b7faff9c8911402b86c8b368471f369b40b1fcd399955c36281.jpg)



(a)

![](images/becd2c80f779e5c345f02554eed97e83024b01c84f628a765ec086a1bad9040a.jpg)



(b)

![](images/6107e31fdf55296e9f65bdf82d5477ba3e951218cdcf6f3e87690d6a038d56c2.jpg)



（c）  
Fig. 1. The underground coal mine environment. (a) and (b) The safety props in the main tunnel and the working face. (c) The sensor node deployed on a safety prop.

The multipath routing architecture is constructed by a two-phase initialization process, DIFFUSION and ECHO. In the DIFFUSION phase, the sink originated indicator message is flooded into the network. Each sensor node estimates its hop count from the sink. When the DIFFUSION phase completes, each sensor node gets its level and discovers its parent neighbors and child neighbors. The ECHO phase is triggered by the highest level sensor nodes, which are farthest from the sink. ECHO messages are created by those nodes and flooded in the network. Hence, the total level count is captured by all the nodes and each node calculates its own operation schedule for each sampling cycle. Fig. 2b shows that sensor nodes in different levels share different schedules. Each node carries out sensing and processing at the beginning of a data sampling cycle. Nodes in different levels transfer data in different time slots within the same sampling cycle. Lower level nodes need to wait for the data from higher level nodes so that data aggregation could be implemented in each level. The sampling cycle interval $D _ { s \prime }$ data processing time $T _ { p } ,$ and the total level count c determine the duration d of data transfer and aggregation for nodes in each level, $d = 2 ( D _ { s } - T _ { p } ) / c$ . For each node at the ith level, its data transfer and aggregation process lies in the slot of $[ ( c - i - 1 ) d / 2 , ( c - i + 1 ) d / 2 ]$ .

While more redundancy of the aggregated data has been provided by multipath routing, data duplicates have been introduced at the time of multiple relaying. Therefore, we must employ duplicate-insensitive methods (such as [7] and [22]) to prevent error during data aggregation.

# 3.2 Three-Dimensional Gradient Data Map

Under the network architecture described in Section 3.1, we propose 3D gradient data map to describe the monitored environment. As mentioned above, the sensor nodes are deployed in a 3D space in the monitoring area and each sensor is responsible for sensing the environmental data within its unit cubic cell (we assume that the data within a unit cube have the similar values). Thus, we can aggregate the cubic cells with similar sensor readings into a cube cluster and construct the gradient data map at each sampling period within the network. The gradient data map consists of different clusters with their own geometric shapes and data distributions. The gradient data map is an approximation of monitored environment and reflects environmental data distribution at each sampling period.

We employ data aggregation in each sampling process and create partial gradient data maps from sensor readings. The partial data maps are merged as much as possible along the paths from sensors to the sink. At the sink, the gradient data map is built from a set of partial gradient data maps. Along with a sequence of sampling, a time series of approximated 3D gradient data maps is constructed at the sink, on which event detection is performed. Fig. 3 exhibits a partial gradient data map including three different cube clusters. We can simply use the average value of all sensor readings in the cube cluster to approximate the data of this cluster during the aggregation. However, that approach introduces large approximating errors. In our gradient data map, we compute the data distribution $f$ of each cube cluster and represent each cube cluster by the geometric structure, called space OP. By manipulating two parameters of OP, which can be simply transmitted with little bandwidth, the sensor nodes are collaborated to construct the gradient data map in an innetwork manner. The key operations in the aggregation process are estimating the similarity of different OP and merging the similar OP at each sensor node.

![](images/cc937354f7b01164ce8822a2da71f4caa8a50d5103e55f3334643940a86af1ca.jpg)



(a)

![](images/ced412ead05b3114535f93d7e29ce537e24b23b53062c6ca684a7fd42460f09f.jpg)



(b)   
Fig. 2. (a) The multilevel network architecture. (b) Node schedules in this network.

![](images/d7ad218330f5d75bb7d4d546a382c776242294e1170d95b9f9076dc57588127c.jpg)



Fig. 3. Three-dimensional space gradient data map.

# 3.3 Space OP Model and Gradient Map Construction

We use the space OP model to describe different cube clusters. OP can capture the data distribution in 3D cubic space and only requires few parameter settings. The OP was first introduced in Constructive Solid Geometry (CSG). Aguilera and Ayala investigated the characteristics of OP [1] and presented the geometric models to represent OP as well as some basic geometric operations, which are summarized as follows:

Definition 3.1. OP are polyhedra with all faces oriented in three orthogonal directions.

In OP, all planes and lines are parallel to three orthogonal axes. The number of incident edges for each vertex can be only three, four, or six, which is referred as V3, V4, or V6, respectively [1]. An Extreme Vertices (EV) model has been proposed to represent OP.

Definition 3.2. The EV model for OP is defined as a model that only stores all V3 vertices.

Aguilera and Ayala proved that the EV model is a valid B-Rep model, i.e., it is complete and compact in the sense of geometry. Furthermore, they proposed the ABC-sorted EV model, which provides computational convenience for geometric operations.

Definition 3.3. An ABC-sorted EV model is an EV model where V3 vertices are sorted first by coordinate A, then by B and then by C.

Fig. 4 gives an example of the ABC-sorted EV model for the OP. The model is stored as a series of vertices (node 1 to node 16). Based on ABC-sorted EV models, the following geometric operations can be efficiently performed:

1. Volume calculation—To calculate the volume of OP. An $O ( n )$ algorithm exists by accumulating the strip region between any consecutive different sections, where n is the number of vertices of the OP.   
2. Relationship checking—To check the relationship of two OP: overlapping, adjacent, or separated. An OðnÞ algorithm exists by sequentially checking the relationship of the sections of the two OP along some axis, where n is the number of vertices of the OP.   
3. Boolean operations—To compute the union or intersection or difference of two OP. An OðnÞ algorithm exists, which sequentially performs Boolean operations on the sections of the two OP along some axis.

Since a cube cluster is composed of multiple cubic cells, the geometric shape of clusters can be well modeled by OP, which is described by the geometric shape of the covered area and a data distribution function in this area. The partial gradient data map stored in each sensor node is represented as a list of OP depicted by the ABC-sorted EV model. The in-network construction of the gradient data map starts from each node sensing its environment and generating the OP model for its own cell. Each node receives the partial maps from all its child neighbors at the time slot of data aggregation. The OP from different partial maps form an active set $S _ { p } .$ . Through investigating the relationship among OP within $S _ { p } ,$ the sensor node estimates the similarity of OP and merges the mergeable OP. Fig. 5 illustrates the possible relationships between two OP. Finally, the partial maps are aggregated into a single map $M _ { f } ,$ which includes disjointed OP. The lower level sensor node transfers $M _ { f }$ to its parent neighbors.

Algorithm 1 presents detail steps of partial map generation for each sensor node. A min-heap H is constructed containing possible mergers (line 1). Different OP pairs from the active set $S _ { p }$ are checked by function checkMergeable, which verifies whether two OP are mergeable. Two OP are mergeable when they are overlapping or adjacent and have enough similarity (as will be defined in Section 3.4). The function createMerge creates a merger for two mergeable OP and adds it into H. This merger contains a key value indicating the potential of merging the two OP. A smaller key value indicates a higher potential of merging, and this key value is used as the element key in H (lines 2-4). In later sections, we will introduce how the function checkMergeable and createMerger estimate the similarity of two OP and calculate the key value of the merger, respectively. After all the possible mergers have been added into $H ,$ the mergers are extracted from H by increasing order of the key values (line 6). The two OP in each merger are merged into a new OP by the function merge (line 7). The two merged OP are deleted from the active set $S _ { p }$ and all the merges related to these OP are deleted from the min-heap H (lines 8-11). The newly created OP is then inserted into the active set H and immediately checked whether it could be further merged (lines 12-15). After all mergeable OP are merged, we process the overlapping but not mergeable OP pairs and remove the intersection region from one of them so that no ambiguous regions exist in our generated map (lines 16-18).

![](images/c8a81b4da0a81dfea29c283ef39884230c2d7f2728f5d727b7e87f0962789884.jpg)

![](images/9920eb41155c6dcefbc16c7add2639967d2def58ab415af7a741e6d4bd7975db.jpg)



(a)

![](images/a719f20c41300e84bb3e13e02dd9d7a06205fd4d9d882779068f1db5eb55cba2.jpg)



(b)   
Fig. 4. XYZ-sorted EV model. (a) A hidden line representation of OP. (b) The order number of its XYZ-sorted EV model (V3 vertices on three planes).

![](images/e677e5f6df78498f5d7fd989eef9c7cd07c331696aed15ace9f7455e5d23ac6a.jpg)



Fig. 5. The possible relationships of two $\mathtt { O P }$ .

# Algorithm 1 Partial Map Generating

Input: the active set $S _ { p }$

Output: the resulting map $M _ { f }$

1: construct an empty min-heap H, to contain mergers $\langle O P _ { 1 } , O P _ { 2 } \rangle$ ;   
2: for each OP pair OPi and $O P _ { j } \ ( i \neq j )$ in $S _ { p }$ do   
3: $\textbf { i f } c h e c k M e r g e a b l e ( O P _ { i } , O P _ { j } )$   
4: $H . \ a d d ( c r e a t e M e r g e r ( O P _ { i } , O P _ { j } ) ) ;$   
5: while not H. emptyðÞ do   
6: merger $m \langle O P _ { 1 } , O P _ { 2 } \rangle = H .$ . extractðÞ;   
7: create $O P = m e r g e ( O P _ { 1 } , O P _ { 2 } ) ;$   
8: for any merger m containing OP1 or $O P _ { 2 }$ do   
9: H. deleteðmÞ;   
10: $S _ { p } . \ : d e l e t e ( O P _ { 1 } ) ;$   
11: $S _ { p } . \ : d e l e t e ( O P _ { 2 } ) ;$   
12: for each OPk in $S _ { p }$ do   
13: $\mathbf { i f } \ c h e c k M e r g e a b \bar { l } e ( O P , O P _ { k } ) \ 1$   
14: $H . \ a d d ( c r e a t e M e r g e r ( O P , O P _ { k } ) ) ;$   
15: $S _ { p } . { \mathrm { ~ } } a d d ( O P ) ; $   
16: for each overlapping region $R = O P _ { i } \cap O P _ { j }$ in $S _ { p }$ do   
17: $O P _ { i } = O P _ { i } - R \mathrm { o r } O P _ { j } = O P _ { j } - R ;$   
18: return $M _ { f } = S _ { p } ;$

# 3.4 Aggregation Criteria

To aggregate different partial maps, we need to adopt effective criteria for measuring the similarity of OP so that the resulting partial data map well approximates the actual data map.

The OP model used in our system represents a cluster of cubic cells with similar environmental data. We can use a specific data value to represent the data in the whole OP region, e.g., the average value of all the sensor readings in the OP. In such case, to check the similarity of two OP, we only need to check their representing values. However, a single data value can hardly reflect full-scale environmental conditions in the OP. Moreover, only investigating the representative value of OP will miss the important spatial information. For example, with the same value, OP occupying a larger space is still different from OP holding a smaller space. Thus, we can merge a tiny OP (OP with small space) into a much larger OP (OP with large space) even though their representative data values differ a lot, because the merging simplifies the data map representation without losing much accuracy. However, for the case in which two OP both occupy large spaces, merging them may greatly reduce the accuracy of the resulting gradient data map.

In our design, each OP is associated with a data distribution model, which describes the environmental data within this OP. There have been several techniques proposed to represent the data distribution with compression, such as wavelet transformation [26], histogram-based model [8], [10], and so forth. In this work, we choose to adopt linear regression (LR) model, which incurs constant communication overhead and facilitates the aggregation of OP. A function $v = f ( x , y , z )$ is employed to approximate the data value in each spot in the $\mathrm { O } \dot { \mathrm { P } } ,$ where $x , \ y ,$ and z correspond to the spot coordinate in the 3D space. Polynomial models can be utilized to formulate this approximation function. To reduce the computational overhead for resource constraint sensor nodes, we adopt the linear model $\begin{array} { r } { f ( x , y , z ) = c _ { 0 } + c _ { 1 } x + c _ { 2 } y + c _ { 3 } z , } \end{array}$ where the data distribution is approximated by a hyperplane in the 4D space built on $< x , y , z , v >$ . In the sampling period, each node first computes its initial model for its cubic cell from its sensor reading. During the aggregation, a linear model is built by conducting LR over the whole OP area. For OP containing n cubes, n values are extracted for all cubes. Thus, we can get n 4-tuples $< x _ { 1 } , y _ { 1 } , z _ { 1 } , v _ { 1 } > _ { \mathrm { { \ O } } }$ ; $< x _ { 2 } , y _ { 2 } , z _ { 2 } , v _ { 2 } > , . . . , < x _ { n } , y _ { n } , z _ { n } , v _ { n } >$ from which we compute the coefficients of the linear model by solving the following equation:

$$
A w = b
$$

$$
A = \left( \begin{array}{c c c c} 1 & \sum_ {i = 1} ^ {n} x _ {i} & \sum_ {i = 1} ^ {n} y _ {i} & \sum_ {i = 1} ^ {n} z _ {i} \\ \sum_ {i = 1} ^ {n} x _ {i} & \sum_ {i = 1} ^ {n} x _ {i} ^ {2} & \sum_ {i = 1} ^ {n} x _ {i} y _ {i} & \sum_ {i = 1} ^ {n} x _ {i} z _ {i} \\ \sum_ {i = 1} ^ {n} y _ {i} & \sum_ {i = 1} ^ {n} x _ {i} y _ {i} & \sum_ {i = 1} ^ {n} y _ {i} ^ {2} & \sum_ {i = 1} ^ {n} y _ {i} z _ {i} \\ \sum_ {i = 1} ^ {n} z _ {i} & \sum_ {i = 1} ^ {n} x _ {i} z _ {i} & \sum_ {i = 1} ^ {n} y _ {i} z _ {i} & \sum_ {i = 1} ^ {n} z _ {i} ^ {2} \end{array} \right), \tag {1}
$$

$$
w = \left( \begin{array}{c} c _ {0} \\ c _ {1} \\ c _ {2} \\ c _ {3} \end{array} \right), b = \left( \begin{array}{c} \sum_ {i = 1} ^ {n} v _ {i} \\ \sum_ {i = 1} ^ {n} v _ {i} x _ {i} \\ \sum_ {i = 1} ^ {n} v _ {i} y _ {i} \\ \sum_ {i = 1} ^ {n} v _ {i} z _ {i} \end{array} \right).
$$

The parameters $A ,$ w, and b of the LR model are integrated and transmitted with the OP in the aggregation process, which take Oð1Þ cost to represent the data distribution over the OP. When merging two OP, $O P _ { i }$ and $O P _ { j } ,$ i  we can compute the LR model of the resulting $O P _ { i j }$ from the LR models of $O P _ { i }$ and $O P _ { j }$ . By summing $A _ { i }$ and $A _ { j } ,$ we get $A _ { i j } ,$ so does $b _ { i j }$ with respect to $b _ { i }$ and $b _ { j } .$ . The coefficients $w _ { i j }$ can be derived from the generated $A _ { i j }$ and $b _ { i j } .$ Therefore, we only transmit the parameters of the two matrices, instead of sampling the $< x , y , z , v >$ tuples to construct our LR model, which induces more overhead. The similarity of two OP is estimated based on the linear models of OP. An estimated error bound $\varepsilon _ { i j }$ is computed when aggregating two different OP by the following formula:

$$
\varepsilon_ {i j} = \frac {(1 + \varepsilon_ {i}) \Delta_ {i} + (1 + \varepsilon_ {j}) \Delta_ {j}}{R _ {i} + R _ {j}}, \tag {2}
$$

where $\Delta _ { i }$ represents the difference between the cumulates of $f _ { i j }$ and $f _ { i }$ on $O P _ { i } ,$ , and $\Delta _ { j }$ represents the difference between the cumulates of $f _ { i j }$ and $f _ { j }$ on $O P _ { j } ,$ , i.e.,

$$
\Delta_ {i} = \left| \iiint_ {O P _ {i}} \left(f _ {i j} (x, y, z) - f _ {i} (x, y, z)\right) d \delta \right|, \tag {3}
$$

$$
\Delta_ {j} = \left| \iiint_ {O P _ {j}} \left(f _ {i j} (x, y, z) - f _ {j} (x, y, z)\right) d \delta \right|.
$$

$\varepsilon _ { i }$ and $\varepsilon _ { j }$ are the error bounds for $f _ { i }$ on $O P _ { i }$ and $f _ { j }$ on $O P _ { j }$ . Thus, $( \overset { \cdot } { 1 } + \varepsilon _ { i } ) \Delta _ { i } + ( 1 + \varepsilon _ { j } ) \Delta _ { j }$ gives the maximum difference when we substitute the former LR models on $O P _ { i }$ and $O P _ { j }$ with the aggregated one. $R _ { i }$ and $R _ { j }$ represent the cumulates of $f _ { i }$ on $O P _ { i }$ and $f _ { j }$ on $O P _ { j }$ , respectively, i.e.,

$$
R _ {i} = \iiint_ {O P _ {i}} f _ {i} (x, y, z) d \delta , R _ {j} = \iiint_ {O P _ {j}} f _ {j} (x, y, z) d \delta . \tag {4}
$$

This formula computes the error bound $\varepsilon _ { i j }$ after the aggregation, and it is then evaluated by a user-defined error bound ". Only when $\varepsilon _ { i j }$ is not greater than $\varepsilon ,$ two OP are mergeable. Note that, in the above formula, the error bound is computed in a weighted manner, where the OP volume is the weight factor.

Based on the estimation of the LR model, we consider the data value as well as the volume of the OP when merging two different OP regions. We list all the functions checkMergeable, createMerger, and merge for merging two OP in Algorithm 2. The function checkMergeable first checks the relationship of the two OP. If they are overlapping or adjacent, the function further checks whether the error induced by merging is tolerable. The function createMerge computes the benefit of merging two OP, $\varepsilon _ { i j } / \varphi _ { i j } ,$ the error bound over reduced region, and takes it as the index key of the merger in the minheap H in Algorithm 1. Thus, the merging with less error and larger reduced region will be conducted earlier. The function merge merges two OP by combining their regions and computing the new LR model for the resulting OP.

# Algorithm 2 Merging Manipulations

# Function checkMergeable $( O P _ { i } , O P _ { j } )$

1: if $O P _ { i }$ and $O P _ { j }$ are overlapping or adjacent

2: compute $\varepsilon _ { i j } ,$

3: $\mathbf { i f } \ \varepsilon _ { i j } \leq \varepsilon$

4: return TRUE;

Function create $M e r g e r ( O P _ { i } , O P _ { j } )$

1: $\varphi _ { i j } =$ volumeðOPiÞ þ volumeðOPjÞ - volume $( O P _ { i } \cup O P _ { j } )$

2: if $\varphi _ { i j } > 0$

3: return merger ${ < O P _ { 1 } , O P _ { 2 } > }$ with key $\varepsilon _ { i j } / \varphi _ { i j } ;$

Function merge $( O P _ { 1 } , O P _ { 2 } )$

1: compute $O P = O P _ { i } \cup O P _ { j } ;$

2: $A = A i + A j ;$

3: $b = b i + b j ;$

4: compute w by $A w = b ;$

5: return OP with A, b, and w;

# 3.5 Incremental Update of Gradient Data Map

When carrying out a sequential sampling, each sensor node needs to continuously update its partial gradient data map to reveal environmental status in real time. An effective and efficient criterion for map update can offer the ability of real-time monitoring while minimizing computational and communicational cost. Simply reconstructing a new data map in each sampling period is an easy yet costly approach, which may cause sensor nodes to quickly deplete their power due to the heavy communication traffic. Indeed, the consecutively constructed data maps vary not much due to the rareness of environmental events [9]. Thus, we employ an incremental method to update the partial gradient data map.

In the aggregation process, each sensor node keeps its previously constructed data map as $M _ { p }$ . The node receives the update units $U _ { 1 } , U _ { 2 } , \dots , U _ { n }$ from its child neighbors in each updating phase. The updated units are in fact OP with different data values out of the error bound $\varepsilon$ from their previous statuses. Upon receiving these updated units, the node first constructs an update map $M _ { u }$ by aggregating these updated units. This process is similar to the aggregation of partial maps, with the same aggregation criteria. Before sending out the update map $M _ { u } ,$ , the node diminishes some reducible units to reduce the amount of sending data. In the diminishing phase, the update map $M _ { u }$ is compared with the previous data map $M _ { p } ,$ , and the similarity estimation is conducted for the OP in $M _ { u }$ , which can be enclosed by OP in $M _ { p } .$ . Considering OP $P _ { i }$ in $M _ { u }$ enclosed by some OP $P _ { j }$ in $M _ { p } ,$ , we can calculate the estimated error bound $\varepsilon _ { i j }$ by (2) and evaluate it with a predefined error bound " $\therefore \mathrm { I f } \varepsilon _ { i j } \leq \varepsilon ,$ , the $\mathrm { O P }$ $P _ { i }$ is considered reducible and removed from $M _ { u } ,$ since updating this OP will not bring significant impact to the final data map. After removing all reducible OP from $M _ { u } ,$ the node sends the diminished update map as an update unit U to its parent neighbors and updates its current data map $M _ { c }$ by combining $M _ { u }$ and $M _ { p }$ in the manner described in Section 3.4.

Algorithm 3 illustrates this process. The algorithm receives the previous data map $M _ { p }$ and the updating units $U _ { 1 } , U _ { 2 } , \dots , U _ { n } ^ { \tilde { } }$ from the child neighbors as inputs and outputs the updating unit $U$ it sends to its parent neighbors and the current data map $M _ { c }$ it maintains for recording current environment status. The current data map $M _ { c }$ will be in the next round update taken as the previous data map $M _ { p }$ . This algorithm contains two phases. In the first phase (lines 1-8), the algorithm constructs the updating unit U by generating a partial map from the input OP of $U _ { 1 } , U _ { 2 } , \ldots , { \bar { U } } _ { n }$ . Specifically, the algorithm filters the scrapped small OP generated from small environment variations or measurement noises by merging them into previous large and stable OP, which saves unnecessary communication cost for representing them (lines 3-7). In the second phase (lines 9-10), the algorithm combines the previous data map and the update partial map by merging their OP and obtaining the current data map $M _ { c } ,$ reflecting current environment status.

# Algorithm 3 Data Map Updating

Input: the previous data map $M _ { p }$ and the updating units $U _ { 1 } , U _ { 2 } , \dots , U _ { n }$

Output: the updating unit U and the current data map $M _ { c }$

1: active set $S _ { p } = \{ { \mathrm { a l l ~ O P } } \in U _ { i } | i = 1 , \ldots , n \} .$ ;   
2: generate update map $M _ { u }$ from $S _ { p }$ (Algorithm 1);   
3: for each $\mathrm { O P } _ { i }$ in $M _ { u }$ do   
4: for each $\mathrm { O P } _ { j }$ in $M _ { p }$ do   
5: if $\mathrm { O P } _ { i } \subseteq \mathrm { O P } _ { j }$   
6: if checkMergeable $( O P _ { i } , O P _ { j } )$   
7: drop $O P _ { i }$ from $M _ { u } ;$   
8: $U = M _ { u } ;$   
9: active set $S _ { p } ^ { \prime } = \{ \mathrm { a l l O P } \in M _ { u }$ and $M _ { p } \} _ { }$   
10: generate current data map $M _ { c }$ from $S _ { p }$ (Algorithm 1);   
11: return U and $M _ { c } ;$

The data map updating technique exploits the stabilization of monitored environment where events rarely happen, so the communication cost could be largely saved without losing accuracy. Our experiments in Section 5 further prove this.

# 3.6 Adapting Random Sensor Deployments

To adapt a broader scope of WSN application scenarios, we extend our algorithm into random deployment of sensor networks. In such random sensor deployment, when the cubic grid is established, some of the cubic cells may contain multiple sensor nodes and some of them may be empty. For the cells with multiple sensors, our aggregation algorithm automatically aggregates their readings into the linear function $f .$ However, those empty cells make the constructed gradient map incomplete, with OP of undetermined values. This problem also occurs under node failures and link losses.

We employ spatial interpolation on the server side to recover the complete map from the collected incomplete map. Each undetermined OP is estimated by spatial interpolation around its surrounding OP and gets merged into the most similar neighbor OP. By this means, we can finally construct a complete gradient data map for the random deployed sensor network. Algorithm 4 illustrates this procedure. Algorithm 4 is executed on the server side after the incomplete gradient data map has been collected from the network. Thus, the interpolation will not influence all in-network procedures described in previous sections.

# Algorithm 4 Gradient Map Recovery

Input: the incomplete gradient data map $M _ { i c }$

Output: the recovered complete gradient data map $M _ { c }$

1: for each undetermined OP region $P _ { i }$ in $M _ { i c }$ do

2: compute $w _ { i }$ from interpolation;

3: $\varepsilon _ { i } = \varepsilon ;$

4: for each adjacent OP $P _ { j }$ do

5: compute $\varepsilon _ { i j } ;$

6: if $\varepsilon _ { i j } < \varepsilon _ { i }$

7: $\varepsilon _ { i } = \varepsilon _ { i j } ,$

8: $k = j ;$

9: merge $( P _ { i } , P _ { k } ) ;$

10: return $M _ { c } ;$

# 4 EVENT DETECTION

When the sink receives the aggregated data map, we can perform the event detection based on the exhibited data pattern from the data map. Moreover, the spatiotemporal pattern revealed from the series of data maps provides us the dynamic progress of the event, which helps capture the event developments. In this section, we describe the event feature patterns and propose a formal method of utilizing the predefined feature patterns to detect a specific event.

In previous discussions, the term “data map” refers to the constructed gradient data map in some sampling period. For the purpose of event detection, the spatiotemporal data pattern is often investigated over a time series of data maps. For the convenience of description, without specification, we will later use “data map” referring to the spatiotemporal data map consisting of a time series of received data maps. Each data map in this series is referred to as a data map “snapshot.”

# 4.1 Event Feature Patterns

The event feature pattern F is defined as a time series of snapshots L on the data map of some environmental attribute and a set of relationship R among them. $L = \{ S _ { 0 } , S _ { 1 } , \ldots , S _ { n } \}$ , where $S _ { i }$ is a snapshot $( t _ { i } , M _ { i } )$ on the data map composed of the time label $t _ { i }$ and current data map Mi. Here, $\Delta t = t _ { i + 1 } - t _ { i }$ i is the sampling interval between two consecutive snapshots and the data map $M _ { i }$ consists of different OP $( \bar { P _ { i 1 } } , \bar { P _ { i 2 } } , \ldots , \bar { P _ { i m } } )$ . Different OP are associated with different data values $v _ { i j }$ . The relationship R specifies the event feature pattern on series L. R describes the spatial relationship $R _ { S }$ by regulating the relationships $R ( P _ { i k } , P _ { i l } )$ between different OP on the data map snapshot $M _ { i }$ and the temporal relationship $R _ { T }$ by regulating the relationships $R ( { \bar { M _ { i } } } , { M _ { j } } )$ between different data map snapshots.

The above definition of $F$ describes the spatiotemporal trends on the data map of the specified event. By comparing the obtained aggregated data maps with the predefined feature patterns, we could accurately detect the ongoing development of certain events. We illustrate the event feature pattern in detail by describing two sample events as well as their specified feature patterns.

Spreading Event. For the event of gas leakage, as the gas spreads from the source spot, the distribution of the gas density follows the single source spreading event model in the data map of gas density. Spatially, in the data map snapshots, the leakage source bears the highest gas density value and the value falls along all directions from the source spot. Temporally, as time passes, the abnormal region expands and the gas density rises within the whole region. According to above observed features, we specify the spreading event feature pattern as follows:

The spreading event feature pattern $F ^ { s }$ is determined by the user-specified snapshot series $L ^ { s }$ and the relationship $\dot { R ^ { s } }$ on them, which are customized by the users: 1) $T$ is a userspecified event duration, which defines the time interval between the first snapshot $S _ { 0 }$ and last snapshot $S _ { n }$ in the snapshot series $L ^ { s } ,$ i.e., $T = t _ { n } - t _ { 0 } . \ 2 )$ The spatial relationship $R _ { S } ^ { s }$ regulates a series of nesting $\mathrm { O P } \ \{ P _ { i 1 } , P _ { i 2 } , . . . , P _ { i N i } \}$ for each $M _ { i \cdot } ~ N _ { i } ~ ( 0 \leq i \leq n )$ is the user-specified spreading level, which specifies the number of nesting OP. $P _ { i k }$ occupies the hole region in $P _ { i k + 1 }$ . The difference of data values associated with the two OP ${ v _ { i k } } - { v _ { i k + 1 } }$ is bounded by the user-specified degrading bound $[ D _ { L } , D _ { H } ] .$ , and the ratio of their volumes $\delta _ { k } / \bar { \delta } _ { k + 1 }$ is bounded by the user-specified scaling bound $[ f _ { L } , \dot { f _ { H } } ] , ( 0 < { f _ { L } < f _ { H } < \dot { 1 } } ) . 3 $ ) For the temporal relationship $R _ { T } ^ { s }$ , the variation of data values between two consecutive data maps $M _ { i }$ and $M _ { i + 1 }$ is regulated by the userspecified variation factor $v f ,$ such that the data value variation for any spot $p$ in the event region between $M _ { i }$ and $M _ { i + 1 }$ is $v _ { p i } - v _ { p i + 1 } \geq v f$ . Another user-specified spreading factor $s f \ ( 0 < s f < 1 )$ Þ constrains the ratio of the volumes of event regions (composed of the nesting OP) in consecutive data maps $M _ { i }$ and $M _ { i + 1 . }$ , such that $E _ { i } / E _ { i + 1 } \leq s f .$ . This factor indicates the spreading speed of the source. Fig. 6a illustrates the spreading event.

Fault Event. The fault event corresponds to those breaking out changes in terms of some attribute value. For instance, the underground water seepage can be categorized as a fault event, which induces a large flooded region on the tunnel floor, disturbs the normal work, and damages the working equipment. Moreover, in severe situations, the water destroys the tunnel structure and threatens the life of miners. For the fault event, the sensory readings in the fault region largely differ from those in the normal region. So, the event detection can be featured as a $0 / 1$ detection on the data map by setting appropriate thresholds for two regions. However, this cannot be achieved by simply setting thresholds at individual sensors, because what we need is a big picture of the entire field and we aim to find the two distinct regions in a macroscopic level. This can only be achieved after a global data map of the field is obtained. We, on the server side, thus are able to observe the data pattern and detect the event. Any individual sensor node, without enough information on the global data distribution, cannot draw its local judgement about the event.

![](images/a31a67f705c9e2d7d5acae48c87f167bb4046919909b51fb07d20bbf219e91bc.jpg)



(a)

![](images/833e84e11195c0680c1f988423993fcf9113b6a6fc34223a3ea4c82775073612.jpg)



(b)   
Fig. 6. Illustration of sample event feature patterns. (a) The spreading event pattern. (b) The fault event pattern.

By specifying the relationship between the 0 attribute OP and the 1 attribute OP on the data maps, we can describe the feature pattern of fault event. The fault event feature pattern $F ^ { f }$ is determined by the user-specified snapshot series $L ^ { f }$ and the relationship $R ^ { f }$ on them, which are customized by the users: 1) T is a user-specified event duration, which constrains that, in the snapshot series $L ^ { f } ,$ the time interval between the first snapshot $S _ { 0 }$ and last snapshot $S _ { n }$ is $t _ { n } - t _ { 0 } = T . ~ 2 )$ The spatial relationship $R _ { S } ^ { f }$ regulates two adjacent $\mathrm { O P } , P _ { i 1 }$ and $P _ { i 2 }$ in each $M _ { i } , P _ { i 1 }$ is associated with value $v _ { i 1 }$ in the range $[ b _ { 1 } , b _ { 1 } + k ]$ and $P _ { i 2 }$ with value $v _ { i 2 }$ in the range $[ b _ { 2 } , b _ { 2 } + k ] . \ b _ { 2 } - b _ { 1 } \geq \Delta$ , where $\Delta$ is a user-specified threshold. The volumes of both OP $E _ { 1 }$ and $E _ { 2 }$ should be larger than a user-specified region size bound $E \left( E > 0 \right)$ Þ, which defines the scale of the event to be detected. Another user-specified parameter $S _ { c }$ sets the lower bound of the coincident plane area shared by the two OP. 3) The temporal relationship $R _ { T } ^ { f }$ regulates the event regions in consecutive data maps overlapping at least at a percentage of $\alpha ,$ where $0 < \alpha < 1$ is a user-specified confidence factor. Fig. 6b illustrates the fault event.

# 4.2 Pattern-Based Event Detection

Once the event feature patterns have been specified, the sink continuously processes the received data maps and compares them with the predefined event feature patterns. Once a match between the pattern and the data map is found, the corresponding event is captured. Moreover, by tracking the spatiotemporal feature of the data map series, the development of current event could also be revealed.

We define that an instant snapshot $A _ { t }$ of the data map $A$ matches $S _ { i }$ if and only if the OP in $A _ { t }$ match the OP in $M _ { i }$ and share the same spatial relationships $R ( P _ { i k } , P _ { i l } )$ Þ. We define that the data map A matches pattern $F$ if and only if from time $t ,$ there exists a series of map snapshots $\left\{ A _ { t } , A _ { t + \Delta t 1 } , \ldots , A _ { t + n \Delta t } \right\}$ from $A ,$ , such that any snapshot $A _ { t + i \Delta t }$ matches the corresponding feature snapshot $S _ { i }$ and all map snapshots obey the temporal relationships $R ( A _ { t + i \Delta t } , A _ { t + j \Delta t } )$ .

Algorithm 5 illustrates how the sink processes the matching of data map series with predefined event feature patterns. First, each map snapshot in the data map series $\left\{ { A _ { t } , A _ { t + \Delta t 1 } , \ldots , A _ { t + n \Delta t } } \right\}$ is compared with the feature pattern snapshot according to the spatial relationship $R _ { S }$ (lines 2-7). Only after all snapshots match $R _ { S } ,$ the temporal relationship $R _ { T }$ is checked on this data map series with event duration T (lines 8-13). If $R _ { T }$ holds, the feature pattern matching is achieved, and TRUE is returned (line 14). When any mismatch appears, the starting time t of the series is slid by $\Delta t ,$ and a new round of checking is processed (lines 4-7 and 10-13). If no pattern matching has been detected until the possible event time exceeds the duration $T _ { A } , F A L S E$ is returned, which means no event is detected (lines 5, 6, 11, and 12).

# Algorithm 5 Feature Pattern Matching

Input: the specified event feature pattern ${ \cal F } = < { \cal L } , { \cal R } >$ and the received data map series A

# Output: the matching result (TRUE/FALSE)

1: $t = 0 ;$   
2: for each snapshot $S _ { i } ~ ( 0 \leq i \leq n )$ of L do   
3: if not $A _ { t + i \Delta t }$ matches $S _ { i }$ according to $R _ { S }$   
4: $t = t + \Delta t ;$   
5: if $t + T > T _ { A }$   
6: return FALSE;   
7 : goto $2 ;$   
8: for each pair of map snapshots   
9: if not $R ( A _ { t + i \Delta t } , A _ { t + j \Delta t } )$ conforms to $R _ { T }$   
10: $t = t + \Delta t ;$   
11: if $t + T > T _ { A }$   
12: return FALSE;   
13: goto 2;   
14: return $T R U E ;$

$$
A _ {t + i \Delta t}, A _ {t + j \Delta t} (0 \leq i, j \leq n) \mathbf {d o}
$$

# 5 PERFORMANCE EVALUATION

We conducted a field study by investigating the various environmental conditions in the D.L. Coal Mine. It is one of the most automated coal mines worldwide. We collected different sets of real data in the field and from historic records under normal and exceptional situations. In this section, we investigate the efficacy and efficiency of our proposed event detection mechanism by a trace-driven simulation using synthetic workload generated from the collected raw data.

# 5.1 Simulation Setup

We simulated the event scenarios in a sensor network with a 3D sensor deployment. The widely used Mica2 motes [13] are presumed as the underlying hardware standard. All numbers are 2-byte integers (including sensor readings and all coefficients). The size limit for the simulated packets is set to 60 bytes. Sensor nodes follow a CSMA strategy in the link layer transmission, and according to our experimental observations in the coal mine [15], when the channel is heavily reused (10þ transmitters or interferers for each transmission link), the maximum throughput for each link is limited below 16 packets per second. Any traffic exceeding this amount will be dropped or collided in the delivery.

An $N \times N \times N$ cubical grid topology is initiated with a sensor node placed at the center of each cubical grid. The parameter N indicates the diameter of this cubical grid network, ranging from 5 to 20 (default value is 10) in our experiments to explore the system scalability under different network sizes. Each sensor node has direct communication links with the six closest neighbor nodes surrounding it. The link quality is measured with the link loss rate $q ,$ which is the probability that a packet transmitted along the link gets lost. In our experiment, this parameter varies from 0 percent to 40 percent (default value is 10 percent) to explore the system reliability under different network conditions.

Three types of real-world historic sensory data for the underground environment have been collected in the coal mine as our data trace including gas density, oxygen density, and watery regions. However, due to the constraint on resource and environment, the original data are collected with rough granularity of time scale and incomplete sampling spots in the space scale. Based on the raw data on hand, we generate more detailed synthetic data sets for use in our experiment, which nevertheless mimic the original data characteristics and trends under normal conditions as well as during the period that events happen.

In the experiment, each data set contains all three kinds of environmental data as three different environmental attributes and lasts for 10,000 seconds, while each data sampling cycle interval is 100 seconds. The sample events described in Section 4.1 have been queried over the three different attributes. Event E1 refers to the spreading event of gas density, which occurs with gas leakage; Event E2 refers to the spreading event over oxygen density, which occurs around the oxygen-enriched spots; Event E3 refers to the fault event in watery regions when water osmosis happens. Note that though E1 and E2 both refer to the spreading events, due to the different principles of gas leakage and oxygen concentration, the two events have different spatiotemporal data trends and their feature patterns differ in the parameter settings. The above events are queried over the data set with a predetermined event frequency $f ,$ which depicts the monitoring workload. f is calculated as the duration of events over the total monitoring duration. In our experiment, we vary f from 0 percent to 40 percent (default value is 10 percent) to obtain a full view of the system efficiency under different workload.

We focus on two metrics for performance evaluation. The event detection accuracy measures the efficacy of the approach and the network traffic overhead tells the efficiency on energy consumption. The event detection accuracy is measured by two submetrics, precision and recall, which have been widely used in IR domain [2]. Precision describes the detection precision, which is defined as the percentage of accurately detected real events over all reported events; recall describes the detection completeness, which is defined as the percentage of successfully detected events over all occurred events. The network traffic overhead is measured by the total amount of messages (bytes) transmitted in the network in the monitoring duration.

![](images/635d773fae6c0f7506256447281bb475c809c6c14abd4b70343467649b8afdc1.jpg)



(a)

![](images/dac209dd7b4e8c7f244524dbfba0af160139663ddde1c7f447e974d136cee943.jpg)



(b)

![](images/f4480b7e09e3ed998b19900c265749a4af9c9276f5c4445a5f86059db8a0cdd6.jpg)



（c）  
Fig. 7. The accuracy of our aggregation approach with different settings. (a) The detection recall of different aggregation criteria: average value aggregation versus LR. (b) The detection recall of different sensor placement: grid, perturbed grid, and random. (c) The detection recall of direct aggregation versus incremental update of the data map.

To further evaluate the performance gain of our approach, we did a comparative study investigating three possible approaches: 1) AGG: our proposed in-network data map aggregation approach described in Section 3; 2) SAT: the server side aggregation under TAG [19] framework, in which the network is organized into a tree structure and all data are forwarded to the sink. Data map is constructed in the server side. In the SAT approach, each sensor sends and relays data to only one parent node; and 3) SAM: the server side aggregation under multipath routing strategy [22], in which the network is organized into multipath routing style and the data map is constructed in the server side. In the SAM approach, each sensor sends and relays data to multiple parent nodes. The network architecture is the same as that in AGG.

# 5.2 Simulation Results

Since in all runs of experiments nearly 100 percent detection precision is consistently achieved in different approaches under different parameter settings, we omit this metric and only present the performance on recall in the experiment result part.

Before the comparative study on our AGG approach with the other two approaches, we first evaluate the performance gain of our approach under different settings.

# 5.2.1 Evaluating AGG Performance

Fig. 7 presents the recall of event detection under varied error bound " (Section 3.4). Fig. 7a compares the recall of the aggregation based on LR adopted in AGG approach with the simple average value-based one. For the aggregation based on LR, the error bound refers to the userdefined error bound " introduced in Section 3.4. For the aggregation based on average values, the error bound refers to the difference ratio between two OP. As the figure shows, the aggregation based on LR provides much higher percentage of recall, overcoming the aggregation based on average values by more than 20 percent. The best recall achievable in the average value-based aggregation is 78 percent when the error bound is set to be 0.15, while the best recall achievable in the LR-based aggregation is nearly 100 percent. This is mainly because the average value-based aggregation does not integrate the volume factor of OP in the aggregation process. It simply compares the average value of two different OP and accepts the merge if they have similar values no matter what their sizes are. Thus, the average value-based aggregation is vulnerable to the noises of the environment data.

Fig. 7b compares the recall in different sensor placements. “Grid” placement refers to the regular placement of sensors into 3D grids, which is the ideal case assumed in this paper. “Perturbed Grid” places sensors into grids but with a small random perturbation on their placement. It represents the most possible situation of manually placing sensors in the practical environment. “Random” placement deploys sensors in a purely random way. For the “random” placement, as the sensors might be deployed unbalanced, the network might be disconnected, so we place necessary relay nodes to connect the entire network. As Fig. 7b shows, the “Grid” placement achieves the highest recall rate, while the “Perturbed Grid” achieves slightly lower recall rate. The “Random” placement suffers from the highly unbalanced sensor samplings and, thus, has the lowest recall rate. Nevertheless, it achieves up to 70 percent detection recall when the error bound is properly set. We believe the “Perturbed Grid” placement of sensors gives the most representative results for the practical situations.

In Fig. 7c, we use DIR AGG to represent the method that crudely does data map aggregation and aggregates the data map in every sampling period. We use UPD AGG to represent the refined method that adopts the technique of data map updating described in Section 3.5. As the tolerable error bound is enlarged, the event detection recall in both methods varies slightly, while both strategies achieve perfect detection recall when the error bound is set in the range of [0.15, 0.2]. This shows that the proposed incremental updating technique does not significantly degrade the event detection accuracy.

Fig. 8 compares the network traffic overhead incurred by the original direct aggregation approach DIR AGG and the incremental update approach UPD AGG (see Section 3.5).

Fig. 8a plots the network traffic overhead for both methods under different error bounds. The traffic overhead decreases as the error bound " is enlarged, but much more slowly when " is large. A combined view of this figure and Fig. 7c suggests an optimal choice of the error bound " at about 0.2, which provides perfect detection recall with comprehensive traffic cost. We adopt this optimal setting of " for later experiments. Compared with the DIR AGG, the UPD AGG achieves almost the same detection recall but with 50 percent less traffic cost than with DIR AGG for all error bound settings.

![](images/74e7c8e65ac8c98efd4421ccfa53a1dddaf814567e49fc541ae9fc56e5e66406.jpg)



(a)

![](images/0bf47132c082130b2007279eb9de82ed9a7070ac2ad38b8d48468b790138cb7d.jpg)



(b)

![](images/bb2ab0888ec158e806c1965a6150ac16cc63db316200e2020781bd65f0a2ec9c.jpg)



（c）  
Fig. 8. Network traffic overhead of DIR AGG and UPD AGG under different network settings. (a) Different predefined error bounds. (b) Different event frequencies. (c) Different data dynamics.

Fig. 8b shows the traffic saving in UPD AGG method for various event frequencies, from which we observe that a lower event frequency leads to a larger percentage of saving. That is because the data map updating technique adopted in UPD AGG method reduces more unnecessary traffic overhead when events are rare and historic data are aggressively utilized.

Fig. 8c further shows the traffic saving in UPD AGG method under various data dynamics. We group our data set into three different categories: low data dynamics, medium data dynamics, and high data dynamics. The three different groups account for 73 percent, 21 percent, and 6 percent of the data set separately. From the figure, we observe that the UPD AGG method saves more than 80 percent network traffic under low data dynamics and 54 percent network traffic under medium data dynamics. The two situations account for 94 percent of the whole data set.

# 5.2.2 Comparative Study

We broaden the comparative study among the three different approaches AGG, SAT, and SAM under various parameter settings. Fig. 9 plots the event detection recall of the three approaches. In all cases, our AGG approach achieves the best performance.

As shown in Fig. 9a, as the link loss rate increases, the recall of SAT rapidly drops below 40 percent and tends to 0. SAM approach also bears a bad detection recall. SAM suffers data loss from link loss as well as packet drops and collisions due to the heavy traffic flows. Even when the link loss rate is set to 0, a large amount of data still get lost and lead to a much lower recall of 87 percent, while the other two approaches both achieve nearly 100 percent recall. Our AGG approach demonstrates good tolerability to the network quality. The recall is kept above 60 percent even in a lossy network with up to 40 percent link loss rate.

In Fig. 9b, the network diameter is enlarged to investigate the scalability of three approaches. Again, the SAT approach leads to unacceptable detection recall rate. Our AGG approach keeps high recall rate all along, while the recall of SAM approach drops linearly as the network diameter increases. This is largely because a larger network generates much more network traffics in the SAM approach, leading to more packet drops and collisions.

Fig. 9c plots the detection recall of the three approaches in cases with different event frequencies. We observe that the parameter of event frequency hardly influences the recall rate of the three approaches. All three approaches provide relatively stable recall rates when event frequency is varied, and our AGG approach outperforms the other two. The incremental update in AGG approach provides slightly improved performance when the event frequency decreases.

Fig. 10 plots the network traffic overhead in three approaches. In Fig. 10a, with the increase of the link loss rate, the traffic overhead of all three approaches decreases because of the loss of packets. The SAM approach experiences a faster decrease on the traffic overhead, but the total amount is much larger than the SAT and AGG approaches. The traffic overhead of the SAT approach has a skip decrease when the link loss rate changes from 0 percent to 10 percent; however, from Fig. 9a, we know that this is because most of the useful information gets lost due to the packet loss. Thus, although SAT has the lowest traffic overhead, it provides nearly unacceptable event detection recall. Fig. 10b shows how network traffic overhead grows as the network size increases. We note that while the SAT and AGG approaches maintain comparatively low traffic overhead against the increase of network diameter, the SAM approach has a dramatic increase of traffic overhead, which greatly constrains its scalability. Fig. 10c shows how the parameter of event frequency affects the three approaches. While the event frequency has little influence on SAM and SAT approaches, the traffic overhead of our AGG approach is reduced as the event frequency decreases, benefiting from the data map updating technique. According to our field investigation in the coal mine, generally, the event frequency in the real world remains low, benefiting the application of our AGG approach.

![](images/9ab717fae1a27282a65f49482a7fed64c42e3d1b1489e950031a78db3b219157.jpg)



(a)

![](images/bfddd4b81f5048c380f80943e94ced9e990ef134606db75c1a08b9a00e1793a9.jpg)



![](images/82dd69ccfbc2b7a723d48890581386d86908c6ba57d5651ef6a7f7f9a5f49e89.jpg)



Fig. 9. Event detection recall of the three approaches with different parameter settings. (a) Link quality. (b) Network diameter. (c) Event frequency.

![](images/ba6e105a7c62fcd6645bb2f4cd39273681a5557d52508368cec1335b78ff9bdd.jpg)



(a)

![](images/7ce22dce1a8193f4d1b43136038ea188f55db060ec373ac3226f5ba5eb3ef936.jpg)



(b)

![](images/970821900b287f2820c5156894dba8e53a56067ee427aedf5930c77a50bdd202.jpg)



（c）  
Fig. 10. Network traffic overhead of the three approaches with different parameter settings. (a) Link quality. (b) Network diameter. (c) Event frequency.

To summarize, among the three possible approaches, the SAT approach introduces the least traffic overhead but provides the worst, totally unacceptable event detection accuracy; the SAM approach provides somewhat tolerable event detection accuracy but with the most traffic overhead and the worst scalability; our AGG approach provides the best event detection performance with relatively small traffic overhead. We also achieve the best scalability to the network size and tolerability to the network quality in the AGG approach.

# 6 CONCLUSIONS AND FUTURE WORK

In this paper, we have proposed a nonthreshold-based approach for complex event detection in 3D environment monitoring applications. Other than threshold-based approaches, we have proposed event feature patterns to specify complex events and developed a pattern-based event detection method on the obtained 3D gradient data map. We employ multipath routing architectures to provide robust data delivery and perform in-network aggregation on it to efficiently construct the data map. Space OP model is proposed to describe the environment data distributions. Partial data maps are aggregated by merging OP regions with similar environmental data. The incremental update for the gradient data map explores the usability of historic data while the environment is stable with low frequency of events and further reduces unnecessary data delivery. Our experimental results show the performance gain of our energy-efficient techniques. Moreover, the comparative study with two alternative approaches exhibits that our approach achieves great event detection accuracy with small network traffic overhead.

The future work includes implementing a working system in real-world environment. To carry on, pattern recognition on the obtained gradient data maps with machine learning techniques on historic data samples may provide more efficient detection methods, which will also be included in our future work.

# ACKNOWLEDGMENTS

This work was supported in part by the Hong Kong RGC Grants HKUST6169/07E and HKUST 6119/07E, by the National High Technology Research and Development Program of China (863 Program) under Grant 2007AA01Z180, by the National Basic Research Program of China (973 Program) under Grant 2006CB303000, by the HKUST Nansha Research Fund NRC06/07.EG01, and by the NSFC Key Project Grants 60533110, 60736016, and 60736013.

# REFERENCES

[1] A. Aguilera and D. Ayala, “Orthogonal Polyhedra as Geometric Bounds in Constructive Solid Geometry,” Proc. Solid and Physical Modeling Symp. (SPM), 1997.   
[2] R. Baeza-Yates and R.N. Berthier, Modern Information Retrieval. Addison-Wesley, 1999.   
[3] P. Bonnet, J. Gehrke, and P. Seshadri, “Querying the Physical World,” IEEE Personal Comm., vol. 7, 2000.   
[4] R. Burns, A. Terzis, and M. Franklin, “Design Tools for Sensor-Based Science,” Proc. Third Workshop Embedded Networked Sensors (EmNets), 2006.   
[5] A. Chakrabarti, A. Sabharwal, and B. Aazhang, “Using Predictable Mobility for Power Reduction in Sensor Networks,” Proc. Second IEEE/ACM Int’l Workshop Information Processing in Sensor Networks (IPSN), 2003.   
[6] W. Choi, P. Shah, and S.K. Das, “A Framework for Energy-Saving Data Gathering Using Two-Phase Clustering in Wireless Sensor Networks,” Proc. First IEEE Ann. Int’l Conf. Mobile and Ubiquitous Systems (MobiQuitous), 2004.   
[7] J. Considine, F. Li, G. Kollios, and J. Byers, “Approximate Aggregation Techniques for Sensor Databases,” Proc. 20th IEEE Int’l Conf. Data Eng. (ICDE), 2004.   
[8] D. Donjerkovic, Y. Loannidis, and R. Ramakrishnan, “Dynamic Histograms: Capturing Evolving Data Sets,” Proc. 16th IEEE Int’l Conf. Data Eng. (ICDE), 2000.   
[9] P. Dutta, M. Grimmer, A. Arora, S. Bibyk, and D. Culler, “Design of a Wireless Sensor Network Platform for Detecting Rare, Random, and Ephemeral Events,” Proc. Fourth IEEE/ACM Int’l Symp. Information Processing in Sensor Networks (IPSN), 2005.

[10] F. Furfaro, G.M. Mazzeo, and C. Sriangelo, “Exploiting Cluster Analysis for Constructing Multi-Dimensional Histograms on Both Static and Evolving Data,” Proc. 10th Int’l Conf. Extending Database Technology (EDBT), 2006.   
[11] W.R. Heinzelman, A. Chandrakasan, and H. Balakrishnan, “Energy-Efficient Communication Protocol for Wireless Microsensor Networks,” Proc. 33rd Hawaii Int’l Conf. System Sciences (HICSS), 2000.   
[12] J.M. Hellerstein, W. Hong, S. Madden, and K. Stanek, “Beyond Average: Toward Sophisticated Sensing with Queries,” Proc. Second IEEE/ACM Int’l Workshop Information Processing in Sensor Networks (IPSN), 2003.   
[13] J. Hill and D. Culler, “Mica: A Wireless Platform for Deeply Embedded Networks,” IEEE Micro, vol. 22, pp. 12-24, 2002.   
[14] C. Intanagonwiwat, R. Govindan, and D. Estrin, “Directed Diffusion: A Scalable and Robust Communication Paradigm for Sensor Networks,” Proc. ACM MobiCom, 2000.   
[15] M. Li and Y. Liu, “Underground Structure Monitoring with Wireless Sensor Networks,” Proc. Sixth IEEE/ACM Int’l Symp. Information Processing in Sensor Networks (IPSN), 2007.   
[16] S. Li, Y. Lin, S. Son, J. Stankovic, and Y. Wei, “Event Detection Services Using Data Service Middleware in Distributed Sensor Networks,” Telecomm. Systems J., vol. 26, 2004.   
[17] Z. Li and B. Li, “Loss Inference in Wireless Sensor Networks Based on Data Aggregation,” Proc. Third IEEE/ACM Int’l Symp. Information Processing in Sensor Networks (IPSN), 2004.   
[18] S. Lindsey, C. Raghavendra, and K. Sivalingam, “Data Gathering in Sensor Networks Using Energy Delay Metric,” Proc. IPDPS Workshops, 2001.   
[19] S. Madden, M.J. Franklin, and J.M. Hellerstein, “TAG: A Tiny Aggregation Service for Ad-Hoc Sensor Networks,” Proc. Fifth Symp. Operating System Design and Implementation (OSDI), 2002.   
[20] X. Meng, T. Nandagopal, L. Li, and S. Lu, “Contour Maps: Monitoring and Diagnosis in Sensor Networks,” Computer Networks, 2006.   
[21] V. Mhatre, C. Rosenberg, D. Kofman, R. Mazumdar, and N.B. Shroff, “Design of Surveillance Sensor Grids with a Lifetime Constraint,” Proc. First European Workshop Wireless Sensor Networks (EWSN), 2004.   
[22] S. Nath, P.B. Gibbons, S. Seshan, and Z.R. Anderson, “Synopsis Diffusion for Robust Aggregation in Sensor Networks,” Proc. Second ACM Conf. Embedded Networked Sensor Systems (SenSys), 2004.   
[23] S.-J. Park, R. Vedantham, R. Sivakumar, and I.F. Akyildiz, “A Scalable Approach for Reliable Downstream Data Delivery in Wireless Sensor Networks,” Proc. ACM MobiHoc, 2004.   
[24] I. Solis and K. Obraczka, “Efficient Continuous Mapping in Sensor Networks Using Isolines,” Proc. Second IEEE Ann. Int’l Conf. Mobile and Ubiquitous Systems (MobiQuitous), 2005.   
[25] Y. Tian, E. Ekici, and F. Ozguner, “Energy-Constrained Task Mapping and Scheduling in Wireless Sensor Networks,” Proc. Workshop Resource Provisioning and Management in Sensor Networks (RPMSN), 2005.   
[26] N. Xu et al., “A Wireless Sensor Network for Structural Monitoring,” Proc. Second ACM Conf. Embedded Networked Sensor Systems (SenSys), 2004.   
[27] M. Younis, P. Munshi, and E. Al-Shaer, “Architecture for Efficient Monitoring and Management of Sensor Networks,” Proc. Sixth IFIP/IEEE Int’l Conf. Management of Multimedia Networks and Services (MMNS), 2003.

![](images/ed7f7dbc16715c863257c9a7aedafcc9ee76da3bbab0767ca73c5c6dd0f14602.jpg)



Mo Li received the BS degree in computer science and technology from Tsinghua University, Beijing, in 2004. He is currently working toward the PhD degree in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include wireless sensor networks, pervasive computing, network security, and peer-to-peer computing. He is a member of the IEEE.

![](images/d2dbddd51f31469866ea95f4c3168367308b050589d085f1985ec5427f4a0064.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, Beijing, in 1995, the MA degree from Beijing Foreign Studies University, Beijing, in 1997, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is currently with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He is also an adjunct professor at

Xi’an Jiaotong University, Jilin University, and Ocean University of China. His research interests include wireless sensor network, peer-topeer computing, and pervasive computing. He is a member of the ACM and a senior member of the IEEE.

![](images/77c9fcdec1765f49ef9f9c9a414cf1cadd4ca44958b6139df9d559bb988e692d.jpg)



Lei Chen received the BS degree in computer science and engineering from Tianjin University, Tianjin, China, in 1994, the MA degree from the Asian Institute of Technology, Bangkok, Thailand in 1997, and the PhD degree in computer science from the University of Waterloo, Ontario, Canada, in 2005. He is currently an assistant professor in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research

interests include multimedia databases, sensor databases, peer-topeer databases, and probabilistic databases. He is a member of the ACM and the IEEE.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.