# Inferring Motion Direction using Commodity Wi-Fi for Interactive Exergames

Kun Qian†, Chenshu Wu†, Zimu Zhou‡, Yue Zheng†, Zheng Yang†, Yunhao Liu†

†School of Software and TNLIST, Tsinghua University, China

‡Computer Engineering and Networks Laboratory, ETH, Switzerland

{qiank10, wucs32, cczhengy, hmilyyz, yunhaoliu}@gmail.com, zimu.zhou@tik.ee.ethz.ch

# ABSTRACT

In-air interaction acts as a key enabler for ambient intelligence and augmented reality. As an increasing popular example, exergames, and the alike gesture recognition applications, have attracted extensive research in designing accurate, pervasive and low-cost user interfaces. Recent advances in wireless sensing show promise for a ubiquitous gesture-based interaction interface with Wi-Fi. In this work, we extract complete information of motion-induced Doppler shifts with only commodity Wi-Fi. The key insight is to harness antenna diversity to carefully eliminate random phase shifts while retaining relevant Doppler shifts. We further correlate Doppler shifts with motion directions, and propose a light-weight pipeline to detect, segment, and recognize motions without training. On this basis, we present WiDance, a Wi-Fi-based user interface, which we utilize to design and prototype a contactless dance-pad exergame. Experimental results in typical indoor environment demonstrate a superior performance with an accuracy of 92%, remarkably outperforming prior approaches.

# ACM Classification Keywords

H.5.2. Information Interfaces and Presentation: User InterfacesInput devices and strategies; C.2.1. Computer-Communication Networks: Network Architecture and DesignWireless communication

# Author Keywords

Motion Direction Recognition; Wireless Sensing;

Off-the-shelf Wi-Fi; Exergame

# INTRODUCTION

Exergames, where players are compelled to get up and exercise (e.g., dance, kick-boxing, sports moves), bring more than just fun [8, 15]. Researchers find that exergames can improve the fitness, health and social involvement of players [20, 27]. Due to their health benefits, various exergame interfaces have been developed in both the industries (e.g. Kinect Sports and Wii Fit) and academia [7, 24]. Most interfaces for

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Permissions@acm.org.

CHI 2017, May 06-11, 2017, Denver, CO, USA

© 2017 ACM. ISBN 978-1-4503-4655-9/17/05...\$15.00

DOI: http://dx.doi.org/10.1145/3025453.3025678

![](images/87231a572b5faebcd3e110b34e9729b1d29008f9f7ed7d486b631c2ad9571bc1.jpg)



Figure 1. Human-computer interaction interface of WiDance

exergames are based on computer vision, dedicated sensors or sonic technology. Despite their high accuracy in tracking motions of players, they suffer from limitations such as sensitivity to lighting condition and line-of-sight condition, requirement of device attachment and high-cost installation and instrumentation. We argue that a more ubiquitous exergame interface with fewer environment constraints is essential to fit in the fragmented free time and space in modern life. For instance, a white-collar worker may play a 5-min exergame in the office to refresh. A housekeeper may take a quick workout during the waiting time when preparing dishes in the kitchen.

The need for a low-cost, non-invasive, and ubiquitous user interface has triggered extensive research on in-air human sensing, especially using the almost-everywhere Wi-Fi infrastructure [4, 18, 31, 6, 28]. The main idea is to model and extract motion induced variations on Wi-Fi signals to infer human activities. In principle, it is possible to obtain all parameters of incident signals, including amplitudes, phases, frequency shifts, and relate these parameters with human actions. Pioneer works [4, 22, 12] extract accurate signal parameters to derive motion-induced Doppler shift and time-of-flight, which are used to estimate the speed and distance of motions. However, they require specialized hardware because commodity Wi-Fi devices suffer from random phase shifts caused by lack of synchronization, limited frequency bandwidth and multipath effect. Other works [31, 6, 28, 30] apply machine learning to coarse-grained signal parameters available on commodity Wi-Fi devices to infer user activities. Yet the training efforts involved and the less interpretable features extracted make them unfavorable as a robust and light-weight user gesture interface.

This paper seeks to advance the state-of-the-art in wireless interaction interfaces by accurately deriving motion-induced Doppler shifts using Channel State Information (CSI) available on unmodified Wi-Fi devices, and further extracting motion directions for exergame designs. As a proof-of-concept, we present WiDance, a dance-pad like exergame with commercial Wi-Fi devices. As shown in Figure 1, it tracks the leg moving directions of players by monitoring the minute Doppler shifts in the received CSI of Wi-Fi signals, and recognizes the estimated directions as the ones shown on a screen. Technically, WiDance addresses two critical challenges. (1) How to obtain full information of Doppler shifts from off-the-shelf imperfect Wi-Fi devices? While some previous works [30] have extracted Doppler-related features from commodity Wi-Fi devices, they only extract the absolute values of Doppler shifts without arithmetic signs, and thus fail to identify the direction of motions. Instead, WiDance extracts accurate and comprehensive Doppler shifts with direction information from CSI by leveraging multiple antennas on commodity Wi-Fi devices. The key insight is that while antennas at the same receiver experience different channel distortions due to spatial diversity, they suffer from the same noise sources. Therefore, we propose a series of signal processing steps to properly manipulate signals from multiple antennas, making it possible to eliminate random noises while retaining Doppler shifts of interests. (2) How to detect, segment and recognize complex player actions from Doppler shifts series? To robustly recognize player motions without training, we first verify that single link is insufficient for tracking player actions, and solve inherent ambiguities with minimum cost by adopting one more link. An effective light-weight model is proposed to relate Doppler shifts observed from joint two wireless links with player actions, and a series of data processing steps are developed to achieve robust detection, segmentation and finally recognition of player actions.

We prototype WiDance with commodity Wi-Fi infrastructure and evaluate its performance in various indoor environments. Experimental results show that WiDance yields accuracies for recognizing player actions of 92%. Compared with the stateof-the-art, the Doppler shifts features obtained by WiDance can differentiate all eight actions required by dancing games, while those in existing approaches [30, 6] can only classify actions into three coarse categories. The motion recognition accuracy of WiDance is comparable to popular classifiers such as HMM, even without training. We envision WiDance as a promising step towards practical wireless human-computer interaction interface, which underpins new insights for future wireless sensing applications.

In summary, the main contributions are as follows:

We design a novel algorithm to extract complete information of motion-induced Doppler shifts (both absolute values and signs) leveraging antenna diversity on commodity Wi-Fi devices. As far as we are aware of, it is the first work that

![](images/8b1acda4a2136ecd97ee2d5444de7850b68dc1b26934c7d318881ca012e33da2.jpg)



Figure 2. WiDance logic flow

obtains accurate arithmetic signs of Doppler shifts on Wi-Fi infrastructure without modification.

We model the relations between Doppler shifts with motion directions, and develop a wireless interactive exergame, i.e., a dance pad with eight types of inputs. It operates via a light-weight yet effective signal processing pipeline to detect, segment and recognize player actions from Doppler shift series without prior training. In addition to interactive exergames, the core techniques in WiDance are applicable in various gesture recognition applications, including, but not limited to, fall detection for the elderly, and gait recognition for user identification.   
We implement WiDance on commodity Wi-Fi devices and validate its effectiveness with various indoor settings. Experimental results demonstrate that WiDance achieves recognition accuracy of 92%. By exploiting complete information of Doppler shifts for motion recognition, WiDance outperforms previous feature-based approaches, which fail to derive the direction of motions.

The rest of the paper is organized as follows. We first provide the overview of WiDance, followed by the principles of Doppler shifts extraction and player actions recognition. Then, performance evaluation and user study of WiDance are provided. Finally, related works are reviewed and conclusion is drawn.

# WIDANCE OVERVIEW

WiDance is a passively interactive dancing pad-like exergame using off-the-shelf Wi-Fi devices. Figure 2 shows the logic process of WiDance. The game starts by selecting a piece of music. For each note in the music, WiDance rhythmically displays an arrow of certain direction on the screen. The player follows visual notes and moves his/her legs along the directions indicated by the notes. WiDance continuously records and processes CSI for recognizing the player reactions over the whole gaming period. Each recognized reaction is compared with the corresponding visual note, and the comparison result is displayed on the screen and the reaction is scored.

The main technical challenge for WiDance is to promptly and robustly recognize player reactions from noisy CSI data. Towards this goal, WiDance leverages the motion-induced Doppler effect observed in CSI and propose a two-step reaction recognition procedure. As shown in Figure 2, the first step is to extract Doppler effect from CSI. It recovers a spectrogram of Doppler frequency shifts in presence of random phase offsets, burst noise and interferences using a series of signal processing techniques including antenna selection, data sanitization and time-frequency analysis. The second step is to recognize player reactions from the spectrogram of Doppler frequency shifts. The challenge for this step is to robustly recognize each individual player reaction from continuous Doppler frequency shifts that may consist of multiple reactions. Operations adopted in this step include movement detection, trace segmentation and motion classification. The output of this step is reaction series recognized by WiDance.

![](images/6aebad0425522c10b1fa9be8982c4a4d51780836f7480d216b9c33ec5a7b0e7c.jpg)



(a) Illustration of Doppler effect

![](images/f298c6f8f9725843947e0e03e0c45b39525e0d69e014c621df72867bd53e2bce.jpg)



(b) Spectrogram of Doppler effect

![](images/cb5278c4d12e0e47ced4815ac99e8bed8b65b15f5f3686ce1cd2a19e51e81af8.jpg)



(c) Doppler effect with multiple antennas   
Figure 3. Modeling Doppler effect in multipath scenarios.

# DOPPLER EFFECT IN WI-FI

WiDance extracts Doppler effect from Wi-Fi signals to recognize dancing actions of players. This section provides the technical preliminaries, fundamental model and practical issues of identifying Doppler frequency shifts from noisy Wi-Fi signals on commercial devices.

# Doppler Effect

Doppler shift is the change in the frequency of a wave for observers. It is caused by change in relative locations of sources, observers and reflectors. In the context of contactless sensing, both transmitters (sources) and receivers (observers) are statically deployed, while target objects (reflectors) move and alter the wireless transmission. As shown in Figure 3a, when the target object moves towards the transmitter and the receiver, the crests and troughs of the reflected signals arrive at the receiver at a faster rate. Conversely, when an object moves away from the receiver, the crests and troughs arrive at a slower rate. In general, for a point object, the Doppler frequency shift of the signal reflected off the object is:

$$
f _ {D} = - \frac {1}{\lambda} \frac {\mathrm{d}}{\mathrm{dt}} d (t), \tag {1}
$$

where λ is the wavelength of the signal and $d ( t )$ is the length of the reflected path.

As an illustrative example, we prototype a wireless transceiver system using two USRPs synchronized by an external clock. The two USRPs are placed together near the ground, and a participant strides with his right leg at moderate rate, at the direction orthogonal to the link, as in Figure 3a. The Doppler effect caused by striding is obtained by tracking the phase of the received signal. Figure 3b shows the spectrogram of Doppler effect of striding. Clearly, positive Doppler shifts appear as the user strides towards the link, while negative Doppler shifts appear as the user strides away from the link. Thus, it is possible to track target motion (both speed and direction) by exploiting Doppler effect.

# Doppler Effect in CSI

In reality, instead of single path as the reflected path in $\mathrm { F i g \mathrm { - } }$ ure 3a, there are multiple paths where signal propagates from the transmitter to the receiver. The phenomenon is known as multipath. As a result, the response of the wireless channel at frequency f and time t is the superimposition of responses of each individual path [21]:

$$
H (f, t) = \sum_ {k = 1} ^ {K} \alpha_ {k} (t) e ^ {- j 2 \pi f \tau_ {k} (t)}, \tag {2}
$$

where K is the total number of multipath, and $\alpha _ { k } ( t )$ and $\tau _ { k } ( t )$ are the complex attenuation factor and time of flight for the k-th path, respectively.

For the k-th path, the time of flight $\tau _ { k } ( t )$ is the time for light to travel at a distance of path length of $d _ { k } ( t ) , \mathrm { i . e . } ~ d _ { k } ( t ) = c \tau _ { k } ( t )$ , where c is the speed of light. Thus, according to Equation 1, the channel response can be represented by Doppler frequency shift on each path and further divided into two categories:

$$
H (f, t) = H _ {s} (f) + \sum_ {k \in P _ {d}} \alpha_ {k} (t) e ^ {j 2 \pi \int_ {- \infty} ^ {t} f _ {D _ {k}} (u) \mathrm{d} u}, \tag {3}
$$

where $H _ { s } ( f )$ is the sum of responses of all static path $( f _ { D } = 0 )$ , and $P _ { d }$ is the set of dynamic path $( f _ { D } \neq 0 )$ .

Assuming that $\alpha _ { k } ( t )$ and $f _ { D _ { k } } ( t )$ are nearly constant during short time interval, Doppler frequency shifts can be obtained from spectrogram with time-frequency analysis:

$$
\mathcal {H} (f, t) \approx H _ {s} (f) + \sum_ {k \in P _ {d}} \alpha_ {k} (t) B (f _ {D _ {k}} (t)), \tag {4}
$$

where $B ( \cdot )$ is the window function for cutting out the signal segment of interest.

CSI is the sampled version of the channel response in Equation 2 and 3. It is available from upper layers on off-the-shelf

![](images/835bc2accdfb8cd2299bee188a7f9b258da4c3521ac55101d69b6d1420c7bd63.jpg)



(a) Antenna selection

![](images/873f6dd53150b94cce4bd87c92dd67e1f8706acd4813ec5c4ae0a10799a0e8ae.jpg)



(b) Raw CSI

![](images/9f21169ce92a4bbefc4824a0eb0c6fb1531b484e9b9b6dd94a2abbaf8988e1dd.jpg)



(c) Data sanitization

![](images/6bff0dfe176d8c495934fa5b77ecd6a39dfc2dce4864f10b9ceda85ffe64e775.jpg)



(d) Spectrogram of CSI   
Figure 4. Extraction of Doppler frequency shifts from CSI of multiple antennas

Wi-Fi Network Interface Cards with only slight driver modification [9]. However, lack of synchronization between Wi-Fi NICs induces unknown phase shifts in raw CSI:

$$
\hat {H} (f, t) = H (f, t) e ^ {- j 2 \pi (\Delta_ {t} f + \Delta_ {f} t)}, \tag {5}
$$

where $2 \pi ( \Delta _ { f } t + \Delta _ { t } f )$ is phase shift caused by carrier frequency and timing offset. Therefore, it is infeasible to directly extract Doppler components from actual CSI measurements.

Prior works [30, 6] eliminates phase noises by calculating CSI power, i.e. $| \hat { H } ( \dot { f } , t ) | ^ { 2 } = | H ( \dot { f } , t ) | ^ { 2 }$ . However, this process meanwhile eliminates the imagery part of CSI, and thus loses the information of signs of Doppler shifts. That is, with only CSI power, we have no idea whether reflectors moves towards or away from the link. As a result, CSI power can only be used to recognize what target does (e.g. activity types), but not how target does (e.g. activity directions), through an upper-layer learning-based framework.

# Doppler Effect by Multiple Antennas

To remove unknown phase shifts while still retain complete Doppler frequency shifts, WiDance uses multiple antennas available on Wi-Fi NICs. Since all antennas on the same NIC experience the same phase shifts, calculating conjugate multiplication of CSI of one pair of antennas also eliminates the phase offset. Specifically, denote the CSI of the i-the antenna as $H ^ { ( i ) } ( f , t )$ , we have the following product:

$$
\begin{array}{l} H ^ {(1)} (f, t) H ^ {(2)} (f, t) ^ {*} \approx H _ {s} ^ {(1)} (f) H _ {s} ^ {(2)} (f) ^ {*} \\ + \sum_ {k \in P _ {d} ^ {(1)}} \alpha_ {k} ^ {(1)} (t) H _ {s} ^ {(2)} (f) ^ {*} e ^ {j 2 \pi \int_ {- \infty} ^ {t} f _ {D _ {k}} ^ {(1)} (u) \mathrm{d} u} \\ + \sum_ {k \in P _ {d} ^ {(2)}} H _ {s} ^ {(1)} (f) \alpha_ {k} ^ {(2)} (t) ^ {*} e ^ {- j 2 \pi \int_ {- \infty} ^ {t} f _ {D _ {k}} ^ {(2)} (u) \mathrm{d} u} \tag {6} \\ + \sum_ {k \in P _ {d} ^ {(1)}, l \in p _ {d} ^ {(2)}} \alpha_ {k} ^ {(1)} (t) \alpha_ {l} ^ {(2)} (t) ^ {*} e ^ {j 2 \pi \int_ {- \infty} ^ {t} f _ {D _ {k}} ^ {(1)} (u) - f _ {D _ {l}} ^ {(2)} (u) \mathrm{d} u}. \\ \end{array}
$$

As in Figure 3c, by closely placing antennas $A _ { 1 }$ and $A _ { 2 }$ of the receiver $( \mathrm { e } . \mathrm { g } . , 2 f \leq \lambda )$ , CSI of two antennas may contain the same major multipaths $( \mathrm { i . e . , } P _ { d } ^ { ( 1 ) } = P _ { d } ^ { ( 2 ) } )$ with different complex attenuation factors but similar Doppler shifts. Then the terms in Equation 6 can be divided into three categories:

Static terms. The static term $H _ { s } ^ { ( 1 ) } ( f ) H _ { s } ^ { ( 2 ) } ( f ) ^ { * }$ are calculated by multiplication of static responses (e.g., LOS) of two antennas. This term does not contain Doppler shifts and can be filtered out with a high-pass filter.

Target terms. Target terms are calculated by multiplication of static responses of one antenna and responses that contain target Doppler shifts of the other antenna. They contain Doppler shifts of interest and their arithmetic opposite numbers. A sufficient condition for extracting Doppler shifts instead of their opposite numbers is that terms containing Doppler shifts have larger amplitudes. Specifically, for the k-th path, following condition should be fulfilled:

$$
\left| \frac {H _ {s} ^ {(1)} (f)}{\alpha_ {k} ^ {(1)} (t)} \right| <   \left| \frac {H _ {s} ^ {(2)} (f)}{\alpha_ {k} ^ {(2)} (t)} \right|. \tag {7}
$$

Although it is unable to separate static and dynamic responses from CSI and directly verify the condition, there still exist some clues in CSI, which can guide us to obtain multiplication results that satisfy the condition. Note that the issues of antenna selection will be discussed later in this section.

Cross terms. Cross terms are products of dynamic responses of antennas. They only contain difference of Doppler shifts and may obfuscate real Doppler shifts. Fortunately, the static responses indoors are likely to dominate dynamic responses, due to strong LOS signals or large static reflectors like walls. As a result, the cross terms are orders weaker than target terms. Furthermore, in WiDance, only one player moves his legs in the monitor area at any time. And the difference of Doppler shifts caused by different body parts are usually small, and can be filtered out with high-pass filter. Thus, the negative effect of cross terms can be tolerated.

# Extraction of Doppler Effect

To convert noisy CSI to spectrogram of Doppler frequency shifts, WiDance introduces a series of processing steps.

Antenna Selection. Recall that to correctly extract Doppler frequency shift, the condition in Equation 7 should be satisfied. Thus, we should properly select pairs of antennas and assign the order of antennas in conjugated multiplication. Despite of the mixture of static and dynamic responses, CSI itself reveals some clues that help verify the condition.

Observation I: CSI with higher amplitude is likely to possess larger static responses. This is because the amplitude of static responses are orders of magnitude larger than that of dynamic responses, due to existence of strong LOS signals and larger static reflectors like walls. Consequently, even if slightly disturbed by dynamic responses, the averaged CSI can be used to approximate the static response in Equation 7.

![](images/5316ec88ddfdf9c09ac73f6b5a83cb70b6de79f474c3d287ba8599c53d6fe519.jpg)  
Figure 5. Translation between Doppler effect and player reaction

Observation II: CSI with higher variance is likely to possess larger dynamic responses. This is because only dynamic responses contributes to variation of CSI. As a result, the standard deviation of CSI can be used to indicate the dynamic responses in Equation 7.

Figure 4a illustrates the criterion for selection of pair of antennas. The boxes show distributions of CSI of different antennas and across subcarriers over time. In this example, the 2nd antenna has the largest variances with relative small amplitudes, while the 3rd antenna has the largest amplitudes with relative small variances. By comparing the ratio of amplitudes and standard deviations of CSI, the 3rd and 2nd antennas are orderly selected.

Data Sanitization. As noted in Equation 6, raw CSI contains significant static components, low-frequency interferences and burst noises, which obfuscate Doppler shifts of interest. Thus, it is natural to remove these signal components with filters. Specifically, we adopt Butterworth bandpass filter for its flat amplitude response in the pass band, and apply the filter to the multiplication series of each CSI subcarrier. The upper and lower cutoff frequencies of Butterworth filter are set to 40Hz and 2Hz respectively. The upper cutoff frequency is decided by the experimental observation that normal human striding velocities are no more than $\nu _ { m } = 1 \mathrm { m / s }$ . For Wi-Fi devices working at 5.8GHz, the upper bound of Doppler frequency of PLCR is f = 2vm $\begin{array} { r } { f = \frac { 2 \nu _ { m } } { \lambda } \approx \frac { 2 \times 1 \mathrm { m / s } } { 0 . 0 5 \mathrm { m } } = 4 0 \mathrm { H z } } \end{array}$ . The lower cutoff frequency is decided by trade-off between fully eliminating interference and loss of low-frequency components of Doppler effect. However, such loss has minor impact on WiDance, since WiDance can still leverage high-frequency components that are more stable against burst noises for motion recognition.

Figure 4b and 4c show the amplitude and phase of CSI series before and after filtering. Clearly, burst noises and lowfrequency interferences are removed. Moreover, the cyclic phase changes that correspond to the target Doppler shifts at time 1 and 1.5 second are signified.

Time-frequency analysis. To further denoise and compress CSI data for time-frequency analysis, we perform Principle Component Analysis (PCA) on all CSI subcarriers and select the first principle component that contains major and consistent power variations caused by target motions. Then, short-term Fourier transform (STFT) is applied to the first principle component to obtain the spectrogram of Doppler frequency shifts. Specifically, a Gaussian window with length shorter than 0.15s is applied in STFT to meet the assumption of nearly constant amplitudes and Doppler shifts in Equation 4. A zero padding is further applied in order to generate finer-grained spectrogram. Finally, the non-overlapping spectrograms of all CSI segments are spliced together to generate the whole spectrogram.

Note that there is lower bound on range of actions that can be detected by WiDance, due to the well-known uncertainty principle. Specifically, suppose the time length of the data window of STFT is T , then the frequency resolution of the spectrum is $\begin{array} { r } { \Delta _ { f } = \frac { 1 } { T } } \end{array}$ . To correctly identify the signal of the frequency shift, the amplitude of the frequency shift must fall into the non-DC bins, which correspond to a minimum frequency of $\textstyle { \frac { 2 } { T } }$ . For a signal segment with constant frequency shift, the frequency shift should fulfil $\begin{array} { r } { F = \frac { V } { \lambda } \ge \frac { 2 } { T } } \end{array}$ , where V is the change rate of the reflecting signal path and λ is the wave length of the signal. Thus the sensitivity of action range R is:

$$
R > \frac {1}{2} V T \geq \lambda \tag {8}
$$

In reality, the sensitivity of WiDance is worse than the theoretical bound due to complex stride actions including acceleration and deceleration and existence of environmental noises.

Figure 4d illustrates the spectrogram of Doppler shifts induced by striding (first towards and then away from the link), from noisy CSI provided by commercial Wi-Fi NIC. Though fluctuating, the spectrogram clearly reflects the trend of signed Doppler effect (first positive and then negative), which we use to recognize the reaction performed by the player.

# MOTION RECOGNITION

This section details the principles and practical issues to recognize player reactions from spectrogram of Doppler shifts.

# Player Reaction in Doppler Effect

We first derive the relation between movements of reflector (player) and Doppler shifts. As shown in Figure 5a, given constant length of the reflecting path, the reflector is on an ellipse with the transceivers as focuses. Based on the impact on the ellipse, the velocity of the reflector can be divided into the tangential velocity along the tangent and the radial velocity along the norm. Specifically, the tangential velocity guides the target moving along the ellipse while the radial velocity drives the target moving off the ellipse. Evidently, the radial velocity is the only cause of change in the length of the reflected path, and thus the Doppler frequency shift. That is, if the reflector moves along various directions with the same speed, the link will experience different changes in the length of the reflected path, according to the radial velocities projected on the norm direction. As a result, it is possible to obtain the moving direction of the reflector with the level of radial velocity derived from Doppler effect.

![](images/6e6b923876d5d35fbaaa6023041fe726d975beddaab696c8b25ba610ad9c0cf4.jpg)



(a) Spectrogram

![](images/212355e5aa8c12bed0f721931b99ba12da42d6b7f03641ff70a2357af2f54980.jpg)



(b) Detection

![](images/05469e642a66c4f984061d457702166039efc97901b814963bcb757eb0eb6a5e.jpg)



(c) Segmentation

![](images/e3f6d3a1044164df289c5698dd3505af3500aa88ad4552478c8c1c38884db17e.jpg)



(d) Classification   
Figure 6. Motion recognition process from Doppler shifts

However, it is insufficient to use one link to estimate the moving direction for the following two reasons. First, the distribution of radial velocity is symmetric about the norm. So it is unable to distinguish any two symmetric directions using Doppler effect of a single link only. Second, recognition using a single link assumes that the player performs reactions at constant speed to consistently map the level of radial velocity to moving direction. However, such assumption will not hold in practice due to diverse actions performed by players.

To address the above challenges, we propose a recognition scheme to solve the symmetric ambiguities with minimum cost by adding one additional link. As shown in Figure 5b, two links are placed orthogonal with each other. As the player stands at the intersection of midnormals of the two link, for any direction where the player reacts, the velocity can be projected on the 2D $V _ { 1 } - V _ { 2 }$ plane, where $V _ { i }$ is the speed of the radial velocity for the i-th link. Even if the player performs reactions at various speeds, the moving direction is reserved by radial velocities of the two orthogonal links, making it possible to recognize player reactions.

# Motion Recognition Workflow

Figure 6 shows an illustrative process of motion recognition in WiDance. In this example, a player stands at the intersection of midnormals of the two link, facing towards the transmitter. The player first halts for 1s, then moves the leg in left-rear direction within 2s, and halts again for another 2s. Next, the player moves forward, continuously followed by two left-front movements, which takes 6s in total. Finally, the player halts for 1s. The corresponding spectrogram is shown in Figure 6a.

Movement Detection. During the game, the player may occasionally halt, due to e.g. long waiting intervals between successive visual action notes (arrow) or tiredness. Periods during which the player halts do not contain valid actions, and should be skipped for efficiency. Thus, it is necessary to perform movement detection before motion recognition.

WiDance conducts movement detection based on the following intuition. When a player is static, no Doppler effect will be observed and the spectrogram contains only noises. As a result, the power of spectrogram spreads out across the whole frequency band. In contrast, when a player moves, the spectrogram is dominated by Doppler effect, and the power of spectrogram concentrates on the frequency of interest. Therefore, WiDance calculates and smooths variances of power distribution in frequency domain for movement detection. Note that only the filter of CSI sanitization affects the variance, as the filter decides to which extent the out-of-band components are filtered out. Therefore, regarding a fixed filter, it is feasible to use a predefined threshold. Player movement is detected when the variance falls below the threshold, as shown in Figure 6b.

Trace Segmentation. During an exergame, a player may frequently perform continuous actions, as in Figure 6. Thus, it is necessary for WiDance to correctly segment them into individual ones for recognition.

WiDance leverages the characteristics of action patterns performed by players. Specifically, for each action, the player first stretches one of his/her legs in some direction, and then retracts the leg back to stand. As a result, the player action causes a pair of peaks or valleys in Doppler frequency shifts with significantly different amplitudes, depending on the player’s moving direction, as illustrated in Figure 6c. For each action, by orthogonally placing two links, at least one link experiences large fluctuations no matter at which direction the player moves. Thus, WiDance computes the average sum of absolute values of Doppler frequency shifts of the two links, and detects the prominent peaks. Then two adjacent peaks are grouped as the spectrum of one complete action. An illustrative segmentation result is shown in Figure 6c.

Motion Classification. Finally, WiDance applies the recognition model in Figure 5b to Doppler frequency segments to identify the corresponding actions. As Doppler frequency shifts vary even within one segment, due to acceleration and deceleration of human motions, simply estimating moving direction corresponding to each time sample may suffer from significant noises. Hence we propose a two-level rule-based classification scheme, which comprehensively takes advantage of all data available within the Doppler frequency segments.

In the first step, WiDance classifies movement directions based on the ratio of accumulative absolute values of Doppler frequency shifts of two links, as shown in Figure 6d. For clarity, we represent the ratio with its arctangent value, which range in [0, 90°]. Clearly, the movement directions can be classified into three coarse categories: LR/RF, front/right/rear/left, LF/RR. The theoretical ratios of three categories are 0°, 45° and 90°, respectively. However, due to noises and variations of player positions, non-zero Doppler frequency shifts can still be observed even if the player moves in parallel with the link, which leads to practical ratios slightly larger than 0° for LR/RF category, and smaller than 90° for LF/RR category. Thus, we slightly adjust the thresholds to $3 0 ^ { \circ }$ and 60°, respectively.

![](images/fa7a64192380324d14cfcb5c5c7136b6240f5e3dcc01ccb96827dae56318d5d5.jpg)



(a) WiDance

![](images/64c54a149319e576a29a28df6a5af70b856b8f9a33c22eb425b46d1fda7bac97.jpg)



(b) User action   
Figure 7. Experiment setup

In the second step, WiDance further differentiates movement directions in each coarse categories, based on the order of appearances of the positive and negative Doppler frequency shifts in the segment. Specifically, for any link, if the positive Doppler shift firstly appears, the player stretches his leg towards the link. In contrast, if the negative Doppler shift firstly appears, the player stretches his leg away from the link. Thus, the directions in each coarse directions can be further classified with the knowledge of whether the player stretches his leg towards or away from the two links. With the two-step scheme above, the movement directions of actions can be identified.

# EVALUATION

This section presents the experimental settings and the detailed performance of WiDance.

# Experiment Methodology

Evaluation Setup. WiDance consists of one transmitter and two receivers equipped with wireless cards. As shown in Figure 7a, three ThinkPad T-series laptops equipped with Intel 5300 wireless NICs are used to establish orthogonal links. For easier deployment, we connect the devices with external antennas. Specifically, the transmitter has one antenna, and each receiver has three antennas. The links are set up to work on Channel 165 at 5.825GHz. CSI are collected with modified network driver [9], and then passed to processing computer via TCP/IP protocol. The processing computer uses a Intel i7- 5600U 2.6GHz CPU, and processes CSI data using MATLAB. The antennas of each receiver are placed loosely in a line, with a spacing distance of about one wavelength (5.2cm). And the packet transmission rate is set to 1024Hz, which is later decimated for study of the impact of sampling rates. The transmission power are set to 15dBm by default.

All experiments are conducted in rooms in academic buildings, where experimental areas are surrounded with desks, chairs and other equipments. Players are asked to stand at the intersection of midnormals of the two links, facing towards the transmitter. To interact with players, we write a program that randomly displays visual notes on the screen, guiding players to perform dancing actions. An action of rear stride is illustrated in Figure 7b. To make sure that players concentrate on the experiment, no music is incorporated in the current version.

To fully understand the variations in user diversity, we recruit 30 participants and ask them to play dancing games with WiDance. For preparation, we demonstrate the usage of WiDance. Then, participants are asked to individually practice dancing. During experiment, each participant is asked to play 2-minute

![](images/68e52181350f45b68ed6f364d1e66e7e32e926e47e5533056cade4bf8f6bd19d.jpg)



(a)

![](images/15dfbbd75c5fcfee85a582a1ce77e7e20569a373aeb9649a8c0346e89af021a1.jpg)



Figure 10. Criterions and errors. (a) The ratio of Doppler shifts and errors between adjacent directions. (b) The moving directions and errors between non-adjacent directions.

dancing game for 4 times. Games are played in turns to ensure that participants get enough rest before each game. All participants are rewarded after the experiment. The total experiment lasts totally for 2 days and 8 hours each day, and over 10,000 actions are recorded during the experiment.

Baselines. To fairly demonstrate the performance of WiDance, we implement WiDance and two learning-based schemes, HMM-WiDance and CARM [30], for comparison. On one hand, HMM-WiDance uses Doppler frequency shifts as WiDance does, yet trains HMM for all eight actions. We compare WiDance with HMM-WiDance to evaluate the non-learning recognition scheme. On the other hand, CARM uses only absolute values of Doppler frequency shifts that is obtained from CSI power, and trains HMMs using this truncated features. We compare WiDance with CARM to evaluate the extraction of Doppler frequency shifts. The HMMs implemented in both schemes are similar to those in [30].

# Performance

Overall performance. Taking all parameters into consideration, WiDance yields an overall accuracy of 92%. As the confusion matrix in Figure 8a shows, WiDance achieves consistently high recognition accuracy for all actions.

Yet, there still exist errors for some directions. Based on the root causes, we divide errors into two categories: errors between adjacent directions and errors between non-adjacent errors. Recall that WiDance recognizes actions with two criterions: the amplitude ratio of Doppler shifts and the appearance order of positive and negative Doppler shifts. As shown in Figure 10a, errors in Doppler ratios make WiDance confuse actions with adjacent directions, while in Figure 10b, errors in moving directions make WiDance confuse actions with nonadjacent directions. Most errors come from misclassification between actions with adjacent directions. For example, about 10.6%, 10.2% and 8.7% actions with right-front, right-rear and left directions are misclassified to their adjacent directions: right, rear and left-rear, respectively. In contrast, errors in moving directions only cause negligible errors, which is about only 0.52% for actions with left direction and 0.14% for actions with front and right direction. The result demonstrates that the condition in Equation 7 can be almost always fulfilled to correctly recognize the true Doppler shifts. Also, it means that compared with signs of Doppler shifts, amplitudes of Doppler shifts is more difficult to estimate, due to environmental noises.

![](images/4e54d2e6524c94040cafc9f027f3f916db0f9a603857dd544a2105779251eaa8.jpg)



(a) WiDance (overall 92%)

![](images/8936ce9c1e77bb018e8aa1afb6d703135b0cc84f72ea4d510413822d64c0be0a.jpg)



(b) HMM-WiDance (overall 95%)

![](images/70af062f2b2dc47a6f4b5ef9873812ffa33f7a9b317703889e9ab4ada5441dfa.jpg)



(c) CARM (overall 50%)

![](images/0e2b98767f50de59396f054af5f43606b7118a3162b4fd15f933e1f5c19b0443.jpg)



Figure 9. Performance of successive actions. (overall 85%)   
Figure 8. Confusion matrices of various methods.

Further, the confusion matrix reveals that WiDance statistically outperforms in straight directions (front, right, rear, left) than in oblique directions (right-front, right-rear, left-rear, left front). Note that the oblique directions are parallel with one of two links. For simplicity of modelling, WiDance assumes that movement in parallel with the link causes zero Doppler shifts to signals of that link. However, such assumption holds only when the player moves strictly at the intersection of midnormals of two links. In reality, as the player strides within a small range, the link may experience significant Doppler shifts even if the player moves in parallel with the link, which may lead to errors in Doppler amplitude ratios and thus incorrect recognition outputs. Such issues can be solved by further modelling positions of legs, in addition to movement directions in current model, which we leave for future work.

Performance of recognition scheme. To evaluate the performance of non-learning recognition scheme implemented in WiDance, we compare WiDance with HMM-WiDance, which applies Doppler shifts feature to HMM for modelling of eight actions. By carefully tuning the HMM parameters, HMM-WiDance merely achieves an accuracy of 95%, which is slightly higher than that of WiDance. Thus, we claim that the non-learning recognition scheme can achieve high accuracy comparable with the complex learning method.

Different from WiDance which exhibits slightly different performance for different directions, HMM-WiDance achieve mild accuracy for all directions. The accuracies of oblique directions and straight directions achieved by HMM-WiDance are comparable. As trained with real samples, HMM-WiDance is able to differentiate directions at global scale, while modeling small deviations at local scale. Specifically, the fluctuations of Doppler shifts when the player moves in parallel with the link are successfully modelled by HMM. However, HMM-WiDance suffers from the common over-fitting problem. For example, the accuracy of actions with rear direction decreases when applying HMM-WiDance instead of WiDance.

Performance of extraction scheme. To demonstrate the uniqueness and evaluate the performance of extraction of Doppler frequency shifts in WiDance, we compare WiDance with CARM. Note that we can omit the impact of difference of recognition methods used by WiDance and CARM, as these methods have comparable performance, as indicated by the comparison between WiDance and HMM-WiDance above.

Figure 8c shows the confusion matrix for CARM. CARM fails to recognize actions in several directions, and achieves only 60% accuracy even after carefully tuning the HMM parameters. This is because CARM is based on CSI power and only obtains the absolute values of Doppler shifts, due to loss of imagery part of the signal. Theoretically, if we just use absolute values of Doppler shifts in the non-learning recognition scheme, then only Doppler ratio can be calculated. As a result, only the first step in non-learning recognition scheme can be carried out, and actions can be classified into three coarse categories: LR/RF, front/right/rear/left, LF/RR. However, there is no more clue to differentiate actions in each category. Clearly, some directions are more confused with directions in the same category, besides the large adjacent errors. For example, the right direction is statistically more confused with the front, rear and left direction, and the left-front direction is more confused with the right-rear direction. However, in practice, directions in the same coarse categories are not totally confused by CARM. For all directions, most actions can be correctly classified by CARM. It is because the actions involve movements of whole body rather than only feet and legs, which can be incomprehensively captured by learning method used in CARM to correctly recognize the majority of actions. However, even with these features cannot CARM fully outline the moving directions of actions, which leads to low recognition accuracy.

Performance of compound gestures. Currently, we choose 9 motion directions as the gesture set to fit the dance game. A natural way to scale the gesture set to enable more HCI applications is to construct compound gestures from the 9 motion directions as primitives, e.g. double-left, front-right. Figure 9 shows the performance of WiDance in recognizing compound gestures that composes two primitive actions. WiDance achieves an overall accuracy of 85%, which is slightly lower than that of recognizing primitive actions. And the accuracy of recognizing compound gestures ranges from 71.4% to 100%. Such diversity in accuracy shows the bias of gesture recognition of WiDance. As a result, it is better for real users to conduct pre-training operations to select gestures with high recognition accuracy for practical use. For example, as shown in Figure 9, 33 out of 64 gestures have recognition accuracy higher than 85%, which can be selected to form a larger gesture set than that of 9 primitive actions.

# Parameter Study

Impact of user diversity. To evaluate the robustness of WiDance for various users, we recruit 30 participants (17 males, 13 females) to test WiDance. Figure 12 shows the statistics of participants. The participants have various heights, weights and somatotype, as indicated by Body Mass Index (BMI). Note that the participants also have different levels of body coordination and familiarity with dancing games. Figure 12 shows the performance of WiDance with different participants. WiDance recognizes actions of all participants with accuracy higher than 85%, without any beforehand per-person learning. However, the result shows no clear correlation between user types and performance of WiDance, the further study of which is leaved as future work.

![](images/fa33083cdc2182f30d5ed6e3e2553948ead60560c37d3f50db93eeda348519ac.jpg)



Figure 11. Statistics of participants.

![](images/8f0a5e860309a51826ff89ba819c8cc90d3bd0c53c5cfa1c99abf0a4f2de9e59.jpg)



Figure 12. Impact of user diversity.

![](images/09e71401fbb56b7b18a5e08afcdcbc054bbebf38c343bffd5aa19c3060146d3e.jpg)



Figure 13. Impact of action range.

![](images/4ea1885a742fc138e329b8f415eee0a9600fb5c61c6a8e731b82d46ea69237ed.jpg)



Figure 14. Impact of interval.

![](images/2f83776b7e0c3d2a80c2dd46d62b9d864f54034115b47630ac369335efe992f9.jpg)



Figure 15. Impact of area size.

![](images/8ddf00e26dae0a94ca6e63d1090bd4c443e7a53cd585c3c554e0d168568b5b59.jpg)



Figure 16. Impact of packet rate.

![](images/5d4c2e47aadaa907d0817da0b939d20ba1023a830993ea4f56bde6677d46daca.jpg)



Figure 17. Computation overhead.

Impact of action range. We evaluate the sensitivity of WiDance by asking participants to perform actions with various ranges from 0.3m to 0.9m. Note that a range of 0.3m is comparable to the working range of dancing mats, and a range of 0.9m is almost the extreme range that participants can achieve with the limit of both leg length and note interval length. As shown in Figure 13, WiDance maintains consistent high accuracy of 92% when the action range is larger than 0.6m, and slightly degrades to 86% when the range decreases to 0.5m. However, with further decreasing of action range, the accuracy dramatically decreases. It is consistent with the analysis that smaller action ranges leads to shorter actions time and smaller action speed, making it harder to extract Doppler frequency shifts from spectrogram.

Impact of note interval. In real dancing exergames, visual notes appear with various intervals. To evaluate the performance of WiDance with different note intervals, we conduct experiments with intervals from 1s to 3s. Note that most novices need repetitive practices to catch up with notes with interval less than 2s. For notes with about 1s interval, users have to perform actions promptly in natural amplitudes without stop to catch up with the notes. As shown in Figure 14, WiDance achieves the highest accuracy of 97% with an interval of 1.5s. When the note interval is set to 1s, the accuracy sharply decreases to 84%. The reason is that the interval is too short for players to complete each individual action. Instead, they struggle to catch up with the fast visual notes, and stride with their bodies in an uncontrolled way, which interferes the Doppler frequency shifts of interest. Conversely, when the time interval is longer than 1.5s, the accuracy slightly decreases to about 92%. It is because with a larger interval, players are able to slowly stride during the interval, causing a smaller Doppler frequency shifts that may be interfered with noises.

Impact of area size. We evaluate WiDance in monitoring areas with sizes of 2m 2m, 3m 3m, 4m 4m. Figure 15 plots the performance of WiDance. As shown, even with an area of as large as 16m2, WiDance still achieves an accuracy of 90%. While the size of existing dancing pads is only about 1m 1m, WiDance enables a large exercising area for players. Players can perform macro actions in the area, which is more helpful for their fitness and health.

Impact of transmission rates. As WiDance requires packets transmission for sensing actions, which may occupy channels and interfere normal communication links, we evaluate the performance of WiDance with different transmission rates. Initially, we set the transmission rate to 1024Hz and decimate the CSI series to 512, 256, 128Hz. As shown in Figure 16, with decreasing of transmission rate, the performance of WiDance slightly degrades, as the high-frequency noises aliases with Doppler frequency of interest. However, WiDance still achieves acceptable performance at the transmission rate of 256Hz. Since only the CSIs of packets are used, WiDance can transmit even short packets (e.g. RTS/CTS) to further reduce the impact on the normal communication channel.

A side effect of using lower transmission rate is reduction of processing time cost. Figure 17 plots the per-second computation cost of each step in WiDance. As shown, the major time cost comes from generating spectrogram in the step of timefrequency analysis. By reducing the transmission rate by half, the data amount and thus the processing time reduce by half. With a practical transmission rate of 256Hz, the processing time for a single action is only 25ms, thus enabling real-time processing and reaction of WiDance.

# LIMITATIONS AND DISCUSSION

Multiple moving objects. Targeting single-player dancing, WiDance is unfortunately vulnerable to movements nearby, since reflections from both dancer and intruder are superimposed at receiver. WiTrack [2] enables multiple human tracking by successive silhouette cancellation using FMCW signals. However, it relies on separation of distance and azimuth of multiple objects, which is not feasible for WiDance, in that the Doppler shift of the dancer is obfuscated by the similar shift of the intruder. Enabling recognition of multiple objects still remains an open and challenging problem in future.

Dependency on particular hardware cards. CSI is formulated in 802.11 standards for OFDM and MIMO operations. However, accessing CSI is limited to certain NICs with modified drivers (e.g. Intel 5300). An alternative to reduce specific devices is to configure a Wi-Fi device with Intel 5300 NIC as a hotspot and send ICMP packets to collect CSIs from multiple other normal Wi-Fi clients [16]. In this way, only one device with specific NIC is needed. Moreover, as CSI-based Wi-Fi sensing applications continue to explode and mature, we envision future NIC manufacturers will expose CSI to upper layers on most NICs in 3-5 years.

Detection range. While WiDance supports up to 4m 4m interaction range, achieving whole-home coverage is not an easy task. As the operation distance increases, (1) The reflected power attenuates exponentially while the interference from static signals and noises remains unchanged; (2) The field of directions with Doppler shifts over the sensitivity continuously narrows. Given the lowest SINR and sensitivity of an NIC, these two factors determines the maximum coverage of the system. Nevertheless, whole-home can still be achieved by deploying more systems in the area of interest, or by sensing actions with larger Doppler frequency shifts (e.g. walking).

Potential applications. The core technology of WiDance is to derive motion directions in a device-free manner, which can be applied to various scenarios. In addition to games, it facilitates smart home applications such as remote device selection and control. For example, a user can select a lamp by moving his/her arm towards it, and he/she can control the volume of a speaker by pushing towards or polling away from it. It also benefits localization to eliminate ambiguity in walking directions [17], which enables a range of locationbased services such as emergency evacuation, virtual reality and activity tracking. We leave the study on these applications for future work.

# RELATED WORK

Wireless Sensing Systems. As an alternative of computer vision in NLOS or dark environments, contactless sensing using wireless signals has attracted extensive interests in recognizing location [4, 3, 2, 25], body activities [22, 32, 12], and vital signs [5, 19, 29, 33]. These systems mainly adopt a radar principle by associating motions with physical measurements such as time-of-flight and Doppler effects, and enable finegrained and interpretable motion tracking using specialized hardware. For instance, mTrack [32] accurately locates and tracks finger movement using customized millimeter signals. WiSee [22] is the closest to our work, which extracts Doppler shifts in wide-band OFDM signals using USRPs. WiDance also recognizes motion directions by modeling and interpreting motion-induced Doppler effects. However, WiDance advances the state-of-the-art by extracting Doppler shifts on commercial multi-antenna Wi-Fi devices without any modification.

Wi-Fi-based Gesture Sensing Systems. To bring gesture recognition to commodity Wi-Fi devices, both modeling [1, 30] and pattern matching based principles [31, 28] have been adopted. E-eyes [31] exploits subcarriers of CSI to recognize household activities such as washing dishes and taking a shower. WiGest [1] maps changes in Wi-Fi RSSI into motion primitives, upon which a family of gestures are defined and accurately recognized for device interaction. WiDir [34] proposes to recognize human motion direction by calculating phase differences between CSI subcarriers. In contrast, WiDance directly extract Doppler frequency shift with multiple antennas available on commercial Wi-Fi devices, which may serves a wide range of sensing applications than human motion direction. CARM [30] extracts speed-related features from CSI and proposes an effective machine learning framework for CSI-based activity recognition. WiDance is built upon this trend of research, and makes one step further by modeling motion directions and extracting the corresoponding Doppler features from noisy CSI, enabling contactless dancing exergame without the need of prior machine learning.

Interfaces for Exergames. Exergame enables physical interaction with users for exercise benefits [26, 10]. Mainstream exergame interfaces are based on either computer vision [24, 11] or controller embedded with sensors [14, 7]. Kinect Sports and Wii Fit are the leading gaming consoles for indoor exergames. ACW [13] combines computer vision and interactive projected graphics for motivating and instructing indoor wall climbing. RetroFab [23] leverages 3D printing technique to agilely adapt physical controllers to arbitrary use. In contrast, wireless sensing with off-the-shelf devices complements shortages of vision-based and sensor-based sensing. We develop a new wireless based exergame interface that tracks body movements and reactions through Doppler effect, and validate the efficiency of the interface by prototyping a dancing game on it. While preliminary, we believe that WiDance opens up a new direction for design and development of exergame interfaces.

# CONCLUSION

In this paper, we propose WiDance, a Wi-Fi-based user interface for contactless dance-pad exergame. First, we design a novel algorithm to extract motion-induced Doppler shifts leveraging antenna diversity on commodity Wi-Fi devices. Then, we model the relation between Doppler shifts and motion directions, and propose a light-weight yet effective signal processing pipeline to translate the model into the interactive dancing exergame. Extensive experimental results show that WiDance achieves an overall recognition accuracy of 92% in various indoor environments. Requiring no hardware modifications, WiDance is envisioned as a promising step towards practical wireless human-computer interface, which underpins new insights for future wireless sensing applications.

# ACKNOWLEDGEMENTS

This work is supported in part by the NSFC under grant 61522110, 61332004, 61672319, 61632008, National Key Research Plan under grant No. 2016YFC0700100.

# REFERENCES

1. Heba Abdelnasser, Moustafa Youssef, and Khaled A Harras. 2015. Wigest: A ubiquitous wifi-based gesture recognition system. In Proc. of IEEE INFOCOM.   
2. Fadel Adib, Zachary Kabelac, and Dina Katabi. 2015. Multi-person localization via rf body reflections. In Proc. of USENIX NSDI.   
3. Fadel Adib, Zach Kabelac, Dina Katabi, and Robert C Miller. 2014. 3d tracking via body radio reflections. In Proc. of USENIX NSDI.   
4. Fadel Adib and Dina Katabi. 2013. See through walls with wifi!. In Proc. of ACM SIGCOMM.   
5. Fadel Adib, Hongzi Mao, Zachary Kabelac, Dina Katabi, and Robert C Miller. 2015. Smart homes that monitor breathing and heart rate. In Proc. of ACM CHI.   
6. Kamran Ali, Alex Xiao Liu, Wei Wang, and Muhammad Shahzad. 2015. Keystroke recognition using wifi signals. In Proc. of ACM MobiCom.   
7. Meng-Chieh Chiu, Shih-Ping Chang, Yu-Chen Chang, Hao-Hua Chu, Cheryl Chia-Hui Chen, Fei-Hsiu Hsiao, and Ju-Chun Ko. 2009. Playful bottle: a mobile social persuasion system to motivate healthy water intake. In Proc. of ACM Ubicomp.   
8. Stefan Göbel, Sandro Hardy, Viktor Wendel, Florian Mehm, and Ralf Steinmetz. 2010. Serious games for health: personalized exergames. In Proc. of ACM MM.   
9. Daniel Halperin, Wenjun Hu, Anmol Sheth, and David Wetherall. 2011. Predictable 802.11 packet delivery from wireless channel measurements. In Proc. of ACM SIGCOMM.   
10. Hamilton A Hernandez, Zi Ye, TC Graham, Darcy Fehlings, and Lauren Switzer. 2013. Designing action-based exergames for children with cerebral palsy. In Proc. of ACM CHI.   
11. Leo Holsti, Tuukka Takala, Aki Martikainen, Raine Kajastila, and Perttu Hämäläinen. 2013. Body-controlled trampoline training games based on computer vision. In Proc. of ACM CHI.   
12. Kiran Joshi, Dinesh Bharadia, Manikanta Kotaru, and Sachin Katti. 2015. Wideo: Fine-grained device-free motion tracing using rf backscatter. In Proc. of USENIX NSDI.   
13. Raine Kajastila, Leo Holsti, and Perttu Hämäläinen. 2016. The Augmented Climbing Wall: High-Exertion Proximity Interaction on a Wall-Sized Interactive Surface. In Proc. of ACM CHI.   
14. Dagmar Kern, Mark Stringer, Geraldine Fitzpatrick, and Albrecht Schmidt. 2006. Curball–A Prototype Tangible Game for Inter-Generational Play. In Proc. of IEEE WETICE.   
15. Mallory Ketcheson, Luke Walker, and TC Graham. 2016. Thighrim and Calf-Life: a study of the conversion of off-the-shelf video games into exergames. In Proc. of ACM CHI.

16. Mengyuan Li, Yan Meng, Junyi Liu, Haojin Zhu, Xiaohui Liang, Yao Liu, and Na Ruan. 2016. When CSI Meets Public WiFi: Inferring Your Mobile Phone Password via WiFi Signals. In Proc. ACM SIGSAC CCS.   
17. Alex T Mariakakis, Souvik Sen, Jeongkeun Lee, and Kyu-Han Kim. 2014. SAIL: single access point-based indoor localization. In Proc. of ACM MobiSys.   
18. Pedro Melgarejo, Xinyu Zhang, Parameswaran Ramanathan, and David Chu. 2014. Leveraging directional antenna capabilities for fine-grained gesture recognition. In Proc. of ACM Ubicomp.   
19. Phuc Nguyen, Xinyu Zhang, Ann Halbower, and Tam Vu. 2016. Continuous and Fine-grained Breathing Volume Monitoring from Afar Using Wireless Signals. In Proc. of IEEE INFOCOM.   
20. Wei Peng, Jih-Hsuan Lin, and Julia Crouse. 2011. Is playing exergames really exercising? A meta-analysis of energy expenditure in active video games. Cyberpsychology, Behavior, and Social Networking 14, 11 (2011), 681–688.   
21. John G Proakis. 1995. Digital communications. McGraw-Hill, New York (1995).   
22. Qifan Pu, Sidhant Gupta, Shyamnath Gollakota, and Shwetak Patel. 2013. Whole-home gesture recognition using wireless signals. In Proc. of ACM MobiCom.   
23. Raf Ramakers, Fraser Anderson, Tovi Grossman, and George Fitzmaurice. 2016. Retrofab: A design tool for retrofitting physical interfaces using actuators, sensors and 3d printing. In Proc. of ACM CHI.   
24. Kyle Rector, Cynthia L Bennett, and Julie A Kientz. 2013. Eyes-free yoga: an exergame using depth cameras for blind & low vision exercise. In Proc. of ACM SIGACCESS.   
25. Longfei Shangguan, Zheng Yang, Alex X Liu, Zimu Zhou, and Yunhao Liu. 2016. STPP: Spatial-Temporal Phase Profiling-Based Method for Relative RFID Tag Localization. IEEE/ACM Transactions on Networking (2016).   
26. Mike Sheinin and Carl Gutwin. 2014. Exertion in the small: improving differentiation and expressiveness in sports games with physical controls. In Proc. of ACM CHI.   
27. Amanda E Staiano and Sandra L Calvert. 2011. Exergames for physical education courses: Physical, social, and cognitive benefits. Child development perspectives 5, 2 (2011), 93–98.   
28. Sheng Tan and Jie Yang. 2016. WiFinger: leveraging commodity WiFi for fine-grained finger gesture recognition. In Proc. of ACM MobiHoc.   
29. Hao Wang, Daqing Zhang, Junyi Ma, Yasha Wang, Yuxiang Wang, Dan Wu, Tao Gu, and Bing Xie. 2016. Human Respiration Detection with Commodity WiFi Devices: Do User Location and Body Orientation Matter?. In Proc. of ACM Ubicomp.

30. Wei Wang, Alex X Liu, Muhammad Shahzad, Kang Ling, and Sanglu Lu. 2015. Understanding and modeling of wifi signal based human activity recognition. In Proc. of ACM MobiCom.   
31. Yan Wang, Jian Liu, Yingying Chen, Marco Gruteser, Jie Yang, and Hongbo Liu. 2014. E-eyes: device-free location-oriented activity identification using fine-grained wifi signatures. In Proc. of ACM MobiCom.   
32. Teng Wei and Xinyu Zhang. 2015. mtrack: High-precision passive tracking using millimeter wave radios. In Proc. of ACM MobiCom.   
33. Chenshu Wu, Zheng Yang, Zimu Zhou, Xuefeng Liu, Yunhao Liu, and Jiannong Cao. 2015. Non-invasive detection of moving and stationary human with wifi. IEEE Journal on Selected Areas in Communications (2015).   
34. Dan Wu, Daqing Zhang, Chenren Xu, Yasha Wang, and Hao Wang. 2016. WiDir: Walking Direction Estimation Using Wireless Signals. In Proc. of ACM Ubicomp.