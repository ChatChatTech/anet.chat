# Accurate Spatial Calibration of RFID Antennas via Spinning Tags

Chunhui Duan∗, Lei Yang∗† and Yunhao Liu∗

∗School of Software, Tsinghua University, Beijing, China

†Department of Computing, The Hong Kong Polytechnic University, Hong Kong, China

Email: hui@tagsys.org, young@tagsys.org, yunhao@greenorbs.com

Abstract—Recent years have witnessed the advance of RFIDbased localization techniques that demonstrate high precision. Many efforts have been made locating RFID tags with a mandatory assumption that the RFID reader’s position is known in advance. Unfortunately, calibrating reader’s location manually is always time-consuming and laborious in practice. In this paper, we present Tagspin, an approach using COTS tags to pinpoint the reader (antenna) quickly and easily with high accuracy. Tagspin enables each tag to emulate a circular antenna array by uniformly spinning on the edge of a rotating disk. We design an SARbased method for estimating the angle spectrum of the target reader. Compared to previous AoA-based techniques, we employ an enhanced power profile modeling the signal power received from the reader along different spatial directions, which is more accurate and immune to ambient noise as well as measurement errors caused by hardware characteristics. Besides, we find that tag’s phase measurements in practice are related to its orientation. To the best of our knowledge, we are the first to point out this fact and quantify the relationship between them. By calibrating the phase shifts caused by orientation, the positioning accuracy can be improved by 3.7×. We have implemented Tagspin with COTS RFID devices and evaluated it extensively. Experimental results show that Tagspin achieves mean accuracy of 7.3cm with standard deviation of 1.8cm in 3D space.

Keywords—RFID; reader localization; Tagspin

# I. INTRODUCTION

Radio Frequency IDentification (RFID) is a rapidly developing technology which uses RF signals for automatic identification of objects. Many new RFID localization systems have shown high precision, such as [1]–[4]. Much of the attention has been paid on how to accurately locate the RFID tags instead of readers. Many applications would benefit from accurate tag localization or tracking. For example, it can aid in supply chain management, automatic customer checkout in a supermarket, enable human-machine interaction with the tag attached on the finger, etc. However, considering previous work locating tags, all of them have a mandatory precondition that the reader’s location is known or calibrated in advance. This calibration procedure is often conducted manually, which can be time-consuming, laborious and inaccurate, especially when many antennas are required. To illustrate this, we repeat the experimentation in [4], trying to give a practical example. In summary, the inconvenience of calibration are mainly three folds: a) time cost: It takes us 20 ∼ 30 minutes to calibrate all four antennas and the more antennas needed, the more time spent. b) energy cost: To get the antennas’ accurate locations, we need to measure their coordinates carefully along the three spatial axes, which is quite exhausting and boring. c) accuracy cost: To achieve high accuracy, more antennas are needed with each of them further apart. This however, would add more errors to the calibration results, which in turn will decrease the final tag localization precision. So our point is, to accomplish the goal of fine-grained tag localization, the calibration for RFID reader antennas is very necessary and existing manual method is not satisfactory enough. To tackle this, a simple, convenient and accurate way of calibration is in pressing demand.

At first glance, why not use the existing methods locating tags to pinpoint readers? One dominate approach locating tags is to deploy plenty of tags as references [1], [5]. The difference of RSSI [5] or multi-path profile [1] between the target and reference tag is used as a metric for their spatial distance. The nearest neighbours of the target tag are identified and the target tag’s location is considered as the average of the neighbors’. Apparently, the reader’s location is independent of reference tags for this approach, and thereby cannot be inferred by tags, even knowing all tags’ locations. Another method is Synthetic Aperture Radar (SAR), which has been widely used for mapping the topography of the Earth’s surface, and is also introduced for RFID localization recently. Specially, a moving reader takes snapshots of the tag’s signals at different spatial directions. The snapshots mimic a large-scale antenna array. Then, the standard antenna array equations on the signals are used to compute the relative powers received from transmitting source along different spatial directions. It, however, is infeasible for us to move the reader when our goal is to calibrate it.

In this paper, we present an light-weighted, inexpensive yet highly precise reader localization system with centimeter-level positioning accuracy using a few infrastructural reference tags. Rather than relying on the dynamic movement of reader to produce a virtual antenna array, Tagspin reverses the approach by relying on the spinning motion of infrastructure tags to produce predicable, distinguishable and periodic signal snapshots. These snapshots caught from each spinning tag mimic a circular antenna array. The reason why we prefer circular array to linear array is that to simulate the same number of virtual tags, linear array requires more space than circular array and is sometimes unpractical especially in space-limited environment. Besides, moving the tag along a line is also more troublesome than making it travel on a circle. In our experiment, to simulate circular antenna array, we simply make the tag spinning by attaching it onto the edge of a disk which slowly rotates with a stable speed. An SAR-based method is designed to estimate the relative power profile over all possible spatial angles. The profile has a sharp peak at the real direction from tag to reader. Specially, the direction starting from the spinning tag with known location determines a straight line that passes through or nearby the target reader. More than two (or more) lines are generated by using two (or more) spinning tags in 2D and even 3D space. Finally, the target can be pinpointed from the intersection of these lines. To illustrate Tagspin’s approach, Fig. 1(a) shows a toy example with three spinning tags. Each tag moves along a pre-defined circular track with a uniform speed. Fig. 1(b)-1(d) show estimated power profiles for the three spinning tags respectively, using standard circular antenna array equations [6]. It is clear from this figure that the sharp peak in the power profile indicates the reader’s position relative to tag. Finally, the reader’s position is revealed by the three straight lines.

![](images/390a4d5d971041ccda28c1b4fae5ee97367b728922302877170b348a026b423f.jpg)  
Fig. 1: Illustration of Tagspin. (a) The signal snapshots of three spinning tags anchored in the infrastructure are used to mimic three circular antenna arrays. (b)-(d) Power profile. There is a sharp peak at the direction of the reader relative to the tag.

While some people may think the reader localization is a dual problem of tag localization because we have to know the locations of the reference tags in advance to give absolute location of the reader, our key point is that we just need a few pre-deployed infrastructural tags to easily, precisely and simultaneously locate even multiple target antennas and further locate many more surrounding tags that are of interest.

Contributions: In summary, this paper makes the following contributions:

• First, Tagspin gives an innovative improvement to the previous AoA-based localization, namely an enhanced version of spinning tag’s power profile is proposed. By doing so, the phase measurement error is well handled meanwhile both the positioning accuracy and robustness are reinforced.

Second, in the scope of our knowledge, Tagspin is the first to put forward the finding that there exists a regular pattern between tag’s phase measurements and its orientations. We quantify this interplay and calibrate corresponding phase shifts to make localization more accurate.   
Third, we implement the system with COTS RFID products and evaluate it comprehensively. Tagspin is lightweighted, time-saving and can provide mean accuracy of 7.3cm even in 3D space, which is fairly good compared to the reader antenna’s size (usually decimeter level).

The rest of the paper is organized as follows. The main design of Tagspin is overviewed in II. We present the interrelation of tag’s phase and orientation in §III. The details of our proposed power profile is described in IV. We elaborate Tagspin’s techniques under 3D space in V. The implementation of Tagspin is described in VI and evaluated in VII. We review related work in §VIII and conclude this paper in §IX.

# II. TAGSPIN OVERVIEW

Tagspin is a fined-grained UHF RFID localization system targeting to pinpoint readers, providing a resolution on the order of a few centimeters, much smaller than the read range of UHF RFIDs. Ultra-low cost UHF tags (5-10 cents each) become the preferred choice of many industrial applications. Following the common practices, we concentrate on the deployed UHF tags.

Tagspin deploys a set of spinning tags in the environment. Its infrastructure also includes a central localization server which stores the spinning tags’ locations, moving speeds and other system settings. Tagspin goes through the following steps at a high level to locate the RFID reader:

• The reader interrogates the nearby spinning tags for a while and sends the signal snapshots to the server.   
• Tagspin acquires and calibrates the phase shifts from the signal snapshots of spinning tags, using the technique in III.   
• Tagspin generates an angle spectrum for each spinning tag as described in IV.   
• Tagspin pinpoints the target reader using multiple angle spectrums (see V).

The technical details on the above steps are elaborated in the next few sections.

# III. ACQUIRING PHASE SHIFTS

In this section, we firstly model the phase shifts of spinning tag, and then introduce how to eliminate the influence from the orientations.

# A. Modeling Phase Shifts

The SAR-based localization works by comparing the phases of the received signals at multiple antennas. Suppose d(t) is the distance between the reader and tag at time t, the signal traverses a total distance of 2d(t) back and forth in RFID systems. The total phase rotation outputs by the reader equals [7]:

![](images/b220acff0bfbfc6294e2050107a4453354b0a80c9095889bbe28a69f0dfc4054.jpg)



(a) |T R| < |OR|

![](images/ab85ed1f60d52f02c6f5d9d8124c0921482537daf26f6516bcc7e8fd4616c1f2.jpg)



(b) |T R| > |OR|

![](images/2d722a4f209333f05e8878c0834db8fb516f7b6327cfe260db4e212646c97dfa.jpg)



Fig. 3: The original phase measurements.   
Fig. 2: Geometric relationship between spinning tag T and reader R.

$$
\theta (t) = \left(\frac {2 \pi}{\lambda} \times 2 d (t) + \theta_ {\mathrm{div}}\right) \bmod 2 \pi \tag {1}
$$

where λ is the wavelength. The term $\theta _ { \mathrm { d i v } }$ is called diversity term, which is related to the hardware characteristics. The phase is a periodic function with period 2π radians which repeats every $\lambda / 2$ in the distance of backscatter communication.

Now let us consider the geometric relationship between the spinning tag and the reader, as shown in Fig. 2(a). Specifically, suppose the spinning tag T rotates at the origin O with a uniform angular velocity ω. The radius of the track equals r. φ and ωt denote the angles of reader and tag at time t. Then the angle $\angle T O R$ equals ωt φ. When R is relatively far from the tag, as the figure shows, d(t) can be approximated as $\vert A R \vert$ where $T A \perp O R$ . Thus, in this case we can get the distance d(t) as

$$
d (t) = D - r \cos (\omega t - \phi) \tag {2}
$$

where $D = | O R |$ , the distance between the origin and reader. Fig. 2(b) shows the second case when $\left| T R \right| > \left| O R \right|$ . The $\angle T O A$ turns to $\omega t - \phi - \pi .$ Then

$$
\begin{array}{l} d (t) = D + r \cos (\omega t - \phi - \pi) \\ = D - r \cos (\omega t - \phi) \\ \end{array}
$$

which has the same mathematical expression as that in the first case. Apparently, d(t) can be any value in $\left[ \boldsymbol { D } - \boldsymbol { r } , \boldsymbol { D } + \boldsymbol { r } \right]$ . Finally, substituting Eqn. 2 into Eqn. 1, the received signal phases have the following expression.

$$
\theta (t) = \left(\frac {4 \pi}{\lambda} \times (D - r \cos (\omega t - \phi)) + \theta_ {\mathrm{div}}\right) \bmod 2 \pi \tag {3}
$$

# B. Calibrating Phase Shifts

We attach a tag on edge of a circular disk with a radius of 10cm (for detailed settings please refer to §VII). The tag rotates with an angle speed of 0.4425 radians per second. The centers of disk and reader locate at O(20cm, 0) and R(0, 137.7cm) respectively. Both the tag and reader are on the same plane parallel to the disk surface. We keep the reader’s position unchanged and collect the phase shifts for 400 times. The collected phase values are shown in Fig. 3. As expected, the phase shifts repeat every time the disk completes a rotation. The curve is not continuous due to the mod operation. For being convenient to study the characteristics of spinning tag’s phase shifts, we smooth the curve using the following simple approach. Suppose the sequence of phase shifts is $[ \theta ( 1 ) , \theta ( 2 ) , \cdots , \theta ( t ) ]$ , then

$$
\theta (t) = \left\{ \begin{array}{l l} \theta (t) - 2 \pi & \text { if } \theta (t) - \theta (t - 1) > \pi \\ \theta (t) + 2 \pi & \text { if } \theta (t) - \theta (t - 1) <   - \pi \\ \theta (t) & \text { otherwise } \end{array} \right.
$$

where $t > 1 .$ Fig. 4(a) shows the smoothed phase shifts and ground truth. The ground truth is calculated using Eqn. 3. Through comparisons, we have an important observation that the theoretical values of the phase sequence are not consistent with those obtained in the experiments. There is about 2.7 radians misalignment between them. As mentioned in Eqn. 1, the misalignment results from the diversity factor $\theta _ { \mathrm { d i v } }$ [4]. Since the misalignment relatively remains unchanged under the same macro environment (e.g. same temperature, humid, etc.), it is reasonable to assume $\theta _ { \mathrm { d i v } }$ is a constant term in the obtained phase sequence. Then we can use the first phase value as a reference to eliminate the influence on localization from the misalignment. The details are addressed in IV.

Here, we simply align the two sequences by subtracting 2.7 radians from the ground truth, as shown in Fig. 4(b). Overall, both sequence are matched very well except the values around peaks. There still exists about 0.7 radians gap between the two sequences, which may introduce $0 . 7 / ( 2 \pi ) \times 3 4 / 2 \approx$ 1.9cm distance error1 for certain sampling points. Specifically, we also observe that the sampling density (defined as the number of phase values collected per second) varies a lot. Roughly, the sampling density should be similar because the reader randomly interrogates the tags over time. Actually, it has higher density around the peaks and valleys (see segment A and C in Fig. 4(b)) but becomes lower in the middle segment (B). Both of these observations reveal that there must exist another factor affecting the phase values.

To explore the reason, we conduct the second experiment in which we attach the tag at the center of the circular disk (i.e. position O) and rotate the disk using the same speed, as illustrated in Fig. 5(a). In theory, since the tag stays at the origin and its distance to the reader remains unchanged, the collected phase values should always be equal. However, the phase exhibits a small fluctuation (∼ 0.7 radians) as rotating, as shown in Fig. 5(b), resulting from the tag orientation. The orientation is defined as the angle between the tag plane where its antenna deploys and the line of OR, denoted as $\rho ( t )$ in the figure. The tag’s antenna is supposed to be symmetrical as a whole. Unfortunately, the practical design always contains an offset. It causes the very small distance difference over orientation, which is badly magnified by the forth-and-back traversals. On the other hand, when $\begin{array} { r } { \rho ( t ) = \frac { \pi } { 2 } + k \pi , ( k = 0 , 1 , \cdot \cdot \cdot ) } \end{array}$ , the tag plane is perpendicular to the electric field radiated by the reader, leading to much more radiation and energy received by the tag. Thus, it has higher sampling rate near the peak or valley. Lower sampling density in the middle segment (B) also brings additional error to corresponding phase measurement.

![](images/a42c545e3412adfeae85df836bf9420db2a12d864cdb725015a0e471be37fd52.jpg)



(a) Smoothed phase shifts

![](images/8e88d2a5cd3d720f12c077186c5f920f7ee90f1cfaddf0efe60635a9ea44020a.jpg)



(b) Calibrating the diversity

![](images/0ad50148464c3b7f5accab04ea580da28ded8b8bcd3d9419ec1a221a3ddc0e1a.jpg)



(c) Calibrating the orientation   
Fig. 4: Calibrating the phase shifts. (a) The smoothed phase shifts. (b) The phase shifts after calibrating the device diversity. (c) The phase shifts after calibrating the tag orientation.

To inspect whether tag diversity and spatial location will have an impact on the relationship between tag orientation and phase value, we further conduct experiments over 20 tags with location coordinates varying among the whole surveillance region. For more details, please refer to VII-C. It turns out that with individual tag and its spatial position varying, various amplitude in the fluctuation curve is observed, but the holistic changing pattern is almost the same, which can be fitted by a Fourier transform function. Formally, we summarize our findings into the following observation.

Observation 3.1: Tag’s phase value has an inherent correlation with its orientation relative to the reader antenna, namely the angle between the tag plane and the line from tag to reader. And this specific correlation can be quantified as a function through data fitting using Fourier series.

As a result, to rectify the impact tag’s orientation imposes on its phase value, we suggest that there should be a calibration procedure before formal process of collecting phase measurements. The entire workflow is generalized as below.

• Step 1: Acquiring phase-orientation function: As a prelude stage, phase measurements versus orientation change

are sampled by attaching the tag at the center of the rotating disk. Then the correlation is fitted through Fourier series, thus a phase-orientation function is formed.

• Step 2: Calibrating phase values: Attach the tag onto the edge of the disk and collect raw phase data. Calculate the phase offset of every sampled orientation using the results in the above step. The phase value when orientation $\rho =$ $\pi / 2$ is used as a reference. Then erase the offset from original data.

After calibrating the orientation’s impact, the phase shifts are more consistent with the ground truth, as shown in Fig. 4(c). This makes the measured data more errorless and plays an active role in improving positioning accuracy.

# IV. GENERATING ANGLE SPECTRUM

Our theoretical basis is that the tag’s phase rotation exhibits different value patterns if the reader signal’s angle of arrival changes. Imagine there exists a surveillance plane where the spinning tag and reader lie on whose size is $W \times L$ . For simplicity, we first focus on the case the reader and tag are on the same plane. The extended 3D scenario is discussed in §V-B.

Suppose the target reader takes n signal snapshots of every spinning tag with each snapshot taken at time $t _ { i } .$ . Let $\vartheta _ { i } ( \phi )$ be the theoretical phase value of the $i ^ { t h }$ snapshot when signal direction is φ. Then

$$
\vartheta_ {i} (\phi) = \frac {4 \pi}{\lambda} \times (D - r \times \cos (\omega t _ {i} - \phi)) \mod 2 \pi \tag {4}
$$

From basic channel models, we can express the wireless channel parameter $h _ { i }$ measured at the $i ^ { \mathit { t h } }$ snapshot as the complex number [8]:

$$
h _ {i} = \frac {1}{D} e ^ {- \mathbf {J} \theta_ {i}} \approx \frac {1}{D} e ^ {- \frac {\mathbf {J} 4 \pi}{\lambda} (D - r \times \cos (\omega t _ {i} - \phi_ {R}))} \tag {5}
$$

where $\theta _ { i }$ is the measured phase at the $i ^ { t h }$ snapshot and $\phi _ { R }$ is denoted as the reader’s real direction. In a traditional AoA approach, the relative power $P ( \phi )$ along direction φ is calculated as

$$
P (\phi) = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} h _ {i} e ^ {- \frac {\mathbf {J} 4 \pi}{\lambda} r \times \cos (\omega t _ {i} - \phi)} \right| ^ {2} \tag {6}
$$

![](images/cf918b4d6e327d7baa9d13fce2e96a499268ce44e42b7ef772a37e633de588a9.jpg)



(a) Experiment setup

![](images/548fb021aecbd64765c3fd563772b55dbbd9685f73015d6f6d3b61a59e4e0a2d.jpg)



(b) Phase sequence   
Fig. 5: Influence of tag orientation. Fixing tag at the origin and then collecting the phase sequence. There exists about 0.7 radians shifts when changing tag’s orientation.

When we traverse through all the possible angles φ along the surveillance plane, theoretically $P ( \phi )$ will get its maximum value if and only if $\phi = \phi _ { R }$ . That’s how the previous method works. Unfortunately, in a real experimental environment, tag’s phase measurements have more or less deviation from the theoretical ones, adding error to the estimated angle φ. We know that small error of angle will cause big coordinate bias, especially when the reader is quite far from the tag, leading to low precision in real scenario. We wonder whether the positioning accuracy can be improved. As we know, tag’s phase rotation outputs by the reader is associated with hardware diversity $\theta _ { \mathrm { d i v } }$ . Namely,

$$
\theta_ {i} = \vartheta_ {i} (\phi_ {R}) + \theta_ {\mathrm{div}}
$$

Above all we need to eliminate the misalignment of measured phase resulting from term $\theta _ { \mathrm { d i v } }$ . We can use the first phase value as a reference as mentioned in §III. Divide Eqn. 6 with $h _ { 1 } ^ { 2 }$ we get:

$$
\begin{array}{l} Q (\phi) = \frac {P (\phi)}{h _ {1} ^ {2}} = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} \frac {h _ {i}}{h _ {1}} e ^ {- \frac {\mathrm{J} 4 \pi}{\lambda} r \times \cos \left(\omega t _ {i} - \phi\right)} \right| ^ {2} \tag {7} \\ = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\theta_ {i} - \theta_ {1}\right)} e ^ {- \frac {\mathbf {J} 4 \pi}{\lambda} r \cos (\omega t _ {i} - \phi)} \right| \\ \end{array}
$$

Thus, both the diversity term $\theta _ { \mathrm { d i v } }$ and distance variable D are removed.

Although the misalignment problem is solved, just replacing absolute phase value with relative one will not improve accuracy. We observe that, in practice, the angles around the ground truth may also cause comparatively large amplitudes in $Q ( \phi )$ (we will give simulation results later, as depicted in Fig. 6(a)), especially under the influence of noise. In order to further reduce error, we propose a new power profile which is an enhanced version of the original one. Inspired from previous work [4], we know that tag’s real phase measurements contain random errors, following a typical Gaussian distribution with a standard deviation of 0.1 radians. By assigning a virtual amplitude $w _ { i }$ to $Q ( \phi )$ , we get the final power profile $R ( \phi )$ , which is defined as follows.

Definition 4.1: The proposed power profile revealing the power distribution at each direction $\phi \in [ 0 , 2 \pi )$ is given by:

![](images/f7192b23b05f08869a5895e1e161e7b695d6fbff3b2c6b9e28f8d0694b0a88d3.jpg)



(a) Original power profile

![](images/8b1bed55a9504b4001427eaeeb33503642ac83ea454a0703ac89fd5362a856c6.jpg)



(b) Proposed power profile   
Fig. 6: Generated power profiles with one spinning tag. (a) Q(φ). (b) $R ( \phi )$ . The tag and target reader are centered at (20cm, 0) and (−80cm, 0) respectively.

$$
R (\phi) = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} w _ {i} e ^ {- \mathbf {J} \left(\theta_ {i} - \theta_ {1}\right)} e ^ {- \frac {\mathbf {J} 4 \pi}{\lambda} r \cos \left(\omega t _ {i} - \phi\right)} \right| ^ {2} \tag {8}
$$

where

$$
\left\{ \begin{array}{l} w _ {i} = f (\theta_ {i} - \theta_ {1}; c _ {i}, 0. 1 \times \sqrt {2}) \\ f (x; \mu , \sigma) = \frac {1}{\sigma \sqrt {2 \pi}} e ^ {- \frac {(x - \mu) ^ {2}}{2 \sigma^ {2}}} \\ c _ {i} = \vartheta_ {i} (\phi) - \vartheta_ {1} (\phi) = \frac {4 \pi r}{\lambda} (\cos (\omega t _ {1} - \phi) - \cos (\omega t _ {i} - \phi)) \end{array} \right.
$$

$f ( x ; \mu , \sigma )$ is the Probability Density Function (PDF) of Gaussian distribution $\mathcal { N } ( \mu , \sigma )$ and $c _ { i }$ is the theoretical phase of the $i ^ { t h }$ snapshot relative to the first one.

Notice that $( \theta _ { i } - \theta _ { 1 } ) - ( \vartheta _ { i } ( \phi ) - \vartheta _ { 1 } ( \phi ) ) = ( \theta _ { i } - \vartheta _ { i } ( \phi ) ) - ( \theta _ { 1 } -$ $\theta _ { 1 } ( \phi ) ,$ ). Suppose the reader is at angle φ, then, $( \theta _ { i } - \vartheta _ { i } ( \phi ) ) \sim$ $\mathcal { N } ( 0 , 0 . 1 )$ and $( \theta _ { 1 } - \vartheta _ { 1 } ( \phi ) ) \sim \mathcal { N } ( 0 , 0 . 1 )$ , then $( \theta _ { i } - \theta _ { 1 } ) \ : - \ :$ $( \vartheta _ { i } ( \phi ) - \vartheta _ { 1 } ( \phi ) ) \sim \mathcal { N } ( 0 , 0 . 1 \times \sqrt { 2 } )$ . So $\theta _ { i } - \theta _ { 1 } \sim \mathcal { N } ( c _ { i } , 0 . 1 \times$ $\sqrt { 2 } )$ . By calculating the proposed power formula $R ( \phi )$ for all possible values of $\phi$ on the whole surveillance plane, a power profile for all angles is formed. Further, by searching φ for the maximum amplitude of $R ( \phi )$ , we can get the target reader’s angle spectrum.

To demonstrate the effectiveness of our approach, a typical indoor scenario is simulated: the center of the tag’s circular antenna array is at (20cm, 0) with 10cm radius, while the target reader locates at ( 80cm, 0). Namely, the reader’s direction $\phi _ { R }$ is $1 8 0 ^ { \circ }$ . Fig. 6(a) and Fig. 6(b) present the results with $Q ( \phi )$ and $R ( \phi )$ as power formulas respectively. It can be clearly seen that in either of the situations, the generated power profile has a peak at the angle direction (180◦) from tag to reader. But the peak in Fig. 6(b) is far sharper than that in Fig. 6(a). There exists a large continuous region around the ground truth with relatively high power values in Fig. 6(a), which means when using $Q ( \phi )$ as power formula, the result is not so distinctive and may be susceptible to thermal noise. On the contrary, when $R ( \phi )$ is adopted, the real angle of target reader becomes highlighted. This is because by assigning the probability weight $w _ { i }$ to power formula, the power profile is enhanced for angles with higher probability to be the ground truth and weakened for others. Thus many false candidates fade away, protruding the real one. It validates that our proposed method is more effective and accurate than the traditional AoA approach, especially in strong noise environment.

# V. LOCATING THE TARGET READER

# A. 2D Plane

Specifically in 2D plane, by combining the results of two spinning tags’ relative power profiles, the target reader’s location can be uniquely inferred. As can be illustrated by Fig. 7, 2D is the special case of 3D and R is overlapped with $R ^ { \prime }$ . The two spinning tags’ centers are marked as $O _ { 1 }$ and $O _ { 2 } ,$ , locating at $( x _ { 1 } , y _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } )$ . Their angle spectrums generated in the previous section emit at directions $\phi _ { 1 }$ and $\phi _ { 2 }$ respectively. We establish the reference Cartesian coordinate system with the line determined by $O _ { 1 }$ and $O _ { 2 }$ as the x-axis. Then the target reader $R \mathrm { { : } } { \bf s }$ coordinates $( x _ { R } , y _ { R } )$ can be calculated as follows.

$$
\left\{ \begin{array}{l} x _ {R} = \frac {y _ {2} - y _ {1} + x _ {1} \tan \phi_ {1} - x _ {2} \tan \phi_ {2}}{\tan \phi_ {1} - \tan \phi_ {2}} \\ y _ {R} = \frac {\left(x _ {1} - x _ {2}\right) \tan \phi_ {1} \tan \phi_ {2} + y _ {2} \tan \phi_ {1} - y _ {1} \tan \phi_ {2}}{\tan \phi_ {1} - \tan \phi_ {2}} \end{array} \right. \tag {9}
$$

# B. 3D Scenario

In this section, we relax the assumption that the reader antenna and tag lie on the same plane, gaining insight into Tagspin’s technical details under 3D scenario.

First, we extend the surveillance region to 3D space with the height of H. Further, we decompose the entire region into H planes along z-axis, each of which has a size of $W \times L$ points. Theoretically, even in 3D space, the target reader’s location can be well determined with only two spinning tags. Here for the sake of experiment simplicity, we make the two spinning tags lie on the same plane with height = 0 while the reader may situate at different planes, as illustrated in Fig. 7. In addition to the azimuthal angle φ in the horizontal plane, we also need another parameter, i.e. the polar angle $\gamma$ (represents the angle between R and its projection on the horizontal plane R ) along the vertical direction to fully describe the reader antenna’s incident signal. Apparently, γ has a value falling inside the range of $[ - \pi / 2 , \pi / 2 ]$ ]. Then the phase formula in Eqn. 4 can be rewritten as

$$
\vartheta_ {i} (\phi , \gamma) = \frac {4 \pi}{\lambda} (D - r \times \cos (\omega t _ {i} - \phi) \times \cos \gamma) \bmod 2 \pi \tag {10}
$$

The original power profile $Q ( \phi , \gamma )$ is calculated by

$$
Q (\phi , \gamma) = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} e ^ {- \mathbf {J} \left(\theta_ {i} - \theta_ {1}\right)} e ^ {- \frac {\mathbf {J} 4 \pi}{\lambda} r \cos (\omega t _ {i} - \phi) \cos \gamma} \right| ^ {2} \tag {11}
$$

And the improved power profile $R ( \phi , \gamma )$ when extended to 3D case, is redefined as below.

Definition 5.1: The proposed power profile revealing the power distribution along each azimuthal direction $\phi \in [ 0 , 2 \pi )$ and polar direction $\gamma \in [ - \frac { \pi } { 2 } , \frac { \pi } { 2 } ]$ is given by:

$$
R (\phi , \gamma) = \left| \frac {1}{n} \sum_ {i = 1} ^ {n} w _ {i} e ^ {- \mathbf {J} \left(\theta_ {i} - \theta_ {1}\right)} e ^ {- \frac {\mathbf {J} 4 \pi}{\lambda} r \cos \left(\omega t _ {i} - \phi\right) \cos \gamma} \right| ^ {2} \tag {12}
$$

![](images/0fb53636f9a12a206884e3617415465688def0fb1d81f567302cced9a43b1450.jpg)



Fig. 7: Geometric relationship between the reader R and two spinning tags $T _ { 1 } , T _ { 2 }$ in 3D scenario. $R ^ { \prime }$ is $R \ ' \mathrm { s }$ projection on the horizontal plane.

where

$$
\left\{ \begin{array}{l} w _ {i} = f (\theta_ {i} - \theta_ {1}; c _ {i}, 0. 1 \times \sqrt {2}) \\ f (x; \mu , \sigma) = \frac {1}{\sigma \sqrt {2 \pi}} e ^ {- \frac {(x - \mu) ^ {2}}{2 \sigma^ {2}}} \\ c _ {i} = \vartheta_ {i} (\phi , \gamma) - \vartheta_ {1} (\phi , \gamma) \\ \qquad = \frac {4 \pi r}{\lambda} (\cos (\omega t _ {1} - \phi) - \cos (\omega t _ {i} - \phi)) \times \cos \gamma \end{array} \right.
$$

By traversing through all possible values of $\phi$ and $\gamma \mathrm { ~ \ o n ~ }$ the whole surveillance region, a power profile for all spatial angles is formed. Further, by getting φ and $\gamma$ for the maximum amplitude of $R ( \phi , \gamma )$ , the target reader’s spatial angle spectrum is generated. Combining the angle spectrums of two spinning tags in 3D space, we can infer the reader’s spatial position $( x _ { R } , y _ { R } , z _ { R } )$ in the end. Denote $O _ { 1 }$ and $O _ { 2 } \mathrm { { ' } s }$ coordinates as $( x _ { 1 } , y _ { 1 } , z _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } , z _ { 2 } )$ . In our case, $z _ { 1 } = z _ { 2 } = 0$ . Then $x _ { R } , y _ { R }$ can be similarly given by Eqn. 9. And

$$
z _ {R} = \left\{ \begin{array}{l l} \sqrt {(x _ {1} - x _ {R}) ^ {2} + (y _ {1} - y _ {R}) ^ {2}} \times \tan \gamma_ {1} & (1 3 a) \\ \sqrt {(x _ {2} - x _ {R}) ^ {2} + (y _ {2} - y _ {R}) ^ {2}} \times \tan \gamma_ {2} & (1 3 b) \end{array} \right.
$$

Actually, the final estimate of $z _ { R }$ is often obtained by comparing and balancing the results of Eqn. 13a and Eqn. 13b.

We also run simulation study to examine Tagspin’s performance under 3D environment. The similar scenario as that in 2D is simulated: the center of the tag’s circular antenna array is at $( 2 0 c m , 0 , 0 )$ with 10cm radius, while the target reader locates at $( - 6 6 . 6 c m , 0 , 5 0 c m )$ . Namely, the reader’s azimuthal angle $\phi _ { R }$ is $1 8 0 ^ { \circ }$ and polar angle $\gamma _ { R }$ is $3 0 ^ { \circ }$ . Fig. 8 depicts the original and improved power profiles in both 3D mesh and 2D image. It’s obvious that $R ( \phi , \gamma )$ still performs far better than $Q ( \phi , \gamma )$ . Besides, the ground truth corresponds to just one of the two sharp peaks, which indicates that even in 3D case, Tagspin works as well as that in 2D condition, except that it will output two candidate location estimates with symmetric z-coordinates. It’s apparent that two spatial points whose z-coordinates are opposite will generate the same distance from any point located on the horizontal plane. So it’s easy to understand why Tagspin will give two symmetric location candidates. In practical applications, there always exists dead space, causing some spatial locations impossible or meaningless. So it’s reasonable that we can eliminate ambiguity in real practice. If we want to further enhance accuracy, the third spinning tag, which rotates along the vertical direction to provide more aperture diversity in zaxis, can be introduced. This forms a part of our future work.

![](images/fcf130b4c51d860f000983b6bc3aa0136a94ea93b6c45b16d63ceae1b9b8d3dd.jpg)



(a) 3D mesh with Q(φ, γ)

![](images/2843a73dff678b6ec7764b60302b7fd3a91dccb9401adc6435733176ac63ca14.jpg)



(b) 2D image with Q(φ, γ)

![](images/9aef9240854575a1b89c8eb70279baaae02f1dfe5bceae83c21258574292eb1d.jpg)



(c) 3D mesh with R(φ, γ)

![](images/bf4b1430a309e2b63266eb8e9e6d97122b6cfe287ba03fa23712d63f9c4a3344.jpg)



(d) 2D image with R(φ, γ)

Fig. 8: Simulation results in 3D scenario. (a)-(b) The original power profile with $Q ( \phi , \gamma )$ as power formula. (c)-(d) The improved power profile with $R ( \phi , \gamma )$ as power formula.   
![](images/78168d0e223543ead7a86112aee1cf5f8525f6dcecf221bc4487e2cc681d3198.jpg)



Fig. 9: Experiment setup. We evaluate Tagspin in both 2D and 3D scenarios.

# VI. IMPLEMENTATION

We build a prototype of Tagspin using the COTS RFID reader and tags as shown in Fig. 9.

Hardware: Reader: We adopt an Impinj Speedway Revolution R420 reader [9] which is compatible with EPC Gen2 standard and supports four directional antennas at most. The whole RFID system operates during the frequency of 920.5MHz ∼ 924.5MHz band by default, which is the legal UHF band in China. Correspondingly, the wavelength ranges from 32.43cm to 32.57cm. The size of reader antenna is 22.5cm 22.5cm 4cm. Total four different antennas with circular polarization manufactured by Yeon technology [10] are used. The reader is connected to our host end through Ethernet. Tag: Altogether five types of tags from Alien Corp [11], namely Alien “Squig” (AZ-9610), “Square” (AZ-9629), “Squiglette” (AZ-9630), “2 × 2” (AZ-9634) and “Short” (AZ-9662) are employed (listed in Table I). Many of the tags are widely used in today’s industrial area, such as supply chain applications. All of them are low-cost (only about 5 cents per tag on average).

Software: We use a Samsung PC to run our algorithms, as well as connecting to the reader through Ethernet under LLRP (Low Level Reader Protocol) [12]. The machine equips Intel Core i7 CPU at 2.4GHz and 4G memory. Impinj reader extends the LLRP protocol to support the phase report. We

adjust the configuration of reader to immediately report its readings whenever tag is detected. The client code is implemented using Java language. Besides, both the reader and host have their own local clock and attach a timestamp for each tag read. In order to erase the influence of network latency, we adopt the timestamp provided by reader rather than host machine for phase value acquisition.

# VII. EVALUATION

In this section, we give the evaluation results of Tagspin. Our experiments are performed in an office room whose size is $4 0 0 \times 9 0 0 c m ^ { 2 }$ .

# A. Evaluation Methodology

Baseline: We compare Tagspin with other four localization methods, including LandMarc [5], AntLoc [13], PinIt [1] and BackPos [14]. LandMarc is an RSS-based schema which achieves combined error distance of 100cm on average. AntLoc is one of the few systems that focus on the problem of antenna localization. Its mean error is around 15cm with mobile and rotatable antenna as a prerequisite. The mean error distance of PinIt is 12cm with 6cm standard deviation requiring reference tags pre-deployed. BackPos is a phasebased method with mean error of 17cm and standard deviation of 5cm.

Metric: We adopt the error distance, defined as the Euclidean distance between the result and ground truth, as our basis metric. All ground truth is measured by a laser rangefinder with an error of ±0.1mm. For each same setting, we repeat the experiments over 50 times.

It only take Tagspin several minutes to finish the whole localization procedure, including data sampling and algorithm running. The time cost is much lower than manual calibration of antennas.

<table><tr><td>#</td><td>Model</td><td>Company</td><td>Chip</td><td>Size ( $mm^{2}$ )</td><td>QTY</td></tr><tr><td>1</td><td>AZ-9610</td><td>Alien</td><td>H3</td><td> $44.5 \times 10.4$ </td><td>4</td></tr><tr><td>2</td><td>AZ-9629</td><td>Alien</td><td>H3</td><td> $22.5 \times 22.5$ </td><td>4</td></tr><tr><td>3</td><td>AZ-9630</td><td>Alien</td><td>H3</td><td> $70 \times 9.5$ </td><td>4</td></tr><tr><td>4</td><td>AZ-9634</td><td>Alien</td><td>H3</td><td> $44 \times 46$ </td><td>4</td></tr><tr><td>5</td><td>AZ-9662</td><td>Alien</td><td>H3</td><td> $70 \times 17$ </td><td>4</td></tr></table>

TABLE I: The tag models

![](images/52bc4066fd0a924ef7ff641ed8a9a1cd5d493a84baadef1475784db37ff5b4a8.jpg)



(a) 2D

![](images/c0d23d4fd61a2b59f406a9d58d13a125cae9b49726ed37295cc189c54e7a5082.jpg)



(b) 3D   
Fig. 10: Localization error

![](images/788a252859b0a0e76b9173a87f3c343352acf1e0c6c39e2fff6aca588b2946b6.jpg)



(a) Phases vs. orientations

![](images/d4390e72714b8297bc5cbe4d283f954857708330a0f9664275e9088eefc23f9c.jpg)



(b) Error comparison   
Fig. 11: Tag orientation impact

# B. Localization Accuracy

To fully inspect Tagspin’s performance, we carry out extensive experiments in both 2D plane and 3D space.

1) 2D: As illustrated in Fig. 9, the rotating disk with a tag adhere to is placed on a flat desk, while the reader antenna is several meters away from the disk. We establish the Cartesian coordinate system with regard to the desktop, which means we treat the desktop plane as the horizontal plane. We make the reader stay on the same plane with the rotating tag under the support of a laser level. The locations of the two spinning tags’ centers are chosen to be (−20cm, 0) and (20cm, 0).

Furthermore, we change the reader’s location randomly across the surveillance plane and perform the localization procedure for 100 times. Fig. 10(a) plots the CDF of positioning error. The mean error distance of Tagspin under 2D scenario is 3.1cm in x-axis, 4.1cm in y-axis and 5.3cm in combined dimension with standard deviation of 1.6cm, outperforming LandMarc, AntLoc, PinIt and BackPos by 18.9 , 2.8 , 2.3 and 3.2 respectively. Besides, 90% of the errors are less than 7.5cm with minimal error of 1.7cm and maximum error of 9.5cm.

2) 3D: After validating Tagspin’s performance in 2D plane, we wonder whether it can still work well when applied to 3D space. As is similar to the case in 2D scenario, we still regard the desktop plane as the horizontal plane, while the reader may lie on different planes from the tags. The center locations of the two spinning tags are chosen to be (−20cm, 0, 9.5cm) and (20cm, 0, 9.5cm).

The CDF of positioning error is plotted in Fig. 10(b). The mean error distance of Tagspin in 3D space is 3.4cm in xaxis, 4.0cm in y-axis, 4.7cm in z-axis and 7.3cm in combined dimension with standard deviation of 1.8cm. It’s worth noting that none of the baseline systems are validated under 3D scenario. Even so, Tagspin outperforms the two-dimensional LandMarc, AntLoc, PinIt and BackPos by 13.7 , 2.1 , 1.6 and 2.3 respectively. Moreover, 90% of the errors are less than 9.4cm with minimal error of 2.9cm and maximum error of 11.2cm. It’s worth noting that among the three dimensions, the error on the z-axis is larger than the other two. This is because we make both spinning tags rotate along the x-y plane, which means more aperture diversity is introduced on x and y axes instead of z axis.

# C. Impact of Tag Orientation

As we mentioned in III, even if location remains unchanged, tag’s orientation does have an effect on its phase value in practice. We conduct numerous experiments to give a comprehensive analysis over different tags and locations. Totally, we test 20 tags of 5 types with each of them at 10 various locations uniformly chosen over the surveillance plane. Table I lists detailed information of the tags we adopt. Each time we make the tag’s geometric center stays at the same location, while change its orientation towards reader antenna from 0◦ to 360◦. Fig. 11(a) shows how tag’s phase measurements change along with its orientations. As to the same location, when the orientation is 90◦, namely the tag plane is perpendicular to the reader’s incident signal, we make the phase measurement collected then as the reference phase value of that location. All records in Fig. 11(a) are relative values compared to the reference one. The result is computed as an average over all the different tags and locations. It’s obvious to see that tag orientation does play a non-ignorable role in tag’s phase measurements and there exhibits stable regularity between orientation angle and corresponding phase value.

Significance of accounting for tag orientation’s impact: As stated before, a calibration step is undergone to eliminate tag orientation’s influence mathematically. We want to validate the effectiveness of our calibration method through experimentation. After collecting original phase measurements, we first deal with them normally with the calibration step and then omit the procedure to make a controlled study. The comparison results of the controlled experiments are plotted in Fig. 11(b) by CDFs. The mean error distance of Tagspin with phase calibration procedure is 7.3cm under 3D scenario, while without calibration the error is increased to 27.1cm. So it’s apparent that our idea and method of accounting for tag orientation’s impact is significant and can improve localization accuracy by 3.7 , which is an appreciable amount in indoor environment.

# D. Impact of Parameters

After evaluating Tagspin’s accuracy from a global perspective, in this subsection, we’ll discuss different parameter values, system settings and device diversity’s impact on Tagspin’s performance. Note that, all our experiments in this subsection are carried out under 3D scenario.

![](images/829409054f4f973af49ea65596b33c308b6f06b0364c0acaedf215157880cac5.jpg)



(a) Centers’ distance

![](images/d061fe49ee6e722dc0720e764fe7e1cf0567e172e2a025776835649217687fa5.jpg)



(b) Radius

![](images/41f8a6cd8e75f9c11d317f3ed9c54be9263f86223cb667528fe544cbf51d732f.jpg)



(c) Tag diversity

![](images/07cfe7157f977b8088b6eefefd6eacbbf9f0f864e80bb8b4d472fa0733b92055.jpg)



(d) Antenna diversity   
Fig. 12: Impact of parameters

1) Center Location of Spinning Tag: As we mentioned before, the x-y coordinates of the spinning tags’ two centers are fixed to ( 20cm, 0) and (20cm, 0) respectively, which means the distance between the two centers maintains a constant value as 40cm. It’s worth investigating whether their distance will exert an effect on the final localization accuracy. So we change the rotating disks’ locations and conduct sufficient experiments right along. Fig. 12(a) depicts the localization error of different distance between center locations. We make the distance as a variable whose value falls within the range from 20cm to 80cm at every 5cm interval. It can be seen from the figure that the localization error is almost stable with small vibration when the two centers’ distance  30cm. For the sake of convenience, we select the distance’s default value as 40cm in the rest of our experiments in order to achieve relatively high accuracy as well as improve space efficiency. However, when the distance is less than 30cm, especially when its smallest value (20cm) is achieved, the localization accuracy is impaired to a certain degree, which is explicable because if two centers’ distance is too short, some sampling points of different disks will get very close, bringing more uncertainty to the phase measurements, thus localization error is increased. Note that, here the radius of disk is 10cm, so the smallest value of two centers’ distance is 20cm as shown in Fig. 12(a).

2) Radius of Spinning Tag: In addition to the centers’ distance, the radius of spinning tag is another parameter that may have an influence on Tagspin’s accuracy. In our previous experiments, the radius is set to 10cm. Here, we ranging the radius from 2cm to 24cm with a step length of 2cm in order to study whether it will make a difference in positioning accuracy. The result is revealed in Fig. 12(b). We can see from the figure that when the radius value falls within the interval of [8cm, 16cm], the positioning accuracy remains high and stable. But when the radius < 8cm or > 16cm, the positioning error increases by quite an amount. The reason why localization accuracy drops is that the phase measurements along circular track become hard to be distinguished when the radius is too small and the assumption $D \gg r$ we make in III is untenable when r is too large. So it’s suggested that the value of radius should be chosen from the interval of [8cm, 16cm] and we make 10cm as default in our experiments.

3) Tag Diversity: One big advantage of our system is its simplicity, which means it only takes very simple manipulation to reach localization purpose without sacrificing precision. One of the things is that we employ only two tags from beginning to end. So tag diversity is another factor that may bring fluctuation in positioning error. Totally, we experiment on five models of tags, as illustrated in Table I, all of which have different antenna sizes and shapes. As our proposed method has already taken device diversity into consideration, it’s expected that different tags will have little impact on accuracy. We repeat localization experiments over 20 different tags coming from the aforementioned 5 types with 4 tags each model. Fig. 12(c) plots the relationship between positioning accuracy and tag diversity. For each tag model, the localization error is calculated as an average over all the tags of that model. Our findings are as follows: a) although tag type varies, the positioning accuracy almost remains constant with maximum value only differs 0.5cm from minimum one; b) for tags of the same model, different individual basically demonstrates the same accuracy. The results are consistent with our expectation. And the tag type we adopt in most of our experiments is $ { \mathrm { ~ \hat { ~ } { ~ } 2 ~ } } \times  { \mathrm { ~ 2 ~ } } ^ { , , } (  { \mathrm { A Z } }  { - } 9 6 3 4 )$ because of its proper form factor, high signal strength and stability.

4) Antenna Diversity: Apart from the diversity caused by tags, different reader antenna is another form of device diversity that may cause uncertainty in localization accuracy. Since the reader we adopt supports four directional antennas at most, it’s convenient for us to conduct experiments for different antennas. We totally experiment on four antennas from Yeon technology. The CDFs of errors are plotted in Fig. 12(d). We observe that there is only slight difference among the positioning errors, which is in accordance with our expectation because antenna diversity is just one type of device diversity we’ve already allowed for in our method. The mean error distances of the four antennas are 7.3cm, 7.4cm, 7.5cm and 7.3cm respectively. And the corresponding standard deviations are 1.8cm, 1.8cm, 2.0cm and 1.6cm. Specifically, in most of our experiments, we use Antenna 1 as default.

# VIII. RELATED WORK

In this section, we review the state-of-the-arts that are directly related to our work.

RF-based localization: Recent years have witnessed the flourishing of myriad localization technologies, especially in RF domain. Mainstreaming works in this domain adopt Received Signal Strength Indicator (RSSI) as the fingerprint or distance ranging metric for localization [5], [14]–[19]. Typically, RSSIs of reference tags at known positions are measured and used to locate the desired tag. Besides, AoA (Angle of Arrival) is another important location indicator drawing many researchers’ attention, which works by measuring the phase difference between the received signals at different antennas [20]–[22]. Systems like ArrayTrack [23] and PinPoint [24] propose novel algorithms to calculate the AoA information, enabling localization or tracking of wireless clients at a fine granularity. While much attention has been paid on locating RFID tags, little concern has been shown for the issue of reader localization. Luo et al. [13] are the few pioneers that concentrate on the problem of reader localization. They utilize the relative angle between RFID reader and tag to locate position of reader, and use variable RF-attenuation to reduce error.

SAR: SAR is firstly used in military Radar system for both geographic imaging and object localization with the help of antenna array. Recently there is a growing interest in borrowing this idea to pervasive wireless localization domain [1], [4], [22], [25]–[27]. PinIt [1] leverages SAR technique to extract the multi-path profiles of RFID tags and then adapts dynamic time warping to pinpoint a tag’s location, which is robust to non-line-of-sight scenario. Miesen et al. [26] present a holographic method to show tag’s real position with phase values sampled from a synthetic aperture by a RFID reader. Parr et al. [27] extend the work in [26] to realize trajectory reconstruction of RFID tags through inverse synthetic aperture. The authors in [22] utilize phase difference of arrival (PDoA) information between pairs of antenna elements in each antenna array to estimate the AoA information for tag localization. Ubicarse [25] performs a new formulation of SAR on handheld devices twisted by their users to enable fine-grained indoor localization. Tagoram [4] proposes Differential Augmented Hologram (DAH) to track the tag accurately and successfully handles the thermal noise and device diversity.

# IX. CONCLUSION

In this work we present a phase-based RFID reader localization system Tagspin, which can locate the reader antenna in 3D space with only a few spinning tags. Tagspin fills in the gap of RFID reader localization area and achieves fairly good accuracy with very low time cost. Our key innovations are studies on phase patterns observed by spinning tag and as far as we know, our method is the first to quantify tag orientation’s effect on the phase measurements. We implement Tagspin using COTS RFID products and experimental results show that it achieves mean accuracy of 7.3cm with standard deviation of 1.8cm in 3D space.

# ACKNOWLEDGMENT

This research is partially supported by the NSF China General Program under Grant No. 61572282 and China Postdoctoral Science Foundation under Grant No. 2015M570100.

# REFERENCES

[1] J. Wang and D. Katabi, “Dude, where’s my card?: RFID positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[2] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “RF-compass: Robot object manipulation using RFIDs,” in Proc. of ACM MobiCom, 2013.   
[3] J. Wang, D. Vasisht, and D. Katabi, “RF-IDraw: Virtual touch screen in the air using RF signals,” in Proc. of ACM SIGCOMM, 2014.   
[4] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: Real-time tracking of mobile RFID tags to high precision using COTS devices,” in Proc. of ACM MobiCom, 2014.   
[5] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “LANDMARC: Indoor location sensing using active RFID,” Wireless Networks, vol. 10, no. 6, pp. 701–710, 2004.   
[6] S. J. Orfanidis, Electromagnetic waves and antennas. Rutgers University New Brunswick, NJ, 2002.   
[7] ImpinJ, “Speedway revolution reader application note: Low level user data support,” in Speedway Revolution Reader Application Note, 2010.   
[8] D. Tse and P. Viswanath, Fundamentals of Wireless Communication. Cambridge University Press, 2005.   
[9] “Impinj, Inc,” http://www.impinj.com/.   
[10] “Yeon Antenna,” http://www.yeon.com.tw/content/product.php?act= detail&c id=43.   
[11] “Alien,” http://www.alientechnology.com/tags/square.   
[12] EPCglobal, “Low level reader protocol (LLRP),” 2010.   
[13] R. C. Luo, C.-T. Chuang, and S.-S. Huang, “RFID-based indoor antenna localization system using passive tag and variable RF-attenuation,” in Proc. of IEEE IECON, 2007.   
[14] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu, “Anchor-free backscatter positioning for RFID tags with high accuracy,” in Proc. of IEEE INFOCOM, 2014.   
[15] G. Li, D. Arnitz, R. Ebelt, U. Muehlmann, K. Witrisal, and M. Vossiek, “Bandwidth dependence of CW ranging to UHF RFID tags in severe multipath environments,” in Proc. of IEEE RFID, 2011.   
[16] A. Rai, K. K. Chintalapudi, V. Padmanabhan, and R. Sen, “Zee: Zero-effort crowdsourcing for indoor localization,” in Proc. of ACM MobiCom, 2012.   
[17] L. Shangguan, Z. Li, Z. Yang, M. Li, and Y. Liu, “Otrack: Order tracking for luggage in mobile RFID systems,” in Proc. of IEEE INFOCOM, 2013.   
[18] L. Yang, Y. Qi, J. Fang, X. Ding, T. Liu, and M. Li, “Frogeye: Perception of the slightest tag motion,” in Proc. of IEEE INFOCOM, 2014.   
[19] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Relative Localization of RFID Tags using Spatial-Temporal Phase Profiling,” in Proc. of USENIX NSDI, 2015.   
[20] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar, “Accurate localization of RFID tags using phase difference,” in Proc. of IEEE RFID, 2010.   
[21] P. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. Rao, “Phase based spatial identification of UHF RFID tags,” in Proc. of IEEE RFID, 2010.   
[22] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, “New measurement results for the localization of UHF RFID transponders using an angle of arrival (AoA) approach,” in Proc. of IEEE RFID, 2011.   
[23] J. Xiong and K. Jamieson, “ArrayTrack: A fine-grained indoor location system,” in Proc. of USENIX NSDI, 2013.   
[24] K. R. Joshi, S. S. Hong, and S. Katti, “PinPoint: Localizing interfering radios,” in Proc. of USENIX NSDI, 2013.   
[25] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proc. of ACM MobiCom, 2014.   
[26] R. Miesen, F. Kirsch, and M. Vossiek, “Holographic localization of passive UHF RFID transponders,” in Proc. of IEEE RFID, 2011.   
[27] A. Parr, R. Miesen, and M. Vossiek, “Inverse SAR approach for localization of moving RFID tags,” in Proc. of IEEE RFID, 2013.