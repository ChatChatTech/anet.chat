# STPP: Spatial-Temporal Phase Profiling-Based Method for Relative RFID Tag Localization

Longfei Shangguan, Student Member, IEEE, ACM, Zheng Yang, Member, IEEE, ACM, Alex X. Liu, Member, IEEE, Zimu Zhou, Student Member, IEEE, ACM, and Yunhao Liu, Fellow, IEEE

Abstract— Many object localization applications need the relative locations of a set of objects as oppose to their absolute locations. Although many schemes for object localization using radio frequency identification (RFID) tags have been proposed, they mostly focus on absolute object localization and are not suitable for relative object localization because of large error margins and the special hardware that they require. In this paper, we propose an approach called spatial-temporal phase profiling (STPP) to RFID-based relative object localization. The basic idea of STPP is that by moving a reader over a set of tags during which the reader continuously interrogating the tags, for each tag, the reader obtains a sequence of RF phase values, which we call a phase profile, from the tag’s responses over time. By analyzing the spatial-temporal dynamics in the phase profiles, STPP can calculate the spatial ordering among the tags. In comparison with prior absolute object localization schemes, STPP requires neither dedicated infrastructure nor special hardware. We implemented STPP and evaluated its performance in two real-world applications: locating misplaced books in a library and determining the baggage order in an airport. The experimental results show that STPP achieves about 84% ordering accuracy for misplaced books and 95% ordering accuracy for baggage handling. We further leverage the controllable reader antenna and upgrade STPP to infer the spacing between each pair of tags. The result shows that STPP could achieve promising performance on distance ranging.

Index Terms— Communication technology, wireless communication, wireless networks.

# I. INTRODUCTION

# A. Motivation

M ANY object localization applications need the relativelocations of a set of objects as oppose to their absolute locations of a set of objects as oppose to their absolute locations. The relative location of an object in a set of objects

Manuscript received October 27, 2015; revised May 28, 2016; accepted July 4, 2016; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor S. Chen. This work was supported in part by the National Natural Science Foundation of China (NSFC) through the General Program under Grant 61522110, in part by the Jiangsu Future Internet Program under Grant BY2013095-4-08, and in part by NSFC through the Major Program under Grant 61190110. Parts of this paper have been reported at USENIX NSDI 2015 [26]. (Corresponding authors: Zheng Yang and Alex X. Liu.)

L. Shangguan, Z. Yang, and Y. Liu are with the School of Software, Tsinghua University, Beijing 100084, China (e-mail: shanggdik@gmail.com; yang@greenorbs.org; yunhao@greenorbs.org).

A. X. Liu is with the Computer Science and Engineering Department, Michigan State University, East Lansing, MI 48824-1226 USA (e-mail: alexliu@cse.msu.edu).

Z. Zhou is with the Electrical Engineering Department, Swiss Federal Institute of Technology Zurich, Zürich 8092, Switzerland (e-mail: zimu.zhou@tik.ee.ethz.ch).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TNET.2016.2590996

refers to the order of the object with respect to other objects along each dimension. The absolute location of an object refers to its coordinate value in each dimension. For example, in a library, to find misplaced books, we need to obtain the current order of the books on shelves rather than their absolute coordinate values.

# B. Limitations of Prior Art

Although many schemes for object localization using Radio Frequency Identification (RFID) tags have been proposed [17], [20], [29]–[31], [35], they mostly focus on absolute object localization. They are not suitable for relative object localization because of two reasons. First, as the error margin achieved by most absolute object localization schemes (e.g., [17], [20], [30]) is still large, sorting objects based on their absolute coordinate values may not result in the correct ordering of all objects because the distance between two objects may be less than the error margin. For example, the state-of-the-art absolute object localization scheme PinIt achieves an accuracy of 16cm at the 90th percentile [30]; however, such an error margin of 16cm could allow a book to be incorrectly ordered several books away from its correct order on a bookshelf. Second, the absolute object localization schemes that can achieve small error margins require either dedicated hardware (such as USRP) [30] or multiple predeployed antennas as reference points [31], [35], which make them relatively harder and more expensive to deploy in practice. For example, the state-of-the-art scheme Togoram [35] can achieve millimeter localization accuracy; however, it relies on the collaboration of multiple reader antennas and requires sophisticated calibration process before putting into use.

# C. Proposed Approach

In this paper, we propose an approach called Spatial-Temporal Phase Profiling (STPP) to RFID based relative object localization. STPP uses commercial off-the-shelf (COTS) RFID readers and passive tags and requires no pre-deployed infrastructure. The basic idea of STPP is that by carefully moving an RFID reader over a set of tags during which the reader continuously interrogating the tags, for each tag, the reader obtains a sequence of RF phase values, which we call a phase profile, from the tag’s responses over time. As a reader moves closer to (or further away from) a tag, the phase value that the reader obtains from interrogating the tag changes. Thus, the phase profile of each tag corresponds to the spatial changes of the reader with respect to the tag. By analyzing the temporal dynamics in the phase profiles of a set of tags, the reader can obtain the spatial ordering among the tags. Specifically, STPP is based on the observation that as we move the reader along a dimension in one direction, for any tag, its distance to the reader first decreases and then increases, and becomes the minimum when the reader is perpendicular above the tag along that dimension; in other words, the distance values are symmetric around the minimum distance. Thus, in this reader moving process, if the reader continuously interrogate the tag, the phase values that reader can measure from the tag responses are also symmetric around the perpendicular point. Based on the symmetry in this observation, by moving the reader along a dimension in one direction, we can determine the order that the tags become perpendicular with the reader along that dimension, which is the order of the tags. Furthermore, by moving the reader two times, each time along a different dimension in the two dimensional space, the reader can obtain the order of the tags along each dimension. Note that an equivalent way of moving the reader while keeping the tags stationary is to move the tags altogether (with the relative positions among tags preserved) while keeps the reader stationary. For example, for airport baggage handling systems, we can keep the reader stationary while the baggages move on a conveyor belt. Therefore, our relative localization scheme can handle applications in both tag moving and antenna moving cases.

This paper focuses on relative object localization in a two dimensional space $( i . e .$ , locating the relative order of tags on a plane). The straightforward solution to achieve this is to move the reader two times, each time along a different dimension in the two dimensional space. In this paper, we propose to achieve two dimensional object localization by moving the reader only once along any dimension. This is based on our observation that given a sequence of objects aligned along a dimension, as we move the reader along that dimension in one direction, the larger the distance between the reader moving trajectory and that dimension, which are in parallel, the smaller the phase changes as the reader moves. Thus, given a set of objects placed within $x _ { 1 }$ and $x _ { 2 }$ (where $x _ { 1 } \leq x _ { 2 }$ along the X dimension) and within $y _ { 1 }$ and $y _ { 2 }$ (where $y _ { 1 } \le y _ { 2 }$ along the Y dimension) as shown in Figure 1, if we move the reader along the X dimension from $x _ { 1 }$ to $x _ { 2 }$ perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $( x _ { 2 } , y _ { 2 } )$ , objects with smaller values on the $Y$ dimension will have smaller phase changing rate; similarly, if we move the reader along the X dimension from $x _ { 1 }$ to $x _ { 2 }$ perpendicularly above the line from $( x _ { 1 } , y _ { 1 } )$ to $( x _ { 2 } , y _ { 1 } )$ , objects with larger values on the Y dimension will have smaller phase changing rate. Based on this observation, by moving the reader along the X dimension from $x _ { 1 }$ to x2 perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $( x _ { 2 } , y _ { 2 } )$ (or the line from $( x _ { 1 } , y _ { 1 } )$ to $( x _ { 2 } , y _ { 1 } ) )$ , we can determine the order of the objects along the Y dimension for any point on the X dimension, in addition to obtaining the order of the objects along the X dimension; in other words, we can determine the relative location of all objects in the two dimensional region.

Our STPP approach achieves relative object localization without calculating the absolute coordinate values of tags. It has two key features in comparison with prior absolute object localization schemes. First, STPP requires no dedicated infrastructure. In contrast, prior RFID based object localization schemes (e.g., [17], [30]) often require dedicated infrastructure such as carefully deployed anchor tags or antennas as reference points. Second, STPP uses COTS RFID readers and tags, and requires no special hardware. In contrast, prior RFID based object localization schemes (e.g., [29]) often require special hardware such as USRP.

![](images/f2aa280ddd14c1bedcb85545e460e026f496bd1b56c9c0bd94e956c129dbca43.jpg)



Fig. 1. Illustration of STPP approach.

# D. Technical Challenges and Solutions

There are three key technical challenges in building a relative object localization system using our STPP approach. The first challenge is to achieve high accuracy. In STPP, phase profiles often come with noises and missing data points due to multi-path self-interference [38], which makes finding the perpendicular point for each tag challenging. To address this challenge, in this paper, we first acquire the symmetric part of each phase profile, which we call a V-zone. Within the V-zone of each phase profile, we further perform quadratic fitting on the incomplete phase values to complete the profile.

The second challenge is to achieve high robustness. As the mobile reader is often moved manually, the phase profile will be stretched when the movement slows down or compressed when the movement speeds up. To address this challenge, we use the Dynamic Time Warping (DTW) technique to find the V-zone within each phase profile. DTW compresses or stretches the profiles with the goal of minimizing the distance between these profiles. It naturally compensates for the warps of phase profiles and is robust to varying reader moving speed.

The third challenge is to achieve low latency. The time warping distance is calculated using dynamic programming algorithm in $O ( M N )$ time complexity, where M and N are the lengths of a phase profile and its reference phase profile, respectively. This process can take time, especially for long phase profiles. Furthermore, as there are typically a large number of tags for localization, $e . g .$ , in a library there are millions of books, detecting the V zone for each tag’s profile would incur large computational overhead. To address this challenge, we perform DTW on the coarser grained representation of phase profiles. Specifically, given a phase profile with length M , we first split it into $\textstyle { \frac { \mathbf { \bar { \boldsymbol { M } } } } { w } }$ w segmentations where each segment is of length w. In each segmentation, we record its maximum and minimum phase values, as well as the start and end points of this segment on the phase profile. After the segmentation, this coarser grained phase profile is used for V zone detection. Using segmentation, we thus can reduce the time complexity of DTW from O(M N ) down to $\begin{array} { r } { O ( \frac { M } { w } \frac { N } { w } ) = O ( \frac { M N } { w ^ { 2 } } ) } \end{array}$ .

# E. Key Contributions

This paper presents the first study of relative object localization. Specifically, we make three key contributions in this paper. First, we propose the concept of spatial-temporal phase profiling, which can be used for RFID based relative object localization. Second, we propose algorithms to capture the spatial-temporary dynamics of RF phase profiles and algorithms to determine the tag order along each dimension. Third, we implemented STPP and evaluated its performance in two real-world applications: locating misplaced books in a library and determining the baggage order in an airport. The experimental results show that we achieve about 84% ordering accuracy for misplaced books and 95% ordering accuracy for baggage handling.

The rest of this paper proceeds as follows. In Section II, we discuss the difficulties on relative localization and the concept of spatial-temporal phase profiling (STPP). In Section III, we present the design details of our STPP based relative localization system. In Section IV, we present the evaluation results of our system. In Section V, we present our findings in deploying our system in two real-world applications. In Section VII, we review related work. We conclude this paper in Section VIII.

# II. SPATIAL-TEMPORAL PHASE PROFILING

In this section, we first discuss the difficulties that we experienced in our initial attempts to directly use the information that can be measured by commercial readers towards relative localization. Then, we introduce the concept of phase profiling and show how it can capture the spatialtemperal phase dynamics that helps us to achieve relative localization.

# A. Initial Attempts

As an RFID reader sweeps over a set of tags and keeps querying them, the reader can obtain the following information that can be impacted by the changes in the spatial relationship between the tags and the readers: tag identification order, the Received Signal Strength Indication (RSSI), and the received signal phase value. We next explain the reasons that we did not use these three types of information for relative localization.

Tag Identification Order: The Class1 Generation2 (C1G2) RFID standard [4] specifies two tag identification protocols: frame slotted ALOHA [3] and tree walking [16]. Unfortunately, in both protocols, the order that the tags are identified does not correspond to the order that the reader moves across them. In frame slotted ALOHA, the identification order depends on the random numbers that tags choose by themseleves. In tree walking, the order depends on the IDs stored in the tags.

![](images/5d155a872af1183bead1b948193f0640348770df1b73c09ce82fb2df9ee51b4f.jpg)



(a)

![](images/e12cde47d56a807112341c7aed2ede4cb2efcf949d4c87a8279aa3f05d5b9e51.jpg)



(b)   
Fig. 2. RSSI values measured over time for two tags. (a) Experiment setup. (b) RSS trends.

RSSI: RSSI measures the power of received radio signal, which is inverse proportional to the distance between the tag and the reader (more precisely, the reader antenna) [11]. As a reader moves across a set of tags, for each tag, the RSSI values measured by the reader should increase and then decrease because the distance between the tag to the reader first decreases and then increases; thus, by ordering the tags according to the time that their peak RSSI values appear, the reader obtains the order of the tags along the moving direction. Unfortunately, this works only in theory because of the multiple paths that the signal traverses. To evaluate the multi-path impact, we conducted an experiment by attaching tags to the books on a shelf and moving the reader from left to right as shown in Figure 2(a). Figure 2(b) shows the RSSI values that the reader measures over time for two tags labeled 01 and 02, where tag 01 is placed 13cm to the left of tag 02. The left and right vertical lines corresponds to the time that the reader passes through tag 01 and 02, respectively. From this figure, we first observe that for both tags, their RSSI values fluctuate and their peak RSSI values appear before the reader moves across them. Second, the order of the two tags based on the time that their peak RSSI values appear is inconsistent with the actual tag order.

RF Phase Values: Phase is a basic attribute of a signal along with amplitude and frequency. The phase value of an RF signal describes the degree that the received signal is offset from sent signal, ranging from 0 to 360 degrees. Let l be the distance between the reader antenna and the tag, the signal traverses a round-trip (2l) in each backscatter communication. Apart from the RF phase rotation over the distance, both the antenna and the tag will introduce additional phase distortion. Specifically, let $\theta _ { T x } , \theta _ { T A G }$ , and $\theta _ { R x }$ be the phase rotation introduced by the reader’s transmission circuit, the tag’s reflection characteristic, and the reader’s receiver circuits, respectively. The phase measurement θ output by the reader thus can be expressed as:

$$
\left\{ \begin{array}{l} \theta = \left(2 \pi \frac {2 l}{\lambda} + \mu\right) \mod 2 \pi \\ \mu = \theta_ {T x} + \theta_ {R x} + \theta_ {T A G} \end{array} \right. \tag {1}
$$

where λ is the wavelength, μ is system noise. Most commercial RFID readers (such as ImpinJ R420 [1]) are able to report θ as the difference of the transmitted and the received signal. Given the ultra-high working frequency of the commercial passive RFID system, it is possible to achieve mm-level ranging accuracy in theory [35]. However, as the phase is a periodic function that repeats every λ in the distance of signal propagation, we cannot use phase value to pinpoint relative tag locations.

# B. Phase Profile

The basic idea of our approach is that by carefully moving an RFID reader over a set of tags during which the reader continuously interrogating the tags, for each tag, the reader obtains a sequence of RF phase values, which we call a phase profile, from the tag’s responses over time. Considering Figure 1 where the set of tags are placed within $x _ { 1 }$ and $x _ { 2 }$ along the X dimension and within $y _ { 1 }$ and $y _ { 2 }$ along the Y dimension, suppose we move the reader along the X dimension from $x _ { 1 }$ to $x _ { 2 }$ perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $( x _ { 2 } , y _ { 2 } )$ . Taking tag 01 as an example, its distance to the reader first decreases until the reader is perpendicular above tag 01, and then increases. According to Equation 1, the phase of the received signal will also decrease first and then increase. Since the range of any phase value is [0, 2π), when this phase value decreases to 0, it immediately jumps to 2π. This process repeats until the reader reaches the perpendicular point right above tag 01, where the received phase stops decreasing and starts to increase from a certain value within [0, 2π); when the phase value increases to $2 \pi .$ , it will immediately drop to 0 and then increases again. Such periodic change of phase values is reflected visually as follows: (1) The phase profile of each tag has a “V-zone” where its bottom occurs at the time when the reader is perpendicular above the tag. (2) Multiple curves are symmetrically distributed on both sides of the V-zone where each curve except the V-zone spans the whole range of [0, 2π). A curve is called one period of the phase profile.

Given a layout of tags and the reader, their relative positions and the reader moving speed, assuming the speed is steady, we can calculate the phase profile of each tag, which we call the reference phase profile. Consider tags 01 and 02 and the reader in Figure 1, and suppose the reader moves at a constant speed of 0.1m/s along the line from $x _ { 1 }$ to x2 perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $( x _ { 2 } , y _ { 2 } )$ . Suppose the distance between $x _ { 1 }$ and $x _ { 2 } .$ , the height of the reader, and the distance from tag 02 to the line from $( x _ { 1 } , y _ { 2 } )$ to $( x _ { 2 } , y _ { 2 } )$ are 3m, 1m and 0.5m, respectively. Figure 3(a) shows the reference phase profiles of tags 01 and 02 when their distance is 5cm. This figure shows that the phase profiles of tag 01 and tag 02 have similar V-zone patterns.

Given the phase profiles of multiple tags, the order that the reader passes through the tags along the X-axis is consistent with the order that the V-zones reach their bottom. By ordering the V-zones according to the time that they reach their bottoms, we can order the tags along the X-axis. Figure 3(a) shows that the V-zone of tag 01 reaches its bottom earlier than that of tag 02, which is consistent with the order that the reader passes through the tags. Furthermore, the longer the distance between two adjacent tags, the longer the time duration between the bottoms of two V-zones is. For example, Figure 3(b) shows the reference phase profiles of tags 01 and 02 when their distance is 10cm. As we increase the distance between the two tags from 5cm to 10cm, the time duration between the two V-zones also increases.

![](images/631d5f30952d1ddcf5c5185f71a52c27ffc2ce337c68bf1709c89e3dc865a735.jpg)



(a)

![](images/39ce40ed7a591642acf90b0f100bb813de9fe229d7901d0c4d5e7b0f950f94e0.jpg)



(b)   
Fig. 3. Reference phase profile along X-axis. (a) X dimension spacing = 5cm. (b) X dimension spacing = 10cm.

![](images/17c9d53f26bd06a170404c5094c7e10fdaa144df4471efe28dfa3805764d5e58.jpg)



(a)

![](images/6d430d2bb90aab1fb7c1b4d59471c8d0dd020319e5b68586d4c4a81cfad29af7.jpg)



Fig. 4. Reference phase profile along Y-axis. (a) Y dimension spacing = 5cm. (b) Y dimension spacing = 10cm.

Given the phase profiles of multiple tags, the larger the bottom phase value of a V-zone is, the longer the distance between the tag that corresponds to the V-zone and the reader. By ordering the V-zones according to the phase value of their bottoms, we can order the tags along the Y-axis. Figure 4(a) shows that the V-zone bottom phase value of tag 04 is smaller than that of tag 01, which means that tag 04 is farther away than tag 01 with respect to the reader. Furthermore, the larger the two bottom phase values of two V-zones differ, the larger the distance between the two corresponding tags along the Y-axis. Figure 4(a) and (b) shows the phase profiles of tag 01 and 04, whose distances along the Y-axis are 5cm and 10cm, respectively. We observe that by increasing the tag distances from 5cm to 10cm, the distances between the bottom phase values of the two corresponding V-zones increases.

To validate the above observations from reference phase profiles, we reproduce the layout of tags in Figure 1 on a white board. We attach an RFID reader on a shopping cart and wheel the cart along the X-axis in the positive direction. The speed of the cart is also set to be 0.1m/s. Figure 5 and Figure 6 shows the two measured phase profiles. From these figures, we can derive the same observations as above. Besides, we also found that due to channel instability, the phase profiles outside the V-zone are fragmentary. It is thus error-prone to connect the whole profile into a big V-zone for tag ordering.

![](images/60c07c9e8b5593ef7646dcaaf350524cefc65e2c107461ef2486335965f02562.jpg)



(a)

![](images/4d7d07e33b8d0d7302cf2c6ad007ceaaa37ddab1530b5371e53483e2d39111f8.jpg)



(b)

Fig. 5. Measured phase profile along X-axis. (a) X dimension spacing = 5cm. (b) X dimension spacing = 10cm.   
![](images/a5ee92c74cc405792d56db3478637254138c5d489e82410727086fda28eb0674.jpg)



(a)

![](images/5b58263bedea40f51d61e7c2f3948912047af272f1744c2650793803921e5d73.jpg)



（b）  
Fig. 6. Measured phase profile along Y-axis. (a) Y dimension spacing = 5cm. (b) Y dimension spacing = 10cm.

# III. SYSTEM DESIGN

In this section, we present the details of our STPP approach to obtain the order of the tags along the X- and Y- axis, respectively. Without loss of generality, we assume that the reader moves along the X-axis from left to right.

# A. Tag Ordering Along X-Axis

The profile segment within the V-zone differs from the other parts of the phase profile from two aspects. First, it changes continuously without jumping from 0 to 2π. Second, it is self-symmetric around the time point that the reader is perpendicular with the tag, which we call the perpendicular point. A straightforward solution to detect the V-zone is to use a sliding window to find the profile segment that satisfies these two properties. However, in reality, due to multi-path self-interference, the phase profile often has missing values within the V-zone as shown in Figure 6(a). Thus, this solution is unreliable for V-zone detection.

1) Detecting V-Zone With Time Warping: Our basic approach is to match the measured phase profile against a pre-calculated reference phase profile, and try to find where the V-zone appears in the measured phase profile. As the reader is often hand held and moved manually, the phase profile become stretched when the movement slows down and compressed when the movement speeds up during the movement. Thus, subsequence matching algorithms (such as the KMP algorithm [12]) will not work for our V-zone detection. To find the place where the V-zone appears, we need to stretch or compress the calculated profile to match the corresponding V-zone on the given phase profile.

To address this issue, we use the Dynamic Time Warping (DTW) technique to match the V-zone in the calculated phase profile against the measured phase profile. DTW is a transformation that automatically compresses or stretches a sequence with the goal of minimizing the distance between these sequences. It naturally compensates for the shifts among different phase profiles caused by the varying reader moving speed. The input to the DTW algorithm consists of a reference phase profile $P$ of length N and a measured phase profile Q of length M . DTW first constructs a distance matrix $D _ { M \times N }$ where each element $D _ { i , j }$ is defined as the Euclidean distance between $p _ { i }$ and $q _ { j }$ :

![](images/309e11d22602ad426b7a581cf3fde9f8bafa2f9af8fae3af8249ae40363b6540.jpg)



(a)

![](images/3dac6e75d9c0f18448628fe67bbf2116b4dd46b7970829d0370c70a7bac11401.jpg)



(b)   
Fig. 7. V-zone detection using DTW. (a) Before warping. (b) After warping.

$$
D _ {i, j} = \left\| p _ {i} - q _ {j} \right\| \tag {2}
$$

where $p _ { i }$ and $q _ { j }$ are the $i ^ { t h }$ and $j ^ { t h }$ elements of the phase profiles P and Q, respectively. The output of the DTW algorithm is a warping path $\mathcal { L } = \{ l _ { 1 } , l _ { 2 } , . . . , l _ { k } \}$ such that the total cost $C _ { \mathcal { L } }$ of the warping path L is minimized:

$$
\underset {\mathcal {L}} {\operatorname{argmin}} \quad C _ {\mathcal {L}} = \sum_ {i = 1} ^ {k} D _ {x (l _ {i}), y (l _ {i})} \tag {3}
$$

where $l _ { i } = ( x , y ) \in [ 1 : M ] \times [ 1 : N ]$ for $l \in [ 1 : k ]$ . The warping path must satisfy the following conditions:

• Boundary Condition: $l _ { 1 } ~ = ~ ( 1 , 1 )$ and $\boldsymbol { l } _ { k } ~ = ~ ( M , N )$ . This ensures the warping path always starts from (1, 1) and end with (M, N ).   
• Monotonicity Condition: if $l _ { i - 1 } = ( c , d )$ and $l _ { i } = ( e , f )$ , then we have $e - c \geq 0$ and $f - d \geq 0$ . This ensures the matching always progresses in the forward direction of time.   
Local Constraints: $| x ( l _ { i } ) - y ( l _ { i } ) | \le \delta$ . This constraint defines a set of admissible step-patterns that only a diagonal band of width 2δ in cost matrix $C _ { \mathcal { L } }$ needs to be computed.

Algorithm (sketch): To generate the optimal warping path, DTW constructs the cost matrix $C _ { i , j }$ using dynamic programming. The optimal substructure is defined as:

$$
C _ {i, j} = D _ {i, j} + \min \left\{C _ {i, j - 1}, C _ {i - 1, j}, C _ {i - 1, j - 1} \right\} \tag {4}
$$

Figure 7(b) shows the matching result using DTW. It shows that the V-zone of the measured profile matches well with that of the reference profile. On the reference profile, as the start and the end point of the V-zone is known a priori, it is easy to locate the corresponding V-zone on the measured profile.

2) Optimizing V-Zone Detection Efficiency: The core of DTW is dynamic programming whose complexity is O(N M ). This process may take some time because the phase profiles may be long (e.g., typically around 400 samples) and the number of tags may be large. To improve efficiency, we apply DTW on the coarser grained representations of phase profiles. Given a phase profile $P ,$ we split it into d segments: record its segmentthe segment range ${ { S } _ { P } } = \left\{ { { s } _ { P , 1 } } , { { s } _ { P , 2 } } , . . . , { { s } _ { P , d } } \right\}$ $s _ { P , i } ^ { R }$ . For each segment i and time interval fined as: $s _ { P , i } ,$ $s _ { P , i } ^ { T }$ we further . Formally, $s _ { P , i } ^ { R }$

![](images/8e6a2d5212784041e9fb5e8a2ffa571b1c666b7d6c2065cfdc7f09f18cbb6624.jpg)



Fig. 8. Phase profile segmentation.

$$
s _ {P, i} ^ {R} = \{s _ {P, i} ^ {L}, s _ {P, i} ^ {U} \}
$$

$$
s _ {P, i} ^ {L} = \min \left\{p _ {a},..., p _ {b} \right\}, s _ {P, i} ^ {U} = \max \left\{p _ {a},..., p _ {b} \right\}
$$

where $s _ { P , i } ^ { L }$ and $s _ { P , i } ^ { U }$ are the minimum and maximum phase values within $i ^ { t h }$ segment. a and b are the begin and the end index of the phase profile within this segment. Note that if within a segment the phase value jumps from 0 to $2 \pi$ , we split the segment into two segments at that point so that no segment contains such phase value jumping. Figure 8 shows an example segmentation. In this figure, we represent the original profile with 25 segments, with each consists of its segment range and time interval.

Given two phase profiles $P$ and $Q ,$ we first acquire their segmented presentation $S _ { P }$ and $S _ { Q }$ , with each contained J and K segments, respectively. Similar to DTW, we construct a distance matrix $D _ { J \times K }$ , where each element $D _ { i , j }$ is defined as the distance between the segmentation $s _ { P , i }$ and $s _ { Q , j }$ . It is intuitively the distance of their two closest points:

$$
D _ {i, j} = \left\{ \begin{array}{l l} \| s _ {P, i} ^ {L} - s _ {Q, j} ^ {U} \|, & \text {   if   } (s _ {P, j} ^ {L} > s _ {Q, j} ^ {U}) \\ \| s _ {Q, j} ^ {L} - s _ {P, i} ^ {U} \|, & \text {   if   } (s _ {Q, i} ^ {L} > s _ {P, i} ^ {U}) \\ 0, & \text {   otherwise   } \end{array} \right. \tag {5}
$$

After compute each element in the matrix $D _ { J \times K }$ , we align $S _ { P }$ and $S _ { Q }$ using dynamic programming. The optimal substructure defined as follows:

$$
\begin{array}{l} C _ {i, j} = \min \left\{s _ {P, i} ^ {T}, s _ {Q, j} ^ {T} \right\} \cdot D _ {i, j} \\ + \min \left\{C _ {i, j - 1}, C _ {i - 1, j}, C _ {i - 1, j - 1} \right\} \tag {6} \\ \end{array}
$$

Using segmentation, we reduce the time complexity of DTW from O(MN) down to $\begin{array} { r } { { \cal O } ( \frac { M } { w } \frac { N } { w } ) = { \cal O } ( \frac { M \bar { N } } { w ^ { 2 } } ) } \end{array}$ w MN w2 where w is the length of each segment. We need to choose the value for w carefully to tradeoff between efficiency and accuracy. The larger the w is, the more efficient DTW is, but the less accurate our V-zone detection is due to the unclear outline of the segmented phase profile. In Section IV, we investigate how to select a proper w value.

However, as Figure 9 shows, due to the multipath and selfinterference, the measured phase profile often contains noise and missing values, which may cause the nadir of the V-zone profile to wrap around. To minimize the noise impact, in this work we use the quadratic fitting technique to minimize such influences. Once the fitting function is determined, by referring the time point when the fitting function achieves the minimum value, we sort this tag together with those tags whose V-zones have already been determined. Figure 10 shows a concrete example. In this example, three tags are attached on a white board, then the antenna moves along the X-axis from the right to the left at a speed of approximate 0.1m/s. The distance between tag 03 and tag 01, tag 01 and tag 02 are 15cm and 2cm, respectively. After performing the quadratic fitting on these phase profiles, we see a clear lag between the phase profiles of these three tags. Based on the time point when the fitting function achieves the minimum value, we further determine the order of these three tags as 01, 02, and 03, which is coherent with the actual order.

# B. Tag Ordering Along Y-Axis

The movement model of the reader when it passes by two tags at a constant speed v is shown in Figure 11. Intuitively, the radial velocity $v _ { R }$ of the tag is inverse proportional to its distance with respect to the antenna. That is, the larger the distance between the tag and the moving trajectory of the reader, the lower the radial velocity of this tag. The lower radial velocity further leads to a smaller phase changing rate, therefore a shallower V-zone profile. Based on the above observation, we propose another segmentation based method to determine the tag order along the Y-axis.

1) Tag Ordering via V-Zone Profile Comparison: The basic idea to determine tag ordering along the Y-axis is to comparing their phase changing rates. One straightforward method is to first derive the span and offset of the quadratic model, and then uses these two parameters to calculate the phase changing rate. However, in reality, if the tags are placed close to each other (such as 5cm), the V-zone profiles of these tags would be similar and would lead to similar curve fitting results. In STPP, we compare the phase changing rate by jointly considering multiple local phase profile segments within the V-zone profile. Notice that the V-zone profile may vary in length due to the random access property of ALOHA protocol [3]. Thus, we first split each profile into equal number of segments to facilitate the comparison. Within each segment of the V-zone profile, we calculate the mean value of phase values. Therefore, given a phase profile $P ,$ we can get its coarse representation by using the set of mean values, i.e., we represent the V-zone profile P by $S ( P ) = \left\{ s _ { P , 1 } , s _ { P , 2 } , . . . , s _ { P , k } \right\}$ , where k is the number of segments and $s _ { P , k }$ is the mean value of $k ^ { t h }$ segment. Averaging over all phase values within each segment will eliminate the impact of noise introduced in phase value measurements. Since each segment corresponds to one specific time window, the average phase value also reflects the accumulated phase changing rate within each segment. By calculating the average phase values, we can improve the robustness of our scheme. Figure 12 shows an example coarse representation of the V-zone profile. In this figure, the phase value within each segment is represented by its mean value.

To determine the order of two tags along the Y-axis, we compare the coarse representation of their V-zone profiles, say $S ( P )$ and $S ( Q )$ , using the following metric:

![](images/04da1ed9a571a6ac74a5f42c7bd7170447da528bc69fc3390526a91848c8d72d.jpg)



(a)

![](images/fce17e21c6757777b193ed69cfa7e4e169135165c288b28fec9b0326c4066e5f.jpg)



(b)

![](images/9ddc41492601d88888901614b99757de7ee0c2ceab592e2537b0b757244c8b11.jpg)



(c）

![](images/4225d5385ba410a112cb7591def9bbc96e81714bf5d7d6488c6fac5d593dcf50.jpg)



(d)

![](images/9ac04e2590035dea49ddbe4259552c52533c6c071741e867945ea8f52c6540c4.jpg)



(e)

Fig. 9. Snapshot of V-zone profiles. (a) Sample 01. (b) Sample 02. (c) Sample 03. (d) Sample 04. (e) Sample 05.   
![](images/48af7dd5e7df1efa82e4255f085b3a4ff6993106f86659cc706e116377a4cc63.jpg)



Fig. 10. Tag ordering with quadratic fitting.

![](images/01d3162799bb2fcf497cc37db7146870ae50c543bc1e0e3d9771574bff87ec52.jpg)



Fig. 11. Reader movement model.

![](images/f60ad59b12c7f5ada194ac692019264be335a2e55f9025edb26e6e4ce31c8cfe.jpg)



Fig. 12. Examples of coarse representation of V-zone profile.

$$
O (P, Q) = \sum_ {i = 1} ^ {k} \lceil \frac {s _ {P , i} - s _ {Q , i}}{s _ {P , i}} \rceil \tag {7}
$$

Generally, if the phase changing rate of $P$ is smaller than that of $Q ,$ for each segment i, $s _ { P , i }$ will be larger than $s _ { Q , i } .$ Therefore, $O ( P , Q )$ will be close to k. On the contrary, if the phase changing rate of $P$ is larger than that of $Q , \ s _ { P , i }$ will be no larger than $s _ { Q , i }$ . Here $O ( P , Q )$ will be close to 0 accordingly. Therefore, we can determine the tag order along the Y-axis based on the value of $O ( P , Q )$ .

![](images/2bdf7a8002f14af0b47c8d31e6d35f5d833029fc8cdbee3dd6f0dbef3cdd777d.jpg)



Fig. 13. w vs. matching accuracy.

2) Optimizing the Ordering Efficiency: The core of determining the tag order along the Y-axis is to compare the V-zone profiles by using the metric $O ( P , Q )$ . This process may take some time because we need to compare each pair of phase profiles. For example, it takes $\textstyle { \frac { M ( M - { \bar { 1 } } ) } { 2 } }$ comparison to determine the order of M tags along the Y-axis. To speed up this process, we further introduce a new metric $G ( P , Q )$ to measure the gap between two phase profiles $P$ and Q. It is defined as follows:

$$
G (P, Q) = \sum_ {i = 1} ^ {k} \| s _ {P, i} - s _ {Q, i} \| \tag {8}
$$

where $\| s _ { P , i } - s _ { Q , i } \|$ is the Euclidean distance between the mean phase value $s _ { P , i }$ and $s _ { Q , i }$ . In an intuitive level, $G ( P , Q )$ is proportional to the physical spacing of these two tags. i.e., the larger the physical spacing between these two tags, the larger the $G ( P , Q )$ will be. For M tags, we then randomly choose one tag as the pivot. Let P be the V-zone profile of this pivot, then we calculate $O ( P , Q )$ and $G ( P , Q )$ between $P$ and each profile $Q$ of the remaining tags. By doing so, we can not only determine the relative order between the pivot tag and other tags, but also acquire the relative distance of these tags. Therefore, we can order these M tags with only $M - 1$ comparison, which is significantly smaller than $\textstyle \frac { M ( M - 1 ) } { 2 }$ .

# IV. SYSTEM EVALUATION

# A. Implementation

Hardware: Our system consists of a COTS UHF RFID reader, a directional antenna, and a set of passive tags. To account for device diversity, we have tested our system using different hardware, including an ImpinJ R420 reader, an ImpinJ Threshold RFID Antenna IPJ-A0311, an Alien ALR-8696-C antenna, and four types of passive tags: Alien ALR-9610, ALN-9662, ALN-9634, and ALN-9720.

For diversity, we choose four types of tags of different size and shape.

Software: We implemented our algorithms in Java, which were executed on a Lenovo PC equipped with an Intel(R) Celeron G530 CPU and 4G RAM. The PC is connected to the RFID reader via Ethernet. The reader is programmed to continuously query the RFID tags on a randomly chosen channel $( 6 ^ { t h }$ in this paper) returns the signal phase for each tag reply.

# B. Deployment

One deployment issue is to determine the number of periods that the reference phase profile should contain. In theory, the reference phase profile should contain the same number of periods as the measured profile. In order to obtain a proper reference phase profile, we put the reader 30cm (a common distance between a librarian and a bookshelf) away from the tags. We collected phase profiles by holding the reader and passing 200 tags for 15 times. Of the 3,000 phase profiles that we collected, more than 97% of them contain 4 partial or complete periods. Thus, we generate a 4-period reference phase profile as the default setting in our experiment.

Another deployment issue is to determine the height that the antenna should be moving across the tags. As STPP uses the phase changing rate of each tag to determine its relative order along the Y-axis, we need to place the antenna at a height such that the tags with different Y coordinates differ in phase changing rate. This can be ensured if all the tags are either above or below the antenna along the Y-axis since their antenna to tag distances would differ from each other. For example, in library, we can put the antenna at the bottom of the lowest shelf so that each tag has a different distance to the reader, which is moving along the X-axis. In our experiments, we simply place the antenna at a height below all tags.

# C. Micro-Benchmarks

Experimental Setup: We have two experimental cases: the antenna moving case and the tags moving case. In the antenna moving case, we partition 150 tags into 3 groups and attach them on a white board as shown in Figure 16(a). The antenna is fixed on a wheeled chair which is pushed manually at a rough speed of 0.3m/s. This experimental setup simulates the misplaced book locating application in libraries where a librarian moves a reader across a bookshelf.

In the tag moving case, we use a conveyor belt and a tape to compose a mobile RFID system as shown in Figure 16(b). The antenna is placed 1m away from the tape and 1m above the top of the winder. We attach a set of tags on the tape, which move at a constant speed of 0.3m/s. This case simulates the baggage handling application in airports where baggage or cargos attached with RFID tags are delivered on a conveyor belt.

Evaluation Metrics: We mainly use the metric of ordering accuracy defined in Equation 9. A tag is ordered incorrectly in a sequence of tags if and only if the detected order of the tag is not equal to the actual order of that tag. For example, suppose there are five tags and the correct order of these five tags is 1-2-3-4-5. If the output of our scheme is 1-2-4-3-5, then we immediately know that the tag 4 and tag 3 are ordered incorrectly, and thus the accuracy is 3/5=60%.

![](images/8bc25c0602ea4eba6e1b727939cbffc19aa3c5183b457b6e3ad62b1c80598903.jpg)



Fig. 14. Tag moving case.

![](images/864be455de06d183b6f9b10488cbfab46296aa5cb9c001b3f8009c78b14a915a.jpg)



Fig. 15. Antenna moving case.

![](images/8af3b7f7096b17e00e795a287c08d32dea3a5bba1ac9dff43360590afb47950b.jpg)



(a)

![](images/fc983de3b2d87a4833badc12a41b9d4af850b1a56b34a381de423003789f402a.jpg)



(b)   
Fig. 16. Experimental setup. (a) Antenna moving case. (b) Tag moving case.

$$
\text { Ordering   Accuracy } = \frac {\# \text { of   tags   ordered   correctly }}{\# \text { of   tags   in   total }} \tag {9}
$$

Determining a Proper Window Size w: In general, a larger window size contributes to higher efficiency but lower accuracy. As shown in Figure 13, the ordering accuracy of STPP remains high for small window sizes (e.g., nearly 98% when w = 3), decreases slightly with window sizes increased from 3 to 5, and drops sharply for window sizes larger than 5. Therefore we set w to be 5 in our experiments to tradeoff between latency and accuracy.

Tag-to-Tag Distance vs. Ordering Accuracy: We further vary the tag-to-tag distance to investigate the ordering accuracy in both controllable and uncontrollable cases. The results are shown in Figure 14 and Figure 15. As Figure 14 indicates, the ordering accuracy along both the X-axis and the Y-axis increases with the spanning of tag-to-tag distance. Specifically, when the distance between each pair of tags is extremely small (e.g., 2cm), STPP achieves an undesirable performance, with an accuracy of 0.42 for X-axis ordering and 0.23 for Y-axis ordering. One possible reason for this is that if two tags are placed too close to each other, these two tags will form two identical circular loops, which will generate inductive coupling effect. Consequently, each tag will be shadowed by another, resulting in low reading rate. The ordering accuracy of STPP then increases dramatically as we slightly span the tag-to-tag distance. As Figure 14 shows, when the distance between each pair of tags is 8cm, STPP could correctly distinguish the order of tags along both the X-axis and the Y-axis with a success rate of above 0.8. Such figure boosts to 0.92 and 0.88 along X-axis and Y-axis respectively, when we further increase the tag-to-tag distance to 10cm. Similar trend can be also found in uncontrollable case. As shown in Figure 15, the gaining trend of the ordering accuracy along both the X-axis and the Y-axis increases dramatically when we increase the tag-to-tag distance. Such trend then becomes steady when the tag-to-tag distance is larger than 8cm. Figure 14 and Figure 15 together demonstrate that STPP can successfully judge the order of tags along both the X-axis and Y-axis in fine-grained manner.

![](images/1d32bc8e0d0f170a2756594cf7e1cc38dab2d901a7881e17d7f4bf9ec0b168cf.jpg)



![](images/b07fbc5ec20a4cad09f80545d2197de95736d90d5eb2342b56b74b2fc49e245a.jpg)



(b)

![](images/dba1968584fc4642936b9f5eb06523448148fc6d03101b4e40fb504422866fb7.jpg)



(（c)

![](images/87edb66385fd3c82119c8d48c817a512fc8ffd288331177cc80e25c8433040cf.jpg)



![](images/a5559770d4b74d023eb74c81c1446fa947cfc691074445bf84ca4718acf886f5.jpg)



Fig. 17. Tag layout settings. (a) Test case 1. (b) Test case 2. (c) Test case 3. (d) Test case 4. (e) Test case 5.

TABLE I TAG POPULATION VS. ORDERING ACCURACY 

<table><tr><td rowspan="2">Tag moving</td><td colspan="6">Tag population size within the reading zone</td></tr><tr><td>n=5</td><td>n=10</td><td>n=15</td><td>n=20</td><td>n=25</td><td>n=30</td></tr><tr><td>X-axis</td><td>0.963</td><td>0.954</td><td>0.952</td><td>0.937</td><td>0.906</td><td>0.884</td></tr><tr><td>Y-axis</td><td>0.917</td><td>0.903</td><td>0.878</td><td>0.874</td><td>0.863</td><td>0.856</td></tr></table>

TABLE II TAG POPULATION VS. ORDERING ACCURACY 

<table><tr><td rowspan="2">Antenna moving</td><td colspan="6">Tag population size within the reading zone</td></tr><tr><td>n=5</td><td>n=10</td><td>n=15</td><td>n=20</td><td>n=25</td><td>n=30</td></tr><tr><td>X-axis</td><td>0.873</td><td>0.865</td><td>0.861</td><td>0.852</td><td>0.841</td><td>0.813</td></tr><tr><td>Y-axis</td><td>0.809</td><td>0.806</td><td>0.798</td><td>0.779</td><td>0.765</td><td>0.754</td></tr></table>

Tag Population vs. Ordering Accuracy: Commercial RFID reader have limited reading rate. If the reading zone of the antenna contains a large number of tags, we will have under-sampling of phase readings which potentially degrades the ordering accuracy. We change the tag populations from 5 to 30 within the reading zone of the antenna and examine the performance of STPP. The distance between two adjacent tags is randomly chosen in the range of [2cm, 10cm]. We present the experimental results in Table I and Table II to compare the data values. As shown in this table, when the tag population is small within the reading zone of the antenna, e.g., n = 5,

![](images/6700f845170fa26dfcd16d59f8e3fdf156fd21e72e2e94f618db8c163c2ae499.jpg)



Fig. 18. Accuracy vs. schemes.

STPP achieves satisfactory performance, with ordering accuracies of above 90% and 80% for the tag moving and antenna moving cases, respectively. As we steadily increase the tag population within the reading zone, the ordering accuracy degrades gradually in both two cases. When the tag population reaches 30, the ordering accuracy remains at an acceptable level, with average accuracies of above 0.85 and 0.75 for tag and antenna moving cases, respectively. This result indicates that the performance of STPP will degrade a little bit when the tag population increases.

# D. Macro-Benchmarks

We evaluated STPP in comparison with the following four schemes that are implementable on COTS RFID readers:

1) G-RSSI: This is a straightforward scheme that uses RSSI value changes to infer tag orders along the X-axis.   
2) OTrack [25]: This scheme combines RSSI dynamics and tag successful reading rates to determine tag orders along the X-axis.   
3) Landmarc [20]: This scheme uses multiple reference tags to calculate the absolute location of a tag in 2 dimensional region.   
4) BackPos [17]: This scheme uses RF phase values and the hyperbolic positioning technique to calculate the absolute location of a tag in 2 dimensional region.

Our experimental results show that STPP significantly outperforms the other four schemes for the accuracy of relative localization. We compare the ordering accuracy of these schemes under various layout settings as shown in Figure 17. In each setting, we repeat the experiment 100 times and use their average ordering accuracy values. The distance between adjacent tags ranges from 1cm to 10cm. As shown in Figure 18, G-RSSI and Landmarc achieve similar low ordering accuracy values of below 25% along both axes.

![](images/64012ebbe2d1c1d4826778176c85ca77c8296e46860c5a5ded2449e59ba2d36d.jpg)



Fig. 19. Accuracy vs. tag distance.

![](images/da79ba4dd24b926a015de4eb2ff98484605c4807c3122cbd34d1153f3ae11b3e.jpg)



Fig. 20. Accuracy vs. population.

Using both RSSI dynamics and tag successful reading rates, OTrack outperforms G-RSSI and Landmarc, yet can only reach an ordering accuracy of belowing 50%. With more precise signal measurement, BackPos can locate each tag and further distinguish their relative order with an average ordering accuracy of 80%. While STPP achieves an average ordering accuracy of more than 88%.

Our experimental results show that STPP scales better than the other four schemes as adjacent tag distance decreases. To perform this evaluation, we choose a population of 20 tags and vary the adjacent tag distance from 100cm to 10cm. Figure 19 shows the box plot of the accuracy values of different schemes as we vary the distance. The whisker indicates values outside the upper and lower quartiles. From this figure, we can observe that the median accuracy of STPP is significantly higher than that of other four schemes. Besides, the likely range of variation (IQR) of STPP is the smallest as the adjacent tag distance decreases.

Our experimental results show that STPP scales better than the other four schemes as tag population size increases. To perform this evaluation, we choose 10cm to be the adjacent tag distance and vary the tag population from 5 to 30. As G-RSSI, Landmarc, and BackPos are insensitive to tag population sizes, we thus compare STPP with OTrack. Figure 20 shows the box plot of the accuracy values of different schemes as we vary the tag population size. From this figure, we observe that likely range of variation (IQR) of STPP is significantly smaller than that of OTrack.

# V. CASE STUDIES

We deployed our relative RFID tag localization system in two real-world applications: a misplaced book locating system in a library and a baggage handling system in an airport. In this section, we present our experimental results with these two case studies. Note that our relative localization scheme is not limited to these two applications. Other applications (such as locating suspicious baggage and warehouse stocktaking) can also benefit from our localization scheme.

![](images/83442cdc1830e97577dab3ac40c1fbfeca4ff3f9e64b9edeb220b238f635ae0f.jpg)



Fig. 21. Locating misplaced books. The distance from the antenna to each layer of books are different, so as to ensuring a different phase changing rate.

![](images/01c332523026b69587e618a2e959027c4882208012890f13c9bebb0f5769d346.jpg)  
Fig. 22. Layout of detected books by STPP.

# A. Misplaced Book Locating in Library

A major task for librarians is to locate misplaced books and relocate them to the right place. Note that library books are typically strictly ordered based on their IDs so that borrowers can find a specific book easily. To help locate misplaced books, we deploy our STPP system in a school library. For one bookshelf in the library, we attach 90 RFID tags to 90 books, one tag per book. These books are placed on three levels. The thickness of each book spans from 3cm to 8cm. We attach an RFID antenna on a cart and manually push it across the bookshelf from left to right, as shown in Figure 21. Here we put the antenna at the height of 1.6 m, such that the distance from the reader antenna to each layer of books are different.

This case study also shows that STTP can achieve high relative localization accuracy. We sweep these 90 books over 50 times. The result shows that our relative localization scheme achieves an accuracy of 0.84 on average. This implies that in most cases, STPP can precisely pinpoint the relative location of the misplaced book. For the remaining cases, although STPP cannot correctly find the relative location of tags, it still helps the librarian to narrow down the searching space. Figure 22 shows the order of the books that we obtained in one experiment, whee each dot represents a book and each cross represents a book that we ordered incorrectly. Note that the gap between two dots reflects the distance between two tags.

TABLE III RESULT OF MISPLACED BOOK DETECTION BY STPP 

<table><tr><td></td><td>Detection success rate</td></tr><tr><td>1 book</td><td>98%</td></tr><tr><td>2 books</td><td>97%</td></tr><tr><td>3 books</td><td>98%</td></tr></table>

![](images/653af3fe701380dd7893e8dce4ce5f5abc642c320cd3a4dc812c79ab725a319b.jpg)



(a)

![](images/f185b7ed67c3f98f464430a0a23dd5d1a6be74dfd1ca92b4579e9dfea6194e86.jpg)



(b）  
Fig. 23. Baggage handling in the airport. (a) RFID tag for baggage check-in. (b) Baggage handling in Terminal One, Sanya Phoenix airport.

From this figure, we observe that all incorrectly ordered books are those thin ones as their tags are much closer.

We also conducted experiments to evaluate the ability of STPP in detecting misplaced books. We randomly picked one book, two books, and three books from a bookshelf and inserted them into a differently chosen location on this bookshelf. This location is randomly chosen from the range of 2 books away from the original place to 10 books away. Each case was repeated 100 times. The detection success rate is shown in Table III.

# B. Baggage Handling in Airport

To avoid mis-delivered baggages, baggage handling systems in airports need to find the order of the baggages on the conveyor belt [2]. Although the size of one baggage item is usually large, the distance between adjacent tags (attached to different baggages) can be rather close due to the arbitrary orientation of baggage on the convey belt. It is thus critical to pinpoint the relative order of baggage with high resolution. We deployed our STPP system at Terminal One, Sanya Phoenix airport, Sanya, Hainan Province, China. Three RFID reader antennas are deployed at three places on the tunnel as shown in the left figure in Figure 23(b). Based on the tag ordering information, the visualization module displays each baggage and tracks its movement on the baggage conveyor belt, as shown in the right figure in Figure 23(b). As reference tags and antennas, which are the essential part of the localization scheme Landmarc and BackPos, cannot be deployed on the commercial baggage handling system, we thus compare STPP with OTrack and G-RSSI in this case study. Our experiments were carried out during three periods: 7:00AM∼9:00AM, 13:00PM∼15:00PM, and 19:00PM∼21:00PM, during which over 1,000 pieces of baggage from 9 flights are handled.

This case study shows that STTP can achieve high relative localization accuracy. Table IV shows the accuracy results of STPP in comparison with G-RSSI and OTrack during the three time periods. During the peak hours of 7:00AM∼9:00AM and 19:00PM∼ 21:00PM, during which the distance between each baggage is typically smaller than 20cm, our STPP achieves accuracy values of 97% and 96%, respectively; whereas OTrack achieves an accuracy of 88% for both time periods and G-RSSI achieves accuracy values of 59% and 51%, respectively. During the off peak hours of 13:00PM∼15:00PM, our STPP, OTrack, and G-RSSI achieve accuracy values of 97%, 95%, and 72%, respectively.

TABLE IV ACCURACY OF STPP, OTRACK, AND G-RSSI 

<table><tr><td></td><td>7:00~9:00</td><td>13:00~15:00</td><td>19:00~21:00</td></tr><tr><td>STPP</td><td>388/400=97%</td><td>224/230=97%</td><td>422/440=96%</td></tr><tr><td>OTrack</td><td>352/400=88%</td><td>218/230=95%</td><td>388/440=88%</td></tr><tr><td>G-RSSI</td><td>234/400=59%</td><td>166/230=72%</td><td>226/440=51%</td></tr></table>

![](images/3288975755ebd8e636b011be872767b485bfcdb49c1bcebd144a1b515b989592.jpg)



Fig. 24. Ordering latency of STPP and OTrack.

![](images/d94928a5fccf97c55be493ef870805a7533c511e9aa1006fc78b334a79cecfe0.jpg)



Fig. 25. Terminology definition; $d _ { x }$ and $d _ { y }$ are the spacing between each pair of tags along X-axis and Y-axis, respectively.

We further examine the ordering latency of OTrack and STPP. In this trial of experiments, we use OTrack and STPP to detect the order of 100 baggages on a moving conveyor. The CDF of the ordering latency incurred by each scheme is shown in Figure 24. As the result indicates, the average latency of STPP is 1.473s, which is slightly hight than that of OTrack.

# VI. STPP FOR SPACING MEASUREMENT

So far, we have introduced how STPP is used to determine the tag order along each dimension. In this section, we show that in controllable cases, e.g., the reader antenna moves at a constant speed along a strictly straight line, we can measure the spacing between each pair of tags and further acquire their absolute locations. Without loose of generality, we define the spacing between each pair of tags as the distance from the geometric center of one tag to that of another tag (as shown in Figure 25). We assume the reader antenna moves at a constant speed v. As before, we present how to measure the spacing between each pair of tags X-axis and Y-axis, separately.

![](images/952d42c50ba43036271470ee94000ed5e5c6b7dc2c95f70a1660650a136947f3.jpg)



Fig. 26. An illustration of spacing measurement along Y-axis.

# A. Principle

A typical UHF RFID reader has 16 channels working at the 920∼926 MHz ISM band. The reader we used here reports the phase value as an integer between 0∼4096, hence providing a ranging resolution of 320mm · $\begin{array} { r } { \frac { 2 \cdot \pi } { 4 0 9 6 } = 0 . 0 4 m m } \end{array}$ . Such a high resolution provides theoretical foundation of accurate spacing measurement.

Determine the Tag Spacing Along X-Axis: We take tag 01 and tag 02 in Figure 1 as an example to illustrate the basic principle here. Let $t _ { i }$ and $t _ { j }$ be the time-stamp when the reader is perpendicular above these two tags along X-axis. Then it is easy to know that the distance between these two tags can be computed as: $v \cdot \left( \left| t _ { i } - t _ { j } \right| \right)$ .

Determine the Tag Spacing Along Y-Axis: As shown in Figure 26, two tags locate in different Y coordinates. The spacing between these two tags along the Y-axis is denoted as |DE|. Hence our goal here is to infer the distance |DE|. Suppose the reader antenna moves from A to B, the moving distance $( | A B | )$ thus equals to $v \cdot \Delta t ,$ where v is the moving speed and $\Delta t$ is the travel time. During antenna’s movement, the distance between this antenna and the tag changes and can be measured by the changing of phase readings. Let $\Delta \theta _ { 3 }$ and $\Delta \theta _ { 4 }$ be the phase changing of tag 03 and tag 04 when the reader moves from A to B, respectively. Hence we have:

$$
\left\{ \begin{array}{l} | A D | ^ {2} + | A B | ^ {2} = | B D | ^ {2} \\ | B D | - | A D | = \lambda \cdot \frac {\Delta \theta_ {3}}{\pi} \end{array} \right. \tag {10}
$$

Where λ is the wavelength. Hence we can easily acquire the distance $| A D |$ . Similarly, for tag 04, we have:

$$
\left\{ \begin{array}{l} | A E | ^ {2} + | A B | ^ {2} = | B E | ^ {2} \\ | B E | - | A E | = \lambda \cdot \frac {\Delta \theta_ {4}}{\pi} \end{array} \right. \tag {11}
$$

In a similar way, we can acquire the distance |AE|. Accordingly, the spacing |DE| can be easily computed as $\sqrt { | A E | ^ { 2 } - | A D | ^ { 2 } }$ .

# B. Experiment

We evaluate the performance of spacing measurement approach and presents the result in Figure 27. In this trail of experiments, 16 tags are attached on the moving conveyor, forming a $4 \times 4$ matrix. We vary the spacing between each pair of tags from 5cm to 20cm, with a step of 5cm. In each spacing settings, we conduct the experiment 10 times and summarize the results in Figure 27. As the result indicates, when the spacing is relative small, e.g., 5cm, STPP achieves unsatisfying performance, with an overall ranging error of 6.5cm and 8.74cm on average for X-axis and Y-axis, respectively. This is because with a smaller spacing setting, more tags will appear within the coverage area of the reader antenna. As a result, each tag will get less tag reading, leading to a sparse phase profile. Hence STPP is more likely to get a wrong timestamp of the nadir point. As we gradually increase the spacing, the ranging error decreases gradually, and finally maintains an average below 6cm and 5cm for X-axis and Y-axis, respectively.

![](images/963edd2e7eb24db93e70265cd87aec27b1a2c458320d1d097314123433b920e4.jpg)



Fig. 27. Spacing ranging accuracy.

# VII. RELATED WORK

In this section, we broadly review state-of-the-arts that are directly related to our work.

# A. Localization and Tracking

WiFi-Based Human/Object Localization: A large body of works either adopt signal modeling or fingerprinting matching as the basic scheme for localization. The pioneer work, RADAR [9], combines signal strength measurements with signal propagation model to determine user location. SurroundSense [6] combines the WiFi signatures with other ambient characteristics such as light, sound recorded by smartphone for room-level localization. LIFS [37] leverages the human walking trail inferred by smartphone sensors to reduce the overhead of WiFi fingerprinting database construction, which is the essential component for WiFi based localization scheme. Xiong et al. designs and implements ArrayTrack [34], which adopts Angle-of-Arrival information of the receiver for centimeter-scale object localization. The advance of software defined radio platform further boosts the development of through wall localization and tracking using WiFi. WiTrack [5] explores the FMCW technique to acquire the Time-of-Flight for antenna-to-human ranging, and achieves 10cm error margin for through-wall human tracking.

RFID-Based Human/Object Localization: Early RF-based localization schemes primarily rely on RSSI information to acquire the absolute location of an object [20], [25], [36].

They typically pre-deploy tags densely on a monitoring region as anchors, and then use the RSSI values of these anchor tags as references to locate a specific tag [20], [39]. Succeeding works explore the anchor-free approach by either modeling the signal propagation process in complex environment [36] or taking a combination of various signal features (e.g. the RSSI and the tag’s reading rate [25]). The limitation of RSSI-based approaches is that they are sensitive to multi-path propagation, and thus difficult to achieve high-precision localization.

There is a growing interest in using phase values to estimate the absolute location of an object. Pioneer work uses hyperbolic localization techniques [17], [31] or Angle of Arrival (AoA) information [7], [15], [21] to locate tags by measuring the phase difference between the received signals at different antennas. To reduce the hardware deployment cost, state-of-the-art systems use synthetic aperture radar (SAR) to simulate multiple antennas to extract RF information [23], [30]. For instance, by leveraging antenna motion, PinIt achieves a location accuracy on the order of centimeters [30]. Another line of work employs multiple antennas to construct a hologram for tag localization [19], [35].

Our work is inspired by the above works in phase-based tag localization, but we focus on leveraging reader mobility to generate phase profiles for tag localization. In this setting, PinIt [30] is perhaps most related to ours. It locates RFID tags by analyzing their multi-path profiles collected by a moving antenna. However, the intuition behind PinIt is that nearby RFID tags experience a similar multi-path environment and thus exhibit similar multi-path profiles. In contrast, the intuition behind our scheme is that by analyzing the spatialtemporal dynamics in the phase profiles of a set of tags, we can calculate the spatial ordering among tags. Moreover, PinIt relies on dedicated hardware (i.e., USRP) to capture the multi-path profile of each tag and requires densely deployed reference tags. In contrast, our scheme works on COTS devices and does not rely on any reference tags. Although both PinIt and our scheme leverage DTW metric and optimize its execution for tag localization, the targets of the DTW optimization in these two schemes are different. PinIt leverages derivative DTW (DDTW) technique to handle the power scaling problem, whereas our scheme optimizes the computational efficiency by applying the DTW on the coarsegrained representation of the phase profile.

# B. Activity Recognition

Wearable Sensor Based Activity Recognition: there are a plenty of works adopt wearable sensors for human activity recognition. JigSaw [18] relies on smartphone sensors to monitor and distinguish activity context such as walking, cycling and running, etc.. Swimmaster [8] extracts velocity, arm strokes, and body balance via wearable sensors, and provides a fine-grained swimming quality assessment. Other researchers further exploits inertial sensors for smoking recognition [22], sleeping quality monitoring [13] etc..

WiFi-Based Posture Recognition: There are also a plenty of works focusing on WiFi-based human posture recognition. WiSee [24] adopts doppler Effect on WiFi signals for whole-home human gesture recognition. WiHear [28] is designed for human speaking recognition by processing the reflected WiFi signals on human’s mouth. E-eyes [33] exploits the CSI signature of different indoor activities for fine-grained home activity recognition. Similarly, Wang et al. [32] builds up a CSI-speed model for fine-grained human activity sensing, such as walking, falling down and running.

RFID-Based Human Motion Sensing: There are also a large portion of works on RFID-based human motion sensing. FEMO [10] is designed to recognize free-weight activity and further help to rectify nonstandard actions in the gym. CBID [14] leverages the doppler effect of phase value for pick-up detection in shops. Similarly, ShopMiner [27] exploits the temporal variation of phase pattern for hot item detection, popular category identification, and correlated item discovery in physical clothing stores.

# VIII. CONCLUSIONS

In this paper, we propose the phase profiling approach to relative localization of RFID tags by exploiting the spatialtemporal dynamics in tag phase profiles. We show that relative localization can be achieved without the absolute location of tags. Our approach requires neither dedicated infrastructure nor special hardware. We implemented our approach and conducted experiments in two realistic case studies: locating misplaced books in a library and determining baggage ordering in an airport. The result shows that our approach can achieve high accuracy in realistic settings. This paper represents an early comprehensive study of relative localization of RFID tags. Our system can be used in a wide range of applications such as inventory control, asset management, and customer behavior tracking.

# REFERENCES

[1] ImpinJ, accessed on Aug. 18, 2015. [Online]. Available: http://www. impinj.com   
[2] The Statistics of Luggage Missing in Airport, accessed on Aug. 18, 2015. [Online]. Available: http://gadling.com/2010/03/26/ airlines-losing-3000-bags-every-hour-of-every-day/   
[3] EPC Radio-Frequency Identity Protocols Class-1 Generation-2 UHF RFID Protocol for Communications at 860 MHz–960 MHz, EPCglobal, Jan. 2005.   
[4] UHF Class 1 Gen 2 Standard Version 1.0.9, EPCglobal, Jan. 2005.   
[5] F. Adib, Z. Kabelac, D. Katabi, and R. C. Miller, “3D tracking via body radio reflections,” in Proc. 11th USENIX NSDI, 2014, pp. 317–329.   
[6] M. Azizyan, I. Constandache, and R. R. Choudhury, “Surround-Sense: Mobile phone localization via ambience fingerprinting,” in Proc. 15th Annu. Int. Conf. Mobile Comput. Netw., 2009, pp. 261–272.   
[7] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, “New measurement results for the localization of UHF RFID transponders using an angle of arrival (AoA) approach,” in Proc. RFID, 2011, pp. 91–97.   
[8] M. Bächlin, K. Förster, and G. Tröster, “SwimMaster: A wearable assistant for swimmer,” in Proc. 11th Int. Conf. Ubiquitous Comput., 2009, pp. 215–224.   
[9] P. Bahl and V. N. Padmanabhan, “RADAR: An in-building RF-based user location and tracking system,” in Proc. 19th Annu. Joint Conf. IEEE Comput. Commun. Soc. (INFOCOM), vol. 2, Mar. 2000, pp. 775–784.   
[10] H. Ding et al., “FEMO: A platform for free-weight exercise monitoring with RFIDs,” in Proc. 13th ACM Conf. Embedded Netw. Sensor Syst. (SenSys), 2015, pp. 141–154.   
[11] D. M. Dobkin, The RF in RFID: Passive UHF RFID in Practice. Amsterdam, The Netherlands: Elsevier, 2008.   
[12] D. E. Knuth, J. H. Morris, Jr., and V. R. Pratt, “Fast pattern matching in strings,” SIAM J. Comput., vol. 6, no. 2, pp. 323–350, 1977.

[13] W. Gu et al., “Intelligent sleep stage mining service with smartphones,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2014, pp. 649–660.   
[14] J. Han et al., “CBID: A customer behavior identification system using passive tags,” in Proc. IEEE 22nd Int. Conf. Netw. Protocols (ICNP), Oct. 2014, pp. 47–58.   
[15] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar, “Accurate localization of RFID tags using phase difference,” in Proc. RFID, 2010, pp. 89–96.   
[16] C. Law, K. Lee, and K.-Y. Siu, “Efficient memoryless protocol for tag identification (extended abstract),” in Proc. DIALM, 2000, pp. 75–84.   
[17] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu, “Anchor-free backscatter positioning for RFID tags with high accuracy,” in Proc. IEEE INFOCOM, Apr./May 2014, pp. 379–387.   
[18] H. Lu et al., “The Jigsaw continuous sensing engine for mobile phone applications,” in Proc. 8th ACM Conf. Embedded Netw. Sensor Syst., 2010, pp. 71–84.   
[19] R. Miesen, F. Kirsch, and M. Vossiek, “Holographic localization of passive UHF RFID transponders,” in Proc. RFID, 2011, pp. 32–37.   
[20] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “LANDMARC: Indoor location sensing using active RFID,” Wireless Netw., vol. 10, no. 6, pp. 701–710, 2004.   
[21] P. V. Nikitin et al., “Phase based spatial identification of UHF RFID tags,” in Proc. RFID, 2010, pp. 102–109.   
[22] A. Parate, M.-C. Chiu, C. Chadowitz, D. Ganesan, and E. Kalogerakis, “RisQ: Recognizing smoking gestures with inertial sensors on a wristband,” in Proc. 12th Annu. Int. Conf. Mobile Syst., Appl., Services, 2014, pp. 149–161.   
[23] A. Parr, R. Miesen, and M. Vossiek, “Inverse SAR approach for localization of moving RFID tags,” in Proc. RFID, 2013, pp. 104–109.   
[24] Q. Pu, S. Gupta, S. Gollakota, and S. Patel, “Whole-home gesture recognition using wireless signals,” in Proc. 19th Annu. Int. Conf. Mobile Comput. Netw., 2013, pp. 27–38.   
[25] L. Shangguan, Z. Li, Z. Yang, M. Li, Y. Liu, and J. Han, “OTrack: Towards order tracking for tags in mobile RFID systems,” IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 8, pp. 2114–2125, Aug. 2014.   
[26] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Relative localization of RFID tags using spatial-temporal phase profiling,” in Proc. 12th USENIX Symp. Netw. Syst. Design Implement. (NSDI), 2015, pp. 251–263.   
[27] L. Shangguan et al., “ShopMiner: Mining customer shopping behavior in physical clothing stores with COTS RFID devices,” in Proc. 13th ACM Conf. Embedded Netw. Sensor Syst. (SenSys), 2015, pp. 113–125.   
[28] G. Wang, Y. Zou, Z. Zhou, K. Wu, and L. M. Ni, “We can hear you with Wi-Fi!” in Proc. 20th Annu. Int. Conf. Mobile Comput. Netw., 2014, pp. 593–604.   
[29] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “RF-compass: Robot object manipulation using RFIDs,” in Proc. 19th Annu. Int. Conf. Mobile Comput. Netw., 2013, pp. 3–14.   
[30] J. Wang and D. Katabi, “Dude, where’s my card?: RFID positioning that works with multipath and non-line of sight,” ACM SIGCOMM Comput. Commun. Rev., vol. 43, no. 4, pp. 51–62, 2013.   
[31] J. Wang, D. Vasisht, and D. Katabi, “RF-IDraw: Virtual touch screen in the air using RF signals,” in Proc. ACM Conf. SIGCOMM, 2014, pp. 235–246.   
[32] W. Wang, A. X. Liu, M. Shahzad, K. Ling, and S. Lu, “Understanding and modeling of WiFi signal based human activity recognition,” in Proc. 21st Annu. Int. Conf. Mobile Comput. Netw., 2015, pp. 65–76.   
[33] Y. Wang et al., “E-eyes: Device-free location-oriented activity identification using fine-grained WiFi signatures,” in Proc. 20th Annu. Int. Conf. Mobile Comput. Netw., 2014, pp. 617–628.   
[34] J. Xiong and K. Jamieson, “ArrayTrack: A fine-grained indoor location system,” in Proc. NSDI, 2013, pp. 71–84.   
[35] L. Yang et al., “Tagoram: Real-time tracking of mobile RFID tags to high precision using COTS devices,” in Proc. 20th Annu. Int. Conf. Mobile Comput. Netw., 2014, pp. 237–248.   
[36] L. Yang et al., “Frogeye: Perception of the slightest tag motion,” in Proc. IEEE INFOCOM, Apr./May 2014, pp. 2670–2678.   
[37] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: Wireless indoor localization with little human intervention,” in Proc. 18th Annu. Int. Conf. Mobile Comput. Netw., 2012, pp. 269–280.   
[38] P. Zhang, J. Gummeson, and D. Ganesan, “BLINK: A high throughput link layer for backscatter communication,” in Proc. 10th Int. Conf. Mobile Syst., Appl., Services, 2012, pp. 99–112.   
[39] Y. Zhao, Y. Liu, and L. M. Ni, “VIRE: Active RFID-based localization using virtual reference elimination,” in Proc. ICPP, 2007, p. 56.

![](images/f39b2c8d660ed6e1bfff5880129ba97c391aec99da3954863222a41f09c3661c.jpg)



Longfei Shangguan (S’11) received the B.S. degree in software engineering from Xidian University in 2011, and the Ph.D. degree from HKUST in 2015. He is currently a Post-Doctoral Research Associate with the Computer Science Department, Princeton University. His research interests include pervasive computing and RFID system. He is a Student Member of IEEE and ACM.

![](images/e4bb5f02a936d29b3e567544e5147bc16c0ec56d9a7d44b041d083dc2557b988.jpg)



Zheng Yang received the B.Eng. degree from Tsinghua University in 2006, and the Ph.D. degree in computer science from the Hong Kong University of Science and Technology in 2010. He is currently an Associate Researcher with Tsinghua University. His main research interests include wireless ad hoc sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/3f15423efc6b34591d5b040db8034f0c6ceaa2d3e449374a00a39bb97bc91e23.jpg)



Alex X. Liu (M’08) received the Ph.D. degree in computer science from The University of Texas at Austin in 2006. He is currently an Associate Professor with the Department of Computer Science and Engineering, Michigan State University. His research interests focus on networking, security, and dependable systems. He received an NSF CAREER Award in 2009. He received the MSU College of Engineering Withrow Distinguished Scholar Award in 2011.

![](images/5073902ec1fb67fa5ad5088c8cc5a1f4e71f9fbc962a76b5d1fbb6a0fde9b92c.jpg)



Zimu Zhou (S’13) received the B.E. degree from Tsinghua University in 2011, and the Ph.D. degree from the Hong Kong University of Science and Technology in 2015. He is currently a Post-Doctoral Researcher with ETH Zurich. His research interests include wireless localization and mobile computing. He is a Student Member of the IEEE and ACM.

![](images/7439216e46ef7f5913d0ef856ce010fa6f2d7cf6538cfdc55ee4548c68ccefb5.jpg)



Yunhao Liu (S’03–M’04–SM’06–F’15) received the B.Eng. degree from Tsinghua University in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is currently a Chang Jiang Chair Professor and the Dean with the School of Software, Tsinghua University, China. He is a Fellow of IEEE.