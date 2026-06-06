# Enabling Contactless Detection of Moving Humans with Dynamic Speeds Using CSI

KUN QIAN, CHENSHU WU, ZHENG YANG, and YUNHAO LIU, Tsinghua University FUGUI HE, West Anhui University TIANZHANG XING, Northwest University

Device-free passive detection is an emerging technology to detect whether there exist any moving entities in the areas of interest without attaching any device to them. It is an essential primitive for a broad range of applications including intrusion detection for safety precautions, patient monitoring in hospitals, child and elder care at home, and so forth. Despite the prevalent signal feature Received Signal Strength (RSS), most robust and reliable solutions resort to a finer-grained channel descriptor at the physical layer, e.g., the Channel State Information (CSI) in the 802.11n standard. Among a large body of emerging techniques, however, few of them have explored the full potential of CSI for human detection. Moreover, space diversity supported by nowadays popular multiantenna systems are not investigated to a comparable extent as frequency diversity. In this article, we propose a novel scheme for device-free PAssive Detection of moving humans with dynamic Speed (PADS). Both full information (amplitude and phase) of CSI and space diversity across multiantennas in MIMO systems are exploited to extract and shape sensitive metrics for accuracy and robust target detection. We prototype PADS on commercial WiFi devices, and experiment results in different scenarios demonstrate that PADS achieves great performance improvement in spite of dynamic human movements.

CCS Concepts: • Computer systems organization → Embedded software; • Networks → Location based services;

Additional Key Words and Phrases: Noninvasive, motion detection, channel state information, phase difference

# ACM Reference format:

Kun Qian, Chenshu Wu, Zheng Yang, Yunhao Liu, Fugui He, and Tianzhang Xing. 2018. Enabling Contactless Detection of Moving Humans with Dynamic Speeds using CSI. ACM Trans. Embed. Comput. Syst. 17, 2, Article 52 (January 2018), 18 pages.

https://doi.org/10.1145/3157677

# 1 INTRODUCTION

Device-free passive detection is an emerging technology to detect whether there exist any (moving) entities in the areas of interest without attaching any device to them (Youssef et al. 2007;

This work is supported in part by the NSFC under grants 61522110, 61332004, 61472098, 61672319, and 61632008, 61702375 and the National Key Research Plan under grant no. 2016YFC0700100.

Authors’ addresses: K. Qian, Z. Yang, and Y. Liu, School of Software and TNList, Tsinghua University, Beijing, China; emails: {qiank10, hmilyyz, yunhaoliu}@gmail.com; C. Wu, Department of Electrical and Computer Engineering, University of Maryland, College Park; email: wucs32@gmail.com; F. He, Department of Information Engineering, West Anhui University, Liu’an, Anhui, China; email: fuguihe@163.com; T. Xing, School of Information and Technology, Northwest University, Xi’an, Shanxi, China; email: xtz@nwu.edu.cn.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2018 ACM 1539-9087/2018/01-ART52 \$15.00

https://doi.org/10.1145/3157677

Patwari and Wilson 2010). It is an essential primitive for various applications including intrusion detection for safety precautions, patient monitoring in hospitals, child and elder care in the home, detection of living people in a fire or earthquake, and battlefield military applications. In such applications, users should not be expected to carry any purposed devices for localization or detection. Consequently, traditional device-based techniques that require specialized hardware attached to people are no longer applicable (Yang et al. 2012; Wu et al. 2015a; Tian et al. 2017a, 2017b; Shangguan et al. 2017; Yang et al. 2015). Device-free detection has thus drawn increasing attention recently to enable motion detection and target localization in ubiquitous wireless environments (Pu et al. 2013; Adib et al. 2014; Kellogg et al. 2014; Seifeldin et al. 2013).

With the widespread development and deployment of wireless networks, it is possible to realize passive detection of moving targets by capturing the wireless context changes caused by intruders. Various moralities of radio signals have been explored to enable device-free passive detection, among which RSS is one of the most popular ones due to its handy accessibility on existing wireless infrastructure (Wilson and Patwari 2010; Kosba et al. 2012). RSS-based device-free detection schemes exploit variations in RSS measurements to infer anomalous environment changes. Despite extensive research conducted and great progress achieved, the RSS-based scheme still suffers from its coarse granularity and high susceptibility to background noise. As a result, false detection can happen frequently since RSS changes caused by especially slow and slight target movements would be buried by its intrinsic variances.

More robust and reliable solutions resort to a finer-grained channel descriptor at the physical layer that is more sensitive to human presence while keeping rather stable in static environments (Zhou et al. 2015a). Channel State Information (CSI), which is now tractable on commodity network interface cards (NICs), presents subcarrier-level channel measurements in the framework of the modern OFDM technique. With dominant advantages to RSS, CSI-based device-free detection and localization have recently attracted growing interest (Xiao et al. 2012; Zhou et al. 2014; Xi et al. 2014). Among a large body of emerging techniques, however, few of them have explored the full potential of CSI for human detection. Specifically, most of the previous works stop by amplitude of the Channel Frequency Response (CFR) yet ignore the sensitive phase information (mainly because the raw phases are meaningless). Moreover, space diversity supported by nowadays popular multiantenna systems are not investigated to the comparable extent as frequency diversity. Finally, most previous works do not consider human behavior diversity, especially dynamic walking speed, and thus might fail for extremely slow-moving targets.

In this article, we propose a novel scheme for device-free PAssive Detection of moving humans with dynamic Speed (PADS). Exploiting full information (both amplitude and phase) provided by CSI and space diversity across multiantennas in MIMO systems, our approach is able to accurately detect human movements of dynamic speed. To achieve this, we first extract raw CSI from the PHY layer and preprocess both amplitude information and phase information in different manners according to their characteristics. For phase information, phase difference of raw CSI between antenna pairs is calculated and unwrapped to eliminate the significant random noise while preserving sensitivity against environment changes. For amplitude information, we apply an outlier filtering to sift out biased observations. Afterward, a novel unified feature, i.e., maximum eigenvalue of correlation matrix, is extracted from calibrated amplitude and phase information, respectively. The feature is designed to be power irrelevant yet variation dependent and thus is generally extensible to various scenarios without specific environment calibration. Next, we introduce the Support Vector Machine (SVM) algorithm to seek for a cutting line of the feature values for different states (moving human presence and absence) for estimation. Finally, CSIs across multiantennas in MIMO systems are exploited and integrated to improve the detection accuracy and robustness.

To validate our design, we prototype PADS on commercial off-the-shelf (COTS) WiFi devices (ordinary wireless routers and laptops). Experiment results in different scenarios including the laboratory, classrooms, corridors, and meeting rooms demonstrate that PADS achieves great performance in spite of dynamic human movements (various walking speed). Concretely, PADS accurately alarms human movements by 99% on average with almost no false-negative errors. Moreover, PADS achieves consistently great performance in cases of walking humans with dynamic speeds, which outperforms existing approaches.

In summary, our main contributions are as follows:

—We propose a design for passive human detection leveraging full information of CSI. To the best of our knowledge, we are the first to incorporate meaningful phase information for device-free human detection by successfully removing the randomness involved in the raw phase.   
—We propose a novel unified feature using the eigenvalue of the correlation matrix of CSI. The feature holds excellent properties for device-free detection due to its stability for both amplitude and phase and irrelevance to specific power parameters that vary over different links and over time and space.   
—We explore space diversity provided by multiantennas supported by modern MIMO communicating systems to enable more accurate and robust detection.   
—We present the design and implementation of PADS in commodity WiFi devices. Benefiting from full advantages of CSI, especially the sensitive phase feature, PADS is capable of detecting walking humans with dynamic speeds. Experiment results demonstrate that PADS can achieve high performance that outperforms traditional RSS-based and CSI-based systems.

A conference version of this work can be found in Qian et al. (2014). Instead of using linear transformation on phase information of CSI, we apply phase differences across antennas as a new feature. In addition, we provide a detailed description on manipulation of both amplitude and phase information of CSI to extract proper features. Finally, we redo the experiment to take impacts of more parameters into consideration. The adoption of new features improves the detection rate from 97% to 99%, with almost no false alarm.

The rest of the article is organized as follows. In Section 2, we present a brief review of recent innovations on device-free human detection. Section 3 gives an overview of the system architecture, while the detailed design is presented in the subsequent Section 4. In Section 5, we introduce the experiment settings and results. Finally, we conclude the work in Section 7.

# 2 RELATED WORKS

Device-free passive detection or localization has drawn much attention in the past years (Youssef et al. 2007). In this section, we briefly review the most related works on passive motion detection in pervasive wireless environments, which can be classified into two categories: RSS based and CSI based.

RSS-based detection. RSS is especially attractive for device-free detection since RSS measurements are easily accessible in existing wireless networks with commodity devices. Existing RSSbased passive detection or localization mainly relies on RSS changes due to target presence and movements. More specifically, a large value of RSS variance generally indicates a moving target in the monitoring area, while a small value infers none (Yang et al. 2010). The most well-known RSS-based device-free localization should be the Radio Tomographic Imaging (RTI) (Wilson and Patwari 2010), which deploys a sensor network around the target area and uses the RSS changes to localize and track a person. Several varieties of the RTI technique have been proposed, including the vRTI (Wilson and Patwari 2011) and mRTI (Wilson and Patwari 2010). RSS readings are also used for identifications of human movements such as walking, standing, and running (Archasantisuk and Aoyagi 2015). Another system, RASID (Kosba et al. 2012), improves the detection accuracy by analyzing the RSS features and adopting a nonparametric technique for adapting to environment changes. A more recent work (Zheng et al. 2013) experimentally shows that the localization performance degrades significantly when people are moving at dynamic speeds and thus proposes a scheme that adaptively adjusts the sample window size to facilitate localization accuracy based on the estimated speed. Benefiting from full advantages of CSI, especially the sensitive phase feature, our proposed system is also capable of detecting walking humans with dynamic speeds, yet without the complex speed estimation.

![](images/ef559c383ed7c77d861702f124758897a06d9a44f109b438829a0415e9ef2712.jpg)



Fig. 1. Architecture overview of PADS.

CSI-based detection. The CSI-based scheme has attracted more attention in recent years since CSI can be exported from commodity wireless NICs (Halperin et al. 2010; Yang et al. 2013). Similar to the RSS-based scheme, most CSI-based detection approaches also leverage variations in CSI measurement to infer target locations or presences. Pilot (Xiao et al. 2013) is an early attempt in device-free positioning, which leverages the correlation of CSI over time to monitor abnormal appearance and further locate the entity. Omni-PHD (Zhou et al. 2014) studies the omnidirectional sensing coverage for passive human detection using multipath effects captured by CSI. FIMD (Xiao et al. 2012) enables accurate fine-grained burst motion detection by exploiting the temporal stability of CSI in static environments. FCC (Xi et al. 2014) studies the relationship between the number of moving people and the variation of CSI and thus achieves device-free crowd counting. Despite that many works have investigated CSI for device-free detection, most of the previous approaches merely leverage the amplitude of CSI information and leave phase information unexplored. In this article, we first explore and incorporate phase with amplitude for device-free human detection.

Detection as prerequisite. Detecting moving objects acts as a prerequisite for many other wireless sensing techniques. For example, line-of-sight identification (Zhou et al. 2015b; Wu et al. 2015c) and respiration detection (Wu et al. 2015b) require a quasi-static environment to avoid contamination of detection features by artificial motion. In contrast, gesture recognition (Wang et al. 2015) needs to sense moving humans before starting recognition progress. Most of these works focus on their specific sensing purposes, yet resign detection of moving humans to simple threshold-based method. Thus, PADS is able promote performance of these works as a complementary function module of moving human detection.

# 3 OVERVIEW

As shown in Figure 1, we utilize the physical layer CSI as a primary indicator for human motion. CSI depicts the temporal and spectral structure properties of a wireless link when an RF signal propagates along multiple paths. The rationale for device-free human detection is that a fraction of propagation paths would be affected due to intruder presence. Specifically, for moving targets, this contributes to the dramatic changes in CSI over time, which can then be captured by the temporal variations of CSI. CSI can be measured and collected from commodity WiFi devices using off-the-shelf NICs such as Intel 5300 (Halperin et al. 2010). In modern multiple subcarrier radios like OFDM, CSI is usually portrayed in the frequency domain by the form of CFR.

To enable a fast and efficient detection system, three main components are incorporated in PADS, i.e., data preprocessing, feature extraction, and target detection. First, CSIs are exported from an off-the-shelf NIC that communicates with an ordinary wireless router. Raw CSI measurements could contain significant phase random noise and occasionally amplitude outliers. The phase random noise is supposed to be removed by the phase sanitization module. Meanwhile, an outlier filter is applied to eliminate outlier observation in amplitude sequences of CSI.

Feature extraction acts as the most critical part for accurate and efficient human detection. In PADS, we propose to exploit amplitude and phase information of CFR simultaneously. To avoid the influence of diverse transmitting power in specific scenarios, we devise a novel feature using the respective three maximum eigenvalues of the correlation matrices of amplitude and phase information over a certain time window.

The features are then fed to an inference model to alarm user movements. Instead of using a clustering algorithm, we adopt a threshold-like detection scheme. A cutoff line is precalibrated by employing a classical classification algorithm, i.e., SVM, on a certain amount of preliminary measurements. Movement inference is then done by comparing the amplitude and phase feature to the precalibrated values. The approach has advantages in zero data constraints and smaller response delay. Specifically, the clustering-based method would require collecting a group of data that contains measurements corresponding to at least two different states (Xiao et al. 2012), while the classification-based method can respond to each single data, according to the precalibrated cutoff line. Finally, to enhance the detection accuracy and robustness, multiple antennas in modern MIMO systems are also explored and integrated.

# 4 METHODOLOGY

In this section, we detail the design of PADS by real measurements.

# 4.1 Data Preprocessing

Leveraging the off-the-shelf NIC with slight driver modification, a group of CFRs on $N = 3 0$ subcarriers can be exported to up-layer users for every one packet in the format of CSI:

$$
H = \left[ H (f _ {1}), H (f _ {2}), \dots , H (f _ {N}) \right]. \tag {1}
$$

Each CSI represents the amplitude and phase of an OFDM subcarrier:

$$
H (f _ {k}) = \| H (f _ {k}) \| e ^ {j \angle H (f _ {k})}, \tag {2}
$$

where $H ( f _ { k } )$ is the CSI at the subcarrier $k ( k \in [ 1 , 3 0 ] )$ with central frequency of $f _ { k }$ , and $\angle H ( f _ { k } )$ denotes its phase (for convenience, we also use $\phi _ { k }$ to denote the phase in the following). To monitoring an area of interest, CSIs are continuously collected and K measurements within a specific time window form the CSI sequence, which can be denoted as

$$
\mathbb {H} = \left[ H _ {1}, H _ {2}, \dots , H _ {K} \right]. \tag {3}
$$

The K measurements of CFR then serve as the basic input for our movement detection algorithm, which will be first passed through a phase sanitization and an outlier filtering process.

![](images/e3a5df31305d13049529f4e26680ad1420cffa14d0f0de4ed200e12c4804ee9a.jpg)



Fig. 2. Phase before and after sanitization.

![](images/d6c3ba61182e77f7094d098c89cbd1eda1b2228f88c145db398aa9c43e9271e5.jpg)



Fig. 3. Outlier detection for CSI observations.

4.1.1 Phase Sanitization. Although CSI has been widely explored for various applications, most of them only consider amplitudes of either CFR or CIR and thus the counterpart of CSI, i.e., phase information, does not attract enough attention. One of the most important reasons lies in the unavailability of phase information on commodity devices (Sen et al. 2012; Xiao et al. 2013). As shown in Figure 2, due to random noise and an unsynchronized time clock between transmitter and receiver, raw phase information behaves extremely randomly over all feasible fields, making it inapplicable for any detection.

Specifically, the unwrapped measured phase $\hat { \phi } _ { i } ^ { j }$ for the $i ^ { t h }$ subcarrier of the $j ^ { t h }$ antenna can be expressed as

$$
\hat {\phi} _ {i} ^ {j} = \phi_ {i} ^ {j} - 2 \pi \frac {k _ {i}}{N} \delta + \beta_ {j} + Z, \tag {4}
$$

where $\boldsymbol { \phi } _ { i } ^ { j }$ denotes the true phase. δ is the timing offset at the receiver, which is defined as the time interval between time of signal arrival and signal detection. The timing offset $\delta$ causes phase error expressed as the middle term. $\beta _ { j }$ is an unknown phase offset, and Z is some measurement noise. $k _ { i }$ denotes the subcarrier index (ranging from −28 to 28 in IEEE 802.11n) of the $i ^ { t h }$ subcarrier, and N is the FFT size (which equals 64 in IEEE 802.11 $\mathrm { a / g / n ) }$ . Due to the unknowns listed above, it is infeasible to obtain the true phase shifts with solely commodity WiFi NICs.

In the conference version of this work (Qian et al. 2014), we show that significant components of random phase offsets can be removed by employing a linear transformation on the raw phase readings. However, the purpose can also be achieved by calculating phase differences across multiple antennas. With an intuitive analysis, we show that the phase difference has a larger variance and thus outperforms linear transformation of the phase on motion detection.

Linear transformation of phase. To mitigate the impact of random noise, we perform a linear transformation on the raw phases, as recommended in Sen et al. (2012). The key idea is to eliminate $\delta$ and $\beta$ by considering the phase across the entire frequency band. First, we define two terms a and b as follows:

$$
a = \frac {\hat {\phi} _ {n} - \hat {\phi} _ {1}}{k _ {n} - k _ {1}} = \frac {\phi_ {n} - \phi_ {1}}{k _ {n} - k _ {1}} - \frac {2 \pi}{N} \delta \tag {5}
$$

$$
b = \frac {1}{n} \sum_ {j = 1} ^ {n} \hat {\phi} _ {j} = \frac {1}{n} \sum_ {j = 1} ^ {n} \phi_ {j} - \frac {2 \pi \delta}{n N} \sum_ {j = 1} ^ {n} k _ {j} + \beta . \tag {6}
$$

If the subcarrier frequency is symmetric, which indicates $\begin{array} { r } { \sum _ { j = 1 } ^ { n } k _ { j } = 0 , } \end{array}$ b can be expressed as $\begin{array} { r } { b = \frac { 1 } { n } \sum _ { j = 1 } ^ { n } \phi _ { j } + \beta . } \end{array}$ . Subtracting the linear term $a k _ { i } + b$ from the raw phase $\hat { \phi } _ { i }$ , we obtain a linear combination of true phases, denoted as $\tilde { \phi } _ { i } ,$ , from which the random phase offsets have been removed (omitting the small measurement noise $Z )$ :

$$
\tilde {\phi} _ {i} = \hat {\phi} _ {i} - a k _ {i} - b = \phi_ {i} - \frac {\phi_ {n} - \phi_ {1}}{k _ {n} - k _ {1}} k _ {i} - \frac {1}{n} \sum_ {j = 1} ^ {n} \phi_ {j}. \tag {7}
$$

Difference of phase. The phase difference of any pair of antennas $j _ { 1 }$ and $j _ { 2 }$ , denoted as $\Delta \hat { \phi } _ { i } ^ { j _ { 1 } , j _ { 2 } }$ , is naturally free from phase noise caused by timing errors:

$$
\Delta \tilde {\phi} _ {i} ^ {j _ {1}, j _ {2}} = \hat {\phi} _ {i} ^ {j _ {1}} - \hat {\phi} _ {i} ^ {j _ {2}} = \Delta \phi_ {i} ^ {j _ {1}, j _ {2}} - 2 \pi \frac {k _ {i}}{N} \Delta \delta_ {j _ {1}, j _ {2}} + \Delta \beta_ {j _ {1}, j _ {2}}, \tag {8}
$$

where $\Delta \phi _ { i } ^ { j _ { 1 } , j _ { 2 } } = \phi _ { i } ^ { j _ { 1 } } - \phi _ { i } ^ { j _ { 1 } }$ is the difference of true phases, $\Delta \delta _ { j _ { 1 } , j _ { 2 } } = \delta _ { j _ { 1 } } - \delta _ { j _ { 2 } }$ is the difference of timing offsets, and $\Delta \beta _ { j _ { 1 } , j _ { 2 } } = \beta _ { j _ { 1 } } - \beta _ { j _ { 2 } }$ ,is the difference of unknown phase offsets. Note that all antennas ,have fixed time of signal arrival as the wireless devices used in PADS are fixed, and have the same random time of signal detection decided by hardware. Thus, $\Delta \delta _ { j _ { 1 } , j _ { 2 } }$ is a constant. Further, $\Delta \beta _ { j _ { 1 } , j _ { 2 } }$ is a constant since $\beta _ { j } { \bf s }$ , , are constant once the receiver starts up. As a result, the variances of phase difference $\Delta \tilde { \phi } _ { i } ^ { j _ { 1 } , j _ { 2 } }$ are only decided by variances of true phases. Thus, phase difference $\Delta \tilde { \phi } _ { i } ^ { j _ { 1 } , j _ { 2 } }$ can be used as an indicator of human motion.

Comparison of two methods. Figure 2 illustrates examples of the phase after sanitization with two methods, which distribute relatively stable as expected compared to the original random version. Although we could not claim the sanitized information is just the true phase, we do derive two usable and effective features of the true phase. Now, a natural question to ask is: which feature is better for detection of human motion? We answer this question by qualitative analysis.

Intuitively, with the simple assumption that true phases $\phi _ { i }$ are i.i.d, variances of derived phases $\tilde { \phi } _ { i }$ are approximately equal to variances of true phases:

$$
\sigma_ {\tilde {\phi} _ {i}} ^ {2} = C _ {i} \sigma_ {\phi} ^ {2}, \tag {9}
$$

where $C _ { i }$ is the amplified coefficient of variance of the $i ^ { t h }$ subcarrier and ranges between 0.5 and 1.5.

In contrast, variances of derived phase difference $\Delta \tilde { \phi } _ { i } ^ { j _ { 1 } , j _ { 2 } }$ are the sum of variances of true phases:

$$
\sigma_ {\Delta \tilde {\phi} _ {i} ^ {j _ {1}, j _ {2}}} = \sigma_ {\phi_ {i} ^ {j _ {1}}} ^ {2} + \sigma_ {\phi_ {i} ^ {j _ {2}}} ^ {2} = 2 \sigma_ {\phi} ^ {2}. \tag {10}
$$

Thus, phase difference tends to have higher variance and signify influence of human motion.

Figure 4 shows the example of variance of features exported by two sanitization methods. Apparently, the variance of phase difference is consistently larger than that of linear transformation on phase. The possible reason for the huge gap of variances of the two methods is that phases of different antennas separated by more than half the wavelength are independent, while phases of adjacent subcarriers of one antenna are highly correlated.

Moreover, linear transformation unnaturally assigns different weights $( \mathrm { i . e . , } C _ { i } )$ to variances of subcarriers. Specifically, the variances of phases of the first and last subcarriers are underweighted, with $C _ { i }$ less than 0.25, which may weaken the impacts of these subcarriers. For example, in the case shown in Figure 4(b), it is indicated that the largest phase variances exist at the first and last subcarriers. However, such large phase variances are weakened by linear transformation (Figure 4(a)), which reduces the distinction between phase features of static and motion cases.

Finally, comparing to linear transformation on phase, phase differences across antennas have clear physical meaning and are easy to compute. Thus, we redesign PADS by replacing linear transformation on phase with phase difference. For clarity, we directly use $\phi$ instead of $\Delta \tilde { \phi }$ to refer to the phase difference hereafter.

![](images/3f7d1d99bccbb5fd1759a5ec748fc00c22fcd67b98cddd78ac2b1bf7153f432b.jpg)



(a)Linear transformation on phase.

![](images/4d163f3c3d470d4be8edf50ea6ee026083f349881f277c3f6aa3098b268b66aa.jpg)



(b) Phase difference   
Fig. 4. Variance of features exported by two sanitization methods.

4.1.2 Outlier Filter. Outliers might appear in CSI measurements due to protocol specifications as well as environmental noise. As motion detection techniques mostly adopt variation-based detection whenever algorithms are used, such outliers could affect the movement detection performance a lot and thus should be sifted out before detecting motion. To identify and remove these biased measurements, we adopt a Hampel identifier (Davies and Gather 1993), which declares any point falling out of the closed interval $[ \mu - \gamma \sigma , \mu + \gamma \sigma ]$ as an outlier, where μ and σ are the median ,and the median absolute deviation (MAD) of the data sequence, respectively. γ is an applicationdependent parameter and the most widely used value is 3. Figure 3 illustrates the frequent outlier observations that might be contained in raw measurements and the results of outlier filtering (using window size and γ by default).

# 4.2 Feature Extraction

An appropriate feature plays a critical role in device-free detection, and feature extraction serves as the most important component of PADS. Various statistical features have been exploited for detection, such as variance (Wilson and Patwari 2011), mean (Wilson and Patwari 2010), distribution distance (Zhou et al. 2014; Zhao and Patwari 2012), and so forth. Different from previous works that mostly utilize a single feature from amplitude information, we seek for both amplitude-based and phase-based features and use them simultaneously for motion detection.

Although accounting for both amplitude and phase, we strive to search for unified feature metrics that are suitable for both sides, in order for light and practical learning-based detection scheme. Apparently, the feature metric should be absolute power irrelevant and possibly variance dependent, since transmitting power parameters would be adapted over different scenarios and thus are scenario dependent, while human movements contribute to disturbances of amplitude as well as phase. As illustrated in Figure 5 and Figure 6, one can see variances of both amplitude and phase in cases when human movements are significantly larger than those in static cases. Figure 7 further illustrates the variances over each individual subcarrier in cases of moving human presence and absence.

Motivated by these observations, we suspect that variances of amplitude and phase would be good indicators for abnormal appearance of moving people. Unfortunately, due to lack of knowledge on transmit power at the receiver side, variance cannot be normalized to adapt to diverse scenarios with various link states, and thus be directly used as a distinctive feature for human detection. As a consequence, we propose to extract features from the respective correlation matrix of CFR amplitude and phase of n sequential measurements over a certain time window. Denote -Hand Φ as the normalized CFR amplitude and phase sequence; then their corresponding covariance matrix is, respectively,

![](images/e590101a514bfb2b0b2390bea05d19d440247e087b6e212e5c99f62aea6a091e.jpg)



![](images/987a4282ee9cf97cf66a18e24faa5f603dff13a892ab507045e931b2b78474fd.jpg)



Fig. 5. Variances of amplitude increase significantly due to human movements.

![](images/d424c1b3ad924ad4b8b8ceed5183843153aac26078eefeb1f3e27431fce523bb.jpg)



![](images/afa4af0f5c29801cad1e77f770a1ae1a2424dcabf981225764b080d689885f0f.jpg)



Fig. 6. Variances of phase increase significantly due to human movements.

![](images/2fdb806a37f0ec7e12fbc4c8f67112387eaf72586a87e1117637591b4ab51450.jpg)



![](images/20bf29f6d7ee094aec9a1bad9f9e425223be5b3b77cf18e172024b5caa360220.jpg)



![](images/33a87e1eadda30d23c06dbc5df7b4c33bba17a51f7799b69c48aec389b72980c.jpg)



![](images/e8e6e40b0a44c23f0b96316a51390c44d9faaef0b49c4a39b95f0e797615a9f5.jpg)



Fig. 7. Variances of both amplitude and phase increase significantly due to human movements. (a) Subcarrier 10 of static case; (b) subcarrier 10 of dynamic case; (c) subcarrier 20 of static case; (d) subcarrier 20 of dynamic case.

$$
\mathrm{R} (| | \mathbb {H} | |) = [ \mathrm{R} (H _ {i}, H _ {j}) ] _ {K \times K}, \tag {11}
$$

$$
\mathrm{R} (\Phi) = \left[ \mathrm{R} (\phi_ {i}, \phi_ {j}) \right] _ {K \times K}, \tag {12}
$$

where $\mathrm { R } ( X _ { i } , X _ { j } )$ denotes the correlation between vectors $X _ { i }$ and $X _ { j }$ and is defined by covariance ,C between two vectors:

$$
\mathrm{R} (X _ {i}, X _ {j}) = \frac {\mathrm{C} (X _ {i} , X _ {j})}{\sqrt {\mathrm{C} (X _ {i} , X _ {i}) \mathrm{C} (X _ {j} , X _ {j})}}. \tag {13}
$$

For both matrices, with lower covariance values the link is more likely to be static and free of intrusion. In contrast, higher covariances would probably indicate the presence of moving humans who disturb the link.

![](images/fecb0e28236a5a39c38b700d11d4634274aa0089293ec3bb506eaab6541954a4.jpg)



Fig. 8. Preliminary classification result using SVM.

To extract a simple feature for further detection, we compute the eigenvalues of both matrices and select the maximum eigenvalue of each matrix, which finally forms a two-tuples $F = [ \alpha , \rho ]$ :

$$
\alpha = \max (e i g e n (\mathrm{R} (\| \mathbb {H} \|))), \rho = \max (e i g e n (\mathrm{R} (\Phi))). \tag {14}
$$

In practice, to guarantee the accuracy and robustness of detection, we further introduce the second maximum eigenvalue of amplitude and phase, respectively, and thus devise a four-tuple feature as $F = [ \alpha _ { 1 } , \alpha _ { 2 } , \rho _ { 1 } , \rho _ { 2 } ]$ , where $\alpha _ { 1 } , \alpha _ { 2 }$ and $\rho _ { 1 } , \rho _ { 2 }$ represent the respective maximum and sec-, , , , ,ond maximum eigenvalue for amplitude and phase. In Section 5, we will experimentally validate that more eigenvalues would result in better performance, while two are sufficient for achieving satisfied accuracy.

# 4.3 Motion Detection

Aiming at achieving calibration-free detection, there are generally two categories of methods that can be adopted: clustering based and threshold based. The former automatically clusters measurement data into several clusters and then distinguishes different clusters as different states (presence or absence of human) by comparing the center distance of each cluster. The latter seeks for a general threshold from partial precollected data and conducts state identification based on the threshold value. Although the clustering approach avoids both environment calibration and threshold training efforts, it implicitly assumes that at least two states are involved in each group of measurements to be processed (otherwise one cluster or several clusters corresponding to a same state result, leading to a miss or false detection), which is impractical for most applications. In contrast, the classification approach can classify each single measurement in real time by comparing the measurement with the general threshold. As a consequence, we adopt the threshold-based scheme assisted by SVM classification.

We first conduct an SVM-based classification on preliminary measurements collected from several scenarios. The above-mentioned feature factors $\alpha$ and $\rho$ are used as the input feature of the SVM. As shown in Figure 8, we are delighted to see that a clear gap can be found between the data corresponding to the presence or absence of moving humans. Moreover, although people with different moving speeds exhibit various values on each metric (since they induce diverse alterations on the signal propagation paths), the self-similarity within individual states is always remarkably smaller than cross-similarity of data corresponding to different states. This lays the fundamental underpinnings of detection of people with dynamic moving speeds. The rationale is that even slight motion can cause perceivable changes in CSI, which enables its detection.

![](images/cfe79e34ecbc941c6b94110dc0e118b13a38472143037c14a203fc5c151b3137.jpg)



Fig. 9. Antenna diversity of amplitude feature.

![](images/063d2b201b37493485c8a644aa41ce1750902e0b10b1a3e0383bde8642c81ec6.jpg)



Fig. 10. Antenna diversity of phase feature.

A precalibrated empirical cutting line is on this basis determined and then used to further moving human detection. The precalibrated cutting line, according to our measurements, would fit various scenarios including different propagation distances, channel attenuation, and different target behaviors. One key reason is that all the features involved are power independent but only relate to the extent of temporal changes.

# 4.4 Enhancement via Multiple Antennas

Noticing that multiple antennas are available in the more and more popular MIMO communicating systems, we also exploit multiple antennas to improve the precision and robustness of human detection.

As shown in Figure 9 and Figure 10, while the selected features of amplitude and phase do vary over different antennas, they still preserve the capability of distinguishing static and dynamic environments in most cases. Furthermore, it is very unlikely that multiple antennas simultaneously fail to sense motion. Thus, we use features extracted from multiple antennas together as the input of the SVM classifier.

# 5 EXPERIMENTS AND EVALUATION

# 5.1 Experimental Setup

To evaluate the performance of PADS, we conduct real experiments on commodity-ready COTS devices. Specifically, we use mini-desktops with three external antennas as AP and client. Both mini-desktops are equipped with Intel 5300 NIC and run Ubuntu 11.04 OS (Figure 12). We collect data from different scenarios: classrooms, labs, corridors, and meeting rooms (Figure 11). The classrooms and labs are large rooms with an area of about $8 0 m ^ { 2 }$ . The classrooms are furnished with low desks and chairs, while the labs are furnished with cubicles with high metal and glass fences and instruments. The meeting room is a small room with an area of $3 0 m ^ { 2 }$ and furnished with a conference table and chairs. The corridor is about 2m wide and 27m long, and is empty during the experiment. (Figure 13 and Figure 14 show two samples of these scenarios.) In each case, we let a volunteer walk through the monitoring area with different speeds (about 0 5m s 1m s 2m s) . / , / , /along a trajectory that traverses the space uniformly. We also collect data when there is no human presence or there are only stationary persons. In total, we collect mobile and static traces for more than 1 hour, respectively. Since multiple moving humans cause larger temporal variations than single moving humans and are thus easier for PADS to detect, we omit experiments on multiple moving humans.

![](images/03cbf90a12d297ee94ca26627a290abc75eadbadec1f68c4a7bdbfe74f2f281c.jpg)



Fig. 11. Experiment building (testing areas are highlighted).

![](images/6f8e05716c463b2dc3a357c7a02496c52805c5ef9853f89d5b1c2f270113f0ae.jpg)



Fig. 12. Mini-desktop.

![](images/e54f2e588b7dbbd6009200fd67d31d4b6da4def61ebfd511ae6b8f727025f911.jpg)



Fig. 13. Sample 1: Corridor.

![](images/8bbcaf9345790bbb44beefd9689e2ad79c7f0c6f23cdbeb334dec8699d246116.jpg)



Fig. 14. Sample 2: Lab.

In different scenarios, the AP is placed at various heights from 1.2m to 2m. Diverse TX-RX distances from 2m to 7m are also considered. In addition, LOS and NLOS conditions (when the AP is blocked by the wall) are also both involved.

By working in monitor mode, the packet transmission rate of Intel 5300 NIC can be as large as 1,000Hz. Thus, we set the original packet rate as 1,000Hz and downsample CSI data with multiple integrals (1, 2, 5, 10, 20) to assess performance of PADS with different transmission rates (1,000Hz, 500Hz, 200Hz, 100Hz, 50Hz). The transmission rate of 200Hz is used as the default transmission rate.

# 5.2 Performance Evaluation

5.2.1 Evaluation Metric. We use the following two metrics to evaluate the performance of our proposed PADS system based on phase difference, as well as the PADS system in the conference version of this work and the FIMD system, in respective environments. For clarity, we denote PADS with phase difference as PADS-PD, and PADS with linear transformation on phase as PADS-LT.

—True-Negative (TN) Rate: The TN rate is the probability that the static environment is correctly classified.   
—True-Positive (TP) Rate: The TP rate is the probability that the human motion events are correctly detected.

5.2.2 Overall Performance. To assess the overall performance of PADS, we adopt a common parameter setting where sliding window size is 1s and three eigenvalues of both amplitude and phase are used as features. We train the SVM classifier with data collected in both static and dynamic scenarios at all places, and test the classifier with other data collected at each place.

![](images/6b96d52c103da6c077d83c848beb1a4b614016e03eb8b047f22f417021f307dc.jpg)



Fig. 15. TN rate of static cases.

![](images/d6c2d75ae763a0e87c68351a83e960362c3aead8e7f3be71e9e947f71c193a1f.jpg)



Fig. 16. TP rate of cases with human motion.

Figure 15 shows the TN rates of systems working in static scenarios at different places. All methods achieve excellent performance with TN rates almost equal to 100%. The result is consistent with the assumption that CSI gathered in a static environment is stable and highly correlated.

Figure 16 shows TP rates of systems working in dynamic scenarios where a volunteer walks in the monitor area with various speeds. PADS with different phase sanitization methods consistently achieves a TP rate higher than 93%, while PADS-PD outperforms PADS-LT at all places, which demonstrates that phase difference is better at capturing environmental change than the previous linear transformation method. As a comparison, the performance of FIMD is comparable to PADS at three out of four places. However, the TP rate of FIMD drops significantly to 80% when tested at the corridor, which means simply using amplitude features is not sufficient for obtaining a universal classifier.

The three detection systems work well in regular rooms like the classroom, lab, and meeting room, which means that the size of and furniture in the room have little impact on performance. However, the three systems experience the same trend of degradation of performance in the corridor, though to different extent, which means that the shape of the monitor area plays an important role. In fact, the shape of the monitor area limits the deployment of transceivers in the area. Specifically, in the corridor, the transceivers can only be deployed in parallel with the corridor (see Figure 13). As a result, when humans pass transceivers and get away from the LoS path of the link, they are at the areas that are most hard to detect due to unidirectional elliptical coverage of the link (Zhou et al. 2014). Thus, using CSI amplitude only is insufficient for motion detection in these areas. In contrast, by adding the sensible CSI phase as one extra dimension of feature, PADS is able to sense signal variations caused by human motion even in these extreme cases, and achieves significantly less degradation than FIMD.

Before analyzing the influence of different parameters on the performance of PADS, we first present the final assessed results. With common parameter settings, PADS accurately alarms human movements by 99% on average with almost no false-negative error.

5.2.3 Impacts of Sliding Window Size. Intuitively, the larger the size of the sliding window is, the better the performance gains, since the influence of human motion would be more probably captured by using a longer time window of data. The intuition can be verified in Figure 17, which shows the change of detection rate against window size. As the window size increases, detection rates of all three systems consistently increase and converge to some detection rates larger than 97%. However, although we argue that an extremely longer sliding window may inversely degrade detection performance due to temporal variance of CSI in the conference version of this work (Qian et al. 2014), such a trend is not observed in the present experiment, meaning that for sliding windows less than 2s, the influence of temporal variance is not significant.

![](images/b46ef9370e0befa035603447ddb9b9144e2f6b592a7251acdce498dd65bf0e18.jpg)



Fig. 17. Relationship of detection rate and sliding window size.

![](images/6f2ab4cacad9b4f8c048826343187b168b1a6664be65c46d152d700792989a78.jpg)



Fig. 18. Relationship of detection rate and number of features.

Moreover, PADS-PD continuously outperforms the other two systems when the window size increases from 0.2s to 2s. Especially, even with a window size as short as 0.2s, PADS-PD is still able to achieve a relatively high detection rate of 94%, while PADS-LT and FIMD can detect at most 86% of motion cases. By using a short window size, PADS-PD is able to save a large amount of computation resources, while still maintaining a reasonable detection rate for practical human motion detection.

5.2.4 Impacts of Number of Features. In general, the more eigenvalues are used as features, the higher detection rate the system can achieve, since more information is leveraged. Figure 18 shows the performance of three systems when different numbers of features are employed. The impact of the number of features can be separated as two phases. When the number of features is less than three, adding a (pair of) eigenvalue may significantly increase the detection rate. In contrast, when the number of features exceeds three, the detection rate just slightly increases. The result indicates that major information of human motion centers upon the first three eigenvalues of correlation matrices of both amplitude and phase. Practically, using the first three eigenvalues is sufficient for motion detection. Note that features other than eigenvalues can also be incorporated to further improve the detection. However, since PADS-PD already achieves an accuracy of 99% with only the first three eigenvalues, the gain in performance by incorporating other features is marginal, yet may incur more computing cost. Thus, we omit the discussion on selection of different features.   
5.2.5 Impacts of Number of Antennas. The impacts on detection performance of number of antennas we leveraged in the PADS system are studied by testing in different places. Figure 19 shows the promotion of the detection rate by using multiple antennas against a single antenna. While using a single antenna yields excellent results in most cases, using multiple antennas further improves the performance of the PADS system in “hard” cases (corridor) for a single antenna. Except for those cases that are completely detected with a single antenna, using multiple antennas improves the performance of the PADS system significantly, due to the decreasing impacts of “bad” antennas used in the PADS system.   
5.2.6 Impact of Transmission Rate. Performance of detection can benefit from a high transmission rate in the form of finer features. Figure 20 shows the relationship between detection rate and transmission rate. Obviously, as the transmission rate increases, the detection rates of all systems increase. The reason is that the variance of CSI can be captured more precisely by using more CSI samples in a fixed timing window.

![](images/57266069fe2f31e180cce468840f17dec2477c8843fcabf70b6b2973068c3d26.jpg)



Fig. 19. Detection rate of cases with different number of antennas.

![](images/41b700f8b48bd5c18a4acf9f104de3a6ba5e8ba5329e615c615a3fb292a347f1.jpg)



Fig. 20. Relationship of detection rate and transmission rate.

![](images/5de75ece3fb0a918569ccfa1b6837a5697c1d8f08ae773669d78ea8f562dd903.jpg)



Fig. 21. Detection rate of human motions with dynamic speed.

![](images/db49c8cedb70ef8c1354f391045929e02f36cc620239a5b8ec2f8000bf7671c6.jpg)



Fig. 22. Cross-validation of detection with dynamic speed.

The result also demonstrates that, comparing to PADS-LT and FIMD, the newly proposed PADS-PD is able to achieve a high detection rate even with a transmission rate of only 50Hz, which means PADS-PD can be deployed in the current WiFi infrastructure with minimum computation and networking cost.

5.2.7 Performance against Dynamic Speed. So far, we have been focusing on the general performance of the PADS system. To study the beneficial gain of more sensitive features used in our system, we compare the performance of the PADS and FIMD systems in different scenarios when the intruders walk with dynamic speeds. Figure 21 shows the detection rate of human motion with different speeds. With humans walking slowly, all three systems experience a fall in performance, yet to different extents. The degradation of PADS-PD is statistically less than PADS-LT and FIMD, which demonstrates the higher sensitivity of phase difference, compared with linear transformation on phase and amplitude, as features for detection of slow motion.

Finally, we cross-validate classification with dynamic speeds. Specifically, we train classifiers using CSI data with different human walking speeds and test each classifier against CSI data with these speeds. Figure 22 illuminates that the classifier trained by CSI data with a slower speed yields the best detection rate, which is consistent with our intuition that it is harder to distinguish walking of slow speeds than of fast speeds. The cross-validation result also provides a guideline for gathering training data for the system. That is, gathering CSI data where humans walk at slow speeds is sufficient and necessary for obtaining a high-quality classifier.

# 6 DISCUSSION

Finding true CSI phase. Whether there is a linear transformation on phase or phase difference is the compromise between nonignorable phase noises and stable phase features. As noted in Equation (4), timing, frequency, and sampling offsets due to imperfection of wireless devices contribute to phase noise. Recently, Splicer (Xie et al. 2015) was proposed to reveal the true CSI phase from contaminated measurements and further splice the CSI measurements from multiple WiFi frequency bands to derive high-resolution power delay profiles. PADS can benefit from Splicer by using the true phase generated by Splicer, which has a higher degree of freedom than phase difference across antennas. In addition, by splicing CSI measurements from multiple bands together, CSI measurements from more subcarriers are available and the correlation between CSI measurements can be more accurate. However, Splicer requires tens of CSI measurements to derive one CSI measurement with true phase, which limits the sampling rate of CSI as low as 17Hz. PADS, as well as other contactless sensing works, cannot work well at such a low sampling rate. Thus, improving the efficiency of Splicer and improving the sensitivity of PADS are two ways for solving the problem of low sampling rate.

Detecting static human. Although working well even when humans walk at very slow speeds, PADS is only able to detect moving humans due to its theoretical basis. When humans are quasistatic, PADS cannot tell humans from the static environment even if the human is in the monitor area. Fortunately, humans cannot be absolutely static, due to life processes such as breathing and heartbeat, which provides the possibility for detection of static humans. However, such tiny motions of the human body are easily drowned out by fluctuations of CSI measurements as humans are away from the wireless link. In order to catch such tiny motions, finer propagation models and more sensitive features are undoubtedly required (Wu et al. 2015b; Liu et al. 2014).

# 7 CONCLUSIONS

In this study, we design and implement a WiFi-based sensing system for passive detection of moving targets. To the best of our knowledge, this is the first study to exploit the more sensitive phase information other than amplitude information in this field. We have conducted extensive experiments and the evaluation results show that both sensitivity and robustness are improved simultaneously compared with previous approaches. We open up the utilization of CSI’s phase information for passive target detection, and future work will focus on taking full advantage of CSI.

# REFERENCES

Fadel Adib, Zach Kabelac, Dina Katabi, and Robert C. Miller. 2014. 3D tracking via body radio reflections. In 2014 14th USENIX Symposium on Networked Systems Design and Implementation (NSDI’14). USENIX, 317–329.   
Sukhumarn Archasantisuk and Takahiro Aoyagi. 2015. The human movement identification using the radio signal strength in WBAN. In 2015 9th IEEE International Symposium on Medical Information and Communication Technology (ISMICT’15). IEEE, 59–63.   
Laurie Davies and Ursula Gather. 1993. The identification of multiple outliers. J. Amer. Statist. Assoc. 88, 423 (1993), 782–792.   
Daniel Halperin, Wenjun Hu, Anmol Sheth, and David Wetherall. 2010. Predictable 802.11 packet delivery from wireless channel measurements. ACM SIGCOMM Computer Communication Review 40, 4 (2010), 159–170.   
Bryce Kellogg, Vamsi Talla, and Shyamnath Gollakota. 2014. Bringing gesture recognition to all devices. In 2014 14th USENIX Symposium on Networked Systems Design and Implementation (NSDI’14). USENIX, 303–316.   
Ahmed E. Kosba, Ahmed Saeed, and Moustafa Youssef. 2012. Rasid: A robust WLAN device-free passive motion detection system. In 2012 10th IEEE International Conference on Pervasive Computing and Communications (PerCom’12). 180–189.   
Xuefeng Liu, Jiannong Cao, Shaojie Tang, and Jiaqi Wen. 2014. Wi-Sleep: Contactless sleep monitoring via WiFi signals. In 2014 IEEE Real-Time Systems Symposium (RTSS’14). IEEE, 346–355.   
Neal Patwari and Joey Wilson. 2010. Rf sensor networks for device-free localization: Measurements, models, and algorithms. Proc. IEEE 98, 11 (2010), 1961–1973.

Qifan Pu, Sidhant Gupta, Shyamnath Gollakota, and Shwetak Patel. 2013. Whole-home gesture recognition using wireless signals. In Proceedings of the 19th Annual International Conference on Mobile Computing & Networking (MobiCom’13). ACM, 27–38.   
Kun Qian, Chenshu Wu, Zheng Yang, Yunhao Liu, and Zimu Zhou. 2014. PADS: Passive detection of moving targets with dynamic speed using PHY layer information. In 2014 20th IEEE International Conference on Parallel and Distributed Systems (ICPADS’14). IEEE, 1–8.   
Moustafa Seifeldin, Ahmed Saeed, Ahmed E. Kosba, Amr El-Keyi, and Moustafa Youssef. 2013. Nuzzer: A large-scale devicefree passive localization system for wireless environments. IEEE Trans. Mobile Comput. 12, 7 (2013), 1321–1334.   
Souvik Sen, Bozidar Radunovic, Romit Roy Choudhury, and Tom Minka. 2012. You are facing the Mona Lisa: Spot localization using PHY layer information. In Proceedings of 10th International Conference on Mobile Systems, Applications, and Services (MobiSys’12). ACM, 183–196.   
Longfei Shangguan, Zheng Yang, Alex X. Liu, Zimu Zhou, and Yunhao Liu. 2017. STPP: Spatial-temporal phase profilingbased method for relative RFID tag localization. IEEE/ACM Trans. Network 25, 1 (2017), 596–609.   
Xiaohua Tian, Ruofei Shen, Duowen Liu, Yutian Wen, and Xinbing Wang. 2017a. Performance analysis of RSS fingerprinting based indoor localization. IEEE Trans. Mobile Comput. 16, 10 (2017), 2847–2861.   
Xiaohua Tian, Zhenyu Song, Binyao Jiang, Yang Zhang, Tuo Yu, and Xinbing Wang. 2017b. HiQuadLoc: A RSS fingerprinting based indoor localization system for quadrotors. IEEE Trans. Mobile Comput. 16, 9 (2017), 2545–2559.   
Wei Wang, Alex X. Liu, Muhammad Shahzad, Kang Ling, and Sanglu Lu. 2015. Understanding and modeling of WiFi signal based human activity recognition. In Proceedings of the 21st Annual International Conference on Mobile Computing and Networking. ACM, 65–76.   
Joey Wilson and Neal Patwari. 2010. Radio tomographic imaging with wireless networks. IEEE Trans. Mobile Comput. 9, 5 (2010), 621–632.   
Joey Wilson and Neal Patwari. 2011. See-through walls: Motion tracking using variance-based radio tomography networks. IEEE Trans. Mobile Comput. 10, 5 (2011), 612–621.   
Chenshu Wu, Zheng Yang, and Yunhao Liu. 2015a. Smartphones based crowdsourcing for indoor localization. IEEE Trans. Mobile Comput. 14, 2 (2015), 444–457.   
Chenshu Wu, Zheng Yang, Zimu Zhou, Xuefeng Liu, Yunhao Liu, and Jiannong Cao. 2015b. Non-invasive detection of moving and stationary human with WiFi. IEEE J. Selected Areas Comm. 33, 11 (2015), 2329–2342.   
Chenshu Wu, Zheng Yang, Zimu Zhou, Kun Qian, Yunhao Liu, and Mingyan Liu. 2015c. Phaseu: Real-time los identification with WiFi. In 2015 IEEE Conference on Computer Communications (INFOCOM’15). IEEE, 2038–2046.   
Wei Xi, Jizhong Zhao, Xiang-Yang Li, Kun Zhao, Shaojie Tang, Xue Liu, and Zhiping Jiang. 2014. Electronic frog eye: Counting crowd using WiFi. In 2014 IEEE Conference on Computer Communications (INFOCOM’14). IEEE, 361–369.   
Jiang Xiao, Kaishun Wu, Youwen Yi, Lu Wang, and Lionel M. Ni. 2012. FIMD: Fine-grained device-free motion detection. In 2012 18th IEEE International Conference on Parallel and Distributed Systems (ICPADS’12). IEEE, 229–235.   
Jiang Xiao, Kaishun Wu, Youwen Yi, Lu Wang, and Lionel M. Ni. 2013. Pilot: Passive device-free indoor localization using channel state information. In 2013 33th IEEE International Conference on Distributed Computing Systems (ICDCS’13). IEEE, 236–245.   
Yaxiong Xie, Zhenjiang Li, and Mo Li. 2015. Precise power delay profiling with commodity WiFi. In Proceedings of the 21st Annual International Conference on Mobile Computing and Networking (MobiCom’15). ACM, 53–64.   
Jie Yang, Yong Ge, Hui Xiong, Yingying Chen, and Hongbo Liu. 2010. Performing joint learning for passive intrusion detection in pervasive wireless environments. In 2010 IEEE Conference on Computer Communications (INFOCOM’10). IEEE, 1–9.   
Zheng Yang, Chenshu Wu, and Yunhao Liu. 2012. Locating in fingerprint space: Wireless indoor localization with little human intervention. In Proceedings of the 18th Annual International Conference on Mobile Computing and Networking (MobiCom’12). ACM, 269–280.   
Zheng Yang, Chenshu Wu, Zimu Zhou, Xinglin Zhang, Xu Wang, and Yunhao Liu. 2015. Mobility increases localizability: A survey on wireless indoor localization using inertial sensors. ACM Comput. Surv. (CSUR) 47, 3 (2015), 54.   
Zheng Yang, Zimu Zhou, and Yunhao Liu. 2013. From RSSI to CSI: Indoor localization via channel response. ACM Comput. Surv. (CSUR) 46, 2 (2013), 25.   
Moustafa Youssef, Matthew Mah, and Ashok Agrawala. 2007. Challenges: Device-free passive localization for wireless environments. In Proceedings of the 13th Annual International Conference on Mobile Computing and Networking (Mobi-Com’07). ACM, 222–229.   
Yang Zhao and Neal Patwari. 2012. Histogram distance-based radio tomographic localization. In Proceedings of the 11th International Conference on Information Processing in Sensor Networks (IPSN’12). ACM, 129–130.   
Xiuyuan Zheng, Jie Yang, Yingying Chen, and Yu Gan. 2013. Adaptive device-free passive localization coping with dynamic target speed. In 2013 IEEE Conference on Computer Communications (INFOCOM’13). IEEE, 485–489.

Zimu Zhou, Chenshu Wu, Zheng Yang, and Yunhao Liu. 2015a. Sensorless sensing with WiFi. Tsinghua Science and Technology 20, 1 (2015), 1–6.

Zimu Zhou, Zheng Yang, Chenshu Wu, Shangguan Longfei, Haibin Cai, Yunhao Liu, and Lionel M. Ni. 2015b. WiFi-based indoor line-of-sight identification. IEEE Trans. Wireless Comm. 14, 11 (2015), 6125–6136.

Zimu Zhou, Zheng Yang, Chenshu Wu, Longfei Shangguan, and Yunhao Liu. 2014. Omnidirectional coverage for device-free passive human detection. IEEE Trans. Parallel Distrib. Syst. 25, 7 (July 2014), 1819–1829.

Received December 2015; revised January 2017; accepted October 2017