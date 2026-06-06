# Towards Omnidirectional Passive Human Detection

Zimu Zhou $^{*†}$ , Zheng Yang $^{*†}$ , Chenshu Wu $^{\dagger}$ , Longfei Shangguan $^{*†}$ , and Yunhao Liu $^{*†}$

\*CSE, Hong Kong University of Science and Technology

$^{\dagger}$ School of Software and TNList, Tsinghua University

{zhouzimu, yang, wu, shangguanlongfei, yunhao}@greenorbs.com

Abstract—Passive human detection and localization serve as key enablers for various pervasive applications such as smart space, human-computer interaction and asset security. The primary concern in devising scenario-tailored detecting systems is the coverage of their monitoring units. In conventional radiobased schemes, the basic unit tends to demonstrate a directional coverage, even if the underlying devices are all equipped with omnidirectional antennas. Such an inconsistency stems from the link-centric architecture, creating an anisotropic wireless propagating environment. To achieve an omnidirectional coverage while retaining the link-centric architecture, we propose the concept of Omnidirectional Passive Human Detection, and investigate to harness the PHY layer features to virtually tune the shape of the unit coverage by fingerprinting approaches, which is previously prohibited with mere MAC layer RSSI. We design the scheme with ubiquitously deployed WiFi infrastructure and evaluate it in typical multipath-rich indoor scenarios. Experimental results show that our scheme achieves an average false positive of 8% and an average false negative of 7% in detecting human presence in 4 directions.

# I. INTRODUCTION

The ubiquity of wireless devices has triggered the triple convergence of pervasive, context-aware and human-centric computing, where the ability to detect nearby human presence plays a central role in various scenario-tailored applications. Particularly, the situation where the person carries no devices, is termed as Device-free [1] or Passive Human Detection (PHD). Device-free detection is especially advantageous in secured region monitoring and emergency response like fire alarms. Such passive detecting manner is also crucial in context-aware computing, due to the raising demand for differentiated quality of location-based services (LBS). For instance, infrared devices are commonly employed for directional human detection applications (e.g. the doors of elevators), while museum exhibitions might expect disk detection range so as to display item-specific information for surrounded visitors in all directions. Although disk-like proximity detection can be achieved by radar based techniques, the expense for the dedicated infrastructure hampers viability. The pervasively deployed WLAN, in contrast, also holds potential for such purpose without extra cost. As an illustration, a laptop store might exploit the computers on the shelves to detect nearby customers in order to display their new properties, while simultaneously rating the computers' popularity according to the total customer staying time.

The state-of-the-art in passive human detection varies in the underpinning infrastructure [1] [2] [3] [4] [5], and the monitoring unit can be either a single RX in camera-based solutions or a TX-RX link in infrared and radio based methods. In radio-based schemes, the impact of human presence on the radio signals is correlated to certain variation of the received signals, where RSSI enjoys sheer prevalence due to its handy accessibility $[1]$ $[3]$ $[6]$ . Nevertheless, RSSI tends to be a fickle indicator. To compensate for its unreliability, Wilson et al. $[3]$ proposed the Radio Tomographic Imaging (RTI), which embraces the redundancy introduced by dense-deployed sensors to visualize the human induced RSSI attenuations. However, as the links are interweaved to create a redundant network to ensure performance, failures of several links might degrade the whole system. A disk coverage unit, on the contrary, potentially decomposes the network and is more flexible in providing high-quality detection performance only at the spots of interests.

Despite vast literature on radio-based passive human detection and localization [1] [2] [3] [6], it is non-trivial to obtain a disk detection coverage. The primary hurdle lies in the transmitter-receiver (TX-RX) link architecture, which naturally demonstrates a link-centric coverage. More concretely, most experimentally fitted coverage models for passive human detection tend to have boundary shapes similar to a directional ellipse along the TX-RX link [3] [6], rather than a disk centered at the RX (Fig. 1). We therefore introduce the concept of Omnidirectional Passive Human Detection (Omni-PHD), in referring to the problem of realizing passive human detection with a coverage of disk-like boundary, by employing link-centric detecting unit architectures. Besides the application-driven motivations for Omni-PHD, we also envision our work as an effort towards bridging the gap between the theoretical analysis of coverage problems in wireless sensor networks (WSN) and the practical hardware performances [7] [8] [9], as well as guidelines for applications such as monitoring [10] localization [11], data collection [12], topology analysis [13], etc.

We ground our Omni-PHD scheme on the fine-grained PHY layer features to virtually tune the coverage shape into a more omnidirectional one by fingerprinting the signatures within the coverage. The advantages are twofold. On the one hand, the PHY layer features portray the small-scale multi-path components, and are more sensitive to human presence. On the other hand, the structure of PHY layer signatures is more temporally stable than the MAC layer RSSI, thus possessing stronger resistance to background dynamics. Unlike conventional RSSI-based schemes which strive to mitigate the rich multipath effects indoors, we exploit the multipath components as signatures to detect human presence in a reliable and omnidirectional manner. Our scheme is prototyped with existing WiFi infrastructure leveraging the off-the-shelf Intel 5300 NIC. Experimental results show both average false positive and false negative along 4 directions of below 9% by fingerprinting, and around 10% by threshold based detection. Our main contributions are summarized as follows.

- We introduce the concept of Omnidirectional Passive Human Detection (Omni-PHD), which serves as an early effort in breaking the limit of the link-centric unit architecture.   
- We exploit the finer-grained subcarrier information, i.e., the channel frequency response from the PHY layer, and utilize it in the context of device-free passive human detection. Our scheme is implemented on existing WLAN infrastructure with off-the-shelf Intel 5300 NIC, requiring no extra hardware support.   
- We validate our scheme in various indoor scenarios, including a vacant conference hall and a clustered computer laboratory, and consider both stationary presence and mobile user detection. Experimental results show an average false positive of 8% and an average false negative of 7% in detecting human presence in 4 directions.

In the rest of the paper, we first provide a preliminary in Section II, and detail our scheme in Section III and IV. Section V presents the performance evaluation, Section VI discusses the related work, and Section VII concludes this work.

# II. PRELIMINARIES

Passive human detection refers to identifying the presence of a person by already deployed monitors, while the intruder carries no detectable devices. It usually correlates the variations of certain signal features measured at a single or a set of fixed receivers with the environmental changes due to human locomotion [1]. Two factors significantly affect the performance of device-free passive detection: (1) the basic monitoring units, and (2) the measured signal features.

The primary concern in devising scenario-tailored applications is the coverage of the underlying monitoring units, which is denoted as cell coverage. A crucial characteristic of the cell coverage, is its boundary shape, which pictorially delineates the directivity of the cell coverage. For instance, infrared devices naturally possess a unidirectional cell coverage, and are commonly used in directional human detection applications (e.g. the doors of elevators). However, a disk-like cell coverage is preferable in other application scenarios. That is, as depicted in Fig. 1, instead of the unidirectional cell coverage $\Omega$ with sharp directionality along the TX-RX link, we expect an omnidirectional coverage centred at RX with radius r, like the region of A.

Achieving omnidirectional cell coverage, though, is non-trivial in the context of device-free detection, which leads to the omnidirectional passive human detection problem.

![](images/6b549e9c8dd507a894968a19bda83241a8dae503e969267bfd6c7ab314668149.jpg)



Fig. 1. The Omnidirectional Passive Human Detection Problem

# A. The Omnidirectional Passive Human Detection Problem

In the literature of radio-based device-free passive human detection, most cell coverage models for monitoring units are experimentally fitted, and vary in directivity, even if the underlying devices are equipped with omnidirectional antennas [3] [6]. This phenomenon stems from the link-centric monitoring unit architecture and the passive nature of human induced impact on wireless signals.

More specifically, given a fixed distance from the RX, the measured signal would undergo larger deviation from the normal profile with human obstruction in the direction of the dominant paths (the paths with less attenuation). The human body, though, acts as a near-constant signal absorber at a specific location. Therefore, with human as the passive source for signal deviation, while the TX-RX link sketches the anisotropic propagating circumstance, the cell coverage for omnidirectional devices tends to demonstrate sharper directionality in the direction of the dominating paths.

Therefore, the term of omnidirectional passive human detection refers to the problem of device-free detection with a disk-like cell coverage, by employing link-centric monitoring unit architectures with only omnidirectional devices. Two levels of detection are envisioned:

- Equalized Decision: Determine whether a person presents within a near-disk region or not, with equally guaranteed confidence along all directions.   
- Azimuth Distinction: Discriminate the particular azimuth of the human presence within a near-disk region, with equally guaranteed confidence along all directions.

Besides the challenges entailed by the link-centric architecture and the passive source nature, it poses strict discriminative requirements on the signal signatures to distinguish particular azimuth. Yet we still consider omnidirectional passive human detection promising for the following reasons. (1) Recent advances in communication communities have shed light upon extracting fine-grained and robust signatures from the PHY layer, while the state-of-the-art exploits the coarse MAC layer features. (2) With fingerprinting approaches, it is possible to harness the anisotropic radio propagation circumstances to virtually tune the shape of the cell coverage instead of avoiding the multipath effects.

Although we mainly focus on Equalized Decision in this paper, we also achieve reasonable results for Azimuth Distinction. As detailed in Section V, our scheme achieves below 9% false negative and false positive for Equalized Decision and above

75% direction distinction accuracy for Azimuth Distinction. However, we defer more comprehensive studies of the Azimuth Distinction level in future work.

# B. Signal Power Features

Before closing this section, we concisely review the available signal features on a commercial receiver.

RSSI dominates in current device-free detection schemes, yet acts as a fickle power feature. As a superposition of multipath, it yields limited resistance to environmental noise, thus derailing the accuracy of cell coverage models and offering little flexibility for omnidirectional detection. Diving into the PHY layer, though, it is possible to resolve the alias versions of superposed signals.

In typical indoor scenarios, a transmitted signal propagates to the receiver through multiple paths, each introducing a different time delay, amplitude attenuation, and phase shift. To distinguish individual paths from the time domain, wireless channel is portrayed as a temporal linear filter $h(\tau)$ , known as Channel Impulse Response (CIR).

$$
h (\tau) = \sum_ {i = 1} ^ {N} | a _ {i} | \exp (- j \theta_ {i}) \delta (\tau - \tau_ {i}) \tag {1}
$$

where $a_{i}$ , $\theta_{i}$ and $\tau_{i}$ represent the amplitude, phase and time delay of the $i^{th}$ multipath component, respectively, and N denotes the total number of paths. $\delta(\tau)$ is the Dirac delta function. Nevertheless, constrained by the system bandwidth, the time resolution remains at the granularity of discriminating clusters of multipath components [14].

Alternatively, in the frequency domain, modern multi-carrier radio such as OFDM provides a sampled version of Channel Frequency Response (CFR) within the band of interest.

$$
H (f) = \left[ H (f _ {1}),..., H (f _ {K}) \right] \tag {2}
$$

where each $H(f_{k})$ is a complex number depicting the amplitude and phase of the sub-carrier $f_{k}$ . CFR correlates with CIR by Fourier transform:

$$
H (f) = F F T (h (\tau)) \tag {3}
$$

Leveraging the off-the-shelf Intel 5300 NIC with a publicly available driver as in [15], a group of CFRs on K = 30 subcarriers is exported to uplayer users in the format of Channel State Information (CSI).

In a nutshell, channel response exposes a finer-grained temporal and spectral structure of wireless links. The next section strives to extract proper features from channel response information for omnidirectional passive human detection.

# III. FEATURE EXTRACTION AND CLASSIFICATION

Recently, there is an increasing interest in fingerprinting based indoor localization with PHY layer information $[16]$ $[17]$ . Despite the literally similar requirements on signatures for conventional indoor localization and passive human detection, there is a subtle yet fundamental distinction in between, which impedes direct transplanting of the signatures adopted in the former to the latter problem.

![](images/3b57b75f733105f7c7008c2628ddb36ff4285e6a89a6d9cc1b861660041c8a53.jpg)



![](images/25a70f15589eecbe054bd6375f17cad4a53928e90ebfdc819d07e6d532c52e7a.jpg)



Fig. 2. Amplitude of CIR and CFR

In indoor localization, the chosen signature is expected to stay stable with all other persons' presences in the environment except the served user's presence. Nevertheless, it is the task for passive human detection to distinguish users near the receiver and those faraway. Consequently, the extracted features ought to be both (1) sensitive to human presence in the vicinity and (2) robust to external background dynamics.

The above two requirements are the basis for our omnidirectional passive detection scheme. The omnidirectional coverage is further enhanced by the rich multipath effects indoors, which sort of blur the link-centric property. For instance, a reflected path from the back of the RX might also lead to detectable variations on the received signals if one person presents there. Nevertheless, RSSI features tend to be unreliable and coarse-grained, thus unable to distinguish such variations from background dynamics. PHY layer features, in contrast, naturally possess richer distinction and therefore are capable of reliably discriminating variations induced by even subordinate paths in all directions from background interferences.

For our scheme, we employ a $K$ -dimensional vector of the amplitude histograms of CFRs as the PHY layer signature, and leverage the Earth Mover's Distance (EMD) [18] as the metric for signature classification.

# A. Sensitivity to Human Presence

As discussed in Section II, the rationale for passive human detection is that a fraction of propagating paths would be affected due to intruder presence. In the time domain, this contributes to changes on the corresponding paths, which are portrayed as the disturbances of CIR. From the frequency perspective, these changes are captured by the variations of frequency diversity, which are reflected by CFR.

Although CIR and CFR are equivalent in modeling channel responses, their amplitudes differ in sensitivity to human presence. We collect CSIs for situations with one person presents at two spots in a conference hall (Spot 1 and 2 in Fig. 2), and also for the normal course with no one around. For each case, raw CSIs from 2000 packets are recorded, which are then transformed into CIRs and CFRs as in Section II. Fig. 2 depicts the average CIR and CFR amplitudes in dB. As is shown, notable fluctuations of CIR locate narrowly around the $5^{th}$ time index, while the deviations of CFR span across the entire subcarrier indices. The physical underpinning is that the temporally separable multipath components twist in the frequency domain. Although human locomotion usually changes only a subset of paths, even a small portion of affected paths would significantly change the CFR amplitudes across all the subcarriers, since an impulse function $\delta(\tau)$ contributes to a constant across the entire frequency range. Hence CFR is more preferable in passive human detection due to its sensitivity to human locomotion.

![](images/08c40bb1c5a3a28bf006ba6c2c3c441093e5546c2fcfb10498bdbd0a05019a17.jpg)



![](images/f13556eeadea314a8b86faf7f6f718a67b41fa444b0c2975b3808dcb7b9dbd00.jpg)



![](images/2d3283b8da4f81a5b86a06a8b13a6f54393c8e78ee0e9a8c068e1be8dd212b1f.jpg)



Fig. 3. Density Distributions of CFR Amplitude

Furthermore, CIR features extracted from current commercial WiFi infrastructure suffer two limitations:

- The 20MHz bandwidth in 802.11n yields a time resolution of 50ns, while the typical indoor maximum excess delay is smaller than 500ns [19]. Hence only the first 10 out of the 30 available CIR components are relevant to multipath effects. Instead, each component in CFR represents the amplitude and phase on one subcarrier.   
- The lack of TX-RX synchronization makes it difficult to align the multipath components w.r.t. the first arriving path. CFR naturally avoids this problem as each component corresponds to a fixed subcarrier.

# B. Resistance to Environmental Dynamics

Another major concern for passive human detection is how to derive CFR features that are resistant to irrelevant dynamics while retaining sensitive to humans in the vicinity. And we mainly exploit the structure of CFR.

To identify the CFR amplitude structure's resistance to environmental noise, we collect three sequences of CFR amplitudes, each derived from 1000 packets. The first case is measured with no one around while in the second case, 3 men stroll at random in the room but keep away from the TX-RX link (3-5m away). The third case denotes the situation where one person stands 0.5m away from the RX (Note that although the azimuth of the person matters, the following qualitative results still hold). Fig. 3 demonstrates the density distributions of the CFR amplitudes. The upper two figures verify the stability of the CFR structures as in [17] while the uppermost and the lowermost confirm that the CFR structures would disperse in case of close obstruction. Therefore, the amplitudes of CFRs discriminate the irrelevant background unstableness from the desired local perturbations due to human locomotion, which is almost impossible with RSSI based descriptors [20].

Moreover, despite dispersing, the probability density distribution (pdf) of CFR on each subcarrier still acts as a discriminative signature. As validated in Section V, the histograms of CFR amplitudes alone have offered adequate discrimination for both the Equalized Detection and Azimuth Distinction levels of omnidirectional detection.

# C. Modeling CFR Amplitude Features

Although CFR consists of both amplitude and phase information, we only adopt the amplitude of CFRs for two concerns.

- Despite that phase information enriches the feature space, it needs careful calibration to mitigate dramatic drifts due to external noise [21]. The amplitude of CFR, in contrast, remains sensitive to human activities in the vicinity, yet pertains the spectral structures in case of external perturbation.   
- According to our measurements, the phases on a portion of subcarriers tend to be uniformly distributed, which possess limited location-dependent distinctions.

Fig. 4 demonstrates the pdf of the complex CFRs measured in the third case of Fig. 3. While the complex CFRs on subcarrier 30 can be well represented by a single cluster, the complex CFRs on subcarrier 4 demonstrate a circle-like distribution, with almost uniformly distributed phases within the entire $(- \pi, \pi)$ range. The only difference is that the amplitudes of CFRs on subcarrier 30 spreads out to near zero values, while for subcarrier 4, the amplitudes of CFRs vary within a range relatively faraway from zero, which contributes to a circle like distribution in the complex plane.

The circle-like distribution makes it difficult to model the CFR signatures by clustering. We thus leave out the uniformly distributed phase information and employ the amplitude distribution on each subcarrier only, and model it as a histogram. Albeit simple, the histogram representation avoids the overfitting problems induced by pdf estimation. We validate the feasibility of the histogram approach in Section V.

![](images/4d126a63bc176d10d8c6de45636614a17cb2dbca413ee3c5c25a83fdc9154126.jpg)



![](images/60fcd26e430974a114c2513b873cb5a5721d897ddef357cd708715c02ce20f3b.jpg)



Fig. 4. PDF of the Complex CFRs on Subcarrier 04 and 30

To sum up, we employ the histograms of all the CFR amplitudes for a group of K accessible subcarriers $\overrightarrow{hist}(\|H(f)\|)$ as the proposed PHY layer features:

$$
\overrightarrow {h i s t} (\| H (f) \|) = [ h i s t (\| H (f _ {1}) \|), \dots , h i s t (\| H (f _ {K}) \|) ] \tag {4}
$$

where K = 30 in our case, and each $hist(\|H(f_{k})\|)$ is calculated within a pre-defined time window W.

# D. Signature Classification

In comparing the similarity between two histograms, we adopt the Earth Mover's Distance (EMD) [18], which is a cross-bin similarity metric to calculate the distances between histograms or probability distributions. EMD is analogous to the minimal effort to transform one pile of earth into another one. In general, the EMD measures the dissimilarity between two signatures $P = \{(p_i, u_i)\}_{i=1}^m$ of size m and $Q = \{(q_j, v_j)\}_{j=1}^n$ of size n, where $u_i$ and $v_j$ denote the positions of the $i^{th}$ and $j^{th}$ elements in each signature, and $p_i$ and $q_j$ represent the corresponding weights, respectively. The EMD between P and Q is then calculated as [18]:

$$
E M D (P, Q) = \min _ {F = \{f _ {i j} \}} \frac {\sum_ {i , j} f _ {i j} d _ {i j}}{\sum_ {i , j} f _ {i j}} \tag {5}
$$

with the constraints:

$$
\sum_ {j} f _ {i j} \leq p _ {i},
$$

$$
\sum_ {i} f _ {i j} \leq q _ {j},
$$

$$
\sum_ {i, j} f _ {i j} = \min \left\{\sum_ {i} p _ {i}, \sum_ {j} q _ {j} \right\},
$$

$$
f _ {i j} \geq 0
$$

To compare the distance between two histograms, each histogram is regarded as a signature, for each histogram bin can be considered as an element in a signature. Accordingly, the histogram values act as the corresponding weights in the signature, while the indices of bins serve as the positions in the signature.

Since the raw CSI data reported are at the granularity of 1dBm (equivalent to the precision of 1dB when comparing the differences between two amplitudes), the number of bins to calculate the histograms is also set to ensure the granularity of 1dB. In our measurements, the fluctuation range of most CFR amplitudes on a single subcarrier is around 20dB, we therefore set the number of bins for each histogram as 20.

We then calculate the EMD for each subcarrier before adding the K = 30 EMDs into a single distance as the similarity between signatures $s_{1}$ and $s_{2}$ . The rationale to calculate the EMD separately for each subcarrier is to preserve the spectral structure. The final summation is due to the fact that the subcarriers in OFDM fade independently. As a consequence, each subcarrier weighs equally in calculating the total dissimilarity between the two vectors.

# IV. HUMAN DETECTION

In this section, we detail our Omni-PHD scheme. The CSI sequences reported from the RX are first converted into the amplitudes of CFRs (measured in dBm). The histograms of CFR amplitudes for K subcarriers are calculated for a set of packets within a fixed time window W.

To determine whether there is an intruder within the cell coverage, we adopt the prevalent fingerprinting based approach in literature of indoor localization.

The fingerprinting approach consists of two phases: training (a.k.a. calibration) and monitoring [22]. The first stage involves a site-survey process, in which a tuple $\langle s,l\rangle$ is recorded to correlate a location $l$ with a measured signature $s$ . The signature for all intruder locations are measured and pre-stored in advance to construct a fingerprint database. Next during the monitoring stage, the RX measures a new signature $s_t$ within a time window $W$ and calculates the distance between $s_t$ and the normal profile $S_{out}$ (termed as $d(s_t,S_{out})$ ) as well as the distance between $s_t$ and all the signatures $S_{in} = \{s_i|i\in \mathcal{I}\}$ , where

$$
d (s _ {t}, S _ {i n}) = \min _ {s _ {i} \in S _ {i n}} d (s _ {t}, s _ {i}) \tag {6}
$$

And $\mathcal{I}$ is the set of the indices for all signatures in the database with an intruder within the cell coverage. If $d(s_t, S_{out})$ is smaller than $d(s_t, S_{in})$ , then a 'detected' event is announced. To improve the reliability of detection, we employ a sliding window approach with step size $s$ . More specifically, if the signatures calculated for $N$ consecutive sliding windows $\{W_1, W_2, ..., W_N\}$ , all resembles more to the signatures with intruders, then a 'detected' event is announced. As for the Azimuth Distinction level, the direction (including the normal profile) with the highest similarity to the measured signature is returned as the estimated intruder's azimuth.

Note that in passive detection, users carry no devices. Hence unlike in conventional indoor localization, the calibration stage for passive detection is less error-prone to improper usage of devices and thus relies less on professionals to conduct the calibration. Also, for Equalized Detection, since it only involves two scenarios (user detected and no one around), it is possible to only randomly measure a few signatures as fingerprints for the case with intruders, especially the direction backwards the TX-RX link. In all, the calibration efforts in passive detection is comparably reasonable with respect to those in traditional fingerprinting.

![](images/fa08b027f732e393ba4161609c89df144d4ba2c4e0efb221c3161318ee4ff3d1.jpg)



Fig. 5. Multipath-scarce Scenario

![](images/8606091b477832fa8d17052089941fe7def0e6cdbab3da0503a2949bb93098af.jpg)



Fig. 6. Multipath-rich Scenario

# V. PERFORMANCE

In this section, we evaluate the performance of the proposed device-free detection scheme in various indoor scenarios, considering multipath-rich environments, background dynamics and both stationary presence and mobile user detections.

# A. Experiment Methodology

During our evaluations, we employ a TP-LINK TL-WR741N wireless router as the transmitter operating in IEEE 802.11n AP mode, and a LENOVO laptop equipped with Intel 5300 NIC as the receiver downloading packets from the AP. The firmware is modified as [15] to export channel state information (CSI) of each packet, i.e., a group of 30 channel frequency response (CFR) for further analysis. The transmission rate is 20 packets per second. We elaborate the settings of experiments in detail as follows.

The measurements are conducted in two representative indoor scenarios: a conference hall and a small computer lab (Fig. 5, Fig. 6). The former is relatively vacant, while the latter is piled with desks and computers, creating rather complex wireless propagating environment.

During the experiments, we denote one pair of AP location and laptop location as a link. In the hall scenario, we first put the AP 2m above the floor and on the floor, respectively, and fix the laptop 0.6m above the floor. For each AP placement, we pick two different laptop locations. For the lab case, the AP is about 1.2m above the floor, and we choose 3 laptop locations. Therefore, we have measured 4 links in the hall and 3 links in the lab.

For each link, we collect data with a person standing in 4 directions around the laptop at the distances of 0.5m and 1.0m, respectively. We also record the normal profile, i.e., when there is no one around. Hence, each link has 9 testing cases.

For each of the 9 testing cases, we collect CSIs for 1 minute and employ them for the fingerprint database. To collect test samples, we measure CSIs for the 9 testing cases for about 30 seconds on each link, from which the CSIs of 6 seconds are randomly picked as one test sample. We repeat the collection with 9 different persons at the 4 directions for both the range of 0.5m and 1.0m, thus obtaining 9 test samples for each intruder case. Finally, we collect 9 sets of CSIs when there is no one around as the test samples for the normal profiles for each link. To identify the robustness to background dynamics, half of the test data are measured when there are 3 men strolling in the test room, but keeping away from the TX-RX link for at least 2.5m.

The fingerprint database for each link is built up as follows. For database within coverage of radius 0.5m, only the training data collected within 0.5m are employed (i.e., 4 intruder cases and those for the normal profile). For the database of 1.0m, all training data are used.

To evaluate the scheme's realtime performance, we let one person faraway from the receiver (about 2.5m away) walk towards the receiver and then walk away again, from 4 directions w.r.t. the receiver for one link in the hall scenario.

We mainly focus on the following metrics to evaluate our detection scheme. (1) False Positive (FP): The fraction of cases where the receiver announces a 'Detected' event when there is no one within the disk range. (2) False Negative (FN): The fraction of cases where there is an intruder within the disk range, but the receiver fails to detect him.

Further, to represent how 'directional' the cell coverage is, we borrow the mathematical form to measure the directivity of a radiation pattern in the antenna jargon. For instance, a monitoring unit capable of detecting intruders in all directions within a disk range of radius $r_0$ with equal detection rate $P$ , would hold zero effective directionality, and therefore the directivity $D$ of this monitoring unit at radius $r_0$ would be 1 or 0 dB. Mathematically, the directivity of a monitoring unit at radius $r$ is defined as:

$$
D _ {r} = \frac {1}{\frac {1}{2 \pi} \int_ {0} ^ {2 \pi} p _ {r} (\theta) d \theta} \tag {7}
$$

where $p_r(\theta)$ is the normalized with maximal equal to 1.

$$
p _ {r} (\theta) = \frac {P _ {r} (\theta)}{P _ {r , m a x}} \tag {8}
$$

where $P_{r}(\theta)$ is the detection rate in the direction of $\theta$ at radius of r and $P_{r,max}$ is the maximum detection rate in all directions at radius of r.

![](images/828e214696a23d04eaf0f28be98786a416a3a9f939ba6b4eb72916259f4ae60b.jpg)



Fig. 7. FN/FP of Fingerprinting based Detection

![](images/dcae4e64fd779d288d1e811442c46ff43a309d2dbcdd7a6a8f33ede320997a59.jpg)



Fig. 8. Direction Performance of Fingerprinting

![](images/86f8d4359c8f51c55453093dc381d2d52170e79d3d2e2dba0c9a4a092c4d03e2.jpg)



Fig. 9. Average FN/FP w.r.t. Window Size

![](images/3ad3e6649acb13356d103afd676c3a53fc523bcdf4598034cf035aab64a0ca4b.jpg)



Fig. 10. Direction Performance w.r.t. Window Size

# B. Static Detection Performance

Fig. 7 demonstrates the false positive (FP) and false negative (FN) of the 7 links at radius of 0.5m and 1.0m, respectively. The average FN / FP across all the 7 links are 7.9% / 4.8% for the 0.5m range, and 6.9% / 6.4% for the 1.0m range. The reasons for such low FP and FN are twofold. One the one hand, fingerprinting approach compensates for the potential FN since it occurs only when the intruder's impact on wireless signals is quite different from all the fingerprints in the database. Further, with finer-grained CFR features, the distinction and location-dependence of the signatures have both improved considerably, compared with a single valued and unstable RSSI. On the other hand, the low FP owes to the resistance of the CFR feature to irrelevant noise.

Comparing the performance of the range of 0.5m and 1.0m, we see a slight rise of average FP from 0.5m to 1.0m. This is because the farther the intruder presents to the RX, the less severe impact the received signals would undergo. As a result, some test samples might resemble more to the fingerprints at 1.0m in the database, which contributes to a FP. We find no obvious performance gap between the relatively vacant hall and the clustered lab, which indicates that the feasibility of our scheme even in scenarios without abundant multipath effects.

Taking a closer look at the detection performance in detail, we evaluate the directivity of the cell coverage, i.e., the average detection rate for each direction w.r.t. the TX-RX link. Fig. 8 demonstrates the detection rate (DR) and the direction distinction accuracy along 4 directions (denote the direction along the TX-RX link as 0 degree, and follow a clockwise direction) including both the hall and lab scenarios.

As depicted in Fig. 8, the detection rate for each direction is around 90%, while the direction distinction accuracies reasonably ranges from 76% to 85%. The directivity at radius 1.0m is therefore approximately $D_{DR,1m} \approx 0.17dB$ with the metric of detection rate while $D_{DA,1m} \approx 0.58dB$ with the metric of direction distinction accuracy. The sharper directivity measured in direction distinction accuracy reveals that the signatures against the TX-RX link (0 degree) still hold less distinction compared with those along the TX-RX link (180 degree), which is ruled by the underlying anisotropic signal propagations. That is, when the user stands backwards the TX-RX link (0 degree of azimuth), it might be classified into other directions or the normal profile, since a user with such location tends to introduce similar extent of variations on the received signals. For the Equalized Detection level, though, the differences between the normal profile and all cases when there is a user nearby is comparatively larger. Hence the CFR signature proves to provide sufficient distinction from the normal profile, and the detection rate along each direction is comparably uniform.

![](images/9b6379e244d67d077dde06f67f3d5e4a7e13dbe2c3ecadb6fa7dff05a4d0f4aa.jpg)



Fig. 11. Fingerprinting based Mobile User Detection

# C. The Impact of Window Size

Since the window size represents the realtime performance of the detection, we measure the variation of FP and FN with different window sizes. Fig. 9 demonstrates the average FP and FN across 7 links at the radius of 1.0m with a window size range of 2 seconds to 10 seconds. Both FP and FN drop gracefully with the increasing window sizes since the histograms measured within longer time intervals generally incur less random noise. On the other hand, both FP and FN retain within 10% even with a window size of only 2 seconds. This indicates that the fingerprinting based scheme is feasible for realtime detection as long as the intruder stays within the range for about 3 to 4 seconds (accounting for both the window size and software delays).

Fig. 10 further illustrates the detection rate and direction distinction accuracy across each direction. Again, the performance along each direction tends to be insensitive to the variation of window size. Furthermore, for direction distinction, the direction towards the TX-RX link (180 degree) still enjoys the highest classification accuracy, indicating that the coverage shape of the proposed scheme is still not perfectly omnidirectional. Finer-grained and more effective features extracted from channel responses might ultimately contribute to a perfect disk-like coverage, even for the Azimuth Distinction level.

# D. Mobile Detection Performance

This experiment shows the realtime performance of our scheme with real mobile traces. Fig. 11 illustrates the detection results for a mobile user. The window size is set to 2 seconds, with a sliding step size of 0.5 seconds. At first, the measured signatures bear more resemblance to the normal profile, i.e., with smaller EMD to the signatures for the normal profile. In the time interval of 5.5 to 9.0 seconds, the distances between the measured signatures in each time window and the intruder signatures drop smaller. Therefore the RX announces a series of 'detected' events during this interval. The variation trends of the two sequences of EMDs demonstrate the feasibility of the proposed scheme in detecting mobile users who are approaching and walking away from the receiver for Equalized Detection. Nevertheless, the accuracy in discriminating the direction of the mobile user is less satisfactory due to the small window size and the uncertainty induced by mobility. We leave the more quantitative study on the mobile user detection, especially the Azimuth Distinction level to future work.

# VI. RELATED WORK

Device-free Passive Systems. The concept of radio-based device-free passive localization stems from the seminal work by Youssef et al. [1], which localizes or tracks a person carrying no radio enabled devices based on his impact on the wireless signals. Most device-free systems exploit the handy signature, RSSI, from either WiFi enabled monitors [23], or ZigBee sensors [6]. Despite its easy accessibility, RSSI fluctuates considerably even at a stationary link [14], which makes it an unreliable indicator to human presence. To achieve high robustness, Wilson et al. [3] proposed the radio tomographic imaging (RTI) technique, which exploits the redundancy introduced by sensor arrays surrounding the monitored region to visualize the human-induced RSSI fluctuations. Nevertheless, the dense deployment of sensors impedes its viability. To provide guidelines in devising optimal sensor deployment topology and placement, an in-depth scrutiny on the performance of the basic monitoring unit is indispensable, which grounds the primary purpose of our work.

Coverage Modeling. The coverage modeling serves as a fundamental issue in the coverage problems of wireless sensor networks $[7]$ $[8]$ $[9]$ . Both disk-like $[7]$ and non-disk $[9]$ models are used, yet these coverage models tend to be the compromise between theoretical simplicity and practical feasibility. In the literature of device-free systems, most coverage models of monitoring units are experimentally fitted and vary in shapes. Zhang et al. $[6]$ employed an eclipse coverage centered in the middle of the TX-RX link, while Wilson et al. $[3]$ used an oval coverage with foci at TX and RX. These models demonstrate a link-centric property $[24]$ , even with omnidirectional antennas. Only very recently did Patwari et al. $[25]$ propose a spatial model for human induced RSSI variance from a statistical perspective. We also target at the detection performance in the context of device-free systems, yet our effort deviates from previous research in that we strive to extract PHY layer information instead of the dominant MAC layer RSSI, and target at an omnidirectional range.

PHY assisted Indoor Localization. Originated from wireless channel sounding, Nerguizian et al. [16] leveraged the finer-grained PHY layer signal power features for indoor localization with dedicated infrastructure like Vector Network Analyzer (VNA). The PHY layer feature, channel impulse response (CIR) and its frequency domain counterpart, channel frequency response (CFR), are capable of discriminating multipath components, which is impossible with RSSI alone, the MAC layer superimposition of multipath signals. Recently, a thriving trend in PHY assisted indoor localization is to exploit modern radios such as OFDM to obtain PHY layer features with off-the-shelf hardware. Sen et al. [17] employed the rich multipath information in CFR for fingerprinting based spot localization, while both Wu et al. [14] and Sen et al. [26] extracted information about the direct path from CIR. The former takes the direct path power for accurate ranging, and the latter transforms the body blocking effect with respect to the direct path into reliable AoA information for triangulation. Our work builds upon this thread of research in device-based localization, but emphasizes more on the interplay between directional properties and the signal power features in device-free scenarios.

# VII. CONCLUSION

In this study, we demonstrate that the PHY layer information unfolds new possibilities for passive human detection, hence holding potential for breaking the limit restricted by link-centric architecture. On observing that the statistical spectral structures of small-scale multipath signals possess resistance to irrelevant background dynamics while retaining sensitivity to nearby human locomotion, we propose to leverage the histogram feature of the subcarrier amplitudes as signatures for our omnidirectional passive human detection. Experimental evaluations considering the richness of multipath, background dynamics and mobility have validated the feasibility of the Omni-PHD scheme, with an average false positive of 8% and false negative of 7% in detecting human presence in 4 directions. We envision this work as an early step towards passive human detection with flexible coverage, which acts as a crucial concern in human-centric computing.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program under grant No. 61190110, NSFC under grants No. 61171067, 61133016, and 61272466, National High-Tech R&D Program of China (863) under grant No. 2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under grant No. 61125202.

# REFERENCES

[1] M. Youssef, M. Mah, and A. Agrawala, “Challenges: Device-free passive localization for wireless environments,” in Proc. of ACM MobiCom, 2007.

[2] Y. Liu, Y. Zhao, L. Chen, J. Pei, and J. Han, “Mining frequent trajectory patterns for activity monitoring using radio frequency tag arrays,” IEEE Transactions on Parallel and Distributed Systems, vol. 23, no. 11, pp. 2138–2149, 2012.   
[3] J. Wilson and N. Patwari, “See-through walls: Motion tracking using variance-based radio tomography networks,” IEEE Transactions on Mobile Computing, vol. 10, pp. 612–621, 2011.   
[4] J. Krumm, S. Harris, B. Meyers, B. Brumitt, M. Hale, and S. Shafer, "Multi-camera multi-person tracking for easyliving," in Proc. of IEEE International Workshop on Visual Surveillance, 2000.   
[5] R. J. Orr and G. D. Abowd, “The smart floor: a mechanism for natural user identification and tracking,” in Extended abstracts in ACM CHI, 2000.   
[6] D. Zhang, J. Ma, Q. Chen, and L. M. Ni, “An rf-based system for tracking transceiver-free objects,” in Proc. of IEEE PerCom, 2007.   
[7] S. Meguerdichian, F. Koushanfar, M. Potkonjak, and M. B. Srivastava, "Coverage problems in wireless ad-hoc sensor networks," in Proc. of IEEE INFOCOM, 2001.   
[8] S. Kumar, T. H. Lai, and A. Arora, “Barrier coverage with wireless sensors,” in Proc. of the ACM MobiCom, 2005.   
[9] R. Tan, G. Xing, B. Liu, J. Wang, and X. Jia, “Exploiting data fusion to improve the coverage of wireless sensor networks,” IEEE/ACM Transactions on Networking, vol. 20, no. 2, pp. 450–462, 2012.   
[10] D. Dong, X. Liao, Y. Liu, C. Shen, and X. Wang, “Edge self-monitoring for wireless sensor networks,” IEEE Transactions on Parallel and Distributed Systems, vol. 22, no. 3, pp. 514–527, 2011.   
[11] Y. Liu and Z. Yang, “Understanding node localizability of wireless ad hoc and sensor networks,” IEEE Transactions on Mobile Computing, vol. 11, no. 8, pp. 1249–1260, 2012.   
[12] Z. Li, M. Li, J. Wang, and Z. Cao, “Ubiquitous data collection for mobile users in wireless sensor networks,” in Proc. IEEE INFOCOM, 2011.   
[13] S. Yang, X. Wang, and L. Fu, “On the topology of wireless sensor networks,” in Proc. IEEE INFOCOM, 2012.   
[14] K. Wu, J. Xiao, Y. Yi, M. Gao, and L. M. Ni, “Fila: Fine-grained indoor localization,” in Proc. IEEE INFOCOM, 2012.   
[15] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 packet delivery from wireless channel measurements,” in Proc. of ACM SIGCOMM, 2010.   
[16] C. Nerguizian, C. Despins, and S. Affes, “Geolocation in mines with an impulse response fingerprinting technique and neural networks,” IEEE Transactions on Wireless Communications, vol. 5, no. 3, pp. 603–611, 2006.   
[17] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are facing the mona lisa: Spot localization using phy layer information,” in Proc. of ACM MobiSys, 2012.   
[18] Y. Rubner, C. Tomasi, and L. J. Guibas, “The earth mover’s distance as a metric for image retrieval,” Springer International Journal on Computer Vision, vol. 40, no. 2, pp. 99–121, Nov. 2000.   
[19] Y. Jin, W.-S. Soh, and W.-C. Wong, “Indoor localization with channel impulse response based fingerprint and nonparametric regression,” IEEE Transactions on Wireless Communications, vol. 9, no. 3, pp. 1120–1127, march 2010.   
[20] K. Kleisouris, B. Firner, R. Howard, Y. Zhang, and R. P. Martin, "Detecting intra-room mobility with signal strength descriptors," in Proc. of ACM MobiHoc, 2010.   
[21] J. Zhang, M. H. Firooz, N. Patwari, and S. K. Kasera, “Advancing wireless link signatures for location distinction,” in Proc. of ACM MobiCom, 2008.   
[22] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: Wireless indoor localization with little human intervention,” in Proc. of ACM MobiCom, 2012.   
[23] A. E. Kosba, A. Saeed, and M. Youssef, “Rasid: A robust wlan device-free passive motion detection system,” in Proc. of IEEE PerCom, 2012.   
[24] D. Zhang, Y. Liu, and L. M. Ni, “Link-centric probabilistic coverage model for transceiver-free object detection in wireless networks,” in Proc. of IEEE ICDCS, 2010.   
[25] N. Patwari and J. Wilson, “Spatial models for human motion-induced signal strength variance on static links,” IEEE Transactions on Information Forensics and Security, vol. 6, no. 3-1, pp. 791–802, 2011.   
[26] S. Sen, R. R. Choudhury, and S. Nelakuditi, “Spinloc: Spin once to know your location,” in Proc. of ACM HotMobile, 2012.