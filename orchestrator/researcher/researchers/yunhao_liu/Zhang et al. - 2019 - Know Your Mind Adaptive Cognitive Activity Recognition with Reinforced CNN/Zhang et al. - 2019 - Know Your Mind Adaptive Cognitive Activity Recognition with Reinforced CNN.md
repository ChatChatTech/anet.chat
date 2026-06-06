“© 2019 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.”

# Know Your Mind: Adaptive Cognitive Activity Recognition with Reinforced CNN

Xiang Zhang∗, Lina Yao∗, Xianzhi Wang§, Wenjie Zhang∗, Shuai Zhang∗, Yunhao Liu¶

∗University of New South Wales, Sydney, Australia

§ University of Technology Sydney, Sydney, Australia

¶ Michigan State University, East Lansing, USA

{xiang.zhang3, shuai.zhang}@student.unsw.edu.au, {lina.yao, wenjie.zhang}@unsw.edu.au

xianzhi.wang@uts.edu.au, yunhao@cse.msu.edu

Abstract—Electroencephalography (EEG) signals reflect and measure activities in certain brain areas. Its zero clinical risk and easy-to-use features make it a good choice of providing insights into the cognitive process. However, effective analysis of time-varying EEG signals remains challenging. First, EEG signal processing and feature engineering are time-consuming and highly rely on expert knowledge, and most existing studies focus on domain-specific classification algorithms, which may not apply to other domains. Second, EEG signals usually have low signal-to-noise ratios and are more chaotic than other sensor signals. In this regard, we propose a generic EEG-based cognitive activity recognition framework that can adaptively support a wide range of cognitive applications to address the above issues. The framework uses a reinforced selective attention model to choose the characteristic information among raw EEG signals automatically. It employs a convolutional mapping operation to dynamically transform the selected information into a feature space to uncover the implicit spatial dependency of EEG sample distribution. We demonstrate the effectiveness of the framework under three representative scenarios: intention recognition with motor imagery EEG, person identification, and neurological diagnosis, and further evaluate it on three widely used public datasets. The experimental results show our framework outperforms multiple state-of-the-art baselines and achieves competitive accuracy on all the datasets while achieving low latency and high resilience in handling complex EEG signals across various domains. The results confirm the suitability of the proposed generic approach for a range of problems in the realm of Brain-Computer Interface applications.

Index Terms—deep learning, reinforcement learning, attention mechanism, brain-computer interface

# I. INTRODUCTION

Electroencephalography (EEG) is an electrophysiological monitoring indicator to analyze brain states and activities by measuring the voltage fluctuations of ionic current within the neurons of brains [1]. In practice, EEG signals can be collected by portable and off-the-shelf equipment in a non-invasive and non-stationary way [2]. EEG signal classification algorithms have been studied for a range of real-world applications [3]. The accuracy and robustness of EEG classification model have promising meanings to identify cognitive activities in the realms of movement intention recognition, person identification, and neurological diagnosis. Cognitive activity recognition systems [4] provide a bridge between the inside cognitive world and the outside physical world. They are recently used in assisted living [5], smart homes [6], and entertainment industry

![](images/afcccaa29307d8c20324663ececeed2856ca86ab459cbf6259ff3cbca6976c77.jpg)  
(a) T-2

![](images/2786e9f4001f190e00c8f8e628cd94d78427c7eedfb6059391190a35720cbbe9.jpg)  
(b) T-1

![](images/79cad26981b20cff14495276d0157fe41d38e00b3afea2c9132aa87d231fd7cf.jpg)  
(c) T

![](images/c598a85f7ae3bc6fc5fef9a380f3106d28b649ff82b60aa4c6931e024d962d6b.jpg)  
(d) T+1

![](images/9bf81a01848abce8d7928c8ba3cf4c9e1c8314b548c2b099b78e583f246e24e8.jpg)  
(e) T+2   
Fig. 1: EEG topography with continuous samples. The interval among samples is 0.00625 second.

[7]; EEG-based person identification technique empowers the security systems deployed in bank or customs [8], [9]; EEG signal-based neurological diagnosis can be used to detect the organic brain injury and abnormal synchronous neuronal activity such as epileptic seizure [10], [11].

The classification of cognitive activity faces several challenges. First, the EEG data preprocessing and feature extraction methods (e.g., filtering, Discrete Wavelet Transformation, and feature selection) which are employed by most existing EEG classification studies [3], [7] are time-consuming and highly depend on expertise. Meanwhile, the hand-crafted features require extensive experiments to generalize well to diverse settings such as filtering bands and wavelet orders. Therefore, an effective method which can directly work on raw EEG data is necessary.

Second, most current EEG classification methods are designed based on domain-specific knowledge and thus may become ineffective or even fail in different scenarios [2]. For example, the approach customized for EEG-based neurological diagnosis may not work well on intention recognition. Therefore, a general EEG signal classification method is expected to be both efficient and robust across various domains for better usability and suitability.

Third, EEG signals have a low signal-to-noise ratio and more chaotic than other sensor signals such as wearable sensors. Thus, the segment-based classification which is widely used in sensing signal classification may not fit cognitive activity recognition. A segment contains some continuous EEG samples clipped by the sliding window method [12] while a single EEG sample (also called EEG instance) is collected at a specific time point. In particular, segmentbased classification has two drawbacks compared with samplebased classification: 1) in a segment with many samples, the sample diversity may offset by other inverse changed samples as EEG signals vary rapidly (Section II). 2) segment-based classification requires more training data and a longer datacollecting time. For example, suppose each segment has ten samples without overlapping; for the same training batch size, segment-based classification requires ten times of the data size and the data-collecting time than sample-based classification. As a result, segment-based classification cannot exploit the immediate intention of changing and thus achieves low precision in practical deployment. To this end, sample-based classification is more attractive.

TABLE I: Time domain and correlation coefficient analysis. n-points denotes the values are measured by the samples with n sampling points. We compare EEG signals with other sensing data (such as wearable sensor data and smartphone data) over five different scales and the results constantly show that EEG signals have the highest instability. 

<table><tr><td rowspan="5">Time Domain</td><td rowspan="2">Signals</td><td colspan="2">5-points</td><td colspan="2">50-points</td><td colspan="2">100-points</td><td colspan="2">500-points</td><td colspan="2">1000-points</td><td colspan="2">Average</td></tr><tr><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td></tr><tr><td>Phone</td><td>0.0025</td><td>0.0061</td><td>0.0179</td><td>0.0494</td><td>0.0166</td><td>0.0612</td><td>0.0253</td><td>0.1177</td><td>0.0259</td><td>0.1281</td><td>0.0882</td><td>0.3625</td></tr><tr><td>Wearable</td><td>0.0012</td><td>0.0029</td><td>0.0107</td><td>0.0369</td><td>0.0147</td><td>0.0519</td><td>0.0197</td><td>0.1041</td><td>0.016</td><td>0.1058</td><td>0.0623</td><td>0.3016</td></tr><tr><td>EEG</td><td>0.0087</td><td>0.0218</td><td>0.0199</td><td>0.0824</td><td>0.0245</td><td>0.1195</td><td>0.0299</td><td>0.1619</td><td>0.0308</td><td>0.1802</td><td>0.1138</td><td>0.5658</td></tr><tr><td rowspan="5">Correlation Coefficient</td><td rowspan="2">Signals</td><td colspan="2">5-points</td><td colspan="2">50-points</td><td colspan="2">100-points</td><td colspan="2">500-points</td><td colspan="2">1000-points</td><td colspan="2">Average</td></tr><tr><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td><td>STD</td><td>Range</td></tr><tr><td>Phone</td><td>0.0015</td><td>0.0038</td><td>0.0243</td><td>0.0832</td><td>0.0248</td><td>0.0964</td><td>0.0244</td><td>0.104</td><td>0.0247</td><td>0.104</td><td>0.0997</td><td>0.3914</td></tr><tr><td>Wearable</td><td>0.01</td><td>0.0252</td><td>0.0155</td><td>0.0702</td><td>0.0147</td><td>0.0866</td><td>0.0469</td><td>0.2299</td><td>0.0729</td><td>0.3905</td><td>0.16</td><td>0.8024</td></tr><tr><td>EEG</td><td>0.0392</td><td>0.0991</td><td>0.1077</td><td>0.4096</td><td>0.0955</td><td>0.4849</td><td>0.1319</td><td>0.7626</td><td>0.1533</td><td>0.99</td><td>0.5276</td><td>2.7462</td></tr></table>

To address the aforementioned issues, first, we propose a novel framework which can automatically learn distinctive features from raw EEG signals by developing a deep convolutional mapping component. Additionally, to grasp the characteristic information from different EEG application circumstance adaptively, we design a reinforced selective attention component that combines the benefits of attention mechanism [13] and deep reinforcement learning. Moreover, we overstep the challenge of chaotic information by working on EEG samples instead of segments. The single EEG sample only contains spatial information without spatial clue1. The main contributions of this work are highlighted as follows:

• We propose a general framework for automatic cognitive activity recognition to facilitate a scope of diverse cognitive application domains including intention recognition, person identification, and neurological diagnosis.   
• We design the reinforced selective attention model, by combining the deep reinforcement learning and attention mechanism, to automatically extract the robust and distinct deep features. Specially, we design a non-linear reward function to encourage the model to select the best attention area that leads to the highest classification accuracy. Besides, we customize the states and actions based on our cognitive activity recognition environment.   
• We develop a convolutional mapping method to explore the distinguishable spatial dependency and feed it to the classifier for classification, among selected EEG signals.   
• We demonstrate the effectiveness of the proposed framework using four real-world datasets concerning three representatives and challenging cognitive applications.

The experiment results demonstrate that the proposed framework outperforms the state-of-the-art and strong baselines by consistently achieving the accuracy of more than 96% and low latency.

Note that all the necessary reusable codes and datasets have been open-sourced for reproduction, please refer to this link2.

# II. ANALYSIS OF EEG SIGNALS

In this section, we demonstrate EEG signals’ unique characteristics (e.g., rapid-varying and chaotic) and that single samples are more suitable than segments for classification. By comparing EEG signals with two typical sensor signals collected by smartphone (accelerometers in Samsung Galaxy S2) and wearable sensors (Colibri wireless IMU). The participants are walking during the data collection session.

The brain activity is very complex and rapid varying, but EEG signals can only capture a few information through the discrete sampling of biological current. Figure 1 demonstrates the characteristics of rapidly varying and complex of EEG signals and provides the EEG topography of consecutive 5 samples. The sampling rate is 160 Hz while the sampling interval is 0.00625 second. It can be observed that the topography changes dramatically within such a tiny time interval.

Furthermore, to illustrate the chaotic of EEG signals, we compare EEG with smartphone and wearable sensors in two aspects: the time domain and the inter-samples correlations.

In the time domain, we evaluate the STD and range of sensor signals on five levels of sample length: 5, 50, 100, 500, 1000 continuous samples. The evaluations on the above five scales are expected to show the tendency that how the EEG characteristic varies with the sampling period.

The inter-sample correlation coefficient calculates the average cosine correlations between the specific sample and its neighbor samples (5, 50, 100, 500, and 1000 samples). A low correlation coefficient represents EEG signals dramatically and rapidly varying all the time.

As a result, Table I present the STD and range values in the time domain and correlation coefficient. We observe that EEG signals have the highest STD and range over all the five sample window scales both on time domain and correlation coefficient, compared with wearable sensor data and smartphone signals. This demonstrates that the EEG sample has more unstable correlations with neighbors and the instability is very high even in the nearest five samples. More specifically, EEG signals are very chaotic and rapidly changing at each single sampling point.

# III. PROPOSED METHOD

Based on the above analysis, we propose reinforced attentive convolutional neural networks (CNNs) to classify raw EEG signals accurately and efficiently directly. The overall workflow is shown in Figure 2.

# A. Replicate and Shuffle

To provide as much as possible information, we design an approach to exploit the spatial relationships among EEG signals. The signals belonging to different brain activities are supposed to have different spatial dependent relationships. We replicate and shuffle the input EEG signals on dimension-wise. Within this method, all the possible dimension arrangements have the equiprobable appearance.

Suppose the input raw EEG data are denoted by ${ \textbf { X } } =$ $\{ ( \mathbf { x } _ { i } , y _ { i } ) , i ~ = ~ 1 , 2 , \cdot \cdot \cdot I \}$ , where $\left( \mathbf { x } _ { i } , y _ { i } \right)$ denotes a single EEG sample and I denotes the number of samples. In each sample, the feature $\mathbf { x } _ { i } = \{ x _ { i k } , k = 1 , 2 , \cdot \cdot \cdot , K \} , \mathbf { x } _ { i } \in \mathbb { R } ^ { K }$ contains K elements corresponding to K EEG channels and $y _ { i } \in \mathbb { R }$ denotes the corresponding label. $x _ { i k }$ denotes the k-th dimension value in the i-th sample.

In real-world collection scenarios, the EEG data are generally concatenated following the distribution of biomedical EEG channels. However, the biomedical dimension order may not present the best spatial dependency. The exhausting method is too computationally expensive to exhaust all the possible dimension arrangements. For example, a 64-channel EEG sample has $A _ { 6 4 } ^ { 6 4 } = 1 . 2 8 \times 1 0 ^ { 8 9 }$ combinations, which is an astronomical figure.

To provide more potential dimension combinations, we propose a method called Replicate and Shuffle (RS). RS is a two-step mapping method which maps $\mathbf { x } _ { i }$ to a higher dimensional space $\mathbf { x } _ { i } ^ { \prime }$ with complete element combinations:

$$
\mathbf {x} _ {i} \in \mathbb {R} ^ {K} \rightarrow \mathbf {x} _ {i} ^ {\prime} \in \mathbb {R} ^ {K ^ {\prime}}, K ^ {\prime} > K \tag {1}
$$

In the first step (Replicate), replicating $\mathbf { x } _ { i }$ for $h = K ^ { \prime } / K { + } 1$ times. Then, we get a new vector with length as h ∗ K which is not less than $K ^ { \prime } ;$ in the second step (Shuffle), we randomly shuffle the replicated vector in the first step and intercept the first $K ^ { \prime }$ elements to generate $\mathbf { x } _ { i } ^ { \prime }$ . Theoretically, compared with $\mathbf { x } _ { i } , \mathbf { x } _ { i } ^ { \prime }$ contains more diverse dimension combinations. Note, this RS operation only be performed once for a specific input dataset in order to provide a stable environment for the following reinforcement learning.

# B. Reinforced Selective Attention

Inspired by the fact that the optimal spatial relationship only depends on a subset of feature dimensions, we introduce an attention zone to focus on a fragment of feature dimensions. Here, the attention zone is optimized by deep reinforcement learning, which has been proved to be stable and wellperformed in policy learning.

In particular, we aim to detect the optimal dimension combination, which includes the most distinctive spatial dependency among EEG signals. Since $K ^ { \prime } { \mathrm { , } }$ , the length of $\mathbf { x } _ { i } ^ { \prime } ,$ is too large and computationally expensive, to balance the length and the information content, we introduce the attention mechanism [14] since its effectiveness has been demonstrated in recent research areas such as speech recognition [15]. We attempt to emphasize the informative fragment in $\mathbf { x } _ { i } ^ { \prime }$ and denote the fragment by $\bar { \mathbf { x } } _ { i }$ , which is called attention zone. Let $\bar { \mathbf { x } } _ { i } \in \mathbb { R } ^ { \bar { K } }$ and $\bar { K }$ denote the length of the attention zone which is automatically learned by the proposed algorithm. We employ deep reinforcement learning to discover the best attention zone [16].

As shown in Figure 2, the detection of the best attention zone includes two key components: the environment (including state transition and reward model) and the agent. Three elements (the state s, the action a, and the reward r) are exchanged in the interaction between the environment and the agent. All of the three elements are customized based on our context in this study. Next, we introduce the design of the crucial components of our deep reinforcement learning structure:

• The state $\mathcal { S } = \{ s _ { t } , t = 0 , 1 , \cdot \cdot \cdot , T \} , s _ { t } \in \mathbb { R } ^ { 2 }$ describes the position of the attention zone, where t denotes the time stamp. Since the attention zone is a shifting fragment on $1 - \mathrm { D } \ \mathbf { x } _ { i } ^ { \prime } .$ , we design two parameters to define the state: $s _ { t } ~ = ~ \{ s t a r t _ { i d x } ^ { t } , e n d _ { i d x } ^ { t } \}$ , where $s t a r t _ { i d x } ^ { t }$ and $e n d _ { i d x } ^ { t }$ denote the start index and the end index of the attention zone3, separately. In the training, $s _ { 0 }$ is initialized as

$$
s _ {0} = \left[ (K ^ {\prime} - \bar {K}) / 2, (K ^ {\prime} + \bar {K}) / 2 \right] \tag {2}
$$

• The action $\mathcal { A } = \{ a _ { t } , t = 0 , 1 , \cdot \cdot \cdot , T \} \in \mathbb { R } ^ { 4 }$ describes which action the agent could choose to act on the environment. Here at time stamp t, the state transition chooses one action to implement following the agent’s policy π:

$$
s _ {t + 1} = \pi (s _ {t}, a _ {t}) \tag {3}
$$

In our case, we define four categories of actions (Figure 3) for the attention zone: left shifting, right shifting, extend, and condense. For each action, the attention zone moves a random distance $d \in [ 1 , d ^ { u } ]$ where $d ^ { u }$ is the upper boundary. For left shifting and right shifting actions, the attention zone shifts light-ward or right-ward with the step d; for the extend and condense actions, both $s t a r t _ { i d x } ^ { t }$ and $e n d _ { i d x } ^ { t }$ are moving d. At last, if the state start index or end index is beyond the boundary, a clip operation is conducted. For example, if $s t a r t _ { i d x } ^ { t } = - 5$ which is lower than the lower boundary 0, we clip the start index as sta $r t _ { i d x } ^ { t } = 0$ .

3For example, for a random $\begin{array} { r c l } { \mathbf { x } _ { i } ^ { \prime } } & { = } & { \left[ 3 , 5 , 8 , 9 , 2 , 1 , 6 , 0 \right] } \end{array}$ , the state {starttidx $\{ s t a r t _ { i d \ast } ^ { t } = \stackrel { . } { 2 } , e n d _ { i d x } ^ { t } = 5 \}$ i  is sufficient to determine the attention zone as [8, 9, 2, 1].

![](images/dea9af71e8a58de4c7d9f97f54a348653fc220806374ee007901d526c540f2e0.jpg)



Fig. 2: Flowchart of the proposed approach. The input raw EEG single sample $\mathbf { x } _ { i }$ (K denotes the Kth element) is replicated and shuffled to provide more latent spatial combinations of feature dimensions. Then, an attention zone $\bar { \mathbf { x } } _ { i }$ , which is a fragment in $\mathbf { x } _ { i } ^ { \prime } ,$ , with the state $s _ { t } = \{ s t a r t _ { i d x } ^ { t } , e n d _ { i d x } ^ { t } \}$ is selected. The selected attention zone is input to the state transition and the reward model. In each step $t ,$ one action is selected by the state transition to update $s _ { t }$ based on the agent’s feedback. The reward model evaluates the quality of the attention zone by the reward score $r _ { t } .$ . The dueling DQN is employed to discover the best attention zone $\bar { \mathbf { x } } _ { i } ^ { * }$ which will be fed into the convolutional mapping procedure to extract the spatial dependency representation. The represented features will be used for the classification. F CL denotes a fully connected layer. The reward model is the combination of the convolutional mapping and the classifier.

![](images/cf2cc38badd17a3d2fc605d7a3b2dbe346238331a9039f02500b3761cbc26832.jpg)

![](images/36c16ed0b07390090cc6a5dc27a749b60975b9a2a89c70b8a16bc918d62dbf5d.jpg)

![](images/62535ce6f283b5593b79051ec0635168e1d55343196a0b185c69b52fa037253b.jpg)

![](images/a7da2adb533d9d8b846eca0351bc438f7172272eeda2b7896def29ab89c361f4.jpg)

# Left Shifting RightShifting

# Extend

# Condense

Fig. 3: Four actions in the state transition: left shifting, right shifting, extend, and condense. The dashed line indicates the position of the attention zone before the action while the solid line indicates after the action.

• The reward $\mathcal { R } = \{ r _ { t } , t = 0 , 1 , \cdot \cdot \cdot , T \} \in \mathbb { R }$ is calculated by the reward model, which will be detailed later. The reward model Φ:

$$
r _ {t} = \Phi (s _ {t}) \tag {4}
$$

receives the current state and returns an evaluation as the reward.

Reward Model. Next, we introduce in detail the design of the reward model. The purpose of the reward model is to evaluate how the current state impacts the classification performance. Intuitively, the state which leads to better classification performance should have a higher reward: $r _ { t } = \mathcal { F } ( s _ { t } )$ . We set the reward modal $\mathcal { F }$ as a combination of the convolutional mapping and classification (Section III-C). Since in the practical approach optimization, the higher the accuracy is, the more difficult to increase the classification accuracy. For example, improving the accuracy on a higher level (e.g., from 90% to 100%) is much harder than on a lower level(e.g., from 50% to 60%). To encourage accuracy improvement at the higher level, we design a non-linear reward function:

$$
r _ {t} = \frac {e ^ {a c c}}{e - 1} - \beta \frac {\bar {K}}{K ^ {\prime}} \tag {5}
$$

where acc denotes the classification accuracy. The function contains two parts; the first part is a normalized exponential function with the exponent acc ∈ [0, 1], this part encourages the reinforcement learning algorithm to search the better $s _ { t }$ which leads to a higher acc. The motivation of the exponential function is that: the reward growth rate is increasing with the accuracy’s increase4. The second part is a penalty factor for the attention zone length to keep the bar shorter and the $\beta$ is the penalty coefficient.

In summary, the aim of the deep reinforcement learning is to learn the optimal attention zone $\overline { { \mathbf { x } } } _ { i } ^ { * }$ which leads to the maximum reward. The selective mechanism totally iterates $N = n _ { e } * n _ { s }$ times where $n _ { e }$ and $n _ { s }$ denote the number of episodes and steps [17], respectively. ε-greedy method [18] is employed in the state transition, which chooses a random action with probability $1 - \varepsilon \ \mathrm { o r }$ an action according to the optimal Q function argmax $\cdot _ { a _ { t } \in \mathcal { A } } Q ( s _ { t } , a _ { t } )$ with probability ε. In formula,

$$
a _ {t + 1} = \left\{ \begin{array}{c c} \operatorname{argmax} _ {a _ {t} \in \mathcal {A}} Q \left(s _ {t}, a _ {t}\right) & \varepsilon^ {\prime} <   \varepsilon \\ \bar {a} \in \mathcal {A} & \text { otherwise } \end{array} \right. \tag {6}
$$

where $\varepsilon ^ { \prime } \in [ 0 , 1 ]$ is random generated for each iteration while a¯ is random selected in A.

For better convergence and quicker training, the ε is gradually increasing with the iterating. The increment $\varepsilon _ { 0 }$ follows:

$$
\varepsilon_ {t + 1} = \varepsilon_ {t} + \varepsilon_ {0} N \tag {7}
$$

Agent Policy and Optimization. The Dueling DQN (Deep Q Networks [17]) is employed as the optimization policy $\pi ( s _ { t } , a _ { t } )$ , which is enabled to learn the state-value function efficiently. The primary reason we employ a dueling DQN to uncover the best attention zone is that it updates all the four Q values at every step while other policies only update one Q value at each step. The Q function measures the expected sum of future rewards when taking that action and following the optimal policy thereafter. In particular, for the specific step t, we have:

$$
\begin{array}{l} Q (s _ {t}, a _ {t}) = \mathbb {E} (r _ {t + 1} + \gamma r _ {t + 2} + \gamma^ {2} r _ {t + 3} \dots) \\ = \sum_ {n = 0} ^ {\infty} \gamma^ {k} r _ {t + k + 1} \tag {8} \\ \end{array}
$$

where $\gamma \in \ [ 0 , 1 ]$ is the decay parameter that trade-off the importance of immediate and future rewards while n denotes the number of following step. The value function $V ( s _ { t } )$ estimate the expected reward when the agent is in state s. The Q function is related to the pair $( s _ { t } , a _ { t } )$ while the value function only associate with $s _ { t } .$ .

Dueling DQN learns the Q function through the value function $V ( s _ { t } )$ and the advantage function $A ( s _ { t } , a _ { t } )$ and combines them by the following formula

$$
Q (s _ {t}, a _ {t}) = \theta V (s _ {t}) + \theta^ {\prime} A (s _ {t}, a _ {t}) \tag {9}
$$

where $\theta , \theta ^ { \prime } \in \Theta$ are parameters in the dueling DQN network and are optimized automatically. Equation: 9 is unidentifiable which can be observed by the fact that we can not recover $V ( s _ { t } )$ and $A ( s _ { t } , a _ { t } )$ uniquely with the given $Q ( s _ { t } , a _ { t } )$ . To address this issue, we can force the advantage function equals to zero at the chosen action. That is, we let the network implement the forward mapping:

$$
Q (s _ {t}, a _ {t}) = V (s _ {t}) + \left[ A (s _ {t}, a _ {t}) - \max _ {a _ {t + 1} \in \mathcal {A}} (A (s _ {t}, a _ {t + 1})) \right] \tag {10}
$$

Therefore, for the specific action a∗, if

$$
\operatorname{argmax} _ {a _ {t + 1} \in \mathcal {A}} Q (s _ {t}, a _ {t + 1}) = \operatorname{argmax} _ {a _ {t + 1} \in \mathcal {A}} A (s _ {t}, a _ {t + 1}) \tag {11}
$$

then we have

$$
Q (s _ {t + 1}, a *) = V (s _ {t}) \tag {12}
$$

Thus, as shown in the Figure 2 (the second last layer of the agent part), the stream $V ( s _ { t } )$ is forced to learn an estimation of the value function, while the other stream produces an estimation of the advantage function.

To assess the Q function, we optimize the following cost function at the i-th iteration:

$$
\begin{array}{l} L _ {i} \left(\Theta_ {i}\right) = \mathbb {E} _ {s _ {t}, a _ {t}, r _ {t}, s _ {t + 1}} \left[ \left(\bar {y} _ {i} - Q \left(s _ {t}, a _ {t}\right)\right) ^ {2} \right] \tag {13} \\ = \mathbb {E} _ {s _ {t}, a _ {t}, r _ {t}, s _ {t + 1}} [ (\bar {y} _ {i} - \theta V (s _ {t}) + \theta^ {\prime} A (s _ {t}, a _ {t})) ^ {2} ] \\ \end{array}
$$

with

$$
\bar {y} _ {i} = r _ {t} + \gamma \max _ {a _ {t + 1}} Q (s _ {t + 1}, a _ {t + 1}) \tag {14}
$$

The gradient update method is

$$
\begin{array}{l} \nabla_ {\Theta_ {i}} L _ {i} (\Theta_ {i}) = \mathbb {E} _ {s _ {t}, a _ {t}, r _ {t}, s _ {t + 1}} [ (\bar {y} _ {i} - Q (s _ {t}, a _ {t})) \nabla_ {\Theta_ {i}} Q (s _ {t}, a _ {t}) ] \\ = \mathbb {E} _ {s _ {t}, a _ {t}, r _ {t}, s _ {t + 1}} [ (\bar {y} _ {i} - \theta V (s _ {t}) - \theta^ {\prime} A (s _ {t}, a _ {t})) \\ \left. \nabla_ {\Theta_ {i}} \left(\theta V \left(s _ {t}\right) + \theta^ {\prime} A \left(s _ {t}, a _ {t}\right)\right) \right] \tag {15} \\ \end{array}
$$

# C. Convolutional Mapping

For each attention zone, we further exploit the potential spatial dependency of selected features $\bar { \mathbf { x } } _ { i } ^ { * } .$ . Since we focus on a single sample, the EEG sample only contains a numerical vector with very limited information and is easily corrupted by noise. To amend this drawback, we attempt to mapping the EEG single sample from the original space $\mathcal { O } \in R ^ { \bar { K } }$ to a sparsity space $\tau \in \bar { R } ^ { M }$ by a CNN structure.

To extract as more potential spatial dependencies as possible, we employ a convolutional layer [19] with many filters to scan on the learned attention zone $\bar { \mathbf { x } } _ { i } ^ { * }$ . The convolutional mapping structure contains five layers (as shown in Figure 2): the input layer receives the learned attention zone, the convolutional layer followed by one fully connected layer, and the output layer. The one-hot ground truth is compared with the output layer to calculate the training loss.

The Relu non-linear activation function is applied to the convolutional outputs. We describe the convolutional layer as follows:

$$
x _ {i j} ^ {c} = \operatorname{ReLU} \left(\sum_ {b = 1} ^ {\bar {b}} W _ {c} \bar {x} _ {i j} ^ {*}\right) \tag {16}
$$

where $\boldsymbol { x } _ { i j } ^ { c }$ denotes the outcome of the convolutional layer while ¯b and $W _ { c }$ denote the length of filter and the filter weights, respectively. The pooling layer aims to reduce the redundant information in the convolutional outputs to decrease the computational cost. In our case, we try to keep as much information as possible. Therefore, our method does not employ a pooling layer. Then, in the fully connected layer and output layer

$$
x _ {i} ^ {f} = \operatorname{ReLU} \left(W ^ {f} x _ {i} ^ {c} + b ^ {f}\right) \tag {17}
$$

ALGORITHM 1: The Proposed Approach   
Input: Raw EEG signals X
Output: Predicted cognitive activity label $y_{i}^{\prime}$ 1: Initialization $s_{0}$ ;
2: RS: $\bar{x}_{i} \leftarrow x_{i}^{\prime}$ ;
3: Reinforced Selective Attention:
4: if t < N then
5: $a_{t} = argmax_{a_{t} \in \mathcal{A}} Q(s_{t}, a_{t})$ 6: $s_{t+1} = \pi(s_{t}, a_{t})$ 7: $r_{t} = \mathcal{F}(s_{t})$ 8: $\varepsilon_{t+1} = \varepsilon_{t} + \varepsilon_{0} N$ 9: $\bar{x}_{i}^{*} \leftarrow \bar{x}_{i}, a_{t}, s_{t}, r_{t}$ 10: end if
11: Convolutional Mapping & Classifier:
12: if iteration < N' then
13: $y_{i}^{\prime} \leftarrow \bar{x}_{i}^{*}$ 14: end if
15: return $y_{i}^{\prime}$

$$
y _ {i} ^ {\prime} = \text { softmax } (W ^ {o} x _ {i} ^ {f} + b ^ {o}) \tag {18}
$$

where $W ^ { f } , W ^ { o } , b ^ { f } , b ^ { o }$ denote the corresponding weights and biases, respectively. The $y ^ { \prime }$ denotes the predicted label. The cost function is measured by cross entropy, and the $\ell _ { 2 }$ -norm (with parameter λ) is adopted as regularization to prevent overfitting.:

$$
c o s t = - \sum_ {x} y _ {i} ^ {\prime} l o g (y _ {i}) + \lambda \ell_ {2} \tag {19}
$$

The AdamOptimizer algorithm optimizes the cost function. The fully connected layer extracts as the represented features and fed them into a lightweight nearest neighbor classifier. The convolutional mapping updates for $N ^ { \prime }$ iterations. The proposed adaptive cognitive activity recognition with reinforced attentive convolutional neural networks is shown in Algorithm 1.

# IV. EXPERIMENTS

In this section, we report our evaluation of the proposed approach on three datasets corresponding to different application scenarios, with a focus on accuracy, latency, and resilience.

# A. Application Scenarios and Datasets

1) Application Scenarios: We evaluate our approach on various datasets in three applications of EEG-based Brain-Computer Interfaces.

Movement Intention Recognition (MIR). EEG signals measure human brain activities. Intuitively, different human intention will lead to diverse EEG patterns [5]. Intention recognition plays a significant role in practical scenarios such as smart home, assisted living [6], brain typing [5], and entertainment. For the disabled and elders, intent recognition can help them to interact with external smart devices such as wheelchairs or service robots real-time BCI systems. Besides, for people without vocal ability, they may have the chance to express their thoughts with the help of certain intention recognition technologies (e.g., brain typing). Even for the healthy human being, intent recognition can be used in video game playing and other daily living applications.

Person Identification (PI). EEG-based biometric identification [8] is an emerging person identification approach, which is highly attack-resilient. It has the unique advantage of avoiding or alleviating the threat of being deceived which is often faced by other identification techniques. This technique can be deployed in identification and authentication scenarios such as bank security system and customs security check.

Neurological Diagnosis (ND). EEG signals collected in the unhealthy state differ significantly from the ones collected in the normal state concerning frequency and pattern of neuronal firing [2]. Therefore, EEG signals have been used for neurological diagnosis for decades [39]. For example, the epileptic seizure is a common brain disorder that affects around 1% of the population, and an EEG analysis of the patient could detect its octal state.

2) Datasets: To evaluate how the proposed approach works in the aforementioned application scenarios, we choose several EEG datasets with various collection equipment, sampling rates, and data sources. We utilize motor imagery EEG signals from a public dataset eegmmidb for intention recognition, the EEG-S dataset for person identification, and the TUH dataset for neurological diagnosis.

eegmmidb. EEG motor movement/imagery database (eegmmidb)5 were collected by the BCI200 EEG system, which recordsed the brain signals using 64 channels with a sampling rate of 160Hz. EEG signals were recorded when the subject was imaging about certain actions (without any physical action). This dataset includes 560,000 samples collected from 20 subjects. Each sample have one of five different labels: eye-closed, left hand, right hand, both hands, and both feed. Each sample is a vector of 64 elements that correspond to 64 channel of EEG data.

EEG-S. EEG-S is a subset of eegmmidb, in which the data were gathered while the subject kept eyes closed and stayed relaxed. Eight subjects were involved and each subject generated 7,000 samples. Labels are the subjects’ IDs, which range within [0-7].

TUH. TUH [40] is a neurological seizure dataset of clinical EEG recordings. The EEG recording is associated with 21 channels from a 10/20 configuration and a sampling rate of 250 Hz. We selected 12,000 samples from each of five subjects (2 males and three females). Half of the samples were labeled as epileptic seizure state. The remaining samples were labeled as the normal state.

3) Parameter Settings: We configured the default settings of our approach as follows. In the selective attention learning: $\bar { K } = 1 2 8$ , the Dueling DQN had 4 lays and the node number in each layer were: 2 (input layer), 32 (FCL), 4 $( A ( s _ { t } , a _ { t } ) )$ $+ \mathrm { ~ 1 ~ } ( V ( s _ { t } ) )$ , and 4 (output). The decay parameter $\gamma = 0 . 8 ,$ , $n _ { e } = n _ { s } = 5 0 , N = 2 , 5 0 0 , \epsilon = 0 . 2 , \epsilon _ { 0 } = 0 . 0 0 2$ , learning rate= 0.01, memory size = 2000, length penalty coefficient $\beta = 0 . 1$ , and the minimum length of attention zone was set as 10. In the convolutional mapping, the node number in the input layer equaled to the number of attention zone dimensions. In the convolutional layer: the stride had the shape [1, 1], the filter size was set to [1, 2], the depth to 10, and the non-linear function as ReLU. The padding method was zero-padding. No pooling layer was adopted. The subsequent fully connected layer had 100 nodes. The learning rate was 0.001 while the \`2-norm coefficient λ equaled 0.001. The transformation was trained for 2000 iterations. In addition, we configured the key parameters of the baselines as follows: Linear SVM (C = 1), Random Forest (RF, $n \ = \ 2 0 0 )$ , KNN (k = 1). In LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit), $n _ { s t e p s } = 5 $ , other settings were the same as [6]. The CNN had the same structure and hyper-parameters setting with the convolutional mapping component in the proposed show.

TABLE II: Comparison with baselines 

<table><tr><td rowspan="2">Scenarios</td><td rowspan="2">Datasets</td><td rowspan="2">Metrics</td><td colspan="5">Non-Deep Learning Baselines</td><td colspan="4">Deep Learning Baselines</td></tr><tr><td>SVM</td><td>RF</td><td>KNN</td><td>AB</td><td>LDA</td><td>LSTM</td><td>GRU</td><td>CNN</td><td>Ours</td></tr><tr><td rowspan="4">MIR</td><td rowspan="4">eegmmidb</td><td>Accuracy</td><td>0.5596</td><td>0.6996</td><td>0.5814</td><td>0.3043</td><td>0.5614</td><td>0.648</td><td>0.6786</td><td>0.91</td><td>0.9632</td></tr><tr><td>Precision</td><td>0.5538</td><td>0.7311</td><td>0.6056</td><td>0.2897</td><td>0.5617</td><td>0.6952</td><td>0.8873</td><td>0.9104</td><td>0.9632</td></tr><tr><td>Recall</td><td>0.5596</td><td>0.6996</td><td>0.5814</td><td>0.3043</td><td>0.5614</td><td>0.6446</td><td>0.6127</td><td>0.9104</td><td>0.9632</td></tr><tr><td>F1-score</td><td>0.5396</td><td>0.6738</td><td>0.5813</td><td>0.2037</td><td>0.5526</td><td>0.6619</td><td>0.7128</td><td>0.9103</td><td>0.9632</td></tr><tr><td rowspan="4">PI</td><td rowspan="4">EEG-S</td><td>Accuracy</td><td>0.6604</td><td>0.9619</td><td>0.9278</td><td>0.35</td><td>0.6681</td><td>0.9571</td><td>0.9821</td><td>0.998</td><td>0.9984</td></tr><tr><td>Precision</td><td>0.6551</td><td>0.9625</td><td>0.9336</td><td>0.3036</td><td>0.6779</td><td>0.9706</td><td>0.9858</td><td>0.998</td><td>0.9984</td></tr><tr><td>Recall</td><td>0.6604</td><td>0.962</td><td>0.9279</td><td>0.35</td><td>0.6681</td><td>0.9705</td><td>0.9857</td><td>0.998</td><td>0.9984</td></tr><tr><td>F1-score</td><td>0.6512</td><td>0.9621</td><td>0.9282</td><td>0.2877</td><td>0.668</td><td>0.9705</td><td>0.9857</td><td>0.998</td><td>0.9984</td></tr><tr><td rowspan="4">ND</td><td rowspan="4">TUH</td><td>Accuracy</td><td>0.7692</td><td>0.92</td><td>0.9192</td><td>0.5292</td><td>0.7675</td><td>0.6625</td><td>0.6625</td><td>0.9592</td><td>0.9975</td></tr><tr><td>Precision</td><td>0.7695</td><td>0.9206</td><td>0.923</td><td>0.7525</td><td>0.7675</td><td>0.6538</td><td>0.6985</td><td>0.9593</td><td>0.9975</td></tr><tr><td>Recall</td><td>0.7692</td><td>0.92</td><td>0.9192</td><td>0.5292</td><td>0.7675</td><td>0.6417</td><td>0.6583</td><td>0.9592</td><td>0.9975</td></tr><tr><td>F1-score</td><td>0.7692</td><td>0.9199</td><td>0.9188</td><td>0.3742</td><td>0.7675</td><td>0.6449</td><td>0.6685</td><td>0.9592</td><td>0.9975</td></tr></table>

TABLE III: Comparison with the state-of-the-art approaches 

<table><tr><td>Scenarios</td><td>Datasets</td><td>Metrics</td><td colspan="6">State-of-the-art</td></tr><tr><td rowspan="10">MIR</td><td rowspan="10">eegmmidb</td><td>Method</td><td>Rashid [20]</td><td>Zhang [5]</td><td>Ma [21]</td><td>Alomari [22]</td><td>Sita [23]</td><td>Alomari [24]</td></tr><tr><td>Accuracy</td><td>0.9193</td><td>0.9561</td><td>0.6820</td><td>0.8679</td><td>0.7584</td><td>0.8515</td></tr><tr><td>Precision</td><td>0.9156</td><td>0.9566</td><td>0.6971</td><td>0.8788</td><td>0.7631</td><td>0.8469</td></tr><tr><td>Recall</td><td>0.9231</td><td>0.9621</td><td>0.7325</td><td>0.8786</td><td>0.7702</td><td>0.8827</td></tr><tr><td>F1-score</td><td>0.9193</td><td>0.9593</td><td>0.7144</td><td>0.8787</td><td>0.7666</td><td>0.8644</td></tr><tr><td>Method</td><td>Shenoy [25]</td><td>Szczuko [26]</td><td>Stefano [27]</td><td>Pinheiro [28]</td><td>Kim [29]</td><td>Ours</td></tr><tr><td>Accuracy</td><td>0.8308</td><td>0.9301</td><td>0.8724</td><td>0.8488</td><td>0.8115</td><td>0.9632</td></tr><tr><td>Precision</td><td>0.8301</td><td>0.9314</td><td>0.8874</td><td>0.8513</td><td>0.8128</td><td>0.9632</td></tr><tr><td>Recall</td><td>0.8425</td><td>0.9287</td><td>0.8874</td><td>0.8569</td><td>0.8087</td><td>0.9632</td></tr><tr><td>F1-score</td><td>0.8363</td><td>0.9300</td><td>0.8874</td><td>0.8541</td><td>0.8107</td><td>0.9632</td></tr><tr><td rowspan="5">PI</td><td rowspan="5">EEG-S</td><td>Method</td><td>Ma [30]</td><td>Yang [31]</td><td>Rodrigues [32]</td><td>Frashini [12]</td><td>Thomas [33]</td><td>Ours</td></tr><tr><td>Accuracy</td><td>0.88</td><td>0.99</td><td>0.8639</td><td>0.956</td><td>0.9807</td><td>0.9984</td></tr><tr><td>Precision</td><td>0.8891</td><td>0.9637</td><td>0.8721</td><td>0.9458</td><td>0.9799</td><td>0.9984</td></tr><tr><td>Recall</td><td>0.8891</td><td>0.9594</td><td>0.8876</td><td>0.9539</td><td>0.9887</td><td>0.9984</td></tr><tr><td>F1-score</td><td>0.8891</td><td>0.9615</td><td>0.8798</td><td>0.9498</td><td>0.9843</td><td>0.9984</td></tr><tr><td rowspan="5">ND</td><td rowspan="5">TUH</td><td>Method</td><td>Ziyabari [34]</td><td>Harati [35]</td><td>Zhang [36]</td><td>Goodwin [37]</td><td>Golmohammadi [38]</td><td>Ours</td></tr><tr><td>Accuracy</td><td>0.9382</td><td>0.9429</td><td>0.994</td><td>0.924</td><td>0.9479</td><td>0.9975</td></tr><tr><td>Precision</td><td>0.9321</td><td>0.9503</td><td>0.9951</td><td>0.9177</td><td>0.9438</td><td>0.9975</td></tr><tr><td>Recall</td><td>0.9455</td><td>0.9761</td><td>0.9951</td><td>0.9375</td><td>0.9522</td><td>0.9975</td></tr><tr><td>F1-score</td><td>0.9388</td><td>0.9630</td><td>0.9951</td><td>0.9275</td><td>0.9480</td><td>0.9975</td></tr></table>

# B. Overall Comparison

1) Comparison Baselines: To measure the accuracy of the proposed method, we compared with a set of baseline methods including five non-deep learning and three deep learning based baselines. Furthermore, we chose some competitive state-ofthe-art algorithms for every single task separately.

# MIR Baselines:

Rashid et al. [20] use Discrete Wavelet Transform (DWT) to extract features and feed into Levenberg-Marquardt Algorithm (LMA) based neural network for motor imagery EEG intention recognition.

Zhang et al. [5] design a joint convolutional recurrent neural network to learn robust high-level feature presentations by low-dimensional dense embeddings from raw MI-EEG signals.

Ma et al. [21] transform the EEG data into a spatial sequence to learn more valuable information through RNN.

Alomari et al. [22] analyze the EEG characteristics by the Coiflets wavelets and manually extract features using different amplitude estimators. The extracted features are inputted into SVM classifier for EEG data recognition.

Sita et al. [23] employ independent component analysis (ICA) to extract features which are fed to a quadratic discriminant analysis (QDA) classifier.

Alomari et al. [24] use wavelet transformation to filter and process EEG signals. Then calculate the Root Mean Square and Mean Absolute Value features for EEG recognition.

Shenoy et al. [25] propose a regularization approach based on shrinkage estimation to handle small sample problem and retain subject-specific discriminative features.

Szczuko [26] design a rough set based classifier for the aim of EEG data classification.

Stefano et al. [27] extract the mu $( 7 \sim 1 3 H z )$ and beta $( 1 3 \sim 3 0 H z )$ bands’ power spectral density (PSD) as manual features to discriminate different motor imagery intentions.

Pinheiro et al. [28] adopt a C4.5 decision tree as the classifier to distinguish the manually extracted EEG features such as arithmetic mean and maximum value of the Fourier transform.

![](images/e95f95d9edc051ebf5d3963f10e8200c70ad58edd6c8fd5aa74088d3bf7f501f.jpg)



(a) CM of eegmmidb

![](images/3a979b49253c84cf475848205f1050d77451ca45c88036249eed89191cd26d5f.jpg)



(b) CM of EEG-S

![](images/62c39a481beb5aa1020bcd6ceca25ed6d3a7b50878912e3be70898706173e64d.jpg)



(c) CM of TUH

![](images/a2255e841e876cd7cb234ae24cebf7d5589830c7853d61e2825bc1f91a6e6437.jpg)



(d) ROC of eegmmidb

![](images/1abe909be6f4323d98112ef7dc4eaed4c9ebb784f02d4a159275826b7a06ba27.jpg)



(e) ROC of EEG-S

![](images/44f2349593c250c021f2b914d7c2775ecec689fbef5a028bb96d86ca230ba84b.jpg)



(f) ROC of TUH   
Fig. 4: Confusion matrix and ROC curves with AUC scores of each dataset. CM denotes confusion matrix.

Kim et al. [29] use a multivariate empirical mode decomposition to obtain the mu and beta rhythms from the nonlinear EEG signals.

# PI Baselines:

Ma et al. [30] adopt a CNN structure to automatically extract an individual’s best, unique neural features with the aim of person identification.

Yang et al. [31] present an approach for biometric identification using EEG signals based on features extracted with the Hilbert-Huang Transform (HHT).

Rodrigues et al. [32] propose the Flower Pollination Algorithm under different transfer functions to select the best subset of channels that maximizes the accuracy, which is measured using the Optimum-Path Forest classifier.

Frashini et al. [12] decompose EEG signals into standard frequency bands by a band-pass filter and estimate the functional connectivity between the sensors using the Phase Lag Index. The resulting connectivity matrix was used to construct a weighted network for person identification.

Thomas et al. [33] extract sample entropy features from the delta, theta, alpha, beta and gamma bands of 64 channel EEG data, which are evaluated for subject-identification.

# ND Baselines:

Ziyabari et al. [34] adopt a hybrid deep learning architecture, including LSTM and stacked denoising Autoencoder, that integrates temporal and spatial context to detect the seizure.

Harati et al. [35] demonstrate that a variant of the filter bank-based approach and provides a substantial reduction in the overall error rate.

Zhang et al. [36] extract a list of 24 feature types from the scalp EEG signals and found 170 out of the 2794 features to classify epileptic seizures accurately.

Goodwin et al. [37] combine recent advances in RNN with access to textual data in EEG reports to automatically extracting word- and report-level features and infer underspecified information from EHRs (electronic health records).

Golmohammadi et al. [38] propose a seizure detection method by using hidden Markov models (HMM) for sequential decoding and deep learning networks.

2) Results: Tables II presents the classification metrics comparison between our approach and well-known baselines (including Non-DL and DL baselines), where DL, AdaB, LDA represent deep learning, Adaptive Boosting, and Linear Discriminant Analysis, respectively. The results show that our approach achieved the highest accuracy on all the datasets. Specifically, the proposed approach achieved the highest accuracy of 0.9632, 0.9984, and 0.9975 on eegmmidb, EEG-S, and TUH dataset, respectively. Further, we conducted an ablation study by comparing our method, which mainly combined selective attention mechanism and CNN, with the solo CNN. It turned out that our approach outperformed CNN, demonstrating the proposed selective attention mechanism improved the distinctive feature learning.We show the confusion matrix and ROC curves (including the AUC scores) of each dataset in Figure 4. In Figure 4a, ‘L’, ‘R’, and ‘B’ denote left, right, and both, respectively.

Besides, to further evaluate the performance of our model, we compared our framework with 21 state-of-the-art methods which using the same dataset. In particular, we compared with

![](images/0074d8375829346f40f4d73e37ea60361cad7e29d24eb74972cb662849a78aa3.jpg)



Fig. 5: Latency comparison

![](images/3de98d3559927493f6cc490f1e163fd9e8250a2b31c6073e7938d273520312ed.jpg)



Fig. 6: Varying # of channels

11 competitive state-of-the-art methods over motor imagery classification and five cutting edges separately over person identification and neurological diagnosis scenarios. Table III shows the comparison results.

We could observed that our proposed framework consistently outperformed a set of widely used baseline methods and strong competitors on three different datasets. The performance shows a significant improvement compared with other baselines. These datasets were collected using different EEG hardware, ranging from high-precision medical equipment to off-the-shelf EEG headset with a different number of EEG channels. Regarding the seizure diagnosis in ND, by setting the normal state as impostor while the seizure state as genuine, our approach gained a False Acceptance Rate (FAR) of 0.0033 and a False Rejective Rate (FRR) of 0.0017. This outperformed the existing methods by a large margin [11], [35], [37], [38].

# C. Resilience Evaluation

In this section, we focus on evaluating the resilience of proposed method in coping with various number of EEG signal channels, and incomplete EEG signals.

In practice, the number of EEG channels of EEG devices are diverse due to two reasons. First, different off-the-shelf or onthe-shelf devices have various channels numbers. Intuitively, the quality of signals and the contained information is directly associated with the number of channels. In the meantime, the devices with more channels usually are more expensive and less portable. Second, incomplete EEG signals cause the degradation of BCI applications. It could happen when some electrical nodes are loosened because of weak maintenance of EEG devices. To investigate the robustness of incomplete EEG signals with missing channels, we also conduct experiments by randomly selecting part of a proportion of signal channels over three datasets. For example, by selecting 20% of channels on the eegmmidb dataset, the selected channel number is $1 2 ~ = ~ r o u n d ( 6 4 * 0 . 2 )$ . Figure 6 shows the experiments results (0.4 denotes the accuracy and 20% denotes the channel percentage used for training). The radar chart demonstrates that eegmmidb and EEG-S, both with 64 channels, can achieve competitive accuracy even with only 20% signal channels. In contrast, TUH (21 channels) is highly dependent on the channel numbers. The reason is that TUH only remains five channels for 20% channel percentage, respectively. According to our experience, the proposed framework requires at least eight EEG channels to achieve high accuracy.

# D. Latency Analysis

Except for the high accuracy of EEG signal classification, the low latency is another critical requirement for the success of real-world BCI applications.

In this section, we take the eegmmidb dataset as an example to compare the latency of the proposed framework with several state-of-the-art algorithms. The results are presented in Figure 5. We observed that our approach had competitive latency compared with other methods. The overall latency was less than 1 second. The deep learning based techniques in this work do not explicitly lead to extra latency. One of the main reasons may lie in that the reinforced selective attention has filtered out unnecessary information. To be more specific, the classification latency of the proposed framework was about 0.7∼0.8 seconds, which mainly resulted from the classifying procedure and convolutional mapping. The latency caused by the classifier was around 0.7 seconds. The convolutional mapping only took 0.05 sec on testing although it took more than ten minutes on training.

# E. Reward Model Demonstration

We briefly report the empirical demonstration of the proposed exponential reward model (Section III-B). We compared the proposed reward model in Eq. 5 with the traditional reward $\boldsymbol { r } _ { t } = e ^ { a c c }$ over three benchmark datasets (eegmmidb, EEG-S, and TUH). The experiment results show that the novel reward model achieved higher accuracy (0.9632, 0.9984, and 0.9975) than the traditional model (0.9231, 0.9901, and 0.9762).

# V. DISCUSSIONS

In this paper, we propose a robust, universal, adaptive classification framework to deal with cognitive EEG signals effectively and efficiently. However, there are several remaining challenges.

First, the single EEG sample-based classification can only reflect the instantaneous intention of the subject instead of a long-term stable intention. One possible modification method is post-processing like voting. For instance, we can classify 100 EEG samples and count the mode of the 100 outcomes as the final classification result.

In addition, the reinforcement learning policy only works well in the environment in which the model is trained, meaning the dimension index should be consistent in the training and testing stages. Various policies should be trained according to different sensor combinations. Also, the replicate and shuffle process cannot always provide the best spatial dependency. Therefore, when the classification accuracy is not satisfied, repeating the replicate and shuffle procedure help to enhance the additional performance.

# VI. CONCLUSION

This paper proposes a generic and effective framework for raw EEG signal classification to support the development of BCI applications. The framework works directly on raw EEG data without requiring any preprocessing or feature engineering. Besides, it can automatically select distinguishable feature dimensions for different EEG data, thus achieving high usability. We conduct extensive experiments on three well-known public datasets and one local dataset. The experimental results demonstrate that our approach not only outperforms several state-of-the-art baselines by a large margin but also shows low latency and high resilience in coping with multiple EEG signal channels and incomplete EEG signals. Our approach applies to wider application scenarios such as intention recognition, person identification, and neurological diagnosis.

# VII. ACKNOWLEDGMENTS

This research was partially supported by grant ONRG NICOP N62909-19-1-2009.

# REFERENCES

[1] X. Zhang, L. Yao, X. Wang, J. Monaghan, D. Mcalpine, and Y. Zhang, “A survey on deep learning based brain computer interface: Recent advances and new frontiers,” arXiv preprint arXiv:1905.04149, 2019.   
[2] H. Adeli, S. Ghosh-Dastidar, and N. Dadmehr, “A wavelet-chaos methodology for analysis of eegs and eeg subbands to detect seizure and epilepsy,” IEEE Transactions on Biomedical Engineering, vol. 54, no. 2, pp. 205–211, 2007.   
[3] D. Zhang, L. Yao, X. Zhang, S. Wang, W. Chen, and R. Boots, “Eegbased intention recognition from spatio-temporal representations via cascade and parallel convolutional recurrent neural networks,” in AAAI, 2018.   
[4] A. Vallabhaneni, T. Wang, and B. He, “Brain computer interface,” in Neural engineering. Springer, 2005, pp. 85–121.   
[5] X. Zhang, L. Yao, Q. Z. Sheng, S. S. Kanhere, T. Gu, and D. Zhang, “Converting your thoughts to texts: Enabling brain typing via deep feature learning of eeg signals,” 2018.   
[6] X. Zhang, L. Yao, C. Huang, Q. Z. Sheng, and X. Wang, “Intent recognition in smart living through deep recurrent neural networks,” in ICONIP. Springer, 2017, pp. 748–758.   
[7] C. V. Russoniello, K. OBrien, and J. M. Parks, “The effectiveness of casual video games in improving mood and decreasing stress,” Journal of CyberTherapy & Rehabilitation, vol. 2, no. 1, pp. 53–66, 2009.   
[8] V. Schetinin, L. Jakaite, N. Nyah, D. Novakovic, and W. Krzanowski, “Feature extraction with gmdh-type neural networks for eeg-based person identification,” IJNS, p. 1750064, 2017.   
[9] X. Zhang, L. Yao, S. S. Kanhere, Y. Liu, T. Gu, and K. Chen, “Mindid: Person identification from brain waves through attention-based recurrent neural network,” ACM IMWUT, vol. 2, no. 3, p. 149, 2018.   
[10] V. Veeriah, R. Durvasula, and G.-J. Qi, “Deep learning architecture with dynamically programmed layers for brain connectome prediction,” in SIGKDD. ACM, 2015, pp. 1205–1214.   
[11] E. Acar, C. A. Bingol, H. Bingol, R. Bro, and B. Yener, “Seizure recognition on epilepsy feature tensor,” in EMBS. IEEE, 2007, pp. 4273–4276.   
[12] M. Fraschini, A. Hillebrand, M. Demuru, L. Didaci, and G. L. Marcialis, “An eeg-based biometric system using eigenvector centrality in resting state brain networks,” IEEE Signal Processing Letters, vol. 22, no. 6, pp. 666–670, 2015.   
[13] X. Zhang, L. Yao, C. Huang, S. Wang, M. Tan, G. Long, and C. Wang, “Multi-modality sensor data classification with selective attention,” in IJCAI-18, 2018, pp. 3111–3117.   
[14] P. Cavanagh et al., “Attention-based motion perception,” Science, vol. 257, no. 5076, pp. 1563–1565, 1992.   
[15] J. K. Chorowski, D. Bahdanau, D. Serdyuk, K. Cho, and Y. Bengio, “Attention-based models for speech recognition,” in NeurIPS, 2015, pp. 577–585.   
[16] V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. Riedmiller, A. K. Fidjeland, G. Ostrovski et al., “Human-level control through deep reinforcement learning,” Nature, vol. 518, no. 7540, p. 529, 2015.   
[17] Z. Wang, T. Schaul, M. Hessel, H. Van Hasselt, M. Lanctot, and N. De Freitas, “Dueling network architectures for deep reinforcement learning,” vol. 48, 2016, pp. 1995–2003.

[18] M. Tokic, “Adaptive ε-greedy exploration in reinforcement learning based on value differences,” in Annual Conference on Artificial Intelligence. Springer, 2010, pp. 203–210.   
[19] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” in NeurIPS, 2012, pp. 1097– 1105.   
[20] M. M. or Rashid and M. Ahmad, “Classification of motor imagery hands movement using levenberg-marquardt algorithm based on statistical features of eeg signal,” in ICEEICT. IEEE, 2016, pp. 1–6.   
[21] X. Ma, S. Qiu, C. Du, J. Xing, and H. He, “Improving eeg-based motor imagery classification via spatial and temporal recurrent neural networks,” in EMBC. IEEE, 2018, pp. 1903–1906.   
[22] M. H. Alomari, A. AbuBaker, A. Turani, A. M. Baniyounes, and A. Manasreh, “Eeg mouse: A machine learning-based brain computer interface,” IJACSA, vol. 5, no. 4, pp. 193–198, 2014.   
[23] J. Sita and G. Nair, “Feature extraction and classification of eeg signals for mapping motor area of the brain,” in ICCC. IEEE, 2013, pp. 463– 468.   
[24] M. H. Alomari, A. M. Baniyounes, and E. A. Awada, “Eeg-based classification of imagined fists movements using machine learning and wavelet transform analysis,” International Journal of Advancements in Electronics and Electrical Engineering, vol. 3, no. 3, pp. 83–87, 2014.   
[25] H. V. Shenoy, A. Vinod, and C. Guan, “Shrinkage estimator based regularization for eeg motor imagery classification,” in ICICS. IEEE, 2015.   
[26] P. Szczuko, “Real and imaginary motion classification based on rough set analysis of eeg signals for multimedia applications,” Multimedia Tools and Applications, vol. 76, no. 24, pp. 25 697–25 711, 2017.   
[27] C. A. Stefano Filho, R. Attux, and G. Castellano, “Eeg sensorimotor rhythms variation and functional connectivity measures during motor imagery: linear relations and classification approaches,” PeerJ, vol. 5, p. e3983, 2017.   
[28] O. R. Pinheiro, L. R. Alves, M. Romero, and J. R. de Souza, “Wheelchair simulator game for training people with severe disabilities,” in TISHW. IEEE, 2016.   
[29] Y. Kim, J. Ryu, K. K. Kim, C. C. Took, D. P. Mandic, and C. Park, “Motor imagery classification using mu and beta rhythms of eeg with strong uncorrelating transform based complex common spatial patterns,” Computational intelligence and neuroscience, vol. 2016, pp. 1–14, 2016.   
[30] L. Ma, J. W. Minett, T. Blu, and W. S. Wang, “Resting state eegbased biometrics for individual identification using convolutional neural networks,” in EMBC. IEEE, 2015, pp. 2848–2851.   
[31] S. Yang and F. Deravi, “Novel hht-based features for biometric identification using eeg signals,” in ICPR. IEEE, 2014, pp. 1922–1927.   
[32] D. Rodrigues, G. F. Silva, J. P. Papa, A. N. Marana, and X.-S. Yang, “Eeg-based person identification through binary flower pollination algorithm,” Expert Systems with Applications, vol. 62, pp. 81–90, 2016.   
[33] K. P. Thomas and A. P. Vinod, “Biometric identification of persons using sample entropy features of eeg during rest state,” in SMC. IEEE, 2016, pp. 003 487–003 492.   
[34] S. Ziyabari, V. Shah, M. Golmohammadi, I. Obeid, and J. Picone, “Objective evaluation metrics for automatic classification of eeg events,” arXiv preprint arXiv:1712.10107, 2017.   
[35] A. Harati, M. Golmohammadi, S. Lopez, I. Obeid, and J. Picone, “Improved eeg event classification using differential energy,” in SPMB. IEEE, 2015, pp. 1–4.   
[36] Y. Zhang, S. Yang, Y. Liu, Y. Zhang, B. Han, and F. Zhou, “Integration of 24 feature types to accurately detect and predict seizures using scalp eeg signals,” Sensors (Basel, Switzerland), vol. 18, no. 5, 2018.   
[37] T. R. Goodwin and S. M. Harabagiu, “Deep learning from eeg reports for inferring underspecified information,” AMIA Summits on Translational Science Proceedings, vol. 2017, pp. 112–121, 2017.   
[38] M. Golmohammadi, A. H. H. N. Torbati, S. L. de Diego, I. Obeid, and J. Picone, “Automatic analysis of eegs using big data and hybrid deep learning architectures,” arXiv preprint arXiv:1712.09771, 2017.   
[39] X. Zhang, L. Yao, and F. Yuan, “Adversarial variational embedding for robust semi-supervised learning,” in SIGKDD, 2019, pp. 139–147.   
[40] M. Golmohammadi, V. Shah, S. Lopez, S. Ziyabari, S. Yang, J. Camaratta, I. Obeid, and J. Picone, “The tuh eeg seizure corpus,” in ACNS Annual Meeting, 2017, p. 1.