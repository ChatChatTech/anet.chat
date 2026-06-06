# PADS: Passive Detection of Moving Targets with Dynamic Speed using PHY Layer Information

Kun Qian∗, Chenshu Wu∗, Zheng Yang∗, Yunhao Liu∗, Zimu Zhou†,

∗School of Software and TNList, Tsinghua University

† The Hong Kong University of Science and Technology

Abstract—Device-free passive detection is an emerging technology to detect whether there exists any moving entities in the area of interests without attaching any device to them. It is an essential primitive for a broad range of applications including intrusion detection for safety precautions, patient monitoring in hospitals, child and elder care at home, etc. Despite of the prevalent signal feature Received Signal Strength (RSS), most robust and reliable solutions resort to finer-grained channel descriptor at physical layer, e.g., the Channel State Information (CSI) in the 802.11n standard. Among a large body of emerging techniques, however, few of them have explored full potentials of CSI for human detection. Moreover, space diversity supported by nowadays popular multi-antenna systems are not investigated to the comparable extent as frequency diversity. In this paper, we propose a novel scheme for device-free PAssive Detection of moving humans with dynamic Speed (PADS). Both amplitude and phase information of CSI are extracted and shaped into sensitive metrics for target detection; and CSI across multiantennas in MIMO systems are further exploited to improve the detection accuracy and robustness. We prototype PADS on commercial WiFi devices and experiment results in different scenarios demonstrate that PADS achieves great performance improvement in spite of dynamic human movements.

# I. INTRODUCTION

Device-free passive detection is an emerging technology to detect whether there exists any (moving) entities in the area of interests without attaching any device to them [1], [2]. It is an essential primitive for various applications including intrusion detection for safety precautions, patient monitoring in hospitals, child and elder care in home, detection of living people in a fire or earthquake, and battlefield military applications, etc. In such applications, users should not be expected to carry any purposed devices for localization or detection. Consequently, traditional device-based techniques that require specialized hardware attached to people are no longer applicable [3]– [5]. Device-free detection has thus drawn increasing attention recently to enable motion detection and target localization in ubiquitous wireless environments [6]–[9].

With the widespread development and deployment of wireless networks, it is possible to realize passive detection of moving targets by capturing the wireless context changes caused by intruders. Various moralities of radio signals have been explored to enable device-free passive detection, among which RSS is one of the most popular ones due to its handy accessibility on existing wireless infrastructure [10], [11]. RSS-based device-free detection schemes exploit variations in RSS measurements to infer anomalous environment changes. Despite of extensive research conducted and great progress achieved, RSS-based scheme still suffers from its coarse granularity and high susceptibility to background noise. As a result, false detection can happen frequently since RSS changes caused by especially slow and slight target movements would be buried by its intrinsic variances.

More robust and reliable solutions resort to finer-grained channel descriptor at physical layer that is more sensitive to human presence while keeps rather stable in static environments. Channel State Information (CSI), which is now tractable on commodity NICs , presents subcarrier-level channel measurements in the framework of modern OFDM technique. With dominant advantages to RSS, CSI-based device-free detection and localization have recently attracted growing interests [12]–[14]. Among a large body of emerging techniques, however, few of them have explored full potentials of CSI for human detection. Specifically, most of previous works stop by amplitude of CFR yet ignore the as well sensitive phase information (mainly because the raw phases are meaningless). Moreover, space diversity supported by nowadays popular multi-antenna systems are not investigated to the comparable extent as frequency diversity. Finally, most previous works do not consider human behavior diversity, especially dynamic walking speed, and thus might fail for extremely slow moving targets.

In this paper, we propose a novel scheme for devicefree PAssive Detection of moving humans with dynamic Speed (PADS). Exploiting full information (both amplitude and phase) provided by CSI, our approach is able to accurately detect human movements of dynamic speed. To achieve this, we firstly derive meaningful phase information by employing a linear transformation on the raw CSI to eliminate the significant random noise. Then an outlier filtering is applied to sift out biased observations. Afterwards, a novel unified feature, i.e., maximum eigenvalue of covariance matrix, is extracted from normalized amplitude and phase information respectively. The feature is designed to be power-irrelevant yet variation-dependent and thus is generally extensible to various scenarios without specific environment calibration. Next, we introduce the Support Vector Machine (SVM) algorithm to seek for a cutting line of the feature values for different states (moving human presence and absence) for estimation. Finally, CSIs across multi-antennas in MIMO systems are exploited and integrated to improve the detection accuracy and

robustness.

To validate our design, we prototype PADS on commercial off-the-shelf (COTS) WiFi devices (ordinary wireless routers and laptops). Experiment results in different scenarios including laboratory, offices and classrooms demonstrate that PADS achieves great performance in spite of dynamic human movements (various walking speed). Concretely, PADS accurately alarms human movements by 97% in average with false negative rate of 2%. Moreover, PADS achieve consistently great performance in cases of walking human with dynamic speeds, which outperforms existing approaches.

In summary, our main contributions are as follows:

• We propose a design for passive human detection leveraging full information of CSI. To the best of our knowledge, we are the first to incorporate meaningful phase information for device-free human detection by successfully removing the randomness involved in raw phase.   
• We propose a novel unified feature using the eigenvalue of covariance matrix of normalized CSI. The feature holds excellent properties for device-free detection due to its universal applicability for both amplitude and phase and irrelevance to specific power parameters that vary over different links and over time.   
• We explore space diversity provided by multi-antennas supported by modern MIMO communicating systems to enable more accurate and robust detection.   
• We present the design and implementation of PADS in commodity WiFi devices. Benefit from full advantages of CSI, especially the sensitive phase feature, PADS is capable of detecting walking humans with dynamic speeds. Experiment results demonstrate that PADS can achieve high performance that outperforms traditional RSS-based and CSI-based systems.

The rest of the paper is organized as follows. In Section II, we present a brief review of recent innovations on devicefree human detection. Section III gives an overview of the system architecture while the detailed design is presented in the subsequent Section IV. In Section V, we introduce the experiment settings and results. Finally, we conclude the work in Section VI.

# II. RELATED WORKS

Device-free passive detection or localization have drawn much attention in the past years [1]. In this section, we briefly review the most related works on passive motion detection in pervasive wireless environments, which can be classified into two categories: RSS-based and CSI-based.

RSS-based detection. RSS is especially attractive for device-free detection since RSS measurements are easily accessible in existing wireless networks with commodity devices. Existing RSS-based passive detection or localization mainly rely on RSS changes due to target presence and movements. More specifically, a large value of RSS variance generally indicates a moving target in the monitoring area while a small value infers none [15]. The most well-known RSS-based device-free localization should be the Radio Tomographic Imaging (RTI) [10], which deploys a sensor network around the target area and uses the RSS changes to localize and track a person. Several varieties of RTI technique have been proposed, including the vRTI [16], mRTI [10], etc. Another system, RASID [11], improves the detection accuracy by analyzing the RSS features and adopting a non-parametric technique for adapting to environment changes. A more recent work [17] experimentally shows that the localization performance degrades significantly when people are moving in dynamic speeds and thus proposes a scheme that adaptively adjusts the sample window size to facilitate localization accuracy based on the estimated speed. Benefiting from full advantages of CSI, especially the sensitive phase feature, our proposed system is also capable of detecting walking humans with dynamic speeds, yet without the complex speed estimation.

![](images/b81dafdd57f3b5dd45b4b195dc678fa800b23661a10e6b6b31d3eeacd636c238.jpg)



Figure 1. Architecture overview of PADS

CSI-based detection. CSI-based scheme attracts more attention in recent years since CSI can be exported from commodity wireless NICs [18]. Similar to RSS-based scheme, most CSI-based detection approaches also leverage variations in CSI measurement to infer target locations or presences. Pilot [19] is an early attempt in device-free positioning, which leverages the correlation of CSI over time to monitor abnormal appearance and further locate the entity. Omni-PHD [13] studies the omnidirectional sensing coverage for passive human detection, using multipath effects captured by CSI. FIMD [12] enables accurate fine-grained burst motion detection by exploiting the temporal stability of CSI in static environments. FCC [14] studies the relationship between the number of moving people and the variation of CSI and thus achieves device-free crowd counting. Despite that many works have investigated CSI for device-free detection, most of previous approaches merely leverage the amplitude of CSI information and leave phase information unexplored. In this paper, we firstly explore and incorporate phase with amplitude for device-free human detection.

# III. OVERVIEW

As shown in Figure 1, we utilize the physical layer channel state information (CSI) as a primary indicator for human motion. CSI depicts the temporal and spectral structure properties of a wireless link when an RF signal propagates along multiple paths. The rationale for device-free human detection is that a fraction of propagation paths would be affected due to intruder presence. Specifically, for moving targets, this contributes to the dramatic changes in CSI over time, which can then be captured by the temporal variations of CSIs. CSIs can be measured and collected from commodity WiFi devices using off-the-shelf network interface cards (NIC) such as Intel 5300 [18]. In modern multiple subcarrier radio like OFDM, CSI is usually portrayed in the frequency domain by the form of Channel Frequency Response (CFR).

![](images/49e3482260c54d24ed223122c23c7b36e0880833464c7c623879d6bf18362fcd.jpg)



Figure 2. Phase before and after linear transformation

To enable a fast and efficient detection system, three main components are incorporated in PADS, i.e., data preprocessing, feature extraction, and target detection. Firstly, CSIs are exported from off-the-shelf NIC that communicates with an ordinary wireless router. Raw CSI measurements could contain significant phase random noise, which are supposed to be removed by the phase sanitization module. After that, an outlier filter is applied to eliminate occasional outlier observations in CSI sequence.

Feature extraction acts as the most critical part for accurate and efficient human detection. In PADS, we propose to exploit amplitude and phase information of CFR simultaneously. To avoid the influence of diverse transmitting power in specific scenarios, we devise a novel feature using the respective three maximum eigenvalues of the covariance matrices of a normalized version of amplitude and phase information over a certain time window.

The features are then fed to an inference model to alarm user movements. Instead of using a clustering algorithm, we adopt a threshold-like detection scheme. A cut-off line is precalibrated by employing a classical classification algorithm, i.e., Support Vector Machine (SVM), on certain amount of preliminary measurements. Movement inference is then done by comparing the amplitude and phase feature to the precalibrated values. The approach advantages in zero data constraints (the clustering-based method would require each group of data to contain measurements corresponding to at least two different states [12]). Finally, to enhance the detection accuracy and robustness, multiple antennas in modern MIMO systems are also explored and integrated.

![](images/2c3270b3b0e4575bba7f7ee4fd8e14b69bf27e7b3baa8c0408d6e1656fd1cd06.jpg)



Figure 3. Outlier detection for CSI observations

# IV. METHODOLOGY

In this section, we details the design of PADS by real measurements.

# A. Data preprocessing

Leveraging the off-the-shelf NIC with slight driver modification, a group of CFRs on $N = 3 0$ subcarriers can be exported to uplayer users for every one packet in the format of CSI:

$$
H = \left[ H (f _ {1}), H (f _ {2}), \dots , H (f _ {N}) \right] \tag {1}
$$

Each CSI represents the amplitude and phase of an OFDM subcarrier:

$$
H (f _ {k}) = \| H (f _ {k}) \| e ^ {j \angle H (f _ {k})} \tag {2}
$$

where $H ( f _ { k } )$ is the CSI at the subcarrier $k ( k \ \in \ [ 1 , 3 0 ] )$ with central frequency of $f _ { k } ,$ and $\angle H ( f _ { k } )$ denotes its phase (for convenience, we also use $\phi _ { k }$ to denote the phase in the following). To monitoring an area of interests, CSIs are continuously collected and K measurements within a specific time window form the CSI sequence which can be denoted as

$$
\mathbb {H} = \left[ H _ {1}, H _ {2}, \dots , H _ {K} \right] \tag {3}
$$

The K measurements of CFR then serve as the basic input for our movement detection algorithm, which will be first passed through a phase sanitization and an outlier filtering process.

1) Phase sanitization: Although CSI has been widely explored for various applications, most of them only considers amplitudes of either CFR or CIR and thus the counterpart of CSI, i.e., phase information does not attract enough attentions. One of the most important reasons lies in the unavailability of phase information on commodity devices [4], [19]. As shown in Figure 2, due to random noise and unsynchronized time clock between transmitter and receiver, raw phase information behaves extremely random over the all feasible field, making it inapplicable for any detection.

In this paper, we seek to derive and incorporate usable phase information to enable motion detection of dynamic target speeds. Our key observation is that significant component of random phase offsets can be removed by employing a linear transformation on the raw phase readings.

![](images/fc434da7af45a544ac7b13e7f50fa252f65ce26189d55aa27e69b6b517ad1441.jpg)



![](images/b5d944f3986b7db9a32089efe3dfbd689ea8b13e68bad4c35462136e5b60d6d1.jpg)



Figure 4. Variances of both amplitude and phase increase significantly due to human movements.

Specifically, the measured phase $\hat { \phi } _ { i }$ for the $i ^ { t h }$ subcarrier can be expressed as:

$$
\hat {\phi} _ {i} = \phi_ {i} - 2 \pi \frac {k _ {i}}{N} \delta + \beta + Z, \tag {4}
$$

where $\phi _ { i }$ denotes the true phase, δ is the timing offset at the receiver, which causes phase error expressed as the middle term, $\beta$ is an unknown phase offset, and Z is some measurement noise. $k _ { i }$ denotes the subcarrier index (ranging from -28 to 28 in IEEE 802.11n) of the $i ^ { t h }$ subcarrier and N is the FFT size (which equals to 64 in IEEE 802.11 a/g/n). Due to the unknowns listed above, it is infeasible to obtain the true phase shifts with solely commodity WiFi NICs.

To mitigate the impact of random noises, we perform a linear transformation on the raw phases, as recommended in [4]. The key idea is to eliminate δ and β by considering phase across the entire frequency band. Firstly, we define two terms a and b as follows:

$$
a = \frac {\hat {\phi} _ {n} - \hat {\phi} _ {1}}{k _ {n} - k _ {1}} = \frac {\phi_ {n} - \phi_ {1}}{k _ {n} - k _ {1}} - \frac {2 \pi}{N} \delta \tag {5}
$$

$$
b = \frac {1}{n} \sum_ {j = 1} ^ {n} \hat {\phi} _ {j} = \frac {1}{n} \sum_ {j = 1} ^ {n} \phi_ {j} - \frac {2 \pi \delta}{n N} \sum_ {j = 1} ^ {n} k _ {j} + \beta \tag {6}
$$

If the subcarrier frequency is symmetric, which indicates $\textstyle \sum _ { j = 1 } ^ { n } k _ { j } \ = \ 0 .$ , b can be expressed as $\begin{array} { r } { b = \frac { 1 } { n } \sum _ { j = 1 } ^ { n } \phi _ { j } + \beta . } \end{array}$ . Subtracting the linear term $a k _ { i } + b$ from the raw phase φˆi, we obtain a linear combination of true phases, denoted as $\phi _ { i }$ , from which the random phase offsets have been removed (omitting the small measurement noise Z):

$$
\tilde {\phi} _ {i} = \hat {\phi} _ {i} - a k _ {i} - b = \phi_ {i} - \frac {\phi_ {n} - \phi_ {1}}{k _ {n} - k _ {1}} k _ {i} - \frac {1}{n} \sum_ {j = 1} ^ {n} \phi_ {j} \tag {7}
$$

Figure 2 illustrates an example of the phase after transformation, which distributes relatively stable as expected compared to the original random version. Although we could not claim the sanitized information is just the true phase, we do derive a usable and effective feature of the true phase. For clarity, we directly use φ instead of ˜phi to refer to the transformed phase hereafter.

![](images/388f3dd375b2619c887d4019015d5eb4cda27e2513b25c88a061de0556d18654.jpg)



![](images/4245d5c54025f456fafe7646dc5a8652a040043113480450efdeb23fb9d1863a.jpg)



Figure 5. Variances of both amplitude and phase increase significantly due to human movements.

2) Outlier filter: Outliers might appear in CSI measurements due to protocol specifications as well as environmental noises. As motion detection techniques mostly adopt variation based detection whatever algorithms are used, such outliers could affect the movement detection performance a lot and thus should be sifted out before detecting motion. To identify and remove these biased measurements, we adopt a Hampel identifier [20], which declares any point falling out of the closed interval $[ \mu \ : - \ : \gamma \sigma , \mu \ : + \ : \gamma \sigma ]$ as an outlier, where µ and σ are the median and the median absolute deviation (MAD) of the data sequence, respectively. γ is an application dependent parameter and the most widely used value is 3. Figure 3 illustrates the frequent outlier observations that might be contained in raw measurements and the results of outlier filtering (using window size of 100 and γ of 3).

# B. Feature Extraction

An appropriate feature plays a critical role in device-free detection and feature extraction serves as the most important component of PADS. Various statistical feature has been exploited for detection,such as variance [16], mean [10], distribution distance [13], [21], etc. Different from previous works that mostly utilize single feature from amplitude information, we seek for both amplitude-based and phase-based features and use them simultaneously for motion detection.

Although accounting for both amplitude and phase, we strive to search for unified feature metrics that are suitable for both sides. Apparently, the feature metric should be absolute power irrelevant and possibly variance dependent, since transmitting power parameters would be adapted over different scenarios and thus are scenario dependent while human movements contribute to disturbances of amplitude as well as phase. As illustrates in Figure 4 and Figure 5, one can see variances of both amplitude and phase in case of human movements are significantly larger than those in static cases. Figure 6 further illustrates the variances over each individual subcarrier in case of moving human presence and absence.

Motivated by these observations, we suspect that variances of amplitude and phase would be a couple of good indicators for abnormal appearance of moving people. Unfortunately, variance could not directly be used as distinctive feature for human detection because it is related to absolute signal power and thus does not scale to diverse scenarios with various link states. As a consequence, we propose to extract feature from the respective covariance matrix of normalized CFR amplitude and phase of n sequential measurements over a certain time window. Denote ¯ kHk and Φ¯ as the normalized CFR amplitude and phase sequence, then their corresponding covariance matrix is respectively

![](images/76c6c4368f2221d1832a612d7cb435694db607db9e5d62e92cec9d65a68af1ed.jpg)



![](images/572041f6d27b2dd0ef9d99d0072f33535ef31253d5107181f443304e63da35b7.jpg)



![](images/e9c1aa0db45c8cbc5d28fc04f67abf15b92f9936186997ad89d06b8647530b91.jpg)



![](images/b5835e99bcf5685c6c9d546c8959eae9da9825267f1fb89d81e2032885c7be0a.jpg)



Figure 6. Variances of both amplitude and phase increase significantly due to human movements. (a) Subcarrier 10 of static case; (b) Subcarrier 10 of dynamic case; (c) Subcarrier 20 of static case; (d) Subcarrier 20 of dynamic case.

$$
\Sigma (\| \bar {\mathbb {H}} \|) = [ \operatorname{cov} (\bar {H} _ {i}, \bar {H} _ {j}) ] _ {K \times K}, \tag {8}
$$

$$
\Sigma (\bar {\Phi}) = \left[ \operatorname{cov} \left(\bar {\phi} _ {i}, \bar {\phi} _ {j}\right) \right] _ {K \times K}, \tag {9}
$$

where cov $( X _ { i } , X _ { j } )$ denotes the covariance between vectors $X _ { i }$ and $X _ { j }$ and X¯ indicates the normalized version of variable X. For both matrices, with lower covariance values the link is more likely to be static and free of intrusion. In contrast, higher covariances would probably indicate presence of moving humans who disturb the link.

To extract a simple feature for further detection, we compute the eigenvalues of both matrices and select the maximum eigenvalue of each matrix, which finally forms a two-tuples $F = [ \alpha , \rho ] ;$

$$
\alpha = \max (e i g e n (\Sigma (\| \bar {\mathbb {H}} \|))), \rho = \max (e i g e n (\Sigma (\bar {\Phi}))). \tag {10}
$$

In practice, to guarantee the accuracy and robustness of detection, we further introduce the second maximum eigenvalue of amplitude and phase respectively and thus devise a four-tuple feature as $F ~ = ~ \left[ \alpha _ { 1 } , \alpha _ { 2 } , \rho _ { 1 } , \rho _ { 2 } \right]$ , where $\alpha _ { 1 }$ , α2 and $\rho _ { 1 } , \rho _ { 2 }$ represent the respective maximum and second maximum eigenvalue for amplitude and phase. In SectionV, we will experimentally validate that more eigenvalues would result in better performance while two is sufficient for achieving satisfied accuracy.

![](images/4b054ad4f8fb50c939a7c6f69e2b04392e4dc7ec51533af85a539f4ace9f2190.jpg)



Figure 7. Preliminary classification result using SVM

# C. Motion Detection

Aiming at achieving calibration free detection, there are generally two categories of methods can be adopted: clustering based and threshold based. The former automatically clusters measurement data into several clusters and then distinguish different clusters as different states (presence or absence of human) by comparing the center distance of each cluster. The latter seeks for a general threshold from partial pre-collected data and conducts state identification based on the threshold value. Although the clustering approach avoids both environment calibration and threshold training efforts, it implicitly assumes that at least two states are involved in each group of measurements(otherwise one cluster or several clusters corresponding to a same state are resulted, leading to miss or false detection), which is impractical for most applications. As a consequence, we adopt the threshold based scheme assisted by SVM classification.

We first conduct an SVM based classification on preliminary measurements collected from several scenarios. The abovementioned feature factors α and $\rho$ are used as the input feature of the SVM. As shown in figure Figure 7, we are delighted to see that a clear gap can be found between the data correspond to presence and absence of moving human. Moreover, although people with different moving speeds exhibit various values on each metric (since they induce diverse alterations on the signal propagation paths), the self-similarity within individual state is always remarkably smaller than cross-similarity of data correspond to different states. This lays the fundamental underpinnings of detection of people with dynamic moving speeds. The rationale is that even slight motion can caused perceivable changes in CSI, which enables its detection.

A pre-calibrated empirical cutting line is on this basis determined and then used to further moving human detection. The pre-calibrated cutting line, according to our measurements, would fit various scenarios including different propagation distances, channel attenuation, different target behaviors, etc. One key reason is that all the features involved is power independent but only relates to the extent of temporal changes.

![](images/e0152b45d72e6afac857faf11789fc486d33f82f6d819d5c0b5a9c81d587c6ea.jpg)



Figure 8. Antenna diversity of amplitude feature

![](images/b17f0cf7061902344a957848721d0435150c34e462c9cc62bcb29236b9b9fe67.jpg)



Figure 9. Antenna diversity of phase feature

![](images/27ad062970e9869a41a0205d4c9ca483d78185aabde7c8cf53555e5a7bd9910b.jpg)



Figure 10. Receiver

![](images/d293bfe245cf51fb4bf0aa978cbd4909a5a05063f0db4bd10b0dafca5062a57d.jpg)



Figure 11. Sample 1: Corridor

![](images/817d9ba18d66e0ebe72c49ee08b874a2ba3ff6083637d1403ee1bd90bfc46007.jpg)



Figure 12. Sample 2: Lab

# D. Enhancement via Multiple Antennas

Noticing that multiple antennas are available in the more and more popular MIMO communicating systems, we also exploit multiple antennas to improve the precision and robustness of human detection.

As shown in Figure 8 and Figure 9, the selected features of amplitude and phase do vary over different antennas. If mistakenly using a “bad” antenna, significant false alarm might occur. Fortunately, we observe that the median value of all antennas keep relatively stable across different scenarios. As a result, for multi-antenna systems, we choose the median indicator for detection, which is demonstrated to be simple and effective by real experiments.

# V. EXPERIMENTS AND EVALUATION

# A. Experimental Setup

To evaluate the performance of PADS, we conduct real experiments on commodity readily COTS devices. Specifically, we use a single antenna TP-link wireless router as transmitter and a mini PC with three antennas as receiver, which is shown in Figure 10. We collect data from different scenarios: classrooms, offices, corridors, etc. Figure 11 and Figure 12 show two samples of these scenarios. In each case, we let a volunteer walk through the monitoring area with different speeds along a trajectory that traverses the space uniformly. We also collect data when there is no human presence or there are only stationary persons. In total, we collect mobile and static traces for more than one hour, respectively.

In different scenarios, the AP is placed at various height from 1.2m to 2m. Diverse TX-RX distances from 2m to 7m are also considered. In addition, LOS and NLOS conditions (when the AP is blocked by the wall) are also both involved.

# B. Performance Evaluation

1) Evaluation Metric: We use following two metrics to evaluate the performance of our proposed PADS system, as well as present FIMD system and RSSI-based system, in respective environment.

• True Negative (TN) Rate: TN rate is the probability that the static environment is correctly classified.   
• True Positive (TP) Rate: TP rate is the probability that the human motion events is correctly detected.

2) Overall Performance: First we depict TN rates of systems working in static environments. Figure 13 presents results of five different test cases measured at different time or places. All methods achieve excellent performance of TN rates higher than 98% in most cases. However, we argue that though RSSIbased aproach reaches equally high performance comparing with PADS and FIMD in most cases, it suffers from temporal variance and thus its performance is unstable (as indicated by the performance drop in case 5).

Furthermore, we present TP rates of systems when human motions present in the monitoring areas. Figure 14 shows results of five different cases measured at the same places as static cases. As can be seen, PADS and FIMD systems can detect human motions more precisely than RSSI-base system. More importantly, PADS slightly outperforms FIMD system, which validate the effectiveness of our newly incorporated phase information as well as the novel features.

![](images/2a1e6232e387ee0901460cc764cae32995ceeb52a5fda17ddcdf918e0bd00f67.jpg)



Figure 13. TN rate of static cases

![](images/ac2decd51e304e45674fe70df682816c5321a52597ee73666757fbd1966bc6f6.jpg)



Figure 14. TP rate of cases with human motion

![](images/bb9c4e40103aace0d6ba3a5a7f1bc1b3210819abfe6b2052642d577192ce5122.jpg)



Figure 15. Relationship of detection rate and sliding window size

![](images/75974a4d3ce6b9661f9207ee1dfa468809f24f6fc513a139e2b70dfc6713aa44.jpg)



Figure 16. Relationship of detection rate and number of features

Before analyzing the influence of different parameters on performance of PADS, we first present the final access results. Balancing the performance and runtime delay, with sliding window size and number of eigenvalues setting to be 50 and 3, the TN rate and TP rate of PADS would be greater than 98% and 97% in average, respectively.

3) Impacts of Sliding Window Size: Intuitively, the larger the size of sliding window is, the better the performance gains, since the influence of temporal variance would be relieved by using large portion of data. It can be verified in Figure 15, which presents the change of detection rate against window size. For all three systems, the detection rates consistently raise up when sliding window size increases. Yet it is not a panacea. When sliding window size exceeds some threshold, the intrinsic temporal variance of CSI will become comparable to variance caused by human motion, which offsets the benefit of increasing window size, stalling or even reversing the rising trend of detection rates.

4) Impacts of Number of Features: Different from eigenvalues of correlation matrix used in FIMD, whose principle portions are concentrated in first two eigenvalues, eigenvalues of covariance matrix used in PADS are more distributed. As a result, more features used might result in higher detection rate. Figure 16 shows the performance of alternate systems, PADS and FIMD, when different number of features are employed. As seen, with the number of features increased, the detection rate of PADS increases and remains stable when the number of features reaches 5. In contrast, the turning point of FIMD is 4, after which the performance drops significantly due to addition of useless eigenvalues with high order.   
5) Impacts of Number of Antennas: The impacts on detection performance of number of antennas we leveraged in PADS system are studied by testing several human motion cases. Figure 17 shows the promotion of detection rate by using multiple antennas against single antenna. Except for those cases which are completed detected with single antenna, using multiple antennas improve the performance of PADS system significantly, due to the decreasing of the probability that a “bad” antenna is used in PADS system.   
6) Performance against Dynamic Speed: So far, we have been focusing on general performance of PADS system. To study the beneficial gain of more sensitive features used in our system, we compare the performance of PADS, FIMD and

![](images/72ce359630476634ae0b32162a065fb2ecd6fa0c5c6dd715e31d42f30da307ad.jpg)



Figure 17. Detection rate of cases with different number of antennas

RSSI-based system in different scenarios when the intruders walk with dynamic speeds. Figure 18 shows the detection rate of human motion with different speeds. With human walks slowly, both FIMD and RSSI-based system experience fall of performance to different extents, while the performance of PADS retains almost unchanged even human walk very slowly. In summary, comparing to drastic changes of amplitudes when fast human motion exists, the changes of phases are much more sensitive to slow human motion, and thus can be leveraged to maintain the high performance in the situation that human walk very slowly.

# VI. CONCLUSIONS

In this study, we design and implement a WiFi-based sensing system for passive detection of moving targets. To the best of our knowledge, this is the first to exploit the more sensitive phase information other than amplitude information in this field. We have conducted extensive experiments and the evaluation results show that both sensitivity and robustness are improved simultaneously compared with previous approaches. We open up the utilization of CSI’s phase information for passive target detection and future work will focus on taking full advantage of CSI.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program 61190110, NSFC under grant 61171067, 61133016, and 61472098, National Basic Research Program of China (973) under grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under Grant 61125202.

# REFERENCES

[1] M. Youssef, M. Mah, and A. Agrawala, “Challenges: device-free passive localization for wireless environments,” in Proceedings of ACM MobiCom, 2007, pp. 222–229.   
[2] N. Patwari and J. Wilson, “Rf sensor networks for device-free localization: Measurements, models, and algorithms,” Proceedings of the IEEE, vol. 98, no. 11, pp. 1961–1973, 2010.   
[3] N. Patwari and S. K. Kasera, “Robust location distinction using temporal link signatures,” in Proceedings of ACM MobiCom, 2007, pp. 111–122.   
[4] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are facing the mona lisa: spot localization using PHY layer information,” in Proceedings of ACM MobiSys, 2012, pp. 183–196.

![](images/c6b40bc240ab140b030e3e9bd2d823f7baed4f791dae8f500ec20fe3beef3640.jpg)



Figure 18. Detection rate of human motions with dynamic speed

[5] K. Wu, J. Xiao, Y. Yi, M. Gao, and L. M. Ni, “Fila: Fine-grained indoor localization,” in Proceedings of IEEE INFOCOM. IEEE, 2012, pp. 2210–2218.   
[6] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proceedings of ACM MobiCom. ACM, 2013, pp. 27–38.   
[7] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller, “3d tracking via body radio reflections,” in Proceedings of Usenix NSDI, vol. 14, 2013.   
[8] B. Kellogg, V. Talla, and S. Gollakota, “Bringing gesture recognition to all devices,” in Proceedings of Usenix NSDI, vol. 14, 2014.   
[9] M. Seifeldin, A. Saeed, A. E. Kosba, A. El-Keyi, and M. Youssef, “Nuzzer: A large-scale device-free passive localization system for wireless environments,” Mobile Computing, IEEE Transactions on, vol. 12, no. 7, pp. 1321–1334, 2013.   
[10] J. Wilson and N. Patwari, “Radio tomographic imaging with wireless networks,” Mobile Computing, IEEE Transactions on, vol. 9, no. 5, pp. 621–632, 2010.   
[11] A. E. Kosba, A. Saeed, and M. Youssef, “Rasid: A robust wlan devicefree passive motion detection system,” in Proceedings of IEEE PerCom. IEEE, 2012, pp. 180–189.   
[12] J. Xiao, K. Wu, Y. Yi, L. Wang, and L. M. Ni, “Fimd: Fine-grained device-free motion detection.” in Proceedings of IEEE ICPADS, 2012, pp. 229–235.   
[13] Z. Zhou, Z. Yang, C. Wu, L. Shangguan, and Y. Liu, “Omnidirectional coverage for device-free passive human detection,” Parallel and Distributed Systems, IEEE Transactions on, vol. 25, no. 7, pp. 1819–1829, July 2014.   
[14] W. Xi, J. Zhao, X.-Y. Li, K. Zhao, S. Tang, X. Liu, and Z. Jiang, “Electronic frog eye: Counting crowd using wifi,” in Proceedings of IEEE INFOCOM, 2014.   
[15] J. Yang, Y. Ge, H. Xiong, Y. Chen, and H. Liu, “Performing joint learning for passive intrusion detection in pervasive wireless environments,” in Proceedings of IEEE INFOCOM. IEEE, 2010, pp. 1–9.   
[16] J. Wilson and N. Patwari, “See-through walls: Motion tracking using variance-based radio tomography networks,” Mobile Computing, IEEE Transactions on, vol. 10, no. 5, pp. 612–621, 2011.   
[17] X. Zheng, J. Yang, Y. Chen, and Y. Gan, “Adaptive device-free passive localization coping with dynamic target speed,” in Proceedings of IEEE INFOCOM, 2013, pp. 485–489.   
[18] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 packet delivery from wireless channel measurements,” SIGCOMM Comput. Commun. Rev., vol. 40, no. 4, pp. 159–170, Aug. 2010.   
[19] J. Xiao, K. Wu, Y. Yi, L. Wang, and L. M. Ni, “Pilot: Passive device-free indoor localization using channel state information,” in Proceedings of IEEE ICDCS. IEEE, 2013, pp. 236–245.   
[20] L. Davies and U. Gather, “The identification of multiple outliers,” Journal of the American Statistical Association, vol. 88, no. 423, pp. 782–792, 1993.   
[21] Y. Zhao and N. Patwari, “Histogram distance-based radio tomographic localization,” in Proceedings of ACM IPSN, 2012, pp. 129–130.