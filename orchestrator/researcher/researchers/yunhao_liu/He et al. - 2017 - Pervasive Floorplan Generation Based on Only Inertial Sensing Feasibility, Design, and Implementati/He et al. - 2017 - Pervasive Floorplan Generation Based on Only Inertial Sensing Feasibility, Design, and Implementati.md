# Pervasive Floorplan Generation Based on Only Inertial Sensing: Feasibility, Design, and Implementation

Yuan He, Member, IEEE, Jiaqi Liang, and Yunhao Liu, Fellow, IEEE, ACM

Abstract—Mobile crowdsourcing is deemed as a powerful technique to solve traditional problems. But the crowdsourced data from smartphones are generally with low quality, which induce crucial challenges and hurt the applicability of crowdsourcing applications. This paper presents our study to address such challenges in a concrete application, namely floorplan generation. Existing proposals mostly rely on infrastructural references or accurate data sources, which are restricted in terms of applicability and pervasiveness. Our proposal called SenseWit is motivated by the observation that people's behavior offers meaningful clues for location inference. The noise, ambiguity, and behavior diversity contained in the crowdsourced data, however, mean non-trivial challenges in generating high-quality floorplans. We propose 1) a novel concept called Nail to identify featured locations in indoor space and 2) a heuristic pathlet bundling algorithm to progressively discover the internal layouts of a floorplan. We implement SenseWit and conduct real-world experiments in different spaces to demonstrate its efficacy. Our work offers an efficient technique to obtain high-quality structures (either logical or physical) from low-quality data. We believe it can be generalized to other crowdsourcing applications.

Index Terms—Mobile Crowdsourcing, Floorplan Generation, Inertial Sensing.

# I. INTRODUCTION

CROWDSOURCING is currently a hot topic in the research community. Relying on appropriate division of work and collaboration among participants, it offers a new way to efficiently accomplish many jobs that are previously considered to be cost-intensive.

With rapid development of MEMS and mobile communications, smartphones are empowered with capacities of sensing, computing, and communications. Utilizing smartphones for crowdsourcing, i.e. mobile crowdsourcing, becomes a promising direction. There are many proposals of mobile crowdsourcing, such as traffic management $[1]$ , localization $[2]$ $[3]$ , map generation $[4]$ , floorplan generation $[5]$ $[6]$ , etc..

Most smartphones have equipped with inertial sensors (e.g., accelerometer, gyroscope). These sensors can finish the same task consuming less energy and user concern. To utilize data

Manuscript received on 09-06-2016, revised on 01-12-2017.

This research is supported in part by the National Natural Science Fund for Excellent Young Scientist under grant No. 61422207 and the National Natural Science Foundation of China under Grant No. 61373146.

Yuan He and Yunhao Liu are with the School of Software and Tsinghua National Lab for Information Science and Technology, Tsinghua University, China, 100084. TEL: 86-10-62797784. FAX:86-10-62773281. Email: {heyuan, yunhao}@tsinghua.edu.cn. Jiaqi Liang is with the IT Department, China Merchants Bank, Shanghai, China, 201201. TEL: 86-18521352699. Email: lmumu77@163.com. Yuan He is the directing correspondence.

from smartphones, however, is a non-trivial task. The main challenge is low quality of data. Generally, the data quality may be interpreted in three levels: 1) accuracy and precision of measurements; 2) quantity and density of data, with respect to the application requirement; 3) fidelity and consistency of results, contrasted to the ground truth.

This paper presents our study to address the above challenges in a concrete application called floorplan generation. A floorplan is a diagram of the room layouts in one floor of a building. With the popularity of LBS, floorplans are in great demand. But they are not available in many contexts, due to commercial or security-related reasons. Floorplan generation via mobile crowdsourcing thus becomes a desirable technique.

Floorplan generation is partially similar to the problem of map generation $[4]$ $[7]$ . Given the ability of localization, the common idea behind map generation is to connect discrete points into curves. Since indoor localization is a non-trivial issue, existing proposals mostly rely on infrastructural references or accurate data sources. For example, $[8]$ collects measurements of signal strength to a couple of WiFi APs. $[9]$ requires to mount inertial sensors on user bodies for precise sensing. Note that for people in a venue where the floorplan is unknown, it is very likely that the abovementioned references/data sources are unavailable. How to generate floorplans under such scenarios remains an open problem.

Our idea is motivated by the observation that people's behavior offers meaningful clues for location inference. From a statistical point of view, people make turns at corners and stay stationary for a short in particular positions like water dispenser. Locations corresponding to those behavioral features may be labeled, called $featured \ locations$ . Using only inertial sensing to identify people's behavior, one can crowdsource plenty of movement pathlets through $featured \ locations$ . Intuitively, if one bundles those labeled pathlets together, a complete floorplan can be generated progressively.

Towards this goal, we need to address several critical challenges: First, the noise in inertial sensing, caused by either hardware diversity or motion instability, often blurs the features of behavior data; Second, diversity of people's behavior often causes false identifications of featured locations; Third, a featured location, even correctly identified, sometimes may correspond to multiple locations in the space, as is called ambiguity of labels.

Our work — SenseWit, is an efficient technique to generate indoor floorplans while coping with the above challenges. Our contributions can be summarized as follows.

(1) Based on real-world experiments and observation, we show both opportunities and challenges in utilizing low-quality inertial sensing data. We propose the concept of Nail to identify featured locations.   
(2) We design an efficient pathlet bundling algorithm to generate floorplan with pathlets. It is robust to noise, ambiguity, and diversity of people's behavior.   
(3) We implement SenseWit and evaluate its performance through real-world experiments. The result demonstrates that SenseWit generates accurate floorplans even with limited amount of data, while the cost is relatively low.

The rest of this paper is organized as follows. In Section II we discuss the related work. Section III elaborates on the system design and detailed solutions. Section IV shows the implementation and evaluation results. In Section V, we conclude this paper.

# II. RELATED WORK

# A. Mobile Crowdsourcing

Mobile crowdsourcing has been used in traffic management $[10]$ $[11]$ , environment protection $[12]$ , localization $[13]$ , etc.. PiLoc $[14]$ designs an indoor localization system utilizing opportunistically sensed data contributed by users. It merges walking segments to derive a map of walking paths annotated with radio signal strengths. Shu et al. $[15]$ try to solve the last-mile navigation problem using crowdsourced leader's data to guide followers, and they point at the quality control problem of traces' quality. CrowdMap $[16]$ is a crowdsourcing system utilizing sensor-rich video data from mobile users for indoor floorplan reconstruction. It jointly leverages crowdsourced sensory and video data to track user movements, then use the inferred user motion traces and context of the image to produce an accurate floorplan.

# B. Inertial and Motion Sensing

Inertial sensors consume less energy than traditional sensors such as camera, WiFi and GPS, likely to be used in localization $[17]$ and navigation $[18]$ $[19]$ . Dead-reckoning is a way to track people without any prior setup cost $[20]$ .

The most significant challenge in inertial sensing is the accumulation of errors [21] and error caused by phone's attitude [22]. Zee [23] addresses this problem by leveraging the constraints imposed by maps to filter out erroneous measurements. MoLoc [3] gets rid of outliers by comparing the measurement results with that calculated from the corresponding coordinates. However, Zee and Moloc both require the indoor floorplan as a known condition.

Some studies focus on how to reduce the error caused by inertial sensing. For example, WalkCompass $[24]$ describes a phenomenon that the maximum amplitudes along all 3 axes of the accelerometer occur when the heel strikes the ground, and uses a peak recognition algorithm to detect strikes/steps, eliminating cumulative error. In FollowMe $[15]$ , they use the basic idea that rotation axis of the body during a turn is always directed toward the center of earth to detect turn degree.

![](images/27521a63cc68de1135920fe14930e64d245e0ff926119ba6b04a2c3c1cdde3b7.jpg)



Fig. 1: The architecture of SenseWit.

# C. Map Generation and Floorplan Generation

Map generation and floorplan generation are two similar problems, respectively corresponding to outdoor and indoor spaces. But floorplan generation is more challenging, since it is more difficult to obtain accurate coordinates indoors. Jiang et al. [25] propose an automatic floorplan generation method based on hallway, but it mainly depends on WiFi fingerprints to function. Piloc [14] utilizes inertial sensor data and radio signal strengths to calculate the correlation among paths, such that different user trajectories can be merged. Similarly, by identifying remarkable change points of WiFi signals, Walkiemarkie [19] defines WiFi-Marks as landmarks in the 2D plane, which can then be utilized to infer pathway maps. Jigsaw [6] proposes an indoor floorplan reconstruction system, which extracts the position, size and orientation information of individual landmark objects from images taken by volunteers, and combine user mobility traces and location excavated from these images to reconstruct floorplan. CrowdInside [5] adopts the dead-reckoning technique and enhances the accuracy by using unique anchor points, while requiring numerous traces and a uniform starting point to function.

Differing from the existing works, SenseWit doesn't require any infrastructural support (e.g. knowledge of WiFi APs or signals) or high-quality data sources (e.g. photos). It is purely based on inertial sensing of smartphones and generate high-quality floorplans in face of noisy crowdsourced data.

# III. DESIGN

Fig. 1 describes the overall architecture of SenseWit. The entire flow involves volunteering users and a floorplan generation server in the cloud. Data are collected from the inertial sensors in users' smartphones and uploaded to the server. On the server, motion pathlets are generated, features are extracted, and then featured locations (Nails) are labelled on the pathlets. Based on those Nails, pathlets are bundled together according to our pathlet bundling algorithm. In this way, a complete floorplan is progressively generated.

![](images/b1635601ae13e9e22552e971d34dde7593c87f2225e0d342c2c7d73b1d40de3e.jpg)



Fig. 2: The decision tree in feature recognition phase.

# A. Feature Recognition and Labeling

1) Data Collection: In SenseWit, three kinds of sensors are used — Accelerometer and gyroscope are used to compute steps and generate movement pathlets. Compass can fix the pathlets into a certain direction. Note that we employ periodical checking instead of collecting data all the time. The collection process is triggered when a step is detected, and is stopped after the user keeps stationary for a certain period or the collection time exceeds a threshold. It is worth noticing that the indoor magnetic field is usually distorted by ambient interferences. We borrow the technique in WalkCompass [24] to eliminate the errors induced by those interferences. Although that technique does not work for all the cases, it offers quite good performance according to our own implementation results.

2) Feature Recognition: Given the preprocessed data, we first use a sliding window of 128 samples to segment data. The effectiveness has been shown in previous work [26]. For each segment, we use a decision tree to identify the motion state (walking, keeping stationary or irregular), as shown in Fig. 2. Particular features are then used to discover featured locations, e.g. water dispenser, turning, and door. We use these three types of featured locations as examples to illustrate our idea, but our approach can identify and utilize any distinguishable featured location in the indoor space.

Turning: The most direct way to recognize a turning is to calculate the change in walking direction. However, both the diversity of people's behavior and the error introduced by direction estimation cause interference. The biggest difference is “soft turn” and “sharp turn”. When people make a soft turn, each amplitude of variation is smaller. So we take two ways to recognize a turning:

First, a sharp turn is recognized if $|d_{s_{n+1}} - d_{s_n}| \geq d_\alpha$ , where $s_n$ and $s_{n+1}$ are two sequential steps and d is the walking direction. Second, if we detect $|d_{s_{n+1}} - d_{s_n}| \geq d_\beta$ , we record and analyze the following directions. If the direction change exceeds $d_\alpha$ in 6 steps, we consider it as a soft turn. Otherwise, we ignore it. We choose 6 steps because people usually make a turning in less than 6 steps [24].

Water Dispenser: When people walk to a water dispenser or a reception, a relatively long stationary period and a direction change can be extracted as feature, as shown in Fig. 3. The recognition process starts when the state transits from walking to the stationary state. In order to distinguish this feature from other behavioral interference, such as a temporary stop or sitting, we propose two measures. First, If the stationary duration is longer than a threshold $t_{\alpha}$ , it may represent sitting and is not what we need. Otherwise, we get the walking direction and judge if the change is larger than $d_{\gamma}$ . Only when these two conditions are satisfied, we recognize this location effective.

![](images/19c16c830261f4c65527482327ca053bf1bdc344fa732b867f3098400ad0d7b7.jpg)



(a) Acceleration

![](images/7db32b8147110e3f94ded51ad4afeb93f30e7e238811fc78fd41c9132fb5e371.jpg)



(b) Walking direction

Fig. 3: Features of water dispenser.   
![](images/7717899e65a1b56064bf6d011cd9b079f3c16a90824461a65d8151f7ef8e0bf7.jpg)



(a) in the palm/pocket

![](images/5137b412435e66fadc861d3d9d499a7b33c30e1182d8ebc4d904e65eac676600.jpg)



(b) in a swinging hand   
Fig. 4: Features of door in different phone placements.

Door: When people are walking through a door, they tend to slow down, open the door, then make a turning and close the door. These continuous motions can be recognized as features. However, interfered by the placement and orientation of the phone, the features are probably blurred.

According to the experiments, when people hold the phone in the palm, texting, phoning or in the pocket, the angular velocity always presents similar characteristics, namely a pair of prominent crest and valley, as shown in Fig. 4(a). When people hold the phone in a swinging hand, the features are quite different, as shown in Fig. 4(b), where the two slow valleys are distinguished from the normal periodical motions. We borrow the classifier in [26] to judge phone placement, so that these two situations can be distinguished and the features of door can be recognized. It is worth mentioning that if a user operates in totally uncontrolled condition, false positive in feature recognition may occur. The chance of a same false positive to occur multiple times, however, is generally very low. As a result, such uncontrolled behavior will not be recognized as a stable feature.

3) Feature Labeling: Knowing the step length and direction, each walking pathlet can be denoted as follows:

$$
P = \{(0, 0), (x _ {1}, y _ {1}), (x _ {2}, y _ {2}),..., (x _ {n}, y _ {n}) \} \tag {1}
$$

where n is the total moving steps. On each pathlet, the coordinates of the starting point are $(0,0)$ . Different pathlets have different starting points. We unify all the pathlets to a global coordinate system based on the compass reading so that a collected pathlet can be translated but cannot be arbitrarily rotated. The featured location set corresponding to each pathlet can be described as:

$$
\{\{l _ {1}, (x _ {1}, y _ {1}) \}, \{l _ {2}, (x _ {2}, y _ {2}) \},..., \{l _ {k}, (x _ {k}, y _ {k}) \} \} \tag {2}
$$

where k is the number of features on this pathlet and $l_{k}$ represents the label of feature.

# B. Floorplan Generation

In this section, we first introduce details about TriNail, including the definition, the reason we choose it, and the pathlet matching strategy. Then we demonstrate how to evaluate the priority of TriNail classes and the pathlet bundling algorithm. Finally, we present the floorplan shaping.

# 1) TriNail Overview:

Definition of TriNail: A TriNail is defined as a virtual triangle formed by three non-collinear Nails on a certain pathlet, which can be described with a feature vector:

$$
\text { TriNail } (i, P _ {k}) = \left(l _ {1}, l _ {2}, l _ {3}, e _ {1 2}, e _ {1 3}, e _ {2 3}\right), 1 \leq k \leq m \tag {3}
$$

$P_{k}$ is the $k$ th pathlet and $i$ denotes the $i$ th TriNail on $P_{k}$ . $l$ are the labels of Nails. $e$ represent the features of an edge, including the edge's length and orientation.

Reason for Choosing TriNail: The main role of TriNail is to improve the pathlet bundling accuracy. Influenced by feature recognition and labeling error, not all the pathlets carry correct information. If we use incorrect pathlets as references, there will be paradoxes in the result. Note that three points are the minimum to achieve a stable planar structure. Using three Nails for matching enables one to learn stable structures as efficient as possible, while eliminates the interferences of paradoxes. We use TriNail in pathlet priority assessment, ensuring the reliability of bundled pathlets.

However, TriNails still meet a problem called analogous sub-structures, meaning that though pathlets own the same feature vector, they belong to different indoor regions and should not be bundled. Fig. 7(a) shows a real example. TriNails $A_{1}B_{1}C_{1}$ and $A_{2}B_{2}C_{2}$ are both featured with three turnings and similar in shape, but they represent different regions. We propose an improved method to resolve this problem in Sec. III-B2 and discuss it in Sec. III-C.

TriNail Matching Principle: In principle, two TriNails are matched only if they have the same feature vectors. But it is hard to find two TriNails that have exactly same feature vectors due to the localization error. Therefore, we devise an approximation strategy to tolerate errors while preserving the correctness and efficiency of TriNail matching.

For two TriNails A and B, they are considered to be matched and belong to the same TriNail class if and only if:

$$
\frac {S (A \cap B)}{\max \{S (A) , S (B) \}} \geq \alpha \text {   and   } f (A) = f (B) \tag {4}
$$

where $S(A)$ and $S(B)$ represent the area of A and B. $S(A \cap B)$ is the maximum common area, which is obtained by translating two triangles and making them overlap with each

![](images/87655ba544f8446ff3b66b486414dc0914095e682dcd72c4640496e5a0361d4d.jpg)



Fig. 5: Analogous sub-structures problem.

Algorithm 1 Pathlet Bundling Algorithm   
Require: m useful pathlets $\{P_{k}\}, 1 \leq k \leq m$ and pathlets $\{p\}$ that do not contain TriNails
Ensure: An indoor floorplan F
1: Construct TriNail set $S\{P_{k}\}$ ;
2: Classify $S\{P_{k}\}$ into classes $S\{C\}\{C_{1}, C_{2}, \cdots, C_{n}\}$ ;
3: Select a seed $C_{s} \in S\{C\}$ ;
4: repeat
5: Bundle pathlets $\{P_{a}, P_{b}, \cdots\} \in P_{k}$ based on $C_{s}$ ;
6: Delete $C_{s}$ from $S\{C\}$ ;
7: Refresh the Matrix;
8: if $\{C_{i}\} \in S\{C\}$ appears in both $\{P_{a}, P_{b}, \cdots\}$ and $\{P_{k}\} - \{P_{a}, P_{b}, \cdots\}$ then
9: select $C_{s} \in \{C_{i}\}$ that appears most in $\{P_{k}\} - \{P_{a}, P_{b}, \cdots\}$ as the seed;
10: else
11: select $C_{s} \in S\{C\}$ as the seed;
12: end if
13: Delete $\{P_{a}, P_{b}, \cdots\}$ from $\{P_{k}\}$ ;
14: until $S\{C\} \emptyset$ or $\{P_{k}\} \emptyset$ 15: if more than one set exist
    and the sets can be connected through $\{p\}$ then
16: bundle the sets;
17: end if

other as much as possible. $\alpha$ is a threshold that constrains the similarity of TriNail's shape, which is obtained through empirical experiments. If the ratio exceeds $\alpha$ , we define them as similar in shape. $f(A)=f(B)$ means that the matched TriNails have completely same labels.

# 2) Pathlet Bundling Algorithm:

Priority of TriNail Class: TriNails are converted into discrete classes through the matching principles, and a TriNail class includes all the matched TriNails having the same labels and similar shape. The relationship between classes and pathlets are acquired, so that the occurrence frequency of each class can be described by a matrix:

$$
M = \begin{array}{c} C _ {1} \\ C _ {2} \\ \vdots \\ C _ {k} \end{array} \left( \begin{array}{c c c c c} P _ {1} & P _ {2} & \ldots & P _ {m} & T o t a l \\ 1 & 0 & \ldots & 2 & N _ {1} \\ 0 & 1 & \ldots & 0 & N _ {2} \\ \vdots & \vdots & \ddots & \vdots & \vdots \\ 1 & 1 & \ldots & 0 & N _ {k} \end{array} \right)
$$

The elements in the matrix represent how many times the TriNail class $C_{i}$ appears on pathlet $P_{j}$ , and the last column represents the total number of times this class appears.

There are still two challenges in pathlet bundling. First, errors occur in feature recognition, leading to wrong labels. A TriNail with label $\{1,2,1\}$ might be judged as $\{1,2,2\}$ , or an extra label is added although it does not exist at all. Second, TriNail matching does not eliminate all the ambiguity, due to the analogous sub-structures problem.

Analogous sub-structures problem is quite common in indoor space. Figure. 5 presents a general floorplan of a shopping mall. There exist two pathlets: one has three Nails $\{A, B, C\}$ , another with three same Nails $\{a, b, c\}$ , and the path segments are all identical. But these two pathlets cannot be bundled because they are actually in different regions. If they are bundled, the result will be wrong.

In order to solve the above problem, SenseWit runs in an iterative manner. In each round, we select the TriNail class with the highest priority as the footstone. There are three stepwise principles to determine the priority of TriNail class:

(1) If the matrix element in the row $C_{i}$ (except the total number) is larger than 1, the corresponding TriNail class is suspected to be analogous sub-structure and therefore disabled throughout the pathlet bundling process. This step is completed before the pathlet bundling iterations.   
(2) A class that appears more frequently on the remaining pathlets is given higher priority. This principle is designed to deal with the label error, for the occurrence of a wrong label is actually a special case. If the occurrences are the same, the one with larger area is prioritized.   
(3) If the occurrence frequency of a TriNail class is less than a threshold, we discard the corresponding pathlets, because those pathlets often indicate uncommon behavior. The threshold is acquired through experiments.

The function of the above principles is to filter out various errors including the analogous sub-structures, so that incorrect pathlet bundling can hardly happen. We admit that there might be both false positives and false negatives generated during the first step. The false positives are due to repeated traverses on a same TriNail. The corresponding side effect is that some useful pathlets are discarded, which is usually not a big problem in the assumed scenario. On the other aspect, when two analogous sub-structures are not covered by any of the pathlets, they two will not be filtered out, thus being a false negative. The worst case caused by false negatives is a small fraction of pathlets are bundled to wrong places. Generally speaking, that will not change the floorplan shape we obtain in the end.

Algorithm Flow: The algorithm works in a greedy manner, as described in Algorithm 1. In each round, a TriNail class with the highest priority is selected as the footstone, and all the pathlets containing the seed are bundled.

![](images/f7bd27e8f4c3fb8d1cc37f179b120bf45543c08fbde03fbb183f396e4b1df4c7.jpg)



Fig. 6: Two rounds of pathlet bundling.

Fig. 6 illustrates two iterations. The TriNails are denoted using dashed line while the labels are represented with different icons and numbers. In the first round, the pathlets are bundled based on the TriNail with label sets $\{1,1,2\}$ . Next, another TriNail with label sets $\{1,3,2\}$ can be found on the bundled pathlets. Based on this TriNail, the third pathlet is bundled together in the second round.

3) Floorplan Shaping: After the above steps, chaotic pathlets have been processed and bundled together. In this way, a rough floorplan is generated. To provide a better visualized result, we go one step further and utilize the technique of occupancy grid map $[6]$ $[27]$ to construct the hallway and room structure. The experiment results in Sec. IV present clear instances.

# C. Discussion

We have analyzed the complexity and storage cost of our algorithm in the previous work [28]. Here we make some deeper discussion about our work.

Pervasiveness of Featured Locations: In this paper, we only illustrate three types of featured locations as examples and the main scene is office or teaching building. Different features can be exploited in different scenarios, such as open space, museum, and shopping mall. The case without turning points, e.g. a circle floor plan, is especially interesting. In fact, there are many featured locations that can be exploited, such as entrance, elevator, gate of a shop, and a small coffee bar in the area, etc. Generally pedestrians have featured behavior at those locations, e.g. change in walking speed (looking for directions, slow down at a crowded entrance), stop at the gate or the coffee bar, or change in Z-axis acceleration (i.e. on/off the elevator). Meanwhile, a pedestrian's temporary behavior (e.g., meet someone and stop for a while) might induce label error, and our priority-based algorithm can deal with such situations.

Feature Labeling: Intuitively, the labeling error increases with the growth of hallway's width, caused by people's different walking habits (e.g., walk in the middle vs. along the side). Our study on 30 volunteers indicates that over $90\%$ people tend to walk in the middle of hallways. The experiments in Sec. IV also demonstrate that the labeling errors of turning are acceptable when the hallway width is within $3\mathrm{m}$ .

![](images/50aace85c73012814294d1eb25a791c18c01a26fc62fa438826e052d7e3af800.jpg)



(a) Scenario 1

![](images/ead5f7c0a2ff1f8b8509bed5a930b5c7f751ae850fa580ddc9a2f373dd5d566e.jpg)



(b) Scenario 2

Fig. 7: The ground truth of two scenarios.   
![](images/aec1a4ad4535620582d95708efc70b2f863d839c54315e5f58be90355d15fdf0.jpg)



(a) Matching 35 pathlets with varied $\alpha$ .

![](images/706ea9c4e32e4a9d6efad352af13b15c7937762be39384a7c77df79b82c911af.jpg)



(b) Matching a combined set of pathlets with varied $\alpha$ .   
Fig. 8: Tuning the parameter $\alpha$ .

It sometimes happens that a featured location (e.g. a door) is not recognized. Generally, the misrecognition of a featured location changes the feature labels corresponding to a pathlet and decreases the chance of TriNail matching, but does not introduce any error into the floorplan.

Energy and Privacy: We use inertial sensors instead of power-wasting ones (camera, radio, GPS), and employ periodical checking and conditional triggering instead of always on. Therefore, the energy cost can be reduced to an acceptable degree. Moreover, we do not need users' personal information, avoiding leakage of user privacy.

# IV. EVALUATION

In this section, we first introduce our experimental environments and present the tuning of key parameters, followed by evaluation on the feature recognition accuracy, pathlet labeling accuracy, and floorplan generation performance.

# A. Experimental Environments

We implement SenseWit on different Android phones (Samsung Galaxy S5, Galaxy Note3, HTC ONE M8, Millet 3) and conduct experiments in two scenarios: an office of $24m \times 19.2m$ with 2 doors, 2 water dispensers (marked with red dots) and more than 10 turnings; and one floor in a campus library with $464m^{2}$ area, having 6 rooms. Fig. 7 is the ground truth. 10 volunteers are invited in two scenarios respectively. The sampling rate is 50Hz.

# B. Tuning of a Key Parameter

Recall Eq. (4) in Section III, $\alpha$ is a similarity threshold used to judge whether two TriNails are matched. A higher value of $\alpha$ may introduce false negatives while a lower value may cause false positives. Therefore, we conduct experiments to tune this parameter and obtain the appropriate setting of $\alpha$ .

TABLE I: Hallway shape precision with different values of $\alpha$ . 

<table><tr><td></td><td> $\alpha = 0.6$ </td><td> $\alpha = 0.7$ </td><td> $\alpha = 0.8$ </td></tr><tr><td>Scenario 1</td><td>69.2%</td><td>75.0%</td><td>78.5%</td></tr><tr><td>Scenario 2</td><td>62.5%</td><td>66.9%</td><td>72.1%</td></tr></table>

TABLE II: Confusion matrix of feature recognition. 

<table><tr><td></td><td>Turning</td><td>Door</td><td>Water</td><td>Null</td><td>Recall</td></tr><tr><td>Turning</td><td>73</td><td>0</td><td>0</td><td>3</td><td>96.1%</td></tr><tr><td>Door</td><td>5</td><td>40</td><td>0</td><td>0</td><td>88.9%</td></tr><tr><td>Water</td><td>0</td><td>0</td><td>23</td><td>4</td><td>85.2%</td></tr><tr><td>Precision</td><td>93.6%</td><td>100%</td><td>100%</td><td>-</td><td>-</td></tr></table>

First, we select 35 pathlets that contain a same class of TriNail. Ideally, each pair of the TriNail should be matched. But due to the noise of sensor data, the similarity between some pairs might decrease. Fig. 8(a) plots the percentage of matched pairs when different threshold $\alpha$ is set. We can see that setting $\alpha$ at 0.6 tolerates all errors, while $\alpha$ over 0.8 may filter out a large fraction of truly matched pairs.

Second, we add additional 25 pathlets in, which contain another class of TriNail. Ideally, there should be 895 ( $\binom{35}{2}$ + $\binom{25}{2}$ ) matched pairs in total. Fig. 8(b) plots the matched pairs when different threshold $\alpha$ is set. The result of the first experiment is included for comparison. Note that ticks on the X-axis are in descending order. When $\alpha$ is 0.8, $60.1\%$ of the 895 pathlets are correctly matched while 9 pathlets are wrongly matched, but when $\alpha$ is 0.6, the correctly matched num increases to $70.2\%$ at the cost of 174 are wrongly matched. We can see that the false positives grow faster when $\alpha$ is smaller.

Table I shows the overall precision of the generated hallway shape with $\alpha$ at 0.6, 0.7, and 0.8. One can see that $\alpha=0.8$ obtains the highest precision, because there is less false matching. Therefore, we set $\alpha$ at 0.8 in our implementation and later experiments.

# C. Feature Recognition Accuracy

We select 30 typical pathlets with 148 featured locations to evaluate the accuracy of feature recognition. The result is shown in Table II. The row denotes the real features, while the column is the recognition results. The diagonal indicates the number of correctly classified features, while “Null” column indicates failing to recognize. We can see that the recalls are all higher than 85% and the precisions are more than 90%. Some doors are wrongly recognized as turning because the door opening/closing motions are often along with turning. And the missing water dispenser might be caused by particular behavior (such as waiting for long time when fetching water).

# D. Pathlet Labeling Accuracy

We conduct experiments to measure the labeling accuracy for turning, water dispenser, and door, respectively. Fig. 9 shows the cumulative distributed function of the location deviations in all three cases.

![](images/daa21763f981202a3606a73d21fa77e31b849bb86dadf37df69497b46c0b2ddd.jpg)



(a) Turning

![](images/926996b4f878bd94406fe2b908a92c96cfebbccaf21b537d26495b15336a5e00.jpg)



(b) Water dispenser

![](images/1b3fbd621a40ae59cb774f883678cbc78196cd083aa21b8f46396fc5490379f2.jpg)



(c) Door   
Fig. 9: Labeling deviations.

![](images/72677f99a49468e8c69b18c65720e9aaa0c2cc6931eeaccd2e781d0112f33c8a.jpg)



(a) The median

![](images/4b827285dc618b292568a88d2622c83ada345f6babb16750569eb5bfac637732.jpg)



(b) The $75^{th}$ percentile   
Fig. 10: Influence of hallways' width and length.

We can see that though a small proportion of large deviations (1.8m) occur for water dispenser and door, around 90% of the results have errors less than 1m. Considering that we select the front of water dispenser and door's center as the labelled point, the result is relatively accurate. Although the result of turning is not so accurate as the others, 70% of the location deviation is still under 1m and 90% of the results have deviations less than 1.5m, demonstrating a good accuracy. In addition, there're a spot of deviations larger than 2m in turning, caused by people who sometimes walk along the border of corridor, but this only accounts for less than 3% of all measurements.

We present more details to measure the influence of different users and placements. Due to the page limit, we only take turning as an example to illustrate the results.

Fig. 10 shows the median and the $75^{th}$ percentile for different situations of hallways' width and pathlet length. We can see that although the location deviation grows a bit larger when the hallway becomes wider, it still keeps at a low error level of around $0.8m$ in median and $1.2m$ for $75^{th}$ percentile, respectively. Considering that the hallways are commonly less than $3m$ in daily life, our method is robust to different environments.

# E. Floorplan Generation Performance

Fig. 11 and Fig. 12 present the results of two scenarios. In Scenarios 1, the dotted lines in Fig. 11(a) draw the hallway. The blank area represent stationary objects like tables, seats, or other obstacles. The final floorplan is presented in Fig. 11(b). And in Scenario 2, there are 6 detached regions, and 5 of them are recognized. Two detached rooms in the left are combined

![](images/84a28976e69727939ffa324ce54f3223c8cf548ca4a33f2a1d13f323208950d5.jpg)



(a) Pathlet Bundling Result

![](images/8cd6270a5cc54170f4b019e3c704f18cf0688893ccc9e493e8db76e55a2c0292.jpg)



(b) Shaped Floorplan

Fig. 11: Floorplan generation of the first scenario.   
![](images/07a2c61febb39c319a54a82f099cef2f6a1d239181754708fbd57edb5116beb2.jpg)



(a) Pathlet bundling result

![](images/8af67b55140d4c8ea2eb7abef264e76a3ce626547cd40285285951639128bc28.jpg)



(b) Shaped floorplan   
Fig. 12: Floorplan generation of the second scenario.

as one because the door is always open, resulting that people behave the same as elsewhere in the hallway.

We evaluate the performance from three aspects: pathlet dependency, hallway shape, and room size. In terms of hallway shape and room size, we compare Sensewit with CrowdInside [5] and Jigsaw [6]. Specifically, we implement CrowdInside and show its performance in two scenarios. Note that Jigsaw also uses visual data. We cannot implement it with the same conditions. Therefore we cite the evaluation results presented by Jigsaw itself in [6] for comparison.

Pathlet Dependency: We carry out a new experiment to assess the dependency between the number of TriNail classes and the number of pathlets. This is an indirect indicator of the floorplan generation efficiency using our proposal. Specifically, there are 20 Nails in Scenario 1. So the number of all possible TriNail classes is $\binom{20}{3}=1140$ . Meanwhile in practice, we can see from Fig. 13 that the number of TriNail classes is around 450. The number of TriNail classes does not apparently increase after 250 pathlets are used. The result is similar in Scenario 2. The number of TriNail classes does not apparently increase after 300 pathlets are used. It is because $\binom{N}{3}$ is the maximum of all possible TriNail classes. There are some pathlet, i.e. the combinations of Nails, which rarely appear in a real data set. That indirectly means our floorplan generation approach can work with relatively small data sets.

![](images/1df89e3e3033dbf9a7fe45f90b12de319f8e8b9d43b6dff74b6d74d741969e4d.jpg)



Fig. 13: TriNail statistics.

Hallway Shape: We adopt the same metric as CrowdMap [16] to evaluate the hallway shape similarity, and the result is shown in Table III. Three metrics below are used.

$$
\mathcal {P} = \frac {\left| S _ {\text { gen }} \cap S _ {\text { true }} \right|}{\left| S _ {\text { gen }} \right|} \tag {5}
$$

$$
\mathcal {R} = \frac {\left| S _ {\text { gen }} \cap S _ {\text { true }} \right|}{\left| S _ {\text { true }} \right|} \tag {6}
$$

$$
\mathcal {F} = 2 * \frac {\mathcal {P} * \mathcal {R}}{\mathcal {P} + \mathcal {R}} \tag {7}
$$

The overlapping area is acquired by aligning both the center point and the orientation. We can see that SenseWit is better than CrowdInside in both two scenarios, while a little poorer than Jigsaw. This is because that Jigsaw uses reliable images obtained by camera instead of low-quality inertial sensors. But the camera will consume a lot of energy. In addition, Jigsaw achieves its accuracy at very high labor cost and complexity, which are not required in SenseWit. In SenseWit, recalls are both higher than precisions for two scenarios because the bundled pathlets are a bit wider than the ground truth, due to location errors.

Room Size: We evaluate the error of reconstructed room size and compare SenseWit with CrowdInside in the second scenario and Jigsaw. Room area error is defined as the area difference between the generated room layout and the ground truth divided by the ground truth. It is calculated and the result is shown in Table IV. Jigsaw achieves an average error of 27.6%, and CrowdInside has an error of 40.6%. SenseWit only needs the featured pathlets instead of other references like low-efficiency cameras in Jigsaw, while the error level of SenseWit is comparable to that of Jigsaw. The error is mainly caused by obstacles, where people's movements do not cover.

TABLE III: Evaluation of hallway shape. 

<table><tr><td></td><td>Scenario 1</td><td>Scenario 2</td><td>CrowdInside Scenario 1</td><td>CrowdInside Scenario 2</td><td>Jigsaw</td></tr><tr><td> $\mathcal{P}$ </td><td>78.5%</td><td>72.1%</td><td>60.8%</td><td>58.2%</td><td>77.8%</td></tr><tr><td> $\mathcal{R}$ </td><td>84.5%</td><td>80.3%</td><td>46.9%</td><td>45.3%</td><td>90.4%</td></tr><tr><td> $\mathcal{F}$ </td><td>81.4%</td><td>76.0%</td><td>53.0%</td><td>50.9%</td><td>83.6%</td></tr></table>

TABLE IV: Evaluation of room size. 

<table><tr><td></td><td>SenseWit</td><td>CrowdInside</td><td>Jigsaw</td></tr><tr><td>Error</td><td>31.4%</td><td>40.6%</td><td>27.6%</td></tr></table>

# V. CONCLUSION

This paper presents our effort to employ mobile crowdsourcing in the application scenario of floorplan generation. The design and implementation of SenseWit involves successful practice to address practical challenges in utilizing crowdsensed data, such as noise, ambiguity, and diversity of people's behavior. We believe this work acts as an example of using crowdsourcing to solve traditional hard problems.

# REFERENCES

[1] D. M, P. R. L, and L. A. B, “Gbus-route geotracer,” in IEEE Workshop on Vehicular Traffic Management for Smart Cities, 2012.   
[2] K. Chintalapudi, A. P. Iyer, and V. N. Padmanabhan, “Indoor localization without the pain,” in ACM MobiCom, 2010.   
[3] W. Sun, J. Liu, C. Wu, Z. Yang, X. Zhang, and Y. Liu, “Moloc: On distinguishing fingerprint twins,” in IEEE ICDCS, 2013.   
[4] X. Chen, X. Wu, X. Li, Y. He, and Y. Liu, “Privacy-preserving high-quality map generation with participatory sensing,” in IEEE INFOCOM, 2014.   
[5] A. Moustafa and Y. Moustafa, “Crowdinside: Automatic construction of indoor floorplans,” in ACM SIGSPATIAL, 2012.   
[6] R. Gao, M. Zhao, T. Ye, F. Ye, Y. Wang, K. Bian, T. Wang, and X. Li, "Jigsaw: Indoor floor plan reconstruction via mobile crowdsensing," in ACM MobiCom, 2014.   
[7] S. V. G. de Magalhaes, W. R. Franklin, W. Li, and M. V. A. Andrade, "Fast map generalization heuristic with a uniform grid," in ACM SIGSPATIAL, 2014.   
[8] M. Azizyan, I. Constandache, and R. R. Choudhury, “Surroundsense: Mobile phone localization via ambience fingerprinting,” in ACM Mobi-Com, 2009.   
[9] H. Shin, Y. Chon, and H. Cha, “Unsupervised construction of an indoor floor plan using a smartphone,” IEEE Transactions on Systems, Man, and Cybernetics Society, vol. 42, no. 6, pp. 889–898, 2012.   
[10] P. Zhou, Y. Zheng, and M. Li, “How long to wait?: Predicting bus arrival time with mobile phone based participatory sensing,” in ACM MobiSys, 2012.   
[11] L. S, L. Y, and N. L, “Detecting crowdedness spot in city transportation,” IEEE Transactions on Vehicular technology, vol. 62, no. 4, pp. 1527–1539, 2013.   
[12] R. R. K, C. C. T, and K. S. S, “Ear-phone: an end-to-end participatory urban noise mapping system,” in IEEE IPSN, 2010.   
[13] H. Wang, S. Šen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: Unsupervised indoor localization,” in ACM MobiSys, 2012.   
[14] C. Luo, H. Hong, and M. C. Chan, “Piloc: a self-calibrating participatory indoor localization system,” in IEEE IPSN, 2014.   
[15] Y. Shu, K. G. Shin, T. He, and J. Chen, “Last-mile navigation using smartphones,” in ACM MobiCom, 2015.   
[16] S. Chen, M. Li, K. Ren, and C. Qiao, “Crowd map: Accurate reconstruction of indoor floor plans from crowdsourced sensor-rich videos,” in IEEE ICDCS, 2015.   
[17] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: Wireless indoor localization with little human intervention,” in ACM Mobicom, 2012.   
[18] F. Li, C. Zhao, G. Ding, J. Gong, C. Liu, and F. Zhao, “A reliable and accurate indoor localization method using phone inertial sensors,” in ACM Ubicomp, 2012.

[19] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, “Walkiemarkie: Indoor pathway mapping made easy,” in USENIX NSDI, 2013.   
[20] M. Alzantot and M. Youssef, “Uptime: Ubiquitous pedestrian tracking using mobile phones,” in IEEE WCNC, 2012.   
[21] S. Beauregard and H. Haas, “Pedestrian dead reckoning: A basis for personal positioning,” in IEEE WPNC, 2014.   
[22] L. Zhang, K. Liu, Y. Jiang, X. Li, Y. Liu, and P. Yang, “Montage: Combine frames with movement continuity for realtime multi-user tracking,” in IEEE INFOCOM, 2014.   
[23] R. Anshul, K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: Zero-effort crowdsourcing for indoor localization,” in ACM MobiCom, 2012.   
[24] N. Roy, H. Wang, and R. R. Choudhury, “I am a smartphone and i can tell my users walking direction,” in ACM MobiSys, 2014.   
[25] Y. Jiang, Y. Xiang, X. Pan, K. Li, Q. Lv, R. P. Dick, L. Shang, and M. Hannigan, “Hallway based automatic indoor floorplan construction using room fingerprints,” in ACM UbiComp, 2013.   
[26] M. Susi, V. Renaudin, and G. Lachapelle, “Motion mode recognition and step detection algorithms for mobile phone users,” Sensors, vol. 13, no. 2, pp. 1539–1562, 2013.   
[27] S. Thrun, “Learning occupancy grid maps with forward sensor models,” Autonomous robots, vol. 15, no. 2, pp. 111–127, 2003.   
[28] L. Jiaqi, H. Yuan, and L. Yunhao, “Sensewit: Pervasive floorplan generation based on only inertial sensing,” in IEEE DCOSS, 2016.

![](images/491af2ec036c8ff6e8fa66ffedfe0c2669a321027044a6a028eb054f032c851d.jpg)



Yuan He is an associate professor in the School of Software and TNLIST of Tsinghua University. He received his BE degree in University of Science and Technology of China, his ME degree in Institute of Software, Chinese Academy of Sciences, and his PhD degree in Hong Kong University of Science and Technology. His research interests include Internet of Things, wireless networks, pervasive computing, and cloud computing. He is a member of the IEEE and ACM.

![](images/a9dfefb4f942d93791b5bfa189908ca649bbe97709833d8c3f251085ed1518fe.jpg)



Jiaqi Liang is now a software engineer in the IT department of China Merchants Bank. She received her ME degree in the School of Software and TNLIST of Tsinghua University, and received her BE degree in Northeastern University, China. Her research interests include Internet of Things and mobile computing.

![](images/94acd183cd84bb95ec5b16374d2aa5b2e275eaec5b121b53b6896238f857b0c9.jpg)



Yunhao Liu Yunhao Liu received the BS degree from the Automation Department, Tsinghua University, and the MA degree from Beijing Foreign Studies University, China. He received the MS and PhD degrees in computer science and engineering from Michigan State University. He is currently the dean of the School of Software, and holds ChangJiang Chair Professorship at Tsinghua University. He is serving as the associate editor-in-chief for the IEEE Transactions on Parallel and Distributed Systems and associate editor for the IEEE/ACM Transactions on

Networking and ACM Transactions on Sensor Networks. He is a fellow of the IEEE, a fellow of the ACM, and chair for the ACM China Council. His research interests include sensor network and iot, localization, network diagnosis, rfid, distributed systems, and cloud computing.