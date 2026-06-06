# Tagbeat: Sensing Mechanical Vibration Period With COTS RFID Systems

Lei Yang , Member, IEEE, Yao Li,

Qiongzheng Lin, Huanyu Jia, Student Member, IEEE,

Xiang-Yang Li, Fellow, IEEE, and Yunhao Liu, Fellow, IEEE, ACM

Abstract— Traditional vibration inspection systems, equipped with separated sensing and communication modules, are either very expensive (e.g., hundreds of dollars) and/or suffer from occlusion and narrow field of view (e.g., laser). In this paper, we present an RFID-based solution, Tagbeat, to inspect mechanical vibration using COTS RFID tags and readers. Making sense of micro and high-frequency vibration using random and low-frequency readings of tag has been a daunting task, especially challenging for achieving sub-millisecond period accuracy. Our system achieves these three goals by discerning the change pattern of backscatter signal replied from the tag, which is attached on the vibrating surface and displaced by the vibration within a small range. This paper introduces three main innovations. First, it shows how one can utilize COTS RFID to sense mechanical vibration and accurately discover its period with a few periods of short and noisy samples. Second, a new digital microscope is designed to amplify the micro-vibration-induced weak signals. Third, Tagbeat introduces compressive reading to inspect high-frequency vibration with relatively low RFID read rate. We implement Tagbeat using a COTS RFID device and evaluate it with a commercial centrifugal machine. Empirical benchmarks with a prototype show that Tagbeat can inspect the vibration period with a mean accuracy of 0.36ms and a relative error rate of 0.03%. We also study three cases to demonstrate how to associate our inspection solution with the specific domain requirements.

Index Terms— RIFD, backscatter communication, vibration sensing, wireless.

# I. INTRODUCTION

IBRATION is a mechanical phenomenon whereby oscillations occur around an equilibrium point. It incurs a time-based periodic or cyclic displacement of its surface around the point [1]. In many cases, vibration is undesirable

Manuscript received October 15, 2016; revised April 17, 2017 and April 28, 2017; accepted September 19, 2017; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor A. X. Liu. Date of publication December 1, 2017; date of current version December 15, 2017. This work was supported in part by ECS under Grant 25222917, in part by the NSFC General Program under Grant 61572282, in part by The Hong Kong Polytechnic University under Grant 1-ZVJ3, and in part by the Alibaba Innovative Research Program. (Corresponding author: Lei Yang.)

L. Yang and Q. Lin are with the Department of Computing, The Hong Kong Polytechnic University, Hong Kong (e-mail: young@tagsys.org; lin@tagsys.org).

Y. Li is with ING, 1102CT Amsterdam, The Netherlands (e-mail: yao.li@ing.com).

H. Jia and Y. Liu are with the School of Software, Tsinghua University, Beijing 100084, China (e-mail: yunhaoliu@gmail.com; jia@tagsys.org).

X.-Y. Li is with the School of Computer Science and Technology, University of Science and Technology of China, Hefei 230026, China (e-mail: xiangyang.li@gmail.com).

This paper has supplementary downloadable material available at http://ieeexplore.ieee.org, provided by the authors.

Digital Object Identifier 10.1109/TNET.2017.2769138

and must be observed accurately. For example, rotating machineries nowadays are widely employed in industrial equipment. Their unexpected downtime due to its undesirable vibrations has become more costly than ever before [2]. Similarly, every building or bridge has a “fundamental frequency” at which it vibrates. The frequency is related to how a structure may respond to forces like wind, or even earthquakes. On the contrary, vibrations sometimes are useful. For instance, heterogeneous mixtures (e.g., blood samples) are separated into different layers by using a shaker (or a centrifuge machine). A recent interesting application is to modulate packets of information through physical vibrations produced by the motors [3] or speakers [4] in mobile phones for near field communication. These applications are from quite different areas but have a common interest: vibration period (or vibration frequency, equivalently).

Traditional approaches for vibration sensing require specialized sensors (e.g., acceleration, velocity or displacement sensor), and most of them are neither non-intrusive nor universal. For example, accelerometers suffer from the issue of frequency-selections. Velocity sensors like laser [5] are the best choice for high-resolution and high-speed measurements, but fail in the absence of a line-of-sight to the objects. Highspeed cameras may become the third option, but are seldom adopted in industry due to their cost and deployment/usage challenges. Recent work, ART [6], exploited a new way of eavesdropping loudspeaker sounds through wireless vibrometry. However, it is not a universal solution for vibration sensing because it requires an extremely quiet environment. Any neighboring vibrations (e.g., the spinning of fans) would introduce large errors.

In this paper, we turn our attentions to a mature technology, RFID, which is evolving as a major technology enabler for identifying and tracking objects all around the world [7]–[10]. Many industries are already rapidly attaching RFID tags on their products as a replacement to barcodes. In this work we supplement the RFID communication functionality with fine-grained sensing. The concept underlying making sense of vibration using RFID is to inspect the vibration through the random and low-frequency readings of tag, where each reading is viewed as one sampling of the vibration. Specifically, vibration displaces the tag attached on the vibrating surface within a small range, resulting in a regular change pattern of backscatter signals. Tagbeat can reveal the relevant vibration information like frequency or period by discerning such communication pattern without specialized sensors. In comparison to existing vibration sensors, RFID-based vibration sensing offers an appealing alternative, with the advantages of being cost-effective and applicable to occluded and non-line-ofsight objects, e.g., inspecting chemical tubes in a centrifuge machine. Moreover, the RFID tag contains the object ID, enabling the system to automatically associate the vibration with the particular vibration object.

In this paper, we present Tagbeat to make sense of vibration using COTS RFID. Our objective is to enable universal solution that is low-cost, battery-free and non-intrusive. While vibration inspection is conceptually simple, performing it without objectionable artifacts requires considerable rigorous design. First, most displacements induced from daily vibration (e.g., shaking of auto engine) are extremely tiny, making the vibration signal hard to be well-perceived. The mobile tag is usually randomly read for about 40 times per second on average. Even more challenging is that such relatively low read rate (i.e., 40Hz) is far less than the vibration frequency, leading to sub-Nyquist sampling. Third, it is well known that backscatter signal measurement is affected by noise at the receiver side. How to quickly derive a definite and accurate vibration frequency from a few discrete and noisy samples remains challenging.

The COTS RFID reader (e.g., ImpinJ R420) supports millidegree resolution as well as microsecond-level timing accuracy in detecting the phase of the received backscatter signals. These two features offer an opportunity to resolve the vibration period with high accuracy. We discern the vibration period through the changes of phase. To this end, we design a group of novel signal processing algorithms to tackle above challenges. First, we introduce a new type of digital ‘microscope’ for micro-vibration in §III, which uses a special technique of signal processing to amplify the phase values. Second, recent advances inspire us to deal with the aliasing challenge using compressive sampling (CS). Unlike past CS-based systems, which need schedule sampling with a prepared plan, we virtually construct measurement matrix and sampling results afterwards via existing readings of tag, without any modification on low-layer of COTS readers (see §IV). We take advantage of the inherent randomness in RFID reading time to design a compressive reading. Third, we design RF Folding (see §V) to quickly search vibration period even given a few periods of noisy samples, and further enhance the correlation at correct period stochastically.

Summary of Results: In comparison to existing solutions, Tagbeat is relatively cheap and does not require heavy instrumentation of the environment. It naturally solves the object recognition problem by using the unique ID stored in the RFID tag. We built a prototype of Tagbeat using a COTS reader equipped with one directional antenna (see §VI). We used our prototype to inspect the spinning (i.e., a controllable case of vibration) of a centrifuge machine in our micro benchmarks (see §VII). Our experiments lead to the following findings:

• Tagbeat can exactly recover the signal of high-frequency vibration feeding with over 1-second samples. In LOS scenario, the period error of the recovered vibration signal has the 50th percentile of 0ms and the 90th percentile of 0.5ms. Tagbeat also achieves a mean error of 0.36ms over different RPMs. On average, the relative error rate (i.e., the ratio of the error to the true period) of Tagbeat is 0.03%, while that of Laser meter is 0.01%. Such surprisingly high accuracy makes Tagbeat a competent equivalent of specialized sensors.

• Tagbeat can discover the vibration period with a mean error of 1.56ms when given 3 periods of discrete and noisy samples. Increasing the number of samples to more than 4 periods, it rapidly reduces the mean period error to 0.011ms.   
• Tagbeat can successfully amplify the micro-vibration with 1cm-radius by 20× while keeping the period error < 0.5ms.

![](images/2390c911ba2245f787fb0963929f617fe49c1fcdfd8b13fc9b4ec52cf9437107.jpg)



(a)

![](images/9fd4f8d0283135604b9042187f8bf29d4470db2f3043825fc26eb1923b3b5750.jpg)



![](images/8ae3a1cfcdd7fcccb8e73f5d5caaaf9ee2042371b9f6eb5e709fd7c617dfafb9.jpg)



（c）

Fig. 1. Applications of Tagbeat. Tagbeat measures wind speed freely, monitors the shaking of blood samples in high-speed centrifuge, and troubleshoots auto engine. (a) Anemometer. (b) Centrifugation. (c) Car engine.   
![](images/33e4eea071c398041e0116aca884f13e9763caa3366ee7af28e6d1548cf24041.jpg)



Fig. 2. Viberation model.

Case Study: We also study three cases shown in Fig. 1 to associate Tagbeat’ inspection solution with the specific domain knowledge (refer to §VIII). The first case demonstrates how to freely measure the wind speed, breaking the limitations of power and cables. The second case utilizes Tagbeat to track blood samples in real-time, which are being shaken by a high-speed (i.e., 6, 000 RPM) centrifuge machine. Lastly, we attempt to troubleshoot our auto engine through its vibration.

Contributions: Tagbeat is the first RFID-based system that makes sense of mechanical vibration within sub-millisecond accuracy using tag’s backscatter signals. It solves a practical problem for vibration related domains, which need inspection method that is highly accurate, cost-effective, and capable of dealing with occlusion. Tagbeat introduces a group of novel signal processing algorithms, which are almost immune to most negative impacts (e.g., from diversity, noise, multipath effect and Doppler effect), without the need of ideal communication model. Furthermore, we implement and evaluate the prototype with micro benchmarks and case studies, demonstrating the practicality and effectiveness of our design.

# II. OVERVIEW

Tagbeat is an RFID-based universal solution for inspecting vibration frequency of any objects. Although we present the system in the context of spinning in most of the time, Tagbeat’s technique could be applied to any modalities of vibrations, like shaking of bridge and car engine.

# A. System Scope

The ultimate purpose of vibration inspection is applicationdependent. For example, engineers inspect the vibrations of engine for automobile diagnose, or architects want to know the fundamental frequency how a building responds. Since our goal is to provide a universal service for various upper applications, we mainly concentrate on their common interest, vibration period or vibration frequency, in this paper. How to associate our service with the purpose of the application will be demonstrated in §VIII. Generally speaking, vibration is a mechanical phenomenon whereby oscillations occur about one equilibrium point. In context of multiple equilibrium points, we could treat all vibrations as if they came from a single virtual point, thanks to the linear superposition of mechanical waves. In addition, since the RF is vulnerable to the change of environment, we should keep the environment static as much as possible. Such condition is acceptable in practice because the system requires a few millisecond samples to find the period. The macro environment can be considered as being relatively static in most of time during such short time.

![](images/86b78483a16bd737a201ea4d38ca6eff472032fc2595dea831fe61d92136afcf.jpg)



(a)

![](images/40f5d42b4b5ae9159ccc209ee7b9cafd45be5662d20b583d06595cbb740d5ec3.jpg)



(b)

![](images/014e9e6fa4dd73074f081b6d03302424ec372ca0c8aa4eeca98ef0726b486d0e.jpg)



Fig. 3. Vibration signal acquired with different distances. (a) $d _ { 0 } = 5 6 0 c m _ { ☉ }$ (b) d0 = 540cm. (c) d0 = 520cm.

# B. Problem Formulation

We leverage the periodic changes of backscatter signal to feature the target’s vibration. Backscatter signal is composed of two metrics, amplitude and phase. We treat the phase resolved from the received backscatter signals as the vibration signal for two reasons. First, the amplitude of signal is notably distorted due to multipath effect and has a terrible resolution. Second, most COTS RFID products support millidegree resolution and microsecond-level timing accuracy in the detecting the phase of the received backscatter signals [11], such that any mm-level and instant movement of tag can trigger a change on phase value. Thus, we frame our problem as follows:

Problem 1: Given a sequence of measured phase values, $\{ \tilde { \theta } [ t _ { 1 } ] , \tilde { \theta } [ t _ { 2 } ] , \cdot \cdot \cdot , \tilde { \theta } [ t _ { N } ] \}$ , with the length of N , how to find out the vibration period $T _ { v }$ such that $\theta [ t ] = \dot { \theta } [ t + T _ { v } ] . \dot { }$

The vibration period and fundamental frequency are denoted as $T _ { v }$ and $f _ { v }$ respectively. They are equivalent, i.e., $f _ { v } = 1 / T _ { v } .$ The standard unit of frequency is Hz. However, mechanical engineers would love to represent vibration or rotation in the unit of RPM (Revolution Per Minute) where $\mathrm { 1 H z = 6 0 R P M } .$ Following their practices, we sometimes also express the vibration in RPM. Furthermore, the reader remains motionless during the measurement to avoid the errors incurred by its movement.

# C. Vibration and Vibration Induced Signal

Although it is very complex to quantify a vibration, we could consider it as a combination of a serial of simple harmonic motions. To intuitively understand the vibration, we present a geometric model of spinning in Fig. 2. Any other form of vibration is a special case of the spinning model. In the figure, the tag is attached on the position B and the spinning center is at position O. The distance r from the center to the tag is called as vibration radius. When vibrating with the surface, the tag follows a typical simple harmonic motion, which can be typified by the motion of a mass on a spring. Define δ(t) to be the displacement of the tag with respect to the reader, then displacement model can be given by:

$$
\delta (t) \approx r \left(1 - \cos (2 \pi f _ {v} t)\right) \tag {1}
$$

where $f _ { v }$ is the vibration frequency. The displacement is between 0 and $2 r$ . Since the majority of vibration come from the spinning of rotating machine (e.g., fan, auto engine, smartphoneetc) and spinning is also a controllable modality of vibration, we will test our solution most of the time using such vibration.

Vibration Signal: Passive RFID system communicates using a backscatter radio link. The tag with no battery equipped, purely harvests energy from the reader’s signal. The tag modulates its ID on the backscatter signal using ON-OFF keying [12]. The phase is a common parameter supported by COTS readers, which employ preamble correlation for acquiring and tracking carrier signal [13]. Let $d _ { 0 }$ be the distance from equilibrium point B to reader R. Then the phase shift during vibration can be expressed as:

$$
\theta (t) = \left(\frac {2 (d _ {0} + \delta (t))}{\lambda} \times 2 \pi + c _ {0}\right) \bmod 2 \pi \tag {2}
$$

where $c _ { 0 }$ denotes the constant phase shift introduced by the hardware [11], [13]. Notice the total distance is $2 ( d _ { 0 } + { \bf \bar { \delta } } \delta ( t ) )$ because the signal traverses a double distance back and forth in backscatter communication. Substituting Eqn. 1 into Eqn. 2,

$$
\theta (t) \approx \phi_ {0} - \frac {4 \pi r}{\lambda} \cos (2 \pi f _ {v} t) \mod 2 \pi \tag {3}
$$

where $\begin{array} { r } { \phi _ { 0 } = \frac { 4 \pi } { \lambda } ( d _ { 0 } + r ) + c _ { 0 } } \end{array}$ is the initial phase. θ(t) is our vibration signal. From the equation, we see that the vibration signal is a cosine signal.

To visually figure out what the vibration-induced signal $( i . e . ,$ , vibration signal for short) looks like, we attach an RFID tag on a turntable and let it spin at the frequency of 2.8Hz (see §VII for details). Fig. 3 shows the acquired sequence of phase, which is our vibration signal. Specifically, Fig. 3(a) shows the phase sequence in the time domain when $d _ { 0 } = 5 6 0 c m$ . We observe a close-to-perfect representation of the vibration signal agreeing with our model that the vibration signal is a perfect cosine curve as we expected. Decreasing $d _ { 0 }$ to 540cm, the sequence is segmented into upper and lower parts due to the function of mod, as shown in Fig. 3(b). If we continue to reduce $d _ { 0 } ,$ , the lower sequence successively increases while the upper one decreases (see Fig. 3(c)). However, the one merged from these two parts is still as same as the one shown in Fig. 3(a). The discontinuity may affect the recovery of the signal and we will address this issue in the next section.

# D. Solution Sketch

In this paper, we propose a holistic solution, Tagbeat, to address the vibration problem. Querying the RFID tag attached to the vibrating surface continuously, at a high level Tagbeat goes through the following three main steps:

• Magnifying micro-vibration: Tagbeat magnifies the tiny vibration signal induced from micro-vibration, using the technique in §III, if the amplitude of the vibration signal is less than a small threshold.

• Recovering vibration signal: Tagbeat recovers the vibration signal using compressive reading as described in §IV.   
• Discovering vibration period: Finally, Tagbeat discovers the fundamental vibration period from the recovered signal (see §V).

The next few sections elaborate on the above steps, providing the technical details.

# III. MAGNIFYING MICRO-VIBRATION SIGNAL

In most of the time, the displacements induced from routine vibration are within a few centimeters, making the changes of backscatter signal too small to be perceived. This section introduces a new type of digital ‘microscope’, a microscope for vibrations.

# A. Magnifying Weak Vibration Signal

Tagbeat bootstraps its algorithm to deal with tiny vibration signal induced from the micro-vibration. We say a vibration signal is tiny when the standard derivation of its amplitude falls into within a small range (e.g., ±1.0 radians). Recalling our purpose is to look for the vibration frequency and period, our magnification algorithm must guarantee these two metrics remain unchanged.

Rational Behind: Revisiting Fig. 2, the displacement highly depends on the vibration radius (i.e., the distance from source to tag). Intuitively, moving tag far away from the vibration source (i.e., increasing vibration radius) could make the tag move in a larger range and could increase displacements. This can be also explained using Eqn. 1, which implies that δ(t) is approximately proportion to the r. Therefore, our strategy is to increase the vibration radius from r to αr where α is called as amplification factor (α > 1).

Unfortunately, many practical constraints do not allow us to physically adjust the tag’s position. We need to find a way to virtually extend the vibration radius. To facilitate our analysis, we remove the mod operation from the Eqn. 3:

$$
\theta (t) = \phi_ {0} - \frac {4 \pi r}{\lambda} \cos (2 \pi f _ {v} t) \tag {4}
$$

The removal is reasonable because the tiny vibration cannot make phase value greater than 2π. Even when the initial phase (w.r.t. $\theta ( t ) = \phi _ { 0 } )$ is close to 0 or 2π, we could adjust the reader’s position to obtain a continuous phase sequence. Following Taylor’s theorem, we can expand Eqn. 4:

$$
\begin{array}{l} \theta (t) = \theta (0) + \frac {\theta^ {\prime} (t)}{1 !} t + \frac {\theta^ {(2)} (t)}{2 !} t ^ {2} + \dots \\ = \theta (0) + r \left(\frac {8 \pi^ {2} f _ {v}}{\lambda} \sin \left(2 \pi f _ {v} t\right) + \frac {1 6 \pi^ {3} f _ {v} ^ {2}}{2 ! \lambda} \cos \left(2 \pi f _ {v} t\right) + \dots\right) \tag {5} \\ \end{array}
$$

where $\theta ^ { ( n ) }$ is the $n ^ { t h }$ order derivative. The first term $\begin{array} { r } { \theta ( 0 ) = \phi _ { 0 } - \frac { 4 \pi r } { \lambda } } \end{array}$ , which is the Direct Constant (DC) component. We do not care about DC component since it does not affect the periodicity. Let B(t) be the reminder after filtering the DC component. Namely,

$$
B (t) = r \left(\frac {8 \pi^ {2} f _ {v}}{\lambda} \sin (2 \pi f _ {v} t) + \frac {1 6 \pi^ {3} f _ {v} ^ {2}}{2 ! \lambda} \cos (2 \pi f _ {v} t) + \dots\right) \tag {6}
$$

The above equation implies that B(t) is also proportional to r, so amplifying r by α is equivalent to amplifying B(t) by α. Let $\widehat { B } ( t )$ be the amplified non-DC component, which is given by:

![](images/ada0b93aa76f6df5206173d90007374522015fd4ac36d5d50e9d4df4a51a368e.jpg)



(a)

![](images/96a71882dd03f6bdc66033ae49f1c61d80a142fd4e75210a94ad998aae3a913b.jpg)



Fig. 4. Illustration of magnification on tiny vibration signal. (a) Feasibility— shows the original tiny vibration signal and the amplified ones. (b) Effectiveness—plots the virtually and physically amplified vibration signal.

$$
\begin{array}{l} \widehat {B} (t) = \alpha r \left(\frac {8 \pi^ {2} f _ {v}}{\lambda} \sin (2 \pi f _ {v} t) + \frac {1 6 \pi^ {3} f _ {v} ^ {2}}{2 ! \lambda} \cos (2 \pi f _ {v} t) + \dots\right) \\ = \alpha B (t) \tag {7} \\ \end{array}
$$

Now, we put our thoughts together to show our methodology:

$$
\alpha \times \theta (t) \Rightarrow \alpha \times \delta (t) \Rightarrow \alpha \times r \Rightarrow \alpha \times B (t)
$$

Magnification Methodology: We firstly filter out non-DC component B(t) by a DC filter from original signal θ(t) as well as obtain the DC term $\theta ( 0 ) = \theta ( \bar { t } ) - B ( \bar { t } )$ . Given an amplification factor α, the amplified signal ${ \hat { \theta } } ( t )$ can be calculated as follows:

$$
\begin{array}{l} \hat {\theta} (t) = \theta (0) + \widehat {B} (t) = \theta (t) - B (t) + \alpha B (t) \\ = \theta (t) + (\alpha - 1) B (t) \mod 2 \pi \tag {8} \\ \end{array}
$$

The amplified phase value may be beyond [0, 2π], so we add the operation of mod to wrap the amplified phase, enabling the result within a reasonable range.

Fig. 4(a) shows a tiny vibration signal, whose amplitude is within 0.8 radians. The tiny signal is amplified by $1 . 5 \times \sim$ 5.5×. It is easy to validate that the vibration period remains unchanged even the signal is magnified by 7.5×. This is understandable because Tagbeat never changes the harmonic frequencies in Eqn. 6. It is worth noting that there exists small sawtooth when zooming in the curve, due to the side-effect of magnification that noise is amplified too. We will discuss how to choose an appropriate α in §VII. Further, we also conduct the second experiment in which we acquire vibration signals from 1cm- and 3cm-vibration $( i . e . , \ r = 1 c m , 3 c m )$ . Meanwhile, we amplify the signal of 1cm-vibration by 3×. These three vibration signals are shown in Fig. 4(b). In theory, the radius of 3cm-vibration is 3× than that of 1cm-vibration, so 3cm-vibration-induced signal should be the same as 3× signal of 1cm-vibration-induced. From the figure, we see the two signals match each other well as expect.

# IV. RECOVERING VIBRATION SIGNAL

As will soon become clear, the samples fail to represent the original vibration signal due to frequency aliasing. We must recover the vibration signal before discovering its period. This section starts out with the sampling fundamentals and two important insights about RFID reading. Finally, we delve into the details of compressive reading for highfrequency vibration.

# A. Sampling Fundamentals

The sampling is the process of converting a continuous domain signal into a set of discrete samples in a manner that allows to approximately represent or exactly reconstruct the original signal from the discrete samples. First of all, let’s briefly review two different sampling techniques.1 Nyquist sampling. The most fundamental principle on sampling is the Nyquist-Shannon sampling theorem, which states that when a continuous domain signal is band-limited to $[ 0 , \ : f _ { \mathrm { m a x } } ]$ , one can exactly recover the band-limited signal by just observing discrete samples of the signal at a sampling rate $f _ { s }$ which is greater than $\bar { 2 } f _ { \mathrm { m a x } } .$ . The spectrum of the sampled signal $s ( t )$ is copied and shifted every $f _ { s }$ in the Fourier domain. Since $f _ { s } ~ > ~ 2 f _ { \operatorname* { m a x } } .$ , the copied versions are isolated well so that one version can be separated for reconstructing the signal. Otherwise, the copied versions are aliased, making the reconstruction erroneous. Compressive Sampling. Intuitively, inadequate uniform sampling rate makes the instances of sampling in every cycle are identical, so these repeated instances are useless. Recent advances in the field of compressive sampling (or called compressive sensing) have developed reliable recovery algorithms for inferring sparse representations if one can randomly measure arbitrary linear combinations of the signal, then the signal could be reliably reconstructed through solving a $l _ { 1 }$ optimization problem.

# B. Two Observations

Nowadays, a modern COTS RFID reader has the ability of 40 readings per second on average, offering a sampling frequency of 40Hz. According to the Nyquist-Shannon sampling theorem, Tagbeat can only monitor the vibration signal with a frequency of lower than 20Hz, which is apparently insufficient for most cases in daily life. Can we break the limitation of Nyquist-Shannon to inspect the high-frequency vibration? In order to explain the intuition behind our work, we firstly observe the following two facts:

Observation 1 (Sparse Spectrum): A vibration signal is a kind of periodic signal, which has a maximum of $2 K + 1$ nonzero Fourier coefficients. Thus, it has a very sparse representation in the Fourier domain.

Vibration is a kind of simple harmonic motion thereby its signal is a periodic signal. We assume that the vibration keeps its fundamental frequency in a short time or only one fundamental frequency dominates its vibration each time. It is well known that any periodic signal with fundamental frequency $f _ { v }$ can be expanded as a linear combination of phasors via the exponential Fourier series, namely, $s ( t ) \ =$ $\scriptstyle \sum _ { k = - K } ^ { K } a _ { k } e ^ { \mathbf { J } 2 \pi ( k f _ { v } ) t }$ where $k f _ { v }$ is the $k ^ { t h }$ harmonic frequency of the fundamental, $a _ { k }$ represents the coefficient of the $\bar { k } ^ { t h }$ , and $K f _ { v }$ corresponds to the maximum nonzero harmonic frequency. It can been seen that a periodic signal is composed of $\bar { 2 } K + \bar { 1 }$ harmonic signals. Although the signal is not sparse at all in its time domain, it is more compact and sparse in Fourier domain. Fig. 5(a) illustrates a spectrum example of a vibration signal, which can be represented with 5 nonzero coefficients in the Fourier domain.

Observation 2 (Random Reading): COTS reader randomly read tag, offering an inherent random sampling.

COTS RFID readers adopt Q-adaptive anti-collision algorithm [14], which is a variant of ALOHA algorithm. Specifically, the reader divides the time into small slots and allows tag to randomly pick up a slot to backscatter its ID. Fig. 5(b) shows the 5-second reading trace captured in a

![](images/d0424c429d07f539fc7aa9fda4f205f80226fcebe840a352d1949dcafa116e28.jpg)  
(a)

![](images/7d1470671076f11f1184bb79a628de741cca2ea5c98d84388c0c365330b8090a.jpg)  
${ \mathrm { F i g . } }$ . 5. Two observations. (a) Sparse spectrum—shows the spectrum of a periodic vibration signal. (b) Random reading—shows the sequence of read time where each bar indicates the time when the tag is read.

COTS RFID system consisting of one ImpinJ reader [15] and one Alien tag [16]. We cannot find any specific pattern via visual inspection. We perform the Kolmogorov-Smirnov test (KS-test) to study their randomness. We find that the read time is verified to follow a uniform distribution with 0.5 significant level. Overall, we can believe the tag is read at a random time point, offering an inherent random sampling of the vibration signal. Such random sampling is able to ensure a set of sampling instances for any two cycles to be different. As long as sufficient samples are obtained, it is possible to recover the periodic signal.

# C. Compressive Reading

Inspired by the previous two observations, Tagbeat attempts to recover the vibration signal using compressive sampling. We call this process compressive reading, which contains two key tasks: (1) projecting the time-domain vibration signal into Fourier domain for a compressible and sparse representation. (2) constructing the measurement matrix to schedule the sampling. A diagram of the compressive reading is shown in Fig. 7. The input is a sequence of two-tuples, $\{ < \bar { t } _ { 1 } , \theta [ t _ { 1 } ] > , <$ < $t _ { 2 } , \theta [ t _ { 2 } ] , \ldots , < t _ { N } , \theta [ t _ { n } ] > \}$ , where $\theta [ t _ { n } ]$ ] is the phase value read at time $t _ { n }$ .

Modeling Signal: The compressive sampling requires the recovering signal to be very sparse. Observation 1 suggests that vibration signal has a very sparse representation in the Fourier domain. However, the phase sequence may be cut into several sub-sequences due to the operation of mod (see Fig. 3(c)). For example, 6.1 and 0.1 radians are actually very close in terms of the mod of 2π but have a big difference in the time domain. The discontinuous signal goes against the analysis in frequency domain. To remove the mod operation, we redefine our vibration signal by taking sin of $\theta ( t )$ and denote it as s[t]:

$$
s [ t ] = \sin (\theta [ t ]) \tag {9}
$$

Apparently, $s ( t + T _ { v } ) = \sin ( \theta ( t + T _ { v } ) ) = \sin ( \theta ( t ) ) = s ( t )$ , so $s ( t )$ maintains the same period as original phase sequence.

In addition, the phase value may have a π radians of ambiguity due to the half-wave loss such that the resolved phase may be randomly reported as $\theta ( t )$ or $\theta ( t ) + \pi$ according to [17]. This may separate the original phase sequence into two haves. For example, Fig. 6(a) shows the collected phase sequence in the domain of radian. From the figure, we observe two clusters of phase values, which have a difference of π. To address such ambiguity, we can simply define the vibration signal as

$$
s [ t ] = \sin (2 \theta [ t ]) \tag {10}
$$

Similarly, $s ( t )$ also maintains the period because $s [ t ] = s [ t +$ $T _ { v } ]$ . On the other hand, suppose the resolved phase may equal $\theta _ { 1 }$ or $\theta _ { 2 } + \pi \left( e . g . \right.$ ., due to the half-wave loss) at time t. Since si $\iota ( 2 \theta _ { 1 } ) = \sin ( 2 \theta _ { 1 } + 2 \pi ) = \sin ( 2 ( \theta _ { 1 } + \pi ) ) = \sin ( 2 \theta _ { 2 } ) $ , then $s [ t ] = \sin ( 2 \theta _ { 1 } ) = \sin ( 2 \theta _ { 2 } )$ . In other words, even though $\theta _ { 1 }$ and $\theta _ { 2 }$ have a difference of π, their values in the domain of sin(2θ) are same. In this way, the jump of π resulted from half-wave loss are successfully eliminated. Fig. 6(b) shows the transformed vibration signal in the domain of sin(2θ) where no separation is observed. The two types of definitions are similar in our problem domain. For the sake of simplicity, we adopt the first one in the subsequent sections.

![](images/0a93b1826568e7e041fe7798eccd50df938c4e3d74da234181baa2264ffeb081.jpg)



![](images/20945885c3a91173e3990c69fcf7f83ae0496ffd6a479338eb39d997b3275d72.jpg)



(b)

Fig. 6. The vibration signal shown in two domains. (a) Radian domain. (b) sin(2θ) domain.   
![](images/db24ce23898e080ced3953f216c00030e4136c3879efca57cb204f2c75b3d4c6.jpg)



Fig. 7. Illustration of compressive reading. It involves two components, signal model and measurement model.

Based on discrete Fourier transform, we have

$$
S [ k ] = \sum_ {n = 1} ^ {N} s [ n ] e ^ {- \mathbf {J} \frac {2 \pi}{N} (k - 1) (n - 1)} = \sum_ {n = 1} ^ {N} s [ n ] W _ {N} ^ {(k - 1) (n - 1)} \tag {11}
$$

where $W _ { N } = e ^ { - { \bf J } { \frac { 2 \pi } { N } } }$ and $n , k = 1 , 2 , \ldots , N$ . Correspondingly, the vibration signal can be transformed to Fourier representation with Ψ as follows:

$$
S = \Psi s \text {   or   } s = \Psi^ {- 1} S \tag {12}
$$

where $N \times N$ matrix Ψ is the Fourier basis and S is the sparse coefficient vector in Fourier domain. As the right side of Fig. 7 shows, the vibration signal s can be represented in a sparse N -dimensional coefficient vector S.

Modeling Measurement: The second task is to construct measurement matrix Φ. Existing CS systems create measurement matrix in advance and schedule the sampling based on the matrix. This fashion does not work in our scenario, because Tagbeat leverages COTS RFID system to sample the vibration. We can neither make any modification nor access low-level layer to schedule COTS reader. It is also impossible to command COTS tag to reply at a specific timing like proposed in [18]. The inherent random reading shown in Observation 2 reveals an opportunity for compressive sampling via its own inherent randomness. Harvesting this opportunity however requires more than simply aggregating the reading results. Unlike the past systems, Tagbeat constructs the measurement matrix and sampling results based on the existing readings afterwards instead of making them beforehand.

We discretize the total read time into N basic time slots, $\{ t _ { 1 } , ~ t _ { 2 } , ~ . ~ . ~ . ~ , ~ t _ { N } \}$ , at millisecond level. Each reading (or sampling) only occurs within a time slot. The left side of Fig. 7 illustrates the structure of matrix Φ. The matrix contains $M \times N$ elements and each row corresponds to the timeline from $T _ { 1 }$ to $T _ { N }$ . We aggregate $Q$ time slots into a read frame. Each row involves one read frame and the adjacent frames are staggered in two different rows. In this way, there are totally $\bar { M } = \lceil N / Q \rceil$ frames and rows. Formally, the $m ^ { t h }$ read frame starts at the $( ( m - 1 ) Q + 1 ) ^ { t h }$ time slot and ends at the $( m Q ) ^ { t h }$ time slot in the $m ^ { t h }$ row. The elements in the matrix are set to 0 $( e . g .$ , blank grid) or 1 (e.g., green grid). If $\Phi [ m , n ] = 1 { \mathrm { . } }$ , it implies that the tag was read at the $n ^ { t h }$ time slot and within the $m ^ { t h }$ frame. Otherwise, $\Phi [ m , n ] = 0$ implies that the tag was not read in the $n ^ { t h }$ time slot or the $n ^ { t h }$ slot is beyond the $\mathit { \bar { m } } ^ { t h }$ frame. Let $N \times 1$ dimension vector y be the measurement result. The element $y [ m ]$ is the aggregated result of the $m ^ { t h }$ frame, which is defined as follows:

$$
y [ m ] = \sum_ {n = 1} ^ {N} \Phi [ m, n ] s [ n ] \tag {13}
$$

Since $\Phi [ m , n ]$ is either 0 or 1, $y [ m ]$ is actually the sum of the values of the vibration signal sampled in the $m ^ { t h }$ frame. Overall, the measurement model can be given by:

$$
y = \Phi s + \eta \tag {14}
$$

where η represents the measurement noise. Notice that the second Tagbeat’s difference from the past CS systems is that the measurement result y is virtually aggregated based on the existing readings rather than physically produced by the media, allowing us to recover the signal without physical control of the reader.

It is worth noting that there may exist many zero rows in the measurement matrix. Since these zero rows do not bring any useful information and are helpless for the recovery, we can directly delete them from the measurement matrix in order to reduce the computations. However, the deletion would result in a non-uniform sampling. We must use the non-uniform Fourier basis [19] as the basis matrix.

Putting Things Together: Putting together the signal and measurement models, we have

$$
y = \Phi s + \eta = \Phi \Psi^ {- 1} S + \eta \tag {15}
$$

Recovery of the periodic vibration signal in Fourier representation amounts to solving the linear system of Eqn. 15. In the equation, Ψ is the general Fourier basis and known in advance. Φ is the binary measurement matrix constructed with the read time. y is the sampling vector calculated using the under-sampled results. The frame size Q is a user-defined parameter.

Since we discretize the read time at ms-level, the minimum resolvable granularity Tagbeat can achieve is 1ms in theory. In other words, Tagbeat could inspect the vibrations with a maximum vibration frequency of 1K Hz (or 60, 000 RPM). We believe such high frequency is sufficient for major applications because our major goal is to inspect the mechanical vibrations in our daily life. For example, the fast medical centrifugal machine in hospital has a maximum RPM of 21, 000. The engine of Tesla Model S could spin at 16, 000 RPM at most. The voiced speech of a typical adult male has a fundamental frequency from 85 to 180Hz, and that of a female from 166 to 255Hz [20]. All of them are far less than our upper bound.

# D. Reconstructing Vibration Signal

There are only K nonzero elements in $\textit { S } \left( i . e . , \textit { S } \right)$ is K-sparse). The number of nonzero elements as well as their positions in $S$ are unknown. A striking result in compressive sampling is that it is still possible to recover $S$ with high probability by solving the following $l _ { 1 }$ optimization problem:

![](images/23d7d8234bf03085fe4faf22d23862682c068a47eb2a937de16f062ccb5270be.jpg)



Fig. 8. The reconstructed vibration signal.

$$
\widehat {S} = \arg \min _ {S} \| S \| _ {1} \text {   s.t.   } y = \Phi \Psi^ {- 1} S \tag {16}
$$

where $\| \cdot \| _ { 1 ( 2 ) }$ is the $l _ { 1 } - \ ( \mathrm { o r } \ l _ { 2 ^ { - } } )$ norm. However, the signals are always measured with noise (denoted by η in Eqn. 15), the reconstruction would be achieved in practice by solving a relaxed $l _ { 1 }$ -minimization problem:

$$
\widehat {S} = \min _ {S} \| S \| _ {1} \text {   s.t.   } \left\{ \begin{array}{l} \| y - \Phi \Psi^ {- 1} S \| _ {2} <   \varepsilon \\ - 1 \leq S \leq 1 \end{array} \right. \tag {17}
$$

The ε is a predefined error threshold. It has been shown that the above l1-minimization problem can be resolved with linear programming technique [21]. There is numerous on-going work looking for low-complexity reconstruction techniques in order to reduce the cost of computing when N is too large. The deletion does not affect the recovery However, this topic is out of our scope. In addition, we add one more condition that the value of S should be in [−1, 1], because we take sin of the phase.

Compressive sampling theory tells that a K-sparse signal can be reconstructed from M measurements if M satisfies the following condition [22]: $M \ge b \cdot \mu ^ { 2 } ( \Phi , \Psi ) \cdot K$ · log N where b is a positive constant, and $\mu ( \Phi , \Psi )$ is the coherence between measurement matrix Φ and representation basis Ψ. The coherence metric measures the largest correlation between any two element of Φ and Ψ, is defined as: $\mu ( \Phi , \Psi ) =$ $\breve { \overline { { N } } } \cdot \operatorname* { m a x } _ { 1 \leq i , j \leq N } | \langle \phi _ { i } , \psi _ { j } \rangle |$ . Based on the above equation, we can see that the smaller the coherence between Φ and Ψ is, the less measurements are needed to reconstruct the signal. Thanks to the inherent randomness in RFID reading time, we can approximately consider that the measurement matrix is randomly generated. Thus, Φ is a random matrix. It has been shown that a random Φ is largely incoherent with any fixed representation basis Ψ, and $\breve { M } \ = \ 3 K \sim \ 4 K$ is usually sufficient.

An example of vibration signal and its recovery using compressive reading is shown in Fig. 8. The fundamental frequency of the vibration signal equals 33Hz $( \ T _ { v } \approx 3 3 m s )$ . In our experiment, we set $\bar { N = 5 , 0 0 0 , Q = 5 }$ , and $K = 1 0$ . We see that the signal can be sampled less than three times on average in each cycle $( i . e . , 8 / 3 )$ , but the recovered signal is almost as same as the original signal.

# E. Achieving Continuous Spectrum

The fundamental vibration frequency may be time-variant. Sometimes, the upper applications are interested in frequency distributions over time (e.g., troubleshooting auto engine). Tagbeat can achieve continuous spectrum by sliding a window function, which is nonzero for only a short period of time, over the original vibration signal. Mathematically, this is written as:

![](images/3b74a46869a58663836fb17a4a98245c25c37bfd6f1acceaa7561977de5b6025.jpg)



(a)

![](images/9766918d9fac803334d6d9c9a8cec3869a9594004c2320ecf9c013b26adf9941.jpg)



Fig. 9. Achieving continuous spectrum. The continuous spectrum recovered from time-varying vibration. (a) Acquired phase sequence. (b) Resolved specturm.

$$
\hat {s} [ n ] = \sum_ {n = 1} ^ {N} s [ n ] w [ n - w ] \tag {18}
$$

where $w [ n ]$ is the window function, commonly a Gaussian window centered around zero. For example, we monitor the spectrum of a turntable with dynamic vibration frequencies. In the experiment, we firstly start the device and immediately adjust its vibration from 0 RPM to maximum (2, 000 RPM). We then slowly decrease the vibration to 1, 000 RPM (16Hz), and finally change it back to 2, 000 RPM again. Tagbeat uses the above approach to obtain its continuous spectrum, as shown in Fig. 9. From the figure, we can observe two apparent stages as we performed. The frequency quickly reaches to 33Hz and then swings between 16Hz and 33Hz, which fully fits our operations. This example shows Tagbeat is able to monitor time-varying vibration.

Practical Discussions: Finally, we present some practical discussions in supplementary materials with respect to the practicality of compressive reading.

# V. DISCOVERING VIBRATION PERIOD

After recovering the vibration signal, Tagbeat needs to discover its vibration period. Since we have reconstructed the coefficient vector S in Fourier domain, the naive approach is to obtain the fundamental frequency by calculating the greatest common divisor of all the harmonic frequencies $\in S .$ As we will show in §VII, such naive method however has a very bad accuracy (> 100ms) because the result could easily fly away due to noisy frequencies.

Estimating the fundamental frequency has received a lot of attentions in speech processing [23], [24]. The popular one is to fast fold (or auto-correlate) the time-domain signal such that the folding inputting with correct period hypothesis spikes at the positions of the multiple of the fundamental period [25]–[27]. Fast folding is a general algorithm looking for the period of a signal. It can be applied to any periodic signal, but needs to wait for dozens of periods of samples to derive the correct period. For us, it is not fast enough to look for the period of vibration signal in real-time. Recalling that our vibration signal is the phase sequence, we can utilize the characteristic of radio signal to accelerate the folding. Suppose we have reversed the phase sequence $( i . e . , \arcsin ( s [ t ] )$ ) from the recovered signal and denote it as $\{ \theta [ 1 ] , \theta [ 2 ] , . . . , \theta [ N ] \}$ , our folding is defined as follows. Given an assumed period of $T ,$ , the folding divides the phase sequence into L subsequences, each of which has $T$ elements, where $L = \lfloor N / T \rfloor$ . They are denoted as $\{ \Theta _ { 1 } , \Theta _ { 2 } , . . . , \Theta _ { L } \}$ . It further superimposes these L sub-sequences in an element-wise fashion as

follows:

$$
F _ {T} [ t ] = \frac {1}{L} \sum_ {l = 1} ^ {L} w _ {l} [ t ] e ^ {\mathbf {J} (\Theta_ {l} [ t ] - \mu [ t ])} \tag {19}
$$

where

$$
\left\{ \begin{array}{l} \mu [ t ] = \frac {1}{L} \sum_ {l = 1} ^ {L} \Theta_ {l} [ t ] \\ \Delta \Theta_ {l} [ t ] = \mu [ t ] - \Theta_ {l} [ t ] \\ w _ {l} [ t ] = 2 \mathcal {F} (| \sin (\Delta \Theta_ {l} [ t ] |); 0, 0. 0 0 9) \end{array} \right.
$$

In particular, | · | and $\mathcal { F } ( \boldsymbol { x } ; \mu , \boldsymbol { \sigma } )$ denote the abstract operation and the cumulative probability function. Next, we progressively explain the above definition.

RF Folding: The RF folding’s key difference from fast folding is the way of superimposition, i.e., the definition of $F _ { T } [ t ]$ , whereby virtual interfered signals are constructed and superimposed. We use $e ^ { \mathbf { J } \tilde { \Theta } _ { l } [ t ] }$ to denote the measured RF signal in complex representation with the measured phase and unit amplitude. Our basic idea is to interfere the measured RF signal with the theoretical one. If all measured signals conform with the theoretical signal, the interfered signals will reinforce each other. The key question is: how do we know the theoretical signal? Since our approach is independent on any specific geometric model, it is impossible to get theoretical signal by assuming tag’s position like proposed in [11]. Fortunately, the law of large numbers states that the sample mean converges to the distribution expectation as the sample size increases. Thus, we use the mean of phase values to approximate their expectation, namely, $\begin{array} { r } { \mu [ t ] = \frac { 1 } { L } \sum _ { l = 1 } ^ { L } \Theta _ { l } [ t ] } \end{array}$ where $\mu [ t ]$ denotes the expectation of the $t ^ { t h }$ phase value over L sub-sequences.

Enhanced RF Folding: To enhance the superimposition at the correct period, we assign a weight wl[t] for each interfered signal. wl[t] equals cumulative probability of $( \Theta _ { l } [ t ] - \mu [ t ] )$ . However, we observe a phenomenon, called as singularity, that when the expected value is close to 0 or $2 \pi .$ , the instance may be far away from this expectation due to the function of mod, leading to their subtraction beyond the reasonable variance. For example, if $\mu [ t ] = 6 . 2 7 9$ and $\Theta _ { m } [ t ] = 6 . 3 0$ mod $2 \pi =$ 0.0168. Actually, the instance 6.30 follows within the variance $( i . e . , \sigma = 0 . 1 )$ , but their difference $\Delta \Theta _ { m } [ t ] = 6 . 2 6 \gg \sigma$ is far beyond its variance. To deal with this issue, we take sine of the difference so that the mod could be removed. We know that phase value follows Gaussian distribution, i.e., $\Delta \Theta _ { l } [ t ] \sim$ $\mathcal { N } ( 0 , 0 . 1 )$ , so si $\mathsf { \Omega } _ { 1 } ( \Delta \Theta _ { l } [ t ] ) \ \sim \ \mathcal { N } ( 0 , 0 . 0 0 9 )$ . Finally, if the folding happens to divide and align these sub-signals with the true period, the superimposing reinforces each other and make the average energy of final superimposed signal maximum. Namely, the correct periods must yield the maximum average energy of the superimposed signal.

# VI. IMPLEMENTATION

We built a prototype of Tagbeat using ImpinJ Reader [15] and the Alien tags [16].

Hardware: We adopt an ImpinJ Speedway R420 reader (for China region, firmware version is 4.8.3.240.) without any hardware or software modification. The reader is compatible with EPC Gen2 standard. The whole RFID system operates in the 920 ∼ 925 MHz band. The reader is connected to host through the wireless network (TCP/IP). It attaches a timestamp from its local clock for each tag read. We adopt the timestamp provided by the reader instead of the received time as the timing measurement to calculate the phase values, in order to eliminate the influence of network latency. One reader antenna with circular polarization manufactured by Yeon technology [28] is employed to provide ≥ 8dB gain in two directions. Four types of tags from Alien Corp [16], modeled Glint, $2 \times 2 .$ , Square, and HiScan are employed.

![](images/e5addf5345d6646e3269e64d9f520c50b88bb12e3ec31e1454dfcfbc88f54afa.jpg)



Fig. 10. Experimental setup. An RFID tag and an infrared-reflective marker are attached on a turntable which is remade from a middle-sized centrifuge machine. They are respectively monitored by RFID antenna and laser meter (for ground truth) installed on the top.

Software: We adopt Impinj LLRP Tool Kit (LTK) [29] to communicate with the reader. ImpinJ reader extends this protocol for supporting the phase report. The client software is implemented using Java (for network connection) and Matlab (for signal processing). In our experiment, we run the software at a MacBook Pro, equipped with 2.8 GHz Intel Core i7 and 16 G memory. To better understand Tagbeat, we also develop a friendly user interface with the web frameworks of Bootstrap and AngularJS (see [30]).

Open Source: All benchmark samples, source codes and runnable version of Tagbeat have been submitted to Github [30] for free download.

# VII. MICRO BENCHMARKS

We start with a few experiments that provide insight into the working of the system, with the spinning of a controllable turntable, as detailed below.

# A. Methodology

Experiment Setup: Fig. 10 shows the main experimental setup where an RFID tag is attached on a turntable (i.e., remade from a commercial centrifugal machine). The frequency of the machine can be adjusted from 0 to 2, 000 RPM. We evaluate the system in context of spinning because it is the most controllable modality of vibration, whose ground truth is easily accessible. The vibration radius equals 5cm and distance from vibration source to antenna equals 1.5m by default. In our experiment, we command the reader to continuously query the RFIDs using a fixed carrier frequency of 922 MHz. We also set the reader at high-performance mode. The detailed reader and RO (reader operation) configuration files can be found at [31]. This setup is deployed in our office in which approximate 10 individuals work. These people will introduce additional multipath propositions when approaching the tags.

Ground Truth: The laser radar can measure micro displacement very accurately, because tiny motion can alter the reflection angle. We use laser to collect the ground truth. As Fig. 10 shows, we install a hand-held laser meter on the top, meanwhile attach an infrared-reflective marker on the vibrating surface.

![](images/ef4b3bd454de82569e26608259b37c67af3390d0e799c8b61a859f9f4efc7190.jpg)



Fig. 11. Impact of sample length.

![](images/f497d00bd8f233671426ccc58b073b71e3a661eacbc80f868d00dc666de05583.jpg)



Fig. 12. Impact of multipath.

# B. Recovering Vibration Signal

We are most interested in evaluating whether Tagbeat can exactly recover the high-frequency vibration through compressive reading with respect to the following factors:

Impact of Parameters: There are two crucial parameters, N and Q, in compressive reading. These two parameters are defined in advance. The parameter N indicates how many (or how long) samples should be collected for one recovery. Setting $Q = 5 ,$ , we attempt to recover the same signal over N samples where $N = 5 0 0 , 1 , 0 0 0 , 5 , 0 0 0$ and 10, 000. The recovered results are shown in Fig. 11. It can been seen that the recovered signal becomes smoother as N increases. This is because larger N brings more observations from the original signal, improving the quality of reconstruction. However, larger N also incurs much more delays and computations. There is a trade-off choosing N between real-time and accuracy. In practice, we suggest to set $N = 3 , 0 0 0$ . The second parameter Q is the frame size specifying how many reads should be aggregated. We find that Q imposes very little impact on the recovery accuracy when it is less than the period of the signal. Our experience suggests to set Q to 5.

Impact of Multipath Effect: One of the RFID benefits over barcode is that it can identify objects without the need of lineof-sight (LOS) owing to the multipath effect. However, multipath is considered as harmful in many scenarios like tracking and symbol interference. We study the impact of multipath effect on Tagbeat. We conduct experiments in two scenarios. First, we deploy the turntable in a very clear environment without any multipath effect and set the RPM to 1, 723 (with the period of 35ms). Second, we place five metal plates around the instrument to build a multipath-rich environment. Fig. 12 plots the vibration signal recovered in these two scenarios respectively. It can been seen that the vibration signal is seriously distorted in the multipath-rich environment compared with that in clear environment. Even so, it has the same period as that recovered without multipath. This implies compressive reading is independent on the multipath effect. Interestingly, it is much easier to identify the period of a distorted signal because the distortion due to multipath breaks its symmetry. The results also testify our assumption that the backscatter signal remains the same when it is emitted from the same position where the tag repeatedly arrives.

![](images/a6ccefcf598e61fabb0081125b5a3ac6374d4a389ac964b78c29098797f34969.jpg)



Fig. 13. Impact of RPM.

![](images/e8d4cf015ea196fb520cf7f9dfa6aaa48503068a5dd17e99c2a5fc023eb685d6.jpg)



Fig. 14. Impact of diversity.

![](images/b0288dfcc3c42879afbcd7024098657e4c1265cdda8d2398eafd82e1e3d09ee9.jpg)



Fig. 15. Impact of radius.

Impact of RPM: We randomly adjust the RPM of the turntable from 1, 250 to 2, 018 with 8 levels. For each level, we conduct 50 experiments to recover the vibration signal and search its period. Fig. 13 shows the errors in these 8 levels. Totally, the mean error is 0.3624ms over these 8 levels and the average relative error rate (i.e., the ratio of the error to the true period) equals 0.03%. Such surprisingly high accuracy makes Tagbeat a competent equivalent of specialized sensors, like laser meter which has a relative error rate of 0.01%. Even the worst case (at 1, 738 RPM) only has a mean accuracy of 0.8490ms with a standard deviation of 0.98ms.

Impact of Diversity: Keeping the turntable spinning at 1, 510 RPM (i.e., period equals 39.7ms.), we repeat the evaluation over four kinds of RFID tags (Square, 2 × 2, HiScan and Glint) to study the impact of tag’s diversity. For each model, we repeat the experiments for 50 times and report the average. Fig. 14 plots the period errors over these four kinds of tags. Totally, the mean errors are all below 0.72ms. However, the deviations have a little difference. For example, the tag of 2 × 2 has a standard deviation of 0.01ms, while that of Glint is 0.61ms. We find that the deviation highly depends on the antenna size of tag. For example, the antenna size of $2 \times 2$ is 44mm × 44mm while that of Glint is 27mm × 9.7mm. Generally speaking, the tag with larger antenna absorbs more energy from reader so they behaves much more accurate and stable. Glint is the smallest model we have used.

Impact of Vibrating Radius: Fig. 15 plots the recovered vibration signals when the tag is attached with different vibrating radiuses but a same fundamental frequency. In the figure, a period of signal sequence is marked for the three signals. We can see that the period equals 50ms, 50ms and 51ms when the vibration radius is set to 2cm, 5cm and 10cm respectively. The detected periods are very close even the shapes of the vibration signals look very different, because the distortions of the signals depend on the tag’s positions, i.e., radius. Thus, Tagbeat is irrelevant to the vibrating radius.

![](images/990bc341a7666f51b7d4706368b3df4265d0b009bf7130639ba13d0666c1f488.jpg)



Fig. 16. Impact of distance.

![](images/57f5613249b8c3f3879c55224c351c5dfe148fd5029183c992e0499dafa9531d.jpg)



Fig. 17. Impact of tag number.

Impact of Distance: Fig. 16 shows the accuracy with varying distances from 1m to 12m with the same setting. As we can see, Tagbeat does not exhibit strong correlation with the distance. However, the accuracy indeed decreases a little when the distance is over than 10m, which is the range limit of the current RFID reader. When the tag is far away from the reader, the read rate would decreases. As a result, the number of samples decreases and accuracy is affected.

Impact of Tag Number: Next, we investigate the relationship between the accuracy and the number of tags. We attached extra tags nearby our target tag. Fig. 17 shows the accuracy in five cases. The target tag was totally read for #1565, #1577, #1060, #1110 and #1040 times within 30s when there are 2, 5, 10, 15 and 20 extra tags around the target tag. The read rate of the target tag does not receive any apparent effect from other tags. This shows that the ImpinJ reader has very good performance on anti-collisions, because Q-adaptive protocol [14] dynamically adjusts the frame lengths in the end of every round reading. In theory, as long as the read rate remains unchanged, the accuracy should maintain at a same level. However, there is a slight trend showing that the error increases as more tags are involved. We think more tags may disturb the reading randomness for a specific tag, making harder recovery, although the total reading distribution over multiple tags is still random.

Impact of NLOS: We conduct 100 experiments in lineof-sight and another 100 experiments in non-line-of-sight, comparing using Tagbeat and Laser to make sense of vibration. In each experiment, we maintain the same parameters (i.e., fv = 1, 666 RPM). In LOS scenario, we keep the reader antenna (or laser meter) and tag (or reflective marker) all in direct line-of-sight of each other. Fig. 20(a) shows the CDF of the period error measured by laser and Tagbeat. The laser can achieve 100% correctness, since there is no occlusion. Tagbeat has a median error of 0ms and less than 0.5ms for 90% measurements. In NLOS scenario, we put up a 1m × 2m solid wooden board between the reader antenna and tag, as well as between the laser and reflective marker. Fig. 20(b) shows the CDF of the period error. Laser cannot locate the marker and hence fails to provide an estimate of how frequently the marker moves. In contrast, RFID signal can penetrate obstacles and reach the RFID reader even when the tag is occluded. The median error remains unchanged, but 90th percentile of period error increases to 16.5ms because the obstacles still reduce SNR, decreasing the number of samples available.

![](images/6813cfd53549cec2e82e1e29cdfc47a52a00591fda07e7478a0d74c90fd1e3af.jpg)



Fig. 18. Searching period.

Impact of Half-Wave Loss: Finally, we attempts to recover non-continuous vibration signal, which are separated into two halves due to half-wave loss. The results is shown in Fig. 6(a).

# C. Discovering Vibration Period

We then verify the accuracy of the period discovering algorithm. The frequency of turntable is adjusted to 187 RPM $( \bar { T _ { v } } = 3 2 0 . 8 5 m s )$ . We collect 120s trace of vibration signal. We then randomly select # periods of data from the trace and search their periods by using Fast Folding (FF), RF Folding (RF) and Enhanced RF Folding (EF) respectively. Each experiment with same parameters is repeated for 10 times and average results are reported.

Fig. 18 shows the period error as a function of number of periods. Each group of bars plots the errors when feeding with # periods of signals. For example, when inputting 3 periods of signal, FF, RF and EF can find out the period with an error of 62.32ms, 3.825ms and 1.56ms respectively. The errors of RF and EF reduce to below 1ms when feeding with more than 4 periods of signals, while FF has a period error of 1ms even giving 8 periods of data. It shows that RF and EF are faster and more accurate to look for the period than FF. This is mainly because FF is a general folding algorithm without caring the physical meaning of signal. It can converge into the correct period as long as sufficient input data are given. On contrary, RF and EF introduce radio model for the vibration signal (i.e., interference of signals), making the folding converge to correct period in a very short time. In particular, the error of EF reduces to 0.011ms when inputting 8 periods of data. Generally, Tagbeat could recover above 10 periods of signal. The standard variance of RF is larger than that of EF. This agrees with the previous analysis that the probabilistic weight produced by EF enhances the amplitude of signals close to their expectation.

For comparison, we also discover the fundamental period based on greatest common divisor (GCD) of harmonic frequencies. In experiment, with regard to energy, top 5 ∼ 10 harmonic frequencies excluding the constant are selected to calculate the fundamental period. As a result, we find the error is above 100ms no matter how many harmonic frequencies are chosen. This is because GCD-based method is fragile to interference and noise, even 0.1Hz error on harmonic frequency would lead to dozens times of error.

![](images/a9d35a3335521be39d7913700530bbb90a899df0a284725ae092db42a8ebf38c.jpg)



Fig. 19. Magnification error.

![](images/b4cfbeb93c6d5b9b3b818d51d0956d1ce9675c898f8655e3d6187b9334a8cfc0.jpg)



![](images/20ee7e208947763f656184d52e6d92814d60b3a6ad07944013c33076e5c95087.jpg)



Fig. 20. Comparison between LOS and NLOS. (a) LOS scenario. (b) NLOS scenario.   
![](images/8b9ce1c56fa4d3da53877490c1af2edc25fdf8bc06b33ba926978034259d7680.jpg)



Fig. 21. Measured wind field.

# D. Magnifying Vibration Signal

Finally, we investigate the effectiveness of magnification for micro-vibration. In the evaluation, we want to know whether magnification changes or affects the vibration period. We amplify a vibration signal with different magnification factors and then look for its period. Fig. 19 shows the period error as a function of magnification factor. It shows that the errors are within 1ms when the vibration signal is magnified under 25×. However, its mean error and standard deviation increase to 4ms and 7ms when the factor is over than 30×, due to amplified noises. Our test suggests to keep magnification factor below 25. This phenomenon can be explained as follows. As we aforementioned, Tagbeat fails to recover the vibration signal when the deviation of the noise is greater than 0.7 radians. The magnification is a double-edged sword. It amplifies both signal and noise at the same time. However, as long as the amplified noise keeps lower than 0.7 radians (i.e., magnification factor is lower than 25×), the positive impact dominates signal and facilitates the recovery as well as discovery. On contrary, the negative impact prevents the recovery when the signal is over-amplified.

# VIII. CASE STUDY

This section studies four cases to introduce how to associate the inspection solution provided by Tagbeat with the specific domain knowledge.

# A. Case Study 1: Measuring Wind Speed

Wind is caused by differences in the air pressure. The speed of wind can be measured using a tool called as anemometer. An anemometer has three cups, each of which is mounted on a central axis, like spokes on a wheel, as shown in Fig. 1(a). When wind pushes into the cups, they rotate the axis, enabling sensor inside to transform the rotations to electrical signal. The traditional anemometer must be wired to a meter which supplies energy to the sensor and collects the signal. Thus, the anemometers must be deployed at the top of telegraph poles or equipped with a solar battery. This confines us to freely measure the wind speed, especially in the wild. Tagbeat provides a potential way to freely measure wind speed using backscatter nodes, which may be powered by a TV tower or a mobile station [32], [33], breaking deployment limitation.

To study the feasibility of using backscatter signals to measure wind speed, we deploy an industrial-sized fan to emulate the winds in our office as shown in Fig. 1(a). Meanwhile, we attach a Square tag on one cup of the anemometer. The wind speed is measured by using anemometer (for ground truth) and Tagbeat concurrently. The wind speed is expressed in the unit of $m / s ,$ so we calculate the speed with the formula of $2 r \beta / T _ { v }$ (i.e., perimeter to period). β is constant coefficient and can be calibrated in practice. r is the vibration radius and $T _ { v }$ is the inspected period. We use the prototype to measure the wind in 40 different positions. The wind field is plotted in Fig. 21. In the figure, we add a small angle to separate the ground truth and our results for comparison. Notice the wind directions are simulated in theory. We also sketch the contour of the wind based on our measurement. As a result, Tagbeat has a mean speed error of $0 . 6 1 8 1 m / s$ with a standard deviation of 0.33m/s. This case study fully shows the feasibility of using Tagbeat to measure the wind speed.

# B. Case Study 2: Monitoring Centrifugation

Centrifugation is a process which leverages centripetal force to separate various heterogeneous mixtures by using centrifuge. This equipment is the most frequently used device in hospital. It can separate whole blood into its various components, such as red blood cells, white blood cells, plasma, etc. Our partner, Hospital X, needs to centrifuge thousands of blood samples every day. It is a burdensome task to manage so many bloods. Many patients were asked for re-test due to over centrifugation. Fig. 1(b) shows a real high-speed centrifuge used in clinical laboratories. It supports 6, 000 RPM (i.e., 10ms period) of centrifugation. We attach Glint tags on 8 test tubes and let Tagbeat automatically associate the tubes with their centrifugations.

We use the machine to perform 2-minute centrifugation on these 8 tubes. We randomly pick up 600-ms recovered vibration signal and show it in Fig. 22. It can been seen that majority of samples match the recovery well even for so highfrequency vibration. In this case, we care about how much time are taken on centrifugation for each tube. Tagbeat can exactly track the vibration time. We find that the time error has a mean of 1.6s (i.e., about 16 periods) with a standard deviation of 1.8s, implying that Tagbeat can accurately track the centrifugation of each tube.

# C. Case Study 3: Troubleshooting Engine

If the vehicle shakes violently or the engine vibrates excessively when parked with the engine on, this may be an indicator of engine breakdown. A common way of troubleshooting engine is to inspect the vibration of the engine by a specialized equipment at a qualified repair shop or professional mechanic. Attaching a Square tag on the cover of the engine of our car, we put the car in neutral and utilize Tagbeat to inspect its vibration. During the testing, we dynamically increase the RPM from 1, 000 to 4, 000. We troubleshoot engine by determining how well the inspected continuous spectrum fits the records shown in the dashboard. We find that the car is in excellent condition if the matching accuracy is above 85%. Otherwise, there may be a problem about the engine.

![](images/48adce5232e6d23931399d8fc6e50eb36ea1dd554accd65c603fbd37bc3c3d97.jpg)



Fig. 22. Recovered vibration signal of one test tube.   
![](images/4b2477ed0193b8f0f7e3342b6aaac28f44666b517ede43f2d0f46ca70874b596.jpg)



Fig. 23. Spring enabled vibration.

# D. Case Study 4: Spring Enabled Vibration

Finally, we consider another common modality of vibration, i.e., spring enabled vibration. We attach an RFID tag at the tip of a spring, which is made of aluminum alloy and has a length of 10cm. The spring was placed int he clamps of the retort stand and was held together tightly enough to hold it in place. At the end of the spring where the hook is, a mass of 100 grams was placed and as a result the spring started to extend downwards. Fig. 23 shows a 200-millisecond samples and recovered vibration signal. From the figure, we can see that the vibration signal is a little distorted because of the multi-path effect. As the time increases, the displacement of tag slowly and gradually decreases due to the air resistance. This is fully reflected from the ‘amplitude’ of the vibration signal where smaller displacement induces smaller phase change.

# IX. RELATED WORK

In this section, we briefly review the related literature in vibration measurement.

Measurement With Accelerometers: Accelerometers are small devices that are installed directly on the surface of (or within) the vibration object [5], [34]. They contain a small mass which is suspended by flexible parts that operate like springs. Vibrations at higher frequencies have greater accelerations than those at lower frequencies. For this reason, accelerometers are extremely insensible to low frequency vibration. References [35] and [36] leveraged the accelerometer built within a smartwatch to track user’s hand vibration, inferring his inputs on keyboards possible in theory. Compared with accelerometers, RFID tags are relatively cheap.

Measurement With Displacement Sensors: Displacement sensors [5], like laser, capacitive and eddy-current sensors, are the best choice for high-resolution and high-speed measurements, because they could enable sensing even micron displacement very accurately [37], [38] demonstrated realtime nanometer-vibration measurements by using a DPSSL (Laser-diode-pumped microchip solid-state lasers) and the self-mixing modulation technique. Compared with laser, the advantage of Tagbeat is the ability to sense vibration through opaque obstacles.

Measurement With High-Speed Camera: Capturing highspeed events, e.g., vibrations, requires fast and high-frame-rate cameras with high photoresponsivity at short integration times. Veeraraghavan [39] leveraged the compressive sensing to turn an off-the-shelf video camera into a powerful high-speed video camera for observing periodic events. Seitz and Dyer [40] introduced a general framework for image-based analysis of repeating motions. Jia [41] repaired videos with large static background or cyclic motion. Laptev et al. [42] detected and segmented periodic motion based on sequence alignment without the need for camera stabilization and tracking.

Measurement With Wireless Vibrometry: Recent breakthrough, ART [6], exploited a new way of eavesdropping loudspeaker sounds through wireless vibrometry. Unfortunately, ART requires an extremely quiet condition. Any ambient vibrations would introduce noises, leading to relatively large errors.

# X. CONCLUSION

We present Tagbeat for real-time tracking of vibration using COTS RFID tags and readers in this work. A key innovation is to make sense of the vibration through the changes of tag’s backscatter signals. Tagbeat can sense the vibration period to an accuracy of sub-millisecond, providing the necessary precision for many novel applications, such as high-speed centrifugation. The system not only has been tested and used in practical applications, but also will open up a wide range of exciting opportunities. In our future work, we will explore more kinds of vibrations and address the limitations shown in supplementary materials.

# REFERENCES

[1] W. Weaver, Jr., S. P. Timoshenko, and D. H. Young, Vibration Problems in Engineering. Hoboken, NJ, USA: Wiley, 1990.   
[2] Y. Lei, Z. He, and Y. Zi, “Application of an intelligent classification method to mechanical fault diagnosis,” Expert Syst. Appl., vol. 36, no. 6, pp. 9941–9948, 2009.   
[3] N. Roy, M. Gowda, and R. R. Choudhury, “Ripple: Communicating through physical vibration,” in Proc. USENIX NSDI, 2015, pp. 265–278.   
[4] N. Roy and R. R. Choudhury, “Ripple II: Faster communication through physical vibration,” in Proc. USENIX NSDI, 2016, pp. 671–684.   
[5] Lion Precision. Accessed: Nov. 15, 2017. [Online]. Available: http://www.lionprecision.com/   
[6] T. Wei, S. Wang, A. Zhou, and X. Zhang, “Acoustic eavesdropping through wireless vibrometry,” in Proc. ACM MobiCom, 2015, pp. 130–141.   
[7] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “RF-compass: Robot object manipulation using RFIDs,” in Proc. ACM MOBICOM, 2013, pp. 1–12.   
[8] J. Wang, D. Vasisht, and D. Katabi, “RF-IDraw: Virtual touch screen in the air using RF signals,” in Proc. ACM SIGCOMM, 2014, pp. 1–3.   
[9] J. Wang and D. Katabi, “Dude, where’s my card?: RFID positioning that works with multipath and non-line of sight,” in Proc. ACM SIGCOMM, 2013, pp. 51–62.   
[10] O. Abari, D. Vasisht, D. Katabi, and A. Chandrakasan, “Caraoke: An e-toll transponder network for smart cities,” in Proc. ACM SIGCOMM, 2015, pp. 297–310.   
[11] L. Yang et al., “Tagoram: Real-time tracking of mobile RFID tags to high precision using COTS devices,” in Proc. ACM MobiCom, 2014, pp. 1–12.   
[12] D. M. Dobkin, The RF in RFID: Passive UHF RFID in Practice. Boston, MA, USA: Newnes, 2012.   
[13] Low Level Reader Protocol (LLRP), EPCglobal, Lawrenceville, NJ, USA, 2010.   
[14] EPCglobal. EPC Gen2. Accessed: Nov. 15, 2017. [Online]. Available: www.gs1.org/epcglobal   
[15] Impinj, Inc. ImpinJ Official Web. Accessed: Nov. 15, 2017. [Online]. Available: http://www.impinj.com/   
[16] Alien. Alien Official Web. Accessed: Nov. 15, 2017. [Online]. Available: http://www.alientechnology.com

[17] ImpinJ, “Speedway revolution reader application note: Low level user data support, revision 3.0,” ImpinJ Inc., Seattle, WA, USA, White Paper Revision 3.0, Sep. 2013.   
[18] J. Wang, H. Hassanieh, D. Katabi, and P. Indyk, “Efficient and reliable low-power backscatter networks,” in Proc. ACM SIGCOM, 2012, pp. 61–72.   
[19] Non-Uniform Fourier Transform: A Tutoria. Accessed: Nov. 15, 2017. [Online]. Available: http://homepages.inf.ed.ac.uk/   
[20] I. R. Titze and D. W. Martin, “Principles of voice production,” J. Acoust. Soc. Amer., vol. 104, no. 3, p. 1148, 1998.   
[21] D. L. Donoho, “Compressed sensing,” IEEE Trans. Inf. Theory, vol. 52, no. 4, pp. 1289–1306, Apr. 2006.   
[22] E. J. Candès, J. Romberg, and T. Tao, “Robust uncertainty principles: Exact signal reconstruction from highly incomplete frequency information,” IEEE Trans. Inf. Theory, vol. 52, no. 2, pp. 489–509, Feb. 2006.   
[23] R. C. Maher and J. W. Beauchamp, “Fundamental frequency estimation of musical signals using a two-way mismatch procedure,” J. Acoust. Soc. Amer., vol. 95, no. 4, pp. 2254–2263, 1994.   
[24] J. C. Brown, “Musical fundamental frequency tracking using a pattern recognition method,” J. Acoust. Soc. Amer., vol. 92, no. 3, pp. 1394–1402, 1992.   
[25] R. V. E. Lovelace, J. M. Sutton, and E. E. Salpeter, “Digital search methods for pulsars,” Nature, vol. 222, pp. 231–233, Apr. 1969.   
[26] D. H. Staelin, “Fast folding algorithm for detection of periodic pulse trains,” Proc. IEEE, vol. 57, no. 4, pp. 724–725, Apr. 1969.   
[27] R. Zhou, Y. Xiong, G. Xing, L. Sun, and J. Ma, “ZiFi: Wireless LAN discovery via ZigBee interference signatures,” in Proc. ACM MobiCom, 2010, pp. 49–60.   
[28] Yeon Antenna. Accessed: Nov. 15, 2017. [Online]. Available: http://www.yeon.com.tw/content/product.php   
[29] LLRP Toolkit. Accessed: Nov. 15, 2017. [Online]. Available: http://www.llrp.org   
[30] Tagbeat. Accessed: Nov. 15, 2017. [Online]. Available: https://github.com/tagsys/tagbeat   
[31] TagSee. Accessed: Nov. 15, 2017. [Online]. Available: https://github.com/tagsys/tagsee   
[32] V. Liu et al., “Ambient backscatter: Wireless communication out of thin air,” in Proc. ACM SIGCOMM, 2013, pp. 39–50.   
[33] A. N. Parks, A. Liu, S. Gollakota, and J. R. Smith, “Turbocharging ambient backscatter communication,” in Proc. ACM SIGCOMM, 2014, pp. 619–630.   
[34] Measurement Specialties. TE Connectivity Corporation. Accessed: Nov. 15, 2017. [Online]. Available: http://www.meas-spec. com/vibration-sensors.aspx   
[35] X. Liu, Z. Zhou, W. Diao, Z. Li, and K. Zhang, “When good becomes evil: Keystroke inference with smartwatch,” in Proc. ACM CCS, 2015, pp. 1273–1285.   
[36] H. Wang, T. T.-T. Lai, and R. Roy Choudhury, “Mole: Motion leaks through smartwatch sensors,” in Proc. ACM MobiCom, 2015, pp. 155–166.   
[37] P. Castellini, M. Martarelli, and E. P. Tomasini, “Laser Doppler Vibrometry: Development of advanced solutions answering to technology’s needs,” Mech. Syst. Signal Process., vol. 20, no. 6, pp. 1265–1285, 2006.   
[38] K. Otsuka, K. Abe, J.-Y. Ko, and T.-S. Lim, “Real-time nanometervibration measurement with a self-mixing microchip solid-state laser,” Opt. Lett., vol. 27, no. 15, pp. 1339–1341, Aug. 2002.   
[39] A. Veeraraghavan, D. Reddy, and R. Raskar, “Coded strobing photography: Compressive sensing of high speed periodic videos,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 33, no. 4, pp. 671–686, Apr. 2011.   
[40] S. M. Seitz and C. R. Dyer, “View-invariant analysis of cyclic motion,” Int. J. Comput. Vis., vol. 25, no. 3, pp. 231–251, 1997.   
[41] J. Jia, Y.-W. Tai, T.-P. Wu, and C.-K. Tang, “Video repairing under variable illumination using cyclic motions,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 28, no. 5, pp. 832–839, May 2006.   
[42] I. Laptev, S. J. Belongie, P. Perez, and J. Wills, “Periodic motion detection and segmentation via approximate sequence alignment,” in Proc. IEEE ICCV, Oct. 2005, pp. 816–823.   
[43] E. J. Candès et al., “Compressive sampling,” in Proc. Int. Congr. Math., vol. 3. Madrid, Spain, 2006, pp. 1433–1452.   
[44] L. Yang et al., “Anti-counterfeiting via federated RFID tags’ fingerprints and geometric relationships,” in Proc. IEEE INFOCOM, Apr./May 2015, pp. 1966–1974.   
[45] ImpinJ TSL 1128 Handheld Reader. Accessed: Nov. 15, 2017. [Online]. Available: http://www.impinj.com/products/readers/tsl-1128-handheld/   
[46] ImpinJ ATID AB700 Handheld Reader. Accessed: Nov. 15, 2017. [Online]. Available: http://www.impinj.com/products/readers/atidab700-handheld/

![](images/895f50e2c9872a27ec5b1a11c015bebc9163c81d01f98c7ac63bb4965d5cff82.jpg)



Lei Yang received the B.S. and Ph.D. degrees from the School of Software and the Department of Computer Science and Engineering, Xi’an Jiaotong University. He was a Post-Doctoral Fellow with the School of Software, Tsinghua University. He is currently a Research Assistant Professor with the Department of Computing, The Hong Kong Polytechnic University. His research interests include RFID and backscatters, and wireless and mobile computing. He received best paper awards of Mobi-Com’14 and MobiHoc’14 and the Runner-up of the

Best Video Award of MobiCom’16, and he is also a recipient of the ACM China Doctoral Dissertation Award.

![](images/5d5052b46225fd78254fd8c3b1f585d1d70aa6452ae941940c79a9ee938784cd.jpg)



Yao Li received the B.S. degree from Xiamen University, China, in 2014, and the M.S. degree from Tsinghua University, China, in 2017. She is currently with the ING Bank, Amsterdam, The Netherlands. She is also a Trainee of the ING International Talent Programme. She is a Student Member of the ACM.

![](images/0b671537ea3581727a64e1865c497ed3dd8a60e360febc8f70b46d897f75ea33.jpg)



Qiongzheng Lin received the B.S. degree from the School of Software, Tsinghua University, China, in 2012, where he is currently pursuing the Ph.D. degree with the School of Software. His research interests include radio frequency identification and sensor network, mobile sensing, and pervasive computing. He is a Student Member of the ACM.

![](images/6339c63d207e5bf1b3002ba6ee64f4249773575b1f673d6e4029ed2e79ef289a.jpg)



Huanyu Jia received the B.Eng. degree from the Software School, Beihang University, in 2015. He is currently pursuing the master’s degree with the School of Software, Tsinghua University, Beijing, China. His research interests include radio frequency identification, and mobile sensing.

![](images/1f1189f390b46388ace182e151b9623a38c3965e458ac5f1f59a6fbf11009363.jpg)



Xiang-Yang Li (F’15) received the bachelor’s degrees from the Department of Computer Science and the Department of Business Management, Tsinghua University, China, in 1995, and the M.S. and Ph.D. degrees from the Department of Computer Science, University of Illinois at Urbana– Champaign, in 2000 and 2001, respectively. He was a Professor with the Illinois Institute of Technology. His research interests include wireless networking, mobile computing, security and privacy, cyber physical systems, and algorithms. He was an ACM Dis-

tinguished Scientist in 2015. He was a recipient of the China NSF Outstanding Overseas Young Researcher (B).

![](images/bc48aa1cc152c130245090238ae41dab9c1ac738f745d47e8746193b2a117a4e.jpg)



Yunhao Liu (M’00–F’15) received the B.S. degree in automation from Tsinghua University, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, USA, in 2003 and 2004, respectively. He is currently a Chang Jiang Chair Professor and the Dean of the School of Software, Tsinghua University, China. His research interests include RFID and sensor network, the Internet and cloud computing, and distributed computing. He is a fellow of the ACM. He is an ACM Distinguished Speaker and

also the Chair of the ACM China Council. He is an Associate Editor of the IEEE/ACM TRANSACTIONS ON NETWORKING and the ACM Transactions on Sensor Networks.