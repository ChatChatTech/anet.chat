# Multicast Throughput for Hybrid Wireless Networks under Gaussian Channel Model

Cheng Wang, Student Member, IEEE, Xiang-Yang Li, Senior Member, IEEE, Changjun Jiang, Member, IEEE, Shaojie Tang, Student Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—We study the multicast capacity for hybrid wireless networks consisting of ordinary ad hoc nodes and base stations under Gaussian Channel model, which generalizes both the unicast and broadcast capacities for hybrid wireless networks. Assume that all ordinary ad hoc nodes transmit at a constant power $P ,$ and the power decays along the path, with attenuation exponent $\alpha > 2 .$ The data rate of a transmission is determined by the Signal to Interference plus Noise Ratio (SINR) at the receiver as B logð1 þ SINRÞ. The ordinary ad hoc nodes are placed in the square region $\scriptstyle A ( a )$ of area a according to a Poisson point process of intensity $n / a .$ . Then, m additional base stations (BSs) acting as the relaying communication gateways are placed regularly in the region AðaÞ, and are connected by a high-bandwidth wired network. Let a ¼ n and a ¼ 1, we construct the hybrid extended network (HEN) and hybrid dense network (HDN), respectively. We choose randomly and independently $n _ { s }$ ordinary ad hoc nodes to be the sources of multicast sessions. We assume that each multicast session has $n _ { d }$ randomly chosen terminals. Three broad categories of multicast strategies are proposed. The first one is the hybrid strategy, i.e., the multihop scheme with BS-supported, which further consists of two types of strategies called connectivity strategy and percolation strategy, respectively. The second one is the ordinary ad hoc strategy, i.e., the multihop scheme without any BS-supported. The third one is the classical BS-based strategy under which any communication between two ordinary ad hoc nodes is relayed by some specific BSs. According to the different scenarios in terms of $m , n ,$ and $n _ { d } ,$ we select the optimal scheme from the three categories of strategies, and derive the achievable multicast throughput based on the optimal decision.

Index Terms—Wireless hybrid networks, wireless ad hoc networks, multicast throughput, random networks, multicast capacity, Gaussian channel model.

# 1 INTRODUCTION

HE asymptotic capacity for wireless ad hoc networks has Tbeen intensively studied under different channel models [2]. Most existing related works are based on two types of channel models. The first is called the thresholdbased channel model [3] that determines the transmission rate as a binary function. The protocol interference model (PrIM) and physical interference model (PhIM) [2] both belong to the threshold-based channel model. The second one is the Gaussian Channel model [4] that determines the transmission rate based on a continuous function of the

C. Wang and C. Jiang are with the Department of Computer Science and Engineering, Tongji University, Building of Electronics and Information Engineering, NO. 4800, Caoan Road, Shanghai, China, 201804, and the Key Laboratory of Embedded System and Service Computing, Ministry of Education, Shanghai, China.   
E-mail: 3chengwang@gmail.com, cjjiang@tongji.edu.cn.   
. X.-Y. Li is with the Tsinghua National Laboratory for Information Science and Technology (TNLIST), Department of Computer Science and Engineering, Tongji University, and the Department of Computer Science, Illinois Institute of Technology, 10 West 31st Street, Chicago, IL 60616. E-mail: xiangyang.li@gmail.com.   
. S. Tang is with the Department of Computer Science, Illinois Institute of Technology, 10 West 31st Street, Chicago, IL 60616. E-mail: stang7@iit.edu.   
. Y. Liu is with the TNLIST and School of Software, Tsinghua University, and the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong. E-mail: yunhao@greenorbs.com.

Manuscript received 27 Jan. 2010; revised 1 July 2010; accepted 12 Aug. 2010; published online 19 Oct. 2010.

For information on obtaining reprints of this article, please send e-mail to: tmc@computer.org, and reference IEEECS Log Number TMC-2010-01-0043. Digital Object Identifier no. 10.1109/TMC.2010.206.

receiver’s Signal to Interference plus Noise Ratio (SINR). The Gaussian Channel model is also called generalized physical model [5], it captures better the physical layer of wireless networks than threshold-based channel model that is a very crude approximation for wireless networks, under which any communication pair $v _ { i }$ and $v _ { j }$ can establish a direct communication link, over a channel of bandwidth $B ,$ of rate $R ( v _ { i } , v _ { j } ) = B \log ( 1 + \mathrm { S I N R } ( v _ { j } ) )$ , i.e., the link achieves Shannon’s capacity for a wireless channel with additive Gaussian white noise, see [6], [7].

A hybrid wireless network (HN) consists of two types of network terminals: base stations and ordinary ad hoc nodes. Assume that all base stations can communicate with wireless ad hoc nodes, and further assume that each base station is neither a source nor a receiver, it simply serves as a relaying gateway. Intuitively, wireless ad hoc networks and cellular networks can both be regarded as the special cases of the HN, as the number of base stations is adjusted. Thus, the study of the capacity for HN has more generality than that of wireless ad hoc networks and cellular networks, while it was not fully studied. In addition, as we know, multicast capacity can unify the unicast and broadcast capacities [8], which increases the generality of the research on the multicast capacity for HN. For HNs, there are also generally two channel models as in most existing works for wireless ad hoc networks. To the best of our knowledge, all existing results of multicast capacity for hybrid networks are derived under the threshold-based model [9], a natural and interesting issue arises: What is the multicast capacity for hybrid networks when the Gaussian channel model is used. This paper aims to derive an achievable multicast throughput for HNs under Gaussian channel model.

![](images/b8f23c32af4c3de9ba3fdccb919cbcdd64a4e48da4d081db0d6456a22a1f9ed9.jpg)



（a)

![](images/bca7502c60d37a4dd71bfbaf8dc16a046321b505fede606163309bb2417e5f4e.jpg)



（b)

![](images/6853a3d621b69de55ed365c74ada1c825efe1396a7c8ed138a6c2a4500346386.jpg)



（c）

![](images/9dae3fd01d1f079d985216b8420bb668a47f2ef9b2a1fe4afdfc4e7d048abfea.jpg)



(d）  
Fig. 1. Illustrations of three types of multicast routing schemes. The small hexagons represent the base stations that are assumed to be connected via the high-bandwidth wired links. The cases that $a = n$ and $a = 1$ correspond to the hybrid extended network and hybrid dense network, respectively. (a) Original network. (b) Ordinary ad hoc strategy. (c) BS-based strategy. (d) Hybrid routing strategy.

We assume that the ordinary ad hoc nodes are placed in the square region $\mathcal A ( a )$ of area a according to a Poisson point process of intensity $n / a$ . In addition, m additional base stations (BSs) serving as the relaying communication gateways are placed regularly in the region $\mathcal A ( a )$ and they are connected by the high-bandwidth wired links. Let $a = n$ and $a = 1$ , we construct two scaling network models: the hybrid extended network (HEN) and hybrid dense network (HDN), respectively. There are $n _ { s }$ randomly and independently chosen multicast sessions. Each multicast session has $n _ { d }$ randomly chosen terminals. According to different relations among $m , n ,$ and ${ \boldsymbol { n } } _ { d } ,$ we adopt different types of multicast strategies. To be specific, we propose three broad categories of multicast strategies for both HEN and HDN. The first one is called the hybrid strategy, i.e., the multihop scheme with BS-supported, which further consists of two types of schemes called connectivity strategy and percolation strategy, respectively. The second one is the ordinary ad hoc strategy, i.e., the multihop scheme without any BS-supported. The third one is the classical BS-based strategy, under which any communication between two ordinary ad hoc nodes is relayed by some specific BSs. For different cases in terms of $m , n ,$ and ${ \boldsymbol { n } } _ { d } ,$ we select the optimal strategy from the three categories of strategies, and derive the achievable multicast throughput based on the optimal scheme. To the best of our knowledge, this is the first work that addresses the multicast routing and scheduling strategy in hybrid wireless networks under Gaussian channel model.

The rest of the paper is structured as follows: In Section 2, we introduce the network model. Main results are presented and discussed in Section 3. We make technical preparations in Section 4. In Section 5, we design the multicast schemes for hybrid extended networks. In Section $^ { 6 , }$ we extend our results to hybrid dense networks. In Section $^ { 7 , }$ we review the related existing literature. In Section 8, we conclude the paper.

# 2 NETWORK MODEL

Throughout this paper, we denote the probability of an event E as $\operatorname* { P r } ( E )$ , and we are mainly concerned with events that take place with high probability $( w . h . p . )$ , i.e., with probability 1 as the number of nodes $n \longrightarrow \infty .$ .

# 2.1 Network Topology

For the ordinary ad hoc nodes, we consider two classical random networks, i.e., the random extended network (REN) and random dense network (RDN). We construct REN (or RDN) by placing ordinary ad hoc nodes according to a Poisson point process of intensity 1 (or n) on the square $\mathcal { A } ( n ) = [ 0 , \sqrt { n } ] \times [ 0 , \sqrt { n } ] \mathrm { ( o r } \mathcal { A } ( 1 ) = [ 0 , 1 ] \times [ 0 , 1 ] )$ ). By Chebyshev’s Inequality, we can easily obtain that the number of ordinary ad hoc nodes in $\mathcal { A } ( n )$ (or Að1Þ) is within $( ( 1 - \epsilon ) n , ( 1 + \epsilon ) n )$ , where $\epsilon > 0$ is an arbitrarily small constant. We assume that there are exactly n ordinary ad hoc nodes in AðnÞ (or Að1Þ), which has no impact on our results in order sense [10], [22]. Furthermore, we place regularly m base stations (BSs, with wireless transmitting power P ) in AðnÞ (or Að1Þ), which are connected by the highbandwidth wired links, to construct the hybrid extended network (or hybrid dense network). Please see the illustration in Fig. 1b. To be specific, divide $\mathcal { A } ( n )$ (or Að1Þ) into m subregions with side length ${ \frac { \sqrt { n } } { \sqrt { m } } } \ ( \mathrm { o r } \ { \frac { 1 } { \sqrt { m } } } )$ and place one BS on the center position of each subregion. We further assume that the number of BSs $m = O ( n )$ .

# 2.2 Achievable Multicast Throughput

Now, we give the formal definition of capacity in our model. We assume that $\mathcal { V } = \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { n } \}$ is the set of nodes in the network, $\mathcal { S } \subseteq \mathcal { V }$ is the set of sources of multicast, and assume that the number of multicast sessions $| \mathcal { S } | = n _ { s }$ . For each source node $v _ { S , i } \in S ,$ we uniformly select $n _ { d }$ nodes at random from the other nodes to constitute a set ${ \mathcal { D } } s , i = \{ v _ { \mathcal { S } , i _ { 1 } } , v _ { \mathcal { S } , i _ { 2 } } , . . . , v _ { \mathcal { S } , i _ { n _ { d } } } \}$ as the set of destinations, where obviously $n _ { d } \le n - 1$ . Furthermore, define $\mathcal { U } _ { S , i } : = \{ v _ { S , i } \} \cup$ $\mathcal { D } _ { { \cal S } , i }$ i as the spanning set of the ith multicast sessions.

Denote $\dot { \Lambda } _ { \mathcal { S } , n _ { d } } = \mathsf { \bar { ( } } \lambda _ { S , 1 } , \lambda _ { S , 2 } , \ldots , \lambda _ { S , n _ { s } } )$ as the rate vector of the multicast data rate of all multicast session.

Definition 1 (Feasible Rate Vector). A multicast rate vector $\Lambda _ { \mathcal { S } , n _ { d } } = ( \lambda _ { \mathcal { S } , 1 } , \lambda _ { \mathcal { S } , 2 } , \ldots , \lambda _ { \mathcal { S } , n _ { s } } )$ is feasible if there is a spatial and temporal scheme for scheduling transmissions such that by operating the network in a multihop fashion and buffering at intermediate nodes when awaiting transmission, the ith source node, denoted as $v _ { S , i }$ , can deliver data to all its $n _ { d }$ destinations at rate of $\lambda _ { S , i }$ bits/second, where $i = 1 , 2 , \dots , n _ { s }$ . That is, there is a $\mathit { T } <$ 1 such that in every time interval (with unit seconds) $[ ( j - 1 ) \cdot T , j \cdot T ]$ , every node $v _ { S , i } \in S$ can send $T \cdot \lambda _ { \mathcal { S } , i }$ bits to all its $n _ { d }$ destinations.

Considering a multicast rate vector, we define the total multicast throughput of such feasible rate vector as $\Lambda _ { S , n _ { d } } ^ { \mathrm { T } } ( n ) = \Sigma _ { i = 1 } ^ { n _ { s } } \lambda _ { S , i } ,$ define the average multicast throughput as $\begin{array} { r } { \bar { \Lambda } _ { { \mathcal S } , n _ { d } } ^ { \mathrm { A } } ( n ) = \frac { \Sigma _ { i = 1 } ^ { n _ { s } } \lambda _ { S , i } } { n _ { s } } } \end{array}$ ns , and define the minimum per-session multicast throughput (also called per-session multicast throughput for concise) as $\begin{array} { r } { \Lambda _ { S , n _ { d } } ^ { \mathrm { P } } ( n ) = \operatorname* { m i n } _ { v _ { S , i } \in \mathcal { S } } \lambda _ { S , i } } \end{array}$ .

Definition 2 (Throughput Capacity). An aggregated multicast throughput $\Lambda _ { S , n _ { d } } ^ { \mathrm { T } } ( n ) = \Sigma _ { i = 1 } ^ { n _ { s } } \lambda _ { S , i }$ is achievable for $n _ { s }$ multicast sessions (each session with $n _ { d }$ destinations) if the rate vector $\Lambda _ { \mathcal { S } , n _ { d } } = ( \lambda _ { \mathcal { S } , 1 } , \lambda _ { \mathcal { S } , 2 } , \ldots , \lambda _ { \mathcal { S } , n _ { s } } )$ is feasible.

Similarly, we can define the achievable average multicast throughput and achievable per-session multicast throughput.

# Definition 3 (Multicast Capacity of Random Networks).

The per-session multicast capacity of a class of random networks is of order $\Theta ( g ( n ) )$ Þ bits/sec if there are deterministic constants $c > 0$ and $c < c ^ { \prime } < + \infty$ such that

$$
\lim _ {n \rightarrow + \infty} \operatorname * {P r} \left(\Lambda_ {\mathcal {S}, n _ {d}} ^ {\mathrm{M}} (n) = c g (n) \text {   is   achievable }\right) = 1,
$$

$$
\liminf _ {n \to + \infty} \operatorname * {P r} \left(\Lambda_ {\mathcal {S}, n _ {d}} ^ {\mathrm{M}} (n) = c ^ {\prime} g (n) \text {   is   achievable }\right) <   1.
$$

We can similarly define the aggregated multicast capacity and average multicast capacity for random networks. In this paper, we will only consider the per-session multicast capacity by which the other two types of capacities can be derived straightforwardly. The achievable multicast throughput is a lower bound of the multicast capacity. Without loss of compatibility to most existing works, we assume that $n _ { s } = \Theta ( n )$ .

# 2.3 Gaussian Channel Model

Assume that all nodes transmit with a constant power $P ,$ and any two nodes can establish a direct communication link over a channel of bandwidth B, of rate

$$
R (v _ {i}, v _ {j}) = B \log \left(1 + \frac {P \cdot \ell (v _ {i} , v _ {j})}{N _ {0} + \sum_ {v _ {k} \in A (i) / v _ {i}} P \cdot \ell (v _ {k} , v _ {j})}\right),
$$

where $N _ { 0 }$ is the ambient noise power, $A ( i )$ is the set of nodes that transmit when $v _ { i }$ is scheduled. Let $d _ { i j }$ denote the euclidean distance between vi and $v _ { j } .$ . Let the power attenuation function be $\ell ( v _ { i } , v _ { j } )$ . For HEN, let $\ell ( v _ { i } , v _ { j } ) : =$ min $\{ 1 , d _ { i j } ^ { - \alpha } \}$ with $\alpha > 2$ and $N _ { 0 } > 0 ;$ for HDN, let $\ell ( v _ { i } , v _ { j } ) : =$ $d _ { i j } ^ { - \alpha }$ with $\alpha > 2$ and $N _ { 0 } \geq 0 , [ 1 0 ]$ .

Notations. Throughout this paper, for a two-dimensional line segment $L = u v , \left| L \right|$ represents the euclidean distance between u and v; for a discrete set U, jUj represents its cardinality. For a continuous region A, we use kAk to denote its area; for a tree T (or a forest F) , we use $\| T \|$ (or $\| { \mathcal { F } } \| )$ to denote its total euclidean edge length. To simplify the description, let $\theta ( n ) : [ \theta _ { 1 } ( n ) , \theta _ { 2 } ( n ) ]$ represent $\theta ( n ) =$ $\Omega ( \theta _ { 1 } ( n ) )$ and $\theta ( n ) = O ( \theta _ { 2 } ( n ) ) ;$ ; and let $\dot { \theta } ( \bar { n ) } : ( \theta _ { 1 } ( n ) , \theta _ { 2 } ( n ) ]$ represent $\theta ( n ) = \omega ( \theta _ { 1 } ( n ) )$ Þ and $\theta ( n ) = O ( \theta _ { 2 } ( n ) )$ Þ.

# 3 MAIN RESULTS

In this paper, for both HEN and HDN, we design three types of strategies, i.e., hybrid strategy, ordinary ad hoc strategy, and BS-based strategy. Please see Fig. 1 for illustrations.

1. Ordinary ad hoc strategy will not use any base station, in other words, we treat the hybrid network as a pure ad hoc network assuming there are no base stations.   
2. BS-based strategy can only allow receivers (or source nodes) to communicate with base stations in corresponding subregions directly, i.e., we do not allow any relay nodes in each subregion.   
3. Hybrid strategy uses a specific routing and scheduling scheme to let receivers (or source nodes) communicate with central base stations in the corresponding subregion, in particular, we can use the other ordinary ad hoc nodes in the same subregion to relay data.

# 3.1 Optimal Decision Based on Three Strategies

According to different scenarios in terms of $m , n ,$ and ${ \boldsymbol { n } } _ { d } ,$ we select the optimal scheme from the three categories of strategies for HEN and HDN, respectively, and derive the achievable multicast throughput based on the optimal scheme.

# 3.1.1 Optimal Strategy among Three Strategies for HEN

Theorem 1. Combining three types of multicast strategies, the optimal decision of strategy and the achievable multicast throughput for HEN are made as in Table 1.

# 3.1.2 Optimal Strategy among Three Strategies for HDN

Theorem 2. Combining three types of multicast strategies, the optimal decision of strategy and the achievable multicast throughput for HDN are made as in Table 2.

# 3.2 Discussion for Results

# 3.2.1 Generality of Results

Due to the generality of multicast, that is, unicast and broadcast can be regarded as the special cases of multicast, our results can unify the throughput for unicast and broadcast by letting $n _ { d } = 1$ and $n _ { d } = n - 1 ,$ , respectively. However, when we specialize to unicast throughput, i.e., let $n _ { d } = 1 .$ , there is indeed a gap of factor $\left( \log n \right) ^ { - { \frac { \alpha } { 2 } } }$ between our results for HEN and those in [11]. In fact, for the routing of [11], the ordinary ad hoc nodes in each subregion access to the corresponding BS via the connectivity paths defined in Section 5 of this paper. Unlike in dense networks, the connectivity paths in extended networks can only sustain a rate of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ instead of the constant rate as stated [11, Lemma 5]. We believe, the mistake [11, Lemma 5] leads to the gap between our results for unicast case and their results.

# 3.2.2 Analysis of Bottlenecks

As in most existing works for the capacity of hybrid networks, we also assume the links between base stations and ordinary ad hoc nodes (we call such links B-O links) have no difference from those among ordinary ad hoc nodes. While, in the analysis of bottlenecks on three types of strategies for both HEN and HDN (Sections 5 and 6), we find that for most cases in terms of m and ${ \boldsymbol { n } } _ { d } ,$ the bottlenecks locate on B-O links. Therefore, if the bandwidth of B-O links can be increased, the throughput for the whole network will possibly be enhanced. Hence, when we consider the hybrid strategies, we designedly derive the throughput without taking the possible bottlenecks on the B-O links into account. (Please see details in Theorems 3, 5, 10, and 12.) We deem that these results could be used when some new assumptions are made for the B-O links.

TABLE 1 Optimal Decision of Strategy and Multicast Throughput for HEN 

<table><tr><td>Range in terms of m</td><td>Relations among m, nd and n</td><td>Optimal Strategy</td><td>Multicast Throughput</td></tr><tr><td rowspan="2">m : [1, n/ log n]</td><td>If {nd: [1, n/(log n)α+1] and m: [√nnd·(log n)α, n/ log n]</td><td>Hybrid Strategy</td><td>Ω(m/n·nd·(log n)-α/2)</td></tr><tr><td>Otherwise</td><td>Ordinary Ad Hoc Strategy</td><td>Theorem 8</td></tr><tr><td rowspan="7">m : [n/ log n, n]</td><td>If nd: [1, n/(log n)α+2]</td><td>BS-based strategy</td><td> $\frac{m}{nn_{d}} \cdot (\frac{n}{m})^{-\frac{\alpha}{2}}$ </td></tr><tr><td>Else If {nd: [n/(log n)α+2, n/(log n)α+1] and m: [(nα+1·nd)1/α+2, n]</td><td>BS-based strategy</td><td> $\frac{m}{nn_{d}} \cdot (\frac{n}{m})^{-\frac{\alpha}{2}}$ </td></tr><tr><td>Else If {nd: [n/(log n)α+1, n/(log n)2] and m: [n·(log n)-α+1/α+2, n]</td><td>BS-based strategy</td><td> $\frac{m}{nn_{d}} \cdot (\frac{n}{m})^{-\frac{\alpha}{2}}$ </td></tr><tr><td>Else If {nd: [n/(log n)2, n/ log n] and m: [(nα+1·(log n)1-α·nd)1/α+2, n]</td><td>BS-based strategy</td><td> $\frac{m}{nn_{d}} \cdot (\frac{n}{m})^{-\frac{\alpha}{2}}$ </td></tr><tr><td>Else If {nd: [n/ log n, m] and m: [n·(log n)-α/α+2, n]</td><td>BS-based strategy</td><td> $\frac{m}{nn_{d}} \cdot (\frac{n}{m})^{-\frac{\alpha}{2}}$ </td></tr><tr><td>Else If {nd: [m, n] and m: [(n/nd)2/α·n/ log n, n]</td><td>BS-based strategy</td><td> $\frac{1}{n} \cdot (\frac{n}{m})^{-\frac{\alpha}{2}}$ </td></tr><tr><td>Otherwise</td><td>Ordinary Ad Hoc Strategy</td><td>Theorem 8</td></tr></table>

TABLE 2 Optimal Decision of Strategy and Multicast Throughput for HDN 

<table><tr><td>Range in terms of  $m$ </td><td>Relations among  $m,{n}_{d}$  and  $n$ </td><td>Optimal Strategy</td><td>Multicast Throughput</td></tr><tr><td rowspan="4"> $m :\left\lbrack {1,n/\log n}\right\rbrack$ </td><td>If  $\left\{  \begin{array}{l} {{n}_{d} : \left\lbrack  {1,n/\left( {\log n}\right) {}^{3}}\right\rbrack  \text{and }} \\  m : \left\lbrack  {\sqrt{n{n}_{d}},n/\log n}\right\rbrack  \end{array}\right.$ </td><td>Hybrid Strategy</td><td> $\Omega \left( \frac{m}{n \cdot  {n}_{d}}\right)$ </td></tr><tr><td>Else If  $\left\{  \begin{array}{l} {{n}_{d} : \left\lbrack  {n/\left( {\log n}\right) {}^{3},n/\left( {\log n}\right) {}^{2}}\right\rbrack  \text{and }} \\  m : \left\lbrack  {n \cdot  {\left( \log n\right) }^{-\frac{3}{2}},n/\log n}\right\rbrack  \end{array}\right.$ </td><td>Hybrid Strategy</td><td> $\Omega \left( \frac{m}{n \cdot  {n}_{d}}\right)$ </td></tr><tr><td>Else If  $\left\{  \begin{array}{l} {{n}_{d} : \left\lbrack  {n/\left( {\log n}\right) {}^{2},n/\left( {\log n}\right) }\right\rbrack  \text{and }} \\  m : \left\lbrack  {\sqrt{n{n}_{d}} \cdot  {\left( \log n\right) }^{-\frac{1}{2}},n/\log n}\right\rbrack  \end{array}\right.$ </td><td>Hybrid Strategy</td><td> $\Omega \left( \frac{m}{n \cdot  {n}_{d}}\right)$ </td></tr><tr><td>Otherwise</td><td>Ordinary Ad Hoc Strategy</td><td>Theorem 15</td></tr><tr><td> $m :\left\lbrack  {n/\log n,n}\right\rbrack$ </td><td></td><td>BS-based strategy</td><td>Theorem 16</td></tr></table>

# 3.2.3 Matching Upper Bounds

To the best of our knowledge, even for wireless ad hoc networks, for both random extended networks and random dense networks, there are still no matching upper and lower bounds for multicast capacity under Gaussian Channel model, [3]. For hybrid networks, there is no result for such upper bounds. A trivial upper bound is of order Oð1Þ, which is the bound without interference limitation, [12], [13]. For both HEN and HDN, this bound can be achieved by BS-based strategy when $m = \Theta ( n )$ and $n _ { d } = \Theta ( 1 )$ . Please see Tables 1 and 2. It is an interesting issue to derive the upper bounds and validate whether the lower bounds proposed in this paper are tight or not for any regime in terms of m : ½1; nand $n _ { d } : [ 1 , n ]$ .

Moreover, we limit the scope of this paper to networkingtheoretic capacity bounds, i.e., we assume that the signals received from nodes other than one particular transmitter are simply regarded as noise degrading the communication link [2], [10]. From the information-theoretic perspective [14], the bounds beyond those in this paper can be possibly achieved by introducing some physical layer cooperative strategies [13].

# 4 TECHNICAL PREPARATIONS

# 4.1 Probability Inequality

Lemma 1 (Chebyshev’s Inequality). Let X be a random variable, then

$$
\operatorname * {P r} (| X - \mathbf {E} (X) | \geq \epsilon) \leq \mathbf {V a r} (X) / \epsilon^ {2},
$$

where EðXÞ is the mean of X, VarðXÞ is the variance of X, and  is an arbitrary small positive value.

In the following analysis, we often need to prove the uniform convergence of the probability of some events. Vapnik-Chervonenkis Theorem [15] is usually exploited to prove such issue, as in [2], [4], [8]. When the deployment region A is partitioned into a lattice consisting of subsquares that act as Voronoi cells, the exponent tails of probability bound can be equally used to prove the uniform convergence of some probability [10].

Lemma 2 (Tails of Chernoff bounds, Mitzenmacher and Upfal [16]). Let X be a Poisson random variable with parameter . Then,

$$
\operatorname * {P r} (X \geq x) \leq \frac {e ^ {- \lambda} \cdot (e \lambda) ^ {x}}{x ^ {x}}, \quad \text { for   } x > \lambda , \tag {1}
$$

$$
\operatorname * {P r} (X \leq x) \leq \frac {e ^ {- \lambda} \cdot (e \lambda) ^ {x}}{x ^ {x}}, \quad \text { for } 0 <   x <   \lambda . \tag {2}
$$

Proof. The upper tail (1) has been proved by Franceschetti et al. in [10]. Here, we concisely prove the lower tail (2). For $t > 0$ and $0 \leq x < \lambda _ { \cdot }$ , by Markov Inequality,

$$
\operatorname * {P r} (X \leq x) = \operatorname * {P r} (- X \geq - x) \leq E (e ^ {- t X}) / e ^ {- t x}.
$$

Since EðetXÞ ¼ P1k¼0 ekk! $\begin{array} { r } { E ( e ^ { - t X } ) = \sum _ { k = 0 } ^ { \infty } \frac { e ^ { - \lambda } \lambda ^ { k } } { k ! } \cdot e ^ { - t k } = e ^ { \lambda ( e ^ { - t } - 1 ) } , } \end{array}$ thus $\Pr ( X \leq x ) \leq$ $e ^ { \lambda ( e ^ { - t } - 1 ) + t x }$ . Let $t = \ln ( \lambda / x ) > 0 ,$ we complete the proof. tu

# 4.2 Euclidean Spanning Tree

Partition the square $\mathcal { A } ( a )$ into $\rho \leq m$ subsquares while ensuring that there is one base station at the center of each subsquare, where a is the area of the deployment square region. We call those $\rho$ subsquares subregions. Note that one subregion may contain more than one base station, but we only need to use the central one in our proposed routing scheme. For each multicast session $\mathcal { M } _ { k } , k = 1 , 2 , \ldots n _ { s } ,$ , we denote the spanning set as $\mathcal { U } _ { k } = \{ v _ { k } \} \cup \{ v _ { k _ { 1 } } , v _ { k _ { 2 } } , . . . v _ { k _ { n _ { d } } } \} ,$ , where $v _ { k }$ is the source node and the nodes in the latter set are the destinations of $v _ { k }$ . Let ${ \mathcal { U } } _ { k } ^ { \iota } = \{ v _ { k _ { 1 } } ^ { \iota } , v _ { k } ^ { \iota } , \ldots , v _ { k _ { t } } ^ { \iota } \}$ denote a subset of $\mathcal { U } _ { k }$ to represent the set of nodes contained in the subregion $S _ { \iota }$ , where $\mathcal { U } _ { k } = \cup \mathcal { U } _ { k } ^ { \iota }$ and $\mathcal { U } _ { k } ^ { \iota _ { 1 } } \cap \mathcal { U } _ { k } ^ { \iota _ { 2 } } = \emptyset$ for any $\iota _ { 1 } \neq \iota _ { 2 } .$ . Let $\tilde { \mathcal { U } } _ { k } ^ { \iota } = \mathcal { U } _ { k } ^ { \iota } \cup \{ b _ { \iota } \}$ , where $b _ { \iota }$ denotes the base station that is placed at the center of subregion $S _ { \iota }$ . Then, we can build a euclidean spanning tree (EST) based on every set $\tilde { \mathcal { U } } _ { k } ^ { \iota }$ using the method in [8]. Denote those ESTs as $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ , $1 \leq \iota \leq \varphi _ { k } ,$ where $\varphi _ { k }$ is a random variable representing the number of occupied subregions, i.e., those containing at least one ordinary ad hoc node in $\mathcal { U } _ { k }$ . We note that for each $\tilde { \mathcal { U } } _ { k } ^ { \iota }$ except for that one including $v _ { k }$ (denoted by $\tilde { \mathcal { U } } _ { k } ^ { \iota _ { o } } ) , b _ { \iota }$ acts as the root of EST; for $\tilde { \mathcal { U } } _ { k } ^ { \iota _ { o } } , v _ { k }$ acts as the root of EST.

It is the complement issue of occupancy problem [17] to consider the random variable $\varphi _ { k } ,$ i.e., the number of occupied cells. Suppose that $n _ { d } + 1$ balls are randomly distributed into $\rho$ cells. Assume that each ball has an equal chance of being distributed to each cell. Let $\bar { \varphi } _ { k }$ be the number of cells remaining empty. Hence, $\varphi _ { k } = \rho - \bar { \varphi } _ { k }$ . By occupancy theory [17], the probability distribution of $\varphi _ { k }$ is given by

$$
\begin{array}{l} \operatorname * {P r} (\varphi_ {k} = z) = \operatorname * {P r} (\bar {\varphi} _ {k} = \rho - z) \\ = \sum_ {i = 1} ^ {z} (- 1) ^ {i} C _ {z} ^ {i} \left(\frac {z - i}{\rho}\right) ^ {n _ {d} + 1}, \\ \end{array}
$$

where $C _ { \rho } ^ { z }$ is the binomial coefficient equal to the number of combinations of z items selected from $\rho$ items. We necessarily pursue the uniform bound of $\varphi _ { k } , k = 1 , 2 , \ldots n _ { s } .$

Define the random variables $\varphi _ { m a x } = \operatorname* { m a x } _ { k } \{ \varphi _ { k } \}$ and $\varphi _ { m i n } = \mathrm { m i n } _ { k } \{ \varphi _ { k } \}$ . Much research has been implemented to the tail bounds for occupancy [18]. Since we concentrate on the lower bounds on multicast capacity, we only need the following straightforward upper bound on $\varphi _ { m a x }$ (Lemma $3 ) .$ , while noticing that we should use the tail bounds for occupancy to lower bound $\varphi _ { m i n }$ when we study the upper bounds on multicast capacity.

Lemma 3. $\begin{array} { r } { \varphi _ { m a x } = \operatorname* { m a x } _ { k } \{ \varphi _ { k } \} = O ( \operatorname* { m i n } \{ n _ { d } , \rho \} ) , \mathrm { w . h . p . } } \end{array}$

Next, we recall an result on the total length of the EST based on a given set of nodes.

Lemma 4 ([8]). For any set of nodes, denoted by U, placed in a square of area a, the length of a euclidean spanning tree that is obtained by Algorithm 1 with the input U is at most $2 { \sqrt { 2 a } } \cdot { \sqrt { | { \mathcal { U } } | - 1 } }$ .

Algorithm 1. Construction of EST

Input: A set of nodes U with $| \mathcal { U } | = \mathbf { u }$ that are distributed into a square region of area a

Output: A euclidean spanning tree $\mathrm { E S T } ( { \cal U } )$ .

1: In the initial state, all nodes in U are isolated, then there are u connected components.   
2: for $i = 1 : \mathbf { u } - 1$ do   
3: Partition the deployment region $\mathcal { A } ( a ) = [ 0 , \sqrt { a } ] ^ { 2 }$ into at most u  i square cells of side length $\sqrt { a } / \lfloor \sqrt { \mathbf { u } - i } \rfloor ;$   
4: Find a cell that contains more than two nodes of U belonging to two different connected components. By connecting the pair of nodes, we merge the two connected components.

# 5: end for

Denote the forest consisting of all $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } ) ~ ( 1 \leq \iota \leq \varphi _ { k } ) ,$ as $\mathcal { F } _ { k } .$ . Then, we have

Lemma 5. The total euclidean edge length of p $\mathcal { F } _ { k } , i . e . , \| \mathcal { F } _ { k } \| ,$ , is, w.h.p., of order $\begin{array} { r } { O ( \frac { \sqrt { a } } { \sqrt { \rho } } \cdot \sqrt { n _ { d } \cdot \operatorname* { m i n } \{ n _ { d } , \rho \} } ) } \end{array}$ , for any $k , 1 \leq k \leq n _ { s } .$

Proof. Denote the number of vertexes of $\mathrm { E S T } ( { \mathcal { U } } _ { k } ^ { \iota } )$ by $\boldsymbol { x } _ { k } ^ { \iota } ,$ , and that of $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ by $\tilde { x } _ { k } ^ { \iota } ,$ where $1 \leq \iota \leq \varphi _ { k }$ and $1 \leq k \leq n _ { s }$ . Obviously, $\tilde { x } _ { k } ^ { \iota } = x _ { k } ^ { \iota } + 1$ . According to Lemma $\begin{array} { r } { 4 , \| \mathrm { E S T } ( \mathcal { U } _ { k } ^ { \iota } ) \| = O ( \sqrt { x _ { k } ^ { \iota } - 1 } \cdot \frac { \sqrt { a } } { \sqrt { \rho } } ) } \end{array}$ . Hence, there exists a constant $\kappa _ { 1 }$ such that

$$
\sum_ {\iota = 1} ^ {\varphi_ {k}} \| \operatorname{EST} \left(\mathcal {U} _ {k} ^ {\iota}\right) \| \leq \kappa_ {1} \cdot \frac {\sqrt {a}}{\sqrt {\rho}} \cdot \sum_ {\iota = 1} ^ {\varphi_ {k}} \sqrt {x _ {k} ^ {\iota} - 1}.
$$

By the Cauchy-Schwartz Inequality, we have

$$
\sum_ {\iota = 1} ^ {\varphi_ {k}} \sqrt {x _ {k} ^ {\iota} - 1} \leq \sqrt {\varphi_ {k} \sum_ {\iota = 1} ^ {\varphi_ {k}} (x _ {k} ^ {\iota} - 1)} \leq \sqrt {\varphi_ {k} (n _ {d} - \varphi_ {k})}.
$$

Since $\begin{array} { r } { \| \mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } ) \| \leq \| \mathrm { E S T } ( \mathcal { U } _ { k } ^ { \iota } ) \| + \frac { \sqrt { 2 a } } { \sqrt { \rho } } } \end{array}$ , there is a constant 2 such that $\begin{array} { r } { \left\| \mathcal { F } _ { k } \right\| \le \frac { \sqrt { a } } { \sqrt { \rho } } \cdot \left( \kappa _ { 1 } \sqrt { \varphi _ { k } \cdot ( n _ { d } - \varphi _ { k } ) } + \kappa _ { 2 } \cdot \varphi _ { k } \right) } \end{array}$ . Then, $\begin{array} { r } { \| \mathcal F _ { k } \| = O ( \frac { \sqrt { a } } { \sqrt { \rho } } \cdot \sqrt { n _ { d } \cdot \varphi _ { k } } ) } \end{array}$ . Combining with Lemma 3, we complete the proof. tu

# 4.3 Result on Bond Percolation Model

Let $\mathbb { B } ( h , p )$ denote a square lattice composed of $h \times h$ subsquares in which each edge is open with the probability p [19]. We call a path consisting of only open edges (bonds) open path. For a given constant $\kappa > 0 ,$ , we partition the lattice $\mathbb { B } ( h , p )$ into horizontal (vertical) rectangle slabs with the horizontal (or vertical) width of h and the vertical (horizontal) width of  log $h - \epsilon ( h )$ , denoted by $R _ { i } ^ { h }$ (or $R _ { i } ^ { v } )$ . We can choose $\varepsilon _ { h }$ as the smallest value such that the number of rectangle slabs h log hðhÞ is an integer. It is $\frac { h } { \kappa \log h - \epsilon ( h ) }$ obvious that $\epsilon ( h ) = o ( 1 )$ as $h  \infty [ 1 0 ]$ . Denote the number of edge-disjoint open paths in slab $R _ { i } ^ { h }$ (or $R _ { i } ^ { v } )$ by $N _ { i } ^ { h }$ (or $N _ { i } ^ { v } )$ . Let $N ^ { h } \dot { = } \operatorname* { m i n } _ { i } \dot { N } _ { i } ^ { h } , \ \dot { N } ^ { v } = \operatorname* { m i n } _ { i } N _ { i } ^ { v }$ . Then, we have

Lemma 6 ([10]). For any constants $\kappa > 0$ and $p \in ( \frac { 5 } { 6 } , 1 )$ satisfying $2 + \kappa \log ( 6 ( 1 - p ) ) < 0 .$ , there exists a constant $\delta ( \kappa , p )$ such that

$$
\lim _ {h \to \infty} \operatorname * {P r} (N ^ {h} \geq \delta \log h) = 1; \lim _ {h \to \infty} \operatorname * {P r} (N ^ {v} \geq \delta \log h) = 1.
$$

# 4.4 Bottleneck Principle

When the adopted strategy is of hierarchical structure, the final network throughput is determined by the bottleneck in certain phase. That is,

Lemma 7. The achievable multicast throughput derived by the strategy = is of $\Lambda = \operatorname* { m i n } \{ \Lambda _ { j } ; j = 1 , 2 , . . . , \tau \}$ , where we assume that the routing scheme consists of 
 phases and let $\Lambda _ { j }$ denote the throughput in Phase $j .$

# 5 MULTICAST STRATEGIES FOR HEN

We design three types of multicast strategies, i.e., hybrid strategy, ordinary ad hoc strategy, and BS-based strategy, to obtain the achievable multicast throughput for hybrid extended network. A novel technique called parallel transmission scheduling [1] is introduced. The assumption is reclaimed that the bottleneck of the whole routing does not locate on the links among BSs, since they are connected by high-bandwidth wired network. However, the links between BSs and ordinary ad hoc nodes become possibly, actually often, the bottleneck throughout the whole routing. As mentioned above, for the simplicity of analysis, wep partition AðnÞ into  (  m) subregions of side length n  ffiffi p , $\mathcal { A } ( n )$ $\rho \ ( \rho \leq m )$ $\frac { \surd n } { \surd \rho }$ ensuring there is at least one base station contained in each subregion. Note that there may be more than one base station located at same subregion, but we are only interested at the central one. In the following context, we denote the base station located at the center of subregion $S _ { \iota }$ by $b _ { \iota }$ .

All our strategies are devised based on the cell-partitioned method [4], [8], [10]. For clarify the description of the strategies, we first introduce a notion called scheme lattice.

Definition 4 (Scheme Lattice). Divide a square deployment region of side length d into a lattice consisting of square cells of side length l, we call the lattice scheme lattice and denote it as $\mathbb { L } ( \mathbf { d } , \mathbf { l } , \theta )$ , where $\theta \in [ 0 , \frac { \pi } { 4 } ]$ is the minimum angle between the edges of the deployment region and those of the cells.

# 5.1 Hybrid Strategy for HEN

The hybrid strategies can be further classified into two optional strategies called connectivity strategy and percolation strategy, respectively.

# 5.1.1 Connectivity Strategy

We state that the connectivity strategy can be applied when $\rho = O ( n / \log n )$ . We denote connectivity strategy by $\bar { \mathfrak { I } _ { e , } }$ , and the routing and wireless transmission scheduling by $\bar { \mathfrak { I } } _ { e } ^ { r }$ and $\bar { \mathfrak { I } } _ { e } ^ { t } .$ , respectively. Divide $\mathcal { A } ( n )$ into subsquares with area $\bar { a } _ { e } = 2 \theta \cdot \log n ,$ where $\theta$ is a constant with $\begin{array} { r } { \hat { \theta ^ { \mathrm { ~ } } } > \frac { 1 } { 2 \log 2 - \log e } } \end{array}$ . That is, we design the strategy based on the scheme lattice $\mathbb { L } ( { \sqrt { n } } , { \sqrt { { \bar { a } } _ { e } } } , 0 )$ in which the cells are called connectivity cells. Furthermore, we separate each cell into halves horizontally (or vertically) called horizontal (or vertical) half-cells. Please see the illustration in Fig. 3b. Then, we have

Lemma 8. With high probability, there are at most 2  log n and at least $\textstyle { \frac { \theta } { 2 } }$  log n ordinary ad hoc nodes in every half-cell.

Proof. Define the number of ordinary ad hoc nodes in any half-cell, say $c _ { i } ,$ as a random variable $\mu _ { i } .$ . Then, $\mu _ { i }$ follows the Poisson distribution of mean $\bar { a } _ { e } / 2 ,$ , i.e.,   log n. Further, we define the minimum of $\mu _ { i }$ for all $c _ { i }$ as $\underline { { \boldsymbol \chi } } _ { \boldsymbol \chi } ^ { * }$ and define the maximum of $\mu _ { i }$ for all $c _ { i }$ as ${ \overline { { \chi } } } .$ .

Combining (1) in Lemma 2 and union bounds, we have

$$
\begin{array}{l} \operatorname * {P r} (\overline {{\chi}} \geq 2 \theta \cdot \log n) \leq \frac {4 n}{\bar {a} _ {e}} \cdot \operatorname * {P r} (\mu_ {i} \geq 2 \theta \cdot \log n) \\ \leq n \cdot (e / 4) ^ {\theta \cdot \log n} \\ = (e / 4) ^ {(\theta - \frac {1}{2 \log 2 - \log e}) \cdot \log n}. \\ \end{array}
$$

Thus, by $\begin{array} { r } { \theta > \frac { 1 } { 2 \log { 2 } - \log { e } } } \end{array}$ , we have $\operatorname* { P r } ( \overline { { \chi } } \geq 2 \theta \cdot \log n )  0 .$

Similarly, combining (2) in Lemma 2 and union bounds, we have

$$
\begin{array}{l} \operatorname * {P r} \left(\underline {{\chi}} \leq \frac {\theta}{2} \cdot \log n\right) \leq \frac {4 n}{\bar {a} _ {e}} \cdot \operatorname * {P r} \left(\mu_ {i} \leq \frac {\theta}{2} \cdot \log n\right) \\ \leq n \cdot (1 / 2 e) ^ {\frac {\theta}{2} \cdot \log n} \\ = (1 / 2 e) ^ {(\theta - \frac {2}{\log 2 e}) \cdot \frac {\log n}{2}}. \\ \end{array}
$$

Then, by $\begin{array} { r } { \theta > \frac { 1 } { 2 \log { 2 } - \log { e } } } \end{array}$ , we have that $\textstyle \theta > { \frac { 2 } { \log { 2 e } } }$ > 2log 2e . Hence, $\operatorname* { P r } ( \underline { { \chi } } \leq \frac { \theta } { 2 } \cdot \log n ) \ \stackrel { \smile } { \to } 0 .$

Therefore, for all half-cells, it holds uniform, $w . h . p . ,$ , that $\mu _ { i } \in ( \frac { \theta } { 2 } \cdot \log n , 2 \theta \cdot \log n )$ , which completes the proof.tu

Routing scheme $\bar { \mathfrak { I } } _ { e } ^ { r } .$ . We propose Algorithm 2 to construct the multicast routing tree $\mathcal { T } ( \mathcal { U } _ { k } )$ for multicast session $\mathcal { M } _ { k }$ .

Algorithm 2. Connectivity Routing Scheme $\bar { \mathfrak { I } } _ { e } ^ { r }$ Input: $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } ) , 1 \leq \iota \leq \varphi _ { k } .$

Output: A multicast routing tree $\mathcal { T } ( \mathcal { U } _ { k } )$

1: for each $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
2: for each link $u _ { i } u _ { j }$ in $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
3: Connect $u _ { i }$ and $u _ { j }$ using Manhattan routing: Denote the intersection point of the horizontal line through $u _ { i }$ and the vertical line through $u _ { j }$ as $p _ { i , j } ,$ and denote the nearest node to point $p _ { i , j }$ as $u _ { i , j } ;$ choose randomly a node in each half-cell passed by $u _ { i } u _ { i , j }$ and $u _ { j } u _ { i , j }$ , and connect alternately those nodes, as illustrated in Fig. 2.   
4: end for   
5: Merge the same edges (hops) and remove the circles that have no impact on the connectivity of $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ , we obtain the multicast tree $\mathcal { T } ( \mathcal { U } _ { k } ^ { \iota } )$ .   
6: end for   
7: Based on the forest consisting of the constructed trees, i.e., $\mathcal { T } ( \mathcal { U } _ { k } ^ { \iota } ) \mathrm { ~ } ( 1 \leq \iota \leq \varphi _ { k } )$ , we obtain the final multicast tree $\mathcal { T } ( \mathcal { U } _ { k } )$ by connecting base stations $b _ { \iota } ( 1 \leq \iota \leq \varphi _ { k } )$ .

![](images/911c9a3a57705a356a6e0546be631c9f9d2cde6dcd0ed510369fd40e4a7474ad.jpg)



(a)

![](images/0018f2827c98bf08d75cbc71c1e2c29b10e428737da9061a69362cde5a848eb2.jpg)



![](images/5deb0c7c4b116c6206908c320c08efe8fc76c6bf3a0d7ba5f92d0c21285303eb.jpg)



![](images/e4e853b4c2e5d22ef70c08c2f3aac7dd7045f1ac40f45eaa792d9ffeda07e084.jpg)



(b)   
Fig. 2. Construction of connectivity paths. There are at least  log n connectivity paths, represented by the chains, in each column or row. (a) Horizontal parallel connectivity paths. (b) Vertical parallel connectivity paths.

For each edge $u _ { i } u _ { j } \in \mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } ) , 1 \leq \iota \leq \varphi _ { k } .$ we use Manhattan routing to realize it. Note that each hop in Manhattan routing connects two nodes belonging to two adjacent connectivity cells but nonadjacent horizontal (or vertical) half-cells, which ensures that the euclidean length of each hop is at most $\textstyle { \frac { \sqrt { 1 3 } } { 2 } } \sqrt { \bar { a } _ { e } }$ and at least $\frac { 1 } { 2 } \sqrt { \bar { a } _ { e } }$ . We call such paths connectivity paths. According to Lemma 8, there are at least $\textstyle { \frac { \theta } { 2 } }$ log n connectivity paths in each slab of size ${ \sqrt { { \bar { a } } _ { e } } } \times { \sqrt { n } }$ . Hence, we can allocate the total traffic of each slab to such  log n connectivity paths averagely. Please see Fig. 2 for the illustrations.

Transmission scheduling $\bar { \mathfrak { I } } _ { e } ^ { t }$ . We adopt a 9-TDMA scheme, and further divide each time slot into four equal subslots during which we schedule in turn the four half-cells of each cell (Fig. 3). The main technique called parallel transmission scheduling used here is: in each activated subslot, we schedule simultaneously $\textstyle { \frac { \theta } { 2 } }$  log n parallel links (the existence guaranteed by Lemma $^ { 8 ) }$ instead of scheduling only one link in most previous works [4], [10]. We further prove the following result:

Lemma 9. By using the parallel transmission scheduling $\bar { \Im } _ { e } ^ { t } ,$ the rate along each connectivity path can be sustained of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ .

Proof. Considering any link in any time slot, since the length of the link is at least $\begin{array} { r } { \frac { 1 } { 2 } \sqrt { \bar { a } _ { e } } , } \end{array}$ we obtain that the sum of interferences to the receivers is bounded by

![](images/ec2a88c1961a2a64769d78d6bbbee699cc45d7a4e0df3fa6b41aade1a36ba928.jpg)



![](images/57c1008640b7787a135e32bbcc24638ec8b0cf69d4d1d7ab582d9f11cd9e87f0.jpg)



(b)   
Fig. 3. The shaded cells can be scheduled simultaneously in a 9-TDMA scheme. Each time slot can be further divided into four subslots, and the four half-cells in each cell are scheduled one out of four subslots. (a) 9-TDMA. (b) Four subslots.

$$
\begin{array}{l} I (n) \leq P \cdot \left(\frac {\theta}{2} \log n - 1\right) \cdot \ell \left(\frac {1}{2} \sqrt {\bar {a} _ {e}}\right) \\ + \sum_ {i = 1} ^ {n} 8 i \cdot \left(\frac {\theta}{2} \log n\right) \cdot P \cdot \ell \left(\frac {3 i - 2}{2} \sqrt {\bar {a} _ {e}}\right) \\ \leq P \cdot \left(\frac {2}{\theta}\right) ^ {\frac {\alpha}{2} - 1} \cdot (\log n) ^ {1 - \frac {\alpha}{2}} \cdot \left(1 + \lim _ {n \rightarrow \infty} \sum_ {i = 1} ^ {n} \frac {8 i}{(3 i - 2) ^ {\alpha}}\right). \\ \end{array}
$$

The last limitation obviously converges when $\alpha > 2 ,$ , thus $I _ { n } = o ( 1 )$ . Since the length of every hop is at most $\textstyle \frac { \sqrt { 1 3 \bar { a } _ { e } } } { 2 }$ , we have the signal SðnÞ at the receiver can be bounded by

$$
S (n) \geq (1 3 \theta / 2) ^ {- \frac {\alpha}{2}} \cdot P \cdot (\log n) ^ {- \frac {\alpha}{2}}.
$$

By $\alpha > 2$ and $N _ { 0 } > 0 ,$ we have that

$$
\frac {S (n)}{N _ {0} + I (n)} = (\log n) ^ {- \frac {\alpha}{2}} \rightarrow 0.
$$

Under the scheme $\bar { \Im } _ { e } ^ { t } ,$ all connectivity paths can be scheduled twice in $4 \times 9$ subslots. Hence, each link can sustain a rate of $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . tu

Throughput derived by $\bar { \mathfrak { I } _ { e } } .$ . First, we consider the relay burden of each connectivity path.

Lemma 10. By the routing scheme $\bar { \mathfrak { I } } _ { e } ^ { r } ,$ , the relay burden of each connectivity path is at most of order

$$
\bar {L} _ {e} ^ {r} = \left\{ \begin{array}{l l} O (n _ {d} \sqrt {n} / \sqrt {\rho \log n}) & \text {when} \quad n _ {d}: [ 1, \rho ], \\ O (\sqrt {n n _ {d}} / \sqrt {\log n}) & \text {when} \quad n _ {d}: [ \rho , n / \log n ], \\ O (n _ {d}) & \text {when} \quad n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

Proof. Given a node $\bar { v } _ { t } ^ { * }$ on a connectivity path, define the number of multicast sessions routed through $\bar { v } _ { t } ^ { * }$ as a random variable $\bar { \xi } _ { t }$ . We finally consider the uniform upper bound $\bar { \xi }$ of $\bar { \xi } _ { t }$ for every node. Define an event $\bar { E } _ { e } ^ { r } ( k , t )$ : The multicast session $\mathcal { M } _ { k }$ passes through $\bar { v } _ { t } ^ { * }$ . Obviously, if $\bar { E } _ { e } ^ { r } ( k , t )$ happens then there exists an edge $u _ { i } u _ { j } \in \mathcal { F } _ { k }$ that is routed through $\bar { v } _ { t } ^ { * } ,$ , i.e., $u _ { i } u _ { i , j }$ or $u _ { i , j } u _ { j }$ passes through $\bar { v } _ { t } ^ { * }$ . Since there exists a constant $\varrho _ { 1 }$ such that

$$
| u _ {i} u _ {i, j} | \leq | u _ {i} p _ {i, j} | + \varrho_ {1} \cdot \sqrt {\bar {a} _ {e}}, | u _ {i, j} u _ {j} | \leq | p _ {i, j} u _ {j} | + \varrho_ {1} \cdot \sqrt {\bar {a} _ {e}}
$$

and for $| u _ { i } p _ { i , j } | + | p _ { i , j } u _ { j } | \leq \sqrt { 2 } | u _ { i } u _ { j } |$ , we have

$$
\begin{array}{l} \operatorname * {P r} (\bar {E} _ {e} ^ {r} (k, t)) \\ \leq \frac {1}{\frac {\theta}{2} \cdot \log n} \cdot \frac {\sqrt {\bar {a} _ {e}}}{n} \cdot \sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} \left(| u _ {i} u _ {i, j} | + | u _ {i, j} u _ {j} | + 4 \sqrt {\bar {a} _ {e}}\right) \\ \leq \frac {2}{\theta \log n} \left(\frac {(4 + 2 \varrho_ {1}) (n _ {d} + \varphi_ {k}) \bar {a} _ {e}}{n} + \frac {\sqrt {2 \bar {a} _ {e}}}{n} \cdot \sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} | u _ {i} u _ {j} |\right) \\ \leq \frac {1}{n} \cdot (\kappa_ {3} \cdot n _ {d} + \frac {4}{\sqrt {\theta \cdot \log n}} \cdot \| \mathcal {F} _ {k} \|) \\ \leq \frac {1}{n} \cdot \left(\kappa_ {3} \cdot n _ {d} + \frac {\kappa_ {4}}{\sqrt {\log n}} \cdot \sqrt {\frac {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}{\rho}}\right), \\ \end{array}
$$

where $\kappa _ { 3 }$ and $\kappa _ { 4 }$ are some constants and the last inequality is true according to Lemma 5. Thus, an upper bound of $\bar { \xi } _ { t } ^ { } ,$ , denoted as $\bar { \eta } _ { t }$ , follows a Poisson with

$$
\bar {\lambda} _ {e} = \frac {n _ {s}}{n} \left(\kappa_ {3} \cdot n _ {d} + \kappa_ {4} \sqrt {\frac {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}{\rho \cdot \log n}}\right).
$$

Hence, by union bounds, we have

$$
\operatorname * {P r} (\bar {\xi} > \sigma \bar {\lambda} _ {e}) \leq \frac {1}{\bar {a} _ {e}} \cdot \operatorname * {P r} (\bar {\xi} _ {t} > \sigma \bar {\lambda} _ {e}) \leq \frac {n}{2 \log n} \operatorname * {P r} (\bar {\eta} _ {t} > \sigma \bar {\lambda} _ {e}).
$$

According to Lemma 2, for $\begin{array} { r } { \sigma > 1 , \mathrm { P r } ( \bar { \eta } _ { t } > \sigma \bar { \lambda } _ { e } ) \leq ( \frac { e ^ { \sigma - 1 } } { \sigma ^ { \sigma } } ) ^ { \bar { \lambda } _ { e } } } \end{array}$ . Since $n _ { s } = \Theta ( n )$ and $\bar { \lambda } _ { e } = \Omega ( \log n )$ , we can choose  satisfying $\begin{array} { r } { \frac { e ^ { \sigma - 1 } } { \sigma ^ { \sigma } } < 1 } \end{array}$ (e.g., let $\sigma = e )$ , by which we get

$$
\operatorname * {P r} (\bar {\xi} > \sigma \bar {\lambda} _ {e}) = O (1 / \log n) \to 0, \text {   as   } n \to 0.
$$

Then, the relay burden of every node on connectivity paths is of order $O ( \bar { \lambda } _ { e } )$ , which completes the proof. tu

Combining Lemmas 9 and 10, we can easily obtain Theorem 3.

Theorem 3. When $\rho = O ( n / \log n )$ , by the strategy $\bar { \mathfrak { I } _ { e } }$ without taking the bottlenecks on BSs into account, the per-session multicast throughput for HEN can be achieved of order

$$
\bar {\Lambda} _ {e} ^ {\bar {r} _ {b}} = \left\{ \begin{array}{l l} \Omega \Big ((\log n) ^ {\frac {1 - \alpha}{2}} \cdot \frac {\sqrt {\rho}}{n _ {d} \sqrt {n}} \Big) & \text {when} \quad n _ {d}: [ 1, \rho ], \\ \Omega \Big ((\log n) ^ {\frac {1 - \alpha}{2}} \cdot \frac {1}{\sqrt {n n _ {d}}} \Big) & \text {when} \quad n _ {d}: [ \rho , n / \log n ], \\ \Omega \Big ((\log n) ^ {- \frac {\alpha}{2}} \cdot \frac {1}{n _ {d}} \Big) & \text {when} \quad n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

In the following context, we will consider the possible bottleneck that may happen on BSs. Under the strategy $\bar { \mathfrak { I } _ { e } } ,$ all source nodes in some subregion $S _ { \iota }$ will send data to the base station $b _ { \iota }$ as long as some receiver node(s) falling outside of $S _ { \iota }$ . Thus, the base station may become the bottleneck of the network when the number of source nodes exceeds some value. With the increasing number of source nodes inside one subregion, if most of source nodes have some receivers outside the subregion, the base stations may have huge burden, thus become bottlenecks. Using the similar method to Lemma 10, we have the following lemma:

Lemma 11. The maximum load of the links between BSs and ordinary ad hoc nodes is of order

$$
\bar {L} _ {e} ^ {r _ {b}} = \left\{ \begin{array}{l l} O (n \cdot n _ {d} / \rho) & \text { when } \quad n _ {d}: [ 1, \rho ], \\ O (n) & \text { when } \quad n _ {d}: [ \rho , n ]. \end{array} \right.
$$

Proof. Define an event $\bar { E } ^ { b } ( k , t )        $ The subregion $S _ { t }$ contains a node belonging to $\mathcal { U } _ { k }$ . Then, $\begin{array} { r } { \operatorname* { P r } ( \bar { E } ^ { b } ( k , t ) ) \le \frac { n _ { d } } { o } } \end{array}$ , for any $t = 1 , 2 , \ldots , \rho .$ Furthermore, define the load of each subregion as a random variable $\bar { \xi } _ { t } ^ { b } .$ Then, an upper bound of $\hat { \xi } _ { t } ^ { b } ,$ denoted as $\bar { \eta } _ { t } ^ { b } ,$ , follows a Poisson with $\textstyle { \bar { \lambda } } _ { e } ^ { b } = n \cdot { \frac { n _ { d } } { o } }$ Considering the cases , respectively, by using $\bar { \lambda } _ { e } ^ { b } = O ( \log \rho )$ ands and $\bar { \lambda } _ { d } = \Omega ( \log \rho )$ Lemma 2, we complete the proof. tu

From Lemma 9, the capacity of the links between BSs and ordinary ad hoc nodes is of order $\Omega ( ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . Thus,

Lemma 12. Under the strategy $\bar { \mathfrak { I } _ { e } } ,$ the throughput along the wireless links via BSs is of order

$$
\bar {\Lambda} _ {e} ^ {r _ {b}} = \left\{ \begin{array}{l l} \Omega \Big (\frac {\rho}{n \cdot n _ {d}} \cdot (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: [ 1, \rho ], \\ \Omega \Big (\frac {1}{n} \cdot (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: [ \rho , n ]. \end{array} \right.
$$

Combining Theorem 3 and Lemma 12, we conclude that the bottleneck of the whole routing $\bar { \mathfrak { I } } _ { e } ^ { r }$ lies on the wireless links via BSs. According to Lemma $^ { 7 , }$ we obtain the throughput achieved by connectivity strategy.

Theorem 4. By the connectivity strategy $\bar { \mathfrak { I } _ { e } } ,$ the per-session multicast throughput for hybrid extended networks can be achieved of order:

When m : $[ 1 , n / \log n ] ,$ ,

$$
\bar {\Lambda} _ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {m}{n \cdot n _ {d}} \cdot (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: [ 1, m ], \\ \Omega \Big (\frac {1}{n} \cdot (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: [ m, n ]. \end{array} \right.
$$

When m : ½n= log n; n-,

$$
\bar {\Lambda} _ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {1}{n _ {d}} \cdot (\log n) ^ {- \frac {\alpha}{2} - 1} \Big) & \text {when} \quad n _ {d}: \Big [ 1, \frac {n}{\log n} \Big ], \\ \Omega \Big (\frac {1}{n} \cdot (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{\log n}, n \Big ]. \end{array} \right.
$$

# 5.1.2 Percolation Strategy

First of all, we state that the percolation strategy applies to the case when $\textstyle \rho = O { \bigl ( } { \frac { n } { ( \log n ) ^ { 2 } } } { \bigr ) }$ ð nðlog nÞ2Þ. We adopt the percolation strategy denoted as $\Im _ { e } .$ . Obviously, the side length of each subregion is of order ðlog nÞ. We divide the region $\mathcal { A } ( n )$ into subsquares with area of a constant $a _ { e }$ by inclined lines. That is, we design the strategy based on the scheme lattice $\mathbb { L } ( { \sqrt { n } } , { \sqrt { a _ { e } } } , { \frac { \pi } { 4 } } )$ in which the cells are called percolation cells. A percolation cell is open if it is nonempty (occupied). Obviously, the open probability is $p = 1 - e ^ { - a _ { \epsilon } }$ . Using the same procedure in [10], we can map this model into a bond percolation model $\mathbb { B } ( h , p )$ where $h = \sqrt { n } / \sqrt { 2 a _ { e } }$ and $p = 1 - e ^ { - a _ { e } }$ . Moreover, we can partition $\mathcal { A } ( n )$ into slabs of size $\sqrt { 2 a _ { e } } ( \prime$  log $h - \epsilon _ { h } ) \times ( \sqrt { n } / \sqrt { m } )$ , where we can make $\frac { \sqrt { n } } { \sqrt { m } \sqrt { 2 a _ { e } } ( \kappa \log h { - \epsilon _ { h } } ) }$ be an integer by adjusting $\epsilon _ { h } = o ( 1 )$ . We call those slabs highway slabs. Then, by Lemma $6 ,$ we have the following lemma:

Lemma 13. For any $\kappa > 0$ and $a _ { e } > \log 6 + 2 / \kappa ,$ , there exists a constant $\delta _ { 1 } ( \kappa , a _ { e } )$ such that there are, w.h.p., at least $\delta _ { 1 }$ log n horizontal (vertical) highways in all highway slabs.

Based on Lemma 13, we can divide horizontally (or vertically) each highway slab into slices of size $\kappa _ { 5 } \times ( \sqrt { n } / \sqrt { \rho } )$ , where $\begin{array} { r } { \kappa _ { 5 } = \frac { \delta _ { 1 } } { 2 \kappa } } \end{array}$ is a constant. Then, we can define a mapping other words, we can ensure that the traffics initiated from each slice are taken charge by a corresponding highway, and every highway only bear with the traffic initiated from at most one slice.

Routing scheme $\Im _ { e } ^ { r } .$ . Based on every ES $\hat { \ b { \tau } } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } ) , 1 \leq \iota \leq \varphi _ { k } ,$ , we realize the routing of each link $u _ { i } u _ { j } \in \mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ by two broad phases, $\mathrm { i . e . , }$ highway phase and connectivity path phase. $\mathtt { B y }$ Lemma $^ { 8 , }$ we can build at least ${ \frac { \theta } { 2 } } \mathrm { l o g }$ n disjoint connectivity paths in each slab of size $\sqrt { \bar { a } _ { e } } \times \left( \kappa \cdot \mathrm { l o g } h - \epsilon _ { h } \right)$ . Thus, similar to routing scheme $\bar { \mathfrak { I } } _ { e } ^ { r } ,$ , we can allocate averagely the traffics initiated by such slabs to at least $\textstyle { \frac { \theta } { 2 } }$ log n connectivity paths. We propose Algorithm 3 to describe the multicast routing scheme in detail.

Algorithm 3. Percolation Routing Scheme $\mathfrak { F } _ { e } ^ { r }$

Input: EST $\hat { ( \mathcal { U } _ { k } ^ { \iota } ) } , 1 \le \iota \le \varphi _ { k }$

Output: A multicast routing tree $\mathcal { T } ( \mathcal { U } _ { k } )$

1: for each $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
2: for each link $u _ { i } u _ { j }$ in $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
3: $u _ { i }$ drains the packets into the specific horizontal highway along the specific connectivity path.   
4: Packets are carried along the horizontal highway, and are carried along the specific vertical highway.   
5: Packets are delivered to $u _ { j }$ from the vertical highway along the specific connectivity path.

6: end for

7: Merge the same edges (hops) and remove the circles that have no impact on the connectivity of $\mathrm { E S T } ( \tilde { \mathcal { U } } _ { k } ^ { \iota } )$ , we obtain the multicast tree $\mathcal { T } ( \mathcal { U } _ { k } ^ { \iota } )$ .

8: end for

9: By using the similar method as Line 7 in Algorithm 2, we obtain the final multicast tree $\mathcal { T } ( \mathcal { U } _ { k } )$ based on the forests consisting of the trees $\mathcal { T } ( \mathcal { U } _ { k } ^ { \iota } ) \ : ( 1 \leq \iota \leq \varphi _ { k } )$ .

Transmission scheduling $\Im _ { e } ^ { t }$ . We use two independent TDMA schemes to schedule transmissions along highways and connectivity paths. To be specific, we divide a scheduling period into two subperiods with the same size, which are called highway scheduling $\Im _ { e } ^ { t _ { 1 } }$ and connectivity path scheduling $\Im _ { e } ^ { t _ { 2 } }$ , respectively. The two scheduling phases corresponds to the two phases of routing, i.e., highways phase $\Im _ { e } ^ { r _ { 1 } }$ and connectivity path phase $\Im _ { e } ^ { r _ { 2 } }$ . The scheme $\Im _ { e } ^ { t _ { 1 } }$ can be adopted as same as the scheduling of highways in [10]. Then, we have

Lemma 14. By the transmission scheduling $\mathfrak { F } _ { e } ^ { t _ { 1 } }$ , the rate along highways can be achieved of order ð1Þ.

Since we can only ensure that there exists at least one connectivity path, instead of highway, passing through every BS $b _ { \iota . }$ , for $1 \leq \iota \leq \varphi _ { k }$ and $1 \leq k \leq n _ { s }$ , then similar to connectivity strategy, we have

Lemma 15. By the strategy $\Im _ { e } ,$ the throughput along the wireless links via BSs is of order $\Lambda _ { e } ^ { r _ { b } } = \bar { \Lambda } _ { e } ^ { r _ { b } }$ , where $\bar { \Lambda } _ { e } ^ { r _ { b } }$ is defined in Lemma 12.

The scheme $\Im _ { e } ^ { t _ { 2 } }$ can be adopted as same as $\bar { \mathfrak { I } } _ { e } ^ { t } .$ . Then, according to Lemma 9, we can obtain,

Lemma 16. Under the scheme $\Im _ { e } ^ { t _ { 2 } }$ , the rate along each connectivity path can be achieved of order ð 1ðlog nÞ -=2Þ. $\Omega ( \frac { 1 } { ( \log n ) ^ { \alpha / 2 } } )$

Throughput derived by $\mathfrak { F } _ { e }$ . First, we analyze the load of the routing paths in the highway phase and connectivity path phase.

Lemma 17. During highway phase $\Im _ { e } ^ { r _ { 1 } }$ , the maximum relay burden of each node on the highways is, w.h.p., of order

$$
L _ {e} ^ {r _ {1}} = \left\{ \begin{array}{l l} O \Big (\frac {\sqrt {n n _ {d}}}{\sqrt {\rho}} \Big) & \text {when} \quad n _ {d}: [ 1, \rho ], \\ O (\sqrt {n n _ {d}}) & \text {when} \quad n _ {d}: [ \rho , n / (\log n) ^ {2} ], \\ O (n _ {d} \log n) & \text {when} \quad n _ {d}: [ n / (\log n) ^ {2}, n / \log n ], \\ O (n) & \text {when} \quad n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

Proof. Given a node $v _ { t } ^ { * }$ on the highways, define the number of multicast sessions routed through $v _ { t } ^ { * }$ in highway phase $\Im _ { e } ^ { r _ { 1 } }$ as a random variable $\xi _ { t } ^ { r _ { 1 } }$ , and finally we consider the uniform upper bound $\xi ^ { r _ { 1 } }$ of $\xi _ { t } ^ { r _ { 1 } }$ . Define an Event $E _ { e } ^ { r _ { 1 } } ( k , t ) ;$ : The multicast session $\mathcal { M } _ { k }$ passes through $v _ { t } ^ { * }$ in phase $\mathfrak { I } _ { e } ^ { r _ { 1 } }$ . Obviously, if $E _ { e } ^ { r _ { 1 } } ( k , t )$ happens then there exists an edge $u _ { i } u _ { j } \in \mathcal { F } _ { k }$ that is routed through $v _ { t } ^ { * }$ in phase $\Im _ { e } ^ { r _ { 1 } }$ , in other words, a vertical (or horizontal) line through $v _ { t } ^ { * }$ intersects with the segment $u _ { i } u _ { i , j }$ (or $u _ { i , j } u _ { j } )$ . Similar to Lemma 10, we have

$$
\begin{array}{l} \operatorname * {P r} (E _ {e} ^ {r _ {1}} (k, t)) \\ \leq \frac {\kappa_ {5}}{n} \cdot \sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} \left(| u _ {i} p _ {i, j} | + | p _ {i, j} u _ {j} | + 2 \sqrt {2 a _ {e}} (\kappa \log h - \epsilon_ {h})\right) \\ \leq \frac {\kappa_ {6}}{n} \cdot (n _ {d} \log n) + \frac {\kappa_ {7}}{n} \cdot \| \mathcal {F} _ {k} \| \\ \leq \frac {1}{n} \cdot \left(\kappa_ {6} \cdot n _ {d} \cdot \log n + \kappa_ {8} \cdot \sqrt {\frac {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}{\rho}}\right), \\ \end{array}
$$

where $\kappa _ { \mathrm { 5 } } { - } \kappa _ { \mathrm { 8 } }$ are some constants and the last inequality is true according to Lemma 5. Thus, an upper bound of $\bar { \xi } _ { t } ,$ , denoted as $\eta _ { t } ,$ , follows a Poisson distribution of mean

$$
\lambda_ {e} ^ {r _ {1}} = \frac {n _ {s}}{n} \left(\kappa_ {6} \cdot n _ {d} \cdot \log n + \frac {\kappa_ {8}}{\rho} \cdot \sqrt {n \cdot n _ {d} \cdot \min \{n _ {d} , \rho \}}\right).
$$

Hence, by the similar procedure of Lemma 10, we obtain that the relay burden of every node on the highways in phase $\Im _ { e } ^ { r _ { 1 } }$ is of order $O ( \lambda _ { e } ^ { r _ { 1 } } )$ , which completes the proof. tu

Lemma 18. During the connectivity path phase $\Im _ { e } ^ { r _ { 2 } }$ , the maximum relay burden of each node on the connectivity path is, w.h.p., of order $L _ { e } ^ { r _ { 2 } } = O ( n _ { d } ( \log n ) ^ { 1 / 2 } )$ .

Proof. For a given node $v _ { t } ^ { * * }$ on the connectivity paths, define the number of multicast sessions routed through $v _ { t } ^ { * * }$ in connectivity path phase $\Im _ { e } ^ { r _ { 2 } }$ as a random variable $\xi _ { t } ^ { r _ { 2 } }$ , and finally we consider the uniform upper bound $\xi ^ { r _ { 2 } }$ of $\xi _ { t } ^ { r _ { 2 } }$ . Define an Event $E _ { e } ^ { r _ { 2 } } ( k , t )$ : The multicast session $\mathcal { M } _ { k }$ passes through $v _ { t } ^ { * * }$ in phase $\Im _ { e } ^ { r _ { 2 } }$ . We can see that if $\bar { E } _ { e } ^ { r _ { 2 } } ( k , t )$ happens then there is a node belongs to p $\boldsymbol { \mathcal { U } } _ { k }$ and locates in a slab of size $\begin{array} { r } { \frac { 2 \sqrt { \bar { a } _ { e } } } { \theta \cdot \log n } \times \left( \kappa \cdot \log h - \epsilon _ { h } \right) } \end{array}$ . Hereafte $^ { \mathrm { { r } , } }$ using a similar procedure in Lemma $^ { 1 7 , }$ we can complete the proof. tu

Combining Lemmas 14 and $^ { 1 7 , }$ we can obtain Lemma 19.

Lemma 19. During phase $\Im _ { e } ^ { r _ { 1 } }$ , the multicast throughput can be achieved of order

$$
\Lambda_ {e} ^ {r _ {1}} = \left\{ \begin{array}{l l} \Omega \Big (\frac {\sqrt {\rho}}{n _ {d} \sqrt {n}} \Big) & \text {when} n _ {d}: [ 1, \rho ], \\ \Omega \Big (\frac {1}{\sqrt {n n _ {d}}} \Big) & \text {when} n _ {d}: [ \rho , n / (\log n) ^ {2} ], \\ \Omega \Big (\frac {1}{n _ {d} \log n} \Big) & \text {when} n _ {d}: [ n / (\log n) ^ {2}, n / \log n ], \\ \Omega (1 / n) & \text {when} n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

Furthermore, combining Lemmas 16 and 18, we can obtain the following lemma:

Lemma 20. During phase =r2 , the multicast throughput can be achieved of order $\begin{array} { r } { \dot { \Lambda } _ { e } ^ { r _ { 2 } } = \Omega ( \frac { 1 } { n _ { d } } \cdot ( \log n ) ^ { - \frac { \alpha + 1 } { 2 } } ) } \end{array}$ .

Based on Lemma 19 and Lemma 20, and according to Lemma $^ { 7 , }$ we can obtain Theorem 5.

Theorem 5. When $\rho = O ( n / ( \log n ) ^ { 2 } )$ , by the percolation strategy =e without taking the bottlenecks on BSs into account, the per-session multicast throughput for HEN can be achieved of order:

When $\stackrel { \prime } { \rho } : [ 1 , ( n / ( \log n ) ^ { \alpha + 1 } ) ] .$ ,

$$
\Lambda_ {e} ^ {\overline {{r}} _ {b}} = \left\{ \begin{array}{l l} \Omega \Big (\frac {\sqrt {\rho}}{n _ {d} \sqrt {n}} \Big) & \text {when} n _ {d}: [ 1, \rho ], \\ \Omega \Big (\frac {1}{\sqrt {n n _ {d}}} \Big) & \text {when} n _ {d}: \Big [ \rho , \frac {n}{(\log n) ^ {\alpha + 1}} \Big ], \\ \Omega \Big (\frac {1}{n _ {d} \cdot (\log n) ^ {\frac {\alpha + 1}{2}}} \Big) & \text {when} n _ {d}: \Big [ \frac {n}{(\log n) ^ {\alpha + 1}}, n \Big ]. \end{array} \right.
$$

When  : ½ $\begin{array} { r } { \rho : [ \frac { n } { ( \log n ) ^ { \alpha + 1 } } , \frac { n } { ( \log n ) ^ { 2 } } ] , \Lambda _ { e } ^ { \bar { r } _ { b } } = \Omega ( \frac { 1 } { n _ { d } } ( \log n ) ^ { - \frac { \alpha + 1 } { 2 } } ) . } \end{array}$

Combining Theorem 5 and Lemma 15, we get the following result:

Theorem 6. Under the percolation strategy $\Im _ { e } ,$ the per-session multicast throughput for HEN is achieved of order:

When m : ½1; n= log n-,

$$
\Lambda_ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {m}{n \cdot n _ {d}} (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: [ 1, m ], \\ \Omega \Big (\frac {1}{n} (\log n) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: \bigg [ m, \frac {n}{\sqrt {\log n}} \bigg ], \\ \Omega \Big (\frac {1}{n _ {d}} (\log n) ^ {- \frac {\alpha + 1}{2}} \Big) & \text {when} \quad n _ {d}: \bigg [ \frac {n}{\sqrt {\log n}}, n \bigg ]. \end{array} \right.
$$

When m : ½n= log n; n-,

$$
\Lambda_ {e} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {1}{n _ {d}} (\log n) ^ {- \frac {a}{2} - 1} \Big) & \text {when} \quad n _ {d}: [ 1, n / \log n ], \\ \Omega \Big (\frac {1}{n} (\log n) ^ {- \frac {a}{2}} \Big) & \text {when} \quad n _ {d}: \bigg [ n / \log n, \frac {n}{\sqrt {\log n}} \bigg ], \\ \Omega \Big (\frac {1}{n _ {d}} (\log n) ^ {- \frac {a + 1}{2}} \Big) & \text {when} \quad n _ {d}: \bigg [ \frac {n}{\sqrt {\log n}}, n \bigg ]. \end{array} \right.
$$

Furthermore, combining Theorems 4 and $6 ,$ we can get the throughput derived by hybrid routing strategies.

Theorem 7. By the hybrid strategies, the multicast throughput for HEN is achieved of order $\Lambda _ { e } ^ { r }$ (defined in Theorem 6).

# 5.2 Ordinary Ad Hoc Strategy for HEN

Different from the previous routing strategy, in ordinary ad hoc strategy, we will not use any base station but only the ordinary ad hoc nodes. In particular, we treat the network as a ordinary ad hoc network and we construct global multicast trees composed of only ordinary nodes. Similar to the hybrid strategy, the ordinary ad hoc strategy consists of connectivity strategy and percolation strategy. Indeed, the ordinary ad hoc strategy can be regarded as the special cases of hybrid strategies by removing the technical details about BSs. Then, by using a similar procedure as in the analysis of the hybrid strategy, we obtain the following result:

Theorem 8. Under the ordinary ad hoc strategy, the multicast throughput for HEN is achieved of order

$$
\left\{ \begin{array}{l l} \Omega \Big (\frac {1}{\sqrt {n _ {d} n}} \Big) & \text {when} \quad n _ {d}: \Big [ 1, \frac {n}{(\log n) ^ {\alpha + 1}} \Big ], \\ \Omega \Big (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha + 1}{2}}} \Big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{(\log n) ^ {\alpha + 1}}, \frac {n}{(\log n) ^ {2}} \Big ], \\ \Omega \Big (\frac {1}{\sqrt {n n _ {d}} \cdot (\log n) ^ {\frac {\alpha - 1}{2}}} \Big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} \Big ], \\ \Omega \Big (\frac {1}{n _ {d} (\log n) ^ {\frac {\alpha}{2}}} \Big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{\log n}, n \Big ]. \end{array} \right.
$$

# 5.3 BS-Based Strategy for HEN

Under the classical BS-based strategy, sources deliver data to BSs directly during the uplink phase and BSs deliver received data to destinations directly during the downlink phase. Since in any time slot, all wireless links associate with the BSs, then the parallel transmission scheduling is disabled. Denote the BS-based strategy by $\Im _ { e } \Im _ { e }$ and denote the corresponding routing and transmission scheduling schemes by $\tilde { \Im } _ { e } ^ { r }$ and $\tilde { \Im } _ { e } ^ { t } ,$ respectively. Different from the previous partition method, here, we simply partition p $\mathcal { A } ( n )$ into m subregions of side length $\frac { \sqrt { n } } { \sqrt { m } }$ , and place one base station at the center of each subregion.

Routing scheme $\tilde { \mathbb { S } } _ { e } ^ { r } .$ . The routing consists of three phases: uplink phase $\tilde { \mathcal { \Im } } _ { e } ^ { r _ { 1 } }$ , BS-to-BS phase $\tilde { \Im } _ { e } ^ { r _ { 2 } } .$ , and downlink phase $\tilde { \mathbb { S } } _ { e } ^ { r _ { 3 } }$ . That is,

1. During the uplink phase, source nodes in subregion $S _ { \iota } , \iota = 1 , 2 , \ldots , m ,$ , transmit the packets to BS $b _ { \iota } .$ .   
2. The BS receiving the packets from source $v _ { k } ,$ $k = 1 , 2 , \dots , n _ { s } ,$ delivers the packets to those BSs that are placed in the subregions containing the destinations of $v _ { k }$ via BS-to-BS links.   
3. During downlink phase, each BS $b _ { \iota } , \ \iota = 1 , 2 , \ldots , m ,$ broadcasts the packets to the nodes in subregion $S _ { \iota }$

Transmission scheduling $\tilde { \mathfrak { I } } _ { e } ^ { t }$ . This transmission scheduling scheme includes three independent phases, denoted by $\tilde { \mathcal { { S } } } _ { e } ^ { t _ { 1 } } , \ \tilde { \mathcal { { S } } } _ { e } ^ { t _ { 2 } }$ , and $\tilde { \mathcal { I } } _ { e } ^ { t _ { 3 } }$ , corresponding to three routing phases. e Since the BS-to-BS phase is surely not the bottleneck, we only focus on the other two phases. That is,

1. During uplink phase $\tilde { \mathcal { I } } _ { e } ^ { t _ { 1 } }$ , all BSs $b _ { \iota } , \ \iota = 1 , 2 , \ldots , m ,$ receive simultaneously packets from the nodes in $S _ { \iota } .$   
2. During downlink phase $\tilde { \mathcal { \tilde { S } } } _ { e } ^ { t _ { 3 } }$ , all BSs $b _ { \iota } , \iota = 1 , 2 , \ldots , m ,$ deliver simultaneously packets to the nodes in $S _ { \iota }$ .

Lemma 21. Under the scheduling scheme $\tilde { \mathcal { \mathrm { I } } } _ { e } ^ { t } ,$ each subregion can sustain a total rate of order $\Omega ( ( n / m ) ^ { - \frac { \alpha } { 2 } } )$ during both the downlink phase and uplink phase.

Proof. Due to the regular location of BSs, for any receiver in a subregion, the nearest transmitter outside the subregion is faraway in distance of at least $\frac { { \sqrt { n } } } { 2 { \sqrt { m } } }$ . Similar to Lemma 9, the sum of interferences to the receivers is bounded by

$$
I (n) \leq \sum_ {i = 1} ^ {m} 8 i P \ell \left(\frac {2 i - 1}{2} \cdot \frac {\sqrt {n}}{\sqrt {m}}\right) \leq \left(\frac {m}{n}\right) ^ {\frac {\alpha}{2}} \cdot 2 ^ {\alpha} P \sum_ {i = 1} ^ {\infty} \frac {8 i}{(2 i - 1) ^ {\alpha}}.
$$

Thus, $I ( n ) = O ( ( n / m ) ^ { - { \frac { \alpha } { 2 } } } )$ . While, the signal $S ( n )$ can be bounded by

$$
S (n) \geq P \cdot \left(\frac {\sqrt {n}}{\sqrt {2 m}}\right) ^ {- \alpha} \geq \left(\frac {\sqrt {1 0}}{2}\right) ^ {- \alpha} \cdot P \cdot \left(\frac {n}{m}\right) ^ {- \frac {\alpha}{2}}.
$$

Then, $S ( n ) = \Omega ( ( n / m ) ^ { - \frac { \alpha } { 2 } } )$ . For the assumption $m = O ( n )$ , we have $I ( n ) = { \cal { O } } ( 1 )$ and $S ( n ) = O ( 1 )$ . Hence, we have $\frac { S ( n ) } { N _ { 0 } + I ( n ) } = O ( 1 )$ SðnÞ and

$$
\log \left(1 + \frac {S (n)}{N _ {0} + I (n)}\right) = \Omega ((n / m) ^ {- \frac {\alpha}{2}}),
$$

which completes the proof.

![](images/96f7d33ca0e399d48d960833a2181be41ccf1ae6fdc0fe54e40fc9d1bb93689e.jpg)

Next, we consider the load of BSs during the downlink and uplink phases. Similar to Lemma 11, we have,

Lemma 22. Under the strategy $\tilde { \Im } _ { e } ^ { r } ,$ , the load of each BS is of order $\tilde { L } _ { e } ^ { r } = \bar { L } _ { e } ^ { r _ { b } }$ , where $\bar { L } _ { e } ^ { r _ { b } }$ is defined in Lemma 11.

According to Lemmas 21 and 16, we have

Theorem 9. By the BS-based strategy, the per-session multicast throughput for HEN can be achieved of order

$$
\left\{ \begin{array}{l l} \Omega \Big (\frac {1}{\log m} \cdot \big (\frac {n}{m} \big) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: \big [ 1, \frac {m \log m}{n} \big ], \\ \Omega \Big (\frac {m}{n \cdot n _ {d}} \cdot \big (\frac {n}{m} \big) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: \big [ \frac {m \log m}{n}, m \big ], \\ \Omega \Big (\frac {1}{n} \cdot \big (\frac {n}{m} \big) ^ {- \frac {\alpha}{2}} \Big) & \text {when} \quad n _ {d}: [ m, n ]. \end{array} \right.
$$

# 5.4 Integration of Three Types of Strategies

To achieve the optimal multicast throughput, we will select the best strategy according to different scenarios in terms of m and $n _ { d } .$ Combining Theorems 7, 8, and 9, we can obtain the main result in Theorem 1.

# 6 MULTICAST STRATEGIES FOR HDN

In this section, we consider the hybrid dense network. Corresponding to the hybrid extended network, we also design the hybrid strategy, the BS-based strategy, and the ordinary ad hoc strategy.

# 6.1 Hybrid Strategy for HDN

As in HEN, the hybrid strategy for HDN also consists of connectivity strategy, denoted by $\bar { \Im _ { d } } ,$ , and percolation strategy, denoted by ${ \mathfrak { P } } _ { d } .$ The strategy $\bar { \mathfrak { I } } _ { d }$ can be applied only when $\rho = O ( n / \log n ) ;$ ; the strategy $\Im _ { d }$ can be used when $\rho = O ( n / ( \log n ) ^ { 2 } )$ .

# 6.1.1 Connectivity Strategy $\bar { \mathcal { \Sigma } } _ { d }$

Under the strategy $\bar { \Im _ { d } } ,$ , the routing $\bar { \Im } _ { d } ^ { r }$ is built based on the connectivity paths. We construct the connectivity paths based on the scheme lattice $\mathbb { L } ( 1 , \sqrt { \bar { a } _ { e } / n } , 0 )$ . In each column or row of $\mathbb { L } ( 1 , \sqrt { \bar { a } _ { e } / n } , 0 )$ , we can also construct $\Theta ( \log n )$ connectivity paths as the case in HEN. However, unlike in HEN, the parallel transmission scheduling does not work in HDN, which can be explained in the following lemma:

Lemma 23. The total rate of each connectivity path can be achieved of order $\Theta ( 1 / \pi ( n ) )$ when $\pi ( n )$ connectivity paths are simultaneously scheduled, where $\pi ( n ) = O ( \log n )$ .

Proof. For any link in any time slot, since the length of the link is at least $\begin{array} { r } { \frac { 1 } { 2 } \sqrt { \bar { a } _ { e } / n } } \end{array}$ , we obtain that the sum of interferences to the receivers is bounded by

$$
\begin{array}{l} I (n) \leq P \cdot (\pi (n) - 1) \cdot \ell \left(\frac {1}{2} \sqrt {\bar {a} _ {e} / n}\right) \\ + \sum_ {i = 1} ^ {n} 8 i \cdot \pi (n) \cdot P \cdot \ell \left(\frac {3 i - 2}{2} \sqrt {\bar {a} _ {e} / n}\right) \\ \leq P \cdot \left(\frac {2}{\theta}\right) ^ {\frac {\alpha}{2}} \cdot \pi (n) \cdot \left(\frac {n}{\log n}\right) ^ {\frac {\alpha}{2}} \Bigg (1 + \lim _ {n \to \infty} \sum_ {i = 1} ^ {n} \frac {8 i}{(3 i - 2) ^ {\alpha}} \Bigg). \\ \end{array}
$$

The last limitation obviously converges when $\alpha > 2 ,$ , thus $\begin{array} { r } { I _ { n } = O ( \pi ( n ) \cdot ( \frac { n } { \log n } ) ^ { \frac { \alpha } { 2 } } ) } \end{array}$ . Since the length of every hop is at most $\begin{array} { r l r } { \frac { 1 } { 2 } \sqrt { 1 3 \bar { a } _ { e } / n } } & { { } } & { } \end{array}$ we have the signal $S ( n )$ at the receiver can be bounded by $\begin{array} { r } { S ( n ) \geq ( \frac { 1 3 } { 2 } \cdot \theta ) ^ { - \frac { \alpha } { 2 } } \cdot P \cdot ( \frac { n } { \log n } ) ^ { \frac { \alpha } { 2 } } . \mathrm { B y } N _ { 0 } \geq 0 , } \end{array}$ , we have $\begin{array} { r } { \frac { S ( n ) } { N _ { 0 } + I ( n ) } = { O } ( \frac { 1 } { \pi ( n ) } ) } \end{array}$ , which completes the proof. tu

According to Lemma 23, we construct only one connectivity path in each column or row. Then, by a similar procedure to HEN, we can get the following results:

Theorem 10. When $\rho = O ( n / \log n )$ , under the strategy $\bar { \mathfrak { I } } _ { d } ,$ without taking the bottlenecks on BSs into account, the persession multicast throughput for HDN is achieved of order

$$
\bar {\Lambda} _ {d} ^ {\bar {r} _ {b}} = \left\{ \begin{array}{l l} \left(\frac {\sqrt {\rho}}{n _ {d} \sqrt {n \log n}}\right) & \text {when} \quad n _ {d}: [ 1, \rho ], \\ \Omega \left(\frac {1}{\sqrt {n n _ {d} \log n}}\right) & \text {when} \quad n _ {d}: [ \rho , n / \log n ], \\ \Omega \left(\frac {1}{n}\right) & \text {when} \quad n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

Lemma 24. The maximum load on the links between BSs and ordinary ad hoc nodes is of order

$$
\bar {L} _ {d} ^ {r _ {b}} = \left\{ \begin{array}{l l} O (n \cdot n _ {d} / \rho) & \text { when } \quad n _ {d}: [ 1, \rho ], \\ O (n) & \text { when } \quad n _ {d}: [ \rho , n ]. \end{array} \right.
$$

On the other hand, similar to Lemma 9, we can prove that the capacity of the links between BSs and ordinary ad hoc nodes (B-O links) is of order $\Omega ( 1 )$ . Thus,

Lemma 25. Under the strategy $\bar { \Im _ { d } } ,$ the throughput along the wireless links via BSs can be achieved of order

$$
\bar {\Lambda} _ {d} ^ {r _ {b}} = \left\{ \begin{array}{l l} \Omega \Big (\frac {\rho}{n \cdot n _ {d}} \Big) & \text {when} \quad n _ {d}: [ 1, \rho ], \\ \Omega \big (\frac {1}{n} \big) & \text {when} \quad n _ {d}: [ \rho , n ]. \end{array} \right.
$$

Combining Theorem 10 and Lemma 25, we conclude that the bottleneck of the whole routing $\bar { \mathfrak { I } } _ { d } ^ { r }$ lies on the B-O links. According to Lemma $^ { 7 , }$ we obtain the multicast throughput derived by the connectivity strategy.

Theorem 11. Under the connectivity strategy $\bar { \Im _ { d } } ,$ the persession multicast throughput for HDN is achieved of order:

When $m : [ 1 , n / \log n ] .$ ,

$$
\bar {\Lambda} _ {d} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {m}{n \cdot n _ {d}} \Big) & \text { when } \quad n _ {d}: [ 1, m ], \\ \Omega \big (\frac {1}{n} \big) & \text { when } \quad n _ {d}: [ m, n ]. \end{array} \right.
$$

When $m : [ n / \log n , n ] ,$ ,

$$
\bar {\Lambda} _ {d} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {1}{n _ {d} \log n} \Big) & \text {when} \quad n _ {d}: [ 1, n / \log n ], \\ \Omega (\frac {1}{n}) & \text {when} \quad n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

# 6.1.2 Percolation Strategy $\Im _ { d }$

We design the percolation strategy, denoted by ${ \mathfrak { F } } _ { d } ,$ based on the connectivity paths and highways. We build the highways based on the scheme lattice $\bar { \bf L } ( 1 , \bar { \sqrt { a _ { e } / n } } , { \frac { \pi } { 4 } } )$ in which the cells are called percolation cells.

The average number of nodes in each percolation cell is also the same, namely $a _ { e } .$ . Therefore, all the percolation results above still hold for HDN, and we can find as many highways as in HEN. By a similar procedure to HEN, we can obtain the following results:

Lemma 26. Along the highways, the multicast throughput can be achieved of order

$$
\Lambda_ {d} ^ {r _ {1}} = \left\{ \begin{array}{l l} \Omega \Big (\frac {\sqrt {\rho}}{n _ {d} \sqrt {n}} \Big) & \text {when} n _ {d}: [ 1, \rho ], \\ \Omega \Big (\frac {1}{\sqrt {n n _ {d}}} \Big) & \text {when} n _ {d}: [ \rho , n / (\log n) ^ {2} ], \\ \Omega \Big (\frac {1}{n _ {d} \log n} \Big) & \text {when} n _ {d}: [ n / (\log n) ^ {2}, n / \log n ], \\ \Omega (1 / n) & \text {when} n _ {d}: [ n / \log n, n ]. \end{array} \right.
$$

Lemma 27. Along the connectivity paths, the multicast throughput can be achieved of order $\begin{array} { r } { \dot { \Lambda } _ { d } ^ { r _ { 2 } } = \Omega ( \frac { 1 } { n _ { d } } \cdot ( \log n ) ^ { - \frac { 3 } { 2 } } ) } \end{array}$ .

Based on Lemmas 26 and $^ { 2 7 , }$ and according to Lemma $^ { 7 , }$ we can obtain Theorem 12.

Theorem 12. When $\rho = O ( n / ( \log n ) ^ { 2 } )$ , by the percolation strategy $\Im _ { d }$ without taking the bottlenecks on BSs into account, the per-session multicast throughput for HDN can be achieved of order:

When $\rho : [ 1 , ( n / ( \log n ) ^ { 3 } ) ] ,$ ,

$$
\Lambda_ {d} ^ {\bar {r} _ {b}} = \left\{ \begin{array}{l l} \Omega \Big (\frac {\sqrt {\rho}}{n _ {d} \sqrt {n}} \Big) & \text {when} n _ {d}: [ 1, \rho ], \\ \Omega \Big (\frac {1}{\sqrt {n n _ {d}}} \Big) & \text {when} n _ {d}: \Big [ \rho , \frac {n}{(\log n) ^ {3}} \Big ], \\ \Omega \Big (\frac {1}{n _ {d} \cdot (\log n) ^ {\frac {3}{2}}} \Big) & \text {when} n _ {d}: \Big [ \frac {n}{(\log n) ^ {3}}, n \Big ]. \end{array} \right.
$$

When $\begin{array} { r } { \rho : [ \frac { n } { ( \log n ) ^ { 3 } } , \frac { n } { ( \log n ) ^ { 2 } } ] , \Lambda _ { d } ^ { \bar { r } _ { b } } = \Omega ( \frac { 1 } { n _ { d } } \cdot ( \log n ) ^ { - \frac { 3 } { 2 } } ) . } \end{array}$

Combining Theorem 12 and Lemma 25, we have the following result:

Theorem 13. Under the percolation strategy $\Im _ { d } ,$ , the persession multicast throughput for HDN is achieved of order:

When $m : [ 1 , n \cdot ( \log n ) ^ { - { \frac { 3 } { 2 } } } ] ,$

$$
\Lambda_ {d} ^ {r} = \left\{ \begin{array}{l l} \Omega \Big (\frac {m}{n \cdot n _ {d}} \Big) & \text {when} \quad n _ {d}: [ 1, m ], \\ \Omega \big (\frac {1}{n} \big) & \text {when} \quad n _ {d}: \big [ m, n \cdot (\log n) ^ {- \frac {3}{2}} \big ], \\ \Omega \Big (\frac {1}{n _ {d}} (\log n) ^ {- \frac {3}{2}} \Big) & \text {when} \quad n _ {d}: [ n \cdot (\log n) ^ {- \frac {3}{2}}, n ]. \end{array} \right.
$$

$W h e n ~ m : [ n \cdot ( \log n ) ^ { - 3 / 2 } , n ] , ~ \Lambda _ { d } ^ { r } = \Omega ( \textstyle { \frac { 1 } { n _ { d } } } \cdot { \bigl ( } \log n { \bigr ) } ^ { - \frac { 3 } { 2 } } ) .$

Furthermore, combining Theorems 11 and 13, we can get the multicast throughput derived by the hybrid strategy.

Theorem 14. By using the hybrid strategy, the multicast throughput for HEN is achieved of order $\bar { \Lambda } _ { d } ^ { r }$ that is defined in Theorem 11.

# 6.2 Ordinary Ad Hoc Strategy for HDN

In this case, we treat the network as an ordinary random dense network. According to the results in [3], we have

Theorem 15. The achievable per-session multicast throughput for random dense networks is of order

$$
\left\{ \begin{array}{l l} \Omega \Big (\frac {1}{\sqrt {n _ {d} n}} \Big) & \text {when} \quad n _ {d}: \Big [ 1, \frac {n}{(\log n) ^ {3}} \Big ], \\ \Omega \Big (\frac {1}{n _ {d} (\log n) ^ {\frac {3}{2}}} \Big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{(\log n) ^ {3}}, \frac {n}{(\log n) ^ {2}} \Big ], \\ \Omega \Big (\frac {1}{\sqrt {n n _ {d} \log n}} \Big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{(\log n) ^ {2}}, \frac {n}{\log n} \Big ], \\ \Omega \big (\frac {1}{n} \big) & \text {when} \quad n _ {d}: \Big [ \frac {n}{\log n}, n \Big ]. \end{array} \right.
$$

# 6.3 BS-Based Strategy for HDN

The BS-based strategy for HDN is similar to that for HEN described in Section 5.3. By a similar procedure, we can prove the following theorem:

Theorem 16. Under the strategy $\tilde { \Im _ { d } } ,$ the achievable multicast throughput for HDN is of order

$$
\bar {\Lambda} _ {d} = \left\{ \begin{array}{l l} O (1 / \log n) & \text {when} \quad n _ {d}: \big [ 1, \frac {m \cdot \log n}{n} \big ], \\ O \Big (\frac {m}{n \cdot n _ {d}} \Big) & \text {when} \quad n _ {d}: \big [ \frac {m \cdot \log n}{n}, m \big ], \\ O (1 / n) & \text {when} \quad n _ {d}: [ m, n ]. \end{array} \right.
$$

# 6.4 Integration of Three Types of Strategies

To achieve the optimal multicast throughput, we can select the best strategy according to the different scenarios in terms of m and $n _ { d } .$ . Combining Theorems 14, 13, and 16, we can obtain Theorem 2 as one of main results.

# 7 LITERATURE REVIEWS

We review the existing works on the capacity scaling laws of wireless ad hoc networks and hybrid networks under two popular communication models.

# 7.1 Wireless Ad Hoc Networks

# 7.1.1 Under Threshold-Based Channel Model

Gupta and Kumar [2] studied the unicast capacity in dense networks, they showed that a scheme of nearest neighbor communication can achieve a throughput of $\Theta ( 1 / { \sqrt { n \log n } } )$ . Keshavarz-Haddad et al. [20] studied the broadcast capacity of an arbitrary network, and showed that the per-session broadcast capacity is only of $\Theta ( 1 / n )$ . Shakkottai et al. [21] designed a novel routing scheme, called comb scheme, by which the per-session multicast throughput can be achieved of order $\Omega ( \textstyle { \frac { 1 } { \sqrt { n n _ { d } } } } )$ . Li [8] showed that, assuming that $n _ { s } = \Omega ( \log n _ { d } \sqrt { n \log n / n _ { d } } )$ , for random networks, the persession capacity of $n _ { s }$ multicast sessions is $\Theta ( 1 / \sqrt { n _ { d } n \log n } )$ when $n _ { d } = O ( n / \log n )$ , and is $\Theta ( 1 / n )$ when $n _ { d } = \Omega ( n / \log n )$ .

# 7.1.2 Under Gaussian Channel Model

Franceschetti et al. [10] showed that the throughput for both random extended networks and random dense networks can be achieved of order $\Omega ( 1 / \sqrt { n } )$ . Zheng [22] proved that the broadcast capacity for random extended networks is of order $\Theta ( \textstyle { \frac { 1 } { n } } ( \log n ) ^ { - \frac { \alpha } { 2 } } )$ . Li et al. [4] showed that, when $\begin{array} { r } { n _ { d } = O ( \frac { n } { ( \log n ) ^ { 2 \alpha + 6 } } ) } \end{array}$ ð ðlog nÞ 2-þ6Þ and exten $n _ { s } = \Omega ( n ^ { \frac { 1 } { 2 } + \theta } )$ , the multicast throughcan be achieved of order random, where $\begin{array} { r } { \Omega ( \frac { \sqrt { n } } { n _ { s } \sqrt { n _ { d } } } ) . } \end{array}$ $\theta > 0$ is a constant. In [3], such threshold of $n _ { d }$ was improved to $\begin{array} { r } { n _ { d } = O ( \frac { n } { ( \log n ) ^ { \alpha + 1 } } ) } \end{array}$ ð nðlog nÞ-þ1Þ, and the corresponding upper bounds were proposed. Keshavarz-Haddad and Riedi [23] proposed a technique called arena to study upper bounds of capacity. They [24] devised a scheme and computed the achievable throughput for random dense networks.

# 7.2 Hybrid Wireless Networks

# 7.2.1 Under Threshold-Based Channel Model

Earlier, Liu et al. [25] introduced the model based on the dense network in which the base stations are regularly placed and the ad hoc nodes are randomly distributed. The case that both base stations and ad hoc nodes are randomly placed in the dense network was studied by Kozat and Tassiulas in [26]. Agarwal and Kumar [5] considered the unicast capacity for hybrid networks under PhIM. Recently, Mao et al. [9] studied the multicast capacity for hybrid networks under threshold-based channel model by assuming $m = O ( n / \log n )$ .

# 7.2.2 Under Gaussian Channel Model

Agarwal and Kumar [5] studied the unicast capacity for hybrid dense networks, and they designed the same bounds as that under the threshold-based model. Liu et al. [11] studied the achievable unicast throughput for hybrid extended networks. They showed that in a two-dimensional square hybrid wireless network with n ordinary ad hoc nodes and m base stations, it is necessary that $m = \Omega ( { \sqrt { n } } )$ in order to obtain a linear gain of capacity. Focusing on hybrid dense networks, Wang et al. [27] derived the achievable multicast throughput under the schemes without introducing the percolation-based routing [10], which leads to poor multicast throughput for some cases in terms of $n _ { d }$ and m.

# 8 CONCLUSION

We study the multicast throughput for hybrid extended networks and hybrid dense networks under Gaussian Channel model. Three types of multicast strategies are devised. Based on the multicast throughputs derived by all strategies, we make the decisions on selecting the optimal strategy according to different scenarios in terms of m, n, and $n _ { d } .$ . To the best of our knowledge, this paper is the first work that addresses the multicast routing and scheduling strategy in hybrid wireless networks under Gaussian Channel model. A number of interesting questions remain open: How to derive tight upper bound on the network capacity for hybrid wireless networks? What type of strategy should be implemented if the access links between ordinary ad hoc nodes and base stations are different from those among ordinary ad hoc nodes, e.g., they may have larger bandwidth, or if the links among base stations are not wired and their bandwidth are not arbitrary large?

# ACKNOWLEDGMENTS

The authors would like to thank the anonymous reviewers for their constructive comments. This research was partially supported by the National Basic Research Program of China (973 Program) under grants No. 2010CB328101, No. 2010CB334707, and No. 2009CB3020402, the Program for Changjiang Scholars and Innovative Research Team in the University, the Shanghai Key Basic Research Project under grant No. 10DJ1400300, the Expo Science and Technology Specific Projects of China under grant No. 2009BAK43B37, the US National Science Foundation under grant NSF CNS-0832120, the National Natural Science Foundation of China under grants No. 60828003 and No. 61003277, the Program for Zhejiang Provincial Key Innovative Research Team, and the Program for Zhejiang Provincial Overseas High-Level Talents. The preliminary result [1] was published at IEEE ICDCS 2009.

# REFERENCES

[1] C. Wang, S. Tang, X.-Y. Li, C. Jiang, and Y. Liu, “Multicast Throughput of Hybrid Wireless Networks under Gaussian Channel Model,” Proc. IEEE Int’l Conf. Distributed Computing Systems (ICDCS ’09), 2009.   
[2] P. Gupta and P.R. Kumar, “The Capacity of Wireless Networks,” IEEE Trans. Information Theory, vol. 46, no. 2, pp. 388-404, Mar. 2000.   
[3] C. Wang, X.-Y. Li, C. Jiang, S. Tang, and Y. Liu, “Scaling Laws on Multicast Capacity of Large Scale Wireless Networks,” Proc. IEEE INFOCOM, 2009.   
[4] S. Li, Y. Liu, and X.-Y. Li, “Capacity of Large Scale Wireless Networks under Gaussian Channel Model,” Proc. ACM MobiCom, 2008.   
[5] A. Agarwal and P.R. Kumar, “Capacity Bounds for Ad Hoc and Hybrid Wireless Networks,” ACM SIGCOMM Computer Comm. Rev., vol. 34, no. 3, pp. 71-83, 2004.   
[6] S. Toumpis and A.J. Goldsmith, “Capacity Regions for Wireless Ad Hoc Networks,” IEEE Trans. Wireless Comm., vol. 2, no. 4, pp. 736-748, July 2003.   
[7] T.M. Cover and J.A. Thomas, Elements of Information Theory. Wiley, 1991.   
[8] X.-Y. Li, “Multicast Capacity of Wireless Ad Hoc Networks,” IEEE/ACM Trans. Networking, vol. 17, no. 3, pp. 950-961, June 2009.   
[9] X. Mao, X.-Y. Li, and S. Tang, “Multicast Capacity for Hybrid Wireless Networks,” Proc. ACM MobiHoc, 2008.   
[10] M. Franceschetti, O. Dousse, D. Tse, and P. Thiran, “Closing the Gap in the Capacity of Wireless Networks via Percolation Theory,” IEEE Trans. Information Theory, vol. 53, no. 3, pp. 1009- 1018, Mar. 2007.   
[11] B. Liu, P. Thiran, and D. Towsley, “Capacity of a Wireless Ad Hoc Network with Infrastructure,” Proc. ACM MobiHoc, 2007.   
[12] M. Grossglauser and D. Tse, “Mobility Increases the Capacity of Ad Hoc Wireless Networks,” IEEE/ACM Trans. Networking, vol. 10, no. 4, pp. 477-486, Aug. 2002.   
[13] A. O¨ zgu¨ r, O. Le´v^eque, and D. Tse, “Hierarchical Cooperation Achieves Optimal Capacity Scaling in Ad Hoc Networks,” IEEE Trans. Information Theory, vol. 53, no. 10, pp. 3549-3572, Oct. 2007.   
[14] L. Xie and P. Kumar, “A Network Information Theory for Wireless Communication: Scaling Laws and Optimal Operation,” IEEE Trans. Information Theory, vol. 50, no. 5, pp. 748-767, May 2004.   
[15] V. Vapnik and A. Chervonenkis, “On the Uniform Convergence of Relative Frequencies of Events to Their Probabilities,” Theory of Probability and Its Applications, vol. 16, no. 2, pp. 264-280, 1971.   
[16] M. Mitzenmacher and E. Upfal, Probability and Computing: Randomized Algorithms and Probabilistic Analysis. Cambridge Univ., 2005.

[17] W. Feller, An Introduction to Probability Theory and Its Applications, vol. 1, John Wiley and Sons, 1968.   
[18] V. Kolchin, B. Sevast’yanov, and V.P. Chistyakov, Random Allocations. Winston and Sons, 1978.   
[19] O. Dousse, M. Franceschetti, N. Macris, R. Meester, and P. Thiran, “Percolation in the Signal to Interference Ratio Graph,” J. Applied Probability, vol. 43, no. 2, pp. 552-562, 2006.   
[20] A. Keshavarz-Haddad, V. Ribeiro, and R. Riedi, “Broadcast Capacity in Multihop Wireless Networks,” Proc. ACM MobiCom, 2006.   
[21] X. Shakkottai, S. Liu, and R. Srikant, “The Multicast Capacity of Large Multihop Wireless Networks,” Proc. ACM MobiHoc, 2007.   
[22] R. Zheng, “Asymptotic Bounds of Information Dissemination in Power-Constrained Wireless Networks,” IEEE Trans. Wireless Comm., vol. 7, no. 1, pp. 251-259, Jan. 2008.   
[23] A. Keshavarz-Haddad and R. Riedi, “Bounds for the Capacity of Wireless Multihop Networks Imposed by Topology and Demand,” Proc. ACM MobiHoc, 2007.   
[24] A. Keshavarz-Haddad and R. Riedi, “Multicast Capacity of Large Homogeneous Multihop Wireless Networks,” Proc. IEEE Sixth Int’l Symp. Modeling and Optimization in Mobile, Ad Hoc, and Wireless Networks and Workshops (WiOpt ’08), 2008.   
[25] B. Liu, Z. Liu, and D. Towsley, “On the Capacity of Hybrid Wireless Networks,” Proc. IEEE INFOCOM, 2003.   
[26] U.C. Kozat and L. Tassiulas, “Throughput Capacity of Random Ad Hoc Networks with Infrastructure Support,” Proc. ACM MobiHoc, 2003.   
[27] C. Wang, C. Jiang, X.-Y. Li, and G. Dai, “Achievable Throughput for Hybrid Wireless Networks under Gaussian Channel Model,” Proc. IEEE Int’l Conf. Comm. (ICC ’09), 2009.

![](images/9fa3415c18bd407ef0b0a1de04eff6686ae0344c148edf349b80b6d1e4d2be70.jpg)



Cheng Wang received the BS degree from the Department of Mathematics and Physics at Shandong University of Technology in 2002, and the MS degree from the Department of Applied Mathematics at Tongji University in 2006. He is currently a PhD student in the Department of Computer Science at Tongji University. His research interests include wireless communications and networking, network coding, and distributed computing. He is a student member of the IEEE.

![](images/583e847f017221ccc8ec700beddf2bfd733b8c1979d97166e462c959283446a9.jpg)



Xiang-Yang Li received the bachelor’s degree from the Department of Computer Science and the bachelor’s degree from the Department of Business Management from Tsinghua University, China, both in 1995, and the MS and PhD degrees from the Department of Computer Science in the University of Illinois at Urbana-Champaign in 2000 and 2001, respectively. He has been an associate professor (since 2006) and an assistant professor (from 2000 to 2006) of computer science at the Illinois Institute of Technology. His research interests include wireless ad hoc and sensor networks, game theory, computational geometry, and cryptography and network security. He served as a cochair of the ACM FOWANC 2008 workshop, a cochair of the AAIM 2007 conference, a program committee cochair of WTASA 2007, and program committee member of a number of conferences such as ACM MobiCom, ACM MobiHoc, IEEE INFOCOM, and IEEE ICDCS. He has served as an editor of the IEEE Transactions on Parallel and Distributed Systems (TPDS) since 2010, as an editor of Networks: An International Journal since 2009, and on the Advisory Board of Ad Hoc & Sensor Wireless Networks: An International Journal since 2005. He was a guest editor of special issues of ACM Mobile Networks and Applications, the IEEE Journal on Selected Areas in Communications, and several other journals. He published a monograph, “Wireless Ad Hoc and Sensor Networks: Theory and Applications” (June 2008, Cambridge University Press). He also coedited the Encyclopedia of Algorithms (Springer) as the area editor for mobile computing. He is a senior member of the IEEE.

![](images/36658679da41ccf744787db1b17903cb9e1adf821b241875e250986784625245.jpg)



Changjun Jiang received the PhD degree from the Institute of Automation, Chinese Academy of Sciences, Beijing, China, in 1995 and conducted postdoctoral research at the Institute of Computing Technology, Chinese Academy of Sciences, in 1997. Currently, he is a professor with the Department of Computer Science and Engineering, Tongji University, Shanghai. He is also a council member of the China Automation Federation and the Artificial Intelligence Federation, the vice director of the Professional Committee of Petri Net of the China Computer Federation, the vice director of the Professional Committee of Management Systems of the China Automation Federation, and an Information Area Specialist of the Shanghai Municipal Government. His current areas of research are concurrent theory, Petri nets, and formal verification of software, concurrency processing, and intelligent transportation systems. He is a member of the IEEE.

![](images/2a664fcb8265e803e3c6970c9488b9086572841221068521ed46515bc75c9cda.jpg)



Shaojie Tang received the BS degree in radio engineering from Southeast University, China, in 2006 and has been a PhD student of the Computer Science Department at the Illinois Institute of Technology since 2006. His current research interests include algorithm design and analysis for wireless ad hoc networks, wireless sensor networks, and online social networks. He is a student member of the IEEE.

![](images/74848500d52d5bcd37346851a2c95f281ae6c6f746afeb8ad0e08d492209727b.jpg)



Yunhao Liu received the BS degree from the Automation Department at Tsinghua University, China, in 1995, the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is a member of the Tsinghua National Lab for Information Science and Technology and the director of the Tsinghua National MOE Key Lab for Informa-

tion Security. He is also on the faculty of the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He is a senior member of the IEEE and an ACM distinguished speaker.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.