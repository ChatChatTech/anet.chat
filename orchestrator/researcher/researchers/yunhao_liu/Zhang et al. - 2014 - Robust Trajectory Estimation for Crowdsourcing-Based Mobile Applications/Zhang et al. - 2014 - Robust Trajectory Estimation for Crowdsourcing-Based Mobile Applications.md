# Robust Trajectory Estimation for Crowdsourcing-Based Mobile Applications

Xinglin Zhang, Student Member, IEEE, Zheng Yang, Member, IEEE, Chenshu Wu, Student Member, IEEE, Wei Sun, Student Member, IEEE, Yunhao Liu, Senior Member, IEEE, and Kai Xing, Member, IEEE

Abstract—Crowdsourcing-based mobile applications are becoming more and more prevalent in recent years, as smartphones equipped with various built-in sensors are proliferating rapidly. The large quantity of crowdsourced sensing data stimulates researchers to accomplish some tasks that used to be costly or impossible, yet the quality of the crowdsourced data, which is of great importance, has not received sufficient attention. In reality, the low-quality crowdsourced data are prone to containing outliers that may severely impair the crowdsourcing applications. Thus in this work, we conduct pioneer investigation considering crowdsourced data quality. Specifically, we focus on estimating user motion trajectory information, which plays an essential role in multiple crowdsourcing applications, such as indoor localization, context recognition, indoor navigation, etc. We resort to the family of robust statistics and design a robust trajectory estimation scheme, name TrMCD, which is capable of alleviating the negative influence of abnormal crowdsourced user trajectories, differentiating normal users from abnormal users, and overcoming the challenge brought by spatial unbalance of crowdsourced trajectories. Two real field experiments are conducted and the results show that TrMCD is robust and effective in estimating user motion trajectories and mapping fingerprints to physical locations.

Index Terms—Crowdsourcing, robust estimation, mobile applications, motion trajectory

# 1 INTRODUCTION

HE smartphone market is growing rapidly in recent years. According to the International Data Corporation (IDC), 712.6 million smartphones were shipped in 2012, which was 44.1 percent more than in 2011 [1]. On the other hand, smartphones today are equipped with various functional sensors, which act as important information interfaces between users and environments. These advances have stimulated the development of crowdsourced sensing applications based on smartphones, such as indoor localization, context recognition, indoor navigation, etc.

Among multiple crowdsourced sensing applications, fingerprint-based indoor localization by crowdsourcing is a typical example and thus is chosen for the sake of illustration. Traditional fingerprint-based methods consist of two phases: calibration phase and operation phase. In calibration phase, fingerprint measurements, mostly received signal strength (RSS) measurements, are recorded at known locations of interest, forming a fingerprint database.

X. Zhang and W. Sun were research associates at School of Software, Tsinghua University during this study, and now PhD students at CSE, Hong Hong University of Science and Technology, Kowloon, Hong Kong. E-mail: {zhxlinse, sunw1989}@gmail.com.   
Z. Yang, C. Wu, and Y. Liu are with the School of Software and Tsinghua National Lab for Information Science and Technology (TNLIST), Tsinghua University, China. E-mail: {hmilyyz, wucs32, yunhaoliu}@gmail.com.   
K. Xing is with the School of Computer Science and Technology, and the Suzhou Institute for Advanced Study, University of Science and Technology of China, China. E-mail: kxing@ustc.edu.cn.

Manuscript received 7 Apr. 2013; revised 27 July 2013; accepted 18 Sept. 2013. Date of publication 30 Sept. 2013; date of current version 13 June 2014. Recommended for acceptance by D. Xuan. For information on obtaining reprints of this article, please send e-mail to: reprints@ieee.org, and reference the Digital Object Identifier below. Digital Object Identifier no. 10.1109/TPDS.2013.250

Then in operation phase, when a user requests her location, the system will match her fingerprint against the fingerprint database to estimate a location. Calibration phase is known to be prohibitively expensive, but it is inevitable for all fingerprint-based localization approaches since the fingerprint database has to be constructed by mapping fingerprints to corresponding physical locations. To accommodate the bottleneck of calibration, researchers investigated the relationship between user motion trajectories and fingerprints, coming up with a new dimension to link the original discrete fingerprint points. The common ground of these approaches lies in that the costly on-site calibration can be crowdsourced implicitly through collecting user trajectories without putting any burden on user ends. Fingerprints together with other trajectory information are sufficed to perform indoor localization. Specifically, Unloc [2] leverages the traces of users to recognize the special locations, termed as landmarks, in a floorplan, and thus localize users’ locations. From a different perspective of employing the floor plan, Zee [3] records user’s trajectories and fits them into the floor plan, thus removing the impossible placements of those trajectories. More trajectories add more constraints and reduce the possible positions. Eventually the position of the trajectory will converge.

The key insight of these crowdsourcing-based localization techniques is to estimate user motion trajectories and then map crowdsourced fingerprints to physical locations, such that a fingerprint database can be constructed. However, none of the proposed methods considered whether the estimated trajectories are robust and trustful enough to build an accurate fingerprint database in the first place, which we believe is of critical importance in the family of crowdsourcing schemes. In reality, the trajectories obtained from crowdsourcing are apt to contain outliers due to various reasons, such as abnormal behaviors of a user or equipment malfunctioning. The erroneous trajectory estimation will mismatch against the floor plan and the consequent localization procedures will thus be far from satisfaction.

![](images/44f64bd01049000cbdf8250a8778ef1e33429c873cbfa60b1a255a1bf932c180.jpg)



Fig. 1. Motivated scenery. A, B, C and D represent four reference location points. Curves labeled with different shapes represent motion trajectories of different users.

In order to get a clearer picture of the hurdles brought by outliers in estimating user motion trajectories accurately. we describe a motivated scenery as shown in Fig. 1. There are four reference points (where the fingerprints are supposed to be recorded), A, B, C, and D. Assume that in daily life, many people walk through A, B, and C, and few people step from C towards D. We are interested in obtaining reliable distance estimates among these reference points, such that the fingerprints in trajectories can be mapped to these reference points correctly.

One significant problem is that different mobile phone users may collect different distance measurements due to various reasons. For example, users have different strides (triangle-curve and circle-curve between A and B shown in Fig. 1), users behave in different walking manners, or simply users choose a curving trace between two reference points (square-curve and triangle-curve between A and C shown in Fig. 1), etc. These unavoidable factors put up a barrier for us to employ those freely collected data. It is desirable to estimate distances robustly such that the ground truth is correctly reflected.

Another problem is that, in this scenery, the collected trajectories are spatially unbalanced: some areas (e.g., A !C !B) are trajectory-dense, while others (e.g., C !D) are trajectory-sparse. This phenomenon makes estimation in trajectory-sparse area very tough by only applying statistical methods. For example, if there are only 3 users walking through C to D, and 2 of them report abnormal sensor readings, the statistical methods may fail as the majority of the data is abnormal. In this situation, if the prior confidence on the 3 users can be revealed, the estimation will be on the correct track. Hence it is important to obtain the estimates that are not only met with reliable inter-point distances, but also able to classify users as trustworthy or not. If this can be accomplished, the information obtained can be used to facilitate robust distance estimations in the less walked regions.

Taking all difficulties into account and inspired by the effective works on handling outliers in wireless sensor networks (WSNs) [4], [5], we propose a robust trajectory estimation scheme (TrMCD) based on the idea of robust statistics to make the geometric relation estimation efficient and outlier-tolerant. The key idea behind TrMCD is that crowdsourced data provides redundancy for robustly estimating trajectories. Different from the measurements between sensor nodes in WSNs, the trajectory measurements are more challenging to model and estimate due to following reasons:

We have to first model trajectories containing multiple measurements, including fingerprint and acceleration readings. Then we need to merge numerous trajectories to generate reference fingerprint points;   
Crowdsourced trajectories are spatially unbalanced in different areas. In the trajectory-sparse area, all statistical methods may fail due to the insignificant statistical properties.

TrMCD first selects an area, e.g., a corridor, where most users step through and record user trajectories automatically, and models trajectories accordingly. Then by employing a multivariate robust estimator, the distances among a subset of collected trajectories are robustly estimated and at the same time each user is labeled as normal or abnormal. This high-level user-based robustness facilitates the estimation computation of less walked areas, such as personal offices.

To the best of our knowledge, no prior methods have been developed to deal with measurement errors in crowdsouring from the robust statistical point of view. And we take one step further by revealing the novel userbased point of view, besides a tailored robust statistical method. We envision that the robust trajectory estimation can be applied in crowdsourcing-based sensing applications that need user trajectory information, such as indoor localization, context recognition, indoor navigation, etc. Thus we emphasize that we are not developing a specific localization scheme, but investigating robust methods in the context of crowdsourcing-based sensing applications that needs user trajectory data. For the ease of discussion, we assume that the fingerprint of a location is the received signal strength (RSS) value at that location, and a user’s trajectory consists of a sequence of accelerometer readings and RSS values.

To validate the proposed design, we conduct two real field experiments in a middle-size academic building. Experimental results demonstrate the robustness and effectiveness of the proposed TrMCD. The average mapping error of TrMCD is 0.84 meters, superior to that of 2.13 meters obtained by traditional Least Squares (LS) estimator.

# 1.1 Contribution

In summary, the main contributions of our work include:

Outliers in crowdsourced data are explicitly contended with and thus the trajectory information estimation among all interested locations become robust and accurate, which is of essential importance in multiple crowdsourcing-based mobile applications;

A natural and useful concept of individual robustness has been realized so that normal and abnormal users can be distinguished. Individual robustness is a novel perspective in using robust statistical methods for crowdsourcing-based applications;

The widely existed problem of trajectory density unbalance in crowdsourcing is accommodated in our proposed method. Accurate trajectory estimation in trajectory-sparse area can not be accomplished by employing statistical methods even without outliers. Our method overcomes the difficulty based on the trajectory information in trajectory-dense area.

# 1.2 Paper Organization

The rest of the paper is organized as follows. The related works are discussed in Section 2. We introduce the preliminaries of robust statistics and the key component in our proposed method, the minimum covariance determinant (MCD), in Section 3. The design and computation details of TrMCD are given in Section 4. In Section 5, experiments are illustrated and discussed. Finally, Section 6 concludes our work.

# 2 RELATED WORK

The research of crowdsourced user trajectories is in its infancy, which is following the fast pace of mobile crowdsourcing applications. The most related works we have found come from two aspects, crowdsourcing-based mobile applications, in which the quality of user trajectories may be of central role, and error management in WSN localization, which demonstrates the great potential of quality control of crowdsourced data.

# 2.1 Crowdsourcing-Based Mobile Applications

Crowdsoucing-based indoor localization is closely related to fingerprint-based indoor localization schemes, which are widely used and studied due to the satisfactory accuracy. Among the various techniques, WiFi signals are commonly used as fingerprints, such as in RADAR [6], Horus [7], LANDMARC [8] and SurroundSense [9]. To reduce the cost of fingerprint calibration, researchers turn to crowdsourcing-based localization schemes. UnLoc [2] extracts identifiable indoor signatures as landmarks of a building, and then apply dead-reckoning schemes to track users between landmarks. Sensor readings from different users are gathered to be analyzed in order to discover new landmarks that can further help localization. Zee [3] collects the user’s trajectory information and matches it with the map, which constrains the possible positions of the trajectory by physical walls. Zee heavily relies on the trajectory quality in order to get accurate estimations and build up the fingerprint database. LiFS [10] also makes use of pedestrian trajectories to sample fingerprint values. And it then constructs the geometrical relationship among those sampled points in the fingerprint space. In order to get the hfingerprint, positioni pairs, the floor plan is used and the mapping is conducted between the stress-free floor plan and the fingerprint space obtained by Multidimensional scaling.

Crowdsourced motion trajectories can be used to recognize contexts. CrowdInside [11] leverages user trajectories to first detect the overall floorplan shape of the building, and further recognize the high level context such as room and corridor shapes. Walkie-Markie [12], on the other hand, focuses on recognizing and reconstructing pathway in a building, by exploiting the WiFi infrastructure-defined landmarks (WiFi-Marks) to fuse crowdsourced user trajectories. Frequent pattern mining techniques [28], [29] may be further incorporated in these systems to discover richer contexts, such as popular routines of users.

User motion trajectories are also related to indoor navigation. FootPath [13] uses the accelerometer and the compass in smartphones to localize a user on her route, and provide further turn-by-turn instructions guiding to her destination. Escort [14] presents a navigation service for finding a specific person. Escort learns the walking trails or trajectories of different individuals as well as the encounter events in space-time. A route then can be computed between any pair of persons.

Most of these works are concentrating on crowdsouring ample mobile phone data and thus saving the expensive cost of explicit calibration or other infrastructure construction. However, these proposed methods assume implicitly that users and equipments that provide the data are behaving regularly, which makes them vulnerable to the anomalous collected data. In the real world, data collected from crowdsouring is prone to containing certain amount of outliers due to various factors that are hard to explicitly enumerate and handle. In this study, we are going to contend with outliers in crowdsourcing and develop robust trajectory estimations that can be widely used in crowdsourcing applications.

# 2.2 Error Management

Range-based localization algorithms are well studied in WSNs society. These methods need pairwise distance measurements among nodes, which are used to derive localization. Error in distance measurements is the major issue for range-based localization schemes, thus a large body of research works are devoted to acquiring high quality measurement data and mitigate the error influence. For WSN localization, Liu et al. [15] recorded error information in each node and selected nodes that participate in localization based on their relative contribution to the localization accuracy. ‘‘Robust quadrilaterals’’ were proposed in [16] to prevent large localization errors caused by flip ambiguities. Yang and Liu [17] introduced the concept of Quality of Trilateration, which considers both geometric relationship and errors for all nodes. In [18], Jian et al. investigated outlier detections for network localization based on graph embeddability and rigidity theory.

Another line of researches resort to the family of robust statistics to carry out robust estimation in presence of outliers. As the virtue of robust statistics is to summarize the majority of the data while mitigating the negative effects of outliers, it is naturally attractable and effective in the field of error management in localization. Li et al. [4] introduced Least Median of Squares (LMS) to estimate inter-node distances. LMS has a high breakdown point of

![](images/08b079a4e650d040063e45a7987f4013763d772c3a5527e226ec5f0d90a77fa9.jpg)



Fig. 2. Influence of outliers. Crosses are sample points, and the triangle and circle are sample mean (break down point value of 0) and sample median (break down point of 0.5). The Break of lines means an arbitrarily large gap between the values on different sides.

50 percent and thus it can tolerate up to half of the data being outliers theoretically. However, LMS is not statistically efficient on the other hand. To accommodate this deficit, the authors design an approach of combining LMS and LS estimators. Kung et al. [5] modified the shape of the residual function in the traditional LS method, resulting in snap-inducing shaped residuals (SISR) method. SISR is able to differentiate good and bad nodes automatically, which makes the estimation robust to outliers. Tuning the parameters appropriately, SISR can achieve a breakdown value around 30 percent and maintain satisfiable efficiency.

Our proposed method also relies on robust statistics. However, it differs from the above methods in that the measurement dimension of our method is higher. The previous estimators are estimating a single measurement value between sensor nodes, but our target is to estimate multivariate measurements simultaneously. Also, in our application, there exists an unavoidable and important problem, the spatially unbalanced density of samples. What’s more, we propose to form a higher level concept of robustness based on users, which is natural and informative in the case of crowdsourcing. To the best of our knowledge, our method is the first work on applying robust statistics to refine sensor readings in mobile crowdsourcing application.

# 3 PRELIMINARIES

As our developed method depends largely on the knowledge of robust statistics, we first briefly introduce the most relevant preliminaries.

Suppose that we have a model $X _ { i } = \theta + \epsilon _ { i } ,$ where $\epsilon _ { i }$ conforms to the standard normal distribution, i.e., $\epsilon _ { i } \sim \mathcal { N } ( 0 , 1 )$ . Given i.i.d. samples $X _ { i } , i = 1 , \dotsc , n ,$ we would like to estimate parameter -. By using the well-known LS estimator, we will have the estimate $\textstyle { \hat { \theta } } = 1 / n \sum _ { i = 1 } ^ { n } X _ { i }$ . However, when we have an observation $X _ { j }$ that is far away from the other sample points, $\hat { \theta }$ would be unavoidably pulled towards $X _ { j }$ and thus the estimate is destroyed by this outlier observation, as is shown in Fig. 2.

Robust statistics is a class of methods that can handle the above problem, as it is designed well to describe the majority of the data while dealing with outlier points. An important measurement of robustness is the breakdown point (BP), which is the smallest fraction of contamination that can pull the value of the estimator far away from the ground truth. Mathematically, the BP of an estimator at sample X is defined as

$$
\varepsilon_ {n} ^ {*} (X) = \min _ {m} \left\{\frac {m}{n}; \sup _ {\tilde {X}} \left\| \hat {\theta} (\tilde {X}) - \hat {\theta} (X) \right\| = \infty \right\} \tag {1}
$$

where $\tilde { X }$ is any possible contaminated dataset that replaces m points of the original n-point dataset by arbitrary values. The range of the BP value is 0 - 50 percent. In Fig. 2, we can see that the mean estimator have a BP of 0, as only one outlier is able to totally destroy the estimate; while the median estimator, which belongs to the robust estimator family, obtains the best BP value of 50 percent.

To estimate the user motion trajectory, we draw the estimators from multivariate robust statistics. Several commonly used multivariate estimators for location include M-estimator [19], ellipsoidal multivariate trimming (MVT) [20], [21], the minimum volume estimator (MVE) [22], and MCD estimator [22]. In this paper, we are going to focus on the MCD estimator for the following considerations. Firstly, compared to the M-estimator and MVT, MCD has a higher BP value. which means that MCD is able to tolerate more contaminations. Secondly, MCD has a faster convergence rate than MVE and it maintains high finite sample efficiency. Last but not the least, MCD can be welltailored for our application, as can be seen in Section 4.

Given a sample $X = \{ x _ { 1 } , x _ { 2 } , . . . , x _ { n } \}$ , where $x _ { i } \in R ^ { d } , i =$ $1 , 2 , \ldots , n ,$ and $\dot { R } ^ { d }$ represents d-dimensional space, the MCD estimator of its location T ðXÞ is defined as the mean of the h observations of X whose covariance matrix obtains the smallest determinant. The BP of the MCD estimator is $\varepsilon _ { n } ^ { * } ( X ) \approx { ( n - h ) / n } ,$ , and when $\begin{array} { r } { h = \lfloor \frac { n + d + 1 } { 2 } \rfloor } \end{array}$ , the BP approximates 50 percent, the best performance one can expect. An example of MCD is shown in Fig. 3.

MCD can be computed by the efficient FAST-MCD algorithm [23], [24], which gives a one-step weighted estimate:

$$
T = \frac {\left(\sum_ {i = 1} ^ {n} w _ {i} x _ {i}\right)}{\left(\sum_ {i = 1} ^ {n} w _ {i}\right)}, \tag {2}
$$

$$
S = \frac {\left(\sum_ {i = 1} ^ {n} w _ {i} (x _ {i} - T) (x _ {i} - T) ^ {\prime}\right)}{\left(\sum_ {i = 1} ^ {n} w _ {i} - 1\right)} \tag {3}
$$

where

$$
w _ {i} = \left\{ \begin{array}{l l} 1 & \text { if } d _ {T _ {\text { init }}, S _ {\text { init }}} (i) \leq \sqrt {\chi_ {d , . 9 7 5} ^ {2}}, \\ 0 & \text { otherwise } \end{array} \right. \tag {4}
$$

$T _ { i n i t } / T$ and $S _ { i n i t } / S$ are the initial/final mean and covariance estimates of MCD, respectively. $d _ { T _ { i n i t } , S _ { i n i t } } ( i )$ represents the distance of sample point i to the mean given the initial estimates. If the value of $d _ { T _ { i n i t } , S _ { i n i t } } ( i )$ exceeds the statistical threshold $\sqrt { \chi _ { d , . 9 7 5 } ^ { 2 } }$ (i.e., chi-squared test with significance level of .025), sample i is considered an outlier, and thus is given a weight $w _ { i } = 0$ . For those who are interested in more detail of MCD, we refer them to [22], [23], [24].

![](images/77a79b9e6bf59b3338f976a7c28a706a891acf3ebf3b3dbc44cedb7a65662a74.jpg)



Fig. 3. Example showing the MCD ellipsoid. The triangles encased by the MCD ellipsoid are normal points, while the squares outside the ellipsoid are outliers.

The weights actually provide very helpful information about observations. Specifically, $w _ { i } = 1$ means that the i-th observation is normal and should be incorporated in calculating the location estimate, while $w _ { i } = 0$ wipes out the corresponding negative observation. In Section 4 we will subtly make use of these weights of users to facilitate trajectory estimation in areas such as rooms where trajectories are of low density, which we deem to enhance the performance effectively.

# 4 ROBUST TRAJECTORY ESTIMATION

For the purpose of describing our proposed method TrMCD clearly, we define the following concepts. A trajectory is a user record that includes walking step counts and sample RSS readings as she walks from a starting spot to an ending spot. Whenever a user walks along an accessible area, a physical route is formed. So in the area like a corridor, there may be many trajectories corresponding to the same route. TrMCD aims to reveal the distances among RSS sample locations along a route by mining the trajectory records.

The general framework of TrMCD is shown in Fig. 4. Roughly speaking, there are three phases: data preparation, trajectory estimation, and mapping. In data preparation phase, user trajectory information, including RSS fingerprint values and accelerometer readings, are collected. Fingerprints are merged to generate a reference set. It’s this representative fingerprint set that will be used in the following trajectory estimation phase, which is the focus of this work. In the trajectory estimation phase, we first propose to model the basic point-to-point distances for all fingerprints, constructing geometric constraints among these discrete points. Then user trajectory model is designed to reveal the data characteristics of crowdsourcing. To estimate the trajectories robustly, we progressively deal with simple trajectories and compound trajectories. The resultant trajectory estimation then can be mapped to physical indoor locations, which completes the workflow of TrMCD.

The trajectory estimation is the kernel of TrMCD. Thus in the rest of this section, we will elaborate on the designs of point-to-point distance model, trajectory model, and trajectory estimation, while data preparation and mapping will be illustrated in Section 5, where experiments are conducted.

![](images/29e5689c6c89c954a14249adb85e48de7ebde2298a0fc2f987b7ddb0bb1646a3.jpg)



Fig. 4. TrMCD framework.

# 4.1 Trajectory Modeling

# 4.1.1 Modeling Point-to-Point Distance

In order to measure the distance of two sample locations, a commonly used method is to use the step counts of a user between those two points, as the records of an accelerometer in the mobile phone can be transformed to step counts. However, there are difficulties in using step counts to reflect distance. Different individuals have different strides, and a specific individual may have collected different data due to various reasons, e.g., the position where she puts the mobile phone in, whether the path she takes is straight, and whether she is cheating the mobile phone by abnormal movements. What’s more, if a user walks through multiple sample locations, the ranging measurement between any two consecutive locations also exhibit randomness, which is not sufficient to reflect the ground truth of the geometry of those sample locations.

Normally, the distribution of the heights of people in a region conforms to a Gaussian distribution [25], thus from this perspective, assuming that the step size of a person is in direct proportion to her height, we can model the step numbers between two sample locations as a random variable, which saves us from modeling complex factors that may affect the step counting methods. Given the random variable, we need to collect observations and estimate the location of it.

In the classical statistics, the distance is usually estimated by the mean value of a collection of sample data. However, as mentioned earlier, the collected data from users are highly untruthful due to unpredictable user behaviors and device malfunctioning, i.e., the data may be contaminated. classical statistical estimators are not able to handle contaminated data and may perform arbitrarily badly if contamination exists.

![](images/2dd39f2908d0a52814ce0e50a744eef71242978f7752e6b1d3a9d4e56f23e2eb.jpg)



Fig. 5. Simple example of trajectory and route. The trajectory consists of 4 fingerprints $( F _ { 1 } ^ { \mathrm { ~ \ i ~ } }$ to $F _ { 4 } )$ and 3 distance measurements (x1 to x3); while the corresponding physical route consists of 4 locations $( L _ { 1 }$ to L4) and 3 distance constraints (d to d ).

Robust statistics fits in this circumstance, which is able to alleviate the negative effects of contaminated data. Thus we naturally adopt this idea and apply robust estimator to estimate point-to-point distance.

# 4.1.2 Modeling Trajectory

To accommodate the specific scenery we encounter, we go a step further, i.e., we not only want to estimate the distance between two locations robustly, but hope to differentiate good users from bad users such that we form a high level of perspective regarding users. The trajectory estimation thus includes two folds: point-to-point distance estimates along the trajectory and user classification. The user-based information is novel and natural in crowdsourcing, and is subtly incorporated in our framework. Compared to the traditional robust distance measurements that has been introduced in multiple research fields, robust trajectory is of higher level perspective, and is more natural and effective in the emerging crowdsourcing applications.

Point-to-point distance is not sufficient to label a user as a good one or not, because accidently a good user may also report a corrupted measurement between two locations. For example, in Fig. 1, assume that a normal user U walk along the route $A \to { \overline { { B \to C } } } \to D$ . Accidently her smartphone fails to report the step counts in the segment $B  C$ . If we only use the distance reports between B and C, user U will be classified as abnormal, which is not what we expected. To comply with this difficulty, we propose to inspect a user in several consequent measurements along a route. We make use of multivariate random variable to model the consecutive sample location distances of a route. There are different kinds of multivariate robust estimators, among which we deem the minimum covariance determinant estimator as the best fit in our application, as it not only provides the robust distance estimate that we want, but also contains weight information equation (4) that we can further extract to label a user being normal or abnormal. More technique details will be discussed in the next subsection.

In summary, our trajectory estimation model includes two aspects: estimating the point-to-point distance of sample locations along the route and classifying a user as normal or abnormal.

# 4.2 Robust Trajectory Computation

# 4.2.1 Simple Trajectory

Given a collection of trajectory observations along a route, we assign a unique ID $i \in \mathcal { T }$ for each user. For the first stage, we assume that all observations are collected along the same route, thus we associate a d-dimension random vector X with the route (assuming that there are d þ 1 sample locations along the route), and each observation is denoted by $x _ { i } \in R ^ { d } ( { \mathrm { F i g . ~ } } 5 )$ . Suppose we have n trajectory observations of the route, now we want to robustly estimate the location of the real route. By using the MCD estimator, we obtain the estimate $T ( X )$ Þ:

$$
T (X) = \frac {1}{h} \sum_ {j \in H _ {\min}} x _ {j} \tag {5}
$$

where $H _ { \operatorname* { m i n } } = \arg \operatorname* { m i n } _ { H \in H _ { h } }$ det covðHÞ, with $H _ { h } = \{ Y \subseteq X$ : $| Y | = h \}$ .

The parameter h means that we expect to select h normal observations out of the total n observations. Thus h controls the BP value of the estimator, and as stated in Section 3, the estimator achieves the best BP value of 50 percent when $\begin{array} { r } { h = \lfloor \frac { n + d + 1 } { 2 } \rfloor } \end{array}$ . However, Experience [26] has shown that commonly, in practice, there are 1-10 percent outliers. Guided by this experience, we will set $h = 0$ :75n so that the BP value equals 25 percent, which also maintains a high statistical efficiency.

# 4.2.2 Compound Trajectory

Next we relax the assumption that all users walk along the same route. Consider that the route is divided into m parts, the j-th part has $d _ { j }$ segments and records $n _ { j }$ users’ data. Among the m parts, we assume there is one part that records all users’ data, which is quite reasonable in practice. For example, before entering a specific room, each user may have to walk along the corridor as shown in Fig. 7. We name this special part as the main-route, and the other parts as marginal-routes. To estimate the whole route, we first compute the main-route by using equation (5). At this stage, we have obtained the weight for each user, given by equation (4). The weights associated with users reflect normal/abnormal users. Thus in the next stage, we compute marginal-routes as follows, excluding the effect of abnormal users:

$$
T _ {j} (Y _ {j}) = \frac {\left(\sum_ {j \in Y _ {j}} w _ {j} x _ {j}\right)}{\left(\sum_ {j \in Y _ {j}} w _ {j}\right)}, j = 1, \dots , m \tag {6}
$$

where $Y _ { j } = \{ i \in \mathcal { T }$ : i-th user is in the m-th part of the routeg.

One may argue that why not use the same MCD estimator for marginal-routes as for the main-route. Firstly, there may be much fewer available users walking along marginal areas such as personal offices. In this situation, the statistical properties of only few observations are not sufficiently revealed. The other concern is that in some extremely unlucky scenery, there may be more bad users than good ones in the marginal area, which may result in completely wrong estimations if using the MCD estimator. Considering these aspects, obtaining prior trustworthy weights for users makes the whole estimation procedure more robust and practical.

# 4.2.3 Practical Concerns

Theoretically, the robust procedure we have designed so far should be adequate to compute all point-to-point distances. However, the framework need to be more carefully tailored in our application. Firstly, we notice that the step numbers of consecutive sample locations may be of small variation among different users, which makes it hard to recognize whether the user is walking normally or not. For example, an abnormal user may exhibit 2 steps less than other normal users between any two consecutive fingerprint sample locations, and this deviation may be treated acceptable. However, if the deviation accumulates for several consecutive sampled locations, the deviation is large enough to be detected as an outlier. Secondly, if we are to apply the proposed method for a long route, which is usually encountered in practice, too many trajectory records are required for calculation.

![](images/6b30d85961e2cea17496a07497c6d80e035f5d90c66500ce4b8d885f54e705dd.jpg)



Fig. 6. Floor plan.

To accommodate these difficulties, we divide the calculation into two steps. In the first place, we cut the main-route into k segments. Each segment contains 4-6 sample locations. By far, we can apply the MCD method to the main-route as stated above. We then have obtained the robust distance estimates for a chosen subset of sample locations and the weights for each user. In the next step, we make use of weighted mean values to calculate all necessary point-to-point distance estimates for the rest of sample locations in trajectory-dense and trajectory-sparse regions.

# 4.3 Discussion

The proposed method TrMCD is based on the statistical properties of mobile crowdsourced data as those proposed in existing solutions [2], [10], [12]. Therefore, TrMCD can fit into the majority of crowdsourcing based mobile applications easily. In addition, we conduct our experiments in typical office buildings where the corridor in the middle connects all other office rooms that lie on both sides of the corridor. Many mobile applications are designed for such scenarios since the building layout can be distinguished by user trajectories.

However, in large open environments, such as hall, atrium, gymnasium or museum, where user movements are difficult to characterize, the crowdsourcing-based methods may fail. From this aspect, the proposed TrMCD is also restricted to the building types in the moment. Yet we believe that, once the crowdsourcing applications scale to complex and large open environments, TrMCD can also scale as the crowdsourced data still possess statistical redundancy. In other words, TrMCD is only relevant to the statistical properties of mobile data, but independent of the specific environments where the data are collected.

# 5 EXPERIMENTS

In this section, we conduct two real field experiments to demonstrate the performance of TrMCD. Also, we introduce several tools to assist analyzing the results.

The experiments are conducted on one floor of an office building covering 1600 m2. As shown in Fig. 6, the building contains 16 offices, of which 5 are large rooms of 142 m2. We choose 4 large rooms, labeled Room 1-4 in Fig. 7, as they are easily accessible and are sufficed to design various pedestrian trajectories.

# 5.1 Data Pre-Processing

The rationality behind step counts is that the accelerations exhibit periodically repetitive patterns, which arises from the nature rhythmic of human walking. As shown in Fig. 8, the magnitude of acceleration during walking presents a stronger deviation and is easily recognizable. Therefore, step counts based on acceleration are widely applied in existing works [2], [10], [12].

![](images/353212c15450969c89288512acc57db1ec209726ca4d2345b52cd1f40cc3952a.jpg)



Fig. 7. Motion trajectories.

In this paper, we employ a local variance threshold method [27] to detect the step counts. The method filters the magnitude of acceleration and applies a threshold on the variance of acceleration over a sliding window. If the users are walking normally, the counting method is quite accurate in our experiment. However, in reality, there may be abnormal users reporting inaccurate outlier counts. For example, users may hold the phone steadily or jolt the phone from time to time while walking. These abnormal behaviors result in error or outlier readings, which can be well accommodated in TrMCD by using robust statistics.

The collected fingerprints from all users are first preprocessed to generate a reference fingerprint set. Given two fingerprints $f _ { i }$ and $f _ { j } ,$ we use the 1-norm distance as their RSS difference $\delta _ { i j } ,$ i.e., $\delta _ { i j } = \| f _ { i } - f _ { j } \| _ { 1 }$ . And we define a threshold $\epsilon ,$ such that the two fingerprints are considered from the same physical location if $\delta _ { i j } < \epsilon$ . In our experiment, we set $\epsilon = 3 0$ , as recommended in [10]. Then for all fingerprints that are assigned to the same physical location, we use the mean value to represent that location.

After the preprocessing phase, we collect a set of reference fingerprint points, which form a fingerprint space. Note that there may be error or outlier fingerprint readings in the collection. In this case, the error or outlier readings will propagate to the distance estimation between consecutive reference points. Therefore, the proposed robust trajectory estimation method (Section 4.1) is able to alleviate the influence abnormal fingerprint readings.

# 5.2 Evaluation of the Robust Trajectory

In this part, we are going to verify the robustness of the trajectory estimation obtained by using our proposed method TrMCD. Specifically, it’s expected that, with collected data contaminated by some outliers, the trajectory estimation can still approximately retain the geometric relation of the interested locations.

As shown in Fig. 7, We choose A, B, C, and D (stars in the figure) as interested location points, with the length of each segment being $A B = 1 0 \mathrm { ~ m } , \ : \ : \ : B C = 1 0 \mathrm { ~ m } , \ : \ : C D = 1 1$ m and DA ¼ 15 m. 20 volunteers are recruited to walk through these reference points. We only constrain that they should walk in the order $A \to B \to C \to D \to A$ . And they can choose whatever path or walking manner or the way they take the phones. From the floor plan we can see that, users have large degree of freedom to choose the path. Due to these loose constraints, the trajectory records they collect will exhibit variations. And we also ask 3 of them to behave adversely, i.e., to create outlier observations intentionally.

![](images/5c854bf534204cf1e0f430525d400a3fe27e7a99dc817f119edce8819e972864.jpg)



Fig. 8. Acceleration pattern for 10 steps.

TABLE 1 Walking Step Numbers 

<table><tr><td>AB</td><td>BC</td><td>CD</td><td>DA</td><td>AB</td><td>BC</td><td>CD</td><td>DA</td></tr><tr><td>13</td><td>13</td><td>15</td><td>20</td><td>11</td><td>12</td><td>14</td><td>19</td></tr><tr><td>12</td><td>13</td><td>14</td><td>18</td><td>12</td><td>12</td><td>15</td><td>20</td></tr><tr><td>14</td><td>14</td><td>15</td><td>20</td><td>13</td><td>12</td><td>16</td><td>20</td></tr><tr><td>13</td><td>14</td><td>15</td><td>21</td><td>11</td><td>12</td><td>14</td><td>18</td></tr><tr><td>13</td><td>14</td><td>16</td><td>21</td><td>12</td><td>12</td><td>15</td><td>19</td></tr><tr><td>11</td><td>12</td><td>14</td><td>18</td><td>14</td><td>14</td><td>16</td><td>21</td></tr><tr><td>12</td><td>13</td><td>15</td><td>19</td><td>3</td><td>30</td><td>100</td><td>40</td></tr><tr><td>14</td><td>15</td><td>16</td><td>22</td><td>13</td><td>14</td><td>15</td><td>20</td></tr><tr><td>1</td><td>13</td><td>14</td><td>20</td><td>14</td><td>15</td><td>16</td><td>21</td></tr><tr><td>14</td><td>15</td><td>17</td><td>22</td><td>15</td><td>20</td><td>40</td><td>30</td></tr></table>

Here we cut the trajectory into four pieces according to the four reference points. The step numbers are shown in Table 1. Note that the step number varies among different users for multiple reasons, for example, the position where the user keeps the mobile phone, the height differences among users, the gender of a user, the walking habit of a user, etc. All of these factors will cause the step numbers to deviate from the ideal result, and are considered normal noises. However, the adverse users may create outlier observations that are far away from those normally obtained data. For instance, an anomalous user may keep the mobile phone extremely stable while walking, which cheats the mobile phone that the user is not walking at all, or she may choose a very long and curving path between reference points, which results in exceptionally many steps.

To verify the effectiveness of the robust estimation, we compare it with other two commonly used methods, i.e., the shortest path, corresponding to the Least Value (LV) estimator, and the average path, corresponding to the LS estimator. The quality of an estimate of the trajectory can be measured by the transform ratio and variance. Specifically, the transform ratio is defined as the ratio of estimate distance to ground truth distance for each pair of reference points in a suitable space. If the estimation is accurate, the ratio values of all pairs of reference points should be the same; otherwise, the ratio values will present large variances, meaning that the geometrical relations among reference points are not well preserved. Table 2 shows the results of the three approaches. We can see that TrMCD well preserve the spatial constraints on the four reference points, with the ratio variance being close to 0. LV estimator performs worst as it is very sensitive to small value outlier measurements. LS estimator seems not easy to be broken down from the statistics in the table, however, the outlier measurements are not very sharp in our experiment, and the sufficient number of users also helps to alleviate the influence of outliers. In our application, as will be shown in the following experiment, LS estimate will be greatly biased in trajectory-sparse area and hence distort the trajectory severely.

TABLE 2 Ratio and Variance 

<table><tr><td rowspan="2">Methods</td><td colspan="4">Ratio</td><td rowspan="2">Variance</td></tr><tr><td>AB</td><td>BC</td><td>CD</td><td>DE</td></tr><tr><td>TrMCD</td><td>1.2687</td><td>1.3375</td><td>1.3528</td><td>1.3291</td><td>0.0014</td></tr><tr><td>LS</td><td>1.1750</td><td>1.4450</td><td>1.8425</td><td>1.4300</td><td>0.0760</td></tr><tr><td>LV</td><td>0.1000</td><td>1.2000</td><td>1.2522</td><td>1.2000</td><td>0.3128</td></tr></table>

![](images/fd0b70d3d7087cc6700a591f8a3f997ef49159c9c8c9973cfd153c50354a699d.jpg)



Fig. 9. CDF of mapping error.

# 5.3 Mapping Trajectories to Locations

To certify the performance of TrMCD in mapping the crowdsourced fingerprints to physical locations, we conduct a real field indoor experiment. As a comparison, we will compare the performance of TrMCD to the traditional LS estimator.

The floor plan of the office building where we conduct the experiment is shown in Fig. 6. As our purpose is to verify the robustness of TrMCD in forming hfingerprint, positioni pairs, four rooms (Room 1-4 in the figure) and the corridor are adequate such that we don’t need the luxury of employing too many volunteers and at the same time, the superiority of TrMCD can be shown both visually and statistically.

Among the 20 users recruited, we ask three (two users in Room 1 and one user in Room 4) to play the role of ‘‘bad’’ guys, i.e., they will intentionally report outlier observations. Specifically, the abnormal user in Room 4 and one abnormal user in Room 1 tries to cheat the mobile phone sensor by walking steadily so that the step counting method based on accelerometer fails; while the other abnormal user in Room 1 creates more step counts by jolting her phone from time to time. Each user’s phone will record the fingerprints every 4 or 5 steps (corresponding to 2 to 3 meters under normal walking styles), which are chosen to approximately conform with the floor plan sampling resolution. At the same time, the step counting and reference fingerprint set are acquired as demonstrated in Section 5.1.

The cumulative distribution (CDF) of the location mapping error is plotted in Fig. 9. The red curve represents the CDF of TrMCD, while the blue one represents the CDF of the LS estimator. The red curve is upper-left to the blue one for all scales of errors, indicating the superiority of TrMCD. The mapping results obtained by TrMCD are robust and satisfactory as around 90 percent of the points are located within 3 meters of error. In addition, the average mapping error of TrMCD is 0.84 meters, superior to that of 2.13 meters obtained by LS estimator.

Further illustration and analysis of the experiment can be found in the supplementary file which is available in the Computer Society Digital Library at http://doi. ieeecomputersociety.org/10.1109/250.

# 6 CONCLUSION

In this paper, we investigated the problem of how to estimate crowdsourced user motion trajectories robustly and map the fingerprints to the physical locations correctly. We have derived a robust estimation method, named TrMCD, which can not only predict user trajectories, but also differentiate normal users from abnormal users, resulting in a novel userbased robustness. The difficulty in trajectory estimation due to unbalance distribution of crowdsourced trajectories is also accommodated in TrMCD. The preliminary experiment results show that TrMCD achieves high robustness and effectiveness compared to the traditional LV estimator and LS estimator. TrMCD sets up a pioneer work to guarantee that the large amount of crowdsourced data is used in a robust and effective way. Our ongoing research focus on tailoring our method for specific crowdsourcing-based mobile applications.

# ACKNOWLEDGMENT

This work is supportedin part by the NSFC Major Program 61190110, NSFC under Grant 61171067, 61133016, and 61332004, National Basic Research Program of China (973) under Grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under Grant 61125202.

# REFERENCES

[1] Worldwide Mobile Phone Market at the End of 2012. [Online]. Available: https://www.idc.com/getdoc.jsp?containerId= prUS23916413.   
[2] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. Choudhury, ‘‘No Need to War-Drive: Unsupervised Indoor Localization,’’ in Proc. ACM MobiSys, 2012, pp. 197-210.   
[3] A. Rai, K. Chintalapudi, V. Padmanabhan, and R. Sen, ‘‘Zee: Zero-Effort Crowdsourcing for Indoor Localization,’’ in Proc. ACM MobiCom, 2012, pp. 293-304.   
[4] Z. Li, W. Trappe, Y. Zhang, and B. Nath, ‘‘Robust Statistical Methods for Securing Wireless Localization in Sensor Networks,’’ in Proc. IEEE IPSN, 2005, pp. 91-98.   
[5] H. Kung, C. Lin, T. Lin, and D. Vlah, ‘‘Localization with Snap-Inducing Shaped Residuals (SISR): Coping with Errors in Measurement,’’ in Proc. ACM MobiCom, 2009, pp. 333-344.   
[6] P. Bahl and V. Padmanabhan, ‘‘Radar: An In-Building RF-Based User Location and Tracking System,’’ in Proc. IEEE INFOCOM, 2000, pp. 775-784.

[7] M. Youssef and A. Agrawala, ‘‘The Horus Location Determination System,’’ Wireless Netw., vol. 14, no. 3, pp. 357-374, June 2008.   
[8] L. Ni, Y. Liu, Y. Lau, and A. Patil, ‘‘Landmarc: Indoor Location Sensing using Active RFID,’’ Wireless Netw., vol. 10, no. 6, pp. 701- 710, Nov. 2004.   
[9] M. Azizyan, I. Constandache, and R. Roy Choudhury, ‘‘Surroundsense: Mobile Phone Localization via Ambience Fingerprinting,’’ in Proc. ACM MobiCom, 2009, pp. 261-272.   
[10] Z. Yang, C. Wu, and Y. Liu, ‘‘Locating in Fingerprint Space: Wireless Indoor Localization with Little Human Intervention,’’ in Proc. ACM MobiCom, 2012, pp. 269-280.   
[11] M. Alzantot and M. Youssef, ‘‘Crowdinside: Automatic Construction of Indoor Floorplans,’’ in Proc. ACM SIGSPATIAL GIS, 2012, pp. 99-108.   
[12] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, ‘‘Walkie-Markie: Indoor Pathway Mapping Made Easy,’’ in Proc. USENIX NSDI, 2013, pp. 85-98.   
[13] J.A.B. Link, P. Smith, N. Viol, and K. Wehrle, ‘‘Footpath: Accurate Map-Based Indoor Navigation using Smartphones,’ in Proc. IEEE IPIN, 2011, pp. 1-8.   
[14] I. Constandache, X. Bao, M. Azizyan, and R.R. Choudhury, ‘‘Did You See Bob?: Human Localization using Mobile Phones,’’ in Proc. ACM MobiCom, 2010, pp. 149-160.   
[15] J. Liu, Y. Zhang, and F. Zhao, ‘‘Robust Distributed Node Localization with Error Management,’’ in Proc. ACM MobiHoc, 2006, pp. 250-261.   
[16] D. Moore, J. Leonard, D. Rus, and S. Teller, ‘‘Robust Distributed Network Localization with Noisy Range Measurements,’’ in Proc. ACM SenSys, 2004, pp. 50-61.   
[17] Z. Yang and Y. Liu, ‘‘Quality of Trilateration: Confidence-Based Iterative Localization,’’ IEEE Trans. Parallel Distrib. Syst., vol. 21, no. 5, pp. 631-640, May 2010.   
[18] Z. Yang, L. Jian, C. Wu, and Y. Liu, ‘‘Beyond Triangle Inequality: Sifting Noisy and Outlier Distance Measurements for Localization,’’ ACM Trans. Sensor Netw., vol. 9, no. 2, pp. 26:1-26:20, Mar.2013.   
[19] R. Maronna, ‘‘Robust m-Estimators of Multivariate Location and Scatter,’’ Ann. Statist., vol. 4, no. 1, pp. 51-67, Jan. 1976.   
[20] R. Gnanadesikan and J. Kettenring, ‘‘Robust Estimates, Residuals, Outlier Detection with Multiresponse Data,’’ Biometrics, vol. 28, no. 1, pp. 81-124, Mar. 1972.   
[21] S. Devlin, R. Gnanadesikan, and J. Kettenring, ‘‘Robust Estimation and Outlier Detection with Correlation Coefficients,’’ Biometrika, vol. 62, no. 3, pp. 531-545, Dec. 1975.   
[22] P. Rousseeuw, ‘‘Multivariate Estimation with High Breakdown Point,’’ Mathematical Statistics and Applications, vol. 8. Dordrecht, The Netherlands: Reidel, 1985, pp. 283-297.   
[23] P. Rousseeuw and K. Van Driessen, ‘‘A Fast Algorithm for the Minimum Covariance Determinant Estimator,’’ Technometrics, vol. 41, no. 3, pp. 212-223, Aug. 1999.   
[24] S. Verboven and M. Hubert, ‘‘Libra: A Matlab Library for Robust Analysis,’’ Chemometrics Intell. Lab. Syst., vol. 75, no. 2, pp. 127- 136, Feb. 2005.   
[25] D.F. Gudbjartsson, G.B. Walters, G. Thorleifsson, H. Stefansson, B.V.Halldorsson,P.Zusmanovich,P.Sulem,S.Thorlacius,A.Gylfason, S. Steinberg, A. Helgadottir, A. Ingason, V. Steinthorsdottir, E.J. Olafsdottir, G.H. Olafsdottir, T. Jonsson, K. Borch-Johnsen, T. Hansen, G. Andersen, T. Jorgensen, O. Pedersen, K.K. Aben, J.A. Witjes, D.W. Swinkels, M. den Heijer, B. Franke, A.L. Verbeek, D.M. Becker, L.R. Yanek, L.C. Becker, L. Tryggvadottir, T. Rafnar, J. Gulcher, L.A. Kiemeney, A. Kong, U. Thorsteinsdottir, and K. Stefansson, ‘‘Many Sequence Variants Affecting Diversity of Adult Human Height,’’ Nat. Genet., vol. 40, no. 5, pp. 609-615, May 2008.   
[26] F. Hampel, E. Ronchetti, P. Rousseeuw, and W. Stahel, Robust Statistics: The Approach Based on Influence Functions. Hoboken, NJ, USA: Wiley, 2011.   
[27] A. Jimenez, F. Seco, C. Prieto, and J. Guevara, ‘‘A Comparison of Pedestrian Dead-Reckoning Algorithms using a Low-Cost MEMS IMU,’’ in Proc. IEEE WISP, 2009, pp. 37-42.   
[28] Y. Tong, L. Chen, Y. Cheng, and P. Yu, ‘‘Mining Frequent Itemsets over Uncertain Databases,’’ in Proc. of VLBD Endowment, 2012.   
[29] Y. Tong, L. Chen, and B. Ding, ‘‘Discovering Threshold-Based Frequent Closed Itemsets over Probabilistic Data,’’ in Proc. IEEE ICDE, 2012.

![](images/276572fb0e54d7b2f7f1837c83871b9055166f8810af1187f1de78442eaaad06.jpg)



Xinglin Zhang received the BE degree in School of Software from Sun Yat-sen University, Guangdong, China, in 2010. He is now pursuing the PhD degree in Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include wireless ad-hoc/sensor networks, mobile computing and crowdsourcing. He is a Student Member of the IEEE and the ACM.

![](images/fb9e9dcc2453bcff984f75998e9ccd17289aab339aff7b173710d8816d739ec2.jpg)



Zheng Yang received a BE degree in computer science from Tsinghua University, China, in 2006 and the PhD degree in computer science from Hong Kong University of Science and Technology. Hong Kong, in 2010. He is currently an Assistant Professor in Tsinghua University. His main research interests include wireless ad-hoc/ sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/7debfc7ad7d53a1a81de70c6843315a1ac8452b73ba823cf32e29172bed911f2.jpg)



Chenshu Wu received the BE degree in School of Software from Tsinghua University, Beijing, China, in 2010. He is now pursuing the PhD degree in Department of Computer Science and Technology, Tsinghua University. He is a member of Tsinghua National Lab for Information Science and Technology. His research interests include wireless ad-hoc/sensor networks and pervasive computing. He is a Student Member of the IEEE and the ACM.

![](images/c6b59d2e7ce00749d7d402bec883f51cd48b7df6d76c9f637371287781997cd5.jpg)



Wei Sun received the BE degree in the School of Computer Science and Technology from University of Science and Technology of China, China, in 2011. He is now pursuing the PhD degree in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong. His research interests include wireless sensor networks and pervasive computing. He is a Student Member of the IEEE and the ACM.

![](images/e6b1d2522efd6d477e1e8a5f3c1eb3d4e8631368ebb1b425345c135067b0ac0a.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now a professor at Tsinghua University. His research interests include wireless sensor network, peerto-peer computing, and pervasive computing. He is a Senior Member of the IEEE.

![](images/1d088fc0d9bbdc86a068268d636b0f104a43a2f34b2d3105ee958f0fb8f9fba8.jpg)



Kai Xing received the MS and PhD degrees in computer science from The George Washington University, Washington, DC in 2006 and 2009, respectively. He is an Associate Professor at the School of Computer Science and Technology, The University of Science and Technology of China. He received his MS and PhD degree in Computer Science from The George Washington University in 2006 and 2009, respectively. His current research interests included cyber physical networking systems, wireless networks,

mobile computing, in-network information processing, and network security. He is a member of the IEEE and the ACM.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.