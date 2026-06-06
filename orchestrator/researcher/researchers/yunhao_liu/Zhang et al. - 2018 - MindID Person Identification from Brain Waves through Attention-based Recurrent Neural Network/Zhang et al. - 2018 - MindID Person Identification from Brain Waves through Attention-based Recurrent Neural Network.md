# MindID: Person Identification from Brain Waves through Attention-based Recurrent Neural Network

XIANG ZHANG, University of New South Wales, AU

LINA YAO, University of New South Wales, AU

SALIL S. KANHERE, University of New South Wales, AU

YUNHAO LIU, Tsinghua University, China

TAO GU, RMIT University, AU

KAIXUAN CHEN, University of New South Wales, AU

Person identification technology recognizes individuals by exploiting their unique, measurable physiological and behavioral characteristics. However, the state-of-the-art person identification systems have been shown to be vulnerable, e.g., antisurveillance prosthetic masks can thwart face recognition, contact lenses can trick iris recognition, vocoder can compromise voice identification and fingerprint films can deceive fingerprint sensors. EEG (Electroencephalography)-based identification, which utilizes the user’s brainwave signals for identification and offers a more resilient solution, draw a lot of attention recently. However, the accuracy still requires improvement and very little work is focusing on the robustness and adaptability of the identification system. We propose MindID, an EEG-based biometric identification approach, achieves higher accuracy and better characteristics. At first, the EEG data patterns are analyzed and the results show that the Delta pattern contains the most distinctive information for user identification. Then the decomposed Delta pattern is fed into an attention-based Encoder-Decoder RNNs (Recurrent Neural Networks) structure which assigns varies attention weights to different EEG channels based on the channel’s importance. The discriminative representations learned from the attention-based RNN are used to recognize the user’ identification through a boosting classifier. The proposed approach is evaluated over 3 datasets (two local and one public). One local dataset (EID-M) is used for performance assessment and the result illustrate that our model achieves the accuracy of 0.982 which outperforms the baselines and the state-of-the-art. Another local dataset (EID-S) and a public dataset (EEG-S) are utilized to demonstrate the robustness and adaptability, respectively. The results indicate that the proposed approach has the potential to be largely deployment in practice environment.

CCS Concepts: • Security and privacy → Biometrics; • Computing methodologies → Machine learning algorithms.

Additional Key Words and Phrases: EEG, biometric identification, EEG pattern decomposition, deep learning

# ACM Reference Format:

Xiang Zhang, Lina Yao, Salil S. Kanhere, Yunhao Liu, Tao Gu, and Kaixuan Chen. 2017. MindID: Person Identification from Brain Waves through Attention-based Recurrent Neural Network. ACM J. Comput. Cult. Herit. 9, 4, Article 39 (March 2017), 20 pages. https://doi.org/0000001.0000001

# 1 INTRODUCTION

Over the past decade, biometric information have been widely used in identification and have gained more acceptance due to their reliability and adaptability. Existing biometric identification systems are mainly based on

Authors’ addresses: Xiang Zhang, University of New South Wales, CSE, UNSW, Sydney, NSW, 2052, AU; Lina Yao, University of New South Wales, CSE, UNSW, Sydney, NSW, 2052, AU; Salil S. Kanhere, University of New South Wales, CSE, UNSW, Sydney, NSW, 2052, AU; Yunhao Liu, Tsinghua University, School of Software, Tsinghua University, Beijing, Beijing, 100084, China; Tao Gu, RMIT University, , Melbourne, VIC, 3001, AU; Kaixuan Chen, University of New South Wales, CSE, UNSW, Sydney, NSW, 2052, AU.

ACM acknowledges that this contribution was authored or co-authored by an employee, contractor, or affiliate of the United States government. As such, the United States government retains a nonexclusive, royalty-free right to publish or reproduce this article, or to allow others to do so, for government purposes only.

© 2017 Association for Computing Machinery.

XXXX-XXXX/2017/3-ART39 \$15.00

https://doi.org/0000001.0000001

individuals’ unique intrinsic physiological features (e.g., face [10], iris [18], retina [25], voice [11], and fingerprint [31]). However, the state-of-the-art person identification systems have been shown to be vulnerable, e.g., antisurveillance prosthetic masks can thwart face recognition, contact lenses can trick iris recognition, vocoder can compromise voice identification and fingerprint films can deceive fingerprint sensors.

The EEG (Electroencephalography) signal-based system is an emerging approach in physiological biometrics. Such systems measure an individual’s brain response to a number of stimuli in the form of EEG signals, which record the electromagnetic, invisible, and untouchable electrical neural oscillations. These characteristics enable EEG-based identification highly attack-resilient and escape from the threat of being deceived which is often faced by other identification techniques. For example, people can easily trick a fingerprint-based identification system by using a fake fingerprint film1 or a face-recognition-based identification system by simply wearing a 200 dollars’ worth anti-surveillance mask2. EEG signals, compared with other biometrics, have the following significant inherent advantages [8, 27]:

• Attack-Resilience. EEG data is invisible and untouchable and is impossible to be cloned and duplicated. Therefore, an EEG-based identification system is strengthened to verify human ID and robust against faked identities.   
• Universality. One’s EEG signals are typically associated with the subject all the time and hence security can be enforced anywhere and anytime.   
• Uniqueness. Each individual processes his/her EEG signals which are unique, independent and different from other’s [12]. This can potentially achieve high identification accuracy.   
• Accessibility. We have seen an increasing effort in recent years in the development of low-cost and easy-towear EEG headsets. For example, the behind-the-ear EEG collection equipment[15] can be easily attached to the ear (similar to wireless earphone).

We put up a table showing the comparison of EEG with other biometric information on several key characteristics in Table 1. EEG signals stand out in a number of aspects, and hence attract many research work in EEG-based biometric identification. For instance, Chuang et al. [8] propose a single-channel EEG-based identification system and Sarineh Keshishzadeh et al. [14] employ a statistical model for analyzing EEG signals.

Despite the efforts done recently, the research work in EEG-based identification is still in its early stage, and several key challenges exist. One of the most significant challenges is poor stability (the identification system may work well at one time but fail another time due to the EEG signals are easy to be interfered). This may due to the user’s physiological and psychological states such as fatigue and angry [30, 33]. Intuitively, the states shift brought by the fluctuation of user states can be divided into two categories: the dramatically shift (e.g., hysterical, drunk, or under threaten) and the slight shift (e.g., headache or exciting). On one hand, the EEG signals divergence bought by the former can help to enhance the robustness of the identification system. For example, the phenomena could enhance the security of the identification system that it fails to recognize the subject who is under threatening (e.g., Hijacked by kidnapper). On the other hand, however, the latter will reduce the signal quality but more commonly occurred in the real world. For instance, the identification system could identify the user when s/he is happy but fail when upset. Thus the slight shift should be overcome for its negative effect. To eliminate the interference of the slight shift brought by the daily physical and mental states, we attempt to learn the robust and reliable representation via EEG pattern decomposition. Pattern decomposition is to decompose the full-frequency EEG signals into a specific pattern (Delta, Theta, Alpha, Beta, and Gamma). Pattern decomposition of EEG signals has been employed on EEG signal classification (e.g., movement task classification [23]) for a long time. However, few attentions are paid to the Delta pattern. In this paper, we discover that the Delta pattern is the most discriminative and efficient pattern through our analysis in Section 3.

Another challenge is performance issue such as accuracy, robustness, and adaptability. The most recent identification systems can achieve a range from 80% to 95% [6, 14, 17, 21, 29], which is not enough for practical deployment in many confidential scenarios. Also, the identification algorithms rely much on the EEG collecting environment. The shifting of application environment (e.g., the number of channels, the sampling rate, and the training data size) may lead to the decrease of accuracy3. This refers to that the existing EEG-based identification model may work well under one kind of application environment (e.g., 64 channels and 160 Hz), but could not handle another application environment (e.g., 14 channels and 128 Hz). So far, we have not seen a universal EEG-based identification algorithm which can performance good in a variety of real environments. To address this challenge, we introduce the attention-based RNNs (Recurrent Neural Networks) [4] which can automatically detect the most useful information from input data no matter what the environment is. More importantly, the attention mechanism4 would automatically re-allocate the weights to extract most discriminative features according to the change of environmental factors. The efficiency of attention-based RNN framework has been demonstrated by the studies in areas such as speech recognition [4], NLP (Natural Language Processing) [3], and computer version [20].

To address the aforementioned problems, we propose MindID, a Delta pattern EEG-based person identification algorithm through an attention-based recurrent neural network. Our main contributions of this paper are highlighted as follows:

• We present an EEG-based identification approach, MindID, which adopts a novel attention-based Encoder-Decoder RNN framework for learning discriminative features among the user’s brainwaves and utilizes the learned features to identify user ID through a boosting classifier. The attention mechanism enables our approach to automatically search the most discriminative features for identification, consequently, to operate robust and adaptive over different datasets and collecting environment.   
• We analyze the EEG pattern decomposition and propose that the Delta pattern is the most steady and distinguishable pattern for user identification. Moreover, we design and conduct a set of experiments to verify the proposed hypothesis.   
• We design and conduct an EEG experiment along with collecting two real-world local dataset (EID-M and EID-S) which are separately collected under single-trial and multi-trial5.   
• We evaluate the proposed approach on 3 datasets (2 local and 1 public). The results illustrate that our model achieves an accuracy of 0.982 which outperforms the state-of-the-art and baselines. We demonstrate the robustness and adaptability by the comparison between 3 datasets.

Note that all the necessary reusable codes and datasets in this paper have been open-sourced for reproduction, please refer to this link 6.

The remainder of this paper is organized as follows. Section 2 introduces the literature related to this paper. Section 3 analyzes the characteristics of EEG patterns. Section 4 details the methodology of the MindID identification system. Section 5 evaluates the proposed approach on the local and public dataset and provides analysis of the experimental results. Section 6 discussed the limitation of our work and the future research potentials. Finally, Section 7 summarizes this paper and gives the conclusion.

Table 1. Comparison of various biometrics. EEG have considerable rttack-resilient which is the most significant character of identification systems. ↑ denotes the higher the better while ↓ denotes the lower the better. 

<table><tr><td>Biometrics</td><td>Attack-Resilient ↑</td><td>Universality ↑</td><td>Uniqueness ↑</td><td>Stability ↑</td><td>Accessibility ↑</td><td>Performance ↑</td><td>Computational cost ↓</td></tr><tr><td>Face/Vedio</td><td>Medium</td><td>Medium</td><td>Low</td><td>Low</td><td>High</td><td>Low</td><td>High</td></tr><tr><td>Fingerprint/Palmprint</td><td>Low</td><td>High</td><td>High</td><td>High</td><td>Medium</td><td>High</td><td>Medium</td></tr><tr><td>Iris</td><td>Medium</td><td>High</td><td>High</td><td>High</td><td>Medium</td><td>High</td><td>High</td></tr><tr><td>Retina</td><td>High</td><td>Medium</td><td>High</td><td>Medium</td><td>Low</td><td>High</td><td>High</td></tr><tr><td>Signature</td><td>Low</td><td>High</td><td>Low</td><td>Low</td><td>High</td><td>Low</td><td>Medium</td></tr><tr><td>Voice</td><td>Low</td><td>Medium</td><td>Low</td><td>Low</td><td>Medium</td><td>Low</td><td>Low</td></tr><tr><td>face</td><td>Medium</td><td>High</td><td>Medium</td><td>Medium</td><td>Medium</td><td>Medium</td><td>High</td></tr><tr><td>Gait</td><td>High</td><td>Medium</td><td>High</td><td>Medium</td><td>Medium</td><td>High</td><td>Low</td></tr><tr><td>EEG</td><td>High</td><td>High</td><td>High</td><td>Low</td><td>Medium</td><td>High</td><td>Low</td></tr></table>

# 2 RELATED WORK

In this section, we separately present literature on three aspects: the EEG-based person identification models, the EEG pattern decomposition, and the attention-based RNN application.

# 2.1 EEG-based person identification

Since EEG can be gathered in a safe and non-intrusive way, researchers have paid great attention to exploring this kind of brain signals. For person identification, EEG is promising for being confidential and attack-resilient but on the other hand, complex and hard to be analyzed. Marcel and Millán [21] use Gaussian Mixture Models and train client models with Maximum A Posteriori (MAP). Ashby et al. [2] extract five sets of features from EEG electrodes and inter-hemispheric data, combine them together, and process the final features with support vector machine (SVM). The study shows that EEG identification is also feasible with less-expensive devices. Altahat et al. [1] select Power Spectral Density (PSD) as the feature instead of the widely used autoregressive (AR) models to get higher accuracy. They also conduct channel selection to determine contributing channels among all 64 channels. Thomas and Vinod [29] take advantage of individual alpha frequency (IAF) and delta band signals to compose specific feature vector. They also prefer PSD features but only perform the extraction merely on gamma band. Most of the identification algorithms are concentrating on a specific application environment. Few studies attempt to build a universal EEG-based identification model.

# 2.2 EEG pattern decomposition

Generally, the EEG data could be decomposed into several patterns (delta, theta, alpha, beta, and gamma) corresponding to various brain states [19]. So far, the majority of user ID identification studies are exploiting the features of Alpha and Beta pattern[17, 27]. In particular, most EEG based identification models are work on the situation that the subject keeps rest/relax (under Alpha pattern) or concentrating state (under Beta pattern) for the high data quality. The rest and relax states are represented by the Alpha wave, therefore, a number of studies decompose EEG raw signals into the Alpha pattern for future analysis. Sohankar et al. [27] extract Alpha pattern features for identification and authentication. Bashar et al. [6] use the filtered signals with frequency ranges from 0.5 − 59???? (including Delta, Theta, Alpha, Beta and part of Gamma patterns) and calculate the statistics for user ID classification. Kumari and Vaish [17] employ wavelet analysis to decompose original EEG signals into 5 patterns and extract statistical measures of each pattern. Thomas and Vinod [29] take Alpha peak frequency and peak power and Delta band power as recognition features and achieves the highest recognition rate as 0.9. To our best knowledge, this paper is the very first work which specialized focus on the decomposition and analysis of Delta pattern and studies the person identification based on it (the justification is given in Section 3).

Table 2. EEG patterns and corresponding characters. Awareness Degree denotes the awareness the degree of being aware of an external world. 

<table><tr><td>Patterns</td><td>Frequency (Hz)</td><td>Amplitude</td><td>Brain State</td><td>Awareness Degree</td><td>Produced Location</td></tr><tr><td>Delta</td><td>0.5-4</td><td>Higher</td><td>Deep sleep pattern</td><td>Lower</td><td>Frontally and posteriorly</td></tr><tr><td>Theta</td><td>4-8</td><td>High</td><td>Light sleep pattern</td><td>Low</td><td>Entorhinal cortex, hippocampus</td></tr><tr><td>Alpha</td><td>8-12</td><td>Medium</td><td>Closing the eyes, relax state</td><td>Medium</td><td>Posterior regions of head</td></tr><tr><td>Beta</td><td>12-30</td><td>Low</td><td>Active thinking, focus, high alert, anxious</td><td>High</td><td>Most evident frontally</td></tr><tr><td>Gamma</td><td>30-100</td><td>Lower</td><td>During cross-modal sensory processing</td><td>Higher</td><td>Somatosensory cortex</td></tr></table>

# 2.3 Attention-based RNN Model

Attention-based RNN model [20] refers to introduce attention mechanism to the RNN framework. The attention mechanism enables RNN algorithm to allocate different weights to different parts of the input, and consequently, improve the exploration of the corresponding relationship between the input sequence and the output sequence. Generally, attention module is added to the original RNN framework as an external module, however, the attention module is trained instantaneously with the RNN structure [32]. Attention-based RNN model has achieves success in speech recognition [4], NLP (Natural Language Processing) [3], and computer version [20]. Bahdanau et al. [4] attempt to build a Large Vocabulary Continuous Speech Recognition (LVCSR) Systems by attention-based RNN and demonstrate this approach, compared with traditional methods, requires fewer training stages, less auxiliary data, and less domain expertise. Luong et al. [3] explore the architecture of attention-based neural machine translation and exam the effects of two attentional mechanism (attends to all source words and attends to a subset of words) on the WMT translation tasks between English and German in both directions. Ba et al. [20] present an attention-based RNN model for recognizing multiple objects in images, which is attempts to recognize multiple objects despite being given only class labels during training. The results show that the attention-based RNN is more accurate and uses less computation than the state-of-the-art. However, few work is taken based on attention mechanism in EEG related area. To our best knowledge, we are the very first work employing attention-based RNN model on the EEG-based user identification topic.

# 3 EEG PATTERN ANALYSIS

In this section, we first introduce the basic knowledge of EEG patterns and then analyze the relationship between EEG patterns and individual states. Moreover, we propose a hypothesis to capture the most distinctive features to distinguish the subject’s identity.

In practical EEG data analysis, the assembled EEG signals can be divided into several different frequency patterns (delta, theta, alpha, beta, and gamma) based on the strong intra-band correlation with a distinct behavioral state [5, 19, 28]. Each decomposed EEG pattern contains signals associated with particular brain information. The EEG frequency patterns and the corresponding characters are listed in Table 2. The awareness degree denotes the perception of individuals while facing outside stimuli. Each EEG patterns represents a specific active situation of brain state and a qualitative assessment of awareness. More specifically,

• Delta pattern (0.5 − 4 Hz) is associated with deep sleep while the subject has lower awareness.   
• Theta pattern (4 − 8 Hz) being presented during light sleep, is the realm of the low awareness state.   
• Alpha pattern (8 − 12 Hz) mainly occurs during eye closed and deeply relax state, lies at the medium awareness.   
• Beta pattern (12 − 30 Hz) is the dominant rhythm while the subject keeps eye-opening and claims high awareness. Most of the human daily activities (such as eating, walking, and talking) are under Beta pattern.   
• Gamma pattern (30 − 100 Hz) representing the co-work of several brain areas to carry out a specific motor and cognitive function. This pattern is associated with higher awareness.

Table 3. The inter-subject correlation coefficients. Full denotes the un-decomposed full-frequency band data. The lower coefficients indicate that the subject’s EEG data is easier to be distinguished. The data come from the EID-M dataset (detailed in Section 5.1). 

<table><tr><td>Subject</td><td></td><td>Subject 1</td><td>Subject 2</td><td>Subject 3</td><td>Subject 4</td><td>Subject 5</td><td>Subject 6</td><td>Subject 7</td><td>Subject 8</td><td>STD</td><td>Average</td></tr><tr><td rowspan="6">Patterns</td><td>Delta</td><td>0.137</td><td>0.428</td><td>0.246</td><td>0.179</td><td>0.221</td><td>0.119</td><td>0.187</td><td>0.239</td><td>0.089554</td><td>0.219</td></tr><tr><td>Theta</td><td>0.447</td><td>0.671</td><td>0.552</td><td>0.31</td><td>0.387</td><td>0.207</td><td>0.199</td><td>0.386</td><td>0.151929</td><td>0.395</td></tr><tr><td>Alpha</td><td>0.387</td><td>0.629</td><td>0.615</td><td>0.377</td><td>0.299</td><td>0.306</td><td>0.283</td><td>0.457</td><td>0.128653</td><td>0.419</td></tr><tr><td>Beta</td><td>0.249</td><td>0.487</td><td>0.329</td><td>0.308</td><td>0.281</td><td>0.307</td><td>0.238</td><td>0.441</td><td>0.083224</td><td>0.33</td></tr><tr><td>Gamma</td><td>0.528</td><td>0.692</td><td>0.538</td><td>0.362</td><td>0.521</td><td>0.667</td><td>0.428</td><td>0.537</td><td>0.102288</td><td>0.534</td></tr><tr><td>full</td><td>0.333</td><td>0.329</td><td>0.408</td><td>0.304</td><td>0.297</td><td>0.621</td><td>0.302</td><td>0.447</td><td>0.104231</td><td>0.38</td></tr></table>

We claim that the EEG patterns are internally related with the awareness degree. As shown in Table 2: with the increase of band frequency (from Delta pattern, Theta pattern, Alpha pattern, Beta pattern to Gamma pattern), the awareness degree is increasing. The above statement can be inferred by the following two factors. First, EEG pattern is relevant to brain neuron activity. In essence, EEG signals are measured by the voltage fluctuations which are resulted from the ionic current within the neuron activity of the brain [22]. Second, the awareness degree is associated with the brain neuron activity. Intuitively, the higher awareness the subject has, the more neurons are activated. In particular, more and more brain areas are activated while the subject’s awareness is higher and higher (the brain state changes from deep sleep, light sleep, to normal awake). At the same time, more neural cells are aroused and more function are attached. As a result, more complex and blend EEG signals are produced by the brain.

Additionally, we know that the awareness of human is naturally connected with individuals’ mental and physical states (organics and systems) [9, 24]. For example, while the subject is under lower awareness situation (like deep sleep, Delta pattern), the most parts of physical functions of the body (such as sensing, thinking, even dreaming) are completely detached. Only the very essential life-support organs and systems (such as breathing, heart beating, and digesting) keep working. While the subject is under medium awareness state (like eye relaxation, Alpha pattern), the subject has more activated functions such as imaging, visualizing and concentrating. Also, more brain functions like hearing, touching, and thinking are attached, which means that more physical brain areas (such as frontal lobe, temporal lobe, and parietal lobe) are activated.

According to the above two statements, it can be inferred that the EEG patterns are associated with individuals’ mental and physical states (organics and systems). Note, under the medium awareness situation, the life-support systems which worked under lower awareness situation are still working. Which means that while the subject has high-degree awareness, his or her EEG signals contain both high-degree and low-degree awareness at the same time. The pattern (with low-degree awareness) is not replaced by another pattern (with high-degree awareness) but included by the latter. Specifically, Delta pattern is not replaced but included in other patterns. In other word, Delta pattern exists in all the brain states7 (e.g., deep sleep, light sleep, relax, and focus).

For identification techniques, the EEG signals feature should satisfy two demands: steady and distinguishable. The steady means that the system should be robustness enough to identify the user even when the user’s mental or physical states have tiny fluctuation (such as tired). The distinguishable refers that the EEG signals should vary with the different subject. Based on the analyzed conclusion, we claim a hypothesis that Delta pattern contains the most steady and distinctive information for user identification. This hypothesis will be demonstrated both qualitatively and quantitatively.

Here we attempt to qualitatively demonstrate the hypothesis based on the relationship between EEG patterns and human states. At first, Delta pattern naturally keeps steady under different situations since it is produced by and only related with the basic life-support systems. Comparatively, other EEG patterns like the Alpha pattern is unsteady and it could be easily influenced by subject states and environmental factors (such as fatigue, emotion, and noise). The higher consciousness, the easier to be influenced by the noise. In addition, the life-support systems are associated with the physiological characteristics of different subjects, which enables Delta pattern distinguishing. Then we present the quantitative demonstration. To find the best pattern for user ID recognition, we analyze the inter-subject correlations of EEG decomposed pattern. The inter-subject correlations, measured by the correlation coefficient, denotes that the connection of the same pattern but from different subjects. For example, the inter-subject Alpha pattern correlations of subject 1 are calculated by the Pearson correlation coefficient between the Alpha signal (belong to subject 1) and another Alpha signal (belong to another subject). In practical, we select a set of samples and measure the average level. The correlation coefficient analysis results are shown in Table 3. In which, we can observe that the Delta pattern has the lowest correlation coefficients compared with other patterns. This consequence indicates that Delta pattern is enabled to achieve the best performance for the user identification. Furthermore, the comparative experiment between different EEG patterns will be reported in Section 5.6.

![](images/c80ee359348e3d6885a2d65578dff0e72fcf15a78a69beabeaf5f742ee3a4c92.jpg)



Fig. 1. Flowchart of the proposed approach. In the beginning of identification, EEG raw data ?? is collected from the user and then be transmitted to preprocessing stage. The preprocessed data $E ^ { \prime }$ is decomposed to Delta pattern ?? which is regarded as the input of the attention-based RNN. The encoder compresses the input sequence $X ^ { 1 }$ into an intermediate coder ?? and produces the weights $W _ { a t t } ^ { \prime }$ at the same time. The attention-based module accepts both ?? and $W _ { a t t } ^ { \prime }$ from the LSTM layer $X ^ { i ^ { \prime } }$ , processes $W _ { a t t } ^ { \prime }$ through a softmax layer, and calculates the attention-based code $C _ { a t t }$ . Assess the representation ability of $C _ { a t t }$ via the decoder and utilize it to identify the user ID in the identification step.

# 4 METHODOLOGY

In this section, we first give an overview of the proposed MindID system and then present the technical details for each component, namely, Preprocessing, EEG pattern decomposition, Attention-based RNN, and Classification.

# 4.1 Overview

Figure 1 outlines the specific steps of the proposed MindID system. The brainwave is collected by the portable EEG acquisition equipment while the user closed his/her eyes and keep relaxation. Under relaxation mental and physical states, the EEG signals are supposed to be more stable and reliable. Each EEG data is a numerical feature vector with N dimensions which corresponding to the N channels of the wearable EEG headset. The EEG samples are first preprocessed to remove the Direct Current (DC) offset and normalize the signals (Section 4.2). Next, we employ EEG pattern decomposition to isolate the Delta waves from preprocessed data since they contain the most distinctive information which can be used to identify the subject (as outlined in Section 3). The delta waves are fed to an attention-based Encoder-Decoder RNN model, which identifies the most distinctive channels and adjusts the weights accordingly. The attention-based RNN model accepts Delta pattern signals and explores the deep correlations between Delta pattern. The learned deep representations are fed into a statistical boosting classifier (Section 4.5) to recognize the user ID.

# 4.2 Preprocessing

The raw EEG samples are pre-processed to remove the DC offset and normalize the signals.

Eliminating DC offset is necessary because EEG collection headsets invariably introduce a constant noise component in the recorded signals. The specific headset used in our experiments (details in Section 5) introduces a DC offset of 4200 muV8. In the preprocessing stage, this constant DC offset is first subtracted from the raw signal E.

Normalization also plays a crucial role in a knowledge discovery process for handling different units and scales of features. For example, given one raw data dimension ranges from 0 to 1 while another dimension ranges from 0 to 100, the analysis results will be dominated by the latter. Generally, there are three widely used normalization methods: Min-Max Normalization, Unity Normalization, and Z-score Scaling Normalization [34]. Our experiments (not shown for brevity) indicated that Z-score scaling is the most suited for the EEG data. In summary, the preprocessed data ??′ can be calculated by

$$
E ^ {\prime} = \frac {(E - D C) - \mu}{\sigma}
$$

where ???? denotes the Direct Current which is 4200 muV, ?? denotes the mean of ?? − ???? and ?? denotes the standard deviation.

# 4.3 EEG Pattern Decomposition

In Section 3, we used empirical EEG data to show that the part of the EEG signals that belong to the Delta frequency band (0.5 − 4????) is particularly well-suited to identify user’s ID accurately and steady. To isolate the signals in the Delta band, we use a Butterworth band-pass filter of order 3 with the frequency range of 0.5Hz to 4Hz. The designed filter has following specifications: the order is three, the low cut is 0.5????, and the high cut is set as 4????. All dimensions of the preprocessed ??′ are fed into the band-pass filter in turn and finally get the decomposed Delta pattern ??.

# 4.4 Attention-based RNN

After EEG pattern decomposition, the composed Delta pattern ?? is fed into an attention-based Encoder-Decoder RNN structure [32] aims to learn more representable features for user identification. The general Encoder-Decoder RNN framework regards all the feature dimensions of input sequence has the same weights, no matter how important the dimension is for the output sequence. In our research, the different feature dimensions of the EEG data are corresponding to the different nodes of the EEG equipment. For example, the first dimension (first channel) collects the EEG data from the ???? 39 node which located at the frontal lobe of the scalp while the 7-th dimension is gathered from ??1 node at the occipital lobe. To assign varies weights to different dimensions of the brainwave data, we introduce the attention mechanism to the Encoder-Decoder RNN model. The proposed attention-based Encoder-Decoder RNN is consists of three components (as shown in Figure 1): the encoder, the attention module, and the decoder. The encoder is designed to compress the input Delta ?? wave into a single intermediate code ??; the attention module helps the encoder to calculate a better intermediate code $C _ { a t t }$ by generating a sequence of the weights $W _ { a t t }$ of different dimensions; the decoder accepts the attention-based code $C _ { a t t }$ and decode it to the user ID. Note, this user ID is predicted by the attention-based RNN instead of MindID, and the final identified ID of MindID approach will be introduced in Section 4.5.

Table 4. Notation 

<table><tr><td>Parameters</td><td>Explanation</td></tr><tr><td> $E$ </td><td>EEG raw data</td></tr><tr><td> $E'$ </td><td>Preprocessed EEG data</td></tr><tr><td> $\delta$ </td><td>Delta pattern of  $E'$ </td></tr><tr><td> $X^{i}$ </td><td>Data in the  $i$ -th layer in attention-based RNN</td></tr><tr><td> $I$ </td><td>The number of layers in attention-based RNN</td></tr><tr><td> $N^{i}$ </td><td>The number of dimensions of  $X^{i}$ </td></tr><tr><td> $Y$ </td><td>The one-hot label of user ID</td></tr><tr><td> $Y'$ </td><td>The attention-based RNN predicts user ID</td></tr><tr><td> $K$ </td><td>The number of user ID categories</td></tr><tr><td> $\mathcal{T}(\cdot)$ </td><td>The linear function</td></tr><tr><td> $C$ </td><td>The intermediate code</td></tr><tr><td> $\mathcal{L}(\cdot)$ </td><td>The output calculation procedure of LSTM cell</td></tr><tr><td> $\mathcal{L}'(\cdot)$ </td><td>The final hidden state calculation procedure of LSTM cell</td></tr><tr><td> $f_{i}, f_{f}, f_{o}, f_{m}$ </td><td>The input, forget, output, and input modulation gate</td></tr><tr><td> $W_{att}'$ </td><td>The unnormalized attention weights</td></tr><tr><td> $W_{att}$ </td><td>The normalized attention weights</td></tr><tr><td> $C_{att}$ </td><td>The attention-based intermediate code</td></tr><tr><td> $n_{iter}$ </td><td>The iteration threshold of attention-based RNN</td></tr><tr><td> $X_{D}$ </td><td>The learned deep feature from attention-based RNN</td></tr><tr><td> $x_{d}$ </td><td>A single sample in  $X_{D}$ </td></tr><tr><td> $m$ </td><td>The  $m$ -th tree</td></tr><tr><td> $M$ </td><td>The number of XGB trees</td></tr><tr><td> $I_{D}$ </td><td>The final identified user ID of MindID approach</td></tr></table>

Suppose the data in ??-th layer could be denoted by $X ^ { i } = ( X _ { i } ^ { i } ; i \in [ 1 , 2 , \cdots , I ] , j \in [ 1 , 2 , \cdots , N ^ { i } ] )$ where ?? denotes the ??-th dimension of $X ^ { i }$ . ?? represents the number of neural network layers in the proposed attention based RNN model while $N ^ { i }$ denotes the number of dimensions in ????. Take the first layer as an example, we have $X ^ { 1 } = \delta$ which indicates the input sequence is the Delta pattern. Let the output sequence be $Y = \left( Y _ { k } ; k \in \left[ 1 , 2 , \cdots , K \right] \right)$ ) where K denotes the number of user ID categories. In this paper, the user ID is represented by the one-hot label with length ??. For simplicity, let’s define the operation T (·) as:

$$
\mathcal {T} (X ^ {i}) = X ^ {i} W + b
$$

Further more, we have

$$
\mathcal {T} (X _ {j} ^ {i - 1}, X _ {j - 1} ^ {i}) = X _ {j} ^ {i - 1} * W ^ {\prime} + X _ {j - 1} ^ {i} * W ^ {\prime \prime} + b ^ {\prime}
$$

where $W , b , W ^ { \prime } , W ^ { \prime \prime } , b ^ { \prime }$ denote the corresponding weights and biases parameters.

The the encoder component contains several non-recurrent fully-connected neural network layers and one recurrent Long Short-Term Memory (LSTM) layer. The non-recurrent layers are employed to construct and fit a non-linear function to purify the input Delta pattern, the necessity is demonstrated by the preliminary experiments10. The data flow in these non-recurrent layers could be calculated by

$$
X ^ {i + 1} = \mathcal {T} (X ^ {i})
$$

The LSTM layer is adopted to compress the output of non-recurrent layers to a length-fixed sequence which is regarded as the intermediate code ??. Suppose LSTM is the ??′-th layer, the code equals to the output of LSTM, which is $C = X _ { j } ^ { i ^ { \prime } }$ . The $X _ { j } ^ { i ^ { \prime } }$ can be measured by

$$
X _ {j} ^ {i ^ {\prime}} = \mathcal {L} (c _ {j - 1} ^ {i ^ {\prime}}, X _ {j} ^ {i - 1}, X _ {j - 1} ^ {i ^ {\prime}}) \tag {1}
$$

where $c _ { j - 1 } ^ { i ^ { \prime } }$ denotes the hidden state of the $( j - 1 )$ -th LSTM cell. The operation $\mathcal { L } ( \cdot )$ denotes the calculation process of the LSTM structure, which can be inferred from the following equations

$$
X _ {j} ^ {i ^ {\prime}} = f _ {o} \odot t a n h (c _ {j} ^ {i ^ {\prime}})
$$

$$
c _ {j} ^ {i ^ {\prime}} = f _ {f} \odot c _ {j - 1} ^ {i ^ {\prime}} + f _ {i} \odot f _ {m}
$$

$$
f _ {o} = \text { sigmoid } (\mathcal {T} (X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}}))
$$

$$
f _ {f} = \text { sigmoid } (\mathcal {T} (X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}}))
$$

$$
f _ {i} = \text { sigmoid } (\mathcal {T} (X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}}))
$$

$$
f _ {m} = \tanh (\mathcal {T} (X _ {j} ^ {i ^ {\prime} - 1}, X _ {j - 1} ^ {i ^ {\prime}}))
$$

where $f _ { o } , f _ { f } , f _ { i }$ and $f _ { m }$ represent the output gate, forget gate, input gate and input modulation $\mathrm { g a t e } ^ { 1 1 }$ , separately, and ⊙ denotes the element-wise multiplication.

The attention module accepts the final hidden states as the unnormalized attention weights $W _ { a t t } ^ { \prime }$ which can be measured by the mapping operation $\mathcal { L } ^ { \prime } ( \cdot )$ (similar with Equation 1)

$$
W _ {a t t} ^ {\prime} = \mathcal {L} ^ {\prime} (c _ {j - 1} ^ {i ^ {\prime}}, X _ {j} ^ {i - 1}, X _ {j - 1} ^ {i ^ {\prime}})
$$

and calculate the normalized attention weights $W _ { a t t }$

$$
W _ {a t t} = \text { softmax } (W _ {a t t} ^ {\prime})
$$

The softmax function is employed to normalize the attention weights into the range of [0, 1]. Therefore, the weights can be explained as the probability that how the code ?? is relevant to the output results. Under the attention mechanism, the code ?? is weighted to $C _ { a t t }$

$$
C _ {a t t} = C \odot W _ {a t t}
$$

Note, ?? and $W _ { a t t }$ are trained instantaneously. The decoder receives the attention-based code $C _ { a t t }$ and decode it to predict the user ID $Y ^ { \prime 1 2 }$ . Since $Y ^ { \prime }$ is predicted at the output layer of the attention based RNN model $( Y ^ { \prime } = X ^ { I } )$ , we have

$$
Y ^ {\prime} = \mathcal {T} (C _ {a t t})
$$

At last, we employ the cross-entropy function to calculate the prediction cost between the predicted ID $Y ^ { \prime }$ and the ground truth $Y . \ell _ { 2 } – \mathrm { n o r m }$ (with parameter ??) is selected to prevent overfitting. The cost is optimized by the AdamOptimizer algorithm [16]. The iterations threshold of attention-based RNN is set as $n _ { i t e r }$ . The weighted code $C _ { a t t }$ has a directly linear relationship with the output layer and the predict results. If the model is trained well and get low cost, we could regard the weighted code as a high-quality representation of the user ID. We set the learned deep feature $X _ { D }$ equals to $C _ { a t t } , X _ { D } = C _ { a t t }$ , and use it to recognize the final user ID in the identification stage.

ALGORITHM 1: The MindID User Identification Algorithm   
Input: EEG raw data E
Output: Identification results $I_{D}$ 1: Initialization;
2: Preprocessing: $E' \leftarrow E$ ;
3: EEG pattern decomposition: $\delta \leftarrow E'$ ;
4: if iteration < niter then
5: for $i = 1, 2, \cdots, I$ do
6: $X^{1} = \delta$ 7: $C \leftarrow X^{1}, \mathcal{L}(c_{j-1}', X_{j}^{i-1}, X_{j-1}')$ 8: $W_{att} \leftarrow C, \mathcal{L}'(c_{j-1}', X_{j}^{i-1}, X_{j-1}')$ 9: $C_{att} = C \odot W_{att}$ 10: $X_{D} = C_{att}$ 11: end for
12: else
13: Return $X_{D}$ 14: end if
15: for $X_{D}$ do
16: $I_{D} \leftarrow X_{D}$ 17: end for
18: return $I_{D}$

# 4.5 Identification

In this section, we employ Extreme Gradient Boosting classifier (XGB) [7] to classify the learned deep feature $X _ { D }$ for user ID identification. The XGB classifier fuses a set of classification and regression trees (CART) and tries to exploit as detailed as possible the information from the input data. It builds multiple trees and each tree has its leaves and corresponding scores. Moreover, it proposes a regularized model formalization to prevent over-fitting and it is widely used for its accurate prediction power.

The learned deep feature $X _ { D }$ is taken to train a list of the CART (set there are ?? trees) and predict a set of user’s IDs. Suppose $x _ { d } \in X _ { D }$ is a single sample of the deep feature. The finally identification result of the input $x _ { d }$ is calculated as

$$
y _ {m} = f (x _ {d})
$$

$$
I _ {D} = F \left(\sum_ {1} ^ {M} y _ {m}\right), m = 1, 2, \dots , M
$$

where ?? denotes the classify function of a single tree, $y _ { m }$ denotes the predicted ID of the ??-th tree and ?? denotes the mapping from single tree prediction space to the final prediction space. The $I _ { D }$ is the final identified user ID based on EEG data. The overall procedure of the proposed approach is summarized in Algorithm 1. All the parameters mentioned in this section are listed in Table 4.

![](images/0c34668467ac2a856b094bdc2f1bb111c86902291ddbf67bb957656f4db84fc4.jpg)



![](images/e7d88a6fb9be0c378149b2e2d83f1e37c8d537bea886eb3783df535dc80a5e03.jpg)



Fig. 2. EEG collection and the collected raw data. The EEG raw data is gathered by the EEG headset and transmitted to the collector through bluetooth. The EEG data with the user keep relaxation and eye-closed is recorded.

Table 5. Datasets details. In Trial column, M denotes multi-trials and S demotes single-trial. EID-M is used to compare with the state-of-the-arts and baselines; the comparison between EID-M and EID-S are used to verify the robustness; the comparison between EID-S and EEG-S are used to verify the adaptability. 

<table><tr><td>Name</td><td>Source</td><td>Channels</td><td>Trial</td><td>Frequency</td><td>Subjects</td><td>Comparison</td><td>Robustness</td><td>Adaptability</td></tr><tr><td>EID-M</td><td>Local</td><td>14</td><td>M</td><td>128 Hz</td><td>8</td><td>√</td><td>√</td><td>-</td></tr><tr><td>EID-S</td><td>Local</td><td>14</td><td>S</td><td>128 Hz</td><td>8</td><td>-</td><td>√</td><td>√</td></tr><tr><td>EEG-S</td><td>Public</td><td>64</td><td>S</td><td>160 Hz</td><td>8</td><td>-</td><td>-</td><td>√</td></tr></table>

# 5 EXPERIMENTS AND RESULTS

We first outline the experimental settings in Section 5.1. Next, we systematically investigate the following questions:

• How does MindID compare with state-of-the-art methods and other baselines (Section 5.2)?   
• How efficient is MindID (Section 5.3)?   
• Is MindID robust under a multi-trial setting (Section 5.4)?   
• Does MindID exhibit consitent results when tested with different datasets (Section 5.5)?   
• Is the Delta pattern exactly works better than other patterns (Section 5.6)?

# 5.1 Experimental settings

5.1.1 Datasets. The proposed MindID system is evaluated by three datasets: a multi-trial local dataset (EID-M), a single-trial dataset (EID-S), and a public dataset (eegmmidb). The details of datasets are introduced in Table 5. All the datasets are measured the EEG raw data from the subject’s scalp while the subject keeps relax and eye-closed.

EID-M EID-M denotes EEG based ID recognition with the training set comes from the multi-trial collection. Since multi-trial scenarios are mostly happed in the practical applications, EID-M dataset is taken to report a comparison with the state-of-the-art methods and baselines. The EID-M dataset is gathered in the experiment which is carried on by 8 subjects (5 males and 3 females) aged from 24 to 28. During the experiment, the subject wearing the Emotiv Epoc+13 EEG collection headset, keeping relax and eye-closed (shown in Figure 2). The Emotiv Epoc+ contains 14 channels and the sampling rate is set as 128 ????. In the experiment, each subject takes three trials and each trial produce 7,000 EEG samples. Summarily, each subject has 21,000 samples and the whole EID-M dataset contains 168,000 samples.

EID-S EID-S is collected under the same situation with EID-M (5 males, 3 females, 14 channels, and 128 Hz). The main difference between them is the former dataset are belonged single trial. EID-S totally contains 56,000 samples belong to 8 subjects (7,000 samples belong to each subject).

EEG-S EEG-S is a subset of the widely used online public dataset eegmmidb (EEG motor movement/imagery database)14. It is collected with the BCI2000 (Brain Computer Interface) instrumentation system 15 [26] (64 channels and 160 ???? sampling rate). EEG-S contains 8 subjects with each subject owns 7,000 samples which are collected in single trial.

To assess the performance of the proposed MindID model, we employ several widely-used evaluation metrics such as accuracy, precision, recall, F1 score, ROC (Receiver Operating Characteristic) curve, support, and AUC (Area Under the Curve).

![](images/f52df3b8ebbecd10d005032cd7da4f3df263f0c45b8e66ff775063c52493a049.jpg)  
Fig. 3. Confusion matrix of EID-M

![](images/b025146fecda9b009804040c0fab1f15d1ececcf203c02e1a0562887b8906207.jpg)



Fig. 4. Confusion matrix of EID-S

![](images/163ac74c3165900b7c9954d2d87572c5a22ed4252074efa3ea4d2bfe9420d35c.jpg)  
Fig. 5. Confusion matrix of EEG-S

![](images/1a0ef65da73c456d61cc3ee2b43605858393a15ae204b63cab74226877e7d350.jpg)



Fig. 6. ROC and AUC of EID-M

![](images/de19f3af35d9f67f3822fc90dddf0298a0e2ab5bf39a2aa00510f435eba23336.jpg)



Fig. 7. ROC and AUC of EID-S

![](images/fab99a7e48a6d0fe0c38c41e1a247328dee11dc4ab2d49e1596974af56662483.jpg)



Fig. 8. ROC and AUC of EEG-S

# 5.2 Overall comparison

In this section, we firstly report our model’s performance evaluated on EID-M dataset and then compare the proposed approach with the state-of-the-art approaches and baselines. Our approach extract Delta wave through pattern decomposition fed it into an attention-based Encoder-Decoder RNN model, and predict the user’s ID via a boosting classifier. We randomly select 147,000 samples from EID-M to train the model and the residual

Table 6. Evaluation report of EID-M dataset. The overall accuracy achieves 0.982 of 21000 testing samples. The support is the number of samples of each class. 

<table><tr><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>Average/Total</td></tr><tr><td>Precision</td><td>0.9723</td><td>0.9789</td><td>0.9777</td><td>0.9894</td><td>0.989</td><td>0.9814</td><td>0.9898</td><td>0.9774</td><td>0.982</td></tr><tr><td>Recall</td><td>0.9822</td><td>0.9885</td><td>0.9945</td><td>0.9711</td><td>0.9808</td><td>0.9821</td><td>0.9742</td><td>0.9834</td><td>0.9821</td></tr><tr><td>F1-score</td><td>0.9772</td><td>0.9837</td><td>0.9860</td><td>0.9802</td><td>0.9849</td><td>0.9818</td><td>0.9820</td><td>0.9804</td><td>0.982</td></tr><tr><td>Support</td><td>2674</td><td>2554</td><td>2601</td><td>2650</td><td>2639</td><td>2634</td><td>2636</td><td>2612</td><td>21000</td></tr></table>

Table 7. The accuracy comparison with baselines and the state-of-the-art methods over EID-M dataset. The result shows that our approach achieves the highest accuracy of 0.982. 

<table><tr><td>Index</td><td>Method</td><td>Acc</td><td>Recall</td><td>F1-Sore</td><td>AUC</td></tr><tr><td>1</td><td>Jayarathne[13]</td><td>0.919</td><td>0.914</td><td>0.9165</td><td>0.946</td></tr><tr><td>2</td><td>Bashar et al. [6]</td><td>0.873</td><td>0.898</td><td>0.8853</td><td>0.907</td></tr><tr><td>3</td><td>Keshishzadeh et al. [14]</td><td>0.815</td><td>0.843</td><td>0.8288</td><td>0.859</td></tr><tr><td>4</td><td>Gui et al.[12]</td><td>0.833</td><td>0.811</td><td>0.8219</td><td>0.842</td></tr><tr><td>5</td><td>Thomas and Vinod [29]</td><td>0.859</td><td>0.869</td><td>0.8640</td><td>0.888</td></tr><tr><td>6</td><td>Kumari and Vaish [17]</td><td>0.875</td><td>0.872</td><td>0.8735</td><td>0.901</td></tr><tr><td>7</td><td>RF</td><td>0.795</td><td>0.813</td><td>0.8039</td><td>0.827</td></tr><tr><td>8</td><td>KNN</td><td>0.849</td><td>0.836</td><td>0.8424</td><td>0.847</td></tr><tr><td>9</td><td>RNN</td><td>0.815</td><td>0.803</td><td>0.8090</td><td>0.821</td></tr><tr><td>10</td><td>RNN+XGB</td><td>0.808</td><td>0.789</td><td>0.7984</td><td>0.803</td></tr><tr><td>11</td><td>PD+RNN</td><td>0.853</td><td>0.821</td><td>0.8367</td><td>0.844</td></tr><tr><td>12</td><td>AR+RNN</td><td>0.811</td><td>0.798</td><td>0.8044</td><td>0.831</td></tr><tr><td>13</td><td>XGB</td><td>0.815</td><td>0.811</td><td>0.8130</td><td>0.853</td></tr><tr><td>14</td><td>PD+XGB</td><td>0.965</td><td>0.959</td><td>0.9620</td><td>0.977</td></tr><tr><td>15</td><td>Ours (EID-M)</td><td>0.982</td><td>0.9821</td><td>0.9820</td><td>0.999</td></tr></table>

21,000 samples are used to test the performance. Through tuning, the hyper-parameters used in our approach are listed following. In EEG pattern decomposition, we employ a 3 order butter-worth band-pass filter and the passband is [0.5????, 4????]. In the attention-based RNN structure, the encoder consists of 1 input layer (14 nodes), 3 non-recurrent fully-connected hidden layers (164 nodes) and 1 recurrent LSTM layer (164 cells); the decoder includes 1 fully-connected hidden layer (164 nodes) and 1 output layer (8 nodes). The learning rate is 0.001; the parameter of ℓ − 2 norm is set as 0.001; the encoder and decoder separately have 6 and 2 layers; training dataset is divided into 7 batches with the batch size of 21,000; the number of training iterations is 2000. In the classifier: the learning rate is 0.7; the sub-sampling rate is 0.9; the max depth is set as 6; the training iterations is 500. The ground truth (from 0 to 7) is represented as a one-hot label which corresponding to the ID of subjects.

The proposed approach achieves the identification accuracy as 0.982. The detailed confusion matrix, evaluation report, and ROC curves (with AUC scores) are illustrated in Figure 3, Table $^ { 6 , }$ and Figure $^ { 6 , }$ respectively. The above evaluation metrics illustrate that our approach obtains higher than 0.97 precision of each class.

In addition, the accuracy comparison between our method and other state-of-the-art and baselines are listed in Table 7. RF denotes Random Forest, AdaBoost denotes Adaptive Boosting, LDA denotes Linear Discriminant Analysis, PD denotes for Pattern Decomposition, AR denotes AutoRegressive method, and XGB denotes for X-Gradient Boosting classifier (the classifier used in our approach). In addition, the key parameters of the baselines are listed here: Linear SVM (?? = 1), RF (?? = 200), KNN (k=3), and AR (13 order autoregressive from 40 samples). The setting up of PD, RNN and XGB classifier are same as the hyper-parameters mentioned above. The methods used in the state-of-the-art are introduced as follows:

• Jayarathne et al. [13] focus on the 8 to 30 Hz Alpha and Beta combined frequency band across all EEG channels and extract the Common Spatial Patterns (CSP) values as classification features. LDA is employed as the classifier.   
• Bashar et al. [6] first remove noise and artifacts using Bandpass FIR filter. Then learning the features through multi-scale shape description (MSD), multi-scale wavelet packet statistics (WPS) and multi-scale wavelet packet energy statistics (WPES). These features are finally used to train a support vector machine (SVM) classifier.   
• Keshishzadeh et al. [14] investigates the Autoregressive (AR) coefficients as the feature set which is identified by an SVM classifier.   
• Gui et al.[12] propose to reduce the noise level through a low-pass filter, extract frequency features using wavelet packet decomposition, and perform classification based on a deep neural network.   
• Thomas and Vinod [29] combines subject-specific alpha peak frequency, peak power, and delta band power values to form discriminative feature vectors and templates.   
• Kumari and Vaish [17] apply discrete wavelet analysis to decompose EEG raw signal corresponding to EEG sub-band frequency (0-59Hz). The extracted statistical measures and energy calculation of each decomposed wave are classified by neural network structure.

All the approaches are working on the preprocessed EID-M dataset. The results show that our method achieves the highest accuracy of 0.982 compared with other methods.

# 5.3 Efficiency Evaluation

In this section, the efficiency refers to the required identification time. The low efficiency may limit the suitability for practical deployment. To assess the efficiency of the proposed approach, we focus on the algorithm running time and compared it with the widely used baselines and other classification methods. In this paper, we run the experiments on a GPU-accelerated machine with Nvidia Titan X pascal GPU, 768G memory, and 145 TB PCIe based SSD.

The time required to train the identification model is firstly given in Figure 9(the X-axis label denotes the index of algorithms shown in Table 7), which illustrates that our approach (PD+RNN+XGB) and the RNN+XGB approach take much more training time than other methods. The reasons are in two aspects. On one hand, the algorithm loops take a considerable amount of time (RNN run for 2000 iterations and XGB run for 500 loops). On the other hand, the deep learning structure and the boosting trees have much more parameters and complex structures than other classification models. Compared to the training time, however, for practical considerations, the execution time of an algorithm during testing is more important. Figure 10 presents that the testing time of our model is less than 1 second, which is shorter than most of the state-of-the-arts and baselines. Summarily, our model takes only tiny testing time although it requires more time to train the model, which is acceptable and reasonable in the real world implement.

In the practical deployment, the data size used to train the model generally is one important impact factor of the model’s performance. We conduct a set of experiments to investigate the accuracy influence brought by training data size. We run the experiments for 5 times and report the error-bar of results in Figure 11, which shows that our approach could achieve the accuracy around 0.9 even when only 12.5% of the available dataset is used for training. This presents that the proposed approach has a low dependency on the training data size.

![](images/10c7cae1658ffcca41bab3ae988a202ceee003e720761fadbe6d8ef963746b04.jpg)



![](images/b4e631ebb126363b5d9282402d7a7947eab251895f352294cfa008613f328f67.jpg)



![](images/abab1c3316a95b53decfd447f2761764b4b1305eb5e12cf70cef2f75ebcc14c2.jpg)



Fig. 9. Training time. The index cor- Fig. 10. Testing time. The index cor- Fig. 11. The accuracy change trend responding the index in Table 7. responding the index in Table 7. with training data size

Table 8. Evaluation report of EID-S dataset. The overall accuracy achieves 0.9882 of 7000 testing samples. 

<table><tr><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>Average/Total</td></tr><tr><td>Precision</td><td>0.9897</td><td>0.9881</td><td>0.9944</td><td>0.9837</td><td>0.9895</td><td>0.9844</td><td>0.9866</td><td>0.9897</td><td>0.9882</td></tr><tr><td>Recall</td><td>0.992</td><td>0.9924</td><td>0.9944</td><td>0.9712</td><td>0.986</td><td>0.9939</td><td>0.9789</td><td>0.9977</td><td>0.9883</td></tr><tr><td>F1-score</td><td>0.9908</td><td>0.9903</td><td>0.9944</td><td>0.9774</td><td>0.9878</td><td>0.9891</td><td>0.9827</td><td>0.9937</td><td>0.9883</td></tr><tr><td>Support</td><td>872</td><td>927</td><td>892</td><td>857</td><td>857</td><td>831</td><td>893</td><td>871</td><td>7000</td></tr></table>

# 5.4 Robustness evaluation

In practical scenarios and real-world deployment, the identification system is applied to the multi-trial situation. The data used to train the system and the test data used to identify the user come from different trials (different placements of the device). For example, the user wears the EEG headset and collect the first trial data; then collect the second trial data after he/she removes the headset and puts it back again. There maybe some difference between two trials data, which is caused by the different placement position or other internal equipment reasons. Therefore, The divergence of the training data and testing data should be considered when the identification system is designed.

In this section, we evaluate the robustness of the proposed approach by analyzing how the single-trial/multitrial affect the identification accuracy. Two datasets, which respectively contain single-trial identification data (EID-S) and multi-trial identification data (EID-M), are employed to assess our method. More details about the datasets are provided in Section 5.1.

The evaluations of EID-S is shown in Table 8, through which we can observe that our approach achieves the overall accuracy of 0.9882% on EID-S and the precisions of all classes are higher than 0.98. To take a closer look at the result, confusion matrix (Table 4) and ROC curves (Figure 7) are provided. The performances of EID-M are reported in Section 5.2 (Figure 3, Table 6, and Figure 6). Through the comparison of the performances of EID-M and EID-S, we could know that the identification overall accuracy has a slight decrease (from 0.9882 to 0.982) with the increase of data trials. The inter-trial divergence only contributes a slight fluctuation (0.062) on the identification accuracy. This fact illustrates that the proposed approach has potential on the real world implement and large-scale application.

# 5.5 Adaptability evaluation

To examine the adaptability and consistency, our model is evaluated on another dataset which is more precisely but difficult-to-operate. According to the principle of single variable, both the local dataset (EID-S) and the public dataset (EEG-S) are collected from single-trial and contains 56,000 samples belong to 8 subjects. The details of EID-S and EEG-S can be found in Section 5.1. Compared with the Emotiv headset used in EID-S, the BCI 2000 system used in EEG-S is more accurately but inconvenient.

Table 9. Evaluation report of EEG-S dataset. The overall accuracy achieves 0.9989 of 7000 testing samples. 

<table><tr><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>Average/Total</td></tr><tr><td>Precision</td><td>1</td><td>0.9988</td><td>0.9988</td><td>0.9957</td><td>1</td><td>1</td><td>0.9988</td><td>0.9989</td><td>0.9989</td></tr><tr><td>Recall</td><td>1</td><td>0.9988</td><td>0.9988</td><td>0.9989</td><td>1</td><td>0.9988</td><td>0.9964</td><td>0.9989</td><td>0.9988</td></tr><tr><td>F1-score</td><td>1</td><td>0.9988</td><td>0.9988</td><td>0.9973</td><td>1</td><td>0.9994</td><td>0.9976</td><td>0.9989</td><td>0.9989</td></tr><tr><td>Support</td><td>872</td><td>869</td><td>848</td><td>939</td><td>880</td><td>864</td><td>842</td><td>886</td><td>7000</td></tr></table>

The experiment report (Table 9) of EEG-S illustrates our model gains the accuracy of 0.9989 and all the evaluation metrics (precision, recall, and F1-score) are higher than 0.995. The confusion matrix and ROC curves are given in Figure 5 and Figure 8, respectively. The accurate classification of EEG-S demonstrates that our approach has good adaptability and ables to handle different situations (like various EEG equipment).

Recall the results of EID-S (Figure 4, Table 8, and Figure 7), EEG-S performs better and achieves an accuracy of around 0.01 improvement. The reason is that EEG-S has more channels (64 vs 14) and higher sampling rate (160????????128????) which encloses more useful information for the identification.

This section and the previous section illustrate that our approach has the potential to be largely deployment in practice environment from different aspects (robustness and adaptability).

# 5.6 EEG pattern decomposition effects

This section designs a set of comparison experiments to validate the hypothesis proposed in Section 3, which claims that the Delta pattern signals takes the most distinguishable information for identification. To demonstrate the priority of Delta pattern, we decompose the EEG data into 6 patterns: Delta pattern, Theta pattern, Alpha pattern, Beta pattern, Gamma pattern, and Full-frequency pattern. The Full-frequency pattern contains full frequency bands from 0 to 128 ????. Note that the sampling rate in the local datasets is 128 ????, which means that the maximum filtering range of butter-worth filter is 0-64 ????. Therefore, the Gamma pattern used in this study is set as 30-63 ????.

Our approach and other widely used classifiers are evaluated all of the EID-M, EID-S, and EEG-S datasets over 6 different patterns. The experiments results are shown in Table 10. The primary conclusions are listed as follows:

• Our approaches achieves the highest accuracy on all of the three datasets (with different trials, collection equipment, and sampling precision), which proofs that our model has outstanding robustness and adaptability.   
• Delta pattern signals provide higher identification accuracy compared with other 5 categories of patterns over all datasets. This fact presents that Delta pattern contains the most discriminative information for identification and demonstrates the hypothesis proposed in Section 3 is appropriate.   
• Several statistic based classification models (such as RF, KNN, and XGB) work well on the low-frequency patterns (Delta and Theta) but cannot handle high-frequency band signals (Alpha, Beta, and Gamma).   
• The deep learning algorithm can extract deep relationships between samples from complicated and high fluctuate situations. This conclusion can be inferred from the observations that RNN has lower accuracy than RF/KNN/XGB in Delta and Theta patterns but performs better in other patterns. The above two attributes inspire the combination of the attention-based RNN structure and the tree-boosting classifier.   
• The baselines and the state-of-the-art methods can gain acceptable identification accuracy on highquality EEG dataset but fails on the low-quality dataset. Take the Full-frequency pattern as an example, RF/XGB/RNN achieves the accuracy of more than 0.95 on EEG-S but lower than 0.82 on EID-M. However, our approach keeps consistently high accuracy no matter the data quality. This phenomenon promotes the future deployment in practical of our approach.

Table 10. EEG Pattern Decomposition Analysis 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Methods</td><td colspan="6">EEG Patterns</td><td rowspan="2">Best Level</td></tr><tr><td>Delta</td><td>Theta</td><td>Alpha</td><td>Beta</td><td>Gamma</td><td>Full</td></tr><tr><td rowspan="8">EID-M</td><td>SVM</td><td>0.143</td><td>0.157</td><td>0.137</td><td>0.135</td><td>0.138</td><td>0.2745</td><td></td></tr><tr><td>RF</td><td>0.936</td><td>0.707</td><td>0.677</td><td>0.489</td><td>0.435</td><td>0.7935</td><td></td></tr><tr><td>KNN</td><td>0.941</td><td>0.804</td><td>0.618</td><td>0.35</td><td>0.313</td><td>0.819</td><td></td></tr><tr><td>AdaBoost</td><td>0.251</td><td>0.13</td><td>0.15</td><td>0.15</td><td>0.171</td><td>0.24</td><td rowspan="5">0.982 (Delta)</td></tr><tr><td>LDA</td><td>0.148</td><td>0.154</td><td>0.135</td><td>0.135</td><td>0.129</td><td>0.28</td></tr><tr><td>XGB</td><td>0.965</td><td>0.665</td><td>0.69</td><td>0.495</td><td>0.414</td><td>0.815</td></tr><tr><td>RNN</td><td>0.917</td><td>0.709</td><td>0.708</td><td>0.518</td><td>0.411</td><td>0.813</td></tr><tr><td>Ours</td><td>0.982</td><td>0.713</td><td>0.73</td><td>0.513</td><td>0.423</td><td>0.822</td></tr><tr><td rowspan="8">EID-S</td><td>SVM</td><td>0.135</td><td>0.162</td><td>0.181</td><td>0.152</td><td>0.132</td><td>0.408</td><td></td></tr><tr><td>RF</td><td>0.947</td><td>0.771</td><td>0.719</td><td>0.587</td><td>0.377</td><td>0.863</td><td></td></tr><tr><td>KNN</td><td>0.953</td><td>0.824</td><td>0.714</td><td>0.472</td><td>0.495</td><td>0.853</td><td></td></tr><tr><td>AdaBoost</td><td>0.278</td><td>0.29</td><td>0.162</td><td>0.2</td><td>0.16</td><td>0.3</td><td rowspan="5">0.9882 (Delta)</td></tr><tr><td>LDA</td><td>0.14</td><td>0.16</td><td>0.183</td><td>0.152</td><td>0.122</td><td>0.41</td></tr><tr><td>XGB</td><td>0.981</td><td>0.785</td><td>0.791</td><td>0.599</td><td>0.489</td><td>0.893</td></tr><tr><td>RNN</td><td>0.9425</td><td>0.7568</td><td>0.8175</td><td>0.6331</td><td>0.5141</td><td>0.9045</td></tr><tr><td>Ours</td><td>0.9882</td><td>0.821</td><td>0.8259</td><td>0.612</td><td>0.517</td><td>0.913</td></tr><tr><td rowspan="8">EEG-S</td><td>SVM</td><td>0.216</td><td>0.167</td><td>0.148</td><td>0.169</td><td>0.186</td><td>0.652</td><td></td></tr><tr><td>RF</td><td>0.972</td><td>0.885</td><td>0.819</td><td>0.823</td><td>0.87</td><td>0.957</td><td></td></tr><tr><td>KNN</td><td>0.974</td><td>0.865</td><td>0.781</td><td>0.559</td><td>0.743</td><td>0.936</td><td></td></tr><tr><td>AdaBoost</td><td>0.32</td><td>0.32</td><td>0.27</td><td>0.23</td><td>0.22</td><td>0.34</td><td rowspan="5">0.9989 (Delta)</td></tr><tr><td>LDA</td><td>0.186</td><td>0.17</td><td>0.28</td><td>0.168</td><td>0.162</td><td>0.6618</td></tr><tr><td>XGB</td><td>0.9972</td><td>0.982</td><td>0.967</td><td>0.959</td><td>0.953</td><td>0.989</td></tr><tr><td>RNN</td><td>0.9981</td><td>0.9667</td><td>0.964</td><td>0.947</td><td>0.952</td><td>0.9886</td></tr><tr><td>Ours</td><td>0.9989</td><td>0.972</td><td>0.968</td><td>0.961</td><td>0.955</td><td>0.99</td></tr></table>

# 6 DISCUSSION AND FUTURE WORK

In this paper, we propose an EEG-based identification approach and evaluate the robustness and adaptability over three datasets. In this section, we discuss the challenges and potential future work of our research.

First of all, the impaction of multi-trial worth to attract more attention although we have investigated a preliminary study on this topic. Limited by the local experimental conditions, our study only gathered EEG data from 8 subjects with few trials. The dataset is only divided into two categories (Multi and Single), which is not enough to explore the change trend of the identification accuracy with the increase of data trials. The accuracy trend is supposed to be investigated over the dataset with enough trials.

Moreover, the pre-trained model should be updated for a period of time since the user’s EEG data is gradually changed with the environmental factors such as age, mental state, and living style. One of our future work is to develop an online learning system which is enabled to automatically update the training dataset based on the testing data which is collected during the operating period.

In addition, the emotional threshold is one potential challenge faced by user identification. It is well known that the EEG signals are associated with user’s emotion. Therefore, an emotional threshold is required to tolerate the slight emotion fluctuation which may be caused by routine factors such as fatigue and temporal emotion shift. At the same time, the threshold is demanded to detect the out-of-bound emotions which may be occurred in dangerous situations such as being hacked by a terrorist.

# 7 CONCLUSION

Taking the advantages of EEG-based techniques for attack-resilient, we propose a biometric EEG-based identification approach, to overcome the limitations of traditional biometric identification methods. We analyzed the EEG data pattern characteristics and capture the Delta pattern which takes the most distinguishable features for user identification. Based on the pattern decomposition analysis, we report the structure of the proposed approach. In the first step of identification, the preprocessed EEG data is decomposed into Delta pattern. Then an attention-based RNN structure is employed to extract deep representations of Delta wave. At last, the deep representations are used to directly identify the user’ ID. The proposed approach is evaluated over 3 datasets (two local and one public dataset). The experiments results illustrate that our model achieves the accuracy of 0.982, 0.9882, and 0.9989 over three datasets, separately. The results also infer the robustness and adaptability of our model. Moreover, a set of experiments are conducted and verified that the Delta pattern is the most reliable and dominant pattern in EEG-based identification.

# ACKNOWLEDGMENTS

# REFERENCES

[1] Salahiddin Altahat, Girija Chetty, Dat Tran, and Wanli Ma. 2015. Analysing the Robust EEG Channel Set for Person Authentication. In International Conference on Neural Information Processing. Springer, 162–173.   
[2] Corey Ashby, Amit Bhatia, Francesco Tenore, and Jacob Vogelstein. 2011. Low-cost electroencephalogram (eeg) based authentication. In Neural Engineering (NER), 2011 5th International IEEE/EMBS Conference on. IEEE, 442–445.   
[3] Jimmy Ba, Volodymyr Mnih, and Koray Kavukcuoglu. 2014. Multiple object recognition with visual attention. arXiv preprint arXiv:1412.7755 (2014).   
[4] Dzmitry Bahdanau, Jan Chorowski, Dmitriy Serdyuk, Philemon Brakel, and Yoshua Bengio. 2016. End-to-end attention-based large vocabulary speech recognition. In Acoustics, Speech and Signal Processing (ICASSP), 2016 IEEE International Conference on. IEEE, 4945– 4949.   
[5] Erol Başar. 1980. EEG-brain dynamics: relation between EEG and brain evoked potentials. Elsevier-North-Holland Biomedical Press.   
[6] Md Khayrul Bashar, Ishio Chiaki, and Hiroaki Yoshida. 2016. Human identification from brain EEG signals using advanced machine learning method EEG-based biometrics. In Biomedical Engineering and Sciences (IECBES), 2016 IEEE EMBS Conference on. IEEE, 475–479.   
[7] Tianqi Chen and Carlos Guestrin. 2016. Xgboost: A scalable tree boosting system. In Proceedings of the 22Nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. ACM, 785–794.   
[8] John Chuang, Hamilton Nguyen, Charles Wang, and Benjamin Johnson. 2013. I think, therefore i am: Usability and security of authentication using brainwaves. In International Conference on Financial Cryptography and Data Security. Springer, 1–16.   
[9] AM Edwards and RCJ Polman. 2013. Pacing and awareness: brain regulation of physical activity. Sports Medicine 43, 11 (2013), 1057–1064.   
[10] Geof H Givens, J Ross Beveridge, Yui Man Lui, David S Bolme, Bruce A Draper, and P Jonathon Phillips. 2013. Biometric face recognition: from classical statistics to future challenges. Wiley Interdisciplinary Reviews: Computational Statistics 5, 4 (2013), 288–308.   
[11] Steven Goldstein. 2016. Methods and systems for voice authentication service leveraging networking. (March 8 2016). US Patent 9,282,096.   
[12] Qiong Gui, Zhanpeng Jin, and Wenyao Xu. 2014. Exploring EEG-based biometrics for user identification and authentication. In Signal Processing in Medicine and Biology Symposium (SPMB), 2014 IEEE. IEEE, 1–6.   
[13] Isuru Jayarathne, Michael Cohen, and Senaka Amarakeerthi. 2016. BrainID: Development of an EEG-based biometric authentication system. In Information Technology, Electronics and Mobile Communication Conference (IEMCON), 2016 IEEE 7th Annual. IEEE, 1–6.   
[14] Sarineh Keshishzadeh, Ali Fallah, and Saeid Rashidi. 2016. Improved EEG based human authentication system on large dataset. In Electrical Engineering (ICEE), 2016 24th Iranian Conference on. IEEE, 1165–1169.   
[15] Preben Kidmose, David Looney, Michael Ungstrup, Mike Lind Rank, and Danilo P Mandic. 2013. A study of evoked potentials from ear-EEG. IEEE Transactions on Biomedical Engineering 60, 10 (2013), 2824–2830.   
[16] Diederik Kingma and Jimmy Ba. 2014. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 (2014).   
[17] Pinki Kumari and Abhishek Vaish. 2015. Brainwave based user identification system: A pilot study in robotics environment. Robotics and Autonomous Systems 65 (2015), 15–23.

[18] Neal S Latman and Emily Herb. 2013. A field study of the accuracy and reliability of a biometric iris recognition system. Science & Justice 53, 2 (2013), 98–102.   
[19] xiaoli Li. 2016. Signal Processing in Neuroscience. Springer, 8–12.   
[20] Minh-Thang Luong, Hieu Pham, and Christopher D Manning. 2015. Effective approaches to attention-based neural machine translation. arXiv preprint arXiv:1508.04025 (2015).   
[21] Sebastien Marcel and José del R Millán. 2007. Person authentication using brainwaves (EEG) and maximum a posteriori model adaptation. IEEE transactions on pattern analysis and machine intelligence 29, 4 (2007).   
[22] Giuseppe Moruzzi and Horace W Magoun. 1949. Brain stem reticular formation and activation of the EEG. Electroencephalography and clinical neurophysiology 1, 1 (1949), 455–473.   
[23] Johannes Müller-Gerking, Gert Pfurtscheller, and Henrik Flyvbjerg. 1999. Designing optimal spatial filters for single-trial EEG classification in a movement task. Clinical neurophysiology 110, 5 (1999), 787–798.   
[24] Timothy David Noakes. 2011. Time to move beyond a brainless exercise physiology: the evidence for complex regulation of human exercise performance. Applied physiology, nutrition, and metabolism 36, 1 (2011), 23–35.   
[25] Fahreddin Sadikoglu and Selin Uzelaltinbulat. 2016. Biometric Retina Identification Based on Neural Network. Procedia Computer Science 102 (2016), 26–33.   
[26] Gerwin Schalk, Dennis J McFarland, Thilo Hinterberger, Niels Birbaumer, and Jonathan R Wolpaw. 2004. BCI2000: a general-purpose brain-computer interface (BCI) system. IEEE Transactions on biomedical engineering 51, 6 (2004), 1034–1043.   
[27] Javad Sohankar, Koosha Sadeghi, Ayan Banerjee, and Sandeep KS Gupta. 2015. E-bias: A pervasive eeg-based identification and authentication system. In Proceedings of the 11th ACM Symposium on QoS and Security for Wireless and Mobile Networks. ACM, 165–172.   
[28] Mircea Steriade. 1991. Alertness, quiet sleep, dreaming. In Normal and Altered States of Function. Springer, 279–357.   
[29] Kavitha P Thomas and A Prasad Vinod. 2016. Utilizing individual alpha frequency and delta band power in EEG based biometric recognition. In Systems, Man, and Cybernetics (SMC), 2016 IEEE International Conference on. IEEE, 004787–004791.   
[30] Leonard J Trejo, Karla Kubitz, Roman Rosipal, Rebekah L Kochavi, and Leslie D Montgomery. 2015. EEG-based estimation and classification of mental fatigue. Psychology 6, 05 (2015), 572.   
[31] JA Unar, Woo Chaw Seng, and Almas Abbasi. 2014. A review of biometric technology along with trends and prospects. Pattern recognition 47, 8 (2014), 2673–2688.   
[32] Feng Wang and David MJ Tax. 2016. Survey on the attention based RNN model and its applications in computer vision. arXiv preprint arXiv:1601.06823 (2016).   
[33] Hong Wang, Chi Zhang, Tianwei Shi, Fuwang Wang, and Shujun Ma. 2015. Real-time EEG-based detection of fatigue driving danger for accident prediction. International journal of neural systems 25, 02 (2015), 1550002.   
[34] Xiang Zhang, Lina Yao, Dalin Zhang, Xianzhi Wang, Quan Z Sheng, and Tao Gu. 2017. Multi-person brain activity recognition via comprehensive eeg signal analysis. In Proceedings of the 13th International Conference on Mobile and Ubiquitous Systems: Computing, Networking and Services (Mobiquitous,2017). ACM.