# Duplicate Detectable Opportunistic Forwarding in Duty-Cycled Wireless Sensor Networks

Daibo Liu, Mengshu Hou, Member, IEEE, Zhichao Cao, Member, IEEE, ACM, Jiliang Wang, Member, IEEE, Yuan He, Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract—Opportunistic routing, offering relatively efficient and adaptive forwarding in low-duty-cycled sensor networks, generally allows multiple nodes to forward the same packet simultaneously, especially in networks with intensive traffic. Uncoordinated transmissions often incur a number of duplicate packets, which are further forwarded in the network, occupy the limited network resource, and hinder the packet delivery performance. Existing solutions to this issue, e.g., overhearing or coordination based approaches, either cannot scale up with the system size, or suffer high control overhead. We present Duplicate-Detectable Opportunistic Forwarding (DOF), a duplicate-free opportunistic forwarding protocol for low-duty-cycled wireless sensor networks. DOF enables senders to obtain the information of all potential forwarders via a slotted acknowledgment scheme, so the data packets can be sent to the deterministic next-hop forwarder. Based on light-weight coordination, DOF explores the opportunities as many as possible and removes duplicate packets from the forwarding process. We implement DOF and evaluate its performance on an indoor testbed with 20 TelosB nodes. The experimental results show that DOF reduces the average duplicate ratio by 90%, compared to state-of-the-art opportunistic protocols, and achieves 61.5% enhancement in network yield and 51.4% saving in energy consumption.

Index Terms—Duplicate-detectable, energy constraint, low-duty-cycled, opportunistic forwarding, wireless sensor network.

# I. INTRODUCTION

W IRELESS sensor networks [1]–[4] are usually duty-cy-cled to prolong the network lifetime. A widely adopted cled to prolong the network lifetime. A widely adopted low-duty-cycled media access mechanism is low power listening (LPL) [5]. Taking X-MAC [6] as a typical example of LPL, each node periodically wakes up and checks the received signal strength to detect the potential traffic. If the channel

Manuscript received March 15, 2014; revised September 19, 2014; accepted November 30, 2014; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor L. Qiu. This work was supported in part by the NSFC under Grants No. 61472067, No. 61472217, No. 61202359, and No. 61170213; the National Basic Research Program (973 program) under Grant No. 2014CB347800; the Key Technologies Research and Development Program of China under Grant No. 2013BAH33F02; the Key Technologies Research and Development Program of Sichuan Province under Grant No. 2013GZ0006; the National Science Fund for Excellent Young Scientist under Grant No. 61422207; and the NSF China Distinguished Young Scholars Program under Grant No. 61125202.

D. Liu and M. Hou are with the School of Computer Science and Engineering, University of Electronic Science and Technology of China, Chengdu 611731, China (e-mail: dbliu.sky@gamil.com; mshou@uestc.edu.cn).

Z. Cao, J. Wang, Y. He, and Y. Liu are with the School of Software, TNLIST, Tsinghua University, Beijing 100084, China (e-mail: caozc@greenorbs.com; wang@greenorbs.com; he@greenorbs.com; yunhao@greenorbs.com).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TNET.2014.2387440

is clear, it turns off the radio to sleep for a certain period. Note that the sleep schedule of different nodes is generally unsynchronized. A sender probably has to spend much time waiting for its corresponding forwarder to wake up. During the waiting time, the sender continuously transmits the same data packet (called preamble) until the preset timer expires or an acknowledgment is received. As a result, if the forwarder is deterministic, the end-to-end delay is likely high. Obviously, sender energy is wasted on waiting for the forwarder. The duty-cycled communication nature makes the deterministic forwarding schemes inefficient.

To shorten the waiting time, an intuitive idea is to take the earliest forwarding opportunity instead of waiting for the deterministic forwarder, like opportunistic routing [7]. Temporally available links may be exploited to reduce the transmission cost in wireless mesh networks. Landsiedel et al. propose ORW [8], an opportunistic forwarding protocol for low-duty-cycled unsynchronized sensor networks. In ORW, any forwarder with certain routing progress can acknowledge the preamble transmission in LPL. The first wake-up neighbor that successfully receives the packet is selected as the next-hop forwarder. Nevertheless, ORW cannot support high-traffic-load applications due to channel capacity degradation incurred by the inherent duplicate problem.

Most duplicate packets are generated when several forwarders keep awake and receive the same data packet during the same period. In low-duty-cycled sensor networks, the high traffic load will significantly increase the risk of producing duplicates. Although several duplicate suppression mechanisms are proposed [7]–[9], the overhearing-based approaches are not well adapted to the bursty traffic, especially in the large-scale networks with dynamic links. Moreover, according to MORE [10], the long coordination process diminishes the benefits brought by opportunistic routing. The amount of duplicate packets might increase exponentially along the multihop relay such that the network throughput is significantly degraded.

In order to address the above issues, we propose Duplicate-Detectable Opportunistic Forwarding (DOF). Instead of direct data transmission in LPL, a sender sends a probe and asks the potential forwarders to acknowledge the probe respectively in different time-slots. By utilizing the temporal diversity of multiple acknowledgments, the sender detects the quantity and differentiates the priority of all potential forwarders. The sender then forwards its data in the deterministic way to avoid multiple forwarders hearing the same packets. We develop methods to resolve possible collisions among multiple acknowledgments and exploit temporal long good links for opportunistic forwarding. With the lightweight mechanism to suppress duplicates, DOF can adapt to various traffic loads in duty-cycled sensor networks and enhances the system performance with respect to both network yield and energy efficiency.

The contributions of this work are as follows.

• Under the context of duty-cycled sensor networks, we extend the opportunistic routing to fit the needs of various traffic loads. This work presents a more comprehensive solution to low-duty-cycled opportunistic forwarding.   
• We propose DOF, a practical duplicate-free opportunistic forwarding protocol, by exploiting the temporal diversity of the acknowledgments. DOF minimizes the control overhead and improves the reliability of duplicate suppression. It can be easily extended to opportunistic routing in other networks.   
• We implement DOF and evaluate it on a testbed with 20 TelosB nodes. In high-traffic-load settings, the evaluation results show that DOF reduces the average duplicate ratio by 90%, compared to state-of-the-art protocols. Meanwhile, DOF achieves 61.5% enhancement in network yield and 51.4% saving in energy consumption.

The rest of the paper is organized as follows. Section II presents the motivation of this work. Section III introduces the system design and analysis, followed by its implementation and evaluation in Sections IV and V, respectively. We illustrate some uncertainty in Section VI. Section VII discusses the related work. Section VIII concludes this paper.

# II. MOTIVATION

In this section, we examine the performance degradation brought by inherent duplicates of state-of-the-art opportunistic routing in duty-cycled sensor networks. First, under different probabilistic models of traffic loads, e.g., Poisson and uniform distribution, we analyze the probability for multiple forwarders to wake up simultaneously under different network densities and protocol settings. Then, through testbed experiments of ORW, we show the relationship between the duplicates and system performance. Finally, we explain why the current duplicate suppression mechanisms are inefficient in duty-cycled sensor networks.

# A. Protocol Analysis

The forwarders that simultaneously keep awake may receive the same data packet. The number of duplicates goes up as the probability of multiple simultaneously waking forwarders increases. Due to the long preamble transmission of LPL, data forwarding with LPL significantly prolongs the waking time of the forwarders. Thus, the number of potential forwarders, the wake-up interval, and the traffic load may influence the probability of multiple forwarders being awake at one moment.

In the analysis, we assume each forwarder periodically wakes up every 512 or 1024 ms. The forwarder stays awake for 20 ms after it wakes up. The traffic model of a forwarder follows either Poisson or uniform distribution. indicates the average number of data packets passing each forwarder in 10 s. The time of the preamble transmission of individual data forwarding is calculated according to the traffic model. We simulate the data forwarding process to calculate the probability of multiple waking forwarders at one moment.

![](images/36a2e8b6aa06ef97e0a769551fc094118b93b39269fe2c22101c8ade2a47fe20.jpg)



(a)

![](images/bf357e64551539db32b7a32a85df0f48a9b90e4c2cb0fc0c1ab348f983ce7885.jpg)



(b)

Fig. 1. Probability of multiple waking forwarders at one moment under Poisson traffic model, with different number of potential forwarders and wake-up intervals. indicates the average traffic load of each forwarder (packets per 10 s). (a) Wake-up interval 512 ms. (b) Wake-up interval 1024 ms.   
![](images/4493900c391018e48eb289ead879e4080c2f0e0b61766327aee91d7640e8106c.jpg)



![](images/ee5d83863f24bab14047b5df4e0035b237ad93ad56d6f4e6e2239942bf5829b6.jpg)



(b)   
Fig. 2. Probability of multiple waking forwarders at one moment under uniform traffic model, with different number of potential forwarders and wake-up intervals. (a) Wake-up interval 512 ms. (b) Wake-up interval 1024 ms.

Figs. 1 and 2 show the probability distribution under Poisson and uniform traffic model, with wake-up intervals 512 ms [e.g., Figs. 1(a) and 2(a)] and 1024 ms [e.g., Figs. 1(b) and 2(b)], respectively. In both scenarios, the probability goes up with the increasing traffic load. For the same traffic load, the probability increases as the number of potential forwarders increases. Thus, the duplicates tend to appear in the areas with bursty traffic or high node density. With a longer wake-up interval (increasing from 512 to 1024 ms), the probability changes little, indicating the influence of wake-up interval on the probability is not obvious. This is because for a longer wake-up interval, each node needs to keep the radio on for a longer time to send packets to the forwarder. This increases the probability that multiple forwarders are simultaneously awake. However, the longer duration of packet transmission also makes a sender easily batch its packets and transmit all of them when the forwarder wakes up. This will decrease the total wake-up period of the individual node. Thus, the trend of the probability under different wake-up intervals looks almost the same. Compared to wake-up interval, the traffic load and the number of potential forwarders dominate the probability that multiple forwarders keep awake simultaneously. Specifically, in both Figs. 1(a) and 2(a), when the average traffic load is 1 packet/s ( ) and there are six potential forwarders, the probability of multiple simultaneously waking forwarders is about 30%–50%. This is much higher than that in the low-traffic-load setting in ORW [8] (when every node generates a packet randomly with an average interval of 4 min, ORW reports the probability that multiple forwarders receive the same packet is about 10%).

![](images/c94dd898b631315b152e464c7beb89f1439b38e581eb48d96267fa2db5cdf7ff.jpg)

![](images/1828a8fb7cb9d41e970bf33ad35db9310caba110a75b5f99d953e856d783eac3.jpg)  
Fig. 3. Cumulative distribution function (CDF) of the duplicate ratio, radio duty-cycle, and packet reception ratio with different traffic loads on testbed experiment, when the wake-up interval is set to (a) 512 and (b) 1024 ms, respectively.

TABLE I DISTRIBUTION OF THE TRAFFIC LOAD CARRIED BY EACH NODE WITH 512-ms WAKE-UP INTERVAL 

<table><tr><td rowspan="2">Inter Packet Interval (IPI) (s)</td><td colspan="3">Average Traffic Load (packets/10s)512ms Wake-up Interval</td></tr><tr><td>Minimum</td><td>Median</td><td>Maximum</td></tr><tr><td>20</td><td>0.55</td><td>1.26</td><td>7.2</td></tr><tr><td>10</td><td>1</td><td>1.80</td><td>8.14</td></tr><tr><td>4</td><td>2.41</td><td>5.05</td><td>17.78</td></tr><tr><td>2</td><td>5.02</td><td>11.03</td><td>28.81</td></tr></table>

TABLE II DISTRIBUTION OF THE TRAFFIC LOAD CARRIED BY EACH NODE WITH 1024-ms WAKE-UP INTERVAL 

<table><tr><td rowspan="2">Inter Packet Interval(IPI) (s)</td><td colspan="3">Average Traffic Load (packets/10s)1024ms Wake-up Interval</td></tr><tr><td>Minimum</td><td>Median</td><td>Maximum</td></tr><tr><td>20</td><td>0.49</td><td>0.83</td><td>4.36</td></tr><tr><td>10</td><td>1.02</td><td>1.90</td><td>6.11</td></tr><tr><td>4</td><td>2.27</td><td>4.95</td><td>17.77</td></tr><tr><td>2</td><td>4.98</td><td>7.33</td><td>18.21</td></tr></table>

# B. System Measurement

Based on the implementation of ORW in TinyOS, we further evaluate the influence of duplicates on a testbed with 25 TelosB nodes. We set the radio power at 1 in TinyOS, and the wake-up interval is 512 or 1024 ms. On the testbed, the minimum, median, and maximum number of available next-hop forwarders of different nodes are 1, 5, and 11, respectively. The average length of routing paths is 2.08 hops. The maximum length is 7 hops. Each node generates data periodically. We select four different traffic loads with the interpacket interval (IPI) to be 2, 4, 10, and 20 s, respectively. The actual distribution of the traffic load is shown in Tables I and II, respectively.

According to the sequence number of the data packets received by sink, we take the duplicate ratio, i.e., the number of duplicates to the number of different packets received, as the metric of duplicates. According to Fig. 3, by setting different wake-up intervals, the duplicate ratio is low when the traffic load is low. It increases quickly with the increase of traffic load, and the maximum duplicate ratio reaches 200%. When the IPI is 2 s, the duplicate ratio of over 50% of nodes is higher than 100%.

We then take the radio duty-cycle as the energy consumption indicator for a node. We can see a significant increase of the radio duty-cycle when the duplicate ratio increases. When the IPI is 2 s, the radio duty-cycle of over 40% of nodes is higher than 60%. About half of the energy is wasted on the transmission of duplicates. According to packet reception ratio (PRR) of Fig. 3(a) and (b), we can see the PRR stays stable when the packet interval is 4 s, but it decreases quickly when the traffic load gets higher. The main cause of packet drops is forwarding queue overflow, where the queue size is 10.

The experiments show that many duplicates indeed exist with the state-of-the-art low-duty-cycled opportunistic routing protocols, especially when the traffic load is high. Moreover, the duplicates significantly degrade the system performance and should be avoided.

# C. Duplicate Suppression Mechanism

Most existing duplicate suppression mechanisms are based on overhearing. When a forwarder overhears a packet, which is identical to a pending packet in the forwarding queue, it deletes the packet from the queue. However, in current sensor operating systems like TinyOS, the nonpreemptive task abstraction does not allow a node to interrupt on ongoing transmission tasks. Moreover, the bursty traffic, especially in large-scale networks with dynamic links, further makes a forwarder hard to exactly overhear every packet relayed by others.

To further reduce duplicates in the bursty traffic, packet transmissions are coordinated among different nodes in the network. For example, ExOR [7] arranges the forwarding order according to the routing progress and the quantity of received data packets. According to MORE [10], however, the coordination process introduces extra overhead. Moreover, the coordination restricts concurrent transmissions and hence reduces the network yield.

We want to develop a forwarding approach, which can detect the simultaneous waking-up forwarders and inherently avoid the duplicates. Meanwhile, the forwarding approach keeps the spatial diversity of the opportunistic routing as much as possible.

![](images/3fe8c6a6942f6e658cf0751dd5dc1a83eb8122331302f7d6439b81566dc35a98.jpg)



![](images/9561c543925cedbe5d8294dbbe1993d5ad12dc09328e47d293a60f78cd923977.jpg)



(b)

![](images/0265bf6a5d97a8a756d0ffcc493794afe97cfc805fd37cd45cd18f42840ca0db.jpg)



（c）

![](images/0bc5daa6d126c6fc964795bcd36e890365d8ebe71bf8b1c5b77c79d23c442b14.jpg)



(d）  
Fig. 4. Different from deterministic forwarding and ORW, in DOF the sender distinguishes the multiple waking forwarders by the temporal diversity of ACKs. Then, it sends the data packet to an exclusive forwarder by adding in the ACK slot information. (a) Topology. (b) Deterministic forwarding. (c) ORW. (d) DOF.

# III. SYSTEM DESIGN

DOF targets on developing a practical opportunistic forwarding scheme for various duty-cycled sensor network applications. In this section, we discuss several issues: 1) the overview of how DOF detects the potential forwarders by slotted acknowledgment (ACK); 2) the algorithm of ACK slot assignment and forwarding strategy; 3) the adaptive routing metric. For simplicity, we here illustrate the basic design of DOF using X-MAC, a well-adopted unsynchronized LPL MAC as we mentioned above.

# A. Overview of DOF

As Fig. 4(a) shows, sends packets to the intended destination (a destination is the final receiver like the sink node). There are three potential forwarders , , and (a forwarder is one relay node along the routing path). The links are either reliable or bursty, indicated as the solid or dashed lines, respectively.

As Fig. 4(b) shows, in traditional deterministic forwarding, continuously sends the data to the predetermined relay node until it wakes up. As Fig. 4(c) shows, ORW takes the early wake-up nodes ( , , or ) that receive the data and provide routing progress as the next-hop forwarder. However, as Fig. 4(c) shows, , , and may receive the data simultaneously. The duplicates then significantly degrade the system performance as introduced above.

DOF detects potential duplicates by using adaptive slotted ACK when multiple forwarders are awake simultaneously. As Fig. 4(d) shows, instead of directly sending data, a sequence of probes is first broadcast by . The interval of two adjacent probes is divided into multiple time-slots. Each slot is long enough to receive an ACK. When , , and receive one probe and any of them offers routing progress, each of them independently selects a slot (2, 0, and 4) to send the ACK back. According to the slot information of the received ACKs (0 and 4), sends the data packet to a forwarder ( ) by adding in the slot information (0).

To minimize the duplicates and keep the benefit of opportunistic routing, the design of DOF faces several challenges: 1) Different forwarders should acknowledge the probe at different slots. In addition, the routing progress of different forwarders should be distinguished because the forwarder with more routing progress should be used with a higher priority. 2) Although the communication overhead caused by probe transmissions for each data packet is little, it should be avoided when the traffic load is high. 3) DOF may explore temporally available links to forward data. However, the data ACK loss over these links may lead to undesirable retransmissions due to the bursty loss. Thus, the short-term link performance should be considered.

![](images/c99234b9150567419dddcef07fe3ed66bcd56da87a887a5d77e5c71d0278aa57.jpg)



Fig. 5. DOF splits all the ACK slots into three slightly overlapped priority zones. According to the routing progress, DOF randomly maps each forwarder into a slot in different priority zones.

# B. ACK Slot Assignment

As we mentioned in Section III-A, the two requirements of ACK slot assignment are that multiple forwarders should be distributed into different slots, and the sender should infer the routing progress of different forwarders by ACK slot distribution. As Fig. 5 shows, the basic strategy is as follows: First, according to a hash function, the forwarder matches its routing progress $\Delta$ to a location $H _ { s f }$ on the priority sequence. The priority sequence is like a ruler to measure the routing progress; then, we split all the ACK slots into multiple slightly overlapped zones, which are matched to different segments of the priority sequence (e.g., zone ); last, according to $H _ { s f }$ , we randomly assign one slot in the selected zone.

There are six parameters in the calculation procedure, as shown in Table III. When forwarder receives the probe sent by $s ,$ the routing progress is calculated by

$$
\Delta_ {s f} = W _ {s} - W _ {f}. \tag {1}
$$

$W _ { s }$ is carried in the probe, and $W _ { f }$ is local routing information. If $\Delta _ { s f }$ is larger than $\Delta _ { \mathrm { m a x } } .$ , we set it as $\Delta _ { \mathrm { m a x } }$ . By (2), the routing progress $\Delta _ { s f }$ is mapped to a location $H _ { s f }$ in the priority sequence. A forwarder with a larger routing progress is mapped into the head area of the sequence

$$
H _ {s f} = \left\lfloor \left(1 - \frac {\Delta_ {s f}}{\Delta_ {\max}}\right) * N \right\rfloor . \tag {2}
$$

TABLE III DESCRIPTION OF THE SYMBOLS IN THE ACK ASSIGNMENT ALGORITHM. 

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $W_s$ </td><td>the routing metric value of the source node</td></tr><tr><td> $\Delta_{max}$ </td><td>the maximum routing progress over one hop</td></tr><tr><td>N</td><td>the total length of the priority sequence</td></tr><tr><td>M</td><td>The total number of ACK slots</td></tr><tr><td>L</td><td>the number of priority zone of ACK slots</td></tr><tr><td>R</td><td>the number of ACK slots in each priority zone</td></tr></table>

calculates in which ACK zone $( z o n e _ { f } )$ it should acknowledge the probe and the offset $( \delta _ { f } )$ in the segment of priority sequence corresponding to

$$
\text { zone } _ {f} = \left\lfloor \frac {H _ {s f} \cdot L}{N} \right\rfloor \tag {3}
$$

$$
\delta_ {f} = H _ {s f} - \left\lfloor z o n e _ {f} \cdot \frac {N}{L} \right\rfloor . \tag {4}
$$

randomly maps $H _ { s f }$ into the final ACK slot, $s l o t _ { f }$ , as the following equation shows:

$$
\operatorname{slot} _ {f} = \text { zone } _ {f} \cdot \left\lfloor \frac {M}{L} \right\rfloor + \left\lfloor \frac {\delta_ {f} \cdot L \cdot R}{N} \right\rfloor + \operatorname{rand} () \tag {5}
$$

where is a random number between 0 and . If $s l o t _ { f }$ is larger than , we make $s l o t _ { f }$ equal to .

Let us take Fig. 5 as an example. We assume $L , \Delta _ { \operatorname* { m a x } } , N ,$ , and are 3, 5, 30, 10, and 4, respectively. If the forwarder provides routing progress $\Delta _ { s f }$ as 2.8, the location of priority sequence, $H _ { s f }$ , equals to 13. Then, and $\delta _ { f }$ are 1 and 3. If we assume the random number is 3, the will be the seventh slot.

In our design of Fig. 5 with a small number of ACK slots (10), by using overlapping zones, the number of ACK slots in each zone will be enlarged. Thus, the probability that several forwarders with similar routing progress choose the same ACK slot will be reduced. Moreover, the size of overlapping slots between two adjacent zones is small. With our random mapping algorithm, the probability that several forwarders that select different zones choose the same ACK slot is small.

Note that there are still chances (with very small probability) that the ACKs from multiple forwarders collide. On one hand, if the sender still receives other ACKs distributed in different slots, DOF will ignore the collision and select the forwarder that sends the earliest coming ACK. On the other hand, if the sender has not received any ACK, it will keep transmitting the probe to find other forwarding opportunities.

Rather than assigning each forwarder a fixed ACK slot, our method is more flexible to utilize all temporarily available links. Moreover, the parameters of our method are predetermined based on the local routing information so that there is no extra communication overhead. The computation complexity of the algorithm is $O ( 1 )$ . However, this algorithm does not guarantee that multiple forwarders do not choose the same ACK slot. We show in practice this situation rarely happens in Section IV.

# C. Forwarding Management

Note that a forwarder may serve multiple senders during a short period. Each forwarder maintains a sender table, which records the ACK slot information to trace the potential senders. Each entry of the sender table includes the following: the sender's address, expected data sequence number (DSN), and the selected ACK slot.

When a probe is received, the forwarder first checks the attached routing metric $W _ { s }$ of the sender . If the forwarder can provide routing progress $( \Delta _ { s f } > 0 )$ , it selects an ACK slot $o t _ { f }$ to acknowledge the sender. Then, if there is a record of the same sender, the forwarder updates the corresponding record in the sender table. Otherwise, the forwarder adds a new entry into the table. Note that the DSN attaching in the received probe copies that of the sender's pending data packet. Upon the acknowledged probe, the sender attaches the DSN and the selected ACK slot number as the virtual intended forwarder address. When the forwarder receives a data packet, it queries the sender table. If there is no matched entry, the forwarder drops the packet and does nothing. Otherwise, it will take the responsibility to forward the data packet.

Moreover, although the forwarder acknowledges the received probe, it still receives the duplicate of the same probe. The probe duplicate indicates the sender has not received the ACK for the previous probe due to the asymmetric link or link dynamics. Considering that the ACK collision rate is low by using ACK slot assignment and the potential forwarders are sufficient, DOF makes a tradeoff between making full use of the forwarders in awake state and decreasing the impact of link burstiness and link asymmetry on energy consumption. If the forwarder receives the duplicate probe, it goes back to sleep to save energy.

On the other hand, the sender may receive multiple ACKs distributed in different slots after sending a probe. According to our ACK slot assignment algorithm, the forwarder corresponding to the earlier coming ACK provides relatively high routing progress. Thus, the sender inserts the DSN and the minimum slot number of ACK received to the pending data packet and sends it.

When the sender prepares to send a batch of packets, the intended forwarder will keep awake during the batched sending. Besides the probes of the first packet, the probes of the rest of the packets are not needed. Thus, to save the extra overhead of the probe transmission, the sender directly sends the rest of the packets with the connection (called Tunnel) found by the probes of the first packet until either the loss of data ACK or there are no pending data packets.

When the pending data packet is acknowledged, the sender finishes this transmission. However, because of the lossy link or misalignment of the probe ACK slots, the sender may not receive the data ACK from the intended forwarder. Hence, with a larger retransmission limit is inadvisable. Whether we should keep retransmitting the data packet or send a probe again to detect new forwarders is an important problem for the agility and efficiency of the protocol. According to [11] and [12], the packet loss tends to be bursty over temporally available links. We propose the Limited Retransmission Strategy (LRS) to address the data ACK loss. The basic idea is to estimate the available period of those links and then adaptively bound the number of retransmissions. The specific setting of LRS is shown in Section IV.

# D. Low-Duty-Cycled Opportunistic Routing

In DOF, a packet is sent to one of the waking neighbors, which provides certain routing progress. As a result, the routing topology toward the sink is not fixed. A packet may be forwarded to the sink along different paths. Moreover, considering the unsynchronized sleep schedule in LPL, DOF drives two requirements on routing. First, the routing metric should reflect the waiting time of the link-layer transmissions. Second, each node should adaptively choose a set of forwarders from all neighbors to determine the local routing metric.

Considering the two requirements above, expected duty-cycle (EDC), which is introduced by ORW [8], acts well on the whole. Hence, we adopt the concept of EDC as the routing metric. Our method of duplicate detection can be easily built on other routing metrics as well, such as end-to-end delay or ETX [13].

Briefly, EDC is an adaptive metric of ETX for opportunistic routing in duty-cycled wireless sensor networks (WSNs). EDC describes the expected number of wake-up intervals from the beginning of the transmission to the sink along multihop relay. Hopefully, in unsynchronized duty-cycled schedule, multiple next-hop routing choices decrease the expected waiting time to successfully send the packet to any of them.

For node , giving the next-hop forwarder set $\mathbf { F _ { i } }$ and the quality $q _ { i j }$ of the link with next-hop forwarder $j ~ ( j ~ \in ~ \bf { F } _ { i } )$ , it defines the single-hop EDC as the inverse of the sum of the link quality of all forwarders in $\mathbf { F _ { i } } ,$ as follows:

$$
\mathrm{EDC} _ {i} (1) = \frac {1}{\sum_ {j \in F _ {i}} p _ {i j}}. \tag {6}
$$

This indicates how many units of time it requires on average to send a packet to one of the forwarders in $\mathbf { F _ { i } } .$ . It further defines the by adding the routing progress the $\mathbf { F _ { i } }$ offer, as follows:

$$
\mathrm{EDC} _ {i} (F _ {i}) = \mathrm{EDC} _ {i} (1) + \frac {\sum_ {j \in F _ {i}} p _ {i j} \mathrm{EDC} _ {j}}{\sum_ {j \in F _ {i}} p _ {i j}} + \omega . \tag {7}
$$

The illustrates the cost of forwarding. The could balance the system performance and the routing stability. The larger leads to a smaller forwarder set, so that makes the routing more stable, but it might incur larger delay and energy waste. However, low also increases the risk of temporary routing loops. These are specifically illustrated in [8].

Taking Fig. 6 as an example and setting as 0, in the left case, has a single forwarder with a perfect link. The $\operatorname { E D C } _ { S }$ is $1 / 1 + 1 \times 1 / 1 = 2$ . In the middle case, has two forwarders, and , with link quality 1 and 0.5. Its $\operatorname { E D C } _ { S }$ is $0 . 5 ) + ( 1 \times 1 + 0 \times 0 . 5 ) / ( 1 + 0 . 5 ) \approx 1 . 3 3 $ .

One left essential problem is how to determine the forwarder set $\mathbf { F _ { i } }$ from all neighbors. First, [8] sorts all of the neighbors by their EDC value from small to large. Then, [8] continuously adds the neighbors by the sorted order to $\mathbf { F _ { i } }$ until $\mathrm { E D C } _ { i }$ reaches the minimum. As the right case of Fig. 6 shows, if the forwarder set of contains and , the $\operatorname { E D C } s$ is 1.33. If adding into $\mathbf { F _ { S } }$ , the $\operatorname { E D C } _ { S }$ will be 1.25, which is less than the previous . Thus, should be added into $\mathbf { F _ { S } }$ . While adding into $\mathbf { F _ { S } }$ , the $\operatorname { E D C } s$ will be 1.5, which is larger than the previous $\operatorname { E D C } _ { S }$ . Thus, the should not be added into $\mathbf { F _ { S } }$ . Because the sender only selects the nodes that provide strictly more routing progress than itself, the resulting topology is convergent and forms a loop-free graph.

![](images/c82cacf9103788535f0c9c5b72f385ff46de2915d20de53da7fec359100a77f2.jpg)



Fig. 6. Illustration of the computation of EDC.

# IV. IMPLEMENTATION

We implement DOF on TelosB nodes in TinyOS 2.1.1. The RAM and ROM consumption of the program are 6268 and 39 714 B, respectively. Next, several implementation issues are carefully discussed.

# A. ACK Slot Settings

For the forwarder, when the radio (CC2420) has received a packet, it will generate an interrupt (FIFOP) to trigger the handler function. Meanwhile, for the sender, it will also generate an interrupt (falling-edge SFD) when the transmission has finished. We neglect the propagation delay so that the FIFOP interrupts of the probe on different forwarders happen simultaneously. Thus, we take the simultaneous interrupts as the beginning of ACK response for the sender and forwarders.

When the FIFOP interrupt is generated, the forwarder calculates its ACK slot $K _ { f }$ and sends the ACK after $K _ { f } T _ { \mathrm { s l o t } }$ time, where $T _ { \mathrm { s l o t } }$ is the slot time span. Upon receiving the ACKs from different forwarders, the sender needs to determine the slot number for different forwarders. Since the ACK slot calculation and ACK reception take a certain time, there is a shift between the time the probe is sent and the time the first ACK is received. We denote the shift between the earliest received ACK (i.e., the ACK sent in the first slot) and the falling-edge SFD interrupt as $T _ { \mathrm { b a s e . } } T _ { \mathrm { b a s e } }$ is close to a constant time. In our implementation, the measured $T _ { \mathrm { b a s e } }$ is about 2.3 ms. Thus, according the interval $T _ { r }$ from the falling-edge SFD interrupt to the ACK received, the sender calculates the slot number $K _ { s }$ as

$$
K _ {s} = \left\lfloor \left(T _ {r} - T _ {\text { base }}\right) / T _ {\text { slot }} \right\rfloor \tag {8}
$$

where $K _ { s }$ should equal $K _ { f }$ . If the maximum ACK waiting duration is $T _ { \mathrm { m a x } } .$ , the maximum number $s l o t _ { \mathrm { m a x } }$ of the ACK slots is calculated as

$$
\operatorname{slot} _ {\max} = \left\lfloor \left(T _ {\max} - T _ {\text { base }}\right) / T _ {\text { slot }} \right\rfloor . \tag {9}
$$

In practice, the clock drift and the variance of the software execution time will incur the mismatch between $K _ { f }$ and $K _ { s }$ .

![](images/77f92a304e819b871ca6fa5f7c5d0097a256b9a7714d547eefdcd30716fc6447.jpg)



Fig. 7. Relationship between the ACK slot time span and the prediction accuracy.

![](images/4f8117c9d24dec257f893bf72a5b99be1ef0a0ef2e0009a2c919be6e6c0371b4.jpg)



Fig. 8. Clock drift as temperature changes.

Assume the clock drift between the forwarder and sender is $\sigma ,$ a mismatch only occurs when

$$
\sigma T _ {r} \geq T _ {\text { slot }}. \tag {10}
$$

Thus, increasing the slot time span reduces the probability of mismatch, while it limits the number of available ACK slots. In practice, the less available ACK slots might increase the probability that multiple receivers choose the same ACK slot.

We conduct experiments to show the prediction accuracy and the average time variance with different slot time spans. In the experiments, two senders transmit packets to the same receiver in the office environment. The results are shown in Fig. 7. We can see the predication accuracy is close to 100%, when the slot time span is larger than 0.1 ms. The average variance is relatively stable, about 0.5 jiffy ( jiffy ms). Considering the more complicated environment in practice, the slot time span is conservatively set as 0.2 ms, and the total number of ACK slots is 10.

Moreover, we measure the clock drift under different temperatures between a pair of nodes. We use two TelosB nodes to record local time every 5 s under different temperatures. Using the recorded data, we use the least-squares fitting method [14] to calculate clock drift. As Fig. 8 shows, the clock drift goes up when temperature rises from hour 11 to hour 13. The clock drift is less stable when the temperature is higher than $3 5 ^ { \circ } \mathrm { C }$ . The maximum clock drift is about 140 ms per minute (about 0.0023 ms per 1 ms). Under the above settings, the maximum ACK waiting duration is about 4.3 ms. Thus, the maximum variance incurred by the clock drift is about 0.009 ms, which is far less than 0.2 ms.

# B. Data ACK Loss and Retransmission

As Section III-C mentioned, the data ACK may be lost due to the mismatch of the probe ACK slot between sender and forwarder or link dynamics. Fig. 9 shows the data ACK loss rate when multiple senders send packets periodically to the same receiver. The data ACK loss ratio is no more than 3% with different numbers of senders. In DOF, the sender opportunistically utilizes the temporally available links, for which the probe ACKs have been successfully received. Thus, the data ACK loss is rare in the experiments. The probe ACK loss will reduce the available opportunities, but not degrade the reliability when the firm links exist.

![](images/f59c11fb04a2bc20246b8de0de233ae75b8896113ded4142443d9435c2d49e13.jpg)



Fig. 9. Situation of data ACK loss with multiple senders.

![](images/3e5b4c78b8fc6c7b7c51b527e5315c4fced3fa2bc143320f4b8976c01e4ab0e7.jpg)



Fig. 10. Average transmission count of the successfully delivered packet.

Due to the possible bursty loss, we propose the limited retransmission strategy (LRS) to bound the number of data retransmissions. To determine the maximum retransmission count in practical networks, we make multiple senders send packets to the same receiver. For each packet, the maximum number of retransmission count is initially set to 10. The packet will be dropped when the retransmission is larger than 10. We measure the average transmission count of the successful data transmissions of all senders. As shown in Fig. 10, the average transmission count of a successful transmission is smaller than 2. Thus, we set the transmission threshold as 2. When the sender does not hear the ACK, it will retransmit the data packet once. If the retransmission also fails, the sender will broadcast the probe to find the available forwarder again.

# C. Tunnel Transmission

The probe is utilized to detect the potential forwarders. As Section III-C mentioned, when there are several packets in the forwarding queue, the sender will take the tunnel transmission to save the energy consumption on the probe transmission. Fig. 11 shows the ratio between the number of tunnel transmissions and total data transmissions for different traffic loads on a testbed experiment with 20 TelosB nodes. We could see for high traffic loads the portion of tunnel transmission ratio is high.

![](images/132c6cb959f0cbae0fe5b559bc2cbc149320c72262a81e89778161640971fec8.jpg)



Fig. 11. Ratio of tunnel transmissions over the total transmissions under different traffic loads.   
![](images/4c42d3ce896beb30070ce9cba3498191c7caabc1a7eeb75a3550915f7c8109ec.jpg)



Fig. 12. Duplicate ratio of DOF slot assignment algorithm compared to the ideal assignment.

Especially, over 50% of transmissions are tunnel transmissions when the interpacket interval is 1 s.

# D. Slot Assignment

As mentioned in Section III-B, the slot assignment algorithm of DOF may map different forwarders into the same ACK slot. In this situation, it is possible that multiple forwarders receive the same packet so that duplications occur. We compare our algorithm to the ideal slot assignment, in which we manually assign a unique ACK slot for each of the forwarders. Fig. 12 shows that, in practice, the duplicate ratio of our slot assignment algorithm is just a little higher than the ideal method. The duplicate in the ideal assignment algorithm is induced by the data ACK loss. In such a case, the sender will transmit the data packet again to a new forwarder, while the previous forwarder actually has received the packet.

In summary, we show the details of the implementation settings in Table IV.

# V. EVALUATION

In this section, we evaluate DOF through various testbed experiments. We compare the network yield, energy consumption, and duplicate ratio of DOF to two unsynchronized low-duty-cycled forwarding protocols such as ORW and CTP-XMAC. We also compare the performance of DOF to CTP-AMAC [15], which is the-state-of-art synchronized receiver-initiated low-duty-cycled protocol. In addition, considering the system stability under network churns, we compare DOF to $L ^ { 2 }$ [16], which is proposed to optimize the energy efficiency by incorporating with the synchronized rendezvous, link burstiness, and dynamic forwarding.

We use the PRR as the indicator of the network yield. It also indicates the network throughput combining with the interpacket interval. In our implementation, the on-board sensor and flash memory is rarely used, and thus the radio consumes most of the energy [17]. The energy consumption is measured by the radio duty-cycle. Moreover, we use the average preamble count to approximate the delay. In CTP-XMAC and ORW, it is the average number of the data transmissions. In DOF, it is the sum of the probes and data transmissions on average. Normally, the smaller the average preamble count is, the less the delay is.

![](images/29f0e811102923f15d7f4260a9d0f7323b0f119014ef6394931686c185a4abd8.jpg)



Fig. 13. Topology of indoor testbed. Twenty TelosB sensor nodes are selected in the experiments, ensuring multihop communication.

TABLE IV SYSTEM PARAMETERS 

<table><tr><td>Parameters</td><td>Value</td></tr><tr><td>M</td><td>10</td></tr><tr><td>L</td><td>3</td></tr><tr><td>R</td><td>4</td></tr><tr><td>N</td><td>30</td></tr><tr><td>Slot time span</td><td>0.2ms</td></tr><tr><td>LRS threshold</td><td>2</td></tr><tr><td> $\Delta_{max}$ </td><td>3</td></tr></table>

# A. Evaluation Setup

We evaluate the performance of different forwarding protocols on an indoor testbed (Fig. 13) with 20 TelosB sensor nodes. We set the transmission power of CC2420 as 1 to ensure multihop communication (maximum hop is 3).

Each node generates packets with a fixed IPI. We vary the traffic load by setting different IPIs, such as 1, 2, 4, 8, and 16 s. The packet length is 80 B. Thus, the wake-up interval of other protocols is set to 512 ms, except AMAC, which is set to the default setting 128 ms. For each traffic load, the experiments last for at least 30 min and are repeated three times. The experiments are often conducted during the night to mitigate the influence of the human behavior.

# B. Network Yield

Fig. 14(a) shows the experiment results of the average PRR for different forwarding protocols with different traffic loads. We can see that when the IPI is no less than 8 s, the packet loss of all forwarding protocols is small. However, with the decreasing of IPI, the PRR of ORW, CTP-AMAC, and CTP-XMAC sharply decreases from 95% to less than 50%. In contrast, the PRR of DOF is still higher than 90% and 70% when the IPI is 2 and 1 s, respectively. When the IPI is 1 and 2 s, the network yield of DOF is about 46.5% and 61.5% higher than the best of ORW, CTP-AMAC, and CTP-XMAC.

![](images/b2d47b487be2014ec3717123ec211a4c782941c3195ab670b8a8c08bac85170f.jpg)



(a)

![](images/c2cc4e0e5db5dd3fd1f930bee75666a31d6d8a4afcfee1772c81a20eb9d120bd.jpg)



(b)

![](images/db3292552fb37fe731b59800e925ff4fd2cae11513c4893ad23642844b9f2854.jpg)



(c）

![](images/b2ab1faff428e1194a6a1f12cbf1cff937df9553d32fd39f4d9f72f004d3ccab.jpg)



(d）

Fig. 14. Overall comparison of different system performance metrics between DOF and the other forwarding protocols. (a) Packet reception ratio. (b) Radio duty-cycle. (c) Duplicate ratio. (d) Average preamble count.   
![](images/a400cebb8481374d3873bb61b3f8b18e5baf6626219840d3653323dd6623b7d6.jpg)



(a）

![](images/e38816d7c3d420df8f013915a19d61d7fdd49d9c97c856f6e164232ddaf64fd6.jpg)  
(b)

![](images/460aa0bc80774b4fcae674d7c02739718ccb174700791bd782b1d3aa11069e71.jpg)



（c）  
Fig. 15. Per-node comparison of different system performance metrics between DOF and the other forwarding protocols in high traffic loads. (a) s. (b) s. (c) s.

The significant decreasing of PRR in a high traffic load is due to the inefficient channel utilization. In CTP-XMAC, each sender will occupy the channel for a long time until the intended receiver wakes up. As shown in Fig. 14(d), the average preamble count of CTP-XMAC is much larger than both ORW and DOF. Although ORW has the smallest average preamble count, the duplicate ratio is much higher than others as shown in Fig. 14(c). The duplicate degrades the channel utilization, as explained in Section II. In AMAC, instead of the continuous data packet transmission, the sender waits for the probe from the receiver when it wakes up. Upon receiving a probe, the sender sends the pending packet to the receiver immediately. When multiple senders have packets for the same receiver, packet collisions occur and data retransmissions will significantly reduce the channel utilization. Hence, DOF is more adaptive for various traffic loads, and thus the network yield of DOF is better than others.

# C. Energy Consumption

As Fig. 14(b) shows, the average duty-cycle of DOF is the smallest among various traffic loads, except for the case of CTP-AMAC when the traffic load is low ( s). AMAC is highly energy-efficient in low traffic load because it uses one-hop synchronization. The advantages of transmission solicitation and synchronization in AMAC transform to the weakness as the traffic load increases. This is because the solicitation from the receiver to effectively synchronize packet transmissions results in concentration in packet transmission, and thus contention and collision. DOF saves at least 21.4% and 51.4% of energy compared to others when IPI is 1 and 2 s, respectively. The CTP-XMAC has the lowest energy efficiency. ORW performs badly when IPI is less than 4 s. The energy consumption of CTP-AMAC increases slowly when IPI is less than 8 s.

In a high traffic load, the sharp increasing of energy consumption of CTP-XMAC and ORW is due to the degradation of the channel utilization mentioned above. However, the energy consumption in CTP-AMAC increases slowly. We guess the reason is the synchronized sleep schedule of AMAC.

The histograms in the middle of Fig. 15 clearly show the dutycycle of each node for different protocols with different traffic loads. When the IPI is 1 and 2 s, on most nodes, the duty-cycle of DOF is much better than ORW and CTP-XMAC. ORW consumes almost the same energy as CTP-XMAC. When IPI is 4 ${ \mathrm { s } } ,$ on most nodes, the duty-cycle of ORW is close to that of DOF, and both of them are better than CTP-XMAC. The results verify that although ORW performs well in a low-traffic-load network, DOF can keep the energy consumption low for various traffic loads.

DOF utilizes the probe to detect potential forwarders so that it induces a low communication overhead. The experiments show that in the high traffic load, the energy efficiency brought by the probe is much larger than the overhead. In a low traffic load, the overhead of the probe transmission is also limited.

# D. Duplicate Ratio

In Fig. 14(c), compared to ORW, DOF significantly reduces duplicate ratio when IPI is less than 4 s. The average duplicate ratio of ORW is about 85% when IPI is 1 s. This is about 10 times larger than DOF. The duplicate ratio of DOF is comparable to the deterministic routing under various traffic loads. As the histograms on the top of Fig. 15 show, on most of the nodes, the duplicate ratio of DOF and CTP-XMAC are much less than ORW. When IPI is 1 s, the highest duplicate ratio of ORW exceeds 300% (e.g., node 19). Compared to ORW's high duplicate ratio, DOF always keeps the duplicate ratio low, which is close to the duplicate ratio of CTP-XMAC in different traffic loads. The results of duplicate ratio verify the efficiency of the ACK slot assignment algorithm.

# E. Delay

As Fig. 14(d) shows, the average preamble count of CTP-XMAC does not change significantly with the increasing of network traffic load. The average preamble count of DOF, which is comparable to ORW, is 3 times less than CTP-XMAC. The average preamble count increases when the traffic load increases. The histograms on the bottom of Fig. 15 show the average preamble count of each node in different traffic loads. We can see CTP-XMAC always has the largest delay on every node. Due to channel degradation, the maximum average preamble count reaches 8 and 12 when IPI is 2 and 1 s, respectively. DOF has less delay than ORW in the scenarios when IPI is no more than 2 s because the waking forwarders simultaneously send ACKs resulting in ACK collisions in ORW protocol. Then, the sender will broadcast the data packet again. In a low traffic load, the overhead brought by probe transmission makes the average preamble count of DOF a little greater than that of ORW in single-hop propagation. Considering the preferential use of the links with high routing progress, we believe that DOF can reduce hop count compared to ORW.

# F. Impact of Network Churn

The node reboot, node replacement, or link dynamic will incur network churn, which may further lead to the degradation of system performance. We evaluate the impact of network churn on DOF and $L ^ { 2 }$ . $L ^ { 2 }$ optimizes the energy utility by incorporating the synchronized rendezvous, link burstiness, and dynamic forwarding. In the implementation of $L ^ { 2 }$ , each node will take 10 min to synchronize the rendezvous with neighbors by routing beacons before it begins to generate data. When the synchronization is stable, the frequency of the routing beacon is reduced to one per several minutes.

![](images/067174ac320cc070c38c856eb202dadd9fc8a19c7470a2013c7151bbd8dc2471.jpg)



Fig. 16. Impact of churn on DOF and $L ^ { 2 }$ in the network with s and removing or adding several nodes. The -axis indicates the time units. Each unit is corresponding to 2 min.

We set the IPI as 4 s and do the experiments for 1 h in the daytime with the influence of the human behavior and WiFi. Moreover, for DOF, we randomly remove and add nodes. For $L ^ { 2 }$ , we randomly reboot nodes. The top figure of Fig. 16 shows the number of nodes sending packets.

The middle figure of Fig. 16 illustrates the variance of the PRR. We can see that there is almost no influence on DOF since there is no need of any extra control message in DOF. However, we can see the PRR of $L ^ { 2 }$ decreases even without churn. The reason is that the a high traffic load will lead to time error accumulation in TinyOS system so that the synchronization accuracy will decrease quickly. Without enough routing beacons for resynchronization, routing loops or data retransmissions will significantly degrade the PRR. When there are network churns, the PRR of $L ^ { 2 }$ tends to be more dynamic.

The bottom figure of Fig. 16 illustrates the variance of the radio duty-cycle along the time. We can see that the energy consumption of DOF without churn is relatively stable. When there are network churns, since the reduced data amount brings low channel contention, the energy consumption could be reduced as shown around the 15th time unit. However, if nodes around the sink are removed, the path length will increase. Thus, the churn might also increase the energy consumption as shown around the 22nd time unit. The window-based transmission of $L ^ { 2 }$ makes the energy consumption of a single transmission is bounded, even with packet loss. We can also see the energy consumption of $L ^ { 2 }$ last increasing slowly.

Although $L ^ { 2 }$ has less energy consumption, it needs extra control overhead, i.e., routing beacon, to deal with network churns and thus the energy consumption increases. In contrast, DOF explores the temporally available links by probe, but does not need up-to-date link-state maintenance. Thus, DOF is more adaptive to practical large-scale network deployments.

# VI. DISCUSSION

In this section, we first discuss the impact of software ACK on performance, and then state the possible optimization on DOF.

# A. Software ACK

DOF uses software acknowledgment in the implementation. However, in current CC2420 radio stack in TinyOS system, we found the software ACK is vulnerable when the traffic load is high. The limitation is due to the slow buffer swapping between MCU and CC2420. One consequence is that a new packet may arrive when the sender is waiting for the ACK. The processing time of the received packet might affect the accuracy of the ACK slot calculation. The other consequence is increasing the collision probability between ACK and data packets.

For DOF in a high traffic load, the transmission of probe, data packet, and ACK are mixed, which might lead to ACK loss or ACK slot prediction error. This explains why the PRR in Fig. 7 is lower than 80% when IPI is 1 s. The average preamble count when IPI is 1 s is higher than that when IPI is 2 s. We believe that DOF could work better with more fine-grained timing control in the radio stack.

# B. Fixed Slot Number

In the design of the protocol, DOF adopts a fixed number of slots to detect the quantity and differentiate the priority of all potential forwarders. The strategy of fixed slot number is not the most energy-efficient strategy for the diverse network scenarios. For example, in a sparse network, sensor nodes usually have a limited number of forwarders. The sender may not necessarily wait such a long period to recognize a few of potential forwarders. We believe that an adaptive algorithm, which adjusts the maximum slot number according to local routing information and dynamic changes, can further improve the performance of DOF.

# VII. RELATED WORK

In this section, we first make a brief summary about the widely used deterministic forwarding protocols, and then discuss related work on opportunistic and dynamic forwarding mechanisms. Moreover, we illustrate the advantage of our adaptive duplicate suppression schemes in unsynchronized duty-cycled wireless sensor networks.

Deterministic forwarding protocols, such as CTP [18], have been widely applied in WSNs. Considering the limited energy of sensor nodes, WSNs are usually duty-cycled to prolong the network lifetime. The main two types of duty-cycled media access mechanisms for deterministic forwarding are low power listening, such as X-MAC [6], and low power probing, such as A-MAC [15]. Built upon a duty-cycled MAC, the duty-cycled communication nature makes the deterministic forwarding protocols inefficient, e.g., sleep state of the next-hop node bringing about high forwarding latency and high energy consumption, network dynamics reducing the reliability of deterministic forwarding, etc. To address the deficiencies of deterministic forwarding, scientists have devoted much of their research to opportunistic forwarding.

ExOR [7] develops a complete opportunistic routing for wireless networks. ExOR assigns each receiver to further transmit in a distinct time-slot, and the receiver overhears others' transmissions to avoid the duplicates. MORE [10] targets the inefficient coordination process of ExOR and proposes a coding approach to eliminate the overhead. Rather than network coding, DOF takes a lightweight method to mitigate the overhead for wireless sensor networks.

BRE [12] develops the overhearing scheme in CTP [18] to capture the temporally good links. The sender changes the next-hop receiver when the opportunity appears to reduce the transmission count. However, BRE does not address the duty-cycle issue, in which the waiting time dominates the energy efficiency.

In DSF [19], each node knows the schedule of neighbor nodes by synchronization. DSF dynamically selects multiple next-hop forwarders based on the sleep schedules and routing metrics of the neighbors. $L ^ { 2 }$ [16] further notices the link burstiness to optimize the energy consumption on each packet and improve the network yield. However, DSF and $L ^ { 2 }$ need extra control overhead to stabilize the forwarding schedule, which is vulnerable to dynamic links and network churn.

ORW [8] implements the opportunistic routing for unsynchronized low-duty-cycled wireless sensor networks, but shows the limited performance for high-traffic-load applications. DOF extends this work to more general-purpose wireless sensor network applications. CMAC [9] includes the slotted acknowledgments, but CMAC still determines the unique forwarder by overhearing others’ acknowledgments. In DOF, the sender distinguishes the forwarders, and then considers the link quality to arrange the forwarding schedule.

There are also some theoretical works focusing on opportunistic routing [20]–[22] and dynamic forwarding [23], [24] for wireless sensor networks. Although the models and simulation show the efficiency of the opportunistic routing, they neglect the practical issues addressed by DOF.

# VIII. CONCLUSION

Developing an adaptive and efficient forwarding protocol is urgent for a duty-cycled wireless sensor network. In this paper, we propose DOF, a duplicate-detectable unsynchronized low-power opportunistic forwarding that is adaptive to various traffic loads. Based on the slotted acknowledgment, DOF mainly solves the channel degradation problem incurred by the large amount of duplicates in traditional opportunistic forwarding and retains the benefits of the opportunistic routing as much as possible. The testbed experiments show DOF is more efficient and reliable than state-of-the-art low-duty-cycled forwarding protocols.

# REFERENCES

[1] X. Mao, X. Miao, Y. He, X.-Y. Li, and Y. Liu, “Citysee: Urban CO monitoring with sensors,” in Proc. IEEE INFOCOM, 2012, pp. 1611–1619.

[2] L. Mo et al., “Canopy closure estimates with greenorbs: Sustainable sensing in the forest,” in Proc. Sensys, 2009, pp. 99–112.   
[3] M. Ceriotti et al., “Is there light at the ends of the tunnel? Wireless sensor networks for adaptive lighting in road tunnels,” in Proc. IPSN, 2011, pp. 187–198.   
[4] X. Wu, M. Liu, and Y. Wu, “In-situ soil moisture sensing: Optimal sensor placement and field estimation,” Trans. Senor Netw., vol. 8, no. 4, p. 33, 2012.   
[5] J. Polastre, J. Hill, and D. Culler, “Versatile low power media access for wireless sensor networks,” in Proc. Sensys, 2004, pp. 95–107.   
[6] M. Buettner, G. V. Yee, E. Anderson, and R. Han, “X-MAC: A short preamble MAC protocol for duty-cycled wireless sensor networks,” in Proc. Sensys, 2006, pp. 307–320.   
[7] S. Biswas and R. Morris, “Exor: Opportunistic multi-hop routing for wireless networks,” Comput. Commun. Rev., vol. 35, no. 4, pp. 133–144, 2005.   
[8] O. Landsiedel, E. Ghadimi, S. Duquennoy, and M. Johansson, “Low power, low delay: Opportunistic routing meets duty cycling,” in Proc. IPSN, 2012, pp. 185–196.   
[9] S. Liu, K.-W. Fan, and P. Sinha, “CMAC: An energy-efficient MAC layer protocol using convergent packet forwarding for wireless sensor networks,” Trans. Senor Netw., vol. 5, no. 4, pp. 29:1–29:34, 2009.   
[10] C. Szymon, J. Michael, K. Sachin, and K. Dina, “MORE: Network coding approach to opportunistic routing,” MIT-CSAIL-TR-2006-049, 2006.   
[11] K. Srinivasan, M. A. Kazandjieva, S. Agarwal, and P. Levis, “The -factor: Measuring wireless link burstiness,” in Proc. Sensys, 2008, pp. 29–42.   
[12] M. H. Alizai, O. Landsiedel, J.Á. B. Link, S. Götz, and K. Wehrle, “Bursty traffic over bursty links,” in Proc. Sensys, 2009, pp. 71–84.   
[13] D. S. De Couto, D. Aguayo, J. Bicket, and R. Morris, “A high-throughput path metric for multi-hop wireless routing,” Wireless Netw., vol. 11, no. 4, pp. 419–434, 2005.   
[14] N. Cressie, “Fitting variogram models by weighted least squares,” Math. Geol., vol. 17, no. 5, pp. 563–586, 1985.   
[15] P. Dutta, S. Dawson-Haggerty, Y. Chen, C.-J. M. Liang, and A. Terzis, “Design and evaluation of a versatile and efficient receiver-initiated link layer for low-power wireless,” in Proc. Sensys, 2010, pp. 1–14.   
[16] Z. Cao, Y. He, and Y. Liu, “ : Lazy forwarding in low duty cycle wireless sensor networks,” in Proc. IEEE INFOCOM, 2012, pp. 1323–1331.   
[17] R. Fonseca, P. Dutta, P. Levis, and I. Stoica, “Quanto: Tracking energy in networked embedded systems,” in Proc. OSDI, 2008, pp. 323–338.   
[18] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection tree protocol,” in Proc. Sensys, 2009, pp. 1–14.   
[19] Y. Gu and T. He, “Data forwarding in extremely low duty-cycle sensor networks with unreliable communication links,” in Proc. Sensys, 2007, pp. 321–334.   
[20] X. Mao, X.-Y. Li, W.-Z. Song, P. Xu, and K. Moaveni-Nejad, “Energy efficient opportunistic routing in wireless networks,” in Proc. MSWiM, 2009, pp. 253–260.   
[21] G. Schaefer, F. Ingelrest, and M. Vetterli, “Potentials of opportunistic routing in energy-constrained wireless sensor networks,” in Wireless Sensor Networks. New York, NY, USA: Springer, 2009, pp. 118–133.   
[22] J. Lu and X. Wang, “Interference-aware probabilistic routing for wireless sensor networks,” Tsinghua Sci. Technol., vol. 17, no. 5, pp. 575–585, 2012.   
[23] J. Kim, X. Lin, and N. Shroff, “Optimal anycast technique for delaysensitive energy-constrained asynchronous sensor networks,” in Proc. IEEE INFOCOM, 2009, pp. 612–620.   
[24] J. Kim, X. Lin, N. B. Shroff, and P. Sinha, “On maximizing the lifetime of delay-sensitive wireless sensor networks with anycast,” in Proc. IEEE INFOCOM, 2008, pp. 807–815.

![](images/a187cdbfddc68e37fc32e9155ab5fdc8eb89d96d0cda7a7a0ef06c6cb2c1ff9c.jpg)



Daibo Liu received the B.E. degree in computer science and technology from Dalian Maritime University, Liaoning, China, in 2009, and the M.E. degree in computer science and engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2012, and is currently pursuing the Ph.D. degree at the University of Electronic Science and Technology of China.

His current research interest is wireless sensor networks.

![](images/8aef43b1b648eecbd5bdf1eba6f29a0eeeac8cb059ecd0f9983aa6ee094f3740.jpg)



Mengshu Hou (M’13) received the Ph.D. degree in computer application from the University of Electronic Science and Technology of China, Chengdu, China, in 2005.

He is currently a Professor with the School of Computer Science and Engineering, University of Electronic Science and Technology of China. His research interests include wireless sensor networks, distributed computing, and trusted P2P computing.

![](images/413b9935092d8554e73ad4eb7e5b2c4e10b2009a5ae5904bd4f209877839e9e2.jpg)



Zhichao Cao (S’12–M’13) received the B.E. degree in computer science and technology from Tsinghua University, Beijing, China, in 2009, and the Ph.D. degree in computer science and engineering from Hong Kong University of Science and Technology, Hong Kong, in 2013.

He is currently with the School of Software, TNLIST, Tsinghua University. His research interests include sensor networks, mobile networks, and pervasive computing.

Dr. Cao is a member of the Association for Com-

puting Machinery (ACM).

![](images/9c208a1d502228ba7cb02550bf83c145a91674cf7d99c62ee725c412ae95bd53.jpg)



Jiliang Wang (S’09–M’12) received the B.E. degree in computer science and technology from University of Science and Technology of China, Hefei, China, in 2007, and the Ph.D. degree in computer science and engineering from Hong Kong University of Science and Technology, Hong Kong, in 2011.

He is currently with the School of Software and TNLIST, Tsinghua University, Beijing, China. His research interests include sensor and wireless networks, network measurement, and pervasive computing.

![](images/eac6c6850a228af9015eb7833e372de0d23ae92b52504473403ad40780b2e7da.jpg)



Yuan He (S’09–M’12) received the B.E. degree in computer science from the University of Science and Technology of China, Hefei, China, in 2003, the M.E. degree in computer software and theory from the Chinese Academy of Sciences, Beijing, China, in 2006, and the Ph.D. degree in computer science and engineering from the Hong Kong University of Science and Technology, Hong Kong, in 2010.

He is now an Assistant Professor with the School of Software, Tsinghua University, and the Vice Director of the IOT-Tech Center, Tsinghua National

Lab for Information Science and Technology, both in Beijing, China. His research interests include sensor networks, peer-to-peer computing, and pervasive computing.

![](images/debbc55f21378e76e4699a00c9a2c52d487e3907814985961ffd8840836669b2.jpg)



Yunhao Liu (S’03–M’04–SM’06–F’15) received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, the M.A. degree from Beijing Foreign Studies University, Beijing, China, in 1997, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively.

He holds the Changjiang Chair Professorship with Tsinghua University.

Prof. Liu is a Fellow of the IEEE Computer Society. He is currently an ACM Distinguished Speaker and Vice Chair for the ACM China Council. He is serving as an Associate Editor-in-Chief for the IEEE TRANSACTIONS ON PARALLEL AND DISTRIBUTED SYSTEMS and Associate Editor for the IEEE/ACM TRANSACTIONS ON NETWORKING and ACM Transactions on Sensor Networks.