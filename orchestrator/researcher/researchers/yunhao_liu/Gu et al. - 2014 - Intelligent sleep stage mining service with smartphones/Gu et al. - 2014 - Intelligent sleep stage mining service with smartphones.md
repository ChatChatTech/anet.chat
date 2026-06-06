# Intelligent Sleep Stage Mining Service with Smartphones

Weixi Gu $^{\dagger}$ , Zheng Yang $^{\dagger}$ , Longfei Shangguan $^{\ddagger}$ , Wei Sun $^{\ddagger}$ , Kun Jin $^{\dagger}$ , Yunhao Liu $^{\dagger}$ $^{\dagger}$ School of Software and TNList, Tsinghua University, China

{guweixigavin, evilying2016}@gmail.com, {yang, yunhao}@greenorbs.com

$^{\ddagger}$ CSE, Hong Kong University of Science and Technology, Hong Kong

longfei@greenorbs.com, wsunaa@cse.ust.hk

# ABSTRACT

Sleep quality plays a significant role in personal health. A great deal of effort has been paid to design sleep quality monitoring systems, providing services ranging from bedtime monitoring to sleep activity detection. However, as sleep quality is closely related to the distribution of sleep duration over different sleep stages, neither the bedtime nor the intensity of sleep activities is able to reflect sleep quality precisely. To this end, we present Sleep Hunter, a mobile service that provides a fine-grained detection of sleep stage transition for sleep quality monitoring and intelligent wake-up call. The rationale is that each sleep stage is accompanied by specific yet distinguishable body movements and acoustic signals. Leveraging the built-in sensors on smartphones, Sleep Hunter integrates these physical activities with sleep environment, inherent temporal relation and personal factors by a statistical model for a fine-grained sleep stage detection. Based on the duration of each sleep stage, Sleep Hunter further provides sleep quality report and smart call service for users. Experimental results from over 30 sets of nocturnal sleep data show that our system is superior to existing actigraphy-based sleep quality monitoring systems, and achieves satisfying detection accuracy compared with dedicated polysomnography-based devices.

# Author Keywords

Smartphones; sleep stage; sensors.

# ACM Classification Keywords

H.5.m. Information Interfaces and Presentation (e.g. HCI): Miscellaneous

# INTRODUCTION

Sleep, occupying nearly one-third of human lifetime, is a necessary and vital biological function. Physiological communities often regard sleep as a cyclical process composed of three stages: rapid eye movement (REM) stage, light sleep stage and deep sleep stage [23]. The biological characteristics of different sleep stages exhibit distinguishingly. REM is an active period of sleep marked by intense brain activities and dream occurrence. Light sleep stage is a period of relaxation, when the heartbeat, breathing rate and muscle activity slow down. Deep sleep stage triggers hormones to promote body growth, as well as the repair and restoration of energy. Sleep quality is actually determined by

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Permissions@acm.org.

UbiComp '14, September 13 - 17, 2014, Seattle, WA, USA

Copyright 2014 ACM 978-1-4503-2968-2/14/09...\$15.00.

http://dx.doi.org/10.1145/2632048.2632084

the distribution of different sleep stages rather than the time of sleep [7]. Even though people experience a full night's sleep, they may still feel fatigued after being woken up. A longer deep sleep period contributes to a better sleep. Moreover, a proper wake-up time is also helpful for mental and physical health [38]. Comparing with other sleep stages, people woken up in light sleep stage feel more refreshed generally.

Sleep quality monitoring requires a careful observation of individuals' sleep stages. The approaches to recording sleep stages are divided into two categories. The first category is based on polysomnography [32]. The methods in this category leverage electroencephalograph (EEG) to observe brain waves and then recognize sleep stages accurately. EEG systems, e.g., Zeo [41], however, are usually limited to medical and physiological studies. High cost and complicated operations make them hard to be accepted by the public. The approaches in the second category are based on actigraphy [1] utilizing some certain physical activities such as body movement or snore to predict sleep stage. The detection performance based on these approaches, e.g., Jawbone up [16] and Sleep As Android [37], has not yet been evaluated against medically accepted methods. In this paper, we show their performance to be substantially lesser than the methods used in physiological studies.

In this paper, we present Sleep Hunter, a sleep stage detection system based on actigraphy that predicts sleep stage transitions by smartphone. The information collected by Sleep Hunter can be used to evaluate human sleep quality and provide smart call service, which wakes up users in light sleep stage intelligently. The principle behind our system is that apart from implicit brain wave changes, individuals usually exhibit distinguishable physical activities during different sleep stages. For example, in REM, breathing rate is commonly unstable and people tend to exhibit large body movements. Whereas in the deep sleep stage, breathing rate becomes slower and more regular, accompanied with slight body movements such as arm trembling and leg jerking [39]. Moreover, sleep environment, sleep duration and some certain personal factors also impact the transition of sleep stages. Sleep Hunter leverages built-in sensors of the smartphone to detect such sleep-related events and then predicts the transition of sleep stages overnight. Based on the detected sleep stages, it generates a corresponding score for sleep quality evaluation and provides smart call service. Compared with the methods in the first category, Sleep Hunter is a service that runs on a commercial off-the-shelf smartphone which requires no additional device. The simple operation makes it more convenient than polysomnography-based systems. Furthermore, Sleep Hunter integrates sleep-related events comprehensively and leverages a statistical model to predict sleep stage. The fine-grained detection results and promising performance make Sleep Hunter more suitable than those actigraphy-based products in the second category.

<table><tr><td>Activity</td><td>Explanation</td></tr><tr><td>Tachypneic breath</td><td>A condition of rapid breathing, commonly between 12-20 breaths per minute.</td></tr><tr><td>Apneustic breath</td><td>A series of slow, deep breathing, lasting about 6-10 seconds, after which the air is suddenly expelled by the elastic recoil of the lung.</td></tr><tr><td>Cough</td><td>A sudden and often repetitively occurring reflex which helps to clear the large breathing passages from secretions, irritants.</td></tr><tr><td>Snore</td><td>A vibration of respiratory structures and a resulting sound, due to obstructed air movement during breathing while sleeping.</td></tr><tr><td>Somniloquy</td><td>A parasomnia that refers to talking aloud while asleep. It can be quite loud, ranging from simple sounds to long speeches, and can occur many times during sleep.</td></tr><tr><td>Macro body movement</td><td>A serials of significant activities happened in sleep cycles, such as turning body over, driving or raising legs and so on.</td></tr><tr><td>Micro body movement</td><td>A serials of tiny activities appeared in sleep cycles, including short convulsion and hand trembling, head moving.</td></tr></table>

Table 1. The physical activities happened in sleep process

We face two challenges when codifying such idea into a practical system. The first challenge is how to identify discriminative activities from a variety of primitive data, given the condition that sensory data are sparse and full of noise. For example, audio signals recorded by the microphone contain not only sleep-related primitives, but also ambient noise. The second challenge is how to leverage sleep-related events to figure out features for capturing sleep stage transitions. Many events such as snore, body movement, sleep duration and even people's age have close relationships with sleep. The influence of these factors should be reasonably utilized.

To address the above challenges, we design a unique feature-extraction mechanism for each of sleep-related events based on their physical characteristics. Moreover, we exploit conditional random field (CRF), a statistical model to parse the relations behind these events according to our over 90 sets of nocturnal sleep data, and evaluate them on our testing dataset.

The contributions of our paper are listed as follows. 1) We put forward a set of efficient algorithms to detect sleep-related events and adopt a CRF to depict the relationship between such events and sleep stages. 2) We implement Sleep Hunter on Android platform and conduct evaluation experiments on 15 participants from various age groups. The result of the testing data over one month demonstrates that the detection accuracy of Sleep Hunter attains $64.55\%$ , which is superior to the existing actigraphy-based applications to our best knowledge. 3) We conduct extensive case studies and show that Sleep Hunter is able to provide sleep quality reports and smart call services for users.

# SYSTEM OVERVIEW

In this section, we present the key insight in our sleep stage detection scheme first. Then, we specify the design targets of our system. Finally, we describe the system architecture of Sleep Hunter.

# Key Insight

Our key insight here is related to the following aspects. Firstly, apart from the implicit physiological activities (e.g.,

![](images/fddf6076246495c9f07500987e80b0f6cc609d83b5c92e5c5d0156a7bde51dad.jpg)



Figure 1. An illustration of sleep stage transition

body temperature changes and brain activity variations), sleepers usually exhibit distinguishable physical activities in different sleep stages [2]. For example, short breaths and large body movements such as body rollovers usually happen in light sleep, resulting from the fast heartbeat. On the contrary, slight body movements such as arm trembling and leg jerking [18] mostly occur in deep sleep due to the slow and regular breathing rate. Moreover, somniloquy and body trembles caused by frequent dreams generally appear in REM. Such physical activities can be detected via off-the-shelf smartphones, serving as the basis for the sleep stage analysis. Table 1 summarizes the physical activities that Sleep Hunter mainly monitors during the sleep process.

Secondly, sleep usually follows a predictable pattern, moving cyclically among light sleep stage, deep sleep stage and REM. Each sleep cycle typically lasts for about 90 minutes and repeats four to six times over a night. In each sleep cycle, sleepers firstly experience a transition from light sleep to deep sleep and then enter REM. This sequence is shown by solid black lines in Fig. 1. Nevertheless, sleep cycle is not an absolute case. The phenomenon of skipping some certain sleep stages usually occurs during sleep. For example, as shown by the grey dashed lines in Fig. 1, sleep stage could jump to REM from light sleep or return to deep sleep from REM directly. The dependence between two successive sleep stages, however, still exists. This inherent temporal sequence, intuitively, could also be utilized for analyzing sleep stages. Moreover, sleep environment, e.g., ambient illumination, and certain personal factors, e.g., age, also impact the sleep phases [18], which help us to predict the transition of sleep stages.

![](images/b4be0cdc4e3fed04a2589c8a9426b6d6a956a9bcc6611e75b16994faf342057f.jpg)



Figure 2. The architecture of Sleep Hunter

![](images/57217df078b23c9f858cb5975493ec24f051d99456ada858a89af0e18f293230.jpg)



Figure 3. Acceleration trace of body movement

![](images/54cc62df586cf49ce44d44a89452f38ddfb6711dd149d0526a32ee715206327c.jpg)



![](images/bd57e42a6988bc074f5d8f7d7c4a262d1480daf32396631a8b2e7982acab2b7f.jpg)



Figure 4. Durations of body movements

# Design Target

The design target of Sleep Hunter is twofold. 1) Sleep Hunter needs to detect the sleep stages of users within an allowed latency for the requirement of the smart call service, as well as for the fine-grained sleep stage record. This record can further help to analyze the sleep quality of users, which reflects their mental and physical health conditions. 2) As a long-term running mobile application, the CPU share of Sleep Hunter should be small enough to support the service for the whole sleep process. This is a basic requirement and is widely accepted by mobile applications [14, 37, 40].

# System Architecture

Sleep Hunter is a two-layer system and provides an interface for its applications as shown in Fig. 2. The first layer is composed of five submodules: body movement detection module, acoustic event detection module, illumination condition detection module, sleep duration tracking module and personal factor collection module. Each module is responsible for collecting its related primitive data and extracting associated features. The second layer leverages CRF to integrate features from the upper layer. Based on these collected features, this layer makes sleep stage prediction for the corresponding period, which is called detection phase. The duration of detection phase is set to be 5 minutes. In other words, Sleep Hunter detects sleep stage every 5 minutes during sleep. Moreover, Sleep Hunter provides sleep quality report and smart call service for users in the interface layer based on the monitoring results of sleep stages.

# SYSTEM DESIGN

In this section, we specify the design and implementation details for each component in Sleep Hunter.

# Body Movement Detection (BM)

Sleepers usually exhibit various physical activities during different sleep stages. As reported by medical views $[2]$ , large body movements like body rollovers usually occur when people are in light sleep, which result from the fast heartbeat during this stage. In contrast, some tiny body movements such as body trembling and leg jerking usually occur in deep sleep stage. Moreover, some unconscious body movements such as the leg stretching and the arm rising would happen during REM, which are caused by frequent dreams. Accordingly, we could leverage the distinguishable movements to detect various sleep stages.

# Body Movement Experiments

In order to better understand the phenomenon of body movements during sleep, 100 groups of sleep-related body movement experiments are conducted by 10 volunteers across different ages when they are in bed. Every volunteer contributes 10 groups of experiments. In each experiment, the volunteer puts a smartphone beside his/her head and enables the accelerometer to calculate the corresponding acceleration variance trace of the body movement. The sample rate of accelerometer is set to be 100Hz, which is same as the configuration of Sleep Hunter. Acceleration variance is calculated as $V(i) = a(i) - a(i - 1)$ , where $a(i) = \sqrt{a_x(i)^2 + a_y(i)^2 + a_z(i)^2}$ and $a_x(i)$ , $a_y(i)$ and $a_z(i)$ represent the accelerometer sample value of X-axis, Y-axis and Z-axis at time stamp i respectively. The sleep-related body movements include body rollover, leg stretching, arm raising, figure trembling, leg jerking and head movement. Fig. 3 plots a real acceleration variance trace of one volunteer's body movements.

# Body Movement Extraction

Considering the distribution of inherent accelerometer's noise, we denote the threshold by $\xi$ to classify the accelerations of body movement and noise. If $|V(i)| \geq \xi$ , we regard it as an occurrence of body movement. Otherwise, we take it as noise. However, if $\xi$ is set too large, some tiny body movements are likely to be ignored. Conversely, if $\xi$ is too small, some acceleration noises may be mistaken as body movements. Either case would make negative influence on the detection performance of body movement. In order to find an effective threshold, we vary $\xi$ from 0.01 to 1 and eventually set $\xi$ to be 0.05, which achieves the best detection performance based on our body movement experiments. However, one issue of this mechanism is that body movements such as body rollover and leg stretching are not continuous. The temporal pauses in body movements would cause our mechanism mistakenly to split a single body movement into multiple movements. To solve this problem, we realize the longest temporal pause in our body movement experiments belongs to the body rollover, which lasts less than 1.5s. Sleep Hunter empirically merges two successive movements into a single one if they occur within 1.5s.

# Body Movement Classification

For a better analysis of the relationship between sleep-related body movements and sleep stages, we calculate the durations of those large, long-lasting actions such as body rollover, leg stretching and arm raising, and tiny, short-lasting activities including arm trembling and leg jerking from our body movement experiments. Fig. 4 shows the distribution of body movement's durations in two sets. We found that all of the large, long-lasting body movements last at least 2.8s while those tiny, short-lasting activities last at most 0.85s. This obvious temporal gap helps us to distinguish these movements into two categories. In Sleep Hunter, we define the movements lasting less than 1s as micro body movements and those lasting longer as macro body movements, and leverage these two kinds of body movements as sleep-related features.

# Acoustic Event Detection (AE)

![](images/b7b2d15196ec13d8f550ee3144d4ef3bcdca930a64b79d94e62e23757ab39b42.jpg)



Figure 5. Correlation matrix between features and acoustic events

Apart from body movements, people usually display some acoustic events during sleep. We concentrate on five common sleep-related acoustic events: somniloquy, tachypneic breath, apneustic breath, snore and cough. Based on the physiological research [2], somniloquy occurs frequently during REM because of continual dreams. Tachypnea, which is easily incurred by the rapid heartbeat, usually happens during light sleep. Moreover, apneusis often appears in deep sleep due to the slow heartbeat, and snore usually emerges in deep or light sleep. Furthermore, cough is not likely to come about during deep sleep, since it can easily disturb the sleep process.

# Acoustic Event Experiments

We utilize the built-in microphone, whose sample rate is set to be 16KHz, to record acoustic data. A total of 30 participants join our acoustic experiments and their smartphones are placed beside their heads during sleep. According to these recording data, we label acoustic events manually and thus collect 180 sound clips for each type of acoustic event from the 30 people, with each sound clip lasting around 5 seconds. The collected data, therefore, are sufficient for us to study the inner properties of these sleep-related acoustic events.

The acoustic analysis begins with dividing the audio stream from the microphone into frames of equal duration. Each frame is composed of 1024 acoustic samples, and thus its duration is 64ms, which is able to capture the acoustic characteristics of sounds [27].

# Noise elimination

Since different kinds of noise exist in the sleep environment, the negligible effect of noise should be eliminated firstly. According to our observation, there are mainly three types of noises during sleep: ambient noise, noise made by body movement and traffic noise. Sleep Hunter leverages the scheme in $[27]$ to differentiate the ambient noise from other types of noise and sleep-related acoustic events. The scheme recognizes ambient noise by its low root-mean-square (RMS) energy and high spectral entropy [25]. If RMS of the current frame is less than a predefined threshold $Th_{rms}$ and its entropy is higher than $Th_{entropy}$ , it is ambient noise. Here, we empirically set $Th_{rms} = 0.006$ and $Th_{entropy} = 25$ , which locally optimizes the detection accuracy on our acoustic event experiments. Moreover, body movements such as body rollovers during sleep would make additional noise. Since they generally induce variances of acceleration and sound simultaneously, we preset threshold $\epsilon$ to measure this simultaneity and leverage it to detect the noise made by body movement. In other words, if the temporal deviation between the beginnings of an acoustic event and a body movement is less than $\epsilon$ , and the temporal deviation between their endings is also less than $\epsilon$ , we regard the acoustic event as noise made by body movement and then filter it out. In Sleep Hunter, we set $\epsilon = 0.5s$ based on our experiments. As the acoustic characteristics of traffic noise are complicated, we classify it with sleep-related acoustic events together.

![](images/3a5240386403400a11776ebe5ca69a451159052b598b2dff036b18a706a433bf.jpg)



Figure 6. The performance of acoustic event classification

# Acoustic Feature Selection

In this section, we extract features of sleep-related acoustic events and traffic noise. Several most representative features for acoustic event classification are chosen. These features are also widely adopted by various works $[27, 14, 33]$ .

The features are divided into two categories as follows.

# 1) Time-domain feature:

1. Zero Crossing Rate (ZCR): $\frac{1}{2}\sum_{j = 1}^{m}|sign(s_j) -$

$sign(s_{j-1})|$ , where $s_{j}$ stands for the jth sample in a frame who has m samples. Zero Crossing Rate [20] is an indicator to represent the rate where the sample value changes from positive to negative or back in time domain.

# 2) Frequency-domain feature :

To better extract frequency-domain features, we firstly calculate the frequency spectrum of each frame by N-point Fast Fourier Transform(FFT), where N equals 1024. We then normalize the spectrum of each frame and let $f_{t}(j)$ be the normalized magnitude of the jth frequency bin in the spectrum of frame $f_{t}$ . We compute the following spectral features for acoustic event classification.

1. Spectral Entropy: $-\sum_{j=1}^{N} f_t(j) \log f_t(j)$ . Spectral Entropy [34] has been widely used to evaluate the flatness of the acoustic spectrum shape.

2. Spectral Centroid: $\sum_{j=1}^{N} j \cdot |f_t(j)|^2 / \sum_{j=1}^{N} |f_t(j)|^2$ . Spectral Centroid [25] aims to calculate the balancing point of the power spectral distribution.

![](images/c84470dabe0f904ef6bed9c4767267cf5ed89a1351ad9532ac57ebfe453ed287.jpg)



Figure 7. Illumination intensity under different conditions

3. Spectral Flux: $-\sum_{j=1}^{N}(f_t(j) - f_{t-1}(j))^2$ . Spectral Flux   
[25] reflects the stability of acoustic events. $f_{t}(j)$ and $f_{t-1}(j)$ stand for the jth frequency bin in the current frame and the last frame respectively.

4. Bandwidth: $\sum_{j=1}^{N}(j - Cen)^{2} \cdot |f_{t}(j)|^{2} / \sum_{j=1}^{N}|f_{t}(j)|^{2}$ , where $Cen$ indicates the spectral centroid of $f_{t}$ . Bandwidth [25] describes the continuous frequency range beyond zero from lower to upper ends.

5. Spectral Rolloff: $\max(h| \sum_{j=1}^{h} f_t(j) < \text{threshold})$ .

Spectral Rolloff [25] indicates the percentage frequency bin below a predefined threshold, which is usually set to be 93%. It reflects the skewness of the spectral distribution.

Fig. 5 illustrates the correlation matrix between the aforementioned acoustic features and the frames of different acoustic events collected by our experiments. Each row/column represents a feature. The curve in the boxes on the diagonal line stands for the distribution of the corresponding feature. We can learn that the flux of somniloquy lies in a relatively low level, which demonstrates that its frequency spectrum is stable. On the contrary, the flux of traffic is generally higher than those of others, which is coherent with our intuition that the frequency spectrum of traffic is abrupt. Moreover, the apneustic breath, whose rolloff is large, possesses a high frequency. Furthermore, we can see that most tachypneic breaths locate where entropy and bandwidth are both low. It shows a fact that the sound of this type of breath possesses an obvious pattern and its frequency spectrum is narrow. Since different acoustic events perform distinguishing distributions under various features, we can leverage such features to classify them.

# Acoustic Event Classification

As acoustic features depicted in Fig. 5 are not likely to be classified by a simple linear function, we expect to use a nonlinear classifier to analyze these features and make further classification. Here, we adopt support vector machine (SVM) [5] to express this kind of nonlinear regression. The 10-fold cross-validation [21] has been done on the collected frames of acoustic event across the 30 participants and the classification performance is illustrated in Fig. 6. We can observe that the best classification performance is achieved by traffic. Its average precision and recall reach $98.3\%$ and $96.9\%$ respectively. The average F1 [13] is up to $97.6\%$ . Even though the worst result belongs to cough, its average precision and recall are still over $66\%$ , and average F1 runs up to $67.13\%$ . Moreover, for other four types of acoustic events (i.e., somniloquy, apneustic breath, tachypneic breath and snore), average F1 values of them are from 70% to 88%, which demonstrates the classification performance is acceptable. Furthermore, the standard deviations of all the indices illustrated by the error bars are less than 6%, which shows that the classification performance of SVM is stable and robust. Therefore, we could filter out the traffic noise and recognize the sleep-related acoustic events, and then leverage them as features to predict sleep stages.

# Illumination Condition Detection (IC)

Generally, sleep quality is also affected by the ambient illumination conditions [18]. People may enjoy a good sleep in dim environment while feel difficult to fall asleep under strong illuminative conditions. To characterize the relationship between sleep stages and illumination intensity around, we categorize the illumination intensities into different conditions, and then explore the transition of sleep stages under these conditions. Fig. 7 illustrates the illumination intensity under different sleep environments, which is broadly categorized into three conditions: bedroom without light (Weak illumination condition, $\leq 10Lux$ ( $\beta_1$ )); bedroom with dim light (Moderate illumination condition, $10 \sim 2000Lux$ ( $\beta_2$ )); bedroom with strong lights (Strong illumination condition, $\geq 2000Lux$ ). Therefore, we could measure the sleep environment according to the three illumination conditions by the built-in light sensor of smartphones. The sample rate of the light sensor is set to be $100\mathrm{Hz}$ , which is the same as the configuration of Sleep Hunter. The three types of illumination conditions are also leveraged as sleep-related features for sleep stage detection.

According to our survey, for most smartphones, the light sensor is usually installed in the front face of the phone. As a result, if the phone is facing toward the ground, the illumination sensing module could be paralyzed because the illumination samples cannot reflect the real illumination conditions around the phone. Indeed, this phenomenon occurs frequently during sleep given that some unconscious body movements would occasionally change the position of smartphones.

To overcome this challenge, we build a light-weight hierarchical illumination intensity sensing scheme. Firstly, Sleep Hunter employs the proximity sensor to detect whether the light sensor is blocked or not. If it is not blocked, Sleep Hunter calculates the average illumination intensity $l_{cur}$ in the detection phase, and then determines the current illumination condition by comparing $l_{cur}$ with the two preset thresholds: $\beta_{1},\beta_{2}$ . On the other hand, if the light sensor is blocked, then Sleep Hunter locates the latest record of the illumination condition when the light sensor is not blocked, and treats it as the current illumination condition until the light sensor recovers.

# Sleep Duration (SD) and Personal Factor (PF)

Apart from those associated physical activities and sleep environment, the transition of sleep stage is affected by chronological rules statistically during the sleep process. According to the clinical study in [18], the first REM sleep stage usually occurs about 70 to 90 minutes after we fall asleep. A complete sleep cycle takes 90 to 110 minutes on average. Moreover, the first sleep cycle each night contains the relatively short REM phase and the relatively long period of deep sleep. As time goes by, the duration of REM increases while that of deep sleep decreases. By morning, people spend nearly all their sleep time in light sleep and REM. According to this chronological property, Sleep Hunter takes its running time as sleep duration and regards it as a sleep-related feature. Moreover, the sleep stage is also affected by the personal physiological status. For example, the proportion of deep sleep stage decreases with the increase of the user's age [26]. Since the age of sleeper is an important physiological factor impacting sleep [29, 8], Sleep Hunter obtains the user's age from the registration information and further takes it with the sleep duration as features for the sleep stage detection.

![](images/5ef1f4c2e31979d6f756ba9adc53cb2950bf29509f029e883f9cbae280374044.jpg)



Figure 8. Conditional random field

# SLEEP STAGE DETECTION

In this section, we present the details of the sleep stage detection scheme.

We propose a linear-chain conditional random field (CRF) [22] to integrate the aforementioned features and make further inference. CRFs are discriminative models that predict the global probability of a sequence of random variables. The probability structure of a CRF depends on a log-linear combination of observable features and dependence of hidden variables, which is depicted as a bipartite factor graph. CRFs have been widely used in audio, speech, language processing and health sensing [12, 24]. The rationale of CRF applied here lies twofold. Firstly, as depicted in Fig. 1, the occurrence of sleep stages during sleep forms a sequence. This process can be characterized by the CRF model. Secondly, sleep-related events have dependent relationships. For example, cough or snore often leads to transient asphyxia, which decreases the oxygen capacities, and in turn, results in body movements during sleep. CRFs, compared with HMMs, are better suited for sequences that have long interdependencies and therefore may have better performance in our applications.

# Building up the Detection Model

Fig. 8 gives the structure of CRF model we used. The shaded nodes $(Y_{1},\dots,Y_{t - 1},Y_{t})$ indicate the hidden sleep stage variables during sleep. $Y_{t}\in$ {light sleep, deep sleep, REM} is an output of CRF model, which represents the sleep stage in the detection phase $t$ . The unshaded node $\overrightarrow{X} = \{X_1,\dots,X_{t - 1},X_t\}$ denotes the observable sleep-related features occurred in the sleep process. $X_{t} = \{N_{B}(t),N_{A}(t),N_{I}(t),N_{D}(t),N_{P}\}$ represents the feature vector at detection phase $t$ . The explanation of each item, which is the input of model, is listed as follows. $N_B(t)$ : the number of occurrences of micro body movement and macro body movement during the detection phase $t$ . $N_{A}(t)$ : the number of occurrences of sleep-related acoustic events during the detection phase $t$ . $N_I(t)$ : the illumination condition during the detection phase $t$ . $N_D(t)$ : sleep duration. $N_P$ : age of user.

The factor $\psi_t(Y_{t-1}, Y_t, \vec{X}, t)$ of CRF shown as black boxes in Fig. 8, returns a positive real valued number that represents the compatibility of the observable feature vector $\vec{X}$ to the current hidden sleep stage $Y_{t}$ , and the dependence between $Y_{t-1}$ and $Y_{t}$ . The standard log-linear form of the factor is listed as Equation 1,

<table><tr><td></td><td>OS Platform</td><td>RAM</td><td>CPU</td><td>Battery</td></tr><tr><td>Galaxy S4</td><td>Android OS 4.2.2</td><td>2GB</td><td>quad-core 1.638 GHz</td><td>2600mAh</td></tr><tr><td>Samsung Note2</td><td>Android OS 4.1</td><td>2GB</td><td>quad-core 1.638 GHz</td><td>3100mAh</td></tr><tr><td>HTC G14</td><td>Android OS 2.3</td><td>2GB</td><td>dual-core 1.228 GHz</td><td>1520mAh</td></tr><tr><td>MIUI 2SC</td><td>Android OS 2.3</td><td>2GB</td><td>quad-core 1.700 GHz</td><td>2000mAh</td></tr></table>

Table 2. Information of experimental smartphones

$$
\psi_ {t} (Y _ {t - 1}, Y _ {t}, \overrightarrow {X}, t) = e x p \left(\sum_ {i = 1} ^ {m} \lambda_ {i} f _ {i} (Y _ {t - 1}, Y _ {t}, \overrightarrow {X}, t)\right) \tag {1}
$$

where $\lambda_{i}$ is the parameter used to indicate the real-valued weight of feature functions in CRF. $f_{i}$ is a positive real-valued feature function used for characterizing its arguments, which is set manually according to our training data. m is the number of feature functions. Assuming the length of the observation sequence is $n + 1$ , the conditional distribution $p(\overrightarrow{Y}|\overrightarrow{X})$ based on the factor $\psi_{t}(Y_{t-1}, Y_{t}, \overrightarrow{X}, t)$ is listed as follows,

$$
p (\overrightarrow {Y} | \overrightarrow {X}) = \frac {1}{Z _ {\lambda} ^ {\rightarrow} (\overrightarrow {X})} e x p \left(\sum_ {t = 1} ^ {n} \sum_ {i = 1} ^ {m} \lambda_ {i} f _ {i} (Y _ {t - 1}, Y _ {t}, \overrightarrow {X}, t)\right) \tag {2}
$$

where $Z_{\overrightarrow{\lambda}}(\overrightarrow{X})$ is a normalized factor defined in [22] to normalize probability $p(\overrightarrow{Y}|\overrightarrow{X})$ in [0,1].

Given the training data, we can estimate the weight $\lambda_{i}$ of each feature function $f_{i}$ by maximizing the conditional log-likelihood of the labelled sequences [28]. For fast training, the parameter estimation is based on the limited-memory BFGS [36]. CRF leverages Viterbi Algorithm [11] to predict the current hidden sleep stage $Y_{t}$ according to the feature functions and their weights.

# EXPERIMENTS

Sleep Hunter is implemented as a prototype system on Android OS platform with various types of mobile phones. The experiments are described as follows.

# Experiment setups

To give a comprehensive evaluation, we install Sleep Hunter on four different types of smartphones including: Samsung Galaxy S4 I9508, Samsung Note 2, HTC G14, and MIUI 2SC. All these smartphones are equipped with necessary sensors for sleep stage detection. The hardware configurations of these phones are detailed in Table 2. As Sleep Hunter is independent of platforms, we envision Sleep Hunter to be easily extended to other mobile operating systems like WP8 and iOS.

# Training Data

We collect 90 sets of nocturnal sleep data as the training data to learn the sleep-related features by the CRF model. A total of 45 volunteers from 10 years old to 60 years old participate in the experiments and each of them contributes 2 sets of nocturnal sleep data. We divide these volunteers' ages into 5 stages by every 10 years and there are 9 participants in each stage. During experiments, these volunteers sleep alone in a quiet room and each of them sleeps at least 6 hours within a general period from 22:00 to 9:00 the next day. Moreover, every participant wears Zeo and runs Sleep Hunter in his/her smartphone simultaneously during sleep. The smartphone is placed beside the participant's head.

![](images/7d80c5585e36e793602aba874c82f0808d0183ff645d3e21b1a8a07901ed689f.jpg)



Figure 9. The results of cross validation

Considering that there is no absolute ground truth to detect sleep stage and the operations of other professional medical equipment are complicated, we leverage the result of Zeo, which is based on EEG, as the ground truth. Though Zeo is not a professional medical sleep monitor, its accuracy is around 75% [35], which is comparable to the accuracy (about 80%) of those polysomnography-based research works [23, 30, 9]. Therefore, it is reasonable to regard the results of Zeo as our ground truth to train the CRF model and measure the detection performance of Sleep Hunter.

Actually, Zeo detects four sleep stages: wake, REM, light sleep and deep sleep. Since both physiological properties and physical activities of wake and REM are similar, and the duration of wake rarely occurs in the sleep process based on our experiments, we regard wake stage as REM in Sleep Hunter, which makes little negative influence on the sleep stage detection.

Fig. 9 shows the 10-fold cross-validation [21] based on the training data. For REM and light sleep, the average precisions and recalls lie above $60\%$ . For deep sleep, its precision is around $63\%$ and its recall is about $52\%$ . Moreover, the standard deviations of precision and recall of each stage are less than $5\%$ , demonstrating the performance of CRF is stable and robust.

# Testing Data

The testing data is collected over 30 sets of nocturnal sleep data from 15 volunteers with different genders and careers across various age stages as those of 45 training participants. In each age stage, we collect sleep data from 3 volunteers, with each contributing 2 sets of nocturnal sleep data. The sleep periods are also consistent with those of participants in the training data. To compare the detection performance of Sleep Hunter with other actigraphy-based products, apart from wearing Zeo and placing a smartphone installed Sleep Hunter beside his/her head as the 45 training participants, each volunteer is also asked to wear Jawbone Up [16] on his/her wrist and installs Sleep As Android [37] in the smartphone. Jawbone Up and Sleep As Android, the two representative and widely used products for sleep stage

<table><tr><td rowspan="2">Ground Truth</td><td colspan="3">Predictions</td><td rowspan="2" colspan="2"></td></tr><tr><td>REM</td><td>Light Sleep</td><td>Deep Sleep</td></tr><tr><td>REM</td><td>538</td><td>206</td><td>39</td><td>68.71%</td><td rowspan="3">Recall</td></tr><tr><td>Light Sleep</td><td>246</td><td>630</td><td>77</td><td>66.11%</td></tr><tr><td>Deep Sleep</td><td>61</td><td>108</td><td>174</td><td>50.73%</td></tr><tr><td rowspan="2"></td><td>63.67%</td><td>66.74%</td><td>60.00%</td><td rowspan="2" colspan="2">64.55%Accuracy</td></tr><tr><td colspan="3">Precision</td></tr></table>

Figure 10. Performance of sleep stage detection

![](images/da803bc6bdd1fa300ab0883f6a68c7c89260c36ba7c5ffb901c9483bc46b5e8e.jpg)



Figure 11. Accumulative time error

detection, run the whole sleep process with Sleep Hunter. Since Jawbone Up is a comfortable and effortless bracelet $[17]$ , its small size and light weight make it hard to be felt by sleepers during sleep. Moreover, Sleep As Android is an app running on smartphone. The sleep environments of the 15 testing participants, therefore, are similar to those of the 45 training participants.

# Performance of Sleep Stage Detection

We measure the sleep stage detection performance of Sleep Hunter based on the testing dataset. The overall detection performance is shown in Fig. 10. The percentages in black blocks point to the precisions and recalls of the three types of sleep stages and the overall detection accuracy. The result of light sleep, whose precision reaches 66.74% and recall arrives at 68.71%, shows the outstanding detection performance. REM also exhibits satisfying detection performance. Its precision arrives at 63.67% and recall reaches 66.11%. The precision and recall of the deep sleep stage seem slightly weaker than those of the other stages. The values of these two indices are 60.00% and 50.73% respectively. We can explain this phenomenon by the values in the confusion matrix in Fig. 10. The values in white and grey blocks are the corresponding numbers of the three types of sleep stages in our testing data. We can learn the total amount of deep sleep is much less than REM and light sleep. It shows that the occurrence of deep sleep stage in the entire sleep process is much less than those of the other two sleep stages. Since the deep sleep happens rarely, it is harder for the classifier to learn a competitive result of this sleep stage than those of others. The values in grey blocks, however, still demonstrate that most sleep stages are detected accurately. The detection accuracy of system runs up to 64.55%, showing the overall detection performance of Sleep Hunter is satisfying.

Moreover, we also evaluate the accumulative time error of each sleep stage detected by Sleep Hunter over a whole sleep process. Fig. 11 summarizes this kind of time error accumulated over the entire 6-9 hours of sleep based on our testing dataset. We can learn that 80% accumulative time errors of deep sleep stages stay under 45 minutes. The median error of this sleep stage is only around 25 minutes. Similarly, we also see that 80% accumulative time errors of REM are under 60 minutes and its median accumulative time error reaches about 30 minutes. The upper bound of the 80% accumulative time errors of light sleep arrives at around 75 minutes, which is the longest time in the three sleep stages. Its median error is around 50 minutes. Even though the precision and recall of deep sleep are little weaker than those of the others, its accumulative time error is the lowest in the sleep stages. It can also be explained that there are less occurrences of deep sleep than those of light sleep and REM during sleep. In Fig. 11, most accumulative time errors of the three sleep stages are shorter than one hour. Since the sleep duration lasts for 6 hours to 9 hours in the testing experiments, the fact of less than one hour accumulative time error demonstrates that the detection performance of Sleep Hunter is outstanding.

![](images/7405e63bd9373f5ec3b3749e44544a9a0b551a587e35f581cab7c74ce4253757.jpg)  
Figure 12. Sleep stage tracking of one user during a night

<table><tr><td></td><td colspan="2">REM</td><td colspan="2">Light Sleep</td><td colspan="2">Deep Sleep</td></tr><tr><td>Features</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td></tr><tr><td>BM</td><td>39.62%</td><td>34.91%</td><td>37.84%</td><td>47.11%</td><td>30.12%</td><td>28.27%</td></tr><tr><td>BM+AE</td><td>45.41%</td><td>39.67%</td><td>47.83%</td><td>49.31%</td><td>38.34%</td><td>33.27%</td></tr><tr><td>BM+AE+IC</td><td>46.13%</td><td>41.81%</td><td>49.10%</td><td>52.27%</td><td>42.91%</td><td>35.84%</td></tr><tr><td>BM+AE+IC+SD</td><td>60.89%</td><td>67.99%</td><td>63.36%</td><td>59.15%</td><td>57.96%</td><td>46.53%</td></tr><tr><td>BM+AE+IC+SD+PF</td><td>63.67%</td><td>68.71%</td><td>66.74%</td><td>66.11%</td><td>60.00%</td><td>50.73%</td></tr></table>

Table 3. Evaluation of sleep-related features

Fig. 12 shows a user sleep tracking instance in our testing dataset. We carefully compared the detection results of Sleep Hunter with those of Zeo, which we regard as the ground truth. The sleep stage detection errors are labelled as the wrong zone in the last boxed line. The right zone indicates the right detection of Sleep Hunter. Since we regard wake stage as REM in Sleep Hunter, the wake stages detected by Zeo are labelled as REM in the ground truth.

In Fig. 12, we can observe that the detection errors occur frequently in the following two cases: one is during the transition of two different sleep stages, while the other is in the sleep stages with a short lifespan (i.e., less than 10 minutes). In the former case, as physical activities of sleepers do not occur immediately when a new sleep stage begins, Sleep Hunter may fail to realize the sleep transitions and make error predictions accordingly. For the sleep stages whose durations are short, physical features may not be displayed obviously, which cannot be sensed by Sleep Hunter and thus induces mistakes. Actually, this phenomenon is also consistent with the results of the testing experiments over 30 sets of nocturnal sleep data, which could be seen as the main sources of error in Sleep Hunter.

From Fig. 12, we can see that although Sleep Hunter makes misjudgement occasionally, it still obtains 57 right zones accounting for 285 minutes, which occupies nearly 70% lifespan of the sleep process.

# Evaluation on Features

Table 3 exhibits the trend of detection performance by adding each feature incrementally. The contributions of features for classification are reliant on the design of feature functions in CRF, which predict hidden variables by incorporating observable features together. Apparently, with the increasing number of features, the detection performance of the CRF model improves, demonstrating the rationality of our configurations of the feature functions and selected features.

<table><tr><td rowspan="2">Device\Stage</td><td colspan="2">Light Sleep</td><td colspan="2">Deep Sleep</td></tr><tr><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td></tr><tr><td>Sleep Hunter</td><td>66.74%</td><td>66.11%</td><td>60.00%</td><td>50.73%</td></tr><tr><td>Jawbone UP</td><td>37.74%</td><td>65.14%</td><td>34.62%</td><td>29.03%</td></tr><tr><td>Sleep As Android</td><td>25.71%</td><td>32.14%</td><td>36.36%</td><td>49.61%</td></tr></table>

Figure 13. Performance comparison

# Performance Comparison

To our best knowledge, there is no obvious baseline for the sleep stage detection performance in actigraphy-based work, and thus we compare the detection performance of Sleep Hunter with Jawbone Up and Sleep As Android, two representative actigraphy-based products monitoring sleep stage and having been widely used in the market. Since these two devices only detect the light sleep stage and the deep sleep stage, we compare these two with those of Zeo.

The average values of precision and recall of these products are calculated based on our testing dataset, which are shown in Fig. 13. Even though Sleep Hunter detects one more sleep stage than the other devices, its detection ability is still much better than the other two products, which clearly demonstrates that Sleep Hunter is superior to the existing actigraphy-based detection systems of sleep stage.

# System Overhead

# System Delay and CPU Share

In this section, we leverage four types of experimental smartphones to measure the system delay and the CPU share of Sleep Hunter. Since Sleep Hunter predicts the sleep stage every 5 minutes, it makes classification by the data recorded from each submodule in the last 5 minutes while it is running. Accordingly, the system delay is determined by the time cost to deal with the data in the last 5 minutes. As the personal factor submodule collects information from the user's registration, we mainly analyze the time consumptions of other four submodules and the whole system. Table 4 illustrates the average delay of the corresponding submodules. The system delays for the smartphones range from 79s to 82.93s. Specifically, the acoustic event detection module occupies the major part of time consumption. Such cost is caused by parsing acoustic primitive data and computing its frequency spectrum. Given these submodules in the first layer run in parallel, the system delay of Sleep Hunter equals the largest time consumption of submodules in the first layer plus the time cost of the CRF model in the second layer. Since the sleep stage hardly changes in a short time (i.e., less than 2 minutes) and the smart call service could be provided as long as it lies in the wake-up period that lasts one hour in Sleep Hunter, the system delay around 80s makes little negative influence on the performance of our system.

<table><tr><td>Phones</td><td>Body Movement</td><td>Acoustic Events</td><td>Light</td><td>Duration</td><td>CRF</td><td>Total</td><td>CPU Share</td></tr><tr><td>Galaxy S4</td><td>12.72s</td><td>77.75s</td><td>1.61s</td><td>0.69s</td><td>1.55s</td><td>79.00s</td><td>6%</td></tr><tr><td>Note2</td><td>12.21s</td><td>77.87s</td><td>1.87s</td><td>0.58s</td><td>1.63s</td><td>80.50s</td><td>5%</td></tr><tr><td>HTC G14</td><td>14.78s</td><td>80.12s</td><td>2.37s</td><td>1.02s</td><td>2.81s</td><td>82.93s</td><td>9%</td></tr><tr><td>MIUI 2SC</td><td>12.31s</td><td>78.19s</td><td>1.58s</td><td>0.59s</td><td>2.74s</td><td>80.90s</td><td>8%</td></tr></table>

Table 4. CPU share and processing time

![](images/01dcd93c67fa81c4111390698b073e08b65635111dd77fe53c10243b03528749.jpg)



![](images/c9a0b9a4db3ee32ac58aa746ec7aba8a47d4b300b88e7244c88c5b4306533b01.jpg)



Figure 14. Sleep quality report

Furthermore, we can observe that the CPU shares of Sleep Hunter with 4 types of smartphones in Table 4. The CPU share for G14 is little larger than those of other three smartphones, which may be caused by the different properties of CPU. Despite such a difference, the CPU share of Sleep Hunter stays stable from 5% to 9%, indicating that Sleep Hunter occupies negligible CPU resource for daily use.

# Case study

# Sleep Quality Report

Since sleep quality is determined by the percentage of different sleep stages during the whole sleep process, we can measure a user's sleep quality by Sleep Hunter. We design a sleep quality measuring method based on the evaluation approach 'ZQ' of Zeo [42]. 'SQ' is a score shown in Eq. 3 for measuring the sleep quality of users in Sleep Hunter. Its structure and parameters are designed according to 'ZQ', where REM, Deep and Light represent their durations (minutes) in a sleep process. The range of 'SQ' is from 50 to 100.

$$
S Q = \left\lceil \frac {(R E M \times 0 . 5 + L i g h t \times 0 . 7 5 + D e e p) \times 1 0 0}{R E M + L i g h t + D e e p} \right\rceil \tag {3}
$$

The right figure in Fig. 14 illustrates the average ‘SQ’ and ‘ZQ’ of 2 sets of nocturnal sleep data for the 15 users in the testing dataset. Though differences exist in the structures of ‘SQ’ and ‘ZQ’, the general variance trends of these two indices are correlated with the growth of age.

We analyze the sleep quality by ‘SQ’ in the following parts.

We observed that the occurrence of deep sleep is usually affected by its starting time and duration. According to our observation of the testing dataset, we figure out that if the deep sleep stage occurs in the first hour after the user falls asleep and lasts more than 10 minutes, the possibility of its recurrence is high and the sleep quality is usually appealing. Otherwise, the percentage of deep sleep would be low and the sleep quality is disappointing. The left figure in Fig. 14 shows the distribution of sleep stages in the two different conditions based on our testing dataset. Condition 1 stands for the distribution of sleep stages in a sleep process when the deep sleep stage occurs in the first hour and lasts for more than 10 minutes. Condition 2 represents the opposite case. Clearly, the percentage of deep sleep in Condition 1 is significantly larger than that in Condition 2. Based on Eq. 3, 'SQ' in Condition 2 is usually lower than that in Condition 1. It reflects the fact that if a user cannot fall into deep sleep within one hour or remains in this stage in a short time, the user's sleep quality will be low. Based on our knowledge of medical research [4], if the brain waves of a person remain rapid for a long time, it is hard for him/her to transform the fast brain waves to slow brain waves. It is because fast

![](images/91c71d3771dd637fcbe0bfb954892cefa2c53fb999babf6d1902d53f3faee689.jpg)



Figure 15. Smart call service

brain waves often make individuals excited, the long period excitement would disturb their normal rest habits.

As a point of interest, we also make an analysis on the relationship between age and sleep quality. From the right figure in Fig. 14, we observe that 'SQ' decreases with the increase of the age generally. More specifically, we find two rapid drops in Fig. 14. The first sudden drop occurs at the age of around 30. 'SQ' falls from the score around 75 to the score about 65. According to our observation, we think the 10-point drop stems from users' work and family stress. At this age stage, most individuals have their own families to take care of and carry more workload than they used to do in school. High pressure, therefore, leads to the poor sleep quality. The second sudden drop occurs at the age of 40. 'SQ' slips from the score above 65 to the score near 55. It is likely that many users are approaching menopause during this age stage, when their physiological functions are experiencing changes. Some climacteric syndromes cause adverse impacts on the users and then decrease their sleep qualities. Given that the gender and career of the 15 participants in the testing dataset are different, our sleep quality report, therefore, is convincing and representative to some extent. We note that all conclusions are speculative based on our small sample size, but our observations are consistent with other sleep research studies [6, 31, 10].

According to the observations above, we could make two recommendations for users. 1) Since the beginning of sleep highly impacts the quality of the whole sleep process, people may benefit from light activities for relaxation before going to bed. For example, listening to some soft music, making several deep breaths or taking a warm bath can greatly help people relax before sleep. 2) People in their 30s are largely threatened by the pressure from work. Individuals at this age may benefit from some adjustments to achieve a greater balance between work and life. Seeking advice from more experienced people and cultivating a positive attitude may help them release some pressure off. For those at their 40s, health deals, moderate but habitual exercise could help them improve sleep quality.

# Smart Call

Sleep Hunter can also provide smart wake-up services based upon the sleep stage detection, since individuals feel much more refreshed when they are woken up in light sleep [4]. Users are allowed to set a one-hour period when they want to be woken, and then Sleep Hunter wakes the user up when it detects the current sleep stage is light sleep during the preset period. If Sleep Hunter detects no light sleep for the duration, it wakes users up at the end of this period. Fig. 15 depicts an illustration of a real smart call case in our testing experiments. The user sets the wake-up period from 6:30 a.m. to 7:30 a.m., and then Sleep Hunter will automatically wake the user up based on the detection result of sleep stages in the period. When Sleep Hunter detects that the user stays in a light sleep at 7:25 a.m., Sleep Hunter sings a soft song to wake him/her up.

<table><tr><td>Case</td><td>Explanation</td><td>Sleep Hunter</td><td>Sleep As Android</td></tr><tr><td>Case 1</td><td>There are actual some light sleep stages in the preset wake-up period and the app detects these light sleep stages rightly.</td><td>86.67%</td><td>42.33%</td></tr><tr><td>Case 2</td><td>There are actual some light sleep stages in the preset wake-up period but the app does not detect these light sleep stages in the right time or does not find any light sleep stages at all.</td><td>6.67%</td><td>36.33%</td></tr><tr><td>Case 3</td><td>There are no light sleep stage in the preset wake-up period actually but the app mistakes some other sleep stages as light sleep.</td><td>6.67%</td><td>21.33%</td></tr><tr><td>Case 4</td><td>There are no light sleep stage in the preset wake-up period actually and the app also does not find them.</td><td>0%</td><td>0%</td></tr></table>

Table 5. Performance of smart call service

We evaluate the smart call performance of Sleep Hunter and Sleep As Android by the users in our testing experiments. Each user is asked to select a wake-up period before going to bed. Table 5 gives the occurrence rates of these two apps under four different cases. Compared with Sleep As Android, the larger occurrence rate in Case 1 and smaller occurrence rates in Case 2 and Case 3 show that the smart call service of Sleep Hunter performs much better. Moreover, 86.67% occurrence rate of Case 1 demonstrates that Sleep Hunter is able to provide the smart call service accurately. There are mainly two reasons behind this. The first one is the remarkable sleep stage detection performance of Sleep Hunter. The second one is that more light sleep stages and REM occur and less deep sleep stages happen during the latter period of sleep. Since Sleep Hunter has shown excellent detection performances of light sleep and REM, smart call service, therefore, exhibits outstanding.

# DISCUSSION

The sleep stage detection accuracy of Sleep Hunter is 64.55%, which seems hardly comparable to those of polysomnography-based devices. Therefore, Sleep Hunter cannot take place of those professional medical devices for the high-accurate sleep detection. However, Sleep Hunter, as an app, pays more attention to providing a pervasive and less intrusive sleep service using commodity smartphones. By Sleep Hunter, users can be informed of their general sleep condition conveniently and be woken up properly.

# RELATED WORK

The state-of-the-art research areas related to our work can be divided into the following two categories.

# Polysomnography-based work

Polysomnography-based research works detect sleep quality by some certain biomedical signals. For example, most medical research works on sleep quality leverage electroencephalograph (EEG) to monitor brain waves and then recognize sleep stages. In $[23, 30, 9]$ , authors extract the electroencephalograph features from polysomnography (PSG) and leverage unsupervised learning approaches to predict sleep stages.

Moreover, some sleep quality monitors are assisted by additional devices. Zeo [41], which is a product based on EEG, leverages a brain wave sensor built in a headband to monitor sleeper's electroencephalograph, and then the EEG recordings are sent to the user's smartphone via Bluetooth. Zhang et al. [43] design a real-time system to monitor the user's sleep condition. It ameliorates users' sleep qualities by exploiting a pulse oximeter to detect the pulse oxygen saturation (SPO2) of the human body during their sleep processes.

Compared with such works, Sleep Hunter concentrates on physical activities rather than biomedical signals. Moreover, it does not need special additional devices for detection.

# Actigraphy-based work

Actigraphy-based research works leverage physical activities to predict sleep quality. iSleep [14] measures the sleep quality by recording some certain sleep-related acoustic events and evaluates it by the Pittsburgh Sleep Quality Index (PSQI) [7]. Bai et al. [3] predict the sleep quality by observing users' daily activities with smartphones. In [19], the authors leverage pervasive sensors to record the sleep disruptors for users. The authors in [15] monitor sleep by the RFID sensors installed with accelerometers.

Many products such as Sleep As Android [37] and Jawbone Up [16] predict sleep stages and measure sleep quality based on physical activities including body movement and snore simply. For example, when many body movements or acoustic events happen in a period, they regard the user stays in light sleep. On the contrary, the user is assumed to step into deep sleep as long as little body movement and ambient noise occur in the period.

Different from these works, Sleep Hunter evaluates the user's sleep quality by measuring the durations of different sleep stages in a sleep process rather than recording some certain sleep-related activities. It incorporates sleep-relative events from different perspectives and leverages a statistical model to predict the sleep stage, which provides a fine-grained detection performance of sleep stages without any assistant devices.

# CONCLUSION

Recent advances in sensor technology and machine learning technique empower machine to intelligently understand human behaviors. This paper guides this opportunity into an application that automatically detects sleep stage transitions of sleepers for sleep quality monitoring. The core idea is to leverage built-in sensors on commodity phones to sense sleep-related events, and further predict the dwelling time of each sleep stage by a statistical model based on these observable events. We implement Sleep Hunter on Android platform and test it with data collected over 30 sets of nocturnal sleep data. The results show that our system achieves desirable detection accuracy.

# ACKNOWLEDGMENT

We would like to thank the anonymous reviewers and our shepherd, Eric C. Larson, for providing valuable comments. This work is supported in part by the NSFC Major Program 61190110, NSFC under grant 61171067 and 61133016, National Basic Research Program of China (973) under grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under grant 61125202.

# REFERENCES

1. Actigraphy.
http://en.wikipedia.org/wiki/Actigraphy.   
2. Ancoli-Israel, S., Cole, R., Alessi, C., Chambers, M., Moorcroft, W., and Pollak, C. The role of actigraphy in the study of sleep and circadian rhythms. american academy of sleep medicine review paper. Sleep 26, 3 (2003), 342–392.   
3. Bai, Y., Xu, B., Ma, Y., Sun, G., and Zhao, Y. Will you have a good sleep tonight?: sleep quality prediction with mobile phone. In Proceedings of the 7th International Conference on Body Area Networks, ICST (Institute for Computer Sciences, Social-Informatics and Telecommunications Engineering) (2012), 124–130.   
4. Beloved, M. Meditation Pictorial. Michael Beloved, 2011.   
5. Boswell, D. Introduction to support vector machines, 2002.   
6. C. Marquie, J. Foret, Y. Q. J. Effects of age, working hours, and job content on sleep: a pilot study. Experimental aging research 25, 4 (1999), 421–427.   
7. Carpenter, J. S., and Andrykowski, M. A. Psychometric evaluation of the pittsburgh sleep quality index. Journal of psychosomatic research 45, 1 (1998), 5–13.   
8. Carskadon, M. A., Dement, W. C., et al. Normal human sleep: an overview. Principles and practice of sleep medicine 4 (2000), 13–23.   
9. Ebrahimi, F., Mikaeili, M., Estrada, E., and Nazeran, H. Automatic sleep stage classification based on eeg signals by using neural networks and wavelet packet coefficients. In Engineering in Medicine and Biology Society, 2008. EMBS 2008. 30th Annual International Conference of the IEEE, IEEE (2008), 1151–1154.   
10. Eichling, P., and Sahni, J. Menopause related sleep disorders. J Clin Sleep Med 1, 3 (2005), 291–300.   
11. Forney Jr, G. D. The viterbi algorithm. Proceedings of the IEEE 61, 3 (1973), 268–278.   
12. Fosler-Lussier, E., He, Y., Jyothi, P., and Prabhavalkar, R. Conditional random fields in speech, audio, and language processing. Proceedings of the IEEE 101, 5 (2013), 1054–1075.   
13. Goutte, C., and Gaussier, E. A probabilistic interpretation of precision, recall and f-score, with implication for evaluation. In Advances in information retrieval. Springer, 2005, 345–359.   
14. Hao, T., Xing, G., and Zhou, G. isleep: unobtrusive sleep quality monitoring using smartphones. In Proceedings of the 11th ACM Conference on Embedded Networked Sensor Systems, ACM (2013), 4.   
15. Hoque, E., Dickerson, R. F., and Stankovic, J. A. Monitoring body positions and movements during sleep using wisps. In Wireless Health 2010, ACM (2010), 44–53.   
16. Jawbone Up. https://jawbone.com/up.   
17. Jawbone Up review: An easy-to-wear and insightful fitness pal.
http://www.cnet.com/products/jawbone-up/.

18. Jean-Louis, G., Kripke, D. F., Ancoli-Israel, S., Klauber, M. R., and Sepulveda, R. S. Sleep duration, illumination, and activity patterns in a population sample: effects of gender and ethnicity. Biological psychiatry 47, 10 (2000), 921–927.   
19. Kay, M., Choe, E. K., Shepherd, J., Greenstein, B., Watson, N., Consolvo, S., and Kientz, J. A. Lullaby: a capture & access system for understanding the sleep environment. In Proceedings of the 2012 ACM Conference on Ubiquitous Computing, ACM (2012), 226–234.   
20. Kedem, B. Spectral analysis and discrimination by zero-crossings. Proceedings of the IEEE 74, 11 (1986), 1477–1493.   
21. Kohavi, R., et al. A study of cross-validation and bootstrap for accuracy estimation and model selection. In IJCAI, vol. 14 (1995), 1137–1145.   
22. Lafferty, J., McCallum, A., and Pereira, F. C. Conditional random fields: Probabilistic models for segmenting and labeling sequence data.   
23. Längkvist, M., Karlsson, L., and Loutfi, A. Sleep stage classification using unsupervised feature learning. Advances in Artificial Neural Systems 2012 (2012), 5.   
24. Larson, E. C., Goel, M., Boriello, G., Heltshe, S., Rosenfeld, M., and Patel, S. N. Spirosmart: Using a microphone to measure lung function on a mobile phone. In Proceedings of the 2012 ACM Conference on Ubiquitous Computing, ACM (2012), 280–289.   
25. Li, D., Sethi, I. K., Dimitrova, N., and McGee, T. Classification of general audio data for content-based retrieval. Pattern recognition letters 22, 5 (2001), 533–544.   
26. Lichstein, K. L., Durrence, H. H., Riedel, B. W., Taylor, D. J., and Bush, A. J. Epidemiology of sleep: Age, gender, and ethnicity. Psychology Press, 2004.   
27. Lu, H., Pan, W., Lane, N. D., Choudhury, T., and Campbell, A. T. Soundsense: scalable sound sensing for people-centric applications on mobile phones. In Proceedings of the 7th international conference on Mobile systems, applications, and services, ACM (2009), 165–178.   
28. Myung, I. J. Tutorial on maximum likelihood estimation. Journal of Mathematical Psychology 47, 1 (2003), 90–100.   
29. Ohayon, M. M., Carskadon, M. A., Guilleminault, C., and Vitiello, M. V. Meta-analysis of quantitative sleep parameters from childhood to old age in healthy individuals: developing normative sleep values across the human lifespan. SLEEP-NEW YORK THEN WESTCHESTER- 27 (2004), 1255–1274.   
30. Oropesa, E., Cycon, H. L., and Jobert, M. Sleep stage classification using wavelet transform and neural network. International computer science institute (1999).   
31. Polo-Kantola, P., Erkkola, R., Irjala, K., Helenius, H., Pullinen, S., and Polo, O. Climacteric symptoms and sleep quality. Climacteric 2, 4 (1999), 293–294.

32. Polysomnography.
http://en.wikipedia.org/wiki/Polysomnography.   
33. Saunders, J. Real-time discrimination of broadcast speech/music. In Acoustics, Speech, and Signal Processing, 1996. ICASSP-96 Vol 2. Conference Proceedings., 1996 IEEE International Conference on, vol. 2, IEEE (1996), 993–996.   
34. Scheirer, E., and Slaney, M. Construction and evaluation of a robust multifeature speech/music discriminator. In Acoustics, Speech, and Signal Processing, 1997. ICASSP-97., 1997 IEEE International Conference on, vol. 2, IEEE (1997), 1331–1334.   
35. Shambroom, J. R., Fabregas, S. E., and Johnstone, J. Validation of an automated wireless system to monitor sleep in healthy adults. Journal of Sleep Research 21, 2 (2012), 221–230.   
36. Skajaa, A. Limited memory bfgs for nonsmooth optimization. Master's thesis (2010).   
37. Sleep As Android. https://play.google.com/store/apps/details?id=com.urbandroid.sleep&hl=zh\_EN.   
38. Trinder, J., Kleiman, J., Carrington, M., Smith, S., Breen, S., Tan, N., and Kim, Y. Autonomic activity during human sleep as a function of time and sleep stage. Journal of sleep research 10, 4 (2001), 253–264.   
39. Webb, W., and Agnew, H. Sleep stage characteristics of long and short sleepers. Science (1970).   
40. Yang, Z., Shangguan, L., Gu, W., Zhou, Z., Wu, C., and Liu, Y. Sherlock: Micro-environment sensing for smartphones.   
41. Zeo Sleep Manager Pro.
http://www.digifit.com/Zeo/.   
42. Whats Your Bulletproof ZQ Score? The Zeo Hack Every Sleep Hacker Needs To Know.
http://www.bulletproofexec.com/zeo-hack/.   
43. Zhang, J., Zhang, Q., Wang, Y., and Qiu, C. A real-time auto-adjustable smart pillow system for sleep apnea detection and treatment. In Proceedings of the 12th international conference on Information processing in sensor networks, ACM (2013), 179–190.