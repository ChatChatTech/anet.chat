# VoIP Aggregation in Wireless Backhaul Networks

Yongzhen Zhuang $^{\dagger}$ , Kun Tan $^{\ddagger}$ , Vincent Shen $^{\dagger}$ , Yunhao Liu $^{\dagger}$

† Computer Science Department HKUST {cszyz, shen, liu}@cs.ust.hk

‡ Microsoft Research Asia
kuntan@microsoft.com

Abstract—The newly emerging wireless backhaul network has fundamental difficulties in supporting Voice over IP (VoIP) applications due to the MAC overheads introduced by huge amounts of small packets. Packet aggregation is a promising approach to mitigate these overheads. However, previous approaches to such problems are often stringent, not adaptive to the change of channel conditions. They are operated by each TAP (Transit Access Point) separately without any coordination in the use of shared channels. As a result, they fail to ensure the VoIP quality in terms of delay and loss. The major contribution of this paper is the proposal of a coordinated aggregation algorithm, which is adaptive and distributed. By coordinating with neighboring TAPs, the proposed algorithm is able to assign an appropriate aggregation rate to each TAP, aiming at better channel utilization and lower packet loss and delay. We evaluate this design by comprehensive analysis and simulations. The simulation results show that our algorithm significantly improves the VoIP capacity in wireless backhaul networks and outperforms existing aggregation algorithms.

Keywords-Voice over IP (VoIP); Wireless backhaul networks; Packet aggregation

# I. INTRODUCTION

With the proliferation of wireless technology and devices, “hot spot” services are becoming more attractive for providing users with seamless Internet access in public places. A backhaul network is required to inter-connect a number of geographically dispersed “hot spot” access points (AP) and further connect them to the Internet. Clearly, a traditional wired backhaul network is too expensive for rural areas. Therefore, a wireless backhaul network, which inter-connects APs using multi-hop wireless links based on the IEEE 802.11 technique [1, 2], is increasingly gaining more attention due to its easy and cheap deployment [3-6]. It is a natural expectation that the wireless backhauls should provide similar or better performance for most existing Internet applications, including real-time applications like VoIP, which has been identified as one of the most important real-time applications with potential commercial interest [7-11]. However, supporting VoIP applications over wireless backhaul networks poses a number of new challenges that have not existed in the previous Internet VoIP research [12-14].

One major challenge lies in that the IEEE 802.11 DCF (Distributed Coordination Function) is based on CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance) MAC protocol, which imposes great overheads to transmit small packets. Due to the real-time characteristics, VoIP applications usually generate voice data of many small packets. Consequently, the capacity of VoIP in such networks is surprisingly low [15-17]. Moreover, the multihop relays in the wireless backhaul networks further exaggerate the wireless overheads and incline to create congestion regions near the Internet Transit Access Point (ITAP).

Previous work [15] proposes to adjust voice encoder parameters to mitigate overheads by encoding large voice packets. This, however, increases the packetization delay. Since VoIP applications have a strict delay constraint, larger packetization delay often means less transmission budget for packet delivery, making it more difficult for underlying layers to fulfill the QoS requirements, especially for the multi-hop wireless backhaul networks. Worse, when the packet size is enlarged, the VoIP application quality tends to be sensitive to packet loss which is very difficult to conceal in stringent encoding approaches [12, 18].

In this paper, we propose an alternative way that uses packet aggregation to improve capacity to support VoIP in multihop wireless backhaul networks. Packet aggregation multiplexes voice packets from different connections into one large packet. In this way, the wireless channel utilization is improved without increasing the packetization delay of each individual flow. When an aggregated packet is lost, the loss is distributed among different flows and therefore can be easily concealed. Unlike previous packet aggregation methods, our approach adapts to each link along the end-to-end path, so that it may lead to a more efficient use of wireless channels.

The key challenge to design a packet aggregation algorithm is the aggregation rate for each TAP in a multihop wireless network. The aggregation rate determines the average time that a packet stays in a TAP's queue before it is sent out. Indeed, the optimal aggregation rate of one TAP cannot be determined by local knowledge only, because in a multihop wireless network, the wireless channel is a spatially shared resource. Wireless nodes within the interference range may compete for the same wireless channel, and at most one transmission is allowed at each time slot.

The major contribution of this work is the proposal of a coordinated packet aggregation algorithm. We develop a fluid model of packet aggregation for VoIP applications, and then provide a distributed solution to explicitly set the aggregation rate by coordinating with neighboring TAPs that compete for the same channel resource. We implemented our algorithm in the NS2 simulator and conducted extensive simulations. Results show the effectiveness of our algorithm. To the best of our knowledge, it is the first work that addresses the optimization of packet aggregation problem.

The rest of the paper is organized as follows. In Section II, we introduce the background. We detail our coordinated packet aggregation algorithm in Section III. We evaluate our proposal using excessive simulations and present the results in Section IV. The related work is discussed in Section V and Section VI concludes this work.

# II. BACKGROUND AND MOTIVATION

An example of a wireless backhaul network is shown in Figure 1. Each node in a wireless backhaul network is called Transit Access Point (TAP). A TAP receives traffic from mobile users, and relays this traffic to the Internet through multi-hop wireless links. A special TAP which accesses the wired Internet is called Internet Transit Access Point, or ITAP.

![](images/1e50e2f46b1a495a5fb2c0666b880e7a25b020ea202ecdea0d584d752e5e5028.jpg)



Figure 1. Wireless Backhaul forms a tree topology.

TAP communicates with adjacent TAPs using IEEE 802.11 technology in which CSMA/CA mechanism is adopted. In CAMA/CA collisions, back-off behavior, ACK frames, as well as the physical layer preamble constitute the significant overheads for small packets, which may contain only a few bytes of application data. The overheads are heavier if the RTS/CST (Request-To-Send/Clear-To-Send) handshake is adopted.

Such overheads greatly limit the number of VoIP flows supported in such wireless backhaul networks. Let us see the example shown in Figure 1, in which TAP 0 is launching an increasing amount of flows. Here IEEE 802.11b is used, which has 11Mbps data rate. We add VoIP flows from TAP 0 to ITAP (assuming every VoIP flow is going to the Internet). Each VoIP uses a GSM encoder which gives out 13.2kbps constant bit-rate (CBR) data flow. Fig. 2 and Fig. 3 plots the delay and loss rates of VoIP flows. After 9 flows join, the loss and delay start to increase sharply due to the network congestion. Packets are lost due to a) buffer overflow and b) the collision on the wireless channel. The example also reveals the fact that goodput is influenced more by packet overheads than by bandwidth. In Fig. 4, the goodput is limited to about 226.8 Kbps, although the bandwidth is as high as 11Mbps and the ideal goodput is expected to keep rising. This means that raising the bandwidth to 54M or even higher is not a solution for this problem. The above results are consistent with that in [15].

The fundamental difficulty is the heavy overhead encountered when transmitting large numbers of small packets. This overhead makes the transmission of a single package much slower, and hence it affects the queuing delay and loss. Adjusting the queuing buffer size is also not a solution of this problem, because longer buffer size is preferred for less packet loss, while shorter buffer size is required for keeping lower packet delay. We will see the tradeoff more in the simulation section. The basic and most effective solution of the problem is to get rid of the huge packet overhead, and this can be done by aggregating several small packets into a large packet. However, the aggregation is not that trivial. As the VoIP application is very sensitive to packet delay and loss, a good aggregation strategy should be delicate enough to ensure lower packet delay and loss in most situations. That means the aggregation algorithm should adapt to the dynamic situation. That motivates us to develop an adaptive and distributed packet aggregation algorithm, by which the overheads can be greatly mitigated and the packet delay and loss can be reduced.

# III. COORDINATED AGGREGATION ALGORITHM

We assume that a TAP maintains several queues, each for one out-link. When a VoIP packet arrives at the TAP, a timestamp is assigned to it, and the packet is put into a corresponding queue based on its next-hop address. When a TAP is idle, it checks each link queue in a round-robin manner. If one link queue satisfies one of the two conditions, the queue is chosen to be aggregated: a) if the queue size is larger than $K_{l}$ ; or b) if the timestamp of the head-of-line packet indicates that it is $T_{l}$ millisecond old. The aggregation is done by packing as many

![](images/1981e1f9a2ed2e823e20b5deb8326a419ee1aaa87a90ee54cff1961b06bd86a5.jpg)  
Figure 2 end-to-end delay

![](images/0d0edded67d1d96d4a709d14c56cd6de8410ea227d6dab32b77b59442428a7a4.jpg)



Figure 3. end-to-end loss

![](images/0e364d4d2637d036652ed898b2134fae651fb827fa2cbc717bbc6942980f4b4f.jpg)



Figure 4. goodput   
Fig. 2, Fig. 3, and Fig. 4. VoIP capacity of wireless backhaul networks is limited. Delay and loss increase sharply after 9 VoIP flows join over a 5-hop Chain. Goodput is limited at about 226.8Kbps though the bandwidth is as high as 11Mbps.

VoIP packets as possible into a large packet until the queue is empty or the aggregated packet is larger than MTU (Maximal

Transmission Unit). If no queue satisfies that, the TAP stays in an idle state. Note that although this TAP remains idle, it does not mean that the wireless channel is going to be idle. This is because the wireless channel is shared among all TAPs nearby and therefore other TAPs may access the channel when the TAP is idle. Also note here, although two parameters are used to control the aggregation, the relation between these two parameters is $K_{l} = \varphi_{l} \cdot T_{l}$ , given the average input rate of link $l$ as $\varphi_{l}$ . Therefore, the fundamental question is how to choose $T_{l}$ for each wireless link. We define $\lambda_{l} \equiv 1 / T_{l}$ as the packet aggregation rate of wireless link $l$ . After the above introduction, in the next subsection we formulate the problem of choosing the packet aggregation rate as an optimization problem, which minimizes the overall packet delay in the wireless backhaul network. Then, we propose a distributed solution to that problem.

# A. System Model

In this paper, the wireless backhaul network is modeled as a DAG (direct acyclic graph) including TAPs and uplinks. For easy demonstration we neglect the downlink since uplink and downlink are symmetric. In the remainder of this paper, without special indication all the expression of “link” refers to “uplink”. A clique contains the links that share the same wireless channel. All links in a clique mutually interfere with each other. They cannot transmit simultaneously. Therefore, a link can transmit if and only if none of the other links that share at least one clique is transmitting. We assume the same transmission range and interference range, then in Fig. 1, out-links of TAP 3, 4, and 5 can form a clique, but it is not a maximal one. Only those maximal cliques need to be considered. The solid ellipse in Fig. 1 shows an example of a maximal clique that contains out-links of TAP 3, 4, 5, 6 and 7. Thereby TAP 3, 4, 5, 6 and 7 cannot transmit on their out links, simultaneously. However, TAP 7 and TAP 2 can transmit at the same time as no clique can contain both TAP 7 and TAP 2’s out-links. Note that since the network topology is static, the clique information can be determined when the network is set up.

Let $L$ denote the set of uplinks, $L = \{l_1, l_2, \ldots l_N\}$ , and $Q$ denote the set of maximal cliques, $Q = \{Q_1, Q_2, \ldots, Q_M\}$ . Let $l_i \in Q_j$ denote uplink $l_i$ in clique $Q_j$ . The union of all $Q_j$ is the complete set $R$ , $R = \{\bigcup Q_j, \forall Q_j \in Q\}$ . Define a $|Q|\mathsf{X}|L|$ matrix $A$ , where $A_{j,i} = 1$ if $l_i \in Q_j$ ; and $A_{j,i} = 0$ otherwise.

# B. Packet Aggregation Rate Formulation

The packet aggregation rate of a link is the packet sending rate (pps) that link should adopt. The packet aggregation rate of the uplink $l_{i}$ is denoted as $\lambda_{l_i}$ . We formulate this aggregation rate as an optimization problem, where the constraints and the objective function are as follows:

# Flow Conservation Property

This property describes the fact that the incoming data rate (bps) of a link $l_{i}$ equals the outgoing data rate. Each link has a corresponding next-hop queue at its front end TAP. The outgoing rate of $l_{i}$ is the output rate of the next-hop queue, which is also the packet sending rate (or aggregation rate) $\lambda_{l_i}$ . The incoming data rate of the $l_{i}$ is the incoming rate of the next-hop queue, summing from its incoming links and local VoIP flows. Applying the flow conservation property, we obtain the following equation:

$$
\lambda_ {l _ {i}} S _ {l _ {i}} = \sum_ {l _ {k}} \widetilde {\lambda} _ {l _ {k}, l _ {i}} \widetilde {S} _ {l _ {k}, l _ {i}} + \omega_ {l _ {i}} \lambda_ {0} S _ {0}, \tag {1}
$$

where $\lambda_{l_i}$ and $S_{l_i}$ represent the packet sending rate and the packet size of link $l_i$ . $\widetilde{\lambda}_{l_k,l_i}$ and $\widetilde{S}_{l_k,l_i}$ is the incoming rate and incoming packet size from $l_k$ to $l_i$ . We let $\omega_{l_i}$ denote the number of local VoIP flows traversing through link $l_i$ , and let $\lambda_0$ and $S_0$ denote the predefined packet sending rate and packet size of VoIP applications. The summation on the right adds up the incoming data rate, either from each incoming link or from the local traffic. Therefore (1) can be written as:

$$
\lambda_ {l _ {i}} S _ {l _ {i}} = \widetilde {\omega} _ {l _ {i}} \lambda_ {0} S _ {0}, \tag {2}
$$

where $\widetilde{\omega}_{l_i}$ can be interpreted as the total number of all VoIP flows that pass through link $l_{i}$

$$
\widetilde {\omega} _ {l _ {i}} = \frac {\sum_ {l _ {k}} \widetilde {\lambda} _ {l _ {k} , l _ {i}} \widetilde {S} _ {l _ {k} , l _ {i}}}{\lambda_ {0} S _ {0}} + \omega_ {l _ {i}}. \tag {3}
$$

# Capacity Constraint

The capacity constraint ensures that the utilized capacity is no more than the overall capacity that a channel can offer. Let $\rho C$ be the portion of capacity reserved for VoIP traffic. The capacity constraint of each clique $Q_{k}$ is given by

$$
\sum_ {l _ {i} \in Q _ {k}} 2 \lambda_ {l _ {i}} (S _ {l _ {i}} + O) \leq \rho C, \tag {4}
$$

where $O$ is a constant, which counts for the overheads of transmitting a packet. This inequation points that data rate including overheads in a clique should not be more than the available channel capacity. Simplifying (4) with (2), we have

$$
\sum_ {l _ {i} \in Q _ {k}} \lambda_ {l _ {i}}: C _ {Q _ {k}}, \tag {5}
$$

where $C_{Q_k}$ is a constant, thus

$$
C _ {Q _ {k}} = \frac {\frac {1}{2} \rho C - \sum_ {l _ {i} \in Q _ {k}} \widetilde {\omega} _ {l _ {i}} \lambda_ {0} S _ {0}}{O}. \tag {6}
$$

# MTU Constraint

The aggregated packet size $S_{l_{i}}$ should not exceed MTU. The MTU constraint is further simplified using (2) as follows:

$$
\lambda_ {l _ {i}} \geq \sigma_ {l _ {i}}, \tag {7}
$$

where $\sigma_{l_i}$ is a constant,

$$
\sigma_ {l _ {i}} = \frac {\widetilde {\omega} _ {l _ {i}} \lambda_ {0} s _ {0}}{M T U}. \tag {8}
$$

# Objective Function

The objective is to minimize the delay in the system.

$$
\min \sum_ {l _ {i} \in L} (\frac {1}{\lambda_ {l _ {i}}} + \frac {S _ {l _ {i}}}{C}) \tag {9}
$$

The system delay includes two parts: the delay introduced by aggregation queuing and the delay of the packet transmission. They correspond to the two terms inside the summation of (9). Simplifying (9) using (2) again, we have

$$
\min \sum_ {l _ {i} \in L} \frac {\xi_ {l _ {i}}}{\lambda_ {l _ {i}}} \text {,} \tag {10}
$$

where $\xi_{l_i}$ is a constant

$$
\xi_ {l _ {i}} = 1 + \frac {\widetilde {\omega} _ {l _ {i}} \lambda_ {0} s _ {0}}{C}. \tag {11}
$$

# Optimization Problem

The optimization problem (P) is written as follows:

$$
\min \sum_ {l _ {i} \in L} \frac {\xi_ {l _ {i}}}{\lambda_ {l _ {i}}} \text {,} \tag {12}
$$

s.t.

$$
A \lambda \leq C _ {Q}
$$

$$
\lambda \geq c
$$

Vector $\lambda$ ( $\lambda_1, \lambda_2, \ldots, \lambda_N$ ) is the aggregation rate of $N$ links. Vector $C_Q$ is ( $C_{Q_1}, C_{Q_2}, \ldots, C_{Q_M}$ ) for $M$ cliques calculated by Formula 4; vector $c$ is ( $\sigma_{l_1}, \sigma_{l_2}, \ldots, \sigma_{l_N}$ ) for $N$ cliques by Formula 8.

# C. Decentralized Solution

The optimization problem (P) in (12) is mathematically tractable, but it requires the global information of $\xi_{l_i}$ , $c_{l_i}$ , $\widetilde{a}_{l_i}$ and $C_{Q_k}$ for all $l_i \in L$ and $Q_k \in Q$ . In this section, we explore a decentralized algorithm to approximate (P).

We can use the Lagrange relaxation to solve the problem define in (12). We define the Lagrangian as

$$
L = - \sum_ {l _ {i} \in L} \frac {\xi_ {l _ {i}}}{\lambda_ {l _ {i}}} - \alpha^ {T} (A \lambda - C _ {Q}) - \beta^ {T} (\sigma - \lambda), \tag {13}
$$

where vector $\alpha$ and $\beta$ are Lagrange multipliers. Then the local optimum is given by the Kuhn-Tucker conditions.

$$
\frac {\partial L}{\partial \lambda_ {l _ {i}}} = \frac {\xi_ {l _ {i}}}{\lambda_ {l _ {i}} ^ {2}} - \sum_ {Q _ {j}: l _ {i} \in Q _ {j}} \alpha_ {j} + \beta_ {i} = 0 \tag {14}
$$

$$
\alpha \geq 0, A \lambda \leq C _ {Q} \text { and } \alpha^ {T} (A \lambda - C _ {Q}) = 0 \tag {15}
$$

$$
\beta \geq 0, \lambda \geq c \text { and } \beta^ {T} (\sigma - \lambda) = 0 \tag {16}
$$

Note that (P) has been decoupled in (14). We therefore define an adjustment strategy as

$$
\dot {\lambda} _ {l _ {i}} = \kappa (\xi_ {l _ {i}} - \lambda_ {l _ {i}} ^ {2} \sum_ {Q _ {j}: l _ {i} \in Q _ {j}} p _ {j} (\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}}) + \lambda_ {l _ {i}} ^ {2} p (\lambda_ {l _ {i}})), \tag {17}
$$

where $p_{j}$ is interpreted as the price to charge by clique $Q_{j}$ per square-unit of aggregation rate; p is a reward to praise per square-unit of aggregation rate. The adjustment comprises a steady increase at a rate proportional to $\xi_{l_{i}}$ , a quadratic decrease proportional to the price, and a quadratic increase proportional to the reward, and $\kappa$ is the speed of the adjustment.

This adjustment strategy coincides with a strictly increasing system and is going to be stable at some point. We construct the Lyapunov function for the system (17) as follows:

$$
V = - \sum_ {l _ {i} \in L} \frac {\xi_ {l _ {i}}}{\lambda_ {l _ {i}}} - \sum_ {Q _ {j} \in Q} \int_ {0} ^ {\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}}} p _ {j} (y) d y + \int_ {0} ^ {\lambda_ {l _ {i}}} p (y) d y. \tag {18}
$$

The maximum of $V$ is achieved at $\lambda^{*}$ when

$$
\frac {\partial V}{\partial \lambda_ {l _ {i}}} = \frac {\xi_ {l _ {i}}}{\lambda_ {l _ {i}} ^ {2}} - \sum_ {Q _ {j}: l _ {i} \in Q _ {j}} p _ {j} (\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}}) + p (\lambda_ {l _ {i}}) = 0. \tag {19}
$$

The time derivative of $V$ is

$$
\begin{array}{l} \dot {V} = \sum_ {l _ {i} \in L} \frac {\partial V}{\partial \lambda_ {l _ {i}}} \cdot \dot {\lambda} _ {l _ {i}} \tag {20} \\ = \kappa \sum_ {l _ {i} \in L} \frac {1}{\lambda_ {l _ {i}} ^ {2}} (\xi_ {l _ {i}} - \lambda_ {l _ {i}} ^ {2} \sum_ {Q _ {j}: l _ {i} \in Q _ {j}} p _ {j} (\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}}) + \lambda_ {l _ {i}} ^ {2} p (\lambda_ {l _ {i}})) ^ {2} \\ \end{array}
$$

where $\dot{V}$ is positive. Equation (20) shows that in the system (17), V is strictly increasing, and therefore it is stable at point $\lambda^{*}$ that maximizes V.

We further define the price function and award function as

$$
p _ {j} (\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}}) = (\frac {\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}} - C _ {Q _ {j}}}{\sum_ {l _ {k} \in Q _ {j}} \lambda_ {l _ {k}}}) ^ {+} \tag {21}
$$

and $p(\lambda_{l_i}) = \left(\frac{\sigma - \lambda_{l_i}}{\sigma}\right)^+$ . (22)

# D. System Implementation

We show a decentralized approach that approximates the original optimization problem (P). This approach employs the strategy defined in (17) to adaptively adjust the aggregation rate in every u millisecond. The implementation details of this decentralized approach are as follows.

(a) Each TAP monitors the transmission rate of its neighbors, and exchanges this information, i.e. $\lambda_{l}$ and $S_{l}$ , with its two hop neighbors. Note that no additional control packet may be created. This information exchange can be attached in the VoIP packets.   
(b) Each TAP updates $\lambda_{j}$ for each of its out-link. The update is based on the clique information of the out-link and the latest $\lambda_{j}$ and $S_{j}$ .

1 MAC header is sent in Data Rate; 2 ACK is sent in Basic Rate.   
TABLE 1: PARAMETERS USED IN THIS SIMULATION.(802.11G MIXED MODE) 

<table><tr><td>MAC_HDR</td><td>34bytes</td><td>ACK</td><td>14bytes</td></tr><tr><td>DIFS</td><td>50μsec</td><td>PHY Preamble</td><td>20+6μsec</td></tr><tr><td>SIFS</td><td>10μsec</td><td>Data Rate</td><td>54 Mbps</td></tr><tr><td>slot timeσ</td><td>20μsec</td><td>Basic Rate</td><td>6 Mbps</td></tr><tr><td>E[CW]</td><td>15/2</td><td>Other HDR</td><td>40bytes</td></tr></table>

(c) After the periodical update in (b), each TAP informs other TAPs at the back end of each out-link its current aggregation rate $\lambda_{l}$ , such that the aggregation rate can be applied to the corresponding downlink.

(d) As a result each TAP maintains several next-hop queues for its uplinks and downlinks. Each queue is associated with an aggregation rate $\lambda_{l}$ . These queues conduct aggregation according to the two parameters $K_{l}$ and $T_{l}$ derived from $\lambda_{l}$ , as is described at the beginning of this section.

# IV. SIMULATION RESULTS

We use NS2 to conduct a series of tests, comparing coordinated aggregation and previous aggregation approaches. Jain et al proposed an aggregation approach that aggregates all the packets in the next-hop queue once a packet transmission is triggered. We call this approach simple aggregation as it is straightforward and does not actively adjust the aggregation rate collaboratively with neighboring nodes. Such simple aggregation is sensitive to queuing buffer size, which is the number of packets that can be queued in each TAP. In our simulations, we make two implementations of simple aggregation: one with longer buffer size (len = 1000), and the other with shorter buffer size (len = 50). The wireless parameters used in the simulation are listed are listed in table 1.

We conduct case studies on different topologies: (a) A multi-hop train, in which increasing amount of VoIP flows are sending from TAP 0 to ITAP in Fig. 1. (b) A multi-hop tree, in which VoIP flows are sending from TAP 1-8 to ITAP in Fig. 1. (c) A Grid topology, where the ITAP is placed at the top right corner. The size of the topology increases from 4 TAPs to 81 TAPs, in the meanwhile the longest hop count increases from 1 to 7. In the simulation each VoIP flow stands for a VoIP session using a GSM encoder that has 13.2kbps constant output data rate.

In our simulations, we mainly focus on two performance metrics: end-to-end delay and the end-to-end packet loss rate. For the simple aggregation algorithms, there is always a trade-off between delay and loss rate. Fig. 5 and Fig. 7 plot the average end-to-end delay of multihop chain and tree cases of two simple aggregation algorithms and coordinated aggregation algorithm. Coordinated aggregation has the lowest delay of the three. It is clear that with short buffer size, simple aggregation can preserve relatively low delay in spite of increasing traffic load. This is because the small buffer size prevents the accumulation of queuing delay. However, the delay of simple aggregation with longer queue is pretty high. A very long queue is easily built up as simple aggregation can not coordinate the transmission properly. According to the MTU constraint, at most 33 packets can be aggregated in each round of aggregation. This means that to empty a long buffer about 30 rounds of aggregation are needed, leading to higher delay. Although short buffer outperforms longer buffer in delay, it suffers high loss rate. Fig. 6 and Fig. 8 plot the loss rate. We examine the turning point at which the packet loss increases abruptly. In both figures, the turning point of coordinated aggregation is at the right most. In Fig. 6 (Fig. 8), the short buffer simple aggregation turns at 10 (5) flows, the longer buffersimple aggregation turns at 24 (19) flows, while coordinated algorithm turns at 28 (23) flows. They show that coordinated aggregation can support many more VoIP flows.

In general, if we use a short buffer size in simple aggregation algorithms, almost all of the queuing delays are reduced, but a great deal of queuing losses still remains. If a longer buffer size is used, the queuing losses are reduced to an acceptable level, but the queuing delays rise sharply. On the other hand, our coordinated aggregation algorithm can provide both lower delays and lower losses through an adaptive packet aggregation rate adjustment.

We then examine the scalability of proposed coordinated aggregation by increasing topology sizes. The number of TAPs in this simulation set is increased from 3 to 81, where each TAP has 2-4 neighbors and each participating TAP is sending out 5 VoIP flows. With the increasing number of TAPs, the maximum hop count is also increased from 1 to 7. An 81-TAP wireless backhaul network is able to cover most of the campus or residential area. The results are shown in Fig. 9 and Fig. 10. In Fig. 9, the delay of coordinated aggregation is always less than 10ms, which is the lowest of the three. In Fig. 10, we see the packet loss rate of coordinated aggregation much lower than the other two. Even in a bigger topology (more than 80 TAPs in the network), the loss rate is still less than $30\%$ . This loss is distributed among different flows, so its affection on each flow is diminished. When the system has more than 30 TAPS, both the delay and the loss rates increase sharply, as shown in Fig. 9 and Fig. 10. However, compared with the other two algorithms, coordinated aggregation still has about $89\%$ improvement in delays and $62\%$ improvement in loss rates.

# V. RELATED WORK

The problem of 802.11 protocols in dealing with small packet transmission has long been recognized. Hole and Tobagi found that each AP can only support a few VoIP flows due to the large overheads of 802.11 MAC in processing small packets [15]. Many WLAN approaches have been proposed to get rid of these overheads. Lin et al removed the expensive MAC-layer ACK and used redundancy to guarantee successful transmission [19]. Other research resorted to packet aggregation to alleviate the situation: for examples, Tourrilhes [16] and later Ransbottom [20] proposed packet aggregation in the WLAN, where each wireless station aggregates its own packets before sending to the AP.

![](images/f0865912f3ac14b94c60024ae60726ab4ef79d6ecbc000a6c2389ec838e6b9ae.jpg)



Figure 5. end-to-end delay of multihop chain

![](images/70f35e5b0b8470538db2a9227ecaadd4097859092cd9a5ec339aeb8ce97cf889.jpg)



Figure 7. end-to-end delay of multihop tree

![](images/8b6118e3688d677eeca480d77abbc0b97df0fc7beff518091ad9c6e049469a8e.jpg)



Figure 9. delay of increasing topology

![](images/68623ca5ca6d1fea95172aabd2f2b8c14d2365408c78b93937caacc941a16abb.jpg)



Figure 6. end-to-end loss of multihop chain

![](images/0621f74916c498b715cf2f58d6b78c58722da51aef94b6cb9fc2a3ead7ab2fb0.jpg)



Figure 8. end-to-end delay of multihop tree

![](images/998e0c7be5b826922f7fdbef6178a69b489b1e42370255d1b9ba84d492502f59.jpg)



Figure 10. loss of increasing topology

Karl et al and Jain et al proposed a fix aggregation algorithm that can be adopted in multihop wireless links. In their methods, packets are collected in separate next-hop queues. They are aggregated whenever enough packets have been collected or they have been delayed for some fixed duration $[21]$ . However this algorithm is not practical, as it asks the users to predefine some fixed aggregation parameters. It cannot cope with the changing channel conditions or ensure the minimum packet delay. Jain et al proposed another aggregation algorithm in which all the packets waiting in the same next-hop queue are aggregated just before the transmission $[17]$ . In this method, each TAP aggregates packets separately while they share the same wireless channel. Without coordination, this sharing is unable to lead to optimal channel utilization. That is why we proposed a coordinated aggregation algorithm, which adapts to dynamic channel condition and can be implemented in a distributed manner.

# VI. CONCLUSIONS

In this paper, we study how to use packet aggregation for VoIP applications in multi-hop wireless backhaul networks. We propose a coordinated aggregation algorithm that is adaptive to dynamic channel conditions in a distributed manner. We evaluate the proposed approach through comprehensive simulations.

# REFERENCES

[1] IEEE., "Wireless LAN medium access control (MAC) and physical layer (PHY) specifications: further higher data rate extension in the 2.4 GHz band," 2003.   
[2] IEEE., "Wireless LAN medium access control (MAC) and physical layer (PHY) specifications," IEEE Standard 802.11 1999.   
[3] R. Karrer, I. A. Sabharwa, and E. Knightly, "Enabling Large-scale Wireless Broadband: The Case for TAPs," In Proceedings of ACM HotNets, 2003.   
[4] M. Zhang and R. S. Wolf, "Using multi-hop for broadband fixed wireless access in rural areas," In Proceedings of Wireless Communications, 2004.

[5] B. Chambers, "The grid roofnet: a rooftop ad hoc wireless network," in M.S. Thesis, MIT, 2002.   
[6] V. Gambiroza, B. Sadeghi, and E. Knightly, "End-to-end performance and fairness in multihop wireless backhaul networks," In Proceedings of MOBICOM, 2004.   
[7] V. Varshney, A. Snow, M. McGivern, and C. Howard, "Voice over IP," in Commun. ACM, 2002, pp. 89-96.   
[8] P. Mehta and S. Udani, "Voice over IP," in IEEE Potentials, vol. 20, 2001, pp. 36-40.   
[9] Skype, "Peer-to-peer telephony," http://www.skype.com.   
[10]Net2Phone, "A telecommunications application," http://www.net2phone.com/.   
[11]Peerio444, "a multi-level, open-source project for serverless client software for VoIP," http://www.populartelephony.com.   
[12]C. Boutremans and J.-Y. L. Boudec, "Adaptive joint playout buffer and FEC adjustment for Internet telephony," In Proceedings of INFOCOM, 2003.   
[13]Y. J. Liang, E. G. Steinbach, and B. Girod, "Real-time voice communication over the Internet using packet path diversity," In Proceedings of ACM MM, Ottawa, Canada, 2001.   
[14]Y. L. Liang, N. Farber, and B. Girod, "Adaptive playout scheduling and loss concealment for voice communication over IP networks," IEEE Transactions on Multimedia, vol. 5, pp. 532 - 543, 2001.   
[15]D. P. Hole and F. A. Tobagi, "Capacity of an IEEE 802.11b wireless LAN supporting VoIP," In Proceedings of IEEE Int. Conference on Communications (ICC), 2004.   
[16]J. Tourrilhes, "Packet frame grouping: improving IP multimedia performance over CSMA/CA," In Proceedings of ICUPC, 1998.   
[17]A. Jain, M. Gruteser, M. Neufeld, and D. Grunwald, "Benefits of packet aggregation in ad-hoc wireless network," Technical Report of University of Colorado 2003.   
[18]J. Rosenberg, "G.729 error recovery for Internet telephony," Columbia University Technical Report 2001.   
[19]C. Lin, H. Dong, U. Madhow, and A. Gersho, "Supporting real-time speech on wireless ad hoc networks: Inter-packet redundancy, path diversity, and multiple description coding," In Proceedings of WMASH, Philadelphia, Pennsylvania, USA., 2004.   
[20]J. S. Ransbottom, "Mobile wireless system interworking with 3G and packet aggregation for wireless LAN," Virginia Tech, 2004.   
[21]D. Karl, S. Monahan, and A. Whitman, "KarlNet's TurboCell: enhancing the capabilities of standard 802.11," white paper of Karlnet Inc 2003.