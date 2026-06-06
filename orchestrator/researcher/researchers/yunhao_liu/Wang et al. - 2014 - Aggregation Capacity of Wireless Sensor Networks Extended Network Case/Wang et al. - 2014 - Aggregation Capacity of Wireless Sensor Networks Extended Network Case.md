# Aggregation Capacity of Wireless Sensor Networks: Extended Network Case

Cheng Wang, Changjun Jiang, Yunhao Liu, Senior Member, IEEE, Xiang-Yang Li, Senior Member, IEEE, and Shaojie Tang

Abstract—A critical function of wireless sensor networks (WSNs) is data gathering. One is often only interested in collecting a specific function of the sensor measurements at a sink node, rather than downloading all the raw data from all the sensors. In this paper, we study the capacity of computing and transporting the specific functions of sensor measurements to the sink node, called aggregation capacity, for WSNs. We focus on random WSNs that can be classified into two types: random extended WSN and random dense WSN. All existing results about aggregation capacity are studied for dense WSNs, including random cases and arbitrary cases, under the protocol model (ProM) or physical model (PhyM). In this paper, we propose the first aggregation capacity scaling laws for random extended WSNs. We point out that unlike random dense WSNs, for random extended WSNs, the assumption made in ProM and PhyM that each successful transmission can sustain a constant rate is over-optimistic and unpractical due to transmit power limitation. We derive the first result on aggregation capacity for random extended WSNs under the generalized physical model. Particularly, we prove that, for the type-sensitive divisible perfectly compressible functions and type-threshold divisible perfectly compressible functions, the aggregation capacities forrandom extended WSNs with nodes are of order  and  , respectively, where  > denotes the power attenuation exponent in the generalized physical model. Furthermore, we improve the aggregation throughput for general divisible perfectly compressible functions to  by choosing sensors from a small region (relative to the whole region) as sink nodes.

Index Terms—Wireless sensor networks, data aggregation, aggregation capacity

# 1 INTRODUCTION

WIRELESS sensor networks (WSNs) are composed of nodeswith the capabilities of sensing, communication and with the capabilities of sensing, communication and computation. One important application of wireless sensor networks (WSNs) is data gathering, i.e., sensor nodes transmit data, possibly in a multi-hop fashion, to a sink node. Actually, one is often only interested in collecting a relevant function of the sensor measurements at a sink node, rather than downloading all the data from all the sensors. Hence, it is necessary to define the capacity of computing and transporting specific functions of sensor measurements to the sink node. Since in-network aggregation plays a key role in improving such capacity for WSNs, we can reasonably call such capacity aggregation capacity for WSNs.

In this paper, we focus on scaling laws of the aggregation capacity for WSNs. Gupta and Kumar [1] initiated the study of capacity scaling laws for large-scale ad hoc wireless networks.

The main advantage of studying scaling laws is to highlight qualitative and architectural properties of the system without getting bogged down by too many details [1], [2]. Generally, the capacity scaling laws of a network are directly determined by the adopted network models, including deployment models, scaling models and communication models, besides the pattern of traffic sessions. According to the controllability of a network, Gupta and Kumar [1] defined two types of deployment models: arbitrary networks and random networks. In terms of scaling methods, there are two types of scaling network models, i.e., dense networks and extended networks. Moreover, the protocol model (ProM), physical model (PhyM) and generalized physical model (GphyM, also called Gaussian Channel model, [3]) are three typical communication models. Following these models, most works focus on the capacities for different traffic sessions, such as unicast, broadcast, multicast, anycast, and many-to-one session, etc. Data aggregation of WSNs studied in this paper can be regarded as a special case of many-to-one sessions. The involvement of in-network aggregation [4] makes it more complex than the general data collecting in many-to-one sessions. Naturally, aggregation capacity scaling laws have characteristics different from the capacity of any other sessions, which is worth studying.

There exists some literature dealing with scaling laws of the aggregation capacity for different functions, e.g., [4]–[8]. To the best of our knowledge, almost all related works, for both random networks and arbitrary networks, only have considered the dense network model, and the results are all derived under fixed-rate communication model [9], including ProM and PhyM [1]. Hence, in this work, we study aggregation capacity scaling laws for the random extended WSN, contrary to existing theoretical results that apply only to dense WSNs.

![](images/3c6cc29a2264f90f6ee836b3796e3120e27054e5d9b2729a24bcd33475c8c30a.jpg)



Fig. 1. Aggregation functions of interest.

Since the basic assumption in ProM and PhyM, i.e., any successful transmission can sustain a constant rate, is indeed over-optimistic and unpractical in extended networks, we use generalized physical model to capture the nature of wireless channels better.

We design an original aggregation scheme comprised of the tree-based routing and TDMA transmission scheduling. This scheme hierarchically consists of local aggregation phase and backbone aggregation phase. Based on this original aggregation scheme, we adopt two techniques to improve the aggregation capacity. The first one is to introduce block coding strategy into the local aggregation phase, by which the throughput during the local aggregation phase is improved; the second one is to devise the parallel transmission scheduling, which can improve the throughputs during both the local aggregation phase and backbone aggregation phase except for the bottleneck on the sink node.

Main Contributions: We now summarize major contributions of this paper as follows:

1. For a special subclass of symmetric functions, called divisible functions, we design an aggregation scheme, denoted by $\mathcal { A } _ { N , n } ,$ for the random extended WSN (RE-WSN), and derive the general result on the achievable aggregation throughput, depending on the characteristics of specific aggregation functions. Please see the relations among functions of interest studied in this paper in Fig. 1. (Theorem 1)   
2. For a special subclass of divisible functions, called divisible-perfectly-compressible aggregation functions (DPC-AFs), we show that under the scheme $\mathcal { A } _ { N , n } ,$ , the achievable aggregation throughput for RE-WSN is of order $\Omega ( ( \log n ) ^ { - { \frac { \alpha } { 2 } } - 1 } )$ . (Theorem 2)   
3. For a special subclass of DPC-AFs, called type-threshold DPC-AFs, such as max (or min), range, and various kinds of indicator functions, we devise a new aggregation scheme, denoted by $\boldsymbol { \mathcal { A } } _ { N , n } ^ { b c } ,$ by integrating the block coding [4] into the scheme $\mathcal { A } _ { N , n } .$ We show that under $\mathcal { A } _ { N , n } ^ { b c }$ the $\Omega ( \frac { ( \log n ) ^ { - \alpha / 2 } } { \log \log n } )$ aggregation capacity for RE-WSN is of order. (Theorem 3)   
4. For two subclasses of $\mathrm { D P C - A F s , i . e . , }$ type-sensitive DPC-AFs (e.g., average function) and type-threshold DPC-AFs, we derive the upper bounds on aggregation capacities, and prove that our schemes $\mathcal { A } _ { N , n }$ and $\boldsymbol { \mathcal { A } } _ { N , n } ^ { b c }$ are optimal

for type-sensitive DPC-AFs and type-threshold DPC-AFs, respectively. Combining the lower bounds (Theorem 2 and Theorem 3) with the upper bounds (Theorem 4 and Theorem 5), we obtain the tight bounds on aggregation capacities for type-sensitive DPC-AFs and typethreshold DPC-AFs are of order $\Theta \Big ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } \Big )$ and Θ $\left( \frac { ( \log n ) ^ { - \alpha / 2 } } { \log \log n } \right)$ , respectively. (Theorem 6)

5. By choosing sensors randomly from a small region, of which the area is an infinitesimal proportion, i. $\mathbf { e . , } \Theta ( \textstyle { \frac { \log n } { n } } ) .$ , of the total area of the RE-WSN, as the sink nodes, we design a parallel aggregation scheme, denoted by $\mathcal { A } _ { N , n } ^ { p } .$ . Under this scheme, we introduce a technique called parallel transmission scheduling, and show that for DPC-AFs, the measurements from all sensors can be aggregated into those sink nodes at a throughput of order . (Theorem 7)

The rest of the paper is organized as follows. In Section $^ { 2 , }$ we introduce the system model. In Section 3, we propose the specific aggregation schemes for RE-WSNs to derive the achievable aggregation capacity. In Section 4, we compute the upper bounds on the aggregation capacities for typesensitive divisible perfectly compressible functions and divisible type-threshold perfectly compressible functions, then obtain the tight capacity bounds for two types of functions. In Section 5, we make efforts in improving further the aggregation capacity for RE-WSNs by introducing the technique called parallel transmission scheduling. In Section 6, we review the related work. In Section 7, we draw some conclusions and discuss the future work.

# 2 SYSTEM MODEL

Throughout the paper, we mainly consider the events that happen with high probability (w.h.p.) as the scale of a network (the number of sensors in a network) goes to infinity.

# 2.1 Aggregation Capacity

We consider a random WSN, denoted by $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n ) , ^ { 1 }$ where sensors are placed uniformly at random in a square $\mathcal { A } ( \mathfrak { a } ^ { 2 } ) = [ 0 , \mathfrak { a } ] \overset { \cdot } { \times } [ 0 , \mathfrak { a } ] .$ , and a sensor, denoted by $s _ { 0 } ,$ , is chosen as the sink node. Like in most models considered in related works, every sensor node $s _ { i } , 0 \leq i \leq n - 1 ,$ , periodically generates measurements of the environment that belong to a fixed finite set M with $| { \mathcal { M } } | = \mathfrak { m }$ , and the function of interest is then required to be computed repeatedly. Intuitively, the capacity for WSNs depends on the aggregation functions of interest to the sink node, [4], [8].

# 2.1.1 Formal Notations

Define the aggregation function of interest to the sink node as $\mathbf { g } _ { n } : \mathcal { M } ^ { n }  \mathcal { G } _ { n } ;$ ; furthermore, for any $k , 1 \leq k \leq n ,$ , define the function of the sensor measurements as $\mathbf { g } _ { k } : \mathcal { M } ^ { k }  \mathcal { G } _ { k } ,$ , where $\mathcal { G } _ { k }$ is the range of $\mathbf { g } _ { k }$ . Suppose that each sensor has an associated block of readings, known a priori [4]. We define $N$ rounds of measurements from all sensors as a processed unit. From a practical perspective, only the same round of measurements, which are usually attached to the same time

1. The results in this paper also apply to the random network where the sensors are placed in the region $\ddot { \mathcal { A } } ( \alpha ^ { 2 } ) = [ 0 , \alpha ] \times [ 0 , \alpha ]$ according to a Poisson point process of density $\textstyle \lambda = { \frac { \dot { n } } { \alpha ^ { 2 } } }$ .

![](images/13ad955373eca57b348509fe63c1b7cf29b4435382aa4d443c374f0cfb75d72c.jpg)



Fig. 2. System model. An aggregation unit consists of measurements. Each measurement can be indicated by m bits, [10].

stamps, are requested and permitted to be aggregated. Please see the illustration in Fig. 2. We first introduce some notations.

A processed unit consisting of rounds of measurements from all sensors is denoted by ${ \textbf { a } } \ n \times N$ matrix $M ^ { n \times N } \in \mathcal { M } ^ { n \times N }$ , where $M ^ { n \times N } ( i , j )$ is the th measurement of sensor node $s _ { i } , M ^ { n \times N } ( i , \cdot )$ is the th row of $M ^ { n \times N } , \mathrm { i . e . , }$ the block of measurements of sensor node $s _ { i } ,$ and $M ^ { n \times N } ( \cdot , j )$ is the th column of $\mathcal { M } ^ { n \times N }$ , i.e., the set of the th measurements of all sensor nodes.   
For a -vector $M ^ { k } = [ M _ { 1 } , M _ { 2 } , \ldots , M _ { k } ] ^ { T } \in \mathcal { M } ^ { k }$ , where $M _ { i } \in { \mathcal { M } } ,$ , define $\mathbf { g } _ { k } ( M ^ { k } ) : = \mathbf { g } _ { k } ( M _ { 1 } , M _ { 2 } , \ldots , M _ { k } )$ .   
Given a matrix $M ^ { k \times N } , 1 \le k \le n ,$ , define   
$\bullet \ \mathbf { g } _ { k } ^ { \mathrm { N } } ( M ^ { k \times N } ) : = ( \mathbf { g } _ { k } ( M ^ { k \times N } ( \cdot , 1 ) ) , \ldots , \mathbf { g } _ { k } ( M ^ { k \times N } ( \cdot , N ) ) ) .$   
An aggregation scheme dealing with the aggregation of rounds of measurements, denoted by $\mathcal { A } _ { N , n } ,$ determines a sequence of message passings between sensors and computations at sensors. Under the scheme $\mathcal { A } _ { N , n } ,$ input any $\mathbf { \bar { \boldsymbol { M } } } ^ { n \times N } \in \mathcal { M } ^ { n \times N }$ , output a result $\mathbf { g } _ { n } ^ { \mathrm { N } } ( M ^ { n \times N } )$ at the sink node $s _ { 0 }$ .

# 2.1.2 Capacity Definition

First, we give the definition of achievable aggregation throughput for WSNs. All the logs in this paper are to the base 2.

Definition 1. A throughput of $\Lambda ( n )$ bits/s is achievable for a given aggregation function ${ \bf { g } } _ { n }$ if there is an aggregation scheme, denoted by $\mathcal { A } _ { N , n } ,$ by which any $\mathbf { \bar { \boldsymbol { M } } } ^ { n \times N } \in \mathcal { M } ^ { \times N }$ can be aggregated into $\mathbf { g } _ { n } ^ { \mathrm { { N } } } ( M ^ { n \times N } )$ at the sink node within $T ( \mathcal { A } _ { N , n } )$ seconds, where $\begin{array} { r } { \dot { \Lambda ( n ) } \le \frac { N \cdot \log \mathfrak { m } } { T ( A _ { N , n } ) } , \mathfrak { m } = | \mathcal { M } | } \end{array}$ , and m is the total number of bits representing measurements from each sensor.

Based on Definition 1, we define the aggregation capacity for random WSNs.

Definition 2. For a given aggregation function $\mathbf { g } _ { n } ,$ we say that the aggregation capacity of a class of random WSNs is of order $\Theta ( f ( n ) )$ bits/s for ${ \bf g } _ { n } , i f$ there are constants $c > 0$ and $c < d < + \infty$ such that

$$
\lim _ {n \to + \infty} \operatorname * {P r} (\Lambda (n) = c \cdot f (n) \text {   is   achievable   for   } \mathbf {g} _ {n}) = 1,
$$

$$
\liminf _ {n \to + \infty} \operatorname * {P r} (\Lambda (n) = d \cdot f (n) \text {   is   achievable   for   } \mathbf {g} _ {n}) <   1.
$$

# 2.1.3 Aggregation Functions of Interest

We focus our attention to the symmetric functions, which are invariant with respect to permutations of their arguments. That is, for $1 \leq k \leq n ,$ , and for all permutation $\sigma ,$ it holds that ${ \bf g } _ { k } ( M _ { 1 } , M _ { 2 } , \ldots , M _ { k } ) = { \bf g } _ { k } ( \sigma ( M _ { 1 } , \bar { M } _ { 2 } , \ldots , M _ { k } ) )$ . From an application standpoint, many natural functions of interest, including most statistical functions, belong to this class. Symmetric functions embody the data centric paradigm [4], [11], where it is the data generated by a sensor that is of primary importance, rather than its identity [4]. Furthermore, we limit the scope of this work to a special subclass of symmetric functions, called divisible functions [4], which can be computed in a divide-and-conquer fashion. Divisible functions are usually deemed as the general functions in the study of data aggregation in WSNs.

Next, we introduce other two special subclasses of symmetric functions, called type-sensitive functions and typethreshold functions, respectively.

Type-Sensitive Functions: A symmetric function ${ \bf g } _ { n } ( \cdot )$ is said to be type-sensitive if there exist a constant with $< \theta < 1 ,$ , and an integer $n _ { 0 } ,$ , such that for $n \geq n _ { 0 } .$ , and any $i \leq n - \lceil \theta n \rceil ,$ given any subset $\{ M _ { 1 } , M _ { 2 } , \ldots , M _ { i } \}$ , there are two subsets of values $\{ \bar { M } _ { i + 1 } ^ { \prime } , M _ { i + 2 } ^ { \prime } , . . . , M _ { n } ^ { \prime } \}$ and $\{ M _ { i + 1 } ^ { \prime \prime } , M _ { i + 2 } ^ { \prime \prime } , . . . , M _ { n } ^ { \prime \prime } \}$ , such that

$$
\mathbf {g} _ {n} (M _ {1}, \ldots , M _ {i}, M _ {i + 1} ^ {\prime}, \ldots , M _ {n} ^ {\prime}) \neq \mathbf {g} _ {n} (M _ {1}, \ldots , M _ {i}, M _ {i + 1} ^ {\prime \prime}, \ldots , M _ {n} ^ {\prime \prime}).
$$

For a -vector $M ^ { n } \in \mathcal { M } ^ { n }$ , the mode of $M ^ { n } \left( \mathrm { i . e . } \right.$ , the value that occurs most frequently), the mean of $M ^ { n }$ , the median of $M ^ { n }$ , and the standard deviation of $M ^ { n }$ all belong to the type-sensitive functions.

Type-Threshold Functions: A symmetric function ${ \bf g } _ { n } ( \cdot )$ is said to be type-threshold if there exists a nonnegative m-vector $\xi ,$ called the threshold vector, such that

$$
\mathbf {g} _ {n} (M ^ {n}) = \mathbf {g} _ {\mathfrak {m}} ^ {\prime} (\phi (M ^ {n})) = \mathbf {g} _ {\mathfrak {m}} ^ {\prime} (\min \{\phi (M ^ {n}), \xi \}),
$$

for all $M ^ { n } \in { \mathcal { M } } ^ { n }$ , with min signifying element-wise minimum, where $\phi ( M ^ { n } )$ is called type-vector that is defined as

$$
\phi (M ^ {n}) = \left[ \phi_ {1} (M ^ {n}), \phi_ {2} (M ^ {n}), \dots , \phi_ {\mathfrak {m}} (M ^ {n}) \right],
$$

with $\phi _ { k } ( M ^ { n } ) : = | \{ s _ { i } : M _ { i } = k \} |$ .

For a -vector $M ^ { n } \in \mathcal { M } ^ { n }$ , the max function, the min function and the range function $M _ { i } - \operatorname* { m i n } _ { i } M _ { i } )$ of $M ^ { n }$ , the th largest value of $M ^ { n } ,$ , the mean of the largest values of $M ^ { n } ,$ , and the indicator function $I \{ M _ { i } = k ,$ all belong to typethreshold functions.

Note that there are indeed some symmetric functions which are neither type-sensitive nor type-threshold, [4]. Please see the illustration in Fig. 1.

Specially, we focus on an important class of symmetric functions called divisible-perfectly-compressible aggregation functions (DPC-AFs). A divisible function is perfectly compressible if all information concerning the same measurement round contained in two or more messages can be perfectly aggregated in a single new packet of equal size (in order sense), [8]. The following lemma is straightforward.

Lemma 1. For any divisible-perfectly-compressible aggregation function $( D P C \cdot A F ) \ \mathbf { g } _ { k } , 1 \leq k \leq n ,$ , it holds that $| \mathcal { G } _ { k } | = \Theta ( \mathfrak { m } )$ , where $\mathcal { G } _ { k }$ is the range of the function $\mathbf { g } _ { k }$ .

We mainly consider two subclasses of DPC-AFs, i.e., typesensitive DPC-AFs and type-threshold DPC-AFs. A DPC-AF is type-sensitive (or type-threshold) if it is a type-sensitive function (or type-threshold function). Please see the illustration in Fig. 1.

Intuitively, the value of a type-sensitive function cannot be determined if a large enough fraction of the arguments are unknown, whereas the value of a type-threshold function can be determined by a fixed number of known arguments. A representative case of type-sensitive DPC-AFs is the average function; while, the typical type-threshold DPC-AFs include max (or min), range, and various kinds of indicator functions.

# 2.2 Communication Model

A communication model can be defined as a interference-safe feasible family [12] in which each element is a set consisting of the links that can transmit simultaneously without negative effects, or in order sense, on each other in terms of link rate. Generally, there are two types of communication models in the research of capacity bounds: adaptive-rate communication model and fixed-rate communication model.

# 2.2.1 Adaptive-Rate Communication Model (ACM)

Under the adaptive-rate communication model, the reliably transmission rate is determined based on a continuous function of the receiver’s SINR (Signal to Interference plus Noise Ratio). Generally, any communication pair $v _ { i }  v _ { j }$ can establish a direct link, over a channel of bandwidth $B ,$ of rate $\begin{array} { r } { R ( v _ { i } , v _ { j } ) = B \log ( 1 + \frac { 1 } { \eta } \cdot \mathrm { S I N R } ( v _ { j } ) ) } \end{array}$ . When $\eta > 1$ , the receiver can achieve the maximum rate that meets a given BER requirement under a specific modulation and coding scheme. When $\eta = 1$ , the adaptive-rate channel model is also called generalized physical model (GphyM) [3], [13]. It is practically assumed that all nodes are individually power-constrained under GphyM, i.e., for any node $v _ { i } ,$ it transmits at a constant power $\bar { P } _ { i } \in [ P _ { m i n }$ $P _ { m a x } ] ,$ , where $P _ { m i n }$ and $P _ { m a x }$ are some positive constants. The receiver $v _ { j }$ receives the signal from the transmitter $v _ { i }$ with strength $\dot { P } _ { i } \cdot \ell ( v _ { i } , v _ { j } ) .$ , where $\ell ( v _ { i } , v _ { j } )$ indicates the path loss between $v _ { i }$ and $v _ { j } .$ Any two nodes can establish a direct communication link, over a channel of bandwidth $B ,$ of rate

$$
R (v _ {i}, v _ {j}) = B \log \left(1 + \frac {P _ {i} \cdot \ell (v _ {i} , v _ {j})}{N _ {0} + \sum_ {v _ {k} \in A (i)} P _ {k} \cdot \ell (v _ {k} , v _ {j})}\right), \tag {1}
$$

where $N _ { 0 } > 0$ is the ambient noise power at the receiver, and $A ( i )$ is the set of nodes transmitting concurrently with $v _ { i }$ . The wireless propagation channel typically includes path loss with distance, shadowing and fading effects. As in $[ 3 ] , [ 9 ] , [ 1 3 ] , [ 1 4 ] ,$ we assume that the channel gain depends only on the Euclidean distance between a transmitter and receiver, and ignore shadowing and fading.

# 2.2.2 Fixed-Rate Communication Model (FCM)

To simplify the analysis of the system, Gupta and Kumar [1] defined the fixed-rate communication model as the abstraction of the wireless communication model, under which if the value of a defined conditional expression is beyond some threshold, the transmitter can send successfully to the receiver at a specific constant data rate; otherwise, it can not send any, $\mathrm { i . e . , }$ the transmission rate is assumed to be a binary function. The protocol model (ProM) and physical model (PhyM) defined in [1] both belong to the fixed-rate channel model. The former’s conditional expression is the fraction of the distances from the intended transmitter and other ones to a specific receiver; the latter’s conditional expression is SINR. Obviously, the validity of FCM is based on the following assumption.

Assumption 1. Any successful transmission can sustain the rate of a fixed constant order.

# 2.3 Network Scaling Model

We clarify the differences between the random extended WSN (RE-WSN) and random dense WSN (RD-WSN).

# 2.3.1 Criteria of Scaling Patterns

In the research of network capacity scaling laws, there are two typical models in terms of scaling patterns of the network: extended scaling model and dense scaling model [2], [13], [15]. The major difference between the engineering implications of these two scaling models is related to the classical notions of interference-limitedness and coverage-limitedness. The dense networks tend to have dense deployments so that signals are received at the users with sufficient signal-to-noise ratio (SNR) but the throughput is limited by interference among the simultaneous transmissions. That is, all nodes can communicate with each other with sufficient SNR, and the throughput can only be interference-limited. While, the extended networks tend to have sparse deployments so that the throughput is mainly limited by the ability to transmit signals to the users with sufficient SNR. That is, the source and destination pairs are at increasing distance from each other, so both interference limitation and power limitation can come into play.

Recall that a given random network $\mathcal { N } ( \bar { \alpha } ^ { 2 } , \bar { n } )$ is constructed by placing uniformly at random sensors in a square deployment region $\mathcal { A } ( \alpha ^ { 2 } ) = \dot { [ 0 , \alpha ] } \times [ 0 , \alpha ]$ . Next, we examine the scaling characteristics of ${ \mathcal { N } } ( \alpha ^ { 2 } , n )$ as $n  \infty ,$ , according to the relation between a and .

First, we recall some existing results about random Euclidean Minimum Spanning Tree (EMST) from [16]–[21]. Let $\mathcal { T } ( \mathfrak { a } ^ { 2 } , n )$ denote the length of the longest edge of EMST built on the set of nodes in the random network ${ \bar { \mathcal { N } } } ( \alpha ^ { 2 } , n )$ . For the random variable $\textstyle { \mathcal { T } } ( \alpha ^ { 2 } , n )$ , according to a related result proven in [16], Li et al. [20], [21] proposed the following lemma.

Lemma 2. ([20], [21]). For the random variable $\scriptstyle { \mathcal { T } } ( \alpha ^ { 2 } , n )$ , and for any real number $\nu ( n )$ , it holds that

$$
\lim _ {n \rightarrow \infty} \operatorname * {P r} \left(n \pi \cdot \left(\frac {\mathcal {T} (\mathfrak {a} ^ {2} , n)}{\mathfrak {a}}\right) ^ {2} - \ln n \leq \nu (n)\right) = \frac {1}{e ^ {e ^ {- \nu (n)}}},
$$

where is the natural logarithm to the base .

Based on Lemma 2, let $\nu ( n ) { \underline { { = } } } -$ , we get that $\begin{array} { r } { T ( \mathfrak { a } ^ { 2 } , n ) = \Omega ( \mathfrak { a } \cdot \sqrt { \frac { \ln n } { n } } ) , \mathrm { i . e . , } \Omega ( \mathfrak { a } \cdot \sqrt { \frac { \log n } { n } } ) } \end{array}$ with high probability, $\begin{array} { r } { \mathrm { e . g . , ~ } 1 - \frac { 1 } { n ^ { \prime } } } \end{array}$ and let $\nu ( n ) = \ln n ,$ we obtain that $\begin{array} { r } { T ( \mathfrak { a } ^ { 2 } , n ) = O ( \mathfrak { a } \cdot \sqrt { \frac { \log n } { n } } ) } \end{array}$ with high probability, e.g., at least $\textstyle 1 - { \frac { 1 } { n } } .$ . Hence, we have

$$
\lim _ {n \to \infty} \operatorname * {P r} \left(\mathcal {T} (\mathfrak {a} ^ {2}, n) = \Theta \left(\mathfrak {a} \cdot \sqrt {\frac {\log n}{n}}\right)\right) \geq 1 - \frac {1}{n}. \tag {2}
$$

Now, we can define the criterion of the extended scaling versus dense scaling networks according to the order of the length of $\begin{array} { r l } {  { T ( \mathfrak { a } ^ { 2 } , n ) , \mathrm { i . e . , \ } \Theta ( \mathfrak { a } \cdot \sqrt { \frac { \log n } { n } } ) } } \end{array}$ .

Definition 3. Given a random network ${ \mathcal { N } } ( \alpha ^ { 2 } , n ) ,$ , it is dense scaling if $\mathfrak { a } \cdot \sqrt { \frac { \log n } { n } } = O ( 1 )$ , i.e., $\mathfrak { a } = O \big ( \sqrt { \frac { n } { \log n } } \big ) .$ , with high is extended scaling,, with high probability. $i f \ a \cdot { \sqrt { \frac { \log n } { n } } } = \omega ( 1 )$ , i.e., $\begin{array} { r } { \alpha = \omega \big ( \sqrt { \frac { n } { \log n } } \big ) } \end{array}$

# 2.3.2 RE-WSN vs. RD-WSN

The extended network and dense network are the representative cases of the extended and dense scaling models, respectively. They are specialized into the cases of ${ \mathfrak { a } } = { \sqrt { n } }$ and $\alpha = 1$ , respectively, i.e., they can be denoted by $\mathcal { N } ( n , n )$ and $\sqrt { ( 1 , n ) }$ , respectively. A random dense WSN (RD-WSN) represents the scenario where the monitoring region is fixed, and the scale of a network is expanding as the density of sensors is increasing; while, a random extended WSN (RE-WSN) represents the scenario where the density of sensors is fixed, and the scale of the network is expanding as the area of monitoring region is increasing.

Denote the sets of all sensors in the RE-WSN and RD-WSN by $ { \boldsymbol { S } } _ { e }$ and $\boldsymbol { S } _ { d } ,$ respectively. Furthermore, denote $\begin{array} { r } { \boldsymbol { S } _ { e } = \boldsymbol { S } _ { d } : = } \end{array}$ $\{ s _ { 0 } \} \cup \{ s _ { 1 } , s _ { 2 } , . . . , \bar { s } _ { n - 1 } \}$ , where $s _ { 0 }$ is the sink node and $s _ { i }$ $( 1 \leq i \leq n - 1 )$ denotes the sensor node.

# 2.3.3 Communication Models in Scaling Models

Now, we analyze the combinations of communication models and scaling models, and make a choice of communication model for this paper. Following the setting in [13], the channel power gain is given by $\ell ( v _ { i } , v _ { j } ) =$ min $\{ 1 , \breve { d } _ { i j } ^ { - \alpha } \}$ in the extended scaling network; and it is given by $\ell ( v _ { i } , v _ { j } ) ^ { \prime } = d _ { i j } ^ { - \alpha }$ in the dense scaling network. Here, $d _ { i j } = \| v _ { i } v _ { j } \|$ is the Euclidean distance between two nodes $v _ { i }$ and $v _ { j } , \alpha > 2$ denotes the power attenuation exponent [13].

FCM in Dense Scaling Networks: Gupta and Kumar [1] only defined the FCM, including protocol model and physical model, in dense networks under which Assumption 1 is convincing because the large enough SINR (generally of order ) can be obtained. Thus, most results of the aggregation capacity [4], [5], [22], [23] derived under FCM are reasonable for dense networks.   
GphyM in Dense Scaling Networks: In dense networks, FCM can be regarded as a perfect abstraction of the generalized physical model (GphyM). Indeed, the capacity derived under GphyM can be equally derived by using FCM, and vice versa.   
FCM in Extended Scaling Networks: In extended networks, according to Definition $^ { 3 , }$ under any routing scheme for a random network $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ , there must be, $w . h . p . , \mathsf { a }$ link of distance of order $\begin{array} { r } { \Omega ( \bar { \boldsymbol { \alpha } } \cdot \sqrt { \frac { \log n } { n } } ) , \mathrm { i . e . , } \omega ( 1 ) } \end{array}$ . By Equation (1), the SINR of such a link is too small to contribute to a constant rate. In other words, Assumption 1 is over-optimistic for random extended networks.   
GphyM in Extended Scaling Networks: The GphyM can appropriately embody the continuous link rate in extended networks, which is the reason why most existing studies on the capacity for extended networks are implemented under GphyM, [3], [9], [13], [24].

# 3 LOWER BOUNDS ON AGGREGATION CAPACITY

To simplify the description, we define a notion called network lattice that is frequently used in the design of aggregation schemes and the analysis of network characteristics.

Definition 4. (Network Lattice). For a network $\mathcal { N } ( \mathfrak { a } ^ { 2 } , n )$ , divide the deployment region $\mathcal { A } ( \mathfrak { a } ^ { 2 } )$ into a lattice consisting of subsquares (cells) of side length l, we call the generated lattice network lattice, and denote it by L a l .

From now on, we focus on the RE-WSN $\mathcal { N } ( n , n )$ .

# 3.1 Aggregation Scheme for General Divisible Functions

Our aggregation scheme, denoted by $\mathcal { A } _ { N , n . }$ , is designed based on the network lattice $\mathbb { L } _ { 1 } = \mathbb { L } ( { \sqrt { n } } , 2 { \sqrt { \log n } } , n )$ . To simplify the description, we ignore the details about the integers, and assume that the number of rows (or columns) $\textstyle { \frac { { \sqrt { n } } } { 2 { \sqrt { \log n } } } }$ is always an integer, which has no impact on the results due to the characteristics of scaling laws issue. Taking the cell in top left corner as the origin with a 2-dimensional index (0,0), we give each cell in $\mathbb { L } _ { 1 }$ an index in the order from left to right and from top to bottom, i.e., the index of the cell in bottom right corner is $( \delta , \delta )$ , where $\begin{array} { r } { \delta = \delta ( n ) = \frac { \sqrt { n } } { 2 \sqrt { \log n } } - 1 } \end{array}$ . By using VC Theorem (Theorem 25 in [3]), we have the following result,

Lemma 3. For all subsquares of side length ${ \mathrm { I } } = 2 { \sqrt { \log n } }$ in the deployment region ${ \mathcal { A } } ( n ) ,$ , the number of sensors in those cells is uniform w.h.p., within $\begin{array} { r } { \frac { \log n } { 2 } < n _ { i , j } < 8 \log n . } \end{array}$ .

The proof of Lemma 3 is very similar to that of Lemma 18 in [20] (based on VC theorem [25]). Note that the involved constants in Lemma 3, i.e., and $8 ,$ do not change the final scaling laws of aggregation capacity indeed.

# 3.1.1 Aggregation Routing Scheme

The aggregation routing tree is divided into two levels, i.e., the aggregation backbones and local aggregation links.

Aggregation Backbones: In the network lattice $\mathbb { L } _ { 1 } ,$ , from the cells, except for that one containing $s _ { 0 } ,$ we randomly choose one sensor from each cell, and obtain a set, denoted by $B _ { s }$ consisting of $\left( \delta + 1 \right) ^ { 2 } - 1$ nodes (sensors). Then, define the set ${ \vec { B } } : = { \vec { B } } _ { s } \bigcup \left\{ s _ { 0 } \right\}$ as backbone set. We call the nodes in B as aggregation stations, or simply as stations.

We assume that the sink $s _ { 0 }$ is located in the cell $C _ { \delta , \delta }$ . By connecting the adjacent aggregation stations in the same rows, as illustrated in Fig. 3(a), we construct the horizontal backbones of the aggregation routing; by connecting the adjacent stations in th column, we build the vertical backbone. For the general case in terms of the location of sink $s _ { 0 } ,$ , we introduce the extending method as follows: Assume that $s _ { 0 }$ is located in the cell $C _ { i , j } ,$ the difference in the construction of routing backbone is that the vertical backbone is built in th column, instead of in th column, as illustrated in Fig. 3(b). In fact, we can build a multihop path between the station in cell $C _ { \delta , \delta }$ and the sink in $C _ { i , j } ,$ as illustrated in Fig. 3(c). It can be proven that any such path is definitely not the bottleneck throughout routing. In words, the location of $s _ { 0 }$ does not change scaling laws of the aggregation capacity.

Local Aggregation Links: In each cell of $\mathbb { L } _ { 1 } ,$ all sensors, except for the station, communicate with the station in a single hop. Please see the illustration in Fig. 4(a).

![](images/a24db267f2252f3244cb061ba59465ab844e7949f93b5ec9d380bb8c5d6d1cf1.jpg)



(a) $s _ { 0 } \mathrm { ~ i n ~ } C _ { \delta , \delta }$

![](images/feac61994c070b674ce119b5927958182d9143572cea398835ca1f4aa807ba38.jpg)



(b) sink in $C _ { i , j }$

![](images/0a87cb1e1ea454fcae7957f52830537ab73c2165d07355d56cc75d140ecb7582.jpg)



(c)additional path   
Fig. 3. Construction of aggregation backbones. (a) The case that we mainly focus on in this paper. (b) The general case in terms of the location of $s _ { 0 }$ (c) The additional path from our final station to the sink $s _ { 0 } .$

![](images/f754b2391a71117f803d6506e4df21268d46fdefdcb87190c89a9857f48496c3.jpg)



(a)Local Aggregation

![](images/9adb248d78ded7af07dc1b30631f960b43743b7db4e2d24b8aeb474b5821f13e.jpg)



(b)Limiting Interference   
Fig. 4. Local aggregation. (a) A 4-TDMA scheme is adopted. Each slot is further divided into subslots that are assigned to all links in the cell. (b) 4-TDMA scheme guarantees that the distance between any receiver and the nearest unintended transmitters is of at least $\operatorname { I } = 2 { \sqrt { \log n } }$ .

# 3.1.2 Aggregation Scheduling Scheme

In a global perspective, the aggregation scheduling scheme is divided into two phases: local aggregation scheduling and backbone aggregation scheduling. In both phases, all scheduled senders transmit with a same fixed power $P \in [ P _ { m i n } , P _ { m a x } ]$ . In first phase, each aggregation station collects the measurements from the sensors in its assigned cell in L . In second phase, the data in the aggregation stations are collected into the sink node (not simply level by level). Recall that we make a group of rounds of measurements from all sensors as a processed unit, denoted by a matrix $M ^ { n \times N }$ (Please refer to Section 2.1.1).

Local Aggregation Scheduling: Firstly, we use a 4-TDMA scheme to schedule the cells in L , as illustrated in Fig. 4(a). In this phase, only the links completely contained in some cells are scheduled. From Lemma 3, the number of all links in each cell is w.h.p., not more than . Then, we can further divide each slot of the 4-TDMA scheme into subslots, by which we can ensure that all links can be scheduled once during a scheduling period that consists of subslots.

Backbone Aggregation Scheduling: In this phase, the aggregated data are sent to the sink in a pipelined fashion [4], [8], and are aggregated on the way in each aggregation station. The backbone aggregation scheduling consists of two phases: horizontal backbone phase and vertical backbone phase. First, the data are horizontally aggregated into the stations in th column; then the data are vertically aggregated into the sink node in the cell $C _ { \delta , \delta }$ .

In the initial state of horizontal scheduling, for all and $j ,$ the aggregation station in cell $C _ { i , j } ,$ denoted by $b _ { i , j } ,$ , holds aggregation functions values of rounds of measurements from all sensors in $C _ { i , j }$ that can be denoted by a matrix $M ^ { n _ { i , j } \times N }$ . Denote those aggregation functions by

$$
\mathbf {g} _ {n _ {i, j}} ^ {\mathrm{N}} (M ^ {n _ {i, j} \times N}) = (\mathbf {g} _ {n _ {i, j}} (M ^ {n _ {i, j} \times N} (\cdot , z)), z = 1, 2, \dots , N).
$$

By this time, denote all rounds of data held by all $( \delta + 1 ) ^ { 2 }$ stations as a matrix $M _ { h } ^ { ( \delta + 1 ) ^ { 2 } \times N }$ .

During the horizontal backbone phase, denote the set of $b _ { i , j }$ and all its descendants by $D _ { i , j } ^ { h } ,$ thus the cardinality of $D _ { i , j } ^ { h }$ is $| D _ { i , j } ^ { h } | = \Theta ( ( j + 1 )$ . Then, the aggregation function value of the th round of data at station $b _ { i , j }$ is denoted by

$$
\mathfrak {b} _ {i, j} ^ {h} (k) := \mathbf {g} _ {| D _ {i, j} ^ {h} |} (M _ {h} ^ {| D _ {i, j} ^ {h} | \times N} (\cdot , k)). \tag {3}
$$

Here, $\mathfrak { b } _ { i , 0 } ^ { h } ( k ) = \mathbf { g } _ { n _ { i , 0 } } ( M ^ { n _ { i , 0 } \times N } ( \cdot , k ) )$ , for $k = 1 , 2 , \ldots , N .$

In the initial state of the vertical backbone phase, all stations $b _ { i , \delta }$ hold aggregation function values of rounds of data from the stations $\bar { b _ { i , j } } , 0 \leq j \leq \delta , \mathrm { i . e . , } \mathrm { b } _ { i , \delta } ^ { h } ( k ) , 1 \leq k \leq N$ .

By this time, denote rounds of data holden by all $\delta + 1$ stations as a matrix $M _ { v } ^ { ( \delta + 1 ) \times N }$ . Denote the set of $b _ { i , \delta }$ and all its descendants by $D _ { i . \delta } ^ { v } ,$ then the cardinality of $D _ { i , \delta } ^ { v }$ is $| D _ { i , \delta } ^ { v } | = \Theta ( ( i + \bar { 1 } ) \cdot \sqrt { n \log n } )$ . During the vertical backbone phase, the value of the aggregation function of the th round of data at station $b _ { i , \delta }$ is denoted by

$$
\mathfrak {b} _ {i, \delta} ^ {v} (k) := \mathbf {g} _ {| D _ {i, \delta} ^ {v} |} (M _ {v} ^ {| D _ {i, \delta} ^ {v} | \times N} (\cdot , k)). \tag {4}
$$

Here, $\mathfrak { b } _ { 0 , \delta } ^ { v } ( k ) = \mathfrak { b } _ { 0 , \delta } ^ { h } ( k )$ , for $k = 1 , 2 , \ldots , N .$

We adopt a 9-TDMA scheme to schedule the horizontal backbones, as illustrated in Fig. 3(a), and adopt a 3-TDMA scheme to schedule the vertical backbone. We design Algorithm 1 and Algorithm 2 to schedule the horizontal and vertical backbone aggregations in a pipelined fashion, respectively. Implementing two algorithms once, we can compute aggregation function values of rounds of measurements at the sink node. Before presenting these two algorithms, we define two sequences of sets:

For $h = 0 , 1 , 2$ and $v = 0 , 1 , 2 ,$ define

$$
\mathcal {H} _ {h, v} := \{b _ {i, j} | i \bmod 3 = h, \text {   and   } j \bmod 3 = v \};
$$

for $h = 0 , 1 , 2 ,$ define $\mathcal { V } _ { h , \delta } : = \{ b _ { i , \delta } | i$ mod 3 = h}.

Algorithm 1. Horizontal Backbone Aggregation

Input: $\mathbf { g } _ { n _ { i , j } } ^ { \mathrm { N } } ( M ^ { n _ { i , j } \times N } )$ at all stations, i.e., $M _ { h } ^ { ( \delta + 1 ) ^ { 2 } \times N }$ .

Output: $\mathfrak { b } _ { i , \delta } ^ { h } ( k )$ at all station $b _ { i , \delta } .$

$\mathrm { f o r } \ k = 1 , 2 , \ldots , N , N + 1 , \ldots , N + \delta ( n ) - 3$ do

$$
k \rightarrow k ^ {\prime};
$$

if $k > N$ then ;

else for do

for do

for $r = 1 , \ldots , k$ do

All $b _ { i , j } \in \mathcal { H } _ { h , v }$ are permitted to transmit; if it holds that $1 \leq j \leq \bar { \delta } - 1 ,$ , and

1. $b _ { i , j } , j \geq 1 ,$ , has already received $\mathfrak { b } _ { i , j - 1 } ^ { h } ( r )$ from $b _ { i , j - 1 } ,$ and

2. $b _ { i , j + 1 }$ has not received $\mathfrak { b } _ { i , j } ^ { h } ( r )$ from $b _ { i , j } ,$ then $b _ { i , j }$ sends $\mathsf { b } _ { i , j } ^ { h } ( r )$ to $b _ { i , j + 1 } ;$ else $\mathbf { i } \mathbf { f } \ j = 0 .$ , and $b _ { i , 1 }$ has not received $\bar { \mathsf { b } } _ { i , 0 } ^ { h } ( r )$ , i.e., ${ \bf g } _ { n _ { i , 0 } } ( M ^ { n _ { i , 0 } \times N } ( \cdot , r ) )$ ） from $b _ { i , 0 } ,$ ,then $b _ { i , 0 }$ sends $\mathfrak { b } _ { i , 0 } ^ { h } ( r )$ to $b _ { i , 1 }$ .

Kk

# 3.1.3 Aggregation Capacity Analysis

Aggregation capacity depends on the type of functions of interest. We propose a general method in the analysis of aggregation throughput, although we mainly focus on the divisible-perfectly-compressible functions (Section 2.1.3). Due to the hierarchical structure of our scheme, we carry out the analysis phase by phase.

Local Aggregation Phase: In this phase, since it is guaranteed that each link is scheduled at least once out of time slots, Lemma 4 intuitively holds.

Lemma 4. In the local aggregation phase, if each scheduled link can achieve the rate of $R _ { 1 } ( n ) \ b i t s / s$ , then each link can sustain an average rate of $\begin{array} { r } { \dot { \Lambda } _ { 1 } ( n ) = \frac { R _ { 1 } ( n ) } { 3 2 \log n } } \end{array}$ 32logn bits/s. Thus, it takes at most

$$
T _ {1} (n) = \frac {N \cdot \log \mathfrak {m}}{\Lambda_ {1} (n)} = \frac {3 2 N \cdot \log \mathfrak {m} \cdot \log n}{R _ {1} (n)} \tag {5}
$$

seconds to finish the aggregation of rounds of measurements from sensors, i.e., a processed unit, at $( \delta + \mathsf { 1 } ) ^ { 2 }$ stations.

During the local aggregation phase, when block coding [4] is not adopted, since all data to be transmitted are the original measurements instead of the aggregated data, the throughput in this phase is independent of the type of aggregation functions. Next, we commence deriving the rate $\bar { R } _ { 1 } ( n )$ .

Lemma 5. During the local aggregation phase, every scheduled link can achieve the rate of order

$$
R _ {1} (n) = \Omega ((\log n) ^ {- \frac {\alpha}{2}}). \tag {6}
$$

Proof. Consider a given active cell, say $C _ { i , j } ,$ in a time slot under the 4-TDMA scheme. Please see illustration in Fig. 4(b). First, we find an upper bound for the interference at the receiver (station). We notice that the transmitters in the eight closest cells are located at Euclidean distance at least $\operatorname { I } = 2 { \sqrt { \log n } }$ from the receiver (station) in $C _ { i , j }$ . The transmitters in the 16 next closest cells are at Euclidean distance at least l, and so on. By extending the sum of the interferences to the whole plane, this is bounded as follows:

$$
I _ {1} (n) \leq \sum_ {k = 1} ^ {\infty} P \cdot \frac {8 k}{((2 k - 1) \cdot 1) ^ {\alpha}} \leq \frac {P}{2 ^ {\alpha - 3}} \cdot (\log n) ^ {- \frac {\alpha}{2}} \cdot \sum_ {k = 1} ^ {\infty} \frac {k}{(2 k - 1) ^ {\alpha}}.
$$

From $\begin{array} { r } { \alpha > 2 , \sum _ { k = 1 } ^ { \infty } \frac { k } { ( 2 k - 1 ) ^ { \mathrm { o } } } } \end{array}$ converges to a constant. Then, $I _ { 1 } ( n ) = O ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

Next, we find a lower bound on the strength of signal received from the transmitter. Since all links are limited within the same cells, the link length is at most ${ \sqrt { 2 } } \cdot 1 .$ . Thus, the signal at the receiver can be bounded by

$$
S _ {1} (n) \geq P \cdot (\sqrt {2} \cdot 1) ^ {- \alpha} = P \cdot 2 ^ {- \frac {3}{2} \alpha} \cdot (\log n) ^ {- \frac {\alpha}{2}}.
$$

Hence, $S _ { 1 } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$

Finally, combining the fact that $I _ { 1 } ( n ) = O ( ( \log n ) ^ { - { \frac { \alpha } { 2 } } } )$ and $S _ { 1 } ( \dot { n } ) = \Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ , we obtain a lower bound on the rate of scheduled link as

$$
R _ {1} (n) = B \log \left(1 + \frac {S _ {1} (n)}{N _ {0} + I _ {1} (n)}\right) = \Omega \left(\left(\log n\right) ^ {- \frac {\alpha}{2}}\right),
$$

which completes the proof.

Hence, according to Lemma 4 and Lemma 5, we have the following result,

Lemma 6. When the technique of block coding is not used, the time cost of the local aggregation for rounds of measurements is of order

$$
T _ {1} (n) = O (N \cdot (\log n) ^ {1 + \frac {\alpha}{2}}). \tag {7}
$$

Backbone Aggregation Phase: First, we consider the horizontal backbone phase.

Lemma 7. In the horizontal backbone phase, if each scheduled link can achieve the rate of $R _ { 2 } ^ { h } ( n )$ bits/s, then all horizontal backbones can sustain a rate of . $\begin{array} { r } { \Lambda _ { 2 } ^ { \tilde { h _ { 2 } } } ( n ) = R _ { 2 } ^ { h } ( n ) \cdot \frac { N } { 9 ( N + \delta ( n ) - 3 ) } . } \end{array}$

Proof. According to Algorithm 1, each horizontal backbone can be scheduled in order at least times out of $3 \times 3 \times ( N + \delta ( n ) - 3 )$ time slots. Thus, the lemma holds. ◽

Now, we start to derive the link rate $R _ { 2 } ^ { h } ( n )$ .

Lemma 8. During the horizontal backbone phase, every scheduled link can achieve the rate of order

$$
R _ {2} ^ {h} (n) = \Omega ((\log n) ^ {- \frac {\alpha}{2}}). \tag {8}
$$

Proof. This lemma can be proven in a similar procedure to that of Lemma 5. ◽

Lemma 9. To finish the horizontal backbone aggregation for rounds of measurements, it takes at most

$$
T _ {2} ^ {h} (n) = 9 \cdot \zeta_ {m a x} ^ {h} \cdot (\log n) ^ {\frac {\alpha}{2}} \cdot (N + \delta (n) - 3) \tag {9}
$$

seconds, where

$$
\zeta_ {m a x} ^ {h} = \max \{\zeta_ {i, j} ^ {h} | 0 \leq i \leq \delta - 1; 0 \leq j \leq \delta - 1 \},
$$

with $\zeta _ { i , j } ^ { h } = \log | \mathcal { G } _ { | D _ { i , j } ^ { h } | } | ,$ , and $\mathcal { G } _ { \vert D _ { i , j } ^ { h } \vert }$ is the range of $\mathbf { g } _ { \vert D _ { i , j } ^ { h } \vert }$

Proof. In this phase, the aggregation function value of the th round of data at station $b _ { i , j }$ is

$$
\mathfrak {b} _ {i, j} ^ {h} (k) := \mathbf {g} _ {| D _ {i, j} ^ {h} |} (M _ {h} ^ {| D _ {i, j} ^ {h} | \times N} (\cdot , k)).
$$

Since the technique of block coding is not adopted here, the load of station ${ \bar { b } } _ { i , j } ,$ denoted by $\Gamma _ { i , j } ^ { \breve { h } } ,$ i s

$$
\Gamma_ {i, j} ^ {h} = \sum_ {k = 1} ^ {N} \log | \mathcal {G} _ {| D _ {i, j} ^ {h} |} | = N \cdot \zeta_ {i, j} ^ {h}.
$$

Hence, in the horizontal backbone phase, the time cost of the aggregation for rounds of measurements is at most

$$
T _ {2} ^ {h} (n) = \frac {N \cdot \zeta_ {m a x} ^ {h}}{\Lambda_ {2} ^ {h} (n)} = 9 \zeta_ {m a x} ^ {h} \cdot (\log n) ^ {\frac {\alpha}{2}} \cdot (N + \delta (n) - 3),
$$

which completes the proof.

Next, we analyze the vertical backbone phase in a similar method to the horizontal one. For concision, we omit some similar proofs.

Lemma 10. In vertical backbone aggregation phase, the rate of each scheduled link is of order $R _ { 2 } ^ { v } ( n ) \stackrel { \smile \to } { = } \bar { \Omega ( } ( \log \dot { n } ) ^ { - \frac { \alpha } { 2 } } )$ , and the vertical backbone can sustain a rate of order

$$
\Lambda_ {2} ^ {v} (n) = \Omega \bigg ((\log n) ^ {- \frac {\alpha}{2}} \cdot \frac {N}{3 (N + \delta (n) - 3)} \bigg).
$$

Proof. In this phase, a 3-TDMA scheme is adopted. By using the similar approach to Lemma 5 and Lemma 8, we can

prove that $R _ { 2 } ^ { v } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . In Algorithm 2, the vertical backbone can be scheduled at least times out of $3 \times ( N + \delta ( n ) - 3 )$ time slots, which proves the lemma. ◽

Lemma 11. To finish the vertical backbone aggregation for rounds of measurements, it takes at most

$$
T _ {2} ^ {v} (n) = 3 \cdot \zeta_ {m a x} ^ {v} \cdot (\log n) ^ {\frac {\alpha}{2}} \cdot (N + \delta (n) - 3) \tag {10}
$$

seconds, where

$$
\zeta_ {m a x} ^ {v} = \max \{\zeta_ {i, \delta} ^ {v} | 0 \leq i \leq \delta - 1 \},
$$

with $\zeta _ { i , \delta } ^ { v } = \log | G _ { | D _ { i , \delta } ^ { v } | } | .$ , and $G _ { | D _ { i , \delta } ^ { v } | }$ is the range of $\mathbf { g } _ { | D _ { i , \delta } ^ { v } | }$ .

Proof. In this phase, the aggregation function value of the th round of data at station $b _ { i , \delta }$ is

$$
\mathfrak {b} _ {i, \delta} ^ {v} (k) := \mathbf {g} _ {| D _ {i, \delta} ^ {v} |} (M _ {v} ^ {| D _ {i, \delta} ^ {v} | \times N} (\cdot , k)).
$$

Since block coding is not used here, the load of station $b _ { i , \delta } ,$ denoted by $\Gamma _ { i , \delta } ^ { v } ,$ , is $\Gamma _ { i , \delta } ^ { v } = N \cdot \zeta _ { i , \delta } ^ { v } .$ Hence, to finish the vertical backbone aggregation for rounds of measurements, it takes

$$
T _ {2} ^ {v} (n) = \frac {N \cdot \zeta_ {m a x} ^ {v}}{\Lambda_ {2} ^ {v} (n)} = 3 \zeta_ {m a x} ^ {v} \cdot (\log n) ^ {\frac {\alpha}{2}} \cdot (N + \delta (n) - 3),
$$

which completes the proof.

# Algorithm 2. Vertical Backbone Aggregation

Input: $\mathfrak { b } _ { i , \delta } ^ { h } ( k )$ at all station $b _ { i , \delta } .$

Output: $\mathbf { g } _ { n } ^ { \mathrm { N } } ( M ^ { n \times N } )$ at the sink node $s _ { 0 } .$

for $k = 1 , 2 , \ldots , N , N + 1 , \ldots , N + \delta ( n ) - 3$ do

$$
k \rightarrow k ^ {\prime};
$$

if > then $N \to k ;$

else for $h = 0 , 1 , 2$ do

for do

All $b _ { i , \delta } \in \mathcal { V } _ { h , \delta }$ are permitted to transmit;

if it holds that $1 \leq i \leq \delta - 1$ , and

(1) $b _ { i , \delta } , \ i \geq 1 ,$ , has already received $\mathfrak { b } _ { i - 1 , \delta } ^ { v } ( r )$ from $b _ { i - 1 , \delta } ,$ and

(2) $b _ { i + 1 , \delta }$ has not received $\mathrm { b } _ { i , \delta } ^ { v } ( r )$ from $b _ { i , \delta } ,$

then $b _ { i , \delta }$ sends $\mathrm { b } _ { i , \delta } ^ { v } ( r )$ to $b _ { i + 1 , \delta } ;$

else if $i = 0 ,$ , and $b _ { 1 , \delta }$ has not received

$\mathsf { b } _ { 0 , \delta } ^ { v } ( r ) ,$ , i.e., $\mathsf { b } _ { 0 , \delta } ^ { h } ( r ) ,$ from $b _ { 0 , \delta } ,$

then $b _ { 0 , \delta }$ sends $\mathfrak { b } _ { 0 , \delta } ^ { v } ( r )$ to $b _ { 1 , \delta } .$

$$
k ^ {\prime} \rightarrow k
$$

According to Definition 1, we obtain Theorem 1.

Theorem 1. The aggregation throughput under the scheme $\mathcal { A } _ { N , n }$ with $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) } \end{array}$ is of order

$$
\Lambda (n) = \Omega \left(\frac {(\log n) ^ {- \frac {\alpha}{2}}}{\log n + \zeta_ {m a x} ^ {h} + \zeta_ {m a x} ^ {v}}\right), \tag {11}
$$

where $\zeta _ { m a x } ^ { h }$ and $\zeta _ { m a x } ^ { v }$ are defined in Lemma 9 and Lemma 11, respectively.

Proof. First, we consider the total time cost, say $T ( A _ { N , n } ) ,$ , during which the aggregation functions of rounds of measurements from sensors are computed at the sink node. It holds that $T ( A _ { N , n } ) = T _ { 1 } ( n ) + T _ { 2 } ^ { \hat { h } } ( n ) + T _ { 2 } ^ { v } ( n )$ , and the aggregation throughput under the scheme $\mathcal { A } _ { N , n }$ is of order

$$
\Lambda (n) = \frac {N \log \mathfrak {m}}{T _ {1} (n) + T _ {2} ^ {h} (n) + T _ {2} ^ {v} (n)}. \tag {12}
$$

Based on Lemma 9 and Lemma 11, for $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) . } \end{array}$ $\mathrm { i . e . , } N = \Omega ( \delta ( n ) )$ , it holds that

$$
T _ {2} ^ {h} (n) + T _ {2} ^ {v} (n) = O ((\log n) ^ {\frac {\alpha}{2}} \cdot N \cdot (\zeta_ {m a x} ^ {h} + \zeta_ {m a x} ^ {v})).
$$

Combining with Lemma $^ { 6 , }$ we can prove this theorem. ◽ From the analysis above, $T _ { 2 } ^ { h } ( n )$ and $\bar { T } _ { 2 } ^ { v } ( n )$ depend on the types of aggregation functions indeed. Consequently, we instantiate the general result in Theorem 1 to a special case, i.e., the case of divisible perfectly compressible functions.

# 3.2 Aggregation Throughput for Divisible-Perfectly-Compressible Functions

From the characteristic of divisible-perfectly-compressible aggregation functions (DPC-AFs, Lemma 1), by Theorem 1, we have the following result,

Theorem 2. For ${ \cal D } { \cal P } { \cal C } { - } A { \cal F } s ,$ the achievable aggregation throughput under the scheme $\mathcal { A } _ { N , n }$ with $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) } \end{array}$ is $\Lambda ( n ) =$ $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } )$ .

Proof. By Lemma 1, for DPC-AFs,

$$
\zeta_ {m a x} ^ {h} \leq \max \{\log | \mathcal {G} _ {| D _ {i, j} ^ {h} |} | \} = \Theta (\log \mathfrak {m}).
$$

Similarly, $\zeta _ { m a x } ^ { v } = O ( \log \mathfrak { m } )$ . Recall that ${ \mathfrak { m } } = \Theta ( 1 )$ , the theorem can thus be proven by using Theorem 1. ◽

# 3.3 Aggregation Scheme for Type-Threshold DPC-AFs

Sensing measurements are periodically generated, so the function of interest is required to be computed repeatedly. Hence, the technique, called block coding [4], is permitted. The technique of block coding combines several consecutive function computations, and can significantly improve the throughput for type-threshold functions [4] in the collocated network whose interference graph is a complete graph. For a given round of measurements, denoted by a -vector $M ^ { n } \in { \mathbf { \mathcal { M } } } ^ { n }$ , the max function, the min function and the range function $M _ { i } - \operatorname* { m i n } _ { i } M _ { i } )$ of $M ^ { n } .$ , the th largest value of $M ^ { n }$ , the mean of the largest values of $M ^ { n }$ , and the indicator function $I \{ M _ { i } = k ,$ for some $i \}$ are all typethreshold functions. We first refer to a result of [4] (Part of Theorem 4 in [4]).

Lemma 12. ([4]). Under the protocol model, the aggregation capacity for type-threshold functions in a collocated network of vertices is of order .

Under our scheme $\mathcal { A } _ { N , n } ,$ in each cell of the scheme lattice $^ { - 1 \prime }$ the communication graph can be regarded as a collocated network of vertices, because any two links in a cell can not be scheduled simultaneously during the local aggregation phase. Then, it is possible to improve the throughput by introducing the block coding into the scheme $\mathcal { A } _ { N , n }$ . The main question to be solved is how to extend the result of Lemma 12 to that under the generalized physical model. Analyze the proof of Lemma 12: Let $N = { \hat { \Theta } } ( { \dot { n } } )$ , and under the assumption that each successful transmission can achieve a constant rate, prove that it takes time slots to finish the aggregation for rounds of measurements. Thus, since during the local aggregation phase of $\mathcal { A } _ { N , n } ,$ each successful transmission can sustain a rate of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ instead of a constant order, we have the following result,

Lemma 13. Under generalized physical model, by block coding with $N _ { b } = \Theta ( \log n )$ , for type-threshold $D P C { - } A \dot { F } s ,$ , the time cost of the local aggregation $f o r \quad N = \Omega ( \log n )$ rounds of measurements is of order $T _ { 1 } ^ { b c } \bar { ( n ) } = O ( N \cdot \bar { ( \log n ) ^ { \frac { \alpha } { 2 } } }$ · log log n).

Proof. For the communication graph in each cell, we implement the local aggregation by using block coding with length $N _ { b } = \Theta ( \log n )$ . Similar to Lemma 12, the time cost of aggregating $N _ { b }$ rounds of measurements is of $O ( ( \log n ) ^ { \frac { \alpha } { 2 } } \cdot N _ { b }$ . By partitioning rounds of measurements into blocks of length $N _ { b } ,$ , we prove the lemma. ◽

Lemma 12 holds when $N = \Omega ( \log n )$ which does not contradict with the condition that $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) } \end{array}$ in Theorem 1 and √logn Theorem 2. Then, we can modify the scheme $\mathcal { A } _ { N , n }$ by introducing the block coding in the local aggregation phase. Denote this scheme by $\mathcal { A } _ { N , n } ^ { b c } .$ . Finally, we propose,

Theorem 3. For type-threshold DPC-AFs, theaggregation throughput under the scheme $\mathcal { A } _ { N , n } ^ { b c }$ ievablewith $\begin{array} { r } { N = \Omega ( \frac { \sqrt { n } } { \sqrt { \log n } } ) } \end{array}$ is of order

$$
\Lambda (n) = \Omega \left(\left(\log n\right) ^ {- \frac {\alpha}{2}} \cdot \frac {1}{\log \log n}\right). \tag {13}
$$

Proof. By using block coding, $T ( A _ { N , n } ^ { b c } ) = T _ { 1 } ^ { b c } ( n ) + T _ { 2 } ^ { h } ( n ) +$ $T _ { 2 } ^ { v } ( n ) \bar { = } O ( N \cdot ( \log n ) ^ { \frac { \alpha } { 2 } } \cdot \log \log n )$ . According to Definition 1, we can complete the proof. ◽

# 4 UPPER BOUNDS ON AGGREGATION CAPACITY

In this section, we compute the upper bounds on aggregation capacities for type-sensitive divisible perfectly compressible aggregation functions (type-sensitive DPC-AFs) and type-threshold divisible perfectly compressible aggregation functions (typethreshold DPC-AFs) over RE-WSN.

# 4.1 Upper Bounds for Type-Sensitive DPC-AFs

Theorem 4. The aggregation capacity for type-sensitive DPC-AFs over RE-WSN is of order $O ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } )$ .

Proof. By Equation (2), in any aggregation tree, there exists, $w . h . p . .$ , a link of length $\Omega ( { \sqrt { \log n } } )$ , say . The capacity of such a link is upper bounded by

$$
B \log \left(1 + \frac {\left(\kappa_ {1} \sqrt {\log n}\right) ^ {- \alpha}}{N _ {0}}\right) = O \left(\left(\log n\right) ^ {- \frac {\alpha}{2}}\right),
$$

where $\kappa _ { 1 } > 0$ is a constant. According to the characteristics of type-sensitive DPC-AFs, it takes at least $\kappa _ { 2 } \cdot n N \cdot ( \log n ) ^ { \frac { \alpha } { 2 } }$ transmissions to finish the aggregation of rounds of measurements from every sensor, where $\kappa _ { 2 } > 0$ is a constant that has no impact on the final results in order sense. By a similar procedure to Lemma 3 (based on VC theorem [25]), we get that each cell in the network lattice $\mathbb { L } ( \sqrt { n } , \frac { 2 } { \kappa _ { } } \sqrt { \log { n } } , n )$ must make at least $\kappa _ { 3 }$ log n transmissions, where $\begin{array} { r } { \frac { 1 } { 2 } < \kappa _ { 3 } < 8 . } \end{array}$ . Since the arena-bounds [26] for the generalized physical model is of order , [27], the total aggregation rate of those $\kappa _ { 3 }$ log n transmissions can be upper bounded of order $O ( \mu ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ when the data from the senders of these transmissions are aggregated into $\mu$ receivers, where $\mu = O ( \log n )$ . For any aggregation tree, consider the cells in $\mathbb { L } ( \sqrt { n } , \frac { 2 } { \kappa _ { \mathrm { o } } } \sqrt { \log n } , n )$ , from the farthest (in hopdistance) cell to that contains the sink node, there must be a scenario where $\mu = \Theta ( 1 )$ , because all data will converge to the sink node. In this case, transmissions share the total link rate of $O ( ( \log n ) ^ { - { \frac { \alpha } { 2 } } } )$ , and it takes $\Omega ( n N ( \log n ) ^ { \frac { \alpha } { 2 } + 1 } )$ ） slots to finish the aggregation. Thus, the aggregation capacity is bounded b y . ◽ $\frac { n N } { \Omega ( n N ( \log n ) ^ { \frac { \alpha } { 2 } + 1 } ) } = O ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } )$

# 4.2 Upper Bounds for Type-Threshold DPC-AFs

Theorem 5. The aggregation capacity for type-threshold DPC-AFs over RE-WSN is of order $\begin{array} { r } { O ( \frac { ( \log \breve { n } ) ^ { - \alpha / 2 } } { \log \log n } ) } \end{array}$ (logn)-a/2 (logn)gn).

Proof. For type-threshold DPC-AFs, by a similar procedure to Theorem 4 and according to Theorem 4 of [4], each cell in the network lattice L $. ( { \sqrt { n } } , { \kappa _ { 4 } } { \sqrt { \log n } } , n )$ must make at least $\kappa _ { 5 } N$ transmissions, when each sensor produces rounds of measurements, where $\kappa _ { 4 } , \kappa _ { 5 } > 0$ are some constants. By a similar argument to Theorem $^ { 4 , }$ there must be a level of aggregation that takes at least , which completes $\frac { \Omega ( N \log \log n ) } { O ( ( \log n ) ^ { - \alpha / 2 } ) } = \Omega ( N$ $n \cdot ( \log n ) ^ { \alpha / 2 } )$ the proof. ◽

Combining the lower bounds (Theorem 2 and Theorem 3) with upper bounds (Theorem 4 and Theorem 5), we get that

Theorem 6. The aggregation capacities for type-sensitive DPC-AFs and type-threshold DPC-AFs over RE-WSN are of order $\Theta ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } )$ and $\Theta ( \frac { ( \log n ) ^ { - \alpha / 2 } } { \log \log n } )$ (logn)-α/2 , respectively.

# 5 IMPROVING CAPACITY BY MULTIPLE SINKS

According to Theorem 1, Theorem 2 and Theorem 3, we learn that even by using block coding, the bottleneck still lies in the local aggregation phase. More specifically, the size of each collocated network, i.e., the number of nodes in each cell, is still too large. Consequently, we resort to reducing the size of the collocated network without diminishing the link rate. As a solution, we exploit a technique called parallel transmission scheduling [9].

![](images/64866d7137af63cc9eaf1e49fcc8e2bfbbd28b6356a4bf31ff35617d87202eb5.jpg)



Fig. 5. Parallel aggregation backbones. Black cycles denote aggregation stations. Black squares denote $\Theta ( \log n )$ sink nodes that are deployed randomly in a small region (shaded) of area . In each row (or column backbo $\bar { \delta } - 1$ and column ), there are $\frac { \log n } { 2 }$ log n horizontal (or vertical)

# 5.1 Parallel Aggregation Scheme $\mathcal { A } _ { N , n } ^ { p }$

According to Lemma 3, in any cell of the network lattice $\mathbb { L } _ { 1 } ,$ , the number of nodes is $w . h . p .$ . within $( { \scriptstyle { \frac { 1 } { 2 } } } \log n , 8 \log n )$ . Hence, intuitively, when we randomly choose stations from each cell in $\mathbb { L } _ { 1 } ,$ , there are backbones in each row (or column). However, the rate of each backbone does not exceed that of the backbone in the scheme $\mathcal { A } _ { N , n }$ because of the nondecreasing interference to each link. Thereby, we attempt to simultaneously schedule multiple backbones in each row (or column), without impairing the rate of every backbone, that is, with sustaining the rate of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . We denote the new scheme with parallel scheduling by $\mathcal { A } _ { N , n } ^ { p } .$ . Like $\mathcal { A } _ { N , n } ,$ the scheme $\mathcal { A } _ { N , n } ^ { p }$ also consists of two phases: local aggregation phase and backbone aggregation phase; and the backbone phase is further divided into two subphases: horizontal backbone phase and vertical backbone phase.

Backbone Aggregation Phase: Denote the stations in the cell $C _ { i , j }$ of L by $b _ { i , j } ( \iota ) , 1 \leq \iota \leq \frac { \log n } { 2 }$ . Then, we construct the horizontal backbones in the following method (Please see illustration in Fig. 5): In each row $i , 0 \leq i \leq \delta ,$

when is even, for $\ : 0 \leq k \leq \lfloor \frac { \delta } { 2 } \rfloor - 1 \ :$ and $\begin{array} { r } { 1 \leq \iota \leq \frac { \log n } { 2 } } \end{array}$ , connect the station $b _ { i , 2 k } ( \iota )$ to $b _ { i , 2 k + 2 } ( \iota ) .$ ;   
when is odd, for $\begin{array} { r } { 0 \leq k \leq \lfloor \frac { \delta } { 2 } \rfloor - 1 } \end{array}$ and $\begin{array} { r } { 1 \leq \iota \leq \frac { \log n } { 2 } } \end{array}$ , connect the station $b _ { i , 2 k + 1 } ( \iota )$ to $\bar { b _ { i , 2 k + 3 } } ( \iota )$ .

Similarly, we can build the vertical backbones in column $\delta - 1$ and column . Note that not all cells contain the station.

For the convenience of description, we assume that is even without loss of generality. During the horizontal backbone phase, the data are aggregated into the stations on the vertical backbones in two columns; during the vertical backbone phase, the data are aggregated to the stations in the cells $C _ { \delta - 1 , \delta - 1 }$ and $C _ { \delta , \delta }$ . When is odd, the data are finally aggregated into the stations in the cells $C _ { \delta - 1 , \delta }$ and $C _ { \delta , \delta - 1 } .$ .

Now, the key question is how to schedule the backbones to improve the total rate. To schedule the horizontal backbones, we adopt a 4-TDMA scheme, denoted by $H _ { N , n } ^ { p }$ . Under the scheme $H _ { N , n } ^ { p } ,$ as illustrated in Fig. 6(a), a scheduling unit (SU) consists of $2 \times 4$ cells. Since there are only four cells that contain stations and need to be scheduled in each SU, we can complete the scheduling of each SU once in a period of four time slots. Similarly, we can use a 4-TDMA scheme, denoted by bac $V _ { N , n } ^ { p }$ and described in Fig. 6(b),nes. we iterate that for both heduand vertical the key $H _ { N , n } ^ { p }$ $V _ { N , n } ^ { p } ,$ technique to improve the throughput is to permit stations in a scheduled cell to transmit simultaneously. Next, we prove the improvement in the total rate of backbones.

![](images/241f70d21f9b880d716fa6a8df0c437d801cd7b12a3e81144a2563633b651fda.jpg)



(a) horizontal scheduling

![](images/a32d983bc338c7bd2b7bb9d73d476a70182af1e659346216562f3a41bd3eb213.jpg)



(b) vertical scheduling   
Fig. 6. Parallel backbone scheduling. The $\frac { \log n } { 2 }$ 2 stations in each scheduled cell can transmit simultaneously.

Lemma 14. Under the scheduling scheme $\mathcal { H } _ { N , n } ^ { p } \left( o r \mathcal { V } _ { N , n } ^ { p } \right) ,$ , every horizontal (or vertical) backbone can still sustain a rate of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

Proof. Let us consider any scheduled link of horizontal backbones. The interferences at the receiver of the link are produced by those $\textstyle { \frac { \log n } { 2 } } - 1$ stations in the cell containing the intended transmitter and ones in other scheduled cells. Since the length of the link is at least of ${ \mathrm { I } } = 2 { \sqrt { \log n } } ,$ , the sum of interferences at the receiver can be bounded by $\begin{array} { r } { I _ { h } ^ { p } ( n ) \leq P \cdot ( \frac { \log n } { 2 } - 1 ) \cdot \ell ( 2 \sqrt { \log n } ) + \sum _ { i = 1 } ^ { n } 8 i P \cdot } \end{array}$ $\begin{array} { r } { \frac { \log n } { 2 } \cdot \ell \big ( \big ( 4 i - 3 \big ) \cdot 2 \sqrt { \log n } \big ) \ \stackrel { \sim } { \ } \frac { P } { 2 ^ { \alpha + 1 } } \cdot ( \log n ) ^ { 1 - \frac { \alpha } { 2 } } \cdot ( 1 + \operatorname* { l i m } _ { n \to \infty } } \end{array}$ 2 . The latest limitation converges when $\bar { \sum _ { i = 1 } ^ { n } \frac { 8 i } { ( 4 i - 3 ) ^ { \alpha } } } )$ $\alpha > 2 .$ Since the distance of every hop is at most ${ \sqrt { 1 0 } } \cdot 1 ,$ , we have the signal at the receiver can be bounded as $S _ { h } ^ { p } ( n ) \geq 4 0 ^ { - \alpha } P \cdot ( \log n ) ^ { - { \frac { \alpha } { 2 } } } ,$ . Then, $\frac { S _ { h } ^ { p } ( n ) } { N _ { 0 } + I _ { h } ^ { p } ( n ) } = O ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ since $\log ( 1 + x ) \sim x$ as $x = o ( 1 )$ , the scheduled link can achieve the rate of $R _ { h } ^ { p } ( n ) = \Theta ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . Since all horizontal backbones are scheduled once in four time slots, every horizontal backbone can sustain a rate of $\begin{array} { r } { \frac { R _ { h } ^ { p } ( n ) } { 4 } . } \end{array}$ , which proves the result on horizontal backbones. In a similar way, we get the result on vertical backbones. ◽

Local Aggregation Phase: Now, we discuss how to efficiently collect the measurements into those stations. We still set the scheduling unit as a cluster of $2 \times 4$ cells, like in Fig. 6 (a). Denote a scheduling unit by $U _ { h , v }$ that consists of the cells $C _ { 2 h , 4 v } , \quad C _ { 2 h , 4 v + 1 } , \quad C _ { 2 h , 4 v + 2 } , \quad C _ { 2 h , 4 v + 3 } , \quad C _ { 2 h + 1 , 4 v } , \quad C _ { 2 h + 1 , 4 v + 1 } ,$ $C _ { 2 h + 1 , 4 v + 2 } ,$ and $C _ { 2 h + 1 , 4 v + 3 } , \mathrm { i f }$ any. The parallel routing and scheduling scheme can be described as follows. To simplify the description, let $t _ { 0 } - t _ { 1 } \colon C _ { i , j } { \Rightarrow } C _ { k , l }$ represent that all measurements from nodes in $C _ { i , j }$ are evenly aggregated into the $\frac { \log n } { 2 }$ stations in $C _ { k , l }$ during time slots $t _ { 0 } - t _ { 1 }$ . It takes 128 time slots to schedule all links in $U _ { h , v }$ :

$$
\begin{array}{l} 1 \quad - 1 6: C _ {2 h, 4 v} \quad \Rightarrow C _ {2 h, 4 v + 2} \\ 1 7 \quad - 3 2: C _ {2 h, 4 v + 1} \quad \Rightarrow C _ {2 h + 1, 4 v + 3} \\ 3 3 \quad - 4 8: C _ {2 h, 4 v + 2} \quad \Rightarrow C _ {2 h, 4 v} \\ 4 9 \quad - 6 4: C _ {2 h, 4 v + 3} \quad \Rightarrow C _ {2 h + 1, 4 v + 1} \\ 6 5 \quad - \quad 8 0 \quad : \quad C _ {2 h + 1, 4 v} \quad \Rightarrow \quad C _ {2 h, 4 v + 2} \\ 8 1 \quad - 9 6: C _ {2 h + 1, 4 v + 1} \Rightarrow C _ {2 h + 1, 4 v + 3} \\ 9 7 \quad - 1 1 2: C _ {2 h + 1, 4 v + 2} \Rightarrow C _ {2 h, 4 v} \\ 1 1 3 - 1 2 8: C _ {2 h + 1, 4 v + 3} \Rightarrow C _ {2 h + 1, 4 v + 1} \\ \end{array}
$$

Under the above scheduling scheme, the hop-length of every link is of order $\Omega ( { \sqrt { \log n } } )$ . From the analysis in Lemma $^ { 1 4 , }$ we can schedule simultaneously $\frac { \log n } { 2 }$ links in each scheduled cell, ensuring that the rate of every link is of order $R _ { 1 } ^ { p } ( n ) = \Omega ( ( \log n ) ^ { - \alpha / 2 } )$ . On the other hand, it takes at most 16 time slots to schedule all links from one cell to the stations in other cell, because $\frac { \log n } { 2 }$ links can be simultaneously scheduled while there are at most nodes in each cell.

# 5.2 Throughput under Aggregation Scheme $\mathcal { A } _ { N , n } ^ { p }$

First, for the local aggregation phase, we have the following result,

Lemma 15. Under the parallel scheduling scheme, the time cost of the local aggregation for rounds of measurements is of order $T _ { 1 } ^ { p } ( n ) = \bar { O ( N \cdot ( \log n ) ^ { \frac { \alpha } { 2 } } ) }$ .

Proof. Since in the local phase, each link can be scheduled once out of 128 time slots, then the average rate of each link can sustain of order $\begin{array} { r } { \Lambda _ { 1 } ^ { p } ( n ) = \frac { R _ { 1 } ^ { p } ( n ) } { 1 2 8 } , ~ \mathrm { i . e . , } ~ \Lambda _ { 1 } ^ { p } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } ) } \end{array}$ . And, each sensor has a load of measurements to transmit into the corresponding station, thus, the total time cost is $\begin{array} { r } { \frac { N \log { \mathfrak { m } } } { \Lambda _ { 1 } ^ { p } ( n ) } = O ( N ^ { \bullet } \cdot ( \log { n } ) ^ { \frac { \alpha } { 2 } } ) } \end{array}$ , which completes the proof. ◽

Next, we consider the backbone phase. Under the scheme $\mathcal { A } _ { N , n } ^ { p } ,$ define the set of $b _ { i , j } ( \iota )$ and all its descendants as $D _ { i , j } ^ { p , h } ( \iota )$ for all $i , ~ j$ and ; and define the set of $b _ { i , j } ( \iota )$ and all its descendants as $D _ { i , j } ^ { p , v } ( \iota )$ for all , and $j = \delta - 1 , \delta$ . Since there are $\frac { \log n } { 2 }$ stations that contribute the burden-sharing of each cell, then it holds that

$$
| D _ {i, j} ^ {p, h} (\iota) | = \Theta (\frac {2}{\log n}) \cdot | D _ {i, j} ^ {h} |; | D _ {i, j} ^ {p, v} (\iota) | = \Theta (\frac {2}{\log n}) \cdot | D _ {i, \delta} ^ {v} |
$$

Then, in the horizontal phase and vertical phase, the load produced by th round of measurements on station $b _ { i , j } ( \iota )$ is

$$
\zeta_ {i, j} ^ {p, h} (\iota) = \log | \mathcal {G} _ {| D _ {i, j} ^ {p, h} |} | \text {   and   } \zeta_ {i, j} ^ {p, v} (\iota) = \log | \mathcal {G} _ {| D _ {i, j} ^ {p, v} |} |,
$$

respectively. Then, we further define

$$
\zeta_ {m a x} ^ {p, h} := \max _ {i, j, \iota} \zeta_ {i, j} ^ {p, h} (\iota), \zeta_ {m a x} ^ {p, v} := \max _ {i, j, \iota} \zeta_ {i, j} ^ {p, v} (\iota). \tag {14}
$$

Thus, in a similar procedure to the proofs of Lemma 9 and Lemma 11, we can obtain

Lemma 16. Under the parallel scheduling scheme, to finish the backbone aggregation for rounds of measurements, it takes at most

$$
T _ {2} ^ {p, h} (n) = O ((\zeta_ {m a x} ^ {p, h} + \zeta_ {m a x} ^ {p, v}) \cdot (\log n) ^ {\frac {\alpha}{2}} \cdot (N + \delta (n)))
$$

seconds, where $\zeta _ { m a x } ^ { p , h }$ and $\zeta _ { m a x } ^ { p , v }$ are defined in (14).

Combining Lemma 15 and Lemma 16, we get that,

Theorem 7. Under the parallel aggregation scheme $\mathcal { A } _ { N , n } ^ { p }$ with $N = \Omega ( \sqrt { n } / \sqrt { \log n } )$ , the measurements from all sensors can be aggregated into sink nodes in a small region of which the area is an infinitesimal proportion, i.e., $\frac { 4 \log n } { n }$ , of the whole deployment region, at a throughput of

$$
\Lambda (n) = \Omega \left(\frac {(\log n) ^ {- \frac {\alpha}{2}}}{1 + \zeta_ {m a x} ^ {p , h} + \zeta_ {m a x} ^ {p , v}}\right). \tag {15}
$$

For the $D P C { \mathrm { - } } A F s ,$ , such achievable throughput is of order $\Lambda ( n ) = \Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

# 5.3 Implications of Theorem 7

# 5.3.1 Elimination of Interference-Limitedness

According to Lemma 2, for any aggregation tree, there must be a link of length $\Omega ( { \sqrt { \log n } } )$ , which leads to the network throughput is limited to the rate of such a link, i.e., the order $O ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ due to coverage-limitedness (Section 2.3.1). From Theorem 7, this upper bound can be indeed achieved by choosing randomly sensors from a small region (relative to the whole deployment region) of area .

# 5.3.2 Gains of Multiple Sinks

It is straightforward that choosing multiple sinks can possibly improve the network throughput. While, some potential questions might be asked:

1. Why not we choose uniformly at random sensors from the whole network as sink nodes? The reason is two-fold: (1) Since each sink usually connects with a processing station (e.g., computer) via a reliable link (even a wired link), and it should be always guaranteed with a stable power supply, it is easy to understand that the smaller the region contained sink nodes is, the more convenient the network management is. (2) It cannot improve the order of throughput indeed when we choose uniformly $\Theta ( \log n )$ sink nodes. An intuitive (but not rigorous) explanation is as following: divide the network into subregions, choose one sensor from each subregion as a sink node that takes charge of data gathering in this subregion. By doing so, the throughput of each subregion is also of the same order as that of the whole region with a single sink node, because the area of the subregions (then, the number of sensors), $\textstyle \operatorname { i . e . , } \Theta ( { \frac { n } { \log n } } )$ , is still too large to ease the bottlenecks in the whole network.

2. Can we improve further the aggregation throughput by more sink nodes? It can definitely improve the network throughput when we choose uniformly a large enough number of sensors as sink nodes. An extreme case is that all sensors are chosen as sink nodes. Of course, it makes no sense. It can be straightforwardly inferred that the throughput under such parallel aggregation schemes can be increased by times when sinks are chosen from a subregion of area $\Theta ( k ( n )$ · log n), where $k ( n ) = \Omega ( 1 )$ and $\begin{array} { r } { k ( \bar { n } ) = { O } \left( \frac { n } { \log n } \right) } \end{array}$ . Finally, we conjecture that the throughput derived in Theorem 7 is indeed optimal if the number of sink nodes is limited to the number of . We leave the rigorous validation to future work.

# 5.4 Challenges in Practical Implementation

This work falls within the scope of scaling laws, i.e., scaling of the network performance in the limit when the network gets large, [4]. We aim to investigate the qualitative and fundamental properties of WSNs in terms of aggregation capacity, [4], [10], [28], [29]. The proposed schemes provide some architectural guidelines on how to design the practical aggregation schemes for WSNs that scale well. It should be emphasized that when implementing the specific schemes under the proposed architecture, we need to take into account some technique details, e.g., the tuning of many parameters and optimization of some pre-constants in the system throughput, [10], [29].

# 6 LITERATURE REVIEW

The issue of capacity scaling laws for wireless ad hoc networks [1] has been intensively studied under different models. The firstwork about aggregation capacity scalinglaws ofWSNwas done by Marco et al. [5]. They considered the capacity of random dense WSNs under the protocol model [1]. In [4], Giridhar and Kumar also focused on dense WSNs, and investigated the more general problem of computing and communicating symmetric functions of the sensor measurements. They showed that for type-sensitive functions and type-threshold functions, the aggregation capacities for random dense WSNs under the protocol model are of order $\textstyle \Theta ( { \frac { 1 } { \log n } } )$ and $\Theta ( \frac { 1 } { \log \log n } ) .$ , respectively. Ying et al. [30] studied the optimization problem of the total transmission energy for computing a symmetric function, subject to the constraint that the computation is w.h. $p _ { \cdot , \cdot }$ , correct. Moscibroda [8] derived the aggregation capacity scaling laws of divisible perfectly compressible functions for worst-case networks. They showed that under the protocol model and physical model [1], the capacity for worst-case networks is of order and $\Omega ( \frac { 1 } { ( \log n ) ^ { 2 } } )$ , respectively. Zheng et al. [31] proposed an Attribute-aware Data Aggregation mechanism using Dynamic Routing (ADADR) that can make packets with the same attribute convergent as much as possible and therefore improve the efficiency of data aggregation. Under the cooperative paradigm, Zheng and Barton [7] demonstrated that the upper bound of the capacity of data collecting for extended WSNs is of order $\Theta ( \bar { \log { n } / n } )$ and $\Theta ( 1 / n )$ when operating in fading environments with power path-loss exponents that satisfy $2 < \alpha < 4$ and $\alpha > 4 ,$ , respectively. The work considered the aggregation functions without no innetwork aggregation [32], e.g., data downloading problem [4]. It might be interesting to merge this technique into our scheme to improve the results under the cooperative paradigm.

Note that unlike all other works mentioned, including our work, the result in [7] is information-theoretic bounds instead of networking-theoretic bounds. (Section 2.1). In [33], Wang et al. studied the capacity, delay and their tradeoffs in -source converge-cast networks. They showed that the essential key controlling the capacity is the redundancy, with inverse relationship. In [29], [34], by introducing the visual MIMO techniques, Fu and Wang et al. designed two different cooperative schemes for static and mobile ad hoc wireless networks, respectively. Servetto [35] constructed a structured class of asymptotically optimal quantizers for the problem of rate/distortion with side information available only at the decoder. He showed that there exist quantizers whose performance comes arbitrarily close to Wyner¡¯s bound [36]. Guleryuz and Kozat [37] studied an important class of sensor networks where the ultimate goal is not necessary to collect each individual measurement but rather a potentially smaller set of statistics. They determined how the flow of information emanating from the sensors should be managed, yielding optimal routing algorithms and jointly optimized networks.

Some work focused on the data transmission in mobile WSNs where the sensors and/or sinks are mobile. In [38], Chen et al. proposed to use multihop forwarding to form a cluster around the expected position of a mobile sink, in order to guarantee packet delay and minimize energy consumption. Park et al. [39] designed a simple route maintaining algorithm to support the sink mobility of conventional routing protocols. The algorithm does not use the flooding method and does not require the information on the geometric location of sensor nodes. In [40], Gao et al. formulated the problem of jointly improving the amount of data collected and reducing the energy consumption as an integer linear programming problem, and proposed a corresponding data collection scheme based on optimizing the assignment of sensor nodes.

# 7 CONCLUSION

We emphasize that for random extended WSNs (RE-WSNs), the basic assumption of the protocol model and physical model [1] that any successful transmission can sustain a constant rate is over-optimistic and unpractical. We derive the first result on scaling laws of the aggregation capacity for RE-WSNs under generalized physical model. We show that, for general divisible perfectly compressible aggregation functions (DPC-AFs), the achievable aggregation throughput of RE-WSNs is of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } ) ;$ and for type-sensitive DPC-AFs and type-threshold DPC-AFs, aggregation capacities are of order $\Theta ( ( \log n ) ^ { - \frac { \alpha } { 2 } - 1 } )$ and $\Theta ( \frac { 1 } { \log \log n } \cdot ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ respectively. Furthermore, by introducing the parallel transmission scheduling, we prove that the achievable aggregation throughput for DPC-AFs is of order by choosing sink nodes in a small region.

There are some interesting directions left to study: (1) An interesting future work is to derive the aggregation capacity scaling laws for mobile WSNs consisting of mobile sensors or mobile sinks with energy limitations. (2) It is worth deriving the aggregations capacity of WSNs for more general aggregation functions. (3) It would be interesting to investigate how real-world wireless propagation, such as shadowing, path loss and multipath fading, affects the aggregation capacity of WSNs by introducing more realistic communication models.

# ACKNOWLEDGMENT

The authors would like to thank the anonymous reviewers for their constructive comments. The research of authors is partially supported in part by the National Natural Science Foundation of China (NSFC) under Grant 61202383, in part by the National Basic Research Program of China (973 Program) under Grant 2010CB328101, in part by the Shanghai Rising-Star Program under Grant 14QA1403700, in part by the Program for New Century Excellent Talents in University (NCET) under Grant NCET-12-0414, in part by the Natural Science Foundation of Shanghai under Grant 12ZR1451200, in part by the Integrated Project for Major Research Plan of the National Natural Science Foundation of China under Grant 91218301, and in part by the Research Fund for the Doctoral Program of Higher Education of China (RFDP) under Grant 20120072120075.

# REFERENCES

[1] P. Gupta and P. R. Kumar, “The capacity of wireless networks,” IEEE Trans. Inf. Theory, vol. 46, no. 2, pp. 388–404, 2000.

[2] A. Özgür, O. Lévêque, and D. Tse, “Hierarchical cooperation achieves optimal capacity scaling in ad hoc networks,” IEEE Trans. Inf. Theory, vol. 53, no. 10, pp. 3549–3572, 2007.   
[3] S. Li, Y. Liu, and X.-Y. Li, “Capacity of large scale wireless networks under Gaussian channel model,” in Proc. ACM Annu. Int. Conf. Mobile Comput. Netw. (MobiCom), 2008, pp. 140–151.   
[4] A. Giridhar and P. Kumar, “Computing and communicating functions over sensor networks,” IEEE J. Sel. Areas Commun., vol. 23, no. 4, pp. 755–764, 2005.   
[5] D. Marco, E. Duarte-Melo, M. Liu, and D. Neuhoff, “On the many-toone transport capacity of a dense wireless sensor network and the compressibility of its data,” in Proc. ACM Int. Conf. Inf. Process. Sens. Netw. (IPSN’03), 2003, pp. 1–16.   
[6] R. Barton and R. Zheng, “Cooperative time-reversal communication is order-optimal for data aggregation in wireless sensor networks,” in Proc. IEEE Int. Symp. Inf. Theory (ISIT’06), 2006, pp. 222–226.   
[7] R. Zheng and R. Barton, “Toward optimal data aggregation in random wireless sensor networks,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM’07), 2007, pp. 249–257.   
[8] T. Moscibroda, “The worst-case capacity of wireless sensor networks,” in Proc. ACM/IEEE Int. Conf. Inf. Process. Sens. Netw. (IPSN’07), 2007, pp. 1–10.   
[9] C. Wang, X.-Y. Li, and C. Jiang, “Scaling laws on multicast capacity of large scale wireless networks,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM’09), 2009, pp. 1863–1871.   
[10] C. Wang, C. Jiang, S. Tang, and X.-Y. Li, “Selectcast: Scalable data aggregation scheme in wireless sensor networks,” IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 10, pp. 1958–1969, 2012.   
[11] S. Shenker, S. Ratnasamy, B. Karp, R. Govindan, and D. Estrin, “Data-centric storage in sensornets,” ACM SIGCOMM Comput. Commun. Rev., vol. 33, no. 1, p. 142, 2003.   
[12] C. Chau, M. Chen, and S. Liew, “Capacity of large-scale CSMA wireless networks,” in Proc. ACM Annu. Int. Conf. Mobile Comput. Netw. (MobiCom), 2009, pp. 97–108.   
[13] M. Franceschetti, O. Dousse, D. Tse, and P. Thiran, “Closing the gap in the capacity of wireless networks via percolation theory,” IEEE Trans. Inf. Theory, vol. 53, no. 3, pp. 1009–1018, 2007.   
[14] R. Zheng, “Asymptotic bounds of information dissemination in power-constrained wireless networks,” IEEE Trans. Wireless Commun., vol. 7, no. 1, pp. 251–259, Jan. 2008.   
[15] O. Dousse and P. Thiran, “Connectivity vs capacity in dense ad hoc networks,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), 2004, pp. 476–486.   
[16] M. Penrose, “The longest edge of the random minimal spanning tree,” Ann. Appl. Probab., vol. 7, pp. 340–361, 1997.   
[17] P. Gupta and P. Kumar, “Critical power for asymptotic connectivity in wireless networks,” Stochastic Anal. Control Optim. Appl.: A Volume Honor Fleming, vol. 3, no. 20, pp. 547–566, 1998.   
[18] P. Santi and D. Blough, “The critical transmitting range for connectivity in sparse wireless ad hoc networks,” IEEE Trans. Mobile Comput., vol. 2, no. 1, pp. 25–39, 2003.   
[19] P. Santi, “The critical transmitting range for connectivity in mobile ad hoc networks,” IEEE Trans. Mobile Comput., vol. 4, no. 3, pp. 310–317, 2005.   
[20] X.-Y. Li, “Multicast capacity of wireless ad hoc networks,” IEEE/ ACM Trans. Netw., vol. 17, no. 3, pp. 950–961, 2009.   
[21] C. Wang, C. Jiang, X. Li, and Y. Liu, “Asymptotic throughput for large-scale wireless networks with general node density,” Wireless Netw., vol. 19, no. 5, pp. 713–725, 2013.   
[22] E. Duarte-Melo and M. Liu, “Data-gathering wireless sensor networks: organization and capacity,” Comput. Netw., vol. 43, no. 4, pp. 519–537, 2003.   
[23] H. Gamal, “On the scaling laws of dense wireless sensor networks: the data gathering channel,” IEEE Trans. Inf. Theory, vol. 51, no. 3, pp. 1229–1234, 2005.   
[24] B. Liu, P. Thiran, and D. Towsley, “Capacity of a wireless ad hoc network with infrastructure,” in Proc. ACM Int. Symp. Mobile Ad Hoc Netw. Comput. (Mobihoc), 2007, pp. 239–246.   
[25] V. Vapnik and A. Chervonenkis, “On the uniform convergence of relative frequencies of events to their probabilities,”Theory Probab. Its Appl., vol. 16, no. 2, pp. 264–280, 1971.   
[26] A. Keshavarz-Haddad and R. Riedi, “Bounds for the capacity of wireless multihop networks imposed by topology and demand,” in Proc. ACM Int. Symp. Mobile Ad Hoc Netw. Comput. (MobiHoc), 2007, pp. 256–265.

[27] A. Keshavarz-Haddad and R. Riedi, “Multicast capacity of large homogeneous multihop wireless networks,” in Proc. IEEE Int. Symp. Modeling Optim. Mobile Ad Hoc Wireless Netw. (WiOpt), 2008, pp. 116–124.   
[28] C. Wang, C. Jiang, Y. Liu, X.-Y. Li, S. Tang, and H. Ma, “Aggregation capacity of wireless sensor networks: Extended network case,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), 2011, pp. 1701–1709.   
[29] L. Fu, Y. Qin, X. Wang, and X. Liu, “Throughput and delay analysis for convergecast with MIMO in wireless networks,”IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 4, pp. 768–775, 2012.   
[30] L. Ying, R. Srikant, and G. Dullerud, “Distributed symmetric function computation in noisy wireless sensor networks,”IEEE Trans. Inf. Theory, vol. 53, no. 12, pp. 4826–4833, 2007.   
[31] J. Zhang, F. Ren, T. He, and C. Lin, “Attribute-aware data aggregation using dynamic routing in wireless sensor networks,” in Proc. IEEE Int. Symp. World Wireless Mobile Multimedia Netw. (WoWMoM), 2010, pp. 1–9.   
[32] P. Wan, C. Scott, L. Wang, Z. Wan, and X. Jia, “Minimum-latency aggregation scheduling in multihop wireless networks,” in Proc. ACM Int. Symp. Mobile Ad Hoc Netw. Comput. (MobiHoc), 2009, pp. 185–194.   
[33] X. Wang, L. Fu, X. Tian, Y. Bei, Q. Peng, X. Gan, H. Yu, and J. Liu, “Converge cast: On the capacity and delay tradeoffs, ”IEEE Trans. Mobile Comput., vol. 11, no. 6, pp. 970–982, June 2012.   
[34] L. Fu, Y. Qin, X. Wang, and X. Liu, “Converge-cast with MIMO,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), 2011, pp. 649–657.   
[35] S. Servetto, “Lattice quantization with side information: Codes, asymptotics, and applications in sensor networks,” IEEE Trans. Inf. Theory, vol. 53, no. 2, pp. 714–731, 2007.   
[36] A. Wyner and J. Ziv, “The rate-distortion function for source coding with side information at the decoder,” IEEE Trans. Inf. Theory, vol. 22, no. 1, pp. 1–10, 1976.   
[37] O. Guleryuz and U. Kozat, “Joint compression, detection, and routing in capacity contrained wireless sensor networks,” in Proc. IEEE/SP 13th Workshop Stat. Signal Process., 2005, pp. 1026–1031.   
[38] C. Chen, J. Ma, and K. Yu, “Designing energy-efficient wireless sensor networks with mobile sinks,” in Proc. ACM Sensys’06 Workshop WSW, 2006.   
[39] C. Park, K. Lee, Y. Kim, and S. Ko, “A route maintaining algorithm using neighbor table for mobile sinks,” Wireless Netw., vol. 15, no. 4, pp. 541–551, 2009.   
[40] S. Gao, H. Zhang, and S. Das, “Efficient data collection in wireless sensor networks with path-constrained mobile sinks,” IEEE Trans. Mobile Comput., vol. 10, no. 4, pp. 592–608, Apr. 2011.

![](images/3cab07c008801de9080666fb2555c8bf36917ea1b497f9e64b4df3d136a8889a.jpg)



Yunhao Liu (SM’06) received the BS degree in Automation Department from Tsinghua University, China, in 1995, and the MA degree in Beijing Foreign Studies University, China, in 1997, and an MS and a Ph.D. degree in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively. He is a member of Tsinghua National Lab for Information Science and Technology, China, and the director of Tsinghua National MOE Key Lab for Information Security, China. He is also a faculty at

the Department of Computer Science and Engineering, the Hong Kong University of Science and Technology, Clear Water Bay, Hong Kong, China. He is also the ACM Distinguished Speaker.

![](images/b47ad1692a83ad5315ef82efa66988a07a815b7d617f9259ee42e73b54c5782a.jpg)



Xiang-Yang Li (M’99–SM’08) received MS and PhD degrees at Department of Computer Science from University of Illinois, Urbana-Champaign, in 2000. He received the Bachelor degree at Department of Computer Science and Bachelor degree at Department of Business Management from Tsinghua University, China, both in 1995. He is an associate professor of computer science at the Illinois Institute of Technology, Chicago, IL, USA. He serves as an editor of of several journals, including IEEE TPDS and Networks. He also

serves in Advisory Board of Ad Hoc & Sensor Wireless Networks from 2005, and IEEE CN from 2011.

![](images/84351a7e548df849f961e8a3269397018c0faf2f5f1fb9f90d14925da1c409a1.jpg)



Shaojie Tang has been a PhD student of Computer Science Department, the Illinois Institute of Technology, Chicago, IL, USA, since 2006. He received BS degree in radio engineering from Southeast University, China, in 2006. His current research interests include algorithm design and analysis for wireless ad hoc networks, wireless sensor networks, and online social networks.

▽ For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.

![](images/995ccb65b6a2d4ff3f8327ff313cc2ff675e3bde5aa5845b4349b3cf16520c31.jpg)



Cheng Wang received the PhD degree in Department of Computer Science, Tongji University, Shanghai, China, in 2011. Currently, he is with the Department of Computer Science and Engineering, Tongji University. His research interests include wireless communications and networking, mobile social networks, and mobile cloud computing.

![](images/aff52b3f932b8fb21e7509239b0cef42a0ca073b130e3ee65a7287a248c05f50.jpg)



Changjun Jiang received the PhD degree from the Institute of Automation, Chinese Academy of Sciences, Beijing, China, in 1995. Currently, he is a professor with the Department of Computer Science and Engineering, Tongji University, Shanghai, China. His current areas of research are concurrent theory, Petri net, and formal verification of software, wireless networks, concurrency processing, and intelligent transportation systems.