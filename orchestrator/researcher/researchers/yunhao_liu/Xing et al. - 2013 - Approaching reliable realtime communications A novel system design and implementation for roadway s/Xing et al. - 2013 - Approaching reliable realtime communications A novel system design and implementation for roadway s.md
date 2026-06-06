# Approaching Reliable Realtime Communications? A Novel System Design and Implementation for Roadway Safety Oriented Vehicular Communications

Kai Xing∗, Tianbo Gu∗, Zhengang Zhao∗, Lei Shi†, Yunhao Liu‡, Pengfei Hu∗, Yuepeng Wang∗, Yi Liang∗ Shuo Zhang∗ Yang Wang∗, Liusheng Huang∗, ∗University of Science and Technology of China, Anhui, China 230027

mail: {kxing,gavin,angyan,lshuang}@ustc.edu.cn, gu,pfh, wangyuep,yiliang,zshuo}@mail.ustc.edu.cn fei University of Technology, Anhui, China 230009 Email: thunder10@163.com

‡Tsinghua University, Beijing, China 100084 Email: yunhao@greenorbs.com

Abstract—Though there exist ready-made DSRC/WiFi/3G/4G cellular systems for roadway communications, there are common defects in these systems for roadway safety oriented applications and the corresponding challenges remain unsolved for years, i.e., WiFi cannot work well in vehicular networks due to the high probability of packet loss caused by burst communications, which is a common phenomenon in roadway networks; 3G/4G cannot well support real-time communications due to the nature of their designs; DSRC lacks the support to roadway safety oriented applications with hard realtime and reliability requirements [1].

To solve the conflict between the capability limitations of existing systems and the ever-growing demands of roadway safety oriented communication applications, we propose a novel system design and implementation for realtime reliable roadway communications, aiming at providing safety messages to users in a realtime and reliable manner. In our extensive experimental study, the latency is well controlled within the hard realtime requirement (100ms) for roadway safety applications given by NHTSA [2], and the reliability is proved to be improved by two orders of magnitude compared with existing experimental results [1]. Our experiments show that the proposed system for roadway safety communications can provide guaranteed highly reliable packet delivery ratio (PDR) of 99% within the hard realtime requirement 100ms under various scenarios, e.g., highways, city areas, rural areas, tunnels, bridges. Our design can be widely applied for roadway communications and facilitate the current research in both hardware and software design and further provide an opportunity to consolidate the existing work on a practical and easy-configurable low-cost roadway communication platform.

# I. INTRODUCTION

In our daily lives, one most overriding concern on the road is safety. Though great effort has been made on roadway safety for years, the total number of fatalities and injuries involved in motor vehicle traffic crash in the world remains high, as reported by WHO [3], [4] (World Health Organization), BTS [5] (Bureau of Transportation Statistics) and FARS [6] (Fatality Analysis Reporting System). The high fatality/injury and involved asset damage result in enormous economic losses, which emphasize the necessity and importance of new technologies to roadway safety.

To improve the roadway environment in the aspects of safety enhancements, Inter-vehicle Communications (IVC) systems are proposed as an enabling technology for roadway safety. Wireless access in vehicular environments (WAVE), which is based on the Dedicated Short Range Communications (DSRC) standard (IEEE 802.11p Standard), is the latest IVC technology that provides the physical platform for ITS (Intelligent Transportation System) to achieve its claimed goals of safety, management and data services.

In these communication protocols and technologies, from the perspective of roadway safety communications the fundamental performance metrics are packet delivery ratio and latency. Specifically, NHTSA (National Highway Traffic Safety Administration) has identified a number of high priority safety applications for DSRC-equipped vehicles, e.g., traffic signal violation, emergency brake lights, pre-crash sensing, collision warning, left turn assistance, lane change warning, stop sign assistance, curve speed warning, most of which require singlehop communications that the latency is required to be less than 100 ms and the packet delivery ratio is higher than 99%, where the packet length is usually 64 bytes or less [2], [7].

However, most recent results in [1] show that DSRC lacks the ability to fulfill the requirements of these roadway safety applications, i.e., it is common in realistic roadway environments to observe poor ( 20%) or intermediate ([20%, 80%]) packet reception (or gray-zone phenomenon), which is far from satisfying the 99% packet reception requirement. Furthermore, due to the burst communication nature of roadway safety applications and the unreliable packet reception characteristics of DSRC, realtime roadway communications (< 100 ms) is still far away in realistic roadway safety environments at the

current stage.

This paper proposes a novel communication system for roadway safety oriented communications for single-hop roadway safety communications, e.g., emergency brake lights, collision warning, left turn assistance, lane change warning, stop sign assistance, curve speed warning, etc. The goal of this system is to develop a low-cost, promptly-deployable wireless communication system for realtime and reliable communications for roadway safety oriented applications. Our idea leverages the advanced wireless communication and vehicular technologies, and further the sensing technologies. Specifically, we developed a novel reliable realtime roadway communication system based on our carrier sensing, channel allocation, multi-channel radios and chips designs, etc. The major contributions of this paper are identified as follows:

Highly reliable communications: Our system can stably achieve a highly reliable packet delivery ratio of 99% under various scenarios, e.g., highways, city areas, rural areas, tunnels, bridges. The reliability (in terms of packet loss rate) is improved by two orders of magnitude compared with existing experimental results [1]   
Ultra low latency: The extensive experimental study under different scenarios shows that the latency of any arbitrary vehicle/road-side unit which successfully delivers a packet to its neighbors in vehicular networks is well controlled within 100ms.   
• Burst traffic: In the worst case that multiple neighboring vehicles send their messages on the same channel at the same time, our system can still stably provide 99% PDR within 100ms. Specifically, we have verified in the 5-to-1 scenario (i.e., 5 senders and 1 receiver on the same channel).

The rest of the paper is organized as follows: Section II presents the related works. Section III is devoted to the development of our MAC design. Section IV provides the details of our system design and implementation. Section IV-C reports our experimental results, followed by the conclusions in Section V.

# II. RELATED WORK

In this section, we briefly summarize the most relevant existing works.

In intelligent transportation systems (ITS), roadway safety oriented applications [8]–[11] pose a strict requirement of communication latency and reliability. Unfortunately, the medium access control and related techniques [12], [13], e.g., CSMA/CA used in 802.11p, cannot provide the guarantee of hard realtime communications. To overcome this issue, many approaches are proposed. For example, [14] [15] propose the self-organizing time division multiple access(STDMA) scheme that outperforms CSMA for timecritical traffic safety applications. [16] proposes safety-critical vehicle-to-infrastructure communication system based on an extension to the upcoming IEEE 802.11p MAC standard. A local peer group(LPG) [17] architecture is proposed for the roadway safety communication scenario in which vehicles’ neighborhood topology frequently changes. [18] proposes a prototype that can accommodate different models, such as general traffic prediction and re-routing during emergencies in case of fire, accidents etc. The study of [19] provides a guideline for the design of a secure and practical VANET.

[1] [15] [20] [21] analyze the performance of DSRC. [15] shows that IEEE 802.11p might lead to unbounded delays under the scenarios of high channel utilization. An analytical model [20] is proposed to evaluate the performance of IEEE 802.11a-based broadcast services in DSRC system. [21] conducts a study of delay-critical safety applications based on DSRC in vehicular ad hoc networks on latency and throughput. The suitability of DSRC for a class of vehicular safety applications is studied in [22]. [23] provides an overview of the latest draft proposed for IEEE 802.11p. A revised architecture for the IEEE 802.11 MAC and PHY modules is proposed in [24]. [25] discusses the factors that may affect broadcast performance in 802.11-based vehicular ad-hoc networks.

Instead of using CCA threshold, a stepwise CCA Threshold Adaptation(CTA) is proposed in [26] to determine whether the channel is busy or not. [27] studies adaptive threshold based physical carrier sense. [28] proposes a cross-layer MAC design and a clustering solution for supporting the fast propagation of broadcast messages in VANETs. [29] addresses that Dedicated Short-Range Communication(DSRC) cannot meet the requirements of channel congestion control and broadcast performance in VANETs, and proposes a coherent set of communication protocols. [30] proposes a distributed, positionaware broadcast protocol(Smart Broadcast) for VANETs. [31] proposes an improved MAC protocol Adaptive-ADHOC(A-ADHOC) that can obtain 50% reduction of response time and maintain a high contending success probability over the original ADHOC protocol.

# III. INTERFERENCE FREE CHANNEL ALLOCATION

In this section, we provide a brief introduction of our algorithmic design. The MAC design of this system lies in several key aspects: carrier sensing, channel allocation and collision avoidance. For detailed algorithmic designs and corresponding analysis and implementations, we refer to our technical report in [32].

# A. Carrier Sensing

To tackle with the unreliable nature of wireless communication, we design a statistic-based realtime carrier sensing scheme based on radio and channel technologies by multiplexing time, frequency, and space domains. Specifically, we assume that there is temporal correlation among a short sequence of channel states.

In the scheme, we use a parameter θ(t) as a threshold to determine the state of the channel at time t, i.e., to determine whether the channel is busy or not. Specifically, given a node u on which a transceiver at channel k is going to send packets, let RSSI(t) denote the received signal strength indicator sensed by its transceiver at the same channel k. If the sensed RSSI is below θ, the channel is determined to be available at time t. Particularly, we use

$$
\begin{array}{l} \theta (t) = \Sigma_ {i = 1} ^ {m} \left(a _ {1} R S S I (t) + \dots + a _ {m - 1} R S S I (t - m) \right. \\ + \quad a _ {m} \frac {\Sigma_ {i = 1} ^ {n} R S S I (t - i)}{n}) \tag {1} \\ \end{array}
$$

where $\Sigma _ { i = 1 } ^ { m } a _ { i } = 1$

Particularly, the last part provides a rough estimate of the moving average of background noise, while the other part provides an updated estimate to exploit the temporal correlation among a short sequence of channel states. Specifically, we set $m = 3$ and and $n = 2 0 0$ . The value of $a _ { i }$ is trained with a least square estimate with a training data.

# B. Channel Allocation

In this section, we apply the preliminary results of interference free channel allocation design proposed in [33]. The channel used in this section represents a virtual channel, e.g., a frequency, a time slot, etc. Specifically, we utilize 64 frequencies and 20 time slots, which in total provides 1000 virtual channels.

Before deployment, an s-disjunct code X is pre-computed offline, and taken as the channel code for the network, where X is a $M \times N$ binary matrix, M is the number of orthogonal channels, N is the number of nodes in the network region. For any node u in the network, a unique wishlist $X ( u ) \in X$ is associated based on its ID u indicating u’s favored and unfavored channel sets. This assignment is done by an oneto-one mapping function $\mathcal { F }$ between ID and wishlist.

Note that N increases superlinearly compared to M [34], the number of wishlists could be much larger than the number of virtual channels. However, this number is probably not sufficiently large enough to cover all the cars on the road. To solve this issue, we apply our spacial reuse strategy.

We also assume each node u has the wishlists of its twohop neighbors. A natural question is: how to obtain the wishlists from neighboring nodes before channel allocation? In this study, a default channel is utilized for periodically ID broadcast within two hops. Once obtaining the IDs, u could compute the wishlists of its two-hop neighbors.

The design criterion is stated as follows.

1) A node should utilize its favored channels that are unfavored by its two-hop neighbors.   
2) Otherwise, it should choose an unfavored channel that is unfavored by all nodes in its two-hop neighborhood. Since all nodes intend to utilize their favored channels whenever possible, choosing a channel that is unfavored by all interferers is reasonable.   
3) If such channel does not exist, u picks up a favored channel that is favored by the least number of nodes in its two-hop neighborhood.

These channel allocation criterions reflect our design principle: A node always selects a channel that causes the least interference to its neighborhood. It is proved in [33] that a sufficient condition for interference free communication is guaranteed when all nodes succeed in step 1.

Remark 3.1: It is worth pointing out that in our design a node in the network does not require any cooperation/coordination, or any external/environment information except the IDs of its neighbors, which can be quickly obtained in milliseconds from periodically ID broadcasts over a control channel.

# C. Collision Avoidance

Based on the channel allocation algorithm given in [33], each node u could easily know the nodes that may stay on the same channel with u. Let $I ( u )$ denote this node set. Note that $I ( u )$ is an empty set in most time according to [33]. However, collisions may happen among the nodes in I(u)∪u when they transmit at the same time given $I ( u ) \ne \emptyset$ .

In our design, each node in $I ( u ) \cup$ u selects a unique codeword $Y ( u ) \in \mathcal { V }$ according to its ID and location information. Each element in the codeword corresponds to a transmission slot and its $1 / 0$ value representing this slot being a primary slot or a secondary slot of node u. Then u should choose only those slots not being used by any node in $I ( u )$ from its primary slots. If none of these primary slots is available, u should compete the secondary slots that are not primary to any of the nodes in $I ( u )$ with a random backoff mechanism.

Let $D _ { s e n s e }$ denote a sensing duration and $T r a n s _ { w i n d o w }$ denote a series of transmission windows: unless the duration that a channel stays free is longer than $D _ { s e n s e }$ and the transmission window $T r a n s _ { w i n d o w }$ is open for $u ,$ , node u could use the channel.

# IV. EXPERIMENTAL STUDY

Though our design can easily accommodate with many other hardware platforms, protocols and technologies, we apply them to commonly-used cheap hardware, i.e., software/hardware self-defined wireless radios, low cost chips with multichannel support.

# A. Hardware Platform

In the implementation, the communication system is developed based on Si4432. It is compatible with at most 64 user-configurable channels, working with 240-930MHz, and 1-256kbps data rate. In the following, we list some important experimental findings after hardware/software designs and configurations.

Note that the Si4432 chip has two 64-byte TX/RX FIFOs, so it can send or receive a maximum 64-byte packet. When sending a 64-byte packet, it costs about 5.6 milliseconds at the sender, including 1.7 milliseconds for writing the 64-byte packet to the 64-byte FIFO buffer and 3.56 milliseconds for transmitting the packets over the air at the date rate of 200kbps, and the remaining 0.34 millisecond is consumed for other operations and on board transmissions.

After receiving the packets and sensing the RSSI values, the communication unit transmits the data to the control device to process (if necessary the result will be returned to the communication node). The control device, namely ARM11, needs to spend 2.56 milliseconds reading a 64- byte packet from a transceiver in the communication unit, mainly caused during the processing and communicating procedures within the communication unit itself.

# B. Communication Scenario Settings

Our experiment consists of two parts:

• 4-to-4 experiment, in which there are four pairs of nodes communicating at the same time. This experiment mimics the performance of our system in general scenarios;   
5-to-1 experiment, in which there are five nodes as senders and one node as a receiver communicating at the same channel. This experiment mimics the performance of our system in the worst-case scenario.

In all the experiments, the power and the data rate of the radio unit is set to 20dBm and 200kbps, respectively.

In order to verify the performance of our communication system, we have done extensive experimental study and collect a large volume of data under various environment, i.e., highways, city areas, rural areas, tunnels, bridges. These measurements were conducted in Suzhou area, Jiangsu Province, China, from July 2011 to June 2012.

# C. Performance Analysis

In this section, we mainly focus on the performance of the communication system under different environment factors. In order to evaluate the performance, we use packet delivery ratio incorporated with hard realtime requirements as our performance metric. Specifically, a packet transmission failure is denoted as follows:

• The receiver fails to receive the packet, e.g., due to collisions, interferences, etc.   
• The packet fails to be delivered to the receiver within 100ms.

During the experimental study, we have collected a large volume of data (dozens of GBs). It is believed that the results are statistically meaningful.

In the 4-to-4 experiment as shown in Fig. 1(a), when the distance between communication node pairs is about 50m, the PDR under all environments is a little higher than that with a distance of 100m. This is obvious since as the distance increases, the PDR generally decreases in most wireless networks. However, the PDRs under different environments and distances are all beyond 99%. This indicates that there are almost no collisions, co-channel interference, or interchannel interference in the network, which further validates our designs. Under the same distance, the PDRs in different environments are quite close. It is difficult to tell in which environment the communication system could perform better.

Note that the PDR in Fig. 1(a) is computed by the average of four node pairs, the corresponding standard deviation is given in Fig. 1(b). From this figure, it can be found that the PDR fluctuations are small in all environments and settings. We can find that the standard deviation under the distance of 100 meters is bigger than that of 50 meters in all five environments. This also indicates that as the distance increases, the PDR fluctuation increases. Note that the standard deviation in different environments under the same distance are close, it is hard to tell in which environment the communication system could perform more stable.

In the 5-to-1 experiment as shown in the Fig. 2(a), the PDR shows the average packet delivery ratio of the five senders under the case that the senders and the receiver communicate on the same channel. This experiment mimics the worst-case scenario that burst traffic occurs from multiple neighboring nodes on the same channel at the same time. It is easy to find that the PDRs under different environments are all beyond 99%. The standard deviations in Fig. 2(b) show the fluctuation of the PDRs under different environments. This also indicates that as the distance increases, the PDR fluctuation increases. Note that the standard deviation observed in different environments under the same distance are close (except the highway environment at distance 50m), it is hard to tell in which environment the communication system performs more stable. For the case in the highway environment at distance 50m, probably because the sampled data of the 5- to-1 experiment is bigger than that of the other environments, the corresponding standard deviation is smaller due to the law of large numbers.

In general, we can see that the vehicle communication system could stably achieve 99% PDR within 100ms in both the 4-to-4 experiment and the 5-to-1 experiment under different environments.

![](images/de24767a8aa94b312df86e91f1cc77043ce0faf531008b4e239d47df50b0ab1b.jpg)



(a) The PDR of 4-to-4 Experiment in Different Environments with the Separation Distance 50m, 100m

![](images/3e74091d86aa83e819eb5dc3bef4307ae2698598e26a0eff495a24c2dad9dcc9.jpg)



(b) The Standard Deviation of PDR of 4-to-4 Experiment in Different Environments with the Separation Distance 50m, 100m   
Fig. 1. The PDR of 4-to-4 Experiment

# V. CONCLUSION

In this paper, we have proposed a novel reliable realtime communication system to fulfill the hard realtime requirement (100ms) for roadway safety applications given by NHTSA [2]. Furthermore, we have demonstrated that the packet loss rate (namely reliability) is improved by two orders of magnitude compared with existing experimental results [1]. To our best knowledge, it is the first system for roadway safety communications that provides guaranteed highly reliable packet delivery ratio at 99% within the hard realtime requirement 100ms.

![](images/3517a400252ceee1bb61c8ec33873a57af7421c009b3edfa4b84e2df8045db53.jpg)



(a) The PDR of 5-to-1 Experiment in Different Environments with the Separation Distance 50m, 100m

![](images/6e0eb961b7b47d9d11a30f27c08c9a0ba72f9e6e34cf0f13ca22d4eaf9895c62.jpg)



(b) The Standard Deviation of PDR of 5-to-1 Experiment in Different Environments with the Separation Distance 50m, 100m   
Fig. 2. The PDR of 5-to-1 Experiment

Our design can be widely applied for roadway communications and facilitate the current research in both hardware and software design and further provide an opportunity to consolidate the existing work on a practical and easyconfigurable low-cost roadway communication platform. As a future research work, we will further explore the potentials of our system in more roadway safety communication scenarios.

# VI. ACKNOWLEDGMENTS

This research is supported by NSFC under grant 61170267, Jiangsu NSF under grant BK2011358, RFDP under grant 20113402120008, NSFC Distinguished Young Scholars Program under Grant 61125202, National 863 Program under grant 2011AA010100, and National 973 Program under grant 2011CB302905.

# REFERENCES

[1] F. Bai, D. D. Stancil, and H. Krishnan, “Toward understanding characteristics of dedicated short range communications (dsrc) from a perspective of vehicular network engineers,” in Proceedings of the sixteenth annual international conference on Mobile computing and networking, ser. MobiCom ’10, 2010, pp. 329–340.   
[2] NHTSA, http://www-nrd.nhtsa.dot.gov/pdf/nrd-01/esv/esv19/05-0264- w.pdf.   
[3] M. e. a. Peden, “World report on road traffic injury prevention,” 2004.   
[4] ——, “Global status report on road safety,” 2009.   
[5] BTS, http://www.transtats.bts.gov.   
[6] FARS, http://www-fars.nhtsa.dot.gov.   
[7] NHTSA, http://www-nrd.nhtsa.dot.gov/pdf/nrd-12/1665CAMP3web/pages/4HiPriorityB.html.   
[8] W. Cheng, X. Cheng, M. Song, B. Chen, and W. Zhao, “On the design and deployment of rfid assisted navigation systems for vanets,” Parallel and Distributed Systems, IEEE Transactions on, vol. 23, no. 7, pp. 1267– 1274, 2012.   
[9] M. D. Xing, Kai, X. Cheng, and S. Rotenstreich, “Safety warning based on highway sensor networks,” in IEEE WCNC, 2005, pp. 2355–2361.   
[10] K. Xing, X. Cheng, J. Li, and M. Song, “Location-centric storage and query in wireless sensor networks,” in Wireless Networks, vol. 16, no. 4, 2010, pp. 955–967.   
[11] B. Zhang, K. Xing, X. Cheng, L. Huang, and R. Bie, “Traffic clustering and online traffic prediction in vehicle networks: A social influence perspective,” in INFOCOM, 2012 Proceedings IEEE. IEEE, 2012, pp. 495–503.   
[12] F. Liu, K. Xing, X. Cheng, and S. Rotenstreich, “Energy-efficient mac layer protocols in ad hoc networks,” in Resource management in wireless networking, 2005, pp. 300–341.   
[13] T. Jing, X. Chen, Y. Huo, and X. Cheng, “Achievable transmission capacity of cognitive mesh networks with different media access control,” in INFOCOM, 2012 Proceedings IEEE. IEEE, 2012, pp. 1764–1772.

[14] K. Bilstrup, E. Uhlemann, E. Strom, and U. Bilstrup, “On the ability ¨ of the 802.11 p mac method and stdma to support real-time vehicleto-vehicle communication,” EURASIP Journal on Wireless Communications and Networking, vol. 2009, p. 5, 2009.   
[15] K. Bilstrup, E. Uhlemann, E. Strom, and U. Bilstrup, “Evaluation of the ieee 802.11 p mac method for vehicle-to-vehicle communication,” in Vehicular Technology Conference, 2008. VTC 2008-Fall. IEEE 68th. IEEE, 2008, pp. 1–5.   
[16] A. Bohm and M. Jonsson, “Supporting real-time data traffic in safetycritical vehicle-to-infrastructure communication,” in IEEE LCN 2008. IEEE, 2008, pp. 614–621.   
[17] W. Chen and S. Cai, “Ad hoc peer-to-peer network architecture for vehicle safety communications,” Communications Magazine, IEEE, vol. 43, no. 4, pp. 100–107, 2005.   
[18] A. Murali, K. Bhanupriya, S. Smitha, and G. Kumar, “Performance evaluation of ieee 802.11p for vehicular traffic congestion control,” in ITST 2011, 2011, pp. 732–737.   
[19] Y. Qian and N. Moayeri, “Design of secure and application-oriented vanets,” in Vehicular Technology Conference, 2008. VTC Spring 2008. IEEE, 2008, pp. 2794–2799.   
[20] X. Ma, X. Chen, and H. Refai, “Performance and reliability of dsrc vehicular safety communication: a formal analysis,” EURASIP Journal on Wireless Communications and Networking, vol. 2009, p. 3, 2009.   
[21] J. Yin, T. ElBatt, G. Yeung, B. Ryu, S. Habermas, H. Krishnan, and T. Talty, “Performance evaluation of safety applications over dsrc vehicular ad hoc networks,” in ACM VANET Workshop. ACM, 2004, pp. 1–9.   
[22] T. ElBatt, S. Goel, G. Holland, H. Krishnan, and J. Parikh, “Cooperative collision warning using dedicated short range wireless communications,” in Proceedings of the 3rd international workshop on Vehicular ad hoc networks, 2006, pp. 1–9.   
[23] D. Jiang and L. Delgrossi, “Ieee 802.11 p: Towards an international standard for wireless access in vehicular environments,” in Vehicular Technology Conference, 2008. VTC Spring 2008. IEEE. Ieee, 2008, pp. 2036–2040.   
[24] Q. Chen, F. Schmidt-Eisenlohr, D. Jiang, M. Torrent-Moreno, L. Delgrossi, and H. Hartenstein, “Overhaul of ieee 802.11 modeling and simulation in ns-2,” in Proceedings of the 10th ACM Symposium on Modeling, analysis, and simulation of wireless and mobile systems, 2007, pp. 159–168.   
[25] M. Torrent-Moreno, D. Jiang, and H. Hartenstein, “Broadcast reception rates and effects of priority access in 802.11-based vehicular ad-hoc networks,” in Proceedings of the 1st ACM international workshop on Vehicular ad hoc networks, 2004, pp. 10–18.   
[26] R. Schmidt, A. Brakemeier, T. Leinmuller, F. Kargl, and G. Sch ¨ afer, ¨ “Advanced carrier sensing to resolve local channel congestion,” in Proceedings of the Eighth ACM international workshop on Vehicular inter-networking, 2011, pp. 11–20.   
[27] R. Stanica, E. Chaput, and A. Beylot, “Physical carrier sense in vehicular ad-hoc networks,” in IEEE MASS. IEEE, 2011, pp. 580–589.   
[28] L. Bononi and M. Di Felice, “A cross layered mac and clustering scheme for efficient broadcast in vanets,” in Mobile Adhoc and Sensor Systems, 2007. MASS 2007. IEEE Internatonal Conference on, 2007, pp. 1–8.   
[29] D. Jiang, V. Taliwal, A. Meier, W. Holfelder, and R. Herrtwich, “Design of 5.9 ghz dsrc-based vehicular safety communication,” Wireless Communications, IEEE, vol. 13, no. 5, pp. 36–43, 2006.   
[30] E. Fasolo, R. Furiato, and A. Zanella, “Smart broadcast algorithm for inter-vehicular communication,” in Proceedings of the Wireless Personal Multimedia Communications Symposium (WPMC), 2005.   
[31] J. Liu, F. Ren, L. Miao, and C. Lin, “A-adhoc: An adaptive realtime distributed mac protocol for vehicular ad hoc networks,” Mobile Networks and Applications, vol. 16, no. 5, pp. 576–585, 2011.   
[32] K. Xing and T. Gu, “Approaching reliable realtime communications? a novel approach with algorithmic designs and systematic implementation for roadway safety oriented vehicular communications,” in Tech Report, 2012, http://staff.ustc.edu.cn/ kxing/Publications/TechReport/tianbo.pdf.   
[33] K. Xing, X. Cheng, L. Ma, and Q. Liang, “Superimposed code based channel assignment in multi-radio multi-channel wireless mesh networks,” in Proceedings of the 13th annual ACM international conference on Mobile computing and networking, ser. MobiCom ’07, 2007, pp. 15– 26.   
[34] A. G. D’yachkov and V. V. Rykov, “Optimal superimposed codes and designs for renyi’s search model,” Journal of Statistical Planning and Inference, vol. 100, no. 2, pp. 281–302, 2002.