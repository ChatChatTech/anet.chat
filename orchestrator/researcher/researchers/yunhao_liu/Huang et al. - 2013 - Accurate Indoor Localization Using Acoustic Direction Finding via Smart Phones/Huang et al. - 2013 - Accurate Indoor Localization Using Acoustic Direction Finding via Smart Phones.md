# Accurate Indoor Localization Using Acoustic Direction Finding via Smart Phones

Wenchao Huang, Yan Xiong ∗, Xiang-Yang Li †, Hao Lin ‡, Xufei Mao , Panlong Yang , Yunhao Liu §

# ABSTRACT

We propose and implement a novel indoor localization scheme, Swadloon, built upon an accurate acoustic direction finding. Swadloon leverages sensors of the smartphone without the requirement of any specialized devices. The scheme Swadloon does not rely on any fingerprints and is very easy to use: a user only needs to shake the phone for a short duration before walking and localization. Our Swadloon design exploits a key observation: the relative displacement and velocity of the phone-shaking movement corresponds to the subtle phase and frequency shift of the Doppler effects experienced in the received acoustic signal by the phone. A novel method is designed to derive the direction from the phone to the acoustic source by combining the velocity calculated from the subtle Doppler shift with the one from the inertial sensors of the phone. Then a real-time precise localization and tracking is enabled by using a few anchor speakers with known locations. Major challenges in implementing Swadloon are to measure the frequency shift precisely and to estimate the shaking velocity accurately when the speed of phone-shaking is low and changes arbitrarily. We propose rigorous methods to address these challenges, and then design and deploy Swadloon in several floors of an indoor building each with area about 2000m2. Our extensive experiments show that the mean error of direction finding is around 2.1o when the acoustic source is within the range of 32m. For indoor localization, the 90-percentile errors are under 0.92m, while the maximum error is 1.73m and the mean is about 0.5m. For real-time tracking, the errors are within 0.4m for walks of 51m.

# 1. INTRODUCTION

Phone-to-phone direction finding is attractive in mobile social networks nowadays for supporting various applications, e.g., friending, and sharing. Recent mobile apps have made similar functions, such as Facebook’s Friendshake [2] and Google Latitude [4]. However, they are based on GPS and cannot be applied to indoor environment. An accurate method of direction finding is by using directional antenna [11,19,30], but it requires specialized hardware and clearly limits the availability to regular users. Several approaches of direction finding by smartphones have been proposed [20, 25, 38]. However, it remains a challenge to do accurate direction finding by phone under long distance.

Precise indoor localization is also important for location based services. Those methods achieving high accuracy usually require special hardware not readily available on smartphones [24], or infrastructures expensive to deploy [15]. Pure WiFi-based localization can achieve reasonable accuracy (e.g., 3∼4m), but there always exist large errors (e.g., 6∼8m) unacceptable for many scenarios [16]. Though there have been many proposals improving the accuracy of WiFi based localization (e.g., with 80-percentile errors about 1m [16]) by exploiting additional signals, low-cost precise indoor localization is still challenging.

We propose Swadloon, a Shake-and-Walk Acoustic Direction-finding and indoor LOcalizatiON scheme using smartphones. Swadloon has two key components, precise phone-to-phone (or phone-to-speaker) direction finding and accurate indoor localization, each of which has a wide range of applications. Assume that there is an acoustic signal emitted from a speaker or a phone. Swadloon exploits the fact that shaking the smartphone or walking with the smartphone will cause Doppler effects on the acoustic signal received by the smartphone. Swadloon precisely measures the real-time phase and frequency shift of the Doppler effect, which corresponds to the relative displacement and velocity from the phone to the acoustic source respectively. Swadloon then obtains the accurate direction of the acoustic source by combining the relative velocity calculated from the Doppler shift with the one from the inertial sensors of the smartphone, i.e., the accelerometer and the gyroscope.

The main challenges of implementing Swadloon are the noisy data collected from inertial sensors, and the measurement of the subtle frequency shift when the motion velocity of phone is slow or fluctuates continuously. We propose several rigorous methods (discussed in detail in Section 4) in Swadloon to address these challenges, e.g., we use Phase Locked Loop (PLL) to precisely measure the phase and frequency shift. Note that for phone-to-phone direction finding, the object phone of direction finding serves as an acoustic source, and the finder shakes his/her phone gently to produce the Doppler effect.

Based on this precise direction finding, Swadloon achieves accurate real-time indoor localization using a few anchoring nodes with known locations. These anchoring speakers will emit acoustic signals using non-audible frequency (typically around 20kHz). The smartphones play the role of receivers. As it is difficult for a smartphone to find an accurate North as base for absolute direction, our localization method does not exploit the absolute direction. Instead we use a simple “triangulation” method by exploring the accurate opening angle from phone to two anchoring speakers. Swadloon let each phone measure the direction to source and its relative displacement for achieving precise localization and real-time tracking respectively. Anchor nodes will not perform any computation or communication. Thus, Swadloon supports arbitrary number of users with extremely low cost.

We designed, deployed, and evaluated Swadloon for both direction finding and real-time indoor localization. Our extensive experimental results show that Swadloon supports high accuracy for both direction finding and real-time indoor localization. In our testing of Swadloon, the finder only needs to shake the phone gently and in arbitrary patterns, which is different from the method in [20] as it requires the user to stretch the arm and then swing the phone through 180 degrees. For the phone-to-phone direction finding, the mean error of the measured angle is 2.10o within the range of 32m, and the errors are under 2.06o, 4.43o, 5.81o at 50%, 90%, 95% respectively, when the acoustic source faces towards to the phone. For indoor localization, we deploy one acoustic source per 6 meters, which broadcasts signals at a predefined frequency. For indoor localization, Swadloon achieves 90-percentile accuracy of 0.92m, maximum error of 1.73m, and the mean error of 0.5m. For real-time indoor tracking, the error is always kept within 0.4m even when users walk for more than 50 meters.

The rest of the paper is organized as follows. We review the related work in Section 2 and present technical preliminaries in Section 3. We present the acoustic direction finding of Swadloon in Section 4, and indoor localization and tracking in Section 5. We report our extensive experiment results in Section 6. We conclude the paper in Section 7.

# 2. RELATED WORK

# 2.1 Direction Finding

Specialized Hardware: One type of approaches is by using directional antenna [11, 19, 30] or antenna array [12] to implement Angle of Arrival (AOA) [18] in localization. For example, by rotating the beam of its antenna, a receiver can pinpoint the direction of the AP as the direction that provides the highest received strength [30].

Non-specialized hardware: [38] effectively emulates the sensitivity and functionality of a directional antenna by rotating the phone around the user’s body, to locate outdoor APs. [25] leverages 2 microphones at each phone, i.e., at least 4 microphones, for calculating 3D position of each other by using the distance ranging method [21]. As the work is intended for high-speed, locational, phone-to-phone (HLPP) games, it does not show the result when two phones are in long distances. Another method [22] close to direction finding is to identify which target the user is pointing at when s/he moves mobile phone towards the target phone.

To the best of our knowledge, the approach closest to ours in direction finding is [20]. It estimates the direction by using Doppler effect and achieves the mean angular errors within 18o. This approach requires the searching user generates a Doppler Effect to all directions, e.g., the user stretches the arm while holding the searching device, and then swings it through 180 degrees. Swadloon only requires that the user shakes the phone in an arbitrary path.

# 2.2 Indoor Localization and Tracking

Wireless Localization: A significant advantage of wireless localization is that it only leverages an existing infrastructure instead of special-purpose hardware. Hence it attracts many research efforts, e.g., [5, 9, 16, 26, 35, 36]. However, it is found [16] that the wireless localization, such as the WiFi-based localization, can achieve reasonable accuracy (e.g., 3 ∼ 4m), but there always exist large errors (e.g., 6 ∼ 8m) unacceptable for many scenarios. There have been many schemes proposed recently that improve the accuracy, such as using hundreds of APs [7], or adding additional constraints by exploiting the coordination among several phones running this application in a small area [16].

Infrastructure-based Localization: There have been myriad approaches of indoor localization based on specialpurpose infrastructure. They are based on alternative signals, e.g., infrared [32], acoustic [33], visual [29]. These approaches can achieve high accuracy, but the need for special-purpose hardware and infrastructure is a significant challenge [26]. Cricket [23] uses concurrent radio and ultrasonic signals to infer distance and obtain the location. ByteLight [1] claims to be able to provide low-price infrastructure for localization using ceilingembedded LEDs which send out Morse Code-like signals to be detected by the smartphone’s camera.

Our prototype provides another choice for precise indoor localization, which only needs the off-the-shelf speakers, or even the loudspeakers installed in the mall, which can beep using high frequency channel without affecting normal broadcast.

Leveraging the acoustic wave by phone: The methods of leveraging the acoustic wave in smartphone applications have been well addressed. Most of them are leveraging the low speed of the acoustic wave compared to wireless signals, such as the mechanism of TOA [21] and TDOA [34]. BeepBeep [21] detects the distance between two smartphones with high accuracy. It has been used by many other schemes, such as HLPP games [25, 37], device pairing [22] and indoor localization [16, 17].

In this work, we leverage the Doppler effects of the acoustic waves $( i . e . ,$ measuring the precise relative displacement and velocity of phone) to design Swadloon for direction finding and indoor localization. Swadloon is precise enough to be another basic tool of AOA, while it only requires off-the-shelf speakers. Furthermore, Swadloon supports arbitrary number of users and the phones of users do not need to send any signals to get the location, which avoids the signal interference when the number of users increases.

Leveraging the Doppler effects: Doppler effects have been leveraged in wide areas, such as radar, satellite communication, medical imaging and blood flow measurement, etc. There are also localization approaches leveraging the Doppler shift of wireless signals in localization [14] and tracking [13] in wireless sensor networks. But it also needs special hardware not available for smartphone users. Meanwhile, by using the phase shift, Swadloon easily implements precise tracking without complicated algorithms compared with [13] which uses frequency shift.

Leveraging the inertial sensors: Inertial sensors have been used for pedestrian dead-reckoning [6] in indoor localization. The challenge is that it suffers from large accumulation of errors. The complementary approaches to this problem are proposed in [26,31]. Swadloon uses the accelerometer and gyroscope to obtain the direction of the acoustic source.

# 3. PRELIMINARY APPROACHES

# 3.1 Mapping from Doppler Effects to Motion

Our scheme is based on the relationship between Doppler effects and the relative motion from the phone to the acoustic source, when the phone moves and causes Doppler effects on the received acoustic waves. Suppose the acoustic source is emitting the sinusoidal signal at $\begin{array} { r } { f _ { r } = \frac { v _ { a } + v } { v _ { a } + v _ { s } } f _ { a } } \end{array}$ $f _ { a } ,$ , the observed frequency e v is the velocity of the $f _ { r } \ [ 2 8 ]$ iser; positive if the receiver is moving towards the source and negative in the opposite position. $v _ { s }$ is the velocity of the source and $v _ { a }$ is the traveling speed of the acoustic wave.

In this paper, we only consider the circumstance that the acoustic source is motionless or the velocity of the phone is far greater than the source, $i . e . , \ v \gg v _ { s }$ . As typically $v _ { a } \gg v _ { s } ,$ we simplify the computing of the frequency shift $f$ as follows:

$$
f = f _ {r} - f _ {a} = \frac {v - v _ {s}}{v _ {a} + v _ {s}} f _ {a} \approx \frac {v}{v _ {a} + v _ {s}} f _ {a} \approx \frac {f _ {a}}{v _ {a}} v (1)
$$

We also assume the acoustic source sends the consecutive sinusoidal acoustic wave at constant frequency $f _ { a } .$ To derive the relative displacement from Doppler effect, we assume that the received signal has the form:

$$
r (t) = A (t) \cos (2 \pi f _ {a} t + \phi (t)) + \sigma (t) \tag {2}
$$

where $A ( t )$ is the amplitude which changes continuously, φ(t) is the phase which is affected by the Doppler effect and $\sigma ( t )$ is the noise. Assuming $\phi ( t )$ is a continuous function, the observed frequency $f _ { r }$ at time t is fr(t) = 2π $\begin{array} { r } { f _ { r } ( t ) = \frac { 1 } { 2 \pi } \frac { d ( 2 \pi f _ { a } t + \phi ( t ) ) } { d t } = f _ { a } + \frac { \hat { 1 } } { 2 \pi } \frac { d \phi ( \tilde { t } ) } { d t } } \end{array}$ 1 d(2πfat+φ(t)) = fa + 1 d φ(t) . From Eq. (1), the frequency shift f at time t is

$$
f (t) = \frac {1}{2 \pi} \frac {d \phi (t)}{d t} \tag {3}
$$

From Eq. (1)(3), we get the velocity and displacement relative to the acoustic source:

$$
\left\{ \begin{array}{l} v (t) = \frac {v _ {a}}{2 \pi f _ {a}} \frac {d \phi (t)}{d t} \\ s (t) = \frac {v _ {a}}{2 \pi f _ {a}} \phi (t) - \frac {v _ {a}}{2 \pi f _ {a}} \phi (0) \end{array} \right. \tag {4}
$$

where $s ( t )$ is the relative displacement from the phone to the acoustic source. Specifically, $s ( t ) = L ( 0 ) - L ( t )$ , where $L ( t )$ is the distance between the phone and the source at time t. In Section 4.3, we further show how to calculate φ(t) in order to obtain v(t) and $s ( t )$ .

# 3.2 Basic Direction-Finding Using Doppler Effect for Simple Motion

We make a simple case of phone-to-phone direction finding to illustrate the intuition and challenges in designing Swadloon.

Assume that the phone and the acoustic source are at the same height and the mobile phone starts moving in north and in a path of rectangle with the constant velocity u1, u2, u3, u4 in each direction, shown in Figure 1a. So, frequency shifts are generated, where $f _ { i }$ corresponding to $u _ { i } .$ . If the velocities and the frequency shifts are obtained, from Eq. (1), we can calculate the direction in the following equations:

![](images/cdb4ae518722884805100c24bcd59e9bec8a04312acbb3af619ab40d9dc7c65b.jpg)



(a) Phone movement.

![](images/846db17cb47ba827f42a3a8c688b125feb9667c67d3c899c7cee1bc00e68a5a1.jpg)



(b) Error from motion.

![](images/1589f5cced396a855ad5617ea25aa5a4b94ca37fd6821566583595b2630ffacb.jpg)



(c) Velocity at north axis.

![](images/3852352130a1bd0c6d00cfc27def080b56b78156de5012a0765365ead9aa5732.jpg)



(d) FFT of received signal.   
Figure 1: A simple case of calculating the direction α. (a) The phone starts moving north and draw a rectangle. (b) The error $\alpha _ { e }$ and $d _ { e }$ caused by the movement of the phone. (c) The velocity calculated from the inertial sensors. (d) FFT on the received acoustic signal.

$$
\left\{ \begin{array}{l l} u _ {1} \sin \alpha = \frac {v _ {a}}{f _ {a}} f _ {1}; & u _ {2} \cos \alpha = \frac {v _ {a}}{f _ {a}} f _ {2}; \\ - u _ {3} \sin \alpha = \frac {v _ {a}}{f _ {a}} f _ {3}; & - u _ {4} \cos \alpha = \frac {v _ {a}}{f _ {a}} f _ {4} \end{array} \right. \tag {5}
$$

Intuitively from Eq. (5), if $u _ { 1 } = u _ { 2 } = u _ { 3 } = u _ { 4 } , f _ { 2 } >$ $f _ { 1 } > 0 > f _ { 3 } > f _ { 4 }$ , which indicates that $0 < \alpha < 4 5 ^ { o } .$ . Formally, only two equations are needed to calculate α if the velocity in one equation is not parallel to the other. The additional equations can improve the accuracy by using maximum likelihood estimation.

Note that α is changing while the phone is moving, so it will cause errors on calculating α. However, it won’t affect much on calculating the direction. In Figure 1b, if the initial distance from the phone to acoustic source is L and the maximum moving range of the phone is $d ,$ the maximum angle error is $\begin{array} { r } { \alpha _ { e } = \arcsin \frac { d } { L } } \end{array}$ . As the phone moves gently, we assume that d is 10cm at maximum. The maximum errors are $5 . 7 ^ { o } , \ 1 . 1 5 ^ { o } , \ 0 . 5 7 ^ { o } , \ 0 . 1 9 ^ { o }$ at $L = 1 , 5 , 1 0$ , 30m respectively, i.e., the errors get smaller when the distance becomes longer.

Moreover, if the phone calculates the position of acoustic source by not only the direction α according to Swadloon but also the distance L according to other techniques such as BeepBeep [21] while the measured L is accurate, the distance $d _ { e }$ from the calculated position to the actual position is de = 2L sin αe = 2L sin arcsin(d/L) . $\begin{array} { r } { d _ { e } = 2 L \sin \frac { \alpha _ { e } } { 2 } = 2 L \sin \frac { \arcsin ( d / L ) } { 2 } } \end{array}$ 2 When $d \ll L , \ e . g ,$ ., $1 0 d \leq L$ , arcsin $. ( d / L ) \approx ( d / \tilde { L ) }$ and sin $( d / 2 L ) \approx d / 2 L$ . So we simplify $d _ { e }$ as $d _ { e } \approx d .$ . Then the maximum error on computed location caused by shaking is close to the shaking distance $d ,$ which is acceptable in direction finding.

However, there are several problems on applying this simple approach. First, the accurate velocity of the phone is hard to be obtained by using the inertial sensors. Though it can be calculated by the accelerometer and other sensors if given the initial velocity of the phone, the errors of the acceleration will be accumulated on its integration, i.e., the calculated velocity. For instance in Figure 1a, the velocity is zero at the end of moving while the calculated one is $- 0 . 7 7 m / s$ in

Figure 1c. Second, the mobile phone and the acoustic source may not be of the same height. In this case, the calculated f is lowered and the equations in Eq. (5) are not right. Third, it would be hard and exhausting to draw the regular rectangle for the phone users. Fourth, the velocity of the phone v cannot be constant in each direction. So we need a more general solution in cases of different heights and arbitrary motion patterns.

Normally, the velocity increases and then decreases, as shown in Figure 1c. The rapid changes of v bring the difficulties on calculating the frequency shift f. Specifically, spectrum analysis, such as Fast Fourier Transform (FFT), is efficient in calculating f , if v is large or close to constant for a while. But FFT cannot measure the precise value of $f$ if v changes quickly due to the timefrequency resolution problem [8]. That is, for any signal, the time duration ∆T and the spectral bandwidth $\Delta F$ are related by $\Delta F \Delta T \geq 1$ . For example, in Figure 1d, we try to apply FFT on the received signal, where the frequency of the acoustic wave is $f _ { a } = 1 9 0 0 0 \mathrm { { H z } }$ , the sample rate is 44100Hz, and FFT size is 8192. So, the time resolution is $\Delta T = 8 1 9 2 / 4 4 1 0 0 \mathrm { H z } { = 0 . 1 9 s }$ . Then, the frequency resolution $\Delta F \ge 1 / \Delta T = 5 . 3 8 \mathrm { H z }$ . However, we assume that the maximum speed of a user’s hand is 2m/s [37]. The maximum frequency shift is $f _ { m a x } = 2 * 1 9 0 0 0 / 3 4 0 = 1 1 1 . 8 \mathrm { H z }$ . Even if the maximum speed is satisfied, the relative velocity may not reach $2 m / s .$ . For instance, when the maximum speed of phone is about 2m/s shown in Figure 1c, for the phone never moves towards directly to the acoustic source, the maximum frequency shift is about 60Hz in Figure 1d, which corresponds to the relative velocity $v = 1 . 1 m / s$ . Furthermore, in our circumstance, we only require that the user shakes the phone gently, so most of the time the frequency shift is far less than 111.8Hz. The resolution $\Delta F _ { \ l }$ , which is more than 5.38Hz, is not precise enough to measure the frequency shift.

Hence, if the relative velocity and corresponding frequency shift are close to constant for a period, designers can increase $\Delta T$ to get better frequency resolution by FFT. However, in our circumstance, the velocity is always changing, which requires that both ∆T and ∆F is small enough, to get more precise f at smaller time block. Hence, it is in conflict with the time-frequency resolution problem of FFT for estimating $f .$

Besides the challenge of calculating the frequency shift $f ( t )$ for direction finding, the further problem is calculating the phase shift φ(t), from which f (t) can be obtained by Eq. (3). We also show that the real-time indoor tracking can be implemented by using φ(t) in Section 5.2.

# 4. ACOUSTIC DIRECTION FINDING

In this section, we present the acoustic direction finding component of Swadloon. We show the design of Swadloon in Figure 2. The phone gathers samples from the microphone, gyroscope and the accelerometer, when the user shakes the phone or walks in an arbitrary path. The data are processed in real time to maximize the utilization of the CPU. The phone dynamically updates the direction of the source according to the previous calculated samples.

In Figure 2, The noise $\sigma ( t )$ and variational amplitude $A ( t )$ in Eq. (2) is eliminated by BPF and AGC respectively. The phase $\phi$ and frequency $f$ are then obtained by PLL. Swadloon further combines the velocity from the acoustic and inertial sensor samples to get the source direction α in LR. The phone returns the value of α and $\phi$ in real time for direction finding, indoor localization or tracking. We describe each component of the design as follows.

![](images/15310b207d31ad60163dd34a514534297a561abda2f8c23289b37ecde9c2bbc4.jpg)



Figure 2: Implementation of Swadloon.

# 4.1 Band Pass Filter (BPF)

To get rid of the interference of other acoustic waves, we assume the phones of different users send acoustic waves in different frequency bands. Hence, in our implementation, the acoustic sample first walks through the Band Pass Filter (BPF) such that only the waves at the specific frequency pass through BPF. The interference by other acoustic sources and the low frequency noises that human can hear are both eliminated.

Note that the type of BPF should be carefully chosen. All frequency components of a signal are delayed when passed through BPF. As the frequency is changing in Doppler effect and we need to get the precise phase, the delay at each frequency components must be constant, such that the different frequency component will not suffer distortion, which is known as the linear phase property. As a result, we choose equiripple FIR filter, which satisfies the linear phase property.

Meanwhile, the bandwidth should be wide enough to get the total signal. Normally, the maximum speed of shaking the phone is less than $\mathrm { 2 m / s }$ . Thus, if the frequency of acoustic signal is $f _ { a } = 1 9 0 0 0 \mathrm { { H z } }$ , the maximum frequency shift $f _ { m a x } = 1 1 1 . 8 \mathrm { H z }$ . So, the minimum pass band of the filter is 223.6Hz. For avoiding the interference by other acoustic sources, there should not be multiple signals that pass through the same BPF. Besides, acoustic bandwidth that the almost all the smartphones support is limited with maximum of 22050Hz (i.e., sample rates of 44100Hz) and we find that the lowest frequency that human can hardly hear is about 17000Hz in our experiment. Thus, the maximum number of acoustic sources that can sound simultaneously in a small area (with radius about 30m) and be successfully detected is limited to $( 2 2 0 5 0 - 1 7 0 0 0 ) / 2 2 3 . 6 \approx 2 3$ . However, this is not a challenge for Swadloon as we show that we only need a small number (less than 10) of acoustic sources in a small area for high accuracy. Though there are possible ways to allow more simultaneous acoustic waves such as dividing the signal into different time slots, like TDMA in shared medium network, it is beyond the scope of this paper.

# 4.2 Automatic Gain Control (AGC)

We adjust the filtered data by Automatic Gain Control (AGC) such that the amplitude of the acoustic signal A(t) in Eq. (2) is replaced by another one that is close to constant. The purpose is to let the magnitude of $( \theta [ k + 1 ] - \theta [ k ] )$ in Eq. (8) only be determined by $\mu ,$ rather than $A ( t )$ , which is discussed in Section 4.3. We adopt the design of AGC from [27]. Suppose $T _ { s }$ is the sampling period of the received signal and $k$ is the step count of sampling, then $t = k T _ { s }$ . The main idea is for the input $r _ { b } [ k ]$ from BPF, we estimate the amplitude $A [ k ]$ in Eq. (2) by updating A1[k] with the equation:

$$
\log (A _ {1} [ k ]) = (1 - A _ {\alpha}) \log (A _ {1} [ k - 1 ]) - A _ {\alpha} \log (A _ {r} [ k - 1 ])
$$

Here $A _ { \alpha }$ represents the sensitivity for adjusting $A _ { 1 } [ k ]$ . $A _ { r } [ k ]$ resents the coaplementation, $A [ k ]$ $\begin{array} { r } { A _ { r } [ k ] = \frac { 1 } { 7 } \sum _ { i = k - 1 0 } ^ { k } | r _ { b } [ i ] | } \end{array}$ $A _ { \alpha } = 0 . 9$ $r _ { b } [ k ]$ output

$$
r _ {c} [ k ] = A _ {1} [ k ] r _ {b} [ k ]
$$

For the amplitude of $r _ { c } [ k ]$ is close to constant by AGC, if $A _ { 1 } [ k ] = A _ { 1 } [ k - 1 ] , A _ { 1 } [ k ] A _ { r } [ k - 1 ] = 1$ . Thus, the amplitude of $r _ { c } [ k ]$ is close to 1. Hence, we get $r _ { c } ( t ) \approx \cos ( 2 \pi f _ { a } t + \phi ( t ) )$ , where $\sigma ( t )$ and $A ( t )$ in Eq. (2) is eliminated by BPF and AGC respectively.

# 4.3 Phase Locked Loop (PLL)

According to $\operatorname { E q . }$ (4), we use Phase Locked Loops (PLL) to calculate the phase $\phi ( t )$ , in order to get the precise relative displacement $s ( t )$ and velocity $v ( t )$ of the phone. PLL can be thought as a device that tracks the phase and frequency of a sinusoid [27]. In software implementation, we draw the idea from [10]. To get the precise $\phi ( t )$ , we update an adaptive estimation of $\phi ( t )$ in real time, denoted as $\theta ( t )$ in order that $\theta ( t )$ ≈ $\phi ( t )$ . To make θ converge to φ after enough iterations, we define the corresponding function $J _ { P L L } ( \theta )$ such that $J _ { P L L }$ converges to its maximum at the same time. Specifically, $\theta ( t )$ is updated in the iterations as:

$$
\theta^ {\prime} = \theta + \frac {d J _ {P L L}}{d \theta} \tag {6}
$$

As a result, $J _ { P L L }$ should satisfy that

$$
\max (J _ {P L L} (\theta)) = J _ {P L L} (\phi) \tag {7}
$$

In Swadloon, we choose $J _ { P L L }$ as follows:

$$
{J _ {P L L} (\theta)} = {\mathrm{LPF} \{r _ {c} (t) \cos (2 \pi f _ {a} t + \theta (t)) \}}
$$

$$
\approx \frac {1}{2} \mathrm{LPF} \{\cos (\phi (t) - \theta (t)) \}
$$

Here, LPF is the Low Pass Filter which excludes the high frequency component in the above approximation. Hence, $J _ { P L L }$ satisfies Eq. (7).

Next, we need to change the continuous estimation process of Eq. (6) to the discrete one. Assuming a small step size, the derivation in Eq. (6) with respect to $\theta$ at $k T _ { s }$ can be approximated1:

$$
\begin{array}{l} \frac {d J _ {P L L}}{d \theta} \approx \mathrm{LPF} \{\frac {d [ r _ {c} [ k ] \cos (2 \pi f _ {a} k T _ {s} + \theta)) ]}{d \theta} \} \bigg | _ {\theta = \theta [ k ]} \\ = - \mathrm{LPF} \left\{r _ {c} [ k ] \sin \left(2 \pi f _ {a} k T _ {s} + \theta [ k ]\right) \right\} \\ \end{array}
$$

As a result, the estimating of $\theta ( t )$ is shown as follows:

$$
\theta [ k + 1 ] = \theta [ k ] - \mu \mathrm{LPF} \{r _ {c} [ k ] \sin (2 \pi f _ {a} k T _ {s} + \theta [ k ]) \} (8)
$$

where $\theta [ k ] = \theta ( k T _ { s } )$ and $\mu$ is a small positive value. Hence, $\phi [ k ] \approx \theta [ k ]$ after enough iterations. According to $\mathrm { E q . \ ( 4 ) }$ , if the max velocity of the phone is $v _ { m a x } =$ $2 m / s , f _ { s } = 4 4 1 0 0 \mathrm { H z }$ and $f _ { a } = 1 9 0 0 0 \mathrm { { H z } }$ , the max offset per sample $\begin{array} { r } { | \Delta \phi _ { m a x } | = \frac { 2 \pi f _ { a } } { v _ { a } f _ { s } } v _ { m a x } = 0 . 0 1 6 } \end{array}$ . Besides,

$$
r _ {c} [ k ] \sin (2 \pi f _ {a} k T _ {s} + \theta [ k ]) \approx \frac {1}{2} \sin (4 \pi f _ {a} k T _ {s} + 2 \theta [ k ]) \leq \frac {1}{2}
$$

Thus, $\mu > 0 . 0 3$ in Eq. (8), otherwise, the transition rate of $\theta [ k ]$ cannot catch up with the real phase. Furthermore, as $\begin{array} { r } { \frac { 1 } { 2 } \sin ( 4 \pi f _ { a } k T _ { s } + 2 \theta [ k ] ) } \end{array}$ cannot always be $1 / 2$ , µ needs to be much more than 0.03 to let $\theta [ k ]$ converge to $\phi [ k ]$ . However, when $\mu$ is bigger, the calculated

phase is more sensitive to noises, and cannot be precise either. Hence, there is a trade off on choosing the $\mu .$ . In the implementation, we choose $\mu = 0 . 0 3$ .

# 4.4 Leveraging Sensors

The acceleration in world coordinate system (WCS) is calculated by using accelerometer and gyroscope of the phone. As compass is not accurate, we make the following implementation to avoid the error of compass. The accelerometer records the 3D acceleration in user’s phone coordinate system (UCS). So, we convert the acceleration in UCS to the one in WCS as follows: 1) On initialization, by leveraging the force of gravity of the earth [3], the $\mathrm { Z }$ axis in WCS is calculated by the accelerometer. Typically Z axis is accurate. The X axis in WCS is computed from the values of compass and gyroscope, which is supposed to point to the east but often has large errors due to noisy data. 2) After initialization, the conversion function is updated by using the gyroscope.

Hence in our WCS, the Z axis is considered to be accurate, but the X axis may not point to east. $\mathrm { S o } .$ , the calculated direction α in WCS may not be the actual direction relative to the east. To evaluate the performance of our direction finding, we will evaluate the direction (denoted as $\alpha _ { r } )$ of the acoustic source using the UCS of the phone that is placed horizontally such that its Z axis is same as the Z axis of WCS, as shown in Figure 4a. When phone is static, the value $\alpha _ { r }$ does not change. Thus, in Section 6.1, we measure $\alpha _ { r }$ to evaluate the precision of direction finding shown in Figure 4b.

Hence, suppose the phone is horizontal, we get value α by using Swadloon and the opening angle from X axis in UCS to the one in WCS $\left( \alpha _ { 0 } \right)$ by using the transform function from UCS to WCS. $\alpha _ { r }$ is calculated by

$$
\alpha_ {r} = \pi / 2 - \alpha - \alpha_ {0} \tag {9}
$$

# 4.5 Getting Direction by Linear Regression (LR)

Assuming the direction vector of the acoustic source relative to the phone is $\vec { \lambda } = ( \lambda _ { x } , \lambda _ { y } , \lambda _ { z } )$ and velocity vector of the phone is $\vec { \boldsymbol { u } } = ( v _ { x } , v _ { y } , v _ { z } )$ , then $\vec { u } \cdot \vec { \lambda } =$ $\textstyle { \frac { v _ { a } } { f _ { a } } } f$ according to Eq. (1). For the obtained array ${ \vec { u } } [ k ]$ and $f [ k ]$ , they satisfy the following equations

$$
\lambda_ {x} v _ {x} [ k ] + \lambda_ {y} v _ {y} [ k ] + \lambda_ {z} v _ {z} [ k ] = \frac {v _ {a}}{f _ {a}} \cdot f [ k ], \quad \forall k \tag {10}
$$

Hence, the 3D direction $\vec { \lambda }$ can be obtained by solving these equations using linear regression, where $f [ k ]$ can be calculated by Eq. (3), Eq. (8). Ideally, if $u [ k ]$ is obtained from inertial sensors and there are no errors of $u [ k ]$ , there are 3 unknowns $\lambda _ { x } , \lambda _ { y } , \lambda _ { z }$ in the equation set. Moreover, using this we can calculate the direction when the phone moves in arbitrary paths, because different motion patterns of the phone merely causes different array $\Vec { u } [ k ]$ and $f [ k ]$ .

We can also translate 3D direction $\vec { \lambda }$ to 2D direction α as follows:

$$
\alpha = \left\{ \begin{array}{l l} \arcsin \frac {\lambda_ {y}}{\sqrt {\lambda_ {x} ^ {2} + \lambda_ {y} ^ {2}}} & \lambda_ {x} \geq 0 \\ \pi + \arcsin \frac {\lambda_ {y}}{\sqrt {\lambda_ {x} ^ {2} + \lambda_ {y} ^ {2}}} & \lambda_ {x} <   0 \end{array} \right. \tag {11}
$$

We now address non-ideal circumstance with noisy sensor data, i.e., to minimize the error of velocity which is derived from the calculated acceleration in WCS. In phone-to-phone direction finding and indoor localization, we only need the 2D direction α rather than the 3D direction $\left( \lambda _ { x } , \lambda _ { y } , \lambda _ { z } \right)$ . Thus, $\lambda _ { z }$ is not needed. From Eq. (10), if $\lambda _ { z } v [ k ] \approx 0$ , i.e., the phone moves in a horizontal plane or the two phones are at the same height approximately, we can calculate the direction by the following equation to eliminate the error of $v _ { z } .$

$$
\lambda_ {x} v _ {x} [ k ] + \lambda_ {y} v _ {y} [ k ] = \frac {v _ {a}}{f _ {a}} \cdot f [ k ] \tag {12}
$$

Suppose $\hat { a } _ { x } [ i ] = a _ { x } [ i ] + \sigma _ { x } [ i ]$ where $\hat { a } _ { x } [ i ] , a _ { x } [ i ] , \sigma _ { x } [ i ]$ is the real acceleration, the calculated acceleration, the error of the calculation on the acceleration of the ith sample respectively. We can derive $v _ { x }$ from

$$
v _ {x} [ k ] = v _ {x} [ 0 ] + \sum_ {i = 0} ^ {k - 1} T [ i ] a _ {x} [ i ] + \sum_ {i = 0} ^ {k - 1} T [ i ] \sigma_ {x} [ i ]
$$

where $T [ i ]$ is the time interval from $a _ { x } [ i ]$ to $a _ { x } [ i + 1 ]$ .

The error $\sigma _ { x }$ is related the natural quality of the inertial sensors and challenging to be measured. In this paper, we simply assume at a short period. Suppo $\sigma _ { x }$ stant , we $e _ { x }$ $\begin{array} { r } { t [ k ] = \sum _ { i = 0 } ^ { k - 1 } T [ i ] } \end{array}$ $\begin{array} { r } { \sum _ { i = 0 } ^ { k - 1 } T [ i ] \sigma _ { x } [ i ] = e _ { x } t [ k ] } \end{array}$ . Similarly, we also assume the error of $a _ { y }$ is a constant $e _ { y }$ at a short period.

As a result, from Eq. (9)(11)(12), we could calculate the 2D direction by linear regression from the following equation set which has 4 unknowns $( \lambda _ { x } , \lambda _ { y } , \lambda _ { 0 } , \lambda _ { 1 } )$

$$
\left( \begin{array}{c c c c} w _ {x} [ 0 ] & w _ {y} [ 0 ] & 1 & t [ 0 ] \\ w _ {x} [ 1 ] & w _ {y} [ 1 ] & 1 & t [ 1 ] \\ \dots & \dots & \dots & \dots \\ w _ {x} [ n ] & w _ {y} [ n ] & 1 & t [ n ] \end{array} \right) \left( \begin{array}{c} \lambda_ {x} \\ \lambda_ {y} \\ \lambda_ {0} \\ \lambda_ {1} \end{array} \right) = \frac {v _ {a}}{f _ {a}}. \left( \begin{array}{c} f [ 0 ] \\ f [ 1 ] \\ \dots \\ f [ n ] \end{array} \right)
$$

where $\begin{array} { r } { w _ { x } [ k ] = \sum _ { i = 0 } ^ { k - 1 } T [ i ] a _ { x } [ i ] , w _ { y } [ k ] = \sum _ { i = 0 } ^ { k - 1 } T [ i ] a _ { y } [ i ] . } \end{array}$ 1 $\lambda _ { 0 } = \lambda _ { x } v _ { x } [ 0 ] + \lambda _ { y } v _ { y } [ 0 ]$ and $\lambda _ { 1 } = \lambda _ { x } e _ { x } + \lambda _ { y } e _ { y }$ . Note that, we allow that $v _ { x } [ 0 ] \ \neq \ 0$ and $v _ { y } [ 0 ] \ \ne \ 0$ in our solution, which means we don’t require the phone to be motionless before shaking the phone and calculating the direction. $v _ { x } [ 0 ]$ and $v _ { y } [ 0 ]$ are put together as an unknown $\lambda _ { 0 }$ in the equation.

# 5. INDOOR LOCALIZATION & TRACKING

We now describe our basic method in Swadloon for fine-grained indoor localization illustrated in Figure 3a, which is based on the direction α and the phase φ in Section 4. We require that there are at least three acoustic sources as anchor nodes installed, which send sinusoid signals at the specific different frequencies. Users need to get the position and frequency of each anchor node from network service. Swadloon includes two phases: finding the initial position and real-time tracking.

![](images/d6022020536776f26a7ec396474cea2c34a85ed2a08df6ebd7ea97e5f06e7d4b.jpg)



(a) WCS vs. UCS

![](images/828ac72f9d002fbd50e7b07b4874b39c0d209eaac48305699b6cfd49138acbcd.jpg)



(b) Experiment setup   
Figure 4: (a) WCS vs. UCS when the phone is horizontal. (b) Experiment of direction finding.

# 5.1 Finding the initial position

The user needs to shake the phone first in order to get his/her initial position. The phone calculates the direction of each anchor node in WCS and then gets the position. Note that as the compass is not precise, the calculated directions, such as $\alpha _ { 1 }$ , $\alpha _ { 2 }$ in Figure 3a, are not directly used in calculating the position. However, observe that the opening angle $\left( \alpha _ { 1 } - \alpha _ { 2 } \right)$ is fixed no matter which WCS is chosen. We calculate the initial position using this opening angle. Taking the positions $( x _ { 1 } , y _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } )$ of two anchor nodes $A _ { 1 }$ and $A _ { 2 }$ and the relative directions $P A _ { 1 } , P A _ { 2 }$ from phone (with unknown position P ) to $A _ { 1 }$ and $A _ { 2 }$ , we can compute the distance $D = \| A _ { 1 } - A _ { 2 } \|$ and the opening angle $\alpha _ { d } =$ $\angle A _ { 1 } P A _ { 2 }$ , as illustrated in Figure 3a. It can be inferred that the position $P$ is on a fixed circle illustrated in Figure 3b, 3c. If $\alpha _ { d }$ is a cute angle as in Figure 3b, αc = 2αd. So, the radius of the circle R = D2 sin αd $\alpha _ { c } = 2 \alpha _ { d }$ $\begin{array} { r } { R = \frac { D } { 2 \sin \alpha _ { d } } } \end{array}$ . Then we get at most two possible solutions of the position of the circumcenter O by using radius R and the given coordinates of two nodes $A _ { 1 }$ and $A _ { 2 }$ . If $\alpha _ { d }$ is a cute angle, then O and P are on the same side of $A _ { 1 } A _ { 2 }$ . Similarly, if $\alpha _ { d }$ is an obtuse angle, as in Figure 3c, O and P are on the opposite side of $A _ { 1 } A _ { 2 }$ .

For a system of n anchor nodes, there are $\textstyle { \frac { n ( n - 1 ) } { 2 } }$ pairs of anchor nodes. As a result, phone P lies on $\textstyle { \frac { n ( n - 1 ) } { 2 } }$ circles. Thus, with at least 3 anchor nodes, we can get the position of P . It is worth mentioning that for the circle formed by a node pair, the circle is divided into two arcs by the node pair. Node P only lies on one of the arcs, depending on whether $\alpha _ { d }$ is an acute angle or an obtuse angle. Hence, for localization we search for the point P to minimize $\textstyle \sum _ { i } d _ { i }$ where $d _ { i }$ is the distance from P to the ith arc.

We claim that it will result in better localization accuracy if we place the anchor nodes in a line as in Figure 3d compared to the one in Figure 3e. In Figure 3e, the centers of the circles are too close, which causes big potential errors. The root reason is that the 4 points $A _ { 1 }$ , $A _ { 2 } , A _ { 3 } , P$ are nearly at the same circle, which means the arbitrary point, $e . g . , A _ { 1 }$ , is close to the circle which is constructed by the rest of 3 points, $e . g . , A _ { 2 } , A _ { 3 } , P .$

![](images/2553427ace720a73d9594444ff7526a0c82e53c6bd40fef0094c9af65446a0ae.jpg)



(a) Trilateration

![](images/f5e5e9d94b7cfa5a8dec15436009fc93e1d988ac4d00b6521d54772e22bece3f.jpg)  
(b) Acute Angle

![](images/2c1e44f35237b47340887c1097b3d53648328ad40a8e51a90256480dc54ccb16.jpg)



(c) Obtuse Angle

![](images/6f44db14f58436bf9f33480762c4446b7970f33910f124ffd659a82377d06a70.jpg)



(d) Good layout

![](images/ffb40d51d9900f50eac6883da8a8c716779c0b47dea336dcf3cdcbc90fc60ac1.jpg)



(e) Bad layout   
Figure 3: Indoor localization and tracking: trilateration, pinpoint candidate location to a circle (acute angle and obtuse angle), and impact of layout of anchors (good and bad).

# 5.2 Real-time tracking

After getting the initial location of phone, the phone then gets the real-time location by calculating the relative displacement to each anchor node without shaking the phone again. In Figure 3a, if the location of phone at time t has been calculated, denoted as $( x , y )$ , we calculate its location $( \tilde { x } , \tilde { y } )$ at the latter time t˜ by getting $s ( t )$ and $s ( \widetilde t )$ using Eq. (4), Eq. (8). Then we calculate next location according to $( \tilde { x } , \tilde { y } )$ iteratively. Specifically, if the user gets the location $( x , y )$ , then the distance from $( x , y )$ to $( x _ { i } , y _ { i } )$ is $L _ { i } = { \sqrt { ( x - x _ { i } ) ^ { 2 } + ( y - y _ { i } ) ^ { 2 } + h _ { i } ^ { 2 } } }$ where $h _ { i }$ is the relative height between the phone and the source $( x _ { i } , y _ { i } )$ . Thus, s/he gets the distances from all the available acoustic sources at time t. According to Eq. (4), Eq. (8) and the definition of $s _ { i } ,$ we have

$$
\tilde {L} _ {i} = L _ {i} - \frac {v _ {a}}{2 \pi f _ {a}} (\tilde {\phi} _ {i} - \phi_ {i}) \tag {13}
$$

where $\tilde { L _ { i } } ~ = ~ L _ { i } ( \tilde { t } )$ and $\tilde { \phi } _ { i } ~ = ~ \phi _ { i } ( \tilde { t } )$ . Then we search for location $( \tilde { x } , \tilde { y } )$ near $( x , y )$ to minimize $\textstyle \sum _ { i } M _ { i }$ where $M _ { i } = \left| \tilde { L _ { i } } - \sqrt { ( \tilde { x } - x _ { i } ) ^ { 2 } + ( \tilde { y } - y _ { i } ) ^ { 2 } + h _ { i } ^ { 2 } } \right|$ .

# 6. EXPERIMENT

We implement Swadloon on Nexus 7, where all the components, including BPF and PLL, are implemented by using Android APIs. The audio sample rate is 44100Hz, and sample rate of the gyroscope and accelerometer is 200Hz.

# 6.1 Phone-to-phone Direction Finding

# 6.1.1 Experiment Design

The vertical view of the phone and acoustic source is shown in Figure 4b. The distance between the phone and the acoustic source is L. The orientation angle of the phone and acoustic source at the horizontal plane is $\alpha _ { r }$ and $\beta$ respectively. There are reference objects at places A, B, C which are used to align the phones. The place C is used to put new acoustic source for further experiment. Additionally, we assume elevation angle of the acoustic source is $\gamma$ which is not shown in this 2D figure. The acoustic source is on the floor, the height of phone from the floor is about 40cm.

The main process of evaluating performance of direction finding is as follows: we vary $L , \alpha _ { r } , \beta , \gamma$ by moving the reference objects. We obtain the measured direction $\alpha _ { r }$ by shaking the phone, aligning the phone to the reference object, and reading the direction value from the phone. We measure $\alpha _ { r }$ 50 times for each configuration.

# 6.1.2 Empty Room with Single Acoustic Wave

We first conduct the experiment in a large empty room for examining the accuracy of direction finding when there is only single acoustic wave. The sound pressure of the room is −41 dBFS (about 30 dB SPL) measured by Nexus 7. The amplitude of the acoustic source at the distance of 1m is −20 dBFS.

Effect by L and $\alpha _ { r }$ . The cases we mostly care about is the performance when the distance L and the orientation of the phone $\alpha _ { r }$ is changing. Hence, we set $\beta = 0$ and $\gamma = 0$ , and plot the standard deviations and cumulative distribution function (CDF) of the angular errors when $L$ and $\alpha _ { r }$ are changed in Figure 5.

![](images/382cce2abc07794db1cd51ca61c02d1007b06d8c2f8128241c60dafe1bc9462f.jpg)



(a) Angle (degree)

![](images/5591d5f0c969f74e9a9653da68af9037a6a27c4d89a7a27168d5884c0c4a508c.jpg)



(b) Angular Error (degree)   
Figure 5: The result of direction finding in an empty room when $\beta = 0$ and $\gamma = 0$ .

The key observation is that the measurement is very precise when $L \ \leq \ 3 2 m$ . We examine the reason in Figure 6, which plots the calculated φ(t) on random samples with different L values. The calculated $\phi ( t )$ is always smooth when $L \leq 2 4 m$ , while there are small noises when $L = 3 2 m$ and much bigger noises if $L =$ 40m. Hence, the calculated related displacement and velocity become much less precise when $L = 4 0 m$ , which affects the calculation of direction. It is similar that most of the following cases mainly affect the calculated phase which finally affect the precision of direction finding.

![](images/4ec854b6662dc88ef4ad9b1d7a997d740b02f1c5f3f7b921eb62421d77ce628a.jpg)



Figure 6: The calculated phase φ(t).

When $L \leq 3 2 m$ , the mean error and standard deviation of the measurement is 2.10o and 2.66o. The angular errors are within 2.06o, 4.43o, 5.81o at 50%, 90%, 95% respectively. Though the errors become larger when $L = 4 0 m .$ , it is still acceptable. We also test angle errors when L > 40m, but it becomes much unstable as the signal is too weak. So we do not show the result of this case.

We also find that $\alpha _ { r }$ has little effect on precision according to Figure 5a. As the errors are so close for different $\alpha _ { r } ,$ we don’t show the CDF of different $\alpha _ { r }$ .

Effect by β and γ. We test the errors when the orientation of the acoustic source is not directly pointing to the phone. In this case, we set $\alpha _ { r } = 4 5 ^ { o }$ . In Figure 7a, 7b, we show the mean and standard deviation with different choices of $\beta , \gamma , L$ .

It shows an interesting result that when β changes, the mean value changes more in L = 8m than the one in $L = 3 2 m$ . The main reason is that the acoustic source we choose is not omnidirectional, and the signal is much stronger right in front of the source. The signal reflected from the wall affects the result, which is so-called the multipath effect. When the phone is further from the source, the signal reflected from the wall becomes much weaker than the one directly from the acoustic source.

Another observation is that if the phone turns up, such as $\gamma ~ = ~ 4 5 ^ { o } , ~ 6 0 ^ { o }$ , 90o, the mean value will not change a lot no matter $L = 8 m$ or $L = 3 2 m$ . That is, though there is multipath from the ceiling, it has little effect on the mean direction. We find a new phenomenon on multipath effect in latter experiment, which explains these observations here.

Motion Pattern. We also analyze the angular errors caused by the inertial sensors. As we claim that Swadloon supports arbitrary pattern of phone movement, we test errors caused by different motion patterns of the phone. In this case, we set $L = 3 2 m , \alpha _ { r } = 4 5 ^ { o }$ , $\beta = \gamma = 0$ .

![](images/6e5434750607e38af44d3b2a40d91f63e549118a210a253e1787d3bcb7c5fa6b.jpg)



Figure 8: Basic phone motion patterns.

We define several motion patterns in Figure 8. Pattern A is the default basic pattern used in the whole experiment. The pattern A is a mix of rectangle and circle. The pattern B, C, D is the circle, the rectangle, and the arbitrary pattern respectively. We shake the phone with the basic patterns anti-clockwise or clockwise for a few times and get the result in Figure 7c. The first motion pattern of this figure, named A-caca, means we shake the phone 4 times in basic pattern A: clockwise, anticlockwise, clockwise, anticlockwise. The rest of the patterns can be explained similarly.

First of all, we found the result of arbitrary pattern D is still acceptable in $L = 3 2 m \colon$ the standard deviation of the measurement is 4.96o. Another important observation is that, when the phone moves clockwise, there is a positive shift on the mean value. When the phone moves anti-clockwise, there is a negative shift. For the pattern D, there are both positive and negative shifts in the measurement, so the standard deviation becomes a little bigger. We also observed that when the phone was shaken in other regular patterns compared to pattern D, the standard deviation becomes smaller. That is, the error shift is close to constant in these cases. We also find that when we shake the phone in A-caca, Cca, the means are close to same. We leave it as a future work to understand why the phenomena happen.

Non-line of sight. We set $L = 8 m , \alpha _ { r } = 4 5 ^ { o } , \beta =$ $\gamma = 0 ,$ , and test a simple case on the effect by Nonline of sight (NLOS). In Figure 7d, a person stands between the phone and acoustic source, and we measure the errors related to the distance from the person to the phone. It becomes apparent that when the person stands in either ends, the standard deviation is enlarged, while the person stands in the middle, it is close to the one without obstruction. Hence, the person has little effect on direction finding, as long as s/he is not too close to the acoustic source or the receiver. This is also verified in the experiment of noisy environment.

Another case of NLOS is that the user put his back to the source. The signal turns so weak and the result becomes unstable. In this case, the user can turn around to get the precise direction. The other possible complementory method is to let user rotate the phone around the user’s body, similar to [38].

![](images/efd67b9269adb95100153feb5cc3ee25b069f3156ba538efed05c1524985be33.jpg)  
Figure 7: Effect by (a) $\beta$ and γ when $L = 8 m$ (b) $\beta$ and $\gamma$ when $L = 3 2 m$ (c) motion pattern (d) non-line of sight (e) man-made multipath (f) multipath from the wall.

Multipath effect. As the multipath effect is hard to measure exactly, we first make a man-made multipath to find its impact. Then, we make a simple real case to verify our finding.

We set $L = 8 m , \alpha _ { r } = 4 5 ^ { o } , \beta = \gamma = 0$ and add another phone as acoustic source placed at position C in Figure 4b. The new source is also 8 meters from the phone. It beeps at the same frequency with the source at B. The volume of the source at B is constant 60%. We change the volume of the source at C from 0% to 100%, and plot the Figure 7e. When the volume is less than 20%, it has little effect: the standard deviation is low, and the mean value is slightly lowered. There is an interesting phenomenon that when the volume becomes larger, the angle becomes lower which is close to the direction of the new source. However, the standard deviation becomes bigger when both sources have high volume.

We then conduct experiment with both acoustic source and phone near the wall. The wall is on the right hand side of the user while shaking the phone. We set $\alpha _ { r } = \beta = \gamma = 0$ and $L = 8 , 1 6 , 2 4 , 3 2 m$ . The result is shown in Figure 7f. $\alpha _ { r }$ becomes bigger for all the distances which can be inferred from the above conclusion. It can also be inferred that the strengths of the reflected signals relative to the respective direct signals are different at each L, which causes different mean shifts of $\alpha _ { r } .$ . The other observation is that the standard deviation is low for each distance. Hence, reflected signal is weak compared to the one directly from the acoustic source.

# 6.1.3 Empty Room with Multiple Acoustic Waves

To validate the robustness of Swadloon, we conduct two types of experiments: (1) an acoustic source broadcasts multiple signals at different frequencies, (2) multiple sources broadcast signals at different frequencies.

In experiment (1), we measure the angular errors when the acoustic source sends 6 sinusoidal signals at the frequency from 17000Hz to 19500Hz. The experiment is performed by setting $\alpha _ { r } = \beta = \gamma = 0$ . We find that the results are similar for different L that $L \leq 2 4 m ,$ while the ones at $L = 3 2 m$ are a little worse. It is because that when the phone sends multiple signals, the signal strength of each component becomes weaker. We plot the CDF at $L \leq 2 4 m$ in Figure 9a. The performance is almost the same with the one sending single wave. It can be inferred that we can use loudspeakers in the mall as anchor nodes while they are playing music.

![](images/9285858d62915865edc15b1b011e5cd4627960ee59c36752fd9502b0651ccf51.jpg)



![](images/7892749d93b4aebfeb4e11ceb579f4b8c0bcc9e9d3b5d5c5de5919b4dcac78c3.jpg)



Figure 9: (a) Errors on different cases when $L \leq$ 24m, $\alpha _ { r } = \beta = \gamma = 0 .$ . (b) The opening angle errors when there are multiple signals.

We now analyze the performance of direction finding when there are multiple acoustic sources. The performance in this case will have direct impact on the accuracy of the localization to be studied later in Subsection 6.2.2. Recall that as the computing of the absolute direction requires the accurate compass which is hard to get, in our localization method we use the opening angle $\angle A _ { i } P A _ { j }$ from the phone with location $P$ to two arbitrary anchor nodes $A _ { i }$ and $A _ { j }$ instead of the absolute orientation of any vector $P A _ { i }$ or $P A _ { j }$ . Thus, here we measure the accuracy of estimated angle $\angle A _ { i } P A _ { j }$ by varying the locations of $P , A _ { i } ,$ and $A _ { j }$ .

Figure 9b shows the opening angle errors in three cases: (1) single source, multiple waves, super market, (2) single source, multiple waves, empty room, (3) multiple source, multiple waves, empty room. We find that the opening angle errors in cases (1), (2) are less than the direction errors in Figure 9a. Furthermore, we observe that case (3) is much worse than (2). Though it is unfair to compare the two cases that the acoustic sources are different, it shows the possibility of improvement on the precision of indoor localization by using better acoustic sources, as we use the worse case for calculating the latter position.

# 6.1.4 Noisy Environment

We conduct this experiment in a super market, where it is noisy (−21 dBFS) and there are people walking around and blocking the line from the acoustic source to the phone. We also let the phone send multiple signals. In Figure 9, the result becomes a little worse than the one in empty room. Almost all errors are less than 10 degrees, which is acceptable.

# 6.1.5 Overhead

As Swadloon calculates the direction in real time, we only evaluate the CPU usage. When Swadloon processes one acoustic signal, the CPU usage is 20.5%. When it process 6 signals at the same time, the CPU usage of this application is 95.25% and it takes the phone 3.9 seconds to process 1 second of signal samples on average. The main cost for computation is the Band Pass Filter (BPF). We choose the FIR filter to achieve linear phase property as discussed earlier. However, the computation overhead is much higher than IIR filters. When there are multiple signals, we need to shorten the bandwidth of the filter, which costs more computation overhead. So there is a trade-off between processing speed and accuracy: we can enhance the speed by using IIR filter by sacrificing a little accuracy. In fact, as we only need to shake the phone for a short duration to get the directions, the overhead is not the key problem.

# 6.2 Real-time Indoor Localization

# 6.2.1 Experimental setup

In Figure 11, we place 6 phones as anchor nodes in the same empty room in the previous subsection. The positions are $( 0 , - 3 ) , ( 6 , 0 ) , ( 1 2 , 0 ) , ( 1 8 , 0 ) , ( 2 4 , 0 ) , ( 3 0 , - 3 )$ (meters) respectively. The beep frequencies are from 17000 to 19500Hz. We choose spots at $y \in \{ - 3 , - 6 \}$ and $x \in \{ 6 , 9 , 1 2 , 1 5 , 1 8 , 2 1 , 2 4 \}$ . We conduct the localization when people stay at these spots, and repeat the experiment 30 times for each spot. How to place anchor nodes in optimal way in an area is left for future research.

![](images/5c7843b9a21059fcef34a5a0528c1389d6e6eeecb8664bad04fb600695b1c589.jpg)



(a) Indoor environment

![](images/89d3e2cd69d1ed3f291c6076ff0e85dc3f91dc3bce42f62c6e1ad15330e2343f.jpg)



(b) Layout of anchors   
Figure 11: Indoor localization testing prototype.

# 6.2.2 Static Position Localization

The accuracy of static localization is shown in Figure 10a. Swadloon achieves localization errors within 0.42m, 0.92m, 1.08m, 1.73m at the percentage of 50%, 90%, 95%, and 100% respectively. The mean error and the standard deviation is 0.50m and 0.59m respectively. We also find that the localization accuracy at spots with $y = - 3 m$ is better than the ones on $y = - 6 m$ . Specifically, on $y = - 3 m ,$ , the localization errors are within 0.28m, 0.73m, 0.91m, 1.73m at the percentage of 50%, 90%, 95%, and 100% respectively.

Meanwhile, we find that there are nearly constant error shifts of the calculated position at all locations. Thus, we further adjust the position by linear regression. That is, we build a polynomial function model from the calculated positions to more precise positions by learning the results from half of the samples. We then apply the function to the other half and the result is ploted in Figure 10b. It shows that the precision is greatly enhanced (i.e., the errors are within 0.67m, 0.82m, 1.56m at the percentage of 90%, 95%, 100% respectively).

We then measure the errors of static localization in a large office (-34 dBFS), where the environment is much more complicated. The layout of the anchor nodes is nearly the same with the one in Figure 11, except the anchor nodes are installed on the ceiling. Figure 10b shows that the error is within 0.94m, 1.23m, 2.59m at the percentage of 80%, 90%, 100% respectively after linear regression.

We also choose specific number of nodes $( i . e . , 3 \sim 6 )$ from the 6 nodes to calculate the position. In Figure 10c, it shows that the precision is greatly enhanced when the number of nodes increases. Besides, the precision in case of 3 nodes becomes much worse for it is more sensitive by the layout shown in Figure 3d, 3e.

# 6.2.3 Real-time Tracking

We also conduct real time indoor tracking using the same environment as in Figure 11. Assume that we get the initial position of the user before s/he walks by shaking the phone. In our experiments reported here, users starts from spot $( 6 , - 6 )$ shown in Figure 12. Then, the user walks in some specific paths with length more than 50m with the phone in his/her hand to the destination at spot (24, −3). The errors are kept within 0.4m shown in Figure 10d and Figure 12.

![](images/5b931eb5ab79c1d4f02fe472f64d3b20e4287ec9105eb80ec4c8bc9326286624.jpg)



Figure 12: Precise real-time indoor tracking.

![](images/0af3aa955812d4f225787c92ad897889d3480406c07d4694f7d602e387a969f8.jpg)



(a) Position Error (m)

![](images/7067e7a6d3650398170d1b5ade0be5b29ad2c64fefe18752b988e87e47fd7ab6.jpg)



(b) Position Error (m)

![](images/44640b43d5a2092b1c2e2741815a7348d46455d4c509a66371a9aabb4332515a.jpg)



(c) Position Error (m)

![](images/4acff0e85ab64885bd32fc1537030e6470266ad64421128f28b8067ada7f42e7.jpg)



(d) Walking Length (m)

![](images/9d8f60373184edbd83aa6c4a141492d0b1dfbeeb4978ed434b089fefed4c8f90.jpg)



(e) Position Error (m)   
Figure 10: Static localization accuracy (a) in different locations, (b) in different scenes and by different methods, (c) when parts of the anchor nodes are chosen for calculation. Tracking accuracy (d) along the walking paths, (e) at final point (24, −3) when there are initial position errors at (6, −6).

We then consider the case that there are errors on the calculated initial position when the user starts walking. For each test, we uniformly choose a spot which is 0.25m, 0.5m, 0.75m, or 1m from (6, −6), and measure the localization accuracies at the destination, i.e., distances from (24, −6) to the calculated final positions in Figure 10e. We can observe that the errors at initial position do not affect the real time tracking, where the error is still within 2m when the user walks for 51 meters and the initial position error is 1m.

As the phone needs 3.9s to process the acoustic samples of 1s, for real-time tracking by Swadloon, we let the phone process 20% of the samples, instead of full samples. Specifically, it processes consecutive samples of 0.05s for each 0.25s. Hence, the phone can deal with the samples and track the position in real time. The result is close to the one which processes full samples in Figure 12. We plot the localization errors in Figure 10d. The mean error and standard deviation in this case is 0.29m and 0.34m respectively, which is still very precise. The CPU usage can also be lowered down by using 10% of the sample with the mean error of 1.02m, if the CPU of some other phone is not fast enough.

# 7. CONCLUSION

In this paper, we propose Swadloon, a novel acousticbased method to find the direction of the acoustic source, and a real-time accurate indoor localization scheme based on this precise direction-finding. Swadloon effectively leverages the Doppler effects of the acoustic waves received by phones by exploiting the sensors in the smartphone and existing speakers to send sinusoidal signals. Our extensive evaluations show that Swadloon performs extremely well in phone-to-phone direction finding and real-time indoor localization. Note that Swadloon did not directly use the ranging result as accurate ranging often needs either time-synchronization or communication between two nodes, both of which incur overhead. Some future work are to study the optimal placement of acoustic anchors, and to develop a low overhead distance estimation between phone and source for further improving the performances and reducing the number of anchors of Swadloon.

# 8. REFERENCES

[1] Bytelight technology. http://www.bytelight.com/.   
[2] Facebook’s friendshake. http://www.facebook.com.   
[3] Getting the force of gravity by using the accelerometer. https://developer.android.com/reference/android/ hardware/SensorEvent.html.   
[4] Google latitude. https://www.google.com.hk/latitude/.   
[5] Bahl, P., and Padmanabhan, V. N. Radar: An in-building rf-based user location and tracking system. In INFOCOM (2000).   
[6] Beauregard, S., Haas, and Wpnc. Pedestrian dead reckoning: A basis for personal positioning. WPNC (2006).   
[7] Chandrasekaran, G., Ergin, M., Yang, J., Liu, S., Chen, Y., Gruteser, M., and Martin, R. Empirical evaluation of the limits on localization using signal strength. In SECON (2009).   
[8] Claerbout, J. Earth soundings analysis: Processing versus inversion. Blackwell Scientific Publications, 1992.   
[9] Constandache, I., Bao, X., Azizyan, M., and Choudhury, R. R. Did you see bob?: human localization using mobile phones. In MobiCom (2010).   
[10] Johnson, C. R., and Sethares, W. A. Telecommunication Breakdown; Concepts of communication Transmitted via Software-Defined Radio. Prentice Hall, August 2003.   
[11] Kim, M., and Chong, N. Y. Direction sensing rfid reader for mobile robot navigation. Automation Science and Engineering, IEEE Transactions on (2009).   
[12] Kulakowski, P., Vales-Alonso, J., Egea-Lopez, E., ´ Ludwin, W., and Garc´ıa-Haro, J. Angle-of-arrival localization based on antenna arrays for wireless sensor networks. Computers & Electrical Engineering (2010).   
[13] Kusy, B., Ledeczi, ´ A., and Koutsoukos, X. D. ´ Tracking mobile nodes using rf doppler shifts. In SenSys (2007).   
[14] lin Chang, H., ben Tian, J., Lai, T.-T., Chu, H.-H., and Huang, P. Spinning beacons for precise indoor localization. In SenSys (2008).   
[15] Liu, H., Darabi, H., Banerjee, P. P., and Liu, J. Survey of wireless indoor positioning techniques and systems. IEEE Transactions on Systems, Man, and Cybernetics, Part C (2007).   
[16] Liu, H., Gan, Y., Yang, J., Sidhom, S., Wang, Y., Chen, Y., and Ye, F. Push the limit of wifi based localization for smartphones. In MobiCom (2012).   
[17] Nandakumar, R., Chintalapudi, K. K., and Padmanabhan, V. N. Centaur: locating devices in an office environment. In MobiCom (2012).   
[18] Niculescu, D., and Badrinath, B. R. Ad hoc positioning

system (aps) using aoa. In INFOCOM (2003).   
[19] Niculescu, D., and Nath, B. Vor base stations for indoor 802.11 positioning. In MobiCom (2004).   
[20] Nishimura, Y., Imai, N., and Yoshihara, K. A proposal on direction estimation between devices using acoustic waves. In MobiQuitous (2012).   
[21] Peng, C., Shen, G., Zhang, Y., Li, Y., and Tan, K. Beepbeep: a high accuracy acoustic ranging system using cots mobile devices. In SenSys (2007).   
[22] Peng, C., Shen, G., Zhang, Y., and Lu, S. Point&connect: intention-based device pairing for mobile phone users. In MobiSys (2009).   
[23] Priyantha, N. B., Chakraborty, A., and Balakrishnan, H. The cricket location-support system. In MobiCom (2000).   
[24] Prorok, A., Tome, P., and Martinoli, A. Accommodation of nlos for ultra-wideband tdoa localization in single- and multi-robot systems. In IPIN (2011).   
[25] Qiu, J., Chu, D., Meng, X., and Moscibroda, T. On the feasibility of real-time phone-to-phone 3d localization. In SenSys (2011).   
[26] Rai, A., Chintalapudi, K. K., Padmanabhan, V. N., and Sen, R. Zee: zero-effort crowdsourcing for indoor localization. In MobiCom (2012).   
[27] Rice, M. Digital Communications: A Discrete-Time Approach. Prentice Hall, 2008.   
[28] Rosen, J., and Gothard, L. Encyclopedia of Physical Science. 2009.   
[29] Se, S., Lowe, D. G., and Little, J. J. Vision-based global localization and mapping for mobile robots. IEEE Transactions on Robotics (2005).   
[30] Subramanian, A., Deshpande, P., Gaojgao, J., and Das, S. Drive-by localization of roadside wifi networks. In INFOCOM (2008).   
[31] Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., and Choudhury, R. R. No need to war-drive: unsupervised indoor localization. In MobiSys (2012).   
[32] Want, R., Hopper, A., Falcao, V., and Gibbons, J. ˜ The active badge location system. ACM Trans. Inf. Syst. (1992).   
[33] Ward, A., Jones, A., and Hopper, A. A new location technique for the active office. Personal Communications, IEEE (1997).   
[34] Yang, J., Sidhom, S., Chandrasekaran, G., Vu, T., Liu, H., Cecan, N., Chen, Y., Gruteser, M., and Martin, R. P. Detecting driver phone use leveraging car speakers. In MobiCom (2011).   
[35] Yang, Z., Wu, C., and Liu, Y. Locating in fingerprint space: wireless indoor localization with little human intervention. In MobiCom (2012).   
[36] Youssef, M., and Agrawala, A. The horus wlan location determination system. In MobiSys (2005).   
[37] Zhang, Z., Chu, D., Chen, X., and Moscibroda, T. Swordfight: enabling a new class of phone-to-phone action games on commodity phones. In MobiSys (2012).   
[38] Zhang, Z., Zhou, X., Zhang, W., Zhang, Y., Wang, G., Zhao, B. Y., and Zheng, H. I am the antenna: accurate outdoor ap location using smartphones. In MobiCom (2011).