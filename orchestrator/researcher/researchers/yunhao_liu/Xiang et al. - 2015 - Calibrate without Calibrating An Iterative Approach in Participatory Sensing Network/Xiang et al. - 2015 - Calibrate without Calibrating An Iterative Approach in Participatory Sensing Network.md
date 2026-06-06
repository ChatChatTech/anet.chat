# Calibrate without Calibrating: An Iterative Approach in Participatory Sensing Network

Chaocan Xiang, Student Member, IEEE, Panlong Yang, Member, IEEE, Chang Tian, Member, IEEE, Haibin Cai, and Yunhao Liu, Senior Member, IEEE

Abstract—With widespread usages of smart phones, participatory sensing becomes mainstream, especially for applications requiring pervasive deployments with massive sensors. However, the sensors on smart phones are prone to the unknown measurement errors, requiring automatic calibration among uncooperative participants. Current methods need either collaboration or explicit calibration process. However, due to the uncooperative and uncontrollable nature of the participants, these methods fail to calibrate sensor nodes effectively. We investigate sensor calibration in monitoring pollution sources, without explicit calibration process in uncooperative environment. We leverage the opportunity in sensing diversity, where a participant will sense multiple pollution sources when roaming in the area. Further, inspired by expectation maximization (EM) method, we propose a two-level iterative algorithm to estimate the source presences, source parameters and sensor noise iteratively. The key insight is that, only based on the participatory observations, we can “calibrate sensors without explicit or cooperative calibrating process”. Theoretical analysis proves that, our method can converge to the optimal estimation of sensor noise, where the likelihood of observations is maximized. Also, extensive simulations show that, ours improves the estimation accuracy of sensor bias up to 20 percent and that of sensor noise deviation up to 30 percent, compared with three baseline methods.

Index Terms—Participatory sensing, sensor calibration, expectation maximization (EM) method

# 1 INTRODUCTION

RCECENT years have witnessed widespread usages ofsmart phones [1]. Sensors, e.g., cameras, GPS, accelerphone, are now becoming available at very low cost. Smart phone users unintentionally form a dense, large-scale sensing network with multiple sensors [2], [3]. Participatory sensing applications are becoming mainstream, especially for applications requiring pervasive deployment with massive number of sensors, such as urban environment monitoring [4], [5], [6]. For example, using the smartphones equipped with pollution sensors, the participants measure the pollution concentration at different locations when roaming. Large numbers of participants upload the measurements along with its locations (e.g., GPS) to the central server. Based on these measurements, the central server could determine the presence of the pollution sources and calculate the parameters accordingly (e.g., the source positions) [7], [8].

However, the low-cost sensors for the participatory sensing are prone to the unknown and uncontrollable

measurement errors. As a result, a fundamental issue is to automatically calibrate the sensors among uncooperative participants. Current cooperative methods [9], [10], [11], [12], [13], [14] calibrate with neighbor sensors or groundtruth. Nevertheless, the untrained and uncontrollable participants will not cooperate for sensor calibration [15]. Although several uncooperative calibration methods [16], [17] have been proposed, they need an explicit and particular calibration process, such as controlling the behaviors of the interesting sources.

We calibrate the sensors in the process of monitoring pollution sources, without an explicit and cooperative calibration process. Namely, only using the measurements for monitoring pollution sources, we can estimate the parameter values of sensor noise for each participant. The opportunity we use is that, a participant can sense multiple pollution sources at different locations with different time, due to routine roaming. We can exploit these diverse measurements across different pollution sources to estimate the sensor noise. Notably, two challenges need to be well addressed:

In participatory sensing without an explicit calibration process, the presences of the pollution sources along with their parameters are unknown in advance.   
Even worse, source presence estimation, source parameter estimation and sensor noise estimation are tightly coupled with each other, which makes previous methods without joint considerations unapplicable to our problem.

We tackle these challenges with two basic ideas. First, we leverage the diversity in the participatory sensing data for source presence estimation, while the presence information is fed back to enhance the estimation accuracy of source parameters and sensor noise. Second, most importantly, inspired by expectation maximization (EM) method [18], we can incrementally enhance the estimations of source presences, sensor noise and source parameters through a twolevel iterative algorithm. Also, we have validated the convergence of the proposed algorithm through theoretical analysis and experimental studies.

The contribution of this paper is three-fold:

1) To the best of our knowledge, ours is the first work to calibrate sensors in the participatory sensing network, where the participants are uncontrollable and uncooperative. With the participatory observations only, ours “calibrate sensors without explicit or cooperative calibrating process”.   
2) Inspired by EM method, we present ACTION, a sensor uto- alibration algorithm in wo-level tera-A C T Iti . The source presences are estimated based ONon the estimations of sensor noise and source parameters, which are afterwards re-estimated to enhance the previous estimations. Theoretical analysis shows that, ACTION can converge to the optimal estimations of sensor noise, where the likelihood of observations is maximized.   
3) We conduct extensive simulations in a medium-scale participatory sensing scenario. The results show that, ACTION can improve the sensor bias estimation accuracy about 20 percent, and the sensor noise deviation estimation accuracy about 30 percent, comparing with three baseline methods.

The remainder of this paper is organized as follows. Section 2 presents our system model. Section 3 formulates our study problem and transforms this problem into maximum expected likelihood problem. To address this problem, a sensor auto-calibration algorithm called ACTION is proposed in Section 4, followed by the experimental evaluation in Section 5. We discuss several influenced factors and give the future work in Section 6. Finally, we review the related works in Section 7 and conclude this paper in Section 8.

# 2 SYSTEM MODEL

In this section, we describe the system model of the participatory sensing for monitoring urban pollution sources. We consider that, N participants join in the participatory sensing network and report the observations about the pollution sources. We assume that each observation is only associated with one pollution source at one time with one location. The rationality behind this is that, most of the sensors can sense the pollution source with limited range. Since the number of pollution sources are limited and distributed in wide area, the sensing range is negligible to the distances between pollution sources.

The observation reported by the ith participant for the jth pollution source is denoted by $z _ { i j } ,$ which includes the pollution measurement $( \mathrm { i } . \mathrm { e } . , m _ { i j } ) ,$ , as well as its location $\mathcal { X } _ { i j } ,$ , $\mathrm { i . e . , ~ } z _ { i j } = ( m _ { i j } , \mathcal { X } _ { i j } )$ X. Note that, we only consider the two-¼ ð X Þdimensional coordinate [7]. Suppose that the jth pollution source with the intensity $\mathscr { C } _ { j }$ is located at the position $\chi _ { j } .$ . According to the inverse square law [8], the concentration measured at the location $\hat { \mathscr { X } _ { i j } } \left( \hat { \mathscr { X } _ { i j } } \neq \hat { \mathscr { X } _ { j } } \right)$ under the diffusion X X 6¼ Xof the jth pollution source is given by

$$
\mathbb {C} _ {j} (\mathcal {X} _ {i j}) = \frac {\mathcal {C} _ {j}}{\| \mathcal {X} _ {i j} - \mathcal {X} _ {j} \| ^ {2}}, \tag {1}
$$

where $\| \bullet \|$ denotes the euclidean distance between the locak  ktion of measurement $( \mathrm { i } . \mathbf { e } . , \ X _ { i j } )$ and that of the jth pollution source $( \mathrm { i . e . , } \ X _ { j } )$ X. We note that the above diffusion model has Xbeen widely used in the literatures of pollution source monitoring [7], [8], [19]. Besides, our method can apply to other models of the pollution sources.

The low-cost sensors suffer from the measurement errors, including the systematic bias and the random noise [12], [13]. According to Feng et al. [13], the random noise follows the Gaussian distribution with zero mean. Specifically, let $n _ { i }$ denote the random variable for the sensor noise of the ith participant. Then,

$$
n _ {i} \sim u _ {i} + N (0, \sigma_ {i} ^ {2}), \tag {2}
$$

where $u _ { i }$ denotes the systematic bias experienced by the sensor of the ith participant, and $\sigma _ { i }$ denotes the standard deviation of its random noise.

Depending on the hypothesis that the pollution source is absent $( H _ { 0 } )$ or present $\overset { \cdot } { ( } H _ { 1 } )$ , the measurement $m _ { i j }$ at the location $\mathcal { X } _ { i j }$ is given by

$$
H _ {0}: m _ {i j} = n _ {i} \tag {3}
$$

$$
H _ {1}: m _ {i j} = \mathbb {C} _ {j} (\mathcal {X} _ {i j}) + n _ {i}. \tag {4}
$$

According to Eqs. (2), (3) and (4), the conditional probability density of the observation $z _ { i j }$ reported by the ith participant about the jth pollution source is given by

$$
p \left(z _ {i j} \mid S _ {j} ^ {f}\right) = \phi \left(\frac {m _ {i j} - u _ {i}}{\sigma_ {i}}\right) \tag {5}
$$

$$
p \left(z _ {i j} \mid S _ {j} ^ {t}\right) = \phi \left(\frac {m _ {i j} - \mathbb {C} _ {j} \left(\mathcal {X} _ {i j}\right) - u _ {i}}{\sigma_ {i}}\right), \tag {6}
$$

where $S _ { \mathbf { \Phi } _ { i } } ^ { f }$ and $S _ { \it _ i } ^ { t }$ denote the jth pollution source is absent and present respectively. $\phi ( \bullet )$ is the probability density ðÞfunction of the standard normal distribution, i.e., $\phi ( x ) = $ 1 p x2= . $\scriptstyle { \frac { 1 } { \sqrt { 2 \pi } } } \exp ( - x ^ { 2 } / 2 )$

ffiffiffiffi2p expð 2ÞTable 1 summarizes the notations frequently used in this paper.

# 3 PROBLEM FORMATION AND TRANSFORMATION

In this section, we first formulate our problem as a maximum likelihood estimation (MLE) problem. Afterwards, we transform this problem into maximizing the expected likelihood, as it is extremely difficult to be solved due to ‘incomplete data problem’ [18]. We have proved that, maximizing the expected likelihood is the sufficient condition for MLE.

# 3.1 Problem Formulation

In the participatory sensing, using the smartphone, each participant reports the observations about the pollution source to the server, including the pollution concentration $( \mathrm { i } . \mathrm { e } . , m _ { i j } )$ and the measured location $( \mathrm { i . e . , } \chi _ { i j } )$ . Owing to the Xnatural mobility, a participant can report massive observations about multiple suspected pollution sources. Let N and M denote the number of the participants and that of the suspected pollution sources respectively. Note that, the number of the suspected pollution sources can be determined by clustering these observations according to the measured locations, and we adopt Mutual Information Based Clustering Algorithm [20] for clustering. As a result, the server acquires the observation matrix Z as Eq. (7).

TABLE 1 Frequently Used Notations 

<table><tr><td>Symbol</td><td>Definition</td></tr><tr><td> $N$ </td><td>the number of the participants</td></tr><tr><td> $M$ </td><td>the number of the suspected pollution sources</td></tr><tr><td> $U_i, S_j$ </td><td>theith participant, jth pollution source</td></tr><tr><td> $\mathbb{U}_j$ </td><td>the subset of participants reporting  $S_j$ </td></tr><tr><td> $\mathbb{S}_i$ </td><td>the subset of pollution sources reported by  $U_i$ </td></tr><tr><td> $\mathbb{C}_j(\mathcal{X}_{ij})$ </td><td>diffusion concentration of the location  $\mathcal{X}_{ij}$  for  $S_j$ </td></tr><tr><td> $m_{ij}, \mathcal{X}_{ij}$ </td><td>measurement of  $U_i$  about  $S_j$ , its location</td></tr><tr><td> $z_{ij}$ </td><td>observation of  $U_i$  about  $S_j$ , i.e.  $z_{ij} = (m_{ij}, \mathcal{X}_{ij})$ </td></tr><tr><td> $Z$ </td><td>observation matrix of participants, i.e.  $z_{ij} \in Z$ </td></tr><tr><td> $u_i, \sigma_i$ </td><td>noise bias and deviation for the sensor of  $U_i$ </td></tr><tr><td> $\Psi$ </td><td>parameter set of sensor noise, i.e.  $(u_i, \sigma_i) \in \Psi$ </td></tr><tr><td> $\mathcal{X}_j, \mathcal{C}_j$ </td><td>the location and intensity of  $S_j$ </td></tr><tr><td> $\Theta$ </td><td>parameter set of pollution sources, i.e.  $(\mathcal{X}_j, \mathcal{C}_j) \in \Theta$ </td></tr><tr><td> $\nu_j$ </td><td>presence of  $S_j$ </td></tr><tr><td> $\vartheta$ </td><td>parameter set of source presences, i.e.  $\nu_j \in \vartheta$ </td></tr></table>

$$
Z = \{z _ {i j} | z _ {i j} = (m _ {i j}, \mathcal {X} _ {i j}), j = 1, 2 \dots M, i \in \mathbb {U} _ {j} \}, \tag {7}
$$

where $\mathbb { U } _ { j }$ is the subset of the participants, reporting the observations about the jth pollution source. Note that, each pollution source is reported by only portion of participants, due to the roaming behavior of the participants. Hence, we can get $0 < \parallel \mathbb { U } _ { j } \parallel \dot { \leq } N$ . Also, a participant can report more 0 k kthan one observation about the same pollution source. For ease of modeling, we only select the observation with the largest measurement value, as the accuracy of MLE improves with the increasing signal noise ratio (SNR) [19], and the larger measurement has higher SNR due to stable sensor noise model for the same participant.

The sensors of the participants are susceptible to the unknown measurement noise. As a result, it is vitally important to calibrate the sensors based on observation matrix only. Note that, the objective of sensor calibration is to estimate the sensor noise parameters for each participant, $\mathrm { i . e . , } u _ { i }$ and $\sigma _ { i }$ . Nevertheless, it is non-trivial to estimate these parameters, because there is no prior knowledge about the pollution sources, e.g., whether the pollution sources are present or not and where the locations are.

In this study, we will discuss and solve this sensor calibration problem. Specifically, only given the observation matrix $Z ,$ our objective is to estimate the sensor noise parameters C of N participants, so as to be consistent with this observation matrix, when both the source presences # and source parameters Q are previously unknown. This problem is formulated as follows:

$$
<   \hat {\Psi} > = \underset {<   \Psi , \vartheta , \Theta >} {\arg \max} P (Z | \Psi , \vartheta , \Theta), \tag {8}
$$

where sensor noise parameters $\Psi = \{ ( u _ { i } , \sigma _ { i } ) , i = 1 , 2 \ldots , N \}$ . Source presences $\bar { \vartheta } = \{ \nu _ { j } , j = 1 , 2 \ldots , M \} $ Þ ¼ 1 2 . . . g, nj denotes the ¼ f ¼ 1 2 . . .presence of the jth pollution source, $\nu _ { j } = 1 ( 0 )$ denotes the ¼ 1ð0Þjth pollution source is present (absent). Source parameters $\Theta \overset { \cdot } { = } \{ ( \mathcal { X } _ { j } , \mathcal { C } _ { j } ) , j = 1 , 2 \ldots , M \}$ .

¼ fðX C Þ ¼ 1 2 . . . gAccording to the literature [21], the probability of observations $P ( Z | \Psi , \vartheta , \Theta )$ in Eq. (8) can be quantified by the likejlihood of observations. Specifically, according to the law of total probability [22], the likelihood function of the observation matrix Z is given by:

$$
\begin{array}{l} L (Z | \Psi , \Theta) = \log \prod_ {j = 1} ^ {M} \prod_ {i \in \mathbb {U} _ {j}} p (z _ {i j} | \Psi , \Theta) \\ = \prod_ {j = 1} ^ {M} \prod_ {i \in \mathbb {U} _ {j}} \log \left[ p (z _ {i j} | S _ {j} ^ {t}) p (S _ {j} ^ {t}) + p (z _ {i j} | S _ {j} ^ {f}) p (S _ {j} ^ {f}) \right]. \tag {9} \\ \end{array}
$$

Our problem is to compute the optimal estimations of sensor noise to maximize the likelihood function $L ( Z | \Psi , \Theta )$ , which can be formulated as:

$$
<   \hat {\Psi} > = \underset {<   \Psi , \Theta >} {\arg \max} L (Z | \Psi , \Theta). \tag {10}
$$

# 3.2 Problem Transformation

It is worth noting that, maximizing the likelihood function in Eq. (10) is greatly difficult due to the ‘incomplete’ data, including three unknown parameters, i.e., source presences, source parameters and sensor noise. To address this problem, we transform the maximum likelihood estimation problem into the simple problem of maximizing expected likelihood function.

Specifically, inspired by EM method, we judiciously choose the source presences # as the latent variable, and the likelihood function based on the source presences is given by

$$
\begin{array}{l} L (Z | \vartheta , \Psi , \Theta) = \sum_ {j = 1} ^ {M} \left\{\nu_ {j} \times \sum_ {i \in \mathbb {U} _ {j}} \log \left[ p \left(z _ {i j} \mid S _ {j} ^ {t}\right) \right] \right. \\ \left. + (1 - \nu_ {j}) \times \sum_ {i \in \mathbb {U} _ {j}} \log \left[ p \left(z _ {i j} \mid S _ {j} ^ {f}\right) \right] \right\}. \\ \end{array}
$$

As the source presences # are unknown, we define the expected value of the likelihood $L ( Z | \vartheta , \Psi , \Theta )$ as follows:

Expected likelihood function, denoted by $\xi ( \vartheta , \Psi$ ; $\Theta , Z )$ on 1., is the expected value of the likelihood $L ( Z | \vartheta , \Psi , \Theta )$ , Þ ð j Þwith respect to the distribution of the source presences #. It is a function of #, C; Q and Z, and formulated as

$$
\begin{array}{l} \xi (\vartheta , \Psi , \Theta , Z) = E _ {\vartheta} [ L (Z | \vartheta , \Psi , \Theta) ] \\ = \sum_ {j = 1} ^ {M} \left\{p (\nu_ {j} = 1) \times \sum_ {i \in \mathbb {U} _ {j}} \log \left[ p (z _ {i j} | S _ {j} ^ {t}) \right] \right. \\ \left. + \left(1 - p \left(v _ {j} = 1\right)\right) \times \sum_ {i \in \mathbb {U} _ {j}} \log \left[ p \left(z _ {i j} \mid S _ {j} ^ {f}\right) \right] \right\}. \tag {12} \\ \end{array}
$$

![](images/f66b2161f2821586b233fa43a6faa962eb69a5f49c36eed07fef218f1e87660c.jpg)



Fig. 1. The framework of ACTION, sensor auto-calibration algorithm in two-level iteration. Note that, $\vartheta ^ { ( t ) } , \dot { \Psi } ^ { ( t ) }$ and $\Theta ^ { ( t ) }$ denote the estimations of the source presences, sensor noise and source parameters in the tth iteration respectively.

#; C and Q, $L ( Z | \Psi , \Theta ) \ge \xi ( \vartheta , \Psi , \Theta , Z )$ , where eorem 1. 8 8 8 ðthe equality holds if and only i $f p ( \vartheta ) = p ( \vartheta | Z , \Psi , \Theta )$ .

The proofs of Theorem 1 are presented in Appendix 1. According to Theorem 1, the expected likelihood function $\xi ( \vartheta , \Psi , \Theta , \overline { { Z } } )$ is the lower bound of the likelihood function $L ( Z | \Psi , \Theta )$ Þ. Thus, we have the following corollary, where ð j Þthe proofs are proposed in Appendix 2.

If there exist $\vartheta ^ { * } , \ \Psi ^ { * }$ and $\Theta ^ { * }$ , which maximize $\xi ( \vartheta , \Psi , \Theta , Z )$ , then, $L ( Z | \Psi ^ { * } , \Theta ^ { * } )$ also reaches the maximum.

According to Corollary 1, the sensor noise estimations $\Psi ^ { * }$ , which maximize the expected likelihood function $\xi ( \vartheta , \Psi , \Theta , Z )$ , will also maximize the likelihood function $L ( Z | \Psi , \Theta )$ Þ. As a result, we can make the following ð j Þconclusion.

: The complex problem of maximizing likelihood markfunction can be transformed into the maximizing expected likelihood problem. Formally,

$$
<   \hat {\Psi} > = \underset {<   \Psi , \vartheta , \Theta >} {\arg \max} \xi (\vartheta , \Psi , \Theta , Z). \tag {13}
$$

In the following sections, we will study how to estimate the sensor noise to maximize this expected likelihood function.

# 4 ACTION: SENSOR AUTO-CALIBRATION ALGORITHM IN TWO-LEVEL ITERATION

# 4.1 Overview of ACTION

To address the problem of maximizing the expected likelihood, we propose ACTION, a sensor Auto-Calibration algorithm in Two-level IteratiON. Through these two-level iterations, ACTION can gradually increase the expected likelihood of observations to the maximum, achieving optimal estimations of sensor noise. Specifically, as shown in Fig. 1, ACTION is mainly comprised of two-level iterations:

Outer Loop: The source presences are estimated based on the latest estimations of sensor noise and source parameters $( \mathrm { i . e . , } \Psi ^ { ( t - 1 ) }$ and $\Theta ^ { ( t - 1 ) } )$ . These estimation results $( \mathrm { i } . \mathrm { e } . , \vartheta ^ { ( t ) } )$ are fed back to re-estimate the sensor noise and the source parameters in the inner loop. These two steps are executed iteratively until the expected likelihood of observations converges.   
Inner Loop: Given the source presence estimations $( \mathrm { i . e . , ~ } \vartheta ^ { ( t ) } )$ , we alternately estimate the sensor noise $( \mathrm { i } . \mathrm { e } . , \Psi ^ { ( k ) } )$ and the source parameters $( \mathrm { i } . \mathrm { e } . , \Theta ^ { ( k ) } )$ based

on each other, until the expected likelihood of observations converges.

In these two-level iterations, ACTION consists of three basic components, namely, estimating source presences, sensor noise and source parameters. In the following, we first specify the method of estimating source presences in the outer loop and that of estimating sensor noise and source parameters in the inner loop. Afterwards, we present the algorithm description of ACTION, followed by the theoretical analysis of its convergence and optimality.

# 4.2 Estimating Source Presences (Outer Loop)

According to Theorem 1, the likelihood function $L ( Z | \Psi , \Theta )$ ð j Þis the upper bound of the expected likelihood function $\xi ( \vartheta , \Psi , \Theta , \hat { Z } )$ . If given the sensor noise C and source paramð Þeters Q, the likelihood $L ( Z | \Psi , \Theta )$ is the maximum of the expected likelihood $\xi ( \vartheta , \Psi , \Theta , Z )$ Þ. Moreover, according to ð ÞTheorem 1, the expected likelihood equals this maximum when $p ( \vartheta ) = p ( \vartheta | Z , \Psi , \Theta )$ . Note that, $\bar { p } ( \vartheta | Z , \Psi , \Theta )$ denotes ð Þ ¼ ð j Þ ð jthe posterior probability of source presences #.

As a result, the basic idea of estimating source presences is that, the posterior probability of the source presences is considered as the estimation of the source presences.

Specifically, we take the tth iteration as an example. Let $\vartheta ^ { ( t ) }$ denote the estimation of source presences in the tth iteration, i.e., $\vartheta ^ { ( t ) } = \{ \vartheta _ { i } ^ { ( t ) } , j = 1 , 2 \ldots , \dot { M } \}$ , where $\vartheta _ { i } ^ { ( t ) }$ denotes ¼the estimation of $p ( \nu _ { j } = 1 )$ 1 2 . . . gin the tth iteration. $\Psi ^ { ( t - 1 ) }$ and $\Theta ^ { ( t - 1 ) }$ ð ¼ 1Þdenote the estimation of sensor noise C and source parameters Q in the $( t - 1 )$ th iteration respectively, i.e., $\begin{array} { r l } { \Psi ^ { ( t - 1 ) } = } & { { } \{ ( u _ { i } ^ { ( t - 1 ) } , \sigma _ { i } ^ { ( t - 1 ) } ) , i = 1 , 2 \ldots , N \} , \Theta ^ { ( \bar { t } - 1 ) } = \{ ( \stackrel { \triangledown } { \boldsymbol { \chi } } _ { i } ^ { ( t - 1 ) } , } \end{array}$ $\mathcal { C } _ { j } ^ { ( t - 1 ) } ) , j = \dot { 1 } , 2 \ldots , \dot { M } \}$ Þ; sði Þ  ¼ 1 2 . . .  g ¼ fðX j . According to Bayes’ theorem [23], C Þ ¼ 1 2 . . . gthe estimation of source presence in the tth iteration is

$$
\begin{array}{l} \vartheta_ {j} ^ {(t)} = p \left(\nu_ {j} = 1 | Z, \Psi^ {(t - 1)}, \Theta^ {(t - 1)}\right) \\ = \frac {p (Z , \Psi^ {(t - 1)} , \Theta^ {(t - 1)} | v _ {j} = 1) p (v _ {j} = 1)}{\sum_ {\tau = 0} ^ {\tau = 1} [ p (Z , \Psi^ {(t - 1)} , \Theta^ {(t - 1)} | v _ {j} = \tau) p (v _ {j} = \tau) ]} \tag {14} \\ = \left\{1 + \mathcal {F} (j, t) \left(\frac {1}{\vartheta_ {j} ^ {(t - 1)}} - 1\right) \right\} ^ {- 1}, \\ \end{array}
$$

where $\mathcal { F } ( j , t )$ denotes the ratio of $p ( Z , \Psi ^ { ( t - 1 ) } , \Theta ^ { ( t - 1 ) } | \nu _ { j } = 0 )$ to $p ( Z , \Psi ^ { ( \ell - 1 ) } , \Theta ^ { ( t - 1 ) } | \nu _ { j } = 1 )$ ð j ¼ 0Þ. According to Eqs. (1), (5) and ð(6), it is derived as

$$
\begin{array}{l} \mathcal {F} (j, t) = \frac {\prod_ {i \in \mathbb {U} _ {j}} p \left(z _ {i j} , \Psi^ {(t - 1)} , \Theta^ {(t - 1)} \mid v _ {j} = 0\right)}{\prod_ {i \in \mathbb {U} _ {j}} p \left(z _ {i j} , \Psi^ {(t - 1)} , \Theta^ {(t - 1)} \mid v _ {j} = 1\right)} \\ = \prod_ {i \in \mathbf {U} _ {j}} \exp \left\{\frac {1}{- 2 \left(\sigma_ {i} ^ {(t - 1)}\right) ^ {2}} \left[ \left(m _ {i j} - u _ {i} ^ {(t - 1)}\right) ^ {2} \right. \right. \tag {15} \\ \left. \left. - \left(m _ {i j} - \frac {\mathcal {C} _ {j} ^ {(t - 1)}}{\| \mathcal {X} _ {i j} - \mathcal {X} _ {j} ^ {(t - 1)} \| ^ {2}} - u _ {i} ^ {(t - 1)}\right) ^ {2} \right] \right\} \\ \end{array}
$$

In summary, according to Eqs. (14) and (15), we can compute the source presence estimations #ðtÞ (i.e., #ðtÞ #ðtÞ ; $\vartheta ^ { ( t ) } \ ( \mathrm { i . e . , } \ \vartheta ^ { ( t ) } = \{ \vartheta _ { i } ^ { ( t ) }$ ¼ f j j  ;  ; M ) based on the sensor noise estimations Cðt1Þ $\bar { \boldsymbol { j } } = 1 , 2 \dots , M \} )$ $\dot { \Psi } ^ { ( t - 1 ) }$ ¼ 1 2 . . . gand the source parameter estimations Qðt1Þ . $\Theta ^ { ( t - 1 ) }$

# 4.3 Estimating Sensor Noise and Source Parameters (Inner Loop)

In the inner loop, we compute the new estimations of sensor noise $\Psi ^ { ( t ) }$ and source parameters $\Theta ^ { ( t ) }$ based on the source presence estimations $\dot { \vartheta } ^ { ( t ) }$ , so as to maximize the expected likelihood function as follows:

$$
\begin{array}{l} \xi \big (\Psi , \Theta , Z | \vartheta^ {(t)} \big) = \sum_ {j = 1} ^ {M} \sum_ {i \in \mathbb {U} _ {j}} \left\{\frac {\vartheta_ {j} ^ {(t)} \cdot (m _ {i j} - \mathbb {C} _ {j} (\mathcal {X} _ {i j}) - u _ {i}) ^ {2}}{- 2 \sigma_ {i} {} ^ {2}} \right. \\ \left. + \frac {\left(1 - \vartheta_ {j} ^ {(t)}\right) \left(m _ {i j} - u _ {i}\right) ^ {2}}{- 2 \sigma_ {i} {} ^ {2}} - \log \left(\sqrt {2 \pi} \sigma_ {i}\right) \right\}. \tag {16} \\ \end{array}
$$

It is difficult to directly maximize the expected likelihood function in $\operatorname { E q . }$ (16). To address this problem, we utilize an iterative method to achieve the maximum expected likelihood.

Specifically, we take the kth iteration as an example. In the first place, we estimate the sensor noise $\Psi ^ { ( k ) }$ based on the latest estimations of source parameters $\Theta ^ { ( k - 1 ) }$ . And then, based on these estimation results $\Psi ^ { ( k ) }$ , we re-estimate the source parameters $\Theta ^ { ( k ) }$ . In the following, we will present these two steps in detail.

# 4.3.1 Estimating Sensor Noise

Given the source parameter estimations $\Theta ^ { ( k - 1 ) }$ , we calculate the new estimations of sensor noise $\begin{array} { c c } { { \Psi ^ { ( k ) } } } & { { ( \mathrm { i . e . , } } } \end{array} \Psi ^ { ( k ) } =$ $\{ ( u _ { i } ^ { ( k ) } , \sigma _ { i } ^ { ( k ) } ) , i = 1 , 2 \dots , N \} )$ ð Þ ð Þ ¼, which maximize the expectafð i  i Þ ¼ 1 2 . . . tion likelihood function $\xi ( \Psi , Z | \vartheta ^ { ( t ) } , \Theta ^ { ( k - 1 ) } )$ . Then, we have

$$
\left. \frac {\partial \xi (\Psi , Z | \vartheta^ {(t)} , \Theta^ {(k - 1)})}{\partial u _ {i}} \right| _ {(u _ {i} ^ {(k)}, \sigma_ {i} ^ {(k)})} = 0 \tag {17}
$$

$$
\left. \frac {\partial \xi (\Psi , Z | \vartheta^ {(t)} , \Theta^ {(k - 1)})}{\partial \sigma_ {i}} \right| _ {\left(u _ {i} ^ {(k)}, \sigma_ {i} ^ {(k)}\right)} = 0. \tag {18}
$$

As only the sensor noise C are unknown in Eqs. (17) and (18), it is easy to solve these partial differential equations. Thus, the estimations for sensor noise (i.e., $\Psi ^ { ( k ) } \stackrel { * } { = } \{ ( u _ { i } ^ { ( k ) }$ $\sigma _ { i } ^ { ( k ) } ) , i = 1 , 2 \dots , N \} )$ are derived as

$$
u _ {i} ^ {(k)} = \frac {1}{J _ {i}} \sum_ {j \in \mathbb {S} _ {i}} \left\{m _ {i j} - \frac {\mathcal {C} _ {j} ^ {(k - 1)} \vartheta_ {j} ^ {(t)}}{\left\| \mathcal {X} _ {i j} - \mathcal {X} _ {j} ^ {(k - 1)} \right\| ^ {2}} \right\} \tag {19}
$$

$$
\begin{array}{l} \left(\sigma_ {i} ^ {(k)}\right) ^ {2} = \frac {1}{J _ {i}} \sum_ {j \in \mathbb {S} _ {i}} \left\{\left(1 - \vartheta_ {j} ^ {(t)}\right) \left(m _ {i j} - u _ {i} ^ {(k)}\right) ^ {2} \right. \\ \left. + \vartheta_ {j} ^ {(t)} \left(m _ {i j} - \frac {\mathcal {C} _ {j} ^ {(k - 1)}}{\| \mathcal {X} _ {i j} - \mathcal {X} _ {j} ^ {(k - 1)} \| ^ {2}} - u _ {i} ^ {(k)}\right) ^ {2} \right\}, \tag {20} \\ \end{array}
$$

where $\mathbb { S } _ { i }$ denotes the subset of the pollution sources, reported by the ith participant, and $J _ { i }$ denotes the set size of $\mathbb { S } _ { i } , \mathrm { i . e . , } J _ { i } = \parallel \mathbb { S } _ { i } \parallel$ .

# 4.3.2 Estimating Source Parameters

Given the sensor noise estimations $\Psi ^ { ( k ) }$ , we need to comer estimations , which maxim $\Theta ^ { ( k ) } \left( \mathrm { i . e . , } \Theta ^ { ( k ) } = \right.$ $\{ ( \mathcal { C } _ { j } ^ { ( k ) } , \mathcal { X } _ { j } ^ { ( k ) } ) , j = 1 , \dot { 2 } \dots , N \}$ sensor noise are known, this expected likelihood function can be simplified to

$$
\xi_ {1} (Z, \Theta | \vartheta^ {(t)}, \Psi^ {(k)}) = \sum_ {j = 1} ^ {M} \sum_ {i \in \mathbb {U} _ {j}} \left\{\frac {\vartheta_ {j} ^ {(t)} \cdot \left[ m _ {i j} - \frac {\mathcal {C} _ {j}}{\| \mathcal {X} _ {i j} - \mathcal {X} _ {j} \| ^ {2}} - u _ {i} ^ {(k)} \right] ^ {2}}{- 2 \left(\sigma_ {i} ^ {(k)}\right) ^ {2}} \right\}. \tag {21}
$$

Since only the source parameters are unknown in Eq. (21), it is simple to maximize this likelihood function. There are numerous approaches [20], [24] in solving this non-linear optimization problem. We leverage the simulated annealing algorithm [24] to compute the source parameter estimations QðkÞ $\Theta ^ { ( k ) }$ for higher computational efficiency.

# 4.4 Algorithm Description of ACTION

The algorithm of ACTION is described in Algorithm 1. First of all, the source presences, sensor noise and source parameters are initialized in line 1. The experiments in Section 5.3.5 show that, the initial values make a slight influence on the calibration accuracy, owing to the convergence of this algorithm.

Algorithm 1 ACTION: Sensor Auto-Calibration Algorithm in Two-level Iteration

# Input:

Observation matrix of participants:

$$
Z = \left\{\left(m _ {i j}, \mathcal {X} _ {i j}\right), j = 1, 2 \dots M, i \in \mathbb {U} _ {j} \right\}
$$

# Output:

Sensor noise estimations:

$$
\hat {\Psi} = \left\{\left(\hat {u} _ {i}, \hat {\sigma} _ {i}\right), i = 1, 2 \dots N \right\}
$$

1: Initialize $\vartheta , \Psi$ and Θ by $\vartheta ^ { ( 0 ) } , \Psi ^ { ( 0 ) }$ and $\Theta ^ { ( 0 ) }$ respectively;   
2:while $\xi ( \vartheta ^ { ( t - 1 ) } , \Psi ^ { ( t - 1 ) } , \Theta ^ { ( t - 1 ) } )$ does not converge do   
3: Compute $\vartheta ^ { ( t ) }$ using $\Psi ^ { ( t - 1 ) }$ and $\Theta ^ { ( t - 1 ) }$ ，according to Eq.14 and 15;   
4:while $\xi \big ( \Psi ^ { ( k - 1 ) } , \mathsf { \dot { \Theta } } ^ { ( k - 1 ) } | \vartheta ^ { ( t ) } \big )$ does not converge do   
5: Compute $\Psi ^ { ( k ) }$ using $\boldsymbol { \vartheta } ^ { ( t ) }$ and $\Theta ^ { ( k - 1 ) }$ ,according to Eq.19 and 20;   
6: Compute $\Theta ^ { ( k ) }$ using $\vartheta ^ { ( t ) }$ and $\Psi ^ { ( k ) }$ ， according toEq.21；  
7: $k \stackrel { - } { = } k + 1 ;$   
8:end while   
9:Let $\Psi ^ { ( t ) } , \Theta ^ { ( t ) }$ = converged values of $\Psi ^ { ( k ) }$ and $\Theta ^ { ( k ) }$ respectively;   
$t = t + 1 ;$   
11: end while   
12:Let $\hat { \Psi } =$ converged values of $\Psi ^ { ( t ) } ;$   
13: return $\hat { \Psi } = \{ ( \tilde { \hat { u _ { i } } } , \hat { \sigma } _ { i } ) , i = 1 , 2 \ldots , N \} ;$

After that, ACTION algorithm is primarily comprised of two-level iterations. In the outer loop, source presences are estimated based on the latest estimations of sensor noise and source parameters in line 3. Afterwards, based on these estimation results, the sensor noise and source parameters are re-estimated in the inner loop in line 4-8. It is noted that, we use the simulated annealing solver of Matlab toolbox [25] to solve the nonlinear optimization of Eq. (21) in line 6. After the convergence of the inner loop, the converged values of sensor noise estimation and source parameter estimation are considered as their new estimations of the outer loop in line 9. After the convergence of the outer loop, in line 12-13, the converged values of the sensor noise estimation are considered as the optimal estimations of sensor noise, i.e., u and ${ \hat { \sigma } } _ { i }$ .

^The time complexity of our algorithm is $O ( N \cdot M \cdot T \cdot K )$ , ð 
 
 
 Þwhere N; M; T and K are the number of the participants, the pollution sources, the outer iterations and the inner iterations respectively. The experiments in Section 5.2 show that, the number of the outer iterations and the inner iterations are both significantly small. Further more, we make experiments to evaluate the time complexity in Appendix 4. The experiment results show that, the execution time of our algorithm increases approximately linearly with the number of participants and pollution sources.

# 4.5 Convergence and Optimality Analysis

In this section, we analyze the convergence and optimality of ACTION algorithm in terms of two-level iterations. Firstly, we analyze the convergence of the inner loop, and get the following conclusion, where the detailed analysis is proposed in Appendix 3.

The inner loop of ACTION increases the expected emark:likelihood gradually to the maximum, if given the source presences.

And then, we discuss the convergence and optimality of the outer loop. According to Theorem 1, we can have the following corollary easily, and the simple proofs are omitted.

Given $\Psi ^ { ( t - 1 ) } , \Theta ^ { ( t - 1 ) }$ and $Z ,$ the expected likelihood orollary function $\xi ( \vartheta , \Psi ^ { ( t - 1 ) } , \Theta ^ { ( \dot { t } - 1 ) } , Z )$ is maximized if and only if $\mathbf { \boldsymbol { p } } ( \vartheta ) = \boldsymbol { p } ( \vartheta | Z , \boldsymbol { \Psi } ^ { ( t - 1 ) } , \boldsymbol { \Theta } ^ { ( t - 1 ) } )$ .

As we leverage the posterior probability of the source presences to estimate the source presences in the first step, according to Corollary 2, the expected likelihood is maximized in the first step, when given the estimations of source parameters and sensor noise.

In the second step, based on the estimation results of source presences, the source parameters and sensor noise are re-estimated by the iterative method of the inner loop. According to the above analysis of the inner loop, the expected likelihood is also maximized, when given the source presence estimations.

In summary, the expected likelihood is increasing step by step in each iteration of the outer loop. As the observation matrix is known and determinate, its maximum expected likelihood exists. As a result, the outer loop can converge to the maximum expectation likelihood of observations. According to Corollary 1, the solution maximizing the expected likelihood function will maximize the likelihood function. Thus, we have the following conclusion.

ACTION can converge to the optimal estimations mark:of sensor noise, where the likelihood of observations is maximized.

# 5 EVALUATIONS

We conduct extensive simulations to evaluate ACTION in this section. First, we introduce the scenario and settings of these simulations. And then, in the following two sections, we evaluate the performance of ACTION, including the convergence of two-level iterations as well as the estimation precision of sensor noise.

# 5.1 Simulation Scenario and Settings

We simulate a medium-scale participatory sensing scenario to identify the present pollution sources. Specifically, M pollution sources are randomly distributed in the square region of . The intensity of the 2000  2000 mpollution sources changes randomly from $2 \times 1 0 ^ { 5 }$ to $\bar { 6 } \times 1 0 ^ { 5 }$ 2  10counts-per-minute (CPM), which are consistent 6  10with the settings of low-level radioactive pollution source [8]. Each pollution source is present with the probability $P _ { p } ,$ named as present probability. We set the maximum radius of the detection area to , where the pollution 150 msources can be reported by the participants. N participants join in this participatory sensing. A participant arrives in the detection area of certain pollution source and makes an observation at a random location, according to the probability $P _ { o }$ called observable probability. The observation includes the measurement of concentration as well as its location. The measurement consists of the diffusion concentration of the pollution source and sensor noise of the participant. The bias and deviation of sensor noise for each participant vary randomly from 50 to 100 CPM, and from 10 to 20 CPM respectively [7].

In order to validate the performance of our approach, we compare it with three baseline methods. Specially, the first kind, including ML-H1 and ML-H0, does not take account into whether the pollution sources is present or not. They directly estimate the sensor noise using MLE, based on the assumption H the pollution sources are 1present in ML-H1, and the assumption H the pollution 0sources are absent in ML-H0. In the other kind, it considers the source presences while ignoring the influence of source parameters on sensor noise estimation, and we call it EM-TS. More specifically, EM-TS method has one-level iteration [26]. The parameters of the pollution sources are estimated first, followed by estimating source presences and estimating sensor noise iteratively based on EM method as ACTION. The simulation programs are written in Matlab. All the simulations are executed for 100 times and we get the average values.

# 5.2 Convergence of Two-Level Iterations

In the first experiment, we validate the convergence of twolevel iterations in ACTION. The number of the pollution sources $( \mathrm { i . e . , } M )$ is 30, and the present probability $P _ { p }$ is 0.6. Also, the number of the participants (i.e., N) is 60, and the observable probability $P _ { o }$ is 0.6. The maximum number of the outer loop is set to 15.

First, we analyze the expected likelihood value verse each step of two-level iterations, including source presence estimation, source parameter estimation and sensor noise estimation. As shown in Fig. 2a, the expected likelihood value increases with two-level iterations. The reason behind it is that, the source presences are estimated based on the parameter estimations of the pollution sources and sensor noise in the outer loop. Likewise, the estimation results are fed back to re-fine the previous estimations of the pollution sources and sensor noise alternately in the inner loop. As a result, both source presence estimation and source parameter estimation play an important role in sensor noise estimation. Moreover, the expected likelihood value increases rapidly in the first two iterations of the outer loop, and both the outer loop and the inner loop converge fast. ACTION converges after 11 iterations of the outer loop, and the number of iterations in the inner loop is less than 3.

![](images/632c766ec8f307c063eff0a53bc820c5b45be7c17468f7d113a6ab5280811493.jpg)



(a) Performance of each step

![](images/989c1618d8beb1f6561bbb2b6e08ac10728dfce4cf10cc9d341198d6d45d3bbe.jpg)



(b)Robustness of initial settings

![](images/9bd3c14f2981beb4afd9e0a86d1d71ba90c66698997d8d18962efdd26c3606de.jpg)



(c) Influence of location errors

Fig. 2. a) Expected likelihood verse three steps of two-level iterations. b) Estimation errors of sensor noise verse the initial settings of source presences. c) The concentration measurement errors verse the location errors of sensors.   
![](images/7b7e631f5284542d600e0d68f775d4cf4fb86a22afbbad17c62d08a8833d31b7.jpg)



(a) Source presences

![](images/2167fd776dc6ec3b70a4ea1e08b002de1e3a6d3a91b838fcf4e6653bb976ca1e.jpg)



(b) Sensor noise

![](images/e8215905fbf65cbd605b1b7611c2872d421adce3ed9c9e10df53b58433cdb6db.jpg)



(c) Source parameters   
Fig. 3. Performance verse two-level iterations, in terms of the estimation errors of source presences, sensor noise and source parameters.

Second, we analyze the performance of ACTION verse each iteration, in terms of the estimation error of source presences, source parameters and sensor noise. As shown in Fig. 3a, the false negative rate of identifying the present pollution sources decreases with the iteration of the outer loop, while its false positive rate is zero from beginning to end and we do not plot it. Thus, the iteration of the outer loop can gradually improve the estimation accuracy of source presences. Similarly, as shown in Figs. 3b and 3c, the estimation precision of sensor noise and source parameter increases with two-level iterations.

# 5.3 Estimation Precision of Sensor Noise

In this section, compared with three baseline methods, we evaluate our estimation precision of sensor noise in terms of five different aspects, including the observable probability of participants, the number of participants, the present probability of pollution sources, the number of pollution sources, and the initial settings. The experimental settings are the same to the previous experiment. We take the following two metrics for the estimation precision of sensor noise, i.e., the average value of the relative bias error (RBE) and that of the relative deviation error (RDE) for all the participants.

# 5.3.1 Observable Probability of Participants

The observable probability $P _ { o }$ of the participants varies from 0.3 to 0.9 uniformly. As shown in Figs. 4a and 4b, ACTION outperforms three baseline methods in term of both noise bias estimation and noise deviation estimation. ACTION improve the RBE up to 20 percent and the RDE up to 31 percent, compared with the best performance of three baseline methods. Further, the performance of ACTION changes slightly with the observable probability of the participants, and achieves a high estimation accuracy even when the observable probability of the participants is low.

![](images/2571f9604177279d55e21ebdfada1db1fe69ed82ac993d114c8045e8e7538801.jpg)



(a) Noise bias

![](images/12fe8eb69d205c7c4af54f2eb1265d0814e59e3401db4e7dd7ea345e9b4058f9.jpg)



(b) Noise deviation   
Fig. 4. Estimation error of sensor noise verse the observable probability of participants.

![](images/e6fbf8ec2e0e9f8f24504219a9e153de53db92779557179ab584d38071a57441.jpg)



(a) Noise bias

![](images/c10333d813e75aa9cc657d19683d5e14e252a9ad00742063095f6153e975165e.jpg)



(b) Noise deviation   
Fig. 5. Estimation error of sensor noise verse the number of participants.

# 5.3.2 The Number of Participants

The number of participants ranges from 20 to 90. As shown in Figs. 5a and 5b, ACTION performs better rather than three baseline methods in both noise bias estimation and noise deviation estimation. More specifically, ACTION improves the RBE up to 17 percent, and the RDE up to 29 percent in comparison with the optimal performance of three baseline methods.

# 5.3.3 Present Probability of Pollution Sources

The present probability of the pollution sources changes from 0.2 to 0.9. As shown in Figs. 6a and 6b, ACTION outperforms these baseline methods in noise estimation accuracy. Compared with their optimal performance, the improvements of the RBE and RDE are up to 22 and 31 percent respectively. What’s more, the precision of noise estimation decreases with the present probability of the pollution sources for all these four methods. The reasons are as follows. As ML-H0 is based on the assumption that all the pollution sources are false, the performance degrades when the present probability of the pollution sources increases. For ACTION, EM-TS and ML-H1, the noise estimation is dependent on the source parameter estimation. When the number of the present pollution sources becomes large, the precision of estimating source parameters gets worse, leading to the lower precision of noise estimation.

# 5.3.4 The Number of Pollution Sources

The number of the pollution sources changes from 10 to 45. As shown in Figs. 7a and 7b, ACTION achieves a better performance of noise estimation in comparison to three baseline methods. ACTION increases the RBE up to 19 percent, and RDE up to 29 percent, compared with the optimal performance of three baseline methods. Furthermore, our performance varies slightly with the number of pollution

![](images/035571ff1664fcba67f25e3504303f975d739cc4e1bc61c0cd7f40121e2fcc41.jpg)



(a) Noise bias

![](images/027049f7506655cdf5166c48a0272a042640ae9a115bb4c9bbca2c77c4d2b12c.jpg)



(b) Noise deviation   
Fig. 6. Estimation error of sensor noise verse the present probability of pollution sources.

![](images/9d8c78d3a754dc81cb627ff0260baf28c3adbb11e4df87f68b36e928ab0fe28c.jpg)



(a) Noise bias

![](images/4e0331b8f4043f058bc944c8c195055403fb0e6363cc4e6830d51ba98ec94d4f.jpg)



(b) Noise deviation   
Fig. 7. Estimation error of sensor noise verse the number of pollution sources.

sources. Hence, ACTION achieves a good performance even when there are few pollution sources.

# 5.3.5 The Initial Settings

In this section, we explore the impact of the initial settings on the calibration accuracy. We change the initial settings of source presences from 0.1 to 1. As shown in Fig. 2b, the estimation precision of sensor noise changes slightly with the initial settings of source presences. Thus, the initial settings have a slight influence on the calibration accuracy, due to the convergence of ACTION. The experimental results for the initial settings of source parameters and sensor noise are the similar to that of source presence. We do not show them due to the page limit.

# 6 DISCUSSION AND FUTURE WORK

In this section, we will discuss the impact of four influenced factors on the sensor calibration accuracy.

Time-varying Drift Error of Sensors. According to the experimental results in [12], the low-cost sensors have timevarying drift errors, requiring periodical calibration. Due to the property of ‘calibrate without calibrating’, our method can solve this problem well without periodically particular calibration. Specifically, in each time of implementing the pollution monitoring mission, our method can calibrate the sensors at the same time. Moreover, these drift errors are changing very slowly, e.g., there is a visible change only after one day [12]. Hence, it makes a slight influence on the calibration performance when several sensors are not available in a short time.

Participant mobility model. The mobility model of participants determines the spatial distribution of measurements, affecting the calibrating performance of sensors. Nevertheless, our method only inputs the observation matrix, and makes no assumption on the mobility model. Thus, the mobility model is not the focus of this paper. However, as the extension of our study, we will study the influence of the mobility model on the calibrating performance, including the different models (e.g., random walk model [27] and Manhattan model [28]), and the distribution of participants, etc. Also, we will collect the real mobility traces of participants (e.g., Dartmouth data set [29]) to evaluate the mobility models further.

Sampling Frequency of Sensors. Intuitively, when the sampling frequency is higher, the sampling data is more and the sensor calibration is more accurate. However, the experiment results in Section 5.3.1 show that, the calibration accuracy increases slightly with the number of sampling data. Thus, the sampling frequency makes a slight influence on the calibration accuracy. Moreover, the highly frequent sampling will consume large amount of energy, which is limited in the participatory sensing network. As a result, the sampling frequency is a tradeoff between the calibration accuracy and the energy cost. In the future work, we will explore the information share between the participants to achieve a good tradeoff, by avoiding the useless sampling, where there is no pollution source all around.

Error of sensor location. The sensor locations may have errors, such as GPS. We make a basic experiment to explore the impact of the location errors on our calibration accuracy. As shown in Fig. 2c, the location errors have no significant influence on the accuracy of the concentration measurement, compared with that of the sensor measurement noise. Note that, when the location error is 0 m, the errors of concentration measurement are dominated by the random sensor measurement noise. Thus, the small location errors (less than 10 ) make a slight impact on the calibration accuracy.

# 7 RELATED WORK

Current studies of sensor calibration focus on automatic calibration, and can mainly be classified into the cooperative calibration and uncooperative calibration.

In cooperative calibration methods [9], [10], [11], [12], [13], [14], researchers leverage the spatial correlation of measurements, i.e., the measurements change slightly within certain physical distance, and the sensors are calibrated by collaborating with the neighbor sensors or the ground-truth sensors . Many studies [10], [13], [14] consider the sensor calibration in static wireless sensor network, while several researches [9], [11], [12] take into account of the mobile sensor network. CaliBree [9] exploits the opportunistic encounter with the calibrated sensors to calibrate the mobile sensors. Similarly, Tsujita et al. [11] use the average measurements of encountered sensors to be the calibrated values. As the measurement errors of the sensors are different from each other, it is greatly inaccurate to average the measurement as the calibrated values. To address this problem, Xiang et al.[12] propose an optimal collaborative calibration algorithm to compute the optimal weight for each sensor. The above methods are based on the assumptions that, the sensors can collaborate with each other and the ground-truth sensors are easily available. However, in participatory sensing, it is difficult to make the uncontrollable participants cooperate for calibration. Further, the expensive, ground-truth sensors are often unaffordable in a large-scale deployment. In contrast, our approach calibrates the sensors without the collaboration of the participants and ground-truth sensors.

The uncooperative calibration approaches [16], [17], [30] integrate the measurements of all the sensors for calibration. Whitehouse and Culler [16] exploit the correlation between the sensors’ measurements and the measurement model parameters, formulating the calibration problem into a nonlinear function minimization problem. Tan et al. [17] propose a two-tier calibration approach, considering the limited energy and computing capability in the mobile sensors. In the first tier, each sensor makes local calibration to learn model parameters. And then, the head calibrates the model parameters of each sensor globally to maximize the sensing performance. All of them should need an explicit and particular calibration process, such as controlling the behaviors of the interesting sources. Nevertheless, this particular calibration process is difficult to be realized in participatory sensing network, owing to the uncooperative and uncontrollable participants. Our approach belongs to the uncooperative calibration method. Nevertheless, distinguished from these existing studies, our method calibrates the sensors in the process of monitoring pollution sources, without a particular and cooperative calibration process. Similar to ours, Balzano, etc., [30] blindly calibrate the sensors using routine sensor measurements. They employ the spatial over-sample of sensors to calibrate the static sensor network, yet it is difficult to be achieved for the uncontrollable participants.

# 8 CONCLUSION

In this paper, we study sensors calibration in the participatory sensing network, where the participants are uncooperative and uncontrollable. We calibrate the sensors in the process of monitoring pollution sources, without a particular and cooperative calibration process. Inspired by EM method, we propose a two-level iterations based sensor calibration algorithm, converging to an optimal estimations of sensor noise in the sense of maximum likelihood.

# APPENDIX

# 1.Proof of Theorem 1

According to the properties of the conditional probaoof.bility, we have

$$
\begin{array}{l} L (Z | \Psi , \Theta) = \ln p (Z | \Psi , \Theta) \\ = \ln p (Z | \vartheta , \Psi , \Theta) + \ln \frac {p (\vartheta)}{p (\vartheta | Z , \Psi , \Theta)}. \tag {22} \\ \end{array}
$$

We compute the expectations for both two sides of Eq. (22), with respect to the distribution of #. $\begin{array} { r } { \mathrm { A s } p ( Z | \Psi , \Theta ) } \end{array}$ is independent of #, $E _ { \vartheta } ( L ( Z | \Psi , \Theta ) ) = L ( Z | \Psi , \Theta )$ j Þ. Then, we have

$$
\begin{array}{l} L (Z | \Psi , \Theta) = E _ {\vartheta} \bigl (\ln p (Z | \vartheta , \Psi , \Theta) \bigr) + E _ {\vartheta} \left[ \ln \frac {p (\vartheta)}{p (\vartheta | Z , \Psi , \Theta)} \right] \\ = \xi (\vartheta , \Psi , \Theta , Z) + E _ {\vartheta} \left[ \ln \frac {p (\vartheta)}{p (\vartheta | Z , \Psi , \Theta)} \right]. \tag {23} \\ \end{array}
$$

$\begin{array} { r } { E _ { \vartheta } [ \ln \frac { p ( \vartheta ) } { p ( \vartheta | Z , \Psi , \Theta ) } ] } \end{array}$ is Kullback-Leibler divergence of $p ( \vartheta | Z ,$ ; $\Psi , \Theta )$ ½ln ð jfrom $p ( \vartheta )$ Þ ð jin information theory [31]. According to Þ ð ÞInformation Inequality[32], it is non-negative, and equals to zero if and only if $p ( \vartheta ) = p ( \vartheta | Z , \Psi , \Theta )$ . Thus, according to Eq. (23), we have $L ( Z | \Psi , \Theta ) \ge \xi ( \vartheta , \Psi , \Theta , Z ) .$ , and the ð jequality holds if and only if $\mathrm { \dot { \cdot } } p ( \vartheta ) = p ( \vartheta | Z , \Psi , \Theta )$ Þ. □

# 2. Proof of Corollary 1

We use the method of proof by contradiction. More oof.specifically, we assume the conclusion is not true, namely, $\overset { \cdot } { L } ( Z | \Psi ^ { * } , \Theta ^ { * } )$ is not the maximum. Thus, there exist $\Psi ^ { 0 }$ and $\Theta ^ { 0 } \quad ( \Psi ^ { 0 } \neq \Psi ^ { * }$ and $\Theta ^ { 0 } \neq \Theta ^ { * } )$ , where $L ( Z | \Psi ^ { 0 } , \Theta ^ { 0 } ) > L ( Z | \Psi ^ { * } , \Theta ^ { * } )$ ¼. We let $p ( \vartheta ^ { 0 } ) = p ( \vartheta | Z , \Psi ^ { 0 } , \Theta ^ { 0 } )$ . ð j Þ ð j Þ ðAccording to Theorem 1, we have $L ( Z | \Psi ^ { 0 } , \Theta ^ { 0 } ) = \xi ( \vartheta ^ { 0 }$ ; $\Psi ^ { 0 } , \Theta ^ { 0 } , \check { Z } ) , \mathrm { a n d } L ( Z | \Psi ^ { * } , \Theta ^ { * } ) \ge \xi ( \vartheta ^ { * } , \Psi ^ { * } , \Theta ^ { * } , Z ) .$ ¼ ð. Then, $\xi ( \vartheta ^ { 0 } , \Psi ^ { 0 } , \Theta ^ { 0 } , Z ) > \xi ( \vartheta ^ { \ast } , \Psi ^ { \ast } , \Theta ^ { \ast } , Z ) . \xi ( \vartheta ^ { \ast } , \Psi ^ { \ast } , \Theta ^ { \ast } , Z )$ is not ð Þ ð Þ ð Þthe maximum, which contradicts with the given conditions of Corollary 1. As a result, Corollary 1 is true. □

![](images/24f9a4e47c2ea347f403eb580c50d5643739e23b2656b9e88e5aa572a6a032a7.jpg)



(a) The number of participants

![](images/4f8cb0d1a1645fa4d3b94b09351e8d437e372c8dea1a57229dfad52336451684.jpg)



(b) The number of pollution sources   
Fig. 8. Execution time of our algorithm verse the number of participants and pollution sources.

# 3. Convergence Analysis of Inner Loop

Convergence Analysis of Inner LoopWe analyze the convergence of the inner loop, and take the kth iteration for example. The expected likelihood is initially $\xi ( \Psi ^ { ( k - 1 ) } , \Theta ^ { ( k - 1 ) } , Z | \vartheta ^ { ( \hat { t } ) } )$ . Each iteration of the inner loop ð j Þincludes two steps, i.e., estimating sensor noise and estimating source parameters.

In the estimating sensor noise, the sensor noise estimations $\Psi ^ { ( k ) }$ are computed according to Eqs. (19) and (20), maximizing the expected likelihood $\xi \dot { ( \Psi , Z | \vartheta ^ { ( t ) } , \Theta ^ { ( k - 1 ) } ) }$ . Hence, we have

$$
\xi \big (\Psi^ {(k - 1)}, \Theta^ {(k - 1)}, Z | \vartheta^ {(t)} \big) \leq \xi \big (\Psi^ {(k)}, \Theta^ {(k - 1)}, Z | \vartheta^ {(t)} \big). \tag {24}
$$

In the estimating source parameters, the source parameter estimations $\Theta ^ { ( k ) }$ are computed by solving the optimization problem of maximizing the likelihood function $\xi _ { 1 } \big ( Z , \hat { \Theta } | \vartheta ^ { ( t ) } , \Psi ^ { ( k ) } \big )$ . Thus, we have $\xi _ { 1 } ( Z , \Theta ^ { ( k - 1 ) } | \vartheta ^ { ( t ) } , \Psi ^ { ( k ) } ) \leq$ $\xi _ { 1 } ( Z , \Theta ^ { ( k ) } | \vartheta ^ { ( t ) } , \Psi ^ { ( k ) } ,$ . Then, we have

$$
\xi \big (\Psi^ {(k)}, \Theta^ {(k - 1)}, Z | \vartheta^ {(t)} \big) \leq \xi \big (\Psi^ {(k)}, \Theta^ {(k)}, Z | \vartheta^ {(t)} \big). \tag {25}
$$

Note that, in Eqs. (24) and (25), the equality holds only when the expected likelihood reaches the maximum. According to Eqs. (24) and (25), the expected likelihood increases with the iteration. As a result, we can make the conclusion as in Section 4.5.

# 4. Experimental Analysis of Time Complexity

Experimental Analysis of Time ComplexityWe make simulations to evaluate the time complexity of our algorithm in a Dell computer with Win7 Intel Core i3 processor (3.3 GHZ) and 2 GB RAM. Firstly, we change the number of participants from 100 to 900, and set the number of pollution sources 20. As shown in Fig. 8a, the execution time of our algorithm increases roughly linearly with the number of participants. Similarly, we vary the number of pollution sources from 10 to 120, and set the number of participants 200. As shown in Fig. 8b, the execution time also grows approximately linearly with the number of pollution sources. Moreover, the number of pollution sources makes a more significant influence on the execution time, rather than that of participants. In sum, the time complexity of our algorithm increases approximately linearly with the number of participants and pollution sources.

# REFERENCES

[1] R.K. Ganti, F. Ye, and H. Lei, “Mobile Crowdsensing: Current State and Future Challenges,” IEEE Comm. Magazine, vol. 49, no. 11, pp. 32-39, Nov. 2011.   
[2] J. Burke, D. Estrin, M. Hansen, A. Parker, N. Ramanathan, S. Reddy, and M. Srivastava, “Participatory Sensing,” Proc. ACM Sensys Workshop World-Sensor-Web (WSW), 2006.   
[3] N.D. Lane, E. Miluzzo, H. Lu, D. Peebles, T. Choudhury, and A.T. Campbell, “A Survey of Mobile Phone Sensing,” IEEE Comm. Magazine, vol. 48, no. 9, pp. 140-150, Sept. 2010.   
[4] R. Rana, C. Chou, S. Kanhere, N. Bulusu, and W. Hu, “Ear-Phone: An End-to-End Participatory Urban Noise Mapping System,” Proc. ACM/IEEE Ninth Int’l Conf. Information Processing in Sensor Networks (IPSN), pp. 105-116, 2010.   
[5] M. Faulkner, M. Olson, R. Chandy, J. Krause, K.M. Chandy, and A. Krause, “The Next Big One: Detecting Earthquakes and Other Rare Events from Community-Based Sensors,” Proc. 10th Int’l Conf. Information Processing in Sensor Networks (IPSN), pp. 13-24, 2011.   
[6] W. Willett, P. Aoki, N. Kumar, S. Subramanian, and A. Woodruff, “Common Sense Community: Scaffolding Mobile Sensing and Analysis for Novice Users,” Pervasive Computing, vol. 6030, pp. 301-318, 2010.   
[7] J.-C. Chin, D.K.Y. Yau, N.S. Rao, Y. Yang, C.Y.T. Ma, and M. Shankar, “Accurate Localization of Low-Level Radioactive Source Under Noise and Measurement Errors,” Proc. ACM Sixth Conf. Embedded Network Sensor Systems (Sensys), 2008.   
[8] J.-C. Chin, N.S. Rao, D.K.Y. Yau, M. Shankar, Y. Yang, J.C. Hou, and S.Srivathsan, S. Iyengar, “Identification of Low-Level Point Radioactive Sources Using a Sensor Network,” ACM Trans. Sensor Networks, vol. 7, no. 3, pp. 1-35, 2010.   
[9] E. Miluzzo, N. Lane, A. Campbell, and R. Olfati-Saber, “CaliBree: A Self-Calibration System for Mobile Sensor Networks,” Proc. IEEE Fourth Int’l Conf. Distributed Computing in Sensor Systems (DECOSS), pp. 314-331, 2008.   
[10] V. Bychkovskiy, S. Megerian, D. Estrin, and M. Potkonjak, “A Collaborative Approach to In-Place Sensor Calibration,” Proc. Second Int’l Conf. Information Processing in Sensor Networks (IPSN), pp. 556-556, 2003.   
[11] W. Tsujita, H. Ishida, and T. Moriizumi, “Dynamic Gas Sensor Network for Air Pollution Monitoring and its Auto-Calibration,” Proc. IEEE Sensors, pp. 56-59, 2004.   
[12] Y. Xiang, L. Bai, R. Piedrahita, R.P. Dick, Q. Lv, M. Hannigan, and L. Shang, “Collaborative Calibration and Sensor Placement for Mobile Sensor Networks,” Proc. 11th Int’l Conf. Information Processing in Sensor Networks (IPSN), pp. 73-84, 2012.   
[13] J. Feng, S. Megerian, and M. Potkonjak, “Model-Based Calibration for Sensor Networks,” Proc. IEEE Sensors, pp. 737-742, 2003.   
[14] R. Tan, G. Xing, X. Liu, J. Yao, and Z. Yuan, “Adaptive Calibration for Fusion-Based Wireless Sensor Networks,” Proc. IEEE INFOCOM, pp. 1-9, 2010.

[15] W. Khan, Y. Xiang, M. Aalsalem, and Q. Arshad, “Mobile Phone Sensing Systems: A Survey,” IEEE Comm. Surveys and Tutorials, vol. 15, no. 1, pp. 402-427, First Quarter, 2013.   
[16] K. Whitehouse and D. Culler, “Calibration as Parameter Estimation in Sensor Networks,” Proc. ACM Workshop Wireless Sensor Networks and Applications, pp. 59-67, 2002.   
[17] R. Tan, G. Xing, Z. Yuan, X. Liu, and J. Yao, “System-Level Calibration for Fusion-Based Wireless Sensor Networks,” Proc. IEEE 31st Real-Time Systems Symposium (RTSS), pp. 215-224, 2010.   
[18] A. Dempster, N. Laird, and D. Rubin, “Maximum Likelihood From Incomplete Data via the EM Algorithm,” J. Royal Statistical Soc. Series B, vol. 39, no. 1, pp. 1-38, 1977.   
[19] Y. Wang, R. Tan, G. Xing, and X. Tan, “Accuracy-Aware Aquatic Diffusion Process Profiling Using Mobile Sensor Networks,” Proc. 11th Int’l Conf. Information Processing in Sensor Networks (IPSN), pp. 1-12, 2012.   
[20] A. Krause, “SFO: A Toolbox for Submodular Function Optimization,” J. Machine Learning Research, vol. 11, pp. 1141-1144, 2010.   
[21] D. Wang, T. Abdelzaher, and L. Kaplan, “On Truth Discovery in Social Sensing: A Maximum Likelihood Estimation Approach,” Proc. 11th Int’l Conf. Information Processing in Sensor Networks (IPSN), 2012.   
[22] D. Zwillinger and S. Kokoska, CRC Standard Probability and Statistics Tables and Formulae. CRC Press, 1999.   
[23] B.P. Carlin and T.A. Louis, “Bayes and Empirical Bayes Methods for Data Analysis,” Statistics and Computing, vol. 7, no. 2, pp. 153- 154, 1997.   
[24] S. Kirkpatrick, C.D. Gelatt Jr., and M.P Vecchi, “Optimization by Simulated Annealing,” Science, vol. 220, no. 4598, pp. 671-680, 1983.   
[25] Global Optimization Toolbox, http://www.mathworks.cn/cn/ products/global-optimization/description7.html, 2014.   
[26] C. Xiang, P. Yang, C. Tian, Y. Yan, X. Wu, and Y. Liu, “PassFit: Participatory Sensing and Filtering for Identifying Truthful Urban Pollution Sources,” IEEE Sensors J., vol. 13, no. 10, pp. 3721-3732, Oct. 2013.   
[27] B. Han and A. Srinivasan, “Your Friends Have More Friends Than You Do: Identifying Influential Mobile Users through Random Walks,” Proc. ACM Mobihoc, 2012.   
[28] F. Bai, N. Sadagopan, and A. Helmy, “The Important Framework for Analyzing The Impact of Mobility on Performance of Routing Protocols for Adhoc Networks,” Ad Hoc Networks, vol. 1, no. 4, pp. 383-403, 2003.   
[29] D. Kotz, T. Henderson, I. Abyzov, and J. Yeo, “CRAWDAD Trace Set dartmouth/campus/movement (v. 2005-03-08),” http:// crawdad.cs.dartmouth.edu/dartmouth/campus/movement, 2005.   
[30] L. Balzano and R. Nowak, “Blind Calibration of Sensor Networks,” Proc. Sixth Int’l Symp. Information Processing in Sensor Networks (IPSN), pp. 79-88, 2007.   
[31] S. Kullback and R.A. Leibler, “On Information and Sufficiency,” The Annals of Math. Statistics, vol. 22, no. 1, pp. 79-86, 1951.   
[32] T.M. Cover and J.A. Thomas, Elements of Information Theory. Wiley-Interscience, 2006.

![](images/8a2c4188274b44ca1d348286fc57898dbfcb46c33715df48d958ed53d291d1cf.jpg)



Chaocan Xiang (S’10) received the BS degree in computer science and engineering from the Institute of Communication Engineering, PLA University of Science and Technology, China, in 2009. He is currently working toward the PhD degree from the PLA University of Science and Technology. His current research interests include energy efficient algorithm design for wireless sensor networks, participatory sensing. He is a student member of the IEEE.

![](images/c995905fb491b249844cf8bcec312417f0ba61049fbcccf1671d3f186ac6e2dc.jpg)



Panlong Yang (M’02) received the BS, MS, and the PhD degrees in communication and information system from the Nanjing Institute of Communication Engineering, China, in 1999, 2002, and 2005, respectively. During September 2010 to September 2011, he was a visiting scholar in HKUST. He is now an associate professor in the Nanjing Institute of Communication Engineering, PLA University of Science and Technology. His research interests include wireless mesh networks, wireless sensor networks and cognitive

radio networks. He has published more than 50 papers in peer-reviewed journals and refereed conference proceedings in the areas of mobile ad hoc networks, wireless mesh networks and wireless sensor networks. He has also served as a member of program committees for several international conferences. He is a member of the IEEE Computer Society, the IEEE, and the ACM SIGMOBILE Society.

![](images/6c1046b3ddc4dbb4219eadd631771d68a92b466ab9d6eef4d58684c907b323fe.jpg)



Chang Tian (M’02) received the BS degree in communication and information system, MS and PhD degrees in computer science and engineering from the Institute of Communications Engineering, Nanjing, China, in 1984, 1989 and 2001, respectively. During September 1995 to September 1996, he was a visiting scholar in the Universit¤ di Pisa of Italy. He is currently a professor €at the PLA University of Science and Technology, China. He has published widely in the areas of distributed system, wireless ad-hoc network,

signal processing for communications, information theory. His current research interests include wireless sensor network, network coding, etc. He is a member of the IEEE.

![](images/c9d45c048c1d37a190120b11f6814684c04c55db863de6a212c02ef63363ce1f.jpg)



Haibin Cai received the BEng degree from the National University of Defense Technology, in 1997, and the MS degree from the National University of Defense Technology, in 2004, and the PhD degree from the Donghua University, Shanghai, China, in 2008. He is an associate professor in the Software Engineering Institute, East China Normal University. His research interests include Internet of things, embedded systems and cyber-physical systems.

![](images/fe77aa163717130c4928e5f1e441180b0f2e682b03bb8644eeb2b2b128e49977.jpg)



Yunhao Liu (SM’06) received the BS degree in automation from Tsinghua University, Beijing, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. Being a member of Tsinghua National Lab for Information Science and Technology, he holds Tsinghua EMC chair professorship. He is the director of Key Laboratory for Information System Security, Ministry of Education, and a professor at School of Software, Tsinghua University. He is

also a faculty member at the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include pervasive computing, peer-to-peer computing, and sensor networks. He is a senior member of the IEEE.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.