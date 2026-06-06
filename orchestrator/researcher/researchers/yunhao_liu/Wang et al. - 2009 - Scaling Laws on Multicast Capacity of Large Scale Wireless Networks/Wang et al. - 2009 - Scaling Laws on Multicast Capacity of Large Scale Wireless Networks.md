# Scaling Laws on Multicast Capacity of Large Scale Wireless Networks

Cheng Wang∗, Xiang-Yang Li†, Changjun Jiang∗, Shaojie Tang†, Yunhao Liu‡ and Jizhong Zhao§

∗ Department of Computer Science and Technology, Tongji University, Shanghai, China

† Department of Computer Science, Illinois Institute of Technology, Chicago, IL, 60616

‡ Department of Computer Science and Engineering, Hong Kong University of Science and Technology

§ Department of Computer Science and Technology, Xi’an Jiaotong University, Xi’an, China

Abstract—In this paper, we focus on the networking-theoretic multicast capacity for both random extended networks (REN) and random dense networks (RDN) under Gaussian Channel model, when all nodes are individually power-constrained. During the transmission, the power decays along path with the attenuation exponent $\alpha > 2 .$ In REN and RDN, n nodes are randomly 2distributed in the square region with side-length $\sqrt { n }$ and , respectively. We randomly choose $n _ { s }$ 1nodes as the sources of multicast sessions, and for each source v, we pick uniformly at random $n _ { d }$ nodes as the destination nodes. Based on percolation theory, we propose multicast schemes and analyze the achievable throughput by considering all possible values of $n _ { s }$ and $n _ { d } .$ As a special case of our results, we show that for $n _ { s } = \Theta ( n )$ , the per-session multicast capacity of RDN is $O ( { \frac { n } { ( \log n ) ^ { 3 } } } )$ n 3 and is $\Theta \left( { \textstyle { \frac { 1 } { n } } } \right)$ when $\begin{array} { r } { n _ { d } \ = \ \Omega ( \frac { n } { \log n } ) ; } \end{array}$ $\Theta \big ( \frac { 1 } { \sqrt { n _ { d } n } } \big )$ 1√ndn ) = the per-session = Θ(when $n _ { d } =$ ( (log ) ) Θ( )multicast capacity of REN is α $\Theta \big ( \textstyle \frac { 1 } { \sqrt { n _ { d } n } } \big )$ Ω( log) when $\begin{array} { r } { n _ { d } = O \big ( \frac { n } { ( \log n ) ^ { \alpha + 1 } } \big ) } \end{array}$ n α + 1 and is $\Theta \big ( { \textstyle { \frac { 1 } { n _ { d } } } } \cdot ( \log n ) ^ { - { \frac { \alpha } { 2 } } } \big )$ Θ(when $\begin{array} { r } { n _ { d } = \Omega \big ( \frac { n } { \log n } \big ) } \end{array}$ .

Θ( (log ) ) = Ω( log )Index Terms—Multicast Capacity, Percolation, Wireless ad hoc networks, Random networks, Achievable throughput

# I. INTRODUCTION

The problem of asymptotic scalability of capacity for wireless networks has received much attention recently, especially after the pioneer work by Gupta and Kumar [1]. They defined two types of networks: arbitrary networks and random networks. For random networks, two typical network models, extended networks and dense networks were studied in the literature. Most of the succeeding network capacity results follow those network models, and they differ from each other because of the diversity of analytical models and assumptions to be used. There are generally two levels of capacity bounds. The first level is information-theoretic bounds that are obtained by allowing arbitrary (physical layer) cooperative relay strategies [2]. The issue was first addressed by Xie and Kumar [3]. The second is networking-theoretic bounds in which we assume that the signals received from nodes other than one particular transmitter are interference to a receiver, degrading the communication link. For networking-theoretical capacity bounds, there are in general three types of channel models used. The first is the threshold-based channel model under which if the value of a given conditional expression is beyond a threshold, the transmitter can send successfully to the receiver at a specific constant data rate; otherwise, it can not send any. The protocol interference model (PrIM) and physical interference model (PhIM) defined in [1] both belong to the threshold-based channel model. The second is the probability-based channel model used in [4] under which the receiver can receive packets at a specific rate successfully if the probability that SINR is below the threshold is less than a certain value. The third is the rate-based channel model that determines the transmission rate at which the transmitter can send its data to the receiver reliably, based on a continuous function of the receiver’s SINR. Generally, any communication pairs $v _ { i }$ and $v _ { j }$ can establish a direct communication link, over a channel of bandwidth $B ,$ of rate $R ( v _ { i } , v _ { j } ) = B \log ( 1 + ( 1 / \eta ) \mathrm { S I N R } ( v _ { j } ) )$ . When $\eta > 1$ , the ( ) = log(1 + (1 ) ( )) 1receiver can achieve the maximum rate that meets a given BER requirement under a specific modulation and coding scheme. When $\eta = 1$ , the receiver achieves Shannon’s capacity for = 1a wireless channel with additive Gaussian white noise, [5], [6]. For this case, rate-based channel model can be called Gaussian channel model.

In this paper, we study the networking-theoretic multicast capacity for both random extended networks (REN) and random dense networks (RDN) under Gaussian Channel model. We present both improved lower bound and improved upper bound on multicast capacity, compared with previous literatures. See Section III for our main results. As we know, unicast and broadcast can be regarded as two specific cases of multicast corresponding to the case $n _ { d } = 1$ and $n _ { d } = n - 1$ , respectively, where $n _ { d }$ = 1 = 1is the number of destinations for each multicast session. Some existing results can be derived by our result as the specific cases, such as [2], [7]–[9].

For studying the lower bound of multicast capacity, we design two types of multicast schemes for REN and RDN. In one type of scheme, we construct the routing based on percolation theory and schedule respectively short-hops and long-hops. In the other type, we construct the routing without using the percolation theory in order to avoid the bottleneck on the accessing path into highways [7]. Combining with the two types of schemes, we obtain the achievable throughput as the lower bounds of multicast capacity. A characteristics of this paper is that we take account of all cases of $n _ { s }$ and $n _ { d } ,$ without any assumption of $n _ { s }$ and $n _ { d }$ as in most other literatures, which contributes to the generality of the paper. Our lower bounds on multicast capacity improve the previously best known results. We design our routing and schedule schemes based on several innovative techniques: using both backbone highway system and second highway systems based on percolation theory, and parallel scheduling of nearby links. Using second highway systems and parallel scheduling of nearby links, to the best of our knowledge, are not used in previous studies.

On the other hand, using new analyzing techniques, we derive upper bounds on multicast capacity of REN. Our upper bounds also rely on several new techniques. Two different approaches are proposed in the paper to study the upper bound. The first approach partitions the region into cells with constant side length and we show that some of these cells will have large load, regardless of the routing and scheduling schemes. The second approach is to study the bottleneck on some links. We show that there exist some special links that will be used by many multicast sessions (thus high load) and its own data rate is relatively small, thus, implying an upper bound on persession multicast capacity.

The rest of the paper is structured as follows. In Section II, we introduce the network model. Main results are presented in Section III. We design the multicast schemes and analyze the achievable throughput for random extended networks and random dense networks respectively in Section IV and Section V. In Section VI, we discuss the upper bound of the multicast capacity. In Section VII, we present a review of existing results on the capacity scaling of multihop wireless networks. In Section VIII, we conclude the paper.

# II. NETWORK MODEL

We focus on two typical random networks, i.e., the random extended network (REN) and random dense network (RDN). We construct the former by placing nodes according to a Poisson point process (p.p.p.) of unit intensity on the square $\mathcal { A } _ { n } ~ = ~ [ 0 , \sqrt { n } ] \times [ 0 , \sqrt { n } ]$ . Similarly, we construct the latter = [0 ] [0 ]by placing nodes according to a p.p.p. of intensity n over the square $A _ { 1 } = [ 0 , 1 ] \times [ 0 , 1 ]$ . According to Chebyshev’s Inequality, we can easily obtain the number of nodes in $\mathcal { A } _ { n }$ (or A ) is within $( ( 1 - \varepsilon _ { 0 } ) n , ( 1 + \varepsilon _ { 0 } ) n )$ . To simplify the description, we assume that the number of nodes are n, without changing our results in order sense.

# A. Capacity Definition

Assume that $V = \{ v _ { 1 } , v _ { 2 } , \cdots , v _ { n } \}$ is the set of nodes in the network, and ${ \mathcal { S } } \subseteq V$ 1 2is the set of source nodes of multicast, denote the number of multicast sessions as $| \boldsymbol { S } | = n _ { s }$ . For each source node, we randomly select $n _ { d }$ =nodes as destinations from the other nodes. Let $\Lambda _ { { \mathcal S } , n _ { d } } = ( \lambda _ { S , 1 } , \lambda _ { S , 2 } , \cdot \cdot \cdot , \lambda _ { S , n _ { s } } )$ Λ = ( 1 2 )be the rate vector of the multicast data rate of all multicast sessions. Define the total multicast throughput capacity of such feasible rate vector as $\Lambda _ { S , n _ { d } } ^ { \mathrm { T } } ( n ) ~ = ~ \Sigma _ { i = 1 } ^ { n _ { s } } \lambda _ { S , i }$ , de-Λ ( ) = Σ =1fine the average per-session multicast throughput capacity as $\begin{array} { r } { \Lambda _ { S , n _ { d } } ^ { \mathrm { P } } ( n ) = \frac { 1 } { n _ { s } } \Sigma _ { i = 1 } ^ { n _ { s } } \lambda _ { S , i } } \end{array}$ , and define the minimum per-session Λ ( ) = Σ =1multicast throughput capacity as 1ns $\begin{array} { r } { \Lambda _ { S , n _ { d } } ^ { \mathrm { M } } ( n ) = \operatorname* { m i n } _ { v _ { S , i } \in S } \lambda _ { S , i } } \end{array}$ see the formal definitions of capacity in [10] and [11].

# B. Channel Model

We assume all nodes are individually power-constrained, $i . e .$ , for any node $v _ { i } .$ , it transmits at constant power $P _ { i } \in$ $[ P _ { m i n } , P _ { m a x } ] .$ , where $P _ { m i n }$ and $P _ { m a x }$ are some positive con-[ ]stants. Node $v _ { j }$ receives the transmitted signal from node $v _ { i }$ with power $\bar { P _ { i } } \cdot \ell ( v _ { i } , v _ { j } )$ , where $\ell ( v _ { i } , v _ { j } )$ indicates the path loss between $v _ { i }$ (and $v _ { j }$ ( ). We restrict ourselves to a model of communication where the interference at the receiver is simply regarded as noise, i.e., we focus on the networkingtheoretic bounds. Hence, any two nodes can establish a direct communication link, over a channel of bandwidth B, of rate

$$
R (v _ {i}, v _ {j}) = B \log (1 + \frac {P _ {i} \cdot \ell (v _ {i} , v _ {j})}{N _ {0} + \sum_ {v _ {k} \in A (i)} P _ {k} \cdot \ell (v _ {k} , v _ {j})}),
$$

where $N _ { 0 }$ is the ambient noise power at the receiver, and A i 0is the set of nodes that transmit when $v _ { i }$ is scheduled.

# C. Useful Known Results

We recall some related results to be used in the paper.

Lemma 1 (Tail on Chernoff Bounds): For a Poisson random variable X of parameter λ, we have

$$
\operatorname * {P r} (X \geq x) \leq e ^ {- \lambda} (e \lambda) ^ {x} / x ^ {x}, \text {   for   } x > \lambda ,
$$

$$
\operatorname * {P r} (X \leq x) \leq e ^ {- \lambda} (e \lambda) ^ {x} / x ^ {x} \text {for} 0 \leq x <   \lambda .
$$

Lemma 2 (Azuma’s Inequality): Suppose that random variables $X _ { 0 } , X _ { 1 } , X _ { 2 } , \dots , X _ { n } , \dots$ are martingale and $\left| X _ { k } \right. -$ $X _ { k - 1 } | \leq a _ { k }$ 1 2almost surely for any $k \geq 1$ . Then for all positive 1 1integers N and all positive real number δ, we have

$$
\operatorname * {P r} (| X _ {N} - X _ {0} | \geq \delta) \leq 2 \exp \left(- \frac {\delta^ {2}}{2 \sum_ {i = 1} ^ {N} a _ {k} ^ {2}}\right)
$$

Recall that a sequence of random variables $X _ { i } , \ 0 \ \leq \ i ,$ , are called martingale if they satisfy that

$$
E (X _ {N + 1} \mid X _ {0}, X _ {1}, \dots , X _ {N}) = X _ {N}.
$$

NOTATIONS: Throughput the paper, for a 2-dimension line segment $L ~ = ~ u v , ~ \left| L \right|$ represents the Euclidean distance =between u and v; for a discrete set U , |U | represents its cardinality. For a continuous region A, we use A to denote its area; for a tree T , we use T  to denote its total Euclidean edge lengths; $x \to \infty$ denotes that variable x takes value to infinity. To facilitate the expression, define a function as

$$
\max _ {o r d e r} \{\varphi (n), \phi (n) \} = \left\{ \begin{array}{l l} \Theta (\varphi (n)), & \text { if } \varphi (n) = \Omega (\phi (n)) \\ \Theta (\phi (n)), & \text { if } \phi (n) = \Omega (\varphi (n)) \end{array} \right.
$$

Similarly, we define another function as

$$
\min _ {o r d e r} \{\varphi (n), \phi (n) \} = \left\{ \begin{array}{l l} \Theta (\varphi (n)), & \text { if } \varphi (n) = O (\phi (n)) \\ \Theta (\phi (n)), & \text { if } \phi (n) = O (\varphi (n)) \end{array} \right.
$$

To simplify the description, let $\theta ( n ) \colon [ \theta _ { 1 } ( n ) , \theta _ { 2 } ( n ) ]$ represent that $\theta ( n ) \ = \ \Omega ( \theta _ { 1 } ( n ) )$ and $\theta ( n ) ~ = ~ { \cal O } ( \theta _ { 2 } ( n ) ) ;$ ] let $\theta ( n ) { \mathrm { : } }$ $( \theta _ { 1 } ( n ) , \theta _ { 2 } ( n ) ]$ Ω( 1( ))represent that $\theta ( n ) = \omega ( \theta _ { 1 } ( n ) )$ ))and $\theta ( n ) =$ $O ( \theta _ { 2 } ( n ) )$ 2(.

# III. MAIN RESULTS

Let $d _ { i j }$ be the Euclidean distance between two nodes $v _ { i }$ and $v _ { j }$ . Let the power attenuation function be $\ell ( v _ { i } , v _ { j } )$ . We study the capacity issue taking account of all $n _ { s }$ (and $n _ { d }$ )under Gaussian channel model. The general results are presented in Theorem 6 and Theorem 7. Here, we present the results under the popular assumption that $n _ { s } = \Theta ( n )$ as the specific cases of our general results.

# A. Random Extended Networks

For random extended networks, we assume that $\ell ( v _ { i } , v _ { j } ) =$ $\operatorname* { m i n } \{ 1 , \ d _ { i j } ^ { - \alpha } \}$ with $\alpha > 2$ and $N _ { 0 } > 0$ .

in 1 2 0 0Theorem 1: The achievable per-session multicast throughput for random extended networks is of order

$$
\left\{ \begin{array}{l l} \Omega (\frac {1}{\sqrt {n _ {d} n}}) & \text { when } n _ {d}: [ 1, \frac {n}{(\log n) ^ {\alpha + 1}} ] \\ \Omega (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}}) & \text { when } n _ {d}: [ \frac {n}{(\log n) ^ {\alpha + 1}}, \frac {n}{(\log n) ^ {2}} ] \\ \Omega (\frac {1}{\sqrt {n n _ {d}} \cdot (\log n) ^ {\frac {\alpha - 1}{2}}}) & \text { when } n _ {d}: [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} ] \\ \Omega (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha}{2}}}) & \text { when } n _ {d}: [ \frac {n}{\log n}, n ] \end{array} \right. \tag {1}
$$

For the upper bound, we have

Theorem 2: The per-session multicast throughput for random extended networks is of order

$$
\left\{ \begin{array}{l l} O (\frac {1}{\sqrt {n _ {d} n}}) & \text { when } n _ {d}: [ 1, \frac {n}{(\log n) ^ {\alpha}} ] \\ O (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha}{2}}}) & \text { when } n _ {d}: [ \frac {n}{(\log n) ^ {\alpha}}, n ] \end{array} \right. \tag {2}
$$

Combining Theorem 1 and Theorem 2, we obtain

Theorem 3: The per-session multicast capacity for random extended networks is of order

$$
\left\{ \begin{array}{l l} \Theta (\frac {1}{\sqrt {n _ {d} n}}) & \text { when } n _ {d}: [ 1, \frac {n}{(\log n) ^ {\alpha + 1}} ] \\ \Theta (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha}{2}}}) & \text { when } n _ {d}: [ \frac {n}{\log n}, n ] \end{array} \right. \tag {3}
$$

# B. Random Dense Networks

For the random dense network, we assume that $\ell ( v _ { i } , v _ { j } ) =$ $d _ { i j } ^ { - \alpha }$ with $\alpha > 2 .$ .

2Theorem 4: The achievable per-session multicast throughput for random dense networks is of order

$$
\left\{ \begin{array}{l l} \Omega (\frac {1}{\sqrt {n _ {d} n}}) & \text { when } n _ {d}: [ 1, \frac {n}{(\log n) ^ {3}} ] \\ \Omega (\frac {1}{n _ {d} (\log n) ^ {\frac {3}{2}}}) & \text { when } n _ {d}: [ \frac {n}{(\log n) ^ {3}}, \frac {n}{(\log n) ^ {2}} ] \\ \Omega (\frac {1}{\sqrt {n n _ {d} \log n}}) & \text { when } n _ {d}: [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} ] \\ \Omega (\frac {1}{n}) & \text { when } n _ {d}: [ \frac {n}{\log n}, n ] \end{array} \right. \tag {4}
$$

Combining with the upper bound proposed in [8] (as in Lemma 13), we obtain

Theorem 5: The per-session multicast capacity for random dense networks is of order

$$
\left\{ \begin{array}{l l} \Theta (\frac {1}{\sqrt {n _ {d} n}}) & \text { when } n _ {d}: [ 1, \frac {n}{(\log n) ^ {3}} ] \\ \Theta (\frac {1}{n}) & \text { when } n _ {d}: [ \frac {n}{\log n}, n ] \end{array} \right. \tag {5}
$$

# IV. LOWER BOUND FOR RANDOM EXTENDED NETWORKS

In this section, we focus on the lower bound of multicast capacity for REN. We will propose two multicast schemes, denoted as $\mathfrak { F }$ and $\bar { \mathfrak { F } }$ respectively. Combining the throughput achieved by them, we obtain the achievable throughput for REN that acts as the lower bound for multicast capacity.

![](images/9e962cd17d619d05f3dd222d0437fe8ce5bb2e4e206aeb7b68fe0e690d4b904d.jpg)



(a) First-class highway

![](images/71d0ca02d949037f6c9ffbb7c6a7bb9c9f6fb24b6105bc4b66a5e174846eb750.jpg)



(b) Second-class highways   
Fig. 1. (a) The bold polygonal line represents an open path consisting of open edges. A vertical first-class highway is described as a polygonal line whose inflexions are called first-class stations. (b) The bold lines connecting the nodes called second-class stations represent second-class highways.

# A. Highways System

Highway system consists of two levels of highways. The first is the first-class highway (FH), it is indeed the highway constructed in [7]. The second is the second-class highway (SH) that is built without using percolation theory as FH.

1) First-class highways: We use the same method in [7] to construct FHs. As an illustration for the discrete edgepercolation model in Fig.1(a), if a cell $c _ { i }$ contains at least one node, it is called open and its specific diagonal line is called open edge. An open path consists of open edges. A first-class highway is built based on an open path crossing the area from a bound to its opposite, see Fig.1(a).

Density of FHs: We partition the region ${ \mathcal { A } } _ { n }$ into subsquares with a constant side length c to obtain $m ^ { 2 }$ cells and the grid graph $\mathcal { C } _ { n } .$ , where $m = \lceil { \sqrt { n } } / { \sqrt { 2 } } c \rceil$ . We call these cells =percolation-cells. For a given $\kappa > 0$ , we partition the grid graph $\mathcal { C } _ { n }$ 0into horizontal (vertical) rectangle slabs with the horizontal (vertical) width of m subsquares and the vertical (horizontal) width of κ $m \mathrm { ~ - ~ } \varepsilon _ { m }$ subsquares, denoted as $R _ { i } ^ { h } ~ ( R _ { i } ^ { v } )$ log. Denote the number of disjoint open paths contained in slab $R _ { i } ^ { h } ~ ( R _ { i } ^ { v } )$ , i.e., the number of disjoint horizontal (vertical) first-class highways in each slab, as $N _ { i } ^ { h } ~ ( N _ { i } ^ { v } )$ . Let $N ^ { h } = \operatorname* { m i n } _ { \cdot } N _ { i } ^ { h } , N ^ { v } = \operatorname* { m i n } _ { \cdot } \dot { N } _ { i } ^ { v }$ . From [7], we get

Lemma 3: ( [7]) For all κ and $p \in ( 5 / 6 , 1 )$ satisfying $2 +$ κ $( 6 ( 1 - p ) ) < 0$ (5 6, there exists a constant $\delta ( \kappa , p )$ 2 +such that $\operatorname* { l i m } _ { m \to \infty } \operatorname* { P r } ( N ^ { h } \geq \delta \log m ) = 1 ; \operatorname* { l i m } _ { m \to \infty } \operatorname* { P r } ( N ^ { v } \geq \delta \log m ) = 1 .$ limm→∞ limm→∞

Pr( log ) = 1; Pr( log ) = 1Notations of FHs: We assume that there are just δ  m loghorizontal (vertical) first-class highways in each horizontal (vertical) slab, which does not degrade the derived throughput in order sense. From lemma 3, we can subdivide each slab into δ m slices with width l, where $l = ( \kappa \log m - \varepsilon _ { m } ) / \delta \log m$ . Hence, we can define a bijec-= ( log )/ logtive mapping from horizontal slices to horizontal first-class highways, denoted as $g ^ { h } : \mathbb { S } ^ { h } \longrightarrow \mathbb { H } ^ { h }$ , where $\mathbb { S } ^ { h }$ represents the :set of all horizontal slices and $\mathbb { H } ^ { h }$ represents the set of all horizontal first-class highways. Similarly, we can define the bijective mapping from vertical slices to vertical first-class highways, denoted as $g ^ { v } \ : \mathbb { S } ^ { v } \ \longrightarrow \ \mathbb { H } ^ { v }$ , where $\mathbb { S } ^ { v }$ represents :the set of all vertical slices and $\mathbb { H } ^ { v }$ represents the set of all

# Algorithm 1 Multicast Routing Scheme $\mathfrak { F } ^ { R }$

Input: The multicast session $\mathcal { M } _ { k }$ and $( U _ { k } )$ .

Output: A multicast routing graph $\mathcal { G } ( U _ { k } )$ T.

1: For each link $\begin{array} { r l } { v _ { i } } & { { } \to \ v _ { j } } \end{array}$ of $\operatorname { E S T } ( U _ { k } )$ , implement the EST( )following sub-steps to realize the routing $v _ { i }  v _ { j }$ .

(1) By a single hop, $v _ { i }$ drains the packet into the VSH $\bar { f } ^ { v } ( v _ { i } )$ via $\bar { w } _ { i } ^ { v }$ that is the closest second-class station in $\bar { f } ^ { v } ( v _ { i } )$ ¯with the distance of $| v _ { i } \bar { w } _ { i } ^ { v } | = \Theta ( \sqrt { \log n } )$ to $v _ { i }$ .   
( )(2) Along the VSH $\bar { f } ^ { v } ( v _ { i } )$ ¯ = Θ( log, the packet is drained into the HFH $f ^ { h } { \bar { ( v _ { i } ) } }$ via $w _ { i } ^ { h }$ ( )that is the closest first-class station (Fig. $2 ( \mathrm { c } ) )$ ) to the intersection point of $\bar { f } ^ { v } ( v _ { i } )$ and $f ^ { h } ( v _ { i } )$ .   
(3) The packet is transmitted along $f ^ { h } ( v _ { i } )$ )to $u _ { i j } ^ { h }$ ( )that is the closest first-class station on $f ^ { h } ( v _ { i } )$ ( )to $u _ { i j } .$ , where $u _ { i j }$ denotes the intersection point of $f ^ { h } ( v _ { i } )$ and $\bar { f } ^ { v } ( v _ { j } )$ .   
( ) ( )(4) By a single hop, the packet is transported from $u _ { i j } ^ { h }$ to $u _ { i j } ^ { v }$ that is the closest first-class station on $f ^ { v } ( v _ { j } )$ to $u _ { i j }$ .   
(5) The packet is transmitted along $f ^ { h } ( v _ { i } )$ (to $w _ { j } ^ { v }$ that is ( )the closest first-class station to the intersection point of the HSH $\bar { f } ^ { \bar { h } } ( v _ { j } )$ and the VFH $f ^ { v } ( v _ { j } )$ .   
( )(6) Along the HSH $\bar { f } ^ { h } ( v _ { j } )$ ( ), the packet is delivered to $\bar { w } _ { j } ^ { h }$ ( )that is the closest second-class station in $\bar { f } ^ { h } ( v _ { j } )$ ¯with the distance of $| v _ { j } \bar { w } _ { j } ^ { h } | = \Theta ( \sqrt { \log n } )$ to $v _ { j }$ .   
¯ =(7) By a single hop, $\bar { w } _ { j } ^ { h }$ ( log )delivers the packet to $v _ { j }$

¯2: Consider the next link of $\operatorname { E S T } ( U _ { k } )$ (go to step 1), until all the links in $\operatorname { E S T } ( U _ { k } )$ EST( )are checked.

EST( )3: Considering the resulted routing graph, we merge the same edges (hops), remove those circles which have no impact on the connectivity of the communications for $\left( U _ { k } \right)$ . Finally, we obtain the multicast routing graph $\mathcal { G } ( U _ { k } )$ .

vertical first-class highways. Notice that any slice can and only can project to the first-class highway contained in the slab that posses the slice, which ensures that the distance from any points in the slice to the corresponding highway is at most κ $m - \varepsilon _ { m }$ . Based on the two mappings, we can define two logfunctions as $f ^ { h } : V \to \mathbb { H } ^ { h }$ and $f ^ { v } : V \to \mathbb { H } ^ { v }$ , where V is :the set of all nodes in region ${ \mathcal { A } } _ { n } .$ :. The two functions satisfy the condition: For a node v and a horizontal slice $s _ { i } ^ { h } \in \mathbb { S } ^ { h }$ (or vertical slice $s _ { i } ^ { v } \in S ^ { v } )$ , if v locates in the region $\bar { s } _ { i } ^ { h }$ (or $s _ { i } ^ { v } )$ , then $f ^ { h } ( v ) = \dot { g } ^ { h } ( s _ { i } ^ { h } )$ (or $f ^ { v } ( v ) = g ^ { v } ( s _ { i } ^ { v } ) )$ .

( ) = ( ) (2) Second-class highway $\ ( S H s ) { \mathrm { . } }$ ( )We partition the region $\mathcal { A } _ { n }$ into subsquares of a side length $\sigma \sqrt { \log n } - \epsilon _ { n }$ to obtain $n / ( \sigma \sqrt { \log n } - \epsilon _ { n } ) ^ { 2 }$ logcells, as depicted in Fig.1(b). We denote ( log )these subsquares as $\bar { c } _ { j }$ and call them connected-cells.

¯Density of SHs: Let $N ( \bar { c } _ { j } )$ be the number of Poisson (¯ )points inside the connected-cell $\bar { c } _ { j }$ . Furthermore, we define the uniform lower bound of $N \big ( \bar { c } _ { j } \big )$ as $N _ { \bar { c } }$ . We firstly show

Lemma 4: For any , $2 \varrho \ : > \ : 1 \ : +$ ¯   and $\sigma , ~ \sigma ^ { 2 } ~ \geq$ 2 1 + log4− − , w.h.p., each connected-cell contains no less than $\frac { 4 \varrho } { ( 2 \varrho - \log \varrho - 1 ) }$  $\theta _ { 1 }$ n nodes, where $\begin{array} { r } { \theta _ { 1 } = \frac { \sigma ^ { 2 } } { 2 \varrho } } \end{array}$ σ2 is a constant.

log 1 = 2It is proved based on lemma 1. See detail in our report [12].

Each row (column) is called row-slab (column-clab). Denoted them as $\bar { R } _ { i } ^ { h } \ ( \bar { R } _ { i } ^ { v } )$ . We construct the SHs within each row-slab (column-slab) by the method illustrated in Fig.1(b). According to Lemma 4, w.h.p., each connected-cell contains at least $\theta _ { 1 }$ n nodes, then we can construct $2 \theta _ { 1 }$ n disjoint 1 log 2 1 logSHs in each row-slab (column-slab). Here, we say two secondclass highways are disjoint if there is no common second-class station shared by them.

Notations of SHs: Assume that there are just $2 \theta _ { 1 }$ n horizontal (vertical) second-class highways in each $\bar { R } _ { j } ^ { h } \ ( \bar { R } _ { j } ^ { v } )$ , then we can subdivide every $\bar { R } _ { j } ^ { h } \mathbf { \Sigma } ( \bar { R } _ { j } ^ { v } )$ into $2 \theta _ { 1 }$ n slices with width l and length ${ \sqrt { n } } ,$ , where $\bar { l } ~ = ~ \sigma / ( 2 \theta _ { 1 } \sqrt { \log n } )$ . = (2 1 log )We call these slices as row-slices (column-slices). Hence, we can define a bijective mapping from row slices to horizontal second-class highways, denoted as $\bar { g } ^ { h } : \bar { \mathbb { S } } ^ { h } \to \bar { \mathbb { H } } ^ { h }$ , where $\bar { \mathbb { S } } ^ { h }$ ¯represents the set of all row slices and $\bar { \mathbb { H } } ^ { h }$ represents the set of all horizontal second-class highways. Similarly, we can define the bijective mapping from column slices to vertical secondclass highways, denoted as $\bar { g } ^ { v } : \bar { \mathbb { S } } ^ { v } \longrightarrow \bar { \mathbb { H } } ^ { v }$ , where $\bar { \mathbb { S } } ^ { v }$ represents ¯ :the set of all vertical slices and $\bar { \mathbb { H } } ^ { v }$ represents the set of all vertical second-class highways. Notice that any slice can and only can project to the second-class highway contained by the slab that passes the slice, which ensures that the distance from any points in the slice to the corresponding highway is at most $\sigma { \sqrt { \log n } }$ . Based on the two mappings, we can define logtwo functions as ${ \bar { f } } ^ { h } : V \to { \bar { \mathbb { H } } } ^ { h }$ and ${ \bar { f } } ^ { v } : { \bar { V } } \stackrel { \cdot } {  } { \bar { \mathbb { H } } } ^ { v }$ , where $V$ is :the set of all nodes in region $\mathcal { A } _ { n } = [ 0 , \sqrt { n } ] \times [ 0 , \sqrt { n } ]$ . The two = [0 ] [0 ]functions satisfy the condition: For a node v and horizontal slice $\bar { s } _ { i } ^ { h } \in \bar { \mathbb { S } } ^ { h }$ (or vertical slice $\bar { s } _ { i } ^ { v } \in \bar { \mathbb { S } } ^ { v } )$ , if v belongs to region $\bar { s } _ { i } ^ { h }$ ¯(or $\bar { s } _ { i } ^ { v } )$ ¯, then $\bar { f } ^ { h } ( v ) = \bar { g } ^ { h } ( \bar { s } _ { i } ^ { h } )$ ¯(or $\bar { f } ^ { v } ( v ) = \bar { g } ^ { v } ( \bar { s } _ { i } ^ { v } ) )$ ).

# B. Multicast Scheme $\mathfrak { F }$

Denote the routing and transmission scheduling of the scheme $\mathfrak { F }$ as $\mathfrak { F } ^ { R }$ and $\bar { \boldsymbol { \mathfrak { F } } } ^ { T }$ .

1) Transmission scheduling scheme $\mathfrak { F } ^ { T } .$ : We make all nodes transmit at a constant power $P \in [ P _ { m i n } , P _ { m a x } ]$ , and schedule [ ]FHs and SHs respectively, i.e., without any overlapped time slot, by which the rate along them can be achieved of $\Omega ( 1 )$ ( [7]) and $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ (Lemma 5), respectively.

Ω((log ) )First-class scheduling: Since the first-class highways are indeed highways in [7], we can adopt the same scheduling scheme as that in [7]. Specially, because we only schedule the short links with constant distance, we can use a TDMA scheme with constant scheduling period, for example, a 9-TDMA, to obtain the constant rate of FHs. See detail in [7].

Second-class scheduling: We adopt 16-TDMA scheme to schedule the transmissions of second-class highways. The main trick here is: Instead of scheduling only one link starting at each activated (scheduled) cell in each time slot, we consider scheduling a set of links which initiate from the same connected-cell together. Specially, after we partition the deployment region into connected-cells, we further divide time into a sequence of 16 successive slots. In each time slot, we consider disjoint sets of connected-cells that are allowed to be activated simultaneously, as depicted in Fig. 2(b). Notice that if a connected-cell is activated, $\theta _ { 1 }$ n links initiating from 1 logthe connected-cell can transmit simultaneously. Obviously, compared with only scheduling one link in each connected cell, this modification increase the total bit-rate by order of n if the total interference is still bounded. So can we prove logthat the total interference is still bounded? Fortunately, the proof of Lemma 5 give us a positive answer. We further derive the data rate of the second-class highways.

![](images/3a9f84de144857d6a687043c25223268bec13b6bf4db327afa5599401b3f2255.jpg)



(a) Parallel transmission scheduling

![](images/3d4a510ff6c8378aaf8b9ab3430939788be61baced178ba2ace396d7fce23f23.jpg)



(b) Overview of multicast routing $\mathfrak { F } ^ { R }$

![](images/300653974dfdabe1f33c115a5f4926bdc016e1ee177b3a97b9d1e40799d3dc8d.jpg)



(c) Routing for communication-pairs   
Fig. 2. (a) Gray squares can be scheduled simultaneously. Around each gray square there is a silence region of squares in which nodes are prohibited to transmit in a given time slot. In any time slot, there are $\Theta ( { \dot { \log n } } )$ concurrent links initiated from every activated connected-cell. (b) The EST consists of edges $e _ { 1 } \sim e _ { 5 } . \ v _ { i }$ Θ(log )drains packets into the specific first-class highway (bold solid curves) via the second-class highway (the thin solid curves with arrows). (c) Two 1 5bold solid curves represent the first-class highways $f ^ { h } ( v _ { i } )$ and $f ^ { v } ( v _ { j } )$ , respectively. Two thin solid curves represent the second-class highways $\mathring { f } ^ { v } ( v _ { i } )$ and $\bar { f } ^ { h } ( v _ { j } )$ ( ) ( ), respectively. The path consisting of the solid curves with arrows represents the routing from vi to vj .

Lemma 5: Along each second-class highway, the achievable rate is of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

Proof: For any link along second-class highways in any time slot, since the length of the link is at least $\sigma \sqrt { \log n } - \epsilon _ { n } ,$ lowe obtain the sum of interference to the receiver as:

$$
\begin{array}{l} I (n) \leq P \cdot (\theta_ {1} \log n - 1) \cdot \ell (\sigma \sqrt {\log n} - \epsilon_ {n}) \\ + \sum_ {i = 1} ^ {n} 8 i P (\theta_ {1} \log n) \cdot \ell ((4 i - 3) \cdot (\sigma \sqrt {\log n} - \epsilon_ {n})) \\ \leq P \cdot 2 ^ {\alpha} \theta_ {1} \sigma^ {- \alpha} (\log n) ^ {1 - \frac {\alpha}{2}} \cdot \left(1 + \lim _ {n \rightarrow \infty} \sum_ {i = 1} ^ {n} \frac {8 i}{(4 i - 3) ^ {\alpha}}\right) \\ \end{array}
$$

The latest limitation is obviously converges when $\alpha > 2$ . Since the distance of every hop is at most ${ \sqrt { 1 0 } } \cdot ( \sigma { \sqrt { \log n } } - \epsilon _ { n } )$ , we have the signal $S ( n )$ 10 ( log )at the receiver can be bounded as $S ( n ) ~ \geq ~ { \cal P } \bar { ~ } \cdot 1 0 ^ { - \frac { \alpha } { 2 } } \bar { \sigma } ^ { - \alpha } ( \log n ) ^ { - \frac { \alpha } { 2 } }$ . Then, the rate along ( ) 10the SH is achieved of $\begin{array} { r } { \bar { R } ( n ) \ = \ \frac { 1 } { 1 6 } \log \Big ( 1 + \frac { S ( n ) } { N _ { 0 } + I ( n ) } \Big ) } \end{array}$ . By α >  and N > , we have S(n)N0 I n $\alpha \ > \ 2$ $N _ { 0 } > 0$ $\frac { S ( \grave { n } ) } { N _ { 0 } + I ( n ) } ~ \to ~ 0$ . Hence, $\bar { R } ( n ) = \Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

2) Routing scheme $\mathfrak { F } ^ { R } .$ : Considering a multicast session $\mathcal { M } _ { k } , \ k = 1 , 2 , \cdot \cdot \cdot n _ { s } ,$ we denote the set of nodes as $U _ { k } =$ $\{ v _ { k _ { 0 } } \} \cup \{ v _ { k _ { 1 } } , v _ { k _ { 2 } } , \cdot \cdot \cdot v _ { k _ { n _ { d } } } \}$ , where $\boldsymbol { v } _ { k _ { 0 } }$ =is the source node and $\{ v _ { k _ { 1 } } , v _ { k _ { 2 } } , \cdot \cdot \cdot v _ { { k _ { n _ { d } } } } \}$ is the set of destinations. We firstly construct the Euclidean spanning tree (EST) based on $U _ { k }$ using the method in [10], denoted as $\operatorname { E S T } ( U _ { k } )$ . Based on $\operatorname { E S T } ( U _ { k } )$ EST( ), we propose Algorithm 1 to construct the multicast EST( )routing graph $\mathcal { G } ( U _ { k } )$ . To simplify the notation, we denote the (multicast session $\mathcal { M } _ { k }$ as $U _ { k } = \{ v _ { 0 } \} \cup \{ v _ { 1 } , v _ { 2 } , \cdot \cdot \cdot v _ { n _ { d } } \}$ and = 0 1 2reaffirm that HSH (VSH) and HFH (VFH) are respectively the abbreviations of horizontal (vertical) second-class highway and horizontal (vertical) first-class highway.

# C. Multicast Throughput Achieved by F

For the seven phases of routing for a communication-pairs (See illustration in Fig.2(c)), we successively analyze the achievable total rate and relay burden of each cell (or station) for every phase. In Phase 3 and Phase 5, the packet is both transmitted along the first-class highways (FHs). From Lemma 7, we know a constant rate can be achieved along FHs. For Phase 4, the analysis of rate and relay burden is similar to that of Phase 3 and Phase 5, because the single hop in Phase 4 has no difference from the hops in the HFH and VFH. Thus, we do not individually analyze Phase 4, and call generally Phases 3, 4 and 5 as first-class highway phase (FH-Phase). For FH-Phase, we state Lemma 7. Before presenting the lemma, we recall a result proposed in [11].

Lemma 6: For EST built by the method in [11], we have $\| \operatorname { E S T } ( U _ { k } ) \| \ \leq \ 2 { \sqrt { 2 } } { \sqrt { n _ { d } } } { \sqrt { n _ { \ell } } }$ , where $k = 1 , 2 , \cdots , n _ { s }$ and $\| \operatorname { E S T } ( U _ { k } ) \|$ denotes the total Euclidean edge lengths.

EST( )Lemma 7: During FH-Phase, the per-session throughput is achieved of order

$$
\left\{ \begin{array}{l l} \Omega (n / (n _ {s} \Gamma (n, n _ {d}))) & \text { when } n _ {s} \Gamma (n, n _ {d}) / n = \Omega (\log n) \\ \Omega (1 / \log n) & \text { when } n _ {s} \Gamma (n, n _ {d}) / n = O (\log n) \end{array} \right. \tag {6}
$$

where $\begin{array} { r } { \Gamma ( n , n _ { d } ) = \operatorname* { m i n } _ { o r d e r } \{ \sqrt { n n _ { d } } + n _ { d } \log n , \ n \} } \end{array}$ .

Γ( ) = min + logProof: Since the rate along first highways can be achieved of a constant order, we need only to prove the maximum relay burden of first-class stations is w.h.p.,

$$
\left\{ \begin{array}{l l} O (n _ {s} \Gamma (n, n _ {d}) / n) & \text { when   } n _ {s} \Gamma (n, n _ {d}) / n = \Omega (\log n) \\ O (\log n) & \text { when   } n _ {s} \Gamma (n, n _ {d}) / n = O (\log n) \end{array} \right. \tag {7}
$$

with $\Gamma ( n , n _ { d } ) = \operatorname* { m i n } _ { o r d e r } \{ { \sqrt { n n _ { d } } } + n _ { d } \log n , \ n \}$ .

Γ( ) = min + logBy Lemma 6, upper tail on Chernoff bound (Lemma 1) and union bounds, we can prove the result in Equation (7), which completes the proof.

The detailed proof can be seen in our report [12].

Subsequently, we consider Phase 2 and Phase 6. We have the following two results.

Lemma 8: During Phase 2, the per-session throughput is achieved of order

$$
\left\{ \begin{array}{l l} \Omega (\frac {n}{n _ {s} n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}}) & \text { when   } n _ {s} n _ {d} = \Omega (n \sqrt {\log n}) \\ \Omega (\frac {1}{(\log n) ^ {1 + \frac {\alpha}{2}}}) & \text { when   } n _ {s} n _ {d} = O (n \sqrt {\log n}) \end{array} \right. \tag {8}
$$

Proof: By Lemma 5, the rate along SHs is achieved of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . Using the similar way to Lemma 7, we Ω((log ) )can prove that the maximum relay burden of the second-class stations during Phase 2 is $w . h . p .$ ., of order

$$
\left\{ \begin{array}{l l} O (\frac {n _ {s} \cdot n _ {d} \cdot \sqrt {\log n}}{n}) & \text { when } n _ {s} n _ {d} = \Omega (n \sqrt {\log n}) \\ O (\log n) & \text { when } n _ {s} n _ {d} = O (n \sqrt {\log n}) \end{array} \right. \tag {9}
$$

Then, we complete the proof.

Lemma 9: During Phase 6, the per-session throughput is achieved of order as in Equation (8).

In Phase 1 and Phase 7, as in Phase 2 and Phase 6, we can use 16-TDMA scheme to schedule the links with distance of $\Theta ( { \sqrt { \log n } } )$ in parallel, by which the rate of every link can Θ( log )be achieved of $\bar { \Omega ( ( \log n ) ^ { - \frac { \bar { \alpha } } { 2 } } ) }$ . On the other hand, there is no Ω((log ) )relay burden for the transmitters in Phases 1 and 7 due to the method of single-hop, thus, the following result holds.

Lemma 10: For all seven phases, it holds that Phases 1 and 7 must not be the bottleneck of the whole routing as long as Phases 2 and 6 are not the bottleneck.

We consider the bottleneck of the whole routing scheme $\mathfrak { F } ^ { R }$ that can be regarded as the per-session multicast throughput. For the Phases 3, 4 and 5, we have the result of Lemma 7. For Phases 2 and 6, we have the result of Lemma 8 and Lemma 9. For Phases 1 and 7, we have the result as in Lemma 10.

Based on an overall consideration of all phases of the routing $\mathfrak { F } ^ { R }$ , we can obtain

Lemma 11: By the multicast scheme F, the per-session multicast throughput is achieved of order

When $n _ { d } = O ( n / { \sqrt { \log n } } )$ ,

$$
\left\{ \begin{array}{l l} \Omega (\frac {1}{(\log n) ^ {1 + \frac {\alpha}{2}}}) & \text {when} n _ {s}: (1, \frac {n \log n}{\Gamma} ] \\ \Omega (\min _ {o r d e r} \{\frac {n}{n _ {s} \Gamma}, \frac {1}{(\log n) ^ {1 + \frac {\alpha}{2}}} \}) & \text {when} n _ {s}: [ \frac {n \log n}{\Gamma}, \frac {n \sqrt {\log n}}{n _ {d}} ] \\ \Omega (\min _ {o r d e r} \{\frac {n}{n _ {s} \Gamma}, \frac {n}{n _ {s} n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}} \}) & \text {when} n _ {s}: [ \frac {n \sqrt {\log n}}{n _ {d}}, n ] \end{array} \right.
$$

When $n _ { d } = \Omega ( n / \sqrt { \log n } )$ ,

$$
\left\{ \begin{array}{l l} \Omega (\frac {n}{n _ {s} n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}}) & \text {when} n _ {s}: (1, n \sqrt {\log n} / n _ {d} ] \\ \Omega (\frac {1}{(\log n) ^ {1 + \frac {\alpha}{2}}}) & \text {when} n _ {s}: [ n \sqrt {\log n} / n _ {d}, n ] \end{array} \right.
$$

where  is defined as Equation (11).

# D. Multicast Throughput Achieved by $\bar { \mathfrak { F } }$

We design the routing scheme of ${ \bar { \mathfrak { F } } } ,$ denoted as $\bar { \mathfrak { F } } ^ { R }$ , totally based on the SHs. Each edge $v _ { i }  v _ { j }$ in EST of a multicast session realizes the routing between them via a specific pair SHs: firstly, $v _ { i }$ drain the packet in SH $\bar { f } ^ { v } ( v _ { i } )$ by a single ( )hop. Secondly, the packet is transmitted along SH $\bar { f } ^ { v } ( v _ { i } )$ . Thirdly, the packet is carried from SH $\bar { f } ^ { v } ( v _ { i } )$ to SH $\bar { f } ^ { h } ( v _ { i } )$ . (Forthly, the packet is transmitted along SH $\bar { f } ^ { h } ( v _ { i } )$ ( ). Finally, the packet is delivered to $v _ { i }$ . The single hops in Phase 1 and Phase 4 will not become the bottleneck due to their same hop length as that of links along SHs and having not heavier relay burden than second-class stations. For the transmission scheduling of $\bar { \mathfrak { F } } ,$ denoted as $\bar { \mathfrak { F } } ^ { T }$ , we only need implement second-class scheduling for no other types of hops exist. It can be shown when the bottleneck of $\mathfrak { F } ^ { R }$ locates in SH-Phase, no poorer performance of throughput may be derived by scheme F than that derived by scheme ${ \mathfrak { F } } .$ . Subsequently, we consider the throughput achieved by ${ \bar { \mathfrak { F } } } .$ .

Lemma 12: By the multicast scheme $\bar { \mathfrak { F } } ,$ the per-session throughput is achieved of order

$$
\left\{ \begin{array}{l l} \Omega (\frac {n}{(\log n) ^ {\frac {\alpha}{2}} n _ {s} \cdot \phi (n , n _ {d})}) & \text {when} n _ {s} \cdot \phi (n, n _ {d}) / n = \Omega (\log n) \\ \Omega (1 / (\log n) ^ {1 + \frac {\alpha}{2}}) & \text {when} n _ {s} \cdot \phi (n, n _ {d}) / n = O (\log n) \end{array} \right.
$$

where $\phi ( n , n _ { d } ) = \operatorname* { m i n } _ { o r d e r } \{ { \sqrt { n n _ { d } } } / { \sqrt { \log n } } + n _ { d } , \ n \}$

( ) = min log +Proof: The throughput in Phase 1 and Phase 5 is not less than that in other phases, which means the bottleneck of the whole routing locates on second-class highways. According to Lemma 5, the rate along the second-class highways can be achieved of $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . On the other hand, using the Ω((log ) )similar way to the proof of Lemma 7, we can obtain that the maximum relay burden of the second-class stations is $w . h . p .$ ,

$$
\left\{ \begin{array}{l l} O (n _ {s} \phi (n, n _ {d}) / n) & \text { when } n _ {s} \phi (n, n _ {d}) / n = \Omega (\log n) \\ O (\log n) & \text { when } n _ {s} \phi (n, n _ {d}) / n = O (\log n) \end{array} \right. \tag {10}
$$

with $\phi ( n , n _ { d } ) = { \left\{ \begin{array} { l l } { \Theta ( { \sqrt { \frac { n _ { d } n } { \log n } } } ) { \mathrm { ~ w h e n ~ } } n _ { d } = O ( { \frac { n } { \log n } } ) } \\ { \Theta ( n _ { d } ) { \mathrm { ~ w h e n ~ } } n _ { d } = \Omega ( { \frac { n } { \log n } } ) } \end{array} \right. }$ l o g  nd   n n

Θ( ) when = Ω( log )Combining the rate and relay burden, the lemma is proved.

# E. General Result for Random Extended Networks

Combining Lemma 11 and Lemma 12, we can obtain the general result in Theorem 6. To simplify the description, let

$$
\begin{array}{l} \lambda_ {1} (n) := \frac {1}{(\log n) ^ {1 + \frac {\alpha}{2}}} \quad \lambda_ {2} (n) := \frac {n}{n _ {s} \Gamma} \\ \lambda_ {3} (n) := \frac {n}{n _ {s} n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}} \quad \lambda_ {4} (n) := \frac {n}{(\log n) ^ {\frac {\alpha}{2}} n _ {s} \Phi} \\ \end{array}
$$

and let $\Psi : = n _ { d } \cdot \sqrt { \log n }$ ,

$$
\Gamma := \left\{ \begin{array}{l l} \Theta (\sqrt {n _ {d} n}) & \text { when } n _ {d}: [ 1, \frac {n}{(\log n) ^ {2}} ] \\ \Theta (n _ {d} \log n) & \text { when } n _ {d}: [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} ] \\ \Theta (n) & \text { when } n _ {d}: [ n / \log n, n ] \end{array} \right. \tag {11}
$$

$$
\Phi := \left\{ \begin{array}{l l} \Theta (\sqrt {\frac {n _ {d} n}{\log n}}) & \text { when } n _ {d}: [ 1, n / \log n ] \\ \Theta (n _ {d}) & \text { when } n _ {d}: [ n / \log n, n ] \end{array} \right.
$$

Theorem 6: The achievable per-session throughput for random extended networks is of order $\Omega ( \lambda ( n ) )$ as in Table I.

Ω( ( ))By Theorem 6, Theorem 1 is obtained by letting $n _ { s } = \Theta ( n )$ .

# V. LOWER BOUND FOR RANDOM DENSE NETWORKS

In this section, we consider random dense networks (REN). We set the side length of the percolation-cell and connectedcell as $c / { \sqrt { n } }$ and $( \sigma \sqrt { \log n } - \epsilon _ { n } ) / \sqrt { n } .$ , respectively. We can ( log )obtain the first-class highways with the same density and rate as that in REN, and we obtain the second-class high system with the same density but with different rate as REN. The multicast scheme $\mathfrak { F }$ and $\bar { \mathfrak { F } }$ are still applicable to RDN, and we can show that the parallel scheduling technique in $\mathfrak { F } ^ { T }$ indeed has no effect in RDN. Due to space limitation, we only list the main results as follows. See detail in our report [12]. Let $\Psi _ { d } = n _ { d } ( \log n ) ^ { \frac { 3 } { 2 } }$ and

TABLE I PER-SESSION THROUGHPUT FOR Random Extended Networks 

<table><tr><td>Range of  $n_{d}$ </td><td>Order of  $\lambda(n)$ </td></tr><tr><td> $[1, \frac{n}{(\log n)^{3}}]$ </td><td> $\begin{cases}\lambda_{1}(n) & \text{if } n_{s} : (1, \frac{n \log n}{\Gamma}] \\ \min_{order} \{\lambda_{1}(n), \lambda_{2}(n)\} & \text{if } n_{s} : [\frac{n \log n}{\Gamma}, \frac{n \log n}{\Psi}] \\ \min_{order} \{\lambda_{2}(n), \lambda_{3}(n)\} & \text{if } n_{s} : [\frac{n \log n}{\Psi}, n]\end{cases}$ </td></tr><tr><td> $[\frac{n}{(\log n)^{3}}, \frac{n}{(\log n)^{2}}]$ </td><td> $\begin{cases}\lambda_{1}(n) & \text{if } n_{s} : (1, \frac{n \log n}{\Phi}] \\ \min_{order} \{\lambda_{1}(n), \lambda_{2}(n)\} & \text{if } n_{s} : [\frac{n \log n}{\Phi}, \frac{n \log n}{\Psi}] \\ \min_{order} \{\lambda_{2}(n), \lambda_{3}(n)\} & \text{if } n_{s} : [\frac{n \log n}{\Psi}, n]\end{cases}$ </td></tr><tr><td> $[\frac{n}{(\log n)^{2}}, n]$ </td><td> $\begin{cases}\lambda_{1}(n) & \text{if } n_{s} : (1, \frac{n \log n}{\Phi}] \\ \lambda_{4}(n) & \text{if } n_{s} : [\frac{n \log n}{\Phi}, n]\end{cases}$ </td></tr></table>

$$
\Phi_ {d} = \left\{ \begin{array}{l l} \Theta (\sqrt {n \cdot n _ {d} \cdot \log n}) & \text { when } n _ {d} = O (n / \log n) \\ \Theta (n) & \text { when } n _ {d} = \Omega (n / \log n) \end{array} \right.
$$

Theorem 7: The achievable per-session throughput for random dense networks is of order $\Omega ( \lambda _ { d } ( n ) )$ as in Table II.

TABLE II PER-SESSION THROUGHPUT FOR Random Dense Networks 

<table><tr><td>Range of  $n_d$ </td><td>Order of  $\lambda_d(n)$ </td></tr><tr><td> $[1, \frac{n}{(\log n)^3}]$ </td><td> $\begin{cases} \Omega(1/\log n) & \text{if } n_s : (1, \frac{n\log n}{\Phi_d}] \\ \Omega(\frac{n}{n_s \cdot \sqrt{n_n d}}) & \text{if } n_s : [\frac{n\log n}{\Phi_d}, n] \end{cases}$ </td></tr><tr><td> $[\frac{n}{(\log n)^3}, \frac{n}{(\log n)^2}]$ </td><td> $\begin{cases} \Omega(1/\log n) & \text{if } n_s : (1, \frac{n\log n}{\Phi_d}] \\ \Omega(\frac{n}{n_s n_d (\log n)^{\frac{3}{2}}}) & \text{if } n_s : [\frac{n\log n}{\Phi_d}, n] \end{cases}$ </td></tr><tr><td> $[\frac{n}{(\log n)^2}, \frac{n}{\log n}]$ </td><td> $\begin{cases} \Omega(1/\log n) & \text{if } n_s : (1, \frac{n\log n}{\Psi_d}] \\ \Omega(\frac{\sqrt{n}}{n_s \sqrt{n_d \log n}}) & \text{if } n_s : [\frac{n\log n}{\Psi_d}, n] \end{cases}$ </td></tr><tr><td> $[\frac{n}{\log n}, n]$ </td><td> $\begin{cases} \Omega(1/\log n) & \text{if } n_s : (1, \frac{n\log n}{\Psi_d}] \\ \Omega(\frac{1}{n_s}) & \text{if } n_s : [\frac{n\log n}{\Psi_d}, n] \end{cases}$ </td></tr></table>

Based on Theorem 7, Theorem 4 can be obtained by letting $n _ { s } = \Theta ( n )$ .

# VI. UPPER BOUND FOR MULTICAST CAPACITY

In this section, we consider the upper bounds for both random extended networks and random dense networks under the assumption that $n _ { s } ~ = ~ \Theta ( n )$ . Note that we revoke the = Θ( )meaning of all variables and number labels in above sections, unless we explicitly use them.

# A. Random Dense Networks

Based on a novel technique called arena exploited in [9], Keshavarz-Haddad et al. have proposed the upper bound of the multicast capacity for dense networks in [8]. That is,

Lemma 13: The per-session multicast capacity for dense networks is at most of order

$$
\left\{ \begin{array}{l l} O (\frac {1}{\sqrt {n _ {d} n}}) & \text {when} n _ {d}: [ 1, \frac {n}{(\log n) ^ {2}} ] \\ O (\frac {1}{n _ {d} \cdot \log n}) & \text {when} n _ {d}: [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} ] \\ O (\frac {1}{n}) & \text {when} n _ {d}: [ \frac {n}{\log n}, n ] \end{array} \right.
$$

# B. Random Extended Networks

In this subsection, we give an upper bound for multicast capacity for random extended networks.

Firstly, by partitioning the region $\mathcal { A } ( a ) = [ 0 , a ] \times [ 0 , a ]$ into ( ) = [0 ] [0 ]cells of side length g, we obtain a grid graph consisting of $\textstyle \Theta \bigl ( { \frac { a ^ { 2 } } { q ^ { 2 } } } \bigr )$ cells, denoted as $\mathbb { L } ( a , g )$ . Based on $\mathbb { L } ( a , g )$ , we propose a result for arbitrary multicast trees.

Lemma 14: Given a multicast session $\mathcal { M } _ { k } .$ , let $T _ { k }$ be the multicast tree for $\mathcal { M } _ { k }$ and $N ( T _ { k } )$ denote the number of cells used in $T _ { k }$ , then we have $\begin{array} { r } { \dot { N ( T _ { k } ) } = \Omega ( \frac { 1 } { q } \cdot \| \operatorname { E M S T } ( \mathcal { M } _ { k } ) \| ) } \end{array}$ when $\begin{array} { r } { n _ { d } = O ( \frac { a ^ { 2 } } { q ^ { 2 } } ) } \end{array}$ , where  Mk  denotes the total = ( ) EMST( )length of Euclidean Minimum Spanning Tree spanning $\mathcal { M } _ { k }$ .

Let $a = { \sqrt { n } }$ and $g = c ,$ where $c > 0$ is a constant, we =obtain a grid graph $\mathbb { L } ( { \sqrt { n } } , c )$ 0consisting of $\textstyle m ^ { 2 } = \Theta ( { \frac { n } { c ^ { 2 } } } )$ cells. ( )Firstly, we give the following lemma.

Lemma 15: The throughput capacity of any cell in the grid graph $\mathbb { L } ( { \sqrt { n } } , c )$ is of order $O ( 1 )$ .

( )Proof: For any cell $c _ { i }$ (in $\mathbb { L } ( { \sqrt { n } } , c )$ , and in any time t, ( )define the set of all links that are scheduled simultaneously and initiate from (or terminate in) ci as $\Pi _ { i } ( t )$ . Since the number of nodes in any cell of $\mathbb { L } ( { \sqrt { n } } , c )$ Π ( )is of order $O ( \log n )$ (by Lemma 1), we have $\{ \pi _ { i } ( n , t ) \} = O ( \log n )$ (log ), where $\pi _ { i } ( n , t ) ~ = ~ | \Pi _ { i } ( t ) |$ max ( ) = (log ). Denote the transmitting power, length ( ) = Π ( )and rate of the links in $| \Pi _ { i } ( t ) |$ | as $P _ { i ( j ) } \in [ P _ { m i n } , P _ { m a x } ] .$ , $l _ { i ( j ) }$ and $\lambda _ { i ( j ) }$ for $1 \ \leq \ j \ \leq \ \pi _ { i } ( n , t )$ ( ) [. Therefore, $\lambda _ { i ( j ) } \ \leq$ B log(1 + min 1N0+min{1,(li(j)+√2c)−α} - k=j P $\begin{array} { r } { B \log ( 1 + \frac { P _ { i ( j ) } \cdot \operatorname* { m i n } \{ 1 , l _ { i ( j ) } ^ { - \alpha } \} } { N _ { 0 } + \operatorname* { m i n } \{ 1 , ( l _ { i ( j ) } + \sqrt { 2 } c ) ^ { - \alpha } \} \sum _ { k \neq j } P _ { i ( k ) } } ) } \end{array}$ 1 (Pi(j)· { ,l−αi(j)} . Thus, we have λi(j) = O( N0 { , li(j) √ c −α} - k=j P $\begin{array} { r } { \lambda _ { i ( j ) } = O \big ( \frac { P _ { i ( j ) } \cdot \operatorname* { m i n } \{ 1 , l _ { i ( j ) } ^ { - \alpha } \} } { N _ { 0 } + \operatorname* { m i n } \{ 1 , ( l _ { i ( j ) } + \sqrt { 2 } c ) ^ { - \alpha } \} \sum _ { k \neq j } P _ { i ( k ) } } \big ) } \end{array}$ Pi(j)·min{1,l−αi(j)} . Since $c > 0$ is i(k) a constant, it holds that $\begin{array} { r } { \lambda _ { i ( j ) } = O ( \frac { P _ { i ( j ) } \cdot \operatorname* { m i n } \{ 1 , l _ { i ( j ) } ^ { - \alpha } \} } { N _ { 0 } + \operatorname* { m i n } \{ 1 , l _ { i ( j ) } ^ { - \alpha } \} \sum _ { k \neq i } P _ { i ( k ) } } ) } \end{array}$ ( min 1N0+min{1,l−αi(j)} - k=j P . Furthermore, we have $\begin{array} { r } { \sum _ { j = 1 } ^ { \pi _ { i } ( n ) } \lambda _ { i ( j ) } = O ( 1 ) } \end{array}$ , which completes the proof. $\lambda _ { i ( j ) } = { \cal O } ( \frac { 2 P _ { i ( j ) } } { \sum _ { k = 1 } ^ { \pi _ { i } ( n ) } P _ { i ( k ) } } )$ - 2πi(n)k=1 Pi(k) ) Pi(j) . Obviously,

=1 ( ) = (1)Based on Lemma 14 and Lemma 15, we can obtain an upper bound of multicast capacity for random extended networks.

Lemma 16: The minimum per-session multicast throughput that can be supported by using any multicast scheme is of order $\scriptstyle O \big ( { \frac { \sqrt { n } } { n _ { s } { \sqrt { n _ { d } } } } } \big )$ .

(  )Furthermore, we will derive another upper bound on a result in [13]. That is, for the random extended network, the nearest neighbor graph has w.h.p., an edge of length $\Omega ( { \sqrt { \log n } } )$ . By exploring this long edge, we can derive another upper bound on multicast capacity.

Lemma 17: The minimum per-session multicast throughput that can be supported by using any multicast scheme is of order $O ( \frac { n } { n _ { s } n _ { d } } ( \log { n } ) ^ { - \frac { \alpha } { 2 } } )$ O nnsnd .

log )Proof: Assume that the longest edge in the nearest neighbor graph of the random network is uv. Then the length of uv is of order $l ( u , v ) = \Omega ( \sqrt { \log n } )$ ( [2]). Thus, the capacity of the link uv is $\begin{array} { r } { C ( u , v ) \le B \log ( 1 + \frac { P _ { m a x } l _ { A i t } ^ { - \alpha } } { N _ { 0 } } ) } \end{array}$ N0 (in absence ( )of interference). That is, $C ( u , v ) = O ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . On the ( ) = ((log ) )other hand, for node v, the probability p that it is chosen as a terminal of a given multicast flow is ${ \mathfrak { p } } = { \frac { n _ { d } } { n } }$ . It is easy to =show that, with high probability, the number of multicast flows that will choose the node v as a terminal is at least $n _ { s } { \mathfrak { p } } / 2$ . Then, combining with the fact that $C ( u , v ) = O ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ , ( ) = ((log ) )we obtain that the minimum per-session multicast data rate is of order $\begin{array} { r } { O ( \frac { 1 } { n _ { s } \mathfrak { p } } \cdot C ( u , v ) ) } \end{array}$ 1nsp , which completes the proof.

( ( ))Combining Lemma 16 and Lemma 17, we get Theorem 2.

# VII. LITERATURE REVIEWS

In this section, we mainly review the networking–theoretic capacity bounds for wireless networks. We classify them in terms to the diversity of sessions.

Unicast Sessions: Gupta and Kumar [1] studied the unicast capacity for dense network under the threshold-based channel model. They show that classical multihop architectures with conventional single-user decoding and forwarding of packets can achieve the per-session throughput of order $O ( 1 / \sqrt { n } )$ , and (1 )that a scheme of nearest neighbor communication can achieve a throughput of order $\Theta ( 1 / { \sqrt { n \log n } } )$ . Later, Franceschetti et Θ(1 log )al. [7] showed the per-session throughput for random extended networks and random dense networks can both be achieved of order $O ( 1 / \sqrt { n } )$ . Note that their results are derived under (1 )the Gaussian Channel model. Xie and Kumar [3] have shown that the information-theoretic upper bound of unicast capacity for extended networks is also of order $O ( 1 / \sqrt { n } )$ when the power path loss exponent $\alpha > 6 ,$ (1 )which means that the classic 6multihop scheme is in fact order-optimal for $\alpha > 6 ,$ [14]. In 6fact, Xie and Kumar [15] successively improved the threshold on α for which multihop is order-optimal from  to .

6 4Broadcast Sessions: Under the threshold-based channel model, Keshavarz-Haddad et al. [16] studied the broadcast capacity of an arbitrary network. They showed that the persession broadcast capacity is only of $\Theta ( 1 / n )$ . The same Θ(1 )bound is proposed in [17]. In [18], Keshavarz-Haddad et al. studied the broadcast capacity with dynamic power adjustment for physical model. Under the Gaussian Channel model, Zheng [2], [19] proved that the per-session broadcast capacity for extended networks is ${ \frac { 1 } { n } } ( \log n ) ^ { - { \frac { \alpha } { 2 } } }$ . Wu et al. [20] (log )generalize the result to a general sized deployment square. The gap between the results of [2] and that of [16] means that for extended networks the assumption of the threshold-based channel model that each successful transmission can sustain a constant rate W is over-optimistic, because the value of W depends on n under more realistic channel models. The same effect could occur in unicast and multicast sessions.

Multicast Sessions: Earlier, Jacquet and Rodolakis [21] studied the scaling properties of multicast for random wireless networks. They showed that the maximum rate at which a node can transmit multicast data at rate of $O ( 1 / \sqrt { n _ { d } n \log n } )$ (1 log )order. Li et al. [10] and Shakkottai et al. [22] proposed results for multicast throughput of networks, respectively. Li et al. showed that, assuming that the number of multicast sessions is $n _ { s } = \Omega ( \log n _ { d } \cdot \sqrt { n \log n / n _ { d } } )$ [11], for random = Ω(log lognetworks, the per-session capacity of $n _ { s }$ )multicast sessions is $\Theta ( 1 / \sqrt { n _ { d } n \log n } )$ when $n _ { d } = O ( n / \log n )$ , and is $\Theta ( 1 / n )$ Θ(when $n _ { d } = \Omega ( n / \log n )$ = ( log ) Θ(1 ). Shakkottai’s result can be regarded as = Ω( log )a special case of Li’s [11]. They studied the multicast capacity of random networks when the number of multicast sources is $n ^ { \varepsilon }$ for some $\varepsilon > 0 ,$ and the number of receivers per multicast session is $n ^ { 1 - \varepsilon }$ 0. They proposed a novel routing scheme, called comb scheme, by which the per-session throughput can achieve order $\Theta ( 1 / \sqrt { n _ { d } n \log n } )$ . All above results for multicast capac-Θ(1 log )ity is derived under the threshold-based channel model.

Recently, Li et al. [23] studied the multicast capacity of random networks under Gaussian Channel Model. They show that, when $\begin{array} { r } { n _ { d } ~ = ~ O ( \frac { n } { ( \log n ) ^ { 2 \alpha + 6 } } ) } \end{array}$ and $n _ { s } ~ = ~ \Omega ( n ^ { \frac { 1 } { 2 } + \not \theta } )$ , the = ( (log ) ) = Ω( )per-session multicast throughput can be achieved of order $\Omega \big ( \frac { \sqrt { n } } { n _ { s } \sqrt { n _ { d } } } \big )$ , where $\theta > 0$ is any positive constant. Keshavarz-Ω(  ) 0Haddad et al. [9] proposed a technique called arena that is a novel tool to study upper bounds of capacity for wireless networks. Successively, they [8] studied the multicast capacity for dense networks. They also sketched schemes and estimated the throughput achieved by their method.

# VIII. CONCLUSION

In this paper, we focus on the networking-theoretic multicast capacity bounds for both random extended networks (REN) and random dense networks (RDN) under Gaussian Channel model. Based on percolation theory, we propose two multicast schemes for REN and derive the achievable throughput taking account of all $n _ { s }$ and $n _ { d } .$ . We show that under the assumption of $n _ { s } = \Theta ( n )$ , the per-session multicast throughput derived by = Θ( )our scheme is order-optimal when $\begin{array} { r } { n _ { d } = O \big ( \frac { n } { ( \log n ) ^ { \alpha + 1 } } \big ) } \end{array}$ or $n _ { d } =$ n n $\Omega ( { \frac { n } { \log n } } )$ = ( (log ) ) =. When the schemes are extended to random dense Ω( log )networks, we analyze the difference between REN and RDN in terms of capacity and adapt the schemes for RDN. We show that for RDN, the per-session multicast throughput derived by our scheme is order-optimal when $\begin{array} { r } { n _ { d } \ = \ O ( \frac { n } { ( \log n ) ^ { 3 } } ) } \end{array}$ or $\begin{array} { r } { n _ { d } = \Omega \big ( \frac { n } { \log n } \big ) } \end{array}$ = ( (log ) ). There are still gaps between the lower bounds = Ω( log )and upper bounds of multicast capacity for some ranges of $n _ { d } ,$ i.e., nd   n n 3 , $i . e . , n _ { d } : [ \frac { n } { ( \log n ) ^ { 3 } } , \frac { n } { \log n } ]$ n n  for RDN and nd   n n α + 1 , n n $n _ { d } : [ \frac { n } { ( \log n ) ^ { \alpha + 1 } } , \frac { n } { \log n } ]$ : [ (log ) log ] : [ (log ) log ]for REN. An interesting and challenging issue is to close the gaps on multicast capacity by presenting possibly new tighter upper bounds, and lower bounds, and designing corresponding algorithms to achieve the asymptotic multicast capacity.

# ACKNOWLEDGMENTS

This work is partially supported by the National Natural Science Funds under Grant No. 60534060, the National High Technology Research and Development Program of China (863 Program) under Grants No. 2007AA01Z136, No. 2007AA01Z149, No. 2007AA01Z180, Shanghai International Cooperation Project under Grant No. 075107005. The research of Xiang-Yang Li is also partially supported by NSF CNS-0832120, NSF CCF-0515088, National Natural Science Foundation of China under Grant No. 60828003, National Basic Research Program of China (973 Program) under grant No. 2006CB30300, Hong Kong RGC HKUST 6169/07, the RGC under Grant HKBU 2104/06E, and CERG under Grant PolyU-5232/07E.

# REFERENCES

[1] P. Gupta and P. R. Kumar, “The capacity of wireless networks,” IEEE Trans. on Information Theory, vol. 46, no. 2, pp. 388–404, 2000.

[2] R. Zheng, “Asymptotic bounds of information dissemination in powerconstrained wireless networks,” IEEE Trans. on Wireless Communications, vol. 7, no. 1, pp. 251–259, Jan. 2008.   
[3] L. Xie and P. Kumar, “A network information theory for wireless communication: scaling laws and optimal operation,” IEEE Trans. on Information Theory, vol. 50, no. 5, pp. 748–767, 2004.   
[4] S. Kulkarni and P. Viswanath, “A deterministic approach to throughput scaling in wireless networks,” IEEE Trans. on Information Theory, vol. 50, no. 6, pp. 1041–1049, 2004.   
[5] S. Toumpis and A. J. Goldsmith, “Capacity regions for wireless ad hoc networks,” IEEE Trans. on Wireless Communications, vol. 2, no. 4, pp. 736–748, 2003.   
[6] T. M. Cover and J. A. Thomas, Elements of Information Theory. New York: Wiley, 1991.   
[7] M. Franceschetti, O. Dousse, D. Tse, and P. Thiran, “Closing the gap in the capacity of wireless networks via percolation theory,” IEEE Trans. on Information Theory, vol. 53, no. 3, pp. 1009–1018, 2007.   
[8] A. Keshavarz-Haddad and R. Riedi, “Multicast capacity of large homogeneous multihop wireless networks,” in Proc. IEEE WiOpt 2008.   
[9] A. Keshavarz-Haddad and R. Riedi, “Bounds for the capacity of wireless multihop networks imposed by topology and demand,” in Proc. ACM MobiHoc 2007.   
[10] X. Li, S. Tang, and F. Ophir, “Multicast capacity for large scale wireless ad hoc networks,” in Proc. ACM Mobicom 2007.   
[11] X.-Y. Li, “Multicast capacity of wireless ad hoc networks,” IEEE/ACM Tracsaction on Networking, January, 2008.   
[12] C. Wang, X.-Y. Li, C. Jiang, S. Tang, and Y. Liu, “Scaling laws of networking-theoretic bounds on capacity for wireless networks,” CS of IIT, available at http://www.cs.iit.edu/ xli/paper/Submitted/multicastcapacity-full.pdf, Tech. Rep., 2008.   
[13] M. Penrose, “The longest edge of the random minimal spanning tree,” Annals of Applied Probability, vol. 7, pp. 340–361, 1997.   
[14] A. Ozg ¨ Ur, O. L ¨ Ev´ Eque, and D. Tse, “Hierarchical Cooperation Achieves ˆ Optimal Capacity Scaling in Ad Hoc Networks,” IEEE Trans. on Information Theory, vol. 53, no. 10, pp. 3549–3572, 2007.   
[15] L. Xie and P. Kumar, “On the path-loss attenuation regime for positive cost and linear scaling of transport capacity in wireless networks,” IEEE/ACM Trans. on Networking, vol. 14, pp. 2313–2328, 2006.   
[16] A. Keshavarz-Haddad, V. Ribeiro, and R. Riedi, “Broadcast capacity in multihop wireless networks,” in Proc. ACM MobiCom 2006.   
[17] B. Tavli, “Broadcast capacity of wireless networks,” IEEE Communications Letters, vol. 10, no. 2, pp. 68–69, 2006.   
[18] A. Keshavarz-Haddad and R. Riedi, “On the broadcast capacity of multihop wireless networks: Interplay of power, density and interference,” in Proc. IEEE SECON 2007.   
[19] R. Zheng, “Information dissemination in power-constrained wireless networks,” in Proc. IEEE INFOCOM 2006.   
[20] Y.-W. Wu, J. Zhao, X.-Y. Li, S.-J. Tang, X.-H. Xu, and X.-F. Mao, “Broadcast capacity forwireless ad hoc networks,” in Proc. IEEE MASS 2008.   
[21] P. Jacquet and G. Rodolakis, “Multicast scaling properties in massively dense ad hoc networks,” in Proc. 11th Int. Conf. on Parrallel and Distri. Syst. - Workshops, 2005.   
[22] X. Shakkottai, S. Liu, and R. Srikant, “The multicast capacity of large multihop wireless networks,” in Proc. ACM MobiHoc 2007.   
[23] S. Li, Y. Liu, and X.-Y. Li, “Capacity of large scale wireless networks under gaussian channel model,” in Proc. ACM Mobicom 2008.

# APPENDIX

Proof of Lemma 14: We prove the lemma using some existing results under protocol model, especially the area argument in [10]. Based on the original network under Gaussian channel model, we construct a new network under protocol model as follows.

1) Set each node’s transmission range as g, i.e., the side length of each cell in $\mathbb { L } ( a , g )$ .   
( )2) Add some artificial “additional relay nodes” $v _ { a }$ such that any pair of nodes will have enough relay nodes along its link to make sure that the minimum number of cells the routing path crosses under protocol model is no more than

the number of cells the direct link will cross in Gaussian channel model. Notice that $v _ { a }$ cannot be selected as source or receivers, they can only act as relay nodes.

Let T be any multicast tree in original network under Gaussian channel model and $T _ { p }$ denote the corresponding multicast tree (spanning the same multicast session) constructed on the network under protocol model. Denote the area covered by the multicast tree $T _ { p } , i . e .$ , the union of its nodes’ transmitting disks as $| D ( T _ { p } )$ |. We have two important observations here:

( )1) Our preceding two modifications will not affect the proof for Lemma 11 in [11]. In other words, the lower bound on $| D ( T _ { p } ) |$ | still holds,   
( )2) Furthermore, any link in Gaussian channel model can be simulated by using these artificial “additional relay nodes” in the protocol model such that the number of cells it will cross is not increased. So the lower bound of N T is no smaller than the lower bound of $N ( T _ { p } )$ .

( )According to Lemma 11 of [11], we get that $D ( T _ { p } ) = \Omega ( { \sqrt { n _ { d } } } .$ $a \cdot g )$ ( ) = Ω(. Since one transmitting disk can cover no more than 4 )cells. We have, w.h.p., $\begin{array} { r } { N ( T _ { p } ) = \Omega ( \frac { 1 } { q } \cdot \sqrt { n _ { d } } \cdot a ) } \end{array}$ . Hence, when $\begin{array} { r } { n _ { d } = O ( \frac { a ^ { 2 } } { g ^ { 2 } } ) , w . h . p . , N ( T ) = \Omega ( \frac { 1 } { g } \cdot \sqrt { n _ { d } } \cdot a ) } \end{array}$ . Combining with the fact that | ${ \mathrm { E M S T } } | \leq 2 { \sqrt { 2 } } { \sqrt { n _ { d } } } \cdot a$ for any given multicast EMST 2 2session ( [11]), we complete the proof.

Proof of Lemma 16: Firstly, we define a random variable $\begin{array} { r } { F { : = } \sum _ { k = 1 } ^ { n _ { s } } N ( T _ { k } ) } \end{array}$ -: -k ns . Based on Lemma 14, we have that there = =1 (exists a constant $\nu _ { 1 } > 0$ such that w.h $\cdot p .$ .,

$$
F \geq \nu_ {1} \cdot \sum_ {k = 1} ^ {n _ {s}} | \operatorname{EMST} (\mathcal {M} _ {k}) | \tag {12}
$$

Define a sequence of random variables:

$$
X _ {q} = \sum_ {j = 1} ^ {q} (| \operatorname{EMST} (\mathcal {M} _ {j}) | - E (| \operatorname{EMST} (\mathcal {M} _ {j}) |))
$$

Then $E ( X _ { q + 1 } | X _ { 1 } , \cdot \cdot \cdot , X _ { q } ) = X _ { q }$ , which means that the variables $X _ { i }$ ( +1 1 ) =are martingale (Lemma 2). In addition, $X _ { q } - X _ { q - 1 } =$ $| \operatorname { E M S T } ( \mathcal { M } _ { q } ) | - E ( | \operatorname { E M S T } ( \mathcal { M } _ { q } ) | )$ 1 =. Combining Lemma 9 and EMST( ) ( EMSTLemma 10 in [11], we have $| X _ { q } - X _ { q - 1 } | = O ( { \sqrt { n n _ { d } } } )$ . Hence, let $X _ { 0 } \equiv 0$ 1 = ( ), from Azuma’s Inequality, there exists a constant $\nu _ { 2 } > 0$ 0such that

$$
\operatorname * {P r} (| X _ {n _ {s}} - X _ {0} | \geq \delta) \leq 2 \exp (- \frac {\delta^ {2}}{2 \nu_ {2} ^ {2} \cdot n _ {s} \cdot n _ {d} \cdot n}). \tag {13}
$$

Let $\begin{array} { r } { \delta \ = \ \frac { 1 } { 2 } \cdot \sum _ { i = 1 } ^ { n _ { s } } E ( | \mathrm { E M S T } ( \mathcal { M } _ { i } ) | ) } \end{array}$ 2. Then, there are some√ = 2 =1 ( EMconstant ν and ν such that $\nu _ { 3 } { \cdot } n _ { s } { \cdot } \sqrt { n n _ { d } } \leq \delta \leq \nu _ { 4 } { \cdot } n _ { s } { \cdot } \sqrt { n n _ { d } } .$ 3 4By Equation (13), we have

$$
\operatorname * {P r} (\sum_ {k = 1} ^ {n _ {s}} | \mathrm{EMST} (\mathcal {M} _ {k}) | \leq \delta) \leq 2 \exp (- \frac {\nu_ {3} ^ {2}}{2 \nu_ {2} ^ {2}} \cdot n _ {s}) \tag {14}
$$

According to Equation (12) and Equation (14), we can obtain that $\begin{array} { r } { \operatorname* { P r } ( F \geq \nu _ { 1 } \nu _ { 3 } \cdot n _ { s } \sqrt { n _ { d } n } ) \geq 1 - 2 \exp ( - \frac { \nu _ { 3 } ^ { 2 } } { 2 \nu _ { \ast } ^ { 2 } } \cdot n _ { s } ) } \end{array}$ . Thus, by pigeonhole principle, w. $h . p .$ 2 ., there is at least one cell that will be used by at least $\Omega ( \frac { \bar { n } _ { s } \sqrt { n _ { d } n } } { m ^ { 2 } } )$ m2 , i.e., $\Omega \big ( \frac { n _ { s } \sqrt { n _ { d } } } { \sqrt { n } } \big )$ flows. Ω( ) Ω( )By Lemma 15, the total throughput capacity of any cell in $\mathbb { L } ( { \sqrt { n } } , c )$ is of order O . Thus, due to the congestion in some cells, the minimum per-session throusupported by using any strategy is of order $\begin{array} { r } { O \big ( \frac { \sqrt { n } } { n _ { s } \sqrt { n _ { d } } } \big ) } \end{array}$ can be.