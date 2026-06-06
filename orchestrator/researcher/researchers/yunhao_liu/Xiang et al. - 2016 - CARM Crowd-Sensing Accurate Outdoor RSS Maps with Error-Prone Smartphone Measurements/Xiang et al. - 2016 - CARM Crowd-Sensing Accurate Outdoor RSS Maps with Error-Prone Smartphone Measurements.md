# CARM: Crowd-sensing Accurate Outdoor RSS Maps with Error-prone Smartphone Measurements

Chaocan Xiang, Panlong Yang, Chang Tian, Lan Zhang, Hao Lin, Fu Xiao, Maotian Zhang, Yunhao Liu

Abstract—RSS (Received Signal Strength) maps provide fundamental information for mobile users, aiding the development of conflict graph and improving communication quality to cope with the complex and unstable wireless channels. In this paper, we present CARM: a scheme that exploits crowd-sensing to construct outdoor RSS maps using smartphone measurements. An alternative yet impractical approach in literature is to appeal to professionals with customized devices. Our work distinguishes itself from previous studies by supporting off-the-shelf smartphone devices, and more importantly, by mitigating the error-prone nature and inaccuracies of these devices to build RSS maps through crowd-sensing. The main challenges are that, we need to calibrate error-prone smartphone measurements with ‘inaccurate’ and ‘incomplete’ data. To address these challenges, we build the measurement error model of smartphone based on the experimental observations and analyses. Moreover, we propose an iterative method based on DFP(Davidon-Fletcher-Powell) algorithm, to estimate the parameters for the error models of each smartphone and the signal propagation models of each AP simultaneously. The key intuition is that, the calibrated measurements based on the error model are constrained by the physics of the signal propagation model. Finally, a model-driven RSS map construction scheme is built upon these two models with these estimated parameters. The theoretical analyses prove the optimality and convergence of this iterative method. Also, the crowdsensing experiments show that, CARM can achieve an accurate RSS map, decreasing the average error from 19.8 dBm to 8.5 dBm.

Index Terms—Crowd-sensing, Received signal strength, Smartphone, Signal propagation model

# 1 INTRODUCTION

W IFI APs have been pervasively deployed in urbanareas, e.g. i-Shanghai [1], and many urban WiFi areas,e.g. i-Shanghai [1], and many urban WiFi AP systems are emerging, such as SKYHOOK [2]. Communication quality and interference patterns are leading concerns for WiFi APs users. The RSS (Received Signal Strength) map of AP exhibits the received signal strength corresponding to this AP at each location within its coverage. Hence, in large-scale outdoor environments, RSS maps of APs could provide fundamental information for mobile users, e.g. aiding the development of conflict graph and knowing the conflict between APs on specific spectrum bands [3], selecting AP wisely and improving communication quality [4], as well as exploring white space for device-to-device communications in cellular networks [5].

• C. Xiang is with the Logistic Engineering University, Chongqing, China, 401331. E-mail: xiang.chaocan@gmail.com.   
• P. Yang (Correspondent author) is with the College of Computer Science and Technology, University of Science and Technology of China. E-mail: panlongyang@gmail.com.   
• C. Tian and M. Zhang are with the College of Communications Engineering, PLA University of Science and Technology, China. Email: maotianzhang@gmail.com.   
• H. Lin is with the School of Internet of Things Engineering, Jiangnan University, China.   
• F. Xiao is with the School of Computer, Nanjing University of Posts and Telecommunications, China, and Jiangsu High Technology Research Key Laboratory for Wireless Sensor Networks, China. E-mail: xiaof@njupt.edu.cn.   
• L. Zhang and Y. Liu are with MOE Key Lab for Information System Security, School of Software, Tsinghua University, China.

Unfortunately, it is non-trivial to construct accurate RSS maps due to highly complex physical environments. Moreover, extremely large-scale wireless network [6], [7], especially urban wireless access network, makes the RSS map construction more difficult. A naive method [8]–[10] can build artificial RSS maps with unacceptable inaccuracy [11], [12], using a signal propagation model with rule of thumb parameters. To address this problem, a measurement-calibrated propagation model based method [3] is recently proposed to construct accurate RSS maps with partial measurements. However, this method [3] is expensive and rarely updated in largescale outdoor environments, as it relies on customized measurements by the professionals with customized devices.

To solve these drawbacks of the current methods [3], [8]–[10], the crowd-sensing [13] can be leveraged to create an open and inexpensive platform for rendering up-to-date RSS maps. Recent studies also show that, the highly dynamic RSS values from smartphones can be leveraged for localization [14] and floor plan construction [15], [16] in some specific scenarios. Inspired by these works, we aim at building a crowd-sensing system to construct accurate outdoor RSS maps with RSS measurements of massive smartphones. Distinguished from previous methods [3], [8]–[10], this system can construct the accurate RSS maps with commercial offthe-shelf (COTS) devices, which significantly decreases the map construction cost.

To achieve this system, two principal challenges need

to be seriously addressed:

• Apart from the environment effects, the RSS measurements of smartphone are inaccurate. First, the noise from the specific mobile devices is diverse due to the diversity of smartphone manufactures. Moreover, the working scenario (such as putting the phone in hand and in pocket) also makes such diversity complex, bringing about even more dynamic of RSS values.   
• As the crowd-sensing users are untrained, and the application or software should be non-invasive, the RSS measurement collection is not reliable. Moreover, it does not make sense to require users to report RSS measurements constantly, especially in large-scale outdoor scenario, which incurs the ‘incomplete data’ problem.

In this paper, we present a Crowd-sensing Accurate outdoor RSS Map method with error-prone smartphone measurements, called CARM. Specifically, to address the first challenge, we build the measurement error model of smartphone based on the experimental observations. Further, we propose an iterative approach based on DFP(Davidon-Fletcher-Powell) algorithm [17], where crowd-sensing measurements are calibrated based on the ‘coarse’ signal propagation model, and these calibrated measurements are fed back to refine the previous ‘coarse’ model. The key intuition is that the calibrated measurements based on the error model are constrained by the physics of the propagation model. When the iterative process converges, we can achieve both the accurate calibrated measurements and the accurate propagation model simultaneously. Moreover, according to the second challenge, we leverage the accurate propagation model to predict the RSS values of the locations without measurements. In addition, we use a small number of seed users1 to improve the calibrated accuracy by direct and indirect encounter of other users. Theoretical analyses prove the convergence and optimality of our method, while real experiments evaluate its performance.

The major contribution of this paper is three-folds:

1) Based on the observations of real experiments, we build the measurement error model of smartphone. To the best of our knowledge, our work is the first study on building and using the measurement error model for taming noisy crowd-sensing data.   
2) We propose an iterative method based on the DFP algorithm to estimate the parameters of the measurement error model and the signal propagation model simultaneously, where both of them are unknown in prior and the ground truth is generally unavailable. The key insight is that, correlating the roaming features of mobile users and the propagation model, we can tame the ‘inaccurate’ and ‘incomplete’ crowd-sensing data.

1. The seed users’ smartphones have been calibrated, and its error model parameters are known previously.

3) We build the prototype system of crowd-sensing outdoor RSS maps, based on which we evaluate the proposed method. The results show that, CARM can achieve accurate RSS map with 8.5dBm average error, improving the accuracy by 57.2% when compared with the baseline method2 . The improved accuracy of RSS map will make conflict graph more convincing, and achieve more efficient spectrum usages.

The remainder of this paper is organized as follows. Firstly, we literally review the related work in Section 2, and make preliminary experiment studies for RSS measurement error in Section 3. After that, Section 4 introduces the research motivation and challenges. Section 5 proposes CARM method to address these challenges. We make the experiments based on the crowd-sensing prototype system to evaluate CARM approach in Section 6. Section 7 discusses the limitations of CARM method, and indicates the future work. Finally, we conclude our work in Section 8.

# 2 RELATED WORK

The simple methods [8]–[10] (called as parameters-based method) use the signal propagation model with rule-ofthumb parameters to construct artificial RSS maps in the outdoor environment. It is noted that, the propagation model is an empirical mathematical formulation for the characterization of wireless signal propagation [18]. However, according to the empirical studies [11], [12], these methods produce unacceptably inaccurate RSS map with low cost. Another naive method is the exhaustive on-site survey of RSS, which is nearly impossible in large-scale outdoor environments due to extremely high measurement cost. To address these problems, Zhou et al. [3] recently propose a method based on the measurement-calibrated propagation models, named as ground-truth based method. They only use a subset of on-site ground-truth samples to calibrate the propagation model, which is exploited to predict the RSS values of the overall area. This method can achieve an accurate RSS map. However, as it needs the professionals with special devices to accurately measure the RSS values, such approach would be costly and cannot be put into practice in large scale. In contrast, we leverage the crowd-sensing of users with the available but inaccurate devices (such as smartphone) to build accurate RSS maps with low cost. To sum up, the main differences between our method and existing methods are illustrated in Table 1.

Several studies [14]–[16], [19]–[22] also use crowdsensing to build other maps. Specifically, Rana et al. [19] use the microphones and GPS sensors of smartphones to build the noise map of city. They use the compressive sensing algorithm [23] to solve the ‘incomplete data’

2. It directly uses the raw measurements of smartphone to construct the RSS map based on the propagation model.

TABLE 1: Comparison between current methods and ours in constructing outdoor RSS maps. 

<table><tr><td>Methods</td><td>Working Condition</td><td>Accuracy</td><td>Cost</td></tr><tr><td>Parameters-based method</td><td>empirical parameters</td><td>low</td><td>low</td></tr><tr><td>Ground-truth based method</td><td>partial ground truth</td><td>high</td><td>high</td></tr><tr><td>CARM method</td><td>crowd-sensing measurements</td><td>high</td><td>low</td></tr></table>

problem of crowd-sensing, while exploiting manual calibration method to calibrate the measurement errors of each smartphone. However, the manual calibration of each user’s smartphone is difficult to realize for a large number of uncooperative users in crowd-sensing system. Conversely, we propose an automatic calibration method without the cooperation of the users. Additionally, crowd-sensing RSS measurements were used to build indoor map [14]–[16], [20]–[22]. For example, Shen et al. [14] build the indoor pathway map, while Bruno et al. [15], [16], [20]–[22] construct indoor RSS map. As these methods use the exhaustive samples of crowd-sensing to build map in the indoor environments, they cannot solve our problem, where crowd-sensing samples are partial in the outdoor environment. Similar to our work, in France, research scientists developed a crowd-sensing based project ( called Sensorly [24]) in 2010. The Sensorly project use the smartphone sensing data of 500 million volunteers from 50 countries to construct the coverage map of wireless network, such as 3G and WiFi. Also, this project provides a free web service for querying the wireless signal coverage. The Sensorly project focuses on constructing coarse signal coverage map, and could not effectively solve the inaccurate problem of the crowdsensing data. In contrast, our work digs into the measurement error model of smartphone, and leverages the signal propagation model to construct accurate RSS map.

# 3 UNDERSTANDING RSS MEASUREMENT ER-ROR IN SMARTPHONE

As the crowd-sensing system of RSS map construction heavily depends upon the sensing of users’ smartphones, the measurement errors of smartphones is a major reason leading to poor RSS map construction. As a result, in this section, we explore the errors of smartphone RSS measurements with real experiment study, bringing about the research problem and the solved ideas.

# 3.1 Experiment Design

We deploy four APs at different locations in an outdoor environment (i.e. the building rooftop of our laboratory as shown in Fig.1a). As shown in Fig.1b, three APs (i.e. AP1, AP2 and AP4) are deployed outside of buildings, while one AP (i.e. AP3) is deployed inside of buildings. In the building rooftop, the WiFi APs can be deployed arbitrarily according to our experimental requirements.

![](images/32a69d0c47791b4ee9c3006b07aad0031ab08f6c5e0a42141d73e814d8887c78.jpg)



(a) Site in Google satellite map

![](images/4aafc468e57c08418b8136f243250c22ae515a31bba097c5e76c3fcc6ed7bd6e.jpg)



(b) Actual deployment   
Fig. 1: Outdoor experiment site, i.e. the building rooftop of our laboratory(111m × 167m).

Also, considering the limited coverage of the deployed APs, e.g. less than 100m, the building roof top (111m × 167m) is qualified and satisfactory to investigate error models in a controllable environment with limited interference.

We develop an android-based smartphone application for sensing and collecting the RSS of APs. This application uses the WiFi signal detecting sensor and GPS of smartphone to acquire the ID number and RSS of the APs, as well as the location and time of sensing. Also, this application automatically sends this sensing data to the central server via the available wireless networks, such as WiFi network.

In this experiment, we divide the whole outdoor area into 2m × 2m grids, whose size is reasonable as the error of the GPS positioning is 2-3 meters [25]. The number of the grid points is about 1000. We measure RSS values of the APs at each grid point, using three types of ‘off-theshelf’ smartphones, i.e. Samsung, Huawei and Sharp3. Also, we collect measurements in three conventional working scenarios of smartphone, i.e. putting in hand, in pocket and in bag (backpack). Note that, these working scenarios can be identified by the IMU (Inertial Measurement Unit) sensors of smartphone in practice, which has been well studied in the literature [26]. Thus, this experiment has equivalently 9000 measured points. Several measured points are line-of-sight, while the others obstructed by obstacles are non-LoS. Notably, we employ a laptop equipped with an advanced WiFi card4 to achieve ground-truth measurement of each location. Such WiFi card is often used for ground-truth evaluation [3] due to its higher receiving sensitivity (-92dBm) comparing with conventional cards. Additionally, at each location, for both the smartphone measurement and the ground-truth measurement, we continuously measure for 50 times (it takes about 1 minute), and average these measurements to decrease errors.

![](images/f29590a45fe3b6584c1eff0f5ce9751c1a361f22e2e0cebe2da4f45b39376b8a.jpg)



(a) Samsung

![](images/2161eaadce7de8f762c068d17e2ed1f2fb751fa59dd85a2d626a9816241bf51b.jpg)



(b) Huawei

![](images/4f8e05dfb4092ae10d28bf382b48c04a1a93ef3b3b1adc2e6df8824c432475ca.jpg)



(c) Sharp   
Fig. 3: The frequency histogram for RSS measurement error of smartphone.

![](images/a56aeb14618084b8ab779f5b22b0f9e1974aec65e62f94f404908c65d2d8dd39.jpg)



(a) Samsung

![](images/ebc265f07ae5e7dade8c5ed670f0b2cbe01ad0dc6bbcf80f179ef28aed85221c.jpg)



(b) Huawei

![](images/5c20504d8b4ebb86a719da05348e413b16b8999ae6d2c6b0c50aca37ec39a3ed.jpg)



Fig. 4: RSS measurements of three different smartphones versus ground truth. The RSS measurements of all the smartphones in all the working scenarios are linear with the ground truth.

![](images/e84e529e05d0aceeccbeb91d99c312bfb1236512b0cc668ec8ba9a608ccc8be9.jpg)



Fig. 2: CDF of smartphone RSS measurement errors. 96% of the errors range from 10 dBm to 40 dBm.

# 3.2 Experiment Observation

Based on the above experiments, we make three observations as follows.

First, the RSS measurements in smartphone are bearing

3. Samsung N7108, Huawei U9508 and Sharp SH3307 smartphone.   
4. IDU-2850UG-U20 high-power wireless USB adapter of Wifly-City System Inc [27], equipped with a 7dBi external omni antenna and a dual amplifier.

TABLE 2: Error model of smartphone RSS measurement. y and x denote the smartphone RSS measurement and its ground truth, respectively. 

<table><tr><td>Error Model</td><td>In Hand</td><td>In Pocket</td><td>In Bag</td></tr><tr><td>Huawei</td><td>y=0.9x-32</td><td>y=1.2x-14</td><td>y=1.2x-16</td></tr><tr><td>Samsung</td><td>y=1.2x-17</td><td>y=1.1x-19</td><td>y=1.0x-22</td></tr><tr><td>Sharp</td><td>y=1.1x-17</td><td>y=1.1x-12</td><td>y=1.0x-21</td></tr></table>

considerable error. We evaluate the RSS measurement errors for these three types of smartphones. As shown in Fig.2, 96% of the errors are above 10 dBm, and more than 40% of the errors are above 20 dBm. Notably, the maximum error is up to 40 dBm.

Further, the errors of RSS measurements in smartphone can be characterized by the linear error model, i.e. the measurement errors are linear with the ground truth. We explore the model of RSS measurement error by experiments. Firstly, we try the normal distribution model. As illustrated in Fig.3a, 3b and 3c, the frequency distributions of RSS measurement errors are distinguished from the normal distribution for all these three types of smartphones. Moreover, we exploit the Jarque-Bera test method [28] to test the assumption, i.e. the RSS measurement errors of smartphone follow normal distribution. The test results reject this assumption. As a result, the RSS measurement errors of smartphone do not follow normal distribution model. Finally, we use the linear regression method to fit the relationship between the RSS measurements and the ground truth. As shown in Fig.4a, 4b and 4c, the measurements are linear with the ground truth in all the three types of smartphones as well as all the three working scenarios. The linear model achieved under Least Squares Rule [29] is shown in Table 2. Specifically, the slopes of all the error models are around 1. It is reasonable because the measurements should equal to the ground truth in the ideal case. Moreover, all the measurements have a negative offset, since the smartphones are provided with lower receiving gain due to the small antennas. These experiment results show that the RSS measurements of smartphone are linear with the ground truth. Thus, the RSS measurement errors of smartphone are linear with the ground truth.

Finally, the parameters for the error model of RSS measurements are tightly coupled with the working scenarios and smartphone types. As shown in Table 2, the smartphone types and working scenarios make a significant impact on the error models. Specifically, as shown in each column of Table 2, the model parameters vary with the smartphone types even in the same working scenario. Also, as shown in each row of Table 2, the model parameters differ among the working scenarios even in the same smartphone. Both the slope and the offset of the models are different. The offset difference is the dominant factor when users are far away from the AP (the ground truth is smaller). Conversely, the slope difference is the dominant factor when users are approaching to the AP.

# 4 MOTIVATION AND CHALLENGE

In this section, based on the experimental observations of Section 3, we present the motivation of the research problem and its challenges.

# 4.1 Motivations

It is a fundamentally important study to construct RSS maps in large-scale outdoor environment. However, current methods either have poor accuracy based on empirical parameters or have high cost based on onsite survey with customized devices. To address these drawbacks, the crowd-sensing of massive common users with smartphones can be leveraged to construct accurate RSS maps with small cost in large-scale environments.

The work process of the crowd-sensing based RSS map construction system is as follows. Large numbers of users simply walk around in the large-scale outdoor environment in normal course. Each user’s smartphone automatically records the RSS values corresponding to APs along with current locations (e.g. GPS) at different positions and different time. Simultaneously, they report this sensing data to a central server by available wireless networks, e.g. WiFi and cellular network. The server exploits large amounts of sensing data to construct and update the RSS maps for these APs in real time.

The RSS measurements of smartphones have large errors according to the experiment observations in Section 3.2, while they are incomplete due to the uncontrolled property of crowd-sensing users. As a result, the key to realizing this crowd-sensing system is to construct accurate RSS maps based on the inaccurate and incomplete crowdsensing measurements in the central server.

There are two opportunities which we can use to address this critical problem. First, the inspiring observation in Section 3.2 shows the linear relationship between the measurement error and the ground-truth value. Leveraging such simple but effective measurement error model would ensure the fidelity of smartphone measurements, which is fundamentally important for future efficient crowd-sensing applications [14], [30]. However, it is extremely difficult to use this error model to construct accurate RSS maps without any ground truth [31] [32]. Fortunately, in outdoor environment, signal propagation model can predict the RSS value of each location, providing instructive error correction hints in different locations. To the end, leveraging these two models will bring us opportunities to build accurate RSS maps with ‘inaccurate’ and ‘incomplete’ crowd-sensing data.

# 4.2 Challenges

However, achieving accurate measurement error model as well as signal propagation model is non-trivial. Two principal challenges should be well addressed as follows.

1) Measurement calibration with unknown model parameters: Although measurement error model can be used for calibration, its parameters are not previously known for mobile crowd-sensing users. Even worse, the parameters heavily depend on both smartphone types and working scenarios of users.   
2) Building propagation model with inaccurate measurements: Although signal propagation model can be used to predict the RSS values, unfortunately, the parameters of propagation model vary with physical environments [3], [18]. Furthermore, the parameter estimation only relies on inaccurate crowd-sensing measurements, thus coupling with the measurement calibration.

# 5 CARM DESIGN

# 5.1 Overview of CARM

In tackling the aforementioned challenges, we propose CARM method to construct accurate outdoor RSS maps with inaccurate and incomplete crowd-sensing measurements, based on the following two basic ideas.

1) We combine the measurements with the predictive RSS values based on the propagation models to estimate the error model parameters, which are used to calibrate the measurement errors. After that, we use these calibrated measurements to estimate the parameters of the propagation models.

2) We propose an iterative method to calibrate the measurements and estimate the propagation model parameters iteratively. Through iterations, the accuracy for both the calibrated measurements and the estimated parameters of propagation model improves incrementally until convergence.

Specifically, CARM method mainly consists of two following components.

• Iterative Estimation of Model Parameters (Section 5.2): Based on the DFP algorithm [17], we estimate the parameters of the measurement error models and those of the signal propagation models iteratively until convergence.   
• Model-driven RSS Map Construction (Section 5.3): When the iterations converge, based on the converged values of model parameter estimation, we use the measurement error model and the signal propagation model to construct accurate and complete RSS maps.

In the following sections, we firstly specify these two components of CARM individually, followed by giving the description and analysis of CARM algorithm.

# 5.2 Iterative Estimation of Model Parameters

In this section, leveraging the inherent relationship between the measurement error model and the propagation model, we propose an iterative method based on the DFP algorithm to estimate the parameters of these two models. In the following, we first build these two models, followed by formalizing the estimation problem of model parameters. Finally, we propose an iterative method to solve this problem.

# 5.2.1 Measurement Error Model and Propagation Model

Measurement Error Model: According to the experimental observation of Section 3.2, the RSS measurements of smartphone are linear with the ground truth. Let $S _ { i j } ^ { k }$ denote the k-th RSS measurement by the i-th user about the j-th AP. Hence, its calibrated RSS measurement $\mathcal { C } _ { i j } ^ { k }$ is given by:

$$
\mathcal {C} _ {i j} ^ {k} = \pi_ {i} \cdot S _ {i j} ^ {k} + \eta_ {i} \tag {1}
$$

In the error model, $\pi _ { i }$ and $\eta _ { i }$ denote two unknown parameters of this model, depending on both the smartphone types and the working scenarios. Table 3 summarizes the notations frequently used in this paper.

Signal Propagation Model: We use a typical signal propagation model $( i . e .$ . the uniform path loss model [18]) to characterize the outdoor RSS distribution of AP. Let $\chi _ { j }$ denote the location of the j-th AP, and ${ \ X } _ { i j } ^ { k }$ denote the k-th measured location of the i-th user about this AP. Thus, the predictive RSS value of the j-th AP at the location $\mathcal { X } _ { i j } ^ { k }$ is given by:

$$
\mathcal {P} _ {i j} ^ {k} = \beta_ {j} - \alpha_ {j} \cdot \log l _ {i j} ^ {k} \tag {2}
$$

TABLE 3: The frequently used notations. 

<table><tr><td>Symbol</td><td>Definition</td></tr><tr><td> $M, N$ </td><td>the number of APs and crowd-sensing users</td></tr><tr><td> $\pi_i, \eta_i$ </td><td>parameters of error model for  $i$ -th user</td></tr><tr><td> $\beta_j, \alpha_j$ </td><td>parameters of propagation model for  $j$ -th AP</td></tr><tr><td> $\mathcal{X}_{ij}^k$ </td><td> $k$ -th measured location of  $i$ -th user at  $j$ -th AP</td></tr><tr><td> $S_{ij}^k$ </td><td>RSS measurement of  $j$ -th AP by  $i$ -th user at  $\mathcal{X}_{ij}^k$ </td></tr><tr><td> $\mathcal{C}_{ij}^k$ </td><td>calibrated value for RSS measurement  $S_{ij}^k$ </td></tr><tr><td> $\mathcal{P}_{ij}^k$ </td><td>predictive RSS value of  $j$ -th AP at location  $\mathcal{X}_{ij}^k$ </td></tr><tr><td> $l_{ij}^k$ </td><td>distance of the location  $\mathcal{X}_{ij}^k$  from  $j$ -th AP</td></tr><tr><td> $U_j$ </td><td>set of users measuring  $j$ -th AP</td></tr><tr><td> $\mathbf{K}_{ij}$ </td><td>sample index set of  $i$ -th user at  $j$ -th AP</td></tr><tr><td> $\mathbb{X}_j$ </td><td>set of all the locations in  $j$ -th AP&#x27;s coverage</td></tr><tr><td> $\mathcal{F}$ </td><td>objective function of the estimation problem</td></tr><tr><td> $\mathbf{x}_t$ </td><td>current solution of the  $t$ -th iteration</td></tr><tr><td> $\mathbf{g}_t$ </td><td>current gradient of the  $t$ -th iteration</td></tr><tr><td> $\mathbf{d}_t$ </td><td>searching direction of the  $t$ -th iteration</td></tr></table>

In this propagation model, $l _ { i j } ^ { k }$ denotes the distance between the location $\mathcal { X } _ { i j } ^ { k }$ and the j-th AP. $\beta _ { j } = P _ { j } ^ { 0 }$ + $1 0 \gamma _ { j }$ log $d _ { 0 }$ , and $\alpha _ { j } ~ = ~ \mathrm { { \bar { 1 0 } } } \gamma _ { j } . ~ P _ { j } ^ { 0 }$ denotes the transmit power of the j-th AP. $d _ { 0 }$ and $\gamma _ { j }$ denote the reference distance and the path loss exponent, respectively. Thus, $\alpha _ { j }$ and $\beta _ { j }$ are the unknown parameters, depending on the settings of the j-th AP and its physical deployment environment.

# 5.2.2 Estimation Problem of Model Parameters

Ideally, both the calibrated measurements based on the accurate error model and the predictive RSS values based on the accurate propagation model are very close to the ground truth. Thus, the difference between the calibrated measurements and their corresponding predictive values is greatly small, when the parameters of the propagation model and the error model are both accurate. As a result, our goal is to compute the parameter estimations of the error model and propagation model, minimizing this difference. Formally, according to Eq.1 and $^ { 2 , }$ this parameter estimation problem is formalized as:

Minimize $\mathcal { F } ( \pi _ { i } , \eta _ { i } , \alpha _ { j } , \beta _ { j } , i \in [ 1 , N ] , j \in [ 1 , M ] ) ( 3 )$

where

$$
\begin{array}{l} \mathcal {F} = \sum_ {j = 1} ^ {M} \sum_ {i \in U _ {j}} \sum_ {k \in \mathbf {K} _ {i j}} \left(\mathcal {C} _ {i j} ^ {k} - \mathcal {P} _ {i j} ^ {k}\right) ^ {2} \tag {4} \\ = \sum_ {j = 1} ^ {M} \sum_ {i \in U _ {j}} \sum_ {k \in \mathbf {K} _ {i j}} \left(\pi_ {i} S _ {i j} ^ {k} + \eta_ {i} + \alpha_ {j} \log l _ {i j} ^ {k} - \beta_ {j}\right) ^ {2} \\ \end{array}
$$

where N and M denote the number of the crowd-sensing users and the deployed APs, respectively. $U _ { j }$ denotes the set of the users, measuring the RSS values of the j-th AP. $\mathbf { K } _ { i j }$ denotes the index set of samples by the i-th user about the $j \cdot$ th AP. The equation $\dot { ( } \mathcal { C } _ { i j } ^ { k } - \dot { \mathcal { P } } _ { i j } ^ { k } )$ quantifies the difference between the calibrated measurement of user and the corresponding predictive value. Since one $\mathrm { A P }$ may be sensed by several users for several times, $\mathcal { F }$ denotes the sum of all the differences between the calibrated measurements of all the users and the corresponding predictive values for each AP.

# 5.2.3 Iterative Estimation Method

As this parameter estimation problem is a singleobjective non-linear optimization problem [33], we use DFP algorithm to solve this problem. DFP algorithm exploits the gradient information and the variation of solution to adjust the search direction iteratively, in order to achieve the optimal solution. In each iteration, it mainly consists of two components, and we take the t-th iteration for an example to illustrate them in the following.

• Adjusting searching direction. Based on the current gradient and current solution, adjust the searching direction, so as to converge into the optimal solution. Let $\mathbf { x } _ { t }$ and ${ \bf g } _ { t }$ denote the current solution and the current gradient of the t-th iteration, respectively, i.e. $\mathbf { g } _ { t } = \nabla \mathcal { F } ( \mathbf { x } _ { t } )$ . Then, the searching direction of the t-th iteration (i.e. dt) is:

$$
\mathbf {d} _ {t} = - \mathbf {H} _ {t} \cdot \mathbf {g} _ {t} \tag {5}
$$

$$
\mathbf {H} _ {t} = \mathbf {H} _ {t - 1} - \frac {\mathbf {H} _ {t - 1} \cdot \mathbf {y} _ {t} \cdot \mathbf {y} _ {t} ^ {T} \cdot \mathbf {H} _ {t - 1}}{\mathbf {y} _ {t} ^ {T} \cdot \mathbf {H} _ {t - 1} \cdot \mathbf {y} _ {t}} + \frac {\mathbf {s} _ {t} \cdot \mathbf {s} _ {t} ^ {T}}{\mathbf {s} _ {t} ^ {T} \cdot \mathbf {y} _ {t}} \tag {6}
$$

where $\mathbf { H } _ { t }$ denotes the positive definite matrix of the t-th iteration, and the initial value $\mathbf { H } _ { 0 }$ is set in prior. $\mathbf { y } _ { t }$ denotes the difference between the current gradient and the latest one, i.e. $\mathbf { y } _ { t } = \mathbf { g } _ { t } - \mathbf { g } _ { t - 1 } . \mathbf { s } _ { i }$ t denotes the difference between the current solution and the latest one, i.e. $\mathbf { s } _ { t } = \mathbf { x } _ { t } - \mathbf { x } _ { t - 1 }$ .

• Estimating new solution. Based on the searching direction $\mathbf { d } _ { t } ,$ estimate the new solution to minimize the objective function in terms of this direction. Let $\mathbf { x } _ { t + 1 }$ denote the new solution of the (t + 1)-th iteration. Then, estimating this new solution is to solve the linear searching problem as Eq.7. It is easy to solve this problem by computing the derivative of the objective function.

$$
<   \hat {\tau} _ {t} > = \underset {<   \tau_ {t} >} {\arg \min} \mathcal {F} (\mathbf {x} _ {t + 1})
$$

$$
\mathbf {x} _ {t + 1} = \mathbf {x} _ {t} + \tau_ {t} \cdot \mathbf {d} _ {t} \tag {7}
$$

where $\tau _ { t }$ denotes the length of searching step.

# 5.3 Model-driven RSS Map Construction

We construct RSS maps, based on the parameter estimations of the measurement error model and the propagation model in the previous section. Specifically, according to the error model in Eq.1, we compute the calibrated values for the measurements of each smartphone, given its error model parameters. As only a small number of locations are measured, most of the locations are left without measurements. Luckily, we leverage the propagation model in Eq.2 to predict the RSS values of each location without measurement, given the model parameters for each AP.

Algorithm 1 : Crowd-sensing Accurate Outdoor RSS Maps Method with Error-prone Smartphone Measurements (CARM)

# Input:

Position set of APs: $\mathbf { X } _ { a } = \{ \mathcal { X } _ { j } , j \in [ 1 , M ] \}$

Crowd-sensing measurement set: Φ $\cup _ { i = 1 } ^ { N } \big \{ ( S _ { i j } ^ { k } , \mathcal { X } _ { i j } ^ { k } ) \big \}$

# Output:

RSS maps of APs: $\begin{array} { r } { \mathbb { R } = \bigcup _ { i = 1 } ^ { M } \{ ( R , \mathcal { X } ) | \forall \mathcal { X } \in \mathbb { X } _ { j } \} } \end{array}$

1: Initialize ${ \bf x } _ { 0 } ~ = ~ \{ \pi _ { i } ^ { ( 0 ) } , \eta _ { i } ^ { ( 0 ) } , \alpha _ { j } ^ { ( 0 ) } , \beta _ { j } ^ { ( 0 ) } , i ~ \in ~ [ 1 , N ] , j ~ \in ~$ $[ 1 , M ] \}$ .

%DFP-based Iterative Estimation

2: while $\mathcal { F } ( \mathbf { x } _ { t } )$ does not converge do

3: Compute the new searching direction $\mathbf { d } _ { t }$ according to $\operatorname { E q } . { \dot { 5 } }$ and $^ { 6 , }$ based on $\mathbf { x } _ { t }$ and $\mathbf { x } _ { t - 1 } .$ .

4: Compute the new solution $\mathbf x _ { t + 1 }$ according to Eq.7, based on $\mathbf { d } _ { t }$ and $\mathbf { x } _ { t } .$

5: $t = t + 1 ;$

6: end while

%Models-based RSS Map Construction

7: Let $\hat { \pi } _ { i } , \hat { \eta } _ { i } =$ converged value of $\pi _ { i } ^ { ( t ) }$ and $\eta _ { i } ^ { ( t ) }$ , respectively.

8: Compute $\mathcal { C } _ { i j } ^ { k }$ for $S _ { i j } ^ { k }$ according to Eq.1, based on $\hat { \pi } _ { i }$ and $\hat { \eta } _ { i } .$ .

9: Let $\begin{array} { r l } { \dot { \alpha } _ { j } , \ \hat { \beta } _ { j } } & { { } = } \end{array}$ converged value of $\alpha _ { j } ^ { ( t ) }$ and $\beta _ { j } ^ { ( t ) }$ respectively.

10: Compute $\dot { \mathcal { P } } ^ { k }$ of unmeasured location $\chi ^ { k } \in \mathsf { \Gamma } ( \mathcal { K } ^ { k } ) $ $\mathbb { X } _ { j } \backslash \widetilde { \mathbb { X } } _ { j } )$ , according to $\operatorname { E q } . 2 ,$ based on ${ \hat { \alpha } } _ { j }$ and $\hat { \beta } _ { j } .$ .

11: $\begin{array} { r } { \mathbb { R } = \bigcup _ { j = 1 } ^ { M } \Big \{ \{ { \mathcal C } _ { i j } ^ { k } , { \mathcal X } _ { i j } ^ { k } \} | \widecheck { \forall } { \mathcal X } _ { i j } ^ { k } \ \in \ \widetilde { \mathbb { X } } _ { j } \} \bigcup \{ ( { \mathcal P } ^ { k } , { \mathcal X } ^ { k } ) | { \mathcal X } ^ { k } \ \in \ } \end{array}$ $\mathbb { X } _ { j } \backslash \widetilde { \mathbb { X } } _ { j } \} \Bigg \} .$ .

12: return R

In addition, we use a small number of seed users, where the error model parameters of their smartphones are known previously. It is reasonable to include several ground-truth values as well as calibrated measurements in practice. First, there are a few advanced users or cooperative users, whose smartphones have been calibrated before being put into use. Second, although measurements with customized device need labor-intensive site-survey, sampling only several locations should be acceptable, $e . g .$ it could be possible that a user with a laptop comes in the vicinity of an AP and reports its measured RSS values. Leveraging a small number of calibrated smartphones or ground-truth values, CARM can effectively calibrate massive smartphone measurements. Further, even if more new smartphones were joined to contribute data, CAMR can still calibrate them with very few ‘bootstrapping’ measurements. It is worth noting that, only small numbers of seed users with limited samples are enough, e.g. only one seed user is used in our experimental study, and 25 samples for each AP can achieve high precision. Also, we will evaluate the impact of the seed user in Section 6.

# 5.4 Description and Analysis of CARM Algorithm

# 5.4.1 Description of Algorithm

Summarizing the two components of CARM method in Section 5.2 and 5.3, as illustrated in Algorithm 1, we give the algorithm description of CARM as follows.

The error model parameters of each user and the propagation model parameters of each AP are initialized by the empirical values in line 1. Note that, the influence of the initial values on the algorithm performance is slight, due to the convergence of iterations. In line 2- $6 ,$ the algorithm iteratively estimates the propagation model parameters and the error model parameters, until the objective function converges. After the iterations converge, in line 7-10, we use the converged parameter estimations of the error models to calibrate the smartphone measurements, and use those of the propagation models to predict the RSS values at the locations without measurement. Finally, in line 11-12, we construct the RSS maps, aggregating the calibrated measurements and the predictive values at the locations without measurement $\widehat { ( } i . e . \ \mathbb { X } _ { j } \backslash \widetilde { \mathbb { X } } _ { j } )$ . Note that, Xj denotes the set of all the locations in the coverage area of the j-th AP, and $\widetilde { \mathbb { X } } _ { j }$ denotes the set of locations with measurements, i.e. $\widetilde { \mathbb { X } } _ { j } \subseteq \mathbb { X } _ { j }$ .

# 5.4.2 Analysis of Algorithm

First, CARM algorithm has a polynomial time complexity. According to the literature [33], the time complexity of DFP-based Iterative Estimation is $O \big ( ( N + M ) ^ { 2 } { \dot { I } } \big )$ , where I denotes the number of the iterations. Moreover, in Models-based RSS Map Construction, the time complexity is O(T ), where $\hat { T }$ denotes the number of all the samples in RSS map. Thus, the time complexity of this algorithm is $O \big ( I ( N { + } M ) ^ { 2 } + T \big )$ .

And then, CARM method can converge to the optimal solution. In the following, we prove the optimal property of this method.

Theorem 1: The objective function of the model parameter estimation problem is convex.

Proof: We let $\begin{array} { r } { \Theta ^ { \mathbf { \widetilde { \mathbf { \Gamma } } } } = ( \pi _ { i } , \eta _ { i } , \alpha _ { j } , \beta _ { j } ) ^ { T } , \Gamma _ { i j } ^ { k } ( \Theta ) = ( \boldsymbol { \pi } _ { i } \cdot \boldsymbol { S } _ { i j } ^ { k } + } \end{array}$ $\eta _ { i } + \alpha _ { j } \cdot \log l _ { i j } ^ { k } - \beta _ { j } ) ^ { 2 }$ , and $\mathrm { G } _ { i j } ^ { k } ( \Theta ) = \pi _ { i } \cdot S _ { i j } ^ { k } + \eta _ { i } + \bar { \alpha _ { j } }$ log $l _ { i j } ^ { k } - \beta _ { j }$ . Then, we can derive the derivative of $\Gamma _ { i j } ^ { k } ( \stackrel { . } { \Theta } )$ with respect to Θ as:

$$
\nabla \Gamma_ {i j} ^ {k} (\Theta) = 2 G _ {i j} ^ {k} (\Theta) \cdot \left(S _ {i j} ^ {k}, 1, \log l _ {i j} ^ {k}, - 1\right) \tag {8}
$$

Thus, $\begin{array} { r } { \check { \forall } \Theta _ { 1 } = ( \pi _ { i } ^ { 1 } , \eta _ { i } ^ { 1 } , \alpha _ { j } ^ { 1 } , \beta _ { j } ^ { 1 } ) ^ { T } , \forall \Theta _ { 2 } = ( \pi _ { i } ^ { 2 } , \eta _ { i } ^ { 2 } , \alpha _ { j } ^ { 2 } , \beta _ { j } ^ { 2 } ) ^ { T } , } \end{array}$ according to Eq.8, we have:

$$
\nabla \Gamma_ {i j} ^ {k} (\Theta_ {1}) \cdot (\Theta_ {2} - \Theta_ {1}) = 2 \mathrm{G} _ {i j} ^ {k} (\Theta_ {1}) \left(\mathrm{G} _ {i j} ^ {k} (\Theta_ {2}) - \mathrm{G} _ {i j} ^ {k} (\Theta_ {1})\right) \tag {9}
$$

Also, we have

$$
\begin{array}{l} \Gamma_ {i j} ^ {k} (\Theta_ {2}) - \Gamma_ {i j} ^ {k} (\Theta_ {1}) = \left(\mathrm{G} _ {i j} ^ {k} (\Theta_ {2}) + \mathrm{G} _ {i j} ^ {k} (\Theta_ {1})\right) \\ \times \left(\mathrm{G} _ {i j} ^ {k} (\Theta_ {2}) - \mathrm{G} _ {i j} ^ {k} (\Theta_ {1})\right) \tag {10} \\ \end{array}
$$

According to Eq.9 and Eq.10, we have:

$$
\begin{array}{l} \Gamma_ {i j} ^ {k} (\Theta_ {2}) - \Gamma_ {i j} ^ {k} (\Theta_ {1}) - \nabla \Gamma_ {i j} ^ {k} (\Theta_ {1}) \cdot (\Theta_ {2} - \Theta_ {1}) \\ = \left(\mathrm{G} _ {i j} ^ {k} (\Theta_ {2}) - \mathrm{G} _ {i j} ^ {k} (\Theta_ {1})\right) ^ {2} \tag {11} \\ \end{array}
$$

As $\left( \mathrm { G } _ { i j } ^ { k } ( \Theta _ { 2 } ) - \mathrm { G } _ { i j } ^ { k } ( \Theta _ { 1 } ) \right) ^ { 2 } \geq 0 ,$ according to Eq.11, we have:

$$
\Gamma_ {i j} ^ {k} (\Theta_ {2}) - \Gamma_ {i j} ^ {k} (\Theta_ {1}) \geq \nabla \Gamma_ {i j} ^ {k} (\Theta_ {1}) (\Theta_ {2} - \Theta_ {1}) \tag {12}
$$

According to the decision condition of the convex function [33], $\Gamma _ { i j } ^ { k } ( \Theta )$ is convex. Since ${ \mathcal { F } } =$ $\sum _ { j = 1 } ^ { M } \sum _ { i \in U _ { j } } \sum _ { k \in \mathbf { K } _ { i j } } \Gamma _ { i j } ^ { k } ( \Theta )$ M , according to the additive property of the convex function [33], the objective function $\mathcal { F }$ of the model parameter estimation problem is also convex.

According to Theorem 1, the objective function of the model parameter estimation problem is a convex function. According to the convergence condition of the DFP algorithm [34], we can get the conclusion of the optimal solution5.

# 6 EXPERIMENTAL RESULTS

In this section, we conduct crowd-sensing experiment to evaluate CARM in terms of the two following aspects. First, we evaluate the calibration accuracy and prediction accuracy of CARM along with its convergence. After that, we evaluate the performance of RSS map construction based on a small-scale crowd-sensing system.

To evaluate our approach, we compare it with two comparative methods. The first one, called the Baseline method, does not calibrate the smartphone measurements. The raw measurements are directly used to estimate the signal propagation models, which are exploited to predict the RSS map. The second one is based on the ground-truth measurements of partial locations, called Partial ground truth based (PGT) method. Specifically, based on these ground truth, PGT method uses the linear regression method to estimate the measurement error model parameters of smartphone and the signal propagation model parameters of APs individually. After that, it uses this error model and this propagation model to calibrate the RSS measurements and predict the RSS values at unmeasured locations, respectively. PGT method is similar to the current work [3], while the difference is that PGT method additionally uses the error model to calibrate the RSS measurements. However, distinguished from CARM, PGT method uses the ground truth to estimate the parameters of these two models alone, while CARM jointly estimates them only based on raw RSS measurements.

# 6.1 Performance Evaluation of CARM

In this section, we make experiments to evaluate the performance of CARM in terms of the calibration accuracy and the prediction accuracy. In these experiments, we make a slight modification on the experimental settings

5. Our iterative method can converge to the optimal solution, where the total difference between the calibrated measurements based on the error model and the predictive RSS values based on the propagation model is minimized.

![](images/b43ac327cff229e8670ccc0e7850820ed6a07a35f3d216cb421ca3d197dc5818.jpg)



(a) Calibration error

![](images/9ef34649751ce90f352d21bd01c4d1ffbcbb79aa55e16669e7fb6c5032d96fbc.jpg)



(b) Prediction error   
Fig. 5: Comparison of both the calibration error and prediction error.

![](images/cf100fa2dcfed0f80bc3f3662f33b88ca17c0b56bd33354f0e417e79f6cd56ec.jpg)



(a) Calibration error

![](images/2fe89173291f7973575d471cb28cef20b3525f433fef81fedd9f64e5ce602c6c.jpg)



(b) Prediction error   
Fig. 6: Performance versus the number of APs sampled by the seed user.

![](images/0b3766357d28baa859c9ed1d68d98381cfb9996d035ddf04339bcc764a55709f.jpg)



(a) Calibration error

![](images/62ea8f1e9b2005d1e5622fd2141cba20ce5f4ca0c59058c623ff78b4b98f7208.jpg)



(b) Prediction error   
Fig. 7: Performance versus the number of samples by the seed user.

of Section 3.1 as follows. We recruit 9 volunteers to measure the RSS values of four APs as shown in Fig.1b. We set one user as the seed user, where the error model parameters are known in prior and achieved by off-line learning in practice. This seed user measures four APs, and makes 25 samples per AP at 25 different locations. Other users randomly walk in the deployed region of APs to make measurements at about 5000 locations, including line-of-sight ones and none-line-of-sight ones. Thus, the number of measurements by the seed user is significantly smaller than that of other crowd-sensing users.

There are two main metrics, i.e. the calibration error and prediction error. The calibration error (the prediction error) denotes the difference between the calibrated measurements of smartphone (the prediction RSS values) and the ground truth. In the baseline method, we use the errors of the raw RSS measurements as the calibration errors since it has no calibration. PGT method uses the ground-truth measurements of about 2000 locations for calibration and prediction.

In the following, we evaluate the calibration error and prediction error of CARM, the impact of the seed user (the number of APs and samples) on the performance, as well as the convergence of this algorithm.

# 6.1.1 Calibration and Prediction Accuracy

In this experiment, comparing with the baseline method and the PGT method, we evaluate the calibration and prediction accuracy of our approach.

For the calibration and prediction accuracy, our method makes a great improvement (20dBm) than the baseline method, and almost achieves the same accuracy as PGT method. As shown in Fig.5a and 5b, the calibration errors and prediction errors of CARM method are significantly less than those of the baseline method. Specifically, 95% of the calibration errors are less than 10 dBm for the CARM method, while 90% of the calibration errors are ranging from 10 dBm to 30 dBm in the baseline method. Notably, 94% prediction errors of the CARM method are less than 10 dBm. Meanwhile, 98% prediction errors of the baseline method are beyond 10 dBm, reaching up to 30 dBm in the worst case. Thus, our method can decrease the calibration and the prediction errors by about 20 dBm. Further, as depicted in Fig.5a and Fig.5b, CARM method achieves almost the same accuracy as the PGT method, in terms of both the measurement calibration and RSS prediction. Specifically, in PGT method, 95% of the calibration errors are less than 10 dBm, and 98% of the prediction errors are less than 10 dBm. However, the PGT method is nearly infeasible to realize, as it is laborintensive and time-consuming to get the massive ground truth in a large-scale environment.

The reasons in achieving these desirable properties of CARM are as follows. Combining the signal propagation model of APs with the measurement error model of smartphone, CARM calibrates the smartphone measurements and predicts the RSS values iteratively. Moreover, we use only a small number of available seed users (e.g. one seed user in this experiment) to calibrate other smartphones and estimate the propagation model. Leveraging the nature of the random roaming and the opportunistic encounters of the crowd-sensing users, CARM can achieve surprisingly good performance. Note that, the encountering of mobile users means that they are within the communication coverage, and highly possible that, they are connecting with the very same AP. As the communication coverage of the AP is large (e.g. 100 m) [18], the opportunities of encountering are fruitful.

# 6.1.2 Impact of the Number of APs

In this experiment, we analyze the influence of the number of the APs sampled by the seed user on the performance of our method. We change the number of

![](images/46f85df4b0c1a169a36608329ff591371381f2eec1481a0b3e30f1538a5e715d.jpg)



Fig. 8: Convergence of our algorithm. Our method converges only after 4 iterations.

![](images/2e68f189c1ab29d5436df196f7aa49d3a1e758464c21eb736822577b2c58a53e.jpg)



Fig. 9: Distribution of APs (red triangles) and the sampling trajectories of crowd-sensing users (black dotted lines).

# APs from 1 to 4.

The calibration and prediction accuracy of CARM increases with the number of sampled APs, but outperforms the baseline method all the time. As shown in Fig.6a and 6b, both the calibration accuracy and the prediction accuracy of CARM method increase with the number of sampled APs. Nevertheless, the accuracy of CARM method is much better than that of the baseline method, even when the seed user only samples one AP. For example, 50% of the calibration and prediction errors in CARM method are less than 15 dBm, while those in the baseline method are less than about 23 dBm. What’s more, the accuracy when the number of APs is 3 nearly approaches to that when the number of APs is 4. As a result, our method still achieves a high accuracy, even when the seed user does not sample all the APs. The reason is that, the seed user could calibrate the smartphones of the encountering users, which will also calibrate the smartphones of other users by random roaming and opportunistic encounter. Thus, leveraging the nature of the random roaming, more and more smartphones can be calibrated, even when they did not encounter the limited seed users directly.

# 6.1.3 Impact of the Number of Samples

In this experiment, we study the impact of the number of samples by the seed user. The number of the APs sampled by the seed user is set to 3. The number of RSS samples measured by the seed user per AP is 5 to 25.

Our method achieves high accuracy as the PGT method, only needing 25 samples. As depicted in Fig.7a and 7b, calibration errors and prediction errors of CARM method decrease with the number of the samples. However, when the number of samples is 5, our method can achieve a much higher accuracy comparing with the baseline method. Specifically, 90% of the calibration and prediction errors are less than 13 dBm in CARM method, while 90% of the errors are above 15 dBm for the baseline method. Furthermore, when the number of samples is 25, CARM method also achieves similar performance as the PGT method.

# 6.1.4 Convergence of Algorithm

In this experiment, we validate the convergence property of our algorithm. As depicted in Fig.8, after limited iterations (about 4 iterations), CARM method can converge into the optimal solution, where the objective function is minimized. Also, as shown in Fig.8, the objective values decrease dramatically with the iterations. Note that, the objective value denotes the value of the objective function F (•) in Eq.3. In addition, this experiment result is consistent with the theoretical analysis in Section 5.4.2.

# 6.2 Evaluation of RSS Map Construction

In this section, we evaluate the performance of RSS map construction by a small-scale crowd-sensing experiment. Specifically, as shown in Fig.9, we deploy 5 APs in the outdoor environment. Also, we recruit 20 volunteers to join in this crowd-sensing experiment. These users measure RSS values of the APs by roaming randomly in the trajectories, as shown in Fig.9. The movement speeds of these users are about 60-120 m/minute (i.e. the normal movement speed of persons). Moreover, they use 5 different types of smartphones (i.e. Samsung, Huawei, Sharp, Lenovo and HTC) with three working scenarios (i.e. in hand, in pocket and in bag). We set one user as the seed user, who measures 3 APs for about 35 measurements per AP, while other users make about 8000 measurements. Further, we use the advanced WiFi card to measure the ground-truth measurements exhaustively in these trajectories, the number of these measurements is about 2200 (the number of the measured points in the whole area is about 6000). In PGT method, we construct the RSS map by combining these ground-truth measurements at partial locations and the measurements of other locations which are predicted based on the signal propagation model calibrated by these ground truth measurements.

Our method can achieve a highly accurate RSS map with 8.5 dBm average error, and improve the accuracy by 57.2% in comparison with the baseline method. Here we only plot the RSS map of the 4-th AP due to limited pages, and those of other APs are similar to it. As shown in Fig.10a, 10b and 10c, comparing with that of the baseline method, the RSS maps of our method are much more similar to that of PGT method. Further, the average RSS error of RSS maps is 8.5 dBm in CARM, and 19.8 dBm in the baseline scheme, with the benchmark of the PGT method.

![](images/a0c7f4912afa3aec3f6204b8430208cb4b726d863e4773c71c5b959b28a2533f.jpg)



(a) CARM method

![](images/781729289008ff9dce66b5bd193e8de9df343d24195441601265580335f5b878.jpg)



(b) PGT method

![](images/1e43d31d56ac9d4758e19ff027a909e3af4b96cd62f7e70c279bf72b91a12c0f.jpg)



(c) Baseline method   
Fig. 10: RSS map construction of our method, comparing with the baseline method and PGT method. Back triangle denotes the AP location of the RSS map.

# 7 LIMITATIONS AND FUTURE WORK

In this section, we will discuss the limitations of our approach as well as the future work.

Change of RSS Measurements with Time: We make experiments to evaluate the change of smartphone RSS measurements with time. As the experiment settings of Section 3.1, we use three smartphones in hand to measure the RSS of AP at 26 locations. In each location, each smartphone measures 50 times consecutively with 2 seconds interval. First, we analyze the change of RSS measurements with the time at one location. As shown in Fig.11a, the RSS measurements vary slightly with the time for these three smartphones. The standard deviations are 1.52dBm, 0.77dBm, and 1.06dBm for Samsung, Huawei and Sharp smartphones, respectively. Moreover, we investigate the change of RSS measurement with the time at all the locations, and plot a box plot for the standard deviations of the RSS measurement change at 26 locations. As illustrated in Fig.11b, the change of RSS measurements with time is small at all these locations for the three smartphones. Specifically, the median standard deviations are 1.55dBm, 1.92dBm and 2.06 dBm, while the maximum ones are 2.40dBm, 3.56dBm, 3.32dBm for Samsung, Huawei and Sharp smartphones, respectively. In summary, these experimental results indicate that, the smartphone RSS measurements vary with the time due to environmental influences, such as the movement of other persons. However, this measurement change is slight in outdoor environments, e.g. the maximum deviation is less than 4 dBm for about 2 minutes. Thus, according to the experimental results, the long time may affect the performance of CARM method due to the timevarying RSS measurements, which will be explored and solved in the future.

Signal Propagation Model for WiFi AP: In this paper, we use the signal propagation model of WiFi AP to predict the RSS values, based on a assumption that the propagation of wireless signal follows the uniform path loss model. As this typical model mainly captures the essence of signal propagation, it is limited due to not considering several complex factors in various environments, such as shadow fading [25], the outage probability and coverage area [18]. There are two possible methods to solve the limitations of this model. First, we can use a more complex model to characterize the signal propagation based on available city maps which provide the information of shadowing fading [25], such as the Combined Path Loss and Shadowing model [18]. On the other hand, the accurate propagation models are extremely difficult to be achieved owing to variable wireless signal and complex environments [18]. Hence, instead of the propagation model, we can use the Compressive Sensing (CS) theory [35] to predict the RSS values, leveraging the correlation of RSS values in adjacent areas. Further, we will explore these two methods in the future.

Linear Model for Smartphone Measurement Error: In this paper, we exploit the linear model for characterizing the smartphone RSS measurement errors due to the following three reasons. At first, this model has been validated by different smartphones, usages, locations and environments in our real experiments. Also, a similar conclusion has been drawn and validated by the real experiments in the studies [36] [37] [38], i.e. the RSS measurements vary with WiFi devices owing to the difference of WiFi chipset, antenna type as well as encapsulation material, and they exhibit a linear relationship. Thus, as WiFi devices, smartphones of different companies also have this property. At last, this paper aims at constructing an accurate RSS map, using the measurement error model and signal propagation model. Although the linear model is not highly accurate, e.g. adding more complex and high-level residual term, this model is often used since it is simple and effective [36]–[38]. In future work, we will deeply investigate the RSS measurement error model of smartphone, and build more accurate and complex model.

![](images/da5581191a7eed7cc787fc741bccf3018c676b9c2498eed948ef4ab024f50e1f.jpg)



(a) One location

![](images/0e715e107ca77fe1712b02419f0f58561d460fdc39cecc385648a925b353f6ad.jpg)



(b) All the locations   
Fig. 11: (a) RSS measurements vary with time at one location; (b) The boxplot for the standard deviations of RSS measurement change with time at all the locations.

Ground-truth Evaluation: First, in our study, the ground-truth measurements have errors and are not strictly “ground truth”. However, it is reasonable for the following reasons. It is extremely hard to achieve the ground-truth RSS measurements in practice. Moreover, as most of current methods [3], we use an advanced device [3] with greatly smaller error to measure RSS values, which are considered as the ground truth roughly. In the future work, we will evaluate the errors of this advanced device further.

Second, in the experiments, we use PGT method as the benchmark of comparison. As mentioned in Section 6, PGT method is only based on the ground-truth measurements of partial locations and the measurements of other locations are estimated based on the signal propagation model, while the ground-truth method is based on the ground-truth measurements of all the locations. Thus, PGT (Partial ground truth based) method is not a strictly ground-truth method. However, it is reasonable to use PGT method as the benchmark for the following reasons. The ground-truth method is difficult and labor-intensive due to making exhaustive measurements in large-scale outdoor environments. Thus, as an approximate substitute, we use the PGT method to produce a rough ground-truth map. PGT method is proposed by Zhou et al. [3], and the experiment results [3] show that it can achieve high accuracy. In the future work, we will measure the ground truth exhaustively in the whole experiment area, and compare our method with the ground-truth method further.

Complex and Dynamic Environment: In this work, we only made a preliminary experiment in a controlled outdoor environment (e.g. a rooftop) to evaluate the CARM approach. Our setup allows us to realistically examine several challenges, e.g. several volunteers are roaming in this place; this area is shadowed by several obstacles, and several APs (e.g. AP3) are deployed inside of buildings as shown in Fig.1. However, there are other real world challenges we leave to future work. For example, in railway station and city-center, the dynamic space is crowded with persons; the APs are intermittently available; large numbers of users are participated in large-scale environments. These challenges will be considered in the future experiments.

The dynamic environments with many persons may deteriorate the performance of CARM method for the following reasons. As large numbers of persons are roaming around the APs, it dynamically changes the propagation of wireless signal, leading to the larger errors of the propagation model. In addition, massive APs in large-scale environments may make impacts on the performance of CARM method for the following reasons. CARM method uses the indirect calibration of a few seed users. When there are large numbers of APs deployed in large-scale environments, many APs are not sampled by these limited seed users. As shown in Fig.6, both the calibration accuracy and prediction accuracy of CARM method decrease with the number of the APs which are not sampled by the seed users. Hence, massive APs in the deployed area may decrease the performance of CARM method. To address this problem, we can use more crowd-sensing measurements from more users, leveraging the measurement diversity of different users. Moreover, we can add more seed users to achieve the ground-truth measurements for easing up the adverse influence of indirect calibration. In future work, we will study how to apply our method into these complex and dynamic environments.

AP Location: As mentioned before, we made an assumption that the APs’ locations are known in this paper. This assumption is reasonable for the following two reasons. First, parts of APs’ locations are available. e.g., the deployed geography of the city pubic WiFi APs is easily available [1]. Second, if some APs’ locations are unavailable, such as a few personal or private APs, we can achieve these APs’ locations with the involvement of persons [39], which is probable in the centralized crowdsensing network.

# 8 CONCLUSION

In this study, we construct accurate RSS maps with the crowd-sensing of available error-prone smartphones. We propose CARM method to solve the ‘inaccurate and incomplete data’ problem of the crowd-sensing. Specifically, we build the measurement error model of smartphones based on the experiment observations. Moreover, combining the error model with the propagation model, we propose an iterative method based on DFP algorithm to estimate the parameters of these two models at the same time. Also, the propagation models are used to predict the RSS values of the locations without measurements. The theoretical proof shows that our iterative method can converge to the optimal solution. Further, through the validation of the crowd-sensing experiments, our method outperforms the baseline method, and almost achieves the same accuracy as the Partial ground truth based method.

# ACKNOWLEDGMENT

We thank the anonymous reviewers for their constructive comments. This research is partially supported by NSF China under Grants No. 61190114, 61272487, 61232016, 61502520, U1405254, 61173136, 61232018, BK20150030, and CMMI 1436786, PAPD fund, CICAEET, and WSNLBKF201509.

# REFERENCES

[1] i-shanghai. [Online]. Available: http://www.i-Shanghai.sheitc. gov.cn/   
[2] Skyhook. [Online]. Available: http://www.skyhookwireless.com/   
[3] X. Zhou, Z. Zhang, G. Wang, X. Yu, B. Y. Zhao, and H. Zheng, “Practical conflict graphs for dynamic spectrum distribution,” in SIGMETRICS, 2013.   
[4] A. Schulman, V. Navda, R. Ramjee, N. Spring, P. Deshpande, C. Grunewald, K. Jain, and V. N. Padmanabhan, “Bartendr: a practical approach to energy-aware cellular data scheduling,” in Mobicom, 2010.   
[5] M. Fitch, M. Nekovee, S. Kawade, K. Briggs, and R. MacKenzie, “Wireless service provision in tv white space with cognitive radio technology: A telecom operator’s perspective and experience,” IEEE Communications Magazine, vol. 9, no. 3, pp. 64–73, 2011.   
[6] J. Shen, H. Tan, J. Wang, J. Wang, and S. Lee, “A novel routing protocol providing good transmission reliability in underwater sensor networks,” Journal of Internet Technology, vol. 16, no. 1, pp. 171–178, 2015.   
[7] S. Xie and Y. Wang, “Construction of tree network with limited delivery latency in homogeneous wireless sensor networks,” Wireless Personal Communications, vol. 78, no. 1, pp. 231–246, 2014.   
[8] Z. J. Haas, J. H. Winters, and D. S. Johnson, “Simulation study of the capacity bounds in cellular systems,” in PIMRC/WCN, 1994.   
[9] M. C. Necker, “Towards frequency reuse 1 cellular fdm/tdm systems,” in MSWiM, 2006.   
[10] L. Yang, L. Cao, and H. Zheng, “Physical interference driven dynamic spectrum management,” in DySPAN. IEEE, 2008, pp. 1–12.   
[11] J. Padhye, S. Agarwal, V. N. Padmanabhan, L. Qiu, A. Rao, and B. Zill, “Estimation of link interference in static multi-hop wireless networks,” in IMC, 2005, pp. 28–28.   
[12] R. Maheshwari, S. Jain, and S. R. Das, “A measurement study of interference modeling and scheduling in low-power wireless networks,” in Mobisys. ACM, 2008, pp. 141–154.   
[13] M.-R. Ra, B. Liu, T. F. La Porta, and R. Govindan, “Medusa: A programming framework for crowd-sensing applications,” in Mobisys, 2012.   
[14] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, “Walkiemarkie: Indoor pathway mapping made easy,” in NSDI, 2013.   
[15] H. Shin, Y. Chon, and H. Cha, “Unsupervised construction of an indoor floor plan using a smartphone,” IEEE Transactions on Systems, Man, and Cybernetics, vol. 42, no. 6, pp. 889 – 898, 2011.   
[16] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in Mobicom, 2012.   
[17] W. C. Davidon, “Variable metric method for minimization,” SIAM Journal on Optimization, vol. 1, no. 1, pp. 1–17, 1991.   
[18] A. Goldsmith, Wireless communications. Cambridge university press, 2005.   
[19] R. Rana, C. Chou, S. Kanhere, N. Bulusu, and W. Hu, “Ear-phone: an end-to-end participatory urban noise mapping system,” in IPSN, 2010.   
[20] L. Bruno and P. Robertson, “Wislam: Improving footslam with wifi,” in IPIN, 2011.   
[21] B. Ferris, D. Fox, and N. Lawrence, “Wifi-slam using gaussian process latent variable models,” in IJCAI, 2007, pp. 2480–2485.   
[22] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: Zero-effort crowdsourcing for indoor localization,” in Mobicom, 2012.   
[23] X. Wu and M. Liu, “In-situ soil moisture sensing: Measurement scheduling and estimation using compressive sensing,” in IPSN, 2012, pp. 1–11.   
[24] Sensorly. [Online]. Available: http://www.sensorly.com/

[25] J. Robinson, R. Swaminathan, and E. W. Knightly, “Assessment of urban-scale wireless networks with a small number of measurements,” in Mobicom. ACM, 2008, pp. 187–198.   
[26] M. Keally, G. Zhou, G. Xing, J. Wu, and A. Pyles, “Pbn: towards practical activity recognition using smartphone-based body sensor networks,” in Sensys. ACM, 2011, pp. 246–259.   
[27] “Wifly-city,” http://www.wifly-city.com.tw/en/index.php.   
[28] C. M. Jarque and A. K. Bera, “Efficient tests for normality, homoscedasticity and serial independence of regression residuals,” Economics Letters, vol. 6, no. 3, pp. 255–259, 1980.   
[29] A. Charnes, E. L. Frome, and P. L. Yu, “The equivalence of generalized least squares and maximum likelihood estimates in the exponential family,” Journal of the American Statistical Association, vol. 71, no. 353, 1976.   
[30] D. R. Karger, S. Oh, and D. Shah, “Efficient crowdsourcing for multi-class labeling,” in SIGMETRICS, 2013.   
[31] D. Wang, T. Abdelzaher, and L. Kaplan, “On truth discovery in social sensing: A maximum likelihood estimation approach,” in IPSN, 2012.   
[32] C. Xiang, P. Yang, C. Tian, Y. Yan, X. Wu, and Y. Liu, “Passfit: Participatory sensing and filtering for identifying truthful urban pollution sources,” IEEE Sensor Journal, 2013.   
[33] S. P. Boyd and L. Vandenberghe, Convex optimization. Cambridge university press, 2004.   
[34] P. Gill and W. Murray, “Quasi-newton methods for unconstrained optimization,” IMA Journal of Applied Mathematics, vol. 9, no. 1, pp. 91–108, 1972.   
[35] X. Wu, P. Yang, S. Tang, X. Zheng, and Y. Xiong:, “Privacy preserving rss map generation for a crowdsensing network,” IEEE Wireless Communications, vol. 22, no. 4, 2015.   
[36] A. Haeberlen, E. Flannery, A. M. Ladd, A. Rudys, D. S. Wallach, and L. E. Kavraki, “Practical robust localization over large-scale 802.11 wireless networks,” in Mobicom, 2004.   
[37] M. B. Kj?rgaard and C. V. Munk, “Hyperbolic location fingerprinting: A calibration-free solution for handling differences in signal strength,” in PerCom, 2008.   
[38] A. W. Tsui, Y.-H. Chuang, and H.-H. Chu, “Unsupervised learning for solving rss hardware variance problem in wifi localization,” Mobile Networks and Applications, vol. 14, no. 5, pp. 677–691, 2009.   
[39] K. Chintalapudi, A. P. Iyer, and V. N. Padmanabhan, “Indoor localization without pain,” in Mobicom, 2010.

![](images/4f73cbfd0c4a0f7488eb2c25b0e01cbb4083809d9cf68f0f72f86a0992892cb9.jpg)



Chaocan Xiang (S’10) received his B.S. degree and Ph.D. degree in computer science and engineering from Institute of Communication Engineering at the PLA University of Science and Technology, China, in 2009 and 2014, respectively. He is currently a lecturer in Logistic Engineering University of PLA, China. He has published more than 15 papers in peer-reviewed journals and refereed conference, such as IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Vehicular Technology,

and IEEE Sensors Journal, IEEE conference of MASS. His current research interests include wireless sensor networks, crowd-sensing networks and IOT.

![](images/38ce8cfb31772fa4cce2d04c4cb3fc7d7419eaf62cbbb7c7762a2949e72a2983.jpg)



SIGMOBILE Society.

Panlong Yang (M’02) received his B.S. degree, M.S. degree, and Ph.D. degree in communication and information system from Nanjing Institute of Communication Engineering, China, in 1999, 2002, and 2005, respectively. Dr. Yang is now a professor in the College of Computer Science and Technology, University of Science and Technology of China. His research interests include wireless mesh networks, wireless sensor networks and cognitive radio networks. He is a member of the IEEE Computer Society and ACM

![](images/2fe235b3b78c777ae22b8356cc4438c89a871edd1a3c1bce04b9d5aadc7afb9f.jpg)



Chang Tian (M’02) received his B.S. degree in communication and information system, M.S. degree and Ph.D. degree in computer science and engineering from Institute of Communications Engineering, Nanjing, China, in 1984, 1989 and 2001, respectively. During September 1995 to September 1996, he was a visiting scholar in Universit di Pisa of Italy. He is currently a professor at the PLA University of Science and Technology, China. He has published widely in the areas of distributed system, wireless ad-hoc network, signal processing for communications, information theory. His current research interests include wireless sensor network, network coding, etc.

![](images/8e145e6fadcfb07413a587a6b8bece9a3b22012fdd0413fc6cf2f36100f7c5b6.jpg)



Yunhao Liu (SM’06) received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. Being a member of Tsinghua National Lab for Information Science and Technology, he holds Tsinghua EMC Chair Professorship. Yunhao is the Director of Key Laboratory for Information System Security, Ministry of Education, and Professor at School of Software, Tsinghua University. He is also a faculty member at the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include pervasive computing, peerto-peer computing, and sensor networks.

![](images/bb133b61bf88970944101c7c22b983c0527b7b1fcd362f0551eba8207219061a.jpg)



Lan Zhang (M) received the Bachelor degree (2007) in School of Software at Tsinghua University, China, the PhD degree (2014) in the department of Computer Science and Technology, Tsinghua University, China. She is now a Post Doctor in the School of Software, Tsinghua University, China. Her research interests span social networks, privacy, secure multi-party computation and mobile computing, etc.

![](images/9477193edfe249c30de9e1cd8630a8ad1b8240e52713eaabed546755104a29eb.jpg)



Hao Lin received his B.S. degree and M.S. degree in computer science from Jiangnan University, in 2011 and 2014, respectively. He is currently a software engineer in China Pacific Insurance (Group) Co. Ltd. His current research interests include mobile computing, wireless network and data mining.

![](images/09fbf3082b213362807a78545fe1343fdac15ba8d686fcdf2053e4de2aaab074.jpg)



Maotian Zhang (S’12) received the B.S. degree in communication engineering from Tianjin University, China, in 2011. He is currently pursuing the Ph.D. degree in computer science and engineering at PLA University of Science and Technology, China. His current research interests include mobile computing, mobile crowdsensing networks and mobile social networks.

![](images/a850484e3be422afd3c36d08355b1d114182949a79729a2716d77e053d598646.jpg)



Fu Xiao received Ph.D in Computer Science and Technology from Nanjing University of Science and Technology, China. He is currently professor and PhD supervisor in School of Computer, Nanjing University of Posts and Telecommunications, China. His main research interests are Sensor Networks.