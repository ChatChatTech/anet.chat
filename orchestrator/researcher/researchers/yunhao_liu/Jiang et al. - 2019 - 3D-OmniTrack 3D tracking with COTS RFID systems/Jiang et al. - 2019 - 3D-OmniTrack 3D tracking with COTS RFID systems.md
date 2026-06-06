# 3D-OmniTrack: 3D Tracking with COTS RFID Systems

Chengkun Jiang1, Yuan He1, Songzhen Yang1, Junchen Guo1, Yunhao Liu1,2

1School of Software and BNRist, Tsinghua University

2Department of Computer Science and Engineering, Michigan State University

{jck15, ysz18, gjc16}@mails.tsinghua.edu.cn, {heyuan, yunhao}@tsinghua.edu.cn

# ABSTRACT

RFID tracking has attracted significant interest from both academia and industry due to its low cost and ease of deployment. Previous works focus more on tracking in 2D space or separately consider tracking of the location and the orientation. They especially struggle in 3D situations due to the increase in the degree of freedom and the limited information conveyed by the RFID tags. In this paper, we propose 3D-OmniTrack, an approach that can accurately track the 3D location and orientation of an object. We introduce a polarization-sensitive phase model in an RFID system, which takes into consideration both the distance and the 3D posture of an object. Based on this model, we design an algorithm to accurately track the object in 3D space. We conduct real-world experiments and present results that show 3D-OmniTrack can achieve centimeterlevel location accuracy with the average orientation error of 5◦. 3D-OmniTrack has significant advantages in both the accuracy and the efficiency, compared with state-of-the-art approaches.

# CCS CONCEPTS

• Computer systems organization → Embedded and cyberphysical systems; Real-time systems; • Hardware → Sensor applications and deployments.

# KEYWORDS

RFID; 3D Tracking; Orientation; Polarization; Location; Rotation

# ACM Reference Format:

Chengkun Jiang1, Yuan He1, Songzhen Yang1, Junchen Guo1, Yunhao Liu1,2. 2019. 3D-OmniTrack: 3D Tracking with COTS RFID Systems. In The 18th International Conference on Information Processing in Sensor Networks (colocated with CPS-IoT Week 2019) (IPSN ’19), April 16–18, 2019, Montreal, QC, Canada. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/ 3302506.3310386

# 1 INTRODUCTION

Tracking the location and the orientation of a target becomes an indispensable function for many applications in both Internet of Things (IoT) and Human-Computer Interaction (HCI) fields, such as industrial monitoring, gesture recognition and VR control [4, 6, 8, 14, 18, 19, 26, 27]. Much effort from academia and industry focuses on realizing an accurate and effective tracking system [7, 9, 10, 15,

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

IPSN ’19, April 16–18, 2019, Montreal, QC, Canada

© 2019 Copyright held by the owner/author(s). Publication rights licensed to ACM.

ACM ISBN 978-1-4503-6284-9/19/04. . . \$15.00

https://doi.org/10.1145/3302506.3310386

![](images/8eacf7ad4d197300e028128d7af5cba494c60d0969cab4931675f327e10aecf0.jpg)



![](images/718d016387551156d6056613ee2dbcf8809c281e5a3834bde37a6b440e9a2790.jpg)



![](images/7776bdb8c9232af23f6697af305ff5d7ede816ff5fd9a1dcbad51a6a0b1faa75.jpg)



![](images/6a12a389da1dcab141fcf5d5229042e38249ce861a8f1ef3cd72309ea6ec085a.jpg)



Figure 1: The application scenarios of tracking the 3D location and orientation

16, 21, 28]. Radio Frequency IDentification (RFID) is a promising solution for target tracking , due to its low cost, ease of deployment, and high efficiency of information gathering.

Previous RFID-based localization and tracking systems [8, 10, 15, 28] often rely on the signal phase information to calculate the distance between a reader and a tag. Compared to the received signal strength (RSS), the phase change between the transmitted and backscattered signals is a more reliable indicator of the reader-tag distance. Tagoram [28] and MobiTagbot [15] propose to calculate the probability of the target being at a certain position according to the received phases. Holographic methods are then used to probabilistically track the location of the target based on the probability.

In those phase-based tracking approaches, the distance is the main variable to affect the phase value, so the tracking is accurate when the orientation of the target does not change frequently or dramatically. However, the orientation of the tag relative to the reader’s antenna is a crucial factor that can significantly affect the received phase. Indeed, the phase change is jointly determined by the reader-tag distance and the tag’s orientation. Most of the existing approaches exploit the distance-phase model that overlooks the impact of the orientation change.

In practice, many targets need to be tracked with both location change and orientation change as shown in Fig. 1. For example, along conveyor belts, products move with frequent self-rotation and some operations will introduce extra rotation like rotating the product for labeling or painting at the specified sides. Gesture monitoring in the HCI applications often requires tracking at hand movements, which contain both location and orientation changes that need to be accurately tracked for recognition. Existing approaches [10, 15, 28] suffer large tracking errors with the distance-phase model and fail to provide both the location and orientation information in such scenarios.

It is also nontrivial to provide both location and orientation simultaneously in 3D space even if we propose a theoretical phase model quantifying the orientation effect. In 3D space, the same phase measurement can correspond to many different combinations of a tag’s location and orientation. When tracking a moving tag, the possible trajectories in terms of the location and orientation increase exponentially with the number of phase samplings. Existing approaches like holographic methods inevitably introduce heavy computational overhead, which makes it difficult to track the targets in real time.

In order to tackle the above problems, we face two main challenges. First, it is unclear how the 3D orientation will affect the phase change in the backscattered signal. To track the 3D location and orientation, we need a phase model that quantitatively shows the impact of the 3D orientation. Second, 3D tracking of both location and orientation will lead to much higher computational complexity when compared with 2D tracking. It will be challenging to design an algorithm that can efficiently find out the real location and orientation of a target.

In this paper, we propose 3D-OmniTrack, an approach to accurately track the 3D location and the orientation using commercial off-the-shelf (COTS) RFID systems.

• By analyzing the signal propagation and the polarization in the RFID systems, we first propose the polarization-sensitive phase model to explicitly quantify the respective impact of the reader-tag distance and the tag’s 3D orientation on the phase change.   
• We propose 3D-OmniTrack, a light-weight and accurate tracking approach based on the Multiple Hypotheses Tracking (MHT) framework. To the best of our knowledge, 3D-OmniTrack is the first approach that can simultaneously pinpoint a tag’s location and orientation in 3D space.   
• We implement 3D-OmniTrack on a COTS RFID platform. The experimental results demonstrate that OmniTrack achieves centimeter-level location accuracy with low orientation error.

The remainder of the paper is organized as follows. We discuss the related works in Section 2. Section 3 analyzes the phase change in typical RFID systems and presents the polarization-sensitive phase model. Then we propose the design of 3D-OmniTrack in Section 4. In Section 5, we discuss the initialization methods to reduce the computational complexity of 3D-OmniTrack and some practical issues concerning the applicability of the approach. Section 6 presents the implementation details and the evaluation results. We conclude the paper in Section 7.

# 2 RELATED WORKS

In this section, we survey the state-of-the-art tracking approaches classified into two main categories: traditional and RFID-based tracking approaches. We then discuss how 3D-OmniTrack differs from those methods.

# 2.1 Traditional Tracking Approaches

Traditional tracking approaches leverage visual clues, motion clues and etc. The proliferation of computer vision provides many different categories of tracking methods, e.g. visual tracking [12] and detect-to-track [23]. Motion clues provided by inertial sensors are also the common input of a tracking system [24, 30]. Arm-Track [17] estimates the 3D posture of the human arm by fusing the sensors’ data such as accelerator, gyroscope and compass, and reducing the searching space with the priori of arm’s rigid motion model. Apart from inertial sensors [2], acoustic sensors [20] and visible light sensors [31] in mobile devices are also utilized for millimeter-level tracking.

Computer vision based approaches naturally suffer from the problems of the non-line-of-sight (NLOS) blockage and the poor light condition, and often induce high computation overhead. Active sensor based approaches put strict requirements on the battery life and the deployment condition. Our RFID-based approach, 3D-OmniTrack, is less susceptible to the NLOS blockage and other environmental factors, and the passive RFID tag has great significance in practical usage due to its battery-free, low-cost and easyto-deployment characteristics.

# 2.2 RFID-based Tracking Approaches

RFID technology has been widely applied for target tracking [10, 25, 28, 29]. Most of the previous work can achieve high-accuracy tracking by analyzing the RSSI and phase readings. However, those approaches consider the location tracking and the orientation tracking separately.

Early location tracking approaches leverage RSS fingerprinting [13, 22] and ranging [3, 32], which are sensitive to the environmental dynamics and signal interferences. They struggle to achieve the fine-grained localization. Recent approaches rely on the phase measurements for high-accuracy location tracking. BackPos [10] exploits the phase differences to calculate the distance differences between the target to three antennas. Then the location of the target is pinpointed at the intersection of the hyperbola defined by any two antennas. Tagoram [28] builds a differential augmented hologram to estimate the probabilities of the tag’s existence on the 2D surveillance plane. MobiTagbot [15] constructs multiple virtual antennas to improve the localization accuracy of the hologram for multiple tags by introducing a moving RFID reader. However, those phase-based tracking approaches, that either exploit the geometric relationship or holographic methods, suffer in performance when the target changes the orientation frequently and dramatically. Our approach on the other hand can still maintain the high accuracy when the target has both location and orientation change.

Apart from leveraging phase values, RFind [11] achieves subcentimeter accuracy of 3D localization by measuring the time-offlight (ToF). It emulates a 220 MHz virtual localization bandwidth to reduce the error when shifting the signal frequency. Those approaches rely heavily on dedicated devices to obtain extra information for the location inference, which is expensive and hard to deploy at large scale.

For orientation tracking, RF-3DScan [5] estimates the 3D angle of tagged objects by calculating the phase difference during the linear movement of the reader’s antenna. Tagyro [21] tracks the 3D rotation of a tagged object by exploiting the phase differences of two groups of RFID tags. During the tracking process, the location of the object must stay unchanged. Those orientation tracking approaches always assume that there is no location change of the target so that the phase change is solely caused by the orientation change. In our approach, we don’t make that assumption, 3D-OmniTrack can provide both location and orientation in 3D space.

OmniTrack [8] is the first RFID system to track a tag’s location and orientation simultaneously. In OmniTrack, the authors derive an orientation-aware phase model by measuring the linear relationship between the tag polarization and the phase change, and leverage it to achieve high-accuracy tracking in the 2D plane. This phase model can only suit the movement in well-defined 2D space and can’t generalize to the 3D space, which is the focus of our work.

3D-OmniTrack outperforms those previous techniques because we model the polarization effects on RFID phase readings, derive the polarization-sensitive phase model, and prototype a system that can simultaneously track the location and orientation of one single tag in the 3D plane with high accuracy.

# 3 THEORETICAL FOUNDATION

# 3.1 Traditional Phase Model for RFID Systems

In RFID systems, the reader queries the RFID tags by transmitting a constant single-tone carrier wave. The tag modulates its information on the carrier signal and backscatters it back to the reader. The received phase is then calculated as the phase difference between the transmitted and the received signals. We use $\phi$ to denote the received phase and in a traditional phase model, it is expressed as follows:

$$
\left\{ \begin{array}{l} \phi = \left(\frac {2 \pi}{\lambda} \times 2 d + \delta\right) \mod 2 \pi \\ \delta = \phi_ {T x} + \phi_ {R x} + \phi_ {T a g} \end{array} \right. \tag {1}
$$

d refers to the reader-tag distance and $\phi _ { T x } , \phi _ { R x }$ , and $\phi _ { T a g }$ are the phase changes introduced by the reader’s transmitter, the tag, and the reader’s receiver circuit. λ is the wave length of the signal. $\phi _ { T x }$ and $\phi _ { R x }$ are the constants that are only related to the hardware circuits. In the traditional phase model, $\phi _ { T a g }$ is commonly treated as a constant or the random noise.

The change in the received phase is considered to be solely affected by the distance change and the traditional phase model is generally used for localization or tracking in the previously proposed works. However, from our experiments, we find that the empirical results deviate from this model and it turns out that the orientation of the tag can actually affect the phase difference. Fig. 3 shows the phase change with the tag’s orientation. In this example, we fix the reader-tag distance and the tag is placed in parallel to the antenna plane of the reader. We rotate the tag for one cycle $( 3 6 0 ^ { \circ } )$ along the axis defined by the line connecting the centers of the antenna and the tag. It can be observed that the phase changes for 2π .

# 3.2 The Polarization Effect on the Phase

The effect of the tag’s orientation on the phase provides the opportunity for tracking the tag’s orientation with just a single tag. We observe that there is indeed relationship between the tag’s orientation and the received phase by the reader. It is natural to ask why the tag’s orientation can affect the phase and how the phase is related to the orientation. This phenomenon is actually caused by the polarization.

![](images/2e47fbb2a61de6100cb3256d2fbb7ac1f825f09b48a7901aa915aa63f20d2678.jpg)



Figure 2: Polarization

Polarization is an important parameter of RF antennas and electromagnetic waves. For the electromagnetic wave, the polarization refers to the direction in which the electric wave vibrates. Fig. 2 shows an example of an electromagnetic wave. The electric wave vibrates at the X-Y plane and the wave is polarized in X-Y plane. The polarization of an antenna similarly refers to the direction of the electric field of the radio waves it radiates. Therefore, in order to maximize the RSS of the received signals, we will generally match the polarization of the antennas and the signals.

In an RFID system, the polarization of the antennas can be classified into two categories: linear polarization and circular polarization. The electric field of the linear polarization maintains a single direction. For circular polarization, the electric field keeps changing like a clock in a plane as shown in Fig. 2. As mentioned before, most RFID antennas in the reader are circularly-polarized so as to match different tags’ polarized directions.

In our experiments, although we keep the transmitted signals and the tag’s location unchanged, the polarized direction of the tag is continuously changing, so the phase offset will be different when the tag’s orientation changes.

# 3.3 Polarization-sensitive Tag Phase Model for RFID Systems

In order to find the deterministic relationship between the phase and the polarized direction, we theoretically analyze the signal propagation in an RFID system. As show in Fig. 4, we abstract the circularly-polarized reader antenna to two orthogonal-placed linearly-polarized antennas. The signals fed to the two antennas have π /2 phase offset, which form the circularly-polarized electromagnetic waves.

In Fig. 5, we illustrate the signal propagation from the circularlypolarized antenna to the linearly-polarized tag. We denote the directional vectors of the two orthogonal antennas as u and v. The tag’s polarized direction is denoted as w. The signal sent by

![](images/c3cc76cb9b06e0ab8cd889fd409c7417297e03bef93af6f1ea2ab34418449349.jpg)



![](images/61fd4f383917654392d99d8c7e517075a88be5bfc82391ee5f801e659458c11f.jpg)



![](images/d564c1a7ab57a1e9e0a19aa01f23131ac29d0d2d70b60a79b349da187fb20f94.jpg)



Figure 3: Phase changing with rotation Figure 4: Circularly-polarized antenna   
Figure 5: RFID signal propagation

the reader will be:

$$
S (t) = u c o s (k t) + v c o s (k t - \pi / 2) = u c o s (k t) + v s i n (k t) \tag {2}
$$

When the signal arrives at the tag’s location, the signal will be:

$$
\left\{ \begin{array}{l} S ^ {\prime} (t) = S (t - t _ {d}) = u \cos (k t - \phi_ {d}) + v \sin (k t - \phi_ {d}) \\ \phi_ {d} = 2 \pi d / \lambda \end{array} \right. \tag {3}
$$

The signal induced by the electromagnetic waves will be the projection of $\mathbf { \boldsymbol { S } } ^ { \prime } ( t )$ onto the tag’s polarized direction w. So the signal reflected by the tag will be:

$$
S ^ {\prime \prime} (t) = (u \cdot w) c o s (k t - \phi_ {d} + \phi_ {t}) + (v \cdot w) s i n (k t - \phi_ {d} + \phi_ {t}) \tag {4}
$$

$\phi _ { t }$ is the phase offset caused by the tag’s hardware. Then $S ^ { \prime \prime } ( t )$ will propagate back to the reader’s antenna and will induce the signal at each linear antenna.

$$
\left\{ \begin{array}{l} S _ {u} (t) = S ^ {\prime \prime} (t - t _ {d}) \cdot u \\ \quad = (u \cdot w) ^ {2} \cos (k t - 2 \phi_ {d} + \phi_ {t}) \\ \quad + (u \cdot w) (v \cdot w) \sin (k t - 2 \phi_ {d} + \phi_ {t}) \\ S _ {v} (t) = S ^ {\prime \prime} (t - t _ {d}) \cdot v \\ \quad = (u \cdot w) (v \cdot w) \cos (k t - 2 \phi_ {d} + \phi_ {t}) \\ \quad + (v \cdot w) ^ {2} \sin (k t - 2 \phi_ {d} + \phi_ {t}) \end{array} \right. \tag {5}
$$

The signals from two linear antennas will finally merge into the signal $R ( t )$ received by the reader. Based on the abstraction of the reader antenna, there will be $\pi / 2$ phase offset incurred in the signal $S _ { v } ( t )$ . So the received signal R(t ) will be:

$$
\left\{ \begin{array}{l} R (t) = S _ {u} (t) + S _ {v} (t - \Delta t) \\ \quad = \cos (k t - 2 \phi_ {d} - \phi_ {t} - \phi_ {r} - \phi_ {o}) \\ \tan \phi_ {o} = \frac {2 (u \cdot w) (v \cdot w)}{(u \cdot w) ^ {2} - (v \cdot w) ^ {2})} \end{array} \right. \tag {6}
$$

where $\phi _ { t }$ and $\phi _ { r }$ correspond to the phase offsets caused by the hardwares of the tag and the reader antenna.

From Eq. 6, we can derive our phase model as:

$$
\left\{ \begin{array}{l} \phi = (\frac {2 \pi}{\lambda} \times 2 d + \delta) \mod 2 \pi \\ \delta = \phi_ {o} + \phi_ {t} + \phi_ {r} \\ t a n \phi_ {o} = \frac {2 (u \cdot w) (v \cdot w)}{(u \cdot w) ^ {2} - (v \cdot w) ^ {2})} \end{array} \right. \tag {7}
$$

$u , v ,$ w are the unit directional vectors of the reader antenna and the tag. Different from the traditional phase model shown in Eq. 1, our polarization-sensitive phase model explicitly takes into account the 3D orientation of the tag.

![](images/9762024cca4b19fe8734086d0ac50df1bf33fd161f8308ae6f2952c6a4f1b6c0.jpg)



(a) incline angle = 0◦

![](images/b362aac271843936f6b32b77cbd671a7e937140f690814428718d08552cf2cee.jpg)



(b) incline angle = 15◦

![](images/130aa56d428d7e05f3833dbba8fe2a79f15f94bbbf3ef508ca36ea80648178b5.jpg)



(c) incline angle = 45◦

![](images/5feaf803d2b091c9bfeea8de9d55f75146967e4e87cac53c075582aa3c29a199.jpg)



(d) incline angle = 60◦   
Figure 6: The comparison between the real phases and the predicted phases.

# 3.4 Phase Observations in Practice

Although we have theoretically derived the phase model, it is still an important question whether this model matches the received phases in real experiments. In order to validate the model, we conduct a series of experiments to show the comparison between the real phases and the theoretical ones. In our experiments, we fix the distance between the antenna and the tag and rotate the tag for one cycle with different incline angles of the tag (the angle between the tag’s polarized direction and the reader’s antenna plane).

The results are shown in Fig. 6. We can observe that the change pattern of the theoretical phases with our phase model can match the phases collected from real experiments. The overall shift between the theoretical phases and the real phases is actually caused by the unknown hardware phase offsets $\phi _ { t } , \phi _ { r }$ in the phase model. Therefore, we can conclude that our phase model can explain the phase changes in the RFID systems correctly.

# 4 TRACKING IN 3D SPACE

Our phase model proves that both the changes of the tag’s orientation and location can be calculated quantitatively, which is the cornerstone of our tracking system: 3D-OmniTrack. Before diving into the details of the algorithm, we first present the overview of 3D-OmniTrack in Fig. 7.

3D-OmniTrack consists of three main parts. The first part is the Information Collection Module. We design the reader’s antenna to be a combination of three circularly-polarized antennas. The three antennas are placed together as shown in Fig. 7 so as to cover the movement of the object in 3D space.

![](images/81c21e62c53509d3aaa726838c12cf764d348442d60c0cf9e30b72cf7d902e14.jpg)



Figure 7: Overview of 3D-OmniTrack

The second part is the Initialization Module, which can provide the system with the initial location and the orientation to reduce the computational complexity of the 3D tracking. This module takes into consideration the different constraints under various situations and incorporates different initialization methods to satisfy different requirements.

The third part is the 3D Tracking Module. In this module, we adopt Multiple Hypotheses Tracking (MHT) [1] approach to estimate both the location and the orientation of the target. We will infer the possible locations and orientations of the target based on its current state of the tag. Then the phases and the RSS observed by the antennas will be exploited to calculate the probabilities of different target’s movements. At the end of tracking, we will select the moving trajectory with the highest probability as the output of 3D-OmniTrack.

# 4.1 3D coordinate system

In order to track the location and orientation changes in 3D space, it is important to build an appropriate coordinate system that can represent the location and orientation of the target. In 3D-OmniTrack, our coordinate system is based on the view of the reader antennas. We define the plane of the top antenna as the X-Y plane and the axis parallel to the ground as the X axis, as shown in Fig. 8. Y axis is orthogonal to the X axis and Z axis is orthogonal to the X-Y plane. The positive directions of the axis satisfies the righthanded coordinate system. Actually we can deploy the antenna in many different ways. The antenna deployment is further discussed in Section 5.

We can now define each unit directional vector (u,v in the phase model) of the antennas and the directional vectors of the tag based on the coordinate system. All the three v vectors point to the positive direction of Y axis (0, 1, 0) and the u vector for the upper

![](images/0aac430783a4ab42bbc930704d06937c9f2082836b82b18c21879c2b21df1c23.jpg)



Figure 8: Coordinate system of 3D-OmniTrack

antenna points to the positive direction of X axis (1, 0, 0). The u vectors of the lower two antennas are in the X-Z plane and in our setup, the two vectors are $( \frac { \sqrt { 2 } } { 2 } , 0 , \frac { \sqrt { 2 } } { 2 } ) , ( \frac { \sqrt { 2 } } { 2 } , 0 , - \frac { \sqrt { 2 } } { 2 } )$ , .

# 4.2 Tracking the location and the orientation

MHT is a commonly-used tracking approach that lends itself well to our problem. Although we have a quantitative phase model, the same phase change can still correspond to multiple combinations of the location and orientation changes in 3D space. MHT is beneficial because it will treat all the combinations as valid current states and maintain multiple hypotheses about the trajectories from all these states. A pruning method can then be used to eliminate impossible hypotheses during the tracking. At the end of tracking, the remaining hypothesis with the highest probability is treated as the real trajectory of the target. Since we consider all the combination of the 3D location and orientation, the computational complexity will be high, making it important to design the algorithm in a time-efficient and effective manner.

In 3D-OmniTrack, the tracking space is divided into $L \times W \times H$ grids at cm level. For each grid, we use its centroid as its coordinate. The state inference in MHT treats all the neighbor grids of the current grid as the next possible locations. The phase model is then exploited to calculate the likelihood of the possible locations being the real next position of the target’s movement. However, a group of phase measurements can correspond to many different locations, which result in many fake candidates with high probabilities. In 3D-OmniTrack, by taking the advantage of our phase model, the orientation change is also exploited to estimate the probability of the next location.

Suppose the current location of the tag at sample i is $\boldsymbol { p } _ { i } ^ { t }$ and the orientation of the tag is $o _ { i } ^ { t } ,$ , we have the phase readings from the three antennas as:

$$
\left\{ \begin{array}{l} \phi_ {i} ^ {\text {   ant }} = (\frac {4 \pi}{\lambda} \times \text { dist } (p _ {i} ^ {t}, p ^ {\text {   ant }}) + \delta) \mod 2 \pi \\ \delta = \phi_ {o _ {i}} + \phi_ {t} + \phi_ {\text {   ant }} \\ \tan \phi_ {o} = \frac {2 (u ^ {\text {   ant }} \cdot o _ {i} ^ {t}) (v ^ {\text {   ant }} \cdot o _ {i} ^ {t})}{(u ^ {\text {   ant }} \cdot o _ {i} ^ {t}) ^ {2} - (v ^ {\text {   ant }} \cdot o _ {i} ^ {t}) ^ {2}} \end{array} \right. \tag {8}
$$

The superscript ant = 1, 2, 3 denotes the identifier of the reader antennas and $u , v$ are the two unit directional vectors of an antenna.

We then track the next possible location of the target based on the consecutive phase readings from the three antennas. Since the location change is continuous, we just need to check the neighbor grids around the current location. In 3D-OmniTrack, the grids inside a cube of length $S _ { l }$ that centers the current location are considered as the next candidate locations, as shown in Fig. 9. For example, if the sampling rate of the reader is low, we will treat all the grids adjacent to the current grid as the candidate next locations, which will be $3 \times 3 \times 3 = 2 7$ grids. It is worth noting that we also consider the current location since there exits only rotation of the target without any location changes.

![](images/ed23457a914329cca2a54e3559b327226f41f78311a82d6355bcbde0aa153175.jpg)



Figure 9: Neighbor locations Figure 10: Neighbor orientations

The window size is set based on both the sampling rate of the reader and the moving speed of the target. If the target has a higher speed and the sampling rate is low, we will enlarge the window size. While the target has a low speed and the sampling rate is very high, it will be useless to set a large window since most grids in this window will have the low probabilities to be the next location.

Although we can select the window size, it is obvious that we can’t just let the number of the candidates unboundedly grow. In 3D-OmniTrack, we will rely on the probability of the orientation calculated at each candidate location to eliminate the impossible candidates.

# 4.3 Candidate Generation

In the candidate location, we have the phase valu e ϕ a n t $\phi _ { i + 1 } ^ { a n t }$ and subtract it with $\phi _ { i } ^ { a n t }$ for all the antennas. The phase difference will be:

$$
\Delta \phi_ {i} ^ {a n t} = (\frac {4 \pi}{\lambda} \times (d i s t (p _ {i + 1} ^ {t}, p ^ {a n t}) - d i s t (p _ {i} ^ {t}, p ^ {a n t})) + (\phi_ {o _ {i + 1}} - \phi_ {o _ {i}})) \tag {9}
$$

Here, we remove the modulo operator. We can assume the moving of the target is consecutive so that the phase change between adjacent samples won’t exceed 2π . We will unwrap the phase values based on the rules below:

$$
\Delta \phi_ {u n w r a p} = \left\{ \begin{array}{l l} \Delta \phi , & | \Delta \phi | \leq \pi \\ \Delta \phi + 2 \pi , & \Delta \phi <   - \pi \\ \Delta \phi - 2 \pi , & \Delta \phi > \pi \end{array} \right. \tag {10}
$$

After the unwrapping, the phase change is constrained within $[ - \pi , \pi ]$ to avoid the ambiguity. In Eq. 9, the phase change corresponding to the distance change can be calculated since we know the location of the previous sample and the candidate. The hardware-dependent phase offset is also cancelled out due to the same antenna for the phase measurements. The tag’s previous orientation $o _ { i } ^ { t }$ is known to us so we can derive the phase change $\Delta \phi ^ { a n t }$ corresponding to the current orientation $o _ { i + 1 } ^ { t } = ( x _ { i + 1 } , y _ { i + 1 } , z _ { i + 1 } )$ .

![](images/78cd66d01aa133d43a0a80b73518851492a830c7b440c5cf79a5435bb20a6ff4.jpg)  
Figure 11: Probability distribution of possible tag movements

$$
\arctan \phi_ {o _ {i + 1}} ^ {a n t} = \frac {2 (u ^ {a n t} \cdot o _ {i + 1} ^ {t}) (v ^ {a n t} \cdot o _ {i + 1} ^ {t})}{(u ^ {a n t} \cdot o _ {i + 1} ^ {t}) ^ {2} - (v ^ {a n t} \cdot o _ {i + 1} ^ {t}) ^ {2})} \tag {11}
$$

Unfortunately, it is hard to directly derive the current orientation $o _ { i + 1 } ^ { t }$ . The equations like Eq. 11 will involve square operations so that only three equations from three antenna are not enough for calculating the current 3D orientation.

In 3D-OmniTrack, instead of calculating the 3D orientation, we calculate the theoretical phase change based on all the neighbor orientations relative to the previous orientation as shown in Fig. 10. We consider this to be reasonable because the moving of the target is consecutive and the instant change of the orientation between two samples is limited. In Fig. 10, we consider the window size of the orientation change to be $S _ { o } \times S _ { o } .$ . In practice, the size of the window is decided by the application and the sampling rate of the devices.

Fig. 11 presents an example of the probability distribution for all the possible candidates. In this example, we only rotate the target with a certain angle. 9 neighbor orientations and 27 neighbor locations are considered and the differences between the theoretical phase change and the real phase change are calculated. The candidate with only angle change in the lower left corner has the smallest difference and is the correct next state of the tag. The probability is calculated as:

$$
\operatorname{prob} _ {\text { loc,   orien }} = \left| \sum^ {K} e ^ {j \left(\Delta \phi_ {\text { real }} - \Delta \phi_ {\text { theoretical }}\right)} \right| / K \tag {12}
$$

K is the number of antennas. Now, we are able to calculate the theoretical phase changes based on different combination of the location and the orientation. The difference between the theoretical values and the real values will be exploited as the indicator of how likely the combination is the real current 3D location and the orientation of the target.

Compared with holographic methods, our approach constrains the searching area to a constant size centered at the current state. Holographic methods require to compute all the $n ^ { 3 } m ^ { 3 }$ combinations of the location and orientation, where n is the searching size at each space axis and m is the searching size at each angle axis.

# 4.4 Candidate Pruning

The random noise introduced by the hardware may lead to multiple candidates with high probabilities. In Fig. 11, we can observe other combinations with higher probabilities even if the number of them is small due to the constraints of three antenna. We set up a threshold γ to limit the number of the candidates.

![](images/912c10e522e2d258dd3bfecc780785415fe36bbed548d54bf0ccc779b7a5c469.jpg)



Figure 12: The tracking of the target’s movement

However, in MHT, if we keep tracking of all the possible candidates every iteration, it will be computationally intractable. In such scenarios, we will exploit changes in RSSI to help eliminate impossible candidates. Although RSSI is not a reliable for accurate tracking, it can reflect the trend of the tag’s movement to some extent especially when the orientation changes. When the angle between the tag’s orientation and the antenna plane approaches 90◦, the phase readings will drop sharply. Fig. 13 presents the RSSI values when we rotate the tag to point at the antenna.

Although RSSI is not sensitive to the distance change, it can reflect the trend of the change. We continuously move the tag away from the antenna and the received RSSI is shown in Fig. 13. When applied with an average filter for smoothing, the RSSI can reflect the distance change between the tag and the reader. Therefore, RSSI can serve as an indicator to eliminate those candidates who have abnormal RSSI changes.

In 3D-OmniTrack, we will trigger pruning every N times of the candidate generation and compare the RSSI change from all three antennas so that we can cut off some impossible hypotheses on the trajectory. The whole process of pruning is described in Fig. 12. Each red circle represents a target state (location, orientation) and each arrow line represents a hypothesis on the next target state. With pruning, we can eliminate those impossible hypotheses denoted with red crosses and the yellow hypothesis is left as the right trajectory of the target.

At the end of tracking, we will select the trajectory with the highest probability as the output of our approach.

# 5 PRACTICAL ISSUES IN 3D-OMNITRACK

In this section, we discuss the important issues to make 3D-OmniTrack practical.

# 5.1 Initialization

It is important to accurately seed the system with an initial localization and orientation in order to reduce the search complexity.

![](images/e3ead5d2144c273cff3b84c917bf1a81676a1be36f1013e0dece62c0e1f82821.jpg)



(a) RSS changing when the angle changing (b) RSS changing when the distance changing   
![](images/bf8a993baa254438fdc6e87dbf4e541d345a89b56b7a48d3aac3cd4cd560dbb5.jpg)



Figure 13: RSS changing pattern

The intuitive method for initialization is to search all the combinations of the location and orientation in our surveillance space. However, suppose we have a 1m × 1m × 1m space and search all orientation with 3◦ granularity, it will calculate 1012 combinations to determine the exact initial location and orientation. This is quite time-consuming and can’t work in some scenarios. In order to reduce the time for initialization, we provide three different methods in different situations. Due to the page limit, we omit the details of each method and only describe the main working mechanism. Nevertheless, the brute-force method can still be exploited as a backup method.

Initialization with multiple frequencies: We can adopt the multiple frequencies for initialization. The method is based on the distance-phase model and it can be transformed to:

$$
\phi = \frac {4 \pi d}{c} f \tag {13}
$$

The phase is linearly related to the carrier frequency. Therefore, if we have the phase readings from different carriers, we can use the phase difference to estimate the distance between the tag and the reader. In our system, we have three antennas to determine the location of the antenna and then we can easily search for the proper orientation based on the phase difference between three antennas. The accuracy of multi-channel method is largely determined by the frequency gap of the channels, so we may require a large frequency gap for higher accuracy.

Initialization with rotations: In HCI or industrial scenarios , it is reasonable to calibrate the system with the predefined movements like rotations. We can rotate the target for one cycle before the tracking to initialize the system. When rotating the target, the location stays unchanged so phase change corresponding to each antenna is only caused by the orientation changes. Based on the polarization-sensitive phase model, the phase change with the rotation angle and the incline angle between the tag and antenna is shown below:

$$
\phi = \arctan (\tan \theta / \cos \theta) \tag {14}
$$

θ is the rotation angle of the tag. We can pre-generate all the phase changes corresponding to different incline angles, then compare the real phase trace with generated ones to determine the incline angle. The orientation can be easily determined based on our phase model. Then we search the space for the location based on the phase difference between antennas.

Initialization with linear movements: For industrial scenarios such as conveyor belts, we can assume the target moves linearly for initialization. When the target moves linearly along the belts, the phase reading reaches its lowest as the moving direction is perpendicular to the line connecting the target and the antenna. We can record this phase value $\phi _ { s }$ and the phase corresponding to any other position $P$ along the trajectory as $\phi _ { e } .$ Since the linear movement incurs no orientation change, the phase difference $\phi _ { e } - \phi _ { s }$ can be used directly to calculate the distance difference ∆d. With the moving distance $d _ { t }$ of the target, we can calculate the distance from the antenna to position P as: $\frac { d _ { t } ^ { 2 } + \Delta d ^ { 2 } } { 2 \Delta d }$ . Similarly, we can obtain the distances from P to all three antennas in order to pinpoint the location of the target at P . Finally, the orientation can be obtained by searching the possible orientations based on the phase differences between the antennas.

# 5.2 Antenna deployment

3D-OmniTrack has no additional constraints on the relative location between three antennas as long as the antennas are located at different planes. Therefore, there are alternative ways to deploy the antennas. For example, we can deploy the three antennas that are orthogonal to each other in the surveillance area. The antenna deployment in Section 4.1 is convenient since the antennas are placed together and it is easy to measure the relative locations and directional vectors of the antennas.

It is also possible to track the location and orientation more accurately by increasing the number of antennas. In this paper, we demonstrate that three antennas are enough for tracking the location and orientation. Additional antennas can be exploited in our tracking algorithm to improve the overall performance as long as the locations are known.

# 5.3 The Multi-path Effect

The multi-path effect is a common problem in RF-based localization and tracking since it directly interferes with the signal propagation. The line-of-sight signal may be entangled by the multi-path signals to affect the phase calculation at the reader’s hardware. Therefore, the actually received phase will be much different from the theoretically derived one. In our approach, there are two methods to mitigate the multi-path effect: 1) By examining the application scenarios for our approach, we can deploy the antennas at appropriate positions to reduce the multi-path effect. For example, we can deploy the antennas close to the conveyor belts to ensure the line-of-sight propagation. We can also deploy the antennas on the ceiling to avoid the signal blockage by our body in the HCI applications. 2) The number of antennas exploited in our approach is not limited to three so the multi-path effect may be mitigated by increasing the number of antennas. As stated in MobiTagbot [15], the phase readings distorted severely by the multi-path effect can be recognized by channel hopping. With many antennas, we can select the phase readings from the antennas with less interference to track the target.

# 6 EVALUATION

# 6.1 Implementation

This section presents the implementation details and evaluation results. We implement 3D-OmniTrack on COTS devices. Then we compare it with the state-of-the-art approaches under different experimental settings.

![](images/ee44007d9d4845e795641c7f7e05fd310d69014c43b4452f1ebb44a1c85d47ca.jpg)



Figure 14: Experimental Setup

In our experiment, we use an ImpinJ Speedway R420 RFID reader, three Laird S9028PCL circularly-polarized antennas, and Alien UHF passive RFID tags. The software is implemented using C#. In the lab experiments, we run the software at a MSI desktop PC equipped with i7 6700 CPU at 2.6GHz and 8G memory. The rotator to simulate the orientation change supports 720◦ rotation around two axes. The rotating speed is controllable in our experiments.

Methodolgy: The experiment setup is shown in Fig. 14. We build a 3D rail that supports the moving along three axes with a controllable speed. The three antennas are place as we mentioned in Section 4. The upper antenna is placed parallel to X-Y plane and the lower two antennas are placed symmetric along the Y-Z plane with the intersection angle of 90◦. The size of the moving area is 1.5m × 1.5m × 1.5m. We attach a tag onto the automatic rotator and set different speeds of the rotator to rotate along two axes, then we fix the rotator to the 3D rail.

We evaluate the performance of tracking in terms of the localization error and the orientation error. The ground-truth location of the target is calculated according to the moving speed of the target and the geometric property of the rails. The ground-truth orientation is acquired based on the speed of the rotator and the preset rotating mode.

We compare 3D-OmniTrack with the state-of-the-art approaches: Tagoram [28] and OmniTrack [8]. Tagoram assumes the prior knowledge of the rails so as to emulate virtual antenna arrays. OmniTrack and 3D-OmniTrack require no prior knowledge, but the former one can only work in 2D scenarios. We implement the three approaches with the same hardwares. We also evaluate Tagyro [21], an approach to track the 3D rotation without location changes. 3D-OmniTrack can track both the 3D orientation change and the 3D location change.

# 6.2 Overall performance

We first evaluate the performance on the rail shown in Fig. 14. The target is set to move along the edge of a cube and finally move back to the start point. The rotator is set to rotate along two axes with different speeds.

![](images/ca5ae0e0342ae8c993185f3c0bc152f464a2e843ba81cb667ff01e6fdfa8967f.jpg)



(a) v=0.1m/s

![](images/89972ab9c5b0a528547897725de7a6ffbbab80852fd6675f2718c3259940927f.jpg)



(b) v=0.2m/s

![](images/2148d2cf80866a874804b77c4ec596609afffb4feab657b7e79178fef50b1252.jpg)



(c) v=0.25m/s

Figure 15: Location error without rotation in 3D space   
![](images/e9bd4c2998e5ac18ca557f6ab4aa92d63ee08bbec85fa4090af2a0b996989053.jpg)



(a) rotating speed = 10◦/s

![](images/0a4951dd0e72ec671b5da4ba2e52691b728b1a88c6d7b2ffdd62a64df9e758fb.jpg)



(b) rotating speed =15◦/s

![](images/1fe579e8514e47979c180cad828a3ca4398fa29f65c44fe1d1254f40b855f0fe.jpg)



Figure 17: Orientation error with rotation in 3D space   
Figure 16: Location error with rotation in 3D space

In this experiment, the target’s moving speeds are set to three levels: $( 0 . 1 m / s , 0 . 2 m / s , 0 . 2 5 m / s )$ . The rotating speeds are set to No Rotation, $1 0 ^ { \circ } / s$ and $1 5 ^ { \circ } / s$ . We repeat the experiments 5 times for each combination of the moving and rotating speeds. The average location errors of 3D-OmniTrack and Tagoram are shown in Fig. 15 and Fig. 16.

We first disable the rotator and the results are shown in Fig. 15. When the target moves at $0 . 1 m / s$ , the average location errors of Tagoram and 3D-OmniTrack are 5.8cm and 4.3cm. When the speed is $0 . 2 m / s ,$ the average location errors of Tagoram and 3D-OmniTrack are 6.7cm and 5.1cm. When the speed is 0.25m/s, the average location errors are 7.3cm and 5.5cm respectively. The two approaches suffer accuracy degradation because as the speed increases, the phase samplings over a fixed distance decrease. Since the three antennas are actually used to transmit the signals in turn, the phase samples for calculating the probability are not from the same time, which leads to the accuracy degradation. The performance of 3D-OmniTrack is slightly better than Tagoram because Tagoram don’t know the trajectory of the target in order to simulate the virtual antenna arrays. The tag’s orientations relative to the three antennas are different, which also leads to the performance degradation in Tagoram.

Then we enable the rotation in the target and the results are shown in Fig. 16 When we set the rotating speed to $1 0 ^ { \circ } / s$ . The average location errors of Tagoram and 3D-OmniTrack are 9.1cm and 5.3cm, 11.5cm and 6.6cm, 12.8cm and 7.1cm corresponding to the moving speeds $0 . 1 m / s , 0 . 2 m / s , 0 . 2 5 m / s$ . The results demonstrate apparently that the accuracy of Tagoram degrades severely. From the CDFs of the localization error of Tagoram, we can observe that the maximum localization error can approach nearly 20cm, making it unreliable in practice. The reason behind the poor performance of Tagoram is the impact of the orientation change. As mentioned in Section 3, the orientation change can lead to the maximum phase change of 2π that corresponds to about 30cm in the distance estimation. Tagoram is unable to deal with the explicit orientation change while 3D-OmniTrack maintains the centimeter-level accuracy due to the polarization-sensitive phase model.

When we change the rotating speed to $1 5 ^ { \circ } / s ,$ we can observe the same results between Tagoram and 3D-OmniTrack. The average location errors are 9.5cm and 5.7cm, 11.4cm and 7.2cm, 13.8cm and 7.7cm with three moving speeds respectively.

# 6.3 Performance in 2D space

It is actually inconvenient to compare the performance of 3D-OmniTrack in terms of both the localization error and the orientation error since we can’t find existing works that simultaneously track the location and the orientation in 3D space. Therefore, we can only evaluate the localization accuracy and the orientation accuracy separately. In 2D space, OmniTrack can indeed be compared with our work in both localization and orientation tracking. We make the target move in the X-Y plane to form a square with three speeds $0 . 1 m / s , 0 . 2 m / s , 0 . 2 5 m / s$ and set the rotator to rotate along the Z axis since OmniTrack can only support the rotation in 2D space. The rotation speed is set to three levels $0 ^ { \circ } / s , 1 0 ^ { \circ } / s , 1 5 ^ { \circ } / s$ .

Fig. 18 presents the results. When there is no rotation, we can observe that the localization accuracies of OmniTrack and 3D-OmniTrack are 4.8cm and 4.3cm, 5.5cm and 4.6cm, 5.7cm and 4.9cm corresponding to the moving speeds 0.1m/s, 0.2m/s, 0.25m/s. 3D-OmniTrack can achieve a slightly better performance due to the three antenna and the polarization-sensitve phase model. Omni-Track assumes the linear relation between the orientation and the phase, which can introduce the error, because the linear relationship is the special case when the tag is placed parallel to the antenna plane as metioned in Section 3,. 3D-OmniTrack can take the advantage of the accurate phase model to improve the accuracy.

![](images/adf548cdcdd5088a6d70996ced7d84d7f3289d71213c691cca424d963a143c9c.jpg)



(a) rotating speed =0◦/s

![](images/8e8982cbbc559b938e239941d79d245a8e01260987e50d52e75856e8b2ad5625.jpg)



(b) rotating speed =10◦/s

![](images/1363861dbe6536b3ec717d280819b0fb32cc9d321ff73c926cfe2c2bf6ed2279.jpg)



(c) rotating speed =15◦/s

Figure 18: Location error in 2D space   
![](images/ea8bf67790736b2d2572462482f7a1c22ab0ef6f323724171e9d2567fa1cc1c3.jpg)



(a) rotating speed =0◦/s

![](images/0f3e67453a9116f3de03dd6151fcb194fc8161ca87739f8bcc79b5080e833b3b.jpg)



(b) rotating speed =10◦/s

![](images/eb1fb59dbfa8c79af38aed572b984fb07712c812bca341bc0ba4609620c1a418.jpg)



(c) rotating speed =15◦/s   
Figure 19: Orientation error in 2D space

When there are rotations with $1 0 ^ { \circ } / s ,$ the localization errors of OmniTrack and 3D-OmniTrack are 6.2cm and 5.3cm, 6.8cm and $5 . 5 c m ,$ 7.1cm and 6.0cm corresponding to the increasing moving speeds. 3D-OmniTrack has better performance due to the more accurate phase model. In the rotation scenario, the linear relation fails to hold so that OmniTrack has worse performance. When the rotation speed is $1 5 ^ { \circ } / s ,$ , we observe that 3D-OmniTrack outperforms OmniTrack by 1.2×, 1.25×, 1.23× respectively with different moving speeds.

# 6.4 Accuracy of Orientation

When we move and rotate the target on the 3D rails with three different speeds, the performance of 3D-OmniTrack in terms of the orientation is shown in Fig. 17. With the rotating speed of $1 0 ^ { \circ } / s ,$ the average orientation errors of 3D-OmniTrack are $5 . 8 ^ { \circ } , 6 . 9 ^ { \circ }$ and $7 . 5 ^ { \circ }$ corresponding to the three levels of moving speeds: 0.1m/s, 0.2m/s, 0.25m/s. With the rotating speed of ${ 1 5 } ^ { \circ } / s ,$ , the average orientation errors of 3D-OmniTrack are $6 . 5 ^ { \circ } , 7 . 9 ^ { \circ }$ and $9 . 3 ^ { \circ }$ when we increase the moving speed. The performance of 3D-OmniTrack can degrade when we increase the moving speed and the rotating speed. It is reasonable since the increase of the speed will cause the decrease of the sampling rate and it will lead to the higher orientation error. The overall orientation errors are all below $1 0 ^ { \circ }$ , which is acceptable in 3D space with both moving and rotating.

In 2D situations, we present the orientation errors of 3D-OmniTrack and OmniTrack in Fig. 19 when the rotating speed is $1 0 ^ { \circ }$ , the average orientation errors of 3D-OmniTrack and OmniTrack are $4 . 3 ^ { \circ }$ and $5 . 5 ^ { \circ } , 4 . 9 ^ { \circ }$ and 6 $. 3 ^ { \circ } , 5 . 6 ^ { \circ }$ and $7 . 1 ^ { \circ }$ with the increasing moving speeds. When the rotating speed is $1 5 ^ { \circ }$ , the average orientation errors of 3D-OmniTrack and OmniTrack are $5 . 2 ^ { \circ }$ and $6 . 3 ^ { \circ } , 5 . 7 ^ { \circ }$ and $7 . 5 ^ { \circ } , 6 . 3 ^ { \circ }$ and $8 . 1 ^ { \circ }$ with the increasing moving speeds. When there is no rotation change in the 2D space, we observe that the two approaches can both achieve higher orientation accuracies, which are $3 . 5 ^ { \circ }$ and $3 . 9 ^ { \circ } , 4 . 2 ^ { \circ }$ and $4 . 5 ^ { \circ } , 4 . 8 ^ { \circ }$ and $5 . 1 ^ { \circ }$ respectively. 3D-OmniTrack can achieve better orientation accuracy than Omni-Track in 2D space.

In order to evaluate the performance of 3D-OmniTrack in terms of the orientation thoroughly, we compare 3D-OmniTrack with Tagyro considering only orientation change. We fixed the location of the target and rotate the target along different axes to evaluate the orientation accuracy. The results are shown in Fig. 20. The experiments are conducted under three rotation speeds 1 $0 ^ { \circ } / s , 1 2 ^ { \circ } / s$ and $1 5 ^ { \circ } / s .$ The average orientation errors of 3D-OmniTrack are $5 . 6 ^ { \circ } , 6 . 7 ^ { \circ }$ and $7 . 4 ^ { \circ }$ , while the average orientation errors of Tagyro are $5 . 3 ^ { \circ } , 7 . 2 ^ { \circ }$ and $7 . 6 ^ { \circ }$ . The accuracies from two approaches are similar. However, Tagyro requires two arrays of tags and two antennas to calculate the orientation, while 3D-OmniTrack only requires one tag attached to the target. Moreover, 3D-OmniTrack can also track the location change of the target, which can be applied in more scenarios.

# 6.5 Evaluation with Different Initialization

The initialization can help 3D-OmniTrack reduce the complexity of the tracking by providing the initial location and orientation. We have three different initialization methods that can be applied in different scenarios: Multiple Channel, Linear Movement, Rotation.

![](images/f93e0b2bb0cbf684bde91b022278b167c8acfd8494095f00b8704189904c9be1.jpg)



Figure 20: Tracking accuracy of the orientation

![](images/aa0d2706226b46ae0cde86c91caf384a689f106dfad56becd1e4966402763900.jpg)



Figure 21: Location error of the initialization

![](images/ab060c45c8645f300e279bcba7d7248a98a88a732cedbc654bcf0d6bd88ad9bb.jpg)



Figure 22: Orientation error of the initialization

![](images/dccdc60d094e7328e774ff12bbfe46e9dfacc7d234b00e0c52eae6bbf5f85412.jpg)



(a) Location accuracy

![](images/86765d07731b59249fc9af3fa677e04d7a35ba3ef1f34a82cc5ebb1e8ceb4639.jpg)



(b) Orientation accuracy   
Figure 23: Impacts of Multi-path Effect

It is hard to evaluate the multi-channel method in COTS RFID systems because the frequency band supported is limited to affect the tracking accuracy. Therefore we evaluate the other two methods in terms of the location error and the orientation error.

The initialization results are shown in Fig. 21 and Fig. 22. For the linear moving, we select different positions P for the initialization and over 80% of the location errors are below 3.1cm. For the rotation scenario, we rotate the target at 50 different locations and 80% of the location errors are below 3.6cm. The orientation errors for the linear moving and the rotation are $4 . 4 ^ { \circ }$ and $3 . 9 ^ { \circ }$ on average respectively.

# 6.6 Impacts of Multi-path Effect

Multi-path interference is a common problem in RFID systems. In order to evaluate its impact on 3D-OmniTrack, we conduct the experiment under two different scenarios: (1) a large conference room without many reflectors; (2) a small lab with many different reflectors placed around the system. The conference room can guarantee the LOS propagation and the multi-path effect is mitigated since the reflectors near the experimental devices are minimized. The lab environment has many reflectors around the experimental devices and people will walk around casually to create severe multi-path effect.

The results in terms of the location error and orientation error are shown in Fig. 23. We can find the average location error in the lab is 2.3× higher than in the conference room and has large variation. The orientation error shows the same trend as the location error. It is 3.7× higher in the lab. From the results, the multi-path can severely degrade the performance of 3D-OmniTrack. The multipath signals can directly interfere with the LOS signal so that the phase difference between the transmitted and the received signals can’t reflect the location and orientation change of the tag.

# 7 CONCLUSION

Tracking both the location and orientation in 3D space is a significant problem in industrial IoT and HCI fields. In this work, we theoretically analyze the signal propagation between an RFID reader’s antenna and a tag. A polarization-sensitive phase model is introduced to consider the impact of tag’s 3D orientation. Based on this model, we propose 3D-OmniTrack, a 3D tracking approach that can track both the location and orientation in 3D space efficiently and accurately. In 3D-OmniTrack, MHT is exploit to find the correct trajectory of the target in 3D space. The empirical results demonstrate that 3D-OmniTrack can achieve centimeter-level location accuracy with the average orientation error of 5◦.

# ACKNOWLEDGMENTS

We sincerely thank our shepherd and the anonymous reviewers for their valuable feedback. This work is supported in part by National Key R&D Program of China No. 2017YFB1003000 and National Natural Science Foundation of China under grant No. 61772306.

# REFERENCES

[1] S. S. Blackman. Multiple hypothesis tracking for multiple target tracking. IEEE Aerospace and Electronic Systems Magazine, 19(1):5–18, 2004.   
[2] C. Bo, T. Jung, X. Mao, X.-Y. Li, and Y. Wang. Smartloc: Sensing landmarks silently for smartphone-based metropolitan localization. EURASIP Journal on Wireless Communications and Networking, 2016(1):111, 2016.   
[3] J. L. Brchan, L. Zhao, J. Wu, R. E. Williams, and L. C. Pérez. A real-time rfid localization experiment using propagation models. In Procs. of IEEE RFID, 2012.   
[4] N. Brouwers, M. Zuniga, and K. Langendoen. Incremental wi-fi scanning for energy-efficient localization. In Procs. of IEEE PerCom, 2014.   
[5] Y. Bu, L. Xie, J. Liu, B. He, Y. Gong, and S. Lu. 3-dimensional reconstruction on tagged packages via rfid systems. In Procs. of IEEE SECON, 2017.   
[6] K. DorfmÃĳller. An Optical Tracking System for VR/AR-Applications. Springer Vienna, 1999.   
[7] J. Hightower, R. Want, and G. Borriello. Spoton: An indoor 3d location sensing technology based on rf signal strength. 2000.   
[8] C. Jiang, Y. He, X. Zheng, and Y. Liu. Orientation-aware rfid tracking with centimeter-level accuracy. In Procs. of ACM/IEEE IPSN, 2018.   
[9] X. Li, Y. Zhang, and M. G. Amin. Multifrequency-based range estimation of rfid tags. In Procs. of IEEE RFID, 2009.   
[10] T. Liu, Y. Liu, L. Yang, Y. Guo, and C. Wang. Backpos: High accuracy backscatter positioning system. IEEE Transactions on Mobile Computing, 15(3):586–598, 2016.   
[11] Y. Ma, N. Selby, and F. Adib. Minding the billions: Ultra-wideband localization for deployed rfid tags. In Procs. of ACM MobiCom, 2017.   
[12] H. Nam and B. Han. Learning multi-domain convolutional neural networks for visual tracking. In Procs. of IEEE CVPR, 2016.   
[13] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil. Landmarc: indoor location sensing using active rfid. Wireless networks, 10(6):701–710, 2004.   
[14] S. Satyavolu, G. Bruder, P. Willemsen, and F. Steinicke. Analysis of ir-based virtual reality tracking using multiple kinects. In Virtual Reality Short Papers and Posters, pages 149–150, 2012.

[15] L. Shangguan and K. Jamieson. The design and implementation of a mobile rfid tag sorting robot. In Procs. of USENIX NSDI, 2016.   
[16] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu. Stpp: Spatial-temporal phase profiling-based method for relative rfid tag localization. IEEE/ACM Transactions on Networking, 25(1):596–609, 2017.   
[17] S. Shen, H. Wang, and R. Roy Choudhury. I am a smartwatch and i can track my user’s arm. In In Procs. of ACM MobiSys, 2016.   
[18] Y. Shen, W. Hu, M. Yang, J. Liu, B. Wei, S. Lucey, and C. T. Chou. Real-time and robust compressive background subtraction for embedded camera networks. IEEE Transactions on Mobile Computing, 15(2):406–418, 2016.   
[19] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus. Rf-compass: Robot object manipulation using rfids. In Procs. of ACM MobiCom, 2013.   
[20] W. Wang, A. X. Liu, and K. Sun. Device-free gesture tracking using acoustic signals. In Procs. of ACM MobiCom, 2016.   
[21] T. Wei and X. Zhang. Gyro in the air: tracking 3d orientation of batteryless internet-of-things. In Procs. of ACM MobiCom, 2016.   
[22] Y. Wen, X. Tian, X. Wang, and S. Lu. Fundamental limits of rss fingerprinting based indoor localization. In Procs. of IEEE INFOCOM, 2015.   
[23] N. Wojke, A. Bewley, and D. Paulus. Simple online and realtime tracking with a deep association metric. In Procs. of IEEE ICIP, pages 3645–3649, 2017.   
[24] C. Wu, Z. Yang, Y. Xu, Y. Zhao, and Y. Liu. Human mobility enhances global positioning accuracy for mobile phone localization. IEEE Transactions on Parallel and Distributed Systems, 26(1):131–141, 2015.

[25] F. Xiao, Z. Wang, N. Ye, R. Wang, and X.-Y. Li. One more tag enables finegrained rfid localization and tracking. IEEE/ACM Transactions on Networking, 26(1):161–174, 2018.   
[26] Z. Xiao, H. Wen, A. Markham, and N. Trigoni. Lightweight map matching for indoor localisation using conditional random fields. In Procs. of ACM/IEEE IPSN, 2014.   
[27] C. Xu, B. Firner, Y. Zhang, R. Howard, J. Li, and X. Lin. Improving rf-based devicefree passive localization in cluttered indoor environments through probabilistic classification methods. In Procs. of ACM/IEEE IPSN, 2012.   
[28] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: Real-time tracking of mobile rfid tags to high precision using cots devices. In Procs. of ACM MobiCom, 2014.   
[29] L. Yao, Q. Z. Sheng, X. Li, T. Gu, M. Tan, X. Wang, S. Wang, and W. Ruan. Compressive representation for device-free activity recognition with passive rfid signal strength. IEEE Transactions on Mobile Computing, 17(2):293–306, 2018.   
[30] Y. Yin, L. Xie, Y. Fan, and S. Lu. Tracking human motions in photographing: A context-aware energy-saving scheme for smart phones. ACM Transactions on Sensor Networks, 13(4):29, 2017.   
[31] C. Zhang, J. Tabor, J. Zhang, and X. Zhang. Extending mobile interaction through near-field visible light sensing. In Procs. of ACM MobiCom, 2015.   
[32] Y. Zhao, Y. Liu, T. Yu, T. He, and C. Qian. Fredi: Robust rss-based ranging with multipath effect and radio interference. Computer Networks, 147:49–63, 2018.