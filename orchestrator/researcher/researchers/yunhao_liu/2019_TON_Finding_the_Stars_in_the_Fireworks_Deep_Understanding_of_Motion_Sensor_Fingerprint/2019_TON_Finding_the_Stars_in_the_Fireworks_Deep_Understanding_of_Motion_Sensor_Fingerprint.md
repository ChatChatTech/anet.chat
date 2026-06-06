# Finding the Stars in the Fireworks: Deep Understanding of Motion Sensor Fingerprint

Xiang-Yang Li , Fellow, IEEE, Huiqi Liu , Lan Zhang Member, IEEE, Zhenan Wu, Yaochen Xie, Ge Chen, Chunxiao Wan, and Zhongwei Liang

Abstract— With the proliferation of mobile devices and various sensors (e.g., GPS, magnetometer, accelerometers, gyroscopes) equipped, richer services, e.g. location based services, are provided to users. A series of methods have been proposed to protect the users’ privacy, especially the trajectory privacy. Hardware fingerprinting has been demonstrated to be a surprising and effective source for identifying/authenticating devices. In this work, we show that a few data samples collected from the motion sensors are enough to uniquely identify the source mobile device, i.e., the raw motion sensor data serves as a fingerprint of the mobile device. Specifically, we first analytically understand the fingerprinting capacity using features extracted from hardware data. To capture the essential device feature automatically, we design a multi-LSTM neural network to fingerprint mobile device sensor in real-life uses, instead of using handcrafted features by existing work. Using data collected over 6 months, for arbitrary user movements, our fingerprinting model achieves 93% F-score given one second data, while the state-of-the-art work achieves 79% F-score. Given ten seconds randomly sampled data, our model can achieve 98.8% accuracy. We also propose a novel generative model to modify the original sensor data and yield anonymized data with little fingerprint information while retain good data utility.

Index Terms— Motion sensor, device fingerprint, privacy.

# I. INTRODUCTION

O PROVIDE richer services, modern mobile devices are equipped with various sensors, e.g., GPS, magnetometer, accelerometers, gyroscopes. Sensor data is continuously generated and collected by service providers to support various functions like recording running traces, step count and calorie burning [1], as well as a variety of other novel uses, e.g.,

Manuscript received December 25, 2017; revised June 12, 2019; accepted July 30, 2019; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor T. Date of publication August 22, 2019; date of current version October 15, 2019. This work was supported in part by the National Key R&D Program of China under Grant 2017YFB1003003, in part by the China National Funds for Distinguished Young Scientists under Grant 61625205, in part by the NSFC under Grant 61822209, Grant 6193000068, Grant 61472281, Grant 61520106007, and Grant 61751211, in part by the Key Research Program of Frontier Sciences, CAS, under Grant QYZDY-SSW-JSC002, Grant NSF ECCS-1247944, and Grant NSF CNS 1526638, and in part by the Fundamental Research Funds for the Central Universities. (Corresponding author: Lan Zhang.)

X.-Y. Li, H. Liu, L. Zhang, Z. Wu, and Y. Xie are with the School of Computer Science and Technology, University of Science and Technology of China, Hefei 230022, China (e-mail: xiangyangli@ustc.edu.cn; liuhuiqi@ mail.ustc.edu.cn; zhanglan03@gmail.com; ariadust@mail.ustc.edu.cn; xieyc95@mail.ustc.edu.cn).

G. Chen, C. Wan, and Z. Liang are with Tencent, Shanghai 200233, China (e-mail: gechen@tencent.com; lincwan@tencent.com; chaliang@ tencent.com).

Digital Object Identifier 10.1109/TNET.2019.2933269

human activities understanding and searching [2], pedestrian tracking [3], eye gaze tracking [4], [5] and password input by gesture and context detection [6]. On the customer information market [7], [8], sensor data may also be put on the shelves for further research. Despite the aforementioned attractive features, rich personal information contained in the sensor data could also pose a serious privacy threat. Traditional anonymization methods, e.g., hiding user ID, querying location with encryption [9], automatically erasing privacy sensitive photos [10], privacy-preserving image search with fine-grained access control [11], perturbing voiceprint [12], [13], cannot effectively mitigate the risk, because each sensor has its unique physical characteristics, which can be captured as a fingerprint in its produced data.

Fingerprinting sensors also provides a more robust way for device identification, which can better resist device impersonation and data tampering. On the other hand, a well designed anonymization method is also required to provide better privacy protection to networking devices.

Some existing efforts have explored various methods to fingerprint different kinds of sensors for tracking users across applications [14]–[16]. These methods often extract dozens of pre-defined features (e.g., max value, min value, mean, deviation and spectral centroid) which are characteristics of sensor data being observed, and use various supervised classifiers (e.g., SVM, Naive-Bayes, and Multiclass Decision Tree) to fingerprint devices. Some countermeasures are also proposed, such as calibration and obfuscation, to mitigate fingerprinting.

Those methods, however, have limitations in practical scenarios, and few of them achieve a systematic understanding of mobile sensor fingerprint, which makes it quite challenging to answer the following key questions.

First, what is the capacity of device fingerprint? Manufacturing imperfection makes each sensor have specific physical characteristics. In order to leverage these characteristics as fingerprint, we need to find out if the capacity of the characteristic space is sufficient to distinguish a substantially large number of devices. This cannot be answered by existing experiment results based on only dozens of devices.

Second, which features and models are better to achieve robust and efficient fingerprinting? How do the human activities affect device fingerprinting? Handcrafted features used by existing method cannot capture the essential characteristics of device fingerprint. Moreover, many of the pre-defined features, e.g., mean deviation, and spectral entropy, are highly sensitive to noises like human activity, which deteriorates the robustness of fingerprint in complex real-life scenarios. For example, using 70 features, the identification F-score of [14] is about 93% when the phone has only lightly movement, however the

F-score reduces to 78% when the phone moves in a moderate speed. Besides, it takes us about 5 seconds to extract those 70 features from 1 second data. To achieve robust and efficient fingerprinting, we need to extract intrinsic features of sensors when they are swallowed by user’s substantial movements.

Third, how to retain utility while anonymizing sensor data? Existing countermeasures include calibration and obfuscation. Calibration can eliminate some of the errors that result from manufacturing imperfections, but many sensors, like gyroscope, are hard to calibrate manually or require specialized equipment. Obfuscation adds noises (e.g., uniform noise and Laplace noise) to the sensor readings, which reduces the fingerprinting accuracy, but also sacrifices some data utility, e.g., resulting in incorrect step count. It is challenging to design a general countermeasure to achieve a good anonymization results, as well as tradeoff between anonymization and utility for different types of sensor data.

Methodology and Contributions: To answer aforementioned challenging questions, we deeply investigate the mobile sensor fingerprint and make the following contributions.

Theoretical fingerprint capacity model: We are the first to propose a theoretical model to quantify the capacity of device fingerprint with multiple dimension features, and analyze/verify this model with a large collection of mobile device data. Our model assumes that the collection of devices’ fingerprinting features follow certain distributions such as normal distribution, or uniform random distribution. We then derive the theoretical fingerprinting capacity by studying the impact of the number of features, the partition granularity of the feature space, and the number of devices to be fingerprinted.

Deep neural network based fingerprinting model: To capture the essential fingerprinting feature automatically, we design a multi-LSTM neural network to fingerprint mobile device sensors in real-life uses. This is a non-trivial task due to two reasons. First, despite the great success deep learning has achieved in computer vision, speech recognition and natural language processing, little work has applied deep learning to fingerprint sensors. It’s a challenge to design a proper network structure to achieve robust fingerprinting. Second, the sensor data is sampled unevenly and extremely noisy due to arbitrary user activities. We need to carefully pre-process the raw data and pack it properly as input of the neural network. Comparing to previous work, our proposed multi-LSTM model achieves better accuracy and much stronger robustness.

Generative model based anonymizing method: We propose a novel generative model to anonymize sensor data while retain good data utility. Our method can be applied to various sensor data for real-time data release.

With users’ permission, we collect motion data from 117 mobile phones, with 13 different brands devices, over more than 6 months period, and then conduct extensive evaluations. The experiments show consistent results with our capacity model. For arbitrary user movements, given only 1 second data, our fingerprinting model achieves 93% F-score, while the state-of-the-art work achieves 79% F-score.

With only accelerometer, our model can still achieve 90.26% accuracy.

If there are only 20 devices, they can be fingerprinted with 99.2% accuracy. For different devices (13 brands, 65 models in our experiment) of the same brand/model, the fingerprinting accuracy is still above 93.5%. For different devices (12 devices in our experiment) used by the same person, the accuracy reduces to 89%, due to the influence of human behavior fingerprints. Using 20s data, the top-1 accuracy is 99% and top-2 accuracy is 99.94% by voting.

Using our model, we can extract fingerprint features in an unsupervised manner.

It only takes 0.04ms to fingerprint 1 second data. Our anonymizing model can reduce the fingerprinting accuracy to 5% while retaining good utility with only 0.9 ms delay.

The rest of this paper is organized as follows. We review related work in Section II, and describe our methodology in Section III. In Section IV, we theoretically analyze the capacity of device fingerprint. Section V presents our neural network model for robust fingerprinting, and Section VI presents our generative model based anonymization method. Section VII reports experimental results, and Section VIII concludes the work with future work.

# II. BACKGROUND AND RELATED WORK

Existing efforts mainly investigated two categories of device fingerprints, software fingerprints and hardware fingerprints. Hardware fingerprints are more persistent but more challenging to characterize.

# A. Software Fingerprinting

Researchers have characterized different installed softwares as fingerprints to distinguish different devices, for example, the installed device drivers [17], the performance benchmarks of JavaScript engines [18], the characteristics of 802.11 traffic [19], and the timing analysis of 802.11 probe request frames [20]. A common set of approaches collect information via browsers to generate a device’s software fingerprint, such as the HTML5 canvas elements [21] and user browsing history [22], [23]. Due to the dynamic nature of installed softwares, the software-based fingerprints usually change with time.

# B. Hardware Fingerprinting

Different hardware components of mobile devices have been investigated to generate fingerprints. Wireless transmitters can be fingerprinted by radio frequency (RF) [24]–[26].

Network devices have distinguishing and stable clock skews [27] [28], which can be used for fingerprinting [29]. The source network interface card (NIC) can be identified using minute imperfections in transmitter hardware [30] [31].

Sensor Fingerprinting: Hardware characteristics can be used to identify devices, and then users. These characteristics are caused by manufacturing differences or manufacturing imperfections. In theory, most sensors have some sort of measurable bias. For example, accelerometer, gyroscope, magnetometer and ambient light sensors generate data with linear bias, and GPS sensor has clock skew imperfection.

Stisen et al. [32] investigate mobile sensing heterogeneities for HAR (human activity recognition).

Zhou et al. [33] extract features from audio pieces and conducted fingerprinting by feature matching. Das et al. [34] extract rich acoustic features and applied traditional classification algorithms to fingerprint. Accessing to the microphones and speakers require obvious user permission, while motion sensors (e.g., accelerometer and gyroscope) can be accessed without requiring any user permission, which raises potential threats to privacy. Dey et al. [16] use feature extraction and Bagged Decision Trees to generate accelerometer fingerprint.

Bojinov et al. [15] have analyzed common mobile device sensors along with their imperfections.

Das et al. [14] use 70 temporal and spectral features of gyroscopes and accelerometers to track mobile users through web browsers.

They also propose calibration and obfuscation as two straightforward defenses.

However, the calibration requires specialized equipments, while obfuscation reduces the utility of the motion sensors.

As a summary, existing works have tried around 100 handcrafted features working along with different classifiers to fingerprint sensors, and evaluated the accuracy with dozens of devices.

# III. METHODOLOGY AND PROBLEM SCOPE

In this work, towards a systematic deep understanding of mobile sensor fingerprint, we thoroughly investigate the following challenging issues.

Capacity of device fingerprint. To theoretically analyze the fingerprint capacity, we propose a multidimensional Balls-into-Bins model, taking the devices as balls and the partitions of the multidimensional hardware feature space as bins. Leveraging the statistic results of our 117 diverse mobile devices dataset, our theoretical model shows the fingerprint capacity as the devices number and sensor category grow. (See Section IV.)   
• Robust fingerprinting deep neural network. To achieve robust device fingerprint in practical uses, where the subtle hardware characteristics are swallowed by environment noises and arbitrary user activities, we design a series of deep neural networks to automatically extract essential fingerprinting features which outperforms existing handcrafted feature based methods. Moreover, we reveal several insights about influence factors of device fingerprinting. (See Section V and Section VII.)   
• Defense model retaining utility. To anonymize sensor data as well as retain the data utility, we propose a novel generative model consisting of an encoder and a decoder, which makes minimal modifications to the sensor data to remove fingerprint information in a real-time manner. (See Section VI.)

Our theoretical capacity model can be adopted for analyzing fingerprints of diverse mobile devices. The proposed fingerprinting and anonymizing models can be applied for various sensor data in time series form. In our data-driven analysis (in Section V and Section VII), we take motion sensors (namely, accelerator and gyroscope) as examples. Because motion sensors can be accessed without requiring any obvious user permission, which raise high privacy threats as well as great challenges for fingerprinting due to the rich user activity information in the sensor data.

Different from the previous work, which places devices on a flat surface (i.e., a static scenario) or holds in hand with slightly movement, we consider more practical scenarios, where users can perform arbitrary activities, e.g., browsing, walking and running.

# IV. UNDERSTANDING CAPACITY OF FINGERPRINT

In this section, we propose a theoretical capacity model to understand the capability of hardware fingerprinting and conduct rigorous analysis considering multidimensional features.

# A. Brief Introduction to Onboard Sensors

Substantial efforts have been devoted to modeling MEMS-based motion sensor noise. For the most common noises, Gabrielson [35] models the mechanical thermal noise as function of absolute temperature and the damping coefficient. Djuric [36] derives more complex noise models combining mechanical thermal noise with electrical noise sources, including thermal noise, shot noise, and flicker noise.

These noises are the characteristics (like damping coefficient) of the motion sensors. They are slightly different from each other due to the heterogeneities of the manufacturing procedure, thus, forming fingerprints for sensors.

# B. Capacity Model of Fingerprinting

We propose a multidimensional Balls-into-Bins model to analyze the capacity of device fingerprint. Here we take m devices as balls and n partitions of the hardware feature space as bins, and throw m balls into n bins. Intuitively, when a ball falls into a bin, it means this device possesses a specific feature. When more than one balls fall into the same bin, a collision indicates these devices have the same feature, that is they cannot be distinguished by this type of feature.

We are interested in four factors affecting the capacity of fingerprint, namely, m, n, the dimension of feature space and the distribution of fingerprinting features. For the convenience of analysis, we take two typical distributions, uniform distribution and normal distribution as examples of feature distributions. Uniform distribution is a simple and basic distribution, and normal distribution is often used to represent real-valued random variables whose distributions are unknown. In Section VII-C, we analyze the real feature distributions of motions sensors using data from 117 mobile devices. Though those real-world feature distributions cannot be expressed by formulas, we can still estimate the capacity in the similar way as shown in the Appendix. The estimated capacity is consistent with the experimental result.

1) One-Dimension Feature Space: Let’s start with onedimension feature space. The feature of each device’s sensor is independent of that of other devices’ sensors. Sensor features are continuously distributed, and we discretize the feature space into n partitions.

Uniformly distributed feature: First, we assume sensor features follow a uniform distribution.

In this case, the model is that each ball is independently thrown into a random bin following the uniform distribution. So the probability that a ball falls into any bin is 1/n.

Let $C o l _ { i } ^ { j }$ denote the event that there exist collisions for the balls whose indices are within the range [i, j ]. E(C) denotes the expectation number of collisions. Note that we count collisions over distinct pairs, that is, if three balls fall into one bin, three collisions are counted. The probability that there exist collisions is (proof in Appendix A)

$$
P r (C o l _ {1} ^ {m}) = 1 - P r (\neg C o l _ {1} ^ {m}) = 1 - \frac {(n - 1) !}{n ^ {m - 1} (n - m) !}.
$$

The expected number of collisions is (proof in Appendix B) $\begin{array} { r } { \mathbb { E } ( C ) = \frac { \dot { m } ( m - 1 ) } { 2 n } } \end{array}$ 2n

We now analyze how the device number m and feature space size n change the collision probability $P r ( C o l _ { 1 } ^ { m } )$ and collision number E(C). Obviously, increasing device number m brings larger collision probability (Fig. 1a) and more collision devices (Fig. 2a), while increasing feature space size n reduces collision probability (Fig. 1b) and collision number (Fig. 2b). Given one-dimension feature space with limited size, e.g., 100 bins, even a small set of devices, e.g., 20 devices, there is a more than 80% collision probability (Fig. 1).

![](images/9e9ad321b707f6e134f8c85ea85c25d7cb820e3dfe4a87ed8b85d941973d1e71.jpg)



(a) Fixed feature space size n.

![](images/4575ea5caff6271452a6360af9d9723031d56cf5ed24ce08142e01914e8d1209.jpg)



(b) Fixed device number m.

Fig. 1. The probability ${ P r } ( C o l _ { 1 } ^ { m } )$ vs device # m and feature space size n when the feature is uniformly distributed.   
![](images/4a9244779622608d9a1263303d0d2dd0bec4011581f57a8088ec84a12e58b8f2.jpg)



(a) Fixed feature space size n.

![](images/dec7b0644ec989347a6820840bcbf9191abc2eb86aa0634f913eb2724aaa5afe.jpg)



(b) Fixed device number m.

Fig. 2. Expected # of collisions E(C) vs device # m and feature space size n when the feature is uniformly distributed.   
![](images/afb347b9fdd0d45f60d61cc46f179a7ef6bebbab7b5094a0226064439b1c01c6.jpg)



(a) The probability $P r ( C o l _ { 1 } ^ { m } )$

![](images/9b32e17039d7a5d6e7274835b1c1e90e90f7acc3e3f8fa5b5eab7abd03fbe4b9.jpg)



(b) The expected collision E(C)   
Fig. 3. The collision probability ${ P r } ( C o l _ { 1 } ^ { m } )$ and the number of expected collision E(C) changes against m and n when the feature is a binomial distribution $B ( n - 1 , \top 2 )$ .

Normally distributed feature: Second, we consider sensor features follow a normal distribution.

To describe the feature distribution over discrete bins, we use a discrete distribution, binomial distribution, to approximate normal distribution.

For m balls and n bins, each time a ball is independently thrown into a bin follow the binomial distribution $B ( n - 1 , p )$ , which means that a ball falls into the x -th bin with probability ${ \binom { n - 1 } { x - 1 } } p ^ { x - 1 } ( 1 - p ) ^ { n - x }$ .

In this case, the probability that there exist collisions is (proof in Appendix A)

$$
Pr(Col_{1}^{m}) = 1 - \sum_{\substack{\{r_{1},r_{2},\dots ,r_{m}\} \\ \subset \{0,1,\dots ,n - 1\}}}\prod_{i = 1}^{m}\binom {n - 1}{r_{i}}p^{r_{i}}(1 - p)^{n - 1 - r_{i}},
$$

where $r _ { i }$ is the index of the bin $( 0 ~ \leq ~ r _ { i } ~ \leq ~ n ~ - ~ 1 )$ which the i-th ball falls into. The expected number of collisions is (proof in Appendix B) $\mathbb { E } ( C ) ~ = ~ \frac { 1 } { 2 } m ( m - 1 )$ $\begin{array} { r } { \sum _ { i = 0 } ^ { n - 1 } \left( { \binom { n - 1 } { i } } p ^ { i } ( 1 - p ) ^ { n - 1 - i } \right) ^ { 2 } } \end{array}$ .

Fig 3a and Fig. 3b plot the collision probability and expected collision number. Similar to the uniform distribution case, larger m and smaller n increase the collision significantly. Differently, in the normal distribution case, the collision happens with a much higher probability, which means it is much more difficult to distinguish devices in this case.

2) Multi-Dimension Feature Space: In practice, multiple features can be utilized to distinguish mobile devices. Now we consider the multi-dimension Balls-into-Bins problem.

![](images/c1f3b6aef7f0d00ea9e8bd828b4b0cddd77c9d21938f2f4fb210b37af6c76f43.jpg)



(a)Uniform distribution, 2D bins

![](images/e93f0c80509826e395a1ed297b77737a8fe330931a67f8cd0d6e901ca2f0f630.jpg)



(b) Uniform distribution, 6D bins

Fig. 4. The probability $P r ( I _ { 1 } ^ { m } )$ versus m, n and k when features are uniformly distributed (here we suppose each dimension has the same number of bins).   
![](images/afc38caf365ccefdbca4084e09d75eabefc3430d281e03d694581dd9eae657b9.jpg)  
(a) Uniform distribution,2D bins

![](images/50cc658f622b47b96a2ac87243b5556615f920cbfb53c8a9ef09778b3a91af05.jpg)

![](images/648cd1bb010353056698254bc412056e8234a093a43981f2ead96b512c05df5c.jpg)



(b) Normal distribution,2D bins   
Fig. 5. The expected number of indistinguishable balls E(I ) versus m, n and k when the feature space is 2-dimension (here we suppose each dimension has the same number of bins).

Here we suppose each dimension is independent to give the upper bound of fingerprint capacity. In practice, different sensors’ noise, e.g, gyroscope and accelerometer, can be considered as independent.1 Two indistinguishable balls must collide in all dimensions, i.e. in the same high-dimensional grid.

Let $I _ { i } ^ { j }$ denote the k-dimension collision event that there exist indistinguishable balls in the k-dimension feature space.

Suppose there are k-dimension bins with bin sizes $\{ n _ { 1 } , n _ { 2 } , \cdots , n _ { k } \}$ .

Uniform distributed feature: In uniform distribution case, the probability that indistinguishable balls exist is (proof in Appendix C)

$$
P r (I _ {i} ^ {m}) = 1 - P r (\neg I _ {i} ^ {m}) = 1 - \binom {n} {m} m! * \left(\frac {1}{\prod_ {i = 1} ^ {k} n _ {i}}\right) ^ {m},
$$

where $\textstyle n = \prod _ { i = 1 } ^ { k } n _ { i }$ . The expected number of indistinguishable balls is (proof in Appendix D) $\begin{array} { r } { \mathbb { E } ( I ) = \frac { m ( m - 1 ) } { 2 \prod _ { i = 1 } ^ { k } n _ { i } } } \end{array}$ .

Fig. 4 plots the probability of k-dimension collision. Compared to the one-dimension case, two independent feature dimensions, e.g., two independent sensors such as accelerometer and gyroscope, significantly reduce the indistinguishable probability.

With limited bin size on each dimension, e.g., 100, given 20 devices, the indistinguishable probability drops to less than 5% (compared to 80% in the one-dimension case). 50 bins on each dimension can reduce the expected collision number of 50 devices to lower than 1 (Fig. 5a).

Normally distributed feature: Similarly, we use binomial distribution $B ( n \mathrm { ~ - ~ } 1 , \dot { p } )$ as the approximation of normal distribution, and the probability for a ball falls into the k-th bin in the i-th dimension is -ni −1x−1  px−1i (1 − pi )ni −x , (ni-1) $\binom { n i - 1 } { x - 1 } p _ { i } ^ { x - 1 } ( 1 - p _ { i } ) ^ { n _ { i } - x }$

where $p _ { i }$ is the binomial distribution parameter for the i-th dimension. So the expected number of indistinguishable balls is (proof in Appendix D) $\mathbb { E } ( I ) ~ = ~ \frac { 1 } { 2 } m ( m ^ { - } - 1 )$ $\begin{array} { r } { \prod _ { i = 1 } ^ { k } \sum _ { j = 0 } ^ { n _ { i } - 1 } \left( { \binom { n _ { i } - 1 } { j } } p _ { i } ^ { j } ( 1 - p _ { i } ) ^ { n _ { i } - 1 - j } \right) ^ { 2 } } \end{array}$ . Fig. 5b plots the expected number of indistinguishable devices for 2-dimension feature space. Compared to the uniform distribution case, the fingerprint capacity decreases, while increasing feature dimensionality still significantly enlarges the capacity.

![](images/d29a561c3af161eae2d1d2a22ce5ced9adb4cbf6884b158e4b09a65408d62b42.jpg)



Fig. 6. Fingerprinting accuracy of of the state-of-the-art method [14] in both static and dynamic scenario.

![](images/6495805bfbcc06ebbf782d00a55ee87a2a26b5e6a97770fcd8fedbb5fe3c10a3.jpg)



Fig. 7. Fingerprinting F-score of the state-of-the-art method [14] in both static and dynamic scenario.

# V. ROBUST DEVICE FINGERPRINTING

In this section, we explore features for robust device fingerprinting. Existing works have proposed dozens of handcrafted features (e.g., max value, min value, mean, deviation and spectral centroid). The state-of-the-art work [14] uses 70 temporal and spectral features of sensor data as device fingerprints.

Most of these features are highly sensitive to large noises like human activities. In practical sensor data, subtle hardware fingerprints are usually swallowed by substantial movement signals, e.g., walking and running. To investigate the impact of activities on fingerprinting, we implement the proposed method in [14], and test the accuracy and efficiency on our data collected from 117 different devices. Our sensor data are collected in both static scenario (97 of 117 devices), where the phone is placed flat on a surface, and highly dynamic scenario (117 devices), where the user holds the phone and performs arbitrary activities such as walking and gaming. It takes us about 5 seconds to extract 70 pre-defined features [14] from 1 second data. As shown in Fig. 6 and Fig. 7, in the static scenario, using a set of handcrafted features can achieve 94% accuracy and 93% F-score for 97 devices given 1 second data.2 When it comes to the highly dynamic scenario, the accuracy and F-score reduce significantly to 79% for 117 devices. And the accuracy and F-score decline significantly as the device number increases.

# A. Neural Network Based Fingerprinting

Our results reveal that, it is quite challenging to achieve robust device fingerprinting using real-life sensor data. In order to capture the inherent hardware features automatically, we propose to use deep neural network for fingerprints extraction. Facing various challenges, we explore a variety of deep

2As reported in [14], it can achieve 96% F-score given 5 seconds data of 96 devices. With our dataset, [14] achieves 97.6% F-score given 5 seconds data for 97 devices, which is consistent with the reported result.

![](images/c02b384b27f15e5ca419f533941ee70fb2a67080750f227bb2c6422cac3cb934.jpg)



Fig. 8. Fingerprinting accuracy of different models for different input data lengths in dynamic scenario.

![](images/dabaa51223bb9acce755d45d60a9188e5406082c98f9556f90c161e3483d8956.jpg)



Fig. 9. Fingerprinting F-score of different models for different input data lengths in dynamic scenario.

![](images/d2452b70c454326db4b6b419aa72209aeb164e59dca1c5d16783f371bd876627.jpg)



Fig. 10. The network structure of LSTM fingerprinting model.

neural networks and design a Long Short Term Memory network (LSTM) model which is suitable for sensor feature extraction. Raw data are carefully processed before being fed into the model. Our proposed model achieves high accuracy in highly dynamic scenarios.

1) Multi-LSTM Fingerprinting Model: LSTM network, as a variant of RNN introduced by Hochreiter and Schmidhuber [37], is capable of learning long-term dependencies like the fingerprinting information in sensor data. We design a Multi-LSTM structure as shown in Fig. 10. More specifically, the input are w×k sequences, where w is the data length (e.g., w = 100 when input 1-second data with 100Hz sample rate), k is the channel number (e.g., k = 3 for data from three axes of the accelerometer). w is correlated to the fingerprinting delay in a realtime system. k is the dimension number in our theoretical capacity model in Section IV, if k input channels are independent. Through one hidden layer, data are fed into a multi-LSTM structure in order to extract persistent features. Then it outputs a size h vector as the input of the second hidden layer, which is then connected with the soft-max layer.

In general LSTM works better than CNN (Conventional Neural Network) in treating sequential data. Some previous work also used a CNN model to learn good feature representations for sequential data like audio data [38]. As a comparison, we also design and build a CNN model taking raw sensor data as input, and another CNN model taking the data processed by Short-Time Fourier Transform (STFT) as input. Fig. 8 reveals that the CNN-raw model and CNN-STFT model we used here are sensitive to the length of input data. More specifically, when the input length is more than 5 seconds, these two models show poor performances with less than 80% fingerprinting accuracy. Based on our extensive evaluation, we find that the multi-LSTM model significantly outperforms the two CNN models.

Unsupervised fingerprinting: Based on our LSTM model, unsupervised fingerprinting can also be conducted by treating the penultimate layer (the size h vector) of our network as a device’s fingerprint feature. Given unlabelled data from K devices, we can extract the fingerprint feature of each piece of data, and apply unsupervised learning, e.g., k-means clustering, on all data pieces to cluster data from the same device together. Furthermore, given only a few labelled data for each device, we can identify a large-scale of unlabelled data, which enables more stronger and more practical unsupervised attack without requiring many labelled training data.

2) Data Pre-Processing: For each motion sensor, i.e., accelerometer or gyroscope, three data sequences are simultaneously generated with timestamps by three axes. So, in our experiments, we obtain 6 data sequences from two motion sensors. Each sequence can be a channel of the neural network input. However, they are generated with unstable time intervals, which depends on the schedule of the mobile operating system according to the real-time system load. Hence, we conduct piece-wise cubic Hermite interpolation to obtain equally spaced data sequences as the inputs of neural networks. We also divide the continuous sensor data into small sequences of the same length w.   
3) Evaluation Metric and Model Comparison: To evaluate the effectiveness of fingerprinting models, we use two metrics: accuracy and F-score. As a multi-class classification task, the model accuracy is defined as the proportion of correction predictions, F-score gives a tradeoff between precision and recall, which is defined as $\begin{array} { r } { \mathrm { F - s c o r e } = \frac { 2 * P r e s i c i o n * R e c a l l } { P r e c i s o n + R e c a l l } } \end{array}$   
Using our large dataset collected from 117 diverse devices in real-life scenarios, we conduct comprehensive evaluation on our three neural networks as well as the state-of-theart methods [14]. We report detailed evaluation results and analysis in Section VII. As a summary, Fig. 9 shows the fingerprinting accuracy of our model compared with models in [14] for highly dynamic scenarios (i.e., sensor data of arbitrary user activities) given different input data lengths w. It reveals that handcraft features based models (Random Forest and SVM) can only achieve 74% ∼ 87% F-score due to the large noise caused by human activities. Our multi-LSTM approach achieves 93% F-score with only 1 second sensor data.   
4) Majority Voting Strategy: To further increase the accuracy, we apply the Majority Voting Strategy: suppose a fingerprinting model for t-second input data has been trained to achieve an accuracy p. Then theoretically, given a piece of s × t-second data, where s ∈ N and s > 1, by majority voting we can achieve the following accuracy:

$$
A c c u r a c y (s) = \left\{ \begin{array}{l} \sum_ {i = m} ^ {s} C _ {s} ^ {i} p ^ {i} (1 - p) ^ {s - i} - \frac {1}{2} C _ {s} ^ {m} p ^ {m} (1 - p) ^ {s - m}, \\ \quad \text {if s is even and m = s / 2} \\ \sum_ {i = m + 1} ^ {s} C _ {s} ^ {i} p ^ {i} (1 - p) ^ {s - i}, \\ \quad \text {if s is odd and m = (s - 1) / 2} \end{array} \right.
$$

Using our dataset we conduct Monte Carlo simulation to simulate the performance of majority voting strategy on real data.3 Fig. 11 shows the theoretical and real data based Monte Carlo simulation results. With majority voting, given 10 seconds data, the theoretical accuracy can achieve 99.9%, and the simulation results can exceed 99%. Then we evaluate the voting strategy for two different real-life scenarios: (1)continuous voting: an attacker obtains a piece of continuous data of a device and divided them into small pieces for voting; (2)uncontinuous voting: an attacker obtains pieces of uncontinuous data collected at different time, and uses them for voting. The uncontinuous voting attack can compromise privacy-preserving methods which release scattered data pieces to protect user privacy. As shown in Fig. 11 and Fig. 12, the continuous voting can achieve 96% top-1 accuracy and 97.4% top-2 accuracy given 10 seconds data, while the uncontinuous voting can achieve 98.8% top-1 accuracy and 99.7% top-2 accuracy given 10 pieces of 1 second data.

![](images/2116d1ad5e5eca8fd15f4ad0cc1c5e2666554dd159b3863fbde930a52f91a222.jpg)



Fig. 11. Fingerprinting accuracy with Majority Voting.

![](images/a5709ac61092cbc7c8f195c56af923d031f797413f91631af109fb5ee459a496.jpg)



Fig. 12. Fingerprinting accuracy with Majority Voting.

# VI. ANONYMIZING SENSOR DATA

Facing fingerprinting attack with high accuracy, there is an urgent demand for effective countermeasures to protect user privacy. Specifically, the attack can be modeled by that given a set of devices $\mathbb { D } = \{ d _ { 1 } , d _ { 2 } , . . . , d _ { n } \}$ and their sensor data, for a new piece of sensor data $s ^ { \prime }$ generated by one of the device d ∈ D, the attacker utilizes a fingerprinting method to identify the exact device which generated $\mathit { \Pi } _ { S ^ { ' } , }$ To anonymize sensor data, we propose a novel generative model, which eliminates the fingerprints effectively while minimizing data utility loss. The goal of our anonymization model is (1) defending all existing fingerprinting methods proposed by both previous works as well as ours, i.e., SVM and random forest models based on handcrafted features and our end-to-end LSTM fingerprinting model; (2) maximizing the remaining utility of sensor data.

# A. Anonymization Model

The model is composed of a generator and a discriminator. The basic idea is to train a generator, which takes the original

3First, we use 1-second pieces of training data to train our multi-LSTM model. Then, during each step in the simulation, we randomly select a label category of test data and randomly choose a piece of s-second data from this category. Next, we split the data into s 1-second pieces, and use the trained model to predict the label of each piece. Using the s labels for majority voting, we obtain the final predicted label for this s-second data.

![](images/6be97f2c3f95c09ca4c5de526841e9887d9466996483e4d6a99d5c4b2897cc44.jpg)



Fig. 13. The network structure of data anonymization model.

data as input and outputs de-fingerprinted data to fool a well-trained discriminator, e.g., our multi-LSTM fingerprinting model. That is, the discriminator takes the de-fingerprinted data as input and outputs incorrect labels. The discriminator can be replaced by some more advanced fingerprinting model in the future. The goal is to maximize the randomness of the discriminator’s output labels with minimal data modification. In this way, our model anonymizes the input data while retains the data utility. Our model structure is demonstrated in Fig. 13. The generator is an auto-encoder like structure containing two convolutional layers. For the discriminator, we use our multi-LSTM model since it outperforms other fingerprinting models.

When training the generator, instead of using correct labels, we match each piece of sensor data with a random label to force the generator to modify the original data to anonymized data. Simultaneously, the generator also tries to minimize differences between anonymized data and original data. We define the loss function as lo $s _ { S _ { g } } ~ = ~ k$ ∗ $c r o s s \_ e n t r o p y ( y , y ^ { \prime } ) + m a x \{ 0 , \| x - x ^ { \prime } \| _ { L 2 } - \epsilon \} , ^ { 4 }$ where y denotes the random labels we match to the data, y denotes the outputs of discriminator during training, x and ${ \bf { \bar { \Phi } } } _ { X ^ { ' } }$ denote the original data and de-fingerprinted data, - denotes an acceptable error of the generator, and k is the weight parameter. - and k control the trade-off between the anonymization effect and data utility. By reducing the loss during training, we can control similarity level between original and anonymized data, as well as the anonymization level. Our model takes less than 1 ms to anonymize 1 second data. So it can serve as a new feature in the future mobile operating systems.

# B. Evaluation Metrics

We use following metrics to evaluate anonymization methods.

Anonymization Effect: It is hard to tell whether a countermeasure can defend against all fingerprinting methods. A fair metric is to use the state-of-the-art fingerprinting methods [14] and our multi-LSTM based fingerprinting as attack models, and measure the fingerprinting accuracy of these models on the anonymized data. The lower the accuracy, the better the anonymization effect.

Utility: It is essential that the anonymized data should not scarify the data utility. We measure data utility from two perspectives: (1) Modification distance: We use the $L _ { 2 }$ distance between the original data sequence and anonymized data sequence to measure the extent of the modification, which should be as small as possible. (2) Data usage: We use

$^ 4 \mathrm { I t }$ is also reasonable to design the loss function as $l o s s _ { g } ^ { \prime } = - k *$ $c r o s s \_ e n t r o p y ( y _ { t r u e } , y ^ { \prime } ) + m a x \{ 0 , \| x - x ^ { \prime } \| _ { L 2 } - \epsilon \} ,$ where ytrue denotes the ground truth labels rather than random labels. $l o s s _ { g } ^ { \prime }$ only indicates the purpose of anonymizing data, but $l o s s _ { g }$ has not only an anonymization effect but also a camouflage effect which forces the output of generator to be some specific label.

TABLE I DETAILS OF THE DEVICE MODELS 

<table><tr><td>Brand</td><td>Proportion</td><td>Brand</td><td>Proportion</td></tr><tr><td>Apple iPhone</td><td>30.77%</td><td>Nexus</td><td>3.42%</td></tr><tr><td>Apple iPad</td><td>16.24%</td><td>Vivo</td><td>2.56%</td></tr><tr><td>Xiaomi</td><td>9.40%</td><td>Nubia</td><td>1.71%</td></tr><tr><td>Huawei</td><td>12.82%</td><td>LeShi</td><td>1.71%</td></tr><tr><td>Samsung</td><td>7.69%</td><td>LG</td><td>0.85%</td></tr><tr><td>OnePlus</td><td>5.98%</td><td>Lenovo</td><td>0.85%</td></tr><tr><td>MeiZu</td><td>5.13%</td><td>OPPO</td><td>0.85%</td></tr></table>

TABLE IIFINGERPRINTING ACCURACY FOR 117 DEVICES OF A SINGLE SENSORAND FUSING 2 SENSORS GIVEN 1 SECOND DATA

<table><tr><td></td><td>Accuracy</td><td>Majority voting (20s)</td></tr><tr><td>Accelerometer</td><td>90.26%</td><td>93.99%</td></tr><tr><td>Gyroscope</td><td>68.62%</td><td>80.03%</td></tr><tr><td>Fusing results of 2 sensors</td><td>91.41%</td><td></td></tr></table>

the output of motion sensor based applications to test the anonymized data, e.g., we use the output of a pedometer application to check if the step count of the anonymized data is correct.

# VII. DATA-DRIVEN ANALYSIS

To deeply investigate, we collect a large highly diverse reallife dataset over 6 months, and conduct a series of data analysis and evaluation based on the dataset. Based on extensive experimental results, we further explore the multi-dimension device features and the fingerprint capacity, and reveal more insights about different influence factors (e.g., human and hardware model) on fingerprinting. We also prove the effectiveness and efficiency of our fingerprinting and anonymizing models.

# A. Data Collection

With users’ permission, we collect motion sensor (accelerometer and gyroscope) data from total 117 mobile phones with 13 different brands (Tab. I) when the users performed arbitrary movements. The sensor data is sampled at $6 0 H z \sim 2 0 0 H z$ , and each data record is annotated with the device id and user id. We divide continuous sensor data (more than 150 hours data) into 1 ∼ 20-second segments as our dataset. For training and testing, we randomly split our dataset into two parts: 80% for training and the other 20% for testing. To prevent bias of evaluation results caused training/testing data selection, for every experiment we repeat random training data selection ten times and report the average results.

# B. Explore Multi-Dimension Features

We firstly explore the multi-dimension feature space of the device fingerprint, since feature dimensionality significantly affects the capacity (see Section IV-B).

Two sensors: accelerometer and gyroscope: Here, two sensors (accelerometer and gyroscope) can be treated as independent dimensions for device fingerprinting. First, we conduct LSTM-based fingerprinting on each sensor’s data separately. As shown in Tab. II, given only 1 second data, to identify 117 devices we can achieve 90.26% accuracy for accelerometer and 68.62% accuracy for gyroscope. With majority voting of 20 seconds data, the accuracy can be improved to 93.99% and 80.03% respectively. By fusing predict results of two sensors using confidence boosting strategy,5 our model achieves 91.41% accuracy, which is close to the accuracy of fusing two sensors’ data together as input into one network.

![](images/e26419ce80fcd07d163a04965c92aa1751991d9b5a81511acab845702d261ed4.jpg)



(a）Distribution in accelerometer dimension

![](images/13bbcb11d60fa66401fb0d2c1a3f0e213cd8e3474bbf9fdd1d09912f20f46f67.jpg)



(b）Distribution in gyroscope dimension

![](images/485a8f348e21a21c8e36b37d9e7dc2f84328a758fcffb9f802f5d0b5df3f3df0.jpg)



(c)Expectation number of indistinguishable devices

![](images/baea22f6347e159eee99dbc339b4b9ab7f71fe515344acee32376a625d21b3b9.jpg)



(d）The probability for indistinguishable devices

Fig. 14. Fingerprinting capacity in two dimension   
TABLE IIIFINGERPRINTING ACCURACY FOR 117 DEVICES OF A SINGLE AXIS ANDFUSING 6 AXES GIVEN 1 SECOND DATA

<table><tr><td>Senor</td><td>Axes</td><td>Accuracy</td></tr><tr><td rowspan="3">Accelerometer</td><td>ax</td><td>72.56%</td></tr><tr><td>ay</td><td>72.96%</td></tr><tr><td>az</td><td>43.57%</td></tr><tr><td rowspan="3">Gyroscope</td><td>gx</td><td>52.92%</td></tr><tr><td>gy</td><td>54.02%</td></tr><tr><td>gz</td><td>53.85%</td></tr><tr><td colspan="2">Fusing results of 6 axes</td><td>87.01%</td></tr></table>

Six axes of accelerometer and gyroscope: Each sensor has three axes, which are supposed to be independent because they are physically separated in the MEMS-based model. We fingerprint three axes of each sensor separately. Given 1 second data of one axis of accelerometer and gyroscope, our model can respectively achieve 72.56% and 53% accuracy for 117 devices (Tab. III). Fusing the results of 6 axes together by confidence boosting strategy produces 87.01% accuracy.

Note that, though different sensors and different axes are physically independent, we cannot claim their fingerprint data are absolutely independent, because there may be some correlation among their fingerprints due to the environment influence like temperature and humidity. This may explain that, prediction based on fused data achieves better accuracy (92%) than fusing prediction results of different sensors/axes.

# C. Fingerprint Capacity Analysis

After exploring multi-dimension features, we are ready to map the Balls-into-Bins model with the fingerprinting scenario, and to estimate the capacity bound based on the investigation of real-life data. In our model, the “balls” are devices. “bins” are partitions of a feature space with distinguishable resolution. Since the fingerprinting model output a feature mapping for each data sample, we can treat the output of the model as a feature space, thus we first set the space partition to 117 according to the implemented model in our experiments. For the different feature dimensions, they are required to be independent to each other. Based on the analysis in Section VII-B, here we model feature dimensions as two sensors, which can be assumed independent. This two

5The confidence boosting strategy works as follows. For a prediction, a single predictor has different confidence scores for each label, which is the last layer’s values of the LSTM network. We add up the confidence scores of multiple predictors and take the maximum of them as the final predicted label.

![](images/9150c64b2b6f54cbffa4d502bb07cc4a04dd28eb48a8f2d57112b957274f8277.jpg)



Fig. 15. Capacity with different number of feature partition.

dimension model with 117 “bins” for each dimension gives the lower bound of fingerprint capacity. For the ball’s distribution probability on each dimension, we use the frequency that devices are classified into one “bin” (i.e., label). Fig. 14a and Fig. 14b illustrate the distribution probability of 117 bins for accelerometer and gyroscope respectively. First, we assume that all balls/devices have the same feature distribution in each dimension. Now we have obtained all required parameters of our multi-dimension feature capacity model (in Section IV-B) based on real data. Using our capacity model, we can estimate device fingerprint capacity as shown in Fig. 14c and 14d. For less than 90 devices, the expected collision is less than 1, and the probability of collision is less than 50%. For more than 110 devices, there is expected to be at least one collision.

Then we consider that different devices have distinct feature distributions in each dimension, which is the real situation based on our analysis on real data. Our theoretical model can be adapted to this case with a little expansion, and then we can calculate the expectation of indistinguishable devices in this 117 devices pool. Given any two devices, the probability that these two devices collide is the sum of the probabilities that they collide in each feature space bin. The expectation that they are indistinguishable $\mathbb { E } ( I _ { i j } )$ is the probability that they collide in each dimension, and the value can be calculated by multiplying all probabilities that two devices collide in each dimension. Thus, the expectation of the number of indistinguishable devices is summing over all distinct device pairs’ expectation that they are indistinguishable. That is $\mathbb { E } ( I ) =$ $\begin{array} { r } { \sum _ { 1 \le < i < j < m } \mathbb { E } ( I _ { i j } ) } \end{array}$ . Following the previous calculation, we investigate the influence of different feature space partitions on capacity. The number of partition (i.e. “bin” number) corresponds to the number of the model output nodes as well as the number of devices. Fig 15 shows the expectation of the number of indistinguishable devices6 and the single sensor fingerprinting accuracy against different number of “bins”. Analysis on the real data reveals that if 117 devices have distinct distribution in these two dimensions, the expected number of indistinguishable devices is 0.38. This is consistent with our experiment result that for 117 devices given 20 seconds data of each device the fingerprinting accuracy is 99%.

TABLE IV RESULTS IN DIFFERENT SCENARIOS AND COMPARISON WITH THE STATE-OF-THE-ART WORK [14] 

<table><tr><td>Device placement scenario</td><td>Method</td><td># of device</td><td>Metrics</td><td>Remarks</td></tr><tr><td>On flat surface</td><td>[14]</td><td>93</td><td>96% F-score</td><td>[14]&#x27;s result</td></tr><tr><td>On flat surface</td><td>Our LSTM model</td><td>97</td><td>97% Accuracy, 97% F-score</td><td>1 second, Our dataset</td></tr><tr><td rowspan="2">Arbitrary human motion</td><td>[14]</td><td>117</td><td>77% Accuracy, 78% F-score</td><td>[14]&#x27;s method and our 1 second dataset</td></tr><tr><td>Our LSTM model</td><td>117</td><td>91% Accuracy, 91% F-score</td><td>1 second, Our dataset</td></tr><tr><td rowspan="6">Mixed data</td><td>[14]</td><td>117</td><td>80% Accuracy, 79% F-score</td><td>[14]&#x27;s method and our 1 second dataset</td></tr><tr><td>Our LSTM model</td><td>117</td><td>92% Accuracy, 93% F-score</td><td>1 second, Our dataset</td></tr><tr><td>LSTM model</td><td>117</td><td>96% Accuracy (top-1), 97.4% Accuracy (top-2)</td><td>10 seconds, Our dataset</td></tr><tr><td>with continuous voting</td><td>117</td><td>96.5% Accuracy (top-1), 98% Accuracy (top-2)</td><td>20 seconds, Our dataset</td></tr><tr><td>LSTM model</td><td>117</td><td>98.8% Accuracy (top-1), 99.7% Accuracy (top-2)</td><td>10 1-second pieces, Our dataset</td></tr><tr><td>with un-continuous voting</td><td>117</td><td>99% Accuracy (top-1), 99.9% Accuracy (top-2)</td><td>20 1-second pieces, Our dataset</td></tr></table>

# D. Fingerprinting Accuracy in Different Scenarios

Now we conduct extensive experiments using our dataset to evaluate the performance of our LSTM model in different scenarios and compare it with the state-of-the-art work [14].

Static vs. Dynamic: First, we consider the static scenario, where the phone is placed on a flat surface, versus dynamic scenarios, where the user hold phone to conduct arbitrary movements, e.g., walking, running, typing. As summarized in Tab. IV, in the static scenario, our model and [14] both achieve a high accuracy, which are 97% and 96% F-score respectively. But when it comes to the highly dynamic scenario, given 1 second data, the F-score of [14] drops to 78% while the F-score of our model is 91%. Mixing the static and dynamic data together to recover the real-life scenario, our model achieves 93%, while F-score of [14] is only 79%. The results show that our model can achieve high fingerprinting accuracy and is more robust to large noises like human activity. The reason is that handcrafted features (e.g., max, min, mean, deviation and spectral centroid) used by [14] is very sensitive to large noises, while LSTM model is naturally designed to extract interested features of time sequences more effectively.

Majority voting: As presented in Tab. IV, leveraging continuous majority voting, given 10 seconds data, we can achieve 96% top-1 accuracy and 97.4% top-2 accuracy.

For our uncontinuous majority voting, given 10 pieces of 1 second data, we can achieve 98.8% top-1 accuracy and 99.7% top-2 accuracy. Fig. 11 and Fig. 12 plot the voting accuracy increasing with the length of data. Given 20 pieces of 1 second data, we can achieve 99.9% top-2 accuracy.

Influence of brands and models: Here, we are interested in the question “is it more difficult to distinguish devices of the same brand/model? ” The devices in our experiment have 13 brands and 65 models. As reported in Tab. V, the device distinguishability is slightly different across different brands or models. For the same brand or model, devices can still be identified with a high accuracy, e.g., 93% for 36 iPhones, 93% for 12 iPhone6 and 92% for 9 iPhone7.

Influence of human: The collected data carry both hardware information and human behavior information. To answer how

TABLE V FINGERPRINTING ACCURACY IN DIFFERENT GRANULARITY GIVEN 1 SECOND DATA 

<table><tr><td>Granularity</td><td>device #</td><td>user #</td><td>Accuracy</td><td>Remarks</td></tr><tr><td>All devices, all users</td><td>117</td><td>77</td><td>92%</td><td>Whole dataset</td></tr><tr><td rowspan="5">One brand, different devices</td><td>55</td><td>36</td><td>94%</td><td>Apple products</td></tr><tr><td>36</td><td>29</td><td>93%</td><td>iPhone</td></tr><tr><td>19</td><td>17</td><td>96%</td><td>iPad</td></tr><tr><td>11</td><td>10</td><td>94%</td><td>Xiaomi</td></tr><tr><td>15</td><td>14</td><td>91%</td><td>Huawei</td></tr><tr><td rowspan="3">One model, different devices</td><td>12</td><td>10</td><td>93%</td><td>iPhone6</td></tr><tr><td>9</td><td>8</td><td>92%</td><td>iPhone7</td></tr><tr><td>8</td><td>7</td><td>95%</td><td>iPad Air2</td></tr><tr><td rowspan="2">One user, different devices</td><td>12</td><td>1</td><td>89%</td><td>Our LSTM model</td></tr><tr><td>12</td><td>1</td><td>71%</td><td>Random Forest</td></tr></table>

![](images/3c4a592d31c4dfbb139c32038be26c0830a01cc7287f09d523b2b967756321cc.jpg)  
Fig. 16. Visualization of fingerprint features of different devices.

the human behavior fingerprints affect device fingerprinting, we asked one volunteer to use 12 different devices freely. As presented in Tab. V, in this case, our model can identify the 12 devices with 89% accuracy, which is slightly worse than the overall accuracy, while using random forest in [14] achieves 71% accuracy. So, the human factor indeed increases the difficulty of motion sensor based device fingerprinting. How to separate the human fingerprints and device fingerprints remains a challenging question.

Influence of device number and training data size: Given the fingerprint capacity, more devices imply more collisions in the feature space. Our evaluation results show that as the device number increases from 20 to 117, the accuracy declines from 99.20% to 92%. Obviously, more training data samples produce stronger fingerprinting models.

Feature visualization and Unsupervised fingerprinting: We treat the penultimate layer of our LSTM network as a device fingerprint feature and apply t-Distributed Stochastic Neighbor Embedding (t-SNE) to reduce the feature dimension for visualization. As Fig. 16 shows, most of the data samples are well separated, and some devices belonging to the same brand, i.e., Apple devices, are relatively close in the figure, which means these features can well represent the motion sensors’ hardware differences among different devices. Furthermore, we apply k-means clustering $~ ( k ~ = ~ 1 1 7 )$ o n features of 100,730 1 second data pieces of 117 devices. The Adjust Rand Index and the Adjust Mutual Information between the clustering result and the ground truth are 81.492% and 87.59% respectively. Compared with the ground truth, the k-means clustering achieves 61.28% accuracy for the top-1 voting and 84.656% for the top-2 voting. This result also proves the effectiveness of our fingerprinting model, more importantly, presents the chance to conduct unsupervised fingerprinting using the extracted features.

![](images/b228cceab9d2818df944b6f1b4563a7e42f2ffa3a8296d35dfaa003355bb0e66.jpg)



Fig. 17. Loss trend in training phase when using convolutional generator and full connected generator.

# E. Defenses Performance

1) Defenses Model Analysis: The generator of our anonymization model is analog to auto-encoder and it contains two convolutional layers. Comparing to the auto-encoder with fully connected layers, which is difficult to mimic the input data while training, our design with convolutional layers is much easier to train and minimize the loss. Fig. 17 shows the $L _ { 2 }$ distance between input data and de-fingerprinted data when training with the fully connected generator and convolutional generator. It reveals that during training, the $L _ { 2 }$ distance is hard to decrease to 20 or a lower level when using the fully connected generator, while $L _ { 2 }$ distance = 20 is a huge difference in 1 second sensor data (See Tab. VI).

In loss function loss $\begin{array} { r l r } { g } & { { } = } & { k } \end{array}$ ∗ cr oss\_entr opy(y, y ) + max $\{ 0 , \| x - x ^ { \prime } \| _ { L ^ { 2 } } - \epsilon \} , \ k$ and - are important parameters to balance two parts, i.e. the anonymization level as well as similarity level between original and anonymized data. Fig. 18 shows the anonymization level (Fingerprinting Accuracy) as well as similarity level $( L _ { 2 }$ Distance) between original and anonymized data with different $k ,$ epsilon values while training. When - = 6 and $k \ = \ 0 . 5 ,$ , we obtain an optimal $L _ { 2 }$ distance (i.e. around 5) but result in a fluctuated de-fingerprinting effect (i.e. fingerprinting accuracy ranging from 15% to 75% ). What’s more, by increasing k, the fingerprinting accuracy tends to be at a low level as well as a stable state (i.e. - = 6, k = 0.5 and - = 15, k = 1), and by increasing -, the model tends to make the sensor data more noisy (i.e. - = 30, k = 2 and - = 45, k = 2).

2) Defenses Trade-Off: We evaluate our anonymization model, and compare it with methods in [14], which directly adds various noises to the data. Since in dynamic scenario the sensor data has large variance, adding Laplace noise and white noise according to the methods in [14] will cause large $L _ { 2 }$ distance. So, here we compare the uniform noise in [14] with our model. We use the fingerprinting accuracy of our LSTM model, SVM and Random Forest models in [14] as the anonymization effect metric, and $L _ { 2 }$ distance and step count results as the data usage metric. There is a tradeoff between anonymization effect and data utility.

![](images/03060ed1eb3ccee7c62d06696087c89e4c98202a5485c633868dd04156d3bcc7.jpg)



![](images/2fca1e0e71d71136f40332f96a05bcb6e90cf342b6912e9d4e8d5b19ba566d24.jpg)



![](images/e6673b00a04c2afd01711a7de19a708cdb84007f640d828750917764e8ba3543.jpg)



![](images/2bbe48b5ef67ab264848ccadc6391602b2084f0fc768d2b593a6de06c03898a6.jpg)



Fig. 18. Loss trend with different parameter $k$ and $e .$

TABLE VI STEP COUNT RESULTS OF ANONYMIZED DATA BY OUR MODEL AND EXISTING METHOD [14] 

<table><tr><td rowspan="3">Our model</td><td> $L_2(\approx)$ </td><td>0</td><td>6</td><td>9</td><td>15</td><td>20</td><td>30</td></tr><tr><td>Mean</td><td>30</td><td>30</td><td>29.97</td><td>29.97</td><td>29.68</td><td>29.38</td></tr><tr><td>Stdev</td><td>0</td><td>0</td><td>0.21</td><td>0.34</td><td>0.63</td><td>0.89</td></tr><tr><td rowspan="3">Uniform noise</td><td> $L_2(\approx)$ </td><td>0</td><td>6</td><td>12</td><td>18</td><td>24</td><td>30</td></tr><tr><td>Mean</td><td>30</td><td>29.86</td><td>29.52</td><td>28.77</td><td>29.02</td><td>29.27</td></tr><tr><td>Stdev</td><td>0</td><td>0.51</td><td>0.76</td><td>1.31</td><td>1.62</td><td>1.78</td></tr></table>

![](images/41c1e879c43542184b078a72b3e58afb49a3c98d12a784067a9ae48c34f5a316.jpg)



Fig. 19. $L _ { 2 }$ distance and anonymization effect (measured by LSTM model).

Tab. VI presents step count results7 on sensor data anonymized by our model and uniform noise. The results in Tab. VI and Fig. 19 show that when $L _ { 2 }$ distance $< ~ 6 ,$ our model reduces the fingerprinting accuracy to 19% and cause no error to the step count; while uniform noise causes 0.51 deviation and only reduces the fingerprinting accuracy to 32%. When $L _ { 2 }$ distance < 30, our model causes less than 0.89 deviation and reduces the accuracy to 5%; while uniform noise causes 1.78 deviations and reduces the accuracy to 10%. Thus, our model achieves both better anonymization effect and data utility. Fig. 20 confirms that our model works effectively against different fingerprinting models.

7In our experiment, each of volunteers takes 30 steps with the mobile phones and repeats it for 20 times.

![](images/0f221a7e5f3b8f43069b818fac4ce0207a01428e5c65087adb71c6bffb891698.jpg)



Fig. 20. Anonymization effect measured by different fingerprinting models.

# F. Efficiency

We run our experiments on a server with 12 Intel Core i7-5930K 3.50GHz CPUs and 1 Titan X (Pascal) GPU. It takes us around 2 hours to train the LSTM model on the whole dataset. For the testing, it takes 0.04 ms to fingerprint 1 second sensor data, and around 0.9 ms for anonymizing the fingerprint of 1 second sensor data. As a comparison, we use MATLAB 2016b to run the SVM, random forest classifiers on a desktop with 8 Intel Core i7-6700 3.40GHz CPUs, the average time of extracting the 70 features proposed in [14] from 1 second data is 5.16s (some features are time-consuming), and it takes 0.5ms to classify 1 second data for Random Forest model. The results show that it is very costly to extract a large set of temporal and spectral features from the data. Instead, our models can provide both realtime fingerprinting and anonymizing.

# VIII. CONCLUSION

The raw sensor data, containing device-dependent noises, has been demonstrated to be an effective fingerprint of mobile devices. In this work, we showed that a few (less than 100) data samples collected from the motion sensors are enough to uniquely identify the source mobile device. We designed a multi-LSTM neural network framework to fingerprint mobile device sensor in real-life uses. Our system achieves 93% fingerprinting F-score given only one second data even users are doing arbitrary movement, and the accuracy improves to 98.8% when we have 10 seconds data. We then proposed a novel generative model to yield anonymized data with little fingerprint information while retain good data utility. Several interesting directions are left for the future investigation: in this work we only use motion sensors, while integrating other sensor data to define better device/human ID is still need to be studied; our method need sufficient sensor data to train the LSTM model, but how to reduce required training data is still an open question; in our anonymizing data utility evaluation, we use the $L _ { 2 }$ distance and a step counter application as metrics, which are still narrow, finding more applications to verify the utility of data is also a future work, e.g., positioning and navigation applications.

# APPENDIX A PROBABILITY OF COLLISION HAPPENS IN ONE DIMENSION

Balls-into-Bins problem with n bins and m balls in one dimension. In general setting, the probabilities that a ball is thrown into bins are $P = [ p _ { 0 } , p _ { 2 } , \cdot \cdot \cdot , p _ { n - 1 } ]$ , and each throw is independent. We denote $C o l _ { i } ^ { j }$ the event that there exist collisions for the balls whoses indices are within the range [i, j ]. We firstly consider the probability without any collision, which means that every two balls are in different bins for m balls:

$$
\{r _ {1}, r _ {2}, \dots , r _ {m} \} \subset \{0, 1, \dots , n - 1 \}
$$

where $r _ { i }$ is the index of bin the ball i thrown in.

We call this event a selection. And each selection happens with probability:

$$
\prod_ {i = 1} ^ {m} p _ {r _ {i}}
$$

So the probability without any collision is to add up all possible selection probability:

$$
Pr(\neg Col_{1}^{m}) = \sum_{\substack{\{r_{1},r_{2},\dots ,r_{m}\} \\ \subset \{0,1,\dots ,n - 1\}}}\prod_{i = 1}^{m}p_{r_{i}}
$$

We aim to calculate the collision probability and:

$$
\begin{array}{l} P r (C o l _ {1} ^ {m}) = 1 - P r (\neg C o l _ {1} ^ {m}) \\ = 1 - \sum_{\substack{\{r_{1},r_{2},\dots ,r_{m}\} \\ \subset \{0,1,\dots ,n - 1\}}}\prod_{i = 1}^{m}p_{r_{i}} \\ \end{array}
$$

Uniform distribution: Uniform distribution means that

$$
P = \left[ p _ {0} = \frac {1}{n}, p _ {1} = \frac {1}{n}, \dots , p _ {n - 1} = \frac {1}{n} \right]
$$

The probability for one selection happens is:

$$
\prod_ {i = 1} ^ {m} p _ {r _ {i}} = \frac {1}{n ^ {m}}
$$

and the number of selection is ${ \binom { n } { m } } * m ! .$ , so the collision probability:

$$
\begin{array}{l} P r (C o l _ {1} ^ {m}) = 1 - P r (\neg C o l _ {1} ^ {m}) \\ = 1 - \binom {n} {m} * m! \cdot \frac {1}{n ^ {m}} \\ = 1 - \frac {(n - 1) !}{n ^ {m - 1} (n - m) !} \\ \end{array}
$$

Normal distribution: we use binomial distribution B(n−1, p) as the approximation of normal distribution, which means that

$$
\begin{array}{l} P = \left[ p _ {0} \right. \\ = \binom {n - 1} {0} p ^ {0} (1 - p) ^ {n - 1},   p _ {1} \\ = \binom {n - 1} {1} p ^ {1} (1 - p) ^ {n - 2}, \dots , p _ {n - 1} \\ = \binom {n - 1} {n - 1} p ^ {n - 1} (1 - p) ^ {0} \\ \end{array}
$$

The probability for one selection happens is:

$$
\prod_ {i = 1} ^ {m} p _ {r _ {i}} = \prod_ {i = 1} ^ {m} \binom {n - 1} {r _ {i}} p ^ {r _ {i}} (1 - p) ^ {n - 1 - r _ {i}}
$$

So the collision probability is:

$$
P r (C o l _ {1} ^ {m}) = 1 - P r (\neg C o l _ {1} ^ {m})
$$

$$
= 1 - \sum_{\substack{\{r_{1},r_{2},\dots ,r_{m}\} \\ \subset \{0,1,\dots ,n - 1\}}}\prod_{i = 1}^{m}\binom {n - 1}{r_{i}}p^{r_{i}}(1 - p)^{n - 1 - r_{i}}
$$

# APPENDIX B EXPECTATION OF NUMBER OF COLLISIONS IN ONE DIMENSION

Note that we count collisions over distinct pairs, that is, if three balls fall into one bin, three collisions are counted. We denote $C o l _ { i j }$ be the event that ball i and ball j collide and $F _ { i } ^ { j }$ is the event that ball i falls into bin j . For balls i and ${ \boldsymbol { j } } ^ { \prime } { \boldsymbol { i } } \neq { \boldsymbol { j } } .$ , the probability that these two balls fall into the same bin k is $P r ( \dot { F } _ { i } ^ { k } ) \cdot P r ( \mathbf { \dot { \cal F } } _ { i } ^ { k } ) = p _ { k - 1 } ^ { 2 }$ since balls are thrown independently. A collision must occur in some bin, and any two balls cannot collide in more than one distinct bin. The probability that some two balls collide is the sum of their probability of collision over bins:

$$
P r (C o l _ {i j}) = \sum_ {k = 0} ^ {n - 1} p _ {k} ^ {2}
$$

It is also the expected number of collisions for balls i and j . That is

$$
\mathbb {E} (C o l _ {i j}) = \sum_ {k = 0} ^ {n - 1} p _ {k} ^ {2} = P P ^ {\prime}
$$

Summing over all distinct balls results in the expected total number of collisions C:

$$
\begin{array}{l} \mathbb {E} (C) = \mathbb {E} \left(\sum_ {1 \leq i <   j \leq m} C o l _ {i j}\right) \\ = \sum_ {1 \leq i <   j \leq m} \mathbb {E} (C o l _ {i j}) \\ = \sum_ {1 \leq i <   j \leq m} \sum_ {k = 0} ^ {n - 1} p _ {k} ^ {2} \\ = \frac {1}{2} m (m - 1) P P ^ {\prime} \\ \end{array}
$$

Uniform distribution: The probability for each bin is:

$$
P = \left[ p _ {0} = \frac {1}{n}, p _ {1} = \frac {1}{n}, \dots , p _ {n - 1} = \frac {1}{n} \right]
$$

and

$$
P P ^ {\prime} = \frac {1}{n}
$$

The expectation of number of collisions is:

$$
\mathbb {E} (C) = \frac {m (m - 1)}{2 n}
$$

Normal distribution: we use binomial distribution $B ( n \mathrm { ~ - ~ }$ 1, p) as the approximation of normal distribution, and the probability for each bin is:

$$
\begin{array}{l} P = \left[ p _ {0} \right. \\ = \binom {n - 1} {0} p ^ {0} (1 - p) ^ {n - 1},   p _ {1} \\ = \binom {n - 1} {1} p ^ {1} (1 - p) ^ {n - 2}, \dots , p _ {n - 1} \\ = \binom {n - 1} {n - 1} p ^ {n - 1} (1 - p) ^ {0} \\ \end{array}
$$

The expectation of number of collisions is:

$$
\mathbb {E} (C) = \frac {1}{2} m (m - 1) \sum_ {i = 0} ^ {n - 1} \left(\binom {n - 1} {i} p ^ {i} (1 - p) ^ {n - 1 - i}\right) ^ {2}
$$

# APPENDIX C PROBABILITY OF INDISTINGUISHABLE BALLS EXISTING IN MULTI-DIMENSION

There are k dimensional bins with the bin size ni where i is the dimension index, the probability that a ball is thrown into bins are $P _ { 1 } = [ \bar { p } _ { 0 } ^ { 1 } , p _ { 1 } ^ { 1 } , \bar { \cdot \cdot \cdot } , p _ { n _ { 1 } - 1 } ^ { 1 } ] , P _ { 2 } =$ $\begin{array} { c c c } { { [ p _ { 0 } ^ { 2 } , p _ { 1 } ^ { 2 } , \cdots , p _ { n _ { 2 } - 1 } ^ { 2 } ] , \cdots , P _ { k } } } & { { = } } & { { [ p _ { 0 } ^ { k } , p _ { 1 } ^ { k } , \cdots , p _ { n _ { k - 1 } } ^ { k } ] , } } \end{array}$ the $\bar { p }$ of p is the bin index, and each throw is independent, each dimension is independent. In k-dimensional case, each throw results in a k-dimensional coordinate $( x _ { 1 } , x _ { 2 } , \cdots , x _ { k } )$ of this ball. We denote P is the Cartesian product of k-dimension probability sets:

$$
\begin{array}{l} P = \left\{\left(p _ {1}, p _ {2}, \dots , p _ {k}\right) \mid p _ {i} \in \left\{p _ {j} ^ {i} \right\}, \right. \\ i \in \{0, 1, \dots , k \}, j \in \{0, 1, \dots , n _ {i} \} \} \\ \end{array}
$$

where i and $| P | = n _ { 1 } * n _ { 2 } * \cdot \cdot \cdot * n _ { k }$

Since each throw is independent, the probability that a ball throw into a k-dimensional bins with coordinate $( x _ { 1 } , x _ { 2 } , \cdots , x _ { k } )$ is:

$$
P r \left[ \left(p _ {1}, p _ {2}, \dots , p _ {k}\right) \right] = \prod_ {i = 1} ^ {k} p _ {x _ {i}} ^ {i}
$$

where as

$$
\begin{array}{l} x _ {1} \in \{0, 1, \dots n _ {1} \}, x _ {2} \in \{0, 1, \dots n _ {2} \}, \dots , x _ {k} \in \{0, 1, \dots n _ {k} \} \\ p _ {1} = p _ {x _ {1}} ^ {1}, p _ {2} = p _ {x _ {2}} ^ {2}, \dots , p _ {k} = p _ {p _ {k}} ^ {k} \\ \end{array}
$$

We first consider the probability that every two balls are distinguishable, which means that all balls’ coordinate are different from each other:

$$
P r (\neg I _ {i} ^ {j}) = \sum_ {\{P _ {1} ^ {\prime}, P _ {2} ^ {\prime}, \dots , P _ {m} ^ {\prime} \} \subset P} \prod_ {i = 1} ^ {m} P r (P _ {i} ^ {\prime})
$$

We aim to calculate the probability of indistinguishable balls existing:

$$
\begin{array}{l} P r (I _ {i} ^ {j}) = 1 - P r (\neg I _ {i} ^ {j}) \\ = 1 - \sum_ {\left\{P _ {1} ^ {\prime}, P _ {2} ^ {\prime}, \dots , P _ {m} ^ {\prime} \right\} \subset P} \prod_ {i = 1} ^ {m} P r (P _ {i} ^ {\prime}) \\ \end{array}
$$

Uniform distribution: In uniform distribution, bins’ probability in each dimension are

$$
P _ {k} = \left[ \frac {1}{n _ {k}}, \frac {1}{n _ {k}}, \dots , \frac {1}{n _ {k}} \right]
$$

The probability that a ball throw into a k-dimensional bins is:

$$
P r \left[ \left(p _ {1}, p _ {2}, \dots , p _ {k}\right) \right] = \frac {1}{\prod_ {i = 1} ^ {k} n _ {i}}
$$

the probability of indistinguishable balls existing:

$$
\begin{array}{l} P r (I _ {i} ^ {j}) = 1 - P r (\neg I _ {i} ^ {j}) \\ = 1 - \sum_ {\{P _ {1} ^ {\prime}, P _ {2} ^ {\prime}, \dots , P _ {m} ^ {\prime} \} \subset P} \prod_ {i = 1} ^ {m} P r (P _ {i} ^ {\prime}) \\ = 1 - \sum_ {\left\{P _ {1} ^ {\prime}, P _ {2} ^ {\prime}, \dots , P _ {m} ^ {\prime} \right\} \subset P} \prod_ {i = 1} ^ {m} \frac {1}{\prod_ {i = 1} ^ {k} n _ {i}} \\ = 1 - \sum_ {\left\{P _ {1} ^ {\prime}, P _ {2} ^ {\prime}, \dots , P _ {m} ^ {\prime} \right\} \subset P} \left(\frac {1}{\prod_ {i = 1} ^ {k} n _ {i}}\right) ^ {m} \\ = 1 - \binom {| P |} {m} m! * \left(\frac {1}{\prod_ {i = 1} ^ {k} n _ {i}}\right) ^ {m} \\ \end{array}
$$

# APPENDIX D

# EXPECTATION OF THE NUMBER OF INDISTINGUISHABLE BALLS IN MULTI-DIMENSION

Note that we also count indistinguishable balls over distinct pairs. The probability that some two balls collide in one dimension is:

$$
P r (C o l _ {i j}) = \sum_ {k = 0} ^ {n - 1} p _ {k} ^ {2}
$$

For k-dimension, we denote $I _ { i j }$ the event that some two balls are indistinguishable and it is:

$$
P r (I _ {i j}) = \mathbb {E} (I _ {i j}) = \prod_ {s = 1} ^ {k} \sum_ {t = 0} ^ {n _ {s} - 1} (p _ {t} ^ {s}) ^ {2} = \prod_ {s = 1} ^ {k} P _ {s} P _ {s} ^ {\prime}
$$

Summing over all distinct balls results in the expected total number of collisions I :

$$
\mathbb {E} (I) = \sum_ {1 \leq i <   j \leq m} \prod_ {s = 1} ^ {k} \sum_ {t = 0} ^ {n _ {s} - 1} (p _ {t} ^ {s}) ^ {2} = \frac {1}{2} m (m - 1) \prod_ {i = 1} ^ {k} P _ {i} P _ {i} ^ {\prime}
$$

Uniform distribution: The probability for each bin in one dimension is:

$$
P _ {k} = \left[ \frac {1}{n _ {k}}, \frac {1}{n _ {k}}, \dots , \frac {1}{n _ {k}} \right]
$$

and

$$
P _ {k} P _ {k} ^ {\prime} = \frac {1}{n _ {k}}
$$

The expectation of number of indistinguishable balls is:

$$
\mathbb {E} (I) = \frac {m (m - 1)}{2 \prod_ {i = 1} ^ {k} n _ {i}}
$$

Normal distribution: we use binomial distribution $B ( n -$ $1 , p )$ as the approximation of normal distribution, where $p$ for dimension i is $p _ { i } .$ , and the probability for each bin in dimension i is:

$$
\begin{array}{l} P _ {i} = \left[ \binom {n _ {i} - 1} {0} p _ {i} ^ {0} (1 - p _ {i}) ^ {n _ {i} - 1}, \binom {n _ {i} - 1} {1} p _ {i} ^ {1} (1 - p _ {i}) ^ {n _ {i} - 2}, \right. \\ \dots , \binom {n _ {i} - 1} {n _ {i} - 1} p _ {i} ^ {n _ {i} - 1} (1 - p _ {i}) ^ {0} \Big ] \\ \end{array}
$$

The expectation of number of collisions is:

$$
\mathbb {E} (N) = \frac {1}{2} m (m - 1) \prod_ {i = 1} ^ {k} \sum_ {j = 0} ^ {n _ {i} - 1} \left(\binom {n _ {i} - 1} {j} p _ {i} ^ {j} (1 - p _ {i}) ^ {n _ {i} - 1 - j}\right) ^ {2}
$$

# REFERENCES

[1] X. Guo, J. Liu, and Y. Chen, “FitCoach: Virtual fitness coach empowered by wearable mobile devices,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), May 2017, pp. 1–9.   
[2] C. Liu et al., “Lasagna: Towards deep hierarchical understanding and searching over mobile sensing data,” in Proc. 22nd Annu. Int. Conf. Mobile Comput. Netw. (MobiCom), Oct. 2016, pp. 334–347.   
[3] Y. Jiang, Z. Li, and J. Wang, “PTrack: Enhancing the applicability of pedestrian tracking with wearables,” in Proc. IEEE 37th Int. Conf. Distrib. Comput. Syst. (ICDCS), Jun. 2017, pp. 2193–2199.   
[4] L. Zhang et al., “It starts with iGaze: Visual attention driven networking with smart glasses,” in Proc. 20th Annu. Int. Conf. Mobile Comput. Netw. (MobiCom), Sep. 2014, pp. 91–102.   
[5] Z. Li, M. Li, P. Mohapatra, J. Han, and S. Chen, “iType: Using eye gaze to enhance typing privacy,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), May 2017, pp. 1–9.   
[6] M. Shahzad, A. X. Liu, and A. Samuel, “Secure unlocking of mobile touch screen devices by simple gestures: You can see it but you can not do it,” in Proc. 19th Annu. Int. Conf. Mobile Comput. Netw. (MobiCom), Oct. 2013, pp. 39–50.   
[7] C. Dwyer, “Privacy in the age of Google and Facebook,” IEEE Technol. Soc. Mag., vol. 30, no. 3, pp. 58–63, Sep. 2011.   
[8] L. Zhang et al., “Crowdbuy: Privacy-friendly image dataset purchasing via crowdsourcing,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Apr. 2018, pp. 2735–2743.   
[9] X.-Y. Li and T. Jung, “Search me if you can: Privacy-preserving location query service,” in Proc. IEEE INFOCOM, Apr. 2013, pp. 2760–2768.   
[10] L. Zhang et al., “Cloak of invisibility: Privacy-friendly photo capturing and sharing system,” IEEE Trans. Mobile Comput., to be published. doi: 10.1109/TMC.2018.2878711.   
[11] L. Zhang et al., “PIC: Enable large-scale privacy preserving contentbased image search on cloud,” IEEE Trans. Parallel Distrib. Syst., vol. 28, no. 11, pp. 3258–3271, Nov. 2017.   
[12] J. Qian et al., “Towards privacy-preserving speech data publishing,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Apr. 2018, pp. 1079–1087.   
[13] J. Qian et al., “Voicemask: Anonymize and sanitize voice input on mobile devices,” Nov. 2017, arXiv:1711.11460. [Online]. Available: https://arxiv.org/abs/1711.11460   
[14] A. Das, N. Borisov, and M. Caesar, “Tracking mobile Web users through motion sensors: Attacks and defenses,” in Proc. NDSS, Feb. 2016, pp. 1–15.   
[15] H. Bojinov, Y. Michalevsky, G. Nakibly, and D. Boneh, “Mobile device identification via sensor fingerprinting,” Aug. 2014, arXiv:1408.1416. [Online]. Available: https://arxiv.org/abs/1408.1416   
[16] S. Dey, N. Roy, W. Xu, R. R. Choudhury, and A. Nelakuditi, “AccelPrint: Imperfections of accelerometers make smartphones trackable,” in Proc. NDSS, 2014, pp. 1–16.   
[17] J. Franklin et al., “Passive data link layer 802.11 wireless device driver fingerprinting,” in Proc. 15th Conf. USENIX Secur. Symp., Aug. 2006, Art. no. 12.   
[18] K. Mowery, D. Bogenreif, S. Yilek, and H. Shacham, “Fingerprinting information in javaScript implementations,” in Proc. W2SP, May 2011, vol. 2, no. 11, pp. 1–11.   
[19] J. Pang, B. Greenstein, R. Gummadi, S. Seshan, and A. Wetherall, “802.11 user fingerprinting,” in Proc. 13th Annu. ACM Int. Conf. Mobile Comput. Netw. (MobiCom), Sep. 2007.   
[20] L. C. C. Desmond, C. C. Yuan, T. C. Pheng, and R. S. Lee, “Identifying unique devices through wireless fingerprinting,” in Proc. 1st ACM Conf. Wireless Netw. Secur. (WiSec), Apr. 2008, pp. 46–55.   
[21] K. Mowery and H. Shacham, “Pixel perfect: Fingerprinting canvas in HTML5,” in Proc. W2SP, May 2012, pp. 1–12.   
[22] P. Eckersley, “How unique is your Web browser?” in Privacy Enhancing Technologies. Berlin, Germany: Springer, 2010, pp. 1–18.   
[23] L. Olejnik, C. Castelluccia, and A. Janc, “Why Johnny can’t browse in peace: On the uniqueness of Web browsing history patterns,” in Proc. 5th Workshop Hot Topics Privacy Enhancing Technol. (HotPETs), Jul. 2012, pp. 1–17.   
[24] N. Patwari and S. K. Kasera, “Robust location distinction using temporal link signatures,” in Proc. 13th Annu. ACM Int. Conf. Mobile Comput. Netw. (MobiCom), Sep. 2007, pp. 111–122.

[25] Z. Li, W. Xu, R. Miller, and W. Trappe, “Securing wireless systems via lower layer enforcements,” in Proc. 5th ACM Workshop Wireless Secur. (WiSe), Sep. 2006, pp. 33–42.   
[26] D. B. Faria and D. R. Cheriton, “Detecting identity-based attacks in wireless networks using signalprints,” in Proc. 5th ACM Workshop Wireless Secur. (WiSe), Sep. 2006, pp. 43–52.   
[27] V. Paxson, “On calibrating measurements of packet transit times,” in Proc. ACM SIGMETRICS Joint Int. Conf. Meas. Modeling Comput. Syst., vol. 26, Jun. 1998, pp. 11–21.   
[28] S. B. Moon, P. Skelly, and D. Towsley, “Estimation and removal of clock skew from network delay measurements,” in Proc. INFOCOM, Mar. 1999, pp. 227–234.   
[29] T. Kohno, A. Broido, and K. C. Claffy, “Remote physical device fingerprinting,” IEEE Trans. Dependable Secure Comput., vol. 2, no. 2, pp. 93–108, Apr./Jun. 2005.   
[30] R. M. Gerdes, T. E. Daniels, M. Mina, and S. F. Russell, “Device identification via analog signal fingerprinting: A matched filter approach,” in Proc. NDSS, Feb. 2006, pp. 1–11.   
[31] V. Brik, S. Banerjee, M. Gruteser, and S. Oh, “Wireless device identification with radiometric signatures,” in Proc. 14th ACM Int. Conf. Mobile Comput. Netw. (MobiCom), Sep. 2008, pp. 116–127.   
[32] A. Stisen et al., “Smart devices are different: Assessing and mitigatingmobile sensing heterogeneities for activity recognition,” in Proc. 13th ACM Conf. Embedded Netw. Sensor Syst. (SenSys), Nov. 2015, pp. 127–140.   
[33] Z. Zhou, W. Diao, X. Liu, and K. Zhang, “Acoustic fingerprinting revisited: Generate stable device id stealthily with inaudible sound,” in Proc. (CCS), Nov. 2014, pp. 429–440.   
[34] A. Das, N. Borisov, and M. Caesar, “Do you hear what I hear?: Fingerprinting smart devices through embedded acoustic components,” in Proc. (CCS), Nov. 2014, pp. 441–452.   
[35] T. B. Gabrielson, “Mechanical-thermal noise in micromachined acoustic and vibration sensors,” IEEE Trans. Electron Devices, vol. 40, no. 5, pp. 903–909, May 1993.   
[36] Z. Djuri´c, “Mechanisms of noise sources in microelectromechanical systems,” Microelectron. Rel., vol. 40, no. 6, pp. 919–932, Jun. 2000.   
[37] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Comput., vol. 9, no. 8, pp. 1735–1780, Nov. 1997.   
[38] H. Lee, P. Pham, Y. Largman, and A. Y. Ng, “Unsupervised feature learning for audio classification using convolutional deep belief networks,” in Proc. Adv. Neural Inf. Process. Syst., 2009, pp. 1096–1104.

![](images/1236167203f09c727caeabc0709ece0c75ee01fb720dbd87b27d018ea8d8c4c5.jpg)



Xiang-Yang Li received the bachelor’s degree from the Department of Computer Science and the bachelor’s degree from the Department of Business Management both from Tsinghua University, China, in 1995, and the M.S. and Ph.D. degrees from the Department of Computer Science, University of Illinois at Urbana–Champaign, in 2000 and 2001, respectively. He was a Professor with the Computer Science Department, Illinois Institute of Technology. He is currently a Professor with the School of Computer Science and Technology, University of

Science and Technology of China. He published a monograph Wireless Ad Hoc and Sensor Networks: Theory and Applications. He co-edited several books, including Encyclopedia of Algorithms. His research interests include wireless networking, mobile computing, security and privacy, cyber physical systems, and algorithms. He is an ACM Distinguished Scientist. He and his students received five best paper awards (IEEE GlobeCom 2015, IEEE HPCCC 2014, ACM MobiCom 2014, COCOON 2001, and IEEE HICSS 2001) and one best demo award (ACM MobiCom 2012). He is an Editor of several journals, including the IEEE TRANSACTIONS ON MOBILE COMPUTING and the IEEE/ACM TRANSACTIONS ON NETWORKING. He has served many international conferences in various capacities, including ACM MobiCom, ACM MobiHoc, and IEEE MASS.

![](images/3f6abe12964aed6ce89b43d3cbf3e69f813f5e88df1e9592f23ed2462c9fcea8.jpg)



Huiqi Liu received the B.S. degree from the Department of Computer Science and Technology, University of Science and Technology of China, China, in 2017, where he is currently pursuing the master’s degree. His research interests include mobile sensing data privacy, privacy issues in data publishing, and deep learning.

![](images/28d9689b913edc1994d872f3842a8445fb40af0cb2c05482db7c659d1eedbcf2.jpg)



Lan Zhang received the bachelor’s degree from the School of Software, Tsinghua University, China, in 2007, and the Ph.D. degree from the Department of Computer Science and Technology, Tsinghua University, in 2014. She is currently a Research Professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests span privacy protection, secure multiparty computation, and mobile computing, etc.

![](images/4d34a1aa12ae599a4e50822c4846501e942606ced38adc25a782c098015b33c0.jpg)



Zhenan Wu is currently pursuing the master’s degree with the Department of Computer Science and Technology, University of Science and Technology of China, China. His research interests include big data privacy and blockchain, etc.

![](images/465e849ef47a0700b77ef441ddef17091c2619ae0dc46dafa86b9be3cb8e68df.jpg)



Yaochen Xie is currently pursuing the bachelor’s degree in statistics with the School for the Gifted Young, University of Science and Technology of China. His research interests lie in data understanding, machine learning, and computer vision.

![](images/6b02bc873583d5075f7ef515687c8d8b4814ccdb58761f1be5775255464a80ab.jpg)



Ge Chen is an Expert Engineer and the Director with the Tencent Online Media Group, Advertising Platform Department. He has nearly ten years’ experience in online advertising, machine learning, and big data architecture.

![](images/3ce0dc54c9a516b5c513a91fa09dff43b9d04e19c0c8136d71f1cdf4fa1761da.jpg)



Chunxiao Wan is a Senior Software Engineer with the Tencent Online Media Group, Advertising Platform Department. He is responsible for big data product and architecture of Tencent.

![](images/c0bb968910b20761b11c4eb57eb7d4fcf72c01ce177642e9ac619a601c41de88.jpg)



Zhongwei Liang is the General Manager with the Tencent Online Media Group, Advertising Platform Department. He has over 15 years’ experience in online advertising, big data architecture, and software engineering.