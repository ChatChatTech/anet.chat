# Triggercast: Enabling Wireless Collisions Constructive

Yin Wang†§, Yuan He†§, Dapeng Cheng†, Yunhao Liu†§, Xiang-yang Li‡†

†MOE Key Lab for Information System Security, School of Software, TNLIST, Tsinghua University

§Department of Computer Science and Engineering, HKUST

‡Department of Computer Science, Illinois Institute of Technology

{wangyin00,chengdapeng}@gmail.com, {he, yunhao}@greenorbs.com, xli@cs.iit.edu

Abstract—It is generally considered that concurrent transmissions should be avoided in order to reduce collisions in wireless sensor networks. Constructive interference (CI) envisions concurrent transmissions to positively interfere at the receiver. CI potentially allows orders of magnitude reductions in energy consumptions and improvements on link quality. In this paper, we theoretically introduce a sufficient condition to construct CI with IEEE 802.15.4 radio for the first time. Moreover, we propose Triggercast, a distributed middleware, and show it is feasible to generate CI in TMote Sky sensor nodes. To synchronize transmissions of multiple senders at the chip level, Triggercast effectively compensates propagation and radio processing delays, and has 95th percentile synchronization errors of at most 250ns. Triggercast also intelligently decides which co-senders to participate in simultaneous transmissions, and aligns their transmission time to maximize the overall link PRR, under the condition of maximal system robustness. Extensive experiments in real testbeds reveal that Triggercast significantly improves PRR from 5% to 70% with 7 concurrent senders. We also demonstrate that Triggercast provides on average 1.3× PRR performance gains, when integrated with existing data forwarding protocols.

# I. INTRODUCTION

In wireless sensor networks (WSNs), it is widely accepted that simultaneous transmissions will result in packet collisions. Recently, Backcast [1] and Glossy [2] demonstrate that it is feasible for a common receiver to decode concurrent transmissions of an identical packet with high probability, if multiple transmissions are accurately synchronized. Their works enable simultaneous transmissions to interfere nondestructively, namely to generate non-destructive interference (NDI), in order to enhance network concurrency. By leveraging NDI, Glossy achieves nearly optimal network flooding latency. Since NDI requires different nodes transmitting the same packet and thus may consume more power and require collaboration, one question naturally arises: is NDI constructive? Unfortunately, our extensive experiments disclose that NDI provides no guarantee of power gains and PRR improvements compared with the single best link (Fig. 1(a)).

Our work aims to implement constructive interference (CI) in WSNs. CI is especially attractive for WSNs, because it potentially improves energy efficiency, and thus mitigates the limited power supply issue. A set of N nodes can achieve an $N ^ { 2 }$ -fold increase in the received power of baseband signals, compared to a single node transmitting individually. It indicates that, to achieve the same SNR, each node can reduce signal power with a factor of $\frac { 1 } { N ^ { 2 } }$ , and the total power consumed by N nodes can be $\frac { 1 } { N }$ of the transmitting power required by a single sender. Moreover, simultaneously forwarding a packet can harness signal superposition gain, to improve RSSI and PRR (Fig. 1(b)).

![](images/a4e0c489667b5e3fd004b8170acf89f1315dbc90d2fb8e878ce563624a99d2c1.jpg)



(a) Non-destructive interference

![](images/be6390319f627337522b82b0c9d1b8dad885c70447c086de348977e1fda82572.jpg)



(b) Constructive interference   
Fig. 1. Both NDI and CI enable concurrency. Only CI improves RSSI and PRR. Here, we use (a, b) to describe a link, while a and b represent the RSSI and PRR respectively.

However, implementing CI in WSNs is challenging due to the following reasons. First, simultaneous transmissions must be synchronized at the chip level, namely 0.5µs for IEEE 802.15.4 radio. To generate NDI, Glossy’s synchronization is sufficient, since it compensates most factors, such as clock drifts, software routine uncertainties of OS as well as asynchronous clocks (e.g., transmitter’s radio and receiver’s radio, MCU and radio module). However, it is not sufficient to construct CI. Experiments reveal that propagation delays and radio processing delays significantly influence CI generation. Even worse, estimating radio processing delays is an especially challenging task, as it varies from packet to packet, depends on the SNR, and is affected by multi-path characteristics of the channel. Besides, in the absence of a central controller or a shared clock (e.g., GPS), they can only rely on their own radio signal as a reference.

Second, even if simultaneous transmissions are perfectly synchronized, i.e. no phase offset, they might not guarantee CI. The reason is because a radio signal has noise. Although signals are exactly aligned, noises also superpose. Whether SNR of the combined signal increases depends on SNRs and Tx powers of individual signals.

Third, sensor nodes are always battery-powered, and have limited computational resources. It is difficult or even impossible to deploy complex signal processing algorithms in commercial of the shelf (COTS) sensor platforms.

We propose Triggercast, a practical distributed middleware to generate CI in WSNs. Triggercast enables a co-sender (sender-initiated Triggercast, Fig. 2(a)) or a receiver (receiverinitiated Triggercast, Fig. 2(b)) to trigger a radio signal, which acts as a common reference for all concurrent senders to implement synchronized transmissions. The chip level synchronization (CLS) algorithm of Triggercast enables concurrent transmissions to be synchronized in 0.5µs, by compensating propagation and radio processing delays. Our experiments demonstrate that CLS has $9 5 ^ { t h }$ percentile synchronization errors of at most 250ns. The accuracy is bounded by the running frequency (4,194,304Hz) of on-board MCU of TMote Sky sensor node. Triggercast’s link selection and alignment (LSA) algorithm intelligently decides which co-senders to participate in simultaneous transmissions, and aligns their transmission time to maximize the overall link PRR under the condition of maximal system robustness. The underling CLS and LSA algorithms together ensure Triggercast to generate CI in a practical testbed. Extensive experiments show that Triggercast can improve PRR from 5% to 70% with 7 senders, and from 50% to 98.3% with 6 senders. Experiments also demonstrate that Triggercast on average brings a 1.3× PRR performance gain of data forwarding in realistic deployments.

![](images/fe57f9738d8e7fde6dabe90c876a6e737fd4d7eb93cc2d3eea0a82a10634cf7f.jpg)



(a) sender-initiated

![](images/b1d2db1f4947dde81c08377dae9b99a10cbbc86db5858ab8ebaa027b0e58af42.jpg)



(b) receiver-initiated   
Fig. 2. Triggercast: a radio triggered concurrent transmission architecture.

Experimental results indicate that Triggercast can control topology without increasing Tx power or adding new nodes, which opportunistically reduces latency of data forwarding (in Fig. 3(a)). Triggercast can also reduce packet retransmissions by improving PRR (in Fig. 3(b)). For example, in Fig. 3(b), the ETX of traditional routing is $\mathrm { E T X } _ { 1 } = { } ^ { 1 } / _ { 0 . 2 } + 1 = 6$ , while the ETX of Triggercast might be $^ { 1 } / _ { 0 . 3 2 } + \dot { 1 }$ ≈ 4 (the number 0.32 comes from real measurements).

The contributions of this paper are summarized as follows.

i) We are the first to provide a theoretical sufficient condition for generating CI in WSNs.   
ii) We propose Triggercast, a practical middleware to ensure concurrent transmissions to interfere constructively. The underlining CLS algorithm effectively evaluates and compensates propagation and radio processing delays.   
iii) We implement Triggercast in real testbeds. Extensive experiments show Triggercast can construct CI in TMote Sky platforms. We integrate Triggercast into data forwarding protocols and show its performance gains.

# II. RELATED WORK

Exploiting concurrent transmissions while suppressing interference is a promising direction, for its ability to decode packets from collisions, increase network throughput [3]–[5], alleviate the broadcast storm problem of ackowledgements [1], enhance packet transmission reliability, and reduce flooding latency [2]. Prior works can be categorized as signal processing based and physical-layer phenomenon based.

![](images/7d4b992bce300cc42e6e2e14db171a175abcab2ffd8876b64c409ad2db15a2e6.jpg)



(a) Reduce transfer latency

![](images/7b41e57c1a8cae1421fdcc841d9b2904cc14d305675457266e52db70cab5c73a.jpg)



(b) Reduce data retransmissions   
Fig. 3. (a) Triggercast generates a new link from three disconnected links and thus reduce data forwarding latency. (b) Triggercast makes use of signal superposition to improve PRR and hence reduce retransmission times.

Works based on signal processing include ANC [6] for network coding, SIC [7] and Zigzag [8] for interference cancelation, 802.11n+ [9] for interference alignment in MIMO, AutoMAC [10] for rateless coding, and full-duplex wireless radios [11]. Those works leverage powerful softwaredefined radio platforms (e.g., USRP), and mainly aim at improving throughput in wireless networks. Unfortunately, these signal processing algorithms can not be directly applied in WSNs, in which sensor nodes have insufficient computation resources and limited energy supplies.

Physical-layer phenomenon based works mainly focus on exploring wireless radio properties of COTS transceivers. Such physical-layer phenomena mainly include capture effect [12] and message-in-message (MIM) [13]. Capture effect requires signal of interest is sufficient stronger than the sum of interference. MIM needs special hardware support to continuously synchronize with the preamble of stronger signal. Both capture effect and MIM can only decode the stronger signal at the cost of dropping the other signals.

Recently, Backcast [1] experimentally discovers that, concurrent transmissions of short acknowledgment packets automatically generated by the radio hardware can interfere non-destructively. This characteristic can be utilized to alleviate the ACK implosion problem [14]. Glossy [2] advances this work of NDI by implementing designs such as interrupt compensation and precise timing controls. Although multiple senders transmiting the same packet many times means consuming more power and needs cooperation, NDI is reasonable because it greatly reduces the time incurred by collision scheduling, and thus improves network throughput. The main purpose of our work is to make those wireless collisions interfere constructively.

Triggercast’s radio-triggered synchronization mechanism is comparable with those in SourceSync [15] and Glossy [2]. SourceSync exploits the fundamental property of FFTs to evaluate the radio processing delay, which varies dynamically in multi-path channels. Unfortunately, singlecarrier communication (e.g., IEEE 802.15.4) systems cannot benefit from this method introduced by SourceSync. Glossy is able to synchronize packet transmissions at the magnitude of sub-microseconds, which previously is considered too challenging to implement on COTS sensor platforms. However, for signals to superpose constructively, we need more accurate synchronization algorithms to compensate propagation delays and radio processing delays. Triggercast aims to address this problem.

# III. PACKET TRANSMISSIONS OVER INTERFERENCES

# A. Background

Concurrent Transmissions: packet transmissions over interferences have been studied extensively as they can be utilized to help receivers to decode packets from collisions. In WSNs, due to the limitations of low-cost sensor nodes and COTS radio transceivers (e.g., CC2420, AT86RF230), it is usually difficult or even impossible to leverage techniques such as network coding, successive interference cancelation or MIMO to accomplish packet transmissions while suppressing interference. As a result, previous studies in WSNs mainly focus on exploring physical layer phenomena to realize concurrent packet transmissions.

There are two well-known concurrent transmission techniques, namely capture effect [12] and MIM [13]. It can be seen from Fig. 4 that, when multiple independent transmissions appear simultaneously, the receiver can successfully capture the signal of interest (SOI) if its Tx power is sufficiently larger than the sum of interferences. Capture effect matters on the order of the SOI and interferences. If the SOI arrives first and its power is higher than the interferences, it is called power capture. For delay capture, if the SOI arrives some time later, but before the end of preamble symbols of the interfered packets and the SOI’s Tx power is sufficiently large, the receiver can also successfully decode the SOI. Delay capture happens because of radio transceivers’s ability to do continuous preamble detection during synchronization process. In our measurement, when using CC2420 radio transceivers, the maximal temporal displacements for delay capture to function can be 16Ts (it is considered 8Ts previously), while $T _ { s } = 1 6 \mu s$ represents one symbol time of IEEE 802.15.4 modulation. Differing from capture effect, MIM allows a receiver to disengage from an ongoing packet reception, and engage in a new, stronger packet. An MIM receiver can simultaneously searches for a new (stronger) preamble of the SOI even when locked onto the interferences. For this reason, MIM reckons on special hardware and upper layer protocol support and is mainly applied in WLAN APs.

Recently, Backcast [1] and Glossy [2] exploit identical packet transmissions to interfere non-destructively. This physical layer phenomenon is called non-destructive interference (NDI), as illustrated in Fig. 4. NDI originates from the scenario that multiple spatially distributed transmitters send an identical packet to a common receiver simultaneously. Traditionally, we might think concurrent packet transmissions will collide and prevents the common receiver from successfully decoding the packet, if Tx power of each transmission is the same (In this case, no capture effect happens). However, the receiver can decode the packet with high probability if the maximal temporal displacement of concurrent transmissions is within a chip time, namely, 0.5µs for the IEEE 802.15.4 radio. Indeed, NDI makes good use of the physical layer tolerance for multipath signals.

![](images/1dea71c7ff054b070d2e272e809cd65ec87b61e82933d7b373e50c7a8460a945.jpg)



Fig. 4. Concurrent transmission techniques supported by COTS IEEE 802.15.4 transceivers.

IEEE 802.15.4 Radio: In IEEE 802.15.4, outgoing symbols are mapped to one of 16 pseudo-random, 32-chip sequences by direct-sequence spread spectrum (DSSS) technique. The duration of each chip is $T _ { c } = 0 . 5 \mu \mathrm { s }$ , while each symbol takes up $T _ { s } = 1 6 \mu s$ . The chip sequences are modulated with orthogonal quadrature phase shift keying (O-QPSK) with half-sine pulse shaping. The demodulator de-spreads 32-chip sequences to 16 valid sequences with smallest Hamming distance. Symbol synchronization and data decoding are achieved by a continuous preamble and Start of Frame Delimiter (SFD) search.

# B. Is NDI constructive?

The interference due to concurrent packet transmissions is non-destructive if it doesn’t destroy the normal packet reception. Since NDI requires different nodes transmitting the same packet and thus may consume more power, more channel resources and require collaboration, one question naturally arises: is NDI constructive? In other words, is the aggregated effect of multiple concurrent transmissions better than arbitrary single packet transmission?

To test whether NDI interfere constructively, we use 3 Tmote Sky sensor nodes, each of which has CC2420 transceiver and MSP430F1611 micro-controller. One node is selected as the initiator (I), while the other two are chosen as receivers (R1 and R2). We leverage Glossy source code, an open-source project running on Contiki OS, to generate NDI and add runtime parameter adaption function. We do experiments in both outdoor environment and indoor environment. In each experiment, we fix the positions of I and R1, making them 1 meter away. We move the position of R2, altering its distance with I from 1 meter to 100 meters (outdoor) or from 1 meter to 55 meters (indoor). We keep each individual link a perfect link (e.g., PRRs are larger than 99%), and measure the received PRR and RSSI of I when two receivers transmit packets simultaneously. The experimental results are illustrated in Fig. 5 and Fig. 6.

To verify whether NDI can give rise to power gain, we fix the positions of R1 and R2 1 meter distance away from I. We measure the received RSSI gain of concurrent transmissions compared with the single better link transmitting individually, drawn as Y-axis in Fig. 6. The X-axis denotes the received RSSI difference when two receivers transmit independently. It can be observed from Fig. 6 that, the best case of power gain due to two concurrent transmissions can be as high as 6 dB. However, if the received RSSI difference is larger than 3dB, there is no noticeable power gain. It is perhaps, capture effect dominates the packet reception. The results indicate that adding more senders can not help increase the received RSSI under the condition of capture effect.

![](images/b3c18be1e86b65a0fda39f1920173a077d0e8f0022302aaf4c28d8f517d94f87.jpg)



Fig. 5. No obvious power gain if the received RSSI differences of R1 and R2 exceed 3dB.

![](images/86a51d749725f2aba4737660e7b877f6824eeee762bcceff8b1410c1da907918.jpg)



Fig. 6. The PRR of NDI drops quickly as the differences of propagation delay increase.

![](images/e284b2ebbf1431f9db98a5dbc35ef472b1749f2582023f86aa62675442d9e133.jpg)



Fig. 7. Two signals superpose destructively even if they are perfectly aligned.

We also discover that more senders may not lead to PRR improvement. Even worse, more senders might degrade PRR significantly with NDI. We change the distance between R2 and I, and record the PRR when R1 and R2 transmit simultaneously, as shown in Fig. 6. To mitigate the effect of capture effect, we make sure the RSSI values of successful packet receptions of each individual receiver are almost the same. Indeed, due to multi-path effect and external interferences, the received RSSI values are not always stable. We accurately adjust parameters such as Tx powers, antenna directions and retransmission times, to make sure the RSSI values are steady in a short time interval. It can be seen from Fig. 6, when the distance between R2 and I increases, the PRR performance of node I drops distinctly. The experiments indicate that propagation delays also play a crucial role in PRR, even if the differences of transmission distances are only about 40 meters. In order to ensure concurrent transmissions to interfere constructively, we must compensate propagation delays of spatially distributed transmitters.

# IV. A SUFFICIENT CONDITION FOR GENERATING CI

Could we ensure to construct CI, if we compensate different delay uncertainties and perfectly align concurrent transmissions? To answer this question, we first take a simple case in Fig. 7 as an example, and then provide theoretical analysis to provide a sufficient condition for generating CI in WSNs.

We suppose sender S1 and S2’s signals arriving at the antenna of the destination node have unified signal power 10 and 1, as well as noise power 4 and 4 respectively. Even if the signals of S1 and S2 exactly align at the common receiver, the effective power of the superposed signal is√ $( \sqrt { 1 0 } + 1 ) ^ { 2 } { \approx } 1 7 . 3$ , while the noise power equals 8. The SNR (2.17) of superposed signal degrades slightly compared with the single best signal (2.5). This simple case indicates that only chip level synchronization is not sufficient for CI to function, exactly synchronized signals with different link qualities might also superpose destructively. In the following discussions, we will focus on baseband signals, and examine the role link quality (e.g., PRR, SNR) plays with waveform analysis.

The basic principle of 802.15.4 PHY layer is elaborated in [16]. Let $S _ { m s k } ( t )$ be the transmitted signal after MSK modulation, I(t) and Q(t) denote the in-phase component and quadrature-phase component respectively. Let $\mathfrak { c o } _ { c } = \pi / 2 T _ { c }$ represent the angular frequency of half-sine pulse shaping. The combined MSK signal can be calculated as

$$
S _ {m s k} (t) = I (t) \sin \omega_ {c} t - Q (t) \cos \omega_ {c} t \tag {1}
$$

$$
\text { where } \left\{ \begin{array}{l} I (t) = \sum_ {n} (2 C _ {2 n} - 1) \mathrm{rect} (\frac {t}{2} - n T _ {c}) \\ Q (t) = \sum_ {n} (2 C _ {2 n + 1} - 1) \mathrm{rect} (\frac {t}{2} - n T _ {c} - \frac {T _ {c}}{2}) \end{array} \right. \tag {2}
$$

Here, $C _ { n } \in \{ 0 , 1 \}$ represents the nth chip, and rect() function is a rectangle window, defined as

$$
\operatorname{rect} (t) \triangleq \left\{ \begin{array}{l l} 1 & 0 \leq t \leq T _ {c} \\ 0 & \text { otherwise. } \end{array} \right. \tag {3}
$$

After Rayleigh multi-path channel, the received signal $S _ { R } ( t )$ is convolution of the original signal and the channel $H ( t )$

$$
S _ {R} (t) = S _ {m s k} (t) * H (t) + N (t). \tag {4}
$$

We suppose there are N transmitters $\{ T _ { i } , i = 1 , 2 , . . . , N \}$ simultaneously sending an identical packet to a common receiver R. All the transmissions have already been synchronized at chip level relative to the strongest signal. In our experiment with CC2420 chip, we find the receivers always synchronize with the strongest signal. The output signal from each transmitter Ti arriving at the antenna of the receiver R is denoted as $S _ { R } ^ { i } ( t )$ . Let $\lambda _ { i }$ be SNR of the output signal $S _ { R } ^ { i } ( t )$ , Pi denote average power of signal $S _ { R } ^ { i } ( t )$ and $N _ { i }$ represent power of noise $N _ { i } ( t )$ . Obviously, we have $\begin{array} { r } { \lambda _ { i } = \frac { P _ { i } } { N _ { i } } } \end{array}$ . The SNR $\lambda _ { i }$ is mainly determined by the radio propagation environments (e.g., multipath channels, interferences) and Tx powers of the senders.

The received superposed signal $\overline { { S _ { R } ( t ) } }$ is the sum of the N output signals $S _ { R } ^ { i } ( t )$ . Hence we can approach

$$
\overline {{S _ {R} (t)}} = \sum_ {i = 1} ^ {N} \left(A _ {i} S _ {R} ^ {i} (t - \tau_ {i}) + N _ {i} (t)\right), | \tau_ {i} | \leq T _ {c} \tag {5}
$$

where $A _ { i }$ and $\tau _ { i }$ respectively depict the unified amplitude and phase offset of the ith arriving signal relative to the instant when the strongest signal reaching the receiver. Let $S _ { R } ^ { 1 } ( t )$ be the strongest signal. Correspondingly, we have $A _ { 1 } = 1 , \thinspace \thinspace \tau _ { 1 } =$ $0 , P _ { i } = \check { P } _ { 1 } A _ { i } { } ^ { 2 }$ . According to [17], it can be derived that the effective power $\overline { P }$ of superposed signals after demodulation is

$$
\overline {{P}} = P _ {1} (\sum_ {i = 1} ^ {N} A _ {i} \cos \omega_ {c} \tau_ {i}) ^ {2}, \tag {6}
$$

while the aggregated power of noise $\overline { { S _ { R } ( t ) } }$ is

$$
\overline {{N}} = \sum_ {i = 1} ^ {N} \frac {P _ {i}}{\lambda_ {i}}. \tag {7}
$$

As a result, the SNR of the received superposed signal is

$$
\frac {\overline {{P}}}{\overline {{N}}} = \frac {P _ {1} (\sum_ {i = 1} ^ {N} A _ {i} \cos \omega_ {c} \tau_ {i}) ^ {2}}{\sum_ {i = 1} ^ {N} P _ {i} / \lambda_ {i}} \leq \frac {P _ {1} \sum_ {i = 1} ^ {N} A _ {i} ^ {2} \sum_ {i = 1} ^ {N} (\cos \omega_ {c} \tau_ {i}) ^ {2}}{P _ {1} \sum_ {i = 1} ^ {N} A _ {i} ^ {2} / \lambda_ {i}}. \tag {8}
$$

The inequality (8) can be derived by Cauchy-Schwarz inequality and equality holds if the condition satisfies

$$
\frac {A _ {i}}{\cos \omega_ {c} \tau_ {i}} = \frac {A _ {j}}{\cos \omega_ {c} \tau_ {j}}, \quad (\forall i, j). \tag {9}
$$

To guarantee the received SNR of superposed signal is better than the SNR of any single signal in the worst case, namely to ensure simultaneous transmissions to interfere positively, it is required that the maximum value of the received SNR is no less than $\lambda _ { \mathrm { m a x } }$ x

$$
(\frac {\overline {{P}}}{\overline {{N}}}) _ {m a x} > \lambda_ {\min} \sum_ {i = 1} ^ {N} (\cos \omega_ {c} \tau_ {i}) ^ {2} \geq \lambda_ {\max}. \tag {10}
$$

Consequently, we derive a theoretical sufficient condition (SC) for concurrent transmissions with IEEE 802.15.4 radio to interfere constructively.

i) Concurrent transmissions with an identical packet should be synchronized at chip level, namely less than $T _ { c } { = } 0 . 5 \mu \mathrm { s } ;$   
ii) The phase offset of the ith arriving signal should satisfy:

$$
\left| \tau_ {i} \right| \leq^ {\mathrm{I}} \cos^ {- 1} \frac {P _ {i}}{P _ {1}} / _ {\omega_ {c}} (\text { SC - I });
$$

iii) The ratio of the minimum SNR $\lambda _ { \operatorname* { m i n } }$ and the maximum SNR $\lambda _ { \operatorname* { m a x } }$ of current transmissions should satisfy: $\frac { \lambda _ { \operatorname* { m i n } } } { \lambda _ { \operatorname* { m a x } } } \ge$ λmax $\frac { 1 } { \displaystyle \sum _ { i = 1 } ^ { N } ( \cos \omega _ { c } \tau _ { i } ) ^ { 2 } } \ ~ ( \mathrm { S C - I I I } )$ .

# V. TRIGGERCAST IMPLEMENTATION

# A. Triggercast Overview

In this section, we introduce the implementation of Triggercast to generate CI in WSNs. As illustrated in Fig. 2, Triggercast leverages the instant of a triggered signal as a common reference for all concurrent senders to implement synchronized packet transmissions. In the MAC layer design, the trigger node utilizes a standard CSMA/CA protocol to acquire the medium. Once the trigger node senses the channel is free, it first broadcasts a synchronization packet, and tell all the co-senders the destination and when to start forwarding data. After a promissory duration of time (e.g., tens of ms), all the co-senders begin to transmit simultaneously.

In the PHY layer design, Triggercast utilizes our proposed chip level synchronization (CLS) and link selection and alignment (LSA) algorithms to ensure concurrently transmitted packets interfere constructively. For receiver-initiated Triggercast, the receiver first performs LSA to select which links will participate in concurrent transmissions. For sender-initiated Triggercast, each co-sender individually runs the LSA, to determine whether it will join in the concurrent transmission process. Then selected senders will use CLS to evaluate propagation and radio processing delays. Finally, they insert a number of no operations (NOPs) (Eq. (15)) to compensate the evaluated delays and phase offsets obtained in LSA. It should be noticed that, Triggercast can leverage normal packet transmissions to obtain parameters for CLS and LSA, which can significantly mitigate the overhead.

# B. Chip Level Synchronization (CLS)

1) Timing Diagram Analysis: In practice, it is very challenging to synchronize outgoing IEEE 802.15.4 symbols at a magnitude of chip level, namely 0.5µs. One straightforward approach is through accurate time synchronization. To the best of our knowledge, in WSNs, there is no such time synchronization protocol [18] that can achieve such synchronization accuracy. Taking the Tmote Sky sensor node as an example, we elaborate fine-grained timing diagram analysis of different delays that might influence the synchronization accuracy of Triggercast. The Tmote Sky node has an onboard MCU running at a frequency of $f _ { p } = 4 , 1 9 4$ ,304Hz and a CC2420 radio transceiver which updates its digital output with frequency $f _ { r } = 8 \mathbf { M } \mathrm { H z }$ .

Fig. 8 and Fig. 9 illustrate the detailed SFD pin activities during a packet transmission and reception. From Fig. 9, it can be noticed that the synchronization accuracy of Triggercast accounts for the propagation delay, the radio processing delay introduced by the radio at the beginning of a packet reception, the hardware turn around delay from the reception state to the transmission state and the software delay. Note that the data transmission delay is a fixed value, determined by packet length. The promissory interval is configured by the MAC layer of Triggercast, and may alter from hundreds of µs to tens of ms. The uncertainty of promissory interval can be mitigated by classical time synchronization algorithm, which is beyond the scope of this paper.

(a)Radio processing delay describes the time between the arrival of the packet at the antenna and the instant when the radio circuits successfully decode the first sample. Estimating radio processing delay is a challenging task, as it varies from packet to packet, depends on the SNR, as well as the multi-path characteristics of the channel. Moreover, the asynchronous radio clocks between the transmitter and the receiver also cause a uniform distributed quantization error.

(b)Propagation delay is the signal’s flight time between transmitter and receiver. The propagation delay is determined by the distance of a transmitter-receiver pair.

![](images/be8b2f15091fbb8f256bfc12bc2d7b675bd8129a5c13451131dba6efd041117e.jpg)



Fig. 8. SFD pin activities captured by Agilent oscilloscope MSO-X 2024A. Channel 1 and channel 2 display the SFDs of two concurrent transmitted senders. Channel 4 expounds the SFD signal of a receiver.

![](images/fe8fd2cf84c29e9c1db692da0046bb6877d9eacda3484238cbfde2b731cad091.jpg)



Fig. 9. The timing diagram of SFD signal for TMote Sky node with Triggercast (Without Preamble).

(c)Software delay is defined as the duration from the falling edge of the SFD interrupt to the end of a successful packet reception. The software delay uncertainty mainly depends on variable interrupt serving delays, and the unsynchronized clocks between the MCU and the radio module. The interrupt serving delays can be accurately evaluated and compensated with the method explained by Glossy [2]. The new generation chip CC2530 integrates MCU and radio module in one chip with synchronized clock frequency, indicating the software delay uncertainty can be perfectly eliminated.

(d)Hardware turnaround delay is the time required for a node to switch from packet reception phase to transmission phase. The hardware turnaround delay is constant, and determined by the speed of the radio frontend from reception to transmission.

2) Delay measurement and compensation: From Fig. $^ { 6 , }$ we conclude that propagation delays of spatially distributed transmitters must be compensated, in order to make concurrent transmissions positively superpose. The TMOTE Sky node has an internal DCO operating at frequency $f _ { p } = 4 , 1 9 4 , 3 0 4 \mathrm { H z } ,$ which means the evaluated propagation delays can only have an accuracy of 0.238µs (about 71.5 meters). Even worse, the frequency of the DCO can deviate up $10 \pm 2 0 \%$ from the nominal value, with temperature and voltage drifts of $- 0 . 3 8 \% ^ { \circ } C$ and 5%/V . Moreover, the pair-wise packet transmissions

method can only measure the sum of the propagation delay and the radio processing delay. To subtract the radio processing delay in realistic environment is challenging, as it varies from one packet to another, and is influenced by communication link qualities. Fortunately, we manifest that the compensation of the sum of the propagation delay and the radio processing delay is sufficient for chip level synchronization. This task is still difficult due to many time uncertainty factors such as the quantization uncertainty, the software delay uncertainty due to asynchronous radio clocks, as well as clock drifts due to packet transmissions.

Methodology: According to the law of large numbers, the average of the results obtained from a large number of trails should be close to the expected value. Inspired by this, we select one transmitter-receiver pair which is 40 meters away in indoor environment, and let the transmitter periodically send a packet every 500ms. Once the receiver successfully decodes a packet, it piggybacks a reply packet as soon as possible to the previous transmitter. As shown in Fig. 9, the time-stamps $T _ { S 1 }$ and $T _ { S 2 }$ represent the phases, when the sender’s radio starts transmitting a packet and ends a packet transmission, while the time-stamp $T _ { S 3 }$ denotes the phase when the radio begins a packet reception. The time-stamps $T _ { R 1 }$ , $T _ { R 2 }$ and $T _ { R 3 }$ characterize the phases when the receiver’s radio starts a packet reception, ends a packet reception as well as begins a packet transmission respectively. The TMote Sky node can accurately capture the exact instants when MCU detects rising edge and falling edge of SFD interrupts, with MCU’s timer capture functionality. The nth packet sent by the receiver includes time-stamps $T _ { R 1 } ( n )$ , $T _ { R 2 } ( n )$ and $T _ { R 3 } ( n - 1 )$ , which can be used by the transmitter, to evaluate the expected value of radio processing delay and propagation delay

$$
\widehat {\Delta} = \frac {(\widehat {T _ {S 3}} - \widehat {T _ {S 1}}) - (\widehat {T _ {R 3}} - \widehat {T _ {R 1}})}{2}, \tag {11}
$$

where the symbol $\widehat { \lambda }$ defines the mean value of $\lambda .$

Experimental results of delay measurement using Eq. (11) is displayed in Fig. 10 as the ’raw’ curve. Unfortunately, the result is pessimistic. The measured delay ranges from 0.596µs to $5 . 0 1 \mu \mathrm { s }$ , with average value 2.32µs and variance $0 . 6 2 8 \mu \mathrm { s }$ . The instability of measured delay indicates that, it is difficult to synchronize different transmitters at a magnitude of 0.5µs, if we straightly use the measured data for compensation. Fortunately, we disclose the data transmission delay is the same for all nodes. And thus we have

$$
T _ {S 2} (n) - T _ {S 1} (n) = T _ {R 2} (n) - T _ {R 1} (n). \tag {12}
$$

The data transmission delays of the transmitter and the receiver are drawn in Fig. 11.

We also find that the measured data transmission delays are not stable for the transmitter-receiver pair. The reason for the instability is because of the jitters, clock drifts as well as hardware diversities of the nodes’ DCOs. The drifts can be as high as 5000ppm in our measurement. We define $\chi ( n ) = ( T _ { S 2 } ( n ) - T _ { S 1 } ( n ) ) / ( T _ { R 2 } ( n ) - T _ { R 1 } ( n ) )$ as the unified clock drift coefficient relative to the receiver. Consequently,

![](images/ca17c30e4ec3e1bacb8f46a3f8bffaedc0a90a3f68a6edabb548d3198d316f45.jpg)



![](images/9df1c8ee68451b67eed7f67272cf32d0d31d452efef272cd3bf67208cb0500d4.jpg)



![](images/7b3061adea29deba33330790cc51167bc7db352b312cde85ab7ca285b77aee06.jpg)



Fig. 10. Measured and calibrated delays of Fig. 11. Measured delays of data transmission for Fig. 12. Convergence time analysis of CLS. About propagation and radio processing the transmitter and the receiver using DCO ticks $2 \breve { 2 }$ runs are enough for delay evaluation.

we can calibrate Eq. (11) as

$$
\widehat {\Delta} _ {c a l} = \frac {\text { mean } (\frac {T _ {S 3} (n) - T _ {S 1} (n)}{\chi (n)}) - (\widehat {T _ {R 3}} - \widehat {T _ {R 1}})}{2}. \tag {13}
$$

We obtain the expected radio processing and propagation delay represented by DCO Ticks after the calibration of Eq. (13). To translate them to time, we also utilize the Virtual High-resolution Time (VHT) [19] approach, which calibrates the receiver’s DCO with more stable external 32,768 Hz crystal as a reference. The measured propagation and radio precessing delay after clock drift calibration is shown as the ’drift calibration’ curve in Fig. 10. The calibrated delay ranges from 3.66µs to 4.12µs, with average value 3.90µs and variance 0.012µs.

Convergence Time: To measure CLS’s convergence performance, we do experiments with two transmitter-receiver pairs. Pair 1 and pair 2 are 40 meters and 20 meters away respectively. We average the calibrated delay with Eq. (13), and test how well CLS works in terms of convergence time. Experimental results are shown in Fig. 12. The medium convergence time are 22 runs. Since each run can be done in at least $8 9 2 \mu \mathrm { s } .$ , the delay evaluation algorithm consumes about 20ms and can be accomplished adaptively as the channel state dramatically changes. We disclose that, in our measurements, the delays don’t change so much as thought before. The measurement delay are almost constant, unless the nodes move or the channel significantly changes.

# C. Link Selection and Alignment (LSA)

Note that SNR can be derived from PRR through theoretical models [17] or online measurements [20]. The relationships between SNR and PRR can be mapped as look-up tables and stored in the external flashes of sensor nodes for Triggercast to use. Assuming all the concurrent transmissions are synchronized at the chip level with CLS, according to the proposed sufficient condition in Section IV, the problem to make concurrent transmissions superpose constructively can be formalized as CI-generation problem.

Problem: Let $\Phi = \{ ( P _ { 1 } , \lambda _ { 1 } ) , ( P _ { 2 } , \lambda _ { 2 } ) , . . . , ( P _ { N } , \lambda _ { N } ) , \}$ define a lossy link set, where $P _ { i }$ and $\lambda _ { i }$ denote the received signal’s RSSI and SNR of transmitter $T _ { i }$ respectively. The problem is to find a lossy link subset Ω, in order to maximize the superposed signal’s SNR on condition that the combined link is better than any lossy link in Φ and the phase offset $\tau _ { i }$ is as large as possible.

Algorithm 1: Link Selection and Alignment   
Input: Given a lossy link set $\Phi < P_i, \lambda_i >$ , where $P_i$ and $\lambda_i$ represent the received RSSI and SNR. All link pairs of $\Phi$ are ordered

Output: A lossy link subset $\Omega < P_j, \lambda_j, \tau_j >$ to maximize the superposed signal's SNR, where $\tau_j$ is the maximal allowed phase offset.

1 Sort $\Phi$ with arbitrary optimal sorting algorithm, and store the result as $\Phi'$ 2 Get the best link $< P, \lambda >$ in $\Phi'$ Insert link $< P, \lambda >$ and "0" (phase offset) in empty set $\Omega$ 3 for $i = 2:N$ do

4 get the best link $< P_i, \lambda_i >$ in sorted set $\Phi'$ , store as link $< P_t, \lambda_t >$ ;

5 calculate maximal allowed phase offset $\tau_i$ of link $< P_t, \lambda_t >$ using link $< P, \lambda >$ , to satisfy (SC-I) of the sufficient condition provided in Section IV;

6 use set $\Omega$ , link $< P_t, \lambda_t >$ , phase offset $\tau_i$ to verify SC-II of the sufficient condition;

7 if SNR of link $< P_t, \lambda_t >$ satisfies SC-II then

8 insert link $< P, \lambda >$ , phase offset $\tau_i$ to set $\Omega$ ;

9 else

10 break;

11 end

12 end

13 end

We define a link pair $( L _ { i } , L _ { j } )$ is ordered if $P _ { i } \geq P _ { j }$ indicates $\lambda _ { i } \geq \lambda _ { j } , 1 \leq i , j \leq N$ . According to the sufficient condition for CI, it can be proved that this problem is NP-hard if there exists disordered link pair in Φ. In practice, it is reasonable to assume all the link pairs in Φ are ordered. Based on this assumption, we will show this problem can be solved in $O ( n l o g n )$ time.

The pseudocode of LSA is described in algorithm 1. The for-loop can safely break if $\lambda _ { i }$ doesn’t satisfy SC-II of the sufficient condition. For all $\lambda _ { j } \leq \lambda _ { i }$ , we have $\tau _ { j } \geq \tau _ { i }$ and thus we can prove that they all don’t satisfy SC-II.

![](images/5e59d86988b9bb27250d2452c55f3fedef88e9b55d3098e275368efab8ee167d.jpg)



Fig. 13. We probe pin activities from CC2420 with very thin enameled wire.

![](images/88ce1dbae780ede9bb7b8028c2999205f8c2ba187a010ed5328449cf3cbc0d00.jpg)



Fig. 14. A snapshot of part of our testbed.

![](images/18f73e07f7b4e4d6a9ef8dea9fcdd218d76d4cc5f06d3041ad92fe98f4285bbc.jpg)



Fig. 15. Synchronization error of Triggercast less than 250 ns has more than 95% confidence

$$
\begin{array}{l} \frac {\lambda_ {j}}{\lambda_ {\max}} \leq \frac {\lambda_ {i}}{\lambda_ {\max}} = \frac {1}{\sum_ {k = 1} ^ {i - 1} (\cos \omega_ {c} \tau_ {k}) ^ {2} + (\cos \omega_ {c} \tau_ {i}) ^ {2}} \\ \leq \frac {1}{\sum_ {k = 1} ^ {i - 1} \left(\cos \omega_ {c} \tau_ {k}\right) ^ {2} + \left(\cos \omega_ {c} \tau_ {j}\right) ^ {2}} \tag {14} \\ \end{array}
$$

Time Complexity: the time complexity of LSA algorithm is dominated by the sort function. Clearly, the optimal sort algorithm has an $O ( n l o g \ n )$ time complexity. Thus the time complexity of LSA algorithm is also O(nlog n).

Total compensation time: we let τi as large as possible to obtain the system’s maximal robustness for synchronization errors. Consequently, the total number $N _ { c o m }$ of NOPs for cosender Ti in Triggercast is

$$
N _ {c o m} = \left[ (T - \widehat {\Delta} _ {c a l} + \tau_ {i}) f _ {p} \right] \tag {15}
$$

where [] is the round function, and T is a predefined maximum delay calibration time.

# VI. PERFORMANCE

We have implemented a prototype Triggercast on TMote sky sensor nodes. The software is based on Contiki OS. During the overall Triggercast’s duration, except for the promissory interval, all the relevant interrupts and hardware timers that are not essential to Triggercast’s functioning are disabled. Since this interval is very short (several milliseconds), it is feasible that Triggercast doesn’t influence the upper layer’s functionality. A runtime parameter adjustment software is developed, to make sure we can online change the system running parameters, without altering communication channels by programming the nodes. We test the performance of Triggercast in a practical testbed (Fig. 14).

# A. Synchronization Accuracy

We first test the synchronization performance of multiple concurrent transmitters. We use three TMote sky nodes, one as a receiver and two as transmitters. We set the promissory interval parameter to 0 in receiver-initiated Triggercast. We connect the SFD pins of the receiver (R) and one of the transmitters (S1) to a Agilent MSO-X serial oscilloscope (Fig. 13). The other transmitter (S2) is 30 meters away in an indoor environment. However, it is difficult to measure the synchronization of S1 and S2 directly with the oscilloscope. As a result, we use R as a reference node. The synchronization between S1 and R can be monitored by the oscilloscope with a granularity of 5ns. The durations between $T _ { R 1 }$ and $T _ { R 3 }$ (Fig. 9) of the receiver are accurately measured when S1 and S2 transmit independently. The differences of the durations can be used for synchronization accuracy measurement, since both S1 and S2 rely on the instant $T _ { R 1 }$ as a reference. The CDF of synchronization errors compared with the Glossy synchronization algorithm is illustrated in Fig. 15. Triggercast’s CLS algorithm can synchronize multiple transmitters at a magnitude of 250ns. The accuracy is limited by the operating frequency of the MCU of TMote Sky sensor nodes. The Glossy synchronization algorithm degrades as the distance differences between two transmitter-receiver pairs increase. CLS outperforms Glossy because CLS compensates the time due to propagation and radio processing delays.

# B. Power Gains and PRR Improvements

The main purpose of this paper is to make wireless collisions interfere constructively. In other words, multiple senders transmit an identical packet simultaneously can improve RSSI and PRR. We do experiments by carrying out Triggercast in both indoor and outdoor environments with our testbed (Fig. 14). Up to 8 senders with all three different kinds of links (low $( \mathrm { P R R } < 5 \% )$ , medium $( 5 \% < \mathrm { P R R } < 9 0 \% )$ ), high(PRR > 90%)), are executed to transmit packets at the same time. Due to the limit of physical space, we randomly insert NOPs to simulate different propagation and radio processing delays. We adjust the received RSSIs of each sender’s individual packet transmission to almost the same, to eliminate the influence of capture effect. All the results are averages of more than 1000 tests. Fig. 16 lists the power gains due to multiple senders of different link types (disconnected link: 1-5 dB, intermediate link: 2-6 dB, connected link: 2-6 dB). The maximum power gain can approach $N ^ { 2 }$ for N concurrent transmitters. Fig. 17 shows that PRR can be significantly improved by leveraging CI. For 7 disconnected links, the PRR achieves almost 70%, which is better than our previous understandings of harnessing sender diversity gain $( 1 - ( 1 - 0 . 0 5 ) ^ { 3 } \approx 3 0 . 2 \% )$ . Triggercast improves the PRR of intermediate links from 50% to almost 100% with 6 concurrent senders. Our experiments indicate that Triggercast can control network topology (e.g., increasing new communication links) without changing the original network state (adding new nodes, increasing nodes’ power, etc.). This characteristic is attractive to improve routing performance (explained in Fig. 3). To the best of our knowledge, we are the first to report multiple concurrent transmitters can reach such PRR improvements in realistic WSNs.

![](images/70f86878b6ba87ecc10b8efeb83b4000081d7d643c3372529d0ab091773e94f2.jpg)



Fig. 16. Triggercast increases RSSI.

![](images/6639f9ad38364759c3033000a509f1e264d081896c2cb3a04439c3eb085316d5.jpg)



Fig. 17. Triggercast improves PRR.

![](images/2e719879702e792d2f40f6f552eec9e83d1d788ca4d4d5fafd863daa3912537f.jpg)



Fig. 18. Triggercast provides PRR gains over traditional single-path routing.

# C. Data forwarding with Triggercast

We create a five node topology as in Fig. 3(b). We select two nodes as the source node and the receiver node respectively. The other three nodes perform forwarding. All five nodes are placed in random positions in our office. One of the three relay nodes is deployed near the window, exposure to sunshine. We also use a hair dryer to heat the node to increase the DCO jitters and decrease its link quality. We first measure pairwise loss rates between the nodes to compute the ETX metric for each link. We also evaluate the propagation and radio processing delays with CLS algorithm. We fix Tx power of source node as 0dBm, online adjust Tx power of relay nodes from -25dBm to 0dBm, and record the PRR of the receiver. Experimental results are elaborated in Fig. 18.

As expected, exploring CLS and LSA together results 1.3× PRR gains on average over traditional single-path routing. The gain of using CLS alone is not obvious. The reason is because the dirty link (the heated node/receiver pair) influences the overall performance. Glossy works even worse than singlepath routing. The reason is beacuse Glossy only generates NDI, and doesn’t compensate propagation and radio processing delays, as well as make link selections.

# VII. CONCLUSIONS AND FUTURE WORK

We introduce Triggercast, the first work to implement CI instead of NDI in WSNs, to the best of our knowledge. Triggercast compensates propagation and radio processing delays, and makes link selection as well as transmission alignment, in order to construct CI. We implement Triggercast in real testbed, and experimentally demonstrate that Triggercast produces significant performance gains in data forwarding protocols. We also provide a theoretical sufficient condition on how to ensure concurrent transmissions interfere constructively. Future work includes adding node mobility and low duty-cycle factors in Triggercast, and exploiting Triggercast in time synchronization and localization. We are also developing Triggercast as an independent service and open source software component to the community.

# REFERENCES

[1] P. Dutta, S. Dawson-Haggerty, Y. Chen, C. Liang, and A. Terzis, “Design and evaluation of a versatile and efficient receiver-initiated link layer for low-power wireless,” in Proceedings of ACM SenSys, Nov. 2010.   
[2] F. Ferrari, M. Zimmerling, L. Thiele, and O. Saukh, “Efficient network flooding and time synchronization with Glossy,” in Proceedings of ACM/IEEE IPSN, Apr. 2011.   
[3] X. Wang, L. Fu, and C. Hu, “Multicast performance with hierarchical cooperation,” IEEE/ACM Transactions on Networking, vol. 20, no. 3, pp. 917–930, 2010.   
[4] T. Jing, X. Chen, Y. Huo, and X. Cheng, “Achievable transmission capacity of cognitive mesh networks with different media access control,” in Proceedings of IEEE INFOCOM, Mar. 2012.   
[5] S. Chu and X. Wang, “Opportunistic and cooperative spatial multiplexing in mimo ad hoc networks,” IEEE/ACM Transactions on Networking, vol. 18, no. 5, pp. 1610–1623, 2010.   
[6] S. Katti, S. Gollakota, and D. Katabi, “Embracing wireless interference: Analog network coding,” in Proceedings of ACM SIGCOMM, Aug. 2007.   
[7] D. Halperin, T. Anderson, and D. Wetherall, “Taking the sting out of carrier sense: interference cancellation for wireless lans,” in Proceedings of ACM MOBICOM, Sep. 2008.   
[8] S. Gollakota and D. Katabi, “Zigzag decoding: combating hidden terminals in wireless networks,” in Proceedings of ACM SIGCOMM, Aug. 2008.   
[9] K. Lin, S. Gollakota, and D. Katabi, “Random access heterogeneous mimo networks,” in Proceedings of ACM SIGCOMM, Aug. 2011.   
[10] A. Gudipati, S. Perreira, and S. Katti, “AutoMAC: Rateless wireless concurrent medium access,” in Proceedings of ACM MOBICOM, Aug. 2012.   
[11] M. Jain, J. Choi, T. Kim, D. Bharadia, S. Seth, K. Srinivasan, P. Levis, S. Katti, and P. Sinha, “Practical, real-time, full duplex wireless,” in Proceedings of ACM MOBICOM, Sep. 2011.   
[12] K. Leentvaar and J. Flint, “The capture effect in fm receivers,” IEEE Transactions on Communications, vol. 24, no. 5, pp. 531–539, 1976.   
[13] N. Santhapuri, J. Manweiler, S. Sen, R. Choudhury, S. Nelakuditi, and K. Munagala, “Message in message (MIM): A case for reordering transmissions in wireless networks,” in Proceedings of ACM HotNets-VII, Oct. 2008.   
[14] S. Ni, Y. Tseng, Y. Chen, and J. Sheu, “The broadcast storm problem in a mobile ad hoc network,” in Proceedings of ACM MOBICOM, Aug. 1999.   
[15] H. Rahul, H. Hassanieh, and D. Katabi, “SourceSync: A distributed wireless architecture for exploiting sender diversity,” in Proceedings of ACM SIGCOMM, Aug. 2010.   
[16] N. Oh and S. Lee, “Building a 2.4-ghz radio transceiver using ieee 802.15.4,” IEEE Circuits and Devices Magazine, vol. 21, no. 6, pp. 43– 51, 2006.   
[17] Y. Wang, Y. He, X. Mao, Y. Liu, Z. Huang, and X. Li, “Exploiting constructive interference for scalable flooding in wireless networks,” in Proceedings of IEEE INFOCOM, Mar. 2012.

[18] M. Mar \`oti, B. Kusy, G. Simon, and A\`. L \`edeczi, “The flooding time synchronization protocol,” in Proceedings of ACM SenSys, November 2004.   
[19] T. Schmid, P. Dutta, and M. B. Srivastava, “High-resolution, lowpower time synchronization an oxymoron no more,” in Proceedings of ACM/IEEE IPSN, Apr. 2010.   
[20] S. Liu, G. Xing, H. Zhang, J. Wang, J. Huang, M. Sha, and L. Huang, “Passive interference measurement in wireless sensor networks,” in Proceedings of IEEE ICNP, Oct. 2010.