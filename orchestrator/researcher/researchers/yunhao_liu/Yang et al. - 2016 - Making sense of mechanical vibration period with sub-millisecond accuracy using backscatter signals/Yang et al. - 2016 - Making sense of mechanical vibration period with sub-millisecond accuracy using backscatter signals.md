# Making Sense of Mechanical Vibration Period with Sub-millisecond Accuracy Using Backscatter Signals \*

Lei Yang $^{*†}$ , Yao Li $^{\dagger}$ , Qiongzheng Lin $^{\dagger}$ , Xiang-Yang Li $^{\ddagger}$ , Yunhao Liu $^{\dagger}$

\*Department of Computing, The Hong Kong Polytechnic University (Primary Affiliation)

$^{\dagger}$ School of Information Science and Technology, Tsinghua University (Primary Affiliation)

$^{\ddagger}$ School of Computer Science and Technology, University of Science and Technology of China

{young, yao, lin}@tagsys.org, xiangyang.li@gmail.com, yunhao@greenorbs.com

# ABSTRACT

Traditional vibration inspection systems, equipped with separated sensing and communication modules, are either very expensive (e.g., hundreds of dollars) and/or suffer from occlusion and narrow field of view (e.g., laser). In this work, we present an RFID-based solution, Tagbeat, to inspect mechanical vibration using COTS RFID tags and readers. Making sense of micro and high-frequency vibration using random and low-frequency readings of tag has been a daunting task, especially challenging for achieving sub-millisecond period accuracy. Our system achieves these three goals by discerning the change pattern of backscatter signal replied from the tag, which is attached on the vibrating surface and displaced by the vibration within a small range. This work introduces three main innovations. First, it shows how one can utilize COTS RFID to sense mechanical vibration and accurately discover its period with a few periods of short and noisy samples. Second, a new digital microscope is designed to amplify the micro-vibration-induced weak signals. Third, Tagbeat introduces compressive reading to inspect high-frequency vibration with relatively low RFID read rate. We implement Tagbeat using a COTS RFID device and evaluate it with a commercial centrifugal machine. Empirical benchmarks with a prototype show that Tagbeat can inspect the vibration period with a mean accuracy of 0.36ms and a relative error rate of 0.03%. We also study three cases to demonstrate how to associate our inspection solution with the specific domain requirements.

# CCS Concepts

\- Networks → Cyber-physical networks; •Computer systems organization → Embedded and cyber-physical systems;

# Keywords

RFID, Backscatter, Vibration, Sensing, Wireless

\*This work was conducted at Tsinghua University and The Hong Kong Polytechnic University.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

MobiCom'16, October 03-07, 2016, New York City, NY, USA

© 2016 ACM. ISBN 978-1-4503-4226-1/16/10...\$15.00

DOI: http://dx.doi.org/10.1145/2973750.2973759

# 1. INTRODUCTION

Vibration is a mechanical phenomenon whereby oscillations occur around an equilibrium point. It incurs a time-based periodic or cyclic displacement of its surface around the point $[41]$ . In many cases, vibration is undesirable and must be observed accurately. For example, rotating machineries nowadays are widely employed in industrial equipment. Their unexpected downtime due to its undesirable vibrations has become more costly than ever before $[25]$ . Similarly, every building or bridge has a “fundamental frequency” at which it vibrates. The frequency is related to how a structure may respond to forces like wind, or even earthquakes. On the contrary, vibrations sometimes are useful. For instance, heterogeneous mixtures (e.g., blood samples) are separated into different layers by using a shaker (or a centrifuge machine). A recent interesting application is to modulate packets of information through physical vibrations produced by the motors in mobile phones for near field communication $[31, 32]$ . These applications are from quite different areas but have a common interest: vibration period (or vibration frequency, equivalently).

Traditional approaches for vibration sensing require specialized sensors (e.g., acceleration, velocity or displacement sensor), and most of them are neither non-intrusive nor universal. For example, accelerometers suffer from the issue of frequency-selections. Velocity sensors like laser [6] are the best choice for high-resolution and high-speed measurements, but fail in the absence of a line-of-sight to the objects. High-speed cameras may become the third option, but are seldom adopted in industry due to their cost and deployment/usage challenges. Recent work, ART [42], exploited a new way of eavesdropping loudspeaker sounds through wireless vibrometry. However, it is not a universal solution for vibration sensing because it requires an extremely quiet environment. Any neighboring vibrations (e.g., the spinning of fans) would introduce large errors.

In this paper, we turn our attentions to a mature technology, RFID, which is evolving as a major technology enabler for identifying and tracking objects all around the world $[14, 37, 39, 40]$ . Many industries are already rapidly attaching RFID tags on their products as a replacement to barcodes. In this work we supplement the RFID communication functionality with fine-grained sensing. The concept underlying making sense of vibration using RFID is to inspect the vibration through the random and low-frequency readings of tag, where each reading is viewed as one sampling of the vibration. Specifically, vibration displaces the tag attached on the vibrating surface within a small range, resulting in a regular change pattern of backscatter signals. Tagbeat can reveal the relevant vibration information like frequency or period by discerning such communication pattern without specialized sensors. In comparison to existing vibration sensors, RFID-based vibration sensing offers an appealing alternative, with the advantages of being cost-effective and applicable to occluded and non-line-of-sight objects, e.g., inspecting chemical tubes in a centrifuge machine. Moreover, the RFID tag contains the object ID, enabling the system to automatically associate the vibration with the particular vibration object.

![](images/75d2d7cb21b481be0ac9936213d5e1b458989b6c096b70608a666d0b49469615.jpg)



(a) Anemometer

![](images/866ada970b15204ddcdd1fb90d25b984a085d592c729e78e3c66e11bb1a0658d.jpg)



(b) Centrifugation

![](images/4089be332e27f630f1114b0a3e5a11c0e46fe58df1d035db73de83a7cc140b86.jpg)



(c) Car engine   
Figure 1: Applications of Tagbeat. Tagbeat measures wind speed freely, monitors the shaking of blood samples in high-speed centrifuge, and troubleshoots auto engine.

In this paper, we present Tagbeat to make sense of vibration using COTS RFID. Our objective is to enable universal solution that is low-cost, battery-free and non-intrusive. While vibration inspection is conceptually simple, performing it without objectionable artifacts requires considerable rigorous design. First, most displacements induced from daily vibration (e.g., shaking of auto engine) are extremely tiny, making the vibration signal hard to be well-perceived. The mobile tag is usually randomly read for about 40 times per second on average. Even more challenging is that such relatively low read rate (i.e., 40Hz) is far less than the vibration frequency, leading to sub-Nyquist sampling. Third, it is well known that backscatter signal measurement is affected by noise at the receiver side. How to quickly derive a definite and accurate vibration frequency from a few discrete and noisy samples remains challenging.

The COTS RFID reader (e.g., ImpinJ R420) supports millidegree resolution as well as microsecond-level timing accuracy in detecting the phase of the received backscatter signals. These two features offer an opportunity to resolve the vibration period with high accuracy. We discern the vibration period through the changes of phase. To this end, we design a group of novel signal processing algorithms to tackle above challenges. First, we introduce a new type of digital 'microscope' for micro-vibration in §3, which uses a special technique of signal processing to amplify the phase values. Second, recent advances inspire us to deal with the aliasing challenge using compressive sampling (CS). Unlike past CS-based systems, which need schedule sampling with a prepared plan, we virtually construct measurement matrix and sampling results afterwards via existing readings of tag, without any modification on low-layer of COTS readers (see §4). We take advantage of the inherent randomness in RFID reading time to design a compressive reading. Third, we design RF Folding (see §5) to quickly search vibration period even given a few periods of noisy samples, and further enhance the correlation at correct period stochastically.

Summary of Results: In comparison to existing solutions, Tagbeat is relatively cheap and does not require heavy instrumentation of the environment. It naturally solves the object recognition problem by using the unique ID stored in the RFID tag. We built a prototype of Tagbeat using a COTS reader equipped with one directional antenna (see §6). We used our prototype to inspect the spinning (i.e., a controllable case of vibration) of a centrifuge machine in our micro benchmarks (see §7). Our experiments lead to the following findings:

- Tagbeat can exactly recover the signal of high-frequency vibration feeding with over 1-second samples. In LOS scenario, the period error of the recovered vibration signal has the $50^{th}$ percentile of $0ms$ and the $90^{th}$ percentile of $0.5ms$ . Tagbeat also achieves a mean error of $0.36ms$ over different RPMs. On average, the relative error rate (i.e., the ratio of the error to the true period) of Tagbeat is $0.03\%$ , while that of Laser meter is $0.01\%$ . Such surprisingly high accuracy makes Tagbeat a competent equivalent of specialized sensors.   
- Tagbeat can discover the vibration period with a mean error of $1.56ms$ when given 3 periods of discrete and noisy samples. Increasing the number of samples to more than 4 periods, it can rapidly reduce the mean period error to $0.011ms$ .   
- Tagbeat can successfully amplify the micro-vibration with $1cm$ -radius by $20\times$ while keeping the period error within $0.5ms$ .

Case Study. We also study three cases shown in Fig. 1 to associate Tagbeat' inspection solution with the specific domain knowledge (refer to §8). The first case demonstrates how to freely measure the wind speed, breaking the limitations of power and cables. The second case utilizes Tagbeat to track blood samples in real-time, which are being shaken by a high-speed (i.e., 6,000 RPM) centrifuge machine. Lastly, we attempt to troubleshoot our auto engine through its vibration.

Contributions: Tagbeat is the first RFID-based system that makes sense of mechanical vibration within sub-millisecond accuracy using tag's backscatter signals. It solves a practical problem for vibration related domains, which need inspection method that is highly accurate, cost-effective, and capable of dealing with occlusion. Tagbeat introduces a group of novel signal processing algorithms, which are almost immune to most negative impacts (e.g., from diversity, noise, multipath effect and Doppler effect), without the need of ideal communication model. Furthermore, we implement and evaluate the prototype with micro benchmarks and case studies, demonstrating the practicality and effectiveness of our design.

# 2. OVERVIEW

Tagbeat is an RFID-based universal solution for inspecting vibration frequency of any objects. Although we present the system in the context of spinning in most of the time, Tagbeat's technique could be applied to any modalities of vibrations, like shaking of bridge and car engine.

# 2.1 System Scope

The ultimate purpose of vibration inspection is application-dependent. For example, engineers inspect the vibrations of engine for automobile diagnose, or architects want to know the fundamental frequency how a building responds. Since our goal is to provide a universal service for various upper applications, we mainly concentrate on their common interest, vibration period or vibration frequency, in this paper. How to associate our service with the purpose of the application will be demonstrated in §8. Generally speaking, vibration is a mechanical phenomenon whereby oscillations occur about one equilibrium point. In context of multiple equilibrium points, we could treat all vibrations as if they came from a single virtual point, thanks to the linear superposition of mechanical waves.

![](images/54c5cf8dafbfd93f5627ced3f4e899d57e8d3bd8980a0faa6e9d6b29fe02d117.jpg)



Figure 2: Vibration model.

![](images/8f801dde880c0abf4ff2709fe4d455246b1e64d4cecd34c552206bbe088470e2.jpg)



(a) $d_0 = 560cm$

![](images/fde6603bdebdfb5c8cc7b3dd45f8204294a95bf061c7e68cb29df36203e241eb.jpg)



(b) $d_{0} = 540cm$

![](images/4852b0b73148b9b8e212ece875ab2e517dedf9ba446a95aeb1adcf9169b351ef.jpg)



(c) $d_{0} = 520cm$   
Figure 3: Vibration signal acquired with different distances.

# 2.2 Problem Formulation

We leverage the periodic changes of backscatter signal to feature the target's vibration. Backscatter signal is composed of two metrics, amplitude and phase. We treat the phase resolved from the received backscatter signals as the vibration signal for two reasons. First, the amplitude of signal is notably distorted due to multipath effect and has a terrible resolution. Second, most COTS RFID products support milli-degree resolution and microsecond-level timing accuracy in the detecting the phase of the received backscatter signals $[43]$ , such that any mm-level and instant movement of tag can trigger a change on phase value. Thus, we frame our problem as follows:

PROBLEM 1. Given a sequence of measured phase values, $\{\tilde{\theta}[t_1], \tilde{\theta}[t_2], \cdots, \tilde{\theta}[t_N]\}$ , with the length of $N$ , how to find out the vibration period $T_v$ such that $\theta[t] = \theta[t + T_v]$ ?

The vibration period and fundamental frequency are denoted as $T_{v}$ and $f_{v}$ respectively. They are equivalent, i.e., $f_{v} = 1/T_{v}$ . The standard unit of frequency is Hz. However, mechanical engineers would love to represent vibration or rotation in the unit of RPM (Revolution Per Minute) where 1Hz = 60RPM. Following their practices, we sometimes also express the vibration in RPM. In addition, the reader is required to remain motionless for few seconds during the measurement to avoid the errors incurred by its movement like other vibration method (e.g., laser).

# 2.3 Solution Sketch

In this paper, we propose a holistic solution, Tagbeat, to address the vibration problem. Querying the RFID tag attached to the vibrating surface continuously, at a high level Tagbeat goes through the following three main steps:

- Magnifying micro-vibration: Tagbeat magnifies the tiny vibration signal induced from micro-vibration, using the technique in §3, if the amplitude of the vibration signal is less than a small threshold.   
- Recovering vibration signal: Tagbeat recovers the vibration signal using compressive reading with few samples, as described in §4.   
- Discovering vibration period: Finally, Tagbeat discovers the fundamental vibration period from the recovered signal (see §5).

The next few sections elaborate on the above steps, providing the technical details.

# 3. MAGNIFYING MICRO-VIBRATION

In most of the time, the displacements induced from routine vibration are within a few centimeters, making the changes of backscatter signal too small to be perceived. This section introduces a new type of digital ‘microscope’, a microscope for vibrations.

# 3.1 Vibration-induced Backscattering

Passive RFID system communicates using a backscatter radio link. The tag with no battery equipped, purely harvests energy from the reader's signal. The tag modulates its ID on the backscatter signal using ON-OFF keying [20].

Modeling vibration. To intuitively understand vibration, we show a basic geometric model in Fig. 2. The tag is attached on the position B and the vibration source is at position O. The distance r from vibration source to the tag is called as vibration radius. When vibrating with the surface, the tag follows a typical simple harmonic motion, which can be typified by the motion of a mass on a spring. Define $\delta(t)$ to be the displacement of the tag with respect to the reader, then displacement model can be given by:

$$
\delta (t) \approx \beta r (1 - \cos (2 \pi f _ {v} t)) \tag {1}
$$

where $f_{v}$ is the vibration frequency and $\beta$ is a constant coefficient. Notice, we treat the spinning (i.e., $\beta = 1$ ) as an extreme case of vibration, whose displacement is between 0 and $2r$ . Spinning is also an easily controllable modality of vibration so that we will test our solution most of the time using such vibration.

Phase of backscatter signal. The phase is a common parameter supported by COTS readers, which employ preamble correlation for acquiring and tracking carrier signal [22]. Let $d_0$ be the distance from equilibrium point $B$ to reader $R$ . Then the phase shift during vibration can be expressed as:

$$
\theta (t) = \left(\frac {2 (d _ {0} + \delta (t))}{\lambda} \times 2 \pi + c _ {0}\right) \bmod 2 \pi \tag {2}
$$

where $c_{0}$ denotes the constant phase shift introduced by the hardware [22, 43]. Notice the total distance is $2(d_{0} + \delta(t))$ because the signal traverses a double distance back and forth in backscatter communication. Substituting Eqn. 1 into Eqn. 2,

$$
\theta (t) \approx \phi_ {0} - \frac {4 \pi \beta r}{\lambda} \cos (2 \pi f _ {v} t) \mod 2 \pi \tag {3}
$$

where $\phi_0 = \frac{4\pi}{\lambda} (d_0 + \beta r) + c_0$ is the initial phase. From the equation, we see that the vibration signal is a cosine signal.

To visually figure out what the vibration-induced backscatter signal looks like, we show a sequence of phase in Fig. 3, which is acquired from a tag attached on a turntable with vibration frequency of $2.8\mathrm{Hz}$ (see §7 for details). In experiment, our empirical studies testify that a COTS reader has a mean read rate of 40 (i.e., with sampling frequency of $40\mathrm{Hz}$ ). Fig. 3(a) shows the phase sequence in the time domain when $d_0 = 560cm$ . We observe a close-to-perfect representation of the vibration signal agreeing with our model. It is a perfect cosine curve as we expected. Decreasing $d_0$ to $540cm$ , the sequence is segmented into upper and lower parts due to the function of mod, as shown in Fig. 3(b). If we continue to reduce $d_0$ , the lower sequence successively increases while the upper one decreases (see Fig. 3(c)). However, the one merged from these two parts is still as same as the one shown in Fig. 3(a).

![](images/f812e60925644c0cbf32edc94c20d483d9532f79d6985ef957723a0099ba0c73.jpg)



(a) Feasibility

![](images/20d3e7a536992887de91f4bac16027f6109aabe2300fd0412e9fa16aa980ccf6.jpg)



(b) Effectiveness   
Figure 4: Illustration of magnification. (a) shows the original tiny vibration signal and the amplified ones. (b) plots the virtually and physically amplified vibration signal.

# 3.2 Magnifying Tiny Vibration Signal

Tagbeat bootstraps its algorithm to deal with tiny vibration signal induced from the micro-vibration. We say a vibration signal is tiny when its amplitude follows within a small defined range (e.g., 0.3 radians). Recalling our purpose is to look for the vibration frequency and period, our magnification algorithm cannot change them.

Rational behind. Revisiting Fig. 2, the displacement highly depends on the vibration radius (i.e., the distance from source to tag). Intuitively, moving tag far away from the vibration source (i.e., increasing vibration radius) could make the tag move in a larger range and could increase displacements. This can be also explained using Eqn. 1, which implies that $\delta(t)$ is approximately proportion to the r. Therefore, our strategy is to increase the vibration radius from r to $\alpha r$ where $\alpha$ is called as amplification factor ( $\alpha > 1$ ).

Unfortunately, many practical constraints do not allow us to physically adjust the tag's position. We need to find a way to virtually extend the vibration radius. To facilitate our analysis, we remove the mod operation from the Eqn. 3:

$$
\theta (t) = \phi_ {0} - \frac {4 \pi \beta r}{\lambda} \cos (2 \pi f _ {v} t) \tag {4}
$$

The removal is reasonable because the tiny vibration cannot make phase value greater than $2\pi$ . Even when the initial phase (w.r.t. $\theta(t) = \phi_{0}$ ) is close to 0 or $2\pi$ , we could adjust the reader's position to obtain a continuous phase sequence. Following Taylor's theorem, we can expand Eqn. 4:

$$
\begin{array}{l} \theta (t) = \theta (0) + \frac {\theta^ {1} (t)}{1 !} t + \frac {\theta^ {(2)} (t)}{2 !} t ^ {2} + \dots \tag {5} \\ { = } { \theta ( 0 ) + \beta r \left( \frac { 8 \pi ^ { 2 } f _ { v } } { \lambda } \sin ( 2 \pi f _ { v } t ) + \frac { 1 6 \pi ^ { 3 } f _ { v } ^ { 2 } } { 2 ! \lambda } \cos ( 2 \pi f _ { v } t ) + \cdots \right) } \\ \end{array}
$$

where $\theta^{(n)}$ is the $n^{th}$ order derivative. The first term $\theta(0) = \phi_0 - \frac{4\pi\beta r}{\lambda}$ , which is the Direct Constant (DC) component. We do not care about DC component since it does not affect the periodicity. Let $B(t)$ be the reminder after filtering the DC component. Namely,

$$
B (t) = \beta r \left(\frac {8 \pi^ {2} f _ {v}}{\lambda} \sin (2 \pi f _ {v} t) + \frac {1 6 \pi^ {3} f _ {v} ^ {2}}{2 ! \lambda} \cos (2 \pi f _ {v} t) + \dots\right) \tag {6}
$$

The above equation implies that $B(t)$ is also proportional to $r$ , so amplifying $r$ by $\alpha$ is equivalent to amplifying $B(t)$ by $\alpha$ . Let $\widehat{B}(t)$ be the amplified non-DC component, which is given by:

$$
\begin{array}{l} \widehat {B} (t) = \alpha \beta r \left(\frac {8 \pi^ {2} f _ {v}}{\lambda} \sin (2 \pi f _ {v} t) + \frac {1 6 \pi^ {3} f _ {v} ^ {2}}{2 ! \lambda} \cos (2 \pi f _ {v} t) + \dots\right) \\ = \alpha B (t) \tag {7} \\ \end{array}
$$

Now, we put our thoughts together to show our methodology:

$$
\alpha \times \theta (t) \Rightarrow \alpha \times \delta (t) \Rightarrow \alpha \times r \Rightarrow \alpha \times B (t)
$$

Magnification methodology. We firstly filter out non-DC component $B(t)$ by a DC filter from original signal $\theta(t)$ as well as obtain the DC term $\theta(0) = \theta(t) - B(t)$ . Given an amplification factor $\alpha$ , the amplified signal $\hat{\theta}(t)$ can be calculated as follows:

$$
\begin{array}{l} \hat {\theta} (t) = \theta (0) + \widehat {B} (t) = \theta (t) - B (t) + \alpha B (t) \\ = \theta (t) + (\alpha - 1) B (t) \mod 2 \pi \tag {8} \\ \end{array}
$$

The amplified phase value may be beyond $[0, 2\pi]$ , so we add the operation of mod to wrap the amplified phase, enabling the result within a reasonable range.

Fig. 4(a) shows a tiny vibration signal, whose amplitude is within 0.8 radians. The tiny signal is amplified by $1.5 \times \sim 5.5 \times$ . It is easy to validate that the vibration period remains unchanged even the signal is magnified by $7.5 \times$ . This is understandable because Tagbeat never changes the harmonic frequencies in Eqn. 6. It is worth noting that there exists small sawtooth when zooming in the curve, due to the side-effect of magnification that noise is amplified too. We will discuss how to choose an appropriate $\alpha$ in §7. Further, we also conduct the second experiment in which we acquire vibration signals from $1cm-$ and $3cm$ -vibration (i.e., $r = 1cm, 3cm$ ). Meanwhile, we amplify the signal of $1cm$ -vibration by $3 \times$ . These three vibration signals are shown in Fig. 4(b). In theory, the radius of $3cm$ -vibration is $3 \times$ than that of $1cm$ -vibration, so $3cm$ -vibration-induced signal should be the same as $3 \times$ signal of $1cm$ -vibration-induced. From the figure, we see the two signals match each other well as expect.

# 4. RECOVERING VIBRATION SIGNAL

As will soon become clear, the samples fail to represent the original vibration signal due to frequency aliasing. We must recover the vibration signal before discovering its period. This section starts out with the sampling fundamentals and two important insights about RFID reading. Finally, we delve into the details of compressive reading for high-frequency vibration.

# 4.1 Sampling Fundamentals

The sampling is the process of converting a continuous domain signal into a set of discrete samples in a manner that allows to approximately represent or exactly reconstruct the original signal from the discrete samples. First of all, let's briefly review two different sampling techniques.

Nyquist sampling. The most fundamental principle on sampling is the Nyquist-Shannon sampling theorem, which states that when a continuous domain signal is band-limited to $[0, f_{\mathrm{max}}]$ , one can exactly recover the band-limited signal by just observing discrete samples of the signal at a sampling rate $f_s$ which is greater than $2f_{\mathrm{max}}$ . The spectrum of the sampled signal $s(t)$ is copied and shifted every $f_s$ in the Fourier domain. Since $f_s > 2f_{\mathrm{max}}$ , the copied versions are isolated well so that one version can be separated for reconstructing the signal. Otherwise, the copied versions are aliased, making the reconstruction erroneous.

![](images/e377368c738b54a60db54362095a4eedd22e944bf151ca1b0e1116f98eedc621.jpg)



(a) Sparse spectrum

![](images/64fcd18a39b1fc48873dc0d4b7d6a6ae926ceafe1f40a0eea8ea407c74f3f4d7.jpg)



(b) Random reading   
Figure 5: Two observations. (a) shows the spectrum of a periodic vibration signal. (b) shows the sequence of read time where each bar indicates the time when the tag is read.

Compressive Sampling. Intuitively, inadequate uniform sampling rate makes the instances of sampling in every cycle are identical, so these repeated instances are useless. Recent advances in the field of compressive sampling (or called compressive sensing) have developed reliable recovery algorithms for inferring sparse representations if one can randomly measure arbitrary linear combinations of the signal, then the signal could be reliably reconstructed through solving a $l_{1}$ optimization problem.

# 4.2 Two Observations

Nowadays, a modern COTS RFID reader has the ability of 40 readings per second on average, offering a sampling frequency of 40Hz. According to the Nyquist-Shannon sampling theorem, Tagbeat is able to monitor the vibration signal with a frequency of lower than 20Hz, which is apparently insufficient for most cases in daily life. Can we break the limitation of Nyquist-Shannon to inspect the high-frequency vibration? In order to explain the intuition behind our work, we firstly observe the following two facts:

OBSERVATION 1 (SPARSE SPECTRUM). A vibration signal is a periodic signal, which has a maximum of $2K + 1$ nonzero Fourier coefficients. Thus, it has a very sparse representation in the Fourier domain.

Vibration is a kind of simple harmonic motion thereby its signal is a periodic signal. We assume that the vibration keeps its fundamental frequency in a short time or only one fundamental frequency dominates its vibration each time. It is well known that any periodic signal with fundamental frequency $f_{v}$ can be expanded as a linear combination of phasors via the exponential Fourier series, namely,

$$
s (t) = \sum_ {k = - K} ^ {K} a _ {k} e ^ {\mathbf {J} 2 \pi (k f _ {v}) t}
$$

![](images/6f2d6b8c8fdea7b0bdb09a03d34ace3891200c0f3d9359bb0dcbe362c9c60008.jpg)



Figure 6: Illustration of compressive reading. It involves two components, signal model and measurement model.

where $k f_{v}$ is the $k^{th}$ harmonic frequency of the fundamental, $a_{k}$ represents the coefficient of the $k^{th}$ , and $K f_{v}$ corresponds to the maximum nonzero harmonic frequency. It can be seen that a periodic signal is composed of $2K + 1$ harmonic signals. Although the signal is not sparse at all in its time domain, it is more compact and sparse in Fourier domain. Fig. 5(a) illustrates a spectrum example of a vibration signal, which can be represented with 5 nonzero coefficients in the Fourier domain.

OBSERVATION 2 (RANDOM READING). COTS reader randomly read tag, offering an inherent random sampling.

COTS RFID readers adopt Q-adaptive anti-collision algorithm [2], which is a variant of ALOHA algorithm. Specifically, the reader divides the time into small slots and allows tag to randomly pick up a slot to backscatter its ID. Fig. 5(b) shows the 5-second reading trace captured in a COTS RFID system consisting of one ImpinJ reader [4] and one Alien tag [1]. We cannot find any specific pattern via visual inspection. We perform the Kolmogorov-Smirnov test (KS-test) to study their randomness. We find that the read time is verified to follow a uniform distribution with 0.5 significant level. Overall, we can believe the tag is read at a random time point, offering an inherent random sampling of the vibration signal. Such random sampling is able to ensure a set of sampling instances for any two cycles to be different. As long as sufficient samples are obtained, it is possible to recover the periodic signal.

# 4.3 Compressive Reading

Inspired by the previous two observations, Tagbeat attempts to recover the vibration signal using compressive sampling. We call this process compressive reading, which contains two key tasks: (1) projecting the time-domain vibration signal into Fourier domain for a compressible and sparse representation. (2) constructing the measurement matrix to schedule the sampling. A diagram of the compressive reading is shown in Fig. 6. The input is a sequence of two-tuples, $\{< t_1, \theta[t_1] >, < t_2, \theta[t_2], \ldots, < t_N, \theta[t_n] >\}$ , where $\theta[t_n]$ is the phase value read at time $t_n$ .

Modeling vibration signal. The compressive sampling requires the recovering signal to be very sparse. Observation 1 suggests that vibration signal has a very sparse representation in the Fourier domain. However, the phase sequence may be cut into several subsequences due to the operation of mod (see Fig. 3(c)). The discontinuous signal goes against the analysis in frequency domain. To remove the mod operation, we redefine our vibration signal by taking sin of $\theta(t)$ and denote it as $s[t]$ . Namely,

$$
s [ t ] = \sin (\theta [ t ]) \tag {9}
$$

Apparently, $s(t + T_v) = \sin(\theta(t + T_v)) = \sin(\theta(t)) = s(t)$ , so $s(t)$ has the same period as original phase sequence $^{1}$ . Based on discrete Fourier transform, we have

$$
S [ k ] = \sum_ {n = 1} ^ {N} s [ n ] e ^ {- \mathbf {J} \frac {2 \pi}{N} (k - 1) (n - 1)} = \sum_ {n = 1} ^ {N} s [ n ] W _ {N} ^ {(k - 1) (n - 1)} \tag {10}
$$

where $W_{N} = e^{-\frac{2\pi}{N}}$ and $n, k = 1, 2, \ldots, N$ . Correspondingly, the vibration signal can be transformed to Fourier representation with $\Psi$ as follows:

$$
S = \boldsymbol {\Psi} s \quad \text { or } \quad s = \boldsymbol {\Psi} ^ {- 1} S \tag {11}
$$

where $N \times N$ matrix $\Psi$ is the Fourier basis and S is the sparse coefficient vector in Fourier domain. As the right side of Fig. 6 shows, the vibration signal s can be represented in a sparse N-dimensional coefficient vector S.

Modeling measurement. The second task is to construct measurement matrix $\Phi$ . Existing CS systems create measurement matrix in advance and schedule the sampling based on the matrix. This fashion does not work in our scenario, because Tagbeat leverages COTS RFID system to sample the vibration. We can neither make any modification nor access low-level layer to schedule COTS reader. It is also impossible to command COTS tag to reply at a specific timing like proposed in [38]. The inherent random reading shown in Observation 2 reveals an opportunity for compressive sampling via its own inherent randomness. Harvesting this opportunity however requires more than simply aggregating the reading results. Unlike the past systems, Tagbeat constructs the measurement matrix and sampling results based on the existing readings afterwards instead of making them beforehand.

We discretize the total read time into N basic time slots, $\{t_{1}, t_{2}, \ldots, t_{N}\}$ , at millisecond level. Each reading (or sampling) only occurs within a time slot. The left side of Fig. 6 illustrates the structure of matrix $\Phi$ . The matrix contains $M \times N$ elements and each row corresponds to the timeline from $t_{1}$ to $t_{N}$ . We aggregate Q time slots into a read frame. Each row involves one read frame and the adjacent frames are staggered in two different rows. In this way, there are totally $M = \lceil N/Q \rceil$ frames and rows. Formally, the $m^{th}$ read frame starts at the $((m - 1)Q + 1)^{th}$ time slot and ends at the $(mQ)^{th}$ time slot in the $m^{th}$ row. The elements in the matrix are set to 0 (e.g., blank grid) or 1 (e.g., green grid). If $\Phi[m, n] = 1$ , it implies that the tag was read at the $n^{th}$ time slot and within the $m^{th}$ frame. Otherwise, $\Phi[m, n] = 0$ implies that the tag was not read in the $n^{th}$ time slot or the $n^{th}$ slot is beyond the $m^{th}$ frame. Let $N \times 1$ dimension vector y be the measurement result. The element $y[m]$ is the aggregated result of the $m^{th}$ frame, which is defined as follows:

$$
y [ m ] = \sum_ {n = 1} ^ {N} \Phi [ m, n ] s [ n ] \tag {12}
$$

Since $\Phi[m,n]$ is either 0 or 1, $y[m]$ is actually the sum of the values of the vibration signal sampled in the $m^{th}$ frame. Overall, the measurement model can be given by:

$$
y = \Phi s + \eta \tag {13}
$$

where $\eta$ represents the measurement noise. Notice that the second Tagbeat's difference from the past CS systems is that the measurement result $y$ is virtually aggregated based on the existing readings rather than physically produced by the media, allowing us to recover the signal without physical control of the reader.

Putting Things Together: Putting together the signal and measurement models, we have

$$
y = \boldsymbol {\Phi} s + \eta = \boldsymbol {\Phi} \boldsymbol {\Psi} ^ {- 1} S + \eta \tag {14}
$$

Recovery of the periodic vibration signal in Fourier representation amounts to solving the linear system of Eqn. 14. In the equation, $\Psi$ is the general Fourier basis and known in advance. $\Phi$ is the binary measurement matrix constructed with the read time. $y$ is the sampling vector calculated using the under-sampled results. The frame size $Q$ is a user-defined parameter.

Since we discretize the read time at ms-level, the minimum resolvable granularity Tagbeat can achieve is 1ms in theory. In other words, Tagbeat could inspect the vibrations with a maximum vibration frequency of 1KHz (or 60,000 RPM). We believe such high frequency is sufficient for major applications because our major goal is to inspect the mechanical vibrations in our daily life. For example, the fast medical centrifugal machine in hospital has a maximum RPM of 21,000. The engine of Tesla Model S could spin at 16,000 RPM at most. The voiced speech of a typical adult male has a fundamental frequency from 85 to 180Hz, and that of a female from 166 to 255Hz [35]. All of them are far less than our upper bound.

# 4.4 Reconstructing Vibration Signal

There are only K nonzero elements in S (i.e., S is K-sparse). The number of nonzero elements as well as their positions in S are unknown. A striking result in compressive sampling is that it is still possible to recover S with high probability by solving the following $l_{1}$ optimization problem:

$$
\widehat {S} = \arg \min _ {S} \| S \| _ {1} \quad \text { s.t. } y = \boldsymbol {\Phi} \boldsymbol {\Psi} ^ {- 1} S \tag {15}
$$

where $\| \cdot \|_{1(2)}$ is the $l_{1}$ - (or $l_{2}$ -) norm. However, the signals are always measured with noise (denoted by $\eta$ in Eqn. 14), the reconstruction would be achieved in practice by solving a relaxed $l_{1}$ -minimization problem:

$$
\widehat {S} = \min _ {S} \| S \| _ {1} \quad \text { s.t. } \left\{ \begin{array}{l} \| y - \Phi \Psi^ {- 1} S \| _ {2} <   \varepsilon \\ - 1 \leq S \leq 1 \end{array} \right. \tag {16}
$$

The $\varepsilon$ is a predefined error threshold. It has been shown that the above $l_{1}$ -minimization problem can be resolved with linear programming technique [21]. There is numerous on-going work looking for low-complexity reconstruction techniques in order to reduce the cost of computing when $N$ is too large. However, this topic is out of our scope. In addition, we add one more condition that the value of $S$ should be in $[-1, 1]$ , because we take sin of the phase.

Compressive sampling theory tells that a $K$ -sparse signal can be reconstructed from $M$ measurements if $M$ satisfies the following condition [18]: $M \geq b \cdot \mu^2(\Phi, \Psi) \cdot K \cdot \log N$ where $b$ is a positive constant, and $\mu(\Phi, \Psi)$ is the coherence between measurement matrix $\Phi$ and representation basis $\Psi$ . The coherence metric measures the largest correlation between any two element of $\Phi$ and $\Psi$ , is defined as: $\mu(\Phi, \Psi) = \sqrt{N} \cdot \max_{1 \leq i, j \leq N} |\langle \phi_i, \psi_j \rangle|$ . Based on the above equation, we can see that the smaller the coherence between $\Phi$ and $\Psi$ is, the less measurements are needed to reconstruct the signal. Thanks to the inherent randomness in RFID reading time, we can approximately consider that the measurement matrix is randomly generated. Thus, $\Phi$ is a random matrix. It has been shown that a random $\Phi$ is largely incoherent with any fixed representation basis $\Psi$ , and $M = 3K \sim 4K$ is usually sufficient.

![](images/f43b849b59f0866b89fca198a6fcc5945d00bc8172130bec112e4b155c5b95b2.jpg)



Figure 7: The reconstructed vibration signal. The signal can be sampled less than three times on average in each cycle (i.e., 8/3), but the recovered signal is almost as same as the original signal.

An example of vibration signal and its recovery using compressive reading is shown in Fig. 7. The fundamental frequency of the vibration signal equals 33Hz ( $T_{v} \approx 33ms$ ). In our experiment, we set N = 5,000, Q = 5, and K = 10. We see that the signal can be sampled less than three times on average in each cycle (i.e., 8/3), but the recovered signal is almost as same as the original signal.

# 4.5 Achieving Continuous Spectrum

The fundamental vibration frequency may be time-variant. Sometimes, the upper applications are interested in frequency distributions over time (e.g., troubleshooting auto engine). Tagbeat can achieve continuous spectrum by sliding a window function, which is nonzero for only a short period of time, over the original vibration signal. Mathematically, this is written as:

$$
\hat {s} [ n ] = \sum_ {n = 1} ^ {N} s [ n ] w [ n - w ] \tag {17}
$$

where $w[n]$ is the window function, commonly a Gaussian window centered around zero. For example, we monitor the spectrum of a turntable with dynamic vibration frequencies. In the experiment, we firstly start the device and immediately adjust its vibration from 0 RPM to maximum (2,000 RPM). We then slowly decrease the vibration to 1,000 RPM (16Hz), and finally change it back to 2,000 RPM again. Tagbeat uses the above approach to obtain its continuous spectrum, as shown in Fig. 8. From the figure, we can observe two apparent stages as we performed. The frequency quickly reaches to 33Hz and then swings between 16Hz and 33Hz, which fully fits our operations. This example shows Tagbeat is able to monitor time-varying vibration.

# 4.6 Discussion on Practicality

With respect to the practicality of compressive reading, some issues are worth noting:

\- Impact of diversity: The diversity (i.e., $c_0$ in Eqn. 3) stems from the varieties of hardware, imposing impact on the measured phase [22, 43, 44]. Fortunately, the diversity term keeps constant for a particular pair of reader and tag [44]. It only affects the initial phase $\phi_0$ instead of the periodicity of $\theta(t)$ , while compressive reading is independent on the initial phase. Thus, Tagbeat is immune to the hardware diversity.

\- Impact of thermal noise: It is well known that backscatter

![](images/f9f4f59e98e58f204cc583251031d7a94d259290412b50eb501269b6a94a5f44.jpg)



Figure 8: Achieving continuous spectrum. The continuous spectrum recovered from time-varying vibration.

signal measurement is affected by noise at the receiver side. We introduce $l_{2}$ norm to tolerant the noise as described in Eqn. 16. Thus, Tagbeat has the ability to combat with the thermal noise. After conducting many simulation tests, we find that Tagbeat fails to recovery the signal when the standard deviation of the phase value is beyond 0.7 radians. Our empirical experiments show that the actual standard deviation is usually less than 0.1 radians. Thus, Tagbeat is highly noise-tolerant.

\- Impact of multipath and Doppler effect: The signals propagating along different paths overlap together, making the received backscatter signal seriously distorted. Actually, compressive reading is independent on any specific communication model like described in Eqn. 3. Tagbeat can recover any distorted signal based on a simple assumption that the backscatter signal remains the same when it is emitted from the same position where the tag repeatedly arrives. In fact, the distortion of backscatter signal due to multipath effect (or Doppler effect) benefits to identifying its period, because it would be able to break the signal's symmetry (see §7 for more discussions). Similar to the multipath, Tagbeat is also independent on Doppler effect. Thus, Tagbeat is also immune to both multipath effect and Doppler effect.

# 5. DISCOVERING VIBRATION PERIOD

After recovering the vibration signal, Tagbeat needs to discover its vibration period. Since we have reconstructed the coefficient vector S in Fourier domain, the naive approach is to obtain the fundamental frequency by calculating the greatest common divisor of all the harmonic frequencies $\in S$ . As we will show in §7, such naive method however has a very bad accuracy (>100ms) because the result could easily fly away due to noisy frequencies.

Estimating the fundamental frequency has received a lot of attentions in speech processing [15, 28]. The popular one is to fast fold (or auto-correlate) the time-domain signal such that the folding inputting with correct period hypothesis spikes at the positions of the multiple of the fundamental period [27, 34, 46]. Fast folding is a general algorithm looking for the period of a signal. It can be applied to any periodic signal, but needs to wait for dozens of periods of samples to derive the correct period. For us, it is not fast enough to look for the period of vibration signal in real-time. Recalling that our vibration signal is the phase sequence, we can utilize the characteristic of radio signal to accelerate the folding. Suppose we have reversed the phase sequence (i.e., $\arcsin(s[t])$ ) from the recovered signal and denote it as $\{\theta[1], \theta[2], \ldots, \theta[N]\}$ , our folding is defined as follows. Given an assumed period of $T$ , the folding divides the phase sequence into $L$ sub-sequences, each of which has $T$ elements, where $L = \lfloor N/T \rfloor$ . They are denoted as $\{\Theta_1, \Theta_2, \ldots, \Theta_L\}$ . It further superimposes these $L$ sub-sequences in an element-wise fashion as follows:

![](images/4ef11e26bdae83f66e3e842fc6f2a70bfba957756bc188f847bc96c92cc6a776.jpg)



(a) Dashboard

![](images/9a0db305cd39c65a1e7db1a90d26cb51a6d143b53b36cf787c39ac60b3d7e0d7.jpg)



(b) Recovered signal   
Figure 9: Tagbeat user interface. The user can adjust parameters and view the recovered vibration signal in real-time through the user interface we have developed.

$$
F _ {T} [ t ] = \frac {1}{L} \sum_ {l = 1} ^ {L} w _ {l} [ t ] e ^ {\mathbf {J} (\Theta_ {l} [ t ] - \mu [ t ])} \tag {18}
$$

where

$$
\left\{ \begin{array}{l} \mu [ t ] = \frac {1}{L} \sum_ {l = 1} ^ {L} \Theta_ {l} [ t ] \\ \Delta \Theta_ {l} [ t ] = \mu [ t ] - \Theta_ {l} [ t ] \\ w _ {l} [ t ] = 2 \mathcal {F} (| \sin (\Delta \Theta_ {l} [ t ] |); 0, 0. 0 0 9) \end{array} \right.
$$

In particular, $|\cdot|$ and $\mathcal{F}(x;\mu,\sigma)$ denote the abstract operation and the cumulative probability function. Next, we progressively explain the above definition.

RF Folding. The RF folding's key difference from fast folding is the way of superimposition, i.e., the definition of $F_{T}[t]$ , whereby virtual interfered signals are constructed and superimposed. We use $e^{\mathbf{J}\Theta_l[t]}$ to denote the measured RF signal in complex representation with the measured phase and unit amplitude. Our basic idea is to interfere the measured RF signal with the theoretical one. If all measured signals conform with the theoretical signal, the interfered signals will reinforce each other. The key question is: how do we know the theoretical signal? Since our approach is independent on any specific geometric model, it is impossible to get theoretical signal by assuming tag's position like proposed in [43]. Fortunately, the law of large numbers states that the sample mean converges to the distribution expectation as the sample size increases. Thus, we use the mean of phase values to approximate their expectation, namely, $\mu [t] = \frac{1}{L}\sum_{l = 1}^{L}\Theta_l[t]$ , where $\mu [t]$ denotes the expectation of the $t^{th}$ phase value over $L$ sub-sequences.

Enhanced RF Folding. To enhance the superimposition at the correct period, we assign a weight $w_{l}[t]$ for each interfered signal. $w_{l}[t]$ equals cumulative probability of $(\Theta_{l}[t] - \mu[t])$ . However, we observe a phenomenon, called as singularity, that when the expected value is close to 0 or $2\pi$ , the instance may be far away from this expectation due to the function of mod, leading to their subtraction beyond the reasonable variance. For example, if $\mu[t] = 6.279$ and $\Theta_{m}[t] = 6.30 \mod 2\pi = 0.0168$ . Actually, the instance 6.30 follows within the variance (i.e., $\sigma = 0.1$ ), but their difference $\Delta\Theta_{m}[t] = 6.26 \gg \sigma$ is far beyond its variance. To deal with this issue, we take sine of the difference so that the mod could be removed. We know that phase value follows Gaussian distribution, i.e., $\Delta\Theta_{l}[t] \sim \mathcal{N}(0, 0.1)$ , so $\sin(\Delta\Theta_{l}[t]) \sim \mathcal{N}(0, 0.009)$ based on Lemma 1 (We omit the proof due to space limit.). Finally, if the folding happens to divide and align these sub-signals with the true period, the superimposing reinforces each other and make the average energy of final superimposed signal maximum. Namely, the correct periods must yield the maximum average energy of the superimposed signal.

LEMMA 1. If the random variable $\theta \sim \mathcal{N}(0,\sigma)$ , then $\sin (\theta)$ follows Gaussian distribution with $E(\sin (\theta)) = 0$ and $D(\sin (\theta)) = \frac{1}{2} (1 - e^{-2\sigma^2})$ .

![](images/2942b5f647a5d20db7ee0828140535a66d6c32d09d1a06e9834555dc716c559f.jpg)



Figure 10: Experimental setup. An RFID tag and an infrared-reflective marker are attached on a turntable which is remade from a middle-sized centrifuge machine. They are respectively monitored by RFID antenna and laser meter (for ground truth) installed on the top.

# 6. IMPLEMENTATION

We built a prototype of Tagbeat using ImpinJ Reader [4] and the Alien tags [1].

Hardware: We adopt an ImpinJ Speedway R420 reader (for China region, firmware version is 4.8.3.240.) without any hardware or software modification. The reader is compatible with EPC Gen2 standard. The whole RFID system operates in the 920 \~ 925 MHz band. The reader is connected to host through the wireless network (TCP/IP). It has local clock and attaches a timestamp for each tag read. We adopt the timestamp provided by the reader instead of the received time as the timing measurement to calculate the phase values, in order to eliminate the influence of network latency. One reader antenna with circular polarization manufactured by Yeon technology [12] is employed to provide ≥ 8dB gain in two directions. Four types of tags from Alien Corp [1], modeled Glint, 2 × 2, Square, and HiScan are employed.

Software: We adopt ImpinJ LLRP Tool Kit (LTK) [7] to communicate with the reader. ImpinJ reader extends this protocol for supporting the phase report. The client software is implemented using Java (for network connection) and Matlab (for signal processing). In our experiment, we run the software at a MacBook Pro, equipped with 2.8 GHz Intel Core i7 and 16 G memory. To better understand Tagbeat, we also develop a friendly user interface with the web frameworks of Bootstrap and AngularJS, as illustrated in Fig. 9.

Open source: All benchmark samples, source codes and runnable version of Tagbeat have been submitted to Github [9] for free download.

# 7. MICRO BENCHMARKS

We start with a few experiments that provide insight into the working of the system. Specifically, we inspect the spinning of a controllable turntable, as detailed below.

Experiment setup. Fig. 10 shows the main experimental setup where an RFID tag is attached on a turntable (i.e., remade from a commercial centrifugal machine). The frequency of the machine can be adjusted from 0 to 2,000 RPM. We evaluate the system in context of spinning because it is the most controllable modality of vibration, whose ground truth is easily accessible. The vibration radius equals 5cm and distance from vibration source to antenna equals 1.5m by default. In our experiment, we command the reader to continuously query the RFIDs using a fixed carrier frequency of

![](images/9707332939108f8f5f7f0241841cfd76b0bb61319043eb9a849d35cb264f8567.jpg)



Figure 11: Impact of sample length

![](images/645ed570ff46be7b3cec66598c9b79aa53d40b3f79cd89cbd9aab6861cbd4342.jpg)



Figure 12: Impact of multipath

![](images/14ebece04c11fa99504eece78d27aeed017fe66cfdd400566e42a51d2a1a466f.jpg)



Figure 13: Impact of RPM

![](images/e272666806212732b2dda5992542918b32a77472299fb8dddbd5943a9ce34bc3.jpg)



Figure 14: Impact of diversity

![](images/13e267ceacfb546786b3afe7caf808202f6a0fd81b5e28f39781e15b90526657.jpg)



Figure 15: Impact of radius

![](images/89e663a3862f080e8d142f40682a6c1e23f9460c70fb978a5bd98aaec816e97e.jpg)



Figure 16: Impact of distance

![](images/d05f9d63969d29fcff9f4701cbc9714a46d7954a8914ed0234fa6936415425ad.jpg)



Figure 17: Impact of tag number

![](images/3e7e1b88802a1a821b7d646f7b009efd43d1c64533dac6415d472c68bc0f958a.jpg)



Figure 18: Searching period

![](images/ae452178f5c5cd280cafe761b82619cd37aaaa1bc4872d4dd18c6d7f89992e23.jpg)



Figure 19: Magnification error

922 MHz $^{4}$ . We also set the reader at high-performance mode. The detailed reader and RO (reader operation) configuration files can be found at [10]. This setup is deployed in our office.

Ground truth: The laser radar can measure micro displacement very accurately, because tiny motion can alter the reflection angle. We use laser to collect the ground truth. As Fig. 10 shows, we install a hand-held laser meter on the top, meanwhile attach an infrared-reflective marker on the vibrating surface.

# 7.1 Recovering Vibration Signal

We are most interested in evaluating whether Tagbeat can exactly recover the high-frequency vibration through compressive reading with respect to the following factors:

Impact of parameters. There are two crucial parameters, N and Q, in compressive reading. These two parameters are defined in advance. The parameter N indicates how many (or how long) samples should be collected for one recovery. Setting Q = 5, we attempt to recover the same signal over N samples where N = 500, 1,000, 5,000 and 10,000. The recovered results are shown in Fig. 11. It can be seen that the recovered signal becomes smoother as N increases. This is because larger N brings more observations from the original signal, improving the quality of reconstruction. However, larger N also incurs much more delays and computations. There is a trade-off choosing N between real-time and accuracy. In practice, we suggest to set N = 3,000. The second parameter Q is the frame size specifying how many reads should be aggregated. We find that Q imposes very little impact on the recovery accuracy when it is less than the period of the signal. Our experience suggests to set Q to 5.

Impact of multipath effect. One of the RFID benefits over barcode is that it can identify objects without the need of line-of-sight (LOS) owing to the multipath effect. However, multipath is considered as harmful in many scenarios like tracking and symbol interference. We study the impact of multipath effect on Tagbeat. We conduct experiments in two scenarios. First, we deploy the turntable in a very clear environment without any multipath effect and set the RPM to 1,723 (with the period of 35ms). Second, we place five metal plates around the instrument to build a multipath-rich environment. Fig. 12 plots the vibration signal recovered in these two scenarios respectively. It can be seen that the vibration signal is seriously distorted in the multipath-rich environment compared with that in clear environment. Even so, it has the same period as that recovered without multipath. This implies compressive reading is independent on the multipath effect. Interestingly, it is much easier to identify the period of a distorted signal because the distortion due to multipath breaks its symmetry. The results also testify our assumption that the backscatter signal remains the same when it is emitted from the same position where the tag repeatedly arrives.

Impact of RPM. We randomly adjust the RPM of the turntable from 1,250 to 2,018 with 8 levels. For each level, we conduct 50 experiments to recover the vibration signal and search its period. Fig. 13 shows the errors in these 8 levels. Totally, the mean error is $0.3624ms$ over these 8 levels and the average relative error rate (i.e., the ratio of the error to the true period) equals $0.03\%$ . Such surprisingly high accuracy makes Tagbeat a competent equivalent of specialized sensors, like laser meter which has a relative error rate of $0.01\%$ . Even the worst case (at 1,738 RPM) only has a mean accuracy of $0.8490ms$ with a standard deviation of $0.98ms$ .

Impact of diversity. Keeping the turntable spinning at 1,510 RPM (i.e., period equals 39.7ms.), we repeat the evaluation over four kinds of RFID tags (Square, $2 \times 2$ , HiScan and Glint) to study the impact of tag's diversity. For each model, we repeat the experiments for 50 times and report the average. Fig. 14 plots the period errors over these four kinds of tags. Totally, the mean errors are all below 0.72ms. However, the deviations have a little difference. For example, the tag of $2 \times 2$ has a standard deviation of 0.01ms, while that of Glint is 0.61ms. We find that the deviation highly depends on the antenna size of tag. For example, the antenna size of $2 \times 2$ is $44mm \times 44mm$ while that of Glint is $27mm \times 9.7mm$ . Generally speaking, the tag with larger antenna absorbs more energy from reader so they behaves much more accurate and stable. Glint is the smallest model we have used.

Impact of vibrating radius. Fig. 15 plots the recovered vibration signals when the tag is attached with different vibrating radiuses but a same fundamental frequency. In the figure, a period of signal sequence is marked for the three signals. We can see that the period equals 50ms, 50ms and 51ms when the vibration radius is set to 2cm, 5cm and 10cm respectively. The detected periods are very close even the shapes of the vibration signals look very different, because the distortions of the signals depend on the tag's positions, i.e., radius. Thus, Tagbeat is irrelevant to the vibrating radius.

Impact of distance. Fig. 16 shows the accuracy with varying distances from 1m to 12m with the same setting. As we can see, Tagbeat does not exhibit strong correlation with the distance. However, the accuracy indeed decreases a little when the distance is over than 10m, which is the range limit of the current RFID reader. When the tag is far away from the reader, the read rate would decrease. As a result, the number of samples decreases and accuracy is affected.

Impact of tag number. Next, we investigate the relationship between the accuracy and the number of tags. We attached extra tags nearby our target tag. Fig. 17 shows the accuracy in five cases. The target tag was totally read for #1565, #1577, #1060, #1110 and #1040 times within 30s when there are 2, 5, 10, 15 and 20 extra tags around the target tag. The read rate of the target tag does not receive any apparent effect from other tags. This shows that the ImpinJ reader has very good performance on anti-collisions, because Q-adaptive protocol [2] dynamically adjusts the frame lengths in the end of every round reading. In theory, as long as the read rate remains unchanged, the accuracy should maintain at a same level. However, there is a slight trend showing that the error increases as more tags are involved. We think more tags may disturb the reading randomness for a specific tag, making harder recovery, although the total reading distribution over multiple tags is still random.

Impact of NLOS. We conduct 100 experiments in line-of-sight and another 100 experiments in non-line-of-sight, comparing using Tagbeat and Laser to make sense of vibration. In each experiment, we maintain the same parameters (i.e., $f_v = 1,666$ RPM). In LOS scenario, we keep the reader antenna (or laser meter) and tag (or reflective marker) all in direct line-of-sight of each other. Fig. 20(a) shows the CDF of the period error measured by laser and Tagbeat. The laser can achieve $100\%$ correctness, since there is no occlusion. Tagbeat has a median error of $0ms$ and less than $0.5ms$ for $90\%$ measurements. In NLOS scenario, we put up a $1m \times 2m$ solid wooden board between the reader antenna and tag, as well as between the laser and reflective marker. Fig. 20(b) shows the CDF of the period error. Laser cannot locate the marker and hence fails to provide an estimate of how frequently the marker moves. In contrast, RFID signal can penetrate obstacles and reach the RFID reader even when the tag is occluded. The median error remains unchanged, but 90th percentile of period error increases to $16.5ms$ because the obstacles still reduce SRN, decreasing the number of samples available.

![](images/4639488f88627b15083c6274a6ab9b52c0399f25bf576c29908c0ae187806311.jpg)



(a) LOS scenario

![](images/2ad0b6f6fa5090360a2671fc24a8a1d95731d7e1928b1be3e35eacd0683108f7.jpg)



(b) NLOS scenario   
Figure 20: Comparison between LOS and NLOS

# 7.2 Discovering Vibration Period

We then verify the accuracy of the period discovering algorithm. The frequency of turntable is adjusted to 187 RPM ( $T_{v} = 320.85ms$ ). We collect 120s trace of vibration signal. We then randomly select # periods of data from the trace and search their periods by using Fast Folding (FF), RF Folding (RF) and Enhanced RF Folding (EF) respectively. Each experiment with same parameters is repeated for 10 times and average results are reported.

Fig. 18 shows the period error as a function of number of periods. Each group of bars plots the errors when feeding with # periods of signals. For example, when inputting 3 periods of signal, FF, RF and EF can find out the period with an error of 62.32ms, 3.825ms and 1.56ms respectively. The errors of RF and EF reduce to below 1ms when feeding with more than 4 periods of signals, while FF has a period error of 1ms even giving 8 periods of data. It shows that RF and EF are faster and more accurate to look for the period than FF. This is mainly because FF is a general folding algorithm without caring the physical meaning of signal. It can converge into the correct period as long as sufficient input data are given. On contrary, RF and EF introduce radio model for the vibration signal (i.e., interference of signals), making the folding converge to correct period in a very short time. In particular, the error of EF reduces to 0.011ms when inputting 8 periods of data. Generally, Tagbeat could recover above 10 periods of signal. The standard variance of RF is larger than that of EF. This agrees with the previous analysis that the probabilistic weight produced by EF enhances the amplitude of signals close to their expectation.

For comparison, we also discover the fundamental period based on greatest common divisor (GCD) of harmonic frequencies. In experiment, with regard to energy, top $5 \sim 10$ harmonic frequencies excluding the constant are selected to calculate the fundamental period. As a result, we find the error is above 100ms no matter how many harmonic frequencies are chosen. This is because GCD-based method is fragile to interference and noise, even 0.1Hz error on harmonic frequency would lead to dozens times of error.

![](images/cc73eabf93742f7e9a46a8b03b21e235e298df8958aca0fefb7007a241f76f0d.jpg)



Figure 21: Measured wind field

# 7.3 Magnifying Vibration Signal

Finally, we investigate the effectiveness of magnification for microvibration. In the evaluation, we want to know whether magnification changes or affects the vibration period. We amplify a vibration signal with different magnification factors and then look for its period. Fig. 19 shows the period error as a function of magnification factor. It shows that the errors are within 1ms when the vibration signal is magnified under $25\times$ . However, its mean error and standard deviation increase to 4ms and 7ms when the factor is over than $30\times$ , due to amplified noises. Our test suggests to keep magnification factor below 25. This phenomenon can be explained as follows. As we aforementioned, Tagbeat fails to recover the vibration signal when the deviation of the noise is greater than 0.7 radians $^{3}$ . The magnification is a double-edged sword. It amplifies both signal and noise at the same time. However, as long as the amplified noise keeps lower than 0.7 radians (i.e., magnification factor is lower than $25\times$ ), the positive impact dominates signal and facilitates the recovery as well as discovery. On contrary, the negative impact prevents the recovery when the signal is over-amplified.

# 8. CASE STUDY

This section studies three cases to introduce how to associate the inspection solution provided by Tagbeat with the specific domain knowledge.

# 8.1 Case Study 1: Measuring Wind Speed

Wind is caused by differences in the air pressure. The speed of wind can be measured using a tool called as anemometer. An anemometer has three cups, each of which is mounted on a central axis, like spokes on a wheel, as shown in Fig. 1(a). When wind pushes into the cups, they rotate the axis, enabling sensor inside to transform the rotations to electrical signal. The traditional anemometer must be wired to a meter which supplies energy to the sensor and collects the signal. Thus, the anemometers must be deployed at the top of telegraph poles or equipped with a solar battery. This confines us to freely measure the wind speed, especially in the wild. Tagbeat provides a potential way to freely measure wind speed using backscatter nodes, which may be powered by a TV tower or a mobile station $[26, 30]$ , breaking deployment limitation.

![](images/ddef7604c8b1d8a721858ba9fa276b13f17e9fd967b7edad12e0268ab0374103.jpg)



Figure 22: Recovered vibration signal of one test tube

To study the feasibility of using backscatter signals to measure wind speed, we deploy an industrial-sized fan to emulate the winds in our office as shown in Fig. 1(a). Meanwhile, we attach a Square tag on one cup of the anemometer. The wind speed is measured by using anemometer (for ground truth) and Tagbeat concurrently. The wind speed is expressed in the unit of m/s, so we calculate the speed with the formula of $2r\beta/T_{v}$ (i.e., perimeter to period). $\beta$ is constant coefficient and can be calibrated in practice. r is the vibration radius and $T_{v}$ is the inspected period. We use the prototype to measure the wind in 40 different positions. The wind field is plotted in Fig. 21. In the figure, we add a small angle to separate the ground truth and our results for comparison. Notice the wind directions are simulated in theory. We also sketch the contour of the wind based on our measurement. As a result, Tagbeat has a mean speed error of 0.6181m/s with a standard deviation of 0.33m/s. This case study fully shows the feasibility of using Tagbeat to measure the wind speed.

# 8.2 Case Study 2: Monitoring Centrifugation

Centrifugation is a process which leverages centripetal force to separate various heterogeneous mixtures by using centrifuge. This equipment is the most frequently used device in hospital. It can separate whole blood into its various components, such as red blood cells, white blood cells, plasma, etc. Our partner, Hospital X, needs to centrifuge thousands of blood samples every day. It is a burden-some task to manage so many bloods. Many patients were asked for re-test due to over centrifugation. Fig. 1(b) shows a real high-speed centrifuge used in clinical laboratories. It supports 6,000 RPM (i.e., 10ms period) of centrifugation. We attach Glint tags on 8 test tubes and let Tagbeat automatically associate the tubes with their centrifugations. We use the machine to perform 2-minute centrifugation on these 8 tubes. We randomly pick up 600-ms recovered vibration signal and show it in Fig. 22. It can be seen that majority of samples match the recovery well even for so high-frequency vibration. In this case, we care about how much time are taken on centrifugation for each tube. Tagbeat can exactly track the vibration time. We find that the time error has a mean of 1.6s (i.e., about 16 periods) with a standard deviation of 1.8s, implying that Tagbeat can accurately track the centrifugation of each tube.

# 8.3 Case Study 3: Troubleshooting Engine

If the vehicle shakes violently or the engine vibrates excessively when parked with the engine on, this may be an indicator of engine breakdown. A common way of troubleshooting engine is to inspect the vibration of the engine by a specialized equipment at a qualified repair shop or professional mechanic. Attaching a Square tag on the cover of the engine of our car, we put the car in neutral and utilize Tagbeat to inspect its vibration. During the testing, we dynamically increase the RPM from 1,000 to 4,000. We troubleshoot engine by determining how well the inspected continuous spectrum fits the records shown in the dashboard. We find that the car is in excellent condition if the matching accuracy is above 85%. Otherwise, there may be a problem about the engine.

# 9. REMARKS & LIMITATIONS

Measurement of vibration based purely on backscatter signal is a challenging technical problem. We believe Tagbeat has taken an important step toward addressing this issue. However, a few points are still worth discussing:

Reader cost. Our initial assumption is that the reader (e.g., ImpinJ R420) has been deployed in warehouse or chemical laboratory for asset management. Tagbeat just supplements an extra functionality apart from identification, rather than serves as a dedicated vibration meter. Since ImpinJ R420 is a universal RFID reader and originally designed for logistics and supply chain management, it has relatively higher price. With regard to cost, the mobile readers (e.g., ImpinJ TSL [5] and ATID [3]) are more suitable for serving as dedicated vibration meters.

Sensing range. Tagbeat inherits the shortcoming that its sensing range is limited within dozens of meters, from the RFID technology. Such relatively short range is apparently insufficient for wind measurement in the wild, but Tagbeat provides a potential way for this purpose when integrating with ambient communication technology $[26, 30]$ .

Tolerant to ambient interference. Tagbeat has stronger anti-interference ability for four reasons. (1) Bit level: The reader usually calculates the phase value over 96-bits of the ID and reports the average value [22]. The impact from sudden signal interferences are smoothed. (2) Packet level: According to EPCglobal air protocol [2], collided packets from different tags will be discarded, ensuring the packet interferences are not propagated to Tagbeat. (3) Channel level: There are dozens of frequency hopping channels available. We can view the reading over different channel as independent observations and fuse the inspecting results, to avoid the enduringly inferences at one specific signal channel. (4) Signal processing level: The $l_2$ -minimization could relax the inaccurate measurement when recovering the vibration signal.

Our simulation suggests that Tagbeat could accurately recover the signal if the standard deviation of the phase value is within 0.7 radians. Our empirical experiments also show that the value is usually less than 0.3 radians for a mobile tag in practice. Totally, many inherent characteristics of backscatter communication make Tagbeat highly noise-tolerant.

Channel hopping. The UHF reader for USA region hops between 50 channels in the 902MHz \~ 928MHz ISM band. FCC regulations specify that a reader can have a maximum channel dwell time of 0.4 seconds in any ten second period to reduce interference in a channel [17]. The hopping breaks our assumption that the signal remains same when passing by the same position. To tackle with this issue, we could separate the phase sequences over different channels and separately recover the vibration signals. The simple method is to average these independent results.

Energy consumption. A usual accelerometer based system is wiredly connected to processing unit. Wired system is obviously more energy-saving than any corresponding wireless system. However, the benefits of Tagbeat are also apparent. For example, it could be applicable to occluded and non-line-of-slight objects, e.g., inspecting chemical tubes in a centrifuge machine. Moreover, the RFID tag contains the object ID, enabling the system to automatically associate the vibration with the particular vibration object. So we believe it is worth sacrificing a little more energy for free and easy deployment.

# 10. RELATED WORK

In this section, we briefly review the related literature in vibration measurement.

Measurement with accelerometers. Accelerometers are small devices that are installed directly on the surface of (or within) the vibration object $[6, 8]$ . They contain a small mass which is suspended by flexible parts that operate like springs. Vibrations at higher frequencies have greater accelerations than those at lower frequencies. For this reason, accelerometers are extremely insensible to low frequency vibration. The recent advances made in sensing platform (such WISP $[11]$ , CRFID $[13, 16]$ , EkhoNet $[45]$ , etc) could integrate with the accelerometer component, offering potential solutions for wireless vibration measurement. These platforms also require RFID reader for energy supply, and are usually hundreds of more expensive than an RFID tag. Thus, Tagbeat is a relatively cheap solution compared with accelerometer based methods.

Measurement with displacement sensors. Displacement sensors $[6]$ , like laser, capacitive and eddy-current sensors, are the best choice for high-resolution and high-speed measurements, because they could enable sensing even micron displacement very accurately $[19]$ . $[29]$ demonstrated real-time nanometer-vibration measurements by using a DPSSL (Laser-diode-pumped microchip solid-state lasers) and the self-mixing modulation technique. Compared with laser, the advantage of Tagbeat is the ability to sense vibration through opaque obstacles.

Measurement with high-speed camera. Capturing high-speed events, e.g., vibrations, requires fast and high-frame-rate cameras with high photoresponsivity at short integration times. Veeraraghavan [36] leveraged the compressive sensing to turn an off-the-shelf video camera into a powerful high-speed video camera for observing periodic events. Seitz and Dyer [33] introduced a general framework for image-based analysis of repeating motions. Jia [23] repaired videos with large static background or cyclic motion. Laptev et al. [24] detected and segmented periodic motion based on sequence alignment without the need for camera tracking.

Measurement with wireless vibrometry. ART [42] exploited a new way of eavesdropping loudspeaker sounds through wireless vibrometry. Unfortunately, ART requires an extremely quiet environment. Any ambient or neighboring vibrations would introduce noises, leading to relatively large errors. On contrary, Tagbeat attaches different tags on different vibration objects so it well isolated the interferences from neighboring vibrations.

# 11. CONCLUSION

In this work we present Tagbeat for real-time tracking of vibration using COTS RFID tags and readers. A key innovation is to make sense of the vibration through the changes of tag's backscatter signals. Tagbeat can sense the vibration period to an accuracy of sub-millisecond, providing the necessary precision for many novel applications, such as high-speed centrifugation. The system not only has been tested and used in practical applications, but also will open up a wide range of exciting opportunities.

# 12. ACKNOWLEDGMENTS

The research of Yang is supported by NSF China General Program (NO. 61572282) and China Postdoctoral Science Foundation funded project under NO. 2015M570100. The research of Liu is supported by NSF China Major Program 61190110. The research of Li is partially supported by NSF ECCS-1247944, NSF CMMI 1436786, NSF CNS 1526638, National Natural Science Foundation of China under Grant No. 61520106007. We thank all the reviewers and shepherds for their valuable comments and helpful suggestions.

# 13. REFERENCES

[1] Alien. http://www.alientechnology.com.   
[2] EPC Gen2, EPCglobal. www.gs1.org/epcglobal.   
[3] ImpinJ ATID AB700 Handheld Reader. http://www.impinj.com/products/readers/atid-ab700-handheld/.   
[4] Impinj, Inc. http://www.impinj.com/.   
[5] ImpinJ TSL 1128 Handheld Reader.
http://www.impinj.com/products/readers/tsl-1128-handheld/.   
[6] Lion Precision. http://www.lionprecision.com/.   
[7] LTK SDK. https://support.impinj.com.   
[8] Measurement Specialties.
http://www.meas-spec.com/vibration-sensors.aspx.   
[9] Tagbeat. https://github.com/tagsys/tagbeat.   
[10] TagSee. https://github.com/tags/s/tagsee.   
[11] WISP. https://wisp.wikispaces.com/.   
[12] Yeon Antenna. http://www.yeon.com.tw/content/product.php?act=detail&c\_id=43.   
[13] BLINK: A High Throughput Link Layer for Backscatter Communication. pages 1–14, 2012.   
[14] O. Abari, D. Vasisht, D. Katabi, and A. Chandrakasan. Caraoke: An e-toll transponder network for smart cities. In Proc. of ACM SIGCOMM, pages 297–310, 2015.   
[15] J. C. Brown. Musical fundamental frequency tracking using a pattern recognition method. The Journal of the Acoustical Society of America, 92(3):1394–1402, 1992.   
[16] M. Buettner, B. Greenstein, and D. Wetherall. Dewdrop: an energy-aware runtime for computational RFID. In Proc. of USENIX NSDI, 2011.   
[17] M. Buettner and D. Wetherall. An empirical study of UHF RFID performance. In Proc. of ACM MobiCom, page 223, 2008.   
[18] E. J. Candès, J. Romberg, and T. Tao. Robust uncertainty principles: Exact signal reconstruction from highly incomplete frequency information. Information Theory, IEEE Transactions on, 52(2):489–509, 2006.   
[19] P. Castellini, M. Martarelli, and E. P. Tomasini. Laser doppler vibrometry: Development of advanced solutions answering to technology's needs. Mechanical Systems and Signal Processing, 20(6):1265–1285, 2006.   
[20] D. M. Dobkin. The RF in RFID: UHF RFID in Practice. Newnes, 2012.   
[21] D. L. Donoho. Compressed sensing. IEEE Transactions on Information Theory, 52(4):1289–1306, 2006.   
[22] EPCglobal. Low level reader protocol (llrp). 2010.   
[23] J. Jia, Y.-W. Tai, T.-P. Wu, and C.-K. Tang. Video repairing under variable illumination using cyclic motions. IEEE Transactions on Pattern Analysis and Machine Intelligence, 28(5):832–839, 2006.   
[24] I. Laptev, S. J. Belongie, P. Perez, and J. Wills. Periodic motion detection and segmentation via approximate sequence alignment. In Proc. of IEEE ICCV, 2005.   
[25] Y. Lei, Z. He, and Y. Zi. Application of an intelligent classification method to mechanical fault diagnosis. Expert Systems with Applications, 36(6):9941–9948, 2009.   
[26] V. Liu, A. Parks, V. Talla, S. Gollakota, D. Wetherall, and J. R. Smith. Ambient backscatter: wireless communication out of thin air. In Proc. of ACM SIGCOMM, 2013.   
[27] E. Lovelace, J. Sutton, and E. Salpeter. Digital search methods for pulsars. Nature, 222:231–233, 1969.   
[28] R. C. Maher and J. W. Beauchamp. Fundamental frequency

estimation of musical signals using a two-way mismatch procedure. The Journal of the Acoustical Society of America, 95(4):2254–2263, 1994.   
[29] K. Otsuka, K. Abe, J.-Y. Ko, and T.-S. Lim. Real-time nanometer-vibration measurement with a self-mixing microchip solid-state laser. Optics letters, 27(15):1339–1341, 2002.   
[30] A. N. Parks, A. Liu, S. Gollakota, and J. R. Smith. Turbocharging ambient backscatter communication. In Proc. of ACM SIGCOMM, 2014.   
[31] N. Roy and R. R. Choudhury. Ripple ii: Faster communication through physical vibration. In Proc. of USENIX NSDI, 2016.   
[32] N. Roy, M. Gowda, and R. R. Choudhury. Ripple: Communicating through physical vibration. In Proc. of USENIX NSDI, 2015.   
[33] S. M. Seitz and C. R. Dyer. View-invariant analysis of cyclic motion. International Journal of Computer Vision, 25(3):231–251, 1997.   
[34] D. H. Staelin. Fast folding algorithm for detection of periodic pulse trains. In IEEE Proceedings, volume 57, pages 724–725, 1969.   
[35] I. R. Titze and D. W. Martin. Principles of voice production. The Journal of the Acoustical Society of America, 104(3):1148–1148, 1998.   
[36] A. Veeraraghavan, D. Reddy, and R. Raskar. Coded strobing photography: Compressive sensing of high speed periodic videos. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2011.   
[37] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus. Rf-compass: robot object manipulation using rfids. In Proc. of ACM MobiCom, 2013.   
[38] J. Wang, H. Hassanieh, D. Katabi, and P. Indyk. Efficient and reliable low-power backscatter networks. In Proc. of ACM SIGCOMM, pages 61–72. ACM, 2012.   
[39] J. Wang and D. Katabi. Dude, where's my card?: Rfid positioning that works with multipath and non-line of sight. In Proc. of ACM SIGCOMM, 2013.   
[40] J. Wang, D. Vasisht, and D. Katabi. Rf-idraw: virtual touch screen in the air using rf signals. In Proc. of ACM SIGCOMM, 2014.   
[41] W. Weaver Jr, S. Timoshenko, and D. Young. Vibration problems in engineering.   
[42] T. Wei, S. Wang, A. Zhou, and X. Zhang. Acoustic eavesdropping through wireless vibrometry. In in Proc. of ACM MobiCom, pages 130–141, 2015.   
[43] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: real-time tracking of mobile rfid tags to high precision using cots devices. In Proc. of ACM MobiCom, 2014.   
[44] L. Yang, P. Peng, F. Dang, C. Wang, X.-Y. Li, and Y. Liu. Anti-counterfeiting via federated rfid tags' fingerprints and geometric relationships. In Proc. of IEEE INFOCOM, 2015.   
[45] P. Zhang, P. Hu, V. Pasikanti, and D. Ganesan. EkhoNet: high speed ultra low-power backscatter for next generation sensors. In Proc. of ACM MobiCom, 2014.   
[46] R. Zhou, Y. Xiong, G. Xing, L. Sun, and J. Ma. Zifi: wireless lan discovery via zigbee interference signatures. In Proc. of ACM MobiCom, 2010.