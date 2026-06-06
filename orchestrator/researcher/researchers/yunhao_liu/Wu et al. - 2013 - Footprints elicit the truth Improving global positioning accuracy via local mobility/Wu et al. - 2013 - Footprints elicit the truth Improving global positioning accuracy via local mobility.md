# Footprints Elicit the Truth: Improving Global Positioning Accuracy via Local Mobility

Chenshu Wu $^{*}$ , Zheng Yang $^{*\dagger}$ , Yiyang Zhao $^{*}$ , Yunhao Liu $^{*\dagger}$

\*TNList and School of Software, Tsinghua University

$^{\dagger}$ Department of Computer Science and Engineering, Hong Kong University of Science & Technology

Email: {wu, yang, zhaoyy, yunhao}@greenorbs.com

Abstract—Global Positioning System (GPS) has enabled a number of geographical applications over many years. Quite a lot of location-based services, however, still suffer from considerable positioning errors of GPS (usually 1m to 20m in practice). In this study, we design and implement a high-accuracy global positioning solution based on GPS and human mobility captured by mobile phones. Our key observation is that smartphone-enabled dead reckoning supports accurate but local coordinates of users' trajectories, while GPS provides global but inconsistent coordinates. Considering them simultaneously, we devise techniques to refine the global positioning results by fitting the global positions to the structure of locally measured ones, so the refined positioning results are more likely to elicit the ground truth. We develop a prototype system, named GloCal, and conduct comprehensive experiments in both crowded urban and spacious suburban areas. The evaluation results show that GloCal can achieve 30% improvement on average error with respect to GPS.

# I. INTRODUCTION

Global positioning technology has enabled a great number of yet-unimagined applications and attracted millions of civil users worldwide. Among all positioning techniques, Global Positioning System (GPS) [1] is widely adopted from industries to personal applications. Along with the popularity of mobile phones with built-in GPS, location information is available in more people's pockets. Burgeoning markets of mobile phone applications are telling a true success story of the integration of GPS and mobile phones.

Although GPS has proven its availability and dependability over many years, many location-based services still suffer from considerable positioning errors. Albeit the officially reported accuracy with high-quality GPS receivers can achieve 3 meters [2], the actual accuracy users attain from commodity smartphones ranges from 1m to up to 20m, which limits the uses of numerous applications while leaves room for various augmented technologies.

Generally, GPS accuracy is affected by a number of unavoidable factors, including satellite positions, atmospheric conditions, and the blockage to the satellite signals caused by mountains and buildings, etc. To overcome or bypass these factors, several augmentation systems, for instance, Assisted GPS (AGPS) [3], Differential GPS (DGPS) [4], and Wide Area Augmentation System (WAAS) [5], have been developed to aid GPS by providing accuracy, integrity, availability, or any other improvement that is not inherently part of GPS itself.

Conventional augmentation systems mostly rely on fixed reference locations, e.g., cell towers, and hence require specific infrastructure provided by either public or private sectors. Consequently, it is difficult for mobile phone users to embrace these augmentations any time at any place. Motivated by the proliferation of mobile phones with rich internal sensors, we propose to enhance the accuracy of global positioning technology by utilizing local position information captured by only mobile phones.

Nowadays, mobile phones possess powerful computation and communication capability, and are equipped with various functional built-in sensors. These sensors enable so-called inertial sensing to characterize human mobility [6], [7]. Inertial sensing, a.k.a. dead reckoning, is a mean of calculating one's current location by using a previously determined location and the estimations of displacement and direction moved. With internal sensors like accelerometer, gyroscope, and compass (or magnetometer), which, respectively, reveal the acceleration, rotational velocity, and direction of user motion, one user's moving trajectory can be tracked by dead reckoning [8].

Phone-based dead reckoning supports accurate but local coordinates of users' trajectories, while GPS provides global but inconsistent coordinates. This study aims at bridging phone-based dead reckoning and GPS to offer high-accuracy global positioning. We present GloCal (naming thanks to its connotation of 'think GLObally and act loCALly'), a global positioning refinement approach via local trajectories tracked by mobile phones. The rationale behind GloCal is that global positions can be refined by fitting their structure to that of local positions, which is more accurate and hence eliciting the ground truth (Fig. 1). To faithfully depict users' trajectory, GloCal first employs a novel scheme for highly accurate dead reckoning on mobile phones. The dead-reckoned local trajectory and the global trajectory, obtained from a series of GPS measurements, are then converted to local and global coordinates in a 2D plane, respectively. On this basis, GloCal refines the originally inaccurate global positions by transforming the local coordinates into the global ones.

To evaluate our design, we implement a prototype on Android OS using Google Nexus S phones and conduct comprehensive experiments in both crowded urban and spacious suburban areas. The evaluation results suggest that GloCal can reduce 30% of global positioning errors of GPS with only negligible extra energy consumption, which demonstrates the feasibility of GloCal in real world deployment.

The rest of this paper is organized as follows. Section II introduces the system design of GloCal. A novel scheme for dead reckoning, as well as the local and global coordinate generation, is presented in Section III. Section IV illustrates how to transform the local coordinate system to the global one. Section V presents the experiments. We discuss related work in Section VI and conclude the work in Section VII.

![](images/283b062b6394418a9a17f0d3fb13dbb87bc1009243001001c39cfeeb6f576c1c.jpg)



Fig. 1. An illustration of user trajectory with both GPS and local measurements, where local footprints elicit the ground truth fantastically well. For the ease of visualization, distances between footprints are larger than the facts.   
![](images/817ced080b8158225c9e9aee9a685d39233ac5314f6030e42f91b1c36f28cb45.jpg)



Fig. 2. System architecture of GloCal

# II. OVERVIEW AND CHALLENGES

As shown in Fig. 2, the working process of GloCal consists of two core phases: coordinate generation and coordinate transformation. Imagine that when a user uses global positioning services for navigation using his mobile phone GloCal records the internal sensor readings, including accelerometer and gyroscope, as well as GPS reports. These consecutive global locations along the user trajectory form a global coordinate system, while the local measurements from inertial sensors will construct a local coordinate system.

GloCal characterizes and exploits user mobility to attain local position information. Analogous to conventional dead reckoning techniques, GloCal uses accelerometer to identify user walking steps and gyroscope to estimate moving directions. Acceleration feature is further investigated to determine the accurate stride length of a specific user. The walking displacement is then derived by multiplying the step counts with the stride length. Provided that the displacement and direction are available, a user trajectory beyond GPS is obtained and a local coordinate system, namely, the relative locations, is accordingly delineated.

Observing that the dead-reckoned local positions preserve the structure of ground truth trajectory better than the global positions obtained from GPS, GloCal therefore intends to improve the global positioning accuracy by fitting the global positions to the local ones. The best fitting is achieved by realizing an optimal transformation that converts the local coordinates exactly into the global ones. All global positions along the user trajectory are concurrently refined with the transformed local positions by doing this.

# III. COORDINATE GENERATION

# A. Local Position Measurements

GloCal uses the accelerometer in combination with gyroscope sensors to infer user walking characteristics, particularly, the displacement and the direction.

Displacement Ranging. As many other works do [7]–[9], we adopt the individual step counts as a metric of walking distance.

The rationality behind step counts is that the accelerations exhibit periodically repetitive patterns, which arises from the nature rhythmic of human walking, as shown in Fig. 3. GloCal thoroughly investigates this observation and designs a novel step counting algorithm based on the finite state machine (FSM). Fig. 3 gives a glance of the performance of the proposed FSM based algorithm. In addition to the accurate results, the algorithm is advantageous in detecting the starting and ending points of each step, which is, to our best knowledge, beyond attainment of most conventional approaches [7]–[9].

To convert the step counts into displacement, GloCal needs the accurate stride length estimation. Previous solutions $[8]$ , $[9]$ mostly assume a fixed stride length of a person according to his weight and height. As is well known, however, stride length can vary widely from user to user and from scenario to scenario. Different from traditional approaches, GloCal uses a learning based method to dynamically estimate the stride lengths. As can be observed from Fig. 4, accelerations of users with different stride lengths exhibit considerable differences on characteristics such as variance, yet evince similarly repetitive patterns. Consequently, using data pre-collected from a group of users with various weights and heights (and thus various stride lengths), GloCal learns the variance-stride relationship model, which is further used to predict the stride length of other users in any scenarios.

Direction Reckoning. Since GloCal solely leverages user mobility to construct a relative coordinate system, the absolute orientation is not necessary involved. Consequently, GloCal is free of using the noisy compass and employs solely the gyroscope, which provides accurate angular velocity of human motion, to infer the changes of direction during every step. The method is fairly intuitive: integrating the angular velocity captured by the gyroscope with respect to time within the interval of a step (detected by the FSM-based algorithm). Due to the high precision and its insensitivity to magnetic fields, the direction changes can be precisely estimated and hence the structure of a user path can be well identified, which is exactly what GloCal desires.

# B. Local Coordinate System

If the displacement and changes of direction of each step are known, we can build a Cartesian coordinate system, namely, the local coordinate system, to portray the trajectory. Given a trajectory $S = \{s_{1}, s_{2}, \cdots, s_{N}\}$ of N steps, each step $s_{j}$ corresponds a displacement $d_{j}$ and a direction change $\gamma_{j}$ . Treating each step as a point and the start of the first step $s_{1}$ as the origin with coordinates $(0, 0)$ , the coordinate of each point can be obtained, where the direction of the vector from $s_{1}$ to $s_{2}$ is defined as that of the x axis and the orthogonal vector is y axis. As shown in Fig. 5, assuming the coordinates of step $s_{j-1}$ (point A) is $(x_{j-1}, y_{j-1})$ , then the coordinates of the next step $s_j$ (point B) can be calculated as

![](images/106ff837a0938a8383d9bd9708c1dc21cd82eeebedcd9d14c47c2773462b3172.jpg)



Fig. 3. Results of FSM based step counting algorithm

![](images/cc25e987de131297c3099f378a3d42e79b053db15b6b9c93de57556c7bdaf870.jpg)



Fig. 4. Walking patterns of users with different strides exhibit distinct characteristics.

![](images/68b8654c726d0fce31e50c86bc0b0643697fbd423c6feaf4c0cb9ffa72a94989.jpg)



Fig. 5. Local coordinate system generation

$$
(x _ {j}, y _ {j}) = (x _ {j - 1} + d _ {j} \cos (\phi + \gamma_ {j}), y _ {j - 1} + d _ {j} \sin (\phi + \gamma_ {j})), \tag {1}
$$

where $\phi = \sum_{p=1}^{j-1} \gamma_{p}$ is the separation angle of vector $\vec{OA}$ and the x axis. Noting that in GloCal the $\gamma_{j}$ is negative if the direction change is clockwise, otherwise positive.

# C. Global Coordinate System

As we assume the global coordinate system and the local one are co-planar, such geographical coordinates must be converted into 2D Cartesian coordinates. Global positioning technology, however, typically reports geographical locations on the spherical surface of the earth in the form of longitude and latitude. Fortunately, GPS reported geographic coordinates can be accurately converted to Universal Transverse Mercator Grid System (UTM) format [10]. UTM is a formal, globally referenced planimetric coordinate system supported by most GPS receivers today. The UTM coordinates are in the form of $(E,N)$ , where $E$ and $N$ denotes the easting and northing values (in meters), respectively. In GloCal, we convert all GPS readings in the form of longitude and latitude to the UTM format based on formulas mentioned in [10] for further processing.

# IV. COORDINATE TRANSFORMATION

At this point, we have obtained both the local and global coordinates. In the following, we present how to improve the global positioning accuracy by harnessing local positions. Our method is based on transforming the local coordinate system into the global one using a set of translation, scaling, and rotation operations based on Horn's method $[11]$ . Horn presented a closed-form solution of absolute orientation problem $[12]$ using unit quaternions in 3D space. In GloCal, assuming the local and global coordinate systems are both in a plane, unit quaternion is not necessary used. Instead, we use complex numbers to denote the coordinates of points, for which the rotation can be represented as a multiplication between numbers, and derive a form of optimal transformation.

# A. Problem Formulation

Assume there are n points in the local coordinate system, denoted as $L = \{w_{j}, j = 1, \ldots, n\}$ , and n corresponding points in the global coordinate system, denoted as $G = \{z_{j}, j = 1, \ldots, n\}$ . Instead of a 2-dimensional vector, each point is represented as a complex number, i.e., $z_{j} = z_{x,j} + iz_{y,j}$ , $w_{j} = w_{x,j} + iw_{y,j}$ . According to [11], the transformation between these two coordinate systems $\mathbb{L}$ and $\mathbb{G}$ can be thought of a rigid-body motion and can thus be decomposed into a translation, a scaling, and a rotation. In other words, the problem is to look for a transformation of the form

$$
\boldsymbol {w} ^ {\mathrm{g}} = s R \left(\boldsymbol {w} ^ {1}\right) + \boldsymbol {t} _ {0} \tag {2}
$$

from the local to the global coordinate system, where $w^{1} \in L$ , $w^{g}$ is the corresponding transformed one in global coordinate system, s is a scale factor, $t_{0}$ is the translational offset, and $R(\boldsymbol{w}^{1})$ denoted the rotated version of $w^{1}$ . Unless the data are perfect, we will not be able to find a transformation such that the equation above is satisfied for each pair of points in L and G. Hence, the optimal solution aims to minimize the sum of squares of the residual errors:

$$
\sum_ {j = 1} ^ {n} \parallel e _ {j} \parallel^ {2} = \sum_ {j = 1} ^ {n} \parallel z _ {j} ^ {\mathrm{g}} - w _ {j} ^ {\mathrm{g}} \parallel^ {2}, \tag {3}
$$

where $z_{j}^{\mathrm{g}} \in \mathbb{G}$ and $e_{j}$ is the residual error between $z_{j}^{\mathrm{g}}$ and $w_{j}^{\mathrm{g}}$ .

As Horn's solution does, we consider the total residual errors first with translation, then with scaling, and finally with respect to rotation.

# B. Optimal Transformation

Translation. First of all, we refer all positions to centroids defined by $\bar{z}^{g} = \frac{1}{n} \sum_{j=1}^{n} z_{j}^{g}$ , $\bar{w}^{1} = \frac{1}{n} \sum_{j=1}^{n} w_{j}^{1}$ , and derive the following new coordinates: $z_{j}^{\bar{g}} = z_{j}^{g} - \bar{z}^{g}$ , $w_{j}^{\bar{1}} = w_{j}^{1} - \bar{w}^{1}$ . The residual error can be rewritten as $e_{j} = z_{j}^{\bar{g}} - w_{j}^{\bar{g}} = z_{j}^{\bar{g}} - s R(w_{j}^{\bar{1}}) - \bar{t}_{0}$ , where $\bar{t}_{0} = t_{0} - \bar{z}^{g} + s R(\bar{w}^{1})$ . The sum of squares of the residuals becomes

$$
\sum_ {j = 1} ^ {n} \left\| \boldsymbol {z} _ {j} ^ {\bar {\mathrm{g}}} - s R \left(\boldsymbol {w} _ {j} ^ {\bar {1}}\right) + \bar {\boldsymbol {t}} _ {0} \right\| ^ {2} = \sum_ {j = 1} ^ {n} \| S \| ^ {2} + 2 \bar {\boldsymbol {t}} _ {0} \cdot \sum_ {j = 1} ^ {n} S + n \| \bar {\boldsymbol {t}} _ {0} \| ^ {2} \tag {4}
$$

where $S = z_{j}^{\bar{g}} - sR(\boldsymbol{w}_{j}^{\bar{l}})$ and $\sum_{j=1}^{n} S$ equals zero, since all positions are referred to their centroids. Thus we are left with the first and last term of this expression. The first is independent from $\bar{t}_{0}$ while the last cannot be negative. The sum will be evidently minimized when $\bar{t}_{0} = 0$ , or $t_{0} = \bar{z}^{g} - sR(\bar{w}^{1})$ . That is, the optimal translation is just the difference of the global centroid and the scaled and rotated local centroid. Since both centroids are known if given the two sets of positions, the optimal translational offset, i.e., $t_{0}$ , can be derived once the scale and rotation factors are found.

![](images/152f69d845bfb38a830f59cd86724a859a44e40cfbb5513e3f332cc7222248a4.jpg)



(a) Urban areas

![](images/c7e4aab5747264b3ef48b15c399a29365d928a7b2c7575afc58b45ef08cf8de8.jpg)



(b) Suburban areas   
Fig. 6. Experiment areas in Wuxi City

![](images/0c342a1b3b55aca89770dbcd0f6318c0dcf3adf16b33c16ea80435e43400b94c.jpg)



Fig. 7. Step counting accuracy on different users

![](images/a93576d3e93a8ebd1b690b3c0847aa72fdf7fa33c1686d3147b9c4ba8d7644f9.jpg)



Fig. 8. Stride estimation accuracy with different size of training data

Scaling. At this point, assuming that the optimal translation is given as $t_{0} = \bar{z}^{\mathrm{g}} - sR(\bar{w}^{\mathrm{l}})$ , we have $\bar{t}_{0} = 0$ and hence the sum of squares of the residual errors can be written as $\sum_{j=1}^{n} \| z_{j}^{\bar{g}} - sR(w_{j}^{\bar{1}}) \|^{2}$ . Expanding the above term to complete the square form in s and noting that $\| R(w_{j}^{\bar{1}}) \|^{2} = \| w_{j}^{\bar{1}} \|^{2}$ , we have $s = \frac{\sum_{j=1}^{n} z_{j}^{\bar{g}} \cdot R(w_{j}^{\bar{1}})}{\sum_{j=1}^{n} \| w_{j}^{\bar{1}} \|^{2}}$ minimize the above residual errors with respect to scale s.

Rotation. At present, the only remaining task is to find the rotation in the plane of global coordinate system. By doing this, final complete solution of the position transformation problem will be achieved.

The optimal rotation should minimize the sum of squares of distances between corresponding points of local and global coordinates [11], say, minimize $\sum_{j=1}^{n}\parallel z_{j}^{\bar{g}}-R(\boldsymbol{w}_{j}^{\bar{1}})\parallel^{2}$ . As the local and global coordinate systems are coplanar, there is an angle between corresponding positions $z_{j}^{\bar{g}}$ and $w_{j}^{\bar{1}}$ , denoted as $\alpha_{j}$ . In other words, $z_{j}^{\bar{g}}\cdot w_{j}^{\bar{1}}=\parallel z_{j}^{\bar{g}}\parallel\parallel w_{j}^{\bar{1}}\parallel\cos\alpha_{j}$ . Let $\theta$ denote the angle the global coordinates have rotated. The above term can be expanded as follows since the angle $\alpha_{j}$ is reduced by $\theta$ .

$$
\sum_ {j = 1} ^ {n} \left\| z _ {j} ^ {\bar {\mathrm{g}}} \right\| ^ {2} + \sum_ {j = 1} ^ {n} \left\| w _ {j} ^ {\bar {\mathrm{I}}} \right\| ^ {2} - 2 \sum_ {j = 1} ^ {n} \left\| z _ {j} ^ {\bar {\mathrm{g}}} \right\| \left\| w _ {j} ^ {\bar {\mathrm{I}}} \right\| \cos (\alpha_ {j} - \theta). \tag {5}
$$

To minimize Eqn. 5, we need to maximize the last term, or $A \cos \theta + B \sin \theta$ , where $A = \sum_{j=1}^{n} \| z_j^{\bar{\mathrm{g}}} \| \| w_j^{\bar{\mathrm{l}}} \| \cos \alpha_j$ , $B = \sum_{j=1}^{n} \| z_j^{\bar{\mathrm{g}}} \| \| w_j^{\bar{\mathrm{l}}} \| \sin \alpha_j$ . This term achieves extremum when $A \sin \theta = B \cos \theta$ , that is, $\theta = \arcsin \pm \sqrt{\frac{B^2}{A^2 + B^2}}$ , one maximizing, and one minimizing the residual errors.

Accomplishing the coordinate transformation, global positions are aligned to their corresponding transformed local ones, which delineate the structure of true trajectory better. In other words, a global position $\bar{z}_{j}^{g}$ is replaced with $\bar{w}_{j}^{g}$ .

# V. EXPERIMENTS

# A. Experiment Methodology

We implemented GloCal on Android OS using Google Nexus S phones, which are equipped with accelerometers, gyroscopes, and compasses, and as well support GPS functions. Our experimental environments are twofold: a built-up urban region around an academic building (Fig. 6a) and a spacious suburban area (Fig. 6b). Trajectories are collected from users automatically when they are walking naturally and using their mobile phones for navigation. All raw sensor data are first sanitized for further uses, while accelerometer readings are additionally compensated for gravity.

To obtain the ground truth geographical positions of the paths user traveled for evaluation, users have to walk along our predefined paths depicted on a map. The real position information can then be acquired by carefully putting the routes into handy digital map services, for instance, Google Maps, as shown in Fig. 6a and Fig. 6b.

# B. Performance Evaluation

Local Positioning Performance. We first test the FSM based step counting algorithm on 3 users by collecting 8 traces from their natural walking with various lengths ranging from 10 steps to 300 steps, which are counted by the users themselves and used as ground truth. As shown in Fig. 7, the counting errors are bounded in 5 steps for all but one cases.

To evaluate the efficiency of stride length estimation, we conduct testing on totally 20 users with various heights and weights by having them step along two pre-defined paths. One user's actual stride lengths (in different traces) are measured as the quotients of the path length to the number of steps he took within the path. The integrated results depicted in Fig. 8 show fairly good performance of the learning method.

Positioning Accuracy. Now we turn to the accuracy improvement of GloCal on GPS. We first take a glance at the accuracy of raw GPS with commodity mobile phones. With our experimental phones, the average location error from 14 measurements over one week in urban areas is 5m\~8m. Fusing all results from multiple traces, we plot the respective accuracy of GloCal in urban and suburban areas in Fig. 9a and Fig. 9b, and incorporate them to derive the overall accuracy in Fig. 9c. All results show that an impressive improvement of 20%\~30% over raw GPS is achieved while the average error is limited under 4m. This accuracy also outperforms the CompAcc [8], which provides an average accuracy of 11m in urban regions. We believe GloCal sets up an unconventional perspective provides a practical way to improve GPS accuracy using mobile phone only, with negligible extra energy consumption compared to the GPS only mode.

# VI. RELATED WORK

# A. Global Positioning Technology

Global positioning technologies, like GPS, GLONASS, and Galileo, have revolutionized a range of location-awareness services $[13]$ . However, many applications still suffer from global positioning errors due to various factors $[1]$ . For the dominant GPS, several augmentation systems, e.g., AGPS $[3]$ ,

![](images/c3a31ffb24eefd8c7b2cdf15c0a69bd2c5e72f5ff227ad56f76b11f8fe38398b.jpg)



(a) Overall accuracy in urban areas

![](images/3e28133de65b1bdc122799063ebb1c8a175bdeef249f6c748c9831df2cc8e5e0.jpg)



(b) Overall accuracy in suburban areas

![](images/ba4591de3a091f2fcff1526c94133eea59920f3325313af4b9aa4da6cb9ec00c.jpg)



(c) Overall accuracy of GloCal   
Fig. 9. Overall positioning accuracy

DGPS [4], and the most recent WAAS [5], etc, are developed to provide accuracy, availability, or any other improvement. Other augmentation systems include IGS, CORS, LAAS, etc [2]. Either relying on fixed reference stations with exactly known locations, or requiring constant network connections, all these augmentation systems need to be run by special operators and are available only in limited areas.

On the other hand, considering problems with GPS beyond accuracy, including poor indoor supports, large battery consumption, and long acquisition time, innovated algorithms $[14]$ , $[15]$ and supplementary solutions to GPS such as GSM/WiFi based positioning $[16]$ , $[17]$ are also proposed.

# B. Mobile Phone Localization

Adhere to the thinking of marine or air navigation, smartphone-enabled dead reckoning is well-studied for both indoor and outdoor localization. [18] combines a foot-mounted inertial unit and a detailed building model to provide absolute positioning. CompAcc [8] both provide localization in outdoor environments, depending on the GPS infrequently for recalibration. Unloc [9] and Zee [7] enable zero-calibration indoor localization by leveraging multimodal sensors. Considering human mobility, LiFS [6] releases the site survey process of traditional indoor localization. Different from conventional work using inertial sensing for absolute positioning and thus requiring additional reference information to recalibrate the dead-reckoned user positions, such as GPS [8], indoor landmarks [9], and digital maps imposed constraints [7], GloCal aims at improving global positioning accuracy by using inertial sensing as a second, local localization. Desiring solely the relative structure of user trajectories, GloCal is free of using any reference information or extra infrastructure.

# VII. CONCLUSION

In this paper, we propose an innovative approach to improve global positioning accuracy using user trajectories measured by commodity mobile phones, without any dependence on either fixed infrastructure or additional reference information. We design a novel smartphone-enabled dead reckoning technique to accurately delineate users' locomotion. On this basis, the global positioning accuracy is refined by fitting the less accurate global positions to the structure of the more precise local trajectories. The preliminary experiment results suggest that GloCal can achieve 30% improvement on GPS average accuracy, demonstrating its promise in real-world feasibility.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program under grant 61190110, NSFC under grant 61171067, 61133016, 61272429, and 61272466, National High-Tech R&D Program of China (863) under grant No. 2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200.

# REFERENCES

[1] E. Kaplan and C. Hegarty, Understanding GPS: principles and applications. Artech House Publishers, 2006.   
[2] “Government information about the global positioning system (gps).” [Online]. Available: http://www.gps.gov/   
[3] J. LaMance, J. DeSalas, and J. Jarvinen, “Assisted gps: a low-infrastructure approach,” GPS World, vol. 13, no. 3, pp. 46–51, 2002.   
[4] B. Parkinson and P. Enge, “Differential gps,” Global Positioning System: Theory and applications., vol. 2, pp. 3–50, 1996.   
[5] P. Enge and A. Van Dierendonck, “Wide area augmentation system,” Progress in Astronautics and Aeronautics, vol. 164, pp. 117–142, 1996.   
[6] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: Wireless indoor localization with little human intervention,” in Proceedings of the ACM MobiCom, 2012, pp. 269–280.   
[7] A. Rai, R. Sen, K. K. Chintalapudi, and V. Padmanabhan, “Zee: Zero-effort crowdsourcing for indoor localization,” in Proceedings of the ACM MobiCom, 2012, pp. 293–304.   
[8] I. Constandache, R. R. Choudhury, and I. Rhee, “Towards mobile phone localization without war-driving,” in Proceedings of the IEEE INFOCOM, 2010, pp. 1–9.   
[9] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: unsupervised indoor localization,” in Proceedings of the ACM MobiSys, 2012, pp. 197–210.   
[10] C. Karney, “Transverse mercator with an accuracy of a few nanometers,” Journal of Geodesy, vol. 85, no. 8, pp. 475–485, August 2011.   
[11] B. K. P. Horn, “Closed-form solution of absolute orientation using unit quaternions,” Journal of the Optical Society of America A, vol. 4, no. 4, pp. 629–642, 1987.   
[12] J. McGlone, E. Mikhail, J. Bethel, R. Mullen, A. S. for Photogrammetry, and R. Sensing, Manual of photogrammetry. American Society for Photogrammetry and Remote Sensing, 2004.   
[13] B. Hofmann-Wellenhof, H. Lichtenegger, and E. Wasle, GNSS–global navigation satellite systems: GPS, GLONASS, Galileo, and more. Springer Verlag Wien, 2008.   
[14] H. Hassanieh, F. Adib, D. Katabi, and P. Indyk, “Faster gps via the sparse fourier transform,” in Proceedings of the ACM MobiCom, 2012, pp. 353–364.   
[15] J. Liu, B. Priyantha, T. Hart, H. Ramos, A. A. Loureiro, and Q. Wang, "Energy efficient gps sensing with cloud offloading," in Proceedings of the ACM SenSys, 2012.   
[16] Y.-C. Cheng, Y. Chawathe, A. LaMarca, and J. Krumm, “Accuracy characterization for metropolitan-scale wi-fi localization,” in Proceedings of the ACM MobiSys, 2005, pp. 233–245.   
[17] W. G. Griswold, P. Shanahan, S. W. Brown, R. Boyer, M. Ratto, R. B. Shapiro, and T. M. Truong, “ActiveCampus: experiments in community-oriented ubiquitous computing,” Computer, vol. 37, no. 10, pp. 73–81, 2004.   
[18] O. Woodman and R. Harle, “Pedestrian localisation for indoor environments,” in Proceedings of the ACM UbiComp, 2008, pp. 114–123.