# Capacity of Large Scale Wireless Networks Under Gaussian Channel Model∗

Shi Li

Dept. of Comp. Sci. & Tech.

Tsinghua University BeiJing, China

Yunhao Liu

Dept. of Comp. Sci. & Eng. HK Univ. of Sci. & Tech.

HongKong, China

liu@cse.ust.hk

Xiang-Yang Li

Microsoft Research Asia, & Dept. of Computer Science

Illinois Inst. of Tech., Chicago

xli@cs.iit.edu

# ABSTRACT

In this paper, we study the multicast capacity of a large scale random wireless network. We simply consider the extended multihop network, where a number of wireless nodes $v _ { i } ( 1 \leq i \leq n )$ are randomly located in a square region with side-length $a = { \sqrt { n } } ,$ , by use of Poisson distribution with density 1. All nodes transmit at constant power $P ,$ , and the power decays along path, with attenuation exponent $\alpha > 2 .$ The data rate of a transmission is determined by the SINR as $B \log ( 1 + \mathrm { S I N R } )$ . There are $n _ { s }$ randomly and independently chosen multicast sessions. Each multicast has k randomly chosen terminals. We show that, when $\begin{array} { r } { k \leq \theta _ { 1 } \frac { n } { ( \log n ) ^ { 2 \alpha + 6 } } , } \end{array}$ and $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \beta }$ , the capacity that each multicast session can achieve, with high probability, is at least $c _ { 8 } \frac { \sqrt { n } } { n _ { s } \sqrt { k } }$ , where $\theta _ { 1 } , \theta _ { 2 } ,$ and $c _ { 8 }$ are some special constants and $\beta > 0$ is any positive real number. Our result generalizes the unicast capacity [3] for random networks using percolation theory.

# Categories and Subject Descriptors

C.2.1 [Network Architecture and Design]: Wireless communication, Network topology; G.2.2 [Graph Theory]: Network problems, Graph algorithms

# General Terms

Algorithms, Design, Theory

# Keywords

Wireless ad hoc networks, capacity, multicast, broadcast, unicast, scheduling, optimization, probability theory, percolation theory.

∗Part of the work was done when Xiang-Yang Li visited Microsoft Research Asia, BeiJing, China. The research of Yunhao Liu and Xiang-Yang Li are partially supported by National Basic Research Program of China (973 Program) under grant No. 2006CB30300, the National High Technology Research and Development Program of China (863 Program) under grant No. 2007AA01Z180, and Hong Kong RGC HKUST 6169/07. Xiang-Yang Li is also partially supported by NSF grant CCF-0515088, the RGC under Grant HKBU 2104/06E and CERG under Grant PolyU-5232/07E.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, to republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee.

MobiCom’08, September14–19, 2008, San Francisco, California, USA.

Copyright 2008 ACM 978-1-60558-096-8/08/09 ...\$5.00.

# 1. INTRODUCTION

In many applications, e.g., wireless sensor networks, we often need an estimation on the (asymptotic) achievable throughput when we randomly deploy n wireless nodes in a given region. The main purpose of this paper is to study the asymptotic capacity of large scale random wireless networks when we choose the best protocols for all layers. As in the literature, we will mainly consider one type of networks, large scale random networks, where a large number of nodes are randomly placed in the deployment region.

Due to spatial separation, several wireless nodes can transmit simultaneously provided that these transmissions will not cause destructive wireless interferences to any of the simultaneous transmissions. To describe when a transmission is received successfully by its intended recipient, a number of interference models have been proposed and studied in the literature, which include

1) Protocol Interference Model (PrIM) [7]: In this model, a transmission by a node vi is successfully received by an intended target $v _ { j }$ iff node vj is sufficiently apart from the source of any other simultaneous transmission, $i . e . , \| v _ { k } - v _ { j } \| \geq ( 1 + \eta ) \| v _ { i } - v _ { j } \|$ for any transmitting node $v _ { k } \ne v _ { i }$ . Here η is a constant.

2) Fixed-Power Protocol Interference Model (fPrIM): In this model, each node $v \in V$ has a fixed constant transmission range r and a fixed constant interference range $R > r$ . A node u can successfully receive a transmission from another node v iff (1) ku− $\left. v \right\| \leq r ,$ , and (2) there is no other node w such that $\| w - u \| \leq$ R and node w is transmitting simultaneously with node v. Here $\lVert \boldsymbol { w } - \boldsymbol { u } \rVert$ is the Euclidean distance between w and u.

3) Physical Interference Model(PhIM): At any time, given a set of simultaneous transmitting nodes $A ~ = ~ \{ u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot ~ , u _ { a } \}$ , a node v can successfully receive the signal from a sender u iff $\begin{array} { r } { \mathrm { S I N R } \ = \ \frac { P _ { u } \cdot \ell ( u , v ) } { N _ { 0 } + \sum _ { i = 1 } ^ { a } P _ { u _ { i } } \ell ( u _ { i } , v ) } \ \geq \ \sigma , } \end{array}$ . Here σ is a threshold for SINR, $P _ { u _ { i } }$ is the transmission power of node $u _ { i } , \ell ( u _ { i } , v )$ is the path loss of signal propagation, and $N _ { 0 }$ is the variance of background noise.

4) Gaussian Channel Model (GIM): At any time instance, given a set of simultaneous transmitting nodes $A = \{ u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot , u _ { a } \}$ . a node v can successfully receive the signal from a sender $u _ { j }$ at a data rate B log(1 + SINR), where SINR =  N0+Pai=1 Pui \`(ui,v) $\begin{array} { r } { \mathrm { S I N R } = \frac { P { \boldsymbol { u } } _ { j } \cdot { \boldsymbol { \ell } } ( { \boldsymbol { u } } _ { j } , { \boldsymbol { v } } ) } { N _ { 0 } + \sum _ { i = 1 } ^ { a } P _ { { \boldsymbol { u } } _ { i } } { \boldsymbol { \ell } } ( { \boldsymbol { u } } _ { i } , { \boldsymbol { v } } ) } } \end{array}$ Puj ·\`(uj ,v) and B is the bandwidth of the channel.

In the first three of the preceding models (PrIM, fPrIM, PhIM), when the transmission is successful, each wireless node can transmit at W bits/second over a common wireless channel. The unicast capacity for large scale random wireless networks has been extensively studied. The ground breaking work by Gupta and Kumar [7] has shown that, (1) for large scale random networks of n nodes inside a unit square, the asymptotic per-flow unicast capacity with n random flows is $\Theta ( W / \sqrt { n \log n } )$ under fPrIM, (2) for networks where nodes are arbitrarily located (not necessarily randomly placed) in a unit square, when each node wishes to communicate to a destination located at a nonvanishingly small distance away, the amount of information that can be exchanged by each source-destination pair must go to zero, as √ $n  \infty$ , at least at rate $\Theta ( W / \sqrt { n } )$ under PrIM or PhIM. This result was originally proved as the consequences of the interference model used (fPrIM or PhIM with assumption $\ell ( u , v ) = 1 / \| u - v \| ^ { \alpha }$ for a constant $\alpha > 2 ) [ 7 ]$ . It has later been extended to hold in a more general information theoretic setting [22]. Gupta and Kumar [7] also showed that when nodes are randomly located in a unit square area, each source-destination pair can achieve a bit rate only of order $1 / { \sqrt { n \log n } }$ , by using a specific multihop strategy, when fPrIM or PhIM models are used. For Gaussian channel model, using multihop transmission, pairwise coding and decoding at each hop, and a TDMA scheme, Franceschetti et al. [3] shows that a rate $\Omega ( 1 / \sqrt { n } )$ is achievable in networks of randomly located nodes (not only some arbitrarily placed nodes). Hence, there is no gap between the capacity of randomly located, and arbitrarily located nodes, at least up to a constant scaling, although using different channel models.

In this paper, we will concentrate on the multicast capacity of a random wireless network, which generalizes both the unicast capacity [7] and broadcast capacity [9, 20] for random networks. We assume that a set of wireless nodes $V = \{ v _ { 1 } , v _ { 2 } , \cdot \cdot \cdot , v _ { n } , \cdot \cdot \cdot \}$ are randomly distributed (with Poisson distribution of rate 1) in a square region $B _ { n }$ with a side-length $a \ = \ { \sqrt { n } }$ and all nodes transmit at a constant power $P .$ . Assume that a subset $s \subseteq V$ of $n _ { s } = | \boldsymbol { S } |$ random nodes will serve as the source nodes of $n _ { s }$ multicast sessions. We randomly and independently choose ns multicast sessions as follows. To generate the i-th $( 1 ~ \leq ~ i ~ \leq ~ n _ { s } )$ multicast session, k points $p _ { i , j } ( 1 \leq j \leq k )$ are randomly and independently chosen from the deployment region $B _ { n }$ . Let $v _ { i , j }$ be the nearest wireless node from $p _ { i , j }$ (ties are broken randomly). In the i-th multicast session, $v _ { i , 1 }$ will multicast data to $k - 1$ nodes $U _ { i } = \{ v _ { i , j } \mid 2 \leq j \leq k \}$ at an arbitrary data rate $\lambda _ { i }$ . The aggregated multicast capacity with $\boldsymbol { S } = \left\{ v _ { 1 , 1 } , v _ { 2 , 1 , } \cdot \cdot \cdot \ , v _ { n _ { s } , 1 } \right\}$ as roots for a network is defined as $\begin{array} { r } { \Lambda _ { k , S } ( n ) = \sum _ { v _ { i } \in { \mathcal { S } } } \lambda _ { i } } \end{array}$ when there is a schedule of transmissions such that all multicast flows will be received by their destination nodes successfully within a finite delay. Similarly, we define the minimum per-flow multicast throughput (or capacity) as $\begin{array} { r } { \lambda _ { k , s } ( n ) = \operatorname* { m i n } _ { v _ { i } \in \mathcal { S } } \lambda _ { i } } \end{array}$ . Our result will show how the multicast capacity of wireless networks scale with the number of nodes in the networks, or scale with the size of the deployment region, or scale with the size of multicast group.

Using fixed-power protocol interference model fPrIM, Li et al. [14] and Shakkottai et al. [19] showed that, when there are $n _ { s }$ multicast flows and each multicast flow will have k receivers, the perflow multicast capacity of $\boldsymbol { n } _ { s }$ flows for random networks is of order $\frac { W { \sqrt { n } } } { n _ { s } { \sqrt { k \log n } } }$ when $k = O ( n / \log n )$ , and is of order $W / n _ { s }$ when $k = \Omega ( n / \log n )$ . Although protocol interference model can approximate the interference to some extent, experiment studies show that they are still much different from the practice. In this paper, we study the asymptotic network capacity using the Gaussian Channel model. For presentation simplicity, we assume that there is only one channel in the wireless networks. As always, we assume that the packets are sent from node to node in a multi-hop manner until they reach their final destinations. The packets could be buffered at intermediate nodes while awaiting for transmission. Intermediate nodes can only store and forward packets (no other operations such as network coding are allowed here). We assume that the buffer is large enough so packets will not get dropped by any intermediate node. We leave it as future work to study the scenario when network coding is permitted, the buffers of intermediate nodes are bounded by some values. In some results, we assume that every intermediate node have infinite buffer size. For most of the results presented here, the delay of the routing is not considered, $i . e .$ , the delay in the worst case could be arbitrarily large for some results.

Our Main Contributions: This paper shows that a per-flow√ multicast rate $1 / { \sqrt { n k } }$ is achievable in networks of n randomly located nodes in a square region $B _ { n } = { \sqrt { n } } \times { \sqrt { n } }$ . Specifically, we will prove the following main theorem.

THEOREM 1. When $\begin{array} { r } { k \le \theta _ { 1 } \frac { n } { ( \log n ) ^ { 2 \alpha + 6 } } } \end{array}$ 1 n(log n)2α+6 and ns ≥ θ2n1/2+β $n _ { s } ~ \ge ~ \theta _ { 2 } n ^ { 1 / 2 + \beta }$ for some constants $\theta _ { 1 } , \theta _ { 2 }$ and and any positive real number $\beta ,$ , with high probability1, each multicast source node can send data to all its intended receivers with rate at least

$$
c _ {8} \frac {\sqrt {n}}{n _ {s} \sqrt {k}}
$$

where constants $\begin{array} { r } { c _ { 8 } = { \frac { 1 } { 2 } } \operatorname* { m i n } \{ c _ { 4 } , c _ { 7 } \} , c _ { 4 } = { \frac { 2 ^ { \alpha } B P } { c _ { 0 } N _ { 0 } \sqrt { \theta _ { 1 } } } } \quad } \end{array}$ 2 BPc0N0√θ1 , and c7 =´ $c _ { 7 } =$ $\begin{array} { r } { \frac { B } { 1 0 0 ( ( 9 7 \kappa \sqrt { \theta _ { 3 } } + 2 4 ) h + 1 ) } \log \left( 1 + \frac { P \cdot ( 2 \sqrt { 2 } c ) ^ { - \alpha } } { N _ { 0 } + 2 2 P ( 2 \sqrt { 2 } c ) ^ { - \alpha } } \right) } \end{array}$ Here c0, c, κ are constants.

In terms of capacity upper bound, we proved that

THEOREM 2. The asymptotic per-flow unicast capacity of n flows in a large scale random network with n nodes randomly distributed in a square $B _ { n }$ is at most of order $1 / \sqrt { n }$ .

Compared with [14, 19], studying the multicast capacity with Gaussian channel model requires new technical insights. Our result is derived based on the highway system that can be formed by use of percolation theory. The upper bound on asymptotic perflow unicast capacity proved in Theorem 2 shows that the capacity achieved by [3] is asymptotically optimal, and thus closes the gap when Gaussian link model is used.

The rest of the paper is organized as follows. In Section 2, we briefly describe the network and system model used throughout the paper. Our routing strategy that can achieve asymptotic optimal multicast capacity is presented in Section 3. We present the theoretic analysis in Section 4 and present a matching upper bound for asymptotic per-flow unicast capacity in Section 5. We review the related work in Section 6 and conclude the paper in Section 7.

# 2. NETWORK AND SYSTEM MODEL

Consider a square region $B _ { n }$ of side-length ${ \sqrt { n } } .$ . We randomly place a number of nodes inside this square region by use of Poisson distribution with rate 1. Assume that each node can transmit at constant power $P ,$ , and node $v _ { j }$ receives the transmitted signal from $v _ { i }$ with power $P \cdot \ell ( d ( v _ { i } , v _ { j } ) )$ , where $d ( v _ { i } , v _ { j } )$ is the Euclidean distance between vi and $v _ { j } .$ , and $\ell ( d )$ is the transmission loss during a path of length d. In this paper, we consider the attenuation function

$$
\ell (d) = \min \{1, d ^ {- \alpha} \},
$$

where the constant $\alpha > 2 .$ . In a Gaussian channel model, the rate of a transmission from node $v _ { i }$ to node $v _ { j }$ is

$$
\begin{array}{l} R (v _ {i}, v _ {j}) = B \log \left(1 + \frac {S (v _ {i} , v _ {j})}{N _ {0} + I (v _ {i} , v _ {j})}\right) \\ = B \log \left(1 + \frac {P \cdot \ell (d (v _ {i} , v _ {j}))}{N _ {0} + \sum_ {k \neq i , v _ {k} \in \mathcal {A}} P \cdot \ell (d (v _ {k} , v _ {j}))}\right) \\ \end{array}
$$

where $\mathcal { A }$ is the set of nodes transmitting simultaneously with node $v _ { i } , B$ is the channel bandwidth, $N _ { 0 }$ is the variance of background noise, $I ( v _ { i } , v _ { j } )$ is the total interference at the receiving node $v _ { j }$ when $v _ { i }$ is communicating with $v _ { j } .$ and $S ( w , v )$ is the strength of signal (sent by w and received at v).

We choose $n _ { s }$ nodes to be the sources of the multicast sessions. For each source node, choose $k - 1$ nodes to be its intended receivers. The source nodes and their receivers are chosen using the the process described in Algorithm 1.

Algorithm 1 Process for selecting $n _ { s }$ multicast sessions   
1: for $i \leftarrow 1, 2, \cdots, n_{s}$ do
2:    for $j \leftarrow 1, 2, \cdots, k$ do
3:    Randomly choose a point $p_{i,j}$ in $B_{n}$ .
4:    Choose a node $v_{i,j}$ from V that is closest to $p_{i,j}$ 5:    end for
6:    Let $v_{i,1}$ be a source node and $v_{i,2}, v_{i,3}, \cdots, v_{i,k}$ be its intended receivers.
7: end for

In Algorithm 1, different multicast sessions may have the same source, and two receivers of a multicast session may be the same. A source node may be also an intended receiver of itself. These may confuse us when considering the multicast rate. Therefore, it is necessary to clarify them. If two receivers of a multicast session are the same, i.e, $v _ { i , j _ { 1 } } = v _ { i , j _ { 2 } }$ , we can simply remove one of them. To notice that, a node can transmit data to itself with arbitrary large rate. However, things are different when considering the set of $n _ { s }$ sources. If the sources of two multicast sessions are the same, we must treat them separately. Notice that both the transmitted data and the intended receivers of the two multicast sessions are different. We can not combine the receivers of these two multicast sessions together either.

Given a random wireless network of n nodes and the set $s$ of $n _ { s } = | \boldsymbol { S } |$ source nodes, let $\lambda _ { \mathcal { S } } = ( \lambda _ { i _ { 1 } } , \lambda _ { i _ { 2 } } , \cdots , \lambda _ { i _ { n _ { s } - 1 } } , \lambda _ { i _ { n _ { s } } } )$ be the rate vector of the multicast data rate of all $n _ { s }$ multicast sessions. Here $\lambda _ { i _ { j } }$ is the data rate of node $v _ { i _ { i } } \in S$ , for $1 \leq j \leq n _ { s }$ . When given a fixed network $G = ( V , E )$ , where the node positions of all nodes $V ,$ set S of $n _ { s }$ source nodes, the set of receivers $U _ { i }$ for each source node vi, and the multicast data rate $\lambda _ { i }$ for each source node $v _ { i }$ are all fixed, we first define what is a feasible rate vector λ for the network G. A multicast rate vector $\lambda _ { \mathcal { S } }$ bits/sec is feasible if there is a spatial and temporal scheme for scheduling transmissions such that by operating the network in a multi-hop fashion and buffering at intermediate nodes when awaiting transmission, every node vi can send $\lambda _ { i }$ bits/sec average to its chosen $k - 1$ destination nodes. That ${ \mathrm { i s } } ,$ there is a $T < \infty$ such that in every time interval (with unit seconds) $[ ( i - 1 ) \cdot T , i \cdot T ]$ , every node $v _ { i } \in S$ can send $T \cdot \lambda _ { i }$ bits to its corresponding $k - 1$ receivers $U _ { i }$ .

The total throughput of such feasible rate vector for multicast is defined as $\begin{array} { r } { \Lambda _ { k , S } ( \bar { n } ) \stackrel { - } { = } \sum _ { v _ { i } \in { \mathcal { S } } } \lambda _ { i } } \end{array}$ . The average per-flow multicast throughput is $\begin{array} { r } { \lambda _ { k , S } ^ { a } ( n ) = \frac { \sum _ { v _ { i } \in S } \lambda _ { i } } { n _ { s } } } \end{array}$ . The minimum per-flow multicast throughput is $\begin{array} { r } { \lambda _ { k , s } ( n ) \stackrel { \smile } { = } \operatorname* { m i n } _ { v _ { i } \in \mathcal { S } } \lambda _ { i } } \end{array}$ , where k is the total number of nodes in each multicast session, including the source node. When S is clear from the context, we drop S from our notations. When we mention per flow multicast capacity, hereafter we mean the minimum per flow multicast capacity, if not explained otherwise. An aggregated multicast throughput $\Lambda _ { k } ( n )$ bits/sec is feasible for $n _ { s }$ multicast sessions (each session with k terminals) if there is a rate vector $\lambda _ { \mathcal { S } } ~ = ~ \left( \lambda _ { i _ { 1 } } , \lambda _ { i _ { 2 } } , \cdot \cdot \cdot ~ , \lambda _ { i _ { n _ { s } - 1 } } , \lambda _ { n _ { s } } \right)$ ) that is feasible and $\begin{array} { r } { \Lambda _ { k } ( n ) = \sum _ { v _ { i } \in \mathcal { S } } \dot { \lambda _ { i } } } \end{array}$ . Similarly, we say $\lambda _ { k } ( n ) =$ min $. v _ { i } \in S$ λi is a feasible per-flow multicast throughput.

DEFINITION 1 (CAPACITY OF RANDOM NETWORKS). We say that the multicast capacity per flow of a class of random networks is of order $\Theta ( f ( n ) )$ bits/sec if there are deterministic constants $c > 0$ and $c < c ^ { \prime } <$ < +∞ such that

$$
\lim _ {n \rightarrow \infty} \boldsymbol {P r} (\lambda_ {k} (n) = c f (n) i s f e a s i b l e) = 1
$$

$$
\operatorname * {l i m i n f} _ {n \to \infty} \boldsymbol {P r} \left(\lambda_ {k} (n) = c ^ {\prime} f (n) \text {   is   feasible }\right) <   1
$$

Here the probability is computed using all possible connected random networks formed by n nodes distributed in a square with sidelength a. We will study the per-flow multicast capacity under Gaussian channel model, instead of the fPrIM used in [14, 19].

# 3. OUR SOLUTION

In this section, we will first present several technical lemmas that will be used in our latter analysis; then we briefly review the highway system proposed in [3]; we then present our multicast method based on the highway system; we finally analyze the performance of our multicast method.

# 3.1 Technical Lemmas

To study the asymptotic multicast capacity, we first present some technical lemmas that are essential for the analysis.

LEMMA 3. At any time instance, assume that for any receiver $v _ { i } ,$ the following two conditions are satisfied:

• $C _ { 1 } \colon$ vi is within Euclidean distance r from its sender $v _ { j } ;$ and   
• $C _ { 2 } \colon$ for any other sender $v _ { k } ( k \neq j )$ , the Euclidean distance between vk and $v _ { i }$ is at least R with $R > r$ .

Then each receiver can receive at rate at least

$$
B \log \left(1 + \frac {P \cdot \ell (r)}{N _ {0} + c _ {1} P (R - r) ^ {- \alpha}}\right),
$$

where $c _ { 1 }$ is a constant only depending on α.

PROOF. Let $V _ { S }$ be the set of senders (which have at least one intended receiver), and $V _ { R }$ be the set of receivers. So, $V _ { S } \cap V _ { R } =$ Ø. If conditions $C _ { 1 }$ and $C _ { 2 }$ are satisfied, any two senders are at least $R ^ { \prime } = R - r$ away from each other. For any receiver $v ^ { \ast } \in V _ { R }$ and non-negative integer g, let

$$
\mathcal {N} _ {g} (v ^ {*}) = \left\{v \in V _ {S} \mid g R ^ {\prime} \leq d (v ^ {*}, v) <   (g + 1) R ^ {\prime} \right\}.
$$

Let $v ^ { \prime }$ be the intended sender of $v ^ { \ast }$ , and $n _ { g } ( v ^ { * } ) = | \mathcal { N } _ { g } ( v ^ { * } )$ | be the size of $ { \mathcal { N } } _ { g } ( v ^ { * } )$ . If we divide the ring (centered at node $v ^ { * } )$ into tg = 2d π(g+1)R00 e $\begin{array} { r } { t _ { g } = 2 \lceil \frac { \pi ( g + 1 ) R ^ { \prime } } { R ^ { \prime } / 2 } \rceil \ = \ 2 \lceil \pi ( 2 g + 2 ) \rceil } \end{array}$ R /2 sectors (see Figure 1), the distance of any two points in the same sector is at most $R ^ { \prime }$ . Here the ring is divided as follows: We first divide the ring into π(g+1)R0R0/2 $\frac { \pi ( g + 1 ) R ^ { \prime } } { R ^ { \prime } / 2 }$ sectors, then each sector is divided into two sectors by a circle with radius $( g + 1 / 2 ) R ^ { \prime }$ . Thus, a sector contains at most 1 sender, i.e.,

$$
n _ {g} (v ^ {*}) \leq t _ {g} = 2 \lceil \pi (2 g + 2) \rceil .
$$

Since other traP $\begin{array} { r } { n _ { 0 } ( v ^ { * } ) = 0 , } \end{array}$ , the tdes is $v ^ { * }$ $\begin{array} { r } { I ( v ^ { \prime } , \breve { v } ^ { * } ) \leq \sum _ { a = 1 } ^ { \infty } n _ { g } ( v ^ { * } ) P \cdot \ell ( g R ^ { \prime } ) \leq } \end{array}$ $\begin{array} { r } { \sum _ { a = 1 } ^ { \infty } 2 \lceil \pi ( 2 g + 2 ) \rceil P ( g R ^ { \prime } ) ^ { - \alpha } \leq P R ^ { \prime - \alpha } \sum _ { a = 1 } ^ { \infty } 2 \lceil \pi ( 2 g + 2 ) \rceil g ^ { - \alpha } } \end{array}$ . Obviously, the sum in the rightmost inequality converges if α $\iota > 2 .$ . So, $I ( v ^ { \prime } , \bar { v } ^ { * } ) \leq c _ { 1 } P ( R - r \bar { ) } ^ { - \alpha }$ , where $c _ { 1 }$ is a constant. Thus,

$$
\begin{array}{l} R (v ^ {\prime}, v ^ {*}) = B \log \left(1 + \frac {S (v ^ {\prime} , v ^ {*})}{N _ {0} + I (v ^ {\prime} , v ^ {*})}\right) \\ \geq B \log \left(1 + \frac {P \cdot \ell (r)}{N _ {0} + c _ {1} P (R - r) ^ {- \alpha}}\right), \\ \end{array}
$$

where $\begin{array} { r } { c _ { 1 } = \sum _ { g = 1 } ^ { \infty } { 2 \lceil \pi ( 2 g + 2 ) \rceil g ^ { - \alpha } } } \end{array}$ is a constant if $\alpha > 2 .$ .

LEMMA 4. $F o r \gamma > 0 ,$ , if we partition the square $B _ { n } = [ 0 , \sqrt { n } ] \times$ [0, n] into at least τ1 nlogγ n $[ 0 , \sqrt { n } ]$ $\tau _ { 1 } \frac { n } { \log ^ { \gamma } n }$ subsquare regions of area at most $\tau _ { 2 } \log ^ { \gamma } n$ , then w.h.p every region contains at most $2 \tau _ { 2 } \log ^ { \gamma }$ n nodes. (τ1 and τ2 are constants.)

PROOF. Let $A _ { n }$ be the event that there are more than $2 \tau _ { 2 } \log ^ { \gamma }$ n nodes in some subsquare. Then by the union bound and Chernoff bound (Lemma 24), the probability of event $A _ { n }$ is

$$
\begin{array}{l} \operatorname * {P r} (A _ {n}) \leq \left[ \tau_ {1} \frac {n}{\log^ {\gamma} n} \right] \frac {e ^ {- \tau_ {2} \log^ {\gamma} n} (e \tau_ {2} \log^ {\gamma} n) ^ {2 \tau_ {2} \log^ {\gamma} n}}{(2 \tau_ {2} \log^ {\gamma} n) ^ {2 \tau_ {2} \log^ {\gamma} n}} \\ = \left\lceil \tau_ {1} \frac {n}{\log^ {\gamma} n} \right\rceil e ^ {- \tau_ {2} \log^ {\gamma} n} \left(\frac {e}{2}\right) ^ {2 \tau_ {2} \log^ {\gamma} n} \\ = \left\lceil \tau_ {1} \frac {n}{\log^ {\gamma} n} \left. \right]\left(\frac {e}{4}\right) ^ {\tau_ {2} \log^ {\gamma} n} \rightarrow 0 \\ \end{array}
$$

as n tends to infinity.

Observe that when $\begin{array} { r } { \gamma > 1 , \mathrm { P r } ( A _ { n } ) < \frac { \tau _ { 1 } } { n ^ { \tau _ { 2 } \log ( 4 / e ) - 1 } } . } \end{array}$ .

LEMMA 5. If we partition $B _ { n }$ into regions of area at least a log n $( f o r a \ge 1 )$ , then w.h.p every region contains at least 1 node.

PROOF. Let $A _ { n }$ be the event that some region is empty of nodes. Then $\begin{array} { r } { \operatorname* { P r } ( A _ { n } ) \leq \left\lceil \frac { n } { a \log n } \right\rceil \left( 1 - \frac { a \log n } { n } \right) ^ { n } \leq \left\lceil \frac { n } { a \log n } \right\rceil e ^ { - a \log n } = } \end{array}$ a log n $\textstyle \left\lceil { \frac { n } { a \log n } } \right\rceil { \frac { 1 } { n ^ { a } } } \to 0$ as n tends to infinity. That’s to say, w.h.p, there are at least 1 node in every region.

# 3.2 Constructing highway system using percolation theory

Our routing strategy is built upon the highway system developed in [3]. We first review the highway system defined in [3]. To begin the construction of highway system, we partition the deployment box $B _ { n }$ into subsquares si of a constant side length c, as depicted in Figure 2. In Figure 2, let $X ( s _ { i } )$ be the number of random nodes inside si. By appropriately choosing c, we can arrange that the probability that a square contains at least a Poisson node is as high as we want. Indeed, for all i, we have $p \equiv \operatorname* { P r } ( X ( s _ { i } ) \geq 1 ) = 1 - e ^ { - c ^ { 2 } }$ e−c2 . We say that a square is open if it contains at least one node, and closed otherwise. Notice that squares are open (and closed) with a probability $p$ (and $1 - p )$ , independently of each other. Observe that the event whether a square $s _ { i }$ is open is independent of the event whether another square $s _ { j }$ is open. Thus, percolation theory can be applied here. This model is then mapped into a discrete edge-percolation model on the square grid.

We associate an edge to each square, traversing it diagonally, as depicted on the right-hand side of the Figure 2. The edge is said to be either open or closed according to the state of the corresponding square. We then obtain a grid $G _ { n }$ of horizontal and vertical edges, each edge being open, independently of all other edges, with probability p. A path of $G _ { n }$ is said to be open if it contains only open edges. Observe that an open edge implies that we have a routing path such that the data rate achievable by this path is of a constant value (depending on c) from Lemma 3, using a TDMA scheduling of nodes. Note that, when constant c is large enough, the preceding construction produces winding open paths that cross the entire network area. Denote the number of edges composing the side length of $B _ { n }$ by $\begin{array} { r } { m = \frac { \sqrt { n } } { c \sqrt { 2 } } } \end{array}$ c  2 , where c is rounded up such that m is an integer. By Theorem 23, we can choose c large enough such that, w.h.p., there are $\Omega ( m )$ paths crossing $B _ { n }$ from left to right. These paths can be grouped into disjoint sets of paths: each group have dδ log me paths, crossing a rectangle of width m and height κ log $m - \epsilon _ { m }$ , for all $\kappa > 0 , \delta$ small enough, and a vanishingly small $\epsilon _ { m }$ so that the side length of each rectangle is an integer. See Figure 3 for illustration. The same is true if we divide the area into vertical rectangles and look for paths crossing the area from bottom to top. Using the union bound, they [3] conclude that there exist both horizontal and vertical disjoint paths w.h $\cdot \mathrm { p } .$ These paths form a backbone, that was called the highway system [3].

We then slice each horizontal rectangle into horizontal strips of constant height $h .$ By choosing h appropriately we can guarantee that there are at least the same paths as strips in every strip. Similarly, we can divide the vertical rectangle into vertical strips. We let $H = \kappa \log m - \epsilon _ { m }$ be the height of the horizontal rectangles(or the width of the vertical rectangles), h be the height of the strips(or the width of the vertical strip), $J = \sqrt { n } / H$ be the number of horizontal(vertical) rectangles, and $L = H / h$ be the number of horizontal(vertical) strips in a horizontal(vertical) rectangle. As there are at least the same horizontal(vertical) highways as the strips in a horizontal(vertical) rectangle, L node-disjoint horizontal crossing highways can be chosen in each rectangle. In all, we choose $\overset { \vartriangle } { M } = \overset { \vartriangle } { J } \times \dot { L }$ horizontal(vertical) highways.

Let $\Pi _ { 1 } , \Pi _ { 2 } , \cdots$ , ΠM be the M horizontal highways, such that $\Pi _ { ( i - 1 ) L + j } ( 1 \leq i \leq J , 1 \leq j \leq L )$ is a highway in the i-th rectangle. We also let $\pi _ { i , j }$ be the j-th node in the i-th horizontal highway. So, a highway Πi can be denoted by a list of nodes, i.e, $\Pi _ { i } =$ $( \pi _ { i , 1 } , \pi _ { i , 2 } , \cdot \cdot \cdot , \pi _ { i , s _ { i } } )$ . Similarly, we use $\Phi _ { 1 } , \Phi _ { 2 } , \cdots , \Phi _ { M }$ to denote the M vertical highways, where $\Phi _ { i } = ( \phi _ { i , 1 } , \phi _ { i , 2 } , \cdot \cdot \cdot , \phi _ { i , t _ { i } } )$ . In this paper, we propose the following definition that will be used in our proofs later.

DEFINITION 2. We call a horizontal(vertical) highway $\Pi _ { i } \ =$ $( \pi _ { i , 1 } , \pi _ { i , 2 } , \cdot \cdot \cdot , \pi _ { i , s _ { i } } ) ( o r \Phi _ { i } = \left( \phi _ { i , 1 } , \phi _ { i , 2 } , \cdot \cdot \cdot , \phi _ { i , t _ { i } } \right) )$ legal if there does not exist j1, j2 such that $1 \ \leq \ j _ { 1 } \ < \ j _ { 2 } \ \leq \ s _ { i } ( o r t _ { i } )$ and $X ( \pi _ { i , j _ { 1 } } ) > X ( \pi _ { i , j _ { 2 } } ) + 2 H ( o r Y ( \phi _ { i , j _ { 1 } } ) > Y ( \phi _ { i , j _ { 2 } } ) + 2 H )   $ . Here $X ( p )$ and $Y ( p )$ are the x-coordinate(from left to right) and y-coordinate(from up to down) of point p, respectively.

In the appendix, we will prove the following theorem.

THEOREM 6. If we find a set of M horizontal highways and M vertical highways using the percolation method, we can find a set of M legal horizontal highways and M legal vertical highways.

# 3.3 Schedule the multicast tasks

We now are ready to describe our multicast method. The proposed solution is based on multihop routing, and exploits the formation of paths percolating across the network. As in [3], we divide the nodes into disjoint sets that cross the network area. These sets form a “highway system” of nodes (called stations sometime) that can carry information across the network at constant rate, using short hops. The rest of the nodes access the highway system using single hops of longer lengths.

Our multicast protocol (Algorithm 3) contains two kinds of hops: the constant-length hop in the highway system, and the longer hop connecting a receiver $v _ { i , x }$ to some entry node $q _ { i , x }$ in the highway. We will then perform multicast (using multicast tree) to these entry nodes in the highway. To transmit data through the multicast tree, we divide our communication strategy into three separate phases:

1. In the first phase, every non-station node $v _ { i , x }$ exchanges its data with some station $q _ { i , x }$ in the highway system (we call the nodes in the highway system stations) using a single-hop communication; see Figure 4.   
2. in the second phase, data is transmitted through highways using station nodes that are part of some special Euclidean spanning tree constructed;   
3. in the third phase, data is forwarded directly to the destination nodes from the nodes of the highway system.

![](images/78b41c9f9e934c899a696d815268dcd9b094d8923569d3ef74eca69cd2d77c92.jpg)



Figure 1: Divide a ring into sectors.

![](images/69bececc19697f13d41d286e7d2f439e9fa12289da1d75f5dc26a5eaff7f8f98.jpg)



Figure 2: Construction of the bond percolation model.

![](images/c5ed832afcd14ffa64d5c2735fa68789d3af47b8ee3f89fb4d1949e40a2c9d33.jpg)



![](images/00ea423f688412ea2bb3219b57bb559a70caa1a01de1e4d623b477bc91a0a46b.jpg)



Figure 3: There exists a large number of crossing paths in $B _ { m } .$ .

![](images/b4f14a336dfa00cacdb989830fb8d3a4dbe10c0529b8600292533cbda4894529.jpg)



Figure 4: Choose $q _ { i , x }$ for $v _ { i , x }$ where the path is a highway.

In the rest of our analysis, we typically will not distinguish the first phase and the third phase. In the following, we take all the $n _ { s }$ multicast sessions into consideration and analyze the date rate per multicast-session of the two phases separately.

![](images/eaa250e1e7ca49ece1461313e0f788c34302a361be493d727849ab625d3c967c.jpg)



Figure 5: A path connecting $q _ { i , x }$ and $q _ { i , y }$ contains 3 highway segments: the horizontal one from $q _ { i , x }$ to $\pi _ { z _ { x } , u _ { 1 } }$ , the vertical one from $\phi _ { w _ { x } , u _ { 2 } }$ to $\phi _ { w _ { x } , u _ { 3 } } ,$ and the horizontal one from $\pi _ { z _ { y } , t _ { 4 } }$ to $q _ { i , y } ,$ . These 3 segments are connected by shortcuts, $\pi _ { z _ { x } , u _ { 1 } } \phi _ { w _ { x } , u _ { 2 } }$ and $\phi _ { w _ { x } , u _ { 3 } } \pi _ { z _ { y } , u _ { 4 } } ,$ of length at most $\sqrt { 5 } c$ .

We first describe our method (Algorithm 2) to construct an Euclidean spanning tree of a set $P _ { i }$ of k points. We have to point out that our method will not necessarily construct an Euclidean minimum spanning of these k points. Assume that the set $P _ { i }$ of k points is located in a square region $[ 0 , a ] \times [ 0 , a ]$ . Our method for constructing an Euclidean spanning tree will first divide the region into cells (with side-length $\mathbf { \bar { \rho } } _ { a / 2 } t { - } \mathbf { \bar { 1 } }$ for $t = \lceil \log _ { 4 } k \rceil )$ . This cells are

called level $t - 1$ cell. Similarly, we can define level g cells with side-length $a / 2 ^ { g }$ . Originally, all nodes are representant nodes in level $t - 1 .$ If a level i cell contains some representant nodes, we randomly pick one (as the representant node to upper level $i - 1 )$ and build edges from all other representant nodes in this cell to the randomly picked node. We will show that the Euclidean length of the constructed tree is of order of the Euclidean length of Euclidean minimum spanning tree.

Algorithm 2 Find a Euclidean Spanning Tree for k points   
Input: $P_{i} = \{p_{i,1}, p_{i,2}, \cdots, p_{i,k}\}$ Output: An Euclidean tree spanning $P_{i}$ , denoted as $EST(P_{i})$ Algorithm:

1: $t \leftarrow$ the minimum integer such that $4^{t} \geq k$ ;

2: $P \leftarrow P_{i}$ 3: $E \leftarrow \emptyset$ ;

4: for $g \leftarrow t - 1, \cdots, 1, 0$ do

5: Divide $B_{n}$ into $2^{g} \times 2^{g}$ cells, each with size $\frac{a}{2^{g}} \times \frac{a}{2^{g}}$ ;

6: for each cell of size $\frac{a}{2^{g}} \times \frac{a}{2^{g}}$ do

7: if the cell contains $s \geq 2$ points in P then

8: Randomly choose a point $p_{i,x}$ from these s points;

9: for any other point $p_{i,y} (y \neq x)$ in this cell do

10: $E \leftarrow E \cup \{\overline{p_{i,x} p_{i,y}}\}$ 11: $P \leftarrow P - \{p_{i,y}\}$ ;

12: end for

13: end if

14: end for

15: end for

16: Output E as the edges of $EST(P_{i})$ .

# 4. ANALYSIS OF CAPACITY

We now analyze the per-flow multicast capacity achievable by our routing and scheduling protocol.

# 4.1 Data rate of the first phase

To notice that a receiver will have the same relay node from highways in all multicast sessions, our computation of the data rate from a node to its highway entrance station comprises two steps. In the first step, we only need to analyze the rate between receivers and their relay nodes. While in the second step, we calculate how many multicast sessions a non-station node $v ^ { \ast }$ is covered by, which will imply the data rate achievable in 1st and 3rd phase.

LEMMA 7. In the first (and 3rd) phase of the transmission, w.h.p.for any $1 \leq i \leq n _ { s }$ and for any $x ( 1 \leq x \leq k )$ , the date rate achievable by our method between a terminal $v _ { i , x }$ and the highway en-

# Algorithm 3 Build a multicast tree using highway

# Input:

1. $P _ { i } = \{ p _ { i , 1 } , p _ { i , 2 } , \cdot \cdot \cdot , p _ { i , k } \}$ and $E S T ( P _ { i } )$ generated from Algorithm 2,   
2. $V _ { i } = \left\{ v _ { i , 1 } , v _ { i , 2 } , \cdot \cdot \cdot , v _ { i , k } \right\}$ generated from Algorithm 1,   
3. M horizontal highways $\Pi _ { 1 } , \Pi _ { 2 } , \cdots , \Pi _ { M }$ and M vertical highways $\Phi _ { 1 } , \Phi _ { 2 } , \cdots , \Phi _ { M }$ as described previously.

Output: A multicast tree spanning $V _ { i } ,$ denoted as $M T ( V _ { i } )$ .

1: for $x  1 , 2 , \cdots , k$ do   
2: Suppose $p _ { i , x }$ is in the $z _ { x } \mathrm { - t h }$ horizontal strip;   
3: Let $q _ { i , x }$ be the node from $\Pi _ { z _ { x } }$ which is closest to the vertical line drawn from $p _ { i , x }$ (see Figure 4);

$$
\triangleright q _ {i, x} \text {   will   relay   data   for   } v _ {i, x}.
$$

4: end for

5: for each edge $\overline { { p _ { i , x } p _ { i , y } } }$ in $E S T ( P _ { i } )$ do

6: Suppose $q _ { i , x } = \pi _ { z _ { x } , u _ { 0 } ; }$ , and $q _ { i , y } = \pi _ { z _ { y } , u _ { 5 } } ;$

7: if $z _ { x } = z _ { y }$ then

8: $E ( q _ { i , x } , q _ { i , y } ) \gets ( \pi _ { z _ { x } , u _ { 0 } } , \pi _ { z _ { x } , u _ { 0 } \pm 1 , \cdot } \cdot \cdot , \pi _ { z _ { x } , u _ { 5 } } ) .$

9: else

10: Suppose $p _ { i , x }$ is on the $w _ { x } { \cdot }$ -th vertical strip.

11: Find a station $\pi _ { z _ { x } , u _ { 1 } }$ in $\Pi _ { z _ { x } }$ and a station √ $\phi _ { w _ { x } , u _ { 2 } }$ in $\Phi _ { w _ { x } }$ such that $d ( \pi _ { z _ { x } , u _ { 1 } } , \dot { \phi _ { w _ { x } , u _ { 2 } } } ) \leq \sqrt { 5 } c ;$

12: Find a station $\phi _ { w _ { x } , u _ { 3 } }$ in $\Phi _ { w _ { x } }$ and a station $\pi _ { z _ { y } , u _ { 4 } }$ in $\Pi _ { z _ { y } }$ such that $d ( \phi _ { w _ { x } , u _ { 3 } } , \pi _ { z _ { y } , u _ { 4 } } ) \leq \sqrt { 5 } c ;$

13: $E _ { 1 } ( q _ { i , x } , q _ { i , y } ) \gets ( \pi _ { z _ { x } , u _ { 0 } } , \pi _ { z _ { x } , u _ { 0 } \pm 1 , \cdot \cdot \cdot , \mathcal { \pi } _ { z _ { x } , u _ { 1 } } } ) ;$

14: $E _ { 2 } ( q _ { i , x } , q _ { i , y } ) \gets ( \phi _ { w _ { x } , u _ { 2 } } , \phi _ { w _ { x } , u _ { 2 } \pm 1 , } \cdot \cdot \cdot , \phi _ { w _ { x } , u _ { 3 } } ) ;$

15: $E _ { 3 } ( q _ { i , x } , q _ { i , y } ) \gets ( \pi _ { z _ { y } , u _ { 4 } } , \pi _ { z _ { y } , u _ { 4 } \bot 1 } , \cdot \cdot \cdot , \pi _ { z _ { y } , u _ { 5 } } ) ;$

16: $E ( q _ { i , x } , q _ { i , y } ) \ \gets \ E _ { 1 } ( q _ { i , x } , q _ { i , y } ) \ \propto \ E _ { 2 } ( q _ { i , x } , q _ { i , y } )$ ∝ $E _ { 3 } ( q _ { i , x } , q _ { i , y } ) ;$ . See Figure 5 for illustration, ∝ means concatenation of paths. . Here $E ( q _ { i , x } , q _ { i , y } )$ is a path in the highway system connecting $q _ { i , x }$ and $q _ { i , y }$ (See Figure 5).

17: end if

18: end for

19: Let $M T ^ { \prime } ( V _ { i } )$ be the set of edges that covered by any path $E ( q _ { i , x } , q _ { i , y } )$ , union the set $\{ \overline { { q _ { i , x } v _ { i , x } } } \mid 1 \leq x \leq k \}$ .

20: $M T ^ { \prime } ( V _ { i } )$ is a connected graph that covers $V _ { i } .$ We can break the cycles of the graph by removing some edges and the resulted graph would be a tree. Let $M { \bar { T } } ( V _ { i } )$ be the resulted tree.

trance station $q _ { i , x }$ is $c _ { 2 } ( \log n ) ^ { - \alpha - 2 }$ in both directions. Here $c _ { 2 }$ is a constant.

PROOF. Notice that the node $p _ { i , x }$ and $q _ { i , x }$ are within the same rectangle with height H, and the horizontal distance between them√ is at most √ ${ \sqrt { 2 } } c .$ . Then the distance between $p _ { i , x }$ and $q _ { i , x }$ is at most $H + { \sqrt { 2 } } c$ .

From Lemma $^ { 5 , }$ we can see w.h.p there is at least 1 node in every region with area log n. Thus, we could divide square $B _ { n }$ into squares with side-length $\left( 1 + \xi _ { n } \right) { \sqrt { \log n } } .$ , where $\xi _ { n }$ is the smallest positive number that $\frac { \sqrt { n } } { ( 1 + \xi _ { n } ) \sqrt { \log n } }$ is an integer. It is easily seen that $\xi _ { n }$ tends to 0 when n tends to $\infty$ . Since w.h.p each square contains a node and $v _ { i , x }$ is the closest node from the point√ $p _ { i , x } ,$ the distance $d ( p _ { i , x } , v _ { i , x } )$ is at most $\sqrt { 2 } ( 1 + \xi _ { n } ) \sqrt { \log n } , w . h . p .$ .

By adding the above two upper bounds, we can see that the√ √ distance between $v _ { i , x }$ and $q _ { i , x }$ is at most √ √ $H + \sqrt { 2 } c + \sqrt { 2 } ( 1 +$ $\xi _ { n } \bigr ) \sqrt { \log n } = \kappa \log m - \epsilon _ { m } + \sqrt { 2 } c + \sqrt { 2 } ( 1 + \xi _ { n } ) \sqrt { \log n }$ . This is√ smaller than 2κ log m for a sufficient large n. Note $m = \sqrt { n } / ( c \sqrt { 2 } )$

Then we let $r \ : = \ : 2 \kappa$ log m and $R = 2 r$ . Then by Lemma $^ { 3 , }$ the data rate $R ( v _ { i , x } , q _ { i , x } )$ that can be achieved between ´ $v _ { i , x }$ and $q _ { i , x }$ is at least B log $\begin{array} { r } { \left( 1 + \frac { P \cdot \ell ( r ) } { N _ { 0 } + c _ { 1 } P ( R - r ) ^ { - \alpha } } \right) } \end{array}$ when the condition C2 of Lemma 3 is satisfied. This condition can be guaranteed by dividing the phase 1 into time slots. We partition the square $B _ { n }$ into a number of subsquares with length $r ,$ and divide the phase 1 into 16 time slots such that within a time slot, any two subsquares that contain transmitting nodes is at least 4 subsquares away (See Figure 6 (a) for illustration). Thus, any two transmitting nodes are at least 3r away from each other. To make sure that at the same time there is at most 1 transmitting node at each subsquare, each of the 16 time slots should be divided into smaller mini-time-slots. By Lemma 4, we can see, $2 r ^ { 2 }$ mini time slots is enough w.h.p., since, w.h.p., each subsquare contains at most $2 r ^ { 2 }$ nodes. Considering the number of mini time slots, we could see that w.h $\cdot \mathbf { p } ,$ , the data rate between each pair of $v _ { i , x }$ and $q _ { i , x }$ that we can achieve is at least

$$
B \log \left(1 + \frac {P \cdot \ell (r)}{N _ {0} + c _ {1} P (R - r) ^ {- \alpha}}\right) / (1 6 \times 2 r ^ {2})
$$

$$
\geq (1 - \varepsilon_ {1}) B P \cdot r ^ {- \alpha} / (3 2 N _ {0} r ^ {2}) = (1 - \varepsilon_ {1}) \frac {B P}{3 2 N _ {0}} r ^ {- \alpha - 2}
$$

$$
\geq (1 - \varepsilon_ {1}) \frac {B P}{3 2 N _ {0}} \left((1 + \varepsilon_ {2}) \frac {\log n}{2}\right) ^ {- \alpha - 2}
$$

$$
= \frac {2 ^ {\alpha} B P}{1 6 N _ {0}} (\log n) ^ {- \alpha - 2} (1 - \epsilon_ {1}) (1 + \epsilon_ {2}) ^ {- \alpha - 2}
$$

$$
\geq \frac {2 ^ {\alpha} B P}{1 7 N _ {0}} (\log n) ^ {- \alpha - 2}
$$

The above inequality requires that n is sufficient large. In the above inequality, $\varepsilon _ { 1 }$ and $\varepsilon _ { 2 }$ are positive numbers whose value we can set.

In the above reasoning, we assigned each node a time slot and thus ${ \boldsymbol { v } } _ { i _ { x } }$ and $q _ { i , x }$ will have separate time slots. Thus, the rates in both direction can achieve the lower bound. Setting $\begin{array} { r } { c _ { 2 } = \frac { 2 ^ { \alpha } B P } { 1 7 N _ { 0 } } } \end{array}$ 17N0 will finish our proof.

![](images/9fc687cfc981b96ffd673e4af6302153d1cc7ca7e1226e03477a92ea21b92110.jpg)



Figure 6: (a) The subsquares that contain transmitting nodes are at least 4 subsquares away from each other, and each subsquare contains at most 1 transmitting node. In the figure, the nodes with arrows represent transmitting nodes. (b) The subsquares where $v ^ { * }$ may be located. $p ^ { * }$ is located in the square in the center, and the green squares and the center square (totally 21 squares) are the squares where $v ^ { * }$ may be located w. $h . p .$ .. The statement is also correct when we exchange the position of $v ^ { \ast }$ and $p ^ { * }$ .

Now we move to the second step. We need to show how many multicast sessions a node $v ^ { * }$ may be part of. First, we consider the process $\mathcal { Q }$ for choosing one node $v ^ { * }$ : randomly selecting a point $q ^ { * }$ in $B _ { n }$ and let $v ^ { * }$ be its nearest wireless node. We then are asking, what is the probability that a node $v ^ { * }$ is chosen in this process $\dot { \mathfrak { Q } } \dot { ? }$ The following lemma gives the answer.

LEMMA 8. $W . h . p ,$ , for any node $v ^ { * } ,$ , the probability that a node $v ^ { * }$ is chosen by process $\mathcal { Q }$ is at most $c _ { 3 } \frac { \log { \bar { n } } } { n }$ log n for a constant $c _ { 3 } .$ .

PROOF. This is exactly to compute the area of the regions in the Voronoi graph of the n nodes. In Lemma 5, we partition the square $B _ { n }$ into subsquares of side-length $( 1 + \xi _ { n } ) \sqrt { \log n }$ and w.h.p each subsquare contains at least 1 node. Considering a point $p ^ { * }$ in a subsquare s, w.h.p., its nearest node $v ^ { * }$ must fall in s or the 20 subsquares around s (see Figure 6 (b)). To speak in another way, if $v ^ { * }$ is in a subsquare $s ^ { \prime } , p ^ { * }$ must fall in $s ^ { \prime }$ or the 20 subsquares around $s ^ { \prime } .$ . So, the probability that a node $v ^ { \ast }$ is chosen by process $\mathcal { Q }$ at most , it is sm $2 1 { \overset { ( 1 + \xi _ { n } ) ^ { 2 } \log n } { n } }$ Since  when $\xi _ { n }$ tends to 0 as n tends tois sufficiently large. So, if $+ \infty ,$ $2 2 { \frac { \log n } { n } }$ we let $c _ { 3 } = 2 2$ , w.h.p, for any station $v ^ { * }$ , the probability is at most $c _ { 3 } { \frac { \log n } { n } } . \quad \boxed { \begin{array} { r l } \end{array} }$ n

LEMMA 9. $W . h . p ,$ , for any non-station node $v ^ { * }$ , the probability that a multicast session has $v ^ { * }$ as a receiver is at most $\overset { \cdot } { c _ { 3 } } k \frac { \log n } { n }$ .

PROOF. Since the probability that a node $v ^ { * }$ is chosen by process $\mathcal { Q }$ is at most $c _ { 3 } { \frac { \log n } { n } }$ , and $v ^ { * }$ is chosen by a multicast session as receiver if $v ^ { * }$ is chosen by at least one of k processes, the probability is at most $\displaystyle c _ { 3 } k { \frac { \log n } { n } } . \quad \boxed { \begin{array} { r l } \end{array} }$ n

LEMMA 10. In Algorithm 1, w.h.p, for any node $v ^ { * }$ , the number of times that $v ^ { * }$ is chosen by process $\mathcal { Q }$ as a multicast receiver is at most 3c3 $n _ { s } k { \frac { \log n } { n } }$ when $n _ { s } k \ge n$ .

PROOF. Let $A _ { n }$ be the event that a node $v ^ { * }$ is chosen by $\mathcal { Q }$ more than $3 c _ { 3 } n _ { s } k \frac { \log n } { n }$ times. Let $p = c _ { 3 } k { \frac { \log n } { n } }$ , the probability that $v ^ { \ast }$ is chosen as terminal of a multicast session. Then

$$
\begin{array}{l} \operatorname * {P r} (A _ {n}) \leq n _ {s} \binom {n _ {s}} {3 n _ {s} p} p ^ {3 n _ {s} p} \leq n _ {s} \left(\frac {n _ {s} e}{3 n _ {s} p}\right) ^ {3 n _ {s} p} p ^ {3 n _ {s} p} \\ \leq n _ {s} \left(\frac {n _ {s} e}{3 n _ {s}}\right) ^ {3 n _ {s} p} \leq n _ {s} \left(\frac {e}{3}\right) ^ {3 n _ {s} p} \leq n _ {s} \left(n ^ {- 3 c _ {3} (\log 3 - 1)}\right) ^ {\frac {n _ {s} k}{n}} \\ \rightarrow \quad 0 (\text { notice   that } 3 c _ {3} (\log 3 - 1) > 1 \text { and } n _ {s} k \geq n) \\ \end{array}
$$

This finishes the proof.

LEMMA 11. W.h.p, there exist a constant $c _ { 4 } > 0 ,$ the data rate that any multicast session can achieve in the first phase is at least $\begin{array} { r } { c _ { 4 } \frac { \sqrt { n } } { n _ { s } \sqrt { k } } , i f k \le \theta _ { 1 } \frac { n } { \log ^ { 2 \alpha + 6 } n } } \end{array}$ c4 n s  k 1 nlog2α+6 n and ns ≥ θ2n1/2+β, where θ1, θ2 are $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \beta }$ $\theta _ { 1 } , \theta _ { 2 }$ special constants, and $\beta > 0 i s$ s any positive real number.

PROOF. When $n _ { s } k \ge n$ and $\begin{array} { r } { k \le \theta _ { 1 } \frac { n } { \log ^ { 2 \alpha + 6 } n } } \end{array}$ , based on Lemma 7 and Lemma 10, w.h $\mathrm { . . p . }$ ., the data rate achievable per-multicast session in the first phase is

$$
\begin{array}{l} {R _ {1} ^ {1}} \geq {\frac {c _ {2} (\log n) ^ {- \alpha - 2}}{3 c _ {3} n _ {s} k \frac {\log n}{n}} = \frac {c _ {2}}{3 c _ {3}} \frac {n (\log n) ^ {- \alpha - 3}}{n _ {s} k}} \\ \geq \frac {c _ {2}}{3 c _ {3}} \left(\frac {n (\log n) ^ {- \alpha - 3}}{n _ {s} \sqrt {k}}\right) / \left(\sqrt {\theta_ {1} \frac {n}{\log^ {2 \alpha + 6} n}}\right) \\ { = } { \frac { c _ { 2 } } { 3 c _ { 3 } \sqrt { \theta _ { 1 } } } \frac { \sqrt { n } } { n _ { s } \sqrt { k } } } \\ \end{array}
$$

When $n _ { s } k < n ,$ the number of multicast session that will choose a node as receiver is w.h.p. at most 3c3 n log n = 3c3 log n. Then, $\textstyle { \frac { \log n } { n } } = 3 c _ { 3 }$ n w.h.p, the data rate that per-multicast session of the first phase can achieve is, when nsk < n and ns ≥ θ2n1/2+β, $n _ { s } k < n$ $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \beta }$

$$
\begin{array}{l} R _ {1} ^ {2} \geq \frac {c _ {2} (\log n) ^ {- \alpha - 2}}{3 c _ {3} n \frac {\log n}{n}} \geq \frac {c _ {2}}{3 c _ {3}} (\log n) ^ {- \alpha - 3} \\ \geq \frac {c _ {2}}{3 c _ {3} \sqrt {\theta_ {1}}} \frac {n ^ {- \beta}}{\sqrt {k}} \geq \frac {c _ {2}}{3 c _ {3} \sqrt {\theta_ {1}}} \frac {\sqrt {n}}{n _ {s} \sqrt {k}} \\ \end{array}
$$

In all, w.h.p., the data rate of any multicast session in the first phase is at least, when $\begin{array} { r } { k \le \theta _ { 1 } \frac { n } { \log ^ { 2 \alpha + 6 } n } } \end{array}$ and ns ≥ θ2n1/2+β, $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \varepsilon }$

$$
R _ {1} \geq \frac {c _ {2}}{3 c _ {3} \sqrt {\theta_ {1}}} \frac {\sqrt {n}}{n _ {s} \sqrt {k}}
$$

The lemma then follows by setting $\begin{array} { r } { c _ { 4 } = \frac { c _ { 2 } } { 3 c _ { 3 } \sqrt { \theta _ { 1 } } } . \quad \varTheta } \end{array}$

Note we assumed that $\begin{array} { r } { k \le \theta _ { 1 } \frac { n } { \log ^ { 2 \alpha + 6 } n } } \end{array}$ and $n _ { s } \ge \theta _ { 2 } n ^ { 1 / 2 + \beta }$ . It is interesting to see if our results still hold for general k.

# 4.2 Capacity of the highway system

We then study the capacity of the highway system for multicast. We begin our analysis on the spanning tree used for multicast constructed by Algorithm 2. For a region R, and $g ( 0 \leq g \leq t - 1 )$ , we first run Algorithm 2 line by line. When we run to line 5 for the $( t - g )$ -th time, for any region R, let $E ( \mathbb { R } , g )$ be the event that there is a node from P that falls in region R. Recall that here $\mathcal { P }$ is the set of nodes representing all connected components (each node for one connected component). We use $\mathbb { D } ( p )$ to denote a small enough region that contains point p, and $D ( p ) = \left| \mathbb { D } ( p ) \right.$ | is the area of $\mathbb { D } ( p )$ . Then we have the following lemma.

LEMMA 12. For any point p in $B _ { n }$ and $0 \leq g \leq t$ , we have

$$
\operatorname * {P r} \{E (\mathbb {D} (p), g) \} \leq \frac {4 ^ {g + 1}}{a ^ {2}} D (p).
$$

PROOF. For $g \leq t - 2 .$ , at line (5) of Algorithm 2, there is at most one representant wireless node in each a2g+1 × ${ \frac { a } { 2 g + 1 } } \times { \frac { a } { 2 g + 1 } }$ 2g+1 cells. Furthermore, we can see if there is a node in a cell s, this node is randomly located in s. i.e, each point in s has the same probability density 1a2/4g+1 $\textstyle { \frac { 1 } { a ^ { 2 } / 4 ^ { g + 1 } } } = { \frac { 4 ^ { g + 1 } } { a ^ { 2 } } }$ 4g+1 a2 to be the node. $\mathrm { S o } ,$ , when $g \leq t - 2$ , for each point $\begin{array} { r } { p , \operatorname* { P r } \{ E ( \mathbb { D } ( p ) , g ) \} \leq \frac { 4 ^ { g + 1 } } { a ^ { 2 } } D ( p ) . } \end{array}$ 4g+1 a2 .

When $g = t - 1$ , since there are k nodes in $\mathcal { P }$ , we have

$$
\operatorname * {P r} \{E (\mathbb {D} (p), g) \} \leq \frac {k}{a ^ {2}} D (p) \leq \frac {4 ^ {t}}{a ^ {2}} D (p) = \frac {4 ^ {g + 1}}{a ^ {2}} D (p).
$$

So, for $0 \leq g \leq t - 1$ , we have $\begin{array} { r } { \operatorname* { P r } \{ E ( \mathbb { D } ( p ) , g ) \} \leq \frac { 4 ^ { g + 1 } } { a ^ { 2 } } D ( p ) } \end{array}$ 4g+1 a2 This finishes the proof.

LEMMA 13. For any region R in $B _ { n }$ and $0 \leq g \leq t - 1$ ,

$$
\boldsymbol {P r} (E (\mathbb {R}, g)) \leq \frac {4 ^ {g + 1}}{a ^ {2}} | \mathbb {R} |
$$

PROOF. The probability is computed by integration: $\operatorname* { P r } \{ E ( \mathbb { R } , g ) \} =$ $\begin{array} { r l } { \oint _ { p \in \mathbb { R } } \mathrm { P r } \{ E ( \mathbb { D } ( p ) , g ) \} \le \oint _ { p \in \mathbb { R } } \frac { 4 ^ { g + 1 } } { a ^ { 2 } } D ( p ) = \frac { 4 ^ { g + 1 } } { a ^ { 2 } } | \mathbb { R } | . } & { { } \bigsqcup } \end{array}$ 4g+1 a2 4g+1 a2

LEMMA 14. In the second phase, the probability that a station is covered by a multicast session is at most $c _ { 5 } \frac { \dot { \sqrt { k } } } { \sqrt { n } }$ when $k \leq$ $\theta _ { 3 } { \frac { n } { \log ^ { 2 } n } }$ θ3 , where $c _ { 5 }$ and $\theta _ { 3 }$ are constants.

PROOF. Considering Algorithm 3, we can see a highway node $v ^ { \ast }$ can be covered by a multicast session in the following two cases.

1. $v ^ { \ast }$ is covered by a horizontal path $E ( q _ { i , x } , q _ { i , y } )$ got by line 8 of Algorithm 3.   
2. v∗ is covered by a horizontal path $E ( q _ { i , x } , q _ { i , y } )$ got by Line 16 of Algorithm 3.

We now study these two cases separately.

Case $\mathbf { 1 } \colon \boldsymbol { v } ^ { * }$ is covered by a horizontal path $E ( q _ { i , x } , q _ { i , y } )$ got by line 8 of Algorithm 3.

In this case, $q _ { i , x }$ must be in the same horizontal highway with $v ^ { \ast } ,$ , say, $\Pi _ { z _ { x } } .$ . It means that $p _ { i , x }$ must be in the $z _ { x } \mathrm { - t h }$ horizontal strip. Thus, the vertical span of $p _ { i , x }$ is h. Consider the value of $g$ at the line 10 of Algorithm 2 when $\overline { { p _ { i , x } p _ { i , y } } }$ is inserted into $E S T$ . We can see both the horizontal and the vertical span of ${ \overline { { p _ { i , x } p _ { i , y } } } } ,$ $d _ { H } ( p _ { i , x } , p _ { i , y } )$ , are at most ${ \frac { a } { 2 ^ { g } } } . \ \mathrm { S o }$ , we will show the upper bound of the vertical span of $p _ { i , x }$ on g. Since $v ^ { * }$ is between $q _ { i , x }$ and $q _ { i , y }$ in the highway, considering the position of $v ^ { * }$ in relation to $q _ { i , x }$ and $q _ { i , y } ,$ there will be 3 subcases: (we suppose the x-coordinate $X ( q _ { i , x } )$ of $q _ { i , x }$ is less than $X ( q _ { i , y } ) )$ )

![](images/f4999c87e22bde9cf056134a7e1bc5bfda0027a429f433428279f7c1bc42085d.jpg)



Case 1

![](images/7b21450acab9c60438111b8901d20515d53e0d67f66a9f4067e9adaaba1d7a78.jpg)



Case 2(1)

![](images/31e2b97f714465e016714e5ffb04c678894a20bec153efe5c852f0d5d1b0876b.jpg)



Case 2(2)

![](images/3cc31a613db9f1f262f555d27772da087baf5952fe69857e441a2c749f0d20fd.jpg)



Case 2(3)   
Figure 7: The cases in which the station ¡ √ ¢ $v ^ { * }$ is covered. In all cases, either $p _ { i , x }$ or $p _ { i , y }$ is bounded in a rectangle with size at most $\begin{array} { r } { h \stackrel { - } { \times } \left( \frac { a } { 2 ^ { g } } + 3 H + \sqrt { 2 } c \right) } \end{array}$ .

$1 . \ X ( v ^ { * } ) \leq X ( q _ { i , x } )$ . Since the highway $\Pi _ { w _ { x } }$ is legal, we have $d _ { H } ( v ^ { * } , q _ { i , x } ) < 2 H$ . Thus $d _ { H } ( v ^ { * } , p _ { i , x } ) \leq d _ { H } ( v ^ { * } , q _ { i , x } ) +$ $d _ { H } ( q _ { i , x } , p _ { i , x } ) \leq 2 H + d _ { H } ( q _ { i , x } , p _ { i , x } )$ .   
2. $X ( q _ { i , x } ) < X ( v ^ { * } ) \leq X ( q _ { i , y } ) .$ . In this case, $d _ { H } ( v ^ { * } , p _ { i , x } ) \leq$ ma $\mathbf { x } \{ d _ { H } ( q _ { i , x } , p _ { i , x } ) , d _ { H } ( q _ { i , y } , p _ { i , x } ) \}$ .   
3. $X ( q _ { i , y } ) < X ( v ^ { * } )$ . Similar with the preceding subcase 1), we have $d _ { H } ( v ^ { * } , p _ { i , x } ) \leq 2 H + d _ { H } ( q _ { i , y } , p _ { i , x } )$ .

In summary, we have

$$
\begin{array}{l} d _ {H} (v ^ {*}, p _ {i, x}) \leq \max \{2 H + d _ {H} (q _ {i, x}, p _ {i, x}), \\ d _ {H} (q _ {i, x}, p _ {i, x}), d _ {H} (q _ {i, y}, p _ {i, x}), \\ \left. 2 H + d _ {H} \left(q _ {i, y}, p _ {i, x}\right) \right\} \\ = 2 H + \max \left\{d _ {H} \left(q _ {i, x}, p _ {i, x}\right), d _ {H} \left(q _ {i, y}, p _ {i, x}\right) \right\}. \\ \end{array}
$$

Note $d _ { H } ( p _ { i , x } , q _ { i , x } ) \leq \sqrt { 2 } c$ , and $d _ { H } ( p _ { i , x } , q _ { i , y } ) \leq d _ { H } ( p _ { i , x } , p _ { i , y } ) +$ $\begin{array} { r } { d _ { H } ( p _ { i , y } , q _ { i , y } ) \leq \frac { a } { 2 ^ { g } } + \sqrt { 2 } c } \end{array}$ . Thus, for a sufficiently large n,

$$
d _ {H} (v ^ {*}, p _ {i, x}) \leq 2 H + \frac {a}{2 ^ {g}} + \sqrt {2} c \leq (2 + \varepsilon) H + \frac {a}{2 ^ {g}}.
$$

Combining the horizontal span and vertical span of ¡ ¢ $p _ { i , x } ,$ we know $p _ { i , x }$ is in a $\begin{array} { r } { { \bf \nabla } . h \times \left( ( 2 + \varepsilon ) H + \frac { a } { 2 g } \right) } \end{array}$ rectangle (see Figure 7, case 1).

Case $\scriptstyle 2 \colon { \boldsymbol { v } } ^ { * }$ is covered by a horizontal path $E ( q _ { i , x } , q _ { i , y } )$ got by Line 16 of Algorithm 3. In this case, the path $E ( q _ { i , x } , q _ { i , y } )$ will contain $q _ { i , x } , \pi _ { z _ { x } , u _ { 1 } } , \phi _ { w _ { x } , u _ { 2 } } , \phi _ { w _ { x } , u _ { 3 } } , \phi _ { z _ { y } , u _ { 4 } } , q _ { i , y }$ in that order.

Considering the position of $v ^ { \ast }$ in this path, there are 3 sub-cases.

Case $2 ( 1 ) : v ^ { * }$ is covered by a horizontal path $E _ { 1 } ( q _ { i , x } , q _ { i , y } )$ got by line 13 of Algorithm 3. Similar with case $1 , p _ { i , x }$ is bounded in the $z _ { x }$ -th horizontal strip. Furthermore.

$$
\begin{array}{l} d _ {H} (v ^ {*}, p _ {i, x}) \leq 2 H + \max \left\{d _ {H} \left(q _ {i, x}, p _ {i, x}\right), d _ {H} \left(\pi_ {z _ {x}, u _ {1}}, p _ {i, x}\right) \right\} \\ \leq 2 H + \max \{\sqrt {2} c, \\ \left. d _ {H} \left(p _ {i, x}, \phi_ {w _ {x}, u _ {2}}\right) + d _ {H} \left(\pi_ {z _ {x}, u _ {1}}, \phi_ {w _ {x}, u _ {2}}\right) \right\} \\ \leq 2 H + H + \sqrt {2} c \leq (3 + \varepsilon) H \\ \end{array}
$$

${ \mathrm { S o } } , p _ { i , x }$ is in a rectangle region with height h and width $( 3 + \varepsilon ) H$ (see Figure 7, case $2 ( 1 ) )$ .

Case $2 ( 2 ) : v ^ { * }$ is covered by a vertical path $E _ { 2 } ( q _ { i , x } , q _ { i , y } )$ got by line 14 of Algorithm 3. In this case, $v ^ { * }$ is on highway $\Phi _ { w _ { x } } ,$ , between $\phi _ { w _ { x } , u _ { 2 } }$ and $\phi _ { w _ { x } , u _ { 3 } }$ . Since $p _ { i , x }$ is on the $w _ { x } .$ -th vertical strip, its vertical span is at most h. In addition, $d _ { V } ( p _ { i , x } , \phi _ { w _ { x } , u _ { 3 } } ) \ \leq$ $\begin{array} { r } { d _ { V } ( p _ { i , x } , p _ { i , y } ) + d _ { V } ( p _ { i , y } , \pi _ { z _ { y } , u _ { 4 } } ) + d _ { V } ( \pi _ { z _ { y } , u _ { 4 } } , \phi _ { w _ { x } , u _ { 3 } } ) \leq \frac { a } { 2 ^ { g } } + } \end{array}$ $H + { \sqrt { 2 } } c$ , and furthermore, $d _ { V } ( p _ { i , x } , \phi _ { w _ { x } , u _ { 2 } } ) \leq d _ { V } ( p _ { i , x } , \pi _ { z _ { x } , u _ { 1 } } ) +$

$d _ { V } ( \pi _ { z _ { x } , u _ { 1 } } , \phi _ { w _ { x } , u _ { 2 } } ) \leq H + \sqrt { 2 } c .$ . Similar with case 1, we have

$$
d _ {V} (p _ {i, x}, v ^ {*})
$$

$$
\leq 2 H + \max \{d _ {V} (p _ {i, x}, \phi_ {w _ {x}, u _ {2}}), d _ {V} (p _ {i, x}, \phi_ {w _ {x}, u _ {3}}) \}
$$

$$
\leq 2 H + \frac {a}{2 ^ {g}} + H + \sqrt {2} c
$$

$$
\leq (3 + \varepsilon) H + \frac {a}{2 ^ {g}} (\text { when   } n \text {   is   large   enough })
$$

${ \mathrm { S o } } , p _ { i , a }$ is in a rectangle region of height h and width $\begin{array} { r } { \left( ( 3 + \varepsilon ) H + \frac { a } { 2 ^ { g } } \right) } \end{array}$ (see Figure 7, case 2(2)).

Case $2 ( 3 ) : ~ v ^ { * }$ is covered by a horizontal path $E _ { 3 } ( q _ { i , x } , q _ { i , y } )$ got by line 15 of Algorithm 3. In this case, $v ^ { * }$ is located in the highway $\Pi _ { z _ { y } }$ . So, $p _ { i , y }$ is bounded in the $z _ { y } .$ -th horizontal strip. Additionally, we have $d _ { H } ( p _ { i , y } , \pi _ { z _ { y } , u _ { 4 } } ) \leq d _ { H } ( \pi _ { z _ { y } , u _ { 4 } } , \phi _ { w _ { x } , u _ { 3 } } ) +$ $\begin{array} { r } { d _ { H } ( \phi _ { w _ { x } , u _ { 3 } } , p _ { i , x } ) + d _ { H } ( p _ { i , x } , p _ { i , y } ) \leq \sqrt { 2 } c + H + \frac { a } { 2 ^ { g } } } \end{array}$ . Also similar with case 1, we have

$$
d _ {H} (p _ {i, y}, v ^ {*})
$$

$$
\leq 2 H + \max \left\{d _ {H} \left(p _ {i, y}, \pi_ {z _ {y}, u _ {4}}\right), d _ {H} \left(p _ {i, y}, q _ {i, y}\right) \right\}
$$

$$
\leq 2 H + \sqrt {2} c + H + \frac {a}{2 ^ {g}}
$$

$$
\leq (3 + \varepsilon) H + \frac {a}{2 ^ {g}} (\text { when   } n \text {   is   large   enough })
$$

Thus, $p _ { i , y }$ is bounded in a rectangle of width $\begin{array} { r } { \left( ( 3 + \varepsilon ) H + \frac { a } { 2 ^ { g } } \right) } \end{array}$ and of height h (see Figure 7, case 2(3)).

In all cases, either $p _ { i , x } \ { \mathrm { o r } } \ p _ { i , y }$ is bounded in a rectangle. For some g, the probability that v∗ is covered by an edge from d is at most $\begin{array} { r } { P _ { g } \overset { ^ { } } { \underset { } {  } } h ( ( 2 + \varepsilon ) H + \frac { a } { 2 ^ { g } } ) \frac { 4 ^ { g + 1 } } { a ^ { 2 } } + h ( 3 + \varepsilon ) H \frac { 4 ^ { g + 1 } } { a ^ { 2 } } + } \end{array}$ ¢ 4g+1 a2 + h(3 + ε)H 4g+1a2 a2 $\begin{array} { r } { h \left( ( 3 + \varepsilon ) H + \frac { a } { 2 ^ { g } } \right) \frac { 4 ^ { g + 1 } } { a ^ { 2 } } + h \left( ( 3 + \varepsilon ) H + \frac { a } { 2 ^ { g } } \right) \frac { 4 ^ { g + 1 } } { a ^ { 2 } } } \end{array}$ 4 g +1 a2 4g +1 a2 , which is ≤ $h \left( 1 2 H + 3 { \frac { a } { 2 ^ { g } } } \right) { \frac { 4 ^ { g + 1 } } { a ^ { 2 } } }$ 4g+1 a2 . Then, consider all $g = 0 , 1 , 2 , \cdots , t - 1$ , the probability that $v ^ { * }$ is covered is at most

$$
\begin{array}{l} p \leq \sum_ {g = 0} ^ {t - 1} P _ {g} \leq \sum_ {g = 0} ^ {t - 1} h \left(1 2 H + 3 \frac {a}{2 ^ {g}}\right) \frac {4 ^ {g + 1}}{a ^ {2}} \\ = 4 8 H h \sum_ {g = 0} ^ {t - 1} \frac {4 ^ {g}}{a ^ {2}} + 1 2 h \sum_ {g = 0} ^ {t - 1} \frac {2 ^ {g}}{a} \leq 4 8 H h \frac {4 ^ {t}}{a ^ {2}} + 1 2 h \frac {2 ^ {t}}{a} \\ \leq 4 8 H h \frac {4 k}{a ^ {2}} + 1 2 h \frac {2 \sqrt {k}}{a} = 1 9 2 H h \frac {k}{a ^ {2}} + 2 4 h \frac {\sqrt {k}}{a} \\ \end{array}
$$

Replacing H with κ log $\frac { \sqrt { n } } { c \sqrt { 2 } } - \epsilon _ { m }$ and a with ${ \sqrt { n } } ,$ we will get

$$
{ p } { \leq } { 1 9 2 \left( \kappa \log \frac { \sqrt { n } } { c \sqrt { 2 } } - \epsilon _ { m } \right) h \frac { k } { n } + 2 4 h \frac { \sqrt { k } } { \sqrt { n } } }
$$

Use the condition ³ $k \leq \theta _ { 3 } \frac { n } { \log ^ { 2 } n }$ , we have, for a sufficient large q $n ,$ $\begin{array} { r } { p \leq 1 9 2 \left( \kappa \log \frac { \sqrt { n } } { c \sqrt { 2 } } - \epsilon _ { m } \right) h \frac { \sqrt { k } } { n } \sqrt { \theta _ { 3 } \frac { n } { \log ^ { 2 } n } } + 2 4 h \frac { \sqrt { k } } { \sqrt { n } } \leq ( 9 6 + } \end{array}$ θ3 nlog2 n + 2 4 h √ k $\begin{array} { r } { \varepsilon _ { 1 } ) \kappa h \sqrt { \theta _ { 3 } } \frac { \sqrt { k } } { \sqrt { n } } + 2 4 h \frac { \sqrt { k } } { \sqrt { n } } \leq ( 9 7 \kappa \sqrt { \theta _ { 3 } } + 2 4 ) h \frac { \sqrt { k } } { \sqrt { n } } } \end{array}$ , where √ $\varepsilon _ { 1 }$ is a constant that satisfies $0 < \varepsilon _ { 1 } \le 1$ . Setting $c _ { 5 } = ( 9 7 \kappa \sqrt { \theta _ { 3 } } + 2 4 ) h$ finishes the proof.

With Lemma 14, the following lemma is straightforward.

LEMMA 15. For any station $v ^ { * }$ , the expected number of multicast sessions that pass $v ^ { \ast }$ is at most c5 $\frac { n _ { s } { \sqrt { k } } } { { \sqrt { n } } }$ , when $\begin{array} { r } { k \leq \theta _ { 3 } \frac { n } { \log ^ { 2 } n } . } \end{array}$ 3 log2

PROOF. Since the $n _ { s }$ multicast sessions are generated independently, multiplying the upper bound of the probability that $v ^ { * }$ is covered by a multicast sessions by $ { n _ { s } }$ will result in the upper bound of the expected number of covering multicast sessions. That is $\begin{array} { r } { c _ { 5 } \frac { \sqrt { k } } { \sqrt { n } } \times n _ { s } = c _ { 5 } \frac { n _ { s } \sqrt { k } } { \sqrt { n } } } \end{array}$ □

The preceding result only shows the probability upper bound that a given node $v ^ { * }$ is used by multicast sessions, when $v ^ { * }$ is given a prior. Next, we use VC theorem (Theorem 25) to give the upper bound of the multicast sessions that pass $v ^ { * }$ for every possible node in the highway system. Recall that, we used $n _ { s }$ sets of k points to generate $n _ { s }$ multicast trees. So, the input space should be the√ family of sets of k points, $\mathrm { i . e , } [ 0 , \sqrt { n } ] ^ { 2 k }$ . To notice that the output $M T$ of Algorithm 3 is fixed for a fixed set of k points, we could set the universal input space U be the set of all possible output multicast trees of Algorithm 3. For each wireless station $v ^ { * } , v ^ { * }$ is either covered or not covered by a tree T in U. For a subset S of $u ,$ , we use $\boldsymbol { \mathcal { T } } _ { S } ( \boldsymbol { v } ^ { * } )$ to denote the set of trees from S that cover $v ^ { \ast }$ . Le t

$$
\mathcal {C} _ {S} = \{\mathcal {T} _ {\mathcal {U}} (v ^ {*}) \mid v ^ {*} \text {   is   a   node   in   the   highway   system } \},
$$

our objective is to compute the VC-dimension of $\mathcal { C } _ { \mathcal { U } }$ . Here, we simply use $\log _ { 2 } n$ as the upper bound of $\operatorname { V C - d } ( \mathcal { C } _ { u } )$ . This upper bound is obvious due to the fact that there is at most n elements in $\mathcal { C } _ { \mathcal { U } }$ . Notice that a careful analysis can show that the VC-dimension $\operatorname { V C - d } ( \mathcal { C } _ { u } )$ is actually of order Θ(log k).

THEOREM 16. With high probability, for every station $v ^ { * }$ , the number of multicast sessions that cover $v ^ { \ast }$ is at most c6 $\frac { n _ { s } { \sqrt { k } } } { { \sqrt { n } } }$ , when $k \leq \theta _ { 3 } \frac { n } { \log ^ { 2 } n }$ and $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \beta }$ , where $c _ { 6 }$ is a constant to be specified and $\beta > 0$ is any positive real number.

PROOF. Recall that in Lemma 14, the probability that a station $v ^ { * }$ is covered by a random multicast session is at most c5 $\frac { \sqrt { k } } { \sqrt { n } }$ Using VC-theorem, we have

$$
\operatorname * {P r} \left(\sup _ {v ^ {*}} \left| \frac {\# \text {   of   sessions   covering   } v ^ {*}}{n _ {s}} - c _ {5} \frac {\sqrt {k}}{\sqrt {n}} \right| <   \epsilon (n)\right) > 1 - \sigma (n)
$$

$$
\mathrm{if} n _ {s} \geq \max \left\{\frac {8 d}{\epsilon (n)} \cdot \log \frac {1 3}{\epsilon (n)}, \frac {4}{\epsilon (n)} \log \frac {2}{\sigma (n)} \right\}
$$

If we set $\begin{array} { r } { \epsilon ( n ) = \frac { \sqrt { k } } { \sqrt { n } } } \end{array}$ and $\textstyle \sigma ( n ) = { \frac { 2 } { n } }$ , we have

$$
\operatorname * {P r} \left(\sup _ {v ^ {*}} (\# \text {   of   sessions   covering   } v ^ {*}) <   (c _ {5} + 1) \frac {n _ {s} \sqrt {k}}{\sqrt {n}}\right) > 1 - \frac {2}{n}
$$

$$
\text {   if   } n _ {s} \geq \max \left\{\frac {8 \sqrt {n} \log n}{\sqrt {k}} \cdot \log \frac {1 3 \sqrt {n}}{\sqrt {k}}, \frac {4 \sqrt {n}}{\sqrt {k}} \log n \right\}
$$

$$
= \frac {8 \sqrt {n} \log n}{\sqrt {k}} \cdot \log \frac {1 3 \sqrt {n}}{\sqrt {k}}
$$

To guarantee the above lower bound for $n _ { s }$ for a large enough $n ,$ it is sufficient that $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \beta }$ for a constant $\beta > 0$ . Let $c _ { 6 } = c _ { 5 } + 1$ and we finish the proof.

LEMMA 17. $W . h . p ,$ the data rate of the second phase in any multicast session is at least $\begin{array} { r } { c _ { 7 } \frac { \sqrt { n } } { n _ { s } \sqrt { k } } , } \end{array}$ 7 n s  k when $n _ { s } ~ \ge ~ \theta _ { 2 } n ^ { 1 / 2 + \beta }$ and k ≤ θ3 nlog2 n . $k \leq \theta _ { 3 } { \frac { n } { \log ^ { 2 } n } }$

PROOF. As the distance between two adjacent highway stations is at most $2 \sqrt { 2 } c$ , we can set $r = 2 \sqrt { 2 } c$ and $R = 4 \bar { \sqrt { 2 } } c$ and apply Lemma 3. We do it in the similar way with the proof of Lemma 7. As there is at most 1 station in a square of size $c \times c ,$ we only need to divide the 2nd phase into $\textstyle { \left( \lceil \frac { R + r } { c } \rceil + 1 \right) ^ { 2 } = 1 0 0 }$ time slots. Then, w.h $\cdot \mathrm { p } ,$ each station can send data to its adjacent stations (on the same highway) at rate at least B log $\begin{array} { r } { \left( 1 + \frac { P \cdot \ell ( 2 \sqrt { 2 } c ) } { N _ { 0 } + c _ { 3 } P ( 2 \sqrt { 2 } c ) ^ { - \alpha } } \right) / 1 0 0 } \end{array}$ which is at least a constant.

In addition, w.h.p, each station in highway system is covered by at most $c _ { 6 } \frac { n _ { s } \sqrt { k } } { \sqrt { n } }$ multicast sessions when k ≤ θ3 nlog2 n . $k \leq \theta _ { 3 } \frac { n } { \log ^ { 2 } n }$ So, the stations of each multicast session can get transmitting rate at least

$$
\begin{array}{l} R _ {2} \geq B \log \left(1 + \frac {P \cdot \ell (2 \sqrt {2} c)}{N _ {0} + c _ {3} P (2 \sqrt {2} c) ^ {- \alpha}}\right) / \left(1 0 0 c _ {6} \frac {n _ {s} \sqrt {k}}{\sqrt {n}}\right) \\ { = } { \frac { B } { 1 0 0 c _ { 6 } } \log \left( 1 + \frac { P \cdot \ell ( 2 \sqrt { 2 } c ) } { N _ { 0 } + c _ { 3 } P ( 2 \sqrt { 2 } c ) ^ { - \alpha } } \right) \frac { \sqrt { n } } { n _ { s } \sqrt { k } } } \\ \end{array}
$$

${ \mathrm { S o } } ,$ if letting $\begin{array} { r } { c _ { 7 } = \frac { B } { 1 0 0 c _ { 6 } } \log \left( 1 + \frac { P \cdot \ell ( 2 \sqrt { 2 } c ) } { N _ { 0 } + c _ { 3 } P ( 2 \sqrt { 2 } c ) ^ { - \alpha } } \right) } \end{array}$ 100c6 , we get the result we need.

# 4.3 Per-flow multicast capacity of the system

By combining the data rate in the two phases, we have

THEOREM 18. If k ≤ θ1 nlog2α+6 n $\begin{array} { r } { I f k \le \theta _ { 1 } \frac { n } { \log ^ { 2 \alpha + 6 } n } } \end{array}$ and $n _ { s } \geq \theta _ { 2 } n ^ { 1 / 2 + \beta }$ , w.h.p., the per-flow multicast rate is at least $\displaystyle c _ { 8 } \frac { \sqrt { n } } { n _ { s } \sqrt { k } }$ 8 n s k n , where $\begin{array} { r } { c _ { 8 } = \frac { 1 } { 2 } \operatorname* { m i n } \{ c _ { 4 } , c _ { 7 } \} } \end{array}$ .

PROOF. When $\begin{array} { r } { k \leq \theta _ { 1 } \frac { n } { \log ^ { 2 \alpha + 6 } n } } \end{array}$ , it is sufficient that $k \leq \theta _ { 3 } \frac { n } { \log ^ { 2 } n }$ for large n. Then both Lemma 11 and Lemma 17 are applicable. We assign the two phases the same amount of time and thus the achievable per-flow date rate is $\frac { 1 } { 2 }$ min $\begin{array} { r } { \left\{ c _ { 4 } , c _ { 7 } \right\} \frac { \sqrt { n } } { n _ { s } \sqrt { k } } = c _ { 8 } \frac { \sqrt { n } } { n _ { s } \sqrt { k } } , } \end{array}$ n s  k 8 n s  k

# 5. UPPERBOUND ON UNICAST CAPACITY

It has been shown in [3] that the asymptotic per-flow unicast capacity under Gaussian channel model is $\mathrm { \Omega } \mathrm { \Omega } \mathrm { \Omega } \mathrm { \Omega } \mathrm { \bar {Omega } } \mathrm { \Omega } \mathrm { \Omega } \mathrm { \Omega }$ when a square $B _ { n }$ contains a number of nodes following Poisson distribution with rate 1. We here show that the per-flow unicast capacity is at most $O ( 1 / \sqrt { n } )$ in this setting.

The basic idea of the proof is as follows. We partition the region into grids of cells of side-length c (value of c depending on p and $c _ { 0 } )$ such that, the probability that a cell contains at most $c _ { 0 }$ nodes is at least $p .$ Here $p > 5 / 6$ and $c _ { 0 } > 1$ are constants. We say a cell is quasi-closed if it contains at most $c _ { 0 }$ nodes. We call a path of cells quasi-closed cut if it contains only quasi-closed cells and crosses from left to right side of square $B _ { n }$ . Furthermore, we define the length of a quasi-closed cut as the total number of cells it contains.

As shown in [3], for all $k \ > \ 0$ and $\frac { 5 } { 6 } ~ < ~ p ~ < ~ 1$ with $2 +$ $k \log ( 6 ( 1 - p ) ) < 0$ , there exists a number of disjoint groups containing at least dδ log me disjoint paths in every group, and each group is constraint in a stripe of size $m \times ( k \log m - \epsilon _ { m } )$ , for $\delta$ small enough and δ log $\begin{array} { r } { \frac { p } { 1 - p } + 1 + k \log ( 6 ( 1 - p ) ) < 1 , m = \frac { \sqrt { n } } { c \sqrt { 2 } } } \end{array}$ √n c 2 and a non-zero small $\epsilon _ { m }$ such that the side length of each stripe is integer. When k is some appropriate constant, the number of groups is mk log m−²m $\frac { m } { k \log m - \epsilon _ { m } } > n ^ { 1 / 3 }$ when n is large enough. Then by pigeonhole principle, it is easy to show the following

LEMMA 19. Assume that dδ log me disjoint paths (formed by quasi-closed cells) inside a stripe of length m-cells and width (k log m− $\epsilon _ { m } ) { - } c e l l s$ . There exists a quasi-closed cut whose length is at most $c _ { 9 } { \sqrt { n } } .$ for some constant $\begin{array} { r } { c _ { 9 } = \frac { k } { \delta c \sqrt { 2 } } } \end{array}$ .

We call such cut in the middle group as $\mathbb { C } .$ . It is easy to show that the expected number of unicast flows that will cross this cut C (with end nodes on different sides of C) is at least $n _ { s } / 9$ , and thus, with high probability, the number of unicast flows that will cross $\mathbb { C }$ is at least $n _ { s } / 1 8$ . This implies that, by pigeonhole principle, there exists a cell in C that will be crossed by at least $\frac { n _ { s } } { 1 8 c _ { 9 } \sqrt { n } }$ unicast flows. Since the cell has only a constant number of nodes, the longest link needed to cross such special cell is at least a constant value $\varrho .$ Thus, the data rate that can be supported by this special link is at most a constant. Thus, we have (whose detailed proofs are omitted due to space limit)

THEOREM 20. The asymptotic per-flow unicast capacity of $n _ { s }$ flows in a large scale random network with n nodes randomly distributed in a square $B _ { n } ,$ , with high probability, is at most $O ( \sqrt { n } / n _ { s } )$ when $n _ { s }$ is large enough.

# 6. LITERATURE REVIEWS

The ground-breaking work by Gupta and Kumar [7] studied the asymptotic unicast capacity of a multi-hop wireless networks for two different models. When each wireless node is capable of transmitting at W bits per second using a constant transmission range, the throughput obtainable by each node for a randomly chosen destination is ${ \dot { \Theta } } ( { \frac { W } { \sqrt { n \log n } } } )$ ( √ n log n ) bits per second under PrIM. If nodes are optimally placed and transmission range is optimally chosen, even under optimal circumstances, the throughput is only $\Theta \big ( \textstyle { \frac { W } { \sqrt { n } } } \big )$ bits per second for each node. Similar results also hold for PhIM Kulkarni and Viswanath [12] obtained a stronger (almost sure) version of√ the $\sqrt { n \log n }$ throughput for random node locations in a fixed area obtained in [7].

Grossglauser and Tse [6] showed that mobility actually can help to improve the unicast capacity if we allow arbitrary large delay. Their main result shows that the average long-term throughput per source-destination pair can be kept constant even as the number of nodes per unit area increases. Notice that this is in sharp contrast to the fixed network scenario (when nodes are static after random deployment). In summary, for random networks, under the protocol model, the achievable per-flow throughput capacity $\lambda ( n )$ and the average travel distance L satisfies $\begin{array} { r } { \lambda ( \bar { n } ) \cdot \bar { L } \overset { \cdot } { \leq } \Theta \overset { \cdot } { \left( \frac { W } { \Delta ^ { 2 } n \cdot r ( n ) } \right) } } \end{array}$ . Similar phenomenon has also been observed in [13]. Gastpar and Vetterli [5] study the capacity of random networks using relay. Chuah et al. [2] studied the capacity scaling in MIMO wireless systems under correlated fading. Vu et al. [21] studied the scaling laws of cognitive networks. Liu et al. [15] studied the capacity of a wireless ad hoc network with infrastructure. Another stream of work (e.g. [17]) has proposed progressively refined multi-user cooperative schemes, which have been shown to significantly outperform multi-hop communication in many environments. Bounds for the capacity of wireless multihop networks imposed by topology and demand were studied in [11]. Their techniques can be used to study unicast, broadcast and multicast capacity. Bhandari and Vaidya [1] studied the unicast capacity of multi-channel wireless networks with random $( c , f )$ assignment. Garetto et al. [4] studied the capacity scaling in delay tolerant networks with heterogeneous mobile devices. Their methodology allows to identify the scaling laws for a general class of mobile wireless networks, and to precisely determine under which conditions the mobility of nodes can indeed be exploited to increase the per-node throughput.

Broadcast capacity of an arbitrary network has been studied in [9, 20]. They essentially show that, under fPrIM, the broadcast capacity is Θ(W ) for single source broadcast and the achievable broadcast capacity per flow in any network is only $\Theta ( W / n )$ if each of the n nodes will serve as source node. This capacity bounds also apply to random networks. Keshavarz-Haddad et al. [10] studied the broadcast capacity with dynamic power adjustment for physical interference model. Zheng [23] studied the data dissemination capacity in power-constrained networks: w.h.p., the total broadcast capacity is $\bar { P } { \cdot } \Theta ( ( \log n ) ^ { - \alpha / 2 } )$ when each node transmits at a power $P$ in the Gaussian channel model.

Multicast capacity was also recently studied in the literature. Jacquet and Rodolakis [8] studied the scaling properties of multicast for random wireless networks. They briefly claimed that the maximum rate at which a node can transmit multicast data is $O ( { \frac { W } { { \sqrt { k n \log n } } } } )$ . Recently, rigorous proofs of the multicast capacity were given in [14, 19]. Li et al. [14] studied the multicast capacity of the following random networks: n wireless nodes are randomly deployed in a square region with side-length a and each wireless node can transmit/receive at $W$ bits/second over a common wireless channel. They proved that, in fPrIM, the per-flow multicast capacity (of n multicast flows, each flow with k receivers) is $\Theta ( { \sqrt { \frac { 1 } { n \log n } } } \cdot { \frac { W } { \sqrt { k } } } )$ when $\begin{array} { r } { k = O ( \frac { n } { \log n } ) } \end{array}$ ; the per-flow multicast capacity is $\Theta ( W / n )$ when $\begin{array} { r } { k = \Omega ( \frac { n } { \log n } ) } \end{array}$ . Shakkottai et al. [19] log n studied the multicast capacity of random networks when the number of multicast sources is $n ^ { \epsilon }$ for some $\epsilon > 0$ , and the number of receivers per multicast flow is $n ^ { 1 - \epsilon }$ . Recently, Mao et al. [16] studied the multicast capacity for hybrid networks. They derived several capacity regimes based on the relations of the number k of receivers per multicast session, the total number n of nodes, and the number m of base stations.

These results $[ 6 - 1 0 , 1 4 , 1 9 , 2 0 ]$ for the network capacity of random networks all assumed that the data rate supported by each communication link is a constant $W { \mathrm { - } } { \mathsf { b p s } }$ (using PrIM, fPrIM, or PhIM interference models). Using percolation theorem, multihop transmission, pairwise coding and decoding at each hop, and a TDMA scheme, Franceschetti et al. [3] shows that a rate $1 / \sqrt { n }$ is achievable in networks of randomly located nodes (not only some arbitrarily placed nodes) when Gaussian channel is used.

# 7. CONCLUSION

In this paper, we studied the multicast capacity of randomly placed wireless nodes in $B _ { n }$ under Gaussian model, in which nodes can transmit data over large distance and the rates of the transmission are determined by SINR. Nodes transmit at constant power $P ,$ and the power attenuates according to the power decay law with exponent $\alpha \ > \ 2$ . We assume that these nodes are randomly located in Poisson distribution of rate 1 in a square $B _ { n }$ with sidelength ${ \sqrt { n } } ;$ there are $n _ { s }$ multicast flows, each flow has k receivers, and the sources and targets of the $n _ { s }$ sessions are chosen by repeating $n _ { \varepsilon }$ times the process (Algorithm 1). We show that, when $\begin{array} { r } { \bar { k } \le \bar { \theta _ { 1 } } \frac { n } { ( \log n ) ^ { 2 \alpha + 6 } } } \end{array}$ and $n _ { s } \geq \theta _ { 2 } \overline { { n } } ^ { 1 / 2 + \beta }$ for some constants $\theta _ { 1 } , \theta _ { 2 }$ and any positive real number $\beta ,$ , with high probability, each multicast source node can send data to all its intended receivers with rate at least $\displaystyle c _ { 8 } \frac { \sqrt { n } } { n _ { s } \sqrt { k } }$ where $c _ { 8 }$ is a constant depending on attenuation α, bandwidth B, and background noise $N _ { 0 }$ . We also present a matching upperbound $O ( 1 / \sqrt { n } )$ for per-flow unicast capacity under Gaussian channel.

A number of interesting questions remain open. The first question is to derive an upper bound on the per-flow multicast capacity jecture that it is also O using the Gaussian channel model for arbitrary k and n. We con- $\begin{array} { r } { O \big ( \frac { \sqrt { n } } { n _ { s } \sqrt { k } } \big ) } \end{array}$ ( √nns√k ). The second question is to derive tight upper bound and lower bound on the network capacity when k could be any arbitrary value from 2 to n. The results presented here only hold when $\begin{array} { r } { k = O ( \frac { n } { ( \log n ) ^ { 2 \alpha + 6 } } ) } \end{array}$ ( n(log n)2α+6 ). We conjecture that

CONJECTURE 21. When k is $\Omega ( \frac { n } { ( \log n ) ^ { d } } )$ ( n(log n)d ), under Gaussian channel model, the per-flow multicast capacity $\textstyle i s \Theta \big ( \frac { 1 } { n _ { s } ( \log n ) ^ { \alpha / 2 } } \big ) , f o r$ ( ns(log n)α/2 ), for some positive constant d $\leq 2 \alpha + 6 .$ .

Notice that, the above conjecture was proved to be true for broadcast (i.e. k = n) [24] under Gaussian channel model. Their proof is to essentially study the longest edge length of the Euclidean minimum spanning tree, which is asymptotically log n when n nodes are randomly placed in a square $B _ { n }$ from [18]. A sufficient condition for the correctness of our conjecture is the correctness of the following conjecture:

CONJECTURE 22. The longest edge of a Steiner spanning tree, which spans k nodes randomly chosen from n nodes randomly placed in $B _ { n }$ , is of order log n, when k is large enough, say $\Omega { \bigl ( } { \frac { n } { \log n } } { \bigr ) }$ .

The third question is to study the capacity when the receiving terminals in a multicast group are within certain region (e.g., a disk with a radius $b ,$ or a square with a side-length b). Finally, we point out that the problem of optimizing the multicast throughput of a given arbitrary network by choosing best routing protocol, and optimizing the hidden constant in our formulas remains open.

# 8. REFERENCES

[1] BHANDARI, V., AND VAIDYA, N. H. Capacity of multi-channel wireless networks with random (c, f) assignment. In MobiHoc ’07 (2007), pp. 229–238.   
[2] CHUAH, C.-N., TSE, D. N. C., KAHN, J. M., AND VALENZUELA, R. A. Capacity scaling in MIMO wireless systems under correlated fading. In IEEE Transactions ON Information Theory (March 2002), vol. 48.   
[3] FRANCESCHETTI, M., DOUSSE, O., N.C.TSE, D., AND THIRAN, P. Closing the gap in the capacity of wireless networks via percolation theory. In IEEE Transactions ON Information Theory (2007),   
[4] GARETTO, M., GIACCONE, P., AND LEONARDI, E. Capacity scaling in delay tolerant networks with heterogeneous mobile nodes. In ACM MobiHoc (2007), pp. 41–50.   
[5] GASTPAR, M., AND VETTERLI, M. On the capacity of wireless networks: the relay case. In IEEE INFOCOM (2002).   
[6] GROSSGLAUSER, M., AND TSE, D. Mobility increases the capacity of ad hoc wireless networks. IEEE/ACM Transactions on Networking (ToN) 10, 4 (2002), 477–486.   
[7] GUPTA, P., AND KUMAR, P. Capacity of wireless networks. IEEE Transactions on Information Theory IT-46 (1999), 388–404.   
[8] JACQUET, P., AND RODOLAKIS, G. Multicast scaling properties in massively dense ad hoc networks. In ICPADS ’05: Proceedings of the 11th IEEE International Conference on Parallel and Distributed Systems (2005), pp. 93–99.   
[9] KESHAVARZ-HADDAD, A., RIBEIRO, V., AND RIEDI, R. Broadcast capacity in multihop wireless networks. In ACM MobiCom ’06 (2006), pp. 239–250.   
[10] KESHAVARZ-HADDAD, A., AND RIEDI, R. On the broadcast capacity of multihop wireless networks: Interplay of power, density and interference. In 4th IEEE SECON (2007).   
[11] KESHAVARZ-HADDAD, A., AND RIEDI, R. H. Bounds for the capacity of wireless multihop networks imposed by topology and demand. In ACM MobiHoc ’07 (2007), pp. 256–265.   
[12] KULKARNI, S., AND VISWANATH, P. A deterministic approach to throughput scaling in wireless networks. IEEE Transactions on Information Theory, 50, 6 (2004), 1041–1049.   
[13] LI, J., BLAKE, C., COUTO, D. S. J. D., LEE, H. I., AND MORRIS, R. Capacity of ad hoc wireless networks. In ACM MobiCom (2001).   
[14] LI, X.-Y., TANG, S.-J., AND OPHIR, F. Multicast capacity for large scale wireless ad hoc networks. In ACM Mobicom (2007).

[15] LIU, B., AND TOWSLEY, D. Capacity of a wireless ad hoc network with infrastructure. ACM MobiHoc (2007), 239–246.   
[16] MAO, X., LI, X.-Y., AND TANG, S.-J. Multicast capacity for hybrid wireless networks. In ACM MobiHoc (2008).   
[17] O¨ ZGU¨ R, A., LE´ VEˆ QUE, O., AND TSE, D. Hierarchical Cooperation Achieves Optimal Capacity Scaling in Ad Hoc Networks. Information Theory, IEEE Transactions on 53, 10 (2007), 3549–3572.   
[18] PENROSE, M. The random minimal spanning tree in high dimensions. Annals of Probability 24 (1996), 1903–1925.   
[19] SHAKKOTTAI, S., LIU, X., AND SRIKANT, R. The multicast capacity of ad hoc networks. In Proc. ACM Mobihoc (2007).   
[20] TAVLI, B. Broadcast capacity of wireless networks. IEEE Communication Letters 10, 2 (February 2006).   
[21] VU, M., DEVROYE, N., SHARIF, M., AND TAROKH, V. Scaling Laws of Cognitive Networks. Submitted to IEEE Journal on Selected Topics in Signal Processing, June (2007).   
[22] XIE, L., AND KUMAR, P. A network information theory for wireless communication: scaling laws and optimal operation. Information Theory, IEEE Transactions on 50, 5 (2004), 748–767.   
[23] ZHENG, R. Information dissemination in power-constrained wireless networks. In IEEE INFOCOM (2006).   
[24] ZHENG, R. Information Dissemination in Power-Constrained Wireless Networks. IEEE Transaction on Wireless Communication 6, 12 (2007).

# 9. APPENDIX

# 9.1 Percolation Theory Result( [3])

Consider a square lattice $B _ { m }$ with side length m. We declare each edge of the square grid open with probability p and closed otherwise, independently of all other edges.

For any given $\kappa > 0 ,$ let us partition $B _ { m }$ into rectangles $R _ { m } ^ { i }$ of sides $m \times \left( \kappa \log m - \epsilon _ { m } \right)$ . We choose $\epsilon _ { m } >$ 0 as the smallest value such that the number of rectangles mκ log m−²m $\frac { m } { \kappa \log m - \epsilon _ { m } }$ in the partition is an integer. It is easy to see that $\epsilon _ { m } = o ( 1 )$ as $m  \infty$ . We let $C _ { m } ^ { i }$ be the maximal number of edge-disjoint left to right crossings of rectangle $R _ { m } ^ { i }$ and let $N _ { m } = \operatorname* { m i n } _ { i } C _ { m } ^ { i }$ . The result is the following.

THEOREM 23. ( [3]) For all $\kappa > 0$ and $\begin{array} { r } { \frac { 5 } { 6 } < p < 1 } \end{array}$ satisfying $2 + \kappa \log ( 6 ( 1 - p ) ) < 0$ , there exists a $\delta ( \kappa , \tilde { p } ) > 0$ such that

$$
\lim _ {m \to \infty} P _ {p} (N _ {m} \leq \delta \log m) = 0
$$

# 9.2 Legalize the highways

Theorem 6: If we find a set of M horizontal highways and M vertical highways using the above method, we can find a set of M legal horizontal highways and M legal vertical highways.

PROOF. We prove it by legalizing these 2M paths.

In the first step, we adjust the horizontal highways, so that any two horizontal highways do not cross each other. As we can see, only the horizontal highways from the same rectangle may cross. If in a rectangle, two highways $P _ { i }$ and $P _ { j }$ across in segments $\overline { { \pi _ { i , k } \pi _ { i , k + 1 } } }$ and $\overline { { \pi _ { j , l } \pi _ { i , l + 1 } } } .$ , we can break the two highway segments and then build two new highway segments $\overline { { \pi _ { i , k } \pi _ { j , l + 1 } } }$ and $\overline { { \pi _ { j , l } \pi _ { i , k + 1 } } }$ . We could see, there are still L highways in the rectangle, but the total length of these L highways is reduced. We repeatedly check whether there are crossing highway segments and break the segments if there are. Since we can not endlessly reduce the total length, at the end of the procedure there are no crossing segments.

Likewise, we can do the same thing with the vertical highways. At the end of the first step, we get a set of M node-disjoint and mutual non-crossing horizontal highways as well as M node-disjoint and mutual non-crossing vertical highways.

In the second step, we try to legalize all the highways. An intuition about a legal highway is that it will never go backward too far, say 2H along the coordinate direction.

It seems impossible to legalize a horizontal highway if only a set of M horizontal highways is considered. However, if we take the M vertical highways into account, the goal is achievable. Be aware of that, the M vertical highways are well distributed : each rectangle with width H has L vertical highways.

We try to explain why we can legalize a horizontal highway. For a illegal horizontal highway, it must traverse a vertical rectangle $R _ { i } ^ { \prime }$ backwardly. As there are L vertical highways in $R _ { i } ^ { \prime } .$ , we could find a ”shortcut” to reduce the backward interval (notice that a horizontal highway and a vertical highway can share stations). We can do so if we do not result in two horizontal highways sharing a same station. Luckily, we have L vertical highways and we can always legalize the highway while keep all horizontal highways node-disjoint.

To present our method, we consider a illegal horizontal highway Πi. As what we have shown, it must go backward at least 2H and thus horizontally traverse at least 1 vertical rectangle R. Let b be the intersecting point of the backward interval of Πi and $L _ { l } ,$ where $L _ { l }$ is the left side of R. Let a be the last intersecting point before b of Πi and Ll(see Figure 8). We consider all the cross points of horizontal highways and $L _ { l }$ between a and b, inclusive. We mark these points from up to bottom(we suppose b is under a) with $p _ { 0 } , p _ { 1 } , \cdots , p _ { t - 1 }$ . It is easy to check that $p _ { 0 } = a , p _ { t - 1 } = b$ and t is even. These t points are comprised of $t / 2$ pairs of points, with $t / 2$ highway intervals connect each pair. Since no two horizontal highways cross each other, there are two kinds of relationship between two highway intervals. Either a highway interval is ”inside” another highway interval, or two highway intervals totally exclude each other. A highway interval is 1-level if no highway intervals are inside it. A highway interval is 2-level if it is not 1-level and no highway intervals other than 1-level highway intervals are inside it. Similarly, we call a highway interval is k-level, if it is not 1-level, 2-level, · · · , k − 1-level, and no highway intervals other than 1-level, 2-level, · · · , k − 1-level highway intervals are inside it.

Figure 8 is a example where $t = 8 ,$ .

![](images/8ee408471aad6dc780bf71f09a6c295e3866fc3eab80ddb8c91db49c2b09560e.jpg)



Figure 8: A example of highway intervals when $t = 8 .$ There are 4 highway intervals, among which there are 2 1-level intervals, 1 2-level interval and 1 3-level interval.

To notice that L vertical highways inside R do not cross each other, we can sort them from left to right. Suppose the L highways are $\Phi _ { j L + 1 } , \Phi _ { j L + 2 } , \Phi _ { j L + 3 } , \cdot \cdot \cdot , \Phi j L + L$ from left to right. We could rebuild these $t / 2$ highway intervals without changing the endpoint of them such that for any $0 \ < \ k \ \le \ t / 2$ , and for any $k < l \leq L$ , no k-level highway intervals cross with $\Phi _ { j L + l }$ .

We can do this simply by rebuilding the intervals from low level to high level. Suppose we are now rebuilding the k-level highway intervals, and all the highway intervals with low levels are rebuilt correctly. The highway $\Phi _ { j L + k }$ intersects with the k-level highway intervals and divide them into two parts : the part on the left side of the $\Phi _ { j L + k }$ and the part on the right side of $\Phi _ { j L _ { k } }$ . Here, ”left” and ”right” are from the topological view. We keep the left side of these highway intervals, while replace the right side with the highway intervals on $\Phi _ { j L + k }$ . Then the resulted horizontal highway intervals does not cross with any vertical highway $\Phi _ { j L + l }$ for $l > k . ( \mathrm { S e e }$ Figure 9).

![](images/f9134e11cff8d2386bf518ef4d1d78dd32f025e91bd7d1a32042b85697f5ab97.jpg)



(a) a highway system

![](images/c110208805b7266f3d7df82048ad5fd4ee44646824960165133c7fe0f10ec21a.jpg)



(b)legalized highway system   
Figure 9: (a) the red line and the blue line are horizontal highway intervals, while the green line and the cyan line are intervals of two vertical highways. (b) the resulted horizontal highway intervals after we legalize the red highway interval.

At the end, we could see that the resulted intervals are all on the left side of $\Phi _ { j L + t / 2 } ,$ which is or is at left side of $\Phi _ { j L + L }$ . Therefore, the resulted intervals will not cross with the right side of R.

By repeatedly checking the legality of horizontal highways(vertical highways similarly), finally, we could build a highway network system where all highways are legal.

# 9.3 Chernoff bound and VC-theorem

LEMMA 24. Let X be a Poisson random variable of rate λ.

$$
\operatorname * {P r} (X \geq x) \leq \frac {e ^ {- \lambda} (e \lambda) ^ {x}}{x ^ {x}}, f o r x > \lambda \tag {1}
$$

Let U be the input space. Let C be a family of subsets of U . A finite set S (called sample in machine learning) is shattered by C, if for every subset B of S, there exists a set $A \in { \mathcal { C } }$ such that $A \cap S = B$ .

The VC-dimension of C, denoted by VC-d(C), is defined as the maximum value d such that there exists a set S with cardinality d that can be shattered by C. For sets of finite VC-dimension, one has uniform convergence ini the weak law of large numbers:

THEOREM 25 (THE VAPNIK-CHERVONENKIS THEOREM). If C is a set of finite VC-dimension ${ \mathrm { V C } } { \mathrm { - d } } ( { \mathcal { C } } )$ , and $\{ X _ { i } \mid i = 1 , 2 \cdot \cdot \cdot , N \}$ is a sequence of i.i.d. random variables with common probability distribution P , then for every $\epsilon , \delta > 0$ ,

$$
\boldsymbol {P r} \left(\sup _ {A \in \mathcal {C}} \left| \frac {\sum_ {i = 1} ^ {N} I (X _ {i} \in A)}{N} - \operatorname * {P r} (A) \right| \leq \epsilon\right) > 1 - \delta \tag {2}
$$

$$
\text { whenever } N > \max \left\{\frac {8 \cdot \mathrm{VC-d} (\mathcal {C})}{\epsilon} \cdot \log \frac {1 3}{\epsilon}, \frac {4}{\epsilon} \log \frac {2}{\delta} \right\}. \tag {3}
$$

Here $I ( X _ { i } \in A )$ takes value 1 if Xi ∈ A and 0 otherwise.