# OmniTrack: Orientation-aware RFID Tracking with Centimeter-level Accuracy

Chengkun Jiang, Member, IEEE, Yuan He, Senior Member, IEEE, Xiaolong Zheng, Member, IEEE, Yunhao Liu, Fellow, IEEE

Abstract—RFID tracking attracts a lot of research efforts in recent years. Most of the existing approaches, however, adopt an orientation-oblivious model. When tracking a target whose orientation changes, those approaches suffer from serious accuracy degradation. In order to achieve target tracking with pervasive applicability in various scenarios, we in this paper propose OmniTrack, an orientation-aware RFID tracking approach. Our study presents a generic model that discribes the linear relationship between the tag orientation and the phase change of the backscattered signals. Based on this finding, we propose an orientation-aware phase model to explicitly quantify the respective impact of the read-tag distance and the tag’s orientation. OmniTrack addresses practical challenges in tracking the location and orientation of a mobile tag. Our experimental results demonstrate that OmniTrack achieves centimeter-level location accuracy and has significant advantages in tracking targets with varing orientations, compared to the state-of-the-art approaches.

Index Terms—RFID, Tracking, Orientation, Polarization

# 1 INTRODUCTION

Location is indispensable information in modern industry. Target tracking, namely, to continuously determine the location of a mobile target, has great significance and therefore attracts a lot of research efforts in the area of industrial cyber-physical systems (CPS) [16], [22], [25], [27]. Radio Frequency IDentification (RFID) has been widely applied in industrial scenarios [2], [11]. Due to its low cost, ease of deployment, and high efficiency in terms of information gathering, RFID is deemed as a promising solution for target tracking [14], [18], [26].

Early works on RFID-based localization and tracking rely on the received signal strength (RSS) to calculate the distance between a reader and a tag or construct a RSS map for fingerprinting. Since RSS is susceptible to environmental dynamics and external signals, the accuracy of those approaches is limited. Recently, researchers propose to exploit signal phase information for RFID tracking. Compared to RSS, the phase change between the transmitted and the backscattered signals is more reliable as an indicator of the reader-tag distance. BackPos in [8] localizes a tag according to the finding that the difference of the phases received by two antennas of a reader corresponds to the difference of the distances from the tag to the two antennas. Assuming that the phase change is solely determined by the readertag distance, Tagoram [26] and MobiTagbot [14] exploit the holography to estimate the probability that a tag is located at a certain location.

The phase change, however, is jointly determined by

C. Jiang and Y. He are with the School of Software, Tsinghua University, Beijing, China. E-mail: jck15@mails.tsinghua.edu.cn, heyuan@mail.tsinghua.edu.cn.   
• X. Zheng is with School of Computer Science, Beijing University of Posts and Telecommunications, Beijing, China. E-mail: zhengxiaolong@bupt.edu.cn.   
Y. Liu is now with the Department of Computer Science and Engineering, Michigan State University, USA. Email: yunhaoliu@gmail.com

![](images/311880624e23eb4a5b435ab938fbd49cc472bf63fe39754f93d1e3f7c0253dfc.jpg)

![](images/a09b5838e682f43cbb998fca3f8729f9fa7492a3b107a84692c86c8ec35a755c.jpg)

![](images/fa87aab3ae5fc579d672804324185ac3cca6f8fafd67ff2c89fb9c2c8f40be72.jpg)

![](images/4d270c5790b6ba596ca75c81aafc8b8024d466929404738d854d0b65a4236b45.jpg)  
Fig. 1. Industrial production lines.

both the reader-tag distance and the tag’s orientation. Most of the existing approaches adopt an orientation-oblivious model that neglects the non-trivial impact of orientation on the phase change. The tracking accuracy will degrade when the tag’s orientation changes while moving. A few works address the problem of orientation change [21], but they cannot be applied to the scenarios where the location and the orientation simultaneously change. There are many such scenarios in industrial applications, as shown in Fig. 1. For example, on a medicine bottling line and a soda production line, the bottles move along the lines with continuous self-rotation. Other production lines make operations to the moving targets, such as labeling or spray painting, which not only require the information of orientation, but also change the orientation of the targets. Besides the product lines, applications such as luggage sorting and warehouse inventory will also inevitably experience simultaneous changes in location and orientation. Directly using an orientation-oblivious model will be error-prone, not to mention the inability to calculate the orientation. In such scenarios, orientation-aware tracking has practical significance, but remains an open problem.

To tackle the above problem, we may meet the following challenges. First, though we know that the backscattered signals from a RFID tag is anisotropic, the relationship between the phase and the orientation is still unclear. Blurring the impact of orientation on the signal phase inevitably introduces errors in tracking a tag. Second, the tag’s orientation and the reader-tag distance jointly affect the phase of the received signal at the reader. A group of phase measurements often correspond to a number of possible location-orientation combinations. Without an effective solution to cope with such ambiguity, the tracking process cannot converge to a unique result.

In this paper, we propose OmniTrack, an orientationaware tracking approach that applies to commercial off-theshelf (COTS) RFID systems.

• By exploiting the phenomenon of tag polarization, we conduct real-world observation and discover the linear relationship between the phase change of the signal and the tag’s orientation. Based on this finding, we propose a generic orientation-aware model to explicitly quantify the respective impact of the reader-tag distance and the tag orientation on the phase change.   
• We propose a light-weight and accurate tracking approach called OmniTrack. To the best of our knowledge, OmniTrack is the first approach that can pinpoint tag’s location and orientation simultaneously. OmniTrack also deals with practical challenges in initializing, updating, and calibrating the location and orientation of a mobile tag. We further presents the extension of OmniTrack for tracking in 3D space.   
• We implement OmniTrack on a COTS RFID platform. The experimental results demonstrate that OmniTrack achieves centimeter-level location accuracy and has significant advantages in tracking targets with varing orientations, compared to the state-of-the-art approaches.

The remainder of the paper is structured as follows. We discuss the related works in Section 2. Section 3 shows the limitation of the existing phase model and presents the orientation-aware phase model. In Section 4 we elaborate on the design of OmniTrack. Section 5 discusses important issues concerning the applicability and the extensibility of OmniTrack in practice. Section 6 presents the implementation details and the evaluation results. Section 7 concludes the paper.

# 2 RELATED WORKS

This section reviews the state of the arts in RFID localization, tracking, and rotation detection. At the end of this section, we briefly discuss how our work differs from the existing works.

RFID Localization and Tracking: Early proposals on RFID localization and tracking generally exploit RSS for location inference. Depending on the specific technique, the existing works can be classified into two categories: RSS-based ranging [1], [4] and fingerprinting [10]. Since RSS is susceptible to environmental dynamics and external signals, ranging based on those environment-dependent propagation models are generally inaccurate. The accuracy of fingerprint-based approaches, however, is constrained by the granularity of site survey or the density of deployed tags.

In recent years the research focus moves onto phasebased localization and tracking [5], [7], [8], [14], [26], [29]. The phase change between the transmitted and the backscattered signals can be an approximate indicator of the readertag distance. Liu et al. [8] directly uses such a phase model to estimate the distance differences from the tag to multiple antennas. And then a hyperbolic positioning method is exploited to localize a tag. In [29], multi-frequency approaches are used to obtain more accurate ranging data for localization.

Phase change introduced by a backscattering tag is a non-negligible factor in phase-based localization and tracking [28]. Under this circumstances, the holographic approaches are proposed and achieve so far the best accuracy. Miesen et al. [9] introduce a holographic scheme to localize a tag with phase values sampled from a synthetic aperture on the RFID reader. Parr et al. [12] exploit tag mobility and adopt Inverse Synthetic Apertures Radar (ISAR) to generate holograms for tag localization and tracking. Tagoram [26] proposes Differential Augmented Hologram (DAH) to track the tag accurately. MobiTagbot in [14] improves the holographic approach with channel hopping to suppress the multi-path effect. Angle of Arrival (AoA) is another metric proposed for localization and tracking [6], [20], [24], which can be derived from the phase difference at different antennas.

RFID Rotation Detection: There are works based on RFID system for orientation or rotation detection. RFcompass [19] uses a 2D-plane partitioning method to navigate a robot to gradually converge to the object’s orientation, but it cannot directly track the object’s orientation. The works in in [3], [17] deploy dense RFID tags to cover the site of interest and then detect position and orientation of the target with a reader installed on it. They need complex and burdensome preparation before tracking, which limits the practical applicability. PolarDraw [15] leverages electromagnetic polarization to identify tag movement, by utilizing information like phase change and RSS. Tagyro [21] proposes a 3D rotation detection system that exploits the phase difference. It requires two sets of tags attached to the target and two readers for rotation detection. They realize 3D rotation detection, however, under the assumption that the position of the target is fixed.

As we exemplify before, tracking targets with the varing orientation is a frequent task in practical production lines. Neglecting the impact of the varing orientation will cause the loss of tracking accuracy. Most of the existing works overlook this problem or tolerate the orientation-induced errors by employing certain probabilistic methods [9], [12], [26]. As for the orientation tracking approaches, most of them consider the orientation change while assuming a fixed location. Our work for the first time explicitly addresses the above problem and innovates RFID tracking with orientation-awareness. OmniTrack can simultaneously pinpoint the location and the orientation. Compared to the existing works, OmniTrack has significant advantages in tracking targets with varing orientations.

# 3 ON THE ORIENTATION-AWARENESS OF THE PHASE MODEL

In this section, we first introduce the limitations of the traditional phase model adopted in the existing approaches.

![](images/e4c6a15221746b92086ff94ffb486b1b91e45aed8eef1bacb38a119bc598ea2b.jpg)



Fig. 2. A typical passive RFID sys- Fig. 3. Tag’s Rotation tem.

![](images/63c6b50c66d5ebf03903e8f7ca8641084673385fa979278f7943450fe3c1c0d4.jpg)



![](images/17a02b91fb8f399086149a47d4d55dd116ff9d98e5772e7667e8a9f5fd2b124c.jpg)



Fig. 4. The impact of tag’s orienta- Fig. 5. Inaccuracy with the tion orientation-oblivious phase model

then we conduct the experiments to show the huge impact of the tag polarization on the received phases. To explain the phenomenon, we theoretically analyze the signal propagation in RFID systems and propose the orientation-aware phase model.

# 3.1 Limitations of the Orientation-oblivious Model

A typical scenario of backscatter communication is shown in Fig. 2. The phase received by the reader is defined as the modulo difference between the phases of the transmitted signal and the received signal. The orientationoblivious phase model will model the phase ϕ based on the distance between the tag and the reader:

$$
\left\{ \begin{array}{l} \phi = \left(\frac {2 \pi}{\lambda} \times 2 d + \delta\right) \mod 2 \pi \\ \delta = \phi_ {T x} + \phi_ {R x} + \phi_ {T a g} \end{array} \right. \tag {1}
$$

where d is the reader-tag distance. $\phi _ { T x } , \phi _ { R x } ,$ and $\phi _ { T a g }$ are the phase changes introduced by the reader’s transmitter, the tag, and the reader’s receiver circuit. λ is the wave length of the signal. $\phi _ { T x }$ and $\phi _ { R x }$ are the constants that are only related to the hardware circuits. In this model, $\phi _ { T a g }$ is commonly treated as a constant or the random noise. The real-world experiment, however, shows that the phase change can achieve up to 2π as shown in Fig. 4 when we fix the reader-to tag distance as 1 m and rotate the tag for one cycle as shown in Fig. 3.

The variation in the received phase will lead to inaccuracy of the target localization. For example shown in Fig. 5, when we rotate the tag to different orientation a, b and $c ,$ it will be wrongly located at position $P _ { a } , P _ { b }$ and $P _ { c }$ rather than its actual position $P _ { 0 } .$ . The error can achieve up to half of the wavelength (about 15cm).

# 3.2 The Orientation-aware Phase Model

The orientation change can affect the received phase, which makes the performance of the existing phase-based localization and tracking approaches degrade. Therefore, it is important to build up a new phase model that can accurately account for the impacts of both the distance and orientation.

# 3.2.1 Polarization

Before presenting the new phase model, we explain why the orientation can change the phase of the received signal. The phenomenon is actually caused by the polarization. Fig. 6 shows the two types of polarization that exist with the RFID system. The first type of polarization is called linear polarization, which is commonly seen in strip-sized RFID tag. With such polarization, the signal transmitted by the tag maintains its direction of electric field in a certain line. This direction is called polarization direction and corresponds to the body direction of the strip-sized tag.

Another type of polarization is called circular polarization. Different from linear polarization, circular polarization makes the direction of electric field continuously change as a circle as shown in Fig. 6. This polarization is implemented in circularly-polarized RFID antennas and used to extend the receiving range. The most important property of polarization is the signal can only be received along the polarization direction. For example, if the direction of a linearly-polarized signal is orthogonal to the direction of a linearly-polarized antenna, the antenna cant receive the signal. Furthermore, if the two directions have a certain angle, the antenna can only receive the projected signal onto the polarization direction of the antenna.

The polarization direction of a strip-sized tag will change when we rotate the tag. Accordingly, the received signal by the antenna changes, which affects the received phase. Given the above-described reason of the phase change, we can mathematically derive the propagation of the signal in a RFID system to build up an orientation-aware phase model.

# 3.2.2 Phase model

We assume the tag is linearly-polarized and the antenna is circularly-polarized, which is a typical setup in many RFID systems. The circularly-polarized antenna can be abstracted as the combination of two linearly-polarized antennas as shown in Fig. 6.

The signal sent by the reader is:

$$
S (t) = u \cos (k t) + v \sin (k t) \tag {2}
$$

where $u ,$ v are the directional vectors of the two abstracted linearly-polarized antennas. The signal received by the tag first travels for d distance and is projected onto the tag’s polarization direction w:

$$
S _ {r} (t) = (u \cdot w) \cos (k t - \phi_ {d} + \phi_ {t}) + (v \cdot w) \sin (k t - \phi_ {d} + \phi_ {t}) \tag {3}
$$

$\phi _ { d } = 2 \pi d / \lambda$ is the phase offset of the distance and $\phi _ { t }$ is the phase offset caused by the tag’s hardware. Then the signal bounces off the tag and returns to the antenna. Again, the signal can only be received along two directions u, v. The two signals add up at last to form the final received signal $R ( t )$ :

$$
\left\{ \begin{array}{l} R (t) = R _ {u} (t) + R _ {v} (t - \Delta t) \\ = \cos (k t - 2 \phi_ {d} - \phi_ {t} - \phi_ {r} - \phi_ {o}) \\ \tan \phi_ {o} = \frac {2 (u \cdot w) (v \cdot w)}{(u \cdot w) ^ {2} - (v \cdot w) ^ {2}} \end{array} \right. \tag {4}
$$

![](images/dd691b0a356a7ffdbff538c973fa95b119af1ea161d333eb6875a3d746036bca.jpg)



![](images/2b3e441d9280b5283110e6e60addce22f58f2252bb9ab22395c78d22600f320c.jpg)



![](images/74f369d6318fe5fbca96e8c522666c8d8f97f7adeeb3bf765737c9c3158f8a9a.jpg)



![](images/e81ca0043df9e94a580c854a5db480a6085ee6c70328e660da332cd828ae5bb4.jpg)



Fig. 8. Phase variation changing the tag type   
when Fig. 9. Phase variation when changing the distance

Fig. 6. Two types of polarization   
Fig. 7. The propagation of the polarized signal   
![](images/c20a3848f3867a5fcdca212fa2e388e9d564544cf60403ea8055b7d1a2b64a8d.jpg)



![](images/91e452707608d488dc33c5d28b246cbc6ab3dcb11180e0e22652c5551871dbea.jpg)



![](images/7144408b2ebedb6a63a8f1beba10189ad53c983b82b35ce2e3a248bd349f5fed.jpg)



![](images/ee7ca084a78593dd623a4046af42081484e08dc02861b6e7106a24af6c2f80ab.jpg)



Fig. 10. The comparison between the real phases and the predicted phases.

![](images/c1ff54d4a7de995508b51610971fbc1016499fc8ac267d16f0322dafb4e8683c.jpg)



Fig. 11. The Overview of OmniTrack

$\phi _ { d } , \phi _ { t } , \phi _ { r }$ are the phase offsets corresponding to the distance, tag’s hardware and the reader’s hardware. $\phi _ { o }$ is the phase offset corresponding to the orientation of the tag. Therefore, we in Eq. (4) quantitatively derive the relationship between the orientation and the phase.

As a special case, when we set the direction of the tag rotate in the uv plane, $p h i _ { o }$ changes linearly with the rotation angle θ (orientation). This is in accordance with the observation from Fig. 4.

# 3.3 Empirical Observations

It is still necessary to verify our model in real experiments even though we derive it based on the signal propagation. In order to prove the correctness of our model, we conduct experiments in both 2D and 3D space to compare the results.

In our experiments, we fix the distance (1m) between the tag and the antenna, which are polarized linearly and circularly respectively. We rotate the tag for one cycle with different incline angles (the angle between the antenna plane and the tag’s polarized direction).

Fig. 10 shows the results. We can find the real received phases match the theoretical phases derived from our phase model. There are also some shift between the two data because we manually set the $\phi _ { t }$ and $\phi _ { r }$ to zero. The overall matched changing trends demonstrate the correctness of our new phase model.

In 2D space, we can find the phase change is linearly related to the orientation change and the changing rate is constant. Although the linear relation fluctuates when the incline angle is not zero, we can still exploit the linearity when the angle is less than $3 0 ^ { \circ }$ because the error between the real phase and the derived phase is less than 0.1 radian, which corresponds to less than 0.5cm in distance. We also conduct experiments with different types of linearlypolarized tags to show the stability of our model. Fig. 8 shows the results with three different tags (Alien 9662, Alien 9654 and Impinj E52). Fig. 9 shows the results with different tag-antenna distance. This linear relation serves as the cornerstone of our 2D tracking algorithm that tracks both the location and orientation.

# 4 DESIGN

The design of OmniTrack must meet the following goals: (1) The location and orientation must be accurately tracked; (2) An initial location and orientation should be provided to ensure the tracking accuracy and efficiency; (3) Accumulated errors should be tackled with appropriately.

The overview of OmniTrack is shown in Fig. 11. The system takes the phase and RSSI as its inputs and a core component Updating Component is used to track the current location and orientation with such inputs. Initialization Component provides the initial location and orientation by using techniques like channel hopping and phase pattern matching. Calibration Component exploits long-term RSSI features or special cases to control the accumulated errors during the tracking.

We will first design an 2D algorithm with the linear orientation-phase relation and then extend it to 3D tracking with the generalized orientation-aware phase model.

# 4.1 2D Orientation-aware Tracking

In 2D tracking, we deploy an RFID reader with two antennas as shown in Fig. 12. It queries the tag continuously and reports each phase reading.

![](images/7a7901aac4d3d6cd548ca32a9efd954f2358cd122da83520500abcece6c7eb54.jpg)



Fig. 12. Tag’s Movement

![](images/2ca9d715f3dabe18cd2806560be8ae239566480e7032bc8b9648028f8325c6b7.jpg)



Fig. 13. Tracking the tag

![](images/cba533cb405e0b0d97b7a3f878b2aeaad81fc91ec1a00341f2b10775d5f0a0c4.jpg)



Fig. 14. Initial position estimation

The detailed updating process runs as follows. As illustrated in Fig. 12, suppose we have phase readings from antennas $A _ { 1 }$ and $A _ { 2 }$ at time $t _ { i }$ and $t _ { i + 1 }$ . We denote the corresponding phase readings by $\phi _ { i } ^ { p } ,$ , where $p$ is the antenna index and i is the time index. The phases at time $t _ { i }$ and $t _ { i + 1 }$ are shown below according to Eq. (4):

$$
\left\{ \begin{array}{l} \phi_ {i} ^ {p} = \left(\frac {2 \pi}{\lambda} \times 2 d _ {i} ^ {p} + k \times \theta_ {i} ^ {p} + c ^ {p}\right) \mod 2 \pi \\ \phi_ {i + 1} ^ {p} = \left(\frac {2 \pi}{\lambda} \times 2 d _ {i + 1} ^ {p} + k \times \theta_ {i + 1} ^ {p} + c ^ {p}\right) \mod 2 \pi \end{array} \right. \tag {5}
$$

$d _ { i } ^ { p }$ denotes the distance between the antenna $p \ ( p = 1 , 2 )$ and the tag at time $t _ { i } . \ \theta _ { i } ^ { p }$ denotes the angle between the tag’s polarized direction and antenna-tag direction. $c ^ { p }$ is the constant phase offset of each antenna.

Suppose the tag’s location and orientation at $t _ { i }$ are known, our task is to calculate $d _ { i + 1 } ^ { p }$ and $\theta _ { i + 1 } ^ { p }$ . Note that there are only two constraints in Eq. (5) corresponding to the two antennas. Solving Eq. (5) does not yield a unique solution. We need to exploit additional geometric relationship to determine the tag’s location and orientation.

It is helpful that the rotation angle $\varDelta \theta _ { i } ^ { p }$ between adjacent samples will be same for two antennas. Therefore, by subtracting two phases at adjacent samples, we will have:

$$
\Delta \phi_ {i} ^ {p} = (\frac {2 \pi}{\lambda} \times 2 \Delta d _ {i} ^ {p} + k \times \Delta \theta_ {i} ^ {p}) \mod 2 \pi \tag {6}
$$

According to the above inference, $\varDelta \theta _ { i } ^ { 1 } = \varDelta \theta _ { i } ^ { 2 }$ . By further subtracting $\breve { \varDelta { \phi } } _ { i } ^ { 1 }$ and $\varDelta \phi _ { i } ^ { 2 }$ in Eq. (6), we can eliminate the impact of rotation angles and get

$$
\left\{ \begin{array}{l} \Delta \phi_ {i} = \Delta \phi_ {i} ^ {2} - \Delta \phi_ {i} ^ {1} = \left(\frac {2 \pi}{\lambda} \times 2 \Delta d _ {i}\right) \mod 2 \pi \\ \Delta d _ {i} = (d _ {i + 1} ^ {2} - d _ {i + 1} ^ {1}) - (d _ {i} ^ {2} - d _ {i} ^ {1}) \end{array} \right. \tag {7}
$$

Recall that we know the previous position and orientation of the tag, the distance difference $( d _ { i } ^ { 2 } - d _ { i } ^ { 1 } )$ is known. According to Eq. (7), we can obtain the distance difference at time $t _ { i + 1 }$ as long as $\varDelta \phi _ { i }$ is uniquely determined.

Fig. 12 illustrates the geometric relationship during tracking. According to the triangle inequality theorem, we have

$$
\left| d _ {i} ^ {2} - d _ {i} ^ {1} \right| <   2 m, \left| d _ {i + 1} ^ {2} - d _ {i + 1} ^ {1} \right| <   2 m \tag {8}
$$

2m is the distance between the two antennas. Thus if we make the distance between the two antennas within the halfwavelength $\frac { \lambda } { 2 }$ (about 15cm), then we have

$$
\left| d _ {i} ^ {2} - d _ {i} ^ {1} \right| <   \frac {\lambda}{2}, \left| d _ {i + 1} ^ {2} - d _ {i + 1} ^ {1} \right| <   \frac {\lambda}{2}. \tag {9}
$$

That means the $- \frac { \lambda } { 2 } ~ < ~ \varDelta d ~ < ~ \frac { \lambda } { 2 }$ , which constrains the range of the phase between −2π and 2π according to Eq. (7). In this way, we can eliminate the phase ambiguity and obtain $( d _ { i + 1 } ^ { 2 } - \dot { d } _ { i + 1 } ^ { 1 } )$ . Actually, the constraints for the distance between antennas can be relaxed based on the feasible region proposed in BackPos [8].

So far we know the position of the antennas and the difference of the distances from the tag to the antennas, the tag is located in a hyperbola with the two antennas as the focus. As shown in Fig. 13, we denote the current location of the tag by $P _ { i }$ . The tag’s movement direction consists of two# » # » projected directions: $\overrightarrow { A _ { 1 } P _ { i } }$ and $\overrightarrow { A _ { 2 } P _ { i } }$ . As illustrated before, the sampling interval of the reader is very short so that we can assume the tag’s moving direction doesn’t change during a sampling interval. The moving distances $\Delta d _ { i } ^ { 1 } , \Delta { \breve { d } _ { i } ^ { 2 } }$ from time $t _ { i }$ to time $t _ { i + 1 }$ at the two projected directions can be calculated according to Eq. (6):

$$
\Delta d _ {i} ^ {p} = (\frac {\lambda}{4 \pi} (\Delta \phi_ {i} ^ {p} - k \times \Delta \theta_ {i}) \tag {10}
$$

We can then calculate the new position of the tag $P _ { i + 1 }$ by:

$$
P _ {i + 1} = P _ {i} + \Delta d _ {i} ^ {1} \overrightarrow {A _ {1} P _ {i}} + \Delta d _ {i} ^ {2} \overrightarrow {A _ {2} P _ {i}} \tag {11}
$$

The new location of the tag is the intersection of line $P _ { i } P _ { i + 1 }$ and the hyperbola described before. We define the line connecting two antennas as the X axis and the vertical bisector of the two antennas as the Y axis. Then we have:

$$
\left\{ \begin{array}{l} \frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \\ m ^ {2} - a ^ {2} = b ^ {2} (b > 0) \\ x _ {i} + \Delta d _ {i} ^ {1} \cos \alpha_ {1, i} + \Delta d _ {i} ^ {2} \cos \alpha_ {2, i} = x \\ y _ {i} + \Delta d _ {i} ^ {1} \sin \alpha_ {1, i} + \Delta d _ {i} ^ {2} \sin \alpha_ {2, i} = y \end{array} \right. \tag {12}
$$

$\alpha _ { i } ^ { 1 }$ and $\alpha _ { i } ^ { 2 }$ are denoted in Fig. 13. Solving the above equation yields the tag’s rotation angle $\varDelta \theta _ { i }$ and new coordinates $( x , y )$ . Through the above updating process, OmniTrack keeps tracking the location and the orientation of a moving tag.

It is worth noting that for ease of illustration, we present the algorithm as the antennas are located at the same plane of tag rotation. In practice, OmniTrack works as long as the perpendicular distance h from the antennas to the tag rotation plane is known. The moving distance of a tag can be calculated using our algorithm, according to the geometric relation as shown in Fig. 16.

# 4.2 Initialization

OmniTrack tracks the target in an iterative way according to the consecutively received phases, the previous location, and the previous orientation of the target. We should design a light-weight component to calculate both the initial location and orientation of the target. The initialization component mainly uses the techniques of channel hopping and RSS pattern matching.

![](images/26e91a461c4783c809f98312eee2a074b89b0ffa0987f0edd07ffffb9a38703c.jpg)



Fig. 15. Initialization in a straight line

![](images/357ff67ef231b373b9ca3f0197be4cef1dd2341c987cb36ef414efc2c8ed6cb5.jpg)



Fig. 16. The antenna plane is different from the rotation plane of the tag

# 4.2.1 Channel Hopping

According to our orientation-aware phase model provided in Eq.(4), the random hardware phase offset denoted by c can make the distance derivation unreliable. However, we observe that our orientation-aware phase model in $\operatorname { E q . } ( 4 )$ can also be expressed as follow:

$$
\phi = \left(\frac {2 \pi f}{v} \times 2 d + k \times \theta + c\right) \mod 2 \pi \tag {13}
$$

f is the frequency of the carrier wave and v is the speed of the electromagnetic wave.

The phase changes linearly with the frequency. If we measure multiple phase readings with channel hopping, the effect of the angle θ and hardware c can be eliminated through the subtraction among the phase readings with different frequencies.

In COTS RFID system, the gaps of adjacent hopping channels are equal, we still can’t solve out a unique distance through phase differences.

In OmniTrack, we make the antennas to hop the channels with the same frequency gap $\varDelta f ,$ then we can obtain the phase change $\varDelta \phi _ { i }$ corresponding to the frequency change $\bar { \Delta } f$ at the antenna i. The $\varDelta \phi _ { i }$ can be expressed as:

$$
\Delta \phi_ {i} = (\frac {4 \pi}{v} \times d _ {i} \times \Delta f) \mod 2 \pi \tag {14}
$$

$d _ { i }$ is the distance between the tag and the antenna i. There still exists phase ambiguity. However, with at least two antennas, we can obtain the distance difference between the tag and two antennas i and $j \colon$

$$
\Delta \phi = \Delta \phi_ {i} - \Delta \phi_ {j} = (\frac {4 \pi}{v} \times (d _ {i} - d _ {j}) \times \Delta f) \mod 2 \pi \tag {15}
$$

We observe that $d _ { i } - d _ { j }$ is unique if $\begin{array} { r } { | d _ { i } - d _ { j } | < \frac { v } { 2 \Delta f } } \end{array}$ , which constrains the range of $\varDelta \phi$ between −2π and 2π. As shown in Fig. 14, we can locate the tag in a hyperbola defined by the two antennas and the distance difference. When there are more antennas, we can draw multiple hyperbolas for each two antennas and locate the tag at their intersecting point.

![](images/04254317c368b8e6641574ec57eaf2a66fd1bb058d2d3915ee2e27e9985c9dcf.jpg)



(a) Phase changing with rotation

![](images/ac3989aef0a3c8aea73af3108031225efb9f85f30d93bb264893d472ab05fdf3.jpg)



(b) RSS changing with rotation   
Fig. 17. Measured phase and RSS of a tag rotating for $3 6 0 ^ { \circ }$

# 4.2.2 Pattern Matching

The phase and RSS received by the reader can present unique pattern when we rotate the tag by one cycle (360◦) at a fixed position. As shown in Fig. 17, the phase changes linearly with the relative rotation angle, which satisfies our phase model in Eq.(4). The relation between the RSS and the rotating angle satisfies the sinusorotates to point at the reader (the $\theta = \textstyle { \frac { \pi } { 2 } } o r ^ { \frac { 3 \pi } { 2 } }$ . When the tag in Eq.(4)), the between the polarized directions of the antenna and the tag. Thus we can know the tag’s current direction if the current RSS reaches its lowest value.

In OmniTrack, with two antennas $A _ { 1 }$ and $A _ { 2 }$ as shown in Fig. $^ { 1 4 , }$ we rotate the tag anticlockwise. The RSS received by $A _ { 1 }$ will first capture a lowest value at time $t _ { 0 } ,$ then we mark a corresponding time $t _ { 1 }$ at antenna $A _ { 2 }$ . After that, antenna $A _ { 2 }$ will capture a lowest value at time $t _ { 2 }$ . We know that during the time period $( t _ { 1 } , t _ { 2 } )$ , the tag rotates for ∆θ. In order to calculate $\varDelta \theta ,$ , we retrieve the phase values $\phi _ { 1 }$ and ϕ2 corresponding to t1 and $t _ { 2 }$ at antenna $A _ { 2 }$ . So according to the model in Eq.(4), the $\varDelta \theta$ is $| k ( \phi _ { 2 } - \phi _ { 1 } ) |$ . In another case, if the tag rotates clockwise, the ∆θ is $2 \pi - | k ( \phi _ { 2 } - \phi _ { 1 } ) |$ : k is the fixed phase changing rate in Eq.(4).

We already know the hyperbola and the intersecting angle $\varDelta \theta$ in Fig. 14, then we can solve out both the location and orientation of the tag if we define the line connecting two antennas as the X axis and the vertical bisector of the two antennas as the Y axis. The set of equations is expressed below:

$$
\left\{ \begin{array}{l} \frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \\ m ^ {2} - a ^ {2} = b ^ {2} (b > 0) \\ d _ {1} ^ {2} + d _ {2} ^ {2} - 2 d _ {1} d _ {2} \cos \theta = 4 m ^ {2} \end{array} \right. \tag {16}
$$

Since the phase value corresponding to the lowest RSS is recorded when we rotate the tag, any orientation of the tag relative to the antenna can be calculated from the phase difference according to Eq.(4).

We could find the initialization of the system is reduced to solve an equation set, which incurs negligible computational cost into the system. As for the channel hopping time and the rotation time, in industrial system, there are preparation zones for each production lines, so these operations could be finished at these places not to incur extra costs to the system.

# 4.2.3 Initialization in a Straight Line

In practice, we can exploit some characteristics in real industrial applications like the product lines. In industrial product lines, products often move in a straight line with a constant speed v as shown in Fig. 15. Moreover, there will be limited orientation changes.

In such scenarios, as the target moves along the path, the phase received by antenna A1 will decrease to a minimum value and increase afterwards. When the phase is at the minimum value, the line connecting the target and the antenna will be perpendicular to the moving direction. Since we can obtain the timestamps of the phase values at $L _ { 1 }$ and $L _ { 2 } ,$ we can calculate the moving distance between them as v∆t

# 4.3 Calibration

The iterative calculation in tracking is likely to accumulate errors. Therefore, we design a calibration component to eliminate the accumulated error.

We first conduct the experiments to find the characteristics of the received signal when the tag is moving and rotating. We slide a tag back and forth in a distance of 20cm and draw the RSS change in Fig. 18 (a). Also, we rotate the tag to measure the RSS value and present the result in Fig. 18 (b).

From Fig. 18, we find: (1) The RSS change caused by tag’s rotation is far more than that caused location displacement. In other word, if the tag’s rotation is the main movement when tracking, we could ignore the effect of the tag’s displacement on the RSS. (2) The RSS change caused by the tag’s rotation satisfies the sinusoid relation and the RSS value is related to the rotating angle.

In most scenarios, the rotation of the target is common and frequent. So in OmniTrack, we try to first capture those intervals that the target’s rotation is dominant and it has almost no movement, then we can search for a proper initial orientation so that all RSS changes in these intervals can fit the sinusoid function well. There are two steps to finish the task: (1) finding the calibration intervals; (2) designing suitable algorithm to calibrate the orientation.

Calibration Interval: The calibration in OmniTrack is passively triggered in a calibration interval. Specifically, the calibration interval is specified according to the observation above: the tag’s rotation is the main movement. In the implementation, we define two variables to detect the calibration interval: the total rotating angle θ and the total moving distance d during the interval. The interval is detected if $\theta \ > \ \theta _ { t }$ and $\textit { d } \ : < \ : \ d _ { t } ,$ where $\theta _ { t }$ and $d _ { t }$ are predefined parameters $( d _ { t } \substack { = } 1 0$ cm, $\theta _ { t } { = } 3 0 ^ { \circ }$ in our implementation).

Calibration Algorithm: In the calibration interval, we can obtain a series of rotation angles as $\{ \varDelta \theta _ { i } \}$ based on our tracking module and our goal is to calibrate the orientation at the beginning of the interval. According to our second observation, we can model these RSS changes as:

$$
r s s = P | \sin (\theta + \Delta \theta) | + P _ {\text { offset }} \tag {17}
$$

where P is the maximum RSS range and $P _ { o f f s e t }$ is the strength offset. We denote the series of RSS differences corresponding to the rotation angles as $\{ \varDelta r s s _ { i } \}$ and the initial orientation angle we want to calibrate as $\theta _ { o }$ .

Our goal is to search for an initial orientation angle that can make the theoretical RSS series suits $\{ \varDelta r s s _ { i } \}$ best. The theoretical $\varDelta r s s _ { i }$ has the expression below:

$$
\Delta r s s _ {i} = P (| \sin (\theta + \Delta \theta_ {i + 1}) | - | \sin (\theta + \Delta \theta_ {i}) |) \tag {18}
$$

![](images/037ab25bba2221b2f2face7213124d0f90bae11ad8369a0b7f9b892958d94fcc.jpg)



![](images/e88f740f7887f2f3d240c8bcb156a8c6c635487093e77a3aa201d18148fa57e8.jpg)



(a) RSS changing in small displace ment   
- (b) RSS changing when angle changing   
Fig. 18. RSS changing pattern

The RSS range P depends on many factors like the tag’s distance to the antenna and the transmitting power of the reader, it is hard to accurate acquire the parameter. Instead, we turn to the metric ∆rssi+1 , which can eliminate the $\frac { \varDelta r s s _ { i + 1 } } { \varDelta r s s _ { i } }$ parameter P . We enumerate the angle θ in the range from 0 to 2π with the accuracy of $1 ^ { \circ }$ and set the angle that minimizes the $\begin{array} { r } { \sum \big ( \frac { \varDelta r s s _ { i + 1 } } { \varDelta r s s _ { i } } \big ) ^ { 2 } } \end{array}$ ∆rssi+1 as the calibrated angle at the ∆rssi beginning of the interval. One thing we should notice is that theoretically we could obtain two angles that both minimize the metric because of the periodicity of the RSS change model. The difference between the two angles is just π. Thus if the angle calculated is not close to the angle $\theta _ { o } ,$ we will use the corresponding angle that close to $\theta _ { o }$ .

The location could be calibrate with the calibrated orientations at different antennas using the method in initialization module.

# 4.4 Extension to the 3D Orientation-aware Tracking

It is feasible to extend our algorithm to 3D space because the orientation-aware phase model is effective as long as the three directional vectors $( u , v , w )$ are provided. Thus we present the 3D tracking algorithm for 3D scenarios.

In 3D space, we can obtain the accurate distance difference between antennas since the rotation is not constrained in 2D and phase-orientation change is not linear. In order to track the location and orientation in 3D space, we use three antennas and particle filtering to track the tag in a probabilistic manner.

We start from an initial state (location, orientatoin) in 3D space. We only consider its neighboring states as next possible states. For example, when we divide the space into a series of cubic gird, the neighboring locations will be the centers of grids around the current grid. As for orientation, the neighboring orientations will be the orientations that are rotated vertically and horizontally with a certain angle $( 3 ^ { \circ }$ in our experiments) from the current orientation. Therefore, the next possible states will be the combinations of neighboring locations and orientations. We assume the state change of a tag is consecutive and the sampling rate of a reader is high enough to capture the tag’s movements.

We can then calculate the received phase difference at time $t _ { i }$ for antenna p as :

$$
\Delta \phi_ {i} ^ {p} = (\frac {4 \pi}{\lambda} \times (d _ {i + 1} ^ {p} - d _ {i} ^ {p}) + (\phi_ {o _ {i + 1}} ^ {p} - \phi_ {o _ {i}} ^ {p})) \tag {19}
$$

where $\phi _ { o _ { i } }$ is the phase offset caused by the orientation at time i. Then, we compare the theoretical phases with real observed phases to calculate the probability of next state:

$$
P _ {i} ^ {p} (l o c, o r i e n) = \frac {1}{\sum_ {p} ^ {K} e ^ {| \Delta \widetilde {\phi_ {i} ^ {p}} - \Delta \phi_ {i} ^ {p} |} / K} \tag {20}
$$

where $\widehat { \varDelta { \phi } _ { i } ^ { p } }$ is the phase received by antenna p. Then those combinations with highest probabilities will be selected as the candidates for particle filtering.

For consecutive N samplings, we will have many trajectories and the long-term RSSI pattern will be exploited to remove the unlikely trajectories. For example, when the tag points to an antenna, its RSSI will drop fast. The RSSI will also experience a significant drop when the tag moves far away from the antenna. These patterns can help us remove the candidates. At last the trajectories with the highest probability will be output as the final trajectory of the target.

# 5 DISCUSSION

Multi-path effect: The multi-path effect is a common problem for phase-based tracking. By examining the real industrial application scenarios, we find that multi-path effect can be avoided as much as possible, by deploying the reader antennas at appropriate positions. For example, for tracking medicine bottles on a biopharmaceutical production line (Fig. 1), one can deploy the antennas sufficiently close to the line to ensure the quality of line-of-sight signals [23]. Even when the multi-path signals really interfere with phase calculation, we can take effective countermeasures, e.g. channel hopping in MobiTagbot [14], to mitigate the negative impact.

Scalability: Note that the communication range of a RFID reader providing phase information in our evaluation is typically several meters. How to extend the deployment of OmniTrack and make it seamlessly cover a large area becomes a meaningful issue. For reliable and seamless tracking, one can deploy multiple pairs of antennas in different subareas. The antennas should be synchronized at the backend with intersected monitoring areas. Knowing the realtime location of a tag, the reader is able to determine when and to which antenna a handover of tracking responsibility should be made. Multiple antennas can also improve the tracking performance. We can detect the impact of the multipath by measuring the linearity of the phase change when hopping the channels [14]. Therefore, we can select those antennas free of the multi-path effect for OmniTrack.

Tracking performance with multiple tags: The performance of OmniTrack can be affected when there are many tags in the field. The sampling rate for each tag will be decreased to affect the phase collection. In order to illustrate how many tags OmniTrack can support with COTS RFID systems, we build a theoretical model to analyze it. Suppose the querying rate of the reader is S with the number of tags as ${ \dot { N , } }$ the target can be queried with the rate of S/N on average. In fact, the querying rate S won’t be assigned equally due to the different RSSIs of the tags. The movements of the tags will average the querying rate so that we can treat it as $\check { S } / N$ . The relationship between the phase change and the distance change is $\Delta \dot { \phi = } 4 \pi \Delta d / \lambda$ . Therefore, if we want to ensure the cm-level accuracy, we expect the reader can capture the phase change corresponding to 1cm distance

![](images/157234ca525e1e60eb569ceee9b33202349103f1e8b3ed59db705550e5e12e96.jpg)



(a) Linear Track

![](images/ee215a023551b0b335cc9ebf1dcba22c174bf399228253c5bbe619905455d29b.jpg)



(b) Circular Track   
Fig. 19. Experiment Setup

change. With a moving speedof consecutive queries will be $\frac { v } { S / N }$ , the moving distancefor the target tag. We $\begin{array} { r } { N ^ { ' } < { \frac { \varDelta d S } { v } } } \end{array}$ . In COTS RFID systems, the querying rate will be around 100 samples/sec and the target moving speed will be about 0.1m/s in many product lines like luggage sorting in the airport. Therefore, we can support $N \ < \ 1 0$ tags without significant performance degradation. It is worth noting that such capability can satisfy a wide range of applications.

Tracking performance with longer distances: Typically, ultrahigh-frequency (UHF) passive tags can be read from up to 4∼6m in free air [13]. Within the accessible range of the reader, the performance of OmniTrack is directly related to the sampling rate of a tag. When the distance between a tag and the reader increases, the sampling rate of the tag decreases so that the tag’s movement can’t be accurately reflected based on the phase change between two adjacent samples. According to [13], the sampling rate won’t change much within a distance of 2m, but will decrease rapidly when the distance exceeds around 4m. Therefore, OmniTrack can achieve the cm-level accuracy within a range of 2m when the tag is moving at a typical speed of 0.1∼0.28m/s in product lines. The performance will degrade to dm-level when the sampling rate decreases to 10% with over 5m distance. When the distance exceeds 6m, OmniTrack fails to track the tag, because under that condition, the sampling rate will decrease to 0. We may resort to the multiple-antenna solution to preserve the scalability of OmniTrack, which we have discussed in the second paragraph of this section.

# 6 EVALUATION

We implement OmniTrack on COTS devices and compare it with two state-of-the-arts approaches under different experimental settings.

Implementation: In the implementation and experiments, we use an ImpinJ Speedway R420 RFID reader, two Laird circular polarized antennas, and Alien UHF linearpolarized RFID tags. The whole system operates at the 920- 926 MHz band, with frequency hopping enabled. We configure the reader to immediately report the phase reading, whenever a tag is detected. The software is implemented using C# and runs in a MSI desktop PC with Intel Core i7 6700 CPU at 2.6 GHz and 8G memory.

Methodology: We attach a tag onto a rotator that is mounted on top of a toy train. Fig. 19 shows the setup and the train rails. We conduct two types of experiments:

![](images/6636a950f4de72749b342e4811b626a9461f634a04fa0b9048d961031faff617.jpg)



(a) v=0.127m/s

![](images/d1921aeeeb333e2d2df647d3c9d33d074e5de9fa2376082f031086a9bb850af2.jpg)



(b) v=0.203m/s

![](images/e6cca6a6b4589f4f1d1605ea427c4ff658d6f549da3fc7f0bd30b79997eac0c8.jpg)



(c) v=0.286m/s

Fig. 20. Location error on the linear rail   
![](images/8a4d1908082a29f29f060d1f585ccc0fb27974147c0cec1c93be0640c9ca218e.jpg)



(a) v=0.127m/s

![](images/72f078a408ac2ea1856ff1f6be71e1bf2925a3da1aa037e9b5281bf3e65654ea.jpg)



(b) $\mathrm { v } { = } 0 . 2 0 3 \mathrm { m } / \mathrm { s }$

![](images/41857a4a7eb3707b3a45588898b624c7748559e6c95791869f49e3158a90b51e.jpg)



(c) $\scriptstyle \mathbf { v = } 0 . 2 8 6 \mathbf { m } / \mathbf { s }$   
Fig. 21. Location error on the circular rail

tracking without rotation and tracking with rotation. In the former experiment, orientation changes are only caused by the train movement. We manually set the rotator to rotate in the latter experiment. The rotating speed is set to $1 0 ^ { \circ } / s$ throughout the evaluation.

We evaluate the performance of tracking in terms of the localization error and the orientation error. The groundtruth location of the target is calculated according to the train speed. The ground-truth orientation is acquired based on the rotating speed. We compare OmniTrack with stateof-the-art approaches: Tagoram [26] and BackPos [8]. We implement the three approaches with the same hardware.

# 6.1 Tracking without Rotation

We first evaluate the performance without manual rotation. The movement speed of the train is set at the same magnitude as the existing works like Tagoram.

Linear Rail: In this experiment, the train drives on the linear rail as shown in Fig. 19 (a). the train’s speed is set at three levels (0.127m/s, 0.203m/s, and $0 . 2 8 \bar { 6 } \mathrm { { m } / \mathrm { { s } ) } }$ . We repeat the experiment 25 times and calculate the average location error of OmniTrack, Tagoram, and BackPos. CDFs of location error are plot in Fig. 20.

When the train’s speed $v = 0 . 1 2 7 \mathrm { m } / \mathrm { s } ,$ , the average location errors of Tagoram, OmniTrack and BackPos are 2.4cm, 3.4cm, and 8.3cm, respectively. When the moving speed $v \ = \ 0 . 2 0 3 \mathrm { { m } } / \mathrm { { s } }$ , the average location errors of Tagoram, OmniTrack, and BackPos are 3.9cm, 5.1cm, and 11.7cm. For $v \ = \ 0 . 2 8 6 \mathrm { { m } } / \mathrm { { s } }$ , the errors increase to 4.9cm, 7.2cm, and 13.1cm. As the speed increases, all the three approaches suffer accuracy degradation because of the decreased sampling rate. Tagoram has the best performance, owning to the prior knowledge of the movement trajectory. The accuracy of OmniTrack is close to that of Tagoram, without the requirement of prior knowledge. BackPos is apparently less accurate, due to the impact of orientation change.

Circular Rail: We then conduct experiments on a circular rail as in Fig. 19 (b). We compare OmniTrack with Tagoram and BackPos and plot the CDFs of location error in Fig. 21.

It shows that the average location errors of OmniTrack are 6.1cm, 7.1cm, and 8.5cm when the moving speeds are $0 . 1 2 7 m / s , \ 0 . 2 0 3 m / s ,$ and $0 . 2 8 6 m / s ,$ respectively. The tag’s orientation keeps changing due to the circular rail, even though we don’t manually rotate it. The orientation change affect the location errors of the three approaches. It is worth noticing that the accuracy gap between OmniTrack and Tagoram is reduced because of the orientation-aware model used in OmniTrack. However, Tagoram still achieves the best accuracy, owing to the prior knowledge of the movement. So in the next experiments, we evaluate the performance in more complex scenarios, which emulate the practical industrial applications scenarios.

# 6.2 Tracking with Rotation

In this section, we evaluate the three approaches when tracking the targets with rotation. The two rails are the straight rail and S-shape rail respectively. We also set the rotator to rotate at $1 0 ^ { \circ } / s$ at certain spots along the rails.

Straight Track: We plot the CDF of location errors in Fig. 22. The train’s speed is set at three levels ${ \bf ( \nabla 0 . 1 0 4 m / s , }$ 0.186m/s, and 0.232m/s).

We can see that OmniTrack apparently outperforms Tagoram and BackPos. When the train’s speed is $0 . { \bar { 1 } } 0 4 m / s ,$ the average location errors of OmniTrack, Tagoram, and BackPos are 4.3cm, 7.7cm, and 13.3cm, respectively. In term of location error, OmniTrack outperforms Tagoram and BackPos by 1.8× and 3.1×, respectively. The reason behind is that OmniTrack quantifies the impact of tag orientation on phase readings and eliminate that negative impact by using the orientation-aware model.

Comparing the results of Fig. 20 and Fig. 22, OmniTrack has consistently stable location accuracy, no matter the tag rotates or not. In comparison, the accuracy of Tagoram and BackPos apparently degrades when the tag rotation is introduced.

To further understand the advantage of OmniTrack, we present the error changes of the three approaches on the straight rail. The results are shown in Fig. 26. We can clearly observe that at every rotation spot, the location errors of Tagoram and BackPos significantly increase while Omni-Track keeps the error at a low level. The reason is OmniTrack explicitly deals with the problem of orientation change.

![](images/bf4b03e5036b1df32ef6372833f926b00dd0ca9de04ff9e3360e96ec495a5bde.jpg)



(a) v=0.104m/s

![](images/a07e8f0725b3a1e824766839c29199751a5536ee812aff77ac966962f026b38b.jpg)



(b) v=0.186m/s

![](images/46329c65b4f9aa79bc71b623aff8bec48c9ecc9c6483c6a57f2f342594ba461c.jpg)



(c) v=0.232m/s

Fig. 22. Location error on the straight rail   
![](images/7fa76774a90d3b8680865c796a70395440175ccc0f520b2b7e8888a3c77d5f1d.jpg)



(a) v=0.102m/s

![](images/2a8b680cdfec5b1996cd28872cdb983b7090b868c20dfcc41028e3b6fadfa56e.jpg)



(b) v=0.174m/s

![](images/123c021505f14222459b7e5e938f7d16ed83fb7f1c6adcae7bef6235b2568409.jpg)



(c) v=0.223m/s

Fig. 23. Location error on the S-shape rail   
![](images/6e3d77fd3ae6cbdd6c8e3b43f8ffadade0a26f2711af4e30818bd646531a2129.jpg)



![](images/bf58172b75b4b4df5e6582b2645a0918d1c241d1ca09275d59705a17933efcd4.jpg)



![](images/f29a3814d5448bab485de400d6b7414d5e833b9d2921659ac7915220b72e0ae9.jpg)



![](images/c15faf28a31e75b606044ed397fc5815e194e2bb5dd1347b1e85b30e885657c3.jpg)



Fig. 24. Orientation error on the rail Fig. 25. Orientation error on the rail Fig. 26. Location error along the rail Fig. 27. Orientation error when rowithout rotation with rotation tating at a fixed position

S-shape Track: We then conduct experiments on a complex S-shape rail and set the rotator to rotate during the tracking. The total length of the track is 232 cm. The train’s speed is set at three levels, namely $0 . 1 0 2 m / s , 0 . 1 7 4 m / s ,$ and 0.223m/s.

We plot the CDF of location errors in Fig. 23. We can find that the S-shape rail with more turns and rotations exacerbates the problem with the orientation-obliviousness model in BackPos and Tagoram. The average location errors of Tagoram and BackPos are 9.7cm and 14.3cm, respectively, when the train’s speed $v = 0 . 1 0 2 m / s .$ . In comparison, OmniTrack has an average location error of only 5.7cm, outperforming Tagoram and BackPos.

# 6.3 Accuracy of Orientation

OmniTrack can simultaneously calculate a tag’s orientation, which cannot be done by either Tagoram or BackPos.

We record the orientation errors during the experiments of tracking targets without rotation in Section 6.1. Fig. 24 presents the means and variations of orientation errors. The average orientation error on the linear rail is 3.2◦, 4.6◦, and 5.5◦, when the train’s speed v is $0 . 1 2 7 m / s , 0 . 2 0 3 m / s ,$ and 0.286m/s, respectively. On the circular rail, the average orientation error is 10.3◦, 12.8◦, and 15.6◦, respectively under the corresponding speed. The orientation error on the circular rail is higher than that on a linear rail, because orientation change is more frequent and continuous on the circular rail. Besides, the attenuation of backscattered signals may be larger when the train drives on the semicircle farther to the antennas. Then the RSS and phase readings appear to be more noisy, potentially inducing higher errors.

We record the orientation errors during the experiments of tracking targets with rotation in Section 6.2. Fig. 25 shows the means and variations of orientation errors. The average orientation errors on the straight rail are $5 . 7 ^ { \circ } , \ 6 . 6 ^ { \circ } .$ , and 8.5◦, when the moving speeds are $0 . 1 0 2 m / s , \ 0 . 1 7 4 m / s ,$ and $0 . 2 2 3 m / s ,$ respectively. On the S-shape rail, the average orientation errors are 8.3◦, 10.6◦, and 13.4◦, respectively under the corresponding speed. The orientation error on the S-shape rail is higher because orientation change is more frequent on the S-shape rail.

# 6.4 Accuracy of Initialization

In this section, we evaluate the accuracy of the initialization in OmniTrack. We select 12 positions on the circular rail to separately initialize OmniTrack. The selected positions are shown in Fig. 19.

In our approach, we use the channel hopping to obtain distance difference to two antennas. In COTS RFID reader, the number of the available channels is limited. We evaluate the distance difference with 2, 4, 6, 8, 10, 12, 14, 16 channels. We present the results of the experiments in Fig. 28. The results are shown in Fig. 28. We can find the estimation accuracy increases with the number of used channels. But using multiple channels is time-consuming because the reader has to access the channels in a round-robin manner. We should to set a delicate tradeoff between the estimation accuracy and the time used for initialization. From the results in Fig. 28, we can find that the improvement is limited when using more than 8 channels. Therefore, in our current implementation, we select 8 channels to perform the distance difference estimation in the initialization component.

![](images/1a0414b9c03f984e3347aa724806997328a9a70d0893e46c5450b4c05e71601c.jpg)



![](images/b8e28baf6ba3d30fc63f27292c8b6989681d50bc96c0bc782cf97983d5ccf250.jpg)



![](images/b2cd85aae109065f1e614aa82767f41bb79e179690f1eaf4633b875f6fda1b24.jpg)



Fig. 29. Accuracy of the initialization at different Fig. 30. Accuracy of the Orientation at different positions positions

Fig. 28. Impact of channels on the initialization   
![](images/7ca14a241a3dc04c0507d023d951e6fd3628516a4ffc8fa6e0cee7bb4d16431d.jpg)



(a) Straight rail

![](images/721d1ea5d3368acae07f3c354ab928a8a9d01b4d2c74d182390b0faf2c2c33d2.jpg)



(b) S-shape rail   
Fig. 31. The impact of the orientation calibration

We conduct initialization at each position for 10 times. The results of the location error are shown in Fig. 29. The average location error is 1.7cm. For positions No. 4 and No. 8, the location errors are higher than the average. At the two positions, the tag is set to point to the antennas, which will cause the polarization direction of the tag to be perpendicular to the antenna plane. Therefore, the RSSI will drop significantly, which leads to the lower sampling rate. The results of the orientation error are shown in Fig. 30. The average orientation error is below 7◦ at the 12 positions. The orientation errors at position No. 4 and No. 8 are still higher than others because of the lower sampling rates.

# 6.5 Accuracy of the Calibration

We evaluate the orientation calibration in this experiment. The rotation spots on the rails naturally become the opportunities for orientation calibration. We plot the orientation error before and after calibration at each spot in Fig. 31. From the results, we can find the calibration on the straight rail can reduce the orientation error by 1.4◦, 2.7◦, $3 . 2 ^ { \circ }$ and $3 . 5 ^ { \circ }$ at the four rotation spots, respectively. Due to errors accumulation , the orientation error is increasing during the movement. The calibration reduces the orientation error by 2.4◦, 1.8◦, 2.1◦, 2.6◦, 3.5◦, and $2 . 6 ^ { \circ }$ at the six rotation spots, respectively.

We also attach the tag at the center of the rotation plate and fix the plate’s location. We rotate the plate from 0◦ to $3 6 0 ^ { \circ }$ at a constant speed of $6 ^ { \circ } / s$ . We calculate the orientation error with and without calibration during the rotation process. The results are shown in Fig. 27. The length of the radius is the scale of orientation error. We can find that without calibration, the error is accumulated and can be as large as $1 2 ^ { \circ }$ . In comparison, our calibration algorithm can limit the accumulated error and keep the orientation error below $6 ^ { \circ }$ .

# 6.6 Multi-path effect

In this experiment, we set the linear rail 3m away from the antennas, which is a typical distance in real applica-

![](images/3569063086e2843e5ff414ab0e48b80775863fe2bb1c8149a25e2f301f634689.jpg)



![](images/6c7145a712fa4772a6dc1f4c18017eba45cf24a528471c4737a1390d8b17fe9a.jpg)



Fig. 32. Location error under multi- Fig. 33. Location errors in 3D space path effect

tions. We conduct the experiments under three conditions: clean environment without obstacles; multi-path environment with many obstacles; people moving around to occasionally block the LOS signals. We set the moving speed to the lowest 0.127 m/s. The results are shown in Fig. 32. We can observe the static obstacles introduce few errors to OmniTrack because they don’t affect the LOS signals. However, the people moving around can really degrade the performance because the LOS signals can be blocked occasionally to affect the phase.

# 6.7 3D Tracking

We evaluate the performance in 3D space. The rotator is set to rotate around two axis and we pad the rail up to form a 3D rail. We set the speed as 0.104m/s, 0.186m/s, and 0.232m/s and plot the location errors in Fig. 33. The results show that OmniTrack can be extended to 3D tracking with the average location errors as 6.3cm, 7.5cm, 8.8cm. It proves the generalizability of our orientation-aware phase model.

# 7 CONCLUSION

Accurate tracking of targets is a significant problem in industrial CPS. In this work, we look into the signal propagation process between a RFID reader and a tag. For the first time in the community, we discover and quantify the impact of tag orientation on phase change. Based on this finding, we propose OmniTrack, an orientation-aware RFID tracking approach that is applicable to COTS RFID systems. Unlike the existing phase-based proposals, OmniTrack employs an orientation-aware phase model for target tracking and efficiently deals with various orientation-dependent problems. The evaluation results demonstrate that OmniTrack achieves centimeter-level location accuracy and has significant advantages in tracking targets with varing orientations, compared to the state-of-the-art approaches.

# ACKNOWLEDGMENTS

This work is supported in part by National Key R&D Program of China No. 2017YFB1003000, National Natural Science Foundation of China under grant No. 61772306 and No. 61672240.

# REFERENCES

[1] J. L. Brchan, L. Zhao, J. Wu, R. E. Williams, and L. C. Perez. A ´ real-time rfid localization experiment using propagation models. In Proceedings of IEEE RFID, pages 141–148, 2012.   
[2] W. Cheng, X. Cheng, M. Song, B. Chen, and W. W. Zhao. On the design and deployment of rfid assisted navigation systems for vanets. IEEE Transactions on Parallel and Distributed Systems, 23(7):1267–1274, 2012.   
[3] S. Han, H. Lim, and J. Lee. An efficient localization scheme for a differential-driving mobile robot based on rfid system. IEEE Transactions on Industrial Electronics, 54(6):3362–3369, 2007.   
[4] J. Hightower, R. Want, and G. Borriello. Spoton: An indoor 3d location sensing technology based on rf signal strength. 2000.   
[5] C. Jiang, Y. He, S. Yang, J. Guo, and Y. Liu. 3d-omnitrack: 3d tracking with cots rfid systems. In Proceedings of ACM/IEEE IPSN, pages 25–36, 2019.   
[6] K. R. Joshi, S. S. Hong, and S. Katti. Pinpoint: Localizing interfering radios. In Proceedings of USENIX NSDI, pages 241–253, 2013.   
[7] Q. Lin and Y. Guo. Accurate indoor navigation system using human-item spatial relation. Tsinghua Science and Technology, 21(5):521–537, 2016.   
[8] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu. Anchor-free backscatter positioning for rfid tags with high accuracy. In Proceedings of IEEE INFOCOM, pages 379–387, 2014.   
[9] R. Miesen, F. Kirsch, and M. Vossiek. Holographic localization of passive uhf rfid transponders. In Proceedings of IEEE RFID, pages 32–37, 2011.   
[10] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil. Landmarc: indoor location sensing using active rfid. Wireless networks, 10(6):701–710, 2004.   
[11] J. Ou, M. Li, and Y. Zheng. Come and be served: Parallel decoding for cots rfid tags. IEEE/ACM Transactions on Networking, 2017.   
[12] A. Parr, R. Miesen, and M. Vossiek. Inverse sar approach for localization of moving rfid tags. In Proceedings of IEEE RFID, pages 104–109, 2013.   
[13] K. M. Ramakrishnan and D. D. Deavours. Performance benchmarks for passive uhf rfid tags. In 13th GI/ITG Conference-Measuring, Modelling and Evaluation of Computer and Communication Systems, pages 1–18. VDE, 2006.   
[14] L. Shangguan and K. Jamieson. The design and implementation of a mobile rfid tag sorting robot. In Proceedings of ACM MobiSys, pages 31–42, 2016.   
[15] L. Shangguan and K. Jamieson. Leveraging electromagnetic polarization in a two-antenna whiteboard in the air. In Proceedings of CoNext, pages 443–456, 2016.   
[16] Y. Shen, W. Hu, J. Liu, M. Yang, B. Wei, and C. T. Chou. Efficient background subtraction for real-time tracking in embedded camera networks. In Proceedings of ACM Sensys, pages 295–308, 2012.   
[17] A. A. N. Shirehjini, A. Yassine, and S. Shirmohammadi. An rfidbased position and orientation measurement system for mobile objects in intelligent environments. IEEE Transactions on Instrumentation and Measurement, 61(6):1664–1675, 2012.   
[18] Y. Shu, P. Cheng, Y. Gu, J. Chen, and T. He. Toc: Localizing wireless rechargeable sensors with time of charge. ACM Transactions on Sensor Networks, 11(3):44, 2015.   
[19] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus. Rf-compass: Robot object manipulation using rfids. In Proceedings of ACM MobiCom, pages 3–14, 2013.   
[20] J. Wang and D. Katabi. Dude, where’s my card?: Rfid positioning that works with multipath and non-line of sight. ACM SIGCOMM Computer Communication Review, 43(4):51–62, 2013.   
[21] T. Wei and X. Zhang. Gyro in the air: tracking 3d orientation of batteryless internet-of-things. In Proceedings of ACM MobiCom, pages 55–68, 2016.   
[22] Z. Xiao, H. Wen, A. Markham, and N. Trigoni. Lightweight map matching for indoor localisation using conditional random fields. In Proceedings of IEEE/ACM IPSN, pages 131–142, 2014.

[23] Z. Xiao, H. Wen, A. Markham, N. Trigoni, P. Blunsom, and J. Frolik. Non-line-of-sight identification and mitigation using received signal strength. IEEE Transactions on Wireless Communications, 14(3):1689–1702, 2015.   
[24] J. Xiong and K. Jamieson. Arraytrack: A fine-grained indoor location system. In Proceedings of USENIX NSDI, pages 71–84, 2013.   
[25] C. Xu, B. Firner, Y. Zhang, R. Howard, J. Li, and X. Lin. Improving rf-based device-free passive localization in cluttered indoor environments through probabilistic classification methods. In Proceedings of IEEE/ACM IPSN, pages 209–220, 2012.   
[26] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: Real-time tracking of mobile rfid tags to high precision using cots devices. In Proceedings of ACM MobiCom, pages 237–248, 2014.   
[27] Z. Yang, L. Jian, C. Wu, and Y. Liu. Beyond triangle inequality: Sifting noisy and outlier distance measurements for localization. ACM Transactions on Sensor Networks, 9(2):26, 2013.   
[28] P. Zhang, M. Rostami, P. Hu, and D. Ganesan. Enabling practical backscatter communication for on-body sensors. In Proceedings of ACM SIGCOMM, pages 370–383, 2016.   
[29] C. Zhou and J. D. Griffin. Accurate phase-based ranging measurements for backscatter rfid tags. IEEE Antennas and Wireless Propagation Letters, 11:152–155, 2012.

![](images/83a583bae18fbd0f85c6a39ef1f68d366cdadf3e803a91b72c21d4c2da87c3ed.jpg)



Chengkun Jiang is a Ph.D student in the School of Software, Tsinghua University. He received his B.E. degree in the University of Science and Technology of China, in 2015. His research interests include wireless localization, mobile pervasive computing and Internet of Things. He is a student member of the IEEE and the ACM.

![](images/bdcbbe1e7f2e0b3fca3914a20a05ae985321c73560b496a8d1f80eafc88ec81e.jpg)



Yuan He is an Associate Professor in the School of Software, Tsinghua University. He received his B.E. degree in the University of Science and Technology of China, his M.E. degree in the Institute of Software, Chinese Academy of Sciences, and his PhD degree in Hong Kong University of Science and Technology. His research interests include wireless networks, Internet of Things, pervasive and mobile computing. He is a senior member of the IEEE and the ACM.

![](images/acf84814515586146690a38cedc38e9ab78bce50df733115f31ebccc42b5b172.jpg)



Xiaolong Zheng is currently a Research Associate Professor with the School of Computer Science, Beijing University of Posts and Telecommunications, China. He received his B.E. degree from the Dalian University of Technology, China, in 2011, and his Ph.D. degree from the Hong Kong University of Science and Technology, China, in 2015. His research interests include the Internet of Things, wireless networks, and ubiquitous computing.

![](images/c358c5f02bfbafca6029aed468800c5fc88acd863b06ca8339cb0029e2524136.jpg)



Yunhao Liu received his BS degree in Automation Department from Tsinghua University in 1995, and an MS and a Ph.D. degree in Computer Science and Engineering at Michigan State University in 2003 and 2004, respectively. Being an ACM Fellow and IEEE Fellow, he is now MSU Foundation Professor of Department of Computer Science and Engineering at Michigan State University. This study was conducted when he was Professor at School of Software in Tsinghua University, and he has been on leave

since early 2018 from Tsinghua.