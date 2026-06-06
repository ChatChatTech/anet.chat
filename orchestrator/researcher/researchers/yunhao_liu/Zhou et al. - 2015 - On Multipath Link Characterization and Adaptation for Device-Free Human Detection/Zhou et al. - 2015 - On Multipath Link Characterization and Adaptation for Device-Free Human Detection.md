# On Multipath Link Characterization and Adaptation for Device-free Human Detection

Zimu Zhou $^{*}$ , Zheng Yang $^{\dagger}$ , Chenshu Wu $^{\dagger}$ , Yunhao Liu $^{\dagger}$ and Lionel M. Ni $*^{\ddagger}$

\*Department of Computer Science and Engineering, Hong Kong University of Science and Technology

$^{\dagger}$ School of Software and TNList, Tsinghua University

$^{\ddagger}$ Department of Computer and Information Science, University of Macau

{zhouzimu, yang, wu, yunhao}@greenorbs.com, ni@umac.mo

Abstract—Wireless-based device-free human sensing has raised increasing research interest and stimulated a range of novel location-based services and human-computer interaction applications for recreation, asset security and elderly care. A primary functionality of these applications is to first detect the presence of humans before extracting higher-level contexts such as physical coordinates, body gestures, or even daily activities. In the presence of dense multipath propagation, however, it is non-trivial to even reliably identify the presence of humans. The multipath effect can invalidate simplified propagation models and distort received signal signatures, thus deteriorating detection rates and shrinking detection range. In this paper, we characterize the impact of human presence on wireless signals via ray-bouncing models, and propose a measurable metric on commodity WiFi infrastructure as a proxy for detection sensitivity. To achieve higher detection rate and wider sensing coverage in multipath-dense indoor scenarios, we design a lightweight subcarrier and path configuration scheme harnessing frequency diversity and spatial diversity. We prototype our scheme with standard WiFi devices. Evaluations conducted in two typical office environments demonstrate a detection rate of 92.0% with a false positive of 4.5%, and almost 1x gain in detection range given a minimal detection rate of 90%.

# I. INTRODUCTION

Recent advances in wireless techniques have extended the abstraction of wireless channels from a sole communication medium to a vehicle for device-free human sensing. It works by analyzing human-induced radio shadowing and reflection conveyed in received signals to detect, localize or track the presence of humans, while users carry no radio-enabled devices [1]–[5]. Unlike conventional paradigms using cameras, infrared detectors or wearable devices, wireless-based device-free human sensing reuses the ubiquitously deployed wireless infrastructure, operates in a non-invasive and privacy-preserving mode, and can work through-walls and in dim lighting. In addition to extracting physical coordinates for location-based services, pioneering work has also succeeded in identifying higher-level contexts such as gestures [6], [7], location-aware activities [8] and breath monitoring [9], [10].

For device-free human sensing to excel indoors, multipath propagation lurks as a major concern. As these applications assume that users carry no radio-enabled devices, a primary step towards higher-level human sensing tasks is to first detect the motion or the presence of the target users. Detecting human presence is relatively easy with a strong Line-Of-Sight (LOS) path along a wireless link in an open area. Yet offices, homes, shopping malls, and the like are often enclosed and have twisted corridors, capsuled rooms piled with furniture and commodity goods, creating multiple intricate propagation paths. Such a multipath propagation phenomenon can invalidate theoretical propagation models $[11]$ , distort received signal signatures $[12]$ , and fundamentally constrain the sensitivity and coverage of a wireless link even when inferring the presence of humans $[13]$ – $[15]$ . To explicitly eliminate any adverse impact of multipath propagation, researchers resort to customized signals $[5]$ and specialized software-defined radios $[6]$ for radar-like signal processing. To enable device-free applications on commodity infrastructures, existing approaches exploit a dense deployment of wireless links $[4]$ , $[12]$ , where each link can only detect a human presence along the LOS path.

In this paper, we ask the question: Instead of avoiding multipath to tradeoff detection reliability with sensing coverage, can we harness multipath for a higher detection rate and wider sensing range with standard WiFi devices? We do an in-depth analysis on how human presence alters wireless signals under different propagation mechanisms, and demonstrate that (1) human-induced reflections potentially extend detection range; (2) multipath superposition status can lead to varied detection sensitivity. To deliver these observations into practical solutions for wider coverage and higher detection rates, multiple challenges arise. (1) How to characterize and adjust detection sensitivity via measurable metrics and configurable settings on commercial WiFi infrastructure? (2) How to distinguish and further optimize reflected paths to extend detection range?

To address the above challenges, we take advantage of two trends: (1) Channel State Information (CSI) offered by IEEE 802.11a/g/n standards depicts multipath propagation at the granularity of OFDM subcarriers [16] in the frequency domain. (2) An increasing number of commercial wireless devices have been manufactured with multiple antennas to bolster capacity [17], bringing in an orthogonal dimension to discern multipath components from the spatial domain.

Through ray-bouncing model analysis and real-world measurements, we derive the multipath factor as a proxy for detection sensitivity, which is directly measurable at runtime from one packet. We demonstrate the feasibility to predict and improve detection sensitivity using the multipath factor metric and the frequency diversity offered by OFDM signals. Since the detection coverage is often constrained by the impact of human presence on Non-Line-Of-Sight (NLOS) paths, it is natural to emphasize the impact of reflected paths for wider coverage. The prerequisite, however, is to distinguish NLOS and LOS paths, which is no easy task for the bandwidth-limited WiFi. The key insight here is to utilize multiple antennas and discern the LOS path from others by identifying the arriving angles. As a proof-of-concept application, we design a lightweight subcarrier and path configuration scheme for device-free human detection. We prototype our scheme with commercial WiFi Network Interface Cards (NICs) and validate its viability in typical office environments. Extensive evaluations demonstrate a detection rate of 92.0% and a corresponding false positive of 4.5% with around 1x gain in detection range given a minimal detection rate of 90% in two office scenarios.

The main contributions are summarized as follows:

- We characterize and measure the diverse impact of human presence on multipath links via PHY layer CSI, and propose a directly measurable and configurable proxy for detection sensitivity on commodity WiFi devices. We envision this work to provide guidelines for infrastructure assessment and deployment of wireless device-free human sensing applications.   
- We harness frequency and spatial diversity to tune detection sensitivity and coverage. The proposed schemes are lightweight and compatible with WiFi standards, thus enabling pervasive adoption.   
- We prototype our schemes with commercial WiFi NICs and validate them in different indoor environments. Experimental results demonstrate a 30% improvement in detection rate and 1x enhancement in coverage compared with baseline CSI-based detection schemes.

We first provide a preliminary in Section II, characterize the impact of human presence on multipath links in Section III, and then detail our subcarrier and path configuration scheme in Section IV. Section V presents the detailed performance evaluation. We review the related work in Section VI and conclude this work in Section VII.

# II. PRELIMINARIES

Wireless-based device-free detection identifies human presence by radio devices deployed in-advance, while the target carries no devices $[1]$ . It relates the impact of human presence to certain changes of the received signals. This impact is often modeled as human-induced shadowing along the LOS path. In the presence of multipath propagation, such an oversimplified model may lead to contradictory link behaviors $[14]$ and unreliable detection results $[12]$ . In this section, we qualitatively illustrate how human presence affects a multipath link via different propagation mechanisms, and briefly review channel information available on commodity WiFi devices.

![](images/50a5d689cd6414d2d2c9a315fdc968ffb620ebc242bf695af49ce26848b682d1.jpg)  
Fig. 1. An illustration of human presence across a wireless link: (a) Ideal model only considers only the impact of shadowing; (b) In multipath-rich indoor scenarios, human presence affects a link via either shadowing or reflection; A multipath link (c) with no human presence, (d) with human shadowing and (e) with human-induced reflection.

# A. Multipath Propagation and Device-free Detection

Radio signals can propagate to the receiver via reflection, diffraction and scattering. As the size of a typical human body is larger than the wavelength of WiFi signals, shadowing dominates the impact when a person blocks the LOS path while reflection dictates with human presence near the transmitter-receiver (TX-RX) link $[14]$ . Most device-free detection models assume that signals propagate via the LOS path only. For instance, when a person traverses a link from A to C as in Fig. 1a, the Received Signal Strength (RSS) is expected to drop dramatically only when the person obstructs the LOS path at B. In multipath-dense indoor environments, however, human presence alters signal propagation in a more sophisticated manner. As illustrated in Fig. 1b, human presence may block certain reflected paths at A or create a new reflected path near the link at C. Even with human presence along the LOS path at B, the RSS may experience either a drop or an increase due to different phase superposition. In summary, multipath brings new opportunities for device-free human detection:

- Both environment and human induced reflections potentially expand the detection range.   
- Different multipath superposition states may lead to varied detection sensitivity.

To harness multipath propagation for a wider detection range and higher detection sensitivity, we first review channel measurements available on commercial WiFi devices.

# B. Channel State Information

A multipath wireless channel is often portrayed as Channel Impulse Response (CIR), which is a linear filter $h(\tau)$ :

$$
h (\tau) = \sum_ {i = 0} ^ {N - 1} a _ {i} e ^ {- j \theta_ {i}} \delta (\tau - \tau_ {i}) \tag {1}
$$

where $a_{i}, \theta_{i}, \tau_{i}, N, \delta(\tau)$ , denote the amplitude, phase, delay of the $i^{th}$ path, the number of paths, and the Dirac delta function, respectively. The Fourier Transform of CIR, $H(f) = \mathfrak{F}(h(\tau))$ , is called Channel Frequency Response (CFR). Leveraging commodity NIC with a modified driver, a discrete version of CFR, $\hat{H} = \{H(f_k)\}$ is revealed to upper layers in the format of Channel State Information (CSI) [16], where each $H(f_{k})$ is a complex number depicting the amplitude and the phase of subcarrier $f_{k}$ .

![](images/6253d35cc646029104ce0e1428b6327ed93dc7a8b219004537343a669b2d0e17.jpg)



(a) RSS change with different human locations.

![](images/be71d0382a450e9132fb1a965501a64962f168cab5ec312666f5e1e728ea2e20.jpg)



(b) RSS change across subcarriers.   
Fig. 2. An illustration of diverse RSS change trends in multipath-dense indoor scenarios. (a) CDF of RSS change measured with 500 different human presence locations. (b) RSS from 1000 packets measured when a person moves across a 4m link. The left figure demonstrates that human-induced RSS change varies across the 30 subcarriers and over time. The right figure shows the RSS change trends differ on two specific subcarriers. Subcarrier 15 mainly exhibits RSS drop due to human motion while subcarrier 25 experiences either RSS drop or RSS rise with different human locations.

Compared with MAC layer RSS, CSI portrays a finer-grained temporal and spectral structure of wireless links. In the subsequent sections, we explore to extract measurable metrics and configurable parameters from CSI to characterize and adjust link sensitivity and range for device-free detection.

# III. LINK CHARACTERISTICS ANALYSIS

In general, device-free human detection schemes work in two steps: calibration and monitoring. During calibration, the receiver measures and stores the RSS when there is no human presence, denoted as $s^{(0)}$ . Then at the monitoring stage, the receiver measures a RSS sequence $s = \{s^{(t)}\}_{t=1}^{T}$ , and infers the presence of a human by comparing whether the RSS difference $\Delta s^{(t)} = s^{(t)} - s^{(0)}$ exceeds a pre-defined threshold. Typically, the mean of the RSS difference is used to detect stationary targets, while the corresponding variance is adopted for mobile targets [18]. In outdoor scenarios, human presence dominates the impact on $\Delta s$ and often induces a notable drop in RSS. In multipath-dense indoor environments, however, human presence is no longer the only influencing factor on $\Delta s$ . Since multipath components can superpose either constructively or destructively, $\Delta s$ can vary even for human presence at a fixed location. In this section, we demonstrate through measurements that a multipath link reacts differently to human presence, and further analyze the link characteristics via an one-bounce multipath propagation model.

# A. Measuring Impact of Human on a Multipath Link

We use a Tenda W3000R wireless router as the transmitter operating in IEEE 802.11n AP mode at 2.4GHz Channel 11. A mini PC equipped with Intel 5300 NIC and the CSI tool [16] is employed as the receiver pinging packets from the AP. A group of 30 CSIs are extracted from each data packet. We fix the TX-RX distance to 4m and collect CSI data for (1) 500 static human presence locations both along the LOS path and in the vicinity of the LOS path, and (2) a person moving across the link. We also collect CSIs when there is no human present within the monitored area. The measurements are conducted in a 6m x 8m classroom.

Fig. 2a plots the Cumulative Distribution Function (CDF) of the measured subcarrier RSS change (i.e. $\Delta s$ ) for the 500 human presence locations. Unlike a LOS link, where human presence is expected to induce notable RSS drop, a multipath link exhibits diverse RSS change trends in response of human presence. Fig. 2b plots the subcarrier RSS changes when a person moves across the link. As is shown, not all subcarriers suffer from a drop in RSS when the person moves near the link (e.g. subcarrier $f_{25}$ exhibits notable RSS rise at packet 450 to 600). In addition, while the subcarriers may behave similarly at certain time stamps (e.g. both subcarrier $f_{15}$ and $f_{25}$ see dramatic RSS drop around packet 350), yet differ at other time periods (e.g. RSS decreases on subcarrier $f_{15}$ yet increases at subcarrier $f_{25}$ from packet 450 to 600). Also the RSS change trend may fluctuate even for the same subcarrier.

The seemingly uncertain link reactions to human presence tend to break down the basic assumption of RSS mean based device-free detection applications, and motivate us to take a deeper analysis on the characteristics of a multipath link.

# B. Characterizing Multipath Link Behaviors

To facilitate quantitative analysis, we consider a simplistic case where signals propagate via the LOS path and a single-bounce reflection as in Fig. 1c. When no one is present near the link, the corresponding CIR can be represented as:

$$
h _ {N} = a _ {L} e ^ {- j \phi_ {L}} + a _ {R} e ^ {- j \phi_ {R}} \tag {2}
$$

where $a_{L}$ , $a_{R}$ , $\phi_{L}$ , and $\phi_{R}$ are the amplitudes and phases of the LOS and reflected paths, respectively.

To indicate the phaser superposition status of multipath components, we define a multipath factor $\mu$ as the ratio between the power of the LOS path and the total power when there is no person around. Denote $\gamma = \frac{a_{L}}{a_{R}} > 1$ as the ratio between the amplitudes of the LOS path and the reflected path, and further suppose that the receiver is synchronized to the transmitter, i.e. $\phi_{L} = 0$ . Let $\phi_{R} = \phi$ . Then the multipath

![](images/68c2232a7a5d9f96d372c86c892fe434b6e50640e8ab7a6991342265f1f43356.jpg)



(a) Multipath factor distribution.

![](images/895548956d6367f5793a96dec060d67998d6e5347276ddda7e9c630ec0c54335.jpg)



(b) Multipath factor vs. RSS change.

![](images/48e41dc5bd697d1621d15606d3d4436b53b8ec13ffabb8338a3cdb9c82eeaa3a.jpg)



(c) Fitting across frequency.   
Fig. 3. Measurements of multipath factor and its relationship with RSS change along a 4m link from 500 human presence locations. (a) Distribution of multipath factor of all the 500 locations. (b) An illustration of the relationship between RSS change and multipath factor with logarithmic fitting at Subcarrier $f_{5}$ . (c) The fitting results at 5 separated subcarriers.

factor $\mu$ can be substituted as:

$$
\mu = \left(\frac {a _ {L}}{h _ {N}}\right) ^ {2} = \frac {\gamma^ {2}}{\gamma^ {2} + 1 + 2 \gamma \cos \phi} \tag {3}
$$

We analyze the impact of $\mu$ on $\Delta s$ for both human-induced shadowing and reflection.

1) Shadowing: When a person obstructs the LOS path as in Fig. 1d, shadowing dominates the impact [19]. Assume the amplitude and phase of the shadowed LOS path are $a_L'$ and $\phi_L'$ . Then the CIR under human-induced shadowing is:

$$
h _ {S} = a _ {L} ^ {\prime} e ^ {- j \phi_ {L} ^ {\prime}} + a _ {R} e ^ {- j \phi_ {R}} \tag {4}
$$

Since human body is often modeled as a dielectric elliptic cylinder [19] and human tissues have sizes no larger than the WiFi wavelength, the impact of human presence on the LOS path can be simplified as solely amplitude attenuation by $\beta = \frac{a_L'}{a_L} < 1$ , while the phase is deterministic, hence $\phi_{L} = 0$ [20]. Thus the link sensitivity under human-induced shadowing $\Delta s_S$ (measured in dB) can be approximated as:

$$
\Delta s _ {S} = 1 0 \lg \left(\frac {h _ {S}}{h _ {N}}\right) ^ {2} = 1 0 \lg \frac {\beta^ {2} \gamma^ {2} + 1 + 2 \beta \gamma \cos \phi}{\gamma^ {2} + 1 + 2 \gamma \cos \phi} \tag {5}
$$

Note that the phase shift of the reflected path with respect to the direct path, $\phi$ , is error-prone to noise and hardware uncertainties with commodity WiFi devices, we substitute $\phi$ by the multipath factor $\mu$ , whose measurement is comparatively more stable and accurate:

$$
\Delta s _ {S} = 1 0 \lg \left[ \beta + (1 - \beta) \left(\frac {1 - \beta \gamma^ {2}}{\gamma^ {2}}\right) \mu \right] \tag {6}
$$

2) Reflection: When a person moves in the proximity to the LOS path as in Fig. 1e, he tends to create a new single-bounce reflected path with amplitude $a_{R}^{\prime}$ and phase $\phi_R^\prime$ . Accordingly, the CIR under human-created reflection is:

$$
h _ {S} = a _ {L} e ^ {- j \phi_ {L}} + a _ {R} e ^ {- j \phi_ {R}} + a _ {R} ^ {\prime} e ^ {- j \phi_ {R} ^ {\prime}} \tag {7}
$$

Suppose $\eta = \frac{a_R'}{a_R}$ and $\Phi_R' = \phi'$ . The corresponding link sensitivity $\Delta s_R$ (measured in dB) can be calculated as:

$$
\begin{array}{l} \Delta s _ {R} = 1 0 \lg \left(\frac {h _ {R}}{h _ {N}}\right) ^ {2} \tag {8} \\ = 1 0 \lg \left\{1 + \frac {\eta^ {2} + 2 \eta [ \gamma \cos \phi^ {\prime} + \cos (\phi^ {\prime} - \phi) ]}{\gamma^ {2}} \mu \right\} \\ \end{array}
$$

3) Discussions: We make the following discussions on the link sensitivity models derived above.

Diverse Link Behaviors. With a single LOS path along the wireless link, human presence poses a drop in RSS by $\Delta s = 10 \lg \beta^{2} < 0$ (since $\beta < 1$ ). However, as shown in Eq. 5 and Eq. 8, $\Delta s$ can be either negative (i.e. RSS decreases) or positive (i.e. RSS increases) for a multipath link. For instance, if the phase shift $\phi$ is large enough such that $\cos \phi < -\frac{\gamma(\beta+1)}{2}$ , then $\Delta s_{S} > 0$ and hence human presence along the LOS path incurs an increase in RSS. A multipath link may also improve detection sensitivity compared with solely a LOS path. For example, if $\cos \phi < -\frac{1+\beta}{2\beta\gamma}$ , then $|\Delta s_{S}| > |10 \lg \beta^{2}|$ .

Predictable Link Characteristics. Given a multipath link and certain human presence location, the amplitude attenuation and phase shifts of all propagation paths are fixed. Thus the amplitude ratio $\gamma$ is determined by the environmental-constants including propagation distances, reflection and path loss coefficients [20]. The human-induced attenuation ratio $\beta$ can be pre-calculated via human body models [19]. Therefore, the link sensitivity changes approximately logarithmically with the multipath factor, and the multipath factor may act as a proxy for link sensitivity to human presence in a particular multipath superposition status.

Configurable Link Sensitivity. For a fixed human presence location, link detection sensitivity $\Delta s$ is proportional to the multipath factor $\mu$ . A key observation to adjust sensitivity is that the status of multipath superposition not only relates to the spatial characteristics of propagation paths, but is also a function of frequency. Specifically, note $\phi = \frac{2\pi f \Delta d}{c}$ , where f, $\Delta d$ , and c denote the signal frequency, the excess propagation distance of the reflected path, and the speed of light, respectively. Hence according to Eq. 3, Eq. 6 and Eq. 8, both the multipath factor $\mu$ and the link sensitivity $\Delta s$ are configurable if multiple frequencies are available.

In summary, we demonstrate through measurements and analysis that a wireless link may react differently to human presence due to varied multipath superposition status and we explore directly measurable and tunable proxy for such link characteristics in the subsequent sections.

![](images/5d0f1b465a5521016e2021c3c29ac37f687d3b11c4250f579aa8ac21b00ffe64.jpg)



![](images/4028c3f09cebd27bbbcee697389533a9af714bf2cfce9163c3cbe70a110c8ac6.jpg)



(a) Measurements from 2 packets.

![](images/e1e0b4e6138e58717492435f0ac73ee5afccaf3710ec2e6ac106bbba8160489b.jpg)



![](images/9b38e10ccb6c85e13232edbb1771cfb3807bc2446059209da75b03ebfdc7530a.jpg)



(b) Temporal stability with one human location

![](images/c37a9aaf0cd50d5eb797330b3b1095d38393b3e89c6c013db0275478fc7369d1.jpg)



![](images/d2d628de18d62d7836ba317c74853d6cbd5cfd24b6cf33214b0f404cafd6d921.jpg)



(c) Temporal stability with another human location.   
Fig. 4. Temporal stability of multipath factor. (a) Measurements of multipath factor and the corresponding RSS change derived from two packets (Packet 1 and Packet 200) at the same human presence location. (b) Distribution of multipath factor and RSS change of 5000 packets measured with one human presence location. (c) Distribution of multipath factor and RSS change of 5000 packets measured with another human presence location.

# IV. EMBRACING MULTIPATH VIA DIVERSITY

In this section, we exploit both frequency diversity and spatial diversity to tune the detection sensitivity and coverage of a multipath link for device-free human detection.

# A. Improving Sensitivity via Frequency Diversity

The sensitivity of a multipath link can vary for human presence at a fixed location due to the constructive or destructive superposition status. In Section III-B, we show that the multipath superposition status relates to the transmission frequency and is configurable given multiple frequencies. Modern modulation schemes such as OFDM simultaneously transmit information via multiple subcarriers, and naturally offer an opportunity to improve detection sensitivity via frequency diversity. We first interpret how to measure the multipath factor $\mu$ , which acts as a proxy for link sensitivity, and propose a subcarrier weighting scheme for higher detection sensitivity.

1) Measuring Multipath Factor: The multipath factor $\mu$ is defined as the ratio between the power of the LOS path and the total received power. Note in previous analysis, we assume a single frequency. For OFDM-based WiFi signals, we define one multipath factor $\mu_{k}$ for each subcarrier $f_{k}$ . Although the received power can be directly obtained from CSI amplitudes, it is difficult to measure the power of the LOS path for each subcarrier due to limited bandwidth of WiFi. Here we follow previous efforts [11], [21] and use the power of the dominant paths across all subcarriers $|\hat{h}(0)|^{2}$ as an approximation.

To further derive the subcarrier-level LOS power, we harness the fact that the power attenuation for the same transmission channel (the LOS path in our case) is inverse-proportional to the transmission frequency. Specifically, the received signal power radiated in free-space is given by [22]:

$$
P _ {r} = \frac {P _ {t} G _ {t} G _ {r} c ^ {2}}{(4 \pi d) ^ {n} f ^ {2}} \tag {9}
$$

where $P_{r}$ , $P_{t}$ , $G_{r}$ , $G_{t}$ are the received and transmitted signal power, the antenna gains at the receiver and transmitter, respectively. The signals propagate with speed c and frequency f, d is the transmitted distance and n is the environmental attenuation factor. Since in OFDM modulation, the transmission power within the operating band is relatively flat, thus we can assume the same transmission power for each subcarrier. Therefore, the LOS power on subcarrier $f_{k}$ can be calculated as:

$$
P _ {L} (f _ {k}) = \frac {f _ {k} ^ {- 2}}{\sum f _ {i} ^ {- 2}} \cdot | \hat {h} (0) | ^ {2} \tag {10}
$$

where $f_{i}$ is the frequency of the $i^{th}$ subcarrier $^{1}$ . Accordingly, the multipath factor $\mu_{k}$ can be represented as:

$$
\mu_ {k} = \frac {P _ {L} (f _ {k})}{| H (f _ {k}) | ^ {2}} \tag {11}
$$

where $H(f_{k})$ is the complex CSI on subcarrier $f_{k}$ .

We plot the calculated multipath factors using the same measurements as Section III in Fig. 3a. The multipath factors distribute diversely over locations and across subcarriers, which accords with the diverse distribution of RSS change in Fig. 2a. We further illustrate the relationship between the RSS change $\Delta s$ (proxy for detection sensitivity) and the multipath factor $\mu$ (indicator for multipath superposition status) on a single subcarrier in Fig. 3b. As expected, the RSS change roughly falls monotonously with the increase of the multipath factor. Fig. 3c demonstrates the logarithmic fitting results between $\Delta s$ and $\mu$ at 5 separated subcarriers. We only display 5 subcarriers for the following reasons: (1) Ease of demonstration; (2) Adjacent subcarriers often have similar fitting results; (3) Some subcarriers only vary within a small range, which may lead to error-prone fitting. As is shown, the monotonous relationship holds for all subcarriers. Although the fitting results vary, the overall trend remains stable. We make the following comments on the multipath factor:

\- For a particular link and monitoring area, the fluctuation range of each subcarrier varies. This might indicate the impact of human presence on multipath superposition can differ across frequency. Some subcarriers are more sensitive to human presence within the monitoring range and are more distinctive.

![](images/6f7a9e98b0bdb25d8398b9a222828ff48204569730cd42209f2a5fed7ed6fda1.jpg)



(a) Multipath with different angles.

![](images/53729fc13a3ac9a48c773f1c1a0e6bc6949bf31a31ed3561f2f268b6ea1c60a8.jpg)



(b) MUSIC pseudospectrum.

![](images/02f0764f38b5cad77916e4f65590d4e9ebc2a665532e05499d196c98d173a3ac.jpg)



(c) RSS change over different angles.   
Fig. 5. Impact of angle-of-arrival on signal strength along a 3m link. (a) Illustration of multipath propagation with different angle-of-arrival. (b) Pseudospectrum output by MUSIC algorithm with a 3-antenna array. (c) Distribution of subcarrier RSS change along different angle-of-arrival.

\- Although the monotonous decreasing trend roughly holds for all subcarriers, the fitting parameters only fall into a certain range. Therefore it is difficult to deduce consistent evaluating metrics across frequency. However, we will show in the subsequent sections how to leverage such monotonous trend only to adjust link sensitivity at run-time.

To summarize, the multipath factor is directly measurable at runtime from one packet. Due to its momentous trend with respect to RSS change (i.e. an indicator for link sensitivity), and its diversity across subcarriers, it holds potential to adjust link sensitivity at runtime by weighting the power of each subcarrier according to the measured multipath factor.

2) Subcarrier Weighting: As discussed above, subcarriers with larger absolute value of multipath factor seem more sensitive to human presence. Hence it is reasonable to penalize the subcarriers with smaller multipath factor by reducing their weights. On receiving a group of CSIs $\{H(f_{k})\}$ from one packet and calculating the subcarrier RSS difference $\{\Delta s(f_{k}) = |H(f_{k})|^{2} - s^{(0)}(f_{k})\}$ , where $s^{(0)}$ denotes the subcarrier RSS on subcarrier $f_{k}$ measured with no persons around, we weight the RSS differences as follows:

$$
\Delta \tilde {s} (f _ {k}) = | \frac {\mu_ {k}}{\sum_ {k} \mu_ {k}} | \cdot \Delta s (f _ {k}) \tag {12}
$$

Although multipath factor is measured on a per-packet basis, device-free human detection schemes often require multiple packets to average out noise and environmental unstableness for more reliable decisions. To assess the potential temporal fluctuation of multipath factors extracted from multiple packets, we collect CSIs along a 3-meter link with a person standing at 2 fixed locations, each with 5000 packets. Fig. 4 plots the distributions of subcarrier RSS changes and the multipath factors. As shown in Fig. 4a, the subcarrier with the maximal multipath factor can vary for packets measured at the same location (from subcarrier $f_{11}$ to $f_{15}$ ). Fig. 4b and Fig. 4c plot the distributions of multipath factor and the corresponding RSS changes for 2 different human presence locations. While the subcarriers with large multipath factors are more temporally stable with certain human presence locations (e.g. subcarrier $f_1$ Fig. 4b), they may exhibit dramatic temporal fluctuation with other human presence locations (e.g. subcarrier $f_{16}$ and $f_{17}$ in Fig. 4c). Since highly unstable subcarriers may lead to unreliable detection results, we assign higher weights to subcarriers with constantly large multipath factor.

To simultaneously reflect link sensitivity and temporal stability, we rectify the subcarrier weights as follows. Assuming a sequence of M CSIs, we first calculate the multipath factors $\{\mu_{k}^{(m)}\}_{m=1}^{M}$ for each packet as Eq. 11. Then the temporal mean of multipath factor $\bar{\mu}_{k} = \frac{1}{M} \sum_{m=1}^{M} \mu_{k}^{(m)}$ accounts for the average detection sensitivity. To assign higher weight on consistently sensitive subcarriers, we calculate the percentage of times when the multipath factor is greater than the median of the multipath factors on all subcarriers $\hat{\mu}^{(m)}$ . Concretely, we maintain a ratio $r_{k}$ for subcarrier $f_{k}$ as:

$$
r _ {k} = \frac {\sum_ {m = 1} ^ {M} \delta_ {m}}{M} \tag {13}
$$

where

$$
\delta_ {m} = \left\{ \begin{array}{l l} 1 & \text { if } \mu_ {k} ^ {(m)} > \hat {\mu} ^ {(m)} \\ 0 & \text { otherwise } \end{array} \right. \tag {14}
$$

Finally, we combine the two weights and obtain the adjusted RSS change $\Delta \tilde{s}(f_k)$ for subcarrier $f_{k}$ as:

$$
\Delta \tilde {s} (f _ {k}) = | \frac {\bar {\mu} _ {k} r _ {k}}{\sum_ {k = 1} ^ {K} \bar {\mu} _ {k} \sum_ {k = 1} ^ {K} r _ {k}} | \cdot \Delta s (f _ {k}) \tag {15}
$$

# B. Extending Coverage via Spatial Diversity

The previous subsection enhances the detection sensitivity of a multipath link leveraging frequency diversity. As in Fig. 1, subcarrier weighting increases the impact of human presence at all the 3 locations (i.e. locations A to C). However, since the decision of human presence is typically drawn based on a unified threshold, the detection coverage is often constrained by the impact of human presence on NLOS paths. For instance, the RSS change with human presence at C (a reflected path) is usually orders-weaker than that with human presence at A (the LOS path). If the pre-defined threshold is larger than the RSS change incurred by human presence at C, the system would fail to detect the person. In fact, when considering the LOS path only, the “sensitivity region” is restricted to 5 to 6 wavelengths around the LOS path [19]. Thus the detection coverage can be expanded by re-assigning the weights of the LOS and the reflected paths.

To re-assign the weights of the LOS and the reflected paths, the first step is to distinguish the two, which is no easy task using WiFi. The LOS and reflected paths are twisted in the frequency domain and unresolvable in the time domain due to insufficient resolution on WiFi devices $[21]$ . Note that current WiFi devices are often equipped with multiple antennas. Thus we may distinguish the LOS and other paths from the spatial domain by identifying their arriving angles.

1) Measuring Angle-of-Arrival: Typical angle-of-arrival estimation algorithms analyze the phases received by multiple antennas [23]. As illustrated in Fig. 5a, signals transmitting through a reflected path arrive at the antennas with an incident angle $\theta$ . Compared with the uppermost antenna, signals arrive at the antenna in the middle with an extra propagation distance of $\Delta d = \frac{\lambda}{2}\sin \theta$ , where the antennas are spatially separated by semi-wavelength $\frac{\lambda}{2}$ . The additional propagation distance $\Delta d$ imposes a phase shift $\Delta \phi = \frac{2\pi}{\lambda}\Delta d = \pi \sin \theta$ . Therefore, by measuring the relative phase shifts between two antennas $\Delta \phi$ , the incident angle can be solved by:

$$
\theta = \arcsin \left(\frac {\Delta \phi}{\pi}\right) \tag {16}
$$

To simultaneously estimate multiple angles from multiple paths, we apply the MUltiple Signal Classification (MUSIC) algorithm $[23]$ . It operates on observations from multiple antennas and outputs an angular pseudospectrum, with each peak corresponding to the angle for one incoming signal. Fig. 5b plots the angular pseudospectrum with a 3-antenna array. The two peaks represent the direction of the LOS and a reflected path, respectively. While the smoothed MUSIC algorithm $[17]$ $[24]$ can achieve better performance for correlated signals (as is the case for multipath signals), it also relegates three antennas to only two, thus unable to detect more than one path. Hence we only adopt the original MUSIC algorithm to distinguish at least two paths with only three antennas. One drawback of the MUSIC algorithm is that the angular resolution is limited by the number of antennas. However, we may benefit from two potentials: (1) Devices are equipped with increasing numbers of antennas to support MIMO operations $[17]$ . (2) Mobile devices can emulate a large antenna array via Synthesis Aperture Radar (SAR) techniques $[25]$ .

2) Path Weighting: To evaluate the impact of human presence from different directions, we collect CSIs along a 3m link as in Fig. 5a. The link is placed in the proximity to a concrete wall to create notable reflected paths. The angular pseudospectrum with no human presence is shown in Fig. 5b. We test 16 human presence locations with incident angles from -90 degrees to 90 degrees one meter away from the receiver. The subcarrier RSS changes (averaged across the three antennas) for the 16 locations are plotted in Fig. 5c. As is shown, most subcarriers exhibit dramatic RSS changes along the direction of the LOS path. In addition, another notable RSS change occurs at approximately the same direction of the NLOS path estimated in Fig. 5b. Also, the average RSS change is proportional to the amplitude of the pseudospectrum

![](images/babeef0c4ad4ddce1cca4f204daf2b57c4b419816511dac7803b457a4b304502.jpg)



Fig. 6. Illustration of testing scenarios. The measurements were conducted in two rooms in an academic building, including 5 links (cases). For each link (case), we tested human presence locations covering a 3x3 grid.

peaks.

Intuitively, path weights inversely proportional to the angular pseudospectrum can be adopted for uniform detection coverage. However, a linear antenna array can only distinguish angles within 180 degree, and the angular estimation for large angles is often error-prone [17]. Hence we choose the path weights to only enhance the impact of reflected paths within a certain angular range for higher reliability. Given the pseudospectrum measured with no human presence $P_{s}(\theta)$ , the weighting function $w(\theta)$ is calculated as:

$$
w (\theta) = \left\{ \begin{array}{l l} \frac {1}{P _ {s} (\theta)} & \text { if } \theta_ {\min} <   \theta <   \theta_ {\max} \\ 0 & \text { otherwise } \end{array} \right. \tag {17}
$$

where $\theta_{min}$ and $\theta_{max}$ are empirically determined. The weights are then assigned to the angular pseudospectrum to improve the impact of reflected paths.

# C. Human Detection with Subcarrier and Path Weighting

As discussed in Section III, a typical device-free human detection scheme works in two stages: calibration and monitoring. During the calibration stage, the receiver starts by collecting CSI samples, and the raw CSI data are calibrated as in [26] to mitigate the impact of random phase noise. After collecting N CSI samples, the receiver calculates the angular pseudospectrum for the static environments using the MUSIC algorithm, and derives the path weights as in Eq. 17, where $\theta_{min} = -60^{\circ}$ and $\theta_{max} = 60^{\circ}$ in our implementation. The mean of the CSI samples $s(0)$ is also stored as the profile when there is no human presence.

During the monitoring stage, the receiver collects M packets and calculate the subcarrier weights as in Eq. 15. The subcarrier weighted signal strengths from multiple antennas (three in our case) are then processed to output the angular pseudospectrum, which is further weighted by the pre-calculated path weights obtained from the calibration stage. Due to the linear properties of the transforms involved in our scheme, we can assign the subcarrier weights separately on the subcarrier signal strengths in the monitoring stage and those during the calibration stage before subtracting them to calculate, e.g., Euclidean distance. To infer human presence, the static profile $s(0)$ is first subcarrier weighted and then transformed into angular pseudospectrum. Afterwards various distance metrics can be employed to quantify their similarity and compare the calculated similarity with a predefined threshold to decide human presence. Here we use the Euclidean distance for its simplicity. The threshold is determined by the variations of the static profile with respect to certain false positive and false negative requirements.

![](images/acd57f093bfc89d46f3fec99a37e53cba9a3b167395bce632230bcfa87903f3a.jpg)



Fig. 7. Overall detection performance.

![](images/ee745144d79995562a0b1d055422522cc9db482ad0d21037b0f47c1cb6633de1.jpg)



Fig. 8. Performance in different cases.

![](images/07b66a549dca3ed3bbd538cffd9a8d1826f62d5c2dd4e2f19c4288db169f3af0.jpg)



Fig. 9. Performance within different range.

# V. EVALUATION

In this section, we first interpret the experiment setup and methodology, followed by detailed performance evaluation.

# A. Methodology

Testing Scenarios: We conduct the measurement campaign in two rooms in an academic building. The rooms are furnished with desks, computers, and other furniture. As shown in Fig. 6, we collect date from 5 TX-RX links (Case 1 to 5) with diverse TX-RX distances and AP heights in total. For each link (case), we test human presence locations within a 3x3 grid to cover different distances and angles with respect to the receiver. For each human presence location, we ping packets from the transmitter for 3 times, with 5000 packets per time. We also collect the same amount of packets with no human presence within the area of interests as static profiles. To account for background dynamics, we allow up to 5 students work at their desks and occasionally walk around in the testing rooms, but remain about 5 meters away from the testing link during the measurement campaign. We also take temporal dynamics into account by (1) pausing for 5 minutes before measuring the next 5000 packets and (2) repeating the above measurements both in the daytime and at night, and after two weeks.

Infrastructure Setup: We employ a Tenda wireless router with one omnidirectional antenna as the transmitter operating in IEEE 802.11n AP mode at 2.4GHz Channel 11. A mini desktop equipped with Intel 5300 NIC and three external omnidirectional antennas running Ubuntu 10.04 works as the receiver, pinging packets at a rate of 50 packets per second. The received packets are processed by the CSI tool [16] and we implemented the human detection scheme with MATLAB running on the mini desktop.

Evaluation Metrics: We mainly focus on the following metrics. (1) True Positive (TP): The fraction of cases where the receiver correctly detects human presence. (2) False Positive (FP): The fraction of cases where the receiver announces a “detected” event when there is no one around.

We compare the performance of the following schemes. (1) Baseline: Calculate the Euclidean distance of CSI amplitudes. (2) Subcarrier weighting: Calculate the Euclidean distance of subcarrier weighted RSS changes as in Eq. 15. (3) Combining subcarrier and path weighting: Calculate the Euclidean distance of weighted pseudospectra as in Section IV-C. Since the former two schemes require only one antenna, their performances are averaged across the three antennas for fair comparison.

# B. Performance

1) Overall Detection Performance: Fig. 7 plots the Receiver Operating Characteristic (ROC) curves of the three schemes. The ROC curve depicts the tradeoff between the true detection rate and the false positive rate over a wide range of thresholds. The closer the ROC curve is to the upper left corner, the better the detection performance. The results in Fig. 7 show that the baseline obtains balanced detection accuracy of about 70% with a false positive rate of 30%. With subcarrier weighting, the balanced detection accuracy boosts to 88.2% with a false positive of 13.0%. Combined with path weighting, the balanced detection accuracy further rises to 92.0% with a false positive of 4.5%. This indicates subcarrier weighting dramatically improves link sensitivity, while path weighting offers moderate gain by enhancing the impact of human presence on NLOS paths. We note, however, a plateau on the ROC curves adopting the weighting schemes. A partial reason might be that although the weighting schemes improve the sensitivity of human presence, certain environmental dynamics (e.g. occasional walks of students during the measurements) might also be magnified. To mitigate the impact of such magnified background dynamics, one solution is to model the static profiles as well, e.g. via hidden Markov models [27]. From the ROC curves, we derive a general threshold for balanced detection accuracy, and use it in the subsequent evaluations.

Fig. 8 plots the detection rates for the 5 testing cases separately using the threshold for balanced overall detection performance in Fig. 7. We see no clear performance gap among these cases. Yet all the 3 schemes in Case 3 slightly outperform the others. This is because the measurements in Case 3 were conducted in a relatively vacant area with a strong

![](images/23aa3e1bae2a5e6a491e00885db3e404fd1d57b98f51ecf70d3d3f6d9d82fa09.jpg)



Fig. 10. Angle estimation errors.

![](images/6e1a1ec3df26e817317b4bfacfe67347be087c46e50b5e7a356dad00d11d7c58.jpg)



Fig. 11. Performance of path weighting.

![](images/a2584bb501b30ec93af2fdeb77d8f2e1ea042953419244fd2d4a2ef7be07f62d.jpg)



Fig. 12. Impact of packet numbers.

LOS path (since it is a 3m link). Lacking of NLOS propagation, however, path weighting brings marginal performance gain for Case 3. Also note that the detection accuracy exhibits a modest drop with path weighting in Case 1. This might be caused by angle estimation errors, as will be discussed shortly.

2) Detection Range: Detection range is critical for device-free human detection systems. We tested human presence locations with distances from approximately 1m to 5m to the receiver and plotted the detection rates in Fig. 9. As is shown, the baseline suffers sharp detection performance degradation for human presence faraway, with a detection rate of lower than 60% for human presence 5m away from the receiver. In contrast, with both subcarrier weighting and path weighting, the detection rate retains above 90% even for human presence 5m away. Path weighting also demonstrates the highest performance gain of 12% for distant humans. Therefore our scheme can potentially increase the detection range of a single TX-RX link by more than 1x given a minimal detection rate of 90%.

3) Impact of Angle Estimation Errors: As shown in Fig. 8 and Fig. 9, while path weighting generally contributes to higher detection rate, it can cause slight performance drop sometimes, e.g. case 1 in Fig. 8. The reason might lie in the angle estimation errors. With only three antennas, the median estimation errors can be more than 20 degrees [11]. Fig. 10 plots the CDF of the angle errors. By averaging over multiple packets, the estimation errors decrease moderately. This is because the person during the measurements was not completely static. Thus averaging the measurements with slight user movements helps to improve the precision of angle estimation. However, the resolution of angle estimation is primarily determined by the antenna aperture, which can only improve via a larger antenna array or SAR techniques. Hence we still see large tail errors even by averaging, which may lead to unstable performance gain via path weighting.

Fig. 11 portrays the detection performance of human presence locations at different angles with the same radius from the receiver. Despite notable improvement at relatively large angles, the performance gain is marginal near the LOS path (around the angles of zero degree). Nevertheless, with the increasing number of antennas on commercial devices [17], we envision more accurate angle estimation via larger antenna arrays or advanced SAR technique [25] would contribute to more robust path weighting for wider coverage.

4) Impact of Packet Quantity: Fast response time is important if the device-free detection systems are for surveillance or security purposes. We plot the impact of packet quantity on the detection rates in Fig. 12. Since the weighting schemes are low in computation complexity, the dominating constraint lies in the number of packets required for reliable detection. As is shown, at a pinging rate of 50 packets per second, the detection rates retain almost stable and tend to saturate with only 0.5 seconds of measurements. Thus the proposed detection scheme can accomplish accurate human detection with less than one second delay.

# VI. RELATED WORK

Our work is related to the following categories of research.

CSI based Device-free Applications: Device-free systems detect, localize and track a user via his impact on the received wireless signals $[1]$ . Conventional schemes employ MAC layer RSSI as signal features to infer human presence. However, RSSI proves to be a fickle feature since it can fluctuate dramatically even at a stationary link $[21]$ . A promising alternative is to exploit the fine-grained PHY layer CSI available on commercial WiFi devices $[8]$ . Previous CSI based device-free systems mostly focus on specific applications such as gesture recognition $[7]$ and breath detection $[9]$ . Instead, this work studies the concerns on detection sensitivity and coverage, and aims to provide guidelines for optimal deployment and parameter configurations in multipath-dense indoor scenarios.

Spatial Human Models: To improve the reliability of RSSI based device-free applications, numerous efforts have explored to model the relationship between signal strength change and human presence location. In [13], the authors empirically demonstrated the link-centric detection coverage, which is then theoretically verified under the assumption of uniformly distributed scatter and reflection [14]. Both human-induced shadowing [19] and reflection [20] have been modeled exploiting ray-bouncing propagation models. Our analysis builds upon this thread of research, yet takes one step further by extracting configurable parameters to adjust link sensitivity and coverage leveraging diversity techniques.

Multipath Link Adaptation: Despite extensive research on human impact modeling, few metrics are tunable on commodity wireless infrastructure. Wilson et al. [12] proposed fade level as an indicator for different link behaviors. It is defined as the difference between the RSSI measured by a link and that calculated via propagation formulas. Primarily designed for ZigBee radios, fade level can be adjusted by sequentially sweeping channels [28]. Our multipath factor also depicts the status of multipath superposition, yet differs in two aspects. (1) The multipath factor is independent of propagation formulas which might lose effect in practice. (2) We can obtain the multipath factors simultaneously for all subcarriers from one packet at runtime, thus incurring negligible network throughput degradation. Some CSI-based work also explored tuning detection coverage. Zhou et al. [15] took a fingerprinting approach for omnidirectional coverage. Xi et al. [29] utilized a time-domain metric to control the width of the detection range. In contrast, we extend the detection coverage via frequency diversity (by subcarrier weighting) and spatial diversity (by path weighting), and require no labor-intensive site-survey.

# VII. CONCLUSION

In this study, we demonstrate that PHY layer channel information opens new opportunities for device-free human detection. Instead of avoiding multipath, we harness multipath for higher detection rates and wider coverage. We conduct an in-depth analysis on the impact of human presence on wireless signals under different propagation mechanisms, and propose a measurable metric on commodity WiFi devices as proxy for detection sensitivity. We propose a lightweight subcarrier and path configuration scheme harnessing both frequency and spatial diversities. We prototype our scheme with standard WiFi devices, and validate its performance in typical indoor environments. Experimental results demonstrate a detection rate of 92.0% with a false positive of 4.5%, and almost a 1x gain in detection range given a minimal detection rate of 90%. We envision this work as an early step towards robust and tunable device-free human detection in practical indoor settings, and would benefit a range of higher-level device-free human sensing tasks in complex propagation environments.

# ACKNOWLEDGMENT

This research was supported in part by Hong Kong RGC Grant HKUST16207714.

# REFERENCES

[1] M. Youssef, M. Mah, and A. Agrawala, “Challenges: Device-free Passive Localization for Wireless Environments,” in Proc. of ACM MobiCom, 2007.   
[2] D. Zhang, J. Ma, Q. Chen, and L. M. Ni, “An RF-Based System for Tracking Transceiver-Free Objects,” in Proc. of IEEE PerCom, 2007.   
[3] J. Wilson and N. Patwari, “Radio Tomographic Imaging with Wireless Networks,” IEEE Transactions on Mobile Computing, vol. 9, no. 5, pp. 621–632, 2010.   
[4] C. Xu, B. Firner, Y. Zhang, R. Howard, J. Li, and X. Lin, “Improving RF-based Device-free Passive Localization in Cluttered Indoor Environments through Probabilistic Classification Methods,” in Proc. of ACM IPSN, 2012.

[5] F. Adib, Z. Kabelac, D. Katabi, and R. Miller, “3D Tracking via Body Radio Reflections,” in Proc. of USENIX NSDI, 2014.   
[6] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-Home Gesture Recognition Using Wireless Signals,” in Proc. of ACM MobiCom, 2013.   
[7] P. Melgarejo, X. Zhang, P. Ramanathan, and D. Chu, “Leveraging Directional Antenna Capabilities for Fine-Grained Gesture Recognition,” in Proc. of ACM UbiComp, 2014.   
[8] Y. Wang, J. Liu, Y. Chen, M. Gruteser, J. Yang, and H. Liu, “E-eyes: In-home Device-free Activity Identification Using Fine-grained WiFi Signatures,” in Proc. of ACM MobiCom, 2014.   
[9] X. Liu, J. Cao, S. Tang, and J. Wen, “Wi-Sleep: Contactless Sleep Monitoring via WiFi Signals,” in Proc. of IEEE RTSS, 2014.   
[10] R. Ravichandran, E. Saba11, K.-Y. Chen, M. Goel, S. Gupta, and S. N. Patel, “WiBreathe: Estimating Respiration Rate Using Wireless Signals in Natural Settings in the Home,” in Proc. of IEEE PerCom, 2015.   
[11] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Back to the Basics: Avoiding Multipath to Revive Inbuilding WiFi Localization,” in Proc. of ACM MobiSys, 2013.   
[12] J. Wilson and N. Patwari, “A Fade-Level Skew-Laplace Signal Strength Model for Device-Free Localization with Wireless Networks,” IEEE Transactions on Mobile Computing, vol. 11, no. 6, pp. 947–958, 2012.   
[13] D. Zhang, Y. Liu, and L. M. Ni, “Link-Centric Probabilistic Coverage Model for Transceiver-Free Object Detection in Wireless Networks,” in Proc. of IEEE ICDCS, 2010.   
[14] N. Patwari and J. Wilson, “Spatial Models for Human Motion-Induced Signal Strength Variance on Static Links,” IEEE Transactions on Information Forensics and Security, vol. 6, no. 3-1, pp. 791–802, 2011.   
[15] Z. Zhou, Z. Yang, C. Wu, L. Shangguan, and Y. Liu, “Towards Omnidirectional Passive Human Detection,” in Proc. of IEEE INFOCOM, 2013.   
[16] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 Packet Delivery from Wireless Channel Measurements,” in Proc. of ACM SIGCOMM, 2010.   
[17] J. Xiong and K. Jamieson, “ArrayTrack: A Fine-Grained Indoor Location System,” in Proc. of USENIX NSDI, 2013.   
[18] Y. Zhao, N. Patwari, J. M. Phillips, and S. Venkatasubramanian, “Radio Tomographic Imaging and Tracking of Stationary and Moving People via Kernel Distance,” in Proc. of ACM IPSN, 2013.   
[19] S. Savazzi, M. Nicoli, F. Carminati, and M. Riva, “A Bayesian Approach to Device-Free Localization: Modeling and Experimental Assessment,” IEEE Journal of Selected Topics in Signal Processing, vol. 8, no. 1, pp. 16–29, 2014.   
[20] O. Kaltiokallio, H. Yiğitler, and R. Jäntti, “A Three-State Received Signal Strength Model for Device-free Localization,” arXiv preprint, 2014.   
[21] K. Wu, J. Xiao, Y. Yi, M. Gao, and L. M. Ni, “FILA: Fine-Grained Indoor Localization,” in Proc. of IEEE INFOCOM, 2012.   
[22] T. Rappaport, Wireless Communications: Principles and Practice (2nd). Prentice Hall PTR, 2002.   
[23] R. Schmidt, “Multiple Emitter Location and Signal Parameter Estimation,” IEEE Transactions on Antennas and Propagation, vol. 34, no. 3, pp. 276–280, 1986.   
[24] F. Adib and D. Katabi, “See Through Walls with Wi-Fi!” in Proc. of ACM SIGCOMM, 2013.   
[25] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate Indoor Localization with Zero Start-up Cost,” in Proc. of ACM MobiCom, 2014.   
[26] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You Are Facing the Mona Lisa: Spot Localization Using PHY Layer Information,” in Proc. of ACM MobiSys, 2012.   
[27] J. Zhang, M. H. Firooz, N. Patwari, and S. K. Kasera, “Advancing Wireless Link Signatures for Location Distinction,” in Proc. of ACM MobiCom, 2008.   
[28] O. Kaltiokallio, M. Bocca, and N. Patwari, “Enhancing the Accuracy of Radio Tomographic Imaging using Channel Diversity,” in Proc. of IEEE MASS, 2012.   
[29] W. Xi, J. Zhao, X.-Y. Li, K. Zhao, S. Tang, X. Liu, and Z. Jiang, "Electronic Frog Eye: Counting Crowd Using WiFi," in Proc. of IEEE INFOCOM, 2014.