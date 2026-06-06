# Aggregation Capacity of Wireless Sensor Networks: Extended Network Case

Cheng Wang∗†, Changjun Jiang∗†, Yunhao Liu‡§, Xiang-Yang Li¶§, Shaojie Tang¶, Huadong Ma∥

∗ Department of Computer Science, Tongji University, Shanghai, China

† Key Laboratory of Embedded System and Service Computing, Ministry of Education, Shanghai, China

‡ Department of Computer Science and Engineering, Hong Kong University of Science and Technology

§ TNLIST, School of Software, Tsinghua University

¶ Department of Computer Science, Illinois Institute of Technology, Chicago, IL, 60616

∥ Department of Computer Science, Beijing University of Posts and Telecommunications, Beijing, China

Abstract—A critical function of wireless sensor networks (WSNs) is data gathering. While, one is often only interested in collecting a relevant function of the sensor measurements at a sink node, rather than downloading all the data from all the sensors. This paper studies the capacity of computing and transporting the specific functions of sensor measurements to the sink node, called aggregation capacity, for WSNs. It focuses on random WSNs that can be classified into two types: random extended WSN and random dense WSN.

All existing results about aggregation capacity are studied for dense WSNs, including random cases and arbitrary cases, under the protocol model (ProM) or physical model (PhyM). In this paper, we propose the first aggregation capacity scaling laws for random extended WSNs. We point out that unlike random dense WSNs, for random extended WSNs, the assumption made in ProM and PhyM that each successful transmission can sustain a constant rate is over-optimistic and unpractical due to transmit power limitation. We derive the first result on aggregation capacity for random extended WSNs under the generalized physical model. Particularly, we prove that, for the type-sensitive perfectly compressible functions and type-threshold perfectly compressible functions, the aggregation capacities for random extended WSNs with ?? nodes are of order $\Theta \left( ( \log n ) ^ { - \frac { \beta } { 2 } - 1 } \right)$ and Θ $\left( { \frac { ( \log n ) ^ { - \beta / 2 } } { \log \log n } } \right)$ ( (log ??)−??/2 ) ， respectively, where $\beta > 2$ denotes the power attenuation exponent in the generalized physical model.

# I. INTRODUCTION

Wireless sensor networks (WSNs) are composed of nodes with the capabilities of sensing, communication and computation. The important application of wireless sensor networks (WSNs) is data gathering, i.e., sensor nodes transmit data, possibly in a multi-hop fashion, to a sink node. Actually, one is often only interested in collecting a relevant function of the sensor measurements at a sink node, rather than downloading all the data from all the sensors. Hence, it is necessary to define the capacity of computing and transporting specific functions of sensor measurements to the sink node. Since in-network aggregation plays a key role in improving such capacity for WSNs, we can reasonably call such capacity aggregation capacity for WSNs.

In this paper, we focus on scaling laws of the aggregation capacity for WSNs. Gupta and Kumar [8] initiated the study of capacity scaling laws for large-scale ad hoc wireless networks. The main advantage of studying scaling laws is to highlight qualitative and architectural properties of the system without getting bogged down by too many details [8], [15]. Generally, the capacity scaling laws of network are directly determined by the adopted network models, including deployment models, scaling models and communication models, besides the pattern of traffic sessions. According to the controllability of network, Gupta and Kumar [8] defined two types of deployment models: arbitrary networks and random networks. In terms of scaling methods, there are two types of scaling network models, i.e., dense networks and extended networks. Moreover, the protocol model (ProM), physical model (PhyM) and generalized physical model (GphyM, also called Gaussian Channel model, [11]) are three typical communication models. Following these models, most works focus on the capacities for different traffic sessions, such as unicast, broadcast, multicast, anycast, and many-to-one session, etc. Data aggregation of WSNs studied in this paper can be regarded as a special case of many-toone sessions. The involvement of in-network aggregation [7] makes it more complex than the general data collecting in many-to-one session. Naturally, aggregation capacity scaling laws have characteristics different from the capacity of any other session, which is worth studying.

There exists some literature that deals with scaling laws of the aggregation capacity for different functions, e.g., [2], [7], [13], [14], [21]. To the best of our knowledge, almost all related work, for both random networks and arbitrary networks, only have considered the dense network model, and the results are all derived under binary-rate communication model [20], including ProM and PhyM [8]. Hence, in this work, we study aggregation capacity scaling laws for the random extended WSN, contrary to existing theoretical results that apply only to dense WSNs. Since the basic assumption in ProM and PhyM, i.e., any successful transmission can sustain a constant rate, is indeed over-optimistic and unpractical in extended networks, we use generalized physical model to capture better the nature of wireless channels.

We design an original aggregation scheme comprised of the tree-based routing and TDMA transmission scheduling. This scheme hierarchically consists of local aggregation phase and backbone aggregation phase. Based on this original aggregation scheme, we adopt a technique, called block coding strategy, to improve the aggregation capacity.

Main Contributions: We now summarize major contributions of this paper as follows:

1. For general divisible functions, we design an aggregation scheme, denoted by $\mathcal { A } _ { N , n }$ , for the random extended WSN (RE-WSN), and derive the general result on the achievable aggregation throughput, depending on the characteristics of specific aggregation functions. (Theorem 1)   
2. For a special subclass of symmetric functions, called perfectly compressible aggregation functions (PC-AFs), we show that under the scheme $\mathcal { A } _ { N , n } ,$ the aggregation throughput for RE-WSN can be achieved of order $\Omega ( ( \log n ) ^ { - \frac { \bar { \beta } } { 2 } - 1 } )$ . (Theorem 2)   
3. For a special subclass of PC-AFs, called type-threshold PC-AFs, such as max (or min), range, and various kinds of indicator functions, we devise a new aggregation scheme, denoted by [7] into scheme $\mathcal { A } _ { N , n } .$ $\mathcal { A } _ { N , n } ^ { b c } ,$ ,?? We show that under by integrating the block coding $\mathcal { A } _ { N , n } ^ { b c }$ the aggregation capacity for RE-WSN can be achieved of order $\left( \frac { \left( \log n \right) ^ { - \beta / 2 } } { \log \log n } \right)$ (log ??)−??/2 . (Theorem 3)   
4. For two subclasses of PC-AFs, i.e., type-sensitive PC-AFs (e.g., average function) and type-threshold PC-AFs, we derive the upper bounds on aggregation capacities, which proves that our schemes $\mathcal { A } _ { N , n }$ and $\mathcal { A } _ { N , n } ^ { b c }$ are optimal for type-sensitive PC-AFs and type-threshold PC-AFs, respectively. Combining the lower bounds (Theorem 2 and Theorem 3) with the upper bounds (Theorem 4 and Theorem 5), we obtain the tight bounds on aggregation capacities for type-sensitive PC-AFs and type-threshold PC-AFs are of order $\Theta ( ( \log n ) ^ { - \frac { \beta } { 2 } - 1 } )$ and $\Theta \big ( \frac { ( \log n ) ^ { - \beta / 2 } } { \log \log n } \big )$ (log ??)−??/2 ), respectively. (Theorem 6)

The rest of the paper is organized as follows. In Section II, we introduce the system model. In Section III, we propose the specific aggregation schemes for RE-WSNs to derive the achievable aggregation capacity. In Section IV, we compute the upper bounds on the aggregation capacities for typesensitive perfectly compressible functions and type-threshold perfectly compressible functions, then obtain the tight capacity bounds for two types of functions. In Section V, we review the related work. In Section VI, we draw some conclusions and discuss the future work.

# II. SYSTEM MODEL

# A. Aggregation Capacity

In this paper, we study the aggregation capacity for wireless sensor networks (WSNs). We consider a random WSN, denoted by $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n ) ^ { 1 }$ , where ?? sensors are placed uniformly at random in a square $\mathcal { A } ( { \mathfrak { a } } ^ { 2 } ) = [ 0 , { \mathfrak { a } } ] \times [ 0 , { \mathfrak { a } } ]$ , and a sensor, denoted by $s _ { 0 } ,$ , is chosen as the sink node. Like in most models considered in related work, every sensor node $s _ { i } , \ 0 \leq i \leq$ $n { - } 1$ , periodically generates measurements of the environment that belong to a fixed finite set ℳ with $| { \mathcal { M } } | = { \mathfrak { m } }$ , and the function of interest is then required to be computed repeatedly.

1The results in this paper also apply to the random network where the sensors are placed in the region $\mathcal { A } ( \mathfrak { a } ^ { 2 } ) \overset { \vartriangle } { = } \left[ 0 , \mathfrak { a } \right] \times \left[ 0 , \right.$ ??] according to a Poisson point process of density $\begin{array} { r } { \lambda = \frac { n } { { \mathfrak { a } } ^ { 2 } } } \end{array}$ .

Intuitively, the capacity for WSNs depends on the aggregation functions of interest to the sink node, [7], [14].

1) Formal Notations: Define the aggregation function of interest to the sink node as ${ \bf g } _ { n } : \mathcal { M } ^ { n }  \mathcal { G } _ { n } ;$ furthermore, for any $k , \ 1 \ \leq \ k \ \leq \ n ,$ define the function of the sensor measurements as $\mathbf { g } _ { k } : \mathcal { M } ^ { k }  \mathcal { G } _ { k } .$ , where $\mathcal { G } _ { k }$ is the range of $\mathbf { g } _ { k }$ . Suppose that each sensor has an associated block of ?? readings, known a priori [7]. We define ?? rounds of measurements from all ?? sensors as a processed unit. From a practical perspective, only the same round of measurements, which are usually attached to the same time stamps, are requested and permitted to be aggregated. We first introduce some notations.

∙ A processed unit consisting of ?? rounds of measurements from all ?? sensors is denoted by ${ \mathrm { ~ a ~ } } n \times N$ matrix $M ^ { n \times N } \in$ $\mathcal { M } ^ { n \times N }$ , where $M ^ { n \times N } ( i , j )$ is the ??th measurement of sensor node $s _ { i } , M ^ { n \times N } ( i , \cdot )$ is the ??th row of $M ^ { n \times N } , i . e .$ , the block of ?? measurements of sensor node $s _ { i } ,$ and $M ^ { n \times N } ( \cdot , j )$ is the ??th column of $\mathcal { M } ^ { n \times N }$ , i.e., the set of the ??th measurements of all ?? sensor nodes.   
∙ For a ??-vector $M ^ { k } = [ M _ { 1 } , M _ { 2 } , . . . M _ { k } ] ^ { T } \in \mathcal { M } ^ { k }$ , where $M _ { i } \in { \mathcal { M } } .$ , define $\mathbf { g } _ { k } ( M ^ { k } ) : = \mathbf { g } _ { k } ( M _ { 1 } , M _ { 2 } , . . . , M _ { k } )$ .   
∙ Given a matrix $M ^ { k \times N } , 1 \le k \le n ,$ , define

$$
\mathbf {g} _ {k} ^ {\mathrm{N}} (M ^ {k \times N}) := \left(\mathbf {g} _ {k} (M ^ {k \times N} (\cdot , 1)), \dots , \mathbf {g} _ {k} (M ^ {k \times N} (\cdot , N))\right)
$$

∙ An aggregation scheme dealing with the aggregation of ?? rounds of measurements, denoted by $\mathcal { A } _ { N , n } ,$ determines a sequence of message passings between sensors and computations at sensors. Under the scheme $\mathcal { A } _ { N , n }$ , input any $\mathbf { \bar { \boldsymbol { M } } } ^ { n \times N } \in \mathcal { M } ^ { n \times N }$ , output a result $\mathbf { g } _ { n } ^ { \mathrm { N } } ( M ^ { n \times N } )$ at the sink node ??0.

2) Capacity Definition: First, we give the definition of achievable aggregation throughput for WSNs. All the logs in this paper are to the base 2.

Definition 1: A throughput of $\lambda ( n )$ bits/s is achievable for a given aggregation function ${ \bf g } _ { n }$ if there is an aggregation scheme, denoted by $\mathcal { A } _ { N , n } ,$ by which any $M ^ { n \times N } \in \bar { \mathcal { M } } ^ { n \times N }$ can be aggregated into $\mathbf { g } _ { n } ^ { \mathrm { { N } } } ( { \dot { M } } ^ { n \times N } )$ N (????×?? ) at the sink node within $T ( \mathcal { A } _ { N , n } )$ seconds, where $\begin{array} { r } { \dot { \lambda } ( n ) \le \frac { N \cdot \log \mathfrak { m } } { T ( \mathcal { A } _ { N , n } ) } , \mathfrak { m } = | \mathcal { M } | } \end{array}$ ??⋅log ???? (A??,??) , ?? = ∣ℳ∣, and ?? log ?? is the total number of bits representing ?? measurements from each sensor.

Based on Definition 1, we define the aggregation capacity for random WSNs.

Definition 2: For a given aggregation function $\mathbf { g } _ { n } .$ , we say that the aggregation capacity of a class of random WSNs is of order $\Theta ( f ( n ) )$ bits/s for ${ \bf g } _ { n }$ , if there are constants $c > 0$ and $c < d < + \infty$ such that

$$
\begin{array}{l} \lim _ {n \rightarrow + \infty} \operatorname * {P r} (\lambda (n) = c \cdot f (n) \text {   is   achievable   for   } \mathbf {g} _ {n}) = 1, \\ \liminf _ {n \to + \infty} \operatorname * {P r} (\lambda (n) = d \cdot f (n) \text {   is   achievable   for   } \mathbf {g} _ {n}) <   1. \\ \end{array}
$$

3) Aggregation Functions of Interest: We focus our attention to the divisible functions [7] which can be computed in a divide-and-conquer fashion. Divisible functions are usually deemed as the general functions in the study of data aggregation in WSNs. Furthermore, we limit the scope of this work to a special class of divisible functions called divisible symmetric functions, or symmetric functions for simplicity, which are invariant with respect to permutations of their arguments. That is, for $1 ~ \leq ~ k ~ \leq ~ n$ , and for all permutation ??, it holds that ${ \bf g } _ { k } ( M _ { 1 } , M _ { 2 } , . . . , M _ { k } ) \ = \ { \bf g } _ { k } ( \sigma ( M _ { 1 } , M _ { 2 } , . . . , M _ { k } ) )$ . From an application standpoint, many natural functions of interest, including most statistical functions, belong to this class. Symmetric functions embody the data centric paradigm [7], [16], where it is the data generated by a sensor that is of primary importance, rather than its identity [7]. Specially, we focus on an important class of symmetric functions called perfectly compressible aggregation functions (PC-AFs). A function is perfectly compressible if all information concerning the same measurement round contained in two or more messages can be perfectly aggregated in a single new packet of equal size (in order sense), [14]. The following lemma is straightforward.

Lemma 1: For any perfectly compressible aggregation function $( \mathrm { P C - A F } ) ~ \mathbf { g } _ { k } , 1 \leq k \leq n$ , it holds that $| \mathcal { G } _ { k } | = \Theta ( \mathfrak { m } )$ , where $\mathcal { G } _ { k }$ is the range of the function g??.

We mainly consider two subclasses of PC-AFs, i.e., typesensitive PC-AFs and type-threshold PC-AFs. A PC-AF is type-sensitive (or type-threshold) if it is a type-sensitive function (or type-threshold function). Due to limited space, we omit the formal definitions of two types of functions. Please refer to [7] (Section IV).

Intuitively, the value of a type-sensitive function cannot be determined if a large enough fraction of the arguments are unknown, whereas the value of a type-threshold function can be determined by a fixed number of known arguments. A representative case of type-sensitive PC-AFs is the average function; while, the typical type-threshold PC-AFs include max (or min), range, and various kinds of indicator functions.

# B. Communication Model

A communication model can be defined as a interferencesafe feasible family in which each element is a set consisting of the links that can transmit simultaneously without negative effects, or in order sense, on each other in terms of link rate. Generally, there are two types of communication models in the research of capacity bounds: continuous-rate communication model and binary-rate communication model.

1) Continuous-rate Communication Model (CCM): Under the continuous-rate communication model, the reliably transmission rate is determined based on a continuous function of the receiver’s SINR (signal to Interference plus noise ratio). The generalized physical model (GphyM) is a specific type of the continuous-rate channel model, [1], [11]. It is practically assumed that all nodes are individually power-constrained under GphyM, that is, for any node $v _ { i } .$ , it transmits at a constant power $P _ { i } \in [ P _ { m i n } , P _ { m a x } ]$ , where $P _ { m i n }$ and $P _ { m a x }$ are some positive constants. The receiver $v _ { j }$ receives the signal from the transmitter $v _ { i }$ with strength $\bar { P _ { i } } \cdot \ell ( v _ { i } , v _ { j } )$ , where $\ell ( v _ { i } , v _ { j } )$ indicates the path loss between $v _ { i }$ and $v _ { j }$ . Any two nodes can establish a direct communication link, over a channel of bandwidth ??, of rate

$$
R (v _ {i}, v _ {j}) = B \log (1 + \frac {P _ {i} \cdot \ell (v _ {i} , v _ {j})}{N _ {0} + \sum_ {v _ {k} \in A (i)} P _ {k} \cdot \ell (v _ {k} , v _ {j})}) \tag {1}
$$

where $N _ { 0 } ~ > ~ 0$ is the ambient noise power at the receiver, and $A ( i )$ is the set of nodes transmitting concurrently with $v _ { i }$ . The wireless propagation channel typically includes path loss with distance, shadowing and fading effects. As in [5], [11], [20], we assume that the channel gain depends only on the Euclidean distance between a transmitter and receiver, and ignore shadowing and fading.

2) Binary-rate Communication Model (BCM): To simplify the analysis of the system, Gupta and Kummar [8] defined the binary-rate communication model as the abstraction of the wireless communication model, under which if the value of a defined conditional expression is beyond some threshold, the transmitter can send data successfully to the receiver at a specific constant rate; otherwise, it can not send any, i.e., the transmission rate is assumed to be a binary function. The protocol model (ProM) and physical model (PhyM) defined in [8] both belong to the binary-rate channel model. The former’s conditional expression is the fraction of the distances from the intended transmitter and other ones to a specific receiver; the latter’s conditional expression is SINR. Obviously, the validity of BCM is based on the following assumption.

Assumption 1: Any successful transmission can sustain the rate of a fixed constant order.

# C. Network Scaling Model

We clarify the differences between the random extended WSN (RE-WSN) and random dense WSN (RD-WSN).

1) Criteria of Scaling Patterns: In the research of network capacity scaling laws, there are two typical models in terms of scaling patterns of the network: extended scaling model and dense scaling model [3], [5], [15]. The major difference between the engineering implications of these two scaling models is related to the classical notions of interferencelimitedness and coverage-limitedness. The dense networks tend to have dense deployments so that signals are received at the users with sufficient signal-to-noise ratio (SNR) but the throughput is limited by interference among the simultaneous transmissions. That is, all nodes can communicate with each other with sufficient SNR, and the throughput can only be interference-limited. While, the extended networks tend to have sparse deployments so that the throughput is mainly limited by the ability to transmit signals to the users with sufficient SNR. That is, the source and destination pairs are at increasing distance from each other, so both interference limitation and power limitation can come into play.

Recall that a given random network $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ is constructed by placing uniformly at random ?? sensors in a square deployment region $\mathcal { A } ( { \mathfrak { a } } ^ { 2 } ) = [ 0 , { \mathfrak { a } } ] \times [ 0 , { \mathfrak { a } } ]$ . Next, we examine the scaling characteristics of $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ as $n  \infty ,$ , according to the relation between ?? and ??.

Definition 3: Given a random network $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ , it is dense scaling if ${ \mathfrak { a } } \cdot { \sqrt { \frac { \log n } { n } } } = O ( 1 )$ log ???? = ??(1) with high probability, i.e., $i . e . ,$ ${ \mathfrak { a } } = O ( { \sqrt { \frac { n } { \log n } } } ) ;$ ; otherwise, it is extended scaling.

2) RE-WSN vs. RD-WSN: The extended network and dense network are the representative cases of the extended and dense scaling models, respectively. They are specialized into the cases of ${ \mathfrak { a } } ~ = ~ { \sqrt { n } }$ and ${ \mathfrak { a } } ~ = ~ 1$ , respectively, $i . e .$ , they can be denoted by $\mathcal { N } ( n , n )$ and $\mathcal { N } ( 1 , n )$ , respectively. A random dense WSN (RD-WSN) represents the scenario where the monitoring region is fixed, and the scale of network is expanding as the density of sensors is increasing; while, a random extended WSN (RE-WSN) represents the scenario where the density of sensors is fixed, and the scale of network is expanding as the area of monitoring region is increasing.

Denote the sets of all sensors in the RE-WSN and RD-WSN by $S _ { e }$ and ${ \cal { S } } _ { d } ,$ respectively. Furthermore, denote $\begin{array} { r } { S _ { e } = S _ { d } : = } \end{array}$ $\{ s _ { 0 } \} \cup \{ s _ { 1 } , s _ { 2 } , \cdot \cdot \cdot , s _ { n - 1 } \}$ , where $s _ { 0 }$ is the sink node and $s _ { i }$ $( 1 \leq i \leq n - 1 )$ denotes the sensor node.

3) Communication Models in Scaling Models: Now, we analyze the combinations of communication models and scaling models, and make a choice of communication model for this paper. Following the setting in [5], the channel power gain is given by $\ell ( v _ { i } , v _ { j } ) = \operatorname* { m i n } \{ 1 , d _ { i j } ^ { - \beta } \}$ in the extended scaling network; and it is given by $\ell ( v _ { i } , v _ { j } ) = d _ { i j } ^ { - \beta }$ in the dense scaling network. Here, $d _ { i j } = | | \boldsymbol { v } _ { i } \boldsymbol { v } _ { j } | |$ is the Euclidean distance between two nodes $v _ { i }$ and $v _ { j } , ~ \beta ~ > ~ 2$ denotes the power attenuation exponent [5].   
∙ BCM in Dense Scaling Networks: Gupta and Kumar [8] only defined the BCM, including protocol model and physical model, in dense networks under which Assumption 1 is convincing because the large enough SINR (generally of order $\Theta ( 1 ) )$ can be obtained. Thus, most results of the aggregation capacity [4], [6], [7], [13] derived under BCM are reasonable for dense networks.   
∙ GphyM in Dense Scaling Networks: In dense networks, BCM can act as a perfect abstraction of the generalized physical model (GphyM). Indeed, the capacity derived under GphyM can be equally derived by using BCM, and vice versa.   
BCM in Extended Scaling Networks: In extended networks, according to Definition 3, under any routing scheme for a random network $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ , there must be, w.h.p., a link of distance of order $\Omega ( { \mathfrak { a } } \cdot { \sqrt { \frac { \log n } { n } } } ) , ~ i . e . , ~ \omega ( 1 )$ log ?? ), i.e., ??(1). By Equation (1), the SINR of such a link is too small to contribute to a constant rate. In other words, Assumption 1 is over-optimistic for random extended networks.   
∙ GphyM in Extended Scaling Networks: The GphyM can appropriately embody the continuous link rate in extended networks, which is the reason why most existing studies on the capacity for extended networks are implemented under GphyM, [5], [11], [20].

# III. LOWER BOUNDS ON AGGREGATION CAPACITY

To simplify the description, we define a notion called network lattice that is frequently used in the design of aggregation schemes and in the analysis of network characteristics.

Definition 4 (Network Lattice): For a network $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ , divide the deployment region $\mathcal { A } ( \mathfrak { a } ^ { 2 } )$ into a lattice consisting of subsquares (cells) of side length ??, we call the generated lattice network lattice, and denote it by $\mathbb { L } ( { \mathfrak { a } } , { \mathfrak { l } } , n )$ .

From now on, we focus on the RE-WSN $\mathcal { N } ( n , n )$ .

# A. Aggregation Scheme for General Divisible Functions

Our aggregation scheme, denoted by ${ \mathcal { A } } _ { N , n } ,$ is designed based on the network lattice $\mathbb { L } _ { 1 } \ = \ \mathbb { L } ( { \sqrt { n } } , 2 { \sqrt { \log n } } , n )$ . To simplify the description, we ignore the details about the integers, and assume that the number of rows (or columns) $2 { \sqrt { \log n } }$ $\underline { { \tilde { \sqrt { n } } } }$ is always an integer, which has no impact on the results due to the characteristics of scaling laws issue. Taking the cell in top left corner as the origin with a 2-dimensional index $( 0 , 0 )$ , we give each cell in $\mathbb { L } _ { 1 }$ an index in the order from left to right and from top to bottom, i.e., the index of the cell in bottom right corner is (??, ??), where ?? = ??(??) = √??2√log ?? $\begin{array} { r } { \delta = \delta ( n ) = \frac { \sqrt { n } } { 2 \sqrt { \log n } } - 1 } \end{array}$ By using VC Theorem (Theorem 25 in [11]), we have

Lemma 2: For all subsquares of side length ${ \mathfrak { l } } = 2 { \sqrt { \log n } }$ in the deployment region $\mathcal { A } ( n )$ , the number of sensors in those cells is uniform $w . h . p .$ ., within $\frac { \log n } { 2 } < n _ { i , j } < 8 \log n$ .

The proof of Lemma 2 is very similar to Lemma 18 in [12] (based on VC theorem [17]). Due to limited space, we omit the detailed proof. Note that the involved constants in Lemma 2, i.e., 1 and 8, do not change the final scaling laws of aggregation capacity indeed.

1) Aggregation Routing Scheme: The aggregation routing tree is divided into two levels, i.e., the aggregation backbones and local aggregation links.

Aggregation Backbones: In the network lattice $\mathbb { L } _ { 1 }$ , from the cells, except for that one containing $s _ { 0 } .$ , we randomly choose one sensor from each cell, and obtain a set, denoted by $B _ { s }$ consisting of $( \delta + 1 ) ^ { 2 } - 1$ nodes (sensors). Then, define the set ${ \cal B } : = { \cal B } _ { s } \cup \{ s _ { 0 } \}$ as backbone set. We call the nodes in ℬ as aggregation stations, or simply as stations.

We assume that the sink $s _ { 0 }$ is located in the cell $C _ { \delta , \delta }$ . By connecting the adjacent aggregation stations in the same rows, as illustrated in Fig.1(a), we construct the horizontal backbones of the aggregation routing; by connecting the adjacent stations in ??th column, we build the vertical backbone. For the general case in terms of the location of sink $s _ { 0 } ,$ , we introduce the extending method as follows: Assume that $s _ { 0 }$ is located in the cell $C _ { i , j }$ , the difference in the construction of routing backbone is that the vertical backbone is built in ??th column, instead of in ??th column, as illustrated in ${ \mathrm { F i g . l } } ( { \mathrm { b } } )$ . In fact, we can build a multihop path between the station in cell $C _ { \delta , \delta }$ and the sink in $C _ { i , j }$ , as illustrated in Fig.1(c). It can be proven that such path is certainly not the bottleneck throughout routing. In a word, the location of $s _ { 0 }$ does not change scaling laws of the aggregation capacity.

Local Aggregation Links: In each cell of $\mathbb { L } _ { 1 }$ , all sensors, except for the station, communicate with the station in a single hop. Please see the illustration in Fig.2(a).

2) Aggregation Scheduling Scheme: In a global perspective, the aggregation scheduling scheme is divided into two phases: local aggregation scheduling and backbone aggregation scheduling. In both phases, all scheduled senders transmit with a same fixed power $P \in [ P _ { m i n } , P _ { m a x } ]$ . In first phase, each aggregation station collects the measurements from the sensors in its assigned cell in $\mathbb { L } _ { 1 }$ . In second phase, the data in the aggregation stations are collected into the sink node (not simply level by level). Recall that we make a group of ?? rounds of measurements from all ?? sensors as a processed unit, denoted by a matrix $M ^ { n \times N }$ (Please refer to Section II-A1).

![](images/32210fbbdb01397688eba2063d507038596187d393a43895a1b7bb05812b0117.jpg)



(a) $s _ { 0 }$ in $C _ { \delta , \delta }$

![](images/104a7a9b4075b71f32cfe171d500207ff8724869cc724f7486fb9c8e67b654c0.jpg)



(b) sink in $C _ { i , j }$

![](images/23c63e2605d9097d5b64a7116a151ef500371b4fb43702f63399cfc906f82979.jpg)



(c) additional path

Fig. 1. Construction of Aggregation Backbones. (a) The case that we mainly focus on in this paper. (b) The general case in terms of the location of $s _ { 0 } . \mathrm { ( c ) }$ the additional path from our final station to the sink $s _ { 0 } .$ .   
![](images/95d5e03beefd476e71c19383c123cb48c3ba6eb1f2696136113b72c0c0d166c6.jpg)



(a) Local Aggregation

![](images/251a2f8140f4bf56198450cd7f18a6bf8933956c9b363def93dd72342f1f5d13.jpg)



(b) Limiting Interference   
Fig. 2. Local Aggregation. (a) A 4-TDMA scheme is adopted. Each slot is further divided into 8 log ?? subslots that are assigned to all links in the cell. (b) 4-TDMA scheme guarantees that the distance between any receiver and the nearest unintended transmitters is of at least $\mathfrak { l } = \overline { { 2 \sqrt { \log n } } }$ .

Local Aggregation Scheduling: In this phase, firstly, we use a 4-TDMA scheme to schedule the cells in ??1, as illustrated in Fig.2(a). In this phase, only the links completely contained in some cells are scheduled. From Lemma 2, the number of all links in each cell is w.h.p., not more than 8 log ??. Then, we can further divide each slot of the 4-TDMA scheme into 8 log ?? subslots, by which we can ensure that all links can be scheduled once during a scheduling period that consists of 32 log ?? subslots.

Backbone Aggregation Scheduling: In this phase, the measurements are sent to the sink in a pipelined fashion [7], [14], and are aggregated on the way in each aggregation station. The backbone aggregation scheduling consists of two phases: horizontal backbone phase and vertical backbone phase. First, the data are horizontally aggregated into the stations in ??th column; then the data are vertically aggregated into the sink node in the cell $C _ { \delta , \delta }$ .

In the initial state of horizontal scheduling, for all ?? and ??, the aggregation station in cell $C _ { i , j }$ , denoted by $b _ { i , j }$ , holds ?? aggregation functions values of ?? rounds of measurements from all sensors in $C _ { i , j }$ that can be denoted by a matrix $M ^ { n _ { i , j } \times N }$ . Denote those ?? aggregation functions by

$$
\mathbf {g} _ {n _ {i, j}} ^ {\mathrm{N}} (M ^ {n _ {i, j} \times N}) = \left(\mathbf {g} _ {n _ {i, j}} (M ^ {n _ {i, j} \times N} (\cdot , z)), z = 1, 2, \dots , N\right)
$$

By this time, denote all ?? rounds of data held by all $( \delta + 1 ) ^ { 2 }$

stations as a matrix ?? (??+1)2×??ℎ . $M _ { h } ^ { ( \delta + 1 ) ^ { 2 } \times N }$

During the horizontal backbone phase, denote the set of $b _ { i , j }$ and all its descendants by $D _ { i , j } ^ { h } ,$ ??,?? , thus the carnality of $D _ { i , j } ^ { h }$ is $| D _ { i , j } ^ { h } | \ : = \ : \Theta ( ( j + 1 ) \cdot \log n )$ . Then, the aggregation function value of the ??th round of data at station $b _ { i , j }$ is denoted by

$$
\mathfrak {b} _ {i, j} ^ {h} (k) := \mathbf {g} _ {\left| D _ {i, j} ^ {h} \right|} \left(M _ {h} ^ {\left| D _ {i, j} ^ {h} \right| \times N} (\cdot , k)\right) \tag {2}
$$

Here, $\mathfrak { b } _ { i , 0 } ^ { h } ( k ) = \mathbf { g } _ { n _ { i , 0 } } ( M ^ { n _ { i , 0 } \times N } ( \cdot , k ) )$ , for $k = 1 , 2 , \cdots , N .$

In the initial state of the vertical backbone phase, all stations $b _ { i , \delta }$ hold ?? aggregation function values of ?? rounds of data from the stations $b _ { i , j } , 0 \leq j \leq \delta ,$ , i.e., $6 _ { i , \delta } ^ { h } ( k )$ , $1 \leq k \leq N$ . By this time, denote $N$ rounds of data holden by all $\delta + 1$ stations as a matrix $M _ { v } ^ { ( \delta + 1 ) \times N }$ . Denote the set of $b _ { i , \delta }$ and all its descendants by $D _ { i , \delta } ^ { v } { : }$ , then the carnality of $D _ { i , \delta } ^ { v }$ is $| D _ { i , \delta } ^ { v } | =$ $\Theta ( ( i + 1 ) \cdot { \sqrt { n \log n } } )$ . During the vertical backbone phase, the value of the aggregation function of the ??th round of data at station $b _ { i , \delta }$ is denoted by

$$
\mathfrak {b} _ {i, \delta} ^ {v} (k) := \mathbf {g} _ {\left| D _ {i, \delta} ^ {v} \right|} \left(M _ {v} ^ {\left| D _ {i, \delta} ^ {v} \right| \times N} (\cdot , k)\right) \tag {3}
$$

Here, ${ \mathfrak { b } } _ { 0 , \delta } ^ { v } ( k ) = { \mathfrak { b } } _ { 0 , \delta } ^ { h } ( k )$ , for $k = 1 , 2 , \cdots , N .$

We adopt a 9-TDMA scheme to schedule the horizontal backbones, as illustrated in Fig.1(a), and adopt a 3-TDMA scheme to schedule the vertical backbone. We design Algorithm 1 and Algorithm 2 to schedule the horizontal and vertical backbone aggregations, respectively. Implementing two algorithms once, we can compute ?? aggregation function values of ?? rounds of measurements at the sink node. Before presenting these two algorithms, we define two sequences of sets: For $h = 0 , 1 , 2$ and $v = 0 , 1 , 2 ,$ , define

$$
\mathcal {H} _ {h, v} := \left\{b _ {i, j} | i \text {   mod   } 3 = h, \text {   and   } j \text {   mod   } 3 = v \right\};
$$

for $h = 0 , 1 , 2 ,$ , define $\mathcal { V } _ { h , \delta } : = \{ b _ { i , \delta } | i$ mod $3 = h \}$ .

3) Aggregation Capacity Analysis: Aggregation capacity depends on the type of functions of interest. We propose a general method in the analysis of aggregation throughput, although we mainly focus on the perfectly compressible functions (Section II-A3). Due to the hierarchical structure of our scheme, we carry out the analysis phase by phase.

Local Aggregation Phase: In this phase, since it is guaranteed that each link is scheduled at least once out of 32 log ?? time slots, Lemma 3 intuitively holds.

Lemma 3: In the local aggregation phase, if the rate of each scheduled link can be achieved of $R _ { 1 } ( n )$ bits/s, then each link can sustain an average rate of $\begin{array} { r } { \lambda _ { 1 } ( n ) = \frac { R _ { 1 } ( n ) } { 3 2 \log n } } \end{array}$ 32 log ?? ??1(??) bits/s. Thus, it takes at most

$$
T _ {1} (n) = \frac {N \cdot \log \mathfrak {m}}{\lambda_ {1} (n)} = \frac {3 2 N \cdot \log \mathfrak {m} \cdot \log n}{R _ {1} (n)} \tag {4}
$$

seconds to finish the aggregation of ?? rounds of measurements from ?? sensors, i.e., a processed unit, at $( \delta + 1 ) ^ { 2 }$ stations.

During the local aggregation phase, when block coding [7] is not adopted, all data to be transmitted are the original measurements instead of the aggregated data, then the throughput in this phase is independent of the type of aggregation functions. Next, we commence deriving the rate $R _ { 1 } ( n )$ .

Algorithm 1: Horizontal Backbone Aggregation   
Input: $\mathbf{g}_{n_{i,j}}^{\mathrm{N}}(M^{n_{i,j}\times N})$ at all stations, i.e., $M_{h}^{(\delta+1)^{2}\times N}$ .
Output: $\mathfrak{b}_{i,\delta}^{h}(k)$ at all station $b_{i,\delta}$ .
for $k=1,2,\cdots,N,N+1,\cdots,N+\delta(n)-3$ do $k\to k'$ ;
    if k>N then $N\to k$ ;
    else for h=0,1,2 do
    for v=0,1,2 do
    for $r=1,\cdots,k$ do
    All $b_{i,j}\in\mathcal{H}_{h,v}$ are permitted to transmit;
    if it holds that $1\leq j\leq\delta-1$ , and
    (1) $b_{i,j}, j\geq1$ , has already received $\mathfrak{b}_{i,j-1}^{h}(r)$ from $b_{i,j-1}$ , and
    (2) $b_{i,j+1}$ has not received $\mathfrak{b}_{i,j}^{h}(r)$ from $b_{i,j}$ , then $b_{i,j}$ sends $\mathfrak{b}_{i,j}^{h}(r)$ to $b_{i,j+1}$ ;
    else if j=0, and $b_{i,1}$ has not received $\mathfrak{b}_{i,0}^{h}(r)$ , i.e., $\mathbf{g}_{n_{i,0}}(M^{n_{i,0}\times N}(\cdot,r))$ from $b_{i,0}$ , then $b_{i,0}$ sends $\mathfrak{b}_{i,0}^{h}(r)$ to $b_{i,1}$ . $k'\to k$

Algorithm 2: Vertical Backbone Aggregation   
Input: $\mathfrak{b}_{i,\delta}^{h}(k)$ at all station $b_{i,\delta}$ .
Output: $\mathbf{g}_{n}^{\mathrm{N}}(M^{n\times N})$ at the sink node $s_{0}$ .
for $k=1,2,\cdots,N,N+1,\cdots,N+\delta(n)-3$ do $k\to k'$ ;
    if k>N then $N\to k$ ;
    else for $h=0,1,2$ do
    for $r=1,\cdots,k$ do
    All $b_{i,\delta}\in V_{h,\delta}$ are permitted to transmit;
    if it holds that $1\leq i\leq\delta-1$ , and
    (1) $b_{i,\delta}, i\geq1$ , has already received $\mathfrak{b}_{i-1,\delta}^{v}(r)$ from $b_{i-1,\delta}$ , and
    (2) $b_{i+1,\delta}$ has not received $\mathfrak{b}_{i,\delta}^{v}(r)$ from $b_{i,\delta}$ ,
    then $b_{i,\delta}$ sends $\mathfrak{b}_{i,\delta}^{v}(r)$ to $b_{i+1,\delta}$ ;
    else if i=0, and $b_{1,\delta}$ has not received $\mathfrak{b}_{0,\delta}^{v}(r)$ , i.e., $\mathfrak{b}_{0,\delta}^{h}(r)$ , from $b_{0,\delta}$ ,
    then $b_{0,\delta}$ sends $\mathfrak{b}_{0,\delta}^{v}(r)$ to $b_{1,\delta}$ . $k'\to k$

Lemma 4: During the local aggregation phase, the rate of scheduled links can be achieved of order

$$
R _ {1} (n) = \Omega ((\log n) ^ {- \frac {\beta}{2}}) \tag {5}
$$

Proof: Consider a given active cell, say $C _ { i , j }$ , in a time slot under the 4-TDMA scheme. Please see illustration in Fig.2(b). First, we find an upper bound for the interference at the receiver (station). We notice that the transmitters in the eight closest cells are located at Euclidean distance at least $~ { \mathrm { ~  ~ l ~ } } = ~ 2 { \sqrt { \log n } }$ from the receiver (station) in $C _ { i , j }$ . The transmitters in the 16 next closest cells are at Euclidean distance at least 3??, and so on. By extending the sum of the interferences to the whole plane, this is bounded as follows:

$$
I _ {1} (n) \leq \sum_ {k = 1} ^ {\infty} P \cdot \frac {8 k}{((2 k - 1) \cdot \mathfrak {l}) ^ {\beta}} \leq \frac {P}{2 ^ {\beta - 3}} \cdot (\log n) ^ {- \frac {\beta}{2}} \cdot \sum_ {k = 1} ^ {\infty} \frac {k}{(2 k - 1) ^ {\beta}}
$$

From $\begin{array} { r } { \beta > 2 , \sum _ { k = 1 } ^ { \infty } \frac { k } { ( 2 k - 1 ) ^ { \beta } } } \end{array}$ converges to a constant. Then, $I _ { 1 } ( n ) = O ( ( \log n ) ^ { - \frac { \beta } { 2 } } )$ .

Next, we find a lower bound on the strength of signal received from the transmitter. Since all links are limited within the same cells, the link length is at most ${ \sqrt { 2 } } \cdot \mathbb { I } .$ Thus, the signal at the receiver can be bounded by

$$
S _ {1} (n) \geq P \cdot (\sqrt {2} \cdot \mathfrak {l}) ^ {- \beta} = P \cdot 2 ^ {- \frac {3}{2} \beta} \cdot (\log n) ^ {- \frac {\beta}{2}}
$$

Hence, $S _ { 1 } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \beta } { 2 } } )$ .

Finally, combining the fact that $I _ { 1 } ( n ) = O ( ( \log n ) ^ { - { \frac { \beta } { 2 } } } )$ ) and $S _ { 1 } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \beta } { 2 } } )$ ), we obtain a lower bound on the rate of scheduled link as

$$
R _ {1} (n) = B \log \left(1 + \frac {S _ {1} (n)}{N _ {0} + I _ {1} (n)}\right) = \Omega \left(\left(\log n\right) ^ {- \frac {\beta}{2}}\right),
$$

which completes the proof.

Hence, according to Lemma 3 and Lemma 4, we have

Lemma 5: When the technique of block coding is not used, the time cost of the local aggregation for ?? rounds of measurements is of order

$$
T _ {1} (n) = O \left(N \cdot (\log n) ^ {1 + \frac {\beta}{2}}\right) \tag {6}
$$

Backbone Aggregation Phase: First, we consider the horizontal backbone phase.

Lemma 6: In the horizontal backbone phase, if the rate of each scheduled link is achieved of $R _ { 2 } ^ { h } ( n )$ bits/s, then all horizontal backbones can sustain a rate of $\begin{array} { r } { \dot { \lambda _ { 2 } ^ { h } } ( n ) = R _ { 2 } ^ { h } ( n ) } \end{array}$ ⋅ $\frac { N } { 9 ( N + \delta ( n ) - 3 ) }$ .

Proof: According to Algorithm 1, each horizontal backbone can be scheduled in order at least ?? times out of $3 \times 3 \times ( N + \delta ( n ) - 3 )$ time slots. Thus, the lemma holds.

Now, we start to derive the link rate $R _ { 2 } ^ { h } ( n )$ .

Lemma 7: During the horizontal backbone phase, the rate of scheduled links can be achieved of order

$$
R _ {2} ^ {h} (n) = \Omega ((\log n) ^ {- \frac {\beta}{2}}) \tag {7}
$$

Proof: This lemma can be proven in a similar procedure to that of Lemma 4. We omit details due to limited space.

Lemma 8: To finish the horizontal backbone aggregation for ?? rounds of measurements, it takes at most

$$
T _ {2} ^ {h} (n) = 9 \cdot \zeta_ {m a x} ^ {h} \cdot (\log n) ^ {\frac {\beta}{2}} \cdot (N + \delta (n) - 3) \tag {8}
$$

s, whe, with $\zeta _ { m a x } ^ { h } = \operatorname* { m a x } \{ \zeta _ { i , j } ^ { h } | 0 \le i \le \delta - 1 ; 0 \le j \le$ $\delta - 1 \}$ $\zeta _ { i , j } ^ { h } = \log | \mathcal { G } _ { | D _ { i , j } ^ { h } | } | .$ $\mathcal { G } _ { | D _ { i , j } ^ { h } | }$ $\mathbf { g } _ { \vert D _ { i . i } ^ { h } \vert } .$ .

Proof: In this phase, the aggregation function value of the ??th round of data at station $b _ { i , j }$ is ${ \mathfrak { b } } _ { i , j } ^ { h } ( k )$ : = $\mathbf { g } _ { | D _ { i , j } ^ { h } | } ( M _ { h } ^ { | D _ { i , j } ^ { h } | \times N } ( \cdot , k ) )$ . Since the technique of block coding is not adopted here, the load of $b _ { i , j }$ , denoted by $\Gamma _ { i , j } ^ { h }$ , is

$$
\Gamma_ {i, j} ^ {h} = \sum_ {k = 1} ^ {N} \log | \mathcal {G} _ {| D _ {i, j} ^ {h} |} | = N \cdot \zeta_ {i, j} ^ {h}
$$

Hence, in the horizontal backbone phase, the time cost of the aggregation for ?? rounds of measurements is at most

$$
T _ {2} ^ {h} (n) = \frac {N \cdot \zeta_ {m a x} ^ {h}}{\lambda_ {2} ^ {h} (n)} = 9 \zeta_ {m a x} ^ {h} \cdot (\log n) ^ {\frac {\beta}{2}} \cdot (N + \delta (n) - 3),
$$

which completes the proof.

Next, we analyze the vertical backbone phase in a similar method to the horizontal one. For concision, we omit some similar proofs.

Lemma 9: In vertical backbone aggregation phase, the rate of each scheduled link is of order $R _ { 2 } ^ { v } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \beta } { 2 } } )$ , and the vertical backbone can sustain a rate of order

$$
\lambda_ {2} ^ {v} (n) = \Omega \left((\log n) ^ {- \frac {\beta}{2}} \cdot \frac {N}{3 (N + \delta (n) - 3)}\right).
$$

Lemma 10: To finish the vertical backbone aggregation for ?? rounds of measurements, it takes at most

$$
T _ {2} ^ {v} (n) = 3 \cdot \zeta_ {\max} ^ {v} \cdot (\log n) ^ {\frac {\beta}{2}} \cdot (N + \delta (n) - 3) \tag {9}
$$

seconds, where ?????????? $\zeta _ { m a x } ^ { v } = \operatorname* { m a x } \{ \zeta _ { i . \delta } ^ { v } | 0 \leq i \leq \delta - 1 \}$ , with $\zeta _ { i , \delta } ^ { v } =$ log $\begin{array} { r } { \left| G _ { | D _ { i , \delta } ^ { v } | } \right| . } \end{array}$ , and $G _ { | D _ { i . \delta } ^ { v } | }$ is the range of $\mathbf { g } _ { | D _ { i . \delta } ^ { v } | }$ .

The proofs of Lemma 9 and Lemma 10 are similar to that of Lemma 8. Please see details in our technical report [19].

According to Definition 1, we obtain Theorem 1.

Theorem 1: The aggregation throughput under the scheme $\mathcal { A } _ { N , n }$ with $\begin{array} { r } { N = \Omega \big ( \frac { \sqrt { n } } { \sqrt { \log n } } \big ) } \end{array}$ is of order

$$
\lambda (n) = \Omega \left(\frac {(\log n) ^ {- \frac {\beta}{2}}}{\log n + \zeta_ {m a x} ^ {h} + \zeta_ {m a x} ^ {v}}\right) \tag {10}
$$

where $\zeta _ { m a x } ^ { h }$ and $\zeta _ { m a x } ^ { v }$ are defined in Lemma 8 and Lemma 10, respectively.

Proof: First, we consider the total time cost, say $T ( \mathcal { A } _ { N , n } )$ , during which the aggregation function of ?? rounds of measurements from ?? sensors are computed at the sink node. It holds that $T ( \mathcal { A } _ { N , n } ) = T _ { 1 } ( n ) + T _ { 2 } ^ { h ^ { * } } ( n ) + T _ { 2 } ^ { v } ( n )$ , and the aggregation throughput under the scheme $\mathcal { A } _ { N , n }$ is of order

$$
\lambda (n) = \frac {N \log \mathfrak {m}}{T _ {1} (n) + T _ {2} ^ {h} (n) + T _ {2} ^ {v} (n)} \tag {11}
$$

Based on Lemma 8 and Lemma 10, for $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) , i . e . } \end{array}$ √log ?? ., $N = \Omega ( \delta ( n ) )$ , it holds that

$$
T _ {2} ^ {h} (n) + T _ {2} ^ {v} (n) = O \left((\log n) ^ {\frac {\beta}{2}} \cdot N \cdot (\zeta_ {m a x} ^ {h} + \zeta_ {m a x} ^ {v})\right)
$$

Combining with Lemma 5, we can prove this theorem.

According to the analysis above, $T _ { 2 } ^ { h } ( n )$ and $T _ { 2 } ^ { v } ( n )$ depend on the types of aggregation functions indeed. Consequently, we instantiate the general result in Theorem 1 to a special case, i.e., the case of perfectly compressible functions.

# B. Throughput for Perfectly Compressible Functions

From the characteristic of perfectly compressible aggregation functions (PC-AFs, Lemma 1), by Theorem 1, we have,

Theorem 2: For perfectly compressible aggregation functions, the aggregation throughput under the scheme $\mathcal { A } _ { N , n }$ with $\begin{array} { r } { N = \Omega \big ( \frac { \sqrt { n } } { \sqrt { \log n } } \big ) } \end{array}$ is achieved of $\lambda ( n ) = \Omega ( ( \log n ) ^ { - { \frac { \beta } { 2 } } - 1 } )$ .

Proof: By Lemma 1, for PC-AFs,

$$
\zeta_ {m a x} ^ {h} \leq \max \{\log | \mathcal {G} _ {| D _ {i, j} ^ {h} |} | \} = \Theta (\log \mathfrak {m})
$$

Similarly, $\zeta _ { m a x } ^ { v } ~ = ~ { \cal O } ( \log { \mathfrak { m } } )$ . Recall that ${ \mathfrak { m } } ~ = ~ \Theta ( 1 )$ , the theorem can thus be proven by using Theorem 1.

# C. Aggregation Scheme for Type-Threshold PC-AFs

Sensing measurements are periodically generated, so the function of interest is required to be computed repeatedly. Hence, here permit block coding [7] that combines several consecutive function computations. The technique of block coding can significantly improve the throughput for type-threshold functions [7], in the collocated network whose interference graph is a complete graph. For a given round of measurements, denoted by a ??-vector $M ^ { n } \in { \mathcal { M } } ^ { n }$ , the max function, the min function and the range function $\left( \operatorname* { m a x } _ { i } M _ { i } - \operatorname* { m i n } _ { i } M _ { i } \right)$ of $M ^ { n }$ , the ??th largest value of $M ^ { n }$ , the mean of the ?? largest values of $M ^ { n }$ , and the indicator function $I \{ M _ { i } = k$ , for some $i \}$ are all type-threshold functions. We first refer to a result of [7] (Part of Theorem 4 in [7]).

Lemma $I I \ ( \ I 7 { \cal I } ) .$ : Under the protocol model, the aggregation capacity for type-threshold functions in a collocated network of ?? vertexes is of order $\Theta ( 1 / \log n )$ .

Under our scheme $\mathcal { A } _ { N , n } ,$ in each cell of the scheme lattice $\mathbb { L } _ { 1 }$ , the communication graph can be regarded as a collocated network of $\Theta ( \log n )$ vertexes, because any two links in a cell can not be scheduled simultaneously during the local aggregation phase. Then, it is possible to improve the throughput by introducing the block coding into the scheme $\mathcal { A } _ { N , n } .$ . The main question to be solved is how to extend the result of Lemma 12 to that under the generalized physical model. Analyze the proof of Lemma 12: Let $N = \Theta ( n )$ , and under the assumption that each successful transmission can achieve a constant rate, prove that it takes ??(?? log ??) time slots to finish the aggregation for ?? rounds of measurements. Thus, since during the local aggregation phase of $\mathcal { A } _ { N , n }$ , the rate of each successful transmission can be achieved of order $\Omega ( ( \log n ) ^ { - \frac { \beta } { 2 } } )$ instead of a constant order, we have

Lemma 12: Under generalized physical model, by block coding with $N _ { b } = \Theta ( \log n )$ , for type-threshold PC-AFs, the time cost of the local aggregation for $N = \Omega ( \log n )$ rounds of measurements is of order $T _ { 1 } ^ { b c } ( n ) = O ( N \cdot ( \log n ) ^ { \frac { \beta } { 2 } } \cdot \log \log n )$ .

Proof: For the communication graph in each cell, we implement the local aggregation by using block coding with length $N _ { b } = \Theta ( \log n )$ . Similar to Lemma 12, the time cost of aggregating $N _ { b }$ rounds of measurements is of $O ( ( \log n ) ^ { \frac { \beta } { 2 } }$ ⋅ $N _ { b } { \cdot } \log \log n )$ . By partitioning ?? rounds of measurements into blocks of length $N _ { b } .$ , we prove the lemma. □

Lemma 12 holds when $N \ = \ \Omega ( \log n )$ which does not contradict with the condition that $\begin{array} { r } { N = \Omega \big ( \frac { \sqrt { n } } { \sqrt { \log n } } \big ) } \end{array}$ in Theorem 1 and Theorem 2. Then, we can modify the scheme $\mathcal { A } _ { N , n }$ by introducing the block coding in the local aggregation phase. Denote such scheme by $\mathcal { A } _ { N , n } ^ { b c }$ . Finally, we propose,

throughput under the scheme Theorem 3: For type-threshold PC-AFs, the aggregation $\mathcal { A } _ { N , n } ^ { b c }$ with $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) } \end{array}$ can be achieved of order $\lambda ( n ) = \Omega \left( ( \log n ) ^ { - { \frac { \beta } { 2 } } } \cdot { \frac { 1 } { \log \log n } } \right)$ log log ??

Proof: By using block coding, $T ( \mathcal { A } _ { N , n } ^ { b c } ) ~ = ~ \dot { T } _ { 1 } ^ { b c } ( n ) +$ $T _ { 2 } ^ { h } ( n ) + T _ { 2 } ^ { v } ( n ) = O ( N \cdot ( \log n ) ^ { \frac { \beta } { 2 } }$ ⋅ log log ??). According to Definition 1, we can complete the proof.

# IV. UPPER BOUNDS ON AGGREGATION CAPACITY

In this section, we compute the upper bounds on aggregation capacities for type-sensitive perfectly compressible aggregation functions (type-sensitive PC-AFs) and type-threshold perfectly compressible aggregation functions (type-threshold PC-AFs) over RE-WSN.

# A. Upper Bounds for Type-Sensitive PC-AFs

Theorem 4: The aggregation capacity for type-sensitive PC-AFs over RE-WSN is of order $O ( ( \log n ) ^ { - { \frac { \beta } { 2 } } - 1 } )$ .

Proof: In any aggregation tree, there exists, w.h.p., a link of length $\Omega ( { \sqrt { \log n } } )$ , say ????. The capacity of such link is upper bounded by ?? log(1 + (??1 √log ??) $\begin{array} { r } { B \log ( 1 + \frac { ( \kappa _ { 1 } \sqrt { \log n } ) ^ { - \beta } } { N _ { 0 } } ) = O ( ( \log n ) ^ { - \frac { \beta } { 2 } } ) } \end{array}$ ??0 , where $\kappa _ { 1 } > 0$ is a constant. According to the characteristics of type-sensitive PC-AFs, it takes at least $\kappa _ { 2 } \cdot n N \cdot ( \log n ) ^ { \frac { \beta } { 2 } }$ transmissions to finish the aggregation of ?? rounds of measurements from every sensor, where $\kappa _ { 2 } > 0$ is a constant that has no impact on the final results in order sense. By a similar procedure to Lemma 2 (based on VC theorem [17]), we get that each cell in the network lattice $\mathbb { L } ( \sqrt { n } , \frac { 2 } { \kappa _ { 2 } } \sqrt { \log n } , n )$ must operate at least $\kappa _ { 3 }$ log ?? transmissions, where $\frac { 1 } { 2 } < \kappa _ { 3 } < 8$ . Since the arena-bounds [9] for the generalized physical model is of order $O ( \log n )$ , [10], the total aggregation rate of those $\kappa _ { 3 }$ log ?? transmissions can be upper bounded of order $O ( \mu ( \log n ) ^ { - \frac { \beta } { 2 } } )$ ) when the data from the senders of these ??3 log ?? transmissions are aggregated into $\mu$ receivers, where $\mu = O ( \log n )$ . For any aggregation tree, consider the cells in $\mathbb { L } ( \sqrt { n } , \frac { 2 } { \kappa _ { 2 } } \sqrt { \log n } , n )$ , from the farthest (in hop-distance) cell to that contains the sink node, there must be a scenario where $\mu = \Theta ( 1 )$ , because all data will converge to the sink node. In this case, ??3 log ?? transmissions share the total link rate of $O ( ( \log n ) ^ { - { \frac { \beta } { 2 } } } )$ , and it takes $\Omega ( n N ( \log n ) ^ { \frac { \beta } { 2 } + 1 } )$ slots to finish the aggregation. Thus, the aggregation capacity is bounded by

$$
\frac {n N}{\Omega (n N (\log n) ^ {\frac {\beta}{2} + 1})} = O ((\log n) ^ {- \frac {\beta}{2} - 1}).
$$

# B. Upper Bounds for Type-Threshold PC-AFs

Theorem 5: The aggregation capacity for type-threshold PC-AFs over RE-WSN is of order $\stackrel { \bf { \bar { O } } } { O } ( \frac { ( \log n ) ^ { - \beta / 2 } } { \log \log n } )$ (log ??)−??/2 .

Proof: For type-threshold PC-AFs, by a similar procedure to Theorem 4 and according to Theorem 4 of [7], each cell in the network lattice $\mathbb { L } ( { \sqrt { n } } , \kappa _ { 4 } { \sqrt { \log n } } , n )$ must operate at least $\kappa _ { 5 } N$ log log ?? transmissions, when each sensor produces ?? rounds of measurements, where $\kappa _ { 4 } , \kappa _ { 5 } ~ > ~ 0$ are some constants. By a similar argument to Theorem $^ { 4 , }$ there must be a level of aggregation that takes at least Ω(?? log log ??)??((log ??)−??/2) $\frac { \Omega ( \tilde { N } \log \log n ) } { { \cal O } ( ( \log n ) ^ { - \beta / 2 } ) } =$ $\Omega ( N \log \log n \cdot ( \log n ) ^ { \beta / 2 } )$ , which completes the proof.

Combining the lower bounds (Theorem 2 and Theorem 3) with upper bounds (Theorem 4 and Theorem 5), we get that

Theorem 6: The aggregation capacities for type-sensitive PC-AFs and type-threshold PC-AFs over RE-WSN are of order Θ((log ??)− ??2 −1) and Θ( (log ??)−??/2log log ?? ), $\Theta ( ( \log n ) ^ { - \frac { \beta } { 2 } - 1 } )$ $\Theta \big ( \frac { ( \log n ) ^ { - \beta / 2 } } { \log \log n } \big )$ respectively.

# V. LITERATURE REVIEW

The issue of capacity scaling laws for wireless ad hoc networks, initiated in the milestone work of Gupta and Kumar in [8], has been intensively studied under different assumptions and channel models. The first work about aggregation capacity scaling laws of WSN was done by Marco et al. [13]. They considered the capacity of random dense WSNs under the protocol model [8]. In [7], Giridhar and Kumar also focused on dense WSNs, and investigated the more general problem of computing and communicating symmetric functions of the sensor measurements. They showed that for type-sensitive functions and type-threshold functions, the aggregation capacities for random dense WSNs under the protocol model are of order $\Theta \big ( \frac { 1 } { \log n } \big )$ ( log ?? ) and $\Theta ( { \frac { 1 } { \log \log n } } )$ , respectively. Ying et al. studied the optimization problem of the total transmission energy for computing a symmetric function, subject to the constraint that the computation is $w . h . p .$ , correct. Moscibroda [14] derived the aggregation capacity scaling laws of perfectly compressible functions for worst-case networks. They showed that under the protocol model and physical model [8], the capacity for worstcase networks can be achieved of order $\Omega ( { \textstyle { \frac { 1 } { n } } } )$ and $\Omega \big ( \frac { 1 } { ( \log n ) ^ { 2 } } \big )$ respectively. All works mentioned above were done for the dense network model, and all results were derived under the binary-rate communication model. Under the cooperative paradigm, Zheng and Barton [21] demonstrated that the upper bound of the capacity of data collecting for extended WSNs is of order $\Theta ( \log n / n )$ and $\Theta ( 1 / n )$ when operating in fading environments with power path-loss exponents that satisfy $2 ~ < ~ \beta ~ < ~ 4$ and $\beta > 4 .$ , respectively. The work considered the aggregation functions without no in-network aggregation [18] , $e . g .$ , data downloading problem [7].

# VI. CONCLUSION

We emphasize that for random extended WSNs (RE-WSNs), the basic assumption of the protocol model and physical model [8] that any successful transmission can sustain a constant rate is over-optimistic and unpractical. We derive the first result on scaling laws of the aggregation capacity for RE-WSNs under generalized physical model. We show that, for general perfectly compressible aggregation functions (PC-AFs), the aggregation throughput of RE-WSNs can be achieved of order $\bar { \Omega _ { \ L } } \Big ( ( \log n ) ^ { - \frac { \beta } { 2 } - 1 } \Big )$ ; and for type-sensitive PC-AFs and type-threshold ${ \mathrm { P C } } { \mathrm { - A F s } } ,$ , aggregation capacities are of order respectively. $\Theta \^ { \ ' } \big ( ( \log n ) ^ { - \frac { \beta } { 2 } - 1 } \big )$ and $\Theta \left( \frac { 1 } { \log \log n } \cdot ( \log \bar { n } ) ^ { - \frac { \beta } { 2 } } \right)$ ,

# ACKNOWLEDGMENTS

The research of authors is partially supported by the National Basic Research Program of China (973 Program) under grants No. 2010CB328101, No. 2011CB302804, and No. 2010CB334707, the Program for Changjiang Scholars and Innovative Research Team in University, the Shanghai Key Basic Research Project under grant No. 10DJ1400300, the NSF CNS-0832120 and CNS-1035894, the National Natural Science Foundation of China under grant No. 60828003, the Program for Zhejiang Provincial Key Innovative Research Team, and the Program for Zhejiang Provincial Overseas High-Level Talents.

# REFERENCES

[1] A. Agarwal and P. Kumar. Capacity bounds for ad hoc and hybrid wireless networks. ACM SIGCOMM Computer Communication Review, 34(3):71–81, 2004.   
[2] R. Barton and R. Zheng. Cooperative Time-Reversal Communication is Order-Optimal for Data Aggregation in Wireless Sensor Networks. In IEEE ISIT, 2006.   
[3] O. Dousse and P. Thiran. Connectivity vs capacity in dense ad hoc networks. In Proc. IEEE INFOCOM 2004.   
[4] E. Duarte-Melo and M. Liu. Data-gathering wireless sensor networks: organization and capacity. Computer Networks, 43(4):519–537, 2003.   
[5] M. Franceschetti, O. Dousse, D. Tse, and P. Thiran. Closing the gap in the capacity of wireless networks via percolation theory. IEEE Trans. on Information Theory, 53(3):1009–1018, 2007.   
[6] H. Gamal. On the scaling laws of dense wireless sensor networks: the data gathering channel. IEEE Trans. on Information Theory, 51(3):1229– 1234, 2005.   
[7] A. Giridhar and P. Kumar. Computing and communicating functions over sensor networks. IEEE Journal on Selected Areas in Communications, 23(4):755–764, 2005.   
[8] P. Gupta and P. R. Kumar. The capacity of wireless networks. IEEE Trans. on Information Theory, 46(2):388–404, 2000.   
[9] A. Keshavarz-Haddad and R. Riedi. Bounds for the capacity of wireless multihop networks imposed by topology and demand. In Proc. ACM MobiHoc 2007.   
[10] A. Keshavarz-Haddad and R. Riedi. Multicast capacity of large homogeneous multihop wireless networks. In Proc. IEEE WiOpt 2008.   
[11] S. Li, Y. Liu, and X.-Y. Li. Capacity of large scale wireless networks under Gaussian channel model. In Proc. ACM Mobicom 2008.   
[12] X.-Y. Li. Multicast capacity of wireless ad hoc networks. IEEE/ACM Trans. on Networking, 17(3):950–961, 2009.   
[13] D. Marco, E. Duarte-Melo, M. Liu, and D. Neuhoff. On the manyto-one transport capacity of a dense wireless sensor network and the compressibility of its data. In IPSN 2003.   
[14] T. Moscibroda. The worst-case capacity of wireless sensor networks. In Proc. ACM/IEEE IPSN 2007.   
[15] A. Ozg ¨ Ur, O. L ¨ Ev´ Eque, and D. Tse. Hierarchical Cooperation Achieves ˆ Optimal Capacity Scaling in Ad Hoc Networks. IEEE Trans. on Information Theory, 53(10):3549–3572, 2007.   
[16] S. Shenker, S. Ratnasamy, B. Karp, R. Govindan, and D. Estrin. Datacentric storage in sensornets. ACM SIGCOMM Computer Communication Review, 33(1):142, 2003.   
[17] V. Vapnik and A. Chervonenkis. On the uniform convergence of relative frequencies of events to their probabilities. Theory of Probability and its Applications, 16(2):264–280, 1971.   
[18] P. Wan, C. Scott, L. Wang, Z. Wan, and X. Jia. Minimum-latency aggregation scheduling in multihop wireless networks. In Proc. ACM Mobihoc 2009.   
[19] C. Wang, C. Jiang, Y. Liu, X.-Y. Li, and S. Tang. Aggregation capacity of wireless sensor networks. Technical report, 2010, CS of HKUST: http://www.cse.ust.hk/%7Eliu/chengwang/Papers/aggregation-full.pdf.   
[20] C. Wang, X.-Y. Li, C. Jiang, S. Tang, and J. Zhao. Scaling laws on multicast capacity of large scale wireless networks. In Proc. IEEE INFOCOM 2009.   
[21] R. Zheng and R. Barton. Toward optimal data aggregation in random wireless sensor networks. In Proc. IEEE INFOCOM 2007.