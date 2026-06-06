# Human Mobility Enhances Global Positioning Accuracy for Mobile Phone Localization

Chenshu Wu, Student Member, IEEE, Zheng Yang, Member, IEEE, Yu Xu, Member, IEEE, Yiyang Zhao, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Global Positioning System (GPS) has enabled a number of geographical applications over many years. Quite a lot of location-based services, however, still suffer from considerable positioning errors of GPS (usually 1m to 20m in practice). In this study, we design and implement a high-accuracy global positioning solution based on GPS and human mobility captured by mobile phones. Our key observation is that smartphone-enabled dead reckoning supports accurate but local coordinates of users’ trajectories, while GPS provides global but inconsistent coordinates. Considering them simultaneously, we devise techniques to refine the global positioning results by fitting the global positions to the structure of locally measured ones, so the refined positioning results are more likely to elicit the ground truth. We develop a prototype system, named GloCal, and conduct comprehensive experiments in both crowded urban and spacious suburban areas. The evaluation results show that GloCal can achieve 30% improvement on average error with respect to GPS. GloCal uses merely mobile phones and requires no infrastructure or additional reference information. As an effective and light-weight augmentation to global positioning, GloCal holds promise in real-world feasibility.

Index Terms—GPS, mobile phone localization, human mobility

# 1 INTRODUCTION

Lobal positioning technology has enabled a great G number of yet-unimagined applications and attracted millions of civil users worldwide. Among all positioning techniques, Global Positioning System (GPS) [1] is widely adopted from industries such as aviation, nautical navigation, and land surveying, to personal applications such as driving navigation, object and individual tracking, and location sharing. Along with the popularity of mobile phones with built-in GPS, location information is available in more people’s pockets. Burgeoning markets of mobile phone applications such as locationbased social networks, geocaching, and geotagging, etc., are telling a true success story of the integration of GPS and mobile phones.

Although GPS has proven its availability and dependability over many years, many location-based services still suffer from considerable errors of GPS. Albeit the officially reported accuracy with high-quality GPS receivers can achieve 3 meters [2], the actual accuracy users attain from commodity smartphones ranges from 1m to up to 20m, which limits the uses of numerous applications, leaving room for various augmented technologies.

Generally, GPS accuracy is affected by a number of unavoidable factors, including satellite positions, atmospheric conditions, and the blockage to the satellite signals caused by mountains and buildings, etc. To overcome or bypass these factors, several augmentation systems, for instance, Assisted GPS (AGPS) [3], Differential GPS (DGPS) [4], and Wide Area Augmentation System (WAAS) [5], have been developed to aid GPS by providing accuracy, integrity, availability, or any other improvement that is not inherently part of GPS itself.

Conventional augmentation systems mostly rely on fixed reference locations, e.g., cell towers, and hence require specific infrastructure provided by either public or private sectors. Consequently, it is difficult for mobile phone users to embrace these augmentations any time at any place. Motivated by the proliferation of smartphones with rich internal sensors, we propose to enhance the accuracy of global positioning technology by utilizing local position information captured by only mobile phones.

Nowadays, mobile phones possess powerful computation and communication capability, and are equipped with various functional built-in sensors. These sensors enable so-called inertial sensing to characterize human mobility [6], [7]. Inertial sensing, a.k.a. dead reckoning, is means of calculating one’s current location by using a previously determined location and the estimations of displacement and direction moved. With internal sensors like accelerometer, gyroscope, and compass (or magnetometer), which, respectively, reveal the acceleration, rotational velocity, and direction of user motion, one user’s moving trajectory can be tracked by dead reckoning [8].

Phone-based dead reckoning supports accurate but local coordinates of users’ trajectories, while GPS provides global but inconsistent coordinates. This study aims at bridging phone-based dead reckoning and GPS to offer high-accuracy global positioning. We present GloCal (naming thanks to its connotation of ‘think GLObally and act loCALly’), a global positioning refinement approach via local trajectories tracked by mobile phones. The rationale behind GloCal is that global positions can be refined by fitting their structure to that of local positions, which is more accurate and hence eliciting the ground truth (Fig. 1a). To faithfully depict users’ trajectory, GloCal first employs a novel scheme for highly accurate dead reckoning on mobile phones. The dead-reckoned local trajectory and the global trajectory, obtained from a series of GPS measurements, are then converted to local and global coordinates in a 2D plane, respectively. On this basis, GloCal refines the originally inaccurate global positions by transforming the local coordinates into the global ones using a set of translation, scaling, and rotation operations, as illustrated in (Fig. 1b).

To evaluate our design, we implement a prototype on Android OS using Google Nexus S phones and conduct comprehensive experiments in both crowded urban and spacious suburban areas. The evaluation results suggest that GloCal can reduce 30% of global positioning errors of GPS with only negligible extra energy consumption, which demonstrates the feasibility of GloCal in real world deployment.

The major contributions are as follows.

• We propose a novel approach to improve global positioning accuracy using local trajectories delineated by mere mobile phones. GloCal requires neither additional infrastructure nor fixed reference points. GloCal works with one user using his mobile phone while walking in normal course, exerting no additional constraints to users. Besides GPS, other coarse-grained global positioning techniques like GSM- and WiFi-based localization can also benefit from this design.   
• We introduce a new scheme for smartphone-enabled dead reckoning, which achieves precise step counting, stride estimation, and direction reckoning, without any dependence on extra information such as digital maps or floor plans.   
• A coordinate transformation algorithm is introduced to achieve effective transformation between local and global coordinate system, which is agnostic to the specific localization techniques used. In other words, given two groups of localization results with different accuracy, the algorithm is universally capable of improving the precision of the less accurate one in its coordinate system.   
• We implement a prototype on commodity mobile phones and conduct real world evaluation in both urban and suburban areas. The results show that GloCal greatly reduces the average error of GPS from 5∼10m to around 3m, which was indicated empirically possible but only with dedicated infrastructure or high-quality receivers.

The rest of this paper is organized as follows. Section 2 introduces the system design of GloCal. A novel scheme for dead reckoning, as well as the local and global coordinate generation, is presented in Section 3. Section 4 illustrates how to transform the local coordinate system to the global one. In Section 5, we provide the experiments and evaluations. We review related works

![](images/ec4c678fd647a8e85949d9cc3b9a05c65e853e6cc61924f8735a42a1d89233a0.jpg)



(a) An illustration of user trajectory with both GPS and local measurements. For the ease of visualization, distances between footprints are larger than the facts.

![](images/0b29dd20fa410d61ffa85a960d5149892062df030a23527f399f8ca4d510bfa9.jpg)



(b) Refine global positions with transformed local coordinates

Fig. 1. Global positions refined by local footprints elicit the ground truth fantastically well.

in Section 6 and conclude the work in Section 7.

# 2 OVERVIEW AND CHALLENGES

We first present the system architecture of GloCal, followed by the challenges faced.

As shown in Fig. 2, the working process of GloCal consists of two core phases: coordinate generation and coordinate transformation. Imagine that when a user uses navigation in some scenic, he may turn to global positioning services for desired locations using his mobile phone. At this point, apart from the global locations, GloCal records the internal sensor readings of the mobile phone that is equipped with accelerometer, gyroscope, and compass, etc. These consecutive global locations along the user trajectory form a global coordinate system, while the local measurements from inertial sensors will construct a local coordinate system.

GloCal characterizes and exploits user mobility to attain local position information. Analogous to conventional dead reckoning techniques, GloCal leverages various sensors to infer user walking characteristics and further to depict the entire user trajectory. Specifically, GloCal uses accelerometer to identify user walking steps and gyroscope to estimate moving directions. Acceleration feature is further investigated to determine the accurate stride length of a specific user. The walking displacement is then derived by multiplying the step counts with the stride length. Provided that the displacement and direction are available, a user trajectory beyond GPS is obtained and a local coordinate system, namely, the relative locations, is accordingly delineated.

![](images/3381088a8b2a5a7e9dc18aae778750f033ec775964438f42098c598bb82276b7.jpg)



Fig. 2. System architecture of GloCal

Observing that the dead-reckoned local positions preserve the structure of ground truth trajectory better than the global positions obtained from GPS, GloCal therefore intends to improve the global positioning accuracy by fitting the global positions to the local ones. The best fitting is achieved by realizing an optimal transformation, including a set of translation, scaling, and rotation operations, that converts the local coordinates exactly into the global ones, minimizing the sum of squares of residual errors. All global positions along the user trajectory are concurrently refined with the transformed local positions once the optimal transformation is accomplished.

The intuitive idea of GloCal involves great challenges:

1) Given the fact that the internal sensors are noisy and that even tiny errors might be rapidly magnified by integration, realizing accurate dead reckoning is non-trivial. While direct integration over time is subject to accumulative errors and is proved to be unfeasible in practice, the method of step counts predominant in the literature is an alternative [6], [9]. However, the difficulty still remains since that the stride lengths vary from user to user and from scenario to scenario.

2) Since the two coordinate systems are constructed by measurements from different techniques and thus are completely independent from each other, how to benefit from the local position information to upgrade the global positioning accuracy?

The following section details our novel dead reckoning scheme and Section 4 addresses the challenges in harnessing the local coordinates.

# 3 COORDINATE GENERATION

In this section, we first present a novel scheme for smartphone-enabled dead reckoning to depict users’ traveling trajectory. On this basis, the generation of local and global coordinates is introduced, respectively.

![](images/64b5bba61890469e5644c0e4b635690e72bd7f6fa80460f206635262059f8f7e.jpg)



Fig. 3. A finite state machine for step detection

# 3.1 Local Position Measurements

GloCal uses the accelerometer in combination with gyroscope sensors to infer user walking characteristics, particularly, the displacement and the direction.

# 3.1.1 Displacement Ranging

In principle, the displacement user traveled can be directly obtained by integrating the acceleration twice with respect to the time. However, error accumulates rapidly due to the presence of noise in accelerometer readings. To avoid accumulation of calculation errors, we adopt the individual step counts as a metric of walking distance instead, as do many other work [7], [8], [10]. Then the problem of displacement ranging is decomposed into two tasks: robust step counting and accurate stride estimation.

The rationality behind step counts is that the accelerations exhibit periodically repetitive patterns, which arises from the nature rhythmic of human walking, as shown in Fig. 4. We thoroughly investigate this property and design a novel step counting algorithm based on the finite state machine (FSM). As shown in Fig. 3, there are 8 states involved in the FSM, modeling the process of one normal human step, which generally includes processes of foot lifting up, moving ahead, and dropping down. In addition to the accurate results (Refer to supplementary file for more details), the algorithm is advantageous in detecting the starting and ending points of each step, which is, to our best knowledge, beyond attainment of most conventional approaches [7], [8], [10] and lays the foundation for following direction reckoning.

To convert the step counts into displacement, GloCal needs the accurate stride length estimation. Previous solutions [8], [10] mostly assume a fixed stride length of a person according to his weight and height. As is well known, however, stride length can vary widely from user to user and from scenario to scenario, making the fixed length estimation inaccurate or even unusable. Some other approaches appraise stride length by carefully modeling the acceleration data [11] or by using an augmented particle filter [7]. However, these works either tend to be too sensitive to the noisy sensors or rely on additional information, limiting the feasibility and ubiquity on mobile phones.

Different from traditional approaches, GloCal uses a learning based method to estimate the stride lengths. As can be observed from Fig. 5, accelerations of users with different stride lengths exhibit considerable different characteristics such as variance, yet evince similarly repetitive patterns. We validate this design on real users in Section 5 and the results indicate reasonable accuracy.

![](images/4a062eecfd05e4fd2a83c8f934feb15979583f85cab0f53a7bf88d534c9bb067.jpg)



![](images/4a2a45cb12bb515d60c9e2914a43e141928207eeeb6376495dbf1b3c6a7de587.jpg)



![](images/f5f7e4da9382428903379ba116781629e3d1b34de0b8d346bdc1630f340e354e.jpg)



Fig. 4. Results of FSM based step Fig. 5. Walking patterns of users with Fig. 6. Local coordinate system gencounting algorithm different strides eration

# 3.1.2 Direction Reckoning

A lot of previous work leverage compass to estimate user orientation, while some also take gyroscope into consideration. Compass reveals the absolute orientation relative to the surface of the earth conveniently, but is usually pretty noisy. [8], [10]. Since GloCal solely leverages user mobility to construct a relative coordinate system, the absolute orientation is not necessary involved. Consequently, GloCal is free of using the noisy compass and employs solely the gyroscope, which provides accurate angular velocity of human motion, to infer the changes of direction during every step. The method is fairly intuitive: integrating the angular velocity captured by the gyroscope with respect to time within the interval of a step (detected by the FSM-based algorithm). Due to the high sampling frequency of gyroscope (about 800Hz with our experimental phones) and its insensitivity to magnetic fields, the direction changes can be precisely estimated and hence the structure of a user path can be well identified, which is exactly what GloCal desires.

Dead-reckoning is well known to suffer from accumulative errors over time [7], [10], [12]. We have significantly reduced such accumulative errors by employing step counting and stride length estimation, which are both immune to cumulative errors. The direction estimation, however, still experiences accumulative errors over time. Although the accumulative errors in direction estimation can be calibrated by leveraging digital compass [8], we shy away them by using only short trajectories that are free from severe accumulative errors for coordinate transformation (detailed in next section). For excessively long traces, we break down them into shorter parts and employ piecewise operations.

# 3.2 Local Coordinate System

If the displacement and changes of direction of each step are known, we can build a Cartesian coordinate system, namely, the local coordinate system, to portray the trajectory. Given a trajectory $\mathbb { S } ~ = ~ \{ s _ { 1 } , s _ { 2 } , \cdot \cdot \cdot ~ , s _ { N } \}$ of $N$ steps, each step $s _ { j }$ corresponds a displacement $d _ { j }$ and a direction change $\gamma _ { j }$ . Treating each step as a point and the start of the first step $s _ { 1 }$ as the origin with coordinates $( 0 , 0 )$ , the coordinate of each point can be obtained, where the direction of the vector from $s _ { 1 }$ to $s _ { 2 }$ is defined as that of the x axis and the orthogonal vector is y axis. As shown in Fig. $^ { 6 , }$ assuming the coordinates of step $s _ { j - 1 }$ (point A) is $( x _ { j - 1 } , y _ { j - 1 } )$ , then the coordinates of the next step $s _ { j }$ (point B) can be calculated as

$$
(x _ {j}, y _ {j}) = (x _ {j - 1} + d _ {j} \cos (\phi + \gamma_ {j}), y _ {j - 1} + d _ {j} \sin (\phi + \gamma_ {j})), \tag {1}
$$

where ϕ = ∑j−1p=1 γ $\begin{array} { r } { \phi = \sum _ { p = 1 } ^ { j - 1 } \gamma _ { p } } \end{array}$ p is the separation angle of vector OA⃗ $\vec { \mathrm { O A } }$ and the x axis. Noting that in GloCal the $\gamma _ { j }$ is negative if the direction change is clockwise, otherwise positive.

Actually, it is not necessary to calculate the coordinates of each step in practice. Since the energy-hungry GPS is usually not such frequent as step rate, we only need to take into account those steps which are accompanied with global positioning stamps, which results in lower computation complexity and fewer energy cost.

# 3.3 Global Coordinate System

Global positioning technology reports geographical locations on the spherical surface of the earth. Such geographical coordinates are usually in the form of (λ, ψ) (without loss of rigor, we consider the elevation to be zero), where λ and ψ denote the longitude and latitude (in degrees), respectively. As we assume the global coordinate system and the local one are co-planar, such geographical coordinates must be converted into 2D Cartesian coordinates.

Fortunately, GPS reported geographic coordinates can be accurately converted to Universal Transverse Mercator Grid System (UTM) format [13]. UTM is a formal, globally referenced planimetric coordinate system, and is also the most common map standard today (supported by most GPS receivers). In UTM, a point is located by specifying a hemispheric indicator, a zone number, an easting value, and a northing value. The coordinates are in the form of (E, N ), where E and N denotes the easting and northing values (in meters), respectively. In GloCal, we convert all GPS readings in the form of longitude and latitude to the UTM format based on formulas mentioned in [13] for further processing.

# 4 COORDINATE TRANSFORMATION

At this point, we have obtained both the local and global coordinates. In the following, we present how to improve the global positioning accuracy by harnessing local positions. Our method is based on transforming the local coordinate system into the global one using a set of translation, scaling, and rotation operations based on Horn’s method [14].

Horn presented a closed-form solution of absolute orientation problem using unit quaternions in 2D and 3D space in [14]. Absolute orientation [15] is referred to finding the relationship, i.e., recovering the transformation, between two coordinate systems using pairs of the coordinates of a number of points in both systems, which is a classical problem in photogrammetric and in robotics. Horn’s solution uses unit quaternions to represent rotation in 3D space. In GloCal, assuming the local and global coordinate systems are both in a plane, unit quaternion is not necessary used. Instead, we use complex numbers to denote the coordinates of points, for which the rotation can be represented as a multiplication between numbers, and derive a form of optimal transformation.

# 4.1 Problem Formulation

Since the local trajectory will generally contain much more points than the GPS sampling points, (i.e., the global coordinate counts), and the two coordinate systems are obviously independent from each other before the transformation is done, it is necessary to align the point number as well as to associate the corresponding points between the two coordinate set. In GloCal, the point number is preferentially determined by the global coordinate system. The local coordinates are then aligned by filtering the timestamps. That is, for each global point, the local point which has the closest timestamp is selected as the associated point. By doing this, both coordinate systems consist of the same number of oneto-one corresponding points.

Assume there are n points in the local coordinate system, denoted as $\mathbb { L } = \{ \pmb { w } _ { j } , j = 1 , \dots , n \}$ , and n corresponding points in the global coordinate system, denoted as $\mathbb { G } = \{ z _ { j } , j = 1 , \dots , n \}$ . Instead of a 2-dimensional vector, each point is represented as a complex number, $\mathrm { i . e . , ~ } z _ { j } = z _ { x , j } + i z _ { y , j } , \ : w _ { j } = w _ { x , j } + i w _ { y , j }$ . According to [14], the transformation between these two coordinate systems L and G can be thought of a rigid-body motion and can thus be decomposed into a translation, a scaling, and a rotation. In other words, the problem is to look for a transformation of the form

$$
\boldsymbol {w} ^ {\mathrm{g}} = s R \left(\boldsymbol {w} ^ {1}\right) + \boldsymbol {t} _ {0} \tag {2}
$$

from the local to the global coordinate system, where $\pmb { w } ^ { 1 } \in \mathbb { L } , \pmb { w } ^ { \mathrm { g } }$ is the corresponding transformed one in global coordinate system, s is a scale factor, $\scriptstyle t _ { 0 }$ is the translational offset, and $R ( w ^ { 1 } )$ denoted the rotated version of $w ^ { 1 }$ . Unless the data are perfect, we will not be able to find a transformation such that the equation above is satisfied for each pair of points in L and G. Hence, the optimal solution aims to minimize the sum of squares of the residual errors:

$$
\sum_ {j = 1} ^ {n} \left\| e _ {j} \right\| ^ {2} = \sum_ {j = 1} ^ {n} \left\| z _ {j} ^ {\mathrm{g}} - w _ {j} ^ {\mathrm{g}} \right\| ^ {2}, \tag {3}
$$

where $z _ { i } ^ { \mathrm { g } } \in \mathbb { G }$ and $e _ { j }$ is the residual error between $z _ { j } ^ { \mathrm { g } }$ and $\pmb { w } _ { i } ^ { \mathrm { g } }$ .

As Horn’s solution does, we consider the total residual errors first with translation, then with scaling, and finally with respect to rotation.

# 4.2 Translation

First of all, we refer all positions to centroids defined by

$$
\bar {\boldsymbol {z}} ^ {\mathrm{g}} = \frac {1}{n} \sum_ {j = 1} ^ {n} \boldsymbol {z} _ {j} ^ {\mathrm{g}}, \quad \bar {\boldsymbol {w}} ^ {\mathrm{l}} = \frac {1}{n} \sum_ {j = 1} ^ {n} \boldsymbol {w} _ {j} ^ {\mathrm{l}}, \tag {4}
$$

and derive the following new coordinates: $z _ { j } ^ { \bar { \mathrm { g } } } = z _ { j } ^ { \mathrm { g } } -$ z¯ g , $\mathbf { \Delta } \mathbf { w } _ { j } ^ { \mathrm { l } } = \mathbf { w } _ { j } ^ { \mathrm { l } } - \bar { \mathbf { w } } ^ { \mathrm { l } }$ .Note that $\begin{array} { r } { \sum _ { j = 1 } ^ { n } z _ { j } ^ { \bar { \mathrm { g } } } = 0 } \end{array}$ ∑n , ∑nj=1 $\begin{array} { r } { \dot { \sum _ { j = 1 } ^ { n } } \pmb { w } _ { j } ^ { \bar { \mathbf { l } } } = } \end{array}$ 0.The residual error can be rewritten as

$$
\boldsymbol {e} _ {j} = \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} - \boldsymbol {w} _ {j} ^ {\bar {\mathrm{g}}} = \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} - s R (\boldsymbol {w} _ {j} ^ {\bar {\mathrm{l}}}) - \bar {\boldsymbol {t}} _ {0}, \tag {5}
$$

where $\bar { \pmb { t } } _ { 0 } = \pmb { t } _ { 0 } - \bar { z } ^ { \mathrm { g } } + s R ( \bar { w } ^ { \mathrm { l } } )$ . The sum of squares of the residuals becomes

$$
\sum_ {\substack {j = 1 \\ n}} ^ {n} \left\| \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} - s R \left(\boldsymbol {w} _ {j} ^ {\bar {\mathrm{l}}}\right) + \bar {\boldsymbol {t}} _ {0} \right\| ^ {2} \tag{6}
$$

$$
= \sum_ {j = 1} ^ {n} \| S \| ^ {2} + 2 \bar {\boldsymbol {t}} _ {0} \cdot \sum_ {j = 1} ^ {n} S + n \| \bar {\boldsymbol {t}} _ {0} \| ^ {2}
$$

where $S = z _ { j } ^ { \bar { \bf g } } - s R ( w _ { j } ^ { \bar { \bf l } } )$ and $\textstyle \sum _ { j = 1 } ^ { n } S$ equals zero, since all positions are referred to their centroids. Thus we are left with the first and last term of this expression. The first is independent from $\bar { \mathbf { t } } _ { 0 }$ while the last cannot be negative. The sum will be evidently minimized when $\bar { \mathbf { t } } _ { 0 } = \mathrm { ~ \bar { 0 } , ~ o r ~ }$

$$
\boldsymbol {t} _ {0} = \bar {\boldsymbol {z}} ^ {\mathrm{g}} - s R (\bar {\boldsymbol {w}} ^ {\mathrm{l}}). \tag {7}
$$

That is, the optimal translation is just the difference of the global centroid and the scaled and rotated local one. As both centroids are known if given the two sets of positions, the optimal translational offset, $\mathrm { i . e . , } t _ { 0 } ,$ can be derived once the scale and rotation factors are found.

# 4.3 Scaling

At this point, assuming that the optimal translation is given as ${ t _ { 0 } = \bar { z } ^ { \mathrm { g } } - s R \mathrm { ( } \bar { w } ^ { \mathrm { l } } \mathrm { ) } }$ , we have $\hat { \bar { t } } _ { 0 } = 0$ and hence the sum of squares of the residual errors can be written as

$$
\sum_ {j = 1} ^ {n} \left\| \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} - s R (\boldsymbol {w} _ {j} ^ {\bar {\mathrm{l}}}) \right\| ^ {2}. \tag {8}
$$

Expanding the above term to complete the square form in s and noting that $\parallel R ( \pmb { w } _ { j } ^ { \bar { 1 } } ) \parallel ^ { 2 } = \parallel \pmb { w } _ { j } ^ { \bar { 1 } } \parallel ^ { 2 } .$ , we have

$$
\sum_ {j = 1} ^ {n} \left\| \boldsymbol {w} _ {j} ^ {\bar {1}} \right\| ^ {2} [ s - F ] ^ {2} + \sum_ {j = 1} ^ {n} \left\| \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} \right\| ^ {2} - \sum_ {j = 1} ^ {n} \left\| \boldsymbol {w} _ {j} ^ {\bar {1}} \right\| ^ {2} F ^ {2}, \tag {9}
$$

![](images/81831916ffd73db68de38b0390e1644a0fc40f215f608127c6891106fb55d0a6.jpg)



(a) Urban areas (180m×190m)

![](images/19f765dda438649064e0103840a159e7aeb63f1eb091a5748c6bbc5717f47025.jpg)



(b) Suburban areas (245×190m)   
Fig. 7. Experiment areas in the New Technology District of Wuxi City

where $\begin{array} { r } { F = \frac { \sum _ { j = 1 } ^ { n } \pmb { z } _ { j } ^ { \bar { \bf g } } \cdot R ( \pmb { w } _ { j } ^ { \bar { 1 } } ) } { \sum _ { i = 1 } ^ { n } \| \pmb { w } _ { i } ^ { 1 } \| ^ { 2 } } } \end{array}$ ∑nj=1∥w¯lj ∥2 .To minimize the above expression with respect to scale $s ,$ the first square term should be set zero, that is, $s = F$ .

# 4.4 Rotation

At present, the only remaining task is to find the rotation in the plane of global coordinate system. By doing this, final complete solution of the position transformation problem will be achieved.

The optimal rotation should minimize the sum of squares of distances between corresponding points of local and global coordinates [14], say, minimize

$$
\sum_ {j = 1} ^ {n} \left\| \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} - R (\boldsymbol {w} _ {j} ^ {\bar {\mathrm{l}}}) \right\| ^ {2}. \tag {10}
$$

As the local and global coordinate systems are coplanar, there is an angle between corresponding positions $z _ { j } ^ { \bar { \mathrm { g } } }$ and $\pmb { w } _ { j } ^ { \bar { 1 } } .$ , denoted as $\alpha _ { j } .$ . In other words, $z _ { j } ^ { \bar { \bf g } } \cdot w _ { j } ^ { \bar { \bf l } } = \parallel z _ { j } ^ { \bar { \bf g } }$ ∥∥ $\mathbfit { w } _ { j } ^ { \bar { 1 } } \parallel$ cos $\alpha _ { j } .$ . Let θ denote the angle the global coordinates have rotated. The above term can be expanded as follows since the angle $\alpha _ { j }$ is reduced by θ.

$$
\sum_ {j = 1} ^ {n} \left\| z _ {j} ^ {\bar {\mathrm{g}}} \right\| ^ {2} + \sum_ {j = 1} ^ {n} \left\| w _ {j} ^ {\bar {1}} \right\| ^ {2} - 2 \sum_ {j = 1} ^ {n} \left\| z _ {j} ^ {\bar {\mathrm{g}}} \right\| \left\| w _ {j} ^ {\bar {1}} \right\| \cos (\alpha_ {j} - \theta). \tag {11}
$$

To minimize Eqn. 11, we need to maximize the last term, or A cos $\theta + B$ sin θ,where $\begin{array} { r } { \underline { { A } } ~ = ~ \sum _ { j = 1 } ^ { n } ~ \| ~ { \boldsymbol z } _ { j } ^ { \bar { \mathrm { g } } } ~ \| \| ~ { \boldsymbol w } _ { j } ^ { \bar { \mathrm { l } } } } \end{array}$ ∥ cos $\begin{array} { r } { \alpha _ { j } , B = \sum _ { j = 1 } ^ { n } \parallel z _ { j } ^ { \mathrm { g } } \parallel \parallel \pmb { w } _ { j } ^ { \mathrm { l } } } \end{array}$ ∥ sin $\alpha _ { j }$ .This term achieves extremum when A sin $\theta = \check { B }$ cos θ, that is,

$$
\theta = \arcsin \pm \sqrt {\frac {B ^ {2}}{A ^ {2} + B ^ {2}}}, \tag {12}
$$

one maximizing, and one minimizing Eqn. 10.

Accomplishing the coordinate transformation, global positions are aligned to their corresponding transformed local ones, which delineate the structure of true trajectory better. In other words, a global position $\bar { z } _ { j } ^ { \mathrm { g } }$ is replaced with $\bar { \pmb w } _ { j } ^ { \mathrm { g } }$ .

# 5 EXPERIMENTS

To evaluate the proposed approach, we implement a prototype system of GloCal on the increasingly popular Android platform and collected data in both urban and suburban areas. In this section, we first detail the experiment environments and methodology, followed by the evaluation of each components. Finally, the overall performance of GloCal is presented.

# 5.1 Experiment Methodology

We implemented GloCal on Android OS using Google Nexus S phones, which are equipped with accelerometers, gyroscopes, and compasses, and as well support GPS functions. The accelerometers and gyroscopes are amenable of a respective frequency of around 50Hz and 800Hz, while the GPS unit can report new data once locations change (around a period of 1 second). In the prototypal GloCal, we set the sampling rate of all sensors and GPS to be as high as possible to record redundant information for the purpose of comprehensive evaluation and analysis.

Our experimental environments are twofold: a builtup urban region around an academic building (Fig. 7a) and a spacious suburban area (Fig. 7b). Generally, raw GPS exhibits different accuracy in these two areas due to distinct natural environments. Trajectories are collected from users automatically when they are walking naturally and using their mobile phones for navigation. Each trajectory contains a sequence of global positioning reports and a series of sensor records. All raw sensor data are first sanitized with a lowpass filter for further uses, while accelerometer readings are additionally compensated for gravity.

Note that no extra behavior constraints are exerted to users for data collection. To obtain the ground truth geographical positions of the paths user traveled for evaluation, however, users have to walk along our predefined paths depicted on a map. The real position information can then be acquired by carefully putting the routes into handy digital map services, for instance, Google Maps, as shown in Fig. 7a and Fig. 7b.

# 5.2 Performance Evaluation

# 5.2.1 Local Positioning Performance

We first evaluate the performance of local positioning, i.e., user trajectory delineation based on dead reckoning, and validate the underpinning that the local positioning preserves the structure of the ground truth picturesquely.

Step Counting Accuracy. We test the FSM based step counting algorithm on 3 users by collecting 8 traces from their natural walking with various lengths ranging from 10 steps to 300 steps, which are counted by the users themselves and used as ground truth. Integrating the results from 24 traces, we inspect the impact of the threshold (negPeak and posPeak in Fig. 3) in Fig. 8a. Obviously, more than 95% traces are counted precisely of less than 5 step error when using peak values within an appropriate range, from 1.0 to 1.4 in our experiments. Furthermore, we compare the performance of the proposed algorithm with previous methods, including the threshold-based [8] and peak-based [10], on 90 traces of different lengths from 9 users. As shown in Fig. 8b, the proposed FSM-based approach consistently outperforms traditional methods. The improvements are achieved by elaborately describing a series of state transitions during human footsteps, while previous methods can be easily affected by single abnormal sensor measurement. Addition to the robustness to noisy sensor and arbitrary users, another excellent property of the proposed algorithm lays on its irrelevance to the number of steps, thus mingling no accumulative error concerns.

![](images/1844630ca3a12ae72a3519cbdd9e59fc1e4d8028cd879fad1ccaaf0e9e1f4a21.jpg)



(a) Step count accuracy with various thresholds

![](images/0b97ebda6b136c74ee320564269301b50eee75db77d28e0ac81a5f8a06fcb0bb.jpg)



(b) Comparison with traditional methods

![](images/0376d591a609e234d2781319aacca520193d72e3be5ebf24bb8862141b1dcb7b.jpg)



Fig. 9. Stride estimation accuracy with different size of training data   
Fig. 8. Step counting accuracy

Stride Length Estimation Accuracy. We collect training data from totally 20 training users with various heights and weights. All users are asked to walk along two pre-defined paths, one with length of 20m and the other of 30m, both in a normal manner. One user’s actual stride lengths (in different traces) are measured as the quotients of the path length to the manually counted steps he took. We train the model using three different sets of training data and evaluate the estimation accuracy on 15 testing users in each case. As shown in Fig. 9, the estimation accuracy is reasonably high, yet not perfect, and increases with the size of sample data as well as the number of training users. Nevertheless, the proposed method does not rely on large amount of training data since a small number of training samples can already provide satisfactory accuracy. For instance, the stride estimation error is only about 8cm using 40 samples from 20 users though it can further decreases to about 6cm with more samples. In addition, it should be pointed out that slight errors in stride length estimation, albeit do exist, can be gracefully tolerated since a scaling factor has been taken into account in the coordinate transformation.

Dead Reckoning Performance. Concerning that whether local positioning could produce precise depiction of users’ real trajectories, we now fuse the outcome of step counting, stride estimation, and direction reckoning to illustrate an intuitively qualitative picture of the local coordinates of 6 user traces with different shapes. As shown in Fig. 10, it can be perceptively seen that the structure of most user traces can be precisely resuscitated by local measurements. Although some trajectories does not necessarily match the ground truths precisely, e.g., case as shown in Fig. 10b, they still perform much better than the global traces. Such results confirm our basic postulation that locally dead-reckoned trajectories preserve the truthful structure better than the global GPS measurements and thus guarantee the correctness and effectiveness of the proposed approach.

# 5.2.2 Positioning Accuracy

Now we turn to the accuracy improvement of GloCal over GPS. We first evaluate the accuracy of raw GPS with commodity mobile phones. With our experimental phones, the average location error from 14 measurements over one week in urban areas is 5m∼8m. In the following, we inspect various factors that might influence the performance of GloCal. Briefly, three parameters are given our attention: the point number n involved in the coordinate system, the unit distance d between adjacent sample points on a trajectory, and the shapes of trajectories.

Impact of point number. To see impact of n, we set n range from 5 to 100 for a long trajectory and integrate the results on all scenarios. Fig. 11 illustrate the effect of n with d=1.5m, 2.5m, and 3.5m, respectively. Obviously, on all unit distances, the positioning errors are significantly reduced with the increase of the number of points used. Such impressive results are natural since that more points forms longer trajectory and thus the influence of those strong misaligned GPS measurements is avoided to a certain extent.

Impact of unit distance. From Fig. 11, one can more or less see that the positioning accuracy also increases when using longer unit distance d. To further validate this point, we examine the accuracy improvements on various d with fixed n. As depicted in Fig. 12, the results pan out as we expected that positioning error does decrease when d lengthens. On one hand, we suspect that such results benefit from the better transformation residual errors under larger unit distances, which resulting sparser sample points and thus relaxed structure constraints. On the other hand, with an identical point number, larger unit distances means longer (but not excessively long) trajectories, which produces superior performance. Albeit counter-intuitive, this crucial property strengthens GloCal’s feasibility and practicability as the performance can be consistently guaranteed even with low GPS sample frequency (which correspondingly means large unit distances).

![](images/c2ba53961e94465e65305b0495aa552cc99e88864d6ec9fd7d70df1a74c7399d.jpg)



(a) Trace I in urban areas

![](images/d369d59bd52a87a48898ae2a0be4cf59fcf115da5a1cb90d8b5196af1c469f7e.jpg)



(b) Trace Z in urban areas

![](images/23278149c98750cf8746aa76597dd8d9cfe40b59cc5b906160f5292400e084c4.jpg)



(c) Trace S in suburban areas   
Fig. 10. Local-generated trajectories preserve the structures of ground truth paths precisely.

Impact of trajectory shape and raw GPS distribution. Apart from the two key parameters, i.e., point number n and unit distance d, we also observe that accuracy of GloCal has no noticeable relevance to the structure of trajectories, yet is directly influenced by the distribution of raw global measurements. As portrayed in Fig. 13, GloCal achieves significant improvement on various trajectories. However, we observe that when raw GPS measurements deviate the true positions heavily, the accuracy GloCal could achieve will also be limited, Nevertheless, one can always see that GloCal improves the global accuracy under all experimental scenarios, which demonstrates its effectiveness in practical usage.

Fusing all results together, we plot the respective accuracy of GloCal in urban and suburban areas in Fig. 14a and Fig. 14b, and incorporate them to derive the overall accuracy in Fig. 14c. All results show that an impressive improvement of 20%∼30% over raw GPS is achieved while the average error is limited under 4m. This accuracy also outperforms the dead-reckoningonly method [8], which provides an average accuracy of 11m in urban regions. We believe GloCal sets up an unconventional perspective and provides a practical way to improve GPS accuracy using mobile phone only, with negligible extra energy consumption compared to the GPS only mode.

# 6 RELATED WORK

# 6.1 Global Positioning Technology

Global positioning technologies, like GPS, GLONASS, and Galileo, have revolutionized a range of locationawareness services with their global coverage and outstanding performance [16]. However, many applications still suffer from global positioning errors due to various factors [1]. For the dominant GPS, several augmentation systems are developed to provide accuracy, availability, or any other improvement. AGPS [3] assists GPS by gaining information via a wireless network, such as the GPS receivers on cell towers which have been accurately located, to relay the satellite information to the receiver. DGPS [4] looks for differences between the satellitelocated positions and the known fixed positions, and broadcasts such differences to the receivers to provide better accuracy. A most recent GPS augmented system is the Wide Area Augmentation System (WAAS) [5], a satellite-based augmentation system operated by the Federal Aviation Administration (FAA), which supports aircraft navigation across North America. Other augmentation systems include IGS, CORS, LAAS, etc [2]. Either relying on fixed reference stations with exactly known locations, or requiring constant network connections, all these augmentation systems need to be run by special operators and are available only in limited areas.

On the other hand, considering problems with GPS beyond accuracy, including poor indoor supports, large battery consumption, and long acquisition time, innovated algorithms and alternative solutions to global positioning are proposed. QuickSync [17] presents a fast GPS synchronization algorithm taking advances in iFFT. Leveraging publicly available information such as GNSS satellite ephemeris and an Earth elevation database, CO-GPS [18] allows a mobile devices to obtain good quality GPS locations from a few milliseconds of raw GPS signals by postprocessing in cloud. Place Lab [19] uses GSM and WiFi signals as fingerprints for localization. Active Campus [20] adopts an idea similar to Place Lab, but assumes that locations of WiFi access points are available a prior. Taking advantage of the millions of WiFi access points throughout populated areas, Skyhook [21] developed a location system for localization indoors and in urban areas, as a supplementary to GPS. While only providing coarse-grained location information, from tens to hundreds of meters, GSM/WiFi based positioning technologies also require war-driving in the target areas to acquire GPS coordinates corresponding to GSM/WiFi fingerprints. In addition, these works all aim at supplementing the coverage of GPS, instead of improving the original GPS accuracy.

# 6.2 Mobile Phone Localization

The mobile phone localization literature is indeed vast. In the space of interests, we only review the most relevant and representative prior work. In particular, we survey the works attempting to leverage inertial sensing to characterize human mobility for localization.

![](images/71f9c1ca98ba35196248f293691eb254749270289152988333661d3772c5faae.jpg)



(a) d = 1.5m

![](images/6bfe1cd22e4e97fcd265db24ba74603444731a3189de34e915ab1a07f35304ba.jpg)



(b) d = 2.5m

![](images/d77aeece4d23d9544a4a871ae4b80cb8d60266785c5a9e77b2cc927bef20f421.jpg)



(c) d = 3.5m

Fig. 11. Positioning error decreases with larger numbers of points used.   
![](images/00e71e5a74d533c82bb20b7d0eeeac624efb422fa9ae6710b1cbd36a1a7c09cd.jpg)



(a) n = 40

![](images/98531aa760930f54bb8dff5dc4196df95125d679069fa2e3be0895365abbf532.jpg)



(b) n = 50

![](images/660cc0be52c13d40c9bac3e44cbae0b2c182bd19bf6a432f8d0a39ea98c43fd6.jpg)



(c) n = 60

Fig. 12. Positioning accuracy increases with larger unit distances.   
![](images/3e79d9ca8ca101be4f9c12c081293c745d8f28d1e9619c314f1a988848a04a36.jpg)



(a) Trace I in urban areas

![](images/02659b9eb136b020b2d148fdb1a19a0a11f913d7422a473b1697b3e614b7ab4c.jpg)



(b) Trace Z in urban areas

![](images/2410161479b70a57b009e3a8c7ba4400967de3e4a4685e2377354c5fb820e04d.jpg)



(c) Trace S in suburban areas   
Fig. 13. Positioning accuracy in crowded urban areas and spacious suburban areas.

Adhere to the thinking of marine or air navigation, known for centuries, smartphone-enabled dead reckoning is well-studied for both indoor and outdoor localization. [9] combines a foot-mounted inertial unit, a detailed building model, and a particle filter to provide absolute positioning. Considering the energy issues, GAC [22], CompAcc [8], and WheelLoc [23] all provide localization in outdoor environments, depending mainly on the accelerometer and compass sensors and using the GPS infrequently for initialization and recalibration. Concerning GPS is unavailable indoors, recent work Unloc [10] identifies indoor landmarks with unique WiFi (and magnetic or accelerometer) signatures in an unsupervised way for zero-calibration localization, while Zee [7] too enables zero-effort indoor localization by placing deadreckoned user paths into an indoor map, according to the constraints imposed by the map. Considering human mobility together with radio fingerprint space, LiFS [6] successfully releases the site survey process of traditional indoor localization by applying human motions to connect previously independent radio fingerprints and construct a fingerprint space.

GloCal differs from previous works towards mobile phone localization in two folds: Firstly, GloCal aims at improving the GPS accuracy by using inertial sensing as a second, local localization while most previous works leverage dead-reckoning as an alternative to GPS to reduce the energy consumption and extend the service coverage. Secondly, GloCal uses dead-reckoning in a diametrically different way compared to previous works. Previous works require additional reference information, such as GPS [8], indoor landmarks [10], and digital floor plans [7], to initialize and recalibrate the dead-reckoned positions. In contrast, desiring solely the relative trajectories, GloCal is free of using any reference information or extra infrastructure and thus is more practical and feasible in real-world applications.

![](images/be545607f2081805cb32587e2f0192600b9be78a9750c57d19843b0b532668e6.jpg)



(a) Overall accuracy in urban areas

![](images/25e5f44f2605345bc668efd0a016cd25d38533b4804d28986bc33efd6775a7ea.jpg)



(b) Overall accuracy in suburban areas

![](images/d708f24a97c4abe2fd1783f4cceeaf29b4f579bfa3c6191900edca6651f3b566.jpg)



(c) Overall accuracy of GloCal   
Fig. 14. Overall positioning accuracy

# 7 CONCLUSION

In this paper, we propose an innovative approach to improve global positioning accuracy using user trajectories measured by commodity mobile phones, without any dependence on either fixed infrastructure or additional reference information. We design a novel smartphoneenabled dead reckoning technique, including step counting, stride estimation, and direction reckoning, to accurately delineate users’ locomotion. On this basis, the global positioning accuracy is refined by fitting the less accurate global positions to the structure of the more precise local trajectories. The preliminary experiment results in urban and suburban areas suggest that GloCal can achieve 30% improvement on GPS average accuracy, demonstrating its promise in real-world feasibility. Our ongoing work focuses on pursuing GloCal to assist GPS positioning for vehicles and unmanned aircrafts.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program under grant No. 61190110, National Basic Research Program of China (973) under grant No. 2012CB316200, and NSFC under grant No. 61171067, 61133016, 61272429, and 61303211.

# REFERENCES

[1] E. Kaplan and C. Hegarty, Understanding GPS: principles and applications. Artech House Publishers, 2006.   
[2] “Goverment information about the global positioning system (gps),” http://www.gps.gov/.   
[3] J. LaMance, J. DeSalas, and J. Jarvinen, “Assisted gps: a lowinfrastructure approach,” GPS World, vol. 13, no. 3, pp. 46–51, 2002.   
[4] B. Parkinson and P. Enge, “Differential gps,” Global Positioning System: Theory and applications., vol. 2, pp. 3–50, 1996.

[5] P. Enge and A. Van Dierendonck, “Wide area augmentation system,” Progress in Astronautics and Aeronautics, vol. 164, pp. 117– 142, 1996.   
[6] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: Wireless indoor localization with little human intervention,” in Proceedings of ACM MobiCom, 2012, pp. 269–280.   
[7] A. Rai, R. Sen, K. K. Chintalapudi, and V. Padmanabhan, “Zee: Zero-effort crowdsourcing for indoor localization,” in Proceedings of ACM MobiCom, 2012, pp. 293–304.   
[8] I. Constandache, R. R. Choudhury, and I. Rhee, “Towards mobile phone localization without war-driving,” in Proceedings of the IEEE INFOCOM, 2010, pp. 1–9.   
[9] O. Woodman and R. Harle, “Pedestrian localisation for indoor environments,” in Proceedings of ACM UbiComp, 2008.   
[10] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: unsupervised indoor localization,” in Proceedings of ACM MobiSys, 2012, pp. 197–210.   
[11] J. Kim, H. Jang, D. Hwang, and C. Park, “A step, stride and heading determination for the pedestrian navigation system,” Journal of Global Positioning Systems, vol. 3, no. 1-2, pp. 273–279, 2004.   
[12] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, “Walkiemarkie: indoor pathway mapping made easy,” in Proceedings of USENIX NSDI, 2013, pp. 85–98.   
[13] C. Karney, “Transverse mercator with an accuracy of a few nanometers,” Journal of Geodesy, vol. 85, no. 8, pp. 475–485, 2011.   
[14] B. K. P. Horn, “Closed-form solution of absolute orientation using unit quaternions,” Journal of the Optical Society of America A, vol. 4, no. 4, pp. 629–642, 1987.   
[15] J. McGlone, E. Mikhail, J. Bethel, R. Mullen, A. S. for Photogrammetry, and R. Sensing, Manual of photogrammetry. American Society for Photogrammetry and Remote Sensing, 2004.   
[16] B. Hofmann-Wellenhof, H. Lichtenegger, and E. Wasle, GNSS– global navigation satellite systems: GPS, GLONASS, Galileo, and more. Springer Verlag Wien, 2008.   
[17] H. Hassanieh, F. Adib, D. Katabi, and P. Indyk, “Faster gps via the sparse fourier transform,” in Proceedings of ACM MobiCom, 2012, pp. 353–364.   
[18] J. Liu, B. Priyantha, T. Hart, H. Ramos, A. A. Loureiro, and Q. Wang, “Energy efficient gps sensing with cloud offloading,” in Proceedings of ACM SenSys, 2012.   
[19] Y.-C. Cheng, Y. Chawathe, A. LaMarca, and J. Krumm, “Accuracy characterization for metropolitan-scale wi-fi localization,” in Proceedings of ACM MobiSys, 2005, pp. 233–245.   
[20] W. G. Griswold, P. Shanahan, S. W. Brown, R. Boyer, M. Ratto, R. B. Shapiro, and T. M. Truong, “ActiveCampus: experiments in community-oriented ubiquitous computing,” Computer, vol. 37, no. 10, pp. 73–81, 2004.   
[21] “Skyhook: The worldwide leader in location positioning, context and intelligence.” http://www.skyhookwireless.com/.   
[22] M. Youssef, M. Yosef, and M. El-Derini, “Gac: Energy-efficient hybrid gps-accelerometer-compass gsm localization,” in Proceedings of the GLOBECOM, 2010, pp. 1–5.   
[23] H. Wang, Z. Wang, G. Shen, F. Li, S. Han, and F. Zhao, “Wheelloc: Enabling continuous location service on mobile phone for outdoor scenarios,” 2013.

![](images/cc8ea0ffa840b66a609c529553f7474946a877c4a8a8b125d6853ab7c3271a7d.jpg)



Chenshu Wu received his B.E. degree in School of Software from Tsinghua University, Beijing, China, in 2010. He is now a Ph.D. student in Department of Computer Science and Technology, Tsinghua University. He is a member of Tsinghua National Lab for Information Science and Technology. His research interests include wireless ad-hoc/sensor networks and pervasive computing. He is a student member of the IEEE and the ACM.

![](images/0864494c0356aad4a74164a6eb43ab8e2f0c571bddffd6a11ee8af7bdcd0ab09.jpg)



Yiyang Zhao received the B.S. degree from Tsinghua University, the Mphil degree from the Institute of Electrical Engineering of CAS, and the PhD degree in computer science from the Hong Kong University of Science and Technology, in 1998, 2001, and 2010, respectively. His research interests include RFID, pervasive computing, distributed systems, embedded systems, and high-speed networking. He is a member of the IEEE and IEEE Computer Society.

![](images/dd0935a36f047fcaab85b60a260b4a49d3fc58fe45f4ec11e1b1e30408e66f19.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an assistant professor in Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/bd39deb5e8a174fe2392652dd1e1ce899908f7b3888108d041018a1d3334e8a4.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now EMC Chair Professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peerto-peer computing, and pervasive computing. He is a senior member of the IEEE.

![](images/24b8c60cbb685cf05597b50c77b8dab05841800dccb16de36aeb5ef28adcc3b3.jpg)



Yu Xu received his B.E. degree in automation and Ph. D degree in control science and engineering from Zhejiang University in 2003 and 2008. He is currently a lecturer in Wenzhou University. His research interestes include robotics, embedded systems and wireless sensor networks.