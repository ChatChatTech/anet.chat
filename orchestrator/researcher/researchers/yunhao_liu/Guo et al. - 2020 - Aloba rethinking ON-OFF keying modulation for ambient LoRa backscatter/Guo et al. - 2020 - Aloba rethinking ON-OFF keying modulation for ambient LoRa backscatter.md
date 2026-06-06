# Aloba: Rethinking ON-OFF Keying Modulation for Ambient LoRa Backscatter

Xiuzhen Guo $^{1}$ , Longfei Shangguan $^{2}$ , Yuan He $^{1}$ , Jia Zhang $^{1}$ , Haotian Jiang $^{1}$ , Awais Ahmad Siddiqi $^{1}$ , Yunhao Liu $^{1,3}$

$^{1}$ School of Software and BNRist, Tsinghua University

$^{2}$ Microsoft

$^{3}$ Department of Computer Science and Engineering, Michigan State University

{guoxz16,j-zhang19,jht19,xidq19}@mails.tsinghua.edu.cn,

longfei.shangguan@microsoft.com,heyuan@mail.tsinghua.edu.cn,yunhaoliu@gmail.com

# ABSTRACT

Backscatter communication holds potential for ubiquitous and low-cost connectivity among low-power IoT devices. To avoid interference between the carrier signal and the backscatter signal, recent works propose a frequency-shifting technique to separate these two signals in the frequency domain. Such proposals, however, have to occupy the precious wireless spectrum that is already overcrowded, and increase the power, cost, and complexity of the backscatter tag. In this paper, we revisit the classic ON-OFF Keying (OOK) modulation and propose Aloba, a backscatter system that takes the ambient LoRa transmissions as the excitation and piggybacks the in-band OOK modulated signals over the LoRa transmissions. Our design enables the backsactter signal to work in the same frequency band of the carrier signal, meanwhile achieving good tradeoff between transmission range and link throughput. The key contributions of Aloba include: i) the design of a low-power backscatter tag that can pick up the ambient LoRa signals from other signals; ii) a novel decoding algorithm to demodulate both the carrier signal and the backscatter signal from their superposition. The design of Aloba completely unleashes the backscatter tag's ability in OOK modulation and achieves flexible data rate at different transmission range. We implement Aloba and conduct head-to-head comparison with the state-of-the-art LoRa backscatter system PLoRa in various settings. The experiment results show Aloba can achieve 39.5–199.4 Kbps data rate at various distances, 10.4–52.4× higher than PLoRa.

# CCS CONCEPTS

\- Networks $\rightarrow$ Network protocol design; Sensor networks; Cross-layer protocols; • Computer systems organization $\rightarrow$ Embedded systems.

# KEYWORDS

ON-OFF Keying Modulation, Ambient LoRa Backscatter

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

SenSys '20, November 16–19, 2020, Virtual Event, Japan

© 2020 Association for Computing Machinery.

ACM ISBN 978-1-4503-7590-0/20/11...\$15.00

https://doi.org/10.1145/3384419.3430719

![](images/bfb85e503a0eeb318e4382deefeb3becf8f0135e0d94f876d94056bd35d5e79b.jpg)



Figure 1: An illustration of Aloba deployment in the factory. Aloba tag takes the ambient LoRa signals as the excitation and transmits the machine status data (e.g., vibration) back to the gateway hundreds of meters away.

# ACM Reference Format:

Xiuzhen Guo $^{1}$ , Longfei Shangguan $^{2}$ , Yuan He $^{1}$ , Jia Zhang $^{1}$ , Haotian Jiang $^{1}$ , Awais Ahmad Siddiqi $^{1}$ , Yunhao Liu $^{1,3}$ . 2020. Aloba: Rethinking ON-OFF Keying Modulation for Ambient LoRa Backscatter. In The 18th ACM Conference on Embedded Networked Sensor Systems (SenSys '20), November 16–19, 2020, Virtual Event, Japan. ACM, New York, NY, USA, 13 pages. https://doi.org/10.1145/3384419.3430719

# 1 INTRODUCTION

The fourth industry revolution (a.k.a. industrial 4.0) aims to transform traditional manufactory and industrial practices with advanced automation, artificial intelligence, and the internet of things technology. The key to the success of industrial 4.0 is the underlying machine to machine (M2M) communication technology that provides ubiquitous and reliable wireless connectivity anywhere, at any time [4, 5, 9, 18, 19, 45]. However, industrial applications have diverse requirements on data exchanging and thus demand different M2M communication technologies. For example, video surveillance on industrial practices requires high-throughput (tens of Gbps) M2M links to ensure reduced communication latency [47]. Keeping track of the status of machines in the factory (e.g., vibration, noise, rotation), on the other hand, demands moderate-throughput (hundreds of Kbps) M2M links for sensing data forwarding [32]. As some of these machines may produce strong noise, flash intense light, and discharge harmful gases (as shown in Figure 1), these data forwarding links should be also low-power and long-range, allowing sensors to transmit their data back to the gateway hundreds of meters away without extra human intervention or frequent battery replacement.

![](images/921a165f75867f25f57386f624bef53c2e592b8c0060c76257595a992e6438f6.jpg)



Figure 2: Comparison of existing backscatter technologies.

While the latest 5G new radio [2] and 802.11ax (a.k.a. Wi-Fi 6) [38] technologies have been successfully deployed in factories for low-latency data transmission, these technologies are not suitable for machine monitoring in the complex industrial environment as they are either susceptible to blockage or constrained by short communication range (tens of meters). On the other hand, Low-power wide-area networks (LPWANs) are able to connect machines across long range. However, these technologies consume substantial amount of energy in around-the-clock monitoring mode and thus require frequent battery replacement.

Due to its low-power and simplicity, backscatter communication becomes a promising technology to enrich the family of existing M2M links. The state-of-the-art backscatter systems (Figure 2) now can transmit at high throughput [1, 14–16, 34, 42, 43, 48–51] and communicate over long distance [35, 39, 41]. These desirable properties make backsactter communication a good candidate for industrial applications. However, as we carefully examine these innovations, we find these designs (Figure 2) either sacrifice the communication range in order to achieve a higher link throughput, or tradeoff the throughput for a decent communication range. None of them is able to balance the throughput and communication range to satisfy the requirement of the machine status monitoring in industrial practices. For example, the throughput of OFDMA-backscatter [51] can reach up to 5.2 Mbps, it however only supports short-range communication (up to 10 m). In contrast, PLoRa [35] supports kilometer-scale backscatter communication at the cost of a very low throughput (limited to tens of Kbps). Similarly, LoRa backscatter [39] allows the backscatter tag to communicate with the gateway kilometers away. However, its maximum link throughput is constrained to 27.3 Kbps due to the LoRa PHY-layer regulation. Besides, LoRa backscatter relies on the dedicated excitation source to send a continuous sinusoidal tone as the carrier signal. This operation inevitably adds cost and complicates the installation and maintenance of the system.

In this paper, we present the design, implementation, and evaluation of Aloba, an ambient backscatter design for machine status monitoring in industrial practices. Aloba takes the ambient LoRa signals (e.g., emitted from nearby active LoRa nodes) as the carrier signal, modulating its sensing data on these carrier signals using ON-OFF Keying (OOK) modulation, and then reflects the modulated signal to the receiver (LoRa gateway). Such design owns three desirable properties: i): Flexible link throughput. OOK modulation enables the Aloba tag to adapt its link throughput to the link quality as opposed to the PHY-layer regulation of carrier signals. ii): Long communication range. By taking ambient LoRa signals as the carrier, the Aloba tag could leverage the unique processing gain brought by the chirp signal design to enable backscatter communication at a range of hundreds of meters. iii): Easy to deploy. The Aloba tag modulates its data on the ambient LoRa signals. This can avoid the installation and maintenance of the dedicated excitation sources.

![](images/1aa9d4957d14a38c8b442996de433af0da8171a73bf9a13bc73dd2b343b953f6.jpg)



Figure 3: LoRa backscatter system. Aloba tag modulates the ambient LoRa signal using On-Off Keying. (a): carrier signal transmitted by LoRa Tx. (b): backscatter signal modulated by Aloba tag. (c): received signal is the superposition of carrier signal and backscatter signal. (d): the LoRa receiver decodes both LoRa carrier signal and backscatter signal using our demodulation algorithm.

Harvesting these benefits, however, faces fundamental challenges. On one hand, unlike the conventional RFID system where the excitation is a continuous wave (a sinusoidal tone), the excitation signal in our design is an ambient, intermittent LoRa signal which already conveys information and changes over time. The backscatter tag should be able to distinguish the LoRa signal from the others and further synchronize with each LoRa symbol for fine-grained modulation. On the other hand, the backscatter signal is orders of magnitude weaker than the excitation signal. The receiver should be able to demodulate this weak backscatter signal in the presence of strong interfering excitation signal. Due to the frequency variation, the superposition of an excitation signal and a backscatter signal changes over time, which makes the demodulation even more challenging ( $\S2$ ).

In Aloba we present a novel hardware-software solution to tackle the above challenges. On a high-level the Aloba tag picks up the ambient LoRa signal from the other signals using a low-power LoRa packet detection circuit. It then modulates data on the LoRa payload chirps using OOK. The LoRa receiver leverages our signal processing algorithm to decode both the excitation and the backscatter signals from their superposition. Aloba makes three key contributions:

\- We design a simple yet effective LoRa packet detection circuit that can detect the ambient LoRa signal as low as -60 dBm with 0.3 mW power consumption. This packet detection circuit serves as a plug-in peripheral that can be easily integrated with commercial backscatter tags, e.g., WISP.

![](images/fd8353d2ba772f017b2d911837b824d505cc0cc2b72cfc60f820d6f08bc7d5e1.jpg)  
Figure 4: LoRa modulation and demodulation. (a): the base-chirp encodes symbol “00”. (b): a cyclic shifted version of the base-chirp encodes symbol “10”. (c): the multiplication of different chirps and down-chirp yields peaks on different FFT bins.

- We comprehensively study the superposition of chirp signals at the LoRa receiver, based on which we propose a novel demodulation algorithm that can detect the fine-grained changes on the phase and amplitude of the received signal to demodulate both the carrier signal and the backscatter signal.   
- We implement Aloba on a PCB (printed circuit board) and integrate it with WISP [37] for evaluation. The experimental results demonstrate that Aloba can achieve various data rates (39.5–199.4 Kbps) at various distances (50–200 m) in the wild. Compared with the state-of-the-art system PLoRa [35], Aloba achieves 10.4–52.4× higher throughput. We shared our schematic and source code in http://tns.thss.tsinghua.edu.cn/sun/researches/BackscatterCommunication.html for reproducibility.

The rest of this paper is organized as follows. Section 2 presents the background knowledge of LoRa and analyzes the self-interference at the LoRa receiver. We introduce the decoding algorithm in Section 3 and present the Aloba operations on tag in Section 4. Section 5 briefly describes the MAC layer of Aloba system. Section 6 introduces the implementation of Aloba system. We show the evaluation results in Section 7 and discuss related works in Section 8. Section 9 discusses future works. We conclude this work in Section 10.

# 2 SELF-INTERFERENCE ON LORA BACKSCATTER

Aloba modulates ambient LoRa signal (the carrier signal) using OOK. In this section, we first introduce the standard LoRa modulation and demodulation process, and then analyze LoRa self-interference.

# 2.1 LoRa Primer

LoRa adopts Chirp Spread Spectrum (CSS) to modulate data. Each LoRa symbol is represented by a chirp where the frequency changes linearly over time, as shown in Figure 4(a)-(b). To demodulate the LoRa symbol, the receiver multiplies an incoming LoRa symbol with a down-chirp and transforms the multiplication from the time domain to the frequency domain, yielding a peak on an FFT bin. The receiver tracks the location of this peak to demodulate the LoRa symbol accordingly. Figure 4(c) illustrates this process.

![](images/dc2353de6fe329e48f168c1d068ed23da2a1b5a36f2a003ff818ad2f8d49106b.jpg)  
Figure 5: The received signal is the superposition of the carrier signal and backscatter signal (propagation delay of the backscatter signal is $1.8 \mu s$ ). The received signal experiences periodic amplitude variation due to constructive and destructive interference.

# 2.2 Modeling the Interference

The frequency of a LoRa chirp can be represented by: $f(t) = F_{0} + kt$ , where $F_{0}$ is the initial frequency of this LoRa chirp; k is the frequency changing rate (over time). The phase of this LoRa chirp at a given time t can be calculated by:

$$
\varphi (t) = 2 \pi \int_ {0} ^ {t} f (t) d t = 2 \pi (F _ {0} t + \frac {1}{2} k t ^ {2}), t \leq T _ {c h i r p} \tag {1}
$$

Phase offset. The backscatter signal and the carrier signal propagate along different paths. The propagation delay due to this path difference d can be represented by $t_{d} = \frac{d}{c}$ , where c is the radio propagation speed. At time t, the phase of the carrier signal and the backscatter signal are $\varphi_{c}(t) = 2\pi(F_{0}t + \frac{1}{2}kt^{2})$ and $\varphi_{b}(t) = 2\pi(F_{0}(t - t_{d}) + \frac{1}{2}k(t - t_{d})^{2})$ , respectively. Hence the phase difference $\Delta\varphi(t)$ between these two signals can be calculated by:

$$
\Delta \varphi (t) = \varphi_ {c} (t) - \varphi_ {b} (t) = 2 \pi ((F _ {0} + k t) t _ {d} - \frac {1}{2} k t _ {d} ^ {2}) \tag {2}
$$

From the above equation we have the following observations: i): The phase difference $\Delta\varphi(t)$ varies over time, as shown in Figure 6(a). Hence the received signal experiences interference that periodically alternates between constructive and destructive states, as shown in Figure 5. ii): The propagation delay changes across tag's locations, so does the amplitude variation of the received signal. Therefore, we cannot rely on the amplitude variation of the received signal to detect the appearance of the backscatter signal. On the other hand, conventional interference cancellation algorithms, e.g., passive RFID and Wi-Fi backscatter [1, 8, 17, 46] are not suitable for solving this LoRa self-interference, since the carrier signal here is unknown to the LoRa receiver. Reconstructing the carrier signal in hopes of canceling it out from the received signal is difficult, since the amplitude and frequency of LoRa signals change over time.

Frequency offset. The propagation delay $t_{d}$ leads to a frequency offset in the frequency domain, as shown in Figure 6(b). The frequency offset $\Delta f$ can be calculated by:

$$
\Delta f = \frac {B W}{T _ {c h i r p}} t _ {d} = \frac {B W}{T _ {c h i r p}} \frac {d}{c} = \frac {B W ^ {2}}{2 ^ {S F}} \frac {d}{c} \tag {3}
$$

![](images/8a4c5bd766bcbb2c0034546704cf241de4916af1d87f2b3407d50d990ca2ecd3.jpg)

Figure 6: Frequency-time domain characteristics of chirp signal combination. (a): the phase offset between the carrier and backscatter signal changes over time. (b): the propagation daley $t_{d}$ between these two signals leads to an offset $\Delta f$ on the frequency domain. (c): both carrier signal and backscatter signal drop to the same FFT bin after demodulation due to the small frequency shift. 

<table><tr><td>Path Difference</td><td>BW (KHz)</td><td>SF</td><td>Frequency Offset</td><td>FFT Bin</td></tr><tr><td>10 m</td><td>500</td><td>7</td><td>65.104 Hz</td><td>3906.25 Hz</td></tr><tr><td>50 m</td><td>500</td><td>7</td><td>325.52 Hz</td><td>3906.25 Hz</td></tr><tr><td>100 m</td><td>500</td><td>7</td><td>651.04 Hz</td><td>3906.25 Hz</td></tr><tr><td>200 m</td><td>500</td><td>7</td><td>1302.08 Hz</td><td>3906.25 Hz</td></tr><tr><td>400 m</td><td>500</td><td>7</td><td>2604.16 Hz</td><td>3906.25 Hz</td></tr><tr><td>600 m</td><td>500</td><td>7</td><td>3906.25 Hz</td><td>3906.25 Hz</td></tr></table>

Table 1: Frequency offset between the carrier signal and the backscatter signal under different parameters

The frequency offset is determined by the LoRa bandwidth BW, the spreading factor SF, and the path difference d. Table 1 lists the maximum frequency offset under different path difference settings. We observe that the receiver is unable to differentiate the backscatter signal and carrier signal in frequency domain, unless the path difference is larger than 600 m. As the tag's location is usually unknown in many outdoor deployments, we cannot blindly borrow the idea of LoRa parallel decoding $[3, 6, 44]$ to separate the two signals from their superposition in the frequency domain.

# 3 DEMODULATION

This section describes the way to decode both the carrier signal and the backscatter signal from their superposition. Due to signal attenuation, insertion loss, and energy transformation loss on the backscatter tag, the backscatter signal is orders of magnitude weaker than the carrier signal. Hence we can first leverage capture effect $^{1}$ to demodulate the carrier signal, using the standard LoRa demodulation scheme. Our task is then transformed into decoding the backscatter signal from the received signal.

Basic idea. The demodulation scheme of Aloba is motivated by the conventional RFID system. RFID system simplifies the backscatter signal decoding by adopting a sinusoidal tone as the carrier signal. In a similar way, if the LoRa receiver can transform the standard LoRa carrier signal into a constant sinusoidal tone, the variation of received signal would be solely determined by the backscatter signal. This implies an opportunity to detect the presence of backscatter signal and then decode it.

![](images/85f1ae6a69c25a9618fe402557468babbb9bfc28c53f47f279817417e3033c79.jpg)

Figure 7: Signal transformation. (a): two LoRa chirps with different initial frequencies. (b): conjugate down-chirps of these LoRa chirps. (c): the multiplication of the chirps and their conjugate down-chirps yields sinusoidal tone at the same frequency.   
![](images/7691929f6fc052da2a5ed957412586a7cebca147e3bb2b634fc2bd87348a196e.jpg)  
Figure 8: Superposition of sinusoidal carrier signal and backscatter signal. (a): carrier signal and backscatter signal are not strictly aligned or misaligned. (b): carrier signal and backscatter signal are strictly aligned. (c): carrier signal and backscatter signal are strictly misaligned.

# 3.1 Transforming Chirps into a Constant Sinusoidal Tone

Signal Transformation. The standard LoRa demodulation scheme multiplies LoRa chirps with a down-chirp (with the frequency changes from $+\frac{BW}{2}$ to $-\frac{BW}{2}$ ), yielding a sinusoidal tone. The frequency of this sinusoidal tone is determined by the initial frequency offset of LoRa chirps. In Aloba, we replace the standard down-chirp with the conjugate of incoming LoRa chirps, as shown in Figure 7(a)-(b). $^{2}$ This operation transforms all incoming LoRa chirps into a sinusoidal tone at the same frequency, as shown in Figure 7(c).

Amplitude variation of the sinusoidal tone. The sinusoidal tone obtained from the signal transformation can be regarded as the superposition of a sinusoidal carrier signal and a backscatter signal. As the backscatter signal is much weaker than the carrier signal, the receiver faces two possible signal combinations. i): When these two signals are either strictly aligned or misaligned (Figure 8(b)-(c)), we expect to see a significant amplitude variation on the received signal, based on which we can detect the presence of the backscatter signal. ii): Most of the time, however, these two signals are neither strictly aligned nor misaligned ((Figure 8(a)). Hence the amplitude of the received signal would not exhibit significant variation in the presence of backscatter signal. As a result, we cannot solely rely on the amplitude variation to detect the backscatter signal in the later case.

![](images/5da3cc32c11e2b7f24972f3d74f7f1518328d8f5b62db6e9f70167b65101f1c5.jpg)



Figure 9: Phase variation of the received signal after signal transformation. (a): phase jumping caused by ON-OFF switching of backscatter signal and false alarms. (b): eliminate the false alarm caused by signal transformation at the boundary of each LoRa chirp. (c) eliminate the false alarm caused by frequency wrapping within the LoRa chirp.

Phase variation of the sinusoidal tone. We instead leverage the phase variation of the received signal to detect the presence of the backscatter signal in the later case. When Aloba tag is at the OFF state, the received signal is determined by the carrier signal. When Aloba tag switches to the ON state, the presence of backscatter signal will alter the received signal, which leads to a phase jumping on the sinusoidal tone, as shown in Figure 9(a). This phase jumping caused by ON-OFF switching could serve as a clue to detect the presence of the backscatter signal. However, false alarm remains as both the frequency wrapping (from $\frac{BW}{2}$ to $-\frac{BW}{2}$ ) within the LoRa chirp and the sinusoidal tone transformation of each LoRa chirp could lead to an abrupt phase jump (denoted as false alarms in Figure 9(a)).

Two-step phase alignment. We design a two-step phase alignment algorithm to eliminate false alarms. In the first step, the receiver checks the boundary of each LoRa symbol on the received signal, wrapping the phase of remaining signal samples for a proper amount of degree such that they are all aligned with the phase samples of the LoRa symbol ahead. This process is repeated from the first LoRa symbol to the last one. After this step, all phase jumpings caused by sinusoidal transformation will be removed, as shown in Figure 9(b). In the second step, the receiver locates those phase jumpings caused by frequency wrapping by reconstructing the carrier symbols. $^{3}$ The receiver visits these phase jumping points sequentially and repeats the phase alignment operation in step one. After this process, all phase jumpings caused by frequency wrapping will be eliminated from the transformed sinusoidal tone, leaving us true positives (those caused by the presence of backscatter signal) only, as shown in Figure 9(c).

![](images/ae1066387ee20facb9f11b113f06b4e1932a9faf6d9f7684407839df00354a88.jpg)



Figure 10: Reconstructed signal. (a): amplitude variation of the reconstructed signal becomes indistinguishable when carrier signal and backscatter signal are not strictly aligned. (b): the phase of this reconstructed signal shows a distinctive pattern.

![](images/658882f1c266c6115c883186f9afddbb65012eab963e967a5db8e1e130cca228.jpg)



(a) Initial phase

![](images/43afafe0c582e8d82ab0edbaa04d4223c11fe8543cdcc85ab8ddece841887815.jpg)



(b) Classification   
Figure 11: The illustration of backscatter data decoding. (a): phase difference between the transformed sinusoidal tone plotted by blue lines and a reference sinusoidal tone plotted by gray lines. (b): reconstructed signal samples with and without backscatter signals aggregate two clusters, and backscatter preamble provides classification anchor points.

# 3.2 Signal Reconstruction and Decoding

In practice, phase noise exists due to timing offset and carrier frequency offset $[40]$ . It is thus unreliable to tell the presence of backscatter signal solely based on abrupt phase jumping points. To solve this problem, we design a robust, clustering-based detection algorithm as follows.

Signal reconstruction. The backscatter signal is modulated on the payload part of the carrier signal (will be detailed in §4.2). Once the receiver detects the payload of a LoRa packet, the receiver reconstructs the transformed sinusoidal tone as $S = A_{i}\Phi_{i}$ , where $A_{i}$ is the $i^{th}$ amplitude sample on the transformed sinusoidal tone. $\Phi_{i}$ is the phase difference between the $i^{th}$ phase sample on this transformed sinusoidal tone and the corresponding phase sample on a reference sinusoidal tone, as shown in Figure 11(a). Figure 10 shows the amplitude and phase of the reconstructed signal. We can see the amplitude variation of this reconstructed signal becomes indistinguishable when these two signals are not strictly aligned, while the phase readings of this reconstructed signal demonstrate a distinctive pattern, which can be leveraged for backscatter signal decoding.

![](images/9051ac7469d997d8939b91709171c2151fdc8a81ae129b78a7387b05a7bf84c9.jpg)



(a) Two tags

![](images/c6c7cc16cb9ec8e4429beb84b0563a87369d86c025db980bf4b42aa2463c5f59.jpg)



(b) Three tags   
Figure 12: Classification results on I-Q plane when multiple tags are concurrent transmitted. (a): two tags correspond to four clusters. (b): three tags correspond to eight clusters.

Backscatter signal decoding. We plot all reconstructed signal samples on the constellation diagram (I-Q plane). As shown in Figure 11(b), these symbols are naturally grouped into two clusters: one for the none-existence of backscatter signal, and another for the existence of backscatter signal. We can then leverage the preamble of the backscatter signal (a 16-bit Barker code, detailed in §4.2) to distinguish these two clusters and decode each trail of backscatter signals accordingly. This clustering-based method leverages all signal samples to detect the presence of backscatter signal, hence it is more robust than the phase jumping based detection method.

On a high-level, Aloba shares the similar decoding principle with the standard LoRa decoding algorithm: transforming the frequency-shifting LoRa chirp into a constant sinusoidal tone. However, the conventional LoRa decoding algorithm multiplies the incoming LoRa chirp with a standard down-chirp and then tracks the peak on FFT bins to demodulate the LoRa chirps. In contrast, the Aloba receiver replaces this down-chirp with the conjugate of each incoming LoRa chirp. It then tracks the amplitude and phase variation to demodulate the backscatter signals overlaid on the carrier LoRa signals. This allows the Aloba receiver to decode both the carrier signal and backscatter signal on the same frequency band.

# 3.3 Extension to the Multi-tag Scenario

The above demodulation scheme can be easily extended to the multi-tag scenario. Suppose there are $M(M > 1)$ Aloba tags. The received signal would be the superposition of multiple backscatter signals and the carrier signal. Following the signal transformation introduced in §3.1, the receiver first transforms this received signals to a sinusoidal tone. It then follows the signal reconstruction introduced in §3.2 to reconstruct the received signal. We thus expect to see $2^{M}$ clusters on the constellation diagram. Figure 12(a) and Figure 12(b) show the constellation diagram of two tags' and three tags' replies, respectively. With these symbol clusters, we can then apply the state-of-the-art parallel decoding algorithms such as [7, 12, 13, 33] to decode the backscatter signals.

![](images/794c3851f755849e1b556d4f49057bb042c4cec859b6e3cb85e359af07dbd042.jpg)



(a) LoRa packet structure   
![](images/12fe8922369b8fd45a5b35b6e9e5439e7238f454b1c8e10abff5efa265e11dfb.jpg)



(b) Packet detection result

Figure 13: LoRa preamble and the corresponding RSSI profile. The ten consecutive up-chirps on LoRa preamble (top) leads to ten equally-spaced RSS pulses (below).   
![](images/e134e279479814606dc0d869c49c0c3371e9217d74247168faefcfe3c1062914.jpg)



Figure 14: The circuit design of LoRa packet detector.

# 4 ALOBA TAG DESIGN

We describe the tag operation in this section.

# 4.1 Low-power LoRa Packet Detection

Aloba tag takes the ambient LoRa signal as the carrier signal. The standard LoRa packet detection scheme is not suitable for Aloba due to its high power consumption.

In Aloba, we design a simple yet effective packet detection circuit to pick up the LoRa signal from the ambient noise and unconcerned signals. Our design exploits the unique pattern of LoRa symbols in the LoRa preamble: ten consecutive up-chirps with zero initial frequency offset. When the incoming signal passes through a low-pass filter (with a cutoff frequency at BW/4), the ten consecutive up-chirps on a LoRa preamble will lead to ten equally spaced RSS (received signal strength) pulses (Figure 13(b)), whereas the noise and other legacy signals will not. Hence Aloba can pick up the LoRa preamble by detecting the appearance of this unique RSS pattern.

Figure 14 shows the circuit design of Aloba packet detection module. The signals are first digitized by an ultra low-power Analog-to-Digital Converter (ADC) on the FPGA board. The sampling rate of this ADC is 250 KHz. LoRa supports different bandwidth (e.g., 500 KHz, 250 KHz, 125 KHz) for data transmission. We thus need a reconfigurable low-pass filter. In Aloba, we implement a moving average filter on software as the low-pass filter [24, 29]. The cutoff frequency of this software-defined low-pass filter can be easily reconfigured by setting different window size w. For instance, w = 5 leads to a 30 KHz cutting-off frequency. Once the FPGA detect ten equally spaced RSS pulses (i.e., the amplitude of incoming signals is larger than a threshold), it immediately knows the arrival of a LoRa packet and automatically switches to the modulation mode.

![](images/f57b6e5042fd5c946304c79ba6e6df6796b6d693f448c45d4788c45ca9af19a3.jpg)



Figure 15: LoRa packet structure and backscatter packet structure

We empirically set this RSS threshold to -60 dBm, which yields the best detection accuracy in our experiments.

Power consumption. Both impedance matching and envelope detector are passive components (e.g., inductance, capacitors, and diodes), hence the energy consumption of this packet detection circuit mainly comes from the ADC and FPGA. Our ADC works on the low sampling rate mode and the detection based on RSS at the FPGA is simple. The total power consumption of ADC and FPGA is around 0.3 mW.

# 4.2 Modulation

After detecting the LoRa preamble, Aloba waits for another 2.25 symbol times (sync. symbols) and then modulates data on the payload part of this incoming LoRa packet using OOK: reflecting the signal when transmitting a bit one, and absorbing the signal when transmitting a bit zero. The backscatter packet contains four fields as shown in Figure 15: a 16-bit baker code-based preamble (010101 · · · 010101), a 4-bit modulation rate field, a 8-bit payload length field, and the payload.

# 5 ALOBA MAC LAYER

We sketch the MAC layer design in this section. We allocate an assigned channel among multiple Aloba tags. Each tag randomly picks up a time slot to transmit. Upon detecting the carrier signals, these Aloba tags achieve time synchronization and reflect backscatter signals. When there are multiple active LoRa nodes in the LoRaWAN, these LoRa nodes also abide by the time-domain ALOHA protocol. In this way, LoRa nodes and Aloba tags form a hybrid LoRaWAN network.

ALOHA protocol can reduce the collision probability. However, it does not guarantee the collision-free transmission. Collision happens when multiple Aloba tags select the same slot. Each tag makes its own choice independent with the other tags. If we have N tags and there are K time slots, the probability that R tags will be transmitted in one time slot is $P = \binom{N}{R}(\frac{1}{K})^{R}(1 - \frac{1}{K})^{N-R}$ [11]. For instance, suppose there are 100 tags and 128 time slots, the probability that 5 tags will be transmitted in one time slot is 0.1%. Our demodulation scheme can be easily extended to the multi-tag scenario. The evaluation in §7.5 shows that the number of concurrent tags supported by Aloba is five.

# 6 IMPLEMENTATION

Tag hardware. The packet detection module is prototyped on a single-layer PCB using commercial off-the-shelf circuit components as shown in Figure 18. The packet detection module uses one omnidirectional antenna with 3 dBi gain [21] and a DE0-Nano-SoC FPGA with an ultra low-power ADC [22]. We optimize the impedance matching coefficient to provide the maximum power transfer from the antenna to the envelope detection. The packet detection module is wired to the WISP 5.0 [37] for evaluation.

Transmitter and receiver. We use a commercial LoRa node (a STM32L083RZ board [30] carrying a Semtech SX1276 [27] chip) with one 3 dBi gain omni-directional antenna [21] as the transmitter, an USRP N210 [31] equipped with the same type of antenna as the receiver. The USRP samples the signal at 10 MHz sampling rate. The LoRa receiver runs the standard LoRa preamble detection algorithm [23] to detect LoRa transmissions and further locates each LoRa symbol on the payload. The receiver then runs Aloba decoding algorithm to decode both the backscatter signal and the ambient LoRa signal.

Extension to commercial LoRa gateways. While the current Aloba decoding algorithm is implemented on USRP, it is worth noting that this algorithm can be easily implemented on a commercial LoRa gateway, since this algorithm requires only the raw signal samples which are accessible on most LoRa RF-front, e.g., Semtech SX1257 front-end [26]. We leave the algorithm implementation on commercial LoRa gateways as our future work.

# 7 EVALUATION

In this section, we first conduct head-to-head comparison with PLoRa [35], the state-of-the-art ambient LoRa backscatter system. We then conduct micro-benchmarks to study the performance of Aloba in various settings, including different LoRa bandwidth, tag-to-source distances, modulation rate, environment, and channel conditions.

# 7.1 Experimental Setup

The LoRa transmitter and the receiver both work on channel one (902.5 MHz). The payload of each LoRa packet consists of 20 symbols. The default spreading factor (SF), coding rate, and bandwidth (BW) of the LoRa signal are 7, 1, and 125 KHz, respectively. The transmission power of the LoRa sender is 20 dBm. We evaluate Aloba both indoors (classroom, hallway and warehouse as shown in Figure 16.) and outdoors (open road, square and parking lot, as shown in Figure 17).

We take throughput and maximum backscatter range as the key metric to evaluate Aloba's performance. Throughput measures the amount of backscattered data correctly decoded within one second at the LoRa receiver. Maximum backscatter range refers to the maximum distance between the Aloba tag and the LoRa receiver when the bit error rate (BER) of the backscatter data is lower than 0.001. We send 1,000 LoRa packets in each experiment, and then repeat the experiment 100 times. Finally we report the averaged result to ensure the statistical validity.

# 7.2 Head-to-head Comparison with PLoRa: Link Throughput

We compare Aloba with PLoRa [35] in various settings. PLoRa encodes one bit per LoRa symbol. The theoretical link throughput

![](images/fd5227e7e33c2d0679fcc40c53275b23bc2e37b5f5fea184c0566d512e35c150.jpg)



Figure 16: The floor plans of indoor experiment field

![](images/afbdf0714056fe4e13dbfb9dbc53245367ccd56b18c27cde77bddcb9b2f263e0.jpg)



Figure 17: Indoor and outdoor experiment field

![](images/4b96200d78982017c19b172dc0429f07d7bf9f4573723b462bcf118af72ee4ee.jpg)



Figure 18: Aloba tag

![](images/d900371eb0f44a59f88e0d416b23c44f0e808d4abd64ca4d8c59e469ab4dbe73.jpg)



(a) tag-to-receiver distance=50m

![](images/1cf2dfd1460a74daa825f187fadd3733decb502db4556f811b617ac3875fb1e3.jpg)



(b) tag-to-receiver distance=100m

![](images/5b1ea711d63ae4b5ee9fccd6bcec322110962be56336792deee3b7d045b61f1e.jpg)



(c) tag-to-receiver distance=150m

![](images/bca899638a3890002cdb3c577ccb76c6c34288e17600f760f0dfeb596f389ff1.jpg)



(d) tag-to-receiver distance=200m

![](images/25335db37e554a69c3ab4d5c01b334b0d8bdb1150fb173e20dcf17e8fe2f25df.jpg)



(e) tag-to-receiver distance=250m

![](images/b4bd6e1e4c5e151a0f2ae5eae0f854c9ed524a4b02913d8c1084f598cc822ac6.jpg)



(f) tag-to-receiver distance=300m   
Figure 19: Link throughput of Aloba and PLoRa in different tag-to-receiver distance settings.

of LoRa carrier and PLoRa are $\frac{BW}{2^{SF}} \cdot SF$ and $\frac{BW}{2^{SF}}$ , respectively. The theoretical link throughput of Aloba is determined by the rate of ON-OFF keying operation.

In these experiments, we place the receiver 50 m, 100 m, 150 m, 200 m, 250 m, and 300 m away from the tag. Within each distance setting, we further vary the distance between the source and the backscatter tag to measure the throughput of PLoRa and Aloba. We tune the spreading factor and bandwidth of the carrier signal to ensure the fair comparison with PLoRa. Figure 19 shows the result. We have two observations from these experimental results.

First, we observe the link throughput of Aloba is orders of magnitude higher than that of PLoRa when the LoRa receiver is within 200 m of the source (Figure 19(a)-(d)). Specifically, when the tag is collocated with the source (with an 10 cm spacing), the link throughput of Aloba is $10.4 \times -52.4 \times$ higher than that of PLoRa in different source-to-receiver distance settings. This is expected since the OOK design enables Aloba to tune up its throughput to best utilize the better link quality in short tag-to-source distance settings. This flexible modulation design enables Aloba to achieve even $1.5 \times -7.3 \times$ higher throughput than that of the LoRa carrier. In contrast, PLoRa adopts a fixed modulation rate and thus achieves consistently low throughput in all different distance settings.

Second, the link throughput achieved by Aloba and PLoRa both decreases with increasing tag-to-source distance, primarily due to the decreasing SNR of the backscattered signal (Figure 19). To expand the backscatter range, similar to the existing backscatter systems [35], Aloba has to sacrifice the throughput to ensure a longer backscatter range (Figure 19(e)). Aloba essentially relies on energy to decode backscatter signals, thus the performance gain of Aloba over PloRa is achieved mainly within short and medium communication range ( $\leq 250$ m shown in Figure 19(f)), since that the signal attenuation, insertion loss, and energy transformation loss on the backscatter tag result in that the backscatter signal is orders of magnitude weaker than the carrier signal. For example, Aloba achieves the throughput of 0.93 Kbps when we place the tag 1 m away from the LoRa sender and the LoRa receiver is within 250 m of the source.

![](images/cf3c9030d78a4bcd6486e7a7fca890f15da53b1a542847746692ee245fd9758b.jpg)



(a) Throughput

![](images/9c3b04ca51b668eb7dcef806544053a424f6ecf8ee9922dea174d0c880191604.jpg)



(a) Throughput

![](images/8cd81d167b2444c24a841fff8403acc1ca71585e70738627b36d201d55121dba.jpg)



(a) Throughput

![](images/f2658ff5bcd7739a8821c763cc2757fc798a8d3680b2cd682970b955cda8fdcb.jpg)



(b) Range

![](images/988d1dec96e1acf19c174ef25ae63b9bafd694af79313c20b389365125f1546f.jpg)



(b) Range

![](images/c3327598b755d4d3d8dcb5986cd8281324288ff74c7c0985059efda46babb178.jpg)



(b) Range   
Figure 20: Performance comparison with different SF settings   
Figure 21: Performance comparison with different BW settings   
Figure 22: Performance comparison with different switch rate settings

# 7.3 Head-to-head Comparison with PLoRa in Different SF and BW Settings

The link throughput of PLoRa is highly sensitive to the LoRa carrier parameters, including spreading factor (SF) and bandwidth (BW). In this section, we compare the performance of PLoRa and Aloba in different SF and BW settings.

7.3.1 Impact of spreading factor (SF). We set the BW at 125 KHz and the switch rate of Aloba tag at 60 KHz. Then we change the value of SF from 7 to 12 and the experiment results are shown in Figure 20(a) and Figure 20(b). We find that the throughput of PLoRa decreases and the backscatter range of PLoRa increases with the increase of SF. The throughput and the backscatter range of Aloba are relatively stable. Specifically, when the value of SF increases from 7 to 12, the throughput of Aloba is $61 \times -1800 \times$ higher than that of PLoRa and the range of PLoRa is $2.1 \times -4.5 \times$ higher than that of Aloba.

7.3.2 Impact of bandwidth (BW). We set the SF at 7 and the switch rate of Aloba tag at 60 KHz. Then we increase the value of BW from 125 KHz to 500 KHz, and the experiment results are shown in Figure 21(a) and Figure 21(b). The throughput of PLoRa increases and the maximum backscatter range of PLoRa decreases with the increase of BW. The throughput and the backscatter range of Aloba

are relatively stable. For example, when the value of BW increases from 125 KHz to 500 KHz, the throughput of Aloba is 61×-15× higher than that of PLoRa and the range of PLoRa is 2.1×-1.6× higher than Aloba's.

Therefore, the performance of PLoRa is more susceptible to the parameters of LoRa excitation signals, but the performance of Aloba is reliable in different LoRa parameter settings. In practice, the performance of Aloba based on the OOK design is affected by the tag's switch rate. So we further conduct experiments to evaluate Aloba's performance under different switch rate.

7.3.3 Impact of switch rate. The throughput of Aloba theoretically equals to the switch rate of Aloba tag. The larger the switch rate is, the larger the throughput is. Whereas, the backscatter range decreases with increase of switch rate due to the decreasing SNR of the backscattered signal. In this experiment, we place the tag 1 m away from the source, and set SF and BW at 7 and 125 KHz. Then we change the switch rate from 10 KHz to 150 KHz. Figure 22(a) and Figure 22(b) show the experiment results. First, the throughput of Aloba varies from 9.9 Kbps to 121.4 Kbps when the switch rate varies from 10 KHz to 150 KHz. The gap between the throughput and the theoretical throughput increases from 0.1 Kbps to 28.6 Kbps due to the increasing BER of backscatter data. Second, the backscatter range of Aloba decreases from 225.6 m to 71.4 m. Hence, Aloba can achieve flexible throughput and backscatter range by adjusting the tag's switch rate.

# 7.4 Indoor Experiments

We further evaluate the performance of Aloba in indoor environments and observe Aloba's performance when the backscatter tag penetrates one concrete wall or two concrete walls. The impact of multi-path in indoor environment on our decoding algorithm is negligible. In our experiments, the LoRa sender and the Aloba tag in the classroom, and the LoRa receiver in the office. We vary the tag-to-source distance and the switch rate to study their impact on Aloba performance. The default LoRa SF is 7 and BW is 125 KHz. The tag-to-receiver distance is 10 m when we measure the variation of throughput. Later, we move the receiver to measure the maximum backscatter range when the BER is lower than 0.001.

![](images/e76d45d1864585002164aa993969d9b7345ce3ab95ecc76addffdd7431dfe144.jpg)



Figure 23: Aloba performance in NLoS indoor environments (penetrating one concrete wall)

![](images/fb1205a0c9ae02ea94634ba28ae70657dc6b238cf0e9bd8d59cd4110af4a655b.jpg)



Figure 25: Aloba performance in multi-tag scenario

7.4.1 Penetrating one concrete wall. First, when the tag is collocated with the source (with an 10 cm spacing) and the switch rate is 60 KHz, the backscatter signal can be decoded by the receiver 32.6 m away from the Aloba tag as shown in Figure 23(a). As we extend the distance between the source and Aloba tag to 5 m, the backscatter signal becomes weaker, and thus the backscatter range decreases to 12.9 m. The throughput of Aloba when we vary the tag-to-source distance is stable at 60 KHz.

Second, we adjust the switch rate from 10 KHz to 100 KHz to balance the data rate and backscatter range. We put the tag 1 m away from the source. As shown in Figure 23(b), the throughput of Aloba increases with the increase of switch rate, and the backscatter range of Aloba decreases with the increase of switch rate. When the switch rate is 10 KHz, the backscatter signal can be decoded by the receiver 31.4 m away from the Aloba tag. When the switch rate is 100 KHz, the backscatter signal can only be decoded by the receiver 17.2 m away from the Aloba tag.

7.4.2 Penetrating two concrete walls. The performance of Aloba after penetrating two concrete walls is worse than the performance of Aloba after penetrating one concrete wall. First, when the tag is collocated with the source (with an 10 cm spacing) and the switch

![](images/3e6b02033edaa6d559c28123b1f063d1fd506b429943715a2c05d8d1ba7bf7b5.jpg)



Figure 24: Aloba performance in NLoS indoor environments (penetrating two concrete walls)

![](images/194d6d778d6c576f832083ab3d75f71553a61d45a0192f2cdabb997ce4c15aa4.jpg)



Figure 26: Packet detection result of tag

rate is 60 KHz, the backscatter signal can be decoded by the receiver 15.6 m away from the Aloba tag as shown in Figure 24(a). As we extend the distance between the source and Aloba tag to 5 m, the backscatter signal becomes much weaker after penetrating two concrete walls. In this condition, the gap between the throughput and the theoretical throughput increases to 20.4 Kbps.

Second, we adjust the switch rate from 10 KHz to 100 KHz to balance the data rate and backscatter range. We put the tag 1 m away from the source. As shown in Figure 24(b), the throughput of Aloba increases with the increase of switch rate, and the backscatter range of Aloba decreases with the increase of switch rate. When the switch rate is 10 KHz, the backscatter signal can be decoded by the receiver 16.4 m away from the Aloba tag. When the switch rate is 100 KHz, the backscatter signal can only be decoded by the receiver 5.6 m away from the Aloba tag after penetrating two concrete walls.

# 7.5 Multi-tag Scenario

We further deploy multiple Aloba tags (2–5) outdoors to examine the multi-tag decoding capability. The switching rate of these tags are set to 60 KHz by default. The distance between each tag and the source varies from one meter to five meters. We show the bit error rate (BER) and the network throughput (sum of each backscatter link) in Figure 25.

We observe the BER is below 0.001 when there is one or two tags in the network. The BER then grows to around 0.05 with increasing number of tags. The high BER is primarily due to the increasing interference in the I/Q plane. With Mac-layer control, i.e., TDMA ( $\S5$ ), we envision less interference among tags and thus expect to see a lower BER of individual backscatter link. On the other hand, we observe the network throughput grows steadily from 60 Kbps to around 200 Kbps when the number of tags grows to five. While the network scale in testing is limited to five tags, we believe our system can support more tags by exploring both the frequency and time division.

![](images/212af85453e93dd275c23f5c82912a021260f480f9724266dd3640f5a9dd3de0.jpg)



Figure 27: LoRa packet reception in different scenarios

# 7.6 Packet Detection Accuracy of Aloba

The Aloba tag needs to pick up the ambient LoRa transmissions from other interfering signals before backscattering. In this subsection, we study the effective LoRa packet detection range and detection accuracy of the Aloba tag. The LoRa sender continuously transmits LoRa packets and the Aloba tag detects the LoRa signals. The distance between the LoRa sender and the LoRa receiver is 200 m. We move the Aloba tag to different locations.

The experiment result is shown in Figure 26. The RSSI of the detectable LoRa signals decreases with the increase of the tag-to-source distance. At the same time, the packet detection error increases. The detection error is 0.003 when the tag-to-source distance is 10 m, however, the detection error increases to 0.028 when the tag-to-source distance is 50 m. When the upper limit of detection error is 0.01, the packet detection range is 30 m.

# 7.7 Impact on LoRa Reception

The Aloba tag adopts the modulation of OOK and it doesn't modify the frequency of the LoRa signal. Therefore, the LoRa packets can still be decoded by the LoRa receiver with high sensitivity. In this subsection, we conduct experiments to study the impact of Aloba on the LoRa packet reception.

Figure 27(a) shows the experiment result in the outdoor environment. The PRR of LoRa packet without Aloba tag is higher than that with Aloba tag. The shorter the tag-to-source distance is, the greater the influence of the Aloba tag on the LoRa PRR is. When the tag-to-source distance is 1 m, the average PRR of LoRa packets decreases by 0.6% compared to the PRR of LoRa packets without Aloba tag. When the tag-to-source distance is 5 m, the average PRR of LoRa packets decreases by 0.1% compared to the PRR of LoRa packets without Aloba tag. Figure 27(b) shows the experiment result in the indoor environment. The impact of Aloba tag on LoRa packets in indoor environment is slightly larger than that in outdoor environment. These results validate that Aloba has negligible influence on LoRa packet reception.

# 8 RELATED WORK

Backscatter systems. In recent years, RF signals, such as TV, WiFi, FM, BLE, LoRa signals, have been widely exploited for backscatter communication. Ambient backscatter [16] reflects broadcast TV or cellular transmissions to achieve device-to-device communication. WiFi backscatter [14] reuses the WiFi signals to convey information by modulating the CSI and RSSI measurements. The data rate of ambient backscatter and WiFi backscatter is limited to 1 Kbps.

In order to improve the data rate, Turbo charging $[34]$ uses the multi-antenna cancellation design with the coding mechanism to achieve the data rate of 1 Mbps. BackFi $[1]$ modulates information by changing the phase of the received WiFi signals, which improves the communication rate to 5 Mbps. Passive WiFi $[14]$ enables a passive tag to generate 802.11b transmissions by leveraging a dedicated excitation device. HitchHike $[48]$ allows a backscatter tag to embed its information on standard 802.11b packets, by translating the original transmitted 802.11b codeword to another valid codeword. FreeRider $[49]$ extends the technique of codeword translation to other radios, such as 802.11g/n, Bluetooth, and ZigBee. OFDMA-WiFi $[51]$ enables OFDMA in WiFi backscatter for capacity and concurrency enhancement. But the farthest communication range is only tens of meters.

To further improve the communication range, researchers focus on Low-Power Wide-Area Network (LPWAN) technologies. Among the LPWAN technologies $[25, 28]$ , LoRa $[23]$ is resilient to interference due to its high receiving sensitivity, making it a natural choice for backscatter. LoRa backscatter $[39]$ synthesizes legitimate LoRa packets to extend the communication to 2 km. However, it requires a dedicated device to generate the excitation signal. PLoRa $[35]$ is the most relevant work with Aloba, which takes ambient LoRa transmissions as the excitation signals and modulates the original LoRa chirp signal into a new standard LoRa chirp signal at another frequency band. Whereas, PLoRa is not spectrum efficient and inevitably consumes the already crowded wireless spectrum.

Compared to the existing works, Aloba adopts the modulation of ON-OFF Keying (OOK) and the data rate can be easily adjusted by tuning the frequency of this RF switch. By taking the ambient LoRa signals as the excitation, the backscatter tag could leverage the unique processing gain brought by the chirp signal design to enable long-range backscatter communication. In this way, Aloba supports flexible data rate at different transmission range. Moreover, Aloba achieves high spectrum efficiency.

Self-interference mitigation. There are three types of approaches for self-interference mitigation in the backscatter system: interference cancellation, parallel decoding, and frequency shifting.

Interference cancellation. RFID system is a typical backscatter system with the full-duplex reader. To mitigate self-interference, the RFID reader uses sophisticated cancellation circuit, including tunable phase shifter and attenuator, to recover the backscatter signal. This method increases the power consumption and limits the achievable range [8]. Liu et al. [17] present a design that enables full-duplex communication on ambient backscatter devices and reduce self-interference by using only fully-passive analog components. BackFi [1] estimates the channel variation and proposes a wideband self-interference cancellation scheme to decode WiFi backscatter signals.

Parallel decoding. Parallel decoding makes it possible to demodulate carrier signals and backscatter signals at the same time. Laissez-Faire [7] extracts edges from interleaved RFID signals, separates collisions, and corrects errors. FlipTracer [13] presents a probabilistic model to capture the transition pattern of collided signals and achieves parallel decoding for RFID backscatter. Choir [3] disentangles the interfering LoRa transmissions by leveraging the hardware imperfection. Netscatter [6] decodes the concurrent LoRa transmissions using the FFT operation, since the cyclic shifting of chirps in the time domain translates to offsets in the frequency domain. FTrack [44] exploits the time-domain information of symbol edges to recover the collided LoRa symbols.

Frequency shifting. Recent backscatter proposals shift the frequency of backscatter signals away from the carrier signals to avoid self-interference [10, 35, 36, 41, 42, 50]. For example, FS-Backscatter [50] shifts WiFi signals to a different non-overlapping frequency band. FM-Backscatter [42] transforms the multiplication operation on RF signals into an FM addition operation on the audio signals to shift frequency. LoRea [41] and PLoRa [41] mitigate the self-interference and extend the communication range by keeping carrier signal and backscattered signal apart in frequency. Whereas, these methods occupy extra spectrum resources.

We cannot borrow the above existing methods to solve LoRa self-interference, as we have analyzed in §2. Therefore, Aloba includes a novel decoding scheme to demodulate backscatter signal by transforming the LoRa carrier signal to sinusoidal carrier signal and detecting the fine-grained changes on the phase and amplitude of the signal.

# 9 DISCUSSION

Effective communication range. The backscatter range scales with the strength of backscatter signals. Due to signal attenuation, insertion loss, and energy transformation loss on the backscatter tag, the backscatter signal is orders of magnitude weaker than the carrier signal. Hence Aloba cannot achieve similar communication range with active LoRa nodes. There are multiple ways to increase the backscatter range. For example, leveraging bemforming techniques or negative impedance components like tunnel diode and we leave it as our future work.

Energy efficiency. Like many state-of-the-art ambient backscatter designs (e.g., PLoRa [35], Turbo charging [34], HitchHike [48]), we adopt a palm-size solar panel to harvest energy. This is different to the passive RFID system where the power comes from the carrier signal. Aloba adopts a low-power ADC and FPGA for packet detection. Hence it consumes more power than conventional RFID systems that assumes an always-on carrier signal. To reduce the power consumption on packet detection, one possible solution could be implementing the packet detection module on Application-specific integrated circuit ASIC and we leave it for our future work.

Time synchronization. There are two critical time synchronization processes that affect the system performance. The first one happens at the Aloba tag where the tag detects the boundary of LoRa chirp and synchronizes with the payload part for modulation (backscatter). The error in synchronization will introduce a time offset between the carrier signal and the backscatter signal. A moving window-based decoding strategy can be used to tolerant the above synchronization error. The moving position which satisfies the requirement of 16-bit baker code-based preamble of Aloba and achieves the maximum distance between two clusters with and without backscatter signals is the corresponding position of the Aloba decoding window. The second one happens at the Aloba receiver where the receiver detects and synchronizes with the boundary of the LoRa chirp for chirp transformation. When the time offset caused by the above chirp edge detection errors is smaller than the time range bin of LoRa chirp (the minimum time offset between two LoRa chirps, which is equal to $\frac{1}{BW}$ ), the chirp transformation can be achieved successfully and the impact on the Aloba decoding can be neglected. Otherwise, the LoRa chirps will be decoded incorrectly and the LoRa packet will be discarded at the LoRa receiver, not to mention the piggy-backed backscatter data.

Potential applications. Aloba can be used in many application scenarios, for example, keeping track of the status of machines in the factory (e.g., vibration, noise, rotation), monitoring the operation of coal mine underground system (e.g., drainage, power supply, and machine status), and uploading the information of all bulk goods in the container in one batch on the seaport. On the one hand, these applications demand moderate-throughput (tens of Kbps) communication links for sensing data forwarding. On the other hand, these data forwarding links should be also low-power and long-range, allowing sensors to transmit their data back to the gateway hundreds of meters away without extra human intervention or frequent battery for two reasons. First, some of these machines may produce strong noise, flash intense light and discharge harmful gases. Second, the operation environment of these applications is complex, and it is easy to have potential safety hazards. Therefore, Aloba with the throughput of 40 Kbps and transmission range of 200 m is applicable to the above scenarios.

# 10 CONCLUSION

Aloba is an ambient LoRa backscatter design using ON-OFF Keying that provides flexible data rate and transmission range for different IoT applications and deployments. By allowing the coexistence of the backscatter signal and the carrier signal in the same frequency band, Aloba achieves a higher spectrum efficiency. Our design contributions are a low-power backscatter design that can pick up the ambient LoRa transmissions from other interfering signals and a decoding algorithm running on the LoRa receiver that can decode both the backscatter signal and the LoRa excitation signal from their superposition. Evaluation results demonstrate that Aloba can achieve various data rates (39.5–199.4 Kbps) at various distances (50–200 m) in the wild. Compared with the state-of-the-art system PLoRa [35], Aloba is 10.4–52.4× better in terms of throughput.

# ACKNOWLEDGMENTS

We would like to thank the anonymous reviewers and the shepherd for their valuable comments and helpful suggestions. This work is supported in part by National Key R&D Program of China No. 2017YFB1003000, National Science Fund of China under grant No. 61772306, the Smart Xingfu Lindai Project, and the R&D Project of Key Core Technology and Generic Technology in Shanxi Province (2020XXX007).

# REFERENCES

[1] Dinesh Bharadia, Kiran Raj Joshi, Manikanta Kotaru, and Sachin Katti. 2018. BackFi: High throughput WiFi backscatter. In Proceedings of ACM SIGCOMM, Budapest, Hungary, August 20-25, 2018.   
[2] János Czentye, János Dóka, Árpád Nagy, László Toka, Balázs Sonkoly, and Róbert Szabó. 2018. Controlling drones from 5G networks. In Proceedings of ACM SIGCOMM, Budapest, Hungary, August 20-25, 2018.   
[3] Rashad Eletreby, Diana Zhang, Swarun Kumar, and Osman Yagan. 2017. Empowering Low-Power Wide Area Networks in Urban Settings. In Proceedings of ACM SIGCOMM, Los Angeles, CA, USA, August 21-25, 2017.   
[4] Kensuke Fukuda, John Heidemann, Abdul Qadeer, Kensuke Fukuda, John Heidemann, and Abdul Qadeer. 2017. Detecting malicious activity with DNS backscatter over time. IEEE/ACM Transactions on Networking 25, 5 (2017), 3203–3218.   
[5] Chuhan Gao, Yilong Li, and Xinyu Zhang. 2018. LiveTag: Sensing human-object interaction through passive chipless WiFi tags. In Proceedings of USENIX NSDI, Renton, WA, USA, April 9-11, 2018.   
[6] Mehrdad Hessar, Ali Najafi, and Shyamnath Gollakota. 2016. NetScatter: Enabling Large-Scale Backscatter Networks. In Proceedings of USENIX NSDI, Santa Clara, CA, March 16-18, 2016.   
[7] Pan Hu, Pengyu Zhang, and Deepak Ganesan. 2015. Laissez-Faire: Fully Asymmetric Backscatter Communication. In Proceedings of ACM SIGCOMM, London, United Kingdom, August 17-21, 2015.   
[8] Pan Hu, Pengyu Zhang, Mohammad Rostami, and Deepak Ganesan. 2016. Braidio: An Integrated Active-Passive Radio for Mobile Devices with Asymmetric Energy Budgets. In Proceedings of ACM SIGCOMM, Salvador, Brazil, August 22-26 2016.   
[9] Vikram Iyer, Rajalakshmi Nandakumar, Anran Wang, Sawyer B. Fuller, and Shyamnath Gollakota. 2019. Living IoT: A flying wireless platform on live insects. In Proceedings of ACM MobiCom, Los Cabos, Mexico, October 21-25, 2019.   
[10] Vikram Iyer, Vamsi Talla, Bryce Kellogg, Shyamnath Gollakota, and Joshua Smith. 2016. Inter-Technology Backscatter: Towards Internet Connectivity for Implanted Devices. In Proceedings of ACM SIGCOMM, Salvador, Brazil, August 22-26 2016.   
[11] Meng Jin, Yuan He, Chengkun Jiang, and Yunhao Liu. 2020. Fireworks: Channel Estimation of Parallel Backscattered Signals. In Proceedings of IEEE/ACM IPSN, Virtual event, Australia, April 21-24, 2020.   
[12] Meng Jin, Yuan He, Xin Meng, Dingyi Fang, and Xiaojiang Chen. 2018. Parallel Backscatter in the Wild: When Burstiness and Randomness Play with You. In Proceedings of ACM MobiCom, New Delhi, India, October 29-November 02, 2018.   
[13] Meng Jin, Yuan He, Xin Meng, Yilun Zheng, Dingyi Fang, and Xiaojiang Chen. 2017. FlipTracer: Practical Parallel Decoding for Backscatter Communication. IEEE/ACM Transactions on Networking 25, 1 (2017), 3559–3572.   
[14] Bryce Kellogg, Aaron Parks, Shyamnath Gollakota, Joshua R. Smith, and David Wetherall. 2014. WiFi backscatter: Internet connectivity for RF-powered devices. In Proceedings of ACM SIGCOMM, Chicago, USA, August 17-22, 2014.   
[15] Bryce Kellogg, Vamsi Talla, Joshua R. Smith, and Shyamnath Gollakot. 2016. Passive WiFi: Bringing low power to WiFi transmissions. In Proceedings of USENIX NSDI, Santa Clara, CA, March 16-18, 2016.   
[16] Vincent Liu, Aaron Parks, Vamsi Talla, Shyamnath Gollakota, David Wetherall, and Joshua R. Smith. 2013. Ambient backscatter: Wireless communication out of thin air. In Proceedings of ACM SIGCOMM, Hong Kong, China, August 12-16, 2013.   
[17] Vincent Liu, Vamsi Talla, and Shyamnath Gollakota. 2014. Enabling instantaneous feedback with full-duplex backscatter. In Proceedings of ACM MobiCom, Maui, Hawaii, USA, September 7-11, 2014.   
[18] Zhiqing Luo, Wei Wang, Jun Qu, Tao Jiang, and Qian Zheng. 2018. Improving IoT security with backscatter assistance. In Proceedings of ACM SenSys, Shenzhen, China, November 4-7, 2018.   
[19] Zhihong Luo, Qiping Zhang, Yunfei Ma, Manish Singh, and Fadel Adib. 2019. 3D backscatter localization for fine-grained robotics. In Proceedings of USENIX NSDI, Boston, MA, February 26-28, 2019.   
[20] Beshr Al Nahas, Simon Duquennoy, and Olaf Landsiedel. 2012. Network-wide Consensus Utilizing the Capture Effect in Low-power Wireless Networks. In Proceedings of ACM SIGCOMM, Helsinki, Finland, August 13-17, 2012.   
[21] Online. 2020. Antenna. https://www.hARRIsaerial.com/product/900-mhz-3dbibase-antenna/   
[22] Online. 2020. DE0-Nano-SoC FPGA. https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=165&No=1081   
[23] Online. 2020. LoRa Alliance. https://www.lora-alliance.org/   
[24] Online. 2020. Moving Average. https://www.dsprelated.com/showthread/comp.dsp/155807-1.php   
[25] Online. 2020. NB-IoT. https://en.wikipedia.org/wiki/Narrowband\_IoT

[26] Online. 2020. Semtech SX1257. https://www.semtech.com/products/wireless-rf/lora-gateways/sx1257   
[27] Online. 2020. Semtech SX1276. https://www.semtech.com/products/wireless-rf/lora-transceivers/SX1276   
[28] Online. 2020. SigFox. http://makers.sigfox.com/   
[29] Online. 2020. Sinc Function. https://en.wikipedia.org/wiki/Sinc\_function   
[30] Online. 2020. STM32L083RZ. https://www.alldatasheet.net/datasheet-pdf/pdf/880744/STMICROELECTRONICS/STM32L083RZ.html   
[31] Online. 2020. USRP. https://www.ettus.com   
[32] Meyendorf Orlik and Morgner Morgenstern. 2001. Condition Monitoring and Diagnostic Engineering Management. ELSEVIER.   
[33] Jiajue Ou, Mo Li, and Yuanqing Zheng. 2017. Come and be served: Parallel decoding for COTS RFID tags. IEEE/ACM Transactions on Networking 25, 3 (2017), 1569–1581.   
[34] Aaron N. Parks, Angli Liu, Shyamnath Gollakota, and Joshua R. Smith. 2014. TurboCharging ambient backscatter communication. In Proceedings of ACM SIGCOMM, Chicago, USA, August 17-22, 2014.   
[35] Yao Peng, Longfei Shangguan, Yue Hu, Yujie Qian, Xianshang Lin, Xiaojiang Chen, Dingyi Fang, and Kyle Jamieson. 2018. PLoRa: A passive long-range data network from ambient LoRa transmissions. In Proceedings of ACM SIGCOMM, Budapest, Hungary, August 20-25, 2018.   
[36] Carlos Perez-Penichet, Frederik Hermans, Ambuj Varshney, and Thiemo Voigt. 2016. Augmenting IoT networks with backscatter-enabled passive sensor tags. In Proceedings of ACM HotWireless, New York, USA, October, 03, 2016.   
[37] Joshua R. Smith, Alanson P. Sample, Pauline S. Powledge, Sumit Roy, and Alexander V. Mamishev. 2006. A Wirelessly-Powered Platform for Sensing and Computation. In Proceedings of ACM UbiComp, Orange County, California, September 17-21, 2006.   
[38] Sanjib Sur, Ioannis Pefkianakis, Xinyu Zhang, and Kyu-Han Kim. 2020. Practical MU-MIMO user selection on 802.11ac commodity networks. In Proceedings of ACM MobiSys, Online, June 16-19, 2020.   
[39] Vamsi Talla, Mehrdad Hessar, Bryce Kellogg, Ali Najafi, Joshua R. Smith, and Shyamnath Gollakota. 2017. LoRa backscatter: Enabling the vision of ubiquitous connectivity. In Proceedings of ACM UbiComp, Maui, HI, USA, September 11-15, 2017.   
[40] David Tse and Pramod Viswanath. 2005. Fundamentals of wireless communication. Cambridge university press.   
[41] Ambuj Varshney, Oliver Harms, Carlos Pérez-Penichet, Christian Rohner, and Thiemo Voigt Frederik Hermans. 2017. LoRea: A backscatter architecture that achieves a long communication range. In Proceedings of ACM SenSys, Delft, Netherlands, November 06-08, 2017.   
[42] Anran Wang, Vikram Iyer, Vamsi Talla, Joshua R. Smith, and Shyamnath Gollakota. 2017. FM backscatter: Enabling connected cities and smart fabrics. In Proceedings of USENIX NSDI, Boston, MA, USA, March 27-29, 2017.   
[43] Jue Wang, Haitham Hassanieh, Dina Katabi, and Piotr Indyk. 2012. Efficient and Reliable Low-Power Backscatter Networks. In Proceedings of ACM SIGCOMM, Helsinki, Finland, August 13-17, 2012.   
[44] Xianjin Xia, Yuanqing Zheng, and Tao Gu. 2019. FTrack: Parallel decoding for LoRa transmissions. In Proceedings of ACM SenSys, New York, USA, November 10-13, 2019.   
[45] Lei Yang, Yao Li, Qiongzheng Lin, Huanyu Jia, Xiang Yang Li, and Yunhao Liu. 2017. Tagbeat: Sensing Mechanical Vibration Period With COTS RFID Systems. IEEE/ACM Transactions on Networking 25, 6 (2017), 3823–3835.   
[46] Nicholas Selby Yunfei Ma and Fadel Adib. 2017. Drone Relays for Battery-Free Networks. In Proceedings of ACM SIGCOMM, Los Angeles, CA, USA, August 21-25, 2017.   
[47] Anlan Zhang, Chendong Wang, Xing Liu, Bo Han, and Feng Qian. 2020. Mobile Volumetric Video Streaming Enhanced by Super Resolution. In Proceedings of ACM MobiSys, Online, June 16-19, 2020.   
[48] Pengyu Zhang, Dinesh Bharadia, Kiran Joshi, and Sachin Katti. 2016. Hitch-Hike: Practical backscatter using commodity WiFi. In Proceedings of ACM SenSys, Stanford, CA, USA, November 14-16, 2016.   
[49] Pengyu Zhang, Colleen Josephson, Dinesh Bharadia, and Sachin Katti. 2017. FreeRider: Backscatter communication using commodity radios. In Proceedings of ACM CONEXT, Incheon, Republic of Korea, December 12-15, 2017.   
[50] Pengyu Zhang, Mohammad Rostami, Pan Hu, and Deepak Ganesan. 2016. Enabling Practical Backscatter Communication for On-body Sensors. In Proceedings of ACM SIGCOMM, Salvador, Brazil, August 22-26 2016.   
[51] Renjie Zhaoand Fengyuan Zhu, Yuda Feng, Siyuan Peng, Xiaohua Tian, Hui Yu, and Xinbing Wang. 2019. OFDMA-enabled WiFi backscatter. In Proceedings of ACM MobiCom, Los Cabos, Mexico, October 21-25, 2019.