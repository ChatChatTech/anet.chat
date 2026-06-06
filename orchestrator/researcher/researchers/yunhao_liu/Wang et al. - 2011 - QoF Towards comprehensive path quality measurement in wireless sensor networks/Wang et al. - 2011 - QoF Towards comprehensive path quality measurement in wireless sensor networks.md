# QoF: Towards Comprehensive Path Quality Measurement in Wireless Sensor Networks

Jiliang Wang∗, Yunhao Liu∗†, Mo Li‡, Wei Dong∗§, Yuan He∗† ∗CSE Department, The Hong Kong University of Science and Technology †TNLIST, School of Software, Tsinghua University ‡School of Computer Engineering, Nanyang Technological University §College of Computer Science, Zhejiang University {aliang, liu, dongw, heyuan}@cse.ust.hk, limo@ntu.edu.sg

Abstract—Due to its large scale and constrained communication radius, a wireless sensor network mostly relies on multi-hop transmissions to deliver a data packet along a sequence of nodes. It is of essential importance to measure the forwarding quality of multi-hop paths and such information shall be utilized in designing efficient routing strategies. Existing metrics like ETX, ETF mainly focus on quantifying the link performance in between the nodes while overlooking the forwarding capabilities inside the sensor nodes. The experience on manipulating GreenOrbs, a large-scale sensor network with 330 nodes, reveals that the quality of forwarding inside each sensor node is at least an equally important factor that contributes to the path quality in data delivery. In this paper we propose QoF, Quality of Forwarding, a new metric which explores the performance in the gray zone inside a node left unattended in previous studies. By combining the QoF measurements within a node and over a link, we are able to comprehensively measure the intact path quality in designing efficient multi-hop routing protocols. We implement QoF and build a modified Collection Tree Protocol (CTP). We evaluate the data collection performance in a test-bed consisting of 50 TelosB nodes, and compare it with the original CTP protocol. The experimental results show that our approach takes both transmission cost and forwarding reliability into consideration, thus achieving a high throughput for data collection.

# I. INTRODUCTION

A wireless sensor network (WSN) is typically designed to span in a large field for data collection. Data delivery is usually achieved with multi-hop transmission along a sequence of nodes. Many multi-hop routing protocols have been proposed for WSN data collection and they usually incorporate special path estimation metrics to select “good” paths for delivering data packets.

There are many estimation metrics proposed to measure the forwarding quality of a multi-hop path, such as ETX [1], ETF [2], PRR, ETOP [3] and etc. Existing metrics mainly focus on estimating the packet delivery quality on links in between the nodes. The quality of forwarding capacity along a path is estimated by the aggregate of the forwarding qualities of all the links on the path. Those link-based metrics while reflect the link performance of the path, however, overlook the forwarding capabilities inside the sensor nodes, thus resulting in an incomplete measurement of the path quality. Using the incomplete path indicators will lead to suboptimal routing decisions and degraded routing performance.

Such an effect has been revealed in our experience in manipulating GreenOrbs [4], a large-scale sensor network with 330 nodes. In current routing implementation in GreenOrbs, we use a modified Collection Tree Protocol (CTP) that relies on path ETX estimation for routing selection. During the field test of the system, we observe a portion of packet drops on some nodes. They are due to a variety of causes, such as forwarding queue overflow under high traffic pressure, software bugs in the CTP implementation, and etc. Those nodes, however, still respond with ACKs at the radio hardware. The bad fact is that with current path indicators the inability of packet forwarding within the individual nodes cannot be shared among the network, yet there does not exist a metric to quantify the packet forwarding quality at each node. As a result, the path estimation does not always truly reflect the path quality and the data delivery performance is severely degraded.

The packet drops on the problematic nodes introduce intrinsic unreliability in data delivery. As a matter of fact, even a single link itself can hardly achieve full reliability. ETX over a link measures the expected number of transmissions for successfully delivering a packet, but transmitting the packet at the expected number of times does not guarantee it will be successfully received at the receiver end. In practical systems, a maximum number of retransmissions are usually set on a link to prevent sending a packet on a “bad” link too many times, which exhausts the finite communication resources. The packet will be eventually dropped by the sender after a maximum number of transmission retries. The network is thus rendered unreliable due to both node unreliability and link unreliability. ETX of a path is estimated as the summation of ETX values over all links constituting the path. Using path-ETX for path selection minimizes the transmission cost and achieves a high throughput. However, ETX presumes that end-to-end delivery is reliable which, however, is not always the truth as we see from the above.

For data delivery within a network of inherent unreliability, a metric that better measures the data productivity is the amount of successful data delivery to the destination, i.e., data yield [5]. Data yield over the actual number of data transmissions, measures both transmission cost as well as achieved throughput. Existing path-ETX does not capture such a parameter. Consider a simplified example depicted in

![](images/b1ade97f5911688034866fa91a2f0a6f8422731f43832091062cf807ec4e0158.jpg)



Fig. 1: Two paths with the same ETX but different PRRs.

Fig. 1. There are two paths, both of which have path-ETX of 20. Suppose the link layer transmission retries is set to 1. In path 1, the probability that a packet passes the first link is $\textstyle { \frac { 1 } { 1 0 } } + ( 1 - { \frac { \bar { 1 } } { 1 0 } } ) \cdot { \frac { 1 } { 1 0 } } = 0 . 1 9$ . Similarly, the probability that a packet passes the second link is 0.19. Therefore, the probability that the packet passes the path (path reliability) is $0 . 1 9 \times 0 . 1 9 = 0 . 0 3 6 1$ , i.e., 361 packets will be received if the source sends 10000 packets. In path 2, however, the path reliability is $\textstyle 1 \times ( { \frac { 1 } { 1 9 } } + { \bar { ( } } 1 - { \frac { 1 } { 1 9 } } ) \cdot { \frac { 1 } { 1 9 } } ) = 0 . 1 0 2 5 ,$ , i.e., 1025 packets will be received if the source sends 10000 packets. This implies that ETX fails to capture the path reliability [6]. The situation is similar if we further consider a higher number of transmission retries as well as node unreliability. Routing based on path-ETX does not give the optimal delivery path in terms of the data yield per transmission.

In this work, we comprehensively investigate the unreliability in both links and nodes. We present QoF, a new metric which estimates the chances for a packet to pass both a link and a node. The link-QoF not only considers the transmission cost at the sender but also considers the data delivery ratio at the receiver. The node-QoF estimates the quality of forwarding within a node, and it plays an important role in differentiating the problematic nodes. Based on link-QoF/node-QoF, we aggregate the QoF measure over a path (path-QoF). The path-QoF metric estimates the intact path forwarding quality and it considers both transmission cost and end-to-end data delivery ratio. The QoF metric measures the data yield over the actual number of data transmissions. Hence using such a metric can greatly improve the data yield while having a low transmission overhead.

The contributions of this paper are summarized as follows.

First, we reveal the limitations of existing link-based indicators like ETX and ETF in estimating the intact path forwarding quality. In a practical system, routing selection based on ETX may lead to severely degraded data yield.

Second, we propose a new metric QoF to measure the path quality. QoF can be used to estimate the forwarding quality over a link or within a node. Using QoF, we are able to characterize both the transmission cost and the data delivery ratio along a forwarding path.

Third, we implement QoF based on TinyOS 2.1 [7] and incorporate it into CTP [8]. We evaluate the QoF based routing performance in a test-bed consisting of 50 TelosB nodes [9]. The results show that using the QoF metric improves the data yield while reducing the per-successful delivery cost.

The rest of this paper is organized as follows. Section II presents the related work. In Section III, we introduce our basic observations in a real working system that motivate this study. In Section IV, we present the detailed design aspects. In Section V, we show the implementation and evaluation results. We conclude this work in Section VI.

# II. RELATED WORK

The quality of packet forwarding is a fundamental factor in wireless sensor networks, which has been studied in a number of works. Such a factor can be estimated on different dimensions over the communication in between nodes, e.g., received signal strength (RSS), transmission delay, packet reception ratio (PRR), and etc. Those parameters are measured at different layers across the communication stacks.

At the physical layer, RSSI and LQI are two most widely used parameters that describe the communicational quality between nodes. Both RSSI and LQI reflect the physical quality of the wireless channel in between the nodes, though as suggested in [10], the two parameters are not adequate to represent the quality of packet forwarding over the link.

At the link layer, many other metrics have been proposed. ETX measures the expected number of transmissions for successfully delivering a packet over the link. Specifically, if we denote $d _ { f }$ as the probability that a packet is successfully received and $d _ { r }$ as the reverse probability that the link ACK can be successfully received. The ETX value over a link is then calculated as $\frac { 1 } { d _ { f } { \times } d _ { r } }$ . Another metric ETF [2] is designed for links of high asymmetry. ETF suggests that though the reverse link quality is low, the ACK still has a high probability being received by the sender. ETOP [3] considers the impact of link positions to the path quality. It presents an algorithm to find the path with minimal ETOP value. Designed for wireless mesh networks, ETOP does not consider the unreliable forwarding quality of sensor nodes. In addition, it requires that the source determines the entire forwarding path to the destination, which is not suitable for the WSNs with unreliable and time-varying links. There are some other link layer metrics, such as ETT (Expected Transmission Time), competence [11], L-NT [12], ENT [13], end-to-end success rate (SR) [14], required number of packets [15], EDR [16], and etc. Among the aforementioned link estimation metrics, ETX is the most widely used one. ETX has worked as the de facto link quality indicator and has been used for a variety of wireless protocols [17] [18]. Currently, ETX estimation has been integrated into CTP [8], for reliable and efficient data collection in WSNs.

Besides those estimators at separate layers, the 4-bit link estimator uses 4 bits to combine information at PHY layer, link layer and network layer. After using PHY signal strength to do the first step link filtering, it also considers link layer packet reception quality and network layer congestion information.

There are different metrics proposed to characterize the forwarding quality of a path. Minimal hop count can be used to select a path. Summing up all link ETX values along the path gives the path-ETX. As we found in our test-bed, however, the path-ETX is not always adequate in practical systems because it only gives an incomplete description of the path quality.

![](images/78dd547a5b3ee39e8503896ab0b460b6e8c5be894fe202ed537b43fa754910f4.jpg)



![](images/3ad55286f3955b9be61d1a66f7d4123863e28ac5cc25eb43d9e84956f5bd11ee.jpg)



Fig. 2: Observation from a 330-node outdoor test-bed. (a) Network yield at different scales. (b) Packet loss on different nodes.

Other metrics [13] [19] [12] overlook the node forwarding quality as well. Simply aggregating the estimated link qualities does not give comprehensive description of the intact path quality.

There are many works focusing on node’s capability and stability. For example, Schmid et al. [20] investigate the relation between the timer stability and the power and other environment factors such as temperature, humidity, the cut of the oscillator, and etc. For an event driven embedded OS, such as TinyOS, a large portion of events are driven by timers. The timer instability largely renders the OS instable.

Queue length is another important factor that affects the forwarding quality of individual nodes. Backpressure routing uses local queue length information to select a node with the largest positive differential backlog. It is designed to be throughput optimal. BCP [21] is a recent realization of backpressure routing protocol for sensor networks. There are also a lot of other works for congestion control such as [22], [23]. While those approaches are effective in handling network congestions, they do not consider other causes affecting the node forwarding quality. As we found in GreenOrbs, there are various causes affecting the node forwarding quality. Our work not only considers packet loss due to congestion but also considers packet loss due to other factors inside the node.

# III. MOTIVATION AND BACKGROUND

This work is mainly motivated from the experience in manipulating a real-world system, GreenOrbs, deployed in the wild. During the experiment, we observe substantial packet loss on a number of nodes that cannot be characterized by existing path estimation metrics. We first give a brief description on the system architecture of GreenOrbs. We then present our basic observations on packet loss, which reveals the gray zone of packet drops within the sensor node. We take a close look at the packet losses with the work flow of the packet forwarding in the software implementation on a sensor node.

# A. GreenOrbs System

GreenOrbs is a sensor network system for supporting a variety of forestry applications, such as canopy closure estimates, fire risk evaluation, microclimate monitoring, and carbon dioxide measurement. The latest deployment of GreenOrbs system consists of 330 nodes in the woodland. It has been in operation since December 2009.

![](images/714dd4ffeb9f71d6193fb024c1505eadc53c2573feb2d42b776e1e2c6ed3940f.jpg)



Fig. 3: Component graph of GreenOrbs implementation.

GreenOrbs uses the TelosB mote with MSP430 processor and CC2420 transceiver. We develop the program based on TinyOS 2.1. Currently, GreenOrbs operates with a low power listening mechanism and employs CTP [8] for data collection. A maximum of 30 retransmissions are provided to improve link layer reliability. In order to record the behaviors and performance of packet forwarding within a sensor node at a fine granularity, we modified the CTP component, recording all related events as well as some statistical information. Fig. 3 shows the component graph of the GreenOrbs system.

# B. Basic Observations

In this section, we present the outdoor test-bed results over 330 nodes that motivate our work. As used in [5], we use network yield to measure the quality of data collection of the network. The network yield measures the quantity of data received at the sink with respect to the total data generated by all nodes in the network. The network yield can be calculated by

$$
\text { yield } = \frac {\# \text { of   data   pkts   received   at   the   sink   during } w}{\# \text { of   data   pkts   sent   by   all   nodes   during } w}
$$

The network yield gives us the goodput of the network, reflecting both forwarding reliability and the throughput.

During the measurement, we vary the network size. The network yield for different network sizes is shown in Fig. 2 (a). We see from the statistics that there are about 22 40% of data lost in the multi-hop data collection when the network scales from 100 to 330. We further look into the lost packets. The packet loss on different nodes is shown in Fig. 2 (b). We find that packet loss is quite common and a small portion of nodes experience excessively high packet losses. The packet loss here is mainly due to two reasons. The first reason is transmission timeout on the links (exceeding the retransmission threshold); and the second reason is local packet drops within the node which are mainly due to receive/transmit queue overflow, memory corruption, routing loops, packet duplication, and program bugs (e.g., race conditions) and etc. We will take a closer look at the causes of packet loss at individual sensor nodes.

![](images/31f5ba7698c9cf7787569646c3c64effb485d1f596b081257c81759bb4cd3d9c.jpg)



Fig. 5: Different causes of packet loss on sensor nodes.

# C. Anatomy of Packet Loss

1) Packet loss within a node: To understand the causes of packet loss, we take a close look into the work flow on a node that forwards a packet. As depicted in Fig. 4, the flow starts with the node perceiving the physical wave that carries the packet from the sender. It ends when the node gets an ACK from the next-hop receiver or the number of retransmissions reaches the limit.

We can see from Fig. 4 that there exists a gray zone in the work flow, spanning across the network, and application layers. Existing path estimators often measure the forwarding quality of packets outside the gray zone. The packet is presumed passing through the gray zone 100% successful. According to aforementioned observations, however, there is a probability for a packet to get lost when it is processed in the gray zone. Though CTP uses software ACK and beacon message to measure link quality, it cannot effectively capture the gray zone and its impact to the entire path.

We conduct experiments on a 50-node test-bed. In Fig. 5, we summarize the occurrence of several causes that lead to packet drops. The receiver queue overflow is due to the resource constraint on sensor nodes. The packets duplicate suppression is due to the fact that routing layer information is not timely updated. Task failure is caused by the OS mechanism that does not allow the same task to be posted twice if the former one has not been finished. The sendDone failure is due to the mismatch of number of successfully send operations and number of sendDone events.

The above anatomy reveals that overlooking the existence of the gray zone inside the sensor node is likely to cause mismatch between the path estimation and the real forwarding capacity of the path. Thus we shall carefully estimate such an unreliable factor in the gray zone and use it as an important indicator to select “good” paths for data delivery.

A node can be rendered unreliable by many factors, e.g.,

• Network congestion. The receive/transmit queues will overflow, resulting in packet drops inside the node.   
Software bugs. For example, on Jan $1 0 ^ { t h }$ 2010, we observed a number of nodes that accept much traffic without forwarding it. After many rounds of verifications, we found it is due to a software bug in receiving buffer contention, which causes a node drop portion of received packets. We also found that many nodes choose those

malfunctioned nodes as parents as they are unaware of the intra-node packet drops. Such a fact reveals the limitation of existing ETX-based routing in overlooking node unreliability.

• Hardware failures. As reported in [20], [24], the sensor hardware becomes more unstable at a higher temperature. The atrocious weather and environment may also increase the chance of packet losses on a relaying node.

Indeed, there are many effective approaches to address software bugs, race conditions, routing loops, congestion and etc. They can, however, hardly address all the problems inside the node, and they may not be effective to address these problems in real time. For example, blacklisting and backpressure are effective to address network congestion, but they may not be effective in fixing software bugs. Therefore, it is likely that a packet gets lost inside the node. Combining all these factors into an integral metric can be beneficial to routing protocols in presence of node unreliability. Therefore, in this paper, we propose node-QoF to measure the instant node forwarding quality and take it into consideration in building optimized routing paths.

2) Packet Loss over Link: Another observation is that transmission timeout is common and accounts for a large portion of packet drops. For a 100-hour data set collected from the 330-node network, the transmission timeout accounts for 61.08% of all packet drops while the remaining packet loss is due to intra-node unreliability. This is the result collected from a network with a relatively high retransmission threshold of 30 in CTP. For lower values of the retransmission threshold, the problem will be more severe. As the example shown in Fig. 1, ETX-based routing will treat both paths equally good because both paths have a path-ETX of 20. However, in considering data delivery reliability, path 2 is obviously better than path 1 as it delivers about 2 times more packets. ETX, which works well in reducing the transmission cost when end-to-end delivery is presumed highly reliable, may not be necessarily appropriate for improving the end-to-end reliability of data delivery.

# IV. QOF METRIC DESIGN

Current metrics for route selection have either of the following two limitations. (1) They only consider the transmission cost without necessary consideration of the data delivery ratio along a forwarding path. (2) They only consider packet losses over the links while overlooking packet drops on a forwarding node. To address these limitations, we propose QoF, Quality of Forwarding, which is defined to be the data yield over the actual number of transmissions. Therefore, the QoF metric comprehensively characterizes both the data delivery ratio and transmission cost of the forwarding paths.

# A. Generic Link Model

We use a generic link model as the basis of QoF design. A generic link from A to B in the model represents either a physical link or a traversing path of the packet inside a node (so called a virtual link). When it is a physical link, A and

![](images/124c7aedeafb6279e2d9eccfb712a8d7e2be93d046ae49a755599b4342533fd1.jpg)



Fig. 4: The work flow of packet forwarding on a sensor node.

B are the corresponding sending and receiving nodes. When it is a virtual link, A and B respectively denote the starting (packet received) and ending (packet successfully sent) points of packet forwarding on a relaying node.

Associated with a link AB, there are two attributes.

• The link quality q, which denotes the probability of a packet to successfully go through the link.   
The limit of retransmissions r. The sender is allowed to retransmit the packet for at most r times before giving up.

Then the packet delivery ratio on a generic link is

$$
P D R = 1 - (1 - q) ^ {r + 1} \tag {1}
$$

Equation (1) indicates the probability of a packet to successfully go through the link with quality q and retransmission limit r.

Note that the physical and virtual links comprise the entire path of packet delivery from source to destination. We examine the PDR on both types of links.

PDR over a physical link. For a physical link, q is the link quality and r is the retransmission limit.

PDR over a virtual link. For a virtual link inside the node, q denotes the forwarding quality of a forwarding node, and $r = 0$ , i.e., no retransmission is executed inside a node. For a typical sensor node, PDR measures the forwarding quality from where the packet is received (at the MAC layer) to where the packet is passed downwards to the MAC layer for transmission.

PDR on a virtual link characterizes the forwarding quality of a node. For example, if a problematic node receives a large number of packets without forwarding them, its PDR equals to 0.

# B. QoF of a Generic Link

In order to consider both the transmission cost and the packet delivery ratio, we define ETC of a generic link to be the expected transmission count for a unique packet over the link,

$$
\begin{array}{l} E T C = \left(\sum_ {k = 1} ^ {r + 1} k q (1 - q) ^ {k - 1}\right) + (r + 1) (1 - q) ^ {r + 1} (2) \\ = \frac {1 - (1 - q) ^ {r + 1}}{q}, \\ E T C = \left(\sum_ {k = 1} ^ {r + 1} k q (1 - q) ^ {k - 1}\right) + (r + 1) (1 - q) ^ {r + 1} (2) \\ = \frac {1 - (1 - q) ^ {r + 1}}{q}, \\ \end{array}
$$

![](images/3d6a0fdd6770830eb776a95c2acac58b2ab3abce698001c1ce20655ca1e55bde.jpg)



Fig. 6: QoF computation.

where $q ( 1 - q ) ^ { k - 1 }$ denotes the probability that a packet passes the link at k-th time. Therefore, the term $\begin{array} { r } { \sum _ { k = 1 } ^ { r + 1 } k q ( 1 - q ) ^ { k - 1 } } \end{array}$ calculates the expected number of transmissions that the packet passes the link and the term $( r + 1 ) ( 1 - q ) ^ { r + 1 }$ calculates the expected transmission counts that a packet fails to pass the link.

ETC represents the actual transmission count a packet experiences. Note that ETC differs from ET X in that it not only considers link quality but also retransmission limit. When r ∞, $E T C { = } E T X$ . When r equals to a fixed number, ET X overestimate the transmission count while ETC reflects the actual transmission count under retransmission limit r.

We define $Q o F$ of a generic link as ratio of the data delivery ratio to the actual transmission cost,

$$
Q o F = \frac {P D R}{E T C}
$$

For a single link, substituting Equations (1) and (2) into the above equation, we have

$$
Q o F = \frac {P D R}{E T C} = q.
$$

For a single link, $Q o F ^ { - 1 } = E T X$ .

# C. QoF of a Forwarding Path

To calculate the $Q o F$ of a forwarding path, we use the following notations as shown in Fig. 6,

· $L i n k P D R _ { n , n - 1 }$ is the PDR over the link from node n to node n-1.   
• $N o d e P D R _ { n }$ denotes the PDR on node n.

$P a t h P D R _ { n , i }$ denotes the PDR of path (n, i), with node PDR on the starting node n excluded. As shown in Fig. 6, PathPDR can be calculated as ${ \cal P } \ / a t h P D { R } _ { n , 1 } ~ = ~ L i n k P D { R } _ { n , n - 1 } ~ \times ~ N o d e P D { R } _ { n - 1 } ~ \times ~$ $L i n k P D R _ { n - 1 , n - 2 } \times N o d e P D R _ { n - 2 } \times . . . \times N o d e P D R _ { 1 }$ .   
• $L i n k E T C _ { n , n - 1 }$ is the ETC over the link from node n to node n 1. It can be calculated according to Equation (2). $P a t h E T C _ { n , 1 }$ is the expected number of transmissions of a packet along the path from n to 1.   
• ${ Q o F } _ { n , 1 }$ is the QoF for the n-hop path from n to 1. ${ Q o F } _ { n , 1 }$ is the number of packets received at the destination over the actual number of transmissions along the path. $Q o F _ { n , 1 } =$ $\frac { P a t h P D R _ { n , 1 } } { P a t h E T C _ { n , 1 } }$ .

We do not count the ETC within a node because it does not incur actual communication cost. ${ \cal Q } o F _ { n , 1 }$ is calculated as,

$$
\begin{array}{l} Q o F _ {n, 1} = \frac {\text { PathPDR } _ {n , 1}}{\text { PathETC } _ {n , 1}} \\ = \frac {\text { PathPDR } _ {n , 1}}{\text { LinkETC } _ {n , n - 1} + \text { LinkPDR } _ {n , n - 1} \cdot \text { NodePDR } _ {n - 1} \cdot \text { PathETC } _ {n - 1 , 1}} \tag {3} \\ \end{array}
$$

where $L i n k P D R _ { n , n - 1 } \cdot N o d e P D R _ { n - 1 }$ denotes the probability that a packet from n can be forwarded by n − 1.

Since $\begin{array} { r } { P a t h E T C _ { n - 1 , 1 } = \frac { P a t h P D R _ { n - 1 , 1 } } { Q o F _ { n - 1 , 1 } } , ~ Q o F _ { n , 1 } } \end{array}$ PathPDRn−1,1QoF , QoFn,1 can also be n 1,1 −calculated in a hop-by-hop recurrence as follows,

$$
\begin{array}{l} Q o F _ {n, 1} = \frac {\text { PathPDR } _ {n , 1}}{\text { LinkETC } _ {n , n - 1} + \text { LinkPDR } _ {n , n - 1} \cdot \text { NodePDR } _ {n - 1} \cdot \text { PathETC } _ {n - 1 , 1}} \\ = \frac {\text { PathPDR } _ {n , 1}}{\text { LinkETC } _ {n , n - 1} + \frac {\text { PathPDR } _ {n , 1}}{Q o F _ {n - 1 , 1}}} \tag {4} \\ \end{array}
$$

$Q o F _ { 2 , 1 }$ can be calculated by Equation (3).

The path $Q o F$ considers both data delivery ratio and transmission cost. If the data delivery ratios of two paths are the same, QoF favors the path with lower transmission cost. If the transmission cost of two paths are the same, $Q o F$ favors the path with high data delivery ratio. The QoF metric differs from ET X in three aspects. First, it calculates the transmission cost more accurately. As mentioned above, ET X overestimate the transmission cost. Second, it considers data delivery ratio which is important for data collection protocols. Third, it also considers node unreliability.

The $Q o F$ metric also considers the impacts of link positions [3] and node positions. Consider path 2 shown in Fig. 1. Path $2 \ ' _ { \textrm { S } } Q o F$ equals to $\frac { 1 } { 5 6 }$ . If the two links were exchanged, path $2 \mathrm { { s } } Q o F$ would be ${ \frac { 1 } { 3 8 } } .$ The $Q o F$ metric selects path with good links near the destination. If bad links are near the destination, the packet loss on such links will waste transmission efforts on previous hops while not contributing to the data yield at the destination.

Now we look back to the example shown in Fig. 1, the following are three scenarios to examine the $Q o F$ for forwarding paths:

Scenario 1. Assume $r = 0$ and all nodes have PDR = 1 (nodes will never drop packets).

For path P1, we have $L i n k P D R _ { 3 , 2 } = 1 / 1 0 , L i n k P D R _ { 2 , 1 } =$ 1/10, and $P a t h P D R _ { 3 , 1 } \ = \ 1 / 1 0 0$ . The expected transmission count for link between node 2 and 3 can be computed as $L i n k E T C _ { 3 , 2 } = 1$ , and $L i n k E T C _ { 2 , 1 } = 1$ . The path QoF for P1 is $Q o F _ { 2 , 1 } = 1 / 1 0$ and $Q o F _ { 3 } = 1 / 1 1 0$ , which means a successful end to end delivery incurs 110 transmissions for P1. For path P2, similarly we have $Q o F _ { 3 , 1 } = 1 / 3 8$ , which means a successful end to end delivery incurs 38 transmissions for P2.

![](images/0ea156866a56ca70fe3e965ff51c70e9a9962ef14219198724ae047da5887c4e.jpg)



Fig. 7: Integrating QoF with CTP and Layer structure of QoF implementation.

This scenario shows that although the paths have equal ET X values, the cost for a successful end to end delivery can be quite different. The cost for P1 is about 2 times larger than the cost for P2. Such a difference cannot be measured by ET X. By simultaneously considering the transmission cost and the packet delivery ratio QoF provides more comprehensive estimation.

Scenario 2. Now we consider the second scenario where r = 0 and there are nodes with PDR less than 1. For simplicity, we assume only one node with PDR value less than 1. If $N o d e P D R _ { 2 } = 1 / 2$ , we have $Q o F _ { 3 , 1 } = 1 / 5 7$ on P2. If $N o d e P D R _ { 1 }$ $= 1 / 2 , Q o F _ { 3 , 1 } = 1 / 7 6$ on P2. This scenario shows that the node’s forwarding quality indeed affects the transmission cost.

Scenario 3. In this scenario, we assume $r = 1$ for all links and $P D R = 1$ for all nodes. For P1, $Q o F _ { 3 , 1 } = 1 9 / 1 1 9 0$ . For P2, $Q o F _ { 3 , 1 } = 3 7 / 1 0 6 4$ , which is about 2 times of P1’s QoF, while originally QoF of P2 is almost 3 times of that of P1. Such a result further implies increasing retransmission count can improve the path quality while the improvements brought by retransmissions are different for different paths.

# V. EVALUATION

Our implementation is based on TinyOS 2.1 in NesC. We implement the QoF and incorporate it in state-of-the-art data collection protocol, CTP. The hardware platform is the TelosB mote with MSP430 MCU and CC2420 radio.

The overview architecture is shown in Fig. 7. In order to incorporate the QoF metric in CTP, we use the QoF estimator, QofC, to interact with CTP for path selection. The QoF estimator is based on PDR estimators for the node (NodePdrC) and for the link (LinkPdrC). It combines the node and link PDR for path quality computation and provide QoF information to the routing protocol. The link PDR estimator is built upon the 4-bit link estimator. The interface provided by the QoF estimator contains only one command, getQoF(), with the path QoF as the return value.

![](images/cc6d1933e03eae0d9915358f8df06179df90a8b3ce3c3f185ba4771022afb6a4.jpg)



Fig. 8: The picture of test-bed.

In this section, we evaluate effectiveness of our design extensively. Section V-A introduces the evaluation methodology. Section V-B examines how QoF improves the routing performance. Section V-C summaries the results.

# A. Methodology

We use a test-bed network consisting of 50 TelosB nodes to evaluate the efficacy of our design. Fig. 8 depicts the testbed we conduct experiments on. We integrate QoF with CTP (CTP-QoF) for evaluating the performance of QoF in supporting routing. In the network, we set the power level of the transmissions to 1 to construct a multi-hop network. We mainly compare CTP-QoF with the original CTP protocol (CTP-ETX) in following two cases.

Case I: streaming application case. In this case, we set the retransmission threshold to 1 and the transmission frequency per node to 3Hz. In such a case, we explore the performance of QoF in supporting data streaming applications that pursue low latency and high traffic throughput without reliability guarantee on individual packets.

Case II: real-world deployment case. In this case, we set the retransmission threshold to 30 and the transmission frequency per node to 3Hz, which is the same with our settings in the real-world deployment. Based on our experience with GreenOrbs, we use a program version before Jan 10th 2010, with some “problematic” nodes that drop a portion of incoming packets. Some problematic nodes can still report QoF to its neighboring nodes while other nodes may keep silent all the time.

We use three key metrics to compare CTP-QoF and CTP-ETX:

1) Data yield: the number of successfully received packets at the sink over the total number of generated packets.   
2) Transmission cost: the total number of packets transmitted in the network.   
3) Transmission cost per data delivery: the number of transmissions normalized by the data yield.

# B. Performance Comparison

We present the experimental results in this section, comparing the performance of CTP-QoF and CTP-ETX.

![](images/72b1766fc6e68c7dcc849f49d70095abd9b781c0b0c9a666d362263d3e4643fc.jpg)



Fig. 9: Comparison of node yield for CTP-ETX and CTP-QoF for Case I.

![](images/3c2885f37c3e138434d4a950deabfb13ab2209a2787e4261113213fc5c529053.jpg)



Fig. 10: Comparison of node yield for CTP-ETX and CTP-QoF for Case II.

1) Data Yield: We first investigate the improvement of using QoF to the data yield in the network. In this experiment, we use the setting in case I and case II. Fig. 9 depicts the node yield of CTP-QoF and CTP-ETX for case I. The node yield shows the data yield for a specified node. We find from Fig. 9 that most nodes have a higher node yield in CTP-QoF than nodes in CTP-ETX. There are only four nodes (ID 9, 12, 41, 45) which have similar node yield. We find that link qualities of those nodes in CTP-QoF are very low and among all outgoing links those nodes cannot find an alternative path to avoid packet drops. The average improvement is around 12%. The improvement of CTP-QoF in case I is mainly due to the fact that as the retransmission limit is low, PDR of links is low and thus packets are likely to be dropped over links. This type of packet drops cannot be captured by ETX estimation. The packet drops due to limited retransmissions affect the entire path and such an effect, while is not quantified by existing methods, can be captured by the QoF metric.

Fig. 10 shows the node yield of CTP-ETX and CTP-QoF for case II. During the experiment, the problematic nodes randomly drop around 30% of the received packets. Again we find from Fig. 10 that almost all nodes in CTP-QoF have higher node yields than those in CTP-ETX. This is because that QoF measures the forwarding qualities of both the nodes and the links. We find from Fig. 10 that the yield of some nodes in CTP-ETX are only one third of those in CTP-QoF.

![](images/b4e2e9ec20da45043b7e77a5b42fc8453baf05aaede3b9902dfc3c2a17e5268e.jpg)



Fig. 11: Topology of the nodes on the test-bed. Node 20 has links to node 14, 15, 88, 89 and node 88 and 89 are two problematic nodes.

![](images/acf9001ac5cfb152754fcb41f90ecd2e38527763dc87e9ce687d2be6ccd0262b.jpg)



(a)

![](images/ab9bfc6f24e0c745e3bed6fb687ebe7c28cdd3ff0159d708c1efeba7ae4b6e58.jpg)



(b)   
Fig. 13: Incoming packets for QoF and ETX in case II. (a) CTP-QoF, (b) CTP-ETX.

![](images/150f4fc00b168e5bbde7e2ed80fbd4219d0ea684b246e524daea474348e21d93.jpg)



![](images/eba9fd2ab188bec05b6d4427e8f148a432a606e0b2d18916dfa074b2d7ce9091.jpg)



Fig. 12: Path-ETX and path-QoF from node 20 through node 14, 15, 88, 89 (a) ETX. (b) QoF.

![](images/837b6166b5cc2fa79fc95ee2b05d45ab5620d1a57e9cb39edd982855b1bafa2f.jpg)



![](images/7337342a4f5abf447545f0bc04bff9de631010e38ced5fd04d4c0d64c30d6788.jpg)



(b)   
Fig. 14: Total traffic comparison of CTP-ETX and CTP-QoF for different cases. (a) Case I, (b) Case II.

We look into the experimental data and find that with ETX estimation, many problematic nodes exist on the optimal data delivery paths chosen by CTP-ETX. In CTP-QoF, however, most of the problematic nodes are excluded from the optimal routing paths. For example, as shown in Fig. 11, we select node 20 near the problematic nodes on the test-bed and investigate its behavior. Links from 20 to nodes 88, 89, 14, 15 are shown in the Fig. 11. Here node 88 and node 89 are two problematic nodes. Fig. 12 (a) shows the ETX values of node 20 to 4 neighbors. By using the ETX values, the node cannot distinguish problematic nodes from normal nodes. Fig. 12 (b) shows that paths containing the problematic nodes have a lower QoF. Therefore, using QoF values can avoid selecting path containing those problematic nodes.

We further investigate the behaviors of problematic nodes in comparison with the normal nodes in CTP-QoF. The normal nodes are selected close to problematic nodes such that they have similar external conditions.

We find from Fig. 13 (a) a clear trend that in CTP-QoF the incoming traffic for problematic nodes does not accumulate much, as the QoF information help to choose paths that avoid the problematic nodes of much lower forwarding quality. On the other hand, CTP-ETX overlooks the internal problems on the problematic nodes and chooses delivery paths simply according to the link estimation. As a result, the incoming traffic on problematic nodes grows similarly with the traffic on normal nodes as shown in Fig. 13 (b). It implies that other nodes are unaware of the packet loss inside the problematic nodes and keep sending packets to them, resulting in degraded routing performance.

2) Transmission Cost: In this set of experiments, we evaluate the total data transmissions incurred within the entire network for CTP-QoF and CTP-ETX. We conduct experiments for both cases I and II. Fig. 14 (a) shows the network traffic cost for case I, and Fig. 14 (b) shows the network traffic cost for case II. In both cases, CTP-QoF saves nearly 30% transmission cost compared with CTP-ETX, which again validates the effectiveness of QoF.

3) Normalized Transmission Cost: In this section, we evaluate the average number of transmissions for a successful end-to-end delivery (i.e. normalized transmission cost), which the QoF metric tries to minimize. Fig. 15 compares CTP-QoF with CTP-ETX in both cases I and II. The average cost for the end-to-end data delivery in CTP-QoF is much less than the cost in CTP-ETX. For case I, the CTP-QoF reduces the average cost/yield by 28%. For case II, the CTP-QoF reduces the average cost/yield by 34%. This is mainly because of the more comprehensive estimation on the path quality in CTP-QoF.

# C. Summary of Results

The above experimental results reveal the following findings.

1) The QoF metric minimizes the benefit/price ratio. The evaluation results show that QoF-based routing reduces the cost/delivery by 28%–34%.

![](images/319b30098d4e9e7f9245c20f4a25639988d3b0039fd8eb20b36d30cc0fb6c14b.jpg)



![](images/daa32f5bbc395e3f5424f16d0bbd6876632c282051d3eff25d1a80568e375b79.jpg)



Fig. 15: Normalized traffic comparison of CTP-ETX and CTP-QoF for different cases. (a) Case I, (b) Case II.

2) The QoF metric can effectively capture the impact of both the data yield and the transmission cost, improving the data yield by 12%–15% and reducing the transmission cost by about 30%.   
3) There is a tradeoff in determining the retransmission limit. With a higher retransmission limit, the link PDR is supposed to be improved while the node PDR may decrease as retransmission consumes system resources. Higher number of retransmissions may also increase channel contentions, affecting other links’ reliability. Therefore, the retransmission limit should be carefully chosen so that we can obtain a satisfactory PDR along a path.

# VI. CONCLUSION

Comprehensive and accurate measurement of path quality is an essential and crucial factor in founding an efficient routing mechanism for multihop wireless sensor networks. Existing approaches for path quality estimation emphasize link quality in between in nodes, but overlook the end-to-end data delivery ratio and the node unreliability. This paper presents our experience with GreenOrbs, which suggests that the existing metrics fail to make comprehensive measurement of path quality. Our proposal called QoF, overcomes this limitation by simultaneously considering node forwarding quality and link quality based on a generic link model. As analyzed and demonstrated by the experiments, routing decisions yielded with QoF achieve low traffic cost as well as high end-toend delivery ratio. We plan to port QoF to GreenOrbs’ future deployments with 1000+ sensor nodes.

# ACKNOWLEDGMENTS

This study is supported in part by NSFC/RGC Joint Research Scheme N HKUST602/08, National Basic Research Program of China (973 Program) under Grants No. 2010CB328000 and 2011CB302705.

# REFERENCES

[1] D. Couto, D. Aguayo, J. Bicket, and R. Morris, “A highthroughput path metric for multi-hop wireless routing,” in Proceedings of ACM MobiCom, 2003.

[2] L. Sang, A. Arora, and H. Zhang, “On exploiting asymmetric wireless links via one-way estimation,” in Proceedings of ACM MobiHoc, 2007.   
[3] G. Jakllari, S. Eidenbenz, and et al, “Link Positions Matter: A Noncommutative Routing Metric for Wireless Mesh Networks,” in Proceedings of IEEE INFOCOM, 2008.   
[4] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X. Li, and G. Dai, “Canopy closure estimates with GreenOrbs: sustainable sensing in the forest,” in Proceedings of SenSys, 2009.   
[5] G. Werner-Allen, K. Lorincz, J. Johnson, J. Lees, and M. Welsh, “Fidelity and yield in a volcano monitoring sensor network,” in Proceedings of USENIX OSDI, 2006.   
[6] CTP TEP: http://www.tinyos.net/tinyos-2.x/doc/html/tep123. html.   
[7] TinyOS. [Online]. Available: http://www.tinyos.net   
[8] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection tree protocol,” in Proceedings of ACM SenSys, 2009.   
[9] J. Polastre., R. Szewczyk., and D. Culler., “Telos: Enabling Ultra-low Power Wireless Research,” in Proceedings of ACM/IEEE IPSN, 2007.   
[10] K. Srinivasan and P. Levis, “Rssi is under appreciated,” in EmNets, 2006.   
[11] S. Lin, G. Zhou, K. Whitehouse, Y. Wu, J. Stankovic, and T. He, “Towards Stable Network Performance in Wireless Sensor Networks,” in Proceedings of IEEE RTSS, 2009.   
[12] H. Zhang, L. Sang, and A. Arora, “Comparison of data-driven link estimation methods in low-power wireless networks,” IEEE Transactions on Mobile Computing, vol. 9, 2010.   
[13] R. Draves, J. Padhye, and B. Zill, “Comparison of routing metrics for static multi-hop wireless networks,” ACM SIGCOMM Computer Communication Review, vol. 34, no. 4, pp. 133–144, 2004.   
[14] O. Gnawali, M. Yarvis, and et al, “Interaction of retransmission, blacklisting, and routing metrics for reliability in sensor network routing,” in Proceedings of IEEE SECON, 2004.   
[15] A. Cerpa, J. Wong, M. Potkonjak, and D. Estrin, “Temporal properties of low power wireless links: modeling and implications on multi-hop routing,” in Proceedings of ACM MobiHoc, 2005.   
[16] Y. Gu and T. He, “Data forwarding in extremely low dutycycle sensor networks with unreliable communication links,” in Proceedings of ACM SenSys, 2007.   
[17] S. Biswas and R. Morris, “Exor: Opportunistic multi-hop routing for wireless networks,” in Proceedings of ACM SIGCOMM, 2005.   
[18] S. Chachulski, M. Jennings, S. Katti, and D. Katabi, “Trading structure for randomness in wireless opportunistic routing,” in Proceedings of ACM SIGCOMM, 2007.   
[19] K. Kim and K. Shin, “On accurate measurement of link quality in multi-hop wireless mesh networks,” in Proceedings of ACM MobiCom, 2006.   
[20] T. Schmid, Charbiwala, and et al, “Exploiting manufacturing variations for compensating environment-induced clock drift in time synchronization,” ACM SIGMETRICS Performance Evaluation Review, vol. 36, no. 1, pp. 97–108, 2008.   
[21] S. Moeller, A. Sridharan, B. Krishnamachari, and O. Gnawali, “Routing without routes: the backpressure collection protocol,” in Proceedings of ACM/IEEE IPSN, 2010.   
[22] B. Hull, K. Jamieson, and et al, “Mitigating congestion in wireless sensor networks,” in Proceedings of ACM SenSys, 2004.   
[23] A. Sridharan and B. Krishnamachari, “Explicit and precise rate control for wireless sensor networks,” in Proceedings of ACM SenSys, 2009.   
[24] T. Schmid, R. S. Shea, and et al, “On the Interaction of Clocks, Power, and Synchronization in Duty-Cycled Embedded Sensor Nodes,” ACM Transactions on Sensor Networks, vol. 7, pp. 24:1–24:19, 2010.