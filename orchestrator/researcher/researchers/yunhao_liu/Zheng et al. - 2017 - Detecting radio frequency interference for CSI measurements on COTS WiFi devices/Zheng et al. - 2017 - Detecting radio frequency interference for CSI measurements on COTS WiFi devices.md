# Detecting Radio Frequency Interference for CSI Measurements on COTS WiFi Devices

Yue Zheng∗†, Chenshu Wu∗, Kun Qian∗, Zheng Yang∗, Yunhao Liu∗, ∗School of Software and TNList, Tsinghua University †Department of Electronic Engineering, Tsinghua University

Abstract—In recent years, WiFi-based sensing applications have been proliferated due to growing capacities of the physical layer. Channel State Information (CSI), which depicts the characteristics of propagation environment and reflects different human behaviors, can be easily obtained on commodity WiFi devices with slight driver modification. For the sake of higher accuracy and robustness of CSI-based sensing, a variety of research efforts have been devoted to model refinement, algorithm optimization and data sanitization. Radio frequency interference (RFI) is a crucial problem, which, however, is surprisingly overlooked and largely unexplored. The sensing performance can be significantly boosted by identifying and properly handling the interfered CSI measurements. In this paper, we demonstrate that it is feasible to identify the interfered CSI measurements due to the unique properties induced by RFI. We propose two RFI detection algorithms by utilizing cyclostationary analysis from different angles. Experimental results on off-the-shelf WiFi devices show that both algorithms are robustly stable for different scenarios and can achieve a remarkable overall accuracy of > 90%.

# I. INTRODUCTION

There are a variety of wireless networks that play different roles in our lives. WiFi is one of the most significant and widely used wireless communication technology, and its infrastructure has been pervasively deployed in the world wide, especially indoor environment. Although WiFi is mainly utilized to transmit data, its potentials for sensing have been dramatically enhanced since Channel State Information (CSI) becomes available on commodity off-the-shelf (COTS) WiFi devices [1]. As fine-grained PHY layer information, CSI captures both amplitude and phase information for wireless channels, and depicts the characteristics of multipath propagation induced by environmental dynamics such as human behaviors. Due to such favourable features, CSI-based sensing applications have been emerging in a large number, such as indoor localization [2], activity classification [3], human presence detection [4], fall detection [5], sleep monitoring [6], walking direction estimation [7] and interactive exergames [8].

To promote the accuracy and robustness of CSI-based sensing, vast research efforts focus on refining models [3], [7], optimizing algorithms [5], [9] as well as sanitizing raw CSI data mixed with random noises [10], [11]. Nevertheless, radio frequency interference (RFI), a common but crucial problem to wireless signals, is surprisingly overlooked in the hot literature.

WiFi signals typically operate in the 2.4 GHz ISM radio band. As other types of devices (e.g., Bluetooth, ZigBee nodes, microwave oven, cordless telephone and baby monitor) also occupy the same unlicensed spectrum, WiFi usually suffers severe cross-technology interference (CTI) in addition to cochannel and adjacent channel interference. Thanks to effective error detection schemes [12], WiFi packets can still be correctly decoded as long as CTI does not emit too high power signals. However, the reported CSI suffers strong distortion [13] and therefore significantly degrades the performance of CSI-based sensing applications.

To the best of our knowledge, the only relevant work that takes RFI into consideration for CSI-based sensing [13] merely applies a noise-resistant classification algorithm to tolerate interference when performing activity recognition. The algorithm does not generalize well to other kinds of sensing applications since it does not deal with the interfered CSI measurements directly. Actually, if the interfered CSI measurements can be distinguished from those without interference in advance, the sensing performance will be boosted significantly by properly handing the distorted CSI.

In this paper, we aim to detect RFI for each CSI measurement directly for general purpose sensing applications. Note that our work is different from previous work [14] which designs elaborate framework to detect the existence of non-WiFi devices with a group of CSI measurements. Based on in-depth understanding of the impacts induced by RFI on CSI, we propose two effective algorithms by leveraging cyclostationary analysis from different perspectives. Specifically, we mainly focus on cross-technology RFI, leaving co-channel and adjacent channel interference to future work. And we will use the terms RFI and CTI interchangeably in this paper.

Cyclostationary analysis is widely used to capture the intrinsic repeating patterns of wireless communication signals. Prior works utilize the unique cyclostationarity of different signals to implement signal type classification [15], interference localization [16], [17] and spectrum occupancy estimation [15]. They all require raw signal samples as inputs and operate only on specialized hardware like USRPs. On commodity WiFi devices, however, only CSI can be obtained, which does not embody the information of transmitted wireless signals. The key insight of our work is that interfered CSI, different from the interference-free CSI, will exhibit underlying patterns due to the impacts of CTI. Specifically, the cyclostationary properties of the RFI signals would not be completely wiped out from CSI. Therefore, cyclostationary analysis is also applicable with CSI as inputs.

Treating one CSI measurement as the frequency-domain form of channel impulse responses which might be mixed with interference, we first propose an efficient and robust algorithm based on the Spectral Correlation Function (SCF) [18] to detect RFI. We exploit the gradient matrices of derived SCF amplitude to differentiate SCF with and without interference.

Examining CSI from a different point of view, we observe that interfered CSI manifests different intrinsic properties when simply regarded as a temporal sequence of data. The main rationale lies in that both amplitude and phase of CSI might suffer abrupt and significant distortion at the subcarriers corresponding to the working channel of CTI. In contrast, the amplitude and phase vary in a relatively smooth and continuous manner when no CTI exists. On this basis, we develop another effective algorithm which utilizes Cyclic Autocorrelation Function (CAF) [18] of CSI vectors for RFI detection. The algorithm works by characterizing the distinctive visionbased features of the calculated CAF amplitude matrix.

To validate the effectiveness of the two proposed algorithms, we conduct real world experiments on COTS WiFi devices. Results demonstrate that both algorithms yield remarkable overall detection accuracy of > 90%. Furthermore, both perform well in various scenarios, including diverse interference types, static/dynamic environments without/with human movements, various distances between the devices. To conclude, the proposed algorithms effectively detect RFI for CSI measurements. We believe the output knowledge of interference existence acts as essential inputs for designing practical CSIbased sensing, regardless of the specific applications.

The rest of the paper is organized as follows. In Section II, we provide preliminary analysis on CSI measurements with interference. Then we present two interference detection algorithms in Section III. The performance evaluation is provided in Section IV. And we conclude our work in Section V.

# II. UNDERSTANDING CSI WITH INTERFERENCE

# A. CSI Measurements on COTS WiFi Devices

With slight driver modification [19], commodity WiFi devices can provide CSI which is recorded for each received packet. The reported CSI is the sampled version of channel response in time-frequency space. In Orthogonal Frequency Division Multiplex (OFDM) based transmission schemes (e.g., IEEE 802.11 a/g/n), CSI is collected in the format of a complex vector, depicting both the gain and phase information of the subcarriers between each single transmit-receive antenna pair. Suppose that there are N subcarriers in an OFDM symbol, then CSI can be expressed as:

$$
H = \left[ H (0), H (1), \dots , H (k), \dots , H (N - 1) \right] ^ {T}, k \in [ 0, N - 1 ] \tag {1}
$$

Each subcarrier H(k) is defined as:

$$
H (k) = | H (k) | e ^ {j (\angle H (k))} \tag {2}
$$

Although a 20/40 MHz channel consists of 56/114 subcarriers in the IEEE 802.11n standard, COTS devices (e.g., Intel 5300 NIC) report CSI with only 30 subcarriers that spread evenly in the channel. Nevertheless, such CSI measurements are sufficient to capture the properties of wireless channels (i.e. frequency-selective fading) [19], and therefore widely used in wireless sensing [2]–[8].

![](images/cc16d59ce5dd674e5e8ef96fad40e0db6f4fee18c6b030c39a0a1545b1e1bd34.jpg)



(a) Amplitude of CSI

![](images/85ca2af4a2d6261a21f06e3a0c478b349ea370a6c07ae0099d6d284081285ef1.jpg)



(b) Phase of CSI   
Figure 1. CSI measured by COTS WiFi NICs

# B. CSI Measurements with Interference

As the unlicensed wireless spectrum is shared by numerous devices of different protocols, WiFi signals usually suffer severe radio frequency interference. Especially, WiFi is exposed to various cross-technology interferences (e.g., Bluetooth, Zig-Bee and microwave ovens).

With the vigorous development of smart space, quantities of ZigBee and Bluetooth devices are widely deployed. Both of them operate in the 2.4 GHz ISM band and their channels overlap with WiFi channels. The bandwidth of ZigBee signals is 2 MHz. Bluetooth and BLE (Bluetooth low energy) occupy 1 MHz and 2 MHz, respectively. In addition, microwave ovens which are prevalent in typical environments such as homes, offices and various public indoor spaces also share the 2.4 GHz radio band.

Suppose that there is a wireless access point sending out OFDM beacons to a laptop. An interference source is also working and its channel overlaps with the WiFi channel. Then CSI is estimated at the receiver as:

$$
\hat {H} = \frac {Y + Y _ {i n t}}{X} \tag {3}
$$

where X and Y denote the transmitted and received WiFi signal respectively, as well as $Y _ { i n t }$ denotes the interfering radio. All the terms above are the frequency version.

Denote the channel frequency responses corresponding to the WiFi signal and interference as H and $H _ { i n t }$ . Then Eqn. (3) can be expressed as:

$$
\hat {H} = H + \frac {H _ {i n t} X _ {i n t}}{X} \tag {4}
$$

where $X _ { i n t }$ indicates the transmitted data of the interference. As Fig. 1a and Fig. 1b illustrate, the subcarriers which correspond to the working channel of the interference will be impacted provided that the interference power is high enough. In terms of the amplitude, there is a narrow and extremely high peak at the affected subcarriers. The corresponding phase, which has been sanitized by a linear transformation [20] to mitigate the random phase offsets induced by packet detection delay, sampling frequency offset and central frequency offset [10], is also distorted.

The severe impacts induced by CTI will definitely degrade the performance of both wireless communication and CSIbased sensing applications. In order to improve communication quality, advanced techniques which can deal with CTI have been developed [21], [22]. In the hot literature of WiFibased sensing, however, the impacts of CTI on CSI has not been paid adequate attention or properly handled yet. To boost the reliability and sensibility of the sensing applications, it is necessary to detect CTI for CSI measurements and identify the eroded ones for further processing.

# III. RFI DETECTION FOR CSI

In this section, we propose two algorithms that are able to detect cross-technology interference accurately by applying cyclostationary analysis in different ways.

# A. Cyclostationary Analysis

Cyclostationary analysis is widely utilized to capture the intrinsic repeating patterns of wireless signals in different physical layers.

Specifically, define the Cyclic Autocorrelation Function (CAF) as follows [18] :

$$
R _ {x} ^ {\alpha} (\tau) \triangleq \lim _ {T \rightarrow \infty} \frac {1}{T} \int_ {- \frac {T}{2}} ^ {\frac {T}{2}} x (t + \frac {\tau}{2}) x ^ {*} (t - \frac {\tau}{2}) e ^ {- j 2 \pi \alpha t} d t \tag {5}
$$

With an appropriate time delay τ , the above function will exhibit a high value since the patterns in $x ( t )$ are aligned [15]. α is called cyclic frequency and it determines the frequency at which the hidden pattern repeats. The value of cyclic frequency depends on the bandwidth, carrier frequency, frame structure and other properties of the signal [15], [23]. And different kinds of signals manifest distinctive cyclic frequencies.

Usually, it’s more efficient to use the frequency version, i.e., Spectral Correlation Function (SCF) rather than CAF in OFDM-based transmission schemes. Then SCF can be computed directly:

$$
S _ {x} ^ {\alpha} [ k ] = \frac {1}{L} \sum_ {l = 0} ^ {L - 1} X _ {l} [ k ] X _ {l} ^ {*} [ k - \alpha ] \tag {6}
$$

$X _ { l } [ k ]$ is the Fourier transform of the received signal during the lth time window:

$$
X _ {l} [ k ] = \sum_ {n = N l} ^ {N l + N - 1} x [ n ] e ^ {\frac {- j 2 \pi n k}{N}} \tag {7}
$$

where N denotes the total number of subcarriers in a single OFDM symbol.

By treating a CSI measurement on COTS devices differently, we can apply SCF on it by using it as frequencydomain input or employ CAF by using it as time-domain input. As a result, we devise two different algorithms as below to implement RFI detection.

# B. SCF-based Algorithm

When there is no radio frequency interference, CSI measurements provided by COTS WiFi devices only capture how propagation environment changes but does not embody the information of the WiFi signal. However, the intrinsic properties of CSI will change when CTI exists.

![](images/c42053bf4d66fe57fbe2c112c1342c48c1804d2b63f459d520b22436c1d2304c.jpg)



(a) SCF without interference

![](images/af9006f9450c915b0a9cc5245e9bc346f0bd284cfa0d698c28e7e5e518f25331.jpg)



(b) SCF with interference   
Figure 2. SCF corresponding to CSI without/with interference

As Eqn. (4) shows, there will be an additional part $\frac { H _ { i n t } X _ { i n t } } { X }$ in distorted CSI measurements. WiFi signal X and the interfering radio $X _ { i n t }$ from a heterogeneous wireless network exhibit different repeating patterns. Thus there is underlying periodicity in $\frac { H _ { i n t } \dot { X } _ { i n t } } { X }$ even if $X _ { i n t }$ is divided by X, which contributes to the cyclostationarity of distorted CSI. Especially, the cyclostationarity is mainly induced by the interfering radio when CTI refers to Bluetooth or ZigBee. Due to the narrow bandwidth of $X _ { i n t }$ , pilot-induced cyclostationarity of WiFi [23] can hardly be depicted in such scenarios. Although another typical interference source, microwave signal, does not possess cyclostationary properties, distorted CSI still exhibits underlying periodicity. Microwave ovens sweep the radio frequency band when working. As one CSI measurement corresponds to a sufficiently short time, only several subcarriers will be distorted by the microwave signal. And cyclostationary analysis is applicable for depicting the underlying patterns induced by the distorted subcarriers.

To apply cyclostationary analysis with CSI, we can replace $X _ { l } [ k ]$ in Eqn. (6) with $H _ { l } [ k ]$ to calculate SCF:

$$
S _ {h} ^ {\alpha} [ k ] = \frac {1}{L} \sum_ {l = 0} ^ {L - 1} H _ {l} [ k ] H _ {l} ^ {*} [ k - \alpha ] \tag {8}
$$

where L refers to the total number of OFDM symbols in a packet. On commodity WiFi devices, CSI is estimated during the packet preamble and considered to be constant during the whole packet. Therefore, SCF and CSI is in one-to-one correspondence and Eqn. (8) can be revised as:

$$
S _ {h} ^ {\alpha} [ k ] = H [ k ] H ^ {*} [ k - \alpha ] \tag {9}
$$

As Fig. 2a shows, the amplitude of SCF corresponding to CSI without interference does not exhibit much higher values at certain cyclic frequencies and varies a small range. In contrast, there are drastic peaks in Fig. 2b, which indicates the cyclostationary properties of distorted CSI measurements.

In order to discriminate the two categories of SCF, it is not feasible to simply select a threshold value for the peaks. The main reason is that absolute threshold based methods depend on scenario-tailored parameters and are susceptible to environment uncertainties.

Note that the amplitude of SCF varies drastically at certain coordinates and the corresponding gradient is much higher when there is an interfering radio. On the contrary, the gradient will be within a small range as the amplitude of SCF without interference changes rather smoothly. Thus the gradient matrices are a good choice to depict intrinsic properties of SCF.

![](images/3eaf7f84959be6b30c9dab765383efe92017fe64526fde1f1f5b2a1fda8f6429.jpg)



(a) CAF without interference

![](images/21312896e9f179d744d4d21ffbde30cba47c4c2aec0548f13466289d3019b5d2.jpg)



(b) CAF with interference   
Figure 3. CAF of CSI without/with interference

We apply Singular Value Decomposition (SVD) on the gradient matrices and choose the highest singular value as an effective feature as it characterizes the distribution of gradient. For SCF of CSI with interference, the max singular value is much higher. Thus we can adopt an appropriate threshold to determine whether the corresponding CSI is affected by CTI.

To improve the robustness of the algorithm, we use normalized CSI to obtain the feature and determine the threshold. As a relative metric, the threshold applies to different scenarios and different interference types.

Although it would be difficult to differentiate two types of CTI simply based on Eqn. (9), we argue that inferring the existence of CTI is sufficient for most CSI-based sensing applications [3], [13]. Besides, some signals (e.g., Bluetooth) adopt frequency hopping mechanism during data transmission. They can be further distinguished from those who work on a predefined channel by investigating the indices of peaks in SCF amplitude matrix.

# C. CAF-based Algorithm

In this section, we investigate the properties of CSI from another point of view.

First suppose that there is no CTI working yet. Each CSI measurement can be simply regarded as a normal sequence of complex numbers with both amplitude and phase varying in a relatively continuous manner over different subcarriers as Fig. 1a and Fig. 1b illustrate. We attempt to utilize Eqn. (5) to discover the implicit characteristics of such data series:

$$
R _ {H} ^ {\alpha} (m) = \sum_ {k = 0} ^ {N - 1} H [ k ] H ^ {*} [ k - m ] e ^ {- j 2 \pi \alpha k} \tag {10}
$$

As CAF has two independent variables m (time delay) and α (cyclic frequency), the amplitude of CAF can be considered as a two-dimensional image. Fig. 3a shows that there is regular texture that looks similar to concentric circles when α ranges from -1 to 0 with step 0.01. Such periodical pattern is resistant to environment dynamics (e.g., human movements) as the continuity of CSI still preserves.

However, the existence of $\frac { H _ { i n t } X _ { i n t } } { X }$ will result in abrupt changes for both the amplitude and phase of CSI when there is an interfering radio. As the continuity is destroyed, the implicit nature of the sequence also changes. The amplitude of CAF is shown in Fig. 3b. It is clear that the texture becomes more complicated and irregular. Note that the texture is not invariable as both the indices and quantity of affected subcarriers might change with different interference sources.

Therefore, in order to differentiate two categories of CAF, we should select a vision-based approach which is able to extract texture features and depict the patterns of the two matrices. In the light of the above, we choose the Energy of the Grey-Level Co-occurrence Matrix (GLCM) [24] derived from the CAF amplitude matrix as the feature.

GLCM, also called Gray-Tone Spatial-Dependence Matrix, depicts how often different combinations of pixel grey levels occur in an image [24] and is widely used in texture analysis. GLCM has many statistical parameters that embody different properties of the texture, e.g., energy, entropy, contrast, variance, correlation and inverse difference moment. Among them, energy meausres textural uniformity, i.e., pixel pairs repetitions [25] and is suitable for capturing the patterns in CAF.

The value of energy ranges from 0 to 1. When the gray level distribution of the image has a periodic form (e.g., Fig. 3a), the value of energy will be much higher. Thus we can select an appropriate threshold for energy to determine whether the corresponding CSI is distorted by CTI.

The above algorithm mainly deals with the problem of detecting RFI for CSI measurements rather than characterizing interference types. It can be further improved in future work.

# IV. PERFORMANCE EVALUATION

# A. Experimental Methodology

We conduct experiments in a classroom (12m 7.2m) equipped with desks and chairs. A mini-desktop and a laptop are deployed as the WiFi transmitter and receiver respectively. Both are equipped with an Intel 5300 NIC as well as one antenna, and run Ubuntu 12.04 OS. With the CSI Tool [19] installed, the transmitter injects 1000 packets per second on channel 7 (2.442 GHz) and the receiver collects CSI. RFI sources include a pair of ZigBee nodes with CC2420 radio chips working on 2.440 GHz, a Bluetooth wireless speaker and a microwave oven. The ZigBee node injects 100 packets per second and each packet lasts around 4 ms.

An Agilent N9340B Handheld Spectrum Analyzer with a frequency range from 100 kHz to 3 GHz is used to indicate whether RFI exists during certain time interval. However, the ground truth of whether one CSI measurement is impacted by RFI cannot be obtained, as not each measurement will be distorted when the interference source is working. The reasons are twofold. One is the transmission rate difference between two kinds of signals. The other is that data preamble corresponds to a sufficiently short time and might stagger the interfering radio.

In spite of above reasons, it is probable that at least a certain number of CSI measurements are distorted during a time period when RFI exists. Thus a heuristic approach is adopted to derive the ground truth. We use a time window (0.5s) of CSI measurements as a basic detection unit. All the units measured with CTI working are marked as interfered. And we label those measured without the existence of CTI as interference-free. To accommodate the unit labels, only when a sufficient number of CSI measurements in a unit are detected to be with interference by the algorithm will the unit be judged as interfered (positive). Otherwise, the unit is determined to be interference-free (negative).

![](images/4d40d84ec74d4422da038c25d2a1a994ced1b0e12e8ff67396656102ceb1bb59.jpg)



Figure 4. Threshold in SCF-based algorithm

![](images/62c0db16419d70bfde8e42f45e9d3d6f221cdd72ae997ccae6b3f5a483f36db7.jpg)



Figure 5. Threshold in CAF-based algorithm

![](images/b46562bc1894efc0f8c5be18980ad89fbd3ce77d0e209792c5d4b5a6d91b774a.jpg)



Figure 6. Detection in static scenarios

![](images/d11154abfeb6ad2132f64f6d7da47e9bba4d16fe5492214c800216bc3608d5ec.jpg)



Figure 7. Detection in dynamic scenarios

![](images/64b782c9b640fadb7a999a22aab18cd4c2716bef857d62ee8ad80def2ef3c60f.jpg)



Figure 8. Impacts of RFI-Rx distance

![](images/2d31afdb462a37d06eafda75dd4d6945de8575f3ed5b422608e69f76a5ed2f28.jpg)



Figure 9. Impacts of Tx-Rx distance

# B. Performance of RFI Detection

1) Evaluation Metric: Two metrics are selected to evaluate the performance of the two algorithms.

• True Positive (TP) Rate: TP rate is the percentage that interference is correctly detected when RFI exists.   
• True Negative (TN) Rate: TN rate is the percentage that CSI is correctly classified as interference-free when no CTI works.

2) Threshold Selection: For both RFI detection algorithms, an appropriate threshold is required for the corresponding feature. Thus before evaluating the performance of RFI detection, we need to train the thresholds with a small data set. The training set is collected in following scenarios: (1) Bluetooth working (2) microwave oven working (3) ZigBee working (4) all of the above interferences working (5) no CTI working. The WiFi receiver is located 3m away from the transmitter. Bluetooth and ZigBee sources are placed 1m away from the receiver. As the microwave oven emits high RF signals, CSI measurements can hardly be collected if it is too close to the WiFi link. Thus it is placed 5m away. To evaluate the robustness of the thresholds later, we collect data in both static and dynamic (a person walking in the classroom) environments for above scenarios. Totally, there are 240 (30 4 2) positive units and 240 negative units in the training set.

As Fig. 4 and Fig. 5 illustrate, both TP rate and TN rate achieve a sufficiently high value (> 90%) with a properly selected threshold for each algorithm. Yet the performance is not sensitive to threshold selection. For later evaluation, 0.13 and 0.38 are chosen as the threshold used in the SCF-based method and CAF-based method, respectively.

3) Impact of Interference Type: Now we analyze whether interference type will influence the performance of proposed algorithms. We collect 80 units of CSI for each scenario that is listed in the previous subsection. Fig. 6 shows the performance of detection in static scenarios by utilizing two algorithms individually. B, M, Z denote Bluetooth, microwave oven and ZigBee, respectively. And BMZ refers to the case when all of them are working. Actually, TN rate has no relation with the interference type and approaches over 95% for both two algorithms. TP rate is relatively low when Bluetooth or the microwave oven is working. As Bluetooth adopts frequency hopping mechanism, it might work at a channel which does not overlap with the WiFi channel. Such problem also occurs when the microwave oven is working because it sweeps frequency band rather than work at fixed frequency. Besides, the high power of the microwave signal results in higher packet losses. Thus the CSI measurements that are strongly distorted cannot be collected. Due to above reasons, the number of the distorted measurements in a detection unit might decrease, which leads to a lower TP rate.   
4) Impact of Environmental Dynamics: Compare Fig. 7 with Fig. 6, and we find that TN rate decreases a little when RFI detection is performed in dynamic environment. Human movements result in more complicated propagation environment. And the transmitter might also adjusts signal power to accommodate with environmental dynamics. Thus CSI could be unstable sometimes and false alarm arises. In practice, the performance of the proposed algorithms can be further improved by adopting different thresholds in dynamic scenarios, which can be easily and confidently inferred by undistorted CSI measurements [26].   
5) Impact of RFI-Rx Distance: As we do not know the location of the interference usually, it is necessary to evaluate the robustness of proposed algorithms when RFI-Rx distance varies. Considering the stability and controllability of CTI, ZigBee is chosen as the interference source. RFI-Rx ranges

from 1m to 4m and Tx-Rx distance is still 3m. 80 units of CSI are collected for each scenario.

Fig. 8 shows that TP rate decreases dramatically when RFI is located 4m away from the receiver no matter which algorithm is used. Note that the power of received interfering radio will be much lower when RFI is located too far. Therefore, the additional part $\frac { H _ { i n t } X _ { i n t } } { X }$ in Eqn. (4) can be hardly depicted in CSI, which results in the decrease of TP rate. As RFI exerts little impact on CSI measurements in such case, the performance of CSI-based sensing applications can hardly be influenced by interference.

6) Impact of Tx-Rx Distance: We also investigate whether Tx-Rx distance will influence the performance of proposed algorithms. ZigBee is employed as the interference and placed 1m away from the receiver. The WiFi transmitter is placed 1m, 2m, 3m or 4m away from the receiver.

When Tx-Rx distance falls to 1m, TP rate decreases sharply. The main reason is similar to that illustrated in previous subsection. If the transmitter is sufficiently close to the receiver, received WiFi signal Y will be of high power and might conceal the interfering radio $Y _ { i n t }$ . Then impacts induced by CTI can be barely depicted in CSI according to Eqn. (3).

7) Performance Comparison: Finally, we compare the performance of two proposed algorithms. Although the CAFbased algorithm outperforms the SCF-based algorithm in specific scenarios (see Fig. 6 and Fig. 7), there is tiny difference between two algorithms’ detection accuracy which equals to T P +T N with a balanced data set. Regardless of interference $\textstyle { \frac { T P + T N } { 2 } }$ 2 type and human movements, the detection accuracy of SCFbased algorithm is 91.8% and that of CAF-based algorithm is 95.3%. However, the SCF-based algorithm has the property of low time complexity as it does not need to calculate a summation formula as the CAF-based algorithm does. Thus both algorithms have unique advantages and can be adopted to detect RFI for CSI measurements effectively.

# V. CONCLUSIONS

Although vast research efforts have been devoted to improve the performance of WiFi sensing from different angles, a crucial problem of RFI is surprisingly overlooked and needs to be explored. In order to avoid performance degradation of CSIbased sensing applications, an essential approach is identifying the CSI measurement strongly distorted by RFI beforehand. In this paper, we propose two algorithms which detect RFI for each CSI measurement by applying cyclostationary analysis in different ways. We conduct real world experiments on COTS WiFi devices to validate the effectiveness and robustness of RFI detection. The overall detection accuracy of both algorithms achieve over 90%. For future work, we will take cochannel and adjacent channel interference into consideration, as well as design elaborate schemes for later processing before feeding CSI into sensing applications.

# ACKNOWLEDGMENTS

This work is supported in part by the NSFC under grant 61522110, 61602381, 61672319, 61632008 and National Key Research Plan under grant No.2016YFC0700100.

# REFERENCES

[1] Z. Yang, Z. Zhou, and Y. Liu, “From RSSI to CSI: Indoor localization via channel response,” ACM Computing Survey, 2013.   
[2] M. Kotaru, K. Joshi, D. Bharadia, and S. Katti, “Spotfi: Decimeter level localization using wifi,” in Proceedings of ACM SIGCOMM, 2015.   
[3] W. Wang, A. X. Liu, M. Shahzad, K. Ling, and S. Lu, “Understanding and modeling of wifi signal based human activity recognition,” in Proceedings of ACM MobiCom, 2015.   
[4] C. Wu, Z. Yang, Z. Zhou, X. Liu, Y. Liu, and J. Cao, “Non-invasive detection of moving and stationary human with wifi,” IEEE Journal on Selected Areas in Communications, 2015.   
[5] H. Wang, D. Zhang, Y. Wang, J. Ma, Y. Wang, and S. Li, “Rt-fall: A real-time and contactless fall detection system with commodity wifi devices,” IEEE Transactions on Mobile Computing, 2016.   
[6] X. Liu, J. Cao, S. Tang, and J. Wen, “Wi-sleep: Contactless sleep monitoring via wifi signals,” in Proceedings of IEEE RTSS, 2014.   
[7] D. Wu, D. Zhang, C. Xu, Y. Wang, and H. Wang, “Widir: walking direction estimation using wireless signals,” in Proceedings of ACM Ubicomp, 2016.   
[8] K. Qian, C. Wu, Z. Zhou, Y. Zheng, Z. Yang, and Y. Liu, “Inferring motion direction using commodity wi-fi for interactive exergames,” in Proceedings of ACM CHI, 2017.   
[9] J. Wang, H. Jiang, J. Xiong, K. Jamieson, X. Chen, D. Fang, and B. Xie, “LiFS: Low human-effort device-free localization with finegrained subcarrier information,” in Proceedings of ACM MobiCom, 2016.   
[10] Y. Xie, Z. Li, and M. Li, “Precise power delay profiling with commodity wifi,” in Proceedings of ACM MobiCom, 2015.   
[11] B. Fang, N. D. Lane, M. Zhang, and F. Kawsar, “Headscan: A wearable system for radio-based sensing of head and mouth-related activities,” in Proceedings of ACM/IEEE IPSN, 2016.   
[12] H. Liu, H. Ma, M. El Zarki, and S. Gupta, “Error control schemes for networks: An overview,” Mobile Networks and Applications, 1997.   
[13] B. Wei, W. Hu, M. Yang, and C. T. Chou, “Radio-based device-free activity recognition with radio frequency interference,” in Proceedings of ACM/IEEE IPSN, 2015.   
[14] S. Rayanchu, A. Patro, and S. Banerjee, “Airshark: detecting non-wifi rf devices using commodity wifi hardware,” in Proceedings of ACM IMC, 2011.   
[15] S. S. Hong and S. R. Katti, “DOF: a local wireless information plane,” in Proceedings of ACM SIGCOMM, 2011.   
[16] C. Du, R. Zhang, W. Lou, and Y. T. Hou, “Mobtrack: Locating indoor interfering radios with a single device,” in Proceedings of IEEE INFOCOM, 2016.   
[17] K. Joshi, S. Hong, and S. Katti, “Pinpoint: Localizing interfering radios,” in Proceedings of USENIX NSDI, 2013.   
[18] W. A. Gardner, “Exploitation of spectral redundancy in cyclostationary signals,” IEEE Signal Processing Magazine, 1991.   
[19] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Tool release: gathering 802.11 n traces with channel state information,” ACM SIGCOMM Computer Communication Review, 2011.   
[20] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are facing the mona lisa: spot localization using phy layer information,” in Proceedings of ACM Mobisys, 2012.   
[21] S. Gollakota, F. Adib, D. Katabi, and S. Seshan, “Clearing the RF smog: Making 802.11n robust to cross-technology interference,” in Proceedings of ACM SIGCOMM, 2011.   
[22] Y. Yan, P. Yang, X. Li, Y. Tao, L. Zhang, and L. You, “ZIMO: building cross-technology mimo to harmonize zigbee smog with wifi flash without intervention,” in Proceedings of ACM MobiCom, 2013.   
[23] C. Du, H. Zeng, W. Lou, and Y. T. Hou, “On cyclostationary analysis of wifi signals for direction estimation,” in Proceedings of IEEE ICC, 2015.   
[24] R. M. Haralick, K. Shanmugam et al., “Textural features for image classification,” IEEE Transactions on systems, man, and cybernetics, 1973.   
[25] A. Baraldi and F. Parmiggiani, “An investigation of the textural characteristics associated with gray level cooccurrence matrix statistical parameters,” IEEE Transactions on Geoscience and Remote Sensing, 1995.   
[26] K. Qian, C. Wu, Z. Yang, Y. Liu, and Z. Zhou, “PADS: passive detection of moving targets with dynamic speed using phy layer information,” in Proceedings of IEEE ICPADS, 2014.