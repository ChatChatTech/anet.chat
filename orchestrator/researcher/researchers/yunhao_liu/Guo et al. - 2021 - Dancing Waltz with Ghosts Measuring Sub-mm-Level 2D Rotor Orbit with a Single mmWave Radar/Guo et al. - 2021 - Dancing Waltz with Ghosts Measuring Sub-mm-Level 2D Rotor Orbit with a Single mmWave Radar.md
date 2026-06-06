# Dancing Waltz with Ghosts: Measuring Sub-????-Level 2D Rotor Orbit with a Single mmWave Radar

Junchen Guo

Tsinghua University

gjc16@mails.tsinghua.edu.cn

Meng Jin

Tsinghua University & SJTU

jinm@sjtu.edu.cn

Yuan He

Tsinghua University

heyuan@tsinghua.edu.cn

Weiguo Wang

Tsinghua University

wwg18@mails.tsinghua.edu.cn

Yunhao Liu

Tsinghua University

yunhao@greenorbs.com

# ABSTRACT

Recently, mmWave has been widely used in fine-grained sensing applications due to its short wavelength and large bandwidth. One mmWave device usually can measure the target’s 1D micro-displacement along the line-of-sight (LOS) direction. In this work, we try to empower mmWave with the capability of measuring 2D micro-displacements. Our insight is that although the mmWave reflection from one path contains only 1D observation, the spatial separability of mmWave offers an opportunity to separate multipath reflections from the received signal. Combining the coherent observations from multipath reflections can restore the 2D orbit of the target. Based on this insight, we present GWaltz, a mmWave sensing system that manages to measure sub-????-level 2D orbits of rotating machinery. In GWaltz, we first reveal the relationship between the rotor’s movement and the observed ghost multipath reflections (GMRs) and then design a set of novel signal processing techniques to restore the rotor orbit from the poor-quality GMR signals. We implement GWaltz with a commercial mmWave radar, and our evaluation results show that it achieves an absolute error of about 8.42???? when measuring 100????-diameter rotor orbits.

# CCS CONCEPTS

• Computer systems organization → Embedded and cyber-physical systems; • Hardware → Sensor applications and deployments.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

IPSN ’21, May 18–21, 2021, Nashville, TN, USA

© 2021 Association for Computing Machinery.

ACM ISBN 978-1-4503-8098-0/21/05. . . \$15.00

https://doi.org/10.1145/3412382.3458258

# KEYWORDS

Wireless Sensing, Millimeter Wave, Displacement Measurement, Multipath Exploitation, Rotor Orbit

# ACM Reference Format:

Junchen Guo, Meng Jin, Yuan He, Weiguo Wang, and Yunhao Liu. 2021. Dancing Waltz with Ghosts: Measuring Sub-????-Level 2D Rotor Orbit with a Single mmWave Radar. In The 20th International Conference on Information Processing in Sensor Networks (co-located with CPS-IoT Week 2021) (IPSN ’21), May 18–21, 2021, Nashville, TN, USA. ACM, New York, NY, USA, 16 pages. https://doi.org/10.1145/ 3412382.3458258

# 1 INTRODUCTION

The past decade has witnessed much progress in mmWavebased wireless sensing, e.g., target localization and motion tracking [3, 21, 24, 42, 48]. As a sensing modality, mmWave has several highly attractive properties. Compared with traditional sensor- or vision-based sensing, it is non-intrusive, cost-effective, and unaffected by ambient light conditions. Compared with other wireless technologies such as 900?????? RFID [45] and 2.4?????? WiFi [41], mmWave naturally supports much more fine-grained sensing. For example, its large bandwidth endows it with a ????-level range resolution, and its high frequency, e.g., 77??????, makes it sensitive to even sub-????-level displacements. With all those properties, mmWave radar is used in many fine-grained sensing applications, from object imaging [25, 49], activity and gesture recognition [20], to vital signal [5, 46] or tiny vibration measurement [15, 36].

In these applications, mmWave radar is basically regarded as a 1D displacement sensor. However, knowing the 2D or higher-dimensional micro-movements of a target is also essential in many scenarios. A typical example is to track the 2D rotor orbit of rotating machinery. Specifically, the rotor is the critical component of a rotating machine (e.g., generator and electric motor), which rotates along an ellipse-shaped orbit with a tiny scale [1, 2, 12]. Tracking the rotor orbit is an essential way to monitor the health of the machine. A conventional method [8] is to deploy vibration sensors along two different axes of the rotor, as shown in Fig. 1(a). However, such specialized vibration sensors require intrusive deployment, which leads to high deployment and maintenance costs. What’s worse, the precise synchronization of multiple sensors further increases the system complexity and brings additional expenses. A non-intrusive alternative is to adopt two mmWave radars. However, apart from the problems mentioned above, this dual-radar solution has to share channel resources among radars, which could, in turn, degrade the measurement accuracy.

![](images/9371860fe40ff756b14a300cd2fd96ee8a8f59f73f22fa9c552c0a6a4441e617.jpg)



Figure 1: Measure 2D rotor orbit with sensors and GWaltz.

Therefore, we wonder: can we measure the 2D rotor orbit with just a single mmWave radar? To do so, we explore the feasibility of leveraging the extra information extracted from the non-line-of-sight (NLOS) paths (i.e., signal’s multipath reflections). Recent studies have already exploited multipath effects [17, 32, 33, 40] for 2D target localization. By observing images of a target from both the LOS reflection and the socalled ghost multipath reflections (GMRs), one can derive the target’s actual position based on signal reflection models [16, 26, 30]. Nevertheless, different from those GMR-based 2D localization tasks, measuring the sub-????-level 2D rotor orbit suffers the following two challenges:

• Understanding the relationship between the rotor orbit and GMR signals. Since the scale of the sub-????- level orbit is much smaller than the target size, we have to regard the target as a rigid body instead of a particle. In this case, the signal will be reflected by different points of the target when it is rotating. So, we have to build a more comprehensive model to (i) analyze the properties of GMR signals reflected from different points of its surface and (ii) understand the relationship between the rotor orbit, orbit of the reflection points GMR signals.   
• Dealing with the poor signal quality of GMR signals. Compared with 2D localization, sub-????-level orbit tracking requires much higher signal quality. However, GMR signals suffer from low SNR due to multiple reflections. As a result, the tiny variations of the signal’s physical-layer properties (e.g., phase), which reflects the target’s micromovements, are easily buried under the noise. Besides,

Table 1: Advantages of GWaltz over other methods 

<table><tr><td></td><td>Sensitivity</td><td>Intrusiveness</td><td>Light Condition</td><td>Synchronization</td><td>Device Cost</td></tr><tr><td>Dual Sensor</td><td>High</td><td>High</td><td>No</td><td>Yes</td><td>Low</td></tr><tr><td>Dual Laser</td><td>High</td><td>Low</td><td>Low</td><td>Yes</td><td>High</td></tr><tr><td>Camera</td><td>High</td><td>No</td><td>High</td><td>No</td><td>High</td></tr><tr><td>RFID, WiFi, etc.</td><td>Low</td><td>No</td><td>No</td><td>Yes</td><td>Low</td></tr><tr><td>Dual Radar</td><td>High</td><td>No</td><td>No</td><td>Yes</td><td>High</td></tr><tr><td>GWaltz</td><td>High</td><td>No</td><td>No</td><td>No</td><td>Low</td></tr></table>

the spatial resolution of commercial mmWave radars can hardly support the accurate separation of GMR signals. So, the received GMR signals might entangle with each other, which further impedes the signal quality.

As the first attempt to achieve the vision of orbit restoration with GMR signals, we propose GWaltz, a system that can measure sub-????-level 2D rotor orbits of rotating machinery with just one mmWave radar. Compared with the existing methods, GWaltz is a high-sensitive, non-intrusive, synchronization-free, and easy-to-deploy solution, as shown in Tab. 1. With the continuously restored rotor orbits, GWaltz can be widely applied in industries for mechanical fault diagnosis. Our contributions can be summarized as follows:

First, with a complete understanding of the principle of mmWave signal reflections and the motion law of rigid bodies, we build an orbit-to-signal transformation (OST) model to quantify the relationship between the rotor orbit, surface vibration, and GMR signals. The model answers the following three questions: (i) how are the GMRs produced? (ii) is the orbit of the rotor consistent with that of the reflection points? (iii) what is the relationship between the 1D observation obtained from GMR signals and the rotor orbit?

Second, we embed the OST model in the design of a complete system GWaltz, and design a set of novel signal processing techniques to overcome practical challenges brought by poor signal qualities, including (i) a high-resolution GMR signal extraction algorithm that improves the separability of GMR signals; (ii) a noise-resilient displacement extraction algorithm that utilizes geometric features of the In-phase &

Quadrature (IQ) domain signal to distinguish noises and displacement sequences; (iii) an independent-observation clustering algorithm to stably select available and independent 1D observations; (iv) a spatiotemporal iterative restoration algorithm that can efficiently extract the 2D rotor orbit.

Last, we implement the prototype of GWaltz with a commercial mmWave radar and evaluate its performance under various conditions. The experiment results demonstrate that GWaltz can achieve an absolute error of 8.42???? when measuring 2D orbits with about 100???? diameters. Also, we find that GWaltz can accurately restore the orbit-shape features, $\mathrm { e . g . } ,$ eccentricity and orbit phase.

The rest of this paper is organized as follows. §2 first presents preliminary understandings of mmWave GMRs to motivate our work. §3 and §4 then introduce the overview and design of GWaltz respectively. §5 presents our prototype implementation and various evaluations and §6 compares GWaltz with related works. Last, §7 summarizes our work.

# 2 EXPLOITING GMRS FOR ORBIT RESTORATION

In this section, we review mmWave basics to measure microdisplacements (§2.1) and introduce our OST model (§2.2).

# 2.1 mmWave Displacement Measurement

The ability of mmWave to measure micro-displacements acts as the foundation of GWaltz. We adopt the commercial frequency-modulated continuous-wave (FMCW) radar (TI IWR1642 [13]) for its good range resolution, lightweight design and low cost. Basically, a FMCW radar sends continuous linear-frequency-modulated chirp signals and translates the beat frequency between the TX and RX signals into the range measurement [5]. To separate targets at different angles, the radar performs the spatial spectrum analysis with multi-RX inputs [14]. Readers are suggested to refer to [5, 14, 34] for details. Here we just summarize the two-step Range-Angle FFT process for the ?? -RX radar as follows:

$$
\begin{array}{l} \left\{y ^ {[ n ]} (t) = A ^ {[ n ]} \exp \left[ j 4 \pi (f _ {c} + K _ {c} t) \frac {R ^ {[ n ]} (t)}{c} \right] \right\} _ {n \in N} \\ \xrightarrow [ \text {per RX} ]{\text {Range FFT}} \left\{y _ {r} ^ {[ n ]} (t) = A ^ {[ n ]} \exp \left[ j 4 \pi f _ {c} \frac {R _ {r} ^ {[ n ]} (t)}{c} \right] \right\} _ {n \in N} \\ \xrightarrow [ \text {all RXs} ]{\text {Angle FFT}} y _ {r, a} (t) = A \exp \left[ j 4 \pi f _ {c} \frac {R _ {r , a} (t)}{c} \right] \tag {1} \\ \end{array}
$$

where $f _ { c } , K _ { c } ,$ and $T _ { c }$ are the start frequency, frequency slot, and FMCW chirp period, respectively. The input of this process is the ?? -RX beat-frequency signals $\{ y ^ { [ n ] } ( t ) \} _ { n \in N } ,$ and the output is the signal reflected from the targets located at the discrete range bin ?? and angle bin ??, denoted as

![](images/1503b9c309ec4cb49f0e866b94a0379fedaef96a10cf14964dd9b55887064249.jpg)



![](images/40a8cccb0620ef3d3f18bd0afbf7c02bb5d8d3f01b3b130adf32ec9a643c6eff.jpg)



Figure 2: The formation and properties of GMRs.

$y _ { r , a } ( t )$ . The Fourier analysis tells us that the range resolution $\begin{array} { r } { \Delta r = \frac { c } { 2 B } } \end{array}$ is determined by the chirp bandwidth $B = K _ { c } \cdot T _ { c }$ while the angle resolution $\textstyle \Delta a = { \frac { \bar { 2 } } { N \cos a } }$ ?? cos ?? is mainly determined by the array size ?? [14]. For TI IWR1642, $\Delta r \approx 4 c m$ and $\Delta a \approx 3 0 ^ { \circ }$ when $a \approx 0$ . Thus, imaging technologies like inverse synthetic aperture radar (ISAR) [23] can hardly track the sub-????-level rotor orbit with such limited resolutions.

Since the sub-????-level displacement is within the wavelength of mmWave, it can be directly extracted from $\angle y _ { r , a }$ [5, 42]. Suppose the radar-target distance $R _ { r , a } ( t ) = R _ { r , a } + d ( t )$ , where $d ( t )$ is the time-varying 1D micro-displacement and $R _ { r , a }$ is the time-invariant term, ?? (?? ) can be computed with:

$$
d (t) = \frac {c}{4 \pi f _ {c}} \text { unwrap } (\angle y _ {r, a}) - R _ {r, a} \tag {2}
$$

# 2.2 Orbit-to-Signal Transformation Model

To track a target’s 2D orbit, GWaltz tries to exploit the extra information contained in GMRs instead of deploying extra devices. Fig. 1(b) depicts its measurement scheme: we place the radar in front of the rotor and ensure that its RX array is perpendicular to the rotor’s central axis. Due to GMRs from ambient reflectors, e.g., wall, floor, or ceiling, the radar will observe several separable ghost images coherently rotating with the intrinsic image, as if they were dancing the waltz together. For each GMR signal, GWaltz extracts one 1D observation at a certain observation angle. Together with all the multi-angle observations, it can finally restore the 2D rotor orbit with just a single radar. Next, we introduce the formation and properties of GMRs (§2.2.1), the coherence between the 2D rotor orbit and 2D surface vibration (§2.2.2), and the projection relationship between 1D observations from GMR signals and the 2D orbit (§2.2.3).

2.2.1 GMR Signal Properties. Eq. 1 tells us that the radar obtains $y _ { r , a } ( t )$ if there are reflections from the location bin $( r , a )$ , where ?? equals the half-length of the traveling path and ?? equals $\operatorname { A o A } .$ Here, $y _ { r , a } ( t )$ can be either a LOS or NLOS reflection. For a LOS reflection, it forms an intrinsic image of the target at the correct location. For a NLOS reflection, it forms a ghost image at an incorrect location, since the radar still assumes the rectilinear signal propagation.

![](images/b1a2f652f8697e102afa2ded0654f765680aaa7bfa7a81a3d1cf952641006ee4.jpg)



(a) Observation Experiment Setup

![](images/43a112cdc7e3810cb3b5f9202b94bb2d9192e9f5f60b87889579953911d70592.jpg)  
(b) Ghost Images in RAM   
Figure 3: Observation experiment of GMR properties.

Fig. 2(a) depicts the relationship between intrinsic and ghost images under the particle GMR assumption. We only focus on GMRs reflected once by the target and zero or multiple times by other reflectors, since only these GMRs carry extractable motion characteristics. We define the order of a GMR as the number of reflections from ambient reflectors. Due to accumulated energy losses, higher-order GMRs are often negligible. So, we in this paper only discuss the properties of $\mathrm { \bar { \theta } ^ { t h } , 1 ^ { s t } }$ and $2 ^ { \mathrm { n d } }$ -order GMRs:

• $0 ^ { \mathrm { t h } }$ -order GMR - ??0: Without loss of generality, $G _ { 0 }$ stands for the LOS reflection from the target. Suppose $L _ { 1 }$ is the vector form of the LOS path, then $r _ { 0 } = | L _ { 1 } |$ and $a _ { 0 } = - \angle L _ { 1 }$ .   
• $\begin{array} { r l } { { 1 ^ { s \mathbf { t } } } { - \mathbf { o r d e r \thinspace G M R } } - G _ { 1 } { : } G _ { 1 } } & { { } } \end{array}$ represents the reflection signal bounced by an ambient reflector for once. There are two reverse traveling paths $\vert L _ { 1 } \vert  \vert L _ { 3 } \vert  \vert L _ { 2 } \vert$ and $| L _ { 2 } |  | L _ { 3 } | $ $| L _ { 1 } |$ . In radar’s perspective, since it can only infer a signal’s propagation distance and $\operatorname { A o A }$ , the reflection signal will induce two GMRs $( G _ { 1 , 1 }$ and $G _ { 1 , 2 } )$ with the same range $r _ { 1 , 1 } = r _ { 1 , 2 } = \textstyle { \frac { 1 } { 2 } } \left( \left| L _ { 1 } \right| + \left| L _ { 2 } \right| + \left| L _ { 3 } \right| \right)$ but different AoAs, i.e., $a _ { 1 , 1 } = \angle L _ { 2 }$ while $a _ { 1 , 2 } = - \angle L _ { 1 }$ .   
• 2nd-order $\mathbf { G } \mathbf { M } \mathbf { R } - G _ { 2 } \colon G _ { 2 }$ represents the signal bounced by ambient reflectors for twice. A typical $G _ { 2 }$ has a traveling path following the principle of specular reflection, i.e., $G _ { 2 }$ and $G _ { 0 }$ are mirrored images. In radar’s perspective, $G _ { 2 }$ has the same AoA as $G _ { 1 , 1 }$ but a longer range.

The above discussion treats the target as a particle. However, the volume and shape of the rigid-body target can’t be neglected in our case, where the target size is much larger than the orbit size. Fig. 2(b) depicts the rigid-body GMR assumption. As we can see, $G _ { 0 }$ and $G _ { 2 }$ are still mirrored images while $G _ { 1 , 1 }$ and $G _ { 1 , 2 }$ slightly deviate from their ideal positions. This is because signals traveling along paths $\vert L _ { 1 } \vert  \vert L _ { 3 } \vert  \vert L _ { 2 } \vert$ and $\vert L _ { 2 } \vert  \vert L _ { 3 } \vert  \vert L _ { 1 } \vert$ will reach different points on the target surface, which further leads to slightly different incident (and thus exit) angle of the two paths. Such a slight deviation makes it difficult to calculate the reflection properties of GMRs deterministically. So we use a searching-based method, as will be discussed in §4.

![](images/9e633daeb4b65c2af42b8c574ea8031f22974317921cd9bec9ec9a5ba32bf5a5.jpg)



(a) Normal Incidence Case

![](images/8651c1d35dcd92c34867ab02f4258217209110c2e6e94b2494a79c30727a51d7.jpg)



(b) Non-normal Incidence Case   
Figure 4: Orbit-to-signal transformation model.

To visualize practical GMRs, we conduct an observation experiment. As shown in Fig. 3(a), a centrifuge and an aluminum plate act as the rotating device and reflector, respectively, whose deployment obeys the illustration in Fig. 2(b). After collecting the reflected signals, we extract $y _ { r , a } ( t )$ from every location bin $( r , a )$ and plot their magnitudes in the range-angle map (RAM): a higher magnitude of a point (??, ??) stands for the stronger signal strength of the reflection from that location [14]. Fig. 3(b) shows the decibel-form RAM that clearly describes GMRs and their properties:

• Higher-order GMRs have lower energy and poorer SNR.   
• GMRs’ geometric relationships obey our assumption.   
• There exist ambient reflections from either the table, floor, or walls that may get entangled with the desired GMRs.

2.2.2 Coherence underlying Rotor Orbit and Surface Vibration. With the basic knowledge of GMR signals, we further analyze the relationship between the reflection signals on the target surface and the rotor orbit. Since the radar cannot directly perceive the movement of the rotor center, it can only receive the signal reflected from the reflection points on the target surface. Although we have the primary assumption that the target surface moves in accord with the rotor, the trajectory of those reflection points are not necessarily the same as the trajectory of the rotor center. We define the latter one as the rotor orbit, whose location at time ?? is $\pmb { s } _ { t } = ( s _ { x , t } , s _ { y , t } ) ^ { \top }$ (⊤ stands for the matrix transpose), and define the former one as the surface vibration $ { \boldsymbol { s } } _ { t } ^ { \prime }$ . Then, to restore the rotor orbit from GMR signals, the preliminary task is to explore whether GMR signals can accurately reflect the rotor orbit or not. That ${ \mathrm { i } } s ,$ denoting $\pmb { o } _ { t } = \pmb { s } _ { t } - \pmb { s } _ { t - 1 }$ and ${ \pmb { o } } _ { t } ^ { \prime } = { \pmb { s } } _ { t } ^ { \prime } - { \pmb { s } } _ { t - 1 } ^ { \prime }$ , do we always have ${ \mathbf o } _ { t } = { \mathbf o } _ { t } ^ { \prime } \hat { \ddot { \mathbf { \Gamma } } }$

We demonstrate the underlying coherence with the two examples in Fig. 4. Based on whether the incident wave arrives at the surface along its normal direction or not, we classify GMR signals into two categories. Fig. $4 ( \mathrm { a } )$ shows the case of normal incidence $( G _ { 0 } \& G 2 )$ , where points $s _ { 1 } \sim s _ { 4 }$ and $s _ { 1 } ^ { \prime } \sim s _ { 4 } ^ { \prime }$ denote the trajectories of the rotor center and the reflection points respectively. For each pair of two successive points, say $s _ { 1 } ^ { \prime }$ and $s _ { 2 } ^ { \prime } ,$ , since the normal incident direction must pass through the center, we have $| \overrightarrow { s _ { 1 } s _ { 1 } ^ { \prime } } | = | \overrightarrow { s _ { 2 } s _ { 2 } ^ { \prime } } |$ . In addition, since incident waves are assumed to be parallel with each other, we further have $\overrightarrow { s _ { 1 } s _ { 1 } ^ { \prime } } \parallel \overrightarrow { s _ { 2 } s _ { 2 } ^ { \prime } }$ . So finally we have ${ \overrightarrow { s _ { 1 } s _ { 1 } ^ { \prime } } } = { \overrightarrow { s _ { 2 } s _ { 2 } ^ { \prime } } }$ and thus $\overrightarrow { s _ { 1 } s _ { 2 } } = \overrightarrow { s _ { 1 } ^ { \prime } s _ { 2 } ^ { \prime } }$ . For the case of nonnormal incidence $( G _ { 1 } )$ in Fig. 4(b), we still have $\overrightarrow { s _ { 1 } s _ { 1 } ^ { \prime } } = \overrightarrow { s _ { 2 } s _ { 2 } ^ { \prime } }$ and $\overrightarrow { s _ { 1 } s _ { 2 } } = \overrightarrow { s _ { 1 } ^ { \prime } s _ { 2 } ^ { \prime } }$ . Therefore, we have proved that ${ \mathbf o } ( t ) = { \mathbf o } ^ { \prime } ( t )$ , i.e. ?? (?? ) and $\mathbf { \boldsymbol { s } } ^ { \prime } ( t )$ are coherent.

![](images/d0b60ce82c8ccd2b1841bb6752d301f8f2ffa3cf5da3c08246b6d9bc18a6d4ba.jpg)



Figure 5: System overview of GWaltz.

2.2.3 2D Orbit Restoration with 1D GMR Observations. The previous section has verified the coherence between the rotor orbit and the surface vibration. However, the radar can only perceive the 1D displacements of the surface rather than its 2D vibrations. Then, this section further explores the relationship between the 2D rotor orbit / surface vibration and those 1D displacements observed from GMRs.

For any 2D movement trajectory of a target, the mmWave radar can only extract its projections on signal propagation directions, i.e., incident and exit directions. We illustrate this projection model in cases of normal and non-normal incidence in Fig. 4. Denoting their normal direction by $\beta$ and the equal incident and exit angles by $\gamma ,$ the incident and exit directions can be represented as $\beta ^ { \prime } = \beta - \gamma$ and $\beta ^ { \prime \prime } = \beta + \gamma$ respectively. Without loss of generality, we have $\gamma = 0$ and $\beta ^ { \prime } = \beta ^ { \prime \prime } = \beta$ for the normal-incidence case. Then the 1D displacement ?? measured by the radar can be computed as the average of the projections of $\mathbf { o ^ { \prime } }$ on $\beta ^ { \prime }$ and $\beta ^ { \prime \prime } { : }$

$$
\begin{array}{l} d (\boldsymbol {o} ^ {\prime} | \beta , \gamma) = d (\boldsymbol {o} | \beta , \gamma) = \frac {1}{2} (\boldsymbol {v} _ {\beta^ {\prime}} ^ {\top} \boldsymbol {o} + \boldsymbol {v} _ {\beta^ {\prime \prime}} ^ {\top} \boldsymbol {o}) \\ = \frac {1}{2} \left[ \left(o _ {x} \cos \beta^ {\prime} + o _ {y} \sin \beta^ {\prime}\right) + \left(o _ {x} \cos \beta^ {\prime \prime} + o _ {y} \sin \beta^ {\prime \prime}\right) \right] (3) \\ = \cos \gamma \cdot (o _ {x} \cos \beta + o _ {y} \sin \beta) = \cos \gamma \cdot \pmb {v} _ {\beta} ^ {\top} \pmb {o} \\ \end{array}
$$

where $\pmb { \upsilon } _ { \beta } = ( \cos \beta , \sin \beta ) ^ { \top }$ is the projection vector. Eq. 3 tells us that ?? is a projection of ?? on the normal direction $\beta$ (also

known as its observation angle), and the incident/exit angle ?? can be considered as a scaling factor whose value range is cos $\gamma \in ( 0 , 1 ] , \gamma \in [ 0 , \frac { \pi } { 2 } )$ . In the case of normal incidence, we have $\gamma = 0$ and cos $\gamma = 1$ .

Finally, we can formulate the coherence underlying multiangle observations $\{ d ( \pmb { o } | \beta _ { m } , \gamma _ { m } ) \} _ { m \in M } : ( \mathrm { i } )$ they are 1D projections of the same 2D movement; (ii) they are intrinsically synchronized since the differences in the propagation time on different paths are significantly smaller than the chirp sampling period. This verifies our insight that we can restore the 2D orbit ?? with multi-angle 1D observations $\{ d ( \pmb { o } | \beta _ { m } , \gamma _ { m } ) \} _ { m \in M } .$ However, it’s a non-trivial task to implement this idea due to the following challenges:

• The first concern is the signal qualities of the GMRs. Since higher-order GMRs basically have poorer SNR, we have to figure out a way to stably identify GMRs and tolerate the phase noises of GMRs when extracting 1D observations.   
• The second concern is the lack of prior knowledge about ambient reflectors. Thus, it’s very difficult to determine the orders of GMRs as well as the projection parameters $\beta _ { m }$ and $\gamma _ { m }$ . Moreover, we find GMRs could be close or even overlap with each other in practice, which could further impede the displacement extraction.

# 3 GWALTZ OVERVIEW

Fig. 5 depicts the overview of GWaltz: it takes raw beatfrequency signals from 4 RXs of the mmWave radar as inputs, and outputs the 2D rotor orbit. To achieve this goal, we design a processing pipeline consisting of the following 4 modules:

• Module 1 - GMR Signal Extraction: The $1 ^ { \mathrm { s t } }$ module serves as the prerequisite of the system: it identifies GMR areas, i.e., the locations of GMRs in the RAM, and extracts corresponding GMR signals. To improve the spatial resolution of GMR signals and avoid them being overwhelmed by noises, we bring several advanced signal processing technologies together.

![](images/ece13e3bdd9830d60a9baec008f30f3304270e18bc0c41c9e04e8992e58286f6.jpg)  
Figure 6: ERAM generation and GMR detection.

• Module 2 - 1D Displacement Extraction: The $2 ^ { \mathrm { n d } }$ module generates the core intermediate results of the system: it extracts the 1D displacement sequence embedded in each GMR signal. To extract the tiny signal variation caused by the sub-????-level displacement from the noisy signal, we utilize the signal’s geometric features in the IQ domain to distinguish noises and displacement sequences. For every GMR signal in every GMR area, we run this module separately to get multiple 1D displacement sequences.   
• Module 3 - Observation Selection: The 3rd module is designed to ensure the quality of the intermediate results. Since one detected GMR area might falsely contain more than one GMR, the extracted 1D displacement sequences might be a joint result of several independent observations. To solve the problem, we design an independence clustering algorithm to generate the final 1D observations for the orbit restoration.   
• Module 4 - 2D Orbit Restoration: The $4 ^ { \mathrm { t h } }$ module collects all the independent 1D observations from all GMR areas to restore the 2D orbit. An optimization problem is formulated to simultaneously solve the orbit as well as the undetermined projection parameters. We design a spatiotemporal iteration algorithm to split the searching space for higher efficiency.

# 4 GWALTZ DESIGN

# 4.1 GMR Signal Extraction

The primary task of this module is to improve the separability of GMR signals, find their locations, and extract them in a high-fidelity and efficient way.

Step 1 - Enhanced RAM Generation: With the FMCW modulation and multi-RX inputs, the raw mmWave signals can be separated into reflection signals from every discrete location bin $( r , a )$ . However, the angular resolution of the raw RAM generated through the Range-Angle FFT process is very limited [27], as shown in Fig. 6(b). This makes the extracted GMR signals entangled with each other. To improve the angular resolution of RAM, our basic idea is utilizing the receiver beamforming (RBF) technology [27, 35] instead of

Angle-FFT. RBF calculates the optimal aggregation weights of the RX antennas that can make them concentrate on the desired direction [34]. To reduce signal distortions under noises during RBF, we choose robust Capon beamforming (RCBF) technology [35]. Then, to further increase the quality of RAM, we adopt Blackman windowing and direct-current component filtering to reduce the spectral leakage problem [27] and eliminate static clutters, respectively. The enhanced RAM (ERAM) shown in Fig. 6(e) shows a much higher resolution than the raw RAM, where GMRs can be clearly separated and observed.

Step 2 - GMR Detection: Next, to find the locations of GMRs in ERAM, the main challenge is the trade-off between the missed and false detection rate under noise. Instead of applying a fixed threshold to ERAM, we adopt constant false alarm rate (CFAR) detector [27], which derives a dynamic power threshold according to the estimated noise level and the expected false alarm rate [28]. We cascade two noiseresilient Ordered-statistic CFAR in the range and angle domains, thus weighing the effectiveness and efficiency. Fig. 6(e) shows the 2D bounding boxes where GMR signals possibly locate in ERAM as detected GMR areas.

Step 3 - GMR Signal Output: With the detected GMR areas, the final step is to extract them from ERAM through RCBF. However, the computation cost of the global operation, i.e., scanning every location bin to perform the signal extraction with RCBF, is relatively high. Fortunately, we find that as long as the operating environment keeps stable, the signal propagation paths are basically unchanged, and thus the detected GMR areas are also unchanged. Thus, we only perform RCBF globally once in a while to generate ERAM for GMR Detection. And then, we perform RCBF locally only on the detected location bins for subsequent data frames. This heuristic idea achieves 3?? ∼ 5?? speed-up.

# 4.2 1D Displacement Extraction

The second module extracts 1D displacement ?? (??) from every GMR signal $y _ { r , a } ( t )$ . In this section, we first show how poor-SNR signal affect the process of 1D placement extraction in §4.2.1 and provide our noise-resilient displacement extraction algorithm in §4.2.2.

4.2.1 GMR Signal Model and Impact of Poor SNR. Inspired by some existing researches [15, 42], the samples of $y _ { r , a } ( t )$ form an arc in the IQ domain. The central angle ?? of the arc is determined by the peak-to-peak amplitude of the displacement $D ,$ and the circle radius ?? is proportional to the signal strength. The center of the arc is theoretically located at the origin of coordinates.

In practice, however, GMR signal contains not only the time-varying part $y _ { r , a } ( t )$ induced by periodic rotor rotation but also the time-invariant part that stands for the static background reflections [42]. Fig. 7(a) visualizes the GMR signal model $y _ { r , a } ^ { * } ( t )$ as:

![](images/7570595c8c1047bb73732f5e7721c79084fe3dea183241fdd4e82774bec90ad6.jpg)  
Figure 7: Signal features in the IQ domain.

$$
y _ {r, a} ^ {*} (t) = y _ {r, a} (t) + \hat {y} _ {r, a} = A \exp \left[ j 4 \pi f _ {c} \frac {R _ {r , a} + d (t)}{c} \right] + \hat {y} _ {r, a} (4)
$$

where $\hat { y } _ { r , a }$ represents an aggregation of all the static background reflections from the bin $( r , a )$ . Since $\hat { y } _ { r , a }$ is a constant value, the background reflection only induces a displacement of the arc in the IQ domain, as shown in Fig. 7(a). The deviation exactly represents the signal vector of the background reflection. So, to infer ${ \hat { y } } _ { r , a } ,$ a common strategy is to find the center of the signal arc in the IQ domain through a circle fitting process [15, 22].

However, traditional fitting-based methods are vulnerable to poor SNR condition that is inevitable for high-order GMRs. To understand this problem, we illustrate an example of the poor-SNR signal in Fig. 7(b). As we can see that (i) the sub-????-level displacements induce a particularly small central angle ??; and (ii) the weak high-order GMR signal makes a particularly low circle radius ??. As a result, the signal samples form a cluster rather than an arc, which significantly degrades the fitting performance. Although some existing methods [15] are proposed to mitigate this problem by utilizing multi-frequency calibration, they require at least one good initial fitting result on a certain frequency. This makes them unsuitable for our case, where the high-order GMRs may exhibit limited SNR on all the frequencies.

4.2.2 Signal Fitting with Circle Fitting Constraint. Before introducing our solution, let’s have a quick look at the 4 typical wrong fitting results in Fig. 7(b): $C _ { 2 }$ and $C _ { 3 }$ show the cases where the arc radius is inaccurately estimated while $C _ { 1 }$ and $C _ { 4 }$ shows the cases where the direction of the circle center (defined as the direction of the circle center respect to the signal arc’s midpoint) is incorrectly identified. The inaccurate circle radius leads to an inaccurate estimation of the signal amplitude $( C _ { 2 } \& C _ { 3 } )$ . However, the wrong circle radius causes a more serious error that treats the signal variation caused by the noise as the vibration signal and outputs a wrong signal sequence (??4). Thus, to cope with the poor-SNR GMR signal, our basic insight is that: we first ensure the

![](images/8fc7b5cc5d48087b2724f245c70e7b91e84cccd0f2cad814ed8f09307e3d9587.jpg)  
Figure 8: Projection-based center direction metric.

correctness of signal extraction with a strong constraint on the center direction, then try our best to improve the accuracy with a weak constraint on the circle radius. Next, we describe how to derive these two constraints.

Center Direction Constraint $\Omega _ { 1 } \colon$ First, we derive $\Omega _ { 1 }$ by searching for the correct center direction ??. Our key insight here is although the signal arc of GMRs may be overwhelmed by noises, the signal’s variation in the IQ domain caused by the noise is highly random, while the variation caused by the displacement is deterministic (i.e., along the arc). Thus, when projecting the IQ samples to the normal direction of the signal arc and observe the change in the signal’s amplitude with time, we can obtain a signal sequence that best preserves the distinct pattern of the sinusoidal waveform, as shown in Fig. 8(a). As a result, for a better center direction, the energy of the projection sequence’s spectrum is more concentrated to a certain frequency. Based on the above observation, we combine two spectrum features to find the best ?? (i) The spectrum kurtosis $\kappa _ { b }$ of the rotation frequency band ??, e.g. [10, 200]???? for the centrifuge we have used. (ii) The band spectrum energy ratio $\begin{array} { r } { \xi _ { b } = \frac { \check { e _ { b } } } { e } } \end{array}$ where ?? is the total spectrum energy and $e _ { b }$ is spectrum energy of the band ??. With $\kappa _ { b }$ and $\xi _ { b } ,$ we propose a metric $k = \operatorname* { m a x } ( 0 , \kappa _ { b } ) \cdot \xi _ { b }$ to quantify how likely a certain direction is the correct center direction.

By enu rating ?? with a step of $\textstyle { \delta \alpha = { \frac { \pi } { 1 6 } } }$ , we compute $k _ { \alpha }$ shown in Fig. 8(b), where red arrows indicate best direction $\alpha ^ { * }$ with the highest $k _ { \alpha ^ { * } }$ . Due to the perpendicularity between $\alpha ^ { * }$ and the deterministic tangent direction of the signal arc, the radar plot forms a shape of the number 8, whose peaks and valleys are perpendicular to each other. Since $k _ { \alpha }$ has two opposite-direction peaks, we construct $\Omega _ { 1 }$ as two symmetrical areas: $\left[ \alpha ^ { * } - \delta \alpha , \alpha ^ { * } + \delta \alpha \right] \bigcup \left[ \alpha ^ { * } - \delta \alpha + \pi , \alpha ^ { * } + \delta \alpha + \pi \right]$ where $\alpha ^ { * } \in [ 0 , \pi )$ . Note that the opposite-direction circle $( C _ { 1 } )$ will generate a displacement sequence with an opposite phase, which is tolerated by inverting its observation angle.

Circle Radius Constraint $\Omega _ { 2 } { : }$ Since the circle radius ?? is hard to accurately estimate in practice, we derive $\Omega _ { 2 }$ based on the prior knowledge of the range in the vibration amplitude $D , \mathbf { e . g . } , D \in [ 2 0 , 1 0 0 ]$ ???? for our centrifuge. Given $\begin{array} { r } { \theta = \frac { 8 \pi D } { \lambda } } \end{array}$ , we can build the relationship between ?? and ?? by introducing the concept of the projection height. As shown in Fig. 9(b), the projection height ℎ is the maximum range of the projected signal samples in the best direction. We can get sin $\begin{array} { r } { \frac { \theta } { 2 } \stackrel { \cdot } { = } \frac { h } { 2 } / \tau ; } \end{array}$ , that is $\begin{array} { r } { \tau = \frac { h } { 2 } / { \sin \left( \frac { 4 \pi D } { \lambda } \right) } } \end{array}$ ?? . Given $D \in [ D _ { \operatorname* { m i n } } , D _ { \operatorname* { m a x } } ]$ , we get $\Omega _ { 2 }$ as $\begin{array} { r } { \left\lceil \frac { h } { 2 } / \sin \left( \frac { \overline { { 4 } } \pi D _ { \mathrm { m a x } } } { \lambda } \right) , \frac { h } { 2 } / \sin \left( \frac { 4 \pi D _ { \mathrm { m i n } } } { \lambda } \right) \right\rceil } \end{array}$

![](images/49515745f31e5d7dcc093caea576309421803a145621c63a054a81327ea36f84.jpg)



![](images/a589ca90c1b810833919ec0821a2a8e7500d4bcc537e3135114d0358619dbd5f.jpg)



Figure 9: Illustration of circle fitting constraint.

Fig. 9(c) shows how $\Omega _ { 1 }$ and $\Omega _ { 2 }$ jointly bound the searching space of the fitting process. Then, we form a nonlinear-leastsquare optimization that minimizes the geometric distances from every sample to the circle under $\Omega _ { 1 }$ and $\Omega _ { 2 } { : }$ :

$$
\boldsymbol {z} ^ {*}, \boldsymbol {\tau} ^ {*} = \operatorname{argmin} L (X | \boldsymbol {z}, \tau) = \sum_ {i = 1} ^ {N} \left(\left\| \boldsymbol {x} _ {i} - \boldsymbol {z} \right\| - \tau\right) ^ {2} \tag {5}
$$

where $z = ( z _ { 1 } , z _ { 2 } ) ^ { \top }$ and ?? are the center coordinate and radius of the fitted circle respectively, and $X = \{ x _ { 1 } , . . . , x _ { N } \}$ , $\boldsymbol { x } _ { i } \in \mathcal { R } ^ { 2 }$ are IQ samples of the GMR signal. We compute $\Omega _ { 1 }$ and $\Omega _ { 2 }$ with ?? and convert them into the penalty terms in the loss function with Lagrange multiplers. Then, the optimization problem is solved with the Levenberg-Marquardt (LM) algorithm [7]. Finally, we get $y _ { r , a } ( t ) = X - z ^ { * }$ an d extract the 1D displacement sequence $d ( t )$ from $\angle y _ { r , a } ( t )$ .

# 4.3 Observation Selection

In ERAM, different GMRs could be very close to or even overlap with each other for the following two reasons. First, due to the limited resolution of ERAM, it is possible that one detected GMR area actually contains multiple GMRs. Second, signals traveling from different paths could occasionally fall into the same location bin if they have similar AoAs and equivalent propagation distances. Either of these two cases results in inaccurate 1D displacement measurement. Therefore, we in this section propose a method to first filter out the bins that contain multiple GMR signals, and then separate the GMRs that are incorrectly bounded into one GMR area.

![](images/0c02dfb87031f563d2df3d3b22f6e4cf090a29eab2efbd14ba898c444186e4a6.jpg)  
(a) Phase Values of All Sequences

![](images/7924f6ee7428b0112b0f0b20cc1a7041cfdc72ff1d8a5027fe0d4343d155251e.jpg)



(b) Clustering Results   
Figure 10: Independent observation clustering.

Step 1 - Usable Candidate Selection: First, we select 1D displacement sequences with good SNR as candidates. Geometric features like circle radius, signal height, best direction metric, and spectrum features like kurtosis and energy ratio are considered. We calculate their normalized sums as the candidate weights. Only top-70% weighted sequences are kept as candidates in this step.

Step 2 - Independent Candidate Clustering: Next, we select independent candidates as the final 1D observations. A problem here is how to quantify their dependence? By observing the candidates extracted from one detected GMR area, we find that two factors cause their dependence:

• Physical Adjacency: GMR signals from adjacent positions on the target surface have similar motion characteristics.   
• Logical Adjacency: FFT or beamforming process causes inevitable spectrum leakage, which makes GMR signals extracted from adjacent bins similar to each other.

Therefore, we empirically select two features to identify two independent GMR signals: (i) the phase value $\phi$ of the candidate, and (ii) the bin location of the GMR signal where the candidate comes from. We consider that two candidates are independent if they have different phase values and they come from non-adjacent bins.

The above insight motivates the our independence clustering algorithm. First, we derive a phase-based similarity metric with a wrapping period of ??: min $\{ | \phi _ { 1 } - \phi _ { 2 } + \Delta \phi | \} , \Delta \phi \in$ $\{ - \pi , 0 , \pi \}$ . We choose the wrapping period of ?? instead of 2??, because our displacement extraction algorithm with symmetrical constrained areas could produce similar displacement sequences with opposite phases. Second, we set the similarity metric to +∞ if two candidates don’t come from each other’s $3 \times 3$ neighborhood. Finally, the similarity metrics are fed into a classic clustering algorithm, DBSCAN [6]. Fig. 10(b) shows the clustering result, where different edge colors of different location bins stand for their different clusters. At last, we calculate the weighted aggregation of the candidates in each cluster as one final observation. Fig. 11 shows an example of this processing chain.

![](images/db17b3d94ecbf29e3273ab1e7a0923f946b469ebb3b2d0ee38c6dcd7749355a9.jpg)



Figure 11: Processing steps of a 3-cluster GMR area.

# 4.4 2D Orbit Restoration

The final module restores the 2D orbit with all the independent 1D observations from all detected GMR areas. We first formulate the restoration problem that exploits the observations’ coherence and diversity to simultaneously solve undetermined projection parameters and the orbit (§4.4.1). A spatiotemporal iteration algorithm is proposed to improve its efficiency by splitting the searching space (§4.4.2).

4.4.1 Problem Formulation. With ?? independent 1D observations, we obtain ?? sequences of 1D displacement measurements $d _ { m } ( t ) , m \in [ 1 , M ]$ . Recall that $d _ { m } ( t )$ is a projection of the orbit ${ \mathbf o } ( t )$ , i.e. $d _ { m } ( t ) = \cos \gamma _ { m } \cdot \boldsymbol { v } _ { \beta _ { m } } ^ { \top } \pmb { o } ( t )$ , where $\pmb { v } _ { \beta _ { m } } = ( \cos \beta _ { m } , \sin \beta _ { m } ) ^ { \top }$ is the projection vector and cos $\gamma _ { m }$ is the amplitude scaling factor. As we have discussed in $\ S 2 ,$ , parameters $\beta _ { m }$ and $\gamma _ { m }$ are determined by the relative positions of the target, the radar, and the ambient reflectors. Moreover, we apply an error factor $\epsilon _ { m } \tan ( t )$ to tolerate the inaccurate amplitude estimation due to poor SNR conditions. Since both $\epsilon _ { m }$ and cos $\gamma _ { m }$ can be considered as amplitude scaling factors, we can combine these two factors to create one variable $\begin{array} { r } { g _ { m } = \frac { \cos \gamma _ { m } } { \epsilon _ { m } } } \end{array}$ cos????

$$
d _ {m} (t) = g _ {m} \boldsymbol {v} _ {\beta_ {m}} ^ {\top} \boldsymbol {o} (t), m \in [ 1, M ] \tag {6}
$$

With ?? samples of $\dot { \boldsymbol { d } } _ { m } ( t ) , t \in [ 1 , T ]$ , Eq. 6 can be expanded into a set of $M \cdot T$ equations, where $2 M + 2 T$ variables are undetermined. Then we can represent the equation set in the matrix form:

$$
D = G V O,
$$

$\mathrm { w h e r e } D = \{ d _ { m } ( t ) \} _ { M \times T } , G = \mathrm { d i a g } \left( \{ g _ { m } \} _ { M \times 1 } \right) ,$ (7)

$$
\boldsymbol {V} = \{\boldsymbol {v} _ {\beta_ {m}} ^ {\top} \} _ {M \times 2}, \boldsymbol {O} = \{\boldsymbol {o} (t) \} _ {2 \times T}
$$

Then, our goal is to search for the optimal variables that minimize the $2 ^ { \mathrm { n d } }$ -norm $\| D - G V O \| ^ { 2 }$ . Two constraints can be applied to bound the searching space. First, for the LOS reflection $G _ { 0 } \ ( \mathrm { i . e . } \ m = 1 )$ , its projection parameters can be obtained as prior knowledge: (i) the observation angle $\beta _ { 1 }$ can be fixed $\mathrm { t o } - \frac { \pi } { 2 }$ if we place the radar directly in front of the rotating device; (ii) $g _ { 1 }$ can be set to 1 since cos $\gamma _ { 1 } = 1$ as we analyzed before and $\epsilon _ { 1 }$ can be deemed as 1 due to the high SNR of $G _ { 0 }$ . Second, we can further derive a rough estimation of $g _ { m } .$ , ?? ∈ [2, ??] in practice: (i) since the low SNR condition basically causes a larger amplitude estimation, we can have $\epsilon _ { m } \in [ 0 . 7 5 , 1 ] ; \left( \mathrm { i i } \right) \gamma _ { m }$ can be roughly estimated based on the deployment, $\begin{array} { r } { \mathbf { e . g . , } \gamma _ { m } \in [ 0 , \frac { \pi } { 6 } ] } \end{array}$ in our experiment setup. Then, the rough value range of $g _ { m } , m \in [ 2 , M ]$ can be computed.

4.4.2 Spatiotemporal Iterative Restoration. Although we have bounded the searching space in the last step, directly searching for $G , V$ and ?? simultaneously is still a highly complex process. We propose a high-efficiency spatiotemporal iteration method to divide and conquer the problem.

Among these unknown variables, we denote time-invariant ?? and ?? as the spatial variables that are only related to the traveling paths of GMRs. And we denote time-varying ?? as the temporal variable that is irrelevant to GMRs. With the prior of spatial variables, the temporal variable can be directly inferred with the equation set and vice versa. Therefore, we design an iteration-based restoration algorithm that significantly reduces the searching space: for each iteration $i \in [ 1 , i _ { m a x } ]$ , we solve $O ^ { [ i ] }$ with $G ^ { [ i - 1 ] } , V ^ { [ i - 1 ] }$ , and then solve $G ^ { [ i ] } , V ^ { [ i ] }$ with $o ^ { [ i ] }$ . The initial value $G ^ { [ 0 ] }$ is set to a vector whose elements are all 1, and $V ^ { [ 0 ] }$ is guessed by regarding all GMRs as $2 ^ { \mathrm { n d } } .$ -order GMRs since their observation angles can be deterministically derived with the OTS model. Next, we present the detailed algorithm, where the superscript ?? is neglected for clarity.

(1) Temporal Variable Solver: With the known ?? and $V , { \mathrm { E q . } }$ 7 is degenerated into a overdetermined linear equation set, where ?? can be solved with the linear least square (LLS) method. We adopt the weighted LLS with a diagonal weight matrix ?? whose elements are the candidate weights of ??:

$$
W G ^ {- 1} D = W V O \Longrightarrow O = \left(V ^ {\top} W V\right) ^ {- 1} V ^ {\top} W G ^ {- 1} D \tag {8}
$$

(2) Spatial Variable Solver: Assuming the independence among spatial variables, we run this solver on each observation separately. Eq. (9) shows the loss function of the searching process. To quantify the similarity between $d _ { m } ( t )$ and $g _ { m } \pmb { v } _ { \beta _ { m } } ^ { \top } \pmb { o } ( t )$ ???? , we first use cosine distance, a widely used metric in comparing two periodic signals, to quantify their similarity in phase, i.e., the amount of misalignment between them. Then we use the Euclidean distance to quantify their similarity in amplitude. We use these two steps to find a sequence with an acceptably high goodness-of-fit.

![](images/e39d85c72d1587604d77e276fca7f7fb8c7b3d70b1c552c71ed514980724d4a4.jpg)  
Figure 12: Restored and ground-truth orbits.

$$
\min _ {\beta_ {m}} L _ {m, 1} = 1 - \frac {\left(\boldsymbol {d} _ {m}\right) ^ {\top} \left(g _ {m} \boldsymbol {v} _ {\beta_ {m}} ^ {\top} \boldsymbol {o}\right)}{\left\| \boldsymbol {d} _ {m} \right\| \cdot \left\| g _ {m} \boldsymbol {v} _ {\beta_ {m}} ^ {\top} \boldsymbol {o} \right\|} \tag {9}
$$

$$
\min _ {g _ {m}} L _ {m, 2} = \left\| \pmb {d} _ {m} - g _ {m} \pmb {v} _ {\beta_ {m}} ^ {\top} \pmb {o} \right\| ^ {2}
$$

Fig. 12 shows examples of the orbits restored by GWaltz, where the blue and red orbits stand for the restored orbit and the ground truth, respectively. The directions and lengths of red arrows indicate the observation angles and amplitudes of 1D observations, respectively. As expected, the initial orbit after one LLS shows great bias due to the incorrect estimation of ?? [0] . While the result after 5 iterations is very similar to the final convergent one, which demonstrates the high efficiency of our algorithm.

Fig. 12(5) shows the orbit restored with only two observations. The result tells that we can still obtain a decent result with only two observations, although the estimated orbit can be distorted if one of the two observations suffers poor accuracy. Fig. 12(6) shows the orbit restored without applying a scaling factor. The result tells that even with multiple GMRs, one inaccurate observation, e.g., GMR-2 in this case, can degrade the performance if scaling factors are not applied. In summary, GWaltz can achieve a good result of the orbit restoration at an acceptable cost.

# 4.5 Discussion

As the first step to achieving the vision of orbit restoration with GMR signals, our current design has several limitations that are left for future work. First, GWaltz identifies the target’s reflections by finding the signal that changes with time. So, GWaltz does not support the cases with multiple rotating targets or with moving ambient reflectors. This problem can be resolved by endowing reflection signals with identities through state-of-the-art battery-free mmWave backscatter technologies [19]. Second, the orbit restoration module of GWaltz requires a coarse-grained prior knowledge of the deployment setup to reduce the searching space. Actually, even without this prior knowledge, we can still obtain a coarse-grained estimation of the deployment setup as well as the value ranges of the projection parameters based on the relative locations of the GMRs in ERAM.

![](images/04fc7638c06c1c154f86203409c7cffd35f9cda8567df7fad5316bc82ade4e6b.jpg)



(a) Moderate Multipath

![](images/41d3cc119735b882f0fa5e43b726157690fddab47217e339ea09457c200791ec.jpg)



(b) Rich Multipath   
Figure 13: Experiment setup.

# 5 EVALUATION

# 5.1 Implementation and Methodology

Implementation: For the hardware, we adopt a commercial mmWave radar TI IWR1642 [13], which has 6 antennas (2 TXs and 4 RXs) and works on 77?????? frequency band with the maximum available bandwidth of 4??????. We let all 4 RXs to receive reflected signals from 1 TX. The cost of IWR1642 IC is < \$40, which is very competitive compared to other solutions. We implement GWaltz software in Python 3, which can be easily translated into other languages or ported to embedded platforms. We open-source the core code as well as our datasets at http://tns.thss.tsinghua.edu.cn/sun/. The experiments are conducted on a laptop with an Intel i7-8550U processor and 16???? memory.

Ground Truth: To obtain the ground truth, we use the eddy-current sensor, [4] which can measure the micro displacement by sensing the change of the magnetic field between its probe and the target surface. The sensor’s datasheet declares a relative measurement error of ±5%. To measure the 1D vibrations along the X and Y axis, we deploy two eddycurrent sensors perpendicularly to each other, as shown in Fig. 14. A multi-input data collector is used to synchronize the data streams from two sensors. After getting two sinusoidal displacement sequences from the collector, we restore the 2D orbit with previously-known observation angles and then fit an ellipse as the ground-truth orbit.

Experiment Settings: All of the experiments are conducted in an office environment as shown in Fig. 13. We use a centrifuge as the rotating machinery during most of the experiments for the convenience of controlling experimental variables, e.g., the distance between the radar and the centrifuge (i.e., measuring distance), the distance between the centrifuge and the ambient reflector (i.e., reflector distance), the rotating speed and the workload of the centrifuge. We also evaluate the impact of different multipath conditions and explore whether deploying dedicated reflectors can improve the performance. Moreover, to demonstrate the floor can act as the ambient reflector for GWaltz, we measure the 2D orbit of a fan whose central axis is parallel to the ground. Last, we also evaluate some microbenchmarks, e.g., the accuracy of 1D vibration measurement, the processing efficiency, and the measurement stability. We have collected > 1600 data traces of about 34????.

![](images/0346ba1cb7c005ebf0e7f849076c44a79ccb05cbe4075ed9f9d025028ee2148c.jpg)



Figure 14: Ground-truth measurement setup.

![](images/fb0a48a6d3abecb2db3ad02a27ad021898af1ec6697e39147966a5175e39e03e.jpg)



(a) Orbit Distance

![](images/30b07691b318975585f9b0ecc31126af371f4bfa8f97c98fc66dfc6fc2fc4f36.jpg)



(b) Eccentricity Error

![](images/f604732da7d48e50f8bea0fcbc3238b906a3879bf4df62ab53ca01b868d86d6e.jpg)



(c) Orbit Phase Error   
Figure 15: Overall performance under different setups.

![](images/d94a4df60362d4e1c1a3eaa3e800fbc11e2a157fe7ef6db9b4d9e8932fd28626.jpg)



(a) Impact of Measuring Distance

![](images/19c2256125c6b65becd41a9c4152e5cba39a5314e8777e6b62b2fcf6ab43e8c0.jpg)



(b) Impact of Reflector Distance

![](images/0902228fb9bd6c90ee49cdcc63469ac3592b0256ab62b79887c8bff191b290cf.jpg)



(c) Impact of Rotating Speed   
Figure 16: Performance of orbit restoration.

Performance Metric: We adopt the polar-coordinate trajectory distance as the main metric for the orbit restoration. Give a point $\mathbf { \nabla } \mathcal { P } i$ of the measured orbit, the line between $\mathbf { \nabla } \mathcal { P } i$ and the origin of coordinate will generate two intersection points $p _ { i } ^ { ' }$ and $p _ { i } ^ { \prime \prime }$ with the ground-truth orbit, and we denote min $( | p _ { i } - p _ { i } ^ { ' } | , | \stackrel { . } { p } _ { i } - p _ { i } ^ { ' \prime } | )$ , the shortest Euclidean distance between $\mathbf { \nabla } \mathcal { P } i$ and the intersection points, as the polar-coordinate trajectory distance. Apart from the absolute trajectory distance, we also use the eccentricity (the focal length divides the length of the major axis) and the phase (the rotation angle of the major axis) of the ellipse-shaped orbit to evaluate the performance of preserving relative shape features.

# 5.2 Performance of Orbit Restoration

In this section, we evaluate the performance of the orbit restoration under different measuring distances (60 ∼ 150????), reflector distances (15 ∼ 60????), and rotating speeds (1500 ∼ 3000??????). The experiments are conducted in a hall where a concrete wall acts as the ambient reflector. We keep the centrifuge running in a relatively stable state with no workload.

5.2.1 Overall Performance. Fig. 15 depicts the overall performance of GWaltz considering the orbit restoration error, i.e., orbit distance and restoration shape features, i.e., eccentricity and orbit phase. For each measured orbit, we record the median orbit distance from the ground-truth orbit as its restoration error. Then we fit an ellipse with the measured orbit to calculate its eccentricity and phase as well as the errors between them and ground-truth ones.

The CDF results show that GWaltz well restores the 2D rotor orbit with $8 0 ^ { \mathrm { t h } }$ -percentile restoration error of 8.42????. The relative error is around 8% respect to the 100????-diameter orbit, which is comparable to traditional sensors. Moreover, GWaltz can well maintain the ellipse shape with the 80thpercentile eccentricity error and phase error about 0.16 and 0.42??????, respectively. We also compare GWaltz with its variant that only uses GMR signals contained in the detected LOS-GMR area. The so-called GWaltz-LOS variant shares the whole processing pipeline with GWaltz and only abandons part of GMR signals before observation selection. The results show GWaltz can achieve 2.86×, 2.25× and 1.30× improvements in the orbit distance, eccentricity error and phase error, respectively. This indicates the effectiveness of GWaltz’s exploitation in ghost multipath reflections.

5.2.2 Performance and Measuring Distance. We evaluate GWaltz under the conditions of different measuring distances (60???? ∼ 150????). The reflector distance and the rotating speed are set to 30???? and 2000?????? respectively.

![](images/2e11a7bf4e2ee3e8fce57b2dce72157d26797136fb463ff445c1c3bb22435af4.jpg)



(a) Impact of Workload Condition

![](images/7bf4c7fb370d73868e84f5c9892cf35fd8ed9b729e532817265045283ecebde1.jpg)



(b) Impact of Multipath Condition

![](images/9f2816d4b69c72d6bf5ac2b4b52fe95e2728bbad52a5e720190eba48c39595fd.jpg)



(c) Impact of Extra Reflector   
Figure 17: Performance with practical factors.

The results are shown in Fig. 16(a). The red bars depict the average absolute errors of the orbit restoration, and their error bars stand for corresponding standard deviations. The stacked blue & yellow bars stand for the average normalized errors of the shape features. We normalize the phase errors to [0, 1] with the value range of [0, ??/2] since the maximum angle between the major axes of two ellipses will not exceed $\pi / 2 .$ . Because the eccentricity of an ellipse belongs to [0, 1), we keep the eccentricity errors unchanged. The stacked bar, i.e., the sum of the normalized shape features (denoted by shape errors below), measures the ability of the shape estimation.

The average orbit distances are 6.62????, 3.99????, 5.53???? and 7.26???? respectively, and the shape errors are 0.35, 0.34, 0.39 and 0.49 respectively. The results show that both orbit errors and shape errors do not increase significantly along with the measuring distance. Since GWaltz has a good performance in relatively long measuring distances, its capability of wireless and non-contact working manner significantly surpasses traditional approaches.

5.2.3 Performance and Reflector Distance. We evaluate GWaltz under the conditions of different reflector distances (15???? ∼ 60????). The measuring distance and the rotating speed are set to 90???? and 2000?????? respectively. Fig. 16(b) shows the average orbit distances are 7.26????, 7.28????, 7.01???? and 8.85???? respectively, and the shape errors are 0.29, 0.34, 0.72 and 0.48 respectively. The errors are acceptable in these cases, although they increase slightly with the increasing reflector distance. We observe the ERAM of the 60???? case and find the magnitudes of NLOS GMRs in it are indeed much weaker than the 15???? case. This relatively long distance indicates that when measuring orbits for horizontally placed rotors in practice, we can probably leverage the GMRs from the floor or pillars to provide multi-angle observations.

5.2.4 Performance and Rotating Speed. We evaluate GWaltz under the conditions of different rotating speeds (1000?????? ∼ 2500??????). The measuring distance and the reflector distance are set to 90???? and 30???? respectively. Fig. 16(c) shows the

average orbit distances are 5.83????, 7.90????, 4.15????, and 7.63???? respectively, and the shape errors are 0.72, 1.13, 0.41 and 0.51 respectively. We find the performance of GWaltz obviously degrades in low-speed cases. This is because when the input power is constant, the lower the rotating speed, the higher the 2D vibration amplitude. However, it’s difficult for the system to determine the cause of an extract displacement with a large amplitude when processing NLOS GMRs: it can result from a large-amplitude motion of the target or just the estimation error when SNR is limited. Therefore, we believe that further improving the displacement extraction from GMR signals is necessary in the future design of GWaltz.

# 5.3 Impact of Practical Factors

Next, we evaluate the impacts of two practical factors, workload, and multipath conditions. We also discuss the necessity of adding extra metal reflectors to improve the performance. The measuring distance, reflector distance, and rotating speed are set to 90????, 30????, and 2000?????? respectively.

5.3.1 Impact of Workload Condition. We add the same amount of water to the 6 evenly-placed test tubes of the centrifuge to control its workload. When there are 0 or 6 test tubes occupied with water, the machine, and its orbit is stable. However, when 2 or 4 test tubes are occupied, the centrifuge works in an unstable state because its center of mass is not in a balanced position.

Fig. 17(a) shows the average orbit distances are 6.95????, 8.14????, 12.08???? and 5.26???? respectively, and the shape errors are 0.39, 0.83, 1.07 and 0.54 respectively. GWaltz works well in stable states, but its performance degrades in unstable states. For unstable states, both the diameter and the eccentricity of the orbits are larger than those of stable states. Thus, the reason for the poor performance is similar to that in §5.2.4, and there’s still room for improvement in the accurate displacement extraction from NLOS GMR signals.

5.3.2 Impact of Multipath Condition. As shown in Fig. 13, we change multipath conditions from mild (one wooden table), moderate (one wall) to rich (two walls) to evaluate

![](images/e24b030aa4a3148068c78621c7099abb50e8f4a7d43d1649f25d573a4d89b9b3.jpg)



(a) Experiment Setup

![](images/0c82ae2e7f4b2df7a66fa6e0e1833c1184643b05198cc6b8dcc37dea4712fc1c.jpg)



(b) Measurement Results   
Figure 18: Measuring the 2D orbit of a fan.

GWaltz. Fig. 17(b) shows the average orbit distances are 4.98????, 7.41????, and 7.51???? respectively, and the shape errors are 0.97, 0.32, and 0.63 respectively. Since GWaltz exploits ambient multipath reflections, basically richer multipath condition tends to achieve better performance. The performance in the moderate condition is good enough, which relaxes the requirements for system deployment.

5.3.3 Necessity of Dedicated Reflector. We place several metal plates with different sizes (diameter of 10????, 20???? and 30????) close to the wall to see whether the metal reflector help GWaltz produce better results or not. Fig. 17(c) shows the average orbit distances are 5.14????, 5.32????, 6.68????, and 4.30???? respectively, and the shape errors are 0.38, 0.31, 0.36 and 0.50 respectively. The results suggest that there is no obvious improvement when we dedicatedly place the metal reflectors instead of leveraging ambient reflectors.

5.3.4 Availability of Floor as Reflector. We also measure the 2D orbit of a fan with GWaltz as shown in Fig 18(a). Since the fan’s central axis is parallel to the ground, the floor is the only ambient reflector we reckon on. We repeat the measurement for about 50 times, and the statistical results in Fig 18(a). The average orbit distance is 13.95???? for the fan with about 220????-diameter 2D trajectory, while the eccentricity error and orbit phase error are also small. The good and relatively consistent results demonstrate the availability of the floor as the only reflector.

# 5.4 Micro Benchmarks

In this section, we run some microbenchmarks on GWaltz.

5.4.1 Accuracy and Correctness of 1D Displacement Extraction. One of the contributions of GWaltz is to ensure the correctness and improve the accuracy of 1D displacement extraction. Fig. 19 shows the amplitude and frequency estimation errors along the X-axis and Y-axis when the measuring distance increases. We define the X-axis as the LOS direction and the Y-axis as its perpendicular direction. Note that the 1D displacement along the X-axis is extracted from the LOS GMR signal, while the 1D displacement along the Y-axis is derived from the projection of the 2D orbit to that direction.

For the correctness, we can see that the frequency estimation errors are all no more than 0.5????, which means Module 2 has extracted the correct displacement sequences. For accuracy, due to the high SNR of the LOS GMR signal, the amplitude estimation errors along the X-axis are basically lower than those along the Y-axis. Nevertheless, the errors of those inferred 1D displacements are no more than 8???? in most cases, which demonstrates our system can accurately measure 2D rotor motion to a certain extent.

5.4.2 System Stability. Next, we evaluate the stability of 3 key functions of GWaltz in terms of GMR detection, 1D observation selection, and 2D restoration. Since our centrifuge can continuously work for about 20 minutes, we collect the mmWave data once every 4 minutes.

(1) Stability of GMR Detection: GMR detection is the 1st function of GWaltz whose stability acts as the prerequisite of the stability of the whole system. We calculate the average intersection over union (IoU) [29] between the GMR areas at time ?? = 0 and those at later times. The line plot in Fig. 20(a) shows that the average IoUs are around 0.9, which means the GMR area detections are highly consistent across time.   
(2) Stability of Observation Selection: Then, we calculate the distances between the aggregated candidate locations across time as the metric for the stability of the 3rd module. The unit of this metric is "bin", i.e., the range or angular bin. The bar plot in Fig. 20(a) proves the stability since both the median distances and their quartile ranges are very small and relatively stable.   
(3) Stability of Orbit Restoration: At last, we evaluate the stability of the 4th module by visualizing 3 shape features, i.e., major-axis length, eccentricity, and orbit phase, across time. The results in Fig. 20(b) illustrate that these shape features achieve relatively high stability in most cases.

5.4.3 Processing Efficiency. At last, we test the processing efficiency of GWaltz. We collect each module’s running time when processing each frame of the entire dataset and show their median values in Fig. 21 The results show that 1D processing uses about 2.16??, almost 80% of processing time, while 2D orbit restoration uses about 0.60??. We find during 1D processing, RBF in the 1st module and fitting process in the 2nd module are the most time-consuming parts. To improve the time efficiency, we can run these two modules in parallel due to the high locality of their input data.

# 6 RELATED WORKS

# 6.1 RF-based Micro-movement Sensing

RF-based wireless sensing is a new family of non-intrusive measurement technologies that have been widely explored in industrial applications recently [9, 11, 12, 15, 18, 25, 45]. In this subsection, we review the most related literature of GWaltz in micro-movement sensing with RF signals.

![](images/3d6bf3e530afffdab8c01885801a045458af474b7a8928a328386c226f8bdbaf.jpg)



Figure 19: Vibration accuracy evaluation.

![](images/8c0e3d5460feb4fbe72d1cffdede655341a3e75a41303c2d38ded66ea603ffc5.jpg)



(a) Detection & Selection

![](images/f910115c33d6e370c751a0daba4d6f46bb7501c4c3da5335cebffbb70c4d5519.jpg)



(b) Orbit Restoration

![](images/386d58b7b82a2d773aa77aaa2e62d60011187607da6dba61a5973651c3d31a58.jpg)



Figure 21: Efficiency test.   
Figure 20: Stability evaluation.

Mechanical Vibration Measurement: Recently, several works have been proposed to measure mechanical vibrations of industrial machines. For the longer-wavelength RF signals, e.g., RFID, Tagbeat manages to estimate the frequency of ????-level mechanical vibrations [45]. Shorter-wavelength RF signals have the opportunity to restore original waveforms of vibration signals, e.g., ART turns a 2.4?????? signal to a wireless vibrometer [41]. Compared to these works, we believe mmWave is a better choice to measure sub-????- level vibrations. Moreover, GWaltz focuses on extracting 2D micro-movements rather than just measuring 1D vibrations.

mmWave Micro-movement Measurement: The sensitivity to micro-movement of mmWave is much higher due to its short wavelength. Therefore, apart from positioning [3, 24, 43], tracking [42, 48], imaging [25, 47, 49], gesture recognition [20, 31, 38] and material recognition [19, 44], mmWave is more competitive in continuous micromovement sensing, e.g., measuring vibrations of the machine surface [15], the water surface [36], the chest [5, 10, 22, 46], and etc. Similarly, GWaltz shares basic ideas of (i) translating signal’s phase changes to 1D displacements and (ii) imaging a rigid-body with reflections from different parts on its surface. But we make extra contributions by studying the properties of mmWave GMRs and conquering critical challenges when exploiting them to measure 2D micro-movements.

# 6.2 Multipath Exploitation

Traditionally, the multipath effect is considered as the main interference for wireless communication and sensing [21, 37]. Nowadays, the increasing size of antenna arrays has improved the spatial separability of multipath reflections, which makes researchers consider exploiting the extra information contained in them.

Since multipath reflections create ghost images of the target, traditional approaches manage to detect and eliminate

GMRs, either through dedicated algorithms [30] or specialized hardware, [39]. Recent studies find ghost images sharing the same motion characteristics with the intrinsic image [16] can improve the positioning performance: the intrinsic image provides the basic location while ghost images from prior known reflectors further revise the positioning result [17, 32]. Moreover, several recent works extend this positioning mechanism to localize the speaker with the help of audio GMRs [33, 40]. GWaltz differs from the above works because it explores the properties of GMRs to reveal micromovements and form multi-angle but coherent observations of the same target.

# 7 CONCLUSION

In this work, we present GWaltz, a mmWave sensing system that manages to measure sub-????-level 2D rotor orbits by exploiting ghost multipath reflections. GWaltz provides an in-depth analysis of the relationship between the rotor orbit and GMR signals and studies the orbit restoration problem under poor signal quality. Our evaluations show that GWaltz achieves an absolute error of about 8.42???? and well restores the shape features when measuring 100????-diameter orbits.

For future work, we plan to deploy an embedded version of GWaltz in the real-world industrial environment to measure the rotor orbits of large rotating machinery like pumps and generators. We believe there could still be plenty of critical challenges to solve during the field studies.

# ACKNOWLEDGMENTS

We are sincerely grateful to all the anonymous reviewers for their valuable and constructive comments. This work was jointly supported by National Key Research and Development Program of China No. 2017YFB1003000, National Natural Science Foundation of China No. 61902213, Nanjing Nangang Industrial IoT Research Fund, and the Research and Development Project of Key Core Technology and Generic Technology in Shanxi Province under Grant 2020XXX007.

# REFERENCES

[1] Maurice L. Adams. 2009. Rotating Machinery Vibration: From Analysis to Troubleshooting. CRC Press.   
[2] N. Bachschmid, P. Pennacchi, and A. Vania. 2004. Diagnostic Significance of Orbit Shape Analysis and its Application to Improve Machine Fault Detection. Journal of the Brazilian Society of Mechanical Sciences and Engineering 26, 2 (2004), 200–208.   
[3] Guillermo Bielsa, Joan Palacios, Adrian Loch, Daniel Steinmetzer, Paolo Casari, and Joerg Widmer. 2018. Indoor Localization using Commercial Off-The-Shelf 60GHz Access Points. In Proceedings of IEEE INFOCOM, Honolulu, HI, USA, April 16-19, 2018. IEEE, 2384–2392.   
[4] Keyence Corporation. 2020. Eddy-Current Displacement Sensor. https://www.keyence.com/ss/products/measure/ measurement\_library/type/inductive/.   
[5] Lei Ding, Murtaza Ali, Sujeet Patole, and Anand Dabak. 2016. Vibration Parameter Estimation using FMCW Radar. In Proceedings of IEEE ICASSP, Shanghai, China, March 20-25, 2016. IEEE, 2224–2228.   
[6] Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu, et al. 1996. A Density-based Algorithm for Discovering Clusters in Large Spatial Databases with Noise. In Proceedings of AAAI KDD, Portland, Oregon, USA, August 2–4, 1996. AAAI, 226–231.   
[7] Walter Gander, Gene H. Golub, and Rolf Strebel. 1994. Least-Squares Fitting of Circles and Ellipses. BIT Numerical Mathematics 34, 4 (1994), 558–578.   
[8] Paul Goldman and Agnes Muszynska. 1999. Application of Full Spectrum to Rotating Machinery Diagnostics. Orbit 20, 1 (1999), 17–21.   
[9] Junchen Guo, Ting Wang, Yuan He, Meng Jin, Chengkun Jiang, and Yunhao Liu. 2019. TwinLeak: RFID-based Liquid Leakage Detection in Industrial Environments. In Proceedings of IEEE INFOCOM, Paris, France, April 29 - May 2, 2019. IEEE, 883–891.   
[10] Unsoo Ha, Salah Assana, and Fadel Adib. 2020. Contactless Seismocardiography via Deep Learning Radars. In Proceedings of ACM MobiCom, Virtual Event, September 21-25, 2020. ACM, 62:1–62:14.   
[11] Yuan He, Junchen Guo, and Xiaolong Zheng. 2018. From Surveillance to Digital Twin: Challenges and Recent Advances of Signal Processing for Industrial Internet of Things. IEEE Signal Processing Magazine 35, 5 (2018), 120–129.   
[12] Yuan He, Yilun Zheng, Meng Jin, Songzhen Yang, Xiaolong Zheng, and Yunhao Liu. 2021. RED: RFID-based Eccentricity Detection for High-Speed Rotating Machinery. IEEE Transactions on Mobile Computing 20, 4 (2021), 1590–1601.   
[13] Texas Instruments. 2020. IWR1642: Single-Chip 76GHz to 81GHz mmWave Sensor Integrating DSP and MCU. http://www.ti.com/ product/IWR1642.   
[14] Texas Intruments. 2020. Introduction to mmWave Sensing: FMCW Radars. https://training.ti.com/intro-mmwave-sensing-fmcw-radarsmodule-1-range-estimation.   
[15] Chengkun Jiang, Junchen Guo, Yuan He, Meng Jin, Shuai Li, and Yunhao Liu. 2020. mmVib: Micrometer-Level Vibration Measurement with mmWave Radar. In Proceedings of ACM MobiCom, Virtual Event, September 21-25, 2020. ACM, 45:1–45:13.   
[16] Alexander Kamann, Patrick Held, Florian Perras, Patrick Zaumseil, Thomas Brandmeier, and Ulrich T. Schwarz. 2018. Automotive Radar Multipath Propagation in Uncertain Environments. In Proceedings of IEEE International Conference on Intelligent Transportation Systems, Maui, HI, USA, November 4-7, 2018. IEEE, 859–864.   
[17] Michael Leigsnering, Fauzia Ahmad, Moeness G. Amin, and Abdelhak M. Zoubir. 2015. Compressive Sensing-based Multipath Exploitation for Stationary and Moving Indoor Target Localization. IEEE Journal of Selected Topics in Signal Processing 9, 8 (2015), 1469–1483.   
[18] Ping Li, Zhenlin An, Lei Yang, and Panlong Yang. 2019. Towards Physical-Layer Vibration Sensing with RFIDs. In Proceedings of IEEE

INFOCOM, Paris, France, April 29 - May 2, 2019. IEEE, 892–900.   
[19] Zhengxiong Li, Baicheng Chen, Zhuolin Yang, Huining Li, Chenhan Xu, Xingyu Chen, Kun Wang, and Wenyao Xu. 2019. FerroTag: a Paperbased mmWave-Scannable Tagging Infrastructure. In Proceedings of ACM SenSys, New York, NY, USA, November 10-13, 2019. ACM, 324–337.   
[20] Jaime Lien, Nicholas Gillian, M. Emre Karagozler, Patrick Amihood, Carsten Schwesig, Erik Olson, Hakim Raja, and Ivan Poupyrev. 2016. Soli: Ubiquitous Gesture Sensing with Millimeter Wave Radar. ACM Transactions on Graphics 35, 4 (2016), 142:1–142:19.   
[21] Chris Xiaoxuan Lu, Stefano Rosa, Peijun Zhao, Bing Wang, Changhao Chen, Niki Trigoni, and Andrew Markham. 2020. See through Smoke: Robust Indoor Mapping with Low-Cost mmWave Radar. In Proceedings of ACM MobiSys, Virtual Event, June 15-19, 2020. ACM, 14–27.   
[22] Ilya V. Mikhelson, Sasan Bakhtiari, Thomas W. Elmer, Alan V. Sahakian, et al. 2011. Remote Sensing of Heart Rate and Patterns of Respiration on a Stationary Subject using 94GHz Millimeter-Wave Interferometry. IEEE Transactions on Biomedical Engineering 58, 6 (2011), 1671–1677.   
[23] Caner Ozdemir. 2012. Inverse Synthetic Aperture Radar Imaging with MATLAB Algorithms. Vol. 210. John Wiley & Sons.   
[24] Ioannis Pefkianakis and Kyu-Han Kim. 2018. Accurate 3D Localization for 60GHz Networks. In Proceedings of ACM SenSys, Shenzhen, China, November 4-7, 2018. ACM, 120–131.   
[25] Akarsh Prabhakara, Vaibhav Singh, Swarun Kumar, and Anthony Rowe. 2020. Osprey: A mmWave Approach to Tire Wear Sensing. In Proceedings of ACM MobiSys, Virtual Event, June 15-19, 2020. ACM, 28–41.   
[26] Alexander Prokhorov. 2012. Effective Emissivities of Isothermal Blackbody Cavities Calculated by the Monte Carlo Method using the Three-Component Bidirectional Reflectance Distribution Function Model. Applied Optics 51, 13 (2012), 2322–2332.   
[27] Mark A. Richards. 2005. Fundamentals of Radar Signal Processing. McGraw-Hill Education.   
[28] Hermann Rohling. 1983. Radar CFAR Thresholding in Clutter and Multiple Target Situations. IEEE Trans. Aerospace Electron. Systems 4 (1983), 608–621.   
[29] Adrian Rosebrock. 2016. Intersection over Union for Object Detection. https://www.pyimagesearch.com/2016/11/07/intersection-overunion-iou-for-object-detection/.   
[30] In-hwan Ryu, Insu Won, and Jangwoo Kwon. 2018. Detecting Ghost Targets using Multi-Layer Perceptron in Multiple-Target Tracking. Symmetry 10, 1 (2018), 16.   
[31] Panneer Selvam Santhalingam, Al Amin Hosain, Ding Zhang, Parth Pathak, Huzefa Rangwala, and Raja Kushalnagar. 2020. mmASL: Environment-Independent ASL Gesture Recognition Using 60GHz Millimeter-Wave Signals. Proceedings of ACM IMWUT 4, 1 (2020), 1–30.   
[32] Pawan Setlur, Moeness Amin, and Fauzia Ahmad. 2011. Multipath Model and Exploitation in Through-the-Wall and Urban Radar Sensing. IEEE Transactions on Geoscience and Remote Sensing 49, 10 (2011), 4021– 4034.   
[33] Sheng Shen, Daguan Chen, Yulin Wei, Zhijian Yang, and Romit Roy Choudhury. 2020. Voice Localization using Nearby Wall Reflections. In Proceedings of ACM MobiCom, Virtual Event, September 21-25, 2020. ACM, 7:1–7:14.   
[34] Petre Stoica, Randolph L. Moses, et al. 2005. Spectral Analysis of Signals. Pearson Prentice Hall Upper Saddle River, NJ.   
[35] Petre Stoica, Zhisong Wang, and Jian Li. 2006. Robust Capon Beamforming. Signal Processing Letters IEEE 10, 6 (2006), 172–175.   
[36] Francesco Tonolini and Fadel Adib. 2018. Networking across Boundaries: Enabling Wireless Communication through the Water-Air Interface. In Proceedings of ACM SIGCOMM, Budapest, Hungary, August 20-25, 2018. ACM, 117–131.

[37] David Tse and Pramod Viswanath. 2005. Fundamentals of Wireless Communication. Cambridge University Press.   
[38] Luc Vignaud, Antoine Ghaleb, Julien Le Kernec, and Jean-Marie Nicolas. 2009. Radar High Resolution Range & Micro-Doppler Analysis of Human Motions. In Proceedings of IEEE International Radar Conference, Pasadena, CA, USA, May 4-8, 2009. IEEE, 1–6.   
[39] Tristan Visentin, Jürgen Hasch, and Thomas Zwick. 2018. Analysis of Multipath and DOA Detection using a Fully Polarimetric Automotive Radar. International Journal of Microwave and Wireless Technologies 10, 5-6 (2018), 570–577.   
[40] Weiguo Wang, Jinming Li, Yuan He, and Yunhao Liu. 2020. Symphony: Localizing Multiple Acoustic Sources with a Single Microphone Array. In Proceedings of ACM SenSys, Virtual Event, November 16-19, 2020. ACM, 82–94.   
[41] Teng Wei, Shu Wang, Anfu Zhou, and Xinyu Zhang. 2015. Acoustic Eavesdropping through Wireless Vibrometry. In Proceedings of ACM MobiCom, Paris, France, September 7-11, 2015. ACM, 130–141.   
[42] Teng Wei and Xinyu Zhang. 2015. mTrack: High-Precision Passive Tracking using Millimeter Wave Radios. In Proceedings of ACM Mobi-Com, Paris, France, September 7-11, 2015. ACM, 117–129.   
[43] Teng Wei, Anfu Zhou, and Xinyu Zhang. 2017. Facilitating Robust 60GHz Network Deployment by Sensing Ambient Reflectors. In Proceedings of USENIX NSDI, Boston, MA, USA, March 27-29, 2017. USENIX,

213–226.   
[44] Chen Shu Wu, Feng Zhang, Bei Bei Wang, and KJ Ray Liu. 2020. mSense: Towards Mobile Material Sensing with a Single Millimeter-Wave Radio. Proceedings of ACM IMWUT 4, 3 (2020), 1–20.   
[45] Lei Yang, Yao Li, Qiongzheng Lin, Huanyu Jia, Xiang-Yang Li, and Yunhao Liu. 2017. Tagbeat: Sensing Mechanical Vibration Period with COTS RFID Systems. IEEE/ACM Transactions on Networking 25, 6 (2017), 3823–3835.   
[46] Zhicheng Yang, Parth H. Pathak, Yunze Zeng, Xixi Liran, and Prasant Mohapatra. 2016. Monitoring Vital Signs using Millimeter Wave. In Proceedings of ACM MobiHoc, Paderborn, Germany, July 4-8, 2016. ACM, 211–220.   
[47] Feng Zhang, Chen Shu Wu, Bei Bei Wang, and KJ Ray Liu. 2020. mm-Eye: Super-Resolution Millimeter Wave Imaging. IEEE Internet of Things Journal 1, 1 (2020), 1–20.   
[48] Anfu Zhou, Shaoyuan Yang, Yi Yang, Yuhang Fan, and Huadong Ma. 2019. Autonomous Environment Mapping Using Commodity Millimeter-Wave Network Device. In Proceedings of IEEE INFOCOM, Paris, France, April 29 - May 2, 2019. IEEE, 1126–1134.   
[49] Yanzi Zhu, Yibo Zhu, Ben Y. Zhao, and Haitao Zheng. 2015. Reusing 60GHz Radios for Mobile Radar Imaging. In Proceedings of ACM Mobi-Com, Paris, France, September 7-11, 2015. ACM, 103–116.