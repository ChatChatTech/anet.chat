# Multicast throughput for large scale cognitive networks

Cheng Wang • Changjun Jiang • Xiang-Yang Li • Yunhao Liu

Published online: 29 January 2010 - Springer Science+Business Media, LLC 2010

Abstract In this paper, we focus on the achievable throughput of cognitive networks consisting of the primary ad hoc network (PaN) and the secondary ad hoc network (SaN). We construct PaN and SaN by placing nodes according to Poisson point processes of density n and m respectively over a unit square region. We directly study the multicast throughput of cognitive network to unify that of unicast and broadcast sessions. In order to ensure the priority of primary users in meanings of throughput, we design a metric called throughput decrement ratio (TDR) to measure the ratio of the throughput of PaN in presence of SaN to that of PaN in absence of SaN. Endowing PaN with the right to determine the threshold of the TDR, we propose multicast schemes based on TDMA and multihop routing for the two networks respectively and derive their achievable multicast throughput depending on the given threshold. Specially, we show when PaN has sparser density than SaN, to be specific, $\begin{array} { r } { n = o \left( \frac { m } { \left( \log m \right) ^ { 2 } } \right) } \end{array}$ ; and if PaN only cares about the order of its throughput, SaN can simultaneously achieve the same order of the aggregated multicast throughput as it were a standalone network in absence of PaN.

Keywords Multicast throughput - Cognitive networks - Gaussian channel model - Asymptotic scalability

# 1 Introduction

The researchers have been performing an extensive and in depth research theoretically and methodologically on the topic of capacity scaling laws of wireless networks. The main advantage of studying scaling laws is to highlight qualitative and architectural properties of the system without getting involved with too many details. Gupta and Kumar [1] showed that for unicast sessions, the per-session throughput can be achieved of order $\Omega ( 1 / { \sqrt { n \log n } } ) ^ { 1 }$ , by using a specific multihop strategy in random networks. For broadcast sessions, Keshavarz-Haddad et al. [2] showed that the achievable broadcast capacity per-session is only of order H(1/n). The research of multicast throughput is more complicated than that of unicast and broadcast. Li et al. [3] and Shakkottai et al. [4] proposed results for multicast throughput of networks. Li et al. [3] showed that, for random networks, if $\begin{array} { r } { n _ { s } \geq \Theta \left( \log n _ { d } \cdot \sqrt { \frac { n \log n } { n _ { d } } } \right) } \end{array}$ the achievable persession multicast throughput is $\begin{array} { r } { \Omega \left( \frac { \sqrt { n } } { n _ { s } \sqrt { n _ { d } \log n } } \right) } \end{array}$ if ${ n } _ { d } =$ $\scriptstyle O \left( { \frac { n } { \log n } } \right)$ ; and is $\Omega \left( \frac { 1 } { n _ { s } } \right)$ if $\begin{array} { r } { n _ { d } = \Omega \left( \frac { n } { \log n } \right) } \end{array}$ where $n _ { s }$ is the number of multicast sessions and $n _ { d }$ is the number of

C. Wang (&) - C. Jiang Key Laboratory of Embedded System and Service Computing, Ministry of Education, Department of Computer Science, Tongji University, Shanghai, China e-mail: chengwang@ust.hk; 3chengwang@gmail.com

X.-Y. Li Department of Computer Science, Illinois Institute of Technology, Chicago, IL 60616, USA

Y. Liu Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong, China

1 Knuth’s Notation: The following notations are used throughout this paper. Given non-negative functions f (n) and $g ( n ) \colon f \left( n \right) = O ( g ( n ) )$ means there exist positive constants c and $n _ { 0 }$ such that f (n) B cg(n) for all $n \geq n _ { 0 } ; f ( n ) = \Omega ( g ( n ) )$ means there exist positive constants c and $n _ { 0 }$ such that $f ( n ) \geq c g ( n )$ for all $n \geq n _ { 0 } ,$ namely, $g ( n ) = O ( f ( n ) ) ;$ $f \left( n \right) = \Theta ( g ( n ) )$ means that both $f ( n ) = \Omega ( g ( n ) )$ and $f ( n ) = O ( g ( n ) )$ hold; $f \left( n \right) , = o \left( g ( n ) \right)$ means that lim $\begin{array} { r } { \frac { f ( n ) } { \varrho ( n ) } = 0 ; f ( n ) = \omega ( g ( n ) ) } \end{array}$ means that limn!1 f ðnÞ $\operatorname* { l i m } _ { n \to \infty } { \frac { g ( n ) } { f ( n ) } } = { \bar { 0 } } , \qquad $ n!1; namely, f (n) = o(g(n)). gðnÞ

destinations of each session. Note that the above results are mainly derived under the protocol model or physical model [1]. For the more challenging Gaussian channel model, some representative works have been carried out for unicast, broadcast and multicast. Franceschetti et al. [5] showed that the per-session unicast throughput of $\Omega ( 1 / { \sqrt { n } } )$ is achievable in random networks. Zheng [6] pointed out that using multihop relay, the rate of broadcast is $\Theta \left( \left( \log n \right) ^ { - \frac { \alpha } { 2 } } \right)$ in random extended networks. Recently, Li et al. [8] proposed that, when $\begin{array} { r } { n _ { d } = O \left( \frac { n } { \left( \log n \right) ^ { 2 \alpha + 6 } } \right) } \end{array}$ 2aþ6 and $n _ { s } = \Omega \Big ( n ^ { \frac { 1 } { 2 } + \theta } \Big )$ ; the achievable per-session multicast throughput is w.h.p., of order $\begin{array} { r } { \Omega \left( \frac { \sqrt { n } } { n _ { s } \sqrt { n _ { d } } } \right) } \end{array}$ where $\theta > 0$ is an arbitrary constant. Most recently, based on percolation theory, Wang et al. [9] proposed the multicast schemes and analyzed the achievable throughput by considering all possible values of $n _ { s }$ and $n _ { d } .$ As a special case of the results, they showed that for $n _ { s } = \Theta ( n )$ , the per-session multicast capacity of random dense networks is $\begin{array} { r } { \Theta \left( \frac { 1 } { \sqrt { n _ { d } n } } \right) } \end{array}$ ffiffiffiffiffind n  when $\begin{array} { r } { n _ { d } = O \left( \frac { n } { \left( \log n \right) ^ { 3 } } \right) } \end{array}$ and is $\Theta \left( { \textstyle { \frac { 1 } { n } } } \right)$ when $\begin{array} { r } { n _ { d } = \Omega \left( \frac { \dot { n } } { \log n } \right) } \end{array}$ Note that all these results are derived under the bounded propagation model [10] and for a single network.

An investigation has shown that, as the demand for bandwidth is increasing, much of the licensed spectrum remains idle in a surprisingly large proportion of the time and space [11, 12]. A natural solution for this issue is to permit some users to access opportunistically the spectrum without having a negative impact on the licensed users. Thus, cognitive networks arise. Generally, the cognitive network consists of two independent overlapping networks, called the primary network and secondary network that operate at the same time, space and frequency. The secondary users require the ability to sense the idle spectrum, and they are often assumed to be equipped with cognitive radios or more intelligent wireless devices which enables them to obtain a certain information of the primary user [13, 14]. The research on the capacity for cognitive networks is a relatively new topic. In [13] the primary sourcedestination and cognitive S-D pairs are modeled as an interference channel with asymmetric side-information. In [15] the communication opportunities are modeled as a two-switch channel. Note that both work [13, 15] has only considered the single-user case in which a single primary and a single cognitive S-D pairs share the spectrum. Recently, a single-hop cognitive network was considered in [16], where multiple secondary S-D pairs transmit in the presence of a single primary S-D pair. They showed that a linear scaling law of the single-hop secondary network is obtained when its operation is constrained to guarantee a particular outage constraint for the primary S-D pair. The most related work to this paper is done by Jeon et al. in [17] for multi-hop and multiple users case. They studied a general environment in which a primary ad hoc network (PaN) and a secondary (cognitive) ad hoc network (SaN) co-exist. PaN and SaN are constructed by placing nodes according to a Poisson point process (p.p.p.) of density n and m respectively over a unit square. They showed that both networks can simultaneously achieve the same scaling law of the throughput as a stand-alone ad hoc network when $m = n ^ { \beta }$ for $\beta > 1$ . Note that they only focus on unicast sessions.

In this paper, we study multicast throughput for a similar cognitive network to the model considered in [17]. For the density of both networks, we assume that $\begin{array} { r } { n = o \left( \frac { m } { \left( \log m \right) ^ { 2 } } \right) } \end{array}$ as a weaker condition than that $n = m ^ { 1 / \beta } \left( \beta > 1 \right)$ in [17]. We essentially investigate two questions. The first is how to define and guarantee the priority of PaN. As pointed out in [17], the most important constraint is that PaN does not alter its protocol due to SaN anyway. Otherwise, a simple equal time-sharing can achieve the same order of throughput for both networks as they are stand-alone, which makes the problem trivial. In addition, we deem that the above constraint can not sufficiently guarantee the overwhelming priority of primary users. We design a metric called throughput decrement ratio (TDR) to measure the ratio of the throughput of PaN in presence of SaN to that of one in absence of SaN. It is obvious that, for a given threshold of TDR, the achievable throughput of both networks must depend on the threshold. We endow PaN with the right to determine the threshold. The other question is how to deal with the extension from unicast session to multicast one. It is known that the result of multicast throughput can usually unify that of unicast and broadcast, which partly contributes to the difficulty in the research of multicast. A characteristics of this paper is that we take account of all cases of $n _ { s }$ and $n _ { d } ,$ , without any assumption of $n _ { s }$ and $n _ { d }$ as in most other literatures. According to a given threshold of TDR, we propose the multicast schemes based on TDMA and multihop routing for two networks respectively and derive their achievable throughput depending on the given threshold. The most challenging issue is to design a scheme for SaN to protect the throughput of PaN from decreasing into the extent they can not tolerate. By set the preservation regions and the transmitting power regulator for the transmissions in SaN, it can ensure the TDR to be over the threshold. To be specific, we show that if PaN only care about the order of its throughput, i.e., the threshold of TDR is a constant in (0, 1], SaN can achieve the same order of the aggregated and per-session multicast throughput as it were a stand-alone topologically isomorphic ad hoc network. In this scenario, the result of [17] can be derived from our result as a special case. If PaN can not tolerate any little impact in asymptotic meaning on its throughput imposed by SaN, i.e., the threshold of TDR is put up as 1, there is an arbitrary infinitesimal factor $\theta ( n ) = o ( 1 )$ as a gap between the achievable throughput of SaN and that of one in absence of PaN.

The rest of the paper is organized as follows. In Sect. 2 the system model is introduced. In Sect. 3 we propose the multicast schemes for both PaN and SaN. In Sect. 4, the main results are presented. In Sect. 5 we analyze the achievable multicast throughput and prove our main results. In Sect. 6, we conclude this paper and discuss the future work. The proofs of some lemmas are provided in Appendix A.

# 2 System model

Throughout the paper, we are mainly concerned with events that happen with high probability $( w . h . p . )$ as the scale of networks goes to infinity.

# 2.1 Network topology

We consider a planar area where two networks share the same space, time and spectrum. The two networks have no communication with each other. We focus on the scenario that two overlapping networks are both ad hoc networks. For another case that the primary network is an infrastructure-supported network (or hybrid network) [18–20], it can be treated as an extension work of this paper in future.

The primary and secondary ad hoc networks are built by placing nodes according to Poisson point processes $\left( \mathrm { p . p . p . } \right)$ of intensity n and m respectively over a unit square $\boldsymbol { A } _ { 1 } =$ $[ 0 , 1 ] \times [ 0 , 1 ] ,$ : Denote the primary network as $\mathcal { N } _ { p } ( n ) =$ $( \mathcal { V } _ { p } ( n ) , \mathcal { E } _ { p } ( n ) )$ ; and denote the secondary network as $\mathcal { N } _ { s } ( m ) = ( \mathcal { V } _ { s } ( m ) , \mathcal { E } _ { s } ( m ) )$ ; where $\nu _ { p } ( n )$ (or $\nu _ { s } ( m ) )$ and $\mathcal { E } _ { p } ( n ) ~ ( \mathrm { o r } ~ \mathcal { E } _ { s } ( m ) )$ are the set of all nodes and edges of $\mathcal { N } _ { p } ( n ) \left( \mathrm { o r } \mathcal { N } _ { s } ( m ) \right)$ ). Note that under our channel model that will be described in Sect. 2.2 below, any two nodes in $\mathcal { N } _ { p } ( n ) ~ ( \mathrm { o r } ~ \mathcal { N } _ { s } ( m ) )$ can build a direct communication, then $\mathcal { N } _ { p } ( n ) \mathrm { ( o r } \mathcal { N } _ { s } ( m ) )$ is indeed a complete graph. By Chebychev’s inequality (Lemma 3), it can be easily obtained that, $w . h . p .$ ., the number of primary nodes $| \mathcal { V } _ { p } ( n ) |$ is within $( ( 1 \mathrm { ~ - ~ } \varepsilon _ { 1 } ) n , ( 1 \mathrm { ~ + ~ } \varepsilon _ { 1 } ) n )$ , and the number of secondary nodes $| \nu _ { s } ( m ) |$ is within $( ( 1 \mathrm { ~ - ~ } \varepsilon _ { 2 } ) m , ( 1 \mathrm { ~ + ~ } \varepsilon _ { 2 } ) m )$ , where $\varepsilon _ { 1 }$ and $\varepsilon _ { 2 }$ are certain constants. To simplify the description, we assume that $| \mathcal { V } _ { p } ( n ) | = n \mathrm { ~ a n d ~ } | \mathcal { V } _ { s } ( m ) | = m$ respectively, which has no impact on our results in order sense. We further state the following assumption.

# 2.1.1 Assumption A

1. $\mathcal { N } _ { p } ( n )$ operates as if $\mathcal { N } _ { s } ( m )$ were absent.   
2. Secondary nodes know the locations of primary nodes and the protocol adopted by $\mathcal { N } _ { p } ( n )$

3. Secondary network is denser than the primary one, to be specific, we assume that $\begin{array} { r } { n = o \left( \frac { m } { \left( \log m \right) ^ { 2 } } \right) } \end{array}$ :

Our work can be expanded to the case multiple overlapping networks with a more general assumption that higher-priority users have less density than those lower-priority nodes. In terms of the network topology, the overlapping networks form a pyramidal structure. We call this network model pyramidal cognitive network.

# 2.2 Channel model

Each network operates based on slotted transmissions. The TDMA schemes for both networks are synchronous, i.e., their time slots have equal length. But the scheduling length (scheduling periods) are unnecessarily equal. Let

$$
\mathcal {V} (\tau) = \left\{v _ {k} \mid v _ {k} \text {   is   scheduled   to   transmit   at   slot   } \tau \right\}
$$

be the subset of nodes simultaneously transmitting in a time slot s. We assume that the interference at a receiver is simply regarded as noise. So, during the time slot $\tau : \nu _ { i } \in$ $\mathcal { V } ( \tau ) , \nu _ { i }$ and $\nu _ { j }$ can communicate via a direct link, over a channel with unit bandwidth, of rate

$$
R (v _ {i}, v _ {j}; \tau) = \log \left(1 + \frac {S (v _ {i} , v _ {j} ; \tau)}{N _ {0} + I (v _ {i} , v _ {j} ; \tau)}\right),
$$

where $N _ { 0 }$ is the ambient noise, $S ( \nu _ { i } , \nu _ { j } ; \tau )$ is the strength of the signal initiated by $\nu _ { i }$ at the receiver $\nu _ { j }$ in the time slot s; $I ( \nu _ { i } , \nu _ { j } ;$ s) is the sum interference power at $\nu _ { j }$ produced by all nodes belonging to $\mathcal { V } ( \tau ) - \{ \nu _ { i } \}$ . We denote the set of all primary nodes (or all secondary nodes) transmitting in any time slot s by $\mathcal { V } _ { p } ( \tau ) : = \mathcal { V } ( \tau ) \cap \mathcal { V } _ { p } ( n )$ (or $\mathcal { V } _ { s } ( \tau ) : = \mathcal { V } ( \tau )$ 号 $\cap \mathcal { V } _ { s } ( m ) )$ ). Furthermore, for any node $\nu _ { i } \in \mathcal { V } _ { p } ( n ) \cup \mathcal { V } _ { s } ( m )$ ; we define $\begin{array} { r } { \mathcal { V } _ { p } ( \nu _ { i } , \tau ) : = \mathcal { V } _ { p } ( \tau ) - \{ \nu _ { i } \} \quad \mathrm { ( o r } \quad \mathcal { V } _ { s } ( \nu _ { i } , \tau ) : = } \end{array}$ $\mathcal { V } _ { s } ( \tau ) - \{ \nu _ { i } \} )$ .

Thus, according to the scenario of two overlapping networks and the fact that no inter-communication occurs between two networks, we have that in any time slot s,

$$
I (v _ {i}, v _ {j}; \tau) =
$$

$$
\left\{ \begin{array}{l l} I _ {p p} (v _ {i}, v _ {j}; \tau) + I _ {s p} (v _ {i}, v _ {j}; \tau), & \text { when } v _ {i}, v _ {j} \in \mathcal {V} _ {p} (n) \\ I _ {p s} (v _ {i}, v _ {j}; \tau) + I _ {s s} (v _ {i}, v _ {j}; \tau), & \text { when } v _ {i}, v _ {j} \in \mathcal {V} _ {s} (m) \end{array} \right.,
$$

where

$\begin{array} { r l } { - } & { { } I _ { p p } ( \nu _ { i } , ~ \nu _ { j } ; ~ \tau ) } \end{array}$ (or $I _ { p s } ( \nu _ { i } , \nu _ { j } ; \tau ) )$ : the sum of interference power at $\nu _ { j }$ from all nodes in $\mathcal { V } _ { p } ( \nu _ { i } , \tau ) ;$ ;   
– $I _ { s p } ( \nu _ { i } , \nu _ { j } ; \tau ) \ ( \mathrm { o r } \ I _ { s s } ( \nu _ { i } , \nu _ { j } ; \tau ) ) { } ;$ the sum of interference power at $\nu _ { j }$ from all nodes in $\mathcal { V } _ { s } ( \nu _ { i } , \tau )$ :

The wireless propagation channel typically includes path loss with distance, shadowing and fading effects. In this paper, we assume the channel gain depends only on the distance between a transmitter and receiver, and ignore shadowing and fading. Thus, the channel power gain $\ell ; ( \nu _ { i } , \nu _ { j } )$ , normalized by a constant, is given by $\ell ( \nu _ { i } , \nu _ { j } ) =$ $d ( \nu _ { i } , \nu _ { j } ) ^ { - \alpha }$ , where $d ( \nu _ { i } , \nu _ { j } ) = \lvert \nu _ { i } - \nu _ { j } \rvert$ is the Euclidean distance between nodes $\nu _ { i }$ and $\nu _ { j } ,$ and $\alpha > 2$ denotes the power attenuation exponent.

In PaN $\mathcal { N } _ { p } ( n )$ ; during a time slot s, when any node $\nu _ { k } \in$ VðsÞ transmits with power $P ( \nu _ { k } , \tau )$ , the primary user pairs $\nu _ { i } ^ { p } \in \mathcal { V } _ { p } ( \tau )$ and $\nu _ { j } ^ { p } \in \mathcal { V } _ { p } ( n )$ can establish a direct communication link, over a channel of unit bandwidth, of rate

$$
R _ {p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) = \log \left(1 + \frac {S (v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau)}{N _ {0} + I _ {p p} (v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau) + I _ {s p} (v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau)}\right),
$$

where

$$
\begin{array}{l} - S (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) = P (v _ {i} ^ {p}, \tau) | v _ {i} ^ {p} - v _ {j} ^ {p} | ^ {- \alpha}, \\ - I _ {p p} \left(v _ {i} ^ {p}, v _ {j} ^ {p}; \tau\right) = \sum_ {v _ {k} ^ {p} \in \mathcal {V} _ {p} \left(v _ {i} ^ {p}, \tau\right)} P \left(v _ {k}, \tau\right) \left| v _ {k} ^ {p} - v _ {j} ^ {p} \right| ^ {- \alpha}, \\ - I _ {s p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) = \sum_ {v _ {k} ^ {s} \in \mathcal {V} _ {s} (v _ {i} ^ {p}, \tau)} P (v _ {k}, \tau) | v _ {k} ^ {s} - v _ {j} ^ {p} | ^ {- \alpha}. \\ \end{array}
$$

Similarly, in SaN $\mathcal { N } _ { s } ( m )$ ; at the time slot s, the secondary user pairs $\nu _ { i } ^ { s } \in \mathcal { V } _ { s } ( \tau )$ and $\nu _ { j } ^ { s } \in \mathcal { V } _ { s } ( m )$ can build a direct communication link, over a channel of unit bandwidth, of rate

$$
R _ {s} (v _ {i} ^ {s}, v _ {j} ^ {s}; \tau) = \log \left(1 + \frac {S (v _ {i} ^ {s} , v _ {j} ^ {s} ; \tau)}{N _ {0} + I _ {p s} (v _ {i} ^ {s} , v _ {j} ^ {s} ; \tau) + I _ {s s} (v _ {i} ^ {s} , v _ {j} ^ {s} ; \tau)}\right),
$$

where

$$
\begin{array}{l} - S \left(v _ {i} ^ {s}, v _ {j} ^ {s}; \tau\right) = P \left(v _ {i} ^ {s}, \tau\right) \left| v _ {i} ^ {s} - v _ {j} ^ {s} \right| ^ {- \alpha}, \\ - I _ {p s} \left(v _ {i} ^ {s}, v _ {j} ^ {s}; \tau\right) = \sum_ {v _ {k} ^ {p} \in \mathcal {V} _ {p} \left(v _ {i} ^ {s}, \tau\right)} P \left(v _ {k}, \tau\right) \left| v _ {k} ^ {p} - v _ {j} ^ {s} \right| ^ {- \alpha}, \\ - I _ {s s} \left(v _ {i} ^ {s}, v _ {j} ^ {s}; \tau\right) = \sum_ {v _ {k} ^ {s} \in \mathcal {V} _ {s} \left(v _ {i} ^ {s}, \tau\right)} P \left(v _ {k}, \tau\right) \left| v _ {k} ^ {s} - v _ {j} ^ {s} \right| ^ {- \alpha}. \\ \end{array}
$$

# 2.3 Assurance of priority for primary users

# 2.3.1 Non-trivial constraint

$\mathcal { N } _ { p } ( n )$ does not alter its protocol due to $\mathcal { N } _ { s } ( m )$ : Otherwise, a simple allocation of time slots can achieve the same asymptotic throughput as if they were stand-alone networks in absence of each other.

# 2.3.2 Priority guarantee in throughput

Due to the nature of wireless spectrum, $\mathcal { N } _ { p } ( n )$ and $\mathcal { N } _ { s } ( m )$ always have negative influence (interference) on each other under the noncooperative communication scheme as long as they share the same spectrum at the same time. Hence, the key issue is how much interference produced by the secondary users is tolerable for $\mathcal { N } _ { p } ( n )$ : We deem that it should be a parameter determined by primary users based on their specific requirements. The strategy in [17] is to ensure that $\mathcal { N } _ { s } ( m )$ does not reduce asymptotic throughput for $\mathcal { N } _ { p } ( n )$ : It is not sufficient to maintain the priority of primary networks. For instance, consider an artificial scenario that the throughput of $\mathcal { N } _ { p } ( n )$ reduces by 50% because of the presence of $\mathscr { N } _ { s } ( m ) . \mathrm { I f } \mathscr { N } _ { p } ( n )$ can tolerate at most 20% decrement of the throughput, then the priority of primary users is indeed not respected, although the throughput of $\mathcal { N } _ { p } ( n )$ is not decreased in order sense. So, for a specific multicast scheme of $\mathcal { N } _ { p } ( n )$ ; we define two parameters TDR [Throughput Decrement Radio, Eq. (2)] and IIF [Interference Intensity Factor, Eq. (4)] to guarantee the priority of $\mathcal { N } _ { p } ( n )$ ; according to its specific requirements in terms of the throughput, instead of only caring about the order of the throughput.

# 2.4 Achievable throughput

We propose the formal definition of achievable throughput by modifying that in [3, 21]. Let $\mathcal { V } = \{ \nu _ { 1 } , \nu _ { 2 } , . . . , \nu _ { n } \}$ denote the set of all nodes in the network and let the subset $\mathcal { S } \subseteq \mathcal { V }$ denote the set of source nodes of multicast. Let the number of multicast sessions be $| S | = n _ { s } .$ : For each source $\nu _ { S , i } \in S ,$ ; we uniformly choose $n _ { d }$ nodes at random from other nodes to construct $\mathcal { D } _ { \mathcal { S } , i } = \{ \nu _ { \mathcal { S } , i _ { 1 } } , \nu _ { \mathcal { S } , i _ { 2 } } , . . . , \nu _ { \mathcal { S } , i _ { n _ { d } } } \}$ as the set of destinations, where obviously $n _ { d } \le n - 1$ . We call $\mathcal { U } _ { S , i } =$ $\{ \nu _ { S , i } \} \cup \mathcal { D } _ { S , i }$ the spanning set of multicast session $\mathcal { M } _ { \mathcal { S } , i }$ : Denote $A _ { S , n _ { d } } = ( \lambda _ { S , 1 } , \lambda _ { S , 2 } , . . . , \lambda _ { S , n _ { s } } )$ as a rate vector of the multicast data rate of all multicast sessions.

Definition 1 (Feasible rate vector) A rate vector ${ \varLambda } _ { S , n _ { d } } =$ $( \lambda _ { S , 1 } , \lambda _ { S , 2 } , . . . , \lambda _ { S , n _ { s } } )$ is called $( \rho _ { s } , \rho _ { d } ) – f e a s i b l e ,$ , where $\rho _ { s }$ and $\rho _ { d }$ are both constants in [0, 1], if for a subset of sources, denoted as $S ^ { \prime } ( \rho _ { s } , \rho _ { d } ) \subseteq S$ satisfying to $| S ^ { \prime } ( \rho _ { s } , \rho _ { d } ) | =$ $\rho _ { s } ( n ) \cdot n _ { s } ,$ ; there exists a spatial and temporal scheme for scheduling transmissions by which every source $\nu _ { S , i } \in$ $\boldsymbol { \mathcal { S } } ^ { \prime } ( \boldsymbol { \rho } _ { s } , \boldsymbol { \rho } _ { d } )$ can deliver data to at least $\rho _ { d } ( n , i ) \cdot n _ { d }$ destinations at rate of $\lambda _ { S , i }$ ; that is, there is a $T < \infty$ such that in every time interval (with unit seconds) $[ ( i - 1 ) \cdot T , i \cdot T ]$ , every node $\nu _ { S , i } \in S ^ { \prime } ( \rho _ { s } , \rho _ { d } )$ can send $T \cdot \lambda _ { \mathcal { S } , i }$ bits to at least its $\rho _ { d } ( n , i )$ - $n _ { d }$ destinations, where

$$
\lim _ {n \to \infty} \rho_ {s} (n) = \rho_ {s}; \lim _ {n \to \infty} \inf _ {v _ {\mathcal {S}, i} \in \mathcal {S} ^ {\prime} (\rho_ {s}, \rho_ {d})} \{\rho_ {d} (n, i) \} = \rho_ {d}.
$$

We call a multicast rate vector $\varLambda _ {  { \mathcal { S } } , n _ { d } } = ( \lambda _ {  { \mathcal { S } } , 1 } , \lambda _ {  { \mathcal { S } } , 2 } , . . . ,$ $\lambda _ { S , n _ { s } } )$ feasible if it is (1, 1)-feasible.

Based on a multicast rate vector, we can define the following three types of multicast throughput (MT).

$$
\begin{array}{l} - \text { Total   MT: } \Lambda_ {\mathcal {S}, n _ {d}} ^ {\mathrm{T}} (n) = \sum_ {v _ {\mathcal {S}, i} \in \mathcal {S} ^ {\prime} (1, 1)} \lambda_ {\mathcal {S}, i}. \\ - \text { Average   per - session   MT: } \Lambda_ {\mathcal {S}, n _ {d}} ^ {\mathrm{P}} (n) = \frac {1}{n _ {s}} \sum_ {v _ {\mathcal {S}, i} \in \mathcal {S} ^ {\prime} (1, 1)} \lambda_ {\mathcal {S}, i}. \\ - \text { Minimum   per - session   MT: } \Lambda_ {\mathcal {S}, n _ {d}} ^ {\mathrm{M}} (n) = \min _ {v _ {\mathcal {S}, i} \in \mathcal {S} ^ {\prime} (1, 1)} \lambda_ {\mathcal {S}, i}. \\ \end{array}
$$

Definition 2 (Achievable throughput) The aggregated multicast throughput $A _ { S , n _ { d } } ^ { \mathrm { T } } ( n ) = \sum _ { \nu _ { S , i } \in S ^ { \prime } ( 1 , 1 ) } \lambda _ { S , i }$ is achievable if there is a feasible rate vector ${ A _ { S , n _ { d } } } = ( \lambda _ { S , 1 } , . . . , \lambda _ { S , n _ { s } } )$ .

Similarly, we say the per-session throughput $A _ { S , n _ { d } } ^ { \mathrm { M } } ( n )$ (or $A _ { S , n _ { d } } ^ { \mathrm { P } } ( n ) )$ ) is achievable if the rate vector $\begin{array} { r } { A _ { S , n _ { d } } = ( \lambda _ { S , 1 } , . . . , } \end{array}$ $\lambda _ { S , n _ { s } } )$ is feasible.

In the following content, we focus on the achievable aggregated multicast throughput and minimum per-session multicast throughput. In addition, to simplify the description, we denote each multicast session $\mathcal { M } _ { \mathcal { S } , k }$ as $\mathcal { M } _ { k } .$ for $k = 1 , 2$ , $\ldots , n _ { s } ,$ when no confusion is made. Similarly, we denote the corresponding spanning set $\boldsymbol { { \mathcal U } } _ { \mathcal { S } k }$ , as $\mathcal { U } _ { k } = \{ u _ { k } \} \cup \mathcal { D } _ { k }$ ; where $u _ { k }$ is the source of $\mathcal { M } _ { k }$ and $\mathcal { D } _ { k } = \{ u _ { k _ { 1 } } , u _ { k _ { 2 } } , . . . , u _ { k _ { n _ { d } } } \}$ is the set of destinations of $\mathcal { M } _ { k }$ :

# 3 Multicast scheme

Since $\mathcal { N } _ { p } ( n )$ does not change its transmission scheme due to the presence of $\mathcal { N } _ { s } ( m )$ ; we assume it transmits by the classic multihop scheme similar to those in [1, 3, 5]. Of greater interest is how the secondary nodes transmit such that $\mathcal { N } _ { p } ( n )$ remains unaffected in terms of its specific requirement.

# 3.1 Multicast scheme for primary network

Due to the overwhelming priority to access the spectrum, $\mathcal { N } _ { p } ( n )$ can operate as if no $\mathcal { N } _ { s } ( m )$ were present. Hence, we can design the multicast scheme for $\mathcal { N } _ { p } ( n )$ as for the single ad hoc network. We will propose the scheme by modifying the nearest neighbor Manhattan multi-hop multicast routing scheme in [22].

# 3.1.1 Primary transmissions scheduling

We use a TDMA scheme to schedule transmissions in order to limit the number of simultaneous transmissions taking place, which in turn limits the interference. Specifically, we divide the region $\boldsymbol { A } _ { 1 }$ into square cells of area $a _ { p } = \log n / n .$ and divide the time into a sequence of $K ^ { 2 } ,$ , $K \geq 3$ successive slots. Each cell is activated during one out of $K ^ { 2 }$ slots, see detail in Fig. 1. A simple round-robin scheme is used for all transmitters in the same cell. At each transmission, a transmitter transmits with power $P \cdot a _ { p } ^ { \alpha / 2 } ,$ i.e.,

$$
P (v _ {i}) = P \cdot a _ {p} ^ {\alpha / 2}, \quad \text { for   all } v _ {i} \in \mathcal {V} _ {p} (n). \tag {1}
$$

# 3.1.2 Primary multicast routing

To ensure the feasibility of the our routing scheme (Algorithm 2), we need prove the following lemma. Lemma 1 Each primary cell has at least one primary node.

![](images/a48312f588bac914f8bb02cef78b0d4894f8b015e6a4d4af8fdbbe71e098ff13.jpg)



Fig. 1 Primary multicast scheme. The situation depicted represents the case $K = 3$ . Gray squares can transmit simultaneously. Note that around each gray square there is a silence region of squares that are prohibited to transmit in the given time slot. The long-dashed lines represent the edge in EST of a multicast session, where $\nu _ { 0 }$ is the source and $\nu _ { 1 } - \nu _ { 8 }$ are the destinations. The dotted lines represent the horizontal and vertical paths for each edge. The solid lines between nodes are the actual route, for instance the route from $\nu _ { 2 }$ to $\nu _ { 8 }$ by multiple hops

Proof Let N denote the number of nodes in a primary cell, then N follows a Poisson distribution with $\lambda = n \cdot a _ { p } = \log$ $n ,$ then $\operatorname* { P r } ( N = 0 ) = e ^ { - \lambda } = 1 / n$ . Thus, the probability that there is at least one cell having no node is upper bounded by $\left( n / \log n \right) \operatorname* { P r } ( N = 0 ) = 1 / \log n { \longrightarrow } 0$ ; where union bounds and the fact that there are H(n /logn) cells are used.

For each multicast session $\mathcal { M } _ { k }$ ; based on its spanning set $\mathcal { U } _ { k } = \{ u _ { k } \} \cup \mathcal { D } _ { k }$ ; where $u _ { k }$ is the source and $\mathcal { D } _ { k }$ is the set of destinations of $\mathcal { M } _ { k } ,$ we can build the Euclidean spanning tree, denoted as $\operatorname { E S T } ( \mathcal { U } _ { k } ) )$ , by Algorithm 1 proposed in [3]. Here, an Euclidean spanning tree represents a spanning tree measured with the Euclidean metric [21]. Furthermore, we give Algorithm 2 to construct the multicast routing tree $\mathcal { M T } ( \mathcal { U } _ { k } )$ based on $\mathrm { E S T } ( { \cal U } _ { k } )$ Þ.

# 3.2 Priority guarantee parameter

We can use a triple $( F , K , P )$ to describe a given multicast scheme, where $F$ denotes the multicast routing scheme, K means that a $K ^ { 2 } – \mathrm { T D M A }$ scheme is adopted, and P is the transmitting power of each scheduled transmitter. Under a given routing scheme $F ^ { p } ( \mathrm { o r } F ^ { s } )$ , we define a set of ordered-pairs (or directed links) in $\nu _ { p } ( n )$ (or $\nu _ { s } ( m ) )$ , denoted by $\Xi _ { p } ( F ^ { p } ) \subseteq \mathcal { E } _ { p } ( n ) \mathrm { ~ } ( \mathrm { o r ~ } \Xi _ { s } ( F ^ { s } ) \subseteq \mathcal { E } _ { s } ( m ) )$ , in which each ordered-pairs can communicate with a direct link (one-hop link). All links in $\Xi _ { p } ( F ^ { p } )$ (or $\Xi _ { s } ( F ^ { s } ) )$ will be periodically scheduled by a $K ^ { 2 } { \cdot } \mathrm { T D M A }$ scheme, under which one scheduling period can be indexed as a set of time slots $\mathcal { T } = \{ 0 , 1 , 2 , . . . , K ^ { 2 } - 1 \}$ . Any time slot, say s, can be mapped into a certain element of the set T by a modulo operation: smod $K ^ { 2 }$ . Hence, in the following analysis, we can only consider the time slots in T . For any time slot $\tau \in \mathcal { T }$ ; we accordingly define the set of links in $\Xi _ { p } ( F ^ { p } )$ (or $\Xi _ { s } ( F ^ { s } ) )$ that are scheduled in s as $\Xi _ { p } ( F ^ { p } , \tau )$ $( \mathrm { o r } \Xi _ { s } ( F ^ { s } , \tau ) . )$

![](images/0522d0e8f51eb02bd63261302bc5d9e8a063069cc792994e02511609c0a1b88b.jpg)



Fig. 2 Secondary communication-pairs routing scheme. The situation depicted represents the case $K = 3$

# Algorithm 1 Construction of EST

Input: The spanning set $\boldsymbol { \mathcal { U } } _ { k } .$

Output: ESTðUkÞ.

1: In the initial state, allnodes of $\mathcal { U } _ { \mathcal { S } , k }$ are isolated, then there are $n _ { d }$ ? 1 connected components.   
2. for $i = 1 \colon n _ { d }$ do   
3. Partition the deployment region $\mathcal { A } _ { 1 } = [ 0 , 1 ] ^ { 2 }$ into at most $n _ { d } + 1$ - i square cells, each with side   
length $1 / \lfloor { \sqrt { n _ { d } + 1 - i } } \rfloor$ ;   
4. Find a cell that contains two nodes of $\mathcal { U } _ { k }$ that are from two different connected components. By   
connecting the pair of nodes, we merge the two connected components.   
5. end for

# Algorithm 2 Primary multicast routing scheme $F$

Input: $\mathrm { E S T } ( { \mathscr { U } } _ { k } )$ .

Output: Multicast routing tree $\mathcal { M T } ( \mathcal { U } _ { k } ) .$ .

1. For each link $\nu _ { i } \nu _ { j }$ in $\mathrm { E S T } ( { \mathscr { U } } _ { k } )$ ; connect $\nu _ { i }$ and $\nu _ { j }$ using Manhattan routing as follows:   
Denote the intersection point of the horizontal line through $\nu _ { i }$ and the vertical line through $\nu _ { j }$ by the   
inflexion vij. $\nu _ { i j } .$   
Define line segments $\nu _ { i } \nu _ { i j }$ and $\nu _ { i j } \nu _ { j }$ as the horizontal path $\mathcal { H P } _ { i j }$ and vertical path $\gamma \mathcal { P } _ { i j } ,$ respectively.   
Choose a node in each cell passed through by $\mathcal { H P } _ { i j }$ and $\mathcal { V } \mathcal { P } _ { i j }$ at random, and connect each node only   
with its neighbors in the two adjacent cells to realize the route from vi to $\nu _ { j } ,$ see Fig. 1.   
2. The resulting structure could contain some redundant edges. We merge the same edges, and remove those   
circles that have no impact on the connectivity of ESTðUkÞ; then we obtain the final multicast routing   
tree $\mathcal { M T } ( \mathcal { U } _ { k } )$

# 3.2.1 Throughput decrement radio (TDR)

The throughput decrement ratio (TDR) is an intuitive metric, denoted by $\nabla ( F , K , P )$ ; that measures the ratio of the reduced throughput of $\mathcal { N } _ { p } ( n )$ to that of $\mathcal { N } _ { p } ( n )$ in absence of the secondary network $\mathcal { N } _ { s } ( m )$ : Since the bottlenecks determine the throughput of the whole network, we define TDR as

$$
\nabla (F, K, P) =
$$

$$
\lim _ {n \rightarrow \infty} \frac {\inf \left\{R _ {p} \left(v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau\right) \mid \left\langle v _ {i} ^ {p} , v _ {j} ^ {p} \right\rangle \in \Xi_ {p} (F , \tau) , f o r a l l \tau \in \mathcal {T} \right\}}{\inf \left\{\tilde {R} _ {p} \left(v _ {i} ^ {p} , v _ {j} ^ {p}; \tau\right) \mid \left\langle v _ {i} ^ {p} , v _ {j} ^ {p} \right\rangle \in \Xi_ {p} (F , \tau) , f o r a l l \tau \in \mathcal {T} \right\}}, \tag {2}
$$

where $\nabla ( F , K , P ) \in ( 0 , 1 ]$ and $\tilde { R } _ { p } ( \nu _ { i } ^ { p } , \nu _ { j } ^ { p } ; \tau )$ denotes the rate of the link $< \nu { ^ { p } } _ { i } , \nu { ^ { p } } _ { j } >$ [ in the time slot s when $\mathcal { N } _ { s } ( m )$ is absent, i.e.,

$$
\tilde {R} _ {p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) = \log \left(1 + \frac {S (v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau)}{N _ {0} + I _ {p p} (v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau)}\right). \tag {3}
$$

Given a $\nabla \in ( 0 , 1 ]$ as the lower bound of TDR, our challenge is to design the multicast scheme for $\mathcal { N } _ { s } ( m )$ by which the maximum throughput can be achieved under the constraint of $\nabla ( F , K , P ) \ge \nabla$ :

# 3.2.2 Interference intensity factor (IIF)

For a given multicast scheme, we devise another more concise and conservative metric to measure the intensity of the interference to the primary users produced by secondary users. It is defined as

$$
\Delta (F, K, P) =
$$

$$
\lim _ {n \rightarrow \infty} \sup \left\{\frac {I _ {s p} \left(v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau\right)}{I _ {p p} \left(v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau\right)} \mid \langle v _ {i} ^ {p}, v _ {j} ^ {p} \rangle \in \Xi_ {p} (F, \tau), f o r a l l \tau \in \mathcal {T} \right\}, \tag {4}
$$

where $\Delta ( F , K , P ) \in ( 0 , \infty ]$ . Given a $\Delta \in [ 0 , \infty )$ acting as the upper bound of IIF, our main task is to design the multicast scheme for SaN to achieve the optimal throughput under the constraint of $\Delta ( F , K , P ) \le \Delta$ :

# 3.2.3 Relations between IIF and TDR

Given the definitions of IIF and TDR, a question arises how to determine the upper bound of IIF, say D, based on a given lower bound of TDR, say r.

Lemma 2 For a given multicast scheme $( F , K , P )$ and a lower bound of TDR, denoted by $\nabla \in ( 0 , 1 ]$ , we can choose the upper bound of IIF as

$$
\Delta = (1 + \delta (F, K, P)) \cdot \left(\frac {1}{\overline {{\nabla}}} - 1\right) \tag {5}
$$

such that $\nabla ( F , K , P ) \ge \nabla$ ; where

$$
\delta (F, K, P) =
$$

$$
\lim _ {n \rightarrow \infty} \inf \left\{\frac {N _ {0}}{I _ {p p} \left(v _ {i} ^ {p} , v _ {j} ^ {p} ; \tau\right)} \mid \langle v _ {i} ^ {p}, v _ {j} ^ {p} \rangle \in \Xi_ {p} (F, \tau), f o r a l l \tau \in \mathcal {T} \right\}. \tag {6}
$$

Proof Without loss of generality, we assume that

$$
\begin{array}{c} R _ {p} (v _ {1} ^ {p}, v _ {2} ^ {p}; \tau_ {1}) = \inf \{R _ {p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \mid \langle v _ {i} ^ {p}, v _ {j} ^ {p} \rangle \in \Xi_ {p} (F, \tau), \\ \text { for   all } \tau \in \mathcal {T} \}, \end{array}
$$

where $\langle \nu _ { 1 } ^ { p } , \nu _ { 2 } ^ { p } \rangle \in \Xi _ { p } ( F , \tau _ { 1 } )$ ; and assume that

$$
\begin{array}{l} \tilde {R} _ {p} (v _ {3} ^ {p}, v _ {4} ^ {p}; \tau_ {2}) = \inf \{\tilde {R} _ {p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \mid \langle v _ {i} ^ {p}, v _ {j} ^ {p} \rangle \in \Xi_ {p} (F, \tau), \\ \text { for   all } \tau \in \mathcal {T} \}, \end{array}
$$

where $\langle \nu _ { 3 } ^ { p } , \nu _ { 4 } ^ { p } \rangle \in \Xi _ { p } ( F , \tau _ { 2 } )$ . Thus, according to Eq. (2), it holds that

$$
\nabla (F, K, P) = \lim _ {n \rightarrow \infty} \frac {R _ {p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\tilde {R} _ {p} \left(v _ {3} ^ {p} , v _ {4} ^ {p} ; \tau_ {2}\right)} \geq \lim _ {n \rightarrow \infty} \frac {R _ {p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\tilde {R} _ {p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}. \tag {7}
$$

By the definition of D, Eqs. (5), and (6), we have that

$$
\lim _ {n \rightarrow \infty} \frac {R _ {p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\tilde {R} _ {p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)} = \lim _ {n \rightarrow \infty} \frac {\log \left(1 + \frac {S \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{N _ {0} + I _ {s p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right) + I _ {p p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}\right)}{\log \left(1 + \frac {S \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{N _ {0} + I _ {p p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}\right)} \tag {8}
$$

$$
\geq \lim _ {n \rightarrow \infty} \frac {\log \left(1 + \frac {S \left(\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1}\right)}{N _ {0} + (1 + \Delta) \cdot I _ {p p} \left(\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1}\right)}\right)}{\log \left(1 + \frac {S \left(\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1}\right)}{N _ {0} + I _ {p p} \left(\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1}\right)}\right)} \tag {9}
$$

$$
\geq \lim _ {n \rightarrow \infty} \frac {\log \left(1 + \frac {S \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\left(1 + \delta (F , K , P) + \Delta\right) \cdot I _ {p p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}\right)}{\log \left(1 + \frac {S \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\left(1 + \delta (F , K , P)\right) \cdot I _ {p p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}\right)} \tag {10}
$$

$$
= \lim _ {n \rightarrow \infty} \frac {\log \left(1 + \frac {\nabla \cdot S \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\left(1 + \delta (F , K , P)\right) \cdot I _ {p p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}\right)}{\log \left(1 + \frac {S \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}{\left(1 + \delta (F , K , P)\right) \cdot I _ {p p} \left(v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1}\right)}\right)} \tag {11}
$$

By the Bernoulli’s inequality: for any $x > - 1 , 1 + r x \ge$ $( 1 + x ) ^ { r }$ when $0 < r < 1$ , we have

$$
\frac {\log \left(1 + \frac {\nabla \cdot S (v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1})}{(1 + \delta (F , K , P)) \cdot I _ {p p} (v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1})}\right)}{\log \left(1 + \frac {S (v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1})}{(1 + \delta (F , K , P)) \cdot I _ {p p} (v _ {1} ^ {p} , v _ {2} ^ {p} ; \tau_ {1})}\right)}
$$

$$
\geq \frac {\log \left(1 + \frac {S (\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1})}{(1 + \delta (F , K , P)) \cdot I _ {p p} (\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1})}\right) ^ {\nabla}}{\log \left(1 + \frac {S (\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1})}{(1 + \delta (F , K , P)) \cdot I _ {p p} (\nu_ {1} ^ {p} , \nu_ {2} ^ {p} ; \tau_ {1})}\right)} = \nabla \tag {12}
$$

Hence, combining Eqs. (7), (11), and 12), we can prove the lemma.

# 3.3 Multicast scheme for secondary network

For $\mathcal { N } _ { s } ( m )$ ;the main issue is to design a scheme to achieve the throughput as much as possible under the condition that $\Delta ( F , K , P ) \leq \Delta .$ ; where D is a given upper bound of IIF. The key techniques are two-fold. One is to set preservation regions [23] through which any routing paths in $\mathcal { N } _ { s } ( m )$ can not pass. The other is to limit the transmitting power of secondary users.

# 3.3.1 Secondary transmissions scheduling

We also use TDMA scheme to schedule transmissions in $\mathcal { N } _ { s } ( m )$ . Similarly, we divide the region $\mathcal { A } _ { 1 } = [ 0 , 1 ] \times [ 0 , 1 ]$ into square cells (called secondary cells) of area $a _ { s } =$ logm/m. Similar to Lemma 1, we can ensure that each secondary cell has at least one secondary node. The difference from $\mathcal { N } _ { p } ( n )$ is to divide the time into a sequence of $M \cdot K ^ { 2 }$ successive slots, where K is determined by the transmission scheduling of $\mathcal { N } _ { p } ( n )$ and M $( 3 \leq M \leq K )$ is a constant. Each cell except one in preservation region is activated for successive M slots during one out of $M \cdot K ^ { 2 }$ slots. At each transmission, a transmitter transmits with power $\boldsymbol { P } \cdot \boldsymbol { \theta } ( \boldsymbol { n } ) \cdot \boldsymbol { a } _ { s } ^ { \alpha / 2 }$ , i.e.,

$$
P (v _ {i}) = P \cdot \theta (n) \cdot a _ {s} ^ {\alpha / 2} \quad \text { for   all } v _ {i} \in \mathcal {V} _ {s} (m), \tag {13}
$$

where $\theta ( n )$ is power regulatory factor and $\begin{array} { r } { \operatorname* { l i m } _ { n \to \infty } \theta ( n ) = } \end{array}$ $\theta , \theta$ is a constant depending on the given $\Delta$ as defined in Theorem 2.

# 3.3.2 Preservation region

If K is an odd, for any primary node $\nu ^ { p } \in \mathcal N _ { p } ( n )$ ; we define its preservation region as a square consisting of $K ^ { 2 }$ secondary cells, with $\nu ^ { p }$ at the center cell. If K is an even, we define the preservation region with the same size as K is an odd, but with the primary node at any one of the four cells intersecting on the center location of the preservation region. Without loss of the generality, we focus on the case that K is an odd.

# 3.3.3 Secondary multicast routing

Unlike in $\mathcal { N } _ { p } ( n )$ ; some secondary cells in $\mathcal { N } _ { s } ( m )$ are covered with preservation regions or with the closed regions encompassed by the clusters of preservation regions. We call them non-served cells. Denote the set of all secondary nodes in the non-served cells as $\mathcal { V } _ { s } ^ { \prime } ( m )$ . Then, for each multicast session $\mathcal { M } _ { k }$ and its spanning set $\mathcal { U } _ { k }$ ; we can define the available spanning set as

$$
\overline {{{\mathcal {U}}}} _ {k} = \left\{ \begin{array}{l l} \emptyset , & \text { when   the   source } u _ {k} \in \mathcal {V} _ {s} ^ {\prime} (m); \\ \mathcal {U} _ {k} - \mathcal {D} _ {k} \cap \mathcal {V} _ {s} ^ {\prime} (m), & \text { otherwise. } \end{array} \right. \tag {14}
$$

For each multicast session $\mathcal { M } _ { k }$ in $\mathcal { N } _ { s } ( m )$ ; using a similar method to Algorithm 1, we can build EST $( \hat { U } _ { k } )$ based on the available spanning set ${ \bar { \mathcal { U } } } _ { k } .$ . Furthermore, based on $\mathrm { E S T } ( \bar { \mathcal { U } } _ { k } )$ ; we can build the multicast tree of $\mathcal { M } _ { k }$ by Algorithm 3.

Algorithm 3 Secondary multicast routing scheme $\bar { F }$ 

<table><tr><td>Input: EST(URk) and all preservation regions.</td></tr><tr><td>Output: The multicast routing tree MT(URk).</td></tr><tr><td>1. For each link vi→vj in EST(URk), construct the routing between viand vj by using the followingmethod:(1) Use a similar method to Step 1 of Algorithm 2 to obtain the horizontal path HPij and vertical pathVPij.(2) Construct the detour-horizontal path and detour-vertical path by using the following method:When the HPij (or VPij) collides with a preservation region, the path detours the preservation regionalong its boundary cell, see Fig. 2. The resulting path is denoted as HPCij (or VPCij). The shorter detour-path can be selected by use of the location of primary users.(3) Choose randomly a node in each cell passed by HPij and VPCij, and connect nodes from adjacentcells to realize the routing from vi to vj.</td></tr><tr><td>2. Use a similar method to Step 2 of Algorithm 2 to obtain the final multicast routing tree MT(URk).</td></tr></table>

# 4 Main results

For $\mathcal { N } _ { p } ( n )$ ; besides addressing the asymptotic throughput, we need consider how to guarantee the priority defined by its specific requirement. For $\mathcal { N } _ { s } ( m )$ ;we expect to derive the optimal throughput in order sense depending on the given constant r.

# 4.1 Asymptotic throughput for primary network

Firstly, we present the following result for $\mathcal { N } _ { p } ( n )$ :

Theorem 1 The achievable per-session multicast throughput for the primary network is w. $h . p .$ , of order

$$
T _ {p} ^ {\mathrm{M}} (n) = \left\{ \begin{array}{l l} \Omega \left(\frac {1}{\log n}\right) & \text { when   } n _ {s} = O \left(\frac {\log n}{\phi (n , n _ {d})}\right) \\ \Omega \left(\frac {1}{n _ {s} \cdot \phi (n , n _ {d})}\right) & \text { when   } n _ {s} = \Omega \left(\frac {\log n}{\phi (n , n _ {d})}\right) \end{array} \right.
$$

The achievable aggregated multicast throughput for the primary network is w. $h . p .$ , of order

$$
T _ {p} ^ {\mathrm{A}} (n) = \left\{ \begin{array}{l l} \Omega \left(\frac {n _ {s}}{\log n}\right) & \text { when   } n _ {s} = O \left(\frac {\log n}{\phi (n , n _ {d})}\right) \\ \Omega \left(\frac {1}{\phi (n , n _ {d})}\right) & \text { when   } n _ {s} = \Omega \left(\frac {\log n}{\phi (n , n _ {d})}\right) \end{array} \right.
$$

Here,

$$
\phi (n, n _ {d}) = \left\{ \begin{array}{l l} \Theta \left(\sqrt {\frac {n _ {d} \cdot \log n}{n}}\right) & \text { when } n _ {d} = O \left(\frac {n}{\log n}\right) \\ \Theta (1) & \text { when } n _ {d} = \Omega \left(\frac {n}{\log n}\right) \end{array} \right. \tag {15}
$$

As a by-product, our primary multicast scheme can also be applied to the single ad hoc networks, because $\mathcal { N } _ { p } ( n )$ 号 operates as if $\mathcal { N } _ { s } ( m )$ does not exist.

# 4.2 Priority of primary network

To ensure the priority of $\mathcal { N } _ { p } ( n )$ ; we necessarily endow $\mathcal { N } _ { p } ( n )$ with the right to determine the lower bound of TDR, denoted as $\nabla ,$ , and must design the corresponding scheme to satisfy the constraint that $\nabla ( F , K , P ) \ge \nabla$ :

Theorem 2 For a given a constant $\nabla \in ( 0 , 1 ]$ , we can ensure that $\nabla ( F , K , P ) \ge \nabla$ by using the following setting: Choose the power regulatory factor h(n) for the secondary users, defined in $E q .$ . (13), such that lim $\theta ( n ) = \theta \leq \Delta$ - $\underline { { C _ { 1 } ( K , \boldsymbol { \alpha } ) } }$ ; where n!1 $\frac { 1 } { C _ { 2 } ( K , \alpha ) }$

$$
C _ {1} (K, \alpha) = \frac {1}{K ^ {2} (K - 2) ^ {\alpha - 2}} \left(\frac {2}{(\alpha - 1) (K - 2)} + \frac {1}{(\alpha - 2)}\right)
$$

$$
C _ {2} (K, \alpha) = \frac {2 ^ {\alpha}}{K ^ {2} (K - 1) ^ {\alpha - 2}} \left(\frac {1}{(\alpha - 2)} + \frac {K + 1}{(\alpha - 1) (K - 1)}\right) \tag {16}
$$

and Dis obtained by Eq. (5) based on the given $\nabla .$

# 4.3 Asymptotic throughput for secondary network

For $\mathcal { N } _ { s } ( n )$ ; we only care its asymptotic throughput in order sense.

Theorem 3 For a $\Delta \geq 0$ based on the given lower bound of TDR, i.e., $\nabla \in \mathsf { \Gamma } ( 0 )$ , 1], the per-session multicast throughput

$$
T _ {s} ^ {\mathrm{M}} (m) = \left\{ \begin{array}{l l} \Omega \left(\frac {\theta (n)}{\log m}\right) & \text { when } m _ {s} = O \left(\frac {\log m}{\phi (m , m _ {d})}\right) \\ \Omega \left(\frac {\theta (n)}{m _ {s} \cdot \phi (m , m _ {d})}\right) & \text { when } m _ {s} = \Omega \left(\frac {\log m}{\phi (m , m _ {d})}\right) \end{array} \right.
$$

is achievable. The aggregated multicast throughput

$$
T _ {s} ^ {\mathrm{A}} (m) = \left\{ \begin{array}{l l} \Omega \left(\frac {\theta (n) \cdot m _ {s}}{\log m}\right) & \text { when } m _ {s} = O \left(\frac {\log m}{\phi (m , m _ {d})}\right) \\ \Omega \left(\frac {\theta (n)}{\phi (m , m _ {d})}\right) & \text { when } m _ {s} = \Omega \left(\frac {\log m}{\phi (m , m _ {d})}\right) \end{array} \right.
$$

is achievable, where lim $\begin{array} { r } { \theta ( n ) = \Delta \cdot \frac { C _ { 1 } ( K , \alpha ) } { C _ { 2 } ( K , \alpha ) } } \end{array}$ and

$$
\phi (m, m _ {d}) = \left\{ \begin{array}{l l} \Theta \left(\sqrt {\frac {m _ {d} \cdot \log m}{m}}\right) & \text { when   } m _ {d} = O \left(\frac {m}{\log m}\right) \\ \Theta (1) & \text { when   } m _ {d} = \Omega \left(\frac {m}{\log m}\right) \end{array} \right.
$$

# 5 Throughput analysis

Given a lower bound of TDR as $\nabla \in ( 0 , 1 ]$ , we will first derive the specific total rate depending on r that all cells can sustain, which is used in conjunction with the number of multicast flows passing through each cell to obtain the multicast throughput for $\mathcal { N } _ { p } ( n )$ and $\mathcal { N } _ { s } ( m )$ .

# 5.1 Technical lemmas and preliminaries

Before proving main results, we recall some useful lemmas.

Lemma 3 (Chebyshev’s Inequality) For a variable $X ,$

$$
\operatorname * {P r} (| X - \mu | \geq \varepsilon) \leq \frac {\operatorname{Var} (X)}{\varepsilon^ {2}},
$$

where $\mu = E ( X )$ , Var(X) is the variance of X, and $\varepsilon > 0$ .

Lemma 4 [5] Let X be a Poisson random variable with parameter k. Then

$$
\operatorname * {P r} (X \geq x) \leq e ^ {- \lambda} (e \lambda) ^ {x} / x ^ {x}, \quad \text { for } x > \lambda .
$$

Lemma 5 [3] For any set U of $n _ { d } + 1$ nodes randomly placed in $\boldsymbol { A } _ { 1 }$ ; the total length of ESTðUÞ obtained by Algorithm 1 is at most $2 { \sqrt { 2 } } { \sqrt { n _ { d } } }$ :

In the Poisson Boolean model $B ( \lambda , r )$ [24], the nodes are distributed according to a Poisson point process of intensity k in $\mathbb { R } ^ { 2 }$ . We associate with each node a closed disk with Rradius r. The region is thus partitioned into two regions: the occupied region $\mathbb { R } _ { \mathrm { o } } ^ { 2 } ,$ which is one covered by the disks, and Rthe vacant region $\mathbb { R } _ { \mathrm { v } } ^ { 2 }$ which is the complement of the Roccupied region. Two disks are directly connected if they overlap. Two disks are connected if there exists a sequence of directly connected disks between them. Define a cluster as a set of disks such that any two disks in the cluster are connected. Define the set of all clusters in the model $B ( \lambda , r )$ as $\mathcal { C } ( \lambda , r ) = \{ C _ { i } \mathrm { { i } s }$ any cluster in $B ( \lambda , r ) ]$ g. Define the number of disks in the cluster $C _ { i }$ as a random variable $N ( C _ { i } )$ .

# 5.1.1 Associated graph

We can associate with the random model $B ( \lambda , r )$ the graph $\mathcal { G } ( \lambda , r )$ by associating a vertex to each node of $B ( \lambda , r )$ and an edge with each direct connection in $B ( \lambda , r ) . ~ \mathcal { G } ( \lambda , r )$ is called the associated graph of $B ( \lambda , r )$ . The two models $B ( \lambda , r )$ and $B ( \lambda _ { 0 } , r _ { 0 } )$ lead to the same associated graph, namely $\mathcal { G } ( \lambda , r ) = \mathcal { G } ( \lambda _ { 0 } , r _ { 0 } )$ if $\lambda _ { 0 } r _ { 0 } ^ { 2 } = \lambda r ^ { 2 }$ . As result, the graph properties of $B ( \lambda , r )$ depend only on one parameter k $r ^ { 2 }$ proportional to the average node degree $\pi \lambda \bar { r ^ { 2 } }$ .

# 5.1.2 Percolation probability

The percolation probability, denoted as p; is one that a given node belongs to a cluster with an infinite number of nodes. With C denoting the cluster containing the given node, the percolation probability is thus defined $\mathrm { a s p } ( \lambda , r ) = \mathfrak { p } ( \lambda r ^ { 2 } ) = \operatorname* { P r } _ { \lambda , r } ( | C | = \infty ) = \operatorname* { P r } _ { \mathfrak { p } } ( | C | = \infty )$ . k;r p

Definition 3 (Critical Percolation Threshold) We call ${ \mathfrak { p } } _ { c }$ the critical percolation threshold of the Poisson Boolean model in $\mathbb { R } ^ { \bar { 2 } }$ ; when

$$
\mathfrak {p} _ {c} = (\lambda r ^ {2}) _ {c} = \sup \{\lambda r ^ {2} | \mathfrak {p} (\lambda r ^ {2}) = 0 \}. \tag {17}
$$

Obtaining the exact value of $( \lambda r ^ { 2 } ) _ { c }$ is still an open problem, numerical results show that it is close to 1.43. Moreover, it can be proved that the percolation threshold in $\mathbb { R } ^ { 2 }$ is such that $0 < { \mathfrak { p } } _ { c } \leq 8 \ln { 2 }$ [25].

According to Definition 3, we can recall the following lemma (Meester and Roy [24]).

Lemma 6 For the Poisson Boolean model $B ( \lambda , r )$ in $\mathbb { R } ^ { 2 }$ ; $i f \lambda r ^ { 2 } < { \mathfrak { p } } _ { c } ,$ ; then

$$
\operatorname * {P r} (\sup _ {C _ {i} \in \mathcal {C}} \{N (C _ {i}) \} <   \infty) = 1,
$$

where ${ \mathfrak { p } } _ { c }$ is the critical percolation threshold of the Poisson Boolean model in $\mathbb { R } ^ { 2 }$ and $\mathcal { C } ( \lambda , r )$ is described simply as $\mathcal { C } .$ :

Based on Lemma 6, we propose a lemma to show that all clusters of preservation regions are bounded.

Lemma 7 When $\begin{array} { r } { n = o \left( \frac { m } { \log { m } } \right) } \end{array}$ any cluster of preservation regions has at most a constant l preservation regions w.h.p, where ${ \mathfrak { p } } _ { c }$ is the critical percolation threshold of the Poisson Boolean model in $\mathbb { R } ^ { 2 }$ ; m and n are the density of primary and secondary networks respectively.

Proof Firstly, we consider a Poisson Boolean model $B ( \lambda , r )$ ; where $\begin{array} { r } { r = \frac { K + 1 } { 2 } \sqrt { 2 a _ { s } } } \end{array}$ and $\lambda = n$ . Since the associated graphs $\mathcal { G } ( \lambda _ { 0 } , r _ { 0 } ) = \bar { \mathcal { G } } ( \lambda , r )$ when $\lambda _ { 0 } \cdot r _ { 0 } ^ { 2 } = \lambda \cdot r ^ { 2 }$ . Hence, the Poisson Boolean model $B ( \lambda , r )$ is equivalent to $B ( \lambda _ { 0 } , r _ { 0 } )$ in terms of the connectivity, where $r _ { 0 } = 1$ and $\lambda _ { 0 } =$ $( K { + } 1 ) ^ { 2 }$ $\begin{array} { r } { n = o \left( \frac { m } { \log m } \right) } \end{array}$ we have is a con $ \lambda \cdot r ^ { 2 } =$ $\begin{array} { r } { \lambda _ { 0 } ^ { ^ { \angle } } \cdot r _ { 0 } ^ { 2 } = \frac { ( K + 1 ) ^ { 2 } } { 2 } \cdot n \cdot a _ { s }  0 . } \end{array}$ 2 ${ \mathfrak { p } } _ { c }$ $( 0 , 8 \mathrm { l n } 2 ) , \lambda \cdot \bar { r } ^ { 2 } < \mathfrak { p } _ { c } . \mathbf { B } \mathbf { y }$ Lemma 6, the size of any cluster is at most a constant l. Since a disk of radius r contains a square preservation region, it is also true for all clusters of preservation regions.

# 5.2 Throughput of primary network

For the primary network $\mathcal { N } _ { p } ( n )$ ; we firstly have

Lemma 8 Given $~ a ~ \Delta ,$ let lim $\begin{array} { r } { { 1 } _ { n \longrightarrow \infty } \theta ( n ) = \theta \le \Delta \cdot \frac { C _ { 1 } ( K , \alpha ) } { C _ { 2 } ( K , \alpha ) } , } \end{array}$ each primary cell can sustain traffic with a constant rate of RpðDÞ ¼ 1K2 log 1 þ 52N =Pþ8ð1þDÞC ðK;aÞ $\begin{array} { r } { R _ { p } ( \Delta ) = \frac { 1 } { K ^ { 2 } } \mathrm { l o g } \Big ( 1 + \frac { 5 ^ { - \frac { \alpha } { 2 } } } { N _ { 0 } / P + 8 ( 1 + \Delta ) C _ { 1 } ( K , \alpha ) } \Big ) } \end{array}$ where the constants $C _ { 1 } ( K , \alpha )$ and $C _ { 2 } ^ { \setminus } ( K , \alpha )$ are defined in $E q .$ (16).

The next lemma derives the number of multicast flows that each primary cell should carry. To facilitate the expression, we define a sequence of the sets of directed edges: $\Pi _ { k } = \{ e _ { i j } | \langle \nu _ { i } , \nu _ { j } \rangle \in \operatorname { E S T } ( \mathcal { U } _ { k } ) \}$ for $k = 1 , 2 , . . . , n _ { s }$ .

Lemma 9 Under the multicast routing scheme F described in Algorithm 2, the number of the multicast flows passing through each primary cell is at most

$$
\operatorname{Load} _ {p} (n) = \left\{ \begin{array}{l l} O (\log n) & \text { when   } n _ {s} = O \bigg (\frac {\log n}{\phi (n , n _ {d})} \bigg) \\ O (n _ {s} \cdot \phi (n, n _ {d})) & \text { when   } n _ {s} = \Omega \bigg (\frac {\log n}{\phi (n , n _ {d})} \bigg), \end{array} \right.
$$

where $\phi ( n , n _ { d } )$ is defined as $E q .$ (15).

Combining Lemmas 8 and 9, we obtain Theorem 1.

# 5.3 Priority for primary network

Because there exists no communications between the primary and secondary networks, the load of each primary cell is independent of $\mathcal { N } _ { s } ( m )$ . That is, the decrement of the throughout for $\mathcal { N } _ { p } ( n )$ only depends on the reduction of the rate that each primary cell can sustain. Then, based on Lemmas 2 and 8, Theorem 2 can be straightforwardly proved.

# 5.4 Throughput of secondary network

Next, we consider the multicast throughput of $\mathcal { N } _ { s } ( m )$ under the constraint that $\nabla ( F , K , P ) \ge \nabla$ ; where r is a given lower bound of TDR determined by $\mathcal { N } _ { p } ( n )$ . The main difference from the multicast scheme for $\mathcal { N } _ { p } ( n )$ results from the preservation regions. Like $\mathcal { N } _ { p } ( n ) , \mathcal { N } _ { s } ( m )$ adopts the Manhattan routing, however, their Manhattan paths may be blocked by a preservation region. In this case, they have to avoid the preservation region or possibly the cluster of preservation regions. We consider the throughput of $\mathcal { N } _ { s } ( m )$ by comprehensively taking account of the rate and relay burden of each secondary cell.

Lemma 10 Each secondary cell can sustain traffic with a rate of order $\Omega ( \theta ( n ) )$ , where h(n) is the power regulatory factor defined in $E q .$ . (13).

Unlike in $\mathcal { N } _ { p } ( n )$ ; the secondary cells can be classified into three kinds based on the preservation regions. The first kind are non-served cells, i.e., those covered by preservation regions or by the closed regions encompassed with preservation regions clusters. The second kind are border cells that are adjacent to the preservation regions but not the non-served cells. A cell is called normal cell if it does not belong to the other two kinds of cells mentioned above. The border cells and normal cells are both called served cells. If the source of the multicast session is in a nonserved cell, we call the session non-served session and call the source non-served source. We call the destinations contained in non-served cells non-served terminals.

Lemma 11 The sum area of the non-served cells, denoted as $S ^ { \prime } ( m )$ , is at most $K ^ { 2 } \cdot \mu \cdot n \cdot { \frac { \log m } { m } } .$ 二 where the constant l is the maximum size of the clusters of preservation regions.

Proof For any cluster with size $\mu _ { i } ,$ it is sure that there exists a square with width of $\mu _ { i } { \cdot } K { \cdot } \sqrt { a _ { s } }$ that contains completely all the $\mu _ { i }$ preservation regions and the nonserved cells encompassed by them. Thus, the sum area of the non-served cells produced by li preservation regions $S ^ { \prime } ( m , \mu _ { i } ) \leq \mu _ { i } ^ { 2 } \cdot K ^ { 2 } \cdot a _ { s }$ . Hence, $S ^ { \prime } ( m ) \leq S _ { \ m a x } ^ { \prime } ,$ where S0 max is the optimum of the following optimization problem.

$$
\max S ^ {\prime} = K ^ {2} \cdot a _ {s} \cdot \sum_ {i = 1} ^ {n} \mu_ {i} ^ {2}
$$

$$
\text { s.t. } \sum_ {i = 1} ^ {n} \mu_ {i} = n, \quad 1 \leq \mu_ {i} \leq \mu , \quad i = 1, 2, \dots , n.
$$

s easy to derive that ; which completes the $\begin{array} { r } { S _ { m a x } ^ { \prime } = \frac { n } { \mu } \cdot \mu ^ { 2 } \cdot K ^ { 2 } \cdot a _ { s } = K ^ { 2 } \mu \cdot n } \end{array}$ $\frac { \log m } { m }$

Lemma 12 Denote the number of multicast sessions in $\mathcal { N } _ { s } ( m ) a s m _ { s } = \omega ( 1 )$ . Then, there exists $\rho _ { s } ^ { \prime } ( m ) = o ( 1 )$ such that the number of non-served sessions is w.h.p., at most $\rho _ { s } ^ { \prime } ( m ) \cdot m _ { s }$ .

Next, we consider the number of non-served terminals, denoted as $\zeta ^ { \prime } { } _ { d } ( k )$ , of the multicast session $\mathcal { M } _ { k }$ in $\mathcal { N } _ { s } ( m )$ . We should give the uniform upper bound, denoted as $\zeta ^ { \prime } { } _ { d } ,$ of all $\zeta ^ { \prime } { } _ { d } ( k ) , k = 1 , 2 , . . . , m _ { s }$ .

Lemma 13 When $m _ { d } = \omega ( \log m _ { s } ) .$ , for all multicast sessions in $\mathcal { N } _ { s } ( m )$ ; the number of non-served terminals are $w . h . p .$ ., at most $\rho ^ { \prime } _ { d } ( m ) \cdot m _ { d } ,$ , where $\rho ^ { \prime } { } _ { d } ( m ) = o ( 1 )$ .

For the case that $m _ { d } = { \cal O } ( \log m _ { s } )$ , we call a multicast session a failed session if any of its destinations is a nonserved terminal.

Lemma 14 When $m _ { d } = { \cal O } ( \log m _ { s } )$ , the number of the failed multicast sessions is at most w. $h . p . , \ \rho ^ { \prime \prime } { } _ { s } ( m ) \ \cdot \ m _ { s } ,$ where $\rho ^ { \prime \prime } { } _ { s } ( m ) = o ( 1 )$ .

According to Lemmas 12, 13 and 14, we obtain,

Lemma 15 For all $m _ { s } = \omega ( l )$ and $m _ { d } ,$ there exist $\rho _ { s } ( m ) \to I$ and $\rho _ { d } ( m ) \to 1$ as $n , m  \infty$ such that there are at least $\nu . h . p . , \rho _ { s } ( m ) m _ { s }$ sessions whose sources are not n and destinations are at least served with a fractionon-served sources $\rho _ { d } ( m )$ .

Proof Obviously, when $m _ { d } = \omega ( \log m _ { s } )$ , we can get that $\rho _ { s } ( m ) = 1 ~ - ~ \rho _ { s } ^ { \prime } ( m )$ and $\rho _ { d } ( m ) = 1 ~ - ~ \rho _ { d } ^ { \prime } ( m ) ;$ when $m _ { d } = { \cal O } ( \log m _ { s } )$ , we can get that $\rho _ { s } ( m ) = 1 - \rho ^ { \prime \prime } { } _ { s } ( m )$ and $\rho _ { d } ( m ) = 1$ .

Subsequently, we consider the relay burden of each served-cell under our secondary multicast routing scheme using a way similar to Lemma 9. Unlike in $\mathcal { N } _ { p } ( n )$ ; a secondary routing should circumvent any preservation regions which lie on its path called detour path (see the definition in Algorithm 3).

Lemma 16 Under the multicast routing scheme described in Algorithm 3, each secondary cell at most carries

$$
\operatorname{Load} _ {s} (n) = \left\{ \begin{array}{l l} O (\log m) & \text { when   } m _ {s} = O \bigg (\frac {\log m}{\phi (m , m _ {d})} \bigg) \\ O (\phi (m, m _ {d}) _ {s}) & \text { when   } \Omega \bigg (\frac {\log m}{\phi (m , m _ {d})} \bigg) \end{array} \right.,
$$

where $\phi ( m , m _ { d } )$ is defined in Theorem 3.

According to Lemmas 10, 15 and 16, we obtain Theorem 3.

# 6 Discussion and conclusion

In this paper, we study the multicast throughput of the cognitive network consisting of the primary network and the secondary network that are both ad hoc networks. We design a metric called the throughput decrement ratio (TDR) to ensure the priority of primary users in terms of the throughput. Based on a given threshold of TDR, we propose multicast schemes for the two networks and derive their achievable multicast throughputs, respectively. Particularly, we show that by using our schemes, when $\begin{array} { r } { n = o \left( \frac { m } { \left( \log m \right) ^ { 2 } } \right) } \end{array}$ (here, n and m are the densities of the primary network and secondary network, respectively), the primary ad hoc network and secondary ad hoc network can achieve simultaneously the multicast throughput as they are stand-alone.

Our schemes are designed based on Gaussian channel model [5, 8], also called generalized physical model [7], under which any node pairs can directly communicate with each other (by one hop) indeed. Thus, the connectivity of the network is different from that under the thresholdbased interference model [9], including protocol model and physical model [1], and it is trivial before the maximum length of single hop is defined. Under our schemes, in order to ensure the validity of the multicast routings, we set the maximum length of single hop to be of order $\Theta ( { \sqrt { \log n / n } } )$ in the primary network (or $\Theta ( \sqrt { \log m / m } )$ in the secondary network), which essentially guarantees the full connectivity of the network. While, according to the well-known percolation-based routing [5, 8], it is unnecessary to set the upper bounds on the length of all hops to be of order $\Theta ( { \sqrt { 1 0 \mathrm { g } n / n } } )$ (or $\Theta ( \sqrt { \log m / m } ) )$ . Then, it is a piece of interesting work to improve further the multicast throughput for both the primary network and the secondary network by exploiting the connection between percolation theory and the way to scale the transmission ranges of nodes [5, 8, 9].

As in most work related to the capacity scaling laws of wireless networks, we also use the centralized TDMA scheme to schedule both the primary network and the secondary network. Under such scheme, we assume that there exists a scheduler that has all the information about the current and past status of the network, and can schedule any transmission in the current and future time slots. Meanwhile, on the practical front, carrier-sensing multi-access (CSMA) networks, which make use of distributed random-access medium-access protocols, are receiving wide application [30]. Then, it will be interesting to find out whether our results derived under TDMA scheme can be directly applicable to the cognitive networks under CSMA scheme.

Finally, in our network model, the primary network is an ad hoc network. It is worth to study how to extend our results to the more realistic network scenarios where the primary network is an infrastructure-supported multihop network [7, 19, 26, 27], or a mobile network [28, 29].

Acknowledgements The research of authors are partially supported by NSF CNS-0832120, National Natural Science Foundation of China under No. 90718012, No. 90818023, No. 60828003, the National High Technology Research and Development Program of China (863 Program) under Grants No. 2007AA01Z180, No. 2007AA01Z136, No. 2007AA01Z149, Shanghai International Cooperation Project under Grant No. 075107005, the Natural Science Foundation of Zhejiang Province under Grant No. Z1080979, National Basic Research Program of China (973 Program) under grant No. 2010CB328100, No. 2006CB30300, Hong Kong RGC HKUST 6169/07, the RGC under Grant HKBU 2104/06E, and CERG under Grant PolyU-5232/07E.

# Appendix A

Proofs for lemmas

Proof Lemma 8: Consider any link $\langle \nu _ { i } ^ { p } , \nu _ { j } ^ { p } \rangle \in \Xi _ { p } ( F , \tau )$ for any $\tau \in \mathcal T$ ; where $\boldsymbol { \nu } _ { \mathrm { ~ } _ { i } } ^ { p }$ and $\nu _ { ~ j } ^ { p }$ locate on two adjacent cells respectively.

First, we bound $I _ { p p } ( \nu ^ { p } { } _ { i } , \nu ^ { p } { } _ { j } ; \tau )$ . We notice that the transmitters in the eight closest cells are located at distance at least $( K - 2 ) \sqrt { a _ { p } } \ ( i . e . , \sqrt { a _ { p } }$ in Fig. 1) from the receiver. The 16 next closest cells are of distance at least $( 2 K - 2 ) \sqrt { a _ { p } } ( i . e .$ , $4 _ { \sqrt { a _ { p } } }$ in Fig. 1). By extending the sum of the interferences to the whole region, it can be upper bounded as follows:

$$
\begin{array}{l} I _ {p p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \leq \sum_ {i = 1} ^ {\lceil 1 / a _ {p} \rceil} 8 i P (a _ {p}) ^ {\alpha / 2} \ell ((K i - 2) \sqrt {a _ {p}}) \\ \leq P \sum_ {i = 1} ^ {n} 8 i (K i - 2) ^ {- \alpha}. \\ \end{array}
$$

For $K \geq 3$ and $\alpha > 2$ , and by the Cauchy Test, we have

$$
\lim _ {n \to \infty} I _ {p p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \leq 8 P \int_ {+ \infty} 1 \frac {x}{(K x - 2) ^ {\alpha}} d x = 8 P \cdot C _ {1} (K, \alpha),
$$

where the constant $C _ { 1 } ( K , \alpha )$ (depending on K and a) that is defined in Eq. (16). It is clear that lim $I _ { p p } ( \nu _ { i } ^ { p } , \nu _ { i } ^ { p } ; \tau )$ gets the minimum value when $\nu _ { \ j } ^ { p }$ n!1 locates in the cell on the corner. Thus, we obtain, for any $\langle \nu _ { i } ^ { p } , \nu _ { j } ^ { p } \rangle { \in } \Xi _ { p } ( F , \tau )$ ; it holds that

$$
\lim _ {n \rightarrow \infty} I _ {p p} \left(v _ {i} ^ {p}, v _ {j} ^ {p}; \tau\right) \geq \frac {1}{4} \cdot 8 P \cdot C _ {1} (K, \alpha) = 2 P \cdot C _ {1} (K, \alpha). \tag {18}
$$

Second, we upper bound $I _ { s p } ( \nu ^ { p } { } _ { i } , \nu ^ { p } { } _ { j } ; \tau )$ . The preservation region centered on $\nu _ { \ j } ^ { p }$ consists of $K ^ { 2 }$ secondary cells, hence, for any slot s, there must exist one cell out of the $K ^ { 2 }$ cells that were to be scheduled in s except it locates in the preservation region, we denote that cell as $c _ { \tau }$ . We consider those cells containing the nodes in $\mathcal { V } _ { s } ( \nu _ { i } ^ { p } , \tau )$ . It can be seen that the secondary users in the eight closest cells to $c _ { \tau }$ are far away from $\nu _ { \ j } ^ { p }$ with distance at least of $\sqrt { a _ { s } } ( K - 1 ) / 2$ . The secondary users in the 16 next closest cells to cs are at Euclidean distance at least $\sqrt { a _ { s } } ( K + ( K - 1 ) / 2 )$ between $\nu _ { \ j } ^ { p }$ . Thus, the sum of the interferences can be upperbounded as follows:

$$
\begin{array}{l} I _ {s p} \left(v _ {i} ^ {p}, v _ {j} ^ {p}; \tau\right) \leq \sum_ {i = 1} ^ {\lceil 1 / a _ {s} \rceil} 8 i \cdot P \cdot \theta (n) \cdot a _ {s} ^ {\frac {\alpha}{2}} \cdot \ell \left(\left(K (i - 1) + \frac {K - 1}{2}\right) \sqrt {a _ {s}}\right) \\ \leq 2 P \cdot \theta (n) \cdot \sum_ {i = 1} ^ {m} 4 i \left(K i - \frac {K + 1}{2}\right) ^ {- \alpha}. \\ \end{array}
$$

Recall that $\begin{array} { r } { n = o \left( \frac { m } { \left( \log m \right) ^ { 2 } } \right) } \end{array}$ mðlog mÞ 2 ; we have

$$
\lim _ {n \rightarrow \infty} \sum_ {i = 1} ^ {m} 4 i \left(K i - \frac {K + 1}{2}\right) ^ {- \alpha} \leq \int_ {1} ^ {+ \infty} \frac {4 x}{(K x - \frac {k + 1}{2}) ^ {\alpha}} d x.
$$

The right integral can be calculated to be a constant $C _ { 2 } ( K , \alpha )$ depending on K and a that is described by Eq. (16). Hence, we have

$$
\lim _ {n \to \infty} I _ {s p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \leq 2 P \cdot \theta \cdot C _ {2} (K, \alpha). \tag {19}
$$

Third, we lower bound the signal received from the transmitter $S ( \nu ^ { p } { } _ { i } , \nu ^ { p } { } _ { j } ; \tau )$ . Since the node only transmits to a destination located in the adjacent cell, i.e., $| \nu _ { i } ^ { p } - \nu _ { j } ^ { p } |$ $\leq \sqrt { 5 a _ { p } }$ : Thus, the strength of the signal is bounded as:

$$
S (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \geq P \cdot (a _ {p}) ^ {\alpha / 2} \cdot (\sqrt {5 a _ {p}}) ^ {- \alpha} = 5 ^ {- \frac {\alpha}{2}} \cdot P. \tag {20}
$$

Finally, taking the limit of the SINR, we can obtain

$$
R _ {p} \left(v _ {i} ^ {p}, v _ {j} ^ {p}; \tau\right) \geq \log \left(1 + \frac {5 ^ {- \frac {\alpha}{2}}}{N _ {0} / P + 8 C _ {1} (K , \alpha) + 8 \theta (n) C _ {2} (K , \alpha)}\right).
$$

By Eqs. (18) and (19), $\begin{array} { r } { \Delta ( F , K , P ) \le \theta \cdot \frac { C _ { 2 } ( K , \alpha ) } { C _ { 1 } ( K , \alpha ) } . } \end{array}$ Let lim $\begin{array} { r } { \theta ( n ) = \theta \leq \Delta \cdot \frac { C _ { 1 } ( K , \alpha ) } { C _ { 2 } ( K , \alpha ) } } \end{array}$ ;we can get $\Delta ( F , K , P ) \le \Delta$ . Hence, n!1

$$
R _ {p} (v _ {i} ^ {p}, v _ {j} ^ {p}; \tau) \geq \log \left(1 + \frac {5 ^ {- \frac {\alpha}{2}}}{N _ {0} / P + 8 (1 + \Delta) C _ {1} (K , \alpha)}\right).
$$

Proof Lemma 9 Given a primary cell $c _ { t } { } ^ { * } .$ , we define the number of multicast sessions (flows) that are routed through the nodes inside $c _ { t } ^ { * }$ as a random variable $X _ { t } ,$ and we finally consider the uniform upper bound of $X _ { t } ,$ denoted by X, for every primary cell.

Define event $A ( k , t ) { \mathrm { : } }$ : Multicast session $\mathcal { M } _ { k }$ passes through the cell $c _ { t } ^ { * }$ . For any link $\nu _ { i } \nu _ { j } \in \operatorname { E S T } ( \mathcal { U } _ { k } )$ , Define event ${ A ^ { h } } _ { i j } ( k ,$ , t): $\mathcal { H P } _ { i j }$ passes through ${ c _ { t } } ^ { * } ;$ and define event $A ^ { \nu } { } _ { i j } ( k$ , t): $\mathcal { V } \mathcal { P } _ { i j }$ passes through $c _ { t } ^ { * }$ . Obviously, we have

![](images/b615d9a2d3ffa9fea7c73b0aef52354fcd2a948affe4bceaa929407986671c61.jpg)



Fig. 3 The construction of the region $ { \boldsymbol { S } } _ { i j } ^ { h } ( k , t )$ . Here |-| represents the Euclid length of a line segment or the Euclid distance between two nodes

$$
\operatorname * {P r} (A (k, t)) = \operatorname * {P r} \left(\bigcup_ {e _ {i j} \in \Pi_ {k}} \left(A _ {i j} ^ {h} (k, t) \cup A _ {i j} ^ {v} (k, t)\right)\right).
$$

By union bounds, it holds that

$$
\operatorname * {P r} (A (k, t)) \leq \sum_ {e _ {i j} \in \Pi_ {k}} (\operatorname * {P r} (A _ {i j} ^ {h} (k, t)) + \operatorname * {P r} (A _ {i j} ^ {v} (k, t))).
$$

First, we give the bound of $\operatorname* { P r } ( A ( k , t ) )$ . Based on the cell $c _ { t } ^ { * }$ , we construct the region $ { \boldsymbol { S } } _ { i j } ^ { h } ( k , t )$ of area $S _ { i j } ^ { h } ( k , t ) =$ $\sqrt { a _ { p } } ( 2 | \mathcal { H P } _ { i j } | + \sqrt { a _ { p } } )$ ; as in Fig. 3. Similarly, we construct the region $S _ { i j } ^ { \nu } ( k , t )$ area of $S _ { i j } ^ { \nu } ( k , t ) = \sqrt { a _ { p } } ( 2 | \mathcal { V } \mathcal { P } _ { i j } | + \sqrt { a _ { p } } )$ . The following two propositions obviously hold.

Proposition 1 The Poisson point $\nu _ { i }$ locates in the region $\mathbf { \mathcal { S } } _ { i j } ^ { h } ( k , t )$ if the event $A _ { i j } ^ { h } \left( k , t \right)$ happens.

Proposition 2 The Poisson point $\nu _ { j }$ locates in the region $S _ { i j } ^ { \nu } ( k , t )$ if the event $A _ { i j } ^ { \nu } \left( k , t \right)$ happens.

Define event $B _ { i j } ^ { h } ( k , t )$ (or $B ^ { \nu } { } _ { i j } ( k , t ) ) ;$ A Poisson node locates in a region of area $\boldsymbol { S } ^ { h } { } _ { i j } ( k , t )$ (or $S ^ { \nu } { } _ { i j } ( k , t ) )$ . Then, by Propositions 1 and 2, we have

$$
\operatorname * {P r} (A _ {i j} ^ {h} (k, t)) \leq \operatorname * {P r} (B _ {i j} ^ {h} (k, t)), \operatorname * {P r} (A _ {i j} ^ {\nu} (k, t)) \leq \operatorname * {P r} (B _ {i j} ^ {\nu} (k, t)).
$$

Moreover, define event B(k, t): A Poisson node locates in a region of area $S ( k , t ) = \operatorname* { m i n } \{ 1 , \tilde { S } ( k , t ) \}$ ; where

$$
\tilde {S} (k, t) = \sum_ {e _ {i j} \in \Pi_ {k}} \left(S _ {i j} ^ {h} (k, t) + S _ {i j} ^ {v} (k, t)\right).
$$

Hence, $\operatorname* { P r } ( A ( k , t ) ) \leq \operatorname* { P r } ( B ( k , t ) )$ .

For A(k, t) and $B ( k , t )$ , define their indicator variables as $\mathcal { T } ( A ( K , t ) )$ and $\mathcal { T } ( B ( K , t ) )$ ; where $\mathcal { T } ( A )$ takes value 1 if event A happens, otherwise 0. Hence, $\begin{array} { r } { X _ { t } = \sum _ { k = 1 } ^ { n _ { s } } \mathcal { T } ( A ( K , t ) ) } \end{array}$ . Define $\begin{array} { r } { Y _ { t } = \sum _ { k = 1 } ^ { n _ { s } } \mathcal { T } ( B ( K , t ) ) } \end{array}$ ; then it represents the number of nodes in the region of area $S ( k , t )$ according to a $\mathrm { p . p . p }$ of density $n _ { s } .$ So it follows a Poisson distribution of mean $\lambda = n _ { s } S ( k , t )$ .

Next, we consider the upper bound of $S ( k , t )$ . Recall that

$$
\tilde {S} (k, t) = \sum_ {e _ {i j} \in \Pi_ {k}} (2 | \mathcal {H P} _ {i j} | + \sqrt {a _ {p}} + 2 | \mathcal {V P} _ {i j} | + \sqrt {a _ {p}}) \sqrt {a _ {p}}.
$$

Since $\vert \mathcal { H P } _ { i j } \vert + \vert \mathcal { V P } _ { i j } \vert \le \sqrt { 2 } \vert \nu _ { i } - \nu _ { j } \vert$ and by Lemma $5 ,$ we have

$$
\tilde {S} (k, t) \leq 2 \sqrt {a _ {p}} \sum_ {e _ {i j} \in \Pi_ {k}} (\sqrt {2} | v _ {i} - v _ {j} | + \sqrt {a _ {p}}) \leq 2 (n _ {d} a _ {p} + 4 \sqrt {n _ {d} a _ {p}}).
$$

From the latest inequality, we obtain the uniform upper bound of $S ( k , t ) .$ , independent of k, denoted as S. That is,

$$
S (k, t) \leq S = \min \{2 (n _ {d} a _ {p} + 4 \sqrt {n _ {d} a _ {p}}), 1 \}.
$$

Hence, the upper bound of $Y _ { t }$ follows Poisson with $\lambda = n _ { s } S .$ .

When $n _ { s } S = \omega ( \log n )$ , by union bounds and Lemma 4, we get

$$
\begin{array}{l} \operatorname * {P r} (X \geq 2 n _ {s} S) \leq \left(\frac {n}{\log n}\right) \cdot \operatorname * {P r} (X _ {t} \geq 2 n _ {s} S) \leq \left(\frac {n}{\log n}\right) \\ \cdot \operatorname * {P r} (Y _ {t} \geq 2 n _ {s} S) \\ \leq \left(\frac {n}{\log n}\right) \cdot \frac {e ^ {- n _ {s} S} (e n _ {s} S) ^ {2 n _ {s} S}}{(2 n _ {s} S) ^ {(2 n _ {s} S)}} \\ = \left(\frac {n}{\log n}\right) \cdot \left(\frac {4}{e}\right) ^ {- n _ {s} S} = o \left(\frac {1}{\log n}\right)\rightarrow 0, (n \rightarrow \infty). \\ \end{array}
$$

When ns S = O(logn), we can assume that limn!1 nsSlog n $n _ { s } \ S = O ( \log n )$ $\begin{array} { r } { \mathsf { l } _ { n \longrightarrow \infty } \frac { n _ { s } S } { \log n } = } \end{array}$ $f ,$ where $f \geq 0$ is a constant. Let $z = e ^ { 2 } \mathrm { m a x } \{ f , 1 \}$ , by union bounds and Lemma 1, we have

$$
\begin{array}{l} \operatorname * {P r} (X \geq z \log n) \leq \left(\frac {n}{z \log n}\right) \cdot \operatorname * {P r} (X _ {t} \geq z \log n) \leq \left(\frac {n}{\log n}\right) \\ \cdot \operatorname * {P r} (Y _ {t} \geq z \log n) \\ \leq \left(\frac {1}{\log n}\right) \cdot \left(\frac {e ^ {\frac {(1 - f)}{z} + 1} f}{z}\right) ^ {z \log n} \\ \leq \left(e ^ {\frac {1}{e ^ {2}} - 1}\right) ^ {z \log n} \rightarrow 0, \text {   as   } n \rightarrow \infty . \\ \end{array}
$$

To sum up the two cases, we can prove the lemma.

Proof Lemma 10 For any link $\langle \nu _ { i } ^ { s } , \nu _ { j } ^ { s } \rangle \in \Xi _ { s } ( \bar { F } ) , \nu _ { j } ^ { s }$ must locate in a primary cell, and it may be served if it is out of the preservation regions. However, there is possibly a time slot $\tau _ { 0 }$ in which the distance from a primary node $\nu _ { 0 } ^ { p } \in$ $\mathcal { V } _ { p } \big ( \nu _ { i } ^ { s } , \tau _ { 0 } \big )$ to $\nu _ { j } ^ { s }$ is so close that a fatal interference is imposed on $\nu _ { j } ^ { s } .$ The secondary transmission scheduling scheme can prevent this scenario from happening. Since for $\mathcal { N } _ { s } ( m )$ the same packet is transmitted along M time slots, we can guarantee that there exists a time slot s out of M time slots in which the minimum distance to $\nu _ { j } ^ { s }$ from all $\nu ^ { p } \in \mathcal { V } _ { p } ( \nu _ { i } ^ { s } , \tau )$ is at least of $( M - \textstyle { \frac { 5 } { 2 } } ) \sqrt { a _ { p } }$ . Hence,

$$
\begin{array}{l} I _ {p s} (v _ {i} ^ {s}, v _ {j} ^ {s}; \tau) \leq \sum_ {i = 1} ^ {\infty} 8 i P (a _ {p}) ^ {\frac {\alpha}{2}} \ell ((K i - 2) \sqrt {a _ {p}}) \\ + P (a _ {p}) ^ {\frac {\alpha}{2}} \ell \left(\left(M - \frac {5}{2}\right) \sqrt {a _ {p}}\right). \\ \end{array}
$$

So, we have

$$
I _ {p s} \left(v _ {i} ^ {p}, v _ {j} ^ {p}; \tau\right) <   8 P \cdot C _ {1} + \left(M - \frac {5}{2}\right) ^ {- \alpha} \cdot P,
$$

where $C _ { 1 } = C _ { 1 } ( K , \ \alpha )$ is the constant defined in Eq. (16).

Similar to Lemma 8, we can obtain that $I _ { p s } ( \boldsymbol { \nu } ^ { s } { } _ { i } , \boldsymbol { \nu } ^ { s } { } _ { j } ) < 8 P$ - $\theta ( n ) \cdot C _ { 1 }$ . Since

$$
S (v _ {i} ^ {s}, v _ {j} ^ {s}; \tau) \geq P \cdot \theta (n) \cdot a _ {s} ^ {\frac {\alpha}{2}} (5 a _ {s}) ^ {\frac {\alpha}{2}}) = P \cdot \theta (n) \cdot 5 ^ {- \frac {\alpha}{2}},
$$

when $\begin{array} { r } { 0 < \operatorname* { l i m } _ { n \to \infty } \theta ( n ) < \infty } \end{array}$ ; we have

$$
R _ {s} (v _ {i} ^ {s}, v _ {j} ^ {s}; \tau) \geq \frac {1}{M K ^ {2}}
$$

$$
\cdot \log \left(1 + \frac {P \cdot \theta \cdot (\sqrt {5}) ^ {- \alpha}}{N _ {0} + P \cdot (6 C _ {1} (1 + \theta) + (\frac {2}{2 M - 5}) ^ {\alpha})}\right).
$$

If $\theta ( n ) = o ( 1 )$ , we have

$$
R _ {s} (v _ {i} ^ {s}, v _ {j} ^ {s}; \tau) \geq \frac {P \cdot \theta (n) \cdot (\sqrt {5}) ^ {- \alpha}}{M K ^ {2} N _ {0} + P \cdot (6 C _ {1} (1 + \theta) + (\frac {2}{2 M - 5}) ^ {\alpha})}.
$$

Combining two cases in terms of $\theta ( n )$ , we complete the proof.

Proof Lemma 12 Define the number of non-served sources as a random variable $\zeta _ { s } ^ { \prime } .$ . According to Lemma 11, it follows a Poisson distribution of mean

$$
\lambda_ {s} ^ {\prime} \leq m _ {s} \cdot S _ {m a x} ^ {\prime} = K ^ {2} \mu \cdot m _ {s} \cdot n \cdot \frac {\log m}{m}.
$$

When $\begin{array} { r } { m _ { s } \cdot n \cdot \frac { \log m } { m } = \omega ( 1 ) } \end{array}$ ; let $\begin{array} { r } { \rho _ { s } ^ { \prime } ( m ) = 2 K ^ { 2 } \cdot \mu \cdot n \cdot \frac { \log m } { m } . } \end{array}$ By Lemma 4, we get

$$
\operatorname * {P r} \left(\xi_ {s} ^ {\prime} \geq \rho_ {s} ^ {\prime} (m) \cdot m _ {s}\right) \leq (e / 4) ^ {K ^ {2} \mu \cdot m _ {s} n \cdot \frac {\log m}{m}} \rightarrow 0.
$$

When $m _ { s } \cdot n \cdot \frac { \log m } { m } = { \cal { O } } ( 1 )$ ; let $\rho _ { s } ^ { \prime } ( m ) = ( m _ { s } ) ^ { - \kappa _ { 1 } }$ ; where $0 < \kappa _ { 1 } < 1$ is a constant. By Lemma 4, there exists a constant $\kappa _ { 2 }$ such that

$$
\operatorname * {P r} \left(\xi_ {s} ^ {\prime} \geq \left(m _ {s}\right) ^ {1 - \kappa_ {1}}\right) \leq \kappa_ {2} \cdot \left(e / \left(m _ {s}\right) ^ {1 - \kappa_ {1}}\right) ^ {\left(m _ {s}\right) ^ {1 - \kappa_ {1}}} \rightarrow 0.
$$

Combining the two cases in terms of the relations among $m _ { s } ,$ m and n, we complete the proof.

Proof Lemma 13 According to Lemma 11, the random variable $\boldsymbol { \xi } _ { \ k } ^ { d }$ follows a Poisson distribution of mean $K ^ { 2 } \mu \cdot m _ { d } \cdot n \cdot \frac { \log m } { m }$ . By using Lemma 4 and union bounds, we separately commence our analysis in two cases according to the relations among $m _ { d } ,$ m and n. When $m _ { d }$ - $\begin{array} { r } { n \cdot { \frac { \log m } { m } } = \omega ( \log m _ { s } ) } \end{array}$ - log m ¼ xðlog msÞ; it holds that, m

$$
\operatorname * {P r} \left(\xi^ {d} \geq 2 K ^ {2} \mu m _ {d} \cdot n \cdot \frac {\log m}{m}\right) \leq m _ {s} \cdot \left(\frac {e}{4}\right) ^ {K ^ {2} \mu m _ {d} \cdot n \cdot \frac {m}{\log m}} \rightarrow 0.
$$

When $\begin{array} { r } { m _ { d } \cdot n \cdot \frac { \log m } { m } = O ( \log m _ { s } ) } \end{array}$ ; and

$$
\lim _ {n \rightarrow \infty} \frac {m _ {d} \cdot n \cdot \log m}{m \cdot \log m _ {s}} = f _ {1}, f _ {1} \geq 0
$$

Let $z _ { 1 } = 3 + \log ( 1 + K ^ { 2 } \mu f _ { 1 } )$ , we have

$$
\begin{array}{l} \operatorname * {P r} \left(\xi^ {d} \geq e ^ {z _ {1}} \log m _ {s}\right) \leq m _ {s} \operatorname * {P r} \left(\Xi_ {k} ^ {d} \geq z _ {1} \log m _ {s}\right) \\ \leq m _ {s} ^ {1 + e ^ {z _ {1}} - K ^ {2} \mu f _ {1} - z _ {1} e ^ {z _ {1}} + e ^ {z _ {1}} \log (1 + K ^ {2} \mu f _ {1})} \rightarrow 0. \\ \end{array}
$$

Combining the two cases, we obtain that

$$
\rho_ {d} ^ {\prime} (m) = \left\{ \begin{array}{l l} O \big (n \cdot \frac {\log m}{m} \big) & \text { when } \quad m _ {d} \cdot n \cdot \frac {\log m}{m} = \Omega (\log m _ {s}) \\ O \Big (\frac {\log m _ {s}}{m _ {d}} \Big) & \text { when } \quad m _ {d} \cdot n \cdot \frac {\log m}{m} = O (\log m _ {s}) \end{array} \right.
$$

Thus, we have that $\rho _ { d } ^ { \prime } ( m ) = o ( 1 )$ when $m _ { d } = \omega ( \log m _ { s } )$ .

Proof Lemma 14 Define the number of the failed multicast sessions as a random variable c. Note that $\gamma$ follows a Poisson distribution of mean

$$
\lambda_ {s} ^ {\prime \prime} \leq m _ {d} \cdot m _ {s} \cdot K ^ {2} \cdot \mu \cdot n \cdot \log m / m.
$$

When $\begin{array} { r } { m _ { d } \cdot m _ { s } \cdot n \cdot \frac { \log m } { m } = \omega ( 1 ) } \end{array}$ ; let $\rho _ { s } ^ { \prime \prime } ( m ) = 2 m _ { d } \cdot K ^ { 2 }$ $\mu \cdot n \cdot { \frac { \log m } { m } }$ - log m . By Lemma 4, we have

$$
\operatorname * {P r} \left(\gamma \geq \rho_ {s} ^ {\prime \prime} (m) \cdot m _ {s}\right) \leq (e / 4) ^ {m _ {d} m _ {s} \cdot K ^ {2} \cdot \mu \cdot n \cdot \frac {\log m}{m})} \rightarrow 0.
$$

When $\begin{array} { r } { m _ { d } \cdot m _ { s } \cdot n \cdot \frac { \log m } { m } = { \cal O } ( 1 ) } \end{array}$ ; let $\rho _ { s } ^ { \prime \prime } ( m ) = ( m _ { s } ) ^ { - \kappa _ { 3 } }$ ; where $0 < \kappa _ { 3 } < 1$ is a constant. By Lemma 4, there exists a constant $\kappa _ { 4 }$ such that

$$
\begin{array}{l} \operatorname * {P r} (\gamma \geq \rho_ {s} ^ {\prime \prime} (m) \cdot m _ {s}) \leq \kappa_ {4} \cdot (e / (m _ {s}) ^ {1 - \kappa_ {3}}) ^ {(m _ {s}) ^ {1 - \kappa_ {3}}} \to 0, \text { as } m, n \\ \to \infty . \end{array}
$$

Combining the two cases, the lemma can be proved.

Proof Lemma 16 As in $N _ { p } ( n )$ , to simplify the description, we define a sequence of sets of directed edges:

$$
\Pi_ {k} ^ {\prime} = \left\{e _ {i j} | \langle v _ {i}, v _ {j} \rangle \in \operatorname{EST} \left(\mathcal {U} _ {k} ^ {\prime}\right) \right\}, f o r k = 1, 2, \dots , m _ {s}.
$$

Given a secondary cell $\hat { c } _ { t } ^ { * }$ ; we define the number of multicast flows that will be routed through the nodes inside this cell as a random variable $Z _ { t } ,$ , and we finally consider the uniform upper bound Z of $Z _ { t }$ for every secondary cell.

Define event D(k, t): Multicast session $\mathcal { M } _ { k }$ passes through the cell $\hat { c } _ { t } ^ { * } .$ . For any link $\nu _ { i } \nu _ { j } \in \operatorname { E S T } ( \mathcal { U } _ { k } ^ { \prime } )$ ; Define event $\begin{array} { r l } { D _ { \ i j } ^ { h } ( k , t ) : } & { { } \overline { { \mathcal { H P } } } _ { i j } } \end{array}$ passes through $\bar { c } _ { t } ^ { * } ;$ and event $D ^ { \nu } { } _ { i j } ( k , t ) : \overline { { \mathcal { V } } } _ { i j }$ passes through $\hat { c } _ { t } ^ { * }$ . Obviously, we have

$$
\operatorname * {P r} (D (k, t)) \leq \sum_ {e _ {i j} \in \Pi_ {k} ^ {\prime}} (\operatorname * {P r} (D _ {i j} ^ {h} (k, t)) + \operatorname * {P r} (D _ {i j} ^ {v} (k, t)).
$$

We firstly give the bound of $\operatorname* { P r } ( D ( k , t ) )$ Þ. Based on the cell $\hat { c } _ { t } ^ { * }$ ; we construct the region $\bar { \boldsymbol { S } } _ { i j } ^ { h } ( \dot { k } , t )$ of area

$$
\bar {S} _ {i j} ^ {h} (k, t) = (2 \mu K + 1) \cdot \sqrt {a _ {s}} \cdot (2 | \mathcal {H P} _ {i j} | + (K + 2) \sqrt {a _ {s}}),
$$

as in Fig. 4. Similarly, we construct the region $\bar { \boldsymbol { S } } _ { i j } ^ { \nu } ( k , t )$ of area

![](images/43d42a6a8d761cdffabd4146b82aff82e3b3fb835217aabdd4e7f93622e99d16.jpg)



Fig. 4 The construction of the region $\bar { \boldsymbol { S } } _ { i j } ^ { h } ( k , t )$ . Here, $l _ { 0 } = \mu K \sqrt { a _ { s } }$ ffi because the maximum size of any clusters is $\mu .$ Obviously, $l = \left( 2 \mu K + 1 \right) \cdot \sqrt { a _ { s } }$ ffis

$$
\bar {S} _ {i j} ^ {\nu} (k, t) = (2 \mu K + 1) \cdot \sqrt {a _ {s}} \cdot (2 | \mathcal {V P} _ {i j} | + (K + 2) \sqrt {a _ {s}}).
$$

The following two propositions are obviously true.

Proposition 3 The Poisson point $\nu _ { i }$ locates in the region $\bar { \boldsymbol { S } } _ { i j } ^ { h } ( \bar { k } , t )$ if the event Dijh (k, t) happens.

Proposition 4 The Poisson point $\nu _ { j }$ locates in the region $\bar { \boldsymbol { S } } _ { i j } ^ { \nu } ( k , t )$ if the event Dijv (k, t) happens.

Then, we get that $\begin{array} { r } { Z _ { t } = \sum _ { k = 1 } ^ { m _ { s } } \mathcal { T } ( D ( K , t ) ) } \end{array}$ follows a Poisson distribution of mean $\lambda \leq m _ { s } \cdot \bar { S } ,$ ; where

$$
\bar {S} = \min \left\{1, \sum_ {e _ {i j} \in \Pi_ {k} ^ {\prime}} \left(\bar {S} _ {i j} ^ {h} (k, t) + \bar {S} _ {i j} ^ {v} (k, t)\right) \right\}.
$$

By Lemma 5, we have

$$
\begin{array}{l} \bar {S} \leq 2 (2 \mu K + 1) \cdot \sqrt {a _ {s}} \cdot \sum_ {e _ {i j} \in \Pi_ {k} ^ {\prime}} \left(\sqrt {2} | v _ {i} v _ {j} | + (K + 2) \sqrt {a _ {s}}\right) \\ \leq 2 (2 \mu K + 1) \cdot (4 \sqrt {m _ {d} a _ {s}} + (K + 2) m _ {d} a _ {s}) = \hat {S}. \\ \end{array}
$$

When $m _ { s } \hat { S } = \omega ( \log n )$ ; by union bounds and Lemma 4, we can obtain

$$
\operatorname * {P r} (Z \geq 2 m _ {s} \hat {S}) \leq (m / \log m) (4 / e) ^ {- m _ {s} \hat {S}} = o (1 / \log m) \rightarrow 0.
$$

When msS^ ¼ Oðlog mÞ and limn!1 msS^log m $m _ { s } \hat { S } = O ( \log m )$ $\begin{array} { r } { \operatorname* { l i m } _ { n  \infty } \frac { m _ { s } \hat { S } } { \log m } = \bar { f } \geq 0 } \end{array}$ . Let $\bar { z } = e ^ { 2 }$ maxff-; 1g;we obtain that

$$
\operatorname * {P r} (Z \geq \bar {z} \log n) \leq (e ^ {\frac {1}{e ^ {2}} - 1}) ^ {\bar {z} \log n} \to 0.
$$

Summing up these two cases, we complete the proof.

# References

1. Gupta, P., & Kumar, P. R. (2000). The capacity of wireless networks. IEEE Transactions on Information Theory, 46(2), 388–404.   
2. Keshavarz-Haddad, A., Ribeiro, V., & Riedi, R. (2006). Broadcast capacity in multihop wireless networks. In Proceedings of ACM MobiCom.   
3. Xiang-Yang, L., Tang, S., & Ophir, F. (2007). Multicast capacity for large scale wireless ad hoc networks. In Proceedings of ACM MobiCom.   
4. Shakkottai, X., Liu, S., & Srikant, R. (2007). The multicast capacity of large multihop wireless networks. In Proceedings of ACM MobiHoc.   
5. Franceschetti, M., Dousse, O., Tse, D., & Thiran, P. (2007). Closing the gap in the capacity of wireless networks via percolation theory. IEEE Transactions on Information Theory, 53(3), 1009–1018.   
6. Zheng, R. (2008). Asymptotic bounds of information dissemination in power-constrained wireless networks. IEEE Transactions on Wireless Communications, 7(1), 251–259.   
7. Agarwal, A., & Kumar, P. R. (2004). Capacity bounds for ad hoc and hybrid wireless networks. ACM SIGCOMM Computer Communication Review, 34(3), 71–81.   
8. Li, S., Liu, Y., & Li, X.-Y. (2008). Capacity of large scale wireless networks under gaussian channel model. In Proceedings of ACM MobiCom.   
9. Wang, C., Li, X., Jiang, C., Tang, S., & Liu, Y. (2009). Scaling laws on multicast capacity of large scale wireless networks. In Proceedings of IEEE INFOCOM.   
10. Keshavarz-Haddad, A., Riedi, R. (2007). Bounds for the capacity of wireless multihop networks imposed by topology and demand. In Proceedings of ACM MobiHoc.   
11. Akyildiz, I. F., Lee, W.-Y., Vuran, M. C., & Mohanty, S. (2006). Next generation/dynamic spectrum access/cognitive radio wireless networks: A survey. Elsevier Computer Networks, 50, 2127–2159.   
12. Federal Communications Commission Spectrum Policy Task Force. (2002). Report of the spectrum efficiency working group, technical report, FCC.   
13. Devroye, N., Mitran, P., & Tarokh, V. (2006). Achievable rates in cognitive radio channels. IEEE Transactions on Information Theory, 52(5), 1813–1827.   
14. Mitola, J. (2000). Cognitive radio, Ph.D. thesis, Royal Institute of Technology (KTH).   
15. Jafar, S., & Srinivasa, S. (2007). Capacity limits of cognitive radio with distributed and dynamic spectral activity. IEEE Transactions on Computer, 25(5), 529–537.   
16. Vu, M., & Tarokh, V. (to appear). Scaling laws of single-hop cognitive networks. IEEE Transactions on Wireless Communications.   
17. Jeon, S.-W., Devroye, N., Vu, M., Chung, S.-Y., & Tarokh, V. (2009). Cognitive networks achieve throughput scaling of a homogeneous network. In Proceedings of IEEE WiOpt.   
18. Liu, B., Liu, Z., & Towsley, D. (2003). On the capacity of hybrid wireless networks. In Proceedings of IEEE INFOCOM.   
19. Mao, X., Li, X.-Y., Tang, S. (2008) Multicast capacity for hybrid wireless networks. In Proceedings of ACM MobiHoc.   
20. Liu, B., Thiran, P., & Towsley, D. (2007). Capacity of a wireless ad hoc network with infrastructure. In Proceedings of ACM MobiHoc.   
21. Li, X.-Y. (2009). Multicast capacity of wireless ad hoc networks. IEEE/ACM Transactions on Networking, 17(3), 950–961.

22. Wang, C., Jiang, C., Li, X.-Y., Tang, S., & Tang, X. (2009). Achievable multicast throughput for homogeneous wireless ad hoc networks. In Proceedings of IEEE WCNC.   
23. Vu, M., Devroye, N. (to appear). On the primary exclusive regions in cognitive networks. IEEE Transactions on Wireless Communications.   
24. Meester, R., & Roy, R. (1996). Continuum percolation. Cambridge: Cambridge University Press.   
25. Grossglauser, M., & Thiran, P. (2005). Networks out of control: Models and methods for random networks, technical report. School of Computer and Communication Sciences (EPFL).   
26. Liu, B., Thiran, P., & Towsley, D. (2007). Capacity of a wireless ad hoc network with infrastructure. In Proceedings of ACM MobiHoc.   
27. Wang, C., Tang, S., Li, X.-Y., Jiang, C., & Liu, Y. (2009). Multicast throughput of hybrid wireless networks under Gaussian channel model. In Proceedings of IEEE ICDCS.   
28. Grossglauser, M., & Tse, D. N. C. (2002). Mobility increases the capacity of ad hoc wireless networks. IEEE/ACM Transactions on Networking (TON), 10(4), 477–486.   
29. Sharma, G., Mazumdar, R., & Shroff, N. (2007). Delay and capacity trade-offs in mobile ad hoc networks: A global perspective. IEEE/ACM Transactions on Networking (TON), 15(5), 992–1103.   
30. Chau, C., Chen, M., & Liew, S. (2009) Capacity of large scale csma wireless networks. In Proceedings of ACM MobiCom.

# Author Biographies

![](images/639f175e4b9445ad45d8adb0c5adb9d0506abcfaff356912aa700f4ca5c48153.jpg)



Cheng Wang received his BS degree in Department of Mathematics and Physics from Shandong University of Technology in 2002, and an MS degree in Department of Applied Mathematics from Tongji University in 2006. He is currently a PhD student in Department of Computer Science at Tongji University. His research interests include wireless communications and networking, network coding, and distributed computing.

![](images/5bd894258080bda319725245042c173fab756f19194a419701a89f53f14556e1.jpg)



Changjun Jiang received the Ph.D. degree from the Institute of Automation, Chinese Academy of Sciences, Beijing, China, in 1995 and conducted post-doctoral research at the Institute of Computing Technology, Chinese Academy of Sciences, in 1997. Currently he is a Professor with the Department of Computer Science and Engineering, Tongji University, Shanghai. He is also a council member of China Automation Federation and Artificial Intel-

ligence Federation, the Vice Director of Professional Committee of Petri Net of China Computer Federation, and the Vice Director of Professional Committee of Management Systems of China Automation Federation. He was a Visiting Professor of Institute of Computing Technology, Chinese Academy of Science; a Research Fellow of the City University of Hong Kong, Kowloon, Hong Kong; and an Information Area Specialist of Shanghai Municipal Government. His current areas of research are concurrent theory, Petri net, and formal verification of software, concurrency processing and intelligent transportation systems.

![](images/6783f3c83ad6542753b746ac0845a071adedfa4df36f4f3cdcfedb5cbbea3429.jpg)



Xiang-Yang Li received MS (2000) and PhD (2001) degree at Department of Computer Science from University of Illinois at Urbana-Champaign. He received his Bachelor degree at Department of Computer Science and Bachelor degree at Department of Business Management from Tsinghua University, P.R. China, both in 1995. He has been with Department of Computer Science at the Illinois Institute of Technology since 2000. Cur-

rently he is an Associate Professor of Department of Computer Science, IIT. He also holds visiting professorship or adjunctprofessorship at the following universities: TianJin University, WuHan University, NanJing University, Tongji University and Microsoft Research Asia. His research interests span the wireless ad hoc networks, computational geometry, game theory, and cryptography and network security. He served various positions (such as conference chair, local arrangement chair) at numerous international conferences. He is an editor of Ad Hoc & Sensor Wireless Networks: An International Journal. He recently also coorganized a special issue of ACM MONET on non-cooperative computing in wireless networks and a special issue of IEEE Journal of Selected Area in Communications. He is a senior member of IEEE computer society, and a member of ACM.

![](images/11d33be2f289ffd2c7bf82eae8ef0a71f799149ad2ddc168cee1b7793ac85699.jpg)



Yunhao Liu received the B.S. degree in Automation from Tsinghua University, China, in 1995, and the M.A. degree from the Beijing Foreign Studies University, China, in 1997, and the M.S. and Ph.D. degrees in Computer Science and Engineering from Michigan State University in 2003 and 2004, respectively. Currently he is an Associate Professor of Department of Computer Science and Engineering at the Hong Kong University of Science and

Technology. He is also an Adjunct Professor of Xi’an Jiaotong University, Jilin University, and Ocean University of China. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. Dr. Liu and his student Li Mo received the Grand Award of Hong Kong ICT Best Innovation and Research Award 2007. He is a senior member of IEEE computer society, and a member of ACM.