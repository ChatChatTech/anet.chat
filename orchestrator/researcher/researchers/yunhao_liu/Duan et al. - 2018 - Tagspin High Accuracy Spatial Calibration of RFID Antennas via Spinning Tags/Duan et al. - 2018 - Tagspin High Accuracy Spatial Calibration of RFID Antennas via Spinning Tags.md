# Tagspin: High Accuracy Spatial Calibration of RFID Antennas via Spinning Tags

Chunhui Duan, Student Member, IEEE, Lei Yang, Member, IEEE, Qiongzheng Lin, Student Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract—Recent years have witnessed the advance of RFID-based localization techniques that demonstrate high precision. Many efforts have been made locating RFID tags accurately with a mandatory assumption that the RFID reader’s position is known in advance. Unfortunately, calibrating reader’s location manually is always time-consuming and laborious in practice. In this paper, we present Tagspin, an approach using COTS tags to pinpoint the reader (antenna) quickly and easily with high accuracy. Tagspin enables each tag to emulate a circular antenna array by uniformly spinning on the edge of a rotating disk. We design an SAR-based method for estimating the angle spectrum of the target reader. Compared to previous AoA-based techniques, we employ an enhanced power profile modeling the relative signal power received from the reader along different spatial directions, which is more accurate and immune to ambient noise as well as measurement errors caused by hardware characteristics. Besides, we find that tag’s phase measurements in practice are related to its orientation. To the best of our knowledge, we are the first to point out this fact and quantify the relationship between them. By calibrating the phase shifts caused by orientation, the positioning accuracy can be improved by 3.7×. We have implemented Tagspin with COTS RFID devices and evaluated it extensively. Experimental results show that Tagspin achieves mean accuracy of 7.3cm with standard deviation of 1.8cm in 3D space.

Index Terms—RFID, reader localization, Tagspin.

# 1 INTRODUCTION

R ADIO Frequency IDentification (RFID) is a rapidly develop-ing technology which uses RF signals for automatic iden- ing technology which uses RF signals for automatic identification of objects. Many new RFID localization systems have shown high precision, such as [1], [2], [3], [4]. Much of the attention has been paid on how to accurately locate the RFID tags instead of readers. Many applications would benefit from accurate tag localization or tracking. For example, we can quickly check whether the books on certain shelves are out of order in a library, aid in automatic customer checkout in a supermarket, enable human-machine interaction with the tag attached on the finger, etc. However, considering previous work locating tags, all of them have a mandatory precondition that the reader’s location is known or calibrated in advance. This calibration procedure is often conducted manually, which can be time-consuming, laborious and inaccurate, especially when many antennas are required.

To illustrate this, we repeat the experimentation in [4], trying to give a practical example. In summary, the inconvenience of calibration are mainly three folds: a) time cost: It takes us 20 ∼ 30 minutes to calibrate all four antennas and the more antennas needed, the more time spent. b) energy cost: To get the antennas’ accurate locations, we need to measure their coordinates carefully along the three spatial axes, which is quite exhausting and boring. c) accuracy cost: To achieve high accuracy, more antennas are needed with each of them further apart. This however, would add more errors to the calibration results, which in turn will decrease the final tag localization precision. So our point is, to accomplish the goal of fine-grained tag localization, the calibration for RFID reader antennas is very necessary and existing manual method is not satisfactory enough. To tackle this, a simple, convenient and accurate way of calibration is in pressing demand.

At first glance, why not use the existing methods locating tags to pinpoint readers? One dominate approach locating tags is to deploy plenty of tags as references [1], [5]. The difference of RSSI [5] or multi-path profile [1] between the target and reference tag is used as a metric for their spatial distance. The nearest neighbours of the target tag are identified and the target tag’s location is considered as the average of the neighbors’. Apparently, the reader’s location is independent of reference tags for this approach, and thereby cannot be inferred by tags, even knowing all tags’ locations. Another method is Synthetic Aperture Radar (SAR), which has been widely used for mapping the topography of the Earth’s surface, and is also introduced for RFID localization recently. Specially, a moving reader takes snapshots of the tag’s signals at different spatial directions. The snapshots mimic a largescale antenna array. Then, the standard antenna array equations on the signals are used to compute the relative powers received from the transmitting source along different spatial directions. It, however, is infeasible for us to move the reader when our goal is to calibrate it.

In this paper, we present a light-weighted, inexpensive yet highly precise reader localization system with centimeter-level positioning accuracy using a few infrastructural reference tags. Rather than relying on the dynamic movement of reader to produce a virtual antenna array, Tagspin reverses the approach by relying on the spinning motion of infrastructural tags to produce predicable, distinguishable and periodic signal snapshots. These snapshots caught from each spinning tag mimic a circular antenna array. The reason why we prefer circular array to linear array is that to simulate the same number of virtual tags, linear array requires more space than circular array and is sometimes unpractical especially in space-limited environment. Besides, moving the tag along a line is also more troublesome than making it travel on a circle. In our experiment, to simulate circular antenna array, we simply make the tag spinning by attaching it onto the edge of a disk which slowly rotates with a stable speed. An SAR-based method is designed to estimate the relative power profile over all possible spatial angles. The profile has a sharp peak at the real direction from tag to reader. Specially, the direction starting from the spinning tag with known location determines a straight line that passes through or nearby the target reader. More than two (or more) lines are generated by using two (or more) spinning tags in 2D plane and even 3D space. Finally, the target can be pinpointed from the intersection of these lines. To illustrate Tagspin’s approach, Fig. 1(a) shows a toy example with three spinning tags. Each tag moves along a predefined circular track with a uniform speed. Fig. 1(b)-1(d) show estimated power profiles for the three spinning tags respectively, using standard circular antenna array equations [6]. It is clear from this figure that the sharp peak in the power profile indicates the reader’s position relative to tag. Finally, the reader’s position is revealed by intersecting the three straight lines.

![](images/c7dada0e788cff64b4b97e13b5c5fa498ccc02bda65dc2949525237115ecb28f.jpg)



(a) Scene

![](images/5bd6ff6993f215b337e021dedc27df290571bfe4201696da1318ecf950fdab47.jpg)  
(b) T1

![](images/cdccd2ab2dbceaa339d7b14eacc236933576bab68b6864218398f472d3debd9f.jpg)  
(c) T2

![](images/817f227e6f1a1ade05edf04143412e774c818a061e92b55201bb7e51a33a734f.jpg)  
(d) $T _ { 3 }$   
240  270  300  240  270  300  240  270  300 Fig. 1: Illustration of Tagspin. (a) The signal snapshots of three spinning tags anchored in the infrastructure are used to mimic three circular antenna arrays. (b)-(d) Power profile. There is a sharp peak at the direction of the reader relative to the tag.

While some people may think the reader localization is a dual problem of tag localization because we have to know the locations of the reference tags in advance to give absolute location of the reader, our key point is that we just need a few pre-deployed infrastructural tags to easily and precisely locate even multiple target antennas at the same time. The typical dimension of a tag (e.g. Alien Squiglette with size of 7cm × 0.9cm) is sufficiently small compared with the antenna (e.g. Impinj Guardwall Antenna with size of 70cm × 40cm × 10cm). Tags’ small dimensions and battery-free characteristics enable us to deploy them everywhere with few restrictions and more flexibility. Besides, compared to traditional manual approaches which need to calibrate the antennas one after another, our schema can simultaneously calibrate as many antennas as the reader can support, which significantly increase the performance. With the reader antennas accurately calibrated, further applications can be promoted, $e . g .$ , locating many more surrounding tags that are of interest.

Contributions: In summary, this paper makes the following contributions:

• First, Tagspin gives an innovative improvement to the previous AoA-based localization, namely an enhanced version of spinning tag’s power profile is proposed. By doing so, the phase measurement error is well handled meanwhile both the positioning accuracy and robustness are reinforced.   
• Second, in the scope of our knowledge, Tagspin is the first to put forward the finding that there exists a regular pattern between tag’s phase measurements and its orientations. We quantify this interplay and calibrate corresponding phase shifts to make localization more accurate.   
• Third, we implement the system with Commercial Off-The-Shelf (COTS) RFID products and conduct comprehensive evaluation. It’s shown that Tagspin is light-weighted, time-saving and can provide mean accuracy of 7.3cm even in 3D space, which is fairly good compared to the reader antenna’s size (usually decimeter level).

The rest of the paper is organized as follows. We review related work in §2. The main design of Tagspin is overviewed in §3. We present the interrelation of tag’s phase and orientation in §4. The details of our proposed power profile and localization method are elaborated in $\ S 5$ and $\ S 6 .$ . The implementation of Tagspin is described in $\ S 7$ and evaluated in §8. Finally, we conclude this paper in $\ S 9$ .

# 2 RELATED WORK

There exists considerable amount of research work on positioning in RFID and other wireless area. We present the most related and recent work in this section, grouped into RF-based and SARbased.

RF-based localization: Recent years have witnessed the flourishing of myriad localization technologies, especially in RF domain [7], [8], [9], [10]. Mainstreaming work in this domain adopts Received Signal Strength Indicator (RSSI) as the fingerprint or distance ranging metric for localization [11], [12], [13]. LandMarc [5] and VIRE [14] are early work of RFID localization. LandMarc firstly employs the idea of having extra fixed location reference tags to help location calibration and VIRE further uses virtual reference tags to enhance accuracy of positioning. Bekkali et al. use Kalman filtering to build a probabilistic model to reduce the effect of RSS error measurement [15]. Chintalapudi et al. [16] propose a solution which leverages the constraints of wireless propagation physics to improve localization accuracy without pre-deployment efforts. Zee [17] is a typical fingerprinting based indoor localization system, which utilizes crowdsourcing to make the site-specific calibration procedure zero-effort. Besides, AoA (Angle of Arrival) information is another important location indicator drawing many researchers’ attention, which works by measuring the phase difference between the received signals at different antennas [18], [19], [20], [21]. ArrayTrack [22] is an indoor localization system using MIMO-based techniques at commodity multi-antenna APs to track wireless clients at a fine granularity in real time. PinPoint [23] proposes a novel algorithm that accurately computes the line of sight angle of arrival, allowing multiple collaborating access points to localize interfering transmitters on the order of centimeters even under strong multi-path propagations. BackPos [24] utilizes the relationship between tag’s detected phase and distance to enable hyperbolic positioning via COTS devices. While much attention has been paid on locating RFID tags, little concern has been shown for the issue of reader localization. Luo et al. [25] are the few pioneers that concentrate on the problem of reader localization. They arrange tags at fixed position in advance for reference and acquire information to calculate position of reader (antenna) by rotating antenna. It can be applied to localize robot which configures reader.

SAR: SAR is firstly used in military Radar system for both geographic imaging and object localization with the help of antenna array. Recently there is a growing interest in borrowing this idea to pervasive wireless localization domain. PinIt [1] leverages SAR technique to extract the multi-path profile of RFID tags for the tag localization in non-line-of-sight scenario. Miesen et al. [26] present a holographic method to show tag’s real position with phase values sampled from a synthetic aperture by an RFID reader. Parr et al. [27] extend the work in [26] to realize trajectory reconstruction of RFID tags through inverse synthetic aperture. The authors in [21] utilize phase difference between pairs of antenna elements in each antenna array to estimate the AoA information for tag localization. [28] gives an overview of phase based ranging techniques, focusing on the phase difference of arrival method measured in frequency domain (FD-PDoA) and introduces an experimental RFID front-end prototype used for FD-PDoA measurements. In [29], by combining both the phase-of-arrival (PoA) of the backscattered tag signal and the phase-difference-ofarrival (PDoA) of successive measurements, the two-dimensional position and movement of the RFID transponder is estimated simultaneously. Ubicarse [30] performs a new formulation of SAR on handheld devices twisted by their users to enable fine-grained indoor localization. Tagoram [4] successfully handles the thermal noise and device diversity and achieves mm-level tag localization accuracy in 2D plane.

Other RFID related issues: Instead of getting the absolute locations, many applications would benefit from knowing the relative locations (order) of a set of objects. The authors in [31] propose an approach called Spatial-Temporal Phase Profiling which leverages phase values to calculate the spatial ordering among tags to realize RFID-based relative object localization. Frogeye [32] focuses on the problem of the slightest tag motion and tries to perceive it through the radio signal strength changes combing the background subtraction algorithm in computer vision. Season [33] deals with collision in large-scale RFID systems and proposes a schema of shelving interference and joint identification to improve throughput. Liu et al. [34], [35], [36] have studied issues related to missing tag detection and proposed multiple hashing and time-efficient algorithms.

Our work is inspired by the above works in SAR and phasebased tag localization domain, but we focus on the problem of reader localization instead. Overall, Tagspin has three main virtues. First, we only need to deploy a few tags (2 is enough) in the target space. Such few tags barely take any effect on the reading performance of existing RFID systems. Second, while previous work leveraging tag’s phase value in positioning works on the premise that phase measurements are resistant against tag orientations, Tagspin first points out that tag’s phase value is susceptible to its orientation and quantifies the interrelation between the two. Third, even if low sample rate and uncertain measurement error exist, Tagspin still maintains good accuracy with simple manipulation.

# 3 TAGSPIN OVERVIEW

Tagspin is a fined-grained UHF RFID localization system targeting to pinpoint readers, providing a resolution on the order of a few centimeters, much smaller than the read range of UHF RFIDs. Ultra-low cost UHF tags (5-10 cents each) become the preferred choice of many industrial applications. Following the common practices, we concentrate on the deployed UHF tags.

Tagspin deploys a set of spinning tags in the environment. Its infrastructure also includes a central localization server which stores the spinning tags’ locations, moving speeds and calibration data. The reader interrogates the nearby spinning tags for a while and sends the signal snapshots to the server. Then Tagspin goes through the following three steps at a high level to locate the RFID reader:

• Acquiring phase shifts. Tagspin acquires and calibrates the phase shifts from the signal snapshots of spinning tags using the technique in §4.   
• Generating angle spectrum. Tagspin generates an angle spectrum for each spinning tag as described in $\ S 5$ .   
• Locating the target reader. Tagspin pinpoints the target reader using multiple angle spectrums (see §6).

The technical details on the above steps are elaborated in the next few sections.

# 4 ACQUIRING PHASE SHIFTS

In this section, we firstly model the phase shifts of spinning tag, and then introduce how to eliminate the influence from the tag’s orientations.

# 4.1 Modeling Phase Shifts

The SAR-based localization works by comparing the phases of the received signals at multiple antennas. Suppose d(t) is the distance between the reader and tag at time t, the signal traverses a total distance of 2d(t) back and forth in RFID systems. The total phase rotation outputs by the reader equals [37]:

$$
\theta (t) = \left(\frac {2 \pi}{\lambda} \times 2 d (t) + \theta_ {\mathrm{div}}\right) \bmod 2 \pi \tag {1}
$$

where λ is the wavelength. The term $\theta _ { \mathrm { d i v } }$ is called diversity term, which is related to the hardware characteristics. The phase is a periodic function with period 2π radians which repeats every $\lambda / 2$ in the distance of backscatter communication.

Now let us consider the geometric relationship between the spinning tag and the reader, as shown in Fig. 2(a). Specifically, suppose the spinning tag $T$ rotates at the origin O with a uniform angular velocity $\omega .$ . The radius of the track equals r. Let $\phi$ and ωt denote the angles of reader and tag at time t in terms of the origin. Then the angle ∠T OR equals ωt−φ. When R is relatively far from the tag, as the figure shows, $d ( t )$ can be approximated as |AR| where $T A \perp O R$ . Thus, in this case we can get the distance d(t) as

$$
d (t) \approx D - r \cos (\omega t - \phi) \tag {2}
$$

where $D = | O R |$ , the distance between the origin and reader. Fig. 2(b) shows the second case when $\vert T R \vert > \vert O \bar { R } \vert$ . The ∠T OA turns to $( \omega t - \phi - \pi )$ . Then

$$
d (t) \approx D + r \cos (\omega t - \phi - \pi)
$$

$$
= D - r \cos (\omega t - \phi)
$$

![](images/71f37f263b651027c422308785152efe77dfa0f6ab50471dd450d7c630276d27.jpg)



(a) |T R| ≤ |OR|

![](images/3d5907d4d2f41ca17645914f97920a6a08583fbce5f55fe671a6175fc2fd7496.jpg)



(b) |T R| > |OR|   
Fig. 2: Geometric relationship between spinning tag T and reader R. (a) shows the first case where the tag $| T R | \leq | O R | .$ . (b) shows the second case where the tag $| T R | > | O R |$ . In any case wherever the tag locates at, the phase value has the same mathematical expression.

which has the same mathematical expression as that in the first case. Apparently, $d ( t )$ can be any value in $\left[ \boldsymbol { D } - \boldsymbol { r } , \boldsymbol { D } + \boldsymbol { r } \right]$ . Finally, substituting Eqn. 2 into Eqn. 1, the received signal phases have the following expression.

$$
\theta (t) = \left(\frac {4 \pi}{\lambda} \times (D - r \cos (\omega t - \phi)) + \theta_ {\mathrm{div}}\right) \bmod 2 \pi \tag {3}
$$

From the equation, we can see that the phase is a periodic function, which has the maximum and minimum values of $4 \pi ( D { + } r ) / \lambda$ and $4 \pi ( D - r ) / \lambda { \mathrm { i f } } r < \lambda / 2$ and $\theta _ { \mathrm { d i v } } = 0$ . However, the curve may be split into several segments in practice due to the mod operation and has a constant shift because of the diversity term.

# 4.2 Calibrating Phase Shifts

Now, we consider the real change of the phase in practice. We attach a tag on edge of a circular disk with a radius of 10cm (please refer to §8 for detailed settings). The tag rotates with an angle speed of 0.4425 radians per second. The centers of disk and reader locate at O(20cm, 0) and R(0, 137.7cm) respectively. Both the tag and reader are on the same plane parallel to the disk surface. We keep the reader’s position unchanged and collect the phase shifts for 400 times. The collected phase values are shown in Fig. 3(a). As expected, the phase is a periodic sequence, which shifts repeat every time the disk completes a rotation. Compared with the ground truth, the sequence, however, goes too far wrong. It is worth noting that here the ground truth is calculated using Eqn. 3 by ignoring the diversity term. Next, we introduce our calibration procedure.

Calibration on Continuity. The curve is not continuous for both measurement results or ground truth due to the mod operation. For being convenient to study the characteristics of spinning tag’s phase shifts, we should firstly smooth the curve by aligning two split sub-sequences. We observe that jumping points must be around 0 or 2π and have very large differences with their adjacent points $( e . g . > \pi )$ ). Simply, we employ a threshold to align the split sequence. Suppose the sequence of phase shifts is $[ \theta ( 1 ) , \theta ( 2 ) , \cdots , \theta ( t ) ]$ ], then

$$
\theta (t) = \left\{ \begin{array}{l l} \theta (t) - 2 \pi & \text { if } \theta (t) - \theta (t - 1) > \pi \\ \theta (t) + 2 \pi & \text { if } \theta (t) - \theta (t - 1) <   - \pi \\ \theta (t) & \text { otherwise } \end{array} \right.
$$

where $t \ > \ 1$ . Fig. 3(b) shows the smoothed phase shifts and ground truth.

Calibration on Diversity. Through comparisons, we have an important observation that the theoretical values of the phase sequence are not consistent with those obtained in the experiments. There is about 2.7 radians misalignment between them. As mentioned in Eqn. 1, the misalignment results from the diversity factor $\theta _ { \mathrm { d i v } }$ [4]. Since the misalignment relatively remains unchanged under the same macro environment (e.g. same temperature, humidity, etc.), it is reasonable to assume $\theta _ { \mathrm { d i v } }$ is a constant term in the obtained phase sequence. In the example, we simply align the two sequences by subtracting 2.7 radians from the ground truth, as shown in Fig. 3(c). Overall, both sequence are matched very well except the values around peaks (which will be addressed later). In practice, it is easy to remove the influence of this constant through a mathematical way. The details are addressed in §5.

Calibration on Orientation. Despite the near-perfect match, there still exist about 0.7 radians gap between the two sequences in the peaks, introducing $0 . 7 / ( 2 \pi ) \times 3 4 / 2 \approx 1$ .9cm distance error $( \lambda = 3 4 c m$ with double distance) for certain sampling points. Specifically, we also observe that the sampling density (defined as the number of phase values collected per second) varies a lot. Roughly, the sampling density should be similar because the reader randomly interrogates the tags over time. Actually, it has higher density around the peaks and valleys (see segment A and C in Fig. 3(c)) but becomes lower in the middle segment (B). Both of these observations reveal that there must exist another factor affecting the phase values.

To explore the reason, we conduct the second experiment in which we attach the tag at the center of the circular disk (i.e. position O) and rotate the disk using the same speed, as illustrated in Fig. 4(a). In theory, since the tag stays at the origin and its distance to the reader remains unchanged, the collected phase values should always be equal. However, the phase exhibits a small fluctuation (∼ 0.7 radians) as rotating, as shown in Fig. 4(b), resulting from the tag orientation. The orientation is defined as the angle between the tag plane where its antenna deploys and the line of OR, denoted as $\rho ( t )$ in the figure. The tag’s antenna is supposed to be symmetrical as a whole. Unfortunately, the practical design always contains an offset. It causes the very small distance difference over orientation, which is badly magnified by the forth-and-back traversals. On the other hand, when $\rho ( t ) = \textstyle { \frac { \pi } { 2 } } + k \pi , ( k = 0 , 1 , \cdot \cdot \cdot )$ , the tag plane is perpendicular to the electric field radiated by the reader, leading to much more radiation and energy received by the tag. Thus, it has higher sampling rate near the peak or valley. On the other hand, lower sampling density in the middle segment (B) also brings additional error to corresponding phase measurement.

![](images/c22f5196549cde228150e6d21c651c0494100f44359199acb309a889a7d14c83.jpg)



(a) Original phase shifts

![](images/7a6711188a4e4a874bb3c018745cceecc2166ac2a9a22ba9dbee093346a28c97.jpg)



(b) Smoothed phase shifts

![](images/bd8d1e5e8776749e6c7bf91ab7cbac1ab2a687bfeca25728b52e3254d6d7a121.jpg)



(c) Calibrating the diversity

![](images/5aab787459e10d91ddc70aa51ced5c41c0e31343b62c95254ce3b6c6e80431dd.jpg)



(d) Calibrating the orientation   
Fig. 3: Calibrating the phase shifts. (a) The original phase shifts. (b) The smoothed phase shifts. (c) The phase shifts after calibrating the device diversity. (d) The phase shifts after calibrating the tag orientation.

To inspect whether tag diversity and spatial location will impose an impact on the relationship between tag orientation and phase value, we further conduct experiments over 20 tags with location coordinates varying among the whole surveillance region. For more details, please refer to §8.3. It turns out that with individual tag and its spatial position varying, various amplitude in the fluctuation curve is observed, but the holistic changing pattern is almost the same, which can be fitted by a Fourier transform function. Formally, we summarize our findings into the following observation.

Observation 4.1. Tag’s phase value has an inherent correlation with its orientation relative to the reader antenna, namely the angle between the tag plane and the line from tag to reader. And this specific correlation can be quantified as a function through data fitting using Fourier series.

# 4.3 Put It Together

As a result, to rectify the impact tag’s orientation imposes on its phase value, we suggest that there should be a calibration procedure before formal process of collecting phase measurements. The entire workflow is generalized as below.

• Step 1: Acquiring phase-orientation function: As a prelude stage, phase measurements versus orientation change are sampled by attaching the tag at the center of the rotating disk. Then the correlation is fitted through Fourier series utilizing the Curve Fitting Toolbox [38] in Matlab, thus a phase-orientation function is formed.   
• Step 2: Calibrating phase values: Attach the tag onto the edge of the rotating disk and collect raw phase measurements with the spinning tag. Calculate the phase offset of every sampled orientation using the results in the above step. Since the orientation actually is a relative variable depending on both the reader and tag, we can simply use the phase measurement at the initial time t = 0 (i.e., tag’s rotation angle ωt equals 0) as reference. Then erase this offset from original phase data. The calibrated phase values will play a part in the next section.

After calibrating the orientation, the phase shifts are more consistent with the ground truth, as shown in Fig. 3(d). This makes the measured data more errorless and plays an active role in improving localization accuracy.

# 5 GENERATING ANGLE SPECTRUM

Our theoretical basis is that the tag’s phase rotation exhibits different value patterns if the reader signal’s angle of arrival changes. Imagine there exists a surveillance plane where the spinning tag and reader lie on whose size is $W \times L$ . For simplicity, we first focus on the case that the reader and tag are on the same plane. The extended 3D scenario is discussed in $\ S 5 . 3$ .

![](images/6db6c045e15741205530cda83e2e6a934896767c8232a609c3306e08de833bf0.jpg)



(a) Experiment setup

![](images/d1a5d9ed303fedfa57646dbc4e67189a639cbfc2c09e0c4f081fc9e869d6b544.jpg)



(b) Phase sequence   
Fig. 4: Influence of tag orientation. Fixing tag at the origin and then collecting the phase sequence. There exists about 0.7 radians shift when changing tag’s orientation.

# 5.1 Traditional AoA Approach

Suppose the target reader takes n signal snapshots of every spinning tag with each snapshot taken at time $t _ { i } .$ . Let $\theta _ { i }$ be the theoretical phase value of the $i ^ { t h }$ snapshot when signal direction is $\phi .$ Then

$$
\theta_ {i} = \frac {4 \pi}{\lambda} \times (D - r \cos (\omega t _ {i} - \phi)) \mod 2 \pi \tag {4}
$$

From basic channel models, we can express the wireless channel parameter $h _ { i }$ measured at the $i ^ { t h }$ snapshot as the complex number [39] in theory:

$$
h _ {i} = \frac {1}{D} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (D - r \cos (\omega t _ {i} - \phi_ {R}))} \tag {5}
$$

where $\phi _ { R }$ is denoted as the reader’s real and unknown direction. One the other hand, we can also obtain the estimated channel parameter $h _ { i }$ using the measured phase value $\tilde { \theta _ { i } }$ :

$$
\tilde {h} _ {i} = \frac {1}{D} e ^ {\mathbf {J} \tilde {\theta} _ {i}} \tag {6}
$$

In a traditional AoA approach, SAR computes the relative signal power along each spatial direction to generate a power profile by correlating $h _ { i }$ and $\tilde { h } _ { i }$ . To do this, it needs two inputs: the measured channel snapshots $\ddot { h } _ { i }$ along the tag trajectory, and the positions $( r , \omega t _ { i } )$ (represented in polar coordinates) of the tag along this trajectory. It then finds the relative power $P ( \phi )$ along direction $\phi$ as

$$
\begin{array}{l} {P (\phi)} = {\frac {1}{n} \left| \sum_ {i = 1} ^ {n} h _ {i} \tilde {h} _ {i} ^ {*} \right| ^ {2} = \frac {1}{n D ^ {2}} \left| \sum_ {i = 1} ^ {n} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (D - r \cos (\omega t _ {i} - \phi))} e ^ {- \mathbf {J} \tilde {\theta} _ {i}} \right| ^ {2}} \\ = \frac {1}{n D ^ {2}} \left| e ^ {\mathbf {J} \frac {4 \pi}{\lambda} D} \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\frac {4 \pi}{\lambda} r \cos (\omega t _ {i} - \phi) + \tilde {\theta} _ {i}\right)} \right| ^ {2} \\ = \frac {1}{n D ^ {2}} \left| \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} \cos (\omega t _ {i} - \phi) + \tilde {\theta} _ {i}\right)} \right| ^ {2} \tag {7} \\ \end{array}
$$

where $| e ^ { \mathbf { J } { \frac { 4 \pi } { \lambda } } D } | = 1$ and $\tilde { h } _ { i } ^ { * }$ denotes the complex conjugate of $\tilde { h } _ { i } .$ . The above relative power profile $P ( \phi )$ is maximum precisely if $\phi = \phi _ { R } ,$ i.e. along the true direction of the reader. This is because the term $h _ { i }$ and $\succnapprox _ { i } *$ are identical in phase, and therefore add up constructively when $\phi = \phi _ { R }$ , while tend to add up destructively

as φ deviates from $\phi _ { R } .$ . Therefore, the relative power profile can be used to accurately ascertain the physical direction of a transmitter, a property crucial for indoor localization. It is worth noting that our goal is to find the real direction $\phi _ { R }$ that makes $P ( \phi )$ maximum by comparing all potential angles. The constant $\scriptstyle { \frac { 1 } { D ^ { 2 } } }$ does not affect the maximum value. Thus, we use the following equation in practice:

$$
P (\phi) = \frac {1}{n} \left| \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} \cos (\omega t _ {i} - \phi) + \tilde {\theta} _ {i}\right)} \right| ^ {2} \tag {8}
$$

By calculating the proposed power formula $P ( \phi )$ for all possible values of $\phi$ on the whole surveillance plane, a power profile for all angles is formed. Further, by searching $\phi$ for the maximum amplitude of $P ( \phi )$ , we can get the target reader’s angle spectrum.

To demonstrate this approach, a typical indoor scenario is simulated as follows: the center of the tag’s circular antenna array is at the origin (coordinates (0, 0)) with 10cm radius, while the target reader locates at (86.6cm, 50cm). Namely, the reader’s direction $\phi _ { R }$ is $3 0 ^ { \circ }$ . Fig. 5(a) plots the results of $P ( \phi )$ . It can be clearly seen that the generated power profile has a peak at the angle direction $( 3 0 ^ { \circ } )$ from tag to reader, which is in conformity with the ground truth.

# 5.2 Enhanced Power Profile

Unfortunately, in a real experimental environment, tag’s phase measurements have more or less deviation from the theoretical ones, adding error to the estimated angle $\phi _ { E }$ . We know that small error of angle will cause big coordinates bias, especially when the reader is quite far from the tag, leading to low localization precision in real scenario. We observe from Fig. 5(a) that there exists a large continuous region around the ground truth with relatively high power values, which means when using $P ( \phi )$ as power formula, the result is not so distinctive and may be susceptible to thermal noise. So we wonder whether the accuracy can be further improved.

As we know, tag’s phase rotation output by the reader is associated with hardware diversity $\theta _ { \mathrm { d i v } }$ . Namely,

$$
\tilde {\theta} _ {i} \approx \theta_ {i} + \theta_ {\mathrm{div}}
$$

Above all, we need to eliminate the misalignment of measured phase resulting from the term $\theta _ { \mathrm { d i v } }$ . Inspired by our previous work [4], We can use the first phase value as a reference as mentioned in §4. Here we explain how this works. Since

![](images/1449eddac5aab6cc161816168d7e8bc30f571e9efc8c7d1b179c62491a0d5512.jpg)



(a) Original power profile

![](images/88ac4be049b907a9d64eac3a88c0eaf50e55bbf21007a92379b0300948784beb.jpg)



(b) Proposed power profile   
Fig. 5: Generated power profiles with one spinning tag. (a) The original power profile with $P ( \phi )$ as power formula. (b) The proposed power profile with modified $R ( \phi )$ as power formula. The spinning tag and target reader are centered at (0, 0) and (86.6cm, 50cm) respectively.

$$
\frac {\tilde {h} _ {i}}{\tilde {h} _ {1}} = \frac {\frac {1}{D} e ^ {\mathbf {J} \tilde {\theta} _ {i}}}{\frac {1}{D} e ^ {\mathbf {J} \tilde {\theta} _ {1}}} = e ^ {\mathbf {J} (\tilde {\theta} _ {i} - \tilde {\theta} _ {1})} \approx e ^ {\mathbf {J} (\theta_ {i} - \theta_ {1})} \tag {9}
$$

There are two key observations here: a) the diversity term $\theta _ { \mathrm { d i v } }$ is eliminated through subtracting the $i ^ { t h }$ measured phase from the first one; and b) the distance variable D is removed by the division operation. So we can obtain a new form of power formula by dividing Eqn. 8 with $( h _ { 1 } \tilde { h } _ { 1 } ^ { * } ) ^ { 2 }$ :

$$
\begin{array}{l} Q (\phi) = \frac {P (\phi)}{(h _ {1} \tilde {h} _ {1} ^ {*}) ^ {2}} = \frac {1}{n} \left| \sum_ {i = 1} ^ {n} \frac {h _ {i}}{h _ {1}} \left(\frac {\tilde {h} _ {i}}{\tilde {h} _ {1}}\right) ^ {*} \right| ^ {2} \\ = \frac {1}{n} \left| \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} (\cos (\omega t _ {i} - \phi) - \cos (\omega t _ {1} - \phi)) + (\tilde {\theta} _ {i} - \tilde {\theta} _ {1})\right)} \right| ^ {2} \\ { = } { \frac { 1 } { n } \left| e ^ { \mathbf { J } \left( \frac { 4 \pi r } { \lambda } \cos ( \omega t _ { 1 } - \phi ) + \tilde { \theta } _ { 1 } \right) } \sum _ { i = 1 } ^ { n } e ^ { - \mathbf { J } \left( \frac { 4 \pi r } { \lambda } \cos ( \omega t _ { i } - \phi ) + \tilde { \theta } _ { i } \right) } \right| ^ { 2 } } \\ \end{array}
$$

Similarly, we extract the constants outside the sum and remove them because they do not affect the final results. Then,

$$
Q (\phi) = \frac {1}{n} \left| \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} \cos (\omega t _ {i} - \phi) + \tilde {\theta} _ {i}\right)} \right| ^ {2} \tag {10}
$$

Surprisingly, we find that $Q ( \phi )$ is exactly the same as $P ( \phi )$ as shown in Eqn. 8. In other words, the diversity actually does not take any impact on the final power profile. It can be understood like this. The diversity poses the same impact on each direction, namely the power along each direction gains same enhancement or weaken due to the diversity. It is equivalent to multiplying a constant to the vector of $P ( \phi )$ , which has no effect on the selection of the maximum element over $P ( \phi )$ .

As is mentioned earlier, in practice, the angles around the ground truth $( \phi _ { R } )$ may also cause comparatively large amplitudes in $Q ( \phi )$ (please refer to the simulation results, as depicted in Fig. 5(a)), especially under the influence of noise. So the results calculated by $Q ( \phi )$ will contain a large number of candidates, which may obscure the ground truth. In order to further reduce error, we propose a new power profile which is an enhanced version of the original one. We know that tag’s real phase measure-

ment results contain random errors, following a typical Gaussian distribution with a standard deviation of 0.1 radians [4]. So we should consider the phase measurement as a Gaussian random variable instead of an accurate value. Our idea is to introduce Gaussian weighing to the power formula. By assigning a virtual amplitude $w _ { i }$ to $Q ( \phi )$ , we get the final power profile $R ( \phi )$ , which is defined as follows.

Definition 5.1. The proposed power profile revealing the power distribution along each direction $\phi \in [ 0 , \overleftarrow { 2 \pi } )$ is given by:

$$
\begin{array}{l} R (\phi) = \frac {1}{n} \left| \sum_ {i = 1} ^ {n} w _ {i} \frac {h _ {i}}{h _ {1}} \left(\frac {\tilde {h} _ {i}}{\tilde {h} _ {1}}\right) ^ {*} \right| ^ {2} \Rightarrow \frac {1}{n} \left| \sum_ {i = 1} ^ {n} w _ {i} h _ {i} \tilde {h} _ {i} ^ {*} \right| ^ {2} \\ = \frac {1}{n} \left| \sum_ {i = 1} ^ {n} w _ {i} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} \cos (\omega t _ {i} - \phi) + \tilde {\theta} _ {i}\right)} \right| ^ {2} \tag {11} \\ \end{array}
$$

where

$$
\left\{ \begin{array}{l} w _ {i} = f (\tilde {\theta} _ {i} - \tilde {\theta} _ {1}; \mu_ {i}, \sqrt {0 . 0 2}) \\ f (x; \mu , \sigma) = \frac {1}{\sigma \sqrt {2 \pi}} e ^ {- \frac {(x - \mu) ^ {2}}{2 \sigma^ {2}}} \\ \mu_ {i} = \frac {4 \pi r}{\lambda} \left(\cos (\omega t _ {1} - \phi_ {R}) - \cos (\omega t _ {i} - \phi_ {R})\right) \end{array} \right.
$$

$f ( x ; \mu , \sigma )$ is the Probability Density Function (PDF) of Gaussian distribution ${ \mathcal { N } } ( \mu , \sigma )$ .

We define the weight as the probability function of the term $( \tilde { \theta } _ { i } - \tilde { \theta } _ { 1 } )$ . Here we consider the measured phase value ${ \tilde { \theta } } _ { i }$ as a random variable whose expectation and standard deviation respectively equal $\theta _ { i }$ and 0.1 radians $( i . e .$ an empirical value). Namely, $\tilde { \theta } _ { i } \sim \mathcal { N } ( \theta _ { i } , 0 . 1 )$ . Although the diversity does not affect the power profile but it does pose impact on the weights, so we must use $( \tilde { \theta } _ { i } - \tilde { \theta } _ { 1 } )$ instead of $\tilde { \theta } _ { i }$ to remove the diversity’s impact. It is well known that the subtraction of two random variables is still a random variable. Here, our question is: what are its expectation and standard deviation? Assume every phase is independently measured, thus $E ( { \tilde { \theta } } _ { i } - { \tilde { \theta } } _ { 1 } ) = E ( { \tilde { \theta } } _ { i } ) - E ( { \tilde { \theta } } _ { 1 } ) = \theta _ { i } - \theta _ { 1 }$ . Let $\mu _ { i }$ denotes the expectation. Then,

$$
\begin{array}{l} \mu_ {i} = \theta_ {i} - \theta_ {1} = \frac {4 \pi}{\lambda} (D - r \cos (\omega t _ {i} - \phi_ {R})) + \theta_ {\mathrm{div}} \bmod 2 \pi \\ - \frac {4 \pi}{\lambda} (D - r \cos (\omega t _ {1} - \phi_ {R})) + \theta_ {\mathrm{div}} \mod 2 \pi \\ = \frac {4 \pi r}{\lambda} \left(\cos (\omega t _ {1} - \phi_ {R}) - \cos (\omega t _ {i} - \phi_ {R})\right) \\ \end{array}
$$

Interestingly, apart from the diversity $\theta _ { \mathrm { d i v } }$ , the difference is also independent on the unknown but constant distance D. On the other hand, $V a r ( \tilde { \theta } _ { i } - \tilde { \theta } _ { 1 } ) = V a r ( \tilde { \theta } _ { i } ) + V a r ( \tilde { \theta } _ { 1 } ) = 2 \times 0 . 0 1 = 0 . 0 2$ . Thus, $( \tilde { \theta } _ { i } - \tilde { \theta } _ { 1 } ) \sim \mathcal { N } ( \mu _ { i } , \sqrt { 0 . 0 2 } )$ .

We attempt to give a qualitative explanation about the definition of the weight. The weight term $w _ { i }$ represents the possibility that the measured phase takes its value when assuming the reader is at direction φ. Keep in mind that the measured $\widetilde { \theta } _ { i }$ comes from the ground truth, associating with $\phi _ { R }$ . If $\phi \ : = \ : \phi _ { R }$ (i.e. guess right), the measured $\widetilde { \theta } _ { i }$ agrees with the calculated expected value $\theta _ { i }$ (i.e. $\tilde { \theta } _ { i } \sim \mathcal { N } ( \theta _ { i } , 0 . 1 ) ;$ ) , and further $w _ { i }$ will get its maximum value because $\theta _ { i } - \theta _ { 1 }$ approaches $\mu _ { i }$ . Otherwise, if φ $\neq \phi _ { R }$ (i.e. guess wrong), the measured ${ \tilde { \theta } } _ { i }$ does not follow $\mathcal { N } ( \theta _ { i } , 0 . 1 )$ , leading to a larger deviation from the real expected value and a smaller weight. Above intuitively accounts for the basic principle behind our proposed method.

Fig. 5(b) presents the results of $R ( \phi )$ . Compared with Fig. 5(a), the peak in Fig. 5(b) is far sharper than that in

Fig. 5(a). This is because by assigning the probability weight $w _ { i }$ to power formula, the power profile is enhanced for angles with higher probability to be the ground truth and weakened for others. Thus many false candidates fade away, protruding the real one. It validates that our proposed method is more effective and accurate than the traditional AoA approach, especially in strong noise environment. This is very meaningful because the precision of AoA has a directly and great impact on the final positioning accuracy of target reader.

# 5.3 Achieving 3D Power Profile

The above analysis is totally based on 2D plane. Now we are going to extend the surveillance region to 3D space with the height of $H .$ For the sake of experiment simplicity, we make the two spinning tags lie on the same plane with height = 0 (also known as the horizontal plane) while the reader may situate at different planes, as illustrated in Fig. 6. In addition to the azimuthal angle φ in the horizontal plane, we also need another parameter, i.e. the polar angle $\gamma$ (represents the angle between $R$ and its projection on the horizontal plane $R ^ { \prime } )$ along the vertical direction to fully describe the reader antenna’s incident signal. Apparently, $\gamma$ has a value falling inside the range of $[ - \pi / 2 , \pi / 2 ]$ . Then the phase formula in Eqn. 4 can be rewritten as

$$
\theta_ {i} = \frac {4 \pi}{\lambda} (D - r \cos (\omega t _ {i} - \phi) \times \cos \gamma) \bmod 2 \pi \tag {12}
$$

where both $\phi$ and $\gamma$ are unknown, which should be guessed. Similar to Eqn. $^ { 8 , }$ the original power profile $P ( \phi , \gamma )$ is defined as follows.

$$
P (\phi , \gamma) = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} \cos (\omega t _ {i} - \phi) \cos \gamma + \tilde {\theta} _ {i}\right)} \right| ^ {2} \tag {13}
$$

Correspondingly, the enhanced 3D power profile is redefined as below.

Definition 5.2. The proposed power profile revealing the power distribution along each azimuthal direction $\phi \in [ 0 , 2 \pi )$ and polar direction $\gamma \in [ - \frac { \pi } { 2 } , \frac { \pi } { 2 } ]$ is given by:

$$
R (\phi , \gamma) = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} w _ {i} e ^ {- \mathbf {J} \left(\frac {4 \pi r}{\lambda} \cos (\omega t _ {i} - \phi) \cos \gamma + \tilde {\theta} _ {i}\right)} \right| ^ {2} \tag {14}
$$

where

$$
\left\{ \begin{array}{l} w _ {i} = f (\tilde {\theta} _ {i} - \tilde {\theta} _ {1}; \mu_ {i}, \sqrt {0 . 0 2}) \\ f (x; \mu , \sigma) = \frac {1}{\sigma \sqrt {2 \pi}} e ^ {- \frac {(x - \mu) ^ {2}}{2 \sigma^ {2}}} \\ \mu_ {i} = \theta_ {i} - \theta_ {1} \\ \qquad = \frac {4 \pi r}{\lambda} (\cos (\omega t _ {1} - \phi) - \cos (\omega t _ {i} - \phi)) \times \cos \gamma \\ \end{array} \right.
$$

$f ( x ; \mu , \sigma )$ is the PDF of Gaussian distribution ${ \mathcal { N } } ( \mu , \sigma )$ and $\mu _ { i }$ is the theoretical phase of the $i ^ { t h }$ snapshot relative to the first one.

By traversing through all potential values of φ and $\gamma$ on the whole surveillance region, a power profile for all spatial angles is formed. Further, by getting φ and $\gamma$ for the maximum amplitude of $R ( \phi , \gamma )$ , the target reader’s spatial angle spectrum is generated. We also run simulation study to examine whether Tagspin is competent to pinpoint the reader antenna with high accuracy and without ambiguity under 3D environment. The similar scenario as that in 2D is simulated: the center of the tag’s circular antenna

![](images/684a2ef4c01e930df1786d68b3c7ad2cc35fbdce5a748d997390e93ce4ec5be2.jpg)



Fig. 6: Generated angle spectrums of reader R with respect to two spinning tags $T _ { 1 } , T _ { 2 }$ in 3D scenario. $R ^ { \prime }$ is $R \mathrm { { ' s } }$ projection on the horizontal plane.

array is at $( 2 0 c m , 0 , 0 )$ with 10cm radius, while the target reader locates at $( - 6 6 . 6 c m , 0 , 5 0 c m )$ . Namely, the reader’s azimuthal angle $\phi _ { R }$ is $1 8 0 ^ { \circ }$ and polar angle $\gamma _ { R }$ is $3 0 ^ { \circ }$ . Fig. 7 depicts the original and improved power profiles respectively in both 3D mesh and 2D image. It’s obvious that the improved power formula $R ( \phi , \gamma )$ still performs far better than the original one. Besides, the ground truth corresponds to just one of the two sharp peaks, which indicates that even in 3D case, Tagspin works as well as that in 2D condition, except that it will output two candidate location estimates with symmetric polar angles. We’ll elaborate on the reason later.

# 6 LOCATING TARGET READER

With the target reader’s angle spectrum generated from the previous section, we can mathematically give the reader’s location by intersecting different angle spectrums.

Locating reader at 2D plane. In theory, given two orientations we could get a intersection point, which is exactly the reader’s location in 2D plane. Specifically, as Fig. 1 depicts, the two spinning tags’ centers are marked as $O _ { 1 }$ and $O _ { 2 }$ , locating at $( x _ { 1 } , y _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } )$ . Their angle spectrums generated in the previous section emit at directions $\phi _ { 1 }$ and $\phi _ { 2 }$ respectively. We establish the reference Cartesian coordinate system with the line determined by $O _ { 1 }$ and $O _ { 2 }$ as the x-axis. Then the target reader $R \mathrm { { ' s } }$ coordinates $( x _ { R } , y _ { R } )$ can be calculated as follows.

$$
\left\{ \begin{array}{l} x _ {R} = \frac {y _ {2} - y _ {1} + x _ {1} \tan \phi_ {1} - x _ {2} \tan \phi_ {2}}{\tan \phi_ {1} - \tan \phi_ {2}} \\ y _ {R} = \frac {\left(x _ {1} - x _ {2}\right) \tan \phi_ {1} \tan \phi_ {2} + y _ {2} \tan \phi_ {1} - y _ {1} \tan \phi_ {2}}{\tan \phi_ {1} - \tan \phi_ {2}} \end{array} \right. \tag {15}
$$

Locating reader at 3D space. Combining the angle spectrums of two spinning tags in 3D space, we can infer the reader’s spatial position $( x _ { R } , y _ { R } , z _ { R } )$ in the end. Denote $O _ { 1 }$ and $O _ { 2 } { \ ' } { \mathfrak { s } }$ s coordinates as $( x _ { 1 } , y _ { 1 } , z _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } , z _ { 2 } )$ , referring to Fig. 6. In our case, $z _ { 1 } = z _ { 2 } = 0$ . Then $x _ { R } , y _ { R }$ can be similarly given by Eqn. 15. And

$$
z _ {R} = \left\{ \begin{array}{l l} \sqrt {(x _ {1} - x _ {R}) ^ {2} + (y _ {1} - y _ {R}) ^ {2}} \times \tan \gamma_ {1} & (1 6 a) \\ \sqrt {(x _ {2} - x _ {R}) ^ {2} + (y _ {2} - y _ {R}) ^ {2}} \times \tan \gamma_ {2} & (1 6 b) \end{array} \right.
$$

Actually, the final estimate of $z _ { R }$ is often obtained by comparing and balancing the results of Eqn. 16a and Eqn. 16b.

It’s apparent that two spatial points whose z-coordinates are opposite (i.e. polar angles are apposite) will generate the same distance from any point located on the horizontal plane. So it’s easy to understand why Tagspin will give two symmetric location candidates (see Fig. 7). In practical applications, there always exists dead space, causing some spatial locations impossible or meaningless. For example, if the horizontal plane (x-y plane) we choose is close to the ground, the candidate location with negative z-coordinate can be eliminated because the antenna can not be located beneath the ground level in practice. So it’s reasonable that we can subtract such dead space from our surveillance region beforehand or exclude the invalid candidates afterwards to eliminate ambiguity in real scenarios. If we want to further enhance accuracy, the third spinning tag, which rotates along the vertical direction to provide more aperture diversity in z-axis, can be introduced. This forms a part of our future work.

![](images/1cb7537c70498a804cdfd7d5aca752d72ea273ab18e0d6c0e035ea8a09348288.jpg)



(a) 3D mesh with Q(φ, γ)

![](images/29da92624e6234308c4d5efa5e82a6a86ab260cd46889d763ff557602833459f.jpg)



(b) 2D image with Q(φ, γ)

![](images/6d63ea37051dca14115b878f4b5f813123df8c83ec1fb26cbdcfbfd2a4717fd2.jpg)



(c) 3D mesh with R(φ, γ)

![](images/f19a9d87da1c4a89a6cc745b9de7fa6ccd63427734adf1e1500ba7f8bf0a82b0.jpg)



(d) 2D image with R(φ, γ)   
Fig. 7: Simulation results in 3D scenario. (a)-(b) The original power profile with $Q ( \phi , \gamma )$ as power formula. (c)-(d) The improved power profile with $R ( \phi , \gamma )$ as power formula.

Dealing with errors. Varying measurement errors in practice may shift these angle spectrums away from the target. Thus, we can increase the number of spinning tags to reduce the errors. For example, three spinning tags bring three orientation lines to intersect at three different points rather than the same point. Given multiple intersection points, a target can be located by several different algorithms. In this paper, we propose to use the Weighted Centroid Localization method like [40] does. We assign weight to each intersection point according to an internally computed confidence value. The confidence value is proportional to the acuteness of the intersection angle between two intersecting orientation lines because the acuteness angle affects the sensitivity of angular error on positional error.

Discussion on multi-path effect. Obstacles in practical scenarios may make the signal propagate along non-line-of sight (NLOS) or introduce multi-path effect, which is a main challenge we deal with in this work. That is also the reason why we utilize several spinning tags for the localization instead of stationary tags. A moving tag would provide phase measurements from various directions/perspectives, making the NLOS propagations vary a lot. However, whatever angle the tag is located at, the LOS propagations are always consistent with the ground truth. Namely, unexpected and unordered wave propagations through NLOS will cancel out each other, while LOS propagations can reinforce their amplitudes. We utilize this characteristic to enhance the location accuracy and degrade the influence from NLOS propagations. So as long as there exists a LOS path, Tagspin can work well and limit the negative impact from multi-path effect.

# 7 IMPLEMENTATION

We build a prototype of Tagspin using the COTS RFID reader, antennas and tags.

Hardware: Reader: We adopt an Impinj Speedway Revolution R420 reader [41] which is compatible with EPC Gen2 standard and supports four directional antennas at most. The whole RFID system operates during the frequency of 920.5M Hz ∼ 924.5M Hz band by default, which is the legal UHF band in China. Correspondingly, the wavelength ranges from 32.43cm to 32.57cm. The size of reader antenna is 22.5cm×22.5cm×4cm. Total four different antennas with circular polarization manufactured by Yeon technology [42] are used. The reader is connected to our host end through Ethernet. Tag: Altogether five types of tags from Alien Corp [43], namely Alien “Squig” (AZ-9610), “Square” (AZ-9629), “Squiglette” (AZ-9630), “2 × 2” (AZ-9634) and “Short” (AZ-9662) are employed (listed in Table 1). Many of the tags are widely used in today’s industrial area, such as supply chain applications. All of them are low-cost (only about 5 cents per tag on average).

Software: We use a Samsung PC to run our algorithms, as well as connecting to the reader through Ethernet under LLRP (Low Level Reader Protocol) [44]. The machine equips Intel Core i7 CPU at 2.4GHz and 4G memory. Impinj reader extends the LLRP protocol to support the phase report. We adjust the configuration of reader to immediately report its readings whenever tag is detected. The client code is implemented using Java language. Besides, both the reader and host have their own local clock and attach a timestamp for each tag read. In order to erase the influence of network latency, we adopt the timestamp provided by reader rather than host machine for phase value acquisition.

# 8 EVALUATION

In this section, we evaluate Tagspin mainly in terms of localization accuracy and overhead. To fully get insights into various factors that may affect Tagspin’s performance, we implement a lightweight testbed, as shown in Fig. 8.

<table><tr><td>#</td><td>Model</td><td>Company</td><td>Chip</td><td>Size ( $mm^{2}$ )</td><td>QTY</td></tr><tr><td>1</td><td>AZ-9610</td><td>Alien</td><td>H3</td><td> $44.5 \times 10.4$ </td><td>4</td></tr><tr><td>2</td><td>AZ-9629</td><td>Alien</td><td>H3</td><td> $22.5 \times 22.5$ </td><td>4</td></tr><tr><td>3</td><td>AZ-9630</td><td>Alien</td><td>H3</td><td> $70 \times 9.5$ </td><td>4</td></tr><tr><td>4</td><td>AZ-9634</td><td>Alien</td><td>H3</td><td> $44 \times 46$ </td><td>4</td></tr><tr><td>5</td><td>AZ-9662</td><td>Alien</td><td>H3</td><td> $70 \times 17$ </td><td>4</td></tr></table>

TABLE 1: The tag models

![](images/de0302b2bd1a20f98c7c29ed37d22662afd8b8b198597e62697ae67ed2adaf85.jpg)



Fig. 8: Experiment setup. We evaluate Tagspin in both 2D and 3D scenarios.

# 8.1 Methodology

Manifold experiments are designed towards measuring the performance of Tagspin. Our experiments are conducted in an office room whose size is $4 0 0 \times 9 0 0 c m ^ { 2 }$ .

Baseline: We compare Tagspin with other four localization methods, including LandMarc [5], AntLoc [25], PinIt [1] and BackPos [24]. LandMarc is an RSS-based schema which achieves combined error distance of 100cm on average. AntLoc is one of the few systems that focus on the problem of antenna localization. Its mean error is around 15cm with mobile and rotatable antenna as a prerequisite. The mean error distance of PinIt is 12cm with 6cm standard deviation requiring reference tags pre-deployed. BackPos is a phase-based method with mean error of 17cm and standard deviation of 5cm.

Metric: We adopt the error distance, defined as the Euclidean distance between the result and ground truth, as our basis metric. All ground truth is measured by a laser rangefinder with a supposed error of ±0.1mm. For each same setting, we repeat the experiments over 50 times.

# 8.2 Localization Accuracy

We investigate the localization accuracy in terms of 2D and 3D space respectively. The reader antenna’s distance range in our experimentation varies from tens of centimeters to several meters (about six meters upper bound in our indoor environment).

# 8.2.1 2D Plane

We first inspect Tagspin’s performance in 2D plane. As illustrated in Fig. 8, the rotating disks each with a tag adhere to are placed on a flat desk, while the antenna is located away from the tag. We establish the Cartesian coordinate system with regard to the desktop, which means we treat the desktop plane as the horizontal plane. We make the reader stay on the same plane with the rotating tag under the support of a laser level. The locations of the two spinning tags’ centers are chosen to be (−20cm, 0) and (20cm, 0) sequentially.

Furthermore, we change the reader’s location randomly across the surveillance plane and perform the localization procedure for 100 times. Fig. 9 plots the CDF of positioning error. The mean error distance of Tagspin under 2D scenario is 3.1cm in x-axis, 4.1cm in y-axis and 5.3cm in combined dimension with standard deviation of 1.6cm, outperforming LandMarc, AntLoc, PinIt and BackPos by 18.9×, 2.8×, 2.3× and 3.2× respectively. Besides, 90% of the errors are less than 7.5cm with minimal error of 1.7cm and maximal error of 9.5cm.

# 8.2.2 3D Space

After validating Tagspin’s performance in 2D plane, we wonder whether it can still work well when applied to 3D space. As is similar to the case in 2D scenario, we still regard the desktop plane as the horizontal plane, while the reader may lie on different planes from the tags. This time, the center locations of the two spinning tags are chosen to be (−20cm, 0, 9.5cm) and (20cm, 0, 9.5cm) with z-coordinates being added.

We enrich our experiment by randomly changing the reader antenna’s location over the surveillance region and conduct the localization process for 100 times. The CDF of positioning error is plotted in Fig. 10. The mean error distance of Tagspin in 3D space is 3.4cm in x-axis, 4.0cm in y-axis, 4.7cm in z-axis and 7.3cm in combined dimension with standard deviation of 1.8cm. It’s worth noting that none of the baseline systems are validated under 3D scenario. Even so, Tagspin outperforms the two-dimensional LandMarc, AntLoc, PinIt and BackPos by 13.7×, 2.1×, 1.6× and 2.3× respectively. Moreover, 90% of the errors are less than 9.4cm with minimal error of 2.9cm and maximum error of 11.2cm. It’s worth noting that among the three dimensions, the error on the z-axis is larger than the other two. This is because we make both spinning tags rotate along the x-y plane, which means more aperture diversity is introduced on x-axis and y-axis instead of z-axis.

Generally speaking, compared to the antenna size which is always quite a few decimeters, our centimeter-level accuracy is quite acceptable. And this calibration error may affect the subsequent tag localization at a degree of a few centimeters, depending on the specific localization approach adopted.

# 8.2.3 Accuracy Comparison among Different Positions

In this subsection, we try to figure out whether different reader positions will make a difference in localization accuracy. Totally, we deploy the reader antenna on 10 different locations uniformly scattered among the field as shown in Fig. 11. The ground truth is marked as $\cdot _ { + } ,$ ’. The two center locations of spinning tags are noted as $\mathbf { \epsilon } \cdot \mathbf { \alpha } \times \mathbf { \gamma }$ . Data points with the same color represent location estimates for the same reader position. For ease of presentation, we consider the accuracy in 2D plane. We have the following observations from this figure. (a) When the antenna has a relative close distance (i.e., less than 3m), the position closer to the spinning tags has a bigger error compared with the farther one. For example, the mean error of $L _ { 1 }$ is 7.6cm while that of $L _ { 3 }$ is 3.1cm. The reason is that when the reader is too close to the centers of spinning tags, the precondition of our method that D  r we make in §4 is not satisfied. So the theoretical phase value we calculate through Eqn. 12 may contain considerably big error, resulting in the large deviation of final location estimate. (b) On the other hand, when the antenna distance is too far (i.e., 5m), the error will also increase, from 3.1cm of $L _ { 3 }$ to 8.2cm of $L _ { 7 } .$ This can be explained as follows. As the distance increases, the multi-path effect may become more complicated than that in the near field, which would introduce more NLOS propagations and degrade the accuracy accordingly.

# 8.3 Impact of Tag Orientation

As we mentioned in §4, even if location remains unchanged, tag’s orientation does have an effect on its phase value in practice. This can be intuitively explained by the angular sensitivity of the tags inlay. We conduct numerous experiments to give a comprehensive analysis on the orientation’s effect over different tags and locations. Table 1 lists detailed information of the tags we adopt. Each time we make the tag’s geometric center stays at the same location, while change its orientation towards reader antenna from $0 ^ { \circ }$ to $3 6 0 ^ { \circ }$ . Fig. 12 shows how tag’s phase measurements change along with its orientations. As to the same location, we make the phase measurement collected at the initial time t = 0 (i.e., tag’s rotation angle ωt equals 0) as the reference phase value of that location. All records in Fig. 12 are relative values compared to the reference one. The result is computed as an average over all the different tags and locations. It’s obvious to see that tag orientation does play a non-ignorable role in tag’s phase measurements and there exhibits stable regularity between orientation angle and corresponding phase value. Note that we also test an omni-directional tag, namely Impinj Monza 4-based H47 [45], which shows similar results.

![](images/8a7ebf6d8f276cbe1765a1f597793b207a92d0d93ae090d2fba286bea519717f.jpg)



Fig. 9: Localization error in 2D

![](images/ce9fecc46036368f6d7ffdc8fb1a8c038166fb502341e24c0c23d9a2d81d102b.jpg)



Fig. 10: Localization error in 3D

![](images/d650c29a23a29f3810b608ed1b4f09bd9c9b2822213a7b894871911edef84920.jpg)



Fig. 11: Errors vs. positions

Significance of accounting for tag orientation’s impact: As stated before, a calibration step is undergone to eliminate tag orientation’s influence mathematically. We want to validate the effectiveness of our calibration method through experimentation. After collecting original phase measurements, we first deal with them normally with the calibration step and then omit the procedure to make a controlled study. The comparison results of the controlled experiments are plotted in Fig. 13 by CDFs. The mean error distance of Tagspin with calibration procedure is 7.3cm under 3D scenario, while without calibration the error is increased to 27.1cm. So our idea and method of accounting for tag orientation’s impact is significant and can improve localization accuracy by 3.7×, which is an appreciable amount in indoor environment.

# 8.4 Tuning Parameters

After evaluating Tagspin’s accuracy from a global perspective, in this subsection, we’ll discuss different parameter values, system settings and device diversity’s impact on Tagspin’s performance. Note that, all our experiments in this subsection are carried out under 3D scenario.

# 8.4.1 Center Location of Spinning Tag

As we mentioned before, the x-y coordinates of the spinning tags’ two centers are fixed to (−20cm, 0) and (20cm, 0) respectively, which means the distance between the two centers maintains a constant value as 40cm. It’s worth investigating whether their distance will exert an effect on the final localization accuracy. So we change the rotating disks’ locations and conduct sufficient experiments right along. Fig. 14 depicts the localization error of different distance between center locations. We make the distance as a variable whose value falls within the range from 20cm to 80cm at every 5cm interval. It can be seen from the figure that the localization error is almost stable with small vibration when the two centers’ distance $\geq 3 0 c m$ . For the sake of convenience, we select the distance’s default value as 40cm in the rest of our experiments in order to achieve relatively high accuracy as well as improve space efficiency. However, when the distance is less than $3 0 c m ,$ especially when its smallest value (20cm) is achieved, the localization accuracy is impaired to a certain degree, which is explicable because if two centers’ distance is too short, some sampling points of different disks will get very close, bringing more uncertainty to the phase measurements, thus localization error is increased. Note that, here the radius of disk is 10cm, so the smallest value of two centers’ distance is 20cm as shown in Fig. 14.

# 8.4.2 Radius of Spinning Tag

In addition to the centers’ distance, the radius of spinning tag is another parameter that may have an influence on Tagspin’s accuracy. In our previous experiments, the radius is set to 10cm. Here, we ranging the radius from 2cm to 24cm with a step length of 2cm in order to study whether it will make a difference in positioning accuracy. The result is revealed in Fig. 15. We can see from the figure that when the radius value falls within the interval of [8cm, 16cm], the positioning accuracy remains high and stable. But when the radius < 8cm or > 16cm, the positioning error increases by quite an amount. The reason why localization accuracy drops is that the phase measurements along circular track become hard to distinguish when the radius is too small and the assumption $D \gg r$ we make in §4 is untenable when the radius r is too large. So it’s suggested that the value of radius should be chosen from the interval of [8cm, 16cm] and we make 10cm as its default value in our experiments.

# 8.4.3 Tag’s Spinning Speed

Actually, the tag’s spinning speed does have an influence on the localization accuracy when it rotates too fast [46]. Backscatter systems will suffer from serious packet loss when the tag moves with a high speed [47], even making the tag hard to be interrogated. That’s why we make the disk rotate slowly with a stable speed in our work. When the spinning speed remains in a relatively small range, we conducted an empirical study to inspect the corresponding accuracy as depicted in Fig. 16. We can see that the accuracy remains high when the tag’s spinning speed is below 1.1 radians per second, but if the tag rotates at a more high speed (e.g. above 2.0 rad/s), the result becomes more erroneous.

![](images/3b2a34cf4001b16ba645b9ef88f9464ccac7df1b0ed68022f56e1bd01b5e4398.jpg)



Fig. 12: Impact of orientation

![](images/c0acb2ead63d514548d1b5be21a9b273ac429edc07cfc0c7d838fb9e0c8a6d3d.jpg)



Fig. 13: Significance of calibration

![](images/84853b7c914e4ee0daffda7cb6c78de36b8ffe68e15579ee836ad81f48b0fc6c.jpg)



Fig. 14: Impact of centers’ distance

![](images/9d4dac0bdc1104ebbad2ac82020d41f9db3f332248ac8b1ec1f358dfe95e03d8.jpg)



Fig. 15: Impact of radius

![](images/f7dd0703654ff59afdd52cd7f6328367dd5b97ae68a90f9aabdd503c07fefe7c.jpg)



Fig. 16: Impact of spinning speed

![](images/59145acf47bb557c27138c807efac672e29aab30fc868ddc89c374998cae1ca4.jpg)



Fig. 17: Impact of tag diversity

So we choose the moderate speed 0.44 rad/s as default in our experiments.

# 8.4.4 Tag Diversity

One big advantage of our system is its simplicity, which means it only takes very simple manipulation to reach localization purpose without sacrificing precision. One of the things is that we employ only two tags from beginning to end. So tag diversity is another factor that may bring fluctuation in positioning error. Totally, we experiment on five models of tags, as illustrated in Table 1, all of which have different antenna sizes and shapes. As our proposed method has already taken device diversity into consideration, it’s expected that different tags will have little impact on accuracy. We repeat localization experiments over 20 different tags coming from the aforementioned 5 types with 4 tags each model. Fig. 17 plots the relationship between positioning accuracy and tag diversity. For each tag model, the localization error is calculated as an average over all the tags of that model. Our findings are as follows: a) although tag type varies, the positioning accuracy almost remains constant with maximum value only differs 0.5cm from minimum one; b) for tags of the same model, different individual basically demonstrates the same accuracy. The results are consistent with our expectation. And the tag type we adopt in most of our experiments is “2 × 2” (AZ-9634) because of its proper form factor, high signal strength and stability.

# 8.4.5 Antenna Diversity

Apart from the diversity caused by tags, different reader antenna is another form of device diversity that may cause uncertainty in localization accuracy. We totally experiment on four antennas from Yeon technology. The CDFs of errors are plotted in Fig. 18. We observe that there is only slight difference among the positioning errors, which is in accordance with our expectation because antenna diversity is just one type of device diversity we’ve already allowed for in our method. The mean error distances of the four antennas are 7.3cm, 7.4cm, 7.5cm and 7.3cm respectively. And the corresponding standard deviations are 1.8cm, 1.8cm, 2.0cm and 1.6cm. Specifically, in most of our experiments, we use Antenna 1 as default.

# 8.5 System Overhead

When we consider Tagspin’s performance, especially compared to traditional manual calibration of antennas, the system overhead including time and energy cost is also an important metric as the localization accuracy. Traditional manual work usually adopts tape measures and/or laser rangefinders to measure the reader’s location, which can be laborious and inaccurate especially in 3D scenario or when the reader is located at a distant place. We carry on the whole localization procedure using both our method and manual calibration to make a comparison of the time cost. The results in Fig. 19 are averaged over 50 experiments. It only take Tagspin 1.7min on average (almost all within 2min) to finish the whole localization procedure, including data sampling and algorithm running. The time cost is much lower than that of manual calibration, which often takes more than 5min with 5.6min on average. In fact, our reader can support four antennas at one time, and to avoid the interference, the reader manufacture adopts a time-sharing strategy to schedule each antenna. It is obvious that if multiple antennas are used, the number of readings for a pair of antenna and tag per second would decrease due to the time-sharing. It means we obtain fewer tag samples, thereby we need a little bit more time to collect enough samplings or readings for our algorithm. Oppositely, the overhead would quadruple when manual calibration is adopted in four-antenna scenario.

So in conclusion, speaking of either localization accuracy or system overhead, Tagspin has it all over the traditional manual calibration method.

![](images/9ec7737b497e5d86a9f1a096fc122979b273572a125e6aaad1e17699b49e6486.jpg)



Fig. 18: Impact of antenna diversity

![](images/23ba3b668fc3a43b3edce2d5eabaac89c12cbf8c892f47776274de09d67b7d99.jpg)



Fig. 19: Time cost

# 9 CONCLUSION AND FUTURE WORK

In this work we present a phase-based RFID reader localization system Tagspin, which can locate the reader antenna in 3D space with only a few spinning tags. Tagspin fills in the gap of RFID reader localization area and achieves fairly good accuracy. Our key innovations are studies on phase patterns observed by spinning tag and as far as we know, our method is the first to quantify tag orientation’s effect on the phase measurements. We implement Tagspin using COTS RFID products and experimental results show that it achieves mean accuracy of 7.3cm with standard deviation of 1.8cm in 3D space. We believe that with the reader being precisely located, our system will open up a whole new class of applications in RFID domain.

For future work, we believe our accuracy still has room to improve. One possible way is to add more spinning tags and balance their results. Besides, it becomes possible to speculate tag’s orientation from measured phase data, which can lead to many new perspectives of scientific problems.

# ACKNOWLEDGMENTS

This research is partially supported by the NSF China General Program under Grant No. 61572282 and China Postdoctoral Science Foundation under Grant No. 2015M570100.

# REFERENCES

[1] J. Wang and D. Katabi, “Dude, where’s my card?: RFID positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[2] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “RF-compass: Robot object manipulation using RFIDs,” in Proc. of ACM MobiCom, 2013.   
[3] J. Wang, D. Vasisht, and D. Katabi, “RF-IDraw: Virtual touch screen in the air using RF signals,” in Proc. of ACM SIGCOMM, 2014.   
[4] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: Real-time tracking of mobile RFID tags to high precision using COTS devices,” in Proc. of ACM MobiCom, 2014.   
[5] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “LANDMARC: Indoor location sensing using active RFID,” Wireless Networks, vol. 10, no. 6, pp. 701–710, 2004.   
[6] S. J. Orfanidis, Electromagnetic waves and antennas. Rutgers University New Brunswick, NJ, 2002.   
[7] C. Wang, H. Wu, and N. F. Tzeng, “RFID-based 3-D positioning schemes,” in Proc. of IEEE INFOCOM, 2007.   
[8] M. Bouet and A. L. dos Santos, “RFID tags: Positioning principles and localization techniques,” in Proc. of IFIP Wireless Days, 2008.   
[9] C. Duan, L. Yang, and Y. Liu, “Accurate spatial calibration of rfid antennas via spinning tags,” in Proc. of IEEE ICDCS, 2016.   
[10] C. Duan, X. Rao, L. Yang, and Y. Liu, “Fusing rfid and computer vision for fine-grained object tracking,” in Proc. of IEEE INFOCOM, 2017.

[11] J. D. Griffin and G. D. Durgin, “Complete link budgets for backscatterradio and RFID systems,” IEEE Antennas and Propagation Magazine, vol. 51, no. 2, pp. 11–25, 2009.   
[12] G. Li, D. Arnitz, R. Ebelt, U. Muehlmann, K. Witrisal, and M. Vossiek, “Bandwidth dependence of CW ranging to UHF RFID tags in severe multipath environments,” in Proc. of IEEE RFID, 2011.   
[13] L. Shangguan, Z. Li, Z. Yang, M. Li, and Y. Liu, “Otrack: Order tracking for luggage in mobile RFID systems,” in Proc. of IEEE INFOCOM, 2013.   
[14] Y. Zhao, Y. Liu, and L. M. Ni, “VIRE: Active RFID-based localization using virtual reference elimination,” in Proc. of IEEE ICPP, 2007.   
[15] A. Bekkali, H. Sanson, and M. Matsumoto, “RFID indoor positioning based on probabilistic RFID map and kalman filtering,” in Proc. of IEEE WiMOB, 2007.   
[16] K. K. Chintalapudi, A. P. Iyer, and V. Padmanabhan, “Indoor localization without the pain,” in Proc. of ACM MobiCom, 2010.   
[17] A. Rai, K. K. Chintalapudi, V. Padmanabhan, and R. Sen, “Zee: Zeroeffort crowdsourcing for indoor localization,” in Proc. of ACM MobiCom, 2012.   
[18] Y. Zhang, M. G. Amin, and S. Kaushik, “Localization and tracking of passive RFID tags based on direction estimation,” International Journal of Antennas and Propagation, vol. 2007, 2007.   
[19] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar, “Accurate localization of RFID tags using phase difference,” in Proc. of IEEE RFID, 2010.   
[20] P. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. Rao, “Phase based spatial identification of UHF RFID tags,” in Proc. of IEEE RFID, 2010.   
[21] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, “New measurement results for the localization of UHF RFID transponders using an angle of arrival (AoA) approach,” in Proc. of IEEE RFID, 2011.   
[22] J. Xiong and K. Jamieson, “ArrayTrack: A fine-grained indoor location system,” in Proc. of USENIX NSDI, 2013.   
[23] K. R. Joshi, S. S. Hong, and S. Katti, “PinPoint: Localizing interfering radios,” in Proc. of USENIX NSDI, 2013.   
[24] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu, “Anchor-free backscatter positioning for RFID tags with high accuracy,” in Proc. of IEEE INFO-COM, 2014.   
[25] R. C. Luo, C.-T. Chuang, and S.-S. Huang, “RFID-based indoor antenna localization system using passive tag and variable RF-attenuation,” in Proc. of IEEE IECON, 2007.   
[26] R. Miesen, F. Kirsch, and M. Vossiek, “Holographic localization of passive UHF RFID transponders,” in Proc. of IEEE RFID, 2011.   
[27] A. Parr, R. Miesen, and M. Vossiek, “Inverse SAR approach for localization of moving RFID tags,” in Proc. of IEEE RFID, 2013.   
[28] A. Povalac and J. Sebesta, “Phase difference of arrival distance estimation for RFID tags in frequency domain,” in Proc. of IEEE RFID-Technologies and Applications, 2011.   
[29] M. Scherhaufl, M. Pichler, and A. Stelzer, “Localization of passive UHF RFID tags based on inverse synthetic apertures,” in Proc. of IEEE RFID, 2014.   
[30] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proc. of ACM MobiCom, 2014.   
[31] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Relative Localization of RFID Tags using Spatial-Temporal Phase Profiling,” in Proc. of USENIX NSDI, 2015.   
[32] L. Yang, Y. Qi, J. Fang, X. Ding, T. Liu, and M. Li, “Frogeye: Perception of the slightest tag motion,” in Proc. of IEEE INFOCOM, 2014.

[33] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: Shelving interference and joint identification in large-scale RFID systems,” in Proc. of IEEE INFOCOM, 2011.   
[34] X. Liu, K. Li, G. Min, Y. Shen, A. X. Liu, and W. Qu, “Completely pinpointing the missing RFID tags in a time-efficient way,” IEEE Trans. Computers, vol. 64, no. 1, pp. 87–96, 2015.   
[35] X. Liu, K. Li, G. Min, K. Lin, B. Xiao, Y. Shen, and W. Qu, “Efficient unknown tag identification protocols in large-scale RFID systems,” IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 12, pp. 3145–3155, 2014.   
[36] X. Liu, K. Li, G. Min, Y. Shen, A. X. Liu, and W. Qu, “A multiple hashing approach to complete identification of missing RFID tags,” IEEE Trans. Communications, vol. 62, no. 3, pp. 1046–1057, 2014.   
[37] ImpinJ, “Speedway revolution reader application note: Low level user data support,” in Speedway Revolution Reader Application Note, 2010.   
[38] “Curve fitting toolbox,” https://www.mathworks.com/products/ curvefitting.html.   
[39] D. Tse and P. Viswanath, Fundamentals of Wireless Communication. Cambridge University Press, 2005.   
[40] H.-l. Chang, J.-b. Tian, T.-T. Lai, H.-H. Chu, and P. Huang, “Spinning beacons for precise indoor localization,” in Proc. of ACM SenSys, 2008.   
[41] “Impinj, Inc,” http://www.impinj.com/.   
[42] “Yeon Antenna,” http://www.yeon.com.tw/content/product.php?act= detail&c id=43.   
[43] “Alien,” http://www.alientechnology.com/tags/square.   
[44] EPCglobal, “Low level reader protocol (LLRP),” 2010.   
[45] “Impinj monza 4,” https://support.impinj.com/hc/en-us/articles/ 115000426164-Monza-4-True3D-Antenna-Technology.   
[46] L. Yang, Y. Li, Q. Lin, X.-Y. Li, and Y. Liu, “Making sense of mechanical vibration period with sub-millisecond accuracy using backscatter signals,” in Proc. of ACM MobiCom, 2016.   
[47] P. Zhang, J. Gummeson, and D. Ganesan, “Blink: A high throughput link layer for backscatter communication,” in Proc. of ACM MobiSys, 2012.

![](images/3b9a36808854f8117315c706ccc573b2ac565163ca6304ae96dc17fb90e08fa7.jpg)



Chunhui Duan received the BS degree from the School of Software at Tsinghua University, China, in 2013. She is now a fourth year PhD student of School of Software at Tsinghua University, China. Her research interests include RFID, wireless network, mobile sensing and pervasive computing. She is a student member of the IEEE.

![](images/c0be2fb0d3687eb2064ef358821b459f319cea4d0b840cbfac21ce7035853d8d.jpg)



Lei Yang received the BS and PhD degree from the School of Software and the Department of Computer Science and Engineering at Xi’an Jiaotong University. Previously, he was a postdoc fellow at the School of Software of Tsinghua University. He is currently working as a Research Assistant Professor with the Department of Computing, The Hong Kong Polytechnic University. He is the winners of Best Paper Awards of MobiCom’14 and MobiHoc’14, the Runner-up of Best Video Award of MobiCom’16.   
He is also the recipient of ACM China Doctoral Dissertation Award. His research interests include RFID and backscatters, wireless and mobile computing, pervasive computing and smart home.

![](images/73a3d86fc197040491cb8c920396d7f72839e2f1abe97071da336902d3a79e81.jpg)



Qiongzheng Lin received the BS degree from the School of Software at Tsinghua University, China, in 2012. He is now a PhD student of School of Software at Tsinghua University, China. His research interests include radio frequency identification (RFID) and sensor network, mobile sensing and pervasive computing. He is a student member of the IEEE and ACM.

![](images/079107d486f644c71201d8f9383d4e398a8ee63f7e3b752d89b0616607af9e57.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, USA, in 2003 and 2004, respectively. He is now Chang Jiang Chair Professor and Dean of School of Software at Tsinghua University, China. He is an ACM Distinguished Speaker and now serves as the Chair of ACM China Council and also the Associate Editor for IEEE/ACM Transactions on Networking and ACM Transac-  
tions on Sensor Network. His research interests include RFID and sensor network, the Internet and cloud computing, and distributed computing. Yunhao is a Fellow of the IEEE and ACM.