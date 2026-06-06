# Robust and Efficient Aggregate Query Processing in Wireless Sensor Networks

Kebin Liu & Lei Chen & Yunhao Liu & Minglu Li

Published online: 8 May 2008

\# Springer Science + Business Media, LLC 2008

Abstract Wireless sensor networks have been widely used in many applications, such as soil temperature monitoring for plant growth and abnormal event detection of industrial parameters. Among these applications, aggregate queries, such as SUM, COUNT, AVERAGE, MIN and MAX are often used to collect statistical data. Due to the low quality sensing devices or random environmental disturbances, sensor data are often noisy. Hence, the idea of moving average, which computes the average over consecutive aggregate data, is introduced to offset the effect. The high link loss rate, however, makes the result after averaging still inaccurate. To address this issue, we propose a PCMbased data transmission scheme to “make up” the possibly lost data. Specifically, we focus on obtaining robust aggregate results under high link loss rate. In order to reduce the communication traffic that dominates the energy consumption of the sensor network, we also design an intelligent path selection algorithm for our scheme. Our extensive simulation results have shown that this technique outperforms its counterparts under various sensor network conditions.

Keywords wireless sensor networks . aggregate query . moving average

# 1 Introduction

Wireless sensor networks have been widely used in many environmental monitoring applications [1]. In most of these applications, aggregate queries, such as SUM, COUNT, AVERAGE (AVG), MIN and MAX, are often used as statistics collected from sensors [12, 13, 22]. However, it is known that data collected from sensors are often noisy for various reasons, such as sensing device noise, inaccuracies in measurement techniques and noise from external resources [24].

For Example, part of our ongoing project with D. L. coal mine is to build a safety monitoring system using sensor networks to warn the impending events, such as the mine collapse, flooding, gas leaks and explosions [41]. Sensors are deployed along the coal mine tunnel. In order to know conditions in the mine tunnel, continuous aggregate queries, such as AVG, MIN and MAX, are sent from the sink to monitor temperature, oxygen, and coal gas. According to the monitored values, preventive procedures can be carried out, for example, ventilating low oxygen areas or cleaning coal gas at potential explosion sites. However, we must be very careful before taking any actions based on the sensor data of a single sample, since it is quite noisy and often lead to false alarms. Actually, to implement preventive procedures requires the entire mining procedure to stop. Hence, false preventive actions cause tens of thousands of dollars loss.

In order to handle data uncertainty and noise issues, a popular statistical method, moving averaging, has been

K. Liu : M. Li (\*)

Shanghai Jiao Tong University,

Shanghai, China

e-mail: li-ml@cs.sjtu.edu.cn

K. Liu

e-mail: kebin@cse.ust.hk

L. Chen : Y. Liu

Hong Kong University of Science and Technology,

Clear Water Bay, Kowloon,

Hong Kong, Hong Kong

L. Chen

e-mail: leichen@cs.ust.hk

Y. Liu

e-mail: liu@cs.ust.hk

used [12, 23, 24, 33]. Specifically, once we find some suspicious sensor values (e.g. values above certain alarm thresholds), instead of taking preventive action immediately, we increase the sampling rates and compute the average value of the next M sensing rounds. Only in the case where the averaged value is still over the alarm threshold, we take the action.

In practice, however, after moving averaging, the system still yields incorrect information due to the high link loss rate, which is especially notable in a coal mine environment. Besides in coal mines, the high link loss rate of WSNs has also been reported in many other applications [5, 12].

In order to offer robust and energy-efficient aggregate results, we propose a probabilistic compensation model (PCM) based approach together with an intelligent path selection algorithm to address link losses and energy constraints in the sensor network. PCM improves the accuracy of moving average over the aggregate results from multiple sampling, and we compensate each sensing value with a probabilistic model to offset the effect of noise. To further save energy consumption, a ring structure together with a path selection algorithm that chooses fewer parents, is introduced for this design, as illustrated in Fig. 1. The contributions of this paper are listed as follows:

1. We propose a probabilistic model to simulate and analyze the general process of current works on collecting data from a sensor network in Section 4. Through this model, we find factors that affect the accuracy of continuous aggregation.   
2. Based on the proposed probabilistic model, we develop a novel PCM-based approach in Section 5. The averaged result (estimated data expectation) of our model is an accurate approximation of the real value even under high link loss rate.   
3. We design a novel path selection method, in which children select the most effective parents to send messages, in Section 6. This method reduces the traffic cost while keeping low variance similar to the previous Ring-structure approach that uses all upstream nodes within the range as parents.

4. Through extensive simulation tests, we evaluate the efficiency and effectiveness of the PCM-based approach in answering aggregate queries compared with its counterparts in Section 8.

In addition to the above mentioned sections, Section 2 briefly overviews previous work on aggregate queries over the sensor network and Section 9 concludes this work.

# 2 Related work

There are many works that have been proposed to investigate issues related to the data collection and query optimization in a wireless sensor network.

In the TAG [12, 13], sensors are organized in a spanning tree rooted at the sink. TAG proposes an in-network aggregation [12] technique which allows nodes to combine its own value with data received from all children and then send one single message to its parent. If there are no packet losses, TAG works quite well on both data quality and energy efficiency, but is vulnerable to node and link failures. Even a single link failure would cause data from the entire sub tree to be lost and the deviation of results would be quite large if the failure is close to the sink. In our experiments, we have compared PCM with the fractional parents algorithm which applies the multi-path to reduce the data variance at the cost of high message reception. The result shows that PCM outperforms the fractional parents approach in TAG, in terms of the accuracy of the data expectation.

Many approaches [3, 8, 10, 21] have been proposed to address the issue of energy saving. Range caching [15] is a basic approach for communication compression. Snapshot [9] and CONCH [18] answer queries with a small set of representative nodes so as to reduce the traffic cost. Cougar [22] considers temporal and spatial suppression. Directed diffusion [16] achieves significant energy savings. Magnetic diffusion [25] is another diffusion-based data dissemination mechanism which achieves both high data reliability and energy efficiency. Tributary-Delta [14] approach combines the tree structure and multi-path approaches by running them in different regions of the network. Silvia et al. [27] proposes an adaptive data reduction strategies aiming to reduce the amount of data sent by each node while keeping high accuracy. Lazaridis [11] proposes a method for compressing time series before sending them. Their method also guarantees the accuracy of the compressed representation.

Figure 1 Comparison of different routing structures   
![](images/0498400e74fd429be99a1bf929cf5be8f3cf559e134221da56c4bc94c534d036.jpg)



Statistical models also have been introduced to provide approximate results. BBQ [7] presents statistical modeling techniques for sensor queries. By introducing approximations with probabilistic confidences, queries can be carried out more efficiently. Ken [2] uses replicated dynamic probabilistic models to reduce the communication cost from sensor nodes to the network’s sink.

In general, aggregate queries can be classified into two categories, duplicate-insensitive and duplicate-sensitive. For duplicate-insensitive aggregations such as MIN and MAX, Silberstein [19] presents a novel query processing algorithm called HAT with the goal of minimizing message traffic cost in a network while guaranteeing data accuracy. This method fully leverages the network topology and achieves high performance. Considine [5] proposes the generalized duplicate-insensitive sketches for approximating COUNT to handle a SUM query. The approach combines the multi-path routing and duplicate-insensitive sketch which improves the fault-tolerance at the expense of extra space and computational cost. However, counting sketch brings high variance that may affect the final aggregation results and the traffic cost is thus high. Synopsis diffusion [36] presents a general framework for improving accuracy of various aggregate queries.

In addition to aggregate queries, holistic queries like quantiles aim to keep track of the integrated data distribution in the entire network. Q-digest [17] achieves high performance in quantile queries with strict theoretical guarantees on the approximation quality. Graham [4] addresses the problem of continuously tracking the data distribution over distributed streams with novel tracking schemes and prediction models. Li et al. [37] present the distributed index for multi-dimensional data (DIM) to support the multi-dimensional range queries. Xue et al. [20] propose the contour map matching approach [20] for event detections.

There are some other works related to sensor networks, such as investigating the advantage of sharing common aggregated values among different queries [26], the correlated attributes [29], the data-centric storage [30], join queries [31] and outlier detections [32]. SIA [38] and research in [28] discuss the security topics in sensor networks. Research in [6] presents the detection and classification system in a cutting-edge surveillance sensor network, which classifies and tracks targets including vehicles, persons. Sadler et al. [39] devise computationally efficient lossless compression algorithms on the source node and can achieve additional significant energy improvement. Our work, PCM, aims at carrying out aggregation queries in a robust and power efficient way. We present the probabilistic compensation model together with multipath routing to provide accurate results with low variance, compared to the existing methods. With the path selection, the traffic cost in PCM is much lower than that in either fractional parents or Sketch approach.

# 3 Running example

Before we show more details, a running example in Fig. 1 is given to further illustrate the motivation of our PCM design. As mentioned earlier, TAG [12] employs a tree-like routing scheme which allows a “child” sensor to send messages to only one parent. As shown in Fig. 1a, one leaf node generates a value $C _ { 0 }$ and tries to transmit it to the sink along a single gray colored path. Note that, in-network aggregation is carried out at each intermediate node for saving the communication cost, and the aggregated value $C _ { 1 }$ and $C _ { 2 }$ transmitted by intermediate nodes are thus different from $C _ { 0 } .$ . Such an approach however, is very sensitive to the link loss. A single link loss close to the sink will cause the whole result to be missing. The fraction parent approach applies the ring-structure. As shown in Fig. 1b, the “child” broadcasts equal fractions to all its parents and these fractions are delivered to the root along multiple paths. For example, one leaf node generates a value $C _ { 0 }$ and transmits to all the parents on level 2 with $C _ { 0 } /$ 3 for each (assume the “child” has three parents within the range). However, the ring approach cannot improve the expectation (averaged) of the results obtained from multiple sampling in order to remove the noise effect. Let L be the link loss, and the possibility that the value will propagate to the sink is thus P=1−L. In this case, the expectation (averaged) of result after multi-sampling, M, in both TAG and Ring is $P { \times } C .$

Our PCM is based on the Ring approach with significant improvements. In the PCM approach, we compensate the fractional value with the inverse $P ,$ so the expectation (averaged) of the result is the exact value C in continuous querying. Second, using all upstream nodes within the range as parent like Ring incurs high reception cost, and our analysis further shows that some of the routing paths are unnecessary. In PCM, an intelligent path selection algorithm is proposed to choose the most efficient paths for message delivery. As shown in Fig. 1c, only two parents are selected from each level and a large amount of message transmissions are saved. In the following sections, we provide the probabilistic analysis for this message propagation process, the probabilistic compensation model and the path selection algorithm, in detail.

# 4 Probabilistic model

In this section, we introduce a probabilistic model to evaluate the performance of the existing methods in answering a continuous aggregate query and explore factors that may affect the accuracy of averaged aggregate result. Throughout this paper, we use SUM and AVG as example queries. However, techniques described in this paper can be extended to other queries as well, which are discussed in Section 7. Suppose there is a sensor network containing N nodes, and each sensor node $S _ { \mathrm { i } }$ generates a sensing value at every sampling timestamp, denoted as $C _ { i } ,$ where i = 1, 2, …, N. For SUM and AVG queries, the data packet sent by each sensor node includes the sensor value, count, or both. Due to the link loss, sink may fail to receive some values or only receive a fraction of them (e.g. the fractional parent approach which decomposes the value into fractions and sends them to multiple parents). Considering the SUM aggregates, we treat each sensing value that reaches the sink as a random variable $X _ { \mathrm { i } }$ following certain (probably unknown) probability distribution with its expectation denoted as $P _ { \mathrm { i } } \left( 0 { \leq } P _ { \mathrm { i } } { \leq } 1 \right)$ . In fact, $P _ { \mathrm { i } }$ indicates the “reachable probability” of each value and sensor values that sink receives for SUM and AVG are $C _ { \mathrm { i } } X _ { \mathrm { i } } .$ Thus, SUM and AVG aggregates over one time sample can be expressed as follows:

$$
\mathrm{SUM} = \mathrm{C} _ {1} X _ {1} + C _ {2} X _ {2} + \dots + C _ {N} X _ {N} \tag {1}
$$

$$
\mathrm{AVG} = f \left(X _ {1}, X _ {2}, \dots , X _ {N}\right) = \frac {C _ {1} X _ {1} + C _ {2} X _ {2} + \dots + C _ {N} X _ {N}}{X _ {1} + X _ {2} + \dots + X _ {N}} \tag {2}
$$

Different from SUM, AVG function is not a linear combination of random variables, $X _ { \mathrm { i } } ,$ which makes it difficult to analyze the result with respect to random variables. Thus, we expand the equation using the Tayler series (note that function f has first order partial derivative), $f ( X _ { 1 } , X _ { 2 } , . . . , X _ { N } ) \mathrm { a t } ( X _ { 1 } ^ { 0 } , X _ { 2 } ^ { 0 } , . . . , X _ { N } ^ { 0 } ) . ( \bar { X } _ { 1 } ^ { 0 } , X _ { 2 } ^ { 0 } , . . . , X _ { N } ^ { 0 } )$ is the expectation of $( X _ { 1 } , \ X _ { 2 } , \ . . . , \ X _ { N } )$ . The initial AVG function (Eq. 3) is transformed to:

$$
\begin{array}{l} \mathrm{AVG} = f \left(X _ {1} ^ {0}, X _ {2} ^ {0}, \dots , X _ {N} ^ {0}\right) + \left(\frac {\partial f}{\partial X _ {1}}\right) _ {0} \left(X _ {1} - X _ {1} ^ {0}\right) \\ + \left(\frac {\partial f}{\partial X _ {2}}\right) _ {0} \left(X _ {1} - X _ {2} ^ {0}\right) + \dots + \left(\frac {\partial f}{\partial X _ {N}}\right) _ {0} \left(X _ {N} - X _ {N} ^ {0}\right) + \varepsilon \tag {3} \\ \end{array}
$$

mentioned above, in which $\left( \frac { \partial f } { \partial X _ { 1 } } \right) _ { 0 }$ @X1 0 is the partial derivative of variable Xi. As $( X _ { 1 } ^ { 0 } , X _ { 2 } ^ { 0 } , . . . , X _ { N } ^ { 0 } ) = ( P _ { 1 } , P _ { 2 } , . . . , P _ { N } )$ . In Eq. 4, ε is very small compared with other parts, and AVG can be rewritten as:

$$
\begin{array}{l} \mathrm{AVG} = f (P _ {1}, P _ {2}, \dots , P _ {N}) + \left(\frac {\partial f}{\partial X _ {1}}\right) _ {0} (X _ {1} - P _ {1}) \\ + \left(\frac {\partial f}{\partial X _ {2}}\right) _ {0} (X _ {1} - P _ {2}) + \dots + \left(\frac {\partial f}{\partial X _ {N}}\right) _ {0} (X _ {N} - P _ {N}) \\ = \frac {C _ {1} P _ {1} + C _ {2} P _ {2} + \dots + C _ {N} P _ {N}}{P _ {1} + P _ {2} + \dots . + P _ {N}} \tag {4} \\ + \frac {P _ {2} (C _ {1} - C _ {2}) + P _ {3} (C _ {1} - C _ {3}) + \dots + P _ {N} (C _ {1} - C _ {N})}{\left(P _ {1} + P _ {2} + \dots + P _ {N}\right) ^ {2}} \left(X _ {1} - P _ {1}\right) + \dots \\ + \frac {P _ {1} (C _ {N} - C _ {1}) + P _ {2} (C _ {N} - C _ {2}) + \dots + P _ {N - 1} (C _ {N} - C _ {N - 1})}{\left(P _ {1} + P _ {2} + \dots + P _ {N}\right) ^ {2}} \left(X _ {N} - P _ {N}\right) \\ \end{array}
$$

# 4.1 Expectation

The expectation is significantly important for measuring the accuracy of results from a continuous aggregate query. If the expectation equals the real value, the averaged result after several rounds may approximately approach the actual value, which is exactly the reason why we want to use the moving average method. Let E(SUM) and E(AVG) denote the expectation of the SUM and AVG queries, respectively, which can be computed as follows.

$$
E (\mathrm{SUM}) = C _ {1} P _ {1} + C _ {2} P _ {2} + \dots + C _ {N} P _ {N} \tag {5}
$$

$$
E (\mathrm{AVG}) = \frac {C _ {1} P _ {1} + C _ {2} P _ {2} + \dots + C _ {N} P _ {N}}{P _ {1} + P _ {2} + \dots + P _ {N}} \tag {6}
$$

According to Eq. 5, the expectation of SUM aggregation will be the real value, only if $P _ { \mathrm { i } }$ is equal to 1 for all i. However, AVG has a looser constraint that only requires all $P _ { \mathrm { i } }$ to be of the same value. In previous approaches, $P _ { \mathrm { i } }$ is less than 1 for the existence of the link loss and is usually not equal to each other when $P _ { \mathrm { i } } { ^ { \circ } \mathbf { s } }$ corresponding aggregate value takes different numbers of hops to the sink (even when assuming loss rates of all links are equal). Therefore, $P _ { \mathrm { i } }$ is one factor that may affect the expectation of aggregation results.

# 4.2 Variance

If the sensors’ values are stable for a long time, the averaged aggregation result is a good approximation of actual values. However, since these values usually change continuously in real applications, the accuracy of results in each round is thus very important. In fact, the variance indicates the results’ average deviations from actual values and reflects the reliability of a single aggregation result. Take the AVG aggregation as an example. We assume that each $P _ { \mathrm { i } }$ has the same value, that is, $P _ { 1 } = P _ { 2 } = . . . = P _ { N } = P ,$ and the expectation of results from a continuous AVG aggregate query is equal to the actual value. With this assumption, the expression of AVG in Eq. 4 can be rewritten as:

$$
\begin{array}{l} \mathrm{AVG} = \frac {C _ {1} + C _ {2} + \dots + C _ {N}}{N} \\ + \frac {N C _ {1} - \left(C _ {1} + C _ {2} + \dots + C _ {N}\right)}{N ^ {2} P} X _ {1} + \dots \\ + \frac {N C _ {N} - (C _ {1} + C _ {2} + \dots + C _ {N})}{N ^ {2} P} X _ {N} \\ = \frac {C _ {1} + C _ {2} + \dots + C _ {N}}{N} + A _ {1} X _ {1} + \dots + A _ {N} X _ {N} \tag {7} \\ \end{array}
$$

where $A _ { \mathrm { i } }$ is a positive constant if its corresponding $C _ { \mathrm { i } }$ is above the average of all values and a negative constant otherwise. Let A denote the vector of $A _ { 1 } , A _ { 2 } , . . . , A _ { N } , A =$ $( A _ { 1 } , A _ { 2 } , . . . , A _ { N } )$ , X the vector of $X _ { 1 } , X _ { 2 } , . . . , X _ { N } , X = ( X _ { 1 }$ , $X _ { 2 } , . . . , X _ { N } ) ^ { \mathrm { T } }$ , and $D _ { X X }$ the covariance matrix of X:

$$
D _ {\mathrm{AVG}} = A D _ {\mathrm{XX}} A ^ {T} = \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} A _ {i} A _ {j} D _ {i j} \tag {8}
$$

Similarly, the variance of SUM is computed as follows:

$$
D _ {\mathrm{SUM}} = \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} C _ {i} C _ {j} D _ {i j} \tag {9}
$$

where $D _ { i j }$ is the covariance of random variables $X _ { \mathrm { i } }$ and $X _ { \mathrm { j } }$ and $D _ { i i }$ is the variance of X .

# 4.3 Factors and analysis

According to the analysis above, we can conclude factors that affect the accuracy of query as follows.

1. The expectation $P _ { \mathrm { i } }$ of $X _ { \mathrm { i } }$ determines the expectation of aggregate data.   
2. The variance and covariance of random variables, that is $X _ { \mathrm { i } }$ in $X ,$ also affect the aggregation results.

As shown in Eqs. 5 and 6, the expectation of a query result equals its real value only when each $P _ { \mathrm { i } }$ is raised to one (there is no link loss). Thus, in order to improve $P _ { \mathrm { i } } ,$ multi-path routing is considered, but this brings about another problem of dealing with duplicate values. One simple approach is to assign a unique ID to each node’s messages and messages with duplicate IDs are removed from the root. However, in this approach, in-network aggregation cannot be applied due to its inability to separate the duplicated values in the final aggregation result at the root. As a consequence, the traffic cost brought about by this simple approach is too expensive for practical applications. The sketch approach [5] uses the duplicate insensitive sketches to fulfill the in-network aggregation. However, the sketch also brings the additional traffic cost as well as a high variance for each aggregate value. Instead of improving $P _ { \mathrm { i } }$ directly, we introduce a novel PCM-based algorithm to adjust the final aggregate results without additional overheads and achieve high accuracy.

For SUM, reducing the total variance is equivalent to reducing the variance and covariance of all variables in X since all coefficients in Eq. 9 are positive. Madden [12] reveals that the fractional parents approach, which decomposes the value into fractions and sends them to multiple parents, which can reduce the variance $D _ { i i } .$ . For example, if node S sends C to a single parent with reachable probability P, the expected value in the parent is $C \times P +$ $0 \times ( 1 - P ) = P C$ and the variance is $\left( C - P C \right) ^ { 2 } \times$ $P + ( 0 - P C ) ^ { 2 } { \times } ( 1 - P ) = C ^ { 2 } P ( 1 - P )$ . In the case where S sends C/2 to two parents each, the sum of the expected values from both parents is $2 \times P \times ( C / 2 ) = P C$ is the same as that of the single parent approach, where the sum of variances is $2 \times ( C / 2 ) ^ { 2 } { \times } P \times ( 1 - P ) = C ^ { 2 } P ( 1 - P ) / 2 ,$ , that is, only half of that achieved by the single parent approach.

There is another fact, however, that link-sharing in the network topology may increase the variance and covariance (if there is no link-sharing, $D _ { i j }$ is equal to 0 for $i \neq j )$ . We illustrate this claim with an example. In Fig. 2, two fractions of a value are transmitted through paths A and B as in case (a) (Fig. 2a) and they share one common link in case (b) (Fig. 2b).

$$
\begin{array}{l} \text { Variance   of   Case   (a) } \quad \frac {C ^ {2} P ^ {2} (1 - P ^ {2})}{2} \\ \text { Variance   of   Case(b) } \quad \frac {C ^ {2} P ^ {2} (1 - P ^ {2} + P - P ^ {2})}{2} \\ \end{array}
$$

Thus, it is clear that the variance of sharing one link (variance of case b) is greater than that of sharing no link (variance of case a). In the multi-path approach, parents that receive fractions of an initial value experience an exponential increase in number. As a result, many fractions will join and be aggregated in intermediate nodes. Thus, paths face link-sharing after a few hops, which reduces the benefit of multi-path routing heavily in terms of reliability (high variance). Furthermore, it would be a waste to transmit messages to all upper level nodes within the range.

# 5 Network topology construction and maintenance

In this work, similar to the TAG approach [12, 13], sensor nodes are also organized into a spanning tree. In TAG, the root is a user-specified sensor node which broadcasts the initial topology construction message with its own ID and level (the root level is 0). Any intermediate node that receives the message would cache this ID as its parent and assign its own level to the message’s level plus one. Then, it replaces the ID and level in the message with its own and rebroadcasts this message. The topology construction message floods down the network in this manner and stops while it reaches leaf nodes. In order to operate the intelligent path selection algorithm together with the fractional parents approach, we make the following changes in constructing a spanning tree. First, we use a serial number that will be specified later to replace the sensor ID. The construction message in our approach consists of two parts, a serial number and a level. A child could derive its parent’s serial number from the construction message and extend this serial number by attaching one figure to it. Then, the child uses this extended serial number as its own. This numbering process is described as follows. When an intermediate node receives a construction message from its parent, it sends that parent a feedback message; this way the parent finds out its children’s details. After that the parent assigns each of its children a unique integer from 0 to the number of children it has and notifies the children of this assignment. This assignment acts according to either the order of the children’s feedback or the children’s physical location [9] if this information is available. Children attach this integer to the serial number in a received message as its own serial number and rebroadcast the message with a new serial number and level plus one. Following this process, each node has a serial number that specifies its logical position in the topology.

![](images/a63edb664b5cf79dce564588d52a43067d32abcbd7442ea41af0df4991706dd1.jpg)



Figure 2 Link-sharing example

For example, in Fig. 3, node A assigns its three children with $0 , 1 ,$ and 2, respectively. Then, three child nodes attach the assigned numbers to the received serial numbers (node A’s serial number) to form their own serial numbers, which are <020>, <021>, and <022>, respectively. In fact, the serial number specifies the path it takes from the current node to the root. Considering serial numbers of the two black nodes, <021> and <022>, on level 3, we can infer that they share the same ancestors: <02> and <0>. Once the node becomes aware that its parent has failed, it can select another cached potential parent node as its new parent and reset its own serial number.

Second, in our approach we apply the fractional parents approach together with a path selection algorithm. That is, the child node caches multiple upstream nodes as its potential parents and transmits a fraction of its value to each parent. As illustrated in Fig. 3, a child node with serial number <020> caches node <02> as its direct parent in a spanning tree, while it could also send packets to nodes <00> and <01> that are potential parents of <020>. However, since it is an energy-consuming choice to use all upstream nodes within a range, we propose a path selection algorithm to choose only a few efficient parents. With the serial number, the distance in the topology between two nodes could be measured easily. In light of this distance computation, the path selection algorithm chooses parents that are the most efficient for the current sensor node. The detailed path selection algorithm is presented in Section 6.3. Note that, the constructed network topology is a logical one, and the distance between two nodes is thus a logical distance, which is not fully consistent with their physical distance.

When the number of hops increases, the serial number would also become long. Since we can only use a fixed space to store this number, we cut out the serial number and retain the number of several latest hops for nodes near each other or generally sharing the same ancestor. Therefore, the serial number has the form <number, $L _ { C } { > }$ in which $L _ { C }$ (level of current node) is the last level of this serial number. As an example, node S has the serial number <1,102, 4> meaning it is on level 4 and the later segment of its full serial number is 1,102. That is, S’s ancestor is assigned 1, 1, and 0 on level 1, 2, and 3, respectively, and S on level 4 is assigned 2. The number assigned to its ancestor on level 0 is cut out. This kind of compression does not affect the distance calculation, since neighboring nodes locate in one subtree and share the same ancestor several hops away. Since their serial numbers are extended from a common ancestor, the most significant parts are the same and thus do not contribute to the distance calculation.

Figure 3 Network topology and serial number   
![](images/aff360ae1b373c072edd2d5eb2e62552e23c61a8131c8026d92c582b028a2c75.jpg)



# 6 Query processing on continuous aggregates

In this work, we assume sensor nodes have been organized into a spanning tree and each sensor will generate a sensing value in each round (a short time period). After the creation of a network topology, users can pose a continuous aggregate query, such as AVG, to the network. This query floods down the spanning tree where snooping techniques [12, 13] are used to avoid the mishearing of a query message. In the following phases, each sensor generates a value of the monitoring parameter and sends the value back to the sink through the network, during which fractional parents together with a path selection are applied to reduce the energy cost. Furthermore, in order to handle the link loss, the transmitted fractions are indemnified by a probabilistic compensation model (PCM). The querying processing steps are summarized in Algorithm 1.

Algorithm 1 Continuous aggregate query processing 

<table><tr><td>1. Query dissemination</td><td>//start sending data back to the sink</td></tr><tr><td>2. Path selection;</td><td>//select proper parents to forward message</td></tr><tr><td>3. Fractional parent division;</td><td>//according to the path selection result</td></tr><tr><td>4. Estimate link loss;</td><td></td></tr><tr><td>5. Probabilistic compensation;</td><td></td></tr><tr><td>6. Sending messages back;</td><td></td></tr></table>

As an example, for an AVG query, we need to wrap both COUNT and SUM values into one packet <count, sum>. If one child node has several potential parents within the transmission range, our path selection algorithm only selects some of them as parents, unlike the ring-structure that chooses all of them as parents, and then sends a fraction of the value to each parent. In the case where three upstream nodes are chosen as parents, one third of the initial value, that is, <count/3, sum/3>, forms a fraction. Using a probabilistic link loss rate estimation module (discussed in Section 6.2 later), we can obtain the average link loss rate of the selected paths denoted as $L .$ The compensated fraction <count/3(1−L), sum/3(1−L)> is sent to each parent. These packets are delivered through the network, in which in-network aggregation is carried out. Intermediate nodes combine packets from all children to one single result and retransmit fractional ones to its chosen parents. Finally, all packets are collected by the root and the final result calculated. In the next few subsections, we illustrate the probabilistic compensation model (PCM), link loss estimation and path selection algorithm, in detail.

# 6.1 Probabilistic compensation model

According to the analysis in Section 4.3, we find that expectations of aggregate queries from the existing approaches are not equal to the actual values at all. Take the SUM query as an example, the expectation of SUM query is given by: $E ( \mathrm { S U M } ) = C _ { 1 } P _ { 1 } + C _ { 2 } P _ { 2 } + . . . + C _ { N } P _ { N }$ . In the TAG [12, 13] approach, the value is transmitted to the root through a single path. Assume that links on this $P _ { \mathrm { i } } = \prod ^ { m } \left( 1 - L _ { \mathrm { i } } \right)$ e loss rate of . With the incr $L _ { 1 } , \ L _ { 2 } , \ . . . , L _ { \mathrm { M } } ,$ , thber $L _ { \mathrm { i } }$ we getof hops, $P _ { \mathrm { i } }$ i¼1decreases quickly. As a result, E(SUM) deviates much from the real value. The sketch approach [5] applied a multi-path routing to improve robustness of the data propagation, where each value is transmitted through several paths. Since value losses happen only if all paths fail in sketch, $P _ { \mathrm { i } }$ is closer to 1 than that in TAG. Generalized COUNT sketch is leveraged to combine duplicate ones caused by the multi-path routing. However, even under conditions of no link losses, Sketch itself brings additional faults due to the hashing conflicts of different values. Later, our simulation results also show that about 10% relative error exists in the case of no link losses. Taking into account all the above issues, we propose a novel compensation method for solving the reliability problem.

Instead of sending $C _ { \mathrm { i } }$ in the data packet, we apply a probabilistic compensation model (PCM), which divides the value in each message by $P _ { \mathrm { i } } ,$ , that is, $C _ { \mathrm { i } } / P _ { \mathrm { i } }$ . Thus, the expectation of the SUM result is:

$$
\begin{array}{l} E (\mathrm{SUM}) = \frac {C _ {1}}{P _ {1}} P _ {1} + \frac {C _ {2}}{P _ {2}} P _ {2} + \dots + \frac {C _ {N}}{P _ {N}} P _ {N} \\ = C _ {1} + C _ {2} + \dots + C _ {N} \\ \end{array}
$$

Note that, this type of compensation works in an ideal situation where $P _ { \mathrm { i } }$ is known. Since nodes on different levels can have various numbers of hops to the root and links may have different loss rates in reality, $P _ { \mathrm { i } }$ are different from each other and thus difficult to predict. Therefore, in our PCM approach, the compensation is decomposed into hops and the discussion is restricted to one hop data propagation. Assume the node on the lower level has an initial value $C _ { \mathrm { i } }$ and is divided into n equal parts for n parents. Let the link loss of sensor node $S _ { \mathrm { i } }$ be $L _ { \mathrm { i } } ,$ and the probability that each packet reaches the upper level $P _ { \mathrm { i } } = 1 - L _ { \mathrm { i } }$ . At the upper level, the expectation of the received value is $n \times ( C _ { \mathrm { i } } / n ) \times ( 1 - L _ { \mathrm { i } } )$ . Since link loss cannot be avoided, we simply add a compensation factor to the data propagation. The compensation factor is the inverse of the link success probability of this hop. That is, the higher the link loss rate, the larger the compensation factor. Thus, each packet contains a value

$$
\frac {C _ {\mathrm{i}}}{n (1 - L _ {\mathrm{i}})}
$$

and the expectation on the upper level is

$$
n \frac {C _ {i}}{n (1 - L _ {i})} \times (1 - L _ {i}) = C _ {i}
$$

which is equal to the actual value. While this kind of compensation is conducted hop by hop, the expectation of the final aggregation result is the actual value theoretically (due to the effect of noises, the aggregated result in practical application will still be approximated).

# 6.2 Loss rate estimation

In the previous subsection, in order to apply the compensation, we need to know the link loss rate from a child to its parents. Next, we present a simple yet energy-efficient algorithm to estimate the link loss rate L dynamically.

The link loss rate depends on the difference between the number of received packets at the receiver and that transmitted by the sender. Here, we monitor the number of received packets at the receiver and send this number to the sender. For example, child node A is transmitting packets to parent node B, which has a counter, for each child, that records the number of packets received from it. Assume B has already received N messages from A during a certain period. This information would be piggybacked to A along with the normal messages sent from node B. Once A receives this information by overhearing, it makes a comparison between the received N and the number of transmissions (denoted as M) recoded by its own counter during the same period. Intuitively, we can use $L =$ $\left( 1 - N / M \right)$ as the observed link loss rate in which N/M is the reception rate. Since the receiver sends feedback in an infrequent and piggyback way, it is only necessary to introduce some counters within nodes in this method, which does not require additional traffic cost.

However, since the single observed link loss rate (L) of the latest period is not accurate enough, we use the Kalman filter [34, 35] to provide an optimal estimation of the real link loss rate based on the observed link loss rates. The continuous observed loss rate over time forms a data stream. We apply the well-known Kalman filter on this data stream. At each timestamp k, the result $x _ { k }$ of the Kalman filter is the optimal estimation of the real link loss rate. $x _ { k }$ is called the state in the Kalman filter model and each observed link loss is denoted as a measurement $z _ { k } .$ The Kalman filter was introduced by Kalman to resolve the discrete-data linear filtering problem which is an optimal recursive data processing algorithm. Kalman filter consists of a set of equations. First of all, the system model in this work is represented as follows:

$$
x _ {k} = \phi_ {k, k - 1} x _ {k - 1} + w _ {k - 1} \tag {10}
$$

$$
z _ {k} = H _ {k} x _ {k} + v _ {k} \tag {11}
$$

where

$x _ { k }$ state (link loss rate) of the process

$\Phi _ { k , k - 1 }$ state transition parameter from $x _ { k - 1 } ~ { \mathrm { t o } } ~ x _ { k }$

$w _ { k - 1 }$ process model noise

$z _ { k }$ measurement (observed loss rate)

$H _ { k }$ system parameter relating state and measurement

$\nu _ { k }$ measurement noise

In a common state measurement system, each symbol in Eqs. 10 and 11 may denote a vector or matrix. However, in this work they are all single value parameters since there is only one state (link loss rate) to estimate. Parameter $w _ { k - 1 }$ and $\nu _ { k }$ are assumed to be White Gaussian Noise with covariances Q and R (constant in this work).

The state at timestamp k is predicted based on a previous state: $x _ { k | k - 1 } = \phi _ { k , k - 1 } x _ { k - 1 } .$ , where $x _ { k - 1 }$ is the optimal estimated result at timestamp $k ^ { - 1 }$ and $x _ { k | k - 1 }$ is the predicted state value at timestamp k based on $x _ { k - 1 }$ . Since we assume that the link loss rate in current timestamp is equal to that in last timestamp, $\phi _ { k , k - 1 } = 1$ and the above equations are transformed to:

$$
x _ {k \mid k - 1} = x _ {k - 1} \tag {12}
$$

By combining the predicted value $x _ { k | k - 1 }$ and measured value $z _ { k } ,$ we can get the optimal estimation of current link loss rate: $x _ { k } = x _ { k | k - 1 } + K _ { k } \left( z _ { k } - H _ { k } x _ { k | k - 1 } \right)$ . Since the observed loss rate $z _ { k }$ is a direct measurement of the real link loss rate, $H _ { k } { = } 1$ and the above equation is transformed to:

$$
x _ {k} = x _ {k \mid k - 1} + K _ {k} \left(z _ {k} - x _ {k \mid k - 1}\right) \tag {13}
$$

where the $K _ { k }$ is called the Kalman Gain, which is denoted as: $K _ { k } = P _ { k | k - 1 } H _ { k } ^ { T } \big ( H _ { k } P _ { k | k - 1 } H _ { k } ^ { T } + R \big ) ^ { - 1 }$ . As mentioned above, $H _ { k } { = } 1$ and this equation can thus be transformed to:

$$
K _ {k} = P _ {k \mid k - 1} \left(P _ {k \mid k - 1} + R\right) ^ {- 1} \tag {14}
$$

where $P _ { k | \underline { { k } } - 1 }$ is a priori error covariance: $P _ { k | k - 1 } =$ $\phi _ { k , k - 1 } P _ { k - 1 } \phi _ { k , k - 1 } ^ { T } + Q .$

Since $\phi _ { k , k - 1 } = 1$ , this formulation is transformed to:

$$
P _ {k \mid k - 1} = P _ {k - 1} + Q \tag {15}
$$

where the posteriori error covariance is: $P _ { k } = \left( I - K _ { k } H _ { k } \right)$ $P _ { k | k - 1 }$ . In this example there is only one state in the system, so I=1 and $H _ { k } { = } 1$ . Then, the equation for $P _ { k }$ is:

$$
P _ {k} = (1 - K _ {k}) P _ {k \mid k - 1} \tag {16}
$$

In summary, Eqs. 12 to 16 describe the recursive process of Kalman filter to provide an optimal estimation for the link loss rate. Result $x _ { k }$ is the estimated link loss rate at timestamp k. For simplicity, we continue denoting the link loss rate as L in the following discussion.

Kalman filter is a widely used estimator [34, 40] which has many excellent statistical properties [34]. First, it is an unbiased estimator. Second, compared with all other linear estimation approaches, Kalman filter minimizes the variance of the square of the estimation error. We now show the time and space complexity of the link loss rate estimation with Kalman filter. Since sensor nodes use average loss rate, each node only needs to run one Kalman filter. Then the space costs incurred by Kalman filter in each node are only five variables and two constants and the time complexity is O(1) which is quite acceptable based on current sensor technology [12].

Apart from the link loss rate estimation, another issue of PCM is that, different loss rates between a child and different parent nodes should be addressed, since the child can only broadcast equal compensated fractions to its parents. In this work, we use the average loss rate to compensate fractions. We prove that it provides an accurate result using the average link loss rate in the following theorem.

Theorem 6.2.1 If the average link loss rate is used for the compensation during data transmission from the child to parent nodes with fraction parent, the expectation of the sum of received values in parent nodes is exactly the same as that sent from the child node.

Proof Assume node A transmits value C to n parents $B _ { \mathrm { i } } ( i =$ $1 , 2 , . . . , n )$ . Each $B _ { \mathrm { i } }$ sends the number of reception Ni to A. Let M be the number of transmissions by node A. Thus, the average loss rate is:

$$
L = \frac {\sum_ {i = 1} ^ {n} \left(1 - \frac {N _ {i}}{M}\right)}{n},
$$

based on which the compensated fraction value is given by:

$$
C _ {p} = \frac {C}{n (1 - L)} = \frac {C}{\sum_ {i = 1} ^ {n} \frac {N _ {i}}{M}}.
$$

Therefore, the sum of received values in parent nodes is:

$$
C _ {p} \times \sum_ {i = 1} ^ {n} (1 - L _ {i}) = \frac {C}{\sum_ {i = 1} ^ {n} \frac {N _ {i}}{M}} \times \left(\sum_ {i = 1} ^ {n} \frac {N _ {i}}{M}\right) = C.
$$

# 6.3 Path selection algorithm

In a dense network, one sensor node may have many potential parents within range. The traffic cost is high if we send fractional values to all potential parents. From the analysis in Section 4.3, we know that too many fractions also cause serious link-sharing problem which is inefficient in reducing the variance. Note that, since our compensation mechanism can guarantee an accurate expectation in a continuous query, the accuracy and stability of the result in one round depends on the variance. Therefore, we propose fractional parents together with a path selection algorithm to reduce the variance in which the path selection algorithm is applied to find the most efficient parents and thus reduce the traffic cost, meanwhile guaranteeing the accuracy.

The goal of the path selection is to reduce the number of parents and link-sharing (different paths join and share the same links). Thus, we want to find a few parents that are “far from each other” in the logical topology. For example, the logical positions of nodes A and B are in different branches, while nodes A and C are in the same branch. Nodes A and C are considered nearer to each other than nodes A and B. If we send fractions to sink through the A and C parents, the two corresponding paths would join immediately and share many links. When we use the A and B parents instead, since they are in different branches, paths through them are less likely to meet each other and thus share much fewer links.

Since the logical position of nodes in the spanning tree is represented by its serial number, as indicated in Section $5 ,$ the distance between nodes can be calculated according to their serials which are assigned during the construction of the spanning tree. For example, we want to calculate the distance between two nodes I and $J ,$ whose serial numbers are $< N I _ { L i - d + 1 } N I _ { L i - d + 2 } . . . N I _ { L i } , L i >$ and $< N J _ { L j - d + 1 }$ $N J _ { L j - d + 2 } \ldots N J _ { L j } , L j >$ , respectively. Let d be the length of each serial, $L _ { \mathrm { i } }$ and $L _ { \mathrm { j } }$ levels of the two nodes, and NI and NJ two sequences $< N I _ { L i - d + 1 } N I _ { L i - d + 2 } . . . N I _ { L i } >$ and $< N J _ { L j - d + 1 } N J _ { L j - d + 2 } . . . N J _ { L j } >$ . The definition of the distance between two nodes is as follows.

$$
D I S _ {i j} = \sum_ {k = \min (L i, L j)} ^ {\max (L i - d + 1, L j - d + 1)} \left(N I _ {k} - N J _ {k}\right) \times S ^ {(\max (L i, L j) - k)} \tag {17}
$$

where $D I S _ { i j }$ denotes the distance from node I to J, S the maximum number of children that a parent can have, and $N I _ { k }$ and $N J _ { k }$ the two nodes’ serial numbers.

Equation 17 calculates the distance between two nodes by comparing their serial numbers. The semantics of this function can be described as follows. First, as mentioned in Section 5, the serial number reveals the path from the root to a certain node. In other words, since the serial number of a node is extended from its parent’s serial number, we can obtain its parent’s serial number from its own and other prior ancestors’ serial numbers along the path from the root to the current node. For example, as shown in Fig. 4a, node T has a serial number <0121, 3>, which indicates that its parent on level 2 has a serial number <012, 2> and prior ancestors <01, 1> on level 1 and root <0, 0>. Node P is also on level 3 and has a serial number <0120, 3>. Since serial numbers of T and P are similar to each other and only the figures in the last position are different, it holds that T and P share the same ancestors and are located under the same branch. Considering node Q with a serial number <0101, 3>, its serial number is different from that of node T at the third position. Therefore, they have different parents <010, 2> and <012, 2>, but common ancestors <01, 1> and <0, 0>. As shown in Fig. 4a, Q and T are under different branches. In our logical structure, T and P are nearer to each other than T and Q. Based on these observations, we infer that the more ancestors two nodes share, the closer they are to each other. Their distances are calculated by comparing serial numbers position by position. Note that, numbers in different positions are of different importance. As an example, if serial numbers of two nodes are different in the first few positions, it indicates that they are far away from each other, since their early ancestors are quite different. In other words, if we go to the two nodes from the root, we need to choose different branches at the very beginning. Thus, we assign different weights to figures at different positions, which are handled by S. According to this definition, parents always have a zero distance from their children, since they are on same path. In the case where the distance is negative, the first node is on the left hand side of the second node; otherwise, it is on the right hand side. The larger the absolution of distance, the farther away they are from each other.

An instance of the calculation is given as follows. Assume there are two nodes with the serial numbers <0123, 3> and <1102, 4>, respectively. Their distance is given by:

$$
D I S = (3 - 0) \times 3 ^ {(4 - 3)} + (2 - 1) \times 3 ^ {(4 - 2)} + (1 - 1) \times 3 ^ {(4 - 1)} = 1 8
$$

Path selection can be divided into two steps. First, distances from other potential parents to a child’s direct parent in the spanning tree are calculated. Since these distances reflect the relative position of these potential parents, all the potential parents can be projected onto a line consistent with their positions, from left to right, in the topology. For example, in Fig. 4b, node C represents the direct parent of the child node colored in black and other gray nodes are parent candidates.

As a second step, we choose parents from these candidates. The child’s direct parent (C in Fig. 4b) in the spanning tree is selected as the default parent. Next, the left most node A and right most node G (with the largest absolution of the distance from C) are the next most efficient candidate choices. If more parents are needed, we can divide the range from A to C or C to G into several equal segments and obtain nodes around the segment points. For example, after selecting nodes C, A, and G, we need one more parent, node E at the mid-point between C and G. Obviously, two parents (C and G in Fig. 4b) could provide similarly accurate results to choose more candidates. Once parents are selected, parents would then cache all their children. After that, parents only receive packets from children in its cache list.

With this path selection algorithm, the number of received messages can be significantly reduced. Suppose the sensor network consists of N nodes, each of which has m potential parents within the range. When we choose two parents, the number of received messages can be significantly reduced from mN to 2N, saving totally $( m { - } 2 ) N$ message receptions.

![](images/ecebe430d3a025abfe6c7ba9661dba88c0778f5addbd64de4afed10b7a5d767e.jpg)



Figure 4 a Distance calculation. b Parent selection

# 7 Extension to other queries

As mentioned before, our PCM approach together with an intelligent path selection algorithm focuses on improving the effectiveness and efficiency of answering aggregate queries. However, the proposed technique can be easily extended to other query types. Apart from SUM and AVG discussed in previous sections, we illustrate examples of other important aggregate queries that can be also handled by the PCM approach.

In particular, for MIN and MAX queries, we can simply set the compensation to 1 and use the path selection algorithm to reduce the traffic cost. Holistic queries, such as quantile and histogram, have the unique property that the data distribution from all sensor values is required to be known. For example, construct a histogram of data distribution or find the median value in the network. This leads to high space and communication requirements. In a SUM query, each node transmits a message of a fixed size containing only one integer that represents the sum of all data values of its children and itself. To answer a median query, however, we need to track all distinct sensor values. Therefore, messages transmitted by a node near the sink are large since they contain the detailed data distribution information from their children. If sensor nodes deliver their values to sink individually without aggregation, the message size can be controlled, whereas the number of messages is extremely large. Some previous works use several variables called buckets to store the distribution information and merge ranges of data into one bucket if necessary. Our PCM and path selection algorithm can be plugged into these bucket-based approaches to improve the data accuracy and energy efficiency.

# 8 Experimental results

In this section, we evaluate our PCM and path selection method against three current approaches in answering continuous aggregates with different link loss rate, number of potential parents, and network size in experiments I–III, respectively. In the compensation module of our PCM approach, we apply the Kalman filter-based loss rate estimation. Method 1 is the standard TAG approach using single path and in-network aggregation. Method 2 is the fractional TAG approach which is denoted as Fraction. Method 3 is the sketch method using generalized counting sketch to conduct aggregation query. We simulate the network topology by organizing nodes into a balanced spanning tree in which each parent has four children. Thus, the number of nodes in one level is four times that of its parent level. In experiments I and II, there are six levels in the tree and the total number of nodes is 1,365. In experiment III, the network size varies from four levels with 85 nodes to seven levels with 5,461 nodes. In all these methods, the moving average is incorporated and fixed to a rate of 50 samples per result.

We use two metrics in our experiments to evaluate the accuracy of the query results. The first one is the average of all results which is an estimation of each query’s expectation. The second one, a relative error, considers aggregation results’ average deviations from real values. Assume that the averaged result is X and the real value is X′, the relative error is $\frac { | \widecheck { X } - X ^ { \prime } | } { X ^ { \prime } }$ Compared with the variance, the relative error is a better measure since it has removed the influence of raw values and focuses on the percentage of deviation.

Figure 5 a SUM results. b Relative error of SUM   
![](images/1386c96742e7bb2307641fb232e4a2666790dc5497e72eb2b2be03b6e11ba721.jpg)



a

![](images/6c04a661f4a25a1d8cd6956babd0aae61a2381bb2528f86e624fca06df47a83b.jpg)



b

Figure 6 a AVG results. b Relative error of AVG   
![](images/6fa265f1de025e5ebecd384c954c074743393dbf7ddb32931a3a3e739656abbb.jpg)



a

![](images/92086f86b1093a6d5156ad32cd199b02cbb4d9c770f7151c466c540b5e640c5e.jpg)



b

# 8.1 Experiment I

In the first experiment, there are totally four potential parents within the range around each child sensor and the network contains above 1,000 sensor nodes in all. The link loss rate changes from 30% to 5%. We run the aggregation queries of 10,000 rounds with each link loss rate. Figures 5a and 6a show the average of all results of 4 methods on SUM and AVG query respectively. Because the TAG and fractional TAG are not designed for handling high link loss, their relative errors will rise up to 80% (which can be inferred from Fig. 5a) on high link loss rate, we only compare the relative errors of Sketch and PCM in answering SUM and AVG query, and the results are shown in Figs. 5b and 6b, respectively.

As the SUM results shown in Fig. 5, With respect to the average of all results, PCM is the best of the 4 methods, which reports accurate average value. The Sketch approach obtains the average which is a little less than the real value under a high link loss rate. In terms of the other measure, the relative error, PCM is still better than Sketch on various link loss rates. Note that the relative error of Sketch is caused by both the link loss and the variance of general counting sketch. So there will be relative error in Sketch even when there is no link loss. TAG and Fraction perform much worse than sketch and PCM.

While considering AVG query, PCM performs the best in both measures as shown in Fig. 6a and b. For the average measurement, the other three approaches all deviate from the real value in which Sketch’s results fluctuate around the real value. The relative error of Sketch in AVG is higher than PCM as well. Compared with the SUM results of Fig. 5, TAG, Fraction and PCM all achieve better performance in AVG than they obtain in SUM. This is because AVG is a ratio between SUM and Count, the aggregate SUM and Count decrease simultaneously with link loss which decreases the deviation of aggregate AVG from real value.

Figure 7 a SUM results. b Relative error of SUM   
![](images/18b0c45b0c72daa0f195cbc158ac3cfc3dfff71b5f4aac7729b6009554c5ba9f.jpg)



a

![](images/774c4c39394ee6b05ebb9ff64f8f709f2dd81467aeb345ef594ac4b42df276e7.jpg)



b

Figure 8 a AVG results. b Relative error of AVG   
![](images/9b8917fc4015ff3f23f09b616a8454bcb38fac0173e269bcfbd946aed337621c.jpg)



a

![](images/d9406224896cbcdbfb56dbc5fdffb8d8c02eb3de4b5f4b110cca2908d74281df.jpg)



b

# 8.2 Experiment II

Due to the various node distributions and signal qualities, there will be different number of potential parents around one child. This experiment is designed to evaluate how the number of potential parents affects the aggregation results. Figures 7 and 8 show the performances of the four methods with the number of potential parents varying from four to eight. The link loss rate is fixed at 20% and the network size is 1,365 nodes.

The results in Figs. 7 and 8 indicate that PCM and Sketch achieve much better performances than the other two approaches. Moreover, the result of PCM is better and more stable than that in Sketch.

# 8.3 Experiment III

In this experiment, network size is taken into consideration which is from less than 100 nodes to more than 5,000 nodes. For simplicity, the link loss rate is set to 20% and potential parents are always four. Figures 9 and 10 report the results.

As shown in Figs. 9 and 10, for SUM query PCM and Sketch have much better performances than TAG and Fraction under various network sizes. For the AVG query, the averaged results of the 4 methods are all comparable. However, PCM provides the lowest relative error with various network sizes in both queries.

In addition to test PCM, we also evaluate our path selection algorithm. We assume that there are totally eight potential parents for each child sensor and the path selection algorithm chooses four of them. We varies the link loss rate from 30% to 5% and fix the network size to 1,365 nodes, the results are shown in Fig. 11. In Fig. 11, PCM-Path selection denotes the approach that combines the PCM and path selection.

There is a trade-off between number of paths (traffic) and the accuracy. However, as shown in Fig. 11a,b, with the intelligent path selection algorithm, the sacrifice of accuracy could be very low while saving a large amount of traffic cost. In Fig. 11b, among all five approaches, one sensor node sends one message per round. However, in Fraction, PCM and Sketch, more messages are received and processed by the parents than TAG and PCM plus path selection, since messages are broadcasted and received by all parents within a certain range. In TAG, a child only has one parent, and in PCM plus path selection, a small number of potential parents are selected. However, the number of parents is less than Sketch, PCM and Fraction after path selection. Finally, Sketch transmits many more packets than the other four methods because the sketch approach requires a data structure with a much larger size. The five approaches sorted by their cost in ascending order are: TAG, PCM plus path selection, PCM and Fraction, Sketch.

Figure 9 a SUM results. b Relative error of SUM   
![](images/a2e2762df93ccbb4d61f7f41cca719fec363b8953b1c636ec91b61c6be56b882.jpg)



a

![](images/714c207995906ca103f9e217e892882574475608b46ad7cbbfb845eab0f617ba.jpg)



b

Figure 10 a AVG results. b Relative error of AVG   
![](images/bd976e51cd2a1e04a07dcc516a7a92759bdfca49c53cc45c78e427bcd995a8a7.jpg)



a

![](images/2bd3ce138d560f2b7f996d518b7f14688a035060c9c2d6674f02c638e2edfc73.jpg)



b

To summarize, from all the results in experiment I, II, III we can conclude that:

1. Expectation: The expectation of PCM is much closer to the real value compared with other approaches. Averaged results of other methods all have deviations from the real value which are especially significant for TAG and Fraction on aggregate queries.

2. Relative error: PCM achieves the best performance on varying conditions and queries. Sketch has a bit higher relative error than PCM. TAG and Fraction are not designed for high link loss and perform much worse than PCM and Sketch.   
3. Traffic: TAG and PCM plus path selection use the least traffic while the Sketch approach requires much more traffic cost than other methods.

Thus, PCM together with the intelligent path selection algorithm is more accurate and energy efficient in answering aggregate queries over the sensor networks.

# 9 Conclusions

In this paper, we formally analyze the characteristics of the data aggregation with high link loss rate and propose a probabilistic model to study factors that may affect the final result of queries in the WSNs. Based on this observation, we propose a probabilistic compensation model (PCM) together with an intelligent path selection algorithm to improve the accuracy and stability of continuous aggregation queries. With the path selection algorithm, PCM can achieve high performance of reducing the communication traffic cost. Our extensive simulation results have demonstrated that our technique outperforms its counterparts under various network conditions.

Figure 11 a Error of AVG. b Traffic cost comparison   
![](images/eb767179adb531fd4c77559f8e189ee6b6baba0248d601c1fe3837bf3849f984.jpg)



a

![](images/7ca7114433319830d219e77f2ac35266a31619ff5c3222df5e538555d222166f.jpg)



b

We are currently testing our PCM scheme in the ongoing coal mine monitoring project. As an interesting topic for the future work, we would provide a general and efficient interface to accomplish data aggregation tasks in sensor networks.

Acknowledgement This work is supported in part by the National Basic Research Program of China (973 Program) under grant no. 2006CB303000, the Hong Kong RGC grants HKUST6169/07E and 611907, NSFC Project grants no. 60533110 and no. 90612018.

# References

1. Cerpa A, Elson J, Estrin D, Girod L, Hamilton M, Zhao J (2001) Habitat monitoring: application driver for wireless communications technology. SIGCOMM Comput Commun Rev 31(2 Suppl)   
2. Chu D, Deshpande A, Hellerstein JM, Hong W (2006) Approximate data collection in sensor networks using probabilistic models. In Proceedings of ICDE Conference   
3. Ciancio A, Pattem S, Ortega A, Krishnamachari B (2006) Energyefficient data representation and routing for wireless sensor networks based on a distributed wavelet compression algorithm. In Proceedings of IPSN Conference   
4. Cormode G, Garofalakis M, Muthukrishnan S, Rastogi R (2005) Holistic aggregates in a networked world: distributed tracking of approximate quantiles. In Proceedings of SIGMOD   
5. Considine J, Li F, Kollios G, Byers J (2004) Approximate aggregation techniques for sensor databases. In Proceedings of ICDE Conference   
6. Gu L, Jia D, Vicaire P, Yan T, Luo L, Tirumala A, Cao Q, He T, Stankovic JA, Abdelzaher T, Krogh BH (2005) Lightweight detection and classification for wireless sensor networks in realistic environments. In Proceedings of SenSys   
7. Deshpande A, Guestrin C, Madden S, Hellerstein JM, Hong W (2004) Model-driven data acquisition in sensor networks. In Proceedings of the VLDB Conference   
8. He T, Krishnamurthy S, Stankovic JA, Abdelzaher T, Luo L, Stoleru R, Yan T, Gu L, Hui J, Krogh B (2004) Energy-efficient surveillance system using wireless sensor networks. In Proceedings of MobiSys Conference   
9. Kotidis Y (2005) Snapshot queries: towards data-centric sensor networks. In Proceedings of ICDE Conference   
10. Jain S, Shah RC, Brunette W, Borriello G, Roy S (2006) Exploiting mobility for energy efficient data collection in wireless sensor networks. Mob Netw Appl 11(3):327–339   
11. Lazaridis I, Mehrotra S (2003) Capturing sensor-generated time series with quality guarantees. In Proceedings of the ICDE   
12. Madden S, Franklin MJ, Hellerstein JM, Hong W (2002) TAG: a tiny aggregation service for Ad-hoc sensor networks. SIGOPS Oper Syst Rev 36(SI):131–146   
13. Madden S, Szewczyk R, Franklin MJ, Culler D (2002) Supporting aggregate queries over Ad-Hoc wireless sensor networks. In Proceedings of WMCSA

14. Manjhi A, Nath S, Gibbons PB (2005) Tributaries and deltas: efficient and robust aggregation in sensor network streams. In Proceedings of the SIGMOD Conference   
15. Olston C, Loo BT, Widom J (2001) Adaptive precision setting for cached approximate values. In Proceedings of SIGMOD   
16. Intanagonwiwat C, Govindan R, Estrin D, Heidemann J, Silva F (2003) Directed diffusion for wireless sensor networking. IEEE/ ACM Trans Netw 11(1):2–16   
17. Shrivastava N, Buragohain C, Agrawal D, Suri S (2004) Medians and beyond: new aggregation techniques for sensor networks. In Proceedings of SenSys Conference   
18. Silberstein A, Braynard R, Yang J (2006) Constraint chaining: on energy-efficient continuous monitoring in sensor networks. In Proceedings of SIGMOD Conference   
19. Silberstein A, Munagala K, Yang J (2006) Energy-efficient monitoring of extreme values in sensor networks. In Proceedings of SIGMOD Conference   
20. Xue W, Luo Q, Chen L, Liu Y (2006) Contour map matching for event detection in sensor networks. In Proceedings of SIGMOD   
21. Xing G, Lu C, Zhang Y, Huang Q, Pless R (2005) Minimum power configuration in wireless sensor networks. In Proceedings of MobiHoc Symposium   
22. Yao Y, Gehrke J (2002) The cougar approach to in-network query processing in sensor networks. SIGMOD Rec 31:3   
23. Hellerstein JM, Hong W, Madden S, Stanek K (2003) Beyond average: toward sophisticated sensing with queries. In Proceedings of IPSN   
24. Elnahrawy E, Nath B (2003) Cleaning and querying noisy sensors. In Proceedings of the 2nd ACM international conference on Wireless sensor networks and applications   
25. Huang H, Chang T, Hu S, Huang P (2005) Magnetic diffusion: disseminating mission-critical data for dynamic sensor networks. In Proceedings of MSWiM   
26. Emekci F, Yu H, Agrawal D, El Abbadi A (2003) Energyconscious data aggregation over large-scale sensor networks. Technical report   
27. Santini S, Romer K (2006) An adaptive strategy for quality-based data reduction in wireless sensor networks. In Proceedings of INSS   
28. Deng J, Han R, Mishra S (2003) Security support for in-network processing in wireless sensor networks. In Proceedings of SASN   
29. Deshpande A, Guestrin C, Hong W, Madden S (2005) Exploiting correlated attributes in acquisitional query processing. In Proceedings of ICDE   
30. Shenker S, Ratnasamy S, Karp B, Govindan R, Estrin D (2002) Data-centric storage in sensornets. In Proceedings of the First ACM SIGCOMM Workshop on Hot Topics in Networks   
31. Abadi DJ, Madden S, Lindner W (2005) REED: robust, efficient filtering and event detection in sensor networks. In Proceedings of VLDB   
32. Subramaniam S, Palpanas T, Papadopoulos D, Kalogeraki V, Gunopulos D (2006) Online outlier detection in sensor data using non-parametric models. In Proceedings of VLDB   
33. Jeffery SR, Garofalakis MN, Franklin MJ (2006) Adaptive cleaning for RFID data streams. In Proceedings of VLDB   
34. Jain A, Chang E, Wang Y-F (2004) Adaptive stream resource management using Kalman filters. In Proceedings of SIGMOD   
35. Kalman RE (1960) A new approach to linear filtering and prediction problems. Trans ASME J Basic Eng 82:35–45   
36. Nath S, Gibbons PB, Seshan S, Anderson ZR (2004) Synopsis diffusion for robust aggregation in sensor networks. In Proceedings of SenSys   
37. Li X, Kim YJ, Govindan R, Hong W (2003) Multi-dimensional range queries in sensor networks. In Proceedings of SenSys   
38. Przydatek B, Song D, Perrig A (2003) SIA: secure information aggregation in sensor networks. In Proceedings of SenSys

39. Sadler CM, Martonosi M (2006) Data compression algorithms for energy-constrained devices in delay tolerant networks. In Proceedings of SenSys   
40. Kaafar MA, Mathy L, Barakat C, Salamatian K, Turletti T, Dabbous W (2007) Securing internet coordinate embedding systems. In Proceedings of SIGCOMM   
41. Li M, Liu Y (2007) Underground structure monitoring with wireless sensor networks. In Proceedings of ACM/IEEE IPSN

![](images/df7d4ec9e5e425013dc0297095c5b5b0fc826205e158ff058f17d3b3121e4153.jpg)



Kebin Liu received his B.S. degree in the Department of Computer Science from Tongji University, and an M.S. degree in Shanghai Jiaotong University, China. He is a Ph.D. candidate in the Department of Computer Science and Engineering at Shanghai Jiaotong University. He is currently a visiting scholar in the Department of Computer Science and Engineering in Hong Kong University of Science and Technology, under supervision of Dr. Yunhao Liu. His research interests include sensor networks, sensor databases, and distributed systems.

![](images/dc2ef65518d64f1c161c358b49f7de39b5f5d3ee087a87362fe50bcf6650b1e2.jpg)



Yunhao Liu received his B.S. degree in Automation Department from Tsinghua University, China, in 1995, and an M.A. degree in Beijing Foreign Studies University, China, in 1997, and an M.S. and a Ph.D. degree in Computer Science and Engineering at Michigan State University in 2003 and 2004, respectively. Yunhao is now with the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology. He is also an Adjunct Professor of Xi’an Jiaotong University, Jilin University, and the Ocean University of China. His research interests include peer-to-peer computing, wireless sensor network, and pervasive computing. He is a senior member of the IEEE, and a member of the ACM. He and his student Li Mo received the Grand Award of Hong Kong ICT Best Innovation and Research Award 2007.

![](images/eb1cebed4c11e2ec62c584d27d216bb7c87a63ad92ca3bb18bcfa0ad944e77b7.jpg)



Lei Chen received his B.S. degree in Computer Science and Engineering from Tianjin University, China, in 1994, the M.A. degree from Asian Institute of Technology, Thailand, in 1997, and the Ph.D. degree in Computer Science from University of Waterloo, Canada, in 2005. He is now an Assistant Professor in the Department of Computer Science and Engineering at Hong Kong University of Science and Technology. His research interests include multimedia database, sensor databases, peer-to-peer databases and probabilistic databases. He is a member of the IEEE, and a member of the ACM.

![](images/9c35b544dc8358a5021c381cd9b1d7fb0ee1eab678efe943a4858c86e409d30d.jpg)



Minglu Li received his B.S. degree in Computer Engineering from the School of Electronic Technology at University of Information Engineering, China, in 1985, and the Ph.D. degree in computer software from Shanghai Jiao Tong University (SJTU), China, in 1996. He is now a full Professor in the Department of Computer Science and Engineering at SJTU. His research interests include grid computing, services computing, and sensor networks.