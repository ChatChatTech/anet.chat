# Efficient Ambient LoRa Backscatter with On-Off Keying Modulation

Xiuzhen Guo, Student Member, IEEE, Longfei Shangguan, Member, IEEE, Yuan He∗, Senior Member, IEEE, Jia Zhang, Student Member, IEEE, Haotian Jiang, Student Member, IEEE, Awais Ahmad Siddiqi, Student Member, IEEE, and Yunhao Liu, Fellow, IEEE/ACM

Abstract—Backscatter communication holds potential for ubiquitous and low-cost connectivity among low-power IoT devices. To avoid interference between the carrier signal and the backscatter signal, recent works propose a frequency-shifting technique to separate these two signals in the frequency domain. Such proposals, however, have to occupy the precious wireless spectrum that is already overcrowded, and increase the power, cost, and complexity of the backscatter tag. In this paper, we revisit the classic ON-OFF Keying (OOK) modulation and propose Aloba, a backscatter system that takes the ambient LoRa transmissions as the excitation and piggybacks the in-band OOK modulated signals over the LoRa transmissions. Our design enables the backsactter signal to work in the same frequency band of the carrier signal, meanwhile achieving flexible data rate at different transmission range. The key contributions of Aloba include:

i) the design of a low-power backscatter tag that can pick up the ambient LoRa signals from other signals; ii) a novel decoding algorithm to demodulate both the carrier signal and the backscatter signal from their superposition. We further adopt link coding mechanism and interleave operation to enhance the reliability of backscatter signal decoding. We implement Aloba and conduct head-to-head comparison with the state-ofthe-art LoRa backscatter system PLoRa in various settings. The experiment results show Aloba can achieve 39.5–199.4 Kbps data rate at various distances, 10.4–52.4× higher than PLoRa.

Index Terms—Wireless Networks, Backscatter Communication, LoRa

# I. INTRODUCTION

The fourth industry revolution (a.k.a. industrial 4.0) aims to transform traditional manufactory and industrial practices with advanced automation, artificial intelligence, and the internet of things technology. The key to the success of industrial 4.0 is the underlying machine to machine (M2M) communication technology that provides ubiquitous and reliable wireless connectivity anywhere, at any time [1], [2], [3], [4], [5], [6]. However, industrial applications have diverse requirements on data exchanging and thus demand different M2M communication technologies. For example, video surveillance on industrial practices requires high-throughput (tens of Gbps) M2M links to ensure reduced communication latency [7]. Keeping track

Xiuzhen Guo, Yuan He, Jiang Zhang, Haotian Jiang, Awais Ahmad Siddiqi and Yunhao Liu are with the School of Software and BNRist, Tsinghua University, P.R. China. Longfei Shangguan is with University of Pittsburgh and Microsoft.

E-mail: guoxiuzhen94@gmail.com, longfei.shangguan@microsoft.com, heyuan@mail.tsinghua.edu.cn, {j-zhang19, jht19}@mails.tsinghua.edu.cn, xidq19@mails.tsinghua.edu.cn, yunhaoliu@gmail.com

∗Yuan He is the corresponding author.

![](images/e73b8deb05154f3148bae1391e51702d71188b7998898cafbb523cbc07f86316.jpg)



Fig. 1. An illustration of Aloba deployment in the factory. Aloba tag takes the ambient LoRa signals as the excitation and transmits the machine status data (e.g., vibration) back to the gateway hundreds of meters away.

of the status of machines in the factory (e.g., vibration, noise, rotation), on the other hand, demands moderate-throughput (hundreds of Kbps) M2M links for sensing data forwarding [8]. As some of these machines may produce strong noise, flash intense light, and discharge harmful gases (as shown in Figure 1), these data forwarding links should be also lowpower and long-range, allowing sensors to transmit their data back to the gateway hundreds of meters away without extra human intervention or frequent battery replacement.

While the latest 5G new radio [9] and 802.11ax (a.k.a. Wi-Fi 6) [10] technologies have been successfully deployed in factories for low-latency data transmission, these technologies are not suitable for machine monitoring in the complex industrial environment as they are either susceptible to blockage or constrained by short communication range (tens of meters). On the other hand, Low-power wide-area networks (LPWANs) are able to connect machines across long range. However, these technologies consume substantial amount of energy in aroundthe-clock monitoring mode and thus require frequent battery replacement.

Due to its low-power and simplicity, backscatter communication becomes a promising technology to enrich the family of existing M2M links. The state-of-the-art backscatter systems (Figure 2) now can transmit at high throughput [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21] and communicate over long distance [22], [23], [24]. These desirable properties make backsactter communication a good candidate for industrial applications. However, as we carefully examine these innovations, we find these designs (Figure 2)

![](images/98b7fb75592b66822a55516ada2a4dd394dddc7920012400eda853fe5d2f7ac5.jpg)



Fig. 2. Comparison of existing backscatter technologies.

either sacrifice the communication range in order to achieve a higher link throughput, or tradeoff the throughput for a decent communication range. None of them is able to balance the throughput and communication range to satisfy the requirement of the machine status monitoring in industrial practices. For example, the throughput of OFDMA-backscatter [21] can reach up to 5.2 Mbps, it however only supports shortrange communication (up to 10 m). In contrast, PLoRa [24] supports kilometer-scale backscatter communication at the cost of a very low throughput (limited to tens of Kbps). Similarly, LoRa backscatter [23] allows the backscatter tag to communicate with the gateway kilometers away. However, its maximum link throughput is constrained to 27.3 Kbps due to the LoRa PHY-layer regulation. Besides, LoRa backscatter relies on the dedicated excitation source to send a continuous sinusoidal tone as the carrier signal. This operation inevitably adds cost and complicates the installation and maintenance of the system.

LoRa transmits data using chirp-modulated signals that can be decoded at very low signal-to-noise ratio (SNR), thus in principle serving as an excellent excitation signal for longrange backscatter. This observation leads us to propose Aloba, an ambient backscatter design for machine status monitoring in industrial practices. Aloba takes the ambient LoRa signals (e.g., emitted from nearby active LoRa nodes) as the carrier signal, modulating its sensing data on these carrier signals using ON-OFF Keying (OOK) modulation, and then reflects the modulated signal to the receiver (LoRa gateway). Such design owns three desirable properties: i): Flexible link throughput. OOK modulation enables the Aloba tag to adapt its link throughput to the link quality as opposed to the PHY-layer regulation of carrier signals. ii): Long communication range. By taking ambient LoRa signals as the carrier, the Aloba tag could leverage the unique processing gain brought by the chirp signal design to enable backscatter communication at a range of hundreds of meters. iii): Easy to deploy. The Aloba tag modulates its data on the ambient LoRa signals. This can avoid the installation and maintenance of the dedicated excitation sources.

Harvesting these benefits, however, faces fundamental challenges. On one hand, unlike the conventional RFID system where the excitation is a continuous wave (a sinusoidal tone), the excitation signal in our design is an ambient, intermittent LoRa signal which already conveys information and changes over time. The backscatter tag should be able to distinguish the LoRa signal from the others and further synchronize with each LoRa symbol for fine-grained modulation. On the other hand, the backscatter signal is orders of magnitude weaker than the excitation signal. The LoRa receiver will receive the direct excitation signal from the LoRa transmitter and the backscatter signal from the Aloba tag. In other words, the received signal is the superposition of excitation signal and backscatter signal. The receiver should be able to demodulate this weak backscatter signal in the presence of strong interfering excitation signal. Due to the frequency variation, the superposition of an excitation signal and a backscatter signal changes over time, which makes the demodulation even more challenging (§II).

In Aloba we present a novel hardware-software solution to tackle the above challenges. On a high-level the Aloba tag picks up the ambient LoRa signal from the other signals using a low-power LoRa packet detection circuit. It then modulates data on the LoRa payload chirps using OOK. The LoRa receiver leverages our signal processing algorithm to decode both the excitation and the backscatter signals from their superposition. Link coding mechanism and interleave operation are used to enhance the reliability of backscatter signal decoding. Moreover, we discuss the impact of synchronization of carrier signal and backscatter signal on the performance of Aloba and propose moving window-based decoding strategy to tolerant synchronization errors. Aloba makes three key contributions:

• We design a simple yet effective LoRa packet detection circuit that can detect the ambient LoRa signal as low as -60 dBm with 0.3 mW power consumption. This packet detection circuit serves as a plug-in peripheral that can be easily integrated with commercial backscatter tags, e.g., WISP.   
• We comprehensively study the superposition of chirp signals at the LoRa receiver, based on which we propose a novel demodulation algorithm that can detect the finegrained changes on the phase and amplitude of the received signal to demodulate both the carrier signal and the backscatter signal.   
• We implement Aloba on a PCB (printed circuit board) and integrate it with WISP [25] for evaluation. The experimental results demonstrate that Aloba can achieve various data rates (39.5–199.4 Kbps) at various tag-to-receiver distances (50–200 m) in the wild, given the tag-to-source distance of 10 m. Compared with the state-of-the-art system ×PLoRa [24], Aloba achieves 10.4–52.4 higher throughput. We shared our schemetic and source code in http://tns.thss.tsinghua.edu.cn/sun/researches/Backscatter Communication.html for reproducibility.

Compared with the published SenSys version [26], we improve the hardware design of Aloba tag and propose a new low-power packet detection circuit in Section IV. We also discuss the power consumption and management of the modified Aloba tag. We add experiments to analyze the distribution of error bits and explain the error types more clearly in Section V. We further propose the link coding mechanism, interleave operation, and coherent combining at the receivers for decoding reliability enhancement. The evaluation results demonstrate the effectiveness of these methods in Section IX. The demodulation extension to the multi-tag scenario is introduced in Section VI. In Section VII, we discuss the impact of synchronization process on the performance of Aloba and propose the potential solutions. Finally, we discuss the challenges in the real application scenarios of Aloba in Section XI. Specifically, we discuss the impact of LoRa duty cycle and industrial environment (especially the vibration, rotation, and EMI generated by the industrial machines) on Aloba decoding in Section XI-A and Section XI-D. We discuss the feedback channel of Aloba and propose the potential solutions to achieve the tradeoff between data rate and communication range in Section XI-B. We also discuss the SNR requirement of Aloba decoding and propose the potential solutions to extend the communication range in Section XI-C.

![](images/6d2e3e7ba3383d5679e6765d99faba7cef7f84e662b7295f29fb106e025ea95b.jpg)



Fig. 3. LoRa modulation and demodulation. (a): the base-chirp encodes symbol “00”. (b): a cyclic shifted version of the base-chirp encodes symbol $^ { \mathrm { { \tiny ~ \circ } } } \mathrm { { 1 0 ^ { \circ } } } .$ . (c): the multiplication of different chirps and down-chirp yields peaks on different FFT bins.

# II. SELF-INTERFERENCE ON LORA BACKSCATTER

Aloba modulates ambient LoRa signal (the carrier signal) using OOK. In this section, we first introduce the standard LoRa modulation and demodulation process, and then analyze LoRa self-interference.

# A. LoRa Primer

LoRa adopts Chirp Spread Spectrum (CSS) to modulate data. Each LoRa symbol is represented by a chirp where the frequency changes linearly over time, as shown in Figure 3(a)- (b). To demodulate the LoRa symbol, the receiver multiplies an incoming LoRa symbol with a down-chirp and transforms the multiplication from the time domain to the frequency domain, yielding a peak on an FFT bin. The receiver tracks the location of this peak to demodulate the LoRa symbol accordingly. Figure 3(c) illustrates this process.

# B. Modeling the Interference

The frequency of a LoRa chirp can be represented by: $f \left( t \right) = F _ { 0 } + k t ,$ where $F _ { 0 }$ is the initial frequency of this LoRa chirp; k is the frequency changing rate (over time). The phase of this LoRa chirp at a given time t can be calculated by:

$$
\phi (t) = 2 \pi \int_ {0} ^ {t} f (t) d t = 2 \pi (F _ {0} t + \frac {1}{2} k t ^ {2}), t \leq T _ {\text { chirp }} \tag {1}
$$

![](images/6f0cbb5f771cdfc11db5dcd8562cc90e0c68b387f82013b108f8974c6e9d0615.jpg)



Fig. 4. The received signal is the superposition of the carrier signal and backscatter signal (propagation delay of the backscatter signal is 1.8 µs). The received signal experiences periodic amplitude variation due to constructive and destructive interference.   
![](images/6eb0e848b4ead718d3ef541dc17e365b438e07cd73e4dd7f5bae3a160bfcb03b.jpg)



Fig. 5. Frequency-time domain characteristics of chirp signal combination. (a) : the phase offset between the carrier and backscatter signal changes over time. (b): the propagation daley td between these two signals leads to an offset $\Delta f$ on the frequency domain. (c): both carrier signal and backscatter signal drop to the same FFT bin after demodulation due to the small frequency shift.

Phase offset. The backscatter signal and the carrier signal propagate along different paths. The propagation delay due to this path difference d can be represented by $\operatorname { \Delta } t d = { \frac { d } { \operatorname { \Delta } _ { \alpha } ! } }$ , where c is the radio propagation speed. At time t , the phase of the carrier $\mathrm { { \normalfont ~ \AA i g e n } } \mathfrak { a } \mathfrak { h } \mathfrak { a } \mathfrak { h } \mathfrak { a } \mathfrak { t } \mathfrak { h } _ { \Sigma \pi } \mathfrak { h } \mathfrak { a } \mathfrak { c } \backslash _ { \boldsymbol { \ell } } \mathfrak { s } \mathrm { c } \mathrm { a } { t } \mathrm { t } \mathfrak { e r } _ { \mathrm { i } } \mathrm { s } \mathrm { i } \mathfrak { g n } \mathfrak { q } \mathfrak { L } \mathfrak { a } { t } \mathfrak { e } _ { \rangle } \mathcal { \ Y } _ { \mathcal { C } } ( t ) = 2 \pi ( F _ { 0 } t + \frac { 1 } { 2 } \ : k t ^ { 2 } )$ b 0 d 2 d , respectively. Hence the phase difference $\Delta \phi ( t )$ between these two signals can be calculated by:

$$
\Delta \phi (t) = \phi_ {a} (t) - \phi_ {b} (t) = 2 \pi ((F _ {0} + k t) t _ {a} - \frac {1}{2} k t _ {a} ^ {2}) \tag {2}
$$

From the above equation we have the following observations: i): The phase difference $\Delta \phi ( t )$ varies over time, as shown in Figure ${ 5 ( \mathrm { a ) } }$ . Hence the received signal experiences interference that periodically alternates between constructive and destructive states, as shown in Figure 4. ii): The propagation delay changes across tag’s locations, so does the amplitude variation of the received signal. Therefore, we cannot rely on the amplitude variation of the received signal to detect the appearance of the backscatter signal. On the other hand, conventional interference cancellation algorithms, $e . g .$ , passive RFID and Wi-Fi backscatter [27], [28], [29], [15] are not suitable for solving this LoRa self-interference, since the carrier signal here is unknown to the LoRa receiver. Reconstructing the carrier signal in hopes of canceling it out from the received signal is difficult, since the amplitude and frequency of LoRa signals change over time.

Frequency offset. The propagation delay $t _ { d }$ leads to a frequency offset in the frequency domain, as shown in Fig-

TABLE I FREQUENCY OFFSET BETWEEN THE CARRIER SIGNAL AND THE BACKSCATTER SIGNAL UNDER DIFFERENT PARAMETERS 

<table><tr><td>Path Difference</td><td>BW (KHz)</td><td>SF</td><td>Frequency Offset</td><td>FFT Bin</td></tr><tr><td>10 m</td><td>500</td><td>7</td><td>65.104 Hz</td><td>3906.25 Hz</td></tr><tr><td>50 m</td><td>500</td><td>7</td><td>325.52 Hz</td><td>3906.25 Hz</td></tr><tr><td>100 m</td><td>500</td><td>7</td><td>651.04 Hz</td><td>3906.25 Hz</td></tr><tr><td>200 m</td><td>500</td><td>7</td><td>1302.08 Hz</td><td>3906.25 Hz</td></tr><tr><td>400 m</td><td>500</td><td>7</td><td>2604.16 Hz</td><td>3906.25 Hz</td></tr><tr><td>600 m</td><td>500</td><td>7</td><td>3906.25 Hz</td><td>3906.25 Hz</td></tr></table>

ure 5(b). The frequency offset ∆f can be calculated by:

$$
\Delta f = \frac {B W}{T _ {\text { chirp }}} t _ {d} = \frac {B W}{T _ {\text { chirp }}} \frac {d}{c} = \frac {B W ^ {2}}{2 ^ {S F}} \frac {d}{c} \tag {3}
$$

The frequency offset is determined by the LoRa bandwidth BW , the spreading factor SF , and the path difference d.

Whereas, the limited resolution of FFT bin at the LoRa receiver makes it hard to apply the existing LoRa parallel decoding methods for Aloba. Table I lists the maximum frequency offset under different path difference settings. We observe that the receiver is unable to differentiate the backscatter signal and carrier signal in frequency domain, unless the path difference is larger than 600 m. As the tag’s location is usually unknown in many outdoor deployments, we cannot blindly borrow the idea of LoRa parallel decoding [30], [31], [32] to separate the two signals from their superposition in the frequency domain.

# III. DEMODULATION

This section describes the way to decode both the carrier signal and the backscatter signal from their superposition. Due to signal attenuation, insertion loss, and energy transformation loss on the backscatter tag, the backscatter signal is orders of magnitude weaker than the carrier signal. Hence we can first leverage capture effect to demodulate the carrier signal, using the standard LoRa demodulation scheme. Capture effect means that the stronger of two signals at the same channel can be demodulated from the superposition due to the capture effect [33]. Our task is then transformed into decoding the backcsatter signal from the received signal.

Basic idea. The demodulation scheme of Aloba is motivated by the conventional RFID system. RFID system simplifies the backscatter signal decoding by adopting a sinusoidal tone as the carrier signal. In a similar way, if the LoRa receiver can transform the standard LoRa carrier signal into a constant sinusoidal tone, the variation of received signal would be solely determined by the backscatter signal. This implies an opportunity to detect the presence of backscatter signal and then decode it.

# A. Transforming Chirps into a Constant Sinusoidal Tone

Signal Transformation. The standard LoRa demodulation scheme multiplies LoRa chirps with a down-chirp (with the frequency changes from $+ \frac { B W } { 2 } \ \mathrm { t o } \ - \frac { B W } { 2 } )$ , yielding a sinusoidal tone. The frequency of this sinusoidal tone is determined by the initial frequency offset of LoRa chirps. In Aloba, we replace the standard down-chirp with the conjugate of incoming LoRa chirps, as shown in Figure 6(a)-(b). The LoRa chirp and its conjugate chirp are symmetric to each other with respect to the reflection off the X-axis. This operation transforms all incoming LoRa chirps into a sinusoidal tone at the same frequency, as shown in Figure 6(c).

![](images/7e4177fe5722d782a96eae4a5910069472d60cecc5ab0d09b73ce83ca9be4e96.jpg)



![](images/b8f73b8e05a6b0864e529f55c6165c7cb51a57b6cce47b123d49b2582507e0be.jpg)



Fig. 6. Signal transformation. (a): two LoRa chirps with different initial frequencies. (b): conjugate down-chirps of these LoRa chirps. (c): the multiplication of the chirps and their conjugate down-chirps yields sinusoidal tone at the same frequency.

![](images/dceabd70e5f9b201af885722d812d23404b97abe57366b09f682200ccf635eb7.jpg)

![](images/776bd50a647fea0529ec346b7ef90b22b56cc6fe69b87ef756458e40e48d7986.jpg)



![](images/13924cff71d919a953cb04c07b3da1974594d013aa3413c82b7b792b51b6fb05.jpg)



Fig. 7. Superposition of sinusoidal carrier signal and backscatter signal. (a): carrier signal and backscatter signal are not strictly aligned or misaligned. (b): carrier signal and backscatter signal are strictly aligned. (c): carrier signal and backscatter signal are strictly misaligned.

Amplitude variation of the sinusoidal tone. The sinusoidal tone obtained from the signal transformation can be regarded as the superposition of a sinusoidal carrier signal and a backscatter signal. As the backscatter signal is much weaker than the carrier signal, the receiver faces two possible signal combinations. i): When these two signals are either strictly aligned or misaligned (Figure 7(b)-(c)), we expect to see a significant amplitude variation on the received signal, based on which we can detect the presence of the backscatter signal. ii): Most of the time, however, these two signals are neither strictly aligned nor misaligned ((Figure 7(a)). Hence the amplitude of the received signal would not exhibit significant variation in the presence of backscatter signal. As a result, we cannot solely rely on the amplitude variation to detect the backscatter signal in the later case.

Phase variation of the sinusoidal tone. We instead leverage the phase variation of the received signal to detect the presence of the backscatter signal in the later case. When Aloba tag is at the OFF state, the received signal is determined by the carrier signal. When Aloba tag switches to the ON state, the presence of backscatter signal will alter the received signal, which leads to a phase jumping on the sinusoidal tone, as shown in Figure 8(a). This phase jumping caused by ON-OFF switching could serve as a clue to detect the presence of the backscatter signal. However, false alarm remains as both the frequency wrapping ( from $\begin{array} { l l l } { { { \frac { B W } { 2 } } } } & { { \mathrm { t o } } } & { { - { \frac { B W } { 2 } } { \it \Delta \phi } } ) } \end{array}$ within the LoRa chirp and the sinusoidal tone transformation of each LoRa chirp could lead to an abrupt phase jump (denoted as false alarms in Figure 8(a)).

![](images/3dc8af45c1d38b46558fe842b32293c307ae619e99ec79e14166be6d2818e292.jpg)



Fig. 8. Phase variation of the received signal after signal transformation. (a): phase jumping caused by ON-OFF switching of backscatter signal and false alarms. (b): eliminate the false alarm caused by signal transformation at the boundary of each LoRa chirp. (c) eliminate the false alarm caused by frequency wrapping within the LoRa chirp.

Two-step phase alignment. We design a two-step phase alignment algorithm to eliminate false alarms. In the first step, the receiver checks the boundary of each LoRa symbol on the received signal, wrapping the phase of remaining signal samples for a proper amount of degree such that they are all aligned with the phase samples of the LoRa symbol ahead. This process is repeated from the first LoRa symbol to the last one. After this step, all phase jumpings caused by sinusoidal transformation will be removed, as shown in Figure 8(b). In the second step, the receiver locates those phase jumpings caused by frequency wrapping by reconstructing the carrier symbols.1 We can also leverage the phase jitter (false phase jumping) proposed in LiteNap [34] as the physical fingerprints to track the continuity of phases before/after frequency wrapping. The receiver further visits these phase jumping points sequentially and repeats the phase alignment operation in step one. After this process, all phase jumpings caused by frequency wrapping will be eliminated from the transformed sinusoidal tone, leaving us true positives (those caused by the presence of backscatter signal) only, as shown in Figure 8(c).

# B. Signal Reconstruction and Decoding

In practice, phase noise exists due to timing offset and carrier frequency offset [35]. It is thus unreliable to tell the presence of backscatter signal solely based on abrupt phase jumping points. To solve this problem, we design a robust, clustering-based detection algorithm as follows.

Signal reconstruction. The backscatter signal is modulated on the payload part of the carrier signal (will be detailed

1Since the content of carrier signal has already been decoded, the receiver can directly obtain the location of the frequency wrapping point within each LoRa symbol.

![](images/6aa12b06ba22068778daf6943f1b66e436f6332a5c241f31ad532a6377605da9.jpg)



Fig. 9. Reconstructed signal. (a): amplitude variation of the reconstructed signal becomes indistinguishable when carrier signal and backscatter signal are not strictly aligned. (b): the phase of this reconstructed signal shows a distinctive pattern.

![](images/86a2f54f915594fd1221361864e02133da6957ecd64f9949227ccab022b70550.jpg)



(a) Initial phase

![](images/08329f1f1c8374c114379ea6efe5bb609b656023d1ee005f72c717956dca4b47.jpg)



(b) Classification   
Fig. 10. The illustration of backscatter data decoding. (a): phase difference between the transformed sinusoidal tone plotted by blue lines and a reference sinusoidal tone plotted by gray lines. (b): reconstructed signal samples with and without backscatter signals aggregate two clusters, and backscatter preamble provides classification anchor points.

in §IV-B). Once the receiver detects the payload of a LoRa packet, the receiver reconstructs the transformed sinusoidal tone as $\begin{array} { r } { \ \pmb { \mathsf { S } } = \ A _ { i } \Phi _ { i } , } \end{array}$ where $A _ { i }$ is the $i ^ { t h }$ amplitude sample on the transformed sinusoidal tone. $\Phi _ { i }$ is the phase difference between the $i ^ { t h }$ phase sample on this transformed sinusoidal tone and the corresponding phase sample on a reference sinusoidal tone, as shown in Figure 10(a). Figure 9 shows the amplitude and phase of the reconstructed signal. We can see the amplitude variation of this reconstructed signal becomes indistinguishable when these two signals are not strictly aligned, while the phase readings of this reconstructed signal demonstrate a distinctive pattern, which can be leveraged for backscatter signal decoding.

Backscatter signal decoding. We plot all reconstructed signal samples on the constellation diagram (I-Q plane). As shown in Figure 10(b), these symbols are naturally grouped into two clusters: one for the none-existence of backscatter signal, and another for the existence of backscatter signal. We can then leverage the preamble of the backscatter signal (a 16-bit Barker code, detailed in §IV-B) to distinguish these two clusters and decode each trail of backscatter signals accordingly. This clustering-based method leverages all signal samples to detect the presence of backscatter signal, hence it is more robust than the phase jumping based detection method.

![](images/50d137c3be9a671fa95ca48d7a25f079647bacbec9098321cc4c5e4e16caa6a0.jpg)



(a) Two tags

![](images/5e81d38c07ccaca712d8d6ac942263ac8b442047382b2d0c18c658ab0a655a94.jpg)



(b) Three tags

Fig. 11. Classification results on I-Q plane when multiple tags are concurrent transmitted. (a): two tags correspond to four clusters. (b): three tags correspond to eight clusters.   
![](images/6cf5c4ca99218cf5ae8d12601cb432e2afa5bd87fe337888e01549e64fcc63b5.jpg)



(a) LoRa packet structure

![](images/8ec4e88afbd6d3a06bcd7e96b02ee06e3ee1e106c84575738eed634f71f3d42e.jpg)



(b) Packet detection result

Fig. 12. LoRa preamble and the corresponding RSSI profile. The ten consecutive up-chirps on LoRa preamble (top) leads to ten equally-spaced RSS pulses (below).   
![](images/604586889f43ebfafd0f019d99ffd9c22ef2aff0a3732e0aefe72bea83826132.jpg)



Fig. 13. The circuit design of LoRa packet detector.

On a high-level, Aloba shares the similar decoding principle with the standard LoRa decoding algorithm: transforming the frequency-shifting LoRa chirp into a constant sinusoidal tone. However, the conventional LoRa decoding algorithm multiplies the incoming LoRa chirp with a standard downchirp and then tracks the peak on FFT bins to demodulate the LoRa chirps. In contrast, the Aloba receiver replaces this down-chirp with the conjugate of each incoming LoRa chirp. It then tracks the amplitude and phase variation to demodulate the backscatter signals overlaid on the carrier LoRa signals. This allows the Aloba receiver to decode both the carrier signal and backscatter signal on the same frequency band.

# IV. ALOBA TAG DESIGN

# A. Low-power LoRa Packet Detection

![](images/a5216c30de7c8bb8452ea95d93f4b8ad032ae075b18768bf602f303680ea5590.jpg)



Fig. 14. LoRa packet structure and backscatter packet structure.

signal. The standard LoRa packet detection scheme is not suitable for Aloba due to its high power consumption.

In Aloba, we design a simple yet effective packet detection circuit to pick up the LoRa signal from the ambient noise and unconcerned signals. Our design exploits the unique pattern of LoRa symbols in the LoRa preamble: ten consecutive upchirps with zero initial frequency offset. When the incoming signal passes through a low-pass filter (with a cutoff frequency at BW/4), the ten consecutive up-chirps on a LoRa preamble will lead to ten equally spaced RSS (received signal strength) pulses (Figure 12(b)), whereas the noise and other legacy signals will not. Hence Aloba can pick up the LoRa preamble by detecting the appearance of this unique RSS pattern.

Figure 13 shows the circuit design of Aloba packet detection module. First, we adopt a Surface Acoustic Wave (SAW) filter of Qualcomm B3715 [36] to support narrowband filtering and offers reduced size, weight, and cost, compared to the RF filtering technology. More importantly, the SAW filter is a purely passive component with zero power consumption. Second, the filtered signal is down-converted to the baseband through an envelope detector for demodulation. To minimize the power consumption on detection, an intuitive solution is using a low-power voltage comparator to replace ADC. The comparator (NCS2202) [37] quantizes the RSS signal to High ("1") and Low ("0") two logical voltages. We empirically set this RSS threshold to -60 dBm, which yields the best detection accuracy in our experiments. We then leverage the built-in low-power counter in the FPGA to sample these logical voltages. Once the FPGA detect ten equally spaced RSS pulses, it immediately knows the arrival of a LoRa packet and automatically switches to the modulation mode.

Power consumption and management. Both impedance matching, SAW filter and envelope detector are passive components (e.g., inductance, capacitors, and diodes), hence the energy consumption of this packet detection circuit mainly comes from the low-power comparator and FPGA. The total power consumption of the packet detection module is around 34.5 uW, which is much lower than those frequency shifting system (about hundreds of uW) [24], [17].

The energy harvester on Aloba consists of a palm-size photovoltaic panel and a high-efficiency step-up DC/DC converter LTC3105 [4]. We add resistors and capacitance on board to best realize the efficiency of this converter. The power management module provides a constant 3.3V output voltage at a high power transforming efficiency (up to 1 mW output power), which is enough to afford the power consumption of the Aloba tag.

![](images/f520fbdca733f1659adf3f85f3afc8f8343d830673b82d29b73a9ae142e83798.jpg)



(a) Number of consecutive error bits

![](images/c599edc36447d6d519f9220c872366e69f82fd62f916e94560f163d854c88e7d.jpg)



(b) Number of symbols affected by consecutive error bits   
Fig. 15. The distribution of consecutive error bits in a LoRa packet.

# B. Modulation

After detecting the LoRa preamble, Aloba waits for another 2.25 symbol times (sync. symbols) and then modulates data on the payload part of this incoming LoRa packet using OOK: reflecting the signal when transmitting a bit one, and absorbing the signal when transmitting a bit zero. The backscatter packet contains four fields as shown in Figure 14: a 16-bit baker code-· · ·based preamble (010101 010101), a 4-bit modulation rate field, a 8-bit payload length field, and the payload.

# V. RELIBILITY ENHANCEMENT

Due to the randomness, dynamics and burst of the channel, error bits are easy to appear during the transmission process of backscatter signals. According to the number of consecutive error bits in a LoRa packet, we classify the errors into two types: random errors and continuous errors. Random errors mean the error probability of each bit is independent, which are caused by noise or electromagnetic flash. Continuous errors mean there are multiple consecutive error bits which are caused by burst of interference. The error bits may distribute on a single symbol or multiple symbols. We conduct experiments to observe the error distribution of the decoded backscatter signals. Figure 15(a) plots the histogram of the number of consecutive error bits. We find that 95.13% of the number of consecutive error bits are less than 12. As shown in Figure 15(b), 58.4% of the error bits are distributed in a single symbol. In this section ,we propose link coding mechanism, interleave operation, and coherent combining at the receivers to enhance the reliability of backscatter signal decoding.

# A. Link Coding

Hamming Code (7, 4) is used to protect the backscatter signal. As shown in Fig. 16, we add 3-bit check data to every 4-bit data and these 3-bit check data can correct 1-bit error data. The Hamming Code (7, 4) has the capability of error detection rate of ${ \underline { { 1 } } } ,$ which is sufficient to handle the errors of the backscatter signal.

# B. Interleave

Interleave [38] operation is robust to handle burst interference since that a codeword is spread out to multiple symbols. Corrupting a single symbol would not result in a loss of the whole codeword. The process of reliability enhancement of backscatter data is shown in Fig. 17. First, the backscatter data is divided into groups. Each group of 4-bit data is encoded by Hamming Code (7, 4) and is transformed to a 7-bit codeword. An interleaver is between the Hamming encoder and the OOK modulator, which writes in columns and reads out in rows. Because of this, bits in a codeword are spread across multiple symbols. At the receiver, the deinterleaver is the opposite, which writes in rows and reads out in columns. Although a whole symbol out of seven symbols is corrupted after channel transmission, codewords are reconstructed by these symbols and there is only a single corrupted bit per codeword. (7, 4) Hamming decoder can correct a single error bit and obtain the backscatter data.

![](images/6a230303d2e2a1170f401ff012a5bacd5660c9608b4b637f9caed61eb6a9c08c.jpg)



Fig. 16. Illustration of hamming coding.

![](images/abd784dfbed5d6783c5c91e977baa66768090ce47b6a247e4bcc3a5ca4d33d56.jpg)



![](images/6f4694f9231f89ce5ef63836291b281b44a1e06316e30c98e394cb08e3c5c3c6.jpg)



(F(c)   
(G(d)   
Fig. 17. The process of reliability enhancement of backscatter data decoding. (a): The backscatter data is divided into 4-bit groups. (b): Each group of 4- bit data is encoded by Hamming Code (7, 4) and is transformed to a 7-bit codeword. (c): After the interleave operation, bits in a codeword are spread across multiple symbols. (d): A whole symbol (consecutive four bits) out of seven symbols is corrupted after channel transmission. (e): After deinterleave operation, codewords are reconstructed and there is only a single corrupted bit per codeword. (f): (7, 4) Hamming decoder can correct a single error bit and obtain the backscatter data.

# C. Coherent Combining

The method of coherent combining [39] at the receivers can also be used to correct the error bits of Aloba. Due to the geometric difference, the bit errors are often disjoint across different receivers. In this way, we can combine the received signals at multiple receivers to recover the Aloba packet. Moreover, the decoding complexity of this method is afforded by the LoRa receivers and it doesn’t bring additional overhead to the Aloba tag.

# VI. ALOBA MAC LAYER

We sketch the MAC layer design in this section. We allocate an assigned channel among multiple Aloba tags. Each tag randomly picks up a time slot to transmit. Upon detecting the carrier signals, these Aloba tags achieve time synchronization and reflect backscatter signals. When there are multiple active LoRa nodes in the LoRaWAN, these LoRa nodes also abide by the time-domain ALOHA protocol. In this way, LoRa nodes and Aloba tags form a hybrid LoRaWAN network.

ALOHA protocol can reduce the collision probability. However, it does not guarantee the collision-free transmission. Collision happens when multiple Aloba tags select the same slot. Each tag makes its own choice independent with the other tags. If we have N tags and there are K time slots, the probability that R tags will be transmitted in one time slot is $P = { \cal N } _ { \not R } ^ { \backslash } ( { \bot } _ { 1 } ) _ { \cal K } ^ { R } ( 1 \mathrm { ~ -- ~ } 1 ) _ { \cal K } ^ { \cal N - R }$ [40]. For instance, suppose 100 tags and 128 time slots, the probability that 5there are tags will be transmitted in one time slot is 0.1%.

The demodulation extension to the Multi-tag Scenario. Our demodulation scheme can be easily extended to the multitag scenario. Suppose there are M $( M \ > \ 1 )$ Aloba tags. The received signal would be the superposition of multiple backscatter signals and the carrier signal. Following the signal transformation introduced in §III-A, the receiver first transforms this received signals into a sinusoidal tone. It then follows the signal reconstruction introduced in §III-B to reconstruct the received signal. One may expect to see 2M clusters on the constellation diagram. Figure 11(a) and Figure 11(b) show the constellation diagram of two tags’ and three tags’ replies, respectively. With those symbol clusters, we can then apply the state-of-the-art parallel decoding algorithms such as [41], [42], [43], [44] to decode the backscatter signals.

# VII. TIME SYNCHRONIZATION

There are two critical time synchronization processes that affect the system performance. We analyze the impact of synchronization accuracy in this section.

# A. The Synchronization Error on LoRa Packet Detection at the Aloba Tag

The first synchronization error happens at the Aloba tag where the tag detects the boundary of LoRa chirp and synchronizes with the payload part for modulation (backscatter). The error in synchronization will introduce a time offset ∆t between the carrier signal (start at $t _ { 1 } )$ and the backscatter signal (start at t2), as shown in Fig. 18(a). Once the LoRa receiver detects the LoRa payload at t1, the LoRa receiver set a decoding window to decode the backscatter signal. The length of decoding window is equal to the duration of one Aloba bit. During the Aloba decoding process, the signal samples with Aloba bit one and zero will aggregate into two clusters. The mismatch between the decoding window and the backscatter signal will affect the aggregation of samples within a decoding window and will further result in Aloba decoding errors.

A moving window-based decoding strategy can be used to tolerant the above synchronization error. As shown in Fig. 19, we select a random position as the start of the moving window and the window length is equal to the duration of one Aloba bit. As the window moves, different decoding results can be obtained. The moving position which satisfies the requirement of 16-bit baker code-based preamble of Aloba and achieves the maximum distance between two clusters with and without backscatter signals is the corresponding position of the Aloba decoding window.

![](images/081e35c919ea20c1a1f3fa8e09704a1bccfeecd61835315916ca4bcd96e2131b.jpg)  
Fig. 18. Synchronization errors. (a): The synchronization error on LoRa packet detection at the Aloba tag. (b): The chirp edge detection error at the LoRa receiver.

![](images/b5b005d9bfc5dc812f5402973b90c2fd0678191b99a3f4cc66b583e0e49efe4c.jpg)



Fig. 19. The moving window-based decoding strategy. The moving position which satisfies the requirement of 16-bit baker code-based preamble of Aloba and achieves the maximum distance between two clusters with and without backscatter signals is the corresponding position of the Aloba decoding window.

# B. The Chirp Edge Detection Error at the LoRa Receiver

The second one synchronization error happens at the Aloba receiver where the receiver detects and synchronizes with the boundary of the LoRa chirp for chirp transformation. As shown in Fig. 18(b), the start of LoRa chirp at the LoRa transmitter is $t _ { 1 } ,$ however, the detected boundary of the LoRa chirp at the LoRa receiver is $t _ { 2 } .$ . When the time offset caused by the above chirp edge detection error is smaller than the time range bin of LoRa chirp (the minimum time offset between two LoRa chirps, which is equal $^ { \mathrm { t o } } _ { \mathcal { B } } ^ { \mathrm { ~ 1 ~ } } )$ , the chirp transformation can be achieved successfully and the impact on the Aloba decoding can be neglected. Otherwise, the LoRa chirps will be decoded incorrectly and the LoRa packet will be discarded at the LoRa receiver, not to mention the piggybacked backscatter data.

# VIII. IMPLEMENTATION

Tag hardware. The packet detection module is prototyped on a single-layer PCB using commercial off-the-shelf circuit components as shown in Figure 20(c). The packet detection module uses one omni-directional antenna with 3 dBi gain [45] and a DE0-Nano-SoC FPGA [46]. The incident signal passes through a passive SAW chip B39871B3715U410 [36] and then can be down-converted to baseband through the envelope detector. We optimize the impedance matching coefficient to provide the maximum power transfer from the antenna to the envelope detection. Finally, a low-power voltage comparator NCS2202 [37] is leveraged to quantize the output signal from the envelope detector. The packet detection module is wired to the WISP 5.0 [25] for evaluation.

![](images/30ebd91f40e77c083d2724e65cd31baeaeba191db437daad4f153ba92002b2e1.jpg)



(a)

![](images/120bee77a6a4530cbec24e5bc1de947fd86c1184faaacc42b5e50723341cb92e.jpg)



![](images/2499b2f13eba8f33f72ff066f792aa64aaab62492f6f8273c5654c40fa84dd2d.jpg)

![](images/cbae4275faabe6374da649d8d9f75b8bc803541cc17fd9a5409ab006848b818a.jpg)  
) Lab (i) Lab   
) Hallway (ii) Hallway   
c) Warehou(iii) Warehouse   
d) Parking lot (e) Road (f) Squar(iv) Parking lot (v) Road (vi) Square   
(b)

![](images/49d9cec35d6288940acca99bcfe115ba49c328a245a38802005b5ac7d5bd98f5.jpg)



(c)   
Fig. 20. The implementation of Aloba. (a): The floor plans of indoor experiment field. (b): Indoor and outdoor experiment field. (c): The packet detection module of Aloba tag.

Transmitter and receiver. We use a commercial LoRa node (a STM32L083RZ board [47] carrying a Semtech SX1276 [48] chip) with one 3 dBi gain omni-directional antenna [45] as the transmitter, an USRP N210 [49] equipped with the same type of antenna as the receiver. We can also choose other types of software defined radio (SDR) devices as long as they can capture the RF signals of the 900 MHz frequency band. We set the sampling rate at 10 MHz to get more sampling points and improve the robustness of the decoding algorithm based on clustering. The sampling rate only needs to meet the requirement of Nyquist Theorem, which is greater than or equal to twice the bandwidth of LoRa signal. The LoRa receiver runs the standard LoRa preamble detection algorithm [50] to detect LoRa transmissions and further locates each LoRa symbol on the payload. The receiver then runs Aloba decoding algorithm to decode both the backscatter signal and the ambient LoRa signal.

Extension to commercial LoRa gateways. While the current Aloba decoding algorithm is implemented on USRP, it is worth noting that this algorithm can be easily implemented on a commercial LoRa gateway, since this algorithm requires only the raw signal samples which are accessible on most LoRa RF-front, e.g., Semtech SX1257 front-end [51]. We leave the algorithm implementation on commercial LoRa gateways as our future work.

# IX. EVALUATION

In this section, we first conduct head-to-head comparison with PLoRa [24], the state-of-the-art ambient LoRa backscatter system. We then conduct micro-benchmarks to study the performance of Aloba in various settings, including different LoRa bandwidth, tag-to-source distances, modulation rate, environment, and channel conditions.

# A. Experimental Setup

The LoRa transmitter and the receiver both work on channel one (902.5 MHz). The payload of each LoRa packet consists of 20 symbols. The default spreading factor (SF), coding rate, and bandwidth (BW) of the LoRa signal are 7, 1, and 125 KHz, respectively. The transmission power of the LoRa sender is 20 dBm. We evaluate Aloba both indoors (classroom, hallway and warehouse as shown in Figure 20(a).) and outdoors (open road, square and parking lot, as shown in Figure 20(b)).

We take throughput and maximum backscatter range as the key metric to evaluate Aloba’s performance. Throughput measures the amount of backscatterred data correctly decoded within one second at the LoRa receiver. Maximum backscatter range refers to the maximum distance between the Aloba tag and the LoRa receiver when the bit error rate (BER) of the backscatter data is lower than 0.001. We send 1,000 LoRa packets in each experiment, and then repeat the experiment 100 times. Finally we report the averaged result to ensure the statistical validity.

# B. Head-to-head Comparison with PLoRa: Link Throughput

We compare Aloba with PLoRa [24] in various settings. PLoRa encodes one bit per LoRa symbol. The theoretical link 2SF2SF ·throughput of LoRa carrier and PLoRa are  SF and BW , respectively. The theoretical link throughput of Aloba 2S

In these experiments, we place the receiver 50 m, 100 m, 150 m, 200 m, 250 m, and 300 m away from the tag. Within each distance setting, we further vary the distance between the source and the backscatter tag to measure the throughput of PLoRa and Aloba. We tune the spreading factor and bandwidth of the carrier signal to ensure the fair comparison with PLoRa. Figure 21 shows the result. We have two observations from these experimental results.

First, we observe the link throughput of Aloba is orders of magnitude higher than that of PLoRa when the LoRa receiver is within 200 m of the source (Figure 21(a)-(d)). Specifically, when the tag is collocated with the source (with an 10 cm ×spacing), the link throughput of Aloba is 10.4 –52.4 higher than that of PLoRa in different source-to-receiver distance settings. This is expected since the OOK design enables Aloba to tune up its throughput to best utilize the better link quality in short tag-to-source distance settings. This flexible modulation ×design enables Aloba to achieve even 1.5 –7.3 higher throughput than that of the LoRa carrier. In contrast, PLoRa adopts a fixed modulation rate and thus achieves consistently low throughput in all different distance settings.

![](images/a0495df93f8a7ab2fc8014cd0143b146658e0de9a97c8ac73d6e956c3f81fd6e.jpg)



(a) tag-to-receiver distance=50m

![](images/8f4d4f4a031009e88eaba94de7242112c478cb9d57d85397991b20872281b646.jpg)



(b) tag-to-receiver distance=100m

![](images/295cca8ca7a4e214d388f5b79a983c0f1579eac45b98079910c962e2b386dc38.jpg)



(c) tag-to-receiver distance=150m

![](images/da4a5b59b994dc3e7ab86bb1f73b2ccee7c5548fd375f972be3e88b5baa02f7d.jpg)



(d) tag-to-receiver distance=200m

![](images/fd7f1b27a7047fed36863e02f8ada1fa42c24b733d2b4dcec6372e355a012871.jpg)



(e) tag-to-receiver distance=250m

![](images/079f5a9e07ed2d281d5b7885720e03065a7350eb3df8757bcc246f3f88b7a880.jpg)



(f) tag-to-receiver distance=300m   
Fig. 21. Link throughput of Aloba and PLoRa in different tag-to-receiver distance settings.

Second, the link throughput achieved by Aloba and PLoRa both decreases with increasing tag-to-source distance, primarily due to the decreasing SNR of the backscattered signal (Figure 21). To expand the backscatter range, similar to the existing backscatter systems [24], Aloba has to sacrifice the throughput to ensure a longer backscatter range (Figure 21(e)). Aloba essentially relies on energy to decode backscatter signals, thus the performance gain of Aloba over PloRa is achieved mainly within short and medium communication ≤range ( 250 m shown in Figure 21(f)), since that the signal attenuation, insertion loss, and energy transformation loss on the backscatter tag result in that the backscatter signal is orders of magnitude weaker than the carrier signal. For example, Aloba achieves the throughput of 0.93 Kbps when we place the tag 1 m away from the LoRa sender and the LoRa receiver is within 250 m of the source. Other evaluation experiments about head-to-head comparison with PLoRa in different SF and BW settings can be found in SenSys version [26].

# C. Aloba Performance under Different Interference Environments

We conduct experiments to evaluate the performance of Aloba under different interference environments. In these experiments, we place the LoRa receiver 50 m away from the LoRa sender and the distance from the tag to the LoRa sender is 10 cm. An USRP N210 platform with the distance of 50 m from the LoRa receiver as the jamming generator transmits interference signals on the 902.5 MHz with the power of 20 dBm. We set the transmission interval of interference signals at 5 ms and the duration of each interference signal varies from 100 µs to 1 ms. Given the backscatter date rate of 25 Kbps, the number of consecutive error bits varies from 4 to 40 when the duration of interference varies from 100 µs to 1 ms. Our proposed interleave operation can theoretically disperse and correct 20 consecutive error bits. We further evaluate the performance gain brought by the link coding and interleave operation. The experimental result is shown in Fig. 22(a).

First, we observe the BER of backscatter signal increases with the increasing of the duration of interference signal. The longer the duration of the interference signal is, the more backscatter signal are affected. For example, the BER is up to 0.12 when the duration of interference signal is 400 us.

Second, Hamming coding (7,4) can effectively reduce the BER when there is transient jamming or interference. Hamming Coding (7,4) can correct one error bit for every sevenbit codeword. We find that the BER is reduced to 0.011 with the Hamming Coding (7,4) when the duration of interference signal is 100 us. Whereas, if more than 1 bit of data is wrong, the corrupted codeword can’t be recovered solely by Hamming Coding.

Third, we adopt interleave operation to handle burst interference and sparse the continuous bit errors to recover more corrupted codewords. The BER is reduced to 0.001 with the interleave operation when the duration of interference signal is 400 us. Due to the interleave depth is limited to 20, the performance gain of interleave reduces when the duration ×of interference signal exceeds 500 µs (20 1 ms). We can increase the check bit of Hamming Coding and interleave depth to further improve the anti-interference ability and enhance reliability.

Finally, we place another receiver 50 m away from the interference jammer and leverage the method of coherent combining at the receivers to correct the error bits. When the duration of interference signal varies from 600 us to 1000 us, the BER can be significant reduced from 0.48% to 2.76%.

![](images/4a2d4de52bc9b18180f043b26e99ff1a7ec6c011fd2ea3f19e0813b04c7a69f8.jpg)



(a)

![](images/e25daaa75b6901ad91c0e5963c693f5316df9965b69278fd3cc2e780ef6b1551.jpg)



(b)

![](images/590e6ba136787b9b7736ad3509aadc8e1f4466996176302d0c168d457dc89c29.jpg)



(c)   
Fig. 22. Performance of Aloba in different settings. (a): Under different interference environments. (b): With time offset between the LoRa signal and the backscatter signal. (c): With the time offset of LoRa packet detection at the LoRa receiver.

# D. The Impact of Time Synchronization

As analyzed in §VII, there are two types of synchronization errors. We conduct experiments to evaluate the impact of time synchronization on the performance of Aloba decoding. In these experiments, we place the LoRa receiver 50 m away from the LoRa sender and the distance from the tag to the LoRa sender is 10 cm. We set the switch rate of the Aloba tag is 40 KHz and the duration of one-bit Aloba backscatter data $\mathrm { i s } \frac { 1 } { 4 }$ ms. Aloba tag modulates data on the payload of LoRa signals after a waiting time, which will result in a corresponding time offset between the LoRa signal and the backscatter signal as shown in Fig. 18(a). The waiting time of Aloba tag varies from $\boldsymbol { 0 } \ \mathrm { t o } \frac { \boldsymbol { 1 } } { 4 }$ ms. The evaluation result is shown in Fig. 22(b).

First, the BER of Aloba data increases when the time offset varies from 0 to $\frac { 1 } { 8 }$ ms, half of the duration of one-bit tag data. The larger the time offset is, the more scattered the sampling points in a time window are, and the more difficult it is for these sampling points to be grouped into a cluster. Second, when the time offset is larger than 1 ms, the decoding result will be shifted and the BER decreases. For example, the 16-bit Barker code-based preamble of one Aloba packet "010101...010101" will be shifted as "101010...101010", and the Aloba data can also be decoded. We further adopt the moving window-based decoding strategy to find the appropriate position of the decoding window. We observe that the BER of Aloba data is lower than 0.005 no matter what the time offset is.

Due to that it is difficult to control the time delay LoRa packet detection at the LoRa receiver shown in Fig. 18(b), we conduct an emulation experiment to evaluate the impact of chirp edge detection errors on the Aloba decoding. We suppose the time offset between the LoRa chirp at the LoRa sender and the detected LoRa chirp at the LoRa receiver varies from to 0 to 1 ms (the time offset between two LoRa chirps). In these cases, we control the backscatter signal and the LoRa signal are aligned without time offset. The evaluation result is shown in Fig. 22(c). We find that the BER increases with the time offset of chirp edge detection. The BER is 0.042 when the time offset of chirp edge detection $\mathrm { i s } _ { + 2 } ^ { ~ 1 }$ ms, which indicates that the impact of chirp edge detection errors on the Aloba decoding is limited and controllable.

# X. RELATED WORK

In recent years, RF signals, such as TV, WiFi, FM, BLE, LoRa signals, have been widely exploited for backscatter communication. Ambient backscatter [11] reflects broadcast TV or cellular transmissions to achieve device-to-device communication. WiFi backscatter [12] reuses the WiFi signals to convey information by modulating the CSI and RSSI measurements. The data rate of ambient backscatter and WiFi backscatter is limited to 1 Kbps.

In order to improve the data rate, Turbo charging [13] uses the multi-antenna cancellation design with the coding mechanism to achieve the data rate of 1 Mbps. BackFi [15] modulates information by changing the phase of the received WiFi signals, which improves the communication rate to 5 Mbps. Passive WiFi [12] enables a passive tag to generate 802.11b transmissions by leveraging a dedicated excitation device. HitchHike [17] allows a backscatter tag to embed its information on standard 802.11b packets, by translating the original transmitted 802.11b codeword to another valid codeword. FreeRider [18] extends the technique of codeword translation to other radios, such as 802.11g/n, Bluetooth, and ZigBee. OFDMA-WiFi [21] enables OFDMA in WiFi backscatter for capacity and concurrency enhancement. But the farthest communication range is only tens of meters.

To further improve the communication range, researchers focus on Low-Power Wide-Area Network (LPWAN) technologies. Among the LPWAN technologies [52], [53], LoRa [50] is resilient to interference due to its high receiving sensitivity, making it a natural choice for backscatter. LoRa backscatter [23] synthesizes legitimate LoRa packets to extend the communication to 2 km. However, it requires a dedicated device to generate the excitation signal. PLoRa [24] is the most relevant work with Aloba, which takes ambient LoRa transmissions as the excitation signals and modulates the original LoRa chirp signal into a new standard LoRa chirp signal at another frequency band. Whereas, PLoRa is not spectrum efficient and inevitably consumes the already crowded wireless spectrum.

Compared to the existing works, Aloba adopts the modulation of ON-OFF Keying (OOK) and the data rate can be easily adjusted by tuning the frequency of this RF switch. By taking the ambient LoRa signals as the excitation, the backscatter tag could leverage the unique processing gain brought by the chirp signal design to enable long-range backscatter communication. In this way, Aloba supports flexible data rate at different transmission range. Moreover, Aloba achieves high spectrum efficiency.

# XI. DISCUSSION

# A. The Impact of LoRa Duty Cycle on Aloba

We propose Aloba to enhance rather than to replace the LoRa communication. Indeed, the Aloba tag relies on the LoRa signals as the carrier signals to transmit data. Multiple Aloba tags join a LoRaWAN to form a hybrid LoRaWAN network. Aloba provides battery-free but efficient communication, which is especially suitable for periodical sensing applications, where the sensor nodes typically work in lowduty cycle mode but desire relatively high data-rate communication. Moreover, with increasingly deployed LoRa nodes in the environment [54], one may expect to see increasing space to deploy Aloba tags and utilize LoRa signals therein for backscatter.

# B. The Adjustment between Data Rate and Communication Range

There are three potential solutions to achieve the tradeoff between data rate and communication range. First, the basic idea is to flexible set the data rate offline according to the geographic location during the deployment of the Aloba tag. Second, the packet detection module of the Aloba tag provides the RSSI information of the LoRa carrier signal, which can be used as an indicator to infer the communication range between the Aloba tag and the LoRa receiver, according to the signal attenuation model [22]. According to the inferred communication range, the Aloba tag can set the corresponding data rate. Third, we may replace the existing packet detection module with Saiyan [55], which allows the Aloba tag to demodulate the incident command/feedback LoRa signals. As a low-power component, Saiyan can serve as a plug-in module to directly benefit Aloba without much engineering efforts. On the software side, we only add a decision layer to configure the data rate based on the decoded messages.

# C. The SNR Requirement of Aloba Decoding

Aloba takes the ambient LoRa transmissions as the excitation and piggybacks the in-band OOK modulated signals over the LoRa transmissions. There is a SNR gap in between at which LoRa symbol is decoded but the Aloba symbol cannot be decoded. Specifically, the chirp-modulated LoRa signals can be decoded at -30 dB SNR, while the OOK-modulated Aloba signals can be decoded at 0 dB SNR. The SNR difference results in that the Aloba tag cannot achieve similar communication range as the active LoRa nodes. There are multiple ways to increase the backscatter range. For example, leveraging beamforming techniques or negative impedance components like tunnel diode and we leave it as our future work.

# D. The Impact of Vibration, Rotation, and EMI

There are interference of vibration, rotation, EMI introduced by the industrial environment. First, the influence of periodic vibration and rotation of industrial machine on carrier signal is limited and can be ignored. On the one hand, periodic vibration and rotation produce mechanical wave, which is different from electromagnetic wave of carrier signal. Hence, the periodic vibration and rotation don’t introduce a period change on the carrier signal. On the other hand, when the Aloba tag attached to an industrial machine, the vibration and rotation of the machine may slightly change the path difference between the backscatter signal of Aloba and the carrier signal of LoRa. Whereas, the influence of the fluctuation of path difference is so small that it is generally negligible. For example, the typical values of vibration period and amplitude of an industrial machine are 1 KHz and 200 µm, respectively [8]. That is to say, the fluctuation of path difference is approximately 200 µm. According to the equation of $\varphi ~ = ~ { \frac { d } { \lambda } } 2 \pi$ (where φ is phase, d is path difference, λ is wave length), the phase change caused by the fluctuation of path difference fluctuation is only $3 . 7 6 \times 1 0 ^ { - 5 }$ , which can be ignored. Second, other electromagnetic interference (EMI) may cause the flicker or disturbance on the carrier signals. We enhance the anti-interference ability of Aloba by leveraging channel coding mechanism, such as Hamming Coding and Interleave Operation.

# XII. CONCLUSION

Aloba is an ambient LoRa backscatter design using ON-OFF Keying that provides flexible data rate and transmission range for different IoT applications and deployments. By allowing the coexistence of the backscatter signal and the carrier signal in the same frequency band, Aloba achieves a higher spectrum efficiency. Our design contributions are a lowpower backscatter design that can pick up the ambient LoRa transmissions from other interfering signals and a decoding algorithm running on the LoRa receiver that can decode both the backscatter signal and the LoRa excitation signal from their superposition. We propose link coding mechanism and interleave operation to enhance the decoding reliability. We also discuss the impact of synchronization on the Aloba performance and leverage moving window-based decoding strategy to tolerant synchronization errors. Evaluation results demonstrate that Aloba can achieve various data rates (39.5– 199.4 Kbps) at various distances (50–200 m) in the wild. Compared with the state-of-the-art system PLoRa [24], Aloba is 10.4–52.4× better in terms of throughput.

# ACKNOWLEDGMENT

This work is supported in part by National Key R&D Program of China No. 2017YFB1003000, National Science Fund of China under grant No. 61772306, the Smart Xingfu Lindai Project, and the R&D Project of Key Core Technology and Generic Technology in Shanxi Province (2020XXX007).

# REFERENCES

[1] Z. Luo, Q. Zhang, Y. Ma, M. Singh, and F. Adib, “3D backscatter localization for fine-grained robotics,” in Proceedings of USENIX NSDI, Boston, MA, February 26-28, 2019.   
[2] V. Iyer, R. Nandakumar, A. Wang, S. B. Fuller, and S. Gollakota, “Living IoT: A flying wireless platform on live insects,” in Proceedings of ACM MobiCom, Los Cabos, Mexico, October 21-25, 2019.   
[3] Z. Luo, W. Wang, J. Qu, T. Jiang, and Q. Zheng, “Improving IoT security with backscatter assistance,” in Proceedings of ACM SenSys, Shenzhen, China, November 4-7, 2018.   
[4] C. Gao, Y. Li, and X. Zhang, “LiveTag: Sensing human-object interaction through passive chipless WiFi tags,” in Proceedings of USENIX NSDI, Renton, WA, USA, April 9-11, 2018.   
[5] K. Fukuda, J. Heidemann, A. Qadeer, K. Fukuda, J. Heidemann, and A. Qadeer, “Detecting malicious activity with DNS backscatter over time,” IEEE/ACM Transactions on Networking, vol. 25, no. 5, pp. 3203– 3218, 2017.   
[6] L. Yang, Y. Li, Q. Lin, H. Jia, X. Y. Li, and Y. Liu, “Tagbeat: Sensing mechanical vibration period with COTS RFID systems,” IEEE/ACM Transactions on Networking, vol. 25, no. 6, pp. 3823–3835, 2017.   
[7] A. Zhang, C. Wang, X. Liu, B. Han, and F. Qian, “Mobile volumetric video streaming enhanced by super resolution,” in Proceedings of ACM MobiSys, Online, June 16-19, 2020.   
[8] M. Orlik and M. Morgenstern, Condition Monitoring and Diagnostic Engineering Management. ELSEVIER, 2001.   
[9] J. Czentye, J. Dóka, Árpád Nagy, L. Toka, B. Sonkoly, and R. Szabó, “Controlling drones from 5G networks,” in Proceedings of ACM SIG-COMM, Budapest, Hungary, August 20-25, 2018.   
[10] S. Sur, I. Pefkianakis, X. Zhang, and K.-H. Kim, “Practical MU-MIMO user selection on 802.11ac commodity networks,” in Proceedings of ACM MobiSys, Online, June 16-19, 2020.   
[11] V. Liu, A. Parks, V. Talla, S. Gollakota, D. Wetherall, and J. R. Smith, “Ambient backscatter: Wireless communication out of thin air,” in Proceedings of ACM SIGCOMM, Hong Kong, China, August 12-16, 2013.   
[12] B. Kellogg, A. Parks, S. Gollakota, J. R. Smith, and D. Wetherall, “WiFi backscatter: Internet connectivity for RF-powered devices,” in Proceedings of ACM SIGCOMM, Chicago, USA, August 17-22, 2014.   
[13] A. N. Parks, A. Liu, S. Gollakota, and J. R. Smith, “TurboCharging ambient backscatter communication,” in Proceedings of ACM SIGCOMM, Chicago, USA, August 17-22, 2014.   
[14] J. Wang, H. Hassanieh, D. Katabi, and P. Indyk, “Efficient and reliable low-power backscatter networks,” in Proceedings of ACM SIGCOMM, Helsinki, Finland, August 13-17, 2012.   
[15] D. Bharadia, K. R. Joshi, M. Kotaru, and S. Katti, “Backfi: High throughput wifi backscatter,” in Proceedings of ACM SIGCOMM, Budapest, Hungary, August 20-25, 2018.   
[16] B. Kellogg, V. Talla, J. R. Smith, and S. Gollakot, “Passive WiFi: Bringing low power to WiFi transmissions,” in Proceedings of USENIX NSDI, Santa Clara, CA, March 16-18, 2016.   
[17] P. Zhang, D. Bharadia, K. Joshi, and S. Katti, “HitchHike: Practical backscatter using commodity WiFi,” in Proceedings of ACM SenSys, Stanford, CA, USA, November 14-16, 2016.   
[18] P. Zhang, C. Josephson, D. Bharadia, and S. Katti, “FreeRider: Backscatter communication using commodity radios,” in Proceedings of ACM CONEXT, Incheon, Republic of Korea, December 12-15, 2017.   
[19] P. Zhang, M. Rostami, P. Hu, and D. Ganesan, “Enabling practical backscatter communication for on-body sensors,” in Proceedings of ACM SIGCOMM, Salvador, Brazil, August 22-26 2016.   
[20] A. Wang, V. Iyer, V. Talla, J. R. Smith, and S. Gollakota, “FM backscatter: Enabling connected cities and smart fabrics,” in Proceedings of USENIX NSDI, Boston, MA, USA, March 27-29, 2017.   
[21] R. Z. F. Zhu, Y. Feng, S. Peng, X. Tian, H. Yu, and X. Wang, “OFDMAenabled WiFi backscatter,” in Proceedings of ACM MobiCom, Los Cabos, Mexico, October 21-25, 2019.   
[22] A. Varshney, O. Harms, C. PÃl’rez-Penichet, C. Rohner, F. Hermans, and T. Voigt, “LoRea: A backscatter architecture that achieves a long communication range,” in Proceedings of ACM SenSys, Delft, Netherlands, November 06-08, 2017.   
[23] V. Talla, M. Hessar, B. Kellogg, A. Najafi, J. R. Smith, and S. Gollakota, “LoRa backscatter: Enabling the vision of ubiquitous connectivity,” in Proceedings of ACM UbiComp, Maui, HI, USA, September 11-15, 2017.   
[24] Y. Peng, L. Shangguan, Y. Hu, Y. Qian, X. Lin, X. Chen, D. Fang, and K. Jamieson, “PLoRa: A passive long-range data network from ambient LoRa transmissions,” in Proceedings of ACM SIGCOMM, Budapest, Hungary, August 20-25, 2018.

[25] J. R. Smith, A. P. Sample, P. S. Powledge, S. Roy, and A. V. Mamishev, “A wirelessly-powered platform for sensing and computation,” in Proceedings of ACM UbiComp, Orange County, California, September 17-21, 2006.   
[26] X. Guo, L. Shangguan, Y. He, J. Zhang, H. Jiang, A. A. Siddiqi, and Y. Liu, “Aloba: Rethinking ON-OFF keying modulation for ambient LoRa backscatter,” in Proceedings of ACM SenSys, Online, November 16-19, 2020.   
[27] P. Hu, P. Zhang, M. Rostami, and D. Ganesan, “Braidio: An integrated active-passive radio for mobile devices with asymmetric energy budgets,” in Proceedings of ACM SIGCOMM, Salvador, Brazil, August 22- 26 2016.   
[28] V. Liu, V. Talla, and S. Gollakota, “Enabling instantaneous feedback with full-duplex backscatter,” in Proceedings of ACM MobiCom, Maui, Hawaii, USA, September 7-11, 2014.   
[29] N. S. Yunfei Ma and F. Adib, “Drone relays for battery-free networks,” in Proceedings of ACM SIGCOMM, Los Angeles, CA, USA, August 21- 25, 2017.   
[30] M. Hessar, A. Najafi, and S. Gollakota, “Netscatter: Enabling large-scale backscatter networks,” in Proceedings of USENIX NSDI, Santa Clara, CA, March 16-18, 2016.   
[31] R. Eletreby, D. Zhang, S. Kumar, and O. Yagan, “Empowering lowpower wide area networks in urban settings,” in Proceedings of ACM SIGCOMM, Los Angeles, CA, USA, August 21-25, 2017.   
[32] X. Xia, Y. Zheng, and T. Gu, “FTrack: Parallel decoding for LoRa transmissions,” in Proceedings of ACM SenSys, New York, USA, November 10-13, 2019.   
[33] B. A. Nahas, S. Duquennoy, and O. Landsiedel, “Network-wide consensus utilizing the capture effect in low-power wireless networks,” in Proceedings of ACM SIGCOMM, Helsinki, Finland, August 13-17, 2012.   
[34] X. Xia, Y. Zheng, and T. Gu, “LiteNap: Downclocking LoRa reception,” in Proceedings of IEEE INFOCOM, Online, July 6-9, 2020.   
[35] D. Tse and P. Viswanath, Fundamentals of wireless communication. Cambridge university press, 2005.   
[36] Online, “Saw chip epcos b39871b3715u410,” 2020.   
[37] Online, “Low-power comparator NCS2202,” 2020.   
[38] H. Iqbal, M. H. Alizai, Z. A. Uzmi, and O. Landsiedel, “Taming linklayer heterogeneity in IoT through Interleaving multiple link-layers over a single radio,” in Proceedings of ACM SenSys, Delft, Netherlands, November 06-08, 2017.   
[39] A. Balanuta, N. Pereira, S. Kumar, and A. Rowe, “A cloud-optimized link layer for low-power wide-area networks,” in Proceedings of ACM MobiSys, Online, June 15-19, 2020.   
[40] M. Jin, Y. He, C. Jiang, and Y. Liu, “Fireworks: Channel estimation of parallel backscattered signals,” in Proceedings of IEEE/ACM IPSN, Virtual event, Australia, April 21-24, 2020.   
[41] P. Hu, P. Zhang, and D. Ganesan, “Laissez-faire: Fully asymmetric backscatter communication,” in Proceedings of ACM SIGCOMM, London, United Kingdom, August 17-21, 2015.   
[42] J. Ou, M. Li, and Y. Zheng, “Come and be served: Parallel decoding for COTS RFID tags,” IEEE/ACM Transactions on Networking, vol. 25, no. 3, pp. 1569–1581, 2017.   
[43] M. Jin, Y. He, X. Meng, Y. Zheng, D. Fang, and X. Chen, “Fliptracer: Practical parallel decoding for backscatter communication,” IEEE/ACM Transactions on Networking, vol. 25, no. 2, pp. 3559–3572, 2017.   
[44] M. Jin, Y. He, X. Meng, D. Fang, and X. Chen, “Parallel backscatter in the wild: When burstiness and randomness play with you,” in Proceedings of ACM MobiCom, New Delhi, India, October 29-November 02, 2018.   
[45] Online, “Antenna,” 2020.   
[46] Online, “De0-nano-soc FPGA,” 2020.   
[47] Online, “STM32L083RZ,” 2020.   
[48] Online, “Semtech SX1276,” 2020.   
[49] Online, “USRP,” 2020.   
[50] Online, “LoRa Alliance,” 2020.   
[51] Online, “Semtech SX1257,” 2020.   
[52] Online, “NB-IoT,” 2020.   
[53] Online, “SigFox,” 2020.   
[54] A. Gamage, J. C. Liando, C. Gu, R. Tan, and M. Li, “LMAC: Efficient carrier-sense multiple access for LoRa,” in Proceedings of ACM MobiCom, Online, September 21-25, 2020.   
[55] X. Guo, L. Shangguan, Y. He, N. Jing, J. Zhang, H. Jiang, and Y. Liu, “Saiyan: Design and implementation of a low-power demodulator for lora backscatter systems,” in Proceedings of USENIX NSDI, Renton, WA, USA, April 4-6, 2022.

![](images/3d40638d7146376c6d5f77c02abdefd1c5a3fa7c2ce3434929f0fef276154448.jpg)



Xiuzhen Guo received the B.E. degree in the School of Electronic and Information Engineering from Southwest University in 2016. She is currently a PhD student in Tsinghua University. Her research interests include Internet of Things and wireless networks.

![](images/e8f1a942fe78002e9507ef9f8103e9d319e43e5f4f9842686fc2b6a3195c5b7e.jpg)



Haotian Jiang is currently an undergraduate student in Tsinghua University. His research interests include wireless network co-existence and crosstechnology communication.

![](images/ab910559f6860ec67f31210cc45ec34260691b34285a70cca8f63d32cf0cbe39.jpg)



Longfei Shangguan is a senior researcher at Microsoft Cloud & AI, Redmond. He received his B.E. degree in Xidian University, and his PhD degree in Hong Kong University of Science and Technology. His research interests include networking, IoT, and wireless systems.

![](images/604ab943a9bfa46a0194f517d65253d1dee2a57c0e2f74619e5299711cf85790.jpg)



Awais Ahmad Siddiqi earned his BS degree in Electronics Engineering from University of Wah, and MS degree from Northeastern University, China. Currently, he is enrolled as a PhD student in Tsinghua University. His research interests include Internet of Things, remote sensing and wireless networks.

![](images/292adce88fba2984d94a20c02a9580e034bb3ad243d2f6eee45fa20b5c8d33c1.jpg)



Yuan He is an associate professor in the School of Software and BNRist of Tsinghua University. He received his B.E. degree in the University of Science and Technology of China, his M.E. degree in the Institute of Software, Chinese Academy of Sciences, and his PhD degree in Hong Kong University of Science and Technology. His research interests include wireless networks, Internet of Things, pervasive and mobile computing. He is a senior member of IEEE and a member of ACM.

![](images/579af133fb596e26ced6bba131af483dbbdee2ed75a4dba041ec563b61831f5e.jpg)



Yunhao Liu received his BS degree in Automation Department from Tsinghua University. He received an MS and a Ph.D. degree in Computer Science and Engineering at Michigan State University, USA. Yunhao is now MSU Foundation Professor and Chairperson of Department of Computer Science and Engineering, Michigan State University, and holds Chang Jiang Chair Professorship at Tsinghua University. He is an ACM Distinguished Speaker and now serves as the Editor-in-Chief of ACM Transactions on Sensor Networks. His research inter-

![](images/79fefe9210b0f210cf8565e555d4a1d642c626ddb9869e20956d49b37ee780e7.jpg)



Jia Zhang is currently an undergraduate student in Tsinghua University. His research interests include wireless sensor networks and cross-technology communication.

ests include sensor network and pervasive computing, peer-to-peer computing, IOT and supply chain. Yunhao is a Fellow of IEEE and ACM.