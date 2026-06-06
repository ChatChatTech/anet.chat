# Vernier: Accurate and Fast Acoustic Motion Tracking Using Mobile Devices

Yunhao Liu, Jiliang Wang, Yunting Zhang, Linsong Cheng,

Weiyi Wang, Zhao Wang, Weimin Xu, Zhenjiang Li

School of Software, Tsinghua University

Department of Computer Science and Engineering, Michigan State University

Department of Computer Science, City University of Hong Kong

Abstract—Acoustic motion tracking has been viewed as a promising user interaction technique in many scenarios such as Virtual Reality (VR), Smart Appliance, video gaming, and etc. Existing acoustic motion tracking approaches, however, suffer from long window of accumulated signal and time-consuming signal processing. They are inherently difficult to achieve both high accuracy and low delay. In this paper, we present Vernier, an efficient and accurate acoustic tracking method based on commodity mobile devices. We design a new approach to efficiently and accurately derive phase change and thus moving distance. Vernier significantly reduces the tracking delay/overhead by removing the complicated frequency analysis and long window of signal accumulation, while keeping a high tracking accuracy. We implement Vernier on Android, and evaluate its performance with COTS mobile devices including Samsung Galaxy S7 and Sony L50t. Experimental results show that Vernier outperforms previous approaches with a tracking error less than 4 mm. The tracking speed achieves 3× improvement to the previous phase based approaches and 10× to Doppler Effect based approaches. Vernier is also validated in applications like controlling and drawing, and we believe it is generally applicable in many real applications.

Index Terms—acoustic signal, tracking, mobile phone

# 1 INTRODUCTION

The rapid development and prevalence of mobile devices enable various ubiquitous mobile applications [33] [19] [41]. Acoustic motion tracking using mobile devices has been demonstrated as a promising user interaction technique in many scenarios such as Smart Appliance (e.g., TV control), Virtual Reality (VR), Augmented Reality (AR), video gaming, and etc., attracting many attentions and research efforts. In acoustic motion tracking, a mobile phone tracks its position using received acoustic signal. For example, with acoustic motion tracking the gesture or posture of a user can be obtained, which can facilitate various applications [33] [38].

Typically, inertial sensors such as accelerometer, gyroscope can be used for mobile motion tracking [37]. However, the tracking error is high (up to 60 cm even in 6s [37]) and thus accurate tracking is difficult to achieve [19]. Various approaches leverage RF signal for mobile device tracking [32] [27] [12] [35]. Those approaches usually require special hardware support or incur a high computation overhead [29] [5] [3] [2].Visual inertial odometry can achieve tracking based on visual and inertial information. Based on camera information, odometry provides nice way for tracking.

Recently, acoustic signal based motion tracking is proposed as a promising technique[25][30][16][4][18][13][6][10]. CAT [19] introduces a novel distributed Frequency Modulated Continuous Wave (FMCW) based method for mobile motion tracking. Using FMCW, the calculation of moving time is translated to calculation of frequency. CAT improves the accuracy by combining inertial sensors. LLAP [33] further persents a tracking method based on phase shift of acoustic signal. In LLAP, a mobile phone transmits an acoustic signal, which is reflected by a moving target and received by the mobile phone again. By calculating the phase shift between the original signal and the reflected signal, the signal travelling time and thus moving distance of the target can be obtained.

Existing approaches, however, all have some limitations in terms of tracking accuracy, overhead and delay. Most approaches require frequency analysis (e.g., FFT) to derive the frequency shift, phase, etc., which inevitably introduces a high computation overhead and delay [37] [7]. Moreover, tracking accuracy is also limited by window length. Achieving high accuracy requires accumulating and processing a sufficient window of signal. Thus it is difficult to achieve both low latency and high accuracy simultaneously. Those limitations hinder performance improvement for acoustic motion tracking and limit their practical application.

# 1.1 Our Approach

To address the limitations, we propose Vernier, an accurate and fast acoustic motion tracking approach using mobile devices. A mobile device running Vernier receives inaudible acoustic signals, each at a certain frequency, from different signal sources (e.g., speakers on TVs). Instead of calculating the frequency shift directly (e.g., using FFT), Vernier employs a novel method to calculate the phase change due to frequency shift with a small window of signal. It then calculates the distance change to each source and derives the real-time position of the mobile device.

![](images/3f68d02456921c079a453175b32d94c1897eb75ed383c119d1813a39913ecc21.jpg)



Fig. 1: Principle of our approach.

In the heart of Vernier, we design a novel method to efficiently calculate the phase change based on a very small window of samples (e.g., 100 samples). This method is inspired by vernier caliper. Signal samples in our method act as the vernier while the local maximums of original signal act as the ruler. For different phase changes (length), the samples on the vernier has different matching positions (local maximum) on the ruler, which can be leveraged to further derive phase change. To further improve the efficiency, we propose a Differentiated window based phase change calculation (DW-PC) in which we calculate the phase change based on local maximum change between two windows. Later we will show that our method can achieve a higher accuracy than existing approaches while has a much smaller delay and overhead.

Overall, Vernier aims to achieve the following goals: (1) accurate tracking with mm-level error, (2) a low delay in order to enable real-time applications such as mobile gaming and (3) a low computation overhead efficiently run on commodity mobile devices.

# 1.2 Summary of Main Results

We implement Vernier on Android and evaluate it on different mobile devices including SAMSUNG Galaxy S7/Sony L50t. Vernier has no special hardware requirements and can run on most commodity mobile phones. The evaluation results show that Vernier can achieve efficient tracking with a median error less than 4 mm in various scenarios at a distance of 7 m. We believe Vernier can facilitate nowadays user interaction like Video Games, VR, AR, smart home applications, and etc.

Our major contributions are as follows:

We design Vernier, an accurate and fast motion tracking approach on mobile devices, which leverages a novel method to efficiently and accurately derive phase change and thus moving distance.   
We analyze the performance of Vernier and compared it with existing approaches. The analysis result shows the performance improvement of Vernier.   
We implement Vernier on Android and evaluate it on different mobile devices including SAMSUNG Galaxy S7/Sony L50t. The evaluate results show that Vernier can achieve efficient tracking with a median error less than 4 mm in various scenarios at a distance of 7 m.

The remainder of this paper is organized as follows. Section 2 analyzes the limitations of existing approaches. Section 3 presents the main design of our approach. Section 4

![](images/bd0af75470ee05ca925e89fece11115f7f15c737f2ddd031c79d496563455f4e.jpg)



Fig. 2: Calculate the time t based on FMCW.

shows implementation parameters in real applications. Section 5 shows the evaluation results. Section 7 concludes this work.

# 2 PRIOR ARTS

We briefly introduce the basic mechanisms of existing acoustic motion tracking approaches and their practical limitations.

# 2.1 Tracking based on Doppler Effect

Suppose a sound source is emitting a signal and a moving receiver receives the signal. Due to the Doppler Effect, the receiver’s relative speed v to the sound source can be calculated by:

$$
v = \frac {F _ {\Delta}}{F _ {0}} c \tag {1}
$$

where $F _ { 0 }$ is the original frequency of the signal, $F _ { \Delta }$ is the frequency shift due to the Doppler Effect, and c is the speed of sound. Therefore, the moving distance for time $\bar { T ^ { } }$ can be calculated as $\begin{array} { r } { d = \int _ { 0 } ^ { T } } \end{array}$ vdt. As a result, given the initial position, the target can be tracked. We derive the resolution of moving speed as

$$
\hat {v} = \frac {\hat {F}}{F _ {0}} c = \frac {F _ {s}}{L _ {w} F _ {0}} c. \tag {2}
$$

We can see that the accuracy of moving speed (and thus distance) is related to the window size $L _ { w } . \mathrm { A }$ larger window can provide better frequency domain resolution and higher moving speed accuracy. On the other hand, a larger window contains more samples and causes a larger delay. For a typical window $L _ { w } = 1 7 6 4$ samples and a sampling rate $\bar { F _ { s } } = 4 4 1 0 0$ Fs Hz [37] [33], the accuracy of spectrum $D _ { F }$ is $\begin{array} { r } { \frac { F _ { s } } { L _ { \infty } } = \frac { 4 4 1 0 0 } { 1 7 6 4 } = 2 5 } \end{array}$ Lw Hz. Suppose the frequency $F _ { 0 } = 2 0 0 0 0$ Hz and the speed of sound wave $c = 3 4 0$ m/s, the moving speed resolution is $\begin{array} { r } { \hat { v } = \frac { 2 5 \times 3 4 0 } { 2 0 0 0 0 } = 0 . 4 2 5 \mathrm { m } / \mathrm { s } , } \end{array}$ indicating that the accumulated distance error in 1 second can be up to 0.425 m. The corresponding delay using such a window is $1 7 6 4 / 4 4 1 0 0 = 4 0$ ms. Moreover, Doppler shift is subject to high noise.

# 2.2 Tracking based on FMCW

A Frequency Modulated Continuous Wave (FMCW) or chirp is a signal with linearly increasing Frequency. An FMCW of length T with frequency ranging from $f _ { m i n }$ to $f _ { m a x }$ can be denoted as

$$
R (t) = \cos (2 \pi (f _ {m i n} + \frac {B}{2 T} t) t). \tag {3}
$$

where $B = f _ { m a x } - f _ { m i n }$ is the bandwidth.

![](images/b8d3a3356c6c4649907c77cc130775d1a52df4385c7fa36b27e2644d00aef115.jpg)



Fig. 3: Working flows of different approaches.

Assume a mobile phone needs to measure the length of path an FMCW travels, e.g., the round-trip distance to a reflected object. By using FMCW, the travelling time calculation can be translated to frequency calculation. The mobile phone first transmits an FMCW signal, which is directly received by the mobile phone itself. Meanwhile, the signal travels along the reflected path and is received by the mobile phone again. The received signal can be denoted as $R ^ { \prime } ( t ) = \stackrel { - } { \alpha } R ( t - \stackrel { . } { t } _ { d } )$ , where $t _ { d }$ is the time delay for travelling along the path and α is the attenuation. Note CAT [19] removes the requirement of receiving reflected signal and synchronization between receiver and signal source by a distributed FMCW. But the basic idea of distance calculation is similar. As shown in Figure 2, the distance d can be calculated as

$$
d = \frac {c \cdot t _ {d}}{2}. \tag {4}
$$

The time $t _ { d }$ can be calculated by the frequency difference $\Delta f$ between two FMCW signals, i.e.,

$$
t _ {d} = \frac {\Delta f \cdot T}{B}. \tag {5}
$$

According to Eq. (5) and (4), the travelling distance can therefore be calculated as $\begin{array} { r } { \dot { d } = \frac { \Delta f \cdot c \cdot T } { B } } \end{array}$ ∆f·c·TB . Thus, the accuracy B of distance can be calculated as

$$
\hat {d} = \frac {c}{B} \tag {6}
$$

Eq. (6) shows that the accuracy is only related to B. For B = 10 kHz [19], which is very large for acoustic signal on mobile, the accuracy is $\hat { d } = 3 4 0 / 1 0 0 0 0 = 0 . 0 3 4 \mathrm { m }$ .

FMCW based approaches require multiplying two signals (to derive $\Delta f ) ,$ frequency analysis (e.g., FFT) and low pass filtering (to remove the high frequency component).

# 2.3 Tracking based on Phase

Recently, LLAP [33] proposes a method for mobile tracking based on low latency acoustic phase [34]. Suppose a sound signal $R ( t ) = \cos 2 \pi f t$ travels through a path p with timevarying path length of $d _ { p } ( t )$ . According to [33], the received sound signal from path p can therefore be represented as

$$
R _ {p} (t) = 2 A _ {p} ^ {\prime} \cos (2 \pi f t - 2 \pi f d _ {p} (t) / c) \tag {7}
$$

where $2 A _ { p } ^ { \prime }$ is the amplitude of the received signal, the term $2 \pi f \dot { d } _ { p } ( t ) / c$ comes from the phase lag caused by the propagation delay of $d _ { p } ( t ) / c$ and c is the speed of sound. The key idea is to obtain the phase from the received signal $R _ { p } ( t )$ . Based on the phase, the change of path length ${ \dot { d } } _ { p } ( t )$

can be obtained. By multiplying the received signal with the signal source cos 2πf t, we have

$$
R (t) R _ {p} (t) = A _ {p} ^ {\prime} (\cos (- 2 \pi f \frac {d _ {p} (t)}{c}) + \cos (4 \pi f t - 2 \pi f \frac {d _ {p} (t)}{c})). \tag {8}
$$

The high frequency component $\cos ( 4 \pi f t - 2 \pi f d _ { p } ( t ) / c )$ can be removed by a low pass filter. Therefore, we can obtain $I _ { p } ( t ) = A _ { p } ^ { \prime } ( \dot { \cos } ( - 2 \pi \hat { f } d _ { p } ( t ) / c )$ . Similarly, multiplying the received signal $R _ { p } ( t )$ with $\sin ( 2 \pi f t )$ , we obtain $Q _ { p } ( t )$ = $A _ { p } ^ { \prime } \sin ( - 2 \pi { \dot { f } } d _ { p } ( t ) { \dot { / } } c )$ . Then based on $I _ { p } ( t )$ and $Q _ { p } ( t )$ , we can calculate the phase $- 2 \pi f d _ { p } ( t ) / c = \overline { { a r c t g ( Q _ { p } ( t ) / I _ { p } ( t ) ) } }$ . Therefore, the path length change in a short time period can be calculated by the phase change.

# 2.4 Summary

We plot the main working flow of different approaches in Figure 3. Both Doppler and FMCW based approach require frequency analysis and filtering, which incur extra overhead on mobile devices. Moreover, the frequency analysis and filtering introduce an inevitable delay, e.g., accumulating a window of samples for processing. They also inherently have a limited resolution in distance measurement. Phase based approach significantly improve the accuracy. It still requires multiplying the received signal with a given signal. It also requires different filters for signal processing, which incurs a relative high computation overhead and a nonnegligible delay.

The analysis coincides with the experimental results in those approaches: (1) For Doppler Effect based approach [37], the median error for tracking is around 1.4 cm and quickly increases over time due to error accumulation. The tracking delay is 40 ms. (2) For FMCW based approach [19], the median tracking error is 6 mm by combining inertial sensors. The tracking delay is at least 40 ms due to the length of STFT window. (3) For phase based tracking [33], the 1D tracking accuracy is 3.5 mm the tracking latency is 15 ms. The effective range for tracking is within 40 cm according to their experiments.

On the other hand, we noticed that passive tracking suffers from multipath effect severely. As a result, the systems based on passive tracking always works in constrained space [9][40][26]. Active tracking can obtain long-distance tracking but suffers from time Inconsistency. As a result, the systems based on active tracking always suffer from accumulative error.

# 3 VERNIER DESIGN

We have the following goals in the design:

Accurate: the approach should be accurate with error in mm-level.   
Efficient: the approach should incur a low overhead, and run on commodity mobile phones without specific hardware support.   
Low latency: the approach should be able to calculate the position with a very small delay to satisfy realtime applications like mobile gaming and VR.

![](images/2daf8431ed9f8ad0a826a1a521b16a1329894aee97f33f489b3ba9b78c57c3c1.jpg)



Fig. 4: Local maximum number and phase change.

![](images/c53bf103545d4ee6966581992a1e97afeadfc84536b4b42f7b5c47a4252505f7.jpg)



Fig. 5: Vernier Caliper.

# 3.1 Principle of Vernier Caliper

As shown in Figure 5, a vernier caliper consists of a sliding vernier and a fixed ruler. In Figure 6, we can see the scale on the sliding vernier is 0.9 mm and the scale on the fixed ruler is 1 mm. If the length of the measured thing is r mm, we have $r - \lfloor r \rfloor + 0 . 9 x = 1$ .0x and then we have: $r - \lfloor r \rfloor =$ 0.1x where x is the reading of aligned sliding scale. When the $\mathbf { r } = 5 . 0$ mm (as shown in Figure 6(a)), $r \bar { - } \lfloor r \rfloor = 0 ,$ we have x = 0. When the r = 5.1 mm (as shown in Figure 6(b)), $r - \lfloor r \rfloor = 0 . 1$ , we have x = 1. When the $\mathbf { r } = 5 . 5$ mm (as shown in Figure $6 ( \mathrm { c } ) ) , r - \lfloor r \rfloor = 0 . 5$ , we have x = 5.

The principle of our approach is inspired by vernier caliper. In our scenario, the sound waves’ peaks are token as the scales on the ruler and samples as the scales on the vernier, both with fixed intervals at a certain time period. Suppose the sound wave cycle is 1 ms and the sampling interval is 0.9 ms. As a result, if the sampling become late for 0.1 ms than before( which means the vernier moves right 0.1 ms), there will be only one sample across a sound wave’s peak. For each sample, we calculate the numbers of peaks before it, and we can know how much time the sampling becoming late.

Suppose a sound source generates sound wave continuously. The sound flies in the air in the speed c. A someone stands near the sound source must hear the sound earlier than a person far away. Similarly, for a sound recording device, if it becomes far away from the sound source, the sampling will become late. The time delay t is proportional to the distance d. If we get the time delay t, the distance d is easy to compute. In this work, the sampling interval are token as the sliding scale and the sound wave cycle are token as the fixed scale.

# 3.2 1D Tracking

We first introduce our approach for 1D case. We then show how to extend to 2D and 3D cases. Considering a static sound source transmits an acoustic signal of frequency $F _ { 0 }$ and a moving receiver (e.g., mobile phone) receives the sound signal. For example, the signal source is the TV speaker and the mobile phone is held by a user. The goal for 1D tracking is to derive the mobile phone’s moving distance d to the sound source. The distance can be calculated as $\begin{array} { r } { d \ = \ \int _ { t } v ( t ) d t } \end{array}$ . Denote the sampling rate as $F _ { s }$ and the frequency for the received signal as $F _ { c } = F _ { \Delta } + F _ { 0 }$ . Due to Doppler Effect, for a time period of length T , we have

![](images/5f65caaa8b77379878e3d5b7d19aadf82642c6c0d540069e4da711d2ea03f0dd.jpg)



![](images/4ca0de75461f7a03f2a445e13d1a600f44a37cbd90b40d9eeb13ec7e76fe68a5.jpg)



![](images/08008642a5fb8fbaad5cdd8dc57642e141561388c7aa8fdd0bf568d78a1dc16e.jpg)



Fig. 6: Principle of vernier caliper.

$$
d = \frac {c}{F _ {0}} \int_ {t} F _ {\Delta} d t = \frac {c}{F _ {0}} \int_ {t} (F _ {c} - F _ {0}) d t = \frac {c \tilde {\phi}}{2 \pi F _ {0}} - c T \tag {9}
$$

where $\tilde { \phi }$ is the phase change for the received signal in a time period of length T , and λ is the wavelength of acoustic signal at frequency $F _ { 0 } .$ . From Eq. (9), we translate distance calculation during a time period [0, T ] to calculation of the phase change φ˜. The phase change can be calculated by the start phase and end phase during the time period. Denote φ0 as the phase at time 0 and $\phi _ { T }$ the phase at time T , we have $\phi = \phi _ { 0 } - \phi _ { T }$ .

# 3.2.1 Sampling based phase calculation

We show how to use the samples to derive the phase change φ˜ in a time window [0, T ] containing n samples. Intuitively, the samples contain the information of phase change. For example, the number of local maximum (or minimum) $N _ { m a x }$ corresponds to the number of cycles in the signal, as long as the sampling frequency $F _ { s }$ is larger than the Nyquist sampling rate. Therefore, the phase change $\tilde { \phi }$ can be approximated as $\tilde { \phi } = N _ { m a x }$ · 2π. Combined with Eq. (9), we can approximate the moving distance $N _ { m a x } \lambda ~ { \stackrel { . } { - } } ~ c T$ . The approximation error is less than a wavelength, i.e. $\lambda = c \bar { / } \hat { F } = 1 . 7$ cm when $F _ { 0 } = 2 0 0 0 0 \mathrm { \ : H z }$ .

Now we show how to improve the accuracy in practice.

Lemma 1. The expected number of local maximums for a signal of phase change $2 \pi N + \phi _ { 0 } ( 0 \leq \phi _ { 0 } < 2 \pi )$ is $\bar { N } + \phi _ { 0 } / 2 \bar { \pi }$ .

Proof 1. Without loss of generality, we assume $0 \leq \phi _ { 0 } \leq$ $\pi / 2 .$ . To calculate the expected number of local maximum. We set $N _ { 1 }$ as the number of local maximum when $\phi _ { 0 } = 0$ . We assume the start of the signal is uniformly distributed in a cycle, i.e., [0, 2π]. As shown in Figure $^ { 4 , }$ the expected number of local maximum is calculated by

![](images/0174df122155094e6ff34a149aa0da79e1bcda761c60af8ef95bc00323fe81dd.jpg)  
Fig. 7: Phase change calaulation $( q = 1 3$ and $p = 3 )$ .

$$
\bar {N} = \int_ {0} ^ {\frac {\pi}{2} - \phi_ {0}} N _ {1} + \int_ {\frac {\pi}{2} - \phi_ {0}} ^ {\frac {\pi}{2}} (N _ {1} + 1) + \int_ {\frac {\pi}{2}} ^ {2 \pi} N _ {1} = N _ {1} + \frac {\phi_ {0}}{2 \pi}. \tag {10}
$$

Similarly, we can extend the proof to the case of $\pi / 2 <$ $\phi _ { 0 } < 2 \pi .$ .

Lemma 1 shows the detailed relation between the frequency change and the number of local maximums. It also shows that by calculating the expected number of local maximum, we can derive the phase change of the signal. Meanwhile, local maximum can be extended to other relatively fixed points in each cycle, e.g., local minimum.

# 3.2.2 Moving window based phase change calculation

Practically, one of the challenges is how to obtain the expected number of local maximum. According to Lemma 1, we need uniformly distributed sampling windows. However, as long as the first window is given, all following windows are determined given the fixed sample frequency. Intuitively, we can randomly choose windows, introducing relatively a long delay to process all windows. We show how to derive the phase change based on the local maximum with discrete samples. Without loss of generality, we consider a signal of p cycles containing q samples as shown in Figure 7. Note p and q can be simply calculated by the smallest integer satisfying $p / q \ = \ F _ { c } { ' } \dot { F } _ { s }$ . For example, if $F _ { s } ~ = ~ 4 4 1 0 0$ Hz and $F _ { c } ~ = ~ 2 0 0 0 0$ Hz, we have $p \ = \ 2 0 0$ and $q = 4 4 1$ . For the ith sample of phase φ[i], denote its relative phase as $\phi [ i ]$ mod $2 \pi$ .

Lemma 2. The relative phases of q samples are uniformly distributed in [0, 2π].

Proof 2. Without loss of generality, assume the signal has an initial phase 0. The relative phase of the ith sample can be calculated as $i p 2 \pi / q$ mod $2 \pi = ( i p$ mod $q ) 2 \pi { \bar { / } } q .$ The result of $i p$ mod q are pairwise distinct for $0 \leq i < q .$ Therefore, the relative phases of q samples are evenly distributed in [0, 2π].

For example, as shown in Figure 7, there are 13 samples covering 3 cycles, i.e., $q = 1 3$ and $p = 3 .$ . Folding the 13 samples into a single cycle results in uniformly distributed samples in the cycle.

# 3.2.3 Differentiated window based phase change calculation

We further propose an efficient method to improve the efficiency, namely Differentiated Window based Sample Counting for Phase Change Calculation (DW-PC).

# Algorithm 1 DW-PC(m, φ˜)

Input: m $\underline { { \boldsymbol { \cdot } } } [ i ] ( i = 1 , 2 , \ldots ) ,$ , the samples continuously feeded from the sampling component.

Output: the phase change $\tilde { \phi } [ i ] ( i = 1 , 2 , . . . ) .$

1: $\tilde { \phi } [ 1 ] = 0$   
2: $\dot { N _ { m a x } } = L M P S ( m [ 1 ] , m [ 2 ] , \dots , m [ q ] )$   
3: for $\mathrm { i } = 2 ;$ ;i++ do   
4: $\underset {  m a x } { \underbrace { N _ { m a x } ^ { \prime } } } = L M P S ( m [ i ] , m [ i + 1 ] , \ldots , m [ i + q - 1 ] )$   
5: $\tilde { \phi } [ i ] = ( N _ { m a x } ^ { \prime } - \dot { N } _ { m a x } ) \cdot \dot { 2 } \pi / q$   
6: end for

Assume there are two windows $w _ { 1 }$ and $w _ { 2 }$ of samples. Each window contains $q$ samples that cover $p$ cycles of signal. Denote the q samples in $w _ { 1 }$ and $w _ { 2 }$ by $m _ { i } ( 1 \leq i \leq q )$ and $m _ { i } ^ { \prime } ( 1 \leq i \leq q )$ . We show that the phase change between $m _ { 1 }$ and $m _ { 1 } ^ { \prime }$ can be calculated based on samples in $w _ { 1 }$ and $w _ { 2 }$ . For sample $m _ { i } ( 0 ~ < ~ i ~ \leq ~ q )$ in $w _ { 1 } ,$ , define the Local Maximum Prefix (LMP) $l _ { i } ( 0 < 0 \le q )$ as the number of local maximum from the beginning of w1 to $m _ { i }$ . Define the Local Maximum Prefix Sum (LMPS) of $w _ { 1 }$ as $\begin{array} { r } { L = \sum _ { i = 1 } ^ { q } l _ { i } . } \end{array}$ Similarly, the LMPS of $w _ { 2 }$ is denoted as $L ^ { \prime } .$ We have the following lemma.

Lemma 3. Assume the LMPS of $m _ { 1 }$ and $m _ { 1 } ^ { \prime }$ are L and $L ^ { \prime }$ respectively, the phase change between $m _ { 1 }$ and $m _ { 1 } ^ { \prime }$ is $( L ^ { \prime } - L ) \frac { 2 \pi } { q }$ .

Proof 3. Lemma 2 shows that the relative phase of q samples are evenly distributed in [0, 2π] with inter-distance $2 \pi / q .$ As shown in Figure $^ { 7 , }$ we can virtually fold all samples into a cycle to obtain uniformly distributed samples in the cycle. Moving the window by $2 \pi / q$ causes the local maximum prefix of exactly one sample increases (decreases) by 1. As a result, the LMPS is increased by 1. Therefore, if the LMPS is increased by $n ,$ , i.e. $L - L ^ { \prime } = n ,$ the window is moved by $n 2 \pi / q$ . Thus the phase change between $m _ { 1 }$ and $m _ { 1 } ^ { \prime }$ is ${ \dot { ( L ^ { \prime } - L ) } } 2 \pi / q$ .

Lemma 3 shows how to calculate phase change. The calculation is not based on the measuring the number of local maximums. Lemma 3 shows the relationship between the LMPS difference and phase change. According to Lemma $^ { 3 , }$ we can use the LMPS difference of two windows to estimate the phase change between the start of two windows. If the LMPS difference of two windows is $n ,$ the phase change $\tilde { \phi }$ can be calculated as $n 2 \pi / q .$ Clearly, the error $e _ { \phi }$ is at most $2 \pi / q .$ Otherwise, the LMPS difference of those two windows should not be n. Based on the phase change $\phi ,$ according to Eq. (9), we can calculate the moving distance by phase change.

According to Eq. (9), the moving distance error can be calculated as 2πF $\frac { c { \cdot } e _ { \phi } } { 2 \pi F _ { 0 } }$ c·eφ . For $F _ { 0 } = 2 0 0 0 0$ and $q = 1 0 0 .$ , we can see that the distance error by this method is only 0.17 mm. Based on ${ \mathrm { D W } } { \cdot } { \mathrm { P C } } ,$ a mobile phone can continuously measure the moving distance. DW-PC can even update the moving distance for each sample, supporting efficient and accurate position measurement and motion tracking. For example, when q is set to 100, only 100 samples are required for each window, $\mathrm { i . e . , }$ , DW-PC can calculate the moving distance with a delay of $1 0 0 / F _ { s } = 2 . 3$ ms.

Algorithm 1 shows the simplified and main steps of DW-PC. The array $\tilde { \phi } [ \cdot ]$ is used to store the phase change. Line 1-2 initialize the parameters. Line 4 calculates the $N _ { m a x } ^ { \prime }$ for window w2. Line 5 calculates the phase change based on Lemma 3. We can see that DW-PC measures the phase change with at most a linear computation overhead to the window length (calculate the local maximum and LMCPS). Usually, the window length is very small (e.g., 100), leading to a very small computation overhead. Therefore, DW-PC can support accurate and efficient distance movement measurement. The performance of DW-PC is further evaluated in Section 5.

![](images/8f2b925c8291921fdfbb2fe438734db341907380ab061dccf96498302f3ef2fb.jpg)



Fig. 8: 2D tracking based on DW-PC.

# 3.3 Frequency of Received Signal

In practice, we do not know the frequency of the received signal (otherwise, we can calculate the velocity based on Doppler Effect), so we do not know the precise value of q. We set the window to contain a fixed number of samples (e.g., 100). We show that DW-PC can achieve a high accuracy with a fixed value of $q .$ When q samples cover p cycles of signal, we can obtain the phase change with error less than $2 \pi / q$ . When $q$ samples cover $p + x \ ( 0 \textless x \textless 1 )$ cycles of signal, we show that LMPS only introduces phase error 2xπ. According to Lemma $^ { 3 , }$ the phase change can be calculated by $n \cdot 2 \pi { \dot { / q } }$ if the LMPS is n for p integral cycles. For $p + x$ cycles, we show that $n \cdot 2 \pi / q + x$ phase change can lead to LMPS change by n. For the ith sample $m _ { i } ^ { \prime }$ in $p + x$ cycles, we map it to the ith sample $m _ { i }$ in p cycles. The maximum offset between $m _ { i }$ and $\bar { m _ { i } ^ { \prime } }$ is less than x. Therefore, if the LMP of the ith sample changes by a phase change φ, the corresponding sample in $p + x$ cycles should also change by a phase change $\phi + x .$ . Thus the phase error is at most x2π.

According to Eq. (9), the distance error introduced is calculated as $\textstyle { \frac { c \cdot x } { 2 \pi F _ { 0 } } }$ . As $p / q = F _ { 0 } / F _ { s } ,$ x can be calculated by $\frac { F _ { c } - F _ { 0 } } { F _ { 0 } }$ 0. The distance error is $\textstyle { \frac { p \cdot v } { c } } \lambda$ . We can choose $F _ { 0 }$ F0 such that p is a small value. For example, when $F _ { 0 } = 1 7 0 0 0$ Hz [33] and $F _ { s } = 4 8 0 0 0 \mathrm { H z }$ , we have $\bar { p } / q = 1 7 / 4 8 = F _ { 0 } / F _ { s }$ . In such a case, the error can be calculated as 17·v340 · 0.02. Even $\frac { 1 7 \cdot v } { 3 4 0 } \cdot 0 . 0 2$ when the moving speed is up to $2 \mathrm { m } / \mathrm { s } ,$ the error can be less than 2 mm.

# 3.4 2D/3D Tracking

2D and 3D tracking can be achieved based on 1D tracking. Assume the distance between two speakers A and B is $d _ { 0 }$ in 2D tracking. As shown in Figure 8, we build the axis with A as the origin and x-axis along the direction from A to $B .$ Assume the mobile phone moves from $X _ { 0 }$ to $X _ { 1 }$ and the position of $X _ { 0 }$ is known.

We show how to calculate the new position $X _ { 1 }$ by DW-PC. First, we calculate the distance $a _ { 1 }$ and $a _ { 2 }$ towards

![](images/c62b4ee63ee5a4aa3562ab09a251e087bfa8929587600886ee9d7f5b5c047906.jpg)



Fig. 9: Initial position of the mobile phone.

signal source A and B by DW-PC. We can then calculate the length $\overline { { { X _ { 1 } A } } } ~ = ~ \overline { { { X _ { 0 } A } } } - a _ { 1 }$ and $\overline { { { X _ { 1 } B } } } ~ = ~ \overline { { { X _ { 0 } B } } } ~ - ~ a _ { 2 }$ . Accordingly, we can calculate cos α = d20+X1A2−X1B . $\begin{array} { r } { \alpha = \frac { d _ { 0 } ^ { 2 } + \overline { { X _ { 1 } A } } ^ { 2 } - \overline { { X _ { 1 } B } } } { 2 d _ { 0 } \overline { { X _ { 1 } A } } } } \end{array}$ The position $( x _ { 1 } , y _ { 1 } )$ of $X _ { 1 }$ can be calculated as $x _ { 1 } = \overline { { X _ { 1 } A } }$ · cos α and $y _ { 1 } = { \overline { { X _ { 1 } A } } }$ · sin α. Similarly, 3D tracking can be achieved by 3 signal sources.

# 3.5 Initial Position of Signal Source

There are two types of information that need to be determined for most acoustic motion tracking approaches [37] [19] [33], $\mathrm { i . e . , }$ the initial position of mobile phone and the initial position of signal source. The first requirement is to calculate the initial position of the signal source. Assume there are two signal sources A and ${ \bar { B , } }$ as illustrated in Figure 9, calculating the initial position is equal to calculate the distance between two signal sources. As DW-PC can directly measure the distance a mobile phone has moved, we move the mobile phone from signal source A to source B. The distance between two signal sources A and B can be obtained.

# 3.6 Initial Position of Mobile Phone

Another important step is to measure the initial position of mobile phone. In [37] [19], a particular filtering method is used to derive the initial position. Intuitively, a large collection of initial positions are generated, each of which is tested according to the movement information. Finally, the centroid of the remaining particulars is calculated as the initial position. This introduces a high overhead and a large measurement error[37].

In our approach, we derive the initial position using DW-PC. Our method only needs to move the mobile phone for a certain distance towards a signal source or move the mobile phone from a signal source to any position to calculate the initial position. We call this method moving while initialization (MOWI).

As shown in Figure 9, assume the distance between A and B is $d _ { 0 } .$ . Here we mainly show how to measure the initial position by moving the mobile phone towards the signal source. The method by moving the mobile phone from the signal source to any initial position is similar. Suppose the initial position of mobile phone is X. A user moves the mobile phone from X to $Z ,$ passing a point $Y .$ During the moving process, we can calculate the distance from X to $Y$ and $\dot { Y }$ to $Z$ using DW-PC. Thus we can calculate the distance for $a _ { 1 } , a _ { 2 }$ for the movement from X to Y , and $b _ { 1 }$ and $b _ { 2 }$ for the movement from Y to $Z$ respectively.

![](images/7920397b7d82716d5079974e251795f15ac965e23ad75cb858442f5d834e5a31.jpg)



(a)

![](images/c08c492236e1f84358a77accf9823a728e6b8d60ae39cdec1197debb4e7636ab.jpg)



(b)   
Fig. 10: (a) Tracking error due to frequency shift; (b) The result after frequency compensation.

Denote the angle $\angle X B A$ as $\alpha ,$ the distance $\overline { { Z B } }$ as $d _ { 1 }$ and the distance $\scriptstyle { \overline { { Z A } } }$ as $d _ { 2 } ,$ , we have

$$
\left\{ \begin{array}{l} \cos \alpha = \frac {d _ {1} ^ {2} + d _ {0} ^ {2} - d _ {2} ^ {2}}{2 d _ {0} d _ {1}} \\ \cos \alpha = \frac {\left(d _ {1} + b _ {1}\right) ^ {2} + d _ {0} ^ {2} - \left(d _ {2} + b _ {2}\right) ^ {2}}{2 d _ {0} \left(d _ {1} + b _ {1}\right)} \\ \cos \alpha = \frac {\left(d _ {1} + b _ {1} + a _ {1}\right) ^ {2} + d _ {0} ^ {2} - \left(d _ {2} + b _ {2} + a _ {2}\right) ^ {2}}{2 d _ {0} \left(d _ {1} + b _ {1} + a _ {1}\right)} \end{array} \right. \tag {11}
$$

Solving this equation, we obtain the value of $d _ { 2 } .$ Plugging $d _ { 2 }$ to the equation array, we can obtain the value of $d _ { 1 }$ . We omit the details for the lengthy formula of $d _ { 1 }$ . Based on $d _ { 1 }$ and $d _ { 2 } ,$ we can obtain the coordination $( x , y )$ of X .

# 4 IMPLEMENTATION

We implement Vernier on Android 6.0.1 as an App. The signal sources of Vernier Tracker can be COTS speakers like the speakers on TV. In our implementation, we use the speaker (SV S840B) as shown in Figure 11. The speakers is connected to a mobile phone which can play audio files containing waves of different frequency. Instead of using a group of sine and chirp signals on different frequency bands [19], our approach uses sine waves (e.g., 20000 Hz and 17500 Hz for 2D tracking in our implementation). The sine wave files are generated on a desktop computer. Vernier on Android receives and analyzes the received signal, and displays the real-time location on the screen. Meanwhile, Vernier Tracker can also record all signal data for further analysis and comparison in evaluation.

# 4.1 Moving Distance Measurement

We use the equipment in Figure 12 (a) to measure distance accurately. The mobile phone is fixed on the platform of the equipment. We can move the platform horizontally and vertically by rolling the rocker. Figure 12 (b) shows the measured distance on the mobile app. In the app, we draw a virtual rule for 10 mm.

There are 25 scales on the rocker and the platform moves 1.25 mm when the rocker rolling one circle (0.05 mm for each scale). We can move the platform horizontally and vertically so we can obtain the ground truth for the mobile phone position.

# 4.2 Clock Inconsistency

During our implementation, we find that there exists a clock inconsistency for the generated signal and the received signal, which further leads to a distance measurement error.

![](images/c5d94c7fce499d50a62c1ab6c565383c55c14f43bd423eadcb60beafad47c834.jpg)



Fig. 11: Experiment scenario.

We conduct an experiment to validate the impact of clock inconsistency. We use a static mobile phone to receive the signal from a speaker and then calculate the distance from the mobile phone to the speaker. Figure 10 shows the result. We notice that even when the mobile phone is static, the distance is still increasing as shown in Figure 10 (a). We investigate the data and find this is due to a clock inconsistency between the signal source and mobile phone. Therefore, the received signal frequency, even when the mobile phone is static, is different from the signal source. This leads to a frequency shift and thus a non-zero moving speed, and distance between the mobile phone and signal source is continuously increasing.

To address the frequency inconsistency, we employ a linear frequency compensate (FC) to calibrate the frequency for the signal source and mobile phone. Assume the frequency shift between the mobile phone and the signal source is α. A signal at frequency $F _ { 0 }$ is received at frequency $( 1 + \alpha ) F _ { 0 }$ . By keeping the mobile phone static, we calibrate the frequency as follows. If there is no frequency drift, the calculated phase change by DW-PC for a time period T should be $T \bar { F _ { 0 } } 2 \pi$ . Assume the calculated the phase change by DW-PC for a time period $T$ is $\phi ,$ we can calculate the frequency drift $\begin{array} { r } { \alpha \ = \ \frac { \phi } { 2 \pi T } } \end{array}$ 2πT . We use α to compensate the frequency shift between the signal source and mobile phone. As shown in Figure 10 (b), we can see that the distance after FC is accurate.

# 5 PERFORMANCE EVALUATION

# 5.1 Experiment Methodology

We examine the performance of Vernier from the following aspects.

Tracking accuracy: we show the accuracy of Vernier in motion tracking compared with other approaches.   
Delay: the time consumption of Vernier and existing approaches.   
Robustness: performance in different application environments.   
Overall performance: we also evaluate the overall performance for different tracking paths.

# 5.2 Tracking Accuracy

We first examine the 1D distance tracking error. Our experiments are conducted in indoor environment as in the meeting room in Figure 11. In this experiment, we vary the initial distance from the mobile phone to the speaker and calculate the corresponding distance measurement error. The result is shown in Figure 13 (a). The error is under 2 mm even when the distance between the mobile phone and speaker is 7 m. Figure 13 (b) shows the detailed measurement error of different moving distance for our approach. We move the mobile phone for different distance from 0 cm to 500 cm. The accumulated error is small for different moving distance, and it is only 27.3 mm when moving distance is up to 500 cm. This enables our approach for many applications, such as video gaming, VR, and smart appliances control.

![](images/ca4218900b546ed73d5021b1c990ff970c5db00378ba51feee27a7dcf9f4b045.jpg)



(a)

![](images/c0d5de9bdab82c5e4400fd62621a758bcb71f2b5b25e2a7bafaf611f3b91bd39.jpg)



(b)   
Fig. 12: (a) Moving distance measurement; (b) mobile app.

![](images/2d382a8cf98293fa839faef78ccf419d2fd359883ecb828c6cfc0d83e94d0d92.jpg)



(a)

![](images/281129aa1b44e8da72792126601de1861116f50e9d65cd1f1577fbe1fdb4a0a7.jpg)



(b)   
Fig. 13: 1-D accuracy: (a) Different initial distance; (b) Different moving distance.

We further measure the tracking accuracy in 2D case. In this experiment, we move the mobile phone following the a path of ”L” whose size is about 2 cm × 2 cm. Figure 16 (a) plots the tracking error of different distance from the mobile phone to the speakers. Figure 16 (b) shows how the tracking error being influenced by the speakers separation when the mobile phone is 3 m away from the speaker. We can see the error for different distance is slightly larger than that in 1D. Nevertheless, the error is still under 4 mm.

We also evaluate the performance of LLAP with a reflector initially with a distance 20 cm to the mobile phone. Then we move the reflector for 10 cm multiple times and measure the tracking error. Figure 5 shows the CDF of tracking error. We can see that most errors are under 15 mm and more than 50% errors are under 10 mm.

# 5.3 Delay Performance

In our evaluation, we implement most recent acoustic tracking approaches including Doppler Effect based approach [37] (denoted by Doppler), phase based approach [33] (denoted by LLAP) and FMCW based approach [19] (denoted by FMCW) for comparison. For fair comparison, we use the same recorded signal in performance comparison for different approaches. The FMCW based approach [19] requires both sine wave and chirp signal for tracking, so we generate chirp signals from 8500

![](images/8b97ae8fc5ef85d98ced070bd4390ba8f2617900bfd3ebbc0e1c93947a11a153.jpg)



Fig. 14: CDF of tracking error for phase+.

Hz to 18500 Hz for this approach. The mobile phone used in our evaluation is Samsung Galaxy S7 with Android 6.0.1.

We implement an active version of this approach by using the phase calculation method introduced in [33]. We directly use the received signal from the speaker instead of the reflected signal. Now the tracking range becomes much larger than before. We denote such a method Phase+. Figure 17 (a) shows average time consumption for each sample using different approaches on Android device.

# 5.4 Robustness

We now evaluate the performance of Vernier in different environments for practical scenarios. We focus on the performance from the following aspects:

• Different intensity of noise.   
• Different devices.   
• Different multipath scenarios.

The impact of noise intensity. We first vary the noise volume to different levels, i.e., around 40 db (library room), 50 db (air conditioner’s noise), 60 db (human talking) and 70 db (noisy street). We move the mobile phone for 1 cm. The result is shown in Figure 17 (b). We can see that the error increases as the noise level increases. The overall error for all distances is still very small.

The impact of device. We test other mobile phones (e.g., Sony L50t) and speakers. Figure 18 (a) shows the results on different devices when the mobile phone moves 1 cm. We can see that two different mobile phones have similar localization accuracy, which shows that our approach can work well on both mobile phones.

The impact of multipath scenarios. Ultra-sound has a strong directionality due to the short wavelength. As a result, the influence of multipath effect in active tracking system is especially weak. Figure 18 (b) shows the distance measurement error in different multipath environments when the mobile phone moves 10 cm at the distance of 1 m. We measure the error of moving distance in large open space, two multipath environments (multipath 1: four chairs around LOS, and multipath 2: two tables around LOS), and block the LOS with a box. We can see that the two multipath environments have similar accuracy with free space environment, and accuracy decrease a lot with LOS blocked. We can conclude that the influence of multipath effect in our experiment is slight. THis is because the LOS signal is much stronger than the reflected signal. Vernier uses acoustic signal on the time domain, the signal from reflect path is much weaker than the signal from LOS, and can only have slight influence on distance measurement. When the LOS is blocked, signal form different multipath can influence each other significantly, due to their strength is similar.

![](images/b433e62e214feaebbf5c3c586c4032031154d14c2644b35bc1cca2be4cdd2b88.jpg)  
(a)

![](images/d1cfbbb0ebb345d5fede1d6391db1dc0429e58182c76becca80f255c9ab5d904.jpg)



(b)

![](images/f24e037ed5c219de7dde6887de94b54b6846c45f02beeac5ec476822e32d32b0.jpg)



(c)

![](images/c30d7dd73a156882d7c0c8159a4266a5d5325d300c29bc0ca85081ca88b5d4c2.jpg)



(d)

![](images/d482c3085888d613568e3bb4005665b081d848fd37ef3f488ab006640bb0d737.jpg)



![](images/6e8973313123a65916c52d1980c5b4f9fc2321e16128de1a917d3e864d2b0f85.jpg)



(f)

![](images/6e5eb2eae4fa574b5922d40d44dad4eeb6ff913a012efc647788ae1f587cc343.jpg)  
(g)

![](images/cc3710675083ceddd2c572f2997ac16a60bb30cca8e8ab563ea03f3ace02b0ee.jpg)



(h)   
Fig. 15: Using 2D tracking to draw different templates. (a) (c) (e) (g) are the original templates of banana, snake, hat and rabbit. (b) (d) (e) (h) are drawing results.

![](images/6b0ec42022b5ed3e7948b115a71459d295a52cf0e91194b12be25321342d6766.jpg)



(a)

![](images/2c5c103f54be4fa077c4efc948c9c4397a4c9831faa166f9a956cf7a82107340.jpg)



(b)   
Fig. 16: 2-D accuracy: (a) Different initial distance; (b) Different speaker separation.

# 5.5 Overall Performance

We evaluate Vernier Tracker using the same method in [19]: the similarity between the Vernier Tracker reported trace and the standard drawing template. In this experiment, we use Vernier to draw different figures. We print different templates (banana, snake, hat and rabbit) and move the mobile phone following the curve of printed templates.

As shown in Figure 15, we plot the tracking results and compare them with the original templates. All the details in the original templates can be plotted, indicating a high accuracy of Vernier. It should also be noted that some places in the drawing may not be as smooth as the original template. We check the data and find the reason is that it is very difficult to control the drawing exactly and smoothly following the original curve. Nevertheless, the results demonstrate that Vernier preserves the details of the original templates and can be used in real applications.

# 5.6 User case

We insert our acoustic motion tracking system into an actual mobile game on Github and ask 11 volunteers to score the

![](images/46374c52fea8a548a2c3965e8ec507a231e02f9321d93c5e5c11ee7b5b69701c.jpg)



(a)

![](images/afd1320df97e19d034c4bc2e3101f773eac0535e482a7653165ecc1554240f7d.jpg)



(b)   
Fig. 17: (a) Time consumption of different approaches; (b) Median error of different noise intensity.

game in terms of four metrics: sensitivity, fluency, interest, noise immunity. The mobile game is a classic aircraft war game and we name it after NiPlane are shown by Figure 19(a). Every volunteer plays the game for 2 minutes and then scores it from 1 to 10 independently. We record all scores and calculate the average scores and their standard deviations as Figure 19(b) shows. Here, we have two observations. First, the average scores of all four kinds of metrics are high (7.5, 7.7, 7.3, and 8.7 respectively). The result demonstrates that the game with our acoustic motion tracking system is quite popular with the volunteers. Second, the average score for interest is the lowest, because the game may be too easy. The average score for noise immunity is the highest, which proves that our system owns high robustness. In future, we will integrate Vernier into more mobile and TV games to provide better user interactive experience.

# 6 RELATED WORK

There are a large collection of acoustic based ranging and tracking methods. We summarize them as follows.

ToA/TDoA based Ranging and Localization Approaches. The first category of methods for ranging and tracking is based on the time (or time difference) information using acoustic signal [17][15][25][13][39][30][16][4][18][23][39][20]. In Beep-Beep [23], each mobile phone transmits an acoustic signal separately and records the local arrival time of each other’s acoustic signal. By leveraging the local arrival time of signals from each other, BeepBeep can calculate the distance between two mobile phones. One of the advantages of BeepBeep is that it does not require synchronization between two mobile phones. By using FMCW, the calculation of time difference is transformed to calculation of frequency difference [21]. By calculating the frequency difference, the distance can thereafter be measured. CAT [19] presents a method to track mobile motion by using a distributed FMCW. CAT also combines Doppler Effect and inertial measurement unit (IMU) to enhance the measurement accuracy. The method in [16] enables fine-grained indoor localization via mobile phone. In [16], a special designed beacon node, which transmits modulated acoustic sharp pulse, is pre-deployed. By receiving beacons, a mobile phone derives the distance to those beacons based on Time of Arrival (TOA). Cricket [24], DOLPHIN [20] and Active Badge [30] can provide the range information based on ultrasound acoustic signal.

![](images/bbe705f5f1f5bdf0262cf56de10b62828dd5fb47368c1aa1b096a8b83cb35a25.jpg)



(a)

![](images/8365c406636e735bfcc32f9ff7a13ecef37123be8476c14bf20511dcbf68aa35.jpg)



(b)   
Fig. 18: (a) Median error on different devices; (b) Median error in different multipath scenario.

SwordFight [39] introduces a method to range the distance between two mobile phones using acoustic signal. In [25], a 3D localization method on mobile phone is proposed to support high-speed, phone-to-phone gaming (HLPP gaming). It needs to use the 3D accelerometers and magnetometers in position estimation. The accuracy is in centimeter level. The method in [13] focuses on generating linear frequency modulated acoustic signal inaudible to human beings. The method in [14] is based on the nonlinearity of the microphone and speaker for acoustic signal. In [31], the authors propose a method to achieve accurate localization with sub-millimeter accuracy based on a single beacon and a microphone array.

Doppler Effect based approaches. There are different approaches using Doppler effect for ranging and localization [22] [11] [28] [8] [37]. Different from the time based approaches, frequency shift and relative moving speed are estimated and calculated. Swadloon [8] proposes a method to derive the direction and location on mobile phone by shaking and walking. For an acoustic source S (e.g., a signal source which continuously generates an acoustic signal at a certain frequency), a mobile phone A with Swadloon can measure its direction to the acoustic source S. A user only need to move the mobile phone A with a certain pattern (e.g., rectangle) and speed. According to the frequency shift, the direction from the receiver to the acoustic source can be calculated.

![](images/7da15f2ec6d55eae657b6ae0ba87c9e6772e4d42fc542c79d013ffe1acdcf784.jpg)



(a)

![](images/d6ca56552065781f461dbb9cf458efe72c3180cf92f17f5d3f60396ccbfe8548.jpg)



(b)   
Fig. 19: User case of a mobile game. (a) Game interface; (b) average scores of four metrics.

AAMouse [37] can also provide real-time tracking of mobile devices based on acoustic signals. The mobile phone running AAMouse receives acoustic signal from speakers (e.g., from a TV’s speakers) and calculates the frequency shift due to Doppler effect. AAMouse then derives the moving speed of the mobile device. Given the initial position, AAMouse can track the mobile device. To calculate initial position, AAMouse leverages a particle filtering method in which many particles are generated and tested according to currently tracking results. The centroid of the left particles are used as the initial position.

Phase shift based approaches. Recently, LLAP [33] proposes a novel method based on the phase shift. It is based on the observation that the phase of a reflected signal will change while the length of travelling path is changing. The amount of phase shift is related to the moving distance. In LLAP, a mobile phone emits an acoustic signal and receives the reflected signal. In [33] a method is proposed to efficiently calculate the phase shift based on the original signal and reflected signal. Based on the phase shift, the distance between the mobile phone and the reflecting object can be calculated. By using two microphones to receive the reflected signal, the 2D position of the mobile phone can be obtained.

RF-based approaches. There are also a large collection of approaches for ranging and localization based on WiFi signal [32] [27] [12] [35] [29] [5] [3] [2] [1] [36]. For example, WiDraw [27] leverages the angel of arrival (AoA) of WiFi signal for localization. RF-IDraw [32] proposes to use commercial RFID reader to track object attached with RFID tags. Those approaches often require special hardware and incur a relative high computation overhead. In this study, we focus more on acoustic motion tracking using mobile device.

# 7 CONCLUSIONS

We present Vernier, an efficient and accurate acoustic motion tracking approach using commodity mobile devices. We address the fundamental limitations of existing approaches in terms of tracking accuracy, overhead and delay. In Vernier, we design a novel differentiated window based sample counting for phase estimate and mobile motion tracking. We show that Vernier can achieve accurate motion tracking with a window much smaller than existing approaches while incurring a small computation overhead and delay. We implement Vernier in Android and examine its performance with Samsung Galaxy S7 and Sony L50t. We conduct extensive experiments to evaluate the performance of Vernier. The results show that Vernier can achieve accurate motion tracking with error less than 4 mm in 7 m. We believe the design of Vernier is general and can facilitate various mobile applications such as video gaming, VR, AR, etc.

# 8 ACKNOWLEDGEMENTS

This work is supported in part by National Key R&D Program of China 2017YFB1003000, National Natural Science Fund China for Excellent Young Scholars (No. 61722210), NSFC, key program (No. 61532012, 61432015), NSFC No. 61572277, 61529202. Jiliang Wang is the corresponding author of this paper.

# REFERENCES

[1] F. Adib, Z. Kabelac, and D. Katabi. Multi-person localization via rf body reflections. In Proceedings of USENIX NSDI, pages 279–292, 2015.   
[2] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller. 3d tracking via body radio reflections. In Proceedings of USENIX NSDI, 2014.   
[3] P. Bahl and V. N. Padmanabhan. Radar: An in-building rfbased user location and tracking system. In Proceedings of IEEE INFOCOM, volume 2, pages 775–784. Ieee, 2000.   
[4] X. Bian, G. D. Abowd, and J. M. Rehg. Using sound source localization in a home environment. In H. W. Gellersen, R. Want, and A. Schmidt, editors, Proceedings of Pervasive Computing, 2005.   
[5] J. Gjengset, J. Xiong, G. McPhillips, and K. Jamieson. Phaser: enabling phased array signal processing on commodity wifi access points. In Proceedings of ACM MobiCom, pages 153–164. ACM, 2014.   
[6] J. Han, C. Qian, X. Wang, D. Ma, J. Zhao, W. Xi, Z. Jiang, and Z. Wang. Twins: Device-free object tracking using passive tags. In Transactions on Networking (TON), volume 25, pages 1605–1617. IEEE/ACM, 2016.   
[7] W. Huang, Y. Xiong, X. Li, H. Lin, X. Mao, P. Yang, and Y. Liu. Shake and walk: Acoustic direction finding and fine-grained indoor localization using smartphones. In 2014 IEEE Conference on Computer Communications, INFOCOM 2014, Toronto, Canada, April 27 - May 2, 2014, pages 370–378, 2014.   
[8] W. Huang, Y. Xiong, X. Li, H. Lin, X. Mao, P. Yang, Y. Liu, and X. Wang. Swadloon: Direction finding and indoor localization using acoustic signal by shaking smartphones. IEEE Transactions on Mobile Computing, 14(10):2145–2157, 2015.   
[9] R. Jia, M. Jin, Z. Chen, and C. J. Spanos. Soundloc: Accurate room-level indoor localization using acoustic signatures. In 2015 IEEE International Conference on Automation Science and Engineering (CASE), pages 186–193, Aug 2015.   
[10] Y. Jiang, Z. Li, and J. Wang. Ptrack: Enhancing the applicability of pedestrian tracking with wearables. In Proceedings of IEEE ICDCS, 2017.   
[11] K. Kalgaonkar and B. Raj. One-handed gesture recognition using ultrasonic doppler sonar. In Proceedings of IEEE Acoustics, Speech and Signal Processing, 2009.   
[12] S. Kumar, S. Gil, D. Katabi, and D. Rus. Accurate indoor localization with zero start-up cost. In Proceedings of ACM MobiCom, 2014.   
[13] P. Lazik and A. Rowe. Indoor pseudo-ranging of mobile devices using ultrasonic chirps. In Proceedings of the ACM SenSys, 2012.   
[14] Q. Lin, Z. An, and L. Yang. Rebooting ultrasonic positioning systems for ultrasound-incapable smart devices. In Proceedings of ACM MOBICOM, 2019.   
[15] K. Liu, X. Liu, and X. Li. Acoustic ranging and communication via microphone channel. In Proceeding of IEEE GLOBECOM, 2012.   
[16] K. Liu, X. Liu, and X. Li. Guoguo: Enabling fine-grained smartphone localization via acoustic anchors. IEEE Transactions on Mobile Computing, 15(5):1144–1156, 2016.

[17] K. Liu, X. Liu, L. Xie, and X. Li. Towards accurate acoustic localization on a smartphone. In Proceedings of IEEE INFOCOM, 2013.   
[18] C. V. Lopes, A. Haghighat, A. Mandal, T. Givargis, and P. Baldi. Localization of off-the-shelf mobile devices using audible sound: Architectures, protocols and performance assessment. ACM SIG-MOBILE Mob. Comput. Commun. Rev., 10(2):38–50, Apr. 2006.   
[19] W. Mao, J. He, and L. Qiu. Cat: High-precision acoustic motion tracking. In Proceedings of ACM MOBICOM, 2016.   
[20] M. Minami, Y. Fukuju, K. Hirasawa, S. Yokoyama, M. Mizumachi, H. Morikawa, and T. Aoyama. Dolphin: a practical approach for implementing a fully distributed indoor ultrasonic positioning system. In Proceedings of UbiComp, 2004.   
[21] R. Nandakumar, S. Gollakota, and N. Watson. Contactless sleep apnea detection on smartphones. In Proceedings of ACM MobiSys, 2015.   
[22] J. Paradiso, C. Abler, K. Hsiao, and M. Reynolds. magic carpet: physical sensing for immersive environments. In Proceedings of ACM CHI, 1997.   
[23] C. Peng, G. Shen, and Y. Zhang. Beepbeep: A high-accuracy acoustic-based system for ranging and localization using cots devices. ACM Transactions on Embedded Computing Systems (TECS), 11(1):4:1–4:29, Apr. 2012.   
[24] N. Priyantha, A. Chakraborty, and H. Balakrishnan. The cricket location-support system. In Proceedings of ACM MobiCom, 2000.   
[25] J. Qiu, D. Chu, X. Meng, and T. Moscibroda. On the feasibility of real-time phone-to-phone 3d localization. In Proceedings of ACM SenSys, 2011.   
[26] Q. Song, C. Gu, and R. Tan. Deep room recognition using inaudible echos. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., 2(3):135:1–135:28, Sept. 2018.   
[27] L. Sun, S. Sen, D. Koutsonikolas, and K.-H. Kim. Widraw: Enabling hands-free drawing in the air on commodity wifi devices. In Proceedings of ACM MobiCom, 2015.   
[28] S. Tarzia, R. Dick, P. Dinda, and G. Memik. Sonar-based measurement of user presence and attention. In Proceedings of ACM UbiComp, 2009.   
[29] D. Vasisht, S. Kumar, and D. Katabi. Decimeter-level localization with a single wifi access point. In Proceeding of USENIX NSDI, pages 165–178, 2016.   
[30] R. Wand, A. Hopper, V. Falcao, and J. Gibbons. The active badage location system. ACM Transactions on Information Systems, 10(1):91– 102, 1997.   
[31] A. Wang and S. Gollakota. Millisonic: Pushing the limits of acoustic motion tracking. In Proceedings of ACM CHI, 2019.   
[32] J. Wang, D. Vasisht, and D. Katabi. Rf-idraw: Virtual touch screen in the air using rf signals. In Proceedings of ACM SIGCOMM, 2014.   
[33] W. Wang, A. X. Liu, and K. Sun. Device-free gesture tracking using acoustic signals. In Proceedings of ACM MOBICOM, 2016.   
[34] T. Wei and X. Zhang. mtrack: High-precision passive tracking using millimeter wave radios. In Proceedings of ACM MobiCom, 2015.   
[35] J. Xiong and K. Jamieson. Arraytrack: a fine-grained indoor location system. In Proceedings of USENIX NSDI, pages 71–84, 2013.   
[36] J. Xiong, K. Sundaresan, and K. Jamieson. Tonetrack: Leveraging frequency-agile radios for time-based indoor wireless localization. In Proceedings of ACM MobiCom, pages 537–549. ACM, 2015.   
[37] S. Yun, Y.-C. Chen, and L. Qiu. Turning a mobile device into a mouse in the air. In Proceedings of ACM MobiSys, 2015.   
[38] M. Zhang, P. Yang, C. Tian, L. Shi, S. Tang, and F. Xiao. Soundwrite: Text input on surfaces through mobile acoustic sensing. In Proceedings of the 1st International Workshop on Experiences with the Design and Implementation of Smart Objects, SmartObjects@MobiCom 2015, Paris, France, September 7, 2015, pages 13–17, 2015.   
[39] Z. Zhang, D. Chu, X. Chen, and T. Moscibroda. Swordfight: Enabling a new class of phone-to-phone action games on commodity phones. In Proceedings of ACM MobiSys, 2012.   
[40] B. Zhou, M. Elbadry, R. Gao, and F. Ye. Battracker: High precision infrastructure-free mobile device tracking in indoor environments. In Proceedings of the 15th ACM Conference on Embedded Network Sensor Systems, SenSys ’17, pages 13:1–13:14, New York, NY, USA, 2017. ACM.   
[41] P. Zhou, Y. Zheng, and M. Li. How long to wait?: Predicting bus arrival time with mobile phone based participatory sensing. In Proceedings of ACM MobiSys, 2012.