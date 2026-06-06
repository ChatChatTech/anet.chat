# iStep: A Step-Aware Sampling Approach for Diffusion Profiling in Mobile Sensor Networks

Chaocan Xiang, Student Member, IEEE, Panlong Yang, Member, IEEE, Xuangou Wu, Hong He, Baowei Wang, and Yunhao Liu, Fellow, IEEE

Abstract—We investigate the mission-critical diffusion profiling problem in mobile sensor networks, where the energy cost and the time delay are constrained. Previous studies fail to solve this problem well enough due to the extremely large searching spaces for sensor measurements and the dynamic evolutions during the diffusion process. We propose a step-aware spatiotemporal sampling approach, which is called iStep, achieving near-optimal profiling precision in terms of the overall profiling process. Leveraging the upper bound of the deviation value in sampling position during each iteration, we build a comprehensive model between sampling interval and the current state parameters, including the distances between the mobile sensors and the pollution source, as well as the confidence interval radius of the source. Building upon this model, we propose an algorithm on computing the step-aware sampling interval. The computational complexity of iStep is O(N S2), which is in the same order of the radial approach, where N is the number of sensors, and S is the total number of movement steps in each iteration. Extensive simulation results show that, compared with the radial approach, iStep can improve the average precision by up to 56.8% and the worst precision by up to 59.1%. Moreover, it performs closely to the brute-force approach, which potentially verifies the near-optimal character of iStep.

Index Terms—Fisher information, mobile sensor network, profiling diffusion, spatiotemporal sampling (STS).

# I. INTRODUCTION

M ORE and more water ecological environments are aptto be polluted due to leakage of chemical materials. For to be polluted due to leakage of chemical materials. For example, the Gulf of Mexico oil spill in 2010 killed 11 men

Manuscript received September 12, 2014; revised January 23, 2015 and September 14, 2015; accepted October 31, 2015. Date of publication November 20, 2015; date of current version October 13, 2016. This work was supported in part by the National Natural Science Foundation of China under Grant 61502520, Grant 61190114, Grant 61272487, Grant 61232016, Grant U1405254, Grant 61173136, Grant 61232018, Grant 61502520, Grant 61402009, and Grant BK20150030; by CMMI 1436786, by the PAPD Fund, and by the Collaborative Innovation Center of Atmospheric Environment and Equipment Technology. The review of this paper was coordinated by Dr. D. Zhao. (Corresponding author: Panlong Yang.)

C. Xiang and H. He are with Logistic Engineering University, Chongqing 401331, China (e-mail: xiang.chaocan@gmail.com).

P. Yang is with the College of Communications Engineering, PLA University of Science and Technology, Nanjing 210007, China (e-mail: panlongyang@ gmail.com).

X. Wu is with the School of Computer Science and Technology, University of Anhui Technology, Anhui 243000, China (e-mail: xuangouwu@gmail.com).

B. Wang is with the School of Computer and Software, Nanjing University of Information Science and Technology, Nanjing 210007, China (e-mail: wbw. first@163.com).

Y. Liu is with the MOE Key Laboratory for Information System Security, School of Software, Tsinghua University, Beijing 100084, China.

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TVT.2015.2502321

and did tremendous damage to marine and wildlife for a long time [2]. Consequently, it is vitally important to profile the pollution diffusion process accurately, including the total amount of discharged pollution, the position of the source, the diffusion speed and time, etc.

There are two common ways to profile diffusion, including manual sampling (such as by boat or handheld devices) and static sensor networks (such as fixed or buoyed sensors) [3]. However, these two ways consume large amounts of money, e.g., wasting a lot of labor or sensors. Moreover, they are difficult to adapt to dynamic evolution of diffusion. To address these problems, mobile sensor networks have been recently proposed in [1], [4], and [5]. Despite the aforementioned advantages, mobile sensor networks introduce a new problem for profiling diffusion. The energy cost and delay are constrained. Moreover, it is worth noting that precision, energy cost, and delay are closely related to each other. Thus, energy and delay constraints should be seriously considered. Unfortunately, current studies fail to focus on the constraints of energy cost and time delay in the optimization criteria.

In summary, there are two challenges that need to be formally addressed for this interesting but challenging topic.

• First, profiling the diffusion by mobile sensors is difficult because of the extremely large searching spaces for measurements. Even worse, considering the constraints of energy cost and time delay, some ideal measurement locations are not reachable, which may eventually affect the profiling accuracy of the pollution source.

• Second, the diffusion process is highly dynamic, which is constantly changing over time and across the interested area. Moreover, the measurement accuracy of sensors also varies during the moving process, which possibly brings more uncertainty into the sampling process. Conventional stochastic modeling methods cannot be applied to tackle this difficulty due to the delay and energy constraints.

In dealing with these challenges, inspired by the radial movement scheduling method [1], we propose iStep, which is a step-aware spatiotemporal sampling (STS) approach for profiling the pollution source. Ours is an iterative and adaptive approach in achieving near-optimal profiling accuracy. More specifically, first, we find that the sampling interval in each iteration plays an important role in the improvement of profiling accuracy when energy and delay are constrained. Second, to optimize the precision under limited energy and delay, we build a comprehensive model between the sampling interval and the state parameters, including the distances of the mobile sensors and the pollution source, as well as the confidence interval radius of the source. Then, this confidence interval radius is derived based on Fisher information [6] and the asymptotic normality property of maximum-likelihood estimation (MLE) [7]. Finally, based upon these models, we propose an algorithm on computing the step-aware sampling interval.

The contributions of this paper are twofold.

1) To the best of our knowledge, iStep is the first work to profile diffusion accurately and efficiently under the constraints of energy cost and delay in the optimization criteria. Comparing with the current constant sampling interval approach [1], our adaptive STS approach achieves much higher precision with the same order of the computational complexity. Moreover, iStep achieves near-optimal profiling accuracy.   
2) We derive a confidence-interval-based scheme for evaluating the profiling errors. As there is no ground-truth location of the pollution source, measuring and evaluating the profiling error is difficult. We leverage Fisher information and the asymptotic normality property of MLE for deriving the confidence interval.

The remainder of this paper is organized as follows. We review the related work in Section II. Section III introduces our system model, and Section IV presents the research motivation and our study problem. In Section V, a step-aware STS approach is proposed to solve the problem. We present the simulation results in Section VI and discuss our work in Section VII. Finally, Section VIII concludes this paper.

# II. RELATED WORK

In most of the previous research studies, static sensor networks [4], [8]–[10] are exploited to monitor the diffusion process. Recently, mobile sensors are leveraged for profiling pollution diffusion to address the drawbacks of static sensors, such as high cost and poorly dynamic adaptation. Jeremic and Nehorai in [4] and Porat and Nehorai in [5] proposed a profiling diffusion approach based on a single mobile sensor, using the iterative movement of a sensor to improve the profiling precision gradually. They can overcome the shortcomings of a static sensor network. However, the profiling precision is low, as the energy of a single sensor is greatly limited, and the sensor movement consumes large amounts of energy. Therefore, Wang et al. [1], [11] exploited the collaboration of multiple mobile sensors to improve the profiling performance. They derived a closed-form expression for the expected accuracy metric based on the Cramér–Rao bound [12]. Furthermore, they proposed a near-optimal algorithm for scheduling the movement of the sensors to maximize this metric in terms of one iteration process. Our study is inspired by this study [1]. Nevertheless, there are distinguished differences between these two works as follows. Wang et al. [1] focused on the movement scheduling in one iteration process and proposed a near-optimal movement scheduling method in terms of one iteration process. In contrast, our work emphasizes the improvement of the profiling accuracy under the limited energy and delay resources in the overall profiling process, which includes several iterations. Furthermore, as the sampling interval makes an important impact on profiling precision under limited energy and delay, we propose a stepaware STS approach, adaptively adjusting the sampling interval based on current state information. Our method can achieve a near-optimal profiling performance in terms of the overall profiling process.

Moreover, in recent years, active sensing has been widely discussed and studied in contour estimation [13], [14], mobile target detection [15], [16], and field reconstruction [17], [18]. Active sensing denotes that the sensors are actively moving with a goal based on feedback or local information [13], [17], [18]. Specifically, Srinivasan et al. in [13] and Srinivasan and Ramamritham in [14] aimed at estimating the contour based on active sensing. They used local gradient information to guide the sensors to move toward the contour. Moreover, they exploited the local sensor measurements and the collaboration between sensors to make a tradeoff between moving toward the contour and spreading around the contour. Chin et al. [15], [16] used the active sensing of mobile sensor networks to detect the mobile target. They formalized this problem as a game between a mouse (mobile target) and a collection of cats (mobile sensors). They presented an optimal cat’s movement strategy for pursing the mouse and an optimal mouse’s movement strategy for escaping in different conditions. Although both aforementioned studies and our method use the active sensing of mobile sensor networks, their problems are different from that of our work. Wang et al. [17] used active sensing to reconstruct the spatiotemporal aquatic field and presented a rendezvous-based mobility control scheme. In this method, the mobile sensors are collaborating with each other in the form of a swarm to maintain wireless connectivity. Moreover, they exploited the information theory to design a scheme for selecting rendezvous regions to maximize the reconstruction accuracy subject to limited sensor mobility. Similar to this work, our study focuses on diffusion profiling in the aquatic environment. Nevertheless, differing from this study, we investigate in depth the relationships among precision, energy cost, and delay and leverage the quantification results of this relationship to propose a near-optimal STS approach.

In addition, there are considerable research studies on the relationship of precision–energy–delay in several relevant areas, e.g., detecting target and estimating the contour. Nowak et al. [18]–[21] studied how to decrease the energy cost while guaranteeing the precision of estimating contour. Their energy cost considers the communication and sense of sensors, whereas that of our study takes account of sensors’ movement. In [22] and [23], considering the energy consumption of movement, an optimal sensor movement scheduling algorithm is developed to minimize the energy cost while satisfying the requirements of the detecting performance and the delay. As these approaches [22], [23] are based on the assumption that the positions of the targets are known beforehand, they cannot be applied to our problem directly, where the position of the source cannot be available previously.

TABLE I FREQUENTLY USED NOTATIONS 

<table><tr><td>Symbol</td><td>Definition</td></tr><tr><td>A</td><td>the total substance discharged at the source (cm3)</td></tr><tr><td>λ,t</td><td>the diffusion coefficient (m2/s) and the diffusion time (s) respectively</td></tr><tr><td>(x0,y0)</td><td>the position of the pollution source</td></tr><tr><td>Θ, Θ</td><td>the diffusion profile and the profile estimation respectively</td></tr><tr><td>u,σ</td><td>the bias of sensor noise and its deviation respectively</td></tr><tr><td>(xj,i,yj)</td><td>the sampling location of the i-th sensor in the j-th iteration</td></tr><tr><td>Xj</td><td>the sampling location vector of the sensors in the j-th iteration, i.e. (xj,i,yj) ∈ Xj</td></tr><tr><td>c(x,y,t)</td><td>the diffusion concentration at the location (x,y) with the diffusing time t</td></tr><tr><td>z</td><td>the measurement of sensor</td></tr><tr><td>N,M</td><td>the number of sensors and iterations respectively</td></tr><tr><td>ε,E,D</td><td>the profiling error, energy constraint and delay constraint respectively</td></tr><tr><td>l</td><td>the unit of moving length, is typically set to 0.5m</td></tr><tr><td>ξ0</td><td>the initial sampling interval</td></tr><tr><td>ξj</td><td>the sampling interval of the j-th iteration</td></tr><tr><td>Li</td><td>the moving length of the i-th sensor in the j-th iteration</td></tr><tr><td>δ</td><td>the global sampling deviation</td></tr><tr><td>γj</td><td>the confidence interval radius of the source in the j-th iteration</td></tr><tr><td>ωj</td><td>the total distance of sensors from the source in the j-th iteration</td></tr><tr><td>L</td><td>the likelihood function</td></tr></table>

# III. SYSTEM MODEL

# A. Pollution Diffusion and Sensor Measurement Model

Suppose that a pollution source diffuses with a constant rate in a two-dimension static aquatic environment. Let $c ( x , y , t )$ denote the diffusion concentration at location $( x , y )$ with diffusion time t. Hence, according to Fick’s law [24], the partial equation of the diffusion concentration [8] is

$$
\frac {\partial c (x , y , t)}{\partial t} = \lambda \cdot \frac {\partial^ {2} c (x , y , t)}{\partial x ^ {2}} + \lambda \cdot \frac {\partial^ {2} c (x , y , t)}{\partial y ^ {2}} \tag {1}
$$

where λ denotes the diffusion coefficient, characterizing the speed of the diffusion. It is a known constant, related to the species of the solvent and diffuser.

We assume that a total pollution substance of $A \ \mathrm { c m ^ { 3 } }$ is discharged at the location $( x _ { 0 } , y _ { 0 } )$ when t = 0. By solving (1), we can derive the diffusion concentration $c ( x , y , t )$ at location $( x , y )$ with diffusing time $t \left( t > 0 \right)$ as

$$
c (x, y, t) = \frac {A}{4 \pi \lambda t} \exp \left(- \frac {d ^ {2} (x , y)}{4 \lambda t}\right) \tag {2}
$$

where $d ( x , y )$ denotes the distance between the sampling location $( x , y )$ and the location of the pollution source $( x _ { 0 } , y _ { 0 } )$ .

This diffusion model in (2) has been widely used in numbers of approaches [1], [5], [8], [25] and validated by the experiment [1]. According to (2), the spatial distribution of the concentration at diffusion time t follows a Gaussian distribution. The diffusion profile is thus described as $\Theta = \{ A , t , x _ { 0 } , y _ { 0 } \}$ .

The sensors’ measurements are subjected to noise, due to the limited capability of sensors and the environment noise. For simplicity, we assume that the noise at each sensor is an independent and identically distributed random variable with a Gaussian distribution. Specifically, the measurement $z ( x , y , t )$ , which is made by the sensor at location $( x , y )$ with diffusion time t, is

$$
z (x, y, t) \sim \mathcal {N} \left(c (x, y, t) + u, \sigma^ {2}\right) \tag {3}
$$

![](images/d6bc2edd3c1dba63af8ff6af139ced11391e2af97554034fec8d60296e005aa3.jpg)



Fig. 1. STS model in a mobile sensor network.

where u denotes the bias of the noise experienced by the sensor, and $\sigma ^ { 2 }$ denotes its variance. We assume that these two parameters are available. For example, they can be specified by the manufacturer of the sensor or measured before real deployment. The above measurement model has been widely used for most of chemical sensors [1], [4], [5], [26]. Table I summarizes the notations frequently used in this paper.

# B. STS Model

STS of mobile sensors is leveraged to profile the diffusion. Its model is described as follows.

STS Model: As shown in Fig. 1, given a two-dimension field, we need to find the optimal sampling location $( x _ { i } ^ { j } , y _ { i } ^ { j } )$ for the ith sensor at diffusion time $t _ { j }$ with the measurement $z ( x _ { i } ^ { j } , y _ { i } ^ { j } , t _ { j } )$ of the pollution diffusion to minimize the profiling error . Thus

$$
\epsilon = \left\| \left(\hat {x} _ {0}, \hat {y} _ {0}\right) - \left(x _ {0}, y _ {0}\right) \right\| _ {2} \tag {4}
$$

![](images/413b77d30c3883f07204652eb01c10fea84cfa1eec62c297083c2cb3db2e030f.jpg)



Fig. 2. Basic scheme of the STS model and the framework of iStep.

where $t _ { j }$ denotes the diffusion time in the jth iteration. $( \hat { x } _ { 0 } , \hat { y } _ { 0 } )$ denotes the estimated position of the source based on the measurements $z ( x _ { i } ^ { j } , y _ { i } ^ { j } , t _ { j } ) \ ( i = 1 , 2 , \dots , N ; j = 1 , 2 , \dots , M )$ . N and M denote the number of the sensors and iterations, respectively. Note that, in this paper, the profiling error  only evaluates the source’s position, which is an important and typical parameter in the diffusion profile. Moreover, it is similar if considering other parameters of the diffusion profile, e.g., A and t.

In the STS model, there are three most important metrics, including the profiling precision, delay, and energy cost.

• The precision is characterized by the profiling error as (4). Less error means higher precision.   
• The delay is the time taken for completing the entire profiling process, mainly including the movement of sensors, the estimation of the diffusion profile, and the selection of sampling locations.   
• The energy consumption denotes the energy cost on sensor moving. We do not consider the energy cost on sensing and communication because it is significantly less than that on moving [13]. Throughout this paper, the energy consumption is quantified by the corresponding moving length of the sensor, due to their approximately proportional relationship [27]. For simplicity, we assume that the moving length is always a multiple of l meters, and this unit length is referred to as a step.

# C. Basic Scheme of STS

Here, we present a basic working scheme for the STS model in a mobile sensor network, which is adopted by most of current studies [1], [4], [5], [11]. It exploits an iterative way to improve the profiling precision gradually, without prior knowledge on the pollution source. Specifically, in each iteration, new sampling locations of sensors are selected based on current profile estimation. As shown in Fig. 2, the process of each iteration includes three steps.

• Step 1: One of the sensors is selected as the head, e.g., the sensor that is closest to the pollution source [1]. All the sensors send their sampling values of current locations to the head. Then, based on these samples, the head estimates the diffusion profile, using the MLE method [5], [8].

• Step 2: According to the previous profile estimation, the head selects the new sampling location for each sensor, which is determined by the moving orientation and moving length. Specifically, the moving orientation of each sensor is toward the estimated location of the source along the straight line between the estimated source location and the current sensor location [1], [4]. The moving lengths of the sensors are selected to maximize the profiling precision, being subject to the sampling interval (as defined in Definition 1).   
• Step 3: The head sends the new sampling locations to each sensor. Each sensor moves to the new sampling location.

These three steps are iterated until satisfying the stop condition, e.g., the maximum number of iterations, the constraints of energy cost and delay, etc. The estimated profile of the final iteration is considered as the profile estimation, i.e., xˆ0, yˆ0, Aˆ, and tˆ.

Definition 1 (Sampling Interval): The sampling interval denotes a constrained value, where the sum of the distances between two consecutive sampling locations of every sensor is constrained. Formally, the sampling interval of the jth iteration, which is denoted by $\xi _ { j }$ , satisfies the following condition:

$$
\xi_ {j} \geq \sum_ {i = 1} ^ {N} \left\| \left(x _ {i} ^ {j}, y _ {i} ^ {j}\right) - \left(x _ {i} ^ {j + 1}, y _ {i} ^ {j + 1}\right) \right\| _ {2} \tag {5}
$$

where $( x _ { i } ^ { j } , y _ { i } ^ { j } )$ denotes the sampling location of the ith sensor in the jth iteration.

# IV. MOTIVATION AND PROBLEM FORMALIZATION

In the STS model, the energy cost and time delay should be seriously considered, where profiling precision, energy cost, and time delay are correlating and affecting each other. Furthermore, the energy cost and delay, both called resource, are constrained in the practical applications. In the following, we analyze the relationship among these three metrics when the resources are limited and propose our study problem.

# A. Efficient Utility of Resources is Important for Profiling Performance

Here, based on the experiments of the basic scheme, we study the relationship among precision, energy, and delay under the constraints of the resources.

The settings of the experiments are as follows. The pollution source is centered at a sensing field of 150 m × 150 m, and 20 sensors are randomly deployed in this field. The sensors begin profiling when the pollution has diffused for 1000 s. The energy cost is constrained by E, uniformly varying from 100l to 300l (the length of a step $l = 0 . 5$ m throughout this paper). For each energy constraint, we get the profiling errors and delays under ten random sampling intervals, which follow the uniform distribution from 20l to 100l. The profiling errors are measured using the distance between the ground-truth pollution source and the estimated source of the final iteration. All the results are averaged over 100 simulation runs. As shown in Fig. 3, these three metrics are highly correlated. The profiling precision roughly increases with the delay and energy cost. It is straightforward to believe that increasing the resources can contribute to the precision. However, the relationship among these three metrics is complex when the resources are limited. Specifically, as shown in Fig. 3, under the same energy constraint, both the delay and the profiling errors vary with the sampling interval. In summary, under limited resources, efficient utilization of resources is significant for the profiling performance in STS.

![](images/dee97253f998de6e418f8777978b61844bae4280d3b832ab09a79d051a6b600f.jpg)



Fig. 3. Color map of the precision–energy–delay relationship in the STS model.

# B. Sampling Interval is the Key to Efficient Utility of Resources

We analyze what the key factor for the efficient utility of resource is in this section.

In the basic scheme of the STS model, it is worth noting that, in each iteration, the total moving length of sensors is constrained by the sampling interval to avoid producing significant profiling error. The error originates from selecting new sampling locations based on the profile estimation with the error. Thus, it is easy to know that the sampling interval makes significant impacts on the profiling performances, including the profiling precision, energy cost, and delay. In the following, we will study how much and why the sampling interval affects the performances based on the experiments as well as analysis. In this experiment, we make a slight modification on our previously experimental settings, where the energy constraint E varies from 200l to 500l. For each constraint E, we uniformly vary the sampling interval from 30l to 150l.

As shown in Fig. 4(a), the ratio of the profiling precision to the energy decreases with the sampling interval. Under the same energy cost, the difference of the precision is up to 10 m. The main reason is as follows. As shown in Fig. 5(a), we take a single sensor for example. In each iteration, the profiling precision will increase if the sensor moves toward the actual pollution source, because the sensor closer to the source will get a higher signal-to-noise ratio (SNR) [1]. However, the location of the actual pollution source is unknown and replaced by the position of the estimated source. Since there is an inherent distance between them, the actual sampling location of the sensor deviates from the ideal location. A longer sampling interval leads to larger sampling deviation, which, in turn, results in lower precision owing to wasting more energy. Note that the sampling deviation is represented by the vertical distance from the actual sampling location to the ideal moving orientation, as shown in Fig. 5(a).

![](images/b809c5f7616ce65f273f170873c3e5658ead53fc3d47a8bd3533cc66c475caf5.jpg)



![](images/0930545eef92b9ba97fb2d7b999cfff0606fb2a728fb168b4b28407caf940256.jpg)



Fig. 4. Impact of sampling interval on profiling precision, delay, and energy. (a) Influence on precision and energy. (b) Influence on delay and energy.

Moreover, Fig. 4(b) shows that the ratio of the delay to energy decreases with the sampling interval. At the same constraint of energy cost, the difference of the delay is up to 3500 s, i.e., nearly 1 h. The main reason is that one of the sensors acts as the head in the basic scheme of the STS model. In each iteration, it takes a nonignorable time for the head to estimate the profile and select new sampling locations, due to the limited processing ability of the sensor. For example, according to the real experiments in [1], the cost time is beyond 100 s when the number of sensors is 20. Since the number of the iterations decreases with the sampling interval when the energy is constrained, the delay decreases with the sampling interval.

In summary, the sampling interval makes a great impact on the precision, energy, and delay of the STS model, due to the sampling deviation and the nonignorable computing delay of the head in each iteration. As a result, the sampling interval is a key factor for efficient utilization of the limited resources.

# C. Optimization Sampling Interval Problem

In the STS model of a mobile sensor network, the energy and delay resources are limited. According to the given analysis, the efficient utilization of the resources is greatly important for the profiling performance under the constraints of the resources, and the key to it is the sampling interval. As a result, in this paper, we focus on designing the STS interval to make the most efficient utilization of the limited energy and delay resources. Specifically, the problem is formalized as follows.

Optimization Sampling Interval Problem: For a given set of N mobile sensors initially deployed at a known position vector $\vec { X } _ { 1 } = \{ ( x _ { i } ^ { 1 } , y _ { i } ^ { 1 } ) , i = 1 , \dots , N \}$ and a pollution source diffusing at an unknown location, our objective is to design the sampling interval for each iteration $\vec { \xi } = ( \xi _ { j } , j = 1 , \dots , M )$ , so as to minimize the final profiling error , subject to the following constraints: 1) The total energy cost is no greater than $E ;$ 2) the total delay is no more than D. This problem is characterized by a 5-tuple $( \vec { X } _ { 1 } , \vec { \xi } , E , D , \epsilon )$ . Formally

![](images/6763e5b00ae232a3dd57b84d540ed451f157d307f1c18d622c14b38eaa32fdab.jpg)



![](images/778367f8e7f906ed186e546afd30f398aac8cfdc2bbcad2c7353d5ce76d02b91.jpg)



(b)   
Fig. 5. Analysis of sampling deviation. (a) Sampling deviation for a single sensor. (b) Quantitative analysis of the relationship between sampling interval and sampling deviation.

minimize  (6)

s.t. $\sum _ { j = 1 } ^ { M } \sum _ { i = 1 } ^ { N } L _ { i } ^ { j } \leq E$ (7)

$$
\sum_ {j = 1} ^ {M} \left\{\max _ {i = 1, \dots , N} \left\{L _ {i} ^ {j} \right\} / \nu \right\} \leq D \tag {8}
$$

where

$$
\overrightarrow {L} _ {j} = \left\{L _ {i} ^ {j}, i = 1, \dots , N \right\} \tag {9}
$$

$$
\overrightarrow {X} _ {j} = \left\{\left(x _ {i} ^ {j}, y _ {i} ^ {j}\right), i = 1, \dots , N \right\} \tag {10}
$$

$$
\overrightarrow {L} _ {j} = \Psi (\overrightarrow {X} _ {j}, \xi_ {j}) \tag {11}
$$

$$
\overrightarrow {X} _ {j + 1} = \Phi (\overrightarrow {X} _ {j}, \overrightarrow {L} _ {j}) \tag {12}
$$

$$
\epsilon = \Gamma (\overrightarrow {X} _ {M}). \tag {13}
$$

The notes for this formalization are as follows.

• ν denotes the moving speed of the sensors and is considered as a constant; $L _ { i } ^ { j }$ denotes the moving distance of the ith sensor in the jth iteration. It is noted that, as mentioned in Section III-B, the energy consumption is quantified by the corresponding moving length of the sensor. Thus, the dimensions of the left side and the right side in (7) are the same.   
• Ψ(·) in (11) represents the movement scheduling, which selects the moving length of each sensor given the sampling interval $\xi _ { j }$ and current sampling location vector $\vec { X _ { j } }$ of the sensors.   
• Φ(·) in (12) calculates the sampling location vector of the sensors in the (j + 1)th iteration, given the sampling location vector $\overrightarrow { X } _ { j }$ and the moving distance vector $\overrightarrow { L } _ { j }$ in the jth iteration.   
• $\Gamma ( \cdot )$ in (13) specifies the profiling error $\epsilon ,$ which is determined by the sampling location vector $\vec { X } _ { M }$ in the final

iteration. $\vec { X } _ { M }$ is computed by (11) and (12) iteratively, given $\overrightarrow { X } _ { 1 }$ and $\overrightarrow { \xi }$ .

# V. iStep: A STEP-AWARE SPATIOTEMPORAL SAMPLING APPROACH

Here, we propose a step-aware STS approach, which is named iStep, to solve the optimization sampling interval problem. We first provide a brief overview of iStep. In iStep, we focus on designing the STS interval, which is proposed in the following three sections.

# A. Overview of iStep

The framework of iStep is illuminated in Fig. 2. Based on the basic scheme of the STS model, iStep emphasizes on selecting new sampling locations based on current profile estimation as follows. Note that, in iStep, the stop condition of iterations is that the energy cost or the delay is beyond the constraints. In the following, we give the process of the jth iteration as an example.

1) The STS interval $\xi _ { j }$ is adjusted according to the state information of the current iteration, including the positions of the sensors, as well as the profile estimation.   
2) Given the current sampling interval $\xi _ { j } ,$ , the movements of sensors are scheduled, including the moving lengths and moving orientations. Based on the scheduling movements, the new sampling locations are selected. Specifically, for the moving orientation, each sensor moves toward the location of the estimated source to improve the profiling precision by increasing SNR. For the moving length, we adopt a radial movement scheduling method [1], which leverages a dynamic programming algorithm to solve an objective optimization problem as

Maximize $\omega = \sum _ { i = 1 } ^ { N } \sigma ^ { - 2 } e ^ { \frac { - d _ { i } ^ { 2 } } { 2 \lambda t } } \left( d _ { i } ^ { 2 } - \operatorname* { m i n } _ { k \in [ 1 , N ] , k \neq i } d _ { k } ^ { 2 } \right)$ d2i (14)

$\mathrm { s . t . } \qquad \sum _ { i = 1 } ^ { N } L _ { i } ^ { j } \leq \xi _ { j } .$ (15)

In (14) and (15), we note the following.

• $d _ { i }$ denotes the distance between the new sampling location of the ith sensor and the estimated source. Given the latest sampling location $( x _ { i } ^ { j - 1 } , y _ { i } ^ { j - 1 } )$ , $d _ { i }$ determines the moving length $L _ { i } ^ { j }$ of the ith sensor in the jth iteration. ω in (14) is a metric, evaluating the profiling accuracy when the sensors are at the new sampling locations.   
• Equation (15) constrains the total moving length of all the sensors by the sampling interval to avoid producing large sampling deviation and improve the profiling performance.

In iStep, we mainly focus on designing the STS interval and propose a step-aware sampling interval. We first derive the stepaware sampling interval in the following two sections. Finally, we present the algorithm on computing this sampling interval.

# B. Deriving Step-Aware Sampling Interval

As shown in Fig. 5(a), the sampling deviation is the root cause for the significant influence of the sampling interval on the profiling accuracy. Thus, we need to quantify the relationship between the sampling interval and the sampling deviation. Unfortunately, the location of the actual pollution source is unavailable. To solve this problem, as shown in Fig. 5(b), we leverage the confidence interval of the source with the radius γ centered at the position of the estimated source, where the actual source is located within this interval with a probability. The rationale behind this is that if the probability is very large and close to 1, the actual source is nearly within this confidence interval.

The sampling deviation varies with the position of the actual source. In the worst case, as shown in Fig. 5(b), when the actual source is located at the intersection of the circle and the tangent line, the sampling deviation is maximum. Using the simple principle of triangle similarity, we derive the relational expression between the moving length and the maximum sampling deviation in the jth iteration as

$$
L _ {i} ^ {j} = \frac {d _ {i} ^ {j}}{\gamma_ {j}} \cdot \delta_ {i} ^ {j} \tag {16}
$$

where $\delta _ { i } ^ { j }$ denotes the maximum sampling deviation of the ith sensor in the jth iteration. $d _ { i } ^ { j }$ denotes the distance between the ith sensor and the estimated source in the jth iteration. $\gamma _ { j }$ denotes the confidence interval radius of the source in the jth iteration.

We set a global sampling deviation $\delta ,$ which is the upper bound for the sampling deviation of each sensor in each iteration. Then

$$
\sum_ {i = 1} ^ {n} L _ {i} ^ {j} \leq \frac {\sum_ {i = 1} ^ {n} d _ {i} ^ {j}}{\gamma_ {j}} \cdot \delta . \tag {17}
$$

Let $\Omega _ { j }$ denote the upper bound for the total moving length of all the sensors in the jth iteration. Then, $\textstyle \Omega _ { j } = ( \sum _ { i = 1 } ^ { n } d _ { i } ^ { j } / \gamma _ { j } )$ · δ. As $L _ { i } ^ { j } = \parallel ( x _ { i } ^ { j } , y _ { i } ^ { j } ) - ( x _ { i } ^ { j + 1 } , y _ { i } ^ { j + 1 } ) \parallel _ { 2 }$ , the sampling interval $\xi _ { j }$ is the constraint value of the total moving length of the jth iteration according to (5). We set $\Omega _ { j }$ as the sampling interval $\xi _ { j }$ for the following reasons. On the one hand, according to $( 1 7 ) , \Omega _ { j }$ is an upper bound for the sampling interval, so that the sampling deviation is not beyond δ. On the other hand, if the sampling interval is too small, the number of the iterations is large, and the profiling delay is large. As a result, the sampling interval of the jth iteration is

$$
\xi_ {j} = \Omega_ {j} = \frac {\varpi_ {j}}{\gamma_ {j}} \cdot \delta \tag {18}
$$

where $\textstyle { \boldsymbol { \varpi } } _ { j } = \sum _ { i = 1 } ^ { n } d _ { i } ^ { j }$ and denotes the total distance between the sensors and the estimated source.

We set the sampling interval of the first iteration as the initial parameter, i.e., $\xi _ { 0 }$ , and call it the initial sampling interval in the remainder of this paper. Then, (18) can be rewritten as

$$
\xi_ {j} = \frac {\varpi_ {j} \cdot \gamma_ {1}}{\gamma_ {j} \cdot \varpi_ {1}} \cdot \xi_ {0}, \quad j = 1, 2, \dots , M. \tag {19}
$$

As the initial sampling interval $\xi _ { 0 }$ can be set previously, the sampling interval $\xi _ { j }$ of the $j \mathrm { t h }$ iteration is determined by two factors, i.e., the initial state information $( \varpi _ { 1 }$ and $\gamma _ { 1 } )$ and the current state information $( \varpi _ { j }$ and $\gamma _ { j } )$ . As $\varpi _ { 1 }$ and $\gamma _ { 1 }$ are determined by the initial sensor deployments and the diffusion parameters of the pollution source, the sampling intervals of each iteration are adjusted according to the state information of the current iteration. As a result, ours is a “step-aware” sampling approach.

In (19), $\varpi _ { j }$ can be easily gotten by online computation, whereas it is difficult to compute $\gamma _ { j }$ . As a result, it is the key to computing the confidence interval radius of the source, i.e., $\gamma _ { j }$ . We will derive it in the following section.

# C. Deriving Confidence Interval Radius

We compute the confidence interval radius of the source, leveraging the Fisher information and the asymptotic normality property of MLE.

In each iteration, the head estimates the diffusion profile Θ based on MLE. The likelihood function is as follows:

$$
L \left(\frac {\Theta}{Z}\right) = \ln \left(\prod_ {k = 1} ^ {N} f _ {k} \left(\frac {\Theta}{z}\right)\right) \tag {20}
$$

where Θ includes $A , t , x _ { 0 }$ , and $y _ { 0 }$ , which are denoted by $\theta _ { 1 }$ , $\theta _ { 2 } , \theta _ { 3 }$ , and $\theta _ { 4 } ,$ respectively. $f _ { k } ( \Theta / z )$ is the probability density function of the kth sensor’s measurement, derived from the measurement model in (2) and (3), i.e.,

$$
f _ {k} \left(\frac {\Theta}{z}\right) = \frac {1}{\sqrt {2 \pi} \sigma} \exp \frac {\left(z - \frac {A}{4 \pi \lambda t} h _ {k}\right) ^ {2}}{- 2 \sigma^ {2}}
$$

$$
\text { where } \quad h _ {k} = \exp \left(\frac {d _ {k} ^ {2}}{- 4 \lambda t}\right). \tag {21}
$$

In (21), it is noted that z denotes the measurement that has removed the bias $u ,$ as it is easy to remove the known bias from the measurement.

MLE has an asymptotic normality property: The distribution of MLE tends to the Gaussian distribution when the scale of the measurements is large [7]. Specifically, the distribution of the estimation error is

$$
\sqrt {N} (\hat {\Theta} - \Theta_ {0}) \xrightarrow {d} \mathcal {N} (0, I ^ {- 1} (\hat {\Theta})) \tag {22}
$$

where $\Theta _ { 0 }$ and $\hat { \Theta }$ denote the actual value and the estimated value for the unknown profile Θ, respectively. Both of them are a 4-D row vector. $I ^ { - 1 } ( \bar { \Theta } )$ is the inverse of Fisher information I(Θ) [6], which is defined as

$$
I (\Theta) = - E \left(\frac {\partial^ {2} L \left(\frac {\Theta}{Z}\right)}{\partial \Theta^ {2}}\right). \tag {23}
$$

As Θ includes four unknown parameters, I(Θ) is a $4 \times 4$ matrix, which is represented by $( J ( i , j ) ) | _ { 4 \times 4 } , \mathrm { i . e . }$ .,

$$
J (i, j) = - E \left(\frac {\partial^ {2} L \left(\frac {\Theta}{Z}\right)}{\partial \theta_ {i} \partial \theta_ {j}}\right), \quad i, j = 1, 2, 3, 4. \tag {24}
$$

According to (20), (21), and (24), we derive $J ( i , j )$ as (25), exploiting the additive property of Fisher information [28], i.e.,

$$
J (i, j) = \sum_ {k = 1} ^ {N} \frac {1}{\sigma^ {2}} \vartheta_ {i} ^ {k} \vartheta_ {j} ^ {k}, \quad i, j = 1, 2, 3, 4
$$

${ \mathrm { w h e r e ~ } } \vartheta _ { i } ^ { k } = { \left\{ \begin{array} { l l } { { \frac { A } { 4 \pi \lambda t } } \cdot { \frac { \partial h _ { k } } { \partial \theta _ { i } } } , } & { i = 2 , 3 , 4 } \\ { h _ { k } , } & { i = 1 . } \end{array} \right. }$ ∂hk ϑki (25)

The confidence interval of $\theta _ { i } \ \left( \forall \theta _ { i } \in \Theta \right)$ with confidence probability p is derived from (22) and (25) as follows:

$$
\theta_ {0} (i) \in \left[ \hat {\theta} (i) \pm \rho_ {p} \cdot \sqrt {I _ {i , i} ^ {- 1} (\hat {\Theta}) \cdot N ^ {- \frac {1}{2}}} \right], i = 1, 2, 3, 4 \tag {26}
$$

where $\rho _ { p }$ denotes the standard score of confidence probability p. $\theta _ { 0 } ( i )$ and ${ \hat { \theta } } ( i )$ denote the actual value and the estimated value for unknown parameter $\theta _ { i } ,$ respectively. $I _ { i , i } ^ { - 1 } ( \Theta )$ denotes the element in the ith row and the ith column of the matrix $I ^ { - 1 } ( \Theta )$ .

As the position of the pollution source involves two parameters, i.e., $x _ { 0 }$ and $y _ { 0 }$ , according to (26), the confidence interval of the source’s position is

$$
\{(x, y) | | x - \hat {x} _ {0} | \leq l _ {x}, | y - \hat {y} _ {0} | \leq l _ {y} \}
$$

$\mathrm { w h e r e } \quad l _ { x } = \rho _ { p } \cdot \sqrt { I _ { 3 , 3 } ^ { - 1 } ( \hat { \Theta } ) \cdot N ^ { - \frac { 1 } { 2 } } }$

$$
l _ {y} = \rho_ {p} \cdot \sqrt {I _ {4 , 4} ^ {- 1} (\hat {\Theta}) \cdot N ^ {- \frac {1}{2}}} \tag {27}
$$

where $\scriptstyle { \hat { x } } _ { 0 }$ and $\hat { y } _ { 0 }$ denote the estimated value of $x _ { 0 }$ and $y _ { 0 }$ respectively.

According to (27), the confidence interval of the source’s position is a rectangle centered at the estimated position of the source. For ease of model processing, we employ a disc of this confidence interval [as defined in (28)] as the confidence interval of the source that is approximately

$$
\left\{(x, y) \mid (x - \hat {x} _ {0}) ^ {2} + (y - \hat {y} _ {0}) ^ {2} \leq \gamma^ {2} \right\} \tag {28}
$$

where $\gamma$ is the confidence interval radius

$$
\gamma = \frac {\rho_ {p}}{\sqrt [ 4 ]{N}} \cdot \sqrt {I _ {3 , 3} ^ {- 1} (\hat {\Theta}) + I _ {4 , 4} ^ {- 1} (\hat {\Theta})} \tag {29}
$$

where $\rho _ { p }$ is a constant. For example, $\rho _ { p }$ is 1.96 when $p = 9 5 \%$ .

# D. Algorithm on Computing Step-Aware Sampling Interval

To summarize the given derivations, we present the algorithm on computing a step-aware sampling interval for each iteration as Algorithm 1. We take the jth iteration for example. As shown in Algorithm 1, the algorithm is greatly simple, and the time complexity is $O ( N )$ , where N is the number of the sensors. The input parameters are the initial sampling interval $\xi _ { 0 }$ , the sensors’ position vector $\vec { X _ { j } }$ , and the profile estimation $\hat { \Theta } _ { j }$ in the jth iteration. $\xi _ { 0 }$ is set previously, and we will analyze the influence of its variation on the profiling performance, giving a basic setting direction in Section VI-B. The other inputs are produced by the basic scheme of the STS model. For example, in the jth iteration, $\vec { X _ { j } }$ is reported by the sensors (e.g., Global Positioning System), and $\hat { \Theta } _ { j }$ is estimated by the head in step 1 of the basic scheme.

# Algorithm 1 Algorithm on Computing Step-Aware Sampling Interval

# Input:

Initial sampling interval $\xi _ { 0 } ;$

Position vector of N sensors in the jth iteration,

$$
\overrightarrow {X} _ {j} = \{(x _ {i} ^ {j}, y _ {i} ^ {j}) | i = 1, 2, \dots , N \};
$$

Profile estimation in the jth iteration,

$$
\hat {\Theta} _ {j} = \{\hat {A}, \hat {t}, \hat {x} _ {0}, \hat {y} _ {0} \};
$$

# Output:

Sampling interval of the jth iteration, $\xi _ { j } ;$

1: Given $\vec { X _ { j } }$ , calculate the Fisher information matrix I(Θ), according to (21) and (25).   
2: Given $I ( \Theta )$ and $\hat { \Theta } _ { j }$ , calculate $\gamma _ { j }$ according to (29).   
3: Given $\overrightarrow { X } _ { j }$ and ${ \hat { \Theta } } _ { j } ,$ calculate the total distance of the sensors from the estimated source, i.e., j .   
4: Given $\varpi _ { j } , \gamma _ { j } ,$ and $\xi _ { 0 } ,$ , calculate the sampling interval of the jth iteration, i.e., $\xi _ { j } ,$ , according to (19).   
5: return $\xi _ { j } ;$

In conclusion, the practical process of profiling diffusion is as follows. We take the jth iteration for illustrative description.

• In the $j \mathrm { t h }$ iteration, as shown in Fig. 2, first, the head sensor uses Algorithm 1 to compute the new sampling interval, according to the initial sampling interval, current positions of the sensors, and current estimation of profile.   
• Second, based on this new sampling interval, the head sensor uses the radial movement scheduling algorithm [1] to compute the moving length of each sensor, thus getting new sampling locations of sensors. Moreover, according to these new sampling locations, the head sensor chooses the new head sensor, which is closest to the estimated location of pollution source [1], [11]. Then, the head sensor

![](images/8f32e234748847e91a965d0301281c51fb5fd7d4e4ba4c67c368165d3b14dafe.jpg)



![](images/731a58327bb8c3e2c467084da8f1480f6f7ecd1a9829932a1a86bbb381ae6b29.jpg)



(b)

![](images/aac39ddca050aed178cc25889f0a405f4774f40d0a8e7bcdbe227f5f06eb43eb.jpg)



Fig. 6. Comparison of profiling precision between iStep and two baseline approaches. Note that a $, b , c , \ldots , k$ denote the energy constraint from 100l to 300l with the interval 20l, as well as the delay constraint from 1300 to 3800 s with the interval 250 s, respectively. (a) Average precision. (b) Worst precision. (c) Best precision.

sends the new sampling locations and the announcement of the new head sensor to each sensor.

• Third, each sensor receives this information and moves to its new sampling location. Moreover, all the sensors sample the pollution concentration and send their measurements along with their current locations to the new head sensor.   
• Finally, after receiving the measurements of all the sensors, the new head sensor estimates the diffusion profile based on these measurements, using the MLE algorithm [8].

# VI. EXPERIMENTAL RESULTS

# A. Simulation Methodology and Settings

The measurement of each sensor is randomly produced according to the sensor measurement model in (3). The diffusion profile is estimated by MLE, and the Nelder–Mead algorithm [29] is exploited to solve the nonlinear optimization of the likelihood objective function. We compare our approach with two baseline approaches. The first approach is the bruteforce approach, which exhaustively searches for every possible sampling interval for each iteration and chooses the optimal interval among them. Its results are considered as the optimal benchmark. The other approach is the radial movement schedule algorithm [1], called the radial approach for short, which achieves the best profiling accuracy in current existing approaches. It exploits a constant sampling interval for each iteration in the basic scheme of the STS model. There is an initial setting parameter for both of iStep and the radial approach, i.e., the initial sampling interval in iStep, and the constant sampling interval in the radial approach. In these simulations, for convenience, the constant sampling interval of the radial approach is also called the initial sampling interval, unless otherwise specified.

The simulation settings are as follows. The parameters of the pollution source are that $\dot { A } = 0 . 7 \times 1 0 ^ { 6 } \mathrm { c m ^ { 3 } }$ and $\lambda = 0 . 5 \mathrm { m ^ { 2 } / s }$ . They are consistent with the real field experiment reports [30]. The standard deviation of the measurement noise for each sensor $\sigma = 1 ~ \mathrm { c m ^ { 3 } / m ^ { 2 } }$ according to [31]. A total of 20 sensors are randomly deployed in the square region of 150 m × 150 m, and the pollution source is centered at this region, i.e., $x _ { 0 } = y _ { 0 } = 0 .$ . We let the sensors always start to profile the diffusion when the pollution has diffused for 1000 s, so as to easily compare various approaches. Sensors profile the diffusion iteratively by moving until the energy cost or the delay is beyond their constraints. The moving speed of each sensor $\nu = 2 . 5$ m/min, according to the speed of the robotic fish developed at Michigan State University [32]. In each iteration, the time spent on sense, communication, estimating, and scheduling the movement of 20 sensors is set to 100 s, according to the real experiment results in [1]. The simulation programs are written in MATLAB. All the simulations are executed 100 times, and we get the average values.

# B. Performance Evaluation of iStep

In the following, we evaluate the performance of iStep from two aspects: 1) the utilization efficiency of limited energy and delay resources; 2) the robustness of iStep.

1) Utilization Efficiency of Limited Energy and Delay Resources: To validate the utilization efficiency of the resources, we evaluate the profiling precision under the different constraints of energy cost and delay. The energy constraint E and the delay constraint D uniformly vary from 100l to 300l and from 1300 to 3800 s, respectively, where l is the length of the step. Under each pair of the constraints, i.e., $( E , D )$ , we randomly choose 20 different initial sampling intervals from E/20 to E/2 for iStep and the radial approach. The too small values and too large values are not chosen due to their poor performances. For each pair of the resource constraints, we compare iStep with two other baseline approaches in terms of the average, the best, and the worst profiling precision under these 20 different initial sampling intervals.

First of all, as shown in Fig. 6(a), iStep has greatly higher average precision than the radial approach. The difference of the average precision between these two approaches is at least 4 m, and up to 10.5 m in the best case. Thus, iStep can improve the average precision up to 56.8% compared with the radial approach. Furthermore, the average precision of iStep is close to that of the brute-force approach. The maximum difference is less than 2.3 m. As a result, iStep can acquire the near-optimal precision.

Then, as shown in Fig. 6(b), in comparison with the radial approach, the worst precision of iStep is closer to the optimal benchmark and makes a significant improvement by about 59.1%. On the other hand, Fig. 6(c) shows that the best precision of our approach can approximately achieve the optimal benchmark and is consistently higher than that of the radial approach.

In addition, as shown in Fig. 6(c), extremely few precisions of the brute-force method are slightly less than that of iStep. The reasons are as follows. As the search spaces of the solutions for the brute-force method are extremely large, it is nearly impossible to search the results exhaustively and get the optimal solution. Thus, in the practical experiments, we search for most of the solution spaces (e.g., 500 different parameter settings) and choose the best results as the approximate results of the brute-force method. Furthermore, as previously mentioned, iStep can achieve an approximately optimal performance. Moreover, the search spaces of the solutions are different between the brute-force method and the iStep method, i.e., the iStep method changes the initial sampling interval while the brute-force method changes the sampling interval of every iteration. As a result, once in a while, as shown in Fig. 6(c), the best results of iStep may be a bit better than the approximate results of the brute-force method. In the future work, we will further search for more results at different parameter settings and achieve more accurate results of the brute-force method.

In summary, under different constraints of the energy and delay resources, our approach has a much better performance than the radial approach in terms of the average, the worst, and the best precision. Furthermore, iStep can achieve near-optimal utilization efficiency of the resources. The reasons are that iStep adaptively adjusts the sampling interval of each iteration, according to the current state information. This adaptive sampling interval makes the utilization of the limited energy and delay resources more efficient rather than the fixed sampling interval in current existing approaches (e.g., radial method [1]). Thus, iStep can achieve an almost optimal profiling performance overall the profiling process, whereas the radial method can only acquire an approximately optimal performance in terms of one iteration process.

2) Robustness of iStep: Here, we evaluate the impact of the initial sampling interval on the profiling performance. At first, we evaluate the influence of its variation on the profiling accuracy to validate the robustness of iStep. In this experiment, for each pair of resource constraints, the initial sampling interval is uniformly varied from 10l to 100l for both iStep and the radial approach. We compare the standard deviation of the profiling precision between iStep and the radial approach in different initial sampling intervals. As shown in Fig. 7, the standard deviation in iStep is greatly small and, at most, 1.5 m, whereas it falls between 1.5 and 5.0 m in the radial approach. Thus, iStep is more robust than the radial approach. It is because the impact of the initial sampling interval on the profiling precision can be mitigated by adaptively adjusting the sampling intervals of the following iterations. Fig. 7 also shows that the standard deviation decreases with the resource constraints. Therefore, we can increase the constraints of the energy cost and delay to improve the robustness of iStep.

![](images/04d1b23cd28d3e3f4b40d4e1e71e3f0482b8a2078ceffb9a5fd23b4e05da9345.jpg)



Fig. 7. Comparison of standard deviation of profiling precision between iStep and the radial approach.

![](images/c20a59b8c2695232dcd4947ed78e35678712b6760b24b79b19536358e557af78.jpg)



Fig. 8. Profiling precision of iStep versus initial sampling interval.

Second, we analyze the profiling precision in different initial sampling intervals to give directions for setting it. As shown in Fig. 8, when the initial sampling interval is below 70l, the profiling precision slightly changes; otherwise, the precision significantly decreases. Therefore, these results give a basic direction for the settings of the first step: The initial sampling interval is not set too large and had better be less than 70l, i.e., 35 m. Moreover, the settings of the initial sampling interval make a slight impact on the profiling precision when its value is below 35 m.

# VII. DISCUSSION AND FUTURE WORK

# A. Scalability

We analyze and compare the scalability of iStep, the radial approach, and the brute-force approach. In each iteration, the time complexity of the radial approach is ${ \cal O } ( N S ^ { 2 } )$ [1], where S denotes the number of the allocatable movement steps in a profiling iteration. iStep only adds the phase of computing the sampling interval as Algorithm 1, where the time complexity is $O ( N )$ . Thus, the time complexity of iStep is $O ( N ) + O ( N S ^ { 2 } ) = O ( N S ^ { 2 } )$ . The brute-force approach searches for every possible sampling interval and executes the movement scheduling algorithm for each of them. Thus, its time complexity is ${ \cal O } ( S ) \times { \cal O } ( N S ^ { 2 } )$ . Considering an entire process of profiling diffusion with M iterations, iStep and the radial approach have the same time complexity, i.e., $O ( N ^ { M } S ^ { 2 M } )$ , whereas the time complexity of the brute-force approach, i.e., $O ( N ^ { M } S ^ { 2 M } ) \times O ( S ^ { \hat { M } } )$ , is exponential times more than that of them.

![](images/dfe33f539945040283571f4b7dc8542c442d61a97c4e17245ae19bc06b61bc7d.jpg)



(a)

![](images/8097e71c25dc7bb81aa42c2ef31ff857ba1b661ee8fe42d218fc02a4a20b04d1.jpg)



![](images/fb79b0250b4a95d813789df5e0bb5cf22ec5cdd378c7f424bd86b14b86ebe19d.jpg)



(c）  
Fig. 9. (a) Profiling precision versus initial sensor deployment. (b) and (c) Profiling precision of original location and drifted location versus advection speed. Note that the drifted location denotes the location of the pollution source drifted from the original location. (a) Sensor deployment. (b) Original location. (c) Drifted location.

# B. Communication Overhead

The overall process of profiling diffusion based on mobile sensor networks is described in Section V-D. To satisfy the demand of the coordination and communication among the sensors and the head sensor, each pair of sensors should have at least one connected communication path [33]. In other words, the communication paths of all the sensors (including the head sensor) form a connected graph. How to maintain wireless connectivity between sensors in water environments was studied in [17] based on the experiments and theoretical analysis. Hence, we do not discuss it any longer.

In iStep, the communication overhead mainly comprises two categories: the sensors-to-head messages (i.e., the messages of reporting measurements) and the head-to-sensors messages (i.e., the announcements of new sampling locations and the new head sensor). The sensors-to-head messages for each sensor only include the sensor ID, the concentration measurement, and the current location, whereas the head-to-sensors messages contain these new sampling locations of all the sensors and the sensor ID of the new head sensor. The distance between sensors makes an impact on the communication quality (e.g., data loss rate) in the water environment [17]. The relationships between the communication quality and the distances in an onwater wireless link have been well studied by the experiments in [11], [17], and [34]. Hence, here, we do not discuss the communication quality any more and assume that the communication path is reliable within the communication rage. Through the theoretical analysis, the total communication complexity is $O ( M * N ^ { 2 } )$ for the overall network, and the maximum communication complexity is $O ( M * N )$ for a single sensor (including the head sensor). Specifically, the communication complexity of scheduling the new head sensor is $O ( M * N )$ , as the head sensor locally chooses the new head sensor and sends the announcement of a new one [the communication complexity is $O ( 1 ) ]$ to each sensor. The detailed processes of other analyses are omitted, as it is simple. In future work, we will further evaluate the communication overhead by the real experiments.

# C. Large Number of Sensors

When there are numbers of sensors for profiling the pollution source, it is critical for how to initially deploy the sensors. The optimal sensor deployment is an open problem when the diffusion parameters of the pollution source are not known previously [35]. Here, we conduct an extensive simulation to analyze the influence of the initial sensor deployment on the profiling performance. We vary the initial sensor deployment under the same constraints of energy cost and delay. The sensors are randomly deployed around the pollution source in one, two adjacent, three, and four quadrants, respectively. As shown in Fig. 9(a), the profiling precision is higher when the sensors are initially spread around the pollution source, e.g., the sensors are initially deployed in three or four quadrants. As a result, it is a good strategy to deploy sensors around the source location randomly and uniformly in the pollution area.

# D. Large-Scale Aquatic Fields

The advection of an aquatic environment is nonignorable and the most influential factor when the sensors are deployed in a large-scale field. Thus, here, we mainly explore the impact made by the advection of an aquatic environment on the profiling performance. Specifically, we consider a complex and practical diffusion model with advection. We make an extensive simulation to evaluate the influence of the aquatic environment advection on the profiling performance. In this simulation, under the same constraints of energy cost and delay, we change the advection speed from 0 to 2 m/min. As shown in Fig. 9(b) and (c), although the profiling error of the original location is large when the advection speed is high, the advection speed makes a slight impact on the profiling precision of the drifted location, due to the relative movement between the pollution source and the sensors. Moreover, the drifted location of the pollution source is more important than its original location in practice.

# E. Energy Constraint

In our study, we only consider the total energy cost of all the sensors, which is the main impact factor on the profiling performance. Hence, we use the sampling interval to constrain the total moving length of all the sensors in each iteration, so as to optimize the utilization of the total energy cost. As the moving length of each sensor has been optimally selected by the dynamic programming algorithm [1], [11], the energy constraint of each sensor makes less impact on the profiling performance, compared with the total energy cost. Thus, it is not our focus in this paper and is set to a constant or a simple function of the total energy cost. In the future work, we will study the adaptive adjusting scheme for the energy constraint of each sensor.

# VIII. CONCLUSION

In this paper, we have studied the mission-critical profiling pollution diffusion in a mobile sensor network with limited energy and delay. We have proposed a step-aware STS approach, which is called iStep, to maximize the profiling precision under the constraints of energy cost and delay. The sampling interval of each iteration is adjusted adaptively according to the state parameters of the current iteration. The simulation results and the theoretic analysis show that, compared with current fixed sampling interval approaches, our approach can greatly improve the profiling accuracy with the same order of time complexity. Furthermore, ours can achieve near-optimal profiling accuracy.

# REFERENCES

[1] Y. Wang, R. Tan, G. Xing, J. Wang, and X. Tan, “Profiling aquatic diffusion process using robotic sensor networks,” IEEE Trans. Mobile Comput., vol. 13, no. 4, pp. 880–893, Apr. 2014.   
[2] Deepwater Horizon Oil Spill. [Online]. Available: http://en.wikipedia.org/ wiki/Deepwater\_Horizon\_oil\_spill   
[3] R. Muzzi et al., “A wireless Internet-based observatory: The REaltime Coastal Observation Network (ReCON),” in Proc. OCEANS, 2007, pp. 1–6.   
[4] A. Jeremic and A. Nehorai, “Landmine detection and localization using chemical sensor array processing,” IEEE Trans. Signal Process., vol. 48, no. 5, pp. 1295–1305, May 2000.   
[5] B. Porat and A. Nehorai, “Localizing vapor-emitting sources by moving sensors,” IEEE Trans. Signal Process., vol. 44, no. 4, pp. 1018–1021, Apr. 1996.   
[6] J. J. Rissanen, “Fisher information and stochastic complexity,” IEEE Trans. Inf. Theory, vol. 42, no. 1, pp. 40–47, Jan. 1996.   
[7] P. J. Bickel and B. Li, Mathematical Statistics, vol. 15. San Francisco, CA, USA: Holden-Day, 1977.   
[8] T. Zhao and A. Nehorai, “Detecting and estimating biochemical dispersion of a moving source in a semi infinite medium,” IEEE Trans. Signal Process., vol. 54, no. 6, pp. 2213–2225, Jun. 2006.   
[9] T. Zhao, “Distributed sequential Bayesian estimation of a diffusive source in wireless sensor networks,” IEEE Trans. Signal Process., vol. 55, no. 4, pp. 1511–1524, Apr. 2007.   
[10] J.-C. Chin et al., “Identification of low-level point radioactive sources using a sensor network,” ACM Trans. Sensor Netw., vol. 7, no. 3, p. 21, Sep. 2010.   
[11] Y. Wang, R. Tan, G. Xing, and X. Tan, “Accuracy-aware aquatic diffusion process profiling using mobile sensor networks,” in Proc. ACM/IEEE IPSN, 2012, pp. 1–12.   
[12] P. Stoica and A. Nehorai, “Music, maximum likelihood, and Cramer–Rao bound,” IEEE Trans. Acoust., Speech, Signal Process., vol. 37, no. 5, pp. 720–741, May 1989.

[13] S. Srinivasan, K. Ramamritham, and P. Kulkarni, “Ace in the hole: Adaptive contour estimation using collaborating mobile sensors,” in Proc. IPSN, St. Louis, MO, USA, 2008, pp. 147–158.   
[14] S. Srinivasan and K. Ramamritham, “Contour estimation using collaborating mobile sensors,” in Proc. DIWANS, Los Angeles, CA, USA, 2006, pp. 73–82.   
[15] J.-C. Chin, Y. Dong, W.-K. Hon, and D. K. Y. Yau, “On intelligent mobile target detection in a mobile sensor network,” in Proc. IEEE MASS, 2007, pp. 1–9.   
[16] J.-C. Chin, Y. Dong, W.-K. Hon, C. Y.-T. Ma, and D. K. Yau, “Detection of intelligent mobile target in a mobile sensor network,” IEEE/ACM Trans. Netw., vol. 18, no. 1, pp. 41–52, Feb. 2010.   
[17] Y. Wang et al., “Spatiotemporal aquatic field reconstruction using robotic sensor swarm,” in Proc. IEEE RTSS, 2012, pp. 1–10.   
[18] A. Singh, R. Nowak, and P. Ramanathan, “Active learning for adaptive mobile sensing networks,” in Proc. IPSN, Nashville, TN, USA, 2006, pp. 60–68.   
[19] R. Nowak and U. Mitra, “Boundary estimation in sensor networks: Theory and methods,” in Proc. IPSN, 2003, pp. 1–16.   
[20] R. Willett, A. Martin, and R. Nowak, “Backcasting: Adaptive sampling for sensor networks,” in Proc. IPSN, 2004, pp. 1–16.   
[21] R. Castro and R. Nowak, “Faster rates in regression via active learning,” in Proc. NIPS, 2005, pp. 179–186.   
[22] G. Xing et al., “Mobile scheduling for spatiotemporal detection in wireless sensor networks,” IEEE Trans. Parallel Distrib. Syst., vol. 21, no. 12, pp. 1851–1866, Dec. 2010.   
[23] R. Tan, G. Xing, J. Wang, and H. C. So, “Exploiting reactive mobility for collaborative target detection in wireless sensor networks,” IEEE Trans. Mobile Comput., vol. 9, no. 3, pp. 317–332, Mar. 2010.   
[24] N. March and M. Tosi, Introduction to Liquid State Physics. Singapore: World Scientific, 2002.   
[25] S. Vijayakumaran, Y. Levinbook, and T. F. Wong, “Maximum likelihood localization of a diffusive point source using binary observations,” IEEE Trans. Signal Process., vol. 55, no. 2, pp. 665–676, Feb. 2007.   
[26] A. Nehorai, B. Porat, and E. Paldi, “Detection and localization of vapor-emitting sources,” IEEE Trans. Signal Process., vol. 43, no. 1, pp. 243–253, Jan. 1995.   
[27] D. S. Barrett, M. S. Triantafyllou, D. P. Yue, M. A. Grosenbaugh, and M. J. Wolfgang, “Drag reduction in fish-like locomotion,” J. Fluid Mech., vol. 392, no. 1, pp. 183–212, 1999.   
[28] T. M. Cover and J. A. Thomas, Elements of Information Theory. Hoboken, NJ, USA: Wiley-Interscience, 2006.   
[29] J. A. Nelder and R. Mead, “A simplex method for function minimization,” Comput. J., vol. 7, no. 4, pp. 308–313, Jan. 1965.   
[30] A. J. Elliott, “Shear diffusion and the spread of oil in the surface layers of the north sea,” Ocean Dyn., vol. 39, no. 3, pp. 113–137, May 1986.   
[31] Cyclops-7 Users Manual, Turner Designs, Sunnyvale, CA, USA, 2014. [Online]. Available: http://www.aqualab.com.au/files/75/manual.pdf   
[32] X. Tan, “Autonomous robotic fish as mobile sensor platforms: Challenges and potential solutions,” Mar. Technol. Soc. J., vol. 45, no. 4, pp. 31–40, Jul./Aug. 2011.   
[33] S. Xie and Y. Wang, “Construction of tree network with limited delivery latency in homogeneous wireless sensor networks,” Wireless Pers. Commun., vol. 78, no. 1, pp. 231–246, Sep. 2014.   
[34] J. Shen, H. Tan, J. Wang, J. Wang, and S. Lee, “A novel routing protocol providing good transmission reliability in underwater sensor networks,” J. Internet Technol., vol. 16, no. 1, pp. 171–178, Jan. 2015.   
[35] A. Krause, A. Singh, and C. Guestrin, “Near-optimal sensor placements in gaussian processes: Theory, efficient algorithms and empirical studies,” J. Mach. Learn. Res., vol. 9, pp. 235–284, Feb. 2008.

![](images/3a7e3b773d77e218694cc9c4e42b440d0236cf33d65230e144567d30412ef65e.jpg)



Chaocan Xiang (S’10) received the B.S. and Ph.D. degrees in computer science and engineering from the Institute of Communication Engineering, PLA University of Science and Technology, Nanjing, China, in 2009 and 2014, respectively.

He is currently a Lecturer with Logistic Engineering University, Chongqing, China. He has published more than ten papers in peer-reviewed journals and refereed conferences, such as the IEEE TRANS-ACTIONS ON PARALLEL AND DISTRIBUTED SYS-TEMS, the IEEE SENSORS JOURNAL, and the IEEE

International Conference on Mobile Ad Hoc and Sensor Systems. His current research interests include wireless sensor networks, crowd sensing networks, and Internet of things.

![](images/1a2598cc399e2619bfcad2f1be82bf674bc81e6b0a14c6538b7571a2b7e58631.jpg)



Panlong Yang (M’02) received the B.S., M.S., and Ph.D. degrees in communication and information system from Nanjing Institute of Communication Engineering, Nanjing, China, in 1999, 2002, and 2005, respectively.

From September 2010 to September 2011, he was a Visiting Scholar with The Hong Kong University of Science and Technology, Hong Kong. He is currently an Associate Professor with the Nanjing Institute of Communication Engineering, PLA University of Science and Technology, Nanjing. He has published

more than 50 papers in peer-reviewed journals and refereed conference proceedings in the areas of mobile ad hoc networks, wireless mesh networks, and wireless sensor networks. His research interests include wireless mesh networks, wireless sensor networks, and cognitive radio networks.

Dr. Yang has served as a member of program committees for several international conferences. He is a member of the IEEE Computer Society and the ACM SIGMOBILE Society.

![](images/457e3a2a7bb4670ef2568b35dd4c8e6a93b089d1e2fba74f330bd76d633f114b.jpg)



Xuangou Wu received the Ph.D. degree from the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China, in 2013.

He is currently a Lecturer with the School of Computer Science and Technology, University of Anhui Technology, Ma’anshan, China. His research interests include wireless sensor networks, crowdsourcing, and compressive sensing.

![](images/cd71fc5f2aa4c8a652e566e30c23ba61907d3960761f5844ce628a192cc623af.jpg)



Baowei Wang received the B.S. and Ph.D. degrees in computer science from Hunan University, Changsha, China, in 2005 and 2011, respectively.

He is currently a Lecturer with the School of Computer and Software, Nanjing University of Information Science and Technology, Nanjing, China. His research interests include steganography, wireless networks, and securing ad hoc networks.

![](images/1aeaa56632004bcee00a939e4d055922449d3688f5f85d9d5bcfa1e0b78afaa1.jpg)



Yunhao Liu (SM’06–F’15) received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995 and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively.

Being a member of Tsinghua National Laboratory for Information Science and Technology, he holds a Tsinghua EMC Chair Professorship. He is the Director of the Key Laboratory for Information System Security, Ministry of Education, and is also a

Professor with the School of Software, Tsinghua University. He is also a faculty member with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong. His research interests include pervasive computing, peer-to-peer computing, and sensor networks.

![](images/f3174d4aba30b937d976674bc7b7f538eb6e1f5700d5cdfb59164d060953ec7b.jpg)



Hong He received the B.S. and M.S. degrees from Chongqing University, Chongqing, China, in 1985 and 1995, respectively.

He is currently a Professor with Logistic Engineering University, Chongqing. His current research interests include Internet of things, computer systems, and operations research.