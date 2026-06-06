# Montage: Combine Frames with Movement Continuity for Realtime Multi-User Tracking

Lan Zhang, Member, IEEE, Kebin Liu, Member, IEEE, Yonghang Jiang, Member, IEEE, Xiang-Yang Li, Fellow, IEEE, Yunhao Liu, Fellow, IEEE, Panlong Yang, Member, IEEE, and Zhenhua Li, Member, IEEE

Abstract—In this work we design and develop Montage for real-time multi-user formation tracking and localization by off-the-shelf smartphones. Montage achieves submeter-level tracking accuracy by integrating temporal and spatial constraints from user movement vector estimation and distance measuring. In Montage we designed a suite of novel techniques to surmount a variety of challenges in real-time tracking, without infrastructure and fingerprints, and without any a priori user-specific (e.g., stride-length and phone-placement) or site-specific (e.g., digitalized map) knowledge: (1) a coded audio tone to support multi-user tracking with minimal latency, in the presence of high noise, multi-path effect and Doppler Shift (2) an innovative stride-length and walking direction estimation method without a priori knowledge of user and site, (3) a vector-based multi-user tracking scheme which connects successive localization snapshots to refine users’ locations and generate continuous moving traces. We implemented, deployed and evaluated Montage in both outdoor and indoor environment. Our experimental results (847 traces from 15 users) show that the stride-length estimated by Montage over all users has error within 9cm, and the moving-direction estimated by Montage is within 20o. For real-time tracking, Montage provides meter-second-level formation tracking accuracy with off-the-shelf mobile phones.

Keywords—Multi-User Tracking, Indoor Localization, Mobile Computing

# 1 INTRODUCTION

RACKING the spatial-temporal formation of multiple mobile users plays an important role in many applications, e.g., real-time team-formation tracking for teamsports strategy study, animal community monitoring for behavior analysis, and virtual-reality interactive games. When users are outdoor, localization and tracking could be solved by GPS. The accurate indoor tracking/localization in realtime is still challenging and has attracted considerable research efforts.

One category of existing methods are based on fingerprints, e.g., [6], [22], [31], which achieve room-level (meter-level) accuracy. Those methods, however, are typ-

L. Zhang is with the School of Computer Science and Technology, University of Science and Technology of China, and School of Software and TNLIST, Tsinghua University.   
E-mail: zhanglan03@gmail.com   
• K. Liu is with the School of Software and TNLIST, Tsinghua University. E-mail: kebin@greenorbs.com   
• Y. Jiang is with the Department of Computer Science, City University of Hong Kong.   
E-mail: leo.jyh@gmail.com   
X.-Y. Li is with School of Computer Science and Technology, University of Science and Technology of China.   
E-mail: xiangyang.li@gmail.com   
Y. Liu is with the School of Software and TNLIST, Tsinghua University. E-mail: yunhao@greenorbs.com   
• P. Yang is with the School of Computer Science and Technology, University of Science and Technology of China.   
E-mail: panlongyang@gmail.com   
• Z. Li is with the School of Software and TNLIST, Tsinghua University. E-mail: lizhenhua1983@tsinghua.edu.cn

ically labor intensive and environment restrictive during fingerprint collection stage. Many dedicated systems with specialized hardware, e.g. sensors [32] and RFID [12], [29], can achieve high accuracy, but are not applicable for phones. Another category of approaches are range-based using different metrics. The acoustic based methods on commercial mobile handset address the issue of meter-level pair-wise ranging, e.g., [17], [18]. Some other solutions use code division multiple access (CDMA) acoustic telemetry to simultaneously monitor the movements of numerous individual users, e.g., [16]. Those schemes, however, require either accurate synchronization or a synchronized hydrophone array which is quite difficult to be implemented on commercial phones. Dead reckoning based approaches, e.g. [1], suffer from accumulated errors. Most of the exiting indoor tracking solutions need a pre-knowledge or at least three anchors.

There are many challenges in achieving high accurate multi-user tracking due to the highly dynamic and continuously evolving movement pattern of mobile users. Acoustic-based ranging can be used to obtain the frame snapshot of multi-user formation. With commercial phones, the accurate acquisition of audio tones is difficult due to the attenuation, distortion, interference, and multi-path effect. Besides, for multiple dynamic users, the required small ranging delay and the narrow available acoustic band make the multi-user ranging even more difficult. As the detectable distance by the audio tone is limited, the ranging results of some frame snapshots may be ambiguous, leaving some users still nonlocalizable. Even when ranging results can produce snapshots of team formation, the continuous movements of individuals are hard to obtain without anchor nodes. We need accurate information about the moving distance and moving direction of users to combine these scattered frames to achieve continuous tracking. The movement continuity may also help to remove ambiguities from each frame. Previous schemes estimate the moving distance and direction by dead-reckoning [20]. But special devices or pre-knowledge are usually required, $e . g .$ , [19], [28], and absolute positions are also require to fix the accumulated errors.

To address above issues, we propose Montage, to track the realtime formation and movements of multiple users. This design uses the coded acoustic signal for simultaneous multi-user ranging and inertial sensors for accurate moving distance/direction estimation. Combining the ranging results and moving estimations, Montage provides meter-second-level formation tracking with off-theshelf mobile phones and requires no pre-knowledge or synchronization services. It achieves accurate localization using merely one anchor node. The contributions of this work are as follows:

• We design coded audio tones with which the instantaneous distances among multiple mobile users are accurately estimated when they generate tones simultaneously, in the presence of high noise, multipath effect and Doppler Shift.   
• We present innovative step stride-length and walking direction estimation methods to achieve a very accurate moving trace estimation without any priori knowledge (such as the stride-length, phoneplacement and indoor map).   
• We connect successive localization snapshots to refine the range-based localization and generate continuous moving traces, by leveraging the accurate moving distance and direction estimation. It provides better disambiguation and estimates the real trace of users without anchor nodes.   
• We design, develop, and deploy Montage in both indoor and outdoor environment to evaluate its performance. 847 traces from 15 volunteers are collected and analyzed. The results show that the estimated stride-lengths over a variety of users have errors within 8.9cm and the mean error is 4.3cm. The estimated moving-direction is within $2 0 ^ { o }$ of the real direction. For real-time single-user indoor tracking, the mean deviation of 847 traces is about 0.87 meter, and 90% deviations are less than 2 meters. For realtime multiuser indoor experiment, the maximum deviation is about 1m while the mean deviation is about 0.5m using both inertial sensors and acoustic ranging.

The rest of the paper is organized as follows. We present problem formation and baseline method in Section 2, and novel multiuser ranging with coded audio tones in Section 3. In Section 4 we discuss our techniques of accurate estimation of moving distance and direction. Our evaluation results are presented in Section 5. We review the related work in Section 6 and conclude the paper in Section 7.

# 2 OUR APPROACH

Assume that there is a group of n mobile users $A =$ $\{ a _ { 1 } , \ldots , a _ { n } \}$ in proximity. At time t, the location of user $a _ { i }$ at earth coordinate is $\dot { P _ { i } ^ { e } } ( t ) = ( x _ { i } ^ { e } ( t ) , y _ { i } ^ { e } ( t ) )$ . If we record the location of user $a _ { i }$ according to the time vector $T =$ $\{ t _ { 0 } , t _ { 1 } , \cdots , t _ { M } \}$ , the moving trace of $a _ { i }$ can be represented by a sequence of locations $\{ P _ { i } ^ { e } ( t _ { 0 } ) , \dot { P } _ { i } ^ { e } ( t _ { 1 } ) , \cdots , \sp { \bf \underline { { { \sigma } } } } , P _ { i } ^ { e } ( t _ { M } ) \}$ . For simplicity of presentation, besides the earth coordinate system, we introduce the translation coordinate system in which each location has a constant offset from that of earth coordinate, $i . e . $ , the origin of a translation coordinate system is moved but the directions of both axes remain the same. For example, let $P _ { 1 } ^ { e } ( t _ { 0 } ) = ( x _ { 1 } ^ { e } ( t _ { 0 } ) , y _ { 1 } ^ { e } ( t _ { 0 } ) )$ be the origin of a translation coordinate system, noted as $P _ { 1 } ( t _ { 0 } ) = ( \breve { 0 } , 0 )$ . If the position of $a _ { i }$ at the translation coordinate is $\dot { P } _ { i } ( \dot { t _ { 0 } } ) = ( x _ { i } \dot { ( } t _ { 0 } ) , y _ { i } ( t _ { 0 } ) )$ , then its earth location is $P _ { i } ^ { e } ( t _ { 0 } ) = P _ { i } ( t _ { 0 } ) + P _ { 1 } ^ { e } ( t _ { 0 } ) ^ { \prime } = ( x _ { 1 } ^ { e } ( t _ { 0 } ) + x _ { i } ( t _ { 0 } ) , y _ { 1 } ^ { e } ( t _ { 0 } ) + y _ { i } ( t _ { 0 } ) )$ .

# 2.1 Main Idea

Our goal is to design a scheme for precise mobile user tracking without pre-deployed infrastructures. Our scheme exploits coded acoustic signals to simultaneously measure the distances among users. The ranging results expose multi-users’ distances at a certain timestamp and thus indicate a logical topology of the network. The logical structure, normally, lacks orientation information and may not be rigid [27]. The second component is the movement vectors detection which leverages information from various sensors on the smartphones. The movement vectors connect locations of the same user at consecutive timestamps. With the ranging results and movement vectors, Montage dynamically calculates the distance vectors to measure the Euclidean distance between different users. Using these vectors, we can easily reassemble the real topology and continuously track users’ movement traces. In Montage, the localization and tracking are at a translation coordinate system in the absence of anchor nodes. As the translation coordinate has a fixed offset from the earth coordinate, given an arbitrary anchor point $P _ { i } ^ { e } ( t _ { j } )$ , our approach can determine the traces and locations at the earth coordinate.

# 2.2 Baseline Approach for Localization

User $a _ { i }$ moves from location $P _ { i } ^ { e } ( t _ { u } )$ to $P _ { i } ^ { e } ( t _ { v } )$ during period $t _ { u }$ to $t _ { v } .$ The movement vector is

$$
M _ {i} (t _ {u}, t _ {v}) = P _ {i} ^ {e} (t _ {v}) - P _ {i} ^ {e} (t _ {u}) = P _ {i} (t _ {v}) - P _ {i} (t _ {u}),
$$

which is independent of the coordinate system and only determined by its magnitude/distance d and orientation θ. The movement vector can also be represented by a twotuple $( r _ { i } ^ { u v } , \theta _ { i } ^ { u v } )$ in the polar coordinate system. Then, the trace of a single user $a _ { i }$ can be recorded by a sequence of movement vectors $\{ M _ { i } ( t _ { 0 } , t _ { 1 } ) , M _ { i } ( t _ { 1 } , t _ { 2 } ) , \cdot \cdot \cdot \}$ . At the time $t _ { u } ,$ the distance vector between user $a _ { i }$ and $a _ { j }$ is defined as

![](images/947bcd229b4ad5a1800721b1fa4a1cfa11570d81ca58bb7a23c5bbaf9f140bd7.jpg)

![](images/849ee7fbbb3dc50463a1b3dbede3d2c3867534db3763a4172114dc883af3490d.jpg)



(1)

![](images/7d1b159f660385bd82191ad9c3b384e4936ece809c7e973816a5365fd28fe88e.jpg)



(2)   
(b) Localize users in sequel   
Fig. 1. Baseline team formation tracking based on movement vector and ranging results.

$$
R _ {i j} (t _ {u}) = P _ {i} ^ {e} (t _ {u}) - P _ {j} ^ {e} (t _ {u}) = P _ {i} (t _ {u}) - P _ {j} (t _ {u}).
$$

The magnitude of the distance vector can be measured by the ranging result between $a _ { i }$ and $a _ { j } ,$ say $r _ { i j } ( t _ { u } )$ . As shown in Fig. 1(a), $M _ { i } ( t _ { 0 } , t _ { 1 } )$ and $M _ { j } ( { \bar { t } } _ { 0 } , t _ { 1 } )$ are movement vectors of user $a _ { i }$ and $a _ { j } . ~ R _ { i j } ( \dot { t } _ { 0 } )$ and $R _ { i j } ( t _ { 1 } )$ are distance vectors at time $t _ { 0 }$ and $t _ { 1 }$ .

Given ranging results, which are the magnitude of distance vectors, only a formation of user locations can be derived at a time if the topology is rigid. The orientation of the formation is uncertain, thus we cannot derive the traces of users’ movement from consecutive formations. The output of the trace detection scheme is represented as a sequence of movement vectors for each single user, but the locations of points in the trace are undetermined. We propose to combine the ranging results and movement vectors to localize all users at each sample time and to acquire continuous user traces. Our approach is based on the observation that the distance vectors and the movement vectors meet the following equation:

$$
\begin{array}{l} D _ {i j} (t _ {u + 1}) = R _ {i j} (t _ {u + 1}) - R _ {i j} (t _ {u}) \tag {1} \\ = M _ {j} (t _ {u}, t _ {u + 1}) - M _ {i} (t _ {u}, t _ {u + 1}). \\ \end{array}
$$

Here $D _ { i j } ( t _ { u + 1 } )$ is defined as the difference vector. Let the two-tuple of the difference vector $\tilde { D _ { i j } } ( t )$ be $( d _ { i j } ( t ) , \theta _ { i j } ( t ) )$ . As illustrated by Fig. 1(a), $D _ { i j } ( t _ { 1 } )$ is the difference vector. When the movement vectors $\dot { M } _ { i } ( t _ { 0 } , t _ { 1 } )$ and $M _ { j } ( t _ { 0 } , t _ { 1 } )$ are known, $D _ { i j } ( t _ { 1 } )$ is determined. And, we have

$$
\left\{ \begin{array}{l} r _ {i j} (t _ {1}) \cos \theta_ {i j} (t _ {1}) - r _ {i j} (t _ {0}) \cos \theta_ {i j} (t _ {0}) = d _ {i j} (t _ {1}) \cos \theta_ {i j} (t _ {1}) \\ r _ {i j} (t _ {1}) \sin \theta_ {i j} (t _ {1}) - r _ {i j} (t _ {0}) \sin \theta_ {i j} (t _ {0}) = d _ {i j} (t _ {1}) \sin \theta_ {i j} (t _ {1}) \end{array} \right. \tag {2}
$$

Given the ranging results $r _ { i j } ( t _ { 0 } )$ and $r _ { i j } ( t _ { 1 } )$ , each solution for $\theta _ { i j } ( t _ { 0 } )$ and $\theta _ { i j } ( t _ { 1 } )$ determines a possible assignment of $a _ { i }$ and $a _ { j } ^ { \prime } \mathbf { s }$ positions at time $t _ { 0 }$ and $t _ { 1 }$ . When $r _ { i j } ( t _ { 1 } ) + r _ { i j } ( t _ { 0 } ) > d _ { i j } ( t _ { 1 } )$ and $r _ { i j } ( t _ { 1 } ) - r _ { i j } ( t _ { 0 } ) < d _ { i j } ( t _ { 1 } )$ , there exist two solutions. As illustrated in Fig. 1(a), both the position groups $\{ P _ { j } ( t _ { 0 } ) , P _ { j } ( t _ { 1 } ) \}$ and $\{ P _ { j } ( t _ { 0 } ) ^ { \prime } , P _ { j } ( t _ { 1 } ) ^ { \prime } \}$ satisfy the constrains of distance vectors and movement vectors. When $r _ { i j } ( t _ { 1 } ) + r _ { i j } ( t _ { 0 } ) ~ = ~ d _ { i j } ( t _ { 1 } )$ or $r _ { i j } ( t _ { 1 } ) \textrm { - }$ $r _ { i j } ( t _ { 0 } ) = d _ { i j } ( t _ { 1 } )$ , there is only one solution, as shown in Fig. 1(a). There exists a special case that the movement vector $M _ { i } ( t _ { 0 } , t _ { 1 } )$ of user $a _ { i }$ and $M _ { j } ( t _ { 0 } , t _ { 1 } )$ of user $a _ { j }$ are equal, i.e. they move in the same direction at the same speed. In this case, $r _ { i j } ( t _ { 1 } ) = r _ { i j } ( t _ { 0 } )$ and there are infinite groups of solutions.

Based on the above calculation, each distance vector may have one, two or infinite possible solutions. For the first case, the distance vector is determined. For the third case, we cannot decide the value of distance vector and require further information. The most common situation is that there are two possible values for the distance vector with the same magnitude while different orientations. In this case, we leverage the neighboring information to eliminate the ambiguity. In the above example, assume that user $a _ { i }$ and $a _ { j }$ both have ranging results to a third user ${ \mathit { a } } _ { k } ,$ then we can get the two possible solutions of $R _ { i k }$ and $R _ { j k }$ as well. Clearly, locations of the user $a _ { i } ,$ $a _ { j }$ and $a _ { k }$ form a triangle (called ranging triangle), and thus theoretically the value of three distance vectors must meet the following equation.

$$
R _ {i j} + R _ {j k} - R _ {i k} = 0 \tag {3}
$$

As each vector has two potential solutions, there are 8 combinations in all. For example in Fig. 1(b)(1), the distance vectors in solid lines meet the equation constraint and the combination in dashed lines is a wrong answer because it leads to two ambiguous locations of user $a _ { j } .$ In practice, we select the combination which minimizes the absolute value of Equation (3). With this scheme, we can determine three distance vectors that are edges of a ranging triangle and thus rebuild the triangle.

# 2.3 Vector Based Multi-User Tracking

We will further discuss the full-featured user tracking approach. In the first step, we select an arbitrary ranging triangle and determine the three distance vectors (edges) of this triangle using the algorithm discussed in previous subsection. Here we prefer to select the start triangle whose vertices have more ranging neighbors. Then we put all three users in this triangle into a set denoted as localized set which keeps all the distance vectors as well.

In the second step, we iteratively add more users to the localized set by determining distance vectors from the new user to neighboring users in the localized set. As illustrated in Fig. 1(b)(2), user $a _ { m }$ has ranging results with $a _ { i }$ and $a _ { j }$ . According to the aforementioned baseline algorithm, we get one or two possible solutions for each of $R _ { i m }$ and $R _ { j m }$ . We simply drop the results of zero solution or infinite solutions, because the distance vector cannot be determined according to them. For the two-solution case, based on the observation that $R _ { i m } ,$ $R _ { j m }$ and $R _ { i j }$ form a triangle, and theoretically we have $\bar { R _ { i j } } + { R _ { i m } } - \bar { R } _ { i m } = 0$ . To address the ranging errors, we will select the pair of $R _ { i m } , R _ { j m }$ values that minimizes $R _ { i j } + R _ { j m } - \bar { R _ { i m } }$ . After that, the distance vectors from two users in localized set to $a _ { m }$ have been determined. We put $a _ { m }$ into the localized set and keep both distance vectors. We calculate the distance vectors from a pair of neighboring users instead of separated ones to a new user, for the purpose of avoiding cascading errors. The above process iterates until no new user can be added. These vectors corresponding to users in the localized set specify the relative locations of users and if we assign location (e.g. at earth or translation coordinate system) for any one of them, all the other users can be located at the specified coordinate system.

Now we have localized all users (obtain distance vectors and rebuild the topology) at time $t _ { 0 }$ and $t _ { 1 , }$ in the coming timestamp $t _ { 2 }$ the localization process can be significantly simplified. Later in Section 2.4 we will show how to calculate the distance vector based on Eq. (1). With knowing the value of the distance vector in prior timestamp, $R _ { i j } ( t _ { 1 } )$ in the example of Fig. 1(a), the distance vector $R _ { i j } ( t _ { 2 } )$ can be directly calculated using $R _ { i j } ( t _ { 1 } ) ~ + ~ D _ { i j } ( t _ { 2 } )$ . With this method, Montage conducts localization in consecutive timestamps and rebuilds topology snapshots over time.

After rebuilding the topology at translation coordinate for each timestamp, we connect these topology snapshots and form integrated user movement traces. As the movement vectors connect locations among continuous timestamps, Montage leverages them to connect consecutive topology snapshots and locate users continuously at the same coordinate system to provide movement traces. Here we select an arbitrary user $a _ { i }$ and set its position at time $t _ { 0 }$ as origin, then all other users’ locations at time $t _ { 0 }$ can be determined. At time $t _ { 1 }$ , we calculate the new position of $a _ { i }$ using its movement vector. We can get different positions of $a _ { i }$ through applying different users’ movement vectors to connect the two topology snapshots. In order to avoid the impact of measurement error in single movement vector, we use the mean value as the new position of $a _ { i }$ . Then the topology can be determined at the same coordinate system as $t _ { 0 }$ . This process iterates until the movement traces of all users are determined.

# 2.4 Design Issues

Three key issues need to be discussed in this approach. First, the order of adding new user into the localized set can impact the overall performance. In this work, we apply a width-first approach to alleviate the accumulating errors. During each iteration, we firstly select all users that have two ranging neighbors in current localized set. After determining the distance vectors for all these users, we add them to update the localized set.

Second, the selected distance vectors can deviate from the real value due to the measurement error, and thus lead to ambiguous locations for a user, for example, user $a _ { m }$ in Fig. 1(b)(2). To address this problem, we introduce an integrated optimization algorithm to achieve a globally consistent result. As the acoustic ranging is relatively accurate, we focus on fine-tuning the orientation of distance vectors, which is formalized as an optimization problem with constraints.

$$
\begin{array}{l} \min \sum_ {i, j = 1, i \neq j} ^ {n} (\delta \theta_ {i, j} ^ {2}), \mathbf {s}. \mathbf {t}. \\ R _ {i j} \left(r _ {i j}, \theta_ {i j} + \delta \theta_ {i, j}\right) + R _ {j k} \left(r _ {j k}, \theta_ {j k} + \delta \theta_ {j, k}\right) \\ = R _ {i k} (r _ {i k}, \theta_ {i k} + \delta \theta_ {i, k}), \forall R _ {i j}, R _ {i k}, R _ {j k} \text {   in   a   ranging   triangle. } \\ \end{array}
$$

Here $R _ { i j } ( r _ { i j } , \theta _ { i j } + \delta \theta _ { i , j } )$ denotes the vector $R _ { i j }$ with magnitude $r _ { i j }$ and direction $\theta _ { i j } + \delta \theta _ { i , j }$ . In the above optimization, $r _ { i j }$ is a known value computed from acoustic ranging, $\theta _ { i j }$ is a known value computed from Eq. (2) in Subsection 2.2. $\delta \theta _ { i , j }$ is a variable to be computed. According to the optimization results, we rotate each distance vector with angle δθ and finally get a consistent localization result.

Third, we consider the situation that the new user only has one ranging neighbor in the localized set. A special scenario for this case is that there are only two users in the network and we want to determine the relative position between them. In the case of single ranging neighbor, we present a multi-stage scheme using the temporal correlation among candidate locations to eliminate ambiguities. Assume that at time $t _ { 1 } ,$ , we get two movement vectors $M _ { i } ( t _ { 0 } , t _ { 1 } )$ and $M _ { j } ( t _ { 0 } , t _ { 1 } )$ of user $a _ { i }$ and $\boldsymbol { a } _ { j } ,$ , we can calculate two possible solutions of $R _ { i j } ( t _ { 0 } )$ . Then at timestamp $t _ { 2 }$ the users report $M _ { i } ( t _ { 1 } , t _ { 2 } )$ and $\dot { M } _ { j } ( t _ { 1 } , t _ { 2 } )$ . We have $\bar { M _ { i } } ( \bar { t _ { 0 } } , t _ { 1 } ) + M _ { i } ( t _ { 1 } , \bar { t _ { 2 } } ) + R _ { i j } ( \bar { t _ { 2 } } ) =$ $M _ { j } ( t _ { 0 } , \mathbf { \dot { t } } _ { 1 } ) + \dot { M } _ { j } ( t _ { 1 } , t _ { 2 } ) + R _ { i j } ( t _ { 0 } )$ .

If we put in the values of movement vectors and two candidate values of $R _ { i j } ( t _ { 0 } )$ , we get two solutions of $R _ { i j } ( t _ { 2 } )$ . As we have the ranging results of $R _ { i j } ( t _ { 2 } )$ , we can distinguish these two solutions and determine the right answer. In most cases, the ranging metric works well and can successfully find the right solution. However, two candidate solutions of $R _ { i j } ( \tilde { t _ { 2 } } )$ ) may have the same length which cannot be distinguished. To address this issue, we wait for some period and use new movement vectors. Then users with at least one ranging neighbor in the localized set can be included and the final localized set contains all users that have at least one ranging path to the initial triangle.

# 3 MULTI-USER RANGING BY CODED AUDIOTONES

The distance vectors among users provide information to determine their locations in translation coordinates. When users are all dynamic, it is difficult to estimate the orientation of a distance vector at the earth coordinate. In our multi-user tracking approach, as presented in the previous section, only the magnitude of the distance vectors are required for multi-user localization and tracking. There are some exiting works dedicating to acoustic signal based accurate ranging between a pair of mobile phones, e.g. the ETOA protocol [17]. But it is still a challenging problem to measure the distances among multiple mobile users. As users walking at a speed about ${ \bar { 2 } } m / s ,$ i.e. a round of multi-user ranging must be completed within a short period to capture the simultaneous locations of multiple users at a high sampling rate. To address this issue, we propose a method using coded audio tones to range multiple users simultaneously.

# 3.1 Acoustic Channel of Mobile Phone

In this subsection, we discuss the characteristic of the acoustic channel of commercial mobile phones. A Frequency Division Multiplexing (FDM) seems a good solution to improve the delay for multi-user ranging, that allows multiple devices transmitting multiple frequencies simultaneously. [2] uses simple audio tones at different frequencies to count the number of users. Fast Fourier Transform (FFT) is applied to find the peaks exceeding an amplitude threshold in the frequency domain. The frequency range used is from 15KHz to 20KHz, and there is a 50Hz gap between two consecutive frequencies, which provides 98 usable frequencies for counting. However, it is not applicable for the scenario when users are mobile, due to the environment noise, device hardware limitation and especially the Doppler Effect.

The supported sample rate of most commercial mobile phones is 44100Hz. Based on Nyquist sampling theory, the detectable frequency range is 0 to 22kHz. The audio signal with frequency below 15kHz is audible to people and the frequency above 20kHz suffers a severe distortion and attenuation, which leaves us a usable frequency range 15kHz to 20kHz. When users are moving, the Doppler shift must be taken into consideration. For example users are walking at a speed $1 . 5 m / s ,$ and the emitted signal is ${ 1 9 } \mathrm { k H z } ,$ at least 350Hz gap between two consecutive frequencies is required to avoid the interference. Thus, there remain very limited usable channels. Besides, a simple audio tone cannot resist environment noises, $e . g .$ the honk of a car.

![](images/90777e8ffced18ca07ba999d1887f2aebc2b9eb113f9b2fe979ad4d099c5df4b.jpg)



Fig. 2. Coding, decoding process of audio tones.

![](images/cd7d9889b3dc4a54f40cb218236b035caf6af32cce641ccdc3880107da4e9177.jpg)



Fig. 4. Relative maximum aperiodic out phase autocorrelation and cross-correlation of three kinds of PN codes, compared to the in phase auto-correlation.

# 3.2 Coded Audio Tones

In our scheme, to separate different users, a set of codes are used to encode the audio tones. A code is a binary sequence $\mathcal { C } = \{ C ( 0 ) , C ( 1 ) , C ( 2 ) , \ldots , C ( N - 1 ) \}$ , with $\dot { N }$ chips $C ( k )$ . These chips can have 2 values -1/1 (polar), $i . e . ^ { \prime } 0 ^ { \prime } / ^ { \prime } 1 ^ { \prime } ( \mathrm { l o g i c a l } )$ . As shown in Fig. 2, each user $a _ { i }$ owns a code $C _ { i }$ of the same length, then modulates a carrier at frequency $\omega _ { c }$ with his/her code. The transmitted audio tone of user $a _ { i }$ is

$$
T ^ {i} (t) = C _ {i} (t) \cdot \cos (\omega_ {c} t). \tag {4}
$$

# 3.2.1 Code Selection

Code selection has a large impact on the performance of multi-user ranging. The coding method of the audio tone should satisfy the following properties:

1) Deterministic: every user is able to independently generates the same code book.   
2) Low correlation: the cross-correlation and out-ofphase auto-correlation must be low enough.   
3) Proper Period: the code must be long enough to discriminate a large number of users, but short enough for small delay.

Definition 1: The aperiodic correlation function $A _ { C _ { i } , \dotsc _ { j } } ( \tau )$ of two sequences {Ci} and $\{ C _ { j } \}$ is:

$$
\left\{ \begin{array}{l l} \sum_ {k = 0} ^ {N - 1 - \tau} C _ {i} (k) \cdot C _ {j} (k + \tau) ^ {*}, & 0 \leq \tau \leq N - 1 \\ \sum_ {k = 0} ^ {N - 1 + \tau} C _ {i} (k - \tau) \cdot C _ {j} (k) ^ {*}, & 1 - N \leq \tau \leq 0 \\ 0, & | \tau | \geq N \end{array} \right.
$$

![](images/8f006d1066a5bae476492456156d90d99fe1e22c9eee7c4eeda7dc1dbe05bec0.jpg)



(a) auto-correlation of 65 63-chip Gold codes.

![](images/30dc7cea8cb5ad1e660d160cd0f9b3249be436352e3bc6e73c8b80fef40b6079.jpg)



(b) auto-correlation of 8 63-chip Kasami codes.

![](images/1affe7ae33a582c81d57f2d47ada2ae83092310845dad22c80de90531373ff1a.jpg)



(c) cross-correlation among 65 63-chip Gold codes.

![](images/005c88fefc322c1b217ad2230ac75265feba552cd72fa14040e550979c08d9c9.jpg)



(d) cross-correlation among 8 63-chip Kasami codes.   
Fig. 3. The aperiodic auto-correlation and cross-correlation properties of 63-chip Gold code and 63-chip Kasami codes of small set.

When Ci is same as $C _ { j } ,$ , we write $A _ { C _ { i } , C _ { i } }$ as $A _ { C _ { i } }$ . When $C _ { i } \neq C _ { j } , A _ { C _ { i } , C _ { j } }$ represents the aperiodic cross-correlation between codes $\{ \stackrel { \bullet } { C } _ { i } \}$ and $\{ C _ { j } \} ;$ and when $C _ { i } \ = \ C _ { j } ,$ $A _ { C _ { i } }$ represents the aperiodic auto-correlation of a code {Ci}. Cross-correlation determines the interference when multiple users emit audio tones concurrently and should be as small as possible. Auto-correlation is the correlation of a code with a time-delayed version of itself, which determines self-interference due to multi-path propagation and should be small for any time delay other than zero. The correlation properties determine not only the level of interference, but also the code acquisition properties.

Since pseudo-noise (PN) codes have good correlation properties in a not well coordinated system, we leverage PN codes to design our multi-user ranging approach. There are three typical PN codes: maximal length sequence (m-sequence), Gold codes and Kasami codes. All these sequences have the maximum possible period $N = 2 ^ { r } - 1$ , where r is the degree of the generator polynomial. M-sequence has optimal autocorrelation property, due to its balance property and shift-and-add property. But the cross-correlation of most pairs of m-sequences tend to be large. Besides there exist very limited number of m-sequences. When $r ~ = ~ 1 0$ , there are only 60 msequences. We need a large number of unique codes to allow a large number of users. When the period of codes $N = 2 ^ { r } - 1$ is determined, the size of Gold codes is $2 ^ { r } + 1$ for r is odd or $r \equiv 2$ mod $4 ;$ the size of a small set of Kasami codes is $2 ^ { \frac { r } { 2 } }$ for r is even; the size of a large set of Kasami codes is $2 ^ { \frac { r } { 2 } } ( 2 ^ { r } + 1 )$ for $r \equiv 2$ mod 4 or $\bar { \boldsymbol { r } } \equiv 0$ mod 4. As shown in Fig. 3, Gold codes and Kasami codes have good aperiodic correlations which are bounded with in a set and much smaller than orthogonal codes. Fig. 4 compares the maximum aperiodic out phase auto-correlation and cross-correlation of Gold codes and Kasami codes. In conclusion, a small-set Kasami codes have the best aperiodic correlation properties, but very small set size; a large-set Kasami codes have large set size but the worst aperiodic correlation properties. Gold codes provide us a tradeoff.

# 3.2.2 Coded Tones Generation

Before the tracking starts, we can detect the background noise of the current environment and select the most clean frequency between 15kHz and 20kHz as $f _ { c } ,$ via simple spectral analysis. Our extensive sampling tests show that, frequency space between 15kHz and 20kHz has less noise even in a very loud environment. Then we have $\omega _ { c } = 2 \pi f _ { c }$ .

Then we need choose the parameter r to generate a set of Gold codes. r determined the period $2 ^ { r } - 1$ of the codes and the size $2 ^ { r } + 1 ~ ( r \not \equiv 0$ mod 4) of the code set. The supported sample rate of most commercial mobile phones is 44100Hz. When each chip is s samples long, the length of the audio tone is $\frac { s } { 4 4 1 0 0 } \ L \ L ^ { 2 } ( 2 \ L ^ { r } - 1 )$ seconds. On one side, the longer the period, the greater the delay; on the other side, tracking n users requires $2 ^ { r } - 1 > n . { \dot { \mathsf { C o n - } } }$ sidering both the delay and user number requirements, a proper r and s can be determined. For example, when $n \bar { = } 2 \bar { 0 }$ , then the selection $r = 5$ and $s = 1 0 0$ will produce 72 ms audio tones.

After the set of Gold codes and the length of a chip are determined, each user $a _ { i }$ is assigned a unique code from the set and generate his/her own tones according to Equation (4). As soon as received a ranging command via a radio channel, each user emits his/her coded tone. For a continuous tracking task with a update interval δt, each user emits his/her coded tone periodically for every δt after the first emission. For different applications, δt varies from tens of milliseconds seconds to tens of seconds.

![](images/738856ed1b085835bf2fc4bac540b945e12f70dea5ea6875d9ef58bd91b06bef.jpg)



(a) Vibration   
![](images/dee8ee358887d97d1274e036684987e9b5c4ee55bbd8c2e50cc7ac310c470764.jpg)



(b) Waggling   
Fig. 5. a) the raw data of acceleration of a walking user; b) the FFT of accelerations along the walking orientation (Y), perpendicular (X) and to the sky (Z).

# 3.2.3 Coded Tones Acquisition

We first introduce our decoding process. As shown in Fig. 2, for an emitted tone $T ^ { i } { \tilde { ( t ) } }$ , the received signal $R \check { ( t ) }$ comprises $T ^ { i } ( t )$ , the interfering tones $I ( t )$ and white noise $n ( t )$ . Then we have: $R ( t ) \stackrel { \smile } { = } T ^ { i } ( t ) \stackrel { \setminus } { + } T ( t ) + n ( t )$ . When the receiver captures a sequence of acoustic signal, he/she uses a narrow frequency bandpass filter to clean most of the background noise and get $T ^ { \prime } ( t )$ . For example, in a walking scenario, the passband could be $[ f _ { c } - \mathrm { \hat { 5 } } 0 0 , f _ { c } + 5 0 0 ]$ .

To recover the code stream, the receiver multiplies $T ^ { \prime } ( t )$ by the reference carrier $\cos ( \omega _ { c } t )$ . Then

$$
\begin{array}{l} T ^ {\prime} (t) \cdot \cos (\omega_ {c} t) \\ = T ^ {i} (t) \cdot \cos (\omega_ {c} t) + (I (t) + n (t)) \cdot \cos (\omega_ {c} t) \\ = 0. 5 C _ {i} (t) + 0. 5 C _ {i} (t) \cdot \cos (2 \omega_ {c} t) + (I (t) + n (t)) \cdot \cos (\omega_ {c} t) \\ \end{array}
$$

After the multiplication, a lowpass filter is used to remove the $\omega _ { c }$ and $2 \omega _ { c }$ component and get $C ^ { \prime } ( t )$ .

If multiple users emit tones simultaneously, $C ^ { \prime } ( t )$ is the sum of all their codes. To acquire the code of user $a _ { i } ,$ a sliding window, whose size is $\frac { s } { 4 4 1 0 0 } ( 2 ^ { r } \textrm { -- } 1 )$ , is used to detect the peak of the correlation between $\dot { C } _ { i } ( t )$ and the $C ^ { \prime } ( t )$ in the window. The correlation is Pearson correlation coefficient of vectors $C ^ { \prime } ( t { + } d )$ and $C _ { i } ( t )$ . When a peak exceeding a threshold is detected, the start sample of the current window will be stamped as the arrival time of $a _ { i } ^ { \prime } \mathbf { s }$ tone.

As the assumption of [17], devices have one mic and one speaker, and can communicate through WiFi or another radio protocol. Then collecting the time line of all participants, the range between each pair of user can be calculated according to ETOA [17].

# 4 MOVEMENT VECTOR DETECTION

In this section, we discuss our scheme for estimating the magnitude and orientation of movement vectors at the earth coordinate system using onboard sensors of commercial smart phones. Compared with existing schemes, our approach achieve higher accuracy without priori knowledge or user inputs. Besides, the distance detection is adaptive for different persons and paces.

Movement vector is the key to connect successive localization snapshots to achieve disambiguated multiuser tracking. There are two major categories of methods for determining the user’s movement vector with a commercial smart phone. One category uses the integration of horizontal acceleration, which is impractical due to the large error caused by double integration of sensor drift and noise. The other category detects the steps of user by pattern recognition and uses the multiplication of step number and average step length to estimate the distance. Those methods require some user measurements and inputs in advance, which can hardly adapt to different users and different paces of the same user. Without the help of GPS, there are no effective accurate methods to detect the moving orientation of a user with the off-theshelf smart phone, e.g., the error spans about $6 0 ^ { \circ }$ in [19].

# 4.1 Understanding the Acceleration

In this work, we use the earth coordinate system as an inertial coordinate system for localization. However, the captured acceleration values are at the coordinate system fixed to the smart phone and here we refer it as a phone coordinate system. Considering a user could hold the phone in any position, we convert the realtime acceleration from the phone coordinate system to the earth coordinate system,i.e. north, east, gravity.

To understand the cause of the error of existing distance and orientation estimation approaches, we analyze the accelerometer data from a commercial smart phone. We observed the following phenomena. Even when the phone is static, there exists huge drifts of acceleration at three orientations, which cause more than 10 cm displacement within 10 seconds by double integration. The drift is much severer when the phone is in a mobile status, exceeding a meter in 10 seconds. As shown in Fig. 5(a), the various springs of acceleration of walking are caused by diverse walking habits of different persons, or changing paces of the same person, or different positions and attitudes of the phone. A very important cause is that the acceleration of walking is not only caused by moving forwards, but also by waggling left and right as well as the vertical movement. Fig. 5(b) presents the spectrum distribution of walking accelerations at three orientations. It shows that there is a great energy from the movement perpendicular to the walking orientation, whose frequency is half of the walking frequency. The perpendicular component could result in great error of the integration and the misunderstanding of the moving orientation.

![](images/032e987d9f762391a0d38786267af680594b81d920f150e5debe93bdd278eb64.jpg)



(a) The raw vertical acceleration and filtered vertical acceleration while user is walking at a normal pace.

![](images/8e139f63020415f73cbd8a34c928a13144366818412b06a6835b80ea4afb5be3.jpg)



(b) The raw vertical acceleration and filtered vertical acceleration while user is walking at a fast pace.   
Fig. 6. The raw vertical acceleration and filtered vertical acceleration when a user walks at different paces.

These observations inspire us to design a method achieving a good movement vector estimation we need first extract the pure acceleration caused by walking from raw acceleration values. In our system, we filter the acceleration using a bandpass filter with a narrow window of the walking frequency,

$$
p b = [ \frac {3 f _ {w}}{4}, \frac {3 f _ {w}}{2} ]. \tag {5}
$$

where $f _ { w }$ is the walking frequency. With a simple step detection, given the sample rate of the accelerometer, the current walking frequency $f _ { w }$ can be determined by counting the sample number of the current step. The filtering eliminates the high-frequency noise from the vibration of the phone and the low-frequency noise from the left and right waggling. Fig. 6 presents example raw vertical acceleration data and filtered acceleration data when the user moves at different paces. As we can see, the filter also removes the large zero-frequency component, i.e. gravity component.

The filtered acceleration works well for movement vector estimation. Fig. 7(a) shows that the walking frequency varies for different people and different paces. It seems that no fixed bandpass filter is suitable for all acceleration data. An adaptive bandpass filter is required. However, to determine the pass band of the filter by detecting the current peak frequency (the walking frequency) through continuously applying FFT to the vertical acceleration could bring heavy computation cost. In our approach, we split the bandpass filtering into two phases to realize adaptive filtering:

In the first phase we combine the step detection and walking frequency detection together. We notice that, usually the walking frequency of people is below 5 Hz. In the vertical orientation, it is mainly the vibrations above 5 Hz causing the spring of the acceleration, which hinders the correct detection of steps. As a result, we apply a low-pass filter whose passband is below 5 Hz to the vertical acceleration first. As shown in Fig. 7(b), although the pace is changing, the low-pass filter removes all the spring of the vertical acceleration well. With the filtered vertical acceleration data, our step detection algorithm is carried out. The algorithm searches for a maximum peak followed by a minimum valley. When the line between the peak and valley crosses the ”zero” point i.e. the overall average of the historical vertical acceleration data, a step is detected. Note that, a threshold is used to prevent noise from fooling the algorithm. In the scenario of daily life, the hit rate of our algorithm exceeds 95% with different people walking at different paces. Then the current walking frequency is obtained by counting the sample number between two successive peaks.

In the second phase, by learning the current walking frequency $f _ { w } ,$ the passband is obtained by Eq. (5). Then a bandpass filter is applied to the raw acceleration data. When a user walks at a steady speed, the filter needs no change. When the change of current walking frequency exceeds a threshold, $\textstyle { \frac { f _ { w } } { 4 } }$ , the filter is updated.

Given a series of accelerations at three orientations, with these two-phase preprocessing, the step detection completes, as well as the pure accelerations of walking is extracted. In the rest work of the movement vector estimation, we only use the adaptively filtered accelerations.

# 4.2 Magnitude of Movement Vector

To estimate the moving distance, we combine dead reckoning and the stride length based approach. The challenges come from the changing stride length of different people at different paces. We propose an adaptive stride length estimation method, which requires no user input and no knowledge from digitalized map. Combining the accurate step detection and the stride length estimation, the moving distance is obtained automatically.

Given one step, our adaptive stride length estimation is based on two principles:

1) As shown in Fig. $\scriptstyle { \mathrm { ~ \bar { 8 } , } }$ the vertical bounce β (i.e., the maximum vertical displacement of user’s hip in one step walking) of a walking person is directly correlated to his/her stride length through an almost equal angle $\phi .$ Here $\phi$ is half of the angle between two legs when both feet touch the floor during walking. When a person walking at a constant pace, the angel is constant. So we can estimate the stride length by 2 cot ϕβ. Here the bounce $\beta$ can be computed from double integration of the vertical acceleration ${ \bf a } \mathrm { ~ - ~ } a v g ,$ where a is current vertical acceleration and avg is the historical average vertical acceleration of this user.

![](images/bf50ffcd73645ee9a04a13f62563d4a7f30479d257a4e6eaaf3d50aed1ba6ab3.jpg)



(a) The spectrum of vertical accelerations

![](images/53dde8f752bb9e7ff868f2b7207a72dc256e25b1b49ab59e9daad033096acf79.jpg)



(b) Filtered by a low pass filter with pass band $\leq 5 H z$

Fig. 7. Preprocessing of vertical accelerations of different users at different paces.   
![](images/f055b1481206a6460355820a74ec7f761ddd46fed67daeabb947064a3b57c311.jpg)



Fig. 8. Movement vector and walk model.

2) For the same person at greater paces, the angle increases. From Fig. $^ { 6 , }$ we notice that when the pace increases, the ratio $\frac { m a x - m i n } { a v g - m i n }$ of the acceleration raw data increases with the stride length. Here max and min is the historical maximum and minimum acceleration data of this user. The spring pattern of the raw acceleration also changes the ratio, as presented in Fig. 6(a), which reflects the difference of different person’s step.

Assume that there are T acceleration samples $\{ { \bf { a } } _ { 1 } , { \bf { a } } _ { 2 } , \cdots , { \bf { a } } _ { T } \}$ within a step. Combining these two principles, we adaptively estimate the moving distance d as $\begin{array} { r } { d \ = \ k \sqrt { \frac { m a x - m i n } { a v g - m i n } \sum _ { j = 1 } ^ { T } \sum _ { t = 1 } ^ { j } ( { \bf a } _ { t } - a v g ) } } \end{array}$ . Here the parameter k is a constant for the same person. In our approach, an initial value of k is given according to the average value of people. Then, according to the online localization with the ranging result, k is calibrated for the first several rounds and fixed for each user respectively.

# 4.3 Orientation of Movement Vector

We use the filtered horizontal accelerations along the east and north axes at the earth coordinate system, as shown in Fig. 9(a), to estimate the orientation of each step. The steps are detected based on the vertical acceleration as we mentioned before. Assume that there are T acceleration samples within a step, the horizontal accelerations within a step are $\mathbf { a } ^ { H } = \{ \mathbf { \dot { a } } _ { 1 } ^ { H } , \mathbf { a } _ { 2 } ^ { H } , \cdot \cdot \cdot , \mathbf { a } _ { T } ^ { H } \}$ , each $\mathbf { a } _ { i } ^ { H } = \sqrt { \mathbf { a } _ { i } ^ { E ^ { 2 } } + \mathbf { a } _ { i } ^ { N ^ { 2 } } }$ ai E2 aNi 2. Here aEi is the east component of $\mathbf { a } _ { i } ^ { E }$ the i-th acceleration sample, and $\mathbf { a } _ { i } ^ { N }$ is the corresponding north component. The maximum horizontal acceleration max $\tau \{ \mathbf { a } _ { 1 } ^ { H } , \mathbf { a } _ { 2 } ^ { \dagger } , \cdots , \mathbf { a } _ { T } ^ { H } \}$ , is detected for each step, let its index be κ. The orientation of $\mathbf { a } _ { \kappa } ^ { H }$ is closest to the moving orientation of this step. As presented in Fig. 9(c), the ratio of $\mathbf { a } _ { \kappa } ^ { E }$ and $\mathbf { a } _ { \kappa } ^ { N }$ is the tangent of the angle between north and the step orientation. As mentioned in [19], even knowing the moving orientation by arctan $\left( \mathfrak { a } _ { \kappa } ^ { E } / \mathfrak { a } _ { \kappa } ^ { N } \right)$ , it is still difficult to determine the forward and backward orientation. To address this issue we notice that the forward acceleration companies the rising edge of the vertical acceleration, as illustrated in Fig. 9(a). With our approach, the orientation of each step can be determined within 20◦ error range. And the orientations of successive steps zigzag around the walking orientations, e.g. Fig. 9(c). So, a Kalman filter can be applied to get the moving orientation of several steps.

# 5 ANALYSIS AND EVALUATION

We implement Montage on Android phones and examine the performance with extensive experiments in this section.

# 5.1 Coded Tone Based Ranging

For the coded tone based multi-user ranging, the delay mainly consists of three parts: the time for tone emission, the time for tone transmission, and the time of coded tone acquisition. The transmission time is decided by the distance, which is usually tens of milliseconds for indoor application. The emission time is determined by the the length of the audio tone, which is $\frac { s } { 4 4 1 0 0 } ( 2 ^ { r } - \dot { 1 } )$ . In the experiments, we select the set of Gold codes with $r = 7$ as the codebook, 19 kHz as the carrier frequency, and the chip length is 40 samples. As a result, the length of a coded tone is 115 ms, so is the sliding detection window. The step of the sliding window is 4 samples. We test the ranging performance with 4 users. Each user selects a unique code from the set. To exam the interferenceresistance property, we design the experiment that will result in larger interference by dividing 4 users into two groups and changing the distance between groups. All users emit their tones as soon as they received a start signal through Wi-Fi. The arrival time of each coded tone is detected by sliding its code to locate the maximum correlation peak. Fig. 10(a) shows the coded tone acquisition result by one of the users in a round of ranging. And Fig. 10(b) presents the ranging results in the hall of an office building. And the delay is less than 200 ms. The result shows that, our coded tone based ranging method achieves sub-meter accuracy when users are about 10 meters apart.

![](images/a749cff6366cc4e8b8bace2bcfb9c2e6c01f1963f3edd727d497a9465c4c119d.jpg)



(a) The acceleration at three orientations after filtering.

![](images/89d4ef1f8b7ad04d58a819b967370be5b9bc082768559a5ccf0affecc595ef4e.jpg)



(b) The orientation of the acceleration using the filtered acceleration. The true walking orientation is $4 5 ^ { \circ }$ north by east.

![](images/f6433e40889cd96e4a90f37de52d02537053bacb90c0904314d9e37c980aa5a2.jpg)



(c) The estimated walking orientation using the peak acceleration of each step. The true orientation is $4 5 ^ { \circ }$ north by east.

Fig. 9. Determine the real-time walking direction.   
![](images/dce1e65698ce265a2697d3b7b6505a0ce98a1841ee73b273feb1b539aa3ee090.jpg)



(a) Tone acquisition of 4 users in a round of ranging.

![](images/02781773c2d8f6246e94afe85047d29e691fa9f9b8c68399f54bccfc700f427b.jpg)



(b) Ranging error when there are 4 users.   
Fig. 10. Coded tone based 4 users ranging.

# 5.2 Movement Vector Determination

We test the accuracy of our stride length estimation method adaptive for different phone placements, different paces and different persons. First, we consider the case that a user holds the phone arbitrarily. As shown in Fig. 11 the patterns of acceleration vary when the placement of the phone changes, which increase the difficulty of getting accurate stride length. We then examine the impact of phone placement on the accuracy of stride length estimations. In the experiments, two persons(a male and a female), walk while the phones are hold in hand, placed in the chest pockets and pants pockets. Fig. 11(d) shows that the mean error of each stride estimated by Montage doesn’t exceed 4 cm for all three placements.

For the same person, we also test the stride length estimation for changing paces. In this experiment, a user walks from slow to fast for 20 steps (with stride length increases). Fig. 12(a) illustrates that the real-time estimated stride length adapts the changing paces, and the accumulated error is only 0.2m. Then we examine the stride length estimation accuracy for different persons. 15 participants in the experiments, including 4 female and 11 male persons. Their heights vary from 1.56m to 1.82m and their average stride lengths vary from 53cm to 83cm. Each participant carries the phone arbitrarily and walks at arbitrary paces. Fig. 12(b) shows the average error of the the estimated stride length for each person. The maximum error is 9cm, and the mean error is 4cm.

We also examine the accuracy of the forward orientation estimation. Fig. 12(c) shows the error of the estimated orientations while the walking orientation changes from −180◦ to 180◦. The mean error of detected orientation by our methods is ±10◦, with 90% errors are within ±20◦, which greatly outperforms the existing orientation estimation work.

# 5.3 Single User Tracking

With the real-time magnitude and orientation estimated by our approach, a single user’s trace can be tracked by a series of movement vectors. First, we conduct an experiment to compare the indoor and outdoor tracking performance. A user first walks freely in an outdoor garden for 125m and then walks along a similar shape trace in our office, which is 76m. She repeats both traces 10 times. Fig. 13(a) and Fig. 13(b) show the average outdoor and indoor tracking results compared with the ground truth, respectively. For the outdoor tracking, the greatest deviation to the ground truth is only about 1.6m, and the mean deviation is only about 0.36m. For the indoor tracking, the largest deviation of is about 2m and the mean deviation is about 0.96m. The result shows that due to the electromagnetic interference in the office, the tracking deviation is greater than that of outdoor.

![](images/f43a879bc0449e18fd3040f215c49f3b1e3a994dc4027c27cbac33381550792c.jpg)



(a) The vertical acceleration when phone is held by hand.

![](images/42513a4969290e46b157f7679636e85073066f45947b57d39868fbe3f9cbae70.jpg)



(b) The vertical acceleration when phone is in lapel pocket.

![](images/691ebb2a52992dfa95535e07fbd8935f1d512381625ecf81261b671c2d4d8051.jpg)



(c) The vertical acceleration when phone is in pants pocket.

![](images/d9912f2dd0edfaf54ffc2fa3185b1c18233e4ccc580c8bf17b57c15bab810df1.jpg)



(d) Average error of stride length detection when the phone at different positions.

Fig. 11. Detection stride length when the phone is at different positions.   
![](images/95027bbd4d20e1a5c3ef9993e107999cf75ff6eb83291209ef08107332c46afa.jpg)



(a) Estimated stride length changes with paces.

![](images/be3c1bbe544d54c0afa3bdfd7df17aba021410984e173672ff82373ba9f2ce96.jpg)



(b) The average error of estimated stride length of 15 users walking free.

![](images/2ced1f87b8a2ec457bc7491043dd3f707a4d72d56a296f9e3dec06170bde4250.jpg)



(c) Error range of estimated orientation when a user is walking.

Fig. 12. Estimation of movement vector.   
![](images/23d1d8551c9e371068462497b0d41e4c99128fd07d8ca069e16e09b9c8edd203.jpg)



(a) Outdoor single user tracking result.

![](images/48f8289effc49eb743bf4dbf9d77b0d83f2a5239aaa1fa7515497b32f1ab34e5.jpg)



(b) Indoor single user tracking result.   
Fig. 13. Compare between outdoor and indoor single user’s tracking result by movement vectors.

To get robust evaluation results of movement-vectorbased single user tracking, we have 15 volunteers (4 female and 11 male) installed Montage in their smart phones to collect traces. Since there is no GPS signal indoor, to get the ground truth we mark the 25 optional traces with diverse lengths, directions and shapes on the floor of our office, which is 1600 square meters. Volunteers can walk along any combinations of these traces with free paces and arbitrary phone positions. 847 traces from 15 volunteers are collected. For every step, there is a tracking location, about 32,000 locations in total. We analyze the deviation of each tracking location, and Fig. 14(a) presents the CDF of deviation. The result shows that, the mean deviation is about 0.87 meter, with 90% tacking location have a deviation less than 2 meters. We also explore the deviation change with the distance to the start point, Fig. 14(b) shows that within the initial 20 steps (about 16 meters), the deviation won’t exceed 0.5

![](images/30736524b9a13e2bfbd6581a56b34615e8d5ba95923a53b1f9d27dfd04fdc337.jpg)



(a) CDF of the deviation of 847 indoor traces.   
![](images/7ef5d90a6907d7e73345f04784141737ff151972590d94639bd56474ddbf277c.jpg)



(b) Mean deviation according to the steps from the start points.   
Fig. 14. Single users’s tracking result by movement vectors.

meter. The deviation increases with the distance to start point and won’t exceed 2 meters for 90% time within 140 steps (about 110 meters). But we notice that, a small portion of large deviations (about 3 meters) occur around 60 steps, and we consider the reason as the scale of our office makes most turns happen between 50 and 70 steps.

Both the outdoor tracking result and extensive indoor tracking results show that, with only inertial sensors of an off-the-shelf mobile phone, our method can achieve a highly accurate tracking result of walking people. To compare with the state-of-art methods in [1], which achieve a tracking error of 6.9%, Montage achieves a tracking error of about 2.5%.

# 5.4 Multi-user Tracking

Combing movement vectors and ranging results, we can track the team formation and movement of multiple users. In our experiments, 4 users walk randomly in a the 1600 square meter office. Their movement vectors are detected in real time and distances between every pair of users are calculated periodically. Each time their ranges are obtained, our localization approach introduced in Section 2 is applied to calculate their locations at a translation coordinate, which takes the initial location of a randomly chosen user as the origin, and calibrate the estimated movement vectors accordingly. Fig. 15 illustrates a fragment of 4 users’ team formation tracking. As shown in Fig. 15(a), with estimated movement vectors, the traces of each user can be obtained. However, without anchor nodes we cannot know the team formation of 4 users. Combing the ranging results and the movement vectors, the locations of 4 users are determined. Fig. 15(b) presents the detected team formation with three rounds of ranging results. When the No.4 user knows the location of his start point (the entrance of the office), the other three users’ absolute locations are determined as illustrated on the floor plan, which matches the ground truth surprisedly well. In our experiments, in which each user walked for about 1000m in the office, the mean deviation of the estimated trace to the ground truth is about 0.5m and the largest deviation is about 1m. With the help of ranging, Montage enables formation detection and improves tracking accuracy. With only one anchor position, Montage enables accurate indoor localization for multiple users.

# 6 RELATED WORK

One popular line of mobile handset indoor localization is fingerprinting. Some systems exploit fingerprints of wireless signals to achieve room-level user localization and tracking, e.g., [6], [22], [31]. [22] presents a GSM indoor localization system that achieves a median accuracy of 4 m. Horus [31] designs a WLAN localization system with a meter-level accuracy. EZ [6] uses the RSSI to indoor APs and yields a median accuracy of 2-7 m with no pre-deployment effort. Ficco et al. [8] propose to optimize the positioning accuracy by selecting the best deployment schema of the wireless access points. There are other types of fingerprints or landmarks used to achieve room-level localization, e.g., [13], [21], [35]. Batphone [21] uses an ambient sound fingerprint called the Acoustic Background Spectrum (ABS), and GROP-ING [35] uses Geo-magnetism as fingerprint. Luxapose [13] encodes location identifiers in visible light and a camera-equipped smartphone can determine its location and orientation relative to the luminaires. PerLoc [7] uses visual feature points to localize mobile users. Most fingerprinting based localization methods cost an effort for site-survey. Some recent systems have incorporated survey by users,e.g. [24], [25], [28]. But they still face the problem that different locations may have similar fingerprints. There are also some works using wireless signal to localize people in a dynamic way, e.g., [26] and C2IL [33]. But it is difficult to track multiple persons simultaneously.

Some schemes perform localization by estimating distances to anchor nodes based on RSSI, time-of-arrival (TOA), time-difference-of-arrival (TDOA) and angle-ofarrival AoA. Peng et al. [17] proposed ETOA with centimeter-level accuracy acoustic-based pair-wise ranging method. ETOA avoids many sources of inaccuracy found in other typical TOA schemes, such as clock synchronization, non-real-time handling, software delays, etc. [18] presents a solution for achieving high speed 3D continuous pair-wise localization using two microphones, one speaker, accelerometer and digital compass on the phone. Liu et al. [14] use acoustic ranging estimates among peer phones as constraints to reduce the significant errors of WiFi-based method. Centaur [15] fuses RF and acoustic ranging based localization techniques into a single systematic framework based on Bayesian inference. [10] and [34] leverage Doppler Effect of acoustic signal to achieve centimeter-level accuracy. Most of the acoustic based ranging approaches are designed for a pair of users. Some work [17] uses a TDMA scheme for multi-users ranging, that results long delay and lack of identification when tracking multiple users. [2] proposes a FDMA based solution to estimate the number of mobile devices present in an area, however when users are moving, the FDMA methods may fail due to the Doppler effect. Many work, like [16] and [4] , propose CDMA based systems using a high frequency acoustic signal and a hydrophone array to enable simultaneous sub-meter tracking of multiple targets. These methods require synchronization or hydrophone array which is quite difficult to implemented on the off-theshelf mobile phones. Besides, anchor nodes are necessary for positioning too.

Several inertial navigation approaches [3] are proposed to tracking the move trace of a user. [9] and [11] provide good survey of inertial positioning systems for pedestrians. Most of them use step-and-heading-based deadreckoning [20], [30], with special devices and absolute position fixes are required to correct dead-reckoning output. Some work use the inertial sensors of smartphones with indoor maps to track users as they traverse indoor, e.g., [5], [19]. But it requires a map showing the pathways and barriers and the orientation estimation is quite inaccurate. [1] provides single pedestrian tracking using mobile phones to achieve a tracking error of 6.9%. Travi-Navi [36] packs both vision features and a rich set of sensor readings into the navigation path. Most of the exiting indoor tracking methods need a pre-knowledge or at least three anchors, and are infeasible to provide the realtime multi-user formation.

![](images/f3fb570f04f5a553879ef20488bafc2aea858aeeb270ffd59c17e9c81c8da6ab.jpg)



(a) Fragments of 4 users’ movement vectors.

![](images/4b9231c5bd2447d0abfeeb89d3e8310bc62b5d61d7b35591343f403d4a55036c.jpg)  
(b) A fragment of indoor tracking results of 4 users.   
Fig. 15. A fragment of four users’s tracking result.

# 7 CONCLUSION

In this paper, we proposed Montage for realtime multiuser team formation tracking with no anchor node and provide multi-user localization with merely one anchor node. We designed coded acoustic tones for supporting tracking of multi-users with small latency and designed innovative techniques to accurately estimate the moving distance and directions with off-the-shelf smartphones. No pre-setting or pre-knowledge is required by Montage. Our extensive evaluations (847 traces from 15 users) showed that Montage achieved meter-second-level accuracy. A future work is to investigate whether Doppler effects will result in better performance for multi-user tracking. as we can estimate the relative distance and direction between two users using Doppler effects caused by mobility.

# 8 ACKNOWLEDGMENT

The research is supported in part by NSF China under Grants No. 61572281, No. 61472218, and China Postdoctoral Science Foundation under Grant No. 2015M580101. The research of Li is partially supported by NSF ECCS-1247944, NSF ECCS-1343306, NSF CMMI 1436786, NSF CNS 1526638, NSF China under Grant No. 61520106007. This work is partially supported by NSF China under Grants No 61472382, No. 61272487, No. 61232018, No. 61471217, the High-Tech R&D (863 C China Cloud) Program of China under grant 2015AA01A201, and CCF-Tencent Open Fund under grant IAGR20150101.

# REFERENCES

[1] ALZANTOT, MOUSTAFA AND YOUSSEF, MOUSTAFA. UPTIME: Ubiquitous pedestrian tracking using mobile phones. In IEEE WCNC (2012).   
[2] ANANDA, A. L., AND PEH, L.-S. Low cost crowd counting using audio tones. In ACM Sensys (2012).   
[3] BHATTACHARYA, S., BLUNCK, H., KJÆRGAARD, M. B., AND NURMI, P. Robust and energy-efficient trajectory tracking for mobile devices. IEEE TMC 14, 2 (2015), pp. 430-443.   
[4] COOKE, S.J., NIEZGODA, G.H., HANSON, K.C., SUSKI, C.D., PHELAN, F.J.S., TINLINE, R., AND PHILIPP, D.P. Use of CDMA acoustic telemetry to document 3-D positions of fish: relevance to the design and monitoring of aquatic protected areas. Marine Technology Society Journal 39, 1 (2005), pp. 31-41.   
[5] CHENG, B., LI, X.-Y., JUNG, T., MAO, X., TAO, Y. AND YAO, L. SmartLoc: Push the Limit of the Inertial Sensor Based Metropolitan Localization Using Smartphone. In ACM MobiCom Poster (2013).

[6] CHINTALAPUDI, K., PADMANABHA IYER, A., AND PADMANAB-HAN, V. Indoor localization without the pain. In ACM MobiCom (2010).   
[7] FENG, P., ZHANG, L., LIU, K., AND LIU, Y. PerLoc: Enabling Infrastructure-Free Indoor Localization with Perspective Projection. In IEEE MASS (2015).   
[8] FICCO, M., ESPOSITO, C., AND NAPOLITANO, A. Calibrating indoor positioning systems with low efforts. IEEE TMC 13, 4 (2014), pp. 737-751.   
[9] HARLE, ROBERT. A survey of indoor inertial positioning systems for pedestrians. IEEE Communications Surveys & Tutorials, (2013).   
[10] HUANG, W., XIONG, Y., LI, X.-Y., LIN, H., MAO, X., YANG, P., LIU, Y., AND WANG, X. Swadloon: Direction Finding and Indoor Localization Using Acoustic Signal by Shaking Smartphones. IEEE TMC 14,10 (2014), pp. 2145-2157.   
[11] JAHN, J., BATZER, U., SEITZ, J., PATINO-STUDENCKA, L. AND GUTIERREZ´ BORONAT, J. Comparison and evaluation of acceleration based step length estimators for handheld devices. IEEE IPIN,(2010).   
[12] JIN, Y., SOH, W., AND WONG, W. An indoor localization mechanism using active RFID tag. IEEE SUTC, (2006).   
[13] KUO, Y.-S., PANNUTO, P., HSIAO, K.-J., AND DUTTA, P. Luxapose: Indoor positioning with mobile phones and visible light. In ACM MobiCom (2014).   
[14] LIU, H., YANG, J., SIDHOM, S., WANG, Y., CHEN, Y., AND YE, F. Accurate WiFi based localization for smartphones using peer assistance. IEEE TMC 13, 10 (2014), pp. 2199-2214.   
[15] NANDAKUMAR, R., CHINTALAPUDI, K. K., AND PADMANAB-HAN, V. N. Centaur: locating devices in an office environment. In ACM MobiCom (2012).   
[16] NIEZGODA, G., BENFIELD, M., SISAK, M., AND ANSON, P. Tracking acoustic transmitters by code division multiple access (cdma)- based telemetry. Hydrobiologia 483, 1 (2002), pp. 275–286.   
[17] PENG, C., SHEN, G., ZHANG, Y., LI, Y., AND TAN, K. Beepbeep: a high accuracy acoustic ranging system using cots mobile devices. In ACM Sensys (2007).   
[18] QIU, J., CHU, D., MENG, X., AND MOSCIBRODA, T. On the feasibility of real-time phone-to-phone 3d localization. In ACM SenSys (2011).   
[19] RAI, A., CHINTALAPUDI, K. K., PADMANABHAN, V. N., AND SEN, R. Zee: Zero-effort crowdsourcing for indoor localization. In ACM MobiCom (2012).   
[20] ROBERTSON, P., ANGERMANN, M., AND KRACH, B. Simultaneous localization and mapping for pedestrians using only footmounted inertial sensors. In ACM UbiCom (2009).   
[21] TARZIA, S., DINDA, P., DICK, R., AND MEMIK, G. Indoor localization without infrastructure using the acoustic background spectrum. In ACM MobiSys (2011).   
[22] VARSHAVSKY, A., DE LARA, E., HIGHTOWER, J., LAMARCA, A., AND OTSASON, V. Gsm indoor localization. Pervasive and Mobile Computing 3, 6 (2007), pp. 698–720.

[23] VITERBI, ANDREW J AND OTHERS CDMA: principles of spread spectrum communication. Addison-Wesley Reading, (1992).   
[24] WU, C., YANG, Z., LIU, Y. AND XI, W. WILL: Wireless indoor localization without site survey. IEEE TPDS, 24 (2013), pp. 839- 848.   
[25] WU, C., YANG, Z., AND LIU, Y. Smartphones based crowdsourcing for indoor localization. IEEE TMC 14, 2 (2015), pp. 444-457.   
[26] XI, W., ZHAO, J., LI, X.-Y., ZAHO, K., TANG, S., AND LIU, X. AND JIANG, Z. Electronic Frog Eye: Counting Crowd Using WiFi. IEEE INFOCOM, (2014).   
[27] YANG, Z., LIU, Y., AND LI, X.-Y. Beyond trilateration: On the localizability of wireless ad hoc networks. IEEE/ACM TON 18, 6 (2010).   
[28] YANG, Z., WU, C., AND LIU, Y. Locating in fingerprint space: wireless indoor localization with little human intervention. In ACM MobiCom (2012).   
[29] YANG, L., CHEN, Y., LI, X.-Y., XIAO, C., LI, M., AND LIU, Y. Tagoram: Real-time tracking of mobile RFID tags to high precision using COTS devices. In ACM MobiCom (2014).   
[30] YANG, Z., FENG, X., AND ZHANG, Q. Adometer: Push the limit of pedestrian indoor localization through cooperation. In IEEE TMC 13 11 (2014), pp. 2473-2483.   
[31] YOUSSEF, M., AND AGRAWALA, A. The horus location determination system. Wireless Networks 14, 3 (2008).   
[32] ZHAO, J., XI, W., HE, Y., LIU, Y., LI, X.-Y., MO, L., AND YANG, Z. Localization of Wireless Sensor Networks in the Wild: Pursuit of Ranging Quality. IEEE/ACM Netw 21, 1 (2013).   
[33] ZHAO, J., JIANG, Z., LI, X.-Y., TANG, S., HAN, J., XI, W., ZHAO, K., WANG, Z., AND XIAO, B. Communicating Is Crowdsourcing: Wi-Fi Indoor Localization with CSI-based Speed Estimation. JCST 29, 4 (2014), pp. 589-604.   
[34] ZHANG, L., LI, X.-Y., HUANG, W., LIU, K., ZONG, S., FENG, P., JUNG, T., AND LIU, Y. It Starts with iGaze: Visual Attention Driven Networking with Smart Glasses. In ACM MobiCom (2014).   
[35] ZHANG, C., SUBBU, K. P., LUO, J., AND WU, J. GROPING: Geomagnetism and cROwdsensing Powered Indoor NaviGation. In IEEE TMC 14 2 (2015), pp. 387-400.   
[36] ZHENG, Y., SHEN, G., LI, L., ZHAO, C., LI, M. AND ZHAO, F. Travi-navi: Self-deployable indoor navigation system. In ACM MobiCom (2014).

![](images/92972fbd18641e21d2fed9efeeb417f8f3560ef0e91d0f8619e4ef9f5d698bcf.jpg)



Lan Zhang received her Bachelor degree (2007) in School of Software at Tsinghua University, China, and her Ph.D. degree (2014) in the department of Computer Science and Technology, Tsinghua University, China. She is currently a distinguished researcher at the School of Computer Science and Technology, at University of Science and Technology of China. Her research interests span privacy protection, secure multiparty computation and mobile computing, etc.

![](images/553bcedbcffd0b167b30b22204b1fbdb2deffb517e36a4a3032214576b01e3cf.jpg)



Kebin Liu received his BS degree in Department of Computer Science from Tongji University in 2004, and MS and Ph.D. degrees in Shanghai Jiaotong University, in 2007 and 2010. He is currently an assistant researcher in the School of Software and TNLIST, Tsinghua University. His research interests include WSNs and distributed systems.

![](images/dafa397d565a7113fe5faad532920f966f129fadec3a281f775e75f04294f972.jpg)



Yonghang Jiang received the BS degree from college of software engineering, Southeast University, China, in 2011 and ME degree from school of software, Tsinghua University, China, in 2014. He is currently working toward the PhD degree in the Department of Computer Science, City University of Hong Kong. His research interests include mobile computing and wearable computing.

![](images/e524b119826c3faa3ff1136c71c5c88f9ac3cd8b199f0c8a706ef3633eaf3656.jpg)



Xiang-Yang Li (F2015, SM2008) is a professor and executive dean at the School of Computer Science and Technology, at University of Science and Technology of China, and was a professor at Illinois Institute of Technology. He is an IEEE Fellow (2015), ACM Distinguished Scientist (2015), and holds EMC-Endowed Visiting Chair Professorship at Tsinghua University from 2014 to 2016. He is a recipient of China NSF Outstanding Overseas Young Researcher (B). Dr. Li received MS (2000) and PhD (2001) degree at

Department of Computer Science from University of Illinois at Urbana-Champaign, a Bachelor degree at Department of Computer Science and a Bachelor degree at Department of Business Management from Tsinghua University, P.R. China, both in 1995. His research interests include wireless networking, mobile computing, security and privacy, cyber physical systems, and algorithms.

![](images/a65e0ea54cbf2e2236285daf1f0bb9521007d4c07fa135dce29173e888fce243.jpg)



Yunhao Liu received his BS degree in Automation Department from Tsinghua University, and an MA degree in Beijing Foreign Studies University, China. He received an MS and a Ph.D. degree in Computer Science and Engineering at Michigan State University, USA. Being ACM Fellow and IEEE Fellow, Yunhao is now ChangJiang Professor at Tsinghua University. His research interests include Sensor Network and IoT, Localization, RFID, Distributed Systems and Cloud Computing.

![](images/962ea42783c46a1fc15dd6a90e619eb080dafaa97a4d05c8f69a3b701e34bdf4.jpg)



SIGMOBILE Society.

Panlong Yang (M’02) received his B.S. degree, M.S. degree, and Ph.D. degree in communication and information system from Nanjing Institute of Communication Engineering, China, in 1999, 2002, and 2005 respectively. Dr. Yang is now a professor in the School of Computer Science and Technology, University of Science and Technology of China. His research interests include wireless mesh networks, wireless sensor networks and cognitive radio networks. He is a member of the IEEE Computer Society and ACM

![](images/31f1f076f1f00d555d768bbbd8c7f82cd755aeb32fc186a7f0cc258fda341b54.jpg)



Zhenhua Li is an assistant professor at the School of Software, Tsinghua University. He received the B.Sc. and M.Sc. degrees from Nanjing University in 2005 and 2008, and the Ph.D. degree from Peking University in 2013, all in computer science and technology. His research areas mainly consist of mobile Internet, cloud computing/storage, and content distribution.