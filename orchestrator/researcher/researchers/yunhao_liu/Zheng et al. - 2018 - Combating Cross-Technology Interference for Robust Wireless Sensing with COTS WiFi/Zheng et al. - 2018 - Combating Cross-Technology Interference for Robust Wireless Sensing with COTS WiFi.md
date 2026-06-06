# Combating Cross-Technology Interference for Robust Wireless Sensing with COTS WiFi

Yue Zheng∗†, Zheng Yang∗, Junjie Yin∗, Chenshu Wu∗, Kun Qian∗, Fu Xiao‡ Yunhao Liu∗, ∗School of Software and TNList, Tsinghua University

†Department of Electronic Engineering, Tsinghua University

‡College of Computer, Nanjing University of Posts and Telecommunications

{cczhengy, hmilyyz, yinjj16, wucs32, qiank10, xiaof, yunhaoliu}@gmail.com

Abstract— The past years have witnessed the rapid conceptualization and development of wireless sensing based on Channel State Information (CSI) with commodity WiFi devices. Many research efforts have been devoted to promote WiFi sensing by innovating applications, refining models and optimizing algorithms. A critical issue of Cross-Technology Interference (CTI), however, is surprisingly unnoticed and largely unexplored in the existing literature. In this paper, we demonstrate that CTI poses severe impacts on CSI measurements and further degrades the performance of CSI-based sensing. Based on indepth understanding of such impacts, we present PERFIC to deal with CTI for CSI on commercial WiFi. We first exploit the inherent cyclostationarity property of different signals to detect CTI and further identify the specific distorted subcarriers on CSI. For each interfered CSI, we then propose to mitigate the impacts of CTI by amending the abnormal subcarriers. We conduct experiments on typical wireless sensing applications, including human detection and activity classification, using offthe-shelf WiFi devices. The results demonstrate that PERFIC yields a remarkable performance gain of >30% with high efficiency and outperforms existing robust classifiers. By providing interference-free CSI that is amendable to existing and emerging CSI-based sensing applications, PERFIC underpins new insights for improving the sensitivity and reliability of wireless sensing.

Index Terms—Wireless Sensing; Channel State Information; Radio Frequency Interference

# I. INTRODUCTION

Wireless networks, especially WiFi, have been pervasively deployed in modern cities. Recently, innovations in WiFi technology have turned WiFi from a sole communication medium to an attractive sensing platform, which is drawing increasing attention. Vast research efforts have been devoted to boost WiFi sensing for a wide range of applications, e.g., indoor localization and navigation [1]–[4], human detection [5], gesture recognition [6], activity classification [7], fall detection [8], sleep monitoring [9], and keystroke recognition [10]. The rapid conceptualization and development of WiFi sensing benefit from the physical layer Channel State Information (CSI), since it is currently available on commodity off-the-shelf (COTS) WiFi devices [11]. The rationale lies in that different human behaviors introduce different multipath distortions in signal propagation, which can be reflected by CSI measurements. The key advantages of wireless sensing lie in that it does not require line-of-sight measurements, provides omnidirectional coverage, preserves sensitive privacy, and works in a contactless manner, fostering various ubiquitous applications particularly in the era of Internet of Things.

![](images/5b16332107b7116a2d68317a83e33571b06d781cf97051b3c9b5ee89bcdeda25.jpg)



Figure 1. An illustrative example of PERFIC

Existing works mostly promote WiFi sensing from various perspectives of innovative applications [6], [9], elaborate models [1], [7], [12], [13], and optimized algorithms [8], [14]. However, WiFi sensing on COTS devices still faces a number of challenges to come into practical uses, among which Radio Frequency Interference (RFI) acts as a critical one. A wellknown fact is that WiFi signals suffer from severe interferences. WiFi typically operates in the free 2.4GHz ISM band, which is extremely crowded especially in modern buildings where there are a large number of radio devices. The RF interference includes both intra-technology interference (ITI) from WiFi devices working on the same or an adjacent channel, and cross-technology interference (CTI) from external non-WiFi RF devices such as Bluetooth, ZigBee nodes and microwave ovens, as shown in Fig. 1. Without loss of generality, we use the term CTI and external RFI interchangeably in this paper. As Fig. 2 shows, CTI can significantly distort CSI, degrading its sensibility and reliability for sensing applications.

Such interferences, while having been recognized and handled in wireless communications [15]–[17], are heavily ignored in WiFi-based sensing. The non-negligible impacts are either mistakenly mixed with motion-induced variations or merely treated as unknown noises [5], [7], [9]. Most of existing works merely neglect the RFI issue and apply general signal processing techniques to filter out uncertain noises [7]–[9]. The only relevant work [18], to the best of our knowledge, that observes the critical impacts of RFI on CSI-based sensing based on a dedicated platform called Wireless Ad hoc System for Positioning (WASP) [19], however, does not provide targeted solutions to cope with interference directly. To stimulate WiFi sensing for practical application in pervasive environment, we need to confidently detect such RFI and meticulously eliminate their crucial impacts on CSI.

To achieve this goal, we propose PERFIC to Process the External RF Interference for commodity CSI (see Fig. 1). Different from traditional interference detection methods like Airshark [20] that target at detecting the existence of RF devices using a group of measurements, we mainly focus on understanding, detecting, and mitigating non-WiFi interferences for each individual CSI measurement. Prior work [21] has found that cyclostationary analysis, which is a typical method for signal detection and identification by exploiting the inherent distinctive cyclostationarity of different signals, is also applicable to detect radio frequency interferences on CSI. In this paper, we further enhance and extend it to precisely identify the specific subcarriers that are interfered for each single CSI measurement.

On this basis, we propose a frequency-domain mitigation algorithm to alleviate the impacts of CTI on sensing by renovating the interfered CSI. In static situations, where CSI keeps relatively stable over time, one can simply replace an interfered CSI reading with an adjacent normal one. In dynamic environments, however, CSI varies over time regardless of RF interference. Thus we need to identify and further repair the stained parts of each interfered CSI measurement. Thanks to the fact that non-WiFi devices occupy only a narrow bandwidth at any instant, each CSI would be affected on a specific subset of subcarriers. Inspired by this insight, we propose a straight-forward method to recover the interfered subcarriers of each CSI, which can be identified by the above mentioned detection algorithm, and then employ linear interpolation of the responses at the unaffected subcarriers. By doing this, a normal (i.e., interference-free) version of CSI would be obtained from the interfered measurement, which can then be used to improve various sensing applications.

To validate the effectiveness of PERFIC, we conduct real world experiments on COTS WiFi devices and implement two case studies of typical sensing applications including human detection and activity recognition. Experimental results demonstrate that a favorable performance gain of over 30% is achieved by pertinently accounting for CTI in moving human detection. With 500 CSI measurements as the input, it takes an average time of 1.50s and 0.66s for RFI detection and mitigation, respectively. And the performance of activity recognition can be further improved with renovated CSI fed into the antinoise classifier. By efficiently producing interference-free CSI with superior sensibility and reliability, we believe this work points out a new angle of view from the interference dimension for comprehensively understanding and profitably promoting CSI-based sensing for existing and emerging applications.

In summary, our core contributions are as follows.

1) We demonstrate the significant impacts and embody the characteristics of CTI on CSI measurements on COTS WiFi devices, which have not been emphatically discussed previously. Our results expand and deepen the literature’s understanding of CSI-based sensing from an unexplored perspective of radio interferences.   
2) We enhance the algorithm for the detection of distorted CSI measurements interfered by different types of external interferences on COTS devices. The algorithm works with single CSI measurement and identifies precisely the

exact subcarriers that are interfered.

3) We devise an interference mitigation scheme that is capable of repairing the stained subcarriers of each interfered CSI without violating the normal components within the same CSI or the adjacent CSI series, yielding a superior CSI with better sensitivity and reliability. As far as we are aware of, PERFIC is the first interferenceaware processing algorithm for CSI noises, which is amendable to various existing or emerging applications.   
4) We validate the effectiveness of PERFIC via experiments on typical sensing applications of human detection and activity applications using COTS devices. The results demonstrate that PERFIC yields a remarkable performance gain of >30% with high efficiency and outperforms existing anti-noise classifiers.

The rest of the paper is organized as follows. In Section II, we provide preliminary measurements and analyses on interferences on CSI. Then we present our interference detection and mitigation techniques in Section III and Section IV, respectively. The experimental evaluation is provided in Section V. We review the related works in Section VI and conclude this work in Section VII.

# II. INSPECTING RFI ON CSI

# A. Radio Frequency Interference on 2.4GHz

CSI-based sensing leverages the prevalent WiFi, which operates in the 2.4GHz and 5.8GHz ISM radio bands. As the unlicensed wireless spectrum continues to be more and more crowded, WiFi signals suffer from severe RF interferences from both internal WiFi radios and external non-WiFi radios.

Intra-technology interference from internal WiFi devices exists in both co-channel and adjacent channels. Firstly, adjacent WiFi channels (e.g. channel 1 and 2) will interfere with each other due to their overlapped spectrum. That is why it is usually advised to only use channel 1/6/11 if there are many WiFi access points (APs) in the environment. In addition, it is very common that multiple WiFi APs operate on the same channel in modern indoors environments where there are typically a number of WiFi devices. This will result in serious co-channel interference.

Apart from the above, there are many non-WiFi devices operating on the same unlicensed ISM band of 2.4GHz (e.g., Bluetooth devices, ZigBee radios, microwave ovens, cordless phones, etc.). The impacts of non-WiFi radios on a WiFi link are two-fold: On one hand, the presence of non-WiFi devices could degrade the throughput of a WiFi link, which erodes the regular sampling of CSI measurements. On the other hand, they can pose a significant impact on the CSI vector of a successfully received packet, altering the amplitudes and phases and distorting the subcarrier shapes as demonstrated in the following. Such cross-technology RF interferences are particularly critical in emerging contexts of smart space (smart home, smart buildings and smart factories, etc.) where a large amount of RF devices are widely deployed, which is also the typical application scenario of WiFi sensing [6]–[8]. Previous work [18] observes that RF interference induced by a pair of IEEE 802.11a devices significantly distorts CSI measurements obtained by WASP platform. Our work, however, mainly focus on understanding, detecting, and mitigating non-WiFi interferences on CSI provided by commercial WiFi devices.

![](images/f98666aef1e0565d7ae5bdc90603c85fd2ef9a4eb181dcb15ec927979e6c3c70.jpg)



(a) Microwave oven interference

![](images/a3a3d4a0fab2f68b6180832af7f1130348bcbf6b547c3ad4d8bc2f6d81fe7381.jpg)



(b) Bluetooth interference

![](images/e0f29c858367f5660590ea8977298049c2bf347a9eaec3cc3098df4795e0a940.jpg)



(c) ZigBee interference   
Figure 2. CSI without and with external interference measured by USRP on WiFi Channel 9

Particularly, there are mainly three common types of non-WiFi radios, i.e., frequency hoppers (Bluetooth), fixed frequency devices (ZigBee) and broadband interferers (microwave ovens), which are as prevalent as WiFi in typical environments such as homes, offices and various public indoor spaces. We first present basic preliminaries on principles and properties of them.

(1) Bluetooth: The Bluetooth protocol divides 2.4 GHz band into 79 designated channels of 1 MHz bandwidth, and uses a technology called frequency-hopping spread spectrum (FHSS) to transmit data. The later Bluetooth low energy (BLE) uses 2 MHz spacing and correspondingly accommodates 40 channels. Therefore, one WiFi channel (20/40 MHz) covers multiple Bluetooth channels. Besides, Bluetooth performs frequency hopping at a rate of 1600 hops per second. Thus we may observe multiple spectrum occupancies of Bluetooth signals on one WiFi channel even in a short time.

(2) ZigBee: ZigBee radio operates on one of the predefined 16 channels in 2.4GHz band, each occupying a bandwidth of 2 MHz. All the ZigBee channels overlap with WiFi channels. Data transmission rate (corresponding to the radio status on/off) depends on the specific protocol implementation.

(3) Microwave oven: A microwave oven typically operates by emitting high RF energy on 2.4 GHz. It uses a selfoscillating vacuum power tube that opens for half of every AC cycle. The instantaneous frequency varies widely over each cycle and occupies only a narrow bandwidth at any instant, rather than the full operating frequency band. As shown in [22], microwave radios can be regarded as FM signals with a sweeping bandwidth which equals the AC power switching frequency.

Among these three types of interference sources, microwave oven operates with a very high power compared to WiFi. In contrast, Bluetooth and ZigBee both emit low-energy signals. Nevertheless, their interference on WiFi cannot be ignored, especially when there are a large number of devices in the era of IoT or they are located near the WiFi devices.

# B. CSI Measurements with Cross-Technology Interference

We now formally analyze and experimentally validate how typical non-WiFi interferences affect CSI measurements.

CSI is the sampled version of channel response in timefrequency space, which is provided by off-the-shelf WiFi Network Interface Cards (NICs), especially the Orthogonal Frequency Division Multiplex (OFDM) based WiFi standards (i.e. IEEE 802.11a/g/n) [23]. Suppose that an AP sends out OFDM beacon messages to a receiver and there is no external interference yet. Denote the transmitted and received signals in frequency domain as X and Y , respectively. Then CSI Hˆ is estimated as follows:

$$
\hat {H} = \frac {Y}{X}, \tag {1}
$$

where $\hat { H } ~ = ~ [ \hat { H _ { 1 } } , \hat { H _ { 2 } } , . . . , \hat { H _ { N } } ] ^ { T }$ , N denotes the number of subcarriers in an OFDM symbol. Each element in vector Hˆ is a complex number encoding amplitude and phase information. For WiFi signals, CSI is estimated during packet preamble [23] since preambles are definite and known by the receiver.

Now assume there is a certain kind of external RF devices working at the same frequency coincidentally at some instants as the AP does. Then the received signal should be revised to $Y { \mathrm { + } } Y ^ { \prime }$ , where $Y ^ { \prime }$ denotes the interfering signal. As the receiver doesn’t know the existence of interference, it still estimates CSI by dividing the received signal by X. Accordingly, the estimated CSI becomes:

$$
\hat {H} = \frac {Y}{X} + \frac {Y ^ {\prime}}{X}. \tag {2}
$$

Evidently, all the three kinds of interferences mentioned above may contribute to $Y ^ { \prime }$ and thus distort the CSI estimation Hˆ .

We verify the above formal insights by experimental measurements. Note that CSI measured on commodity WiFi devices provides only 30 subcarriers [23]. To fully observe the impacts induced by interference on all the subcarriers for thorough analysis, we collect raw WiFi signal samples in interference-free environments as well as under individual interference source of microwave oven, Bluetooth and ZigBee radios using a Universal Software Radio Peripheral (USRP) device. We implement an OFDM receiver to extract CSI from raw signal samples. Fig. 2 depicts the normalized amplitude of CSI with and without interference. Obviously, CSI is significantly distorted by any type of external interferences, of which microwave oven appears to be the most serious one. It is also confirmed that even the low-power Bluetooth and ZigBee radios pose non-negligible impacts. In particular, we observe that the impacts are mainly concentrated on a subset of subcarriers that share exactly the same frequencies with the specific interference radio.

Provided the severe impacts of CTI on CSI, the performance of sensing will definitely degrade. In order to promote the robustness of CSI-based sensing, prior work [18] exploits Sparse Representation Classification (SRC) which is robust to noise to perform activity classification. Such method, however, exhibits high computational complexity and does not deal with CSI directly. The measurements still cannot be utilized in other applications since interferences on CSI are neither identified nor alleviated. Previous work [24] observes that abrupt fluctuations of CSI amplitude are related to the occasionally changed modulation and coding scheme (MCS) index. By digging into RF interference, we further note that WiFi usually adjusts its MCS to better resist interference [25]. In other words, the main reason of MCS index changes is actually RF interference, which further leads to CSI distortions.

Considering that diverse devices affect CSI measurements at different subcarriers and in different degrees, we investigate to propose a generic framework as shown in Fig. 1 which can identify the distorted CSI and amend the stained subcarriers directly to mitigate the impacts of CTI. Previous methods like Airshark [20] can accurately detect the existence of RF devices, but they usually rely on features extracted from a group of CSI measurements and thus do not apply in the case of examining whether and where each CSI measurement is distorted. In the rest of this paper, we still term our problem of detecting and mitigating interfered CSI as interference detection and mitigation respectively for simplicity. Currently we mainly account for CTI while leaving the internal WiFi interference to our future work.

# III. INTERFERENCE DETECTION USING CYCLOSTATIONARITY

Prior work [21] provides an RFI detection algorithm by utilizing the cyclostationarity of wireless signals. The proposed algorithm is capable of detecting distorted CSI measurements, but cannot further determine the exactly interfered subcarriers within each CSI. As mentioned above, an efficient interference processing system should only amend the distorted subcarriers and keep the normal parts intact. Thus in this paper, we enhance and extend it to further identify the distorted subcarriers. In the following, we first provide the preliminaries on cyclostationarity and then briefly introduce the principles of the RFI detection algorithm in [21]. Finally we illustrate how to promote the algorithm for finer-grained detection.

# A. Cyclostationarity

Many wireless signals can be modeled as cyclostationary signals due to the presence of underlying periodicity induced by frame structure, modulation methods, carrier frequencies and so on. For example, WiFi signals exhibit cyclostationary property due to the specific OFDM structure including pilots and cyclic prefixes [26]. Different kinds of signals manifest distinctive repeating patterns, which is also called the cyclic frequency. Therefore, cyclostationary analysis has been adopted as a typical method to detect and identify different signals [17], [27]. Usually it requires raw signal samples as input. Denote the raw signal samples in time domain by x[n], then cyclic frequency can be revealed by calculating the Cyclic Autocorrelation Function (CAF):

$$
R _ {x} ^ {\alpha} (\tau) = \sum_ {n = - \infty} ^ {\infty} x [ n ] x ^ {*} [ n - \tau ] e ^ {- j 2 \pi \alpha n}. \tag {3}
$$

The CAF will only exhibit a high value for certain delay τ and cyclic frequency α. Alternative to CAF that operates on timedomain signal samples, it’s more efficient to use its equivalent frequency-domain representation called Spectral Correlation Function (SCF) to depict underlying cyclostationarity:

$$
S _ {x} ^ {\alpha} [ k ] = \frac {1}{L} \sum_ {l = 0} ^ {L - 1} X _ {l} [ k ] X _ {l} ^ {*} [ k - \alpha ] \tag {4}
$$

where $X _ { l } [ k ]$ is the Fourier transform of the received signal for the lth time window, that is

$$
X _ {l} [ k ] = \sum_ {n = N l} ^ {N l + N - 1} x [ n ] e ^ {\frac {- j 2 \pi n k}{N}}, \tag {5}
$$

where N is the duration of a single OFDM symbol. Once the SCF spectrum is obtained, the signal types can be easily recognized by directly matching the SCF against known ideal SCF profiles [28] or performing classification on a set of unique features [17].

Although cyclostationary analysis usually requires raw signal samples as input, prior work [21] has demonstrated that cyclostationary analysis is also applicable on CSI to detect RFI. Denote the received WiFi signal and interfering signal as $Y = H X$ and $Y ^ { \prime } = H ^ { \prime } X ^ { \prime }$ , respectively. Here H and H′ refer to the CSI corresponding to the two signals. Then the estimated CSI can be expressed as:

$$
\hat {H} = H + \frac {H ^ {\prime} X ^ {\prime}}{X} \tag {6}
$$

Since signals of different protocols own different repeating patterns and cyclic frequencies, cyclostationarity will not disappear from Hˆ even if X′ is divided by X. Therefore, it is feasible to apply cyclostationary analysis for detecting radio frequency interference with merely CSI, as detailed next.

# B. Interference Detection on CSI

Replace $X _ { l } [ k ]$ with $H _ { l } [ k ]$ , and Eqn. (4) is transformed into:

$$
S _ {h} ^ {\alpha} [ k ] = \frac {1}{L} \sum_ {l = 0} ^ {L - 1} H _ {l} [ k ] H _ {l} ^ {*} [ k - \alpha ] \tag {7}
$$

where L denotes the total number of OFDM symbols in a packet. As CSI is estimated from the long preamble on a packet base, all the OFDM symbols in a packet correspond to only one CSI measurement actually. Therefore, Eqn. (7) can be abbreviated into such form:

$$
S _ {h} ^ {\alpha} [ k ] = H [ k ] H ^ {*} [ k - \alpha ] \tag {8}
$$

Then the SCF for each CSI measurement can be calculated.

The SCF matrix can be utilized for RFI detection [21]. As shown in Fig. 3b, if one CSI measurement is distorted by RF interferences, the corresponding SCF will exhibit apparent peaks at certain coordinates. With both amplitude and phase information of several subcarriers distorted by CTI, the cyclic frequencies are sufficiently visible on corresponding SCF. As comparison, SCF without interference does not exhibit any peak as Fig. 3a shows because H itself does not maintain underlying repeating patterns. Specifically, the gradient of a

![](images/12967b43e329361550d4add1ab2529af2222d0df584073f9d5bafebe07ac5aa4.jpg)



(a) SCF without interference

![](images/b18703ed669c9da8ebf1b75b5316f1ba78e20552e66fc399efb741505882a8c3.jpg)



(b) SCF with interference   
Figure 3. SCF without/with external interference measured by COTS WiFi

SCF spectrum with interference increases/decreases rapidly at certain points. On the contrary, for SCF without interference, the gradient changes smoothly within a small range. Thus the gradient matrix of $\mathrm { s c r } { } \mathrm { s }$ amplitude is exploited to recognize the interfered CSI [21]. Then Singular Value Decomposition is performed on the gradient matrices and the highest singular value of the gradient matrix is chosen as the effective feature for detecting interference, which appears to be much larger with existence of RF interference. An appropriate threshold for the highest singular value can be obtained via pre-training.

# C. Distorted Subcarriers Identification

For efficient interference mitigation mechanism, merely identifying the distorted CSI measurements are far from being desired. We need to further determine the stained subcarriers for later amending. Our solution is illustrated as follows.

If one CSI measurement is determined to be with interference by the RFI detection algorithm, we first locate the subset of stained subcarriers by finding the spiked peak/valley of CSI amplitudes as Eqn. (6) performs complex addition. These subcarriers correspond to the central frequency of CTI and suffer the most serious distortion. It is possible that there might exist more than one peak/valley if various RFI sources are working. If they are close to each other, we merge them and choose the most prominent one.

Then we pick a subsequence of subcarriers that covers the identified peak/valley (or neighboring peaks/valleys), by putting the peak/valley in the middle of the subsequence. The bandwidth on which cross-technology interference works is usually no larger than 2MHz. The adjacent subcarriers, however, might also be impacted even if CTI does not occupy the corresponding frequency as Fig. 2 shows. So the subsequence is controlled with a proper length, covering a conservative bandwidth of no more than 4MHz . It is possible that not all the subcarriers (especially the marginal ones) in the subsequence are distorted. Nevertheless, the following interference mitigation mechanism will exert little influence on normal subcarriers and only amend the distorted ones.

# IV. INTERFERENCE MITIGATION

Passive WiFi sensing applications are built upon CSI measurements. Hence CSI distorted by RF interferences could hamper the sensing performance, regardless of application scenarios. In this section, we investigate to mitigate the influence of tampered CSI, provided they are detected to be interfered.

# A. Limitations of Existing Methods

To achieve this goal, many previous works treat the impacts of interferences as general noises and employ time-domain filtering to sift out unpredictable outliers in CSI measurements [5], [7], [9]. These works usually take a time series of a specific subcarrier as inputs and apply proper temporal filters to identify outliers and smooth the whole sequence. However, temporal filtering may not apply to cross-technology interference mitigation because temporal filters generally only deal with sparse noises. If the CTI source works for a long time with sufficiently high packet rate, temporal filters will fail to eliminate the impacts induced by RF interferences gracefully. Fig. 4a illustrates the shortcomings of temporal filters by comparing CSI amplitude before and after calibration. The CSI amplitude shown in the figure is from a single subcarrier collected from a WiFi device in the static scenario. A pair of ZigBee nodes are working 1m away from the WiFi receiver. We apply the Hampel filter [29] with a sliding window to perform temporal filtering. Specifically, Hampel filter computes the median of a window composed of the samples and substitutes outliers falling out of the interval $\left[ \mu - 3 \sigma , \mu + 3 \sigma \right]$ with the median value, where $\mu$ and σ are the median and the median absolute deviation of the data sequence, respectively. As shown in the figure, there are still remaining outliers caused by CTI even after data calibration. Although a stricter threshold can be adopted for the filter to eliminate RF interference, the motion-induced CSI variations will be also attenuated, especially for those interference-free subcarriers. In Fig. 4b, the CSI amplitude is collected in the dynamic scenario. Some of the blue points which indicate interference-free CSI measurements are also filtered out by the temporal filter, leading to motion-induced variations concealed. Further details about how temporal filters perform are illustrated in Section V. Also note that simply discarding the interfered subcarriers is not applicable for frequency hoppers and broadband interferences as the interfered subcarriers vary.

# B. Frequency-Domain Mitigation

Since we have identified whether each CSI measurement is interfered and also known the indices of distorted subcarriers, we intend to patch the interfered subcarriers over the frequency domain. The key advantages over temporal filtering lie in that we only modify the interfered components in each CSI measurement, keeping the precedent or subsequent subcarriers intact, and that frequency-domain method can operate with single measurement without relying on sequential CSI vectors.

In static scenario, we simply replace the interfered CSI with an unaffected normal one at an adjacent time instant since CSI keeps relatively stable in static environments. In dynamic scenario, however, the straight-forward method no longer applies because CSI measurements themselves, whether interfered or not, vary over time due to human motions and environmental changes. Our solution is inspired by the pilotaided channel estimation algorithm [30] which is commonly adopted in OFDM systems. In an OFDM symbol, there are several subcarriers defined as pilot subcarriers with values previously known. Then the channel frequency responses at pilot subcarriers can be easily estimated. By performing interpolation of the responses at pilot subcarriers, the responses of other subcarriers can also be obtained. This algorithm gives us inspiration that it is reasonable to conduct frequency-domain interpolation to patch the interfered CSI. Now we formally illustrate how our frequency-domain mitigation method works.

![](images/99ec11ea7e869b3c0e86c52c8c996b1d5d6199b49ccbf7b483c8619288993d60.jpg)



(a) Apply temporal filtering to resist CTI in static scenario

![](images/60f6642653b92256361d94d6da0355906b03bebebebe62db6451ababca56c0ec.jpg)



(b) Temporal filtering might attenuate motion-induced dynamics   
Figure 4. Illustration of temporal filtering on a single subcarrier with interference working

Our method processes only the interfered CSI one by one. The normal CSI measurements without interference will not be touched. And it is unnecessary to process the whole CSI since we have already identified which subcarriers are polluted. Then we apply linear interpolation of the responses at the adjacent unaffected subcarriers to restore those at the interfered subcarriers. The reasons why linear interpolation is adopted are two-fold. On one hand, the distorted subsequence and its adjacent subcarriers are in a small frequency range and it is probable that the amplitude of those subcarriers exhibits strong correlation when no CTI works. On the other hand, linear interpolation alleviates computational cost compared with other methods (e.g., higher-order polynomial interpolation, DFTbased interpolation, Wiener filter).

If the interfered subcarriers are at the head/end of CSI coincidentally, interpolation does not perform well because unaffected subcarriers will be just on one side of the picked subsequence. In such case, we directly filter out the outliers by applying Hampel filter on the subsequence.

Considering that distortion might still exist after the mitigation algorithm is performed, we adopt the iteration mechanism to eliminate interference on CSI effectively. For each amended CSI measurement, we perform RFI detection to identify whether the impacts that CTI exerts are alleviated. Only when the detection result is negative will we stop to perform frequency-domain mitigation. And we restrict the iterative times to avoid endless loop. Despite the fact that iteration mechanism increases computational cost, we find that linear interpolation is efficient enough and only a small portion of distorted CSI measurements need multiple amendment.

Fig. 5 illustrates an example where the severe impacts of CTI on CSI are gracefully mitigated. The range of the picked subsequence (distorted subcarriers and adjacent unaffected subcarriers) is marked by the grey line. Note that the amended version is not necessarily equivalent to the true CSI without interference. Nevertheless, with precise detection and proper mitigation, the impacts of interference are gracefully identified and eliminated, which paves the way for the enhancements against CTI for CSI-based sensing. In addition, as our approach only alters the interfered CSI and is independent of previous temporal filtering, they can be further integrated to deal with other regular random noises in time series of CSI.

# V. IMPLEMENTATIONS AND EVALUATION

# A. Experimental Methodology

We conduct experiments in a classroom (12m×7.2m) equipped with desks and chairs. We use commodity readily COTS devices to collect CSI. The transmitter is a minidesktop and the receiver is a laptop. Both are equipped with one antenna and an Intel 5300 NIC. They run Ubuntu 12.04 OS, working in the monitor mode [23] with MCS index unchanged. The transmitter injects 1000 packets per second. The interference sources involve a microwave oven, a Bluetooth wireless speaker and a pair of ZigBee nodes with CC2420 radio chips. The transmission rate of the ZigBee node is 100 packets per second and each packet lasts around 4 ms. We choose WiFi channel 7 with a center frequency of 2.442GHz, and accordingly select an overlapping ZigBee channel 18 fixed at 2.440GHz. Two typical and primary sensing applications, including human movements detection and activity classification, are carried out to evaluate PERFIC.

# B. Case Study I: Human Detection

1) Implementation: We implement a prototype based on a recent human detection system PADS [31]. In case of human movements, the amplitude and phase of CSI will vary significantly. Since variances are related to absolute signal power, PADS utilizes the respective covariance matrix of both amplitude and phase over a time window. Then eigenvalues of the covariance matrix are used as features to construct a SVM classifier for human detection.

We place the WiFi transmitter 3m away from the receiver. To amplify the impacts induced by interference, all three kinds of interference, i.e., a Bluetooth speaker, a pair of ZigBee Nodes and a microwave oven are working in the monitoring area. Both Bluetooth and ZigBee devices are placed 1m away from the WiFi receiver. The microwave oven is placed 5m away due to its high power. Otherwise, most packets would be dropped and few CSI readings could be collected.

We evaluate PERFIC from three perspectives: effectiveness, efficiency and robustness. For effectiveness, we evaluate the performance gain with PERFIC incorporated into the whole human detection mechanism. We utilize True Positive (TP)

![](images/79a3a3f91148d763f43048eb3d72ff74a6634329ea1395a8738c8e7b3491736b.jpg)



Figure 5. Illustrative CSI mitigation

![](images/57644ef1aa72c10ec3d61bfde92a52ac5a4067b14f61d3764c26744e8a61e568.jpg)



Figure 6. Human detection w/o CTI

![](images/5ee36b4c96495fca60cff2e170a11592bba4a4ad195d906a0e27ea547c080691.jpg)



Figure 7. Human detection with CTI

![](images/6adc6ccd805e3de861d7910c070f5ae2717e7d53abd6861ac840546adab509ac.jpg)



Figure 8. Time delay of processing 500 CSI measurements

![](images/c0be977fff0ee51d9d6cbc5bda344dd1a83bcd4eb3e6bd2a54b3cdbfdde6c511.jpg)



Figure 9. Detection in static scenarios

![](images/ed0147e7aa693441168ef3b55424273b91ca72eaba2d07d922b4d171f434dd40.jpg)



Figure 10. Detection in dynamic scenarios

rate and True Negative (TN) rate to compare the respective performance of using raw CSI, CSI processed with temporal interference mitigation method and CSI processed with PERFIC. Here TP rate is the proportion that human motion events are correctly detected when there are human movements actually. TN rate is the proportion that the environment is determined to be static when there is no human movements. In total we collect 150 human movement events and another 150 static events. Each event corresponds to a time window of 0.5s. For efficiency, we focus on evaluating CTI detection efficiency, which is the time that PERFIC takes to determine whether each CSI measurement in a group is distorted, and CTI mitigation efficiency, which is the time for reconstructing the distorted subcarriers. For robustness, we evaluate CTI detection accuracy from following aspects to verify that PERFIC can work in different scenarios: (1) different CTI sources (2) different distance between CTI and WiFi devices (3) different distance between WiFi transceivers. We measure over 100 groups of CSI measurements in each scenario and there are 4400 groups of evaluation traces in total.

2) Effectiveness: To quantitatively evaluate the performance of PERFIC, we compare it with using raw CSI (denoted as “None”) and CSI preprocessed by temporal filtering methods (denoted as “Temporal Filtering”). We choose Hampel filter to perform temporal filtering, since it can select sparse noises efficiently and is widely used in previous works [5], [7], [9]. As suggested in Fig. 6, temporal filtering methods promote TP rate slightly when no CTI works. There might exist temporary disturbances on CSI in static environment and temporal filters will remove them out. PERFIC outperforms temporal filtering, with the TP rate increasing to around 99% by mitigating the distortions. PERFIC plays a more significant role in human sensing with RFI. As Fig. 7 shows, when there are interference sources working, the performance of PADS using original CSI will definitely fall. The existence of interference sources destroy the correlation of CSI and debase the robustness of human sensing system. Besides, the weakness of temporal filter methods is apparent. In case of severe interference, temporal filtering fails to identify the distorted subcarriers and cannot eliminate their impacts. What is worse, it might regard the CSI without RFI as noise and significantly degrade the performance of human sensing. Conversely, PERFIC gracefully mitigates the impact of RFI on per CSI measurement and does not alter the human moving induced CSI variations. The accuracy of human sensing, after processing by PERFIC, remains around 99%. To conclude, PERFIC provides effective and robust mitigation of CTI which is fundamental to CSI-based sensing.

3) Efficiency: Efficiency (real-time capability) is an important evaluation metric in sensing applications. Next, we mainly investigate PERFIC’s time delay performance. We deploy the system on a desktop equipped with an Intel Core i5-4460 CPU running at 3.2 GHz. Considering PERFIC processes each CSI measurement individually, we divide all the collected CSI into groups and use 500 measurements as a basic evaluation unit. Fig. 8 shows the estimated processing time distribution of both interference detection and mitigation algorithms on MATLAB. The average time delay of identifying whether and where 500 measurements are distorted is 1.50s. And the average time of RFI mitigation is 0.68s. As not all the measurements are interfered and the number of distorted CSI in a group might vary, the standard deviation of mitigation time is larger than that of detection time. We believe PERFIC suffices the efficiency requirements of most wireless sensing applications.

4) Robustness: Robustness is an important evaluation metric because usually the type of CTI source, the location of interference and many other factors are uncontrollable. Considering that these factors mainly influence the RFI detection accuracy, we investigate the performance of the interference detection algorithm in this subsection. Here TP rate is the percentage that interference is correctly detected when there exists CTI. TN rate is the percentage that interference-free environment is correctly classified when no CTI works.

Impact of Interference Type Fig. 9 and Fig. 10 show the detection performance for different types of CTI, where B is Bluetooth, M is microwave oven, Z is ZigBee and BMZ refers to the co-existence of all three kinds of interference. We observe that PERFIC detects different types of CTI sources accurately and TP rates exceed 90% for all radios except for microwave oven. The rationale is that most of the strongly affected CSI readings are lost when the microwave oven is working. TN rates, which are actually independent of interference type, consistently approximates 100% in static scenario but drops by around 10% if someone is walking around. The main reason is that CSI might be unstable when propagation environment changes despite unaltered MCS index, which leads to false alarms arising.

![](images/d72eb898eaf2fe95372157fbbaf660bbbf392d9cd88b10f69b5ddc9bec3a6c28.jpg)



![](images/86415419381cb24e2ffbc4b7b978b8bd51d72690adc5dee99832e1e43796a4db.jpg)



Figure 11. Impacts of RFI-Rx distance Figure 12. Impacts of Tx-Rx distance

![](images/50e0a13c2d9d544679b6311230c9b0d6d500a9884e87e8915724f9b33dd5adb5.jpg)



(a) without CSI mitigation

![](images/7bafadc92407941ad7acc2dffe900daf595ef72b72a4210a1355fb3f0bd5f9b8.jpg)



(b) with CSI mitigation   
Figure 13. Confusion matrix of activity classification

Impact of RFI-Rx Distance We care about how CTI at different distances affects CSI measurements and how well PERFIC detects the CTI if it is relatively distant with weak impacts. Thus we evaluate the performance with RFI-Rx varying from 1m to 4m and use ZigBee devices as CTI. Fig. 11 shows that TP rate descends rapidly when RFI-Rx distance extends to 4m. ZigBee signal will attenuate seriously during long distance propagation. Thus ZigBee affects CSI fairly weakly when it is too far from the receiver and it can hardly affect the performance of CSI-based sensing.

Impact of Tx-Rx Distance As Fig. 12 shows, TP rate falls rapidly to lower than 20% when Tx-Rx distance is set 1m. The reason lies in that the power of WiFi signals will be much higher than that of interference with Tx-Rx distance decreasing. Hence the impact induced by CTI will be weakened, which results in the degradation of TP rate. Therefore, CTI only poses slight impacts on CSI-based sensing if WiFi transceivers are located sufficiently close.

# C. Case Study II: Activity Classification

1) Implementation: Prior work [18] utilizes Sparse Representation Classification (SRC) to deal with RF interference when performing activity recognition. [18] first collects a group of CSI measurements over a time window. Then raw CSI measurements are fed into the classifier to determine which activity the collected CSI belongs to.

We consider 4 different activity classes: (1) “empty”: empty environment, (2) “sitting”: sitting in the line-of-sight (LOS) path of the WiFi devices, (3) “standing”: standing in the LOS path, (4) “walking”: walking across the LOS path. As SRC involves $l _ { 1 }$ optimization which is of high computational complexity, we apply downsampling on the dataset and CSI is collected at the rate of 20 samples per second. For each activity class, we collect CSI in unchanged physical environments. In total we collect CSI data of 536 events and each event corresponds to the time window of 1 second, which is equivalent to 20 measurements. The training set consists of 60 events (15 for each class). And the other 476 events (119 for each class) are used in the test set. A pair of ZigBee nodes located 1m away from the receiver are CTI sources.

2) Overall Performance: We use the confusion matrix to present the results of activity recognition with raw CSI and CSI preprocessed by PERFIC as input. As shown in Fig. 13, the accuracy of “walking” will be improved from 79.0% to 84.9% if CSI is processed by PERFIC in advance. It is reasonable that there are still some of “walking” events misclassified as “empty” because [18] is actually a fingerprinting approach and motion-induced dynamics can hardly affect CSI when the person walks too far away. We also evaluate whether temporal filtering will influence the accuracy of activity classification. The accuracy of “walking” drops to 74.8% after calibration, which is consistent with the results in Section V-B.

# VI. RELATED WORKS

Wireless sensing with WiFi. Wireless sensing has attracted extensive interests in recognizing locations [2]–[4], [32] and body activities [18], [33]. Especially, the availability of CSI on COTS WiFi devices boosts a wide range of WiFi-based sensing applications, such as indoor localization [1], human presence detection [5], activity classification [7], fall detection [8] and gait recognition [34]. Besides innovating applications, researchers also strive to improve the performance of CSIbased sensing. CARM [7] models the relation between CSI variations and human motion speed to enable accurate activity recognition. Splicer [35] splices CSI readings from multiple channels to generate a wider frequency response and achieves finer-grained measurements in time domain. Despite vast research works, the RF interference problem is surprisingly overlooked in the existing literature. Prior work [18] which takes RFI into consideration merely employs an advanced classification technique for activity recognition, but does not present targeted solutions to renovating distorted CSI. In contrast, we aim to detect and mitigate RF Interference directly on CSI rather than throwing indiscriminate raw CSI into a classifier. While our approach is independent of these works, it is amendable to integrate with them for enhanced sensing.

Interference detection. RF interference is prevalent due to the explosive growth of wireless devices and scarce wireless spectrum. In order to detect interference, many techniques have been investigated including energy detector based, waveform based, cyclostationarity based and others [36]. Cyclostationary analysis relies on the fact that signals of different protocols exhibit different cyclic signatures. Previous works [17], [27], [28] utilize the cyclostationarity of wireless signals to identify the sources of interference, locate interfering radios and estimate spectrum occupancy. These systems all require raw signal samples as inputs, which is only available on specialized hardware like USRPs. Differently, [21] investigates the feasibility of applying cyclostationary analysis on CSI with COTS devices. Airshark [20] also exploits CSI and extract proper features (e.g., pulse distribution, duty cycle, bandwidth, etc.) from a group of CSI measurements to implement decision tree-based non-WiFi device detection. However, Airshark cannot determine whether each CSI measurement is distorted by RF interferences accurately for more robust CSI-based sensing. In this paper, we enhance the RFI detection algorithm proposed in [21] to further identify the distorted subcarriers, design interference mitigation mechanism and deploy PERFIC in typical wireless sensing applications. In order to resist interference, [15], [16] utilize MIMO capabilities. [15] enables 802.11n communication under high-power interference conditions. [16] investigates the co-existence of WiFi and ZigBee. However, both of them focus on the effectiveness of data transmission rather than mitigating interference for sensing.

# VII. CONCLUSIONS

Despite numerous research efforts on WiFi sensing, a critical issue of RFI is surprisingly overlooked and largely unexplored. In this paper, we present PERFIC to process the impacts of CTI on CSI measurements. We demonstrate that RFI poses severe impacts on CSI via theoretical analyses and experimental measurements. Then we exploit the cyclostationarity of different signals to detect RFI for CSI and particularly identify the distorted subcarriers within each interfered CSI. Accordingly, we further mitigate the impacts of RFI by amending the interfered parts of each CSI. We carry out two case studies on human detection and activity classification on COTS devices to validate the effectiveness, efficiency and robustness of PERFIC. Future work includes dealing with internal WiFi interferences and designing elaborate schemes for CSI sensing, accounting for RFI.

# ACKNOWLEDGMENTS

This work is supported in part by the National Key Research Plan under grant No. 2016YFC0700100, NSFC under grant 61522110, 61572366, 61602381, 61472057.

# REFERENCES

[1] M. Kotaru, K. Joshi, D. Bharadia, and S. Katti, “Spotfi: Decimeter level localization using wifi,” in Proceedings of ACM SIGCOMM, 2015.   
[2] C. Wu, Z. Yang, and C. Xiao, “Automatic radio map adaptation for indoor localization using smartphones,” IEEE Transactions on Mobile Computing, 2018.   
[3] Z. Yin, C. Wu, Z. Yang, and Y. Liu, “Peer-to-peer indoor navigation using smartphones,” IEEE Journal on Selected Areas in Communications, 2017.   
[4] Z. Yang, C. Wu, Z. Zhou, X. Zhang, X. Wang, and Y. Liu, “Mobility increases localizability: A survey on wireless indoor localization using inertial sensors,” ACM Computing Surveys, 2015.   
[5] C. Wu, Z. Yang, Z. Zhou, X. Liu, Y. Liu, and J. Cao, “Non-invasive detection of moving and stationary human with wifi,” IEEE Journal on Selected Areas in Communications, 2015.   
[6] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proceedings of ACM MobiCom, 2013.   
[7] W. Wang, A. X. Liu, M. Shahzad, K. Ling, and S. Lu, “Understanding and modeling of wifi signal based human activity recognition,” in Proceedings of ACM MobiCom, 2015.

[8] H. Wang, D. Zhang, Y. Wang, J. Ma, Y. Wang, and S. Li, “Rt-fall: A real-time and contactless fall detection system with commodity wifi devices,” IEEE Transactions on Mobile Computing, 2017.   
[9] X. Liu, J. Cao, S. Tang, and J. Wen, “Wi-sleep: Contactless sleep monitoring via wifi signals,” in Proceedings of IEEE RTSS, 2014.   
[10] K. Ali, A. X. Liu, W. Wang, and M. Shahzad, “Keystroke recognition using wifi signals,” in Proceedings of ACM MobiCom, 2015.   
[11] Z. Yang, Z. Zhou, and Y. Liu, “From RSSI to CSI: Indoor localization via channel response,” ACM Computing Survey, 2013.   
[12] K. Qian, C. Wu, Z. Yang, Y. Liu, and K. Jamieson, “Widar: decimeterlevel passive tracking via velocity monitoring with commodity wi-fi,” in Proceedings of ACM MobiHoc, 2017.   
[13] K. Qian, C. Wu, Y. Zhang, G. Zhang, Z. Yang, and Y. Liu, “Widar2.0: Passive human tracking with a single wi-fi link,” in Proceedings of ACM MobiSys, 2018.   
[14] J. Wang, H. Jiang, J. Xiong, K. Jamieson, X. Chen, D. Fang, and B. Xie, “LiFS: Low human-effort device-free localization with finegrained subcarrier information,” in Proceedings of ACM MobiCom, 2016.   
[15] S. Gollakota, F. Adib, D. Katabi, and S. Seshan, “Clearing the RF smog: Making 802.11n robust to cross-technology interference,” in Proceedings of the ACM SIGCOMM, 2011.   
[16] Y. Yan, P. Yang, X. Li, Y. Tao, L. Zhang, and L. You, “ZIMO: building cross-technology mimo to harmonize zigbee smog with wifi flash without intervention,” in Proceedings of ACM MobiCom, 2013.   
[17] S. S. Hong and S. R. Katti, “DOF: a local wireless information plane,” in Proceedings of ACM SIGCOMM, 2011.   
[18] B. Wei, W. Hu, M. Yang, and C. T. Chou, “Radio-based device-free activity recognition with radio frequency interference,” in Proceedings of ACM/IEEE IPSN, 2015.   
[19] T. Sathyan, D. Humphrey, and M. Hedley, “Wasp: A system and algorithms for accurate radio localization using low-cost hardware,” IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), 2011.   
[20] S. Rayanchu, A. Patro, and S. Banerjee, “Airshark: detecting non-wifi rf devices using commodity wifi hardware,” in Proceedings of ACM IMC, 2011.   
[21] Y. Zheng, C. Wu, K. Qian, Z. Yang, and Y. Liu, “Detecting radio frequency interference for csi measurements on cots wifi devices,” in IEEE ICC, 2017.   
[22] T. M. Taher, M. J. Misurac, J. L. LoCicero, and D. R. Ucci, “Microwave oven signal modelling,” in Proceedings of IEEE WCNC, 2008.   
[23] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Tool release: gathering 802.11 n traces with channel state information,” ACM SIGCOMM Computer Communication Review, 2011.   
[24] Y. Wang, J. Liu, Y. Chen, M. Gruteser, J. Yang, and H. Liu, “E-eyes: device-free location-oriented activity identification using fine-grained wifi signatures,” in Proceedings of ACM MobiCom, 2014.   
[25] S. Lakshmanan, S. Sanadhya, and R. Sivakumar, “On link rate adaptation in 802.11 n wlans,” in Proceedings of IEEE INFOCOM, 2011.   
[26] C. Du, H. Zeng, W. Lou, and Y. T. Hou, “On cyclostationary analysis of wifi signals for direction estimation,” in Proceedings of IEEE ICC, 2015.   
[27] K. Joshi, S. Hong, and S. Katti, “Pinpoint: Localizing interfering radios,” in Proceedings of USENIX NSDI, 2013.   
[28] C. Du, R. Zhang, W. Lou, and Y. T. Hou, “Mobtrack: Locating indoor interfering radios with a single device,” in Proceedings of IEEE INFOCOM, 2016.   
[29] L. Davies and U. Gather, “The identification of multiple outliers,” Journal of the American Statistical Association, 1993.   
[30] Y. Li, “Pilot-symbol-aided channel estimation for ofdm in wireless systems,” IEEE transactions on vehicular technology, 2000.   
[31] K. Qian, C. Wu, Z. Yang, Y. Liu, and Z. Zhou, “PADS: passive detection of moving targets with dynamic speed using phy layer information,” in Proceedings of IEEE ICPADS, 2014.   
[32] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Stpp: Spatialtemporal phase profiling-based method for relative rfid tag localization,” IEEE/ACM Transactions on Networking, 2017.   
[33] B. Fang, N. D. Lane, M. Zhang, and F. Kawsar, “Headscan: A wearable system for radio-based sensing of head and mouth-related activities,” in Proceedings of ACM/IEEE IPSN, 2016.   
[34] W. Wang, A. X. Liu, and M. Shahzad, “Gait recognition using wifi signals,” in Proceedings of ACM UbiComp, 2016.   
[35] Y. Xie, Z. Li, and M. Li, “Precise power delay profiling with commodity wifi,” in Proceedings of ACM MobiCom, 2015.   
[36] T. Yucek and H. Arslan, “A survey of spectrum sensing algorithms for cognitive radio applications,” IEEE communications surveys & tutorials, 2009.