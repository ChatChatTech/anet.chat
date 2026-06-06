# Sleep Hunter: Towards Fine Grained Sleep Stage Tracking with Smartphones

Weixi Gu, Student Member, IEEE, Longfei Shangguan, Student Member, IEEE, Zheng Yang, Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract—Sleep quality plays a vital role in personal health. A great deal of effort has been paid to design sleep quality monitoring systems, providing services ranging from bedtime monitoring to sleep activity detection. However, as sleep quality is closely related to the distribution of sleep duration over different sleep stages, neither the bedtime nor the intensity of sleep activities is able to reflect sleep quality precisely. We present Sleep Hunter, a mobile service that provides a fine-grained detection of sleep stage transition for sleep quality monitoring and intelligent wake-up call. The rationale is that each sleep stage is accompanied by specific body movements and acoustic signals. Leveraging the built-in sensors on smartphones, Sleep Hunter integrates these physical activities with sleep environment, inherent temporal relation and personal factors by a statistical model for a fine-grained sleep stage detection. Based on the duration of each sleep stage, Sleep Hunter further provides sleep quality report and smart call service for users. Experimental results from over 30 sets of nocturnal sleep data show that our system is superior to existing actigraphy-based sleep quality monitoring systems, and achieves satisfying detection accuracy compared with dedicated polysomnography-based devices.

Index Terms—Smartphones; sleep stage; sensors.

# 1 INTRODUCTION

LEEP, occupying nearly one-third of human lifetime, is S a necessary and vital biological function. Physiological communities often regard sleep as a cyclical process composed of three stages: rapid eye movement (REM) stage, light sleep stage and deep sleep stage [1]. The biological characteristics of these three sleep stages are different. REM is an active period of sleep marked by intense brain activities and dream occurrence. Light sleep stage is a period of relaxation, when the heartbeat, breathing rate and muscle activity slow down. Deep sleep stage triggers hormones to promote body growth, as well as the repair and restoration of energy. Sleep quality is actually determined by the distribution of different sleep stages rather than the time duration of the overnight sleep [2]. Moreover, a proper wake-up time is also helpful for mental and physical health [3]. Comparing with other sleep stages, people wake up in light sleep stage will feel more refreshed.

Sleep quality monitoring requires a careful observation of individuals’ sleep stages. The approaches to recording sleep stages are divided into two categories. The first category is based on polysomnography [4]. The methods in this category leverage electroencephalograph (EEG) to observe brain waves and then recognize sleep stages accurately. Due to the high cost, EEG systems, e.g., Zeo [5], however, are usually limited to medical and physiological studies. The approaches in the second category are based on actigraphy [6], which utilizes certain physical activities such as body movement or snore to predict sleep stage. The detection performance of these approaches, e.g., Jawbone up [7] and Sleep As Android [8], has not yet been evaluated against medically accepted methods.

In this paper, we present Sleep Hunter, a sleep stage detection system based on actigraphy that predicts sleep stage transitions by smartphone. The information collected by Sleep Hunter can be used to evaluate human sleep quality and provide smart call service, which wakes up users in light sleep stage intelligently. The principle behind our system is that apart from implicit brain wave changes, individuals usually exhibit distinguishable physical activities during different sleep stages. For example, in REM, breathing rate is commonly unstable and people tend to exhibit large body movements. Whereas in the deep sleep stage, breathing rate becomes slower and more regular, accompanied with slight body movements such as arm trembling and leg jerking [9]. Sleep Hunter leverages built-in sensors of the smartphone to detect such sleep-related events and then predicts the transition of sleep stages overnight. Based on the detected sleep stages, it generates a corresponding score for sleep quality evaluation and provides smart call service. Compared with the methods in the first category, Sleep Hunter is a service that runs on a commercial off-the-shelf smartphone. The simple operation makes it more convenient than polysomnography-based systems. Furthermore, Sleep Hunter integrates sleep-related events comprehensively and leverages a statistical model to predict sleep stage. The fine-grained detection results and promising performance make Sleep Hunter more suitable than those actigraphy-based products.

We face two challenges when codifying this idea into a practical system. The first challenge is how to identify discriminative activities from a variety of primitive data, given the condition that sensory data are sparse and full of noise. For example, audio signals recorded by the microphone contain not only sleep-related primitives, but also ambient noise. The second challenge is how to leverage sleep-related events to capture sleep stage transitions. Many events such as snore, body movement, sleep duration and even people’s age have close relationships with sleep stage transitions. The influence of these factors should be taken into consideration as well.

TABLE 1 The physical activities happened in sleep process 

<table><tr><td>Activity</td><td>Explanation</td></tr><tr><td>Tachypneic breath</td><td>A condition of rapid breathing, commonly between 12-20 breaths per minute.</td></tr><tr><td>Apneustic breath</td><td>A series of slow, deep breathing, lasting about 6-10 seconds, after which the air is suddenly expelled by the elastic recoil of the lung.</td></tr><tr><td>Cough</td><td>A sudden and often repetitively occurring reflex which helps to clear the large breathing passages from secretions, irritants.</td></tr><tr><td>Snore</td><td>A vibration of respiratory structures and a resulting sound, due to obstructed air movement during breathing while sleeping.</td></tr><tr><td>Somniloquy</td><td>A parasomnia that refers to talking aloud while asleep. It can be quite loud, ranging from simple sounds to long speeches, and can occur many times during sleep.</td></tr><tr><td>Macro body movement</td><td>A serials of significant activities happened in sleep cycles, such as turning body over, driving or raising legs and so on.</td></tr><tr><td>Micro body movement</td><td>A serials of tiny activities appeared in sleep cycles, including short convulsion and hand trembling, head moving.</td></tr></table>

To address the above challenges, we design a unique feature-extraction mechanism for each of sleep-related events based on their physical characteristics. Moreover, we exploit conditional random field (CRF), a statistical model to parse the relations behind these events according to our over 90 sets of nocturnal sleep data, and evaluate them on our testing dataset.

The contributions of our paper are listed as follows. 1) We put forward a set of efficient algorithms to detect sleep-related events and adopt a CRF to depict the relationship between such events and sleep stages. 2) We implement Sleep Hunter on Android platform and conduct evaluation experiments on 15 participants from various age groups. The result of the testing data over one month demonstrates that the detection accuracy of Sleep Hunter attains 64.55%, which is superior to the existing actigraphy-based applications to our best knowledge. 3) We conduct extensive case studies and show that Sleep Hunter is able to provide sleep quality reports and smart call services for users.

The rest of this paper is organized as follows. We firstly detail the preliminary of sleep in Section 2. We then introduce the key insight and design targets in Section 3. In Section 4, we briefly overview the architecture of Sleep Hunter. Next, the system design is described in Section 5 and the principles behind the sleep stage detection model are shown in Section 6. Then, we present the experimental evaluation in Section 7 and provide a review of related work in Section 8. Finally, we summarize and make the conclusion in Section 9.

# 2 PRELIMINARY

# 2.1 Sleep cycle

As shown in Fig. 1, physiological communities commonly regard sleep as a cycling process composed of three main sleep stages, namely Rapid Eye Movement (REM) stage (also called dream stage), light sleep stage and deep sleep stage. The light sleep and deep sleep are

![](images/218e25b289b9f5c52c6f09e614c5ffe9e925d30c0225cc1f1612ebcf0d3aca96.jpg)



Fig. 1. An illustration of sleep stage transition

also called Non-Rapid Eye Movement (NREM), which is characterized by a reduction in physiological activities. As S5 sleep gets deeper, brain waves become slower and have greater amplitude. At the same time, breathing and heart rate slow down, and blood pressure drops. By analyzing the associated neurological features during sleep, medical studies further partitioned the three main sleep stages into five substages.

Generally, people commonly experience a transition from light sleep $( { \bar { S } } _ { 1 }$ and $S _ { 2 } )$ to deep sleep $( S _ { 3 }$ and $S _ { 4 } )$ , lasting about $\bar { 7 0 }$ minutes before entering the REM phase. Fig. 1 illustrates the sleep cycle during the night, where sleep follows a predictable pattern, moving cyclically among light sleep stage, deep sleep stage and REM stage. Each cycle typically lasts for about 90 minutes and repeats four to six times over a night.

# 3 KEY INSIGHT AND DESIGN TARGETS

In this section, we first present the key insight for sleep cycle detection scheme, and then specify the design targets.

# 3.1 Key Insight

Our key insight here is related to the following aspects. Firstly, apart from the implicit physiological activities (e.g., body temperature changes and brain activity variations), sleepers usually exhibit distinguishable physical activities in different sleep stages [10]. For example, short breaths and large body movements such as body rollovers usually happen in light sleep, resulting fast heartbeat. On the contrary, slight body movements such as arm trembling and leg jerking [11] mostly occur in deep sleep due to the slow and regular breathing rate. Moreover, somniloquy and body trembles caused by frequent dreams generally appear in REM. Such physical activities can be detected via off-the-shelf smartphones, serving as the basis for the sleep stage analysis. Table 1 summarizes the physical activities that Sleep Hunter mainly monitors during the sleep process.

Secondly, sleep usually follows a predictable pattern, moving cyclically among light sleep stage, deep sleep stage and REM. Each sleep cycle typically lasts for about 90 minutes and repeats four to six times over a night. In each sleep cycle, sleepers firstly experience a transition from light sleep to deep sleep and then enter REM. This sequence is shown by solid black lines in Fig. 1. Nevertheless, sleep cycle is not an absolute case. The phenomenon of skipping some certain sleep stages usually occurs during sleep. For example, as shown by the grey dashed lines in Fig. 1, sleep stage could jump to REM from light sleep or return to deep sleep from REM directly. The dependence between two successive sleep stages, however, still exists. This inherent temporal sequence could also be utilized for analyzing sleep stages. Moreover, sleep environment, $e . g .$ , ambient illumination, and certain personal factors, e.g., age, also impact the sleep phases [11], which help us to predict the transition of sleep stages.

# 3.2 Design Targets

The principal functions of Sleep Hunter are to monitor the sleep quality and wake people up at proper time instance. Specifically, Sleep Hunter is designed to meet the following requirements. (1) As Sleep Hunter operates over sleeping period, it should be non-intrusive. This is a basic requirement and is widely accepted by sleeping-related products or applications [8], [12]. (2) Sleep Hunter needs to precisely detect the current sleep stage of the user, as well as recording the fine-grained duration of each stage across different users. (3) As a long-term running application, Sleep Hunter should be energy efficient. It should be affordable for users to execute during the whole sleep process, and also be able to detect the state transition promptly.

# 4 SYSTEM OVERVIEW

# 4.1 System Architecture

Sleep Hunter is a two-layer system and provides an interface for upper layer applications. Fig. 2 shows its architecture. The first layer is composed of five submodules: body movement detection module, acoustic event detection module, illumination condition detection module, sleep duration tracking module and personal factor collection module. Each module is responsible for collecting its related primitive data and extracting associated features. The second layer leverages CRF to integrate features from the upper layer. Based on these collected features, this layer makes sleep stage prediction for the corresponding period, which is called detection phase. The duration of detection phase is set to be 5 minutes. In other words, Sleep Hunter detects sleep stage every 5 minutes during sleep. Moreover, Sleep Hunter provides sleep quality report and smart call service for users in the interface layer based on the monitoring results of sleep stages.

![](images/be3bd7df6fe6eda717c31aa7018c4cc69f8650daa511f608e5acce417fa4e734.jpg)



Fig. 2. The architecture of Sleep Hunter

# 5 SYSTEM DESIGN

In this section, we specify the design and implementation details for each component in Sleep Hunter.

# 5.1 Body Movement Detection (BM)

Sleepers usually exhibit various physical activities during different sleep stages. As reported by medical views [10], large body movements like body rollovers usually occur when people are in light sleep, which result from the fast heartbeat during this stage. In contrast, some tiny body movements such as body trembling and leg jerking usually occur in deep sleep stage. Moreover, some unconscious body movements such as the leg stretching and the arm rising would happen during REM, which are caused by frequent dreams. Accordingly, we could leverage the distinguishable movements to detect various sleep stages.

# 5.1.1 Body Movement Experiments

In order to better understand the phenomenon of body movements during sleep, 100 groups of sleep-related body movement experiments are conducted by 10 volunteers across different ages when they are in bed. Every volunteer contributes 10 groups of experiments. In each experiment, the volunteer puts a smartphone beside his/her head and enables the accelerometer to calculate the corresponding acceleration variance trace of the body movement. The sample rate of accelerometer is set to be 100Hz, which is same as the configuration of Sleep Hunter. Acceleration variance is calculated as $V ( i ) \ = \ \hat { a } ( i ) \ : - \ : a ( i \ : - \ : 1 )$ , where $a ( i ) = \sqrt { a _ { x } ( i ) ^ { 2 } + a _ { y } ( i ) ^ { 2 } + a _ { z } ( i ) ^ { 2 } }$ and $a _ { x } ( i ) , a _ { y } ( i )$ and $a _ { z } ( i )$ represent the accelerometer sample value of X-axis, Y-axis and Z-axis at time stamp i respectively. The sleep-related body movements include body rollover, leg stretching, arm raising, figure trembling, leg jerking and head movement. Fig. 4 plots a real acceleration variance trace of one volunteer’s body movements.

![](images/6428a2970f09a93d982caa8430de87efd31ab60c862b191a51dffb66528bb405.jpg)



![](images/140fc216baa85ce75be86f5400b980a9b02289a2a66c38bd5f71a11ade842063.jpg)



Fig. 3. Durations of body movements

# 5.1.2 Body Movement Extraction

Considering the distribution of inherent accelerometer’s noise, we denote the threshold by ξ to classify the accelerations of body movement and noise. If $| V ( i ) | \geq \xi ,$ we regard it as an occurrence of body movement. Otherwise, we take it as noise. In order to find an effective threshold. We vary ξ from 0.01 to 0.07 and analyze the precision and recall based on the data trace contains over 4000 body movements. The result is shown in Table. 2. According to the results, we set ξ to 0.05 which locally optimizes the performance.

However, body movements such as body rollover and leg stretching are not continuous. The temporal pauses in body movements would cause our mechanism mistakenly to split a single body movement into multiple movements. To solve this problem, we realize the longest temporal pause in our body movement experiments belongs to the body rollover, which lasts less than 1.5s. Sleep Hunter empirically merges two successive movements into a single one if they occur within 1.5s.

# 5.1.3 Body Movement Classification

For a better analysis of the relationship between sleep-related body movements and sleep stages, we calculate the durations of those large, long-lasting actions such as body rollover, leg stretching and arm raising, and tiny, short-lasting activities including arm trembling and leg jerking from our body movement experiments. Fig. 3 shows the distribution of body movement’s durations in two sets. We found that all of the large, long-lasting body movements last at least 2.8s while those tiny, short-lasting activities last at most 0.85s. This obvious temporal gap helps us to distinguish these movements into two categories. In Sleep Hunter, we define the movements lasting less than 1s as micro body movements and those lasting longer as macro body movements, and leverage these two kinds of body movements as sleep-related features.

# 5.2 Acoustic Event Detection (AE)

Apart from body movements, people usually display some acoustic events during sleep. We concentrate on five common sleep-related acoustic events: somniloquy, tachypneic breath, apneustic breath, snore and cough. Based on the physiological research [10], somniloquy occurs frequently during REM because of continual dreams. Tachypnea, which is easily incurred by the rapid heartbeat, usually happens during light sleep. Moreover, apneusis often appears in deep sleep due to the slow heartbeat, and snore usually emerges in deep or light sleep. Furthermore, cough is not likely to come about during deep sleep, since it can easily disturb the sleep process.

![](images/fb8d8c679d9ed201f08e6c70493e4bcc94f2b44588e93844c86137c11b6b6b19.jpg)



Fig. 4. Acceleration trace of body movement

TABLE 2 The precision, recall, F1 under different ξ settings 

<table><tr><td>ξ</td><td>precision</td><td>Recall</td><td>F1</td></tr><tr><td>0.01</td><td>0.700</td><td>1.000</td><td>0.824</td></tr><tr><td>0.02</td><td>0.700</td><td>1.000</td><td>0.824</td></tr><tr><td>0.03</td><td>0.875</td><td>1.000</td><td>0.933</td></tr><tr><td>0.04</td><td>0.875</td><td>1.000</td><td>0.933</td></tr><tr><td>0.05</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>0.06</td><td>1.000</td><td>0.571</td><td>0.727</td></tr><tr><td>0.07</td><td>1.000</td><td>0.286</td><td>0.444</td></tr></table>

# 5.2.1 Acoustic Event Experiments

We utilize the built-in microphone, whose sample rate is set to be 16KHz, to record acoustic data. A total of 30 participants join our acoustic experiments and their smartphones are placed beside their heads during sleep. According to these recording data, we label acoustic events manually and thus collect 180 sound clips for each type of acoustic event from the 30 people, with each sound clip lasting around 5 seconds. These sound clips cover different sleeping stages and are collected from the 30 volunteers with diverse ages, genders and physical characteristics. Hence we envision such diverse data cover the human diversity and could reflect the inner properties of sleep-related acoustic events. The collected data, therefore, are sufficient for us to study the inner properties of these sleep-related acoustic events.

The acoustic analysis begins with dividing the audio stream from the microphone into frames of equal duration. Each frame is composed of 1024 acoustic samples, and thus its duration is 64ms, which is able to capture the acoustic characteristics of sounds [13].

# 5.2.2 Noise elimination

Since different kinds of noise exist in the sleep environment, the negligible effect of noise should be eliminated firstly. According to our observation, there are mainly three types of noises during sleep: ambient noise, noise made by body movement and traffic noise. Sleep Hunter leverages the scheme in [13] to differentiate the ambient noise from other types of noise and sleep-related acoustic events. The scheme recognizes ambient noise by its low root-mean-square (RMS) energy and high spectral entropy [14]. If RMS of the current frame is less than a predefined threshold $T h _ { r m s }$ and its entropy is higher than $\dot { T h } _ { e n t r o p y } ,$ , it is ambient noise. Here, we empirically set $T h _ { r m s } = 0 . 0 0 6$ and $T h _ { e n t r o p y } =$ 25, which locally optimizes the detection accuracy on our acoustic event experiments. Moreover, body movements such as body rollovers during sleep would make additional noise. Since they generally induce variances of acceleration and sound simultaneously, we preset threshold  to measure this simultaneity and leverage it to detect the noise made by body movement. In other words, if the temporal deviation between the beginnings of an acoustic event and a body movement is less than $\epsilon ,$ and the temporal deviation between their endings is also less than $\epsilon ,$ we regard the acoustic event as noise made by body movement and then filter it out. In Sleep Hunter, we set $\epsilon = 0 . 5 s$ .

![](images/720ffdbddd3b3c9a94335a131815528e98c449fead32e9036eb5f0082143db70.jpg)  
Fig. 5. Correlation matrix between features and acoustic events

# 5.2.3 Acoustic Feature Selection

Let $\{ s _ { 1 } , s _ { 2 } , . . . . . . , s _ { m } \}$ be an acoustic frame sampled by the micrphone, where $s _ { j }$ stands for the jth sample in a frame. We then extract six kinds of acoustic features from both the time and frequency domain. The detailed explanations of these features are listed in Table 3. These features are also widely adopted by various works [12], [13], [15].

Fig. 5 illustrates the correlation matrix between the aforementioned acoustic features and the frames of different acoustic events collected by our experiments. Each row/column represents a feature. The curve in the boxes on the diagonal line stands for the distribution of the corresponding feature. We can learn that the flux of somniloquy lies in a relatively low level, which demonstrates that its frequency spectrum is stable. On the contrary, the flux of traffic is generally higher than those of others, which is coherent with our intuition that the frequency spectrum of traffic is abrupt. Moreover, the apneustic breath, whose rolloff is large, possesses a high frequency. Furthermore, we can see that most tachypneic breaths locate where entropy and bandwidth are both low. It shows a fact that the sound of this type of breath possesses an obvious pattern and its frequency spectrum is narrow. Since different acoustic events perform distinguishing distributions under various features, we can leverage such features to classify them.

TABLE 3 List of acoustic features 

<table><tr><td>Feature domain</td><td>Feature</td><td>Explanation</td></tr><tr><td>Time domain</td><td>ZCR</td><td> $\frac{1}{2} \sum_{j=1}^{m} |sign(s_j) - sign(s_{j-1})|$ </td></tr><tr><td rowspan="5">Frequency domain</td><td>Entropy</td><td> $-\sum_{j=1}^{N} f_t(j) \log f_t(j)$ </td></tr><tr><td>Centriod</td><td> $\sum_{j=1}^{N} j \cdot |f_t(j)|^2 / \sum_{j=1}^{N} |f_t(j)|^2$ </td></tr><tr><td>Flux</td><td> $-\sum_{j=1}^{N} (f_t(j) - f_{t-1}(j))^2$ </td></tr><tr><td>Bandwidth</td><td> $\sum_{j=1}^{N} (j - Cen)^2 \cdot |f_t(j)|^2 / \sum_{j=1}^{N} |f_t(j)|^2$ </td></tr><tr><td>Rolloff</td><td> $max(h| \sum_{j=1}^{h} f_t(j) < threshold)$ </td></tr></table>

![](images/7b844a95edd14c98b861711c5a42a0b56a20d54135fed5860861776a494b681d.jpg)  
Fig. 6. The performance of acoustic event classification

# 5.2.4 Acoustic Event Classification

We adopt support vector machine (SVM) [16] to classify different acoustic sources. The 10-fold cross-validation [17] has been done on the collected frames of acoustic event across the 30 participants and the classification performance is illustrated in Fig. 6. We can observe that the best classification performance is achieved by traffic. Its average precision and recall reach 98.3% and 96.9% respectively. The average F1 [18] is up to 97.6%. Even though the worst result belongs to cough, its average precision and recall are still over 66%, and average F1 runs up to 67.13%. Moreover, for other four types of acoustic events (i.e., somniloquy, apneustic breath, tachypneic breath and snore), average F1 values of them are from 70% to 88%, which demonstrates the classification performance is acceptable. Furthermore, the standard deviations of all the indices illustrated by the error bars are less than 6%, which shows that the classification performance of SVM is stable and robust. Therefore, we could filter out the traffic noise and recognize the sleep-related acoustic events, and then leverage them as features to predict sleep stages.

# 5.3 Illumination Condition Detection (IC)

Generally, sleep quality is also affected by the ambient illumination conditions [11]. People may enjoy a good sleep in dim environment while feel difficult to fall asleep under strong illuminative conditions. To characterize the relationship between sleep stages and illumination intensity around, we categorize the illumination intensities into different conditions, and then explore the transition of sleep stages under these conditions. Fig. 7 illustrates the illumination intensity under different sleep environments, which is broadly categorized into three conditions: bedroom without light (Weak illumination condition, $\leq 1 0 L u x \left( \beta _ { 1 } \right) ) ;$

![](images/fb16d4ac8d15bde7563184312f06d072b60e8785479f67005fb8425528ef7563.jpg)



Fig. 7. Illumination intensity under different conditions

bedroom with dim light (Moderate illumination condition, $1 0 \sim 2 0 0 0 L u x \ ( \beta _ { 2 } ) ) ;$ bedroom with strong lights (Strong illumination condition, $\geq ~ 2 0 0 0 L u x )$ . Therefore, we could measure the sleep environment according to the three illumination conditions by the built-in light sensor of smartphones. The sample rate of the light sensor is set to be 100Hz, which is the same as the configuration of Sleep Hunter. The three types of illumination conditions are also leveraged as sleep-related features for sleep stage detection.

According to our survey, for most smartphones, the light sensor is usually installed in the front face of the phone. As a result, if the phone is facing toward the ground, the illumination sensing module could be paralyzed because the illumination samples cannot reflect the real illumination conditions around the phone. Indeed, this phenomenon occurs frequently during sleep given that some unconscious body movements would occasionally change the position of smartphones.

To overcome this challenge, we build a light-weight hierarchical illumination intensity sensing scheme. Fig. 8 illustrates the work flow of this sensing scheme. Firstly, Sleep Hunter employs the proximity sensor to detect whether the light sensor is blocked or not. If it is not blocked, Sleep Hunter calculates the average illumination intensity $l _ { c u r }$ in the detection phase, and then determines the current illumination condition by comparing $l _ { c u r }$ with the two preset thresholds: $\beta _ { 1 } , \beta _ { 2 }$ . On the other hand, if the light sensor is blocked, then Sleep Hunter locates the latest record of the illumination condition when the light sensor is not blocked, and treats it as the current illumination condition until the light sensor recovers. Since the illumination condition is hard to change in a short time, we design an energy saving mechanism. If the average illumination condition is stable for the third consecutive detection phase, Sleep Hunter would stop the light sensor for 10min.

# 5.4 Sleep Duration (SD) and Personal Factor (PF)

Apart from those associated physical activities and sleep environment, the transition of sleep stage is affected by chronological rules statistically during the sleep process. According to the clinical study in [11], the first REM sleep stage usually occurs about 70 to 90 minutes after we fall asleep. A complete sleep cycle takes 90 to 110 minutes on average. Moreover, the first sleep cycle each night contains the relatively short REM phase and the relatively long period of deep sleep. As time goes by, the duration of REM increases while that of deep sleep decreases. By morning, people spend nearly all their sleep time in light sleep and REM.

![](images/3bb9fc60151dcce241443e733651c8d3b5ad249bb160ed2aa55d3a058ccaaf99.jpg)



Fig. 8. The flow chart of illumination condition detection   
![](images/6af976bc66088c060af03eb8d7f38bb6bde65c7b4d19c9d94759c95d17a02e70.jpg)



Fig. 9. Conditional random field

According to this chronological property, Sleep Hunter takes its running time as sleep duration and regards it as a sleep-related feature. Moreover, the sleep stage is also affected by the personal physiological status. For example, the proportion of deep sleep stage decreases with the increase of the user’s age [19]. Since the age of sleeper is an important physiological factor impacting sleep [20], [21], Sleep Hunter obtains the user’s age from the registration information and further takes it with the sleep duration as features for the sleep stage detection.

# 6 SLEEP STAGE DETECTION

In this section, we present the details of the sleep stage detection scheme.

We propose a linear-chain conditional random field (CRF) [22] to integrate the aforementioned features and make further inference. CRFs are discriminative models that predict the global probability of a sequence of random variables. The probability structure of a CRF depends on a log-linear combination of observable features and dependence of hidden variables, which is depicted as a bipartite factor graph. The CRF is a type of discriminative undirected graphical model. It depicts the known relationships between observations and state transitions. Before putting into practice, the model parameters are trained to maximize the joint likelihood of training examples. CRFs have been widely used in audio, speech, language processing and health sensing [23], [24]. The rationale of CRF applied here lies twofold. Firstly, as depicted in Fig. 1, the occurrence of sleep stages during sleep forms a sequence. This process can be characterized by the CRF model. Secondly, sleep-related events have dependent relationships. For example, cough or snore often leads to transient asphyxia, which decreases the oxygen capacities, and in turn, results in body movements during sleep. Compared with the Hidden Markov Model (HMM) [25], a statistical Markov model where the system is modeled as a Markov process with the hidden states, CRFs are better suited for sequences that have long interdependencies and therefore may have better performance in our applications.

# 6.1 Building up the Detection Model

Fig. 9 gives the structure of CRF model we used. The shaded nodes $( Y _ { 1 } , . . . , Y _ { t - 1 } , Y _ { t } )$ indicate the hidden sleep stage variables during sleep. $Y _ { t } \in \{ l i g h t$ sleep, deep sleep, REM } is an output of CRF model, which represents the sleep stage in the detection phase $t ,$ which is set to be 5 minutes. The unshaded node $\begin{array} { r c l } { \overrightarrow { X } } & { = } & { \{ X _ { 1 } , . . . , X _ { t - 1 } , X _ { t } \} } \end{array}$ denotes the observable sleep-related features occurred in the sleep process. $X _ { t } = \{ \hat { N } _ { B } ( t ) , N _ { A } ( t ) , N _ { I } ( t ) , N _ { D } ( t ) , N _ { P } \}$ represents the feature vector at detection phase t. The explanation of each item, which is the input of model, is listed as follows. $N _ { B } ( t ) ;$ : the number of occurrences of micro body movement and macro body movement during the detection phase t. $N _ { A } ( t )$ : the number of occurrences of sleep-related acoustic events during the detection phase t. ${ \bar { N _ { I } } } ( t )         { \mathrm { : } }$ : the illumination condition during the detection phase t. $N _ { D } ( t )$ : sleep duration. $N _ { P } { : }$ age of user.

Assuming the length of the observation sequence is $n +$ 1, the conditional distribution $p ( \vec { Y } | \vec { X } )$ based on the factor $\psi _ { t } ( Y _ { t - 1 } , Y _ { t } , \vec { X } , t )$ is listed as follows,

$$
p (\overrightarrow {Y} | \overrightarrow {X}) = \frac {1}{Z _ {\overrightarrow {\lambda}} (\overrightarrow {X})} e x p \left(\sum_ {t = 1} ^ {n} \sum_ {i = 1} ^ {m} \lambda_ {i} f _ {i} (Y _ {t - 1}, Y _ {t}, \overrightarrow {X}, t)\right) \tag {1}
$$

where $Z _ { \vec { \lambda } } ( \vec { X } )$ is a normalized factor defined in [22] to normalize probability $p ( \vec { Y } | \vec { X } )$ in [0,1]. Given the training data, we can estimate the weight $\lambda _ { i }$ of each feature function $f _ { i }$ by maximizing the conditional log-likelihood of the labelled sequences [26]. For fast training, the parameter estimation is based on the limited-memory BFGS [27]. CRF leverages Viterbi Algorithm [28] to predict the current hidden sleep stage $Y _ { t }$ according to the feature functions and their weights.

# 7 EXPERIMENTS

In this section, we detail the implementation and evaluation.

# 7.1 Prototype Implementation

We validate the architecture and algorithms of Sleep Hunter through a prototype implemented on Android OS platform. The current version is a two-layer construction which consists of around 5000 lines of code. The first layer is made up of five detection modules to monitor acoustic event, body movement, illumination condition, sleep duration and personal factor respectively. The second layer is a CRF module, which is used to predict the sleep stages. Moreover, the result of the sleep stages serves the applications of Sleep Quality Report and Smart Call Service. The sample rates of accelerometer, microphone and light sensor are set to be 100 Hz, 16KHz and 100 Hz respectively to prevent the distortion.

![](images/43db7627c475b2ea0eec3313bd6e9ce69d99be8faa6192a4fa70e21579fc4635.jpg)



(a)

![](images/65f227b668827681e357342054544ff49097265ccb20cd72490a33cefaf7d417.jpg)



(b)

![](images/022d9ea5a2b5763adc9174dc79fa759a77af696bc9561d5e3416203e04a53a8e.jpg)



(c)   
Fig. 10. User Interface of Sleep Hunter. (a) The Screen of Personal Information Collection and Smart Call Setting. (b) The Screen of Sleep Stages Tracking. (c) The Screen of Sleep Score Recording.

The total size of the application file is about 1.7 MB and occupies around 3.1 MB storage after it is launched. The displaying of user interface and each module of background processing functions are handled with mutithreading to ensure the operation efficiency.

The screen shots are shown in Fig. 10. The screen (a) provides the methods for users to input their ages and set the wake up period. The screen (b) illustrates a fine grained sleep stage conditions during the night. Users could learn their sleep condition concretely by scanning it. The screen (c) provides a historical records of the sleep score in latest seven days, which helps the user have a general view of his/her sleep quality.

The application is easy to operate. Before sleep, the user only needs to initiate the application and put the Smartphone besides his/her pillow. Alternatively, the user could set the period of morning call when he/she wants to wake up. When Sleep Hunter detects a suitable time, it will sing a soft song to wake the sleeper up. The user could scan his/her sleep stages of the night and check the sleep score after getting up.

In order to deal with the problem that the user’s position might make negative influence on the detection of Sleep Hunter, the smartphone is suggested to put beside the pillow, which is far away from the users body. Accordingly, it is hard for the users body to cover the smartphone during the sleep process. Besides, we design the mechanism to solve this kind of problem. More specifically, the illumination detection module in the section of Illumination Condition Detection leverages the proximity sensor to judge whether the front face of the smartphone is blocked by the cover. If it is covered by the other things, it would use the latest illumination intensity to take over the current illumination intensity. Such mechanism could solve the problem effectively. Lastly, even though the smartphone is moved, the performance of the sleep stage detection can still be promised. It is because that Sleep Hunter integrates multiple features with the statistical model to predict the current sleep stage. Given the fact that the prediction of sleep stage relies on many factors rather than some certain ones, even if the smartphone phone is blocked and thus some features cannot be detected accurately, the detection accuracy hardly changes a lot.

TABLE 4 Information of experimental smartphones 

<table><tr><td></td><td>OS Platform</td><td>RAM</td><td>CPU</td><td>Battery</td></tr><tr><td>Galaxy S4</td><td>Android OS 4.2.2</td><td>2GB</td><td>quad-core 1.638 GHz</td><td>2600mAh</td></tr><tr><td>Samsung Note2</td><td>Android OS 4.1</td><td>2GB</td><td>quad-core 1.638 GHz</td><td>3100mAh</td></tr><tr><td>HTC G14</td><td>Android OS 2.3</td><td>2GB</td><td>dual-core 1.228 GHz</td><td>1520mAh</td></tr><tr><td>MIUI 2SC</td><td>Android OS 2.3</td><td>2GB</td><td>quad-core 1.700 GHz</td><td>2000mAh</td></tr></table>

![](images/1ee468de71a95ac4dc1c121639a44b5e865a2d8303d766a829616c61363f5813.jpg)



Fig. 11. The results of cross validation

# 7.2 Experiment setups

To give a comprehensive evaluation, we install Sleep Hunter on four different types of smartphones including: Samsung Galaxy S4 I9508, Samsung Note 2, HTC G14, and MIUI 2SC. All these smartphones are equipped with necessary sensors for sleep stage detection. The hardware configurations of these phones are detailed in Table 4. As Sleep Hunter is independent of platforms, we envision Sleep Hunter to be easily extended to other mobile operating systems like WP8 and iOS.

# 7.3 Training Data

We collect 90 sets of nocturnal sleep data as the training data to learn the sleep-related features by the CRF model. A total of 45 volunteers from 10 years old to 60 years old participate in the experiments and each of them contributes 2 sets of nocturnal sleep data. We divide these volunteers’ ages into 5 stages by every 10 years and there are 9 participants in each stage. During experiments, these volunteers sleep alone in a quiet room and each of them sleeps at least 6 hours within a general period from 22:00 to 9:00 the next day. Moreover, every participant wears Zeo and runs Sleep Hunter in his/her smartphone simultaneously during sleep. The smartphone is placed beside the participant’s pillow.

Considering that there is no absolute ground truth to detect sleep stage and the operations of other professional medical equipment are complicated, we leverage the result of Zeo, which is based on EEG, as the ground truth. Though Zeo is not a professional medical sleep monitor, its accuracy is around 75% [29], which is comparable to the accuracy (about 80%) of those polysomnography-based research works [1], [30], [31]. Therefore, it is reasonable to regard the results of Zeo as our ground truth to train the CRF model and measure the detection performance of Sleep Hunter.

Sleep Hunter detects three sleep stages including REM, light sleep and deep sleep. However, Zeo detects four sleep stages: wake, REM, light sleep and deep sleep, which has one more stage than those of Sleep Hunter. Given the fact that both physiological properties and physical activities of wake stage and REM stage are similar [32], and the duration of wake rarely occurs in the sleep process based on our experiments, hence we replace the wake stage with REM and take them as the ground-truth.

![](images/4c5c8773bde6c69b44432f957f7ac9af5e1da872c58b757076c868781e92f766.jpg)



Fig. 12. Experiment Cases.

Fig. 11 shows the 10-fold cross-validation [17] based on the training data. For REM and light sleep, the average precisions and recalls lie above 60%. For deep sleep, its precision is around 63% and its recall is about 52%. Moreover, the standard deviations of precision and recall of each stage are less than 5%, demonstrating the performance of CRF is stable and robust.

# 7.4 Testing Data

The testing data is collected over 30 sets of nocturnal sleep data from 15 volunteers with different genders and careers across various age stages ranging from 10 years old to 60 years old as those of 45 training participants. To guarantee an objective performance evaluation result, the 15 volunteers composed of 8 males and 7 females are randomly chosen, and they are different from the participants in the training data in case of the over-fitting problem [33]. In each age stage, we collect sleep data from 3 volunteers, with each contributing 2 sets of nocturnal sleep data. The sleep periods are also consistent with those of participants in the training data. All the volunteers measure their sleep quality at their own home. To compare the detection performance of Sleep Hunter with other actigraphy-based products, apart from wearing Zeo and placing a smartphone installed Sleep Hunter beside his/her head as the 45 training participants, each volunteer is also asked to wear Jawbone Up [7] on his/her wrist and installs Sleep As Android [8] in the smartphone. Jawbone Up and Sleep As Android, the two representative and widely used products for sleep stage detection, run the whole sleep process with Sleep Hunter. Sleep Hunter detects the sleep quality of the participant automatically, and then generates the sleep score for the participants. The participants report their score to us and we make further analysis.

Since Jawbone Up is a comfortable and effortless bracelet [34], its small size and light weight make it hard to be felt by sleepers during sleep. Moreover, Sleep As Android is an app running on smartphone. The sleep environments of the 15 testing participants, therefore, are similar to those of the 45 training participants. Fig. 12 illustrates the experimental cases for testing and training respectively.

# 7.5 Micro-benchmarks

This section presents a set of micro-benchmarks that evaluate the performance of sleep stage detection. We also evaluate the effectiveness of feature and model in Sleep Hunter.

![](images/b1c62d8d50e3fdaa45852b7fce9a656561c61307e2e3fa3d7599aa2188cb143f.jpg)



Fig. 13. Sleep stage tracking of one user during a night

<table><tr><td rowspan="2">Ground Truth</td><td colspan="3">Predictions</td><td rowspan="2" colspan="2"></td></tr><tr><td>REM</td><td>Light Sleep</td><td>Deep Sleep</td></tr><tr><td>REM</td><td>538</td><td>206</td><td>39</td><td>68.71%</td><td rowspan="3">Recall</td></tr><tr><td>Light Sleep</td><td>246</td><td>630</td><td>77</td><td>66.11%</td></tr><tr><td>Deep Sleep</td><td>61</td><td>108</td><td>174</td><td>50.73%</td></tr><tr><td rowspan="2"></td><td>63.67%</td><td>66.74%</td><td>60.00%</td><td rowspan="2" colspan="2">64.55%Accuracy</td></tr><tr><td colspan="3">Precision</td></tr></table>

Fig. 14. Performance of sleep stage detection   
![](images/7854e9168face80f4bc0711cf6309f184af5e26a55c2997a1c98f7a969b966a6.jpg)



Fig. 15. Accumulative time error

# 7.5.1 Performance of Sleep Stage Detection

We measure the sleep stage detection performance of Sleep Hunter based on the testing dataset. The overall detection performance is shown in Fig. 14. The percentages in black blocks point to the precisions and recalls of the three types of sleep stages and the overall detection accuracy. The result of light sleep, whose precision reaches 66.74% and recall arrives at 68.71%, shows the outstanding detection performance. REM also exhibits satisfying detection performance. Its precision arrives at 63.67% and recall reaches 66.11%. The precision and recall of the deep sleep stage seem sightly weaker than those of the other stages. The values of these two indices are 60.00% and 50.73% respectively. We can explain this phenomenon by the values in the confusion matrix in Fig. 14. The values in white and grey blocks are the corresponding numbers of the three types of sleep stages in our testing data. We can learn the total amount of deep sleep is much less than REM and light sleep. It shows that the occurrence of deep sleep stage in the entire sleep process is much less than those of the other two sleep stages. Since the deep sleep happens rarely, it is harder for the classifier to learn a competitive result of this sleep stage than those of others. The values in grey blocks, however, still demonstrate that most sleep stages are detected accurately. The detection accuracy of system runs up to 64.55%, showing the overall detection performance of Sleep Hunter is satisfying.

Moreover, we also evaluate the accumulative time error of each sleep stage detected by Sleep Hunter over a whole sleep process.

Fig. 15 summarizes this kind of time error accumulated over the entire 6-9 hours of sleep based on our testing dataset. We can learn that 80% accumulative time errors of deep sleep stages stay under 45 minutes. The median error of this sleep stage is only around 25 minutes. Similarly, we also see that 80% accumulative time errors of REM are under 60 minutes and its median accumulative time error reaches about 30 minutes. The upper bound of the 80% accumulative time errors of light sleep arrives at around 75 minutes, which is the longest time in the three sleep stages. Its median error is around 50 minutes. Even though the precision and recall of deep sleep are little weaker than those of the others, its accumulative time error is the lowest in the sleep stages. It can also be explained that there are less occurrences of deep sleep than those of light sleep and REM during sleep. In Fig. 15, most accumulative time errors of the three sleep stages are shorter than one hour. Since the sleep duration lasts for 6 hours to 9 hours in the testing experiments, the fact of less than one hour accumulative time error demonstrates that the detection performance of Sleep Hunter is outstanding.

The accumulated time error reflects the overall performance of the detection scheme. For example, if a large portion of detection errors maintains in a small time interval (e.g., 20 minutes), then the user may have much confidence with the detection result of Sleep Hunter. Otherwise, if the detection errors maintain in a large time error, e.g., more than 90% errors are below 4 hours, given the typical overnight sleep is about 6 to 9 hours [32], users will lose confidence in the detection result.

Fig. 13 shows a user sleep tracking instance in our testing dataset. We carefully compared the detection results of Sleep Hunter with those of Zeo, which we regard as the ground truth. The sleep stage detection errors are labelled as the wrong zone in the last boxed line. The right zone indicates the right detection of Sleep Hunter. Since we regard wake stage as REM in Sleep Hunter, the wake stages detected by Zeo are labelled as REM in the ground truth.

In Fig. 13, we can observe that the detection errors occur frequently in the following two cases: one is during the transition of two different sleep stages, while the other is in the sleep stages with a short lifespan (i.e., less than 10 minutes). In the former case, as physical activities of sleepers do not occur immediately when a new sleep stage begins, Sleep Hunter may fail to realize the sleep transitions and make error predictions accordingly. For the sleep stages whose durations are short, physical features may not be displayed obviously, which cannot be sensed by Sleep Hunter and thus induces mistakes. Actually, this phenomenon is also consistent with the results of the testing experiments over 30 sets of nocturnal sleep data, which could be seen as the main sources of error in Sleep Hunter.

TABLE 5 Evaluation of sleep-related features 

<table><tr><td></td><td colspan="2">REM</td><td colspan="2">Light Sleep</td><td colspan="2">Deep Sleep</td></tr><tr><td>Features</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td></tr><tr><td>BM</td><td>39.62%</td><td>34.91%</td><td>37.84%</td><td>47.11%</td><td>30.12%</td><td>28.27%</td></tr><tr><td>BM+AE</td><td>45.41%</td><td>39.67%</td><td>47.83%</td><td>49.31%</td><td>38.34%</td><td>33.27%</td></tr><tr><td>BM+AE+IC</td><td>46.13%</td><td>41.81%</td><td>49.10%</td><td>52.27%</td><td>42.91%</td><td>35.84%</td></tr><tr><td>BM+AE+IC+SD</td><td>60.89%</td><td>67.99%</td><td>63.36%</td><td>59.15%</td><td>57.96%</td><td>46.53%</td></tr><tr><td>BM+AE+IC+SD+PF</td><td>63.67%</td><td>68.71%</td><td>66.74%</td><td>66.11%</td><td>60.00%</td><td>50.73%</td></tr></table>

![](images/a7b62123e53642897e2d05e7e9dbb32025639903c0ffbab504722da1afc45112.jpg)



Fig. 16. Detection precision and recall of HMM and CRF in different sleep stages

From Fig. 13, we can see that although Sleep Hunter makes misjudgement occasionally, it still obtains 57 right zones accounting for 285 minutes, which occupies nearly 70% lifespan of the sleep process.

Actually, Sleep Hunter detects the sleep stage by a statistical model, which integrates different sleep-related events and the inner dependency of sleep states into a whole comprehensively. When some data are missing, Sleep Hunter is also able to predict the current sleep stage based on other features.

# 7.5.2 Evaluation on Features

Table 5 exhibits the trend of detection performance by adding each feature incrementally. The contributions of features for classification are reliant on the design of feature functions in CRF, which predict hidden variables by incorporating observable features together. Apparently, with the increasing number of features, the precision and recall of each sleep stage of the CRF model improves, demonstrating the rationality of our configurations of the feature functions and selected features.

Since the sleep transition may vary a little bit from people to people, and the physiological features may also change with different peoples. Hence we collect data from people with different physical characteristics, with the goal of achieving a more robust detection model. Besides, we also regard the age as the one-dimensional feature when Sleep Hunter predicts the sleep stage. In the Table 5, we can see clearly that the detection performance of sleep stage has improved a lot by add this kind of feature.

# 7.5.3 Model Comparison

In order to justify the advantages of CRFs over HMMs in Sleep Hunter, we compare the detection accuracy of these two models in Fig. 16. We report the average detection results, including detection precision and recall in different sleep stages. From the Fig. 16, we can learn that CRFs outperforms HMMs in terms of the mean precision and mean recall over all the three sleep stages, which demonstrates the rationale of CRFs in Sleep Hunter.

TABLE 6 CPU share and processing time 

<table><tr><td>Phones</td><td>Body Movement</td><td>Acoustic Events</td><td>Light</td><td>Duration</td><td>CRF</td><td>Total</td><td>CPU Share</td></tr><tr><td>Galaxy S4</td><td>12.72s</td><td>77.75s</td><td>1.61s</td><td>0.69s</td><td>1.55s</td><td>79.00s</td><td>6%</td></tr><tr><td>Note2</td><td>12.21s</td><td>77.87s</td><td>1.87s</td><td>0.58s</td><td>1.63s</td><td>80.50s</td><td>5%</td></tr><tr><td>HTC G14</td><td>14.78s</td><td>80.12s</td><td>2.37s</td><td>1.02s</td><td>2.81s</td><td>82.93s</td><td>9%</td></tr><tr><td>MIUI 2SC</td><td>12.31s</td><td>78.19s</td><td>1.58s</td><td>0.59s</td><td>2.74s</td><td>80.90s</td><td>8%</td></tr></table>

<table><tr><td rowspan="2">Device\Stage</td><td colspan="2">Light Sleep</td><td colspan="2">Deep Sleep</td></tr><tr><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td></tr><tr><td>Sleep Hunter</td><td>66.74%</td><td>66.11%</td><td>60.00%</td><td>50.73%</td></tr><tr><td>Jawbone UP</td><td>37.74%</td><td>65.14%</td><td>34.62%</td><td>29.03%</td></tr><tr><td>Sleep As Android</td><td>25.71%</td><td>32.14%</td><td>36.36%</td><td>49.61%</td></tr></table>

Fig. 17. Performance comparison

From Fig. 16 we can see that the mean precision and 64.55% mean recall of CRF are higher than that of HMM in all of Accuracy three sleep stages. This is due to the better capability of CRF to depict the interdependence of sleep stage transitions and describe more features. Although the average improvement is about 5%, it is still significant regard to the limited features we can detect by off-the-shelf smartphones.

# 7.6 Macro-benchmarks

This section presents a set of macro-benchmarks that compare the performance of Sleep Hunter with other works.

# 7.6.1 Performance Comparison

To our best knowledge, there is no obvious baseline for the sleep stage detection performance in actigraphy-based work, and thus we compare the detection performance of Sleep Hunter with Jawbone Up and Sleep As Android, two representative actigraphy-based products monitoring sleep stage and having been widely used in the market. Since these two devices only detect the light sleep stage and the deep sleep stage, we compare these two with those of Zeo.

The average values of precision and recall of these products are calculated based on our testing dataset, which are shown in Fig. 17. Even though Sleep Hunter detects one more sleep stage than the other devices, its detection ability is still much better than the other two products, which clearly demonstrates that Sleep Hunter is superior to the existing actigraphy-based detection systems of sleep stage.

# 7.7 System Overhead

# 7.7.1 System Delay and CPU Share

In this section, we leverage four types of experimental smartphones to measure the system delay and the CPU share of Sleep Hunter. Since Sleep Hunter predicts the sleep stage every 5 minutes, it makes classification by the data recorded from each submodule in the last 5 minutes while it is running. Accordingly, the system delay is determined by the time cost to deal with the data in the last 5 minutes. As the personal factor submodule collects information from the user’s registration, we mainly analyze the time consumptions of other four submodules and the whole system. Table 6 illustrates the average delay of the corresponding submodules. The system delays for the smartphones range from 79s to 82.93s. Specifically, the acoustic event detection module occupies the major part of time consumption. Such cost is caused by parsing acoustic primitive data and computing its frequency spectrum. Given these submodules in the first layer run in parallel, the system delay of Sleep Hunter equals the largest time consumption of submodules in the first layer plus the time cost of the CRF model in the second layer. Since the sleep stage hardly changes in a short time (i.e., less than 2 minutes) and the smart call service could be provided as long as it lies in the wake-up period that lasts one hour in Sleep Hunter, the system delay around 80s makes little negative influence on the performance of our system.

IEEE TRANSACTIONS ON MOBILE COMPUTING.   
![](images/c0806b70fbcae2622b47566eb1a4659f4cf997f611061523f5260174fd92d7d6.jpg)



Fig. 18. Battery lifetime trace   
![](images/7fa1ad0384a4dcafbd69603342cf5dcd23e57d5ce93e2ddaba69facbe2a93748.jpg)



Fig. 19. Battery consumption distribution

Furthermore, we can observe that the CPU shares of Sleep Hunter with 4 types of smartphones in Table 6. The CPU share for G14 is little larger than those of other three smartphones, which may be caused by the different properties of CPU. Despite such a difference, the CPU share of Sleep Hunter stays stable from 5% to 9%, indicating that Sleep Hunter occupies negligible CPU resource for daily use.

# 7.7.2 Battery life

Considering the usage period of Sleep Hunter lasts for at least 5 hours, the battery consumption directly impacts its applicability. To record the battery conditions, a volunteer is asked to run Sleep Hunter on our four types of smartphones simultaneously from 23:00 to 7:00 next day. Since Sleep Hunter is a service that could run in backstage, we lock the screen during this process and shut down all the applications except Sleep Hunter and a battery tracing application, which is installed in each smartphone to record the rest battery storage every two hours. Fig. 18 illustrates the battery storage condition of the experimental smartphones. Based on the bar chart, each smartphone consumes around 10% on average every two hours. With time passing by, the power consumption increases gradually, and finally ends up at the level about 60%. As shown in the Fig. 18, the energy consumption rate, although varies a little bit with different devices, still maintains in a moderate level.

![](images/580e1ebc08b10592943839219e17be8fb47afee448b66080f313cbf22f2f2888.jpg)



Fig. 20. Sleep quality report   
![](images/35436bcf05e48d99f1c37225b67c8f51bb85f5e9c5db32b8db6f90bef8732b92.jpg)



Fig. 21. Smart call service

Further, since multiple threads (OS internal threads) may run in backend simultaneously, hence the result in the Fig. 18 cannot precisely depict the energy consumption of Sleep Hunter. Therefore, we further scrutinize the distribution of energy consumption in detail. The result is shown in the Fig. 19, which indicates that less than 40% of energy is caused by Sleep Hunter, and the most power is consumed by Android OS. Combining this result with the data shown in Fig. 18, Sleep Hunter only costs less than 4% power every two hours. Accordingly, the energy consumption of Sleep Hunter is not significant and the battery storage of most smartphones could be affordable for users to execute it during the whole sleep process.

# 7.8 Case study

# 7.8.1 Sleep Quality Report

Since sleep quality is determined by the percentage of different sleep stages during the whole sleep process, we can measure a user’s sleep quality by Sleep Hunter. We design a sleep quality measuring method based on the evaluation approach ‘ZQ’ of Zeo [35]. ‘SQ’ is a score shown in Eq. 2 for measuring the sleep quality of users in Sleep Hunter. Its structure and parameters are designed according to ‘ZQ’, where REM, Deep and Light represent their durations (minutes) in a sleep process. The range of ‘SQ’ is from 50 to 100.

$$
S Q = \left[ \frac {(R E M \times 0 . 5 + L i g h t \times 0 . 7 5 + D e e p) \times 1 0 0}{R E M + L i g h t + D e e p} \right] \tag {2}
$$

The right figure in Fig. 20 illustrates the average ‘SQ’ and ‘ZQ’ of 2 sets of nocturnal sleep data for the 15 users in the testing dataset. Though differences exist in the structures of ‘SQ’ and ‘ZQ’, the general variance trends of these two indices are correlated with the growth of age.

We analyze the sleep quality by ‘SQ’ in the following parts.

We observed that the occurrence of deep sleep is usually affected by its starting time and duration. According to our observation of the testing dataset, we figure out that if the deep sleep stage occurs in the first hour after the user falls asleep and lasts more than 10 minutes, the possibility of its recurrence is high and the sleep quality is usually appealing. Otherwise, the percentage of deep sleep would be low and the sleep quality is disappointing. The left figure in Fig. 20 shows the distribution of sleep stages in the two different conditions based on our testing dataset. Condition 1 stands for the distribution of sleep stages in a sleep process when the deep sleep stage occurs in the first hour and lasts for more than 10 minutes. Condition 2 represents the opposite case. Clearly, the percentage of deep sleep in Condition 1 is significantly larger than that in Condition 2. Based on Eq. 2, ‘SQ’ in Condition 2 is usually lower than that in Condition1. It reflects the fact that if a user cannot fall into deep sleep within one hour or remains in this stage in a short time, the user’s sleep quality will be low. Based on our knowledge of medical research [36], if the brain waves of a person remain rapid for a long time, it is hard for him/her to transform the fast brain waves to slow brain waves. It is because fast brain waves often make individuals excited, the long period excitement would disturb their normal rest habits.

TABLE 7 Performance of smart call service 

<table><tr><td>Case</td><td>Explanation</td><td>Sleep Hunter</td><td>Sleep Android</td><td>As</td></tr><tr><td>Case 1</td><td>There are actual some light sleep stages in the preset wake-up period and the app detects these light sleep stages rightly.</td><td>86.67%</td><td>42.33%</td><td></td></tr><tr><td>Case 2</td><td>There are actual some light sleep stages in the preset wake-up period but the app does not detect these light sleep stages in the right time or does not find any light sleep stages at all.</td><td>6.67%</td><td>36.33%</td><td></td></tr><tr><td>Case 3</td><td>There are no light sleep stage in the preset wake-up period actually but the app mistakes some other sleep stages as light sleep.</td><td>6.67%</td><td>21.33%</td><td></td></tr><tr><td>Case 4</td><td>There are no light sleep stage in the preset wake-up period actually and the app also does not find them.</td><td>0%</td><td>0%</td><td></td></tr></table>

As a point of interest, we also make an analysis on the relationship between age and sleep quality. From the right figure in Fig. 20, we observe that ‘SQ’ decreases with the increase of the age generally. More specifically, we find two rapid drops in Fig. 20. The first sudden drop occurs at the age of around 30. ‘SQ’ falls from the score around 75 to the score about 65. According to our observation, we think the 10-point drop stems from users’ work and family stress. At this age stage, most individuals have their own families to take care of and carry more workload than they used to do in school. High pressure, therefore, leads to the poor sleep quality. The second sudden drop occurs at the age of 40. ‘SQ’ slips from the score above 65 to the score near 55. It is likely that many users are approaching menopause during this age stage, when their physiological functions are experiencing changes. Some climacteric syndromes cause adverse impacts on the users and then decrease their sleep qualities. Given that the gender and career of the 15 participants in the testing dataset are different, our sleep quality report, therefore, is convincing and representative to some extent. We note that all conclusions are speculative based on our small sample size, but our observations are consistent with other sleep research studies [37], [38], [39].

According to the observations above, we could make two recommendations for users. 1) Since the beginning of sleep highly impacts the quality of the whole sleep process, people may benefit from light activities for relaxation before going to bed. For example, listening to some soft music, making several deep breaths or taking a warm bath can greatly help people relax before sleep. 2) People in their 30s are largely threatened by the pressure from work. Individuals at this age may benefit from some adjustments to achieve a greater balance between work and life. Seeking advice from more experienced people and cultivating a positive attitude may help them release some pressure off. For those at their 40s, health deals, moderate but habitual exercise could help them improve sleep quality.

We conduct the case study for the purpose of new findings with Sleep Hunter in practical usage. The findings in this case study are accordance with other medical science findings [37], [38], [39], which in turn verifies the accuracy and effectiveness of Sleep Hunter. On the other hand, since the data we used are collected from people with different age (10 to 60 years old), different weight, and different genders, we envision such comprehensive data incorporate human diversity and could reflect the result objectively.

# 7.8.2 Smart Call

Sleep Hunter can also provide smart wake-up services based upon the sleep stage detection, since individuals feel much more refreshed when they are woken up in light sleep. More specifically, during the light sleep, the sleepers brain waves and muscle activity are relaxed and slow. They drift in and out of sleep and thus can be awakened easily. It is the best time to wake the sleepers up. In the deep sleep stage or REM, the sleepers, however, do not adjust immediately and often feel groggy and disoriented for several minutes after they wake up [32], [36], [40], [41].

Users are allowed to set a one-hour period when they want to be woken, and then Sleep Hunter wakes the user up when it detects the current sleep stage is light sleep during the preset period. If Sleep Hunter detects no light sleep for the duration, it wakes users up at the end of this period. Fig. 21 depicts an illustration of a real smart call case in our testing experiments. The user sets the wake-up period from 6:30 a.m. to 7:30 a.m., and then Sleep Hunter will automatically wake the user up based on the detection result of sleep stages in the period. When Sleep Hunter detects that the user stays in a light sleep at 7:25 a.m., Sleep Hunter sings a soft song to wake him/her up.

We evaluate the smart call performance of Sleep Hunter and Sleep As Android by the users in our testing experiments. Each user is asked to select a wake-up period before going to bed. Table 7 gives the occurrence rates of these two apps under four different cases. Compared with

Sleep As Android, the larger occurrence rate in Case 1 and smaller occurrence rates in Case 2 and Case 3 show that the smart call service of Sleep Hunter performs much better. Moreover, 86.67% occurrence rate of Case 1 demonstrates that Sleep Hunter is able to provide the smart call service accurately. There are mainly two reasons behind this. The first one is the remarkable sleep stage detection performance of Sleep Hunter. The second one is that more light sleep stages and REM occur and less deep sleep stages happen during the latter period of sleep. Since Sleep Hunter has shown excellent detection performances of light sleep and REM, smart call service, therefore, exhibits outstanding.

# 8 RELATED WORK

In this section, we review the state-of-the-arts that are directly related to our work.

Polysomnography-based work: the polysomngraphy is regarded as the gold standard to measure the sleep quality in clinical field. It relies on certain biomedical signals such as brain wave, muscle tone and eye movement to assess the sleep quality. For example, most medical research works on sleep quality leverage electroencephalograph (EEG) to monitor brain waves and then recognize sleep stages. However, these polysomngraphy-based work usually requires to be assisted by the professional devices. For example, Zeo [5], which is a product based on EEG, leverages a brain wave sensor built in a headband to monitor sleeper’s electroencephalograph, and then the EEG recordings are sent to the user’s smartphone via Bluetooth. Zhang et al. [42] design a real-time system to monitor the user’s sleep condition. It ameliorates users’ sleep qualities by exploiting a pulse oximeter to detect the pulse oxygen saturation (SPO2) of the human body during their sleep processes. Such special equipment, professional technologies and expensive cost make them impractical for people in daily use. Compared with such works, Sleep Hunter concentrates on physical activities rather than biomedical signals. Moreover, it does not need special additional devices for detection.

Actigraphy-based work: actigraphy provides a simpler approach depends on physical activities to predict sleep quality. Compared with the polysomngraphy, it is much more convenient for people in daily use. iSleep [12] measures the sleep quality by recording some certain sleep-related acoustic events and evaluates it by the Pittsburgh Sleep Quality Index (PSQI) [2]. Bai et al. [43] predict the sleep quality by observing users’ daily activities with smartphones. The authors in [44] monitor sleep by the RFID sensors installed with accelerometers. Many Smartphone Apps such as Sleep As Android [8], Sleep Journal [45] and numerous consumer-oriented and wearable wrists including Jawbone Up [7], FitBit [46] predict sleep stages and measure sleep quality based on physical activities including body movement and snore. For example, when many body movements or acoustic events happen in a period, they regard the user stays in light sleep. On the contrary, the user is assumed to step into deep sleep as long as little body movement and ambient noise occur in the period.

Different from the simple rationale of these applications, Sleep Hunter incorporates sleep-relative events from different perspectives and leverages a statistical model to predict the sleep stage, which provides a fine-grained detection performance of sleep stages without any assistant devices. Moreover, compared with the wearable intelligent wrists, Sleep Hunter does not require users to wear, providing a non-intrusive method for free use.

# 9 CONCLUSION

Recent advances in sensor technology and machine learning technique empower machine to intelligently understand human behaviors. This paper guides this opportunity into an application that automatically detects sleep stage transitions of sleepers for sleep quality monitoring. The core idea is to leverage built-in sensors on commodity phones to sense sleep-related events, and further predict the dwelling time of each sleep stage by a statistical model based on these observable events. We implement Sleep Hunter on Android platform and test it with data collected over 30 sets of nocturnal sleep data. The results show that our system achieves desirable detection accuracy.

# 10 ACKNOWLEDGE

This work is supported in part by the NSFC Major Program 61190110, NSFC under grant 61171067, National Basic Research Program of China (973) under grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under Grant 61125202, and Beijing Nova Program under grant Z151100000315090.

# REFERENCES

[1] M. Langkvist, L. Karlsson, and A. Loutfi, “Sleep stage classification ¨ using unsupervised feature learning,” Advances in Artificial Neural Systems, vol. 2012, p. 5, 2012.   
[2] J. S. Carpenter and M. A. Andrykowski, “Psychometric evaluation of the pittsburgh sleep quality index,” Journal of psychosomatic research, vol. 45, no. 1, pp. 5–13, 1998.   
[3] J. Trinder, J. Kleiman, M. Carrington, S. Smith, S. Breen, N. Tan, and Y. Kim, “Autonomic activity during human sleep as a function of time and sleep stage,” Journal of sleep research, vol. 10, no. 4, pp. 253–264, 2001.   
[4] “Polysomnography,” http://en.wikipedia.org/wiki/ Polysomnography.   
[5] “Zeo Sleep Manager Pro,” http://www.digifit.com/Zeo/.   
[6] “Actigraphy,” http://en.wikipedia.org/wiki/Actigraphy.   
[7] “Jawbone Up,” https://jawbone.com/up.   
[8] “Sleep As Android,” https://play.google.com/store/apps/ details?id=com.urbandroid.sleep&hl=zh EN.   
[9] W. Webb and H. Agnew, “Sleep stage characteristics of long and short sleepers.” Science, 1970.   
[10] S. Ancoli-Israel, R. Cole, C. Alessi, M. Chambers, W. Moorcroft, and C. Pollak, “The role of actigraphy in the study of sleep and circadian rhythms. american academy of sleep medicine review paper,” Sleep, vol. 26, no. 3, pp. 342–392, 2003.   
[11] G. Jean-Louis, D. F. Kripke, S. Ancoli-Israel, M. R. Klauber, and R. S. Sepulveda, “Sleep duration, illumination, and activity patterns in a population sample: effects of gender and ethnicity,” Biological psychiatry, vol. 47, no. 10, pp. 921–927, 2000.   
[12] T. Hao, G. Xing, and G. Zhou, “isleep: unobtrusive sleep quality monitoring using smartphones,” in Proceedings of the 11th ACM Conference on Embedded Networked Sensor Systems. ACM, 2013, p. 4.

[13] H. Lu, W. Pan, N. D. Lane, T. Choudhury, and A. T. Campbell, “Soundsense: scalable sound sensing for people-centric applications on mobile phones,” in Proceedings of the 7th international conference on Mobile systems, applications, and services. ACM, 2009, pp. 165–178.   
[14] D. Li, I. K. Sethi, N. Dimitrova, and T. McGee, “Classification of general audio data for content-based retrieval,” Pattern recognition letters, vol. 22, no. 5, pp. 533–544, 2001.   
[15] J. Saunders, “Real-time discrimination of broadcast speech/music,” in Acoustics, Speech, and Signal Processing, 1996. ICASSP-96 Vol 2. Conference Proceedings., 1996 IEEE International Conference on, vol. 2, no. 2. IEEE, 1996, pp. 993–996.   
[16] D. Boswell, “Introduction to support vector machines,” 2002.   
[17] R. Kohavi et al., “A study of cross-validation and bootstrap for accuracy estimation and model selection,” in IJCAI, vol. 14, no. 2, 1995, pp. 1137–1145.   
[18] C. Goutte and E. Gaussier, “A probabilistic interpretation of precision, recall and f-score, with implication for evaluation,” in Advances in information retrieval. Springer, 2005, pp. 345–359.   
[19] K. L. Lichstein, H. H. Durrence, B. W. Riedel, D. J. Taylor, and A. J. Bush, Epidemiology of sleep: Age, gender, and ethnicity. Psychology Press, 2004.   
[20] M. M. Ohayon, M. A. Carskadon, C. Guilleminault, and M. V. Vitiello, “Meta-analysis of quantitative sleep parameters from childhood to old age in healthy individuals: developing normative sleep values across the human lifespan,” SLEEP-NEW YORK THEN WESTCHESTER-, vol. 27, pp. 1255–1274, 2004.   
[21] M. A. Carskadon, W. C. Dement et al., “Normal human sleep: an overview,” Principles and practice of sleep medicine, vol. 4, pp. 13–23, 2000.   
[22] J. Lafferty, A. McCallum, and F. C. Pereira, “Conditional random fields: Probabilistic models for segmenting and labeling sequence data,” 2001.   
[23] E. Fosler-Lussier, Y. He, P. Jyothi, and R. Prabhavalkar, “Conditional random fields in speech, audio, and language processing,” Proceedings of the IEEE, vol. 101, no. 5, pp. 1054–1075, 2013.   
[24] E. C. Larson, M. Goel, G. Boriello, S. Heltshe, M. Rosenfeld, and S. N. Patel, “Spirosmart: Using a microphone to measure lung function on a mobile phone,” in Proceedings of the 2012 ACM Conference on Ubiquitous Computing. ACM, 2012, pp. 280–289.   
[25] L. Rabiner and B.-H. Juang, “An introduction to hidden markov models,” ASSP Magazine, IEEE, vol. 3, no. 1, pp. 4–16, 1986.   
[26] I. J. Myung, “Tutorial on maximum likelihood estimation,” Journal of Mathematical Psychology, vol. 47, no. 1, pp. 90–100, 2003.   
[27] A. Skajaa, “Limited memory bfgs for nonsmooth optimization,” Master’s thesis, 2010.   
[28] G. D. Forney Jr, “The viterbi algorithm,” Proceedings of the IEEE, vol. 61, no. 3, pp. 268–278, 1973.   
[29] J. R. Shambroom, S. E. Fabregas, and J. Johnstone, “Validation of an automated wireless system to monitor sleep in healthy adults,” Journal of Sleep Research, vol. 21, no. 2, pp. 221–230, 2012.   
[30] E. Oropesa, H. L. Cycon, and M. Jobert, “Sleep stage classification using wavelet transform and neural network,” International computer science institute, 1999.   
[31] F. Ebrahimi, M. Mikaeili, E. Estrada, and H. Nazeran, “Automatic sleep stage classification based on eeg signals by using neural networks and wavelet packet coefficients,” in Engineering in Medicine and Biology Society, 2008. EMBS 2008. 30th Annual International Conference of the IEEE. IEEE, 2008, pp. 1151–1154.   
[32] “Sleep,” http://en.wikipedia.org/wiki/Sleep.   
[33] D. M. Hawkins, “The problem of overfitting,” Journal of chemical information and computer sciences, vol. 44, no. 1, pp. 1–12, 2004.   
[34] “Jawbone Up review: An easy-to-wear and insightful fitness pal,” http://www.cnet.com/products/jawbone-up/.   
[35] “Whats Your Bulletproof ZQ Score? The Zeo Hack Every Sleep Hacker Needs To Know,” http://www.bulletproofexec.com/ zeo-hack/.   
[36] M. Beloved, Meditation Pictorial. Michael Beloved, 2011.   
[37] Y. Q. J. C. Marquie, J. Foret, “Effects of age, working hours, and job content on sleep: a pilot study,” Experimental aging research, vol. 25, no. 4, pp. 421–427, 1999.   
[38] P. Polo-Kantola, R. Erkkola, K. Irjala, H. Helenius, S. Pullinen, and O. Polo, “Climacteric symptoms and sleep quality,” Climacteric, vol. 2, no. 4, pp. 293–294, 1999.   
[39] P. Eichling and J. Sahni, “Menopause related sleep disorders,” J Clin Sleep Med, vol. 1, no. 3, pp. 291–300, 2005.

[40] K. Lovell and C. Liszewski, “Normal sleep patterns.”   
[41] M. A. Carskadon and A. Rechtschaffen, “Monitoring and staging human sleep,” Principles and practice of sleep medicine, vol. 3, pp. 1359–1377, 2000.   
[42] J. Zhang, Q. Zhang, Y. Wang, and C. Qiu, “A real-time auto-adjustable smart pillow system for sleep apnea detection and treatment,” in Proceedings of the 12th international conference on Information processing in sensor networks. ACM, 2013, pp. 179–190.   
[43] Y. Bai, B. Xu, Y. Ma, G. Sun, and Y. Zhao, “Will you have a good sleep tonight?: sleep quality prediction with mobile phone,” in Proceedings of the 7th International Conference on Body Area Networks. ICST (Institute for Computer Sciences, Social-Informatics and Telecommunications Engineering), 2012, pp. 124–130.   
[44] E. Hoque, R. F. Dickerson, and J. A. Stankovic, “Monitoring body positions and movements during sleep using wisps,” in Wireless Health 2010. ACM, 2010, pp. 44–53.   
[45] “Sleep Journal App,” http://sleeptrackerapp.blogspot.com/.   
[46] “FitBit,” http://www.fitbit.com.

![](images/3eaa9155c7958c1d4cf03b0cf43f09ac7f14b28a062a8d82c874ad231b55b366.jpg)



Weixi Gu is currently a master student in the School of Software, Tsinghua University. He received the B.E. degree in 2012 from the College of Information Security, Shanghai Jiaotong University. He is a student member of IEEE and ACM.

![](images/3b10c331dd403cf4138f2175bab3ecab47c8661a6fc35892db0dc712ff50a1e5.jpg)



Zheng Yang is currently an Assistant Professor in the School of Software of Tsinghua University. He received his B.E. degree in the Department of Computer Science from Tsinghua University, Beijing, China, and his Ph.D. degree in the Department of Computer Science and Engineering of Hong Kong University of Science and Technology. He is a member of IEEE and ACM. He has been awarded the 2011 State Natural Science Award (second class).

![](images/84cbdd637f46e0bc8d18ef1adebab0e8cd820ec8e9abf55dc8eb1388fd98b1e2.jpg)



Longfei Shangguan is currently a Research Associate in the School of Software, Tsinghua University. He received the B.E. degree from Xidian University in 2011, the MS and PhD degrees from from Hong Kong University of Science and Technology in 2013 and 2015, respectively. He is a student member of IEEE and ACM.

![](images/98a6f138d4c2e26b16406d20bcc13996a2af552b540808a6f279c440b997d7a0.jpg)



Yunhao Liu received the B.E. degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now a professor at TNLIST, School of Software, Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a fellow of the IEEE Computer Society and an ACM Distinguished Speaker.