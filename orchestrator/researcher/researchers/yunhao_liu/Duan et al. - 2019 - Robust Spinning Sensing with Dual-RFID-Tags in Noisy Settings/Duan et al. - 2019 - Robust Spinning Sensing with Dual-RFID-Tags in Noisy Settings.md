# Robust Spinning Sensing with Dual-RFID-Tags in Noisy Settings

Chunhui Duan, Student Member, IEEE, Lei Yang, Member, IEEE, Qiongzheng Lin, Student Member, IEEE, Yunhao Liu, Fellow, IEEE, and Lei Xie, Member, IEEE

Abstract—Conventional spinning inspection systems, equipped with separated sensors (e.g., accelerometer, laser, etc.) and communication modules, are either very expensive and/or suffering from occlusion and narrow field of view. The recently proposed RFID-based sensing solution draws much attention due to its intriguing features, such as being cost-effective, applicable to occluded objects and auto-identification, etc. However, this solution only works in quiet settings where both the reader and spinning object remain absolutely stationary, as their shaking would ruin the periodicity and sparsity of the spinning signal, making it impossible to be recovered. To overcome such limitation, this work introduces Tagtwins, a robust spinning sensing system that can work in noisy settings. It addresses the challenge by attaching dual RFID tags on the spinning surface and developing a new formulation of spinning signal that is shaking-resilient, even if the shaking involves unknown trajectories. Our main contribution lies in two newly developed techniques. First, we propose relative spinning signal using dual tags’ readings and analytically demonstrate its feasibility in various settings. Second, we introduce dual compressive reading to inspect high-frequency spinning with relatively low reading rate of RFIDs. We have implemented Tagtwins with commercial RFID devices and evaluated it extensively. Experimental results show that Tagtwins can inspect the rotation frequency with high accuracy and robustness.

Index Terms—RFID, spinning sensing, robust, dual-tag.

# 1 INTRODUCTION

S PINNING is a mechanical phenomenon which dominates ourindustrial lives everyday, such as conveyors, motors, robotics, and so on. In many cases, spinning is undesirable and must be observed accurately, especially in smart factory. For example, rotating machineries nowadays are widely employed in industrial equipment. The unexpected downtime due to their undesirable vibrations has become more costly than ever before [1]. In particular, utilizing spinning frequency for equipment diagnosis is a common method.

There are several traditional approaches to inspect vibration or spinning. They are usually are based on conventional motion sensors, such as acceleration, infrared sensors or cameras. Usually, most of these sensors are bulky, heavy, intrusive, or energyconsuming. For example, accelerometers need to connect to a control panel for vibration signal collection as shown in Fig. 1(a), thus is inconvenient to operate especially for those wired one. Due to the cables, the sensors cannot be freely attached on any kinds of vibrating surface like fans or centrifuging tubes. As Fig. 1(b) shows, infrared sensors [2] are common choices for highresolution and high-speed measurements, but fail in the absence of a line-of-sight to the objects. High-speed cameras may be another option, but are seldom adopted in industry due to their high cost. More details refer to Sec. 2.

To address the above issues, our prior research [3] proposes a novel measurement approach (i.e. Tagbeat), which supplements

Chunhui Duan and Yunhao Liu are with the School of Software, Tsinghua University, Beijing, China. E-mails: hui@tagsys.org, yunhao@greenorbs.com   
Lei Yang and Qiongzheng Lin are with the Department of Computing, The Hong Kong Polytechnic University, Hong Kong. E-mails: {young, lin}@tagsys.org

![](images/a0a437d6df5b2f3806859232a5fca890dbeea893829f7fcd12351ae8fece66a0.jpg)



(a) Accelerator

![](images/030c4a0fd84b447e4419c646f08421e079a4b689cbe272a9aaf1d70327af6bf6.jpg)



(b) Infrared meter   
Fig. 1: Tranditional vibration sensing approaches. (a) shows the accelerator based vibration sensing; (b) shows the infrared ray based vibration sensing.

the RFID communication functionality with fine-grained spinning (or vibration) sensing ability. A small and battery-free RFID tag is attached on the spinning object (i.e. turntable). The spinning displaces the tag within a small range, resulting in a regular change pattern of backscatter signal. Then we can reveal the spinning information by discerning such communication pattern without specialized sensors. Compared against traditional means, Tagbeat offers an appealing alternative, with the advantage of being costeffective, applicable to occluded objects, and auto-associative with the spinning object (by the tag’s ID). Moreover, since battery-free tags are powered and driven by wireless signals, no additional energy suppliers or RF transceivers are required, making them small and light enough to be attached on small objects.

In spite of high availability and promising foreground, Tag-

Lei Xie is with the Department of Computer Science and Technology, Nanjing University, Nanjing, China. E-mail: lxie@nju.edu.cn

![](images/028d4caeffff10681116a23ca4cb44666c781be2c1bf6db06463b1ef5acec819.jpg)



(a) Quiet setting

![](images/6db469ac989c83b63f346ebe97c1d995f40add720f61fc76867222464a18475a.jpg)



(b) Noisy setting   
Fig. 2: Spectrum of the spinning signal. (a) shows the spectrum of the spinning signals in a quiet setting. The spectrum is composed of several primary harmonic frequencies, and thereby the signal is very sparse in frequency domain as described in [3]; (b) shows the spectrum in a noisy setting. The spectrum is out of order and apparently not sparse any more due to the noise from the random shaking of the reader.

beat requires a quite rigorous assumption that the devices and the deployment surroundings must remain quiet, i.e. motionless. This is because any irregular and unexpected jitters of the tag’s backscatter signal incurred by the shaking of the reader or the turntable, would disturb the periodicity of spinning signal and further violate its sparsity in frequency domain. Fig. 2 compares the spectrums of two spinning signals collected in quiet and noisy settings respectively. Clearly, Tagbeat, which is driven by the technique of compressive sensing, fails to recover the nonsparse signal because there are too many linear combinations. Many practical scenarios are against the assumption of motionlessness, especially in industrial noisy settings, where the spinning tag usually experiences fast-changing environment $( e . g .$ , due to surrounding mobile objects) with non-ideal communication conditions every moment. For instance, many industrial operations happen in unstable platforms $( e . g .$ . vehicles and ships), whose shaking would lead to dramatic and unpredictable translations of readers. It is also hard to stably hold a handheld reader for a long time measurement. Our empirical study suggests that even a 5cm noisy translation of the device would make the spinning signal unrecoverable.

Motivated by the above limitations, this work presents a progressive design, named Tagtwins, a robust spinning sensing system that can work in noisy settings. Here, the noise means unpredictable shaking or translation of devices regardless of readers or spinning objects. In this work, Tagtwins addresses the challenge by attaching dual RFID tags on the spinning surface and develops a new formulation of spinning signal that is shaking-resilient. Fig. 3 shows a toy example. We allow both the turntable and reader to be randomly and simultaneously shaken when monitoring the spinning. We can accurately recover its spinning signal even if the shaking involves unknown trajectories. To this end, we exploit the observation that the distance between two tags is fixed independent of how the turntable or the reader shakes. Thus, however the devices change their positions, the relative position vector of dual tags remains constant and changes direction when the turntable rotates. Leveraging this observation, we develop the relative spinning signal which is derived from the relative wireless channels of two tags, to depict the spinning that occurs in noisy settings, without knowing any information on the absolute position or translation of the devices.

To quickly grasp our basic idea, we give a simplified explanation why our relative spinning signal can work in noisy settings.

![](images/9557059cd76b8eb8f3140a436503bb654726907e0d46c09f428a69d1f63b981c.jpg)



Fig. 3: Spinning sensing with dual tags

As Fig. 3 shows, the phase values of signals backscattered from tag $T _ { 1 }$ and $T _ { 2 }$ are respectively given by

$$
\theta_ {1} (t) \approx \frac {4 \pi}{\lambda} \left(d - r _ {1} \cos (2 \pi f _ {s} t + \phi_ {1})\right) \bmod 2 \pi \tag {1}
$$

$$
\theta_ {2} (t) \approx \frac {4 \pi}{\lambda} \left(d - r _ {2} \cos (2 \pi f _ {s} t + \phi_ {2})\right) \bmod 2 \pi
$$

where λ is the wavelength, $d$ is the distance between the reader and turntable center, $f _ { s }$ is the spinning frequency, $r _ { 1 }$ and $r _ { 2 }$ are distances of two tags to the turntable center. Further, $\phi _ { 1 }$ and $\phi _ { 2 }$ are the initial angles of two tags. The detailed geometric model is presented in Sec. 4. Assuming $\phi _ { 1 } = \phi _ { 2 } = 0$ , by subtracting the above two equations, we can obtain the relative phase as follows:

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} (r _ {2} - r _ {1}) \cos (2 \pi f _ {s} t) \bmod 2 \pi \tag {2}
$$

Clearly, the distance d is removed from the equation. Both $r _ { 1 }$ and r2 are constants. Thus, no mater how the reader or the turntable moves, which changes the variable $d ,$ the relative phase $\Delta \theta ( t )$ is only dependent on the spinning frequency $f _ { s }$ .

One might consider using the above relative phase as the spinning signal. Unfortunately, performing it in practice encounters three main challenges.

• First, the measured phase values are discontinuous and wrapped every time when it is over $2 \pi$ . Worsely, the measured phase values may randomly jump π radians due to the imperfection of commercial RFID reader, which is called half-wave loss [4].   
• Second, the assumption of $\phi _ { 1 } = \phi _ { 2 } = 0$ happens only when two tags are attached on a straight line which passes through the turntable center. In practice, some physical constraints do not allow to deploy tags based on a specific rule. Thus, the two equations cannot be merged simply like that.   
• Third, the relative phase is defined as the difference of two tags’ phase values acquired the two tags’ phase values at a same time point. All COTS tags are randomly and exclusively read in different time slots in order to avoid signal collisions at the reader side.

To address the above challenges, we firstly develop Relative Spinning Signal (abbreviated as $\mathbf { \ddot { \mathbf { R } } S 2 } \mathbf { \ ' }$ in the rest of our paper). We analytically demonstrate that RS2 is resilient to surrounding noise, or the shaking of the turntable and the reader even in the presence of multipath effect. Importantly, the underlying sparsity assumption that compressive reading [3] is based on still holds true. Correspondingly, we then design and implement Dual Compressive Reading (DCR) to recover RS2 using COTS RFID devices, with no extra infrastructure or pre-calibration efforts.

Contributions: In summary, this paper makes the following contributions: First, Tagtwins enhances the RFID-enabled system that makes sense of mechanical rotation within sub-hertz accuracy using dual tags’ backscatter signals. It addresses a practical problem of how to robustly sense spinning in noisy settings. Second, we propose the concept of relative spinning signal to depict the shake-resilient sensing, and mathematically demonstrate its feasibility in various real-world settings. Third, we find that previous compressive reading technique [3] can not be directly applied in our case because of the misaligned reading problem (see Sec. 6), and develop DCR approach to inspect high-frequency spinning. Fourth, we implement and evaluate our prototype with extensive experiments, demonstrating the practicality and effectiveness of our design.

TABLE 1: Comparison of existing spinning sensing approaches 

<table><tr><td></td><td>Contactless</td><td>Price</td><td>NLOS</td><td>Deployment</td><td>Accuracy</td></tr><tr><td>Accelerator</td><td>No</td><td>Medial</td><td>Not Supported</td><td>Difficult</td><td>High</td></tr><tr><td>Infrared/Laser</td><td>Yes</td><td>High</td><td>Not Supported</td><td>Difficult</td><td>Low</td></tr><tr><td>Camera</td><td>Yes</td><td>High</td><td>Not Supported</td><td>Difficult</td><td>Medium</td></tr><tr><td>Tagtwins</td><td>Yes</td><td>Low</td><td>Supported</td><td>Easy</td><td>High</td></tr></table>

# 2 RELATED WORK

We briefly review the literature that is related to our work in this section.

# 2.1 Traditional Sensing Approaches

The principle underlying typical spinning or vibration sensing techniques is to convert mechanical motion into electric pulses with or without direct contact with the spinning source. The following main categories are involved.

• Accelerator: One typical way to inspect spinning is to employ mechanical sensors to capture the force induced on the instrument and utilizes the fact that the centrifugal force on a rotating mass depends on the speed of rotation [2]. Besides, accelerometers are also sensitive to vibration because higher frequencies always exhibit greater accelerations. [5] and [6] leverage the accelerometer built within a smartwatch to track user’s hand vibration, inferring his/her inputs on keyboards possible in theory.   
• Infrared/Laser: These methods [7], [8] make sense of spinning via infrared/laser, which is then reflected by a reflective tape on the object. The rotation speed is then measured as the rate at which the light beam is reflected back. The authors in [9] demonstrate nanometer vibration analysis of a target by a selfaligned optical feedback vibrometry technique. Optical-based schema is a powerful choice when direct-contact measurement is infeasible for technical or safety reasons.   
• Camera: High-frame-rate cameras can be utilized to capture high-speed rotation, then infer its corresponding frequency. Seitz and Dyer [10] introduced a general framework for imagebased analysis of repeating motions. The authors in [11] detect and segment periodic motion based on sequence alignment without the need for camera tracking.

We summarize the advantages of Tagtwins over potential solutions in Table. 1. In particular, Tagtwins supports the contactless sensing and NLOS communication.

# 2.2 RF Sensing Approaches

A mountain of research work in RFID area has focused on location sensing in the past years [12], [13], [14], [15]. Recent advances make use of phase information of RF signals [16], [17], [18], [19]. One typical solution is Angle of Arrival (AoA), which works by measuring the phase difference between the received signals at different antennas [20], [21], [22], [23]. PinPoint [24] proposes a novel algorithm that accurately computes the line-of-sight angle of arrival, allowing multiple collaborating access points to localize interfering transmitters even under strong multi-path propagations. The authors in [25] utilize spinning tags to emulate circular antenna arrays to pinpoint target readers’ locations to a fine granularity. In addition to localization, RFID technology has also been applied to many other interesting scenarios. For example, [26] exploits the reading pattern of passive RFID tags to detect and capture customers’ shopping behaviors in physical clothing stores. Ding et al. [27] attach tags on the dumbbells and leverage the backscattered Doppler shift profile for free-weight activity recognition and assessment. RFly [28] extends the communication range in battery-free networks by leveraging drones as relays to detect objects in non-line-of-sight settings and over a wide area.

In particular, our prior work [3] makes the first attempt to inspect vibration via RFID technology, with the advantage of being low-cost and applicable to occluded and non-line-of-sight scenario. But it is not robust to the shake of device, hindering its further application in real practice. In contrast, we [29] tactfully solve this issue by employing dual tags and utilizing their relative phase as the spinning signal.

# 2.3 Other Literature on Vibration

The work [30], [31] aim to communicate small packets of information by modulating the vibrations of motors present in mobile phones. [32] extracts small vibrations caused by sound hitting an object and recovers the sound that produces them using highspeed video of the object. The authors in [33] make it possible to observe and capture a high-speed periodic video well beyond the abilities of a low-frame-rate camera. The proposed reconstruction algorithms are inspired by compressive sensing. Wei et al. [34] recover loudspeaker sound by inspecting the subtle disturbance it causes to the radio signals generated by the co-located WiFi transmitter.

# 3 OVERVIEW

This sections reviews the background of RFID systems and sketches our solution.

# 3.1 Background

Ultra-High-Frequency (UHF) RFID system consists of two actors: reader and tags. They communicate with each other using backscatter signals. Specifically, the reader transmits a high power continuous RF waves (CW). Nearby RFID tags absorb energy form CW to drive their chips and reply to the reader’s reply commands by reflecting the CW using ON-OFF keying, that is the tags transmit a ‘1’ bit or ‘0’ bit by changing or remaining the impedance on their antennas [35]. Such unique communication approach offers the subsequent two appealing features for spinning sensing:

![](images/dbfed3be88728bc617fe779662df519c2f1929a3355b3a4ec3af3bdfe82310fb.jpg)



Fig. 4: Geometric model for spinning. The clockwise rotating turntable displaces the attached tag T along a circle, resulting in varying phase shifts.

• Both energy supply and signal transmission of tags are batteryfree and based on wireless signals.   
• There is no carrier frequency offset between the reader and tags, because tags do not generate their own RF signals but rather reflect the reader’s signal [35].

# 3.2 Solution Sketch

Tagtwins is an RFID-based solution for inspecting mechanical spinning frequency of any objects. Although we present the system in the context of spinning in most of the time, Tagtwins’ technique could be applied to any other modalities of periodic mechanical motion (like vibration or pendulum). At the heart of Tagtwins is the ability to acquire spinning signals using today’s commercial off-the-shelf RFID tags. In the existing solution, the spinning signals highly depend on the relative locations of the reader and the turntable. Therefore, the development of spinning signals requires precise knowledge of how the turntable is affected by the shaking in space, which however is usually out of control.

In Sec. 4, we describe how Tagtwins resolves the above challenges to accurately develop a spinning signal even if a user shakes the turntable or the reader along unknown trajectories. In Sec. 5, we explain how Tagtwins deals with the multipath effect and works in 3D scenarios. In Sec. 6, we develop a new augmented compressive reading to recover the spinning tags through dual tags’ readings. The next few sections elaborate on the above steps, providing the technical details.

# 4 ANTI-SHAKING SPINNING SENSING

In this section, we start with the introduction of RFID-based spinning sensing with a single tag as well as its limitations, and then propose the dual-tag based solution.

# 4.1 Modeling Spinning Signal

The concept underlying spinning sensing is to develop a spinning signal which has a fundamental period or frequency as same as the spinning itself. Using RFID tag (which is attached on a turntable) for spinning sensing considers all discrete, random and low-frequency readings of the tag as samplings of the spinning

![](images/aef3e41c345835653de07aaf63899cea9b3468b0d71282409c6c15edb380ee41.jpg)



(a) Original phase sequence

![](images/ee0f288acb233da908b6b738a5b9f014af0f54b0dec264a438d1cad6a22b1f55.jpg)



(b) Refined spinning signal   
Fig. 5: Spinning signals induced by a spinning tag. (a) shows the original phase sequence θ(t), which is split into many short discontinuous fragments due to the operation of mod and half-wave loss; (b) shows the refined spinning signal s(t), which is continuous, smooth and periodic as the original one.

states. Our goal is to develop a continuous spinning signal through these readings.

The RF phase is a common parameter supported by commercial RFID readers [35]. Suppose a tag $T$ is attached on the turntable. Let $d = | R O |$ and $r = | T O |$ as sketched in Fig. 4. Then the phase shift during the spinning is defined as [4]:

$$
\theta (t) = \frac {4 \pi}{\lambda} (d - \delta (t)) + \theta_ {\mathrm{div}} \bmod 2 \pi \tag {3}
$$

where $\lambda$ is the wavelength and the term $\theta _ { \mathrm { d i v } }$ (called as diversity term) denotes the constant phase shift introduced by the device’s hardware characteristics [36]. As $\theta _ { \mathrm { d i v } }$ is a constant term which remains unchanged during the measurement, we can omit this term for simplicity. It is easy to show that its omission does not affect our subsequent derivation and the periodicity of the spinning signal. Note the total distance is $2 ( d - \delta ( t ) )$ because the signal traverses a double distance back and forth in backscatter communication. δ(t) is the function of time-varying displacement due to the spinning, which can be expressed as:

$$
\delta (t) \approx r \cos (2 \pi f _ {s} t + \phi) \tag {4}
$$

where $f _ { s }$ is the spinning frequency that we expect to inspect, and φ is the initial angle $\angle T O R$ when t = 0. Note the distance $\vert R T \vert$ is approximately equal to $| R A | \ ( R O \perp A T )$ when the reader is far away from the tag (e.g. $\left| R O \right| \gg r ) \ [ 3 7 ]$ . Substituting Eqn. 4 into Eqn. 3, we have the revised phase function:

$$
\theta (t) \approx \frac {4 \pi}{\lambda} \left(d - r \cos (2 \pi f _ {s} t + \phi)\right) \bmod 2 \pi \tag {5}
$$

From the equation, we see that the RF phase is a cosine signal which has a fundamental frequency as same as the spinning. Thus, RF phase can be considered as a raw spinning signal.

![](images/cc93489e77ef69ce54e618682d100c274528f60d9486aaed6ec51caeade5612a.jpg)



Fig. 6: Distorted spinning signal. The refined spinning signal is distorted under the unexpected translations of the reader.

# 4.2 Refining Spinning Signal

With respect to the continuity, using RF phase as spinning signal raises two issues in practice. First, the measured phase value jumps when it approaches to 0 or 2π due to the mod operation [3]. Second, COTS reader may introduce π radians of ambiguity such that the reported phase can be the true phase (θ) or the true phase plus π radians $( \theta + \pi )$ due to the half-wave loss [4]. These two issues cause the measured phase out of order. Fig. 5(a) presents an example of phase sequence which is collected in our lab. From the figure, we can see that the sequence is split up into many short discontinuous series, which goes against our analysis of their frequency or period. To address them, we transform the original phase $\theta ( t )$ to the space of sin(2θ). Then, the spinning signal, denoted as $s ( t )$ , is refined as:

$$
s (t) = \sin (2 \theta (t)) \approx \sin \left(\frac {8 \pi}{\lambda} (d - r \cos (2 \pi f _ {s} t + \phi))\right) \tag {6}
$$

Suppose the original period equals $T _ { s } ~ ( T _ { s } = 1 / f _ { s } )$ . It is easy to figure out that $s ( t + T _ { s } ) = \sin ( 2 \theta ( t + T _ { s } ) ) = \sin ( 2 \theta ( t ) ) =$ $s ( t )$ , that is, the refined spinning signal maintains the period as the original phase sequence. Meanwhile, the refined signal is also resistant to haft-wave loss (see Theorem. 1).

Theorem 1. The refined spinning signal does eliminate the $\pi \cdot$ ambiguity caused by half-wave loss.

Proof. Because sin $( 2 ( \theta ( t ) \pm \pi ) ) ~ = ~ \sin ( 2 \theta ( t ) \pm 2 \pi )$ = sin $( 2 \theta ( t ) ) , s ( t )$ has the same value no matter the reported value equals θ or $\theta \pm \pi$ . Thus, the refined spinning signal resists to half-wave loss. □

Fig. 5(b) illustrates an example of the refined spinning signal, which is much more smooth and continuous compared against the original phase sequence shown in Fig. 5(a).

# 4.3 Limitations of Single-Tag based Approach

The refined spinning signal is a good indicator to describe the spinning in quiet settings. However, such signal heavily depends on d, i.e. the distance between the reader and turntable center, as suggested in Eqn. 6. As aforementioned, it is hard to hold the distance in noisy industrial settings. Even tiny shaking of the reader or the turntable would introduce unpredictable distances. This is the reason why the prior work [3] requires a mandatory assumption that both the RFID reader and spinning source have no additional displacements except those induced by the spinning during the measurement. Further, the final received phase is derived from a combination of multiple copies of RF signals due

![](images/ddc2c0ff6e23fd3412b8110e0882f8bbfd9e48c14f37f1283648891919f78fba.jpg)



Fig. 7: Illustration of device translation in 2D. The reader translates from position R to $R ^ { \prime }$ .

to multipath effect. The measured phase value usually far deviates from the expected one. Fig. 6 shows the spinning signal acquired from a same spinning process as shown in Fig. 5(b) but under a noisy environment. Clearly, it totally cannot represent the original spinning any more. Therefore, we need to develop a more robust spinning signal.

# 4.4 Dual-Tag based Spinning Sensing Solution

We call the instability caused by either motion of devices or changes of environment as system shaking. The approach which can tolerate the system shaking is called as anti-shaking sensing. We attach dual tags on the same spinning object to achieve more robust sensing. Why could dual tags resist shaking? We begin to answer this question from line-of-sight scenario (i.e. free-space scenario), where the signal from the reader arrives along one dominate path, and then discuss it in a more complex scenario with multipath effect later.

Relative phase: For simplicity, we assume that both tags and the reader lie on a two dimensional plane (extension to 3D will be addressed later). We consider the dual tags $T _ { 1 }$ and $T _ { 2 }$ are attached on a turntable, as shown in Fig. 7. The reader situates at direction α (i.e. the angle of arrival). When the tags rotate an angle of $2 \pi f _ { s } t$ at time t, we observe $\Delta d ( t )$ translation between $R O$ and $R ^ { \prime } O$ due to the shaking of the reader or the target. Notice that here we have a reasonable assumption that the reader is at a far distance compared to the movement of devices, thus, the angle of arrival α does not change.

We can acquire the two tags’ phase values when the reader is translated to position $R ^ { \prime }$ as follows:

$$
\begin{array}{l} \theta_ {1} (t) \approx \frac {4 \pi}{\lambda} \left(d + \Delta d (t) - r _ {1} \cos (2 \pi f _ {s} t + \phi_ {1} + \alpha)\right) \bmod 2 \pi \\ \theta_ {2} (t) \approx \frac {4 \pi}{\lambda} \left(d + \Delta d (t) - r _ {2} \cos \left(2 \pi f _ {s} t + \phi_ {2} + \alpha\right)\right) \bmod 2 \pi \tag {7} \\ \end{array}
$$

To remove the common translation $\Delta d ( t )$ , we define the relative phase of the two tags (denoted as $\Delta \theta ( t ) )$ by subtracting their phase values. Since $( a - b )$ mod $c = ( a$ mod $c - b$ mod c) mod $c , \Delta \theta ( t )$ can be given by:

$$
\begin{array}{l} \Delta \theta (t) = (\theta_ {1} (t) - \theta_ {2} (t)) \bmod 2 \pi \\ \approx \frac {4 \pi}{\lambda} \left(r _ {2} \cos (2 \pi f _ {s} t + \phi_ {2} + \alpha) - r _ {1} \cos (2 \pi f _ {s} t + \phi_ {1} + \alpha)\right) \bmod 2 \pi \\ = \frac {4 \pi}{\lambda} [ (r _ {2} \cos (\phi_ {2} + \alpha) - r _ {1} \cos (\phi_ {1} + \alpha)) \cos (2 \pi f _ {s} t) \\ \left. - \left(r _ {2} \sin \left(\phi_ {2} + \alpha\right) - r _ {1} \sin \left(\phi_ {1} + \alpha\right)\right) \sin \left(2 \pi f _ {s} t\right) \right] \bmod 2 \pi \\ = \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \arctan \frac {a _ {2}}{a _ {1}}) \bmod 2 \pi \\ \end{array}
$$

where

$$
\left\{ \begin{array}{l} a _ {1} = r _ {2} \cos (\phi_ {2} + \alpha) - r _ {1} \cos (\phi_ {1} + \alpha) \\ a _ {2} = r _ {2} \sin (\phi_ {2} + \alpha) - r _ {1} \sin (\phi_ {1} + \alpha) \\ r = \sqrt {a _ {1} ^ {2} + a _ {2} ^ {2}} \end{array} \right. \tag {8}
$$

![](images/daa0f43408dbbdb9daeeb1884781e0b0e52f7d560037beb2410e3f5e4940931f.jpg)



(a) Spinning with shaking

![](images/521271309f9f6741ff2c53bbd5028d6bc107ec29f4502160a3d1c8a1147327cf.jpg)



(b) Relative spinning model   
Fig. 8: Illustration of relative spinning. (a) Although the turntable translates a lot when it is spinning, the relative distance between two tags remain unchanged. (b) From the perspective of T1, T2 appears to move around $T _ { 1 }$ in a circle. Thus, the relative phase only depends on the spinning itself instead of the shaking induced translation.

Interestingly, we find that r is actually the separated distance of two tags. Both the variables d and $\Delta d ( t )$ are removed by the subtraction, which means the relative phase at an arbitrary time is independent of either the initial position or device translation as long as the reader’s direction does not change. Eqn. 8 fully considers the initial angles of both tags when $t = 0 .$ which allows to attach tags at arbitrary positions on the turntable when they are driven by the same spinning. The relative phase can be finally converted into a cosine function with the same frequency as the spinning, like what we discuss in the single-tag scenario.

We can also understand the relative phase from another intuitive perspective. Relative to the position of $T _ { 1 }$ , the second tag $T _ { 2 }$ simply appears to move around a circle, as illustrated in Fig. 8(a). Although the turntable translates due to the shaking, the relative distance between two tags remains unchanged. In other words, two tags perform relative motion driven by the spinning instead of the shaking. In this way, we can simplify the relative phase using another equivalent model as shown in Fig. 8(b). Suppose the angle of arrival and the distance between two tags are equal to α and r respectively, then the relative phase is also given by:

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha) \bmod 2 \pi \tag {9}
$$

where $\phi$ is the initial angle between $T _ { 1 } T _ { 2 }$ and x-axis at time $t = 0$ , and r cos $( 2 \pi f _ { s } t + \phi + \alpha )$ is the saved distance of signal propagating to $T _ { 2 }$ compared with that to $T _ { 1 }$ . It is easy to prove that Eqn. 8 and Eqn. 9 are completely equivalent and convertible. We will use Eqn. 9 by default in the subsequent sections for simplicity.

Relative spinning signal: Similarly, to deal with the discontinuity of phase, we formally define the relative spinning signal (RS2) as below:

$$
s (t) = \sin (2 \Delta \theta (t)) = \sin (2 \theta_ {1} (t) - 2 \theta_ {2} (t)) \tag {10}
$$

$\theta _ { 1 }$ and $\theta _ { 2 }$ are measured phase values of two tags in practice. One might wonder if the periodicity generated by the above equation is indeed maintained as that of the actual spinning. In fact, it is easy to observe from Eqn. 10 that $s ( t + T _ { s } ) = \sin ( 2 \Delta \theta ( t + T _ { s } ) ) =$ sin $( 2 \Delta \theta ( t ) ) ~ = ~ s ( t )$ . We can also intuitively understand such conclusion from Fig. 8. The only movement that drives $T _ { 2 }$ to rotate around $T _ { 1 }$ is the spinning of the turntable.

![](images/bccc06876eab98669f65988b131c0fdc2aac8daf945a8c03fa8c74bcd8d0e145.jpg)



Fig. 9: Multipath scenario. The signal coming from reader propagates through two different paths with different directions and distances due to reflectors.

# 4.5 Put Things Together

The discussion so far focuses on the design of anti-shaking spinning sensing. The solution utilizes the relative spinning signals of two tags derived by a same spinning source to identify the characteristics of the spinning itself. We have proved that the RS2 is independent on the location of turntable and its translations during the measurement, namely being anti-shaking or translationresistant.

# 5 DISCUSSIONS

In this section, we concentrate on two main issues: the impact of multipath effect and the usage in 3D scenario.

# 5.1 Impact of Multipath Effect

Our discussion so far has involved line-of-sight scenarios. Here, we extend to multipath environment, showing RS2 continues to be resistant to shaking. As aforementioned, no matter how the reader or turntable shakes, the final effect is equivalent to the relative spinning that $T _ { 2 }$ rotates around $T _ { 1 }$ . Here, we also employ such model to show how the multipath propagation affects the relative spinning signal. As shown in Fig. 9, suppose the wireless signal propagates along K different paths to arrive at $T _ { 1 }$ with initial lengths $d _ { 1 } , d _ { 2 } , \dots , d _ { K }$ , along directions ${ \alpha } _ { 1 } , { \alpha } _ { 2 } , \ldots , { \alpha } _ { K }$ . Finally, these copies of signals are overlapped at each tag. It is known that nearby RFIDs will experience a similar multipath environment [23]. Here we assume dual tags are close to each other (less than half wavelength), then these copies of signals will be overlapped at each tag. From basic channel models, we can write the wireless channel $h _ { i }$ arrived at tag $T _ { i } ~ ( i = 1 , 2 )$ as the complex number [38]:

$$
h _ {i} (t) = \frac {1}{d ^ {2} (t)} e ^ {\mathbf {J} \theta (t)} \tag {11}
$$

where $d ( t )$ and $\theta ( t )$ are the distance and phase shift at time t. We can then get the overlapped RF signals at $T _ { 1 }$ and $T _ { 2 }$ as follows:

$$
h _ {1} (t) \approx \sum_ {\substack {k = 1 \\ K}} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} d _ {k}} \tag{12}
$$

$$
h _ {2} (t) \approx \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {k} - r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k}))}
$$

where $d _ { k }$ is the distance from the reader to $T _ { 1 }$ through the $k ^ { t h }$ propagation path, and r cos $\left( 2 \pi f _ { s } t + \phi + \alpha _ { k } \right)$ is the saved distance to $T _ { 2 }$ compared with $T _ { 1 }$ . Then we compute the relative wireless channel $h ( t ) = h _ { 1 } ( t ) h _ { 2 } ^ { \ast } ( t )$ :

![](images/336eadd34ced995b5418c061ae795ab80b965918613ac6d8da1803c3de1e78ad.jpg)



Fig. 10: 3D scenario. α and $\beta$ denote the azimuthal and polar angle respectively.

$$
\begin{array}{l} h (t) = \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} d _ {k}} \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {- \mathbf {J} \frac {4 \pi}{\lambda} \left(d _ {k} - r \cos \left(2 \pi f _ {s} t + \phi + \alpha_ {k}\right)\right)} \tag {13} \\ = \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k})} \left[ \frac {1}{d _ {k} ^ {2}} + \sum_ {l \neq k} \frac {1}{d _ {l} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {l} - d _ {k})} \right] \\ \end{array}
$$

Notice that the phase of the first term, i.e. $\begin{array} { r } { \frac { 4 \pi } { \lambda } r \cos ( 2 \pi f _ { s } t + \phi + } \end{array}$ $\alpha _ { k } )$ , in the above equation is nearly identical to the relative phase in Eqn. 9 derived in the line-of-sight scenario, and is independent of any translation. Unfortunately, the second term indeed depends on the distances. However, two observations inspire us: First, if the environment remains constant $( i . e .$ ., multiple propagations hold), the second term reduces to a constant multiplier, which merely scales the final phase value. Second, even if the environment changes or the shaking changes the propagations, any variance or noise caused by the second term drops significantly when summing over all multipath propagations. More formally, the following theorem holds:

Theorem 2. The phase of the relative channel $h ( t )$ in Eqn. 13 is independent of multipath distances $d _ { 1 } , d _ { 2 } , \dots , d _ { K }$ .

Proof. From Eqn. 13 we have

$$
\begin{array}{l} h (t) = \sum_ {k = 1} ^ {K} \frac {1}{d _ {k} ^ {4}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k})} \\ + \underbrace {\sum_ {k = 1} ^ {K} \sum_ {l \neq k} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k})} \frac {1}{d _ {k} ^ {2}} \frac {1}{d _ {l} ^ {2}} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {l} - d _ {k})}} _ {②} \\ ② \approx \sum_ {k = 1} ^ {K} \sum_ {l > k} e ^ {\mathbf {J} \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha_ {k})} \frac {1}{d _ {k} ^ {2} d _ {l} ^ {2}} \underbrace {\left(e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {l} - d _ {k})} + e ^ {\mathbf {J} \frac {4 \pi}{\lambda} (d _ {k} - d _ {l})}\right)} _ {③} \\ \end{array}
$$

Since the phase of $\textcircled{3}$ is 0, the phases of $\textcircled{2}$ and further $h ( t )$ are both independent of distance variable $d _ { k }$ .

The relative phase relates only with the spinning itself as long as the multipath angle of arrival $\alpha _ { k }$ maintains. So the above observations show that RS2 is resistant to shaking even in multipath scenarios. This property holds no mater how the turntable or the reader is shaken. Even so, we must stress that shaking-induced translation cannot be unbounded and must be relatively small compared to the distance between the turntable and the reader, even if the reader/turntable shakes moderately. This is not a harsh assumption and can be easily met in practice as validated in our evaluation.

# 5.2 Extending to Three Dimensional Scenario

Let us now consider the RS2 in 3D space. The spinning surface is considered as the x-y plane (i.e. horizontal plane), while the reader may not lie on this plane. In this way, apart from the azimuthal angle α in the horizontal plane, we also need another parameter, $i . e .$ the polar angle $\beta$ along the vertical direction to fully describe the reader’s incident signal, as depicted in Fig. 10. Correspondingly, the relative phase in 3D is given by:

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} r \cos (2 \pi f _ {s} t + \phi + \alpha) \sin \beta \bmod 2 \pi \tag {14}
$$

Apparently, even generalizing to three dimensions, the RS2 depends only on the reader’s spatial orientation instead of its movement. Notice, such a generalization is crucial because we can not require and restrict the reader and object to perfectly stay on a two dimensional plane during the whole spinning in practice.

# 5.3 Effect from Changes in Surrounding Environment

Surrounding rotational objects or obstacles in practical industrial settings could affect the RF signals of tags attached on our target object. As we mentioned before, as long as the dual tags are close enough, they will both experience a similar multipath environment or propagation model. Thus, either motions or changes of surrounding environment will also have similar impact on the two tags concurrently no matter the changing pattern is periodic or not. Let $\delta _ { 1 } ( t )$ and $\delta _ { 2 } ( t )$ denote the time-varying phase changes at time t on two tags respectively due to the changes of surroundings. Then the dual tags’ phase models are sketched as below

$$
\begin{array}{l} \theta_ {1} (t) \approx \frac {4 \pi}{\lambda} \left(d + \Delta d (t) - r _ {1} \cos (2 \pi f _ {s} t + \phi_ {1} + \alpha)\right) + \delta_ {1} (t) \bmod 2 \pi \\ \theta_ {2} (t) \approx \frac {4 \pi}{\lambda} \left(d + \Delta d (t) - r _ {2} \cos (2 \pi f _ {s} t + \phi_ {2} + \alpha)\right) + \delta_ {2} (t) \bmod 2 \pi \\ \end{array}
$$

Then we could derive the relative phase as

$$
\Delta \theta (t) = \frac {4 \pi}{\lambda} r \cos \left(2 \pi f _ {s} t + \arctan \frac {a _ {2}}{a _ {1}}\right) + \delta_ {1} (t) - \delta_ {2} (t) \bmod 2 \pi \tag {15}
$$

The term of $a _ { 1 }$ and $a _ { 2 }$ could refer to Eqn. 8. Since two tags are close to each other, $\delta _ { 1 } ( t ) \approx \delta _ { 2 } ( t )$ or $\delta _ { 1 } ( t ) - \delta _ { 2 } ( t ) \approx 0$ . Clearly, the impact from dynamic surroundings are counteracted finally.

In summary, the accuracy of Tagtwins can hardly be affected by surrounding environment if the pair of RFIDs are placed near each other.

# 6 ENHANCED COMPRESSIVE READING

This section begins with the practical challenges we face when applying relative spinning signal in spinning sensing, and then presents the solution to address these challenges.

Challenges. Making sensing of spinning or vibration using RFID tags is to inspect the motion through the random and lowfrequency readings of tags, where each reading is viewed as one sampling of motion status. A COTS tag can be read for about 40 times per second on average (i.e., sampling frequency equals 40Hz). As stated by the Nyquist-Shannon sampling theorem, for a given analog signal of bandlimit, the sampling rate should be at least twice the highest frequency contained in the signal in order to guarantee perfect reconstruction of the original signal.

![](images/e44a1abf6c5bf7d1617232b6af1b3b029ba36b6ad9f44fd6f063f3593184ed29.jpg)



Fig. 11: Illustration of compressive reading [3]. It involves two components, signal model and measurement model.

Thus, Tagtwins is able to recover spinning signal with up to 20Hz frequency according to the sampling theorem, which obviously can not meet practical needs in most applications. Therefore, the central task of applying RS2 is to recover the spinning signal, even high-frequency signal (> 20Hz), through the random and discrete readings.

# 6.1 Classic Compressive Reading

The work [3] utilizes compressive sensing technique to recover the spinning signal which is derived from a single tag (see Eqn. 6). This approach is called as Compressive Reading (CR), which contains two components as shown in Fig. 11:

Signal model: Compressive sensing states that the sparsity of a signal can be exploited to perfectly reconstruct it from far fewer samples than required by the sampling theorem, if one can randomly measure linear combinations of the signal. Since the time-domain spinning signal is periodic, it has a very sparse representation in the frequency domain, where it can be represented into a sum of phasors via the exponential Fourier series. CR first converts the spinning signal into the frequency domain through Fourier transform:

$$
S = \boldsymbol {\Psi} s \quad \text { or } \quad s = \boldsymbol {\Psi} ^ {- 1} S \tag {16}
$$

where the matrix Ψ is the Fourier basis and S is the sparse coefficient vector in Fourier domain.

Measurement model. The compressive sensing requires to schedule the sampling based on a random measurement matrix that is generated in advance. As we know, commercial RFID readers adopt the Q-adaptive algorithm to prevent tag collisions. There is no way to schedule the reading in the physical layer at a specific time point, namely, it fails to sampling based a planed measurement matrix. Utilizing this inherent randomness of tag’s readings, CR is able to construct the measurement matrix denoted by Φ and corresponding result y. Specifically, CR discretizes the total read time into N basic time slots, $\left\{ t _ { 1 } , \ t _ { 2 } , \ . . . , t _ { N } \right\}$ , at millisecond level. Each reading (or sampling) only occurs within a time slot. The left side of Fig. 11 illustrates the structure of matrix Φ. The matrix contains $M \times N$ elements and each row corresponds to the timeline from $T _ { 1 } ~ \mathrm { t o } ~ T _ { N }$ . We aggregate Q time slots into a read frame. Each row involves one read frame and the adjacent frames are staggered in two different rows. In this way, there are totally $M = \lceil N / Q \rceil$ frames and rows. Formally, the $m ^ { t h }$ read frame starts at the $( ( m - 1 ) Q + 1 ) ^ { t h }$ time slot and ends at the $( m Q ) ^ { t h }$ time slot in the $m ^ { t h }$ row. The elements in the matrix are set to 0 $( e . g .$ . blank grid) or 1 (e.g. green grid). If $\Phi [ m , n ] = 1$ , it implies that the tag was read at the $n ^ { \mathit { \bar { t } h } }$ time slot and within the $\hat { m } ^ { t h }$ frame. Otherwise, $\Phi [ m , n ] = 0$ implies

![](images/b951a926ad54d700c2f61e1deffff8ae2a0b76c69d5c99787e6b2155f2696da1.jpg)



Fig. 12: Construction of measurement matrix and result. As the tag is read at the first, third, fourth and sixth millisecond, the measurement matrix and result are constructed as above.

that the tag was not read in the $n ^ { t h }$ time slot or the $n ^ { t h }$ slot is beyond the $m ^ { t h }$ frame. Let $N \times 1$ dimension vector y be the measurement result. The element y[m] is the aggregated result of the $m ^ { t h }$ frame, which is defined as follows:

$$
y [ m ] = \sum_ {n = 1} ^ {N} \Phi [ m, n ] s [ n ] \tag {17}
$$

Since $\Phi [ m , n ]$ is either 0 or $1 , y [ m ]$ is actually the sum of the values of the spinning signal sampled in the $m ^ { t { \dot { h } } }$ frame. Overall, the measurement model can be given by:

$$
y = \Phi s + \eta \tag {18}
$$

where η represents the measurement noise.

Put it together. Combing Eqn. 16 and Eqn. 18 reveals the subsequent equation:

$$
y = \Phi s + \eta = \Phi \Psi^ {- 1} S + \eta \tag {19}
$$

where Ψ is the measurement matrix, y is the sampling result, and η denotes the measurement noise. Note that the spinning signal derived by a single tag is defined in Eqn. 6 instead of the original phase value. To visually understand the measurement matrix and result, we illustrate an example in Fig. 12. Finally, the signal could be reconstructed reliably through solving an $l _ { 1 }$ or l2 optimization problem. One of the great advantages of CR is that it constructs the measurement matrix based on the collected readings, rather than builds it in advance and then guides the reader’s reading. This allows us to employ COTS readers for sensing without any modification.

# 6.2 Dual Compressive Reading

At first glance, we can employ CR to respectively recover two spinning signals induced by dual tags and then subtract them to obtain the final relative spinning signal. Unfortunately, this naive solution fails because neither of two spinning signals is periodic and sparse, as shown in Fig. 2(b), although their relative value is sufficiently compact in the frequency domain. Thus, we have to directly recover the relative spinning signal. Our approach is called as Dual Compressive Reading (DCR). Being different from CR, DCR has two input sequences in dual-tag systems as follows:

$$
\left. \right.\left\{\left(t _ {1, 1}, \theta_ {1} \left[ t _ {1, 1} \right]\right), \left(t _ {1, 2}, \theta_ {1} \left[ t _ {1, 2} \right]\right), \dots , \left(t _ {1, M _ {1}}, \theta_ {1} \left[ t _ {1, M _ {1}} \right]\right)\right\} \tag {20}
$$

$$
\left\{\left(t _ {2, 1}, \theta_ {2} [ t _ {2, 1} ]\right), \left(t _ {2, 2}, \theta_ {2} [ t _ {2, 2} ]\right), \ldots , \left(t _ {2, M _ {2}}, \theta_ {2} [ t _ {2, M _ {2}} ]\right) \right\}
$$

which are collected from two tags respectively. Similar to Eqn. 18, each element of the measurement result vector is given by

$$
y [ m ] = \sin (2 \Delta \theta (t)) = \sin (2 (\theta_ {1} [ t _ {m} ] - \theta_ {2} [ t _ {m} ])) \tag {21}
$$

This equation indicates that the $m ^ { t h }$ result element equals the phase difference of two tags measured at time $t _ { m }$ .

![](images/3299b6fba624c04f613259d0f2e0ef226ac9787e6d7b6908bec070ac48c093a2.jpg)



(a) Timestamp misalignment

![](images/3a925b8706b8b29db722e24fd4bac43edd38f1c50c054008fa59442ac45ad5df.jpg)



(b) The distribution of time interval   
Fig. 13: Empirical study on dual tags’ readings. (a) shows the reading time of two tags are misaligned. (b) shows two tags are closely read within 3ms in most of the time.

Dealing with misaligned reading. Everything looks like going well so far. Unfortunately, the above phase difference cannot be obtained in practice because tags are exclusively read in a timesharing fashion. In other words, it is impossible for us to read two tags’ phase values simultaneously at a specific time point. We call this problem misaligned reading, as shown in Fig. 13(a). Each bar indicates one read and black and red correspond to different tags. With more observations from Fig. 13(a), we come to an important fact that the measurements have the property of readtime locality, which means two tags are quite closely read although they are read alternatively. Such locality stems from the fact that the whole reading is composed of numerous inventory rounds, within each of which two tags must be read once. Each inventory lasts very short, making the reading time of two tags very close. To validate such observation, we persistently read the two tags for 100, 000 times and then calculate the interval of two tags’ adjacent readings. The interval distribution is shown in Fig. 13(b). Not surprisingly, we find the interval has a mean value of 2.3ms. Compared against the 1ms resolution of timestamp, two tags are almost read concurrently during each inventory.

Driven by the above conclusion, we employ Gaussian Interpolation to align the two phase sequences. Now our problem turns into: how to estimate the phase values of $T _ { 1 }$ (or $T _ { 2 } )$ at timestamps of $\left\{ t _ { 2 , 1 } , \ldots , t _ { 2 , M _ { 2 } } \right\}$ (or $\{ t _ { 1 , 1 } , \dotsc , t _ { 1 , M _ { 1 } } \} ) \colon$ Given a timestamp $t _ { 2 , i } ( i = 1 , \dots , M _ { 2 } )$ , we first choose $L$ phase values of $T _ { 1 }$ whose timestamps are most close to $t _ { 2 , i }$ (according to the read-time locality property). Then,

$$
\theta_ {1} [ t _ {2, i} ] = \sum_ {l = 1} ^ {L} w _ {l} \theta_ {1} [ t _ {l} ] \tag {22}
$$

where $w _ { l }$ is the weight from Balckman window and $\theta _ { 1 } [ t _ { l } ]$ is the ${ { l } ^ { t h } }$ chosen phase value. The similar process is performed for tag $T _ { 2 }$ . In this way, we will totally obtain $M _ { 1 } + M _ { 2 }$ phase values for each tag. Once the two tags’ measurements get aligned, we can thereby compute the result vector y through Eqn. 21.

Period Searching. Finally, we utilize compressive reading over two interpolated phase sequences to recover the relative spinning signal s. The fundamental frequency or period we want to inspect can also be obtained from the frequency spectrum of the recovered signal or using other fast folding approaches as mentioned in [3].

![](images/ed9849f19723aecee6b19c280119801e51c9140c9660551bca409760bf3ab141.jpg)



Fig. 14: Experimental setup

# 7 IMPLEMENTATION AND EVALUATION

In this section, we introduce the implementation and conduct many experiments that provide insight into the working of the system, with the spinning of a controllable turntable, as detailed below.

# 7.1 Implementation

We implement Tagtwins using COTS UHF reader and tags and conduct performance evaluation in our lab environment as shown in Fig. 14.

Hardware: We adopt an Impinj Speedway R420 reader [39] which is compatible with EPC Gen2 standard and operates during the frequency band of 920.5 ∼ 924.5 MHz by default. The reader is connected to our host end through Ethernet. One reader antenna with circular polarization and 8dBi gain is employed, whose size is 225mm × 225mm × 33mm. Totally four types of tags from Alien Corp [40], modeled $^ { 6 6 } 2 \times 2 ^ { , 3 }$ , “Square”, “Squig” and “Squiggle” are employed.

Software: Our implementation involves the LLRP (Low Level Reader Protocol) [41] to communicate with the reader. Impinj readers extend this protocol to support the phase report. We adjust the configuration of reader to immediately report its readings whenever tags are detected. The client software is implemented using Java (for network connection) and Matlab (for signal processing). We use a Samsung PC to run our algorithms, as well as connect to the reader under LLRP. The machine equips Intel Core i7 CPU at 2.4GHz and 8G memory.

Experimental Setup. Two RFID tags are attached on a rotating machine, whose frequency can range from 0 to 2, 100 RPM. They are separated by a distance of 5cm and their distance to the antenna is set to 2m by default. We collect the ground truth of frequency by utilizing a laser tachometer, which can measure RPM (Revolutions Per Minute) from a reflective target using a laser light source. Fig. 14 shows the experimental setup.

# 7.2 Providing Insight to Tagtwins

We start with a microbenchmark experiment to provide insights into the working of our system. To better understand how Tagtwins is resistant to device shaking, we collect the signals of two tags and their relative spinning signal when we randomly shake the reader antenna in a to-and-fro way. Fig. 15(a) and Fig. 15(b) respectively shows the refined spinning signals of two tags. It is clear that the two spinning signals are seriously distorted due to the shaking of the device. We cannot visually inspect the periods of the original spinning at all. On the contrary, Fig. 15(c) shows the relative spinning signal of the two tags, which becomes far more regular. It well reveals the intrinsic spinning frequency as expected, compared with the spinning signal purely collected from each tag. Hence, it is reasonable and feasible that we utilize RS2 to reflect and inspect the frequency of a spinning object.

![](images/9f62ede38db2843b277fd69871a8addc051f5790a60923643c58225ec9122610.jpg)



(a) Signal on the first tag

![](images/1901237466218acd651fdb56020829a65e0e6df8a521cdfe292e1ba483789e03.jpg)



(b) Signal on the second tag

![](images/202acbdb22a9e93ded91045d45e8ef4b34951f709c124f11ea543c2a0da470b9.jpg)



(c) Relative spinning signal   
Fig. 15: Spinning signals. It is difficult to see the periodicity on the received phase sequence at the two tags. Performing the subtraction between two phase values on two tags, reveals the periodic and well aligned spinning signal.

![](images/01fc229f0649fc4b1d2a239b039478c3786779f76d3291ec7164e4dfd07cc79a.jpg)



(a) Linear to-and-fro trajectory

![](images/0f6e1ee5ef25be72c400377d3d37019fb7a30aef7f7cffac80de7b4c329e21b1.jpg)



(b) Arc-shaped trajectory

![](images/fd11d00cfe9ed328c7bbd84876c7ed37b4f46b17bee1a0d0189649cb20d4fc22.jpg)



(c) Arbitrary shaped trajectory

![](images/253bfe65529408ae2d7f186cf00d3fabfe4c1a396319ad184609829f7dc390c0.jpg)



(d) Circular shake of object

![](images/4430c9f6705f541190423a57a099a3e9e76a5874d763363b63a792334fd40be7.jpg)



(e) Tracking accuracy   
Fig. 16: Tracking accuracy under different noisy settings. (a)-(d) show the different trajectories of the turntable; (e) shows the tracking accuracy corresponding to the above settings.

# 7.3 Accuracy Under Various Settings

Method: As is mentioned before, the biggest advantage of our system over prior work [3] is that it can still work well even in quite noisy settings. To gain an intuitive impression on Tagtwins’ anti-shaking sensing accuracy, we randomly shake the reader antenna along the following kinds of trajectories: (a) three dimensional linear to-and-fro trajectory (see Fig. 16(a)); (b) three dimensional arc-shaped trajectory (see Fig. 16(b)); (c) random arbitrary shaped trajectory (see Fig. 16(c)); (d) translation along a circle (see Fig. 16(d)). All of these shakes are performed up to a range of 30cm artificially. Besides, in view of the case that the spinning object shakes, we utilize an orbital shaker to automatically shake the turntable along a restricted circular orbit with different speeds (see Fig. 14). We plot the shaking traces of the four aforementioned categories collected in our experiments in Fig. 16. As a comparison study, we also consider the situation where both the antenna and turntable remain motionless.

Results: We compare the performance of Tagtwins against Tagbeat, which is not resistant to device translation. Fig. 16(e) plots the sensing errors in frequency. We find that both Tagtwins and Tagbeat achieve high precision (around 0.2Hz) if the equipment does not move during the experiment. However, if either the reader or the object observes some level of translation, even in a slight way, the accuracy of Tagbeat will be affected severely, dropping to more than 7Hz. That is where our system wins out. In general, Tagtwins achieves a mean error of 0.27Hz in frequency with the standard deviation of 0.53Hz, corresponding to 0.43ms error in period, which is fairly good and can even rival those of specialized tachometers.

In a typical motor fault detection scenario for example, the engine usually has an idle speed (the rotational speed an engine runs at when it is idling [42]) of 600 ∼ 1, 500 RPM (i.e., 10 ∼ 25Hz), our error ratio could lead to a sub-hertz accuracy, which is sufficient for the fault detection demand. Generally speaking, Tagtwins is applicable to applications with no more than 100Hz (about 6, 000 RPM) revolving speed. Besides, since Tagtwins utilizes RF signals to inspect rotation, it may fail in extreme situations where the reader can not get tags’ any replies. In such complicate environment, we would advise to use the antimetal RFID tags [43], which are made of special materials like ceramics and trickily designed in circuits.

# 7.4 Accuracy vs. Different Parameters

We further discuss the following factors that may have an influence on Tagtwins’ performance.

![](images/1f2e21ed39b7f824aee15b180f2dd31102ca7771e2aea6a4c36b729d87a8a33c.jpg)



(a) Impact of spinning speed

![](images/0af5a396e21321b097c81fba50a7c7032538bbb5561791e73b16bc084951163a.jpg)



(b) Impact of radius

![](images/417069651a58558707f964affb3b44261b2862735bcbb78d63bce9bd6e9f5e47.jpg)



(c) Impact of distance

![](images/749f45c47793717817573c12004fe377f75a5a981c417fbeac9ebb1bd8db379c.jpg)



(d) Impact of diversity   
Fig. 17: Tracking accuracy vs. different parameters

Accuracy vs. Spinning Speed. To check Tagtwins’ effectiveness under high frequency scenario, we tune the revolving speed of the turntable from 670 to 2, 067 RPM with seven levels. For each setting, we repeat the experiment for 50 times and Fig. 17(a) depicts the averaged results. It can be seen that the mean errors among various RPMs have little difference, from the minimum of 0.08Hz to the maximum of 0.42Hz. And the result is more accurate when the object spins at a low speed, which is reasonable because more samples in one period can be collected for recovering.

Accuracy vs. Radius. As mentioned before, we have no requirement of the dual tags’ geometric relationship as long as their separation is fixed. We then set this separation to 3cm, 5cm and 8cm respectively while keeping the same RPM and plot the recovered signals in Fig. 17(b). We observe from this figure that although the three signals vary a lot in pattern, their periods keep consistent (i.e. about 57ms). The averaged sensing accuracy is 0.10Hz, 0.19Hz and 0.28Hz in these three settings. In our experimentation, we choose the dual-tag distance as 5cm by default.

Accuracy vs. Distance. Commercial RFID products can support a reading range of 6 ∼ 7 meters in indoor environment, so we change the distance between reader antenna and spinning object from 0.5m to 5m. Fig. 17(c) shows the accuracy with different distances. We have the following observations: (a) The performance achieves the best when the distance equals 1.5m. (b) When the antenna is too close to the tags, i.e. less than 0.5m, the accuracy will drop. Recall that we have a premise that the antenna and turntable should have a relatively large distance compared to their movement, and this premise will be broken if the antenna gets near the turntable (e.g., distance is below two wavelengths, about 64cm). Thus, shaking-induced translation can not be well handled by our relative signal, leading to more errors. (c) The performance also decreases when the antenna is too far from the tags, i.e. more than 5m. This is understandable because a larger distance will result in a lower reading rate, which means fewer samples are collected. In summary, we suggest a distance of 1m to 3m according to our empirical study.

Accuracy vs. Diversity. We experiment on four models of tags, namely “2 × 2”, “Square”, “Squig” and “Squiggle” to study the influence of tag diversity. All these tag types have different antenna sizes and shapes as depicted in Fig. 17(d). For each tag model, the result is averaged from 50 experiments with the same setting. We find that although the errors of all models maintain at a small value (less than 0.6Hz), there exist some differences among them. 2 × 2, Squig and Squiggle have very close accuracy (i.e., 0.28Hz, 0.25Hz and 0.30Hz respectively), while Square model observes a lower accuracy of 0.61Hz with a higher standard deviation of 0.43Hz. This can be explained by the size of tag’s antenna, because Square has a more compact volume (only 22.5mm × 22.5mm) compared with the other three types. Generally speaking, the tag with larger antenna could absorb more energy from the reader, making its backscattered signal stronger (i.e. higher SNR) and thereby outputting more precise sensing result. In our experimentation, we use model “Squig” in most cases.

# 7.5 Accuracy in Multipath Environment

One prominent advantage of utilizing RFID to sense spinning over prior approaches is that it can work either in the absence of lineof-sight (LOS) or the presence of rich multipath. To investigate this, we perform evaluation in two typical settings: (a) a clear freespace environment with no multipath effect; (b) a non-line-of-sight (NLOS) or strong multipath scenario with obstacles between (or around) the turntable and reader. For each setting, we carry out

![](images/810193bbc682d45fe5015666196a598ad1aa04c78f17ca8ed550f75ef2ab4f9b.jpg)



Fig. 18: Tracking accuracy in LOS & NLOS

50 experiments and plot the CDF of frequency error in Fig. 18. It is clear that the overall accuracy in LOS is better than that in NLOS. The mean error is 0.32Hz with 90% below 0.54Hz in LOS scenario while that of NLOS is 0.79Hz with 90% below 2.1Hz. Since more paths will arrive at the two tags in NLOS scenario instead of one dominant path, the error is accumulated along these paths. Besides, the reflected signal will traverse a longer path compared to the direct one, impairing the signal strength. Even the accuracy drops a little in NLOS environment, it still overwhelms many traditional instruments like laser which fails in such condition.

# 8 CONCLUSION

This work presents an RFID-based spinning sensing system that is robust to noisy settings. Our key innovations lie in leveraging the relative signal of dual RFID tags to resist the system shaking and proposing a new form of compressive reading technique to recover the relative signal. Experimental results demonstrate that Tagtwins can make sense of the rotation frequency to an accuracy of subhertz with strong robustness. We believe our system will promote more possibilities of RFID-based sensing solution in practical deployments.

# ACKNOWLEDGMENT

The research of Lei Yang is partially supported by ECS (NO. 25222917), NSFC General Program (NO. 61572282), and Alibaba Innovation Research. The research of Lei Xie is partially supported by NSFC (No. 61472185), and JiangSu Natural Science Foundation (No. BK20151390).

# REFERENCES

[1] Y. Lei, Z. He, and Y. Zi, “Application of an intelligent classification method to mechanical fault diagnosis,” Expert Systems with Applications, vol. 36, no. 6, pp. 9941–9948, 2009.   
[2] “Lion Precision,” http://www.lionprecision.com/.   
[3] L. Yang, Y. Li, Q. Lin, X.-Y. Li, and Y. Liu, “Making sense of mechanical vibration period with sub-millisecond accuracy using backscatter signals,” in Proc. of ACM MobiCom, 2016.   
[4] ImpinJ, “Speedway revolution reader application note: Low level user data support,” in Speedway Revolution Reader Application Note, 2010.   
[5] X. Liu, Z. Zhou, W. Diao, Z. Li, and K. Zhang, “When good becomes evil: Keystroke inference with smartwatch,” in Proc. of ACM CCS, 2015.   
[6] H. Wang, T. T.-T. Lai, and R. Roy Choudhury, “Mole: Motion leaks through smartwatch sensors,” in Proc. of ACM MobiCom, 2015, pp. 155– 166.

[7] P. Castellini, M. Martarelli, and E. P. Tomasini, “Laser doppler vibrometry: Development of advanced solutions answering to technology’s needs,” Mechanical Systems and Signal Processing, vol. 20, no. 6, pp. 1265–1285, 2006.   
[8] P. Cheng, M. S. M. Mustafa, and B. Oelmann, “Contactless rotor rpm measurement using laser mouse sensors,” IEEE Transactions on Instrumentation and Measurement, vol. 61, no. 3, pp. 740–748, 2012.   
[9] K. Otsuka, K. Abe, J.-Y. Ko, and T.-S. Lim, “Real-time nanometervibration measurement with a self-mixing microchip solid-state laser,” Optics letters, vol. 27, no. 15, pp. 1339–1341, 2002.   
[10] S. M. Seitz and C. R. Dyer, “View-invariant analysis of cyclic motion,” International Journal of Computer Vision, vol. 25, no. 3, pp. 231–251, 1997.   
[11] I. Laptev, S. J. Belongie, P. Perez, and J. Wills, “Periodic motion detection and segmentation via approximate sequence alignment,” in Proc. of IEEE ICCV, 2005.   
[12] J. Wang, H. Hassanieh, D. Katabi, and P. Indyk, “Efficient and reliable low-power backscatter networks,” in Proc. of ACM SIGCOMM, 2012, pp. 61–72.   
[13] M. Scherhaufl, M. Pichler, and A. Stelzer, “Localization of passive UHF RFID tags based on inverse synthetic apertures,” in Proc. of IEEE RFID, 2014.   
[14] Q. Lin, L. Yang, Y. Sun, T. Liu, X.-Y. Li, and Y. Liu, “Beyond one-dollar mouse: A battery-free device for 3d human-computer interaction via rfid tags,” in Proc. of IEEE INFOCOM, 2015.   
[15] T. Liu, Y. Liu, L. Yang, Y. Guo, and C. Wang, “Backpos: High accuracy backscatter positioning system,” IEEE Transactions on Mobile Computing, vol. 15, no. 3, pp. 586–598, 2016.   
[16] J. Wang, D. Vasisht, and D. Katabi, “Rf-idraw: virtual touch screen in the air using rf signals,” in Proc. of ACM SIGCOMM, 2014.   
[17] L. Yang, Q. Lin, X. Li, T. Liu, and Y. Liu, “See through walls with cots rfid system!” in Proc. of ACM MobiCom, 2015.   
[18] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Relative Localization of RFID Tags using Spatial-Temporal Phase Profiling,” in Proc. of USENIX NSDI, 2015.   
[19] C. Duan, X. Rao, L. Yang, and Y. Liu, “Fusing rfid and computer vision for fine-grained object tracking,” in Proc. of IEEE INFOCOM, 2017.   
[20] Y. Zhang, M. G. Amin, and S. Kaushik, “Localization and tracking of passive rfid tags based on direction estimation,” International Journal of Antennas and Propagation, 2007.   
[21] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, “New measurement results for the localization of UHF RFID transponders using an angle of arrival (AoA) approach,” in Proc. of IEEE RFID, 2011.   
[22] J. Xiong and K. Jamieson, “Arraytrack: A fine-grained indoor location system.” in Proc. of USENIX NSDI, 2013.   
[23] J. Wang and D. Katabi, “Dude, where’s my card?: Rfid positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[24] K. R. Joshi, S. S. Hong, and S. Katti, “Pinpoint: Localizing interfering radios.” in Proc. of USENIX NSDI, 2013, pp. 241–253.   
[25] C. Duan, L. Yang, and Y. Liu, “Accurate spatial calibration of rfid antennas via spinning tags,” in Proc. of IEEE ICDCS, 2016.   
[26] Z. Zhou, L. Shangguan, X. Zheng, L. Yang, and Y. Liu, “Design and implementation of an rfid-based customer shopping behavior mining system,” IEEE/ACM Transactions on Networking, vol. 25, no. 4, pp. 2405–2418, 2017.   
[27] H. Ding, L. Shangguan, Z. Yang, J. Han, Z. Zhou, P. Yang, W. Xi, and J. Zhao, “Femo: A platform for free-weight exercise monitoring with rfids,” in Proc. of ACM SenSys, 2015.   
[28] Y. Ma, N. Selby, and F. Adib, “Drone relays for battery-free networks,” in Proc. of ACM SIGCOMM, 2017.   
[29] C. Duan, L. Yang, H. Jia, Q. Lin, Y. Liu, and L. Xie, “Robust spinning sensing with dual-rfid-tags in noisy settings,” in Proc. of IEEE INFO-COM, 2018.   
[30] N. Roy, M. Gowda, and R. R. Choudhury, “Ripple: Communicating through physical vibration,” in Proc. of USENIX NSDI, 2015.   
[31] N. Roy and R. R. Choudhury, “Ripple ii: Faster communication through physical vibration,” in Proc. of USENIX NSDI, 2016.   
[32] A. Davis, M. Rubinstein, N. Wadhwa, G. Mysore, F. Durand, and W. T. Freeman, “The visual microphone: Passive recovery of sound from video,” ACM Transactions on Graphics (Proc. SIGGRAPH), vol. 33, no. 4, pp. 79:1–79:10, 2014.   
[33] A. Veeraraghavan, D. Reddy, and R. Raskar, “Coded strobing photography: Compressive sensing of high speed periodic videos,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 33, no. 4, pp. 671–686, 2011.

[34] T. Wei, S. Wang, A. Zhou, and X. Zhang, “Acoustic eavesdropping through wireless vibrometry,” in Proc. of ACM MobiCom, 2015.   
[35] D. M. Dobkin, The RF in RFID: UHF RFID in Practice. Newnes, 2012.   
[36] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: Realtime tracking of mobile rfid tags to high precision using cots devices,” in Proc. of ACM MobiCom, 2014.   
[37] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proc. of ACM MobiCom, 2014.   
[38] D. Tse and P. Viswanath, Fundamentals of wireless communication. Cambridge university press, 2005.   
[39] “Impinj, Inc,” http://www.impinj.com/.   
[40] “Alien,” http://www.alientechnology.com/.   
[41] EPCglobal, “Low level reader protocol (llrp),” 2010.   
[42] “Idle speed,” https://en.wikipedia.org/wiki/Idle\_speed.   
[43] Y. He and H. Zhang, “A new uhf anti-metal rfid tag antenna design with open-circuited stub feed,” in Proc. of IEEE International Conference on Communications (ICC), 2013, pp. 5809–5813.

![](images/8f5568a457302f903dcb9e88740d2019f35817e0024f9f2ff559b9d2c572961f.jpg)



Chunhui Duan received the BS degree from the School of Software at Tsinghua University, China, in 2013. She is now pursuing her PhD degree in the School of Software at Tsinghua University, China. Her research interests include RFID, wireless network, mobile sensing and pervasive computing. She is a student member of the IEEE and ACM.

![](images/a65c7baa06b456b7579bf95235881c0488b443bcdb2ddc90733fb28f64546941.jpg)



Lei Yang received the BS and PhD degrees from the School of Software and the Department of Computer Science and Engineering at Xi’an Jiaotong University. Previously, he was a postdoc fellow at the School of Software of Tsinghua University. He is currently working as a Research Assistant Professor with the Department of Computing, The Hong Kong Polytechnic University.

![](images/974c41343d748862bcb5ea62c0ff0387760287d6c203e34f4a637755c607a74e.jpg)



Qiongzheng Lin received the BS and PhD degrees from the School of Software at Tsinghua University, China, in 2012 and 2017 respectively. He is now a postdoc fellow at the Department of Computing, The Hong Kong Polytechnic University, Hong Kong. His research interests include RFID and sensor network, mobile sensing and pervasive computing. He is a student member of the IEEE and ACM.

![](images/907b57841eb851449e1f6547b0bc988055610b4b99e957a1e0bdd22375310762.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, USA, in 2003 and 2004, respectively. He is now Chang Jiang Chair Professor and Dean of School of Software at Tsinghua University, China. He is an ACM Distinguished Speaker and now serves as the Chair of ACM China Council and also the Associate Editor for IEEE/ACM Transactions on Networking and ACM Transac-

tions on Sensor Network. His research interests include RFID and sensor network, the Internet and cloud computing, and distributed computing. Yunhao is a Fellow of the IEEE and ACM.

![](images/e153195d5b0a0b5bce092822b399bc67cb7142d2fd1eea21da2030003f0709b0.jpg)



Lei Xie received the B.S. and Ph.D. degrees in computer science from Nanjing University, China, in 2004 and 2010, respectively. He is currently an Associate Professor with the Department of Computer Science and Technology, Nanjing University. He has published over 50 papers in IEEE Transactions on Mobile Computing, IEEE/ACM Transactions on Networking, IEEE Transactions on Parallel and Distributed Systems, ACM Transactions on Sensor Networks, ACM UbiComp, ACM MobiHoc, IEEE IN-

FOCOM, IEEE ICNP, IEEE ICDCS, etc.