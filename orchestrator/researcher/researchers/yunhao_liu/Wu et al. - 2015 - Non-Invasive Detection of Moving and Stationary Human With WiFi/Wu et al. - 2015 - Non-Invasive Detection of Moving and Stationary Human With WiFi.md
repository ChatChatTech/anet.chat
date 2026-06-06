# Non-invasive Detection of Moving and Stationary Human with WiFi

Chenshu Wu, Student Member, IEEE, Zheng Yang, Member, IEEE, Zimu Zhou, Student Member, IEEE, Xuefeng Liu, Member, IEEE, Yunhao Liu, Fellow, IEEE, and Jiannong Cao, Fellow, IEEE

Abstract—Non-invasive human sensing based on radio signals has attracted numerous research interests and fostered a broad range of innovative applications of localization, gesture recognition, smart health-care, etc, for which a primary primitive is to detect human presence. Previous works have studied to detect moving humans via signal variations caused by human movements. For stationary people, however, existing approaches often employ a prerequisite scenario-tailored calibration of channel profile in human-free environments. Based on in-depth understanding of human motion induced signal attenuation reflected by PHY layer channel state information (CSI), we propose DeMan, a unified scheme for non-invasive detection of moving and stationary human on commodity WiFi devices. DeMan takes advantages of both amplitude and phase information of CSI to detect moving targets. In addition, DeMan considers human breathing as an intrinsic indicator of stationary human presence and adopts sophisticated mechanisms to detect particular signal patterns caused by minute chest motions, which could be destroyed by significant whole-body motion or hidden by environmental noises. By doing this, DeMan is capable of simultaneously detecting moving and stationary people with only a small number of prior measurements for model parameter determination, yet without the cumbersome scenario-specific calibration. Extensive experimental evaluation in typical indoor environments validates the great performance of DeMan in case of various human poses and locations and diverse channel conditions. Particularly, DeMan provides detection rate of around 95% for both moving and stationary people, while identifies human-free scenarios by 96%, all of which outperforms existing methods by about 30%.

Index Terms—Non-invasive, human detection, calibration-free, human breathing, Channel State Information

# I. INTRODUCTION

Recent advances in WiFi techniques have enabled a range of ubiquitous applications where wireless signals convey human body induced radio shadowing and reflections. Typical applications include human detection for intruder detection, emergency responses, and in-home children and elderly monitoring. Pioneer efforts have explored the possibility of extracting motion information from wireless signals to localize or track whole-body motions [1]–[3] or even gestures [4], [5] noninvasively. The term “non-invasive”, a.k.a passive or devicefree, means that people are not assumed to carry any wireless device. The primary underpinning is that a person’s movement

C. Wu, Z. Yang and Y. Liu are with the School of Software and TNList, Tsinghua University. Z. Zhou is with the Hong Kong University of Science and Technology. (email: {wucs32, hmilyyz, zhouzimu.hk}@gmail.com; yunhao@greenorbs.com).   
X. Liu and J. Cao are with the Department of Computing, Hong Kong Polytechnic University. (email: {csxfliu, csjcao}@comp.polyu.edu.hk).   
Manuscript received 15 Aug. 2014; revised 26 Nov. 2014; accepted 25 Jan. 2015. Date of publication xx XX. 2015.

can modulate wireless signals and result in temporal changes that are observable from received signals [1]. The mobility of to-be-observed users makes a prerequisite of existing passive human detection systems. However it is intrinsically challenging to detect stationary users based on radio reflections [6]. To detect the presence of stationary people, existing schemes employ a prerequisite calibration of channel profile in humanfree environments, and simplify human presence as shadowing on the Line-Of-Sight (LOS) path [7]. The calibration needs to be conducted offline to collect a link profile for human-free settings and online detection is accomplished by comparing the real-time measurements against the static profile. Despite the cumbersome scenario-tailored profiling, such schemes may still fail due to temporal environmental unstableness and multipath effects [8].

In this work, we ask the following questions: Is it possible to detect stationary people passively without any scenariotailored calibration? Furthermore, can we build a unified framework with commodity WiFi devices to simultaneously detect both moving and static persons? We investigate the interference of human presence on wireless signals and demonstrate that the rhythmic chest’s rise and fall that alternate between inhaling and exhaling of human breathing induce repetitive changes on received signals, shedding promising lights on the non-invasive detection of static people. To deliver these observations into a practical human detection scheme, multiple challenges need to be overcome: 1) How to discover and harness weak human breathing patterns from wireless signals in the presence of environmental unstableness? 2) How to integrate the detection of moving and stationary humans into a unified framework without obscuring the minute breathinginduced chest motion with significant body motions?

To address these challenges, we propose DeMan, a unified scheme for non-invasive DEtection of moving and stationary huMAN with commodity WiFi devices. DeMan leverages the PHY layer Channel State Information (CSI) provided by commercial WiFi products, which offers fine-grained channel description at the granularity of OFDM subcarriers [9]. To differentiate macro human movements and micro chest motion of breathing, we propose a motion interference indicator based on the variances of CSI to provide a primary judgement of two cases: 1) if a moving person is more likely to present, De-Man starts the moving human detection module; 2) otherwise the stationary human detection module is chosen.

On one hand, to detect moving targets, we explore the full potential of CSI in both perspectives of amplitude and phase. We demonstrate that phase information is similarly or even more sensitive to environmental changes, which, however, has not been sufficiently utilized to the comparable extent of amplitude [10]. To extract environment-independent features of both signal amplitude and phase, we propose the maximum eigenvalues of correlation matrices of successive measurements to characterize the variations of temporal wireless signals.

On the other hand, to detect stationary people, DeMan processes the received signals with a bandpass filter to extract the signal components within an interest frequency band (corresponding to the normal frequency range of human breathing). Then we justify a sinusoidal model to formulate the breathing-induced wave-like patterns on wireless signals and detect a breathing person by searching for periodic signals of concerned frequencies. DeMan further harnesses the frequency diversity of modern OFDM modulation to enable static people detection under complicated and diverse human poses and locations.

We prototype DeMan on commodity WiFi devices and evaluate its performance in various scenarios of typical indoor buildings. Experiment results, from over 8-hour measurements in one week, demonstrate that DeMan achieves respective true positive rate for moving and stationary people of 94.82% and 93.33% and a true negative rate of 96.25% for humanfree scenarios, outperforming previous approaches by about 30%. DeMan uses a small number of prior measurements to determine several scenario-independent parameters, which are then applicable to different contexts. Consequently, DeMan requires no scenario-specific calibration, which is beyond the achievement of previous works for stationary target detection. We envision it as an important step towards fully practical technology of device-free human detection.

In summary, the core contributions are as follows:

• We propose a unified framework for simultaneous detection of moving and stationary people. To the best of our knowledge, this is the first solution that converges the advantages of purely WiFi-based, scenario-specific calibration free, and non-invasive together in the literature.   
• We design and implement a unified detection approach for stationary persons by modeling and exploiting minute chest motions of human breathing as an intrinsic indicator for human presence. Different from power fading, chest motion analysis enables DeMan to accurately detect stationary people not only on the direct LOS path, but also on the reflected paths with a single wireless link, resulting in an extended sensing coverage.   
• We investigate previously unexplored phase information of CSI and propose a novel method to extract and analyze phase feature, which is demonstrated to improve the accuracy and sensitivity of moving target detection.

The rest of the paper is organized as follows. We review the related works in Section II and present some preliminaries in Section III. Section IV presents an overview of the system as well as designs of the motion interference indicator and moving target detection, while details of stationary target detection are introduced in Section V. Section VI provides the performance evaluation. We discuss the limitations and future works in Section VII and conclude this work in Section VIII.

# II. RELATED WORKS

The design of DeMan is closely related to the following categories of research.

Wireless Non-invasive Human Detection. Wireless noninvasive human detection systems detect and localize humans via their impact on received signals, while the targets carry no wireless-enabled devices. The basic principles differ for stationary and mobile targets. To detect moving users, the variance of the RSS measurements is directly compared with a predefined threshold [1], while the mean of RSS measurements is compared with that of a normal profile when there are no users in the monitored area to detect motionless users [7]. Recent advances explore stationary and moving target detection based on signal envelope features [6] at the cost of a dense deployed wireless links. Some works develop sophisticated mechanisms for through-wall imaging of subjects (including occluded ones) using RF signals [11]–[13]. One of the latest innovations [14] develops a theoretical and experimental framework with only WiFi power measurements for the problem. In this work, we also aim at detecting both stationary and moving humans, yet dive into the PHY layer in purpose of achieving robust detection with a single wireless link in even multipath-dense indoor environments. Our scheme is able to distinguish the impact of a stationary human and static environmental interference such as the location change of furniture by capturing the unique breathing patterns.

Wireless-based Gesture and Activity Detection. Since wireless signals may be reflected differently with changes of human postures, numerous efforts have utilized wireless signals to detect whole-body [4], [15] or hand gestures [16] and daily activities [17] by analyzing the received signal patterns. Some work extracts Doppler features from received signals using customized OFDM signal processing [4], or leveraging Inverse Synthetic Aperture Radar (ISAR) to enable throughwall gesture sensing [15]. Alternatively, a pattern matching based approach can be employed to recognize hand gestures [5] or daily activities [17] on commodity WiFi devices. The tradeoff, however, is to build up a gesture profile database inadvance. In this work, we also aim to detect humans via their reflected signal patterns, but target at the much more micro motion, i.e. breathing. We try to capture the tiny impact of breathing on wireless signals harnessing the repetitive patterns of breathing.

Contactless Breath Detection. Breath is an important vital sign and active research has been conducted to monitor breath via chest movements or inhaling airflow measured by wearable sensors [18]. A promising alternative is to exploit wireless signals to detect breathing unobtrusively by capturing chest motions during breathing [19] utilizing costly radar infrastructure. Some pioneer work has demonstrated the viability of detecting breaths using commodity wireless devices [20], yet requires multiple transceivers to create a dense network of links. The closest to our works are [21] and [22], which enable non-intrusive breath monitoring on a single wireless link with directional antennas and dedicatedly placed transmitter-receiver pairs, respectively. Nevertheless, they are effective only when people present closely to short LOS links.

![](images/97253c2ecddd3018d77f66633b215389a7d59b6ec39ac0521961de0c4fe8737f.jpg)



Figure 1: System architecture of DeMan

Moreover, these systems are primarily designed for health-care and sleep monitoring applications, where persons are required to be lying on beds. Hence, they cannot be directly adopted for intruder detection or other ubiquitous applications, where users are not expected to always appear at a fixed location. Unlike [20]–[22], DeMan is able to detect breaths over a wider area without dense links and designed link placement, thus extending its applications to intruder detection, emergency responses, and in-home children and elder monitoring, etc, where user presence is unrestricted and unpredictable.

CSI-based Indoor Localization. As a promising substitute for MAC layer RSSI, the fine-grained PHY layer CSI available on commercial WiFi devices has raised increasing enthusiasm on CSI based indoor localization with meter-level accuracy [23], [24]. Since CSI depicts frequency diversity at the granularity of OFDM subcarriers, it also benefits non-invasive human detection as a more informative signature, and has been employed in non-invasive motion detection [25], entity localization [23], crowd counting [26] and walking activity recognition [17]. Our human detection system also builds upon the fine-grained CSI measurements. Nevertheless, unlike existing efforts that either assume moving targets [25], [26] or require signature collection and matching [17], we provide a unified framework to detect both moving and stationary humans without prior signature collection.

# III. PRELIMINARY

With the increase of operating bandwidth and the need to support MIMO techniques, current WiFi devices start to track fine-grained channel measurements leveraging Orthogonal Frequency Division Modulation (OFDM). An OFDM WiFi transmitter (IEEE 802.11a/g/n) sends bits through multiple subcarriers in parallel, and the receiver detects the start of each OFDM packet via a pre-defined preamble [27]. The preamble also facilitates the receiver to estimate channel conditions on each subcarrier [28]. Channel condition on each subcarrier involves both amplitude attenuation and phase shift, and can be represented by a complex number. With commodity WiFi Network Interface Cards (NICs) such as Intel 5300 and slight firmware modification, a group of 30 subcarrier channel measurements can be revealed to upper layer users in the format of Channel State Information (CSI) [9]:

$$
H _ {k} = \| H _ {k} \| e ^ {j \angle H _ {k}} \tag {1}
$$

where $H _ { k }$ is the CSI at the subcarrier k with central frequency of $w _ { k }$ , and $\| H _ { k } \|$ and $\angle H _ { k }$ denote its amplitude and phase, respectively.

Compared with the conventional MAC layer Received Signal Strength Indicator (RSSI), CSI offers finer-grained information in two aspects:

• Phase Information: In multipath-dense indoor environments, wireless signals usually propagate to the receiver through multiple paths. These multipath components can superpose either constructively or destructively depending on their relative phases. Since RSSI only offers amplitude information, previous research explores indirect proxy such as fade level to infer the phase superposition status [8]. In contrast, CSI provides both subcarrier phase and amplitude information, which holds potential for more sensitive and accurate motion detection.   
• Frequency Diversity: In essence, RSSI depicts the total received power across all subcarriers. Therefore, RSSI fails to characterize multipath propagation, which may convey the subtle breathing patterns. Since the subcarriers in OFDM tend to fade independently, CSI brings about opportunities to optimize and magnify the breathing patterns leveraging frequency diversity. It may also extend detection range since breathing patterns from a NLOS path may also be captured and resolved.

In a nutshell, CSI exposes a finer-grained spectral structure of wireless channels. In the subsequent sections, we strive to harness the subcarrier phase and amplitude information to design a unified framework for both moving and stationary human detection.

# IV. DEMAN DESIGN

This section presents the design of DeMan in a top-down manner, with emphasis on moving target detection. As a unified framework, DeMan simultaneously detects both moving and stationary targets in a generic processing flow without scenario-specific pre-training. Yet due to the unique challenges involved in stationary target detection without scenariospecific calibration, we defer the details on stationary target detection in Section V. Here a target refers to a person only and we use the two words interchangeably henceforth.

# A. Overview

The architecture of DeMan mainly consists of two components: moving target detection and stationary target detection. As shown in Figure 1, DeMan works as follows.

DeMan initializes by extracting CSI compatible with IEEE 802.11n standards on commodity NICs. The raw CSI measurements are passed through the Hampel identifier [29] to sift outlier observations [17]. Afterwards the CSIs are processed by a lightweight motion indicator to coarsely decide whether there is a moving person. If the answer is YES, the CSI measurements are further fed into the moving target detection module for finer-grained motion detection. Otherwise, the stationary target detection module is triggered to identify static human presence. DeMan reports a “detected” event if either module outputs affirmatives. Otherwise, no person is detected within the monitoring area.

To reliably detect moving humans, we exploit both amplitude and phase information conveyed in CSI measurements.

![](images/0f78f0b598c24a218a35a2fd69c6a7c238b0cfc0eb5155e299b854c072c0ccb2.jpg)  
(a)

![](images/04046a13c0dd4d328d68f31803fb6d9002de083e180eeea603dfc9f1d55446bf.jpg)

![](images/74e4a462cafa56709c4bbf5e117b337ebd99364db5e9eb4605f67a6bc211f138.jpg)  
(c)

![](images/1048444d63b33c75f0e6fcef71c0a079c3529f1f8ff06cb348f7aff67b2b9e26.jpg)  
(d)

![](images/8322be562383c1ce8d0b31baba4c84209cb79acb44def447ea2e0bf1d70d30d8.jpg)

![](images/30486358fa56482ab7ee6a2752de3750098f6888c7fe100f8f3e499b5eab4e11.jpg)  
(f)   
Figure 2: An illustration of impacts of human presence on signal propagation. (a) Static environment without human. (b) Moving human continuously induces significant changes on RF signals. (c) Breathing motion on the direct LOS path incurs different extent of shadowing. (d) Breathing motion shifts signal propagation between LOS and NLOS paths. (e) Breathing motion alters a reflection path that is generated by the human body. (f) Breathing motion modulates an existing reflection path.

We calculate the correlation matrices for the complex CSI measurements for each subcarrier, and extract the corresponding maximum eigenvalues for each correlation matrix. The maximum eigenvalues are then combined into a twodimensional feature to infer the presence of moving people.

To detect stationary persons without scenario-tailored calibration (profiling and comparing with signal characteristics collected in a “human-free” environment for each case), we harness the observation that humans, even when standing still or remaining seated, exhibit unique “motion” patterns like breathing. We first filter the CSI measurements to suppress signals irrelevant to breathing frequencies. The filtered CSI sequences are then fitted with a sinusoidal breathing model to estimate its dominant frequency. If the estimated frequency falls within the frequencies of normal human breaths, the presence of a person is detected. Otherwise, the stationary target detection module announces negative.

# B. Motion Interference Indicator

It is widely recognized that RF signals would fluctuate remarkably when objects move within the area of interests, and remain stable in case of no motion interference [1], [25]. The motion interference indicator exploits such motion-induced signal fluctuation to infer potential moving persons.

As shown in Figure 2b, when a person passes through a wireless link, his/her presence will continuously violates the original propagation paths (either LOS or reflection paths). In contrast, as shown by other figures in Figure 2, the propagation paths experience subtle changes in case of stationary persons or no person presence.

To validate these observations, we first conduct primary measurements in case of moving human, stationary human, and no human respectively, with a commercial wireless router as transceiver and a laptop as receiver. Since we intend to distinguish the case of mobile people from other cases, data collected in presence of static human and no human are integrated into one category marked as ”no movements” here. Figure 3 experimentally demonstrates the signal strength fluctuations of measurements with and without human movements, each for 5 seconds. As is shown, human movements can induce changes of up to 4dB in signal envelope, while changes caused by electronic noise, quantization errors and/or human breathing in stationary scenarios are mostly limited within only 1.5dB. In other words, CSI exhibits remarkably larger variations in case of moving humans than in case of static humans or no human, although CSI is also sensitive to breathing motion of static humans as we demonstrate later. Denote the mean-removed signal strength as X. Then X is expected to follow a zero-mean Gaussian $X \ \sim \ { \mathcal { N } } ( 0 , \sigma ^ { 2 } )$ . Fusing more data together, Figure 4 further consolidates the observation that human motion induces consistently larger variances $\sigma ^ { 2 }$ than static cases.

Motivated by these observations, we build a lightweight motion interference indicator based on the variance of signal envelope using a hypothesis testing:

$$
\left\{ \begin{array}{l l} S _ {m}: & \sigma^ {2} > \sigma_ {t h (m)} ^ {2} \\ S _ {s}: & \sigma^ {2} <   \sigma_ {t h (s)} ^ {2} \end{array} \right. \tag {2}
$$

case, respectively. σ2th(m) where $S _ { m }$ and $S _ { s }$ $\sigma _ { t h ( m ) } ^ { 2 }$ indicate the state of motion and static and $\sigma _ { t h ( s ) } ^ { 2 }$ denote the corresponding threshold to trigger moving target detection and stationary target detection. Recall Figure 4, there are a small portion of cases where the variances of motion and motionless cases critical zone always exists as are similar. Noticing this, we set σ2th(m) $\sigma _ { t h ( m ) } ^ { 2 } < \sigma _ { t h ( s ) } ^ { 2 }$ < σ2th(s) so that a $[ \sigma _ { t h ( m ) } ^ { 2 } , \sigma _ { t h ( s ) } ^ { 2 } ] ,$ 2 . To avoid false decision in the motion indication stage, those confused cases fallen in the critical zone are doubly checked by both subsequent modules. The thresholds can be determined by some preliminary measurements. Different from previous works that rely on scenario-tailored calibration, however, we do not need to calibrate for each different case because the thresholds can gracefully apply to various environments. Moreover, we design a critical zone of the thresholds to tolerate a range of potentially different values in diverse scenarios.

The design of the motion indicator is lightweight since the calculation of envelope is fast and effective. The hypothesis testing provides a primary indication of motion or motionless, but not the ultimate declaration with high confidence. Actually, while the usage of CSI variations is sufficient for motion indication, it is too optimistic to be an effective metric for target detection since it is too sensitive to environment dynamics. A more elaborative metric is proposed for moving human detection in the following section.

# C. Moving Target Detection

If a group of measurements is labelled with state $S _ { m }$ in the previous stage, it is then passed through a more elaborate and reliable examination, i.e., moving target detection.

Numerous research has explored to detect human movements non-invasively for localization and tracking [1], [3], counting [2], [26] or activity recognition [17]. However, most utilize only the envelope features of received signals, either in the form of value of MAC layer RSSI [1], [2] or amplitude of PHY layer CSI [17], [26], yet ignore the counterpart phase information. In this work, we demonstrate that phase information is similarly or even more sensitive to environmental changes and thus provides more accurate detection of moving humans. Hence we incorporate both amplitude and phase features to unleash the full potential of CSI for more accurate and reliable detection.

![](images/f0812c408a53a22fe301ca5cb3516b2bff156bc67631e7d683cf3d5e1c5d2dda.jpg)



Figure 3: Human movements induce significantly larger changes in signal envelope.

![](images/c42197cdbacb35756d77e7a4b60685bc206fb4e2ef880efcd386ccad1ae9a2bd.jpg)



Figure 4: Envelope variances of human movements are remarkably larger than those of no movements.

![](images/b973631b07e59dff5a4459dbb9f44bd534997ba55da7377accbcc5163241f8e5.jpg)



Figure 5: Normalized maximum eigenvalues of amplitude and phase correlation matrices

Due to the lack of time and frequency synchronization, however, raw phase information extracted from commodity WiFi devices tends to be extremely random [24], [26]. Denote $\hat { \phi } _ { k } \ = \ \phi _ { k } + 2 \pi w _ { k } \Delta t + 2 \pi w _ { k } \Delta w$ as the measured phase at subcarrier k with carrier frequency $w _ { k }$ , where $\phi _ { k }$ is the genuine phase. $2 \pi w _ { k } \Delta t$ and $2 \pi w _ { k } \Delta _ { }$ w are the unknown phase shifts caused by the clock offset $\Delta t$ and frequency difference $\Delta w$ .

To mitigate the random noise in raw phase measurements, we employ a linear transformation as recommended in [24]. We revise the raw phase information as $\phi _ { k } ^ { \prime } = \hat { \phi } _ { k } - \alpha w _ { k } - \beta$ where α and $\beta$ are intuitively the slope and offset of phase change over all the subcarriers, respectively. Then the sanitized phase measurements are re-assembled with the corresponding amplitudes into complex CSIs for mobile target detection.

Consider N CSIs within a time window T , where each CSI on subcarrier k sampled at time $t _ { i } , i \in [ 1 , N ]$ is a complex number as in Equation 1:

$$
H _ {k} (i) = | | H _ {k} (i) | | e ^ {j \angle H _ {k} (i)}, \tag {3}
$$

where $\angle H _ { k } ( i )$ denotes the revised phase $\phi _ { k } ^ { \prime } ( i )$ . Then CSI samples at time $t _ { i }$ over all the n subcarriers form a complex vector

$$
H (i) = \left[ H _ {1} (i), H _ {2} (i), \dots , H _ {n} (i) \right]. \tag {4}
$$

Since human motions induce temporal fluctuations of the received signals, we investigate to depict such temporal disturbance via correlations between successive measurements. Concretely, for the N CSIs $\pmb { H } = [ H ( i ) ] _ { N \times n } .$ we calculate the respective correlation matrices A and C for amplitudes and phases of the CSI measurements as follows:

$$
\boldsymbol {A} = [ a (i, j) ] _ {N \times N}, \boldsymbol {C} = [ c (i, j) ] _ {N \times N}, \tag {5}
$$

where each element denotes the correlation coefficient between H(i) and $H ( j )$

$$
a (i, j) = \operatorname{corr} \left(\left| \left| H (i) \right| \right|, \left| \left| H (j) \right| \right|\right), \tag {6}
$$

$$
c (i, j) = \operatorname{corr} (\angle H (i), \angle H (j)). \tag {7}
$$

Afterwards, we derive the eigenvectors of matrices A and $C$ and exert the normalized maximum eigenvalues (denoted as $\lambda _ { A }$ and $\lambda _ { C }$ for A and C respectively) for moving human detection. Generally, in case of no human presence or merely stationary human, successive measurements would exhibit high correlation factor, resulting in large eigenvalues (close to 1). In contrast, the eigenvalues tend to be small if there are moving humans during the measurements. Figure 5 depicts an illustration of 500 groups of measurements for each case, of which each group involves 500 packets. As seen, both $\lambda _ { A }$ and $\lambda _ { C }$ are close to 1 in case of stationary human presence or no human presence, while decrease dramatically in case of human movements. Consequently, one can easily search for a cutting edge (threshold) to identify measurements accompanied with human movements. In addition, the threshold is scenarioindependent thanks to the use of eigenvalue-based features, which are independent of absolute signal powers that vary over different scenarios and different time. This threshold, together with the ones for motion interference in Equation 2, are the only components of DeMan that need slight prior efforts to calibrate, except for which DeMan requires no calibration.

The use of eigenvalues of a correlation matrix is independent of absolute signal powers. Therefore once the prerequisite thresholds are determined, they are applicable to various scenarios and do not need to be re-calibrated. This approach is inspired by [25] that employs maximum and the second maximum eigenvalues of amplitude, and we advance it by harnessing both amplitude and phase features of CSI.

# V. STATIONARY TARGET DETECTION

In contrast to motion detection, conventional solutions to device-free detection for stationary humans often require a prior profile measured with no human presence within the monitored area [7]. This is because the presence of stationary human normally incurs static signal strength changes by shadowing the LOS path or creating a new reflection path [8], but only slight fluctuation within a temporal window. Hence prior awareness of the signal profiles without human presence is indispensable as reference for individual cases. To eliminate the overhead of such pre-calibration and achieve a unified detection framework for both moving and stationary targets, the key observation is that stationary people continuously breathe, which can be detected from wireless signals if elaborate mechanisms are designed for subtle chest motions.

![](images/9a374531a20a0904a16dfe4f4e2b18efce5c6ca260e4c17d5a9b1b7223e0240d.jpg)



(a) Raw CSI measurements with human breathing for 1 minute

![](images/d8120f0387483f3c908b2e940a15db10da062d0585cb22379345e5793bdad8d9.jpg)



(b) Periodic CSI patterns at subcarrier level (Subcarrier #10)

![](images/a2e139dfc5a52fbc7a0e7b8b609acd6b7684c9e91d759e14168523b9fd760029.jpg)



(c) Conspicuous repetitive patterns over all subcarriers of filtered CSIs   
Figure 6: Rhythmic motions of human breathing induce wave-like patterns on the received signals. Various colors in (a) and (c) indicate different level of signal strengths, decreasing from red to blue.

# A. Periodic Alterations from Breathing

We begin with some intuitive observation and formal justification on why human breathing is measurable via CSI.

Analyzing human breathing. Traditional non-invasive human detection schemes mostly detect whole-body human motions [7], and assume that the signals remain nearly constant in static environments. We demonstrate that, however, the wireless signals are sensitive enough to be distracted by breathing people who stands still on, close to, or distant to the LOS path.

In typical indoor environments, wireless signals can propagate via reflection, diffraction, scattering via human bodies and other environmental obstacles. Therefore, signals can be potentially modulated by periodic chest motions of breathing if it interacts with the person, even when he stands still at the same place.

As illustrated in Figure 2, when a person is present on the LOS path, the movements of chest cavity would either dictates the signal propagation by different extent of shadowing (Figure 2c), or continuously shifts the propagation path between LOS and NLOS (Figure 2d). Several works [20], [21] have observed similar phenomenon on RSSI as Figure 2d and deploy dedicatedly placed TX and RX for breath monitoring. Nevertheless, they are effective only when the conditions in Figure 2d are strictly satisfied.

In presence of a breathing person off the LOS path, the received signals can also be continuously disturbed by reflections from the moving chest. As shown in Figure 2e, the presence of a human body would create a new reflection path while the person’s breathing can repeatedly change that path. Also, a breathing person could refashion an already existing reflection path, as illustrated in Figure 2f. Such changes in multipath propagations, however, are scarcely possible to be captured by the coarse-grained RSSI, yet observable through CSI, which has been demonstrated to be capable of characterizing multipath effects at OFDM subcarrier level [10].

Measuring human breathing. Although human breathing does change signal propagation, are the alterations discernible and measurable using commodity WiFi infrastructure? We give

![](images/4dd9a0275f5ca089c2964fc0ac9252a6ee0fe44dcf4d6f13665229c2f29111e0.jpg)



Figure 7: Power spectral density of the filtered signal

a positive answer to this critical question after conducting real experimental measurements using commodity WiFi devices.

As a preliminary verification, we collect a group of measurements by letting one volunteer stand still and breathe naturally beside a commercial laptop that serves as the receiver. The measurements last for 2 minutes and the original CSI amplitudes are plotted in Figure 6a. The amplitude patterns are different from those of completely human-free static environments. By employing a bandpass filter (details will be discussed in the following section) on the original CSIs, we can see more conspicuous periodically oscillatory patterns, as shown in Figure 6c. Similar periodicities arise over almost all subcarriers, since breathing produce consistent interference on all subcarriers. Thus viewing from individual subcarrier, one can observe obvious wave-like patterns arising in the filtered signals (Figure 6b).

To assuredly examine the existence of a signal component that is caused by human breathing, we dive deeper into the measured signals to see whether there is a signal that has the same frequency as human breathing. Typically, an adult breathes at about 14 breaths per minute (bpm) at rest while a newborn at 36 bpm [30], [31]. Thus the general breathing frequency of a static human is limited in 0.167Hz to 0.667Hz, which corresponds to a breathing rate of 10 and 40 bpm, respectively. Hence, we turn to investigating a potential signal from the received signals with a similar frequency.

To this end, we analyze the power spectral density (PSD) of the filtered signal in the frequency domain. As shown in Figure 7, we can clearly see a significant component that peaks at the frequency of 0.233Hz (about 14 bpm), which corresponds to an adult’s typical breathing frequency (the true breathing rate of this measurement is exactly 14 bpm). As a result, one can conclude the extracted signals as induced by human breathing motion.

![](images/a7415fdddf20c24b73e983307330f11f26b7f1c39b32e3780bbf83c517441e63.jpg)



(a) Human presence with f = 12bpm

![](images/6292fb6bd8cb63da4785b11aa8d062b823f8d0686a32d213ed720bc1c84406da.jpg)



(b) Human presence with f = 13bpm

![](images/17d2dfd5b82097076cc0a5c99322a833c5e3cd5e457d89d5ea8d48e5033c5fb0.jpg)



(c) Human absence (no breathing signals)   
Figure 8: Sinusoidal fitting on CFR amplitude at Subcarrier #10. (a) User breaths evenly over the measuring period. (b) User breaths with different scale (yet similar frequency) over the measuring period. (c) Noise signals without user breaths.

![](images/5f029e968aec45bf7948cec6a2acc46508b8fcef1e0650a913b63d84052f36b6.jpg)  
(a) Breathing signals over all subcarriers

![](images/915fe6b183c8e2ec4219e49e8ac9f28b87a3164b0ccf758490833c08ee22a803.jpg)



(b) Breathing signals at subcarrier #5

![](images/d2027bacae644a94a12a26c497ffd729762a4a19f58be828158f14570168de01.jpg)



(c) Breathing signals at subcarrier #24   
Figure 9: Human breathing introduces diverse signal responses over different frequency subcarriers. (a) All subcarriers but a small portion (subcarrier #19∼#24) depicts obvious breathing pattern, although the amplitude changes may be in the opposite direction (subcarrier #1∼#19 vs. subcarrier #25∼#30). (b) Estimated signals are remarkably close to the breathing signals when using subcarrier #10. (c) Incorrect frequency with meaningless amplitude may be resulted in if using subcarrier #24.

# B. Breathing Detection

To estimate breathing signals, we first pass the original measurements through a filter to remove noises while keep the interested modes. Then we justify a sinusoidal model of the breathing signals and detect human breathing using a parameter estimation technique.

1) Signal Filter: Before estimating breathing signal from the mixed received signals, we first filter out the irrelevant components, such as electronic noise and other motions. We achieve this by applying a bandpass filter.

Since human breathing rates roughly fall into the range of 10bpm to 40bpm, the filter should retain signals within frequencies of 0.167Hz and 0.667Hz, while significantly attenuate the others. To be conservative, we set the minimum frequency as $f _ { m i n } = 0 .$ 15Hz and the maximum $f _ { m a x } = 0 . 7 0 \mathrm { H z } .$ In addition, for a sequence of signals $\{ H _ { k } ( i ) \} _ { i = 1 } ^ { N }$ , the mean values $\bar { H } _ { k }$ (i.e., the DC component) may bury the breathing component that usually only has low amplitudes of 1dB or 2dB. The bandpass filter also removes the DC component in the original signals, i.e., $\bar { H } _ { k } ~ = ~ 0$ . The filtered signals then potentially indicate the presence of human breathing.

2) Sinusoidal Model: Recall Figure 6b, breath-induced signal presents a sinusoid-like pattern. Previous works that monitor breaths with UWB or sensor networks also suppose that breathing attaches an additional sinusoidal component to the received signal [20], [21]. Intuitively, this is because periodic chest motion produces sinusoidal time delays of the signals reflected by chest [20]. For the sake of simplicity, we still use $H _ { k } ( i )$ to denote the amplitude of CSI on subcarrier k measured at time $t _ { i }$ in this section. In a static environment, the amplitude of received signals can be expressed as

$$
H _ {k} (i) = \bar {H} _ {k} + \epsilon_ {k} (i), \tag {8}
$$

where $\bar { H } _ { k }$ is the mean amplitude of the received signal at subcarrier k and $\epsilon _ { k } ( i )$ is an additive noise. When a breathing person presents, an additional sinusoidal term $G _ { k } ( i )$ is added:

$$
H _ {k} (i) = \bar {H} _ {k} + G _ {k} (i) + \epsilon_ {k} (i), \tag {9}
$$

$$
G _ {k} (i) = A _ {k} \cos (2 \pi f t _ {i} + \phi_ {k}), \tag {10}
$$

where $A _ { k } , \phi _ { k }$ , and $f$ are the amplitude, phase, and frequency of the breathing induced periodic component in respective order and $t _ { i }$ is the time when the signal is sampled. For ease of presentation, this term of $G _ { k } ( i )$ is also referred to breathinginduced additive signal, or more concisely, breathing signal. Due to interference of human breathing, the sinusoidal term $G _ { k } ( i )$ is generally larger than the noise term. In some extreme cases with considerable environment noise, the breathing signal, however, could be drowned and thus potentially more difficult to be identified. In this paper, we basically consider relatively stable environments, where the $G _ { k } ( i )$ is larger than or at least comparable to the noise term.

Intuitively, if the received signal is mean removed, it is possible to model the residual component with a sinusoidal model. Further, human breathing can be detected by estimating specific parameters $( \mathrm { i } . \mathrm { e } . , A _ { k } , \phi _ { k }$ , and f ) of the model. In other words, given a deterministic model with unknown parameters, the problem of breathing detection is turned into a parameter estimation problem, which can then be solved by optimization techniques.

3) Parameter Estimation: Specifically, the parameter estimation tasks are two-fold: 1) detect whether there exists a signal component that holds the interested frequency, and 2) if yes, what is the specific frequency (and other parameters like amplitude and period counts).

Given the filtered signals $\tilde { H } _ { k } ( i )$ sampled at time $T _ { i } , 1 \le i \le$ $n ,$ of which the mean amplitude is supposed to be removed, we aim to find a sinusoidal signal $\hat { G } _ { k } ( i ) = \hat { A } _ { k } \cos ( 2 \pi \hat { f } t _ { i } + \hat { \phi } _ { k } )$ that minimizes the residual sum of squares (RSS)

$$
R S S = \sum_ {i = 1} ^ {N} | | \hat {G} _ {k} (i) - \tilde {H} _ {k} (i) | | ^ {2} \tag {11}
$$

We tackle the problem using sinusoidal parameter estimation algorithms that deal with a single sinusoidal signal of unknown frequency, phase, and amplitude. Particularly, we use the Nelder-Mead method [32], which is a common non-linear optimization technique for multidimensional unconstrained minimization, i.e., minimizing an objective function with multiple variables. Nelder-Mead algorithm is a simplex-based direct search that is effective and computationally compact and has been widely employed in parameter estimation and similar statistical problems.

Figure 8 illustrates the preliminary effects of the sinusoidal parameter estimation. As shown in Figure 8a, when the person breathes evenly, a sinusoidal model can fit the breathinginduced signals with precise frequency and amplitude. Figure 8b portrays the case of a person breathing with inconsistent depths over time, which causes breathing signals with diverse amplitudes. As is shown, the sinusoidal parameter estimation method still works excellently in such cases. Specifically, the frequency estimation remains accurate although the RSS of amplitude appears larger. We also test the model estimation on non-breathing signals, i.e., signals measured when there is no human presence, and depict the results in Figure 8c. Compared with previous two figures, the signals without breathing motion interference appear to be more random, lacking periodical patterns. When applying the parameter estimation algorithm, besides that the estimated frequency is beyond the interested band of $[ f _ { m i n } , f _ { m a x } ]$ , the deduced signals make little sense since the amplitudes shrink to insignificance. Consequently, the estimation on non-breathing signals yields meaningless results, which are remarkably discriminative from those produced from breathing signals.

In a nutshell, we conclude that a sinusoidal model can fit the breathing signals measured by CSI (in the form of individual subcarrier) and the parameters can be precisely estimated by the Nelder-Mead method. Thus one can successfully distinguish the presence and absence of a breathing person. In the following, we will extend to the full frequency band, i.e., all available OFDM subcarriers, to make the detection more accurate and robust.

![](images/86f5ec69e13deb0e29b018e510564103278212ff9e51f38dc1f7a508bb389924.jpg)



Figure 10: Frequency estimation on a majority of subcarriers presents accurate results while profaned estimations may appear on a small portion of subcarriers. Nevertheless, these biased estimations tend to be outliers (circled parts) and could be sifted out by LMS estimator.

# C. Embracing Frequency Diversity

Modern modulations such as OFDM transmit information via multiple orthogonal subcarriers simultaneously to combat frequency-selective fading [33], giving rise to frequency diversity for adaptive wireless communications [9], [33] and finegrained indoor localization [24]. In this work, we also harness frequency diversity for more robust breathing parameter estimation.

Ideally, human breathing should attach an additive signal with identical frequency (i.e., the breathing frequency) on each subcarrier, which is expected to be irrelevant to the signal propagations. In practice, however, identical breathing motion causes different extents of signal perturbation on different subcarriers due to frequency-selective fading. Specifically, the same motion does not necessarily consistently increase or decrease the received signal power due to constructive and destructive phaser superposition [8]. Hence breathing signals on some subcarriers would be more conspicuous and thus easier to be captured while on others might be less obvious. Thus, utilizing breathing interferences across multiple subcarriers would improve both detection precision and robustness.

Taking Figure 9 as an example, the rationale and necessity lie in three folds:

1) Breathing signals are well captured on most subcarriers, yet with different amplitude responses. Fusing parameters on individual subcarriers would prospectively produce more accurate estimation.   
2) Breathing motion may have no significant effects on a specific subcarrier, thus leading to miss detection using that subcarrier only. Such miss detection can be avoided by incorporating results across multiple subcarriers.   
3) In cases of human absence, there will be consistently no significant periodic signals appearing on any subcarrier.

To take advantages of multiple subcarriers, we first repeat the above sinusoidal parameter estimation for each individual subcarrier. Then we obtain a group of breathing frequency estimations $\hat { f } _ { k } , 1 \le k \le n$ , with the corresponding amplitude estimations $\hat { A } _ { k }$ . Ideally, all $\hat { f } _ { k }$ should be the same since human breathing frequency is principally nondiscriminatory to all subcarriers. However, as discussed above, due to frequencyselective fading, amplitude attenuation on each subcarrier differs from each other, leading to inconsistent parameter estimation when fitting with a sinusoidal model. Hence we need to obtain reliable parameters from these primary estimations.

Diving into the parameter estimation on multiple subcarriers, the majority of the frequency estimations are quite accurate and stable, and incorrect estimations occasionally appear, as demonstrated by Figure 10. Motivated by this observation, we propose to sift out the biased incorrect frequency parameters by conducting a one-dimension least median of squares (LMS) outlier detection [34]. Mathematically, let $\tilde { f }$ be the LMS estimate of $\hat { \pmb f } = [ \hat { f } _ { k } , k = 1 , \cdots , n ]$ and $r _ { k } = \hat { f } _ { k } - \tilde { f }$ be the residuals, we determine whether $\hat { f } _ { k }$ is an outlier or not following a typical LMS regression as

$$
I (\hat {f} _ {k}) = \left\{ \begin{array}{l l} 1 & \text { if } | r _ {k} / \sigma^ {*} | <   = 2. 5 \\ 0 & \text { otherwise } \end{array} \right. \tag {12}
$$

where

$$
\sigma^ {*} = \sqrt {\frac {\sum_ {k = 1} ^ {n} q _ {k} r _ {k} ^ {2}}{\sum_ {k = 1} ^ {n} q _ {k}}}
$$

$$
q _ {k} = \left\{ \begin{array}{l l} 1 & \text { if } | r _ {k} / s ^ {0} | <   = 2. 5 \\ 0 & \text { otherwise } \end{array} \right.
$$

$$
{s ^ {0}} = {1. 4 8 2 6 * (1 + \frac {5}{n}) \sqrt {\mathrm{med} _ {k} r _ {k} ^ {2}}.}
$$

The involved constant values are widely recognized factors in the literature [34].

After diagnosing the biased and incorrect frequency estimations, we simply sift them out and then average the remained ones as the ultimate estimation of breathing frequency:

$$
\hat {f} = \frac {1}{\sum_ {k = 1} ^ {n} I (\hat {f} _ {k})} \sum_ {k = 1} ^ {n} \hat {f} _ {k} I (\hat {f} _ {k}) \tag {13}
$$

where $I ( \hat { f } _ { k } )$ is the outlier indicator we derived above. If $\hat { f }$ falls in a given frequency band of interests, $[ f _ { m i n } , f _ { m a x } ]$ , then a stationary human is detected; otherwise not.

Generally, LMS regression yields more reliable diagnosis with more sample data. In practice, noticing that nowadays WiFi devices are often equipped with multiple antennas, we incorporate multiple antennas to improve the reliability of frequency estimation. Specifically, we extend the sinusoidal parameter estimation to the CSI measurements on multiple antennas, each of which results in n frequency estimations. Fusing all these estimations for the LMS regression, more accurate and reliable results can be gained than using a single antenna. Having said that, please note the proposed method benefits from, but does not rely on, multiple antennas.

# VI. EXPERIMENTS AND EVALUATION

In this section, we first interpret the experiment methodology, followed by detailed performance evaluation.

# A. Implementation

1) Experimental Environments: We prototype DeMan with commodity WiFi devices and evaluate its performance in a typical office building including a classroom and a laboratory (Figure 11). We employ a commercial TP-LINK TL-WR741N wireless router as the transmitter operating in IEEE 802.11n AP mode at 2.4GHz. A LENOVO desktop running Ubuntu 10.04 is used as a receiver, which is equipped with off-theshelf Intel 5300 NIC and a modified firmware [35]. During the measurements, the receiver pings packets from the router and records the CSI from each packet.

![](images/c1f1e7b8145faef0552d2f4bfb83fe03580f750fd9d538277dc82a6d2695137c.jpg)



Figure 11: Experimental areas

2) Experimental Methodology: We collect data from three categories: 1) Moving data: There are one or more humans walking around in the monitoring area. 2) Breathing data: There is one human standing or sitting in the area of interests, breathing naturally. 3) Human-free data: There is no human presence and thus the environment is relatively static.

To collect moving data, we let a volunteer walk randomly with a nature speed of around 1m/s along a Hilbert-like trajectory [36], which holds a space-filling property and thus traverses the entire monitoring area. We adopt such trajectory in purpose of demonstrating the sensitivity over the covered space. Yet note that we did not necessarily follow a strict Hilbert trajectory in the experiments. Instead, we let the volunteer take a Hilbert-like but less complex path to traverse the space. CSI data are continuously logged during the walking. For breathing data, a volunteer stands or sits at a uniformed grid of locations over the monitoring area, either on or off the LOS path between the transmitter and receiver. For each grid location, we collect a group of breathing data for around 2 minutes. For each link, the monitoring area is defined as a rectangle area centered along the TX-RX path with a width of 2 meter and a length of the TX-RX distance. The volunteer keeps natural breathing without other motions during the measurement. The ground truth respirations are also manually counted and recorded. For fair comparison, we collect a similar amount of data for each category.

As shown in Figure 11, we consider 5 different scenarios with different link conditions. Particularly, we consider both LOS and NLOS propagation, diverse TX-RX distances ranging from about 3 meters to 6 meters. For each scenario, we conduct all the 3 types of measurements, each for three times. The experiments are conducted in different days in a week, with about 8 hours of data or 540k CSI records in total.

For moving target detection, we first employ the wellknown Support Vector Machine (SVM) classification to obtain a threshold line, based on a portion of measurements. The threshold line is one-time learned and, according to our experiments, fits various scenarios. Yet different from previous work that conduct scenario-tailored calibration, we do not need to calibrate the parameters for each different scenario over different time.

![](images/a818a6bf4ee86a33820b5f695f637ba06e093fbe5a88391f242ab345e125fb26.jpg)



Figure 12: Detection accuracy using different features.

![](images/3fd563c95eedcfa2873ca6efca91d3542e748d3e98b9c4f68d03a12a0b042e12.jpg)



Figure 13: Impacts of packet quantity on detection accuracy of moving target.

![](images/3f47132bb5618e09d321f4de8bd9af45e4b14695832528e04cadecb7181f45e4.jpg)



Figure 14: Impacts of sample rate on detection accuracy of moving target.

![](images/80aa676b4235a4c8febb8d64b5a47dd83d4ef7566ad80b119f27a079042b509f.jpg)



Figure 15: Stationary detection accuracy in diverse scenarios

![](images/5d8baa5e878d3f308eb1cd4ba4b7a0a21e90f67ed36b429aaed9f35bfe51503d.jpg)



Figure 16: Impacts of packet quantity on detection accuracy of static target.

![](images/7c08ad05255d5b7d89cecfd8aa80d7c769088d0adffb757ca65271061b81948b.jpg)



Figure 17: Impacts of sample rate on stationary target detection.

3) Evaluation Metrics: We mainly use the following metrics to evaluate the performance of DeMan.

• True Positive Rate (TP): the fraction of cases where a human (either moving or breathing) is correctly detected.   
• True Negative Rate (TN): the ratio of cases where no human presence is correctly identified.

For each metric, we separately examine the performance of moving human detection and stationary human detection, followed with the overall evaluation. We also inspect the impacts of various factors, including packet quantity, link distance, LOS and NLOS propagation, etc.

# B. Performance

1) Performance of Detecting Moving Human: We first examine and compare the performance of moving human detection using moving data and human-free data. Figure 12 shows the performance of moving detection, especially the gain from exploitation of full CSI information, i.e., amplitude and phase. As is shown, DeMan achieves high TP and TN rates of 94.07% and 98.55%, both outperforming the scheme with merely CSI amplitude (by about 2% and 5% respectively). To further demonstrate the benefits of using eigenvalues of correlation matrices, we compare DeMan with a scheme that uses variances of amplitude and phase. As shown in Figure 12, the variance-based scheme attains poor performance with the TP and TN rates of only 81.48% and 78.04% respectively. We suspect that this is because variances, unlike eigenvalues, are dependent on absolute signal powers and thus vary over different scenarios even when the human motions are similar, making a pre-calibrated threshold line inapplicable for extended cases.

We inspect the impacts of packet quantity by applying a sliding window varying from 50 packets to 1000 packets. The results are illustrated in Figure 13, which demonstrates that TP rate improves significantly with more packets (from 87.54% with 50 packets to around 95% with more than 500 packets) while TN rate is almost unaffected at around 98%. The result is reasonable because in case of human-free, the channel measurement mostly keeps stable and thus a short period of samples is sufficient to capture the characteristics. In contrast, insufficient samples fail to characterize the temporal variations of human motions since the influences from human movements do not uniformly distribute over time. Nevertheless, we observe that satisfied accuracy of both TP and TN rates higher than 90% can be consistently achieved when using more than 200 packets.

Figure 14 shows the moving human detection performance under different sample rates. The results are drawn from data measured within the same period of time window. As can be seen, sample rate almost does not affect detection accuracy. This indicates that human movements continuously affects the channel, and either frequent or sparse sampling can capture the variations well.

2) Performance of Detecting Static Human: Breathing data together with human-free data are used for evaluation of stationary human detection. Figure 15 demonstrates that De-Man achieves good detection performance in various scenarios as depicted in Figure 11, with TP and TN rates consistently higher than 90%. Integrating results from different cases, DeMan provides a TP detection rate of 94.64% with a TN rate of 94.49%. Even in case 4 as shown in Figure 11 where the TX-RX distance is more than 6 meters, the TP and TN rates still keep at 92% and 93%, respectively. Since the data are measured when the person stands or sits at different locations with diverse TX-RX distances, we conclude that

![](images/7db7ac61d3bd9b99d461d37ba88cc8917e697f7e247e7afed4dc79233518d047.jpg)



Figure 18: Detection performance in LOS and NLOS propagation

![](images/59e8151ec48b533ba7fde967da05a04e40b280aeaeadf775d271600d615c224e.jpg)



Figure 19: Results of motion indicator. The label “confused” indicates the measurements that are simultaneously inferred as “motion” and “static”.   
![](images/fe4b1e73376f3fa4b2720736e3cab42c11f8c38edda3950ae4f74d1e66d2cd2d.jpg)



Figure 20: The upper figure displays accuracy of breathing rate estimation for users on the LOS paths and the lower for users on the reflected paths.

DeMan extends the breathing detection ability to cases of various poses, presenting locations and longer link lengths, compared with existing approaches [21], [22].

Figure 16 illustrates the performance of stationary target detection with different amount of packets, given a fixed sample rate of 50Hz. As seen, DeMan achieves high detection accuracy, with TP and TN rates both higher than 95% with a window of 1500 packets. The performance slightly degrades with more packets, since human breathing might vary and some motions could be involved during a long time window. Detection performance also drops with too fewer packets. Since human breathing motion is fairly slow, e.g., breathing once within a period of a few seconds, observations within a very short period make no sense of the breathing motion.

The performance under different sampling rate is portrayed in Figure 17. Similar to moving human detection, sampling rate has little impact on detection accuracy. Though a bit counter-intuitive, we suspect this is because measurements with sparse sampling still depict the rhythmic patterns of breathing signals and thus the parameter estimation still works well. In other words, as long as the signal’s periodicity is fully reserved, regardless of the specific sample rate, the performance of breathing detection can be maintained.

We are particularly interested in the performance of detection with stationary people presenting off the LOS path, i.e., on the reflected paths. Figure 18 depicts the detection rate of people on and off the direct LOS path, with various packet numbers. As seen, DeMan achieves great performance in both conditions, with best TP and TN rates of above 95%. Such encouraging results demonstrate the feasibility of DeMan in various environments, without requiring users to stand directly on or extremely close to the LOS path as demanded by previous works [21], [22].

3) Putting it All Together: Finally, we examine the overall performance of DeMan in practical system with all three categories of experimental data, integrating both moving human detection and stationary human detection with the motion indicator process. We use the packet amount of 1500 for evaluation. We implement a baseline approach for comparative study: a modified DeMan without the stationary target detection module, which can thus be treated as an improved version of previous work [25] with phase information extension.

We first present the results of primary motion indicator based on the variances of CSI as in Figure 19. As seen, most

Table I: Overall performance 

<table><tr><td rowspan="2"></td><td colspan="2">DeMan</td><td colspan="2">Baseline</td></tr><tr><td>Human presence</td><td>Human absence</td><td>Human presence</td><td>Human absence</td></tr><tr><td>Moving</td><td>94.82%</td><td>5.18%</td><td>95.39%</td><td>4.61%</td></tr><tr><td>Breathing</td><td>93.33%</td><td>6.67%</td><td>35.71%</td><td>64.29%</td></tr><tr><td>Human-free</td><td>3.75%</td><td>96.25%</td><td>4.57%</td><td>95.43%</td></tr></table>

of human-free cases are accurately categorized as static and only a very small portion of 1.39% is labelled as in motion. In case of breathing human or moving human, however, a significant portion of around 35% will be falsely classified in the motion indicator stage. Nevertheless, most of the falsely labelled cases (25.32% out of 34.27% and 31.48% out of 34.81% for breathing case and moving case respectively) will be doubly checked by both moving and stationary detection.

Table I illustrates the overall detection results of DeMan. Both moving people and stationary people can be accurately detected, with respective detection rate of 94.82% and 93.33%. Integrating the results together, DeMan achieves TP and TN rates of 94.08% and 96.25%, respectively. As comparison, the TP detection rate degrades to 65.55% for the baseline approach, which does not differentiate moving and stationary people and thus mixes up a significant portion (64.29%) of stationary cases with human-free scenarios. Although the baseline approach attains comparable TN rate, the corresponding false negative rate increases to a considerable level of 34.45%. These results demonstrate that DeMan improves detection accuracy and extends detection ability by exposing human breathing as indicators for stationary humans. Note that the detection rate of human-free scenarios is less than 99.86% as in Figure 19 because that a small portion of human-free cases classified as static could be falsely alarmed in the stationary target detection module, which, however, is negligible.

# VII. DISCUSSIONS AND FUTURE WORKS

# A. Monitoring Breathing Rate

Given that DeMan accurately detects stationary people by sensing the breathing motion, we are also interested of how accurately DeMan could estimate the breathing rate. As shown in Figure 20, we test 35 groups of 1 minute measurements and observe that DeMan yields breathing rate of errors less than 1 bpm for most testing cases. Concretely, the average estimation error is 0.86 bpm for LOS scenarios and 0.97 bpm for NLOS scenarios. These results demonstrate that DeMan achieves comparable accuracy of breathing rate estimation with previous contactless approaches and works effectively even when the person presents on the reflected paths. In this sense, breathing rate monitoring is a side product of DeMan, which even outperforms previous dedicated works in case of longer link lengths and diverse user poses and presence locations [20]–[22]. Nevertheless, currently we do not consider people diversity in our experiments, and it is of our interests to study how a person’s age, gender, size, etc. affect breathing detection and estimation.

# B. Expanding Detection Coverage via Space Diversity

Emerging generations of WiFi infrastructure are incorporating an increasing number of antennas to boost capacity leveraging space diversity [28]. Multiple antennas can be controlled digitally to adjust their beams towards a certain direction using beamforming techniques [37]. Such capability of narrowly focusing transmission power on an intended direction can avoid the adverse impact of irrelevant multipath, and offer higher sensitivity on the blockage and reflection induced by the target micro motions (breathing in our case) even from a NLOS path [5]. In addition, since signals propagating through a NLOS path often arrive at the receiver with a different angle-of-arrival, it is possible to intentionally magnify the received signals from directions of the NLOS paths to allow wider detection range, and researchers have demonstrated the feasibility to distinguish arriving angles from multiple paths using commodity software radios [38] and standard WiFi infrastructure [39].

# C. Multiple Target Detection

Current DeMan excels in detecting stationary humans in case of individual person presence. In the future, we intend to expand DeMan to multiple people scenarios. When there are multiple stationary persons in the monitoring area, each person is expected to contribute an additive signal with individual breathing frequency. Hence the resulted breathing signal will be a superposition of multiple sinusoidal signals. To extract the breathing frequencies, we may then apply either a multiple sinusoidal parameter estimation algorithm or successive interference cancellation techniques [40]. Furthermore, we envision the impacts of chest motion on the phase information of CSI as a potential proxy for more complicated cases where multiple persons could hold nearly identical breathing rates.

# D. Extending to Through-wall Detection

The applicability of DeMan in case of human presence on the reflected paths encourages us to extend the detection ability to NLOS scenarios, i.e., the LOS propagation is prohibited between the TX and RX. Specifically, we are interested in exploring the possibility of through-wall detection of human presence, yet without involving a dense network or prior link calibration as [1], [7]. The potentiality of detecting people in case of NLOS propagation is critical and helpful for various applications like disaster relief where survivors are often trapped behind the wall or buried underground.

# VIII. CONCLUSIONS

In this work, we present the design and implementation of DeMan, a unified framework for simultaneous detection of moving and stationary people with COTS WiFi devices. We exploit both amplitude and phase information of CSI for moving target detection. To detect stationary people, we leverage the breathing-induced periodic patterns on wireless signals using a sinusoidal model. To improve detection accuracy and robustness, we further harness the frequency diversity across multiple OFDM subcarriers. We prototype DeMan in typical buildings. Experimental results demonstrate that DeMan achieves great performance for both moving and stationary people detection in various environments. Requiring no prerequisite scenario-tailored link calibration and being effective for persons on and off the LOS paths, DeMan sheds lights on practical non-invasive detection techniques.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program 61190110, NSFC under grant 61171067,61472098, 61361166009, and the NSFC Distinguished Young Scholars Program under Grant 61125202. The research of X. Liu and J. Cao is supported in part under NSFC/RGC Joint Research Schemes 3-ZG1L and the NSFC under Grant No. 61332004.

# REFERENCES

[1] J. Wilson and N. Patwari, “See-Through Walls: Motion Tracking Using Variance-Based Radio Tomography Networks,” IEEE Transactions on Mobile Computing, vol. 10, no. 5, pp. 612–621, 2011.   
[2] C. Xu, B. Firner, R. S. Moore, Y. Zhang, W. Trappe, R. Howard, F. Zhang, and N. An, “SCPL: Indoor Device-free Multi-subject Counting and Localization Using Radio Signal Strength,” in Proceedings of ACM IPSN, 2013.   
[3] F. Adib, Z. Kabelac, D. Katabi, and R. Miller, “3D Tracking via Body Radio Reflections,” in Proceedings of USENIX NSDI, 2014.   
[4] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-Home Gesture Recognition Using Wireless Signals,” in Proceedings of ACM MobiCom, 2013.   
[5] P. Melgarejo, X. Zhang, P. Ramanathan, and D. Chu, “Leveraging Directional Antenna Capabilities for Fine-Grained Gesture Recognition,” in Proceedings of ACM UbiComp, 2014.   
[6] Y. Zhao, N. Patwari, J. M. Phillips, and S. Venkatasubramanian, “Radio Tomographic Imaging and Tracking of Stationary and Moving People via Kernel Distance,” in Proceedings of ACM IPSN, 2013.   
[7] J. Wilson and N. Patwari, “Radio Tomographic Imaging with Wireless Networks,” IEEE Transactions on Mobile Computing, vol. 9, no. 5, pp. 621–632, 2010.   
[8] ——, “A Fade-Level Skew-Laplace Signal Strength Model for Device-Free Localization with Wireless Networks,” IEEE Transactions on Mobile Computing, vol. 11, no. 6, pp. 947–958, 2012.   
[9] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 Packet Delivery from Wireless Channel Measurements,” in Proceedings of ACM SIGCOMM, 2010.   
[10] Z. Yang, Z. Zhou, and Y. Liu, “From RSSI to CSI: Indoor Localization via Channel Response,” ACM Computing Surveys, vol. 46, no. 2, p. 25, 2013.   
[11] Y. Mostofi, “Cooperative Wireless-Based Obstacle/Object Mapping and See-Through Capabilities in Robotic Networks,” Mobile Computing, IEEE Transactions on, vol. 12, no. 5, pp. 817–829, May 2013.

[12] A. Gonzalez-Ruiz, A. Ghaffarkhah, and Y. Mostofi, “An Integrated Framework for Obstacle Mapping With See-Through Capabilities Using Laser and Wireless Channel Measurements,” Sensors Journal, IEEE, vol. 14, no. 1, pp. 25–38, Jan 2014.   
[13] D. Huang, R. Nandakumar, and S. Gollakota, “Feasibility and Limits of Wi-fi Imaging,” in Proceedings of ACM SenSys, 2014.   
[14] S. Depatla, L. Buckland, and Y. Mostofi, “X-Ray Vision with Only WiFi Power Measurements Using Rytov Wave Models,” Vehicular Technology, IEEE Transactions on, to appear 2015.   
[15] F. Adib and D. Katabi, “See Through Walls with Wi-Fi!” in Proceedings of ACM SIGCOMM, 2013.   
[16] B. Kellogg, V. Talla, and S. Gollakota, “Bringing Gesture Recognition To All Devices,” in Proceedings of USENIX NSDI, 2014.   
[17] Y. Wang, J. Liu, Y. Chen, M. Gruteser, J. Yang, and H. Liu, “E-eyes: In-home Device-free Activity Identification Using Fine-grained WiFi Signatures,” in Proceedings of ACM MobiCom, 2014.   
[18] F. Q. AL-Khalidi, R. Saatchi, D. Burke, H. Elphick, and S. Tan, “Respiration Rate Monitoring Methods: a Review,” Pediatric Pulmonology, vol. 46, no. 6, pp. 523–529, 2011.   
[19] C. Li, J. Ling, J. Li, and J. Lin, “Accurate Doppler Radar Non-contact Vital Sign Detection using the RELAX Algorithm,” IEEE Transactions on Instrumentation and Measurement, vol. 59, no. 3, pp. 687–695, 2010.   
[20] N. Patwari, J. Wilson, S. Ananthanarayanan, S. Kasera, and D. Westenskow, “Monitoring Breathing via Signal Strength in Wireless Networks,” IEEE Transactions on Mobile Computing, vol. 13, no. 8, pp. 1774–1786, 2014.   
[21] O. J. Kaltiokallio, H. Yigitler, R. Jantti, and N. Patwari, “Non-invasive ¨ Respiration Rate Monitoring using a Single COTS TX-RX Pair,” in Proceedings of ACM IPSN, 2014.   
[22] X. Liu, J. Cao, S. Tang, and J. Wen, “Wi-sleep: Contactless sleep monitoring via wifi signals,” in Proceedings of IEEE RTSS, 2014.   
[23] K. Wu, J. Xiao, Y. Yi, M. Gao, and L. M. Ni, “FILA: Fine-Grained Indoor Localization,” in Proceedings of IEEE INFOCOM, 2012.   
[24] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You Are Facing the Mona Lisa: Spot Localization Using PHY Layer Information,” in Proceedings of ACM MobiSys, 2012.   
[25] J. Xiao, K. Wu, Y. Yi, L. Wang, and L. Ni, “FIMD: Fine-grained Devicefree Motion Detection,” in Proceedings of IEEE ICPADS, 2012.   
[26] W. Xi, J. Zhao, X.-Y. Li, K. Zhao, S. Tang, X. Liu, and Z. Jiang, “Electronic Frog Eye: Counting Crowd Using WiFi,” in Proceedings of IEEE INFOCOM, 2014.   
[27] M. Gast, 802.11 Wireless Networks: the Definitive Guide. ” O’Reilly Media, Inc.”, 2005.   
[28] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “802.11 with Multiple Antennas for Dummies,” ACM SIGCOMM Computer Communication Review, vol. 40, no. 1, pp. 19–25, 2010.   
[29] L. Davies and U. Gather, “The Identification of Multiple Outliers,” Journal of the American Statistical Association, vol. 88, no. 423, pp. 782–792, 1993.   
[30] P. Sebel, M. Stoddart, R. Waldhorn, C. Waldman, and P. Whitfield, Respiration, the Breath of Life. Torstar Books New York, 1985.   
[31] J. F. Murray, The Normal Lung: the Basis for Diagnosis and Treatment of Pulmonary Disease. Saunders, 1986.   
[32] J. C. Lagarias, J. A. Reeds, M. H. Wright, and P. E. Wright, “Convergence Properties of the Nelder–Mead Simplex method in Low Dimensions,” SIAM Journal on Optimization, vol. 9, no. 1, pp. 112– 147, 1998.   
[33] A. Bhartia, Y.-C. Chen, S. Rallapalli, and L. Qiu, “Harnessing Frequency Diversity in Wi-fi Networks,” in Proceedings of ACM MobiCom, 2011.   
[34] P. J. Rousseeuw and A. M. Leroy, Robust Regression and Outlier Detection. Wiley, 2005.   
[35] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Tool Release: Gathering 802.11n Traces with Channel State Information,” ACM SIGCOMM Computer Communication Review, vol. 41, no. 1, p. 53, 2011.   
[36] Y. Ling, S. Alexander, and R. Lau, “On Quantification of Anchor Placement,” in Proceedings of IEEE INFOCOM, 2012.   
[37] X. Zhou, Z. Zhang, Y. Zhu, Y. Li, S. Kumar, A. Vahdat, B. Y. Zhao, and H. Zheng, “Mirror Mirror on the Ceiling: Flexible Wireless Links for Data Centers,” in Proceedings of ACM SIGCOMM, 2012.   
[38] J. Xiong and K. Jamieson, “ArrayTrack: A Fine-Grained Indoor Location System,” in Proceedings of USENIX NSDI, 2013.   
[39] J. Gjengset, J. Xiong, G. McPhillips, and K. Jamieson, “Phaser: Enabling phased array signal processing on commodity wifi access points,” in Proceedings of ACM MobiCom, 2014.   
[40] S. Gollakota and D. Katabi, “Zigzag Decoding: Combating Hidden Terminals in Wireless Networks,” in Proceedings of ACM SIGCOMM, 2008.

![](images/9804c44e042946c4b927215940c7af4182a103fa4a61cea6fb95911a137b6bca.jpg)



Chenshu Wu received his B.S. degree in School of Software from Tsinghua University, Beijing, P.R. China, in 2010. He is now a Ph.D. student in the Department of Computer Science and Technology, Tsinghua University. His research interests include wireless ad-hoc/sensor networks and mobile computing. He is a student member of the IEEE and the ACM.

![](images/3e15c363b0d2b30d39aa934bbf03e308bc09239183930ca2da0850a7627a40f6.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an assistant professor in Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM. He is awarded the 2011 National Nature Science Award (second class).

![](images/b25fad62125481868ac83b4a27b6bff3f17e9d853bd5375689f4d8d0ccf327e7.jpg)



Zimu Zhou is currently a Ph.D candidate in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He received his B.E. degree in 2011 from the Department of Electronic Engineering of Tsinghua University, Beijing, China. His main research interests include wireless networks and mobile computing. He is a student member of IEEE and ACM.

![](images/dda136a2421933fe9a96e2b20b4ea32ef06da91b5af770ea1260e92f4afa8bb4.jpg)



Xuefeng Liu received his M.S. and Ph.D. degree from Beijing Institute of Technology, China, and University of Bristol, UK, in 2003 and 2008, respectively. He is currently a Research Fellow at the Department of Computing in Hong Kong Polytechnic University. His research interests include wireless sensor networks, distributed computing and in-network processing. He has served as a reviewer for several international journals/conference proceedings.

![](images/7dd62dca58b90b4240cafa457a108a8c2564ff93518a5d954480bae2f60b9004.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is currently a ChangJiang professor at Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing.

![](images/192320f2c6d3ca1eb1523b8cab8ac25f3f3c7ed2e79f86d277ca35acb57d4ccf.jpg)



Jiannong Cao received the BSc degree in computer science from Nanjing University, China, in 1982, and the MSc and PhD degrees in computer science from Washington State University, Pullman, Washington, in 1986 and 1990, respectively. He is currently the head and chair professor in the Department of Computing at Hong Kong Polytechnic University, Hong Kong. Before joining Hong Kong Polytechnic University, he was on the faculty of computer science at James Cook University, the University of Adelaide in Australia, and the City University of

Hong Kong. His research interests include parallel and distributed computing, networking, mobile and wireless computing, fault tolerance, and distributed software architecture. He has published more than 200 technical papers in the above areas. His recent research has focused on mobile and pervasive computing and mobile cloud computing. He is a senior member of the China Computer Federation, a Fellow of the IEEE and the IEEE Computer Society, and a member of the ACM.