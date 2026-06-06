# Decimeter Level Passive Tracking with WiFi

Kun Qian∗, Chenshu Wu∗, Zheng Yang∗, Chaofan Yang∗, Yunhao Liu∗

∗School of Software and TNLIST, Tsinghua University, China

{qiank10,wucs32,hmilyyz,yangcf10,yunhaoliu}@gmail.com

# ABSTRACT

Pioneer approaches for WiFi-based sensing usually employ learning-based techniques to seek appropriate statistical features, but do not support precise tracking without prior training. Thus to advance passive sensing, the ability to track fine-grained human mobility information acts as a key enabler. In this paper, we proposed Widar , a WiFi-based tracking system that simultaneously estimates human’s moving velocity (both speed and direction) and locations at decimeter level. Instead of applying statistical learning techniques, Widar builds a theoretical model that geometrically quantifies the relationships between CSI dynamics and user’s location and velocity. On this basis, we propose novel techniques to identify PLCR components related to human movements from noisy CSIs and then derive a user’s locations in addition to velocities. We implement Widar on commercial WiFi devices and validate its performance in real environments. Our results show that Widar achieves decimeter-level accuracy, with a median location error of 24cm given initial positions and 36cm without them and a mean relative velocity error of 11%.

# 1. INTRODUCTION

Location awareness is a key enabler for a wide range of applications such as smart homes, elderly care, security monitoring, and asset management. Traditional approaches track a user in an active manner via devices such as smartphones or wearable sensors attached to users [6]. These approaches, however, pose inconvenience since users need to wear or take specific devices and thus are inapplicable in some scenarios such as security surveillance. Other approaches work passively with infrastructure installed in the area of interests, such as cameras and wireless sensor networks (WSNs) [11]. Among them, camera based approaches only provide directional coverage with Line-Of-Sight (LOS) condition and breach user privacy significantly. WSN-based approaches require densely deployed nodes.

Recent innovations in wireless communications shed light

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

HotWireless’16, October 03-07, 2016, New York City, NY, USA

c 2016 ACM. ISBN 978-1-4503-4251-3/16/10. . . \$15.00

DOI: http://dx.doi.org/10.1145/2980115.2980131

on passive human sensing with WiFi signals. Various approaches such as WiVi [3], E-eyes [10], CARM [9] have been proposed for human detection, activity classification, gesture recognition, etc. In principle, these works exploit the phenomenon that human motions distort the multipath profiles during signal propagation. These RF based approaches are more attractive than previous solutions since they do not require any user-carried devices, render omni-directional coverage even in Non-Line-Of-Sight (NLOS) scenarios, and preserve user privacy gracefully.

Existing works, however, cannot track fine-grained human mobility information (including speed, direction, location). Most of them employ learning techniques for gesture and activity recognition by seeking appropriate statistical features of WiFi signals [10, 9]. The key limitations are that they only recognize pre-defined gestures and activities and usually require prior training. User locations are thus sometimes identified from recognized specific activities that are highly location-dependent rather than vice versa [10]. Similarly, a user’s moving velocity can only be derived from successive locations rather than vice versa. These drawbacks heavily confine the applications of passive sensing. To promote WiFi-based human sensing, the ability to track fine-grained mobility information directly from RF signals acts as a fundamental primitive.

In this paper, we proposed Widar , a WiFi-based tracking system that simultaneously estimates human’s moving velocity and locations at decimeter level. Specifically, we attempt to not only track fine-grained continuous locations but also measure the instantaneous velocity (both speed and direction). Instead of applying statistical learning techniques, Widar achieves these goals by deriving velocities and locations both directly from the Channel State Information (C-SI) [4]. Our key observation is that human at different locations with different velocities both induce different changes in signal propagation paths. Thus we build a CSI-mobility model that captures the geometrical constraints between the signal propagation path length change rates (PLCRs) and human’s location and velocity. On this basis, we propose techniques to extract PLCRs related to human movements from noisy CSIs and then derive user’s location in addition to velocity. By doing this, we enable, for the first time, precise passive tracking of a user’s location and moving velocity using cheap and imperfect COTS WiFi devices.

Widar advances the state-of-the-art on WiFi-based sensing from two fronts. First, Widar models the relationship between CSI and human mobility from a geometrical perspective, which brings more favorable features than previous learning based techniques. Such a model helps understand the effects of human mobility on CSI changes. Moreover, our model does not require prior training. Second, Widar provides accurate estimation of human moving velocity, which is beyond the achievements of existing approaches. Moving velocity, as an additional dimension of mobility, stimulates a wide variety of novel applications. For example, velocity analysis provides valuable information for indoor fitness, sport training and entertainment interaction.

![](images/66dc81139584c686be143692927b94e4fc9fe0990bb84c289394f087d5007025.jpg)



(a) Spectrogram

![](images/ecaf925b578a0880b1df92a950399ec36f73bfdb9015f317c405afd47a7c07b0.jpg)



(b) PLCRs   
Figure 1: Extraction of PLCRs

We implement Widar on COTS WiFi devices and conduct extensive experiments in real world. Experimental results demonstrate that Widar yields decimeter-level tracking with a respective median location error of 24cm and 36cm with and without initial positions and a mean relative velocity error of 11%.

Our core contributions are as follows: First, we build a geometrical model that captures the relationships of CSI dynamics and human mobility, which underpins the feasibility of human sensing via a non-learning way. Second, we design a system that simultaneously tracks human location and moving velocity (both speed and direction). We envision this leading-edge capability as a key enabler for future motion recognition applications. Third, we preliminarily implement Widar and validate its performance on COTS hardware. Experimental results show that Widar achieves a decimeter-level accuracy in continuous location tracking.

# 2. UNDERSTANDING CSI-PLCR MODEL

# 2.1 From CSI to PLCR

Wireless signals are subjected to distortions caused by physical interactions, such as reflections and diffractions, between the signals and surrounding objects. Previous works have built a model that formally relates CSI dynamics to multipath changes and explained principles of exploiting CSI dynamics for human activity detection [9]. Specifically, the Channel State Information portrayed by off-the-shelf WiFi NICs can be represented in terms of PLCR components [4]:

$$
H (f, t) = (H _ {s} (f) + \sum_ {k \in P _ {d}} \alpha_ {k} (t) e ^ {- j \frac {2 \pi}{\lambda} \int_ {- \infty} ^ {t} r _ {k} (u) \mathrm{d} u}) e ^ {j \phi_ {f, t}}. (1)
$$

where $P _ { d }$ is the set of dynamic paths, and $H _ { s }$ is the sum of CSIs for static paths. $\alpha _ { k }$ and $r _ { k }$ are the complex attenuation factor and path length change rate (PLCR) for the k-th path respectively. And $\phi _ { f , t }$ is unknown phase shift caused by carrier frequency and timing offset. To eliminate unknown phase offsets, CSI power $| H ( f , t ) | ^ { 2 }$ that contains sinusoids with instantaneous frequency described by PLCR is calculated.

![](images/d895075a20c9b295ad456e9a63200e15edd33aa486950c7830871b91692fc116.jpg)



(a) Human walking trajectories

![](images/4844e016537d15afb1af5d0b6e419198d6dccbb6a84ca66407ecbeeeead3f87b.jpg)



(b) Theoretical PLCR   
Figure 2: Typical motion traces and PLCRs.

Note that CSI power contains all frequency shifts induced by motions of different body parts, internal noises caused by hardware imperfection, and static interferences caused by LOS transmission and static reflectors (e.g. walls). Comparing to frequency shifts caused by human movement, the frequency of impulses and burst noises is generally higher, and the frequency of interference caused by static and quasi-static reflectors and the LOS signal is generally lower. Thus, to remove all irrelevant interferences and noises, we first apply a passband filter (e.g. Butterworth filter) to CSI power to eliminate burst noises and interferences that are out of band of interest. Next, we perform PCA analysis on subcarriers of CSI and calculate the first PCA component, in purpose of extracting representative signals for target motion, as well as reducing the dimensionality of the CSI measurements. Finally, we apply Short-Term Fourier Transform (STFT) to the first PCA component to calculate the spectrogram that describes power distribution of PLCR (Figure 1a), and obtain the globally optimal PLCR series that contain maximum power in the spectrum of interest (Figure 1b).

# 2.2 Limitations In Tracking

The CSI-PLCR model is helpful for activity recognition when approximating human velocity as a fixed function of PLCR, which is, however, insufficient for tracking. To inversely use PLCR exposed by CSI for tracking, two types of ambiguities have to be solved.

From PLCR to target velocity. While PLCR to some extent exposes the moving velocity, it actually depends on both velocity and location of target reflector. As depicted in Figure 2a, target $P _ { 1 }$ is on the perpendicular bisector of the link; $P _ { 2 }$ is parallel with the link; $P _ { 3 }$ is on an ellipse whose focuses are the transmitter and receiver. Suppose an identical constant velocity and the same length of each trace, we plot their respective PLCRs in Figure 2b, which turn out to be different from each other. Thus, while PLCR provides some clues of human motion, it can not immediately characterize the moving status. An advanced model that outputs human mobility information from PLCRs is needed for tracking.

Loss of the sign. While CSI power excludes unknown phase offsets, it also loses the sign of PLCR. As the sign of PLCR indicates whether the reflector moves towards or away from the link, without the sign, we are not able to obtain the moving direction or track the locations.

# 3. MODELING OF CSI-MOBILITY

In this section, we attempt to build a model to relate PLCR to human moving velocity together with location directly. We achieve this by considering the geometrical constraints of reflection paths and human movements. As shown in Figure ${ \mathrm { 3 a , } }$ taking the transmitter and receiver as ellipse focuses, the length of reflecting path decides which ellipse the target is on. The target velocity \~v can be orthogonally decomposed as radial velocity $\vec { v _ { r } }$ and tangential velocity \~vt. Only radial velocity $\vec { v _ { r } }$ changes the reflecting path length.

![](images/67e3bb99d899725da24fb5bddc6fa047222abad6cfab981d5fea63a908887b5d.jpg)



(a)

![](images/22a9f3f34daff94c3c02fb6ca5c6fb75651d45ebea11dee53dabc649566f31bb.jpg)



(b)

![](images/8421eab3f9dce8617ad7601b1d44c006688df3595d5017807b87d37adf04c62c.jpg)



(c)

![](images/c44143b3b8843924b709d3f872b344cd2af50e1b4e3193817719928be5ef61c7.jpg)  
Figure 3: Relation between target velocity and PLCR: (a)one link, (b)two links, (c)three links; and (d)consecutiveness of target movements.

Given the posthe i-th link as \~l(i) $\vec { l } _ { t } ^ { ( i ) } = ( x _ { t } ^ { ( i ) } , y _ { t } ^ { ( i ) } ) ^ { T } , \vec { l } _ { r } ^ { ( i ) } = ( x _ { r } ^ { ( i ) } , y _ { r } ^ { ( i ) } ) ^ { T }$ ver of, the current target position as $\vec { l _ { h } } = ( x _ { h } , y _ { h } ) ^ { T }$ , the target velocity as $\vec { v } = ( v _ { x } , v _ { y } ) ^ { T }$ , PLCR as $r ^ { ( i ) }$ , and the sign of PLCR as $s ^ { ( i ) }$ , the relation between PLCR and target velocity can be algebraically described as follows:

$$
a _ {x} ^ {(i)} v _ {x} + a _ {y} ^ {(i)} v _ {y} = s ^ {(i)} | r ^ {(i)} |, \tag {2}
$$

$$
a _ {x} ^ {(i)} = \frac {x _ {h} - x _ {t} ^ {(i)}}{| | \vec {l} _ {h} - \vec {l} _ {t} ^ {(i)} | |} + \frac {x _ {h} - x _ {r} ^ {(i)}}{| | \vec {l} _ {h} - \vec {l} _ {r} ^ {(i)} | |}, \tag {3}
$$

$$
a _ {y} ^ {(i)} = \frac {y _ {h} - y _ {t} ^ {(i)}}{| | \vec {l} _ {h} - \vec {l} _ {t} ^ {(i)} | |} + \frac {y _ {h} - y _ {r} ^ {(i)}}{| | \vec {l} _ {h} - \vec {l} _ {r} ^ {(i)} | |}.
$$

Note that single link is insufficient for velocity estimation, due to loss of tangential velocity $\vec { v } _ { t }$ . Fortunately, with more links, we are able to solve the ambiguity and derive the true velocity. By add one or two extra links, the number of velocity candidates reduces to four and two respectively, as shown in Figure 3b and 3c. Theoretically, aggregating relation of all L links at time $k ,$ we have:

$$
\mathbf {A} \vec {v} = \mathbf {R} \vec {s}, \tag {4}
$$

$$
\mathbf {A} = \left( \begin{array}{c c c c} a _ {x} ^ {(1)} & a _ {x} ^ {(2)} & \dots & a _ {x} ^ {(L)} \\ a _ {y} ^ {(1)} & a _ {y} ^ {(2)} & \dots & a _ {y} ^ {(L)} \end{array} \right) ^ {T},
$$

$$
\mathbf {R} = \operatorname{diag} \left( \begin{array}{c c c c} | r ^ {(1)} | & | r ^ {(2)} | & \dots & | r ^ {(L)} | \end{array} \right),
$$

$$
\vec {s} = \left( \begin{array}{c c c c} s ^ {(1)} & s ^ {(2)} & \dots & s ^ {(L)} \end{array} \right) ^ {T}.
$$

With the knowledge of signs of PLCR, the optimal solution for \~v becomes:

$$
\vec {v} _ {\text { opt }} = (\mathbf {A} ^ {T} \mathbf {A}) ^ {- 1} \mathbf {A} ^ {T} \mathbf {R} \vec {s}. \tag {5}
$$

However, since each link is associated with an unknown sign of PLCR, there are always more variables than equations, no matter how many links are added. To resolve ambiguity of direction, we resort to introduce constraints based on the observation of consecutiveness of the target movements in real world. Specifically, while human is moving, the directions of consecutive velocities, within a certain small time slot, are likely to be similar, due to the nature limitations on people’s moving accelerations and high sampling rate supported by commercial devices. Figure 3d illustratively demonstrates the effect of the constraint. Suppose the last measurement of target velocity is $\vec { v } _ { k - 1 }$ . At time $k ,$ for the two symmetric velocity candidates, ${ \vec { v } } _ { k }$ and $\vec { v } _ { k } ^ { \prime }$ with the smallest fitting error, ${ \vec { v } } _ { k }$ holds a significantly higher probability to be the current velocity since it is almost in the same direction as preceded $\vec { v } _ { k - 1 }$ .

Based on such constraints, the optimal solution for $\vec { s _ { k } }$ can be obtained by minimizing following error function:

$$
\vec {s} _ {k, \text { opt }} = \underset {\vec {s} _ {k} \in \{- 1, 1 \} ^ {N}} {\text { argmin }} (\text { err } _ {l, k} + \beta \cdot \text { err } _ {v, k}),
$$

$$
\operatorname{err} _ {l, k} = \left| \left| \mathbf {A} _ {k} \vec {v} _ {k, \text { opt }} - \mathbf {R} _ {k} \vec {s} _ {k} \right| \right|, \tag {6}
$$

$$
\operatorname{err} _ {v, k} = | | \mathbf {A} _ {k} \vec {v} _ {k, \text { opt }} - \mathbf {A} _ {k - 1} \vec {v} _ {k - 1, \text { opt }} | |,
$$

where $_ { \mathrm { e r r } _ { l , k } }$ is the mean square error that quantifies inconsistency between PLCR and solved velocity. $\mathrm { e r r } _ { v , k }$ is the velocity deviation error that quantifies the deviation of current velocity against to last velocity estimation. $\beta$ is the weight factor to prevent excessive impact of the error term $\mathrm { e r r } _ { v } .$ The rationality lies in that the optimization procedure determines two best fitted candidates mostly based on the mean square error while applies the second velocity deviation error term to exclude one of them. While there are in total $2 ^ { L }$ candidates for initial directions at the start point, the trace converges to 2 solutions after several steps of tracking in Equation 6. Thus, to decide the initial direction at the start point, we set $\vec { v } _ { 0 }$ as a small uncertainty that takes values in a pair of symmetric vectors.

Upon obtaining current velocity $\vec { v } _ { k , \mathrm { o p t } }$ , the target location can be updated as:

$$
\vec {l} _ {k + 1} = \vec {l} _ {k} + \vec {v} _ {k, \text { opt }} \cdot \Delta t, \tag {7}
$$

where $\Delta t$ is the interval between two consecutive measurements. And the target velocity thereafter can be successively estimated in the same way.

# 4. TRACKING VELOCITY & LOCATION

To fully track human location in addition to the velocity, Widar has to opportunistically pinpoint human in order to provide initial target location and avoid accumulative tracking errors. Lacking external information for references, we propose a pseudo self-calibration scheme for such purpose.

Trace Refinement. Opportunistic location hints are generally necessary for calibration in a tracking system to avoid accumulative errors. Since we do not have extra information to serve as precise initial locations and for calibration, we employ a pseudo-calibration approach based on trace segmentation to refine the tracking results and guarantee the accuracy. As Widar may misjudge the velocity direction in some cases especially when the user takes a sharp turning or walks very slowly, we segment the trace at these vulnerable moments and re-initialize the tracking process for each new segment, in order to avoid error accumulation.

![](images/16446ee343a0da4872dfd3647166423256e541e62e611e6ed12db6afbb0f32f9.jpg)



(a) Velocity amplitude

![](images/8f1be49bf8bfe08560d59e619c54bc1fb1b7ce5873d159c2d05feed4f7b9b466.jpg)



(b) Velocity direction

![](images/e292ff32468973d6c30c08292a846fbd235d8e013e3b08007735224602d8f61d.jpg)



(c) Location

![](images/bf246bc76ff833d0cd37fd8050354622f0fbdaa61fd65fa4cc4f372b79453900.jpg)



![](images/f618a860b661049a5a68fa5d27199539bcadec0a835041949e72e33064934d53.jpg)



Figure 5: Examples of tracking results   
Figure 4: Overall performance of velocity and location tracking

For each individual segment, Widar explores all potential candidates of the trace and accounts for extensive constraints to sift out the invalid ones. These constraints include the relation between link-reflector distance and CSI power variance, the limitation of normal walking speed and normal turning angular, and the link coverage.

Initial location estimation. Widar tracks human movements via velocity, rather than direct location estimation. Consequently, an initial location is needed. Due to limitations of transmission bandwidth, number of antennas and hardware imperfections, however, present COTS WiFi NICs are not suitable for non-learning model-based localization [5, 2, 1]. To complement the tracking process while avoiding learning and training, Widar iteratively search through the whole tracking area to identify a location that yields the least fitting error of the trace as the initial location.

The search-based method works effectively in our settings and requires no extra information hints. Yet some inherent disadvantages do exist, such as complex computation, over fitting problem and potential location errors. Non-learning localization techniques should be proposed and incorporated, which we leave as future works.

# 5. FEASIBILITY RESULTS

Experiment Setup. We implement Widar using three off-the-shelf mini-desktops equipped with Intel 5300 NIC. One mini-desktop with one external antenna works as the transmitter, while the other two mini-desktops, each with three external antennas, work as receivers. To obtain CSI measurements from WiFi data frames, all mini-desktops are installed with Linux 802.11n CSI Tool [4] and set up to inject in monitor mode on Channel 161 at 5.825GHz. A transmission rate of 2000Hz is adopted. Different deployment schemes are designed for Widar , for all of which both transmitter and receivers are deployed almost along the same side or in a corner of the tracking area to avoid severe shadowing effect caused by LOS obstruction. The effective area of experiment is 4m×4m. We design traces with various lengths, directions and shapes (such as line, curve, rectangular, circle and fold line, etc.), and collect a total of 580 traces from 5 volunteers. The volunteers include 4 males and 1 female, with heights in the range of 1.6m to 1.8m, and ages in the range of 20 to 35. The ground truth locations and velocities of human trajectories are obtained via visual methods.

Performance in Velocity Tracking We first report performance of Widar on tracking target velocity, in terms of both speed and direction. For speed, we compare Widar with a na¨ıve method: Max PLCR, which converts half of the largest PLCR among all links as target speed. In addition, we show the estimation errors when only one link is available (denoted as Single PLCR). Figure 4a plots the relative speed errors of three methods over all trajectories. As seen, Widar achieves the highest accuracy with a median error of 11%, while those of Max PLCR and Single PLCR are 17% and 34% respectively. The favorable performance of Max PLCR attributes to the deployment of links, where links are deployed in two orthogonal directions in the experiment.

While both Widar and Max PLCR report highly accurate velocity amplitude, Widar further provides velocity direction, which is necessary for tracking. As shown in Figure 4b, the deviation of more than 80% direction measurements are within 20◦, which is sufficient for human tracking.

Performance in Location Tracking Figure 4c shows the tracking errors across all trajectories. As illustrated, with knowledge of accurate initial location, Widar achieves high tracking accuracy with a median tracking error of 24cm. Without initial location, the performance slightly degrades yet the median tracking error is still as low as 36cm, guaranteeing decimeter-level accuracy. Integrated with velocity tracking, Figure 5 shows illustrative tracking results.

# 6. RELATED WORK

RF-based Active Tracking. Active motion tracking, which essentially localizes radio devices attached on objects, has been studied in depth. Various signal features, from RSSI [15] to CSI [7], have been exploited as location fingerprints. Another mainstream of active motion tracking systems are built upon phased antenna array [6]. However, these tracking schemes requires dedicated radio devices that expose accurate phase information of antenna array, which is unavailable in COTS WiFi devices due to unknown carrier frequency offset [9].

RF-based Passive Motion Tracking. Passive motion tracking exploits signals reflected off objects to recognize and localize objects using specialized wireless devices. Isolating certain reflections can be done in either time domain using pulse radar or frequency domain using FMCW radar [2, 1]. WiVi [3] proposes a MIMO interference nulling algorithm to focus the receiver on moving targets. In contrast, however, isolating certain reflections can not be processed on COT-S WiFi devices due to limited bandwidth, constant carrier frequency and asynchronization between transmitter and receiver.

As RF techniques such as RFID and mmWave provide accurate signal phase information, processing signals in phase domain enables tracking with sub-wavelength accuracy [12, 14]. WiDeo [5] jointly estimates ToF and AoA to identify all reflectors and extract moving ones by comparing successive estimation. WiDraw [8] tracks in-air hand motion by computing AoA of blocked incident signals. Similarly, phase information used in these tracking systems is unavailable in COTS WiFi devices. Radio Tomography Imaging [11] deploys a mesh of sensors to enclose sensing area and locate persons by identifying shadowed area with weak RSS or high variation. In contrast, Widar leverages reflection instead of shadow effect, and thus requires fewer sensors while achieves finer tracking resolution.

WiFi-based Gesture and Activity Recognition. WiFibased activity recognition attracts considerable research interests recently [10, 9]. These works mainly target at gesture or activity recognition instead of location tracking, let alone speed estimation. As such, most of them employ learningbased solutions for recognition. Our CSI-Mobility model is inspired by CARM [9], yet Widar reveals the relationships of CSI dynamics and real human moving velocity and enables simultaneous estimation of human velocities and locations.

# 7. CONCLUSION AND FUTURE WORK

In this paper, we propose a WiFi-based passive tracking system Widar that simultaneously estimates human’s location and velocity at decimeter level. We build a model that geometrically quantifies the relationships between CSI dynamics and human mobility. And several novel techniques are proposed to translate this model into a fine-grained tracking system. Widar advances the state-of-the-art on WiFibased sensing from two fronts, theoretical model and nonlearning characteristics.

We also recognize the limitations of this preliminary study and plan to work on the following parts:

Model-based contactless localization. Despite the pseudo self-calibration algorithm in Widar , accumulative errors still may increase over long traces. Thus, location hints obtained by certain passive localization technique, even not accurate enough, benefit initialization and re-calibration for tracking. Non-learning contactless localization may be realized with wider bandwidth, larger number of antennas and purer phase information. Given that splicing multiple CSI channel together to provide wider bandwidth is shown to benefit active localization [13], extending related techniques to enable contactless localization on COTS devices is part of our future work.

Deployment of WiFi links. Widar exploits reflections and diffractions of signals for the tracking model and omits the shadow effects due to blockage of LOS, which, however, may also cause significant CSI variations. To steer by severe shadowing effects, we deploy WiFi links along walls or other obstructions such that human does not traverse through the LOS paths in the tracking area. Nevertheless, shadowing effect has been well studied and utilized in Radio Tomography Imaging [11], despite of a dense sensor networks required to be deployed to enclose the monitor area. In the future, we will try to unify the two tracking models to further release the constraints on deployment of WiFi links.

Velocity-based motion recognition. Widar is capable of deriving precise moving velocity of human movements (represented by human torso). We plan to extend the velocity estimation capability to other body parts in our future works. By doing this, we are able to better understand user’s physical motion and achieve finer-grained gesture and activity recognition, using velocity-based physical characteristics, instead of previous statistical features.

Multiple human tracking. Recently, WiTrack2.0 [1] enables multiple human localization by successive silhouette cancellation using FMCW signals, which is not achieved in its initial version WiTrack1.0 [2]. We also attempt to track multiple people by iteratively cancelling the PLCR components of each target. The results, however, are not satisfiable since the movements of different people are similar and their corresponding frequency components overlap a lot. Enabling tracking of multiple targets remains an open and challenging problem in the future.

# 8. REFERENCES

[1] F. Adib, Z. Kabelac, and D. Katabi. Multi-person localization via rf body reflections. In USENIX NSDI, 2015.   
[2] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller. 3d tracking via body radio reflections. In USENIX NSDI, 2014.   
[3] F. Adib and D. Katabi. See through walls with wifi! In ACM SIGCOMM, 2013.   
[4] D. Halperin, W. Hu, A. Sheth, and D. Wetherall. Predictable 802.11 packet delivery from wireless channel measurements. ACM SIGCOMM, 2011.   
[5] K. Joshi, D. Bharadia, M. Kotaru, and S. Katti. Wideo: Fine-grained device-free motion tracing using rf backscatter. In USENIX NSDI, 2015.   
[6] M. Kotaru, K. Joshi, D. Bharadia, and S. Katti. Spotfi: Decimeter level localization using wifi. In ACM SIGCOMM, 2015.   
[7] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka. You are facing the mona lisa: spot localization using phy layer information. In ACM MobiSys, 2012.   
[8] L. Sun, S. Sen, D. Koutsonikolas, and K.-H. Kim. Widraw: Enabling hands-free drawing in the air on commodity wifi devices. In ACM MobiCom, 2015.   
[9] W. Wang, A. X. Liu, M. Shahzad, K. Ling, and S. Lu. Understanding and modeling of wifi signal based human activity recognition. In ACM MobiCom, 2015.   
[10] Y. Wang, J. Liu, Y. Chen, M. Gruteser, J. Yang, and H. Liu. E-eyes: device-free location-oriented activity identification using fine-grained wifi signatures. In ACM MobiCom, 2014.   
[11] B. Wei, A. Varshney, N. Patwari, W. Hu, T. Voigt, and C. T. Chou. drti: Directional radio tomographic imaging. In ACM/IEEE IPSN, 2015.   
[12] T. Wei and X. Zhang. mtrack: High-precision passive tracking using millimeter wave radios. In ACM MobiCom, 2015.   
[13] Y. Xie, Z. Li, and M. Li. Precise power delay profiling with commodity wifi. In ACM MobiCom, 2015.   
[14] L. Yang, Q. Lin, X. Li, T. Liu, and Y. Liu. See through walls with cots rfid system! In ACM MobiCom, 2015.   
[15] Z. Yang, C. Wu, and Y. Liu. Locating in fingerprint space: wireless indoor localization with little human intervention. In ACM MobiCom, 2012.