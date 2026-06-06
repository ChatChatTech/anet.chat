# End-to-end Delay Measurement in Wireless Sensor Networks without Synchronization

Kebin Liu $^{\dagger}$ , Qiang Ma $^{\dagger\ddagger}$ , Haoxiang Liu $^{\ddagger}$ , Zhichao Cao $^{\dagger\ddagger}$ and Yunhao Liu $^{\dagger}$

† School of Software and TNLIST, Tsinghua University, Beijing, China

‡Department of Computer Science and Engineering, Hong Kong University of Science and Technology

{kebin, maq, haoxiang, zhichao, liu}@greenorbs.org

Abstract—The deployment of large scale Wireless Sensor Networks generally needs network management and measurement solutions. End-to-end delay is one of the most important metrics in assessing the network performance. Many efforts have been devoted to measuring the end-to-end delay efficiently and precisely. Unfortunately, existing approaches often require sensor nodes to be tightly time synchronized which is costly in resource limited sensor network. We propose a novel scheme that can measure the end-to-end delay for each packet to the granularity of tens of microseconds without clock synchronization. Through extensive experiments on our testbed, we examine the effectiveness of our approach. The results show that our scheme achieves high performance with low overhead. We also present observations about the network states by tracking and analyzing the end-to-end delay data.

Index Terms—wireless sensor networks, end-to-end delay, measurement

# I. INTRODUCTION

In recent years, Wireless Sensor Networks have drawn significant attentions from researchers all over the world $[1-7]$ . Many efforts have been made to improve the functionality and performance of sensor network systems, so as to enable the long-term deployment of large scale sensor networks like our ongoing project CitySee $[8]$ . CitySee aims to build a system that collects the realtime environmental data in urban areas such as temperature, humidity and carbon dioxide concentration. Up to now, CitySee has deployed 1200 nodes equipped with various sensors among a large variety of regions including residential quarters, industrial parks, and the like. Figure 1 illustrates a snapshot of the CitySee deployment. Based on the experience in deploying this system, we find that maintenance of such a large scale sensor network brings many new challenges to the network management and measurement. In this research, we focus on the problem of end-to-end packet delivery delay measurement which is a critical metric in assessing the network performance as well as the Quality of Service (QoS) for many applications. Besides, the temporal and spatial distribution of end-to-end delays may indicate the occurrence of some abnormal events such as the link failures, routing loops, and the like.

![](images/6230a07a3b976333115721b5484a3fb079af10cb845584615d349a1a62ba509a.jpg)



Figure 1 A snapshot of the CitySee deployment

Nevertheless, tracking the end-to-end delivery delay of each packet to the granularity of tens of microseconds in large scale sensor networks is non-trivial. First, the sensor nodes are self-organized and thus the network administrator does not really know the network topology as a priori. Second, compared with traditional enterprise networks, sensor networks are much more dynamic both on the routing structure and link status. Third, sensor nodes are extremely energy constraint, so the delay measurement solutions have to incur as low overhead as possible. Finally, it is difficult to get all sensor nodes tightly time synchronized.

End-to-end delay measurement is a well-studied problem in Internet. Those works can be divided into two main categories. The first relies on active probing $[14]$ to determine the path and link properties. These approaches may lead to high traffic to the network and can hardly be applied to the traffic-fragile sensor networks. Importantly, the active probing methods can only sample the network measurements with a limited frequency which is far from enough to reflect the dynamics of sensor networks. The second are passive schemes. For example, the state-of-the-art LDA mechanism $[15]$ proposes to instrument routers with a hash-based primitive through which we can passively analyze the traffic on routers and then capture the fine-grained latency measurements. Such a method, however, has a stringent requirement on the clock synchronization which cannot be easily fulfilled in sensor networks. Clearly, if we already have ideal time synchronization component (high precision with negligible overhead), the end-to-end delay measurement can be simply achieved by taking two timestamps on both the source node and sink side or applying the LDA to save the storage space. In a large scale sensor network, global time synchronization is very costly in both the bandwidth and program memory consumption. Besides, the synchronization services usually suffer a lot from the unreliable wireless links as well as the environmental interferences.

In sensor network research field, many approaches $[9-12]$ focus on improving the performance of network protocols and provide end-to-end delay guarantee as well as theoretical analysis $[16-20]$ . Since it is difficult to achieve the global synchronization in large-scale sensor networks, measuring the end-to-end delay is extremely challenging. LiveNet $[13]$ applies sniffer nodes to record the network transmission traces so as to rebuild the network dynamics. The method, however, requires additional hardware and thus very costly. Another approach is to keep the per-hop delay records in each data packet. While the packet arrives at sink, the end-to-end delay can be calculated by accumulating all per-hop delays. Despite simplicity, the method incurs high overhead for keeping these timestamps. The first choice is to record delay values hop by hop with separate counters (several bytes per hop). As the large scale sensor networks usually contain long end-to-end path, the method may consume a large amount of space in data packets and thus is infeasible. Another choice is to keep only one counter in each packet that records the accumulated delay to date. However, such approach is vulnerable to the clock skew. As the frequencies of different sensor nodes' clock are different and they may output different readings while measuring the same period. The per-hop delay counters on each end-to-end path come from different node clocks, thus a direct summation of these counters can lead to significant measurement errors.

To address these issues, we propose a novel approach named Sequential Difference Recovery (SDR) for end-to-end delay measurement. SDR is a light-weight approach which does not inject extra probing traffic to the network but only add a 4 bytes timestamp field in routine packets (the number of timestamps can be more in a small number of anchor packets). SDR is robust to packet loss, without time synchronization. The contributions of this work are as follows:

1) We present a novel measurement scheme SDR tailored for data delivery delay measurement in large scale sensor networks.   
2) We investigate the key design issues in SDR such as the impact of clock drift and disordered packets.   
3) We implement our scheme on TelosB motes and conduct extensive experiments on a testbed with 50 nodes to verify the effectiveness of our scheme. By tracking and analyzing the end-to-end delays, we present observations about the network operation.

The rest of this paper is organized as follows. In Section II, we review different research works that are related to this work. In Section III, some preliminaries are introduced. We present our main idea in Section IV and discuss the key design issues. In Section V, we demonstrate the experimental results and we conclude this work in Section VI.

# II. RELATED WORK

Network delay is a key performance metric in the IP networks. Many real-time online applications such as IP telephony, online games and video conferences require guaranteed QoS provided by the ISPs to the customers. Hence, delay measurement plays an essential and critical rule to ensure the functionality of IP network. Choi et al. obtain the accurate point-to-point delay measurement in operational tier1 network [21]. Machiraju et al. proposes a measurement friendly architecture to enable accurate active measurement performance [22]. In addition, a measurement method by sampling a subset of packet trajectories is suggested by Duffield et al. [23]. More recently, Kompella et al. study the fine-grain measurement in the applications where stringent end-to-end delay is required. For instance, the Lossy Difference Aggregator (LDA) mechanism is proposed to capture the fine-grained latency in the network [15]. Right after, Lee et al. further discover that different flows exhibit different characteristics in the same link, which cannot be reflected by LDA since LDA only provides aggregate measurements. Consequently, they propose another fine-grained per flow measurement architecture named reference latency interpolation (RLI) [24].

Other than IP networks, real time communications are also required in many time critical applications in wireless sensor networks, in which sensed data should be delivered to the sink node within a bounded latency. To achieve this objective, end to end (E2E) delay analysis is extensively studied in the research field of wireless sensor networks as well. Due to energy supply constraint, sensor nodes adopt duty cycle to save battery and prolong lifetime. Consequently, the E2E delay suffers from sleep latency incurred by duty cycle. Hence, it is not unusual that bounded E2E latency is always achieved while minimizing the overall energy of sensor nodes. Yang et al. explore the energy-latency tradeoff in a real-time scenario $[19]$ . Xue et al. propose a wake up scheme to achieve energy-delay balance $[17]$ . Lu et al. show how to minimize the E2E latency given a specific duty cycle pattern of sensor nodes $[25]$ . Theoretically Dousse et al. present analysis on E2E latency assume that duty cycle schedule among sensor nodes are completely uncoordinated $[16]$ . However, all the works above assume perfect wireless links which can hardly hold in WSNs. To address this problem, Gu et al. introduce dynamic switch based forwarding $[26]$ to optimize expected E2E delay while considering both very low duty cycle sensor nodes and lossy wireless links. In the following work, they provide various energy efficient schemes to bound the communication delay also in low duty cycle WSNs $[20, 27]$ . Nevertheless, most of the works introduced in WSNs above primarily focus on E2E delay minimization, optimization and bound analysis, and they all require tight clock synchronization among sensor nodes. So far, not many works focus on end-to-end delay measurement in WSNs. To the best of our knowledge, this is the first work studying the E2E delay measurement in WSNs without clock synchronization.

![](images/edcf699ac6ecf868406d00a2b2e45f79de258dca97925f6ae7964ebd303fbbd9.jpg)



Figure 2 Frequencies of different sensor nodes

# III. PRELIMINARIES

In this section, we introduce some preliminaries related to our delay measurement, including the factors that may impact the delivery delay, the properties of the clock in a sensor node and the timestamping techniques we applied in this approach.

# A. Understanding the Packet Delivery Delay

In this subsection, we give a brief introduction about the sources of the packet delivery delay as well as their uncertainties. In a typical data acquisition sensor network, the end-to-end delay is composed of multiple per-hop delays. The per-hop delay consists of two major parts, the caching delay and the transmitting delay.

We define the caching delay as the period between the end of receiving a certain packet and the beginning of forwarding it to another sensor node. During this period, the packet may be kept in the message pool or be processed by current node. Finally, the packet is put into the send queue waiting for transmission. The caching delay is nondeterministic that is affected by many factors such as the application specification, the duty cycle strategy of sensor node, the length of the send queue, and the like.

The transmitting delay corresponds to the period of packet transmission. It includes several sources and in our approach we follow the decomposition presented by Kopetz and Ochsenreiter $[28]$ . The first source is Send Time which is used to assemble the packet and issue the request to MAC layer. Send Time is nondeterministic and can reach a magnitude of hundreds of milliseconds. The second source is Access Time, the time of waiting for the channel access. Depending on the channel states, the waiting time can vary from milliseconds to seconds. The third source is the Propagation Time, the time for the signal transmitting from sender to receiver. This delay is deterministic depending on the physical distance and very

![](images/3b901523ca9cb11e84ad6be882c4654aba2681179eac904b6eabaf5ee30a9976.jpg)



Figure 3 Demonstration of the clock skew

small (less than 1 $\mu$ s for distances up to 300 meters). The Fourth source is the Transmission Time (Reception Time), the time for the sender (receiver) to transmit (receive) the packet. Transmission Time and Reception Time are nondeterministic depending on the packet length and radio property. Note that the Transmission Time and Reception Time overlap.

# B. Investigating the Clock Drift

A clock in sensor node is usually composed of two parts, a signal source like a quartz oscillator and a register which keeps the number of periods elapsed. Due to the hardware property and some environmental factors, clocks in different nodes may exhibit varying frequencies. We measure the clock frequency of four randomly selected TelosB motes and the results are shown in Fig.2. Different nodes exhibit varying frequencies and the frequency of each clock has very small jitters over time. The accumulate offset among clocks' outputs are denoted as clock drift. The slope of change in clock drift is called the clock skew [30].

For example, Fig. 3 shows the outputs of two clocks clock B from a sensor node and reference clock A. The X axis describes the real time elapsed and Y axis is the time recorded by different clocks from a same starting point. The solid line in red denotes the output of the reference clock and the dashed line in blue comes from clock B. Note that, we assume that the reference clock A is ideal and thus the slope of the red solid line is $45^{\circ}$ . As shown in Fig.3, for the same time interval, the measured values of clock A and B are $T_{A}'$ and $T_{B}'$ respectively. Therefore, the skew of clock B with respect to A is as follows.

$$
S k e w = \left(T _ {\mathrm{B}} ^ {\prime} - T _ {\mathrm{A}} ^ {\prime}\right) / T _ {\mathrm{A}} ^ {\prime}
$$

Skew is measured in ppm (parts per million). As reported in prior works, it normally ranges from $\pm5$ ppm to $\pm100$ ppm. In order to study the properties of skew, we conduct experiments on TelosB motes. We make one sensor node periodically send beacon messages to 4 receivers. Both the sender and receivers take timestamps during the transmission. By analyzing these timestamps, we can derive the measured time of different nodes on the same intervals. Here we use the sender as the reference clock and the skew values respect to it are illustrated in Fig.4.

![](images/c009c49f8fff96c64cecd3302f6d03cf03667a2070fbf3a37f67fd99081945c3.jpg)



Figure 4 The frequency of oscillator in sensor nodes

Based on the results in Fig.4, we have several observations. First, the skew values vary among different nodes. Second, the skew value of one node is relatively stable over time with very small jitters. Similar results have been reported that today's oscillators exhibit a low aging factor ( $\pm3$ ppm/year). These observations motivate the design of our skew estimation scheme in Section IV as well as its feasibility. Since we do not assume any synchronization services in our approach, clock skew may affect the measured time of different nodes and thus we cannot directly apply them in delay computation. In Section IV, we will discuss the skew estimation in detail.

# C. Mac Layer Timestamping and Per-hop Delay

In order to get accurate delay measurements, we need precise timestamps to mark certain events like the end of a packet transmission. In this approach, we apply a MAC layer timestamping scheme which is similar to that in FTSP $[29]$ . Using this timestamping strategy, the sender and receiver can take timestamps simultaneously during packet transmission. Therefore, the end-to-end delivery delay can be segmented to multiple per-hop delays. Each node takes two timestamps on receiving and transmitting a packet and the difference between these two timestamps is the delay of current hop. As a pair of sender and receiver can take timestamps simultaneously, the summation of multiple per-hop delays can recover the full end-to-end path delay. In SDR, this technology is applied for deriving the end-to-end delay of anchor packets which will be discussed in Section IV. Note that, the MAC layer timestamping scheme cannot compensate for the propagation delay. Fortunately, this delay depends only on distance and is negligible (less than 1 $\mu$ s for distances up to 300 meters).

# IV. OUR APPROACH

In this section, we firstly present a base line approach, and then we discuss the key design issues and present the full-featured SDR.

![](images/a28d1413a17148555233c383a6df9e128de7ad5ce4582e472639bf7fd7eac397.jpg)



Figure 5 The basic SDR approach

# A. The Basic SDR

The network model considered in this work is as follows. A large number of sensor nodes are deployed in a wide area. They connect to each other in an ad-hoc manner and periodically sample the environmental parameter and report the sensory data to sink through multi-hop wireless communications.

In such a network, our goal is to measure the delivery delay of each packet from the source node to sink in a light-weight way. As the sensor nodes are deployed in the wild and remote areas and we cannot directly access them, a straightforward idea is to keep the per-hop delay records in each data packet. While the packet arrives at sink, the end-to-end delay can be calculated by accumulating all per-hop delays. Despite of its simplicity, this method incurs timestamping operation on every data transmission and reception process (as well as storage cost of the reception and transmission timestamps for each packet). In order to keep the per-hop delay information, one strategy is recording them with separate counters (several bytes per hop) hop by hop. As the large scale sensor networks usually contain long end-to-end path, this method may consume a large amount of space in data packets and thus is infeasible. Another choice is to keep only one counter in each packet that records the accumulated delay to date. However, this approach is vulnerable to the clock skew. As discussed in Section III, the frequencies of different sensor nodes' clock are varying and they may output different readings while measuring the same period. Since the per-hop delay counters on each end-to-end path come from different node clocks, a direct summation of these counters can lead to significant measurement errors.

To address these issues, we propose SDR, a novel delay tracking approach based on the end-to-end passive measurement. Our basic idea consists of two stages. In the first stage, instead of directly measuring the end-to-end delay, we choose to derive a sequence of delay differences between consecutive packets. Then in the second stage, we try to recover all the delay information with the differences sequence and a few anchor measurements.

Table 1 Notations 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $T_i$ </td><td>Theith timestamps recorded by an ideal clock</td></tr><tr><td> $T_i^j$ </td><td>Theith timestamps recorded by sensor node j</td></tr><tr><td> $p_m$ </td><td>Data packets</td></tr><tr><td> $d_m$ </td><td>The end-to-end delay of the mth packet</td></tr><tr><td> $a^i$ </td><td>Theskewof theithnode respect to sink</td></tr></table>

Stage One: Figure 5 illustrates a typical data delivery process in a multi-hop sensor network, a source node periodically samples sensory data and sends data packets to sink through multi-hop wireless communications. Here we apply terms $T_{1}$ , $T_{2}$ , $T_{3}$ , etc. to denote timestamps recorded by an ideal clock and $T_{i}^{j}$ to denote the timestamps from the jth sensor node at time $T_{i}$ .

At time $T_{1}$ , the source node finishes transmitting a packet $p_{1}$ to its next hop. In SDR, we make the source node take a timestamp, in this example $T_{1}^{1}$ , and attach this timestamp to the data packet. This packet is forwarded towards sink through multi-hop transmissions. Then at time $T_{2}$ , the sink successfully receives this packet and record the timestamp $T_{2}^{0}$ with its own clock. At the sink side, we get $T_{1}^{1}$ (from the packet) and $T_{2}^{0}$ . Unfortunately, they cannot be directly used to calculate the end-to-end delay because they are recorded by two different clocks which are unsynchronized. Obviously, if the sink knows the corresponding time $T_{1}^{0}$ on its timeline when the packet leaves source node, we can simply get the end-to-end delay $d_{1}$ of $p_{1}$ as follows:

$$
d _ {1} = T _ {2} ^ {0} - T _ {1} ^ {0} \tag {1}
$$

The sink, however, is usually far away from the source node and thus cannot get the exact value of $T_{1}^{0}$ . Similarly, as shown in Fig. 5 the source node is unaware of the packet reception time at sink as well.

Now let's look at two consecutive packets. As illustrated in Fig.5, the second packet is sent at $T_{3}$ and received by sink at $T_{4}$ . These two events are recorded by source node and sink respectively. We observe that the time interval between $T_{3}^{1}$ and $T_{1}^{1}$ overlaps with that between interval between $T_{4}^{0}$ and $T_{2}^{0}$ . Here we assume that the clocks of source node and sink have the same frequency with ideal clock, in other words, there is no clock skew. We will later release this assumption. Then despite of the offsets in different clock readings, we have $T_{3}^{1} - T_{1}^{1} = T_{3} - T_{1}$ and $T_{4}^{0} - T_{2}^{0} = T_{4} - T_{2}$ .

$$
\left(T _ {4} ^ {0} - T _ {2} ^ {0}\right) - \left(T _ {3} ^ {1} - T _ {1} ^ {1}\right) = d _ {2} - d _ {1} \tag {2}
$$

Similarly, we can get a series of delay differences $\{(d_{2}-d_{1}),(d_{3}-d_{2}),(d_{4}-d_{3}),\ldots\}$ at sink when packets accumulate. In real applications, clocks in different sensor nodes do have varying frequencies (clock skew) which may result in biased readings for the same period. In this example, $T_{4}^{0}, T_{2}^{0}$ are generated by sink node and $T_{3}^{1}, T_{1}^{1}$ come from the source node, we should firstly normalize these values to the ideal clock. Since the ideal clock does not exist in real applications, we apply the clock of sink as the reference clock. Assume that $a^{i}$ denotes the skew of

![](images/350d5309ab60806fb1b22247ce5f838738a38cbb1f1a069f395ff04d26e2ad8f.jpg)



Figure 6 An example of the delay difference sequence   
![](images/bb9f0ac0d78cecae74195ee83090338cf612a76ef3bde3fb3acece02202560dd.jpg)



Figure 7 The packet forwarding process and delay segmentation

the ith node respect to sink, and then we have,

$$
\frac {(T _ {3} ^ {1} - T _ {1} ^ {1}) - (T _ {3} ^ {0} - T _ {1} ^ {0})}{(T _ {3} ^ {0} - T _ {1} ^ {0})} = a ^ {1}
$$

Then we replace the $(T_3^1 - T_1^1)$ in equation (2) with $(T_3^0 - T_1^0)$ and get equation (3) which takes skew into account:

$$
\left(T _ {4} ^ {0} - T _ {2} ^ {0}\right) - \frac {\left(T _ {3} ^ {1} - T _ {1} ^ {1}\right)}{\left(1 + a ^ {1}\right)} = d _ {2} - d _ {1} \tag {3}
$$

Consequently, we need to estimate the skew $(a^{\mathrm{i}})$ of each source node respect to the sink. The details of skew estimation will be discussed in later subsections.

Stage two: Figure 6 shows the results from a demonstration experiment in which a source node periodically sends packet to sink through a path of more than 5 hops. At sink side, we collect sending timestamps from packets and receiving timestamps by sink itself. After the stage one calculation, the delay difference sequence between each pair of adjacent packets can be derived. This sequence indicates the variation of consecutive end-to-end packet delays. We can also calculate the sequence of delay differences respect to one particular packet delay, for example, $\{(d_{2}-d_{1}),(d_{3}-d_{1}),(d_{4}-d_{1}),\ldots\}$ . Obviously, if we know the exact value of an arbitrary packet delay $d_{i}$ , we can recover all other delay values. Then in stage two, our goal is to derive at least one end-to-end delay value which we denote as an anchor and then recover the full delay sequence.

![](images/6bc91f1d474c483120541e1a534b7665b05d9ec4b397932558be21f75a4efdfd.jpg)



Figure 8 The clock skew estimation scheme

In order to get the end-to-end delay anchor, we propose to let the source node transmit an extra packet in which the delay is recorded hop by hop. Since the number of anchor packets is very small, the overhead incurred by applying them can be neglected. Figure 7 illustrated a typical process of anchor packet forwarding. When node $S_{2}$ received the anchor packet from $S_{1}$ , it takes a timestamp $T_{1}^{2}$ . After that, the packet is cached in $S_{2}$ for a certain period. $S_{2}$ may conduct some operations to this packet, then put it into the send queue and finally forward the packet to next hop (in this example $S_{3}$ ). At the end of the packet transmission, $S_{2}$ takes the second timestamp $T_{2}^{2}$ and attaches the interval (per-hop delay) $d = T_{2}^{2} - T_{1}^{2}$ and the ID of $S_{2}$ to the anchor packet. By this way, we record the delay hop by hop in the anchor packet. At sink side, we can derive the end-to-end delay by add up all these per-hop delays.

There are two potential sources of errors in this method. The first one is the propagation delay of wireless signals, as shown in Fig. 7, there is always a small gap between the transmission event and the reception event. This error, however, is negligible (less than 1 $\mu$ s for distances up to 300 meters) and deterministic (depends on the distance). The second source of errors comes from the clock skew. As the per-hop delays are recorded by different clocks, direct summation of all per-hop delays may lead to biased results. In SDR, we propose to compensate these errors through clock skew estimation. More details will be discussed in subsection IV B.

Theoretically, we can recover all end-to-end delay values with only one anchor packet. In order to improve the reliability and robustness of our results, we leverage multiple anchor samples in SDR. The advantages of applying multiple anchors are two-fold. First, single anchor is vulnerable to random errors due to the unreliable hardware and environmental interferences. With multiple anchor delay measurements, we can easily identify and eliminate outlier values. Second, multi-anchor can help to alleviate the impact of estimation error of clock skew.

# B. Clock Skew Estimation

According to the discussions in Section III, we know that the skew of each clock is different from each other while relatively stable over a long period. In this section, we focus on estimating the clock skew of each source node respect to sink.

In the example of Fig.8, a source node periodically reports data to sink via multi-hop wireless communications. The sink receives two series of timestamps from both source node and sink after a certain period. Based on equation (3), we can get a set of delay differences $\{(d_{i}-d_{j})\}$ .

![](images/923f1ce785af536514db4aabd475fd11909ce9a634ac9befa921f254a90a75a7.jpg)



Figure 9 Demonstration of the disordered packet transmissions

$$
\left(T _ {i} ^ {0} - T _ {j} ^ {0}\right) - \frac {\left(T _ {i} ^ {1} - T _ {j} ^ {1}\right)}{\left(1 + a ^ {1}\right)} = d _ {i} - d _ {j}
$$

As the end-to-end delay is affected by many random factors such as the network traffic, environmental interference, and the like, we regard the delay $d_{i}$ as a random variable. Based on the central limit theorem, when obtaining sufficient samples, $\hat{d}_{i}$ follows the normal distribution and thus the expectation of $(d_{i} - d_{j})$ is zero while i and j are independently selected. Then we have equation (4) for estimating the clock skew.

$$
\operatorname{Lim} \sum_ {i, j} \left[ \left(T _ {i} ^ {0} - T _ {j} ^ {0}\right) - \frac {\left(T _ {i} ^ {1} - T _ {j} ^ {1}\right)}{\left(1 + a ^ {1}\right)} \right] = 0
$$

$$
\hat {a} ^ {1} = \frac {\sum_ {i , j} (T _ {i} ^ {1} - T _ {j} ^ {1})}{\sum_ {i , j} (T _ {i} ^ {0} - T _ {j} ^ {0})} - 1 \tag {4}
$$

# C. Handling the disordered packets

Due to some routing failures or other abnormal events, the packets may arrive at sink with wrong orders as shown in Figure 9. The first packet $p_1$ sent at $T_1^1$ arrives at sink later than the second packet $p_2$ . In this case, we cannot directly calculate the delay difference between consecutive packets with wrong order.

To address this issue, we propose to use another packet as a reference. In this example, we choose the third packet as a reference point. The transmission and reception of $p_{3}$ are all later than $p_{1}$ and $p_{2}$ . Then we can derive the delay differences between $p_{1}$ and $p_{3}$ as well as that between $p_{2}$ and $p_{3}$ . By this way, the delay difference between the first two packets can be calculated.

# V. EVALUATION

In order to verify the effectiveness of our delay measurement approach, we conduct extensive experiments on a testbed with 50 TelosB motes. By tracking and analyzing the end-to-end delays, we present some observations about the network operation.

# A. Experiment Settings

Figure 10 shows a snapshot of our testbed. In our experiment, we implement SDR on TelosB motes equipped with an MSP430 processor and CC2420 transceiver. The program memory of each node is 48K bytes and the RAM is 10K bytes. The software platform is TinyOS 2.X.

![](images/40ff15e9e192d13cc082292f786a36120b50233593749a02dd0a966b62c7b636.jpg)



Figure 10 Wireless Sensor Network Testbed

We consider two different network settings in this approach. The first one is a fixed path network in which sensor nodes are arranged in line and the route is fixed. The longest path length is 6 hops. This setting specifies a very simple network topology and we will denote this setting as Fixed-Topology setting in the following discussions. In the second network setting, we implement a full-featured sensor network which applies the CTP routing protocol for data acquisition. In this setting, sensor nodes select their parents based on ETX link measurement and the topology consists of multiple paths. Besides, the network topology exhibits high dynamics. We will refer this setting as CTP-Topology setting.

# B. Experimental results

Firstly, we conduct tests to evaluate some basic properties of our approach. In this test, we use three different data rates. In detail, the source nodes transmit a new packet every 10s, 30s and 60s. During this experiment, we collect and analyze 57121 records in all.

SDR is a two-stage approach and in the first stage it derives a sequence of delay differences. Figure 11 shows a piece of delay difference sequence in this experiment. In this figure, each data point on the Delay Difference line denotes the difference between a certain packet delay and the first packet. In this work, we use the accumulation of per-hop delays as the ground-truth of the end-to-end delays, i.e., the Measured Delay line in Fig.11. According to the results, we find the difference line exhibits almost the same shape with the Measured Delay line. Therefore, we believe that all delay values can be accurately recovered through adding a proper offset (calculated by anchor packet) to all delay differences.

![](images/4632fb55953638a5ec9ca90a434b7d16e8d7812c5a4377ad3f544a0fa6ed9899.jpg)



Figure 11 Delay differences respect to the first packet

![](images/f4f7be90159c46055e024948294994704c9d4ca41b73cf90ed4677fe48b8bbc0.jpg)



Figure 12 Estimated end-to-end delays according to different anchor packets

Figure 12 illustrates the results of recovered delay values with different anchor packets. We randomly select 3 different anchor packets and leverage their measured delays to derive the offset which is used to calculate the delay values of all other packets. From results in Fig.12, it can be concluded that the estimated delay of SDR is stable and accurate.

Consequently, we evaluate the percentage error of our approach respect to the accumulation of per-hop delays which is regarded as ground-truth. From the results in Fig.13, the measurement error of SDR achieves a mean error of 0.013% with standard variance 0.0001.

![](images/f9bdcfddef48f1e0a9142aeaf9e3c9b6debbbd7658e24294cc5ab6599a70ef90.jpg)



Figure 13 The delay estimation error of SDR

![](images/4fae86fec9e03ec8ee3a4a029f0594a1859ffc445f7183e1e02e1f5baa6fd24e.jpg)



Figure 15 End-to-end delay distribution in Fixed-Topology

![](images/9428dd6aafa8e6d4ecbb088e9228e387bc1c3bb1b1270d4b1f6c034c90416b29.jpg)



Figure 14 Convergence time of skew estimation

![](images/a782dfc78cc53a6f26f3a6cf59eb1a0d493732c093d3fa16e3d06dc5cf8d6686.jpg)



Figure 16 End-to-end delay distribution in CTP-Topology

We also conduct a group of experiments to test the convergence speed of the skew estimation scheme. As shown in Fig. 14, the estimated skew value has jitters at the beginning and becomes stable after around 30 minutes. The reason for this observation is that when the number of samples is small, the estimated skew value can be heavily affected by delay differences. As samples accumulate, the estimated skew converges to the real value.

Figure 15 and 16 show the end-to-end delay distribution in different network settings. We group these results according to the path length. In Fig.15 and Fig.16, the upper border and lower border of the box denote the 75% and 25% quantiles of the measured delay values and marks away from the box represent outliers. From the results we can find that the averaged end-to-end delay decreases linearly with path length in both network settings. The delay distribution, however, exhibits varying features in different settings. The delay values in Fixed-Topology network are uniformly distributed with small variance. Little outliers are observed. In CTP-Topology, the delay value turns to be more unstable as the path length increases. This may because that the CTP protocol continuously estimates the link qualities and selects optimal routing paths, the CTP-Topology network is more dynamic than the Fixed-Topology network and the outliers may be caused by the topology variation or routing loops.

# VI. CONCLUSION

We tackle the problem of end-to-end delay measurement in wireless sensor networks without time synchronization. To address this issue, we present a novel measurement scheme SDR tailored for data delivery delay measurement in large scale sensor networks. We also investigate key design issues in SDR such as the impact of clock drift and disordered packets. To verify the effectiveness of the proposed scheme, we implement SDR on TelosB motes and extensive experiments show that our approach achieves high precision and robustness.

# REFERENCE

[1] Y. Wang, R. Tan, G. Xing, J. Wang, and X. Tan, "Accuracy-aware aquatic diffusion process profiling using robotic sensor networks," in Proc. of IPSN, 2012.   
[2] M. Keally, Z. Gang, X. Guoliang, and W. Jianxin, "Exploiting sensing diversity for confident sensing in wireless sensor networks," in Proc. of INFOCOM, 2011.   
[3] M. Li and Y. Liu, "Underground structure monitoring with wireless sensor networks," in Proc. of IPSN, 2007.   
[4] Y. Zheng, L. Mo, and L. Yunhao, "Sea Depth Measurement with Restricted Floating Sensors," in Proc. of RTSS, 2007.   
[5] X. Kai, L. Fang, C. Xiuzhen, and D. H. C. Du, "Real-Time Detection of Clone Attacks in Wireless Sensor Networks," in Proc. of ICDCS, 2008.

[6] T. Rui, X. Guoliang, C. Jinzhu, S. Wen-Zhan, and H. Renjie, "Quality-Driven Volcanic Earthquake Detection Using Wireless Sensor Networks," in Proc. of RTSS, 2010.   
[7] T. He, P. Vicaire, T. Yan, Q. Cao, G. Zhou, L. Gu, L. Luo, R. Stoleru, J. A. Stankovic, and T. F. Abdelzaher, "Achieving Long-Term Surveillance in VigilNet," in Proc. of INFOCOM, 2006.   
[8] M. Xufei, M. Xin, H. Yuan, L. Xiang-Yang, and L. Yunhao, "CitySee: Urban CO2 monitoring with sensors," in Proc. of INFOCOM, 2012.   
[9] X. Huang and Y. Fang, "End-to-end delay differentiation by prioritized multipath routing in wireless sensor networks," in Proc. of MILCOM, 2005.   
[10] W. Qing, F. Pingyi, D. O. Wu, and K. Ben Letaief, "End-to-End Delay Constrained Routing and Scheduling for Wireless Sensor Networks," in Proc. of ICC, 2011.   
[11] M. Y. S. Uddin, F. Saremi, and T. Abdelzaher, "End-to-End Delay Bound for Prioritized Data Flows in Disruption-Tolerant Networks," in Proc. of RTSS, 2010.   
[12] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, "Collection tree protocol," in Proc. of SenSys, 2009.   
[13] B.-R. Chen, G. Peterson, G. Mainland, and M. Welsh, "LiveNet: Using Passive Monitoring to Reconstruct Sensor Network Dynamics," in Proc. of DCOSS, 2008.   
[14] N. Duffield, "Simple network performance tomography," in Proc. of the 3rd ACM SIGCOMM conference on Internet measurement, 2003.   
[15] R. R. Kompella, K. Levchenko, A. C. Snoeren, and G. Varghese, "Every microsecond counts: tracking fine-grain latencies with a lossy difference aggregator," in Proc. of ACM SIGCOMM, 2009.   
[16] O. Dousse, P. Mannersalo, and P. Thiran, "Latency of wireless sensor networks with uncoordinated power saving mechanisms," in Proc. of Mobihoc, 2004.   
[17] Y. Xue and N. H. Vaidya, "A wakeup scheme for sensor networks: achieving balance between energy saving and end-to-end delay," in Proc. of RTAS, 2004.

[18] P.-J. Wan, S. C.-H. Huang, L. Wang, Z. Wan, and X. Jia, "Minimum-latency aggregation scheduling in multihop wireless networks," in Proc. of Mobihoc, 2009.   
[19] Y. Yang, B. Krishnamachari, and V. K. Prasanna, "Energy-latency tradeoffs for data gathering in wireless sensor networks," in Proc. of INFOCOM, 2004.   
[20] G. Yu and H. Tian, "Bounding Communication Delay in Energy Harvesting Sensor Networks," in Proc. of ICDCS, 2010.   
[21] B. K. Choi, S. Moon, Z. Zhi-Li, K. Papagiannaki, and C. Diot, "Analysis of point-to-point packet delay in an operational network," in Proc. of INFOCOM, 2004.   
[22] S. Machiraju and D. Veitch, "A measurement-friendly network (MFN) architecture," in Proc. of ACM SIGCOMM workshop on Internet network management, 2006.   
[23] N. G. Duffield and M. Grossglauser, "Trajectory sampling for direct traffic observation," IEEE/ACM Trans. Netw., vol. 9, pp. 280-292, 2001.   
[24] M. Lee, N. Duffield, and R. R. Kompella, "Not all microseconds are equal: fine-grained per-flow measurements with reference latency interpolation," in Proc. of the ACM SIGCOMM, 2010.   
[25] G. Lu, N. Sadagopan, B. Krishnamachari, and A. Goel, "Delay efficient sleep scheduling in wireless sensor networks," in Proc. of INFOCOM, 2005.   
[26] Y. Gu and T. He, "Data forwarding in extremely low duty-cycle sensor networks with unreliable communication links," in Proc. of SenSys, 2007.   
[27] G. Yu, H. Tian, L. Mingen, and X. Jinhui, "Spatiotemporal Delay Control for Low-Duty-Cycle Sensor Networks," in Proc. of RTSS, 2009.   
[28] H. Kopetz and W. Ochsenreiter, "Clock Synchronization in Distributed Real-Time Systems," Computers, IEEE Transactions on, vol. C-36, pp. 933-940, 1987.   
[29] M. Maroti, B. Kusy, G. Simon, and A. Ledeczi, "The flooding time synchronization protocol," in Proc. of SenSys, 2004.   
[30] Z. Ziguo, C. Pengpeng, and H. Tian, "On-demand time synchronization with predictable accuracy," in Proc. of INFOCOM, 2011.