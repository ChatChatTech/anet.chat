# WiFi-based Indoor Line-Of-Sight Identification

Zimu Zhou, Student Member, IEEE, Zheng Yang, Member, IEEE, Chenshu Wu, Student Member, IEEE, Longfei Shangguan, Student Member, IEEE, Haibin Cai, Yunhao Liu, Fellow, IEEE and Lionel M. Ni, Fellow, IEEE

Abstract—Wireless LANs, especially WiFi, have been pervasively deployed and have fostered myriad wireless communication services and ubiquitous computing applications. A primary concern in designing these applications is to combat harsh indoor propagation environments, particularly Non-Line-Of-Sight (NLOS) propagation. The ability to identify the existence of the Line-Of-Sight (LOS) path acts as a key enabler for adaptive communication, cognitive radios, robust localization. Enabling such capability on commodity WiFi infrastructure, however, is prohibitive due to the coarse multipath resolution with MAC layer Received Signal Strength (RSS). In this work, we propose two PHY layer channel statistics based features from both the time and frequency domains. To further break away from the intrinsic bandwidth limit of WiFi, we extend to the spatial domain and harness natural mobility to magnify the randomness of NLOS paths while retaining the deterministic nature of the LOS component. We propose LiFi, a statistical LOS identification scheme with commodity WiFi infrastructure and evaluate it in typical indoor environments covering an area of $1500m^{2}$ . Experimental results demonstrate that LiFi achieves an overall LOS detection rate of 90.42% with a false alarm rate of 9.34% for the temporal feature, and an overall LOS detection rate of 93.09% with a false alarm rate of 7.29% for the spectral feature.

# I. INTRODUCTION

WIFI networks are ubiquitously deployed indoors and act as more than a vehicle for communication. Fast emerging applications, e.g., indoor localization [1], seeing through-walls [2], gesture recognition [3], are continuously revolutionizing the horizon [4]. For innovative designs to excel in multipath-dense indoor scenarios, Non-Line-Of-Sight (NLOS) propagation is a major concern. The severe and fickle attenuation of NLOS propagation deteriorates communication link quality and degrades theoretical propagation models. The past decade has witnessed extensive research to combat such phenomenon [5] [6], where the ability to identify the existence of the Line-Of-Sight (LOS) path serves as a primitive.

Numerous research domains also rely heavily on or even build upon the presence of the LOS path. For instance, NLOS propagation induces positive bias in ranging $[5]$ , and generates

Z. Zhou and L. Shangguan are with the Department of Computer Science & Engineering, Hong Kong University of Science & Technology, Hong Kong. E-mail: {zhouzimu.hk, shanggdlk}@gmail.com

Z. Yang, C. Wu and Y. Liu are with School of Software and TNList, Tsinghua University, Beijing, China.

E-mail: {yang, wu, yunhao}@greenorbs.com

H. Cai is with Shanghai Key Laboratory of Trustworthy Computing, East China Normal University, Shanghai, China.

E-mail: hbcai@sei.ecnu.edu.cn

L. M. Ni is with the Department of Computer and Information Science, University of Macau.

E-mail: ni@umac.mo

spurious angular peaks for angle estimation [7]. Even for fingerprinting-based localization, the fierce signal strength fluctuations due to multipath superposition pose substantial challenges in producing recurring radio fingerprints [1]. The availability of a clear and short-range LOS path also benefits other applications such as wireless energy harvesting by ensuring tight electromagnetic coupling and thus high charging efficiency [8]. In a nutshell, the awareness of LOS and NLOS conditions, and further disentangling the LOS component, enhances all these frameworks.

Achieving LOS/NLOS identification capability with commodity WiFi infrastructure, however, entails a range of challenges. Although vast theoretical channel models have been proposed for LOS and NLOS propagation $[9]$ , a practical LOS identification scheme either requires precise channel profiles, which involves dedicated channel sounders, or assumes abundant randomness to bring the statistical models in effect. Towards more pervasive solutions, most existing approaches either employ extremely wideband signals like Ultra WideBand (UWB) $[10]$ $[11]$ , or resort to relatively long-range communications like cellular networks $[12]$ , and often halt at simulation $[13]$ . Unfortunately, current WiFi operates with a bandwidth of only 20MHz, thus unable to resolve paths with distance difference shorter than 15m, yet often targets at inbuilding services of meter-level accuracy. Such scale mismatch of operating bandwidth and geographic space hampers direct adoption of either category of existing approaches to WiFi due to the coarse-grained channel measurements and short-range indoor propagation environments. Pioneer work $[7]$ extends to the spatial dimension leveraging Multiple-Input-Multiple-Output (MIMO) techniques, but still require hardware modification, impeding immediate viability.

In this work, we aim to design a pervasive primitive to identify the availability of the LOS path under multipath propagation with only commodity WiFi devices. Since the presence and obstruction of the LOS path are mutually exclusive, we harness the hypothesis test framework for statistical LOS identification $[12]$ . To capture the distinctions between LOS and NLOS conditions with merely off-the-shelf WiFi infrastructure, we exploit two key observations. (1) The recently exposed PHY layer information on commercial WiFi devices reveals multipath channel characteristics at the granularity of OFDM subcarriers $[14]$ , which is much finer-grained than the traditional MAC layer RSS. (2) The spatial disturbance induced by natural mobility tends to magnify the randomness of NLOS paths, while retaining the deterministic nature of the LOS path, thus facilitating LOS identification via the statistical characteristics of the received signals.

We propose a LOS identification system with commodity

WiFi infrastructure called LiFi. Leveraging the PHY layer channel state information reported by commercial WiFi-compatible Network Interface Card (NIC), we (1) eliminate irrelevant noise and NLOS paths with large delays in the time domain, and (2) exploit frequency diversity to reveal the spatial disturbances of NLOS propagation. On observing that mobility magnifies the discrepancies between LOS and NLOS paths (i.e., the LOS path remains almost the same with the receiver moves locally within a small range, while the NLOS paths may change dramatically), we involve natural receiver movement (e.g., walking with an ultrabook at hand) to enhance LOS identification. Combined with mobility, we extract representative features from both the time and the frequency domains to quantify the distinctions under LOS and NLOS conditions. Through extensive evaluation, LiFi achieves an overall LOS detection rate of 90.42% with a false alarm rate of 9.34% for the temporal feature, and an overall LOS detection rate of 93.09% with a false alarm rate of 7.29% for the spectral feature. The combination of the two features achieves LOS and NLOS identification rates around 95%. Our scheme is robust to different propagation distances, channel attenuation and blockage diversity.

The main contributions of this work are as follows:

- We exploit channel state information to identify the availability of the LOS component indoors. As far as we are aware of, this is the first LOS identification scheme built upon merely commodity WiFi infrastructure without hardware modification leveraging PHY layer information, which allows pervasive adoption.   
- We harness natural mobility to magnify the distinctions between LOS and NLOS conditions, and put LOS identification into mobile context.   
- We prototype LiFi, a pervasive LOS identification scheme and validate its performance in various indoor office environments. Experimental results demonstrate that LiFi outperforms RSS-based approaches, achieving both a LOS detection rate of 90%-95%.

A conference version of this work can be found in [15]. We omit the comprehensive evaluation of Rician-K factor feature, and propose a new feature leveraging frequency diversity. The combination of the temporal and the spectral features improves both LOS and NLOS identification rates to 95%.

In the rest of this paper, we first present the LOS identification problem and review existing approaches in Section II. We then introduce feature extraction in Section III, followed by the detailed design in Section IV and the performance evaluation in Section V. We discuss the limitations in Section VI and conclude in Section VII.

# II. THE LOS IDENTIFICATION PROBLEM

# A. Problem Definition

In indoor environments, wireless signals often propagate via multiple paths. Fig. 1 illustrates two common cases.

- The LOS path is mixed with multiple time-delayed NLOS paths.   
- The LOS path is too harshly attenuated to be perceivable against the noise floor.

![](images/21df741d061cebab5187f78468119df29648d97c08b7f8fb64d8be23f5eb2b14.jpg)



![](images/7fe57f07193cb3a66a49be934cb182b9a03c8d0ad699584af324213517c50133.jpg)



Fig. 1. Multipath propagation and LOS/NLOS conditions.

The LOS identification problem is to discern the availability of the LOS path in multipath propagation for each receiver location. It can be formulated as a binary hypothesis test with $H_{0}$ (LOS) and $H_{1}$ (NLOS) [16]. Given a generic feature $\xi$ , the conditional Probability Density Function (PDF) under the two hypotheses $p(\xi|LOS)$ and $p(\xi|NLOS)$ are applied to the classical decision theory with a likelihood ratio test:

$$
\frac {p (\xi \mid L O S)}{p (\xi \mid N L O S)} \underset {H _ {1}} {\overset {H _ {0}} {\gtrless}} \frac {P (N L O S)}{P (L O S)} \tag {1}
$$

where $P(LOS)$ and $P(NLOS)$ denote the prior probabilities of LOS and NLOS propagation. Note that LOS identification techniques can also be applied to detect NLOS conditions, yet the former emphasizes more on the accuracy of LOS identification. The selected features might slightly differ when focusing on LOS or NLOS identification.

# B. Existing Approaches

A distinctive feature $\xi$ lies in the core of LOS identification schemes. Existing approaches can be either cooperative or non-cooperative, and extract features in the time or the space domain. Cooperative NLOS identification schemes examine the consistency of multiple estimates (often location estimates) from geographically distributed transceivers [19] [20]. They achieve high accuracies given sufficient links, and are favorable in ad hoc scenarios. Our focus, however, is single-link (non-cooperative) LOS identification, where a WiFi client infers NLOS/LOS conditions by analyzing received signals from one Access Point (AP). Single-link LOS/NLOS identification schemes roughly fall into three categories, i.e., range measurement based, channel characteristics based, and antenna array based. Table I provides a brief comparison of single-link LOS identification schemes and we refer interested readers to [21] for a comprehensive survey. Channel characteristics based single-link LOS schemes exhibit reasonable trade-off between identification performance and system requirements. Hence we restrict our scope to channel characteristics based approaches.

Channel characteristics based approaches differentiate LOS and NLOS propagation via temporal channel characteristics. In theory, a multipath channel can be modeled as a linear filter, known as Channel Impulse Response (CIR) $h(\tau)$ [9]:

$$
h (\tau) = \sum_ {i = 1} ^ {N} a _ {i} e ^ {- j \theta_ {i}} \delta \left(\tau - \tau_ {i}\right) \tag {2}
$$

where $a_{i}$ , $\theta_{i}$ and $\tau_{i}$ are the amplitude, phase and time delay of the $i^{th}$ path, respectively. N is the total number of paths and $\delta(\tau)$ is the Dirac delta function. Intuitively, since the LOS path, if present, always arrives ahead of NLOS paths, the delay characteristics of received signals differ under LOS and NLOS conditions. Hence various features depicting the power-delay characteristics, i.e., the shapes of CIR, are used for LOS/NLOS conditions. Yet most commodity wireless devices fail to capture high-resolution CIRs. Researchers thus resort to analyzing the statistics of multiple received signal measurements. Table II and Table III summarize representative shape-based and statistics-based features for LOS/NLOS identification using channel characteristics, respectively. In general, shape-based features yield good performance with only one snapshot of the wireless channel, yet require precise CIR measurements. Conversely, statistics-based features are applicable to both narrow and wideband signals at the cost of multiple channel measurements.

TABLE I
A BRIEF COMPARISON OF SINGLE-LINK LOS IDENTIFICATION.

<table><tr><td>Category</td><td>Feature Domain</td><td>Example</td><td>Complexity</td><td>Performance</td></tr><tr><td>Range Measurements</td><td>Spatial/Temporal</td><td>Range Variance [12]Range Distribution [17]</td><td>Low-Medium</td><td>Fair</td></tr><tr><td>Channel Characteristics</td><td>Temporal</td><td>Variance of RSS [12]Mean Excess Delay [10]</td><td>Low-Medium</td><td>Varying</td></tr><tr><td>Antenna Array</td><td>Spatial</td><td>Angel-of-Arrival [7]Variance of Phase Difference [18]</td><td>Medium-High</td><td>Good</td></tr></table>

TABLE II
REPRESENTATIVE FEATURES FOR LOS IDENTIFICATION USING SHAPE-BASED CHANNEL CHARACTERISTICS. 

<table><tr><td>Feature</td><td>Example</td><td>Performance</td><td>Device</td></tr><tr><td rowspan="2">Delay</td><td>Mean Excess Delay [10]</td><td>74.3%-100% (Sim)</td><td>UWB</td></tr><tr><td>Delay Spread [22]</td><td>61.7%-100% (Sim)</td><td>UWB</td></tr><tr><td rowspan="2">Power</td><td>Skewness of CIR [23]</td><td>82% (Exp)</td><td>UWB</td></tr><tr><td>Kurtosis of CIR [11]</td><td>66.3%-98.4% (Sim)</td><td>UWB</td></tr></table>

Sim - Simulation, Exp - Experiment

TABLE III
REPRESENTATIVE FEATURES FOR LOS IDENTIFICATION USING STATISTICS-BASED CHANNEL CHARACTERISTICS. 

<table><tr><td>Feature</td><td>Example</td><td>Performance</td><td>Device</td></tr><tr><td rowspan="2">Model</td><td>Rician-K Factor [13]</td><td>85% (Sim)</td><td>N/W</td></tr><tr><td>γ Index [24]</td><td>N/A</td><td>UWB</td></tr><tr><td rowspan="2">Distribution</td><td>Variance of RSS [12]</td><td>N/A</td><td>N/W</td></tr><tr><td>RSS Statistics [25]</td><td>81%-87% (Exp)</td><td>WiFi</td></tr></table>

Sim - Simulation, Exp - Experiment, N/W - Narrow/Wideband

# C. Challenges

Despite vast efforts on LOS identification, it remains an open issue how to design efficient and light-weight LOS identification schemes with merely commodity WiFi infrastructure.

\- Physical Layer Information Unexplored: For decades, commercial narrowband e.g. GSM and wideband e.g. WiFi devices only report single-valued MAC layer RSS

to upper layers, thus limiting the performance of LOS identification. It is only recently that finer-grained physical layer information, i.e., Channel State Information (CSI), has been exposed on commercial WiFi infrastructure [14], which brings new opportunities for pervasive LOS identification with merely WiFi.

- Real-world Evaluation Lacking: Extensive research has focused on theoretical analysis and simulation of various UWB-based NLOS/LOS identification schemes. We argue that real-world evaluation of WiFi-based LOS identification is crucial because (1) WiFi networks are becoming increasingly popular in everyday mobile computing; (2) UWB-based schemes may not be directly adopted to the limited bandwidth of WiFi.   
- Labor-intensive Overhead: Our work is most close to [25], where the authors explore various features extracted from MAC layer RSS on WiFi devices and apply regression to select effective feature sets. Due to the learning-based feature selection and the coarse-grained MAC layer RSS, they require scenario-specific training, and the effective feature set also varies for different scenarios. In contrast, our work aims at light-weight LOS identification with PHY layer CSI, and strives to be robust to background dynamics such as moving people.

# III. MEASUREMENTS AND FEATURE EXTRACTION

In this section, we ask the following questions: (1) How do existing single-link LOS identification schemes perform on WiFi devices with PHY layer CSI? (2) How to extract proper channel characteristics based features from CSI?

# A. Channel State Information

Towards a practical LOS identification scheme with commodity WiFi infrastructure, we explore the recently available PHY layer information. Leveraging the off-the-shelf NIC and a modified driver, a sampled version of Channel Frequency Response (CFR) within WiFi bandwidth is revealed to upper layers in the format of Channel State Information (CSI) [26]. Each CSI depicts the amplitude and phase of a subcarrier:

$$
H (f _ {k}) = \| H (f _ {k}) \| e ^ {j \angle H (f _ {k})} \tag {3}
$$

where $H(f_{k})$ is the CSI at the subcarrier with central frequency $f_{k}$ , and $\angle H(f_{k})$ denotes its phase. Since CFR can be converted into CIR via Inverse Fourier Transform (IFT), an estimation of CIR with time resolution of 1/20MHz = 50ns is exposed. Compared with the MAC layer RSS, CSI portrays a finer-grained structure of wireless links.

![](images/8f2643a6f8834fa21cb2e84725b6dfb22c4d5953e891e6018d32df174117e26b.jpg)



(a) Mean Excess Delay of CIR

![](images/46faff05c42f9725fcc320276a2d76b574e6257374b9a9ccbbf98401c5fc47d3.jpg)



(b) Kurtosis of CIR

Fig. 2. CDFs of shape-based features extracted from CSI under LOS/NLOS propagation.   
![](images/1f8a2862096a2170506febaf00469af50de19d1e90af219dafe7fed0dcb91d97.jpg)



(a) An Illustration of Received Envelope Distribution

![](images/2fc6b3f445375e3633593394b44de80558235590bbec43f6ded1a1058307d44d.jpg)



(b) Distribution of Rician- $K$ Factor   
Fig. 3. An illustration of the received envelope distributions and the distributions of Rician-K factor with CSI.

# B. Measurements with CSI

Since CSI provides a sampled version of CIR, we conduct a measurement study on LOS identification using both shape-based and statistics-based channel characteristics with CSI.

1) Shape-based Features with CSI: Shape-based features exploit the difference in delay and power characteristics between LOS and NLOS propagation:

- Given a wireless link, signals transmitted via the LOS path always arrive first.   
- If unobstructed, the LOS path has weaker attenuation.

We select one delay-based feature (mean excess delay [10]) and one power-based feature (kurtosis of CIR [11]) listed in Table II. Mean excess delay $\tau_{m}$ is defined as:

$$
\tau_ {m} = \frac {\int \tau | h (\tau) | ^ {2} d \tau}{\int | h (\tau) | ^ {2} d \tau} \tag {4}
$$

where $h(\tau)$ is the CIR. Kurtosis of $\mathrm{CIR}\kappa$ is calculated as:

$$
\kappa = \frac {E \left\{\left| h (\tau) \right| - \mu_ {| h |} \right\} ^ {4}}{\sigma_ {| h |} ^ {4}} \tag {5}
$$

where $E\{\cdot\}$ represents the sampling expectation over delay. $\mu_{|h|}$ and $\sigma_{|h|}$ denote the mean and standard deviation of the CIR amplitude $|h(\tau)|$ , respectively. $\tau_{m}$ and $\kappa$ approximate the weighted average and peakedness of the received signal power delay profile, and in general, LOS conditions have a smaller $\tau_{m}$ (shorter average delay) and a larger $\kappa$ (a more sharply distributed power delay profile).

We extracted CSIs from 5000 packets measured under typical LOS and NLOS conditions, and calculated the corresponding CIRs via IFT. Fig. 2a and Fig. 2b illustrate the CDFs of the mean excess delay and kurtosis of CIR. While CIRs derived from CSI do have shorter mean excess delay and larger kurtosis, a threshold to discriminate LOS and NLOS conditions may lead to high false identification rate. This is because given a bandwidth of 20MHz, commodity WiFi yields a time resolution of 50ns. Thus paths with length difference smaller than 15m might be mixed in one CIR sample.

2) Statistics-based Features with CSI: Statistics-based features exploit the difference of LOS and NLOS propagation in the spatial domain. Signals travelling along NLOS paths tend to behave more randomly compared with those along a clear LOS path. We select one model-based feature (Rician-K factor [13]) in Table III. The received signal envelope distribution is often modeled as Rayleigh/Rician fading for NLOS/LOS dominant conditions [9]. Rician-K factor [27] is defined as the ratio of the power in the LOS component to the power in the scattered NLOS paths. A large K indicates strong LOS power and thus, a high probability of LOS propagation.

Fig. 3a plots the distributions of received envelopes and the Rician/Rayleigh fittings with filtered CSI. Although the empirical distributions are well fitted by Rician fading, Rayleigh fitting may fail for NLOS conditions. This is because Rayleigh fading assumes a large number of multipath components with roughly equal power and uniformly distributed azimuths. Yet many NLOS scenarios, such as in Fig. 1, do not match these assumptions. Fig. 3b plots the distributions of Rician-K factor using CSI. While Rician-K factors under LOS propagation are smaller, significant errors still exist. This is because (1) Rician-K factor is derived from propagation models primarily catered for long-range and scattered propagations e.g. a base station and a client at the center of Manhattan [28]; and (2)

![](images/639c22f47929d50360ce7921b87b534c06589412fffaaed8786de394d239d485.jpg)



Fig. 4. Impact of mobility on LOS/NLOS propagation.

Low Rician-K factors might occur in LOS scenarios e.g. a dominant NLOS path mixed with other diffusely scattered NLOS paths. Hence it is infeasible to directly employ Rician-K factor for LOS identification.

# C. Channel Statistics with Mobility

As shown in Section III-B1, shape-based features are infeasible due to insufficient bandwidth of WiFi. To enable LOS identification with commercial WiFi, statistics-based features compensate for the crude CIR measurements by integrating multiple observations. However, as discussed in Section III-B2, model-based metrics such as Rician-K factor still yield large errors. The main hurdle is that constrained by particular indoor floor plans and the relatively short transmission distances, the NLOS paths may not be adequately random, thus degrading the viability of theoretical models.

A key insight to induce more randomness on NLOS paths is to involve mobility. As illustrated in Fig. 4, when Receiver1 moves from $RX_{1}$ to $RX_{1}'$ , the LOS path experiences slight variation, while NLOS paths suffer notable changes in transmission distances, arriving angles, and channel attenuation. Yet in case of undeceivable LOS path, almost all paths would fluctuate considerably during Receiver2's movement from $RX_{2}$ to $RX_{2}'$ , thus creating abundant randomness. Thus we propose two distribution-based channel statistics features from both the time and the frequency domains $^{1}$ .

1) Skewness of Dominant Path Power: While mobility amplifies the fluctuation of NLOS paths, two challenges remain:

- MAC layer RSS can be noisy [5], thus inducing irrelevant variations to the LOS path.   
- In mobile indoor environments, the selected features need to be lightweight and independent on specific distribution modeling due to location changes and model degradation.

To wipe out interference when identifying the LOS path, we exploit CSI to disentangle the dominant paths to mitigate the impact of NLOS paths with long delays and noise. Concretely, we filter the CIR samples obtained from CSI as follows:

- We only keep the first 10 CIR samples. This is because given a typical indoor maximum excess delay of 500ns [29] and a time resolution of 50ns, at most 10 samples are relevant to multipath propagation.   
- We take the CIR sample with the maximum slope in the received CIR sequence (i.e., the maximum difference

$^{1}$ We refer interested readers to the conference version [15] for evaluations of distribution-based features as [25].

between two successive CIR samples) as the start of the dominant paths. Such slope based detection better captures the energy switch from noise to signals.

\- We summate over the CIR sample with the maximum slope with the next CIR sample as the power of the dominant paths. This is to account for the alignment errors due to uncertain time lag, where the CIR sample next to the first detected path may contain the LOS path as well. If the next CIR sample exceeds the indices, we simply discard this CIR sequence.

Fig. 5a plot the envelope distributions of filtered CSI from 1000 packets for a mobile link. As is shown, with mobility, the received envelope under LOS condition distributes almost symmetrically, yet exhibits a notable skew under NLOS conditions. We thus employ skewness to quantify the skewed characteristics. Mathematically, skewness s is defined as:

$$
s = \frac {E \{x - \mu \} ^ {3}}{\sigma^ {3}} \tag {6}
$$

where $x, \mu$ and $\sigma$ denote the measurement, mean, and standard deviation, respectively. Fig. 5b plots the distributions of skewness for the power of dominant paths under both LOS and NLOS propagations. (200 measurements each for LOS and NLOS propagations. 1000 packets for each measurement.) In general, the skewness feature under NLOS conditions exhibits larger positive trend and a threshold to distinguish LOS and NLOS conditions with high accuracy exists.

The skewed characteristics has been observed and modeled as a skewed Laplace distribution, but it involves prior knowledge of the propagation distance along a static link $[30]$ . Conversely, we calculate the skewness feature from filtered CSI for mobile links, which is distribution-agnostic and irrespective of propagation distances.

2) Kurtosis of Frequency Diversity Variation: The rationale to leverage frequency diversity for LOS and NLOS identification on mobile links is as follows. Assuming a constant-gain antenna, which is common for commodity WiFi hardware using e.g. monopole antennas, received power falls off as $\lambda^{2}/d^{n}$ , where $\lambda = c/f$ is the signal wavelength with speed c and frequency f, d is the transmitted distance and n is the environmental attenuation factor [9]. In LOS dominant scenarios, the channel fading is relatively flat since the LOS path dominates. Therefore, the CSIs collected from one packet are similar if normalized to the same frequency, since they transverse the same distance. Conversely, in NLOS dominant scenarios, the richer multipath superposition leads to more notable frequency-selective fading. Consequently, the CSIs measured from one packet may vary even if normalized to the same frequency. That is, we normalize the CSI amplitudes of one received packet to the central frequency $f_{0}$ :

$$
H _ {n o r m} (f _ {k}) = \frac {f _ {k}}{f _ {0}} \cdot H (f _ {k}) \tag {7}
$$

where $H(f_{k})$ and $H_{norm}(f_{k})$ are the original and normalized amplitudes of the $k^{th}$ subcarrier. $f_{k}$ is the frequency of the $k^{th}$ subcarrier $^{2}$ . We expect smaller variance of the normalized CSIs under LOS propagation because the signals transverse the same distance and experience similar attenuation.

![](images/25f04a0f4d49da7ad0a7349e54716292ac89cba67f6b70272ae5f717791a9ccd.jpg)



(a) Distribution of Filtered CSI (1000 Packets)

![](images/7df2c2482167af022d76e4bd5a5f4f8610c6aad4c5f5e048a1f06db8f9624d25.jpg)



(b) Distribution of Skewness (200 Measurements)

Fig. 5. An illustration of received envelope distributions and the distributions of skewness for dominant paths with mobility.   
![](images/9d0bb4d8750100b00c3e6914903720a9ae7a72194de7950e13eeaebea21aa598.jpg)



(a) STD of Normalized CFR (500 Packets)

![](images/5a92e37b9188fb0d30bb22051171e7f43e1fd8aaa5bf4f6a3a2ce16016346991.jpg)



(b) Distribution of Kurtosis (100 Measurements)   
Fig. 6. STD distribution of CFR amplitudes which are converted w.r.t. the central frequency, and the distribution of kurtosis of the STD distributions.

However, we find it insufficient to utilize CSI measurement of one packet for LOS identification. Significant attenuation changes by only fractions for signals even over GHz bandwidth of spectrum [31]. Thus the variation induced by frequency-selective fading may not be large enough in NLOS propagation scenarios. To further increase the variation of the normalized CSI amplitudes in NLOS conditions, we again resort to receiver mobility. In case of LOS propagation, the LOS path still travels almost the same distance with slight receiver mobility. In case of NLOS propagation, however, the NLOS paths are likely to vary dramatically, leading to diverse propagation distances for different receiver locations, even if the locations only change slightly. After involving receiver mobility, we expect the variation of normalized CSI amplitudes from multiple packets remain similar under LOS propagation yet fluctuate under NLOS propagation.

Fig. 6a plots the Standard Deviation (STD) distributions of the normalized CSI amplitudes from 500 packets. STDs under LOS propagation distribute more peaked while those under NLOS propagation demonstrate a more flat distribution.

To quantify the peaked and flat STD distributions, we adopt kurtosis as a candidate feature. Kurtosis $\kappa$ is defined as:

$$
\kappa = \frac {E \{x - \mu \} ^ {4}}{\sigma^ {4}} \tag {8}
$$

where $x, \mu$ and $\sigma$ denote the measurement, mean, and standard deviation, respectively. A large kurtosis indicates more peaked and heavy tailed distributions. Fig. 6b plots the distributions of the proposed kurtosis feature for frequency diversity variation (200 measurements each for LOS and NLOS propagations. 1000 packets for each measurement.) In general, the kurtosis feature under LOS conditions is larger than that under NLOS conditions and a threshold to distinguish LOS and NLOS conditions with high accuracy also exists.

# IV. LOS IDENTIFICATION

# A. Preprocessing

The lack of time and frequency synchronization induces phase noise when measuring the complex channel response $[32]$ . Since phase shifts in the frequency domain is equivalent to delays in the time domain, the phase noise leads to unknown time lags when calculating CIR samples from raw CSI samples. We utilize the linear revision $[32]$ to mitigate the CIR aligning errors incurred by phase noise. The revised phase is then reassembled with the amplitude as the complex CFR sample. The corresponding CIR samples are obtained via a 32-point IFFT on the CFR samples, and the skewness feature is thereafter extracted from the dominant paths as in Section III-C1. Since the kurtosis feature is derived from the amplitude of CSI, it does not involve the above phase calibration process. The amplitudes are converted to the central frequency as in Section III-C2.

![](images/398fa17f9aaf62e40afdc708ca3b60703206839360d25cfa2d1fc5d252f82fd9.jpg)



(a) Testing Building

![](images/74d77a21604c4144591bbc4c21f45d926cdc49134b4fdb90cb9dd5a0f366e502.jpg)



(b) Testing Office   
Fig. 7. Floor plans of the testing scenarios, including corridors and rooms covering an area of approximately $1500m^{2}$ .

# B. Normalization

To make the LOS identification scheme independent of the power attenuation, we normalize the CIR samples and the CSI amplitudes measured at one time by dividing them by the average amplitude, i.e., setting the mean amplitude to 1, before extracting the proposed features.

# C. Identification

Given a set of normalized CIR samples and CSI amplitudes from N packets, the skewness feature s and the kurtosis feature $\kappa$ are calculated as introduced in Section III-C1 and Section III-C2, respectively. Then LOS identification is formulated as a classical binary hypothesis test with LOS condition $H_{0}$ and NLOS condition $H_{1}$ .

For the skewness feature, the hypothesis test is:

$$
\left\{ \begin{array}{l l} H _ {0}: & s <   s _ {t h} \\ H _ {1}: & s > s _ {t h} \end{array} \right. \tag {9}
$$

For the kurtosis feature, the hypothesis test is:

$$
\left\{ \begin{array}{l l} H _ {0}: & \kappa > \kappa_ {t h} \\ H _ {1}: & \kappa <   \kappa_ {t h} \end{array} \right. \tag {10}
$$

where $s_{th}$ and $\kappa_{th}$ represent the corresponding identification threshold for the skewness and kutosis features, respectively. The thresholds are pre-calibrated and according to our measurements, a unified threshold for each feature metric would fit various scenarios including different propagation distances, channel attenuation, and blockage diversity.

# V. PERFORMANCE

In this section, we first interpret the experiment setup and the methodology, followed by detailed performance evaluation of LiFi in various indoor scenarios.

# A. Methodology

Testing Environments: We conduct the measurement campaign over one week in typical office environments including corridors and rooms, covering an area of approximately $1500m^{2}$ . The corridors are enclosed with concrete bearing walls and hollow non-bearing walls. The rooms are furnished with cubicle desks partitioned by glass and metal boards, computers, and other plastic, wooden and metallic furniture. The doors are kept open during the measurements and occasionally there are people passing by. The floor plan of the testing building is illustrated in Fig. 7a. For the corridors, we collect CSIs for LOS, through-wall and around-corner propagation with a maximum transmitter-receiver distance of 30m. For the rooms, we select a grid of 23 testing locations separated by 2m and 2 AP locations (Fig. 7b). The direct link between one transmitter and one receiver could be a clear LOS path, partially blocked by furniture and humans, or through-wall propagation, as shown in Fig. 7b. Different AP heights are also tested including 0m, 0.8m and 2m above the floor.

Data Collection: During the measurements, a TP-LINK TLWR741N wireless router is employed as the transmitter operating in IEEE 802.11n AP mode at 2.4GHz. We use two receiver setups: a LENOVO laptop equipped with Intel 5300 NIC, and a mini PC with external Intel 5300 NIC to take device diversity into consideration. The firmware is modified as in [14] and the receiver pings packets from the AP to collect CSI measurements. A group of 30 CSIs are extracted from each packet and processed as in Section IV-A.

To simulate natural human mobility, the receiver is placed on a wheeled desk of 0.8m in height, and is pushed by 2 different volunteers. For each measurement, the receiver moves randomly within the range of 1m at a speed from 0.5m/s to 2m/s. A smartphone is attached on the receiver to record acceleration traces to measure the average speeds of movements. We collect 2000 packets for each measurement, and in total we conduct 1000 measurements. For fair comparison, we also collect 1000 measurements for static links, with each measurement collected roughly along the user moving traces. Each category of measurements include 500 LOS and 500 NLOS dominant conditions. The ground truth is manually determined for each test location $^{3}$ based on whether a direct straight line exists between the transmitter and the receiver.

Evaluation Metrics: (1) LOS Detection Rate $P_{D}$ : The fraction of cases where the receiver correctly identifies a LOS condition for all LOS cases. (2) False Alarm Rate $P_{FA}$ : The fraction of cases where the receiver mistakes a NLOS condition for LOS condition for all NLOS cases.

# B. Overall Identification Performance

To evaluate the overall LOS identification performances of the two features, we plot the Receiver Operating Characteristic (ROC) curves of the two features in Fig. 8a for (1) skewness feature of static links (2) kurtosis feature of static links (3) skewness feature of mobile links (4) kurtosis feature of mobile links. ROC curves plot the LOS detection probability $P_{D}$ against the probability of false alarms $P_{FA}$ . It demonstrates the tradeoff between false positives and false negatives of a detection algorithm for a wide range of thresholds.

![](images/2af49b47e293324457c1e3a8d42892c85d4e21c400da8d59207b697b43aec5e9.jpg)



(a) ROC Curve of Skewness and Kurtosis

![](images/4645ae6aed4a6db052b454f4ccb533bd9c46d86ddcefbef04bf852b2708b8254.jpg)



(b) ROC Curver of Kurtosis

Fig. 8. Overall LOS identification performance of the skewness and kurtosis features and their combination.   
![](images/ebc3088fbc6d508f497576136384247df4b56400d6011b02414092f3abb86db9.jpg)



(a) Skewness

![](images/df6a1777b2655c6ee110492d8c18e7176809e5f90f735359641d518fea0c4163.jpg)



(b) Kurtosis   
Fig. 9. Impact of propagation distances: Both features perform better for medium propagation ranges.

Static Links vs. Mobile Links: As shown in Fig. 8a, the performance of LOS identification on mobile links notably outperforms that on static links, indicating mobility increases the spatial disturbances of NLOS paths. Mobile links are more robust to accidental disturbance since receiver motion dominates the changes of propagation paths. In contrast, static links may suffer environmental dynamics (e.g. pedestrians), thus degrading identification performance.

Skewness vs. Kurtosis: Given a constant false alarm rate of 10%, the LOS detection rates of both the skewness feature and the kurtosis feature exceed 90%. The more balanced LOS and NLOS detection rates of the skewness feature are 90.42% and 90.66%, while those for the kurtosis feature are 93.09% and 92.71%. The kurtosis feature performs slightly better than the skewness feature. A partial explanation might be that the skewness feature relies on extracting the dominant paths, which is error-prone due to lack of synchronization. However, the kurtosis feature is more sensitive to mobility, as its performance dramatically deteriorates on static links.

Combining Skewness and Kurtosis: Since LOS propagation tends to have low skewness feature and high kurtosis feature, we combine the two features and plot a linear separator using Support Vector Machine in Fig. 8b. The combination yields marginal performance gain, with the optimal LOS and NLOS detection rates of 94.36% and 95.98%.

In the following subsections, we evaluate the impact of distances, number of packets, moving speeds and different obstacles on the identification performance using the thresholds for the balanced detection rates. That is, we select the thresholds where the LOS identification rate equals to the NLOS identification rate in the ROC curves for each feature. the two hypotheses for the kurtosis feature.

# C. Impact of Propagation Distance

We collect data in the corridor with transmitter-receiver distances ranging from 5m to 30m. Fig. 9 shows the LOS detection rates and false alarm rates. There is no direct correlation between the LOS identification rates and propagation distances, indicating a single threshold may be independent of propagation distances. Overall, the kurtosis feature marginally outperforms the skewness feature. For both features, modest performance degradation, is observed for short distance (5m/10m) and relatively long distance (25m/30m). The degeneration in short distance cases is partially because the through-wall path becomes more dominant than the multipath with relatively short propagation distances. Basically, the attenuation of the wall is smaller than that suffered by NLOS due to both reflection and longer distance travelled.

# D. Impact of Packet Quantity

To evaluate the realtime performance of LiFi, we calculate the LOS and NLOS detection rate with different number of packets, ranging from 500 packets to 2000 packets per measurement. Since the receiver downloads 500 packets from the AP per second, this corresponds to a time range of 1s to 4s. As shown in Fig. 10, the LOS and NLOS detection rates of both features retain around 90% with 3 to 4 seconds of measurements. However, the kurtosis feature is more sensitive to the decrease of packet number. With 1s of measurements, its LOS detection rate drops to below 70% while the NLOS detection rate hovers around 90%, indicating a smaller threshold for more balanced detection rates. This is partially because the kurtosis feature does not filter out NLOS paths with long delays from the LOS path. Consequently, background instability and other NLOS paths (although LOS path dominates the propagation) may induce larger variation in case of insufficient packets. In contrast, the skewness feature achieves reasonable LOS and NLOS detection rates of 77.65% and 82.5%, respectively, even with measurements of only about 1s. And the degradation trends of LOS and NLOS detection rates are more consistent. In summary, since both features belong to channel statistics based features, stable estimations rely on adequate received samples, especially with mobile links, unpredictable human behaviors and uncertain background dynamics, which potentially make LOS propagation less deterministic. It suffices to yield satisfactory performance with about 3s of measurements.

![](images/352233878176e8074bd9fa53690c77f43a975f0edadae9ff6914b94d9396f6ba.jpg)



(a) Skewness

![](images/602a5c2876048f7e9c2ceffdc2b88c9f996bf20d25a3a4d4a55cbbc7bd79e9df.jpg)



(b) Kurtosis   
Fig. 10. Impact of packet number: The performances of both features remain stable with 3s-4s of measurements.

# E. Impact of Moving Speed

To evaluate the impact of moving speed, we calculate the LOS and NLOS detection rate with average speeds of 0.5m/s, 1.0m/s, 1.5m/s and 2.0m/s. As the receiver is moved by humans, we use a phone accelerometer to track receiver movements, and the volunteer listens to the beats generated by a metronome application to move the receiver back and forth at a certain speed. For each average speed, we collect 200 measurements for LOS and NLOS conditions. As shown in Fig. 11, the LOS and NLOS detection rates of both features retain around 82% for all the testing average speeds. We only notice a slight performance fall at the moving speed of 2.0m/s. The results indicate that our scheme is robust to Doppler effects. However, we fail to evaluate faster moving speeds due to the bulky receiver size. We envision CSI measurements on truly mobile devices for evaluation of the impact of Doppler effects within a wider receiver moving speed range.

# F. Impact of Obstacle Diversity

To evaluate the robustness of LiFi under different obstruction scenarios, we investigate different blockage: (1) through wall (concrete bearing walls and hollow non-bearing walls), (2) around the corners (could partially be through wall propagation) and (3) office (obstructed by metallic and wooden furniture). For each scenario, we test two AP locations as Fig. 7a and Fig. 7b, and plot the overall detection performances of the three scenarios in Fig. 12. No clear performance gap appears among the three scenarios with lowest LOS/NLOS detection rate of 85.42% for the skewness feature and 88.28% for the kurtosis feature in the 6 tested cases. The two wall cases slightly outperform the others partially because through wall propagation magnifies the difference between LOS and NLOS conditions. While even concrete bearing walls might still be insufficient to 100% block the LOS path, we expect higher NLOS detection rates for NLOS scenarios with the LOS path being completely blocked. Although furniture blockage induces weaker attenuation and disturbance on the LOS component, the relatively open space in offices compared with narrow corridors allows more freedom of the propagation paths. Hence the detection performance is comparable with the other two scenarios even with short propagation distances.

# VI. DISCUSSION

This section discusses some limitations and possible augmentations of our LiFi scheme.

Pre-calibration. Although LiFi does not involve sophisticated training, a pre-calibrated optimal is required. We demonstrate that a unified threshold fits most scenarios, except when the received packets are insufficient for stable estimation of the statistics based features. We envision more robust statistics to further reduce this overhead.

Static Links. A key for our scheme is to exploit mobility (e.g. walking) to magnify the spatial disturbances of NLOS paths. We expect finer-grained features to extend LiFi to smaller-scale motions (e.g. shaking a mobile phone in hand).

Wider Bandwidth. Wider bandwidth would linearly increase the resolution of CIR measurements, which potentially improves the performance of LOS identification. Nevertheless, even the 160MHz bandwidth might still be insufficient for precise CIR measurements to adopt shape-based features as in UWB-based schemes. Yet it may be promising to employ multiple sub-bands such as 2.4GHz and 5GHz to further distinguish LOS and NLOS in the frequency domain.

# VII. CONCLUSION

In this study, we explore PHY layer information to identify LOS conditions with WiFi. Noting that mobility magnifies the randomness of NLOS paths while retaining the deterministic nature of the LOS component, we explore channel statistics based features from both the time and the frequency domains in mobile links for LOS identification. We prototype LiFi, a statistical LOS identification scheme with off-the-shelf 802.11 NIC. Extensive evaluations show an overall LOS detection rate of 90.42% (93.09%) and a false alarm rate of 9.34% (7.29%) for the skewness (kurtosis) feature, while the combination of the two features achieves LOS and NLOS identification rates around 95%. We envision this work as an early step towards a generic, pervasive, and fine-grained channel profiling framework, which paves the way for WLAN based communication, sensing and control services in complex indoor environments.

![](images/b8d34a0a23e8756dab11459e7bc9d1c071afa4d8c357762184fd64fa60c5291a.jpg)



(a) Skewness

![](images/e12f7b71ed038dab5674169230a48f5869db3a2cbb43c1143c3eadfcaa04163b.jpg)



(b) Kurtosis

Fig. 11. Impact of moving speed: Both features retain detection accuracy of above 82% for moving speeds of 0.5m/s to 2.0m/s.   
![](images/e2db5b7807e24b8f834634fd29e6d352f933bf640de2bcd5c80de6ca2c2c8122.jpg)



(a) Skewness

![](images/029c151d149bff9db2ed64faed71e4ab8a52ce153842e1c36e4317864d23fd51.jpg)



(b) Kurtosis   
Fig. 12. Impact of obstacle diversity: Both features are agnostic to the three testing material.

# ACKNOWLEDGMENT

This research was supported in part by Hong Kong RGC Grant HKUST617212 and the NSFC under grant 61171067 and Beijing Nova Program under grant Z151100000315090.

# REFERENCES

[1] H. Liu, Y. Gan, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, “Push the Limit of WiFi based Localization for Smartphones,” in Proceedings of ACM Annual International Conference on Mobile Computing and Networking, 2012.   
[2] F. Adib and D. Katabi, “See Through Walls with Wi-Fi!” in Proceedings of ACM SIGCOMM Conference, 2013.   
[3] P. Melgarejo, X. Zhang, P. Ramanathan, and D. Chu, “Leveraging Directional Antenna Capabilities for Fine-Grained Gesture Recognition,” in Proceedings of ACM International Joint Conference on Pervasive and Ubiquitous Computing, 2014.   
[4] Z. Zhou, C. Wu, Z. Yang, and Y. Liu, “Sensorless Sensing with WiFi,” Tsinghua Science and Technology, vol. 20, no. 1, pp. 1–6, 2015.   
[5] K. Wu, J. Xiao, Y. Yi, D. Chen, X. Luo, and L. M. Ni, “CSI-Based Indoor Localization,” IEEE Transactions on Parallel and Distributed Systems, vol. 24, no. 7, pp. 1300–1309, 2013.   
[6] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Avoiding Multipath to Revive Inbuilding WiFi Localization,” in Proceedings of ACM International Conference on Mobile Systems, Applications, and Services, 2013.

[7] J. Xiong and K. Jamieson, "ArrayTrack: A Fine-Grained Indoor Location System," in Proceedings of USENIX Symposium on Networked Systems Design and Implementation, 2013.   
[8] J. Lin, “Wireless Power Transfer for Mobile Applications, and Health Effects,” IEEE Antennas and Propagation Magazine, vol. 55, no. 2, pp. 250–253, 2013.   
[9] T. Rappaport, Wireless Communications: Principles and Practice (2nd). Prentice Hall PTR, 2002.   
[10] I. Guvenc, C.-C. Chong, F. Watanabe, and H. Inamura, “NLOS Identification and Weighted Least-Squares Localization for UWB Systems using Multipath Channel Statistics,” EURASIP Journal on Advances in Signal Processing, no. 36, 2008.   
[11] L. Mucchi and P. Marcocci, “A New Parameter for UWB Indoor Channel Profile Dentification,” IEEE Transactions on Wireless Communications, vol. 8, no. 4, pp. 1597–1602, 2009.   
[12] J. Borras, P. Hatrack, and N. Mandayam, “Decision Theoretic Framework for NLOS Identification,” in Proceedings of IEEE Vehicular Technology Conference, 1998.   
[13] F. Benedetto, G. Giunta, A. Toscano, and L. Vegni, “Dynamic LOS/NLOS Statistical Discrimination of Wireless Mobile Channels,” in Proceedings of IEEE Vehicular Technology Conference, 2007.   
[14] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Tool Release: Gathering 802.11n Traces with Channel State Information,” ACM SIGCOMM Computer Communication Review, vol. 41, no. 1, p. 53, 2011.   
[15] Z. Zhou, Z. Yang, C. Wu, W. Sun, and Y. Liu, “LiFi: Line-Of-Sight Identification with WiFi,” in Proceedings of IEEE International Conference on Computer Communications, 2014.   
[16] C. Gentile, N. Alsindi, R. Raulefs, and C. Teolis, “Multipath and NLOS Mitigation Algorithms,” in Geolocation Techniques. Springer, 2013, pp. 59–97.   
[17] S. Gezici, H. Kobayashi, and H. V. Poor, “Nonparametric Non-Line-of-Sight Identification,” in Proceedings of IEEE Vehicular Technology Conference, 2003.   
[18] W. Xu, Z. Wang, and S. R. Zekavat, “Non-Line-Of-Sight Identification via Phase Difference Statistics Across Two-Antenna Elements,” IET Communications, vol. 5, no. 13, pp. 1814–1822, 2011.   
[19] L. Cong and W. Zhuang, “Nonline-of-sight Error Mitigation in Mobile Location,” IEEE Transactions on Wireless Communications, vol. 4, no. 2, pp. 560–573, 2005.   
[20] A. Conti, D. Dardari, M. Guerra, L. Mucchi, and M. Z. Win, “Experimental Characterization of Diversity Navigation,” IEEE Systems Journal, vol. 8, no. 1, pp. 115–124, 2014.   
[21] W. Xu, Z. Wang, and S. A. R. Zekavat, “An Introduction to NLOS

Identification and Localization," Handbook of Position Location: Theory, Practice, and Advances, pp. 523–555, 2011.   
[22] I. Güvenç, C.-C. Chong, F. Watanabe, and H. Inamura, “NLOS Identification and Weighted Least-Squares Localization for UWB Systems using Multipath Channel Statistics,” EURASIP Journal on Advances in Signal Processing, p. 36, 2008.   
[23] A. Abbasi and H. Liu, “Improved Line-of-Sight/Non-Line-of-Sight Classification Methods for Pulsed Ultrawideband Localisation,” IET Communications, vol. 8, no. 5, pp. 680–688, 2014.   
[24] L. Mucchi, A. Sorrentino, A. Carpini, M. Migliaccio, and G. Ferrara, “Physically-based Indicator for Identifying Ultra-Wideband Indoor Channel Condition,” IET Microwaves Antennas Propagation, vol. 8, no. 1, pp. 16–21, 2014.   
[25] Z. Xiao, H. Wen, A. Markham, N. Trigoni, P. Blunsom, and J. Frolik, "Identification and Mitigation of Non-Line-of-Sight Conditions using Received Signal Strength," in Proceedings of IEEE International Conference on Wireless and Mobile Computing Networking and Communications, 2013.   
[26] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 Packet Delivery from Wireless Channel Measurements,” in Proceedings of ACM SIGCOMM Conference, 2010.   
[27] C. Tepedelenlioglu, A. Abdi, and G. Giannakis, “The Ricean K factor: Estimation and Performance Analysis,” IEEE Transactions on Wireless Communications, vol. 2, no. 4, pp. 799–810, 2003.   
[28] D. Chizhik, J. Ling, P. Wolniansky, R. Valenzuela, N. Costa, and K. Huber, “Multiple-Input-Multiple-Output Measurements and Modeling in Manhattan,” IEEE Journal on Selected Areas in Communications, vol. 21, no. 3, pp. 321–331, 2003.   
[29] Y. Jin, W.-S. Soh, and W.-C. Wong, “Indoor Localization with Channel Impulse Response based Fingerprint and Nonparametric Regression,” IEEE Transactions on Wireless Communications, vol. 9, no. 3, pp. 1120–1127, 2010.   
[30] J. Wilson and N. Patwari, “A Fade-Level Skew-Laplace Signal Strength Model for Device-Free Localization with Wireless Networks,” IEEE Transactions on Mobile Computing, vol. 11, no. 6, pp. 947–958, 2012.   
[31] W. C. Stone, “NIST Construction Automation Program Report No. 3: Electromagnetic Signal Attenuation in Construction Materials,” Building Fire Res. Lab., Nat. Inst. Standards Technol., Gaithersburg, MD, Tech. Rep. NISTIR 6055, 1997.   
[32] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are Facing the Mona Lisa: Spot Localization using PHY Layer Information,” in Proceedings of ACM International Conference on Mobile Systems, Applications, and Services, 2012.

![](images/58580fb8433f2293012e46f1faff21535f86788edac6a6fccd44092d0706be44.jpg)



Zimu Zhou is currently a Ph.D candidate in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He received his B.E. degree in 2011 from the Department of Electronic Engineering of Tsinghua University, Beijing, China. His main research interests include wireless networks and mobile computing. He is a student member of IEEE and ACM.

![](images/36343b1ded4d67e6bc7d713e5802a723fafc3b0803164a8ff6e5b6cf526568e6.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an assistant professor in Tsinghua University. His main research interests include wireless ad-hoc sensor networking and mobile computing. He is the PI of National Natural Science Fund for Excellent Young Scientist and has been awarded the 2011 State Natural Science Award (second class).

![](images/4336ff4b4f645dd2b41cfcd01f088dec98749919a86b33a669020a428c0794ec.jpg)



Chenshu Wu received his B.E. degree in School of Software from Tsinghua University, Beijing, China, in 2010. He is now a Ph.D. student in Department of Computer Science and Technology, Tsinghua University. He is a member of Tsinghua National Lab for Information Science and Technology. His research interests include wireless ad-hocnsor networks and pervasive computing. He is a student member of the IEEE and the ACM.

![](images/ceb82a0b19f4208576ccde7109b0b0be9542eae7d66fecfb94fdfd0e16a91563.jpg)



Longfei Shangguan is currently a Ph.D candidate in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He received the B.E. degree in 2011 from Xidian University, and M.Phil degree in 2013 from Hong Kong University of Science and Technology. He is a student member of IEEE and ACM.

![](images/c8dd3c14f74fbaf69a9b50f296dad6ee884e5a6808b3a013dc7deb24d4df7dc8.jpg)



Haibin Cai is an associate professor in the Software Engineering Institute, East China Normal University. He received his Ph.D. degree from the Donghua University in 2008, Shanghai, China. He received his B.Eng. from the National University of Defense Technology in 1997, and M.S. degree from the National University of Defense Technology in 2004. His research interests include Internet of Things, Embedded Systems and Cyber-physical Systems.

![](images/d81414df1a63e8a93870f2d9f470716a924e34b2c3bcc2b4daf488ad71f97872.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is Chang Jiang Professor at School of Software and TNLIST, Tsinghua University. His research interests include wireless sensor network and RFID, peer-to-peer computing and pervasive computing. He is a fellow of the IEEE.

![](images/7afeb5e225c34bb920b87f81468fc17aa4b8effcf666ea796ede63f08c5a2f52.jpg)



papers.

Lionel M. Ni is Chair Professor in the Department of Computer and Information Science and Vice Rector of Academic Affairs at the University of Macau. Previously, he was Chair Professor of Computer Science and Engineering at the Hong Kong University of Science and Technology. He received the Ph.D. degree in electrical and computer engineering from Purdue University in 1980. A fellow of IEEE and Hong Kong Academy of Engineering Science, Dr. Ni has chaired over 30 professional conferences and has received eight awards for authoring outstanding