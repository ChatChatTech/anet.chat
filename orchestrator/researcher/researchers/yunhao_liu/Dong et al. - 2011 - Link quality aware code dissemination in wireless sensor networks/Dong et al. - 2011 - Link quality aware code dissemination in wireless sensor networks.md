# Link Quality Aware Code Dissemination in Wireless Sensor Networks

Wei Dong1;2, Yunhao Liu1;3, Chao Wang4, Xue Liu5, Chun Chen2, and Jiajun Bu2

1CSE Department, HKUST; 2CS College, Zhejiang University;

3TNLIST, School of Software, Tsinghua University;

4Beijing University of Posts & Telecommunications; 5McGill University

{dongw, liu}@cse.ust.hk, wangchao2000@bupt.edu.cn, xueliu@cs.mcgill.ca, {chenc, bjj}@zju.edu.cn

Abstract—Wireless reprogramming is a crucial technique for software deployment in wireless sensor networks (WSNs). Code dissemination is a basic building block to enable wireless reprogramming. We present ECD, an Efficient Code Dissemination protocol leveraging 1-hop link quality information. Compared to prior works, ECD has three salient features. First, it supports dynamically configurable packet sizes. By increasing the packet size for high PHY rate radios, it significantly improves the transmission efficiency. Second, it employs an accurate sender selection algorithm to mitigate transmission collisions and transmissions over poor links. Third, it employs a simple impact-based backoff timer design to shorten the time spent in coordinating multiple eligible senders so that the largest impact sender is most likely to transmit. We implement ECD based on TinyOS and evaluate its performance extensively. Testbed experiments show that ECD outperforms state-of-the-art protocols, Deluge and MNP, in terms of completion time and data traffic. (e.g., about 20% less traffic and 20–30% shorter completion time compared to Deluge).

# I. Introduction

Recent advances in microelectronic mechanical systems and wireless communication technologies have fostered the rapid development of networked embedded systems like wireless sensor networks (WSNs) [1]. WSN applications often need to be changed after deployment for a variety of reasons— reconfiguring a set of parameters, modifying tasks of individual nodes, and patching security holes. Many large-scale WSNs [17], however, are deployed in environments where physically collecting previously deployed nodes is either very difficult or infeasible. Wireless reprogramming is a crucial technique to address such challenges.

Code dissemination is a basic building block for wireless reprogramming [5], [28]. Existing code dissemination protocols (represented by Deluge [11] and MNP [12]) adopt several key techniques to ensure high reliability and performance. First, they exchange control-plane messages (ADV-REQ-DATA) for high reliability [11], [12], [28]. Second, they segment a large code object into fixed-sized pages for pipelining [11], [12]. The page transmission time and inter-page negotiation time (which involves control-plane message exchanges) are therefore two major contributors to the overall completion time.

However, existing protocol designs exhibit their inefficiency in two main aspects. First, the data throughput efficiency—the ratio between the network throughput and PHY data rate— degrades rapidly as the PHY rate increases. For example, given the packet size of approximately 36 bytes in both Deluge and MNP (both were originally designed for the 19.2Kbps CC1000 radio), the efficiency ratio of the current 250Kbps CC2420 radio is only 12.5%. Second, the current sender selection algorithm in MNP [12] (for addressing the broadcast storm problem [20]) does not consider link quality information and needs multiple rounds of message exchanges, resulting in transmission redundancy and longer completion time.

To address the first issue, we would like to increase the packet size to improve the transmission efficiency. This approach is appropriate for code dissemination because the traffic is always saturated and there are no delay constraints on individual packets. However, it would be inflexible to fix the packet size to its maximum allowable size as a fixed packet size may not be appropriate for all platforms under all the conditions [4]. Therefore, we support dynamically configurable packet sizes in our protocol design. By increasing the packet size for high PHY radios, it significantly improves the transmission efficiency.

To address the second issue, we leverage 1-hop neighbors’ link quality information learned over the air to improve the sender selection accuracy. We dynamically estimate the impact of senders by considering both uncovered neighbors (i.e., neighbors that do not receive an entire page) and the link qualities to these neighbors. A node’s transmission is considered more effective if the node has more uncovered neighbors with good link qualities. Considering link qualities help to put less weight on potential senders with poor outbound link qualities, thus mitigating transmissions for accommodating low PRR (packet reception ratio) receivers. This is especially important when large packets are transmitted over the air. Given many candidate senders, our design needs to ensure the best sender transmits while avoiding simultaneous retransmission attempts that can lead to duplicates or collisions. Prior work [12] needs multiple rounds of message exchanges and explicit requests from receivers, resulting in high transmission overhead and long delays. We address this issue by proposing a fast sender selection mechanism that does not require explicit coordination. The basic idea is to prioritize sender transmissions so that the best sender with the largest impact is most likely to transmit.

We incorporate the above design principles into a new code dissemination protocol, ECD. We implement it based on the TinyOS operating system. We examine ECD’s performance extensively through a 25-node testbed as well as TOSSIM [14] simulations. Evaluation results show that, (i) by supporting large packets, ECD significantly shortens the completion time. (ii) by supporting accurate sender selection that leverages information learned over the air, ECD effectively reduces contentions and collisions, resulting in fewer packet transmissions. (iii) by the impact-based backoff timer design, ECD reduces the inter-page negotiation time, also shortening the completion time.

In summary, the contributions of this paper are as follows.

- We design a new dissemination protocol that supports dynamically configurable packet sizes. By increasing the packet size for high PHY rate radios, it significantly improves the transmission efficiency.   
- We propose an accurate sender selection algorithm by leveraging 1-hop neighbors’ link quality information learned over the air, which effectively reduces transmission collisions and transmissions over the poor links.   
- We present an impact-based backoff timer design to shorten the time spent in coordinating multiple eligible senders so that the largest impact sender is most likely to transmit.   
We implement the dissemination protocol based on the TinyOS operating system. Both testbed and simulation results show that we effectively improve the performance in terms of completion time and data transmissions.

The rest of this paper is structured as follows. Section II describes the motivation behind the work. Section III presents the design details. Section IV describes the evaluation results. Section V introduces the related work, and finally, Section VI concludes the paper and gives future research directions.

# II. Motivation

This section identifies the need to incorporate two basic design principles, i.e., dynamically configurable packet sizes and sender selection, into our design.

# A. Dynamically Configurable Packet Sizes

The TinyOS CSMA MAC protocol arbitrates access among multiple potential senders and selects one as the winner. The TinyOS CSMA MAC protocol operates as follows. When a data packet is delivered to the MAC layer, the MAC layer performs an initial backoff without sensing the channel. The initial backoff time is randomly selected in $[ 0 , C W _ { \mathrm { i n i t } } )$ where $C W _ { \mathrm { i n i t } } \approx 1 0 \mathrm { m s } .$ . When the initial backoff timer fires, the MAC layer performs clear channel assessment (CCA) to check whether the channel is busy. If the channel is clear, the data packet is transmitted immediately. If the channel is busy, the MAC layer performs a congestion backoff. The congestion backoff time is randomly selected in $[ 0 , C W _ { \mathrm { c o n g e s t i o n } } )$ where $C W _ { \mathrm { c o n g e s t i o n } } \approx 2 . 5 \mathrm { m s }$ . The MAC layer will repeatedly perform the congestion backoff until the channel is clear and the data packet is transmitted out. Figure 1 illustrates the channel access timing diagram of the TinyOS CSMA MAC.

We can build a simple analytical model to compute the efficiency ratio under TinyOS CSMA MAC. Assume there are no packet collisions, so the expected backoff time is $W =$ $C W _ { \mathrm { i n i t } } / 2$ . The packet header consumes H bytes $( H \approx 1 2$ in TinyOS). We assume the remaining data payload length to be l bytes. The efficiency ratio can be computed as,

![](images/30545ae8cc4d0c4c05bdc753121c6424fb9ba86f4b74cf26022100859d644b71.jpg)



Fig. 1: Illustration of TinyOS CSMA access method. The black triangle indicates a busy channel while the white triangle indicates a clear channel.

![](images/fb6a67734bf9ce126c9c29976da2c3beb5fb7e1ab79f33438fe5616405076fbc.jpg)



Fig. 2: Efficiency ratios with varying packet payload length for CC2420 (250Kbps) and CC1000 (19.2Kbps).

$$
\eta = \frac {t _ {\text { data }}}{W + t _ {\text { preamble }} + t _ {\text { data }}} \tag {1}
$$

where $\begin{array} { r } { t _ { \mathrm { p r e a m b l e } } = \frac { H } { \mathrm { P H Y ~ R a t e } } } \end{array}$ （2 and $\begin{array} { r } { t _ { \mathrm { d a t a } } = \frac { l } { \mathrm { P H Y } \mathrm { R a t e } } } \end{array}$ . For example, under CC2420 with 250Kbps PHY rate, for a packet with payload length $l = 2 8$ bytes, the time for transmission is $\begin{array} { r } { = \frac { 2 8 \times 8 } { 2 5 0 } = 0 . \dot { 8 } 9 6 \mathrm { m s } . } \end{array}$ D . Figure 2 shows the efficiency ratios for different packet payload sizes under 250Kbps CC2420 radio and 19.2Kbps CC1000 radio. We can see that using small packets may not be a big issue in low PHY rate radios. It, however, can be extremely inefficient for high PHY rate. For example, with the default data packet payload size of 28 bytes in Deluge [11], the efficiency ratio under CC2420 is only 14.3%. This means that the 250Kbps data rate can sustain an actual throughput of only 35.6Kbps. Increasing the packet size for high PHY rate can effectively improve the transmission efficiency.

Nevertheless, large packets may not be always beneficial for all platforms under all conditions. Prior works [4], [13] demonstrate that a tradeoff exists between the desire to reduce header overhead by making packet large and the need to reduce packet error rates by using small packet length (e.g., when there is WiFi interference [9]). Existing code dissemination protocols cannot support different packet sizes without recompiling the protocol code. To address this issue, we support dynamically configurable packet sizes in our protocol design. System designers can thus configure the packet payload size in operating networks for improved performance (according to network models or experimental observations). We will present the design details in Section III-A.

With the above design principle, we can effectively increase the packet size for high PHY rate radios. As large packets are more susceptible to (i) packet losses induced by protocol interference (ii) packet losses induced by channel link quality. Hence, we need to propose techniques to reduce the transmission collisions and transmissions over poor links. This motivates us to employ sender selection into our design.

![](images/c1fa304e3451a0a135ce03e57561be2fc504aa6f3d451fd14aa57ef23bbf4d96.jpg)



Fig. 3: An example of sender selection. The figures near the arrows indicate the link qualities in terms of packet reception ratio (PRR).

# B. Sender Selection

Sender selection is a well studied technique to reduce contentions, collisions in broadcast protocols. It was also adopted in a previous code dissemination protocol—MNP [12] for improved performance. The basic principle in these algorithms is to select the best sender for forwarding the data while avoiding simultaneous transmissions from other neighboring nodes. This involves two main aspects. First, an accurate metric should be devised to estimate senders’ impacts. Second, efficient mechanisms should be designed to coordinate transmissions of eligible senders so that the largest impact sender is most likely to transmit.

Sender selection in broadcast protocols is a special case of sender selection in code dissemination protocols (i.e., one page, one packet). Sender selection in code dissemination protocols is more complex. For example, (i) code dissemination should be 100% reliable, so senders are enforced to receive requests for transmission; (ii) neighboring nodes should determine whether a page transmission is in the vicinity given the packet transmission within a page is not continuous.

MNP is a code dissemination protocol that incorporates sender selection. The metric it uses for sender selection is the received number of distinct requests. A sender with more requests is more suitable for transmission because its transmission can cover more receivers. The best sender is selected via multiple rounds: the existence of a best node makes other neighboring nodes inactive; then the receivers explicitly request the code from the active sender. The problem therein is that it can cause biased estimation of node’s real impact, resulting in unnecessary packet transmissions.

Figure 3 illustrates the benefits of our accurate sender selection algorithm. In this example, S is the source node. Assume there are 20 packets per page. After S’s transmission of a page, N1 is covered while N2 and N3 only receive 5 packets. With MNP’s approach, S will be the next sender because it will receive the most number of requests. S needs to transmit at least $\frac { 2 0 } { 0 . 2 5 } - 2 0 = 6 0$ packets to cover N2 and N3, even if N2 and N3 lose the same packets within the page. ECD considers link qualities. By one round of page transmission, S cannot cover one receiver whereas N1 can cover N2. Therefore, N1 will be sender (covering N2 by one page transmission), followed by N2 being the next sender (covering N3 by one page transmission). MNP requires at least $\frac { 2 0 } { 2 5 \% } = 8 0$ (by S) packet transmissions while our approach requires $2 0 ( { \tt b y } \ { \tt S } ) + 1 5 ( { \tt b y } \ { \tt N } { \tt l } ) + 1 5 ( { \tt b y } \ { \tt N } { \tt 2 } ) = 5 0$ packet transmissions. The key insight of our approach is to utilize 1-hop neighbors’ link quality information, so that we can put less weight on nodes with poor outbound link quality (S in this case), resulting in fewer packet transmissions.

Distinct from sender selection in broadcast protocols, the neighboring nodes that failed the competition need to estimate the length of ongoing page transmission to avoid simultaneous transmissions. In traditional broadcast protocols, there is no such a problem because a single packet transmission occupies the channel so other nodes will not detect an idle channel (and transmit). In code dissemination protocols, however, neighboring nodes can detect an idle channel because packet transmissions within a page is not continuous. ECD addresses this issue by attaching small meta-data to packets, so that neighboring nodes can accurately predict the activities in the neighborhood.

ECD also needs to shorten the time spent in coordinating the transmission of multiple eligible senders so that the largest impact sender is most likely to transmit. Instead of using MNP’s approach which involves multiple rounds of message exchanges, we employ a simple impact-based backoff timer design that does not require explicit coordination among neighboring nodes.

We will describe how we accurately estimate senders’ impacts in Section III-B and how we coordinate the transmissions of eligible senders in Section III-C.

# III. Design

ECD adopts several key design principles: (i) segmentation and pipelining for scalability in large-scale networks. (ii) inter-page negotiation for 100% reliability, and (iii) adaptive advertisement through Trickle timer [15] to reduce the controlplane traffic. The Trickle timer controls the send rate so that the send rate decreases exponentially when the network is steady and increases to its maximum when inconsistency is found.

ECD consists of five main phases. Figure 4 shows the state transition diagram of ECD. Initially, a node (say S) stays in the IDLE state, advertising about the completed pages it has received. When another node (say R) hears the ADV message, and finds that S has more pages, it sends an REQ message to S and transits into the RX state. R transits back to the IDLE state only when it completely receives the current page. When S overhears the REQ message (note the REQ message may not destined to S), it transits into the ESTIMATION state, waiting for more requests in order to estimate its impact. When the estimation timer fires, S enters into the CONTENTION state. In the contention period, nodes (that overhear the REQ messages) backoff according to their estimated impacts. The largest impact node will likely have the shortest backoff time, and starts to transmit first. The winner of the competition enters into the TX state while other nodes that failed the competition will enter into the IDLE state. The winner will finally go back to the IDLE state when the requested packets are sent out.

![](images/0748ca4f046a7a78c436f69ed5241c24e713377bb42dd51a0e6343d7aa5cf113.jpg)



Fig. 4: ECD state transition diagram.

It is worth mentioning that ECD reserves the benefits of pipelining. Like Deluge and MNP, ECD divides the code image into pages. A node receives the pages in the sequential order. When a node receives a page, it advertises about its available pages. When a node learns that another node has more available pages, it requests for the page and the page transmission starts. In this way, ECD does not require a node to have an entire code image to serve other nodes. Instead, whenever a node has more available pages, it can serve other nodes having fewer available pages. So as long as the transmissions at two links do not collide, different pages can be transmitted concurrently at these two links.

For example, Consider the network: A!B!C!D!E. First, when transmissions can probably collide, ECD enforces strict ordering of page transmission, i.e., a page with lower page number takes higher priority in a neighborhood. For example, when B transmits page 0 to C, A will not transmit page 1 to B after learning that a page with a lower page number is currently transmitting in the neighborhood. Second, when transmissions do not collide with each other, ECD can exploit spatial multiplexing. Suppose page 0 is propagated at D!E. As the transmissions at A!B and D!E do not collide, the transmissions at these two links can happen concurrently. So when node B learns that the source A has more available pages, it will request to node A, and the next page, page 1, will start transmission at the link A!B.

As discussed in Section II, we need to incorporate the design principles of dynamically configurable packet sizes and sender selection into our protocol design for improving the performance. In the following subsections, we will present ECD’s design details. Section III-A describes how to support variable packet sizes. Section III-B describes how to accurately estimate senders’ impacts. Section III-C describes how to prioritize the transmission of eligible senders with low overhead.

# A. Dynamically Configurable Packet Sizes

Both Deluge [11] and MNP [12] use a fixed packet size of approximately 36 bytes. Although the data packet size can be statically configured to be larger, the packet size cannot be dynamically reconfigured without re-compiling the protocol code. This is inflexible as a fixed packet size may not be appropriate for all platforms under all the conditions [4].

ECD supports dynamically configurable packet sizes. When we inject code into the base node, we inform it of the code object size and packet payload size. The base node includes these information into the ADV message. When other nodes receive the ADV message, they get notified about (i) the code object size and (ii) the data packet payload size. They will also include this information in the ADV message that they send. As a result, all nodes in the network know the code object size and the data packet payload size. With this information, nodes can decide whether the current page is sent or received.

For the sender, there is a pktsToSend vector, denoting which packets to send. For the receiver, there is a pktsToReceive vector, denoting which packets to receive. In Deluge [11] and MNP [12], the vector size is statically determined according to the page size and the packet payload size. Only when all the bits in pktsToSend are cleared, the sender finishes the current transmission and enters into the IDLE state; only when all bits in pktsToReceive are set, the receiver completes receiving and enters into the IDLE state. In ECD, we set the page size to be 1104 bytes (the same as in Deluge [11]). The page consists of 48 packets at most. As a result, the vector size consists of 6 bytes at most. Unlike Deluge and MNP which use all the bits for state transition, the sender and receiver in ECD use the first $\lceil \frac { 1 1 0 4 } { l } \rceil$ bits (where l is the dissemination payload length) to determine whether the page is sent or received.

We have also included the code object size field to reduce the overhead of transmitting the last page [21]. In Deluge [11], when the last page cannot be fully filled with useful data, it is padded with all 0s. This is inefficient when the last page cannot be fully filled. With the code object size field, we know that how many bits in the vectors can imply that the page is sent done or received done. The number of bits is d .SCM/%1104 e $\lceil \frac { ( \dot { S } + \mathsf { X } H ) ^ { q _ { o 1 1 } } 1 0 4 } { l } \rceil$ where S is the code object size and M D 256 is the metadata size (contains information about the code object).

Compared to Deluge and MNP, ECD does not require recompiling the protocol code to support configurable packet sizes. The control-plane overhead of ECD is small because the meta information (e.g., the packet payload size) is piggybacked in the ADV messages.

As discussed in Section II-A, large packets can greatly improve the efficiency for high PHY rate radios. However, large packets are more susceptible to wireless losses, sender selection for alleviating simultaneous transmissions and transmissions over poor links should be incorporated into our protocol design.

# B. Impact Estimation

As we discussed in Section II-B, MNP’s sender selection algorithm may spend too many transmissions on poor links. This should be avoided in our protocol design.

We need to estimate the number of uncovered nodes and the outbound link qualities to them.

![](images/1c5ad9c4f00d58cc76289dfacda574e0a977bbafafb3fa8f0c836652ed1f3b1c.jpg)



Fig. 5: Collision probability vs. number of hosts (N )

In order to estimate the number of uncovered nodes, we use the REQ messages sent by uncovered nodes when missing packets are detected. There are two differences between ECD’s REQ mechanism and Deluge’s REQ mechanism. First, multiple eligible senders overhear the REQ message and may be responsible for sending requested packets in REQ that is not destined for them. This enlarges the set of eligible senders so that we select the best one. Second, we note that in Deluge [11], REQ messages may be suppressed if another REQ message for the same page is overheard. This mechanism, however, will lead to biased estimation in our protocol design. For this reason, in ECD, the uncovered nodes send REQ messages unless there is an ongoing page transmission. The estimation period for sending and receiving REQ messages is carefully selected to avoid REQ collisions. As the REQ message is normally sent out within an interval in Œ16; 256/ ms (the default setting in Deluge), we set the estimation period to be $1 6 + 2 5 6 = 2 7 2$ ms.

This will not cause serious collisions, especially for high PHY rate radios. To illustrate this, we here use a simple analytical model [7]. We have $C W = 2 7 2$ because we use a milli-timer for sending REQ so that the idle slot equals to 1ms in our dissemination protocol. According to [7], the attempt probability is,

$$
P _ {e} (C W) = \frac {2}{C W + 1} \tag {2}
$$

$P _ { t } ,$ , the probability of a successful transmission in a given slot, if N hosts contend for the channel is (such an event requires a transmission attempt by a single host and the absence of all the others),

$$
P _ {t} = N P _ {e} (1 - P _ {e}) ^ {N - 1} \tag {3}
$$

The collision probability in a slot is,

$$
P _ {c} = 1 - P _ {t} - P _ {i} \tag {4}
$$

where

$$
P _ {i} = (1 - P _ {e}) ^ {N} \tag {5}
$$

is the probability of an idle slot.

We plot the collision probability vs. number of hosts in Figure 5. As the figure shows, for the CC2420 radio, the collision probability keeps below 10% even when N increases to 60.

In order to estimate the link qualities, we incorporate the LEEP link estimation protocol [25] into our design. LEEP is a passive link estimation protocol that can be invoked in proactive protocols to update neighbors’ link qualities. In ECD, we attach the LEEP header (containing a seqno) to ADV, REQ, and DATA messages. Each node uses these messages to estimate the inbound link qualities from neighboring nodes. It is worth noting that during dissemination, DATA messages are broadcasted to all neighboring nodes and can be used for inbound link estimation. This process effectively calibrates estimated link qualities via control-plane messages. Moreover, we attach the LEEP footer (containing node IDs and their inbound link qualities) to ADV messages. Therefore, the outbound link qualities can be obtained by periodically exchanging the inbound link qualities encompassed in the ADV messages.

![](images/2e8207509d7ddcca4a3f3331d483be65015719db329b03c13df07ba8988da1fc.jpg)



Fig. 6: Estimation period alignment in a neighborhood. The black node (S1) is currently transmitting a page.

Combining the requests sent by uncovered nodes and the link qualities to the requesters, we can estimate a sender’s impact. Intuitively, if a sender has more uncovered nodes with good link qualities, this node should be the next sender.

In ECD, we use .u/ as the metric to estimate the sender’s impact. .u/ considers both the number of uncovered nodes and the link qualities to them,

$$
\epsilon (u) = \sum_ {k \in U (u)} 1 \cdot p (u, k) \tag {6}
$$

where U.u/ contains u’s uncovered nodes, $p ( u , k )$ is the link quality from u to k.

Let’s look at the example shown in Figure 3. After S finishes sending one complete page, we use the metric defined above to estimate the impacts of S and N1. $\epsilon ( S ) = 1 \cdot ( 0 . 2 5 ) + 1$  $( 0 . 2 5 ) = 0 . 5 , \epsilon ( N 1 ) = 1 .$ . Therefore, we will select N1 as the next forwarder. This metric will put less weight on nodes with poor outbound link qualities, thus avoiding transmissions over these poor links.

Another challenge for impact estimation is how to align the estimation periods of different nodes within a neighborhood. To illustrate the importance, let’s look at the example shown in Figure 6. In this example, S1 is currently transmitting a page consisting of, say 20 packets. As N2 is 2 hops away, it cannot hear S1’s transmission. It thus sends an REQ message to S2, requesting the missing packets. When S2 receives the REQ message, S2 cannot start the estimation period because a page transmission is in the vicinity. If S2 starts the estimation period (because of received REQ) and then starts data transmission shortly. It would cause collisions at N3 and N4. This is different from sender selection in traditional broadcast protocols. In broadcast protocols, a single packet fully occupies the channel, so S2 will not transmit when S1 is currently transmitting (because the channel is busy). However, in code dissemination protocols, there is a large time gap between successive packets within the same page (each single packet performs backoff). Hence there is probability that S2 will transmitting the page concurrently with S1. This will introduce contention delays in the MAC layer, or even collisions at some nodes (e.g., N3 and N4).

![](images/27b35be9742b2cba7e58786e89314d1ebec0b6c2826eca2d3a7da3552a159044.jpg)



Fig. 7: CDF of packet transmission time within a page.

![](images/d14a6e7c5c986f4807c9074fd132cfcff707966245775c4eb3c2a4f98ebf50d2.jpg)



Fig. 8: Backoff timer design

To address this problem, we attach a pendingPktNum field to each data packet, indicating the number of remaining packets that the sender intends to transmit. With this information and the expected transmission time for a single packet, we can estimate the end time of the ongoing page transmission.

$$
t _ {\text { page }} = t _ {\mathrm{pkt}} \cdot \text { pendingPktNum } \tag {7}
$$

$t _ { \mathrm { p k t } }$ is the packet transmission time. Figure 7 shows the CDF of the packet transmission time under different payload length of the dissemination protocol. We can then build an empirical model to estimate the packet transmission time, $t _ { \mathrm { p k t } }$ .

# C. Transmission Prioritization

All nodes that overhear the REQ messages and have the requested page are eligible senders. From these eligible senders, we want to select the best sender. MNP selects the best sender via explicit coordination: eligible senders broadcast their impacts in the ADV messages, then the receivers request to the sender that has received the maximum number of distinct requests. This method introduces high overheads. The receivers must send multiple requests to for receiving the missing packets. Some requests are merely for impact estimation while some other requests will be followed by useful data transmissions.

We employ an impact-based backoff mechanism. Assume N is the maximum number of eligible senders. The maximum contention period is $C W _ { \mathrm { c o n t e n t i o n } } .$ . Generally, the larger the impact of node u, the shorter $u ^ { \prime } \mathbf { s }$ backoff time. As depicted in Figure 8, the backoff time of u is,

$$
t _ {\text { backoff }} (u) = (N - \epsilon (u)) \Delta + X \tag {8}
$$

where X is a random period of time generated from $[ 0 , C W _ { X } )$ , and  D C Wcontention $\begin{array} { r } { \Delta = \frac { C W _ { \mathrm { c o n t e n t i o n } } - C ^ { \mathbf { \dot { W } } _ { X } } } { N } } \end{array}$

With this backoff time design, the largest impact node is most likely to transmit first. Other nodes will cancel the data transmission and enter into the IDLE state.

Different choices of $C W _ { \mathrm { c o n t e n t i o n } }$ and $C W _ { X }$ have different impacts. Usually, we need a relatively short contention period for fast propagation. However, if the contention period is too small, we may not effectively differentiate transmissions of different priorities. There is also a tradeoff in determining $C W _ { X } . \operatorname { I f } C W _ { X }$ is large, there is possibility that the best sender loses the competition. If $C W _ { X }$ is small, we may not effectively randomize the transmissions from senders that have the same impact.

We empirically set $C W _ { \mathrm { c o n t e n t i o n } } = 2 5 6 \mathrm { m s }$ and $C W _ { X } =$ 50ms. This strikes a reasonable balance between the tradeoffs discussed above. Additionally, we devise specific mechanisms to avoid priority inversion and concurrent transmissions from senders that have the same impact.

In order to avoid priority inversion (i.e., a lower impact node is transmitting instead of the largest impact one), we attach the impact field into each data packet. Suppose a lower impact node is currently transmitting, the large impact node will start contending with the node. When the lower impact node hears that a larger impact node is transmitting, it will finally enter into the IDLE state. If both impacts are the same, we use the node ID to break the tie.

In order to alleviate concurrent transmissions from senders of the same impact, the collisions, we should restrict the number of eligible senders when there is little diversity in their impacts. When there is very few REQ messages in the neighborhood, it is likely that most of the nodes have already receive the current page. In this case, we only allow the senders that the REQ message is destined to be eligible senders.

The sender selection scheme, while reduces contention and collisions, it does not prevent them in case of hidden terminals. Mechanisms to mitigate hidden terminals may introduce additional overhead that outweigh the achieved benefits, as demonstrated in [12]. We provide an option to mitigate the impact of hidden terminals: nodes that experience collisions can send a “shut down” message to prohibit interfering nodes from transmitting simultaneously.

# IV. Evaluation

We implement ECD based on TinyOS/TelosB platform in nesC. We have also ported the code to TOSSIM 1.x/Mica2 to investigate the sender selection behaviors of ECD and MNP. This is because MNP is implemented for TinyOS 1.x/Mica2/TOSSIM 1.x.

We use Deluge [11] and MNP [12] for performance comparisons. We use two primary metrics—completion time and data traffic to evaluate the protocols.

![](images/59fda1ea7c400d128839c3f9b61bf7a4b0d19549ea03a8924f5570a95390dcd0.jpg)



(a) Testbed topology

![](images/d2cc017b3816e7ad5f955e63555ec6201dceb39751877798b783c927af6a74b0.jpg)



(b) CDF of link qualities

![](images/f25986b4e28935dc12975fe56218179cf2be93409b6fc09004de4ef6212f0421.jpg)



(c) Impact of packet sizes

![](images/1b26b8a67fb7511fd9504ab71602c800a1d6019302855249756753ed251be273.jpg)



(d) CDF of node completion times

![](images/2f95f2281c0aae3f3531a3a12ee69107ab6ec1c5163ec2648f30f0e953c01d60.jpg)



(e) Impact of sender selection

![](images/73de3c45cf5d471f4d63fbcabd71b26e03e93065924ce613b31ff9d17386c1a9.jpg)



(f) CDF of inter-packet arrival times

Fig. 10: Testbed results.   
![](images/dcb235be437835e1abc3b67338966cee9d4c9967f68452595619ace211349a2c.jpg)



Fig. 9: Testbed

# A. Methodology

We evaluate the performance of ECD and Deluge on a 25- node TelosB testbed (as shown in Figure 9).

To simulate the multihop behavior, we set the CC2420 power to -32.5 dbm. The topology used for evaluation is a 5x5 grid where the base node is located at the bottom left corner. We use Deluge’s default configurations (e.g., 23 bytes protocol payload, 48 packets per page). The page size of ECD is 1104 bytes (the same as in Deluge). We inject a program consisting of 10 pages (i.e., approximately 10KB). Each experiment is conducted five times.

To get the performance metrics, we have written a statistic reporting component and a sniffer component. The statistic reporting component is wired to each of the 25 nodes. With this component, the base node broadcasts time synchronization beacons at the maximum power to synchronize all the other nodes. All the other nodes locally record their transmitted data packets and completion time (synchronized to the base node). After the experiments, all the nodes (including the base node) broadcast their statistics at the maximum power. The sniffer component is installed to a separate node. The sniffer node is then used to gather all the performance statistics.

For the simulation, we mainly investigate the sender selection behaviors of ECD and MNP. TOSSIM 1.x simulates for Mica2 platform. We use the LossyBuilder provided in TinyOS 1.x to generate an nss file containing pair-wise link qualities. The topology is a 5x5 grid with 5 feet inter-node spacing. We inject a 2-page code object. The page size is set to 48 packets per page, and the packet payload size is set to 23 bytes in order to speedup the simulation process.

# B. Testbed Experiments

Figure 10(a) gives the network topology we have conducted the experiment. The red star denotes the location of the base node. All other nodes are denoted by circles (there is a link from the base node to this node) or crosses (there is no link from the base node to this node). The radius of the circle represents the quality of link. For example, link quality of 0!5 is 100% while link 0!2 is only 25%. We place the sniffer node near node 12 to overhear radio transmission activities in the vicinity.

Before we conduct the experiment, we first measure the link quality of each node pair. Figure 10(b) gives the CDF of link qualities. We can see that 36% links are good with link quality >90%, 20% links are intermediate with link quality varied between 10%–90%. Additionally, 44% of the links are poor (with link quality <10%) or disconnected, which represents a proper multihop setting.

Figure 10(c) shows the impacts of different protocol payload sizes without sender selection. For data packets, we can see that large packets effectively reduces the transmitted packet number. It is obvious as for large packets, fewer number of packets constitute the entire code object. For the completion time, however, using the largest packets (92 bytes payload) does not lead to the best performance. This is because large packets are more susceptible to wireless losses. With ECD, we can dynamically configure the packet payload length. For example, using packet payload length of 69 bytes can shorten the completion time by 29.2%, compare to Deluge. The performance degradation at 92 payload length illustrates that we should incorporate sender selection into our protocol design in order to alleviate transmission collisions and transmissions over poor links, which causes larger negative impacts to large packets.

![](images/f414750c80a54a15eda86f5a23c7bbc3efaf6c64665de97971fb7a548fe94619.jpg)



(a) ECD

![](images/130643641933a5257c104d25162c8d3aaf993b17bb817057c87b7c69f38efb41.jpg)



(b) MNP   
Fig. 11: Sender selection behaviors of ECD and MNP.

Figure 10(d) shows impacts of sender selection on completion time for large packets (i.e., 92 bytes payload length). With sender selection, ECD can shorten the completion time from 58s to 47s, a 19% reduction. We also observe that, with sender selection, more number of nodes complete receiving the code object earlier. This is because our impact metric favors senders that cover more number of uncovered node with good link qualities. High PRR receivers can complete the code object earlier in time. For example, at time 20s, there are 6 completed nodes with sender selection while there is only 1 completed node without sender selection.

Figure 10(e) shows the impacts of sender selection on data packets. At 23 bytes packet payload, ECD with sender selection can reduce the data packet by 22.8%. At 92 bytes packet payload, ECD with sender selection can reduce the data packet by 20%.

To get further insights why sender selection improved the performance, Figure 10(f) compares the inter-packet arrival time for a consecutive of packets within a page observed on the sniffer node. We can see that without sender selection, the inter-packet arrival time is about 25ms. With sender selection, the inter-packet arrival time can be reduced to about 21ms. This is because there will be more contentions and collisions in protocols without sender selection. Considering that the expected congestion backoff time is 1.25ms under TinyOS CSMA MAC, it means that sender selection reduces 3-4 times collisions for each packet transmission.

# C. TOSSIM Simulation

Figure 11 depicts the packet transmission activities of ECD and MNP in TOSSIM. The red cross denotes data transmissions while the green cross denotes the REQ message. To better understand ECD’s sender selection behaviors, we have also depicted the time instant when the estimation period ends and the contention period starts (denoted by the blue cross).

Overall, ECD completes the dissemination in 33.66s (the time interval between the first data transmission and last data transmission) while MNP completes the dissemination in 74.5s. ECD outperforms MNP mainly because it employs a fast sender selection algorithm which effectively shortens the inter-page negotiation time, resulting in shorter completion time.

In terms of data packets, ECD disseminates 291 data packets while MNP disseminates 422 data packets. We were quite surprised at MNP’s poor performance. From the figure, we can see that MNP cannot effectively avoid concurrent transmissions. For example, at time 5s–10s, nodes 18, 5 concurrently transmit; at time 24s–26s, nodes 14, 15 concurrently transmit. Further investigation of the runtime trace reveals that the link qualities affect the performance. We find that link 18!5 and 15!14 are both poor. So when node 18 and 15 starts transmissions, nodes 5 and 14 may not be aware of the ongoing transmission because the explicit coordination message (START\_DOWNLOAD) may be lost. Nodes 5 and

14 start transmissions later, overlapping with nodes 18 and 15’s transmission. ECD avoids concurrent transmission by attaching each data packet an impact field. Hence, when a lower impact node finds a higher impact node is transmitting (by overhearing the DATA message), it will go back to the IDLE state. This mechanism effectively alleviates concurrent transmissions, resulting in fewer data packets.

In terms of REQ packets, ECD transmits 148 REQs while MNP transmits 208 REQs. ECD transmits fewer REQ message because of its sender selection mechanism. MNP needs multiple rounds of message exchanges—some REQs are merely for impact estimation while other REQs are followed by useful data transmissions. ECD makes more efficient use of the REQs. In the estimation period, nodes not only estimate their impacts but also learn from REQs which packets to transmit in the next phase.

From Figure 11(a), we can also investigate the detailed behavior of ECD and better understand its design principles.

At time 16s, after node 0 finishes one round of transmission, node 8 starts transmission. We can see that at this instant, nodes 0, 5, 8, 11, 18 receive the page, and start the contention period at 17s. Intuitively, nodes 8 and 18 (see Figure 10(a) for the topology) will be better choices than other nodes because they cover more uncovered nodes. This reflects the accuracy of our sender selection algorithm.

Also note that how we align the estimation period of different nodes in a neighborhood. We notice that node 13 sends REQ during node 8’s page transmission (possibly because link 8!13 is not good). If nodes in the vicinity, say nodes 5, 11, start transmission, they will overlap with node 8’s transmission. So we should ignore the REQ and start the estimation period later, only when node 8’s page transmission ends. In order to do so, we must accurately predict the end time of node 8’s page transmission (see the last several paragraphs of Section III-B). In this sense, node 8’s page transmission synchronizes the estimation period in its neighborhood.

We can also see that ECD’s transmission prioritization mechanism effectively reduces transmission collisions. From many eligible senders (represented by blue crosses), we select the best sender most of the time. There do exist some concurrent transmissions of small length, especially when there is little diversity (i.e., there are few REQs, so impacts of eligible senders are roughly the same). This illustrates that mechanisms to reduce the candidate set when there is little diversity is important. To this end, we restrict the candidate set to only include nodes that the REQs are destined to (see the last paragraph of Section III-C).

# V. Related Work

Code dissemination protocols in WSNs can be divided into two categories: (i) structure-less protocols and (ii) structurebased protocols. For structure-less protocols, Deluge [11] is perhaps the most popular code dissemination protocol used for reliable code updates. It uses a three-way handshake and NACK-based protocol for reliability, and employs segmentation (into pages) and pipelining for spatial multiplexing. MNP [12] provides a detailed sender selection algorithm to choose a local source of the code which can satisfy the maximum number of nodes. Our work is based on the principles of structure-less protocols and has two main differences. First, we enable dynamically configurable packet sizes to support large packets to improve the dissemination performance. Second, we employ an accurate and fast sender selection algorithm to alleviate concurrent transmissions and transmissions over poor links. For structure-based protocols, Sprinkler [18] uses the localization service at each node to construct a connected dominating set (CDS). It uses TDMA to schedule packet transmissions among the CDS nodes to reduce energy consumption by minimizing packet transmissions. CORD [10] is a more recent work. It employs a two phase approach in which the object is delivered to a subset of nodes in the network that form a connected dominating set in the first phase, and to the remaining nodes in the second phase. Our design does not rely on the underlying network structure. Therefore it does not incur the overhead of backbone construction and is more suited to dynamic scenarios.

Recently, several coding-based dissemination protocols specifically designed for WSNs are proposed to address the deficiency of Deluge in sparse and lossy networks, such as Rateless Deluge [6], SYNAPSE [19], AdapCode [8], and ReXOR [2]. They all use network coding to encode a packet before transmission. After receiving an expected number of encoded packets, the receiving node uses Gaussian elimination to decode the packets. The difference is that Rateless Deluge [6] uses Random Linear Codes; SYNAPSE [19] uses Fountain Codes; AdapCode [8] also uses linear codes, but the coding scheme is adaptively changed according to the link quality. ReXOR [2] employs a lightweight XOR encoding scheme and an adaptive interpage waiting design to achieve good performance in both dense and sparse networks. These works are orthogonal to this work and the technique of network coding can be adopted into ECD’s design to further improve the performance.

The data transmission rate in WSNs is generally considered low. However, this does not hold true for code dissemination: in the network reprogramming process, nodes need to disseminate a large code object as soon as possible. Hence, improving channel utilization is highly favored. While there are many effective approaches to improve channel utilization, including MIMO, rate adaptation [23], [27], they are not readily available for commonly used sensor nodes. Therefore, we propose adapting the packet size to improve the channel utilization, especially for high PHY rate radios. Dynamically adapting packet sizes has been investigated in [4], [22], [26], but they have not practically applied to the broadcast/dissemination scenario. The design in our work does not aim to derive an optimal packet size. Rather, it aims to support dynamically configurable packet sizes, so that system designers can configure the packet payload size for improved performance, e.g., according to network models [3], [26] or experimental observations.

There is also a rich literature in sender selection in general broadcast protocols. Sender selection is effective in mitigating the broadcast storm problem in wireless networks [20]. A number of approaches have been proposed to select the next forwarder [16], [24], [29]. In DCB [16], nodes maintain 2- hop neighbor information. When a sender broadcasts a packet, it selects the next forwarders in such a way that (i) 2-hop neighbors are covered and (ii) 1-hop non-forwarders need to be covered by at least two forwarders. In RBP [24], every node rebroadcasts the packet for the first time. Then each node adjusts the number of retries based on the neighborhood density. CF [29] is a recent work that exploits spatial link correlation to mitigate ACK overhead. ECD differs from these works in three main aspects. First, these protocols are not required to be 100% reliable. Second, in broadcast protocols, packet size is mainly determined by the application programs rather than underlying mechanisms which may incur delays. Third, in ECD, packets within a page are transmitted in a succession, hence we need a special design to align the estimation period, avoid priority inversions, and alleviate collisions (as discussed in Sections III-B and III-C).

# VI. Conclusion

In this paper, we present ECD, an Efficient Code Dissemination protocol for wireless sensor networks. Compared to prior works, ECD has three salient features. First, it supports dynamically configurable packet sizes. By increasing the packet size for high PHY rate radios, it significantly improves the transmission efficiency. Second, it employs an accurate sender selection algorithm to mitigate transmission collisions and transmissions over poor links. Third, it employs a simple impact-based backoff timer design to shorten the time spent in coordinating multiple eligible senders so that the largest impact sender is most likely to transmit. We implement ECD based on TinyOS and evaluate its performance extensively. Results show that ECD outperforms state-of-the-art protocols, Deluge and MNP, in terms of completion time and data traffic.

Future work leads to two directions. First, we would like to incorporate effective sleep scheduling algorithm into our design. Second, we would like to examine effectiveness of our design in large-scale WSN systems.

# Acknowledgements

This work was supported by the National Science Foundation of China (Grant No. 61070155), the Program for New Century Excellent Talents in University (NCET-09-0685), and in part by NSERC Discovery Grant 341823-07, NSERC Strategic Grant STPGP 364910-08, and FQRNT Grant 2010- NC-131844.

# References

[1] I. F. Akyildiz, W. Su, Y. Sankarasubramaniam, and E. Cayirci, “Wireless sensor networks: A survey,” Computer Networks, vol. 38, pp. 393– 422, 2002.   
[2] W. Dong, C. Chen, X. Liu, J. Bu, and Y. Gao, “A Lightweight and Density-Aware Reprogramming Protocol for Wireless Sensor Networks,” IEEE Transactions on Mobile Computing, vol. 10, no. 10, pp. 1403–1415, 2011.   
[3] W. Dong, C. Chen, X. Liu, J. Bu, and Y. Liu, “Performance of Bulk Data Dissemination in Wireless Sensor Networks,” in Proc. of DCOSS, 2009.   
[4] W. Dong, X. Liu, C. Chen, Y. He, G. Chen, Y. Liu, and J. Bu, “DPLC: Dynamic Packet Length Control in Wireless Sensor Networks,” in Proc. of IEEE INFOCOM, 2010.

[5] W. Dong, Y. Liu, X. Wu, L. Gu, and C. Chen, “Elon: Enabling Efficient and Long-Term Reprogramming for Wireless Sensor Networks,” in Proc. of ACM SIGMETRICS, 2010.   
[6] A. Hagedorn, D. Starobinski, and A. Trachtenberg, “Rateless Deluge: Over-the-Air Programming of Wireless Sensor Networks using Random Linear Codes,” in Proc. of ACM/IEEE IPSN, 2008.   
[7] M. Heusse, F. Rousseau, R. Cuillier, and A. Duda, “Idle Sense: An Optimal Access Method for High Throughput and Fairness in Rate Diverse Wireless LANs,” in Proc. of ACM SIGCOMM, 2005.   
[8] I.-H. Hou, Y.-E. Tsai, T. F. Abdelzaher, and I. Gupta, “AdapCode: Adaptive Network Coding for Code Updates in Wireless Sensor Networks,” in Proc. of IEEE INFOCOM, 2008.   
[9] J. Huang, G. Xing, G. Zhou, and R. Zhou, “Beyond Co-existence: Exploiting WiFi White Space for ZigBee Performance Assurance,” in Proceedings of IEEE ICNP, 2010.   
[10] L. Huang and S. Setia, “CORD: Energy-efficient Reliable Bulk Data Dissemination in Sensor Networks,” in Proc. of IEEE INFOCOM, 2008.   
[11] J. W. Hui and D. Culler, “The dynamic behavior of a data dissemination protocol for network programming at scale,” in Proc. of ACM SenSys, 2004.   
[12] S. Kulkarni and L. Wang, “Energy-efficient multihop reprogramming for sensor networks,” ACM Transactions on Sensor Networks, vol. 5(2), 2009.   
[13] P. Lettierri and M. B. Srivastava, “Adaptive Frame Length Control for Improving Wireless Link Throughput, Range, and Energy Efficiency,” in Proceedings of IEEE INFOCOM, 1998.   
[14] P. Levis, N. Lee, M. Welsh, and D. Culler, “TOSSIM: Accurate and Scalable Simulation of Entire TinyOS Applications,” in Proc. of ACM SenSys, 2003.   
[15] P. Levis, N. Patel, D. Culler, and S. Shenker, “Trickle: A Self-Regulating Algorithm for Code Propagation and Maintenance in Wireless Sensor Networks,” in Proc. of USENIX NSDI, 2004.   
[16] W. Lou and J. Wu, “Towards broadcast reliability in mobile ad hoc networks with double coverage,” IEEE Trans on Mobile Computing, vol. 6, pp. 148–163, 2007.   
[17] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X.-Y. Li, and G. Dai, “Canopy Closure Estimates with GreenOrbs: Sustainable Sensing in the Forest,” in Proc. of ACM SenSys, 2009.   
[18] V. Naik, A. Arora, P. Sinha, and H. Zhang, “Sprinkler: A Reliable and Energy Efficient Data Dissemination Service for Wireless Embedded Devices,” in Proc. of IEEE RTSS, 2005.   
[19] L. M. Ni, Y. Liu, and Y. Zhu, “SYNAPSE++: Code Dissemination in Wireless Sensor Networks Using Fountain Codes,” IEEE Trans on Mobile Computing, vol. 9, pp. 1749–1765, 2010.   
[20] S.-Y. Ni, Y.-C. Tseng, Y.-S. Chen, and J.-P. Sheu, “The Broadcast Storm Problem in a Mobile Ad Hoc Networks,” in Proc. of ACM MobiCom, 1999.   
[21] R. K. Panta, S. Bagchi, and S. P. Midkiff, “Efficient Incremental Code Update for Sensor Networks,” ACM Trans on Sensor Networks, vol. 7, no. 6, pp. 1–32, 2011.   
[22] Y. Sankarasubramaniam, I. F. Akyildiz, and S. W. Mclaughlin, “Energy Efficiency based Packet Size Optimization in Wireless Sensor Networks,” in Proc. of IEEE Internal Workshop on Sensor Network Protocols and Applications, 2003.   
[23] S. Sen, N. Santhapuri, R. R. Choudhury, and S. Nelakuditi, “AccuRate: Constellation based rate estimation in wireless networks,” in Proc. of USENIX NSDI, 2010.   
[24] F. Stann, J. Heidemann, R. Shroff, and M. Z. Murtaza, “RBP: Robust Broadcast Propagation in Wireless Networks,” in Proc. of ACM SenSys, 2006.   
[25] TinyOS TEP 124: The Link Estimation Exchange Protocol (LEEP). [Online]. Available: http://www.tinyos.net/tinyos-2.x/doc/html/tep124.html   
[26] M. C. Vuran and I. F. Akyildiz, “Cross-layer Packet Size Optimization for Wireless Terrestrial, Underwater, and Underground Sensor Networks,” in Proc. of IEEE INFOCOM, 2008.   
[27] M. Vutukuru, H. Balakrishnan, and K. Jamieson, “Cross-layer wireless bit rate adaptation,” in Proc. of ACM SIGCOMM, 2009.   
[28] Q. Wang, Y. Zhu, and L. Cheng, “Reprogramming wireless sensor networks: Challenges and approaches,” IEEE Network Magazine, vol. 20(3), pp. 48–55, 2006.   
[29] T. Zhu, Z. Zhong, T. He, and Z.-L. Zhang, “Exploiting Link Correlation for Efficient Flooding in Wireless Sensor Networks,” in Proc. of USENIX NSDI, 2010.