# Swadloon: Direction Finding and Indoor Localization Using Acoustic Signal by Shaking Smartphones

Wenchao Huang, Yan Xiong, Xiang-Yang Li, Hao Lin, Xufei Mao, Panlong Yang, Yunhao Liu, Xingfu Wang

Abstract—We propose an accurate acoustic direction finding scheme, Swadloon, according to the arbitrary pattern of phone shaking in a rough horizontal plane. Swadloon leverages sensors of the smartphone without the requirement of any specialized devices. Our Swadloon design exploits a key observation: the relative displacement and velocity of the phone-shaking movement corresponds to the subtle phase and frequency shift of the Doppler effects experienced in the received acoustic signal by the phone. Swadloon tracks the displacement of smartphone relative to the acoustic direction with the resolution less than 1 millimeter. The direction is then obtained by combining the velocity from the displacement with the one from the inertial sensors. Major challenges in implementing Swadloon are to measure the displacement precisely and to estimate the shaking velocity accurately when the speed of phone-shaking is low and changes arbitrarily. We propose rigorous methods to address these challenges, and apply Swadloon to several case studies: Phoneto-Phone direction finding, indoor localization and tracking. Our extensive experiments show that the mean error of direction finding is around 2.1o within the range of 32m. For indoor localization, the 90- percentile errors are under 0.92m. For real-time tracking, the errors are within 0.4m for walks of 51m.

Index Terms—Direction Finding; Indoor Localization; Smartphone.

# 1 INTRODUCTION

Direction finding is attractive in mobile social networks nowadays for supporting various applications, e.g., friending, and sharing. Recent mobile apps have made similar functions, such as Facebook’s Friendshake [1] and Google Latitude [2]. However, they Wenchao Huang, Yan Xiong and Xingfu Wang are with School of Computer Science and Technology, University of Science and Technology of China. Email: {huangwc, yxiong,wangxfu}@ustc.edu.cn. Xingfu Wang is the corresponding author.

Xiang-Yang Li is with Department of Computer Science and Technology and TNLIST, Tsinghua University, and Department of Computer Science, Illinois Institute of Technology. Dr. Li is a visiting distinguished professor at School of Computer and Software, Nanjing University of Information Science & Technology, China. Email: xli@cs.iit.edu.

Hao Lin is with School of Internet of Things Engineering, Jiangnan University. Email: imlinhao@gmail.com.

Xufei Mao and Yunhao Liu are with Department of Software Engineering, and TNLIST, Tsinghua University. Email: {xufei.mao, yunhaoliu}@gmail.com.

Panlong Yang is with Institute of Communication Engineering, PLAUST. Email: panlongyang@gmail.com.

are based on GPS and cannot be applied to indoor environment. An accurate method of direction finding is by using antenna array [3], [4] in localization, but it requires specialized hardware and limits the availability to regular users. Several approaches of direction finding by smartphones have been proposed [5]–[7]. However, it remains a challenge for accurate direction finding by phone under long distance.

Precise indoor localization is also important for location based services. Those methods achieving high accuracy usually require special hardware not readily available on smartphones [8], or infrastructures expensive to deploy [9]. Pure WiFi-based localization can achieve reasonable accuracy (e.g., 3∼4m), but there always exist large errors (e.g., 6∼8m) unacceptable for many scenarios [10]. Though there have been many proposals for improving the accuracy of WiFi based localization (e.g., with 80-percentile errors about 1m [10]) by exploiting additional signals, low-cost precise indoor localization is still challenging.

We propose Swadloon, a Shake-and-Walk Acoustic Direction-finding and indoor LOcalizatiON scheme using smartphones. Suppose that there is an acoustic signal emitted from a speaker or a phone. Swadloon exploits the fact that shaking the smartphone or walking with the smartphone will cause Doppler effects on the acoustic signal received by the smartphone. Swadloon precisely measures the real-time phase and frequency shift of the Doppler effect, which corresponds to the relative displacement and velocity from the phone to the acoustic source respectively. Swadloon then obtains the accurate direction of the acoustic source by combining the relative velocity calculated from the Doppler shift with the one from the inertial sensors of the smartphone.

The main challenges of implementing Swadloon are noisy data collected from inertial sensors, and measurement of subtle frequency shift when the motion velocity of the phone is slow or fluctuates continuously. We propose several rigorous methods (discussed in detail in Section 4) in Swadloon to address these challenges, e.g., we use Phase Locked Loop (PLL) to precisely measure the phase and frequency shift.

We evaluate the performance of Swadloon in the case study of phone-to-phone direction finding, where the object phone of direction finding serves as an acoustic source, and the finder shakes his/her phone gently to produce the Doppler effect. We also explore the feasibility of applying Swadloon to real-time indoor localization, which uses a few anchoring nodes with known locations. The scheme does not rely on any fingerprints and is very easy to use: a user only needs to shake the phone for a short duration before walking and localization. These anchoring speakers will emit acoustic signals using non-audible frequency (typically around 20kHz). The smartphones play the role of receivers. As it is difficult for a smartphone to find an accurate North as base for absolute direction, our localization method does not exploit the absolute direction. Instead we use a simple “triangulation” method by exploring the accurate opening angle from phone to two anchoring speakers. It measures the direction to the source and its relative displacement for achieving precise localization and real-time tracking respectively. Anchor nodes will not perform any computation or communication. Thus, dummy speakers such as loudspeakers can serve as anchors.

Our extensive experimental results show that Swadloon supports high accuracy for both Phone-to-Phone direction finding and real-time indoor localization. In our testing of Swadloon, the finder only needs to shake the phone gently and in arbitrary patterns in a rough horizontal plane. For the phone-to-phone direction finding, the mean error of the measured angle is 2.10o within the range of 32m, and the errors are under 2.06o, 4.43o, 5.81o at 50%, 90%, 95% respectively, when the acoustic source faces towards to the phone. Since our acoustic direction finding achieves both long distance (about 32m) and high accuracy (around 2 degrees), it supports a variety of potential applications, such as direction-based advertising that recommends new goods in a shopping mall, or sharing virtual business card with surroundings in a big party, where the former application requires advertisement being broadcasted as long as possible to be detected by users, and the latter one requires accurate direction finding. For indoor localization, we deploy one acoustic source per 6 meters, which broadcasts signals at a predefined frequency. For static localization, Swadloon achieves 90-percentile accuracy of 0.92m, maximum error of 1.73m, and the mean error of 0.5m. For real-time indoor tracking, the error is always kept within 0.4m even when users walk for more than 50 meters.

The rest of the paper is organized as follows. We review related work in Section 2 and present technical preliminaries in Section 3. We present the design of Swadloon in Section 4, We report our extensive experimental results in Section 5. We conclude the paper in Section 6.

# 2 RELATED WORK

# 2.1 Direction Finding

Specialized Hardware: Former approaches requires special hardwares for achieving high accuracy, e.g., by using directional antenna [11]–[13] or antenna array [3], [4] to implement Angle of Arrival (AOA) [14] in localization. For example, by rotating the beam of its antenna, a receiver can pinpoint the direction of the AP as the direction that provides the highest received strength [11].

Non-specialized hardware: [5] effectively emulates the functionality of a directional antenna by rotating the phone around the user’s body, to locate outdoor APs. [7] leverages 4 microphones for calculating 3D position of each other by using the distance ranging method [15]. As the work is intended for high-speed, locational, phone-to-phone (HLPP) games, it does not show the result when two phones are in long distances. [16] calculates direction by head nodding or shaking using smart glasses. Other methods [17], [18] close to direction finding are to identify which target the user is pointing at when s/he moves mobile phone towards the target phone.

To the best of our knowledge, the approach closest to ours in direction finding is [6]. It estimates the direction and achieves the mean angular errors within 18o while ours is around 2o. This approach requires that the searching user generates Doppler Effects to all directions, e.g., the user stretches the arm while holding the searching device, and then swings it through 180 degrees. Correspondingly, as Swadloon tracks the displacement with the resolution under 1mm, Swadloon only requires that the user shakes the phone gently in an arbitrary path.

# 2.2 Indoor Localization and Tracking

In indoor localization, to avoid the use of specialpurpose infrastructure, e.g., [19]–[23], wireless localization, which only leverages an existing infrastructure instead of special-purpose hardware, has attracts many research efforts, e.g., [10], [24]–[33]. However, it is found [10] that pure wireless localization can achieve reasonable accuracy (e.g., 3 ∼ 4m), but there always exist large errors $( e . g . , \ G \sim 8 m )$ unacceptable for many scenarios. ByteLight [34] claims to be able to provide low-price infrastructure for localization using ceiling-embedded LEDs which send out Morse Code-like signals to be detected by the smartphone’s camera. Our case study provides another choice for precise indoor localization, which only needs ceilingembedded low-price speakers instead.

Leveraging acoustic wave by phone: The methods of leveraging the acoustic wave in smartphone applications have been well addressed. Most of them are leveraging the low speed of the acoustic wave for ranging, such as the mechanism of TOA [15] and TDOA [35], [36]. BeepBeep [15] detects the distance between two smartphones with high accuracy. It has been used by many other schemes, such as HLPP games [7], [37], device pairing [17] and indoor localization [10], [38]. Instead of precise ranging, [39], [40] use acoustic background spectrum for coarse-grained indoor localization.

In this work, we leverage Doppler effects of acoustic waves (i.e., measuring the precise relative displacement and velocity of phone) to design Swadloon. Swadloon is precise enough to be another basic tool of AOA, while it only requires off-the-shelf speakers. Furthermore, Swadloon supports arbitrary number of users and the phones of users do not need to send any signals to get the location, which avoids the signal interference when the number of users increases.

Leveraging the Doppler effects: Doppler effects have been leveraged in wide areas, such as radar, satellite communication, medical imaging and blood flow measurement, etc. There are also localization approaches leveraging the Doppler shift of wireless signals in localization [41] and tracking [42] in wireless sensor networks. But it also needs special hardware not available for smartphone users. Meanwhile, by using the phase shift, Swadloon easily implements precise tracking without complicated algorithms compared with [42] which uses frequency shift.

Leveraging the inertial sensors: Inertial sensors have been used for pedestrian dead-reckoning [43] in indoor localization. The challenge is that it suffers from a large accumulation of errors. The complementary approaches to this problem are proposed in [25], [26], [44]. Swadloon uses the accelerometer and gyroscope to obtain the direction of the acoustic source.

# 3 PRELIMINARY APPROACHES

# 3.1 Mapping from Doppler Effects to Motion

Our scheme is based on the relationship between Doppler effects and the relative motion from the phone to the acoustic source, when the phone moves and causes Doppler effects on the received acoustic waves. Suppose the acoustic source is emitting the sinusoidal signal at the frequency of $f _ { a , }$ , the observed frequency $f _ { r } \ [ 4 5 ]$ is $\begin{array} { r } { f _ { r } = \frac { \dot { v } _ { a } + v } { v _ { a } + v _ { s } } \dot { f } _ { a } } \end{array}$ . Here v is the velocity of the va+vs receiver; positive if the receiver is moving towards the source and negative in the opposite position. $v _ { s }$ is the velocity of the source and $v _ { a }$ is the traveling speed of the acoustic wave.

In this paper, we only consider the circumstance that the acoustic source is motionless or the velocity of the phone is far greater than the source, $i . e . , v \gg v _ { s } .$ As typically $v _ { a } \gg v _ { s }$ , we simplify the computing of the frequency shift f as follows:

$$
f = f _ {r} - f _ {a} = \frac {v - v _ {s}}{v _ {a} + v _ {s}} f _ {a} \approx \frac {v}{v _ {a} + v _ {s}} f _ {a} \approx \frac {f _ {a}}{v _ {a}} v \tag {1}
$$

We also assume the acoustic source sends the consecutive sinusoidal acoustic wave at constant frequency $f _ { a } .$ . To derive the relative displacement from Doppler effect, we assume that the received signal has the form:

$$
r (t) = A (t) \cos (2 \pi f _ {a} t + \phi (t)) + \sigma (t) \tag {2}
$$

where $A ( t )$ is the amplitude which changes continuously, $\phi ( t )$ is the phase which is affected by the Doppler effect and $\sigma ( t )$ is the noise. Assuming φ(t) is a continutime t is $f _ { r }$ $\begin{array} { r } { f _ { r } ( t ) = \frac { 1 } { 2 \pi } \frac { d \left( 2 \pi f _ { a } t + \phi ( t ) \right) } { d t } = f _ { a } + \frac { \hat { 1 } } { 2 \pi } \frac { d \phi ( t ) } { d t } } \end{array}$ 1 dφ(t) . From Eq. (1), the frequency shift $f$ at time t is

$$
f (t) = \frac {1}{2 \pi} \frac {d \phi (t)}{d t} \tag {3}
$$

From Eq. (1)(3), we get the velocity and displacement relative to the acoustic source:

$$
\left\{ \begin{array}{l} v (t) = \frac {v _ {a}}{2 \pi f _ {a}} \frac {d \phi (t)}{d t} \\ s (t) = \frac {v _ {a}}{2 \pi f _ {a}} \phi (t) - \frac {v _ {a}}{2 \pi f _ {a}} \phi (0) \end{array} \right. \tag {4}
$$

where $s ( t )$ is the relative displacement from the phone to the acoustic source. Specifically, $s ( t ) = L ( 0 ) { \stackrel { - } { - } } L ( t ) .$ where $L ( t )$ is the distance between the phone and the source at time t. In Section 4.3, we further show how to calculate φ(t) in order to obtain v(t) and s(t).

# 3.2 Basic Direction-Finding Using Doppler Effect for Simple Motion

We make a simple case of phone-to-phone direction finding to illustrate the intuition in designing Swadloon. Then we show the practical limitations of the simple case and implementation challenges. In latter sections, we propose our method on a more complicated case to address these issues.

Assume that the phone and the acoustic source are at the same height and the mobile phone starts moving in north and in a path of rectangle with the constant velocity $u _ { 1 } , u _ { 2 } , u _ { 3 } , u _ { 4 }$ in each direction, shown in Figure 1a. So, frequency shifts are generated, where $f _ { i }$ corresponding to $u _ { i } .$ . If the velocities and the frequency shifts are obtained, from Eq. (1), we can calculate the acoustic direction α in the following equations:

$$
\left\{ \begin{array}{l l} u _ {1} \sin \alpha = \frac {v _ {a}}{f _ {a}} f _ {1}; & u _ {2} \cos \alpha = \frac {v _ {a}}{f _ {a}} f _ {2}; \\ - u _ {3} \sin \alpha = \frac {v _ {a}}{f _ {a}} f _ {3}; & - u _ {4} \cos \alpha = \frac {v _ {a}}{f _ {a}} f _ {4} \end{array} \right. \tag {5}
$$

Intuitively from Eq. (5), if $u _ { 1 } ~ = ~ u _ { 2 } ~ = ~ u _ { 3 } ~ = ~ u _ { 4 } ,$ $f _ { 2 } > f _ { 1 } > 0 > f _ { 3 } > f _ { 4 } ,$ , which indicates that the $0 < \alpha < 4 5 ^ { o }$ . Formally, only two equations are needed to calculate $\alpha$ if the velocity in one equation is not parallel to the other. The additional equations can enhance the accuracy by using maximum likelihood estimation.

Note that α is changing while the phone is moving, so it will cause errors on obtaining α. However, it won’t affect much on calculating the direction. In Figure 1b, if the initial distance from the phone to acoustic source is L and the maximum moving range of the phone is $d ,$ the maximum angle error is $\alpha _ { e } =$ arcsin $\frac { \dot { d } } { L } .$ . As the phone moves gently, we assume that $d$ is 10cm at maximum. The maximum errors are $5 . 7 ^ { o } ,$ $1 . 1 5 ^ { o } , \ 0 . 5 7 ^ { o } , \ 0 . 1 9 ^ { o }$ at $L \ = \ 1 , 5 , 1 0 , 3 0 m$ respectively, $i . e . ,$ the errors get smaller when the distance becomes longer. Note that the user can also shake phone with wider range that the angle error caused by phone movement is ignorable when $L \gg d .$

![](images/b24a525603dc2b7e4f22f3716b45073872a0fa2e65bbdf95862e81ca90d57c14.jpg)



(a) Phone movement.

![](images/8fb821c22ec6cb915d76a872d3cd1cfd5356496d27beaaf36613429a2f1b55dc.jpg)



(b) Error from motion.

![](images/56623cc0df7e1d443aa7261fdcfb45a058a8041aed8f8119cbdbd9936f1d0a9f.jpg)



(c) Velocity at north axis.

![](images/deaaec8597b3e5e96080e8921364ee23b8fc9996cbb55f76331d62efc9ec3c0d.jpg)



(d) FFT of received signal.   
Fig. 1: A simple case of calculating the direction α. (a) The phone starts moving north and draw a rectangle. (b) The velocity calculated from the inertial sensors. (c) FFT on the received acoustic signal.

Moreover, if the phone calculates the position of acoustic source by not only the direction α according to Swadloon but also the distance L according to other techniques such as BeepBeep [15] while the measured $L$ is accurate, the distance $d _ { e }$ from the calculated position to the actual position is $\begin{array} { r l } { d _ { e } } & { { } = } \end{array}$ 2L sin $\begin{array} { r } { \frac { \alpha _ { e } } { 2 } = \overline { { 2 } } L \sin \frac { \arcsin ( d / L ) } { 2 } } \end{array}$ . When $d \ll L , e . g . , 1 0 d \leq$ $L ,$ arcsin $. ( d / L ) ~ \approx ~ ( d / \stackrel { \sim } { L } )$ and sin $( d / 2 L ) ~ \approx ~ d / 2 L$ . So we simplify $d _ { e }$ as $d _ { e }$ ≈ d. Then the maximum error on computed location caused by shaking is close to the shaking distance $d ,$ which is tolerable in direction finding.

However, there are several problems on applying this simple approach. First, the accurate velocity of the phone is hard to be obtained by using the inertial sensors. Though it can be calculated by the accelerometer and other sensors if given the initial velocity of the phone, the errors of the acceleration will be accumulated on its integration, i.e., the calculated velocity. For instance in Figure 1a, the velocity is zero at the end of moving while the calculated one is $- 0 . 7 7 m / s$ in Figure 1c. Second, the mobile phone and the acoustic source may not be of the same height. In this case, the calculated f is lowered and the equations in Eq. (5) are not right. Third, it would be hard and exhausting to draw the regular rectangle for the phone users. Fourth, the velocity of the phone v cannot be constant in each direction. So we need a more general solution in cases of different heights and arbitrary motion patterns.

An important practical challenge is that spectrum analysis, such as Fast Fourier Transform (FFT), is not efficient in calculating frequency shift $f ,$ when the user shakes the phone gently, $e . g .$ , the peak value of the phone speed is $0 . 2 m / s \sim 0 . 4 m / s$ in our experiment in Figure 7. Specifically, FFT cannot measure the precise value of f if v changes quickly due to the timefrequency resolution problem [46]. That is, for any signal, the time duration $\Delta T$ and the spectral bandwidth $\Delta F$ are related by $\Delta F \Delta T \geq 1$ . For example, if the time resolution is $\dot { \Delta } T = 8 1 9 2 / 4 4 1 0 0 \mathrm { H z } \mathrm { = } 0 . \dot { 1 } 9 s _ { i }$ the frequency resolution $\Delta F \ge 1 / \Delta T = 5 . 3 8 \mathrm { H z }$ . In this case, the frequency resolution is far not enough in our experiment where the peak value of frequency shift is around 11.8Hz∼23.6Hz. Furthermore, it is still challenging when the phone speed is high, $e . g .$ , the maximum speed of a user’s hand is $2 m / s \ [ 3 7 ]$ . In our simple case, the maximum speed also reaches $2 \mathrm { m } / \mathrm { s }$ as shown in Figure 1c, where the maximum shift is 111.8Hz theoretically, which seems sufficient for direction finding. However, in Figure 1d we find that the maximum frequency shift only reaches about 70Hz. The main reason is that the direction α is about $4 5 ^ { o }$ and the maximum shift is reduced to 111.8 cos $4 5 ^ { o } =$ 79Hz. Meanwhile, most of the time, the frequency shift is far less than 70Hz. Note that, Spartacus [18] improves the resolution of FFT but also requires peak velocity at $2 \sim 6 m / s$ and achieves angular resolution with 10o; Swadloon lose the limitation that it also supports slow peak velocity $( 0 . 2 \ \sim \ 0 . 4 m / s )$ and higher angular resolution (mean error $\simeq 2 ^ { o } )$ . Hence, more accurate frequency measurement is preferred for calculating accurate direction.

Besides the challenge of calculating the frequency shift $f ( t )$ for direction finding, the further problem is calculating the phase shift $\phi ( t )$ , from which f (t) can be obtained by Eq. (3). We also show that the real-time indoor tracking can be implemented by using φ(t) in Section 5.2.2.

# 4 DESIGN OF SWADLOON

We study the more complicated case that the user shakes the phone or walks in an arbitrary path. We show the design of Swadloon in Figure 2. The phone gathers samples from the microphone and inertial sensors. The data are processed in real time to maximize the utilization of the CPU. The phone dynamically updates the direction of the source according to the previously calculated samples.

In Figure 2, The noise $\sigma ( t )$ and variational amplitude $A ( t )$ in Eq. (2) is eliminated by BPF and AGC respectively. The phase φ and frequency $f ,$ which corresponds to the relative displacement and velocity respectively, are then obtained by PLL. Swadloon further combines the velocity from the acoustic and inertial sensor samples to get the source direction α by Linear Regression. The phone returns the value of α and $\phi$ in real time for direction finding, indoor localization or tracking. We describe each component of the design as follows.

![](images/5335d8c9170db6f575ab4f10c6dbebf0fd02388bc5b6b863c00f1fa043a880a5.jpg)



Fig. 2: Implementation of Swadloon.

# 4.1 Band Pass Filter (BPF)

To get rid of the interference of other acoustic waves, we assume the phones of different users send acoustic waves in different frequency bands. Hence, in our implementation, the acoustic sample first walks through the Band Pass Filter (BPF) such that only the waves at the exact frequency pass through BPF. Interference by other acoustic sources and low frequency noises that human can hear are both eliminated.

Note that the type of BPF should be seriously chosen. All frequency components of a signal are delayed when passed through BPF. As the frequency is changing in Doppler effect and we need to get the precise phase, the delay at each frequency components must be constant, such that the different frequency component will not suffer distortion, which is known as the linear phase property. As a result, we choose equiripple FIR filter, which satisfies the linear phase property.

Meanwhile, the bandwidth should be wide enough to get the total signal. Normally, the maximum speed of shaking the phone is less than 2m/s. Thus, if the frequency of acoustic signal is $f _ { a } \ = \ 1 9 0 0 0 \mathrm { H z } ,$ the maximum frequency shift $f _ { m a x } \ = \ 1 1 1 . 8 \mathrm { H z } .$ So, the minimum pass band of the filter is 223.6Hz. For avoiding the interference by other acoustic sources, there should not be multiple signals that pass through the same BPF. Besides, acoustic bandwidth that almost all the smartphones support is limited to maximum of 22050Hz (i.e., sample rates of 44100Hz) and we find that the lowest frequency that human can hardly hear is about 17000Hz in our experiment. Thus, the maximum number of acoustic sources that can sound simultaneously in a small area (with radius about 30m) and be successfully detected is limited to $( 2 2 0 5 0 - 1 7 0 0 0 ) / 2 2 3 . 6 \approx 2 3$ . However, this is not a challenge for Swadloon as we show that we only need a small number (less than 10) of acoustic sources in a small area for high accuracy. Though there are possible ways to allow more simultaneous acoustic waves such as dividing the signal into different time slots, like TDMA in shared medium network, it is beyond the scope of this paper.

# 4.2 Automatic Gain Control (AGC)

We adjust the filtered data by Automatic Gain Control (AGC) such that the amplitude of the acoustic signal $A ( t )$ in Eq. (2) is replaced by another one that is close to constant. The purpose is to successfully estimate the phase $\phi ( t )$ by using PLL in Section 4.3. We adopt the design of AGC from [47]. Suppose $T _ { s }$ is the sampling period of the received signal and k is the step count of sampling, then $t ~ = ~ k T _ { s }$ . The main idea is for the input $r _ { b } [ k ]$ from BPF, we estimate the amplitude $A [ k ]$ in Eq. (2) by updating $A _ { 1 } [ k ]$ with the equation:

$$
\log (A _ {1} [ k ]) = (1 - A _ {\alpha}) \log (A _ {1} [ k - 1 ]) + A _ {\alpha} \log (1 / A _ {r} [ k - 1 ])
$$

Here $A _ { \alpha }$ represents the sensitivity for adjusting $A _ { 1 } [ k ]$ . $A _ { r } [ k ]$ represents the coarse-grained estimation of $A [ k ]$ .

Since $\overline { { | r _ { b } | } } \simeq { \frac { 2 } { \pi } } A$ and the calculated $\overline { { \left| r _ { b } \right| } }$ is stable when averaging consecutive 11 samples, in our implementation, $\begin{array} { r } { \bar { A } _ { r } [ \bar { k } ] = \frac { \pi } { 1 1 * 2 } \sum _ { i = k - 1 0 } ^ { k } | r _ { b } [ i ] | } \end{array}$ π∗ Pki=k−10 |rb[i]| and Aα = 0.9. $A _ { \alpha } = 0 . 9$ Then, for the received filter data $r _ { b } [ k ]$ , the output

$$
r _ {c} [ k ] = A _ {1} [ k ] r _ {b} [ k ]
$$

For the amplitude of $r _ { c } [ k ]$ is close to constant by AGC, if $A _ { 1 } [ k \hat { \big | ^ { - } } = A _ { 1 } [ k - 1 ] , \ \bar { A } _ { 1 } [ k ] A _ { r } [ k - 1 ] = 1$ . Thus, the amplitude of $r _ { c } [ k ]$ is close to 1. Hence, we get $r _ { c } ( t )$ ≈ cos $( 2 \pi f _ { a } t + \phi ( t ) )$ , where $\sigma ( t )$ and A(t) in Eq. (2) is approximately eliminated by BPF and AGC respectively.

# 4.3 Tracking Subtle Displacement by Phase Locked Loop

According to Eq. (4), we use Phase Locked Loops (PLL) to calculate the phase φ(t), in order to get the precise relative displacement s(t) and velocity $v ( t )$ of the phone. PLL can be thought as a device that tracks the phase and frequency of a sinusoid [47]. In software implementation, we draw the idea from [48]. To get the precise φ(t), we update an adaptive estimation of $\phi ( t )$ in real time, denoted as ${ \theta } ( \bar { t } )$ in order that $\theta ( t ) \approx \phi ( t )$ . To make θ converge to φ after enough iterations, we define the corresponding function $J _ { P L L } ( \theta )$ such that $J _ { P L L }$ converges to its maximum at the same time. Specifically, $\theta ( t )$ is updated in the iterations as:

$$
\theta^ {\prime} = \theta + \frac {d J _ {P L L}}{d \theta} \tag {6}
$$

As a result, $J _ { P L L }$ should satisfy that

$$
\max (J _ {P L L} (\theta)) = J _ {P L L} (\phi) \tag {7}
$$

In Swadloon, we choose $J _ { P L L }$ as follows:

$$
\begin{array}{l} J _ {P L L} (\theta) = \operatorname{LPF} \left\{r _ {c} (t) \cos \left(2 \pi f _ {a} t + \theta (t)\right) \right\} \\ \approx \frac {1}{2} \mathrm{LPF} \{\cos (\phi (t) - \theta (t)) \} \\ \end{array}
$$

Here, LPF is the Low Pass Filter which excludes the high frequency component in the above approximation. Hence, $J _ { P L L }$ satisfies Eq. (7).

Next, we need to change the continuous estimation process of Eq. (6) to the discrete one. Suppose $T _ { s }$ is the sampling period of the received signal and k is the step count of sampling, then $t = k T _ { s } ^ { \phantom { \dagger } }$ . Assuming a small step size, the derivation in Eq. (6) with respect to θ at $k T _ { s }$ can be approximated1:

$$
\begin{array}{l} \frac {d J _ {P L L}}{d \theta} \approx \mathrm{LPF} \{\frac {d [ r _ {c} [ k ] \cos (2 \pi f _ {a} k T _ {s} + \theta)) ]}{d \theta} \} \Bigg | _ {\theta = \theta [ k ]} \\ = - \operatorname{LPF} \left\{r _ {c} [ k ] \sin \left(2 \pi f _ {a} k T _ {s} + \theta [ k ]\right) \right\} \\ \end{array}
$$

As a result, the estimating of $\theta ( t )$ is shown as follows:

$$
\theta [ k + 1 ] = \theta [ k ] - \mu \mathrm{LPF} \left\{r _ {c} [ k ] \sin \left(2 \pi f _ {a} k T _ {s} + \theta [ k ]\right) \right\} \tag {8}
$$

where $\theta [ k ] = \theta ( k T _ { s } )$ and $\mu$ is a small positive value. Hence, $\phi [ k ] \approx \theta [ k ]$ after enough iterations. According to Eq. (4), if the max velocity of the phone is $v _ { m a x } =$ $2 m / \bar { s } , f _ { s } = 4 4 1 0 0 \mathrm { H z }$ and $f _ { a } \stackrel { \cdot } { = } 1 9 0 0 0 \bar { \mathrm { H z } } ,$ the max offset per sample $\begin{array} { r } { | \Delta \phi _ { m a x } | = \frac { 2 \pi f _ { a } } { v _ { a } f _ { s } } v _ { m a x } = 0 . 0 1 6 } \end{array}$ . Besides,

$$
r _ {c} [ k ] \sin (2 \pi f _ {a} k T _ {s} + \theta [ k ]) \approx \frac {1}{2} \sin (4 \pi f _ {a} k T _ {s} + 2 \theta [ k ]) \leq \frac {1}{2}
$$

Thus, $\mu > 0 . 0 3$ in Eq. (8), otherwise, the transition rate of $\theta [ k ]$ cannot catch up with the real phase. Furthermore, as $\begin{array} { r } { \frac { 1 } { 2 } \sin ( 4 \pi f _ { a } k \dot { T _ { s } } + 2 \theta [ k ] ) } \end{array}$ cannot always be $1 / 2$ , µ needs to be much more than 0.03 to let $\theta [ k ]$ converge to $\phi [ k ]$ . However, when $\mu$ is bigger, the calculated phase is more sensitive to noises, and cannot be precise either. Hence, there is a tradeoff on choosing the $\mu .$ Specifically, as moving speed of the phone is not always be $2 m / s ,$ , we can choose a smaller µ such that Swadloon is more robust to noises. In the implementation, we choose $\mu = 0 . 0 3$ .

As the relative displacement is proportional to the phase shift by PLL, we estimate the precision of calculated displacement by Eq. (4). If the phase shift is 1 rad and the frequency of the source is 19000Hz, the relative displacement is 2.8mm. We simply measure the phase when the phone is motionless, and find that the phase is oscillating around a constant central value, $i . e .$ , the real phase, and the amplitude of the oscillation is 0.005 rad when $\mu = 0 . 0 3$ . We also let the phone move in an specific path towards the acoustic source with length of $3 0 c m ,$ and measure the phase shift from the starting point to the end point. The standard deviation is 0.09 rad, which correpsonds the displacement of 0.25mm. Hence, the measurement resolution of the corresponding displacement is less than 1mm. In section $5 ,$ We further evaluate Swadloon which depends on accuracy of PLL, to infer the robustness of PLL against multipath effects, noisy environment, etc.

# 4.4 Getting Direction by Linear Regression (LR)

Assuming the direction vector of the acoustic source relative to the phone is $\vec { \lambda } = ( \lambda _ { x } , \lambda _ { y } , \lambda _ { z } )$ and velocity vector of the phone is $\vec { \boldsymbol { u } } = ( v _ { x } , v _ { y } , v _ { z } )$ , then $\vec { u } \cdot \stackrel {  } { \lambda } \stackrel { \cdot } { = }$ $\textstyle { \frac { v _ { a } } { f _ { a } } } f$ according to Eq. (1). For the obtained array $\vec { \boldsymbol { u } } [ \boldsymbol { k } ]$ and $f [ k ] .$ , they satisfy the following equations

$$
\lambda_ {x} v _ {x} [ k ] + \lambda_ {y} v _ {y} [ k ] + \lambda_ {z} v _ {z} [ k ] = \frac {v _ {a}}{f _ {a}} \cdot f [ k ], \quad \forall k \tag {9}
$$

Hence, the 3D direction $\vec { \lambda }$ can be obtained by solving these equations using linear regression, where $f [ k ]$ can be calculated by Eq. (3), Eq. (8). Ideally, if $u [ k ]$ is obtained from inertial sensors and there are no errors of $u [ k ]$ , there are 3 unknowns $\lambda _ { x } , \lambda _ { y } , \lambda _ { z }$ in the equation set. Moreover, using this we can calculate the direction when the phone moves in arbitrary paths, because different motion patterns of the phone merely cause different array $\vec { \mathcal { U } } [ k ]$ and $f [ k ]$ . We can also translate 3D direction $\overrightarrow { \lambda }$ to 2D direction α as follows:

$$
\alpha = \left\{ \begin{array}{l l} \arcsin \frac {\lambda_ {y}}{\sqrt {\lambda_ {x} ^ {2} + \lambda_ {y} ^ {2}}} & \lambda_ {x} \geq 0 \\ \pi + \arcsin \frac {\lambda_ {y}}{\sqrt {\lambda_ {x} ^ {2} + \lambda_ {y} ^ {2}}} & \lambda_ {x} <   0 \end{array} \right. \tag {10}
$$

We now address the non-ideal circumstance with noisy sensor data, $i . e . ,$ to minimize the error of velocity which is derived from the calculated acceleration in WCS. In phone-to-phone direction finding and indoor localization, we only need the 2D direction α rather than the 3D direction $\left( \lambda _ { x } , \lambda _ { y } , \lambda _ { z } \right)$ . Thus, $\lambda _ { z }$ is not needed. From Eq. (9), if $\lambda _ { z } v _ { z } [ k ] \approx 0 , i . e . ,$ , the phone moves in a horizontal plane or the two phones are at the same height approximately, we can calculate the direction by the following equation to eliminate the error of $v _ { z } { \mathrm { : } }$

$$
\lambda_ {x} v _ {x} [ k ] + \lambda_ {y} v _ {y} [ k ] = \frac {v _ {a}}{f _ {a}} \cdot f [ k ] \tag {11}
$$

Suppose $\hat { a } _ { x } [ i ] = a _ { x } [ i ] + \sigma _ { x } [ i ]$ where $\hat { a } _ { x } [ i ] , a _ { x } [ i ] , \sigma _ { x } [ i ]$ is the real acceleration, the calculated acceleration, the error of the calculation on the acceleration of the ith sample respectively. We can derive $v _ { x }$ from

$$
v _ {x} [ k ] = v _ {x} [ 0 ] + \sum_ {i = 0} ^ {k - 1} T [ i ] a _ {x} [ i ] + \sum_ {i = 0} ^ {k - 1} T [ i ] \sigma_ {x} [ i ]
$$

where $T [ i ]$ is time interval from $a _ { x } [ i ]$ to $a _ { x } [ i + 1 ]$ .

The error $\sigma _ { x }$ is related the natural quality of the inertial sensors and challenging to be measured. In this paper, we simply assume $e _ { x }$ $\begin{array} { r } { \sum _ { i = 0 } ^ { k - 1 } T [ i ] \sigma _ { x } [ \bar { i } ] = e _ { x } t [ k ] } \end{array}$ at a short period. Suppose i=0 ilarly, we also assume theat a short period. $\begin{array} { r } { t [ k ] = \sum _ { i = 0 } ^ { k - 1 } T [ i ] } \end{array}$ $\sigma _ { x }$ equals to a constant , we get $a _ { y }$ $e _ { y }$

We also consider the problem that there is clock drift between acoustic source and smartphone. For example, in our experiment the actual frequency of received signal is 19000.13Hz when the one of sent signal is 19000Hz. Denote the frequency shift caused by clock drift as $f _ { d , }$ , the actual frequency of received signal is $f _ { r } ^ { \prime } = f _ { r } + f _ { d }$ . Since the frequency shift caused by Doppler effects $f \ \ll \ f _ { r } ,$ it can be inferred that $f _ { d }$ is close to constant when f changes. Hence, the measured frequency shift $f ^ { \prime } = f + f _ { d }$ where $f _ { d }$ is close to constant.

As a result, from Eq. (13)(10)(11), we could calculate the 2D direction by linear regression from the following equation set which has 4 unknowns $( \lambda _ { x } , \lambda _ { y } , \lambda _ { 0 } ,$ $\lambda _ { 1 } )$

$$
\left( \begin{array}{c c c c} w _ {x} [ 0 ] & w _ {y} [ 0 ] & 1 & t [ 0 ] \\ w _ {x} [ 1 ] & w _ {y} [ 1 ] & 1 & t [ 1 ] \\ \dots & \dots & \dots & \dots \\ w _ {x} [ n ] & w _ {y} [ n ] & 1 & t [ n ] \end{array} \right) \left( \begin{array}{l} \lambda_ {x} \\ \lambda_ {y} \\ \lambda_ {0} \\ \lambda_ {1} \end{array} \right) = \frac {v _ {a}}{f _ {a}}. \left( \begin{array}{l} f ^ {\prime} [ 0 ] \\ f ^ {\prime} [ 1 ] \\ \dots \\ f ^ {\prime} [ n ] \end{array} \right) \tag {12}
$$

Here, $\begin{array} { r } { w _ { x } [ k ] = \sum _ { i = 0 } ^ { k - 1 } T [ i ] a _ { x } [ i ] , w _ { y } [ k ] = \sum _ { i = 0 } ^ { k - 1 } T [ i ] a _ { y } [ i ] , } \end{array}$ $\begin{array} { r } { \lambda _ { 0 } = \lambda _ { x } v _ { x } [ 0 ] + \lambda _ { y } v _ { y } [ 0 ] + \frac { v _ { a } } { f _ { a } } f _ { d } } \end{array}$ and $\lambda _ { 1 } = \lambda _ { x } e _ { x } + \lambda _ { y } e _ { y } .$ Note that, we allow that $v _ { x } [ 0 ] ~ \neq ~ 0$ and $v _ { y } [ 0 ] ~ \neq ~ 0$ in our solution, which means we don’t require the phone to be motionless before shaking the phone and calculating the direction. Similarly, we don’t need the value of $\breve { f } _ { d } . \ v _ { x } [ 0 ] , \ v _ { y } [ 0 ]$ and $f _ { d }$ are put together as an unknown $\lambda _ { 0 }$ in the equation.

# 4.5 Choosing the Direction in UCS for Evaluation

Vectors can be transformed between World’s Coordinate System (WCS) and User’s phone Coordinate System (UCS) by the rotation matrix. As the compass is not accurate, we obtain the initial rotation matrix of the phone by sensor fusion of the compass, gyroscope, and accelerometer, but update the dynamic rotation matrix by merely using the gyroscope.

Hence in our World Coordinate System (WCS), the Z axis is considered to be accurate, but the X axis may not point to east due to the error of the compass. Hence, the calculated direction α in WCS may not be the actual direction relative to the east. To evaluate the performance of our direction finding, we will evaluate the direction (denoted as the ground truth and the measured value as $\alpha _ { r }$ and $\alpha _ { r } ^ { \prime }$ respectively) of the acoustic source using the UCS of the phone that is placed horizontally such that its Z axis is same as the Z axis of WCS, as shown in Figure 3a. When phone is static, the value $\alpha _ { r }$ does not change. Thus, in Section 5.1, we measure $\alpha _ { r } ^ { \prime }$ to evaluate the accuracy of direction finding shown in Figure 3b.

Hence, suppose the phone is horizontal, we get value α by using Swadloon and the opening angle from X axis in UCS to the one in WCS (α0) by using the rotation matrix from UCS to WCS. αr is calculated by

$$
\alpha_ {r} = \pi / 2 - \alpha - \alpha_ {0} \tag {13}
$$

![](images/4a2a7cae2918b4c6e4c8c946edd58bbdfe4c7d2607d368a94d99f81eb12c88c7.jpg)



(a) WCS vs. UCS

![](images/379f90d32bccfbe0db70005528488afa476f109e8f2d2e07feef13c3d3f92394.jpg)



(b) Experiment setup   
Fig. 3: (a) WCS vs. UCS when the phone is horizontal. (b) Experiment of direction finding.

# 5 CASE STUDIES AND EVALUATIONS

# 5.1 Phone-to-phone Direction Finding

We use Google Nexus 7 and Motorola XT 910 as smartphone and acoustic source respectively. We mainly use Android API to implement Swadloon and the acoustic source. Specifically, the audio playing and recording is implemented by using class AudioTrack and AudioRecord respectively; the inertial sensor samples are gathered through the function on-SensorChanged(). The signal processing components, (i.e., BPF, AGC and PLL), are implemented by pure Java code without the requirement of any third-party libraries or hardware. On calculation direction, we adopt the implementation of linear regression (LR) in Michael Thomas Flanagan’s java scientific library. The audio sample rate is 44100Hz, and sample rate of the inertial sensors is 200Hz.

# 5.1.1 Experiment Design

The vertical view of the phone and acoustic source is shown in Figure 3b. The distance between the phone and the acoustic source is L. The orientation angle of the phone and acoustic source at the horizontal plane is $\alpha _ { r }$ and $\beta$ respectively. There are reference objects at places $\mathrm { A } , \mathrm { B } , \mathrm { C }$ which are utilized to align the phones. The place C is used to put new acoustic source for further experiment. Additionally, we assume the elevation angle of the acoustic source is $\gamma$ which is not shown in this 2D figure. The acoustic source is on the floor. The height of phone from the floor is about 40cm.

The main process of evaluating performance of direction finding is as follows: We vary $L , \alpha _ { r } , \beta , \gamma$ by moving the reference objects. We obtain the measured direction $\alpha _ { r } ^ { \prime }$ by shaking the phone, aligning the phone to the reference object, and reading the direction value from the phone. We measure $\alpha _ { r } ^ { \prime }$ 50 times for each configuration.

# 5.1.2 Empty Room with Single Acoustic Wave

We first conduct the experiment in a large empty room for examining the accuracy of direction finding when there is only single acoustic wave. The sound pressure in the room is −41 dBFS (about 30 dB SPL) measured by Nexus 7. The amplitude of the acoustic source at the distance of 1m is −20 dBFS.

![](images/f4bafa25ee9d2912118824fe25b40b01852937d1bff08c5d25ec71612a10910b.jpg)



(a) β,γ (degree)

![](images/fcff17c7b795439faa5cc16cf263326719c5b540f5bbc8ac39cae5ef272c79d4.jpg)



(b) β,γ (degree)

![](images/d80d7ffe960fc16baa29a389bb6ccd24921a18a21866523230caf34fa46f5e7f.jpg)



a(c) Pattern

![](images/341b5580d2ee0139a216c154a24a199c60cc02a55142ac4e5cba15aaa8e9a82b.jpg)

(d) Distance (m)   
![](images/524423db6974598e4902b06ecd3a56eb0f3a75b2792c7580624bd8e5ddfba244.jpg)



(e) Volume

![](images/c15043c634d59db87501dfe8c04b9ec61ee71d1ec4819d473c49327bc4f3ccaf.jpg)  
(f) L (m)   
Fig. 4: Mean and standard deviation of $\alpha _ { r }$ (degree) affected by (a) β and $\gamma$ when $L = 8 m$ (b) β and $\gamma$ when $L = 3 2 m$ (c) motion pattern (d) non-line of sight (e) man-made multipath (f) multipath from the wall.

Effect by L and $\alpha _ { r } .$ . The case we mostly care about is the performance when the distance L and the orientation of the phone $\alpha _ { r }$ is changing. Hence, we set $\beta = 0$ and $\gamma = 0 ,$ , and plot the standard deviations and cumulative distribution function (CDF) of the angular errors when L and $\alpha _ { r }$ are changed in Figure 5.

![](images/40027a29440b714e25e56ec665b4c5dd5786938dcd65aaebba58109d47fc2e56.jpg)



(a) Angle (degree)

![](images/916fdb7b319d51b290474d4783ff3280e5536a50864a52a3c9385991e4ccb47e.jpg)



(b) Angular Error (degree)   
Fig. 5: The result of direction finding in an empty room when $\beta = 0$ and $\gamma = 0$ .

The key observation is that the measurement is very accurate when $L \le 3 2 m$ . We examine the reason in Figure $6 ,$ which plots the calculated φ(t) on random samples with different L values. The calculated φ(t) is always smooth when $L \ \leq \ 2 4 m$ , while there are small noises when $L = 3 2 m$ and much bigger noises if $L = 4 0 m$ . Hence, the calculated related displacement and velocity become much less scrupulous when $L =$ 40m, which affects the calculation of direction. It is similar that most of the following cases mainly affect the calculated phase which finally affect the precision of direction finding.

![](images/de8000e128b6fd90637e9b95fb94638493f4513da4b43e321ba3be9052561de6.jpg)  
Fig. 6: The calculated phase φ(t).

In Figure 5a, when $L \le 3 2 m _ { i }$ , the mean error and standard deviation of the measurement is $2 . 1 0 ^ { o }$ and $2 . 6 6 ^ { o }$ . The angular errors are within 2.06o, 4.43o, 5.81o at 50%, 90%, 95% respectively. Though the errors become larger when $L = 4 0 m ,$ it is still tolerable. We also test angle errors when $L > 4 0 m$ , but it becomes much unstable as the signal is too weak. So we do not show the result of this case.

In Figure 5a, we also find when $\alpha _ { r }$ is chosen from $- 9 0 ^ { o }$ to $9 0 ^ { o }$ , it has little effect on precision. As the errors are so close for different $\alpha _ { r } ,$ we don’t show the CDF of different $\alpha _ { r }$ .

Effect by $\beta$ and $\gamma .$ We test the errors when the orientation of the acoustic source is not directly pointing to the phone. In this case, we set $\alpha _ { r } = 4 5 ^ { o }$ . In Figure 4a, 4b, we show the mean and standard deviation with different choices of $\beta , \gamma , L$ .

It shows an interesting result that when $\beta$ changes, the mean value changes more when L = 8m in Figure 4a than the one when $L = 3 2 m$ in Figure 4b. The main reason is that the acoustic source we choose is not omnidirectional, and the signal is much stronger right in front of the source. The signal reflected from the wall affects the result, which is so-called the multipath effect. When the phone is further from the source, the signal reflected from the wall becomes much weaker than the one directly from the acoustic source.

Another observation is that if the acoustic source turns up, such as $\gamma = 4 5 ^ { o } , 6 0 ^ { o } , 9 0 ^ { o } .$ , the mean value will not change a lot no matter L = 8m in Figure 4a or $L = 3 2 m$ in Figure 4b. That is, though there is multipath from the ceiling, it has little effect on the mean direction. We find a new phenomenon on multipath effect in latter experiment, which explains these observations here.

Motion Pattern. We also analyze the angular errors caused by the inertial sensors. As we claim that Swadloon supports arbitrary pattern of phone movement, we test errors caused by different motion patterns of the phone. In this case, we set $L = 3 2 m , \alpha _ { r } = 4 5 ^ { o } , \beta =$ $\gamma = 0 .$ . As we calculate the direction by Eq. (11) instead of Eq. (9) for better accuracy, it requires $\lambda _ { z } v _ { z } [ k ] \approx 0$ . Note that in most cases of phone-to-phone direction finding, $\lambda _ { z } ~ \approx ~ 0$ . Hence, we do not strictly require $v _ { z } [ k ] = 0$ that the experimenter shakes the phone in rough horizontal plane in the experiment.

![](images/b0905f364b646fbc20c2b1c4a16fd363c7da913c639654f0f2d8606cfee33ebc.jpg)  
Pattern A   
(arbitrary)

![](images/0fbe296a41daf1d0fd061b9309a568d19ce6462cb3f64e2c779b0af6d9af8456.jpg)  
Pattern B

![](images/0406ea9bd738a35dc9fcaff49aed645a7b9dd1ea47682fc799fa0ceb54374186.jpg)  
Pattern C

![](images/ab3ed37bcfb8d2643e2a1ce1ebe6417907260b8a8f6e3ade3eb71c55c2cce899.jpg)  
Pattern D   
Fig. 8: Tested shaking patterns of the phone.

The experimenter shakes the phone with arbitrary patterns in rough horizontal plane, e.g., pattern A in Figure 8. More specifically, we do not constrain the speed or the amplitude of the phone-shaking movement. Even the subtle movement is tested in the experiment. As the PLL measures the relative displacement with high resolution, the result is acceptable shown in Figure 4c: the standard deviation of the measurement is 4.96o.

![](images/fca237db7f9d0b0567ca670f59bff26f7f3803d0abf6c4864db79e5a23b6f9db.jpg)  
Fig. 7: Examples of direction finding which combines velocity from relative displacement ${ \frac { v _ { a } } { 2 \pi f _ { a } } } \phi ( t )$ with the one from inertial sensors $( w _ { x } ( t )$ and $w _ { y } ( t ) )$ .

We also show results of other regular patterns in Figure 8. The pattern B, C, D is the circle, the rectangle, and mix of the circle and rectangle respectively. We also specify the repeat times and the direction of motion pattern. For example, D-caca in Figure 4c means that the phone is shaked for 4 times in pattern D: clockwise, anticlockwise, clockwise, anticlockwise. The rest of the patterns can be explained similarly. Note that in the experiment, the real shaking pattern is merely close to the specified one, instead of strict match of the two patterns.

The results in Figure 4c shows that Swadloon is accurate for all motion patterns. We further analyze the detailed results of each pattern in Figure 7. More specifically, we calculate unknowns $( \lambda _ { x } , \bar { \lambda } _ { y } , \lambda _ { 0 } , \lambda _ { 1 } )$ by Eq. (12). Then, we substitute the solutions into Eq. (12) and compare the values of expression on the left side of Eq. (12) with the ones on the right side. The values represent real-time velocity relatively from a smartphone to an acoustic source. The key observation is that the compared values are very close in all cases. It means that our PLL is accurate to track relative velocity (e.g., values on the right side of Eq. (12)) and Swadloon is very robust in case of different motion patterns. Figure 7 also shows that Swadloon is very accurate when the phone moves with very small amplitude (5cm) and velocity (0 ∼ 0.4m/s).

We also find that when the phone moves clockwise, there is a positive shift in the mean value. When the phone moves anti-clockwise, there is a negative shift. Since for the arbitrary pattern A, there exist both positive and negative shifts in the measurement, the standard deviation becomes a little bigger. We also observed that when the phone was shaken in other regular patterns compared to pattern A, the standard deviation becomes smaller. That is, the error shift is close to invariable in these cases. We also find that when we shake the phone in C-ca, D-caca, the means are close to the same. Based on the results, we choose D-caca as the default motion pattern in the entire experiment. We leave it as a future work to understand why the phenomena happen.

Non-line of sight. We set $L ~ = ~ 8 m , ~ \alpha _ { r } ~ = ~ 4 5 ^ { o } ,$ $\beta ~ = ~ \gamma ~ = ~ 0 ,$ and test a simple case on the effect by Non-line of sight (NLOS). In Figure 4d, a person stands between the phone and the acoustic source, and we measure the errors related to the distance from the person to the phone. It becomes apparent that when the person stands at either ends, the standard deviation is enlarged, while the person stands in the middle, it is close to the one without obstruction. Hence, the person has little effect on direction finding, as long as s/he is not too close to the acoustic source or the receiver. This is also verified in the experiment of noisy environments.

Another case of NLOS is that the user put his back to the source. The signal turns so weak and the result becomes unstable. In this case, the user can turn around to get the precise direction. The other possible complementary method is to let user rotate the phone around the user’s body, similar to [5].

![](images/35c33710d998ff0f6950bd886fec49f480512c5a4b8e3dbf08b99b32bd878255.jpg)



![](images/d90d0bed404e12df3dcb9616c810cd6ab4e7d46fd01b58053655c31f5bba4a07.jpg)



Fig. 9: (a) Errors on different cases when $L \leq 2 4 m ,$ $\alpha _ { r } = \beta = \gamma = 0$ . (b) The opening angle errors w.r.t. multiple signals.

Multipath effect. As the multipath effect is hard to measure exactly, we first make a man-made multipath to find its impact. Then, we make a simple real case to verify our finding.

We set $L = 8 m , \alpha _ { r } = 4 5 ^ { o } , \beta = \gamma = 0$ and add another phone as acoustic source placed at position C in Figure 3b. The new source is also 8 meters from the phone. It beeps at the same frequency with the source at B. The volume of the source at B is constant 60%. We change the volume of the source at C from 0% to 100%, and plot the Figure 4e. When the volume is less than 20%, it has little effect: the standard deviation is low, and the mean value is slightly lowered. There is an interesting phenomenon that when the volume becomes larger, the angle becomes lower which is close to the direction of the new source. However, the standard deviation becomes bigger when both sources have high volume.

We then conduct an experiment with both acoustic source and phone near the wall. The wall is on the right hand side of the user while shaking the phone. We set $\alpha _ { r } = \beta = \gamma = 0$ and $L = 8 , 1 6 , \bar { 2 } 4 , 3 2 \bar { m }$ . The mean and stand deviation of $\alpha _ { r } ^ { \prime }$ is shown in Figure $4 \mathrm { f } . \ \alpha _ { r } ^ { \prime }$ becomes bigger for all the distances which can be inferred from the above conclusion. It can also be inferred that the strengths of the reflected signals relative to the respective direct signals are different at each $L ,$ which causes different mean shifts of $\alpha _ { r } ^ { \prime }$ . The additional observation is that the standard deviation is low for each distance. Hence, reflected signal is weak compared to the one directly from the acoustic source.

# 5.1.3 Empty Room with Multiple Acoustic Waves

To validate the robustness of Swadloon, we conduct two types of experiments: (1) an acoustic source broadcasts multiple signals at different frequencies, (2) multiple sources broadcast signals at different frequencies.

In experiment (1), we measure the angular errors when the acoustic source sends 6 sinusoidal signals at the frequency from 17000Hz to 19500Hz. The experiment is performed by setting $\alpha _ { r } = \beta = \gamma = 0$ . We find that the results are similar for different L that $L \ \leq \ 2 4 m ,$ while the ones at $L ~ = ~ 3 2 m$ are a little worse. It is because that when the phone sends multiple signals, the signal strength of each component becomes weaker. We plot CDF at $L \leq 2 4 m$ in Figure 9a. The performance is almost the same with the one sending a single wave. It can be deduced that we can use loudspeakers in the mall as anchor nodes while they are playing music.

We now analyze the performance of direction finding when there are multiple acoustic sources. The performance in this case will have direct impacts on the accuracy of the localization to be studied later in Subsection 5.2.1. Recall that as the computing of the absolute direction requires the accurate compass which is hard to get, in our localization method we use the opening angle $\angle A _ { i } P A _ { j }$ from the phone with location $\bar { P }$ to two arbitrary anchor nodes $A _ { i }$ and $A _ { j }$ instead of the absolute orientation of any vector $P A _ { i }$ or $P A _ { j }$ . Thus, here we measure the accuracy of estimated angle $\angle A _ { i } P A _ { j }$ by varying the locations of $P , A _ { i } ,$ and $A _ { j }$ .

Figure 9b shows the opening angle errors in three cases: (1) single source, multiple waves, super market, (2) single source, multiple waves, empty room, (3) multiple source, multiple waves, empty room. We find that the opening angle errors in cases (1), (2) are less than the direction errors in Figure 9a. Furthermore, we observe that case (3) is much worse than (2). Though it is unfair to compare the two cases that the acoustic sources are different, it shows the possibility of improvement on the precision of indoor localization by using better acoustic sources, as we use the worse case for calculating the latter position.

# 5.1.4 Noisy Environment

We conduct this experiment in a super market, where it is noisy (−21 dBFS) and there are people walking around and blocking the line from the acoustic source to the phone. We also let the phone send multiple signals. In Figure 9, the result becomes a little worse than the one in empty room. Almost all errors are less than 10 degrees, which are acceptable.

# 5.1.5 Overhead

As Swadloon calculates the direction in real time, we only evaluate the CPU usage. When Swadloon processes one acoustic signal, the CPU usage of the phone is 20.5%. When processing multiple signals, the pass band of BPF narrows down, which causes higher computation overhead per signal. There are multiple solutions for reducing the overhead, e.g., choosing IIR filter instead of the FIR filter, processing the signal in the network server, etc. Above all, as we only need to shake the phone for a short duration to get the directions, the overhead is low that the total computation time is only within several seconds.

![](images/e033dcc7e4c2f09c09d3e7802ec8e0b5501e6cbe300baf037d4aefdbc3da21b8.jpg)



(a) Trilateration

![](images/de057a300bc216c9f33e3ff6bb47009838f110e22bb5bb023df096955f757156.jpg)



(b) Acute Angle

![](images/0ab69d9bf10b0a0b6239921650d93bee5e8a5038c50446803402d11a9fb60ac1.jpg)



(c) Obtuse Angle

![](images/92e1423b520c38f42ae116d18f745618d305f9d2480d9be1b71a24d69e72d860.jpg)



(d) Good layout

![](images/41d70b5b6c74ea34e8a7d4f36af4e24f3da9adbfc08a0615b6c11b5180cc3a8a.jpg)



(e) Bad layout   
Fig. 10: Indoor localization and tracking: (a) trilateration, (b) pinpoint candidate location to a circle.

# 5.2 Real-time Localization

We now describe our basic method of applying Swadloon to fine-grained indoor localization illustrated in Figure 10a, which is based on the direction α and the phase φ in Section 4. Note that there are sophisticated methods leverage merely the Doppler frequency shift for localization, $e . g .$ , [42], we just provide a simple method as a case study to evaluate the accuracy of direction finding and phase shift measurement.

We require that there are at least three acoustic sources as anchor nodes installed, which send sinusoid signals at the specific different frequencies. Users need to get the position and frequency of each anchor node from network service. It includes two phases: finding the initial position and real-time tracking.

# 5.2.1 Static Position Localization

The user needs to shake the phone first in order to get his/her initial position. The phone calculates the direction of each anchor node in WCS and then gets the position. Note that as the compass is not precise, the calculated directions, such as α1, α2 in Figure 10a, are not directly used in calculating the position. However, observe that the opening angle $\left( \alpha _ { 1 } - \alpha _ { 2 } \right)$ is fixed no matter which WCS is chosen. We calculate the initial position using this opening angle. Taking the positions $( x _ { 1 } , y _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } )$ of two anchor nodes $A _ { 1 }$ and $A _ { 2 }$ and the relative directions $P A _ { 1 } , P A _ { 2 }$ from phone (with unknown position P ) to $A _ { 1 }$ and $A _ { 2 } ,$ we can compute the distance $D \ = \ \| A _ { 1 } - A _ { 2 } \|$ and the opening angle $\alpha _ { d } ~ = ~ \angle A _ { 1 } P A _ { 2 } ,$ , as illustrated in Figure 10a. It can be inferred that the position P is on a fixed circle illustrated in Figure 10b, 10c. If $\alpha _ { d }$ is an acute angle as in Figure 10b, $\alpha _ { c } = 2 \alpha _ { d } . \mathrm { ~ } S 0 _ { \ l { i } }$ , the radius of the circle R = D2 sin α $\begin{array} { r } { R = \frac { \textbf {  { D } } } { 2 \sin \alpha _ { d } } } \end{array}$ . Then we get at most two possible solutions of the position of the circumcenter O by using radius R and the given coordinates of two nodes $A _ { 1 }$ and $A _ { 2 }$ . If $\alpha _ { d }$ is an acute angle, then O and P are on the same side of $A _ { 1 } A _ { 2 }$ . Similarly, if $\alpha _ { d }$ is an obtuse angle, as in Figure 10c, O and $P$ are on the opposite side of $A _ { 1 } A _ { 2 }$ .

For a system of n anchor nodes, there are $\frac { n ( n - 1 ) } { 2 }$ pairs of anchor nodes. As a result, phone P lies on n(n−1) circles. Thus, with at least 3 anchor nodes, $\frac { \ \mathbf { \dot { \bar { \alpha } } } _ { n } ( n - 1 ) } { 2 }$ we can get the position of P . It is worth mentioning that for the circle formed by a node pair, the circle is divided into two arcs by the node pair. Node P only lies on one of the arcs, depending on whether $\alpha _ { d }$ is an acute angle or an obtuse angle. Hence, for localization we search for the point P to minimize $\textstyle \sum _ { i } d _ { i }$ where $d _ { i }$ is the distance from P to the ith arc.

We claim that it will result in better localization accuracy if we place the anchor nodes in a line as in Figure 10d compared to the one in Figure 10e. In Figure 10e, the centers of the circles are too close, which causes big potential errors. The root reason is that the 4 points $A _ { 1 } , A _ { 2 } , A _ { 3 } , P$ are nearly at the same circle, which means the arbitrary point, $e . g . , A _ { 1 } ,$ is close to the circle which is constructed by the rest of 3 points, $e . g . , A _ { 2 } , A _ { 3 } , P .$

Experimental setup: In Figure 11, we place 6 phones as anchor nodes in the same empty room in the previous subsection. The positions are (0, −3), (6, 0), (12, 0), (18, 0), (24, 0), (30, −3) (meters) respectively. The beep frequencies are from 17000 to 19500Hz. We choose spots at $y \in \{ - 3 , - 6 \}$ and $x \in \{ 6 , 9 , 1 2 , 1 5 , 1 8 , 2 1 , 2 4 \}$ . We conduct the localization when people stay at these spots, and repeat the experiment 30 times for each spot.

![](images/ea3aaa12671df7b3bc7cbb76a5a96c9bc882403416564986af61889c312417d2.jpg)



(a) Indoor environment

![](images/7f8c96658e70e74b937f8b089c9dfe924a4b2ce40ee2454d64aa37c236a92918.jpg)



(b) Layout of anchors   
Fig. 11: Indoor localization testing prototype.

Evaluation: The accuracy of static localization is shown in Figure 12a. Swadloon achieves localization errors within 0.42m, 0.92m, 1.08m, 1.73m at the percentage of 50%, 90%, 95%, and 100% respectively. The mean error and the standard deviation is 0.50m and 0.59m respectively. We also find that the localization accuracy at spots with $y = - 3 m$ is better than the ones on $y = - 6 m$ . Specifically, on $y = - 3 m$ , the localization errors are within $0 . 2 8 m , \ 0 . 7 3 m , \ 0 . 9 1 m ,$ , 1.73m at the percentage of 50%, 90%, 95%, and 100% respectively.

Meanwhile, we find that there are nearly constant error shifts of the calculated position at all locations. Thus, we further adjust the position by linear regression. That is, we build a polynomial function model from the calculated positions to more precise positions by learning the results from half of the samples. We then apply the function to the other half and the result is plotted in Figure 12b. It shows that the precision is greatly enhanced (i.e., the errors are within 0.67m,

![](images/f09c2ef801d8899e71b1353aa98a693c7af9c4c21c3782535a19bd0942183818.jpg)



Fig. 13: Precise real-time indoor tracking.

0.82m, 1.56m at the percentage of 90%, 95%, 100% respectively).

We then measure the errors of static localization in a large office (-34 dBFS), where the environment is much more complicated. The layout of the anchor nodes is nearly the same with the one in Figure 11, except the anchor nodes are installed on the ceiling. Figure 12b shows that the error is within 0.94m, 1.23m, 2.59m at the percentage of 80%, 90%, 100% respectively after linear regression.

We also choose specific number of nodes $( i . e . , 3 \sim 6 )$ （号 from the 6 nodes to calculate the position. In Figure 12c, it shows that the precision is greatly enhanced when the number of nodes increases. Besides, precision in case of 3 nodes becomes much worse for it is more sensitive by the layout shown in Figure 10d, 10e.

# 5.2.2 Real-time Tracking

In this phase, the user does not need to shake the phone again to obtain the position. The position is tracked in real time by tracking the relative displacement to each anchor using Eq. (4)(8), and the update rate is 0.05s or 0.25s in our experiment. In Figure 10a, if the location of phone at time t has been calculated, denoted as $( x , y )$ , we calculate its location (˜x, y˜) at the latter time t˜ by getting s(t) and $s ( \tilde { t } )$ using Eq. (4), Eq. (8). Then we calculate next location according to (˜x, y˜) iteratively. Specifically, if the user gets the location (x, y), then the distance from (x, y) to $( x _ { i } , y _ { i } )$ is $L _ { i } = \sqrt { ( x - x _ { i } ) ^ { 2 } + ( y - y _ { i } ) ^ { 2 } + h _ { i } ^ { 2 } } ,$ where $h _ { i }$ is the relative height between the phone and the source $( x _ { i } , y _ { i } )$ . Thus, s/he gets the distances from all the available acoustic sources at time t. For $s ( t ) = L ( 0 ) - L ( t )$ and L(0) is constant initial distance, we can infer from Eq. (4) that

$$
\tilde {L} _ {i} = L _ {i} - \frac {v _ {a}}{2 \pi f _ {a}} (\tilde {\phi} _ {i} - \phi_ {i}) \tag {14}
$$

where $\tilde { L _ { i } } = L _ { i } ( \tilde { t } )$ and $\tilde { \phi } _ { i } = \phi _ { i } ( \tilde { t } )$ . Since $\phi _ { i }$ and $\tilde { \phi _ { i } }$ can be calculated by Eq. (8) and $L _ { i }$ is already calculated, the latter $\tilde { L _ { i } }$ can be derived from Eq(14). Then we search for location (˜x, y˜) near (x, y) to minimize $\textstyle \sum _ { i } M _ { i }$ where $M _ { i } = \big | \tilde { L _ { i } } - \sqrt { ( \tilde { x } - x _ { i } ) ^ { 2 } + ( \tilde { y } - y _ { i } ) ^ { 2 } + h _ { i } ^ { 2 } } \big |$ .

We conduct real time indoor tracking using the same environment as in Figure 11. In our experiments reported here, a user starts from spot (6, −6) shown in Figure 13. Then, the user walks in some specific paths with length more than 50m with the phone in his/her hand to the destination at spot (24, −3). The errors are kept within 0.4m shown in Figure 13.

We then consider the case that there are errors on the calculated initial position when the user starts walking. For each test, we uniformly choose a spot which is 0.25m, 0.5m, 0.75m, or 1m from (6, −6), and measure the localization accuracies at the destination, $i . e . ,$ distances from (24, −6) to the calculated final positions in Figure 12e. We can observe that the errors at the initial position do not affect the real time tracking, where the error is still within 2m when the user walks in 51 meters and the initial position error is 1m.

To reduce the computation overhead, we let the phone process 20% of the samples, instead of full samples. Specifically, it processes consecutive samples of 0.05s for each 0.25s. Hence, the phone can deal with the samples and track the position in real time. The result is close to the one which processes full samples in Figure 13. We plot the localization errors in Figure 12d. The mean error and standard deviation in this case is 0.29m and 0.34m respectively, which is still very precise. CPU usage can also be lowered down by using 10% of the sample with the mean error of 1.02m, if the CPU of some other phone is not fast enough.

Note that the phone still constantly uses extra energy when the user is not shaking the phone. Actually, to determine when we can stop displacement tracking to save energy, we could use the inertial sensors to detect whether the user is static. We can further reduce the energy cost by designing more complicated algorithm, e.g., combining step counting (rough tracking) with our displacement measurement (precise tracking). Since we mainly concern the accuracy and energy cost of displacement tracking by PLL, we do not make further optimization and evaluations in this case.

# 6 CONCLUSION

In this paper, we propose Swadloon, a novel acousticbased method to find the direction of the acoustic source. Swadloon effectively leverages the Doppler effects of the acoustic waves received by phones by exploiting the sensors in the smartphone and existing speakers to send sinusoidal signals. Our extensive evaluations show that Swadloon performs extremely well in phone-to-phone direction finding and realtime indoor localization. Note that in localization, we do not directly use the ranging result as accurate ranging often needs either time-synchronization or communication between two nodes, which require special hardware as anchor. Hence, some future work is to develop some mechanism achieving both ranging and direction finding simultaneously, and achieve the mechanism without the requirement of phoneshaking movement.

# ACKNOWLEDGEMENT

The research is supported by National Natural Science Foundation of China under Grant No.61202404,

![](images/3d4aedaea8278a6054ede4f1413692fd7f658bad7ab1949cdc28d62e99427f45.jpg)



(a) Position Error (m)

![](images/deb7ca833df323311c6a59a3099914b01cfc92a1017d0ceb370083076c29577b.jpg)



(b) Position Error (m)

![](images/43a9226cad4ec515c0e3a19f1453fc711e0d44c5456fbee75132a3cd24685837.jpg)



(c) Position Error (m)

![](images/db608d819b28b74c0b5e06f0306f5e0d7b5c5e40796e89163fd3cc02599dbf78.jpg)



(d) Walking Length (m)

![](images/beedf93a2f7dc69d60ad6333914979465f309025f45c51776a5ac83835087d6b.jpg)



(e) Position Error (m)   
Fig. 12: Accuracy of static localization (a) in different locations, (b) in different scenes and by different methods. (c) when parts of the anchor nodes are chosen for calculation. Tracking accuracy (d) along the walking paths, (e) at final point (24, −3) when there are initial position errors at (6, −6).

No.61170233, No.61232018, No.61272472, No.61272317, No.61272426 and NSF China Major Program 61190110. The research of Li is partially supported by NSF CNS-1035894, NSF ECCS-1247944, NSF ECCS-1343306, NSF CMMI 1436786, National Natural Science Foundation of China under Grant No. 61170216, No. 61228202. It is also supported by NSFC\RGC Joint Research Scheme 61361166009, RFDP 20121018430, and the Fundamental Research Funds for the Central Universities, WK0110000041.

# REFERENCES

[1] Facebook’s friendshake. http://www.facebook.com.   
[2] Google latitude. https://www.google.com.hk/latitude/.   
[3] K. Joshi, S. Hong, and S. Katti, “Pinpoint: localizing interfering radios,” in USENIX NSDI, 2013, pp. 241–254.   
[4] Z. Li, X. Wang, Z. Du, and K. Gong, “Performance evaluation of a four-element antenna array with selection circuits for adaptive mimo systems,” Tsinghua Science & Technology, 2010, pp. 294 – 298.   
[5] Z. Zhang, X. Zhou, W. Zhang, Y. Zhang, G. Wang, B. Y. Zhao, and H. Zheng, “I am the antenna: accurate outdoor ap location using smartphones,” in ACM MobiCom, 2011, pp. 109–120.   
[6] Y. Nishimura, N. Imai, and K. Yoshihara, “A proposal on direction estimation between devices using acoustic waves,” in MobiQuitous, 2012, pp. 25–36.   
[7] J. Qiu, D. Chu, X. Meng, and T. Moscibroda, “On the feasibility of real-time phone-to-phone 3d localization,” in ACM SenSys, 2011, pp. 190–203.   
[8] A. Prorok, P. Tome, and A. Martinoli, “Accommodation of nlos for ultra-wideband tdoa localization in single- and multi-robot systems,” in IEEE IPIN, 2011, pp. 1–9.   
[9] H. Liu, H. Darabi, P. P. Banerjee, and J. Liu, “Survey of wireless indoor positioning techniques and systems,” IEEE Transactions on Systems, Man, and Cybernetics, Part C, 2007, pp. 1067–1080.   
[10] H. Liu, Y. Gan, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, “Push the limit of wifi based localization for smartphones,” in ACM MobiCom, 2012, pp. 305–316.   
[11] A. Subramanian, P. Deshpande, J. Gaojgao, and S. Das, “Driveby localization of roadside wifi networks,” in IEEE INFOCOM, 2008, pp. 718–725.   
[12] G. Zhang, Y. Xu, X. Wang, X. Tian, J. Liu, X. Gan, H. Yu, and L. Qian, “Multicast capacity for vanets with directional antenna and delay constraint,” IEEE Journal on Selected Areas in Communications, 2012, pp. 818–833.   
[13] J. Iguchi-Cartigny, P. M. Ruiz, D. Simplot-Ryl, I. Stojmenovic, and C. M. Yago, “Localized minimum-energy broadcasting for wireless multihop networks with directional antennas,” IEEE Trans. Computers, 2009, pp. 120–131.   
[14] D. Niculescu and B. R. Badrinath, “Ad hoc positioning system (aps) using aoa,” in IEEE INFOCOM, 2003, pp. 1734 – 1743.   
[15] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, “Beepbeep: a high accuracy acoustic ranging system using cots mobile devices,” in ACM SenSys, 2007, pp. 1–14.

[16] L. Zhang, X. Li, W. Huang, K. Liu, S. Zong, X. Jian, P. Feng, T. Jung, and Y. Liu, “It starts with igaze: visual attention driven networking with smart glasses,” in ACM MobiCom, 2014, pp. 91–102.   
[17] C. Peng, G. Shen, Y. Zhang, and S. Lu, “Point&connect: intention-based device pairing for mobile phone users,” in ACM MobiSys, 2009, pp. 137–150.   
[18] R. B. P. Z. Zheng Sun, Aveek Purohit, “Spartacus: Spatiallyaware interaction for mobile devices through energy-efficient audio sensing,” in ACM MobiSys, 2013, pp. 263–276.   
[19] K. Liu, X. Liu, L. Xie, and X. Li, “Towards accurate acoustic localization on a smartphone,” in IEEE INFOCOM, 2013, pp. 495–499.   
[20] L. Zhang, K. Liu, Y. Jiang, X. Li, Y. Liu, and P. Yang, “Montage: Combine frames with movement continuity for realtime multiuser tracking,” in IEEE INFOCOM, 2014, pp. 799–807.   
[21] L. Yang, Y. Chen, X. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: real-time tracking of mobile RFID tags to high precision using COTS devices,” in ACM MobiCom, 2014, pp. 237–248.   
[22] C. Bo, D. Ren, S. Tang, X. Li, X. Mao, Q. Huang, L. Mo, Z. Jiang, Y. Sun, and Y. Liu, “Locating sensors in the forest: A case study in greenorbs,” in IEEE INFOCOM, 2012, pp. 1026–1034.   
[23] L. Li, P. Hu, C. Peng, G. Shen, and F. Zhao, “Epsilon: A visible light based positioning system,” in USENIX NSDI, 2014, pp. 331–343.   
[24] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in ACM MobiCom, 2012, pp. 269–280.   
[25] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: zero-effort crowdsourcing for indoor localization,” in ACM MobiCom, 2012, pp. 293–304.   
[26] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: unsupervised indoor localization,” in ACM MobiSys, 2012, pp. 197–210.   
[27] J. Zhao, W. Xi, Y. He, Y. Liu, X.-Y. Li, L. Mo, and Z. Yang, “Localization of wireless sensor networks in the wild: Pursuit of ranging quality,” IEEE/ACM Trans. Netw., 2013, pp. 311–323.   
[28] W. Xi, Y. He, Y. Liu, J. Zhao, L. Mo, Z. Yang, J. Wang, and X.-Y. Li, “Locating sensors in the wild: pursuit of ranging quality,” in ACM SenSys, 2010, pp. 295–308.   
[29] Z. Yang, Y. Liu, and X.-Y. Li, “Beyond trilateration: On the localizability of wireless ad-hoc networks,” in IEEE INFOCOM, 2009, pp. 2392 – 2400.   
[30] X. Chen, X. Wu, X. Li, Y. He, and Y. Liu, “Privacy-preserving high-quality map generation with participatory sensing,” in IEEE INFOCOM, 2014, pp. 2310–2318.   
[31] J. T. Biehl, M. Cooper, G. Filby, and S. G. Kratz, “Loco: a ready-to-deploy framework for efficient room localization using wi-fi,” in ACM UbiComp, 2014, pp. 183–187.   
[32] Y. Zheng, G. Shen, L. Li, C. Zhao, M. Li, and F. Zhao, “Travi-navi: self-deployable indoor navigation system,” in ACM MobiCom, 2014, pp. 471–482.   
[33] L. Li, G. Shen, C. Zhao, T. Moscibroda, J. Lin, and F. Zhao, “Experiencing and handling the diversity in data density and environmental locality in an indoor positioning service,” in ACM MobiCom, 2014, pp. 459–470.   
[34] Bytelight technology. http://www.bytelight.com/.   
[35] J. Yang, S. Sidhom, G. Chandrasekaran, T. Vu, H. Liu, N. Cecan, Y. Chen, M. Gruteser, and R. P. Martin, “Detecting driver

phone use leveraging car speakers,” in ACM MobiCom, 2011, pp. 97–108.   
[36] K. Liu, X. Liu, and X. Li, “Guoguo: enabling fine-grained indoor localization via smartphone,” in ACM MobiSys, 2013, pp. 235–248.   
[37] Z. Zhang, D. Chu, X. Chen, and T. Moscibroda, “Swordfight: enabling a new class of phone-to-phone action games on commodity phones,” in ACM MobiSys, 2012, pp. 1–14.   
[38] R. Nandakumar, K. K. Chintalapudi, and V. N. Padmanabhan, “Centaur: locating devices in an office environment,” in ACM MobiCom, 2012, pp. 281–292.   
[39] S. P. Tarzia, P. A. Dinda, R. P. Dick, and G. Memik, “Indoor localization without infrastructure using the acoustic background spectrum,” in ACM MobiSys, 2011, pp. 155–168.   
[40] Y. T. H. M. Hiroyuki Satoh, Makoto Suzuki, “Poster abstract: Ambient sound-based proximity detection with smartphones,” in ACM SenSys, 2013, pp. 58:1–58:2.   
[41] H. lin Chang, J. ben Tian, T.-T. Lai, H.-H. Chu, and P. Huang, “Spinning beacons for precise indoor localization,” in ACM SenSys, 2008, pp. 127–140.   
[42] B. Kusy, A. L ´ edeczi, and X. D. Koutsoukos, “Tracking mobile ´ nodes using rf doppler shifts,” in ACM SenSys, 2007, pp. 29– 42.   
[43] S. Beauregard and H. Haas, “Pedestrian dead reckoning: A basis for personal positioning,” in IEEE WPNC, 2006, pp. 27– 36.   
[44] C. Bo, X.-Y. Li, T. Jung, X. Mao, Y. Tao, and L. Yao, “Smartloc: push the limit of the inertial sensor based metropolitan localization using smartphone,” in ACM MOBICOM, 2013, pp. 195–198, poster.   
[45] J. Rosen and L. Gothard, Encyclopedia of Physical Science. Facts on File, 2009.   
[46] J. Claerbout, Earth soundings analysis: Processing versus inversion. Blackwell Scientific Publications, 1992.   
[47] M. Rice, Digital Communications: A Discrete-Time Approach. Prentice Hall, 2008.   
[48] C. R. Johnson and W. A. Sethares, Telecommunication Breakdown; Concepts of communication Transmitted via Software-Defined Radio. Prentice Hall, 2003.

![](images/ebb4ff493fd8516659ceba1e9f314794af3e2629f6485bf353844a73452647a6.jpg)



Wenchao Huang received the B.S. and Ph.D degrees in computer science from University of Science and Technology of China in 2005 and 2011, respectively. He is currently a Research Associate in School of Computer Science and Technology, University of Science and Technology of China. His current research interests include mobile computing, information security, trusted computing and formal methods.

![](images/8bb04936d7bb199e78738a6d12615354e5fdae85190094b032260e3a56641916.jpg)



Yan Xiong received the B.S., M.S., and Ph.D degrees from University of Science and Technology of China in 1983, 1986 and 1990 respectively. He is a professor in School of Computer Science and Technology, University of Science and Technology of China. His main research interests include distributed processing, mobile computing, computer network and information security.

![](images/5b93fe0cf000214a3c4513266a6eb15964a0c7828861690c7fad291310b4ead1.jpg)



Xiang-Yang Li is a professor at the Illinois Institute of Technology, IEEE Fellow, ACM Distinguished Scientist, and holds EMC-Endowed Visiting Chair Professorship at Tsinghua University. He is a recipient of China NSF Outstanding Overseas Young Researcher (B). Dr. Li received MS (2000) and PhD (2001) degree at Department of Computer Science from University of Illinois at Urbana-Champaign, a Bachelor degree at Department of Computer Science and a Bachelor degree at Department of Business Management from Tsinghua University, P.R. China, both in 1995. His research interests include wireless networking, mobile computing, security and privacy, cyber physical systems, smart grid, social networking, and algorithms.

![](images/cc5ea4cbdbdd7df158238975b7d256f62e806831e813483ef2cf89025ca191f3.jpg)



Hao Lin received his B.S. degree and M.S. degree in computer science from Jiangnan University, in 2011 and 2014 respectively. He is currently a software engineer in China Pacific Insurance (Group) Co. Ltd. His current research interests include mobile computing, wireless network and data mining.

![](images/2fba960dffc3e21ffa0dc223252af2c5bce3534a09097515e358334e41a02beb.jpg)



Xufei Mao received the Ph.D. degree in Computer Science from Illinois Institute of Technology, Chicago in 2010. He received the MS degree (2003) in Computer Science and the Bachelor degree (1999) in Computer Science at Northeastern University and Shenyang University of Technology respectively. He is with the School of Software and TNLIST, Tsinghua University, Beijing China. His research interests span wireless ad-hoc networks, wireless sensor networks, pervasive computing, mobile cloud computing and game theory.

![](images/d9fa2d655e32bfdc475327bcb3c058b60ec00d4acd3f0e409b828afdf7f7b573.jpg)



Panlong Yang received his B.S. degree, M.S. degree, and Ph.D. degree in communication and information system from Nanjing Institute of Communication Engineering, China, in 1999, 2002, and 2005 respectively. Dr. Yang is now an associate professor in the PLA University of Science and Technology. Dr. Yang has published more than 50 papers in the areas of mobile ad hoc networks, wireless mesh networks and wireless sensor networks.

![](images/42693909f396136cd6d4da201552e12ae9f5045e08a652e8a8150ef5f9142ab6.jpg)



Yunhao Liu received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. Yunhao is the Director of Key Laboratory for Information System Security, Ministry of Education, and Professor at School of Software, Tsinghua University. His research interests include pervasive computing, peer-to-peer computing, and sensor

networks.

![](images/10c9754199d1e76c1753b3602c9bb395c3ea576b8b98a8d34b321ac83323b26a.jpg)



Xingfu Wang received the B.S. degree in Electronic and Information Engineering from Beijing Normal University of China in 1988 and the M.S. degree in computer science from University of Science and Technology of China in 1997. He is an associate professor in the School of Computer Science and Technology, University of Science and Technology of China. His current research interests include information security, data management, and WSN.