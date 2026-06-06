# Orientation-aware RFID Tracking with tation-aware RFID Trackin

Chengkun Jiang, Yuan He, Xiaolong Zheng, Yunhao Liu

School of Software, Tsinghua University

jck15@mails.tsinghua.edu.cn,{heyuan,zhengxiaolong,yunhao}@tsinghua.edu.cn

# ABSTRACT

RFID tracking attracts a lot of research efforts in recent years. Most of the existing approaches, however, adopt an orientation-oblivious model. When tracking a target whose orientation changes, those approaches suffer from serious accuracy degradation. In order to achieve target tracking with pervasive applicability in various scenarios, we in this paper propose OmniTrack, an orientation-aware RFID tracking approach. Our study discovers the linear relationship between the tag orientation and the phase change of the backscattered signals. Based on this finding, we propose an orientation-aware phase model to explicitly quantify the respective impact of the read-tag distance and the tag’s orientation. OmniTrack addresses practical challenges in tracking the location and orientation of a mobile tag. Our experimental results demonstrate that OmniTrack achieves centimeterlevel location accuracy and has significant advantages in tracking targets with varing orientations, compared to the state-of-the-art approaches.

# KEYWORDS

RFID; Tracking; Orientation; Polarization

# ACM Reference format:

Chengkun Jiang, Yuan He, Xiaolong Zheng, Yunhao Liu. 2018. Orientation-aware RFID Tracking with Centimeter-level Accuracy. In Proceedings of The International Conference on Information Processing in Sensor Networks, Porto, Portugal, April 11–13 2018 (IPSN’18), 12 pages.

DOI:

# 1 INTRODUCTION

Location is indispensable information in modern industry. Target tracking, namely, to continuously determine the location of a mobile target, has great significance and therefore attracts a lot of research efforts in the area of industrial cyber-physical systems (CPS) [2, 15, 21, 24]. Radio Frequency IDentification (RFID) has been widely applied in industrial scenarios [3, 11]. Due to its low cost, ease of deployment, and high efficiency in terms of information

![](images/8194f14f172f68217b5e1958b559fc50cc1d13ca769eb9d0b153b14ebf05d41d.jpg)

![](images/41de74376330a360ca1f78eac3bd788ae839c2221a30a4e7348f3da532b5417a.jpg)

![](images/ba3776094a51343f5e59d92a3501cb038fbccdac4504d0c93638d9c13d6635b0.jpg)

![](images/7c15bb125cc6c202a0cc0ee15ec2c5bd7efa5f6500cb73029d457eadef0cb341.jpg)  
Figure 1: Industrial production lines.

gathering, RFID is deemed as a promising solution for target tracking [13, 17, 25].

Early works on RFID-based localization and tracking rely on the received signal strength (RSS) to calculate the distance between a reader and a tag or construct a RSS map for fingerprinting. Since RSS is susceptible to environmental dynamics and external signals, the accuracy of those approaches is limited. Recently, researchers propose to exploit signal phase information for RFID tracking. Compared to RSS, the phase change between the transmitted and the backscattered signals is more reliable as an indicator of the reader-tag distance. BackPos in [8] localizes a tag according to the finding that the difference of the phases received by two antennas of a reader corresponds to the difference of the distances from the tag to the two antennas. Assuming that the phase change is solely determined by the reader-tag distance, Tagoram [25] and MobiTagbot [13] exploit the holography to estimate the probability that a tag is located at a certain location.

The phase change, however, is jointly determined by both the reader-tag distance and the tag’s orientation. Most of the existing approaches adopt an orientation-oblivious model that neglects the non-trivial impact of orientation on the phase change. The tracking accuracy will degrade when the tag’s orientation changes while moving. A few works address the problem of orientation change [20], but they cannot be applied to the scenarios where the location and the orientation simultaneously change. There are many such scenarios in industrial applications, as shown in Fig. 1. For example on a medicine bottling line and a soda production line, the bottles move along the lines with continuous self-rotation. Other production lines make operations to the moving targets, such as labeling or spray painting, which not only require the information of orientation, but also change the orientation of the targets. Directly using an orientation-oblivious model will be error-prone, not to mention the inability to calculate the orientation. In such scenarios, orientation-aware tracking has practical significance, but remains an open problem.

To tackle the above problem, we may meet the following challenges. First, though we know that the backscattered signals from a RFID tag is anisotropic, the relationship between the phase and the orientation is still unclear. Blurring the impact of orientation on the signal phase inevitably introduces errors in tracking a tag. Second, the tag’s orientation and the reader-tag distance jointly affect the phase of the received signal at the reader. A group of phase measurements often correspond to a number of possible location-orientation combinations. Without an effective solution to cope with such ambiguity, the tracking process cannot converge to a unique result.

In this paper, we propose OmniTrack, an orientationaware tracking approach that applies to commercial off-theshelf (COTS) RFID systems.

• By exploiting the phenomenon of tag polarization, we conduct real-world observation and discover the linear relationship between the phase change of the signal and the tag’s orientation. Based on this finding, we propose an orientation-aware model to explicitly quantify the respective impact of the readertag distance and the tag orientation on the phase change.   
• We propose a light-weight and accurate tracking approach called OmniTrack. To the best of our knowledge, OmniTrack is the first approach that can pinpoint tag’s location and orientation simultaneously. OmniTrack also deals with practical challenges in initializing, updating, and calibrating the location and orientation of a mobile tag.   
• We implement OmniTrack on a COTS RFID platform. The experimental results demonstrate that OmniTrack achieves centimeter-level location accuracy and has significant advantages in tracking targets with varing orientations, compared to the state-of-the-art approaches.

The remainder of the paper is structured as follows. We discuss the related works in Section 2. Section 3 shows the limitation of the existing phase model and presents the orientation-aware phase model. In Section 4 we elaborate on the design of OmniTrack. Section 5 discusses important issues concerning the applicability and the extensibility of OmniTrack in practice. Section 6 presents the implementation details and the evaluation results. Section 7 concludes the paper.

# 2 RELATED WORKS

This section reviews the state of the arts in RFID localization, tracking, and rotation detection. At the end of this section, we briefly discuss how our work differs from the existing works.

RFID Localization and Tracking: Early proposals on RFID localization and tracking generally exploit RSS for location inference. Depending on the specific technique, the existing works can be classified into two categories: RSSbased ranging [1, 6] and fingerprinting [10]. Since RSS is susceptible to environmental dynamics and external signals, ranging based on those environment-dependent propagation models are generally inaccurate. The accuracy of fingerprintbased approaches, however, is constrained by the granularity of site survey or the density of deployed tags.

In recent years the research focus moves onto phase-based localization and tracking. The phase change between the transmitted and the backscattered signals can be an approximate indicator of the reader-tag distance. Liu et al. [8] directly uses such a phase model to estimate the distance differences from the tag to multiple antennas. And then a hyperbolic positioning method is exploited to localize a tag. In [5, 27], multi-frequency approaches are used to obtain more accurate ranging data for localization.

Phase change introduced by a backscattering tag is a nonnegligible factor in phase-based localization and tracking [26]. Under this circumstances, the holographic approaches are proposed and achieve so far the best accuracy. Miesen et al. [9] introduce a holographic scheme to localize a tag with phase values sampled from a synthetic aperture on the RFID reader. Parr et al. [12] exploit tag mobility and adopt Inverse Synthetic Apertures Radar (ISAR) to generate holograms for tag localization and tracking. Tagoram [25] proposes Differential Augmented Hologram (DAH) to track the tag accurately. MobiTagbot in [13] improves the holographic approach with channel hopping to suppress the multi-path effect. Angle of Arrival (AoA) is another metric proposed for localization and tracking [7, 19, 23], which can be derived from the phase difference at different antennas,

RFID Rotation Detection: There are works based on RFID system for orientation or rotation detection. RF-compass [18] uses a 2D-plane partitioning method to navigate a robot to gradually converge to the object’s orientation, but it cannot directly track the object’s orientation. The works in in [4, 16] deploy dense RFID tags to cover the site of interest and then detect position and orientation of the target with a reader installed on it. They need complex and burdensome preparation before tracking, which limits the practical applicability. PolarDraw [14] leverages electromagnetic polarization to identify tag movement, by utilizing information like phase change and RSS. Tagyro [20] proposes a 3D rotation detection system that exploits the phase difference.

![](images/92a5617a062bf0b610e4ece288f0a9859a576d8bfdaba80231b5707307e3a459.jpg)



Figure 2: A typical passive RFID system.

![](images/00e9814493af62cad1e6b45cd7d9bda6755776ea1b264ac27be65be8fd88c544.jpg)



Figure 3: Tag’s Rotation

![](images/22ea8e922e421d43b0ca3cfee532ac6bcf3ee4005858392c5577fd2dfe56c97c.jpg)



Figure 4: The impact of tag’s orientation

It requires two sets of tags attached to the target and two readers for rotation detection. They realize 3D rotation detection, however, under the assumption that the position of the target is fixed.

As we exemplify before, tracking targets with the varing orientation is a frequent task in practical production lines. Neglecting the impact of the varing orientation will cause the loss of tracking accuracy. Most of the existing works overlook this problem or tolerate the orientation-induced errors by employing certain probabilistic methods [9, 12, 25]. As for the orientation tracking approaches, most of them consider the orientation change while assuming a fixed location. Our work for the first time explicitly addresses the above problem and innovates RFID tracking with orientationawareness. OmniTrack can simultaneously pinpoint the location and the orientation. Compared to the existing works, OmniTrack has significant advantages in tracking targets with varing orientations.

# 3 ON THE ORIENTATION-AWARENESS OF THE PHASE MODEL

This section first introduces the model adopted by the existing approaches and discusses its limitation. Then we introduce the concept of tag polarization and present the observations on the relationship between tag orientation and the phase change during backscatter communication. Based on the observations, we propose the orientation-aware phase model.

# 3.1 Limitations of the Orientation-oblivious Model

Fig. 2 shows a typical signal propagation process between a reader and a tag. The phase change is defined as the modulo difference between the phases of transmitted signal and received signal at the reader. We use ϕ to denote the phase change. The general phase model adopted by the existing work is shown below:

$$
\left\{ \begin{array}{l} \phi = \left(\frac {2 \pi}{\lambda} \times 2 d + \delta\right) \mod 2 \pi \\ \delta = \phi_ {T x} + \phi_ {R x} + \phi_ {T a g} \end{array} \right. \tag {1}
$$

where d is the reader-tag distance. $\phi _ { T x } , \phi _ { R x }$ , and $\phi _ { T a g }$ are the phase changes introduced by the reader’s transmitter, the tag, and the reader’s receiver circuit. λ is the wave length of the signal. $\phi _ { T x }$ and $\phi _ { R x }$ are the constants that are only related to the hardware circuits. In this model, $\phi _ { T a g }$ is commonly treated as a constant or the random noise. However, we find it violates our empirical results. We rotate the tag for one cycle while fixing its distance to the antenna and the phase change can achieve up to 2π as shown in Fig. 4.

Therefore, the localization or tracking methods based on this phase model can be inaccurate when there exists tag’s rotation.

# 3.2 Observations

The phenomenon Section 3.1 discusses is actually caused by the antenna polarization. The polarization of an antenna refers to the change of the signal’s electric field produced by the antenna. Generally, the antenna of a COTS passive tag is linear-polarized,, which means the direction of the electric field (polarized direction) is the same as the direction of the tag’s body (Y axis in Fig. 3). When the tag rotates as shown in Fig. 3, the tag’s polarized direction will change relatively to the received RF waves, thus leading to the changes in the measured phase.

We observe from the Fig. 4 that the measured phase linearly changes with the angle of rotation under some certain conditions. So if we can ensure the linear relation during the process of tracking, It is possible to find a way to remove the influence of the polarization and detect the tag orientation. As shown in Fig. 3, We define the X axis is the line perpendicular to the antenna plane and the X-Y plane is parallel to the ground. Z axis is perpendicular to the X-Y plane.

Observation: The measured phase will change linearly with the angle between the polarized direction of the tag and the antenna-to-tag direction.

If the angle between the tag’s rotation plane and the reader’s antennas is fixed, we will always obtain the abovementioned relation. As shown in Fig. 3, if the tag rotates by Z axis, we always have a linear relation no matter the tag’s surface is pointed to the X axis or the Z axis. According to this observation, in industrial production lines, we may just attach a tag at the top of or the side of a target. Then we will see the linear phase change when the target rotates in the 2D space. Fig. 4 shows the phase changes we measure in such a scenario. The results reveal that the phase will change for 2π if we rotate the tag for 360◦.

![](images/335327dba95947c929d4d9a1e3f3f93166959b4e4facdb139d78f2089023caf5.jpg)



Figure 5: The Overview of OmniTrack

# 3.3 The Orientation-aware Phase Model

According to our observations, we propose an orientationaware phase model that takes both the distance and the orientation into consideration. The phase change $\phi$ received by the reader is defined below:

$$
\left\{ \begin{array}{l} \phi = \left(\frac {2 \pi}{\lambda} \times 2 d + k \times \theta + c\right) \mod 2 \pi \\ c = \phi_ {T x} + \phi_ {R x} + \phi_ {T a g} \end{array} \right. \tag {2}
$$

In this phase model, we take into account the angle θ between the tag polarized direction and the tag-to-antenna direction. Through the empirical studies conducted in Section 3.2, we concluded that the phase changes linearly with the angle θ and the changing rate k is $2 \ \mathrm { o r } \ - 2$ according to the rotation direction and the circular polarized antenna. $\phi _ { T x } , \phi _ { R x }$ and $\phi _ { T a g }$ are all constants here. They are the phase changes caused by the transmitter circuits, the receiver circuits and tag’s hardware. Here, we use the constant term c to denote the sum of their impact on the phase change.

In typical 2D scenarios, we can exploit the model to track the orientation change of the target at a fixed position if we attach a tag at the surface of the target. We can derive the orientation change based on this model when we obtain the phase change, However, tracking a target with both rotation and movement is not an easy task. Therefore, we propose our tracking system to realize the tracking of targets with varing orientations, which provides us with both location and orientation.

# 4 DESIGN

The design of OmniTrack must meet the following goals: (1) Both the location and the orientation must be accurately calculated and keep updated throughout the tracking process. (2) Initialization of a tag’s location and orientation must be accurate and efficient, in order to ensure the overall tracking accuracy and efficiency. (3) Errors cumulated during the tracking process are inevitable, but must be well controlled and calibrated in time.

OmniTrack consists of three main components. As shown in Fig. 5, the core of OmniTrack is an orientation-aware $U p \cdot$ dating Component that iteratively updates the tag’s location and orientation according to the consecutive measurements of phases at the reader antennas. The Initialization Component provides the initial location and orientation of the tag by using techniques like channel hopping and phase pattern matching. The Calibration Component deals with the error accumulation while tracking.

# 4.1 Orientation-aware Tracking

With OmniTrack, we have an RFID reader with two antennas, which provide consecutive phase readings of the target tag for the updating module. Tracking with OmniTrack is a continuous process, in which the tag’s location and orientation is periodically updated according to the consecutive phase readings. The updating frequency depends on the sampling rate of the reader, typical at 30-50Hz. For ease of illustration, we present the algorithm as the antennas are located at the same plane of tag rotation. In practice, OmniTrack works as long as the perpendicular distance from the antennas to the tag rotation plane is known. The moving distance of a tag can be calculated using our algorithm, according to the geometric relation.

The detailed updating process runs as follows. As illustrated in Fig. $^ { 6 , }$ suppose we have phase readings from antennas $A _ { 1 }$ and $A _ { 2 }$ at time $t _ { i }$ and $t _ { i + 1 }$ . We denote the corresponding phase readings by $\phi _ { p , q }$ , where $\boldsymbol { p }$ is the antenna index and q is the time index. The expressions of the phases at time $t _ { i }$ and $t _ { i + 1 }$ are shown below according to Eq. (2):

$$
\left\{ \begin{array}{l} \phi_ {p, i} = (\frac {2 \pi}{\lambda} \times 2 d _ {p, i} + k \times \theta_ {p, i} + c _ {p}) \mod 2 \pi \\ \phi_ {p, i + 1} = (\frac {2 \pi}{\lambda} \times 2 d _ {p, i + 1} + k \times \theta_ {p, i + 1} + c _ {p}) \mod 2 \pi \end{array} \right. \tag {3}
$$

$d _ { p , q }$ denotes the distance between the antenna p $( p = 1 , 2 )$ and the tag at time $t _ { q } . ~ \theta _ { p , q }$ denotes the relative angle between the the tag’s polarized direction and the antenna-tag direction. $c _ { p }$ is the constant phase offset depending on the respective antenna and the tag.

Suppose the tag’s location and orientation at $t _ { i }$ (namely $d _ { 1 , i } , d _ { 2 , i } , \theta _ { 1 , i } , \theta _ { 2 , i } )$ are known, the task of the tracking component is to calculate $d _ { 1 , i + 1 } , d _ { 2 , i + 1 } , \theta _ { 1 , i + 1 }$ , and $\theta _ { 2 , i + 1 }$ . Note that there are only two constraints in Eq. (3) corresponding to the two antennas. Solving Eq. (3) does not yield a unique solution. We need to exploit additional geometric relationship to determine the tag’s location and orientation.

![](images/0b3f377ec840f18afa8f9ae67901a1cb73cf9fcb2546e3e8e9940e894f8bd673.jpg)



Figure 6: Tag’s Movement

![](images/ee91481c944a8c7007df1ce371378b71c01403525f50a402b2d16d57049a6e93.jpg)



Figure 7: Tracking the tag

![](images/fd394e8188857b0e8f6611e1fd6d530f5dd5ca937736410ccb76352ffcfd02fc.jpg)



Figure 8: Initial position estimation

Now we look into the movement of a tag in a time slot. Suppose we rotate a tag for Δθ at a fixed position, the angle between the tag’s polarized direction and the antenna-tag direction also rotates for the same Δθ . Note that the phase readings are samples for tens of times every second, we may assume that the movement of a tag in one time slot doesn’t affect the angle between the tag’s polarized direction and the antenna-tag direction. The change of the angle, if detected, is solely caused by the tag self-rotation. Since the tag’s rotation causes simultaneous change of angle at both antennas, we have $\theta _ { 1 , i + 1 } - \theta _ { 1 , i } = \theta _ { 2 , i + 1 } - \theta _ { 2 , i }$ . By respectively subtracting the two formulas at two antennas, we get the following equations.

$$
\left\{ \begin{array}{l} \Delta \phi_ {p, i} = \left(\frac {2 \pi}{\lambda} \times 2 \Delta d _ {p, i} + k \times \Delta \theta_ {p, i}\right) \mod 2 \pi \\ \Delta \phi_ {p, i} = \phi_ {p, i + 1} - \phi_ {p, i}, \Delta d _ {p, i} = d _ {p, i + 1} - d _ {p, i} \\ \Delta \theta_ {p, i} = \theta_ {p, i + 1} - \theta_ {p, i} \end{array} \right. \tag {4}
$$

According to the above inference, $\varDelta \theta _ { 1 , i } = \varDelta \theta _ { 2 , i }$ . By further subtracting $\Delta \phi _ { 1 , i }$ and $\varDelta \phi _ { 2 , i }$ in Eq. (4), we can eliminate the impact of rotation angles and get

$$
\left\{ \begin{array}{l} \Delta \phi_ {i} = \Delta \phi_ {2, i} - \Delta \phi_ {1, i} = (\frac {2 \pi}{\lambda} \times 2 \Delta d _ {i}) \mod 2 \pi \\ \Delta d _ {i} = (d _ {1, i + 1} - d _ {2, i + 1}) - (d _ {1, i} - d _ {2, i}) \end{array} \right. \tag {5}
$$

Recall that we know the previous position and orientation of the tag, the distance difference $( d _ { 1 , i } - d _ { 2 , i } )$ is known. According to Eq. (5), we can obtain the distance difference at time $t _ { i + 1 }$ , namely $( d _ { 1 , i + 1 } - d _ { 2 , i + 1 } )$ , as long as $\Delta \phi _ { i }$ is uniquely determined. Fig. 6 illustrates the geometric relationship during tracking. According to the triangle inequality theorem, we have

$$
\left| d _ {1, i} - d _ {2, i} \right| <   2 m, \left| d _ {1, i + 1} - d _ {2, i + 1} \right| <   2 m \tag {6}
$$

2m is the distance between the two antennas. Thus if we make the distance between the two antennas within the half-wavelength $\frac { \lambda } { 2 }$ (about 15cm), then we have

$$
\left| d _ {1, i} - d _ {2, i} \right| <   \frac {\lambda}{2}, \left| d _ {1, i + 1} - d _ {2, i + 1} \right| <   \frac {\lambda}{2}. \tag {7}
$$

That means the $\begin{array} { r } { - \frac { \lambda } { 2 } < \Delta d < \frac { \lambda } { 2 } } \end{array}$ , which constrains the range of the phase between −2π and 2π according to Eq. (5). In this way, we can get a unique value of $\varDelta \phi _ { i }$ and in turn obtain the value of $( d _ { 1 , i + 1 } - d _ { 2 , i + 1 } )$ . Actually, the constraints for the distance between antennas can be relaxed based on the feasible region proposed in BackPos [8]. Since the location and the orientation are calculated in an iterative way. The distance between antennas has no effect on the accuracy of the tracking.

So far we know the position of the antennas and the difference of the distances from the tag to the antennas, the tag is located in a hyperbola with the two antennas as the focues. As shown in Fig. 7, we denote the current location of the tag by $P _ { i } .$ . The tag’s movement direction consists of two projected directions: $\overrightarrow { A _ { 1 } P _ { i } }$ and $\overrightarrow { A _ { 2 } P _ { i } }$ . As illustrated before, the sampling interval of the reader is very short so that we can assume the tag’s moving direction doesn’t change during a sampling interval. The moving distances $\varDelta d _ { 1 , i } , \varDelta d _ { 2 , i }$ from time $t _ { i }$ to time $t _ { i + 1 }$ at the two projected directions can be calculated according to Eq. (4):

$$
\left\{ \begin{array}{l} \Delta d _ {1, i} = (\frac {\lambda}{4 \pi} (\Delta \phi_ {1, i} - k \times \Delta \theta_ {i}) \\ \Delta d _ {2, i} = (\frac {\lambda}{4 \pi} (\Delta \phi_ {2, i} - k \times \Delta \theta_ {i}) \end{array} \right. \tag {8}
$$

Therefore, we can calculate the new position of the tag $P _ { i + 1 }$ by:

$$
P _ {i + 1} = P _ {i} + \Delta d _ {1, i} \overrightarrow {A _ {1} P _ {i}} + \Delta d _ {2, i} \overrightarrow {A _ {2} P _ {i}} \tag {9}
$$

The new location of the tag is the intersection of the line $P _ { i } P _ { i + 1 }$ and the hyperbola described before. We define the line connecting two antennas as the X axis and the vertical bisector of the two antennas as the Y axis. Then we have:

$$
\left\{ \begin{array}{l} \frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \\ m ^ {2} - a ^ {2} = b ^ {2} (b > 0) \\ x _ {i} + \Delta d _ {1, i} \cos \alpha_ {1, i} + \Delta d _ {2, i} \cos \alpha_ {2, i} = x \\ y _ {i} + \Delta d _ {1, i} \sin \alpha_ {1, i} + \Delta d _ {2, i} \sin \alpha_ {2, i} = y \end{array} \right. \tag {10}
$$

$\alpha _ { 1 , i }$ and $\alpha _ { 2 , i }$ are denoted in Fig. 7. Solving the above equation yields the tag’s rotation angle $\varDelta \theta _ { i }$ and new coordinates $( x , y )$ . Through the above updating process, OmniTrack keeps tracking the location and the orientation of a moving tag.

# 4.2 Initialization

OmniTrack tracks the target in an iterative way according to the consecutively received phases, the previous location, and the previous orientation of the target. We should design a light-weight component to calculate both the initial location and orientation of the target. The initialization component mainly uses the techniques of channel hopping and RSS pattern matching.

According to our orientation-4.2.1 Channel Hopping.aware phase model provided in $\operatorname { E q . } ( 2 ) ,$ the random hardware phase offset denoted by c can make the distance derivation unreliable. However, we observe that our orientation-aware phase model in $\operatorname { E q . } ( 2 )$ can also be expressed as follow:

$$
\phi = (\frac {2 \pi f}{v} \times 2 d + k \times \theta + c) \mod 2 \pi \tag {11}
$$

$f$ is the frequency of the carrier wave and v is the speed of the electromagnetic wave.

The phase changes linearly with the frequency. If we measure multiple phase readings with channel hopping, the effect of the angle θ and hardware c can be eliminated through the subtraction among the phase readings with different frequencies.

In COTS RFID system, the gaps of adjacent hopping channels are equal, we still can’t solve out a unique distance through phase differences. In OmniTrack, we make the antennas to hop the channels with the same frequency gap $\Delta f _ { : }$ , then we can obtain the phase change $\varDelta \phi _ { i }$ corresponding to the frequency change $\Delta f$ at the antenna i. The $\varDelta \phi _ { i }$ can be expressed as:

$$
\Delta \phi_ {i} = (\frac {4 \pi}{v} \times d _ {i} \times \Delta f) \mod 2 \pi \tag {12}
$$

$d _ { i }$ is the distance between the tag and the antenna i. There still exists phase ambiguity. However, with at least two antennas, we can obtain the distance difference between the tag and two antennas i and j:

$$
\Delta \phi = \Delta \phi_ {i} - \Delta \phi_ {j} = (\frac {4 \pi}{v} \times (d _ {i} - d _ {j}) \times \Delta f) \mod 2 \pi \tag {13}
$$

We observe that $d _ { i } - d _ { j }$ is unique if $\begin{array} { r } { | d _ { i } - d _ { j } | < \frac { v } { 2 \Delta f } } \end{array}$ , which constrains the range of $\Delta \phi$ between −2π and 2π. As shown in Fig. 8, we can locate the tag in a hyperbola defined by the two antennas and the distance difference. When there are more antennas, we can draw multiple hyperbolas for each two antennas and locate the tag at their intersecting point.

The phase and RSS received by the reader can present unique pattern when we rotate the tag by one cycle $( 3 6 0 ^ { \circ } )$ at a fixed position. As shown in Fig. 9, the phase changes linearly with the relative rotation angle, which satisfies our phase model in $\operatorname { E q . } ( 2 )$ . The relation between the RSS and the rotating angle satisfies the sinusoid function. When the tag rotates to point at the reader (the $\begin{array} { r } { \theta = \frac { \pi } { 2 } o r \frac { 3 \pi } { 2 } } \end{array}$ $\operatorname { E q . } ( 2 ) )$ , the RSS reaches its lowest value. It is the antenna and the tag. Thus we can know the tag’s current direction if the current RSS reaches its lowest value.

In OmniTrack, with two antennas $A _ { 1 }$ and $A _ { 2 }$ as shown in Fig. 8, we rotate the tag anticlockwise. The RSS received by $A _ { 1 }$ will first capture a lowest value at time $t _ { 0 } ,$ then we mark a corresponding time $t _ { 1 }$ at antenna $A _ { 2 }$ . After that, antenna $A _ { 2 }$ will capture a lowest value at time $t _ { 2 } .$ . We know that during the time period $( t _ { 1 } , t _ { 2 } )$ , the tag rotates for $\varDelta \theta .$ . In order to calculate $\varDelta \theta _ { ; }$ we retrieve the phase values $\phi _ { 1 }$ and $\phi _ { 2 }$ corresponding to $t _ { 1 }$ and $t _ { 2 }$ at antenna $A _ { 2 }$ So according to the model in $\operatorname { E q . } ( 2 )$ , the $\varDelta \theta$ is $| k ( \phi _ { 2 } - \phi _ { 1 } ) |$ . In another case, if the tag rotates clockwise, the $\varDelta \theta$ is $2 \pi - | k ( \phi _ { 2 } - \phi _ { 1 } ) | \colon k$ is the fixed phase changing rate in $\operatorname { E q . } ( 2 )$ .

We already know the hyperbola and the intersecting angle $\varDelta \theta$ in Fig. 8, then we can solve out both the location and orientation of the tag if we define the line connecting two antennas as the X axis and the vertical bisector of the two antennas as the Y axis. The set of equations is expressed below:

$$
\left\{ \begin{array}{l} \frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \\ m ^ {2} - a ^ {2} = b ^ {2} (b > 0) \\ d _ {1} ^ {2} + d _ {2} ^ {2} - 2 d _ {1} d _ {2} \cos \theta = 4 m ^ {2} \end{array} \right. \tag {14}
$$

Since the phase value corresponding to the lowest RSS is recorded when we rotate the tag, any orientation of the tag relative to the antenna can be calculated from the phase difference according to $\operatorname { E q . } ( 2 )$ .

We could find the initialization of the system is reduced to solve an equation set, which incurs negligible computational cost into the system. As for the channel hopping time and the rotation time, in industrial system, there are preparation zones for each production lines, so these operations could be finished at these places not to incur extra costs to the system.

![](images/1505d28f58f32f32029e898ed863f3cced486e9daeeb1b548e7ae74d8762b835.jpg)



(a) Phase changing with rotation

![](images/d630567701723848e2a4ed1d269389c9eeb86f46937fe1eaa35f87fe771d907e.jpg)



(b) RSS changing with rotation   
Figure 9: Measured phase and RSS of a tag rotating for $3 6 0 ^ { \circ }$

# 4.3 Calibration

The iterative calculation in tracking is likely to accumulate errors. Therefore, we design a calibration component to eliminate the accumulated error.

We first conduct the experiments to find the characteristics of the received signal when the tag is moving and rotating. We slide a tag back and forth in a distance of 20cm and draw the RSS change in Fig. 10 (a). Also, we rotate the tag to measure the RSS value and present the result in Fig. 10 (b).

From Fig. 10, we find: (1) The RSS change caused by tag’s rotation is far more than that caused location displacement. In other word, if the tag’s rotation is the main movement when tracking, we could ignore the effect of the tag’s displacement on the RSS. (2) The RSS change caused by the tag’s rotation satisfies the sinusoid relation and the RSS value is related to the rotating angle.

In most scenarios, the rotation of the target is common and frequent. So in OmniTrack, we try to first capture those intervals that the target’s rotation is dominant and it has almost no movement, then we can search for a proper initial orientation so that all RSS changes in these intervals can fit the sinusoid function well. There are two steps to finish the task: (1) finding the calibration intervals; (2) designing suitable algorithm to calibrate the orientation.

Calibration Interval: The calibration in OmniTrack is passively triggered in a calibration interval. Specifically, the calibration interval is specified according to the observation above: the tag’s rotation is the main movement. In the implementation, we define two variables to detect the calibration interval: the total rotating angle θ and the total moving distance d during the interval. The interval is detected if $\theta > \theta _ { t }$ and $d < d _ { t }$ , where $\theta _ { t }$ and $d _ { t }$ are predefined parameters $\left( d _ { t } = 1 0 \right)$ cm, $\theta _ { t } = 3 0 ^ { \circ }$ in our implementation).

Calibration Algorithm: In the calibration interval, we can obtain a series of rotation angles as $\{ \varDelta \theta _ { i } \}$ based on our tracking module and our goal is to calibrate the orientation at the beginning of the interval. According to our second observation, we can model these RSS changes as:

$$
r s s = P \left| \sin (\theta + \Delta \theta) \right| + P _ {\text { offset }} \tag {15}
$$

![](images/58c163fbca4de72283b66d1f2acf79f54da2860945c0c251d011d28fbd070897.jpg)



(a) RSS changing in small displacement (b) RSS changing when angle changing   
![](images/1f13c3a2f1d9da7aa4ffc73e17d318c514e2fbb176023e083bc377325acac18f.jpg)



Figure 10: RSS changing pattern

where P is the maximum RSS range and $P _ { o f f s e t }$ is the strength offset. We denote the series of RSS differences corresponding to the rotation angles as {Δrssi } and the initial orientation angle we want to calibrate as $\theta _ { o }$ .

Our goal is to search for an initial orientation angle that can make the theoretical RSS series suits {Δrssi } best. The theoretical Δrssi has the expression below:

$$
\Delta r s s _ {i} = P (| \sin (\theta + \Delta \theta_ {i + 1}) | - | \sin (\theta + \Delta \theta_ {i}) |) \tag {16}
$$

The RSS range P depends on many factors like the tag’s distance to the antenna and the transmitting power of the reader, it is hard to accurate acquire the parameter. Instead, we turn to the metric $\frac { \varDelta r s s _ { i + 1 } } { \varDelta r s s _ { i } }$ , which can eliminate the parameter P. We enumerate the angle θ in the range from 0 to 2π with the accuracy of $1 ^ { \circ }$ and set the angle that minimizes the $\begin{array} { r } { \sum \big ( \frac { \varDelta r s s _ { i + 1 } } { \varDelta r s s _ { i } } \big ) ^ { 2 } } \end{array}$ as the calibrated angle at the beginning of the interval. One thing we should notice is that theoretically we could obtain two angles that both minimize the metric because of the periodicity of the RSS change model. The difference between the two angles is just π . Thus if the angle calculated is not close to the angle $\theta _ { o } ,$ , we will use the corresponding angle that close to $\theta _ { o }$ .

The location could be calibrate with the calibrated orientations at different antennas using the method in initialization module.

# 5 DISCUSSION

Multi-path effect: The Multi-path effect interferes with signal propagation, which is a common problem for phasebased localization and tracking. The multi-path propagation may also entangle the phase calculation in OmniTrack, as the phase change induced by the tag orientation becomes complicated. By examing the real industrial application scenarios, we find that multi-path effect can be avoided as much as possible, by deploying the reader antennas at appropriate positions. For example, for tracking medicine bottles on a biopharmaceutical production line (Fig. 1), one can deploy the antennas sufficiently close to the line to ensure the quality of line-of-sight signals [22]. Even when the multi-path signals really interfere with phase calculation, we can take effective countermeasures, e.g. channel hopping in MobiTagbot [13], to mitigate the negative impact.

![](images/5c598c6ed2219cb0203804addeca296608d663a3483f46107257d65311224515.jpg)



(a) Linear Track

![](images/3ffa9badd2f08ee2d66edfa42cd29ca18ce8a89e94f7ba68eec548303ef20ee5.jpg)



(b) Circular Track   
Figure 11: Experiment Setup

Scalability: Note that the communication range of a RFID reader is typically several meters. How to extend the deployment of OmniTrack and make it seamlessly cover a large area (e.g. a long pipeline) becomes a meaningful issue. For reliable and seamless tracking, one can deploy multiple pairs of antennas in different subareas. Adjacent pairs of antennas should have their interrogated areas intersected with each other. Moreover, all the antennas are connected and synchronized at the back-end. Knowing the real-time location of a tag, the reader is able to determine when and to which antenna a handover of tracking responsibility should be made.

Generalizability: In many modern industrial production lines, the whole line is separated into different function zones and at the joints of these zones, there are special areas for the products to adjust its states, like orientation. Taking the automobile production line for example, the body of a car needs to pass several function zones like cutting and spraypainting. Before entering the next function zone, there is a specific area to adjust the car’s posture and orientation so that the manipulators can accurately make operations on it. When OmniTrack is applied to such a scenario, the joints of the function zones can be used to initialize and calibrate the system. The orientation and location provided by OmniTrack are also very important information for these function zones. OmniTrack can work with only two antennas, which can save the costs of deployments.

# 6 EVALUATION

This section presents the implementation details and evaluation results. We implement OmniTrack on COTS devices. Then we compare it with two state-of-the-arts approaches with different experimental settings.

Implementation: In the implementation and experiments, we use an ImpinJ Speedway R420 RFID reader, two Laird circular polarized antennas, and Alien UHF passive RFID tags. The whole system operates at the 920-926 MHz band, with frequency hopping enabled.

The tags and the reader adopt LLRP protocol for communication. The ImpinJ reader extends this protocol to support the phase readings. We configure the reader to immediately report the phase reading, whenever a tag is detected. The software is implemented using C#. In the lab experiments, we run the software at a MSI desktop PC, which has Intel Core i7 6700 CPU at 2.6 GHz and 8G memory.

Methodology: We attach a tag onto an automatic rotating plate, then we mount the plate on the top of a toy train. Fig. 11 shows the experiment setups and the rails of the train. There are two types of experiments: tracking without rotation and tracking with rotation. For tracking without rotation, we disable the rotation of the plate when the train drives along the rails. The orientation still changes, but only due to the movement of the train. For tracking with rotation, we select several spots on the rails, where the plate is manually rotated to to emulate the operations that changes the targetfis orientation.

We evaluate the performance of tracking in terms of the localization error and the orientation error. The ground-truth location of the target is calculated according to the moving speed of the train and the geometric property of the rails. The ground-truth orientation is acquired based on the angle marks on the surface of the plate.

We compare OmniTrack with state-of-the-art approaches: Tagoram [25] and BackPos [8]. Tagoram assumes the prior knowledge of the rails so as to emulate virtual antenna arrays. OmniTrack and BackPos requires no prior knowledge. We implement the three approaches with the same hardwares.

# 6.1 Tracking without Rotation

We first evaluate the performance in the rails shown in Fig. 11 and there is no manual rotation during the tracking. The movement speed of the train is set at the same magnitude as the existing works like Tagoram.

Linear Rail: In this experiment, the train drives on the linear rail as shown in Fig. 11 (a). We set the train’s driving speed at three levels (0.127m/s, 0.203m/s, and 0.286m/s). At each speed, we repeat the experiment 25 times and calculate the average location error of OmniTrack, Tagoram, and BackPos. We plot the CDF of location errors in Fig. 12.

When the train’s speed v = 0.127m/s, the average location errors of Tagoram, OmniTrack and BackPos are 2.4cm, 3.4cm, and 8.3cm, respectively. When the moving speed v = 0.203m/s, the average location errors of Tagoram, OmniTrack, and BackPos are 3.9cm, 5.1cm, and 11.7cm, respectively. When the moving speed v = 0.286m/s, the average errors increase to 4.9cm, 7.2cm, and 13.1cm correspondingly. As the speed increases, all the three approaches suffer accuracy degradation because the higher speed decreases the phase samplings within a fixed distance. Tagoram has the best performance, owning to the prior knowledge of the movement trajectory. The accuracy of OmniTrack is close to that of Tagoram, without the requirement of prior knowledge. BackPos is apparently less accurate, due to the impact of orientation change.

![](images/67b25446e7c566c08ca3475aeb1a0f7ba5e02a7d26686d5cda065289253eba81.jpg)



(a) v=0.127m/s

![](images/fa259508c8bfc670c8d139be2653527553794b00571b2220e1877d1695f5cb00.jpg)



(b) v=0.203m/s

![](images/c88561850878ebaefcf464e0e34514bebbf1c37fd9631fab934377726f104758.jpg)



(c) v=0.286m/s   
Figure 12: Location error on the linear rail

![](images/d2bc1cc072827f47acdcff32f78cc6b0f28cbe5d9be7d59094950afe9d2d914f.jpg)



(a) v=0.127m/s

![](images/8f811821b3daa3e217d53ce4d38d2123cf681a336ede787a54746029594b62d3.jpg)



(b) v=0.203m/s

![](images/dd5dcd0f34a4e0ff71006fed2e0c3b850a1b39e2669ef4bd384d7ad1147f1636.jpg)



(c) v=0.286m/s

Figure 13: Location error on the circular rail   
![](images/a3f99564a3f5d2e50265d7971e166f641848b84e4868383be1c051f0ddd7bdef.jpg)



Figure 14: Tracking rotating targets on two different rails

Circular Rail: We then carry out experiments when the train drives on a circular rail as in Fig. 11 (b). In this experiment, we let the train run for a round and calculate the average location error. Similar with the previous experiment, the train’s speed is set at three levels. For each speed, the experiments are repeated for 25 times. We compare OmniTrack with Tagoram and BackPos and plot the CDF of location errors in Fig. 13.

It shows that the average location errors of OmniTrack are 6.1cm, 7.1cm, and 8.5cm when the moving speeds are 0.127m/s, 0.203m/s, and 0.286m/s, respectively. The tag’s orientation keeps changing due to the circular rail, even though we don’t manually rotate it. The orientation change affect the location errors of the three approaches. It is worth noticing that the accuracy gap between OmniTrack and Tagoram is reduced because of the orientation-aware model used in OmniTrack. However, Tagoram still achieves the best accuracy, owing to the prior knowledge of the movement. So in the next experiments, we evaluate the performance in more complex scenarios, which emulate the practical industrial applications scenarios.

# 6.2 Tracking with Rotation

In this section, we evaluate the three approaches when tracking the targets with rotation. The two rails are shown in Fig. 14. Other than the orientation changes at the curves of the rails, we set several rotation spots where the plate on the train rotates for 60◦.

Straight Track: We plot the CDF of location errors in Fig. 15. The train’s speed is set at three levels, namely 0.104m/s, 0.186m/s, and 0.232m/s.

We can see that OmniTrack apparently outperforms Tagoram and BackPos in this group of experiments. When the train’s speed is 0.104m/s, the average location errors of OmniTrack, Tagoram, and BackPos are 4.3cm, 7.7cm, and 13.3cm, respectively. In term of location error, OmniTrack outperforms Tagoram and BackPos by 1.8× and 3.1×, respectively. The reason behind is that OmniTrack quantifies the impact of tag orientation on phase readings and eliminate that negative impact by using the orientation-aware model.

Comparing the results of Fig. 12 and Fig. 15, OmniTrack has consistently stable location accuracy, no matter the tag rotates or not. In comparison, the accuracy of Tagoram and BackPos apparently degrades when the tag rotation is introduced.

To further understand the advantage of OmniTrack, we present the error changes of the three approaches on the straight rail. The results are shown in Fig. 19. We can clearly observe that at every rotation spot, the location errors of

![](images/6182cc4bb0cdf015c86a3aeca449696621c324bfe40fca035d7c2b79a1f9ee6f.jpg)



(a) v=0.104m/s

![](images/23cf4b0d02d417d4fa833cb772f90bca335bce37687c570d8d73916e831d74ea.jpg)



(b) v=0.186m/s

![](images/3a62d829fbe80f2c104050e94c1be78be132fbbce779fbe92b8b62d08bf12482.jpg)



(c) v=0.232m/s   
Figure 15: Location error on the straight rail

![](images/af423bd338a5812414ba665c965e15081ed5f894ad394be5f158bc641d8f3cd6.jpg)



(a) v=0.102m/s

![](images/e6551a61b4848c3f625ed91730f336b0d3e45e6abd8d2fbe1c5e1477ac671013.jpg)



(b) v=0.174m/s

![](images/9c9ffec20423854faf59d5e5f93ab6b421644793017fdf25f66719355bcb5f85.jpg)



(c) v=0.223m/s   
Figure 16: Location error on the S-shape rail

Tagoram and BackPos significantly increase while Omni-Track keeps the error at a low level. The reason is OmniTrack explicitly deals with the problem of orientation change.

S-shape Track: Next we evaluate the tracking performance when the train drives on a more complex rail. This time we adopt a S-shape rail with six rotation spots, as shown in Fig. 14. The total length of the track is 232 cm. The plate attached with tag rotates for $6 0 ^ { \circ }$ at every rotation spot. The train’s speed is set at three levels, namely 0.102m/s, 0.174m/s, and 0.223m/s.

We plot the CDF of location errors in Fig. 16. We can find that the S-shape rail with more turns and rotations exacerbates the problem with the orientation-obliviousness model in BackPos and Tagoram. The average location errors of Tagoram and BackPos are 9.7cm and 14.3cm, respectively, when the train’s speed $v = 0 . 1 0 2 m / s$ . In comparison, OmniTrack has an average location error of only 5.7cm, outperforming Tagoram and BackPos by 1.7× and 2.5×, respectively.

# 6.3 Accuracy of Orientation

OmniTrack can simultaneously calculate a tag’s orientation, which cannot be done by either Tagoram or BackPos.

We record the orientation errors during the experiments of tracking targets without rotation in Section 6.1. Fig. 17 presents the means and variations of orientation errors. The average orientation error on the linear rail is 3.2◦, 4.6◦, and 5.5◦, when the train’s speed v is 0.127m/s, 0.203m/s, and $0 . 2 8 6 m / s _ { \mathrm { ; } }$ , respectively. On the circular rail, the average orientation error is $1 0 . 3 ^ { \circ }$ , 12.8◦, and $1 5 . 6 ^ { \circ }$ , respectively under the corresponding speed. The orientation error on the circular rail is higher than that on a linear rail, because orientation change is more frequent and continuous on the circular rail. Besides, the attenuation of backscattered signals may be larger when the train drives on the semicircle farther to the antennas. Then the RSS and phase readings appear to be more noisy, potentially inducing higher errors.

We record the orientation errors during the experiments of tracking targets with rotation in Section 6.2. Fig. 18 shows the means and variations of orientation errors. The average orientation errors on the straight rail are 5.7◦, $6 . 6 ^ { \circ }$ , and $8 . 5 ^ { \circ }$ , when the moving speeds are 0.102m/s, 0.174m/s, and 0.223m/s, respectively. On the S-shape rail, the average orientation errors are 8.3◦, 10.6◦, and 13.4◦, respectively under the corresponding speed. The orientation error on the S-shape rail is higher than that on the straight rail, because orientation change is more frequent on the S-shape rail.

# 6.4 Accuracy of Initialization

In this section, we evaluate the accuracy of the initialization in OmniTrack. In order to evaluate the accuracy of the initialization, we select 12 positions on the circular rail to separately initialize OmniTrack. The selected positions are shown in Fig. 11. We conduct initialization at each position for 10 times. The results of the location error are shown in Fig. 20. The average location error is 1.7cm. For positions No. 4 and No. 8, the location errors are higher than the average. The two positions are far from the antennas, so the achievable sampling rates of phase and RSS are relatively lower due to the weak signals.

The results of the orientation error are shown in Fig. 21. The average orientation error is below $7 ^ { \circ }$ at the 12 positions. The orientation errors at position No. 4 and No. 8 are still higher than others because of the lower sampling rates.

![](images/0fd61669a78a9a69e4f00546c8910f6943ba6bc0459976f316eaacdcbd1a4ab8.jpg)



![](images/b04220c3873f82b46fcd30729772a3263e330e35f814901fe4e13affb6b23ade.jpg)



![](images/b64f4514a38834dadc50b47471da67288ce283180e089bb74013c2fb768a21a3.jpg)



Figure 17: Orientation error on Figure 18: Orientation error on Figure 19: Location error along the rail the rail without rotation the rail with rotation

![](images/101ee70271b2fb1b6d5e53f4feb02df62f41742e59c6a3a59b7ffcd90f4e0879.jpg)



Figure 20: Accuracy of the initialization at different positions

![](images/c0907d7386eca4d17853dd1a821ff11e31a86d296eba7a4fe9139ac2cb8c4f1e.jpg)



Figure 21: Accuracy of the Orientation at different positions

# 6.5 Accuracy of the Calibration

Recall that the calibration contains two components: location calibration and orientation calibration. The location calibration part is similar to the initialization phase, whose performance is already evaluated in Section 6.4. Next we focus on evaluating the orientation calibration. The rotation spots on the rails naturally become the opportunities for orientation calibration. We plot the orientation error before and after calibration at each spot in Fig. 22.

From the results, we can find the calibration on the straight rail can reduce the orientation error by 1.4◦, 2.7◦, 3.2◦ and $3 . 5 ^ { \circ }$ at the four rotation spots, respectively. Due to errors accumulation , the orientation error is increasing during the movement. The orientation error on the S-shape rail has a similar trend with that on the straight rail. The calibration reduces the orientation error by 2.4◦, 1.8◦, 2.1◦, 2.6◦, 3.5◦, and $2 . 6 ^ { \circ }$ at the six rotation spots, respectively.

To examine the performance of orientation calibration in more details, we carry out a separate experiment. We attach the tag at the center of the rotation plate and fix the location of the plate. We rotate the plate from $0 ^ { \circ }$ to $3 6 0 ^ { \circ }$ at a constant speed of $6 ^ { \circ } / s .$ . We calculate the orientation error with and without calibration during the rotation process. The results are shown in Fig. 23. The length of the radius is the scale of orientation error. We can find that without calibration, the error is accumulated and can be as large as $1 2 ^ { \circ }$ . In comparison, our calibration algorithm can limit the accumulated error and keep the orientation error below $6 ^ { \circ }$ .

# 7 CONCLUSION

Accurate tracking of targets is a significant problem in industrial CPS. In this work, we look into the signal propagation process between a RFID reader and a tag. For the first time in the community, we discover and quantify the impact of tag orientation on phase change. Based on this finding, we propose OmniTrack, an orientation-aware RFID tracking approach that is applicable to COTS RFID systems. Unlike the existing phase-based proposals, OmniTrack employs an orientation-aware phase model for target tracking and efficiently deals with various orientation-dependent problems. The evaluation results demonstrate that OmniTrack achieves centimeter-level location accuracy and has significant advantages in tracking targets with varing orientations, compared to the state-of-the-art approaches.

# ACKNOWLEDGEMENT

This work is supported in part by National Key R&D Program of China No. 2017YFB1003000, NSF China Key Project No. 61432015 and No. 61632008, National Natural Science Foundation of China under grant No. 61772306 and No. 61672320.

# REFERENCES

[1] J. L. Brchan, L. Zhao, J. Wu, R. E. Williams, and L. C. Perez. A real-time ´ rfid localization experiment using propagation models. In RFID (RFID), 2012 IEEE International Conference on, pages 141–148, 2012.   
[2] N. Brouwers, M. Zuniga, and K. Langendoen. Incremental wi-fi scanning for energy-efficient localization. In Pervasive Computing and Communications (PerCom), 2014 IEEE International Conference on, pages 156–162. IEEE, 2014.

![](images/0795b9596155c12c9f6125ac9497d2262e1afab18d5928b48093cd84aa735864.jpg)



(a) Straight rail

![](images/0e88f2f9accae2840ea255bb70e3e37a1162d585726b0411cdfb44d87711c0e9.jpg)



(b) S-shape rail   
Figure 22: The impact of the orientation calibration

![](images/6758ead7009b35009332bf981a7750fcc4b4f6d747fd2a3031dc4bfdeb0ed120.jpg)



Figure 23: Orientation error when rotating at a fixed position

[3] W. Cheng, X. Cheng, M. Song, B. Chen, and W. W. Zhao. On the design and deployment of rfid assisted navigation systems for vanets. IEEE Transactions on Parallel and Distributed Systems, 23(7):1267–1274, 2012.   
[4] S. Han, H. Lim, and J. Lee. An efficient localization scheme for a differential-driving mobile robot based on rfid system. IEEE Transactions on Industrial Electronics, 54(6):3362–3369, 2007.   
[5] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar. Accurate localization of rfid tags using phase difference. In RFID, 2010 IEEE International Conference on, pages 89–96, 2010.   
[6] J. Hightower, R. Want, and G. Borriello. Spoton: An indoor 3d location sensing technology based on rf signal strength. 2000.   
[7] K. R. Joshi, S. S. Hong, and S. Katti. Pinpoint: Localizing interfering radios. In NSDI, pages 241–253, 2013.   
[8] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu. Anchor-free backscatter positioning for rfid tags with high accuracy. In INFOCOM, 2014 Proceedings IEEE, pages 379–387, 2014.   
[9] R. Miesen, F. Kirsch, and M. Vossiek. Holographic localization of passive uhf rfid transponders. In RFID (RFID), 2011 IEEE International Conference on, pages 32–37, 2011.   
[10] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil. Landmarc: indoor location sensing using active rfid. Wireless networks, 10(6):701–710, 2004.   
[11] J. Ou, M. Li, and Y. Zheng. Come and be served: Parallel decoding for cots rfid tags. IEEE/ACM Transactions on Networking, 2017.   
[12] A. Parr, R. Miesen, and M. Vossiek. Inverse sar approach for localization of moving rfid tags. In RFID (RFID), 2013 IEEE International Conference on, pages 104–109, 2013.   
[13] L. Shangguan and K. Jamieson. The design and implementation of a mobile rfid tag sorting robot. In Proceedings of the 14th Annual International Conference on Mobile Systems, Applications, and Services, pages 31–42, 2016.   
[14] L. Shangguan and K. Jamieson. Leveraging electromagnetic polarization in a two-antenna whiteboard in the air. In Proceedings of the 12th International on Conference on emerging Networking EXperiments and Technologies, pages 443–456, 2016.   
[15] Y. Shen, W. Hu, J. Liu, M. Yang, B. Wei, and C. T. Chou. Efficient background subtraction for real-time tracking in embedded camera networks. In Proceedings of the 10th ACM Conference on Embedded Network Sensor Systems, pages 295–308. ACM, 2012.   
[16] A. A. N. Shirehjini, A. Yassine, and S. Shirmohammadi. An rfid-based position and orientation measurement system for mobile objects in

intelligent environments. IEEE Transactions on Instrumentation and Measurement, 61(6):1664–1675, 2012.   
[17] Y. Shu, P. Cheng, Y. Gu, J. Chen, and T. He. Toc: Localizing wireless rechargeable sensors with time of charge. ACM Transactions on Sensor Networks (TOSN), 11(3):44, 2015.   
[18] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus. Rf-compass: Robot object manipulation using rfids. In Proceedings of the 19th annual international conference on Mobile computing & networking, pages 3–14, 2013.   
[19] J. Wang and D. Katabi. Dude, where’s my card?: Rfid positioning that works with multipath and non-line of sight. ACM SIGCOMM Computer Communication Review, 43(4):51–62, 2013.   
[20] T. Wei and X. Zhang. Gyro in the air: tracking 3d orientation of batteryless internet-of-things. In Proceedings of the 22nd Annual International Conference on Mobile Computing and Networking, pages 55–68, 2016.   
[21] Z. Xiao, H. Wen, A. Markham, and N. Trigoni. Lightweight map matching for indoor localisation using conditional random fields. In Information Processing in Sensor Networks, IPSN-14 Proceedings of the 13th International Symposium on, pages 131–142. IEEE, 2014.   
[22] Z. Xiao, H. Wen, A. Markham, N. Trigoni, P. Blunsom, and J. Frolik. Non-line-of-sight identification and mitigation using received signal strength. IEEE Transactions on Wireless Communications, 14(3):1689– 1702, 2015.   
[23] J. Xiong and K. Jamieson. Arraytrack: A fine-grained indoor location system. In NSDI, pages 71–84, 2013.   
[24] C. Xu, B. Firner, Y. Zhang, R. Howard, J. Li, and X. Lin. Improving rfbased device-free passive localization in cluttered indoor environments through probabilistic classification methods. In Proceedings of the 11th international conference on Information Processing in Sensor Networks, pages 209–220. ACM, 2012.   
[25] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: Realtime tracking of mobile rfid tags to high precision using cots devices. In Proceedings of the 20th annual international conference on Mobile computing and networking, pages 237–248, 2014.   
[26] P. Zhang, M. Rostami, P. Hu, and D. Ganesan. Enabling practical backscatter communication for on-body sensors. In Proceedings of the 2016 conference on ACM SIGCOMM 2016 Conference, pages 370–383. ACM, 2016.   
[27] C. Zhou and J. D. Griffin. Accurate phase-based ranging measurements for backscatter rfid tags. IEEE Antennas and Wireless Propagation Letters, 11:152–155, 2012.