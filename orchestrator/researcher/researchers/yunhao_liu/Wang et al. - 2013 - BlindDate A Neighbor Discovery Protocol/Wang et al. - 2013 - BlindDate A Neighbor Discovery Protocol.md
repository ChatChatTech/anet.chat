# BlindDate: A Neighbor Discovery Protocol

Keyu Wang

Department of Computer Science and Engineering

Hong Kong University of Science and Technology

Hong Kong, China

Email: kwangad@cse.ust.hk

Xufei Mao, Yunhao Liu

School of Software, TNLIST

Tsinghua University

Beijing, China

Email: {xufei, yunhao}@greenorbs.com

Abstract—Many wireless applications urgently demand an efficient neighbor discovery protocol to build up a bridge connecting users to service providers or to other users. However, due to intrinsic constraints of wireless devices, e.g., limited energy and error of clock synchronization, there is still absence of effective and efficient neighbor discovery protocols in the literature. In this work, we propose neighbor discovery protocols for the following two problems. We first study Asynchronous Symmetry Neighbor Discovery problem, in which potential neighbor devices with asynchronous time clock but the same duty cycle aim to find each other. We further propose an efficient protocol (using Bouncing strategy) named BlindDate with guaranteed worst-case performance 9 (1 + δ) 2x2 where δ is a small fraction of the length of time slot unit and 1 is the duty cycle. Next, we extend this design to address Asynchronous Asymmetry Neighbor Discovery problem, in which both time clock and the duty cycles of potential neighbors are considered to be heterogeneous. We conduct extensive simulations to examine the feasibility and efficiency of the proposed protocols. Results show that BlindDate protocol outperforms existing approaches in average-case. We conclude that, compared with known protocols, BlindDate achieves a better worstcase discovery latency bound (e.g., 10% performance gain comparing with Searchlight [1]).

Keywords-neighbor discovery; energy efficiency; latency

# I. INTRODUCTION

Recently, social network applications gradually move from the Internet to mobile devices and many mobile applications (e.g., Sony’s Near [2] and Nintendo’s StreetPass [3]) have gained increasing acceptance. One of common properties for this kind of mobile applications is that users can play them together locally without support of a central server as long as their mobile devices are close enough. For instance, a customer in a coffee shop may want to invite other customers who are also interested in the same mobile game to play together without using the Internet. Clearly, asking other customers one-by-one is not a good choice. Hence, one of the challenges in this kind of mobile applications is how to let users find each other efficiently and precisely, which is known as neighbor discovery problem. Let us consider another real application scenario for such kind of problem. In CitySee [4], more than 1000 TelosB sensor nodes have been deployed in the urban area in order to monitor the environment. In purpose of network diagnosis, network administrators sometimes have to carry a handset device to collect packets from deployed sensor

nodes directly. Since all deployed wireless sensor nodes are powered by batteries and the duty-cycle in CitySee is around 4%, which means nodes fall into sleep most of the time, with no doubt, an efficient neighbor discovery is crucial between deployed wireless sensor nodes and the mobile handset. In addition, another work [5] proposed by Liu et. al, points out that a well-designed topology control approach is determined by efficient neighbor discovery strategies to some extent since letting wireless nodes find each other effectively is the precondition of building connections.

Furthermore, a good neighbor discovery strategy can benefit other kinds of applications as well. For example, mobile devices without GPS and devices with GPS can continuously share location information as long as they can discover each other efficiently even when their relative speed is high. Shop owners can push electric coupons to customers immediately when they enter the shop or even pass by the shop. Clearly, an efficient neighbor discovery protocol with low discovery latency can provide better user experience with no doubt.

Based on aforementioned neighbor discovery scenarios, it is not hard to conclude that among all factors which restrict the efficiency of neighbor discovery strategies, energy constraint and low latency requirements are two particularly dominant and contradictive aspects. On the one hand, wireless communication components, like WiFi and 3G, are considered to be the most energy-consuming functions in a mobile device such that most mobile devices only periodically turn their radios on when needed, which may increase the latency of neighbor discovery strategies to some extent. On the other hand, due to the mobility of mobile devices, a high latency usually causes a fail handshaking between users.

Hence, most existing neighbor discovery strategies known in the literature aim at solving either energy efficiency, or latency efficiency, or both problems, which basically fall into two categories: probabilistic-based protocols and deterministic-based protocols. For instance, “Birthday” [6] is a typical probabilistic protocol, which determines whether turning the radio on or shutting it down based on probabilities defined in priori. Probabilistic protocols usually perform well in a static network with large numbers of devices. However, they usually fail to provide guaranteed performance in the worst-case, and have a relatively bad performance when the number of a wireless device’s neighbors is small. On the contrary, deterministic protocols usually have better performance in worst-case scenario. For instance, Quorum-based protocols [7] [8], Disco [9] and U-Connect [10] gradually approach the worst-case energy-latency product with 1.5- approximation ratio [11] of the optimal [10]. Their main ideas are basically to utilize prime numbers to promise the existence of the overlap between active slots. Different from those protocols, Searchlight proposed in work [1] brings us a new view of deterministic protocols, which introduces anchor-probe active slots scheme. Basically, there is a moving probe slot periodically such that one device’s probe slot could ensure an overlap with its neighbors’ active slots in a shorter latency. Through their analysis, Searchlight further approaches the worst-case latency by nearly 50% by adapting a strip strategy while improving the average performance as well.

Enlightened by Searchlight, in this work, we propose a deterministic neighbor discovery protocol named Blind-Date. The main difference between Searchlight and our work is that the latter maintains multiple probe slots with different moving directions in each period such as to increase the chances of the overlaps between two probe slots, i.e., further shorten the discovery latency. Moreover, our simulation results show that BlindDate is more energy efficient and delay efficient. Compared with other known protocols, BlindDate protocol shortens worst-case discovery latency bound and achieves a much better average performance. The major contributions of this study are summarized as follows.

• We propose a general model for designing deterministic asynchronous neighbor discovery strategies, and further analyze its feasibility.   
Based on the presented model, we design the Blind-Date protocol, which further achieves a performance gain by 10% (proved in this work), after Searchlight [1] improved the worst-case latency by almost 50%.   
We simulate all the cases for both proposed protocols and other well known neighbor discovery protocols, and the results show that BlindDate performs well with a 30% ∼ 40% performance gain in average.

The rest of this paper is organized as follows. We discuss some related work in Section II. In Section III, we give the design model of protocols, following which we prove its feasibility through illustrating the strategies of major parameters selections in Section IV. In Section V, we present the details of the BlindDate protocol and show the worst-case latency bound in comparison with other existing neighbor discovery protocols. We introduce the details of simulations and show extensive evaluation results in Section VI. Finally, we conclude our work in Section VII.

# II. RELATED WORK

Neighbor discovery problem is relatively easy to solve when the nodes are deployed in a static and dense network. Wireless devices can communicate by long preamble packets [12], synchronizing their clock [13] or repeatedly sending packets until receiving ACK packet [14]. BMAC [12] and SMAC [15] are proposed for neighbor discovery protocols employing LPL. Many other discovery protocols also use duty cycle schemes, i.e., the radio of mobile devices is turned off for most of the time (i.e., falling into sleep) and periodically reopened in a short time period for neighbor discovery (i.e., going to active state). The key point is to let potential neighbors (within transmission range of each other) in active state concurrently. Generally speaking, current neighbor discovery protocol basically fall into two categories, probabilistic protocols and deterministic protocols, with the objectives to improve different aspects of performance including average latency and worst-case latency bound, etc.

McGlynn and Borbash propose “Birthday protocols” [6], which is a well-known probabilistic approach for asynchronous neighbor discovery in static wireless networks. Basically, for every single node, Birthday sets different probabilities for sending packets, receiving packets and going to sleep. “Birthday protocols” performs well in static wireless networks with multiple neighbors for averagecase. However, it cannot provide a worst-case bound, which is actually the common drawback for all probabilistic approaches.

In contrary, deterministic protocols like Quorum-based protocols [7] [8], can guarantee the worst-case bound. Quorum-based protocols consider time as a 2-dimensional m ∗ m interval array. The node arbitrarily chooses one row and one column of intervals as active slots, which guarantees that any pair of two nodes have at least two active slots overlapped. Although Quorum-based protocols can promise the worst-case latency, they are not suitable for asymmetric case since parameter m needs to be a global parameter. Zheng et al. [16] use different settings to make optimal block designs for symmetric neighbor discovery with the help of the Multiplier Theorem [17]. However, their design did not consider the asymmetric case. One interesting work [18] studied clapping and broadcasting synchronization in wireless sensor networks, which concentrated on how to synchronize nodes using broadcasting property of wireless communications, i.e., touched the neighbor discovery problem from another point of view.

Being another type of deterministic protocols, Primebased protocols aim to solve neighbor discovery problem from the perspective of providing a worst-case bound for discovery latency for both symmetric and asymmetric cases. For instance, in Disco [9], a node selects a pair of unequal prime numbers and comes into active state when the sequence number of a time slot is divisible by any of selected prime numbers. According to the Chinese Remainder Theorem [19], the worst-case discovery latency is bounded by min $\{ ( p _ { 1 } \cdot p _ { 3 } ) , ( p _ { 1 } \cdot p _ { 4 } ) , ( p _ { 2 } \cdot p _ { 3 } ) , ( p _ { 2 } \cdot p _ { 4 } ) \}$ , where one node selects prime numbers $p _ { 1 }$ and $p _ { 2 } ,$ , and the other node selects prime numbers $p _ { 3 }$ and $p _ { 4 } .$ . Kandhalu et al. propose U-Connect [10], which is also based on prime number based theorems. Different from Disco, in U-Connect, the node selects only one prime number p. Except for those multiplies number of slots, there are $\textstyle { \frac { p + 1 } { 2 } }$ more slots for active state such that U-Connect performs much better than Disco in terms of energy-latency product metric. For these existing neighbor discovery protocols, an on-demand generic discovery accelerating middleware called Acc [20] is proposed Zhang et al. It supports both direct and indirect neighbor discoveries.

Recently, Searchlight [21] is proposed for neighbor discovery problems, in which they further define two different types of slots for active slots, anchor slots and probe slots respectively. By keeping a probe slot changing its position (in the temporal dimension) periodically, Searchlight guarantees that a probe slot has an overlap with a potential neighbor’s anchor slot within some time bound, thus finishes a neighbor discovery procedure successfully. Later, an improved version of Searchlight [1] utilizes a strip strategy greatly reducing the worst-case bound by nearly 50% and it also performes better than Prime-based protocols do for average-case. Motivated by Searchlight, in this work, we design a new deterministic protocol (named BlindDate) aiming at further shortening the worst-case latency by increasing the probability of overlaps. Through our analysis, we observe that there is little chance for a overlap between two probe slots when they are moving in the same direction. Thus, we consider adding more probe slots moving in different directions from the temporal points of view in order to increase the probability for an overlap between two probe slots. Meanwhile, without increasing the duty cycle, the length of each period will be prolonged for multiple probe slots. We theoretically analyze the discovery latency and propose a better neighbor discovery solution.

# III. DESIGN OVERVIEW

# A. Neighbor Discovery

Our work is based on a general model in the literature. First, we assume that time has been chopped into welldefined slots with an equal length, in each of which a wireless node (device) can choose either turning on its radio (called “active” state) for data exchanging or shutting down the radio (named “sleep” state) in order to save energy. For any time slot τ , the state of a wireless device A can be indicated by the value of the binary function $\Psi ( A , \tau )$ where $\Psi ( A , \tau ) = 1$ means that A is active in time slot τ , otherwise A goes to sleep. Second, due to the facts that practical limitations on synchronization algorithms among the mobile devices and hardware clocks restrict the efficiency of time synchronization, our work concentrates on slotted asynchronous neighbor discovery protocols.

Definition 1 (Blind Date): For any two potential neighbor devices A and B, the sufficient condition for them to discover each other iff one device which is in the active state hears at least one beacon message (or say probe

Table I SUMMARY OF MAJOR SYMBOLS 

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td>t</td><td>Length of a period</td></tr><tr><td>T</td><td>Hyper-period</td></tr><tr><td>m</td><td>Number of blocks in a period</td></tr><tr><td>s</td><td>Number of time slots in a block</td></tr><tr><td>L</td><td>Worst-case discovery latency</td></tr><tr><td>S</td><td>Static active time slot</td></tr><tr><td>D</td><td>Dynamic active time slot</td></tr><tr><td>P(x)</td><td>Position of the time slot x</td></tr></table>

message) from the other device. In other words, when the time slots of two devices A and B are well aligned, we say that they successfully find each other when $\Psi ( A , t ) =$ $\Psi ( B , t ) = 1$ for some time slot t. If the time slots are not aligned well, two potential neighbors successfully find each other when they have active slot overlaps. We call a successfully neighbor discovery progress between two devices as a successful Blind Date.

Basically, two problems are solved in this work.

1) Asynchronous Symmetric Neighbor Discovery Problem, in which all wireless devices are assigned with the same discovery schedule regardless of asynchronous time clocks different starting time while keeping both discovery latency and energy consumption as optimization objectives.

2) Asynchronous Asymmetric Neighbor Discovery Problem, in which all wireless devices can use individual discovery schedules, i.e., different duty cycles and asynchronous time clocks, etc.

# B. Model

We summarize main parameters used in this work in Table I, which helps explain and analyze our model and protocol. Next, we introduce the protocol model, before which we use the case shown in Fig. 1 as an example to illustrate our main idea.

Let t denote one schedule period of a wireless device, we further divided t into m blocks, each of which consists of s time slots, i.e., $t = m \cdot s .$ . In the example shown in Fig. 1, we have m = 4 and s = 3 such that each period contains $m \cdot s = 1 2$ time slots, whose sequence numbers are defined from 0 to 11 with step of 1. Here, we use bold boxes to represent the blocks and use dotted lines to split the block into time slots (see Fig. 1(a)).

Next, we design two types of active slots. The first type is called Static active slot (abbreviated to Static slot), which is denoted by letter S in uppercase. In addition, we fix the position of the Static slot such that it always allocates at the last time slot (position 11 in the example) of the period t. The second type is called Dynamic active slot (abbreviated to Dynamic slot), which is denoted by letter D in uppercase. Different from the Static slot, the Dynamic slot has different positions for different periods, i.e., continues to move from one side to the other inside one block.

Moving Patterns of Dynamic slots For a Dynamic slot moving from left to right (e.g., the Dynamic slot of the first block in the example), it goes through all time slots inside the block (with step of 1) with the increment of time period. For instance, it first occupies the time slot 0 in the first period (see Fig. 1(a)), and in the second period, the Dynamic slot moves to occupy the right adjacent time slot 1 (see Fig. 1(b)). It continues this moving until reaching the right-most time slot of the block (shown in Fig. 1(c)). Then it restarts from the left-most time slot and repeats this pattern (please refer to Fig. 1(d)). Hence, if we use $P ( D ^ { i } )$ to denote the position of the Dynamic slot for the i-th period, the Dynamic slot locating in the j-th block can be computed as

$$
P (D ^ {i + 1}) = ((P (D ^ {i}) + 1) \mod s) + (j - 1) \cdot s \tag {1}
$$

Similarly, for the Dynamic slot which has the opposite moving direction (the third block’s Dynamic slot in the example), we have

$$
P (D ^ {i + 1}) = ((P (D ^ {i}) - 1) \mod s) + (j - 1) \cdot s. \tag {2}
$$

In addition, we restrict that every block could possess at most one Dynamic slot while Dynamic slots in different blocks can use opposite moving directions, i.e., either from left to right or from right to left. We further call the block owning a Dynamic slot as a Dynamic block.

Protocol Model First, we choose k block(s) from total m blocks as Dynamic blocks to insert a Dynamic slot. In the example shown in Fig. 1, k equals to 2 as we insert a Dynamic slot into the first and the third block respectively. Next, combining with Static slot, for each time period t a wireless device has k + 1 active slots totally including one Static slot and k Dynamic slot(s). Hence, for any two devices A and B, as long as one of the following cases happens, Dynamic-Static overlap, Dynamic-Dynamic overlap and Static-Static overlap, we consider that A and B could successfully find each other.

From the Equation 1 and 2, we know that the schedule repeats every s periods following the pattern we designed. In this example, we have that s equals to 3 such that a wireless device in the status shown in Fig. 1(d) goes into the status shown in Fig. 1(a). We call this period as the hyper-period T, which equals to the product of period t and slots number s of each block, i.e., $T = t \cdot s$ .

# IV. MAJOR PARAMETER SELECTION

We first solve the symmetry case, i.e., all nodes have the same length of period time t. Later we will show how to extend this solution to the asymmetric case. Notice, the following analysis and proofs are based on the symmetry case.

# A. Feasibility of BlindDate protocol

Remembering that the schedule patterns utilizing the proposed BlindDate protocol for a wireless device repeats

![](images/cfbd1a03000afae354e7ede25335db5182de0a83ea2e6bb132272b9b1e555908.jpg)  
(a) The First Period

![](images/0d79041686830a4b7aee69492c428d0b2a2a8b45616941cd0722b8bf621b413b.jpg)  
(b) The Second Period

![](images/6626a600fc004fb960e1e0d7939d2d1f886f43fcd6b4a023a3efa770f1c79533.jpg)  
(c) The Third Period

![](images/8d2b0c9fa70305e44f6b7c702e7fba2a189e551646c8b1c7d4cc896df308ed86.jpg)  
(d) The Forth Period (Repeat)   
Figure 1. Example of Model with m = 4, k = 2 and s = 3. D (resp. S) denotes the Dynamic slot (resp. Static slot).

for every hyper-period T such that the necessary condition for any two devices A and B (having the same hyperperiod T ) based on BlindDate protocol to find each other is that their active states have some overlap in T . Otherwise, they can hardly find each other. Hence, the upper bound of the worst-case discovery latency (assuming L) of BlindDate should not exceed $T = s \cdot t = m s ^ { 2 }$ in order to work feasibly, i.e.,

$$
L = m s ^ {2}
$$

Intuitively, it seems that utilizing more Dynamic blocks for a known m could reduce the discovery latency to some extent. However, we cannot neglect the fact that this increases the energy consumption at the same time since there are more active time slots in each period. As a result, in order to have the same duty cycle, every block needs to contain more time slots (a larger s), which may lead to the increment of discovery latency. Thus, for the same duty cycle and a known m we express the worst-case discovery latency as functions of x, w $\begin{array} { r } { \frac { k + 1 } { m \cdot s } \stackrel { \star } { = } \frac { 1 } { x } } \end{array}$ the duty cycle of the

$$
L = m \cdot s ^ {2} = \frac {(k + 1) ^ {2}}{m} \cdot x ^ {2} \tag {3}
$$

From the Equation 3, it is not hard to conclude that for the same duty cycle and a known m, utilizing more Dynamic blocks increases the worst-case discovery latency in fact.

# B. Selection of m and k

Due to the Equation 3, we know that the discovery latency L decreases along with the decreasing of k for the known m, next, we discuss how to make sure the relationship between k and m such as to guarantee the success of neighbor discovery. We analyze this case by case.

1) Case $k \ = \ m { : }$ When $k \ = \ m ,$ , i.e., every block contains a Dynamic slot so that for any two devices, the Static slot of one device must have overlap with one

![](images/c91923e49bdf04abdc3043401d90992681ec11a4a405c4e0ca598d2fbe332049.jpg)



Figure 2. Select First k Blocks

Dynamic block of the other device no matter what offset difference they have. Clearly, two devices can find each other within s periods with hundred percent guarantee.

2) Case $\lfloor { \frac { m } { 2 } } \rfloor < k < m :$ For the case $\lfloor { \frac { m } { 2 } } \rfloor < k < m$ , we design an easy selection strategy ensuring the success of neighbor discovery (see Fig. 2 for illustration). Basically, for two devices A and B, we select the first k blocks as their Dynamic blocks. Obviously, if the Static slot of node B locates in the first k blocks of node $A ,$ as the same reason for the first case, the Dynamic slot in that block definitely has an overlap time with $B ^ { \prime } { \bf s }$ Static slot within s periods; Otherwise, the Static slot of node B locates outside of the first k blocks, which means $P ( S _ { 1 } ^ { \prime } ) - P ( S _ { 1 } ) > s \cdot k .$ . Since $P ( S _ { i } )$ denotes the position of $S _ { i }$ and $P ( S _ { 2 } ) - P ( S _ { 1 } ) = t = m \cdot s ,$ , we have

$$
\begin{array}{l} P (S _ {2}) - P (S _ {1} ^ {\prime}) = m \cdot s - (P (S _ {1} ^ {\prime}) - P (S _ {1})) \\ <   (m - k) \cdot s \\ \end{array}
$$

As we know that $m - k < k$ due to $k > \lfloor \frac { m } { 2 } \rfloor$ , which indicates that $A \ ' s$ Static slot locates in the first k blocks of B. Hence, they also can definitely discover each other within s periods.

3) Case $\begin{array} { l l l } { { k } } & { { = } } & { { \lfloor { \frac { m } { 2 } } \rfloor . } } \end{array}$ : For simplicity of analysis, we consider m into two cases, i.e., m is an even number or an odd number, i.e., we analyze cases $m = 2 p$ or $2 p + 1$ separately. Substituting m with 2p and 2p+1 respectively, we have

$$
L = \frac {(k + 1) ^ {2}}{m} \cdot x ^ {2} = \frac {(p + 1) ^ {2}}{2 p} \cdot x ^ {2} \tag {4}
$$

and

$$
L = \frac {(k + 1) ^ {2}}{m} \cdot x ^ {2} = \frac {(p + 1) ^ {2}}{2 p + 1} \cdot x ^ {2} \tag {5}
$$

Since both equations imply that L goes smaller when p gets smaller, we pay attention to finding a smaller value of p.

When m is an even number: We select the first $k = p$ blocks as Dynamic blocks. As the same analysis in case $k > \lfloor { \frac { m } { 2 } } \rfloor$ , we have

$$
\min \{P (S _ {1} ^ {\prime}) - P (S _ {1}), P (S _ {2}) - P (S _ {1} ^ {\prime}) \} \leq \frac {m \cdot s}{2}
$$

which points out that at least one node’s Static slot locates in the first half blocks $( k = p$ blocks) of its neighbor. Within s periods, the Dynamic-Static overlap happens. Referring to the Equation 4, when m is an even number, the worst-case discovery latency L achieves the minimal value when we assign $p = 1$ (see Fig. 3 for illustration). Actually in this case, the worst-case discovery latency L equals to $2 x ^ { 2 }$ , which is optimal.

![](images/b3950d9ae9fade634eab52e7095cd32137e0eae0f8562b65bc967e0af8b81bad.jpg)



Figure 3. Optimal Even Case

When m is an odd number: Intuitively, the smallest value for Equation 5 is when $p = 1$ , which means that select one Dynamic block out of total 3 blocks. Unluckily, we cannot find a feasible solution which can guarantee the success of Blind Date when $p = 1$ . Rationally, we choose the value of p as 2.

Fortunately, after carefully arranging the position of Dynamic slots, the proposed BlindDate protocol can guarantee the success of neighbor discovery with latency bound by choosing 2 blocks out of 5 blocks $( i . e . , k = 2$ and $m = 5 )$ . One thing deserves mentioning that the worstcase discovery latency of this specific BlindDate protocol $( k = 2$ and $m = 5 )$ is better than all cases when m is even.

In the following Section V, we provide design details of BlindDate protocol along with proved guaranteed performance.

# V. BLINDDATE PROTOCOL

BlindDate protocol (abbreviated to BD protocol) allocates Dynamic slots in the first and the forth blocks respectively when we put Dynamic slots inside of 2 out of totally 5 blocks. Specially, the first block’s Dynamic slot moves from left to right while the Dynamic slot in the forth block moves in an opposite direction. Through the analysis in last section, we know that BD protocol guarantees the existence of active slots overlap for all offset cases. Next, we first prove the feasibility of BD protocol and later we will show that after adopting the bouncing Dynamic slot, BD protocol’s performance can be further improved.

# A. Feasibility

To illustrate the feasibility of BD protocol, we have to prove that two potential neighbor devices can find each other no matter what scheduling offset they have. Since the schedule pattern repeats every hyper-period, it is sufficient to consider the scheduling offsets within the hyper-period. Next, we use a time slot offset with a period offset to represent the scheduling offset. Here, the time slot offset indicates the offset between the start points of two potential neighbor nodes’ Static slots’. Obviously, in symmetric case, the time slot offset remains the same for all periods. On the other hand, the period offset indicates the period difference between two potential neighbor devices. For instance, when one device A starts the protocol, its potential neighbor device B may have started the protocol for d periods already (d is a constant). Thus, the device A has its Dynamic slot in the first time slot of the block while the other device B has its Dynamic slot in the $d + 1$ time slot (assuming the time slot number of each block is bigger than d + 1). The period offset for this instance is d.

![](images/51f9cff4935bf89e98bb8797c47eb5ef7992127c1f6800788c5dcf71e5407900.jpg)



Figure 4. Feasibility Analysis

As Fig. 4 shows, we split the period t of device A into 6 regions for the convenience of proof. When we claim that a slot locates in region X we mean that the start point of this slot, especially the left edge of the time slot, locates in region X. Here, our partition is based on different time slot offsets. In the following proof, we show that BD protocol is feasible for all period offsets in these 6 regions one by one. In addition, since we have no need to take slot alignment as a condition of the proof, our proof applies to both slot alignment and non-alignment cases.

First of all, in Fig. 4, if the device B’s Static slot locates in region $R ^ { 1 }$ or $R ^ { 4 }$ , there exists a Dynamic-Static overlap because the device A’s Dynamic slot cruises all slots in these regions during s periods. Second, if the device B’s Static slot locates in region $R ^ { 2 }$ or $R ^ { 5 }$ , the device A’s Static slot locates in the forth or the first block of device B, and we clearly have a Dynamic-Static overlap within s periods. Next, when the device $\mathbf { B } ^ { \prime } \mathbf { s }$ Static slot locates in region $R ^ { 6 }$ , the Static slots of A and B obviously have a Static-Static overlap since this region has only one time slot. Then we handle the most complex case when the device $B ^ { * } { \mathrm { s } }$ Static slot locates in region $R ^ { 3 }$ . Fortunately, the opposite moving directions of Dynamic slots benefit us here. For ease of presentation, we first mark several positions, $A _ { 0 } ,$ $A _ { 1 } , A _ { 3 } , B _ { 1 }$ and $B _ { 4 }$ (shown in Fig. 4) where the letter in upper case indicates which device it belongs to and the subscript represents the block it locates at the beginning of. With no doubt, the Dynamic-Dynamic overlap must happen inside those block overlap regions if the overlap exists, as the Dynamic slots go through these regions in the opposite directions. If both of two devices’ Dynamic slots

![](images/fa7ca7225eadf0f852737904b609f3d6e4a3219fc65bc3ca682c030f992a52ef.jpg)



Figure 5. Dynamic Slots Jump Over

are in these regions at some time, the Dynamic-Dynamic overlap certainly happened already or will happen later. Thus, the remaining work is to prove that there exists a moment at which both devices’ Dynamic slots are in the overlap region.

Since $( A _ { 1 } - B _ { 4 } ) + ( B _ { 1 } - A _ { 3 } ) = s ,$ , we have max $\{ A _ { 1 }$ − $\begin{array} { r } { B _ { 4 } , \ B _ { 1 } - A _ { 3 } \} \geq \frac { s } { 2 } } \end{array}$ . Without loss of generality, we assume that

$$
A _ {1} - B _ {4} \geq \frac {s}{2} \tag {6}
$$

From Equation 6, we conclude that the device A’s Dynamic slot spends no less than  s 	 periods in the overlap region. Before the device A’s Dynamic slot leaves the overlap region, the device $B ^ { * } { \mathrm { s } }$ Dynamic slot surely has entered into the overlap region or they are aligned at the different sides of position $A _ { 1 } .$ For the purpose of ensuring that those Dynamic slots have an overlap, we prolong the length of Dynamic slot to (1 + δ) and shorten the adjacent time slot to (1−δ) so that we keep the period t unchanged. This modification also solves the problem of alignment case (see Fig. 5 for illustration), in which two Dynamic slots may jump over each other without an overlap. Later, we will move this prolonged length to other position and obtain an even better performance. From the above proof, we conclude that our protocol guarantees the performance for all cases.

# B. Bouncing Dynamic Slot

When the slots are non-alignment, every active slot of a wireless device probably covers two time slots of its potential neighbor’s, resulting in that the Dynamic slot could skip one time slot for each movement indeed. In BD protocol, we use a bouncing Dynamic slot, which keeps moving with step of 2. In other words, if P represents the position of the Dynamic slot in the i-th period, the Dynamic slot locates in the j-th block and each block contains s slots, then

![](images/84c87ea99d01094f098812ef08ca75c1176af01c34eae0d6bb58fd9d89caab1f.jpg)



(a) Dynamic Slots Jump Over

![](images/95c3e738f3db7fbe144bf76e35bbf02f4a58929aa01cd43ff4f18d3a709c611c.jpg)



(b) Add 2 More Beacons   
Figure 6. Bouncing Dynamic Slot Modification

$$
P (D ^ {i + 1}) = ((P (D ^ {i}) + 2) \mod s) + (j - 1) \cdot s
$$

Similarly, for the opposite moving direction Dynamic slot, we have

$$
P (D ^ {i + 1}) = ((P (D ^ {i}) - 2) \mod s) + (j - 1) \cdot s
$$

It is not hard to see that if this improvement works, it reduces the hyper-period T by nearly 50%, which also decreases the worst-case discovery latency by nealy 50%. The new hyper-period T is as follows.

$$
T = \left\lceil \frac {s}{2} \right\rceil \cdot t = \left\lceil \frac {s}{2} \right\rceil \cdot 5 s
$$

However, the bouncing Dynamic slot brings us a big challenge at the same time, since the bouncing Dynamic slots of opposite directions often jump over each other without overlaps in some case (refer to Fig. 6(a)). To overcome this issue, we shift the prolonged length of time to the beginning of the previous slot and the end of next slot of current Dynamic slot (see Fig. 6(b)). From the point view of system implementation, typically, each prolonged time length should cover the time of sending a single beacon message. Fortunately, these messages take only a little time compared with the length of a time slot.

# C. Worst-case Latency Comparison

In every period t, BD protocol has three active time slots, one Static slot and two Dynamic slots. We use $( 1 + \delta )$ to represent the total length of a Dynamic slot.

Table II WORST-CASE LATENCY FOR DETERMINISTIC PROTOCOLS 

<table><tr><td>Protocol</td><td>Parameters</td><td>Duty Cycle</td><td>Worst-case Bound</td></tr><tr><td>Disco [9]</td><td> $p_1, p_2$ </td><td> $\frac{p_1 + p_2}{p_1 \cdot p_2}$ </td><td> $p_1 \cdot p_2$ </td></tr><tr><td>U-Connect [10]</td><td> $p$ </td><td> $\frac{3p+1}{2p^2}$ </td><td> $p^2$ </td></tr><tr><td>Searchlight [1]</td><td> $t$ </td><td> $\frac{2 \cdot (1+\delta)}{t}$ </td><td> $t \cdot \lceil \frac{\lfloor \frac{t}{2} \rfloor}{2} \rceil$ </td></tr><tr><td>BlindDate</td><td> $s$ </td><td> $\frac{3(1+\delta)}{5s}$ </td><td> $5s \cdot \lceil \frac{s}{2} \rceil$ </td></tr></table>

Table III WORST-CASE LATENCY BOUND UNDER THE SAME DUTY CYCLE 

<table><tr><td>Protocol</td><td>Worst-case Bound</td><td>Expressed by x</td></tr><tr><td>Disco</td><td> $p^{2}$ </td><td> $4x^{2}$ </td></tr><tr><td>U-Connect</td><td> $\frac{3p+1}{2p^{2}}$ </td><td> $\frac{9x^{2}}{4}$ </td></tr><tr><td>Searchlight</td><td> $t \cdot \lceil \frac{\lfloor\frac{t}{2}\rfloor}{2} \rceil$ </td><td> $(1+\delta)^{2}x^{2}$ </td></tr><tr><td>BlindDate</td><td> $5s \cdot \lceil \frac{s}{2} \rceil$ </td><td> $\frac{9}{10}(1+\delta)^{2}x^{2}$ </td></tr></table>

Hence, the duty cycle for our protocol approximatively equals to 3(1 + δ)/5s. Next, we compare the worst-case discovery latency of our protocol with those of other existing deterministic protocols from theoretical point of view. Table II summarizes the worst-case latency bound for deterministic protocols.

All protocols use the same duty cycle as $\textstyle { \frac { 1 } { x } }$ with respect to fairness. For ease of comparison, we make some assumptions that $p _ { 1 } = p _ { 2 } = p$ for Disco, such that

$$
{\frac {1}{x}} = {\frac {p _ {1} + p _ {2}}{p _ {1} \cdot p _ {2}}} \approx {\frac {2}{p}}
$$

Clearly, when we express the parameter as a function of x, we have $p = 2 x$ . Hence, for U-Connect, we have the following result.

$$
\frac {1}{x} = \frac {3 p + 1}{2 p ^ {2}} \Rightarrow p \approx \frac {3 x}{2}
$$

And for Searchlight, the following equation is right.

$$
{\frac {1}{x}} = {\frac {2 \cdot (1 + \delta)}{t}} \Rightarrow t = 2 x (1 + \delta)
$$

Finally, for our BD protocol, we have

$$
\frac {1}{x} = \frac {3 (1 + \delta)}{5 s} \Rightarrow s = \frac {3}{5} x (1 + \delta).
$$

Then, the worst-case discovery latency can be expressed by functions of x (see Table III). Clearly, after Searchlight improved the worst-case latency by almost 50%, we further achieve a performance gain by 10%. One thing needs to be mentioned that BD protocol has the smallest worst-case bound.

# D. Asymmetric Case

In a real application scenario, a mobile device may dynamically adjust it’s duty cycle for a while, e.g., depending on energy conditions, such that two potential neighbor devices may use different duty cycles. Clearly, in this asymmetric case, offset between the period’s starting time of two devices changes along with the time. With no doubt, this brings challenges to guarantee the performance of BD protocol, and makes it harder to provide a worst-case latency bound. Next, we propose an approach to overcome this issue so that BD protocol can be extended to support the asymmetric case as well.

![](images/efe80e00bd93e3d455484409d0f08b4721afdff94c60f559740f55baeff9b7fe.jpg)



(a) CDF for Duty Cycle 1%

![](images/e2c8828a8866107fb96e680b3ae2050f4d7bbc2b41e98aa8d236f8655223ca2b.jpg)



(b) CDF for Duty Cycle 5%

![](images/1d55eeac5a3cdcb176453905c1eae9cd28cf22a1be51989ffc174f698da09730.jpg)



(c) CDF for Duty Cycle 10%

![](images/9c8bde4362202c4a13e6b8788f6e37696ed98f7183b913b7f24035cdf98d0f01.jpg)  
(d) Average performance   
Figure 7. Discovery Latency for Symmetric Case.

For a group of devices, we let the block of the device with highest duty cycle contain s time slots, and the blocks of other devices contain $s \cdot 5 ^ { t }$ time slots, where t is a positive integer. Hence, the offset between devices keeps unchanged as the larger period is a multiple of the smaller one. This promises the success of our BD protocol. Here, we provide a loose worst-case bound.

Assuming that the blocks of the device A contain $s _ { A }$ time slots and the blocks of the device B contain $s _ { B }$ time slots where $s _ { A } ~ = ~ s _ { B } \cdot 5 ^ { t }$ . Within $s _ { B } \cdot 5$ periods, A’s Dynamic slot will cover a whole period of B as the offset is unchanged. During this time, A’s Dynamic slot and B’s Static slot definitely have an overlap. So, we have,

$$
L = s _ {B} \cdot 5 \cdot t _ {A}
$$

Combining with the bouncing Dynamic slot, the worst case discovery latency is shortened by nearly 50%. Then,

$$
L = \left\lceil \frac {s _ {B} \cdot 5}{2} \right\rceil \cdot t _ {A} \tag {7}
$$

One thing deserves mentioning that other protocols using our design model can also adopt the same approach in order to solve asymmetric case by assigning the time slot number of blocks as $s _ { b a s e } \cdot m ^ { t }$ where t is a positive integer. The analysis is similar to that of BD protocol.

Since we only give a loose worst-case bound of BD protocol for asymmetric case, we believe that the real performance of BD protocol is much better than this bound when the possibility of Dynamic-Dynamic overlap is considered. Indeed, the simulation results in Section VI also validate our conjecture.

# VI. PERFORMANCE EVALUATION

We implement BlindDate protocol using Java simulator. Since clock synchronization is not suitable on mobile devices due to the energy-constraint, potential neighbor devices may start at different time. Indeed, even for the symmetric case, the offset between nodes’ start points exists. We consider this offset having a uniform distribution in real world so that we simulate each unique offset for equal times. The evaluation metric (discovery latency) represents the time passed from the potential neighbors entering the transmission range to the first discovery event (as we defined in Section III). To simulate the scenario where a node A enters into the transmission range of the other node B, we involve a random number representing the time that the later starting node has spent before entering the transmission range of the other node. In order to improve the accuracy, we chop a time slot into 10 mini time slots equally. In addition, we simulate both the alignment case and the non-alignment case at the same time. Since different platforms (protocols) may have different width of a time slot, for all results we show, we use the number of time slots collapsing as the measurement index, rather than real running time.

![](images/1eb4c9d20d19070b1e7f16169d4ea3781781f289d968aede7b6ca3e1d912bbfa.jpg)



(a) CDF for Duty Cycle 1%, 5%

![](images/2f1e0e34f8c85a38ae70a706a1360b00f1b7eb410dd6edcc5e682a9fded22fbe.jpg)



(b) CDF for Duty Cycle 2%, 10%   
Figure 8. Discovery Latency for Asymmetry

To compare all deterministic protocols fairly, we simulate all protocols under the same duty cycle such that the discovery latency also indicates the total energy consumption. One thing needs to be mentioned is that, for Searchlight, we implement the version with Strip strategy, which achieves the best performance among all Searchlight families. All protocols we compared repeat their schedules every hyper-period T, which may be different due to the fact that they have the same duty cycle. Hence, the simulation offset is in the range of [0, T − 1].

# A. Symmetric Case

For the symmetric case, we simulate all protocols for three different duty cycles, 1%, 5% and 10% respectively. The results are shown in Fig. 7 and the parameters used for each protocol are also shown on the right-bottom of the CDF graphs. Clearly, for all three different duty cycle cases, BD protocol achieves the best performance among all protocols, and the worst-case discovery latency of BD protocol is around 10% smaller compared with Searchlight.

In addition, the average performance of BD protocol is 30% ∼ 40% better than that of Searchlight. See Fig. 7(d) for details.

# B. Asymmetric Case

For asymmetric case, the worst-case performance of BD protocol is smaller than the theoretically results as shown in Fig. 8. Especially, BD protocol shows a much better average-case performance in Fig. 9: 30% ∼ 40% performance gain.

Notice that in Fig. 8, the lines indicating the performance of BD protocol and Searchlight cross with each other when the discovery ratio is over 95%. This is due to the fact that based on the same duty cycle, the length of period of Searchlight is smaller than that of BD protocol so the upper bound of the worst case of Searchlight is smaller than that of BD protocol. Luckily, for most of situations, BD protocol discovers neighbor faster than all other protocols.

# C. Beacon Message Loss

Since in the real wireless transmission scenario, packet loss due to unstable link quality is hard to avoid, we test the performance of BD protocol considering transmission failures. We test both BD protocol and Searchlight for two nodes discovery case considering different packet loss ratios such as 0%, 50% and 70%. The results in Fig. 10 show that the lossy link does not affect the performance of BD protocol much. The two nodes using BD protocol quickly discover each other for over 80% cases. Even for the situation that the packet loss rate is 70%, BD protocol can still achieve over 80% ratios of discovery within around 300 time slots. Compared with Searchlight, BD protocol achieves a better performance for the averagecase.

# VII. CONCLUSION

In this work, we focus on designing an asynchronous neighbor discovery protocol, which guarantees a better worst-case latency bound for symmetric case and has better performance for average-case. We first introduce a design model addressing neighbor discovery problems, based on which we propose BlindDate protocol. BlindDate shortens the worst-case latency bound by exploiting Static and Dynamic slots with a bouncing strategy. Analysis shows that BlindDate achieves a performance gain by 10% after Searchlight improved the worst-case bound by almost 50%. We perform extensive and comprehensive simulations. The results show that BlindDate reduces the discovery latency by around 30% in average.

# ACKNOWLEDGEMENT

This work is supported by NSFC 61272426, China Postdoctoral Science Foundation funded project under grant No. 2012M510029.

![](images/a2b8e483bf1b1c298bdb9f8773b832e04a0a3823e3c1827a862a94eb7041e785.jpg)



Figure 9. Average Performance for Asymmetry   
![](images/bf33ace67d9a692d83133c7a6d6db63f936de0643c0abc7f008717173f056b27.jpg)



Figure 10. Lossy Link: Duty Cycle 5%

# REFERENCES

[1] M. Bakht, M. Trower, and R. H. Kravets, “Searchlight: won’t you be my neighbor?” in Proceedings of ACM International Conference on Mobile Computing and Networking (ACM MobiCom), 2012.   
[2] “Sony ps vita - near,” http://us.playstation.com/psvita/apps/ psvita-app-near.html.   
[3] “Nintendo 3ds - streetpass,” http://www.nintendo.com/3ds/ features.   
[4] X. Mao, X. Miao, Y. He, X. LI, and Y. Liu, “Citysee: Urban co2 monitoring with sensors,” in Proceedings of IEEE International Conference on Computer Communications (IEEE INFOCOM), 2012.   
[5] Y. Liu, Q. Zhang, and L. M. Ni, “Opportunity-based topology control in wireless sensor networks,” IEEE Transactions on Parallel and Distributed Systems, vol. 21, no. 3, pp. 405–416, 2010.   
[6] M. McGlynn and S. Borbash, “Birthday protocols for low energy deployment and flexible neighbor discovery in ad hoc wireless networks,” in Proceedings of ACM International Symposium on Mobile Ad Hoc Networking and Computing (ACM MobiHoc), 2001.   
[7] S. Lai, “Heterogenous quorum-based wakeup scheduling for duty-cycled wireless sensor networks,” Ph.D. dissertation, Virginia Polytechnic Institute and State University, 2009.

[8] Y. Tseng, C. Hsu, and T. Hsieh, “Power-saving protocols for ieee 802.11-based multi-hop ad hoc networks,” Elsevier Computer Networks, vol. 43, no. 3, pp. 317–337, 2003.   
[9] P. Dutta and D. Culler, “Practical asynchronous neighbor discovery and rendezvous for mobile sensing applications,” in Proceedings of ACM Conference on Embedded Networked Sensor Systems (ACM SenSys), 2008.   
[10] A. Kandhalu, K. Lakshmanan, and R. Rajkumar, “Uconnect: a low-latency energy-efficient asynchronous neighbor discovery protocol,” in Proceedings of ACM International Conference on Information Processing in Sensor Networks (ACM IPSN), 2010.   
[11] T. Cormen, Introduction to algorithms. The MIT press, 2001.   
[12] J. Polastre, J. Hill, and D. Culler, “Versatile low power media access for wireless sensor networks,” in Proceedings of ACM Conference on Embedded Networked Sensor Systems (ACM SenSys), 2004.   
[13] G. Tolle, J. Polastre, R. Szewczyk, D. Culler, N. Turner, K. Tu, S. Burgess, T. Dawson, P. Buonadonna, D. Gay et al., “A macroscope in the redwoods,” in Proceedings of ACM Conference on Embedded Networked Sensor Systems (ACM SenSys), 2005.   
[14] M. Buettner, G. Yee, E. Anderson, and R. Han, “X-mac: a short preamble mac protocol for duty-cycled wireless sensor networks,” in Proceedings of ACM Conference on Embedded Networked Sensor Systems (ACM SenSys), 2006.   
[15] W. Ye, J. Heidemann, and D. Estrin, “An energy-efficient mac protocol for wireless sensor networks,” in Proceedings of IEEE International Conference on Computer Communications (IEEE INFOCOM), 2002.   
[16] R. Zheng, J. Hou, and L. Sha, “Asynchronous wakeup for ad hoc networks,” in Proceedings of ACM International Symposium on Mobile Ad Hoc Networking and Computing (ACM MobiHoc), 2003.   
[17] I. Anderson, Combinatorial designs and tournaments. Oxford University Press, 1997.   
[18] X. Shen, X. Qian, B. Zhao, Q. Fang, and G. Dai, “Clapping and broadcasting synchronization in wireless sensor networks,” IEEE Tsinghua Science and Technology, vol. 16, no. 6, pp. 632–639, 2011.   
[19] G. Hardy and E. Wright, An introduction to the theory of numbers. Oxford University Press, 1979.   
[20] D. Zhang, T. He, Y. Liu, Y. Gu, F. Ye, R. K. Ganti, and H. Lei, “Acc: generic on-demand accelerations for neighbor discovery in mobile applications,” in Proceedings of ACM Conference on Embedded Networked Sensor Systems (ACM SenSys), 2012.   
[21] M. Bakht and R. Kravets, “Searchlight: asynchronous neighbor discovery using systematic probing,” ACM SIG-MOBILE Mobile Computing and Communications Review, vol. 14, no. 4, pp. 31–33, 2010.