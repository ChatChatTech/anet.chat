# Omnidirectional Coverage for Device-Free Passive Human Detection

Zimu Zhou, Student Member, IEEE, Zheng Yang, Member, IEEE, Chenshu Wu, Student Member, IEEE, Longfei Shangguan, Student Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Device-free Passive (DfP) human detection acts as a key enabler for emerging location-based services such as smart space, human-computer interaction, and asset security. A primary concern in devising scenario-tailored detecting systems is coverage of their monitoring units. While disk-like coverage facilitates topology control, simplifies deployment analysis, and is crucial for proximity-based applications, conventional monitoring units demonstrate directional coverage due to the underlying transmitter-receiver link architecture. To achieve omnidirectional coverage under such link-centric architecture, we propose the concept of omnidirectional passive human detection. The rationale is to exploit the rich multipath effect to blur the directional coverage. We harness PHY layer features to robustly capture the fine-grained multipath characteristics and virtually tune the shape of the coverage of the monitoring unit, which is previously prohibited with mere MAC layer RSSI. We design a fingerprinting scheme and a threshold-based scheme with off-the-shelf WiFi infrastructure and evaluate both schemes in typical clustered indoor scenarios. Experimental results demonstrate an average false positive of 8 percent and an average false negative of 7 percent for fingerprinting in detecting human presence in 4 directions. And both average false positive and false negative remain around 10 percent even with threshold-based methods.

Index Terms—Device-free, indoor localization, physical layer, channel state information

# 1 INTRODUCTION

HE ubiquity of wireless devices has triggered the triple Tconvergence of pervasive, context-aware and humancentric computing, where the ability to pinpoint nearby human presence plays a central role. In particular, the situation to detect or locate persons who carry no detectable devices, is termed as Device-free [1] or Passive Human Detection (PHD). Device-free detection is especially advantageous in secured region monitoring and emergency response like fire alarms. Such passive detection is also crucial in context-aware computing, due to the raising demand for differentiated quality of Location-Based Services (LBS). For instance, infrared is employed for directional human detection applications (e.g., the doors of elevators), while museum exhibitions might expect disk-like detection range to display item-specific information for visitors in all directions. Although disk-like proximity detection can be achieved by radar techniques, the expense for dedicated infrastructure hampers viability. The pervasively deployed WLAN, in contrast, holds potential for such purpose without extra cost. As an illustration, a laptop store might leverage the computers on the shelves to detect nearby customers to display their new features, and rate their popularity according to the total customer staying time.

The state-of-the-art in passive human detection varies in the underpinning infrastructure [1], [2], [3], [4], and the monitoring unit can be either a single RX (Receiver) in camera-based solutions or a TX-RX (Transmitter-Receiver) link in infrared and radio based methods. In radio-based schemes, the impact of human presence on the radio signals is correlated to certain variation of the received signals, where RSSI enjoys sheer prevalence due to its handy access [1], [3], [5]. Nevertheless, RSSI tends to be a fickle indicator [6], [7]. To compensate for its unreliability, Radio Tomographic Imaging (RTI) technique [3], [8] exploits the redundancy introduced by multiple radio links to visualize the humaninduced signal variation at the cost of dense sensor deployment. Furthermore, as the links are interweaved, failures of several links might degrade the whole system. A disk coverage unit, on the contrary, decomposes the network and is more flexible in providing high-quality detection performance only at the spots of interests.

Despite vast literature on radio-based device-free systems [1], [2], [3], [5], it is non-trivial to obtain disk-like coverage. The primary hurdle lies in the TX-RX link architecture, which naturally creates link-centric coverage. More concretely, most coverage models demonstrate boundary shapes similar to a directional ellipse along the TX-RX link [3], [5], rather than a disk centered at the RX (Fig. 1). We therefore introduce the concept of Omnidirectional Passive Human Detection (Omni-PHD), referring to the problem of realizing passive human detection with a coverage of disk-like boundary under the link-centric architecture. Besides the applicationdriven motivations for Omni-PHD, we also envision our work as an effort towards bridging the gap between the theoretical analysis of network coverage problems and practical sensor performance [9], [10], [11], as well as guidelines for sensor network monitoring [12], localization [13], etc.

![](images/2a0350538f0817da9cabf3ddbe8f152f59de1f8f92e3ed47c28d6fb8a096ee19.jpg)



Fig. 1. Omnidirectional passive human detection.

We ground Omni-PHD scheme on PHY layer features to virtually tune a more omnidirectional coverage shape. Unlike conventional RSSI-based schemes which strive to mitigate multipath effect, we exploit multipath components as signatures to reliably detect human presence and blur the linkcentric coverage. The advantages are twofold. 1) PHY layer features portray the small-scale multipath propagation, and are more sensitive to human presence. 2) The structure of PHY layer features is more temporally stable than the MAC layer RSSI, thus more resistant to background dynamics. We prototyped our scheme with commercial WiFi infrastructure.

Our main contributions are summarized as follows.

We introduce the concept of Omnidirectional Passive Human Detection (Omni-PHD), which serves as an early effort in breaking the limit of the link-centric unit architecture.   
We exploit the finer-grained subcarrier information, i.e., the channel frequency response from the PHY layer, and utilize it in the context of device-free passive human detection. Our scheme is implemented on existing WLAN infrastructure with off-the-shelf Intel 5300 Network Interface Card (NIC), requiring no extra hardware support.   
We validate our scheme in typical indoor scenarios, considering both stationary and mobile user detection. Experimental results show an average false positive of 8 percent and an average false negative of 7 percent in detecting human presence in 4 directions for fingerprinting, and around 10 percent by threshold based detection.

A preliminary conference version of this work can be found in [14], and we have experimentally verified the richness of the CFR features from another perspective, proposed a new threshold based detection method and validated its effectiveness under typical indoor scenarios.

In the rest of the paper, we first provide a preliminary in Section 2, and detail our scheme in Sections 3 and 4. Section 5 presents the performance evaluation, followed by brief discussions in Section 6. Section 7 reviews the related work, and Section 8 concludes this work.

# 2 PASSIVE HUMAN DETECTION

Passive human detection identifies the presence of a person by already deployed monitors, while the intruder carries no detectable devices. It correlates the impact of human locomotion on wireless signals with certain variations of the received signal features [1], [8]. Two major factors affect the performance of device-free passive detection: 1) the basic monitoring units, and 2) the measured signal features.

The effective detection area of each monitoring unit (termed as cell coverage) acts as a primary concern in designing scenario-tailored applications. A crucial characteristic of the cell coverage, is its boundary shape, which pictorially delineates its directivity. For instance, infrared devices possess a unidirectional cell coverage, and are commonly used in directional human detection applications (e.g., the doors of elevators). A disk-like cell coverage, in contrast, is preferable in other application scenarios as discussed in Section 1. As depicted in Fig. 1, instead of the unidirectional cell coverage W with sharp directionality along the TX-RX link, we expect omnidirectional coverage centred at RX with radius r (region of A).

![](images/b808750ab21a3e2d1deee53b7f4a54de99eb4f5357474af85ddc0eb8f5b236a4.jpg)



Fig. 2. Link-centric coverage of a monitoring unit.

Achieving omnidirectional cell coverage, though, is nontrivial in device-free detection, which leads to the omnidirectional passive human detection problem.

# 2.1 Problem Formulation

As most device-free systems employ a TX-RX link as the basic monitoring unit, the cell coverage demonstrates a link-centric property [15]. More specifically, given a fixed distance from the RX, the measured signal would undergo larger deviation from the normal profile (i.e., no intruders) with a person in the direction of the dominant paths. Since the TX-RX link sketches anisotropic propagating circumstance, the cell coverage thus tends to have sharper directionality in the direction of the dominating paths. As illustrated in Fig. 2 (Each contour represents the intruder locations where the RX experiences the same extent of RSSI variance), more rigorous analysis [16] shows that when scattering dominates, the variance of RSSI increases when the person moves closer to the TX-RX link (the left subfigure in Fig. 2). In reflection-dominant environment, however, the variance of RSSI is larger when the person locates closer to the TX or RX (the right subfigure in Fig. 2).

Therefore, the term of Omnidirectional Passive Human Detection (Omni-PHD) refers to the problem of device-free detection with a disk-like cell coverage under the linkcentric monitoring unit architectures. Two levels of detection are envisioned:

Equalized Decision: Determine whether a person presents within a near-disk region or not, with equally guaranteed confidence along all directions.   
Azimuth Distinction: Discriminate the particular azimuth of the human presence within a near-disk region, with equally guaranteed confidence along all directions.

Besides the challenges entailed by the link-centric architecture, it requires discriminative signal signatures to differ particular azimuth. Yet we consider omnidirectional passive human detection promising for the following reasons. 1) The state-of-the-art only exploits coarse MAC layer features, while the recently available PHY layer features are finergrained. 2) With fingerprinting approaches, it is possible to harness the anisotropic radio propagation to virtually tune the shape of the cell coverage.

Although we mainly focus on Equalized Decision in this paper, we also achieve reasonable results for Azimuth Distinction. Our scheme achieves below 9 percent false negative and false positive for Equalized Decision and above 75 percent direction distinction accuracy for Azimuth Distinction with only commercial WiFi infrastructure.

# 2.2 Signal Power Features

The MAC layer Received Signal Strength Indicator, (RSSI), is one of the most prevalent power features for device-free systems. As a superposition of multipath, however, RSSI is vulnerable to environmental noise, thus derailing the accuracy of cell coverage models and offering little flexibility for omnidirectional detection. Diving into the PHY layer, though, it is possible to resolve the alias versions of superposed signals.

In typical indoor scenarios, a transmitted signal propagates to the RX through multiple paths, each introducing a different time delay, amplitude attenuation, and phase shift. To distinguish individual paths from the time domain, wireless channel is portrayed as a temporal linear filter $h ( \tau )$ , known as Channel Impulse Response (CIR)

$$
h (\tau) = \sum_ {i = 1} ^ {N} | a _ {i} | \exp (- j \theta_ {i}) \delta (\tau - \tau_ {i}) \tag {1}
$$

where $a _ { i } , \theta _ { i }$ and $\tau _ { i }$ represent the amplitude, phase and time delay of the ith multipath component, respectively, and N denotes the total number of paths. $\delta ( \tau )$ is the Dirac delta function. Nevertheless, constrained by the system bandwidth, the time resolution remains at the granularity of discriminating clusters of multipath components [7].

Alternatively, in the frequency domain, modern multicarrier radio such as OFDM provides a sampled version of Channel Frequency Response (CFR) within the band of interest

$$
H (f) = [ H (f _ {1}), \dots , H (f _ {K}) ] \tag {2}
$$

where each $H ( f _ { k } )$ is a complex number depicting the amplitude and phase of the sub-carrier $f _ { k } .$ . CFR correlates with CIR by Fourier transform

$$
H (f) = F F T (h (\tau)). \tag {3}
$$

Leveraging the off-the-shelf Intel 5300 NIC with a publicly available driver as in [6], a group of CFRs on $K = 3 0$ subcarriers is exported to uplayer users in the format of Channel State Information (CSI).

In a nutshell, CSI exposes a finer-grained temporal and spectral structure of wireless links. The next section strives to extract proper features from CSI for omnidirectional passive human detection.

# 3 FEATURE EXTRACTION AND CLASSIFICATION

The rationale to obtain omnidirectional cell coverage is to exploit the rich multipath effects indoors to blur the link-centric property. For instance, a reflected path from the back of the RX might also lead to detectable variations on the received signals if one person presents there. To reliably take advantage of the multipath effect, though, we need a fine-grained and stable signal feature to distinguish the variations caused by even changes of secondary paths from those induced by background dynamics. As discussed in Section 2, conventional RSSI tends to be unstable and coarse-grained. PHY layer CSI, in contrast, possess richer distinction and therefore can reliably discriminate the effects from subordinate paths in all directions from background interferences.

Despite the literally similar requirements on signatures for PHY assisted active indoor localization and passive human detection, there is a subtle yet fundamental distinction in between, which impedes direct transplanting of the signatures adopted in the former to the latter problem. In active indoor localization, the chosen signature is expected to stay stable with all other persons’ presences in the environment except the served user’s presence. Nevertheless, it is the task for passive human detection to distinguish users nearby and those faraway. Consequently, the extracted features ought to be both 1) sensitive to human presence in the vicinity and 2) robust to external background dynamics.

For our scheme, we employ a K-dimensional vector of the amplitude histograms of CFRs as the PHY layer signature, and leverage the Earth Mover’s Distance (EMD) [17] as the metric for signature classification.

# 3.1 Sensitivity to Human Presence

As discussed in Section 2, the rationale for passive human detection is that a fraction of propagation paths would be affected due to intruder presence. In the time domain, this causes changes on the corresponding paths, which lead to the disturbance of CIR. From the frequency perspective, these changes are captured by the variation of frequency diversity, which are reflected by CFR.

Although CIR and CFR are equivalent in modeling channel responses, their amplitudes differ in sensitivity to human presence. As an illustration experiment, we collect CSIs for situations with one person presents at two spots in a conference hall (Spot 1 and 2 in Fig. 3), and also for the normal course with no one around. For each case, raw CSIs from 2000 packets are recorded, which are then transformed into CIRs and CFRs as in Section 2. Fig. 3 depicts the average CIR and CFR amplitudes in dB. As is shown, notable fluctuation of CIR locates narrowly around the 5th time index, while the deviation of CFR spans across the entire subcarrier indices. The physical underpinning is that the temporally separable multipath components twist in the frequency domain. Although human locomotion usually changes only a subset of paths, even a small portion of affected paths would significantly change the CFR amplitudes across all the subcarriers. Hence we choose CFR due to its sensitivity to human locomotion.

Furthermore, CIR features extracted from current commercial WiFi infrastructure suffer two limitations:

The 20 MHz bandwidth in 802.11 n (without channel bonding) yields a time resolution of 50 ns, while the typical indoor maximum excess delay is smaller than 500 ns [18]. Hence only the first 10 out of the 30 CIR components available are relevant to multipath. On the contrary, each component in CFR represents the amplitude and phase on one subcarrier.

The coarse TX-RX synchronization makes it hard to align the multipath components. It is common to only consider the relative delays w.r.t. the first arriving path. However, since only 30 CIR samples are exposed, it would be rather error-prone when determining the first arriving path. CFR avoids this problem as each component corresponds to a fixed subcarrier.

# 3.2 Resistance to Environmental Dynamics

Another major concern is how to derive CFR features that are resistant to irrelevant dynamics while retaining sensitive to humans in the vicinity. We mainly exploit the structure of CFR.

To identify how noise-resistant the CFR amplitude structure is, we collect three sequences of CFR amplitudes, each from 1000 packets. The first case is measured with no one around while in the second case, 3 men stroll at random in the room but keep away from the TX-RX link (3-5 m away). The third case denotes the situation where one person stands 0.5 m away from the RX (Note that although the azimuth of the person matters, the following qualitative results still hold). Fig. 4 demonstrates the density distributions of the CFR amplitudes. The upper two figures verify the stability of the CFR structures as in [19] while the uppermost and the lowermost confirm that the CFR structures would disperse in case of close obstruction. Therefore, CFR amplitudes discriminate irrelevant background unstableness from the desired local perturbation due to human locomotion, which is almost impossible with RSSI based descriptors [20].

Moreover, despite dispersing, the probability density distribution (pdf) of CFR on each subcarrier still remains discriminative. To clarify the richness of CFR amplitudes, we further measure two sets of CFRs with a person at another two spots near the RX in a stationary indoor environment. Each set consists of 500 CSIs. We plot the CFR amplitudes in dB as a two-dimensional gray scale image for each set, with the packet indices as the x axis, the 30 subcarriers as the y axis, and the corresponding amplitudes of CFR denoting the gray scale at coordinate ðx; yÞ. As illustrated in Fig. 5, the green lines in each figure highlight the variation trends of the deepest hollow in each CFR, i.e., the dominant frequency-selective fading [21] w.r.t. time, which sketches the human-induced influence on the spectrally twisted multipath components.

![](images/19c453a5172e91b7747f12eaee2a900875b079e2d018c8ec92ec4b1b880ef2e6.jpg)  
Fig. 3. Amplitude of CIR and CFR.

![](images/8bc0839d196f5c74e1da7a1b16f4cb0804279f64a5386be3a2b04215e05aece8.jpg)



![](images/101515dbd3e7f2a3c1d199486001fdbadcf2e5522ac6e8acb14346544b7632b8.jpg)



![](images/d0003b27003f8a672127f35007695db3f986dee9691bde04c79e3a0cafec160c.jpg)



Fig. 4. Pdf of CFR amplitude.

As shown in Fig. 5, the CFR fluctuation trends vary with intruders at different spots, which contributes to the distinction of CFR amplitudes. In fact, even the dominant frequency-selective fading is rather intruder location specific. The correlation coefficient of the two green lines, for instance, is as low as 0.2. However, we leave this combination of multipath-scale spectral and packet-level temporal features to future work, and only employ the histograms of CFR amplitudes. As validated in Section 5, the histograms of CFR amplitudes alone have offered adequate discrimination.

![](images/2b3f70be53bd893fbeba167383f570eb277bd490e56be5cba9b899a5dcd42f07.jpg)



![](images/f022718649916f991a687b5e18a3c59cf8d6b3d4e832ffbf156ef334fedbbf14.jpg)



Fig. 5. Temporal variation of CFR amplitude.

![](images/4f6e802c4be701ccb5ea4fd14fec6d2fc64c992134d5e5f6d159630b751b32b8.jpg)



![](images/5bd227a05a66a60eb34a7ab366476d9be90571ebf3eed07f52d8a353dddc1aad.jpg)



Fig. 6. Pdf of complex CFRs on subcarrier 04 and 30.

# 3.3 Modeling CFR Amplitude Features

Although CFR consists of both amplitude and phase information, we only adopt the amplitude of CFRs for two concerns.

Despite that phase information enriches the feature space, it needs careful calibration to mitigate dramatic phase drifts [22]. The amplitude of CFR, in contrast, remains sensitive to nearly human activities, yet pertains the spectral structures in case of external perturbation.   
According to our measurements, the phases on a portion of subcarriers distribute uniformly, which possess limited location-dependent distinction.

Fig. 6 plots the pdf of the complex CFRs measured in the third case of Fig. 4. While the complex CFRs on subcarrier 30 can be well represented by a single cluster, the complex CFRs on subcarrier 4 demonstrate a circle-like distribution, with almost uniformly distributed phases within the entire ð-; Þ range. The only difference is that the amplitudes of CFRs on subcarrier 30 spreads out to near zero values, while for subcarrier 4, the amplitudes of CFRs vary within a range relatively faraway from zero, which contributes to a circle like distribution in the complex plane.

The circle-like distribution makes it difficult to model the CFR signatures by clustering. We thus leave out the uniformly distributed phase information and employ the amplitude distribution on each subcarrier only, and model it as a histogram. Albeit simple, the histogram representation avoids the over-fitting problems induced by pdf estimation. We validate the feasibility of the histogram approach in Section 5.

To sum up, we employ the histograms of all the CFR amplitudes for a group of K accessible subcarriers as the proposed PHY layer features

$$
[ h i s t (\| H (f _ {1}) \|), \dots , h i s t (\| H (f _ {K}) \|) ] \tag {4}
$$

where $K = 3 0$ in our case, and each $h i s t ( \| H ( f _ { k } ) \| )$ is calculated within a pre-defined time window W.

# 3.4 Signature Classification

To compare the similarity between two histograms, we adopt the Earth Mover’s Distance (EMD) [17], which is a cross-bin similarity metric to calculate the distances between histograms or probability distributions. EMD is analogous to the minimal effort to transform one pile of earth into another one. In general, the EMD measures the dissimilarity between two signatures $P = \{ ( p _ { i } , u _ { i } ) \} _ { i = 1 } ^ { m }$ of size m and $Q = \mathbf { \bar { \{ } }  ( q _ { j } , v _ { j } ) \} _ { j = 1 } ^ { n }$ 1 of size n, where $u _ { i }$ and $v _ { j }$ denote the positions of the ith and jth elements in each signature, and $p _ { i }$ and $q _ { j }$ represent the corresponding weights, respectively. The EMD between $P$ and Q is then calculated as [17]

$$
E M D (P, Q) = \min _ {F = \{f _ {i j} \}} \frac {\sum_ {i , j} f _ {i j} d _ {i j}}{\sum_ {i , j} f _ {i j}} \tag {5}
$$

with the constraints

$$
\begin{array}{l} \sum_ {j} f _ {i j} \leq p _ {i}, \\ \sum_ {i} f _ {i j} \leq q _ {j}, \\ \sum_ {i, j} f _ {i j} = \min \left\{\sum_ {i} p _ {i}, \sum_ {j} q _ {j} \right\}, \\ f _ {i j} \geq 0. \\ \end{array}
$$

To compare the distance between two histograms, each histogram is regarded as a signature, for each histogram bin can be considered as an element in a signature. Accordingly, the histogram values act as the corresponding weights in the signature, while the indices of bins serve as the positions in the signature.

Since the raw CSI data reported are at the granularity of 1 dBm, and in our measurements, the fluctuation range of most CFR amplitudes on a single subcarrier is around 20 dB, we therefore set the number of bins for each histogram as 20.

We then calculate the EMD for each subcarrier before adding the K ¼ 30 EMDs into a single distance as the similarity between signatures $s _ { 1 }$ and $s _ { 2 }$ . The rationale to calculate the EMD separately for each subcarrier is to preserve the spectral structure. The final summation is due to the fact that the subcarriers in OFDM fade independently. As a consequence, each subcarrier weighs equally in calculating the total dissimilarity between the two vectors.

# 4 HUMAN DETECTION

In this section, we detail our Omni-PHD scheme. The CSI sequences reported from the RX are first converted into the amplitudes of CFRs (measured in dBm). The histograms of CFR amplitudes for K subcarriers are calculated for a set of packets within a fixed time window W.

There are two candidate methods to determine whether there is an intruder within the cell coverage: 1) Fingerprinting and 2) Threshold. We interpret the two methods separately as follows.

# 4.1 Fingerprinting Based Detection

The fingerprinting approach consists of two phases: training (a.k.a. calibration) and monitoring [23]. The first stage involves a site-survey process, in which a tuple hs; li is recorded to correlate a location l with a measured signature s. The signature for all intruder locations are measured and pre-stored in advance to construct a fingerprint database. Next during the monitoring stage, the RX measures a new signature $s _ { t }$ within a time window W and calculates the distance between $s _ { t }$ and the normal profile $S _ { o u t }$ (termed as $d ( s _ { t } , S _ { o u t } ) )$ as well as the distance between $s _ { t }$ and all the signatures $S _ { i n } = \{ s _ { i } | i \in \mathcal { T } \}$ , where

![](images/cd1ad6c293b2abc8964da2e9251c561648f7e01a83a556037cc883f16333fd71.jpg)



Fig. 7. Multipath-scarce scenario.

$$
d (s _ {t}, S _ {i n}) = \min _ {s _ {i} \in S _ {i n}} d (s _ {t}, s _ {i}). \tag {6}
$$

And I is the set of the indices for all signatures in the database with an intruder within the cell coverage. If $d ( s _ { t } , S _ { o u t } )$ is smaller than $d ( s _ { t } , S _ { i n } )$ , then a ‘detected’ event is announced. To improve the reliability of detection, we employ a sliding window approach with step size s. More specifically, if the signatures calculated for N consecutive sliding windows $\{ \breve { W _ { 1 } } , W _ { 2 } , \ldots , W _ { N } \}$ , all resembles more to the signatures with intruders, then a ‘detected’ event is announced. As for the Azimuth Distinction level, the direction (including the normal profile) with the highest similarity to the measured signature is returned as the estimated intruder’s azimuth.

# 4.2 Threshold Based Detection

Although calibration is indispensable for the Azimuth Distinction level, minimal effort of site-survey can be achieved for Equalized Detection, since only the signature for the normal profile is required. The rationale is that the impact of nearby human presence tends to be severer than that of faraway dynamics. Hence if the deviation of the measured signature exceeds a pre-defined threshold from the normal profile, it potentially indicates the presence of an intruder. More formally, the threshold $\gamma _ { i }$ for a monitoring unit i is determined as

$$
\gamma_ {i} = (1 + \delta) \cdot \max _ {k \in K} d (s _ {k}, S _ {\text { out }}) \tag {7}
$$

where  is a constant guard, and $s _ { k }$ denotes one of the K signatures measured when there is no one around in the calibration stage. Afterwards, once the deviation of a signature st measured during the operation stage exceeds $\gamma _ { i } ,$ monitoring i detects an intruder.

This threshold determination method is location-specific and environment-adaptive, and it is convenient to update the threshold in case of dramatic change of surrounding environments. As an illustration, on measuring a set of signatures for the normal profile and the relative distances calculated based on EMD for each pair of signatures, the one with the minimal summons of relative distances to all others is considered as the most representative. Therefore, it is voted as the signature for the normal profile during the consecutive monitoring stage, while the threshold is calculated by Eq. (7). Since only a little training is needed for normal profile updating, it can be conducted when the monitored area ‘ought to’ be static, such as the closed museums at night.

![](images/df19a18eba4c50cf1f36d738fba7229ff059cd04ca2e8fad69fccfe29c3592e1.jpg)



Fig. 8. Multipath-rich scenario.

# 5 PERFORMANCE

In this section, we evaluate the performance of Omni-PHD in various typical indoor scenarios, considering multipathrich environments, background dynamics and both stationary and mobile users.

# 5.1 Experiment Methodology

We employed a TP-LINK TL-WR741N wireless router as the transmitter operating in IEEE 802.11n 2.4 GHz AP mode, and a LENOVO laptop equipped with Intel 5300 NIC as the receiver downloading packets from the AP. The firmware is modified as [6] to export CSI data to upper layer. The transmission rate is 20 packets per second.

The measurements were conducted in two representative indoor scenarios: a conference hall and a small computer lab (Figs. 7, and 8). The former is relatively vacant, while the latter is piled with desks and computers, creating rather complex wireless propagating environment.

In the hall scenario, we first put the AP 2 m above the floor and on the floor, respectively, and fix the laptop 0.6 m above the floor. For each AP placement, we pick 2 different laptop locations. For the lab case, the AP is about 1.2 m above the floor, and we choose 3 laptop locations. Therefore, we measured 4 links in the hall and 3 links in the lab.

For each link, we collected data with a person in 4 directions 0.5 m and 1.0 m away from the laptop. We also recorded the case with no one around. Hence, each link has 9 testing cases.

For each of the 9 testing cases, we collected CSI for 1 minute to build the fingerprint database. To collect test samples, we measured CSI for the 9 testing cases for 30 seconds on each link, from which the CSI of 6 seconds were randomly picked as one test sample. We repeated the collection with 9 different persons at the 4 directions for both the range of 0.5 m and 1.0 m, thus obtaining 9 test samples for each intruder case. Finally, we collected 9 sets of CSI when there was no one around as the test samples for the normal profiles for each link. To identify the robustness to background dynamics, half of the test data were measured when 3 men strolled in the test room, but kept away from the TX-RX link for at least 2.5 m.

![](images/f8624b85d614218733ac915f886c4bccb10a9dac09e5d4adb99577f495b2ed0d.jpg)



![](images/52de5aeb9a9abcd491c9494d075a13d162bd9be4a6991d2445ec41dc24c7e046.jpg)



Fig. 9. FN and FP of fingerprinting based method.

The fingerprint database for each link was built up as follows. For database within coverage of radius 0.5 m, only the training data collected within 0.5 m were employed (i.e., 4 intruder cases and those for the normal profile). For the database of 1.0 m, all training data were used.

To evaluate the scheme’s realtime performance, we let one person faraway from the receiver (about 2.5 m away) walk towards the RX and then walk away again in the hall scenario.

We mainly focus on the following metrics to evaluate our detection scheme. 1) False Positive (FP): The fraction of cases where the receiver announces a ‘Detected’ event when there is no one within the disk range. 2) False Negative (FN): The fraction of cases where there is an intruder within the disk range, but the receiver fails to detect him.

Further, we employ directivity to quantify how ‘directional’ the coverage is. For instance, a monitoring unit capable of detecting intruders in all directions within a disk range of radius $r _ { 0 }$ with equal detection rate $P ,$ would hold 0 (or 1 dB) directionality. Mathematically, the directivity of a monitoring unit D at radius r is defined as

$$
D _ {r} = \frac {1}{\frac {1}{2 \pi} \int_ {0} ^ {2 \pi} p _ {r} (\theta) d \theta} \tag {8}
$$

where $p _ { r } ( \theta )$ is normalized with maximal equal to 1.

$$
p _ {r} (\theta) = \frac {P _ {r} (\theta)}{P _ {r , m a x}} \tag {9}
$$

where $P _ { r } ( \theta )$ is the detection rate in the direction of  at radius of r and $P _ { r , m a x }$ is the maximum detection rate in all directions at radius of r.

# 5.2 Detection Performance

# 5.2.1 Fingerprinting Performance

Fig. 9 shows the FP and FN of the 7 links at radius of 0.5 m and 1.0 m, respectively, with average FN/FP of 7.9 percent/

![](images/b5f98288dc7d0fd43491f608b18a1a112d73fe97877cfd381f3fb5b90c349068.jpg)



Fig. 10. Overall directional performance of fingerprinting.

4.8 percent at 0.5 m, and 6.9 percent/6.4 percent at 1.0 m. The slight rise of average FP from 0.5 m to 1.0 m is because that the farther the intruder presents to the RX, the less severe impact the received signals would undergo. As a result, some test samples might resemble more to the fingerprints at 1.0 m in the database, which contributes to a FP.

Fig. 10 demonstrates the detection rate (DR) and the direction distinction accuracy along 4 directions (denote the direction along the TX-RX link as 0 degree, and follow a clockwise direction) including both the hall and lab scenarios. The detection rates for all directions are around 90 percent, while the direction distinction accuracies reasonably range from 76 percent to 85 percent. The directivity at radius 1.0 m is $\bar { D } _ { D R , 1 \mathrm { ~ m } } \approx 0 . 1 7$ dB in terms of detection rate while $D _ { D A , 1 \mathrm { ~ m } } \approx 0 . 5 8$ dB in terms of direction distinction accuracy. The sharper directivity of direction distinction accuracy reveals that the signatures against the TX-RX link (0 degree) still holds less distinction compared with those along the TX-RX link (180 degree), which is ruled by the underlying anisotropic signal propagation. That is, when the user stands backwards the TX-RX link (0 degree of azimuth), it might be classified as other directions or the normal profile. For the Equalized Detection level, though, the differences between the normal profile and all cases when there is a user nearby is comparatively larger. Hence the CFR signature provides sufficient distinction from the normal profile, and the detection rate along each direction is comparably uniform.

Fig. 11 demonstrates the avearage FP and FN across 7 links at the radius of 1.0 m with a window size ranging from 2 seconds to 10 seconds. Both FP and FN drop gracefully with the increasing window sizes since the histograms measured within longer time intervals generally incur less random noise. On the other hand, both FP and FN retain within 10 percent even with a window size of only 2 seconds. This indicates that the fingerprinting based scheme is feasible for realtime detection as long as the intruder stays within the range for about 3 to 4 seconds (accounting for both the window size and software delays).

Fig. 12 further illustrates the detection rate and direction distinction accuracy across each direction. Again, the performance along each direction tends to be insensitive to the variation of window size. Furthermore, for direction distinction, the direction towards the TX-RX link (180 degree) still enjoys the highest classification accuracy, indicating that the coverage shape of the proposed scheme is still not perfectly omnidirectional. Finer-grained and more effective features extracted from channel responses might ultimately contribute to a perfect disk-like coverage, even for the Azimuth Distinction level.

# 5.2.2 Threshold Based Detection Performance

Fig. 13 portrays the distance distribution of signatures in the fingerprint database for the normal profile and for the 8 intruder cases along different directions. The distance is normalized by the maximal distance among the signatures in the fingerprint database for the normal profiles. The threshold to distinguish normal profiles and the cases with intruders exists for most of the measured links, especially for the multipath-rich scenario (corresponding to link indices of 7-9). This indicates that the richness of multipath does affect the intra signature dissimilarities between the normal profile and situations where there is an intruder, although it might pose less impact for fingerprinting based approach. However, the threshold based method would still be able to distinguish the intruder cases from the normal profile with high probability.

Fig. 14 shows the FN and FP for the 7 links with  ¼ 0:1. (Note that there is a tradeoff in selecting the threshold to balance FN and FP, and we leave the optimal threshold selection to futurework.)The average FN andFP are 7.9percent and 6.8 percent, respectively. The slight performance degradation of the threshold based approach indicates that a single threshold is sufficient to distinguish the normal profile and an intruder in most cases. Nevertheless, both FN and FP are above 10 percent for link 1. Therefore, the threshold based approach might be more effective in multipath-rich environment, yet at the risk of high FN and FP on certain links in multipath-sparse cases. For instance, a signature might have a smaller distance to that of the normal profile, but the distance may exceed the threshold, leading to inconsistent classification results.

![](images/7be0e77dc9819b3f896908203a91ebf97cc50c6bad934395546a506df17c814e.jpg)



![](images/1d1c101123a81552b01229450a2cbabdd07bfe4dbfbbc849ee16f60f1befe58c.jpg)



Fig. 12. Overall directional performance w.r.t. window size.

# 5.2.3 Mobile Detection Performance

Fig. 15 illustrates the detection results for a mobile user. The window size is set to 2 seconds, with a sliding step size of 0.5 seconds. At first, the measured signatures bear more resemblance to the normal profile, i.e., with smaller EMD to the signatures for the normal profile. In the time interval of 5.5 to 9.0 seconds, the distances between the measured signatures in each time window and the intruder signatures drop smaller. Therefore the RX announces a series of ‘detected’ events during this interval. The variation trends of the two sequences of EMDs demonstrate the feasibility of the proposed scheme in detecting mobile users who are approaching and walking away from the receiver for

![](images/2c96c44ecca3d3c9a642a0bfd23ef07e9c5ff1c2b1a66b1fc27a3a66e67e2a0d.jpg)



Fig. 11. Average FN and FP w.r.t. window size.

![](images/5bee6cb38ce87d2c22fbbf41daa27209d86e75c6b72b89593dcd229853b2bef3.jpg)



Fig. 13. Relative signature distribution of links.

![](images/a0c1f61ae44415915fe8f0e5bf9c4fa7ccf14d706e3c61583b74464d7477ab98.jpg)



Fig. 14. FN and FP of threshold based method.

Equalized Detection. Nevertheless, the accuracy in discriminating the direction of the mobile user is less satisfactory due to the small window size and the uncertainty induced by mobility.

# 6 DISCUSSIONS

This section discusses some limitations and possible augmentations of Omni-PHD.

# 6.1 Re-Calibration

As with all fingerprinting based approaches, re-calibration is indispensable after a long period. However, such laborintensive overhead has been eased by crowdsourcing [23], [24]. We envision such crowdsourcing solution for passive localization systems in the near future.

# 6.2 Leveraging MIMO

MIMO is a newly added feature in IEEE 802.11n. A MIMO enabled solution would possess richer information due to spatial diversity besides the frequency diversity used in our scheme. Spatial diversity has been explored in [25] as an enhancement for active localization, but not in the context of passive detection.

# 6.3 Multi-Unit Enhancement

Although experiments show that the coverage shape is not an ideal disk for a single monitoring unit, the combination of multiple TX-RX links would potentially enhance the disk-like coverage with proper placement.

# 7 RELATED WORK

Related work falls in the following three categories:

# 7.1 Device-Free Passive Systems

Device-free passive systems locate a person carrying no radio enabled devices via his impact on wireless signals [1]. Most systems employ RSSI, from either WiFi monitors [26], or ZigBee sensors [5], as an indicator for human presence. Though easy to access, RSSI proves to be unreliable since it fluctuates considerably even at a stationary link [7]. To achieve high robustness, Radio Tomographic Imaging (RTI) technique [3], [8] exploits the redundancy introduced by multiple radio links to visualize the human-induced signal variations at the cost of dense sensor deployment. Our work serves as an early scrutiny on the cell coverage shape, which provides guidelines for optimal sensor deployment.

![](images/e1260a3f7440b275de737e173f79651186261ccc7fcaa54581e32a747bc5b62d.jpg)



Fig. 15. Fingerprinting based mobile user detection.

# 7.2 Sensing Coverage Modeling

Modeling the coverage of each sensor is fundamental when analyzing network coverage for various applications [9], [10], [11]. Disk-like model is widely adopted in theoretical analysis since it simplifies the sensing coverage behavior. In practice, however, most sensing units in device-free systems demonstrate link-centric coverage [15]. Zhang et al. [5] employed an eclipse coverage centered in the middle of the TX-RX link, while Wilson et al. [3] used an oval coverage with foci at TX and RX. Patwari et al. [16] unified the two coverage shapes via a spatial model for human-induced RSSI variance. In this work, we strive to archive omnidirectional sensing coverage leveraging PHY layer information, to bridge the gap between theoretical disk-model based network coverage analysis and practical device-free system design.

# 7.3 PHY Assisted Indoor Localization

Unlike conventional MAC layer RSSI, PHY layer information, such as CIR and CFR, is capable of discriminating multipath components, and has been accessible on off-theshelf hardware [6]. This triggers a thriving trend in PHY assisted indoor localization due to its finer-grained resolution and richer information. Sen et al. [19] employed the multipath information in CFR for fingerprinting based spot localization. Wu et al. [7] extracted the power of the direct path from CIR for accurate ranging, while Sen et al. [27] transformed the body blocking effect with respect to the direct path into reliable angle information for triangulation. Xiao et al. [28] proposed a CFR-based DfP motion detection system, but did not consider its coverage shape. Our work builds upon this thread of research, yet emphasizes on the directional properties of the monitoring unit in device-free scenarios.

# 8 CONCLUSION

In this study, we demonstrate that PHY layer information unfolds new possibilities for passive human detection. Exploiting rich multipath effect indoors, we blur the linkcentric property of traditional monitoring units and explore omnidirectional cell coverage. We extract distinctive features from the small-scale spectral structures of multipath components that are sensitive to nearby human locomotion and resistant to irrelevant background dynamics. Leveraging the histograms of CSI as signatures for different directions, we propose Omni-PHD, an omnidirectional passive human detection scheme and prototype it with mere commercial WiFi infrastructure. Experiments considering the richness of multipath, background dynamics and mobility demonstrated an average false possitive of 8 percent and false negative of 7 percent in detecting human presence in 4 directions for fingerprinting, and both average false positive and false negative of around 10 percent with a singlethreshold based method. We envision this work as an early step towards passive human detection with flexible coverage, which acts as a crucial concern in human-centric computing.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program under grant No. 61190110, NSFC under grants Nos. 61171067, 61133016, and 61272466, National High-Tech R&D Program of China (863) under grant No. 2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under grant No. 61125202.

# REFERENCES

[1] M. Youssef, M. Mah, and A. Agrawala, ‘‘Challenges: Device-Free Passive Localization for Wireless Environments,’’ in Proc. ACM Int. Conf. MobiCom Netw., 2007, pp. 222-229.   
[2] Y. Liu, Y. Zhao, L. Chen, J. Pei, and J. Han, ‘‘Mining Frequent Trajectory Patterns for Activity Monitoring Using Radio Frequency Tag Arrays,’’ IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 11, pp. 2138-2149, Nov. 2012.   
[3] J. Wilson and N. Patwari, ‘‘Radio Tomographic Imaging with Wireless Networks,’’ IEEE Trans. Mobile Comput., vol. 9, no. 5, pp. 621-632, May 2010.   
[4] J. Krumm, S. Harris, B. Meyers, B. Brumitt, M. Hale, and S. Shafer, ‘‘Multi-Camera Multi-Person Tracking for Easy Living,’’ in Proc. IEEE Int. Workshop VS, 2000, pp. 3-10.   
[5] D. Zhang, J. Ma, Q. Chen, and L.M. Ni, ‘‘An RF-Based System for Tracking Transceiver-Free Objects,’’ in Proc. IEEE Int. Conf. PerCom, 2007, pp. 135-144.   
[6] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, ‘‘Predictable 802.11 Packet Delivery from Wireless Channel Measurements,’’ in Proc. ACM SIGCOMM, 2010, pp. 159-170.   
[7] K. Wu, J. Xiao, Y. Yi, M. Gao, and L.M. Ni, ‘‘FILA: Fine-Grained Indoor Localization,’’ in Proc. IEEE INFOCOM, 2012, pp. 2210-2218.   
[8] J. Wilson and N. Patwari, ‘‘See-Through Walls: Motion Tracking Using Variance-Based Radio Tomography Networks,’’ IEEE Trans. Mobile Comput., vol. 10, no. 5, pp. 612-621, May 2011.   
[9] S. Meguerdichian, F. Koushanfar, M. Potkonjak, and M.B. Srivastava, ‘‘Coverage Problems in Wireless Ad-Hoc Sensor Networks,’’ in Proc. IEEE INFOCOM, 2001, pp. 1380-1387.

[10] S. Kumar, T.H. Lai, and A. Arora, ‘‘Barrier Coverage with Wireless Sensors,’’ in Proc. ACM Int. Conf. MobiCom Netw., 2005, pp. 284-298.   
[11] R. Tan, G. Xing, B. Liu, J. Wang, and X. Jia, ‘‘Exploiting Data Fusion to Improve the Coverage of Wireless Sensor Networks,’’ IEEE/ACM Trans. Netw., vol. 20, no. 2, pp. 450-462, Apr. 2012.   
[12] D. Dong, X. Liao, Y. Liu, C. Shen, and X. Wang, ‘‘Edge Self-Monitoring for Wireless Sensor Networks,’’ IEEE Trans. Parallel Distrib. Syst., vol. 22, no. 3, pp. 514-527, Mar. 2011.   
[13] Y. Liu and Z. Yang, ‘‘Understanding Node Localizability of Wireless Ad Hoc and Sensor Networks,’’ IEEE Trans. Mobile Comput., vol. 11, no. 8, pp. 1249-1260, Aug. 2012.   
[14] Z. Zhou, Z. Yang, C. Wu, L. Shangguan, and Y. Liu, ‘‘Towards Omnidirectional Passive Human Detection,’’ in Proc. IEEE INFOCOM, 2013, pp. 3057-3065.   
[15] D. Zhang, Y. Liu, and L.M. Ni, ‘‘Link-Centric Probabilistic Coverage Model for Transceiver-Free Object Detection in Wireless Networks,’’ in Proc. IEEE ICDCS, 2010, pp. 116-125.   
[16] N. Patwari and J. Wilson, ‘‘Spatial Models for Human Motion-Induced Signal Strength Variance on Static Links,’’ IEEE Trans. Inf. Forensics Security, vol. 6, no. 3, pt. 1, pp. 791-802, Sep. 2011.   
[17] Y. Rubner, C. Tomasi, and L.J. Guibas, ‘‘The Earth Mover’s Distance as a Metric for Image Retrieval,’’ Int. J. Comput. Vis., vol. 40, no. 2, pp. 99-121, Nov. 2000.   
[18] Y. Jin, W.-S. Soh, and W.-C. Wong, ‘‘Indoor Localization with Channel Impulse Response Based Fingerprint and Nonparametric Regression,’’ IEEE Trans. Wireless Commun., vol. 9, no. 3, pp. 1120-1127, Mar. 2010.   
[19] S. Sen, B. Radunovic, R.R. Choudhury, and T. Minka, ‘‘You are Facing the Mona Lisa: Spot Localization Using PHY Layer Information,’’ in Proc. ACM Int. Conf. MobiSys, Appl., Serv., 2012, pp. 183-196.   
[20] K. Kleisouris, B. Firner, R. Howard, Y. Zhang, and R.P. Martin, ‘‘Detecting Intra-Room Mobility with Signal Strength Descriptors,’’ in Proc. ACM Int. Symp. MobiHoc Netw. Comput., 2010, pp. 71-80.   
[21] T. Rappaport, Wireless Communications: Principles and Practice, 2nd ed. Upper Saddle River, NJ, USA: Prentice-Hall, 2001.   
[22] J. Zhang, M.H. Firooz, N. Patwari, and S.K. Kasera, ‘‘Advancing Wireless Link Signatures for Location Distinction,’’ in Proc. ACM Int. Conf. MobiCom Netw., 2008, pp. 26-37.   
[23] Z. Yang, C. Wu, and Y. Liu, ‘‘Locating in Fingerprint Space: Wireless Indoor Localization with Little Human Intervention,’’ in Proc. ACM Int. Conf. MobiCom Netw., 2012, pp. 269-280.   
[24] A. Rai, K.K. Chintalapudi, V.N. Padmanabhan, and R. Sen, ‘‘Zee: Zero-Effort Crowdsourcing for Indoor Localization,’’ in Proc. ACM Int. Conf. MobiCom Netw., 2012, pp. 293-304.   
[25] J. Xiao, K. Wu, Y. Yi, and L.M. Ni, ‘‘FIFS: Fine-Grained Indoor Fingerprinting System,’’ in Proc. IEEE ICCCN, 2012, pp. 1-7.   
[26] A.E. Kosba, A. Saeed, and M. Youssef, ‘‘RASID: A Robust WLAN Device-Free Passive Motion Detection System,’’ in Proc. IEEE Int. Conf. PerCom, 2012, pp. 180-189.   
[27] S. Sen, R.R. Choudhury, and S. Nelakuditi, ‘‘SpinLoc: Spin Once to Know Your Location,’’ in Proc. ACM Workshop HotMobile Comput. Syst. Appl., 2012, pp. 1-6.   
[28] J. Xiao, K. Wu, Y. Yi, L. Wang, and L. Ni, ‘‘FIMD: Fine-Grained Device-Free Motion Detection,’’ in Proc. IEEE ICPADS, 2012, pp. 229-235.

![](images/bba7b747f48fc204eeba38cb97e8abf7bda9a3e4d8d0e57c1de760a9688a7a4c.jpg)



Zimu Zhou received the BE degree from the Department of Electronic Engineering of Tsinghua University, Beijing, China, in 2011. He is currently working toward the PhD degree in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong. His main research interests include wireless networks and mobile computing. He is a Student Member of IEEE and ACM.

![](images/53008930ef192e7dbd9835667086115a947e3217cef74b2b34a9736ffaf05d6f.jpg)



Zheng Yang received the BE degree in computer science from Tsinghua University, China, in 2006 and the PhD degree in computer science from Hong Kong University of Science and Technology, Hong Kong, in 2010. He is currently an Assistant Professor at Tsinghua University. His main research interests include wireless ad-hocnsor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/8c1da77940d57013826300539d946f1c23bb6d42043a41c95eb6b783d3e6ff0e.jpg)



Chenshu Wu received the BE degree from the School of Software, Tsinghua University, Beijing, China, in 2010. He is working toward the PhD degree in the Department of Computer Science and Technology, Tsinghua University. He is a member of Tsinghua National Lab for Information Science and Technology. His research interests include wireless ad-hocnsor networks and pervasive computing. He is a Student Member of the IEEE and a member of the ACM.

![](images/01e4554fe912aedc89d6e72da0a2948cf2f994ebe2cbf0379bb859ba140de5e7.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University East Lansing, MI, USA, in 2003 and 2004, respectively. He is now EMC Chair Professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a

Senior Member of the IEEE.

![](images/ac0b511478c043f3734c91d416ecf72e0dc3505df8971a774907c32ea490a45e.jpg)



Longfei Shangguan received the BE degree from the School of Software, Xidian University, China, in 2011. He is currently working toward the PhD degree in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include pervasive computing, wireless sensor networks and RFID system. He is a Student Member of the IEEE and a member of the ACM.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.