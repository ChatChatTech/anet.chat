# Malicious Link Detection in Multi-Hop Wireless Sensor Networks

Yuan Liang∗ Yunhao Liu† Jian Ren∗ Tongtong Li∗

∗Department of Electrical & Computer Engineering, Michigan State University

†Department of Computer Science & Engineering, Michigan State University

Email: liangy11@msu.edu, yunhao@cse.msu.edu, {renjian, tongli}@egr.msu.edu

Abstract—This paper considers malicious link detection in multi-hop wireless sensor networks (WSNs). Existing work on malicious link detection generally requires that the detection process being performed at the intermediate nodes, leading to considerable overhead in system design, as well as unstable detection accuracy due to limited resources and the uncertainty in the loyalty of the intermediate nodes themselves. In this paper, we propose an efficient and robust malicious link detection scheme by exploiting the statistics of packet delivery rates only at the base station. More specifically, first, we present a secure packet transmission protocol to ensure that except the base station, any intermediate nodes on the route cannot access the contents and routing paths of the packets. Second, we design a malicious link detection algorithm that can effectively detect the irregular dropout at every hop (or link) along the routing path. We prove that the proposed algorithm has guaranteed false alarm rate and low miss detection rate. Simulation results are provided to validate the proposed approaches.

# I. INTRODUCTION

Wireless sensor networks (WSNs) are often multi-hop networks where individual sensor nodes need to function as relays to forward the data flow originated from their peers to the sink. Such a distributed network organization makes WSNs especially vulnerable to various attacks, such as wireless jamming, spoofing attacks and internal attacks [1], in a sense that one malicious link or node in the network can compromise the data flow passing through it from multiple nodes. In this paper, we consider the detection of malicious links in WSNs.

The detection of malicious behaviors in WSNs, or more generally, the multi-hop wireless networks, has been broadly discussed in literature. In [2], [3], audit based schemes were proposed for malicious node identification. In [4], the security of disruption tolerant networks (DTN) was studied. In [5], an heuristic method was proposed to identify the failed nodes by re-organizing the network topology. In [6], a 2ACK scheme was proposed to detect the nodes that intentionally drop packets. In [7], the blackhole and grayhole attacks were investigated. In [8], the malicious node detection was explained under the context of network coding. Making use of the open medium in wireless communications, an overhearing scheme was proposed to monitor the behaviors of the neighboring nodes in [9].

A major limitation with most existing methods on malicious behavior detection is that the nodes are required to implement additional verification process in packet delivery, or report additional information to the authority in the network, leading to considerable overhead on complexity, energy consumption and throughput. In this paper, as an effort to improve the efficiency and minimize the system complexity, we propose a malicious link detection algorithm by exploiting the statistics of packet delivery rates at the base station. More specifically, first, we present a secure packet transmission protocol to ensure that except the base station, any intermediate nodes on the route cannot access the contents and routing paths of the packets. Second, we design a malicious link detection algorithm that can effectively detect the irregular dropout at every hop (or link) along the routing path with guaranteed false alarm rate and miss detection rate. Comparing to [10] which can detect whether a routing path is problematic, our detection method can be localized to every link. It should be pointed out that, illegal packet modification and injection of invalid packets, which essentially result in the dropout of legal packets, can be detected successfully as well. Simulation results are provided to validate the proposed approaches.

# II. NETWORK MODEL

In this paper, we consider a single unit of a multi-hop WSN. The unit is governed by an authority, the sink or the base station (BS), which is responsible for collecting data from the nodes in the unit, and issuing control messages. Each node can be either a regular sensor or the aggregator of several sensors. In this paper, we model the WSN unit using the Nhop framework [11], as shown in Fig. 1, where the nodes are sorted basing on the hop distance from each node to the BS. The nodes on layer i are the set of nodes i hops away from the BS; each node at layer i + 1 forwards the packets it generates and receives from higher layers to one or several nodes at layer i until the BS (layer 0). The proposed scheme can be readily scalable to WSNs with multiple BSs.

In a WSN, the major data flow is from the sensors to the base station, i.e., the uplink. Therefore, in this paper, we focus on the uplink data flow of the WSN. Since we consider an environment where the reliability of the links cannot be guaranteed, we employ multi-path routing [12] in the network, to enhance the diversity and robustness of routing. For each packet to be delivered to the BS, a node randomly selects one of the candidate nodes in the lower layer as the next hop with certain probability according to the routing table; the routing table is determined by the BS and assigned to each node through the control message. The topology and the routing table of the network can be determined either statically or dynamically. In the static case, the topology and routing paths are essentially fixed during network operation. In the dynamic case, the routing table can be determined by utilizing the ad-hoc on-demand distance vector (AODV) routing [13] protocol, where the BS sorts the route request (RREQ) messages and selects the next hops accordingly for each node in the unit. Since the major focus of this paper is on malicious link detection process, in the following, we assume that the routing table has been established and fixed during detection.

![](images/08d149c73f649af98ff559f0cb585fea98a05d98668ff7bd99beb47657579a33.jpg)



Fig. 1: Hierarchical structure of a WSN.

![](images/a3b1e52925c31f0b5f2f1659217f48dda13135929cdfa556faaf1edc068fc6c1.jpg)



Fig. 2: The packet encoding process at intermediate node.

The malicious behaviors considered in this paper include (i) irregular dropout of packets, (ii) illegal modification of packets, and (iii) injection of invalid packets. The reasons for the malicious behaviors may be the degradation of wireless channels, attacks from external jammers or corrupted internal nodes, etc. Note that the above malicious behaviors committed by an internal node can be equivalently converted to those happen on its incidental links; therefore, without loss of generality we focus on malicious link detection. A node can be considered as malicious if a certain amount of its incidental links are identified as malicious. We will further show in Section III that the detection of packet modification and packet injection can both be converted to that of packet dropout.

Notations: We let $N _ { i }$ denote the number of node of layer i. Following the notation in graph theory, the nodes of layer i are denoted by $v _ { i , 0 } , v _ { i , 1 } , . . . , v _ { i , N _ { i } - 1 }$ , and $v _ { 0 , 0 }$ denotes the BS; $e _ { i , j _ { 1 } , j _ { 2 } }$ denotes the link/edge $v _ { i , j _ { 1 } } \  \ v _ { i - 1 , j _ { 2 } } . \ G _ { i , j }$ denotes the self generated packet rate of node $v _ { i , j } , \ p _ { d } ( i , j _ { 1 } , j _ { 2 } )$ the dropout rate of link $e _ { i , j _ { 1 } , j _ { 2 } } , p _ { t } ( i , j _ { 1 } , j _ { 2 } )$ the probability that $v _ { i , j _ { 1 } }$ selects $v _ { i - 1 , j _ { 2 } }$ as its next hop in the multi-path routing. $\mathbb { F } _ { q } ^ { n }$ denotes the Galois Field $( q ^ { n } )$ . We use bold capital letters, e.g., X, to denote random vectors, and bold lower case letters, e.g., x, to denote their values.

# III. PACKET TRANSMISSION PROTOCOL

In this section, we design the packet transmission protocol for the WSN. In order to combat packet content attacks, we encrypt the transmitted packets so that except the BS, any intermediate nodes on the route cannot access the contents and the paths of the packets. However, it should be noted that the proposed protocol is not necessary in malicious link detection if the malicious party does not launch attacks basing on the packet contents.

# A. Protocol Description

1) Packet Encoding: Each node in the WSN shares a distinct secret key with the BS for packet encryption. Each packet received at a node contains two parts: the information bits and the ID of the previous hop. Let the length of the node ID be $L _ { n }$ bits. In addition to the content generated from the source, the information bits also contain the history of the previous hops the packet passed through, however, that information is encrypted by each previous hop so it is not accessible by the current node. The encoding process in packet forwarding includes the following steps:

• Generate a packet hash and append it to the packet. The hash is calculated using the entire packet based on a secure hash algorithm [14]. The secure hash is inserted to provide integrity check of the packet. For efficiency, the generated hash sequence may be truncated before attached to the packet. Let the length of the hash sequence be $L _ { h }$ bits.   
• Encrypt the tail part of the packet, including the previous hop ID and packet hash. In general, the verification of a packet is implemented by certain asymmetric encryption algorithms [14]. However, since only the BS, rather than the intermediate nodes, is required to check the integrity of the received packet; hence a symmetric block cipher, i.e., AES algorithm, is sufficient in the proposed scheme. In practice, if the length of the tail, ${ { L } _ { t } } = { { L } _ { n } } + { { L } _ { h } }$ , is less than, or not a multiple of the block size of AES cipher, we can include the tail of the information bits in the plain text.   
• Append the node ID to the packet and transmit it to the next hop.

The encoding process is demonstrated in Fig. 2. The proposed packet relaying protocol ensures that each packet is not traceable in delivery. Therefore, the malicious party is unable to launch attacks to packets based on the routing history.

2) Packet Decoding at the BS: At the reception of a packet, the BS applies the inverse of the encoding process successively. Suppose the BS has recovered the packet received at node $v _ { i - 1 , j _ { 2 } } ,$ , and found that the previous hop is $v _ { i , j _ { 1 } }$ basing on the tail of the packet. Then by decrypting the tail part of the information bits, the BS obtains the packet hash, as well as the packet received by node $v _ { i , j _ { 1 } }$ . Since the BS stores the secret keys of all the nodes in the network, it is able to recover the packet version received by each intermediate node on the route if no malicious link exists.   
3) Protocol Implementation and Efficiency: The proposed protocol is implemented between the existing network layer and transmission layer of the WSN. This implementation has

two advantages: first, it facilitates easy integration into any existing systems; second, the packet length in the proposed protocol is not limited by the network layer design. Therefore, the loss of throughput from the appended tails at the intermediate nodes can be leveraged by the increased packet length.

# B. Security Analysis

In this subsection, we first discuss the security of the packet transmission scheme under illegal packet modification, then we show that both the detection of packet modification and injection can be converted to that of the packet dropout.

Suppose $e _ { i , j _ { 1 } , j _ { 2 } }$ is a malicious link in the network and the secret key of $v _ { i , j _ { 1 } }$ is unknown to the malicious party. For an arbitrary packet passing through $e _ { i , j _ { 1 } , j _ { 2 } }$ , let $X _ { i , j _ { 1 } , j _ { 2 } } ~ \in ~ \mathbb { F } _ { 2 } ^ { L }$ denote the vector of its information bits and $E _ { i , j _ { 1 } , j _ { 2 } } \ \in \ \mathbb { F } _ { 2 } ^ { L }$ the error pattern applied on it, where L is the length of the information bits. To modify the packet without being detected, the malicious link seeks an error pattern $\pmb { E } _ { i , j _ { 1 } , j _ { 2 } } \neq \mathbf { 0 }$ such that $\begin{array} { r } { Y _ { i , j _ { 1 } , j _ { 2 } } = X _ { i , j _ { 1 } , j _ { 2 } } + E _ { i , j _ { 1 } , j _ { 2 } } } \end{array}$ is a valid output of $v _ { i , j _ { 1 } }$ . We have the following proposition on the security.

Proposition 1. Assuming an ideal cipher (random oracle), the probability that the malicious link generates an unseen ${ Y _ { i , j _ { 1 } , j _ { 2 } } }$ that is valid is negligible if it is infeasible for the malicious party to succeed in the preimage attack to the hash function.

Proof. Let $f ( \cdot )$ denote the encryption function, which is an bijective mapping defined on $\| \dot { \mathsf { F } } _ { 2 } ^ { L _ { t } ^ { \star } } \mapsto \mathbb { F } _ { 2 } ^ { L _ { t } }$ 2 . For the random oracle, if the secret key is unknown, for any integer $1 \leq m \leq$ $2 ^ { L _ { t } }$ and $\boldsymbol { x } \in \mathbb { F } _ { 2 } ^ { L _ { t } }$ , we have

$$
\begin{array}{l} \operatorname * {P r} \{f (\boldsymbol {x}) = \boldsymbol {y} \mid f (\boldsymbol {x} _ {k}) = \boldsymbol {y} _ {k}, 1 \leq k \leq m \} \\ = \left\{ \begin{array}{c l} \frac {1}{2 ^ {L _ {t}} - m}, & \boldsymbol {y} \in \mathbb {F} _ {2} ^ {L _ {t}}, \boldsymbol {y} \notin \{\boldsymbol {y} _ {k} \mid 1 \leq k \leq m \}, \\ 0, & \text { otherwise. } \end{array} \right. \tag {1} \\ \end{array}
$$

where for $1 \leq k \leq m , x _ { k } \in \mathbb { F } _ { 2 } ^ { L _ { t } }$ and ${ \pmb x } \neq { \pmb x } _ { k }$ . That is, the cipher text of an unseen plain text is uniformly distributed over all the unseen cipher texts, and vice versa. For the encrypted tail with error $Y _ { i , j _ { 1 } , j _ { 2 } } ( L - L _ { t } : )$ , we consider two cases:

First, if $Y _ { i , j _ { 1 } , j _ { 2 } } ( L - L _ { t } : )$ has been seen, i.e., the malicious link uses the encrypted tail of another packet to replace the current packet; let $f ( X ^ { \prime } ) = Y _ { i , j _ { 1 } , j _ { 2 } } ( L - L _ { t } : )$ , then the target of the malicious party is to find a vector $Y _ { i , j _ { 1 } , j _ { 2 } } ( : L - L _ { t } )$ , combined with $X ^ { \prime } ( : \ L _ { t } \ - \ L _ { h } )$ , such that its hash value is $X ^ { \prime } ( L _ { t } \mathrm { ~ - ~ } L _ { h } \mathrm { ~ } : )$ . This is the preimage attack to the hash function.

Second, if $Y _ { i , j _ { 1 } , j _ { 2 } } ( L - L _ { t } : )$ has not been seen before, then for the malicious party, the plain text of $Y _ { i , j _ { 1 } , j _ { 2 } } ( L - L _ { t } \ : )$ is uniformly distributed over all the unseen plain texts. For any given prefix vector $Y _ { i , j _ { 1 } , j _ { 2 } } ( : L - L _ { t } )$ , there are $2 ^ { L _ { t } - L _ { h } }$ possible tails since the hash value is determined by the content; so given m observed plain and cipher texts for $f ( \cdot )$ , the probability that $Y _ { i , j _ { 1 } , j _ { 2 } }$ is valid is $\begin{array} { r } { \frac { 2 ^ { L _ { t } - L _ { h } } } { 2 ^ { L _ { t } } - m } \approx \frac { 1 } { 2 ^ { L _ { h } } } } \end{array}$ 12Lh , which is negligible for a large $L _ { h }$ . □

A secure hash function which is believed to be resistant against preimage attacks generally requires $L _ { h }$ to be more than 256 bits [15]. However, considering the efficiency, such hash value might be too long since each hop attaches a hash to the packet in relaying. So we employ two different policies depending on the power of malicious party:

Case I: If the malicious party is unable to attack the hash function at each hop, then we believe $\pmb { E } _ { i , j _ { 1 } , j _ { 2 } } = \mathbf { 0 } \mathrm { ~ i f ~ } Y _ { i , j _ { 1 } , j _ { 2 } }$ passes the verification. In this case, for each packet, we are able to locate the last misbehaved link on the route if any.

Case II: If the malicious party is able to attack the hash function at each hop, then $E _ { i , j _ { 1 } , j _ { 2 } }$ might be non-zero even if $Y _ { i , j _ { 1 } , j _ { 2 } }$ passes the verification. However, while the BS is unable to locate the misbehaved link, it is still able to detect an error by checking the integrity of the packet content. In this case, the BS drops the packet.

For generality, in the following analysis, we focus on case II, where the hash can be quite short to achieve higher efficiency. However, case I provides a quick identification of malicious links for illegal packet modification, when the malicious party is less powerful.

Next, we show that the detection of packet modification and injection can be converted to that of legitimate packet dropout.

Packet Modification: As is noted in case II, the modified packets can be detected by checking the packet contents at the BS. This requires the encryption and verification on the higher layers, e.g., the application layer, which has less effect on the efficiency as they are applied only by the source node. The modified packets will be dropped by the BS, which is equivalent to the packet dropout on the malicious link.

Packet Injection: To prevent the injection of invalid packets in the WSN, e.g., the denial of service (DoS) attacks, we apply flow control at each node for each incoming link. Because of the flow control, the invalid packets will occupy the resources of the legitimate packets on the same link, and again, the legitimate packets will be dropped on the malicious link.

# IV. THE PROPOSED MALICIOUS LINK DETECTION ALGORITHM

In this section, we present the proposed malicious link detection algorithm. As shown in Section III, the malicious behaviors considered in this paper can be converted to the irregular packet dropout on the malicious links. The proposed algorithm hence detects links with higher dropout rate than a predefined baseline, denoted by $p _ { 0 }$ . Our algorithm relies solely on the statistics of packet delivery at the BS to identify the malicious links, and does not require any additional information collected from the nodes. Therefore, the system complexity and overhead can be kept minimum.

We will analyze the packet delivery ratio of each node in the WSN during an observation window. We assume the duration of the observation window is T . $K _ { i , j }$ denotes number of received packets at BS generated by $v _ { i , j }$ during the observation window, while $K _ { i , j _ { 1 } , j _ { 2 } }$ denotes number of received packets generated by $v _ { i , j _ { 1 } }$ 1 and passing through $e _ { i , j _ { 1 } , j _ { 2 } }$ during the observation window.

In the following, we first consider the simplistic case of a 1- hop network, then we discuss the 2-hop network, and further generalize the algorithm to the N-hop network. Finally, we analyze the misdetection rate of the proposed algorithm.

# A. 1-Hop Network

The nodes in 1-hop network connect to the BS directly. Verifying the dropout rate of link $e _ { 1 , j , 0 }$ can be formulated as a one-tailed hypothesis testing on a Bernoulli random variable (RV) as

$$
\text { Null   hypothesis } H _ {0}: p _ {d} (1, j, 0) \leq p _ {0}.
$$

Alternative hypothesis $H _ { 1 } : p _ { d } ( 1 , j , 0 ) > p _ { 0 }$

During the observation window of the algorithm, the number of packets generated from $v _ { 1 , j }$ can be approximated by $\lfloor T G _ { 1 , j } \rfloor . \ K _ { 1 , j }$ should follow a binomial distribution $B ( \lfloor T G _ { 1 , j } \rfloor , 1 - \bar { p _ { d } } ( 1 , j , 0 ) )$ . Conventionally, by allowing a probability of α to reject a true hypothesis (type I error or false alarm), define threshold $\theta ( \alpha )$ as

$$
\theta (\alpha , n, p) \triangleq \max \left\{\theta \mid \sum_ {k = 0} ^ {\theta} \binom {n} {k} (1 - p) ^ {k} p ^ {n - k} \leq \alpha \right\}. \tag {2}
$$

Then we reject hypothesis $H _ { 0 }$ if $K _ { 1 , j } < \theta ( \alpha , \lfloor T G _ { 1 , j } \rfloor , p _ { 0 } )$ in the observation window, i.e., link $e _ { 1 , j , 0 }$ is identified as malicious.

# B. 2-Hop Network

In a 2-hop network, all the links incidental to the BS can be tested as in the 1-hop network. Here we focus on the links between layer 2 and layer $1 , \mathrm { e . g . } , \mathrm { } e _ { 2 , j _ { 1 } , j _ { 2 } }$ . We test the following hypothesis:

$$
\text { Null   hypothesis } H _ {0}: p _ {d} (2, j _ {1}, j _ {2}) \leq p _ {0}. \tag {3}
$$

$\mathrm { A l t e r n a t i v e ~ h y p o t h e s i s ~ } H _ { 1 } : p _ { d } ( 2 , j _ { 1 } , j _ { 2 } ) > p _ { 0 } .$ (4)

With multi-path routing, the data rate on $e _ { 2 , j _ { 1 } , j _ { 2 } }$ is $p _ { t } ( 2 , j _ { 1 } , j _ { 2 } ) G _ { 2 , j _ { 1 } }$ . Since the contents and path information of each packet are encrypted, all the packets generated by $v _ { 2 , j _ { 1 } }$ and received by $v _ { 1 , j _ { 2 } }$ should be treated equivalently as the packets generated by $v _ { 1 , j _ { 2 } }$ after leaving ${ v _ { 1 , j _ { 2 } } } ^ { 1 }$ . Let $p _ { d } ( 1 , j _ { 2 } )$ denote the dropout rate of the combined path from $v _ { 1 , j _ { 2 } }$ to BS. Hence, $K _ { 2 , j _ { 1 } , j _ { 2 } }$ follows a binomial distribution ${ \tilde { B ( \lfloor T p _ { t } ( 2 , j _ { 1 } , j _ { 2 } ) G _ { 2 , j _ { 1 } } \rfloor , \bar { ( 1 \mathrm { ~ - ~ } p _ { d } ( 2 , j _ { 1 } , j _ { 2 } ) ) ( 1 \mathrm { ~ - ~ } p _ { d } ( 1 , j _ { 2 } ) ) ) } } }$ , while $K _ { 1 , j _ { 2 } }$ follows a binomial distribution $B ( \lfloor T G _ { 1 , j _ { 2 } } \rfloor , ( 1 -$ $p _ { d } ( 1 , j _ { 2 } ) ) )$ ). However, we are unable to apply the algorithm in the 1-hop network directly to testing link $e _ { 2 , j _ { 1 } , j _ { 2 } }$ as $p _ { d } ( 1 , j _ { 2 } )$ is unknown. Even if we can obtain an estimate of $p _ { d } ( 1 , j _ { 2 } )$ from the value of $K _ { 1 , j _ { 2 } }$ , the estimation error would render the false alarm rate unbounded, as will be shown in Section V.

We solve the problem by exploiting the joint distribution of $K _ { 2 , j _ { 1 } , j _ { 2 } }$ and $K _ { 1 , j _ { 2 } }$ , where we derive a bounded false alarm in testing $e _ { 2 , j _ { 1 } , j _ { 2 } }$ . The result is generalized in the following proposition.

Proposition 2. Consider i.i.d RVs $X _ { i } \sim B e r n o u l l i ( p ) , i =$ $1 , . . . , n _ { 1 }$ and $Y _ { i } \sim$ Bernou $l l i ( p q ) , i = 1 , . . . , n _ { 2 } , \ p \in$ $( 0 , 1 ) , q \in ( 0 , 1 )$ . Let $\begin{array} { r } { \boldsymbol { X } = \sum _ { i } \boldsymbol { X } _ { i } } \end{array}$ and $Y = \textstyle \sum _ { i } Y _ { i }$ follow binomial distribution $B ( n _ { 1 } , p )$ and $B ( n _ { 2 } , p q )$ , respectively, and $\Phi ( x ; n , \rho )$ denote the distribution function of binomial distribution $B ( n , \rho )$ , i.e.

$$
\operatorname * {P r} \{X = x \} = \Phi (x; n _ {1}, p), \quad \operatorname * {P r} \{Y = y \} = \Phi (y; n _ {2}, p q). \tag {5}
$$

For any α ∈ (0, 1), $n \in \mathbb { Z } ^ { + }$ and $x \in ( 0 , \infty )$ , define $\rho ( \alpha , n , x )$

$$
\rho (\alpha , n, x) \triangleq \max \{\rho \mid \sum_ {k = \lceil x \rceil} ^ {n} \Phi (k; n, \rho) \leq \alpha , \rho \in [ 0, 1 ] \}, \tag {6}
$$

and define $\theta ( \alpha , m , n , q , x ) \in \mathbb { Z } ^ { + }$ as

$$
\theta (\alpha , m, n, q, x) \triangleq \max \{\theta \mid \sum_ {k = 0} ^ {\theta} \Phi (k; n, \rho (\alpha , m, x) q) \leq \alpha \}, \tag {7}
$$

then for $\alpha \in ( 0 , 1 )$ we have

$$
P _ {f a l s e} = \operatorname * {P r} \{Y \leq \theta (\alpha , n _ {1}, n _ {2}, q, X) \} \leq 2 \alpha . \tag {8}
$$

Proof. For $\rho \in [ 0 , 1 ] , n \in \mathbb { Z } ^ { + } , \alpha \in ( 0 , 1 )$ , we define function

$$
x (n, \rho , \alpha) = \min \{x \mid \sum_ {k = x} ^ {n} \Phi (k; n, \rho) \leq \alpha , x \in \mathbb {Z} ^ {+} \}, \tag {9}
$$

e.g. $\operatorname* { P r } \{ X \geq x ( n _ { 1 } , p , \alpha ) \} \leq \alpha$ and $\operatorname* { P r } \{ X \geq x ( n _ { 1 } , p , \alpha ) -$ $1 \} > \alpha$ . Note that for any fixed $x \in ( 0 , \infty )$ and $n \in \mathbb { Z } ^ { + }$ , function $\scriptstyle \sum _ { k = \lceil x \rceil } ^ { n } \Phi ( k ; n , \rho )$ is non-decreasing w.r.t. $\rho \in [ 0 , 1 ]$ ⌈Then we have

$$
\rho (\alpha , n, x (n, \rho_ {0}, \alpha) - 1) <   \rho_ {0}, \rho_ {0} \in (0, 1). \tag {10}
$$

which can be obtained from the fact that $\begin{array} { r } { \sum _ { k = x ( n , \rho _ { 0 } , \alpha ) - 1 } ^ { n } \Phi ( k ; n , \rho _ { 0 } ) > \alpha . } \end{array}$ .

$\scriptstyle \sum _ { k = \lceil x \rceil } ^ { n } \Phi ( k ; n , \rho )$

$$
\sum_ {k = 0} ^ {\theta (\alpha , m, n, q, x (m, \rho_ {0}, \alpha) - 1)} \Phi (k; n, \rho_ {0} q) \leq \alpha . \tag {11}
$$

Also note that for any fixed $\alpha ~ \in ~ ( 0 , 1 )$ and $n \in \mathbb { Z } ^ { + }$ , $\rho ( \alpha , n , x )$ is non-decreasing w.r.t. x ∈ (0, ∞). Again, using the monotonicity of $\begin{array} { r } { \sum _ { k = \lceil x \rceil } ^ { n } \Phi ( k ; n , \rho ) , \theta ( \overset { \cdot } { \alpha } , m , n , q , x ) } \end{array}$ is non-decreasing w.r.t. $x \in ( 0 , \dot { \infty } )$ with other parameters being fixed. According to (9) and (11) and the fact that X and Y are independent, we have

$$
\begin{array}{l} P _ {f a l s e} = \sum_ {x = 0} ^ {n _ {1}} \operatorname * {P r} \{X = x \} \operatorname * {P r} \{Y \leq \theta (\alpha , n _ {1}, n _ {2}, q, x) \} \\ \leq \alpha + \operatorname * {P r} \{Y \leq \theta (\alpha , n _ {1}, n _ {2}, q, x (n _ {1}, p, \alpha) - 1) \}, \tag {12} \\ \end{array}
$$

where $\operatorname* { P r } \{ Y \leq \theta ( \alpha , n _ { 1 } , n _ { 2 } , q , x ( n _ { 1 } , p , \alpha ) - 1 ) \}$ equals

$$
\sum_ {k = 0} ^ {\theta (\alpha , n _ {1}, n _ {2}, q, x (n _ {1}, p, \alpha) - 1)} \Phi (k; n _ {2}, p q) \leq \alpha . \tag {13}
$$

which completes the proof.

According to Proposition 2, by setting the threshold of $K _ { 2 , j _ { 1 } , j _ { 2 } }$ as $\theta ( \alpha , \lfloor T G _ { 1 , j _ { 2 } } \rfloor , \lfloor T p _ { t } ( 2 , j _ { 1 } , j _ { 2 } ) G _ { 2 , j _ { 1 } } \rfloor , 1 \ -$ $p _ { 0 } , K _ { 1 , j _ { 2 } } )$ , the false alarm rate in testing is upper bounded by 2α. In this way, all the links can be tested.

# C. N-hop Network

We further generalize the algorithm to the N-hop network. Consider link $e _ { i , j _ { 1 } , j _ { 2 } } , i > 1$ in the network. The input data rate originated from $\begin{array} { r } { v _ { i , j _ { 1 } } \mathrm { ~ o n ~ } e _ { i , j _ { 1 } , j _ { 2 } } \mathrm { ~ i s ~ } p _ { t } ( i , j _ { 1 } , j _ { 2 } ) G _ { i , j _ { 1 } } ; } \end{array}$ after being received by $v _ { i - 1 , j _ { 2 } }$ , these packets should have the same routing distribution as those originated from $v _ { i - 1 , j _ { 2 } } { \mathrm { ~ i f ~ } } v _ { i - 1 , j _ { 2 } }$ behaves normally. Let $p _ { d } ( i - 1 , j _ { 2 } )$ denote the dropout rate from $v _ { i - 1 , j _ { 2 } }$ to BS. Then both $K _ { i , j _ { 1 } , j _ { 2 } }$ and $K _ { i - 1 , j _ { 2 } }$ follow binomial distributions. According to Proposition 2, if $K _ { i , j _ { 1 } , j _ { 2 } } \leq$ $\theta ( \alpha , \lfloor T G _ { i - 1 , j _ { 2 } } \rfloor , \lfloor T p _ { t } ( i , j _ { 1 } , j _ { 2 } ) G _ { i , j _ { 1 } } \rfloor , 1 \ - \ p _ { 0 } , K _ { i - 1 , j _ { 2 } } ) ,$ , we identify $e _ { i , j _ { 1 } , j _ { 2 } }$ as malicious, whose false alarm rate is bounded by 2α.

It is possible that $v _ { i - 1 , j _ { 2 } }$ may treat the packets it relays differently from those it generates, e.g., dropping the incoming packets or forwarding them disobeying the routing table. These malicious behaviors can be decomposed as either the dropout on the incoming links or the injection to the outgoing links, which can both be detected by the proposed algorithm as noted in Section III. Therefore, the misbehavior of $v _ { i - 1 , j _ { 2 } }$ will not void the generality of the proposed algorithm.

# D. Misdetection Rate Analysis

In this subsection, we show that in the proposed algorithm, if the dropout rate from the end node to the BS is less than 1, the misdetection rate on a link converges to 0 as $T \to \infty$ .

Misdetection happens on link $e _ { i , j _ { 1 } , j _ { 2 } }$ if its dropout rate $p _ { d } ( i , j _ { 1 } , j _ { 2 } )$ is greater than the base line p0 while $K _ { i , j _ { 1 } , j _ { 2 } }$ and $K _ { i - 1 , j _ { 2 } }$ satisfy $K _ { i , j _ { 1 } , j _ { 2 } } \qquad >$ $\begin{array} { r l r } { \theta ( \alpha , \lfloor T G _ { i - 1 , j _ { 2 } } \rfloor , \lfloor T p _ { t } ( i , j _ { 1 } , j _ { 2 } ) \overleftarrow { G } _ { i , j _ { 1 } } \rfloor , 1 } & { { } - } & { p _ { 0 } , \overleftarrow { K } _ { i - 1 , j _ { 2 } } ) . } \end{array}$ The analysis on the probability is summarized in the following proposition.

Proposition 3. Consider i.i.d RVs $X _ { i } \sim B e r n o u l l i ( p ) , i =$ $1 , . . . , n _ { 1 }$ and $Y _ { i } \sim$ Bernou $l i ( p q ) , i ~ = ~ 1 , . . . , n _ { 2 } , ~ p ~ \in$ $( 0 , 1 ] , q \in ( 0 , 1 )$ . Let $X = \textstyle \sum _ { i } X _ { i }$ and $Y = \textstyle \sum _ { i } Y _ { i }$ follow binomial distribution $B ( n _ { 1 } , p )$ and $B ( n _ { 2 } , p q )$ , respectively, and suppose $n _ { 2 } / n _ { 1 } ~ = ~ \kappa$ being fixed. For some $\hat { q } \ > \ q ,$ the probability that $Y > \theta ( \alpha , n _ { 1 } , n _ { 2 } , \hat { q } , X )$ converges to 0 $a s \ n _ { 2 } \ \to \ + \infty$ . More specifically, as $n _ { 2 } \to + \infty$ , the miss detection rate $P _ { m i s s } = \mathrm { P r } \{ Y > \theta ( \alpha , n _ { 1 } , n _ { 2 } , \hat { q } , X ) \}$ satisfies

$$
P _ {m i s s} \leq \left[ \frac {e ^ {(1 - \delta) \hat {q} / q - 1}}{[ (1 - \delta) \hat {q} / q ] ^ {(1 - \delta) \hat {q} / q}} + o (1) \right] ^ {n _ {2} p q} + e ^ {- \frac {\delta}{2} n _ {1} p}, \tag {14}
$$

for any $\delta \in ( 0 , 1 )$ and $( 1 - \delta ) \hat { q } / q > 1$ .

Proof. Note that X and Y are independent, so are $\theta ( \alpha , n _ { 1 } , n _ { 2 } , \hat { q } , X )$ and Y . Therefore, the misdetection rate can be expressed as

$$
P _ {m i s s} = \sum_ {x = 0} ^ {n _ {1}} \Phi (x; n _ {1}, p) \sum_ {y = \theta (\alpha , n _ {1}, n _ {2}, \hat {q}, x) + 1} ^ {n _ {2}} \Phi (y; n _ {2}, p q). \tag {15}
$$

One Chernoff bound of binomial distribution $B ( n , \rho )$ is

$$
\sum_ {k = \lceil x \rceil} ^ {n} \Phi (k; n, \rho) \leq \frac {(n \rho) ^ {x} e ^ {x - n \rho}}{x ^ {x}}. \tag {16}
$$

for $x \geq n \rho$ . This implies a lower bound of $\rho ( \alpha , n , x )$ is

$$
\rho (\alpha , n, x) \geq - \frac {x}{n} W _ {0} (- \frac {\alpha^ {\frac {1}{x}}}{e}). \tag {17}
$$

where $W _ { 0 } ( \cdot )$ is the principle branch of the Lambert W function.

Another Chernoff bound of the binomial distribution is

$$
\sum_ {k = 0} ^ {\theta} \Phi (k; n, \rho) \leq e ^ {- \frac {(n \rho - \theta) ^ {2}}{2 n \rho}}, \tag {18}
$$

for $\theta \leq n \rho .$ , from which we have a lower bound of (2) as

$$
\theta (\alpha , n, \rho) \geq n \rho - \sqrt {- 2 n \rho \log \alpha}. \tag {19}
$$

Note that $\scriptstyle \sum _ { k = 0 } ^ { \theta } \Phi ( k ; n , \rho )$ is non-increasing w.r.t. ρ with other parameters being fixed. From (17), we obtain a lower bound of $\theta ( \alpha , m , n , q , x )$ as

$$
- \frac {n}{m} x W _ {0} (- \frac {\alpha^ {\frac {1}{x}}}{e}) q - \sqrt {2 \frac {n}{m} x W _ {0} (- \frac {\alpha^ {\frac {1}{x}}}{e}) q \log \alpha}, \tag {20}
$$

where we denote (20) by $\tilde { \theta } ( \alpha , m , n , q , x )$ .

Since $\theta ( \alpha , m , n , q , x )$ is non-decreasing w.r.t. x, for any $x _ { 0 } \in [ 0 , n _ { 1 } ]$ , an upper bound of $P _ { m i s s }$ is given by

$$
P _ {m i s s} \leq \operatorname * {P r} \{X \leq x _ {0} \} + \operatorname * {P r} \{Y \geq \theta (\alpha , n _ {1}, n _ {2}, \hat {q}, x _ {0}) \}. \tag {21}
$$

Let $x _ { 0 } = ( 1 - \delta ) n _ { 1 } p$ for some $\delta \in ( 0 , 1 )$ and $n _ { 2 } / n _ { 1 } = \kappa$ being fixed, then we have

$$
\lim _ {n _ {1} \rightarrow + \infty} \frac {\tilde {\theta} (\alpha , n _ {1} , n _ {2} , \hat {q} , x _ {0})}{n _ {1}} = (1 - \delta) \kappa p \hat {q}, \tag {22}
$$

i.e., $\tilde { \theta } ( \alpha , n _ { 1 } , n _ { 2 } , \hat { q } , x _ { 0 } ) = ( 1 - \delta ) n _ { 2 } p \hat { q } + o ( n _ { 1 } )$ . Since $q < { \hat { q } } ,$ by setting δ such that $1 - \delta > q / \hat { q } ,$ , we can derive an upper bound of $\operatorname* { P r } \{ Y \geq \theta ( \alpha , n _ { 1 } , n _ { 2 } , \hat { q } , x _ { 0 } ) \}$ from (16) and (20) as

$$
\left[ \frac {e ^ {(1 - \delta) \hat {q} / q - 1 + o (n _ {1}) / n _ {2}}}{[ (1 - \delta) \hat {q} / q + o (n _ {1}) / n _ {2} ] ^ {(1 - \delta) \hat {q} / q + o (n _ {1}) / n _ {2}}} \right] ^ {n _ {2} p q}. \tag {23}
$$

As $n _ { 2 } \to + \infty .$ , the (23) can be rewritten as

$$
\left[ \frac {e ^ {(1 - \delta) \hat {q} / q - 1}}{[ (1 - \delta) \hat {q} / q ] ^ {(1 - \delta) \hat {q} / q}} + o (1) \right] ^ {n _ {2} p q}, \tag {24}
$$

where $\frac { e ^ { ( 1 - \delta ) \hat { q } / q - 1 } } { [ ( 1 - \delta ) \hat { q } / q ] ^ { ( 1 - \delta ) \hat { q } / q } } ~ \in ~ \left( \frac { e ^ { \hat { q } / q - 1 } } { ( \hat { q } / q ) ^ { \hat { q } / q } } , 1 \right)$ e(1−δ)ˆq/q−1 ( (q/qˆ )q/q ˆ , 1). Furthermore, from eq/q ˆ −1 (18),

$$
\operatorname * {P r} \{X \leq x _ {0} \} \leq e ^ {- \frac {\delta}{2} n _ {1} p}. \tag {25}
$$

Then (15) follows from (21), (24) and (25), which completes the proof. □

# V. SIMULATION

In this section, we validate the the proposed malicious link detection algorithm through numerical examples.

We consider an arbitrary link $e _ { i , j _ { 1 } , j _ { 2 } }$ during an observation window of duration T . To demonstrate the performance of the proposed algorithm under different network settings, we vary the data rates $G _ { i , j _ { 1 } }$ and $G _ { i - 1 , j _ { 2 } } ,$ , the dropout rates $p _ { d } ( i , j _ { 1 } , j _ { 2 } )$ and $p _ { d } ( i - 1 , j _ { 2 } )$ , in the numerical results.

Baseline Algorithm: Since the difficulty of the malicious link detection lies in that the dropout rate $p _ { d } ( i - 1 , j _ { 2 } )$ is unknown at the BS, we consider a baseline algorithm which first estimates $p _ { d } ( i - 1 , j _ { 2 } )$ by

![](images/3c50fbefe8e08010084ddc8b2acff9b6f3b3f38f1f42c07419be00499c103aec.jpg)



(a) Proposed algorithm

![](images/3b03c7e338a62d5ac0ead182613bf161f3904ab8d9e2e723fd9c90621865bc79.jpg)



(b) Baseline algorithm

Fig. 3: The false alarm rates versus the data generation rate ratio $p _ { t } ( i , j _ { 1 } , j _ { 2 } ) G _ { i , j _ { 1 } } / G _ { i - 1 , j _ { 2 } }$ .   
![](images/cf21aacd094faede783dafd895778c6886e17b2344d5f39b853bc7a6309f2256.jpg)



Fig. 4: The misdetection rate of the proposed algorithm versus the number of generated packets in the observation window $T G _ { i - 1 , j _ { 2 } }$ for $p _ { d } ( i - 1 , j _ { 2 } ) = 0 . 2$ and pt(i,j1,j2)Gi,j1 = 1. $\begin{array} { r } { \frac { p _ { t } ( i , j _ { 1 } , j _ { 2 } ) G _ { i , j _ { 1 } } } { G _ { i - 1 , j _ { 2 } } } = 1 } \end{array}$ Gi−1,j2

$$
\tilde {p} _ {d} = K _ {i - 1, j _ {2}} / (T G _ {i - 1, j _ {2}}). \tag {26}
$$

Then for a baseline dropout rate p0, it calculates the threshold in the hypothesis test following the traditional method by

$$
\theta (\alpha , T p _ {t} (i, j _ {1}, j _ {2}) G _ {i, j _ {1}}, (1 - \tilde {p} _ {d}) (1 - p _ {0})), \tag {27}
$$

for an allowed false alarm rate of α. However, we will see that its actual false alarm rate cannot be bounded by α.

False alarm rate comparison between the proposed algorithm and the baseline algorithm: In this example, we set the allowed false alarm rate $\alpha _ { 0 } = 0 . 0 5$ and the baseline dropout rate as $p _ { 0 } = p _ { d } ( i , j _ { 1 } , j _ { 2 } ) = 0 . 0 1$ . The results are plotted in Fig. 3a and Fig. 3b, respectively. For the proposed algorithm, it is shown the actual false alarm rate is much lower than the required bound $\alpha _ { 0 }$ . On the other hand, because of the error in $p _ { d } ( i - 1 , j _ { 2 } )$ estimation, the baseline algorithm cannot bound the false alarm rate in detection unless the dropout rate $p _ { d } ( i - 1 , j _ { 2 } )$ is very close to 0.

Misdetection rate of the proposed algorithm: In this example, we evaluate the misdetection rate of the proposed algorithm when $e _ { i , j _ { 1 } , j _ { 2 } }$ is a malicious link. We keep the baseline dropout rate $p _ { 0 } = 0 . 0 1$ and false alarm rate upper bound $\alpha _ { 0 } ~ = ~ 0 . 0 5$ , and set $p _ { t } ( i , j _ { 1 } , j _ { 2 } ) G _ { i , j _ { 1 } } / G _ { i - 1 , j _ { 2 } } ~ = ~ 1$ and $p _ { d } ( i \textrm { -- } 1 , j _ { 2 } ) \ = \ 0 . 2$ . The results are plotted in Fig. 4. The numerical results are consistent with the theoretical analysis, i.e., the misdetection rate becomes arbitrarily small as the observation window duration T increases. However, the number of packets needed for an accurate detection varies significantly with the actual dropout rate $p _ { d } ( i , j _ { 1 } , j _ { 2 } )$ .

# VI. CONCLUSION

In this paper, we proposed an efficient and robust malicious link detection scheme for multi-hop WSNs. Comparing with existing approaches that rely on the intermediate nodes to carry out the detection process, in the proposed scheme, malicious link detection was only performed at the base stations by exploiting the statistics of packet delivery rates. As a result, the proposed scheme could effectively detect the irregular dropout at every hop (or link) along the routing paths with significantly higher accuracy, and at the same time, reducing system overhead and improving the efficiency. The effectiveness of the proposed scheme was demonstrated through both theoretical analysis and simulation results.

# REFERENCES

[1] X. Chen, K. Makki, K. Yen, and N. Pissinou, “Sensor network security: a survey,” IEEE Communications Surveys Tutorials, vol. 11, no. 2, pp. 52–73, Second 2009.   
[2] Y. Zhang, L. Lazos, and W. Kozma, “Amd: Audit-based misbehavior detection in wireless ad hoc networks,” IEEE Transactions on Mobile Computing, vol. 15, no. 8, pp. 1893–1907, Aug 2016.   
[3] T. Shu and M. Krunz, “Privacy-preserving and truthful detection of packet dropping attacks in wireless ad hoc networks,” IEEE Transactions on Mobile Computing, vol. 14, no. 4, pp. 813–828, April 2015.   
[4] Q. Li and G. Cao, “Mitigating routing misbehavior in disruption tolerant networks,” IEEE Transactions on Information Forensics and Security, vol. 7, no. 2, pp. 664–675, April 2012.   
[5] J. Staddon, D. Balfanz, and G. Durfee, “Efficient tracing of failed nodes in sensor networks,” in Proceedings of ACM International Workshop on Wireless Sensor Networks and Applications, 2002, pp. 122–130.   
[6] K. Liu, J. Deng, P. K. Varshney, and K. Balakrishnan, “An acknowledgment-based approach for the detection of routing misbehavior in manets,” IEEE Transactions on Mobile Computing, vol. 6, no. 5, pp. 536–550, May 2007.   
[7] J. Chang, P. Tsou, I. Woungang, H. Chao, and C. Lai, “Defending against collaborative attacks by malicious nodes in manets: A cooperative bait detection approach,” IEEE Systems Journal, vol. 9, no. 1, pp. 65–75, March 2015.   
[8] Q. Wang, L. Vu, K. Nahrstedt, and H. Khurana, “Mis: Malicious nodes identification scheme in network-coding-based peer-to-peer streaming,” in Proceedings of IEEE INFOCOM, March 2010, pp. 1–5.   
[9] S. Buchegger and J. . L. Boudec, “Self-policing mobile ad hoc networks by reputation systems,” IEEE Communications Magazine, vol. 43, no. 7, pp. 101–107, July 2005.   
[10] Y. Xue and K. Nahrstedt, “Providing fault-tolerant ad hoc routing service in adversarial environments,” Wireless Personal Communications, vol. 29, no. 3, pp. 367–388, Jun 2004.   
[11] T. Li, M. Abdelhakim, and J. Ren, “N-hop networks: A general framework for wireless systems,” IEEE Wireless Communications, vol. 21, no. 2, pp. 98–105, 2014.   
[12] D. Thaler and C. Hopps, “Multipath issues in unicast and multicast next-hop selection,” United States, 2000.   
[13] C. E. Perkins and E. M. Royer, “Ad-hoc on-demand distance vector routing,” in Proceedings WMCSA’99. Second IEEE Workshop on Mobile Computing Systems and Applications, Feb 1999, pp. 90–100.   
[14] J. Katz and Y. Lindell, Introduction to Modern Cryptography. Chapman & Hall/CRC, 2007.   
[15] P. Rogaway and T. Shrimpton, “Cryptographic hash-function basics: Definitions, implications, and separations for preimage resistance, second-preimage resistance, and collision resistance,” in International Workshop on Fast Software Encryption, 2004, pp. 371–388.