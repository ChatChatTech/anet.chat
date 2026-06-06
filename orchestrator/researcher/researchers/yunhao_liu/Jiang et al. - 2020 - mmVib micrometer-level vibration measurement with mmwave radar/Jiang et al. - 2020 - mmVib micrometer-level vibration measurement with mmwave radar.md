# mmVib: Micrometer-Level Vibration Measurement with mmWave Radar

Chengkun Jiang

School of Software and BNRist,

Tsinghua University

ahczjck@gmail.com

Meng Jin

School of Software and BNRist, Tsinghua University

mengj@tsinghua.edu.cn

Junchen Guo

School of Software and BNRist, Tsinghua University

gjc16@mails.tsinghua.edu.cn

Shuai Li

School of Software and BNRist, Tsinghua University

lis20@mails.tsinghua.edu.cn

Yuan He

School of Software and BNRist, Tsinghua University

heyuan@tsinghua.edu.cn

Yunhao Liu

Tsinghua University & MSU yunhao@greenorbs.com

# ABSTRACT

Vibration measurement is a crucial task in industrial systems, where vibration characteristics reflect the health and indicate anomalies of the objects. Previous approaches either work in an intrusive manner or fail to capture the micrometer-level vibrations. In this work, we propose mmVib, a practical approach to measure micrometer-level vibrations with mmWave radar. By introducing a Multi-Signal Consolidation (MSC) model to describe the properties of the reflected signals, we exploit the inherent consistency among those signals to accurately recover the vibration characteristics. We implement a prototype of mmVib, and the experiments show that this design achieves 8.2% relative amplitude error and 0.5% relative frequency error in median. Typically, the median amplitude error is 3.4???? for the 100????-amplitude vibration. Compared to two existing approaches, mmVib reduces the 80??ℎ-percentile amplitude error by 62.9% and 68.9% respectively.

# CCS CONCEPTS

• Networks → Cyber-physical networks; • Computer systems organization → Embedded and cyber-physical systems.

# KEYWORDS

Wireless Sensing, Millimeter Wave, Vibration Measurement

# ACM Reference Format:

Chengkun Jiang, Junchen Guo, Yuan He, Meng Jin, Shuai Li, and Yunhao Liu. 2020. mmVib: Micrometer-Level Vibration Measurement with mmWave Radar. In The 26th Annual International Conference on Mobile Computing and Networking (MobiCom ’20), September 21–25, 2020, London, United Kingdom. ACM, New York, NY, USA, 13 pages. https://doi.org/ 10.1145/3372224.3419202

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

MobiCom ’20, September 21–25, 2020, London, United Kingdom

© 2020 Association for Computing Machinery.

ACM ISBN 978-1-4503-7085-1/20/09. . . \$15.00

https://doi.org/10.1145/3372224.3419202

![](images/e89cda979f20f555efad3695321e346d78e33b0a4a3848a1794cb030b4048969.jpg)



Figure 1: Vibration measurement with mmVib

# 1 INTRODUCTION

Vibration is the most common phenomenon in industry. Vibration of the industrial objects generally reflects their internal states. Damage or malfunction of the objects usually leads to abnormal changes in the vibration characteristics [8]. Vibration measurement, namely to measure the vibration amplitude and frequency, is a crucial task in various industrial scenarios for checking machinery health, identifying anomalies, and diagnosing faults [1, 8, 13].

Conventional approaches for vibration measurement rely on specialized sensors like piezoelectric sensors [9, 20] or optical devices like laser vibrometers [6, 27]. Specialized sensors require to be directly installed on the vibrating object, which means high complexity in deployment and maintenance. Optical devices often have high precision and accuracy, but their prohibitive cost prevents them from being widely used in real application scenarios. The table in Fig. 1 shows a brief comparison of vibration measurement approaches [6, 9].

With the rapid progress in wireless sensing, recent works propose to exploit wireless signals, e.g. acoustic signal [21, 31] and radio frequency (RF) signal [18, 32, 36], for vibration measurement. The vibrating object is a physical reflector of the wireless signal, so that the vibration affects the propagation of the reflected signal. By measuring and analyzing the reflected signal, one can obtain the vibration characteristics. Compared to conventional approaches, the measurement based on wireless sensing is low-cost and easy to deploy in practice. However, its precision is often limited, due to the relatively long wavelengths of the employed wireless technologies, while the vibration amplitudes of a large number of machines in the industry do not exceed 100???? [1, 8].

mmWave is a promising technology for measuring tiny displacements, owing to its short wavelength. Recent works propose to use mmWave in different sensing applications [7, 11, 16, 19, 23, 29, 33, 35, 37, 42]. But those approaches cannot provide highly precise and accurate vibration measurement in the industrial scenarios. Fig. 1 shows a typical industrial environment, from which we can perceive the following challenges. First, the industrial environments are multipath-rich environments. Although mmWave has better directionality than the conventional wireless signals, the received signal at the antenna is still a mix of the signals reflected from both the vibrating object and other reflectors in the environment. Second, the vibration of the industrial objects is often at the micrometer level [1, 8]. The signal changes caused by such vibration are easily affected by the noise in the signal. Due to the above reasons, the vibration-induced changes in the reflected signal are obscured and distorted, making it extremely difficult to extract accurate vibration characteristics.

In this work, we address the above challenges and propose mmVib, a practical approach to measure the micrometer-level vibration with mmWave radar. We propose a multi-signal consolidation model (MSC) that describes the properties of the reflected signals in the In-phase and Quadrature (IQ) domain and exploit the inherent consistency among those signals to accurately recover the vibration characteristics. Our contributions are summarized as follows:

• We propose MSC, a signal model that comprehensively describes the composition of the reflected mmWave signals. MSC captures the multi-frequency and multi-antenna properties of the reflected signal from the vibrating object in the multipath-rich environments.   
• Based on MSC, the design of mmVib addresses critical challenges in achieving the micrometer-level accuracy: (i) pinpointing the vibrating object in the mixed reflected signal; (ii) recovering the micrometer-level vibration under the influence of noise and other reflected signals.   
• We implement mmVib on the commercial off-the-shelf (COTS) mmWave radar and evaluate its performance in both lab and real-world environments. The results show that mmVib achieves 8.2% relative amplitude error and 0.5% relative frequency error in median. Typically, the median amplitude error is 3.4???? for the 100????-amplitude vibration. Compared to two existing approaches, mmVib reduces the 80??ℎ-percentile amplitude error by 62.9% and 68.9% respectively.

The rest of the paper is organized as follows: §2 introduces the preliminaries of vibration measurement with mmWave radar. We present the MSC model in §3 and the design of mmVib in §4. §5 discusses the limitations of mmVib. §6 presents implementation details and evaluation results. §7 discusses the related works. We conclude mmVib and discuss future works in §8.

![](images/a74200c895a9fe94101c6440e081a7886b76400e7253097f921cbc43a06956d2.jpg)



(a) High amplitude estimation errors

![](images/7c8ed948be85a7efe5ba60e4774d3f13a54a96b4bd37621542acfb114c9f94a0.jpg)



(b) Impact of metal reflectors   
Figure 2: Direct estimation based on phase change

# 2 PRELIMINARIES

In this section, we first introduce the principles of using mmWave to measure the displacement and then analyze why it can’t be directly used for the micrometer-level vibration measurement in industry.

# 2.1 Estimate Displacement with mmWave

The core idea to track the displacement of the target with wireless technologies is to extract the phase changes of the received signal reflected from the target:

$$
\Delta d = \lambda \frac {\Delta \phi}{2 \pi} \tag {1}
$$

where ?? is the wavelength. The phase change ???? acts as a stable and accurate indicator of the propagation distance change ????, compared to other signal features like RSS. Therefore, the millimeterlevel wavelength of mmWave endows it with over 25× and 65× higher sensitivity to tiny displacements, compared to WiFi and RFID respectively. That’s why mmWave is deemed to be a promising technology for measuring mechanical vibrations in industrial scenarios, where the vibration amplitude typically does not exceed 100????. However, our experiments provide a different observation. We configure a vibration calibrator (the vibrating object we use and introduce in §6.1) to vibrate with different amplitudes (30 ∼ 200????) and 100???? frequency. Fig. 2(a) shows the errors of the vibration characteristics that are directly estimated based on phase change. The results show that the frequency estimation is consistently accurate while the relative errors of the amplitude estimation are over 80%. The accuracy of the frequency estimation indicates that we have indeed extracted the vibration signal. But the amplitude errors are too large to correctly characterize the vibration. In order to find out the reason behind, we take a deep look at the signal processing of mmWave radar in the next subsection.

# 2.2 Phase Extracted from mmWave Radar

mmWave radar usually adopts frequency-modulated continuous wave (FMCW) chirp signals for distance measurement, as shown in Fig. 3. The frequency difference between the transmitted signal (Tx) and the received signal (Rx) indicates the signal propagation time, which can be used to determine the object distance. Denoting the time-variant distance between the antenna and the vibrating object by ??(??), the transmitted and received signal can be expressed by:

![](images/bc8b88fd6a90e4a26ea1e1713a2226e9b6ad0c532f5b5bdf8c2b49e5bcf4557c.jpg)



Figure 3: FMCW chirp signals

$$
S _ {T x} (t) = \exp \left[ j \left(2 \pi f _ {c} t + \pi K t ^ {2}\right) \right] \tag {2}
$$

$$
S _ {R x} (t) = \alpha S _ {T x} [ t - 2 R (t) / c ]
$$

where ?? is the path loss. ???? and ?? are the starting frequency and the chirp slope of FMCW signal respectively. Then a mixer is used to eliminate the carrier wave in the received signal and obtain the so-called beat frequency signal ?? (?? ) as:

$$
s (t) = S _ {T x} ^ {*} (t) S _ {R x} (t) \approx \alpha \exp [ j 4 \pi (f _ {c} + K t) R (t) / c ] \tag {3}
$$

whose phase values contain the distance information ??(??).

In practice, there exist reflected signals from different distances, which cause different frequency components in ?? (??). In order to extract the desired signal from ??(??), a Range-FFT operation [7, 19] is conducted on the samples of ?? (??) within a chirp (denoted as the fast-time samples) for the signal separation. As shown in Fig. 3, this operation maps the frequency spectrum of ?? (??) to the range spectrum indicating the distances of different reflectors. Since the elapsed time of a chirp is around 0.1????, the displacement during this period can be neglected and we only focus on the displacements across consecutive chirps. Therefore, in the Range-FFT results of each chirp, we pick up one sample in each range bin. Then, in a certain range bin, combining those samples (denoted as slow-time samples) forms a sample sequence of 10?????? sampling rate. If we rewrite the object range ?? (?? ) as $R ( t ) = R _ { 0 } + x ( t )$ , where ?? (?? ) is the vibration displacement within the range-bin resolution and ??0 is the object-radar distance, the reflected signal ?? (??) from the object range bin can be represented as:

$$
s (t) \xrightarrow [ \text { at   object   range   bin } ]{\text { Range - FFT }} S (t) = \alpha \exp \left[ j 4 \pi f _ {c} (R _ {0} + x (t)) / c \right] \tag {4}
$$

Then, we can estimate the velocity of ?? (??) by performing another FFT operation called Doppler-FFT on ?? (??). Fig. 4 shows the Range-Doppler spectrum that can detect the existence of the reciprocating motion of a vibrating object. So why can’t the phase change correctly recover the vibration displacement? Actually, ?? (??) is composed of all the reflected signals from the range bin of the vibrating object. Thus, ?? (??) can’t be directly derived with the phase values of ?? (??). Fig. 2(b) shows that the estimation error increases when we

![](images/bc6c47300995aaca2ce3ab4caf6fc7254d8275de1532794d9b4a8dc0341eb809.jpg)



Figure 4: Range-Doppler spectrum

deliberately place multiple metal reflectors in the same range bin, which further verifies the above statement.

Another often neglected fact is that the measurement accuracy is also seriously affected by the signal noise, especially for tiny vibrations. For instance, a 100???? vibration only results in about 0.12?????? phase change, which is very sensitive to the signal noise.

Therefore, to achieve accurate vibration measurement, two critical factors should be properly and carefully considered: (i) other reflected signals entangled with the vibration reflection; (ii) the noise in the phase values.

# 3 MODELING THE VIBRATION

In this section, we introduce the MSC model, which acts as the theoretical foundation of mmVib.

# 3.1 Identifying the Signal in the IQ domain

According to Eq. 4, the reciprocating motion can change the signal phase within a certain range, which means the signal samples plotted in the IQ domain can form an arc-shaped trajectory centered at the origin of coordinates. To verify this, we measure the vibrations of 100???? and 200???? amplitudes with 1?? and 2?? distances away from the radar. The corresponding IQ signal samples are shown in Fig. 6(a).

There indeed exist arc-shaped trajectories: the central angles of the arcs are proportional to their amplitudes, but their centers are obviously not at the origin. The relationship between the central angle and the vibration amplitude is reasonable because the vibration displacement linearly changes the signal phase. For example, the central angle of the 100???? vibration is about the half of the central angle of the 200???? vibration. As for the center coordinates, their offsets from the origin are due to the impact of other reflected signals from the same range bin of the vibrating object. Actually, the theoretical derivation of Eq. 4 only considers the vibration reflection from the object. So in MSC, we modify it to also consider the background reflections:

$$
\begin{array}{l} S ^ {\prime} (t) = \alpha e x p [ j 4 \pi f _ {c} (R _ {0} + x (t)) / c ] + \sum_ {i} \alpha_ {B} ^ {[ i ]} e x p [ j 4 \pi f _ {c} R _ {B} ^ {[ i ]} / c ] \\ = \alpha e x p [ j 4 \pi f _ {c} (R _ {0} + x (t)) / c ] + \alpha_ {B} e x p [ j 4 \pi f _ {c} R _ {B} / c ] \tag {5} \\ \end{array}
$$

![](images/4a4a2658f122faac0bf3e33d24067a31c1915bb170c28f862d6fef613c93cde6.jpg)



(a) Basic signal model

![](images/7cb1a726ee013047a9df9b8d642d41844c36c07c123b6e435af74eb6d07b0775.jpg)



(b) Ideal multi-chirp signals

![](images/bf20746366e79efd18c1fe78fd8835b36964f83624bd66ff98d1bc93786a1736.jpg)



(c) Practical multi-chirp signals

![](images/6a618fdee992b6900911213613fda447809f7b8f0dfa617d7ec94cc9ddf9f5ba.jpg)



(d) Multi-antenna signals

Figure 5: The MSC model   
![](images/a46fb09236509e03eb4ecffd41f80ec6c03760e89796daa5b491302b5a9bb68e.jpg)



(a) Samples of different vibrations

![](images/cd6690d35e17472a7b1a8a6a1c3c11b40b79a44e69b750fcd4cc463f4beee8ef.jpg)



(b) Samples of 8 chirps

![](images/c251d735629592b185136fa92e9099234ca7b05be3036bf0644b98027c27e7b1.jpg)



(c) Translated samples of 8 chirps

![](images/54108445c65558ab98dea2abb118ea83a47b74c3bbb854cf2cbf4082ac5e9b4f.jpg)



(d) Samples from different antennas   
Figure 6: The real IQ samples under different conditions

where MSC regards all the background reflections as one composite reflection $S _ { B }$ from one single virtual reflector. $R _ { B }$ and $\alpha _ { B }$ represent the distance from the virtual reflector to the radar and the signal strength of $S _ { B } ,$ respectively.

As shown in Fig. 5(a), we use the vector form of the signals in the IQ domain to provide an intuitive representation of the signal superimposition: $\overrightarrow { S ^ { \prime } } = \overrightarrow { S } + \overrightarrow { S _ { B } } . \overrightarrow { S ^ { \prime } }$ rotates synchronously with ${ \vec { s } } _ { : }$ which explains the good accuracy of the frequency estimation in Fig. 2. However, since $\theta ^ { \prime }$ differs from the real phase variation $\theta ,$ such direction extraction suffers from errors in the amplitude estimation.

An intuitive way to extract the correct vibration reflection $\vec { s }$ from $\overrightarrow { S ^ { \prime } }$ is to fit a circle based on the signal samples. Then the static component $\overrightarrow { S _ { B } }$ can be eliminated by translating the circle center to the origin of coordinates, and the phase change is proportional to the vibration displacement [23]. However, it’s very challenging for this simple circle fitting to deal with tiny vibrations, as shown in Fig. 7. The low signal-to-noise ratio (SNR) could lead to unstable fitting results and inaccurate vibration measurements.

# 3.2 Properties of MSC

To cope with low-SNR signals, our insight is that increasing the number of observations of the same vibration helps to control measurement errors. We exploit the multi-frequency and multi-antenna properties to provide multiple observations.

3.2.1 Multi-frequency Property of MSC. Eq. 4 indicates the signal phase changes when either ???? or ?? (??) changes. The vibration signal ?? (?? ) is out of our control, but the starting frequency of a chirp ???? can be set in the mmWave radar. When we change $f _ { c }$ and keep ?? (??) the same, the phase of the reflected signal changes. In IQ domain, this results in the rotation of the reflected signal around the origin of coordinates, as shown in Fig. 5(b). Therefore, if we can enable a chirp group with different starting frequencies to simultaneously measure the same vibration, ideally the reflected signal corresponding to each chirp will rotate around the origin of coordinates and form a large arc. The rotation angle between reflected signals of two chirps can be represented by:

$$
\Delta \phi = 4 \pi \Delta f _ {c} (R _ {0} + x (t)) / c \tag {6}
$$

$\Delta f _ { c }$ is the starting frequency gap between the chirps. Therefore, we can fit a better circle using the combined signals.

However, due to the existence of the background reflection, ?? ???? leads to the rotation of the both signal components, as shown in Fig. 5(c). In order to show that, we set a group of 8 chirps with 6?????? starting frequency gap and the same bandwidth. The first chirp has 77?????? starting frequency and we measure the vibration with 50???? frequency and 100???? amplitude. The vibrating object is placed 1?? from the radar and the IQ signals are shown in Fig. 6(b). The vibration reflections (colored lines) rotate around their circle centers (grey dotted circles) and the background reflections (grey lines) also rotate around the origin of coordinates. Since the distance $R _ { B } \ \ne \ R _ { 0 } + x ( t )$ , the rotation angle of the background reflections $\Delta \phi _ { B } = 4 \pi \Delta f _ { c } ( R _ { B } ) / c$ is different from $\Delta \phi .$

Suppose we find the correct circle center of each vibration reflection, we can eliminate the background reflection by moving the circle centers to the origin of the coordinates. As shown in Fig. 6(c), we observe that the combined vibration reflection is robust against the noise by forming a large arc-shaped trajectory. However, to utilize this property, we still face two critical challenges: (i) how to create such a chirp group with a COTS FMCW radar; (ii) how to find the correct circle centers with the knowledge of this property. We address these challenges in §4.

![](images/0b4f3452d190b95fa67c6fce7e8162aa19568b1c941f03ac9f2f5e320bef9008.jpg)  
Figure 7: Signal fitting with different amplitudes

3.2.2 Multi-antenna Property of MSC. Generally, a mmWave radar has multiple antennas. The signals received from multiple Rx antennas can be utilized to pinpoint the vibrating object and refine the measurement.

Due to the half-wavelength spacing of Rx antennas, the propagation distances of the reflected signals from the vibrating object to different antennas are different from each other, as described in Fig. 5(d). Eq. 5 tells us that this will cause the rotations of the vibration reflections as well as background reflections. Fig. 6(d) shows the IQ samples from 4 Rx antennas when measuring a 100???? vibration at 1?? distance and 10◦ angle of arrival (AoA) relative to the first Rx antenna. We can see that the vibration reflections (colored lines) and the background reflections (grey lines) are different.

Note that the measured signal is along the AoA of the vibration reflection, which may differ from the vibrating direction. The measured signal is actually a projection of the real vibration to the AoA of reflection. Therefore, this multi-antenna property not only provides multiple observations but also offers an opportunity to refine the measurement. To estimate AoAs of the vibration reflections from different Rx antennas, we only consider their phase changes, i.e. the geometric rotations of the colored lines in Fig. 6(d). The background reflections also rotate when the propagation distance ???? changes, but we are not interested in their AoAs. How to identify the correct AoAs of the vibration reflections is also a critical challenge to be addressed by mmVib.

# 3.3 MSC Summary

we conclude the following properties of MSC that can improve the vibration measurement:

• The chirp group provides us the opportunity for better signal fitting by creating multiple observations on the same vibration that can consolidate the vibration extraction.   
• The starting frequency gap in the chirp group determines the rotation angle ???? between two vibration reflections from two successive chirps. ???? should be consistent in the whole chirp group, which can be utilized to further improve the signal fitting.

![](images/b07a3ff1bb05a30afc17aed65b12aa72662d1f9d0c4a6e0161e7aa3e8023b46d.jpg)



Figure 8: Overview of mmVib

• The spacing of the Rx antenna array differentiates the received signals due to the different propagation distances. The rotation of the vibration reflections of different antennas can infer their different AoAs.

In the next section, we elaborate in detail how we exploit these properties in our design of the robust and accurate measurement system.

# 4 MMVIB DESIGN

This section introduces the design of mmVib. Fig. 8 shows the workflow of mmVib, which consists of three main modules.

• Vibration Detection (VD): VD takes the raw samples of mmWave signals as inputs. By analyzing the Range-Doppler spectrum of the signals, it detects the candidate range bins of vibrating objects.   
• Robust Vibration Extraction (RVE): RVE takes the extracted signals reflected from each candidate range bin as inputs. Then it exploits MSC to combine the vibration signals from multiple chirps for accurate signal extraction.   
• Vibration Refinement (VR): VR takes into account the multiantenna signals to calculate the AoAs and refine the vibration measurement. It aggregates all the measurements to determine the vibration characteristics.

# 4.1 Vibration Detection

The Range-FFT can separate signals based on their propagation distance. Only specific range bin contains the target vibration signal and we refer it as the vibration bin. Therefore, VD module examines the Range-Doppler spectrum to search for candidate vibration bins.

In the spectrum, a higher magnitude at a certain range bin and a certain Doppler bin indicates the higher probability of the existence of a vibrating object. A candidate vibration bin should contain both positive and negative velocities due to its reciprocating motion. However, as observed in Fig. 9 where only one object is vibrating, the number of candidate bins is much larger than the number of vibrating objects.

To understand this observation, we re-examine our experiment setup (Fig. 13) and find that, besides the vibrator, the body of the calibrator as well as the table are also vibrating. The above observation is the result of the vibration transmission effect [12]: the vibration signal in a certain bin can be transmitted to adjacent bins symmetrically. According to the vibration transmission model [12], the vibration velocity decays by ??1 5 during its transmission, where ?? is the distance between the vibration bin and its adjacent bins.

![](images/20645ad727c0671fd4faa5da39b07d0e80cedc76fdc0d0bf947e2faa8fed0b86.jpg)



Figure 9: Vibration detection

We model the impact of the vibration transmission on the Range-Doppler spectrum as a convolution operation: the vibration at a certain bin transmits to its adjacent bins through a 1D convolution template. Therefore, the detection process can be modeled as a deconvolution operation, which is the inverse operation of the convolution [17].

We illustrate the vibration transmission and detection in Fig. 9. The convolution template can be obtained with the vibration transmission model: we set the coefficient of the middle bin to 1, and calculate the coefficients of the adjacent bins by multiplying an attenuation factor $1 / \epsilon ^ { 1 . 5 }$ . After the deconvolution, VD selects the top-E range bins with the largest magnitude as the candidate vibration bins. According the evaluation results in §6.4.1, we may empirically set E to the number of vibrating objects plus one to achieve a relatively high accuracy in practice.

# 4.2 Robust Vibration Extraction

The RVE module extracts the vibration signal from each detected vibration bin. To guarantee the accurate extraction under low SNR, it first generates a chirp group with different starting frequencies to provide multiple observations, and then eliminates the background reflections with a consolidated vibration extraction algorithm based on MSC.

4.2.1 Chirp Group Generation. A typical FMCW radar transmits only one chirp signal at a time. Then, how to generate a chirp group that can simultaneously measure the same vibration as we expected?

Our key insight is to rearrange the fast-time samples of the beat frequency signal ?? (?? ), defined in Eq. 3. Recall that the traditional Range-FFT operation takes all fast-time samples as inputs and generates one slow-time sample. If we separate fast-time samples into different groups and perform Range-FFT in each group, we can obtain multiple simultaneous slow-time samples for each range bin. Fig. 10 illustrates this process: we use a sliding window of size 4 on 6 fast-time samples, and obtain two fast-time sample groups with a sliding step of 2 samples. This is equivalent to generate two shorter chirps (Chirp #1, Chirp #2) with different starting frequencies from the original long chirp. The chirp group has two appealing characteristics: (i) Since slow-time samples are much longer than fast-time samples, the chirps in a group can be regarded simultaneous to each other. (ii) Different chirps starts at different frequencies, which result in diverse but consistent observations of the same vibration.

![](images/e5a70893b602764db8fd6e64a84e238ec4140bf124ed081b5cfb9a5b56cb3d75.jpg)



Figure 10: Chirp group generation

There are two key parameters to generate the chirp group. Increasing the number of chirps leads to more observations, at the cost of increased computation complexity. Increasing the shift frequency enlarges the difference among chirps, but sacrifices the bandwidth of one chirp as well as its range resolution. In practice, we may first set the number of chirps, according to the constraints in computation complexity and the required measurement latency. In our implementation, the number of chirps is 8. Then, shift frequency is set by considering the complexity of the measurement environment. For example, in our laboratory experiments where there is only one vibrating object, the shift frequency is set at 200??????. In the field experiments where multiple vibrating objects co-exist, we set a relatively small shift frequency of 13?????? to preserve a high range resolution to differentiate reflections from different vibrating objects.

4.2.2 Consolidated Vibration Extraction. To extract the vibration signal, the primary task is to estimate the background reflections. With the multiple IQ signals provided by the generated chirp group, we can improve the vibration extraction process under low SNR.

The multi-frequency property of MSC tells us that, due to their inherent consistency, those signals form a large arc around the origin of coordinates when the background reflections are eliminated. Hence, the consolidated vibration extraction algorithm runs in the following steps: (i) It first estimates the background reflection of each chirp signal through basic circle fitting step; (ii) Then consolidated circle fitting step generates a fitting constraint for each chirp signal that in turn improves the first step; (iii) The first two steps iteratively run until a perfect large arc is obtained. Finally we extract and aggregate the vibration signals through the vibration signal extraction step. Below are the details of the algorithm.

Step 1 - Basic Circle Fitting: Let $X = \{ x _ { l , n } \} _ { L \times N } , x _ { l , n } \in \mathcal { R } ^ { 2 }$ denote the IQ samples from ?? chirps with ?? samples per chirp. For the ??-th chirp, the fitting is turned into an optimization problem to obtain a circle with radius $r _ { l }$ and center $z _ { l }$ that minimizes the summed geometric distance from every sample to the circle:

$$
z _ {l} ^ {*}, r _ {l} ^ {*} = \underset {\boldsymbol {z} _ {l}, r _ {l}} {\arg \min} \quad \sum_ {n = 1} ^ {N} \left(\left\| \boldsymbol {x} _ {l, n} - z _ {l} \right\| - r _ {l}\right) ^ {2}, l \in [ 1, L ] \tag {7}
$$

![](images/b5e41b4b58bd83976b2fa8e58249342688c3215a9c67e715771ded5e3703ea9e.jpg)



Figure 11: Consolidated circle fitting

It is a nonlinear least squares optimization problem and can be solved with the Levenberg-Marquardt (LM) algorithm [10]. When the SNR is low, however, the basic circle fitting is error-prone without a proper constraint on the radius.

Step 2 - Consolidated Circle Fitting: The first step gives a basic but not always accurate estimation of the background reflection of each chirp signal. Therefore, combining multiple translated chirps signals after the background elimination probably won’t form a perfect large arc as expected. Suppose the large arc falls on an intrinsic circle, Fig. 11 shows the two cases that each chirp signal might not necessarily fall on it: (i) translation-needed case: an improperly fitted radius will make the $\mathrm { I Q }$ samples of a chirp fall inside (blue samples) or outside the circle; (ii) scaling-needed case: a stronger or weaker signal strength of a chirp will make its IQ samples fall on other concentric circles of the intrinsic circle (yellow samples). Therefore, by properly translating and scaling the IQ samples of each chirp, we can finally get a perfect large arc. The following is consolidated circle fitting process:

• First, we eliminate the background reflection of each chirp signal. For the IQ samples of the ??-th chirp {????,?? }????=1, $\{ x _ { l , n } \} _ { n = 1 } ^ { N }$ the elimination is $\{ \pmb { x } _ { l , n } ^ { \prime } \} _ { n = 1 } ^ { \hat { N } } = \{ \pmb { x } _ { l , n } - \pmb { z } _ { l } ^ { * } \} _ { n = 1 } ^ { N }$ nter coordinate ???? of the chirp signal:.   
• Second, for each chirp signal, we derive its translation direction Δ?? as the unit vector of the to the average sample point $\textstyle { \frac { 1 } { N } } \sum _ { n = 1 } ^ { N } x _ { l , n } ^ { \prime }$ he origin of coordinates.   
• Third, we simultaneously solve the radius of the intrinsic circle ?? as well as the translation factors $\pmb { \sigma } = \{ \sigma _ { l } \} _ { l = 1 } ^ { L }$ and the scaling factors $\gamma = \{ \gamma \} _ { l = 1 } ^ { L }$ 1 by minimizing the average geometric distance of every sample to the intrinsic circle:

$$
\tau^ {*}, \boldsymbol {\sigma} ^ {*}, \boldsymbol {\gamma} ^ {*} = \underset {\tau , \sigma , \boldsymbol {\gamma}} {\arg \min} \frac {1}{L N} \sum_ {l = 1} ^ {L} \sum_ {n = 1} ^ {N} \left(\left\| \gamma_ {l} \boldsymbol {x} _ {l, n} ^ {\prime} + \sigma_ {l} \Delta \boldsymbol {x} _ {l} \right\| - \tau\right) ^ {2} \tag {8}
$$

We also add a penalty term $\textstyle \Gamma \cdot ( \sum _ { l = 1 } ^ { L } \gamma _ { l } - L ) ^ { 2 }$ to the above loss estimated $\tau ^ { * } , \sigma _ { l } ^ { * }$ and $\gamma _ { l } ^ { * }$ for ??-th chirp, its radius can be constrained around its expected radius $\tau ^ { * } / \gamma _ { l } ^ { * } + \sigma _ { l } ^ { * } \varDelta x _ { l }$ in the next iteration.

The iteration stops after the relative change in ?? is less than a small threshold (e.g. 1%). Denote the time cost of the fitting process

![](images/0c79f9733390e4769f7ff9630197d4974c7abb074b6ce186ca544ab1e99ae7a1.jpg)



Figure 12: AoA estimation and signal projection

for each chirp signal by $I _ { 1 }$ and that of the fitting process for the intrinsic circle by $I _ { 2 } ,$ the time cost of ?? iteration is $\left( L I _ { 1 } + I _ { 2 } \right) \cdot T$ According to our experience, ?? is usually less than 3. So, the total processing time is mainly determined by the number of chirps ??.

Step 3 - Vibration Signal Extraction For ??-th chirp, with the final translated sequence $\{ x _ { l , n } - z _ { l } ^ { * } \} _ { n = 1 } ^ { N }$ whose phase sequence is {????,?? } ??=1 $\{ \phi _ { l , n } \} _ { n = 1 } ^ { N }$ , we obtain one observation of the vibration signal $\{ X _ { l , n } \} _ { n = 1 } ^ { N } \colon$

$$
X _ {l, n} = \frac {c}{4 \pi f _ {c l}} \text { unwrap } (\phi_ {l, n}) - R _ {0}, n \in [ 1, N ] \tag {9}
$$

where $f _ { c _ { l } }$ is the starting frequency of ??-th chirp. By aggregating all the observations from the chirp group, we can obtain the final measurement. We utilize the inter-quartile mean (IQM) algorithm [34] for the signal aggregation, which calculates the truncated mean of the data within its inter-quartile range: $X _ { n } = \mathrm { I Q M } ( \{ X _ { l , n } \} )$ , ?? ∈ [1, ?? ].

# 4.3 Vibration Refinement

In this module, we estimate the AoA of each Rx antenna and refine the vibration measurement, so as to obtain the correct measurement along its actual vibrating direction.

4.3.1 AoA Estimation. The conventional AoA estimation method, which exploits the phase differences among Rxs, might not work here due to the unawareness of background reflections. Our idea is to directly estimate the AoAs of vibration reflections with their rotation angles in the IQ domain. Note that the rotation angles of IQ samples from different Rx antennas reveal their phase differences, which are induced by their different propagation distances. Suppose we derive the difference between the propagation distance of the ??- th antenna compared to that of the first Rx antenna as $\varDelta R _ { m } = R _ { m } -$ $R _ { 1 } , m \in [ 2 , M ]$ , the basic model for AoA estimation is illustrated in Fig. 12: (i) we assume the non-parallelism of the arriving waves that describe different AoAs at different Rx antennas; (ii) suppose $\pmb { p } _ { m } =$ $\begin{array} { r } { \left( - \frac { \lambda } { 2 } ( m - 1 ) , 0 \right) ^ { \top } } \end{array}$ is the location of ??-th Rx and $\pmb { \ o } = ( o _ { 1 } , o _ { 2 } ) ^ { \top }$ is the location of the vibrating object, we can compute $R _ { m } \ a s \ \| \pmb { o } - \pmb { p } _ { m } \|$ . With $\Delta R _ { m } = R _ { m } - R _ { 1 }$ and $R _ { 1 } = \left\| \pmb { o } \right\|$ , we formalize the following optimization problem to solve $\bullet ^ { * }$ :

$$
\boldsymbol {o} ^ {*} = \underset {\boldsymbol {o}} {\arg \min} \quad \sum_ {m = 2} ^ {M} \left(\| \boldsymbol {o} - \boldsymbol {p} _ {m} \| - \| \boldsymbol {o} \| - \Delta R _ {m}\right) ^ {2} \tag {10}
$$

![](images/90acf9cff8cb6bcd8c9eaf9eb3314f405751d2d54307e1558c9661ec9e7f5f94.jpg)



(a) Measurement Distance = 100cm   
(b) Measurement Distance = 700cm   
Figure 13: Experiment setup of mmVib

Then, the AoAs of ?? Rx antennas $\{ \beta _ { m } \} _ { m = 1 } ^ { M }$ can be calculated according to their geometric relationship with $\bullet ^ { * }$ .

4.3.2 Direction-aware Vibration Refinement. Since mmWave radar can only sense the displacement along the LOS direction towards the vibrating objects, the measurement from the RVE module is just a projection of the vibration signal to this direction. mmVib exploits the multi-antenna property to recover the vibration signal along its real vibrating direction.

Suppose the angle between the real vibrating direction and the norm direction of the antenna array is $\beta$ and the AoA of ??-th antenna is $\beta _ { m } .$ , the measurement from ??-th antenna is a projection of the vibration signal with an angle $\beta - \beta _ { m }$ . Denote the measured vibration amplitudes by $\{ \boldsymbol { X _ { m } } \} _ { m = 1 } ^ { M }$ and the correct vibration amplitude by X. We can estimate ?? and X together with the following optimization problem:

$$
\mathcal {X} ^ {*}, \beta^ {*} = \underset {\mathcal {X}, \beta} {\arg \min} \quad \sum_ {m = 1} ^ {M} \| \mathcal {X} \cos (\beta - \beta_ {m}) - \mathcal {X} _ {m} \| ^ {2} \tag {11}
$$

A larger antenna array with more antennas can lead to a better estimation of the final vibration. It is also feasible to obtain more vibration measurements from different AoAs by combining the results of multiple synchronized radars.

# 5 DISCUSSION

# 5.1 Multi-object Measurement

It’s easy for mmVib to handle the multi-object measurement if these vibrating objects fall into different range bins: their reflection signals can be separated through the Range-FFT. In §6.5, our case study shows that we can configure the deployment position of the radar so that multiple vibrating objects are located in different range bins. However, it is possible that we can’t achieve this ideal deployment condition and several vibrating objects might fall into the same range bin. In such cases, spatial spectrum analyses, e.g. receiver beamforming technologies [28] or blind signal separation algorithms [2] can be adopted to separate these reflections.

![](images/30ef47acc6cf0f3921f8e3c39c8e1a29a4869577ccff1920384df92280932fc7.jpg)



(a) CDF of amplitude estimation

![](images/dbfe0579ac80be15fdb027bf3af4f6c2e4aec29994e549c5c506cf3a4b7cf0f3.jpg)



(b) CDF of frequency estimation   
Figure 14: Overall Performance

# 5.2 NLOS Measurement

mmWave signals have limited penetration capability. The evaluation in §6.3.3 shows that the performance of mmVib doesn’t degrade under thin and non-metallic blockages since mmWave signal can penetrate them. Therefore, we may enclose the mmWave board and its on-board antenna to improve the devices’ durability. However, in the practical deployment of mmVib, we should avoid thick or metal blockages, e.g. walls and pillars.

# 5.3 Phase Noise

The phase noise in the vibration signal actually has two sources: multiplicative noise and additive noise [26]. The multiplicative noise is induced by the device circuits such as the oscillator and the mixer. The additive noise is introduced by the wireless channel, which is typically treated as the Additive White Gaussian Noise (AWGN) [30]. The consolidated observations provided by the chirp group in mmVib cope with the additive noise, which is particularly effective in the scenarios where the SNR is low. However, the multiple observations can’t eliminate the inherent multiplicative noise. For even higher accuracy of vibration measurement, one may resort to device calibration prior to deployment.

# 6 EVALUATION

In this section, we implement mmVib and evaluate it in both the lab environment and a real steel plant.

![](images/768792663635491082cd8fbc9c36113bda207d5b7b8bc69efc5ff2a3575122e9.jpg)



![](images/de44b138d2af4dafbfa06e6950f9105a0e299a53419a2e1ebdc06c652109eab4.jpg)



![](images/1d720cbe21696300d1fbcfeff558cc6d04d67aed817a01925e624f5eba00d3c9.jpg)



![](images/d74fe77e3072fa0ae4da3239d553971f64a5b06d5cacb688cfbf9ee74733c299.jpg)



![](images/5a96c341fc6d618db3977b4a1b135d674acdb9e316dd7fd5d46e4e2988bb546e.jpg)



![](images/602d6747dfed1e6e590fc186349a2d7567141f287fbf5183c803b8296fe576c4.jpg)



![](images/2e9e304ec9d5374f2f24d2d87e323107aab072d60297f0ff1ff83566a498713d.jpg)



![](images/fd32659183493221af2a98e31ac78c5935dc8c76cfabe096288e1d5528af1b16.jpg)



(a) Impact of vibration amplitudes on amplitude errors   
(b) Impact of vibration frequencies on amplitude errors   
(c) Impact of measurement distances on amplitude errors   
(d) frequency errors   
Figure 15: Accuracy of amplitude and frequency estimation in the lab environment

# 6.1 Implementation and Methodology

Implementation: We implement mmVib on a commercial mmWave radar board, Texas Instruments (TI) IWR1642 BoosterPack [14]. IWR1642 chip works on the 77?????? millimeter-wave frequency band (77 ∼ 81??????). It integrates 6 on-board antennas (2 Tx antennas and 4 Rx antennas). We let Tx1 send the FMCW signal with 2.5?????? bandwidth, and Rx1∼Rx4 receive the reflected signal. The raw sampling rate (fast-time samples) is around 6?????? and the chirp sampling rate (slow-time samples) is 10??????. The raw fasttime samples are captured through a TI DCA1000EVM [15] data acquisition board in the high-speed and real-time manner. The data processing coded in Python runs on a computer with an Intel i7- 8550U processor and 16???? memory. The mmWave board costs \$299 while its core chip only costs \$40.

Ground Truth: The experiments are conducted in both our lab and a steel plant. In the lab, we use a vibration calibrator to generate tunable vibrations with 20???? to 500???? (±1%) frequency and 5???? to 500???? (±1%) amplitude. These parameters describe typical vibrations of industrial objects. The ground truth of those measurements in the steel plant is provided by a piezoelectric vibration sensor.

Experiment setting: Fig. 13 shows the experiment setup in a hallway of 2.4?? × 10??. The vibration calibrator is placed on a table while the mmWave radar is placed on a tripod. We evaluate mmVib in terms of vibration amplitude and frequency, measurement distance and angle, etc. For each setting, we collect at least 40 traces of raw mmWave data1.

Comparisons: We compare mmVib with two mmWave-based vibration measurement approaches introduced before: the theoretical phase-based method proposed in [7] (denoted by Radar) and the basic fitting-based method proposed in [23] (denoted by CircFit). To ensure fairness, the three approaches use the same data and pre-processing methods.

Metrics: In the experiments, we evaluate the performance in terms of the errors in amplitude and frequency estimation: the latter one indicates the correctness of the measured vibration signals while the former one stands for the accuracy.

# 6.2 Evaluation on Vibration Measurement

In this experiment, we evaluate the performance by changing the amplitude (from 10???? to 200????), frequency (from 20???? to 500????) and distance (from 50???? to 700????). The calibrator is placed directly in front of the radar with a vibrating direction along the radar’s norm direction. In these cases, smaller amplitude and farther distance mean lower SNR.

6.2.1 Overall performance: Fig. 14 shows the overall performance of all the settings: mmVib achieves 8.2% relative amplitude error and 0.5% relative frequency error in median. Typically, mmVib achieves a median amplitude error of 3.4???? for the 100????-amplitude vibration. The comparisons indicate that mmVib outperforms state-ofthe-art approaches by (i) significantly reducing the error of amplitude estimation; (ii) improving the stability of frequency estimation. For all settings, mmVib reduces the 80??ℎ-percentile amplitude error by 62.9% and 68.9%, compared to CircFit and Radar respectively.

Next, we examine the impact of different factors on the estimation accuracy and stability: in Fig. 15, the first row presents the lower-SNR cases while the second row presents the higher-SNR cases. Note that the Y-axis uses the logarithmic scale.

6.2.2 Amplitude accuracy under different amplitudes. In this experiment, we keep the frequency to 50???? and change the amplitudes from 10???? to 200???? at two distances 300???? and 600???? respectively. From the results in Fig. 15(a), we can see that: (i) mmVib can accurately measure the tiny vibrations at a relative far distance: for a typical 300????-30???? case, it achieves an average amplitude error of 2.7????. (ii) For two fitting-based approaches, their performances are basically in proportional to the SNR. (iii) Since CircFit can be easily affected by noises, the improvement of mmVib is more significant when the SNR is lower, i.e. the lower amplitude or the farther distance. (iv) For extremely low-SNR cases, e.g. the 600????-10???? case, mmVib seems to have great improvement in the amplitude estimation. In fact, in these cases mmVib actually doesn’t extract the correct vibration signals, which will be explained in §6.2.5.

![](images/53786601fcbbb9d85c9bfa2c400509bb7934fe257c43950ed5288c0a55ae97cd.jpg)



(a) Reflectors in the same bin

![](images/6c8c349f79ad52f763de50132424e9e21e535b26c74eb7b56e81fab113c747d7.jpg)



(b) Reflectors in the other bins

![](images/db8846b847e615edf212695912cfdeb003352a7eea8496e160207b39791e5334.jpg)



(c) Impact of measurement angle

![](images/c3249a8944b7a315085c6e0b1870ce77257f9a8ce8b29766333067372ba46dd1.jpg)



(d) Impact of LOS blockages   
Figure 16: Impact of practical factors

6.2.3 Amplitude accuracy under different frequencies. In this experiment, we keep the distance to 100???? and change the frequencies from 20???? to 500???? at two amplitudes 10???? and 100???? respectively. Due to power limitations, our calibrator cannot generate vibration signals of a large amplitude at a high frequency or a small amplitude at a low frequency. We can see from Fig. 15(b) that: (i) For 10???? cases, mmVib achieves a low amplitude error at a large frequency range, i.e. 2.1um in average, which significantly outperforms other approaches. (ii) For higher-SNR cases in lower Fig. 15(b), mmVib also outperforms the other two approaches, but the performance gap is relatively small.

6.2.4 Amplitude accuracy under different distances. In this experiment, we keep the frequency to 50???? and respectively measure 30???? and 100???? vibrations at a distance from 50???? to 700????. We can see from Fig. 15(c) that: (i) mmVib can work with a relatively long measurement distance: the average error is 4.7???? for the 500????-30???? case while 6.9???? for the 700????-100???? case. (ii) mmVib outperforms the other two approaches at all the distances.

6.2.5 Frequency accuracy under different conditions. We evaluate the performance of frequency estimation under different vibration amplitudes and measurement distances with the same data in §6.2.2 and §6.2.4. The results in 15(d) show that mmVib achieves the absolute frequency error less than 0.3????. It is also worth noticing that when the distance is 600???? and the amplitudes is not larger than 20????, mmVib has a relatively large frequency estimation error, which means mmVib doesn’t extract the correct vibration signals in those cases. That implies the limitation of mmVib in handling vibration signals with extremely low SNR.

# 6.3 Impact of practical factors

We evaluate the impact of several practical factors that are related to the applicability of mmVib in practice.

6.3.1 Multipath conditions. The multipath condition can significantly affect the mmWave signal. The experiment is conducted in our office where tables, chairs and computers act as multipath

reflectors. Besides, we place extra metal plates at different locations to make the multipath signals fall into the same bin of vibration reflections or the other bins. Denote the cases with 0, 2 or 6 metal plates by clean, light and heavy. The amplitude, frequency and distance are fixed to 100????, 50???? and 100????. The results in Fig. 16(a-b) show that (i) mmVib outperforms other approaches for all the cases; (ii) in the case that strong multipath signal interferes with the vibration reflection, mmVib’s performance degrades. In practice, we can improve the spatial resolution by reducing the frequency shift in the chirp group.

6.3.2 Measurement angles. We evaluate the impact of measurement angles. The measurement angle is defined as the AoA of the first RX antenna. In this experiment, we keep the vibrating direction along the norm direction of the antenna array, and translate the calibrator to control the measurement angles from 0◦ to 40◦, as shown in Fig. 13(a). The amplitude and frequency are set to 100???? and 50????. Fig. 16(c) shows the amplitude errors of mmVib with and without the VR module under different angles. We can see that: (i) The amplitude error increases with the angle, since the measurement distance increases and leads to lower SNR. (ii) For different angles, mmVib achieves the average amplitude error less than 13.7????. (iii) Our VR module brings performance gain, especially when the angle is relatively large.

6.3.3 LOS-path blockages. We evaluate the ability of mmVib to deal with LOS-path blockages. We place various objects with different materials but similar thickness (∼ 1.5????) in front of the mmWave radar (∼ 20????), and evaluate the amplitude errors. Fig. 16(d) shows the results that (i) the metal materials, e.g. laptops and phones, will block the mmWave signal and make the measurement results inapplicable; (ii) the radiation-absorbent material, e.g. the foam, will distort the mmWave signal and greatly degrade the system performance; (iii) due to the penetration property of mmWave, other materials won’t obviously degrade the system performance and only introduce 10???? ∼ 20???? errors in most cases. Based on this result, we may enclose the mmWave board and its on-board antenna to improve the devices’ durability.

# 6.4 System Micro-benchmarks

6.4.1 Vibration detection. This experiment is conducted to illustrate how to select the parameter E in the VD module. We place 4 speakers as vibrating objects in 4 adjacent range bins with the measurement distances of 89????, 95????, 101???? and 108???? respectively. We randomly select different numbers of speakers to play the same single-tone sound and evaluate how many range bins we should inspect, i.e E, to correctly find N vibration bins. From Fig. 17(a), we observe that the VD module can efficiently and accurately localize the vibration bins by setting E to $N + 1$ .

![](images/f13f8386ce04e6125655f6c2ab71ea9f2ad7abb76d8facfe5f21d290926884db.jpg)



(a) Vibration detection

![](images/e6e1cde08c7c00170e8dec0b3390cbc890c2eeeaf306a61b0f7b089258c27d36.jpg)



(b) AoA estimation   
Figure 17: System micro-benchmarks

6.4.2 AoA Estimation. We evaluate the AoA estimation with the same setup and data in §6.3.2. Fig. 17(b) plots the CDFs of AoA estimation errors of Rx1 corresponding to different deployment angles. We observe that: (i) mmVib achieves a relatively low $8 0 ^ { t h } .$ - percentile AoA estimation error of about $1 . 4 ^ { \circ }$ . Since the size of the metal vibrator is relatively small, the results prove that our AoA estimation algorithm is effective by only considering the vibration reflections. (ii) Because the radar’s field of view (FoV) is about ±40◦, the SNR degrades significantly in the $4 0 ^ { \circ }$ cases.

6.4.3 Processing Efficiency. We evaluate the processing efficiency of mmVib. We mainly consider 3 major components of mmVib: pre-processing (chirp group generation and Range-FFT), vibration signal extraction, and post-processing (refinement and aggregation). The median processing time of these components is 103.4????, 428.1???? and 2.5???? for each mmWave data frame. This is an acceptable time cost and we believe it can be further improved by processing all the chirps in parallel.

# 6.5 Field Study

We conduct a field study to deploy and evaluate mmVib in a steel plant, the real-world industrial environment. Fig. 18 and 19 shows the deployment, where the vibrating objects are the bearings of a transmission system containing the descaling pump, speed reducer and main motor. The system works in two modes: low-speed operation and high-speed operation, with different rotating frequencies. The amplitudes of the vibrations are ????-level. The plant installs the piezoelectric vibration sensors on different parts of the target devices and the sensor readings are sent back to the console of the monitoring room via wires. We use those readings as the ground truth.

Non-contact measurement: mmVib outperforms conventional approaches due to its non-contact measurement mechanism without any disturbance on the running machines or extra deployment overhead. Thus, what we are most curious about is whether it works in practice and how far the measurement distance can be. Fig. 20

![](images/048974ed26677c0667dfcbbf19c65dc9a00a712739fd046d9cd3404a61612a25.jpg)



Figure 18: Field study: non-contact measurement

![](images/17ac96842ae51ceaa151505d3f99d3dc87740d5a0826e721fc2f0f909eb22895.jpg)



Figure 19: Field study: multi-object measurement

shows the estimation stability (median and quartiles) and accuracy of the vibration amplitude and frequency of a descaling pump in two operation modes. Taking the high-speed mode for example, when the distance varies from 100???? to 500????, the average amplitude errors are 3.6????, 6.7????, 5.3????, 17.4???? respectively while the average frequency errors are less than 0.4????. This indicates that mmVib is able to sense the ????-level vibration in practice and its measurement is accurate and consistent when the distance ≤ 3??.

Multi-object measurement: The second appealing characteristic of mmVib is its capability of measuring multiple vibrating objects simultaneously. In this experiment, we place the radar in front of the speed reducer and main motor, and ensure that the bearings of these two machines fall into different range bins. Fig. 21 shows that: (i) mmVib captures the fact that, although the amplitudes of the speed reducer and main motor differ from each other, their frequencies are nearly identical due to their direct connection (ii) The relatively small inter-quartile ranges and acceptable estimation errors demonstrate the stability and accuracy of mmVib for multi-object measurement.

# 7 RELATED WORKS

In this section, we review the related literature of mmVib.

Vibration measurement approaches. Conventional approaches for vibration measurement are based on specialized sensors or optical devices. Piezoelectric accelerometer is designed for vibration measurement based on the piezoelectric effect [5, 9, 20]. It requires to be installed on the surface of the vibration source, which could introduce non-trivial deployment and maintenance cost. Laser vibrometer is also a promising solution for high-accuracy vibration measurement [3, 6, 27]. However, its has the high device cost and strict requirement for the LOS path. A recent work Vibrosight proposes to employ a low-cost laser sensor as a long-range vibrometer [38]. It mainly focuses on leveraging vibration spectrums for object recognition rather than restoring vibration signals.

![](images/5e8f64f8208c9d0e81a71199332e24b6dcfd21c65c8af1d613c312fc94ce6f14.jpg)



(a) Amplitude Estimation

![](images/b4c438f627b14adbdfd662b1e9868e8f4d24aba7d106bdc1c52dd759e41aec4d.jpg)



(b) Frequency Estimation   
Figure 20: Non-contact measurement results

![](images/416f6da8193b7889646ae55e8839af2723cff83e7cb5a9fd8495172629b84cc3.jpg)



(a) Amplitude Estimation

![](images/9ee4857bc31279d2184af43e4f0d0eef5a684d8cfcf89e049b7d33d0e603989f.jpg)



(b) Frequency Estimation   
Figure 21: Multi-object measurement results

RF-based vibration measurement. RF-based approaches are promising in measuring a target’s displacement by measuring the change of the RF signals in a non-intrusive manner [4, 18, 32, 36, 39]. ART exploits the 2.4?????? signals and models the relationship between signal features and vibration parameters [32]. However, the mm-level accuracy can’t satisfy the micrometer-level requirement in industry. Tagbeat and TagSound exploit the 915?????? UHF RFID for vibration measurement [18, 36]. Similarly, they face the same limitation on the vibration amplitude. It is still impossible to estimate micrometer-level vibrations.

mmWave-based sensing. Compared with common wireless signals such as RFID, WiFi and acoustic signals, mmWave is highly sensitive to tiny displacements due to the mm-level wavelength. Lots of works exploit mmWave for high-precision tracking [33], hand gesture and human activity recognition [16, 19], object imaging and recognition [25, 41, 42], localization and map construction [11, 22, 24, 40], vital signal monitoring [7, 23, 37], noise-resistant speech sensing [35] and water-to-air wireless communication [29].

mmWave-based vibration measurement. mmWave is therefore a promising solution for micrometer-level vibration measurement [7, 23, 29, 37]. Ding et al. have proposed a theoretical signal model which translates the signal characteristics of FMCW to the vibration parameters [7]. However, without considering the multipath effect, the model fails to extract the correct tiny vibration amplitude. Mikhelson et al. overcome the above problem by analyzing the mmWave signal in IQ domain and introduce circle fitting method [23]. However, this work can’t deal with the tiny vibration because of the ambiguity in the small arc fitting.

Compared with the existing mmWave-based approaches, mmVib particularly addresses the challenges in multipath-rich and noisy environment for highly accurate vibration measurement. Built upon the COTS mmWave radar, mmVib exploits the multi-frequency and multi-antenna properties of the reflected signals and shows superior performance, especially in low-SNR environments.

# 8 CONCLUSION AND FUTURE WORK

In this paper, we present mmVib for micrometer-level vibration measurement. A multi-signal consolidation model is propose to guide the robust and accurate extraction of tiny vibrations under low SNR conditions. We evaluate mmVib in the laboratory as well as field environment. mmVib achieves 8.2% relative amplitude error and 0.5% relative frequency error in median. Typically, the median amplitude error is 3.4???? for the 100????-amplitude vibration.

As of the time of publication of this paper, the real-world deployment and application of mmVib are on the way. The feature of non-invasive measurement and the consistently high measurement accuracy of mmVib have attracted the attention from industry. In the future, we will collaborate with industrial partners to deploy tens of measurement devices in the plants and further extend the research on mmVib in the following aspects:

Solving the practical issues: We plan to make mmVib a more practical solution to support the continuous and multi-object vibration measurement. How to deal with the dynamic interference from surrounding objects and walking people is also an important issue to study.

Extending the sensing capabilities: Through the discussion with industrial partners, we find that some machines have more complex vibration characteristics. For instances, different parts of a machine may vibrate differently. The vibration of a machine may form a 2D trajectory rather than 1D movement. We will address these problems in the future.

# ACKNOWLEDGMENTS

We are grateful to the anonymous reviewers for their valuable and constructive comments. The field study conducted during this work was supported by Nanjing Nangang Iron & Steel United Co., Ltd and Jiangsu Jinheng Information Technology Co., Ltd.

This work was jointly supported by National Key R&D Program of China No. 2017YFB1003000, National Natural Science Foundation of China No. 61772306 and No. 61902213. Chengkun Jiang and Junchen Guo are co-primary authors of this paper.

# REFERENCES

[1] E. Peter Carden and Paul Fanning. 2004. Vibration based condition monitoring: a review. Structural health monitoring 3, 4 (2004), 355–377.   
[2] J. F. Cardoso. 1998. Blind signal separation: statistical principles. Proc. IEEE 86, 10 (1998), 2009–2025.   
[3] P. Castellini, M. Martarelli, and EP. Tomasini. 2006. Laser Doppler Vibrometry: Development of advanced solutions answering to technology’s needs. Mechanical systems and signal processing 20, 6 (2006), 1265–1285.   
[4] Bo Chen, Vivek Yenamandra, and Kannan Srinivasan. 2015. Tracking keystrokes using wireless signals. In Proceedings of ACM MobiSys. 31–44.   
[5] Wenqiang Chen, Maoning Guan, Yandao Huang, Lu Wang, Rukhsana Ruby, Wen Hu, and Kaishun Wu. 2018. ViType: A Cost Efficient On-Body Typing System through Vibration. In Proceedings of IEEE SECON. 1–9.   
[6] Keyence Corporation. 2020. Keyence’s Laser Displacement Sensors. https:// www.keyence.com/products/measure/laser-1d/.   
[7] Lei Ding, Murtaza Ali, Sujeet Patole, and Anand Dabak. 2016. Vibration parameter estimation using FMCW radar. In Proceedings of IEEE ICASSP. 2224–2228.   
[8] Scott W. Doebling, Charles R. Farrar, Michael B. Prime, and Daniel W. Shevitz. 1996. Damage identification and health monitoring of structural and mechanical systems from changes in their vibration characteristics: a literature review. Technical Report. Los Alamos National Lab., NM (United States).   
[9] Banner Engineering. 2020. NI’s Vibration Sensor White Paper. http://www.ni.com/en-us/innovations/white-papers/06/measuring-vibrationwith-accelerometers.html.   
[10] Walter Gander, Gene H. Golub, and Rolf Strebel. 1994. Least-squares fitting of circles and ellipses. BIT Numerical Mathematics 34, 4 (1994), 558–578.   
[11] Francesco Guidi, Anna Guerra, and Davide Dardari. 2015. Personal mobile radars with millimeter-wave massive arrays for indoor mapping. IEEE Transactions on Mobile Computing 15, 6 (2015), 1471–1484.   
[12] Carl E. Hanson, David A. Towers, and Lance D. Meister. 2006. Transit noise and vibration impact assessment. Technical Report.   
[13] Yuan He, Junchen Guo, and Xiaolong Zheng. 2018. From surveillance to digital twin: Challenges and recent advances of signal processing for industrial internet of things. IEEE Signal Processing Magazine 35, 5 (2018), 120–129.   
[14] Texas Instruments Incorporated. 2020. IWR1642: Single-chip 76-GHz to 81- GHz mmWave sensor integrating DSP and MCU. http://www.ti.com/product/ IWR1642.   
[15] Texas Instruments Incorporated. 2020. Real-time data-capture adapter for radar sensing evaluation module. http://www.ti.com/tool/DCA1000EVM.   
[16] Wenjun Jiang, Chenglin Miao, Fenglong Ma, Shuochao Yao, Yaqing Wang, Ye Yuan, Hongfei Xue, Chen Song, Xin Ma, Dimitrios Koutsonikolas, et al. 2018. Towards Environment Independent Device Free Human Activity Recognition. In Proceedings of ACM MobiCom. 289–304.   
[17] M. K. Khan, S. Morigi, L. Reichel, and F. Sgallari. 2013. Iterative methods of Richardson-Lucy-type for image deblurring. Numerical Mathematics: Theory, Methods and Applications 6, 1 (2013), 262–275.   
[18] Ping Li, Zhenlin An, Lei Yang, and Panlong Yang. 2019. Towards Physical-Layer Vibration Sensing with RFIDs. In Proceedings of IEEE INFOCOM. 892–900.   
[19] Jaime Lien, Nicholas Gillian, M. Emre Karagozler, Patrick Amihood, Carsten Schwesig, Erik Olson, Hakim Raja, and Ivan Poupyrev. 2016. Soli: Ubiquitous gesture sensing with millimeter wave radar. ACM Transactions on Graphics 35, 4 (2016), 142.   
[20] Jian Liu, Chen Wang, Yingying Chen, and Nitesh Saxena. 2017. VibWrite: Towards finger-input authentication on ubiquitous surfaces via physical vibration. In Proceedings of ACM CCS. 73–87.   
[21] Jian Liu, Yan Wang, Gorkem Kar, Yingying Chen, Jie Yang, and Marco Gruteser. 2015. Snooping keystrokes with mm-level audio ranging on a single phone. In

Proceedings of ACM MobiCom. 142–154.   
[22] Chris Xiaoxuan Lu, Stefano Rosa, Peijun Zhao, Bing Wang, Changhao Chen, Niki Trigoni, and Andrew Markham. 2020. See Through Smoke: Robust Indoor Mapping with Low-cost mmWave Radar. In Proceedings of ACM MobiSys.   
[23] Ilya V. Mikhelson, Sasan Bakhtiari, Thomas W. Elmer, Alan V. Sahakian, et al. 2011. Remote sensing of heart rate and patterns of respiration on a stationary subject using 94-GHz millimeter-wave interferometry. IEEE Transactions on Biomedical Engineering 58, 6 (2011), 1671–1677.   
[24] Ioannis Pefkianakis and Kyu-Han Kim. 2018. Accurate 3D localization for 60 GHz networks. In Proceedings of ACM SenSys. 120–131.   
[25] Akarsh Prabhakara, Vaibhav Singh, Swarun Kumar, and Anthony Rowe. 2020. Osprey: a mmWave approach to tire wear sensing. In Proceedings of ACM MobiSys. 28–41.   
[26] K. V. Puglia. 2002. Phase noise analysis of component cascades. IEEE Microwave Magazine 3, 4 (2002), 71–75.   
[27] Lorenzo Scalise, Yanguang Yu, Guido Giuliani, Guy Plantier, and Thierry Bosch. 2004. Self-mixing laser diode velocimetry: application to vibration and velocity measurement. IEEE Transactions on Instrumentation and Measurement 53, 1 (2004), 223–232.   
[28] Petre Stoica, Randolph L. Moses, et al. 2005. Spectral analysis of signals. (2005).   
[29] Francesco Tonolini and Fadel Adib. 2018. Networking across boundaries: enabling wireless communication through the water-air interface. In Proceedings of ACM SIGCOMM. 117–131.   
[30] David Tse and Pramod Viswanath. 2005. Fundamentals of wireless communication. Cambridge university press.   
[31] Junjue Wang, Kaichen Zhao, Xinyu Zhang, and Chunyi Peng. 2014. Ubiquitous keyboard for small mobile devices: harnessing multipath fading for fine-grained keystroke localization. In Proceedings of ACM MobiSys. 14–27.   
[32] Teng Wei, Shu Wang, Anfu Zhou, and Xinyu Zhang. 2015. Acoustic eavesdropping through wireless vibrometry. In Proceedings of ACM MobiCom. 130–141.   
[33] Teng Wei and Xinyu Zhang. 2015. mTrack: High-precision passive tracking using millimeter wave radios. In Proceedings of ACM MobiCom. 117–129.   
[34] Wikipedia. 2020. Interquartile Mean. https://en.wikipedia.org/wiki/ Interquartile\_mean.   
[35] Chenhan Xu, Zhengxiong Li, Hanbin Zhang, Aditya Singh Rathore, Huining Li, Chen Song, Kun Wang, and Wenyao Xu. 2019. WaveEar: Exploring a mmWavebased Noise-resistant Speech Sensing for Voice-User Interface. In Proceedings of ACM MobiSys. 14–26.   
[36] Lei Yang, Yao Li, Qiongzheng Lin, Huanyu Jia, Xiang-Yang Li, and Yunhao Liu. 2017. Tagbeat: Sensing mechanical vibration period with COTS RFID systems. IEEE/ACM Transactions on Networking 25, 6 (2017), 3823–3835.   
[37] Zhicheng Yang, Parth H. Pathak, Yunze Zeng, Xixi Liran, and Prasant Mohapatra. 2017. Vital sign and sleep monitoring using millimeter wave. ACM Transactions on Sensor Networks 13, 2 (2017), 1–32.   
[38] Yang Zhang, Gierad Laput, and Chris Harrison. 2018. Vibrosight: Long-Range Vibrometry for Smart Environment Sensing. In Proceedings of ACM UIST. 225– 236.   
[39] Mingmin Zhao, Fadel Adib, and Dina Katabi. 2016. Emotion recognition using wireless signals. In Proceedings of ACM MobiCom. 95–108.   
[40] Anfu Zhou, Shaoyuan Yang, Yi Yang, Yuhang Fan, and Huadong Ma. 2019. Autonomous Environment Mapping Using Commodity Millimeter-wave Network Device. In Proceedings of IEEE INFOCOM. 1126–1134.   
[41] Yanzi Zhu, Yuanshun Yao, Ben Y. Zhao, and Haitao Zheng. 2017. Object recognition and navigation using a single networking device. In Proceedings of ACM MobiSys. 265–277.   
[42] Yanzi Zhu, Yibo Zhu, Ben Y. Zhao, and Haitao Zheng. 2015. Reusing 60 GHz radios for mobile radar imaging. In Proceedings of ACM MobiCom. 103–116.