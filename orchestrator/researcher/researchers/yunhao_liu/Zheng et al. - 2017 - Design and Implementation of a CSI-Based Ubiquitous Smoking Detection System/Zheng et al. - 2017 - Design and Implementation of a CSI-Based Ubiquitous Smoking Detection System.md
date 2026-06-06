# Design and Implementation of a CSI-Based Ubiquitous Smoking Detection System

Xiaolong Zheng, Member, IEEE, ACM, Jiliang Wang, Member, IEEE, Longfei Shangguan, Member, IEEE, ACM, Zimu Zhou, Member, IEEE, ACM, and Yunhao Liu, Fellow, IEEE, ACM

Abstract— Even though indoor smoking ban is being put into practice in civilized countries, existing vision or sensor-based smoking detection methods cannot provide ubiquitous detection service. In this paper, we take the first attempt to build a ubiquitous passive smoking detection system, Smokey, which leverages the patterns smoking leaves on WiFi signal to identify the smoking activity even in the non-line-of-sight and throughwall environments. We study the behaviors of smokers and leverage the common features to recognize the series of motions during smoking, avoiding the target-dependent training set to achieve the high accuracy. We design a foreground detectionbased motion acquisition method to extract the meaningful information from multiple noisy subcarriers even influenced by posture changes. Without the requirement of target’s compliance, we leverage the rhythmical patterns of smoking to detect the smoking activities. We also leverage the diversity of multiple antennas to enhance the robustness of Smokey. Due to the convenience of integrating new antennas, Smokey is scalable in practice for ubiquitous smoking detection. We prototype Smokey with the commodity WiFi infrastructure and evaluate its performance in real environments. Experimental results show Smokey is accurate and robust in various scenarios.

Index Terms— Smoking detection, non-intrusive, channel state information, ubiquitous.

# I. INTRODUCTION

T IS well recognized that smoking is not only a significant I reason of death and disease worldwide, but also a leading cause of fire hazards. According to the report of the U.S. Fire Administration, there are about 7,600 smoking-related fires in homes each year, accounting for 17 percent of fire deaths in residential area [1]. More seriously, the death rate per 1,000 fires in smoking related indoor fires is seven times higher than that in nonsmoking related fires. Given the harms of smoking, public policies such as prohibiting smoking in public spaces, are put into practice in many countries. To ensure

Manuscript received November 18, 2016; revised June 12, 2017; accepted September 9, 2017; approved by IEEE/ACM TRANSACTIONS ON NETWORK-ING Editor X. Zhou. Date of publication October 3, 2017; date of current version December 15, 2017. This work was supported in part by the NSFC under Grant 61672320, Grant 61672240, Grant 61572277, Grant 61532012, and Grant 61529202, and in part by the NSFC/RGC Joint Research Scheme under Grant 61361166009. (Corresponding authors: Xiaolong Zheng; Yunhao Liu.) X. Zheng, J. Wang, and Y. Liu are with the School of Software and TNLIST, Tsinghua University, Beijing 100084, China (e-mail: xiaolong@ greenorbs.com; jiliang@greenorbs.com; yunhao@greenorbs.com).

L. Shangguan is with the Computer Science Department, Princeton University, Princeton, NJ 08544 USA (e-mail: longfeis@cs.princeton.edu).

Z. Zhou is with the Information Technology and Electrical Engineering Department, ETH Zürich, 8092 Zürich, Switzerland (e-mail: zzhou@tik.ee.ethz.ch).

Digital Object Identifier 10.1109/TNET.2017.2752367

the polices really beneficial, an efficient ubiquitous monitoring system, which is able to automatically and accurately detect the smoking activities is imperative.

Unfortunately, to the best of our knowledge, a ubiquitous smoking monitoring system is still absent. Sensor-based detection [2], [3] is one of the most widely adopted passive detection methods. However, smog sensors are not sensitive enough to detect the tobacco smog when the room is large or the ceiling is high. For rooms without smog sensor based detection system, it is also costly to install such a detection system and it may even need to partially re-decorate the rooms after installation. Even the cost can be reduced, each smog sensor has limited sensing range, leading to detection blind point and detection delay [2], [3]. Vision-based detection is another type of passive detection method. Applying computer vision (CV) technique to surveillance video can analyze human gestures for smoking detection [4]. Nevertheless, vision-based methods are restricted to Line-of-Sight (LOS) environments, hindering its applicability in a ubiquitous monitoring system. When smoking actions are blocked by obstacles, CV technique loses efficacy. Besides, due to the cost and privacy concerns, many blind spots exist in the areas without camera such as the stairwell and toilets.

We think of the question: can we build a practical smoking detection system that (1) automatically and accurately detects the smoking activities without deploying special devices, (2) is non-intrusive for detection targets, and (3) works efficiently in a wide range of environment conditions including both LOS and Non-Line-of-Sight (NLOS) conditions? In this paper, we leverage the commercial off-the-shelf (COTS) WiFi infrastructures to detect smoking activity. The WiFi infrastructure is widely available in indoor environments and low-cost to use. Leveraging the wireless signals does not require any device on the targets. We analyze the impact of smoking gestures on WiFi signal propagations and conduct preliminary experiments to validate the feasibility of detecting the smoking activity by its impacts on WiFi signals.

It has been shown that wireless signal provides an information carrier for gesture recognition through the channel characteristics such as Received Signal Strength (RSS) and Channel State Information (CSI) [5]–[9]. However, existing gesture recognition approaches based on wireless signals cannot be directly used in our scenario. Existing approaches assume relative simple or special gestures or a well-defined gesture training set. Meanwhile, existing approaches adopt various methods to improve input data quality. For example, existing approaches may need to specify the start and end of gesture recognition period in which users are required to perform gestures, so as to increase the detection accuracy. However, those requirements may not hold for smoking detection scenario.

To address above challenges, we take the first attempt to build a novel non-intrusive smoking detection system, namely Smokey, that is able to accurately detect the smoking activities by exploiting the impact of smoking on the CSI of WiFi. The design of Smokey is inspired by the following findings. First, instead of recognize a special gesture with carefully trained classifier, we exploit the periodical pattern for event detection. We find that smoking is a rhythmic activity that periodically affects the CSI of WiFi signals. This significantly reduces the impact of individual difference and the detection error comparing with gesture recognition approaches. Second, smoking is a composite activity that contains a series of motions of the arms and chest in the exact order, which is helpful to be distinguished from the daily activities. To avoid the dependency of a good training set, Smokey elaborately uses the temporal features such as the order of motions in smoking and the transition duration between motions.

The implementation of Smokey also faces several challenges. First, since smoking consists of a sequence of motions, its impact on CSI is dynamically scattered across different subcarriers. What’s worse, even in a single subcarrier, the noise is also very high due to the passive detection method for uncooperative users in dynamic environments. We design a motion acquisition method, based on the foreground detection in image processing community, to extract useful information from the noisy CSI traces. We also leverage the spatial diversity of multiple antennas on the receiver to improve the robustness of Smokey. We design the antenna selection and result fusion components to use the multiple antennas appropriately for performance improvement. We also propose event-driven sampling mechanism to avoid congesting the wireless channel and save energy.

We implement Smokey on the commercial WiFi devices and evaluate its performance in real environments. The results show that Smokey can detect the smoking activities with a high TPR of 0.976 (0.919), along with a low FPR of 0.008 (0.097) using a single pair of transceivers in the relatively static (dynamic) environments. We also extensively evaluate the robustness of Smokey under various scenarios.

The contributions are summarized as follows.

• We investigate the characteristics of wireless signal impacted by smoking and validate the feasibility of using wireless signal for smoking detection.   
We take the first attempt to build a non-intrusive ubiquitous smoking detection method, Smokey. We avoid relying on good training data, which is commonly used by existing gesture recognition methods, to detect the unknown smoking persons.   
• To strength the robustness of Smokey in practice, we extend our design by using multiple antennas and propose antenna selection and result fusion to improve the accuracy. We also propose the event-driven sampling

to avoid wireless channel congestions and unnecessary energy consumption.

• We implement Smokey with commercial hardware and evaluate its performance. The experimental results demonstrate the effectiveness of Smokey.

In the rest of this paper, we will present the preliminary findings in Section II. Then we elaborate the design details of Smokey in Section III and evaluate its performance in Section IV. We present the related work in Section V and finally conclude our work in Section VI.

# II. PRELIMINARY FINDINGS

It has been shown that the environment changes such as the presence and motions of human can affect the communications between two wireless devices. The impacts can be captured and utilized for device-free human detection and localization [5]. For example, the variations of Received Signal Strength Indicator (RSSI) caused by motions can be used to track the location of the object even behind the wall [10]. By learning the characteristics of RSSI variations, body motions such as gestures can be recognized in [8].

Existing gesture recognition methods rely on repeatable impacts of motions on wireless signal. They are usually able to work well in the cases of simple or well-defined gestures near the transceivers. It is unclear how unrestricted activities such as smoking performed away from the transceivers affects the WiFi signal and whether it is possible to recognize smoking by its impacts on WiFi signal. In this section, we conduct the preliminary experiments to investigate the feasibility of recognizing smoking activities using WiFi signal.

# A. Smoking Steps

We first introduce the smoking steps of a typical smoker. Normally, smoking a cigarette can be divided into holding phase and smoking phase. After lighting up a cigarette, a smoker usually holds the cigarette in hand and puts up the cigarette to mouth to suck the smoke intermittently. We can further decompose the smoking into six detailed steps [11], as Fig. 1 shown.

(a) Holding the cigarette. Most of the time, a smoker holds the cigarette in hand.   
(b) Putting up the cigarette to mouth. A smoker puts up the cigarette to the mouth for the subsequent inhalation.   
(c) Sucking the smoke in mouth. Note that a smoker usually does not inhale the smoke into lung directly. Instead, the smoker suck the smoke into the mouth.   
(d) Putting down the cigarette. After sucking enough smoke, the smoker will put down the cigarette.   
(e) Inhaling the smoke. And then, the smoker inhales the smoke into the lung.   
• (f) Exhaling the smoke. At last, the smoker exhales the smoke and returns to the holding phase.

Smoking is a rhythmic activity. Step (a), i.e., holding phase, occupies most of the time of smoking. Step (b)-(f) compose the smoking phase which occurs intermittently. We call one round from Step (b) to Step (f) as one smoking motion. Several smoking motions together with the holding phases constitute a smoking activity. The durations of the holding and smoking motions are relatively stable because the smoker’s smoking behavior usually remain unchanged.

![](images/16d1336354b62dbb23540a563b2452458ddabb6d5829e9b02ef67399de6047b2.jpg)  
(a)

![](images/c8aa36450f3ae6e7805b5cc979ba0c76727dec36bc28b44b4521ddf9ca269798.jpg)  
(b)

![](images/2313db798521d4e6a0010e53adda1d92ceab7667c4b8ac7f4d898c15900f2544.jpg)  
(c)

![](images/753ae4a746152b5250b06326274f44d3a0edb3f4fb797801130bd99ea8f76df0.jpg)

![](images/34abe7024765cd56cbc99bb4aff0eaf216559956612b6b736eaa4649d5d43744.jpg)  
(e)

![](images/39484e54960bd81e2e69be60fe695762290bcb0020506f804486e4371c4e3b32.jpg)  
(f)   
Fig. 1. Typical smoking steps: (a) holding the cigarette, (b) putting up the cigarette to mouth, (c) sucking the smoke in mouth, (d) putting down the cigarette, (e) inhaling the smoke, (f) exhaling the smoke.

# B. How Smoking Affects Wireless Signal

Step (b) and (d) are performed with arm motions. In Step (e) and (f), the inhalation and exhalation are performed with chest motions. In this section, we investigate how these motions affect WiFi signal.

Existing commercial WiFi devices provide two channel indicators: Received Signal Strength Indicator (RSSI) and Channel State Information (CSI). RSSI is a common indicator that represents the strength of received signal. When human motions block or unblock the signal transmission path, received signal strength may vary due to severe or weak attenuation. CSI is a fine-grained indicator that measures the channel for Orthogonal Frequency Division Modulation (OFDM). With OFDM, WiFi (IEEE 802.11a/g/n) sender transmits bits through multiple orthogonal subcarriers in parallel. With existing WiFi Network Interface Cards (NICs) such as Intel 5300, a WiFi receiver can obtain a group of 30 subcarrier channel measurements in the form of CSI [12]:

$$
H _ {k} = \left\| H _ {k} \right\| e ^ {j \sin (\angle H _ {k})} \tag {1}
$$

where $H _ { k }$ is the CSI at subcarrier $k , \parallel H _ { k } \parallel$ is the amplitude and $\angle H _ { k }$ denotes the phase. Each measured CSI sample on a subcarrier is a complex number. The real part and imaginary part specify the gain and phase of the signal path between transmitter and receiver. We use the amplitude information to observe the influences of human motions.

We deploy a TP-Link WR742N router and a mini PC with Intel 5300 NIC equipped with one antenna as the generators of WiFi signal. The PC is five meters from the router. We collect the measurements of RSSI and CSI from the received packets. We ask a person to smoke a cigarette between the transmitter and receiver, one meter away from the receiver.

1) Smoking Affects CSI Instead of RSSI: In Fig. 2, we plot the RSSI and CSI sequences obtained during smoking. Smoking motions are recorded in video in this smoking activity. The results clearly show RSSI varies over the time. However, the variation happens in both holding and smoking phases. There is no clear correlation between RSSI variation and the smoking motions. Then we investigate whether CSI is affected by the smoking activity. We find that CSI not only varies during smoking but also shows a very close correlation with smoking motions. This is because CSI is more informative than RSSI [13], [14] and hence more sensitive to smoking motions. The results demonstrate that CSI is more sensitive

![](images/630f13e58fac88267aec4b14aa70fb4a1893ba8fac457a4dac5c8802f2163994.jpg)



Fig. 2. The RSSI and CSI sequences collected during smoking. Ground truth is obtained by the video record.

![](images/2e2e0b28a4b68400b1e162980093216d651db222ce7af587ba364253c750c6aa.jpg)



Fig. 3. The CSI sequences of subcarrier #5, #14, and #23. Light gray areas are the periods of smoking phase from (b) to (d) with arm motions. Dark gray areas are the periods of smoking phase (e) and (f) with chest motions.

to smoking motions, shedding light on detecting smoking activities by CSI information.

Smoking affects CSI instead of RSSI because CSI is more sensitive to human activities. RSSI is only affected when the signal propagation path is significantly altered. The arm and chest movements are hard to change the signal propagation path to the extent of affecting RSSI significantly, especially when the human is in the NLOS transmission path. On the other hand, CSI is a more detailed description of channel state which is able to capture the multipath changes of the signal propagation path [15]. During smoking, the arm and chest motions will changes transmission path. Then the changed mutlipath can be captured by the CSI amplitude.

2) The Impacts of Smoking Are Subcarrier-Dependent: In Fig. 3, we plot the CSI sequences of subcarrier #5, #14, and #23 during smoking. We can find that subcarrier #23 is affected from phase (b) to (d) but not during phase (e) and (f). On the contrary, subcarrier #14 is affected only during phase (e) and (f). For other subcarriers, similar observations also exist. The reason behind these observations is that subcarriers have different sensitivities for the motions of different parts of human body. During smoking motions, a portion of subcarriers may be sensitive to the motions of arms while another portion may be sensitive to the motions of chest. Therefore, different subcarriers are affected in different smoking phases.   
3) The Impacts of Smoking on CSI Vary Dynamically on a Single Subcarrier: We find that the impacts of smoking on CSI vary dynamically across different subcarriers and the

![](images/e6569806862b59d28f972127375517440a16f4226fce8064646282f42d7ae7e7.jpg)



(a)

![](images/db86e8afb130b905c51a0c34561e331c3c12af3f00156829b974397c68fa03cf.jpg)



(b)

![](images/f6355ab937db3dcd0219509e9901bd305d1c8b60de99ccc516d15c6429079cc8.jpg)



![](images/c8493a69ff6a0272ffd49be1aa325883ae121a86ec619c4138d10003fd02b0cc.jpg)



(d)

Fig. 4. The CSI sequences collected during smoking and three other daily activities that may be confused with smoking. (a) Smoking. (b) Eating. (c) Drinking. (d) Deep Breathing.   
![](images/3496fc7a14a3e3936ef01ea5e3e55d665f0aa9d03aa1032790cfacd6d0c92355.jpg)



![](images/ec6c3ce2ec58bc937fcb46c853233a7dc4022fce118e790ca12be5036e62c602.jpg)



Fig. 5. The CSI sequences on subcarrier #27 when the target is (top) deep breathing and (bottom) smoking.

impacts are not stable even in a single subcarrier. Subcarrier #5 is affected from phase (b) to (f) in the first smoking motion ([11.7s, 22.8s]). However, in the second smoking motion ([60.2s, 68.0s]), subcarrier #5 is only affected from phase (b) to (d) but not in phase (e) and (f). This is because the smoker usually does not exactly repeat the same smoking motion. When the environment changes such as smoker posture changes, the sensitivities of subcarriers change, leading to the dynamic impacts on subcarriers even for the same motion.

4) Smoking Is a Composite Activity That Contains a Series of Motions in a Certain Order: Smoking is a composite activity consisting of a series of arm and chest motions in a certain order. We investigate three daily activities: eating, drinking, and deep breathing, which are considered to be confused with smoking. We collect the CSI traces when a person is smoking, eating a hamburger, drinking a cup of coffee and breathing deeply at the same location. Fig. 4 presents how these activities affects CSI. We can find that the CSI sequences show separate peaks when performing confusing activities, while the peaks during smoking appear in pairs. This is because smoking activity consists of a series of arm and chest motions in a certain order while other daily activities do not. Daily motions does not usually happen in the exact order as smoking.

We also find that the order of chest motions during smoking is unique. We plot the CSI amplitudes of subcarrier #27 during deep breathing and smoking in Fig. 5. Normally, the inhalation duration and exhalation duration in one respiration cycle are nearly the same, as shown in the top figure of Fig. 5. However, we find that the exhalation duration is obviously longer than the inhalation duration in smoking, as shown in the bottom figure of Fig. 5 (b). Such a phenomenon is also observed in previous work [16]. Ali et al. [16] use a wearable chest whist to monitor the chest motions and obtain those duration features to recognize the smoking activities. Such information can also be captured by CSI to help detect smoking activities.

# C. Summary

According to the preliminary study, we find smoking is a rhythmic composite activity that contains a series of motions in a certain order. This makes smoking distinguishable for daily motions such as putting arms up or down. The rhythm/order of motions is important information of the common behaviors of most smokers. Using rhythm/order information to detect smoking does not require to “decode” the precise information on a single motion, making it more resilient to detection errors in a single motion. However, we also find that (1) the impact to CSI is dynamic across different subcarriers, and (2) the impact on CSI is also time-varying, making it difficult to extract useful information for detection. Hence, how to extract and leverage rhythm/order information for smoking detection, from timevarying and subcarrier-dependent CSI, needs delicate designs.

# III. SYSTEM DESIGN

In this section, we elaborate the designs of Smokey. Based on the preliminary findings, we propose to leverage the rhythmic pattern and the certain order of smoking motions to detect the smoking activities. Fig. 6 presents the overview of Smokey. To make Smokey practical, we design an eventdriven sampling mechanism that adaptively changes the CSI sampling rate according to the presence of potential targets. First of all, the sampled CSI traces are processed to eliminate outliers and interpolate the irregular data to align time to get time information. Then the motion acquisition component extracts the interested motions that are suspected to be smoking. The extracted suspicious motions are further analyzed by activity analysis component from the aspect of periodicity to decide whether a smoking activity exists. Last but not the least, we leverage the spatial diversity of multiple antennas to enhance the robustness of Smokey. We propose antenna selection and fusion methods to use multiple antennas appropriately to improve the performance.

# A. Event-Driven Sampling

Though a high CSI sampling rate provides detailed information about human motions, it consumes too much additional bandwidth and energy. Note that CSI information is extracted from the received WiFi packets. Hence, when the number of the off-the-shelf WiFi packets such as the beacons and packets generated by customer use is less than required, we have to inject dedicated WiFi packets to obtain enough CSI samples. But the injected packets will congest the wireless channel. Therefore, a high sampling rate is risky to bring about side effects on the WiFi communication. Besides, transmitting injected packets on embedded devices such as samrthphones will consume additional energy.

To save energy and alleviate wireless congestion, we propose an event-driven sampling mechanism that adaptively adjusts the CSI sampling rate. In our application scenario, the presence of human is the prerequisite of potential smoking violation. Therefore, we use the human presence as the event that triggers sampling rate adjustment. By the event-driven sampling, we can keep the system running under low sampling rate $s _ { L }$ when there is no person around and dynamically increase the sampling rate to $s _ { H }$ , to provide enough CSI samples for smoking detection.

It is well known that the presence of human will bring significant changes of CSI. Previous studies [5], [6] have already shown the presence of human will cause significant CSI changes. We borrow the idea from existing work and propose a deviation-based detection method. We monitor the average standard deviation of CSI on all subcarriers, $\sigma _ { p } .$ , during a time window $T _ { p } .$ . If $\sigma _ { p }$ is larger than a preset threshold $\sigma _ { p t } ,$ Smokey detects the presence of human and starts the high sampling rate. If no human is detected during in K windows, Smokey turns to a low sampling rate. In our current implementation, we set the low sampling rate $s _ { L } = 1 0 0 m s / s a m p l e$ and = 100the high sampling rate sH ms/sample. The time window $T _ { p }$ = 30is ms and K is 3. We will show the effectiveness of 3000our method in the evaluation.

# B. Data Processing

Raw CSI data are intrinsically noisy and need processing to improve the accuracy and robustness of further analysis.

1) Outlier Elimination: Since human motions usually alter certain propagation paths and lead to variations in multiple subcarriers, it is unlikely to cause jitters on a single subcarrier. Hence, such jitters are outliers. We adopt Hampel identifier [17], a simple univariate outlier detection method in Smokey. Based on Hampel identifier, any valid sample x should follow $| x - \mu | \leq \varepsilon \cdot \bar { \sigma }$ , where $\mu$ and σ are the median ¯ ¯and the median absolute deviation (MAD) of the data sequence respectively. ε is a coefficient that defines normal ranges. It is application-dependent and we set it to 10 according to the characteristics of human motions. We apply Hampel identifier to 30 subcarriers respectively and eliminate the outliers in each subcarrier.

2) Interpolation: Even though we configure the transmitter sends packets with a fixed rate, the collected CSI sequences on receiver are non-uniformly sampled because we cannot

![](images/7c5c9f85a7aa26333241772bf2d5b2d20c63f87a9e0258bc46ddd55cab4044e0.jpg)



Fig. 6. Overview of Smokey.

guarantee that the receiver gets packets with the same rate due to packet loss, transmission delay and other processing delays. However, as explained in preliminary findings, we need time information to recognize the respirations of smoking. Therefore, interpolation is necessary to obtain the accurate time durations for further analysis. In Smokey, We adopt linear interpolation by adding samples with value equals to the previous sample in the missing sampling slots,to construct the CSI sequence with samples evenly spaced in time.

# C. Motion Acquisition

Human motions are not the only factor affecting wireless signal. Consequently, some subcarriers may be more sensitive to human motions. Leveraging all the subcarriers is therefore not wise because the intrinsic noise on some subcarriers can be too serious to conceal the meaningful information about motions if the subcarriers are sensitive to noise but insensitive to human motions. Selecting the subcarriers can improve the accuracy. However, according to our observations, different subcarriers are sensitive to the motions of different body parts and the sensitivity of even a single subcarrier is dynamic due to the subtle environment changes. Hence, it is infeasible to select some certain subcarriers in advance, as previous methods usually do.

In designing Smokey’s motion extraction method for capturing the dynamic impacts from various subcarriers, we are facing the challenges that combining the information from informative subcarriers without the distractions caused by the uninformed subcarriers with intrinsic noise. To solve this challenge, we are inspired by the foreground detection problem in the image processing community. This problem aims to separate the foreground pixels in continuous image frames with the varying background caused by illumination changes and shadows swing [18]. In the context of Smokey, we want to separate the variations of CSI caused by motions (the foreground pixels) with dynamic noises (varying background). Having understood the similarity of two problem, we propose a foreground detection based method for motion acquisition.

![](images/940db5e783440f9396364f227eabb214fd07ce78e6e011742dc5fd23aa567b4d.jpg)



Fig. 7. Constructing CSI frames from CSI sequences.

![](images/44855a0c8f255904ffb94401979c751e8bc156815451c493fb238b9ced303466.jpg)



Fig. 8. The distributions of noises on different subcarriers.

1) Bulid CSI Frame: Smokey first projects the CSI sequences to CSI frames. As shown in Fig. 7, we partition time into consecutive windows with length T , containing N samples for each subcarrier. Then each frame contains $M \times N$ pixels, where M is the number of subcarriers. The pixel $P _ { m , n }$ in a frame is the CSI amplitude of subcarrier m collected within the n-th time window $( t _ { n } )$ . In Smokey, we have $M =$ subcarriers and we set $N = 1$ and $T = 3 0 m s$ =which is 30same to the sampling period.

2) Foreground Detection: After constructing the CSI frames, Smokey analyzes the pixel values in each frame. The pixels which do not fit the background distribution will be considered as foreground pixels caused by human motions.

a) Constructing the background model: it is well known that the background noise on a single subcarrier usually follows a Gaussian distribution. In the context of analyzing background by the whole frequency band, each pixel in the scene should be modelled by a mixture of K Gaussian distributions. We collect the CSI under static environments without human motions and plot the distributions of CSI samples on different subcarriers in Fig. 8. A mixture of Gaussian distributions is suitable to model the background noise.

The probability that a pixel has value $\mathbf { x } _ { t }$ at time t can be written as:

$$
p (\mathbf {x} _ {t}) = \sum_ {i = 1} ^ {K} w _ {i, t} \eta (\mathbf {x} _ {t}, \mu_ {i, t}, \Sigma_ {i, t}) \tag {2}
$$

where K is the number of Gaussian distributions, $w _ { i , t }$ and $\mu _ { i , t }$ are the estimated weight and the mean value of the i-th Gaussian in the mixture at time t respectively. $\Sigma _ { i , t }$ are Σand covariance matrix of the i-th Gaussian in the mixture at time t, which is assumed as:

$$
\Sigma_ {i, t} = \sigma_ {i} ^ {2} \mathbf {I} \tag {3}
$$

η is a Gaussian probability density function:

$$
\eta (\mathbf {x} _ {t}, \mu , \Sigma) = \frac {1}{(2 \pi) ^ {\frac {n}{2}} | \Sigma | ^ {\frac {1}{2}}} e ^ {- \frac {1}{2} (\mathbf {x} _ {t} - \mu) ^ {T} \Sigma^ {- 1} (\mathbf {x} _ {t} - \mu)} \tag {4}
$$

At time $t ,$ the Gaussian distributions are ordered by the fitness value $w _ { i , t } / \sigma _ { i , t }$ . Then the first B distributions are chosen as the background model, where

$$
B = \underset {b} {\arg \min} \left(\sum_ {i = 1} ^ {b} w _ {i, t} > P\right) \tag {5}
$$

$P$ is the minimum prior probability that background noise is in the trace.

b) Foreground extraction: after obtaining the background model, foreground pixels are extracted by marking any pixel that is more than 2.5 standard deviations away from the B distributions. Fig. 9 (b) presents the results of extracted foreground of the CSI frames in Fig. 9 (a).   
c) Online updating model: self-adaptation to the environment changes is one of the advantages of our foreground detection method. The wireless channel is time-varying. And the posture changes of humans such as in Fig. 9 (a) can also affect the background distribution. Using a model with pre-defined parameters is not appropriate to describe the background. We then propose online updating the background model to adapt to the background environment changes.

If current pixel value does not match any of the K distributions, the distribution with smallest weight is replaced with a distribution with current value as the mean, a high initial variance and low prior weight. In Smokey, the initial variance is 10 and prior weight is $1 / K$ .

1The weight of the K distributions are adjusted as follows

$$
\hat {w} _ {i, t} = (1 - \alpha) \hat {w} _ {i, t - 1} + \alpha \hat {p} (\omega_ {i} | \mathbf {x} _ {t}) \tag {6}
$$

where $\hat { p } ( \omega _ { i } | \mathbf { x } _ { t } )$ is 1 if $\omega _ { i }$ is the first Gaussian distribution that $\mathbf { x } _ { t }$ ˆ( )matches, or 0 otherwise.

The $\mu$ and σ remain the same for unmatched distributions. For the distributions match the pixel value, the $\mu$ and $\sigma$ are updated as follows

$$
\hat {\mu} _ {i, t} = (1 - \alpha) \hat {\mu} _ {i, t - 1} + \rho \mathbf {x} _ {t} \tag {7}
$$

$$
\hat {\Sigma} _ {i, t} = (1 - \alpha) \hat {\Sigma} _ {i, t - 1} + \rho (\mathbf {x} _ {t} - \hat {\mu} _ {i, t}) (\mathbf {x} _ {t} - \hat {\mu} _ {i, t}) ^ {T} \tag {8}
$$

$$
\rho = \alpha \eta (\mathbf {x} _ {t}, \hat {\mu} _ {i, t - 1}, \hat {\Sigma} _ {i, t - 1}) \tag {9}
$$

In foreground detection algorithm, only the learning rate α and prior probability of background noise T are parameters needed to be set for the system. Based on our application scenario, α is set to 0.002 and T is set to 0.25.

3) Motion Extraction: To avoid missing meaningful information, foreground detection component aggressively extracts all the foreground CSI variations possibly caused by human motions. Some counterfeit foregrounds that are not caused by human motions may exist, as shown in Fig. 9 (b).

We leverage the temporal correlation and the frequency correlation to filter out the counterfeit foregrounds. Human motions usually alter certain propagation paths for a period of time, leading to the temporal correlation. The altered propagation paths usually affects multiple subcarriers simultaneously, leading to the frequency correlation. Therefore, we filter out the foregrounds with short time durations or the foregrounds that affects limited number of subcarriers. If a foreground segment has a duration shorter than $T _ { F }$ seconds or affects less than $S _ { F }$ subcarriers, it is removed from the foreground. The filtered foreground is shown in Fig. 9 (c).

![](images/eb38cbde8306c2b3a9114df56f92f76839e4ffc7b8fa23cf28ed31d33b1bd4e8.jpg)



(a)

![](images/0174e1fac35fdc7ba28571d30771e3b95dd537250fcebec29c3416a26d8a2452.jpg)



(b)

![](images/34bdc4676da2e9d059633cd2d0be33c313a681b7e22a2345e2e29686e2ad002e.jpg)



![](images/a13b14063db299b338728168172133a2e26d25a13bad7e4c60b1c377bba73c12.jpg)



(d)   
Fig. 9. (a) The original CSI trace during smoking; (b) after foreground detection; (c) after motion extraction; (d) after composite motion detection.

4) Composite Motion Detection: The single motions need to be removed from the set of extracted motions because we only care smoking which is a composite motion. If a foreground segment does not have any segment $T _ { c }$ seconds before or after it, as the example in Fig. 9 (c), it is considered as a single motion and therefore removed. Then we get the foreground consisted of only composite motions as shown in Fig. 9 (d).

After getting the set of composite motions, we leverage the unique respiration pattern of smoking to judge each composite motion is smoking or not. We analyze the second motion of each composite motion, the inhalation duration is from the beginning of the motion to the peak and the exhalation duration is from the peak to the end of the motion. Then we calculate the difference between exhalation and inhalation durations. If the difference is larger than $T _ { r } ,$ the composite motion is regarded as smoking.

# D. Activity Analysis

As a monitoring system, false alarm is desired to be as less as possible. Hence, we design activity analysis which leverages the rhythmic pattern of smoking to reduce false positives.

1) Periodicity Analysis: In preliminary studies, we find smoking is a rhythmic activity. Therefore, we use periodicity analysis to verify whether a smoking-like rhythm exists for the suspect activity. In Smokey, we partition the time into detection windows with a fixed length equaled to time of smoking a cigarette which is 300s typically. Then we use autocorrelation to analyze the periodicity of the composite motions in each detection window. First, we integrate the information from all subcarriers by simply adding up the values in the foreground since we have obtained only meaningful information after motion acquisition component. Then we analyze the periodicity by detecting the peaks in the autocorrelation function of the integrated foreground sequence. After obtaining the periods, Smokey calculates the standard deviation of the periods to represent for the period’s stability.

In our current implementation, we use autocorrelation to perform periodicity analysis. In fact, frequency analysis is another common method to find periodicity. Fourier transform will provide all the individual frequency components of the waveform. The position of the biggest peak should be the fundamental frequency. If the peaks are harmonically related, but missing the fundamental, there won’t be a peak at the fundamental frequency. Then we have to further process the positions of the harmonics to find the fundamental frequency. On the other hand, autocorrelation is a measure of the similarity between the signals at different lags and the signal itself. When the fundamental frequency is missing, autocorrelation can still find the it by finding the greatest common divisor of the harmonics. In our application, smoking is only an activity that is rhythmic but not strictly periodical. By autocorrelation, we can easily get each period between two adjacent peaks of the autocorrelation function. It is more convenient to observe the period¡¯s stability, which is important for our method to make the judgement. Hence, in our current implementation, we use autocorrelation to perform the periodicity analysis.

![](images/13ae1cbd2fb8e7663d2161a7ea0e770f4f5f6ed5ff55d1e5adc2d9154e4f6e75.jpg)



Fig. 10. The autocorrelation of the foreground in Fig. 9 (d).

2) Activity Recognition: Smoking recognition is based on following intuitions. (1) The smoking period is at least longer than the normal breathing, which is about three seconds. (2) The smoking period can be longer than the normal duration of smoking a cigarette, which is about five minutes typically. (3) The smoking period is decided by the smoker’s habit and usually remains stable during a single cigarette. Based on these institutions, we set a valid range of smoking period, $[ T _ { m i n } , T _ { m a x } ]$ , where $T _ { m a x }$ is 300s, $T _ { m i n }$ is 3.3s since an [ ]adult breaths $1 2 \sim 1 8$ times per minute. We also set a threshold for the standard deviation of periods, $\sigma _ { T } ~ = ~ 5$ , consistent to the maximum period of normal breathing. As an example, in Fig. 10, we plot the autocorrelation of foreground in Fig. 9 (d). The extracted activity in Fig. 9 (d) has periodicity and the average period is 30 seconds which is in the valid range. The standard deviation is 3.095, which does not exceed $\sigma _ { T } .$ . Smokey therefore comes to a conclusion that there is smoking activities in the CSI trace of Fig. 9 (a).

# E. Using Multiple Antennas

Given the rapid development of MIMO (Multiple Input Multiple Output) technique, it is becoming more common for a wireless radio to have multiple antennas. Actually, our receiver supports up to three antennas. With multiple antennas, the CSI information will be much richer due to the spatial diversities of different antennas. In previous design, we have already show the effectiveness of using CSI to detect smoking activity. However, in practice, a single antenna may be influenced by environmental noise and the people around. To improve the robustness of Smokey in practice, we propose using multiple antennas. Each antenna detects the smoking activity individually and all the detection results will be fused to judge whether there is a smoking activity or not. For example, in Fig. 11, we collect the CSI by three antennas during smoking. We can find that Antenna 1 doesn’t capture the smoking information. But Antenna 2 and Antenna 3 are more sensitive to smoking and therefore more informative.

![](images/c4983710a5c47d585c765d7caf4f1e84b14988c600960546244fbc9a15fbc98f.jpg)



Fig. 11. CSI sequences collected by three antennas during smoking.

![](images/9f379704ac598473f820a943d5730a16fe3e2918a389b278f8ae9dc66c213b61.jpg)



Fig. 12. Boxplot of the CSI collected by three antennas during smoking.

1) Antenna Selection: From above example, we can find that many antennas are sensitive to the human motions but some others can be insensitive to the human motions, due to the spatial diversity of antennas. Processing CSI of uninformative antennas such as Antenna 1 will not help to improve the performance. Computation overhead can be saved if we can avoid processing the insensitive antennas. When extending our method to collect CSI from multiple users, a selection of the informative antennas is necessary to avoid wasting computation and network resources.

Fig. 12 presents a box plot of the CSI from three antennas. We can find that the sensitive antennas will have a large CSI variation. Hence, we use the variance of CSI to represent the information gain. If the variance of CSI raw data is larger than the threshold, we upload the users’ data to our serve for further processing. Otherwise, we drop the data to reduce the use of computation and network resources.

![](images/2bf382b1abefd1f1e2e1df7f725724d7d3496b7a0a68819597a72229f72f38e5.jpg)



Fig. 13. The layouts of the office room and the apartments. The deploying locations of the prototype are also shown in the figures.

2) Result Fusion: After getting the CSI data of different antennas from even multiple users, each antenna decides smoking exists or not individually. Then we fuse the results from individual judgements. If any antenna detects there is a smoking activity, Smokey sends the alarm of detecting the smoking event. By this way, we can improve the detection accuracy and improve the robustness for practical applications.

# IV. EVALUATION

In this section, we present the evaluation of Smokey under various environments to show its accuracy and robustness.

# A. Methodology

We implement a prototype of Smokey with commodity WiFi devices. We use a TP-LINK TL-WR742N wireless router as the transmitter and a mini PC with Intel WiFi Link 5300 NIC that equipped with one antenna as the receiver. Both devices operate in IEEE 802.11n mode on Channel 11 at 2.4GHz. We configure the receiver pings the transmitter to get the CSI measurements by the Linux CSI tool [12].

We evaluate the performance of Smokey in three real environments: (a) an apartment of $7 . 5 \times 4 . 5 \ m ^ { 2 }$ with a smoker living in, (b) an apartment of $7 . 5 \times 4 . 5 m ^ { 2 }$ with a non-7 5 4 5smoker living in, and (c) a smoking-allowed office room of $4 . 8 \times 3 . 6 m ^ { 2 }$ in an office building. The two apartments 4 8 3 6share the same structure. The layouts of the apartments and office room are shown in Fig. 13. The transmitter and receiver are placed 0.8m above the floor. For environment (a) and (b), we place the transmitter and receiver at “Location $\mathbf { A } ^ { \prime \prime }$ in Fig. 13. In each environment, we run Smokey for five workdays to count the number of smoking events. The two volunteers living in the apartments are office workers who usually stay at the apartments from 18:00 to 8:00 on the next day, on workdays. For environment (a) and (b), we get the ground truth by asking the volunteers report the times of smoking and the time they are smoking. For environment (c), we deploy a civil camera to record the events in the office room and count the number of smoking events manually as the ground truth. Note in the real experiments, we use the receiver with only one antenna to show Smokey can detect smoking even with the basic hardware setup. We will conduct individual experiments under controlled environments when the receiver is equipped with multiple antennas.

To quantify the performance of Smokey, we focus on (1) True Positive Rate (TPR): the fraction of cases where

TABLE I OVERALL ACCURACY OF SMOKEY IN REAL DEPLOYMENTS 

<table><tr><td></td><td>Apartment with a smoker living</td><td>Apartment with a non-smoker living</td><td>Smoking-allowed office room</td></tr><tr><td>Ground truth</td><td>42</td><td>0</td><td>235</td></tr><tr><td>TP of Smokey</td><td>41</td><td>0</td><td>216</td></tr><tr><td>FP of Smokey</td><td>7</td><td>4</td><td>27</td></tr><tr><td>Total activities Smokey detects</td><td>693</td><td>712</td><td>513</td></tr></table>

Smokey correctly detects the smoking events among all the detected activities, (2) False Positive Rate (FPR): the fraction of cases where Smokey mistakenly generates false alarm when there is actually no smoking event. Since we detect the smoking event instead of detailed smoking behaviors, we only label each activity as “smoking” or “non-smoking” rather than each motion in the activity.

# B. Accuracy of Smokey

1) Overall Accuracy: We present the overall accuracy in three real deployments in Table I. During the experiments, Smokey detects 693, 712 and 513 activities in environment (a), (b) and (c), respectively. An activity is defined as a series of motions within the time window. We artificially define an activity lasts five minutes equaled to the time length of smoking, which is a little bit different from the definition activity in semantics. Therefore, the number of activities are less than conventional wisdom. On the whole, Smokey successfully detects 92.8% of the smoking activities and misjudges 2.3% of the normal activities as smoking. In the relatively static environment such as the apartments that are usually occupied by the single occupant, the TPR of Smokey can be as high as 0.976 and the average FPR is low to 0.008. In the relatively dynamic environment in the office room where people come in and got out frequently, the TPR of Smokey drops to 0.919 and the FPR increases to 0.097.

2) Compare With the Baseline Methods: We compare Smokey with two baseline methods: using the best single subcarrier and using all subcarriers, in the apartment environments. In the scheme of using the best single subcarrier, we test all the subcarriers and select the single subcarrier with best performance as the result. In the scheme of using all the subcarriers, we directly combine the information on all subcarriers by adding up the CSI amplitudes.

To quantitatively compare the overall detection accuracy, we plot the Receiver Operating Characteristic (ROC) curves of four methods in Fig. 14. The ROC curve can depict the tradeoff between TPRs and FNRs over various settings. We find that using the best single subcarrier has the worst performance, only provides a TPR less than 0.2 when the FPR is 0.2. It is even worse than directly combining all the subcarriers which provides a 0.7 TPR when the FPR is 0.2. The reason behind this result is that the information about smoking are dynamically scattered in different subcarriers, a single subcarrier fails to gather enough information to detect the composite motions. Our foreground detection based motion acquisition (Smokey without PA) can identify 93.38% and 98.38% of the smoking activities when the FPR is 0.1 and 0.2 respectively. Keep the FPR to 0.1, PA (Periodicity Analysis) can improve the TPR by 7.2%, compared to Smokey without PA. When keeping the TPR as 1, PA helps Smokey to reduce the FPR from 0.265 to 0.043.

![](images/4d497f0c2cc5bf65c21a92081d49c799ccba43e5916b116019fb1bb53461274f.jpg)



Fig. 14. ROC curves of Smokey with/without PA (Periodicity Analysis), compared with two baseline methods.

3) Periodicity Analysis: In Fig. 15, we plot the autocorrelation results together with the CSI trace collected from environment (a) to show the effectiveness of our periodicity analysis component. After obtaining the motions extracted by foreground detection based motion acquisition, Smokey performs autocorrelation for each activity. Then Smokey extracts the peaks and calculates the intervals between adjacent peaks as the period. Then $\sigma ,$ the standard deviation of periods, is calculated and compared with the threshold $\sigma _ { T }$ . In Fig. 15, the 1st, 2nd and 4th activities have $\sigma > \sigma _ { T }$ and the $\sigma$ of the 3rd activity is smaller than $\sigma _ { T }$ . Smokey therefore concludes a smoking happens during the period from 10 to 15 minutes.

Periodicity analysis in Smokey uses the standard deviation of periods to analyze the stability of period. Hence, the threshold of the standard deviation of periods, $\sigma _ { T } .$ , is important to the accuracy. Fig. 16 plots the TPR and TNR of Smokey in environment (a) and (b) under a range of thresholds. Setting $\sigma _ { T } ~ = ~ 4 . 5$ provides best accuracy in this case. However, = 4 5in Smokey, we have no training set and we can only use the common features of smoking and some intuition universal to most people. $\sigma _ { T } = 5$ in our setting is also able to provide a = 5satisfied performance.

# C. Event-Driven Sampling

To ensure the efficiency of event-driven sampling, an accurate human presence detection method is the prerequisite. Hence, we evaluate the accuracy of our deviation-based detection method. We first conduct an validation experiment to show the effectiveness of our human presence detection. We set the low sampling rate $s _ { L } ~ = ~ 1 0 0 m s / s a m p l e$ and the detection window size $T _ { p } =$ ms. And we use only one antenna. = 1000Initially, no person in the monitoring area. We ask a person enter the area after 60 seconds. The person keeps walking in the area for one minutes and then leave the area. We plot the raw CSI on 30 subcarriers and the average standard deviation $\sigma _ { p }$ during the experiment as Fig. 17 shown. We can find that $\sigma _ { p }$ during s, s is obviously different. Then we can detect [60 120 ]the human presence by setting an appropriate threshold $\sigma _ { p t } .$ . Once detecting the human presence, Smokey will use the high sampling rate to collect more detailed information for the further analysis. Because the low sampling rate used in Smokey is same to the commercial WiFi beacon rate ( ms/sample), Smokey consumes no additional 100energy when there is no potential target in the monitoring area.

![](images/c7df572e5f37043c0850108685cb094ad597e1338676483e3568ba9603d995c0.jpg)



Fig. 15. Periodicity analysis of a piece of CSI traces collected from environment (a).

![](images/28b3285203ad92586a079911c60efbd1fc0166566cef86274494069cdd31c64d.jpg)



Fig. 16. Accuracy of Smokey vs. threshold σT .

![](images/3aca90e0581456b406d893981461990c505ad453b94fcca431916309ba7839e5.jpg)



Fig. 17. Human detection by the changes of average standard deviation. The person enters the monitoring area at 60s and leaves at 120s.

To further study the accuracy of our human detection method, we deploy the prototype (the setting is introduced in Section IV-A) and conduct experiments in three different environments: lab, corridor and classroom. Each time, we ask the volunteer to enter the monitoring area and wander around for one minute and then leave for one minute. The experiments run for 20 minutes in each environment. The experiment parameters are $S _ { L } = 1 0 0 m s / s a m p l e , \sigma _ { p t } = 0 . 8 .$ .

= 100 = 0 8We calculate the detection accuracy under two detection window size ms and ms. The results are shown 1000 3000in Fig. 18. The maximum and minimum accuracy are shown by the error bars. When $T _ { p }$ ms, we can see that the = 1000average detection accuracy is 100%, 98.4% and 80.8% in the lab, corridor and classroom, respectively. If we extend $T _ { p }$ from to ms, the average detection accuracy can be improved 3000to 100%, 100% and 98.3%, as the blue bars shown in Fig. 18. The experiment results demonstrate the effectiveness of our deviation-based human presence detection method. Therefore, the effectiveness of event-driven sampling is ensured.

![](images/41bef34d44db8d3a25684fe5df43cfeccbf2ce81cd873365b26f7896bbfe1a57.jpg)



Fig. 18. Accuracy of the human detection component.   
![](images/cdcddcaad1c3a4af8f5532c0e80ca5358f0cf6b5e71921dd46997ec8b136ed1b.jpg)



Fig. 19. Illustration of the experiment environments in LOS, NLOS, and through-wall scenarios.

# D. Robustness of Smokey

1) Impact of NLOS Propagation: One advantage of Smokey over the video surveillance is that it can work in NLOS propagation. We evaluate the performance of Smokey under the LOS, NLOS and through-wall scenarios, as illustrated in Fig. 19. The experiments are conducted in the apartment. For through-wall scenario, the transmitter and receiver are placed at “Location $\mathrm { C } ^ { \mathrm { { \mathfrak { p } } } }$ shown in Fig. 13. We first equip the receiver with only one antenna. We plot the ROC curves of Smokey with one antenna under different scenarios in Fig. 20. As expected, the accuracy degrades moderately in the NLOS scenario and drops sharply in the through-wall scenario. This is because the concrete wall causes significant attenuation and one antenna is not robust enough. Given the FPR of 0.01, the TPRs are 0.946, 0.567 and 0.304 for LOS, NLOS and through-wall scenarios, respectively. The results reveal that Smokey with one antenna is effective but more appropriate for the non-through-wall scenarios.

We then equip the receiver with three antennas and do the experiments again under the LOS, NLOS and throughwall scenarios. We plot the ROC curves of Smokey with three antennas under those scenarios in Fig. 21. As the results shown, using multiple antennas distinctly improves the accuracy. Given the FPR of 0.01, the TPRs when using three antennas are 0.988, 0.857 and 0.551 for LOS, NLOS and through-wall scenarios, respectively. The results demonstrate that Smokey with multiple antennas is more robust.

![](images/ed72c42b8a53ce2f18a32e29d62b5004eca1ceb2426f1b1106b5045c560229f2.jpg)



Fig. 20. ROC curves of Smokey in LOS, NLOS, and through-wall scenarios, when using one antenna.   
![](images/084dacbacf7e4490c19754364a001140ae86f8a7b3e8b90be33ab50f1bb22abf.jpg)



Fig. 21. ROC curves of Smokey in LOS, NLOS, and through-wall scenarios, when using three antenna.   
![](images/a7fcee47278b196583762f279507a5a9c9dbab5304a3dc8dc2706b19167df3ef.jpg)



Fig. 22. Accuracy of Smokey vs. device-to-target distances, when using one antenna.

This is because the spatial diversity between antennas provides different sensitivities to the human motions. Even though one antenna may fail to capture the smoking motions, other antennas are probably sensitive to the smoking motions.

2) Impact of Device-to-Target Distance: Different from existing gesture recognition systems that require targets near the transceivers, the distance between targets and transceivers can be long in our scenarios. We conduct experiments to evaluate the accuracy of Smokey when the target has various distances to the receiver (termed as device-to-target distance). We place the transmitter and receiver at “Location B” in the apartment shown in Fig. 13. The receiver is configured with a single antenna. We ask the smokers smoking with various distances to the receiver from 0.5m to 3.5m. We plot the TNRs and TPRs of Smokey in Fig. 22. We can find that the accuracy decreases with distance increasing, as expected. When the distance increases to 3m, Smokey is only able to detect 66.67% of the smoking activities, with a FPR 0.114.

We then use three antennas on the receiver and repeat the experiments. We plot the results in Fig. 23. The accuracy is significantly improved even when the distance is long. When the distance increases to m, Smokey can still detect 88.89% 3of the smoking activities, with a FPR 0.056. Compared to using a single antenna, the TPR is increased by 33.3% and the FPR is reduced by 50.9%. The experiment results demonstrate the robustness of Smokey when using multiple antennas.

![](images/85dfb6f0bc7a6049104d9fee4bee61525eac2fffb975f730bbca9b39436b610c.jpg)



Fig. 23. Accuracy of Smokey vs. device-to-target distances, when using three antennas.   
![](images/fb828cc5e9aa05615713f20260f10398972d4122beb4343dbed2b9e962bc2cb7.jpg)



Fig. 24. Accuracy of Smokey vs. CSI sampling rates, when using one antenna.

3) Impact of CSI Sampling Rate: Smokey extras information from CSI sequences. Therefore, the CSI sampling rate influences whether fine-grained information could be captured. We conduct experiments to investigate the performance of Smokey under various sampling rates. We ask a smoker smoking in the office room shown in Fig. 13. We vary the CSI sampling period from ms to ms per sample. Under 10 100each sampling period, we collect the traces during the smoker smoking to measure the detection accuracy. We repeat the experiment three times and calculate the average accuracy of Smokey.

The experiment results are shown in Fig. 24. As expected, the average accuracy decreases with the CSI sampling period increasing. This is because a longer sampling period leads to the loss of detail information. The average accuracy drops from . to . when sampling period increases from 1 00 0 75to ms per sample, and to . when sampling period 10 50 0 19further increases to ms per sample. But we also can 100find Smokey has certain resilience to the reduction of CSI sampling rate. Even the sampling period increases to ms per 40sample, the average accuracy maintains high. From the results, we can find that though Smokey still performs well when sampling period slightly increases, high CSI sampling rate is more preferred. This is also a reason of designing the eventdriven sampling component that detects human presence with low sampling rate. With event-driven sampling component, Smokey can starts sampling with high rate when any human presents. Smokey therefore balances the energy consumption and the detection accuracy.

4) Impact of Multiple People: The rationality behind Smokey is that the smoking motions affect WiFi signal propagation, which is reflected by the variations of CSI. Therefore, if there are too many people moving in the monitoring area, the impacts of smoking on WiFi signal can be corrupted by the motions that have larger impacts on CSI. Even though smoking in public places usually happens in the corners with few people around such as the restrooms and staircases, several people may present in the same monitoring area of Smokey. Note that we have already validate the effectiveness of Smokey under the scenario of multiple people by the experiments in the office in Section IV-B. In the office, there are multiple people working in there and some other people often go in and out. Here, we just want to specifically study the impacts of multiple people. To evaluate the robustness of Smokey in the environments with multiple people, we test its performance in two cases: (1) there are a smoker and several (1-4) non-smokers chatting in the office room, and (2) there are several (2-5) smokers smoking at the same time. We don’t restrict the movements in the room. But the volunteers usually have small movements such as changing body gesture and occasionally walk around in the office.

![](images/d2a535f973bbe292b0c7b418534f5dad4cf77c378a4051dccfc0c2355e901f16.jpg)



(a)

![](images/08d991882303f7701a9466fb80b6f9d87a101270e40acc0aa1d054d9203a765e.jpg)



(b)

Fig. 25. Accuracy of Smokey in scenarios with multiple people, when using one antenna. (a) Case 1: a single smoker is smoking and chatting with different number of non-smokers. (b) Case 2: multiple smokers are smoking at the same time.   
![](images/af92febd1a08427dc584137219aeb7eec5d92c65a10f79a6cacc6eef1bf364f2.jpg)



(a)

![](images/fd86f13a34191dcf202a68cf847e2c734221f0053c04ba4b580bfa6d2886303e.jpg)



(b)   
Fig. 26. Accuracy of Smokey in scenarios with multiple people, when using three antennas. (a) Case 1: a single smoker is smoking and chatting with different number of non-smokers. (b) Case 2: multiple smokers are smoking at the same time.

We plot the results of using one antenna under case (1) and (2) in Fig. 25(a) and (b). When there are two people in the environment, the TPR of case (1) and (2) is 1.0 and 0.95, respectively. When the number of people increases to five, the TPR is only 0.7 and 0.45 for case (1) and (2). For both cases, the accuracy degrades with the number of present people increasing. However, the degradation of case (2) is much faster than case (1). The reason behind the results may be that multiple smokers break the periodicity of smoking more seriously than multiple non-smokers.

We then plot the results when the receiver use three antennas under case (1) and (2) in Fig. 26(a) and (b). The accuracy of Smokey with three antennas increases to 0.889 when a smoker is smoking and other four non-smokers are around. When there are five smokers smoking at the same time, the accuracy can increase to 0.778. Compared to using one antenna, the performance is improved by 27% and 72.9% for case (1) and (2), respectively. The results demonstrate that using multiple antennas is an efficient way to increase the performance of Smokey. Besides, when using Smokey in practice, a crowdsourcing framework that encourages the volunteers contribute their CSI data to the system can be considered. With the help of multiple antennas from multiple devices, Smokey is expected be more robust and accurate.

# V. RELATED WORK

Computer Vision: Based on the civil cameras, researchers in the area of computer vision (CV) deal with the problem of gesture recognition by the motions of the person’s arms [4], [19], [20]. All these CV-based methods are effective when there are clear images. However, since cameras can only capture the line-of-sight (LOS) images, a bunch of blind spots will exist due to the deployment cost or privacy. Different from these CV-based methods with LOS requirements, Smokey detects the smoking activity by commercial WiFi devices under both LOS and NLOS environments.

Wearable Devices: With the development of embedded devices and sensors, wearable devices as well as smartphones are popular in our daily life. Researchers and engineers adopt specific sensors to sense the gas produced by tobacco such as carbon monoxide [2] and nicotine [3]. These sensors can only work in a very limited area to obtain enough concentration of nicotine or carbon monoxide for detection. Recently, researchers focus on leveraging the inertial sensors embedded in users’ devices to detect and monitor the smoking behavior of a smoker [16], [21], [22]. However, all these methods are usually designed for aids in smoking cessation programs. All of them require the targets wearing dedicated devices such as the chest band in mPuff [16], customized electronic lighter in UbiLighter [21], and wristband in RisQ [22]. No such intrusive device is available in our passive detection system.

Wireless Signal: To the best of our knowledge, Smokey is the first attempt that uses wireless signal to achieve device-free passive smoking detection. In the literature, researchers leverage wireless signal to recognize body motions such as walking forward and backward [10]. WiSee [9] and AllSee [23] recognize the pre-trained gestures by learning the training set of RSSI traces and use start gestures to help recognition achieve a high accuracy. Aforementioned systems rely on special hardwa-re such as USRP, self-designed circuit boards, or ultrawideband radar transceivers. Some works [24]–[27] analyze the human behaviors and location by analyzing the signals changes of devices attached on objects, which are not devicefree. Some researchers propose to recognize gestures by commercial WiFi devices. WiGest [8] uses existing WiFi signal to recognize certain hand gestures on top of a laptop with a short distance. It also requires the target to perform start gestures to reduce false positives. WiSleep [7] leverages the WiFi signal to monitor a person’s sleeping in a static environment without other motions’ interference. In Smokey, the potential violators may be neither compliant nor in the static environment.

# VI. CONCLUSION

We present Smokey, a device-free passive smoking detection system by leveraging the CSI information of WiFi signal. We design a foreground detection based motion acquisition method to extract the meaningful information from multiple noisy subcarriers even influenced by the posture changes. We also elaborately leverage the common features to recognize the series of motions during smoking, avoiding the targetdependent training set to achieve a high accuracy. We further leverage the diversity of multiple antennas to enhance the robustness of Smokey in practice. We also propose an eventdriven sampling mechanism to avoid congesting the wireless channel and unnecessary energy consumption. We prototype Smokey on commodity WiFi devices and evaluate it in various environments. Experimental results demonstrate the effectiveness and robustness of Smokey.

# REFERENCES

[1] U. S. Fire Administration. Smoking-Related Fires in Residential Buildings (2008–2010). Accessed: Sep. 22, 2017. [Online]. Available: https:// www.usfa.fema.gov/downloads/pdf/statistics/v13i6.pdf   
[2] Bedfont Scientific Ltd. piCO+ Smokerlyzer. Accessed: Sep. 22, 2017. [Online]. Available: http://www.bedfont.com/smokerlyzer/pico   
[3] Y. Liu, S. Antwi-Boampong, J. J. BelBruno, M. A. Crane, and S. E. Tanski, “Detection of secondhand cigarette smoke via nicotine using conductive polymer films,” Nicotine Tobacco Res., vol. 15, no. 9, pp. 1511–1518, 2013.   
[4] P. Wu, J.-W. Hsieh, J.-C. Cheng, S.-C. Cheng, and S.-Y. Tseng, “Human smoking event detection using visual interaction clues,” in Proc. IEEE Int. Conf. Pattern Recognit. (ICPR), Aug. 2010, pp. 4344–4347.   
[5] Z. Zhou, Z. Yang, C. Wu, L. Shangguan, and Y. Liu, “Omnidirectional coverage for device-free passive human detection,” IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 7, pp. 1819–1829, Jul. 2014.   
[6] Z. Zhou et al., “WiFi-based indoor line-of-sight identification,” IEEE Trans. Wireless Commun., vol. 14, no. 11, pp. 6125–6136, Nov. 2015.   
[7] X. Liu, J. Cao, S. Tang, and J. Wen, “Wi-sleep: Contactless sleep monitoring via WiFi signals,” in Proc. IEEE RTSS, Dec. 2014, pp. 346–355.   
[8] H. Abdelnasser, M. Youssef, and K. A. Harras. (Jan. 2015). “WiGest: A ubiquitous WiFi-based gesture recognition system.” [Online]. Available: https://arxiv.org/abs/1501.04301   
[9] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proc. ACM MobiCom, 2013, pp. 27–38.   
[10] F. Adib and D. Katabi, “See through walls with WiFi!” in Proc. ACM SIGCOMM, 2013, pp. 1–6.   
[11] wikiHow. How to Smoke a Cigarette. Accessed: Sep. 22, 2017. [Online]. Available: http://www.wikihow.com/Smoke-a-Cigarette   
[12] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 packet delivery from wireless channel measurements,” in Proc. ACM SIGCOMM, 2010, pp. 159–170.   
[13] Y. Xie, Z. Li, and M. Li, “Precise power delay profiling with commodity WiFi,” in Proc. ACM MobiCom, 2015, pp. 53–64.   
[14] Z. Li, Y. Xie, M. Li, and K. Jamieson, “Recitation: Rehearsing wireless packet reception in software,” in Proc. ACM MobiCom, 2015, pp. 291–303.   
[15] Z. Yang, Z. Zhou, and Y. Liu, “From RSSI to CSI: Indoor localization via channel response,” ACM Comput. Surv., vol. 46, no. 2, p. 25, 2013.   
[16] A. A. Ali et al., “mPuff: Automated detection of cigarette smoking puffs from respiration measurements,” in Proc. ACM IPSN, 2012, pp. 269–280.   
[17] F. R. Hampel, “A general qualitative definition of robustness,” Ann. Math. Statist., vol. 42, no. 6, pp. 1887–1896, 1971.   
[18] P. KaewTraKulPong and R. Bowden, “An improved adaptive background mixture model for real-time tracking with shadow detection,” in Video-Based Surveillance Systems, vol. 1. New York, NY, USA: Springer, 2002, pp. 135–144.   
[19] C. Nyirarugira and T. Kim, “Stratified gesture recognition using the normalized longest common subsequence with rough sets,” Signal Process. Image Commun., vol. 30, pp. 178–189, Jan. 2015.   
[20] S. B. Wang, A. Quattoni, L. Morency, D. Demirdjian, and T. Darrell, “Hidden conditional random fields for gesture recognition,” in Proc. IEEE CVPR, Apr. 2006, pp. 1–7.   
[21] P. M. Scholl, N. Kucükyildiz, and K. V. Laerhoven, “When do you light a fire?: Capturing tobacco use with situated wearable sensors,” in Proc. ACM UbiComp Adjunct, 2013, pp. 1295–1304.

[22] A. Parate, M.-C. Chiu, C. Chadowitz, D. Ganesan, and E. Kalogerakis, “RisQ: Recognizing smoking gestures with inertial sensors on a wristband,” in Proc. MobiSys, 2014, pp. 149–161.   
[23] B. Kellogg, V. Talla, and S. Gollakota, “Bringing gesture recognition to all devices,” in Proc. USENIX NSDI, 2014, pp. 1–15.   
[24] L. Shangguan et al., “ShopMiner: Mining customer shopping behavior in physical clothing stores with COTS RFID devices,” in Proc. ACM SenSys, 2015, pp. 113–125.   
[25] Z. Zhou, L. Shangguan, X. Zheng, L. Yang, and Y. Liu, “Design and implementation of an RFID-based customer shopping behavior mining system,” IEEE/ACM Trans. Netw., vol. 25, no. 4, pp. 2405–2418, Aug. 2017.   
[26] Z. Yin, C. Wu, Z. Yang, and Y. Liu, “Peer-to-peer indoor navigation using smartphones,” IEEE J. Sel. Areas Commun., vol. 35, no. 5, pp. 1141–1153, May 2017.   
[27] L. Shangguan, Z. Zhou, and K. Jamieson, “Enabling gesture-based interactions with objects,” in Proc. ACM MobiSys, 2017, pp. 239–251.

![](images/ac7d75aca7c4f98c8e70d32c25aff0e819097f9439ad0d59fbd35cbd37f6dff9.jpg)



Xiaolong Zheng (S’13–M’15) received the B.E. degree from the Dalian University of Technology in 2011, and the Ph.D. degree from The Hong Kong University of Science and Technology in 2015. He is currently a Post-Doctoral Researcher with the School of Software and TNLIST, Tsinghua University. His research interests include wireless networking and ubiquitous computing. He is a member of the ACM.

![](images/1a7520abf2e7b9aefcd776199e6c4b1d90c019b7b320472bbc18fe029ea9554d.jpg)



Jiliang Wang (M’10) received the B.E. degree from the Department of Computer Science, University of Science and Technology of China, in 2007, and the Ph.D. degree from the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology. He is an Assistant Professor with the School of Software and TNLIST, Tsinghua University. His research interest includes wireless sensor networks, network measurement, and pervasive computing.

![](images/da27c23093b118ede4f6484a0189c773312ad6853db73b1048459b0e7768fa2f.jpg)



Longfei Shangguan (M’11) received the B.S. degree in software engineering from Xidian University in 2011, and the Ph.D. degree from The Hong Kong University of Science and Technology in 2015. He is currently a Post-Doctoral Research Associate with the Computer Science Department, Princeton University. His research interests include pervasive computing and RFID system. He is a member of the ACM.

![](images/4206c25408e3cd6351787bbfbf9dd74b1bb5ffa0be20921f2eca9dc778196b77.jpg)



Zimu Zhou (M’13) received the B.E. degree from Tsinghua University in 2011, and the Ph.D. degree from The Hong Kong University of Science and Technology in 2015. He is currently a Post-Doctoral Researcher with ETH Zürich. His research interests include wireless localization and mobile computing. He is a member of the ACM.

![](images/fc5752d230b5fc7594d25c44605a37f6c9937411317471db2c5a1f00d984573e.jpg)



Yunhao Liu (F’15) received the B.S. degree in automation from Tsinghua University, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively. He is currently a Cheung Kong Professor and the Dean of the School of Software and TNLIST with Tsinghua University, China. He is also a member of the Tsinghua National Laboratory for Information Science and Technology. His research interests include RFID and sensor network,

the Internet and cloud computing, and distributed computing. He is a fellow of the ACM.