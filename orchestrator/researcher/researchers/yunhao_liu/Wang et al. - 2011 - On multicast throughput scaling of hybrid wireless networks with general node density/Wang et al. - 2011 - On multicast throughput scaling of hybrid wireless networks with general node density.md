# On multicast throughput scaling of hybrid wireless networks with general node density

Cheng Wang a,b,⇑ , Changjun Jiang a,b , Xiang-Yang Li c,d , Yunhao Liu d

a Department of Computer Science and Technology, Tongji University, Shanghai, China   
b Key Laboratory of Embedded System and Service Computing, Ministry of Education, China   
c Department of Computer Science, Illinois Institute of Technology, Chicago, IL 60616, United States   
d TNLIST, School of Software, Tsinghua University, China

# a r t i c l e i n f o

Article history:

Received 30 November 2009

Received in revised form 1 December 2010

Accepted 21 June 2011

Available online 22 July 2011

Keywords:

Multicast throughput

Random networks

Wireless ad hoc networks

Hybrid wireless networks

Capacity scaling laws

# a b s t r a c t

In this paper, we consider hybrid wireless networks with a general node density k 2 [1, n], where n ad hoc nodes are uniformly distributed and m base stations (BSs) are regularly placed in a square region $\boldsymbol { \mathcal { A } } ( \boldsymbol { n } , \boldsymbol { A } ) = \left[ 1 , \sqrt { \boldsymbol { A } } \right] \times \left[ 1 , \sqrt { \boldsymbol { A } } \right]$ with $A \in [ 1 , n ]$ . We focus on multicast sessions in which each ad hoc node as a user chooses randomly d ad hoc nodes as its destinations. Specifically, when d = 1 (or d = n  1), a multicast session is essentially a unicast (or broadcast) session. We study the asymptotic multicast throughput for such a hybrid wireless network according to different cases in terms of m 2 [1, n] and $d \in [ 1 , n ] ,$ , as n ? 1. To be specific, we design two types of multicast schemes, called hybrid scheme and BS-based scheme, respectively. For the hybrid scheme, there are two alternative routing backbones: sparse backbones and dense backbones. Particularly, according to different regimes of the node density k ¼ nA, we derive the thresholds in terms of m and d. Depending on these thresholds, we determine which scheme is preferred for the better performance of network throughput.

\- 2011 Elsevier B.V. All rights reserved.

# 1. Introduction

The last decade has witnessed the rapid development of wireless technology. While, the role of wireless technology in current communication services remains still limited. In cellular networks and wireless LANs, the wireless system involves only with the last stage of communication, from the base stations (in cellular networks) or access points (in wireless LAN) to the end users. In cellular networks, the communication between the base stations is generally taken on by wired links of high-capacity. The expensive cost and difficulty of building base stations promotes the rise of the new networking paradigm – wireless ad hoc networks [13]. Wireless ad hoc networks differ from the

conventional infrastructure-based networks above by the fact that they rely completely on wireless communication. They are simply formed by a group of users that have transmitting and receiving capabilities. The nodes can be the mobile phones of the cellular topology, laptops like in WLANs, or sensors that measure some physical data. Whatever the application is, the common characteristic is the following: A group of nodes want to communicate with each other over the shared wireless medium but there is no additional infrastructure for assisting communication or for coordinating traffic [1,2]. In wireless ad hoc networks, when saving the investment costs of base stations, the other side of the coin is that the network throughput possibly decreases due to the aggravation of interference between the communication pairs. An interesting question is to what extent can a given number of base stations improve the network throughput. The aim of this paper is to contribute in this issue.

The focus of this paper is on scaling laws, i.e., scaling of the network throughput in the limit when the number of users gets large (n ? 1) [1,3–12]. The scaling laws for wireless ad hoc networks have been intensively studied, especially after the milestone work done in [1]. The main advantage of studying scaling laws is to highlight qualitative and architectural properties of the system without getting involved with too many technique details [13]. The scaling laws results provide some architectural guidelines on how to design schemes that scale well, while the detailed design and performance analysis for a network with a given number of users would involve tuning of many parameters and improvements of the scheme to optimize the pre-constant in the system throughput. We consider the hybrid wireless networks that have some amount of infrastructure (e.g., base stations connected by high bandwidth links) available. These base stations neither produce data nor consume data. They support the underlying ad hoc networks by relaying data packets through the infrastructure. The integrate of wireless ad hoc and cellular network architecture is often referred to as hybrid wireless network or multihop cellular network [14–17]. In such a hybrid network, data can be transported in a multi-hop fashion as in ad hoc networks or via the infrastructure as in cellular networks. The hybrid network architecture has at the same time the advantages of both types of networks. It offers the local flexibility of ad hoc networks and efficient long-distance routing of infrastructure. Then, an interesting question arises as to how much the additional infrastructure improves the capacity of pure wireless ad hoc networks. Specifically, we study a hybrid wireless network with a general node density $\lambda : [ 1 , n ] , ^ { 1 }$ where n ad hoc users (AUs) are uniformly distributed and m base stations (BSs) are regularly placed in a square region $\boldsymbol { \mathcal { A } } ( \boldsymbol { n } , \boldsymbol { A } ) = \left\lceil 1 , \sqrt { \boldsymbol { A } } \right\rceil \times \left\lceil 1 , \sqrt { \boldsymbol { A } } \right\rceil$ with A 2 [1, n].

Multicast is an efficient method of supporting group communication, as it allows transmission and routing of packets to multiple destinations using fewer network resources. There are many important applications of wireless multicast, such as distribution of data, audio/video conference, distance education, and distributed interactive games, etc., [18]. Please see the illustration in Fig. 1. An emerging typical application that has already been tested is the use of wireless ad hoc networks to broadcast replays during football games, [12]. In wireless sensor networks, multicast is an important technique for information dissemination or code updating, [19–22]. We focus on multicast sessions in which each AU as a user chooses randomly d ad hoc nodes as its destinations, and study multicast capacity scaling laws for hybrid wireless networks according to different cases in terms of m : [1,n] and d : [1,n], as $n  \infty ,$ . We design two broad types of multicast schemes: hybrid scheme and BS-based scheme. For the hybrid scheme, there are two alternative routing backbones, called sparse backbones and dense backbones, respectively. Hence, three schemes are produced, i.e., hybrid scheme based on sparse backbones (H-SB scheme), hybrid scheme based on dense backbones (H-DB scheme), and BS-based scheme. According to different cases of the network parameters, i.e., the node density $\begin{array} { r } { \lambda = \frac { n } { A } , } \end{array}$ the number of BSs m, and the number of destinations per multicast session d, we choose the optimal one from these three schemes, and derive the optimal multicast throughput for hybrid networks. We show that under the H-SB and H-DB schemes, the bottlenecks are located at B-O links, i.e., the links between BSs and ordinary wireless nodes. Intuitively, if the bandwidth of B-O links can be increased, the throughput for the network should possibly be enhanced. Hence, we designedly derive the multicast throughputs under the H-SB and H-DB schemes without taking the possible bottlenecks on the B-O links into account. Such results could be used when some new technical assumptions are made for the B-O links.

Compared to related works, this work has the following characteristics:

 More general network scaling model. For the scaling laws issue, in terms of scaling patterns, there are two typical network models [10,13]: extended networks [10,23–25,13,16,26] and dense networks [1,11,12,27,28]. In the former, the node density is fixed to a constant and the area of the deployment region increases to infinity; in the latter, the area is fixed to a constant and the node density increases to infinity. It is easy to see that both the extended network and dense network are indeed the special cases of our model corresponding to the cases that A = n and A = 1, i.e., k = 1 and k = n, respectively. The characterization of two particular scalings, i.e., extended networks and dense networks, does not suffice to develop a comprehensive understanding of wireless networks, although they are representative models to some extent [13]. Hence, in this paper, we consider comprehensively the network with a general node density k : [1,n] rather than only the cases k = 1 and k = n, which can offer more insights about the scaling laws for hybrid networks.

 More general session pattern. Intuitively, when d = 1 (or d = n  1), a multicast session is essentially a unicast (or broadcast) one. That is, the unicast and broadcast sessions can be regarded as the special cases of multicast. In this paper, we directly compute multicast throughput to unify the unicast and broadcast throughputs.

 More realistic communication model. For the scaling laws issue, there are two broad types of communication models in general. The first one is the binary-rate model under which if the value of a given conditional expression is beyond the threshold, the transmitter can send successfully to the receiver at a specific constant data rate; otherwise, it can not send any, i.e., the transmission rate is assumed to be a binary function. The protocol model (ProM) and physical model (PhyM) defined in [1] both belong to the binary-rate model. The second one is the continuous-rate model that determines the transmission rate at which the transmitter can send its data to the receiver reliably, based on a continuous function of the receiver’s SINR. Gaussian channel model [24] (also called generalized physical model [15,27]) is a popular continuous-rate communication model, under which any communication pair $\nu _ { i }$ and $\nu _ { j }$ can establish a direct communication link, over a channel of bandwidth B, of rate $R ( \upsilon _ { i } , \upsilon _ { j } ) = B \log ( 1 + \mathrm { S I N R } \left( \upsilon _ { j } \right) )$ . It has been shown that ProM and PhyM are reasonable abstraction of Gaussian channel model for dense networks, but they are over-optimistic and unrealistic for extended networks [1,24,25]. Since we consider the network model with a general node density, we adopt Gaussian channel model to capture better the nature of wireless channel.

![](images/8d3dc5531c1c20c8ddb380e5f1d89fb5e25f91b6654626668a9b839d7e1350db.jpg)



Fig. 1. An illustration of the multicast session in ad hoc networks with infrastructure support. Some of the users might be close to data sources (e.g., Internet access points), and they would act as sources for the multicast traffic. Other nodes would act as relays and sinks (destinations) for the data. The base stations are connected with links of high bandwidth (e.g., wired links).

The rest paper is organized as follows. In Section 2, the network model is introduced. Main results are presented in Section 3. In Section 4, we design the multicast schemes for hybrid wireless networks and derive the achievable throughput. In Section 5, we review the existing related literature. We conclude this study, and discuss the future work in Section 6.

# 2. System model

# 2.1. Network model

First, we build a random wireless ad hoc networks by distributing uniformly n ad hoc users (AUs) at random in a square region $\boldsymbol { \mathcal { A } } ( \boldsymbol { n } , \boldsymbol { A } ) = \left[ 1 , \sqrt { \boldsymbol { A } } \right] \times \left[ 1 , \sqrt { \boldsymbol { A } } \right]$ with $A \in [ 1 , n ] .$ . Each AU as a source chooses randomly d ad hoc nodes as its destinations, where $d : [ 1 , n ]$ . To add the support of infrastructures, we place regularly m base stations (BSs, with wireless transmitting power P) in $\scriptstyle A ( n , A )$ , as illustrated in Fig. 2, to construct the hybrid network. To be specific, divide Aðn; AÞ into m subregions with side length $\frac { \sqrt { A } } { \sqrt { m } }$ and place one BS on the center position of each subregion. We consider the scenario where the number of BSs is no more than the number of users, i.e., m : [1, n].

# 2.2. Communication model

Assume that all nodes transmit with a constant power $P ,$ and any pairs, say $\nu _ { i }$ and $\upsilon _ { j } ,$ can establish a direct communication link over a channel of bandwidth B, of rate $\begin{array} { r } { \mathbf { R } ( \nu _ { i } , \nu _ { j } ) = B \log \left( 1 + \frac { P \cdot \ell ( \nu _ { i } , \nu _ { j } ) } { N _ { 0 } + \sum _ { \nu _ { k } \in A ( i ) / \nu _ { i } } P \cdot \ell ( \nu _ { k } , \nu _ { j } ) } \right) } \end{array}$ where $N _ { 0 } > 0$ i s the ambient noise power, AðiÞ is the set of nodes that transmit when $\nu _ { i }$ is scheduled, and $\ell ( \upsilon _ { i } , \upsilon _ { j } )$ denotes the power attenuation function. Following the setting in [10,24,25], let $\ell ( \nu _ { i } , \nu _ { j } ) = d _ { i j } ^ { - \alpha }$ with the power attenuation exponent $\alpha > 2 .$ .

# 3. Main results

We design two alternative routing backbones, called sparse backbones and dense backbones, respectively. Two types of multicast schemes are proposed: hybrid scheme and BS-based scheme. The hybrid scheme can be further based on the sparse backbones or dense backbones. Consequently, three schemes are produced, i.e., hybrid scheme based on sparse backbones (H-SB scheme, $\mathbb { M } _ { \mathtt { H } - S \mathtt { B } } ) _ { \mathtt { \Gamma } }$ , hybrid scheme based on dense backbones (H-DB scheme, $\mathbb { M } _ { \mathrm { H - D B } } )$ , and BS-based scheme ${ \mathbb { M } } _ { \mathtt { B } }$ .

![](images/8d0e5975d07de14d87f398887dbda4ea99ba16be55ebf7fa186c32f91e31348a.jpg)



(a) Subregions Partitions

![](images/63101a2bd1270ab8f9a6ffac23124d746a9441a39449aabdd305a53d652aa72d.jpg)



(b) Cells Partitions   
Fig. 2. The small hexagons are the BSs that are placed in the center positions of the subregions of area $\textstyle { \frac { n } { m } } .$ The shaded small square is the source of a given multicast session. The small circles are the ordinary ad hoc nodes, and the shaded circles are the destinations of the given multicast session.

# 3.1. Optimal multicast throughput based on three schemes

By adopting cooperatively three schemes, we derive the optimal multicast throughput as described in Figs. 3 and 4 that are obtained by Theorems 8, 14 and 18. Please see the details of the results in Table 1.

# 3.2. Bottlenecks on base stations under schemes $\mathbb { M } _ { \mathrm { H } - S \mathrm { B } }$ and $\mathbb { M } _ { \mathrm { H - D B } }$ MHDB

According to the analysis of multicast throughput under the schemes ${ \mathbb { M } } _ { \mathrm { H } - S \mathrm { B } }$ and $\mathbb { M } _ { \mathrm { H - D B } }$ , the bottlenecks are both located on the wireless links between the ad hoc nodes and BSs, called B-O links. Note that this result holds under the assumption that BSs have the same capability as the ordinary ad hoc nodes when they transmit or receive data along the B-O links. Intuitively, this assumption is a bit conservative. We can improve further the network throughput by improving the capability of BSs. Hence, we purposely derive the multicast throughput under the schemes MHSB and ${ \mathbb { M } } _ { \mathrm { H } } .$ DB without considering the bottlenecks on BSs, which are presented in Theorems 12 and 16, respectively. We expect that these results can be directly exploited in the future work that introduces some communication techniques for BSs. For example, when BSs are permitted to receive the data from k ad hoc nodes simultaneously, the multicast throughput can increase to k times as long as the improved throughput via BSs does not exceed the throughput derived without considering bottlenecks on BSs (Theorem 12 or Theorem 16).

# 4. Multicast schemes

Our multicast schemes are cell-based, then we first give a notion called scheme lattice for succinctness of the description.

Definition 1 (Scheme lattice). Divide the deployment region $\boldsymbol { \mathcal { A } } ( n , A ) = \left\lceil 0 , \sqrt { A } \right\rceil ^ { 2 }$ into a lattice consisting of square cells of side length l, we call the lattice scheme lattice and denote it by $\mathbb { L } \left( { \sqrt { A } } , l \right) . ^ { 2 }$

# 4.1. Division of subregions

As illustrated in Fig. 2(b), the BS $b _ { i } , \ i = 1 , 2 , \dotsc , n ,$ , is placed in the center position of the ith cell (subregion) in $\mathbb { L } \left( { \sqrt { A } } , { \sqrt { A / m } } \right)$ after giving each BS and subregion a unique index in a certain order.

# 4.2. Routing backbones

We partition each subregion, denoted by $\mathcal { R } _ { i } ,$ into a lattice $\mathbb { L } _ { i } \left( { \sqrt { \frac { A } { m } } } , \operatorname* { m i n } \left\{ 3 { \sqrt { \frac { A \log n } { n } } } , { \sqrt { \frac { A } { m } } } \right\} \right)$ , where $i = 1 , 2 , \dots , m$ . We give a lemma to bound the number of ad hoc nodes in each cell. By using Lemma 20, we can easily obtain that

Lemma 1. For all cells in $\mathbb { L } _ { i } \left( { \sqrt { A / m } } \right.$ ; min $\{ 3 { \sqrt { A \log n / n } }  .$ $\sqrt { A / m } \} ) , i = 1 , 2 , \ldots , m _ { \mathrm { ~ } }$ , the number of nodes is w.h.p. of order H(N), where

![](images/30fd502a46e84723fa6376bf6354d48eab36c3dc07ca947bbdb694629e936d9c.jpg)



(a) $A : [ 1 , m ]$

![](images/e19af781d0196f04f930413c2b1add6470dcc14b59c2f973db43e0f22e286e49.jpg)



n logn]

![](images/d5e918bb73c24133a0639821766d9995839b42cb5011aa62ada3046235832b79.jpg)



n n

![](images/037118fb28411882f37d7cf3b227b249426c6884e34ca27745f0f85a899e03d3.jpg)



(d)A:( n   
Fig. 3. Illustrations of results for the case that m : $\left[ 1 , { \frac { n } { \log n } } \right]$ . Here, $\begin{array} { r } { \gamma = \frac { m } { d } . } \end{array}$ The relations between the optimal multicast throughput (y-axis) and c (x-axis) are

 $\mathbf { N } \in \left[ \frac { 9 } { 2 } \right.$ log n; 18 log n 
, when 3 ffiffiffiffiffiffiffiffiffiffiA logp ${ \overline { { n / n } } } \geqslant { \sqrt { A / m } } ,$ , i.e., m 6 n ; $\begin{array} { r } { m \leqslant \frac { n } { 9 \log n } ; } \end{array}$   
 $\mathbf { N } = O ( \bar { l o g n } )$ , when $3 { \sqrt { A \log n / n } } \leqslant { \sqrt { A / m } } ,$ i.e., $\begin{array} { r } { m \geqslant \frac { n } { 9 \log n } . } \end{array}$

When m 6 n9 log n, $\begin{array} { r } { m \leqslant \frac { n } { 9 \log n } , } \end{array}$ Based on the scheme lattice $\mathbb { L } _ { i } \biggl ( \sqrt { A / m } , 3 \sqrt { A \log n / n } \biggr )$ , we build the sparse backbones and dense backbones in each subregion $\mathcal { R } _ { i } ,$ for $i = 1 , 2 , \dots , m .$ .

# 4.2.1. Sparse backbones

We build the sparse backbones by the following operations: choose randomly one ad hoc node from each cell in $\mathbb { L } _ { i } { \Big ( } { \sqrt { A / m } } , 3 { \sqrt { A \log n / n } } { \Big ) }$ , called station; connect those stations in a pattern as illustrated in Fig. 5. Then, we get the sparse backbone system. The whole sparse backbone system can be scheduled by a 9-TDMA scheme, as illustrated in Fig. 5.

Lemma 2. Each sparse backbone can sustain a rate of order

$$
\mathbf {R} _ {\mathrm{SB}} (n, A) = \left\{ \begin{array}{l l} \Omega \left(\left(\frac {n}{\log n}\right) ^ {\frac {\alpha}{2}} \cdot A ^ {- \frac {\alpha}{2}}\right) & \text { when   } A: \left[ \frac {n}{\log n}, n \right], \\ \Omega (1) & \text { when   } A: \left[ 1, \frac {n}{\log n} \right]. \end{array} \right. \tag {1}
$$

Please see the proof in Appendix B.1.

# 4.2.2. Dense backbones

In the center of each cell of L $_ { \mathrm { i } } \left( { \sqrt { A / m } } , 3 { \sqrt { A \log n / n } } \right)$ , we set a smaller square of side length $2 { \sqrt { A \log n / n } } ,$ , as illustrated in Fig. 6, we call it station-cell. Then, by Eq. (A.2), we can prove that.

Lemma 3. For all station-cells, the number of ad hoc users (AUs) inside is w.h.p. at least of 2 log n.

![](images/d6313528c960ca8e4a8483629e47e93ec5ea56575efcb2f27bf45d6354e5e03d.jpg)



(a) A : [1,m]

![](images/0b0fd7b90c62b4a737fdb55689e9a6764e84dcd40316f54a1c5e72cf57a3e3b0.jpg)



(b) A : (m,n]   
Fig. 4. Illustrations of results for the case that m : $\scriptstyle \left( { \frac { n } { \log n } } , n \right] .$ . Here, $\begin{array} { r } { \gamma = \frac { m } { d } . } \end{array}$

Table 1 Optimal multicast scheme among the hybrid scheme based on sparse backbones (H-SB scheme, ${ \mathbb { M } } _ { \mathrm { H - S B } } ) ,$ hybrid scheme based on dense backbones (H-DB scheme, ${ \mathbb { M } } _ { \mathrm { H - D B } } ) ,$ and BS-based scheme $\mathbb { M } _ { \mathtt { B } } .$ . The corresponding throughputs are described in Figs. 3 and 4. 

<table><tr><td>Number of base stations</td><td>Area of deployment region</td><td>Optimal scheme</td></tr><tr><td rowspan="3"> $m : \left[1, \frac{n}{\log n}\right]$ </td><td> $A : [1,m]$ </td><td> $\mathbb{M}_{\text{B}}$ </td></tr><tr><td> $A : \left[m, \frac{n}{(\log n)^{1 - \frac{2}{n}}}\right]$ </td><td> $\mathbb{M}_{\text{H-SB}}$ </td></tr><tr><td> $A : \left[\frac{n}{(\log n)^{1 - \frac{2}{n}}}, n\right]$ </td><td> $\mathbb{M}_{\text{H-SB or }}$  $\mathbb{M}_{\text{H-DB}}$ </td></tr><tr><td> $m : \left(\frac{n}{\log n}, n\right]$ </td><td> $A : [1,n]$ </td><td> $\mathbb{M}_{\text{B}}$ </td></tr></table>

Thus, we can build the dense backbones by the following operations: choose randomly 2 logn nodes from each station-cell, and connect them with each other by a point-to-point pattern. As illustrated in Fig. 6, we will adopt a 4-TDMA scheme to schedule the dense backbone system. Note that there are 2logn links, instead of only one link, initiating from each station-cell to be scheduled simultaneously. Then, it holds that.

Lemma 4. The rate of each dense backbone can be sustained of order

$$
\mathbf {R} _ {\mathrm{DB}} (n, A) = \left\{ \begin{array}{l l} \Omega \left(\left(\frac {n}{\log n}\right) ^ {\frac {\alpha}{2}} \cdot A ^ {- \frac {\alpha}{2}}\right) & \text { when } A: \left[ \frac {n}{(\log n) ^ {1 - \frac {\alpha}{2}}}, n \right], \\ \Omega \left(\frac {1}{\log n}\right) & \text { when } A: \left[ 1, \frac {n}{(\log n) ^ {1 - \frac {2}{2}}} \right]. \end{array} \right. \tag {2}
$$

Please see the proof in Appendix B.2.

# 4.3. Multicast schemes

In general, there are two types of multicast routing schemes: shortest path trees and minimum cost trees, [18]. Our schemes belong to the latter type. For the multicast session $\mathcal { M } _ { k } , \ k = 1 , 2 , . . . n ,$ , denote the set of nodes by ${ \mathcal { U } } _ { k } = \{ \nu _ { k } \} \cup \{ \nu _ { k _ { 1 } } , \nu _ { k _ { 2 } } , \cdot \cdot \cdot \nu _ { k _ { d } } \}$ , where $\upsilon _ { k }$ is the source node and the nodes in the latter set are the destinations of $\upsilon _ { k } .$ . Let $\mathcal { U } _ { k } ^ { l } = \{ \nu _ { k _ { 1 } } ^ { l } , \nu _ { k _ { 2 } } ^ { l } , . . . , \nu _ { k _ { t } } ^ { l } \}$ denote the set of nodes that belong to $\mathcal { U } _ { k }$ and are located in the subregion $\mathcal { R } _ { l }$ , where $\mathcal { U } _ { k } = \cup \mathcal { U } _ { k } ^ { l }$ and $\mathcal { U } _ { k } ^ { l _ { 1 } } \cap \mathcal { U } _ { k } ^ { l _ { 2 } } = \emptyset$ for any $\begin{array} { r } { \iota _ { 1 } \neq \iota _ { 2 } . } \end{array}$ . Define $\widetilde { \mathcal { U } } _ { k } ^ { \iota } : = \mathcal { U } _ { k } ^ { \iota } \cup \{ b _ { \iota } \}$ , where $b _ { \imath }$ denotes the base station placed in subregion $\mathcal { R } _ { \imath } .$ . Then, we can construct the Euclidean spanning tree (EST) based on every set $\widetilde { \mathcal { U } } _ { k } ^ { \iota }$ by using the method in [29], described in Algorithm 1. Denote those ESTs as ESTðUe i Þ; $1 \leqslant \iota \leqslant \nu _ { k } ,$ , where $\nu _ { k }$ is a random variable that represents the number of subregions containing at least one ad hoc node in $\boldsymbol { \mathcal { U } } _ { k } .$ .

# Algorithm 1: Construction of EST $\left( \widetilde { \mathcal { U } } _ { k } ^ { \iota } \right)$

Input : The set of nodes $\widetilde { \mathcal { U } } _ { k } ^ { \iota }$

Output : An Euclidean spanning tree $\mathrm { E S T } ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$

1: In the initial state, all nodes of $\widetilde { \mathcal { U } } _ { k } ^ { \iota }$ are isolated, then there are $d + 1$ connected components.

2: for i = 1 : d do

3: Partition the deployment region $\textstyle A ( n , A )$ into at most $d + 1 - i$ square cells, each with side length $\textstyle \frac { \sqrt { A } } { \left[ \sqrt { d + 1 - i } \right] } ;$

4: Find a cell that contains two nodes of $\widetilde { \mathcal { U } } _ { k } ^ { \iota }$ that belong to two different connected components. By connecting the pair of nodes, we merge the two connected components.

5: end for

Note that for all $\widetilde { \mathcal { U } } _ { k } ^ { \iota }$ except for that one including $\upsilon _ { k }$ denoted as $\widetilde { \mathcal { U } } _ { k } ^ { \iota _ { o } }$ , we set $b _ { \imath }$ as the source; for $\widetilde { \mathcal { U } } _ { k } ^ { \iota _ { o } }$ , we set vk as the source. According to Lemma 3 and Lemma 10 in [17], we have the following lemma.

![](images/5febee900301b7bc3e93be482e5b572ba3b9847e6ca8a5920388101252ac6f9b.jpg)



Fig. 5. Sparse backbones. The shaded cells can be scheduled simultaneously. In any time slot, there are exactly one link initiated from every activated station-cell.

![](images/c80179e31ff99ae2ce9fc950b7d1f0831bcf69365fb6a90e92dfa8025e1eead9.jpg)



Fig. 6. Dense backbones. There is one station-cell centered at each cell of $\mathbb { L } _ { i } \Big ( \sqrt { A / m } , 3 L \Big )$ , where $L = { \sqrt { A } }$ ffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffilog n=n. The shaded station-cells can be scheduled simultaneously. In any time slot, there are 2 logn concurrent links initiated from every activated station-cell.

Lemma 5. With high probability, $\nu _ { k } = \theta ( \operatorname* { m i n } \{ d , m \} )$ for $k ,$ $1 \leqslant k \leqslant n .$ .

# 4.3.1. BS-based scheme ${ \mathbb { M } } _ { \mathtt { B } }$

We adopt a classical BS-based scheme, in which sources deliver data to BSs during the uplink phase and BSs deliver

received data to destinations during the downlink phase, as illustrated in Fig. 7(a). We present the multicast scheme ${ \mathbb { M } } _ { \mathtt { B } }$ as follows:

(1) During the uplink phase, for $\iota = 1 , 2 , \ldots , m$ , the source node in the subregion $\mathcal { R } _ { l }$ transmits the packets to the BS $b _ { \imath \cdot }$ .

(2) For $k = 1 , 2 , \ldots , n ,$ the BS receiving the packets from source $\upsilon _ { k }$ delivers packets to the BSs that are placed in the subregions containing the destinations of $\upsilon _ { k }$ via BS-to-BS links.   
(3) During the downlink phase, for $k = 1 , 2 , \ldots , n$ and $\iota = 1 , 2 , \ldots , m ,$ , the BS $b _ { \imath }$ delivers the packets to the destinations of source $\upsilon _ { k }$ that are located in the subregion $\mathcal { R } _ { l }$ .

Due to the regular position of BSs, we can simultaneously schedule all subregions in both uplink and downlink phases. We have

Lemma 6. Under the scheme ${ \mathbb { M } } _ { \mathrm { B } }$ , each subregion can sustain a rate of order

$$
\mathbf {R} _ {\mathrm{B}} (n, A) = \left\{ \begin{array}{l l} \Omega \left(\left(\frac {m}{A}\right) ^ {\frac {2}{2}}\right) & \text { when   } A: [ m, n ], \\ \Omega (1) & \text { when   } A: [ 1, m ], \end{array} \right. \tag {3}
$$

during both downlink and uplink phases.

Proof. We consider the uplink phase. All subregions are simultaneously scheduled; in each subregion, there is exactly one link from a transmitter to the BS to be permitted. For any link in any time slot, the transmitters in the eight closest cells are located at Euclidean distance at least ${ \frac { 1 } { 2 } } \cdot { \sqrt { \frac { A } { m } } }$ from the receiver (BS); the 16 next closest cells are at Euclidean distance at least ${ \frac { 3 } { 2 } } \cdot { \sqrt { \frac { A } { m } } } ,$ and so on. By extending the sum of the interferences to the whole region, this can then be bounded as follows:

$$
\begin{array}{l} \mathrm{I} (n, A) \leqslant \sum_ {i = 1} ^ {n} 8 i P \cdot \ell \left(\left(i - \frac {1}{2}\right) \cdot \sqrt {\frac {A}{m}}\right) \\ \leqslant 8 \cdot P \cdot \left(\frac {A}{m}\right) ^ {\frac {\alpha}{2}} \cdot \sum_ {i = 1} ^ {\infty} \frac {i}{\left(i - \frac {1}{2}\right) ^ {\alpha}}, \\ \end{array}
$$

since $\alpha > 2$ , we get that $\operatorname { I } ( n , A ) = O ( ( { \frac { m } { A } } ) ^ { \frac { \alpha } { 2 } } )$ . Because the distance of every hop is at most of ${ \frac { \sqrt { 2 } } { 2 } } \cdot { \sqrt { A / m } } ,$ , the signal strength at the receiver can be bounded as $\begin{array} { r } { S ( n , A ) = \Omega \Big ( \big ( \frac { m } { A } \big ) ^ { \frac { \alpha } { 2 } } \Big ) } \end{array}$ . Thus,

$$
\begin{array}{l} \mathbf {R} (n, A) = B \log \left(1 + \frac {S (n , A)}{N _ {0} + I (n , A)}\right) \\ = \left\{ \begin{array}{l l} \Omega \Big (\big (\frac {m}{A} \big) ^ {\frac {\alpha}{2}} \Big) & \text { when } A: [ m, n ], \\ \Omega (1) & \text { when } A: [ 1, m ]. \end{array} \right. \\ \end{array}
$$

Hence, the lemma holds. h

Next, we consider the load of each subregion during the downlink phase and uplink phase. We have

Lemma 7. Under the scheme ${ \mathbb { M } } _ { \mathrm { B } } ,$ , the load of each subregion is of order

$$
\mathbf {L} _ {\mathrm{B}} = \left\{ \begin{array}{l l} O \left(\frac {\log \gamma}{\log \frac {\gamma \log \gamma}{n}}\right) & \text { when   } \gamma = \Omega (1) \text {   and   } \gamma \cdot \log \gamma = \Omega (n), \\ O \left(\frac {n}{\gamma}\right) & \text { when   } \gamma = \Omega (1) \text {   and   } \gamma \cdot \log \gamma = O (n), \\ O (n) & \text { when   } \gamma = O (1), \end{array} \right. \tag {4}
$$

where $\begin{array} { r } { \gamma = \gamma ( m , d ) : = \frac { m } { d } . } \end{array}$

![](images/d77088282e6da2063191a380c05a08cfcb1c646a45a7770276d70cd8a2f9820d.jpg)



(a) BS-based Scheme

![](images/dd5576b30a1a0b3be72c6ddc623b79e13194b3ac7477ba8f269a1ca276dcad89.jpg)



(b) Hybrid Scheme   
Fig. 7. Multicast schemes. (a) BS-based Scheme. The sources directly transmit data to BSs during the uplink phase and BSs also directly deliver received data to destinations during the downlink phase. (b) Hybrid Scheme. In each subregion, the data are transported to the BS by a multihop pattern. The communications between the ad hoc nodes in different subregions are relayed by the corresponding BSs.

Proof. Define an event $\textstyle E _ { \mathrm { B } } ( k , t ) \colon$ The subregion $\mathcal { R } _ { t }$ contains a node belonging to $\mathcal { U } _ { k } .$ . Then, $\begin{array} { r } { \operatorname* { P r } ( E _ { 8 } ( k , t ) ) \leqslant \frac { d } { m } = \frac { 1 } { \nu } , } \end{array}$ for any $t = 1 , 2 , \ldots , m$ . Then, the load of each subregion is no more than ${ \bf L } ( n , \ \gamma )$ , where $\begin{array} { r } { \gamma = \gamma ( m , d ) : = \frac { m } { d } } \end{array}$ and ${ \bf L } ( n , \gamma )$ denotes the maximum number of balls in any bin when n balls are independently and uniformly at random thrown into $\gamma$ bins. Note that we assume that $\gamma$ is an integer, which has no impact on the result in order sense. According to Lemma 19, we can obtain Eq. (4), which completes the proof. h

Combining Lemmas 6 and 7, we finally get the following theorem.

Theorem 8. Under the scheme ${ \mathbb { M } } _ { \mathrm { B } } ,$ , the multicast throughput can be achieved of

$$
\Lambda_ {\mathrm{B}} = \mathbf {R} _ {\mathrm{B}} / \mathbf {L} _ {\mathrm{B}}, \tag {5}
$$

where $\mathbf { R } _ { B }$ and $\mathbf { L } _ { B }$ are defined in Eqs. (3) and (4), respectively.

# 4.3.2. Hybrid schemes based on sparse backbones ${ \mathbb { M } } _ { \mathrm { H } } .$ SB

We first design Algorithm 2 to construct the multicast routing tree $\mathcal { T } _ { \mathtt { H } - \mathtt { S B } } ( \mathcal { U } _ { k } )$ for a given multicast session $\mathcal { M } _ { k } .$ .

# Algorithm 2: Multicast Routing Scheme of ${ \mathbb { M } } _ { \mathrm { H } } .$ SB

Input: $\mathrm { E S T } \Big ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } \Big ) , 1 \leqslant \iota \leqslant \nu _ { k } .$

Output: A multicast routing tree $\mathcal { T } _ { \mathrm { H - S B } } ( \mathcal { U } _ { k } )$

1: for each EST $( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
2: for each link $u _ { i } u _ { j }$ in EST $( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
3: Connect $u _ { i }$ and ujby using the following Manhattan routing:

Denote the intersection point of the horizontal line through $u _ { i }$ and the vertical line through $u _ { j }$ as $p _ { i , j } ,$ and denote the nearest node to $p _ { i , j }$ by $u _ { i , j } ,$ connect $u _ { i }$ and $u _ { i , j }$ by the corresponding horizontal sparse backbone, and connect $u _ { i , j }$ and $u _ { j }$ by the corresponding vertical sparse backbone.

4: end for   
5: Merge the same edges (hops) and remove the circles that have no impact on the connectivity of $\mathrm { E S T } ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ , we obtain the multicast tree $\tau _ { \mathrm { H } } .$ SB $( \mathcal { U } _ { k } ^ { l } )$ .   
6: end for   
7: Based on the forest consisting of the constructed trees, i.e., $\mathcal { T } _ { \mathrm { H - S B } } ( \mathcal { U } _ { k } ^ { l } ) ( 1 \leqslant \iota \leqslant \nu _ { k } )$ , we obtain the final multicast tree $\mathcal { T } _ { \mathrm { H - S B } } ( \mathcal { U } _ { k } )$ by building an EST spanning the set of base stations $b _ { \imath } ( 1 \leqslant \imath \leqslant \nu _ { k } ) .$ .

From Lemma 2, we can get the rate that can be sustained by every sparse backbone. Next, we aim to derive the maximum burden of each sparse backbone under the scheme M H-SB.

Above all, we recall a useful result in [29].

Lemma 9. Using Algorithm 1 with the input of U (a set of nodes) to built the Euclidean spanning tree spanning U, denoted by ESTðUÞ, it holds that

$$
\left\| \operatorname{EST} (\mathcal {U}) \right\| \leqslant 2 \sqrt {2} \sqrt {| \mathcal {U} |} \cdot \sqrt {A},
$$

where A is the area of the deployment square region and jUj denotes the cardinally of the set U.

Denote the forest consisting of all $\mathrm { E S T } ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } ) ( 1 \leqslant \iota \leqslant \nu _ { k } )$ , by ${ \mathcal { F } } _ { k } .$ . Then, we have

Lemma 10. With high probability, the total Euclidean edge length of $\| \mathcal F _ { k } \|$ is of order $\begin{array} { r } { O \left( \sqrt { \frac { A \cdot d \cdot \operatorname* { m i n } \{ d , m \} } { m } } \right) } \end{array}$ , for any k, $1 \leqslant k \leqslant n .$ .

Proof. Denote the number of vertexes of $\ E S \mathrm { T } ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ as $\boldsymbol { x } _ { k } ^ { l } ,$ , where $1 \leqslant \iota \leqslant \nu _ { k }$ and $1 \leqslant k \leqslant n .$ . According to Lemma 9, $\begin{array} { r } { \left\| \mathrm { E S T } \Big ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } \Big ) \right\| = O \Big ( \sqrt { x _ { k } ^ { \iota } } \cdot \frac { \sqrt { A } } { \sqrt { m } } \Big ) } \end{array}$ . Hence, there exists a constant $\kappa _ { 1 }$ such that

$$
\| \mathcal {F} _ {k} \| = \sum_ {\iota = 1} ^ {v _ {k}} \| \mathrm{EST} (\widetilde {\mathcal {U}} _ {k} ^ {\iota}) \| \leqslant \frac {\kappa_ {1} \sqrt {A}}{\sqrt {m}} \cdot \sum_ {\iota = 1} ^ {v _ {k}} \sqrt {x _ {k} ^ {\iota}}.
$$

By Cauchy–Schwartz Inequality, we have

$$
\sum_ {i = 1} ^ {v _ {k}} \sqrt {x _ {k} ^ {i}} \leqslant \sqrt {v _ {k} \cdot \sum_ {i = 1} ^ {v _ {k}} x _ {k} ^ {i}} \leqslant \sqrt {v _ {k} \cdot (v _ {k} + d)} \leqslant \sqrt {2 d \cdot v _ {k}}.
$$

Then, $\begin{array} { r } { \| \mathcal { F } _ { k } \| = O \Big ( \frac { \sqrt { A } } { \sqrt { m } } \cdot \sqrt { d \cdot \nu _ { k } } \Big ) } \end{array}$ , which completes the proof. h

Lemma 11. Under the scheme ${ \mathbb { M } } _ { \mathrm { H } - S \mathrm { B } } ,$ , the burden of each sparse backbone is of

$$
\mathbf {L} _ {\mathrm{H-SB}, 1} = \left\{ \begin{array}{l l} O (d \cdot \sqrt {\frac {n \log n}{m}}) & \text { when   } d = O (m), \\ O (\sqrt {n \cdot d \cdot \log n}) & \text { when   } d = \Omega (m) \text {   and   } d = O (\frac {n}{\log n}), \\ O (n) & \text { when   } d = \Omega \left(\frac {n}{\log n}\right). \end{array} \right. \tag {6}
$$

Proof. Given a station on a sparse backbone, say $s _ { t } ,$ define an event $E _ { \mathrm { H - S B } , 1 } ( k , t ) ;$ The multicast session $\mathcal { M } _ { k }$ passes through $s _ { t } .$ Obviously, $E _ { \mathrm { H - S B } , 1 } ( k , t )$ happens if there exists an edge $u _ { i } u _ { j } \in \mathcal { F } _ { k }$ to be routed through $s _ { t } , i . e . , u _ { i } u _ { i , j }$ or $u _ { i , j } u _ { j }$ passes through $s _ { t } .$ Hence, by $| u _ { i } u _ { i , j } | + | u _ { i , j } u _ { j } | \leqslant \sqrt { 2 } | u _ { i } u _ { j } |$ j,

$$
\begin{array}{l} \operatorname * {P r} (E _ {\mathrm{H-SB}, 1} (k, t)) \\ \leqslant \frac {3 \sqrt {A \log n / n}}{\sqrt {A}}. \frac {\sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} \left(| u _ {i} u _ {i , j} | + | u _ {i , j} u _ {j} | + 2 \cdot 3 \sqrt {A \log n / n}\right)}{\sqrt {A}} \\ \leqslant 1 8 \log n / n \cdot (d + v _ {k}) + 3 \sqrt {\frac {2 \log n}{A n}} \cdot \sum_ {u _ {i} u _ {j} \in \mathcal {F} _ {k}} | u _ {i} u _ {j} | \\ \leqslant 3 6 d \log n / n + 3 \sqrt {\frac {2 \log n}{A n}} \cdot \| \mathcal {F} _ {k} \| \\ \leqslant 3 6 d \log n / n + 3 \kappa_ {2} \sqrt {2 \log n / n} \cdot \sqrt {\frac {d \cdot \min \{d , m \}}{m}}, \\ \end{array}
$$

where $\kappa _ { 2 }$ is a constant and the last inequality supported by Lemma 10. That ${ \mathrm { i } } s ,$ $\operatorname* { P r } ( E _ { \mathrm { \ H - S B } , 1 } ( k , t ) ) = O \Big ( \frac { d \log n } { n } +$ d log n þ ${ \sqrt { \frac { \log n } { n } } } \cdot { \sqrt { \frac { d \cdot \operatorname* { m i n } \{ d , m \} } { m } } } \quad$ dminfd;mgm Þ. According to Lemma 11, we get Eq. (6), and complete the proof. h

Combining Lemmas 2 and 11, we can obtain Theorem 12.

Theorem 12. Under the scheme ${ \mathbb { M } } _ { \mathrm { H } } .$ SB, taking no account of the possible bottleneck on BSs, the multicast throughput can be achieved of

$$
\Lambda_ {\mathrm{H} - \mathrm{SB}, 1} = \mathbf {R} _ {\mathrm{H} - \mathrm{SB}} / \mathbf {L} _ {\mathrm{H} - \mathrm{SB}, 1}, \tag {7}
$$

where $\mathbf { R } _ { H - S B }$ and $\mathbf { L } _ { H - S B , 1 }$ are defined in Eqs. (1) and (6), respectively.

Next, we consider the throughput via BSs. Based on Lemmas 2 and 7, it is easy to obtain that,

Lemma 13. Under the scheme ${ \mathbb { M } } _ { \mathrm { H } - S \mathrm { B } } ,$ , the throughput via BSs can be achieved of

$$
\Lambda_ {\mathrm{H-SB}, 2} = \mathbf {R} _ {\mathrm{H-SB}} / \mathbf {L} _ {\mathrm{B}}, \tag {8}
$$

where $\mathbf { R } _ { H - S B }$ and $\mathbf { L } _ { B }$ are defined in Eqs. (1) and (4), respectively.

Combining Theorem 12 and Lemma 13, we can prove Theorem 14.

Theorem 14. Under the scheme ${ \mathbb { M } } _ { \mathrm { H } - S \mathrm { B } } ,$ , the multicast throughput is achieved of

$$
\Lambda_ {\mathrm{H} - \mathrm{SB}} = \min \left\{\Lambda_ {\mathrm{H} - \mathrm{SB}, 1}, \Lambda_ {\mathrm{H} - \mathrm{SB}, 2} \right\} = \Lambda_ {\mathrm{H} - \mathrm{SB}, 2}, \tag {9}
$$

where KH-SB,1 and KH-SB,2 are defined in Eqs. (7) and (8), respectively.

4.3.3. Hybrid schemes based on dense backbones ${ \mathbb { M } } _ { \mathrm { H } } .$ DB We first design the multicast routing in Algorithm 3.

# Algorithm 3: Multicast Routing scheme of $\mathbb { M } _ { \mathrm { H - D B } }$

Input: $\mathrm { E S T } ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ ; $1 \leqslant \iota \leqslant \nu _ { k } .$

Output: A multicast routing tree $\mathcal { T } _ { \mathrm { H - D B } } ( \mathcal { U } _ { k } ) .$

1: for each $\mathrm { E S T } ( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ do   
2: for each link uiuj in EST $\left( \widetilde { \mathcal { U } } _ { k } ^ { \iota } \right)$ do   
3: Connect $u _ { i }$ to $u _ { j }$ by using Manhattan routing via the dense backbones.   
4: end for   
5: Merge the same edges (hops) and remove the circles that have no impact on the connectivity of EST $( \widetilde { \mathcal { U } } _ { k } ^ { \iota } )$ , we obtain the multicast tree $\mathcal { T } _ { \mathrm { H - D B } } ( \mathcal { U } _ { k } ^ { l } ) .$ .   
6: end for   
7: Based on the forest consisting of the constructed trees, i.e., $\mathcal { T } _ { \mathrm { H - D B } } ( \mathcal { U } _ { k } ^ { \iota } ) ( 1 \leqslant \iota \leqslant \nu _ { k } )$ , we obtain the final multicast tree $\mathcal { T } _ { \mathrm { H - D B } } ( \mathcal { U } _ { k } )$ by building an EST spanning the set of base stations $b _ { \iota } ( 1 \leqslant \iota \leqslant \nu _ { k } ) .$ .

Next, we consider the burden of each dense backbone under the scheme MHDB. By a similar procedure to the proof of Lemma 11, we can get that

Lemma 15. Under the scheme $\mathbb { M } _ { \mathrm { H - D B } }$ , the burden of each dense backbone is of

$$
\mathbf {L} _ {\mathrm{H-DB}, 1} = \left\{ \begin{array}{l l} O \left(\frac {d \sqrt {n}}{\sqrt {m \log n}}\right) & \text { when   } d: [ 1, m ] \\ O \left(\frac {\sqrt {n d}}{\sqrt {\log n}}\right) & \text { when   } d: \left[ m, \frac {n}{\log n} \right], \\ O (d) & \text { when   } d: \left[ \frac {n}{\log n}, n \right]. \end{array} \right. \tag {10}
$$

Combining Lemmas 4 and 15, we can obtain Theorem 16.

Theorem 16. Under the scheme ${ \mathbb { M } } _ { \mathrm { H } } .$ DB, taking no account of the possible bottleneck on BSs, the multicast throughput can be achieved of

$$
\Lambda_ {\mathrm{H} - \mathrm{DB}, 1} = \mathbf {R} _ {\mathrm{H} - \mathrm{DB}} / \mathbf {L} _ {\mathrm{H} - \mathrm{DB}, 1}, \tag {11}
$$

where $ { \mathbf { R } } _ { H - D B }$ and $\mathbf { L } _ { H - D B , 1 }$ are defined in Eqs. (2) and (10), respectively.

Next, we consider the throughput via BSs. It is easy to obtain that,

Lemma 17. Under the scheme $\mathbb { M } _ { \mathrm { H - D B } } ,$ , the throughput via BSs can be achieved of

$$
\Lambda_ {\mathrm{H} - \mathrm{DB}, 2} = \mathbf {R} _ {\mathrm{H} - \mathrm{DB}} / \mathbf {L} _ {\mathrm{B}}, \tag {12}
$$

where $ { \mathbf { R } } _ { H - D B }$ and $\mathbf { L } _ { B }$ are defined in Eqs. (2) and (4), respectively.

Combining Theorem 16 and Lemma 17, we can prove Theorem 18.

Theorem 18. Under the scheme MHDB, the multicast throughput is achieved of

$$
\Lambda_ {\mathrm{H} - \mathrm{DB}} = \min \left\{\Lambda_ {\mathrm{H} - \mathrm{DB}, 1}, \Lambda_ {\mathrm{H} - \mathrm{DB}, 2} \right\} = \Lambda_ {\mathrm{H} - \mathrm{DB}, 2}, \tag {13}
$$

where $A _ { H - D B , 1 }$ and $\scriptstyle A _ { H - D B , 2 }$ are defined in Eqs. (11) and (12), respectively.

# 5. Literature review

We limit the scope of this paper to the multicast at network layer [12,30,24,25] that is different from that at link layer, [31–35]. We review the related work on capacity scaling laws of static wireless networks, including wireless ad hoc networks and hybrid wireless networks.

# 5.1. Wireless ad hoc networks

Gupta and Kumar [1] studied the unicast capacity for dense networks under the protocol model (ProM) and physical model (PhyM). They showed that direct communication between source and destination pairs is not preferable, as the interference generated would preclude most of the other nodes from communicating. On the contrary, the optimal scheme is to confine to nearest neighbor communication and maximize the number of simultaneous transmissions (spatial reuse). However, this means that each packet has to be retransmitted many times before getting to the final destination, leading to a sublinear scaling of system throughput. Specifically, they obtained that the unicast throughput under ProM and PhyM for random dense networks is of order $\Omega { \Bigg ( } { \frac { 1 } { \sqrt { n \log n } } } { \Bigg ) }$ . Keshavarz-Haddad et al. [11] studied the broadcast capacity under ProM for an arbitrary network, and showed that the per session broadcast capacity is only of order H(1/n). Li [29] proved that by using the multicast scheme based on Euclidean spanning tree (EST) and Manhattan routing, the multicast capacity for random networks under ProM can be achieved of order $\Omega \left( { \frac { 1 } { \sqrt { d n \log n } } } \right)$ when $\begin{array} { r } { d = O \left( { \frac { n } { \log n } } \right) } \end{array}$ and is of order $\Omega \left( { \frac { 1 } { n } } \right)$ when $\begin{array} { r } { d = \Omega \Big ( \frac { n } { \log n } \Big ) } \end{array}$ log n Here, d denotes the number of destinations per multicast session. Shakkottai et al. [12] designed a novel routing scheme, called multicast comb, by which the achievable multicast throughput is of order $\Omega ( \frac { 1 } { \sqrt { n ^ { \epsilon } \log n } } )$ when the number of multicast sources is $n ^ { \epsilon }$ , for some $\epsilon > 0 ,$ , and the number of destinations per multicast session is $n ^ { 1 - \epsilon }$ .

By introducing the percolation-based routing, Franceschetti et al. [10] proved that the unicast throughput under the Gaussian channel model (GCM) for both random dense networks and random extended networks, can be achieved of order $\Omega ( 1 / \sqrt { n } )$ . Also based on the percolation theory [36], Zheng [37] proved that the broadcast capacity for random extended networks is of order H $\left( { \frac { 1 } { n } } \cdot ( \log n ) ^ { - { \frac { \alpha } { 2 } } } \right)$ , where a is the power attenuation exponent of GCM. Later, Li et al. [24] showed that, when $\begin{array} { r } { d = O \Big ( \frac { n } { ( \log n ) ^ { 2 x + 6 } } \Big ) } \end{array}$ ðlog nÞ2aþ6 and $n = \Omega \Big ( n ^ { \frac { 1 } { 2 } + \theta } \Big )$ , the multicast throughput for random networks can be achieved of $\begin{array} { r } { \Omega \left( \frac { \sqrt { n } } { n \sqrt { d } } \right) } \end{array}$ . Wang et al. [25] improved the threshold of d above to $\begin{array} { r } { d = O \Big ( \frac { n } { ( \log n ) ^ { \alpha + 1 } } \Big ) } \end{array}$ O nðlog nÞaþ1  by designing a technique called parallel scheduling scheme. Keshavarz-Haddad and Riedi [27,28] proposed a useful technical tool called arena to study upper bounds of capacity, and designed a scheme to derive the achievable multicast throughput for random dense networks.

# 5.2. Hybrid wireless networks

Earlier, Liu et al. [5] introduced a network model where m base stations (BSs) are regularly placed and n ad hoc nodes are randomly distributed in a deployment region of fixed area. The results of [5] showed that if m grows asymptotically slower than ${ \sqrt { n } } ,$ , the benefit of adding base stations on unicast capacity is insignificant. However, if m grows faster than ${ \sqrt { n } } ,$ , the unicast capacity increases linearly with the number of base stations. The scaling model of [5] is indeed the hybrid dense network that can be regarded as a special case of the model of this paper by letting A = 1. Note that the results in [5] are derived under the protocol model (ProM). Also adopting the ProM, Mao et al. examined the multicast capacity of hybrid wireless networks for the case of $\begin{array} { r } { m = O \left( \frac { n } { \log n } \right) } \end{array}$ . A characteristic of the work in [17] is that the network is with a general node density as in the model of this paper. However, they assumed that the communication range under the ProM can increase linearly with the side-length of deployment region, i.e., ffiffiffiA . That implies that the transmitting power of each ad hoc nodes will enhance to infinity when the area of deployment region goes to infinity. It is obviously unrealistic for the practical wireless networks where all users (ad hoc nodes) are power-limited. Thus, the results of [17] are only applicable to the hybrid dense networks indeed for which the ProM is reasonable, [13,25]. There are also some other works to study the unicast capacity under ProM for hybrid dense networks, such as [15,38,39]. Later, as another representative scaling model, the hybrid extended network was studied by [16,26]. Taking the limitation of ProM and PhyM into account, both works properly adopted the Gaussian channel model (GCM), i.e., the generalize physical model. Liu et al. [16] focused on the unicast capacity for hybrid extended networks, and showed that the condition $m = \Omega ( { \sqrt { n } } )$ is also necessary to obtain a linear gain of unicast capacity under GCM for hybrid extended networks. While, Wang et al. [26] investigated the multicast capacity under GCM only for hybrid extended networks. Compared to [26], our work in this paper is more general in terms of scaling models, which can offer more insights about the scaling behaviors for hybrid wireless networks. Besides this, by introducing the sparse backbone system, instead of the parallel connectivity paths system in [26], we can further improve the multicast throughput for the case that $m = \varOmega ( d )$ and $\begin{array} { r } { \frac { m } { d } \log \frac { m } { d } = \Omega ( n ) } \end{array}$ .

# 6. Conclusion

We study the achievable multicast throughput for the hybrid wireless network with a general node density under Gaussian Channel model. As in most existing works for the capacity of hybrid wireless networks, we also assume that the links between base stations and ordinary ad hoc nodes (we call such links B-O links) have the same bandwidth as links between ordinary ad hoc nodes. While, we prove that under the hybrid schemes the bottlenecks are located on B-O links. Therefore, if the bandwidth of B-O links can be increased, the throughput of the network can be enhanced. We designedly derive the multicast throughput without considering the possible bottlenecks on the B-O links. These results could be used when some new assumptions are made for the B-O links.

Since our schemes do not use the method based on percolation theory [36], it is a future work to improve the throughput by exploiting the connection between percolation theory and the way to scale the transmission ranges of nodes [10]. On the other hand, due to not using percolation theory, our schemes have no bottleneck on the accessing paths into the highways [10,28,24,25]. Hence, for some cases of n and $d ,$ our schemes can act as the complements of those schemes based on percolation routing [10,24,25].

Finally, to the best of our knowledge, even for pure wireless ad hoc networks, there are still no matching upper bounds and lower bounds for multicast capacity under Gaussian Channel model. The same question holds for hybrid networks. Then, it is also an interesting issue to be studied.

# Acknowledgments

The authors thank the anonymous reviewers for their constructive comments. The research of authors is partially supported by the National Basic Research Program of China (973 Program) under Grant No. 2010CB328101, the Program for Changjiang Scholars and Innovative Research Team in University, the Shanghai Key Basic Research Project under Grant Nos. 10DJ1400300, the NSF CNS-0832120, the National Natural Science Foundation of China under Grant Nos. 60828003 and 61003277, the Program for Zhejiang Provincial Key Innovative Research Team, and the Program for Zhejiang Provincial Overseas High-Level Talents.

# Appendix A. Useful known results

# A.1. Useful results of occupancy theory

We use the results on the maximum occupancy to derive the lower bounds of the multicast throughput. We recall the following result from [40–42].

Lemma 19. Let $\mathbf { L } ( m , n )$ be the random variable that counts the maximum number of balls in any bin, if we throw m balls independently and uniformly at random into n bins. Then, it holds $w . h . p .$ that,

$$
\mathbf {L} (m, n) = \left\{ \begin{array}{l l} \Theta \left(\frac {\log n}{\log \frac {n}{m}}\right) & \text { when   } m: \left[ 1, \frac {n}{\text { polylog } (n)}\right) \\ \Theta \left(\frac {\log n}{\log \frac {n \log n}{m}}\right) & \text { when   } m: \left[ \frac {n}{\text { polylog } (n)}, n \log n\right) \\ \Theta \left(\frac {m}{n}\right) & \text { when   } m = \Omega (n \log n) \end{array} \right. \tag {A.1}
$$

# A.2. The tail of binomial distribution

Lemma 20 [43]. Consider n independent random variables $X _ { i } \in \{ 0 , 1 \}$ with $p = P r ( X _ { i } = 1 )$ . Let $\begin{array} { r } { \bar { X = \sum _ { i = 1 } ^ { n } X _ { i } } } \end{array}$ . Then,

$$
\operatorname * {P r} (X \leqslant \xi) \leqslant e ^ {\frac {- 2 \cdot (n \cdot p - \xi) ^ {2}}{n}} \quad \text { when } 0 <   \xi \leqslant n \cdot p, \tag {A.2}
$$

$$
\operatorname * {P r} (X > \xi) \leqslant \frac {\xi \cdot (1 - p)}{(\xi - n \cdot p) ^ {2}} \quad \text { when   } \xi > n \cdot p. \tag {A.3}
$$

# Appendix B. Proofs of some lemmas

# B.1. Proof of Lemma 2

Proof. For any link on the sparse backbone in any time slot, the transmitters in the eight closest cells are located at Euclidean distance at least $3 { \sqrt { A \log n / n } }$ from the receiver; the 16 next closest cells are at Euclidean distance at least $4 \times \left( 3 { \sqrt { A \log n / n } } \right)$ , and so on. By extending the sum of the interferences to the whole region, this can then be bounded as follows:

$$
\begin{array}{l} \mathrm{I} (n, A) \leqslant \sum_ {i = 1} ^ {n} 8 i P \cdot \ell \left((3 i - 2) \cdot 3 \sqrt {\frac {A \log n}{n}}\right) \\ \leqslant 9 ^ {1 - \frac {\alpha}{2}} \cdot P \cdot \left(\frac {n}{A \log n}\right) ^ {\frac {\alpha}{2}} \cdot \sum_ {i = 1} ^ {\infty} \frac {i}{(3 i - 2) ^ {\alpha}} \\ \end{array}
$$

since $\alpha > 2 ,$ , we get that $\begin{array} { r } { \mathrm { I } ( n , A ) = O \bigg ( \bigg ( \frac { n } { A \log n } \bigg ) ^ { \frac { \alpha } { 2 } } \bigg ) } \end{array}$ A log n . Because the distance of every hop is at most of ${ \sqrt { 5 } } \cdot 3 { \sqrt { A \log n / n } } ,$ , the signal strength at the receiver can be bounded as $\mathsf { S } ( n , A ) \geqslant 4 5 ^ { - \frac { \alpha } { 2 } } P \cdot ( n / A \log n ) ^ { \frac { \alpha } { 2 } }$ :Then, $\begin{array} { r } { S ( n , A ) = \Omega \bigg ( \bigg ( \frac { n } { A \log n } \bigg ) ^ { \frac { \alpha } { 2 } } \bigg ) } \end{array}$ . Thus,

$$
\begin{array}{l} \mathbf {R} (n, A) = \frac {1}{9} \cdot B \log \left(1 + \frac {S (n , A)}{N _ {0} + I (n , A)}\right) \\ = \left\{ \begin{array}{l l} \Omega \bigg (\Big (\frac {n}{\log n} \Big) ^ {\frac {\alpha}{2}} \cdot A ^ {- \frac {\alpha}{2}} \bigg) & \text {when} A: \Big [ \frac {n}{\log n}, n \Big ], \\ \Omega (1) & \text {when} A: \Big [ 1, \frac {n}{\log n} \Big ]. \end{array} \right. \\ \end{array}
$$

Hence, the lemma holds. h

# B.2. Proof of Lemma 4

Proof. Let $\begin{array} { r } { \lambda : = \frac { n } { A } . } \end{array}$ For any link on the dense backbone in any time slot, since the length of the link is at least of ${ \sqrt { A \log n / n } } ,$ , we can bound the sum of interferences to the receivers as:

$$
\begin{array}{l} \mathrm{I} (n, A) \leqslant P \cdot (2 \log n - 1) \cdot \ell \left(\sqrt {\frac {\log n}{\lambda}}\right) + \sum_ {i = 1} ^ {n} 8 i \cdot P \cdot (2 \log n) \\ \times \ell \left(\left((2 i - 2) \times 3 + 1\right) \cdot \sqrt {\frac {\log n}{\lambda}}\right) \\ \leqslant 2 ^ {1 - \frac {3}{2} \alpha} \cdot (\log n) ^ {1 - \frac {\alpha}{2}} \cdot \lambda^ {\frac {\alpha}{2}} \times \left(1 + \lim _ {n \rightarrow \infty} \sum_ {i = 1} ^ {n} \frac {8 i}{(6 i - 5) ^ {\alpha}}\right). \\ \end{array}
$$

The latest limitation obviously converges when $\alpha > 2 .$ Then,

$$
\mathrm{I} (n, A) = O \left(\left(\log n\right) ^ {1 - \frac {\alpha}{2}} \cdot \lambda^ {\frac {\alpha}{2}}\right). \tag {B.1}
$$

Since the distance of every hop is at most ${ \sqrt { 2 ^ { 2 } + 5 ^ { 2 } } } \cdot \left( { \sqrt { \log n / \lambda } } \right)$ , we have the signal $S ( n , A )$ at the receiver can be bounded as

$$
S (n, A) \geqslant P \cdot 2 9 ^ {- \frac {\alpha}{2}} \cdot (\log n) ^ {- \frac {\alpha}{2}} \cdot \lambda^ {\frac {\alpha}{2}}.
$$

Then, we get that

$$
S (n, A) = \Omega \left(\left(\log n\right) ^ {- \frac {\alpha}{2}} \cdot \lambda^ {\frac {\alpha}{2}}\right). \tag {B.2}
$$

From Eqs. (B.1) and (B.2), we have:

Case 1: When $\lambda : \left[ 1 , ( \log n ) ^ { 1 - \frac { 2 } { \alpha } } \right]$ , it holds that $\begin{array} { r } { \frac { S ( n , A ) } { N _ { 0 } + \mathrm { I } ( n , A ) } : \left[ \frac { \lambda ^ { \frac { \alpha } { 2 } } } { ( \log n ) ^ { \frac { \alpha } { 2 } } } , 1 \right) } \end{array}$ : k a2ðlog nÞ a2 ; 1 , then,

$$
\mathbf {R} (n, A) = \frac {1}{4} \cdot B \log \left(1 + \frac {S (n , A)}{N _ {0} + I (n , A)}\right) = \Omega \left(\frac {\lambda^ {\frac {\alpha}{2}}}{(\log n) ^ {\frac {\alpha}{2}}}\right).
$$

Case 2: When $\lambda : \left[ \left( \log n \right) ^ { 1 - \frac { 2 } { \alpha } } , n \right]$ , it holds that $\begin{array} { r } { \frac { S ( n , A ) } { N _ { 0 } + \mathrm { I } ( n , A ) } = \Omega \Big ( \frac { 1 } { \log n } \Big ) } \end{array}$ , then, $\begin{array} { r } { \mathbf { R } ( n , A ) = \Omega \left( \frac { 1 } { \log n } \right) } \end{array}$

Combining two cases, we complete the proof. h

# References

[1] P. Gupta, P.R. Kumar, The capacity of wireless networks, IEEE Trans. Inform. Theor. 46 (2) (2000) 388–404.   
[2] I. Akyildiz, X. Wang, W. Wang, Wireless mesh networks: a survey, Comput. Netw. 47 (4) (2005) 445–487.   
[3] S. Yi, Y. Pei, S. Kalyanaraman, On the capacity improvement of ad hoc wireless networks using directional antennas, in: Proc. ACM MobiHoc, 2003.   
[4] S.R. Kulkarni, P. Viswanath, A deterministic approach to throughput scaling in wireless networks, IEEE Trans. Inform. Theor. 50 (6) (2004) 1041–1049.   
[5] B. Liu, Z. Liu, D. Towsley, On the capacity of hybrid wireless networks, in: Proc. IEEE INFOCOM, 2003.   
[6] U.C. Kozat, L. Tassiulas, Throughput capacity of random ad hoc networks with infrastructure support, in: Proc. ACM MobiCom, 2003.   
[7] A. Zemlianov, G. de Veciana, Capacity of ad hoc wireless networks with infrastructure support, IEEE J. Selected Areas Commun. 23 (3) (2005) 657–667.   
[8] J. Gomez, A.T. Campbell, Variable-range transmission power control in wireless ad hoc networks, IEEE Trans. Mobile Comput. 6 (1) (2007) 87–99.   
[9] X. Li, S. Tang, F. Ophir, Multicast capacity for large scale wireless ad hoc networks, in: Proc. ACM Mobicom, 2007.   
[10] M. Franceschetti, O. Dousse, D. Tse, P. Thiran, Closing the gap in the capacity of wireless networks via percolation theory, IEEE Trans. Inform. Theor. 53 (3) (2007) 1009–1018.   
[11] A. Keshavarz-Haddad, V. Ribeiro, R. Riedi, Broadcast capacity in multihop wireless networks, in: Proc. ACM MobiCom, 2006.   
[12] X. Shakkottai, S. Liu, R. Srikant, The multicast capacity of large multihop wireless networks, in: Proc. ACM MobiHoc, 2007.   
[13] A. ÖzgÜr, O. LÉvÊque, D. Tse, Hierarchical cooperation achieves optimal capacity scaling in ad hoc networks, IEEE Trans. Inform. Theor. 53 (10) (2007) 3549–3572.   
[14] Y. Lin, Y. Hsu, Multihop cellular: A new architecture for wireless communications, in: Proc. IEEE INFOCOM, 2000.   
[15] A. Agarwal, P.R. Kumar, Capacity bounds for ad hoc and hybrid wireless networks, ACM SIGCOMM Comput. Commun. Rev. 34 (3) (2004) 71–83.   
[16] B. Liu, P. Thiran, D. Towsley, Capacity of a wireless ad hoc network with infrastructure, in: Proc. ACM Mobihoc, 2007.   
[17] X. Mao, X.-Y. Li, S. Tang, Multicast capacity for hybrid wireless networks, in: Proc. ACM MobiHoc, 2008.   
[18] U. Nguyen, On multicast routing in wireless mesh networks, Comput. Commun. 31 (7) (2008) 1385–1399.   
[19] D. Estrin, R. Govindan, J. Heidemann, S. Kumar, Next century challenges: scalable coordination in sensor networks, in: Proc. ACM MobiCom, 1999.   
[20] I. Akyildiz, W. Su, Y. Sankarasubramaniam, E. Cayirci, Wireless sensor networks: a survey, Comput. Netw. 38 (4) (2002) 393–422.   
[21] Q. Huang, C. Lu, G. Roman, Spatiotemporal multicast in sensor networks, in: Proc. ACM Sensys, 2003.   
[22] J. Sanchez, P. Ruiz, J. Liu, I. Stojmenovic, Bandwidth-efficient geographic multicast routing protocol for wireless sensor networks, IEEE Sensors J. 7 (5) (2007) 627–636.   
[23] R. Zheng, Information dissemination in power-constrained wireless networks, in: Proc. IEEE INFOCOM, 2006.   
[24] S. Li, Y. Liu, X.-Y. Li, Capacity of large scale wireless networks under gaussian channel model, in: Proc. ACM Mobicom, 2008.   
[25] C. Wang, X. Li, C. Jiang, S. Tang, Y. Liu, Scaling laws on multicast capacity of large scale wireless networks, in: Proc. IEEE INFOCOM, 2009.   
[26] C. Wang, S. Tang, X.-Y. Li, C. Jiang, Y. Liu, Multicast throughput of hybrid wireless networks under Gaussian channel model, in: Proc. IEEE ICDCS, 2009.   
[27] A. Keshavarz-Haddad, R. Riedi, Bounds for the capacity of wireless multihop networks imposed by topology and demand, in: Proc. ACM MobiHoc, 2007.   
[28] A. Keshavarz-Haddad, R. Riedi, Multicast capacity of large homogeneous multihop wireless networks, in: Proc. IEEE WiOpt, 2008.

[29] X.-Y. Li, Multicast capacity of wireless ad hoc networks, IEEE/ACM Trans. Netw. 17 (3) (2009) 950–961.   
[30] R. Bhatia, L. Li, Characterizing achievable multicast rates in multihop wireless networks, in: Proc. ACM MobiHoc, 2005.   
[31] P. Chaporkar, A. Bhat, S. Sarkar, An adaptive strategy for maximizing throughput in MAC layer wireless multicast, in: Proc. ACM MobiHoc, 2004.   
[32] A. Chen, D. Lee, G. Chandrasekaran, P. Sinha, HIMAC: High throughput MAC layer multicasting in wireless networks, in: Proc. IEEE MASS, 2007.   
[33] S. Sen, J. Xiong, R. Ghosh, R. Choudhury, Link layer multicasting with smart antennas: No client left behind, in: Proc. IEEE ICNP, 2008.   
[34] H. Won, H. Cai, K. Guo, A. Netravali, I. Rhee, K. Sabnani, Multicast scheduling in cellular data networks, IEEE Trans. Wireless Commun. 8 (9) (2009) 4540–4549.   
[35] J. Xiong, R.R. Choudhury, Peercast: Improving link layer multicast through cooperative relaying, in: Proc. IEEE INFOCOM, 2011.   
[36] R. Meester, R. Roy, Continuum Percolation, Cambridge University Press, 1996.   
[37] R. Zheng, Asymptotic bounds of information dissemination in power-constrained wireless networks, IEEE Trans. Wireless Commun. 7 (1) (2008) 251–259.   
[38] U.C. Kozat, L. Tassiulas, Throughput capacity of random ad hoc networks with infrastructure support, in: Proc. ACM Mobihoc, 2003.   
[39] C. Ulas, L. Tassiulas, Throughput scalability of wireless hybrid networks over a random geometric graph, Wireless Netw. 11 (4) (2005) 397–423.   
[40] M. Raab, A. Steger, ‘‘Balls into bins’’ – a simple and tight analysis, in: Proc. the Second International Workshop on Randomization and Approximation Techniques in Computer Science, 1998.   
[41] M. Mitzenmacher, The Power of Two Choices in Randomized Load Balancing, Ph.D. Thesis, University of California, 1996.   
[42] B. Liu, D. Towsley, A. Swami, Data gathering capacity of large scale multihop wireless networks, in: IEEE MASS, 2008.   
[43] J. Littlewood, On the probability in the tail of a binomial distribution, Adv. Appl. Prob. 1 (1) (1969) 43–72.

![](images/163d56369e85b1fa05d9ed0da011b9640683870a80590acedeb911a781e39cfe.jpg)



Cheng Wang received M.S. degree at Department of Applied Mathematics from Tongji University, Shanghai, China, in 2006. He is currently with Department of Computer Science and Technology at Tongji University, Shanghai, China. His research interests are in wireless networking and distributed computing.

![](images/38989aed027452684662e2e8709a17221defb8839d950e4463d66e4693a52e7c.jpg)



Changjun Jiang received the Ph.D. degree from the Institute of Automation, Chinese Academy of Sciences, Beijing, China, in 1995 and conducted post-doctoral research at the Institute of Computing Technology, Chinese Academy of Sciences, in 1997. Currently he is a Professor with the Department of Computer Science and Engineering, Tongji University, Shanghai. He is also a council member of China Automation Federation and Artificial Intelligence Federation, the Vice Director of Professional Committee of Petri Net of China

Computer Federation, and the Vice Director of Professional Committee of Management Systems of China Automation Federation. He was a Visiting Professor of Institute of Computing Technology, Chinese Academy of Science; a Research Fellow of the City University of Hong Kong, Kowloon, Hong Kong; and an Information Area Specialist of Shanghai Municipal Government. His current areas of research are concurrent theory, Petri net, and formal verification of software, concurrency processing and intelligent transportation systems.

![](images/a1ce82afa19551f3e7f81e33f87ccbf577f178462bafd43123f999345a82c481.jpg)



Xiang-Yang Li received M.S. (2000) and Ph.D. (2001) degree at Department of Computer Science from University of Illinois at Urbana-Champaign. He received his Bachelor degree at Department of Computer Science and Bachelor degree at Department of Business Management from Tsinghua University, P.R. China, both in 1995. He has been with Department of Computer Science at the Illinois Institute of Technology since 2000. Currently he is an Associate Professor of Department of Computer Science, IIT. He also holds visiting professorship or adjunct-professorship at the following universities: TianJin University, WuHan University, NanJing University, Tongji University and Microsoft Research Asia. His research interests span the wireless ad hoc networks, computational geometry, game theory, and cryptography and network security. He served various positions (such as conference chair, local arrangement chair) at numerous international conferences. He is an editor of Ad Hoc & Sensor Wireless Networks: An International Journal. He recently also coorganized a special issue of ACM MONET on non-cooperative computing in wireless networks and a special issue of IEEE Journal of Selected Area in Communications. He is a senior member of IEEE computer society, and a member of ACM.

![](images/33a6440db096c6b67adfbc732fb0b5d12ed1efa6d9364ae3cc36576f881a6743.jpg)



Yunhao Liu received the B.S. degree in automation from Tsinghua University, China, in 1995, and the M.A. degree from the Beijing Foreign Studies University, China, in 1997, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. Currently he is an Associate Professor of Department of Computer Science and Engineering at the Hong Kong University of Science and Technology. He is also an Adjunct Professor of Xi’an Jiaotong University, Jilin University, and Ocean University of China. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. Dr. Liu and his student Li Mo received the Grand Award of Hong Kong ICT Best Innovation and Research Award 2007. He is a senior member of IEEE computer society, and a member of ACM.