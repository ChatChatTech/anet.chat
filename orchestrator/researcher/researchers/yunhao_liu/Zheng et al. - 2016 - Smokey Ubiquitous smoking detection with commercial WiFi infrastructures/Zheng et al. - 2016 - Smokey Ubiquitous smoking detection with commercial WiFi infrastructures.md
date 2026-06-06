# Smokey: Ubiquitous Smoking Detection with Commercial WiFi Infrastructures

Xiaolong Zheng $^{*}$ , Jiliang Wang $^{*}$ , Longfei Shangguan $^{\dagger}$ , Zimu Zhou $^{\ddagger}$ , Yunhao Liu $^{*}$

\*School of Software and TNLIST, Tsinghua University

$^{\dagger}$ Computer Science Department, Princeton University

$^{\ddagger}$ Department of Computer Science & Engineering, Hong Kong University of Science and Technology

{xiaolong, jiliang, longfei, zimu, yunhao}@greenorbs.com

Abstract—Even though indoor smoking ban is being put into practice in civilized countries, existing vision or sensor-based smoking detection methods cannot provide ubiquitous smoking detection. In this paper, we take the first attempt to build a ubiquitous passive smoking detection system, which leverages the patterns smoking leaves on WiFi signals to identify the smoking activity even in the non-line-of-sight and through-wall environments. We study the behaviors of smokers and leverage the common features to recognize the series of motions during smoking, avoiding the target-dependent training set to achieve the high accuracy. We design a foreground detection based motion acquisition method to extract the meaningful information from multiple noisy subcarriers even influenced by posture changes. Without requirements of target's compliance, we leverage the rhythmical patterns of smoking to reduce the detection false positives. We prototype Smokey with the commodity WiFi infrastructure and evaluate its performance in real environments. Experimental results show Smokey is accurate and robust in various scenarios.

# I. INTRODUCTION

It is well recognized that smoking is not only a significant reason of death and disease worldwide, but also a leading cause of fire hazards. According to the report of the U.S. Fire Administration, there are about 7,600 smoking-related fires in homes each year, accounting for 17 percent of fire deaths in residential area [1]. More seriously, the death rate per 1,000 fires in smoking related indoor fires is seven times higher than that in nonsmoking related fires. Given the harms of smoking, public policies such as prohibiting smoking in public spaces, are put into practice in many countries. To ensure the polices really beneficial, an efficient ubiquitous monitoring system, which is able to automatically and accurately detect the smoking activities without attaching any device to the targets, is imperative.

Unfortunately, to the best of our knowledge, a ubiquitous smoking monitoring system is still absent. Sensor-based detection $[2]$ , $[3]$ is one of the most widely adopted passive detection methods. However, smog sensors are not sensitive enough to detect the tobacco smog when the room is large or the ceiling is high. For rooms without smog sensor based detection system, it is also costly to install such a detection system and it may even need to partially re-decorate the rooms after installation. Even the cost can be reduced, each smog sensor has limited sensing range, leading to detection blind point and detection delay $[2]$ , $[3]$ . Vision-based detection is another type of passive detection method. Applying computer vision (CV) technique to surveillance video can analyze human gestures for smoking detection [4]. Nevertheless, vision-based methods are restricted to LOS environments, hindering its applicability in a ubiquitous monitoring system. When smoking actions are blocked by obstacles, CV technique loses efficacy. Besides, due to the cost and privacy concerns, many blind spots exist in the areas without camera such as the stairwell and toilets.

In this paper, we ask the question: can we build a smoking detection system that (1) automatically and accurately detects the smoking activities without deploying special devices, (2) is non-intrusive for detection target, and (3) work efficiently in a wide range of environment conditions including both LOS and NLOS conditions? In this work, we leverage the commercial off-the-shelf (COTS) WiFi infrastructures to detect smoking activity. This naturally has two advantages. The WiFi infrastructure is widely available in indoor environments and low-cost to use. Leveraging the wireless signals does not require any device on the targets. We analyze the impact of smoking gestures on WiFi signal propagations and conduct preliminary experiments to validate the feasibility of detecting the smoking activity by its impacts on WiFi signals.

It has been shown that wireless signal provides an information carrier for gesture recognition through the characteristics of wireless signals such as Received Signal Strength (RSS) and Channel State Information (CSI) [5]–[9]. However, existing gesture recognition approaches based on wireless signals cannot be directly used in our scenario. Existing approaches assume relative simple or special gestures or a well-defined gesture training set. Meanwhile, existing approaches adopt various methods to improve input data quality. For example, existing approaches may need to specify the start and end of gesture recognition period in which users are required to perform gestures, so as to increase the detection accuracy. However, those requirements may not hold for smoking detection scenario.

To address above challenges, we take the first attempt to build a novel non-intrusive smoking detection system, namely Smokey, that is able to accurately detect the smoking activities by exploiting the impact of smoking on the CSI of WiFi. The design of Smokey is inspired by the following findings. First, instead of recognize a special gesture with carefully trained classifier, we exploit the periodical pattern for event detection. We find that smoking is a rhythmic activity that periodically affects the CSI of WiFi signals. This significantly reduces the impact of individual difference and the detection error comparing with gesture recognition based approach. Second, smoking is a composite activity that contains a series of motions of the arms and chest in the exact order, which is helpful to be distinguished from the daily activities. To avoid the dependency of a good training set, Smokey elaborately uses the temporal features such as the order of motions in smoking and the transition duration between motions.

The implementation of Smokey also faces several challenges. Since smoking consists of a sequence of motions, its impact on CSI is dynamically scattered across different subcarriers. Even in a single subcarrier, the noisy is also very high due to the passive detection method for uncooperative users in dynamic environment. We design a motion acquisition method, based on the foreground detection problem in image processing community, to extract useful information from the noisy CSI traces.

We implement Smokey on the commercial WiFi devices and evaluate its performance in real environments. The results show that Smokey can detect the smoking activities with a high TPR of 0.976 (0.919), along with a low FPR of 0.008 (0.097) using a single pair of transceivers in the relatively static (dynamic) environments. We also extensively evaluate the robustness of Smokey under various scenarios. The results show that the accuracy of Smokey is still about 70% even there are four non-smoker existing around the target smoker.

The contributions are summarized as follows.

- We investigate the characteristics of wireless signal impacted by smoking. We examine the challenges of using gesture recognition for detecting unknown smoking persons.   
- By exploiting the wireless signal characteristic, we take the first attempt to build a non-intrusive ubiquitous smoking detection method, Smokey. We validate the feasibility of using wireless signal for smoking detection.   
- we implement Smokey with commercial hardware and evaluate its performance. The experimental results demonstrate the effectiveness of Smokey.

In the rest of this paper, we will present the preliminary findings in Section II. Then we elaborate the design details of Smokey in Section III and evaluate its performance in Section IV. We present the related work in Section V and finally conclude our work in Section VI.

# II. PRELIMINARY FINDINGS

It has been shown that the environment changes such as the presence and motions of human can affect the communications between two wireless devices. The impacts can be captured and utilized for device-free human detection and localization $[5]$ . For example, the variations of Received Signal Strength Indicator (RSSI) caused by motions can be used to track the location of the object even behind the wall $[10]$ . By learning the characteristics of RSSI variations, body motions such as gestures can be recognized in $[8]$ .

Existing gesture recognition methods rely on repeatable impacts of motions on wireless signals. They are usually able to work well in the cases of simple or well-defined gestures near the transceivers. It is unclear how unrestricted activities such as smoking performed away from the transceivers affects the WiFi signals and whether it is possible to recognize smoking by its impacts on WiFi signals. In this section, we conduct the preliminary experiments to investigate the feasibility of recognizing smoking activities using WiFi signals.

![](images/1241a74db6663c3f5449ffdcd2bb9b1aff38f1dfa21f136b2e39550a8e9f58cd.jpg)  
(a)

![](images/58de45a88fdb17e0b0066fe30bbb833c5798ba552deac2e8902cde3ec149282a.jpg)  
(b)

![](images/615ee83f718adaef8d797e3db5eed785dc4b39c7268e3d1b7ee664e06c6b4dd4.jpg)  
(c)

![](images/04f77bfb388cb58b2d44f7cba73857193aca13ab963e6d56874ba38f571e9567.jpg)  
(d)

![](images/8b21d67d1a48d97982f8542f73bbc223bf74062e434fe1a03622a7fe97bcb39d.jpg)  
(e)

![](images/309736bae09a1e6958c2c866e0fd3d909dd59a005a9f297ebd9913d27ddc9575.jpg)  
(f)   
Fig. 1. Typical smoking steps: (a) holding the cigarette, (b) putting up the cigarette to mouth, (c) sucking the smoke in mouth, (d) putting down the cigarette, (e) inhaling the smoke, (f) exhaling the smoke.

# A. Smoking steps

We first introduce the smoking steps of a typical smoker. Normally, smoking a cigarette can be divided into holding phase and smoking phase. After lighting up a cigarette, a smoker usually holds the cigarette in hand and puts up the cigarette to mouth to suck the smoke intermittently. We can further decompose the smoking into six detailed steps $[11]$ , as Fig. 1 shown.

- (a) Holding the cigarette. Most of the time, a smoker holds the cigarette in hand.   
- (b) Putting up the cigarette to mouth. A smoker puts up the cigarette to the mouth for the subsequent inhalation.   
- (c) Sucking the smoke in mouth. Note that a smoker usually does not inhale the smoke into lung directly. Instead, the smoker suck the smoke into the mouth.   
- (d) Putting down the cigarette. After sucking enough smoke, the smoker will put down the cigarette.   
- (e) Inhaling the smoke. And then, the smoker inhales the smoke into the lung.   
- (f) Exhaling the smoke. At last, the smoker exhales the smoke and returns to the holding phase.

Smoking is a rhythmic activity. Step (a), i.e., holding phase, occupies most of the time of smoking. Step (b)-(f) compose the smoking phase which occurs intermittently. We call one round from Step (b) to Step (f) as one smoking motion. Several smoking motions together with the holding phases constitute a smoking activity. The durations of the holding and smoking motions are relatively stable because the smoker's smoking behavior usually remain unchanged.

# B. How Smoking Affects Wireless Signal

Step (b) and (d) are performed with arm motions. In Step (e) and (f), the inhalation and exhalation are performed with chest motions. In this section, we investigate how these motions affect WiFi signals.

![](images/0f48011bf9fc14e4c66a717dd630afdd89596315b2c9ad732a4c13192180a514.jpg)



Fig. 2. The RSSI and CSI sequences collected during smoking. Ground truth is obtained by the video record.

![](images/ab7f80a3b54928b42172a40cf43e93f1e4ba84a34003ec7d4abc4f1837687464.jpg)



Fig. 3. The CSI sequences of subcarrier #5, #14, and #23. Light gray areas are the periods of smoking phase from (b) to (d) with arm motions. Dark gray areas are the periods of smoking phase (e) and (f) with chest motions.

We deploy a TP-Link WR742N router and a mini PC with Intel 5300 NIC equipped with one antenna as the generators of WiFi signals. The PC is 5 meters from the router and it generates a 802.11 compliant packet every 30 milliseconds in average. We can therefore obtain the measurements of RSSI and CSI from packets every 30ms. Then we ask a person to smoke a cigarette between the transmitter and receiver, 1 meter away from the receiver.

1) Smoking affects CSI instead of RSSI: In Fig. 2, we plot the RSSI and CSI sequences obtained during smoking. Smoking motions are recorded in video in this smoking activity. The results clearly show RSSI varies over the time. However, the variation happens in both holding and smoking phases. There is no clear correlation between RSSI variation and the smoking motions. Then we investigate whether CSI is affected by the smoking activity. We find that CSI not only varies during smoking but also shows a very close correlation with smoking motions. This is because CSI is more informative than RSSI [12], [13] and hence more sensitive to smoking motions. The results shed light on detecting smoking activities by CSI information.   
2) The impacts of smoking are subcarrier-dependent: In Fig. 3, we plot the CSI sequences of subcarrier #5, #14,

and #23 during smoking. We can find that subcarrier #23 is affected from phase (b) to (d) but not during phase (e) and (f). On the contrary, subcarrier #14 is affected only during phase (e) and (f). For other subcarriers, similar observations also exist. The reason behind these observations is that subcarriers have different sensitivities for the motions of different parts of human body. During smoking motions, a portion of subcarriers may be sensitive to the motions of arms while another portion may be sensitive to the motions of chest. Therefore, different subcarriers are affected in different smoking phases.

3) The impacts of smoking on CSI vary dynamically on a single subcarrier: We find that the impacts of smoking on CSI vary dynamically across different subcarriers and the impacts are not stable even in a single subcarrier. Subcarrier #5 is affected from phase (b) to (f) in the first smoking motion ([11.7s, 22.8s]). However, in the second smoking motion ([60.2s, 68.0s]), subcarrier #5 is only affected from phase (b) to (d) but not in phase (e) and (f). This is because the smoker usually does not exactly repeat the same smoking motion. When the environment changes such as smoker posture changes, the sensitivities of subcarriers change, leading to the dynamic impacts on subcarriers even for the same motion.

4) Smoking is a composite activity that contains a series of motions in a certain order: Smoking is a composite activity consisting of a series of arm and chest motions in a certain order. We investigate three daily activities: eating, drinking, and deep breathing, which are considered to be confused with smoking. We collect the CSI traces when a person is smoking, eating a hamburger, drinking a cup of coffee and breathing deeply at the same location. Fig. 4 presents how these activities affects CSI. We can find that the CSI sequences show separate peaks when performing confusing activities, while the peaks during smoking appear in pairs. This is because smoking activity consists of a series of arm and chest motions in a certain order while other daily activities do not. Daily motions does not usually happen in the exact order as smoking.

We also find that the order of chest motions during smoking is unique. We plot the CSI amplitudes of subcarrier #27 during deep breathing and smoking in Fig. 5. Normally, the inhalation duration and exhalation duration in one respiration cycle are nearly the same, as shown in the top figure of Fig. 5. However, we find that the exhalation duration is obviously longer than the inhalation duration in smoking, as shown in the bottom figure of Fig. 5 (b). Such a phenomenon is also observed in previous work [14]. The authors in [14] use a wearable chest whist to monitor the chest motions and obtain those duration features to recognize the smoking activities. Such information can also be captured by CSI to help detect smoking activities.

# C. Summary

According to the preliminary study, we find smoking is a rhythmic composite activity that contains a series of motions in a certain order. This makes smoking distinguishable for daily motions such as putting arms up or down. The rhythm/order of motions is important information of the common behaviors of most smokers. Using rhythm/order information to detect smoking does not require to “decode” the precise information on a single motion, making it more resilient to detection errors in a single motion. However, we also find that (1) the impact to

![](images/6ef93c28e031481299cf4055afb9da916692154544a6ba0d9b0fcd34c6fe5f55.jpg)



(a) Smoking

![](images/137cebeae21ce8d6d3d5c4691bc5bf4e10b235a1a7ea1d7b630ff12f43a6f13e.jpg)



(b) Eating

![](images/18ac1f234e4e53f89e8200c160bb81cf4bf232ce2487153c9e7d1826e408086d.jpg)



(c) Drinking

![](images/c9a5d2685c7f29e7ae7cfba5612d932dcbe7d46202e9ce73c6fb1a7b5c9c07bb.jpg)



(d) Deep Breathing

Fig. 4. The CSI sequences collected during smoking and three other daily activities that may be confused with smoking.   
![](images/f3f4786912d43f708c81c516b3ba9e8cf214a456a85e4a5b6c04cde6f4408ab6.jpg)



![](images/db9bb06a6695ba63584a6145da1f648acd9f48a7fb035155d659adbc5514a31f.jpg)



Fig. 5. The CSI sequences on subcarrier #27 when the target is (a) deep breathing and (b) smoking.

CSI is dynamic across different subcarriers, and (2) the impact on CSI is also time-varying, making it difficult to extract useful information for detection. Hence, how to extract and leverage rhythm/order information for smoking detection, from time-varying and subcarrier-dependent CSI, needs delicate designs.

# III. SYSTEM DESIGN

In this section, we elaborate the designs of Smokey. Based on the preliminary findings, we propose to leverage the rhythmic pattern and the certain order of smoking motions to detect the smoking activities. Fig. 6 presents the overview of Smokey. First of all, the sampled CSI traces are processed to interpolate the irregular data to align time to get time information. Then the motion acquisition component extracts the interested motions that are suspected to be smoking. The extracted suspicious motions are further analyzed by activity analysis component from the aspect of periodicity to decide whether a smoking activity exists.

# A. Data Processing

Raw CSI data are intrinsically noisy and need processing to improve the accuracy and robustness of further analysis.

Interpolation. Even though we configure the transmitter sends packets with a fixed rate, the collected CSI sequences on receiver are non-uniformly sampled because we cannot guarantee that the receiver gets packets with the same rate due to packet loss, transmission delay and other processing delays. However, as explained in preliminary findings, we need time information to recognize the respirations of smoking.

![](images/5471f3bf7325b5e4bca2b340a12b12baf828f6c84d047f25a9d4ac247cf61d92.jpg)



Fig. 6. Overview of Smokey

Therefore, interpolation is necessary to obtain the accurate time durations for further analysis. In Smokey, We adopt linear interpolation by adding samples with value equals to the previous sample in the missing sampling slots, to construct the CSI sequence with samples evenly spaced in time. Here, we just process the data to reduce the time deviation. In future work, uncertain data processing techniques such as $[15]$ may help to reduce the amplitude error.

# B. Motion Acquisition

Human motions are not the only factor affecting wireless signals. Consequently, some subcarriers may be more sensitive to human motions. Leveraging all the subcarriers is therefore not wise because the intrinsic noise on some subcarriers can be too serious to conceal the meaningful information about motions if the subcarriers are sensitive to noise but insensitive to human motions. Selecting the subcarriers can improve the accuracy. However, according to our observations, different subcarriers are sensitive to the motions of different body parts and the sensitivity of even a single subcarrier is dynamic due to the subtle environment changes. Hence, it is infeasible to select some certain subcarriers in advance, as previous methods usually do.

In designing Smokey's motion extraction method for capturing the dynamic impacts from various subcarriers, we are facing the challenges that combining the information from informative subcarriers without the distractions caused by the uninformed subcarriers with intrinsic noise. To solve this challenge, we are inspired by the foreground detection problem in the image processing community. This problem aims to separate the foreground pixels in continuous image frames with the varying background caused by illumination changes and shadows swing [16]. In the context of Smokey, we want to separate the variations of CSI caused by motions (the foreground pixels) with dynamic noises (varying background). Having understood the similarity of two problem, we propose a foreground detection based method for motion acquisition.

![](images/054ad275ff842b2cdc7bf62ffc2afa898661196cac090923087e1ea210faa5e5.jpg)



Fig. 7. Constructing CSI frames from CSI sequences

CSI Frame. Smokey first projects the CSI sequences to CSI frames. As shown in Fig. 7, we partition time into consecutive windows with length T, containing N samples for each subcarrier. Then each frame contains $M \times N$ pixels, where M is the number of subcarriers. The pixel $P_{m,n}$ in a frame is the CSI amplitude of subcarrier m collected within the n-th time window ( $t_{n}$ ). In Smokey, we have M = 30 subcarriers and we set N = 1 and T = 30ms which is same to the sampling period.

Foreground Detection. After constructing the CSI frames, Smokey analyzes the pixel values in each frame. The pixels which do not fit the background distribution will be considered as foreground pixels caused by human motions.

(1) Constructing the background model: it is well known that the background noise on a single subcarrier usually follows a Gaussian distribution. In the context of analyzing background by the whole frequency band, each pixel in the scene should be modelled by a mixture of K Gaussian distributions. We collect the CSI under static environments without human motions and plot the distributions of CSI samples on different subcarriers in Fig. 8. It is clear a mixture of Gaussian distributions is suitable to model the background noise.

The probability that a pixel has value $\mathbf{x}_t$ at time $t$ can be written as:

$$
p (\mathbf {x} _ {t}) = \sum_ {i = 1} ^ {K} w _ {i, t} \eta (\mathbf {x} _ {t}, \mu_ {i, t}, \Sigma_ {i, t}) \tag {1}
$$

where K is the number of Gaussian distributions, $w_{i,t}$ and $\mu_{i,t}$ are the estimated weight and the mean value of the i-th Gaussian in the mixture at time t respectively. $\Sigma_{i,t}$ are and covariance matrix of the i-th Gaussian in the mixture at time t, which is assumed as:

$$
\Sigma_ {i, t} = \sigma_ {i} ^ {2} \mathbf {I} \tag {2}
$$

$\eta$ is a Gaussian probability density function:

$$
\eta (\mathbf {x} _ {t}, \mu , \Sigma) = \frac {1}{(2 \pi) ^ {\frac {n}{2}} | \Sigma | ^ {\frac {1}{2}}} e ^ {- \frac {1}{2} (\mathbf {x} _ {t} - \mu) ^ {T} \Sigma^ {- 1} (\mathbf {x} _ {t} - \mu)} \tag {3}
$$

![](images/daefa02a0d708da0b2d41f1f51750d832e3fbeb3dbf0395b7bcadba431de8a4b.jpg)



Fig. 8. The distributions of noises on different subcarriers.

At time t, the Gaussian distributions are ordered by the fitness value $w_{i,t}/\sigma_{i,t}$ . Then the first B distributions are chosen as the background model, where

$$
B = \underset {b} {\arg \min} \left(\sum_ {i = 1} ^ {b} w _ {i, t} > P\right) \tag {4}
$$

P is the minimum prior probability that background noise is in the trace.

(2) Foreground extraction: after obtaining the background model, foreground pixels are extracted by marking any pixel that is more than 2.5 standard deviations away from the B distributions. Fig. 9 (b) presents the results of extracted foreground of the CSI frames in Fig. 9 (a).   
(3) Online updating model: one of the advantages of our foreground detection method is self-adaptive to the environment changes such as posture changes in Fig. 9 (a). This superiority is accomplished by online updating the background model to adapt to the background environment changes.

If current pixel value does not match any of the K distributions, the distribution with smallest weight is replaced with a distribution with current value as the mean, a high initial variance and low prior weight. In Smokey, the initial variance is 10 and prior weight is 1/K.

The weight of the $K$ distributions are adjusted as follows

$$
\hat {w} _ {i, t} = (1 - \alpha) \hat {w} _ {i, t - 1} + \alpha \hat {p} (\omega_ {i} | \mathbf {x} _ {t}) \tag {5}
$$

where $\hat{p}(\omega_{i}|\mathbf{x}_{t})$ is 1 if $\omega_{i}$ is the first Gaussian distribution that $x_{t}$ matches, or 0 otherwise.

The $\mu$ and $\sigma$ remain the same for unmatched distributions. For the distributions match the pixel value, the $\mu$ and $\sigma$ are updated as follows

$$
\hat {\mu} _ {i, t} = (1 - \alpha) \hat {\mu} _ {i, t - 1} + \rho \mathbf {x} _ {t} \tag {6}
$$

$$
\hat {\Sigma} _ {i, t} = (1 - \alpha) \hat {\Sigma} _ {i, t - 1} + \rho (\mathbf {x} _ {t} - \hat {\mu} _ {i, t}) (\mathbf {x} _ {t} - \hat {\mu} _ {i, t}) ^ {T} \tag {7}
$$

$$
\rho = \alpha \eta (\mathbf {x} _ {t}, \hat {\mu} _ {i, t - 1}, \hat {\Sigma} _ {i, t - 1}) \tag {8}
$$

In foreground detection algorithm, only the learning rate $\alpha$ and prior probability of background noise T are parameters needed to be set for the system. Based on our application scenario, $\alpha$ is set to 0.002 and T is set to 0.25.

![](images/f68e193eecb7bc0c298660fc5ac392705a455804b7557bb9f1d9ac8c4ce207bc.jpg)



(a)

![](images/82ddff7ffce865d8914800106f6d5f7b7154c1077ad1c379cc0b20448574bde7.jpg)



(b)

![](images/942e2f5638523dc5058c0279660a107ce01208a5cba4e3046c573dbc9d5ffe35.jpg)



(c)

![](images/0ba6919f15cb73cdd2fc437dbd75494a62ef6e8203e78c8f5dba6ad55e3ff63d.jpg)



(d)   
Fig. 9. (a): The original CSI trace during smoking; (b): after foreground detection; (c): after motion extraction; (d): after composite motion detection.

Motion Extraction. To avoid missing meaningful information, foreground detection component aggressively extracts all the foreground CSI variations possibly caused by human motions. Some counterfeit foregrounds that are not caused by human motions may exist, as shown in Fig. 9 (b).

We leverage the temporal correlation and the frequency correlation to filter out the counterfeit foregrounds. Human motions usually alter certain propagation paths for a period of time, leading to the temporal correlation. The altered propagation paths usually affects multiple subcarriers simultaneously, leading to the frequency correlation. Therefore, we filter out the foregrounds with short time durations or the foregrounds that affects limited number of subcarriers. If a foreground segment has a duration shorter than $T_{F}$ seconds or affects less than $S_{F}$ subcarriers, it is removed from the foreground. The filtered foreground is shown in Fig. 9 (c).

Composite Motion Detection. The single motions need to be removed from the set of extracted motions because we only care smoking which is a composite motion. If a foreground segment does not have any segment $T_{c}$ seconds before or after it, as the example in Fig. 9 (c), it is considered as a single motion and therefore removed. Then we get the foreground consisted of only composite motions as shown in Fig. 9 (d).

After getting the set of composite motions, we leverage the unique respiration pattern of smoking to judge each composite motion is smoking or not. We analyze the second motion of each composite motion, the inhalation duration is from the beginning of the motion to the peak and the exhalation duration is from the peak to the end of the motion. Then we calculate the difference between exhalation and inhalation durations. If the difference is larger than $T_{r}$ , the composite motion is regarded as smoking.

# C. Activity Analysis

As a monitoring system, false alarm is desired to be as less as possible. Hence, we design activity analysis which leverages the rhythmic pattern of smoking to reduce false positives.

Periodicity Analysis. In Smokey, we partition the time into detection windows with a fixed length equaled to time of smoking a cigarette which is 300s typically. Then we use autocorrelation to analyze the periodicity of the composite motions in each detection window. Autocorrelation is a simple yet effective approach to assess the periodic signals. First, we integrate the information from all subcarriers by simply adding up the values in the foreground since we have obtained only meaningful information after motion acquisition component. Then we analyze the periodicity by detecting the peaks in the autocorrelation function of the integrated foreground sequence. After obtaining the periods, Smokey calculates the standard deviation of the periods to represent for the period's stability.

![](images/c6d8c14aad50d6b170e5e544826662e677b76bcebb9ccf0b72d9e396311be5c4.jpg)



Fig. 10. The autocorrelation of the foreground in Fig. 9 (d).

Activity Recognition. Smoking recognition is based on following intuitions. (1) The smoking period is at least longer than the normal breathing, which is about three seconds. (2) The smoking period can be longer than the normal duration of smoking a cigarette, which is about five minutes typically. (3) The smoking period is decided by the smoker's habit and usually remains stable during a single cigarette. Based on these institutions, we set a valid range of smoking period, $[T_{min}, T_{max}]$ , where $T_{max}$ is 300s, $T_{min}$ is 3.3s since an adult breaths 12\~18 times per minute. We also set a threshold for the standard deviation of periods, $\sigma_{T} = 5$ , consistent to the maximum period of normal breathing. As an example, in Fig. 10, we plot the autocorrelation of foreground in Fig. 9 (d). The extracted activity in Fig. 9 (d) has periodicity and the average period is 30 seconds which is in the valid range. The standard deviation is 3.095, which does not exceed $\sigma_{T}$ . Smokey therefore comes to a conclusion that there is smoking activities in the CSI trace of Fig. 9 (a).

# IV. EVALUATION

In this section, we present the evaluation of Smokey under various environments to show its accuracy and robustness.

# A. Methodology

We implement a prototype of Smokey with commodity WiFi devices. We use a TP-LINK TL-WR742N wireless router as the transmitter and a mini PC with Intel WiFi Link 5300 NIC that equipped with one antenna as the receiver. Both devices operate in IEEE 802.11n mode on Channel 11 at

![](images/bcf745ca678a651a7efe77942a2cfdedcea59a8e35dec2b2db547daa523c8f73.jpg)



Fig. 11. The layouts of the office room and the apartments. The deploying locations of the prototype are also shown in the figures.

TABLE I. OVERALL ACCURACY OF SMOKEY IN REAL DEPLOYMENTS DURING FIVE WORKDAYS 

<table><tr><td></td><td>Apartment with a smoker living</td><td>Apartment with a non-smoker living</td><td>Smoking-allowed office room</td></tr><tr><td>Ground truth</td><td>42</td><td>0</td><td>235</td></tr><tr><td>TP of Smokey</td><td>41</td><td>0</td><td>216</td></tr><tr><td>FP of Smokey</td><td>7</td><td>4</td><td>27</td></tr><tr><td>Total activities Smokey detects</td><td>693</td><td>712</td><td>513</td></tr></table>

2.4GHz. We configure the receiver pings the transmitter every 30ms to get the CSI measurements by the Linux CSI tool [17].

We evaluate the performance of Smokey in three real environments: (a) an apartment of $7.5 \times 4.5m^{2}$ with a smoker living, (b) an apartment of $7.5 \times 4.5m^{2}$ with a non-smoker living, and (c) a smoking-allowed office room of $4.8 \times 3.6m^{2}$ in an office building. The two apartments share the same structure. The layouts of the apartments and office room are shown in Fig. 11. The transmitter and receiver are placed 0.8m above the floor. For environment (b) and (c), we place the transmitter and receiver at “Location A” shown in Fig. 11. In each environment, we run Smokey for 5 workdays to count the number of smoking events. The two volunteers living in the apartments are office workers who usually stay at the apartments from 18:00 to 8:00 on the next day, on workdays. For environment (a) and (b), we get the ground truth by asking the volunteers report the times of smoking and the time they are smoking. For environment (c), we deploy a civil camera to record the events in the office room and count the number of smoking events manually as the ground truth.

To quantify the performance of Smokey, we focus on (1) True Positive Rate (TPR): the fraction of cases where Smokey correctly detects the smoking events among all the detected activities, (2) False Positive Rate (FPR): the fraction of cases where Smokey mistakenly generates false alarm when there is actually no smoking event. Since we detect the smoking event instead of detailed smoking behaviors, we only label each activity as “smoking” or “non-smoking” rather than each motion in the activity. An activity is defined as a series of motions within the time window equaled to the time of having a cigarette.

# B. Accuracy of Smokey

Overall accuracy. Table I presents the overall accuracy of Smokey in the three real deployments. During the 5 workdays, Smokey detects 693, 712 and 513 activities in environment (a), (b) and (c) respectively. We artificially define an activity lasts five minutes equaled to the time length of smoking, which is a little bit different from the definition activity in semantics. Therefore, the number of activities are less than conventional wisdom. On the whole, Smokey successfully detects 92.8% of the smoking activities and misjudges 2.3% of the normal activities. In the relatively static environment in the apartments where are usually occupied by the single occupant, the TPR of Smokey can be as high as 0.976 and the average FPR is low to 0.008. In the relatively dynamic environment in the office room where many people come in and got out frequently, the TPR of Smokey drops to 0.919 and the FPR increases to 0.097.

![](images/39f5cf246c8f1040587ac6d691d59ccfaa605f264bec69837961b8949dfc1042.jpg)



Fig. 12. ROC curves of Smokey with/without PA (Periodicity Analysis), compared with two baseline methods.

Compare with the baseline methods. We compare Smokey with two baseline methods: using the best single subcarrier and using all subcarriers, in the apartment environments. In the scheme of using the best single subcarrier, we test all the subcarriers and select the single subcarrier with best performance as the result. In the scheme of using all the subcarriers, we directly combine the information on all subcarriers by adding up the CSI values.

To compare the overall identification accuracy of these methods quantitatively, we plot the Receiver Operating Characteristic (ROC) curves of four methods in Fig. 12. The ROC curve can depict the tradeoff between TPRs and FNRs over various settings. We find that using the best single subcarrier has the worst performance, only provides a TPR less than 0.2 when the FPR is 0.2. It is even worse than directly combining all the subcarriers which provides a 0.7 TPR when the FPR is 0.2. The reason behind this result is that the information about smoking are dynamically scattered in different subcarriers, a single subcarrier fails to gather enough information to detect the composite motions. Our foreground detection based motion acquisition (Smokey without PA) can identify 93.38% and 98.38% of the smoking activities when the FPR is 0.1 and 0.2 respectively. Keep the FPR to 0.1, PA (Periodicity Analysis) can improve the TPR by 7.2%, compared to Smokey without PA. When keeping the TPR as 1, PA helps Smokey to reduce the FPR from 0.265 to 0.043.

Periodicity analysis. In Fig. 13, we plot the autocorrelation results together with the CSI trace collected from environment (a) to show the effectiveness of our periodicity analysis component. After obtaining the motions extracted by foreground detection based motion acquisition, Smokey performs autocorrelation for each activity. Then Smokey extracts the peaks and calculates the intervals between adjacent peaks as the period. Then $\sigma$ , the standard deviation of periods, is calculated and compared with the threshold $\sigma_{T}$ . In Fig. 13, the 1st, 2nd and 4th activities have $\sigma > \sigma_{T}$ and the $\sigma$ of the 3rd activity is smaller than $\sigma_{T}$ . Smokey therefore concludes a smoking happens during the period from 10 to 15 minutes.

![](images/99ef0417495c61f3f56461b6b91e3e4119cb4acb70677b5f5b281237af3a4269.jpg)



Fig. 13. Periodicity analysis of a piece of CSI traces collected from environment (a).

![](images/bdb035dd76bf6d3626ca8f5eadad3610a7c1b547f67355fb8b7adb03c8554c94.jpg)



Fig. 14. Accuracy of Smokey vs. threshold $\sigma_{T}$ .

Periodicity analysis in Smokey uses the standard deviation of periods to analyze the stability of period. Hence, the threshold of the standard deviation of periods, $\sigma_{T}$ , is important to the accuracy. Fig. 14 plots the TPR and TNR of Smokey in environment (a) and (b) under a range of thresholds. Setting $\sigma_{T}=4.5$ provides best accuracy in this case. However, in Smokey, we have no training set and we can only use the common features of smoking and some intuition universal to most people. $\sigma_{T}=5$ in our setting is also able to provide a satisfied performance.

# C. Impact of NLOS propagation

One advantage of Smokey over the video surveillance is that it can work in NLOS propagation. We evaluate the performance of Smokey under the LOS, NLOS and through-wall scenarios, as illustrated in Fig. 16. The experiments are conducted in the apartment. For through-wall scenario, the

![](images/ea07666aa6d8f8ef7068c7f12a7a640e8ecdd5300d69f0e416f6b326ba4462e8.jpg)



Fig. 15. ROC curves of Smokey in LOS, NLOS, and through-wall scenarios.   
![](images/58d3301067fcc557ddd6184f8b4ccadfba09cdc4aafc1c2ca081bbdfec053045.jpg)



Fig. 16. Illustration of the experiment environments in LOS, NLOS, and through-wall scenarios.

transmitter and receiver are placed at “Location C” shown in Fig. 11. We plot the ROC curves of Smokey under those scenarios in Fig. 15. As expected, the accuracy degrades moderately in the NLOS scenario and drop sharply in the through-wall scenario. Given the FPR of 0.01, the TPRs are 0.946, 0.567 and 0.304 for LOS, NLOS and through-wall scenarios respectively. These results reveal that Smokey is robust to the NLOS and through-wall scenarios. But it is more appropriate for the non-through-wall scenarios including both LOS and NLOS propagations.

# V. RELATED WORK

Wearable devices. With the development of embedded devices and sensors, wearable devices as well as smartphones are popular in our daily life. Researchers and engineers adopt specific sensors to sense the gas produced by tobacco such as carbon monoxide [2] and nicotine [3]. These sensors can only work in a very limited area to obtain enough concentration of nicotine or carbon monoxide for detection. Recently, researchers focus on leveraging the inertial sensors embedded in users' devices to detect and monitor the smoking behavior of a smoker [14], [18], [19]. However, all these methods are usually designed for aids in smoking cessation programs. All of them require the targets wearing dedicated devices such as the chest band in mPuff [14], customized electronic lighter in UbiLighter [18], and wristband in RisQ [19]. No such intrusive device is available in our passive detection system.

Computer Vision. Based on the civil cameras, researchers in the area of computer vision (CV) deal with the problem of gesture recognition by the motions of the person's arms [4] [20] [21]. All these CV-based methods are effective when there are clear images. However, since cameras can only capture the line-of-sight (LOS) images, a bunch of blind spots will exist due to the deployment cost or privacy. Different from these CV-based methods with LOS requirements, Smokey detects the smoking activity by commercial WiFi devices under both LOS and NLOS environments.

Wireless signals. In the literature, researchers leverage wireless signals to recognize body motions such as walking forward and backward $[10]$ . WiSee $[9]$ and AllSee $[22]$ recognize the pre-trained gestures by learning the training set of RSSI traces and use start gestures to help recognition achieve a high accuracy. Aforementioned systems rely on special hardwares such as USRPs, self-designed circuit boards, or ultra-wideband radar transceivers. Some researchers propose to recognize gestures by commercial devices. Some work $[23]$ – $[25]$ analyze the human behaviors and relative location by analyzing the signals changes of tags attached on objects, which are not device-free. WiGest $[8]$ uses existing WiFi signal to recognize certain hand gestures on top of a laptop with a short distance. It also requires the target to perform start gestures to reduce false positives. WiSleep $[7]$ leverages the WiFi signal to monitor a person's sleeping in a static environment with few other motions' interference. In Smokey, the potential violators may be neither compliant nor in the static environment.

# VI. CONCLUSION

We present Smokey, a device-free passive smoking detection system that leverages the CSI variation information of WiFi signals to detect the rhythmic smoking activity. We design a foreground detection based motion acquisition method to extract the meaningful information from multiple noisy subcarriers that are even influenced by the posture changes. We also elaborately leverage the common features to recognize the series of motions during smoking, avoiding the target-dependent training set to achieve a high accuracy. We prototype Smokey on commodity WiFi devices and evaluate it in various environments. Experimental results demonstrate the effectiveness and robustness of Smokey.

# ACKNOWLEDGMENT

This work is supported by NSFC\RGC Joint Research Scheme No. 61361166009, and also by NSFC under grants No. 61572277, 61373166 and 61532012.

# REFERENCES

[1] U.S. Fire Administration, “Smoking-Related Fires in Residential Buildings,” http://nfa.usfa.dhs.gov/downloads/pdf/statistics/v11i4.pdf.   
[2] Bedfont Scientific Ltd., “piCO $^{+}$ Smokerlyzer,” http://www.bedfont.com/cn/smokerlyzer/pico.   
[3] Y. Liu, S. Antwi-Boampong, J. J. BelBruno, M. A. Crane, and S. E. Tanski, “Detection of secondhand cigarette smoke via nicotine using conductive polymer films,” nicotine & tobacco research, 2013.   
[4] P. Wu, J.-W. Hsieh, J.-C. Cheng, S.-C. Cheng, and S.-Y. Tseng, “Human smoking event detection using visual interaction clues,” in Proceedings of IEEE International Conference on Pattern Recognition (ICPR), 2010.   
[5] Z. Zhou, Z. Yang, C. Wu, L. Shangguan, and Y. Liu, “Towards omnidirectional passive human detection,” in Proceedings of IEEE INFOCOM, 2013.   
[6] Z. Zhou, Z. Yang, C. Wu, Y. Liu, and L. M. Ni, “On multipath link characterization and adaptation for device-free human detection,” in Proceedings of IEEE ICDCS, 2015.   
[7] X. Liu, J. Cao, S. Tang, and J. Wen, “Wi-sleep: Contactless sleep monitoring via wifi signals,” in Proceedings of IEEE RTSS, 2014.   
[8] H. Abdelnasser, M. Youssef, and K. A. Harras, “Wigest: A ubiquitous wifi-based gesture recognition system,” arXiv preprint arXiv:1501.04301, 2015.   
[9] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proceedings of ACM MobiCom, 2013.   
[10] F. Adib and D. Katabi, “See Through Walls with WiFi!” in Proceedings of ACM SIGCOMM, 2013.   
[11] wikiHow, “How to smoke a cigarette,” http://www.wikihow.com/Smoke-a-Cigarette.   
[12] Y. Xie, Z. Li, and M. Li, “Precise power delay profiling with commodity wifi,” in Proceedings of ACM MobiCom, 2015.   
[13] Z. Li, Y. Xie, M. Li, and K. Jamieson, “Recitation: Rehearsing wireless packet reception in software,” in Proceedings of ACM MobiCom, 2015.   
[14] A. A. Ali, S. M. Hossain, K. Hovsepian, M. M. Rahman, K. Plarre, and S. Kumar, “mpuff: automated detection of cigarette smoking puffs from respiration measurements,” in Proceedings of ACM IPSN, 2012.   
[15] Y. Tong, L. Chen, Y. Cheng, and P. S. Yu, “Mining frequent itemsets over uncertain databases,” Proceedings of the VLDB Endowment, vol. 5, no. 11, pp. 1650–1661, 2012.   
[16] P. KaewTraKulPong and R. Bowden, “An improved adaptive background mixture model for real-time tracking with shadow detection,” in Video-based surveillance systems. Springer, 2002, pp. 135–144.   
[17] D. Halperin, W. Hu, A. Sheth, and D. Wetherall, “Predictable 802.11 packet delivery from wireless channel measurements,” in Proceedings of ACM SIGCOMM, 2010.   
[18] P. M. Scholl, N. Kücükyildiz, and K. V. Laerhoven, “When do you light a fire?: capturing tobacco use with situated, wearable sensors,” in Proceedings of ACM UbiComp Adjunct, 2013.   
[19] A. Parate, M.-C. Chiu, C. Chadowitz, D. Ganesan, and E. Kalogerakis, "Risq: recognizing smoking gestures with inertial sensors on a wristband," in Proceedings of MobiSys, 2014.   
[20] S. B. Wang, A. Quattoni, L. Morency, D. Demirdjian, and T. Darrell, "Hidden conditional random fields for gesture recognition," in Proceedings of IEEE CVPR, 2006.   
[21] C. Nyirarugira and T. Kim, “Stratified gesture recognition using the normalized longest common subsequence with rough sets,” Signal Processing: Image Communication, vol. 30, pp. 178–189, 2015.   
[22] B. Kellogg, V. Talla, and S. Gollakota, “Bringing gesture recognition to all devices,” in Proceedings of Usenix NSDI, 2014.   
[23] L. Shangguan, Z. Zhou, X. Zheng, L. Yang, Y. Liu, and J. Han, "Shopminer: Mining customer shopping behavior in physical clothing stores with cots rfid devices," in Proceedings of ACM SenSys, 2015.   
[24] H. Ding, L. Shangguan, Z. Yang, J. Han, Z. Zhou, P. Yang, W. Xi, and J. Zhao, “Femo: A platform for free-weight exercise monitoring with rfids,” in Proceedings of ACM SenSys, 2015.   
[25] L. Shangguan, Z. Yang, L. Alex, and Y. Liu, “Relative localization of rfid tags using spatial-temporal phase profiling,” in Proceedings of USENIX NSDI, 2015.