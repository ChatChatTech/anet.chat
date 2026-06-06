# Walking down the STAIRS: Efficient Collision Resolution for Wireless Sensor Networks

Xiaoyu Ji∗, Yuan He†, Jiliang Wang†, Wei Dong ‡, Xiaopei Wu†, Yunhao Liu†

∗ Department of Computer Science and Engineering, HKUST

† School of Software and TNLIST, Tsinghua University

‡ College of Computer Science, Zhejiang University

Abstract—Collision resolution is a crucial issue in wireless sensor networks. The existing approaches of collision resolution have drawbacks with respect to energy efficiency and processing latency. In this paper, we propose ST AIRS, a time and energy efficient collision resolution mechanism for wireless sensor networks. STAIRS incorporates the constructive interference technique in its design and explicitly forms superimposed colliding signals. Through extensive observations and theoretical analysis, we show that the RSSI of the superimposed signals exhibit stairslike phenomenon with different number of contenders. That principle offers an attractive feature to efficiently distinguish multiple contenders and in turn makes collision-free schedules for channel access. In the design and implementation of STAIRS, we address practical challenges such as contenders alignment, online detection of RSSI change points, and fast channel assignment. The experiments on real testbed show that STARIS realizes fast and effective collision resolution, which significantly improves the network performance in terms of both latency and throughput.

# I. INTRODUCTION

When multiple nodes intend to transmit packets simultaneously in the shared medium, collision happens. Unexpected collisions hurt the utilization of wireless channels, waste communication resources, and degrade network throughput. The collision problem becomes even more serious in the context of wireless sensor networks (WSNs). Being energy constrained, most WSNs employ low duty cycles [1]–[3]. For the purpose of saving energy, sensor nodes try to keep their radio off as much as possible, which squeezes the available time for packet transmissions among the nodes and potentially leads to collisions. In WSNs for event detection, e.g., [4], the unpredictable busty traffic caused by event occurrences further enlarges the chance of collisions.

A number of MAC (Medium Access Control) protocols (e.g. XMAC [5], LPL [6], RIMAC [7], AMAC [8]) are proposed to deal with collisions for WSNs. Most of those proposals basically follow the mechanism of CSMA/CA. A node senses the channel before transmission and takes random backoff in case of collision. The length of a random backoff window is designed to be exponentially increased to avoid secondary collision. The analysis in [9] shows that CSMA-based approaches can achieve acceptable performance in general wireless networks. Nevertheless, the performance may suffer serious degradation in duty cycled WSNs, especially when the network operates in uncoordinated manner with unpredictable burst traffic.

Coordination among the nodes is a helpful mechanism to avoid repeated collisions. For example, RI-MAC [7] is a receiver-initiated MAC protocol for WSNs. If collision occurs, a receiver requests multiple senders to backoff with an exponentially increasing backoff window. But that inevitably incurs large delivery latency and energy consumption. To alleviate the drawbacks of exponential backoff, the authors in [10] propose Strawman, a collision-driven channel arbitration algorithm. By analyzing the temporal characteristics of the colliding signals from multiple concurrent senders, Strawman authorizes the sender with longest straw to access the channel. The identification and collision resolution process, however, is time-consuming and inefficient with respect to energy cost, as at most one sender can be identified and win the channel access in each round. Besides, the control packets for resolving collisions have to be longer than normal and likely interfere with other packet transmissions, which further limits the network throughput.

In order to address the above issues, in this paper we propose STAIRS, a time and energy efficient collision resolution approach for WSNs. We incorporate the Constructive Interference (CI) technique in the design of STAIRS. The basic idea is based on our observations that the Received Signal Strength Indicator (RSSI) value of multiple superimposed signals with different packet lengths exhibits a stairslike pattern (refer to Fig. 1). Along with the change in the number of contenders, one can see clearly jump-downs of the RSSI value, which offers an attractive feature to distinguish multiple contenders in one round. We mainly address two key challenges in the design of STAIRS: (1) The CI requires stringent clock synchronization to function well. Though synchronization is a basic element in many WSNs and has many existing solutions, tight synchronization is energy consuming because it involves frequent control message exchanges. (2) Due to the environmental noise, the measured RSSI is unstable with frequent fluctuations, which tampers with identification of RSSI stairs. To overcome this problem, one can adopt the online Change Point Detection algorithm (CUSUM) with high detection accuracy and robustness against outliers. However, it is computation-intensive and not suitable for resourceconstrained WSNs. In our design, we implement the ACKtriggered synchronization mechanism and tailor the CUSUM algorithm. In summary, our contributions are as follows:

We identify the stairs-like RSSI phenomenon of superimposed colliding signals through observations and present

978-1-4799-3360-0/14/\$31.00 c 2014 IEEE the corresponding theoretical foundation. To the best of our knowledge, this is the first work that explores such a principle and applies it in collision resolution.

• We design the STAIRS protocol and address practical challenges in achieving the collision resolution ability. Specifically, we devise a light-weight time control module to guarantee synchronized transmission among multiple senders, so as to satisfy the first prerequisite of generating CI signals. Second, we propose a modified Change Point Detection algorithm to improve the accuracy and robustness of detecting the falling down edges of RSSI in noisy environments.   
We formulate the channel assignment problem in collision resolution with STAIRS into a Ball and Bin problem and theoretically analyze the achievable performance in comparison with CSMA. We then implement STAIRS on real sensor platforms and carry out extensive experiments for performance evaluation. The results demonstrate S-TAIRS has great advantages over the existing approaches in terms of latency and throughput. In particular, in comparison with its paralleled method Strawman, STAIRS offers up to  latency reduction and  throughput 70% 50%improvement in the multi-hop communication scenario.

The rest of this paper is organized as follows. In Section II we introduce the basic observation and its theoretical principle for the RSSI pattern under constructive interference. Section III presents the design of STAIRS based on the RSSI pattern. In Section IV, we analyze the efficiency of STAIRS from an efficiency model. Section V shows the performance of STAIRS in both testbed environment and in a large-scale simulation. The related work is presented in Section VI and we conclude this paper in Section VII.

# II. RSSI CHARACTERIZATION WITH CONSTRUCTIVE INTERFERENCE

In this section, we first briefly introduce Constructive Interference (CI) [11]. And then we provide an observation of the RSSI enhancement under CI followed by the theoretical model about this observation. At last, we discuss the potential applications in the context of collision resolution with this observation.

# A. Constructive Interference

Constructive Interference has received much attention in recent studies, most of which focus on the preconditions of generating CI, so as to the original data can be correctly reconstructed from corrupted data with higher probability. Given one communication system, such conditions are heavily dependent on the modulation scheme used in the physical layer. For example, IEEE802.15.4 standard involving specifications of physical layer and media access control for resource-limited WSNs employs an offset quadrature phase-shift keying (O-QPSK) modulation scheme [12] in the physical level. And its corresponding requirements for CI are summarized by Glossy [11] in two aspects: (1) all transmitters should send packets with identical contents; (2) the phase displacement of multiple signals must be less than 0.5 μs. Well satisfied these conditions, CI technique can be used to alleviate the ACK storm problem [13], reduce the transmission latency and improve network flooding performance [14], [11] and [15] to name just a few. Instead of improving packet reception ratio, alternatively, in this paper we try to explore the other inherent feature of superposed signals under CI and we wish to apply such features in the context of collision resolution.

![](images/21bb176a5b7d1ed55d731f956025b1fb6c4bd01e51dbd96dda33ef66017edde9.jpg)



Fig. 1. RSSI values observed at the receiver side when  senders simultakneously transmit packets with identical content to the receiver. We find that RSSI value is enhanced when the number of concurrent senders increases. A new sender joins in transmitting every 100 .

# B. RSSI Observations under CI

In telecommunications, as we know, RSSI is widely used to measure the power level of received signals by the antenna. Apparently, the superposition of multiple signals with identical waveform might exhibit some interesting features. To this end, we conduct an experiment to a receiver and observe the RSSI trend of signals under CI with $k ( k = 2 , 3 , \cdots )$ trans-( = 2 3 )mitters. For simplicity, we use CI(k) to denote k superposed CI signals1. Note that CI(k) is generated through k senders simultaneously transmitting identical packets to a common receiver, satisfying the above mentioned two CI conditions for IEEE 802.15.4 standard. The RSSI value sampled on the receiver side is shown in Fig. 1. We find in this figure that the RSSI value sampled at receiver side demonstrates an interesting trend with the increase of number of concurrently transmitting senders. The RSSI of 5 senders’ signal is stronger than the value of a single signal, which means that RSSI enhances with signal superposition. Furthermore, each newly joined signal will contribute the increase of RSSI of the superposed signal.

# C. RSSI Pattern Analysis under CI

To justify our preliminary observations, we derive the theoretical results of RSSI value of CI(k) as shown by Proposition 1. In the following analysis, we use $R S S I _ { C I ( k ) }$ to represent the RSSI value of k superposed signals under CI.

Proposition 1. Given the superposed signal CI k under CI, let $A = \{ A _ { i } \} _ { i = 1 } ^ { k }$ be the amplitude set and $B = \{ \tau _ { i } \} _ { i = 1 } ^ { k }$ denote = =the phase offset set with respect to the first signal generated by transmitter $i \ = \ 1$ . Consider one IEEE802.15.4 standard = 1based communication system, $R S S I _ { C I ( k ) }$ is equal to

$$
R S S I _ {C I (k)} = 2 0 \log \left(\sum_ {i = 1} ^ {k} A _ {i} \cos (\omega_ {c} \tau_ {i})\right),
$$

where $\omega _ { c }$ is a constant and $\tau _ { 1 } = 0 .$

Proof: We start our proof by analyzing the temporal domain waveform of signals, i.e., data chips after O-QPSK modulation. According to [16], the temporal-waveform (say: $S _ { i } ( t ) )$ of a PHY layer frame associated with transmitter i is represented as

$$
S _ {i} (t) = I (t) \sin \omega_ {c} t - Q (t) \cos \omega_ {c} t,
$$

where I t is the even-indexed chips modulated onto in-phase ( )carrier (I) and Q t is the odd-indexed chips modulated onto ( )quadrature-phase carrier (Q).

As the condition of CI is concurrently transmitting packets with identical content, this means the waveform will be identical as well. The phase offset of the k −  signals with 1respect to the first signal might be different. It is therefore that the waveform of the final superposed signal CI k in temporal domain is given by

$$
C I _ {k} (t) = \sum_ {i = 1} ^ {k} A _ {i} S _ {i} (t - \tau_ {i}), \text { with } \tau_ {1} = 0,
$$

On the receiver side, after demodulation, the waveforms at critical time points (e.g., peaks and valleys on the waveform) will be enhanced. The power gain, denoted as $P _ { k }$ , with respect to the first signal e.g., $S _ { 1 } ( t )$ is given by

$$
P _ {k} = \left(\sum_ {i = 1} ^ {k} A _ {i} \cos (\omega_ {c} \tau_ {i})\right) ^ {2}, \tag {1}
$$

For CC2420, an IEEE 802.15.4 compliant transceiver, RSSI is defined as log transformation of the received signal power, thus $R S S I _ { C I ( k ) }$ is given by

$$
R S S I _ {C I (k)} = 1 0 \log P _ {k} \tag {2}
$$

Substituting Equ. (1) into Equ. (2), we get

$$
R S S I _ {C I (k)} = 2 0 \log \left(\sum_ {i = 1} ^ {k} A _ {i} \cos (\omega_ {c} \tau_ {i})\right).
$$

Thus we complete our proof.

The above propositions states the theoretical characterization of RSSI pattern of multiple superposed CI signals in a specific communication system. However, as mentioned above, the reason for these phenomena is the DSSS modulation scheme. Therefore, these results are applicable to many other types of network system as well. For example, it can be extended in 802.11 b/g networks with DSSS modulations. Despite of lacking of practical consideration, e.g., we assume identical amplitudes for all senders, the analyzed results can match our previous observations, as shown by Fig. 1.

D. Application for Collision Resolution

All above observations motive us to build a $C I ( k )$ with k ( )senders transmitting identical content simultaneously, yet with varying lengths. As a result, the sampled RSSI value on the receiver side behaves coarsely like stairs, and each falling edge in the stairs represents an end of data transmission. Consequently, the number of potential senders can be obtained by counting the number of falling edges and these senders can even be identified by the lengths of their transmitted packets. This intentionally generated stair pattern of RSSI provides a helpful tool for collision resolution. The novelty of this stairlike pattern makes it possible to determine the channel access order among all senders in just one operational cycle, thus significantly reducing the overhead. In the following, we offer the design of this collision resolution mechanism based on the stairs behavior of RSSI, which is refereed to as STAIRS for simplicity.

# III. DESIGN OF STAIRS

In this section, we present the design of STAIRS, one collision resolution scheme based on the RSSI enhancement phenomenon. We next discuss its critical challenges in real network system and give our solutions.

# A. Protocol Overview

STAIRS is one complementary component of current MAC protocols, with the goal of resolving collision quickly and efficiently, especially for low power sensor networks with duty cycle mode. STAIRS is collision-driven, and will be executed in presence of collisions.

A visual representation of STAIRS is summarized in Fig. 2. There are in total four phases in STAIRS. Collision detection is the first phase. Upon collision is detected, a Contention Request (CR) packet is broadcasted by the receiver. Here, CR serves as an announcement for the failure of previous data transmission and also triggers the start of STAIRS.

In phase 2, all potential senders that have data for the receiver (i.e., source address of CR) immediately contend for the channel by sending one Contention Packet (CP) with random length, yet with identical payload. In addition, CP packets from multiple senders are required to be aligned at receiver side, so as to guarantee the RSSI pattern of stairs. The receiver then measures the value of RSSI and estimates all possible lengths of CP through examining the falling edges of RSSI value. Note that in this process, the carrier sensing function in CSMA is disabled to enable the concurrent transmissions of CP [17].

In phase 3, STAIRS switches into the schedule phase. In particular, the receiver sends one Schedule Packet (SP) including one estimated CP length. And any sender whose CP length equals to the length carried in the SP packet wins the channel access.

In phase 4, the winner transmits a data packet to the receiver and then it is acknowledged by an ACK from the receiver if the transmission is successful. Similarly, this ACK has two functions. First, it is to confirm the correct receipt of the previous data transmission. Second, it is used to invite another new sender that is identified in the contention phase to transmit. In this way, all the senders that are identified in the contention phase will have chances to transmit their packets. When all detected senders finish transmission in this round, the receiver uses another CR for a new round of contention. This CR is not only used to confirm the last data packet, but also to notify the end of this round and the start of a new round.

![](images/1d8b1284971d19eda00071aad0f12d2d0f2b98f3a5df314ff39cd6ef161f290a.jpg)



Fig. 2. Workflow of STAIRS. It mainly consists of collision detection, contention, schedule and data transmission phases.

Note that there are two problems to be pointed out in STAIRS. The first problem is that data collision might occur in the data transmission phase when more than one sender choose the same length of CP. In this condition, multiple senders will transmit at the same time, which causes collisions. Another problem is that there are false positives, i.e., false falling edges, in the detection. These false edges are from two aspects. First, the fluctuations of RSSI in measurement may contribute to the false falling edges. Second, external interference, e.g., interference from 802.11 Wifi networks may generate some falling edges. Either cases mislead the receiver to detect the actual existence of potential senders. In Section IV, we give deep analysis to the influence from the above two problems and talk about the solutions in the design of STAIRS.

The design of STAIRS faces two challenges. First, the CP packets of senders should be well aligned to meet the requirement of CI, i.e., the offset is no more than 0.5 μs. The second challenge is as mentioned above, receiver needs to accurately detect the falling edges to estimate the number and IDs (the length of their CP packets) of senders. This is highly non-trivial due to the unpredictable physical environmental noise (e.g., interference from other wireless activities). We discuss our solutions to the above challenges in the following sections in detail.

# B. Alignment of CP Packets

Recall that STAIRS is built on the CI technique. As we mentioned above, the success of CI needs strict clock synchronization. Although such requirement is an essential feature of many sensor networks, tight synchronization is energy consuming because it needs frequent control message exchanges. More importantly, their synchronization accuracy can only be several micro-seconds, which doesn’t satisfy the CI requirement.

To meet this precondition of CI, we require that CP packets should be transmitted as quickly as possible after the CR packet is received. Before the transmission of CP, the time duration can be divided into two parts: (1) the propagation time of broadcasting CR, and (2) the time of receiving CR. Compared with (2), propagation time is negligible due to the high propagation speed of wireless signal.

![](images/eecf32bb164c380659c3f8ce2c324eeb2e4a7300117c41776dc8ab4ec4484643.jpg)



Fig. 3. The illustration for CP packet alignment. We parallelize the receiving process from antenna to RX buffer and the process of reading from RX buffer to MCU memory. Besides, we set a unified delay from the end of reception to the start of CP transmission.

Before discussing the second time span, we revisit the complete data reception process of CC2420, one widely used IEEE 802.15.4 compliant RF transceiver. In general, this process is done in two steps: packet temporary reception and data buffer reading. Specifically, transceiver first receives the signal via the antenna and stores the received signal in a temporary Rx buffer. After receiving the packet, the buffered data is transferred to MCU memory through SPI. Thus the reception time of CR consists of: (1) the duration of reading CR packet from antenna to RX buffer and (2) the duration of reading CR packet out of RX buffer to MCU memory.

Ideally, the above two processes are serial. However, we observe that different primitive operations commands with various delays are usually executed between them. This results in the difference of CR receiving time and further affects the synchronization of CP transmission. We therefore introduce the pipelining technique to parallelize these two processes, as shown by Fig. 3. Here, the packet temporary reception denoted as SFD will be activated by the rising edge of SFD pin. Then the data reading process is immediately started. Such two process lasts for a while until the end of the receiving packet. In this way, the time for data buffer reading could be completely removed. Note that time duration for receiving CR packet across senders is deterministic and identical, which only depends on the length of the receiving packet. Therefore, the instant of accomplishing CR reception can be well aligned.

Note that above techniques can synchronize the moment of receiving CR across multiple senders. However, due to the hardware internal interrupt, CP packets are not often scheduled immediately. Instead, they defer for a short and nondeterministic while, usually referred as software delays. Here, our strategy is to let all senders wait for a fixed while, which is longer than the potential maximal software delay, so that the start point of CP packets can be well aligned. We thus achieve the goal of simultaneously scheduling CP packets from multiple senders.

# C. Falling Edges Detection

As mentioned, the key idea of STAIRS is to estimate the lengths of intentionally collided CP packets to arbitrate the channel access order. Due to the stairs-behavior of RSSI, the receiver is capable of computing the time duration between two adjacent falling edges, which is an indication of CP length.

In this subsection, we introduce one efficient approach to estimate the location of falling edges.

In a sense, the problem of detecting falling edges falls in the same category of change point detection (also known as edge or jump detection) which has been extensively studied in statistics and signal processing. And numerous studies have done to develop various algorithms to effectively determine the change point for one discrete signal or a group of sequence data, see e.g., [18] for a nice summary. These are generally classified into online and offline. Obviously, the online version might be more attractive for our specific application.

In our real implementation, we choose the classical online change point detection algorithm called CUSUM method [19]. The reason we consider CUSUM is due to its detection accuracy and robustness against outliers. However, CUSUM involves intensive recursion and its computation complexity will increase as the number of data points grows. In addition, the receiver has no prior knowledge about the CP length. To effectively capture the falling edges, the receiver is required to frequently sample the underlying RSSI. These might impose a huge challenge to the resource-limited sensor nodes.

To reduce the overhead in computation and diminish the chances of false positives, we set the length of CP to be on the granularity of $\Delta L$ bytes, e.g., $\Delta L = 1 0$ in our implementation. Δ Δ = 10By doing so, the RSSI sampling frequency and computation complexity of CUSUM could be significantly reduced without sacrificing the detection performance. In the evaluation part, we experimentally verify the efficiency of this solution.

# D. Discussions

1) Robustness to Hidden Terminals: We claim that STAIRS has the robustness against the hidden terminal problem in wireless networks. Hidden terminals may cause packet collision when the senders without sensing the existence of each other transmit concurrently. However, in STAIRS, senders are explicitly contending for the channel, their transmission order is totally decided by the contending result. Therefore this receiver-initiated transmission mode in STAIRS can efficiently overcome the problem of hidden terminals.   
2) Fairness: STARIS also does well in fairness. Fairness lies in the fact that senders randomly choose the lengths of their CP packets. As a result, the transmission orders for senders are different in each round. In a long run, senders evenly share the channel to the receiver.   
3) Limitations: As a protocol for collision resolution, S-TAIRS has some limitations to be stated. First, it is better to apply STAIRS in scenarios with high node density and intensive traffic. In these situations, collisions happen frequently. While in sparse and low data rate networks, we observe that advantages of STAIRS diminish and CSMA backoff mechanism demonstrates efficiency in its simplicity. Second, because carrier sensing is disabled in STAIRS, transmission is vulnerable to external interference, e.g., interference from 802.11 networks. These external interferences may generate false falling edges that affect the efficiency of STAIRS.

![](images/b0d9fa54ab75aa9dc45e58d1d201f71f592ec611c2d4f22d1e7a2e38a8595d90.jpg)



Fig. 4. The relationship between $\Delta L$ and efficiency of collision resolution. LFor different , the optimal Δ is different.

# IV. EFFICIENCY ANALYSIS

In this section, we give theoretical analysis about the efficiency of resolving collision with STAIRS. For convenience, we divide time into a series of slots. In 802.15.4 networks, for example, a slot is the duration of transmission of one byte. A packet duration can be composed of multiple slots.

The efficiency of collision resolution in STAIRS is dependent on the detection accuracy of falling edges and the subsequent data transmissions. Both the case when multiple senders choose CP packets with the same length and the case when false falling edges are detected affect the collision resolution efficiency. Suppose the total number of senders is N, and the maximum length for the CP packet is $L .$ If we set the step equal to $\Delta L$ , then the space for the possible lengths of CP is $S = \{ \Delta L , 2 \Delta L , . . . m \Delta L \}$ , where $m = L / \Delta L$ = Δ 2Δis the size of the space. The value of $\Delta L$ is a key = Δparameter here. As is discussed above, larger $\Delta L$ Δcan decrease Δthe possibility of false positive, while resulting in a larger possibility of collision. Therefore in the following content, we try to formulate the efficiency of resolving collision as a function of $\Delta L$ .

ΔGiven the N senders and the m possible lengths, this problem is like a ball-and-bin game. Our objective is trying to allocate the N balls into the m bins evenly such that for each bin there is only one sender with high probability [20]. The constrain is that we should use as less bins as possible. The allocation of bins in the contention period directly relates to the data transmission in the transmission period [21]. According to the allocation of CP lengths to senders, we observe that there are three possible schedules:

• Empty schedule: in which there is no sender transmitting. This is caused by the false positives of falling edges detected during the contention period.   
• Success schedule: where there is exactly one sender transmitting in the scheduled slots.   
Collision schedule: where more than one senders transmit packets and collision happens.

Then we denote the possibilities for the above three schedules as $P _ { i } , P _ { s }$ and $P _ { c } .$ . And we further denote the possibility for a sender to choose any of the m lengths as $p = 1 / m$ . So we have:

$$
P _ {i} = \alpha (1 - p) ^ {N} \tag {3}
$$

where α is the possibility of false positives in the detection process. The probability of success schedule is as follows:

$$
P _ {s} = N p (1 - p) ^ {N - 1} \tag {4}
$$

and the probability of collision schedule is therefore:

$$
P _ {c} = 1 - P _ {i} - P _ {s} \tag {5}
$$

Then we can calculate the efficiency of STAIRS with the above possibilities. The number of successfully transmitted packets is $N _ { s } = m P _ { s }$ , the number of collided packets is $N _ { c } =$ m $P _ { c }$ =and the number of empty schedules is $N _ { i } = m P _ { i }$ =. Note that before each schedule, a $\mathrm { S P }$ = packet is needed, thus the schedule overhead is:

$$
T _ {s c h} = (N _ {s} + N _ {c} + N _ {i}) T _ {s p} \tag {6}
$$

where $T _ { s p }$ is the length of a SP packet. Besides the time cost in data transmission and waiting, the time cost in contention $T _ { c o n t }$ should also be counted and this time can be approximated as $T _ { s }$ . For a specific number of senders N, the efficiency η can be represented based on the above formulas:

$$
\eta = \frac {N _ {s} T _ {s}}{N _ {s} T _ {s} + N _ {c} T _ {c} + N _ {i} T _ {\text {wait}} + T _ {\text {sch}} + T _ {s}} \tag {7}
$$

where $T _ { s }$ is the average length of successfully transmitted packets and $T _ { c }$ is the length of collided packets. We use $T _ { w a i t }$ to denote the time to wait in face of an empty schedule.

Equ. 7 reveals the efficiency of resolving collision in S-TAIRS is the ratio of data transmission time to the total time. From another view the inverse of Equ. 7 is the average number of rounds needed for all senders to finish their transmissions. To calculate the optimal $\Delta L$ for a specific N, we can set the Δderivative of Equ. 7 to 0, and thus optimal $\Delta L$ should be:

$$
\Delta L ^ {o p t} = \underset {\Delta L} {\arg \max} \eta \tag {8}
$$

Fig. 4 plots the corresponding $\Delta L ^ { o p t }$ for $N = 5 ,$ 10 and 20 Δrespectively. In this figure, we set $\alpha = 1$ = 5, i.e., in each empty = 1schedule, their is a falsely-detected falling edge and therefore the figure gives a lower bound of the optimal efficiency η. We can find that for different N, the optimal L is different. Specifically, the step $\Delta L$ is 10 bytes when $N = 5$ , it is 5 when $N = 1 0$ Δ, and it decreases to 2 when $N = 2 0$ 5. Optimal $\Delta L$ = 10decreases with the increase of N.

# V. IMPLEMENTATION AND EVALUATION

In this section, we introduce the evaluation of STAIRS in both real testbed and large-scale simulation. We first validate the feasibility of STAIRS by examining the results of synchronization and detection accuracy of falling edges. Then we compare STAIRS with the state-of-the-art protocol Strawman [10] on real testbed. Finally we extend the evaluation in a large scale simulation environment for further analysis. The Clear Channel Assessment (CCA) is set to  dBm and according 77to the specification of 802.15.4, each packet has a maximum length of 128 bytes in which the payload is at most 110 bytes.

![](images/bbc48d76c604710bd62b5e40572eb9e9efbe5a98681d485218c71a709a739451.jpg)



![](images/f19a14d246720c3ef589e534a6325e2f69de07c44bbc395b0fb3ec7c214689c2.jpg)



(b)   
Fig. 5. Micro-benchmark evaluation of STAIRS. Fig. 5(a) shows the offset of packet transmissions among senders and Fig. 5(b) gives the detection time before and after CUSUM is revised.

# A. Micro-Benchmark Evaluation

We first evaluate the micro-benchmark performance of STAIRS. Namely, we want to evaluate (1) how well the mechanism in STAIRS can align senders’ packets, (2) what is the cost in edge detection and (3) what is the accuracy of edge detection.

1) Experiment Settings: We use six nodes in this experiment. 5 nodes transmit packets upon receiving the CR packet form the receiver. Each sender randomly chooses the CP packet length with $\Delta L = 1 0 \mathrm { b y t e s }$ . We measure the time offset Δ = 10among sender’ packets and record the time taken in detecting the falling edges. Based on the ground truth, we calculate the detection accuracy by dividing the actual number of senders by the number of detected falling edges. We repeat the test for 20 rounds and calculate the average values of the above mentioned metrics.

2) Experiment Results: Fig. 5(a) shows the time offset of five senders with respect to a reference node. We find that the mean value of offset among senders is very small, and all the results are smaller than . $\mu s ,$ which is required by 0 5the constructive interference. Fig. 5(b) shows the time cost in detecting the falling edges. In this figure, we can see that the detection time is dependent on the total number of senders. Specifically, the time to detect one sender is only 2.5 ms in average, while it increases to ms when $N = 5$ . This 12 = 5is because the CUSUM detection algorithm need to perform multiplication operations and it runs in an recursive way. The revised CUSUM, i.e., S-CUSUM does better in detection efficiency, with detection time decreased to  ms when $N = 5$ .

![](images/2663b00968b08c62bcea5e3b8b96a478d7800fa0d2ff3a6f1085c4e98b40e8c6.jpg)



(a)

![](images/f2d40c85e0f68b31eca06abb4d23b8a18e558c518732294165c82c57f0930774.jpg)



![](images/ec6fc90a4b570a6b79423f614184c3939011f334669767e5cbbf59180952a3c7.jpg)



![](images/f0a46a29bea8f7f14e80140a3e828b8f85709539a3ceef0990e052cf75515488.jpg)



Fig. 6. Performance comparison with Strawman in a multi-hop-multi-flow scenario. Fig. 6(a) shows the completion time. Fig. 6(b) depicts the overhead of both protocols. In Fig. 6(c), sender duty cycles are shown and receiver duty cycles are compared in Fig. 6(d)

TABLE I DETECTION ACCURACY. 

<table><tr><td>Accuracy (%)</td><td>N = 1</td><td>N = 2</td><td>N = 3</td><td>N = 4</td><td>N = 5</td></tr><tr><td>Avg.</td><td>98.2</td><td>85.0</td><td>89.8</td><td>90.3</td><td>84.7</td></tr><tr><td>Min.</td><td>87.3</td><td>71.5</td><td>69.4</td><td>70.3</td><td>71.7</td></tr><tr><td>Max.</td><td>100</td><td>95.0</td><td>93.8</td><td>90.3</td><td>94.7</td></tr></table>

The detection accuracy is shown in Tab. I. It is easy to find that detection accuracy is not directly related to the number of senders. The general detection accuracy is around  for 90%all the 5 cases. We further verify and find that the error of detection accuracy is mainly from false edges caused by RSSI fluctuation and extern interference. Therefore it is desirable to choose a proper L.

# B. Evaluation in a Multi-hop Network

The realistic WSNs always run in an multi-hop way for a large sensing coverage, and data packets need to be relayed by multiple relay nodes. Considering this property of WSNs, we evaluate the performance of STAIRS on an indoor testbed. We set the power level of RF chip to a low level such that nodes can only communicate with the neighbors in one hop.

1) Experiment Settings: The testbed environment is shown in Fig. 7. We use 20 TelosB nodes to form a multi-hopmulti-flow network. In this network, each column of nodes is a flow, thus there are totally 4 flows in this network. Each row of nodes form a level within which senders have mutual interference with each level. In each flow, a packet need to be transmitted over three hops from level A to level D. We imitate a scenario of packet transmission from the bottom level, i.e., level A to the top level, i.e., level D in an multi-hop manner. And each sender in the bottom transmits 10 packets. The wakeup period is set to 10 ms for both receiver and senders.

2) Evaluation Metrics: We compare STAIRS with Strawman protocol, a state-of-the-art protocol for collision resolution. In Strawman, senders explicitly contend and the contention ends with a winner who has the longest contention packet. The contention process goes on until all senders finish transmissions. As a receiver-initiated protocol, Strawman is thought to perform well in coping with collision. The metrics in this multi-hop experiment are as follows:

Completion time: total time used to transmit the packets of level A to the top level D.

![](images/149c39c2ee178c95b3bb0fe7ab071eaef5f2008eb2f6ac8efe7bde2c3603d3fd.jpg)



Fig. 7. The testbed environment.

• Efficiency: here we consider efficiency by measuring the overhead in collision resolution. Overhead mainly consists of control overhead and the overhead incurred by invalidation of protocols, e.g., the collision and waiting time.   
• Duty cycle: ratio of time when nodes are transmitting to the total time.

3) Evaluation Results: Fig. 6(a) demonstrates the completion time of Strawman and STAIRS. We find that in the multihop case, STAIRS completes transmission much faster than Strawman does. Specifically, when there is only one flow, i.e., there is no mutual interference from other nodes in other flows, the completion time for both Strawman and STAIRS is short. With the increase of the number of flows, though the completion time of Strawman and STAIRS both increase, STAIRS increases more slowly than Strawman does. This demonstrates STAIRS’s efficiency in scheduling transmissions, especially in networks with high node density.

Fig. 6(b) shows the efficiency comparison. As contention becomes more serious with the increase of flow number, Strawman suffers from the serious contention. The incurred overhead increases to about  when flow number is 4. That 20%is because Strawman can only schedule one sender in each round. On the contrary, STAIRS shows an opposite trend. The overhead of protocol decreases with the increase of number of flows. The reason is that STAIRS is able to schedule almost all the senders in only one round. STAIRS becomes more efficient when there are more contending senders as the constant overhead is amortized to the subsequent transmissions.

Fig. 6(c) and Fig. 6(d) show the duty cycle on sender and receiver side. We find that the sender duty cycle increases with the growing of number of flows for both STAIRS and Strawman. The same trend appears also in receiver duty cycle. The increase of duty cycle is due to the fact that nodes spend more time in handling collisions when there are more flows. Though nodes have more time in wake-up mode when flow number increases, it is apparent that STAIRS has relatively smaller duty cycles on both receiver and sender side compared with Strawman. The essential reason is that STAIRS has higher efficiency in collision resolution than Strawman does.

![](images/3a09468228345f5de2188db679e9d763d9151a560b842b175e02eb1998a507f3.jpg)



Fig. 8. Throughput comparison, pkt size = 50.

# C. Large-scale Simulation

To test the performance of STAIRS in large scale networks, we conduct a simulation based on the model in Section IV. Here we also simulate the performance of linear backoff (Backoff-L) and exponential backoff (Backoff-E) mechanism that are adopted in CSMA protocols. Moreover, as mentioned in Section III, we claim there is a tradeoff between backoff mechanism and STAIRS. In this simulation based evaluation, we want to quantify this tradeoff.

1) Simulation Settings: We simulate a network which is one-hop. In this network, there is a receiver and up to 50 senders around the receiver. We set the power of nodes large enough such that nodes have mutual interference with each other. In other words, up to 50 senders contend the channel to the receiver. Based on these settings, we respectively simulate the performance of linear backoff and exponential backoff based protocols in 802.15.4 networks and compare their performance with STAIRS.

The simulation tool we used is MATLAB R2012a, considering this simple network topology. The parameter settings are summarized in Tab. II. In this table, P hyRate represents the effective data rate in physical layer. InitCW and M axCW are the initial and maximum size of the contention window. Besides the settings mentioned in Tab. II, we apply a poisson distribution for the packet arrival time. Average packet size is set to 50 and 100 bytes respectively considering the effect from packet lengths [22]. Based on all the settings above, we record total time spent in transmitting 1000 packets to get the final throughput. The final results are plotted in Fig. 8 and Fig. 9.

2) Results: Fig. 8 plots the throughput comparison with packet size equal to 50. We can find that when number of

![](images/2ebbe798379881d602d87c61d02ead7ee0ac3438d16cff0c40d57704d9148415.jpg)



Fig. 9. Throughput comparison, pkt size = 100.

TABLE II PARAMETERS SETTINGS. 

<table><tr><td></td><td>Backoff - L</td><td>Backoff - E</td><td>STAIRS</td></tr><tr><td>PhyRate(bps)</td><td>256k</td><td>11M</td><td>256k</td></tr><tr><td>SlotTime(us)</td><td>32</td><td>9</td><td>32</td></tr><tr><td>InitCW(slots)</td><td>5</td><td>10</td><td>5</td></tr><tr><td>MaxCW(slots)</td><td>32</td><td>64</td><td>32</td></tr><tr><td>DIFS(us)</td><td>-</td><td>34</td><td>-</td></tr><tr><td>SIFS(us)</td><td>-</td><td>16</td><td>-</td></tr></table>

senders is small, performance of both linear and exponential backoff are good. Especially when N , i.e., there is no = 1collision, backoff mechanisms have higher throughput than STAIRS does. However, when N exceeds 3, the throughput of backoff mechanisms degrades with the increase of number of senders. On the contrary, STAIRS has significantly larger throughput with large number of senders. In the case where packet size is 100 as shown in Fig. 9, we can find the same trend. A remarkable difference is that the critical point occurs when N . The advantages of STAIRS is that it is able to = 5efficiently resolve collision based on the delicate contention mechanism without incurring the overhead of backoff.

# VI. RELATED WORK

Collision resolution receives extensive attention and is tackled from various aspects in the literature. Researchers have proposed a lot of protocols and mechanisms across different network layers. Here we have a brief discussion about the existing proposals and summarize them in the following four classes:

Carrier sensing and backoff. Most existing work resolves collisions in the MAC layer. MAC layer protocols, such as receiver-initiated RI-MAC [7], A-MAC [13], and senderinitiated B-MAC [1] and X-MAC [5] all exploit basic carrier sensing to guarantee that in a specific time slot there should be no more than one sender transmitting, the other senders need to perform random backoff to avoid collision. The limitation of those protocols is that they work well only in the situation where the number of senders is limited. When the number of senders increases, the efficiency of backoff-based mechanisms degrades, because backoff incurs significant overhead to avoid collisions.

Schedule-based protocols. Another thread of MAC layer protocols focus on scheduling senders to eliminate collisions. TCF [23] gets rid of contention overhead of CSMA by allocating the channel resource dynamically. ZMAC [24] proposes a hybrid protocol that combines CSMA and TDMA to be adaptive to varying traffic load. However, at the cost of remarkable overhead incurred by synchronization and coordination, those protocols have limited applicability in large-scale sensor networks.

Collision resolution via explicit contention. Some other protocols tackle the collision problem by explicit contention. Strawman [10] proposes a new contention mechanism of drawing straws. The winner of contention is determined according to the length of the contention packets senders send. This guarantees that there is always a node granted to access the channel, which provides the ability for collision resolution. But the extra overhead in conduct contention is considerable as each round of contention can only support one packet transmission. On the other hand, some papers utilize PHY layer information to enable efficient contention. BACK2F [25] leverages OFDM sub-carriers and transfers channel contention from the time domain to the frequency domain. In this way, senders can be identified and thus batched transmissions without collision become possible. Unfortunately, these protocols require modification to the PHY layer thus they are difficult to be used in practice [26].

STAIRS is also working along the idea of explicit contention, yet needs little modification on the MAC layer and PHY layer and therefore it can be directly used on off-theshelf hardware. We believe that STAIRS is a departure from the established ideas.

# VII. CONCLUSION AND FUTURE WORK

This paper proposes STAIRS, an efficient collision resolution mechanism for WSNs. We first present solid analysis about the phenomenon of RSSI enhancement of multiple concurrent senders under constructive interference. Based on this observation, we design a protocol with explicit contention for collision resolution. We evaluate the performance of STAIRS in both multi-hop-multi-flow scenario and in large-scale simulation. Results show that STAIRS has higher efficiency in collision resolution, especially in networks with high node density and intensive traffic. Several issues are left for future study. First, we plan to explore deeper about the relationship between RSSI and the number of senders under constructive interference. Second, we will make this protocol applicable to a variety of scenarios with different system settings and deployments. We also plan to port the current implementation of STAIRS to 802.11 networks with different modulation schemes.

# ACKNOWLEDGEMENT

This study is supported in part by NSFC Distinguished Young Scholars Program under grant of 61125202, National High-Tech R&D Program of China (863) under grant of 2011AA010100, National Basic Research Program (973 program) under grant of 2014CB347800 and NSFC under grants of 61170213, 61202359, 61373166 and 61202402, and the Research Fund for the Doctoral Program of Higher Education of China (20120101120179).

# REFERENCES

[1] W. Ye, J. Heidemann, and D. Estrin, “An energy-efficient mac protocol for wireless sensor networks,” in IEEE INFOCOM, 2002.   
[2] X. Wu and Y. Wu, “Near-optimal working slots selection for a sensor via sub-modularity,” in IEEE WiCom, 2009.   
[3] X. Wu and M. Liu, “In-situ soil moisture sensing: Optimal sensor placement and field estimation,” Sensor Networks, ACM Transactions on, 2012.   
[4] D. E. Phillips, R. Tan, M.-M. Moazzami, G. Xing, J. Chen, and D. K. Y. Yau., “Supero: A sensor system for unsupervised residential power usage monitoring,” in IEEE PerCom, 2013.   
[5] M. Buettner, G. V. Yee, and R. Han, “X-mac: a short preamble mac protocol for duty-cycled wireless sensor networks,” in ACM SenSys, 2006.   
[6] J. Polastre, J. Hill, and D. Culler, “Versatile low power media access for wireless sensor networks,” in ACM SenSys, 2004.   
[7] Y. Sun, O. Gurewitz, and D. B. Johnson, “Ri-mac: a receiver-initiated asynchronous duty cycle mac protocol for dynamic traffic loads in wireless sensor networks,” in ACM SenSys, 2008.   
[8] P. Dutta, S. Dawson-Haggerty, Y. Chen, C.-J. M. Liang, and A. Terzis, “Design and evaluation of a versatile and efficient receiver-initiated link layer for low-power wireless,” in ACM SenSys, 2010.   
[9] J. Wang, W. Dong, Z. Cao, and Y. Liu, “On the delay performance analysis in a large-scale wireless sensor network,” in IEEE RTSS, 2012.   
[10] F. Osterlind, L. Mottola, T. Voigt, N. Tsiftes, and A. Dunkels, “Strawman: resolving collisions in bursty low-power wireless networks,” in IEEE/ACM IPSN, 2012.   
[11] F. Ferrari, M. Zimmerling, L. Thiele, and O. Saukh, “Efficient network flooding and time synchronization with glossy,” in IEEE/ACM IPSN, 2011.   
[12] WiKipedia web site, 2012. [Online]. Available: http://en.wikipedia.org/ wiki/Phase-shift keying   
[13] P. Dutta, S. Dawson-Haggerty, Y. Chen, C.-J. M. Liang, and A. Terzis, “Design and evaluation of a versatile and efficient receiver-initiated link layer for low-power wireless,” in ACM SenSys, 2010.   
[14] J. Lu and K. Whitehouse, “Flash flooding:exploiting the capture effect for rapid flooding in wireless sensor networks,” in IEEE INFOCOM, 2009.   
[15] X. Zhang and K. Shin, “Chorus: Collision resolution for efficient wireless broadcast,” in IEEE INFOCOM, 2010.   
[16] Y. Wang, Y. He, X. Mao, Y. Liu, Z. Huang, and X. Li, “Exploiting constructive interference for scalable flooding in wireless networks,” in IEEE INFOCOM, 2012.   
[17] M. Sha, G. Xing, G. Zhou, S. Liu, and X. Wang, “C-mac: Modeldriven concurrent medium access control for wireless sensor networks,” in IEEE INFOCOM, 2009.   
[18] WiKipedia web site, 2013. [Online]. Available: http://en.wikipedia.org/ wiki/Step detection   
[19] W. A. Taylor. Change-point analysis: A powerful new tool for detecting changes, 2000. [Online]. Available: http://www.variation.com/cpa/tech/ changepoint.html   
[20] Y. Tong, L. Chen, and B. Ding, “Discovering threshold-based frequent closed itemsets over probabilistic data,” in ICDE, 2012.   
[21] Y. Tong, L. Chen, Y. Cheng, and P. S. Yu, “Mining frequent itemsets over uncertain databases,” in VLDB Endowment, 2012.   
[22] W. Dong, X. Liu, C. Chen, Y. He, G. Chen, Y. Liu, and J. Bu, “Dplc: Dynamic packet length control in wireless sensor networks,” in IEEE INFOCOM, 2010.   
[23] C. Lim and C.-H. Choi, “Tdm-based coordination function (tcf) in wlan for high throughput,” in IEEE GLOBECOM, 2004.   
[24] W. Rhee, I., M. A., Aia, and Min, “Zmac: A hybrid mac for wireless sensor networks,” in ACM SenSys, 2005.   
[25] S. Sen, R. Roy Choudhury, and S. Nelakuditi, “No time to countdown: migrating backoff to the frequency domain,” in ACM MobiCom, 2011.   
[26] Z. Li, D. Pu, W. Wang, and A. Wyglinski, “Forced collision: Detecting wormhole attacks with physical layer network coding,” in IEEE Tsinghua Science and Technology, 2011.