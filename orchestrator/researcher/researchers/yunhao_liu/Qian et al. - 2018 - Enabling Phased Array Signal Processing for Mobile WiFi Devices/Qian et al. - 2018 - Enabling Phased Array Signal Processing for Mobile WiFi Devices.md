# Enabling Phased Array Signal Processing for Mobile WiFi Devices

Kun Qian, Student Member, IEEE, Chenshu Wu, Student Member, IEEE, Zheng Yang, Member, IEEE, Zimu Zhou, Student Member, IEEE, Xu Wang, Student Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract—Modern mobile devices are equipped with multiple antennas, which brings various wireless sensing applications such as accurate localization, contactless human detection and wireless human-device interaction. A key enabler for these applications is phased array signal processing, especially Angle of Arrival (AoA) estimation. However, accurate AoA estimation on commodity devices is non-trivial due to limited number of antennas and uncertain phase offsets. Previous works either rely on elaborate calibration or involve contrived human interactions. In this paper, we aim to enable practical AoA measurements on commodity off-the-shelf (COTS) mobile devices. The key insight is to involve users’ natural rotation to formulate a virtual spatial-temporal antenna array and conduce a relative incident signal of measurements at two orientations. Then by taking the differential phase, it is feasible to remove the phase offsets and derive the accurate AoA of the equivalent incoming signal, while the rotation angle can also be captured by built-in inertial sensors. On this basis, we propose Differential MUSIC (D-MUSIC), a relative form of the standard MUSIC algorithm that eliminates the unknown phase offsets and achieves accurate AoA estimation on COTS mobile devices with only one rotation. We further extend D-MUSIC to 3-D space, integrate extra measurements during rotations for higher estimation accuracy and fortify it in multipath-rich scenarios. We prototype D-MUSIC on commodity WiFi infrastructure and evaluate it in typical indoor environments. Experimental results demonstrate a superior performance with average AoA estimation errors of 13◦ with only 3 measurements and 5◦ with at most 10 measurements. Requiring no modifications or calibration, D-MUSIC is envisioned as a promising scheme for practical AoA estimation on COTS mobile devices.

# 1 INTRODUCTION

Recent years have witnessed the conceptualization and development of wireless sensing, especially using multiantenna devices. Various innovative systems are designed to localize and track mobile devices accurately [1], detect and pinpoint human movements contactlessly [2], and enable human-device interaction wirelessly [3], [4]. A key to such applications is to enable phased array signal processing, which makes various comparisons of signals received from each of the antennas of commodity devices. Particularly, deriving spatial direction of incoming wireless signals, i.e., the Angle of Arrival (AoA), serves as the basis for a number of applications including accurate indoor localization [5], secure wireless communication [6], wireless coverage confining [7] and spatial-aware device interaction [8].

Despite the potential for a myriad of wireless sensing applications, accurate AoA measurement is non-trivial on commodity devices. In principle, it is possible to obtain the incident signals’ directions with a large antenna array. Yet most commercial mobile devices are installed with limited number of antennas (typically fewer than three), making it infeasible to directly derive precise AoA measurements. Even worse, the uncertain phase offsets on commodity WiFi

A preliminary version of this article appeared in International Conference on Computer Communications (IEEE INFOCOM 2016)   
K. Qian, C. Wu, Z. Yang and Y. Liu are with the School of Software and TNLIST, Tsinghua University. C. Wu is also with Jiangsu High Technology Research Key Laboratory for Wireless Sensor Networks. Email: {qiank10, wucs32, hmilyyz, yunhaoliu}@gmail.com   
• Z. Zhou is with Computer Engineering and Networks Laboratory, ETH Zurich.   
E-mail: zzhou@tik.ee.ethz.ch

devices can dramatically deteriorate the performance of classical AoA estimation algorithms e.g. MUltiple SIgnal Classification (MUSIC) [9], leading to unacceptable AoA estimation errors. Pioneer works that achieve accurate AoA measurements either work only for fixed devices with known relative locations between transceivers [10], or involves contrived human intervention to emulate an antenna array to perform sophisticated Synthetic Aperture Radar (SAR) [11]. The vision of AoA estimation on Commercial Off-The-Shelf (COTS) mobile devices without extra efforts entails great challenges and still remains open.

In this paper, we ask the question: can we achieve accurate AoA measurements on COTS mobile devices without modification and with minimal human interaction? As illustrated in Fig. 1, the key insight is to involve rotation, a natural and angleaware user motion, to formulate a virtual spatial-temporal antenna array and a relative incident wireless signal. Specifically, conventional AoA estimation schemes either formulate a spatial array (via physical antennas) or temporal array (via SAR). Yet we take the difference between measurements of one antenna array at two orientations and transform two incident signals into an equivalent relative incident signal. Such a spatial-temporal formulation enjoys two advantages: (1) Since the intrinsic phase offset is unknown yet constant for each individual antenna, taking the differential phase on two measurements naturally remove the phase offset since the antennas are identical. (2) Since the phase measurements of the equivalent incident signal are free of phase offset, the equivalent incident angle can be easily derived using standard AoA estimation algorithms. Furthermore, the equivalent incident angle is coupled with the rotation angle. Given the rotation angle measured by built-in inertial sensors on modern mobile devices, it is feasible to obtain the AoAs before and after rotation with only one rotation. To codify the above insights into a working system, triple challenges reside: (1) Can we obtain unique AoA measurements using minimal rotations? (2) Since wireless signals propagate in 3-D space, can we derive both the azimuth and elevation of each AoA? (3) How to extend the scheme to multipath-rich scenarios?

![](images/f552aa5a762b1e570457021b22dc82b2dbec85da5147069b95569fe40b5cf21d.jpg)



Fig. 1. An illustrative example of D-MUSIC.

To address these challenges, we propose Differential MU-SIC (D-MUSIC), a relative form of the standard MUSIC algorithm that is free of the phase offset for COTS mobile devices. It works by employing users’ natural behaviour of rotating handheld mobile devices and measures the phase information before and after turning via an antenna array as well as records the rotation angle via built-in gyroscope.

To obtain unique solutions of absolute AoAs on relative phase measurements, D-MUSIC further take extra measurement at some orientation during the rotation in addition to the measurements before and after turning, to ensure minimal human interaction.

To decompose both the azimuth and elevation components of each AoA, D-MUSIC exploits the spatial geometric relationships between transceivers during rotation, making D-MUSIC capable of operating in 3-D space with arbitrary transmitter and receiver heights. To fortify D-MUSIC in severe multipath scenarios, we feed D-MUSIC into standard MUSIC algorithms as an auto phase calibration. Since the calibration only needs to be conducted once, D-MUSIC does not exert awkward operations on mobile users while significantly enhances AoA measurements even under multipath environments.

We conducted extensive experiments in various indoor environments to validate the effectiveness and performance of D-MUSIC. Experimental results show that D-MUSIC derives AoA with an average estimation error of 13◦, while standard MUSIC totally fails to yield correct AoA estimation. Particularly, comparable AoA accuracy also holds in 3-D space. We also integrate D-MUSIC as an auto phase correction for previous calibration-based schemes, which yields similar accuracy compared to those obtained by precise manual calibration. Since D-MUSIC achieves delightful performances with neither hardware modifications nor contrived user intervention, we envision it as a promising step towards practical AoA estimation on commodity mobile WiFi receivers, which underpins new insights for plentiful applications in wireless sensing.

In summary, the main contributions are as follows:

We present a novel differential MUSIC algorithm that enables AoA estimation on COTS mobile devices by formulating a virtual spatial-temporal antenna array. D-MUSIC operates with only natural and easy user actions, requiring no hardware modifications, cumbersome calibration, or contrived human intervention.

We extend the applicability of D-MUSIC to 3-D cases with diverse transmitter and receiver heights, which exceeds the achievements of previous schemes. We further integrate multiple measurements from multiple orientations to form a larger spatial-temporal antenna array for higher estimation accuracy. In addition to direct AoA measurements, D-MUSIC can also be employed to tune the unknown phase offsets for numerous applications built upon phased array signal processing, even in multipath-rich scenarios.

We implement D-MUSIC on commodity WiFi devices and validate its effectiveness in various indoor environments. Experimental results demonstrate that D-MUSIC outperforms previous approaches with existence of unknown phase offsets, achieving average estimation error of 13◦ with basic measurements at 3 orientations and 5◦ with measurements at most 10 orientations.

A conference version of this work can be found in [12]. In this paper, we further provide experimental results related to performance of D-MUSIC with detailed technical and implementation issues, and demonstrate the potential versatility of D-MUSIC with different implementation settings. We also provide detailed discussion on limitations of current version of D-MUSIC, and point out the directions of future work of D-MUSIC. Finally, we survey the state-of-art work on AoA-based indoor localization, and explicitly state the difference between D-MUSIC and other work.

The rest of the paper is organized as follows. We provide a primer on AoA estimation and the root causes of AoA estimation errors in Section 2, and detail the principles and designs of D-MUSIC in Section 3. Section 4 evaluates the performance of D-MUSIC. Finally we review related work in Section 6 and conclude in Section 7.

# 2 PRELIMINARIES

This section provides a primer on AoA estimation using the standard MUSIC algorithm, followed by an introduction on the raw phase measurements available on commodity WiFi devices, as well as the impact of phase measurement noise on AoA estimation.

# 2.1 Angle of Arrival Estimation

MUltiple SIgnal Classification (MUSIC) [9] is one of the most commonly adopted algorithm for AoA estimation. It analyses the incident signals on multiple antennas to find out the AoA of each signal. Specifically, suppose D signals $F _ { 1 } , \cdots , F _ { D }$ arrive from directions $\theta _ { 1 } , \cdot \cdot \cdot , { \bar { \theta } } _ { D }$ at $M \ > \ D$ antennas. The received signal at the $i ^ { t h }$ antenna element, denoted as $X _ { i } ,$ is a linear combination of the D incident wavefronts and noise $W _ { i } { \mathrm { : } }$ :

![](images/56b0320daef90c410db1cd93a134f463e7896edf76dfdffd0081b25553777573.jpg)



(a) A signal arrives at an angle θ.

![](images/44924a5b76217d8a7394dc78a813474903e8fafacb42871a2117b3c73ce41930.jpg)



(b) Pseudo spectrum generated by MUSIC.   
![](images/21b609543930db47153ce30c53d3146c03cdafe85d966f0c881bdadf0f206807.jpg)



Fig. 3. Output of MUSIC for a 2-antenna array with random phase offset ranging from −180◦ to 180◦.   
Fig. 2. AoA estimation by standard MUSIC.

$$
\left[ \begin{array}{c} X _ {1} \\ X _ {2} \\ \vdots \\ X _ {M} \end{array} \right] = \left[ \mathbf {a} (\theta_ {1}) \mathbf {a} (\theta_ {2}) \ldots \mathbf {a} (\theta_ {D}) \right] \left[ \begin{array}{c} F _ {1} \\ F _ {2} \\ \vdots \\ F _ {D} \end{array} \right] + \left[ \begin{array}{c} W _ {1} \\ W _ {2} \\ \vdots \\ W _ {M} \end{array} \right]
$$

or

$$
\mathbf {X} = \mathbf {A F} + \mathbf {W} \tag {1}
$$

where $\mathbf { a } ( \theta _ { i } )$ is the array steering vector that characterizes added phase (relative to the first antenna) of each receiving component at the $i ^ { t h }$ antenna. A is the matrix of steer vectors. As shown in Fig. 2a, for a linear antenna array with elements well synchronized,

$$
\mathbf {a} (\theta) = \left[ \begin{array}{c} 1 \\ e ^ {- j 2 \pi \frac {d}{\lambda} \cos \theta} \\ e ^ {- j 2 \pi \frac {2 d}{\lambda} \cos \theta} \\ \vdots \\ e ^ {- j 2 \pi \frac {(M - 1) d}{\lambda} \cos \theta} \end{array} \right] \tag {2}
$$

Suppose $W _ { i } \sim N ( 0 , \sigma ^ { 2 } )$ , and $F _ { i }$ is a wide-sense stationary process with zero mean value, the $M \times M$ covariance matrix of the received signal vector X is:

$$
\begin{array}{l} S = \overline {{\mathbf {X X} ^ {*}}} \\ = \mathbf {A} \overline {{\mathbf {F F} ^ {*}}} \mathbf {A} ^ {*} + \overline {{\mathbf {W W} ^ {*}}} \tag {3} \\ = \mathbf {A P A} ^ {*} + \sigma^ {2} \mathbf {I} \\ \end{array}
$$

where P is the covariance matrix of transmission vector F. The notation $( \cdot ) ^ { * }$ represents conjugate transpose and (·) represents expectation.

The covariance matrix S has M eigenvalues $\lambda _ { 1 } , \cdots , \lambda _ { M }$ associated with M eigenvectors $\mathbf { e } _ { 1 } , \mathbf { e } _ { 1 } , \cdots , \mathbf { e } _ { M }$ . Sorted in a non-descending order, the smallest $M - D$ eigenvalues correspond to the noise while the rest D correspond to the D incident signals. In other word, the M -dimension space can be divided into two orthogonal subspace, the noise subspace $\mathbf { E _ { N } }$ expanded by eigenvectors $\mathbf { e } _ { 1 } , \cdots , \mathbf { e } _ { M - D } ,$ and the signal subspace $\mathbf { E _ { S } }$ expanded by eigenvectors $\ e _ { M - D + 1 } , \cdots$ , eM (or equivalently $\mathbf { \bar { \rho } } _ { D }$ array steering vector $\mathbf { a } ( \theta _ { 1 } ) , \cdot \cdot \cdot , \mathbf { a } ( \theta _ { D } ) )$ .

To solve for the array steering vectors (thus AoA), MU-SIC plots the reciprocal of squared distance $Q ( \theta )$ for points along the θ continuum to the noise subspace as a function of θ (Fig. 2b):

$$
Q (\theta) = \frac {1}{\mathbf {a} ^ {*} (\theta) \mathbf {E} _ {\mathbf {N}} \mathbf {E} _ {\mathbf {N}} ^ {*} \mathbf {a} (\theta)} \tag {4}
$$

This yields peaks in $Q ( \theta )$ at the bearing of incident signals.

As discussed above, MUSIC requires well synchronization of antennas, or at least knowledge of relative phase offsets between antennas. However, such information is usually unavailable on unsynchronized commercial-off-theshelf wireless devices, which limits the usage of MUSIC.

# 2.2 Phase Measurement Noise

Phase information can be extracted from PHY layer Channel State Information (CSI) [13], which is nowadays reachable from upper layers on off-the-shelf Network Interface Cards with only slight driver modification[14]. CSI portrays both amplitude and phase information of OFDM subcarriers:

$$
H (f _ {k}) = | H (f _ {k}) | e ^ {j \angle H (f _ {k})} \tag {5}
$$

where $H ( f _ { k } )$ is the CSI at the subcarrier with central frequency $f _ { k } . \ \| H ( f _ { k } ) \|$ and $\angle H ( f _ { k } )$ denote its amplitude and phase.

The raw phase measurements in CSI, however, are polluted by random noises and appear to be meaningless for practical use. Specifically, the measured phase $\hat { \phi } _ { i }$ for the $i ^ { t h }$ subcarrier of the $j ^ { t h }$ antenna can be expressed as:

$$
\hat {\phi} _ {i} ^ {j} = \phi_ {i} ^ {j} - 2 \pi \frac {k _ {i}}{N} \delta + \beta_ {j} + Z \tag {6}
$$

where $\phi _ { i } ^ { j }$ is the real phase that contains AoA information, δ is the timing offset at the receiver, which causes phase error expressed as the middle term, $\beta _ { j }$ is a constant unknown phase of the $j ^ { t h }$ antenna, and $Z$ is some measurement noise. $k _ { i }$ denotes the subcarrier index (ranging from -28 to 28 in IEEE 802.11n) of the $i ^ { t h }$ subcarrier and N is the FFT size (64 in IEEE 802.11 $\mathsf { a } / \mathsf { g } / \mathsf { n } )$ .

The phase offset incurred by timing offset δ has no impact on AoA estimation, since it is consistent across all antennas of a Network Interface Card (NIC), while AoA estimation only requires the phase difference between individual antennas. The constant term $\beta _ { j }$ , however, varies across each antenna, thus deteriorating the fidelity of MU-SIC outputs. As shown in Fig. 3, the unknown phase offsets can dramatically degrade the performance of the standard MUSIC, making it incapable of obtaining true AoAs on commodity WiFi NICs. In practice, MUSIC would further degenerate into ineffectiveness due to the facts of severe multipath effects indoors versus limited number of antennas on COTS devices. As a result, the vision of practical AoA estimation on commodity mobile devices still remains unsettled.

![](images/ba4c207abbfa776ff303ee9671485a0ae882c6b3af465423d9c07e6c0a277464.jpg)



(a) virtual spatial-temporal antenna array.

![](images/18a6874702cd3cd2c7fee55f5038cc1d487ea15b7486c4a5059b78de3645fe26.jpg)



(b) Resolving ambiguity.

![](images/ea2e3af6121bbbccf9aefc79e1c21284ad51b358f0b3f03e357bc5025dd96753.jpg)



(c) Generalizing to 3-D cases.   
Fig. 4. Principle of D-MUSIC.

# 3 DIFFERENTIAL MUSIC

Fundamentally constrained by the measurement noise, it is infeasible to directly apply the standard MUSIC algorithm on the polluted CSI for accurate AoA estimation. In this section, we firstly propose D-MUSIC, a relative form of the MUSIC algorithm that eliminates impact of unknown phase offsets by rotating the antenna array. Then, we introduce measurement of rotation of array. Finally, we discuss practical use of D-MUSIC in multipath environment.

# 3.1 Principle of Differential MUSIC

As discussed in Section 2, when signal arrives at an $N -$ antenna linear array, the measured phase $\hat { \phi } _ { i }$ for the $i ^ { t h }$ antenna can be expressed as:

$$
\hat {\phi} _ {i} = - 2 \pi \frac {(i - 1) d}{\lambda} \cos \theta + \beta_ {i} + Z \tag {7}
$$

where d denotes the antenna spacing, λ is the wavelength of transmission. θ denotes the AoA, $\beta _ { i }$ is the constant unknown phase offset of the $i ^ { t h }$ antenna, and $Z$ is some measurement noise. To mitigate the impact of the unknown phase offset, instead of directly measuring AoA, we propose D-MUSIC to estimate phase change of array at different orientations.

# 3.1.1 MUSIC by Turning

The key insight of D-MUSIC is that, the uncertain phase offset is constant for each antenna. Thus, the uncertain offset can be cancelled out by subtracting phases of signals with different AoA on each antenna. As depicted in Fig. 4a, suppose that the signal propagates from a distant transmitter and arrives at the antenna array with an AoA of $\theta _ { 1 }$ . To estimate $\theta _ { 1 } ,$ we rotate the linear array counterclockwise by $\Delta \theta .$ . Thus the AoA after rotation becomes $\theta _ { 2 } = \theta _ { 1 } + \Delta \theta$ .

Denote the measured phases of the $i ^ { t h }$ antenna before and after rotation as $\hat { \phi } _ { 1 , i }$ and $\hat { \phi } _ { 2 , i } .$ . According to Equation $^ { 7 , }$ the phase difference caused by rotation is:

$$
\hat {\phi} _ {2 1, i} = \hat {\phi} _ {2, i} - \hat {\phi} _ {1, i} = - 2 \pi \frac {(i - 1) d}{\lambda} (\cos \theta_ {2} - \cos \theta_ {1}) \tag {8}
$$

We make two observations on Equation 8 here:

By subtraction between the measurements at two orientations, the constant unknown phase offset $\beta _ { i }$ is successfully cancelled out.   
If we formally define $\theta _ { 2 1 } = \operatorname { a r c c o s } ( \cos \theta _ { 2 } - \cos \theta _ { 1 } ) .$ , Equation 8 becomes the same form as Equation 2. That is, Equation 8 can be regarded as an equivalent signal with AoA of $\theta _ { 2 1 }$ and phase measurement $\hat { \phi } _ { 2 1 , i }$ on the $i ^ { t h }$ antenna, yet is free of the unknown phase offset $\beta _ { i }$ .

Based on the above observations, we can thus adopt standard MUSIC on the phase difference measurements as in Equation 8 to accurately estimate $\theta _ { 2 1 }$ without the impact of the unknown phase offset. If we further capture the rotation $\Delta \theta$ via the built-in inertial sensors on most smart devices, we have:

$$
\left\{ \begin{array}{l} \theta_ {2 1} = \arccos (\cos \theta_ {2} - \cos \theta_ {1}) \\ \Delta \theta = \theta_ {2} - \theta_ {1} \end{array} \right. \tag {9}
$$

Hence we can derive both $\theta _ { 2 }$ and $\theta _ { 1 }$ from the above equations.

# 3.1.2 Obtaining Unique Solutions

The above D-MUSIC principle involves two subtleties to get unique AoAs.

Firstly, the term $\hat { \phi } _ { 2 1 , 2 } = - 2 \pi { \textstyle \frac { d } { \lambda } } ( \cos \theta _ { 2 } - \cos \theta _ { 1 } )$ should be within an interval of no more than 2π to derive unique solutions from the MUSIC algorithm. This condition is guaranteed by leveraging the rotation direction and properly setting antenna spacing. Specifically, since cos $\theta _ { 2 1 } =$ cos $\theta _ { 2 } - \cos { \theta _ { 1 } }$ has the sign different against $\Delta \theta = \theta _ { 2 } - \theta _ { 1 }$ , the range of cos $\theta _ { 2 1 }$ can be identified as either [−2, 0) or (0, 2] according to the sign of Δθ. Furthermore, by using commonly used half-wavelength antenna spacing [15], i.e. $\begin{array} { r } { d = \frac { \lambda } { 2 } } \end{array}$ , the range of $\hat { \phi } _ { 2 1 , 2 }$ becomes (0, 2π] or [ 2π, 0), which satisfies the constraint for unique solution.

Secondly, replace $\theta _ { 2 }$ with ${ \bar { \theta } } _ { 1 } + \Delta \theta .$ , then we can deduce that:

$$
\sin (\theta_ {1} + \frac {\Delta \theta}{2}) = - \frac {\cos \theta_ {2 1}}{2 \sin \frac {\Delta \theta}{2}} \tag {10}
$$

However, due to ambiguity of sine function in $[ 0 , \pi ]$ , two solutions can be derived from equation 10:

$$
\left\{ \begin{array}{l} \theta_ {1} ^ {\prime} = \theta_ {1} \\ \theta_ {2} ^ {\prime} = \theta_ {2} \end{array} \right. \quad \left\{ \begin{array}{l} \theta_ {1} ^ {\prime \prime} = \pi - \theta_ {2} \\ \theta_ {2} ^ {\prime \prime} = \pi - \theta_ {1} \end{array} \right. \tag {11}
$$

To resolve ambiguity, we rotate the array once more and measure signal phases from an extra direction $\theta _ { 3 }$ . By performing D-MUSIC for pairs of measurements $( \theta _ { 1 } , \theta _ { 2 } )$ and $( \theta _ { 2 } , \theta _ { 3 } )$ , we get four possible combination of solutions. As in Fig. 4b, denoting the solutions for $\theta _ { 2 }$ in $( \theta _ { 2 } , \theta _ { i } )$ as $\boldsymbol { \theta } _ { 2 ; i } ^ { ' }$ and $\theta _ { 2 : i } ^ { ^ { \prime \prime } } \left( i = 1 , 3 \right)$ , only the combination of correct solutions $\boldsymbol { \theta } _ { 2 ; 1 } ^ { ' }$ and $\boldsymbol { \theta } _ { 2 ; 3 } ^ { ' }$ overlaps. Thus, we can identify the correct AoA by finding the combination of solutions whose estimations of $\theta _ { 2 }$ are most closed.

# 3.1.3 Generalizing to 3-D Scenarios

Since wireless signals propagate in a 3-D space, the actual incident angle consists of an azimuth and an elevation component (Fig. 4c). However, commodity smart devices $e . g$ . smartphones are only equipped with linear antenna arrays. Thus the MUSIC algorithm can only compute the AoA in a plane expanded by the array and transmission (as θ in Fig. 4c). To recover both the azimuth and the elevation component from the AoA estimate θ computed by MUSIC, we utilize the following observation. The AoA estimate θ reported by MUSIC has the following relation with its azimuth (γ) and elevation (τ ):

$$
\cos \theta = \cos \gamma \cos \tau \tag {12}
$$

Following the discussion in Section 3.1, the outputs of $D _ { - }$ MUSIC for pairs of measurements $( \theta _ { 1 } , \theta _ { 2 } )$ and $( \bar { \theta _ { 2 } } , \bar { \theta _ { 3 } } )$ are:

$$
\cos \theta_ {2 1} = (\cos \gamma_ {2} - \cos \gamma_ {1}) \cos \tau \tag {13}
$$

$$
\cos \theta_ {3 2} = (\cos \gamma_ {3} - \cos \gamma_ {2}) \cos \tau
$$

Suppose the horizontal rotation of array satisfies that:

$$
\Delta \theta_ {2 1} = \gamma_ {2} - \gamma_ {1} \tag {14}
$$

$$
\Delta \theta_ {3 2} = \gamma_ {3} - \gamma_ {2}
$$

Then the azimuth and the elevation components of AoAs can be deduced without ambiguity:

$$
\gamma_ {2} = \operatorname{arccot} \frac {\cos \theta_ {3 2} \sin \Delta \theta_ {2 1} - \cos \theta_ {2 1} \sin \Delta \theta_ {3 2}}{\cos \theta_ {3 2} (1 - \cos \Delta \theta_ {2 1}) + \cos \theta_ {2 1} (1 - \cos \Delta \theta_ {3 2})}
$$

$$
\gamma_ {1} = \gamma_ {2} - \Delta \theta_ {2 1}
$$

$$
\gamma_ {3} = \gamma_ {2} + \Delta \theta_ {3 2}
$$

$$
\tau = \arccos \frac {\cos \theta_ {2 1}}{\cos \gamma_ {2} - \cos \gamma_ {1}} = \arccos \frac {\cos \theta_ {3 2}}{\cos \gamma_ {3} - \cos \gamma_ {2}} \tag {15}
$$

Note that the sign of elevation (τ ) cannot be solved by D-MUSIC itself. Yet since WiFi Access Points (AP) are commonly deployed on the ceiling to achieve larger coverage, the elevation (τ ) tends to be non-negative.

# 3.1.4 Integrating Multiple Measurements

In Section 3.1, D-MUSIC is performed by calculating phase difference of two measurements. It is naturally expected that the estimation accuracy can be improved with more measurements. However, since measurements contain timevarying timing offset δ (recall Equation 6), it is impossible to directly integrate more than two measurements. To remove timing offset δ, we further calculate difference of phase differences of antennas.

Specifically, suppose the linear array has M antennas and N measurements are collected during rotation. Denote the signal phase of the $i ^ { t h }$ antenna at the ${ j ^ { t h } }$ measurement as $\hat { \phi } _ { j , i }$ . According to Equation 8, the phase difference of the $j ^ { t h } \left( j \neq 1 \right)$ measurement and the $1 ^ { \dot { s } t }$ measurement of the $\bar { i } ^ { t h }$ antenna is:

$$
\hat {\phi} _ {j 1, i} = \hat {\phi} _ {j, i} - \hat {\phi} _ {1, i} = - 2 \pi \frac {(i - 1) d}{\lambda} (\cos \theta_ {j} - \cos \theta_ {1}) - 2 \pi \frac {k _ {u}}{N} (\delta_ {j} - \delta_ {1}) \tag {16}
$$

Where $\theta _ { j }$ and $\delta _ { j }$ are the AoA and the timing offset of the $j ^ { t h }$ measurement respectively. And $k _ { u }$ is the subcarrier index. To remove timing offset $\delta ,$ we further calculate difference of phase difference of the $i ^ { t h } \ ( i \neq 1 )$ antenna and the 1st antenna:

$$
\hat {\phi} _ {j 1, i 1} = \hat {\phi} _ {j 1, i} - \hat {\phi} _ {j 1, 1} = - 2 \pi \frac {(i - 1) d}{\lambda} (\cos \theta_ {j} - \cos \theta_ {1}) \tag {17}
$$

In 3-D space, cos $\theta _ { j } = \cos \gamma _ { j }$ cos τ , where $\gamma _ { j }$ is the azimuth of the $j ^ { \dot { \tau } h }$ measurement and $\tau$ is the elevation. To unify parameters of steer vectors, we replace $\gamma$ with $\gamma _ { 1 } + \Delta \theta _ { j 1 } ,$ where $\Delta \theta _ { j 1 }$ is the accumulate rotation angle from the $1 ^ { s t }$ to the $j ^ { t h }$ measurement:

$$
\hat {\phi} _ {j 1, i 1} = 4 \pi \frac {(i - 1) d}{\lambda} \cos \tau \sin (\gamma_ {1} + \frac {\Delta \theta_ {j 1}}{2}) \sin \frac {\Delta \theta_ {j 1}}{2} \tag {18}
$$

Thus, by integrating N measurements, $( M - 1 ) ( N - 1 )$ virtual antennas are synthesized. Finally, MUSIC is applied to the virtual antenna array to estimate unified azimuth $\gamma _ { 1 }$ and elevation τ .

# 3.2 Measuring Rotation Angle

Recall Equation 9, the measurement accuracy of rotation angle Δθ acts as a critical yet controllable factor for accurate D-MUSIC. In this section, we theoretically quantify the impact of rotation angle measurement error on D-MUSIC scheme and describe how to measure rotation angles on mobile devices. Then we propose an effective method to rectify the rotation measurement errors to enable accurate D-MUSIC.

# 3.2.1 Impact of Rotation Angle Error

For the 2-D case, according to Equation 10, we can derive the following relationship between the AoA estimation error (errθ ) and the rotation measurement error (errΔθ):

$$
\mathrm{err} _ {\theta_ {1}} = \frac {1}{2} \left(\left| \tan \theta_ {\epsilon} \cot \frac {\Delta \theta}{2} \right| + 1\right) \mathrm{err} _ {\Delta \theta} \tag {19}
$$

where $\begin{array} { r } { \theta _ { \epsilon } = \theta _ { 1 } + \frac { \Delta \theta } { 2 } } \end{array}$ is the AoA of bisector of $\theta _ { 1 }$ and $\theta _ { 2 } .$ . As seen, the AoA estimation accuracy is closely related to two properties of the rotation angle Δθ.

Direction of the Angular Bisector. The coefficient tan $\theta _ { \epsilon }$ approaches infinity if $\theta _ { \epsilon }$ reaches $9 0 ^ { \circ } ,$ thus leading to considerable $\mathrm { e r r } _ { \theta _ { 1 } }$ . Fig. 5 plots theoretical AoA estimation errors for counterclockwise rotation of constant $3 0 ^ { \circ }$ with different start orientations (i.e. different AoA of bisectors $\theta _ { \epsilon } )$ . As can be seen, the closer θ is to $9 0 ^ { \circ } .$ , the larger the AoA estimation error is. However, unacceptable $\mathrm { e r r } _ { \theta _ { 1 } }$ only occurs when $\theta _ { \epsilon }$ is sufficiently close to $9 0 ^ { \circ }$ . Once $\theta _ { \epsilon }$ slightly deviates from $9 0 ^ { \circ }$ , the coefficient tan $\theta _ { \epsilon }$ as well as the estimation error decreases sharply.

![](images/4527c0b71e7f17c8ea932b8428661c762b6ed47ecbd9395dd0e05d95634b9d8b.jpg)



Fig. 5. Examples of estimation deviation for different start AoAs.

![](images/dfdf8519da1f9db7105f9ea74cadcfb14e3498fba7d8b83f82721ae354d98c41.jpg)



Fig. 6. Examples of estimation deviation for different rotation angles.

Scale of the Rotation Angle. The coefficient cot $\scriptstyle { \frac { \Delta \theta } { 2 } }$ approaches infinity when $\Delta \theta$ tends to $0 ^ { \circ }$ , thus also leading to unacceptable $\mathrm { e r r } _ { \theta _ { 1 } }$ . Fig. 6 shows the theoretical AoA estimation errors for counterclockwise rotation of different angles with start orientations towards the transmitter $( i . e . \ \theta _ { 1 } = 9 0 ^ { \circ } )$ . As is shown, the smaller rotation angle $\Delta \theta ,$ the larger AoA estimation error. Consequently, we intend to guide users to rotate at a larger scale for better AoA estimation performance.

# 3.2.2 Measurement of Rotation Angle

As depicted by Fig. 5 and Fig. $^ { 6 , }$ in addition to the two factors discussed above, AoA estimation accuracy is also effected by the rotation measurement error errΔθ.

Generally, the rotation angle can be efficiently measured by inertial sensors built in modern mobile devices. In D-MUSIC, we employ gyroscope to monitor rotation motion. Gyroscope has been widely adopted for device attitude sensing and well demonstrated to be yield sufficiently accurate results. Particularly, although it is difficult to track the absolute phone attitude over a long time, the instantaneous rotation angle can be measured with high precision. For instance, the Euler Axis/Angle method can achieve $9 0 ^ { t h }$ percentile and medium rotation measurement errors of $7 ^ { \circ }$ and $3 ^ { \circ }$ for a one-minute walk [16]. In our situation, if a user holds a phone in hand and rotates it for a period of three seconds, the rotation angle measurement error appears to be less than $0 . 5 ^ { \circ }$ , which is accurate enough for D-MUSIC.

# 3.3 Dealing with Multipath

Signals propagating indoors suffer from severe multipath effects, which lead to receptive signals from multiple transmission paths superimposing at the receiver. As a result, the superimposed signal phase is deviated from direct-path signal phase, which may decrease estimation accuracy of difference of cosine values in Equation 9 and thus lead to erroneous AoA estimates. In extreme cases with serious multipath, D-MUSIC might fail to yield accurate AoA estimation results.

A natural alternative to enable AoA measurement in multipath scenarios is to exploit the standard MUSIC algorithm on sufficient antenna elements [9]. However, as previously discussed, directly applying standard MUSIC on commodity WiFi infrastructure fails to derive AoA due to unknown phase offsets. Recent innovation Phaser [10] searches through the phase offset space to find the solution with which standard MUSIC generates high-quality pseudo-spectrum. A prerequisite for Phaser to operate is the prior knowledge of precise relative direction between the transmitter and the receiver, which is, however, commonly unavailable in mobile environments and is manually obtained in Phaser. D-MUSIC can complement Phaser as an automatic phase calibration by feeding its outputs as an auto correction input for Phaser. Specifically, to calibrate phase offsets of a mobile device, we let a user stay around an AP and rotates the device to estimate the relative direction towards the AP. Given that the line-of-sight signal dominates the overall multipath signals in the surrounding areas of an AP, D-MUSIC can output sufficiently precise results to tune the phase offsets. And by doing this, Phaser is enabled to work even in various scenarios, including multipath-dense environments, without elaborate manual calibration. Note that the uncertain phase offset remains unchanged after each time the device powers up. Thus it is unnecessary to perform D-MUSIC and Phaser every time, as long as the phase offset can be calibrated at the beginning.

In a nutshell, by feeding D-MUSIC into Phaser, we can automatically correct the phase offsets on both fixed devices and mobile devices. By doing this, we enable the standard MUSIC algorithm and its primary variations to accurately calculate AoA even in multipath-dense scenarios.

# 4 EXPERIMENTS AND EVALUATION

# 4.1 Experiment Methodology

Experiment Setup: We conduct experiments in an academic buildings with rooms furnished for different use, as in Fig. 7a. Concretely, we collected data in various scenarios including two classrooms, two laboratory rooms and one meeting room. The laboratory rooms are furnished with cubicle desks, computers, wireless mesh nodes and other plastic and metallic furniture. The classrooms are equipped with a metal platform and more desks and chairs. The meeting room is the smallest room with a big rectangular table placed in the center and several chairs around.

![](images/167b7366a4c18e4d178a2df69849d17a10999cd607b6de57ed0dfd1f44d8dcd7.jpg)



(a) Experiment building (testing areas are highlighted).

![](images/cb54406c590604413982066facd3725278a1f2ce444af62e0e6bfff3264080c7.jpg)



(b) The linear array with pad.

![](images/c882b2e188bb1b29ba7d275b7af5263d4277134936de381a6e17017b42cf9c5b.jpg)



(c) The inside of Mini PC.   
Fig. 7. Experiment settings.

Data Collection: Two types of data, CSI and gyroscope readings, are collected in the experiments. For CSI, we use two mini-desktops (physical size 170mm 170mm) with three external antennas as AP and client. Both minidesktops are equipped with Intel 5300 NIC and run Ubuntu 14.04 OS (Fig. 7c), and are set up to inject in monitor mode [17] on Channel 157 at 5.785GHz. The AP is set to send signals via one antenna. The client’s antennas are spaced at a half-wavelength distance (2.59cm) in a linear form to simulate the antenna array in commodity wireless devices. For gyroscope readings, we use a Google Nexus 7 pad to record inertial sensor data. To acquire a mobile device with three or more antennas and enable it to support CSI measurements, we assemble a receiver by attaching the client antenna array and the pad on a plastic turntable, as shown in Fig. 7b, which can simultaneously measure CSI and sensor readings. The equipment is by default placed 1.3m high, which is the height where people can naturally use their phones.

We collect data in group. For each group of measurements, we place the array with AoA of 0◦, and rotate the turntable with an interval of 15◦, until AoA of 180◦. By doing this, we measure the 13 groups of CSIs at 13 orientations during the rotation and record traces of gyroscope readings. Gyroscope readings for each rotation are recorded by the pad. CSI is collected from 100 packets for each placement of the array. To extensively evaluate the performance of D-MUSIC, we perform measurements with different environment settings, i.e. diverse Tx-Rx distances including 2m, 3m and 4m, different Tx height from 0m to 2m (relative to the client) and different spots with various multipath conditions. For each setting, we conduct 3 groups of measurements. The rotation angles derived from gyroscope readings are marked as ground-truths of corresponding AoAs since we start from an AoA of 0◦ for each measurement.

Implementation: To carry out AoA estimation using differential phase, we implement MUSIC algorithm. The dimension of physical linear array is 1. By combining measurements during rotation, D-MUSIC forms a synthetic 2-D array. To obtain accurate estimation of correlation matrix S, we leverage phase information of multiple subcarriers as “snapshots” for MUSIC algorithm. Thus, the equivalent number of “snapshots” used for constructing the correlation matrix S is the number of subcarriers, i.e. 30. Since WiFi adopts collision avoidance scheme, the report of CSI means that only source AP transmits in the space. So the number of source D is set to 1.

# 4.2 Performance

We first report the overall performance of D-MUSIC and then evaluate impacts of different factors.

# 4.2.1 Overall Performance

To quantitatively evaluate the overall performance of D-MUSIC, we compare D-MUSIC with both Phaser and standard MUSIC without phase calibration. Due to the asymmetric physical geometry of the array, information from the linear array becomes unreliable as AoA θ reaches margins (i.e. 0◦ and 180◦) [5]. Thus, we use data recorded with AoA ranging from 15◦ to 165◦ to fairly compare the methods. In addition, we only consider cases with rotation angle no less than 45◦, where D-MUSIC is generally expected to yield better results according to the impact analysis of scale of rotation angle in Section 4.2.3.

As illustrated in Fig. 8, D-MUSIC achieves average estimation error of 13◦. Phaser slightly outperforms D-MUSIC, due to the prior knowledge of precise Tx-Rx direction. The jitter of CDF curve of Phaser demonstrates the unbalanced performance of Phaser. Specifically, the AoA estimation tends to be more accurate when the signal arrives around the Tx-Rx direction used for calibration. Oppositely, the AoA estimation apparently degrades when the received signal deviates from the calibration direction. In contrast, D-MUSIC performs stably across all tested AoAs, due to accurate measurement of rotation angles. Without phase calibration, standard MUSIC yields a large percentage of estimation error. Concretely, more than 20% cases have estimation error beyond 60◦. It means standard MUSIC fails to work with unknown phase offsets.

In the following, we evaluate the impacts of various factors on performance of D-MUSIC.

# 4.2.2 Impact of Tx-Rx distance

The Tx-Rx distance acts as the most critical factor for D-MUSIC, since it decides the work range of the method. We test Tx-Rx distances including 2m, 3m and 4m. As shown in Fig. 9, D-MUSIC consistently achieves accurate AoA estimation with different Tx-Rx distances. However, the performance of D-MUSIC slightly drops down as the distance increases. It is because that large Tx-Rx distance may lead to complex multipath condition for the link, e.g. increasing number of multipath, decreasing of power of direct-path signal relative to overall signal, etc.

![](images/659746dbc2ecc6e5def9df2b7f29e15d06380b97b7799febb43df339828f8d9e.jpg)



Fig. 8. Overall performance comparisons.

![](images/26521c1188b396107d9ab82dc19d521276460bebece0e479db333fefdcac1f6d.jpg)



Fig. 9. Impact of Tx-Rx distances.

![](images/53946681d91bc2b7e7c4a1601f0d5738e11a9586298fc76d81be0b699f099884.jpg)



Fig. 10. Impact of rotation angles.

# 4.2.3 Impact of rotation angle

As discussed in Section 3.2.1, the quantity of rotation angle impacts estimation error by contributing a coefficient term cot $\frac { \Delta \theta } { 2 }$ to scale up the error. To validate the discussion, we test different rotation angles from $1 5 ^ { \circ }$ (resolution of rotation) to $7 5 ^ { \circ }$ (maximum rotation angle available). To get rid of impacts of other factors, we fix the second measured AoA to 90◦, and vary the rotation angle between each successive two measurement only.

Fig. 10 shows the distribution of AoA estimation error for different rotation angles. The AoA estimation error is significantly large when the rotation angle is small. For cases of $1 \dot { 5 } ^ { \circ }$ and 30◦, the error of the worst case reaches beyond 60◦, meaning that D-MUSIC is no longer usable. As the rotation angle increases, the estimation error quickly diminishes. For cases that rotation angle exceeds 45◦, the average estimation error is less than 10◦, which is sufficient for practical use.

It is worthwhile to note that small rotation angle is not the only factor that degrades the the performance of D-MUSIC. For AoAs spaced with small rotation angle, the corresponding CSI measurements are similar. Thus, the difference of cosine values derived from CSI measurements is relatively small. As a result, CSI measurement noise may contribute more to final result, and further degrades the performance of the method.

# 4.2.4 Impact of orientation

The other factor amplifying CSI measurement noise is the array orientation. Due to the asymmetric physical geometry of the array, the quality of CSI measurements significantly degrades as array becomes parallel with incident signal. Thus, the estimation accuracy degrades accordingly. We evaluate the performance of D-MUSIC for estimating different AoAs in Fig. 11. Concretely, we fix the rotation angle to 45◦, and vary (the second) AoAs from 60◦ to 120◦. As is shown, when AoA deviates from 90◦, estimation error statistically increases. The result is consistent with standard MUSIC, which demonstrates the potential deficiency of linear array.

Note that the bisector also changes with different AoAs. However, since D-MUSIC requires successive two rotations of the array, it is not easy to control two bisectors to simultaneously change towards or away from $9 0 °$ while fixing the rotation angle. Meanwhile, the impact of coefficient term tan $\theta _ { \epsilon }$ is not severe when two AoAs are not strictly symmetrical about $\theta = 9 0 ^ { \circ }$ . Thus, we omit the discussion on impacts of different AoA bisectors.

# 4.2.5 Impact of height

Theoretically, D-MUSIC extends the work range of linear array to a new dimension. Namely, it enables linear array to estimate both azimuth and elevation components of AoA. To evaluate the performance of D-MUSIC in 3-D space, we test relative height difference between AP and client from 0m to 2m. The AP and client are placed at a distance of 4m, which is a common setting in indoor environment.

As shown in Fig. 12, the azimuth error statistically increases as the AP lifts up. The degradation of estimation accuracy with increasing height difference has the same reason as that of decreasing rotation angle (Section 4.2.3). Recall that the output of differential MUSIC in 3-D space is $\left( \cos \gamma _ { 2 } \ - \ \cos \gamma _ { 1 } \right)$ cos τ , where $\gamma _ { 1 }$ and $\gamma _ { 2 }$ are azimuth components and τ is elevation component. As relative height difference (i.e. elevation τ ) increases, difference of CSI measurements of AoAs tends to be smaller, which leads to relatively large CSI measurement noise, and thus degrades the estimation accuracy. When the relative height difference is less than or equal to 1.5m, the average estimation error is below 15◦, which is acceptable for a 3-antenna array. However, when the relative height difference reaches 2m, the performance of D-MUSIC dramatically degrades, with average estimation error greater than 25◦. The main reason that D-MUSIC fails when relative height difference reaches 2m is the environment constraint. Specifically, the floor height of our laboratory building is 3m. To evaluate the height difference of 2m, we have to place the client array near the ground while the transmit antenna near the ceiling. As a result, the multipath condition is aggravated comparing to other height difference cases and the performance of D-MUSIC is thus degraded. However, since the relative height difference is commonly no more than 1.5m, D-MUSIC is applicable to most indoor scenarios.

Comparing with azimuth estimation, elevation estimation is more sensitive to the quality of CSI measurements. The estimation errors in the worst cases even reach 15◦, while the ground-truth are just within 30◦. The considerable errors are potentially caused by inaccurate CSI measurements and small range of elevation components. Fortunately, azimuth components plays a more important role than elevation components in practice. It is sufficient to use azimuth components only in most scenarios such as indoor localization.

# 4.2.6 Impact of multipath

We further test the robustness of D-MUSIC under various multipath conditions. Concretely, we evaluate the performance of D-MUSIC in three different types of rooms, classroom, laboratory and meeting room. In each room, the AP and client are placed at the same height of 1.3m and at a distance of 3m. In classroom, the devices are placed along the passageway between desks, where the desks are lower than the devices. In laboratory, the devices are placed along the passageway between the wall and the cubicle desks, where the wall, the desks and other electronic devices (e.g. mesh nodes) surrounding the link are higher than the devices. In meeting room, due to the space limitation, the AP and client are placed separately against the opposites walls in the east-west direction. The conference table is placed between the devices, at the height of about 0.3m lower.

![](images/0ff61de6a02b1aa30c852c8509da2798723ba78e913ed5dce97c9791bfc62e56.jpg)



Fig. 11. Impact of orientations.

![](images/c5d4c150f00bb702cfed0276de110622e9a23b401c9f96d1c8c2ac4b0d739f5d.jpg)



Fig. 12. Impact of Tx-Rx height differences.

![](images/1ad2630a101aa15abdf29ec775d405299a7946d5e491dd1b6c60555600c8319d.jpg)



Fig. 13. Impact of scenarios.

Fig. 13 shows the performance of D-MUSIC in different environments. In the classroom where the least multipath exists, D-MUSIC achieves the best performance with average estimation error of 3◦. In the laboratory, due to reflection signals from surroundings, the performance of D-MUSIC degrades to average error of $7 ^ { \circ }$ . In the meeting room where the wall and the table generates strong reflection signals, D-MUSIC only achieves an average estimation error of 16◦. In general, the more complex multipath conditions, the worse precision D-MUSIC yields. For further more complex multipath conditions, D-MUSIC might fail to yield precise estimations.

# 4.2.7 Impact of AoA estimation approaches

D-MUSIC uses MUSIC algorithm to estimate AoA from signal phase difference. Since D-MUSIC forms a uniform linear array with rotation, other high-resolution AoA approaches compliant with ULA array may also be used to improve estimation performance. Thus, we further implement ES-PRIT [18] and Matrix Pencil [19] algorithms for performance comparison. Specifically, total least squares (TLS) versions of the algorithms are implemented to reduce the impact of measurement errors. Similar to the MUSIC algorithm, we identify the range of phase difference $\hat { \phi } _ { 2 1 , 2 }$ (Equation 8) as either (0, 2π] or [−2π, 0), according to the sign of rotation angle Δθ.

Fig. 14 shows the performance of D-MUSIC with three AoA estimation approaches, i.e., MUSIC, TLS-ESPRIT and TLS-Matrix Pencil. Three AoA estimation approaches achieve similar average estimation accuracy. Yet ESPRIT and Matrix Pencil have shorter error tails and slightly better performance. The superiority of ESPRIT and Matrix Pencil may attribute to the total least squares technique that minimizes residue errors of both matrix of steer vectors and signal measurements with minimum Frobenius norm [20]. Different from MUSIC algorithm, both ESPRIT and Matrix Pencil algorithms require specific array substructures. Specifically, ESPRIT requires repeated rotation invariant structure, and Matrix Pencil requires uniform linear structure. However, when multiple measurements are integrated, substructures required by both algorithms cannot be fulfilled, as indicated by the form of steer vector in Equation 18. As ESPRIT and Matrix Pencil cannot benefit from multiple measurements, we adopt MUSIC algorithm for AoA estimation with phase difference.

# 4.2.8 Impact of measurement counts

By integrating multiple measurements, D-MUSIC can synthesize larger array and achieve higher performance. To evaluate the impact of number of measurements, we fix the start and end orientations of the array, and vary the number of measurements used for AoA estimation. Specifically, AoAs of the start and end orientations are set to $1 5 ^ { \circ }$ and $1 6 5 ^ { \circ }$ respectively. And all combinations of measurements within this range are used for evaluation.

Fig. 15 shows the performance of D-MUSIC with different number of measurements. When only 3 measurements are used, the average AoA estimation error is 22◦. And the error dramatically decreases as the number of measurements increases. The average error finally converges to $4 ^ { \circ }$ when more than 10 measurements are used. As common WiFi APs broadcast beacons at a mild rate of 10 packets per second, and the rotation of the user lasts a few seconds, the beacons overheard by the client during rotation is sufficient for accurate AoA estimation, making client-side localization practical.

# 4.2.9 Impact of antenna combinations

While a minimum number of antennas required for AoA estimation is 2, we evaluate whether D-MUSIC benefits from extra antenna capacity (i.e. the $3 ^ { r d }$ antenna) provided by common WiFi NICs. Specifically, denote 3 antennas of the linear array as A, B, C respectively, we test all possible antenna combinations: all 3 antennas $( \{ A , B , C \} )$ , adjacent 2 antennas ({A, B}, {B, C}) and non-adjacent 2 antennas $\{ A , C \}$ . Since the antenna spacing of combination $\{ A , C \}$ is twice as large as the maximum antenna spacing required by MUSIC algorithm, we carefully select groups of snapshots to avoid possible estimation ambiguity. Specifically, as discussed in Section 3.1.2, the term $\vec { \phi } _ { 2 1 , 2 }$ should be within an interval of no more than 2π. Thus, with the combination $\{ A , C \}$ , the difference of cosines of AoAs cos $\theta _ { 2 } - \cos \theta _ { 1 }$ should be within [ 1, 0] or [0, 1], which can be easily achieved when the rotation angles between adjacent snapshots are no larger than $6 0 ^ { \circ }$ . So we select groups of snapshots that fulfils this constraint to avoid estimation ambiguity. In practice, the constraint can also be easily achieved, since the sampling rates of both gyroscope and NIC are sufficiently high (e.g. 100 Hz) and measurements with adjacent rotation angles smaller than $6 0 ^ { \circ }$ can be picked out for AoA estimation.

![](images/8da6e8f51ae35730161b9402b27a28b5759db6f0fd441dc863bc3741fc8d75a6.jpg)



Fig. 14. Impact of AoA estimation approaches.

![](images/8f1d177339b74e5c281bd105ba12bdecd94e6e6cab88ea9eb6bab237e3ea8af5.jpg)



Fig. 15. Impact of measurement counts.

![](images/272bd7ea330f0e06631ad8c3ac01e03f23fe0707b3a9881349fdc29bbdc89ed8.jpg)



Fig. 16. Impact of antenna combinations.

Fig. 16 shows the impact of antenna combinations on the performance of D-MUSIC. Among all combinations, the combination of all 3 antennas (i.e. A, B, C ) has the lowest estimation error. The combination of 2 non-adjacent antennas (i.e. A, C ) has slightly higher estimation error. And combinations of 2 adjacent antennas (i.e. {A, B}, {B, C}) have the highest estimation error. The reasons are two fold. First, array aperture size impacts AoA resolution [21]. With fixed antenna spacing, the aperture sizes of combinations A, B, C and $\{ A , C \}$ are twice as larger as that of combinations A, B and $\{ B , C \}$ . As a result, the former combinations have higher AoA resolution and thus better performance. Second, number of antennas impacts variance of AoA estimation error [22]. Thus, the combination {A, B, C} has more antennas and lower estimation error.

# 4.2.10 Impact of bandwidth

While MUSIC algorithm is originally proposed as a narrowband AoA estimator, the 802.11n WiFi signal has a relative wide bandwidth, which may violate the constraint of the algorithm. Therefore, we evaluate the performance of D-MUSIC with different bandwidth. While 802.11n supports up to 40MHz channel, we set the link to work in both channel 157 and 161 simultaneously at HT40 mode, and collect extra groups of data. To perform D-MUSIC with different bandwidth, we select different number of consecutive subcarriers. Specifically, we evaluate D-MUSIC with bandwidth of 40MHz, 20MHz and 10MHz, which correspond to 30, 15, 8 subcarriers respectively.

As shown in Fig. 17, the performance of D-MUSIC degrades from 5◦ to 11◦ in terms of median estimation error as the bandwidth decreases from 40MHz to 10MHz. Thus, we can draw two conclusions on the relation between performance of D-MUSIC and bandwidth available in 802.11n WiFi signal. First, although 802.11n WiFi signal has such a relative wide bandwidth that experiences frequency selective channel, its small ratio between bandwidth and carrier frequency still meets the narrowband constraint of MUSIC algorithm. Second, using wider bandwidth can improve performance of $D / - M U S I { \bar { C } } _ { I }$ , as it mitigates the burst noises experienced in some narrowband spectrum.

# 4.2.11 Impact of carrier grouping

Finally, we consider the impact of another implementation issue, carrier grouping. 802.11n standard specifies that NIC vendors can use grouping method to save the size of the CSI Report field by reporting a single value for each group of $N _ { g }$ adjacent subcarriers. For example, Intel 5300 NIC adopts a grouping factor $N _ { g } ~ = ~ 2$ and only reports 30 out of 56 CSI values for one packet. Thus, we conduct experiments to evaluate whether such implementation issue impacts the performance of D-MUSIC. Specifically, we compare the performance of D-MUSIC between $N _ { g } = 2$ and $N _ { g } = 4 .$ . For the case where $N _ { g } = 4 ,$ , we pick corresponding subcarriers out of subcarriers for the case where $\bar { N _ { g } } = 2$ , as guided by the 802.11n standard.

Fig. 18 shows the performance of D-MUSIC with different carrier grouping factors. As shown, carrier grouping method has minor effect on the performance of $\widetilde { D } / \widetilde { M U S I C } ,$ which demonstrates the versatility of D-MUSIC for NICs with different carrier grouping parameters. An interesting finding is that in Section 4.2.10, for the case of 20MHz bandwidth, we select consecutive 15 subcarriers in the middle of 30 subcarriers for performing D-MUSIC. In contrast, for the case where $N _ { g } = \bar { 4 } ,$ we select 15 subcarriers in an alternation manner. However, only the former case leads to degradation of performance of D-MUSIC, which demonstrates that selection of subcarriers impacts the algorithm significantly.

# 4.3 Performance in Phase Calibration

As stated in Section 3.3, D-MUSIC can be integrated with Phaser to calibrate unknown phase offsets of array elements, eliminating the needs of manually acquired prior knowledge. By doing this, it is also possible to moderately avoid the impacts of multipath by performing standard MUSIC on array with enough number of antennas. We conduct a benchmark experiment to show the capability of phase calibration of D-MUSIC. Concretely, we place the AP and client at a distance of 2m and at the same height of 1.3m in the classroom. And we employ the ground-truth angle and AoA estimated by D-MUSIC as the relative Tx-Rx direction input of Phaser, respectively. The ground-truth of phase offset is measured by splitting a reference signal and routing it to multiple receiving radio chains with a 5GHz splitter.

![](images/26b75e2763bb7aff35e279013617b04365d51766752cf8be36f6bb88ac73ccfb.jpg)



Fig. 17. Impact of bandwidth.

![](images/1a3a27d1afe182c1080c6b228842b9713480f4580318c373d8ecf012847803a9.jpg)



Fig. 18. Impact of carrier grouping.

![](images/7ad54a3bb8d62f823cfc7e016faaef0f32d3a103967236eaf90c0a475b9a3037.jpg)



Fig. 19. Comparison of phase calibration error.

As in Fig. 19, by using ground-truth, Phaser achieves average estimation error of 15◦. While with AoA estimation by D-MUSIC for calibration, Phaser achieves average estimation error of 19◦. The accuracies are comparable, demonstrating the capability of D-MUSIC for accurate phase calibration. Furthermore, standard MUSIC is able to be applied on devices calibrated by D-MUSIC to derive accurate AoA estimation even in severe multipath environments, in case of sufficient antenna numbers.

# 5 LIMITATIONS AND DISCUSSION

In this paper, we demonstrate the feasibility of D-MUSIC for AoA estimation. However, D-MUSIC is envisioned only as early step towards practical scheme for accurate AoA estimation as well as indoor localization on COTS mobile devices. In this section, we discuss limitations of current version of D-MUSIC and lists challenges that are required to solve to further revise D-MUSIC.

Dependence on particular NIC. D-MUSIC relies on the availability of CSI information from the wireless chipset. As a result, D-MUSIC cannot be deployed on mobile devices at present, due to lack of hardware support. It is not a difficult problem since the CSI is already calculated and portrayed by the PHY layer of the hardware for channel estimation, calibration and beamforming purposes. Hence, we envision that with a light-weight modification of drivers, D-MUSIC can be deployed on other WiFi NICs as well.

Feasibility for uniform linear array. D-MUSIC estimates phase difference instead of signal phase to eliminate unknown phase offsets. To achieve it, D-MUSIC leverages the repeated manifold of uniform linear array to generate formal array for estimating phase difference. As a result, D-MUSIC cannot be directly generalized to arbitrary types of arrays. However, in reality, uniform linear array is not the only choice for wireless mobile devices, especially when other factors such as device size and shape are considered more by designers. Moreover, the inherent ambiguity of uniform linear array limits its AoA estimation range within π, which, as a result, can not cover the entire physical space. Thus, the model of D-MUSIC should be generalized to arbitrary array types.

Rotation on horizontal plane. D-MUSIC requires the user to rotate the array completely in the horizontal plane, in order to decouple the azimuth and the elevation in the phase difference. However, in reality, users holding the mobile device in their hands cannot rotate the device perfectly in the horizontal plane. As a result, the azimuth and the elevation of signal AoA are correlated with each other, and cannot be estimated by simply applying MUSIC to phase difference. Thus, the model of D-MUSIC should be revised and efficiently evaluated to overcome imperfect rotation performed by real users, which is leaved as future work.

Indirect estimation in multipath-rich scenarios. In current version of D-MUSIC, we overcome multipath effect by indirectly using D-MUSIC as a step for phase calibration. However, the operation of calibration is annoying for practical use. The ideal usage of D-MUSIC is to directly estimate AoA in even in multipath-rich scenarios. To achieve it, much more array elements than current three elements available on Intel 5300 NIC are required. Obtaining sufficient array elements, either by using more physical antennas or by performing more virtual rotations, is one direction of our future work.

Client-side AoA-based localization. D-MUSIC can facilitate client-side AoA-based indoor localization. Comparing with mainstream AP-side localization methods [5], [23], [24], the client-side localization do not require any modification of WiFi infrastructure, and is thus applicable to any WiFi environments with merely location information of APs available. In addition, D-MUSIC helps remove unknown phase offsets and enable direct AoA estimation using COTS wireless mobile devices. Practical localization with D-MUSIC requires simultaneously AoA estimation of multiple APs, which can be achieved with beacons of APs received during rotations [11]. However, as AoAs are estimated in the local frame of the mobile client, it is still unclear the least number of APs required to uniquely pinpoint the client. We leave it for further study.

# 6 RELATED WORK

Related works roughly fall into following categories.

Measuring AoA via Phased Array. AoA has been widely applied as a signal feature in localization [25], [26], wireless coverage confining [7] and location-based wireless security [6]. A primary functionality of these applications is to measure AoA via phased antenna arrays [27]. Wong et al. [28] explores standard phase array processing to obtain AoA, yet fails to develop a practical localization scheme. Array-Track [5] improves AoA with spatial smoothing and spectra grouping to suppress multipath effect to achieve sub-meter localization accuracy with a rectangular array of 16 antennas on dedicated software-defined radio platforms. To enable accurate AoA measurements, it is important to calibrate for unknown phase offset. Our work is motivated by the increasing popularity of AoA-based applications and strives to enable accurate AoA measurement as well as provide a light-weight phase calibration scheme on commodity WiFi infrastructure.

The state-of-the-art work, SpotFi [23], leverages the difference of complex responses of sub-carriers available in CSI to generate smoothed CSI matrix and simultaneously estimate AoA and Time of Flight (ToF). As SpotFi manually calibrates phased array as in ArrayTrack [5], D-MUSIC can complement SpotFi as a light-weight one-time phase calibration method.

Inertial Sensor Auxiliaries. The inertial sensors on modern smart devices bring in an orthogonal dimension for AoA estimation by providing various mobility information [29]. Ubicarse [11] calculates accurate displacement of SAR using gyroscope and active drift compensation algorithm based on mapping of AoA profile. CUPID [30] utilizes compass and accelerometer to compute human moving distance, and further identifies angle of the direct path using geometric constraints. Our work also harnesses mobility information to assist AoA estimation and is complementary to these works. Unlike Ubicarse [11] where spatial phase difference between antennas is calculated to generate “translation-resilient” SAR, our scheme compute temporal phase difference of each single antenna to perform Differential MUSIC. Also, Ubicarse needs high-resolution sensors to record a relatively long trace during device motion. Conversely, our scheme only requires gyroscope readings within one rotation, which thus dramatically avoids the accumulative errors of inertial sensors in the long-run. The rotation operation is also more natural and convenient than CUPID [30] where users are required to walk for a few steps.

Phase Calibration. Phase calibration is crucial for wireless communications and mobile computing applications. Argos [31] performs phase calibration by sending from one antenna on the WARP FPGA-based AP while receiving on the others. Yet this approach is inapplicable on current halfduplex COTS wireless devices, where they cannot transmit and receive on different antennas simultaneously. Another approach is to utilize an extra reference. Chen et al. [32] exploit a short reference signal sent from an additional reference transmitter at a known location to eliminate phase offsets of COTS wireless devices. Phaser [10] computes AoA spectrum of signal sent from reference transmitter, and estimates the unknown phase offsets which lead to maximum likelihood AoA spectrum. One drawback of these calibration schemes is that they require the absolute position of reference transmitter a prior that is only possible to be precisely acquired by manual measurement, and need recalibration for every new wireless network. Conversely, our work utilizes inertial sensors on smart devices to eliminate the need for reference transmitters, enabling phase calibration on COTS wireless devices.

# 7 CONCLUSION

In this paper, we propose D-MUSIC, a relative form of standard MUSIC algorithms that enables accurate AoA estimation on commodity WiFi devices. We leverage users’ natural behaviour of rotation to formulate a virtual spatial-temporal antenna array and a corresponding relative incident signal. The incident angle of the relative signal is derived by standard AoA estimation algorithm, and meanwhile captured by inertial sensors as the rotation angle. Thus D-MUSIC can obtain the AoAs within only one rotation, yet without the impacts of the unknown phase offset on each antenna. D-MUSIC is feasible in 3-D cases with various transmitter and receiver heights, which is beyond the achievements of previous works. Furthermore, we fortify D-MUSIC for multipathrich scenarios by employing its outputs as an auto phase calibration for standard MUSIC algorithm. Extensive experimental results have validated the feasibility of D-MUSIC, with an average error of 13◦ with only 3 measurements and 5◦ with at most 10 measurements. Requiring no hardware modifications or cumbersome calibration, D-MUSIC is envisioned as an early step towards a practical scheme for AoA estimation on COTS mobile devices. Future works include further enhancing D-MUSIC in rich multipath conditions and applying D-MUSIC for accurate indoor localization.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC under grant 61522110, 61332004, 61472098, 61672319, 61632008, National Key Research Plan under grant No. 2016YFC0700100.

# REFERENCES

[1] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” IEEE Transactions on Mobile Computing, vol. 14, no. 2, pp. 444–457, 2015.   
[2] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller, “3d tracking via body radio reflections,” in Proc. of USENIX NSDI, 2014.   
[3] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proc. of ACM MobiCom, 2013.   
[4] C. Wu, Z. Yang, Z. Zhou, X. Liu, Y. Liu, and J. Cao, “Noninvasive detection of moving and stationary human with wifi,” IEEE Journal on Selected Areas in Communications, vol. 33, no. 11, pp. 1–14, Nov 2015.   
[5] J. Xiong and K. Jamieson, “Arraytrack: A fine-grained indoor location system.” in Proc. of USENIX NSDI, 2013.   
[6] , “Secureangle: improving wireless security using angle-ofarrival information,” in Proc. of ACM HotNets, 2010.   
[7] A. Sheth, S. Seshan, and D. Wetherall, “Geo-fencing: Confining wifi coverage to physical boundaries,” in Proc. of Springer Pervasive, 2009.   
[8] Z. Sun, A. Purohit, R. Bose, and P. Zhang, “Spartacus: spatiallyaware interaction for mobile devices through energy-efficient audio sensing,” in Proc. of ACM MobiSys, 2013.   
[9] R. O. Schmidt, “Multiple emitter location and signal parameter estimation,” IEEE Transactions on Antennas and Propagation, vol. 34, no. 3, pp. 276–280, 1986.   
[10] J. Gjengset, J. Xiong, G. McPhillips, and K. Jamieson, “Phaser: enabling phased array signal processing on commodity wifi access points,” in Proc. of ACM MobiCom, 2014.   
[11] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proc. of ACM MobiCom, 2014.   
[12] K. Qian, C. Wu, Z. Yang, Z. Zhou, X. Wang, and Y. Liu, “Tuning by turning: Enabling phased array signal processing for wifi with inertial sensors,” in Proc. of IEEE INFOCOM, 2016.   
[13] Z. Yang, Z. Zhou, and Y. Liu, “From rssi to csi: Indoor localization via channel response,” ACM Computing Surveys (CSUR), vol. 46, no. 2, p. 25, 2013.   
[14] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 packet delivery from wireless channel measurements,” in Proc. of ACM SIGCOMM, 2010.   
[15] J. Choi, Optimal combining and detection: statistical signal processing for communications. Cambridge University Press, 2010.   
[16] P. Zhou, M. Li, and G. Shen, “Use it free: Instantly knowing your phone attitude,” in Proceedings of the 20th annual international conference on Mobile computing and networking, 2014.

[17] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Tool release: Gathering 802.11 n traces with channel state information,” ACM SIGCOMM Computer Communication Review, vol. 41, no. 1, pp. 53– 53, 2011.   
[18] R. Roy and T. Kailath, “Esprit-estimation of signal parameters via rotational invariance techniques,” IEEE Transactions on acoustics, speech, and signal processing, vol. 37, no. 7, pp. 984–995, 1989.   
[19] Y. Hua and T. K. Sarkar, “Matrix pencil method for estimating parameters of exponentially damped/undamped sinusoids in noise,” IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 38, no. 5, pp. 814–824, 1990.   
[20] G. H. Golub and C. F. Van Loan, Matrix computations. JHU Press, 2012, vol. 3.   
[21] C. Zhou, F. Haber, and D. L. Jaggard, “A resolution measure for the music algorithm and its application to plane wave arrivals contaminated by coherent interference,” IEEE Transactions on signal processing, vol. 39, no. 2, pp. 454–463, 1991.   
[22] P. Stoica and A. Nehorai, “Music, maximum likelihood, and cramer-rao bound,” IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 37, no. 5, pp. 720–741, 1989.   
[23] M. Kotaru, K. Joshi, D. Bharadia, and S. Katti, “Spotfi: Decimeter level localization using wifi,” in Proc. of ACM SIGCOMM, 2015.   
[24] J. Xiong, K. Sundaresan, and K. Jamieson, “Tonetrack: Leveraging frequency-agile radios for time-based indoor wireless localization,” in Proc. of ACM MobiCom. ACM, 2015, pp. 537–549.   
[25] D. Niculescu and B. Nath, “Vor base stations for indoor 802.11 positioning,” in Proc. of ACM MobiCom, 2004.   
[26] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Stpp: Spatial-temporal phase profiling-based method for relative rfid tag localization,” IEEE/ACM Transactions on Networking (TON), vol. 25, no. 1, pp. 596–609, 2017.   
[27] D. Inserra and A. M. Tonello, “A frequency-domain los angle-ofarrival estimation approach in multipath channels,” IEEE Transactions on Vehicular Technology, vol. 62, no. 6, pp. 2812–2818, 2013.   
[28] C. Wong, R. Klukas, and G. Messier, “Using wlan infrastructure for angle-of-arrival indoor user location,” in Proc. of IEEE VTC, 2008.   
[29] Z. Yang, C. Wu, Z. Zhou, X. Zhang, X. Wang, and Y. Liu, “Mobility increases localizability: a survey on wireless indoor localization using inertial sensors,” ACM Computing Surveys, vol. 47, no. 3, p. 54, 2015.   
[30] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Avoiding multipath to revive inbuilding wifi localization,” in Proc. of ACM MobiSys, 2013.   
[31] C. Shepard, H. Yu, N. Anand, E. Li, T. Marzetta, R. Yang, and L. Zhong, “Argos: Practical many-antenna base stations,” in Proc. of ACM MobiCom, 2012.   
[32] H.-C. Chen, T.-H. Lin, H. Kung, C.-K. Lin, and Y. Gwon, “Determining rf angle of arrival using cots antenna arrays: a field evaluation,” in Proc. of IEEE MILCOM, 2012.

![](images/992fab5f38b203e63f9dfba325deed61ebd694cc3d40b35deca461b5bd29d158.jpg)



Chenshu Wu received his B.E. degree in School of Software in 2010 and Ph.D. degree in Computer Science in 2015, both from Tsinghua University. He is currently with the School of Software at Tsinghua University and the Tsinghua National Lab for Information Science and Technology. His research interests include wireless networks and mobile computing. He is a student member of the IEEE and the ACM.

![](images/6739508ab747731f7e05efa7c4b375b70f9304dda064d4b0fd4c2ce93a6a4746.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an assistant professor in Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing.

![](images/4c56e6ae6aa04b5404bb6707cdc9b4130684490b657ff1d5e09025a26b6a1a26.jpg)



Zimu Zhou is currently a Ph.D candidate in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He received his B.E. degree in 2011 from the Department of Electronic Engineering of Tsinghua University, Beijing, China. His main research interests include wireless networks and mobile computing. He is a student member of IEEE and ACM.

![](images/5897be8617ed84a20572b8738a9704dd6b03f4bb2a2d60b5648f63e90e639408.jpg)



Xu Wang received his B.E. degree in School of Software from Tsinghua University in 2015. He is currently a PhD student in School of Software at Tsinghua University. He is a member of the Tsinghua National Lab for Information Science and Technology. His research interests include wireless networks and mobile computing. He is a student member of the IEEE.

![](images/3909963765197c69b725345356b4ba1f99deab8bf8df690f4d8f825483984dd7.jpg)



Kun Qian received his B.E. degree in School of Software from Tsinghua University in 2014. He is currently a PhD student in School of Software at Tsinghua University. He is a member of the Tsinghua National Lab for Information Science and Technology. His research interests include wireless networks and mobile computing. He is a student member of the IEEE.

![](images/0c1bec506dbd7cce3fad18213eb309c1f2081b7484c34ab658925380e6a68c8f.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now EMC Chair Professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peerto-peer computing, and pervasive computing. He is a senior member of the IEEE.