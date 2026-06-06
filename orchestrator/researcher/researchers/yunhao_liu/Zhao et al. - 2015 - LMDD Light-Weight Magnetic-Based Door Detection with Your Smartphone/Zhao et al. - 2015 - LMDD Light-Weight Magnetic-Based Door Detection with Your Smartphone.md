# LMDD: Light-weight Magnetic-based Door Detection with Your Smartphone

Yiyang Zhao $^{1}$ , Chen Qian $^{2}$ , Liangyi Gong $^{3}$ , Zhenhua Li $^{1*}$ , and Yunhao Liu $^{1}$

$^{1}$ School of Software and TNLIST, Tsinghua University, China

Email: {yiyangzhao, lizhenhua1983, yunhao}@tsinghua.edu.cn

$^{2}$ Department of Computer Science, University of Kentucky, USA

Email: qian@cs.uky.edu

$^{3}$ Department of Computer Science, Harbin Engineering University, China

Email: gogly.hrbeu@gmail.com

Abstract—Doors are important landmarks for indoor positioning systems. Hence an accurate and light-weight door detection approach is highly desired. The state-of-the-art solutions are either vision based or infrastructure based, which incur non-trivial device or management cost. This paper presents a novel approach, Light-weight Magnetic-based Door Detection (LMDD), which only relies on the information from built-in sensors of a smartphone. LMDD detects a door by analyzing the change of magnetic signal and extracting special features caused by doors. It is light-weight in both computation and infrastructure cost. We have implemented a prototype of LMDD that has been installed on various Android phones. Experimental results show that LMDD achieves door detection accuracy of 74% in average, ranging from 66% to 85% in various typical environments such as offices, classrooms, residential houses, and a hospital.

Index Terms—Door Detection; Indoor Positioning Systems (IPS); Magnetic Signal; Wireless Sensor Network.

# I. INTRODUCTION

Indoor Positioning Systems (IPSs) have attracted much attention from both academia and industry. In many real-world applications, especially some emergent situations, the requirements of location information are raised rapidly. For example, IPSs can help seniors or visually impaired people locate their position and further look for a destination in a building.

As natural landmarks, the locations of doors constitute significant factors for high-accuracy IPS applications. Doors not only connect rooms and corridors, but also determine potential navigation paths. Compared with other architectural elements, like elevators, escalators and stairs, doors are pervasive in almost all indoor environments. To detect doors accurately with low complexity, a light-weight door detection approach is highly desired.

The state-of-the-art door detection solutions can be categorized into two types: vision based and infrastructure based. Vision based solutions rely on complicated image processing and pattern recognition algorithms to identify doors. For example, they have been used to navigate intelligent robots in indoor environments $[44]$ . Meanwhile, door detection with infrastructures, such as preinstalled ultra-wide band devices, WiFi APs, or RFID tags, was proposed for precise indoor

![](images/ca915a4404be90b3631407d44d3dfc19fb62d49d1e2817a4cbd0e6c56fddbe16.jpg)



Fig. 1. Changes of magnetic intensity across sampling points.

localization [24]. For example, Zee [27] combines the sensor information of smartphones with the WiFi information of wireless infrastructures to calculate door positions. In general, these existing solutions incur non-trivial, sometimes even enormous device or management cost.

In this paper we propose a novel door detection approach named LMDD, which is a light-weight and broadly applicable door detection approach based on information collected by a smartphone. It analyzes readings from the built-in magnetic sensors (e.g., magnetometer) of a smartphone. Doors are then detected by capturing the anomalies or sharp fluctuations of magnetic signals, as demonstrated in Fig. 1. Without any pre-installed infrastructure, we can find a door passively and efficiently from magnetic sensing data.

The biggest challenge of an infrastructure-free door detection approach is to accurately extract the signal features for an event of passing through a door. This is because magnetic signal changes may be caused by various “environmental events”. For instance, magnetic intensity values also change sharply when the holder shakes the smartphone. To eliminate such “noises”, we combine feature analysis methods with automatic filtering on magnetic sensing data.

We have implemented a prototype of LMDD and successfully deployed it on a variety of Android phones, including Google Nexus5, Sumsang Galaxy S4, HTC One M8, and so forth. We evaluate our approach in various typical environments, including offices and classrooms in a university, residential houses, and a hospital. The experimental results show that the door detection accuracy is around 74% in average, ranging from 66% to 85%. Meanwhile, the computational complexity of LMDD stays in $O(KN\sigma_{s}^{2})$ , where K denotes the number of doors, N represents the necessary sampling points for detecting a single door (typically between 100 and 200), and $\sigma_{s}$ is the width of the Gaussian function (typically between 20 and 100).

The main contributions of our work are listed as follows:

- A novel light-weight door detection approach based on magnetic signal information (LMDD) is proposed. Without pre-installed facilities, LMDD makes use of natural features of doors in indoor environments. Thus, it can provide fine-grained and sufficient landmarks for IPS applications.   
- A novel detection model is set up to capture door events in the magnetic sensing data. It focuses on drastic intensity variations of built-in magnetic sensors when users pass through a door.   
- We have implemented a prototype of LMDD and deployed it on multiple popular Android smartphones. The experimental results indicate that LMDD achieves an acceptable precision in various typical environments.

Roadmap. The rest of this paper is organized as follows. In Section II, we survey the related work. In Section III, we introduce the design of LMDD. In Section IV, we describe the system implementation and report the evaluation results. Finally, Section V concludes our work.

# II. RELATED WORK

Indoor localization has been a popular research topic in recent years. Numerous door detection solutions have been proposed because doorways often act as useful and important landmarks for indoor localization. To our knowledge, related works of door detection can be roughly divided into three categories: 1) vision based [5], [9], [11], [13], [15], [23], [30], [32], 2) infrastructure based [7], [12], [16], [21], [22], [24], [25], [28], [33], [37]–[40], [42], [43], [45], [46], and 3) infrastructure free [1], [6], [8], [10], [17]–[19], [29], [31], [34], [41].

It is known that the 1) vision based and 2) infrastructure based approaches are both subject to considerable overhead, such as complicated image processing algorithms or expensive infrastructure costs [3], [14], [20]. For example, WiFi fingerprinting based approaches [2], [4] need site survey and WiFi infrastructures [26] in the sensing area. As a result, the 3) infrastructure free approach becomes the focus of our research. With regard to this approach, below we review four recent works that are most relevant to our work.

IndoorAtlas [1], [35], a representative industrial solution, takes advantage of the non-uniform distribution of ambient magnetic fields for indoor positioning. In the training phase, a magnetic distribution map must be established. Next, in the localization phase, by comparing the collected magnetic features with the map, one can obtain the location of a smartphone. As for IndoorAtlas, not only the floor plan of the concerned building is a precondition, but also the workload of site survey is heavy. In our work, the above constrains are released by applying a signal processing algorithm. Moreover, doors are detected in real time without any training phase.

UnLoc [36] is an unsupervised indoor localization approach. It collects time-stamped data from multiple built-in sensors of smartphones and classifies those sensing data as signatures. In UnLoc, some essential structures in a building, such as doors, stairs and elevators, are defined as “Seed Landmarks”, which are significant factors determining the localization accuracy. One of preconditions of those seed landmarks is the floor plan of the building. Without positions of seed landmarks, the accuracy of UnLoc will decrease dramatically. In our approach, the floor plan is not a necessary requirement. Number of doors are calculated by proposed method.

WalkCompass [31] employs the magnetic information and human walk analysis to estimate the direction of human movement. Multiple sensors are used to model the human behaviour. Differently, in this paper we distinguish human actions by analyzing the change patterns of magnetic signals (only from the magnetometer). And our method can generate a sound level of door detection accuracy.

As the magnetic sensor is direction sensitive, Chung et al. [10] design a special sensing device, composed of an array of e-compasses for measuring multi-directional magnetic intensities. By comparing the measurement results with the magnetic distribution map, they are able to obtain the location of the device. In this paper, we only use the off-the-shelf smartphones (rather than special devices), combined with a sophisticated feature analysis algorithm, to detect doors.

# III. METHODOLOGY

LMDD is a door detection approach that only relies on the sensing data from a single smartphone. It utilizes the magnetic field characteristics ( $\S$ III-A) to detect the event of passing through a door. The approach consists of three processes: 1) data acquisition ( $\S$ III-B), 2) signal analysis ( $\S$ III-C), and 3) environmental event cancellation (or denoising) ( $\S$ III-D).

# A. Magnetic Field Characteristics

In general, the magnetic field observed by sensors is a combination of 1) geomagnetic field and 2) ambient magnetic field. The geomagnetic field (i.e., the magnetic field of the earth) often acts as a global reference for orientation detection and navigation. However, modern buildings usually have many electronic and ferromagnetic structures, such as reinforced concrete, electronic sub-systems, and icon furniture. These ambient magnetic fields may well cause geomagnetic anomalies in different areas [10]. In a nutshell, the geomagnetic field is relatively weak in indoor environments.

![](images/1a5ebb00fd9173f688d7e62e582337a12ac4258880bd28a9505ee638517fefb3.jpg)



(a) In a fixed position

![](images/0fbf71d48915d68f765b71ca92c7607539c22b7ecdee678189933c0395902429.jpg)



(b) In a corridor

![](images/7d1385748de2b6a6c11bc71eb1f40d822c64fd369c9cbe6cd202c8e7f5671e48.jpg)



(c) In a corridor with a door   
Fig. 2. Magnetic intensity samples in three situations.

We conduct a series of benchmark experiments using a typical magnetic sensor (Honeywell HMC5883L). First, we measure the magnetic intensity when holding the device in a fixed position. The result is plotted in Fig. 2(a), demonstrating the stability of magnetic intensity in a fixed position. Then, the holder walks along a straight corridor, and the result is shown in Fig. 2(b). In this case, it is hard to identify obvious features from the changes of magnetic intensity. Finally, the holder passes through a door and walks into a corridor, and the result is recorded in Fig. 2(c). Obviously, there is a clear “drop and rise” pattern in Fig. 2(c), which implies the event of passing through a door.

# B. Data Acquisition

Most of today's smartphones contain magnetometers or compasses for providing navigation services. The output of these sensors consists of three vector components in $x$ , $y$ and $z$ axes. It has been reported that a smartphone is in most time horizontally placed [34]. So, when people use smartphones for indoor navigation, the $x$ and $y$ axes compose the horizontal plane and the $z$ axis represents the vertical direction.

A magnetic sample at time t is made up of three components $\{M(x), M(y), M(z)\}$ . Each component represents the reading of an axis. Let M denote the square root of the magnetic fields of all three vectors, so $M = \sqrt{M(x)^{2} + M(y)^{2} + M(z)^{2}}$ . Then, the azimuth angle $\psi$ can be calculated as:

$$
\psi = \arctan \frac {| M (z) |}{\sqrt {M (x) ^ {2} + M (y) ^ {2}}} \tag {1}
$$

Normally, the magnetic sensors are often assembled on the board of a smartphone. During the sensing period, carrying ways of the smartphone are changed frequently. Thus, the spatial posture of the magnetometer must be considered. In addition to the azimuth angle $\psi$ , the pitch angle $\omega$ and the roll angle $\theta$ are introduced to determine the spatial posture. The pitch angle controls the relative elevation between phone and horizontal plane and the roll angle refers to the rotation around the X direction respectively. We can transform the onboard coordinate system (OCS) to the local absolute coordinate system (LACS). All magnetic intensities of our approach are obtained in LACS. Hence, the influence of the spatial posture is limited to a minimum level according to the results of transformation of the coordinate systems. Three components of the magnetic strength in LACS can be derived as follows.

$$
M _ {L} = A _ {\psi} \cdot A _ {\omega} \cdot A _ {\theta} \cdot M _ {O} \tag {2}
$$

where $M_{L}$ represents the magnetic components in LACS and $M_{O}$ represents the magnetic components in the onboard coordinate system respectively. The arrays of three angles are shown as follows.

$$
A _ {\psi} = \left[ \begin{array}{c c c} \cos \psi & \sin \psi & 0 \\ - \sin \psi & \cos \psi & 0 \\ 0 & 0 & 1 \end{array} \right]
$$

$$
A _ {\omega} = \left[ \begin{array}{c c c} 1 & 0 & 0 \\ 0 & \cos \omega & \sin \omega \\ 0 & - \sin \omega & \cos \omega \end{array} \right]
$$

$$
A _ {\theta} = \left[ \begin{array}{c c c} \cos \theta & 0 & - \sin \theta \\ 0 & 1 & 0 \\ \sin \theta & 0 & \cos \theta \end{array} \right] \tag {3}
$$

For simplicity, we still use M to denote the $M_{L}$ in the remaining sections. The magnetic intensity can be calculated from three magnetic components. After the translation from OCS to LACS, the effect of smartphone postures is reduced to the minimum level. Therefore, sensing data traces from different participants have the same evaluation base.

# C. Signal Analysis

LMDD identifies door events in three steps, as plotted in Fig. 3. In the first step (Pre-processing), the modified edge preserving filter is applied to wipe out the Gaussian white noise from raw data. In the second step (Denoising), other noises generated from environmental signals are wiped. In the third step (Feature Definition), we use a Bayes function based on empirical feature classifications to regenerate the signal. After above three steps, the door events can be detected. Let K denote the number of potential doors, N represent the necessary sampling points for detecting a single door (typically between 100 and 200), and $\sigma_{s}$ denote the width of the Gaussian function (typically between 20 and 100), it is easy to prove that the computation complexity of LMDD stays in $O(KN\sigma_{s}^{2})$ . This means that our algorithm only concerns those sharp changes within a short time.

![](images/d3293f82d713b9b71d909a1905ba798b4e4dc5f0c02a9e22ccb5866a7c4fbf2a.jpg)



![](images/64c41de241abb11e25e84d21c06ab7212f36e7e3bebff1dce19d658d6caa5cc3.jpg)



![](images/46da9880f5b434b5998599be93e8dfdc6ad06ecf2836523c395e6504aa6fc299.jpg)



![](images/cddd2dc442eb1cad8d2a55d43cbac663ef9d2a0bbf5459e6615dae1b884e9aed.jpg)



Fig. 3. The outline of denoising procedures.

1) The edge preserving filter: The raw data of magnetic intensity on each axis (say x) collected by a sensor can be represented as

$$
M (x) = M _ {b h} (x) + M _ {n} (x) + M _ {e} (x) \tag {4}
$$

where $M_{bh}$ is the basic harmonic determined by the geomagnetic intensity, $M_{n}$ is the magnetic intensity of noise signal, and $M_{e}$ is the magnetic intensity of environmental signal. $M_{n}(x) + M_{e}(x)$ denotes the intensity of ambient magnetic fields.

The noise signal $M_{n}$ contains sensor noises caused by measurements. We first use empirical values to calibrate the built-in magnetometers. Afterwards, to remove those random measurement noises, we design an edge preserving filter $F[M]_{p}$ (p is a sampling point):

$$
F [ M ] _ {p} = \frac {1}{N _ {p}} \sum_ {q \in S} G _ {\sigma_ {s}} (\| p - q \|) G _ {\sigma_ {r}} (\| M (p) - M (q) \|) M (q) \tag {5}
$$

where $S$ is the linear area centered in $p$ in the $x$ -axis, and $N_{p}$ is the normalization factor

$$
N _ {p} = \sum_ {q \in S} G _ {\sigma_ {s}} (\| p - q \|) G _ {\sigma_ {r}} (\| M (p) - M (q) \|) \tag {6}
$$

Here $G_{\sigma_{s}}$ is a spatial Gaussian kernel and $G_{\sigma_{r}}$ is a range Gaussian kernel. The normal “ $\|\cdots\|$ ” represents the Euclidean distance. Shown in Fig. 4, the spatial Gaussian kernel means the time interval between p and q. Typically, the q is in a range such that $\| p - q \| \leq \sigma_{s}$ . The range kernel gives the difference of magnetic intensities. The parameter $\sigma_{r}$ controls the edge preservation effect. Those kernels can be calculated as follows.

$$
G _ {\sigma_ {s}} (x) = \frac {1}{2 \pi \sigma_ {s} ^ {2}} e x p (- \frac {x ^ {2}}{2 \sigma_ {s} ^ {2}})
$$

$$
G _ {\sigma_ {r}} (y) = \frac {1}{2 \pi \sigma_ {r} ^ {2}} e x p (- \frac {y ^ {2}}{2 \sigma_ {r} ^ {2}}) \tag {7}
$$

where $\sigma_{s}$ and $\sigma_{r}$ are adjustable constants, which are determined by the analysis of empirical results. The spatial parameter $\sigma_{s}$ decides the range features in the time domain, i.e., the width of sampling points. At the same time, the magnetic difference is scaled by $\sigma_{r}$ . The pseudo-code of the filter is illustrated as Algorithm 1.

2) The Bayes function: The change of the environmental signal $M_{e}$ reflects environmental events in two major types: human activities and passive events. Human activities are the phone holder's actions, such as turning around, body shaking, and shaking the phone. They are basically unpredictable. To understand the impact of human activities, detailed feature analysis on signal changes is needed. We use $p_{ea}$ to denote the probability of human activities in all magnetic samples.

On the other hand, passive events represent ambient magnetic changes caused by environmental events, which include the sharp changes in one axis or two axes of the magnetometer. We use $p(d)$ to denote the probability of door event among all passive events. Other passive events may be caused by moving towards metal material or electrical devices. We use $p(\bar{d})$ to denote the probability of other types of passive events. We use $p_{ee}$ to denote the probability of passive events in magnetic samples.

![](images/ff41edaa34df7c8fcd9391f01e1e4d9e8fc316d9fcd5e9f2c815eaa2c1d8e589.jpg)



Fig. 4. The spatial and range Gaussian kernels.

Formally, given the ambient magnetic change, the conditional probability of the door event is calculated as follows:

$$
p (d | e m) = \frac {p (e m | d) \cdot p (d)}{p (e m)} \tag {8}
$$

where $p(em) = p_{ea} + p_{ee}$ is the measurement of all environmental events. $p(em)$ can be calculated as follows:

$$
p (e m) = \sum_ {i = 1} ^ {n} p (e m) _ {i} \tag {9}
$$

$$
p (e m) _ {i} = p (e m _ {i} | d) \cdot p (d) + p (e m _ {i} | \bar {d}) \cdot p (\bar {d}) \tag {10}
$$

where n is the number of distinct environmental events and i is the event index. The parameter $p(em)_{i}$ represents the probability of the i-th event among environmental events. It is difficult to list all possible $p(em)_{i}$ . We only describe three cases. For example, the probability of turn-around events $p(em)_{1}$ is the number of turning around events divided by the number of all environmental events.

Algorithm 1 Edge preserving algorithm $F[M]_p$   
Input: The set of a trace data, $M_{n}$ ; The total number of sampling points, T

Output: The filtered trace, $M_{nn}$ 1) Set a window size S, where $S \leq 2\sigma_{s}$ .

2) For p in T

3) Initialize: $N_{p} = 0$ , $F_{p} = 0$ ;

4) For q from $[p - S/2, p + S/2]$ 5) $m = G_{\sigma_{s}}(\| p - q \|)G_{\sigma_{r}}(\| M(p) - M(q) \|)$ 6) $F_{p} += mM(q)$ 7) $N_{p} += m$ 8) Standardization $M_{nn} = F_{p}/N_{p}$ 9) End For

10) End For

11) Return $M_{nn}$

![](images/c9acead57f35bce29e5d14c495bc31095361c8388f7cc46d362b4823a381b9a4.jpg)



Fig. 5. Changes of magnetic intensities when the holder turns around.

Obviously, $p(em)_{1}$ is a part of $p_{ea}$ , which is caused by human activities. Similarly, the probability of shaking body event $p(em)_{2}$ is the number of shaking body events divided by the number of all environmental events. $p(em)_{2}$ also belongs to the probability $p_{ea}$ . Accordingly, the probability of approaching metals $p(em)_{3}$ is retained in the probability $p_{ee}$ .

We employ $p(d|em)$ as the estimator to determine the door events. If $p(d|em)$ is greater than a given threshold $\varepsilon$ (a constant value based on prior knowledge), a door event is detected. To understand the threshold $\varepsilon$ clearly, below we provide an example. If the door appears after a turn-around event, $\varepsilon$ exceeds the threshold obviously. It means that the door event is very likely to be connected with the turn-around event, since most doors are located in one side of the corridor.

# D. Environmental Event Cancellation (Denoising)

Door event detection results based on signal analysis may involve false positives, due to environmental events that are not essentially related to doors. For more accurately defined features, more detailed signal features of magnetometers need to be investigated. For example, if metal material appears on a side of the sensing area, readings from one axis (x or y) will change (but readings from the z axis are not affected). Signal changes by human activities also have specific patterns. Fig. 5 shows the change pattern of three axes when a man (and the smart phone) makes a $90^{\circ}$ turn. Obviously, the average magnetic intensity almost keeps in the same value, but the values of x-axis and y-axis seem “exchanged”. When the man carrying a smartphone walks slowly and shake their body, the pattern is illustrated as Fig. 6. If the smartphone holder moves to a metal object, the pattern is sketched in Fig. 7.

The features of common environmental events can be formally described. If we define the features with specific functions well, the irregularities and periodic noises like body shaking and turning back can be observed and excluded from event reports. A critical observation lies in that the metal material near the door area only affects one or two plain axes (e.g., x-axis or y-axis) of the magnetometer. Consequently,

![](images/2d385005512edcb4c72236279fcc27f473f7d4b012d8436157e2689312cbfa03.jpg)



Fig. 6. Changes of magnetic intensities when the holder shakes body.

LMDD utilizes the following cross correlative function to search positive activities:

$$
C _ {x y} = \frac {\sum_ {i = 1} ^ {n} (M (x) _ {i} - E (M (x))) (M (y) _ {i} - E (M (y)))}{\sqrt {\sum_ {i = 1} ^ {n} (M (x) _ {i} - E (M (x))) ^ {2} \cdot \sum_ {i = 1} ^ {n} (M (y) _ {i} - E (M (y))) ^ {2}}} \tag {11}
$$

where $E(M(x))$ and $E(M(y))$ are the expected values of magnetic intensity. If $|C_{xy}|$ exceeds a threshold $\xi$ , LMDD will filter this event from the results. Finally, other kinds of environmental events can be identified in a similar way. According to our experiences, the threshold $\xi$ ranges from 0 to 1.0. For highly relevant environmental events, $\xi$ is larger than 0.8. If $\xi$ lies between 0.5 and 0.8, we call those events “correlated events”. In our algorithm, $\xi$ is initialized as 0.7.

# IV. EXPERIMENTAL RESULTS

We have implemented a prototype system of LMDD on top of multiple popular Android phones, including Google Nexus5, Sumsang Galaxy S4, HTC One M8, Huawei Ascend P7, Sony Xperia Z2, XiaoMi M2S, and Meizu MX. Using this prototype system, we conduct real-world experiments in four typical environments, including offices, classrooms, residential houses, and a hospital. The experiments involve 50 volunteers who live, work, or study in the four environments. More than 1800 experiments are conducted in three months.

# A. Devices

First of all, we calibrate the magnetometer of every experimental smartphone with an external high-precision magnetic sensor (i.e., Honeywell HMC5883L is magneto-resistive and its precision can reach 5 milli-gauss). For commercial smart phones, the resolution is normally in $\mu t$ level. After calibration, each smart phone has own linear compensation of errors. According to our experiment experiences, at least 20 samples are required for detecting the event of passing through a door. Besides, in most cases, we observe that a person passes through a door in two seconds. To avoid unnecessary complexity, the sampling rate is configured as 50 Hz in our study.

![](images/f1f5416045a05b4d2ef00dda0826d943fdcf0d59afb3bc806dd724b292e7ab12.jpg)



Fig. 7. Changes of magnetic intensities when the holder closes to metals.

A prototype of LMDD is developed as an Android application. Sensing data are temporarily stored in smartphones and uploaded to a cloud (e.g., Amazon EC2) server. For real-time applications, the cloud server executes the LMDD algorithm and sends the result back to smartphones. On the other side, for delay-tolerant applications, the results are returned after collecting sufficient data, so as to guarantee a certain level of accuracy.

# B. Environments

We select four typical environments to examine the real-world performance of LMDD, including offices, classrooms, residential houses and a hospital:

- The hospital environment is the most complex one. Most of doors in the hospital are made by metallic material, and the equipments inside each room are different. The metallic doors in the hospital are demonstrated in Fig. 9. In general cases, those doors are always open. Therefore, the “open-close” action is not a necessary activity. When people enter those doors, the magnetic strength will still have a severe change. The complex electronic devices in diagnostic chambers also interfere the magnetic strength. According to the proposed algorithm, those changes can give hints about crossing doors.   
- In the classroom environment, the room arrangement is not regular. Therefore, directions of doors are diverse. The furniture (mainly wooden desks and chairs) in each classroom contains little metallic material. We test LMD-D in classrooms of two buildings in our university. The Fig. 10 elucidates the environment of classrooms. Those doors contain metallic frames and knobs, which can interfere the magnetic signals.   
- In the office environment, doors are symmetrically distributed along a corridor. All the walls in the office building (including reinforced concrete walls and hollow walls) contain metallic material. The distributions of magnetic density in this environment are regular. Showed in Fig. 11, wooden doors contain metallic doorknobs and other metalliferous accessories.   
- The area of a typical residential house is much smaller,

![](images/d5b94a9571813a8cce69aeb506cd4d6c5741e9bfb56c2ab974382118ec066adb.jpg)



(a) The floor plan of offices

![](images/2dfdd50afb8be93ee7d37d6054d846ce5ce1f72611b38d12f5738591639b3114.jpg)



(b) The floor plan of classrooms

![](images/da62341e728e6d771cfefaa7ff11c04a31f9393a4bdd522aeb697b3db6aae370.jpg)



(c) The floor plan of the house

Fig. 8. Floor plans of the experimental environments (excluding the hospital).   
![](images/7b7bac748ce6e568525cecc17acd4f0d979dfc496b26693268515e364c282c4b.jpg)



Fig. 9. The environment of the hospital.

![](images/7bc7af95892fb89085597eb1dfefbddaf927445ae84b4b0f549360bc4eb9bec8.jpg)



Fig. 10. Doors of classrooms.

![](images/cb061688af67607f448f843dd66d862470d8bf7b4b665c97fa27cd7d5a3cc012.jpg)



Fig. 11. Doors of offices.

but the ambient magnetic fields are more complex due to the multifarious furniture. The distribution of magnetic signals inside the residential house is unpredictable. Therefore, the precision of the denoising procedure is lower than previous environments. The detection of doors is more difficult.

The floor plans of the office, classroom and residential house environments are illustrated in Fig. 8. Although the floor plan of the hospital is complicated and not demonstrated here, our LMDD works in hospital environment, since fundamental elements are similar with other environments, such as passageways, stairs and rooms. The precision of identifications is even higher than other environments due to metallic doors.

# C. Results

More than 1800 traces (corresponding to over 1800 experiments) have been collected. Most of them include more than 100 door events. In order to comprehensively evaluate the performance of LMDD, in this part we first define the detection accuracy, and then discuss how the detection accuracy is affected by various impact factors.

1) Detection accuracy: We utilize three types of prediction rates: true positive (TP), false positive (FP) and false negative (FN). A TP event is a correct rate to detect door events. An

TABLE I
ACCURACY OF LMDD IN FOUR ENVIRONMENTS 

<table><tr><td>Environment</td><td>TP</td><td>FP</td><td>FN</td><td>Accuracy</td></tr><tr><td>Office</td><td>59%</td><td>10%</td><td>31%</td><td>66%</td></tr><tr><td>Classroom</td><td>61%</td><td>19%</td><td>20%</td><td>75%</td></tr><tr><td>Residential house</td><td>59%</td><td>18%</td><td>23%</td><td>71%</td></tr><tr><td>Hospital</td><td>70%</td><td>19%</td><td>11%</td><td>85%</td></tr></table>

FP is a wrongly reported door event by LMDD. An FN rate is a missed door case by LMDD.

$$
T P = \frac {\sum_ {j = 1} ^ {n} N _ {d j}}{N _ {a}}
$$

$$
F P = \frac {\sum_ {j = 1} ^ {n} N _ {p j}}{N _ {a}}
$$

$$
F N = \frac {\sum_ {j = 1} ^ {n} N _ {f j}}{N _ {a}} \tag {12}
$$

where j is the environment number. $N_{dj}$ represents the number of detected doors in $j_{th}$ environment. $N_{pj}$ is the number of false positive events. $N_{fj}$ denotes the number of missing doors in $j_{th}$ environment. $N_{a}$ is the total number of events.

![](images/307460f125db75dd2b8280f636a6325349010041b0eb238af42f7c20a90768dd.jpg)



Fig. 12. Performance comparison between LMDD and UnLoc.

Finally, the true positive accuracy is defined as follows:

$$
A c c u r a c y _ {t y r} = N _ {T P} / \left(N _ {T P} + N _ {F N}\right) = \frac {\sum_ {j = 1} ^ {n} N _ {d j}}{\sum_ {j = 1} ^ {n} \left(N _ {d j} + N _ {f j}\right)} \tag {13}
$$

The accuracy for all cases can also be obtained.

$$
A c c u r a c y _ {a c} = (N _ {T P} + N _ {T N}) / (N _ {P} + N _ {N}) \tag {14}
$$

where TN is the true negative events. $N_{N}$ is the total rates of negatives. $N_{P}$ is the total rates of positives. The TN is unpredictable parameter, since most of raw data are negatives for a door. Therefore, the $Accuracy_{ac}$ is difficult to calculate correctly. We use the $Accuracy_{tpr}$ as the accuracy of our algorithm.

The detailed accuracy results are listed in Table I. Each item is the average value aggregated from all experiments. LMDD achieves the highest accuracy (85%) in the hospital and the lowest accuracy (66%) in offices. The overall average detection accuracy is 74%, which is basically a sound accuracy to effectively detect doors. Besides, we compare the detection accuracy of LMDD with that of UnLoc, a representative unsupervised indoor localization algorithm that is most similar to LMDD among related works. The comparison results are shown in Fig. 12. Obviously, LMDD outperforms UnLoc.

2) Impact factors: Below we investigate four kinds of impact factors that may affect the performance of LMDD.

Human behavior: The user's habits and carrying motions of a smartphone are also important influential factors. In our experiments, most participants hold smartphones horizontally, and thus the data collected from these participants generate higher detection accuracy. Otherwise, the detection accuracy is generally decreased by $6\% - 14\%$ . Another situation is that a crowd of people cross a door simultaneously. Since the human body can influence the local magnetic strength, the precision of LMDD will decrease within a certain scope. If two or more persons simultaneously pass through a door, the magnetic signals may interfere with each other. To solve this problem, more sensing data are required by LMDD for eliminating unwanted signals.

![](images/5b11204fc85504adbca27610bdef595e931a6934c3302743e936bee6d517ef8b.jpg)



Fig. 13. The different performances for the opened door and the closed door.

TABLE II
THE POWER CONSUMPTION (MW) OF SENSORS 

<table><tr><td>Parts</td><td>Average</td><td>Maximum</td><td>Minimum</td></tr><tr><td>Android system</td><td>151.9</td><td>215.6</td><td>88.2</td></tr><tr><td>Megnetometer</td><td>49</td><td>112.7</td><td>24.5</td></tr><tr><td>WiFi</td><td>147</td><td>245</td><td>122.5</td></tr><tr><td>Gyro., Acc. and Light</td><td>58.8</td><td>49</td><td>73.5</td></tr></table>

Status of doors: Doors normally have two statuses: opened or closed (for some cases, the door is semi-opened. We consider that the semi-opened state is similar with the opened state, which means people can go through doors without any stop.) On the contrary, when a person passed a closed door, he must stop and open the door. During this process, the built-in sensors, such as gyroscope, accelerometer and compass, will have a combination readings. For example, an obvious stop following a speedup process can be defined as a “closed door event”. Fig. 13 shows the difference between a “closed door event” and a “opened door event”. For the “closed door event”, the speed of magnetic intensity changes is slower than the “opened door event”. Meanwhile, the trend of magnetic strengths for the “closed door event” case is more complicated than the trend for the “opened door event” case.

Door type: The material of a door has critical influence on the decision of a door event. In our experiments, different types of doors appear in four environments. The corresponding values of TP, FP and FN of different door types are shown in Fig. 14. From this figure, we can find that it is easiest to detect metallic doors, followed by wooden doors. Glass doors are the most difficult to detect. The reason is intuitive: a glass door contains little metal material except in its frames.

Power consumption: Built-in sensors consume the energy of smartphones. To estimate the energy consumption, we evaluate the usage of sensors when they are switch off separately. Table II reveals the power consumptions of different parts. The average consumption is derived from 100 power measurements during 10 minutes. In this interval, the energy costs are various. The maximum and minimum power consumptions are considered. It is obvious that the magnetometer only use a small number of energies. Meanwhile the gyroscope, accelerometer and light sensor also spend little power. As a basic component, the Android system consumes a high amount of energy (about 30%). WiFi is another main consumer especially in the working mode. LMDD only utilizes one sensor, therefore the energy usage is limited even in the case of a high sampling rate.

![](images/085723a73abd179920b45340140a615f23cdd8a118c54312fb2fab37d537e13b.jpg)



Fig. 14. Impact of door types.

# V. CONCLUSION

Doors are important landmarks for indoor positioning systems. An accurate and light-weight door detection approach is therefore highly desired. In this paper, we observe special change patterns of magnetic signals when carrying a smartphone to pass through a door. Based on this observation, we design a light-weight, infrastructure-free door detection approach (named LMDD) running on a single smartphone. A signal analysis algorithm combined with a feature correlation function is designed to capture door events. Prototype experiments in various typical environments show that LMDD achieves sound door detection accuracy. We believe that our proposed door detection method would significantly benefit indoor positioning systems.

# VI. ACKNOWLEDGEMENTS

This research is supported by the NSF China Major Program No. 61190110, the High-Tech Research and Development Program of China (“863 China Cloud” Major Program) No. 2015AA01A201, the NSF China Distinguished Young Scholars Program No. 61125202, NSF China Projects No. 61272429, 61471217 and 61472098, China Postdoctoral Science Foundation funded Projects No. 2012M510454 and 2014M550735, University of Kentucky College of Engineering Faculty Startup Grant and NSF (US) Project No. CNS-1464335.

# REFERENCES

[1] Indooratlas indoor positioning system. http://www.indooratlas.com.   
[2] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller. ArrayTrack: A Fine-Grained Indoor Location System. In Proceedings of the 10th USENIX Symposium on Networked Systems Design and Implementation (NSDI 13), pages 71–84. USENIX, 2013.

[3] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller. 3D Tracking via Body Radio Reflections. In Proceedings of the 11th USENIX Symposium on Networked Systems Design and Implementation (NSDI 14), pages 317–329. USENIX, 2014.   
[4] F. Adib and D. Katabi. See through walls with WiFi! In Proceedings of Special Interest Group on Data Communication (SIGCOMM), pages 75–86. ACM, 2013.   
[5] D. Anguelov, D. Koller, E. Parker, and S. Thrun. Detecting and Modeling Doors with Mobile Robots. In Proceedings of International Conference on Robotics and Automation (ICRA), pages 3777–3784. IEEE, 2004.   
[6] M. Azizyan, I. Constandache, and R. R. Choudhury. Surroundsense: Mobile Phone Localization via Ambience Fingerprinting. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 261–272. ACM, 2009.   
[7] P. Bahl and V. Padmanabhan. RADAR: An In-building RF based User Location and Tracking System. In Proceedings of International Conference on Computer Communication (INFOCOM), pages 775–784. IEEE, 2000.   
[8] J. Blankenbach and A. Norrdine. Position Estimation using Artificial Generated Magnetic Fields. In Proceedings of International Conference on Indoor Positioning and Indoor Navigation (IPIN), pages 1–5. IEEE, 2010.   
[9] C. Chen and Y. Tian. Door Detection via Signage Context-based Hierarchical Compositional Model. In Proceedings of Conference on Computer Vision and Pattern Recognition (CVPR), pages 1–6. IEEE, 2010.   
[10] J. Chung, M. Donahoe, C. Schmandt, I. Kim, P. Razavai, and M. Wiseman. Indoor Location Sensing Using Geo-magnetism. In Proceedings of International Conference on Mobile Systems, Applications, and Services (MobiSys), pages 141–154. ACM, 2011.   
[11] S. K. Divvala, D. Hoiem, J. H. Hays, A. A. Efros, and M. Hebert. An Empirical Study of Context in Object Detection. In Proceedings of Conference on Computer Vision and Pattern Recognition (CVPR), pages 1271–1278. IEEE, 2009.   
[12] R. Gao, M. Zhao, T. Ye, F. Ye, Y. Wang, K. Bian, T. wang, and X. Li. Jigsaw: Indoor Floor Plan Reconstruction via Mobile Crowdsensing. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 249–260. ACM, 2014.   
[13] J. Hensler, M. Blaich, and O. Bittel. Real-Time Door Detection Based on AdaBoost Learning Algorithm. Research and Education in Robotics - EUROBOT, 82:61–73, 2010.   
[14] Y. Jiang, Y. Xiang, X. Pan, K. Li, Q. Lv, R. P. Dick, L. Shang, and M. Hannigan. Hallway based Automatic Indoor Floorplan Construction using Room Fingerprints. In Proceedings of International Conference on Ubiquitous Computing (UbiComp), pages 315–324. ACM, 2013.   
[15] Y. Kou, P. Pannuto, K. J. Hsiao, and P. Dutta. Luxapose: Indoor Positioning with Mobile Phones and Visible Light. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 447–458. ACM, 2014.   
[16] T. Kubo, A. Tagami, T. Hasegawa, T. Hasegawa, and J. C. Walrand. Range-free Localization using Grid Graph Extraction. In Proceedings of International Conference on Network Protocols (ICNP), pages 1–11. IEEE, 2012.   
[17] S. Kumar, S. Gil, D. Katabi, and D. Rus. Accurate Indoor Localization With Zero Start-up Cost. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 483–494. ACM, 2014.   
[18] W. Kwon, K. S. Roh, and H. K. Sung. Particle Filter-based Heading Estimation using Magnetic Compasses for Mobile Robot Navigation. In Proceedings of International Conference on Robotics and Automation (ICRA), pages 2705–2712. IEEE, 2006.   
[19] B. Li, T. Gallagher, A. G. Dempster, and C. Rizos. How Feasible is the Use of Magnetic Field Alone for Indoor Positioning? In Proceedings of International Conference on Indoor Positioning and Indoor Navigation (IPIN), pages 1–9. IEEE, 2012.   
[20] L. Li, P. Hu, C. Peng, G. Shen, and F. Zhao. Epsilon: A Visible Light Based Positioning System. In Proceedings of the 11th USENIX Symposium on Networked Systems Design and Implementation (NSDI 14), pages 331–343. USENIX, 2014.   
[21] L. Li, G. Shen, C. Zhao, T. Moscibroda, J. Lin, and F. Zhao. Experiencing and Handling the Diversity in Data Density and Environmental Locality in an Indoor Positioning Service. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 459–470. ACM, 2014.

[22] A. Mariakakis, S. Sen, J. Lee, and K. Kim. SAIL: Single Access Point based Indoor Localization. In Proceedings of International Conference on Mobile Systems, Applications, and Services (MobiSys), pages 315-328. ACM, 2014.   
[23] A.C. Murillo, J. Kosecka, J.J. Guerrero, and C. Sagues. Door Detection in Images Integrating Appearance and Shape Cues. In Proceedings of International Conference on Intelligent Robots and Systems (IROS), pages 41–48. IEEE/RSJ, 2007.   
[24] L. M. Ni, Y. Liu, Y. Lau, and P. Abhishek. LANDMARC: Indoor Location Sensing using Active RFID. In Proceedings of International Conference on Pervasive Computing and Communications (PerCom), pages 407–415. IEEE, 2003.   
[25] S. Nirjon, J. Liu, G. DeJean, B. Priyantha, Y. Jin, and T. Hart. COIN-GPS: Indoor Localization from Direct GPS Receiving. In Proceedings of International Conference on Mobile Systems, Applications, and Services (MobiSys), pages 301–314. ACM, 2014.   
[26] R. Ouyang, A. Srivastava, P. Prabahar, R. Choudhury, M. Addicott, and F. McClernon. If You See Something, Swipe towards It: Crowdsourced Event Localization Using Smartphones. In Proceedings of International Conference on Ubiquitous Computing (UbiComp), pages 23–32. ACM, 2013.   
[27] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen. Zee: Zero-Effort Crowdsourcing for Indoor Localization. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 293–304. ACM, 2012.   
[28] J. Ranjan, Y. Yao, and K. Whitehouse. An RF Doormat for Tracking People's Room Locations. In Proceedings of International Conference on Ubiquitous Computing (UbiComp), pages 797–800. ACM, 2013.   
[29] G. Retscher. Test and Integration of Location Sensors for a Multi-sensor Personal Navigator. Journal of Navigation, 60:107–117, 2007.   
[30] M. Rous, H. Lupschen, and K.-F. Kraiss. Vision-based Indoor Scene Analysis for Natural Landmark Detection. In Proceedings of International Conference on Robotics and Automation (ICRA), pages 4642-4647. IEEE, 2005.   
[31] N. Roy, H. Wang, and R. R. Choudhury. I am a Smartphone and I can Tell my Users Walking Direction. In Proceedings of International Conference on Mobile Systems, Applications, and Services (MobiSys), pages 350–363. ACM, 2014.   
[32] R. M. Salinas, E. Aguirre, M. G. Silvente, and A. Gonzales. Door Detection using Computer Vision and Fuzzy Logic. Transactions on Systems, 10(3):3047–3054, 2004.   
[33] L. Shangguan, Z. Yang, Z. Zhou, X. Zheng, C. Wu, and Y. Liu. CrossNavi: Enabling Real-time Crossroad Navigation for the Blind with Commodity Phones. In Proceedings of International Conference on Ubiquitous Computing (UbiComp), pages 105–113. ACM, 2014.   
[34] K. P. Subbu, B. Gozick, and R. Dantu. LocateMe: Magnetic-fields-based Indoor Localization using Smartphones. Transactions on Intelligent Systems and Technology (TIST), 4(4):73:1–73:27, 2013.   
[35] I. Vallivaara, J. Haverinen, A. Kemppainen, and J. Roning. Magnetic Field based SLAM Method for Solving the Localization Problem in Mobile Robot Floorcleaning Task. In Proceedings of International Conference on Advanced Robotics (ICAR), pages 198–203. IEEE, 2011.   
[36] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury. No Need to War-drive: Unsupervised Indoor Localization. In Proceedings of International Conference on Mobile Systems, Applications, and Services (MobiSys), pages 197–210. ACM, 2012.   
[37] X. Wang, Y. Liu, Z. Yang, J. Liu, and J. Luo. ETOC: Obtaining Robustness in Component-based Localization. In Proceedings of International Conference on Network Protocols (ICNP), pages 62–71. IEEE, 2010.   
[38] X. Wang, J. Luo, S. Li, D. Dong, and W. Cheng. Component Based Localization in Sparse Wireless Ad Hoc and Sensor Networks. In Proceedings of International Conference on Network Protocols (ICNP), pages 288–297. IEEE, 2008.   
[39] C. Wu, Z. Yang, Y. Liu, and W. Xi. WILL: Wireless Indoor Localization without Site Survey. In Proceedings of International Conference on Computer Communication (INFOCOM), pages 64–72. IEEE, 2012.   
[40] J. Xiao, Y. Yi, L. Wang, H. Li, Z. Zhou, K. Wu, and L. M. Ni. NomLoc: Calibration-Free Indoor Localization with Nomadic Access Points. In Proceedings of International Conference on Distributed Computing Systems (ICDCS), pages 587–596. IEEE, 2014.   
[41] H. Xie, T. Gu, X. Tao, H. Ye, and J. Lv. MaLoc: A Practical Magnetic Fingerprinting Approach to Indoor Localization using Smartphones. In Proceedings of International Conference on Ubiquitous Computing (UbiComp), pages 30–38. ACM, 2014.

[42] Z. Yang, C. Wu, and Y. Liu. Locating in Fingerprint Space: Wireless Indoor Localization with Little Human Intervention. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 269–280. ACM, 2012.   
[43] Q. Ye, J. Cheng, H. Du, X. Jia, and J. Zhang. A Matrix-Completion Approach to Mobile Network Localization. In Proceedings of International Symposium on Mobile Ad Hoc Networking and Computing (MobiHoc), pages 327–336. ACM, 2014.   
[44] Y. Zhao. Mobile Phone Location Determination and Its Impact on Intelligent Transportation Systems. Transactions on Intelligent Transportation Systems (ITS), 1(1):55–64, 2000.   
[45] Y. Zhao, L. M. Ni, and Y. Liu. VIRE: Active RFID-based Localization Using Virtual Reference Elimination. In Proceedings of International Conference on Parallel Processing (ICPP), pages 56–63. IEEE, 2007.   
[46] Y. Zheng, G. Shen, L. Li, C. Zhao, M. Li, and F. Zhao. Travi-Navi: Self-deployable Indoor Navigation System. In Proceedings of International Conference on Mobile Computing and Networking (MobiCom), pages 471–482. ACM, 2014.