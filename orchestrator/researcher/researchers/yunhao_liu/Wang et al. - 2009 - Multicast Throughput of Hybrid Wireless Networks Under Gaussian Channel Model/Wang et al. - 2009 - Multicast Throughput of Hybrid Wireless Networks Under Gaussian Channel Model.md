# Multicast Throughput of Hybrid Wireless Networks Under Gaussian Channel Model

Cheng Wang∗§, Shaojie Tang†, Xiang-Yang Li†, Changjun Jiang∗§ and Yunhao Liu‡

∗ Department of Computer Science and Technology, Tongji University, Shanghai, China

† Department of Computer Science, Illinois Institute of Technology, Chicago, IL, 60616

‡ Department of Computer Science and Engineering, Hong Kong University of Science and Technology

§ Key Laboratory of Embedded System and Service Computing, Ministry of Education, Shanghai, China

# Abstract

We study the multicast capacity for hybrid wireless networks consisting of ordinary wireless nodes and base stations under Gaussian Channel model, which generalizes both the unicast capacity and broadcast capacity for hybrid wireless networks. We simply consider the hybrid extended network, where the ordinary wireless nodes are placed in the square region A n with side-length n according to a Poisson point process with unit intensity. In addition, m additional base stations (BSs) serving as the relay gateway are placed regularly in the region A n and they are connected by a high-bandwidth wired network. Three broad categories of multicast strategies are proposed in this paper. According to the different scenarios in terms of m, n and nd, we select the optimal scheme from the three categories of strategies, and derive the achievable multicast throughput based on the optimal decision.

# 1. Introduction

The asymptotic capacity for wireless ad hoc networks has been intensively studied under different channel models. Most existing related work are based on two types of channel models. The first is the threshold-based channel model that defines the transmission rate as a binary function. The protocol interference model (PrIM) and physical interference model (PhIM) [3] both belong to the threshold-based channel model. The second is the Gaussian Channel model that determines the transmission rate based on a continuous function of the receiver’s SINR (Signal to Interference plus Noise Ratio). Gaussian Channel model captures better physical layer of wireless networks than threshold-based channel model.

A hybrid wireless network (HN) consists of two types of network terminals: base stations and ordinary wireless nodes. Assume that all base stations can communicate with wireless nodes, and further assume that each base station is neither a source nor a receiver, it simply serves as a relay gateway. The multicast capacity can unify the unicast and broadcast capacity, [7], [8], which increases the generality of the research on multicast capacity for HN. For HNs, there are also generally two channel models as in most existing work for wireless ad hoc networks. Since all existing results of capacity for hybrid networks are derived under the thresholdbased model, [11], a natural and interesting issue arises: What is the multicast capacity for hybrid networks when the Gaussian channel model is used. This paper aims to derive an achievable multicast throughput for HN under Gaussian channel model.

We consider hybrid extended network (HEN) in which the ordinary wireless nodes are placed in the square region A n ( )with side-length n according to a Poisson point process with unit intensity, and m additional base stations (BSs) serving as the relay gateway are placed regularly in the region A n . Furthermore, we assume all base stations are ( )connected by a high-bandwidth wired network. Assume that there are ns random multicast flows, each with randomly chosen nd receivers. According to different cases in terms of m, n and nd, we adopt different types of multicast strategies. To be specific, we propose three broad categories of multicast strategies. The first is called the hybrid strategy, i.e., the multihop scheme with BS-supported, which further consists of two types of strategies called connectivity strategy and percolation strategy respectively. The second is the ordinary ad hoc strategy, i.e., the multihop scheme without any BS-supported. The third is the classical BS-based network protocol, i.e., any communications between ordinary nodes are relayed by some specific BSs. According to the different scenarios of m, n and nd, we select the optimal scheme from the three categories of strategies, and derive the achievable multicast throughput based on the optimal scheme. To the best of our knowledge, this is the first work that addresses the optimum multicast routing and scheduling strategy in hybrid wireless networks under Gaussian channel model.

The rest paper is structured as follows. In Section 2, we introduce the network model. Main results are presented and discussed in Section 3. We make technical preparations in Section 4. In Section 5, we design the multicast schemes for HEN. In Section 6, we review the related existing literature. We conclude the paper in Section 7.

# 2. Network Model

Throughout this paper, we are mainly concerned with events that happen with high probability (w.h.p.).

# 2.1. Network topology and Channel Model

We construct a random extended network by placing ordinary nodes according to a Poisson point process (p.p.p.) of unit intensity on the 2-dimension plane and focusing on the square $\mathcal { A } ( n ) = [ 0 , \sqrt { n } ] ^ { 2 }$ . By Chebyshev’s Inequal-( ) = [0 ]ity (Lemma 1), we easily obtain that, w.h.p. the number of nodes in $\mathcal { A } ( n )$ is within $( ( 1 - \varepsilon ) n , ( 1 + \varepsilon ) n )$ , where $\varepsilon > 0$ ( ) ((1 ) (1 + ) )is an arbitrarily small constant. To simplify the de-0scription, we assume that the number of nodes is $n ,$ without changing our results in order sense, [2], [16]. Furthermore, we place regularly a number of base stations (BSs, with wireless transmission power $P )$ in the region $\mathcal { A } ( n )$ , and ( )they are connected using a high-bandwidth wired network, to construct the hybrid extended network. We assume that the number of BSs m is of order $O ( n )$ . As in most ( )existing work, we further assume that the number of source nodes $n _ { s } ~ = ~ \Theta ( n )$ . Assume that all nodes transmit with = Θ(a constant power $P ,$ , and any two nodes can establish a direct communication link over a channel of bandwidth B, of rate R(vi, vj ) = B log(1 + P ·-(vi,vj N0  - v A(i) P $\begin{array} { r } { R ( v _ { i } , v _ { j } ) = B \log ( 1 + \frac { P \cdot \ell ( v _ { i } , v _ { j } ) } { N _ { 0 } + \sum _ { n } \ldots R \cdot \ell ( v _ { k } , v _ { j } ) } ) } \end{array}$ , where $N _ { 0 } > 0$ is the ambient noise power, $\overset { \triangledown } { \boldsymbol { A } } ( i )$ is the set of nodes 0 0that transmit when $v _ { i }$ ( )is scheduled. Let the power attenuation function be $\ell ( v _ { i } , v _ { j } ) = \operatorname* { m i n } \{ 1 , \ d _ { i j } ^ { - \alpha } \}$ with $\alpha > 2$ , where $d _ { i j }$ ( ) = min 1represents the Euclidean distance between $v _ { i }$ 2and $v _ { j }$ .

# 2.2. Achievable multicast throughput

The achievable multicast throughput is indeed a lower bound of the multicast capacity. In this paper, we follow the formal definitions of capacity in [7], [8], and we focus on the minimum per-session multicast capacity. Other two types of capacity, i.e., average per-session multicast capacity and aggregated multicast capacity, can be straightforwardly derived based on minimum per-session multicast capacity.

NOTATIONS: For a 2-dimension line segment $L = u v .$ , let =|L| represent the Euclidean distance between u and v; for a discrete set $U _ { : }$ let |U | represent its cardinality. For a continuous region A, we use $\lVert \boldsymbol { A } \rVert$ to denote its area; for a tree T (or a forest $\mathcal { F } )$ , we use $\| { \mathcal { T } } \| ~ ( \operatorname { o r } \| { \mathcal { F } } \| )$ to denote its total Euclidean edge length. To simplify the description, let $\theta ( n ) \colon [ \theta _ { 1 } ( n ) , \theta _ { 2 } ( n ) ]$ represent that $\theta ( n ) = \Omega ( \theta _ { 1 } ( n ) )$ and $\theta ( n ) = O ( \theta _ { 2 } ( n ) ) ;$ ( )] and let $\theta ( n ) \colon ( \theta _ { 1 } ( n ) , \theta _ { 2 } ( n ) ]$ Ω( 1( ))represent that $\theta ( n ) = \omega ( \theta _ { 1 } ( n ) )$ ) and $\theta ( n ) = O ( \theta _ { 2 } ( n ) )$ .

# 3. Main Results

In this paper, we design three types of routing strategies for a given hybrid wireless network, namely, ordinary ad hoc strategy, BS-based strategy and hybrid strategy. Please see Fig. 1 for illustration.

1) Ordinary ad hoc strategy will not use any base station for relay. In other words, we treat the hybrid network as a pure ad hoc network by ignoring base stations;   
2) BS-based strategy only allow receivers (or source nodes) to communicate with base stations in corresponding

![](images/c325eeee5e41a6a759bc0355d7b2edf045b0f86a16351c0848200c29e08693ac.jpg)



(a) Original network

![](images/55b749790656ff9751b73f7dc513b1fcf2224a852eb77ba8589b2b6c952b462d.jpg)



(b) Ordinary ad hoc strategy

![](images/be72bbbcc6613f91f721c67b3e99b1f553b7114401915a370697cd7aba32e44b.jpg)



(c) BS-based strategy

![](images/a1fb9934bf36a9ab1290631bbfa623adcf4889abc241da276392e141fa619990.jpg)



(d) Hybrid routing strategy   
Figure 1. Illustrations of three routing strategies. The big dark nodes represent the BSs, small dark node represents a source node, and small gray nodes represent the $n _ { d }$ receivers.

subregion directly, i.e., we do not allow any ordinary node to serve as relay node in each subregion.

3) Hybrid strategy uses a specific routing and scheduling scheme to let receivers (or source nodes) communicate with central base stations in corresponding subregion. In particular, we can use the other ordinary wireless nodes in same subregion to relay data.

According to different scenarios in terms of $m ,$ n and $n _ { d } .$ we select the best scheme from the three categories of strategies, and derive the achievable multicast throughput based on the optimal scheme. The multicast throughput derived by them are presented in Theorem 6, Theorem 7 and Theorem 8, respectively. By combining them, we can obtain the achievable throughput for HEN.

# 3.1. Optimal Decision

Theorem 1: Combining three types of routing strategies, the optimal decision is made as follows.

Case 1: When m: $[ 1 , n / ( \log n ) ^ { \alpha + 1 } ]$

$1 ) \operatorname { I f } { \left\{ \begin{array} { l l } { n _ { d } : [ 1 , n / ( \log n ) ^ { 3 \alpha + 2 } ] { \mathrm { ~ a n d ~ } } } \\ { m : [ { \sqrt { n n _ { d } \cdot ( \log n ) ^ { \alpha } } } , n / ( \log n ) ^ { \alpha + 1 } ] } \end{array} \right. }$

The hybrid strategy is adopted, by which the throughput is of order $\Omega ( \frac { m } { n \cdot n _ { d } } ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

2) Otherwise, the ordinary ad hoc strategy is adopted. The throughput is described in Theorem $^ { 7 }$ .

Case 2: When m: $[ n / ( \log n ) ^ { \alpha + 1 } , n / \log n ]$

$1 ) \operatorname { I f } { \left\{ \begin{array} { l l } { n _ { d } : \left[ 1 , n / ( \log n ) ^ { \alpha + 2 } \right] { \mathrm { ~ a n d ~ } } } \\ { m : \left[ { \sqrt { n n _ { d } \cdot ( \log n ) ^ { \alpha } } } , n / \log n \right] } \end{array} \right. }$

The hybrid strategy is adopted, by which the throughput is of order  mn nd $\begin{array} { r } { \Omega ( \frac { m } { n \cdot n _ { d } } ( \log n ) ^ { - \frac { \alpha } { 2 } } ) } \end{array}$ .

2) Otherwise, the ordinary ad hoc strategy is adopted. The achievable throughput is described in Theorem 7.

Case 3: When m: $[ n / \log n , n ]$ , the BS-based strategy is [ log ]adopted. The throughput is described in Theorem 8.

# 3.2. Discussion for results

Generality of the results: Due to the generality of multicast sessions, i.e., unicast and broadcast can be regarded as the specific cases of multicast, our result can unify the throughput for unicast and broadcast by letting $n _ { d } = 1$ and $n _ { d } = n - 1$ , respectively. However, when we specialize to = 1unicast throughput, i.e., let $n _ { d } = 1$ , there is indeed a gap of factor $( \log n ) ^ { - { \frac { \alpha } { 2 } } }$ = 1between our result and the result in [10]. (log )In fact, for the routing of [10], the ordinary nodes in each subregion access to the corresponding base station via the connectivity paths defined in Section 5 of this paper.

Analysis of bottleneck: As in most existing work for the capacity of hybrid networks, we also assume the links between base stations and ordinary wireless nodes (we call such links B-O links) have no difference from those between ordinary wireless nodes. While, in the analysis of bottlenecks on three types of strategies (Section 5), we find that for most cases in terms of m and $n _ { d } ,$ the bottlenecks are on B-O links. Therefore, if the bandwidth of B-O links can be increased, the throughput for the whole network should possibly be enhanced. Hence, when we consider the hybrid strategies, we designedly derive the throughput without taking the possible bottlenecks on the B-O links into account. (Please see detail in Theorem 2 and Theorem 4.) Our results could be used to derive new capacity results when some new assumptions are made for the B-O links.

Matching upper bounds: As far as we know, even for wireless ad hoc networks, there are still no matching upper bounds and lower bounds for multicast capacity under Gaussian Channel model. The same question holds for hybrid networks case. Then it is also an interesting issue to be studied as our further work.

# 4. Technical Preparations

Probability inequality: Firstly, we recall some useful probability inequalities.

Lemma 1 (Chebyshev’s Inequality): Let X be a random variable, then $\operatorname* { P r } ( | X - \mu | \geq \epsilon ) \leq \operatorname { V a r } ( X ) / \epsilon ^ { 2 }$ , where $\mu =$ Pr( ) (E X , Var X is the variance of X, and $\epsilon > 0$ .

( ) ( ) 0In the following analysis, we often need to prove the uniform convergence in the probability of some events. Vapnik-Chervonenkis Theorem [12] is usually exploited to prove the uniform convergence, as in [3], [6], [8]. When the deployment region A is partitioned into a lattice consisting of subsquares that act as Voronoi cells, the exponent tails of probability bound can be equally used to prove the uniform convergence of some probability.

Lemma 2 (Tails of Chernoff bound): Let X be a Poisson random variable with parameter λ. Then

$$
\operatorname * {P r} (X \geq x) \leq e ^ {- \lambda} (e \lambda) ^ {x} / x ^ {x}, \quad \text { for } x > \lambda . \tag {1}
$$

$$
\operatorname * {P r} (X \leq x) \leq e ^ {- \lambda} (e \lambda) ^ {x} / x ^ {x}, \quad \text { for } 0 <   x <   \lambda . \tag {2}
$$

Euclidean spanning tree: Partition the square $\mathcal A ( a )$ into $\rho \le m$ subsquares $S _ { 1 } , S _ { 2 } , \cdots , S _ { \rho }$ ( )called subregions each with side length ${ \sqrt { a } } / \rho$ 1 2while ensuring that there is one base station, say $b _ { \iota }$ , at the center of each subregion $S _ { \iota }$ . Here a is the area of the deployment square region. Notice that one subregion may contain more than one base stations, but we only need to use the central one in our proposed routing scheme. For each multicast session $\mathcal { M } _ { k } , k = 1 , 2 , \cdot \cdot \cdot n _ { s } .$ , we denote the spanning set as $U _ { k } = \{ v _ { k } \} \cup \{ v _ { k _ { 1 } } , v _ { k _ { 2 } } , \cdot \cdot \cdot v _ { k _ { n _ { d } } } \}$ , where $v _ { k }$ = is the source node and the nodes in the latter set are the destinations of $v _ { k }$ . Let $U _ { k } ^ { \iota } \ = \ \{ v _ { k _ { 1 } } ^ { \iota } , v _ { k _ { 2 } } ^ { \iota } , \cdot \cdot \cdot , v _ { k _ { t } } ^ { \iota } \}$ denote the subset of $U _ { k }$ =that are contained in the subregion $S _ { \iota }$ , where $\textstyle U _ { k } = \bigcup _ { \iota = 1 } ^ { \rho } U _ { k } ^ { \iota }$ and $U _ { k } ^ { \iota _ { 1 } } \cup U _ { k } ^ { \iota _ { 2 } } = \varnothing$ for any $\iota _ { 1 } \neq$ $\iota _ { 2 }$ . Let $\tilde { U } _ { k } ^ { \iota } = U _ { k } ^ { \iota } \cup \{ b _ { \iota } \}$ = 1 =. Then we can build an Euclidean 2 =spanning tree (EST) of every set $\tilde { U } _ { k } ^ { \iota }$ using the method in [7], [8]. Denote those ESTs as $\mathrm { E S T } ( \tilde { U } _ { k } ^ { \iota } ) , 1 \leq \iota \leq \varphi _ { k }$ , where $\varphi _ { k }$ is a random variable representing the number of occupied subregions, i.e., those containing at least one ordinary node in $U _ { k }$ . Notice that for each $\tilde { U } _ { k } ^ { \iota }$ except for that one including $v _ { k }$ (denoted as $\tilde { U } _ { k } ^ { \iota _ { o } } ) , ~ b _ { \iota }$ ˜ acts as the root of EST; for $\tilde { U } _ { k } ^ { \iota _ { o } }$ , $v _ { k }$ acts as the root. These ESTs will be connected by links among base stations.

We first study a uniform bound of $\varphi _ { k } , \ k = 1 , 2 , \cdots n _ { s }$ . Define the random variables $\begin{array} { r c l } { \varphi _ { m a x } } & { = } & { \operatorname* { m a x } _ { k } \{ \varphi _ { k } \} } \end{array}$ and $\varphi _ { m i n } = \mathrm { m i n } _ { k } \{ \varphi _ { k } \}$ = max. Much research has been done on the tail = minbounds for occupancy ( [4]). However, since we concentrate on the lower bounds on multicast capacity, we only need the following straightforward upper bound on $\varphi _ { m a x }$ (Lemma 3). Noticing that we should use the tail bounds for occupancy to lowerbound $\varphi _ { m i n }$ when we study the upper bound on multicast capacity.

Lemma $3 \colon \varphi _ { m a x } = \operatorname* { m a x } _ { k } \{ \varphi _ { k } \} = O ( \operatorname* { m i n } \{ n _ { d } , \rho \} )$ , w.h.p.

= max = (min )Next, we recall a result on the total length of the EST of a given set of nodes [7], [8].

Lemma 4: For the EST spanning a set of nodes U, denoted as EST U , we have $\| \mathrm { E S T } ( \bar { U } ) \| \le 2 \sqrt { 2 } \sqrt { | U | } \cdot \sqrt { a } .$ .

( )Denote the forest consisting of all $\mathrm { E S T } ( \tilde { U } _ { k } ^ { \iota } ) ( 1 \leq \iota \leq \varphi _ { k } )$ , as $\mathcal { F } _ { k }$ . Then we have

Lemma 5: The total Euclidean edge length of $\mathcal { F } _ { k } ,$ , i.e., $\| \mathcal F _ { k } \|$ , is w.h.p.of order $O ( \frac { \sqrt { a } } { \sqrt { \rho } } \cdot \sqrt { n _ { d } \cdot \operatorname* { m i n } \{ n _ { d } , \rho \} } )$ , for any $k , 1 \leq k \leq n _ { s }$ .

1Please see the details of the proof in [15].

Result on bond percolation model [2]: Let $\mathbb { B } ( h , p )$ ( )denote a box with side length h embedded in the square lattice, where each edge (bond) is open with probability p. We call a path consisting of only open edges (bonds) open path. For a given $\kappa ~ > ~ 0$ , we partition the lattice graph $\mathbb { B } ( h , p )$ 0into horizontal (vertical) rectangle slabs with the horizontal (or vertical) width of h and the vertical (horizontal) width of κ $h - \epsilon ( h )$ , denoted as $R _ { i } ^ { h }$ (or $R _ { i } ^ { v } )$ . We can choose $\varepsilon _ { h }$ log ( )as the smallest value such that the number of rectangle slabs $h / ( \kappa \log h - \epsilon ( h ) )$ is an integer. It is obvious that $\epsilon ( h ) = o ( 1 )$ loas $h \to \infty$ ))[2]. Denote the number ( ) = (1)of edge-disjoint open paths in slab $R _ { i } ^ { h }$ (or $R _ { i } ^ { v } )$ as $N _ { i } ^ { h }$ (or $N _ { i } ^ { v } )$ . Let $N ^ { h } = \mathrm { { m i n } } _ { i } N _ { i } ^ { h } , N ^ { v } = \mathrm { { m i n } } _ { i } \bar { N } _ { i } ^ { v }$ Then,

![](images/dd476d11d5cc2a73d1983b1afc57ed5cb2f463ce4706cc212a3ec440504a42c9.jpg)



(a) connectivity paths

![](images/f554a5ca9a8c0ed5c64cdcc7aa63a2a402452a7946e5eec0b3b07b7a19d31aab.jpg)



(b) TDMA scheduling   
Figure 2. (a) The polygonal chains represent the connectivity paths. There are at least $\frac { \theta } { 2 }$ n connectivity paths in each 2column (or row). The shaded rectangles represent the halfcels. (b) The shaded cells can be scheduled simultaneously in a 9-TDMA scheme. Each time slot can be further divided into four subslots, and the four half-cells in each cell are scheduled one out of four subslots.

= min = minLemma 6: ( [2]) For any constants $\kappa > 0$ and $p \in ( \frac { 5 } { 6 } , 1 )$ satisfying $2 + \kappa \log ( 6 ( 1 - p ) ) < 0 ,$ 0 ( 6 1) there is a constant $\delta \ = \ \delta ( \kappa , p )$ + log(6(1such that $1 _ { h \to \infty } \operatorname* { P r } ( N ^ { h } \ \geq \ \delta \log h ) \ = \ 1 ;$ lim $_ { \cdot h \longrightarrow \infty } \operatorname* { P r } ( N ^ { v } \geq \delta \log h ) = 1$ .

m Pr( log ) = 1Bottleneck principle: If the adopted strategy is of hierarchical structure, then the bottleneck of the whole phase of multicast strategy determines the final throughput. That is,

Lemma $7 ;$ The achievable throughput derived by any multicast strategy  is ${ \Lambda = \operatorname* { m i n } \{ \Lambda _ { j } ; ~ j = 1 , 2 , \cdots , \tau \} }$ , Λ = min Λ ; = 1 2where we assume that the routing scheme  consists of constant τ phases and $\Lambda _ { j }$ is the throughput achievable in phase $j .$ .

Note that Lemma 7 does not hold if τ is not a constant.

# 5. Multicast Strategy and Throughput

We design three types of multicast strategies, i.e., hybrid strategy, ordinary ad hoc strategy and BS-based strategy, to obtain the achievable multicast throughput for hybrid extended network (HEN). A novel technique proposed in [14], called parallel transmission scheduling, is introduced. Recall that the bottleneck of the capacity achieving is not on the links between base stations (BSs) since they are connected using high bandwidth. However, the links between BSs and ordinary nodes are possible, actually often, becoming the bottleneck of the whole routing.

# 5.1. Hybrid Strategy for HEN

The hybrid strategy can be further classified into two different strategies called connectivity strategy and percolation strategy respectively.

5.1.1. Connectivity Strategy. The connectivity strategy is typically applied when $\rho = { O } \left( { n } \right/$ n . We denote connectivity strategy by $\bar { \mathfrak { I } } _ { e }$ = ( log ), the routing and wireless transmission scheduling by $\bar { \mathfrak { I } } _ { e } ^ { r }$ and $\bar { \mathcal { S } } _ { e } ^ { t }$ respectively. Divide $\mathcal { A } ( n )$ into subsquares with area $\bar { a } _ { e } = 2 \theta \cdot \log n .$ , where $\theta$ ( )is a constant satisfying $\begin{array} { r } { \theta > \frac { 2 } { 1 - \ln { 2 } } . } \end{array}$ ¯ = 2 log. We call those subsquares connectivity 1 ln 2cells. Furthermore, we separate each cell into halves horizontally (or vertically) called horizontal (or vertical) halfcells. Then according to Lemma 2 and union bounds, we can prove:

Lemma 8: With high probability, there are at most $2 \theta$ · n and at least $\frac { \theta } { 2 }$ 2·  n ordinary nodes in every half-cell.

g 2 logWe then discuss the routing scheme and transmission scheduling of $\bar { \mathfrak { I } } _ { e } .$ .

Routing scheme $\bar { \mathfrak { I } } _ { e } ^ { r }$ : We propose Algorithm 1 to construct the multicast routing tree $\mathcal { T } ( U _ { k } )$ for multicast session $\mathcal { M } _ { k }$ . For each edge $u _ { i } u _ { j } \in \mathrm { E S T } ( \tilde { U } _ { k } ^ { \iota } ) , 1 \le \iota \le \varphi _ { k }$ , we

# Algorithm 1 Connectivity Routing Scheme $\bar { \mathfrak { I } } _ { e } ^ { r }$

Input: $\mathrm { E S T } ( \tilde { U } _ { k } ^ { \iota } ) , 1 \leq \iota \leq \varphi _ { k }$

( ) 1Output: A multicast routing tree ${ \mathcal { T } } ( U _ { k } )$

1: for each $\operatorname { E S T } ( \tilde { U } _ { k } ^ { \iota } )$ do   
(2: for each link $u _ { i } u _ { j }$ in $\operatorname { E S T } ( \tilde { U } _ { k } ^ { \iota } )$ do   
3: Connect $u _ { i }$ and $u _ { j }$ ( )using Manhattan routing as follows:

Denote the intersection point of the horizontal line through $u _ { i }$ and the vertical line through $u _ { j }$ as $p _ { i , j }$ and denote the nearest node to point $p _ { i , j }$ as $u _ { i , j }$

Choose randomly a node in each half-cell passed by $u _ { i } u _ { i , j }$ and $u _ { j } u _ { i , j }$ , and connect alternately those nodes, as illustrated in Fig.2(a).

4: end for   
5: Merge the same edges (hops) and break the circles that have no impact on the connectivity of EST $( \tilde { U } _ { k } ^ { \iota } )$ , we obtain the multicast tree $\mathcal { T } ( U _ { k } ^ { \iota } )$ .   
6: end for   
7: Based on the forest consisting of the constructed trees, i.e., ${ \cal T } ( U _ { k } ^ { \iota } ) \ : ( 1 \leq \iota \leq \varphi _ { k } ) $ , we obtain the final multicast tree $\mathcal { T } ( U _ { k } )$ 1by building an EST spanning the set of base (stations $b _ { \iota } ( 1 \leq \iota \leq \varphi _ { k } ) .$ .

use Manhattan routing to realize it. Notice that each hop in Manhattan routing connects two nodes belonging to two adjacent connectivity cells but nonadjacent horizontal (or vertical) half-cells, which ensures that the Euclidean length of each hop is at most $\frac { \sqrt { 1 3 } } { 2 } \sqrt { \bar { a } _ { e } }$ and at least $\scriptstyle { \frac { 1 } { 2 } } \sqrt { \bar { a } _ { e } }$ . We call 2 ¯ 2 ¯such paths connectivity paths. According to Lemma 8, there $\frac { \theta } { 2 }$ log n connectivity paths in each slab of sizeence, we can allocate the total traffic of each $\sqrt { \bar { a } _ { e } } \times \sqrt { n }$ ¯slab to such $\frac { \theta } { 2 }$ n connectivity paths averagely.

2 logTransmission scheduling $\bar { \mathfrak { P } } _ { e } ^ { t } \colon$ We adopt a 9-TDMA scheme, and further divide each time slot into 4 equal subslots during which we schedule in turn the four halfcells of each cell $\left( \mathrm { F i g . 2 ( b ) } \right)$ . The main technique used here is parallel transmission scheduling: In each activated subslot, we schedule simultaneously $\frac { \bar { \theta } } { 2 }$ ·  n parallel links (the 2 logexistence of these links is ensured by Lemma $^ { 8 ) }$ instead of scheduling only one link in the previous work. We further prove that

Lemma 9: By the parallel transmission scheduling ${ \bar { \mathbb { S } } } _ { e } ^ { t } ,$ the rate along each connectivity path can be achieved is of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

Ω((log ) )Please see the detailed proof in [15].

Throughput achieved by $\bar { \mathfrak { I } } _ { e } { \ : : }$ First, we consider the relay burden of each connectivity path.

Lemma 10: By the routing scheme $\bar { \mathfrak { I } } _ { e } ^ { r } .$ , the relay burden of the nodes on connectivity paths is at most of order

$$
\bar {L} _ {e} ^ {r} = \left\{ \begin{array}{l l} O (n _ {d} \sqrt {n} / \sqrt {\rho \log n}) & \text { when } n _ {d}: [ 1, \rho ] \\ O (\sqrt {n n _ {d}} / \sqrt {\log n}) & \text { when } n _ {d}: [ \rho , n / \log n ] \\ O (n _ {d}) & \text { when } n _ {d}: [ n / \log n, n ] \end{array} \right.
$$

Proof: Given a node $\bar { v } _ { t } ^ { * }$ on a connectivity path, define ¯the number of multicast sessions routed through $\bar { v } _ { t } ^ { * }$ as a random variable $\bar { \xi } _ { t } .$ ¯. We consider the uniform upper bound $\bar { \xi }$ of $\bar { \xi } _ { t }$ for every node. Define an event $\bar { E } _ { e } ^ { r } ( k , t )$ as the multicast session $\mathcal { M } _ { k }$ passes through $\bar { v } _ { t } ^ { * }$ ( ). Obviously, if $\bar { E } _ { e } ^ { r } ( k , t )$ ¯happens then there exists an edge $u _ { i } u _ { j } \in \mathcal { F } _ { k }$ that ( )is routed through $\bar { v } _ { t } ^ { * }$ , i.e., $u _ { i } u _ { i , j }$ or $u _ { i , j } u _ { j }$ passes through $\bar { v } _ { t } ^ { * }$ ¯. Since there exists a constant $\varrho _ { 1 }$ such that

$$
\left| u _ {i} u _ {i, j} \right| \leq \left| u _ {i} p _ {i, j} \right| + \varrho_ {1} \cdot \sqrt {\bar {a} _ {e}}, \quad \left| u _ {i, j} u _ {j} \right| \leq \left| p _ {i, j} u _ {j} \right| + \varrho_ {1} \cdot \sqrt {\bar {a} _ {e}}
$$

and for $| u _ { i } p _ { i , j } | + | p _ { i , j } u _ { j } | \le \sqrt { 2 } | u _ { i } u _ { j } |$ |, we have

$$
\begin{array}{l} \operatorname * {P r} (\bar {E} _ {e} ^ {r} (k, t)) \\ \leq \frac {1}{\frac {\theta}{2} \cdot \log n} \cdot \frac {\sqrt {\bar {a} _ {e}}}{n} \cdot \sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} (| u _ {i} u _ {i, j} | + | u _ {i, j} u _ {j} | + 4 \sqrt {\bar {a} _ {e}}) \\ \leq \frac {2}{\theta \log n} \left(\frac {(4 + 2 \varrho_ {1}) (n _ {d} + \varphi_ {k}) \bar {a} _ {e}}{n} + \frac {\sqrt {2 \bar {a} _ {e}}}{n} \cdot \sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} | u _ {i} u _ {j} |\right) \\ \leq \frac {1}{n} \cdot (\kappa_ {3} \cdot n _ {d} + \frac {4}{\sqrt {\theta \cdot \log n}} \cdot \| \mathcal {F} _ {k} \|) \\ \leq \frac {1}{n} \cdot \left(\kappa_ {3} \cdot n _ {d} + \frac {\kappa_ {4}}{\sqrt {\log n}} \cdot \sqrt {\frac {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}{\rho}}\right) \\ \end{array}
$$

where $\kappa _ { 3 }$ and $\kappa _ { 4 }$ are some constants and the last inequality 3 4is true according to Lemma 5. Thus, an upper bound of $\bar { \xi } _ { t } .$ , denoted as $\bar { \eta } _ { t }$ , follows Poisson with

$$
\bar {\lambda} _ {e} = \frac {n _ {s}}{n} \left(\kappa_ {3} \cdot n _ {d} + \kappa_ {4} \sqrt {\frac {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}{\rho \cdot \log n}}\right).
$$

Hence, by union bounds, we have

$$
\operatorname * {P r} (\bar {\xi} > \sigma \bar {\lambda} _ {e}) \leq \frac {1}{\bar {a} _ {e}} \cdot \operatorname * {P r} (\bar {\xi} _ {t} > \sigma \bar {\lambda} _ {e}) \leq \frac {n}{2 \log n} \operatorname * {P r} (\bar {\eta} _ {t} > \sigma \bar {\lambda} _ {e})
$$

From Lemma 2, for $\sigma > 1$ , $\begin{array} { r } { \mathrm { P r } ( \bar { \eta } _ { t } > \sigma \bar { \lambda } _ { e } ) \leq ( \frac { e ^ { \sigma - 1 } } { \sigma ^ { \sigma } } ) ^ { \bar { \lambda } _ { e } } . } \end{array}$ $n _ { s } = \Theta ( n )$ t $\bar { \lambda } _ { e } = \Omega ( \log n )$ , we choose σ satisfying we get eσ−1 $\frac { e ^ { \sigma - 1 } } { \sigma ^ { \sigma } } < 1 ( e _ { \cdot } g .$ σσ $\sigma = e )$

$$
\operatorname * {P r} (\bar {\xi} > \sigma \bar {\lambda} _ {e}) = O (1 / \log n) \rightarrow 0, \text {   as   } n \rightarrow 0.
$$

Then the relay burden of every node on connectivity paths is of order $O ( \bar { \lambda } _ { e } )$ , which completes the proof. □

Combining Lemma 9 and Lemma 10, we can obtain:

Theorem 2: When $\rho = O ( n / \log n )$ , by the strategy $\bar { \mathfrak { I } } _ { e }$ without taking the bottlenecks on BSs into account, the persession multicast throughput for HEN is at least

$$
\bar {\Lambda} _ {e} ^ {\bar {r} _ {b}} = \left\{ \begin{array}{l l} \Omega ((\log n) ^ {\frac {1 - \alpha}{2}} \cdot \frac {\sqrt {\rho}}{n _ {d} \sqrt {n}}) & \text {when} n _ {d}: [ 1, \rho ] \\ \Omega ((\log n) ^ {\frac {1 - \alpha}{2}} \cdot \frac {1}{\sqrt {n n _ {d}}}) & \text {when} n _ {d}: [ \rho , n / \log n ] \\ \Omega ((\log n) ^ {- \frac {\alpha}{2}} \cdot \frac {1}{n _ {d}}) & \text {when} n _ {d}: [ n / \log n, n ] \end{array} \right.
$$

In the following context we will consider the possible bottleneck that may happen on BSs. Under the strategy $\bar { \mathfrak { I } } _ { e } ,$ all source nodes in some subregion $S _ { \iota }$ will send data to the base station $b _ { \iota }$ as long as some receiver node(s) fall outside of $S _ { \iota }$ . Thus, the base station may become the bottleneck of the network when the number of source nodes exceeds some value. With the increasing number of source nodes inside one subregion, if most of source nodes have some receivers outside the subregion, the base stations may have huge burden, thus become bottlenecks. Using the method similar in Lemma 10, we have,

Lemma 11: The maximum load on the links between BSs and ordinary nodes is of order

$$
\bar {L} _ {e} ^ {r _ {b}} = \left\{ \begin{array}{l l} O (n \cdot n _ {d} / \rho) & \text {when} n _ {d}: [ 1, \rho ] \\ O (n) & \text {when} n _ {d}: [ \rho , n ] \end{array} \right.
$$

Please see the detailed proof in [15].

According to Lemma 9, the capacity of the links between BSs and ordinary nodes is of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . Thus,

Lemma 12: By $\bar { \mathfrak { I } } _ { e } .$ Ω((log ) ) the throughput along the wireless links via BSs is of order

$$
\bar {\Lambda} _ {e} ^ {r _ {b}} = \left\{ \begin{array}{l l} \Omega (\frac {\rho}{n \cdot n _ {d}} \cdot (\log n) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ 1, \rho ] \\ \Omega (\frac {1}{n} \cdot (\log n) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ \rho , n ] \end{array} \right.
$$

Combining Theorem 2 and Lemma 12, we conclude that the bottlenecks of the whole routing $\bar { \mathfrak { I } } _ { e } ^ { r }$ are on the wireless links via BSs. According to Lemma 7, we obtain the throughput achieved by connectivity strategy.

Theorem 3: By the connectivity strategy $\bar { \mathfrak { I } } _ { e }$ , the persession multicast throughput for hybrid extended networks that can be achieved is of order:

When $m : \left\lceil 1 , n / \log n \right\rceil$ ,

$$
\bar {\Lambda} _ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega (\frac {m}{n \cdot n _ {d}} \cdot (\log n) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ 1, m ] \\ \Omega (\frac {1}{n} \cdot (\log n) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ m, n ] \end{array} \right.
$$

When m  n/  n, n ,

$$
\bar {\Lambda} _ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega (\frac {1}{n _ {d}} \cdot (\log n) ^ {- \frac {\alpha}{2} - 1}) & \text {when} n _ {d}: [ 1, n / \log n ] \\ \Omega (\frac {1}{n} \cdot (\log n) ^ {- \frac {\alpha}{2}}) & \text {when} n _ {d}: [ n / \log n, n ] \end{array} \right.
$$

5.1.2. Percolation Strategy. The percolation strategy denoted as $\mathfrak { F } _ { e }$ will be applied when $\textstyle \rho = O { \bigl ( } { \frac { n } { ( \log n ) ^ { 2 } } } { \bigr ) }$ n n 2 . Ob-= ( (log ) )viously, the side length of each subregion is of order n . We divide the region $\mathcal A ( n )$ into subsquares with Ω(log )area of a constant $a _ { e }$ ( )by inclined lines. We call those subsquares percolation cell. A percolation cells is open if it is nonempty (occupied) of ordinary nodes. Obviously, the open probability is $p ~ = ~ 1 - e ^ { - a _ { \epsilon } }$ . Using the same procedure as in [2], we can map this model into a bond percolation model $\mathbb { B } ( h , p )$ where $h = \sqrt { n } / \sqrt { 2 a _ { e } }$ and $p =$ $1 - e ^ { - a _ { e } }$ ( ) =. Moreover, we can partition $\mathcal A ( n )$ 2 =into slabs of 1size $\sqrt { 2 a _ { e } } ( \kappa \log h - \epsilon _ { h } ) \times ( \sqrt { n } / \sqrt { m } )$ ( ), where we can make $\frac { \mathbf { v } \cdot \mathbf { \sigma } } { \sqrt { m } \sqrt { 2 a _ { e } } \left( \kappa \log h - \epsilon _ { h } \right) }$ an integer by adjusting $\epsilon _ { h } = o ( 1 )$ . We 2 ( log )call those slabs highway slabs. Then by Lemma 6, we have

Lemma 13: For any $\kappa > 0$ and $a _ { e } >$ log $6 + 2 / \kappa ,$ , there exists a constant $\delta _ { 1 } ( \kappa , a _ { e } )$ 0 log 6 + 2such that there are w.h.p.at least $\delta _ { 1 }$ 1( ) n horizontal (vertical) highways in all highway slabs.

logBased on Lemma 13, we can divide horizontally (or vertically) each highway slab into slices of size $\kappa _ { 5 } \times ( \sqrt { n } / \sqrt { \rho } )$ , where $\begin{array} { r } { \kappa _ { 5 } = \frac { \delta _ { 1 } } { 2 \kappa } } \end{array}$ 5 ( )is a constant. Then, we can define a mapping 5 = 2function from the set of highways to the set of slices. In other words, we can ensure that the traffic initiated from each slice is routed through a corresponding highway and every highway only relay the traffic initiated from at most one slice.

Routing scheme $\Im _ { e } ^ { r } $ : Based on every EST $\begin{array} { r } { ( \tilde { U } _ { k } ^ { \iota } ) , 1 \leq \iota \leq } \end{array}$ ϕk, we realize each link $u _ { i } u _ { j } \in \mathrm { E S T } ( \tilde { U } _ { k } ^ { \iota } )$ by two broad ( )phases, i.e., highway phase and connectivity path phase. By Lemma 8, we can build at least $\frac { \theta } { 2 }$ n disjoint connectivity paths in each slab of size $\sqrt { \bar { a } _ { e } } \times \bar { ( \kappa \cdot \log h - \epsilon _ { h } ) }$ . Thus, similar to routing scheme $\bar { \mathbb { S } } _ { e } ^ { r } .$ ¯ ( log ) we can allocate evenly the traffic initiated by such slabs to at least $\frac { \theta } { 2 }$ n connectivity paths. 2 logWe present Algorithm 2 to describe our routing scheme.

Algorithm 2 Percolation Routing Scheme $\mathfrak { F } _ { e } ^ { r }$   
Input: $\mathrm{EST}(\tilde{U}_k^\iota)$ , $1 \leq \iota \leq \varphi_k$ .

Output: A multicast routing tree $\mathcal{T}(U_k)$ .

1: for each $\mathrm{EST}(\tilde{U}_k^\iota)$ do
2:    for each link $u_i u_j$ in $\mathrm{EST}(\tilde{U}_k^\iota)$ do
3: $u_i$ drains the packets into the specific horizontal highway along the specific connectivity path.
4:    Packets are carried along the horizontal highway, and are carried along the specific vertical highway.
5:    Packets are delivered to $u_j$ from the vertical highway along the specific connectivity path.
6:    end for
7:    Merge the same edges (hops) and break the circles that have no impact on the connectivity of $\mathrm{EST}(\tilde{U}_k^\iota)$ , we obtain the multicast tree $\mathcal{T}(U_k^\iota)$ .
8: end for
9: By using the similar method as Line 7 in Algorithm 1, we obtain the final multicast tree $\mathcal{T}(U_k)$ based on the forests consisting of the trees $\mathcal{T}(U_k^\iota)$ ( $1 \leq \iota \leq \varphi_k$ ).

Transmission scheduling $\Im _ { e } ^ { t }$ : We use two independent TDMA schemes to schedule transmissions along highways and connectivity paths. To be specific, we divide a scheduling period into two sub-periods with same size called $h i g h -$ way scheduling $\Im _ { e } ^ { t _ { 1 } }$ and connectivity path scheduling $\Im _ { e } ^ { t _ { 2 } }$ . The two scheduling phases correspond to the two phases of routing, i.e., highways phase $\Im _ { e } ^ { r _ { 1 } }$ and connectivity path phase $\Im _ { e } ^ { r _ { 2 } }$ . The scheme $\Im _ { e } ^ { t _ { 1 } }$ can be adopted as same as the scheduling of highways in [2]. Then we have

Lemma 14: By the transmission scheduling $\Im _ { e } ^ { t _ { 1 } }$ , the rate along highways achieved by our method is of order .

Ω(1)Since we can only ensure that there exists at least one connectivity path, instead of highway, passing through every BS $b _ { \iota } ,$ , for $1 \leq \iota \leq \varphi _ { k }$ and $1 \leq k \leq n _ { s }$ , then similar to connectivity strategy, we have

Lemma $I 5 \colon$ By using $\Im _ { e } ,$ the throughput along the wireless links via BSs is of order $\Lambda _ { e } ^ { r _ { b } } = \bar { \Lambda } _ { e } ^ { r _ { b } }$ (in Lemma 12).

The scheme $\Im _ { e } ^ { t _ { 2 } }$ Λ = Λ¯ can be adopted same as $\bar { \mathcal { S } } _ { e } ^ { t }$ . Then according to Lemma 9, we can obtain,

Lemma 16: By $\Im _ { e } ^ { t _ { 2 } }$ , the rate along each connectivity paths achievable by our method is of order $\Omega \big ( \frac { 1 } { ( \log n ) ^ { \alpha / 2 } } \big )$ .

Throughput derived by $\Im _ { e } \colon$ Ω( (log ) )First, we analyze the load of routing paths in highway and connectivity path phases.

Lemma $I 7 \colon$ During highway phase $\Im _ { e } ^ { r _ { 1 } }$ , the maximum relay burden of each node on the highways is w.h $\mathbf { \nabla } \cdot p .$ of order

$$
L _ {e} ^ {r _ {1}} = \left\{ \begin{array}{l l} O (\frac {\sqrt {n n _ {d}}}{\sqrt {\rho}}) & \text { when } n _ {d}: [ 1, \rho ] \\ O (\sqrt {n n _ {d}}) & \text { when } n _ {d}: [ \rho , n / (\log n) ^ {2} ] \\ O (n _ {d} \log n) & \text { when } n _ {d}: [ n / (\log n) ^ {2}, n / \log n ] \\ O (n) & \text { when } n _ {d}: [ n / \log n, n ] \end{array} \right.
$$

Proof: Given a node $v _ { t } ^ { * }$ on the highways, define the number of multicast sessions routed through $v _ { t } ^ { * }$ in highway phase $\Im _ { e } ^ { r _ { 1 } }$ as a random variable $\xi _ { t } ^ { r _ { 1 } }$ , and we consider the uniform upper bound $\xi ^ { r _ { 1 } }$ of $\xi _ { t } ^ { r _ { 1 } }$ . Define an Event $E _ { e } ^ { r _ { 1 } } ( k , t ) ;$ : The multicast session $\mathcal { M } _ { k }$ passes through $v _ { t } ^ { * }$ (in phase $\Im _ { e } ^ { r _ { 1 } }$ . Obviously, if $E _ { e } ^ { r _ { 1 } } ( k , t )$ happens then there exists an edge $u _ { i } u _ { j } \in \mathcal { F } _ { k }$ ( )that is routed through $v _ { t } ^ { * }$ in phase $\Im _ { e } ^ { r _ { 1 } }$ . In other words, a vertical (or horizontal) line through $v _ { t } ^ { * }$ intersects the segment $u _ { i } u _ { i , j }$ (or $u _ { i , j } u _ { j } )$ . Similar to Lemma 10, according to Lemma 5, we have

$$
\operatorname * {P r} (E _ {e} ^ {r _ {1}} (k, t)) \leq \frac {1}{n} \cdot \left(\kappa_ {5} \cdot n _ {d} \log n + \kappa_ {6} \sqrt {\frac {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}{\rho}}\right)
$$

where $\kappa _ { 5 }$ and $\kappa _ { 6 }$ are some constants. Thus, an upper bound of $\bar { \xi } _ { t } ,$ 5 6, denoted as $\eta _ { t }$ , follows Poisson with intensity

$$
\lambda_ {e} ^ {r _ {1}} = \frac {n _ {s}}{n} \left(\kappa_ {6} \cdot n _ {d} \cdot \log n + \frac {\kappa_ {8}}{\rho} \cdot \sqrt {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}\right)
$$

Hence, by the similar procedure of Lemma 10, we obtain that the relay burden of every node on the highways in phase $\Im _ { e } ^ { r _ { 1 } }$ is of order ${ \cal O } ( \lambda _ { e } ^ { r _ { 1 } } )$ , which completes the proof. □

Lemma $I 8 \colon$ ( )During connectivity path phase $\Im _ { e } ^ { r _ { 2 } }$ , the maximum relay burden of each node on the connectivity path is w.h.p. of order $L _ { e } ^ { r _ { 2 } } = O ( n _ { d } \cdot ( \log n ) ^ { 1 / 2 } )$ .

= ( (log ) )Please see the detailed proof in [15].

Combining Lemma 14 and 17, we obtain Lemma 19.

Lemma 19: During phase $\Im _ { e } ^ { r _ { 1 } }$ , the multicast throughput that will be achieved by our method is of order

$$
\Lambda_ {e} ^ {r _ {1}} = \left\{ \begin{array}{l l} \Omega (\frac {\sqrt {\rho}}{n _ {d} \sqrt {n}}) & \text { when } n _ {d}: [ 1, \rho ] \\ \Omega (\frac {1}{\sqrt {n n _ {d}}}) & \text { when } n _ {d}: [ \rho , n / (\log n) ^ {2} ] \\ \Omega (\frac {1}{n _ {d} \log n}) & \text { when } n _ {d}: [ n / (\log n) ^ {2}, n / \log n ] \\ \Omega (1 / n) & \text { when } n _ {d}: [ n / \log n, n ] \end{array} \right.
$$

Furthermore, combining Lemma 16 and Lemma 18, we can obtain the following lemma.

Lemma 20: During phase $\Im _ { e } ^ { r _ { 2 } }$ , the multicast throughput that can be achieved by our method is of order $\Lambda _ { e } ^ { r _ { 2 } } = \Omega ( \frac { 1 } { n _ { d } }$ 1nd · $( \log n ) ^ { - { \frac { \alpha + 1 } { 2 } } } )$ .

og ) )Based on Lemma 19 and Lemma 20, and according to Lemma 7, we obtain Theorem 4.

Theorem 4: When $\rho = O ( n / ( \log n ) ^ { 2 } )$ , by the percolation strategy $\Im _ { e }$ = ( (log ) )without taking bottlenecks on BSs into account, the per-session multicast throughput $\Lambda _ { e } ^ { \bar { r } _ { b } }$ for hybrid extended networks is of order:

When $\rho : [ 1 , ( n / ( \log n ) ^ { \alpha + 1 } ) ]$ ,

$$
\Lambda_ {e} ^ {\bar {r} _ {b}} = \left\{ \begin{array}{l l} \Omega (\frac {\sqrt {\rho}}{n _ {d} \sqrt {n}}) & \text {when n_{d} :[1, \rho]} \\ \Omega (\frac {1}{\sqrt {n n _ {d}}}) & \text {when n_{d} :[\rho, \frac {n}{(\log n)^{\alpha + 1}}]} \\ \Omega (\frac {1}{n _ {d} \cdot (\log n) ^ {\frac {\alpha + 1}{2}}}) & \text {when n_{d} :[\frac {n}{(\log n)^{\alpha + 1}},n]} \end{array} \right.
$$

When $\rho : [ \frac { n } { ( \log n ) ^ { \alpha + 1 } } , \frac { n } { ( \log n ) ^ { 2 } } ] , \Lambda _ { e } ^ { \bar { r } _ { b } } = \Omega ( \frac { 1 } { n _ { d } } ( \log n ) ^ { - \frac { \alpha + 1 } { 2 } } )$

Combining Theorem 4 and Lemma 15, we have

Theorem 5: By the percolation strategy $\mathfrak { F } _ { e } ,$ the persession multicast throughput $\Lambda _ { e } ^ { r }$ for HEN is of order:

When $m : [ 1 , n / \log n ]$ ,

$$
\Lambda_ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega (\frac {m}{n \cdot n _ {d}} (\log n) ^ {- \frac {\alpha}{2}}) & \text {when} n _ {d}: [ 1, m ] \\ \Omega (\frac {1}{n} (\log n) ^ {- \frac {\alpha}{2}}) & \text {when} n _ {d}: [ m, \frac {n}{\sqrt {\log n}} ] \\ \Omega (\frac {1}{n _ {d}} (\log n) ^ {- \frac {\alpha + 1}{2}}) & \text {when} n _ {d}: [ \frac {n}{\sqrt {\log n}}, n ] \end{array} \right.
$$

When m  n/  n, n ,

$$
\Lambda_ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega (\frac {1}{n _ {d}} (\log n) ^ {- \frac {\alpha}{2} - 1}) & \text {when} n _ {d}: [ 1, n / \log n ] \\ \Omega (\frac {1}{n} (\log n) ^ {- \frac {\alpha}{2}}) & \text {when} n _ {d}: [ n / \log n, \frac {n}{\sqrt {\log n}} ] \\ \Omega (\frac {1}{n _ {d}} (\log n) ^ {- \frac {\alpha + 1}{2}}) & \text {when} n _ {d}: [ \frac {n}{\sqrt {\log n}}, n ] \end{array} \right.
$$

Then, combining Theorem 3 and Theorem 5, we have

Theorem 6: By hybrid routing strategy, the multicast throughput for HEN is achieved of order $\Lambda _ { e } ^ { r }$ (defined in Theorem 5).

# 5.2. Ordinary Ad hoc Strategy for HEN

Different from the previous strategies, in ordinary routing ad hoc strategy, we use only the ordinary nodes. In particular, we treat the network as an ordinary ad hoc network and we construct global multicast trees composed of only ordinary nodes, [14], and we can obtain

Theorem $7 ( \ l I 4 ) .$ By the ordinary ad hoc routing strategies, the multicast throughput for HEN is of order

$$
\left\{ \begin{array}{l l} \Omega (\frac {1}{\sqrt {n _ {d} n}}) & \text {when} n _ {d}: [ 1, \frac {n}{(\log n) ^ {\alpha + 1}} ] \\ \Omega (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}}) & \text {when} n _ {d}: [ \frac {n}{(\log n) ^ {\alpha + 1}}, \frac {n}{(\log n) ^ {2}} ] \\ \Omega (\frac {1}{\sqrt {n n _ {d}} \cdot (\log n) ^ {\frac {\alpha - 1}{2}}}) & \text {when} n _ {d}: [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} ] \\ \Omega (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha}{2}}}) & \text {when} n _ {d}: [ \frac {n}{\log n}, n ] \end{array} \right.
$$

# 5.3. BS-based Strategy for HEN

In this routing strategy, we adopt a classical cellular routing strategy, in which sources deliver data to BSs directly during the uplink phase and BSs deliver received data to destinations directly during the downlink phase. Since in any time slot, all wireless links associate with the BSs, then the parallel transmission scheduling is disabled. We denote the BS-based strategy as $\tilde { \mathbb { S } } _ { e }$ and denote the corresponding ˜routing scheme and transmission scheduling as $\tilde { \mathbb { S } } _ { e } ^ { r }$ and $\tilde { \mathcal { \mathrm { S } } } _ { e } ^ { t } ,$ , respectively. Different from the previous partition method, here we simply partition $A ( n )$ into m subregions with side length $\frac { \sqrt { n } } { \sqrt { m } }$ ( )and each base station is placed at the center of each subregion.

Routing scheme $\mathfrak { I } _ { e } ^ { r } \mathrm { : }$ : The routing consists of three phases: uplink phase $\Im _ { e } ^ { r _ { 1 } }$ ˜, BS-to-BS phase $\Im _ { e } ^ { r _ { 2 } }$ and downlink phase $\tilde { \Im } _ { e } ^ { r _ { 3 } }$ . That is,

1) During the uplink phase, source nodes in subregion $S _ { \iota }$ , $\iota = 1 , 2 , \cdots , m$ , transmit the packets to BS $b _ { \iota }$ .   
= 1 22) The BS that receives the packet from source $v _ { k } .$ $k = 1 , 2 , \cdots , n _ { s }$ , delivers it to the BSs placed in the = 1 2subregions containing the nodes in the set of destination of $v _ { k }$ using BS-to-Bs links.   
3) During downlink phase, each BS $b _ { \iota } , \iota = 1 , 2 , \cdot \cdot \cdot , m .$ = 1 2broadcasts the packets to the nodes in subregion $S _ { \iota }$ .

Transmission scheduling $\Im _ { e } ^ { t } \colon$ It includes three independent phases, $i . e . , \ \tilde { \Im } _ { e } ^ { t _ { 1 } } , \ \tilde { \Im } _ { e } ^ { t _ { 2 } }$ and $\Im _ { e } ^ { t _ { 3 } }$ , corresponding to three routing phases. Since we assume that the BS-to-BS phase is surely not the bottleneck, we only focus on the other two phases. That is,

1) During uplink phase $\Im _ { e } ^ { t _ { 1 } }$ , all BSs $b _ { \iota } , \iota = 1 , 2 , \cdot \cdot \cdot , m$ = 1 2receive simultaneously packets from the nodes in $S _ { \iota }$ .   
2) During downlink phase $\Im _ { e } t _ { 3 }$ , all BSs $\begin{array} { r l } { b _ { \iota } , \ \iota } & { { } = } \end{array}$ $1 , 2 , \cdots , m ,$ =, deliver simultaneously packets to the 1 2nodes in $S _ { \iota }$ .

Lemma 21: By the scheduling $\tilde { \mathcal { S } } _ { e } ^ { t }$ , each subregion can sustain traffic with a rate of order $\Omega ( ( n / m ) ^ { - \frac { \alpha } { 2 } } )$ during both downlink and uplink.

Please see the detailed proof in [15].

Next, we consider the load of BS during the downlink phase or uplink phase. Similar to Lemma 11, we have,

Lemma 22: By the strategy $\mathfrak { F } _ { e } ^ { r } .$ the load of each base station is of order $\tilde { L } _ { e } ^ { r } = \bar { L } _ { e } ^ { r _ { b } }$ .

=According to Lemma 21 and Lemma 22, we have

Theorem 8: By the BS-based strategy, the achievable persession multicast throughput for HEN can be is of order

$$
\left\{ \begin{array}{l l} \Omega (\frac {1}{\log m} \cdot (\frac {n}{m}) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ 1, m \log m / n ] \\ \Omega (\frac {m}{n \cdot n _ {d}} \cdot (\frac {n}{m}) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ m \log m / n, m ] \\ \Omega (\frac {1}{n} \cdot (\frac {n}{m}) ^ {- \frac {\alpha}{2}}) & \text { when } n _ {d}: [ m, n ] \end{array} \right.
$$

# 5.4. Integration of Three Routing Strategies

To achieve the optimal throughput, we will select the best routing strategy according to the different scenarios in terms of m and $n _ { d } .$ . Combining Theorem 6, Theorem 7 and Theorem 8, we can obtain the main result in Theorem 1.

# 6. Literature Reviews

In this section, we review the existing work on capacity for hybrid networks under two popular channel models.

Under threshold-based channel model: Earlier, Liu et al. [9] introduced the model based on the dense network in which the base stations are regularly placed and the ad hoc nodes are randomly distributed. The case that both base stations and ad hoc nodes are randomly placed in the dense network is studied by Kozat and Tassiulas in [5]. Agarwal et al. [1] considered the unicast capacity for hybrid networks under PhIM. Recently, Mao et al. [11] studied the multicast capacity for hybrid networks under threshold-based channel model by assuming $m = O ( n / \log n )$ .

= ( log )Under Gaussian Channel model: Liu et al. [10] studied the unicast capacity of the wireless ad hoc network with infrastructure. They showed that in a two-dimensional square hybrid wireless network with n ordinary nodes and m base stations, it is necessary that $m \ = \ \Omega ( { \sqrt { n } } )$ in order = Ω( )to obtain a linear gain of capacity. Recently, Wang et al. [13] derived some achievable throughput for both hybrid extended networks and hybrid dense networks without using the percolation theory.

# 7. Conclusion

We study the multicast capacity for wireless hybrid extended networks under Gaussian Channel model. Three different multicast strategies are proposed and studied. Based on the achievable multicast throughput for each scheme, we give an optimal decision on selecting one of the three routing strategies according to different scenarios in terms of m, n and $n _ { d } .$ . To the best of our knowledge, this is the first work that addresses the multicast routing and scheduling strategy in hybrid wireless networks under Gaussian channel model. A number of interesting questions remain open: How to derive a tight upper bound on the network capacity? What routing strategy should be implemented if the access link between ordinary wireless nodes and a base station is different from wireless links between ordinary nodes, e.g. it may have larger bandwidth. What is the effect on capacity if the links between base stations do not have a sufficiently large bandwidth?

# Acknowledgments

This work is partially supported by the National Natural Science Funds under Grant No. 60534060, No. 90718012, No. 90818023, the National High Technology Research and Development Program of China (863 Program) under Grants No. 2007AA01Z136, No. 2007AA01Z149, No. 2007AA01Z180, Shanghai International Cooperation Project under Grant No. 075107005. The research of Xiang-Yang Li and Yunhao Liu is also partially supported by NSF CNS-0832120, NSF CCF-0515088, National Natural Science Foundation of China under Grant No. 60828003, National Basic Research Program of China (973 Program) under grant No. 2006CB30300, Hong Kong RGC HKUST 6169/07, the RGC under Grant HKBU 2104/06E, and CERG under Grant PolyU-5232/07E.

# References

[1] A. Agarwal and P. R. Kumar. Capacity bounds for ad hoc and hybrid wireless networks. ACM SIGCOMM Computer Communication Review, 34(3):71–83, 2004.   
[2] M. Franceschetti, O. Dousse, D. Tse, and P. Thiran. Closing the gap in the capacity of wireless networks via percolation theory. IEEE Trans. on Information Theory, 53(3):1009– 1018, 2007.   
[3] P. Gupta and P. R. Kumar. The capacity of wireless networks. IEEE Trans. on Information Theory, 46(2):388–404, 2000.   
[4] V. Kolchin, B. Sevast’yanov, and Chistyakov. Random Allocations. Winston and Sons, Washington, DC, 1978.   
[5] U. C. Kozat and L. Tassiulas. Throughput capacity of random ad hoc networks with infrastructure support. In Proc. ACM Mobihoc 2003.   
[6] S. Li, Y. Liu, and X.-Y. Li. Capacity of large scale wireless networks under gaussian channel model. In Proc. ACM Mobicom 2008.   
[7] X. Li, S. Tang, and F. Ophir. Multicast capacity for large scale wireless ad hoc networks. In Proc. ACM Mobicom 2007.   
[8] X.-Y. Li. Multicast capacity of wireless ad hoc networks. IEEE/ACM Tracsaction on Networking, January, 2008.   
[9] B. Liu, Z. Liu, and D. Towsley. On the capacity of hybrid wireless networks. In Proc. IEEE INFOCOM 2003.   
[10] B. Liu, P. Thiran, and D. Towsley. Capacity of a wireless ad hoc network with infrastructure. In Proc. ACM Mobihoc 2007.   
[11] X. Mao, X.-Y. Li, and S. Tang. Multicast capacity for hybrid wireless networks. In Proc. ACM MobiHoc 2008.   
[12] V. Vapnik and A. Chervonenkis. On the uniform convergence of relative frequencies of events to their probabilities. Theory of Probability and its Applications, 16(2):264–280, 1971.   
[13] C. Wang, C. Jiang, X.-Y. Li, and G. Dai. Achievable throughput for hybrid wireless networks under gaussian channel model. In Proc. IEEE ICC 2009.   
[14] C. Wang, X.-Y. Li, C. Jiang, S. Tang, Y. Liu, and J. Zhao. Scaling laws on multicast capacity of large scale wireless networks. In Proc. IEEE INFOCOM 2009.   
[15] C. Wang, S. Tang, X.-Y. Li, C. Jiang, and Y. Liu. Multicast throughput of hybrid wireless networks under gaussian channel model. Technical report, CS of IIT available at http://www.iit.edu/∼stang7/hybrid.pdf, 2009.   
[16] R. Zheng. Asymptotic bounds of information dissemination in power-constrained wireless networks. IEEE Trans. on Wireless Communications, 7(1):251–259, Jan. 2008.