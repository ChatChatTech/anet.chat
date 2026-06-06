# DeepKey: A Multimodal Biometric Authentication System via Deep Decoding Gaits and Brainwaves

XIANG ZHANG, LINA YAO, and CHAORAN HUANG, University of New South Wales, Australia TAO GU, RMIT University, Australia

ZHENG YANG, Tsinghua University, China

YUNHAO LIU, Michigan State University, USA

Biometric authentication involves various technologies to identify individuals by exploiting their unique, measurable physiological and behavioral characteristics. However, traditional biometric authentication systems (e.g., face recognition, iris, retina, voice, and fingerprint) are at increasing risks of being tricked by biometric tools such as anti-surveillance masks, contact lenses, vocoder, or fingerprint films. In this article, we design a multimodal biometric authentication system named DeepKey, which uses both Electroencephalography (EEG) and gait signals to better protect against such risk. DeepKey consists of two key components: an Invalid ID Filter Model to block unauthorized subjects, and an identification model based on attention-based Recurrent Neural Network (RNN) to identify a subject’s EEG IDs and gait IDs in parallel. The subject can only be granted access while all the components produce consistent affirmations to match the user’s proclaimed identity. We implement DeepKey with a live deployment in our university and conduct extensive empirical experiments to study its technical feasibility in practice. DeepKey achieves the False Acceptance Rate (FAR) and the False Rejection Rate (FRR) of 0 and 1.0%, respectively. The preliminary results demonstrate that Deep-Key is feasible, shows consistent superior performance compared to a set of methods, and has the potential to be applied to the authentication deployment in real-world settings.

CCS Concepts: • Human-centered computing → Ubiquitous and mobile computing; • Theory of computation → Design and analysis of algorithms;

Additional Key Words and Phrases: EEG (Electroencephalography), gait, biometric authentication, multimodal, deep learning

# ACM Reference format:

Xiang Zhang, Lina Yao, Chaoran Huang, Tao Gu, Zheng Yang, and Yunhao Liu. 2020. DeepKey: A Multimodal Biometric Authentication System via Deep Decoding Gaits and Brainwaves. ACM Trans. Intell. Syst. Technol. 11, 4, Article 49 (May 2020), 24 pages.

https://doi.org/10.1145/3393619

Authors’ addresses: X. Zhang, L. Yao, and C. Huang, University of New South Wales, CSE, K17, Barker St, UNSW, Sydney, NSW, 2052, Australia; emails: xiang.zhang3@student.unsw.edu.au, {lina.yao, chaoran.huang}@unsw.edu.au; T. Gu, RMIT University, 124 La Trobe St, RMIT University, Melbourne, VIC, 3001, Australia; email: tao.gu@rmit.edu.au; Z. Yang, Tsinghua University, 30 Shuangqing Rd, School of Software, Tsinghua University, Beijing, 100084, China; email: hmilyyz@ gmail.com; Y. Liu, Michigan State University, 220 Trowbridge Rd, East Lansing, MI 48824, USA; email: yunhao@cse. msu.edu.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2020 Association for Computing Machinery.

2157-6904/2020/05-ART49 \$15.00

https://doi.org/10.1145/3393619

# 1 INTRODUCTION

Over the past decade, biometric authentication systems have gained popularity due to their reliability and adaptability. Existing biometric authentication systems generally include physiological and behavioral ones. The former is based on an individual’s unique intrinsic features (e.g., face [14], iris [27], retina [38], voice [15], and fingerprint [43]) and the latter is based on an individual’s behavior patterns such as gait analysis [5]. Recently, biometrics- (e.g., fingerprint, face) based authentication systems face an increasing threat of being deceived as a result of the rapid development of the manufacturing industry and technologies. For example, individuals can easily trick a fingerprint-based authentication system by using a fake fingerprint film1 or an expensive face recognition–based authentication system by simply wearing a two-hundred-dollar anti-surveillance mask.2 Thus, fake-resistance characteristics are becoming a more significant requirement for any authentication system. To address the aforementioned issues, EEG (Electroencephalography) signal–based cognitive biometrics and gait-based systems have been attracting increasing attention.

EEG signal–based authentication systems are an emerging approach in physiological biometrics. EEG signals measure the brain’s response and record the electromagnetic, invisible, and untouchable electrical neural oscillations. Many research efforts have been made on EEG-based biometric authentication for the uniqueness and reliability. EEG data are unique for each person and almost impossible to be cloned and duplicated. Therefore, an EEG-based authentication system has the potential to uniquely identify humans and to be ingenious enough to protect against faked identities [8]. For instance, Chuang et al. [8] propose a single-channel EEG-based authentication system, which achieves an accuracy of 0.99. Keshishzadeh et al. [20] employ a statistical model for analyzing EEG signals and achieve an accuracy of 0.974. Generally, EEG signals have the following inherent advantages:

• Fake-resistibility. EEG data are unique for each person and almost impossible to be cloned and duplicated. EEG signals are individual-dependent. Therefore, an EEG-based authentication system has the potential to verify human identity and to be ingenious enough to protect against faked identities [8].   
• Reliability. An EEG-based authentication system can reject the subjects under abnormal situations (e.g., dramatically spiritual fluctuating, hysterical, drunk, or under threat) since EEG signals are sensitive to human stress and mood.   
• Feasibility. We have seen an important trend to build authentication systems based on EEG because the equipment for collecting EEG data is cheap and easy to acquire, and it is expected to be more precise, accessible, and economical in the future.

In comparison, gait-based authentication systems have been an active direction for years [37, 48]. Gait data are more generic and can be gathered easily from popular inertial sensors. Gait data are also unique because they are determined by intrinsic factors (e.g., gender, height, and limb length), temporal factors [6] (e.g., step length, walking speed, and cycle time), and kinematic factors (e.g., joint rotation of the hip, knee, and ankle, mean joint angles of the hip/knee/ankle, and thigh/trunk/foot angles). In addition, a person’s gait behavior is established inherently in the long term and therefore difficult to be faked. Hoang and Choi [18] propose a gait-based authentication biometric system to analyze gait data gathered by mobile devices, adopt error correcting codes to process the variation in gait measurement, and finally achieve a False Acceptance Rate (FAR) of 3.92% and a False Rejection Rate (FRR) of 11.76%. Cola et al. [9] collect wrist signals and train gait patterns to detect invalid subjects (unauthenticated people). The proposed method achieves an Equal Error Rate (EER) of 2.9%.

Despite the tremendous efforts, various other challenges still remain in single EEG/gait-based authentication systems: (i) the solo EEG-based authentication system has very high fake-resistance and excellent authentication performance but is easily affected by environmental factors (e.g., noise), subjective factors (e.g., mental state), and noisy brain signals (e.g., not concentrating); (ii) the solo gait-based authentication system is more stable over different scenarios but has relatively low performance; (iii) the solo EEG/gait authentication system generally obtains a FAR (which is extremely crucial in high-confidential authentication scenarios)3 higher than 3% [18]. It is not precise enough for highly sensitive places such as military bases, the treasuries of banks, and political offices where tiny misjudgments could provoke great economic or political catastrophes; (iv) the single authentication system may break down while under attack but no backup plan is provided.

In this article, we propose DeepKey, a novel biometric authentication system that enables dualauthentication leveraging on the advantages of both gait-based and EEG-based systems. Compared with either a gait-based or an EEG-based authentication system, a dual-authentication system offers more reliable and precise identification. Table 1 summarizes the overall comparison of DeepKey with some representative works on seven key aspects. DeepKey consists of three main components: the Invalid ID Filter Model to eliminate invalid subjects, the EEG Identification Model to identify EEG IDs, and the Gait Identification Model to identify gait IDs. An individual can be granted access only after she/he passes all the authentication components. Our main contributions are highlighted as follows:

• We present DeepKey, a dual-authentication system that exploits both EEG and gait biological traits. To the best of our knowledge, DeepKey is the first two-factor authentication system for person authentication using EEG and gaits. DeepKey is empowered with highlevel fake-resistance and reliability because both EEG and gait signals are invisible and hard to be reproduced.   
• We design a robust framework that includes an attention-based RNN to detect and classify multimodal sensor data, and to decode the large diversity in how people perform gaits and brain activities simultaneously. The delta band of EEG data is decomposed for its rich discriminative information.   
• We validate and evaluate DeepKey on several locally collected datasets. The results show that DeepKey significantly outperforms a series of baseline models and the state-of-the-art methods, achieving FAR of 0 and FRR of 1%. Further, we design extensive experiments to investigate the impact of key elements.

The remainder of this article is organized as follows. Section 2 introduces the EEG-based, gaitbased, and multimodal biometric systems briefly. Section 3 presents the methodology framework and three key models (Invalid ID Filter Model, Gait Identification Model, and EEG Identification Model) of the DeepKey authentication system in detail. Section 4 evaluates the proposed approach on the public Gait and EEG dataset and provides an analysis of the experimental results. Finally, Section 5 discusses the opening challenges of this work and highlights the future scope of this research, while Section 6 summarizes the key points of this article.

Table 1. Comparison of Various Biometrics 

<table><tr><td></td><td>Biometrics</td><td>Fake-resistance ↑</td><td>Universality ↑</td><td>Uniqueness ↑</td><td>Stability ↑</td><td>Accessibility ↑</td><td>Performance ↑</td><td>Computational Cost ↓</td></tr><tr><td rowspan="8">Uni-modal</td><td>Face/Vedio</td><td>Medium</td><td>Medium</td><td>Low</td><td>Low</td><td>High</td><td>Low</td><td>High</td></tr><tr><td>Fingerprint/Palmprint</td><td>Low</td><td>High</td><td>High</td><td>High</td><td>Medium</td><td>High</td><td>Medium</td></tr><tr><td>Iris</td><td>Medium</td><td>High</td><td>High</td><td>High</td><td>Medium</td><td>High</td><td>High</td></tr><tr><td>Retina</td><td>High</td><td>Medium</td><td>High</td><td>Medium</td><td>Low</td><td>High</td><td>High</td></tr><tr><td>Signature</td><td>Low</td><td>High</td><td>Low</td><td>Low</td><td>High</td><td>Low</td><td>Medium</td></tr><tr><td>Voice</td><td>Low</td><td>Medium</td><td>Low</td><td>Low</td><td>Medium</td><td>Low</td><td>Low</td></tr><tr><td>Gait</td><td>High</td><td>Medium</td><td>High</td><td>Medium</td><td>Medium</td><td>High</td><td>Low</td></tr><tr><td>EEG</td><td>High</td><td>Low</td><td>High</td><td>Low</td><td>Low</td><td>High</td><td>Low</td></tr><tr><td rowspan="4">Multimodal</td><td>Fingerprint+face</td><td>Low</td><td>High</td><td>Low</td><td>Low</td><td>High</td><td>Medium</td><td>High</td></tr><tr><td>Iris+pupil</td><td>Medium</td><td>Medium</td><td>High</td><td>High</td><td>Medium</td><td>High</td><td>High</td></tr><tr><td>Iris+face</td><td>Medium</td><td>High</td><td>Medium</td><td>Medium</td><td>Medium</td><td>Medium</td><td>High</td></tr><tr><td>ECG+fingerprint</td><td>High</td><td>Medium</td><td>Medium</td><td>High</td><td>Low</td><td>High</td><td>Medium</td></tr><tr><td></td><td>EEG+gait</td><td>High</td><td>Low</td><td>High</td><td>High</td><td>Low</td><td>High</td><td>Low</td></tr></table>

e better

# 2 RELATED WORK

In this section, we introduce the related studies on several topics: biometric authentication technologies, EEG-based authentication, gait-based authentication, and multimodal biometric authentication.

# 2.1 Biometric Authentication Technologies

Since biometric features cannot be stolen or duplicated easily, biometric authentication is becoming increasingly commonplace. Currently, the most mature biometric authentication technology is fingerprint-based authentication, which has been demonstrated to have high matching accuracy and been used for decades [30]. Iris recognition is another popular approach for biometric authentication owing to its unique and stable pattern [36]. Daugman [10] proposes to use Gabor phase information and Hamming distance for iris code matching, which still is the most classic iris recognition method. Based on [10], a flurry of research [36] has emerged offering solutions to ameliorate iris authentication problems. For example, Pillai et al. [36] introduce kernel functions to represent transformations of iris biometrics. This method restrains both the intra-class and interclass variability to solve the sensor mismatch problem. Face recognition techniques [13, 17, 52] is the most commonly used and accepted by the public for its unique features and non-invasiveness. Since face recognition systems require tackling different challenges including expression, image quality, illumination, and disguise to achieve high accuracy, Infrared Radiation (IR) [17] and 3D [13] systems have attracted much attention. According to [52], multimodal recognition combining traditional visual textual features and IR or 3D systems can achieve higher accuracy than single modal systems.

# 2.2 EEG-Based Authentication

Since EEG can be gathered in a safe and non-invasive way, researchers have paid great attention to exploring this kind of brain signals. For person authentication, EEG is, on the one hand, promising for being confidential and fake-resistant but, on the other hand, complex and hard to be analyzed. Marcel and Millán [33] use Gaussian Mixture Models and train client models with Maximum A Posteriori (MAP). Ashby et al. [3] extract five sets of features from EEG electrodes and inter-hemispheric data, combine them together, and process the final features with a Support Vector Machine (SVM). The study shows that EEG authentication is also feasible with less-expensive devices. Altahat et al. [2] select Power Spectral Density (PSD) as the feature instead of the widely used AutoRegressive (AR) models to achieve higher accuracy. They also conduct channel selection to determine the contributing channels among all 64 channels. Thomas and Vinod [41] take advantage of individual alpha frequency (IAF) and delta band signals to compose a specific feature vector. They also prefer PSD features but only perform the extraction merely on the gamma band.

# 2.3 Gait-Based Authentication

As the most basic activity in our daily lives, walking is an advanced research hotspot for activity recognition [46]. Differing from previous studies, our work focuses on human gait, a spatiotemporal biometric that measures a person’s manner on walking. Existing gait recognition approaches sit in two categories: One is model-based approach [35], which models gait information with mathematical structures, and the other is appearance-based approach, which extracts features in a straightforward way irrespective of the mathematical structure. Due to its high efficiency and remarkable performance, Gait Energy Image (GEI) [31] has become one of the most popular appearance-based methods in recent years. Based on GEIs, a considerable amount of works have been proposed to explore the exterior factors and distinguish different body parts. In addition, the cross-view variance is also a concern of gait identification [25, 26]. For example, Wu et al. [45] consider not only the cross-view variance but also deep Convolutional Neural Networks (CNNs) for robust gait identification.

![](images/0b729e17cad2c66fa1e56a1328f71247409b80b36447eb1e6e21b736aaa8eae6.jpg)



Fig. 1. Workflow of DeepKey authentication system. The data collection of EEG and gait are cascade.

# 2.4 Multimodal Biometric Authentication

Since traditional unimodal authentication suffers from the negative influence of loud noise, low universality, and intra-class variation, it cannot achieve higher accuracy in a wide range of applications. To address this issue, multimodal biometric authentication, which combines and uses biometric traits in different ways, is becoming popular. Taking the commonness into consideration, most works choose two biometrics from face, iris, and fingerprints and make the fusion [21, 24, 40]. In [11], an innovative combination between gait and electrocardiogram (ECG) is shown to be effective. Manjunathswamy et al. [32] combine ECG and fingerprint at the score level. To the best of our knowledge, the approach proposed in this article is the first to combine EEG and gaits for person authentication. Taking advantage of both EEG and gait signals, the combination is expected to improve the reliability of authentication systems.

This dual-authentication system is partially based on our previous work MindID [50], which is an EEG-based identification system. We emphasize several differences compared to [50]: (1) this work is an authentication system with an invalid ID filter while [50] only focuses on identification; (2) this work adopts two biometrics including EEG and gait while [50] only exploits EEG signals; and (3) this work conducts extensive real-world experiments to collect gait signals.

# 3 DEEPKEY AUTHENTICATION SYSTEM

In this section, we first report the workflow of DeepKey to give an overview of the authentication algorithm, and then present the technical details for each component.

# 3.1 DeepKey System Overview

The DeepKey system is supposed to be deployed in access to confidential locations (e.g., bank vouchers, military bases, and government confidential residences). As shown in Figure 1, the overall workflow of the DeepKey authentication system consists of the following four steps:

(1) Step 1: EEG data collection. The subject, who requests for authentication, is required to wear the EEG headset and stays in relaxation. The collection of EEG data (E) will typically take 2 seconds.

(2) Step 2: Gait data collection. The subject takes off the EEG headset and puts on three IMUs (Inertial Measurement Units) and walks through an aisle to collect gait data G by IMUs.   
(3) Step 3: Authentication. The gathered EEG and gait data are flattened and associated with input data $\boldsymbol { \mathcal { I } } = [ \boldsymbol { \mathcal { E } } : \boldsymbol { \mathcal { G } } ]$ to be fed into the DeepKey authentication algorithm.   
(4) Step 4: Decision. An Approve or Deny decision will be made according to the DeepKey authentication results.

The most crucial component among the above steps is the third step, where the DeepKey authentication system receives the associated input data I and accomplishes two goals: authentication and identification. For the former goal, we employ EEG signals to justify the impostor for its high fake-resistance. EEG signals are invisible and unique, making them difficult to be duplicated and hacked. For the latter goal, we adopt a deep learning model to extract the distinctive features and feed them into a non-parametric neighbor-based classifier for ID identification. In summary, the DeepKey authentication algorithm contains several key stages, namely, Invalid ID Filter, Gait-based Identification, EEG-based Identification, and Decision Making. The overall authentication contains the following several stages (Figure 3):

(1) Based on the EEG data, the Invalid ID Filter decides the subject is an impostor or a genuine. If the subject is an impostor, the request will be denied.   
(2) If the individual is determined as genuine, the EEG/Gait Identification Model will identify the individual’s authorized EEG/Gait ID. This model is pre-trained offline with the attention-based Long Short-Term Member (LSTM) model (Section 3.3). The output is the ID number associated with the person’s detailed personal information.   
(3) The final stage is to check the consistency of the EEG ID and the Gait ID. If they are identical, the system will grant an approval, otherwise it will deny the subject and take corresponding security measures.

# 3.2 Invalid ID Filter Model

Through our preliminary experiments, it has been found that raw EEG signals, compared to raw Gait data, have better characteristics to prevent invalid ID due to the high fake-resistance of EEG data and the richness of distinguishable features in EEG signals. Thus, in this section, we only use EEG for invalid ID filtering.

The subjects in an authentication system are categorized into two classes: authorized and unauthorized. Since the unauthorized data are not available in the training stage, an unsupervised learning algorithm is required to identify the invalid ID. In this work, we apply a one-class SVM to sort out the unauthorized subjects. Given a set of authorized subjects, $\boldsymbol { S } = \{ S _ { i } , i = 1 , 2 , \ldots , L ^ { \circ } \}$ , $S _ { i } \in R ^ { n _ { s } }$ , where $L ^ { \circ }$ denotes the number of authorized subjects and $n _ { s }$ denotes the number of dimensions of the input data. The input data consist of EEG data $\mathcal { E } = \{ E _ { i } , i = 1 , 2 , . . . , L ^ { \circ } \} , E _ { i } \in R ^ { n _ { e } }$ and gait data $\mathcal { G } = \{ G _ { i } , i = 1 , 2 , . . . , L ^ { \circ } \} , G _ { i } \in R ^ { n _ { g } } . n _ { q }$ and $n _ { e }$ denote the number of dimensions of the gait data and EEG data, respectively, and $n _ { s } = n _ { q } + n _ { e }$ . The notation can be found in Table 2.

For each authentication, the collected EEG data $E _ { i }$ includes a number of samples. Each sample is a vector with shape [1, 14] where 14 denotes the number of electric-nodes in the Emotiv headset. To trade off the authentication efficiency (less collecting and waiting time) and computational performance, based on the experimental experience, we fed 200 samples ([200, 14]) into the Invalid ID Filter. 200 EEG samples are collected in 1.56 seconds, which is acceptable. The final filter result is the mean of the results on all the samples.

Table 2. Notation 

<table><tr><td>Parameters</td><td>Explanation</td></tr><tr><td> $L^{\circ}$ </td><td>the number of authorized subjects (genuine)</td></tr><tr><td> $E$ </td><td>the set of EEG signals</td></tr><tr><td> $G$ </td><td>the set of gait signals</td></tr><tr><td> $n_{s}$ </td><td>the number of features in input data sample</td></tr><tr><td> $G_{i}$ </td><td>the  $i$ -th gait data</td></tr><tr><td> $n_{g}$ </td><td>the number of features in per gait sample</td></tr><tr><td> $E_{i}$ </td><td>the  $i$ -th EEG data</td></tr><tr><td> $n_{e}$ </td><td>the number of features in EEG data sample</td></tr><tr><td> $X^{i}$ </td><td>the data in the  $i$ -th layer of attention RNN</td></tr><tr><td> $N^{i}$ </td><td>the number of dimensions in  $X^{i}$ </td></tr><tr><td> $K$ </td><td>the number of participants (genuine and impostor)</td></tr><tr><td> $c_{j}^{i'}$ </td><td>the hidden state in the  $j$ -th LSTM cell</td></tr><tr><td> $\mathcal{T}(\cdot)$ </td><td>the linear calculation of dense neural layers</td></tr><tr><td> $\mathcal{L}(\cdot)$ </td><td>The LSTM calculation process</td></tr><tr><td> $\odot$ </td><td>the elementwise multiplication</td></tr><tr><td> $C_{att}$ </td><td>attention-based code</td></tr></table>

Table 3. Characteristics of EEG Frequency Bands 

<table><tr><td>Name</td><td>Frequency (Hz)</td><td>Amplitude</td><td>Brain State</td><td>Awareness Degree</td><td>Produced Location</td></tr><tr><td>Delta</td><td>0.5–3.5</td><td>Higher</td><td>Deep sleep pattern</td><td>Lower</td><td>Frontally and posteriorly</td></tr><tr><td>Theta</td><td>4–8</td><td>High</td><td>Light sleep pattern</td><td>Low</td><td>Entorhinal cortex, hippocampus</td></tr><tr><td>Alpha</td><td>8–12</td><td>Medium</td><td>Closing the eyes, relax state</td><td>Medium</td><td>Posterior regions of head</td></tr><tr><td>Beta</td><td>12–30</td><td>Low</td><td>Active thinking, focus, high alert, anxious</td><td>High</td><td>Most evident frontally</td></tr><tr><td>Gamma</td><td>30–100</td><td>Lower</td><td>During cross-modal sensory processing</td><td>Higher</td><td>Somatosensory cortex</td></tr></table>

Awareness Degree denotes the degree of being aware of an external world.

# 3.3 EEG Identification Model

Compared to gait data, EEG data contain more noise, which is more challenging to handle. Given the complexity of EEG signals, the data pre-processing is necessary. In practical EEG data analysis, the assembled EEG signals can be divided into several different frequency patterns (delta, theta, alpha, beta, and gamma) based on the strong intra-band correlation with a distinct behavioral state. The EEG frequency patterns and the corresponding characters are listed in Table 3 [50]. Figure 2 reports the topography of EEG signals of different subjects under different frequency bands and demonstrates that the Delta wave, compared to other bands, enriches distinctive features. In detail, we calculate the inter-subject EEG signal cosine-similarity which measures the average similarity among different subjects under all the EEG bands. The results are reported as 0.1313 (full bands), 0.0722 (Delta band), 0.1672 (Theta band), 0.2819 (Alpha band), 0.0888 (Beta band), and 0.082 (Gamma band). This illustrates that the delta band with the lowest similarity contains the most distinguishable features for person identification. Our previous work [50] has demonstrated that Delta pattern, compared to other EEG patterns, contains the most distinctive information and is the most stable pattern in different environments by qualitative analysis and empirical experiment results. Thus, in this article, we adopt a bandpass (0.5 Hz–3.5 Hz) Butterworth filter to extract Delta wave signal for further authentication. For simplicity, we denote the filtered EEG data as E.

![](images/1041f76cf092c01004e5c214efa51092df9dfbb7f09b03aead4891716e0ddf84.jpg)



Fig. 2. EEG topography of different subjects under different frequency bands. The inter-subject EEG signal cosine-similarity is calculated under each band and the results are reported as 0.1313 (full bands), 0.0722 (Delta band), 0.1672 (Theta band), 0.2819 (Alpha band), 0.0888 (Beta band), and 0.082 (Gamma band). This illustrates that the delta band with the lowest similarity contains the most distinguishable features for person identification.

Since different EEG channels record different aspects of the brain signals, some of which are more representative of the individual, an approach that assumes all dimensions to be equal may not be suitable. Thus, we attempt to develop a novel model which can pay more attention to the most informative signals. In particular, the proposed approach is supposed to automatically learn the importance of the different parts of the EEG signal and focus on the valuable part. The effectiveness of attention-based RNN has been demonstrated in various domains including natural language processing [44] and speech recognition [7]. Inspired by the wide success of an attention mechanism [12], we introduce it to the Encoder-Decoder RNN model to assign varying weights to different dimensions of the EEG data. After EEG filtering, the composed Delta pattern E is fed into an attention-based Encoder-Decoder RNN structure [44] aiming to learn more representative features for user identification. The general Encoder-Decoder RNN framework regards all the feature dimensions of input sequence as having the same weights, no matter how important the dimension is for the output sequence. In this article, the different feature dimensions of the EEG data correspond to the different nodes of the EEG equipment. For example, the first dimension (first channel) collects the EEG data from the AF 34 node located at the frontal lobe of the scalp while the seventh dimension is gathered from the O1 node at the occipital lobe. To assign various weights to different dimensions of $\varepsilon ,$ we introduce the attention mechanism to the Encoder-Decoder RNN model. The proposed attention-based Encoder-Decoder RNN consists of three components (Figure 3): the encoder, the attention module, and the decoder. The encoder is designed to compress the input Delta $\delta$ wave into a single intermediate code $C ;$ the attention module helps the encoder calculate a better intermediate code $C _ { a t t }$ by generating a sequence of the weights $W _ { a t t }$ of different dimensions; the decoder accepts the attention-based code $C _ { a t t }$ and decodes it to the output layer $Y ^ { \prime }$ .

![](images/c9e24cb67253fe1281acbab28d10b84e47ae9c5610a3fb45076691f950d9f87e.jpg)



Fig. 3. Authentication workflow. If the input data cannot pass the invalid ID filter, it would directly be regarded as an impostor and deny access. If pass, the Delta pattern and gait signals are parallelly fed into an attention-based RNN structure to study the distinctive features $C _ { a t t }$ . The learned features are classified by the EEG and Gait classifier in order to identify the subject’s EEG and Gait ID. The subject is approved only if the EEG ID is a match with Gait ID.

Suppose the data in the i-th layer can be denoted by $X ^ { i } = ( X _ { i } ^ { i } ; i \in [ 1 , 2 , \ldots , I ] , j \in [ 1 , 2 , \ldots , N ^ { i } ] )$ where j denotes the j-th dimension of $X ^ { i }$ . I represents the number of neural network layers while $N ^ { i }$ denotes the number of dimensions in $X ^ { i }$ . Taking the first layer as an example, we have $X ^ { 1 } = \varepsilon$ , which indicates that the input sequence is the Delta pattern. Let the output sequence be $Y = ( Y _ { k } ; k \in [ 1 , 2 , \ldots , K ] )$ where K denotes the number of users. In this article, the user ID is represented by the one-hot label with length K. For simplicity, we define the operation $\mathcal { T } ( \cdot )$ as

$\mathcal { T } ( X ^ { i } ) = X ^ { i } W + b$ . Furthermore, we have

$$
\mathcal {T} (X _ {j} ^ {i - 1}, X _ {j - 1} ^ {i}) = X _ {j} ^ {i - 1} * W ^ {\prime} + X _ {j - 1} ^ {i} * W ^ {\prime \prime} + b ^ {\prime},
$$

where $W , b , W ^ { \prime } , W ^ { \prime \prime } , b ^ { \prime }$ denote the corresponding weight and bias parameters.

The encoder component contains several non-recurrent fully connected layers and one recurrent LSTM layer. The non-recurrent layers are employed to construct and fit into a non-linear function to purify the input Delta pattern; the necessity is demonstrated by the preliminary experiments.5 The dataflow in these non-recurrent layers can be calculated by

$$
X ^ {i + 1} = \tanh (\mathcal {T} (X ^ {i})),
$$

where tanh is the activation function. We engage the tanh as an activation function instead of siдmoid for the stronger gradient [28]. The LSTM layer is adopted to compress the output of nonrecurrent layers to a length-fixed sequence, which is regarded as the intermediate code C. Suppose LSTM is the i -th layer; the code equals to the output of LSTM, which is $C = X _ { j } ^ { i ^ { \prime } }$ . The $X _ { j } ^ { i ^ { \prime } }$ can be measured by

$$
X _ {j} ^ {i ^ {\prime}} = \mathcal {L} (c _ {j - 1} ^ {i ^ {\prime}}, X _ {j} ^ {i - 1}, X _ {j - 1} ^ {i ^ {\prime}}), \tag {1}
$$

where $c _ { j - 1 } ^ { i ^ { \prime } }$ denotes the hidden state of the (j − 1)-th LSTM cell. The operation $\mathcal { L } ( \cdot )$ denotes the calculation process of the LSTM structure, which can be inferred from the following equations.

$$
X _ {j} ^ {i ^ {\prime}} = f _ {o} \odot t a n h (c _ {j} ^ {i ^ {\prime}}), c _ {j} ^ {i ^ {\prime}} = f _ {f} \odot c _ {j - 1} ^ {i ^ {\prime}} + f _ {i} \odot f _ {m},
$$

$$
f _ {o} = \text { sigmoid } (\mathcal {T} (X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}})), f _ {f} = \text { sigmoid } (\mathcal {T} (X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}})),
$$

$$
f _ {i} = \operatorname{sigmoid} \left(\mathcal {T} \left(X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}}\right)\right), f _ {m} = \tanh \left(\mathcal {T} \left(X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}}\right)\right),
$$

where $f _ { o } , \ f _ { f } , \ f _ { i }$ , and $f _ { m }$ represent the output gate, forget gate, input gate, and input modulation gate, respectively, and  denotes the element-wise multiplication.

The attention module accepts the final hidden states as the unnormalized attention weights $W _ { a t t } ^ { \prime }$ , which can be measured by the mapping operation $\mathcal { L } ^ { \prime } ( \cdot )$

$$
W _ {a t t} ^ {\prime} = \mathcal {L} ^ {\prime} (c _ {j - 1} ^ {i ^ {\prime}}, X _ {j} ^ {i - 1}, X _ {j - 1} ^ {i ^ {\prime}}) \tag {2}
$$

and calculate the normalized attention weights $W _ { a t t }$

$$
W _ {a t t} = \text { softmax } (W _ {a t t} ^ {\prime}).
$$

The softmax function is employed to normalize the attention weights into the range of [0, 1]. Therefore, the weights can be explained as the probability of how the code C is relevant to the output results. Under the attention mechanism, the code C is weighted to $C _ { a t t }$ ,

$$
C _ {a t t} = C \odot W _ {a t t}.
$$

Note, C and $W _ { a t t }$ are trained simultaneously. The decoder receives the attention-based code $C _ { a t t }$ and decodes it to the output $Y ^ { \prime } ,$ . Since $Y ^ { \prime }$ is predicted at the output layer of the attention-based RNN model $( Y ^ { \prime } = X ^ { I } )$ , we have

$$
Y ^ {\prime} = \mathcal {T} (C _ {a t t}).
$$

At last, we employ the cross-entropy cost function, and $\ell _ { 2 } { \mathrm { - n o r m } }$ (with parameter λ) is selected to prevent overfitting. The cost is optimized by the AdamOptimizer algorithm [22]. The iterations threshold of attention-based RNN is set as $n _ { i t e r } ^ { E } .$ . The weighted code $C _ { a t t }$ has a direct linear relationship with the output layer and the predicted results. If the model is well trained with low cost, we could regard the weighted code as a high-quality representation of the user ID. We set the learned deep feature $X _ { D }$ to $C _ { a t t } , X _ { D } = C _ { a t t }$ , and feed it into a lightweight nearest-neighbor classifier. The EEG ID, which is denoted by $E _ { I D }$ , can be directly predicted by the classifier.

ALGORITHM 1: DeepKey System   
Input: EEG data E and Gait data G
Output: Authentication Decision: Approve/Deny
1: #Invalid ID Filter:
2: for E, G do
3:    Genuine/Impostor ← E
4:    if Impostor then
5:    return Deny
6:    else if Genuine then
7:    #EEG Identification Model:
8:    while iteration < $n_{iter}^{E}$ do
9: $X^{i+1} = \tanh(\mathcal{T}(X^{i})) \{X^{1} = \mathcal{E}\}$ 10: $C = X_{j}^{i'} = \mathcal{L}(c_{j-1}', X_{j}^{i-1}, X_{j-1}')$ 11: $W_{att} = softmax(\mathcal{L}'(c_{j-1}', X_{j}^{i-1}, X_{j-1}'))$ 12: $C_{att} = C \odot W_{att}$ 13: $E_{ID} \leftarrow C_{att}$ 14:    end while
15:    #Gait Identification Model:
16:    while iteration < $n_{iter}^{G}$ do
17: $G_{ID} \leftarrow G$ 18:    end while
19:    if $E_{ID} = G_{ID}$ then
20:    return Approve
21:    else
22:    return Deny
23:    end if
24:    end if
25: end for

The Gait Identification Model works similarly to the EEG Identification Model except for the frequency band filtering. The iterations threshold of attention-based RNN is set as $n _ { i t e r } ^ { G }$ . The Gait Identification Model receives a subject’s gait data G from the input data I and maps to the user’s Gait ID $G _ { I D }$ . All the model structures, hyper-parameters, optimization, and other settings in the EEG and Gait Identification Models remain the same to keep the lower model complexity of the DeepKey system.

# 4 EXPERIMENTS AND RESULTS

In this section, we first outline the experimental setting including dataset, hyper-parameters settings, and evaluation metrics. Then we systematically investigate (1) the comparison with the state-of-the-art authentication systems at both system level and component level; (2) the impact of key parameters like single/multiple sessions,6 EEG band, and data size; and (3) the authentication latency.

Step 1: EEG Collection   
![](images/b9ed33315fa77aff2af7e65acf1190d62a1bbb448967f3c255f440597953cb36.jpg)



Step 2: Gait Collection   
![](images/202b68cd2e9dd802c3605c8905de7baf5ac053c1f1757463f05d297ed6862dac.jpg)



Fig. 4. Data collection. Two collection steps are cascaded to eliminate the impact on EEG data of walking. The first step collects the solo EEG signals while the second step collects the gait signals.

# 4.1 Experimental Settings

4.1.1 Datasets. We design real-world experiments to collect EEG data and gait data in cascade.7 The experiments (Figure 4) are conducted by seven healthy participants aged 26 ± 2 including four males and three females. In Step 1, each participant remains standing and relaxed with eyes closed. The EEG data are collected by an EPOC+ Emotiv headset8 which integrates 14 electrodes (corresponding to 14 EEG channels) with a sampling rate of 128 Hz. The Emotiv headset gathers brain signals in a non-invasive manner since it doesn’t require surgery to insert sensors into the user’s skull [51]. In Step 2, each participant walks in an aisle to generate the gait data. In the gait collection procedure, three IMUs are attached to the participants’ left wrist, the middle of the back, and the left ankle, respectively. Each IMU (PhidgetSpatial $3 / 3 / 3 ^ { 9 } )$ with 80 Hz sampling rate gathering nine-dimensional motor features contains a three-axis accelerometer, three-axis gyroscope, and a three-axis magnetometer.

To investigate the impact of dataset sessions, both the EEG and gait data are collected in three sessions. In every cycle of single session, the subject puts on the equipment (headset/IMUs), gathers data, and then takes the equipment off. Therefore, in different sessions, the positions of the equipment may have a slight deviation. Table 4 reports the details of the datasets used in this article. Each EEG or gait sample contains 10 continuous instances without overlapping. The single session datasets (EID-S and GID-S) are collected in a single experiment session while the multisession datasets (EID-M and GID-M) are gathered in three sessions. All the sessions are conducted in the same place but on three different days (each session in one day). The EEG data are easily influenced if the emotional or physical state has changed, thus, we believe the collected data are diverse because of the varying environmental factors (e.g., noise and temperature) and subjective factors (e.g., participants’ mental state and fatigue state). Similarly, the gait signals could be affected by lots of variables like different shoes (comfortable/uncomfortable). In this article, as an exploratory work, we focus on developng a robust discriminative deep learning model which is strong enough to prevent the corruption of the aforementioned influencing factors. The investigation of the detail effect brought by each specific factor will be left as a future research direction.

Table 4. Datasets Description, Australia 

<table><tr><td>Dataset</td><td>Biometric</td><td>#-D</td><td>Session</td><td>Frequency</td><td>Samples</td></tr><tr><td>EID-S</td><td>EEG</td><td>14</td><td>Single</td><td>128 Hz</td><td>49,000</td></tr><tr><td>EID-M</td><td>EEG</td><td>14</td><td>Multiple</td><td>128 Hz</td><td>147,000</td></tr><tr><td>GID-S</td><td>Gait</td><td>27</td><td>Single</td><td>80 Hz</td><td>140,000</td></tr><tr><td>GID-M</td><td>Gait</td><td>27</td><td>Multiple</td><td>80 Hz</td><td>420,000</td></tr></table>

#-D denotes the number of dimensions.

4.1.2 Parameter Settings. The Invalid ID Filter attempts to recognize the unauthorized subject based on the unique EEG data. The filter chooses the RBF kernel with nu = 0.15. In the EEG Identification Model, the Delta band ([0.5 Hz, 3.5 Hz]) is filtered by a three-order Butterworth bandpass filter. In the attention-based RNN, in the input layer, there are 14 nodes for EEG and 27 nodes for gait signals. For both EEG and gait, we have two fully connected hidden layers (each has 64 nodes) and one LSTM layer with 64 cells; the output layer has seven nodes. The learning rate and λ are both set to 0.001. The weighted code is produced after 1,000 iterations. Here, eightfold crossvalidation is used to prevent overfitting. The dataset is randomly separated into eght equal-sized subsets. One of the 10 subsets is used as a test set while the remaining subsets are used as a training set. The user ID ranges from 0 to 6 and is represented in the one-hot label.

4.1.3 Metrics. The adopted evaluation metrics are accuracy, ROC, AUC, along with FAR and FRR. DeepKey is very sensitive to the invalid subject and can acquire very high accuracy in Invalid ID Filter Model for the reason that even a tiny misjudgment may lead to catastrophic consequences. Therefore, FAR is more important than other metrics. Therefore, in DeepKey, FAR has higher priority compared to other metrics such as FRR.

# 4.2 Overall Comparison

4.2.1 System-Level Comparison. To evaluate the performance of DeepKey, we compare it with a set of the state-of-the-art authentication systems. DeepKey is empowered to solve both the authentication and identification problems. As shown in Table 5, DeepKey achieves a FAR of 0 and a FRR of 1%, outperforming other uni-modal and multimodal authentication systems. Specifically, our approach, compared to the listed uni-modal systems, achieves the highest EEG identification accuracy (99.96%) and Gait identification accuracy (99.61%).

4.2.2 Component-Level Comparison. To have a closer observation, we provide the detailed performance study of each component. In the Invalid ID Filter, to enhance the accuracy and robustness of the classifier, EEG samples are separated into different segments, with each segment (without overlapping) having 200 continuous samples. Six in seven subjects are labeled as genuine while the other subject is labeled as an impostor. In the training stage, all the EEG segments are fed into the one-class SVM with RBF kernel for pattern learning. In the test stage, 1,000 genuine segments and 1,000 impostor segments are randomly selected to assess the performance. We use the leave-one-out-cross-validation training strategy and achieve a FAR of 0 and a FRR of 0.006.

In the EEG/Gait Identification Model, the proposed approach achieves an accuracy of 99.96% and 99.61% over the multi-session datasets, respectively. The detailed confusion matrix, ROC curves with AUC scores, and the classification reports (precision, recall, and F1-score) over all the datasets

<table><tr><td></td><td>Reference</td><td>Biometric</td><td>Method</td><td>#-Subject</td><td>Dataset</td><td>Accuracy</td><td>FAR</td><td>FRR</td></tr><tr><td rowspan="13">Uni-modal</td><td>[9]</td><td>Gait</td><td>semi-supervised anomaly detection+NN</td><td>15</td><td>Local</td><td>97.4</td><td></td><td></td></tr><tr><td>[34]</td><td>Gait</td><td>AVTM-PdVs</td><td>100</td><td>Public</td><td>77.72</td><td></td><td></td></tr><tr><td>[1]</td><td>Gait</td><td>MLP</td><td>60</td><td>Local</td><td>99.01</td><td></td><td></td></tr><tr><td>[39]</td><td>Gait</td><td>Artificial features + voting classifier</td><td>10</td><td>Local</td><td>98.75</td><td></td><td></td></tr><tr><td>[23]</td><td>Gait</td><td>Two SVMs</td><td>50</td><td>Local</td><td></td><td>1.0</td><td>1.0</td></tr><tr><td>[42]</td><td>EEG</td><td>PSD + cross-correlation values</td><td>109</td><td>Public</td><td></td><td>1.96</td><td>1.96</td></tr><tr><td>[8]</td><td>EEG</td><td>Customized Threshold</td><td>15</td><td>Local</td><td></td><td>0</td><td>2.2</td></tr><tr><td>[16]</td><td>EEG</td><td>Low-pass filter+wavelets+ ANN</td><td>32</td><td>Local</td><td>90.03</td><td></td><td></td></tr><tr><td>[4]</td><td>EEG</td><td>Bandpass FIR filter +ECOC + SVM</td><td>9</td><td>Local</td><td>94.44</td><td></td><td></td></tr><tr><td>[41]</td><td>EEG</td><td>IAF + delta band EEG + Cross-correlation values</td><td>109</td><td>Public</td><td>90.21</td><td></td><td></td></tr><tr><td>[19]</td><td>EEG</td><td>CSP +LDA</td><td>12</td><td>Local</td><td>96.97</td><td></td><td></td></tr><tr><td>[50]</td><td>EEG</td><td>Attention-based RNN + XGB</td><td>8</td><td>Local</td><td>98.82</td><td></td><td></td></tr><tr><td>[20]</td><td>EEG</td><td>AR + SVM</td><td>104</td><td>Public</td><td>97.43</td><td></td><td></td></tr><tr><td rowspan="15">Multi-modal</td><td></td><td>Fingerprint</td><td></td><td></td><td></td><td>92.89</td><td>7.108</td><td>7.151</td></tr><tr><td>[29]</td><td>Face</td><td>ZM + RBF Neural Network</td><td></td><td></td><td></td><td>11.52</td><td>13.47</td></tr><tr><td></td><td>Fusion</td><td></td><td>40</td><td>Public</td><td></td><td>4.95</td><td>1.12</td></tr><tr><td rowspan="3">[47]</td><td>Iris</td><td></td><td></td><td></td><td></td><td>13.88</td><td>13.88</td></tr><tr><td>Pupil</td><td>Gabor 2D wavelets + Gabor 2D wavelets + Hamming distance</td><td></td><td></td><td></td><td>5.47</td><td>5.47</td></tr><tr><td>Fusion</td><td></td><td>59</td><td>Public</td><td></td><td>2.44</td><td>2.44</td></tr><tr><td rowspan="3">[32]</td><td>ECG</td><td>wavelet decomposition</td><td></td><td></td><td></td><td>2.37</td><td>9.52</td></tr><tr><td>Fingerprint</td><td>Histogram manipulation Image Enhancement</td><td></td><td></td><td></td><td>7.77</td><td>5.55</td></tr><tr><td>Fusion</td><td>Score Fusion</td><td>50</td><td>Public</td><td></td><td>2.5</td><td>0</td></tr><tr><td rowspan="3">[11]</td><td>ECG</td><td></td><td></td><td></td><td></td><td>4.2</td><td>4.2</td></tr><tr><td>Gait</td><td>linear time interpolation + cross correlation</td><td></td><td></td><td></td><td>7.5</td><td>7.5</td></tr><tr><td>Fusion</td><td>Score Fusion</td><td>30</td><td>Local</td><td></td><td>1.26</td><td>1.26</td></tr><tr><td rowspan="3">Ours</td><td>EEG</td><td>Delta wave + Attention-based RNN +KNN</td><td></td><td></td><td>99.96</td><td></td><td></td></tr><tr><td>Gait</td><td>Attention-based RNN +KNN</td><td></td><td></td><td>99.61</td><td></td><td></td></tr><tr><td>Fusion</td><td></td><td>7</td><td>Local</td><td>99.57</td><td>0</td><td>1.0</td></tr></table>

The performance of our methods is evaluated on multi-session datasets (EID-M, GID-M).

![](images/7ff67762e05ebb459a1d28c4d98f5940aac0e829f5573be8becc7eb2fe04a830.jpg)  
Fig. 5. Confusion matrix and ROC curves of the datasets. CM denotes confusion matrix. The AUC are provided on the figures.

Table 6. Classification Report of the Datasets Including Precision, Recall, and F-1 Score 

<table><tr><td>Datasets</td><td colspan="3">EID-S</td><td colspan="3">EID-M</td><td colspan="3">GID-S</td><td colspan="3">GID-M</td></tr><tr><td>Metrics</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td>0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.998</td><td>1.0</td><td>0.999</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td></tr><tr><td>1</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9996</td><td>0.9998</td><td>0.996</td><td>0.996</td><td>0.996</td><td>0.9915</td><td>0.9904</td><td>0.9909</td></tr><tr><td>2</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9999</td><td>1.0</td><td>0.9999</td></tr><tr><td>3</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9992</td><td>0.9996</td><td>0.9992</td><td>0.9988</td><td>0.999</td><td>0.9937</td><td>0.9948</td><td>0.9942</td></tr><tr><td>4</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9976</td><td>0.998</td><td>0.9978</td><td>0.9949</td><td>0.996</td><td>0.9955</td></tr><tr><td>5</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9996</td><td>0.9992</td><td>0.9994</td><td>0.9969</td><td>0.9984</td><td>0.9977</td><td>0.9963</td><td>0.996</td><td>0.9961</td></tr><tr><td>6</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9996</td><td>0.9993</td><td>0.9994</td><td>0.9988</td><td>0.9972</td><td>0.998</td><td>0.9962</td><td>0.9953</td><td>0.9958</td></tr><tr><td>Average</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9996</td><td>0.9996</td><td>0.9996</td><td>0.9983</td><td>0.9983</td><td>0.9983</td><td>0.9961</td><td>0.9961</td><td>0.9961</td></tr></table>

The proposed approach gains impressive results (higher than 99%) on all the metrics over all the seven subjects.

are presented in Figure 5 and Table 6. The above evaluation metrics demonstrate that the proposed approach achieves a performance of over 99% on all the metrics over each subject and each dataset. To make a closer observation, taking the EID-M dataset as an example, we present the training and testing curves. As shown in Figure 8, the horizontal and vertical axes denote the number of training iterations and the accuracy, respectively. We can observe that our model starts at a rather high level, converges steadily in the training stage, and does not suffer from the overfitting problem.

Furthermore, the overall comparison between our model and other state-of-the-art baselines are listed in Table 7. RF denotes Random Forest, AdaB denotes Adaptive Boosting, and LDA denotes Linear Discriminant Analysis. In addition, the key parameters of the baselines are listed here: Linear SVM (C = 1), RF (n = 200), and KNN (k = 3). The settings of LSTM are the same as the attention-based RNN classifier, along with the GRU (Gated Recurrent Unit). The CNN contains two stacked convolutional layers (both with stride [1, 1], patch [2, 2], zero-padding, and the depths are 4 and 8, separately.) followed by one pooling layer (stride [1, 2], zero-padding) and one fully connected layer (164 nodes). Relu activation function is employed in the CNN. The methods used for comparison (three for EEG-based authentication and three for gait-based authentication) are introduced as follows:

Table 7. Component-Level Comparison 

<table><tr><td rowspan="2">Baseline</td><td rowspan="2">Methods</td><td colspan="4">EID-S</td><td colspan="4">EID-M</td></tr><tr><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="5">Non-DL Baseline</td><td>SVM</td><td>0.4588</td><td>0.5848</td><td>0.4588</td><td>0.4681</td><td>0.7796</td><td>0.7815</td><td>0.7796</td><td>0.7796</td></tr><tr><td>RF</td><td>0.9875</td><td>0.9879</td><td>0.9876</td><td>0.9876</td><td>0.8124</td><td>0.8139</td><td>0.8124</td><td>0.812</td></tr><tr><td>KNN</td><td>0.9897</td><td>0.9899</td><td>0.9898</td><td>0.9898</td><td>0.8211</td><td>0.8232</td><td>0.8211</td><td>0.8197</td></tr><tr><td>AdaB</td><td>0.2872</td><td>0.3522</td><td>0.2871</td><td>0.2337</td><td>0.3228</td><td>0.3224</td><td>0.3228</td><td>0.2815</td></tr><tr><td>LDA</td><td>0.1567</td><td>0.1347</td><td>0.1567</td><td>0.1386</td><td>0.3082</td><td>0.285</td><td>0.3082</td><td>0.2877</td></tr><tr><td rowspan="3">DL Baseline</td><td>LSTM</td><td>0.9596</td><td>0.9601</td><td>0.9596</td><td>0.9597</td><td>0.8482</td><td>0.8509</td><td>0.8483</td><td>0.8489</td></tr><tr><td>GRU</td><td>0.9633</td><td>0.9636</td><td>0.99631</td><td>0.9631</td><td>0.862</td><td>0.8638</td><td>0.8626</td><td>0.8629</td></tr><tr><td>CNN</td><td>0.8822</td><td>0.8912</td><td>0.8813</td><td>0.8912</td><td>0.7647</td><td>0.7731</td><td>0.7854</td><td>0.7625</td></tr><tr><td rowspan="3">State-of-the-art</td><td>[19]</td><td>0.5843</td><td>0.5726</td><td>0.5531</td><td>0.5627</td><td>0.5735</td><td>0.5721</td><td>0.5443</td><td>0.5579</td></tr><tr><td>[20]</td><td>0.8254</td><td>0.8435</td><td>0.8617</td><td>0.8525</td><td>0.8029</td><td>0.7986</td><td>0.8125</td><td>0.8055</td></tr><tr><td>[16]</td><td>0.8711</td><td>0.8217</td><td>0.7998</td><td>0.8106</td><td>0.8567</td><td>0.8533</td><td>0.8651</td><td>0.8592</td></tr><tr><td rowspan="2"></td><td>Att-RNN</td><td>0.9384</td><td>0.9405</td><td>0.9388</td><td>0.9391</td><td>0.9324</td><td>0.9343</td><td>0.9322</td><td>0.9326</td></tr><tr><td>Ours</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>0.9996</td><td>0.9996</td><td>0.9996</td><td>0.9996</td></tr><tr><td rowspan="2">Baselines</td><td rowspan="2">Methods</td><td colspan="4">GID-S</td><td colspan="4">GID-M</td></tr><tr><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="5">Non-DL Baseline</td><td>SVM</td><td>0.9981</td><td>0.9981</td><td>0.9981</td><td>0.9981</td><td>0.993</td><td>0.993</td><td>0.993</td><td>0.993</td></tr><tr><td>RF</td><td>0.9878</td><td>0.9878</td><td>0.9878</td><td>0.9878</td><td>0.9954</td><td>0.9954</td><td>0.9954</td><td>0.9954</td></tr><tr><td>KNN</td><td>0.9979</td><td>0.9979</td><td>0.9979</td><td>0.9979</td><td>0.9953</td><td>0.9953</td><td>0.9953</td><td>0.9953</td></tr><tr><td>AdaB</td><td>0.5408</td><td>0.5689</td><td>0.5409</td><td>0.4849</td><td>0.5401</td><td>0.5135</td><td>0.542</td><td>0.4985</td></tr><tr><td>LDA</td><td>0.688</td><td>0.6893</td><td>0.688</td><td>0.6855</td><td>0.6933</td><td>0.693</td><td>0.6933</td><td>0.6915</td></tr><tr><td rowspan="3">DL Baseline</td><td>LSTM</td><td>0.9951</td><td>0.9951</td><td>0.9951</td><td>0.9951</td><td>0.9935</td><td>0.9936</td><td>0.9936</td><td>0.9936</td></tr><tr><td>GRU</td><td>0.9949</td><td>0.9949</td><td>0.9949</td><td>0.9949</td><td>0.9938</td><td>0.9938</td><td>0.9938</td><td>0.9938</td></tr><tr><td>CNN</td><td>0.9932</td><td>0.9932</td><td>0.9932</td><td>0.9932</td><td>0.9845</td><td>0.9845</td><td>0.9845</td><td>0.9845</td></tr><tr><td rowspan="3">State-of-the-art</td><td>[9]</td><td>0.9721</td><td>0.9789</td><td>0.9745</td><td>0.9767</td><td>0.9653</td><td>0.9627</td><td>0.9669</td><td>0.9648</td></tr><tr><td>[1]</td><td>0.9931</td><td>0.9934</td><td>0.9957</td><td>0.9945</td><td>0.9901</td><td>0.9931</td><td>0.9942</td><td>0.9936</td></tr><tr><td>[39]</td><td>0.9917</td><td>0.9899</td><td>0.9917</td><td>0.9908</td><td>0.9875</td><td>0.9826</td><td>0.9844</td><td>0.9835</td></tr><tr><td rowspan="2"></td><td>Att-RNN</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.9894</td><td>0.9895</td><td>0.9895</td><td>0.9895</td></tr><tr><td>Ours</td><td>0.9983</td><td>0.9983</td><td>0.9983</td><td>0.9983</td><td>0.9961</td><td>0.9961</td><td>0.9961</td><td>0.9961</td></tr></table>

DL denotes Deep Learning. Att-RNN denotes attention-based RNN.

• Jayarathne et al. [19] feed EEG data to a bandpass filter (8 Hz − 30 Hz), extract CSP (Common Spatial Pattern) and recognize the user ID by LDA.   
• Keshishzadeh et al. [20] extract autoregressive coefficients as the features and identify the subject by SVM.   
• Gui et al. [16] employ low-pass filter (60 Hz) and wavelet packet decomposition to generate features and distinguish unauthorized person through deep neural network.   
• Cola et al. [9] hire neural networks to analyze user gait pattern by artificial features such as kurtosis, peak-to-peak amplitude, and skewness.   
• Al-Naffakh et al. [1] propose to utilize time-domain statistical features and Multilayer Perception (MLP) for person identification.

![](images/59bc1a0737c9fc63fda05d415e6cc8550d5d7c3d2682cb65582ebb53befceffc.jpg)



Fig. 6. Impact of session.

![](images/1d8563225d644853476a1500f7c7e6cfb950b735c0bc2af7a31a976d3a6ff5bb.jpg)



Fig. 7. Latency.

• Sun et al. [39] adopt a weighted voting classifier to process the extracted features like gait frequency, symmetry coefficient, and dynamic range.

The primary conclusions from Table 7 are summarized as follows:

• Our approach achieves the highest performance over both EEG and gait datasets under single session and multi-session settings.   
• For most of the baselines, we observe lower accuracy in the EEG dataset compared to that in the gait dataset, implying the EEG-based authentication is still challenging and our approach has room to improve; nevertheless, our model outperforms others and shows superiority to both EEG-based or Gait-based methods.   
• The results on single-session datasets are better than that on multi-session datasets. This is reasonable, and it demonstrates that the number of sessions does affect the authentication accuracy. This problem will be further analyzed in Section 4.3.1.   
• Our model achieves better performance than Att-RNN. Since the diversity between our model and Att-RNN is that we employ an external classifier, this observation demonstrates that the external classifier is effective and efficient.

In DeepKey, the subjects passing the Invalid ID Filter are regarded as genuine only if their recognized IDs are consistent, i.e., $E _ { I D } = G _ { I D }$ . It can be inferred easily that the FAR of DeepKey is 0 as well. However, the FRR depends on one or more of these three scenarios: the false rejection of Invalid ID Filter; the incorrect Gait identification; the incorrect EEG identification. In summary, the overall FAR is 0 and the overall FRR is calculated as $1 \% \approx 0 . 0 0 6 + 0 . 9 9 4 * ( 1 - 0 . 9 9 6 1 * 0 . 9 9 9 6 )$ .

# 4.3 Impact of Key Parameters

4.3.1 Impact of Sessions. In practical applications, sessions in different scenarios may result in a minor difference in equipment position, signal quality, and other factors. To investigate the impact of sessions, we conduct external experiments by comparing the performance between singlesession datasets and multi-session datasets. The comprehensive evaluation metrics and the comparison over various baselines are listed in Table 6 and Table 7, while the comparison is summarized in Figure 6. The experiment results show that on the multi-session datasets, compared with the single-session datasets, we achieve a slightly lower but still highly competitive performance.

4.3.2 Impact of EEG Band. A series of comparison experiments are designed to explore the optimal EEG frequency band which contains the most discriminative features. The results presented in Table 8 illustrate the following:

• The Delta band consistently provides higher identification accuracy compared to other frequency bands for both single and multiple sessions. This observation shows that Delta pattern contains the most discriminative information for person identification.

Table 8. EEG Bands Comparison 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Baseline</td><td rowspan="2">Methods</td><td colspan="6">EEG Bands</td><td rowspan="2">Best Level</td><td rowspan="2">Best Band</td></tr><tr><td>Delta</td><td>Theta</td><td>Alpha</td><td>Beta</td><td>Gamma</td><td>Full</td></tr><tr><td rowspan="13">EID-S</td><td rowspan="5">Non-DL Baseline</td><td>SVM</td><td>0.4588</td><td>0.4682</td><td>0.7484</td><td>0.5955</td><td>0.5239</td><td>0.8788</td><td>0.8788</td><td>Full</td></tr><tr><td>RF</td><td>0.9875</td><td>0.8006</td><td>0.7729</td><td>0.6376</td><td>0.5469</td><td>0.8931</td><td>0.9875</td><td>Delta</td></tr><tr><td>KNN</td><td>0.9897</td><td>0.8084</td><td>0.7465</td><td>0.5553</td><td>0.4606</td><td>0.8792</td><td>0.9897</td><td>Delta</td></tr><tr><td>AdaB</td><td>0.2872</td><td>0.2879</td><td>0.2318</td><td>0.3069</td><td>0.2922</td><td>0.3289</td><td>0.3289</td><td>Full</td></tr><tr><td>LDA</td><td>0.1567</td><td>0.1802</td><td>0.1957</td><td>0.1502</td><td>0.1306</td><td>0.4547</td><td>0.4547</td><td>Full</td></tr><tr><td rowspan="3">DL Baseline</td><td>LSTM</td><td>0.9596</td><td>0.8126</td><td>0.8277</td><td>0.6906</td><td>0.6027</td><td>0.9273</td><td>0.9596</td><td>Delta</td></tr><tr><td>GRU</td><td>0.9633</td><td>0.7996</td><td>0.8082</td><td>0.6902</td><td>0.6985</td><td>0.9251</td><td>0.9633</td><td>Delta</td></tr><tr><td>CNN</td><td>0.8822</td><td>0.7416</td><td>0.8079</td><td>0.6918</td><td>0.6059</td><td>0.8985</td><td>0.8985</td><td>Full</td></tr><tr><td rowspan="3">State-of-the-art</td><td>[19]</td><td>0.5843</td><td>0.4487</td><td>0.2918</td><td>0.3017</td><td>0.4189</td><td>0.5112</td><td>0.5843</td><td>Delta</td></tr><tr><td>[20]</td><td>0.8254</td><td>0.7935</td><td>0.7019</td><td>0.6368</td><td>0.6621</td><td>0.8018</td><td>0.8254</td><td>Delta</td></tr><tr><td>[16]</td><td>0.8711</td><td>0.8531</td><td>0.7556</td><td>0.6882</td><td>0.5101</td><td>0.7819</td><td>0.8711</td><td>Delta</td></tr><tr><td rowspan="2"></td><td>Att-RNN</td><td>0.9384</td><td>0.7928</td><td>0.8318</td><td>0.6854</td><td>0.6046</td><td>0.9238</td><td>0.9384</td><td>Delta</td></tr><tr><td>Ours</td><td>1.0</td><td>0.9285</td><td>0.8366</td><td>0.5529</td><td>0.4558</td><td>0.9417</td><td>1.0</td><td>Delta</td></tr><tr><td rowspan="13">EID-M</td><td rowspan="5">Non-DL Baseline</td><td>SVM</td><td>0.7796</td><td>0.5424</td><td>0.5664</td><td>0.6522</td><td>0.4915</td><td>0.7477</td><td>0.7796</td><td>Delta</td></tr><tr><td>RF</td><td>0.8124</td><td>0.7194</td><td>0.7351</td><td>0.6842</td><td>0.4765</td><td>0.8121</td><td>0.7194</td><td>Delta</td></tr><tr><td>KNN</td><td>0.8211</td><td>0.7501</td><td>0.7649</td><td>0.6611</td><td>0.3821</td><td>0.8162</td><td>0.7501</td><td>Delta</td></tr><tr><td>AdaB</td><td>0.3228</td><td>0.3095</td><td>0.2478</td><td>0.2548</td><td>0.2529</td><td>0.3189</td><td>0.3228</td><td>Delta</td></tr><tr><td>LDA</td><td>0.3082</td><td>0.1681</td><td>0.1621</td><td>0.1824</td><td>0.1311</td><td>0.2995</td><td>0.3082</td><td>Delta</td></tr><tr><td rowspan="3">DL Baseline</td><td>LSTM</td><td>0.8482</td><td>0.6926</td><td>0.7438</td><td>0.5726</td><td>0.5008</td><td>0.8185</td><td>0.8482</td><td>Delta</td></tr><tr><td>GRU</td><td>0.862</td><td>0.6935</td><td>0.7531</td><td>0.5672</td><td>0.5072</td><td>0.8221</td><td>0.862</td><td>Delta</td></tr><tr><td>CNN</td><td>0.7647</td><td>0.6712</td><td>0.7191</td><td>0.5588</td><td>0.4949</td><td>0.7749</td><td>0.7749</td><td>Full</td></tr><tr><td rowspan="3">State-of-the-art</td><td>[19]</td><td>0.9721</td><td>0.7019</td><td>0.7091</td><td>0.4189</td><td>0.4089</td><td>0.8195</td><td>0.9721</td><td>Delta</td></tr><tr><td>[20]</td><td>0.9931</td><td>0.6891</td><td>0.6988</td><td>0.5124</td><td>0.3397</td><td>0.7963</td><td>0.9931</td><td>Delta</td></tr><tr><td>[16]</td><td>0.9917</td><td>0.7199</td><td>0.6572</td><td>0.4911</td><td>0.3977</td><td>0.8011</td><td>0.9917</td><td>Delta</td></tr><tr><td rowspan="2"></td><td>Att-RNN</td><td>0.9324</td><td>0.6847</td><td>0.6846</td><td>0.5732</td><td>0.4941</td><td>0.7976</td><td>0.9324</td><td>Delta</td></tr><tr><td>Ours</td><td>0.9996</td><td>0.9013</td><td>0.8989</td><td>0.4428</td><td>0.3661</td><td>0.8858</td><td>0.9996</td><td>Delta</td></tr></table>

The full band denotes the raw EEG data with full frequency bands.

• Our method gains the best outcome on both datasets with different sessions. This validates the robustness and adaptability of the proposed approach.

Why could Delta pattern outperform other patterns since Delta wave mainly appears in deep sleep state? Here we give one possible reason. We know that the EEG patterns are associated with an individual’s mental and physical states (organics and systems). For example, while the subject is under deep sleep and producing Delta pattern, the majority of physical functions of the body (such as sensing, thinking, even dreaming) are completely detached. Only the very essential life-support organs and systems (such as breathing, heart beating, and digesting) keep working, which indicates the brain areas corresponding to life-support functions are active. While the subject is awake (e.g., relax state) and producing Alpha pattern, the subject has more activated functions such as imaging, visualizing, and concentrating. Also, more brain functions like hearing, touching, and thinking are attached, which means that more physical brain areas (such as frontal lobe, temporal lobe, and parietal lobe) are activated. At this time, the life-support organs are still working. In short, only the life-support organs related brain areas are active in the first scenario (Delta pattern), while the brain areas controlling life-support and high-level functions (e.g., concentrating) are active in the second scenario (Alpha pattern). Thus, we infer that the Delta pattern corresponds to the lifesupport organs and systems, which is the most stable function in different scenarios and the most discriminative signal in inter-subject classification.

![](images/1a532ef3e4eb5ca55a7d17cc44c92e1bd12cdc1273ffba0a46b626a38cb3ae4a.jpg)



Fig. 8. Convergence curves.

![](images/04e7f2e33cd559ccb29c09ab0eb6e2d32d5fca530bc0c2fa8fa35f162e54faac.jpg)



Fig. 9. Impact of datasize.

4.3.3 Impact of Datasize. Datasize is one crucial influence element in deep learning based algorithms. In this section, we conduct experiments to train the proposed method over various data sizes. As shown in the radar chart (Figure 9), four datasets are evaluated under different proportions of training datasize. It has five equi-angular spokes which represent the proportion of datasize (20%, 40%, 60%, 80%, 100%), respectively. The four concentric circles indicate the accuracy, which are 85%, 90%, 95%, and 100%, respectively. Each closed line represents a dataset and has five intersections with the five spokes. Each intersection node represents the classification accuracy of a specific dataset with a specific proportion datasize. For example, the intersection of the EID-S line and 20% spoke is about 0.92, which denotes that our approach achieves the accuracy of 92% over the EID-S dataset with 20% datasize. The radar chart infers that gait datasets (GID-S and GID-M) obtain competitive accuracy even with 20% datasize; nevertheless, EID-S and EID-M highly rely on the datasize. This phenomenon is reasonable because EEG data has a lower signal-to-noise ratio and requires more samples to learn the latent distribution pattern.

# 4.4 Latency Analysis

We also study the latency of DeepKey since low delay is highly desirable in real-world deployment. The latency of DeepKey is compared to the response time of several state-of-the-art authentication approaches. The comparison results are shown in Figure 7. The testing latency of our method is 0.39 s, which is competitive compared to the state-of-the-art baselines. Specifically, the reaction time of DeepKey is composed of several components, with the Invalid ID Filter taking 0.06 s and the ID Identification taking 0.33 s.

The overall system latency not only includes the computation latency but also includes the data collection latency such as the time cost when wearing the EEG headset and the IMUs. In detail, the data collection latency of our system is around 10 s, while EEG collection requires about 4 s and gait collection requires above 6 s. We can see that the data collection latency is much higher than computational latency; as a result, one major future direction to reduce system latency is to save the equipment-related time (discussed in Section 4.5).

# 4.5 Usability

The users have to sequentially wear two different devices to complete EEG and gait data collection, which may lead to incontinence and time-wasting. In this section, we justify the usability of the proposed DeepKey system in several aspects. First, the two equipments are non-invasive, light, and easy-to-wear, which will not cost lots of user effort. Second, as mentioned in Section 4.4, the authentication latency is very small (0.39 s); even counting the data collection latency, the whole authentication procedure will cost less than 10 s, which is tolerable for the users. Third, the proposed DeepKey aims at the highly confidential scenarios (e.g., military bases, the treasuries of banks, and political offices) which require strict precision and very high fake-resistance, in which the inconvenience is acceptable.

Even so, we agree that simplifying the authentication procedure will promote the deployment of the system. We attempt to solve this issue in the future. On the one hand, with the development of hardware- related techniques, the EEG headset is becoming more portable and affordable. For example, the developed cEEGrids,10 flex-printed, multi-channel sensor arrays that are placed around the ear using an adhesive, are easy and comfortable to wear and dispatch. This is a good choice of EEG acquisition equipment, although the cEEGrids are currently expensive. On the other hand, a potential solution is to develop a device-free authentication system and measure gait signals by environmental sensors such as RFID (Radio Frequency IDentification) tags. The Received Signal Strength Indication (RSSI) of an RFID tag measures the received signal power which reflects the target subject’s walking information [49]. Another possible solution targeting the two-factor design is to integrate gait sensors into the EEG headset. This will decrease the equipment expense and require less user effort, although this may cause a slight decrease in the authentication accuracy due to the fewer IMUs (there are three IMUs in our experiments but only one IMU after the integration with Emotiv headset). In the future, the wide deployment of the DeepKey authentication system in a real-world environment is possible.

# 5 DISCUSSIONS AND FUTURE WORK

In this article, we propose a biometric identification system based on both EEG and gait information. In this section, we discuss the open challenges and potential future research directions.

First, the datasets used in this article only have limited participants. Extensive evaluations over more subjects are necessary. However, compared to some existing works ([50], [4], and [39] have 8, 9, and 10 subjects in their experiments, respectively), we believe our participation scale is acceptable. Our work has already demonstrated that DeepKey can be used in settings such as small offices which are accessed by a limited group of people. In addition, evaluation can be improved by extending observations on how the system performs in different conditions. For example, considering changes in EEG signals during more trials, and longer times (hours, days, or even months) to understand if these are consistent and reliable for detection.

Second, wearable sensors like an EEG headset and wearable IMUs are required in the data collection stage of the DeepKey system. Extensive experiments are meaningful in the future to investigate how the placement position of the wearable sensor matters. The EEG headset position on the head and the IMU position on the arms may affect the authentication performance.

Additionally, a promising future work is the real-world online deployment of the proposed DeepKey system. Since we have demonstrated the effectiveness and efficiency of DeepKey in the offline situation, a future step is to build a real-time authentication environment to evaluate the online performance.

The brain signals could be easily affected by environmental factors (e.g., noise), subjective factors (e.g., emotion and fatigue), and other brain activities (e.g., eye-opening, staring at a specific image, mental working). The proposed DeepKey is robust to objective and subjective factors due to the deep representation learning. As for other brain activities, various brain activities may lead to different authentication performance. In this work, we collect the brain signals while the user is relaxing with eyes closed because this status will produce more stable EEG signals and have less intra-subject difference. One future work is supposed to investigate how the different brain activities will impact the authentication accuracy.

Furthermore, the proposed DeepKey still faces the challenge of the “in the wild” scenario since the gathered EEG data are easily corrupted by physical actions like walking. In this work, the EEG and gait data are gathered in two separate steps. However, in outdoor environments, the user is hardly standing still and waiting for the authentication. Fortunately, our system has competitive performance in a fixed indoor environment (such as bank vouchers) which can provide a stable data collection environment and mainly concerned about high fake-resistance.

# 6 CONCLUSION

Taking advantage of both EEG- and gait-based systems for fake-resistance, we propose DeepKey, a multimodal biometric authentication system, to overcome the limitations of traditional unimodal biometric authentication systems. DeepKey contains three independent models: an Invalid ID Filter Model, a Delta band based EEG Identification Model, and a Gait Identification Model, to detect invalid EEG data, and recognize the EEG ID and Gait ID, respectively. The DeepKey system outperforms the state-of-the-art baselines by achieving a FAR of 0 and a FRR of 1%. In addition, the key parameters (such as sessions and EEG frequency band) and the system latency are also investigated by extensive experiments.

This work sheds light on further research on multimodal biometric authentication systems based on EEG and gait data. Our future work will focus on deploying the DeepKey system in an online real-world environment. In addition, the gait signals are currently gathered by three wearable IMUs, which may obstruct the large-scale deployment in practice. Therefore, another direction in the future is to collect gait data from non-wearable gait solutions (e.g., sensors deployed in environments).

# REFERENCES

[1] Neamah Al-Naffakh, Nathan Clarke, Fudong Li, and Paul Haskell-Dowland. 2017. Unobtrusive gait recognition using smartwatches. In 2017 International Conference of the Biometrics Special Interest Group (BIOSIG’17). IEEE, 1–5.   
[2] Salahiddin Altahat, Girija Chetty, Dat Tran, and Wanli Ma. 2015. Analysing the robust EEG channel set for person authentication. In International Conference on Neural Information Processing. Springer, 162–173.   
[3] Corey Ashby, Amit Bhatia, Francesco Tenore, and Jacob Vogelstein. 2011. Low-cost electroencephalogram (EEG) based authentication. In 5th International IEEE/EMBS Conference on Neural Engineering (NER’11). IEEE, 442–445.   
[4] Md Khayrul Bashar, Ishio Chiaki, and Hiroaki Yoshida. 2016. Human identification from brain EEG signals using advanced machine learning method EEG-based biometrics. In IEEE EMBS Conference on Biomedical Engineering and Sciences (IECBES’16). IEEE, 475–479.   
[5] Nikolaos V. Boulgouris and Xiaxi Huang. 2013. Gait recognition using HMMs and dual discriminative observations for sub-dynamics analysis. IEEE Transactions on Image Processing 22, 9 (2013), 3636–3647.   
[6] Michele L. Callisaya, Leigh Blizzard, Michael D. Schmidt, Jennifer L. McGinley, Stephen R. Lord, and Velandai K. Srikanth. 2009. A population-based study of sensorimotor factors affecting gait in older people. Age and Ageing 38, 3 (2009), 290–295.   
[7] William Chan, Navdeep Jaitly, Quoc V. Le, Oriol Vinyals, and Noam M. Shazeer. 2017. Speech recognition with attention-based recurrent neural networks. U.S. Patent No. 9,799,327 [P]. 2017-10-24.

[8] John Chuang, Hamilton Nguyen, Charles Wang, and Benjamin Johnson. 2013. I think, therefore I am: Usability and security of authentication using brainwaves. In International Conference on Financial Cryptography and Data Security. Springer, 1–16.   
[9] Guglielmo Cola, Marco Avvenuti, Fabio Musso, and Alessio Vecchio. 2016. Gait-based authentication using a wristworn device. In Mobiquitous. ACM, 208–217.   
[10] John G. Daugman. 1993. High confidence visual recognition of persons by a test of statistical independence. IEEE Transactions on Pattern Analysis and Machine Intelligence 15, 11 (1993), 1148–1161.   
[11] Mohammad Derawi and Iurii Voitenko. 2014. Fusion of gait and ECG for biometric user authentication. In International Conference of the Biometrics Special Interest Group (BIOSIG’14). IEEE, 1–4.   
[12] Manqing Dong, Lina Yao, Xianzhi Wang, Boualem Benatallah, Xiang Zhang, and Quan Z. Sheng. 2019. Dual-stream self-attentive random forest for false information detection. In 2019 International Joint Conference on Neural Networks (IJCNN’19). IEEE, 1–8.   
[13] Hassen Drira, Boulbaba Ben Amor, Anuj Srivastava, Mohamed Daoudi, and Rim Slama. 2013. 3D face recognition under expressions, occlusions, and pose variations. IEEE Transactions on Pattern Analysis and Machine Intelligence 35, 9 (2013), 2270–2283.   
[14] Geof H. Givens, J. Ross Beveridge, Yui Man Lui, David S. Bolme, Bruce A. Draper, and P. Jonathon Phillips. 2013. Biometric face recognition: From classical statistics to future challenges. Wiley Interdisciplinary Reviews: Computational Statistics 5, 4 (2013), 288–308.   
[15] Steven Goldstein. 2016. Methods and systems for voice authentication service leveraging networking. U.S. Patent No. 9,282,096 [P]. 2016-3-8.   
[16] Qiong Gui, Zhanpeng Jin, and Wenyao Xu. 2014. Exploring EEG-based biometrics for user identification and authentication. In 2014 IEEE Signal Processing in Medicine and Biology Symposium (SPMB’14). IEEE, 1–6.   
[17] Ana M. Guzman, Mohammed Goryawala, Jin Wang, Armando Barreto, Jean Andrian, Naphtali Rishe, and Malek Adjouadi. 2013. Thermal imaging as a biometrics approach to facial signature authentication. IEEE Journal of Biomedical and Health Informatics 17, 1 (2013), 214–222.   
[18] Thang Hoang and Deokjai Choi. 2014. Secure and privacy enhanced gait authentication on smart phone. The Scientific World Journal 2014, 438254 (2014).   
[19] Isuru Jayarathne, Michael Cohen, and Senaka Amarakeerthi. 2016. BrainID: Development of an EEG-based biometric authentication system. In 2016 IEEE 7th Annual Information Technology, Electronics and Mobile Communication Conference (IEMCON’16). IEEE, 1–6.   
[20] Sarineh Keshishzadeh, Ali Fallah, and Saeid Rashidi. 2016. Improved EEG based human authentication system on large dataset. In 24th Iranian Conference on Electrical Engineering (ICEE’16). IEEE, 1165–1169.   
[21] Nefissa Khiari-Hili, Christophe Montagne, Sylvie Lelandais, and Kamel Hamrouni. 2016. Quality dependent multimodal fusion of face and iris biometrics. In 6th International Conference on Image Processing Theory Tools and Applications (IPTA’16). IEEE, 1–6.   
[22] Diederik P. Kingma and Jimmy Ba. 2014. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 (2014).   
[23] Shinsuke Konno, Yoshitaka Nakamura, Yoh Shiraishi, and Osamu Takahashi. 2015. Gait-based authentication using trouser front-pocket sensors. International Workshop on Informatics (2015).   
[24] Pavan K. Kumar, PESN Krishna Prasad, M. V. Ramakrishna, and B. D. C. N. Prasad. 2013. Feature extraction using sparse SVD for biometric fusion in multimodal authentication. International Journal of Network Security & Its Applications 5, 4 (2013), 83.   
[25] Worapan Kusakunniran, Qiang Wu, Jian Zhang, Hongdong Li, and Liang Wang. 2014. Recognizing gaits across views through correlated motion co-clustering. IEEE Transactions on Image Processing 23, 2 (2014), 696–709.   
[26] Worapan Kusakunniran, Qiang Wu, Jian Zhang, Yi Ma, and Hongdong Li. 2013. A new view-invariant feature for cross-view gait recognition. IEEE Transactions on Information Forensics and Security 8, 10 (2013), 1642–1653.   
[27] Neal S. Latman and Emily Herb. 2013. A field study of the accuracy and reliability of a biometric iris recognition system. Science & Justice 53, 2 (2013), 98–102.   
[28] Yann LeCun, Léon Bottou, Genevieve B. Orr, and Klaus-Robert Müller. 1998. Efficient backprop. In Neural Networks: Tricks of the Trade. Springer, 9–50.   
[29] Tran Long, Le Thai, and Tran Hanh. 2012. Multimodal biometric person authentication using fingerprint, face features. PRICAI 2012: Trends in Artificial Intelligence (2012), 613–624.   
[30] Dario Maio, Davide Maltoni, Raffaele Cappelli, James L. Wayman, and Anil K. Jain. 2002. FVC2002: Second fingerprint verification competition. In Proceedings of the 16th International Conference on Pattern Recognition, 2002, Vol. 3. IEEE, 811–814.   
[31] Ju Man and Bir Bhanu. 2006. Individual recognition using gait energy image. IEEE Transactions on Pattern Analysis and Machine Intelligence 28, 2 (2006), 316–322.

[32] B. E. Manjunathswamy, Appaji M. Abhishek, J. Thriveni, K. R. Venugopal, and L. M. Patnaik. 2015. Multimodal biometric authentication using ECG and fingerprint. International Journal of Computer Applications 111, 13 (2015).   
[33] Sebastien Marcel and José del R. Millán. 2007. Person authentication using brainwaves (EEG) and maximum a posteriori model adaptation. IEEE Transactions on Pattern Analysis and Machine Intelligence 29, 4 (2007).   
[34] Daigo Muramatsu, Akira Shiraishi, Yasushi Makihara, Md Zasim Uddin, and Yasushi Yagi. 2015. Gait-based person recognition using arbitrary view transformation model. IEEE Transactions on Image Processing 24, 1 (2015), 140–154.   
[35] C. Y. Yam and Mark Nixon. 2009. Model-based gait recognition. In Encyclopedia of Biometrics. Springer, 633–639.   
[36] Jaishanker K. Pillai, Maria Puertas, and Rama Chellappa. 2014. Cross-sensor iris recognition through kernel learning. IEEE Transactions on Pattern Analysis and Machine Intelligence 36, 1 (2014), 73–85.   
[37] Kun Qian, Chenshu Wu, Zheng Yang, Zimu Zhou, Xu Wang, and Yunhao Liu. 2018. Enabling phased array signal processing for mobile WiFi devices. IEEE Transactions on Mobile Computing 17, 8 (2018), 1820–1833.   
[38] Fahreddin Sadikoglu and Selin Uzelaltinbulat. 2016. Biometric retina identification based on neural network. Procedia Computer Science 102 (2016), 26–33.   
[39] Bing Sun, Yang Wang, and Jacob Banda. 2014. Gait characteristic analysis and identification based on the iPhone’s accelerometer and gyrometer. Sensors 14, 9 (2014), 17037–17054.   
[40] Rupali L. Telgad, P. D. Deshmukh, and Almas M. N. Siddiqui. 2014. Combination approach to score level fusion for Multimodal Biometric system by using face and fingerprint. In Recent Advances and Innovations in Engineering (ICRAIE), 2014. IEEE, 1–8.   
[41] Kavitha P. Thomas and A. P. Vinod. 2016. Utilizing individual alpha frequency and delta band power in EEG based biometric recognition. In IEEE International Conference on Systems, Man, and Cybernetics (SMC’16). IEEE, 004787– 004791.   
[42] Kavitha P. Thomas and A. P. Vinod. 2017. EEG-based biometric authentication using gamma band power during rest state. Circuits, Systems, and Signal Processing (2017), 1–13.   
[43] J. A. Unar, Woo Chaw Seng, and Almas Abbasi. 2014. A review of biometric technology along with trends and prospects. Pattern Recognition 47, 8 (2014), 2673–2688.   
[44] Yequan Wang, Minlie Huang, Li Zhao, et al. 2016. Attention-based LSTM for aspect-level sentiment classification. In EMNLP. 606–615.   
[45] Zifeng Wu, Yongzhen Huang, Liang Wang, Xiaogang Wang, and Tieniu Tan. 2017. A comprehensive study on crossview gait based human identification with deep CNNs. IEEE Transactions on Pattern Analysis and Machine Intelligence 39, 2 (2017), 209–226.   
[46] Weitao Xu, Guohao Lan, Qi Lin, Sara Khalifa, Mahbub Hassan, Neil Bergmann, and Wen Hu. 2018. Keh-gait: Using kinetic energy harvesting for gait-based user authentication systems. IEEE Transactions on Mobile Computing 18, 1 (2018), 139–152.   
[47] Vitor Yano, Alessandro Zimmer, and Lee Luan Ling. 2012. Multimodal biometric authentication based on iris pattern and pupil light reflex. In 21st International Conference on Pattern Recognition (ICPR’12). IEEE, 2857–2860.   
[48] Lina Yao, Quan Z Sheng, Xue Li, Tao Gu, Mingkui Tan, Xianzhi Wang, Sen Wang, and Wenjie Ruan. 2018. Compressive representation for device-free activity recognition with passive RFID signal strength. IEEE Transactions on Mobile Computing 17, 2 (2018), 293–306.   
[49] Lina Yao, Quan Z. Sheng, Xue Li, Sen Wang, Tao Gu, Wenjie Ruan, and Wan Zou. 2015. Freedom: Online activity recognition via dictionary-based sparse representation of RFIID sensing data. In 2015 IEEE International Conference on Data Mining. IEEE, 1087–1092.   
[50] Xiang Zhang, Lina Yao, Salil S. Kanhere, Yunhao Liu, Tao Gu, and Kaixuan Chen. 2018. MindID: Person identification from brain waves through attention-based recurrent neural network. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 2, 3 (2018), 149.   
[51] Xiang Zhang, Lina Yao, Xianzhi Wang, Jessica Monaghan, and David Mcalpine. 2019. A survey on deep learning based brain computer interface: Recent advances and new frontiers. arXiv preprint arXiv:1905.04149 (2019).   
[52] Hailing Zhou, Ajmal Mian, Lei Wei, Doug Creighton, Mo Hossny, and Saeid Nahavandi. 2014. Recent advances on singlemodal and multimodal face recognition: A survey. IEEE Transactions on Human-Machine Systems 44, 6 (2014), 701–716.

Received June 2019; revised January 2020; accepted April 2020