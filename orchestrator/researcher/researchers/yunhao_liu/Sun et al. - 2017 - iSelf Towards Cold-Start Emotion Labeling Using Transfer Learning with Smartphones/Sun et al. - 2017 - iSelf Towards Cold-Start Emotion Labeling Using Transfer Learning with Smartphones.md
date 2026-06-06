# iSelf: Towards Cold-Start Emotion Labeling Using Transfer Learning with Smartphones

BOYUAN SUN and QIANG MA, Tsinghua University, ACM Member

SHANFENG ZHANG, Google, ACM Member

KEBIN LIU, Tsinghua University, ACM Member

YUNHAO LIU, Tsinghua University, ACM Fellow

It has been a consensus that a certain relationship exists between personal emotions and usage pattern of the smartphone. Based on users’ emotions and personalities, more and more applications are developed to provide intelligent automation services on the smartphone, such as music recommendations or stranger introductions on social networking sites. Most existing work studies this relationship by learning large amounts of samples, which are manually labeled and collected from smartphone users. The manual labeling process, however, is very time-consuming and labor-intensive. To address this issue, we propose iSelf, a system that provides a general service of automatic detection of a user’s emotions in cold-start conditions with a smartphone. With the technology of transfer learning, iSelf achieves high accuracy given only a few labeled samples. We also embed a hybrid public/personal inference engine and validation system into iSelf, to make it maintain updates continuously. Through extensive experiments in real traces, the inferring accuracy is tested above 74% and can be improved increasingly through validation and updates. The application program interface has been open online for other developers.

CCS Concepts: • Computer Applications → Mobile Applications; • Computing Methodologies → Artificial Intelligence; • Information Technology and Systems → Models and Principles;

Additional Key Words and Phrases: Emotion label, transfer learning, cold-start system

# ACM Reference format:

Boyuan Sun, Qiang Ma, Shanfeng Zhang, Kebin Liu, and Yunhao Liu. 2017. iSelf: Towards Cold-Start Emotion Labeling Using Transfer Learning with Smartphones. ACM Trans. Sen. Netw. 13, 4, Article 30 (September 2017), 22 pages.

https://doi.org/10.1145/3121049

# 1 INTRODUCTION

Nowadays, with the rapid development of mobile communication and sensor technology (Li et al. 2011), the capability of the smartphone has become very powerful. By utilizing various functions, the smartphone can bring us a lot of convenience. For example, the location-based service can provide people accurate weather report or advertisement according to the location; the music player can play hundreds of songs anytime. These services can be implemented easily with the built-in equipment on smartphones. More and more applications, however, provide services based

This research was supported in part by the NSFC program under Grants No. 61472219, No. 61672372, and No. 61472218.

Authors’ addresses: B. Sun, Q. Ma (corresponding author), S. Zhang, K. Liu, and Y. Liu, Room 11-232, East Main Building, Tsinghua University, Beijing, China; emails: {boyuan, maq, shanfeng, kebin, yunhao}@greenorbs.com.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored.

Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2017 ACM 1550-4859/2017/09-ART30 \$15.00

https://doi.org/10.1145/3121049

![](images/d9ef2d2ab8a08394d9a5a5c8d1250c1c50a5352ca4c0d1f4e5c3a0d5c827c5cb.jpg)



![](images/152f08588d03ccd007bc9943faa77c986f123b26d03f1382335e9760f423d4a1.jpg)



Fig. 1. The growth trend of emotion-related applications in the online App Market for Android OS and iOS.

on human emotion or personality, which cannot be measured directly (Liu et al. 2012). For instance, the music player recommends users music list according to their current emotional state; social networking sites (SNS) introduce appropriate strangers according to people’s personality (Li and Lui 2011). As shown in Figure 1, for both Android OS and iOS, there have been more than 55% of such emotion-related applications developed in online App Market in 2014.

Compared to manual input, a general service of automatic detection of a user’s emotion is much more practical. Several recent studies have investigated personal emotion and personality traits and proved that smartphone users’ moods and emotions can be reflected by usage pattern. Most of them study this relationship by learning many labeled samples collected from the users. These training samples include two parts: (1) usage pattern of smartphone, such as call logs, short message service (SMS) logs, application usage logs, and so on, and (2) corresponding label of emotion. The labeled samples are leveraged to train an emotion classifier through some learning approaches, such as multi-linear regression (LiKamWa et al. 2013), support vector machine (SVM) (Chittaranjan et al. 2013; de Montjoye et al. 2013), C4.5 (Chittaranjan et al. 2011), and so on.

Generally speaking, to guarantee a high accuracy, an efficient and valid classifier requires a big data set for training. For example, the authors in LiKamWa et al. (2013) leverage a training set including 32 iPhone users’ daily usage reports for more than two months. Note that, to obtain these samples is non-trivial. Although some background services are available for automatically collecting usage patterns, the labeling process must be done manually in the form of field study (LiKamWa et al. 2013) or personality questionnaire (Chittaranjan et al. 2011), which is time-consuming, laborintensive, and money-consuming. Moreover, even if we collect large amounts of labeled samples to train a classifier, unlike other recognition scenarios, such as image recognition, there must be some feature spaces absent in the training set. For these human behaviors, even a strong classifier may become invalid and fail to infer users’ emotions.

To address these issues, we propose iSelf, a system that can infer personal emotions automatically in cold-start conditions (i.e., with only a few labeled samples) on smartphone. iSelf collects three kinds of data: event data (e.g., calls and applications), sensor data (e.g., WiFi), and content data (e.g., SMS content). To measure the similarity between different usage patterns, iSelf conducts feature extraction for these raw data. By utilizing this feature similarity, iSelf realizes the featurebased transfer learning to infer emotions. To increase iSelf’s inference accuracy, we validate the correctness of labeling results in two ways: automatic validation by overhearing emotion input and querying with minimal feedback using active learning. We also propose a hybrid public/personal inference engine that trains a personal classifier using the ground-truth data collected from the validation. In addition, iSelf updates the public/personal inference model to ensure continuous improvement of performance.

The main contributions of this article are summarized as follows:

— To the best of our knowledge, this work is the first to consider the cold-start problem of inferring personal emotions with smartphone.   
—We design iSelf, a system that can infer personal emotions automatically with only a few labeled samples using transfer learning technology on smartphone.   
—We propose a validation method to check the correctness of inference in two ways: automatic validation by overhearing emotion input and querying with minimal feedback using active learning.   
—We conduct extensive experiments with more than 3,600 samples of 10 participants during 30 days. iSelf achieves an inference accuracy of 75% and costs less than 2% of daily power consumption. We also offer an available API for iSelf for the developers.

The rest of the article is organized as follows. In Section 2, we introduce the related work. In Section 3, we describe the system overview. Section 4 presents the detailed design of iSelf. We demonstrate the implementation, dataset collection, experiment results, and discussions in Section 5. The conclusion is presented in Section 6.

# 2 RELATED WORK

This section surveys the existing methods (LiKamWa et al. 2013; Chittaranjan et al. 2013; de Montjoye et al. 2013; Chittaranjan et al. 2011; Church et al. 2010; Clark and Watson 1988; Manevitz and Yousef 2002; Forgas et al. 1984) for emotion recognition. We classify the existing approaches into two categories: (1) based on the relationship between human emotions and usage pattern of smartphone, (2) with the help of other equipment, such as video camera and facial features. Then, we introduce the related work about transfer-learning (Pan et al. 2008; Hu and Yang 2011; Dai et al. 2008).

# 2.1 Emotion Definition

Emotions are difficult to define and measure. It attracts studies from not only psychology but also neuroscience, sociology, philosophy, anthropology, and biology. After reviewing 92 definitions, Kleigninna proposed the definition trying to reach the best agreement: “Emotion is a complex set of interactions among subjective and objective factors, mediated by neural/hormonal systems, which can (1) give rise to affective experiences such as feelings of arousal, pleasure/displeasure; (2) generate cognitive processes such as perceptually relevant effects, appraisals, labeling processes; (3) activate widespread physiological adjustments to the arousing conditions; and (4) lead to behavior that is often, but not always, expressive, goal-directed, and adaptive” (LiKamWa et al. 2013; Chittaranjan et al. 2011; Laurier 2011; de Montjoye et al. 2013). So, we can see that emotion sometimes is a transient reaction, such as surprise, and may be influenced by a special event.

# 2.2 Emotion Recognition through Smartphone Usage

A number of works (LiKamWa et al. 2013; Chittaranjan et al. 2013; de Montjoye et al. 2013; Chittaranjan et al. 2011; Church et al. 2010) mainly focus on recognizing emotions using smartphone usage patterns. MoodScope (LiKamWa et al. 2013) proposes to infer mood based on how smartphone is used. The authors conducted a user study lasting for more than two months with 32 iPhone users. Similarly, other systems (Chittaranjan et al. 2013, 2011; de Montjoye et al. 2013) utilize phone usage patterns to infer personality. Beside a large amount effort in collecting user patterns, they use questionnaires to label the data. In Chittaranjan et al. (2011), the data is collected from 83 individuals over a continuous period of 8 months, and TIPI (Gosling et al. 2003) questionnaire is leveraged to determine the Big-five personality traits. In these approaches, data collection is time-consuming and labor-intensive. In contrast, iSelf conducts both data collection and labeling procedure automatically using only a few samples as trigger. In addition, iSelf increases detection accuracy continuously through validation and update. Also researchers utilize smartphones to detect emotion-related attributes. Sandstrom et al. (2016) uses smartphones to examine how people feel in different locations and analysis of how people feel in different locations. iSelf uses location data to help detect emotion as well. Lane et al. (2014) introduces a smartphone application to monitor, model, and promote wellbeing utilizing three sensors: global positioning system (GPS), accelerometer, and microphone. In our article, GPS and accelerometer are also used.

# 2.3 Emotion Recognition with Extra Equipments

In this category, most of existing works utilize visual (Wang et al. 2014) and acoustic (Lee and Narayanan 2005; Schuller et al. 2005) signals to extract speech, actions, and facial features. For example, Mood Meter (Hernandez et al. 2012) counts smiles using video cameras. Others (Gluhak et al. 2007; Cohn 2006) use physical signals, such as skin conductance, heart rate, breath rate, blood pressure, and skin temperature. But these methods require additional hardware. In practice, these approaches are not suitable to our scenario due to the heavy sensing and computational burden. In contrast, iSelf only utilizes the usage patterns rather than sampling new signals. Meanwhile, iSelf avoids invasive image and audio data, such that it can run continuously in the background without compromising battery life.

# 2.4 Related work on Transfer Learning

There have been some studies (Pan et al. 2008; Hu and Yang 2011; Dai et al. 2008) about transfer learning. In Pan et al. (2008), the author proposes a new dimensionality reduction method to find a latent space minimizing the distance between distributions of data in different domains. In this article, the approach to transfer learning is verified by experiments in two real-world applications: indoor WiFi localization and binary text classification. And in Hu and Yang (2011), the author proposes a transfer learning framework based on automatically learning a bridge between different sets of sensors to solve the activity recognition problem using transfer-learning technology.

# 3 SYSTEM OVERVIEW

In this section, we present the system architecture of iSelf. As shown in Figure 2, iSelf consists of two parts: mobile client and cloud server. On the mobile client, iSelf infers emotion using the user’s smartphone usage patterns. On the server side, iSelf receives the ground-truth queue and updates the models. Finally, the mobile client downloads the new models. Next, we describe each module in details.

# 3.1 Data Collection Module

Each data collection lasts for 1h. Generally, iSelf collects three kinds of data: event data, sensor data, and content data. Event data include call logs, SMS logs, and applications usage logs. Sensor data include activity states, location information, BT (BlueTooth) logs, and WiFi signals. To save the power, iSelf collects the sensor data every 10min and each collection lasts 5min. Content data include SMS contents, online SNS contents, and browser contents. For privacy issues, we keep the content data on the mobile client.

# 3.2 Feature Extraction Module

For event data, iSelf counts the number of each attribute such as the number of outgoing calls. For sensor data, iSelf transforms the multidimensional data into only one dimension. Take acceleration data, for example, iSelf transforms the three-dimensional raw data to user’s activity state, including silence, run, and walk, by analyzing the activity patterns. For content data, iSelf extracts the adjective, noun, and emoticons and then analyzes them using semantic analyze technology. More details are described in Section 4B.

![](images/427477feadc0e1b99fd02b39e792e8bc91e1de970e20c3a3c8aff022997bb11f.jpg)



Fig. 2. System Architecture.

# 3.3 Inference Module

We use the Circumplex emotion model (Russell 1980), like MoodScope (LiKamWa et al. 2013). As shown in Figure 3, the Circumplex model consists of two fundamental neurophysiological dimensions: a pleasure-displeasure dimension and an active-inactive dimension. Each emotion can be considered as a combination of these two dimensions (Church et al. 2010). We choose a set of standard and representative emotions: sad, happy, angry, content, energetic, and tense.

iSelf needs to be initialized with a small data set of labeled usage patterns. We collect data from 10 participants, covering all the six basic emotions. After feature extraction, we divide all the samples into six sets according to their labels.

iSelf contains two inference engines: public and personal. At the beginning, only public inference engine works, which is built with samples of all involved users by transfer learning. Personal inference is an inference engine constituted for a specific user. After collecting enough labeled data for each user, iSelf utilizes SVM (Manevitz and Yousef 2002) to train the personal model to infer his/her emotions.

![](images/7e8e3ebff011d978bec2a76af059ed8a251a34a085e6344d001f9ee24be69cfb.jpg)



Fig. 3. Circumplex Emotion Model.

# 3.4 Validation Module

iSelf validates the correctness of the result if either of two circumstances happens. One is that iSelf overhears users’ inputs of their own emotions when they use some apps. The other is that iSelf measures the uncertainty and queries the user with minimal intervention. iSelf selects the first way preferentially. If iSelf gets the ground-truth label, which is different from the inferred label, then iSelf puts the ground-truth to a queue and sends it to the cloud server. Otherwise, iSelf triggers the next inference.

# 3.5 Update Module

This module is deployed on the cloud server. When the cloud server receives the ground-truth queue, iSelf puts it to the corresponding emotion set in source domain and re-trains the personal classifier to get a stronger emotion model. When monitoring the Wi-Fi environment and idle state of smartphone, for example, at night when the user is sleeping, iSelf downloads the new models.

# 4 SYSTEM DESIGN

In this section, we present the design of iSelf in details. At first, we only have a few samples collected from 10 participants. Then, we utilize the transfer learning technique to automatically label the input usage pattern. After collecting enough labeled data, iSelf trains a personal classifier to help recognize emotions. Before training, iSelf validates the correctness of inferred emotions. Finally, iSelf increases detecting accuracy by updating models.

# 4.1 Data Collection

We build iSelf’s input feature vector using the usage records collected by the logger. It has been suggested by the literature that emotion is strongly related with the social interaction (Forgas et al. 1984) and daily activity (Clark and Watson 1988) of a person. Our collected data belong to both of them.

Feature Vector: Every data collection lasts 1h. Here, we ignore the instantaneous emotion persisting for less than 30s. Emotion inference is based on the data collected in this 1h. We collect three kinds of data: event data, sensor data, and content data. At the beginning, iSelf explores the user’s smartphone usage history to make sure the unique contacts by calculating the number and duration of the communication. As a matter of fact, the confidence of the inference through these contacts is very high. iSelf regards the top 10 call numbers and top 20 SMS numbers as the unique contacts. We design a background service to collect these three kinds of data. Table 1 shows the data types required in detail. Here, iSelf collects sensor data every 10min and every collection lasts 5min to save the battery power. These three kinds of data are combined as the input feature vector.

# 4.2 Feature Extraction

Before combining these three kinds of data, an important step is feature extraction. For event data, we count the number of each attribute. For sensor data, we handle the data of accelerometer and location (GPS). For accelerometer, we extract the feature of the raw data stream to get the state of people including run, walk, and silence. We approximate the force exerted by people as follows: $H F = { \sqrt { A c c e { l _ { x } } ^ { 2 } + A c c e { l _ { y } } ^ { 2 } + A c c e { l _ { z } } ^ { 2 } - G ( G r a v i t y ) } }$ . We define two thresholds, AccelThreshold1 and AccelThreshold2, where AccelThreshold1  AccelThreshold2. We assume the state is run if the HF is <greater than AccelThreshold2. The state is walk if HF is greater than AccelThreshold1 and less than AccelThreshold2. The state is silence when the HF is less than AccelThreshold1. Then, we change the raw data stream to the state stream. In our experiments, AccelThreshold1 is 0.7 and AccelThreshold2 is 1.47. For location, we cluster our time-series of location data through the DBSCAN (Ester et al. 1996), which allows us to get the visited locations. In DBSCAN, The min points is 120 and distance variables is 30m. For content data, we divide the content into textual data and emoticons. We extract the adjective and noun from the text and convert the emoticons into corresponding emotional text. Table 2 shows the partial converting rules.

Finally, we classify them into three categories according to data type. They are statistical data (SD), stream flow data (SF), and textual data (TD), corresponding to event data, sensor data, and content data, respectively.

# 4.3 Automatically Label

We adopt the transfer learning technology (Hu and Yang 2011) to realize the automatic labeling. To formalize the labeling problem, we define the labeled samples collected from 10 participants in the form of $( x _ { s } , y _ { s } )$ , where $x _ { s }$ means labeled feature vector, $y _ { s }$ means emotion label, and s means ,source domain. Then, we define the new unlabeled input feature vector as $x _ { t }$ , where t means target domain. What we want to know is the corresponding $y _ { t } , y _ { s }$ and $y _ { t }$ belong to the same label space $L ,$ which includes {sad, happy, angry, content, energetic, tense}. But, $x _ { s }$ and $x _ { t }$ are not in the same feature space, because different people have different smartphone usage patterns under the same emotion. Our final goal is to estimate $p ( \boldsymbol { y } _ { t } | \boldsymbol { x } _ { t } )$ . By transfer learning (Hu and Yang 2011), we have

$$
p (y _ {t} | x _ {t}) = \sum_ {\mathbf {c} ^ {(i)} \in L} p (y _ {t} | \mathbf {c}) p (\mathbf {c} | x _ {t}). \tag {1}
$$

Table 1. Feature Vector 

<table><tr><td>Date Style</td><td>Date Type</td><td>Usage Cue</td></tr><tr><td rowspan="3">Event Data</td><td>Calls</td><td>No. of outgoing callsNo. of incoming callsduration of each callNo. of top 10 contacts calledNo. of top 10 contacts who calledNo. of missed calls</td></tr><tr><td>SMS</td><td>No. of SMS receivedNo. of SMS sentNo. of Top 20 contacts received fromNo. of Top 20 contacts sent to</td></tr><tr><td>Application</td><td>No. of uses of Office AppsNo. of uses of Email AppsNo. of uses of Video/Music AppsNo. of uses of Chat Apps: Wechat,etcNo. of uses of SMS AppNo. of uses of Camera AppNo. of uses of Map appNo. of uses of GamesThe time of each app used</td></tr><tr><td rowspan="4">Sensor Data</td><td>Accelerometer</td><td>X,Y,Z Accelerator</td></tr><tr><td>GPS</td><td>Altitude, latitude, longitudeThe time of locations collected</td></tr><tr><td>Bluetooth</td><td>No. of BT IDsBT IDs for more than 3 time slotsMax. time for a BT ID seen</td></tr><tr><td>Wifi</td><td>No.of Wifi signals in each time slot</td></tr><tr><td rowspan="3">Content Data</td><td>SMS content</td><td>Average length of SMSContent of each SMS</td></tr><tr><td>Online SNS</td><td>Key WordsExpression tags</td></tr><tr><td>Browser</td><td>Browser Search contentBrowser Bookmarks content</td></tr></table>

Since the label space $L _ { s }$ and $L _ { t }$ are small. In the future, if the label space become large, we can simplify the Equation (1) by approximating the value of $\dot { \boldsymbol p } ( \boldsymbol y _ { t } | \boldsymbol x _ { t } )$ . Then, we get Equation (2). In this article, we just use the Equation (1):

$$
p (y _ {t} | x _ {t}) \approx p (y _ {t} | \hat {\mathbf {c}}) p (\hat {\mathbf {c}} | x _ {t}) \quad (\hat {\mathbf {c}} = a r g m a x _ {\mathbf {c} \in L} p (\mathbf {c} | x _ {t})). \tag {2}
$$

From the above equation, the automatic labeling takes two steps. First, to estimate every $\scriptstyle p ( \mathbf { c } | x _ { t } )$ , where c is labeled using the source domain label space. In other words, we aim to use the source domain label space to label the target domain feature space $x _ { t }$ . The target domain feature space may be much different from the source domain feature space and unseen before. So, first, we need to transfer across different feature spaces. What follows is to calculate $p ( \boldsymbol { y } _ { t } | \hat { \mathbf { c } } )$ .

Transfer Across Feature Vectors: As discussed above, we need to transfer the knowledge between different feature vectors and estimate $\mathinner { p \mathopen { \left( y _ { t } \vert \mathbf { c } \right) } }$ . For each feature vector $x _ { s }$ in the source domain $S , x _ { s }$ is represented by features $f _ { s }$ . For the new reading vector $x _ { t }$ in the target domain $^ { \mathrm { T , } }$ the features are represented as $f _ { t } . f _ { s }$ is the labeled samples from 10 participants, while $f _ { t }$ is the unseen smartphone usage patterns from other people. $f _ { s }$ and $f _ { t }$ are much different, because people have different usage habits. Even for one person, the usage patterns may vary dramatically. So what we should do is to build a bridge between $f _ { s }$ and $f _ { t }$ . We use a framework similar to translated learning (Dai et al. 2008). The challenge now is to find a translator $T ( f _ { s } , f _ { t } ) \propto p ( f _ { t } | f _ { s } )$ . Due to $p ( f _ { t } | f _ { s } ) = p ( f _ { t } , f _ { s } ) / p ( f _ { s } )$ , we focus on $p ( f _ { t } , f _ { s } )$ :

Table 2. Convert Rule 

<table><tr><td>happy</td><td>(^_^) (*^_^*) (^o^) (^.^)</td></tr><tr><td>sad</td><td>(T_T) (T.T) (T^T) ()</td></tr><tr><td>angry</td><td>(&gt;^&lt;) (&gt; _ &lt;)</td></tr><tr><td>content</td><td>(~^~) &lt; (~)~) &gt; &lt; (-v-) &gt;</td></tr><tr><td>tense</td><td>o_O (@^@) (;;;;;</td></tr><tr><td>energetic</td><td>N/A</td></tr></table>

$$
p (f _ {t}, f _ {s}) = \int_ {\mathcal {X} _ {s}} p (f _ {t} | x _ {s}, f _ {s}) p (f _ {s} | x _ {s}) p (x _ {s}) d _ {x _ {s}}. \tag {3}
$$

If $x _ { s } , f _ { s }$ , and $f _ { t }$ are independent, then Equation (3) can be rewritten as

$$
p (f _ {t}, f _ {s}) = \int_ {\chi_ {s}} p (f _ {t} | x _ {s}) p (f _ {s} | x _ {s}) p (x _ {s}) d _ {x _ {s}} \tag {4}
$$

$$
= \int_ {\mathcal {X} _ {s}} p (f _ {t}, x _ {s}) p (f _ {s} | x _ {s}) d _ {x _ {s}}. \tag {5}
$$

To measure $p ( f _ { t } , f _ { s } ) , p ( f _ { t } , x _ { s } )$ is necessary. In other words, we need to measure the relationship , ,between the input feature vector and feature vectors $x _ { s }$ from source domain. Because the feature vector has three data categories, we measure $p ( f _ { t } , x _ { s } )$ according to different category. Then, we can convert $p ( f _ { t } , x _ { s } )$ into the following equations:

$$
p (f _ {t} ^ {S D}, x _ {s} ^ {S D}) = \frac {\sum_ {f _ {t} ^ {(i)} \in S D _ {t}} \sum_ {x _ {s} ^ {(j)} \in S D _ {s}} p (f _ {t} ^ {(i)} , x _ {s} ^ {(j)})}{| S D _ {t} | | S D _ {s} |}, \tag {6}
$$

$$
p (f _ {t} ^ {S F}, x _ {s} ^ {S F}) = \frac {\sum_ {f _ {t} ^ {(i)} \in S F _ {t}} \sum_ {x _ {s} ^ {(j)} \in S F _ {s}} p (f _ {t} ^ {(i)} , x _ {s} ^ {(j)})}{| S F _ {t} | | S F _ {s} |}, \tag {7}
$$

$$
p (f _ {t} ^ {T D}, x _ {s} ^ {T D}) = \frac {\sum_ {f _ {t} ^ {(i)} \in T D _ {t}} \sum_ {x _ {s} ^ {(j)} \in T D _ {s}} p (f _ {t} ^ {(i)} , x _ {s} ^ {(j)})}{| T D _ {t} | | T D _ {s} |}, \tag {8}
$$

$$
p (f _ {t}, x _ {s}) \approx \frac {p (f _ {t} ^ {S D} , x _ {s} ^ {S D}) + p (f _ {t} ^ {S F} , x _ {s} ^ {S F}) + p (f _ {t} ^ {T D} , x _ {s} ^ {T D})}{3}, \tag {9}
$$

where $S D _ { t }$ is the feature set belonging to statistical data type of target domain and $S D _ { s }$ means the same data type of the source domain. $S F _ { s } , S F _ { t } , T D _ { S }$ , and $T D _ { t }$ are defined similarly. Instead of measuring $p ( f _ { t } , x _ { s } )$ directly, we calculate $\smash { p ( f _ { t } ^ { S D } , x _ { s } ^ { S D } ) , p ( f _ { t } ^ { S F } , x _ { s } ^ { S F } ) }$ F , and $\mathfrak { p } ( f _ { t } ^ { T D } , x _ { s } ^ { \mathbf { \Upsilon } _ { T D } } )$ , respectively. , , , ,We use Jeffrey’s J-divergence (Jeffreys 1946) (the symmetric version of KL-divergence) to approximate $p ( f _ { t } ^ { S D } , x _ { s } ^ { S D } )$ , Dynamic Time Warping (DTW) (Keogh and Pazzani 2000) to approximate $p ( f _ { t } ^ { S F } , x _ { s } ^ { S F } )$ , , and Cosine similarity (Singhal 2001) to approximate $\mathfrak { p } ( f _ { t } ^ { T D } , x _ { s } ^ { \mathbf { \Upsilon } _ { T D } } )$ s T D ).

,To measure cations. Take $p ( f _ { t } ^ { S D } , x _ { s } ^ { S D } )$ ,, we estimate each probability distribution in calls, SMS, andmple, we simply estimate the probability p(OutдoinдCalls) as $\frac { \bar { N } \bar { O } C } { N C }$ where N OC means the number of outgoing calls and N C means the number of calls. Similarly, we can estimate p(IncominдCalls), p(Top10ContactsCalled), and p(Top10ContactsW hoCalled). For SMS and applications, we adopt the same method to estimate their probability distributions. We define the estimated distribution as ${ \mathcal { A } } ,$ , and we wish to find a close distribution B in the source domain. Since $D _ { K L } ( \mathcal { A } | | \mathcal { B } )$ is not equal to $D _ { K L } ( { \mathcal { B } } | | { \mathcal { A } } )$ , we use $D _ { K L } ( \mathcal { A } | | \mathcal { B } ) + D _ { K L } ( \mathcal { B } | | \mathcal { A } )$ instead, which is undoubtedly symmetric. As a definition of J-divergence, the more similar A and B are, the lower the value of $D _ { K L } ( \mathcal { A } | | \mathcal { B } ) + D _ { K L } ( \mathcal { B } | | \mathcal { A } )$ is. So, we only consider distribution pairs at low divergence values.

To measure $\ d _ { p } ( f _ { t } ^ { S F } , x _ { s } ^ { S F } )$ , we first normalize all the stream-flow data readings into the range ,of [0,1]. Then, we consider the sampling rates of different data types may be different such as the activity state stream and the Wi-Fi signals. To solve this problem, we choose a distance metric that can take different sampling rates into account. Now, given two series of sensor readings of only one dimension, such as activity state stream and Wi-Fi signals: M and N of length m and n; we use DTW (Keogh and Pazzani 2000) to measure the similarity of M and N . DTW uses dynamic programming to calculate the matching cost of two time series and find the optimal path. The optimal path from (1,1) to (i,j) must be included in the optimal paths from (1,1) to the three predecessor candidates include (i-1,j), (i-1,j-1), and (i,j-1). Then, the matching cost from (1,1) to $( \mathrm { i } , \mathrm { j } )$ is the distance at (i,j), adding the smallest one of these three candidates. The time and space complexity of DTW are both O (M ∗ N ). The smaller the calculated distance is, the more similar M and N are. So, we only select the low DTW values.

To measure $p ( f _ { t } ^ { T D } , x _ { s } ^ { \ T D } )$ , we extract the emoticons, adjectives, and nouns and convert them ,into scores between [−1,1] using SentiWordNet (Baccianella et al. 2010). We construct a vector $W = \left\{ W _ { 1 } , W _ { 2 } , W _ { 3 } , W _ { 4 } , W _ { 5 } \right\}$ , where $W _ { i }$ means the number of words with scores belonging to [−1 + $( \mathrm { i } - 1 )  \ ^ { \star } \ 0 . 4 , - 1 + \mathrm { i } \ ^ { \star } \ 0 . 4 ]$ . Similarity between $f _ { t } ^ { { T D } }$ and ${ x _ { s } } ^ { T D }$ is calculated using Equation (10):

$$
\text { similarity } = \cos (\theta) = \frac {W _ {t} \cdot W _ {s}}{| | W _ {t} | | \cdot | | W _ {s} | |}, \tag {10}
$$

where $W _ { t }$ and $W _ { s }$ are the vectors of $f _ { t } ^ { T D }$ D and xs T D . ${ x _ { s } } ^ { T D }$

After estimating $\scriptstyle { p ( \mathbf { c } | x _ { t } ) }$ , we calculate $\mathinner { p \mathopen { \left( y _ { t } \vert \mathbf { c } \right) } }$ . If $y _ { t } = \mathbf { c }$ , then $p ( y _ { t } | \mathbf { c } ) = 1$ , and if $y _ { t } \neq \mathbf { c } _ { : }$ , then $p ( y _ { t } | \mathbf { c } ) = 0$ . Then, we finish the automatic labeling. Figure 4 shows the steps of automatic labeling.

# 4.4 Validation

There are two ways for validating the correction of inferred emotion: (1) Automatic Validation: iSelf overhears users’ input of their own emotions; (2) Query with Minimal Feedback: iSelf utilizes active learning method to realize minimal user feedback. There is no user intervention in the first way at all.

Automatic Validation: iSelf overhears users’ inputs of their own emotions. When users use some applications such as music player and SNS, they may input their emotions as a query (e.g., Moodagent) or share with others (e.g., Facebook), which can be overheard by iSelf as the groundtruth. In each slot, iSelf collects a series of user’s input emotions as $E = \{ e _ { 1 } , e _ { 2 } , e _ { 3 } , \ldots , e _ { n } \}$ . Then it calculates the similarity $S ( e _ { i } | y )$ , where $e _ { i } \in E$ , , , . . . ,and y ∈ {sad happy anдry content enerдetic , , , , ,tense}. Since different users’input from the basic emotions may have the same semantic meaning, we utilize SentiWordNet (Baccianella et al. 2010) to calculate the scores of these emotion words and measure the similarity by comparing the scores. iSelf takes the basic emotion with the most occurrences as the ground-truth.

Reinforce Recognition Using Minimal Feedback: When no input about emotion is overheard, iSelf asks users to label the usage pattern. Obviously, it is impractical to query a user every time. The more frequently iSelf asks users, the more intrusive the system is. To address this issue, we use the idea of active learning to measure the uncertainty of a sample through calculating maximum entropy. The equation $\begin{array} { r } { E _ { m } ( Y | x _ { t } ) = - \sum _ { y _ { t } } \mathcal { P } _ { m } ( y _ { t } | x _ { t } ) l o g \phi _ { m } ( y _ { t } | x _ { t } ) } \end{array}$ means the uncertainty the classifier is about the value of label Y given a feature vector $x _ { t }$ and classifier model m. We define a threshold e, and iSelf asks user for a ground-truth label when $E _ { m } ( Y | x _ { t } )$ is not less than e.

![](images/5985fe2d722b59c8d74058fce914ea00abf132dd80d0690be14e8326e9f73c34.jpg)



Fig. 4. Automatic Labeling.

The complete algorithm is shown in Algorithm 1. If the inferred emotion is wrong, then iSelf puts the ground-truth into a queue and sends it to the cloud server for real-time updating.

# 4.5 Hybrid Public/Personal Inference Engine

While utilizing transfer learning method to recognize a user’s emotion, there are certain amounts of useful information in the target feature space that we do not want to discard. A period of time later, for example, one week, for a specific user, many usage patterns with ground-truth label are collected through validation. With the help of these records, iSelf can improve the detection accuracy for this person. Thus, we propose a hybrid public/personal inference method. Public inference is the inference engine utilizing transfer learning method to infer emotions for everyone. Personal inference is an inference engine constituted for a specific user.

To build personal inference engine, our idea is to save the previous labeled usage patterns and train a personal classifier. To infer a specific user’s emotions, if a feature vector belongs to the same feature space with the classifier, we can directly apply the personal classifier. Otherwise, we use transfer learning method.

After the training sets are constructed, a binary classifier is trained for each basic emotion. If the emotion only has a few samples or does not have any sample, then iSelf does not train a classifier for this emotion. Compared with various classifiers, we select the Support Vector Machine (SVM) classifier (Manevitz and Yousef 2002; Chang and Lin 2011). SVM searches the hyperplane $\mathbf { w } ^ { T } \mathbf { x } _ { i } + b = 0$ that maximizes the margin between points from different labels by optimizing the

ALGORITHM 1: Validation   
Require: Collected feature vector $x_t$ ; Inferred emotion label $y_t$ ; An initial classifier model $m$ ; Defined threshold $e$ ;

Ensure: Ground-truth emotion $E_g$ 1: Define a emotion set $E$ 2: while iSelf Service is running do
3:    if iSelf overhears a user's input about emotion then
4:    iSelf put the emotion $e_i$ into $E$ 5:    end if
6:    if size of $E$ is equal to 0 then
7: $E_m(Y|x_t) = -\sum_{y_t} p_m(y_t|x_t) logp_m(y_t|x_t)$ 8:    if $E_m(Y|x_t) \geq e$ then
9: $E_g \leftarrow queryForLabel(x_t)$ 10:    else
11: $E_g \leftarrow NULL$ 12:    end if
13:    else
14:    Calculate Similarity $S(e_i|y)$ 15:    Map $E$ to the six basic emotions
16:    Take the emotion with most occurrences as $E_g$ 17:    end if
18: end while
19: return $E_g$

following Quadratic Programming equation:

$$
\min _ {w, b, \xi} \frac {1}{2} | | w | | ^ {2} + C \sum_ {i = 1} ^ {n} \xi_ {i}, \tag {11}
$$

$$
s. t. a _ {i} (w ^ {T} \mathbf {x} _ {i} + b) \geq 1 - \xi_ {i}, \tag {12}
$$

$$
\xi_ {i} \geq 0, \forall i, \tag {13}
$$

where $\mathbf { x } _ { i }$ and $a _ { i }$ are the feature vector and label value for the ith training sample; w and b controls the offset and orientation of the hyperplane; C refers to a regularization term used to control the overfitting and the false classification tolerance $\xi _ { i }$ for each sample.

After training a classifier for each basic emotion, how can iSelf know if a feature vector belongs to a seen feature space? We develop an “anomaly” detector. If a feature vector is from a seen feature space, then it is similar to the samples in the personal training set. Otherwise, the feature vector is different. To detect an “anomaly,” we first train an unseen feature space detector using the oneclass SVM classifier (Manevitz and Yousef 2002; Chang and Lin 2011). All the usage patterns of a user collected by iSelf as the positive samples (no negative samples) are trained to get a personal classifier for this user to detect if the feature space is unseen. The complete algorithm of hybrid public/personal inference is shown in Algorithm 2.

# 4.6 Update

After validation, iSelf sends the ground-truth queue to the cloud server and then updates the public source domain as well as the personal classifier only in Wifi environment to reduce mobile network data traffic. First, iSelf puts the usage patterns to the source domain sets. It increases the possibility that classifies the similar usage patterns to the truth emotion. Second, iSelf adds the queue to the personal training samples to re-train a stronger personal classifier. For this user, the personal SVM classifier can be more accurate next time. After updating these two parts, iSelf sends the new models back to the mobile client.

ALGORITHM 2: Hybrid Public/Personal Inference   
Require: feature vector $x_{t}$ Ensure: inferred emotion $y_{t}$ 1: isUnseen ← UnseenFeatureSpaceDetection( $x_{t}$ );
2: if isUnseen = true then
3: $y_{t} \leftarrow$ Automatic-Labeling;
4: else
5: $y_{t} \leftarrow$ PersonalSVMClassifier( $x_{t}$ );
6: end if
7: return $y_{t}$

# 5 EVALUATION

# 5.1 System Implementation

We have implemented iSelf system on Samsung Galaxy Note One, which has a three-dimensional accelerometer, Wi-Fi, Bluetooth, GPS, and other basic equipment. The system runs on the Android OS2.3.3. We implemented the code for data collection, feature extraction, automatic labeling, validation, hybrid classification, and update. We also built a cloud server on Sina App Engine in Java. The SVM classifier was implemented using the LibSVM library (Chang and Lin 2011).

# 5.2 Datasets

We collect participants’ mobile usage patterns, including event data, sensor data, and content data for 1h every time, and ask them to label the corresponding emotions. 10 participants (4 females and 6 males) install the service and collect about 3,600 records for 30 days. They are undergraduates, postgraduate, and common IT workers aged from 20 to 40. The features used with iSelf are collected using an application programmed by ourselves. We wrote an Android application collecting mobile usage patterns of participants in background. Once launched, this application pops up a list with six basic emotions every hour to remind users of reporting their emotions during this hour. Thus a bridge of features and emotions is built using our data-collecting app. We regard these labeled usage patterns as the original source domain.

# 5.3 Evaluation Methodology

We use the leave-M-out validation method to examine iSelf’s inference accuracy. Each time we take M from N persons as target and the rest N − M persons as source. We test all $\binom { N } { M }$ target/source combinations. Three metrics are evaluated, which are defined as follows:

$$
P r e c i s i o n = \frac {T P}{T P + F P} \quad R e c a l l = \frac {T P}{T P + F N}, \tag {14}
$$

$$
F 1 - \text { score } = \frac {2 \cdot \text { Precision } \cdot \text { Recall }}{\text { Precision } + \text { Recall }}, \tag {15}
$$

![](images/68097997a36cf3b6dea15e70dd7a7cb8ac07b4219580d3775f7a08ae710af340.jpg)



Fig. 5. Inference Accuracy.

![](images/3487d06f52b4e256ff70e45f43c65fe683a67c10327968448337eddd0b168b2a.jpg)



Fig. 6. Precision, Recall and F1-Score.

where TP, FP, TN, and FN means true positive, false positive, true negative, and false negative, respectively. Precision means the percentage of correct emotion inference made by the system. Recall is the percentage of an emotion detected. F1-score means the combination of them. For iSelf’s inference accuracy, it is calculated as the number of correct inferred emotions divided by the number of all the test samples.

# 5.4 System Performance

5.4.1 Inference Accuracy. We set M = 2. Figure 5 shows the accuracy of iSelf and Figure 6 shows the corresponding precision, recall, and f1-score. The overall accuracy is 77.4% and F1-score is 76.4% over all emotions. Three emotions including happy, content, and sad reach a promising accuracy and F1-score of over 80%. The tense has the minimal accuracy of about 60% and happy is the highest one about 90%. These results support our theory that unseen feature space can be labeled automatically through transfer learning technology.

Another observation from the experimental result is that misclassification usually happens when two feature spaces of one emotion have a very large difference. We discover that usage patterns vary much when people are tense and this leads to low inference accuracy.

5.4.2 Inference Accuracy Variation of Single User. As time goes on, the accuracy of single user increases due to continued validation processes. Through validation, the specific SVM classifier becomes more robust with just a few days. Figure 8 shows the accuracy variation of a user in

![](images/82edf0a85eeda034ee64fb7b42d39ecd197c625f8e18cbeddf985a150d485d84.jpg)



Fig. 7. Inference Accuracy of Three Categories.

![](images/78e601062f0fb9b31ccfd9d98d1eef764d7e12c86fa8f921e96376df06917f94.jpg)



Fig. 8. Accuracy Variation of Validation.

10 days and the accuracy without validation. In the first 4 days, the performances are almost the same. From the 5th day, the accuracy with validation increases dramatically. This is because there are not enough samples to train a personal SVM classifier in the first 4 days.

5.4.3 Influence of Three Categories. We evaluate the sensor data, event data, and content data individually. When we test iSelf, one of three categories is chosen to infer emotions and record the accuracy of each emotion. As shown in Figure 7, we find that content data plays a crucial role in inferring emotions followed by event data. Both content data and event data can infer emotions individually. It is common sense that content data contains much emotion information. Meanwhile, event data has relevance with emotions. However, sensor data has the weakest capabilities to infer emotions.

5.4.4 Inference Latency. Before each inference, iSelf collects data for 1h. Then iSelf determines whether the feature vector is seen or unseen. If seen and SVM classifier exists, then feature vector is sent to the personal SVM classifier directly. Otherwise, iSelf performs feature-space transfer to infer the emotions. Choosing the methods to infer emotions takes about 150ms, in general. Transferring takes longer, about 450ms, when personal SVM classifier takes about 200ms. So the whole inference process takes about 150 + (450 + 200)/2 = 475ms.

Table 3. System Overhead 

<table><tr><td>Data Collection(once/hour)</td><td></td></tr><tr><td>Power Consumption</td><td>110 mW</td></tr><tr><td>Computation Time</td><td>109 ms</td></tr><tr><td>Pre-processing(once/hour)</td><td></td></tr><tr><td>Power Consumption</td><td>122 mW</td></tr><tr><td>Computation Time</td><td>1.7 s</td></tr><tr><td>Inference(once/hour)</td><td></td></tr><tr><td>Power Consumption</td><td>246 mW</td></tr><tr><td>Computation Time</td><td>464 ms</td></tr><tr><td>Interaction(once/day)</td><td></td></tr><tr><td>Data Upload</td><td>2MB</td></tr><tr><td>Data Download</td><td>10KB</td></tr><tr><td>Power Consumption</td><td>3036 mW</td></tr><tr><td>Time to send/receive</td><td>2.3 s</td></tr></table>

5.4.5 System Overhead. Since training and updating the emotion model are conducted offline on the cloud server, we mainly consider the power consumption of emotion inference. iSelf occupies only 4.6M storage when it is running. Then, we measure the energy consumption of data collection, pre-processing, inference, and interaction with server. Meanwhile, we also test the size of files uploaded to and downloaded from the server. All the results are displayed in Table 3.

We obtain the system power consumption of Galaxy Note One using a resistor put in series with the battery. We evaluate iSelf in different environments where the number of WiFi APs and Bluetooth is different. We measure the average consumption in each environment and choose the maxim as the final result. As we can see, the power consumption is less than 500mW during data collection, pre-processing, and inference. In a whole day, iSelf costs less than 2% of a phone’s total power consumption.

Although iSelf needs to open sensors and monitor the running events and input content during data collection, it conducts this every 10min. So, in fact, data collection costs a little energy. Feature Extraction is also lightweight, only involving the data transformation and DBSCAN clustering (Liu et al. 2010; Yu et al. 2013). Inference contains hybrid public/personal emotion detection and validation. Since transferring needs some computation, inference costs more power, which reaches 246mW. Finally, iSelf must upload the entire usage log and download a new specific SVM model.

# 5.5 Impact of Different Parameters

In this part, we measure the impact of different parameters on inference accuracy.

Impact of Parameter N in automatic labeling: We set M = 2 and report the detecting accuracy of iSelf by varying the parameter N in Figure 4. We select the top-N similar SD distributions and top-N minimum SF DTW scores, as well as top-N similar TD contents, a total of 3N input feature vectors and corresponding labels. The result in Figure 9 shows that the accuracy increases as in direct proportion to N . This is because more candidate labels are taken into account and thus we can consider more “probabilities.” However, when N is larger than 25, the accuracy drops slightly due to the noise impact.

Impact of M: Let N = 10. We set M from 2 to 9, where M means the number of target persons, and check the impact of number of unseen persons. The results are shown in Figure 10. As we can see, when the number of seen persons is equal or greater than 7, the accuracy stays constant. The system can maintain an accuracy of over 65% when there are only 6 seen persons. When there is only 1 seen person, the detecting accuracy drops to 11.2%. Overall, iSelf can achieve approximately 20–30% better accuracy than the baseline if four or more persons are seen.

![](images/914cfad16d382963cb22abcb34bbd802bc79d0823e81318972abf814929bffaf.jpg)



Fig. 9. Impact Of N in automatic labeling.

![](images/8b7626451f501a16d93fefb3b61a3f40af8f4d33927320846ded7e59678bb117.jpg)



Fig. 10. Impact of M, the number of testing persons.

# 5.6 Comparison of Different Personal Detectors

We also compare the SVM classifier used in personal inference with other classifiers that are widely used, including the Decision Tree classifier, k-Nearest Neighbor (k-NN) classifier and Naive Bayes classifier. For k-NN, we set k = 4 as the optimal choice.

In the experiments, we set M = 2, N = 10 and choose samples that are classified as seen by the “anomaly” detector. The results are shown in Figure 11. SVM outperforms the Naive Bayes classifier and Decision Tree for all six basic emotions. k-NN is comparable to SVM. However, k-NN needs to save and access to all the training data. Thus, k-NN is less practical to run on mobile devices with limited storage.

# 5.7 Generalization Ability Evaluation of iSelf

We utilize all data from ten participants to build our iSelf service system. In other words, we set M = 0. Then, we install our test application with iSelf service to Smartphones of 100 participants and ask them to use this application in eight weeks. They are recruited from undergraduates, postgraduates, and common IT workers from 20 to 40 years old. Among them, 30 are our schoolmates in our laboratory, and 70 from IT companies that have cooperation with our lab.

![](images/69fb1eb201ce9fad077f0b532e355539ae60a97eba9652d4c0115e0dabbf415a.jpg)



Fig. 11. Comparison of different classifiers for personal inference.

These 100 participants consist of 47 females and 53 males, including 14 undergraduates, 16 postgraduates, and 70 IT workers. We spent 3 dollars for each student and 5 dollars for each IT worker, totalling 440 dollars. The test application offers the user the emotion labels every other hour and the user can determine whether labels are right. Test application sends results to our server every week, and Figure 13 shows the total accuracy and its tendency. As shown in Figure 13, accuracy of iSelf is about 74% in the first four weeks and reaches about 80% in the remaining four weeks. This result proves the generalization ability of iSelf.

Our test app infers emotions every 1h, from 10 a.m. to 10 p.m. Thus, 672 inferred emotion labels are provided per user. We record the inferred labels and the validated labels per user. We calculate average distributions according to gender. Figure 12 shows the distributions of six basic emotions of inferred labels. As shown in Figure 12, the emotion inferred and validated labels of happy and sad have the highest proportion about 20% and accuracy about 80%. We can conclude that happy and sad are the most common emotions in our daily life and features of them are very distinguishable. Then tense and energetic labels show very low proportion and accuracy. It accords with occurrence frequency of emotions.

# 5.8 Application Programming Interface

iSelf exposes an API for developers to use. Knowledge about psychology or machine learning is not necessary for developers. Table 4 shows the API. Other applications can use iSelf to add emotion detecting function. Like a music player application, it can automatically recommend music to users according to the emotion.

# 5.9 Case Study: Analyze Inherent Reason of Results

5.9.1 Same Emotion can Cause Similar SD or SF. It is obvious that contents data sometimes can express explicit emotions. For example, a user sends a message like, “I was punished by my teacher this afternoon. What a sad day!” We can infer that this user is angry or sad. Such messages can help iSelf improve recognizing accuracy. But most of the time, iSelf only has SD or SF or SD+SF. Can iSelf infer emotions correctly without TD information? Through the experiments, we discover that if a user expresses an emotion with the (SD or SF)+TD, the user expresses a similar emotion if he/she only has the similar SD or SF. So, we conclude that the same emotion can cause similar SD or SF with over 65% probability.

![](images/cca9fc3872c6472f5cf3e20b57e329c4fd69194a90723fde6da1db24681641d4.jpg)



(a) Distribution of inferred emotion labels

![](images/0db47cda1abfcb2be7024ff0b773629b4b79f37aacf4c8ae25c2d62ac7a2f9be.jpg)



(b) Distribution of validated emotion labels

Fig. 12. Distribution of inferred and validated emotion labels.   
![](images/3264aa339113497c162cf459dcb928ba95feac5711d3cdfe10e3ff8dfd2bed94.jpg)



Fig. 13. Generalization ability evaluation of iSelf.

Table 4. iSelf API Specification 

<table><tr><td>Interface</td><td>Description</td></tr><tr><td>StartEmotionService</td><td>Start a background service and collect usage patterns</td></tr><tr><td>GetCurrentEmotion</td><td>Return current emotion</td></tr><tr><td>StopEmotionService</td><td>Stop the background service</td></tr><tr><td>GetPastEmotion(time)</td><td>Return the emotion of the give timestamp</td></tr></table>

![](images/95d16ebb32d59e511733188c013eb5253b23e61a29222c0a2dadc6ba051b976b.jpg)



Fig. 14. Distribution of User Emotions.

5.9.2 Emotion Distribution. We also analyze the distribution of emotions. As shown in Figure 14: 38.2% of emotion labels are happy; 19.7% of emotion labels are content; 8.9% of emotion labels are sad; 10.8% of emotion labels are angry; 11.3% of emotion labels are tense; the rest of the labels are energetic. We discover that people are most likely to consider themselves positive rather than negative.

5.9.3 Interesting Things. We find most people have more calls or SMS when they are happy or sad. When they are happy, people are usually outdoors (Wi-Fi) or crowded by others (Bluetooth). But when they are sad, people are always indoors or alone. We consider people prefer to stay alone when they are sad. We also discover that people are usually content or happy when they use the camera application. People are likely to be angry or tense when they use the music player application. Then people are always energetic when the activity state is running or more locations are visited.

# 6 CONCLUSION

In this article, we have shown the design, implementation, and evaluation of iSelf, a system that automatically infers emotions while the feature space is unseen before. Previous works can only infer emotions with the seen input feature space leading to time-consuming, labor-intensive and money-consuming collection, and labeling. iSelf leverages transfer learning technology to infer emotions though the input feature space is unseen. We only need to collect a little labeled data from several people and it saves time, labor, and money. Also, previous works get lower accuracy if the input feature space is unseen and iSelf solves this problem. Validation is developed in two ways to improve the performance with minimal user feedback. iSelf achieved up to an average of 75% inference accuracy on the unseen feature space.

# REFERENCES

Stefano Baccianella, Andrea Esuli, and Fabrizio Sebastiani. 2010. SentiWordNet 3.0: An enhanced lexical resource for sentiment analysis and opinion mining. In Proceedings of ELRA LREC.   
Chih-Chung Chang and Chih-Jen Lin. 2011. LIBSVM: A library for support vector machines. ACM Trans. Intell. Syst. Technol. (TIST) 2, 3 (2011), 27.   
Gokul Chittaranjan, Jan Blom, and Daniel Gatica-Perez. 2011. Who’s who with big-five: Analyzing and classifying personality traits with smartphones. In Proceedings of IEEE ISWC.   
Gokul Chittaranjan, Jan Blom, and Daniel Gatica-Perez. 2013. Mining large-scale smartphone data for personality studies. Person. Ubiq. Comput. 17, 3 (2013), 433–450.   
Karen Church, Eve E. Hoggan, and Nuria Oliver. 2010. A study of mobile mood awareness and communication through mobimood. In Proceedings of ACM NordiCHI.   
Lee A. Clark and David Watson. 1988. Mood and the mundane: Relations between daily life events and self-reported mood. J. Person. Soc. Psychol. 54, 2 (1988), 296.   
Jeffrey F. Cohn. 2006. Foundations of human computing: Facial expression and emotion. In Proceedings of ACM ICMI.   
Wenyuan Dai, Yuqiang Chen, Gui-Rong Xue, Qiang Yang, and Yong Yu. 2008. Translated learning: Transfer learning across different feature spaces. In Proceedings of ACM NIPS.   
Yves-Alexandre de Montjoye, Jordi Quoidbach, Florent Robic, and Alex Sandy Pentland. 2013. Predicting personality using novel mobile phone-based metrics. In Proceedings of LNCS SBP.   
Martin Ester, Hans-Peter Kriegel, Jörg Sander, and Xiaowei Xu. 1996. A density-based algorithm for discovering clusters in large spatial databases with noise. In Proceedings of ACM KDD.   
Joseph P. Forgas, Gordon H. Bower, and Susan E. Krantz. 1984. The influence of mood on perceptions of social interactions. J. Exp. Soc. Psychol. 20, 6 (1984), 497–513.   
Alexander Gluhak, Mirko Presser, L. Zhu, S. Esfandiyari, and S. Kupschick. 2007. Towards mood based mobile services and applications. In Proceedings of ACM EuroSSC.   
Samuel D. Gosling, Peter J. Rentfrow, and William B. Swann Jr. 2003. A very brief measure of the big-five personality domains. J. Res. Personal. 37, 6 (2003), 504–528.   
Javier Hernandez, Mohammed E. Hoque, Will Drevo, and Rosalind W. Picard. 2012. Mood meter: Counting smiles in the wild. In Proceedings of ACM UbiComp.   
Derek Hao Hu and Qiang Yang. 2011. Transfer learning for activity recognition via sensor mapping. In Proceedings of ACM IJCAI.   
Harold Jeffreys. 1946. An invariant form for the prior probability in estimation problems. Proc. Roy. Soc. London. Series A. Math. Phys. Sci. 186, 1007 (1946), 453–461.   
Eamonn J. Keogh and Michael J. Pazzani. 2000. Scaling up dynamic time warping for datamining applications. In Proceedings of ACM KDD.   
Nicholas D. Lane, Mu Lin, Mashfiqui Mohammod, Xiaochao Yang, Hong Lu, Giuseppe Cardone, Shahid Ali, Afsaneh Doryab, Ethan Berke, Andrew T. Campbell, and Tanzeem Choudhury. 2014. BeWell: Sensing sleep, physical activities and social interactions to promote wellbeing. MONET (2014).   
Cyril Laurier. 2011. Automatic Classification of Musical Mood by Content Based Analysis. Universitat Pompeu Fabra.   
Chul Min Lee and Shrikanth S. Narayanan. 2005. Toward detecting emotions in spoken dialogs. IEEE Trans. Speech Audio Process. 13, 2 (2005), 293–303.   
Yongkun Li and John C. S. Lui. 2011. Friends or foes: Detecting dishonest recommenders in online social networks. In Proceedings of IEEE ICCCN.   
Zhenjiang Li, Mo Li, Jiliang Wang, and Zhichao Cao. 2011. Ubiquitous data collection for mobile users in wireless sensor networks. In Proceedings of IEEE INFOCOM.   
Robert LiKamWa, Yunxin Liu, Nicholas D. Lane, and Lin Zhong. 2013. MoodScope: Building a mood sensor from smartphone usage patterns. In Proceedings of ACM MobiSys.   
Siyuan Liu, Yunhuai Liu, Lionel M. Ni, Jianping Fan, and Minglu Li. 2010. Towards mobility-based clustering. In Proceedings of the 16th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Washington, DC, July 25–28, 2010. 919–928. DOI:http://dx.doi.org/10.1145/1835804.1835920   
Zimu Liu, Yuan Feng, and Baochun Li. 2012. Socialize spontaneously with mobile applications. In Proceedings of IEEE INFOCOM.   
Larry M. Manevitz and Malik Yousef. 2002. One-class SVMs for document classification. J. Mach. Learn. Res. 2 (2002), 139–154.   
Sinno Jialin Pan, James T. Kwok, and Qiang Yang. 2008. Transfer learning via dimensionality reduction. In Proceedings of the 23rd AAAI Conference on Artificial Intelligence (AAAI’08). 677–682.   
James A. Russell. 1980. A circumplex model of affect.J. Personal. Soc. Psychol. 39, 6 (1980), 1161.

Gillian M. Sandstrom, Neal Lathia, Cecilia Mascolo, and Peter J. Rentfrow. 2016. Putting mood in context: Using smartphones to examine how people feel in different locations. J. Res. Personal. (2016).   
Björn Schuller, Raquel Jiménez Villar, Gerhard Rigoll, and Manfred K. Lang. 2005. Meta-classifiers in acoustic and linguistic feature fusion-based affect recognition. In Proceedings of IEEE ICASSP.   
Amit Singhal. 2001. Modern information retrieval: A brief overview. IEEE Data Eng. Bull. 24, 4 (2001), 35–43.   
Guojun Wang, Md. Zakirul Alam Bhuiyan, Jiannong Cao, and Jie Wu. 2014. Detecting movements of a target using face tracking in wireless sensor networks. IEEE Trans. Parallel Distrib. Syst. 25, 4 (2014), 939–949.   
Y. Yu, Z. Chen, B. Cao, W. Dong, Y. Guo, and J. Cao. 2013. MobSafe: Cloud computing based forensic analysis for massive mobile applications using data mining. Tsinghua Sci. Technol. 18, 4 (2013), 418–427.

Received June 2016; revised May 2017; accepted June 2017