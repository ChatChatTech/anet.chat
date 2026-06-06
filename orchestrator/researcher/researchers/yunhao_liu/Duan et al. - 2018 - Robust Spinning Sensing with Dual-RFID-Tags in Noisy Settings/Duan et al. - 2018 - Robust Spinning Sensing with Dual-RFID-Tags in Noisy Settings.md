# Robust Spinning Sensing with Dual-RFID-Tags in Noisy Settings

Chunhui Duan⇤, Lei Yang†, Huanyu Jia⇤, Qiongzheng Lin†, Yunhao Liu⇤ and Lei Xie‡

⇤School of Software and TNLIST, Tsinghua University, China

†Department of Computing, The Hong Kong Polytechnic University, Hong Kong

‡Department of Computer Science and Technology, Nanjing University, China

Email: {hui, young, jia, lin}@tagsys.org, yunhao@greenorbs.com, lxie@nju.edu.cn

Abstract—Conventional spinning inspection systems, equipped with separated sensors (e.g., accelerometer, laser, etc.) and communication modules, are either very expensive and/or suffering from occlusion and narrow field of view. The recently proposed RFID-based sensing solution draws much attention due to its intriguing features, such as being cost-effective, applicable to occluded objects and auto-identification, etc. However, this solution only works in quiet settings where the reader and spinning object remain absolutely stationary, as their shaking would ruin the periodicity and sparsity of the spinning signal, making it impossible to be recovered. This work introduces Tagtwins, a robust spinning sensing system that can work in noisy settings. It addresses the challenge by attaching dual RFID tags on the spinning surface and developing a new formulation of spinning signal that is shaking-resilient, even if the shaking involves unknown trajectories. Our main contribution lies in two newly developed techniques, relative spinning signal and dual compressive reading. We analytically demonstrate that our solution can work in various settings. We have implemented Tagtwins with COTS RFID devices and evaluated it extensively. Experimental results show that Tagtwins can inspect the rotation frequency with high accuracy and robustness.

Index Terms—RFID, spinning sensing, robust, dual-tag.

# I. INTRODUCTION

Spinning is a mechanical phenomenon which dominates our industrial lives everyday, such as conveyors, motors, robotics, and so on. In many cases, spinning is undesirable and must be observed accurately, especially in smart factory. For example, rotating machineries nowadays are widely employed in industrial equipment. The unexpected downtime due to their undesirable vibrations has become more costly than ever before [1]. In particular, utilizing spinning frequency for equipment diagnosis is a common method.

There are numerous traditional methods to inspect rotation. However, all of these methods are based on conventional motion sensors, such as acceleration, infrared sensors or cameras. Unfortunately, most of them are bulky, heavy, intrusive, and energy-consuming. For example, accelerometers require wiredly connecting to a control panel for power supply and signal transmission. Even integrated with WSN, they still need extra and cumbersome batteries and transceivers, making it impossible to sense the rotation of small objects with high spinning speed. Infrared sensors are common choices for high-resolution and high-speed measurements, but fail in the absence of a line-of-sight to the objects. High-speed cameras may be another option, but are seldom adopted in industry due to their high cost.

![](images/d294d968fbda1e9a2af2dec01c99243bcf1fbddaa7d69b65d03c8c2bc02cd69d.jpg)



(a) Quiet setting

![](images/7bc580e6b8fdfb0cff3fdee36a70b3ca3779b00efa0ce8b7c57e8d3c90982d24.jpg)



(b) Noisy setting   
Fig. 1: Frequency distributions of the spinning signal collected in quiet or noisy settings. (a) The spectrum is composed of several primary harmonic frequencies and thereby the signal is very sparse in frequency domain as described in [2]. (b) The spectrum is out of order and not sparse any more due to the noise from surroundings.

To address the above issues, [2] proposes a novel measurement approach (i.e. Tagbeat), which supplements the RFID communication functionality with fine-grained spinning (or vibration) sensing ability. Specifically, a slight and battery-free RFID tag is attached on the spinning object (i.e. turntable). The spinning displaces the tag within a small range, resulting in a regular change pattern of backscatter signal. Then we can reveal the spinning information by discerning such communication pattern without specialized sensors. Compared against traditional means, Tagbeat offers an appealing alternative, with the advantage of being cost-effective, applicable to occluded objects, and auto-associative with the spinning object (by the tag’s ID). Moreover, since battery-free tags are powered and driven by wireless signals, no additional energy suppliers or RF transceivers are required, making them small and light enough to be attached on tiny objects.

In spite of high availability and promising foreground, Tagbeat requires a quite rigorous assumption that the devices and the deployment surroundings must remain quiet, i.e. motionless and stationary. This assumption must hold in practice because any irregular and unexpected jitters of the tag’s backscatter signal incurred by the shaking of the reader, the turntable, or the changes of surroundings, would disturb the periodicity of spinning signal and further violate its sparsity in frequency domain. Fig. 1 compares the spectrums of two spinning signals collected in quiet and noisy settings respectively. Clearly, Tagbeat, which is driven by the technique of compressive sensing, fails to recover the non-sparse signal because there are too many linear combinations. Many real scenarios are against such assumption. For instance, industrial operations can happen in unstable platforms (e.g. vehicles and ships), whose shaking would lead to dramatic translations of readers and tags. It is also hard to let a worker stably hold a handheld reader for a long time measurement. Our empirical study suggests that even a 5cm noisy translation of the device would make the spinning signal unrecoverable.

![](images/587d4ab60fcaa1eb2f92b21fde41832624a154507535a3f62edef8c1600a10f5.jpg)



Fig. 2: Spinning sensing with dual-tags

Motivated by the above limitation, we present Tagtwins, a robust spinning sensing system that can work in noisy settings. Here noise means unpredictable shaking or translation of devices (readers and/or spinning objects). Tagtwins addresses the challenge by attaching dual RFID tags on the spinning surface, as shown in Fig. 2, and develops a new formulation of spinning signal that is shaking-resilient. We allow both the turntable and reader to be randomly and simultaneously shaken when monitoring the spinning. Even if the shaking involves unknown trajectories, we can accurately recover its spinning signal. To this end, we exploit the observation that the distance between two tags is fixed independent of how the turntable or the reader shakes. Leveraging this, we develop the relative spinning signal which is derived from the relative wireless channels of two tags, to depict the spinning that occurs in noisy settings, without knowing any information on the absolute position or translation of the devices.

To quickly grasp our basic idea, we give a simplified explanation why our relative spinning signal can work. As shown in Fig. 2, the phase values of signals backscattered from tag $T _ { 1 }$ and $T _ { 2 }$ are respectively given by

$$
\theta_ {1} (t) \approx \frac {4 \pi}{\lambda} \left(d - r _ {1} \cos \left(2 \pi f _ {s} t + \phi_ {1}\right)\right) \bmod 2 \pi \tag {1}
$$

$$
\theta_ {2} (t) \approx \frac {4 \pi}{\lambda} \left(d - r _ {2} \cos (2 \pi f _ {s} t + \phi_ {2})\right) \bmod 2 \pi
$$

where λ is the wavelength, d is the distance between the reader and turntable center, $f _ { s }$ is the spinning frequency, $r _ { 1 } , \ r _ { 2 }$ are distances of two tags to the turntable center, and $\phi _ { 1 }$ , φ2 are the initial angles of two tags. The detailed geometric model is presented in Sec. III. Assuming $\phi _ { 1 } = \phi _ { 2 } = 0$ , we can obtain the relative phase by subtracting the above two equations:

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} (r _ {2} - r _ {1}) \cos (2 \pi f _ {s} t) \bmod 2 \pi \tag {2}
$$

Clearly, the distance d is perfectly eliminated from the formula. This means that no mater how the reader or the turntable moves, the relative phase is only dependent on $f _ { s }$ . Meanwhile, $\Delta \theta ( t )$ also maintains the same frequency as the original.

One might consider using the above relative phase as the spinning signal. Unfortunately, performing it in practice encounters numerous challenges. First, the measured phase values are discontinuous due to the operation of mod. Worsely, the phase may randomly jump ⇡ radians because of the halfwave loss phenomenon [3]. Second, $\phi _ { 1 } = \phi _ { 2 } = 0$ happens only when two tags are attached on a straight line which passes through the turntable center. Apparently, we do not expect to attach tags under some scheduled rules, thus, the two formulas cannot be simply merged together like this. Third, all COTS tags are randomly and exclusively read in a timesharing fashion to avoid signal collisions. It is impossible to simultaneously acquire the two tags’ phase values at a same time point for the calculation of relative phase. To address these challenges, we firstly develop Relative Spinning Signal (RSS). We analytically demonstrate that RSS is resilient to surrounding noise even in the presence of multipath effect. Importantly, the underlying sparsity assumption that compressive reading [2] is built on still holds true. We then design and implement Dual Compressive Reading (DCR) to recover RSS using COTS RFID devices, with no extra infrastructure or pre-calibration efforts.

Contributions: Tagtwins enhances the RFID-enabled system that makes sense of mechanical rotation within sub-hertz accuracy using dual tags’ backscatter signals. It addresses a practical problem of how to robustly sense spinning in noisy settings. Second, we develop RSS to depict the shakeresilient sensing, and DCR to inspect high-frequency spinning. Third, we implement and evaluate our prototype with extensive experiments, demonstrating the practicality and effectiveness of our design.

# II. OVERVIEW

Tagtwins is an RFID-based solution for inspecting mechanical spinning frequency of any objects. Although we present the system in the context of spinning in most of the time, Tagtwins’ technique could be applied to any other modalities of periodic mechanical motion (like vibration or pendulum). Specifically, it decomposes the sensing problem into the following two cases:

Sensing with a single tag. We firstly consider a simplified case where a single tag is used to sense the spinning in quiet settings in Sec. III. Correspondingly, we develop the refined spinning signal with the RF phase values to address the discontinuity caused by either the modulus operation or the half-wave loss.

Sensing with dual tags. We then consider a general case where dual tags are used to defend against signal noises introduced by the devices or the surroundings in Sec. IV. Correspondingly, we develop the relative spinning signal to enhance the system robustness.

The next few sections elaborate on the above steps, providing the technical details.

# III. SENSING WITH A SINGLE TAG

In this section, we introduce RFID-based spinning sensing with a single tag as well as its limitations.

![](images/61fe4eea46c2cc67ab500038ff69e2a84fdc06166ab34fa100e1d3a2f10aed7d.jpg)



(a) Original phase sequence

![](images/d2c0d65f99e72f5e3ae01519fff2c1d7bc7a2ba311e75bd2196761331e903bbc.jpg)



(b) Refined spinning signal

![](images/ba735f8fb8b9ae830f866e8d6a3a6388e73cbd66cdb8b9c4103246cd2c45c53e.jpg)



(c) Distorted spinning signal

Fig. 3: Spinning signals induced by a spinning tag. (a) Original phase sequence ✓(t), which is split into many short discontinuous fragments due to the operation of mod and half-wave loss. (b) The refined spinning signal $s ( t )$ , which is continuous, smooth and periodic as the original one. (c) The Distorted spinning signal caused by the shaking of reader.   
![](images/c065763bbc4950b9bff31265b395370b9018bfd1a80fdce41e589ee65a5fb8fc.jpg)



Fig. 4: Geometric model for spinning. The clockwise rotating turntable displaces the attached tag T along a circle, leading to a varying phase shift.

# A. Modeling Spinning Signal

The concept underlying spinning sensing is to develop a spinning signal which has a fundamental period or frequency as same as the spinning itself, such that we can inspect the states of the spinning through this signal. Using RFID tag (which is attached on a turntable) for spinning sensing considers all discrete, random and low-frequency readings of the tag as samplings of the spinning states. The goal is to develop a continuous spinning signal through these readings.

The RF phase is a common parameter supported by commercial RFID readers [4]. Suppose a tag T is attached on the turntable. Let $d = | R O |$ and $r = | T O |$ as sketched in Fig. 4. Then the phase shift during the spinning is defined as [3]:

$$
\theta (t) = \frac {4 \pi}{\lambda} (d - \delta (t)) + \theta_ {\mathrm{div}} \bmod 2 \pi \tag {3}
$$

where the term $\theta _ { \mathrm { d i v } }$ (called as diversity term) denotes the constant phase shift introduced by the device’s hardware characteristics [5]. As $\theta _ { \mathrm { d i v } }$ is a constant term which remains unchanged during the measurement, we can omit this term for simplicity1. Note the total distance is $2 ( d - \delta ( t ) )$ because the signal traverses a double distance back and forth in backscatter communication. δ(t) is the function of time-varying displacement due to the spinning, which can be expressed as:

$$
\delta (t) \approx r \cos (2 \pi f _ {s} t + \phi) \tag {4}
$$

where $f _ { s }$ is the spinning frequency that we expect to inspect, and φ is the initial angle $\angle T O R$ when t = 0. Note the distance

1It is easy to show that its omission does not affect our subsequent derivation and the periodicity of the spinning signal.

|RT | is approximately equal to $| R A | \ ( R O \bot A T )$ when the reader is far away from the tag $( e . g . > 2 \lambda )$ [6]. Substituting Eqn. 4 into Eqn. 3, we have the revised phase function:

$$
\theta (t) \approx \frac {4 \pi}{\lambda} \left(d - r \cos (2 \pi f _ {s} t + \phi)\right) \bmod 2 \pi \tag {5}
$$

From the equation, we see that the RF phase is a cosine signal which has a fundamental frequency as same as the spinning. Thus, RF phase can be considered as a raw spinning signal.

# B. Refining Spinning Signal

With respect to the continuity, using RF phase as spinning signal raises two issues in practice. First, the measured phase value jumps when it approaches to 0 or 2⇡ due to the mod operation [2]. Second, COTS reader may introduce ⇡ radians of ambiguity such that the reported phase can be the true phase (✓) or the true phase plus ⇡ radians (✓ + ⇡) due to the halfwave loss [3]. These two issues cause the measured phase out of order. Fig. 3(a) presents an example of phase sequence which is collected in our lab. From the figure, we can see that the sequence is split up into many short discontinuous series, which goes against our analysis of their frequency or period. To address them, we transform the original phase ✓(t) to the space of sin(2✓). Then, the spinning signal, denoted as $s ( t )$ , is refined as:

$$
s (t) = \sin (2 \theta (t)) \approx \sin \left(\frac {8 \pi}{\lambda} (d - r \cos (2 \pi f _ {s} t + \phi))\right) \tag {6}
$$

Suppose the original period equals $T _ { s } ( T _ { s } = 1 / f _ { s } )$ . It is easy to figure out that $s ( t + T _ { s } ) = \sin ( 2 \theta ( t + T _ { s } ) ) = \sin ( 2 \theta ( t ) ) = s ( t ) .$ , that is, the refined spinning signal maintains the period as the original phase sequence. Meanwhile, the refined signal is also resistant to haft-wave loss (see Theorem. 1).

Theorem 1. The refined spinning signal does eliminate the ⇡-ambiguity caused by half-wave loss.

Proof. Because sin $( 2 ( \theta ( t ) \pm \pi ) ) ~ = ~ \sin ( 2 \theta ( t ) \pm 2 \pi ) ~ =$ sin(2✓(t)), s(t) has the same value no matter the reported value equals ✓ or $\theta \pm \pi$ . Thus, the refined spinning signal resists to half-wave loss.

Fig. 3(b) illustrates an example of the refined spinning signal, which is much more smooth and continuous compared against the original phase sequence shown in Fig. 3(a).

![](images/4696d59a2644001cfec9389e4ece4ff19f47d7e6e89f215ea7242d52c00a9125.jpg)



Fig. 5: Illustration of device translation in 2D. The reader translates from position R to R0 .

# C. Limitations of Single-Tag Based Approach

The refined spinning signal is a good indicator to describe the spinning in quiet settings. However, such signal heavily depends on d, i.e. the distance between the reader and turntable center, as suggested in Eqn. 6. As aforementioned, it is hard to hold the distance in noisy industrial settings. Even tiny shaking of the reader or the turntable would introduce unpredictable distances. This is the reason why the prior work [2] requires a mandatory assumption that both the RFID reader and spinning source have no additional displacements except those induced by the spinning during the measurement. Further, the final received phase is derived from a combination of multiple copies of RF signals due to multipath effect. The measured phase value usually far deviates from the expected one. Fig. 3(c) shows the spinning signal acquired from a same spinning process as shown in Fig. 3(b) but under a noisy environment. Clearly, it totally cannot represent the original spinning any more. Therefore, we need to develop a more robust spinning signal.

# IV. SENSING WITH DUAL TAGS

We call the instability caused by either motion of devices or changes of environment as system shaking. The approach which can tolerate the system shaking is called as anti-shaking sensing. We attach dual tags on the same spinning object to achieve more robust sensing.

# A. Rationale Behind Anti-Shaking Sensing

Why could dual tags resist shaking? We begin to answer this question from line-of-sight scenario (i.e. free-space scenario), where the signal from the reader arrives along one dominate path, and then discuss it in a more complex scenario with multipath effect later.

Relative phase: For simplicity, we assume that both tags and the reader lie on a two dimensional plane (extension to 3D will be addressed later). We consider the dual tags $T _ { 1 }$ and $T _ { 2 }$ are attached on a turntable, as shown in Fig. 5. The reader situates at direction ↵ (i.e. the angle of arrival). When the tags rotate an angle of 2⇡ $f _ { s } t$ at time $t ,$ we observe $\Delta d ( t )$ translation between RO and $R ^ { \prime } O$ due to the shaking of the reader or the target. Notice that here we have a reasonable assumption that the reader is at a far distance compared to the movement of devices, thus, the angle of arrival ↵ does not change. We can get the two tags’ phase values when the reader is translated to position R0 as follows:

![](images/810a9bf69a558970099a4f2190b7cfe1fcae09bcfa336a485fb2d210f8f85b07.jpg)



(a) Spinning with shaking

![](images/7bd176848872ec07762ab497a6c42129e77b82ebe0b9f68745e8738710f47855.jpg)



(b) Relative spinning model   
Fig. 6: Illustration of relative spinning. (a) Although the turntable translates a lot when it is spinning, the relative distance between two tags remain unchanged. (b) From the perspective of T1, T2 appears to move around $T _ { 1 }$ in a circle. Thus, the relative phase only depends on the spinning itself instead of the shaking induced translation.

$$
\theta_ {1} (t) \approx \frac {4 \pi}{\lambda} \left(d + \Delta d (t) - r _ {1} \cos (2 \pi f _ {s} t + \phi_ {1} + \alpha)\right) \bmod 2 \pi
$$

$$
\theta_ {2} (t) \approx \frac {4 \pi}{\lambda} \left(d + \Delta d (t) - r _ {2} \cos (2 \pi f _ {s} t + \phi_ {2} + \alpha)\right) \bmod 2 \pi
$$

Then, we define the relative phase of the two tags (denoted as $\Delta \theta ( t ) )$ by subtracting their phase values. Since $( { a - b } )$ mod c = (a mod c − b mod c) mod $c , \Delta \theta ( t )$ can be given by:

$$
\begin{array}{l} \Delta \theta (t) = (\theta_ {1} (t) - \theta_ {2} (t)) \bmod 2 \pi \\ \approx \frac {4 \pi}{\lambda} \left(r _ {2} \cos (2 \pi f _ {s} t + \phi_ {2} + \alpha) - r _ {1} \cos (2 \pi f _ {s} t + \phi_ {1} + \alpha)\right) \bmod 2 \pi \\ = \frac {4 \pi}{\lambda} [ (r _ {2} \cos (\phi_ {2} + \alpha) - r _ {1} \cos (\phi_ {1} + \alpha)) \cos (2 \pi f _ {s} t) \\ \left. - \left(r _ {2} \sin \left(\phi_ {2} + \alpha\right) - r _ {1} \sin \left(\phi_ {1} + \alpha\right)\right) \sin \left(2 \pi f _ {s} t\right) \right] \bmod 2 \pi \\ = \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \arctan \frac {a _ {2}}{a _ {1}}) \bmod 2 \pi \tag {7} \\ \end{array}
$$

where

$$
\left\{ \begin{array}{l} a _ {1} = r _ {2} \cos (\phi_ {2} + \alpha) - r _ {1} \cos (\phi_ {1} + \alpha) \\ a _ {2} = r _ {2} \sin (\phi_ {2} + \alpha) - r _ {1} \sin (\phi_ {1} + \alpha) \\ r = \sqrt {a _ {1} ^ {2} + a _ {2} ^ {2}} \end{array} \right.
$$

It is easy to find that r is actually the separated distance of two tags. Both the variables d and $\Delta d ( t )$ are removed by the subtraction, which means the relative phase at an arbitrary time is independent of either the initial position or device translation as long as the reader’s direction does not change. Eqn. 7 fully considers the initial angles of both tags when $t = 0 ,$ , which allows to attach tags at arbitrary positions on the turntable as long as they are driven by the same spinning. Interestingly, the relative phase can be finally converted into a cosine function with the same frequency as the spinning, like what we discuss with a single tag.

We can also understand the relative phase from another intuitive perspective. Relative to the position of $T _ { 1 } ,$ the second tag $T _ { 2 }$ simply appears to move around a circle, as illustrated in Fig. 6(a). Although the turntable translates due to the shaking, the relative distance between two tags remains unchanged. In other words, two tags perform relative motion driven by the spinning instead of the shaking. In this way, we can simplify the relative phase using another equivalent model as shown in Fig. 6(b). Suppose the angle of arrival and the distance between two tags are equal to ↵ and r respectively, then the relative phase is also given by:

![](images/26fde76297ad2c03b6bae5f661ffd73cb8d29bf7c3e69c187c07ff02cbfc371c.jpg)



Fig. 7: Multipath scenario. Because of two reflectors, the signal coming from reader propagates through two different paths with different directions and distances.

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha) \bmod 2 \pi \tag {8}
$$

where φ is the initial angle between $T _ { 1 } T _ { 2 }$ and x-axis at time $t \ = \ 0 ,$ and $r \cos ( 2 \pi f _ { s } t + \phi + \alpha )$ is the saved distance of signal propagating to $T _ { 2 }$ compared with that to $T _ { 1 }$ . It is easy to prove that Eqn. 7 and Eqn. 8 are completely equivalent and convertible. We will use Eqn. 8 by default in the subsequent sections for simplicity.

Relative spinning signal: Similarly, to deal with the discontinuity of phase, we formally define the relative spinning signal (RSS) as below:

$$
s (t) = \sin (2 \Delta \theta (t)) = \sin (2 \theta_ {1} (t) - 2 \theta_ {2} (t)) \tag {9}
$$

$\theta _ { 1 }$ and $\theta _ { 2 }$ are measured phase values of two tags in practice. One might wonder if the periodicity generated by the above equation is indeed maintained as that of the actual spinning. In fact, it is easy to observe from Eqn. 9 that $s ( t + T _ { s } ) = \sin ( 2 \Delta \theta ( t + T _ { s } ) ) = \sin ( 2 \Delta \theta ( t ) ) = s ( t )$ . We can also intuitively understand such conclusion from Fig. 6. The only movement that drives $T _ { 2 }$ to rotate around $T _ { 1 }$ is the spinning of the turntable.

# B. Dealing with Multipath Effect

Our discussion so far has involved line-of-sight scenarios. Here, we extend to multipath environment, showing RSS continues to be resistant to shaking. As aforementioned, no matter how the reader or turntable shakes, the final effect is equivalent to the relative spinning that $T _ { 2 }$ rotates around $T _ { 1 }$ . Here, we also employ such model to show how the multipath propagation affects the relative spinning signal. As shown in Fig. 7, suppose the wireless signal propagates along K different paths to arrive at $T _ { 1 }$ with initial lengths $d _ { 1 } , d _ { 2 } , \dots , d _ { K }$ , along directions ${ \alpha } _ { 1 } , { \alpha } _ { 2 } , \ldots , { \alpha } _ { K }$ . Finally, these copies of signals are overlapped at each tag. From basic channel models, the wireless channel $h _ { i }$ arrived at tag $T _ { i }$ $( i = 1 , 2 )$ can be expressed as the complex number [7]:

$$
h _ {i} (t) = \frac {1}{d ^ {2} (t)} e ^ {\mathbf {J} \theta (t)} \tag {10}
$$

where $d ( t )$ and $\theta ( t )$ are the distance and phase shift at time t. We can then get the overlapped RF signals at $T _ { 1 }$ and $T _ { 2 }$ as follows [6]:

$$
h _ {1} (t) \approx \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} d _ {k}} \tag {11}
$$

$$
h _ {2} (t) \approx \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {k} - r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k}))}
$$

where $d _ { k }$ is the distance from the reader to $T _ { 1 }$ through the $k ^ { t h }$ propagation path, and r cos $\left( 2 \pi f _ { s } t + \phi + \alpha _ { k } \right)$ is the saved distance to $T _ { 2 }$ compared with $T _ { 1 }$ . Then we compute the relative wireless channel $h ( t ) = h _ { 1 } ( t ) h _ { 2 } ^ { \ast } ( t )$ :

$$
\begin{array}{l} h (t) = \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} d _ {k}} \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {- \mathbf {J} \frac {4 \pi}{\lambda} (d _ {k} - r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k}))} \\ = \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k})} \left[ \frac {1}{d _ {k} ^ {2}} + \sum_ {l \neq k} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {k} - d _ {l})} \right] \tag {12} \\ \end{array}
$$

Notice that the phase of the first term, $\begin{array} { r } { i . e . \ \frac { 4 \pi } { \lambda } r \cos ( 2 \pi f _ { s } t + \phi + } \end{array}$ . 4⇡λ r cos(2⇡fst+φ+ $\alpha _ { k } )$ , in the above equation is nearly identical to the relative phase in Eqn. 8 derived in the line-of-sight scenario, and is independent of any translation. Unfortunately, the second term indeed depends on the distances. However, two observations inspire us: First, if the environment remains constant (i.e., multiple propagations hold), the second term reduces to a constant multiplier, which merely scales the final phase value. Second, even if the environment changes or the shaking changes the propagations, any variance caused by the second term drops significantly when summing over all multipath propagations. These two observations show that RSS is resistant to shaking even in multipath scenarios. This property holds no mater how the turntable or the reader is shaken. Even so, we must stress that shaking-induced translation cannot be unbounded and must be relatively small compared to the distance between the turntable and the reader, even if the reader/turntable shakes moderately. This is not a harsh assumption and can be easily met in practice as validated in our evaluation.

# C. Extending to Three Dimensional Scenario

Let us now consider the RSS in 3D space. The spinning surface is considered as the x-y plane (i.e. horizontal plane), while the reader may not lie on this plane. In this way, apart from the azimuthal angle ↵ in the horizontal plane, we also need another parameter, i.e. the polar angle $\beta$ along the vertical direction to fully describe the reader’s incident signal. Correspondingly, the relative phase in 3D is given by:

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha) \sin \beta \bmod 2 \pi \tag {13}
$$

Apparently, even generalizing to three dimensions, RSS depends only on the reader’s spatial orientation instead of its movement. Notice, such a generalization is crucial because we can not require the reader and object to perfectly stay on a two dimensional plane during the whole spinning in practice.

# D. Putting Things Together

In summary, after all the above discussions, RSS holds well either in complex indoor environment (i.e., multipath exists) or

![](images/300d1e00a7f5079376f3319ca4ea5c25d02adbc89611147421458361bb2e52d6.jpg)



(a) Signal on the first tag

![](images/c24eff177a9c343abde3b032f797ece4024193ce6b788b49fbba0d72b789e594.jpg)



(b) Signal on the second tag

![](images/cedf5e21f5546b2fd1102fa04ceba278eaf8a3d60000bca40ad264e97781c9d0.jpg)



(c) Relative spinning signal   
Fig. 8: Spinning signals. It is difficult to see the periodicity on the received phase sequence at the two tags. Performing the subtraction between two phase values on two tags, reveals the periodic and well aligned spinning signal.

3D scenarios. To get a visual impression, we show the spinning signals induced by dual tags respectively, as well as their relative spinning signal, in Fig. 8, under a quite noisy setting. It is clear that the relative spinning signal becomes far more regular and well reveals the intrinsic spinning frequency as expected, compared with the spinning signal purely collected from each tag. Hence, it is reasonable and feasible that we utilize RSS to reflect and inspect the frequency of spinning.

# V. SYSTEM IMPLEMENTATION

This section begins with the practical challenges we face when applying relative spinning signal in spinning sensing, and then presents the solution to address these challenges.

# A. Challenges

Making sensing of spinning or vibration using RFID tags is to inspect the motion through the random and low-frequency readings of tags, where each reading is viewed as one sampling of motion status. A COTS tag can be read for about 40 times per second on average (i.e., sampling frequency equals 40Hz). As stated by the Nyquist-Shannon sampling theorem, for a given analog signal of bandlimit, the sampling rate should be at least twice the highest frequency contained in the signal in order to guarantee perfect reconstruction of the original signal. Thus, Tagtwins is able to recover spinning signal with up to 20Hz frequency according to the sampling theorem, which obviously can not meet practical needs in most applications. Therefore, the central task of applying RSS is to recover the spinning signal, even high-frequency signal (> 20Hz), through the random and discrete readings.

# B. Classic Compressive Reading

The work [2] utilizes compressive sensing to recover the spinning signal which is derived from a single tag (see Eqn. 6). Such approach is called as Compressive Reading (CR). The signal is periodic and thereby has a very sparse representation in the frequency domain, where it can be represented into a linear combination of phasors via the exponential Fourier series. CR firstly converts the spinning signal into the frequency domain, and then utilizes the inherent randomness of tag’s readings to construct the measurement matrix and the corresponding result. Specifically, the spinning signal s can be represented as follows:

$$
y = \Phi s + \eta = \Phi \Psi^ {- 1} S + \eta \tag {14}
$$

$$
\Phi = \left( \begin{array}{c c c c c c} (1, 0. 1) & x & (3, 0. 4) & (4, 0. 6) & x & (6, 0. 8) \\ \hline 1 & 0 & 0 & 0 & 0 & 0 \\ \hline 0 & 0 & 1 & 0 & 0 & 0 \\ \hline 0 & 0 & 0 & 1 & 0 & 0 \\ \hline 0 & 0 & 0 & 0 & 0 & 1 \end{array} \right) \quad y = \left( \begin{array}{c} \sin (2 \times 0. 1) \\ \sin (2 \times 0. 4) \\ \sin (2 \times 0. 6) \\ \sin (2 \times 0. 8) \end{array} \right)
$$

Fig. 9: Illustration of compressive reading. As the tag is read at the first, third, fourth and sixth millisecond, the measurement matrix and result are constructed as above.

where Φ is the measurement matrix, is the Fourier basis, S is the sparse coefficient vector in Fourier domain, and ⌘ denotes the measurement noise. The time-domain signal s is not compact but its frequency representation S is sparse.

Suppose the tag is read M times during N milliseconds. The input is a sequence of two-tuple samples, denoted as $\{ ( t _ { 1 } , \theta [ t _ { 1 } ] ) , ( t _ { 2 } , \theta [ t _ { 2 } ] ) , \dots , ( t _ { M } , \theta [ t _ { M } ] ) \}$ }, where its phase value at time $t _ { m }$ is equal to $\theta [ t _ { m } ]$ . Note that all time variables are integers and expressed with unit of millisecond. Our goal is to know the phase value at any given time, i.e. recovering the signal. Then, the $M \times N$ measurement matrix and $M \times 1$ result vector are respectively constructed as follows:

$$
\Phi [ m, n ] = \left\{ \begin{array}{l l} 1, & \text { if   } t _ {m} \text {   exists   and   } t _ {m} = n \\ 0, & \text { otherwise } \end{array} \right. \tag {15}
$$

where $m = 1 , \ldots , M$ and $n = 1 , \ldots , N$ . The existence of $t _ { m }$ means the tag is read at time $t _ { m } , i . e .$ , the sequence contains a tuple of $\left( { \displaystyle t _ { m } , \theta [ t _ { m } ] } \right)$ . Each row only has one non-zero element. Correspondingly,

$$
y [ m ] = \sin (2 \theta [ t _ {m} ]) \tag {16}
$$

Note that the spinning signal derived by a single tag is defined in Eqn. 6 instead of the original phase value. [2] further aggregates the reading into many frames. However, according to our empirical study, we find that the recovery results are almost identical whether one uses frame or not. To visually understand the measurement matrix and result, we illustrate an example in Fig. 9. Finally, the signal could be reconstructed reliably through solving an $l _ { 1 }$ or $l _ { 2 }$ optimization problem. One of the great advantages of CR is that it constructs the measurement matrix based on the collected readings, rather than builds it in advance and then guides the reader’s reading. This allows us to employ COTS readers for sensing without

![](images/ad1f54eb45b789f89ea14bb50cc1943ef3428366f37c926f37ab9df27d9f39b1.jpg)



Fig. 10: The distribution of timestamp interval

any modification.

# C. Dual Compressive Reading

At first glance, we can employ CR to respectively recover two spinning signals induced by dual tags and then subtract them to obtain the final relative spinning signal. Unfortunately, this naive solution fails because neither of two spinning signals is periodic and sparse, as shown in Fig. 1(b), although their RSS is sufficiently compact in the frequency domain. Thus, we have to directly recover the RSS. Our approach is called as Dual Compressive Reading (DCR). Being different from CR, DCR has two input sequences in dual-tag system as follows:

$$
\left. \right.\left\{\left(t _ {1, 1}, \theta_ {1} \left[ t _ {1, 1} \right]\right), \left(t _ {1, 2}, \theta_ {1} \left[ t _ {1, 2} \right]\right), \dots , \left(t _ {1, M _ {1}}, \theta_ {1} \left[ t _ {1, M _ {1}} \right]\right)\right\} \tag {17}
$$

$$
\left. \right.\left\{\left(t _ {2, 1}, \theta_ {2} [ t _ {2, 1} ]\right), \left(t _ {2, 2}, \theta_ {2} [ t _ {2, 2} ]\right), \dots , \left(t _ {2, M _ {2}}, \theta_ {2} [ t _ {2, M _ {2}} ]\right)\right\}
$$

which are collected from two tags respectively. Similar to Eqn. 16, each element of the measurement result vector is given by

$$
y [ m ] = \sin (2 (\theta_ {1} [ t _ {m} ] - \theta_ {2} [ t _ {m} ])) \tag {18}
$$

This equation indicates that the $m ^ { t h }$ measurement result element equals the phase difference of two tags measured at time $t _ { m } .$ . Everything looks like going well so far. Unfortunately, the above phase difference cannot be obtained in practice because tags are exclusively read in a time-sharing fashion. In other words, it is impossible for us to read two tags’ phase values simultaneously at a specific time point. We call this problem misaligned reading.

We observe an important fact that the measurement of phase value has the property of read-time locality, which means two tags are quite closely read although they are read alternatively. Such locality stems from the fact that the whole reading is composed of numerous inventory rounds, within each of which two tags must be read once. Each inventory lasts very short, making the reading time of two tags very close. To validate such observation, we persistently read the two tags for 100, 000 times and then calculate the interval of two tags’ readings. The interval distribution is shown in Fig. 10. Not surprisingly, we find the interval has a mean of 2.3ms. Compared against the 1ms resolution of timestamp, two tags are almost read concurrently during each inventory.

Driven by the above observation, we employ Gaussian Interpolation to align the two phase sequences. Now our problem turns into: how to estimate the phase values of $T _ { 1 }$ (or $T _ { 2 } )$ at timestamps of $\left\{ t _ { 2 , 1 } , \ldots , t _ { 2 , M _ { 2 } } \right\} ( \mathrm { o r } \left\{ t _ { 1 , 1 } , \ldots , t _ { 1 , M _ { 1 } } \right\} ) ?$ Given a timestamp $t _ { 2 , i } ~ ( i = 1 , \ldots , M _ { 2 } )$ , we first choose L phase values of $T _ { 1 }$ whose timestamps are most close to $t _ { 2 , i }$ (according to the read-time locality). Then, $\begin{array} { r } { \theta _ { 1 } [ t _ { 2 , i } ] = \sum _ { l = 1 } ^ { L } w _ { l } \theta _ { 1 } [ t _ { l } ] } \end{array}$ where wl is the weight from Balckman window and $\theta _ { 1 } [ t _ { l } ]$ is the $l ^ { t h }$ chosen phase value. The similar process is performed for tag $T _ { 2 }$ . In this way, we will totally obtain $M _ { 1 } + M _ { 2 }$ phase values for each tag.

![](images/bfda3475cfd46e9b7015380a135db95bc2e88b00ed56347e4a9d4fb4de5d107f.jpg)



Fig. 11: Experimental setup

Finally, we utilize compressive reading over two interpolated phase sequences to recover the relative spinning signal. The fundamental frequency we want to inspect can also be obtained from the frequency spectrum of the recovered signal.

# VI. EVALUATION

We implement Tagtwins using COTS UHF reader and tags and conduct performance evaluation in our lab environment as shown in Fig. 11.

# A. Building Prototype

Hardware: We adopt an Impinj Speedway R420 reader which is compatible with EPC Gen2 standard and operates during the frequency band of 920.5  924.5 MHz by default. The reader is connected to our host end through Ethernet. One reader antenna with circular polarization and 8dBi gain is employed, whose size is 225mm ⇥ 225mm ⇥ 33mm. Totally four types of tags from Alien Corp, modeled $^ { 6 6 } 2 \times 2 ^ { 5 }$ , “Square”, “Squig” and “Squiggle” are employed. Software: Our implementation involves the LLRP (Low Level Reader Protocol) [8] to communicate with the reader. Impinj readers extend this protocol to support the phase report. The client code is implemented using Jave language. We use a Samsung PC to run our algorithms, as well as connect to the reader under LLRP. The machine equips Intel Core i7 CPU at 2.4GHz and 8G memory. Baseline: Two RFID tags are attached on a rotating machine, whose frequency can range from 0 to 2, 100 RPM. They are separated by a distance of 5cm and their distance to the antenna is set to 2m by default. We collect the ground truth of frequency by utilizing a laser tachometer, which can measure RPM from a reflective target using a laser light source (see Fig. 11).

# B. Overall Sensing Accuracy

To gain an intuitive impression on Tagtwins’ anti-shaking sensing accuracy, we randomly shake the reader antenna along the following kinds of trajectories: (a) three dimensional linear to-and-fro trajectory; (b) three dimensional arc-shaped trajectory; (c) random arbitrary shaped trajectory. All of these shakes are performed up to a range of 30cm. Besides, in view of the case that the spinning object shakes, we utilize an orbital shaker to automatically shake the turntable along a restricted circular orbit with different speeds (see Fig. 11). As a comparison study, we also consider the situation where both the antenna and turntable remain motionless. We compare the performance of Tagtwins against Tagbeat, which is not resistant to device translation. Fig. 12 plots the sensing errors in frequency. We find that both Tagtwins and Tagbeat achieve high precision (around 0.2Hz) if the equipment does not move during the experiment. However, if either the reader or the object observes some level of translation, even in a slight way, the accuracy of Tagbeat will be affected severely, dropping to more than 7Hz. That is where our system wins out. In general, Tagtwins achieves a mean error of 0.27Hz in frequency with the standard deviation of 0.53Hz, corresponding to 0.43ms error in period, which is fairly good and can even rival those of specialized tachometers.

![](images/e02b4d4f14bf71ff6af8853bdf90e5c5ce19d20d2a72aa2cb374af7abea81dfd.jpg)



Fig. 12: Errors vs. trajectories

![](images/98cc59809fb69221c602d16bc2b3488d0d250a2084bd510d0ed6363ea134e425.jpg)



Fig. 13: Impact of spinning speed

![](images/7a76e80c76c2735a87b6359209a14e172bacbd9955cd5f0a6c609819f6751fa3.jpg)



Fig. 14: Impact of dual-tag distance

![](images/066126230e7eff8fdd89d618f510515ce5111e70a0c3ad9b9204907b055a619f.jpg)



Fig. 15: Impact of antenna distance

![](images/a541dfdc6136bebf53ed1f55488a9999cf539a05cf7e5f72c4eb16e0552e25aa.jpg)



Fig. 16: Impact of diversity

![](images/bfe2d4e9f582b5b2babc721d6d93f421fc4859c47a8dda94c851f694ad547c10.jpg)



Fig. 17: Impact of multipath

# C. Tuning Parameters

We further discuss the following factors that may have an influence on Tagtwins’ performance.

1) Impact of Spinning Speed: To check Tagtwins’ effectiveness under high frequency scenario, we tune the revolving speed of the turntable from 670 to 2, 067 RPM with seven levels. For each setting, we repeat the experiment for 50 times and Fig. 13 depicts the averaged results. It can be seen that the mean errors among various RPMs have little difference, from the minimum of 0.08Hz to the maximum of 0.42Hz. And the result is more accurate when the object spins at a low speed, which is reasonable because more samples in one period can be collected for recovering.   
2) Impact of Dual-Tag Distance: As mentioned before, we have no requirement of the dual tags’ geometric relationship

as long as their separation is fixed. We then set this separation to 3cm, 5cm and 8cm respectively while keeping the same RPM and plot the recovered signals in Fig. 14. We observe from this figure that although the three signals vary a lot in pattern, their periods keep consistent (i.e. about 57ms). The averaged sensing accuracy is 0.10Hz, 0.19Hz and 0.28Hz in these three settings. In our experimentation, we choose the dual-tag distance as 5cm by default.

3) Impact of Antenna Distance: Commercial RFID products can support a reading range of 6  7 meters in indoor environment, so we change the distance between reader antenna and spinning object from 0.5m to 5m. Fig. 15 shows the accuracy with different distances. We have the following observations: (a) The performance achieves the best when the distance equals 1.5m. (b) When the antenna is too close to the tags, i.e. less than 0.5cm, the accuracy will drop. Recall that we have a premise in IV that the antenna and turntable should have a relatively large distance compared to their movement, and this premise will be broken if the antenna gets near the turntable (e.g., distance is below two wavelengths, about 64cm). Thus, shaking-induced translation can not be well handled by our relative signal, leading to more errors. (c) The performance also decreases when the antenna is too far from the tags, i.e. more than 5m. This is understandable because a larger distance will result in a lower reading rate, which means fewer samples are collected. In summary, we suggest a distance of 1m to 3m according to our empirical study.   
4) Impact of Diversity: We experiment on four models of tags, namely “2 ⇥ 2”, “Square”, “Squig” and “Squiggle” to study the influence of tag diversity. All these tag types have different antenna sizes and shapes as depicted in Fig. 16. For each tag model, the result is averaged from 50 experiments with the same setting. We find that although the errors of all models maintain at a small value (less than 0.6Hz), there

exist some differences among them. 2⇥2, Squig and Squiggle have very close accuracy (i.e., 0.28Hz, 0.25Hz and 0.30Hz respectively), while Square model observes a lower accuracy of 0.61Hz with a higher standard deviation of 0.43Hz. This can be explained by the size of tag’s antenna, because Square has a more compact volume (only 22.5mm ⇥ 22.5mm) compared with the other three types. Generally speaking, the tag with larger antenna could absorb more energy from the reader, making its backscattered signal stronger (i.e. higher SNR) and thereby outputting more precise sensing result. In our experimentation, we use model “Squig” in most cases.

5) Impact of Multipath: One prominent advantage of utilizing RFID to sense spinning over prior approaches is that it can work either in the absence of line-of-sight (LOS) or the presence of rich multipath. To investigate this, we perform evaluation in two typical settings: (a) a clear freespace environment with no multipath effect; (b) a non-lineof-sight (NLOS) or strong multipath scenario with obstacles between (or around) the turntable and reader. For each setting, we carry out 50 experiments and plot the CDF of frequency error in Fig. 17. It is clear that the overall accuracy in LOS is better than that in NLOS. The mean error is 0.32Hz with 90% below 0.54Hz in LOS scenario while that of NLOS is 0.79Hz with 90% below 2.1Hz. Since more paths will arrive at the two tags in NLOS scenario instead of one dominant path, the error is accumulated along these paths. Besides, the reflected signal will traverse a longer path compared to the direct one, impairing the signal strength. Even the accuracy drops a little in NLOS environment, it still overwhelms many traditional instruments like laser which fails in such condition.

# VII. RELATED WORK

We briefly review the literature that is related to our work.

Traditional sensing approaches: One typical way to inspect spinning is to employ mechanical sensors to capture the force induced on the instrument and utilizes the fact that the centrifugal force on a rotating mass depends on the speed of rotation. These methods [9], [10] make sense of spinning via infrared/laser, which is then reflected by a reflective tape on the object. The rotation speed is then measured as the rate at which the light beam is reflected back. The authors in [11] demonstrate nanometer vibration analysis of a target by a selfaligned optical feedback vibrometry technique. Optical-based schema is a powerful choice when direct-contact measurement is infeasible for technical or safety reasons.

RFID-based sensing approaches: A mountain of research work in RFID area has focused on localization in the past years [5], [12]. Tagbeat [2] makes the first attempt to inspect vibration via RFID technology, with the advantage of being low-cost and applicable to occluded and non-line-of-sight scenario. But it is not robust to the shake of device, hindering its further application in real practice. In contrast, we tactfully solve this issue by employing dual tags and utilizing their relative phase as the spinning signal.

by sound hitting an object and recovers the sound that pro-

Other related issues: [13], [14] aim to communicate small packets of information by modulating the vibrations of motors present in mobile phones. [15] extracts small vibrations caused duces them using high-speed video of the object. The authors in [16] make it possible to observe and capture a high-speed periodic video well beyond the abilities of a low-frame-rate camera. The proposed reconstruction algorithms are inspired by compressive sensing. Wei et al. [17] recover loudspeaker sound by inspecting the subtle disturbance it causes to the radio signals generated by the co-located WiFi transmitter.

# VIII. CONCLUSION

This work presents an RFID-based spinning sensing system that is robust to noisy settings and achieves sub-hertz high accuracy. Our key innovations lie in leveraging the relative signal of dual RFID tags to resist the system shaking and proposing a new form of compressive reading technique to recover the signal. We believe our system will promote more possibilities of RFID-based sensing solution in practical deployments.

# ACKNOWLEDGMENT

The research of Lei Yang is partially supported by ECS (NO. 25222917), NSFC General Program (NO. 61572282), and Alibaba Innovation Research. The research of Lei Xie is partially supported by NSFC (No. 61472185), and JiangSu Natural Science Foundation (No. BK20151390).

# REFERENCES

[1] Y. Lei, Z. He, and Y. Zi, “Application of an intelligent classification method to mechanical fault diagnosis,” Expert Systems with Applications, vol. 36, no. 6, pp. 9941–9948, 2009.   
[2] L. Yang, Y. Li, Q. Lin, X.-Y. Li, and Y. Liu, “Making sense of mechanical vibration period with sub-millisecond accuracy using backscatter signals,” in Proc. of ACM MobiCom, 2016.   
[3] ImpinJ, “Speedway revolution reader application note: Low level user data support,” in Speedway Revolution Reader Application Note, 2010.   
[4] D. M. Dobkin, The RF in RFID: UHF RFID in Practice, 2012.   
[5] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: Realtime tracking of mobile rfid tags to high precision using cots devices,” in Proc. of ACM MobiCom, 2014.   
[6] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proc. of ACM MobiCom, 2014.   
[7] D. Tse and P. Viswanath, Fundamentals of wireless communication. Cambridge university press, 2005.   
[8] EPCglobal, “Low level reader protocol (llrp),” 2010.   
[9] P. Castellini, M. Martarelli, and E. P. Tomasini, “Laser doppler vibrometry: Development of advanced solutions answering to technology’s needs,” Mechanical Systems and Signal Processing, vol. 20, no. 6, pp. 1265–1285, 2006.   
[10] P. Cheng, M. S. M. Mustafa, and B. Oelmann, “Contactless rotor rpm measurement using laser mouse sensors,” IEEE Transactions on Instrumentation and Measurement, vol. 61, no. 3, pp. 740–748, 2012.   
[11] K. Otsuka, K. Abe, J.-Y. Ko, and T.-S. Lim, “Real-time nanometervibration measurement with a self-mixing microchip solid-state laser,” Optics letters, vol. 27, no. 15, pp. 1339–1341, 2002.   
[12] C. Duan, L. Yang, and Y. Liu, “Accurate spatial calibration of rfid antennas via spinning tags,” in Proc. of IEEE ICDCS, 2016.   
[13] N. Roy, M. Gowda, and R. R. Choudhury, “Ripple: Communicating through physical vibration,” in Proc. of USENIX NSDI, 2015.   
[14] N. Roy and R. R. Choudhury, “Ripple ii: Faster communication through physical vibration,” in Proc. of USENIX NSDI, 2016.   
[15] A. Davis, M. Rubinstein, N. Wadhwa, G. Mysore, F. Durand, and W. T. Freeman, “The visual microphone: Passive recovery of sound from video,” in Proc. of ACM SIGGRAPH, 2014.   
[16] A. Veeraraghavan, D. Reddy, and R. Raskar, “Coded strobing photography: Compressive sensing of high speed periodic videos,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 33, no. 4, pp. 671–686, 2011.   
[17] T. Wei, S. Wang, A. Zhou, and X. Zhang, “Acoustic eavesdropping through wireless vibrometry,” in Proc. of ACM MobiCom, 2015.