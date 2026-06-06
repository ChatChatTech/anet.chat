# Gradient Boundary Detection for Time Series Snapshot Construction in Sensor Networks

Jie Lian, Member, IEEE, Lei Chen, Member, IEEE, Kshirasagar Naik, Member, IEEE, Yunhao Liu, Senior Member, IEEE, and Gordon B. Agnew, Member, IEEE

Abstract—In many applications of sensor networks, the sink needs to keep track of the history of sensed data of a monitored region for scientific analysis or supporting historical queries. We call these historical data a time series of value distributions or snapshots. Obviously, to build the time series snapshots by requiring all of the sensors to transmit their data to the sink periodically is not energy efficient. In this paper, we introduce the idea of gradient boundary and propose the Gradient Boundary Detection (GBD) algorithm to construct these time series snapshots of a monitored region. In GBD, a monitored region is partitioned into a set of subregions and all sensed data in one subregion are within a predefined value range, namely, the gradient interval. Sensors located on the boundaries of the subregions are required to transmit the data to the sink and, then, the sink recovers all subregions to construct snapshots of the monitored area. In this process, only the boundary sensors transmit their data and, therefore, energy consumption is greatly reduced. The simulation results show that GBD is able to build snapshots with a comparable accuracy and has up to 40 percent energy savings compared with the existing approaches for large gradient intervals.

Index Terms—Wireless sensor networks, query processing, planar graph.

# 1 INTRODUCTION

DUE to recent advances in computing and wireless communication technologies, wireless sensors are available to measure real-world phenomena. A large number of sensors are densely deployed in a specific region to form a wireless sensor network. These sensor networks are designed for monitoring environment and supporting user queries. In many real applications [1], [2], [3], [4], users are interested in analyzing the changes of value distributions, called snapshots, of the monitored geographic region over time. Fig. 1 shows an example of a snapshot.

From a temporal point of view, queries over a sensor network can be categorized into real-time query and historical query. The response of a real-time query is solely dependent on the current data of the monitored region and the responses are required to be real time. One example of a real-time query is “find the location with the highest temperature in the monitored area now.” Many existing approaches are designed to support such real-time queries [2], [3], [7], especially for target tracing [8], [9], [12], [17], [18]. On the other hand, the response of a historical query relies on historical data. Historical queries are useful in many environment-monitoring applications such as monitoring Yosemite National Park [4]. In the Yosemite National

. J. Lian, K. Naik, and G.B. Agnew are with the Department of Electrical and Computer Engineering, University of Waterloo, Waterloo, ON, Canada, N2L 3G1.   
E-mail: {jlian, knaik}@swen.uwaterloo.ca, gbagnew@engmail.uwaterloo.ca.   
. L. Chen and Y. Liu are with the Department of Computer Science, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong. E-mail: {leichen, liu}@cs.ust.hk.

Manuscript received 30 Dec. 2005; revised 11 Aug. 2006; accepted 9 Nov. 2006; published online 9 Jan. 2007.

Recommended for acceptance by I. Stojmenovic.

For information on obtaining reprints of this article, please send e-mail to: tpds@computer.org, and reference IEEECS Log Number TPDS-0519-1205.

Digital Object Identifier no. 10.1109/TPDS.2007.1057.

Park project, a typical historical query is “find the average temperature in a certain region for each year from 1992 to 1999.” To support this type of query, the sink maintains time series snapshots with a tolerable error for a monitored region. Usually, sensors are battery powered with a limited energy resource and batteries are nonreplicable in many situations [2], [3], [12]. Therefore, energy efficiency is an important goal for constructing time series snapshots. Obviously, periodically transmitting data from all sensors to the sink is not energy efficient. Although many query processing approaches proposed in the literature [7], [9], [11], [12], [13], [14], [15], [16] can be extended to build time series snapshots, as their primary concerns are on processing realtime queries, they cannot address historical queries well.

In this paper, we propose the Gradient Boundary Detection (GBD) algorithm to build time series snapshots for a monitored region. The GBD algorithm depends on the concept of gradient boundary (GB) as follows. In real applications such as temperature monitoring, there exists a high similarity of the temperature values in the vicinity, as demonstrated in Fig. 1.

In Fig. 1, the monitored region is partitioned into a set of subregions, and the value distribution in each subregion is limited by a predefined range of temperature. To find a snapshot at a given time for the region, a solution is to obtain the readings from sensors located close to the boundaries of all subregions. In this way, sensors that are not located at the vicinity of the boundaries do not transmit their data to the sink, resulting in reduced energy consumption. Based on this idea, we propose the GBD algorithm to support snapshot construction. The major contributions of this work are listed as follows:

We introduce the concept of virtual surrounding face (VSF), which is used to approximate the boundaries of partitioned subregions.

![](images/adb9402c19e6452454d193fe2d5a885267850b5d30d5b90c90108119aa014810.jpg)



Fig. 1. Temperature value distribution of permafrost in Canada. Even though the temperature value distributed here is scaled over Canada, it still reflects the realistic situation for smaller areas.

We propose the GBD algorithm to construct snapshots with low transmission cost.   
We compare the performance of the proposed algorithm with the existing approaches and show that GBD is superior to the existing approaches.

The rest of the paper is organized as follows: We review the related work in Section 2 and identify the problems in the existing approaches. A few terms and the idea of the work are given in Section 3. We present the GBD algorithm in Section 4. The simulation methodology is introduced in Section 5, and the performance of GBD is evaluated in Section 6. Finally, we conclude this work in Section 7.

# 2 RELATED WORK

A number of research results have been published on collecting data from sensor networks for energy-efficient query processing [2], [3], [9], [11], [16]. However, most of them focus on supporting real-time queries, and only a few of them aim at building time series snapshots for historical queries. In addition, location detection techniques play an important role for query processing in sensor networks. In this section, we review those approaches as follows:

Directed Diffusion (DD) [2] is a well-known approach to support event-based real-time queries. In such a query, a sensor reports data only if it detects occurrences of some specified events. Extending DD to support historical queries leads to all sensors joining the data collection process and it is therefore not suitable for building time series snapshots. VigilNet [12] implements an integrated system with a focus on tracking mobile targets. Similar to DD, VigilNet is designed to handle event-based real-time queries and is not suitable for historical queries. LEACH [16] is a scalable adaptive clustering protocol in which nodes in the vicinity are organized into clusters. Sensors in a cluster communicate with the cluster header (CH), which directly transmits the processed data to the sink. Even though LEACH can be extended for collecting snapshots of a monitored region, it is not energy efficient due to the longdistance transmissions from sensors to CHs and from CHs to the sink. In general, energy consumption for transmission is a quadratic or hyperquadratic function of a transmission distance [27]. The long-distance transmissions involved in LEACH consume a much larger amount of energy than normal multihop transmissions in sensor networks [27].

Madden et al. [3] propose the Tiny Aggregation Service (TAG) to reduce the energy cost of processing aggregative real-time queries (for example, Sum, Average, Max, Min, and so forth) by using in-network aggregation. Some other work based on TAG supports aggregative queries, such as Cougar [13] and TinA [14]. Cougar not only processes real-time queries by partial data aggregation, but also reduces packet payload by merging data packets. TinA utilizes the temporal coherence among data collected from the same sensor to reduce the number of transmissions. However, these approaches have two major drawbacks when they are extended to support historical queries. First, these approaches are proposed to handle aggregative queries such that data are aggregated during the collection phase. If we use these aggregated data to build the snapshots at the sink, it will result in a large mean error compared with the actual value distribution of the monitored region. Second, in the data collection phase, these approaches have no knowledge about the incoming historical queries; thus, it is difficult to decide which aggregation operators to use. For example, if the operators Average, Max, and Min are chosen to collect data, it cannot answer an incoming historical query: Find all subregions in which the temperature value is between 20- C and 25- C. To overcome these two drawbacks, these approaches have to transmit all of the sensed data back to the sink without any aggregation, resulting in a high transmission cost.

Recently, Kotidis proposed a Data Cluster (DC) approach [11] with a focus on supporting aggregative queries. In DC, a set of nodes is voted as representative nodes based on the value distribution of their neighbor nodes. Then, the representative nodes answer queries on behalf of other nodes. The DC approach can be easily extended to construct snapshots of monitored regions, but with the disadvantage of high cluster construction and maintenance cost.

To obtain time series snapshots of a monitored region, all sensors participating in a query process should know their geographic locations. For outdoor applications, the existing location detection techniques can be classified into two types: Global Positioning System (GPS)-based and GPS-free techniques. The former uses the GPS [21], [22] and can determine locations within a few meters. On the other hand, in GPS-free techniques [23], [24], [25], [26], a small number of master nodes are selected which know their locations precisely. To determine the locations of other nodes, each node with an unknown location broadcasts a message to its neighbors. The master nodes measure the received signal strength from the message initiator and compute the location based on the measurements. In either way, sensor nodes know their location with high accuracy.

# 3 OVERVIEW OF GBD ALGORITHM

In this section, we demonstrate the environment model, introduce the basic idea of the GBD algorithm, define related terminology, and present the idea of VSF, which is a major part of GBD.

# 3.1 GBD Algorithm

We consider the snapshot construction problem to support historical queries in environment monitoring. Fig. 2 shows an example of the value distribution of a monitored region. This environment model is realistic for many applications such as temperature, humidity, and pressure monitoring [3], [4]. In Fig. 2a, the monitored region is divided into three subregions, $R _ { 1 } , R _ { 2 } ,$ , and $R _ { 3 } ,$ . The temperature values of all points in $R _ { 1 } , R _ { 2 }$ and $R _ { 3 }$ are in the ranges 22-24-C, $2 0 { - } 2 2 ^ { \circ } \bar { \mathrm { C } } ,$ and $1 8 { - } 2 0 ^ { \circ } \mathrm { C } ,$ respectively. The dotted (dashed) curves denote the boundaries between two adjacent subregions. To obtain time series snapshots, sensors are evenly deployed in the region (Fig. 2b). The sensors sense the environment periodically and send data to the sink. The sink uses the received data to recover the snapshot of the region.

![](images/68df24a85d6c308d36d52ecd0bf8abdc501ec7f172076db9ed41656765ef96a8.jpg)



(a)   
![](images/38789cdcbb5219ae2b6694b73dc462152ce615d9144fae99ce8767cfdf592fb2.jpg)



(b)   
Fig. 2. (a) Value distribution of the monitored region. (b) Densely deployed sensors in the region.

Obviously, letting all sensors transmit their data to the sink is not energy efficient. This is because values distributed in the vicinity of any location in the monitored region are highly correlated. One sensed value for a location can be used to recover the value distribution in the vicinity of the location. One energy efficient solution is to ask sensors close to the boundaries of the subregions to transmit their data to the sink, and the sink uses these data to recover the boundaries. In this way, sensors far away from the boundaries do not need to send their data to the sink, thus saving energy associated with these transmissions. The GBD algorithm realizes this goal, and an example of GBD is shown in Fig. 2b. In Fig. 2b, to detect the boundary of $R _ { 1 }$ , sensors close to the boundary of $R _ { 1 }$ form a chain that is an approximation of the boundary. In GBD, a sensor, namely, node u, is selected to send two messages traversing the chain in two directions: clockwise and counterclockwise. The traversing messages collect the sensed values of the sensors along the chain and the two messages reach a node v. Then, v forwards the messages to the sink. Finally, the sink can find a boundary of R1 by using the received data. Similar steps can be used to obtain other boundaries. In this way, GBD can obtain an approximated snapshot of a monitored region at any given time. In the rest of this section, we define terminology and describe how to use the idea of the VSF to approximate the boundaries of subregions.

![](images/14e1e0c3b6edc48e580ca937d2477d0cdb8b769ba29133b6ef15950f13637535.jpg)



(a)   
![](images/10e46f08de557f177b83c7f557b7476444a78590180af01d2b7485e6abf11f3e.jpg)



(b)   
Fig. 3. Partitions for a monitored region with different gradient levels. (a) Grid representation of three levels of gradients. (b) Partition with five levels of gradients.

# 3.2 Environmental Model

Before we discuss the GBD algorithm, we state the environment model. In the rest of the paper, we use temperature monitoring as an example to state the GBD algorithm.

Grid representation of a snapshot. For a realistic monitored region, the snapshot can be represented by a temperature value distribution over a two-denominational real plane in which each point is associated with a temperature value. However, it is difficult to maintain values for all points in the real plane since there are an infinite number of points. Instead, we partition the monitored region into a grid structure with integer resolution and maintain a temperature value for each cell in the grid structure. For simplicity, we construct snapshots for a square region, which is represented by a w  w grid. Each cell in the grid is associated to a temperature value. The value distribution in the grid representation is an approximation of the real value distribution in the real plane. The larger the value of w is, the higher the accuracy that can be achieved by using the grid structure comparing with the value distribution in the real plane. An example of a grid structure is shown in Fig. 3a.

GB and gradient region. By using the grid representation, each snapshot of a w  w grid can be stored in a 2D array grid½w½w, where grid½i½j maintains the temperature value at the cell in the ith row and jth column, where $1 \leq i \leq w$ and $1 \leq j \leq w .$ Each cell, except the ones on the edge of the grid, has four neighbors (up, down, left, and right). To capture the snapshot of a monitored region at a given time, the temperature distribution is subdivided into m levels of gradients: $\mathrm { G D } _ { m } { = } \{ [ T _ { k } , T _ { k + 1 } ) | 1 \le k \le m \}$ , where

$T _ { 1 } < T _ { 2 } < . . . < T _ { m + 1 }$ are temperature values and $[ T _ { k } , T _ { k + 1 } )$ is a temperature range.

With a given $\mathrm { G D } _ { m }$ for a w  w grid, the kth gradient region, $\scriptstyle { R _ { k } , }$ is defined as a subregion containing all cells in the grid with their temperature values in the range $[ T _ { k } , T _ { k + 1 } )$ Þ. The boundary of $R _ { k }$ is defined as a set of cells that belong to $R _ { k }$ and each cell has at least one neighbor in a gradient region other than $R _ { k } .$ . The boundary of $R _ { k }$ is called a GB, denoted by $B _ { k } .$ As shown in Fig. 3a, the monitored region is partitioned into three gradient regions $R _ { 1 }$ (dark gray region), $R _ { 2 }$ (light gray region), and $R _ { 3 }$ (the rest of the monitored region) by three levels of gradients, $\mathrm { G D _ { 3 } } = \{ ( 1 8 , 2 0 ) , ( 2 0 , 2 2 ) , ( 2 2 , 2 4 ) \}$ g. A gradient region may not be enclosed by one connected boundary.

Performance metrics of a snapshot. In this paper, we focus on constructing snapshots and detecting the boundaries of gradient regions. To support historical queries, GBD divides the system time into time intervals and the sink collects a snapshot during each interval. Historical queries are answered by using the snapshots. To obtain a more accurate snapshot of the monitored region, more levels of gradients can be used. As shown in Fig. 3b, five levels of gradients are used, resulting in five regions, denoted by $R _ { 1 }$ to $R _ { 5 }$ .

Let $g r i d _ { T } [ w ] [ w ]$ denote the actual value distribution of a region with the grid representation and let $g r i d _ { R } [ w ] [ w$  denote the recovered value distribution (snapshot) by using a detection technique. Two application-dependent metrics are used to measure the accuracy of a snapshot: Mean Absolute Error $( M _ { E R R } )$ and Boundary Error $( B _ { E R R } )$ .

For a given region with a w  w grid, MERR is defined as the mean value of differences between actual value distribution and the recovered value distribution. The formal definition is given in (1) as follows:

$$
M _ {E R R} = \left(\sum_ {i = 1} ^ {w} \sum_ {j = 1} ^ {w} | g r i d _ {T} [ i ] [ j ] - g r i d _ {R} [ i ] [ j ] |\right) / w ^ {2}. \tag {1}
$$

For a monitored region with a $w \times w$ grid representation and $\mathrm { { G D } } _ { m } = \{ [ T _ { k } , T _ { k + 1 } \bar { ) } | 1 \leq k \leq m - 1 \}$ , we define $\partial ( x , y )$ as a testing function as follows:

$$
\begin{array}{l} \partial (i, j) = \\ \left\{ \begin{array}{l l} 1 & \exists k: (g r i d _ {T} [ i ] [ j ] \in [ T _ {k}, T _ {k + 1})) \wedge (g r i d _ {R} [ i ] [ j ] \in [ T _ {k}, T _ {k + 1})), \\ 0 & o t h e r w i s e. \end{array} \right. \\ \end{array}
$$

Then, $B _ { E R R }$ is defined in (2) as follows:

$$
B _ {E R R} = 1 - \sum_ {i = 1} ^ {w} \sum_ {j = 1} ^ {w} \partial (i, j) / w ^ {2}. \tag {2}
$$

$\partial ( x , y )$ is used to determine if the actual value and the recovered value of a given cell belong to the same gradient region. Denominator $\overline { { w ^ { 2 } } }$ denotes the total cells (area) of a region in the grid representation. The numerator denotes the total number of cells whose actual value and recovered value belong to the same gradient region. Hence, BERR denotes the percentage of the areas of incorrectly recovered gradient regions over the total area.

The $\bar { M _ { E R R } }$ is used by the mean-error sensitive queries such as “get the average temperature in a subarea.” However, some applications disregard $M _ { E R R } ,$ but desire to have a small $B _ { E R R }$ such as a query in Fig. 1: “find the subregions in which temperature is in the range between $4 . 5 ^ { \circ } C$ and $6 . 5 ^ { \circ } C . ^ { \prime \prime }$ For such applications, the value distribution inside a gradient region is not of interest, whereas $B _ { E R R }$ has a greater impact on the accuracy of the query response.

![](images/efd663724299d477521ae91e25ffdf8fdfbdee64a64ec1bbe627a63eefebd588.jpg)



Fig. 4. Face partition and face boundary traversal.

# 3.3 Face Traversal

As illustrated in Fig. 2, the GBD algorithm recovers the snapshot by traversing the chains close to the gradient boundaries. GBD uses face traversal to realize this goal. Some preliminary terms and a network model related to face traversal are discussed in this section.

Unit disk graph (UDG). UDGs are accepted models of sensor networks in which all nodes have an identical transmission range $r _ { s }$ [2], [3], [5], [6]. Let V denote a set of nodes in a sensor network. We define UDGðV Þ as a UDG in which an edge $e _ { u v }$ between nodes u and v exists if and only if the euclidean distance between u and v is no longer than $r _ { s } .$ . For an edge $e _ { u v } \in U D G ( V )$ , u and v are called UDG neighbors.

Planar graph and Gabriel graph (GG). Face traversing plays an important role in GBD and can only be applied on a planar graph. A graph is called planar if the graph has no two edges crossing one another. To planarize a ${ \bar { U } } D G ( V ) .$ , a deduced subgraph of $U D G ( V )$ , called ${ \mathrm { G G } } ,$ , is employed. The GG on $U D G ( V )$ is defined as a graph $G G ( V )$ so that, for each edge $e _ { u v } \in U D G ( V ) , \ e _ { u v } \in G G ( V )$ if and only if the circle with $e _ { u v }$ as a diameter does not contain any other nodes. For an edge $e _ { u v } \in G G ( V )$ , nodes u and v are called Gabriel neighbors. A localized algorithm to find $G G ( V )$ has been presented in [6]. For each node $u ,$ let $N _ { U D G } ( u )$ and $N _ { G G } ( u )$ denote the sets of UDG and Gabriel neighbors of $u ,$ respectively.

Faces in a planar graph. The edges in a planar graph partition the network region into a set of faces [5], [6]. A face in a planar graph is a continuous subarea bounded by one or more close sequences of edges. For example, in Fig. 4, the network region is partitioned into four faces, $F _ { 1 } , \ F _ { 2 }$ (dark gray region), $F _ { 3 }$ (light gray region), and $F _ { 4 } ,$ where $F _ { 4 }$ is the unbounded region outside the border of a network graph. Note that face $F _ { 3 }$ is bounded by two sequences of edges:

$$
u \rightarrow u _ {1} \rightarrow u _ {2} \rightarrow \dots \rightarrow u _ {1 0} \rightarrow u _ {1 1} \rightarrow u _ {1 2} \rightarrow u _ {1 1} \rightarrow u _ {1 0} \rightarrow u _ {1 3}
$$

$$
\rightarrow y \rightarrow z \rightarrow u, \text { and } v _ {1} \rightarrow v _ {2} \rightarrow v _ {3} \rightarrow v _ {4} \rightarrow v _ {1}.
$$

Face traversal. A face in a planar graph can be traversed by employing the Right-Hand Rule (R-Rule) or the Left-Hand Rule (L-Rule) [5], [6], or both. In the R-Rule, a person explores a face by keeping her right hand on the walls (edges) and she will eventually visit all edges on the face. In the L-Rule, a person explores a face by using her left hand. We use Fig. 4 as an example to illustrate face traversing. Starting from $u ,$ to traverse $F _ { 1 }$ by R-Rule, u sends a traversing message to v in the form of travðsource; $[ ( d e s t , r u l e ) , \ldots ] )$ , where the source is the message sender, dest is the recipient, rule is R-Rule or L-Rule, and ½. . . means that there may be many ðdest; ruleÞ pairs. For node u, the message is $t r a v ( u , ( v , R i g h t ) )$ Þ. When v receives the message, it sends $t r a v ( v , ( w , R i g h t ) )$ to w. Repeating the step by all nodes receiving the message, $F _ { 1 }$ is traversed counterclockwise. Similarly, u can use trav $\left( u , \left( z , L e f t \right) \right)$ to traverse $F _ { 1 }$ clockwise.

![](images/36e35caba52dbc44b2f589e8649cd843e77c7b285c671a087bc5d5cf695337d7.jpg)



(a)

![](images/cca96ed161cc811f0b5e9c48d9385569f6f0e7bcdbbba241f675a6f566e85a60.jpg)



(b)   
Fig. 5. Illustration of VSF. (a) Crossing edges (dotted lines) of GB $B _ { 1 }$ and (b) VSF $F _ { 1 }$ for GB $B _ { 1 }$ .

# 3.4 VSF of GB

As illustrated in Fig. 2b, the major purpose of the GBD algorithm is to find chains of sensors to approximate the gradient boundaries. GBD achieves this goal by using the concept of VSF as follows:

The sensors in GBD are classified into two types: gradient boundary sensors (GB sensors) and internal sensors. A sensor u is called a GB sensor if there exists a Gabriel neighbor v of u with $g r a d ( u ) \neq g r a d ( v )$ , where gradðuÞ denotes the gradient region in which u is located. In other words, two neighbor nodes v and u are GB sensors if they are Gabriel neighbors of each other and they are in different gradient regions. Then, $e _ { u v }$ is called a crossing edge. A sensor that is not a GB sensor is called an internal sensor. Fig. 5a shows the GG of a sensor network and only the sensors in $R _ { 1 }$ and $R _ { 2 }$ are shown. In the figure, the dotted lines denote crossing edges and the solid lines denote edges other than crossing edges. In Fig. 5a, nodes $u , v , y ,$ and z are GB sensors. Nodes $w , x , z _ { 5 } ,$ and $z _ { \mathrm { 6 } }$ are internal sensors.

VSF of a GB. In a planar graph, for any two faces that share some edges, if one of the shared edges is ignored, the two faces are merged into one face with a larger area. Consider the GG shown in Fig. 5a in which face $F _ { 1 }$ is bounded by the edge sequence $u  v  w  x  y  z  u$ and face $F _ { 2 }$ i s bounded by the edge sequence

$$
y \to z \to z _ {1} \to z _ {2} \to z _ {3} \to z _ {4} \to y.
$$

If the crossing edge $e _ { y z } ,$ which is shared by $F _ { 1 }$ and $F _ { 2 } ,$ , is ignored, then $F _ { 1 }$ and $F _ { 2 }$ are merged into one face bounded by an edge sequence:

$$
u \rightarrow v \rightarrow w \rightarrow x \rightarrow y \rightarrow z _ {4} \rightarrow z _ {3} \rightarrow z _ {2} \rightarrow z _ {1} \rightarrow z \rightarrow u.
$$

If we repeatedly merge all faces that intersect with $B _ { 1 }$ (the GB of $R _ { 1 } )$ by ignoring the crossing edges, eventually we find a unique face containing $B _ { 1 }$ . This face is called the VSF of $B _ { 1 }$ . The result of the face merging process is shown in Fig. 5b in which face $F _ { 1 }$ (light gray region) is the VSF of $B _ { 1 }$ . $F _ { 1 }$ is bounded by two disconnected edge sequences: One is the chain with solid dots and the other is the chain with hollow dots. To traverse a VFS, a node determines its next visited node by using the way discussed in Section 3.3, except that the node ignores all of its crossing edges. After the sink obtains the sensed values of all sensors located on the VSFs (the two chains), it approximates $B _ { 1 }$ by a simple geometric computation.

The node on the VSF boundary is called a VSF sensor. Two Gabriel neighbor nodes on the same VSF boundary are called VSF neighbors of each other. As shown in Fig. 5a, v and w are VSF sensors, and w and x are VSF neighbors. GB sensors are VSF sensors, but VSF sensors in the same gradient region are not necessarily GB sensors. For example, in Fig. 5a, w and x are VSF sensors but not GB sensors.

# 4 DISTRIBUTED GBD ALGORITHM

Based on the idea of VSF, we design the GBD algorithm for time series snapshot construction. GBD consists of three components as follows:

Time series snapshots and historical queries. Since the purpose of GBD is to store long-term time series snapshots for the monitored area, the time interval between successive snapshots is expected to impact the accuracy of query responses. In addition, queries may not ask for historical data concerning the exact time of maintained snapshots and, therefore, there should be a way to answer queries pointing to any given time.   
VSF traversal. All nodes run an algorithm to select starting nodes from which VSF traversing is initialized. When a message traverses a VSF, some information on the visited VSF nodes is collected in the messages.   
Data collection. During the VSF traversal, for each VSF node $u ,$ if u detects that a data collection condition holds, then u transmits the GB data to the sink.

# 4.1 Time Series Snapshots and Historical Queries

GBD divides time into a sequence of predetermined time interval $\Delta t$ and periodically constructs a snapshot for the monitored area at time k-t for $k > 0$ . For a historical query related to the value distribution at an arbitrary time $\dot { t } ^ { \prime }$ satisfying $k \Delta t < t ^ { \prime } < ( k + 1 ) \Delta t ,$ , the sink cannot directly answer the query since it does not store the snapshot at time t 0 . Instead, the sink computes the value distribution by a linear combination of the snapshots at k-t and $( k + 1 ) \dot { \Delta t }$ as follows: Let $g r i d _ { t k } [ w ] [ w ]$ and $g r i d _ { t ( k + 1 ) } [ w ] [ w ]$ denote the snapshots at time k-t and $( k + 1 ) \Delta t ,$ respectively. The snapshot $g r i d _ { t ^ { \prime } } [ w ] [ w ]$ at time t 0 can be computed as follows:

$$
\begin{array}{l} \forall 1 \leq i, j \leq w: g r i d _ {t ^ {\prime}} [ i ] [ j ] \\ = g r i d _ {t k} [ i ] [ j ] \frac {(k + 1) \Delta t - t ^ {\prime}}{\Delta t} + g r i d _ {t (k + 1)} [ i ] [ j ] \frac {t ^ {\prime} - k \Delta t}{\Delta t}. \tag {3} \\ \end{array}
$$

The time interval cannot be too large or too small. Since the purpose of GBD is to maintain long-term time series snapshots for a monitored area, it is better to choose an hourly-based time interval, that is, one snapshot per one or two hours. If the time interval is too small, the current snapshot may be very similar to the previous snapshot, resulting in redundant data transmissions. If the time interval is too large, it is difficult to compute an accurate estimation of the value distribution at a time between two consecutive snapshots. The determination of time interval is a design parameter and depends on applications.

# 4.2 VSF Traversal

Let UDGðV Þ represent a network with node set V and GG ðV Þ denote the GG of V . In GBD, each node u in V maintains the following local information:

Node u knows its own geographic location and the geographic locations of all neighbor nodes in $N _ { U D G } ( u )$ . From $N _ { U D G } ( u )$ , u can compute its Gabriel neighbor set $N _ { G G } ( u )$ [5] without data transmissions. In addition, u knows all temperature readings of nodes in $N _ { U D G } ( u )$ .   
Node u knows the gradient information $\mathrm { G D } _ { m } =$ $\left\{ [ T _ { 1 } , T _ { 2 } ) , [ T _ { 2 } , T _ { 3 } ) , \dots , [ \bar { T _ { m } } , T _ { m + 1 } ) \right\}$ specified by the sink. Many existing techniques [19], [20] can be used to distribute $\mathrm { \bar { G } D } _ { m } . \ \mathrm { \bar { G } D } _ { m }$ distribution is only performed if $\mathrm { G D } _ { m }$ varies.   
Node u knows the sink location and a routing path from u to the sink. This information can be obtained during $\mathrm { G D } _ { m }$ flooding, as demonstrated in [3].   
The sink maintains the location-ID pairs of all sensors in the network, which can be collected while initializing the deployed network.

VSF traversing needs to handle two cases: 1) Some nodes must be selected to start VSF traversing and 2) each node involved in VSF traversing must be able to determine whether VSF traversing is terminated.

# 4.2.1 Starting Node Selection of VSF Traversal

For each VSF in GBD, a VSF message is used to traverse the VSF to collect data from the traversed VSF nodes. This process increases the message size after visiting each VSF node. When the message size exceeds the maximum packet size, the message will be forwarded to the sink and a new empty traversal message will continue the face traversal. According to this feature, it is better to select starting nodes of VSF, which has the longest euclidian distance to the sink among its VSF neighbors. As the example in Fig. 6 illustrates, the sink is located at the top-right corner. If $v _ { 4 }$ is selected as a starting node, one traversal message will visit nodes $v _ { 4 } \longrightarrow v _ { 3 } \longrightarrow v _ { 2 } \longrightarrow v _ { 1 } \longrightarrow u .$ . This message becomes longer after visiting a new node and the node holding the message is farther from the sink, resulting in more energy being consumed to forward this large message over a long path. If we can choose node u as a starting node, the visiting node sequence is $u  v _ { 1 }  v _ { 2 }  v _ { 3 }  . . .$ , which puts the message closer to the sink after each traversal. Hence, we try to choose nodes with longer distances to the sink as starting nodes for each VSF.

![](images/2f87002a1ba343af6b0d16884ab80b9f37ca11b08eb275637a6b37e3d3a36788.jpg)



Fig. 6. Example of VSF traversal.

Based on locally stored information, each node u can determine if it is a GB node and only GB nodes participate in the process to select starting nodes. To avoid all of the GB nodes being selected and to choose nodes with longer distance to the sink as starting nodes, each GB node starts its face traversal at a different time. The longer the distance to the sink, the earlier a GB node starts its face traversal. The starting time is computed as $t _ { \mathrm { s t a r t } } = \Delta t _ { p } \ ( d _ { s } / r _ { s } )$ , where $\Delta t _ { p }$ denotes the time to send one packet with the maximum size, $d _ { s }$ is the distance from the node to the sink, and $r _ { s }$ is the transmission radius. The reader may note that $t _ { \mathrm { s t a r t } }$ does not mean the node transmitting its packet at time $t _ { \mathrm { s t a r t } }$ . Instead, the node starts its transmission process at $t _ { \mathrm { s t a r t } }$ . For example, in the contention-based protocol $\mathrm { C S M A } / \mathrm { C D }$ , the node obtains a time slot for its transmission at $t _ { \mathrm { s t a r t } } + c \Delta t _ { s } ,$ where $c \Delta t _ { s }$ is a random back off delay and $t _ { s }$ is the used time slot.

If a GB node u receives a face traversal message before u starts its own face traversal, u forwards the traversal message to the next node and cancels its own face traversal. The starting node selection process is presented as Algorithm 1.

Algorithm1 Starting Node Selection for Double VSF Traversal 

<table><tr><td>1:</td><td>Input: node u; temperature values of u&#x27;s neighbors; Gradient  $GD_{mi}$ ; sink location;</td></tr><tr><td>2:</td><td>BEGIN</td></tr><tr><td>3:</td><td>if (u is not a GB node) then exit;</td></tr><tr><td>4:</td><td>u computes its time to start its face traversal and set a timer;</td></tr><tr><td>5:</td><td>if( u receives a face traversal message before the timer expires) then u forwards the message and stop timer;</td></tr><tr><td>6:</td><td>else if( the timer expires first) then u starts its face traversal;</td></tr><tr><td>7:</td><td>END</td></tr></table>

When node u is selected as a starting node, u starts VSF traversing in two directions by using the approach discussed in Section 3.3. During VSF traversing, each traversed node u determines its next traversed node by ignoring all of the crossing edges of u.

VSF traversing uses a traversing message in the form of $\mathrm { M S G } ( I D _ { s } , t r a v ( . . . )$ ; dataÞ, where IDs is the ID of the starting node, travð. . .Þ is the traversing method defined in Section 3.3, and the data field is used for data collection to be discussed in Sections 4.2 and 5.1. In the example shown in Fig. 6, if u is selected as a starting node, u sends a message $\mathrm { M S G } ( I D _ { u } ,$ ; $t r a v ( u , ( v _ { 1 } , R i g h t ) , ( w _ { 1 } , L e f t ) ) , d a t a _ { u } )$ to nodes $v _ { 1 }$ and w1. When $v _ { 1 }$ receives this message, $v _ { 1 }$ knows itself to be a VSF node. Then, $v _ { 1 }$ modifies the message to $\mathrm { M S G } ( I D _ { u } .$ ; trav $( v _ { 1 } , ( v _ { 2 } , R i g h t ) ) , d a t a _ { v 1 } )$ and sends the message to $v _ { 2 } .$ . Similarly, v2 sends $\mathrm { M S G } ( I D _ { u } , t r a v ( v _ { 2 } , ( v _ { 3 } , R i g h t ) ) , d a t a _ { v 2 } )$ to v3, and so on. Thus, all VSF nodes are traversed.

# 4.2.2 Termination of VSF Traversal

To avoid unnecessary traversing on a VSF, we define a termination condition for a VSF node to decide whether the received traversing message can be discarded. The termination condition is stated as follows: Since each starting node performs traversing in two directions, intermediate VSF nodes may receive more than one traversing messages. For two VSF neighbors, u and $v ,$ receiving two traversing messages with different traversal rules, if the message received by u will traverse v next and the message received by v will traverse u next, these two messages are discarded by u or v depending on which node transmits its message first. If u transmits its message to v first, then v discards both of the messages. If v transmits first, then u discards both of the messages.

# 4.3 Data Collection of GBD

In the data collection phase, the $I D _ { s }$ and the temperature readings of the sensors related to the VSF traversal are transmitted to the sink for snapshot construction. There are two ways of selecting transmitted data. The first approach is that, in the VSF traversal, each node simply transmits its own reading to the next traversed node. When some nodes collect enough data from previously traversed nodes (such as the data exceeding the maximum packet size), these nodes transmit the data with the locations of the data to the sink. This method works well to construct snapshots aiming to minimize $B _ { E R R } .$ . In the second approach, since the sensors with extreme values in the vicinity of traversed sensors have a greater impact on the accuracy of $M _ { E R R }$ than other sensors, the traversed VSF nodes forward the information of its neighbors with the highest and lowest values to the sink. When the sink receives all the GB data within a time interval, the sink uses these data to recover the snapshot of the monitored region. The snapshot recovery process is discussed in Section 5.

However, in the second approach discussed above, the data received by the sink from the VSF nodes are redundant. This is because a GG is derived from a UDG graph by removing edges between non-Gabriel neighbors. According to the definition of ${ \mathrm { G G } } ,$ the longer edges in UDG have higher probabilities to be removed. In VSF traversing, messages are solely sent to Gabriel neighbors, indicating that each traversal passes the message to the next VSF node over a short distance. Two successive traversed nodes within a short distance may report redundant data, which results in additional transmissions. Hence, we use a skipping technique to reduce the transmission cost of sending redundant data to the sink as follows:

Skipping traversal is applied when three or more successively traversed VSF nodes are located within the transmission range of the first node. Assume that nodes $u ,$ v, and w are three traversed VSF nodes in sequence. First, u sends a traversing message to v and also forwards the information of u’s two neighbor nodes with extreme values to the sink. When v receives the traversing message, v sends the traversing message to w and uses a skipping algorithm to decide whether or not to forward the information of v’s two neighbor nodes with extreme values to the sink. The skipping algorithm is given in Algorithm 2.

Algorithm 2 Skipping Algorithm during VSF Traversal   
1: Input: VSF node v receiving a traversing message containing the last node u which reports data to the sink.
2: Output: determine whether v reports data to the sink;
3: BEGIN
4:    w ← the next traversed node of v
5:    if (u and w are one-hop neighbors of each other)
6:    return true;
7:    else
8:    return false;
9:    end if
10: END

In the skipping algorithm, v can determine whether u and w are neighbors of each other by computing their distance. If u and w are not neighbors of each other, v forwards the information of v’s two neighbor nodes with extreme values to the sink. Otherwise, v does not forward the information and we say that v has been skipped.

# 4.4 VSF Representation in Discrete Grid Structure

Theoretically, we construct a snapshot by using continuous VSFs in a 2D real plane, so the construction will always succeed in this situation. Since it is difficult to represent VSFs in a continuous manner, a discrete grid structure discussed in Section 3.2 is deployed to represent these VSFs. In this case, the selection of the discrete grid structure has a significant impact on the construction of continuous VSFs. If the number of grids in a region is low, the VSF cannot be correctly recovered. On the other hand, if the number of grids is very high, the grid structure will have a heavy computation cost and requires a large amount of memory. Hence, there is a trade-off between the accuracy of the construction and the maintenance cost.

For practical deployment of GBD, we can determine the grid size with respect to the region size as follows: Assume that a monitored region is a $W \times W$ square area. The monitored region is partitioned into a w  w grid structure in which each grid is a square with width (height) $r _ { g } .$ Let $r _ { s }$ denote the transmission radius of a node. Then, we can determine the grid size $r _ { g }$ as follows:

First, as the simulation studies show (Sections 5 and 6), if the transmission radius $r _ { s }$ is more than 10 times the width $r _ { g }$ of a grid, the constructed VSF has a considerably high accuracy. For the same test configurations, further increase of the ratio $( r _ { s } / r _ { g } = 1 0 )$ does not change the results significantly. For a ratio $r _ { s } / r _ { g }$ less than 10, the smaller the ratio is, the lower the probability of successfully constructing the VSF.

Second, for each practical application, the monitored region $( W \times W )$ and the transmission radius $r _ { s }$ of a node are fixed. The ratio $\sigma = W / r _ { \mathrm { : } }$ s approximately indicates the width of the deployed network in terms of hop counts. This ratio is unchangeable due to the requirement of the application.

Hence, in practical applications, it is better to choose the grid size $r _ { g }$ such that $r _ { g } \le W / ( 1 0 \sigma )$ , where W and - are two fixed parameters of an application. For $r _ { g } > W / ( 1 0 \sigma )$ , the constructed VSF may be distorted. Meanwhile, for a known $\boldsymbol { r } _ { g } ,$ we can compute $w = W / r _ { g } .$

# 5 SIMULATION METHODOLOGY

We design a network simulator to evaluate the performance of the GBD algorithm. We define the simulation environment in this section and evaluate the performance of GBD by comparing with the DC algorithm [11] in Section 6. The simulation environment consists of two parts: the network model and the model of test regions (value distribution of a monitored region).

# 5.1 Network Model

We randomly deploy 2,000 homogenous sensors on a $2 0 0 \times$ 200 grid with a transmission radius $r _ { s } = 1 0 \AA$ . Each sensor has a unique ID. The sink is placed at one corner of the region. Two nodes communicate with each other by using media access control (MAC) layer packets. For each packet, we adopt an IEEE 802.11a as the MAC layer standard with modification of packet length. IEEE 802.11a specifies a packet with a 34-octet header and up to 2,312-octet data field. Due to the fact that retransmission of long packets over unreliable wireless channels is high, the maximum length of a packet in the paper is limited to 128 octets. Sensor $I D _ { s }$ s and real-valued temperatures are represented by two octets each. Since the only useful part of a packet at the sink is the data field, packet merging is performed by both GBD and $\scriptstyle \mathrm { { D C } } ,$ that is, the sensors near the sink wait a certain period of time to collect all data from distant sensors, merge all data to a small number of packets, and forward the merged data packets to the sink.

# 5.2 Test Region of Simulation Study

We adopt two environment models to generate the value distribution of an area in simulation. The first model uses a diffusion process to generate complex test environments to evaluate performance $( M _ { E R R }$ and $B _ { E R R } )$ . In this model, we do not simulate the changes of the test regions over time, that is, there is no temporal relationship between any two test regions. The second model generates a simple dynamic environment. In this model, a sequence of test regions is generated in a temporal order to simulate changes of value distributions over time. This model is used to evaluate performance of GBD in terms of $B _ { E R R }$ in a dynamic environment.

# 5.2.1 Diffusion Process Model

We adopt a diffusion process to simulate the value distribution in a test region. In the diffusion process, a test region (network region) is partitioned into a grid structure with w  w resolution. We randomly select m1 number of cells in the grid structure as the sources. Each source is assigned a random value within a range converted to a gray level such that the value distribution can be represented by an image. For each nonsource cell, its value is initialized to a fixed value. Fig. 7a shows the source cells (tiny dark or white points) in a network region. In a diffusion step, the value of each nonsource cell is upgraded to the mean value of its four nearest neighbor cells. All sources retain their original values. The diffusion step repeats a large number of times, say, 1,500, to generate an image (Fig. 7b).

![](images/e1c74a6ec39318df6fc99adc3518e0843b7b330c5ce9e50bde5d512d5f56ba67.jpg)



(a)

![](images/07a2fc42533e0c4ad39547ca5faeb84679c36840e46be02c22dd7945eacbcac8.jpg)



(b)

![](images/149ad716ef8c066230a71fad1b5c87599ae60bfd88d0dc4cb7aee8293e447f6f.jpg)



（c）

![](images/89380755f0c374f5b1be29eff50c5a2e558d5574783cd4367eac64dd03ea5627.jpg)



(d）  
Fig. 7. Simulated value distribution of the monitored region. (a) An area with 150 sources. (b) After diffusion. (c) After softening. (d) Shown with gradient.

The image in Fig. 7b may be too sharp to reflect the actual value distribution in a real scenario, so a softening step is used in which $m _ { 2 }$ number of cells are randomly selected from the image as the sources and the original sources are discarded. Then, the diffusion step repeats to generate the final image (Fig. 7c). Fig. 7d shows the gradient boundaries of Fig. 7c by setting $T _ { k } - T _ { k + 1 } = 5 0$ .

In simulation, each test region is a fixed square region partitioned into a $2 0 0 \times 2 0 0$ unit square cells. A certain number of sources are chosen from the grid structure and each source is assigned to a randomly generated real number in [0, 255] to denote its temperature. In real applications, the range [0, 255] can be projected to any temperature ranges such as ½20:5-C; 30:5-C on a summer day. The temperature of a nonsource cell is initialized to the mean value of all sources. Diffusion and soften steps are performed 1,500 times to generate a test region. The number of sources m1 measures the complexity of a test region. In simulations, $m _ { 1 }$ is taken from a list [50, 100, 150, 200, 250, 300].

In GBD, the sink uses the collected data to recover the snapshot of the monitored region by using a diffusion process as follows: From the collected data, the sink converts each pair of $( I D _ { v i } , T _ { v i } )$ to $( X Y _ { v i } , T _ { v i } )$ , where $X Y _ { v i }$ is the x and y coordinates of a sensor $v _ { i } .$ If a cell contains a sensor $v _ { i } ,$ the cell is a source with temperature $T _ { v i }$ . For each nonsource cell, its temperature is initialized to the mean value of all sources. Next, the diffusion step is repeated until the snapshot reaches a stable state, that is, the difference between two successive snapshots is lower than a threshold value.

# 5.2.2 Simple Dynamic Environment Model

In this model, we consider the temperature distribution in a $2 0 0 \times 2 0 0$ test region located at a cone-shaped hill with the apex at the center of the region. In general, when a subregion in the cone has a smaller height, its temperature is higher too. In this model, the temperature of a point in the test region is inversely proportional to its height. This feature is illustrated in Fig. 8, where the darker area indicates higher height and lower temperature in the area.

(a)   
(b)   
（c）  
![](images/3ce8a9aaad5007e412a6d94e0dca047715a911c64d66cc1db30dbe506fa7a61c.jpg)



Fig. 8. The changes of temperature distribution of the monitored region over time. (a) The temperature distribution at 8:00 am. (b) The distribution at 10:00 am. (c) The distribution at 12:00 am.

GBD is designed for long-term snapshot construction and collects data on an hourly basis. To model the temperature changes over time, we consider a typical day from 8:00 am to 1:00 pm and construct one snapshot per hour. For simplicity and without loss of generality, we assume that each point in the test region increases by 1- C per hour. Hence, from 8:00 am to 1:00 pm, each point increases by 6- C. Fig. 8 shows three temperature distributions at 8:00 am, 10:00 am, and 12:00 pm. From the figure, we can observe that the gradient regions change over time. Even though this model is simple, it captures most of the characteristics when the temperature distribution changes over time in a typical day. We use this simple dynamic model because it requires less computation power for the simulation compared to the diffusion model.

# 6 EXPERIMENTAL RESULTS AND DISCUSSION

Based on the simulation environment discussed in Section 5, we show properties of the GBD algorithm and compare its performance with the DC algorithm [11].

# 6.1 Experiment Results in the Diffusion Process Model

# 6.1.1 Properties of GBD

In GBD, the VSF nodes send their related data to the sink for snapshot construction. Without using GBD, a simple solution is that all normal boundary (NB) nodes report their data. Here, an NB node u is defined as a node with at least one neighbor that is not in the same gradient region as u. However, two reasons prohibit the use of this method.

First, since GB may not enclose the outer boundary of the network graph, it is possible that a part of a network region is not monitored. As shown in Fig. 9, even though NB nodes can detect the gradient boundaries (dotted curves), no NB nodes are located at the part of the border of the monitored regions, resulting in no sensor in the subregions close to the border-reporting data. If these uncovered subregions are large, the recovered snapshots have low accuracy. In addition, it is difficult to determine which node is a border node in a randomly deployed sensor network. Simply using the distance from a node to the border to determine the border nodes results in either too many or too few nodes being selected as border nodes.

![](images/137be74497ed4f97797ac1424bd7c3845f537cbe813d79ff0e80a42d8af1ec47.jpg)



Fig. 9. Gradient boundaries (dotted curves) of the monitored region with $T _ { k + 1 } - T _ { k } = 5 0$ for all possible integers k.

Second, since sensors are densely deployed, the number of NB nodes is much larger than the VSF nodes and the data collected by all of the NB sensors in the vicinity are redundant. Fig. 10 shows NB nodes and VSF nodes in a simple test region. Hence, VSF traversing is used to reduce the total number of nodes reporting data to the sink.

By using test regions generated by the diffusion process, Fig. 11 plots different types of nodes by using simulation. The labels of curves denote the gradient interval $\mathrm { G L } = ( T _ { k + 1 } - T _ { k } )$ . For example, in Fig. 11a, for a test region with 100 sources and GL ¼ 20, the total number of NB nodes is 1,621. In Fig. 11, we make the following observations:

In Fig. 11a, it can be observed that the total number of NB nodes increases with the increase in the number of sources in the monitored regions. This is because a larger number of sources result in more nodes located on the gradient boundaries. It is obvious that the number of gradient regions is smaller if the gradient interval is larger. Hence, the total number of NB nodes decreases with an increase in the gradient interval GL. Fig. 11b depicts that the total number of GB nodes is an increasing function of the number of sources. Intuitively, the more complex a monitored region is, the longer the GB and the larger the number of GB nodes. Fig. 11c shows the total number of traversed VSF nodes that are not GB nodes. This number also indicates the number of nodes located on the border of the monitored region, but not located on any gradient boundaries. When the number of sources increases, the portion of the border of the monitored region not covered by gradient boundaries decreases. Hence, the number of the VSF but not GB nodes is a decreasing function of the number of sources, as shown in Fig. 11c. The reported data from these nodes help to draw the boundary of a recovered snapshot with higher accuracy.

![](images/96d767cf05239e2c3ac4ea90939c864cdfc92313da1dc72e87497a83a9912651.jpg)



(a)

![](images/58b470fd3cc8dd6d46f71e40607224c0e05b9e095986c725676351fba260e574.jpg)



(b)   
Fig. 10. The boundary nodes for a GB (dark circle). (a) Small dark dots are NB nodes. (b) Small dark dots are GB nodes. The number of NB nodes is much larger than the number of GB nodes.

![](images/b767ad2cab55a6d975aa39600306b0666b8b1a25b16bd32203f57ccff0fd91bd.jpg)



(a)   
![](images/e7a1d2a99666d7fa5ec5b75efca5474193cf5aa8d90bf1f90e70aa5f4d25ffdd.jpg)



(b)   
![](images/3ecb452d5b0d948fd1534e72123b49403ee702d64eee8031234c0efd6c865b63.jpg)



（c）  
Fig. 11. Numbers of different types of nodes for networks with 2,000 nodes in the GBD algorithm. (a) Total number of NB nodes. (b) Total number of GB nodes. (c) Total number of VSF but not GB nodes.

We also observed in Figs. 11a and 11b that VSF traversal reduces the total number of NB nodes reporting data to the sink by 40-50 percent. Hence, VSF traversal not only reduces the transmissions of redundant data, but also detects the value distribution on the border of a monitored region.

6.1.2 Comparison of Transmission Cost of GBD and DC We use the total number of transmitted octets, denoted by $C ,$ to measure the efficiency of the algorithms. Then, we compute $M _ { E R R }$ and $B _ { E R R }$ for the original value distribution and the recovered snapshot. Since GBD and DC have different transmission costs, we do not directly compute $M _ { E R R }$ and $B _ { E R R }$ of the two approaches. Rather, we run GBD with varied parameters and generate $M _ { E R R }$ and $B _ { E R R }$

![](images/5c04182d20dcc06e778c5d82e37aa36c8291e7ed888c0c5453a02805c816e088.jpg)



(a)   
![](images/0a9c4daa67e33265b60e6f62a47253a7012933078a43808f260a19e35e7969ae.jpg)



(b)   
Fig. 12. $M _ { E R R }$ and related cost of the GBD algorithm. (a) $M _ { E R R }$ of GBD for networks with 2,000 nodes. (b) Total transmission cost C of GBD to achieve $M _ { E R R }$ specified in (a).

with the associated cost C. Then, we find C of $\scriptstyle \mathrm { { D C } , }$ which generates the same $M _ { E R R }$ and $B _ { E R R }$ of GBD. Finally, we compare the costs of GBD and DC. Each data point in all of the figures in this section is the average of 10 sample runs.

Comparison results for $\mathbf { M } _ { \mathbf { E R R } } . \mathbf { F i g } .$ . 12 shows the $M _ { E R R }$ of the recovered snapshots and the total costs for test regions with varied number of sources by using GBD. In Fig. 12, the labels of curves denote the gradient interval $\mathrm { G L } = ( T _ { k + 1 } - T _ { k } )$ . For example, in Fig. 12a, for a test region with 100 sources and ${ \mathrm { G L } } = 2 0$ , the recovered snapshot has $M _ { E R R } = 1 . 9 6$ . In Fig. 12b, we can find that the total cost C related to $M _ { E R R } = 1 . 9 6$ is 248,000 octets.

To achieve the same $M _ { E R R }$ for the same test field, we list the transmission cost C of DC in Fig. 13. To give a clear view of comparison, we also list the costs of GBD in the same figure. For example in Fig. 13a, for the curve labeled with $\mathrm { D } \mathrm { \bar { C } - G } \mathrm { L } = 2 0$ and a test region with 100 sources, we can find $C = 3 6 5 , 0 0 0 ,$ , which gives the total transmission cost of DC to achieve the $M _ { E R R } = 1$ :96 found in Fig. 12a. To achieve the same $M _ { E R R } = 1 . 9 6 ,$ GBD transmits 248,000 octets in total (the curve labeled with GBD-GL-20 in Fig. 13a).

According to Fig. 13, we observed that GBD saves up to 50 percent of the total cost of DC to construct snapshots with the same $M _ { E R R }$ for the same test regions. This performance gain can be analyzed as follows:

Both GBD and DC have an initialization phase and a data collection phase for each snapshot construction. In the former phase, GBD and DC build their structures (VSF for GBD and representative nodes for DC). In the latter phase, GBD and DC use the built structures to send data to the sink. In addition, VSF traversal in GBD occurs in this phase.

In the initialization phase of GBD, all sensors broadcast their sensed data once for the first snapshot construction. For the successive snapshot constructions, only sensors that change their gradient regions broadcast their sensed data once in the initialization phase. Similarly, in the initialization phase of $\scriptstyle \mathrm { { D C } , }$ all sensors send a maximum of six messages to select representative nodes to construct the first snapshot. In later snapshot constructions, sensors changing their gradient regions broadcast their values and all sensors affected by these changes participate in the new representative node selection process in the initialization phase.

![](images/34c620fa9308b2a14583ecb2cb2e7b5d30f732b6171ac2a7b01c015c167163eb.jpg)



(a)   
![](images/02dee0f0340ef373756aeebc5d69af63aa3ce6eaa34f052bd1398a6c197d5f71.jpg)



(b)   
Fig. 13. Total transmission costs of GBD and DC to achieve the $M _ { E R R }$ level specified in Fig. 12a. (a) Total transmission cost C for $\mathrm { G L = 2 0 }$ and 30. (b) Total transmission cost C for GL ¼ 40 and 50.

Let $C _ { 1 }$ denote the cost of the initialization phase and let $C _ { 2 }$ denote the cost of the data collection phase. We have $C = C _ { 1 } + C _ { 2 }$ . We observed (details not shown in the paper) that the data collection cost $C _ { 2 }$ of GBD is approximately 10 percent more than $C _ { 2 }$ of DC. Combining this observation with the total costs shown in Fig. 13, we conclude that the initialization cost $C _ { 1 }$ of GBD is much smaller than $C _ { 1 }$ of DC.

Obviously, in the initialization phase, GBD has different costs in the first and the later snapshot constructions. The similar result holds for DC too. The results in Fig. 13 only show the performance gain of GBD for the first snapshot construction. One may argue that the performance gain of GBD may not be achieved in the later snapshot constructions. However, the performance gain almost holds in successive snapshot constructions and the reason is as follows: Since GBD is designed for long-term environmental monitoring, the time interval between two successive snapshots is hourly-based. In reality, temperature values change significantly after a long, say, one or two hours time interval. As a consequence, a large number of sensors change their gradient regions. These changed sensors cause almost all sensors in DC to participate in the selection process of representative nodes, which leads to a similar initialization cost as the one in the first snapshot construction. This discussion is verified in the experimental studies shown in Section 6.2 under the dynamic environment.

Comparison results for $\mathbf { B _ { E R R } }$ . In this set of experiments, we compare GBD and DC by considering the cost C to achieve a certain level of $B _ { E R R }$ . Fig. 14 plots $B _ { E R R }$ of recovered snapshots of GBD and its associated cost C has been given in Fig. 12b. In Fig. 14, the labels of curves denote the gradient interval $\mathrm { G L } = ( T _ { k + 1 } - T _ { k } )$ . For example, in Fig. 14, for a test region with 100 sources and $\mathrm { G L = 2 0 }$ , the recovered snapshot has $B _ { E R R } = 0 . 1$ . Then, in Fig. 12b, we can find that the total cost C related to $B _ { E R R } = 0 .$ :1 is 248,000 octets.

![](images/b5673e716f7ff0c2a64c40db4940db2f39be8cb505ca10877c0eed1f6b7aa417.jpg)



Fig. 14. $B _ { E R R }$ of GBD with the cost C given in Fig. 12b.

Fig. 15 plots the cost C of DC and GBD for achieving the same $B _ { E R R }$ levels specified in Fig. 14. In Fig. 15, we observed that GBD saves up to 50 percent of the total cost of DC to construct snapshots for the same test regions.

As discussed above, both GBD and DC have the initialization cost $C _ { 1 }$ and the data collection cost $C _ { 2 }$ . To achieve the same $B _ { E R R }$ levels, we observed (from the experimental results not shown here) that the data collection cost $C _ { 2 }$ of GBD is approximately 5-10 percent higher than the cost of DC for a small gradient interval $\bigl ( \mathrm { G L } = 2 0 \bigr )$ , and GBD saves 10- 40 percent of the data collection cost of DC for a large gradient interval (GL ¼ 30, 40, and 50). Therefore, in boundary detection applications, both the initialization process and the data collection process of GBD contribute to the performance gain of GBD compared with DC.

We also find that, in the initialization phase, the cluster construction (representative node selection) cost for DC can be higher than the data collection cost in the worst case. This worst case occurs when the value distribution of most subregions changes dramatically such that the environmental change exceeds the prespecified gradient interval. In this case, most of the representative nodes are voted again. However, many applications supporting historical queries operate on this worst-case scenario. This is because the sink collects/samples snapshot data on an hourly basis, resulting in the temperature distribution changing significantly between two successive snapshots. On the other hand, GBD has no such initialization cost except nodes changing their gradient regions reporting their values once before each construction. This reporting cost in the initialization phase is local and small compared to the data collection cost of GBD. The experimental results in Section 6.2 support this observation in a dynamic network model. Hence, the overall performance of GBD is superior to DC. According to the simulation results, GBD can save up to 50 percent of the total cost of DC to construct a snapshot with the same $M _ { E R R }$ and $B _ { E R R }$ under the environment models generated by the diffusion process.

![](images/1b4349c1d1d62eed8f6b1fa0b8d1fc9a472d8758d474edbc3e5d7032d3d561aa.jpg)



(a)   
![](images/a0f376d8261ed4ec396663ba59a51cd7f839b490f329ee0de9e7381a6b7332b5.jpg)



(b)   
Fig. 15. Total transmission costs of GBD and DC to achieve the $B _ { E R R }$ level specified in Fig. 14. (a) Total transmission cost C for $\mathrm { G L } = 2 0$ and 30. (b) Total transmission cost C for GL ¼ 40 and 50.

![](images/ffb8ada4a32db507f5ec7a3efe013c276107feaca55ce84246e3b63149d0222d.jpg)



(a)

![](images/c7cb347490ae063680142dc39c3082faa7dd0024d7c83f23c4382b91c01a0aa6.jpg)



(b)

![](images/9c7facbe0fa5dea9d3afc1c619c5475c6d1ad8fa16eced96fa9099004fab0bfc.jpg)



（c）  
Fig. 16. Applying GBD for $B _ { E R R }$ only. (a) Detected GB (circle). (b) GB bounded by two VSFs (inner curve and outer curve of the circle). (c) Detected GB.

# 6.2 Experimental Results in Simple Dynamic Model

In Section 6.1, we applied GBD to reduce $M _ { \mathrm { E R R } }$ and $B _ { \mathrm { E R R } } .$ In addition, GBD is applied to fulfill the features of test regions generated by the diffusion process. More specifically, each VSF node reports the highest and lowest values of its neighbor nodes to the sink. The sink uses these values to recover the snapshots based on the diffusion process. If we only focus on minimizing $B _ { \mathrm { E R R } }$ , which is the primary goal of GBD, there is a more efficient solution as follows:

Fig. 16a shows a circular GB. By using GBD, two VSFs are constructed inside and outside the circular GB (Fig. 16b). The VSF nodes report their values to the sink. Based on the received data, the sink draws the VSF in the recovered grid. More specifically, for any two VSF neighbors, the sink draws a line between the two neighbors and assigns values to all points on the line based on the temperature of the two end nodes of the line. After drawing the VSF, for any point p in the test region but not located on the VSF, p sets its temperature to the value of a point located at the boundary of VSF with the shortest distance to p. Fig. 16c shows the recovered GB by using this method. Even though the recovered temperature distribution inside the gradient region significantly differs from the original distribution in terms of $\begin{array} { r } { \dot { M } _ { \mathrm { E R R . } } } \end{array}$ , we obtain a very close estimation of the GB in terms of the $B _ { \mathrm { E R R } }$ .

By using the preceding method and the dynamic environment model with six temporally ordered snapshots (Section 5.2.2), we compare GBD and DC and show the results in Table 1. In the experiment, the gradient interval is configured to be 25 (gray level in the image). This interval can be easily mapped to any real temperature setting.

TABLE 1 Costs and $B _ { \mathrm { E R R } }$ for GBD and DC in Networks with 2,000 Nodes 

<table><tr><td>Construction Time of snapshot</td><td>Algorithm</td><td>Ini cost (in octets)</td><td>Total cost (in octets)</td><td> $B_{ERR}$ </td></tr><tr><td rowspan="2">8:00 am</td><td>GBD</td><td>75316</td><td>147560</td><td>1.33%</td></tr><tr><td>DC</td><td>262400</td><td>321340</td><td>0.77%</td></tr><tr><td rowspan="2">9:00 am</td><td>GBD</td><td>26448</td><td>96596</td><td>1.66%</td></tr><tr><td>DC</td><td>213532</td><td>279472</td><td>4.88%</td></tr><tr><td rowspan="2">10:00 am</td><td>GBD</td><td>36252</td><td>88340</td><td>2.03%</td></tr><tr><td>DC</td><td>223336</td><td>282276</td><td>5.44%</td></tr><tr><td rowspan="2">11:00 am</td><td>GBD</td><td>25536</td><td>92508</td><td>1.53%</td></tr><tr><td>DC</td><td>212620</td><td>281560</td><td>5.32%</td></tr><tr><td rowspan="2">12:00 noon</td><td>GBD</td><td>31046</td><td>116874</td><td>2.97%</td></tr><tr><td>DC</td><td>218130</td><td>286593</td><td>9.32%</td></tr><tr><td rowspan="2">1:00 pm</td><td>GBD</td><td>31350</td><td>103594</td><td>1.34%</td></tr><tr><td>DC</td><td>218434</td><td>282374</td><td>6.17%</td></tr></table>

According to the results shown in Table 1, we have the following observations: First, in most of the cases, GBD constructs snapshots with much lower $B _ { E R R }$ than DC. Second, the initialization costs of DC for the snapshot at 8:00 am is slightly higher than the initialization cost of the later snapshots. This is because, for any two successive snapshots, approximately $1 / 3$ of the sensors change their gradient regions in the latter snapshot and these sensors lead more nodes in their vicinities to update their representing lists. Therefore, the majority of the sensors participate in the selection process of representative nodes, resulting in similar initialization costs in all snapshot construction. This observation corroborated our discussion in Section 6.1.2 and shows that the simulation results obtained in Section 6.1.2 not only hold for the first snapshot construction, but also approximately hold for all later snapshot constructions. Third, the data collection cost of GBD is slightly higher than the collection cost of DC, which is similar to the observation obtained in Section 6.1.2. Finally, the total cost of DC is almost twice the total cost of GBD. Hence, the experimental results show that GBD outperforms DC in the dynamic environment for large gradient intervals.

# 6.3 Load Balancing

One question not addressed for GBD is the load-balancing problem. In DC, representative nodes consume much more energy than normal nodes. DC achieves load balancing by preventing nodes with low energy levels from becoming representative nodes. More specifically, a node in DC with a low energy level will not respond to the received construction message of the representative node.

In GBD, comparing with other non-VSF nodes, VSF nodes of all gradient boundaries are responsible for traversing VSFs and collecting data for the sink. Hence, VSF nodes have much higher energy consumption than other nodes. However, the load-balancing problem can be easily solved in GBD under two scenarios as follows:

First, in many situations, GBD does not have a loadbalancing problem at all since, in real applications, the changes of temperature distributions in a monitored area automatically balance the load. Considering the temporal snapshots in Fig. 8, we observe that the gradient boundaries change significantly over time. The boundary change causes that different sets of sensors form the VSFs of the same gradient range at different time, which results in load balancing for all sensors. From the same simulation associated with Table 1, under the dynamic environment model, we list the statistics of the total number of messages sent by all sensors during the VSF traversal in Table 2. In Table 2, we can find that 829 VSF nodes sent one VSF message, 432 VSF nodes sent two messages, and 131 nodes sent three messages. Only 11 nodes sent more than six messages and 80 nodes (less than 5 percent of the total nodes) sent more than four messages. For long-term operations, load balancing is not a problem in this type of scenario such as outdoor temperature monitoring.

TABLE 2 Statistics for the Number of VSF Messages Sent by Sensors during the Six Snapshot Constructions 

<table><tr><td>TX#</td><td>1</td><td colspan="2">2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>Node#</td><td>829</td><td colspan="2">432</td><td>194</td><td>103</td><td>44</td><td>25</td><td>4</td><td>0</td><td>1</td></tr><tr><td colspan="11"></td></tr><tr><td>TX#</td><td>10</td><td>11</td><td>12</td><td>13</td><td>14</td><td>15</td><td>16</td><td>17</td><td>18</td><td>19</td></tr><tr><td>Node#</td><td>5</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

TX denotes transmission.

In the second scenario, we assume that the changes of value distributions for a monitored area cannot automatically balance the loads for all sensors in GBD. In this case, GBD needs to balance the load by modifying itself. GBD can easily achieve load balancing by adjusting the initial value of gradient configuration at different time. For example, assume that, initially, we use four levels of gradient $\mathrm { G D _ { 4 } } = \{ ( 1 0 , 2 0 ) , ( 2 0 , 3 0 ) , ( 3 0 , 4 0 ) , ( 4 0 , 5 0 ) \}$ with gradient interval GL ¼ 10. After n number of snapshot constructions, the sink can issue a new query with $\mathrm { \bar { G D } _ { 5 } = }$ fð5; 15Þ; ð15; 25Þ; ð25; 35Þ; ð35; 45Þ; ð45; 55Þg to all sensors. Since GL is not changed in the new query $( \mathrm { G L } = 1 0 ) .$ , the recovered snapshots will retain its accuracy (same $M _ { \mathrm { E R R } }$ and $B _ { \mathrm { E R R } } )$ . However, since the new configuration changes the gradient boundaries, the overloaded VSF nodes in the old configuration become non-VSF nodes, resulting in a balanced load for all nodes in long-term operations. If we choose a relatively large $n ,$ the cost incurred in new query dissemination can be ignored. On the other hand, the sink can also add a tunable parameter of GD in the old query, which triggers all sensors to automatically change their GD after n snapshot constructions. In this way, the new query dissemination cost is removed.

# 7 CONCLUDING REMARKS

In this paper, we propose a GBD algorithm for time series snapshot construction to support historical queries for sensor networks. In GBD, a monitored region is partitioned into a set of gradient regions based on the value distribution and all sensor readings in each region are in the same predefined gradient range. GBD employs the concept of VSF to approximate the boundaries of gradient regions and constructs snapshots of the monitored region by traversing all the VSFs. GBD is designed to minimize $B _ { E R R }$ and $\bar { M _ { E R R } } \overset { \sim } { _ { \mathstrut } }$ and reduce the total transmission cost in constructing snapshots with a given accuracy level.

We compare the performance of GBD with the DC algorithm. According to the experimental results, for applications focusing on minimizing the $M _ { E R R . }$ , GBD has a similar transmission cost of DC in the data collection phase. For applications sensitive to the $B _ { E R R } ,$ in the data collection phase, GBD has a similar transmission cost as DC for small gradient interval and saves 10-40 percent of the transmission cost of DC for large gradient intervals. However, for both applications, the initialization cost of GBD is significantly less than the cluster construction and maintenance cost related to DC. Therefore, GBD can reduce up to 50 percent of the overall cost of DC to construct a snapshot with a given accuracy level for both the $M _ { E R R }$ and the $\bar { B } _ { E R R }$ .

# ACKNOWLEDGMENTS

The authors thank the anonymous reviewers for their helpful comments. This work was supported in part by the NSERC (Canada), the Hong Kong RGC grant HKUST6169/ 07E, the NSFC Key Project Grant 60533110, and the National Grand Fundamental Research 973 Program of China under Grant 2006CB303000.

# REFERENCES

[1] I.F. Akyildiz, W. Su, Y. Sankarasubramaniam, and E. Cayirci, “Wireless Sensor Networks: A Survey,” Computer Networks, vol. 38, no. 4, 2002.   
[2] C. Intanagonwiwat, R. Govindan, and D. Estrin, “Directed Diffusion: A Scalable and Robust Communication Paradigm for Sensor Networks,” Proc. ACM MobiCom, 2000.   
[3] S. Madden, M. Franklin, J. Hellerstein, and W. Hong, “TAG: A Tiny Aggregation Service for Ad-Hoc Sensor Networks,” Proc. Symp. Operating Systems Design and Implementation (OSDI ’02), 2002.   
[4] J. Lundquist, D. Cayan, and M. Dettinger, “Meteorology and Hydrology in Yosemite National Park: A Sensor Network Application,” Information Processing in Sensor Networks, Apr. 2003.   
[5] E. Kranakis, H. Singh, and J. Urrutia, “Compass Routing on Geometric Networks,” Proc. Canadian Conf. Computational Geometry, pp. 51-54, 1999.   
[6] P. Bose, P. Morin, I. Stojmenovic, and J. Urrutia, “Routing with Guaranteed Delivery in Ad Hoc Wireless Networks,” Wireless Networks, vol. 7, no. 6, pp. 609-616, 2001.   
[7] A. Mairwaring, J. Polastre, R. Szewczyk, D. Culler, and J. Anderson, “Wireless Sensor Networks for Habitat Monitoring,” Proc. ACM Workshop Wireless Sensor Networks and Applications, 2002.   
[8] P. Juang et al., “Energy-Efficient Computing for Wildlife Tracking: Design Tradeoffs and Early Experiences with ZebraNet,” Proc. Conf. Architectural Support for Programming Languages and Operating Systems, Oct. 2002.   
[9] P. Zhuang, C. Sadler, S. Lyon, and M. Martonosi, “Hardware Design Experiences in ZebraNet,” Proc. ACM Conf. Embedded Networked Sensor Systems, Nov. 2004.   
[10] I. Stojmenovic, M. Seddigh, and J. Zunic, “Dominating Set and Neighbor Elimination Based Broadcasting Algorithms for Wireless Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 13, no. 1, pp. 14-25, Jan. 2002.   
[11] Y. Kotidis, “Snapshot Queries: Towards Data Centric Sensor Networks,” Proc. Int’l Conf. Data Eng., 2005.   
[12] T. He et al., “VigilNet: An Integrated Sensor Network System for Energy-Efficient Surveillance,” ACM Trans. Sensor Networks, 2005.   
[13] Y. Yao and J. Gehrke, “Query Processing for Sensor Net,” Proc. Conf. Innovative Data Systems Research (CIDR ’03), 2003.   
[14] M.A. Sharaf, J. Beaver, A. Labrinidis, and P.K. Chrysanthis, “TinA: A Scheme for Temporal Coherency-Aware In-Network Aggregation,” Proc. ACM Workshop Data Eng. for Wireless and Mobile Access (MobiDE ’03), 2003.   
[15] J. Beaver, M.A. Sharaf, A. Labrinidis, and P.K. Chrysanthis, “Location-Aware Routing for Data Aggregation in Sensor Networks,” Proc. Geo Sensor Networks Workshop, 2003.

[16] W. Heinzelman, A. Chandrakasan, and H. Balakrishnan, “Energy-Efficient Communication Protocols for Wireless Microsensor Networks,” Proc. Int’l Conf. Systems Science, 2000.   
[17] Q. Fang, F. Zhao, and L. GuiBas, “Lightweight Sensing and Communication Protocols for Target Enumeration and Aggregation,” Proc. ACM MobiHoc ’03, 2003.   
[18] A. Arora et al., “A Line in the Sand: A Wireless Sensor Network for Target Detection, Classification, and Tracking,” Computer Networks, vol. 46, no. 5, pp. 605-634, Dec. 2004.   
[19] A. Qayyum, L. Viennot, and A. Laouiti, “Multipoint Relaying for Flooding Broadcast Messages in Mobile Wireless Networks,” Proc. Hawaii Int’l Conf. System Sciences (HICSS ’02), pp. 3898-3907, 2002.   
[20] I. Stojmenovic, S. Seddigh, and J. Zunic, “Dominating Sets and Neighbor Elimination-Based Broadcasting Algorithms in Wireless Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 13, no. 1, pp. 14-25, Jan. 2002.   
[21] P. Enge and P. Misra, “Special Issue on GPS: The Global Positioning System,” Proc. IEEE, pp. 3-172, Jan. 1999.   
[22] B. Hofmann-Wellenhof, H. Lichtenegger, and J. Collins, Global Positioning System: Theory and Practice. Springer, 1997.   
[23] A.S. Krishnakumar and P. Krishnan, “On the Accuracy of Signal Strength-Based Location Estimation Techniques,” Proc. IEEE INFOCOM ’05, pp. 642-650, 2005.   
[24] S. Ray, W. Lai, and I.C. Paschalidis, “Statistical Location Detection with Sensor Networks,” IEEE Trans. Information Theory, vol. 52, no. 6, 2006.   
[25] N. Patwari, A.O. Hero III, M. Perkins, N. Correal, and R. O’Dea, “Relative Location Estimation in Wireless Sensor Networks,” IEEE Trans. Signal Processing, special issue on signal processing in networks, 2002.   
[26] S. Capkun, M. Hamdi, and J.P. Hubaux, “GPS-Free Positioning in Mobile Ad-Hoc Networks,” Proc. Hawaii Int’l Conf. System Sciences (HICSS ’01), Jan. 2001.   
[27] I. Stojmenovic and L. Xu, “Power Aware Localized Routing in Wireless Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 12, no. 11, pp. 1122-1133, Nov. 2001.

![](images/29bc224dd4fc87eb8c75895e39a699e9707a5a9d8278c5c6cbcc863fa96c0f02.jpg)



Jie Lian received the BS degree in computer science from Inner Mongolia University, China, in 1992, the MA degree from the Asian Institute of Technology, Thailand, in 1998, and the PhD degree in electrical and computer engineering from the University of Waterloo, Canada, in 2006. He is now a postdoctoral fellow in the Department of Electrical and Computer Engineering, University of Waterloo. His research interests include ad hoc and sensor networks, peer-to-peer system, energy-efficient techniques for portable wireless devices, and RFID. He is a member of the IEEE and the IEEE Computer Society.

![](images/6bebce562babd135f6b5303c1e5f8aac69dc223a2ce84daf9de66a28f95e85a4.jpg)



Lei Chen received the BS degree in computer science and engineering from Tianjin University, China, in 1994, the MA degree from the Asian Institute of Technology, Thailand, in 1997, and the PhD degree in computer science from the University of Waterloo, Canada, in 2005. He is now an assistant professor in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include multimedia database, sensor databases, peer-to-peer databases, and probabilistic database. He is a member of the IEEE and the IEEE Computer Society.

![](images/31fedd1a60d85ad1169fd8824c4e29d29408f618d62087ca9727533e41aa76b7.jpg)



Kshirasagar Naik received the BS degree from Sambalpur University, India, the MTech degree from the Indian Institute of Technology, Kharagpur, India, the MMath degree in computer science from the University of Waterloo, and the PhD degree in electrical and computer engineering from Concordia University, Montreal. He worked as a faculty member at the University of Aizu in Japan and Carleton University, Ottawa. Currently, he is an associate professor in the Department of Electrical and Computer Engineering, University of Waterloo. He was a program cochair of the Fifth International Conference on Information Technology, Bhubaneswar, India, in 2002. He is on the program committees of several international conferences in the area of wireless communication and mobile computing. He was a coguest editor of the special issue of the IEEE Journal on Selected Areas in Communication (JSAC) on mobile computing and networking. He was the lead guest editor of the special issue of IEEE JSAC on peerto-peer communications and applications. His research interests include testing of communication protocols, wireless communication, resource allocation in cellular and 3G systems, sensor networks, ad hoc networks, MAC protocols for wireless LAN, Bluetooth networks, mobile computing, and peer-to-peer communication. He is a member of the IEEE and the IEEE Computer Society.

![](images/18d2cde442b41773b7bef9c0c55d6dfb33a8851422bbd6074241fa1a3cb63bba.jpg)



Yunhao Liu received the BS degree from Tsinghua University, China, in 1995, and the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and the PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is now an assistant professor in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include peer-to-peer and grid computing, sensor networks, pervasive computing, network security, and high-speed networking. He is a senior member of the IEEE and the IEEE Computer Society.

![](images/62a207a4f1f434bb490f84258abd9215d0a299a44335b34e0bc72bf0aa5515aa.jpg)



Gordon B. Agnew received the BASc and the PhD degrees in electrical engineering from the University of Waterloo in 1978 and 1982, respectively. He joined the Department of Electrical and Computer Engineering at the University of Waterloo in 1982. His areas of expertise include cryptography, data security, protocols and protocol analysis, electronic commerce systems, high-speed networks, wireless systems, and computer architecture. He is a member of the International Association for Cryptologic Research, a Foundation Fellow of the Institute for Combinatorics and its Applications, and a registered professional engineer in the Province of Ontario. He is also a cofounder of CERTICOM, a world leader in public key cryptosystem technologies. He is a member of the IEEE and the IEEE Computer Society.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.