# RED: RFID-based Eccentricity Detection for High-speed Rotating Machinery

Yilun Zheng $^{1}$ , Yuan He $^{1}$ , Meng Jin $^{2}$ , Xiaolong Zheng $^{1}$ , Yunhao Liu $^{1}$

$^{1}$ School of Software, Tsinghua University & TNLIST, P.R. China

$^{2}$ Northwest University, P.R. China

zhengyl15@mails.tsinghua.edu.cn, heyuan@mail.tsinghua.edu.cn, mengj@stumail.nwu.edu.cn,

zhengxiaolong@mail.tsinghua.edu.cn, yunhao@greenorbs.com

Abstract—Eccentricity detection is a crucial issue for high-speed rotating machinery, which concerns the stability and safety of the machinery. Conventional techniques in industry for eccentricity detection are mainly based on measuring certain physical indicators, which are costly and hard to deploy. In this paper, we propose RED, a non-intrusive, low-cost, and real-time RFID-based eccentricity detection approach. Differing from the existing RFID-based sensing approaches, RED utilizes the temporal and phase distributions of tag readings as effective features for eccentricity detection. RED includes a Markov chain based model called RUM, which only needs a few sample readings from the tag to make a highly accurate and precise judgement. We implement RED with commercial-of-the-shelf RFID reader and tags, and evaluate its performance across various scenarios. The overall accuracy is 93.59% and the detection latency is 0.68 seconds in average.

# I. INTRODUCTION

Rotating machinery is a widely used part in industrial equipments, ranging from small motor to massive generator as shown in Fig. 1. Rotating machinery on those equipments generally plays a key function and counts the major portion of the manufactory cost. It's therefore necessary and crucial to ensure the mechanical health and normal operation of the rotating machinery. When a rotor is rotating, it keeps producing a centrifugal force. When the rotating speed goes high, the resulting strong centrifugal force can make a rotor's center axis deviate from its initial position, as shown in Fig. 2. This is so-called eccentricity. Eccentricity is generally harmful to rotating machinery. Countless industrial accidents and losses are caused by the eccentricity of rotating machinery [1]. Eccentricity detection, namely to detect eccentricity within specified time, becomes an indispensable component of rotating machinery in modern industry.

Conventional techniques in industry for eccentricity detection $[2]$ $[3]$ $[4]$ $[5]$ $[6]$ are mainly based on measuring certain physical indicators, such as electrical current, sound, temperature, vibration, etc. In order to obtain those information, it requires embedding special sensors and data acquisition instruments, which mean unaffordable costs in many cases. For the small rotating machinery, it is even impossible to embed extra hardware when they are manufactured. The above-mentioned facts call for a low-cost non-intrusive technique for eccentricity detection.

![](images/4fb37253fc48e5387bad522a6683e4cd7a0b43ee5d4abbb29cdad0e90c74f3bc.jpg)

![](images/bedf96dfbf014bb6415b2c16a2be2413dc7f82253fe9924a70cfd91f019976af.jpg)

![](images/bdf7d9de5c1bc2f35f43a7b7502c5973d11a5ad09217911d63e63dff6bb812d2.jpg)



![](images/90aa1f644cdcac975663076513d04f0820fe1f05fb8396c330765f4dbfbc7ed5.jpg)



Fig. 1. Some applications of rotating machineries, which are power generator, motor, car engine, and pump

Recent advances in Radio Frequency IDentification (RFID) make it a promising technique for sensing physical phenomenon. The existing works have explored RFID-based sensing in varied cases, e.g. orientation detection $[7]$ $[8]$ $[9]$ $[10]$ , humidity sensing $[11]$ , vibration inspection $[12]$ , motion detection $[13]$ and touch sensing $[14]$ . Successes in those cases demonstrate advantages of RFID-based sensing, especially the low cost and ease of deployment. Then an open problem naturally comes to our mind: Can RFID-based sensing detect eccentricity? After careful thinking and all-sided analysis, we find this problem is extremely challenging, due to the following reasons.

- High-speed rotation produces discrete tag readings. The rotation speed of rotating machinery is very high, typically over thousands RPM (revolutions per minute). The sampling frequency of commercial RFID tags is around 40Hz. When we attach an RFID tag to the surface of the rotor and let them rotate together, the RFID reader can only get sub-Nyquist sampling. The tag readings are essentially discrete and correspond to scattered positions of the tag.   
- High precision requirement. According to practice in industry, the eccentricity cannot exceed a specified distance, which is generally several millimeters or even shorter. Note that the readings from RFID tags are dynamic and noisy, while the resolution of RSSI (received signal strength indicator) readings is only 0.5 dB [15]. It is therefore infeasible to identify eccentricity, solely based

![](images/7878afeb97d8a66b499e8a21609f9452096f7e8d0d501d20d180df738b260413.jpg)



Fig. 2. A sketch of eccentricity

![](images/ebc6768326bc371332766ebbc1d893dfbcc2bc81864d30311d75e5d3a459da19.jpg)



Fig. 3. Experiment setup

on the RSSI and phase readings.

- Real-time requirement. Due to the high-speed rotation, eccentricity that exceeds a predefined threshold must be detected in real time. Otherwise, accidents are likely to happen before one can take any countermeasure.   
- High accuracy requirement. Not only false negative but also false positive alarms should be avoided in eccentricity detection. Excessive false positives will cause unnecessary downtime of the machinery, which is also a kind of loss.

In this paper, we propose RED, an RFID-based approach tailored for eccentricity detection in high-speed rotating machinery. The hardware requirement of RED is very simple: an RFID tag attached to the surface of the rotor and an RFID reader deployed nearby. The tag rotates with the rotor at the same speed, returning readings periodically to the reader. The design of RED is based on the following insight: Despite that every single reading is disorganized, the distribution of readings is stable if there is no eccentricity. When the rotor's eccentricity increases, the distribution of readings will also change. How much the distribution is varied reflects the distance of eccentricity (i.e. shift). We address non-trivial challenges in implementing the above idea and make RED a universal, non-intrusive, and low-cost solution. The contributions of this work are summarized as follows.

- In the context of high-speed rotation, we disclose the relationship between eccentricity and the probabilistic distribution of RFID readings. Instead of judging according to the RSSI and phase values, we identify the temporal and phase distributions of signals as effective features for eccentricity detection.   
- We propose a Markov chain based model called RUM for eccentricity detection. With the RUM model, RED only needs a few sample readings from the tag to make a highly accurate and precise judgement.   
- As a non-intrusive approach, RED is applicable to all kinds of rotating machinery. We implement RED with commercial-of-the-shelf RFID reader and tags, and evaluate its performance across various scenarios. The overall accuracy is 93.59% and the detection latency is 0.68 seconds in average.

The rest of this paper is organized as follows. In Section II, we describe our empirical studies. The design details of model RUM and the overview of RED are presented in Section III. Implementation and evaluation are described in Section IV. Section V discusses related works. We conclude and discuss future work in Section VI.

# II. EMPIRICAL STUDY

Figure 2 shows an eccentricity sketch. When eccentricity happens, the axis of the rotor has a shift $\Delta d$ relative to the initial position. At the same time, the rotation center of the tag shifts $\Delta d$ , too. In this section, we conduct a series of empirical studies to observe how the received signals change when eccentricity happens.

Figure 3 shows the devices that conduct the experiments. We use a centrifuge and a turntable. Their rotation speeds are 10000 RPM and 1 RPM, respectively. We simulate the eccentricity by moving the whole device away from the antenna. Alien UHF passive RFID tags [16] are attached onto the surface of these two devices. An ImpinJ Speedway R420 RFID reader [15] and a Laird circular polarized antenna are nearby, receiving the signals backscattered by the tags. From each sampling, the reader gets a RSSI and a phase value.

# A. The Change of RSSI and Phase

When the tag rotates at 1 RPM, the signal changes slowly and periodically as Fig. 4(a) shows. In a period, RSSI fluctuates within a stable interval, increasing from the minimum to the maximum and then decreasing. At the same time, the phase monotonically increases from 0 to $2\pi$ . We also find that when the tag rotates for half a circle, the RSSI and phase readings change accordingly for a period due to polarization [17]. By comparing the signals before and after eccentricity, both the waveform of RSSI and phase do not change. Only the minimum and the maximum of RSSI change, because the distance between the antenna and the tag changes.

# B. The Received Signals in Case of High-speed Rotation

Fig. 4(b) shows the received signals when the tag rotates at 10000 RPM. Different from Fig. 4(a), the signal is highly dynamic and discrete because of the high rotation speed and sub-Nyquist sampling. But we can still observe some difference from the RSSI readings caused by the shift of 1 cm. When the distance between the tag and the antenna increases, the maximum and the minimum values of the RSSI become smaller. Unfortunately, the phase readings are indistinguishable.

![](images/33b9781c470fe0a3fe3a2816fd5e571887d310be05ea89b4fe385a41c674f8ef.jpg)



—Initial position --Shift 1 cm   
![](images/30f8d11a6a5b60e442a04a33be5094be46396e195b4e9a91b2d2995225eee205.jpg)



(a) Tag rotates at 1 RPM

![](images/5ab5c75b206cf887011db8c68759f100d45d5df4076a43c4fef46e34552fd1a9.jpg)



—Initial position --Shift 1 cm   
![](images/74abec0ae77006abd78d224bfb7ebb644d9f88cd84875e71e4ded09035a36361.jpg)



(b) Tag rotates at 10000 RPM

![](images/62e024ac5adbb936111b889e518bc952c63d3d1b4e2a917d9330fe9374e816de.jpg)



\* Maximum before shift △ Maximum after shift of 1mm

![](images/27dc5aca06768cd4b4771b35e018d944d1de429c83ad9210c7f7d4ab9e4db5a7.jpg)



(c) The maximums of RSSI and their corresponding phase values before and after eccentricity

Fig. 4. Measured RSSI and phase before and after the eccentricity   
![](images/6c1c3ced9b8b95fe808e6545330018963d8f8759f87e2b669198530b43d50d04.jpg)



(a) The CDF of phase difference

![](images/c46327069836e7894e489e015a290d6706fe180b9e0aa6ca4e72b8a26e8ff150.jpg)



(b) The CDF of time interval

![](images/1f40ff592eeba86588d92931351d4b0dd86a816bd4d412136dbb25c32e8bd74b.jpg)



(a) The CDF of phase difference

![](images/bc43be45568e0224c2a2fd78ccff6dd097e2b01863b84be7459b0990debb2a6a.jpg)



(b) The CDF of time interval   
Fig. 5. The CDF of phase difference and time interval over four hours   
Fig. 6. The CDF of phase difference and time interval of two different tags

# C. Signal Analysis and Feature Extraction

According to the above findings, an intuitive idea for eccentricity detection is to detect whether the maximum of RSSI has changed. Consider that the RSSI readings fluctuates even if the tag is stable, we can hardly identify the maximum value, unless a sufficiently large number of samples are collected. What's more, the resolution of RSSI is 0.5 dB due to hardware limitation. When the shift is small, such as 1 mm, the maximum of RSSI stays constant as Fig. 4(c) shows. So it doesn't work if we only focus on the RSSI value of maximum.

We can observe from Fig. 4(c) that when the distance increases, the number of maximum increases during a certain time period. That is, the expected time interval between two maximum decreases. The corresponding phase values concentrate close to a certain value. The reason is that the periods of RSSI and phase are same, so the corresponding phase value of every RSSI is fixed if the environment remain the same. Then we can extract two different features. Consider the dynamics in the RSSI readings, we regard the RSSI readings that are above a certain threshold as the maximum values, and define the corresponding sample as E-points. We name them as E-points. Every time we get an E-point, we compute the time interval (denoted by Int) between this and the last E-point. We also compute the phase difference (denoted by Diff) between this and the last E-point. If the distance between the antenna and the tag increases, the expected Int increases while the expected Diff decreases.

# D. The Stability of The Two Features

We repeat the experiments several times, each for 1 minute, in different conditions to observe the distribution of phase difference and time interval of E-points. From Fig. 5 we can see that these two features are stable. When the tag stays at a fixed position. The CDFs of the two features are almost same over four hours.

# E. On Tag Diversity

We repeat the experiments with two different tag (Tag 1 and Tag 2) that located at the same position. The results are shown in Fig. 6. We can see that the distributions of phase difference and time interval are almost same. Between Tag 1 and Tag 2, hardware differences have almost no influence.

# F. The Distinguishability of The Two Features

Finally we compare the distribution of the two features before and after eccentricity. From Fig. 7 we can see that the result is consistent with our analysis. When the tag approaches the antenna, the maximum and the minimum of RSSI increases, and the number of E-points increases. As a result, the range of phase difference increases and the range of time interval decreases.

![](images/647b8ff2946541cfb02e05c013c115b1277f5ee512048442a83dc2581d98fa65.jpg)



(a) The CDF of phase difference

![](images/09057a2540b53538a82bf5766049c0943f134626eb55bbe5caffd37fc0270657.jpg)



(b) The CDF of time interval   
Fig. 7. The CDF of phase difference and time interval before and after the shift

# G. Findings

From the experiments, we found that in the context of high-speed rotation, the received signals are discrete and highly dynamic. When eccentricity happens, we can detect it by observing the distribution of phase difference and time interval of the E-points. These two features are distinguishable when eccentricity happens. They are stable over time. Tag diversity doesn't bring significant influence on them. Based on these findings, we can design an RFID-based eccentricity detection system.

# III. RED IN PRINCIPLE

To realize eccentricity detection, we propose RED. The first problem is the real-time requirement. Our findings are based on the statistical regularities of the accumulation of data, which is difficult to get in very short time. Besides, we can't get the training data under the environment of eccentricity in a real scenario, so we have no idea about how the distribution is after eccentricity when we deploy the devices in a new environment.

In this section, we first describe an overview of the eccentricity detection model, named RUM, used in this work, which is used to meet the real-time requirement, followed by detailed discussion of the main components of this model including estimate the distribution after eccentricity. At last, we describe how RED work as a whole system. The symbols used in this paper are listed in Table I.

# A. RUM: A Model for Eccentricity Detection

To meet the real-time requirement, we choose to design a Markov chain based model, using Diff and Int as input. It can compute the probabilities that every Diff and Int occur and transmit, and make judgement in several samples.

Specifically, according to the findings in Section II, the change in the distributions of the time interval and the phase difference between two sequentially E-points can be used as an indicator of eccentricity. Therefore, the problem of eccentricity detection can be stated as: given a sequence of E-point measurements, what is the probability that the center of the rotating machinery has deviated from its initial position?

![](images/5fd90ac494c88c4aaf66469b6e7d68eb5837f2d7c2fcb731e335d912fdd57f0f.jpg)



Fig. 8. Illustration of the RUM model

Given the length of the observation window w, we can get a E-point sequence $E_{i}=\{(T_{i},Ph_{i})|n-w\leq i\leq n-1\}$ . Then we can get the time interval sequence as $Int_{i}=\{T_{i+1}-T_{i}|n-w\leq i\leq n-2\}$ , and the phase difference sequence as $Diff_{i}=\{Ph_{i+1}-Ph_{i}|n-w\leq i\leq n-2\}$ . Now the problem is how to instantly detect the change in the Int and Diff sequences which indicates the eccentricity.

Here we choose to use a Markov chain based model (named RUM) which can trace the change in Int and Diff, and detect eccentricity instantly once abnormal Int and Diff occur.

In this model, we mainly focus on two probabilities. The probability that every observation $(Int_{i}, Diff_{i})$ occur is one indicator of eccentricity we use, denoted by $P_{out}^{Unecc}(Int_{i}, Diff_{i})$ , because it change as the distributions change caused by eccentricity. In addition to the probabilities of occurrence, the transition probabilities between two observation is another key indicator.

To compute the transition probabilities conveniently, in the RUM model, we define four states, i.e., States $S_{I}S_{D}$ , $\overline{S_{I}}S_{D}$ , $S_{I}\overline{S_{D}}$ , and $\overline{S_{I}S_{D}}$ (as shown in Fig. 8), to describe how likely the observed $(Int_{i}, Diff_{i})$ implies a non-eccentricity. Specifically, given the distributions of Int and Diff when eccentricity has not occurred, if both the observed $Int_{i}$ and $Diff_{i}$ locate within the pre-defined confidence intervals of Int and Diff (denoted by $Th_{I}$ and $Th_{D}$ ), we identify that $(Int_{i}, Diff_{i}) \in S_{I}S_{D}$ . State $\overline{S_{I}}$ (or $\overline{S_{D}}$ ) means that the observed $Int_{i}$ (or $Diff_{i}$ ) falls outside the confidence interval $Th_{I}$ (or $Th_{D}$ ).

Now the sequence of $(Int_{i}, Diff_{i})$ can be translated to a sequence of states $S_{n} = \{S_{n-1}, ..., S_{n-w}\}$ . Theoretically, if the eccentricity has not occurred, the observed $(Int_{i}, Diff_{i})$ are likely to stay on State $S_{I}S_{D}$ . However, due to the noises and interferences, the observed $(Int_{i}, Diff_{i})$ may occasionally transfer to States $\overline{S_{I}}S_{D}$ , $S_{I}\overline{S_{D}}$ , or even $\overline{S_{I}S_{D}}$ , but the transition probabilities are low. If eccentricity happens, the transition probabilities may increase. As a result, we can compute how likely the transitions happen in every observation window as a indicator of eccentricity.

Specifically, the probability that we can observe a transition chain $\{S_{n-1},\ldots,S_{n-w}\}$ under the non-eccentricity scenario

TABLE I
SOME TYPICAL SYMBOLS IN RED 

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $T_i$ </td><td>Arriving time of the E-point  $E_i$ </td></tr><tr><td> $Ph_i$ </td><td>Phase of the E-point  $E_i$ </td></tr><tr><td> $w$ </td><td>The length of the observation window</td></tr><tr><td> $P_{trans}^{unecc}(S_i|S_{i-1})$ </td><td>The transition probability between two sequential states in the non-eccentricity scenario</td></tr><tr><td> $P_{trans}^{ecc}(S_i|S_{i-1})$ </td><td>The transition probability between two sequential states in the eccentricity scenario</td></tr><tr><td> $P_{out}^{Unecc}(Int_i,Diff_i)$ </td><td>The probability that we can get a observation ( $Int_i, Diff_i$ ) when the eccentricity has not occurred</td></tr><tr><td> $P_{out}^{Ecc}(Int_i,Diff_i)$ </td><td>The probability that we can get a observation ( $Int_i, Diff_i$ ) when the eccentricity occurred</td></tr><tr><td> $P(ecc)$ </td><td>The prior probability which captures the occurrence frequency of eccentricity</td></tr><tr><td> $P(Int_i,Diff_i)$ </td><td>The probability of the observation ( $Int_i, Diff_i$ )</td></tr><tr><td> $\lambda$ </td><td>The mean value of  $Int$ </td></tr><tr><td> $Sa$ </td><td>The mean value of the sampling interval</td></tr><tr><td> $R_E$ </td><td>The RSSI range of the E-points</td></tr><tr><td> $R_{RSSI}$ </td><td>The value range of all the observed RSSIs</td></tr><tr><td> $P_{Unecc}$ </td><td>The probability that the eccentricity has not occurred</td></tr><tr><td> $P_{ecc}$ </td><td>The probability that the eccentricity has occurred</td></tr></table>

is:

$$
P _ {\text { chain }} ^ {U n e c c} = \prod_ {\mathrm{i=n-w}} ^ {n} P _ {\text { trans }} ^ {u n e c c} (S _ {i} | S _ {i - 1}). \tag {1}
$$

Then we can evaluate how likely we observe a state sequence $S_{n}$ under the non-eccentricity scenario using a normalized metric PoC as follow:

$$
P o C ^ {U n e c c} \left(\mathbf {S} _ {\mathbf {n}}\right) = \max \left\{\frac {P _ {\text { chain }} ^ {U n e c c} - \min _ {s \in S} \left(P _ {s}\right)}{\max _ {s \in S} \left(P _ {s}\right) - \min _ {s \in S} \left(P _ {s}\right)}, 1 - \frac {\operatorname{rank} \left(P _ {\text { chain }} ^ {U n e c c}\right) - 1}{| S |} \right. \tag {2}
$$

where $\mathbf{S}$ is the set of all the possible state sequences that include $n$ motions. $\operatorname{rank}(P_{\text{chain}}^{Unecc})$ is the ranking of $P_{\text{chain}}^{Unecc}$ among all the $P_s$ ( $s \in \mathbf{S}$ ).

Based on the $P_{out}^{Unecc}$ of each observed $(Int_{i}, Diff_{i})$ and the estimated $PoC^{Unecc}(\mathbf{S}_{\mathbf{n}})$ for the state sequence $S_{n}$ , we can give a normalized metric $PUnecc(\mathbf{S}_{\mathbf{n}})$ to describe how likely that the eccentricity does not occur:

$$
\begin{array}{l} P U n e c c (\mathbf {S _ {n}}) = P o C ^ {U n e c c} (\mathbf {S _ {n}}) \cdot m i n \{P _ {o u t} ^ {U n e c c} (I n t _ {n - 1}, D i f f _ {n - 1}), \\ \left. \dots , P _ {o u t} ^ {U n e c c} \left(I n t _ {n - w}, D i f f _ {n - w}\right) \right\} \tag {3} \\ \end{array}
$$

Similarly, we can also get a normalized metric $Pecc(\mathbf{S}_{\mathbf{n}})$ to describe how likely the state sequence $S_{n}$ implies an eccentricity scenario. Once RED detects a state sequence which results in $Pecc(\mathbf{S}_{\mathbf{n}}) > PUnecc(\mathbf{S}_{\mathbf{n}})$ , it considers that an eccentricity occurs.

In the following subsections, we will discuss how to estimate $P_{out}$ and PoC in detail.

# B. $P_{out}$ Estimation

The $P_{out}$ estimation component aims to calculate the $P_{out}^{Unecc}$ and $P_{out}^{ecc}$ for each observed $(Int_i, Diff_i)$ as an indicator of eccentricity. According to the Bayes' theorem, we can calculate these two probabilities using the corresponding posterior probability of each observation $(Int_i, Diff_i)$ , given the eccentricity has occurred or not, i.e., $P(Int_i, Diff_i|ecc)$

and $P(Int_i, Diff_i|Unecc)$ . The $P_{out}^{Unecc}$ and $P_{out}^{ecc}$ can be formulated as:

$$
\begin{array}{l} P _ {\text {out}} ^ {\text {Unecc}} = \frac {(1 - P (\text {ecc})) \cdot P (I n t _ {i} , D i f f _ {i} | U n e c c)}{P (I n t _ {i} , D i f f _ {i})} \tag {4} \\ P _ {o u t} ^ {e c c} = \frac {P (e c c) \cdot P (I n t _ {i} , D i f f _ {i} | e c c)}{P (I n t _ {i} , D i f f _ {i})} \\ \end{array}
$$

Since $P(Int_i, Diff_i)$ is the same for both eccentricity and non-eccentricity scenarios, we are only interested in calculating $P(Int_i, Diff_i|ecc)$ , $P(Int_i, Diff_i|Unecc)$ , and $P(ecc)$ :

$$
\begin{array}{l} P _ {o u t} ^ {U n e c c} = (1 - P (e c c)) \cdot P (I n t _ {i} | U n e c c) \cdot P (D i f f _ {i} | U n e c c) \\ P _ {o u t} ^ {e c c} = P (e c c) \cdot P (I n t _ {i} | e c c) \cdot P (D i f f _ {i} | e c c) \tag {5} \\ \end{array}
$$

$P(ecc)$ can be obtained from the statistic data. Therefore, the key goal translates to obtaining $P(Int_{i}|Unecc)$ , $P(Diff_{i}|Unecc)$ , $P(Int_{i}|ecc)$ , and $P(Diff_{i}|ecc)$ . It seems that we can obtain these posterior probabilities just based on training samples of Int and Diff. However, in real world deployment of RED, Int and Diff samples are all from the non-eccentricity scenario, making it difficult to obtain the empirical values of $P(Int_{i}|ecc)$ and $P(Diff_{i}|ecc)$ .

Fortunately, we find that the distribution of Int and Diff are indeed highly related to the factors like and the value range of the measured RSSIs and phases. These factors are proved measurable (or estimable) in both the eccentricity and non-eccentricity scenarios (as shown in this section later). Therefore, if we can find a accurate model to describe the relationship between these factors and the distribution of Int and Diff, then we can estimate the posterior probabilities without relying on the training phase. In the following, we focus on how to estimate $P(Int_{i}|Unecc)$ and $P(Diff_{i}|Unecc)$ , which can be generalized to the estimation of $P(Int_{i}|ecc)$ and $P(Diff_{i}|ecc)$ .

Estimation of $P(Int_{i}|Unecc)$ . Consider that the sampling interval is random in RFID systems, $P(Int_{i}|Unecc)$ is mainly determined by the occurrence probability of E-points $P_{E}^{Unecc}$ and $P_{E}^{Ecc}$ . Int follows the exponential distribution $^{1}$ as $Int \sim E(\lambda)$ . Thus we have:

$$
P (I n t _ {i} | U n e c c) = \lambda e ^ {- \lambda I n t _ {i}} \tag {6}
$$

where $\lambda = \frac{Sa}{P_E^{Unecc}}$ , and $Sa$ can be obtained from the specification of the RFID system. We will introduce how to estimate $P_E^{Unecc}$ and $P_E^{ecc}$ in Section III-C.

Estimation of $\mathrm{P}(\mathrm{Diff}_{\mathrm{i}}|\mathrm{Unecc})$ . The distribution of Diff is highly determined by the phase range of the E-points $[\alpha,\beta]$ . Therefore, considering that the sampling interval is random (as discussed earlier), Diff (ranges from 0 to $\beta-\alpha$ ) will follow the uniform distribution as $Diff \sim U(\frac{\beta-\alpha}{2}, \frac{(\beta-\alpha)^{2}}{12})$ . That is to say, theoretically we have:

$$
P (D i f f _ {i} | U n e c c) = \frac {1}{\beta - \alpha} \tag {7}
$$

In practice, the value of $\alpha$ and $\beta$ can be estimated based on the RSSI range of the E-points, which we will show in Section III-C.

# C. Estimation of $P_{E}^{Unecc}$ and $P_{E}^{ecc}$

As $P_E^{Unecc} = \frac{R_E}{R_{RSSI}}$ , we should estimate the range of the RSSIs and the phases of the E-points.

RSSI range. As discussed in Section III-B, $P(Int_{i}|Unecc)$ is highly related to the proportion of the E-points (i.e., $P_{E} = \frac{R_{E}}{R_{RSSI}}$ ), which is further determined by the RSSI range of the E-Points ( $R_{E}$ ) and the value range of all the sampled RSSIs ( $R_{RSSI}$ ). Here, $R_{E}$ is determined by the predefined threshold $Th_{p}$ . Therefore, to estimate $P_{E}$ , we have to estimate $R_{RSSI}$ .

In real world deployment of RED, the RSSI range in the non-eccentricity scenario can be estimated based on the RSSI samples. The RSSI range in the eccentricity scenario, however, needs to be estimated based on i) the RSSI range that in the non-eccentricity scenario $(R_{RSSI}^{Unecc})$ ; and ii) the expected detection precision of RED (namely $\Delta d$ mentioned in Section II). Specifically, assume that the effect of the polarization is negligible (since that the displacement of the tag is only in mm level), the RSSI range in the eccentricity scenario will change linearly compared with that in the non-eccentricity scenario. Therefore, if the rotating machinery shifts $\Delta d$ , the corresponding variation in RSSI (denoted by $\Delta R$ ) can be estimated by the Friis transmission formula [18].

Phase range. Phase range of the E-points (i.e., $[\alpha, \beta]$ ) is an important information which can be used to estimate the distribution of Diff in both eccentricity and non-eccentricity scenarios. In practice, the phase range can be estimated based on the proportion of the E-points $P_{E}$ . Specifically, the experimental results in Section II shows that the relation between the RSSI and the corresponding phase can be regarded as a sine function. Thus given the proportion of the E-points under

![](images/850dd9b83019141de720fea64b02ec6aeb55520b7d6223ff7786471385b6a627.jpg)



Fig. 9. Estimating of the transition probabilities

the non-eccentricity scenario (i.e., $P_E^{Unecc}$ ), the value of $\alpha$ and $\beta$ can be estimated by:

$$
\begin{array}{l} \alpha = \frac {\pi}{2} - \arcsin \left[ 1 - 2 \cdot \left(\frac {\Delta}{R _ {E}} + P _ {E} ^ {U n e c c}\right) \right] \tag {8} \\ \beta = \frac {\pi}{2} + a r c s i n \left[ 1 - 2 \cdot \left(\frac {\Delta}{R _ {E}} + P _ {E} ^ {U n e c c}\right) \right] \\ \end{array}
$$

Note that we can get the phase range in the non-eccentricity scenario by setting $\Delta = 0$ , while get the range in the eccentricity scenario by setting $\Delta = \Delta R$ .

# D. PoC Estimation

The main target of the PoC estimation component is to calculate the transition probability between each two states. Similar to the estimation of $P_{out}$ , we have to estimate the transition probabilities without relying on the training phase. In the following, we use the transition probabilities from State $S_{I}S_{D}$ to other states as a vehicle to explain the method to estimate the transition probabilities.

Assume that the transition between $S_{I}$ and $\overline{S_{I}}$ and that between $S_{D}$ and $\overline{S_{D}}$ are independent of one another. Based on this assumption, the transition probabilities between these “single states” (i.e., States $S_{I}$ , $\overline{S_{I}}$ , $S_{D}$ , and $\overline{S_{D}}$ ) is solely determined by the confidence interval of the distributions of Int or Diff. For example, the probability of the transition from $S_{I}$ to $\overline{S_{I}}$ can be simply calculated as $1 - Th_{I}$ and that of the transition from $S_{I}$ to $S_{I}$ is $Th_{I}$ .

Then let's look at the transition probabilities between “combined states” ((i.e., States $S_{I}S_{D}$ , $\overline{S_{I}}S_{D}$ , $S_{I}\overline{S_{D}}$ , and $\overline{S_{I}S_{D}}$ ). For example, the transition between $S_{I}S_{D}$ and $\overline{S_{I}}S_{D}$ can be considered as the result of two concurrent event: i) the transition between $S_{I}$ and $\overline{S_{I}}$ ; and ii) the transition between $S_{D}$ and $S_{D}$ . Thus we have:

$$
P \left(\overline {{{S _ {I}}}} S _ {D} \mid S _ {I} S _ {D}\right) = P \left(\overline {{{S _ {I}}}} \mid S _ {I}\right) \cdot P \left(S _ {D} \mid S _ {D}\right) = \left(1 - T h _ {I}\right) \cdot T h _ {D} \tag {9}
$$

Similarly, we can estimate the transition probabilities between $S_{I}S_{D}$ and States $S_{I}S_{D}$ , $S_{I}\overline{S_{D}}$ , $\overline{S_{I}S_{D}}$ as shown in Fig. 9.

# E. Put it together

Fig. 10 illustrates the key workflow of RED, which comprises a training phase and a eccentricity model (RUM).

Before RED start working, we have a short training phase. Through collecting the signals when the tag rotating with the machinery at original position for about 1 minute, we can get the original distribution of Int and Diff. These data are used in RUM not only as original probability, but also for estimating the distribution after eccentricity.

![](images/687694aa5547289ac2e8d63179037d9d28f108a43259ae343b823344be735cf4.jpg)



Fig. 10. The overview of RED

Then we can begin the process of eccentricity detection. First of all, the sampled raw signals from the tag are processed to extract the time interval between two peak RSSIs and the phase difference between their corresponding phases, i.e. Int and Diff. Then the data (Int, Diff) acts as a input of RUM. According to the above content, RUM is able to continuously track the variation of Int and Diff, and instantly estimate the probabilities that the eccentricity has occurred or not, based on the distributions of Int and Diff and how Int and Diff change. At last, by comparing $P_{Unecc}$ and $P_{ecc}$ , RED outputs the detection result.

# IV. EVALUATION

# A. Implementation

The devices we use are shown in Fig. 3. The RFID system operates at 920-926 MHz band. The tags adopt LLRP protocol [19] [20] to communicate with the reader. The mean sampling rate is 40 Hz [12]. To simulate the high speed rotating machinery, the centrifuge rotates at 10000 RPM.

# B. Methodology

We mainly use three metrics to evaluate the performance of RED: True Positive Rate (TPR), False Positive Rate (FPR), and Latency. TPR represents the percentage that RED correctly detects eccentricity. FPR represents the percentage that RED detects falsely when there is no eccentricity. Latency represents how long it takes for RED to detect the eccentricity.

We mainly adjust following settings:

- Precision $(\Delta d)$ . Precision represents the smallest shift we should detect. Every time we move the centrifuge by the same distance, and then evaluate the performance.   
- Initial distance (d). Initial distance means the distance between the tag and the antenna when we deploy RED.

\- Noise (n). We conduct experiments in noisy environments, and try to evaluate the effect of the noise processing module.

In the training phase, we collect data for 1 minute at the initial position. In the testing phase, we move the tag in two directions, approaching and deviating the antenna. At each position, we collect data for 5 seconds and repeat 10 times.

# C. Accuracy of RED

To evaluate accuracy of RED, we place the centrifuge 6 cm away from the antenna, and change $\Delta d$ from 1 to 7 mm. The results are shown in Fig. 11. The overall TPR is $93.59\%$ , while the FPR is $4.88\%$ .

For the approaching case, The overall TPR can reach 90.76%, while FPR is 9.76%. When $\Delta d$ is set to 1 mm, the average of TPR is 85.01% and the FPR is 16.14%. As $\Delta d$ decreases, the TPR rises and the FPR falls. That's because the difference between the RSSI and phase readings before and after eccentricity is more obvious when $\Delta d$ is larger. When the tag deviates from the antenna, the performance of RED is better than the approaching case. The reason is that there is less or even no E-point, which is easy to judge.

# D. Impact of different initial distance

We choose three different initial distances, while $\Delta d$ is 7 mm. The results are shown in Fig. 12. Whether the tag is approaching or deviating from the antenna, the results are similar. As d increases, the TPR decreases and the FPR increases. The reason is that the farther from the antenna, the signal strength is weaker, and the difference caused by same shift is smaller.

# E. Impact of observation number

The observation number of RED is a key metric. It not only affect the accuracy, but also is related to the latency of RED. The more samples we observe, the delay is longer. The impact of changing the observation number is shown in Fig. 13. As we observe more samples, the performance getting better in both cases. So there is a trade off between latency and accuracy. We will discuss about this in a later subsection.

# F. Impact of E-point Threshold

We conduct experiments to examine the impact of choosing E-points. Fig. 14 shows the result. We can see that when the threshold of E-point is higher, the TPR and the FPR are better. The reason is that the difference is more significant around the maximum. The farther from the maximum, the expected Diff is larger and the expected Int is smaller. The influence of eccentricity is less. So we choose 5% as the threshold of E-point.

# G. Detection Latency

Last but not least, we talk about latency, which is another important metric for RED. We set d at 6 cm, and adjust the precision and the observation number. Fig. 15(a) shows the distribution of latency over different observation numbers, while $\Delta d$ ranges from 1 to 7 mm. We can see that when the observation number is small, although the accuracy is low, the latency is low. It can reach 0.1615s when observation number is 1. The time cost of error judgment is less than the time interval of one more observation point. But low accuracy means more unnecessary downtime of the machinery. The economic loss brings by low accuracy is unacceptable. So we think observing 4 samples is proper.

![](images/74e076257250b3bf33628aeafa680290248aacdbe2f8521641d4feec56857a84.jpg)



(a) The result when the tag approaches the antenna

![](images/def593ba2cba2aa82423c8ce3b3bfd8946c04007c08d49147ba298915647bfd8.jpg)



(b) The result when the tag deviates from the antenna

![](images/43a6c8503dfa7c5b97a31d502d2c3c66bcb2b8be36c92fe1bd0583b7846b090b.jpg)



(a) The result when the tag approaches the antenna

![](images/fb19e87338b3516cad5e2b10efa873db0048c0e22c06fd9ac86a47491d047fe0.jpg)



(b) The result when the tag deviates from the antenna

Fig. 11. The average and variance of TPR and FPR with different precision Fig. 12. The TPR and FPR over different initial distances when $\Delta d = 7mm$ when $d = 6cm$   
![](images/65a9c069c74b22721a003dbbf8d9f4bc838f111a073a40aa393790d33f6dec3a.jpg)



(a) The result when the tag approaches the antenna

![](images/7947aafa56708a7c71d4b42db52e9eb366683a5ed39a2d2c59d39e7bb81576f2.jpg)



(b) The result when the tag deviates from the antenna

![](images/86c37d11db628e05230661f85bb271e089f3005f62b33395e32c6b8ab99ab378.jpg)



(a) The result when the tag approaches the antenna

![](images/e8c2f35d70cd1aded041b0e3c378f9936db85eaea664050921cf1068990a90d1.jpg)



(b) The result when the tag deviates from the antenna   
Fig. 14. The overall TPR and FPR over different thresholds of E-point

Fig. 13. The average and variance of TPR and FPR over different observation numbers when d = 6cm, $\Delta d = 7mm$   
![](images/417c3cf659cc6c449070f61eb4621cd720a5997bf29ea48b8b4c024a70c25855.jpg)



(a) The result when $\Delta d$ ranging from 1 to 7 mm

![](images/9d67e6e216e129778eb0052d5c54cbbda45b9ed10734089da634cea8f92b663b.jpg)



(b) The result when the tag approaches the antenna   
Fig. 15. The latency when $d = 6cm$

The distance between the tag and antenna also affects the latency. As Fig. 15(b) shows, as the tag approaches the antenna, the latency decreases. The reason is that the number of E-points reduces, so the expected Int increases.

# V. RELATED WORKS

In this section, we briefly review the related works, by classifying them into two main categories.

Eccentricity detection of rotating machinery. Different methods have been developed for rotating machinery's eccentricity detection. Various fault symptoms are used in the detection method, including vibration signals [3], thermal features [4], acoustic signals [5], oil debris [6], and so on. These symptoms can reflect the state of machinery, but they have their own limitations. To measure vibration signals and thermal signals, special sensors should be embedded into the machinery. That means we must deploy them at the beginning, or stop the machinery and deploy them, which is inconvenient. Measuring acoustic signals and oil debris are via the non-intrusive method. However, it requires a complete system to measure oil debris, which is complex and expensive. Acoustic signals should be measured in a quiet environment. RFID-based system is non-intrusive and low-cost. It's easy to deploy in various environment.

RFID-based sensing. RFID-based sensing has been developed for several years. The researches are aimed at measuring different physical properties, and the common ground of them is to find how these properties affect the RSSI signal, then extract information from the received signals. Bhattacharyya et. al [21] leverage RFID infrastructures design an wireless temperature sensor. They use the changes in tag power characteristics to determine whether the temperature is above threshold. Manzari et. al [11] explore the possibility to integrate chemical species into an RFID tag, and then improve the sensing ability of tag. Tagbeat [12] quantifies the change in phase corresponding to the track of rotation. By recovering the periodic changes in phase, it can measure the vibration period of the device. RIO [14] is based on the impedance changing when a human finger touches a tag. The impedance change influence the phase readings, which makes RFID-based touch sensing possible. Twins [13] leverages the interference among passive tags to do motion detection and achieve high precision.

Regarding the rotation of tags and the resulting tag readings, a tag's orientation is also an interesting factor to study. RF-Compass [7] navigates the robot by using the RFID signals to partition the space based on the robot's consecutive moves. Griffin et al. [17] quantify the basic relationship between multiple factors and the RSSI value, including the polarization factor. Tagyro [8] is an 3D orientation tracking system. They find that polarization leads to the inaccurate readings, so they design a series of recovery algorithm to make the measurement reliable. PolarDraw [9] also observes the phenomenon of polarization. They leverage the relationship between the RSSI readings and the angle of the tag, and determine the rotation angle and displacement of the tag. They can track the handwriting on the board.

As our understanding of the signals deepens, the phenomenon like polarization gives us more opportunities to acquire rich information. The researches above can all provide a high precision result in the case of stationary tags or tags moving at a low speed. In our scenario, however, the tag is rotating at a high speed and the readings are highly dynamic and discrete. Our goal is to offer further insight into the signal change regularities in the high-speed rotation scenario, and leverage them to achieve high precision and low latency detection.

# VI. CONCLUSION

RFID-based sensing, namely to sense physical phenomenon according to the RFID signals, is deemed as a promising technique in the area of cyber-physical systems. In this paper, we advance the state of the arts, by tackling the problem of RFID-based eccentricity detection for high-speed rotating machinery. This problem has great significance in industry, while producing non-trivial challenges in applying RFID-based sensing techniques. Our proposal called RED, utilizes the temporal and phase distributions of tag readings as effective features for eccentricity detection. Implementation of RED offers a non-intrusive, low-cost, and real-time solution, which is applicable to all kinds of rotating machinery. In the future, we plan to further improve the accuracy and the timeliness of eccentricity detection. Potential solutions include to use a combination of multiple tags and to deploy the tags at different positions on the rotor. The Doppler effect induced by the rotation is also an interesting issue, when we try to refine the precision of detection.

# ACKNOWLEDGEMENTS

This work was supported by National Key R&D Program of China 2017YFB1003000, National Natural Science Fund of China for Excellent Young Scientist No.61422207, The NSFC No. 61772306 and No.61672320, NSF China Key Project 61432015 and 61632008, and China Postdoctoral Science Foundation No. 2016M601034.

# REFERENCES

[1] Y. Lei, Z. He, and Y. Zi, “Application of an intelligent classification method to mechanical fault diagnosis,” Expert Systems with Applications, vol. 36, no. 6, pp. 9941–9948, 2009.   
[2] T. Loutas, D. Roulias, E. Pauly, and V. Kostopoulos, “The combined use of vibration, acoustic emission and oil debris on-line monitoring towards a more effective condition monitoring of rotating machinery,” Mechanical systems and signal processing, vol. 25, no. 4, pp. 1339–1352, 2011.   
[3] C. Li, R.-V. Sánchez, G. Zurita, M. Cerrada, and D. Cabrera, “Fault diagnosis for rotating machinery using vibration measurement deep statistical feature learning,” Sensors, vol. 16, no. 6, pp. 895–913, 2016.   
[4] W.-K. Wong, C.-K. Loo, W.-S. Lim, and P.-N. Tan, “Thermal condition monitoring system using log-polar mapping, quaternion correlation and max-product fuzzy neural network classification,” Neurocomputing, vol. 74, no. 1, pp. 164–177, 2010.   
[5] V. Arumugam, A. A. P. Sidharth, and C. Santulli, “Failure modes characterization of impacted carbon fibre reinforced plastics laminates under compression loading using acoustic emission,” Journal of Composite Materials, vol. 48, no. 28, pp. 3457–3468, 2014.   
[6] C. Li, J. Peng, and M. Liang, “Enhancement of the wear particle monitoring capability of oil debris sensors using a maximal overlap discrete wavelet transform with optimal decomposition depth,” Sensors, vol. 14, no. 4, pp. 6207–6228, 2014.   
[7] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “Rf-compass: Robot object manipulation using rfids,” in Proceedings of ACM Mobi-Com, 2013.   
[8] T. Wei and X. Zhang, “Gyro in the air: tracking 3d orientation of batteryless internet-of-things,” in Proceedings of ACM MobiCom, 2016.   
[9] L. Shangguan and K. Jamieson, “Leveraging Electromagnetic Polarization in a Two-Antenna Whiteboard in the Air,” in Proceedings of ACM CoNEXT, 2016.   
[10] J. Liu, M. Chen, S. Chen, Q. Pan, and L. Chen, “Tag-compass: Determining the spatial direction of an object with small dimensions,” in Proceedings of IEEE INFOCOM, 2017.   
[11] S. Manzari, C. Occhiuzzi, S. Nawale, A. Catini, C. Di Natale, and G. Marrocco, “Polymer-doped uhf rfid tag for wireless-sensing of humidity,” in Proceedings of IEEE RFID, 2012.   
[12] L. Yang, Y. Li, Q. Lin, X.-Y. Li, and Y. Liu, “Making sense of mechanical vibration period with sub-millisecond accuracy using backscatter signals,” in Proceedings of ACM MobiCom, 2016.   
[13] J. Han, C. Qian, X. Wang, D. Ma, J. Zhao, W. Xi, Z. Jiang, and Z. Wang, "Twins: Device-free object tracking using passive tags," IEEE/ACM Transactions on Networking (TON), vol. 24, no. 3, pp. 1605–1617, 2016.   
[14] S. Pradhan, E. Chai, K. Sundaresan, L. Qiu, M. A. Khojastepour, and S. Rangarajan, “Rio: A pervasive rfid-based touch gesture interface,” in Proceedings of ACM MobiCom, 2017.   
[15] Impinj Speedway Revolution Reader Application Note, “Low level user data support,” Impinj, Seattle, Washington, USA, 2013.   
[16] Alien Technology, “Alien 'G' Inlay,” http://www.alientechnology.com.   
[17] J. D. Griffin and G. D. Durgin, “Complete link budgets for backscatter-radio and rfid systems,” IEEE Antennas and Propagation Magazine, vol. 51, no. 2, 2009.   
[18] H. T. Friis, “A note on a simple transmission formula,” Proceedings of the IRE, vol. 34, no. 5, pp. 254–256, 1946.   
[19] “LLRP toolkit,” http://www.llrp.org.   
[20] J. Han, C. Qian, P. Yang, D. Ma, Z. Jiang, W. Xi, and J. Zhao, "Geneprint: Generic and accurate physical-layer identification for uhfrfid tags," IEEE/ACM Transactions on Networking (TON), vol. 24, no. 2, pp. 846–858, 2016.   
[21] R. Bhattacharyya, C. Floerkemeier, S. Sarma, and D. Deavours, “Rfid tag antenna based temperature sensing in the frequency domain,” in Proceedings of IEEE RFID, 2011.