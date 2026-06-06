# Opportunistic Concurrency: A MAC Protocol for Wireless Sensor Networks

Qiang Ma, Member, IEEE, Kebin Liu, Member, IEEE, Zhichao Cao, Member, IEEE, Tong Zhu, Member, IEEE, Xin Miao, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—How to shorten the time for channel waiting is critical to avoid network contention. Traditional MAC protocols with CSMA often assume that a transmission must be deferred if the channel is busy, so they focus more on the optimization of serial transmission performance. Recent advances in physical layer, however, allows a receiver to reengage onto a stronger incoming signal from an ongoing transmission or interference, and thus shows the potential of parallel transmissions. Indeed, even if the channel is busy, a node has opportunities to carry out a successful transmission. In this study, we propose opportunistic concurrency (OPC), a new MAC layer scheme, which enables sensor nodes to capture the opportunistic concurrency and carry out parallel transmissions instead of always waiting for a clear channel. Based on local concurrency map, which encodes the interactions among different links, OPC utilizes concurrency control algorithm to make transmission decision distributedly. Our experiments on a testbed consisting of 60 TelosB sensor motes identify the transmission opportunities in WSNs with OPC. Evaluation results show that OPC achieves a 17 percent reduction in packet latency, a 9.4 percent addition in throughput and a 10 percent reduction in power consumption compared with existing approaches.

Index Terms—Concurrent MAC protocol, wireless sensor networks

# 1 INTRODUCTION

N most of existing MAC protocols, we always hold that Ithe data transmissions should make way for the interference. Otherwise, the transmissions must fail. The earliest collision pattern is illustrated as: If the signal of interest (SoI) arrives later than the interference, no matter how strong the power of SoI is, the signal cannot be decoded by the receivers. Carrier sense multiple access (CSMA) is such a probabilistic media access control protocol common to almost all modern wireless networks. The most popular way to detect an ongoing transmission by CSMA is called “Energy Detect” [11], which is based on signal strength readings. Before transmitting, a transmitter listens to the channel. If the channel is busy, the transmission is deferred. Otherwise, the carrier sense is idle and the transmission is allowed. Obviously, to guarantee the channel quality, CSMA forbids any concurrent transmission.

In many cases the network traffic of wireless sensor networks (WSNs) becomes very heavy especially when some links suffer bursty packet forwarding tasks. To avoid traffic contention and high latency, many research efforts have been made on shortening the time for channel waiting. Most of existing approaches, however, only discuss the optimization of serial transmission performance [3], [4], [27].

The latest physical layer advances allow a receiver to reengage onto a stronger incoming signal from an ongoing interference. Capture Effect was understood through the systematic work in [13], [21]. Authors showed that the laterarrived SoI can be successfully decoded if and only if the gap is in the period of preamble. Message in message (MIM) is such a physical layer capability that allows a receiver to reengage onto a stronger incoming signal from an ongoing transmission or interference even if the preamble signal has been received [14], [19].

These capabilities have been leveraged to improve throughput in enterprise wireless networks [19]. Those approaches relying on a central controller, unfortunately, are not feasible for WSNs. A sensor node must make its transmission decision based on its local information. In addition, transmission time for a packet in WSNs is usually very short. Therefore, to fulfill a concurrent transmission puts a strict constraint on the time used for making decisions.

To address the above issues, we propose opportunistic concurrency (OPC), a new MAC layer algorithm integrating concurrency with CSMA to guide the transmission decisions. The main goal of OPC is to enable sensor nodes to capture the opportunistic concurrency and carry out parallel transmissions instead of always waiting for a clear channel. In Fig. 1, $S _ { 1 }$ wants to forward the packets to $R _ { 1 }$ , while $S _ { 2 }$ is transmitting packets to $R _ { 2 } .$ . Due to the broadcasting characteristic in WSN, $R _ { 1 }$ will overhear the packets from $S _ { 2 } .$ . In this case, $S _ { 1 }$ is always making way for the interference from $S _ { 2 }$ under traditional CSMA protocols. In OPC, $S _ { 1 }$ can selectively transmit the packets according to the SINR values on $R _ { 1 }$ and $R _ { 2 } .$ . Each sensor node maintains a local concurrency map which records the SINR values among the neighbors. Once carrier sense indicates that the current channel is busy, the node will identify the interference, then search the map to quickly find out the relevant values, and compute whether a concurrent transmission is allowed or not. Unlike traditional MAC protocols based on CSMA, OPC improves the channel by enhancing parallel transmissions.

![](images/1f533f768fd161e8e31cc1e1b95c5dafc00068a3d3f103e3064d9eb09cc960bf.jpg)



Fig. 1. Transmission opportunity. Real line like $S _ { 1 }  R _ { 1 }$ means SoI while dash line like $S _ { 1 }  R _ { 2 }$ means interference. Under CSMA, the data from $S _ { 1 }$ must be delayed until S finishes its transmission, while OPC allows transmission concurrency if both SINR on $R _ { 1 }$ and $R _ { 2 }$ satisfy.

To the best of our knowledge, OPC is the first distributed scheme which exploits concurrency to aid CSMA in making transmission decisions in WSNs. The contributions of this work are as follows:

We present the concurrency map which encodes the interactions among different links, and thus helps sensor nodes capture the opportunities of concurrent transmissions.   
We propose a concurrency control algorithm that makes transmission decisions distributedly.   
We evaluate OPC through a real testbed consisting of 60 TelosB motes. The results show that OPC achieves a 17 percent reduction in packet latency, a 9.4 percent addition in throughput and a 10 percent reduction in energy consumption compared to the traditional CSMA protocol.

The rest of the paper is organized as follows. Section 2 gives a general background for this work, and summarizes the related work. Section 3 gives a series of validation experiments. Section 4 presents our design and provides additional techniques to deal with several practical issues on implementation. After introducing the implementation details including interface design and overhead control in Section $5 ,$ Section 6 shows the evaluation results from a real indoor testbed experiments. Section 7 finally concludes the paper.

# 2 BACKGROUND

This work is motivated by our deployed sensor network system, GreenOrbs, which aims to achieve large-scale and longterm surveillance in the forest [17], [20]. To achieve this goal, how to beneficially control and save power is critical.

# 2.1 Duty-Cycling MAC Protocol

Idle listening is one of the most significant sources of energy consumption. To enhance the energy efficiency, duty-cycling is widely used in MAC protocol for wireless sensor networks. The approaches to duty-cycling MAC protocols can be broadly divided into two categories: Techniques requiring synchronization to ensure the nodes can concurrently wake and sleep; and those that allow each node to has an independent schedule. The synchronous duty-cycling MAC protocols, such as S-MAC [29], T-MAC [27], and RMAC [4], all simplify the communication and avoid power listening, but add much complexity and need extra overhead to achieve synchronization. On the other hand, the asynchronous dutycycling protocols consume more energy in transmitting preambles which are used to inform the neighbors to achieve action synchronization. B-MAC [24] precedes the data packet with a preamble of determined length.

![](images/e336c1a8fa77fd43a022f405f124e8ed9bfb2c6e0457bbd9833ea8d5c3aa955b.jpg)



Fig. 2. X-MAC protocol. X-MAC guides the sensor nodes when to wake up and sleep. Its default transmission strategy is on the basis of CSMA, that is, no concurrency transmission is allowed.

In some cases, due to that the preamble cannot be cut short, transmissions to the same destination have to cost much time in waiting for a clear channel. X-MAC [3] partly addresses this serial waiting problem by using a short preamble. RI-MAC [26] is similar to X-MAC, in which the sender remains active and waits silently until the receiver explicitly signifies when to start data transmission by sending a short beacon frame. In GreenOrbs, we apply X-MAC which is an advanced asynchronous low duty cycle protocol [3] to guide the nodes wake up and sleep. As illustrated in Fig. 2, X-MAC uses short preamble packets instead of a constant stream of preamble. Thus, X-MAC inserts small gaps between these preamble packets, during which the transmitter is able to listen to the medium. The gap period enables the receiver to send an early acknowledge packet to inform the transmitter, so the sender can immediately begin transmitting the data packet upon receiving the ACK packet. Compared to the traditional protocols, X-MAC shortens the preamble period. Based on CSMA, however, X-MAC does not consider the concurrency cases. When there are a number of pairs of nodes competing for the channel, they still have to proceed in the form of serial transmitting. To overcome the above mentioned limitations as well as improve the network throughput and decrease the packet latency, we seek concurrent transmissions while keeping all collided packets successfully decoded by their respective receivers.

# 2.2 Transmission Concurrency

Transmission concurrency has been extensively investigated in the literature. Most of them focus on 802.11. The empirical evidence of capture was showed in [13], [21], and the study in [14] analyzes the relates threshold requirements. In [19] the authors make use of MIM to reorder the transmissions, thus create the concurrent transmissions. Gudipati and Katti [7] allows a receiver to decode both packets from collisions, and achieves the same throughput as the collision-free scheduler. By leveraging recent works on rateless code [7], [23], the authors in [8] provides a rateless MAC design that systematically exploits interference and consistently performs well across both uplink and downlink scenarios. Acharya et al. [2] presents a distributed algorithm based on RTS/CTS scheme, to enable simultaneous transmissions in multi-hop ad-hoc wireless networks.

![](images/5bf6c8ece6f968ff6a3ba30b436c79bc6a9e111645b7a43a20273a205335af2e.jpg)



Fig. 3. Design of validation experiment.

In WSNs, capture awareness has been used for rapid flooding in [18] and collision detection and recovery in [28]. The authors in [22] systematically analyze the effects of combined interference. Lee et al. [15] presents a captureaware linear order algorithm to estimate link interference in multi-hop wireless networks. Many existing works [6], [9], [10], [16] study about interference cancellation, which claims to compute signal of interest from interference. ZigZag [6] is an 802.11 receiver design that combats hidden terminal and contributes a new form of interference cancellation that exploits asynchrony across successive collisions. These works, however, don’t intend to change the transmission decision for the nodes. Centralized approach is not suitable in WSNs, because it is costly and unreasonable for some deployed environments. Therefore, this work designs a distributed scheme as an assistant component to help the current MAC protocol to make a decision to improve the network performance.

# 3 VALIDATION EXPERIMENTS

To better show the potential benefits, we run a series of validation experiments on ChipCon CC2420 radio [1] in an isolated environment without much interference [19]. As Fig. 3 describes, we set two transmitters Tx and Intf synchronized to each other, and broadcast their messages in the air. Two sniffers are deployed to collect ground truth. We denote SoI-first as the case when SoI comes earlier than the noise. Otherwise, SoI-last. To distinguish SoI-first and SoI-last cases and keep continuous packet transmissions, we modify the traditional MAC layer: the transmitters still turn on the carrier sense, but the result of carrier sense will not impact the transmission decision. If the channel is detected as unclear, a flag bit in the packet will be set as 1, indicating that this packet is sent out under unclear channel. By locating the receivers at different positions, we compare the number of received packets, thus analyze the relationship between SINR and packet reception ratio.

Table 1 shows the delivery ratios for both SoI-first and SoI-last cases at different positions of the receiver. Observe that when the receiver is at position 1 or 2 (i.e., the SINR is high), the delivery ratio is always high independent of the order between SoI and interference. However, the delivery ratio of SoI-last decreases sharply at position 3 while most of SoI-first packets are received. When we put the receiver further from Tx at position 4, almost none of SoI-last cases is successfully decoded, and no more than 30 percent of SoIfirst cases overcome the interference. Besides, we search for the possible correlated parameters, such as SINR and data rate, and summarize that SINR condition is the most critical factor (detailed in Section 4.3). That is, a MIM-like feature supports the radio to successfully decode some SoI-last packets in high SINR condition.

TABLE 1 Result of Validation Experiment 

<table><tr><td></td><td>Position 1</td><td>Position 2</td><td>Position 3</td><td>Position 4</td></tr><tr><td>SoI-first</td><td>98.6%</td><td>90.0%</td><td>62.2%</td><td>28.5%</td></tr><tr><td>SoI-first</td><td>92.0%</td><td>62.7%</td><td>6.4%</td><td>1.5%</td></tr></table>

# 4 MAIN DESIGN

In this section, we present the design of OPC. The design goal of OPC includes efficiency and fairness. First, OPC should try to capture more opportunities of concurrent transmissions thus improve the network throughput as well as reduce the packet delivery latency. Second, OPC should make sure that the transmissions will never disturb each other “on purpose”, which means, within the local perceived knowledge, every transmission decision should consider about whether other transmissions will be impacted or not.

# 4.1 Overview

In traditional approaches, a transmission decision only depends on the channel energy detected by carrier sense. In our algorithm, we try to integrate MIM-like feature and more fine-grained interference information to make transmission decisions, thus increase the packet concurrency cases. Fig. 4 illustrates the framework of OPC and shows how OPC can be embedded into the current work. We describe the establishment of the concurrency map in Section 4.2. The concurrency control algorithm for decision making is presented in Section 4.3. We propose that the hidden terminal occurs following our pursuit of transmission concurrency. Our evaluation also proves that, however, compared to large amount of potential improvement in throughput, the harm of hidden terminal brought by OPC is quite little.

# 4.2 Concurrency Map Establishment

To help a node make timely decisions at MAC layer, locally storing the current concurrency map is needed. Otherwise, the time cost for figuring out the surrounding interference fails to meet the requirement a concurrency decision needs. Utilizing the characteristic of broadcasting in wireless network, every node extracts the signal strength value from the overhearing packets and broadcasts its own record to its neighbors. Simultaneously, every node receives the beacon messages from other nodes, filtering out the useful information to build its own local concurrency map. After a period of initialization process, each node will gain its onehop range concurrency map, which contains all the signal strength values of links between its neighbors if these two neighbors are also in each other’s communication range.

As the link quality changes as time goes by, the SINR value in the concurrency map changes even if the transmission power is fixed for every packet and the network topology is static. OPC also provides an updating scheme for concurrency map. Consider the existence of bursty link, we did not expect to find any correlation between the latest observation and those in history. In our design, the node will update its record whenever it detects its record is different with the latest observation, then broadcasts its local record in the air to inform the neighbors.

![](images/881d3248b50d471bd0483a4e6268b899e9f4c30d33649ac2e0e5244c5d193bc5.jpg)



Fig. 4. Design of OPC and how OPC is embedded into current framework. In the Concurrency Map there are the signal strength records among the neighbors. For example, $( S _ { 1 }  R _ { 1 }$ , D7) means the signal strength of the link from its neighbor $S _ { 1 } ^ { \dot { } }$ to $R _ { 1 }$ is D7, where D7 is the original raw data in TinyOS. Based on this local map, we can calculate the SINR condition on its neighbors. The final output is an interface called TDecision, which combines CCA interface in TinyOS and our calculation to decide the transmission strategy.

# 4.3 Concurrency Control Algorithm Design

Based on the current local concurrency map, a node can decide whether the channel is fit for transmission or not. If carrier sense detects that the channel is clear, the transmission should be allowed. Otherwise, according to the concurrency map and SINR condition, a node can analyze whether the packet concurrency will occur or not. If the SINR requirement is satisfied, the sender launches the transmission instead of making way for the interference. Pseudocode is presented in Algorithm 1.

Algorithm 1. Transmission decision from S to R   
1: Set the max concurrency number as $C_{max}$ 2: Initiate the decision strategy D = TRUE
3: Extract the information of interference. Denote k pairs of source node ID and destination node ID by $S_1$ and $R_1$ , $S_2$ and $R_2$ ... $S_k$ and $R_k$ .
4: if $k \geq C_{max}$ then
5:    Defer!
6: end if
7: if the SINR requirement on the receiver isn't satisfied then
8:    Defer!
9: end if
10: for i = 0 to k do
11:    Denote the interference to $R_i$ from S by $E_S^{R_i}$ .
12:    Compute the maximum allowed interference $E_i$ for $R_i$ .
13:    if $E_i < E_S^{R_i}$ then
14.    D = FALSE; break;
15:    end if
16: end for
17: if D = TRUE then
18:    Transmit!
19: else
20:    Defer!
21: end if

In Algorithm 1, we set a parameter called max concurrency number $C _ { m a x } ,$ i.e., our algorithm only permits at most $C _ { m a x }$ concurrent transmissions. Limiting the number of concurrent packets tends to decrease the following computational overhead, thus makes sure that the decision is timely and beneficial. In fact, our evaluation in Section 6 clearly clarifies that the throughput does not monotonically increase with $C _ { m a x }$ . At line 12, the maximum allowed interference $E _ { i }$ for $R _ { i }$ means that, if and only if the transmission power of interference on $R _ { i }$ is larger than $E _ { i } ,$ collision occurs on $R _ { i } .$ . Once any neighbor will be disturbed, this concurrency transmission is not allowed.

The next step is to filter useful information from the interference, i.e., the source node ID and destination node ID. How to make this real-time information available in our algorithm is nontrivial. Because the CC2420 radio is designed to be packet-level, which means we cannot extract the header information until we completely receive the packet. Neglecting the difference of propagation time, this packet-level scheme provides non-available information, i.e., the decision is for a serial packet transmission, but not for transmission concurrency. We will introduce the solution in what follows.

The third step is to check whether this transmission under an unclear channel will be successful, i.e., to compute SINR value on the receiver according to the concurrency map. If the transmission power fails to achieve the requirement, we give up the transmission concurrency.

Finally, we need to consider about whether the other transmissions will be disturbed by this decision. In our implementation, no priority value is assigned to packets, thus we didn’t allow any transmission decision that will result in any other transmission failure. Actually, what we expect is to utilize the potential opportunities to create transmission concurrency, but not to enforce any transmission with high signal strength.

# 4.3.1 Interference Identification

In X-MAC protocol, the senders need to broadcast additional preambles to inform the receivers to awake for oncoming packets. Every transmission usually needs to broadcast many preambles, so that a node can overhear one of them to accurately infer the possible ongoing transmissions. With a local concurrency map, what a node needs are the sender ID and receiver ID, which have been contained in X-MAC (line 3 in Algorithm 1). The related pseudocode is presented in Algorithm 2.

![](images/c0e5ef98cd3dbc6b51f313fde864e91b6bcaca0c4368e7d3ca24505fc1bbb512.jpg)



Fig. 5. Interference Identification. The main idea is to make use of preambles to timely decodes the interference information. When S1 intends to send out a packet, the carrier sense shows that the channel is busy. Then, S1 can overhear the preambles or packets in the air.

Algorithm 2. Interference identification   
1: Initiate an empty map $M(\text{SenderID}, \text{ReceiverID})$ to record the interference pair.
2: if the channel is unclear then
3: Overhear the following packet.
4: if the packet is a preamble then
5: Extract the information from the preamble.
6: if (SenderID, ReceiverID) is not in M then
7: Insert (SenderID, ReceiverID) into M.
8: end if
9: else if the packet is a data packet then
10: Extract the information from the packet.
11: if (SenderID, ReceiverID) is in M then
12: Remove (SenderID, ReceiverID) from M.
13: end if
14: end if
15: end if

For example, in Fig. 5, when $S _ { 1 }$ intends to send a packet to others, carrier sense indicates that the channel is engaged by others. Then, $S _ { 1 }$ overhears the ongoing transmissions in the air. If the packet is a preamble from $S _ { 2 }$ to $R _ { 2 }$ , the transmission is going-on, thus $S _ { 1 }$ can infer that the following interference is from link $S _ { 2 }  R _ { 2 } ,$ , else if the packet is a data packet, which means the transmission from $S _ { 2 }$ to $R _ { 2 }$ will finish soon. Here, assume that $S _ { 2 }$ only transmits exact one data packet after broadcasting preambles. Otherwise, we can easily modify the update scheme of concurrency map in the algorithm to adapt it. Besides, to avoid the number of packet concurrency is greater than $C _ { m a x . }$ , we add the number of ongoing transmissions into every packets, which consumes only one byte. In addition, when $C _ { m a x }$ is small (e.g., $C _ { m a x }$ is 2 or 3), we can also put the detail information about interference into the packets.

# 4.3.2 SINR Computation

After extracting the information of interference, i.e., Si $R _ { i } ,$ for $i = 1 , 2 , \dots , k .$ If the channel is clear, S transmits the

interface IMap {
    command void setNeighborSize(uint8_t size);
    command uint8_t getNeighborSize();
    command error_t sendBeacon(am_addr_t addr,
    void* msg, uint16_t len);
    command error_t sendMap(am_addr_t addr, void* msg, uint16_t len);
    event void beaconReceive(void* msg, uint8_t len);
    event void mapReceive(void* msg, uint8_t len);
    command uint8_t get(am_addr_t sender, am_addr_t receiver);
}

interface TDecision {
    command void get();
    command void updateInterference(am_addr_t interference_sender, am_addr_t interference_receiver);
}   
Fig. 6. The interfaces of IMap and TDecision. Similar to TinyOS programs, the parameter addr means node address, msg is the packet, len is the packet length.

packet as usual. Otherwise, S begins to compute the SINR on R based on the concurrency map. Under an assumption of additive multiple interference and non-fading channels [19], S checks that if:

$$
\epsilon + \sum_ {i = 1} ^ {k} I (S _ {i} \rightarrow R) \leq \frac {I (S \rightarrow R)}{1 0 ^ {\left(\tau_ {1} / 1 0\right)}}.
$$

$I ( S \to R )$ denotes the signal strength from S to R, and $\tau _ { 1 }$ is the SoI-last SINR threshold, i.e., if SINR is greater than $\tau _ { 1 } ,$ then R can receive packets from S even if S transmits later. - is a backoff signal strength to compensate the error due to environmental factors. Besides, it is to enable some unmeasured interference on the receiver by non-direct neighbors of transmitter.

If this condition is satisfied, the algorithm checks whether this transmission will disturb the others. Similarly, for every pair of interference $S _ { t }  R _ { t } , S$ checks that if:

$$
\epsilon + I (S \rightarrow R _ {t}) + \sum_ {i \neq t} ^ {k} I (S _ {i} \rightarrow R _ {t}) \leq \frac {I (S _ {t} \rightarrow R _ {t})}{1 0 ^ {\left(\tau_ {2} / 1 0\right)}}.
$$

We allow S to transmit if all the conditions are satisfied. $\tau _ { 2 }$ is the SoI-first SINR threshold. To keep the transmission order, we add a value field in the data and preamble packets.

# 5 IMPLEMENTATION

We implement OPC based on TinyOS 2.1. This section describes OPC’s implementation details. To show that it is easy to be embedded in current MAC protocol, we first describe the programming interfaces of OPC. Second, we evaluate OPC’s implementation overhead including required storage and computational overhead to claim that OPC is indeed feasible for current system configurations.

# 5.1 Programming Interface

The OPC module provides two interfaces, i.e., IMap and TDecision (in Fig. 6). IMap is for concurrency map which is the basis of the algorithm, while TDecision implements the core computation to provide transmission decisions.

# 5.1.1 IMap

IMap is provided to establish local concurrency map, including the signal strength values between surrounding neighbors. setNeighborSize and getNeighborSize are two commands for setting and obtaining the maximal number of neighbors. To balance the tradeoff between local storage and algorithm accuracy, the size of concurrency map should be set according to the real topology and deployment density. The sendBeacon command is used to broadcast beacon messages for the others to record the signal strength of this unidirectional link (i.e., we consider about the general cases of asymmetric link). The event beaconReceive will be signaled when the beacon message is actually received. Similarly, when the period for beacon transmission is over, through the command sendMap, we let every node broadcast its own record which contains the link signal strengths from others. Hence we signal mapReceive event to combine these map messages from the neighbors to establish a local concurrency map. Once we offer the sender ID and receiver ID, the command get is able to obtain the unidirectional signal strength value.

# 5.1.2 TDecision

TDecision is provided to make transmission decisions under an unclear channel condition. The command updateInterference is to update the current interference information, including different pairs of sender and receiver. If OPC is enabled, when the channel is detected to be engaged, we use command get to check whether the transmission concurrency is allowed or not. To be more specific, in the implementation of get, we repeat calling IMap. get to fetch the signal strength values between the corresponding nodes, then compute the SINR conditions. Generally, the command TDecision.get is called to make transmission decisions. If the output is TRUE, the concurrency condition is satisfied, otherwise failed.

# 5.2 Overhead

This section analyzes OPC’s implementation overhead in terms of memory overhead and computational overhead to show that our algorithm is feasible in source constrained sensor nodes.

# 5.2.1 Memory Overhead

OPC incurs memory overhead on RAM and ROM respectively for data and program storage. (i) To store concurrency map consumes most data memory in OPC. Let neighborsize denotes the size of neighbor table, hence every node should keep neighborsize2 records of signal strength between these neighbors. Besides, at the very beginning of map establishment, we have to store beacon information (in event IMap.beaconReceive), which needs neighborsize records. Meanwhile, collection of beacon messages can be used as index table while IMap.get expects to find the value item in the map. To specify the sender and receiver of interference, every record contains Sender ID, Receiver ID and Signal Strength, where node ID needs 2 bytes while Signal Strength costs 1 byte. Overall, 5 neighborsize2 neighborsize bytes data memory is needed. In our evaluation experiments, we always set neighborsize as 16, thus the data memory overhead equals to 1.33 KB, which is small compared to 10 KB RAM in TelosB. (ii) To evaluate OPC’s ROM overhead, we first implement a simple application using CTP with the default CSMA protocol. Then, we compare this benchmark and the same one using additional interfaces in Section 5.1. The original benchmark consumes 20,442 bytes ROM while the modified version consumes 28,012 bytes. This indicates the OPC module consumes approximately 7.4 KB ROM, which is acceptable compared to 48 KB ROM in TelosB.

![](images/b9dca54ebc0d3321b698f366023358da6bfc538b3dee73a79570fd6a3e89a981.jpg)



Fig. 7. Indoor testbed.

# 5.2.2 Computational Overhead

OPC incurs computational overhead mainly in command TDecision.get. To be more specific, in TDecision. get, we repeatedly call IMap.get to search for the signal strength items in the map. As what described in Section 5.1, the size of map equals to neighborsize2 . With the index table of size neighborsize, every search operation at most checks 2\*neighborsize records. Overall, every search operation consumes at most 88 ms when neighborsize equals to 16. Usually, a transmission for data packet of size 40 bytes consumes about 2 ms, so the computational overhead is feasible to create transmission concurrency.

# 6 EVALUATION

We evaluate OPC through a real indoor testbed consisting of 60 TelosB motes (see Fig. 7) running CTP protocol, where CTP is a data collection protocol that dynamically selects the best route to the sink according to a hybrid link estimation algorithm [5]. We implement a CTP application similar to TestNetworkLpl, and the MAC protocol implements X-MAC to guide the nodes when to wake up and sleep. The evaluation will compare three MAC schemes: CSMA, OPC and NON-CSMA (i.e., always disabling carrier sense), to show that OPC is a practical design for the tradeoff between keeping out of the interference and transmitting concurrently. As we know, CSMA totally blocks transmission concurrency, while NON-CSMA omits the carrier sense procedure before a transmission. OPC is between these two extreme protocols, opportunistically choosing to transmit under interference. We design a series of experiments to show how OPC can be utilized to improve the performance of existing sensor network protocols and applications in terms of latency, throughput and power consumption. In addition, we also validate the potential opportunities of transmission concurrency in such a real testbed system.

![](images/116f135b7de09d4ad3a9e5b3ac102d2d89501cb854e6a948ee76f08a32411dd7.jpg)



Fig. 8. Potential benefit of OPC.

The transmission power of every packet is fixed as 2 and the retransmission count is four, which means a sender at most sends a packet for five times. All nodes have their own sleep periods on the basis of X-MAC. Preamble length is 500 ms. Note that, OPC also works with the other state-ofthe-art preamble-based MAC protocols. In every experiment, we discard the data in the first 20 minutes warmup time. Due to the observation that CTP usually needs some time to achieve reliable routing, we keep each experiment running for at least 1 hour. The SINR thresholds of SoI-last and SoI-first are set as 8 and 3 dB, respectively.

# 6.1 Basic Observation

We propose that our algorithm is needed, by showing that many transmissions will be blocked by other preamble or data packets. The experiment is repeated with a varying packet transmission interval, 5, 2 and 1 s. As shown in Fig. 8, there exist 8 percent 33 percent of intended transmissions blocked by an unclear channel. The percentage monotonically increases following transmission frequency and network scale. Significantly, when the data rate becomes one packet per second in a 60-node network, more than 30 percent of transmissions will be deferred at least once, which means OPC can avoid at least 10 percent of deferring transmissions if it works even only in one third of these opportunities. OPC gains more improvement to those packets needed to defer for many times. Actually, we didn’t just increase the data rate in the network to enhance the opportunities of concurrent transmissions. The packet reception ratio is maintained reliably, i.e., at least 75 percent of motes can flow the messages to the sink.

Fig. 9 describes how often the concurrency cases happen in our algorithm. How to count concurrent transmissions in OPC? In Fig. 4, the right part explains how OPC is embedded into current framework. Before every transmission, an event called InitialBackoff or CongestionBackoff is triggered, if the result TDecision.get() shows idle, this packet is allowed to send out. There are two possibilities in TDecision.get() = idle. One is that the result of CCA shows an idle channel; the other is that the channel is busy but concurrent transmission is allowed. The former part is in all the CSMA-based protocols, and the latter is implemented in OPC. So we focus on the transmissions under the latter kind of cases, where it counts the total number of concurrent transmissions. Here shows a period of 10 minutes. In fact, we find that the distribution is even dispersing, which is reasonable because X-MAC allows each node has an independent time schedule.

![](images/1027b8bc4a488e5d5d3b7e74c9c24e4cb385041b8e6fc988f39c82286e20b616.jpg)  
Fig. 9. Concurrency-time. Every black dot means a transmission concurrency. X-axis represents the time series, and y-axis denotes the node ID.

Fig. 10 plots the mote locations in our testbed, and the z-axis value represents the concurrency frequency. In our observation, most of the border nodes catch more opportunities of transmission concurrency, because they are more likely to transmit beyond weak interference and avoid hidden terminals, while the inner ones always suffer more complex and strong interference. In this figure, we also find that only 8 percent of deployed motes never benefit from OPC (including the nodes absent in the collection).

![](images/e49f4904289e91ecb3bf788b1c951a5aada0771b02680eb0fc09f900aac9146f.jpg)  
Fig. 10. Concurrency-location. Every location represents a sensor node. The sink locates at (1,2). There are four nodes which never trigger transmission concurrency.

![](images/fb63141e2081942559cb326760079b580ffa9f0334e8cbef262639da4f39b434.jpg)



Fig. 11. How many times a four-hop packet benefits from OPC. For every four-hop packet, it needs to be forwarded for four times, which means it can benefit from OPC for four times at most.

In addition, for each packet, we record the number of times it benefits from OPC. For a four-hop packet, it needs to be forwarded for four times, which means it can benefit from OPC for four times at most. In Fig. 11, we divide these four-hop packets into four groups according to how many times they benefit from OPC. The result shows that some packets are forwarded under an unclear channel for all four hops, which also validates that our algorithm significantly decreases some packets’ delay. Actually, in our experiments, every four-hop packet is forwarded under a busy channel at least once. Notably, almost every packet further than two hops benefits from OPC on the path to the sink.

# 6.2 Energy Consumption

In wireless sensor networks, a critical resource is energy [25]. To reflect the performance of energy consumption, we record the total time when radio is on. Fig. 12 presents that to complete the same collection task, OPC always costs less power. Following the network scale alternates, the reduction of duty cycle is from 5 to 10 percent compared to CSMA, from 18 to 33 percent compared to NON-CSMA. Meanwhile, OPC slightly increases the retransmission cases. Compared to CSMA, OPC needs 5 percent more transmissions. It is easy to understand: 1) we encourage the nodes to create transmission concurrency only within the local interference knowledge, so hidden terminal problem is out of our consideration; 2) the interference may be not totally correctly estimated; 3) our SINR thresholds may be not accurately determined.

# 6.3 Latency

We analyze the performance of packet latency to show that our algorithm indeed decreases the end-to-end delay. As what mentioned above, our work is under an asynchronous background, thus we need some extra effort to calculate the end-to-end delay. In our experiments, the base station sends time beacons to the motes through serial ports. The motes only make use of these beacons to revise the timestamp in packets, but do not cooperate to achieve network synchronization. To comprehensively present the performance on all sides, we analyze the variations of latency in different network scales, data rates and $C _ { m a x }$ respectively.

![](images/4426bc65cbe99605932079bc8027f687a7ba9994f1bf80e87419c72a2bb74280.jpg)



Fig. 12. Duty cycle. The time of radio on is recorded to explain the energy consumption. Here, we omit the energy consumption when the radio is off since it is relatively little.

Fig. 13a presents the latency in different network scales of 20, 40 and 60 nodes. Each node transmits 60 packets per minute. As the network scale expands, more multi-hop packets may suffer more inherent delay of duty cycle. OPC improves 9 perecnt in 20-node scale, while 17 perecnt in 60-nodescale compared to CSMA. Notably, it gains much more improvement compared to NON-CSMA. Fig. 13b presents the latency with varying data rates. As mentioned above, high data rate can create more opportunities of concurrent transmissions (though sometimes aggravates hidden terminal problem). When the data rate is low, since a data transmission only costs no more than 4 ms, thus few concurrent transmissions exist. Fig. 13c presents the latency under different max concurrency number $C _ { m a x }$ of 1, 2, 3 and 4 (i.e., CSMA, OPC-2, OPC-3 and OPC-4 in Figs. 13c and 13f). When we tolerate more concurrent transmissions, the performance adversely decreases. It is mainly caused by information asymmetry between different transmitters. In our recent work [12], more concurrent transmission decisions suffer more unexpected interference from hidden terminals.

# 6.4 Throughput

To show that our algorithm indeed improves the transmission opportunities, we further investigate the performance of throughput (i.e., the average number of successful transmissions per unit time). Fig. 13d presents the average throughput in different network scales of 20, 40 and 60 nodes. Fig. 13e presents the average throughput with varying data rates. Fig. 13f presents the average throughput under different max concurrency number $\bar { C } _ { m a x }$ of 1, 2, 3 and 4. Similarly, when the network scale expands or data rate increases, OPC creates more concurrent transmissions, thus increases the performance compared to CSMA and NON-CSMA. Specifically, OPC achieves an 9.4 percent addition in throughput. In practice, however, when we allow three or four transmissions concurrently proceed, collision mostly happens.

![](images/ad37490323dd5f56752258839bbffe04e9a4849ae57c0a46c6292fc2969ee6ef.jpg)



(a) Latency-scale

![](images/1ad4bda3edfba230f0d7373b9073772f936f00f64a7f192845fc36a3ca162b86.jpg)



(b)Latency-Transmiting frequency

![](images/da513ee7082b023bb6230762487e1ab73e008ae8cd92147e978264168a45aefd.jpg)



(c) Latency-Cmax

![](images/98884efceca194a1df981ad39bdf4821712243e3c1f67564b74f8900c11b0354.jpg)



(d) Throughput-Scale

![](images/a990fadeb5f249f2b6e934275f6aae02e518251dcd15c93db0f17bd66d7959d7.jpg)



(e）Throughput-Transmitting frequency

![](images/a8e2fd0c50f2ec6e455fbe6e18fbab2da0c33e19e2959ce2639838caede49ac5.jpg)



(f) Throughput-Cmax   
Fig. 13. End-to-end latency and throughput.

# 7 CONCLUSION

Traditional MAC protocols with CSMA strictly forbid concurrent transmissions. This paper presents OPC, a new MAC protocol exploiting concurrency to encourage the nodes to create concurrent transmissions. OPC is an assistant component that helps current MAC protocol make transmission decisions to improve network performance. In our decision making scheme, each node seeks the opportunities of concurrent transmissions based on a local concurrency map, even though the channel is detected as unclear. We implement OPC based on TinyOS 2.1. Real indoor testbed experiments running CTP application presents greatly potential benefits with OPC, and further shows that OPC actually achieves a 9.4 percent addition in network throughput, a 17 percent reduction in packet latency and a 10 percent reduction in energy consumption compared to traditional CSMA protocols.

# ACKNOWLEGMENTS

This research was supported in part by the NSFC program under Grant No. 61103187, NSFC Distinguished Young Scholars Program under Grant No. 61125202, NSFC Major Program under Grant No. 61190110, NSFC/RGC Joint Research Funding under Grant No. 61361166009.

# REFERENCES

[1] Chipcon cc2420 radios. (2014). [Online]. Available: http://www. ti.com/product/cc2420

[2] A. Acharya, A. Misra, and S. Bansal, “MACA-P: A MAC for concurrent transmissions in multi-hop wireless networks,” in Proc. IEEE 1st Int. Conf. Pervasive Comput. Commun., 2003, pp. 505–508.   
[3] M. Buettner, G. V. Yee, E. Anderson, and R. Han, “X-MAC: A short preamble MAC protocol for duty-cycled wireless sensor networks,” in Proc. 4th Int. Conf. Embedded Netw. Sensor Syst., Boulder, CO, USA, 2006, pp. 307–320.   
[4] S. Du, A. K. Saha, and D. B. Johnson, “RMAC: A routing-enhanced duty-cycle MAC protocol for wireless sensor networks,” in Proc. IEEE 26th Int. Conf. Comput. Commun., Anchorage, AK, USA, 2007, pp. 1478–1486.   
[5] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection tree protocol,” in Proc. 7th ACM Conf. Embedded Netw. Sensor Syst., Berkeley, CA, USA, 2009, pp. 1–14.   
[6] S. Gollakota and D. Katabi, “Zigzag decoding: Combating hidden terminals in wireless networks,” ACM SIGCOMM Comput. Commun. Rev., vol. 38, no. 4, pp. 159–170, 2008.   
[7] A. Gudipati and S. Katti, “Strider: Automatic rate adaptation and collision handling,” in Proc. ACM SIGCOMM Conf., Toronto, ON, Canada, 2011, pp. 158–169.   
[8] A. Gudipati, S. Pereira, and S. Katti, “AutoMAC: Rateless wireless concurrent medium access,” in Proc. 18th Annu. Int. Conf. Mobile Comput. Netw., Istanbul, Turkey, 2012, pp. 5–16.   
[9] D. Halperin, J. Ammer, T. Anderson, and D. Wetherall, “Interference cancellation: Better receivers for a new wireless MAC,” in Proc. ACM Wrokshop Hot Topics Netw., 2007, pp. 339–350.   
[10] D. Halperin, T. Anderson, and D. Wetherall, “Taking the sting out of carrier sense: Interference cancellation for wireless lans,” in Proc. 14th ACM Int. Conf. Mobile Comput. Netw., San Francisco, CA, USA, 2008, pp. 339–350.   
[11] K. Jamieson, B. Hull, A. Miu, and H. Balakrishnan, “Understanding the real-world performance of carrier sense,” in Proc. ACM SIG-COMM Workshop Exp. Approaches Wireless Netw. Des. Anal., 2005, pp. 52–57.   
[12] X. Ji, Y. He, J. Wang, W. Dong, X. Wu, and Y. Liu, “Walking down the stairs: Efficient collision resolution for wireless sensor networks,” in Proc. IEEE Conf. Comput. Commun., Toronto, Canada, 2014.

[13] A. Kochut, A. Vasan, A. U. Shankar, and A. Agrawala, “Sniffing out the correct physical layer capture model in 802.11b,” in Proc. IEEE 12th Int. Conf. Netw. Protocols, Boston, MA, USA, 2005, pp. 252–261.   
[14] J. Lee, W. Kim, S. J. Lee, D. Jo, J. Ryu, T. Kwon, and Y. Choi, “An experimental study on the capture effect in 802.11a networks,” in Proc. 2nd ACM Int. Workshop Wireless Netw. Testbeds, Exp. Eval. Characterization, 2007, pp.19–26.   
[15] J. Lee, S. J. Lee, W. Kim, D. Jo, T. Kwon, and Y. Choi, “RSS-based carrier sensing and interference estimation in 802.11 wireless networks,” in Proc. IEEE 4th Annu. Commun. Soc. Conf. Sensor, Mesh Ad Hoc Commun. Netw., San Diego, CA, USA, 2007, pp. 491–500.   
[16] L. Li, K. Tan, Y. Xu, H. Vishwanathan, and Y. Yang, “Remap decoding: Simple retransmission permutation can resolve channel collisions,” in Proc. 16th Annu. Int. Conf. Mobile Comput. Netw., Chicago, IL, USA, 2010, pp. 281–292.   
[17] Y. Liu, Y. He, M. Li, J. Wang, K. Liu, and X. Li, “Does wireless sensor network scale? A measurement study on greenorbs,” IEEE Trans. Parallel Distrib. Syst., vol. 24, no. 10, pp. 1983–1993, Oct. 2013.   
[18] J. Lu and K. Whitehouse, “Flash flooding: Exploiting the capture effect for rapid flooding in wireless sensor networks,” in Proc. IEEE Conf. Comput. Commun., Rio de Janeiro, Brazil, 2009, pp. 2491–2499.   
[19] J. Manweiler, N. Santhapuri, S. Sen, R. R. Choudhury, S. Nelakuditi, and K. Munagala, “Order matters: Transmission reordering in wireless networks,” in Proc. 15th Annu. Int. Conf. Mobile Comput. Netw., Beijing, China, 2009, pp. 61–72.   
[20] L. Mo, Y. He, Y. Liu, J. Zhao, S. J. Tang, X. Y. Li, and G. Dai, “Canopy closure estimates with greenorbs: Sustainable sensing in the forest,” in Proc. 7th ACM Conf. Embedded Netw. Sensor Syst., Berkeley, CA, USA, 2009, pp. 99–112.   
[21] T. Nadeem and L. Ji, “Location-aware IEEE 802.11 for spatial reuse enhancement,” IEEE Trans. Mobile Comput., vol. 6, no. 10, pp. 1171–1184, Oct. 2007.   
[22] J. Padhye, S. Agarwal, V. N. Padmanabhan, L. Qiu, A. Rao, and B. Zill, “Estimation of link interference in static multi-hop wireless networks,” in Proc. 5th ACM SIGCOMM Conf. Internet Meas., 2005, p. 28.   
[23] D. J. Perry and H. Balakrishnan, “Rateless spinal codes,” in Proc. 10th ACM Workshop Hot Topics Netw., article 6, 2011.   
[24] J. Polastre, J. Hill, and D. Culler, “Versatile low power media access for wireless sensor networks,” in Proc. 2nd Int. Conf. Embedded Netw. Sensor Syst., Baltimore, MD, USA, 2004, pp. 95–107.   
[25] M. N. Rahman and M. A. Matin, “Efficient algorithm for prolonging network lifetime of wireless sensor networks,” Tsinghua Sci. Technol., vol. 16, no. 6, pp. 561–568, 2011.   
[26] Y. Sun, O. Gurewitz, and D. B. Johnson, “RI-MAC: A receiver-initiated asynchronous duty cycle MAC protocol for dynamic traffic loads in wireless sensor networks,” in Proc. 6th ACM Conf. Embedded Netw. Sensor Syst., Raleigh, NC, USA, 2008, pp. 1–14.   
[27] T. van Dam and K. Langendoen, “An adaptive energy-efficient MAC protocol for wireless sensor networks,” in Proc. 1st Int. Conf. Embedded Netw. Sensor Syst., Los Angeles, CA, USA, 2003, pp. 171–180.   
[28] K. Whitehouse, A. Woo, F. Jiang, J. Polastre, and D. Culler, “Exploiting the capture effect for collision detection and recovery,” in Proc. IEEE 2nd Workshop Embedded Netw. Sensors, 2005, pp. 45–52.   
[29] W. Ye, J. Heidemann, and D. Estrin, “An energy-efficient MAC protocol for wireless sensor networks,” in Proc. IEEE 21st Annu. Joint Conf. Comput. Commun., New York, NY, USA, 2002, pp. 1567–1576.

![](images/1577533105f6787acda86f0b36446ba314b48c456ca71276f37f53dd28ceb8c3.jpg)



Qiang Ma received the BS degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2009, and the PhD degree from the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology, in 2013. He is currently a postdoc researcher at the School of Software, Tsinghua University, China. His research interests include sensor networks, network diagnosis, and mobile computing. He is a member of the IEEE.

![](images/d959cd39103f20c360d8d138e69ee968e5106847230c9783e96a3d7f0701bd2c.jpg)



Kebin Liu received the BS degree from the Department of Computer Science, Tongji University, in 2004, and the MS and PhD degrees from Shanghai Jiaotong University, in 2007 and 2010, respectively. He is currently an assistant researcher at the School of Software and TNLIST, Tsinghua University. His research interests include sensor networks and distributed systems. He is a member of the IEEE.

![](images/f1600bdb18e36e2e32a8b7e469f381e594396850864b76667ff08c8fca063474.jpg)



Zhichao Cao received the BS degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2009, and the PhD degree from the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, in 2013. He is currently a postdoc researcher at the School of Software, Tsinghua University, China. His research interests include sensor networking, network routing, and measurement. He is a member of the IEEE.

![](images/a67b818b772384ea2ad08d76c6b4e5bda9c755a0d9af0a0821027a5dca8e103a.jpg)



Tong Zhu received the BS degree from the Department of Computer Science and Technology, Nanjing University, China, in 2010, and the PhD degree from the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, in 2013. His research interests include sensor networking, measurement, and mobile computing. He is a member of the IEEE.

![](images/d4aced1bb15323bdbb9ba41c5b944a84dedc00eca03831b57bdc284d2596ef96.jpg)



Xin Miao received the BS degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2009, and the PhD degree from the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, in 2013. He is currently a postdoc researcher at the School of Software, Tsinghua University, China. His research interests include sensor networks and RFID. He is a member of the IEEE.

![](images/e8b0a2b819d1e0be0893e2277ea008e3f107f70009d856d03c540210392223ac.jpg)



Yunhao Liu received the BS degree from the Automation Department, Tsinghua University, China, in 1995, and the MS and PhD degrees from the Department of Computer Science and Engineering, Michigan State University, in 2003 and 2004, respectively. He is currently a Chang Jiang professor and the dean of School of Software, Tsinghua University, China. He is a senior member of the IEEE.   
" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.