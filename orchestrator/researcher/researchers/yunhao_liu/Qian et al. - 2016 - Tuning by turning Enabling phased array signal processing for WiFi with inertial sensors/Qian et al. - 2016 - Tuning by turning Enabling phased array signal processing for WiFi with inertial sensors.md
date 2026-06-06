# Tuning by Turning: Enabling Phased Array Signal Processing for WiFi with Inertial Sensors

Kun Qian∗, Chenshu Wu∗, Zheng Yang∗, Zimu Zhou†, Xu Wang∗, Yunhao Liu∗,

∗School of Software and TNList, Tsinghua University

† The Hong Kong University of Science and Technology

Abstract—Modern mobile devices are equipped with multiple antennas, which brings various wireless sensing applications such as accurate localization, contactless human detection and wireless human-device interaction. A key enabler for these applications is phased array signal processing, especially Angle of Arrival (AoA) estimation. However, accurate AoA estimation on commodity devices is non-trivial due to limited number of antennas and uncertain phase offsets. Previous works either rely on elaborate calibration or involve contrived human interactions. In this paper, we aim to enable practical AoA measurements on commodity off-the-shelf (COTS) mobile devices. The key insight is to involve users’ natural rotation to formulate a virtual spatial-temporal antenna array and conduce a relative incident signal of measurements at two orientations. Then by taking the differential phase, it is feasible to remove the phase offsets and derive the accurate AoA of the equivalent incoming signal, while the rotation angle can also be captured by built-in inertial sensors. On this basis, we propose Differential MUSIC (D-MUSIC), a relative form of the standard MUSIC algorithm that eliminates the unknown phase offsets and achieves accurate AoA estimation on COTS mobile devices with only one rotation. We further extend D-MUSIC to 3-D space and fortify it in multipath-rich scenarios. We prototype D-MUSIC on commodity WiFi infrastructure and evaluate it in typical indoor environments. Experimental results demonstrate a superior performance with an average AoA estimation error of 13◦. Requiring no modifications or calibration, D-MUSIC is envisioned as a promising scheme for practical AoA estimation on COTS mobile devices.

# I. INTRODUCTION

Recent years have witnessed the conceptualization and development of wireless sensing, especially using multi-antenna devices. Various innovative systems are designed to localize and track mobile devices accurately [1], detect and pinpoint human movements contactlessly [2], and enable human-device interaction wirelessly [3]. A key to such applications is to enable phased array signal processing, which makes various comparisons of signals received from each of the antennas of commodity devices. Particularly, deriving spatial direction of incoming wireless signals, i.e., the Angle of Arrival (AoA), serves as the basis for a number of applications including accurate indoor localization [1], secure wireless communication [4], wireless coverage confining [5] and spatial-aware device interaction [6].

Despite the potential for a myriad of wireless sensing applications, accurate AoA measurement is non-trivial on commodity devices. In principle, it is possible to obtain the incident signals’ directions with a large antenna array. Yet most commercial mobile devices are installed with limited number of antennas (typically fewer than three), making it infeasible to directly derive precise AoA measurements. Even worse, the uncertain phase offsets on commodity WiFi devices can dramatically deteriorate the performance of classical AoA estimation algorithms e.g. MUltiple SIgnal Classification (MUSIC) [7], leading to unacceptable AoA estimation errors. Pioneer works that achieve accurate AoA measurements either work only for fixed devices with known relative locations between transceivers [8], or involves contrived human intervention to emulate an antenna array to perform sophisticated Synthetic Aperture Radar (SAR) [9]. The vision of AoA estimation on Commercial Off-The-Shelf (COTS) mobile devices without extra efforts entails great challenges and still remains open.

In this paper, we ask the question: can we achieve accurate AoA measurements on COTS mobile devices without modification and with minimal human interaction? As illustrated in Fig. 1, the key insight is to involve rotation, a natural and angle-aware user motion, to formulate a virtual spatialtemporal antenna array and a relative incident wireless signal. Specifically, conventional AoA estimation schemes either formulate a spatial array (via physical antennas) or temporal array (via SAR). Yet we take the difference between measurements of one antenna array at two orientations and transform two incident signals into an equivalent relative incident signal. Such spatial-temporal formulation enjoys two advantages: (1) Since the intrinsic phase offset is unknown yet constant for each individual antenna, taking the differential phase on two measurements naturally remove the phase offset since the antennas are identical. (2) Since the phase measurements of the equivalent incident signal are free of phase offset, the equivalent incident angle can be easily derived using standard AoA estimation algorithms. Furthermore, the equivalent incident angle is coupled with the rotation angle. Given the rotation angle measured by built-in inertial sensors on modern mobile devices, it is feasible to obtain the AoAs before and after rotation with only one rotation. To codify the above insights into a working system, triple challenges reside: (1) Can we obtain unique AoA measurements using minimal rotations? (2) Since wireless signals propagate in 3-D space, can we derive both the azimuth and elevation of each AoA? (3) How to extend the scheme to multipath-rich scenarios?

To address these challenges, we propose Differential MUSIC (D-MUSIC), a relative form of the standard MUSIC algorithm that is free of the phase offset for COTS mobile devices. It works by employing users’ natural behaviour of rotating handheld mobile devices and measures the phase information before and after turning via an antenna array as well as records the rotation angle via built-in gyroscope. To obtain unique solutions of absolute AoAs on relative phase measurements, D-MUSIC is applied on only one extra orientation (included in the same rotation as another two orientations) to ensure minimal human interaction. To decompose both the azimuth and elevation components of each AoA, D-MUSIC exploits the spatial geometric relationships between transceivers during rotation, making D-MUSIC capable of operating in 3-D space with arbitrary transmitter and receiver heights. To fortify D-MUSIC in severe multipath scenarios, we feed D-MUSIC into standard MUSIC algorithms as an auto phase calibration. Since the calibration only needs to be conducted once, D-MUSIC does not exert awkward operations on mobile users while significantly enhances AoA measurements even under multipath environments.

![](images/3ea0a7aed56456de1f7aacdbbaa70f8a881b77a781872f35a32d138fb3dd32e3.jpg)



Fig. 1. An illustrative example of D-MUSIC

We conducted extensive experiments in various indoor environments to validate the effectiveness and performance of D-MUSIC. Experimental results show that D-MUSIC derives AoA with an average estimation error of 13◦, while standard MUSIC totally fails to yield correct AoA estimation. Particularly, comparable AoA accuracy also holds in 3-D space. We also integrate D-MUSIC as an auto phase correction for previous calibration-based schemes, which yields similar accuracy compared to those obtained by precise manual calibration. Since D-MUSIC achieves delightful performances with neither hardware modifications nor contrived user intervention, we envision it as a promising step towards practical AoA estimation on commodity mobile WiFi receivers, which underpins new insights for plentiful applications in wireless sensing.

In summary, the main contributions are as follows:

• We present a novel differential MUSIC algorithm that enables AoA estimation on COTS mobile devices by formulating a virtual spatial-temporal antenna array. D-MUSIC operates with only natural and easy user actions, requiring no hardware modifications, cumbersome calibration, or contrived human intervention.   
• We extend the applicability of D-MUSIC to 3-D cases

![](images/6d8c68675b9c4071fef245427a1e24e400787e3a3fb9fe222bf1c06c7c21c608.jpg)



Fig. 2. Output of MUSIC for a 2-antenna array with random phase offset ranging from 180◦ to 180◦

with diverse transmitter and receiver heights, which exceeds the achievements of previous schemes. In addition to direct AoA measurements, D-MUSIC can also be employed to tune the unknown phase offsets for numerous applications built upon phased array signal processing, even in multipath-rich scenarios.

• We implement D-MUSIC on commodity WiFi devices and validate its effectiveness in various indoor environments. Experimental results demonstrate that D-MUSIC outperforms previous approaches with existence of unknown phase offsets, achieving an average estimation error of 13◦.

The rest of the paper is organized as follows. We provide a primer on AoA estimation and the root causes of AoA estimation errors in Section II, and detail the principles and designs of D-MUSIC in Section III. Section IV evaluates the performance of D-MUSIC. Finally we review related work in Section V and conclude in Section VI.

# II. PRELIMINARIES

This section provides a primer on AoA estimation using the standard MUSIC algorithm, followed by an introduction on the raw phase measurements available on commodity WiFi devices, as well as the impact of phase measurement noise on AoA estimation.

# A. Angle of Arrival Estimation

MUltiple SIgnal Classification (MUSIC) [7] is one of the most commonly adopted algorithm for AoA estimation. It analyses the incident signals on multiple antennas to find out the AoA of each signal. Specifically, suppose D signals $F _ { 1 } , \cdots , F _ { D }$ arrive from directions $\theta _ { 1 } , \cdots , \theta _ { D }$ at $M \ > \ D$ antennas. The received signal at the $i ^ { t h }$ antenna element, denoted as $X _ { i } ,$ is a linear combination of the D incident wavefronts and noise $W _ { i }$ :

$$
\left[ \begin{array}{c} X _ {1} \\ X _ {2} \\ \vdots \\ X _ {M} \end{array} \right] = \left[ \mathbf {a} (\theta_ {1}) \mathbf {a} (\theta_ {2}) \ldots \mathbf {a} (\theta_ {D}) \right] \left[ \begin{array}{c} F _ {1} \\ F _ {2} \\ \vdots \\ F _ {D} \end{array} \right] + \left[ \begin{array}{c} W _ {1} \\ W _ {2} \\ \vdots \\ W _ {M} \end{array} \right]
$$

$$
X = A F + W \tag {1}
$$

where $\mathbf { a } ( \theta _ { i } )$ is the array steering vector that characterizes added phase (relative to the first antenna) of each receiving component at the $i ^ { t h }$ antenna. For a linear antenna array with elements well synchronized,

$$
\mathbf {a} (\theta) = \left[ \begin{array}{c} 1 \\ e ^ {- 2 \pi \frac {d}{\lambda} \cos \theta} \\ e ^ {- 2 \pi \frac {2 d}{\lambda} \cos \theta} \\ \vdots \\ e ^ {- 2 \pi \frac {(M - 1) d}{\lambda} \cos \theta} \end{array} \right] \tag {2}
$$

Suppose $W _ { i } \sim N ( 0 , \sigma ^ { 2 } )$ , the $M \times M$ covariance matrix of the received signal vector X is:

$$
\begin{array}{l} S = \overline {{X X ^ {*}}} \\ = A \overline {{{F F ^ {*}}}} A ^ {*} + \overline {{{W W ^ {*}}}} \tag {3} \\ = A P A ^ {*} + \sigma^ {2} I \\ \end{array}
$$

where $P$ is the covariance matrix of transmission vector $F .$ .

The covariance matrix S has M eigenvalues $\lambda _ { 1 } , \cdots , \lambda _ { M }$ associated with M eigenvectors $\mathbf { e } _ { 1 } , \mathbf { e } _ { 1 } , \cdots , \mathbf { e } _ { M }$ . Sorted in a non-descending order, the smallest $M \ : - \ : D$ eigenvalues correspond to the noise while the rest D correspond to the D incident signals. In other word, the M-dimension space can be divided into two orthogonal subspace, the noise subspace $E _ { N }$ expanded by eigenvectors $\mathbf { e } _ { 1 } , \cdots , \mathbf { e } _ { M - D }$ , and the signal subspace $E _ { S }$ expanded by eigenvectors $\mathbf { e } _ { M - D + 1 } , \cdot \cdot \cdot , \mathbf { e } _ { M }$ (or equivalently D array steering vector $\mathbf { a } ( \theta _ { 1 } ) , \cdot \cdot \cdot , \mathbf { a } ( \theta _ { D } ) )$ .

To solve for the array steering vectors (thus AoA), MUSIC plots the reciprocal of squared distance $Q ( \theta )$ for points along the θ continuum to the noise subspace as a function of θ:

$$
Q (\theta) = \frac {1}{\mathbf {a} ^ {*} (\theta) E _ {N} E _ {N} ^ {*} \mathbf {a} (\theta)} \tag {4}
$$

This yields peaks in $Q ( \theta )$ at the bearing of incident signals.

As discussed above, MUSIC requires well synchronization of antennas, or at least knowledge of relative phase offsets between antennas. However, such information is usually unavailable on unsynchronized commercial-off-the-shelf wireless devices, which limits the usage of MUSIC.

# B. Phase Measurement Noise

Phase information can be extracted from PHY layer Channel State Information (CSI) [10], which is nowadays reachable from upper layers on off-the-shelf Network Interface Cards with only slight driver modification[11]. CSI portrays both amplitude and phase information of OFDM subcarriers:

$$
H (f _ {k}) = \| H (f _ {k}) \| e ^ {i \angle H (f _ {k})} \tag {5}
$$

where $H ( f _ { k } )$ is the CSI at the subcarrier with central frequency $f _ { k } . \ \| H ( f _ { k } ) \|$ and $\angle H ( f _ { k } )$ denote its amplitude and phase.

The raw phase measurements in CSI, however, are polluted by random noises and appear to be meaningless for practical use. Specifically, the measured phase $\hat { \phi } _ { i }$ for the $i ^ { t h }$ subcarrier of the $j ^ { t h }$ antenna can be expressed as:

$$
\hat {\phi} _ {i} ^ {j} = \phi_ {i} ^ {j} - 2 \pi \frac {k _ {i}}{N} \delta + \beta_ {j} + Z \tag {6}
$$

where $\phi _ { i } ^ { j }$ is the real phase that contains AoA information, δ is the timing offset at the receiver, which causes phase error expressed as the middle term, $\beta _ { j }$ is a constant unknown phase of the $j ^ { t h }$ antenna, and $Z$ is some measurement noise. $k _ { i }$ denotes the subcarrier index (ranging from -28 to 28 in IEEE 802.11n) of the $i ^ { t h }$ subcarrier and N is the FFT size (64 in IEEE 802.11 $\mathrm { a / g / n ) }$ .

The phase offset incurred by timing offset δ has no impact on $\operatorname { A o A }$ estimation, since it is consistent across all antennas of a NIC, while AoA estimation only requires the phase difference between individual antennas. The constant term $\beta _ { j } ,$ , however, varies across each antenna, thus deteriorating the fidelity of MUSIC outputs. As shown in Fig. 2, the unknown phase offsets can dramatically degrade the performance of the standard MUSIC, making it incapable of obtaining true AoAs on commodity WiFi NICs. In practice, MUSIC would further degenerate into ineffectiveness due to the facts of severe multipath effects indoors versus limited number of antennas on COTS devices. As a result, the vision of practical AoA estimation on commodity mobile devices still remains unsettled.

# III. DIFFERENTIAL MUSIC

Fundamentally constrained by the measurement noise, it is infeasible to directly apply the standard MUSIC algorithm on the polluted CSI for accurate AoA estimation. In this section, we firstly propose D-MUSIC, a relative form of the MUSIC algorithm that eliminates impact of unknown phase offsets by rotating the antenna array. Then, we introduce measurement of rotation of array. Finally, we discuss practical use of D-MUSIC in multipath environment.

# A. Principle of Differential MUSIC

As discussed in Section II, when signal arrives at an $N _ { - }$ antenna linear array, the measured phase $\ddot { \phi } _ { i }$ for the $i ^ { t h }$ antenna can be expressed as:

$$
\hat {\phi} _ {i} = - 2 \pi \frac {(i - 1) d}{\lambda} \cos \theta + \beta_ {i} + Z \tag {7}
$$

where d denotes the antenna spacing, λ is the wavelength of transmission. θ denotes the AoA, $\beta _ { i }$ is the constant unknown phase offset of the $i ^ { t h }$ antenna, and Z is some measurement noise. To mitigate the impact of the unknown phase offset, instead of directly measuring AoA, we propose D-MUSIC to estimate phase change of array at different orientations.

1) MUSIC by Turning: The key insight of D-MUSIC is that, the uncertain phase offset is constant for each antenna. Thus, the uncertain offset can be cancelled out by subtracting phases of signals with different AoA on each antenna. As depicted in Fig. 3a, suppose that the signal propagates from a distant transmitter and arrives at the antenna array with an AoA of $\theta _ { 1 } .$ . To estimate $\theta _ { 1 } .$ , we rotate the linear array counterclockwise by Δθ. Thus the AoA after rotation becomes $\theta _ { 2 } = \theta _ { 1 } + \Delta \theta$ .

![](images/0af1279009ee0788e725badba94435cb680278970ac07a40493bca54801a1e21.jpg)



(a) virtual spatial-temporal antenna array

![](images/9c19977f600dde226981eb692678eb434e9352eaddedf853bc301ba0a99ed45d.jpg)



(b) Resolving ambiguity

![](images/8e1edd53e9942bef53ad3b2cbbbd5e988b0e82e276f42ee32da9b13e3d5f1ccf.jpg)



(c) Generalizing to 3-D cases   
Fig. 3. Principle of D-MUSIC

Denote the measured phases of the $i ^ { t h }$ antenna before and after rotation as $\hat { \phi } _ { 1 , : }$ i and $\ddot { \phi } _ { 2 , i }$ . According to Equation 7, the phase difference caused by rotation is:

$$
\hat {\phi} _ {2 1, i} = \hat {\phi} _ {2, i} - \hat {\phi} _ {1, i} = - 2 \pi \frac {(i - 1) d}{\lambda} (\cos \theta_ {2} - \cos \theta_ {1}) \tag {8}
$$

We make two observations on Equation 8 here:

By subtraction between the measurements at two orientations, the constant unknown phase offset $\beta _ { i }$ is successfully cancelled out.   
• If we formally define $\theta _ { 2 1 } \ = \ \operatorname { a r c c o s } ( \cos \theta _ { 2 } - \cos \theta _ { 1 } )$ , Equation 8 becomes the same form as Equation 2. That is, Equation 8 can be regarded as an equivalent signal with AoA of $\theta _ { 2 1 }$ and phase measurement $\phi _ { 2 1 , i }$ on the $i ^ { t h }$ antenna, yet is free of the unknown phase offset $\beta _ { i }$ .

Based on the above observations, we can thus adopt standard MUSIC on the phase difference measurements as in Equation 8 to accurately estimate $\theta _ { 2 1 }$ without the impact of the unknown phase offset. If we further capture the rotation Δθ via the built-in inertial sensors on most smart devices, we have:

$$
\left\{ \begin{array}{l} \theta_ {2 1} = \arccos (\cos \theta_ {2} - \cos \theta_ {1}) \\ \Delta \theta = \theta_ {2} - \theta_ {1} \end{array} \right. \tag {9}
$$

Hence we can derive both $\theta _ { 2 }$ and $\theta _ { 1 }$ from the above equations.

2) Obtaining Unique Solutions: The above D-MUSIC principle involves two subtleties to get unique AoAs.

Firstly, the term $\hat { \phi } _ { 2 1 , 2 } ~ = ~ - 2 \pi { \textstyle \frac { d } { \lambda } } ( \cos \theta _ { 2 } - \cos \theta _ { 1 } )$ should be within an interval of no more than 2π to derive unique solutions from the MUSIC algorithm. This condition is guaranteed by leveraging the rotation direction and properly setting antenna spacing. Specifically, since cos $\theta _ { 2 1 } = \cos \theta _ { 2 }$ cos $\theta _ { 1 }$ has the sign different against $\Delta \theta = \theta _ { 2 } - \theta _ { 1 }$ , the range of cos $\theta _ { 2 1 }$ can be identified as either [−2, 0) or (0, 2] according to the sign of Δθ. Furthermore, by using commonly used halfwavelength antenna spacing [12], $\begin{array} { r } { i . e . \ d = \frac { \lambda } { 2 } } \end{array}$ , the range of $\ddot { \phi } _ { 2 1 , 2 }$ becomes (0, 2π] or $[ - 2 \pi , 0 )$ , which satisfies the constraint for unique solution.

Secondly, replace $\theta _ { 2 }$ with $\theta _ { 1 } + \Delta \theta$ , then we can deduce that:

$$
\sin (\theta_ {1} + \frac {\Delta \theta}{2}) = - \frac {\cos \theta_ {2 1}}{2 \sin \frac {\Delta \theta}{2}} \tag {10}
$$

However, due to ambiguity of sine function in [0, π], two solutions can be derived from equation 10:

$$
\left\{ \begin{array}{l} \theta_ {1} ^ {\prime} = \theta_ {1} \\ \theta_ {2} ^ {\prime} = \theta_ {2} \end{array} \right. \quad \left\{ \begin{array}{l} \theta_ {1} ^ {\prime \prime} = \pi - \theta_ {2} \\ \theta_ {2} ^ {\prime \prime} = \pi - \theta_ {1} \end{array} \right. \tag {11}
$$

To resolve ambiguity, we rotate the array once more and measure signal phases from an extra direction $\theta _ { 3 } .$ . By performing D-MUSIC for pairs of measurements $( \theta _ { 1 } , \theta _ { 2 } )$ and $( \theta _ { 2 } , \theta _ { 3 } )$ , we get four possible combination of solutions. As in Fig. 3b, denoting the solutions for $\theta _ { 2 }$ in $( \theta _ { 2 } , \theta _ { i } )$ as $\boldsymbol { \theta } _ { 2 : i } ^ { ' }$ and $\theta _ { 2 : i } ^ { ^ { \prime \prime } } ~ ( i = 1 , 3 )$ , only the combination of correct solutions $\boldsymbol { \theta } _ { 2 ; 1 } ^ { \prime }$ and $\boldsymbol { \theta } _ { 2 ; 3 } ^ { ' }$ overlaps. Thus, we can identify the correct AoA by finding the combination of solutions whose estimations of $\theta _ { 2 }$ are most closed.

3) Generalizing to 3-D Scenarios: Since wireless signals propagate in a 3-D space, the actual incident angle consists of an azimuth and an elevation component (Fig. 3c). However, commodity smart devices e.g. smartphones are only equipped with linear antenna arrays. Thus the MUSIC algorithm can only compute the AoA in a plane expanded by the array and transmission (as θ in Fig. 3c). To recover both the azimuth and the elevation component from the AoA estimate θ computed by MUSIC, we utilize the following observation. The AoA estimate θ reported by MUSIC has the following relation with its azimuth (γ) and elevation (τ ):

$$
\cos \theta = \cos \gamma \cos \tau \tag {12}
$$

Following the discussion in Section III-A, the outputs of D-MUSIC for pairs of measurements $( \theta _ { 1 } , \theta _ { 2 } )$ and $( \theta _ { 2 } , \theta _ { 3 } )$ are:

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

![](images/2fcf527acc46bc35dedddd8dd7166a4238f0f54256b2543b5bf13c7e2bdae495.jpg)



Fig. 4. Examples of estimation deviation for different start AoAs.

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

Note that the sign of elevation (τ ) cannot be solved by $D _ { - }$ MUSIC itself. Yet since APs are commonly deployed on the ceiling to achieve larger coverage, the elevation (τ ) tends to be non-negative.

# B. Measuring Rotation Angle

Recall Equation 9, the measurement accuracy of rotation angle Δθ acts as a critical yet controllable factor for accurate D-MUSIC. In this section, we theoretically quantify the impact of rotation angle measurement error on D-MUSIC scheme and describe how to measure rotation angles on mobile devices.

1) Impact of Rotation Angle Error: For the 2-D case, according to Equation 10, we can derive the following relationship between the AoA estimation error $( \mathrm { e r r } _ { \theta _ { 1 } } )$ and the rotation measurement error $( \mathrm { e r r } _ { \Delta \theta } ) \mathrm { : }$

$$
\mathrm{err} _ {\theta_ {1}} = \frac {1}{2} \left(\left| \tan \theta_ {\epsilon} \cot \frac {\Delta \theta}{2} \right| + 1\right) \mathrm{err} _ {\Delta \theta} \tag {16}
$$

where $\begin{array} { r } { \theta _ { \epsilon } = \theta _ { 1 } + \frac { \Delta \theta } { 2 } } \end{array}$ 2 is the AoA of bisector of $\theta _ { 1 }$ and $\theta _ { 2 } .$ . As seen, the AoA estimation accuracy is closely related to two properties of the rotation angle Δθ.

• Direction of the Angular Bisector. The coefficient tan $\theta _ { \epsilon }$ approaches infinity if $\theta _ { \epsilon }$ reaches $9 0 ^ { \circ }$ , thus leading to considerable $\operatorname { e r r } _ { \theta _ { 1 } }$ . Fig. 4 plots theoretical AoA estimation errors for counterclockwise rotation of constant $3 0 ^ { \circ }$ with different start orientations (i.e. different AoA of bisectors $\theta _ { \epsilon } )$ . As can be seen, the closer $\theta _ { \epsilon }$ is to $9 0 ^ { \circ }$ , the larger the AoA estimation error is. However, unacceptable $\operatorname { e r r } _ { \theta _ { 1 } }$ only occurs when $\theta _ { \epsilon }$ is sufficiently close to $9 0 °$ . Once θ slightly deviates from $9 0 ^ { \circ }$ , the coefficient tan $\theta _ { \epsilon }$ as well as the estimation error decreases sharply.

Scale of the Rotation Angle. The coefficient cot $\scriptstyle { \frac { \Delta \theta } { 2 } }$ approaches infinity when $\Delta \theta$ tends to $0 ^ { \circ }$ , thus also leading to unacceptable $\operatorname { e r r } _ { \theta _ { 1 } }$ . Fig. 5 shows the theoretical

![](images/006be616791d12cd3f67f29b20c1a20c9d2e333dc42a1408681f3269ba67d6ee.jpg)



Fig. 5. Examples of estimation deviation for different rotation angles.

AoA estimation errors for counterclockwise rotation of different angles with start orientations towards the transmitter $( i . e . \ \theta _ { 1 } = 9 0 ^ { \circ } )$ . As is shown, the smaller rotation angle Δθ, the larger AoA estimation error. Consequently, we intend to guide users to rotate at a larger scale for better AoA estimation performance.

2) Measurement of Rotation Angle: As depicted by Fig. 4 and Fig. 5, in addition to the two factors discussed above, AoA estimation accuracy is also effected by the rotation measurement error $\operatorname { e r r } \Delta \theta$ .

Generally, the rotation angle can be efficiently measured by inertial sensors built in modern mobile devices. In D-MUSIC, we employ gyroscope to monitor rotation motion. Gyroscope has been widely adopted for device attitude sensing and well demonstrated to be yield sufficiently accurate results. Particularly, although it is difficult to track the absolute phone attitude over a long time, the instantaneous rotation angle can be measured with high precision. For instance, the Euler Axis/Angle method can achieve $9 0 ^ { t h }$ percentile and medium rotation measurement errors of $7 ^ { \circ }$ and $3 ^ { \circ }$ for a one-minute walk [13]. In our situation, if a user holds a phone in hand and rotates it for a period of three seconds, the rotation angle measurement error appears to be less than 0.5◦, which is accurate enough for D-MUSIC.

# C. Dealing with Multipath

Signals propagating indoors suffer from severe multipath effects, which lead to receptive signals from multiple transmission paths superimposing at the receiver. As a result, the superimposed signal phase is deviated from direct-path signal phase, which may decrease estimation accuracy of difference of cosine values in Equation 9 and thus lead to erroneous AoA estimates. In extreme cases with serious multipath, D-MUSIC might fail to yield accurate AoA estimation results.

A natural alternative to enable AoA measurement in multipath scenarios is to exploit the standard MUSIC algorithm on sufficient antenna elements [7]. However, as previously discussed, directly applying standard MUSIC on commodity WiFi infrastructure fails to derive AoA due to unknown phase offsets. Recent innovation Phaser [8] searches through the phase offset space to find the solution with which standard MUSIC generates high-quality pseudospectrum A prerequisite for Phaser to operate is the prior knowledge of precise relative direction between the transmitter and the receiver, which is, however, commonly unavailable in mobile environments and is manually obtained in Phaser. D-MUSIC can complement Phaser as an automatic phase calibration by feeding its outputs as ground-truth AoA for Phaser. Specifically, to calibrate phase offsets of a mobile device, we let a user stays around an AP and rotates the device to estimate the relative direction towards the AP. Given that the line-of-sight signal dominates the overall multipath signals in the surrounding areas of an AP, D-MUSIC can output sufficiently precise results to tune the phase offsets. And by doing this, Phaser is enabled to work without elaborate manual measurement of ground truth. Note that the uncertain phase offset remains unchanged after each time the device powers up. Thus it is unnecessary to perform D-MUSIC and Phaser every time, as long as the phase offset can be calibrated at the beginning.

![](images/758f35d2b85f785403770b2f678d30b81dd1b9aafecc385f128534b343ea4525.jpg)



(a) Experiment building (testing areas are highlighted)

![](images/b94314aee7589f2fe38328bc76fcda9cf9686fec34399d1786ff4cd576e88db7.jpg)



(b) The linear array with pad

![](images/f099c7153394c5c5e7094f81fb3035ec34bf1acfefcd150050c448556169c7cd.jpg)



(c) The inside of Mini PC   
Fig. 6. Experiment settings

In a nutshell, by feeding D-MUSIC into Phaser, we can automatically correct the phase offsets on both fixed devices and mobile devices. By doing this, we enable the standard MUSIC algorithm and its primary variations to accurately calculate AoA even in multipath-dense scenarios.

# IV. EXPERIMENTS AND EVALUATION

# A. Experiment Methodology

Experiment Setup: We conduct experiments in an academic buildings with rooms furnished for different use, as in Fig. 6a. Concretely, we collected data in various scenarios including two classrooms, two laboratory rooms and one meeting room. The laboratory rooms are furnished with cubicle desks, computers, wireless mesh nodes and other plastic and metallic furniture. The classrooms are equipped with a metal platform and more desks and chairs. The meeting room is the smallest room with a big rectangular table placed in the center and several chairs around.

Data Collection: Two types of data, CSI and gyroscope readings, are collected in the experiments. For CSI, we use two mini-desktops (physical size 170mm×170mm) with three external antennas as AP and client. Both mini-desktops are equipped with Intel 5300 NIC and run Ubuntu 14.04 OS (Fig. 6c), and are set up to inject in monitor mode [14] on Channel 157 at 5.785GHz. The AP is set to send signals via one antenna. The client’s antennas are spaced at a halfwavelength distance (2.59cm) in a linear form to simulate the antenna array in commodity wireless devices. For gyroscope readings, we use a Google Nexus 7 pad to record inertial sensor data. To acquire a mobile device with three or more antennas and enable it to support CSI measurements, we assemble a receiver by attaching the client antenna array and the pad on a plastic turntable, as shown in Fig. 6b, which can simultaneously measure CSI and sensor readings. The equipment is by default placed 1.3m high, which is the height where people can naturally use their phones.

We collect data in group. For each group of measurements, we place the array with AoA of 0◦, and rotate the turntable with an interval of 15◦, until AoA of 180◦. By doing this, we measure the 13 groups of CSIs at 13 orientations during the rotation and record traces of gyroscope readings. To extensively evaluate the performance of D-MUSIC, we perform measurements with different environment settings, i.e. diverse Tx-Rx distances including 2m, 3m and 4m, different Tx height from 0m to 2m (relative to the client) and different spots with various multipath conditions. For each setting, we conduct 3 groups of measurements. The rotation angles derived from gyroscope readings are marked as ground-truths of corresponding AoAs since we start from an AoA of 0◦ for each measurement.

# B. Performance

We first report the overall performance of D-MUSIC and then evaluate impacts of different factors. In this part of experiment, AoA is directly calculated using D-MUSIC.

1) Overall Performance: To quantitatively evaluate the overall performance of D-MUSIC, we compare D-MUSIC with both Phaser and standard MUSIC without phase calibration. Due to the asymmetric physical geometry of the array, information from the linear array becomes unreliable as AoA θ reaches margins (i.e. 0◦ and 180◦) [1]. Thus, we use data recorded with AoA ranging from 15◦ to 165◦ to fairly compare the methods. In addition, we only consider cases with rotation angle no less than 45◦, where D-MUSIC is generally expected to yield better results according to the impact analysis of scale of rotation angle in Section IV-B3.

As illustrated in Fig. 7, D-MUSIC achieves average estimation error of 13◦. Phaser slightly outperforms D-MUSIC, due to the prior knowledge of precise Tx-Rx direction. The jitter of CDF curve of Phaser demonstrates the unbalanced performance of Phaser. Specifically, the AoA estimation tends to be more accurate when the signal arrives around the Tx-Rx direction used for calibration. Oppositely, the AoA estimation apparently degrades when the received signal deviates from the calibration direction. In contrast, D-MUSIC performs stably across all tested AoAs, due to accurate measurement of rotation angles. Without phase calibration, standard MUSIC yields a large percentage of estimation error. Concretely, more than 20% cases have estimation error beyond $6 0 ^ { \circ }$ . It means standard MUSIC fails to work with unknown phase offsets.

![](images/2888975dd98e432a2a7dddbb128b4e74057e1adb3213af2904d67ba4a3d73314.jpg)



Fig. 7. Overall performance comparisons

![](images/69705439106727762103e8dd30d7ea27acc379bf184bc3c93e9f058c6f1551f2.jpg)



Fig. 8. Impact of different Tx-Rx distance

![](images/ccbf17459b961f9645b501fad34fa2945a223f3826c5b9ce54178a7ba3f07ae6.jpg)



Fig. 9. Impact of different rotation angle

![](images/8562738a50072f50fbd790ecc6ae92127c8175de0823f9b47c1dac5d82e57996.jpg)



Fig. 10. Impact of different orientations

![](images/7063f64bc1fb32d21aee8fa35ecc43b15c7a6eec19487e0528231205bd9c600e.jpg)



Fig. 11. Impact of different Tx-Rx height difference

![](images/13a4dcef5d2f4e04c683912639fcf24f6cd3070777644122d6af98f8d0e22ed6.jpg)



Fig. 12. Impact of different scenarios

In the following, we evaluate the impacts of various factors on performance of D-MUSIC.

2) Impact of Tx-Rx distance: The Tx-Rx distance acts as the most critical factor for D-MUSIC, since it decides the work range of the method. We test Tx-Rx distances including 2m, 3m and 4m. As shown in Fig. 8, D-MUSIC consistently achieves accurate AoA estimation with different Tx-Rx distances. However, the performance of D-MUSIC slightly drops down as the distance increases. It is because that large Tx-Rx distance may lead to complex multipath condition for the link, e.g. increasing number of multipath, decreasing of power of direct-path signal relative to overall signal, etc.   
3) Impact of rotation angle: As discussed in Section III-B1, the quantity of rotation angle impacts estimation error by contributing a coefficient term cot $\frac { \Delta \theta } { 2 }$ to scale up the error. To validate the discussion, we test different rotation angles from 15◦ (resolution of rotation) to $7 5 ^ { \circ }$ (maximum rotation angle available). To get rid of impacts of other factors, we fix the second measured AoA to 90◦, and vary the rotation angle between each successive two measurement only.

Fig. 9 shows the distribution of AoA estimation error for different rotation angles. The AoA estimation error is significantly large when the rotation angle is small. For cases of 15◦ and 30◦, the error of the worst case reaches beyond 60◦, meaning that D-MUSIC is no longer usable. As the rotation angle increases, the estimation error quickly diminishes. For cases that rotation angle exceeds 45◦, the average estimation error is less than $1 0 ^ { \circ } .$ , which is sufficient for practical use.

It is worthwhile to note that small rotation angle is not the only factor that degrades the the performance of D-MUSIC. For AoAs spaced with small rotation angle, the corresponding CSI measurements are similar. Thus, the difference of cosine values derived from CSI measurements is relatively small . As a result, CSI measurement noise may contribute more to final result, and further degrades the performance of the method.

4) Impact of orientation: The other factor amplifying C-SI measurement noise is the array orientation. Due to the asymmetric physical geometry of the array, the quality of CSI measurements significantly degrades as array becomes parallel with incident signal. Thus, the estimation accuracy degrades accordingly. We evaluate the performance of D-MUSIC for estimating different AoAs in Fig. 10. Concretely, we fix the rotation angle to 45◦, and vary (the second) AoAs from $6 0 ^ { \circ }$ to 120◦. As is shown, when AoA deviates from 90◦, estimation error statistically increases. The result is consistent with standard MUSIC, which demonstrates the potential deficiency of linear array.   
Note that the bisector also changes with different AoAs. However, since D-MUSIC requires successive two rotations of the array, it is not easy to control two bisectors to simultaneously change towards or away from $9 0 ^ { \circ }$ while fixing the rotation angle. Meanwhile, the impact of coefficient term tan θ is not severe when two AoAs are not strictly symmetrical about θ = 90◦. Thus, we omit the discussion on impacts of different AoA bisectors.   
5) Impact of height: Theoretically, D-MUSIC extends the work range of linear array to a new dimension. Namely, it enables linear array to estimate both azimuth and elevation components of AoA. To evaluate the performance of D-MUSIC in 3-D space, we test relative height difference between AP and client from 0m to 2m. The AP and client are placed at a distance of 4m, which is a common setting in

indoor environment.

As shown in Fig. 11, the azimuth error statistically increases as the AP lifts up. The degradation of estimation accuracy with increasing height difference has the same reason as that of decreasing rotation angle (Section IV-B3). Recall that the output of differential MUSIC in 3-D space is (cos γ2 − cos γ1) cos τ , where $\gamma _ { 1 }$ and $\gamma _ { 2 }$ are azimuth components and τ is elevation component. As relative height difference (i.e. elevation τ ) increases, difference of CSI measurements of AoAs tends to be smaller, which leads to relatively large CSI measurement noise, and thus degrades the estimation accuracy. When the relative height difference is less than or equal to 1.5m, the average estimation error is below 15◦, which is acceptable for a 3-antenna array. However, when the relative height difference reaches 2m, the performance of D-MUSIC dramatically degrades, with average estimation error greater than 25◦. The main reason that D-MUSIC fails when relative height difference reaches 2m is the environment constraint. Specifically, the floor height of our laboratory building is 3m. To evaluate the height difference of 2m, we have to place the client array near the ground while the transmit antenna near the ceiling. As a result, the multipath condition is aggravated comparing to other height difference cases and the performance of D-MUSIC is thus degraded. However, since the relative height difference is commonly no more than 1.5m, D-MUSIC is applicable to most indoor scenarios.

Comparing with azimuth estimation, elevation estimation is more sensitive to the quality of CSI measurements. The estimation errors in the worst cases even reach 15◦, while the ground-truth are just within 30◦. The considerable errors are potentially caused by inaccurate CSI measurements and small range of elevation components. Fortunately, azimuth components plays a more important role than elevation components in practice. It is sufficient to use azimuth components only in most scenarios such as indoor localization.

6) Impact of multipath: We further test the robustness of D-MUSIC under various multipath conditions. Concretely, we evaluate the performance of D-MUSIC in three different types of rooms, classroom, laboratory and meeting room. In each room, the AP and client are placed at the same height of 1.3m and at a distance of 3m. In classroom, the devices are placed along the passageway between desks, where the desks are lower than the devices. In laboratory, the devices are placed along the passageway between the wall and the cubicle desks, where the wall, the desks and other electronic devices (e.g. mesh nodes) surrounding the link are higher than the devices. In meeting room, due to the space limitation, the AP and client are placed separately against the opposites walls in the eastwest direction. The conference table is placed between the devices, at the height of about 0.3m lower.

Fig. 12 shows the performance of D-MUSIC in different environments. In the classroom where the least multipath exists, D-MUSIC achieves the best performance with average estimation error of $3 ^ { \circ }$ . In the laboratory, due to reflection signals from surroundings, the performance of D-MUSIC degrades to average error of $7 ^ { \circ }$ . In the meeting room where the wall and the table generates strong reflection signals, D-MUSIC only achieves an average estimation error of 16◦. In general, the more complex multipath conditions, the worse precision D-MUSIC yields.

![](images/259744527ba3f2e28679d5932b6223732e482a24caf57fa9e49e01d7f1162602.jpg)



Fig. 13. Comparisons of phase offset estimation error

# C. Performance in Phase Calibration

As stated in Section III-C, D-MUSIC can be integrated with Phaser to calibrate unknown phase offsets of array elements, eliminating the needs of manually acquired prior knowledge. By doing this, it is also possible to moderately avoid the impacts of multipath by performing standard MUSIC on array with enough number of antennas. We conduct a benchmark experiment to show the capability of phase calibration of D-MUSIC. AoA reported by D-MUSIC, in comparison with ground-truth AoA, is used in Phaser to perform phase calibration. Concretely, we place the AP and client at a distance of 2m and at the same height of 1.3m in the classroom. And we employ the ground-truth angle and AoA estimated by D-MUSIC as the relative Tx-Rx direction input of Phaser, respectively. The ground-truth of phase offset is measured by splitting a reference signal and routing it to multiple receiving radio chains with a 5GHz splitter.

As in Fig. 13, by using ground-truth, Phaser achieves average estimation error of 15◦. While with AoA estimation by D-MUSIC for calibration, Phaser achieves average estimation error of 19◦. The accuracies are comparable, demonstrating the capability of D-MUSIC for accurate phase calibration.

# V. RELATED WORK

Related works roughly fall into following categories.

Measuring AoA via Phased Array. AoA has been widely applied as a signal feature in localization [15], [16], wireless coverage confining [5] and location-based wireless security [4]. A primary functionality of these applications is to measure AoA via phased antenna arrays [17]. Wong et al. [18] explores standard phase array processing to obtain AoA, yet fails to develop a practical localization scheme. ArrayTrack [1] improves AoA with spatial smoothing and spectra grouping to suppress multipath effect to achieve sub-meter localization accuracy with a rectangular array of 16 antennas on dedicated software-defined radio platforms. To enable accurate AoA measurements, it is important to calibrate for unknown phase offset. Our work is motivated by the increasing popularity of AoA-based applications and strives to enable accurate

AoA measurement as well as provide a light-weight phase calibration scheme on commodity WiFi infrastructure.

Inertial Sensor Auxiliaries. The inertial sensors on modern smart devices bring in an orthogonal dimension for AoA estimation by providing various mobility information [19]. Ubicarse [9] calculates accurate displacement of SAR using gyroscope and active drift compensation algorithm based on mapping of AoA profile. CUPID [20] utilizes compass and accelerometer to compute human moving distance, and further identifies angle of the direct path using geometric constraints. Our work also harnesses mobility information to assist AoA estimation and is complementary to these works. Unlike Ubicarse [9] where relative channel between antennas measured at the same time is calculated to generate “translationresilient” SAR, our scheme compute relative channel between the two measurements from the same antenna at two different orientations to perform Differential MUSIC. Also, Ubicarse needs high-resolution sensors to record a relatively long trace during device motion. Conversely, our scheme only requires gyroscope readings within one rotation, which thus dramatically avoids the accumulative errors of inertial sensors in the long-run. The rotation operation is also more natural and convenient than CUPID [20] where users are required to walk for a few steps.

Phase Calibration. Phase calibration is crucial for wireless communications and mobile computing applications. Argos [21] performs phase calibration by sending from one antenna on the WARP FPGA-based AP while receiving on the others. Yet this approach is inapplicable on current halfduplex COTS wireless devices, where they cannot transmit and receive on different antennas simultaneously. Another approach is to utilize an extra reference. Chen et al. [22] exploit a short reference signal sent from an additional reference transmitter at a known location to eliminate phase offsets of COTS wireless devices. Phaser [8] computes AoA spectrum of signal sent from reference transmitter, and estimates the unknown phase offsets which lead to maximum likelihood AoA spectrum. One drawback of these calibration schemes is that they require the absolute position of reference transmitter a prior that is only possible to be precisely acquired by manual measurement, and need re-calibration for every new wireless network. Conversely, our work utilizes inertial sensors on smart devices to eliminate the need for reference transmitters, enabling phase calibration on COTS wireless devices.

# VI. CONCLUSION

In this paper, we propose D-MUSIC, a relative form of standard MUSIC algorithms that enables accurate AoA estimation on commodity WiFi devices. We leverage users’ natural behaviour of rotation to formulate a virtual spatial-temporal antenna array and a corresponding relative incident signal. The incident angle of the relative signal is derived by standard AoA estimation algorithm, and meanwhile captured by inertial sensors as the rotation angle. Furthermore, we fortify D-MUSIC for multipath-rich scenarios by employing its outputs as an auto phase calibration for standard MUSIC algorithm. Extensive experimental results have validated the feasibility of D-MUSIC, with an average error of $1 3 ^ { \circ }$ . Requiring no hardware modifications or cumbersome calibration, D-MUSIC is envisioned as an early step towards a practical scheme for AoA estimation on COTS mobile devices. Future works include further enhancing D-MUSIC in rich multipath conditions and applying D-MUSIC for accurate indoor localization.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC under grant 61522110, NSFC Major Program 61190110, NSFC under grant 61361166009, 61303209, 61572366.

# REFERENCES

[1] J. Xiong and K. Jamieson, “Arraytrack: A fine-grained indoor location system.” in Proc. of USENIX NSDI, 2013.   
[2] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller, “3d tracking via body radio reflections,” in Proc. of USENIX NSDI, 2014.   
[3] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proc. of ACM MobiCom, 2013.   
[4] J. Xiong and K. Jamieson, “Secureangle: improving wireless security using angle-of-arrival information,” in Proc. of ACM HotNets, 2010.   
[5] A. Sheth, S. Seshan, and D. Wetherall, “Geo-fencing: Confining wi-fi coverage to physical boundaries,” in Proc. of Springer Pervasive, 2009.   
[6] Z. Sun, A. Purohit, R. Bose, and P. Zhang, “Spartacus: spatially-aware interaction for mobile devices through energy-efficient audio sensing,” in Proc. of ACM MobiSys, 2013.   
[7] R. O. Schmidt, “Multiple emitter location and signal parameter estimation,” IEEE Transactions on Antennas and Propagation, vol. 34, no. 3, pp. 276–280, 1986.   
[8] J. Gjengset, J. Xiong, G. McPhillips, and K. Jamieson, “Phaser: enabling phased array signal processing on commodity wifi access points,” in Proc. of ACM MobiCom, 2014.   
[9] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proc. of ACM MobiCom, 2014.   
[10] Z. Yang, Z. Zhou, and Y. Liu, “From rssi to csi: Indoor localization via channel response,” ACM Computing Surveys (CSUR), vol. 46, no. 2, p. 25, 2013.   
[11] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 packet delivery from wireless channel measurements,” in Proc. of ACM SIGCOMM, 2010.   
[12] J. Choi, Optimal combining and detection: statistical signal processing for communications. Cambridge University Press, 2010.   
[13] P. Zhou, M. Li, and G. Shen, “Use it free: Instantly knowing your phone attitude,” in Proceedings of the 20th annual international conference on Mobile computing and networking, 2014.   
[14] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Tool release: Gathering 802.11 n traces with channel state information,” ACM SIGCOMM Computer Communication Review, vol. 41, no. 1, pp. 53–53, 2011.   
[15] D. Niculescu and B. Nath, “Vor base stations for indoor 802.11 positioning,” in Proc. of ACM MobiCom, 2004.   
[16] Y. Xie, Z. Li, and M. Li, “Precise power delay profiling with commodity wifi,” in Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, 2015.   
[17] D. Inserra and A. M. Tonello, “A frequency-domain los angle-ofarrival estimation approach in multipath channels,” IEEE Transactions on Vehicular Technology, vol. 62, no. 6, pp. 2812–2818, 2013.   
[18] C. Wong, R. Klukas, and G. Messier, “Using wlan infrastructure for angle-of-arrival indoor user location,” in Proc. of IEEE VTC, 2008.   
[19] Z. Yang, C. Wu, Z. Zhou, X. Zhang, X. Wang, and Y. Liu, “Mobility increases localizability: a survey on wireless indoor localization using inertial sensors,” ACM Computing Surveys, vol. 47, no. 3, p. 54, 2015.   
[20] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Avoiding multipath to revive inbuilding wifi localization,” in Proc. of ACM MobiSys, 2013.   
[21] C. Shepard, H. Yu, N. Anand, E. Li, T. Marzetta, R. Yang, and L. Zhong, “Argos: Practical many-antenna base stations,” in Proc. of ACM MobiCom, 2012.   
[22] H.-C. Chen, T.-H. Lin, H. Kung, C.-K. Lin, and Y. Gwon, “Determining rf angle of arrival using cots antenna arrays: a field evaluation,” in Proc. of IEEE MILCOM, 2012.