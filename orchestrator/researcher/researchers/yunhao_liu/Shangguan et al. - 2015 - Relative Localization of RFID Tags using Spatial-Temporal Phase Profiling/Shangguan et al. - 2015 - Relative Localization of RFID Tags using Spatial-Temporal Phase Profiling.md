![](images/a33d75266da4084e30d406d9c7f91065f4afd41652babc593c984b9de56b071b.jpg)

# usenix

THEADVANCED

COMPUTING SYSTEMS

ASSOCIATION

# Relative Localization of RFID Tags using Spatial-Temporal Phase Profiling

Longfei Shangguan, The Hong Kong University of Science and Technology and Tsinghua University; Zheng Yang, Tsinghua University; Alex X. Liu, Michigan State University; Zimu Zhou, The Hong Kong University of Science and Technology; Yunhao Liu, Tsinghua University

https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/shangguan

This paper is included in the Proceedings of the 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI ’15).

May 4–6, 2015 • Oakland, CA, USA

ISBN 978-1-931971-218

Open Access to the Proceedings of the 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI ’15) is sponsored by USENIX

# Relative Localization of RFID Tags using Spatial-Temporal Phase Profiling

Longfei Shangguan1,2 Zheng Yang2 Alex X. Liu3 Zimu Zhou1 Yunhao Liu2

1Dept. of Computer Science and Engineering, Hong Kong University of Science and Technology 2School of Software and TNList, Tsinghua University

3Dept. of Computer Science and Engineering, Michigan State University, East Lansing, U.S.A. E-mail: longfei, yang, zimu, yunhao @greenorbs.com, alexliu@cse.msu.edu

# Abstract

Many object localization applications need the relative locations of a set of objects as oppose to their absolute locations. Although many schemes for object localization using Radio Frequency Identification (RFID) tags have been proposed, they mostly focus on absolute object localization and are not suitable for relative object localization because of large error margins and the special hardware that they require. In this paper, we propose an approach called Spatial-Temporal Phase Profiling (STPP) to RFID based relative object localization. The basic idea of STPP is that by moving a reader over a set of tags during which the reader continuously interrogating the tags, for each tag, the reader obtains a sequence of RF phase values, which we call a phase profile, from the tag’s responses over time. By analyzing the spatial-temporal dynamics in the phase profiles, STPP can calculate the spatial ordering among the tags. In comparison with prior absolute object localization schemes, STPP requires neither dedicated infrastructure nor special hardware. We implemented STPP and evaluated its performance in two real-world applications: locating misplaced books in a library and determining baggage order in an airport. The experimental results show that STPP achieves about 84% ordering accuracy for misplaced books and 95% ordering accuracy for baggage handling.

# 1 Introduction

# 1.1 Motivation

Many object localization applications need the relative locations of a set of objects as oppose to their absolute locations. The relative location of an object in a set of objects refers to the order of the object with respect to other objects along each dimension. The absolute location of an object refers to its coordinate value in each dimension. For example, in a library, to find misplaced books, we need to obtain the current order of the books on shelves rather than their absolute coordinate values.

# 1.2 Limitations of Prior Art

Although many schemes for object localization using Radio Frequency Identification (RFID) tags have been proposed [11, 13, 17–20, 23], they mostly focus on absolute object localization. They are not suitable for relative object localization because of two reasons. First, as the error margin achieved by most absolute object localization schemes (e.g., [11, 13, 18, 23]) is still big, sorting objects based on their absolute coordinate values may not result in the correct ordering of all objects because the distance between two objects may be less than the error margin. For example, the state-of-the-art absolute object localization scheme PinIt achieves an accuracy of 16cm at the 90th percentile [18]; however, such an error margin of 16cm could allow a book to be incorrectly ordered several books away from its correct order on a bookshelf. Second, the absolute object localization schemes that can achieve small error margins require either dedicated hardware (such as USRP) [17] or multiple pre-deployed antennas as reference points [19, 20], which make them relatively harder and more expensive to deploy in practice. For example, the state-of-the-art scheme Togoram [20] can achieve millimeter localization accuracy; however, it relies on the collaboration of multiple reader antennas and requires sophisticated calibration process before putting into use.

# 1.3 Proposed Approach

In this paper, we propose an approach called Spatial-Temporal Phase Profiling (STPP) to RFID based relative object localization. STPP uses commercial off-the-shelf (COTS) RFID readers and passive tags and requires no pre-deployed infrastructure. The basic idea of STPP is that by carefully moving an RFID reader over a set of tags during which the reader continuously interrogating the tags, for each tag, the reader obtains a sequence of RF phase values, which we call a phase profile, from the tag’s responses over time. As a reader moves closer to (or further away from) a tag, the phase value that the reader obtains from interrogating the tag changes. Thus, the phase profile of each tag corresponds to the spatial changes of the reader with respect to the tag. By analyzing the temporal dynamics in the phase profiles of a set of tags, the reader can obtain the spatial ordering among the tags. Specifically, STPP is based on the observation that as we move the reader along a dimension in one direction, for any tag, its distance to the reader first decreases and then increases, and becomes the minimum when the reader is perpendicular above the tag along that dimension; in other words, the distance values are symmetric around the minimum distance. Thus, in this reader moving process, if the reader continuously interrogate the tag, the phase values that reader can measure from the tag responses are also symmetric around the perpendicular point. Based on the symmetry in this observation, by moving the reader along a dimension in one direction, we can determine the order that the tags become perpendicular with the reader along that dimension, which is the order of the tags. Furthermore, by moving the reader two times, each time along a different dimension in the two dimensional space, the reader can obtain the order of the tags along each dimension. Note that an equivalent way of moving the reader while keeping the tags stationary is to move the tags altogether (with the relative positions among tags preserved) while keeps the reader stationary. For example, for airport baggage handling systems, we can keep the reader stationary while the baggages move on a conveyor belt. Therefore, our relative localization scheme can handle applications in both tag moving and antenna moving cases.

For simplicity, this paper focuses on relative object localization in a two dimensional space (i.e., locating the relative order of tags on a plane). The straightforward solution to achieve this is to move the reader two times, each time along a different dimension in the two dimensional space. In this paper, we propose to achieve two dimensional object localization by moving the reader only once along any dimension. This is based on our observation that given a sequence of objects aligned along a dimension, as we move the reader along that dimension in one direction, the larger the distance between the reader moving trajectory and that dimension, which are in parallel, the smaller the phase changes as the reader moves. Thus, given a set of objects placed within $x _ { 1 }$ and $x _ { 2 }$ (where $x _ { 1 } \leq x _ { 2 }$ along the X dimension) and within $y _ { 1 }$ and $y _ { 2 }$ (where $y _ { 1 } \leq y _ { 2 }$ along the Y dimension) as shown in Figure 1, if we move the reader along the X dimension from $x _ { 1 }$ to x2 perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $\left( { { x } _ { 2 } } , { { y } _ { 2 } } \right)$ , objects with smaller values on the Y dimension will have smaller phase changing rate; similarly, if we move the reader along the X dimension from $x _ { 1 }$ to x2 perpendicularly above the line from $\left( x _ { 1 } , y _ { 1 } \right)$ to $\left( x _ { 2 } , y _ { 1 } \right)$ , objects with larger values on the Y dimension will have smaller phase changing rate. Based on this observation, by moving the reader along the X dimension from $x _ { 1 }$ to x2 perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $\left( x _ { 2 } , y _ { 2 } \right)$ (or the line from $\left( x _ { 1 } , y _ { 1 } \right)$ to $( x _ { 2 } , y _ { 1 } ) )$ , we can determine the order of the objects along the Y dimension for any point on the X dimension, in addition to obtaining the order of the objects along the X dimension; in other words, we can determine the relative location of all objects in the two dimensional region.

![](images/5003b93a5525763aff79a9f21a5e842a9fdfbd1a4d4dc118b4ddec40737d42fe.jpg)



Figure 1: Illustration of STPP approach

Our STPP approach achieves relative object localization without calculating the absolute coordinate values of tags. It has two key features in comparison with prior absolute object localization schemes. First, STPP requires no dedicated infrastructure. In contrast, prior RFID based object localization schemes (e.g., [11, 18]) often require dedicated infrastructure such as carefully deployed anchor tags or antennas as reference points. Second, STPP uses COTS RFID readers and tags, and requires no special hardware. In contrast, prior RFID based object localization schemes (e.g., [17]) often require special hardware such as USRP.

# 1.4 Technical Challenges and Solutions

There are three key technical challenges in building a relative object localization system using our STPP approach. The first challenge is to achieve high accuracy. In STPP, phase profiles often come with noises and missing data points due to multi-path self-interference [22], which makes finding the perpendicular point for each tag challenging. To address this challenge, in this paper, we first acquire the symmetric part of each phase profile, which we call a V-zone. Within the V-zone of each phase profile, we further perform quadratic fitting on the incomplete phase values to complete the profile.

The second challenge is to achieve high robustness. As the mobile reader is often moved manually, the phase profile will be stretched when the movement slows down or compressed when the movement speeds up. To address this challenge, we use the Dynamic Time Warping (DTW) technique to find the V-zone within each phase profile. DTW compresses or stretches the profiles with the goal of minimizing the distance between these profiles. It naturally compensates for the warps of phase profiles and is robust to varying reader moving speed.

The third challenge is to achieve low latency. The time warping distance is calculated using dynamic programming algorithm in O(MN) time complexity, where M and N are the lengths of a phase profile and its reference phase profile, respectively. This process can take time, especially for long phase profiles. Furthermore, as there are typically a large number of tags for localization, $e . g .$ , in a library there are millions of books, detecting the V zone for each tag’s profile would incur large computational overhead. To address this challenge, we perform DTW on the coarser grained representation of phase profiles. Specifically, given a phase profile with length M, we first split it into $\frac { \mathbf { \mathcal { \overline { { M } } } } } { w }$ segmentations where each segment is of length w. In each segmentation, we record its maximum and minimum phase values, as well as the start and end points of this segment on the phase profile. After the segmentation, this coarser grained phase profile is used for V zone detection. Using segmentation, we thus can reduce the time complexity of DTW from O(MN) down to $\begin{array} { r } { O ( \frac { M } { w } \frac { N } { w } ) = O ( \frac { M N } { w ^ { 2 } } ) } \end{array}$ ( MNw2 ).

# 1.5 Key Contributions

This paper represents the first study of relative object localization. Specifically, we make three key contributions in this paper. First, we propose the concept of spatialtemporal phase profiling, which can be used for RFID based relative object localization. Second, we propose algorithms to capture the spatial-temporary dynamics of RF phase profiles and algorithms to determine the tag order along each dimension. Third, we implemented STPP and evaluated its performance in two real-world applications: locating misplaced books in a library and determining the baggage order in an airport. The experimental results show that we achieve about 84% ordering accuracy for misplaced books and 95% ordering accuracy for baggage handling.

The rest of this paper proceeds as follows. In Section 2, we discuss the difficulties on relative localization and the concept of spatial-temporal phase profiling (STPP). In Section 3, we present the design details of our STPP based relative localization system. In Section 4, we present the evaluation results of our system. In Section 5, we present our findings in deploying our system in two real-world applications. In Section 6, we present the limitation and future works. In Section 7, we review related work. We conclude this paper in Section 9.

# 2 Spatial-Temporal Phase Profiling

In this section, we first discuss the difficulties that we experienced in our initial attempts to directly use the information that can be measured by commercial readers towards relative localization. Then, we introduce the concept of phase profiling and show how it can capture the spatial-temperal phase dynamics that helps us to achieve relative localization.

# 2.1 Initial Attempts

As an RFID reader sweeps over a set of tags and keeps querying them, the reader can obtain the following information that can be impacted by the changes in the spatial relationship between the tags and the readers: tag identification order, the Received Signal Strength Indication (RSSI), and the received signal phase value. We next explain the reasons that we did not use these three types of information for relative localization.

Tag Identification Order: The Class1 Generation2 (C1G2) RFID standard [4] specifies two tag identification protocols: frame slotted ALOHA [3] and tree walking [10]. Unfortunately, in both protocols, the order that the tags are identified does not correspond to the order that the reader moves across them. In frame slotted ALOHA, the identification order depends on the random numbers that tags choose by themseleves. In tree walking, the order depends on the IDs stored in the tags.

![](images/594c7974e0afb098e2891b9a0a8ef5c99d943690ca4309592540329b6ebe17ab.jpg)



(a)

![](images/1767eb6a4934c1d59c84f190424af2dda2555768ddc7e67ca4210978b6e3d1dc.jpg)



Figure 2: RSSI values measured over time for two tags

RSSI: RSSI measures the power of received radio signal, which is inverse proportional to the distance between the tag and the reader (more precisely, the reader antenna) [6]. As a reader moves across a set of tags, for each tag, the RSSI values measured by the reader should increase and then decrease because the distance between the tag to the reader first decreases and then increases; thus, by ordering the tags according to the time that their peak RSSI values appear, the reader obtains the order of the tags along the moving direction. Unfortunately, this works only in theory because of the multiple paths that the signal traverses. To evaluate the multi-path impact, we conducted an experiment by attaching tags to the books on a shelf and moving the reader from left to right as shown in Figure 2(a). Figure 2(b) shows the RSSI values that the reader measures over time for two tags labeled 01 and 02, where tag 01 is placed 13cm to the left of tag 02. The left and right vertical lines corresponds to the time that the reader passes through tag 01 and 02, respectively. From this figure, we first observe that for both tags, their RSSI values fluctuate and their peak RSSI values appear before the reader moves across them. Second, the order of the two tags based on the time that their peak RSSI values appear is inconsistent with the actual tag order.

RF Phase Values: Phase is a basic attribute of a signal along with amplitude and frequency. The phase value of an RF signal describes the degree that the received signal is offset from sent signal, ranging from 0 to 360 degrees. Let l be the distance between the reader antenna and the tag, the signal traverses a round-trip (2l) in each backscatter communication. Apart from the RF phase rotation over the distance, both the antenna and the tag will introduce additional phase distortion. Specifically, let $\theta _ { T x } , \ \theta _ { T A G } ,$ , and $\theta _ { R x }$ be the phase rotation introduced by the reader’s transmission circuit, the tag’s reflection characteristic, and the reader’s receiver circuits, respectively. The phase measurement θ output by the reader thus can be expressed as:

$$
\left\{ \begin{array}{l} \theta = (2 \pi \frac {2 l}{\lambda} + \mu) \mod 2 \pi \\ \mu = \theta_ {T x} + \theta_ {R x} + \theta_ {T A G} \end{array} \right. \tag {1}
$$

where λ is the wavelength, μ is system noise. Most commercial RFID readers (such as ImpinJ R420 [1]) are able to report θ as the difference of the transmitted and the received signal. Given the ultra-high working frequency of the commercial passive RFID system, it is possible to achieve mm-level ranging accuracy in theory [20]. However, as the phase is a periodic function that repeats every λ in the distance of signal propagation, we cannot use phase value to pinpoint relative tag locations.

# 2.2 Phase Profile

The basic idea of our approach is that by carefully moving an RFID reader over a set of tags during which the reader continuously interrogating the tags, for each tag, the reader obtains a sequence of RF phase values, which we call a phase profile, from the tag’s responses over time. Considering Figure 1 where the set of tags are placed within $x _ { 1 }$ and x2 along the X dimension and within y1 and $y _ { 2 }$ along the Y dimension, suppose we move the reader along the X dimension from x1 to x2 perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $\left( x _ { 2 } , y _ { 2 } \right)$ . Taking tag 01 as an example, its distance to the reader first decreases until the reader is perpendicular above tag 01, and then increases. According to Equation 1, the phase of the received signal will also decrease first and then increase. Since the range of any phase value is [0, 2π), when this phase value decreases to 0, it immediately jumps to 2π. This process repeats until the reader reaches the perpendicular point right above tag 01, where the received phase stops decreasing and starts to increase from a certain value within [0,2π); when the phase value increases to 2π, it will immediately drop to 0 and then increases again. Such periodic change of phase values is reflected visually as follows: (1) The phase profile of each tag has a “V-zone” where its bottom occurs at the time when the reader is perpendicular above the tag. (2) Multiple curves are symmetrically distributed on both sides of the V-zone where each curve except the V-zone spans the whole range of [0,2π). A curve is called one period of the phase profile.

Given a layout of tags and the reader, their relative positions and the reader moving speed, assuming the speed is steady, we can calculate the phase profile of each tag, which we call the reference phase profile. Consider tags 01 and 02 and the reader in Figure 1, and suppose the reader moves at a constant speed of 0.1m/s along the line from $x _ { 1 }$ to x2 perpendicularly above the line from $( x _ { 1 } , y _ { 2 } )$ to $\left( { { x } _ { 2 } } , { { y } _ { 2 } } \right)$ . Suppose the distance between $x _ { 1 }$ and $x _ { 2 } ,$ , the height of the reader, and the distance from tag 02 to the line from $( x _ { 1 } , y _ { 2 } )$ to $\left( { { x } _ { 2 } } , { { y } _ { 2 } } \right)$ are 3m, 1m and 0.5m, respectively. Figure 3(a) shows the reference phase profiles of tags 01 and 02 when their distance is 5cm. This figure shows that the phase profiles of tag 01 and tag 02 have similar V-zone patterns.

![](images/ce6926a68800d568f24d00bd69308e4058f011856b6cc5b270e53f8836f16b9c.jpg)



(a) X dimension spacing = 5cm

![](images/76261c7afcac3e9072f6e61c20ab8a5b82dc9612268494707ba34e4a8f1edc15.jpg)



(b) X dimension spacing = 10cm   
Figure 3: Reference phase profile along X-axis

Given the phase profiles of multiple tags, the order that the reader passes through the tags along the X-axis is consistent with the order that the V-zones reach their bottom. By ordering the V-zones according to the time that they reach their bottoms, we can order the tags along the X-axis. Figure 3(a) shows that the V-zone of tag 01 reaches its bottom earlier than that of tag 02, which is consistent with the order that the reader passes through the tags. Furthermore, the longer the distance between two adjacent tags, the longer the time duration between the bottoms of two V-zones is. For example, Figure 3(b) shows the reference phase profiles of tags 01 and 02 when their distance is 10cm. As we increase the distance between the two tags from 5cm to 10cm, the time duration between the two V-zones also increases.

Given the phase profiles of multiple tags, the larger the bottom phase value of a V-zone is, the longer the distance between the tag that corresponds to the V-zone and the reader. By ordering the V-zones according to the phase value of their bottoms, we can order the tags along the Y-axis. Figure 4(a) shows that the V-zone bottom phase value of tag 04 is smaller than that of tag 01, which means that tag 04 is farther away than tag 01 with respect to the reader. Furthermore, the larger the two bottom phase values of two V-zones differ, the larger the distance between the two corresponding tags along the Y-axis. Figure 4(a) and (b) shows the phase profiles of tag 01 and 04, whose distances along the Y-axis are 5cm and 10cm, respectively. We observe that by increasing the tag distances from 5cm to 10cm, the distances between the bottom phase values of the two corresponding V-zones increases.

![](images/4fe24e86be50a72b2a491e7a453aadf474098189a60b5a16ae953164afd2a67b.jpg)



(a) Y dimension spacing = 5cm

![](images/877f687f36de2090e49c671f35c71c19f8d3f74cca661123b9e49063916d7a63.jpg)



(b) Y dimension spacing = 10cm   
Figure 4: Reference phase profile along Y-axis

To validate the above observations from reference phase profiles, we reproduce the layout of tags in Figure 1 on a white board. We attach an RFID reader on a shopping cart and wheel the cart along the X-axis in the positive direction. The speed of the cart is also set to be 0.1m/s. Figure 5 and Figure 6 shows the two measured phase profiles. From these figures, we can derive the same observations as above. Besides, we also found that due to channel instability, the phase profiles outside the V-zone are fragmentary. It is thus error-prone to connect the whole profile into a big V-zone for tag ordering.

![](images/abd26570b30b20a3e8183327e8df1f0761d27ab62186d5bfb837c9884d8071a0.jpg)



(a) X dimension spacing = 5cm

![](images/d5c1ebdf001193e417322238636a8718626759d8f8056582662a67b4b42d2026.jpg)



(b) X dimension spacing = 10cm

Figure 5: Measured phase profile along X-axis   
![](images/126df3df7ee7727a98e96e0a0ca2f48cea01dbcf2b35b240960f3e96c8d2f8d0.jpg)



(a) Y dimension spacing = 5cm

![](images/cc9ddcee2b51f3e3ec840ca0924f36ff4c6aca21be8fee95f340bf2fe0e347bc.jpg)



(b) Y dimension spacing = 10cm   
Figure 6: Measured phase profile along Y-axis

# 3 System Design

In this section, we present the details of our STPP approach to obtain the order of the tags along the X- and Yaxis, respectively. Without loss of generality, we assume that the reader moves along the X-axis from left to right.

# 3.1 Tag Ordering along X-axis

The profile segment within the V-zone differs from the other parts of the phase profile from two aspects. First, it changes continuously without jumping from 0 to 2π. Second, it is self-symmetric around the time point that the reader is perpendicular with the tag, which we call the perpendicular point. A straightforward solution to detect the V-zone is to use a sliding window to find the profile segment that satisfies these two properties. However, in reality, due to multi-path self-interference, the phase profile often has missing values within the V-zone as shown in Figure 6(a). Thus, this solution is unreliable for V-zone detection.

# 3.1.1 Detecting V-zone with Time Warping

Our basic approach is to match the measured phase profile against a pre-calculated reference phase profile, and try to find where the V-zone appears in the measured phase profile. As the reader is often hand held and moved manually, the phase profile become stretched when the movement slows down and compressed when the movement speeds up during the movement. Thus, subsequence matching algorithms (such as the KMP algorithm [7]) will not work for our V-zone detection. To find the place where the V-zone appears, we need to stretch or compress the calculated profile to match the corresponding V-zone on the given phase profile.

To address this issue, we use the Dynamic Time Warping (DTW) technique to match the V-zone in the calculated phase profile against the measured phase profile. DTW is a transformation that automatically compresses or stretches a sequence with the goal of minimizing the distance between these sequences. It naturally compensates for the shifts among different phase profiles caused by the varying reader moving speed. The input to the DTW algorithm consists of a reference phase profile P of length N and a measured phase profile Q of length M. DTW first constructs a distance matrix $D _ { M \times N }$ where each element $D _ { i , j }$ is defined as the Euclidean distance between $p _ { i }$ and $q _ { j } \colon$

$$
D _ {i, j} = \left\| p _ {i} - q _ {j} \right\|
$$

where $p _ { i }$ and $q _ { j }$ are the $i ^ { t h }$ and $j ^ { t h }$ elements of the phase profiles P and Q, respectively. The output of the DTW algorithm is a warping path $\mathcal { L } = \{ l _ { 1 } , l _ { 2 } , . . . , l _ { k } \}$ such that the total cost $C _ { \mathcal { L } }$ of the warping path L is minimized:

$$
\underset {\mathscr {L}} {\operatorname{argmin}} \quad C _ {\mathscr {L}} = \sum_ {i = 1} ^ {k} D _ {x (l _ {i}), y (l _ {i})}
$$

where $l _ { i } = ( x , y ) \in [ 1 : M ] \times [ 1 : N ]$ for $l \in [ 1 : k ]$ .

To generate the optimal warping path, DTW constructs the cost matrix $C _ { i , j }$ using dynamic programming. The optimal substructure is defined as:

$$
C _ {i, j} = D _ {i, j} + \min \left\{C _ {i, j - 1}, C _ {i - 1, j}, C _ {i - 1, j - 1} \right\}
$$

Figure 7(b) shows the matching result using DTW. It shows that the V-zone of the measured profile matches well with that of the reference profile. On the reference profile, as the start and the end point of the V-zone is known a priori, it is easy to locate the corresponding Vzone on the measured profile.

![](images/c9e4415e4fb350d56d9e573958e3fc2453a4adb8c53a48ff275ad8cd5aed4d1c.jpg)



(a) Before warping

![](images/7d128ef7ee907e8c5cf29aa6cba09a4c821ac7713f8d46411ef0c09c9813992b.jpg)



(b) After warping   
Figure 7: V-zone detection using DTW

# 3.1.2 Optimizing V-zone Detection Efficiency

The core of DTW is dynamic programming whose complexity is O(NM). This process may take some time because the phase profiles may be long (e.g., typically around 400 samples) and the number of tags may be large. To improve efficiency, we apply DTW on the coarser grained representations of phase profiles. Given a phase profile $P ,$ we split it into d segments: $S _ { P } =$ $\left\{ s _ { P , 1 } , s _ { P , 2 } , . . . , s _ { P , d } \right\}$ . For each segment $^ { S } P , i ,$ , we further record its segment range $s _ { P , i } ^ { R }$ and time interval $s _ { P , i } ^ { T }$ . Formally, the segment range $s _ { P , i } ^ { R }$ is defined as:

$$
s _ {P, i} ^ {R} = \{s _ {P, i} ^ {L}, s _ {P, i} ^ {U} \}
$$

$$
s _ {P, i} ^ {L} = \min \left\{p _ {a},..., p _ {b} \right\}, s _ {P, i} ^ {U} = \max \left\{p _ {a},..., p _ {b} \right\}
$$

where $s _ { P , i } ^ { L }$ and $s _ { P , i } ^ { U }$ are the minimum and maximum phase values within $i ^ { t h }$ segment. a and b are the begin and the end index of the phase profile within this segment. Note that if within a segment the phase value jumps from 0 to 2π, we split the segment into two segments at that point so that no segment contains such phase value jumping. Figure 8 shows an example segmentation. In this figure, we represent the original profile with 25 segments, with each consists of its segment range and time interval.

Given two phase profiles P and Q, we first acquire their segmented presentation $S _ { P }$ and $S _ { Q } .$ with each contained J and K segments, respectively. Similar to DTW, we construct a distance matrix $D _ { J \times K } .$ , where each element $D _ { i , j }$ is defined as the distance between the segmentation $s _ { P , i }$ and $s _ { Q , j }$ . It is intuitively the distance of their two closest points:

![](images/5efa324cf513a49e409edd3888c995dd18a2ffe2c28fbf78a724296530286c2b.jpg)



Figure 8: Phase profile segmentation;

$$
D _ {i, j} = \left\{ \begin{array}{c l} \| s _ {P, i} ^ {L} - s _ {Q, j} ^ {U} \|, & i f (s _ {P, j} ^ {L} > s _ {Q, j} ^ {U}) \\ \| s _ {Q, j} ^ {L} - s _ {P, i} ^ {U} \|, & i f (s _ {Q, i} ^ {L} > s _ {P, i} ^ {U}) \\ 0, & o t h e r w i s e \end{array} \right.
$$

After compute each element in the matrix $D _ { J \times K }$ , we align $S _ { P }$ and $S _ { Q }$ using dynamic programming. The optimal substructure defined as follows:

$$
C _ {i, j} = \min \left\{s _ {P, i} ^ {T}, s _ {Q, j} ^ {T} \right\} \cdot D _ {i, j} + \min \left\{C _ {i, j - 1}, C _ {i - 1, j}, C _ {i - 1, j - 1} \right\}
$$

Using segmentation, we reduce the time complexity of DTW from O(MN) down to $\begin{array} { r } { O ( \frac { M } { w } \frac { N } { w } ) = O ( \frac { M N } { w ^ { 2 } } ) } \end{array}$ w2 where w is the length of each segment. We need to choose the value for w carefully to tradeoff between efficiency and accuracy. The larger the w is, the more efficient DTW is, but the less accurate our V-zone detection is due to the unclear outline of the segmented phase profile. In Section 4, we investigate how to select a proper w value.

After we detect the V-zone for a tag in its phase profile, we search for the time point with the smallest phase value within the V-zone. However, due to the multi-path selfinterference, the measured phase profile often contains noise and missing values, which may cause the nadir of the V-zone profile to wrap around. In this work, we use the quadratic fitting technique to minimize such influences. Once the fitting function is determined, by referring the time point when the fitting function achieves the minimum value, we sort this tag together with those tags whose V-zones have already been determined. Figure 9 shows a concrete example. In this example, three tags are attached on a white board, then the antenna moves along the X-axis from the right to the left at a speed of approximate 0.1m/s. The distance between tag 03 and tag 01, tag 01 and tag 02 are 15cm and 2cm, respectively. After performing the quadratic fitting on these phase profiles, we see a clear lag between the phase profiles of these three tags. Based on the time point when the fitting function achieves the minimum value, we further determine the order of these three tags as 01, 02, and 03, which is coherent with the actual order.

![](images/c76b3b2a5e7b952a5650d2812a026324a43fd5b6b284e21053e9bf428a47bc45.jpg)



Figure 9: Tag ordering with quadratic fitting   
Figure 10: Reader movement model

![](images/6b42e648bfca18333a31849026e541ff858c3dfb16e8b3cd7e4cd06930dac97b.jpg)



Figure 11: Examples of coarse representation of V-zone profile

# 3.2 Tag Ordering along Y-axis

The movement model of the reader when it passes by two tags at a constant speed v is shown in Figure 10. Intuitively, the radial velocity $\nu _ { R }$ of the tag is inverse proportional to its distance with respect to the antenna. That is, the larger the distance between the tag and the moving trajectory of the reader, the lower the radial velocity of this tag. The lower radial velocity further leads to a smaller phase changing rate, therefore a shallower V-zone profile. Based on the above observation, we propose another segmentation based method to determine the tag order along the Y-axis.

# 3.2.1 Tag Ordering via V-zone Profile Comparison

The basic idea to determine tag ordering along the Y-axis is to comparing their phase changing rates. One straightforward method is to first derive the span and offset of the quadratic model, and then uses these two parameters to calculate the phase changing rate. However, in reality, if the tags are placed close to each other (such as 5cm), the V-zone profiles of these tags would be similar and would lead to similar curve fitting results. In STPP, we compare the phase changing rate by jointly considering multiple local phase profile segments within the V-zone profile. Notice that the V-zone profile may vary in length due to the random access property of ALOHA protocol [3]. Thus, we first split each profile into equal number of segments to facilitate the comparison. Within each segment of the V-zone profile, we calculate the mean value of phase values. Therefore, given a phase profile $P ,$ we can get its coarse representation by using the set of mean values, i.e., we represent the V-zone profile $P$ by $S ( P ) = \{ s { _ { P , 1 } } , s { _ { P , 2 } } , . . . , s _ { P , k } \}$ , where k is the number of segments and $s _ { P , k }$ is the mean value of $k ^ { t h }$ segment. $\mathrm { A v } -$ eraging over all phase values within each segment will eliminate the impact of noise introduced in phase value measurements. Since each segment corresponds to one specific time window, the average phase value also reflects the accumulated phase changing rate within each segment. By calculating the average phase values, we can improve the robustness of our scheme. Figure 11 shows an example coarse representation of the V-zone profile. In this figure, the phase value within each segment is represented by its mean value.

To determine the order of two tags along the Y-axis, we compare the coarse representation of their V-zone profiles, say $S ( P )$ and $S ( Q )$ , using the following metric:

$$
O (P, Q) = \sum_ {i = 1} ^ {k} \lceil \frac {s _ {P , i} - s _ {Q , i}}{s _ {P , i}} \rceil
$$

Generally, if the phase changing rate of P is smaller than that of Q, for each segment $i , s _ { P , i }$ will be larger than $s _ { Q , i } .$ . Therefore, $O ( P , Q )$ will be close to k. On the contrary, if the phase changing rate of $P$ is larger than that of $Q , s _ { P , i }$ will be no larger than $s _ { Q , i } .$ . Here $O ( P , Q )$ will be close to 0 accordingly. Therefore, we can determine the tag order along the Y-axis based on the value of $O ( P , Q )$ .

# 3.2.2 Optimizing the Ordering Efficiency

The core of determining the tag order along the Y-axis is to compare the V-zone profiles by using the metric $O ( P , Q )$ . This process may take some time because we need to compare each pair of phase profiles. For example, it takes $\overset { - } { \frac { M ( M - 1 ) } { 2 } }$ comparison to determine the order of M tags along the Y-axis. To speed up this process, we further introduce a new metric $G ( P , Q )$ to measure the gap between two phase profiles $P$ and $Q .$ . It is defined as follows:

$$
G (P, Q) = \sum_ {i = 1} ^ {k} \| s _ {P, i} - s _ {Q, i} \|
$$

where $\| s _ { P , i } - s _ { Q , i } \|$ is the Euclidean distance between the mean phase value $s _ { P , i }$ and $s _ { Q , i } .$ . In an intuitive level, $G ( P , Q )$ is proportional to the physical spacing of these two tags. $i . e . ,$ , the larger the physical spacing between these two tags, the larger the $G ( P , Q )$ will be. For M tags, we then randomly choose one tag as the pivot. Let $P$ be the V-zone profile of this pivot, then we calculate $O ( P , Q )$ and $G ( P , Q )$ between P and each profile Q of the remaining tags. By doing so, we can not only determine the relative order between the pivot tag and other tags, but also acquire the relative distance of these tags. Therefore, we can order these M tags with only $M - 1$ comparison, which is significantly smaller than $\frac { \operatorname { \bar { M } } ( M - 1 ) } { 2 }$ .

![](images/05bdacb0f2750cbaa6c8ecca461858edb75b22472cba0d8f5d9a0893487acdc6.jpg)



Figure 12: Window size vs. accuracy;

![](images/43b8b25679150b2a1c3b947a72c45c63c40ad035ce00ece24df8d7691f595a9d.jpg)



Figure 13: Tag moving case

![](images/c874d2a49a1acd8e04fff5c507b13ba9cb2347635d60334920b139bc5b2d2fb3.jpg)



Figure 14: Antenna moving case

<table><tr><td rowspan="2" colspan="2"></td><td colspan="6">Tag population size within a reading zone</td></tr><tr><td>n=5</td><td>n=10</td><td>n=15</td><td>n=20</td><td>n=25</td><td>n=30</td></tr><tr><td rowspan="2">Tag moving case</td><td>along X-axis</td><td>0.963</td><td>0.954</td><td>0.952</td><td>0.937</td><td>0.906</td><td>0.884</td></tr><tr><td>along Y-axis</td><td>0.917</td><td>0.903</td><td>0.878</td><td>0.874</td><td>0.863</td><td>0.856</td></tr><tr><td rowspan="2">Antenna moving case</td><td>along X-axis</td><td>0.873</td><td>0.865</td><td>0.861</td><td>0.852</td><td>0.841</td><td>0.813</td></tr><tr><td>along Y-axis</td><td>0.809</td><td>0.806</td><td>0.798</td><td>0.779</td><td>0.765</td><td>0.754</td></tr></table>

Table 1: Tag population vs. ordering accuracy

# 4 System Evaluation

# 4.1 Implementation

Hardware: Our system consists of a COTS UHF RFID reader, a directional antenna, and a set of passive tags. To account for device diversity, we have tested our system using different hardware, including an ImpinJ R420 reader, an ImpinJ Threshold RFID Antenna IPJ-A0311, an Alien ALR-8696-C antenna, and four types of passive tags: Alien ALR-9610, ALN-9662, ALN-9634, and ALN-9720. For diversity, we choose four types of tags of different size and shape.

Software: We implemented our algorithms in Java, which were executed on a Lenovo PC equipped with an Intel(R) Celeron G530 CPU and 4G RAM. The PC is connected to the RFID reader via Ethernet. The reader is programmed to continuously query the RFID tags on the $\dot { 6 } ^ { t h }$ channel in the 920 ∼ 926 MHz ISM band and returns the signal phase for each tag reply.

# 4.2 Deployment

One deployment issue is to determine the number of periods that the reference phase profile should contain. In theory, the reference phase profile should contain the same number of periods as the measured profile. In order to obtain a proper reference phase profile, we put the reader 30cm (a common distance between a librarian and a bookshelf) away from the tags. We collected phase profiles by holding the reader and passing 200 tags for 15 times. Of the 3,000 phase profiles that we collected, more than 97% of them contain 4 partial or complete periods. Thus, we generate a 4-period reference phase profile as the default setting in our experiment.

Another deployment issue is to determine the height that the antenna should be moving across the tags. As STPP uses the phase changing rate of each tag to determine its relative order along the Y-axis, we need to place the antenna at a height such that the tags with different Y coordinates differ in phase changing rate. This can be ensured if all the tags are either above or below the antenna along the Y-axis since their antenna to tag distances would differ from each other. For example, in library, we can put the antenna at the bottom of the lowest shelf so that each tag has a different distance to the reader, which is moving along the X-axis. In our experiments, we simply place the antenna at a height below all tags.

# 4.3 Micro-Benchmarks

Experimental setup: We have two experimental cases: the antenna moving case and the tags moving case. In the antenna moving case, we partition 150 tags into 3 groups and attach them on a white board as shown in Figure 15(a). The antenna is fixed on a wheeled chair which is pushed manually at a rough speed of 0.3m/s. This experimental setup simulates the misplaced book locating application in libraries where a librarian moves a reader across a bookshelf.

In the tag moving case, we use a conveyor belt and a tape to compose a mobile RFID system as shown in Figure 15(b). The antenna is placed 1m away from the tape and 1m above the top of the winder. We attach a set of tags on the tape, which move at a constant speed of 0.3m/s. This case simulates the baggage handling application in airports where baggage or cargos attached with RFID tags are delivered on a conveyor belt.

Evaluation Metrics: We mainly use the metric of ordering accuracy defined in Equation 2. A tag is ordered incorrectly in a sequence of tags if and only if the detected order of the tag is not equal to the actual order of that tag. For example, suppose there are five tags and the correct order of these five tags is 1-2-3-4-5. If the output of our scheme is 1-2-4-3-5, then we immediately know that the tag 4 and tag 3 are ordered incorrectly, and thus the accuracy is 3/5=60%.

![](images/2049b29d7494082ee157ae457d939331b4e96ad1ba3731d28aeaaac7fc8e0322.jpg)  
Figure 15: Experimental setup

$$
\text { Ordering   Accuracy } = \frac {\# \text { of   tags   ordered   correctly }}{\# \text { of   tags   in   total }} \tag {2}
$$

Determining a proper window size w: In general, a larger window size contributes to higher efficiency but lower accuracy. As shown in Figure 12, the ordering accuracy of STPP remains high for small window sizes (e.g., nearly 98% when w = 3), decreases slightly with window sizes increased from 3 to 5, and drops sharply for window sizes larger than 5. Therefore we set w to be 5 in our experiments to tradeoff between latency and accuracy.

Tag-to-tag distance vs. Ordering accuracy: As shown in Figure 13, when each tag pair is placed very close (e.g., 2cm apart), STPP achieves an ordering accuracy of only 42% along the X-axis and 23% along the Yaxis in the tag moving case. The ordering accuracy then increases dramatically as we slightly increase the tag-totag distance: 92% and 88% along the X-axis and the Yaxis respectively for tag-to-tag distance of 10cm. The similar trend is observed for the antenna moving case as shown in Figure 14 where the ordering accuracy remains high for tag-to-tag distances larger than 8cm.

Tag population vs. Ordering accuracy: Commercial RFID reader have limited reading rate. If the reading zone of the antenna contains a large number of tags, we will have under-sampling of phase readings which potentially degrades the ordering accuracy. We change the tag populations from 5 to 30 within the reading zone of the antenna and examine the performance of STPP. The distance between two adjacent tags is randomly chosen in the range of [2cm,10cm]. We present the experimental results in Table 1 to compare the data values. As shown in this table, when the tag population is small within the reading zone of the antenna, e.g., n = 5, STPP achieves satisfactory performance, with ordering accuracies of above 90% and 80% for the tag moving and antenna moving cases, respectively. As we steadily increase the tag population within the reading zone, the ordering accuracy degrades gradually in both two cases. When the tag population reaches 30, the ordering accuracy remains at an acceptable level, with average accuracies of above 0.85 and 0.75 for tag and antenna moving cases, respectively. This result indicates that the performance of STPP will degrade a little bit when the tag population increases.

# 4.4 Macro-Benchmarks

We evaluated STPP in comparison with the following four schemes that are implementable on COTS RFID readers:

1. G-RSSI: This is a straightforward scheme that uses RSSI value changes to infer tag orders along the Xaxis.   
2. OTrack [16]: This scheme combines RSSI dynamics and tag successful reading rates to determine tag orders along the X-axis.   
3. Landmarc [13]: This scheme uses multiple reference tags to calculate the absolute location of a tag in 2 dimensional region.   
4. BackPos [11]: This scheme uses RF phase values and the hyperbolic positioning technique to calculate the absolute location of a tag in 2 dimensional region.

Our experimental results show that STPP significantly outperforms the other four schemes for the accuracy of relative localization. We compare the ordering accuracy of these schemes under various layout settings as shown in Figure 16. In each setting, we repeat the experiment 100 times and use their average ordering accuracy values. The distance between adjacent tags ranges from 1cm to 10cm. As shown in Figure 17, G-RSSI and Landmarc achieve similar low ordering accuracy values of below 25% along both axes. Using both RSSI dynamics and tag successful reading rates, OTrack outperforms G-RSSI and Landmarc, yet can only reach an ordering accuracy of below 50%, which is too low for real-world applications. With more precise signal measurement, BackPos can locate each tag and further distinguish their relative order with an average ordering accuracy of 80%. In contrast, STPP achieves an average ordering accuracy of more than 88%.

Our experimental results show that STPP scales better than the other four schemes as adjacent tag distance decreases. To perform this evaluation, we choose a population of 20 tags and vary the adjacent tag distance from 100cm to 10cm. Figure 18 shows the box plot of the accuracy values of different schemes as we vary the distance. The whisker indicates values outside the upper and lower quartiles. From this figure, we can observe that the median accuracy of STPP is significantly higher than that of other four schemes. Besides, the likely range of variation (IQR) of STPP is the smallest as the adjacent tag distance decreases.

![](images/265c4af36bf78368dfca94adc6fb10884379e5cfe810e9263b8f6472b221c69c.jpg)



(a) Test case 1

![](images/4deb06b8547412e8e91df4cc447cb55bb5e31ba4c71d894a557e54b8fa25abd1.jpg)



(b) Test case 2

![](images/31483ddf69f50f0c13c67276b29b39d47b480cfa7ec1087b0209cfd2b1a2249b.jpg)



(c) Test case 3

![](images/303f14bebf9b0e87c5b3c9d4e8a177b2409be305258705fee8b48bf57ecd2197.jpg)



(d) Test case 4

![](images/d4342c2bb4100bc368760a1d28037c2da388b65c6306c2ec7bab8e0a3041693c.jpg)



(e) Test case 5

Figure 16: Tag layout settings   
![](images/8aa37de02827c2fb53329198ae6c5b418cb0637a4ebf36653d76bad39d4f5d52.jpg)



Figure 17: Accuracy vs. schemes

![](images/98c113c94bdbb6aea5e9b3991d0ae6a7675e780263911d6f9c39b1aca6c800fc.jpg)



Figure 18: Accuracy vs. tag distance

![](images/ff4bad799411c62fb10c3b44a21df06dfe38a68717ab9bcdf81adefb6d0448d1.jpg)



Figure 19: Accuracy vs. population

Our experimental results show that STPP scales better than the other four schemes as tag population size increases. To perform this evaluation, we choose 10cm to be the adjacent tag distance and vary the tag population from 5 to 30. As G-RSSI, Landmarc, and BackPos are insensitive to tag population sizes, we thus compare STPP with OTrack. Figure 19 shows the box plot of the accuracy values of different schemes as we vary the tag population size. From this figure, we observe that likely range of variation (IQR) of STPP is significantly smaller than that of OTrack.

# 5 Case Studies

We deployed our STPP based relative RFID tag localization system in two real-world applications: a misplaced book locating system in a library and a baggage handling system in an airport. In this section, we present our experimental results with these two case studies. Note that our relative localization scheme is not limited to these two applications. Other applications (such as locating suspicious baggage and warehouse stocktaking) can also benefit from our localization scheme.

# 5.1 Misplaced Book Locating in Library

A major task for librarians is to locate misplaced books and relocate them to the right place. Note that library books are typically strictly ordered based on their IDs so that borrowers can find a specific book easily. To help locate misplaced books, we deploy our STPP system in a school library. For one bookshelf in the library, we attach 90 RFID tags to 90 books, one tag per book. These books are placed on three levels. The thickness of each book spans from 3cm to 8cm. We attach an RFID antenna on a cart and manually push it across the bookshelf from left to right, as shown in Figure 20. Here we simply put the antenna at the height

![](images/e054d3fe52f0d72570d975f3f8477ed1898d633e828c68b062711eb96dd7c97b.jpg)



Figure 20: Locaking misplaced books

This case study also shows that STTP can achieve high relative localization accuracy. We sweep these 90 books over 50 times. The result shows that our relative localization scheme achieves an accuracy of 0.84 on average. This implies that in most cases, STPP can precisely pinpoint the relative location of the misplaced book. For the remaining cases, although STPP cannot correctly find the relative location of tags, it still helps the librarian to narrow down the searching space. Figure 21 shows the order of the books that we obtained in one experiment, whee each dot represents a book and each cross represents a book that we ordered incorrectly. Note that the gap between two dots reflects the distance between two tags.

From this figure, we observe that all incorrectly ordered books are those thin ones as their tags are much closer.

![](images/0785ffa466a735d00780a51c5d421d268c8301d229322fa17aef24eee2a29d07.jpg)



Figure 21: Layout of detected books by STPP

We also conducted experiments to evaluate the ability of STPP in detecting misplaced books. We randomly picked one book, two books, and three books from a bookshelf and inserted them into a differently chosen location on this bookshelf. This location is randomly chosen from the range of 2 books away from the original place to 10 books away. Each case was repeated 100 times. The detection success rate is shown in Table 2.

<table><tr><td></td><td>Detection success rate</td></tr><tr><td>1 book</td><td>98%</td></tr><tr><td>2 books</td><td>97%</td></tr><tr><td>3 books</td><td>98%</td></tr></table>

Table 2: Result of misplaced book detection by STPP

# 5.2 Baggage Handling in Airport

To avoid mis-delivered baggages, baggage handling systems in airports need to find the order of the baggages on the conveyor belt [2]. Although the size of one baggage item is usually large, the distance between adjacent tags (attached to different baggages) can be rather close due to the arbitrary orientation of baggage on the convey belt. It is thus critical to pinpoint the relative order of baggage with high resolution. We deployed our STPP system at Terminal One, Sanya Phoenix airport, Sanya, Hainan Province, China. Three RFID reader antennas are deployed at three places on the tunnel as shown in the left figure in Figure 22(b). Based on the tag ordering information, the visualization module displays each baggage and tracks its movement on the baggage conveyor belt, as shown in the right figure in Figure 22(b). As reference tags and antennas, which are the essential part of the localization scheme Landmarc and BackPos, cannot be deployed on the commercial baggage handling system, we thus compare STPP with OTrack and G-RSSI in this case study. Our experiments were carried out during three periods: 7:00AM 9:00AM, 13:00PM 15:00PM, and

![](images/6b6f363198a49600153b824e69cefa3130184de411f349e3db72c8c28dbd8db3.jpg)  
(a) RFID tag for baggage check-in

![](images/091ee2f995e5d0e53a8c6cfc6234acf5399dad1d638db68df722c8b2c43e8c04.jpg)



(b) Baggage handling in Terminal One, Sanya Phoenix airport

![](images/884f6677e0ac2f5baaaacbe00f6852fcb53a391b3953790e8e068c4cc93e439d.jpg)



Figure 22: Baggage handling in the airport

19:00PM∼21:00PM, during which over 1,000 pieces of baggage from 9 flights are handled.

This case study shows that STTP can achieve high relative localization accuracy. Table 3 shows the accuracy results of STPP in comparison with G-RSSI and OTrack during the three time periods. During the peak hours of 7:00AM∼9:00AM and 19:00PM∼ 21:00PM, during which the distance between each baggage is typically smaller than 20cm, our STPP achieves accuracy values of 97% and 96%, respectively; whereas OTrack achieves an accuracy of 88% for both time periods and G-RSSI achieves accuracy values of 59% and 51%, respectively. During the off peak hours of 13:00PM 15:00PM, our STPP, OTrack, and G-RSSI achieve accuracy values of 97%, 95%, and 72%, respectively.

<table><tr><td></td><td>7:00~9:00</td><td>13:00~15:00</td><td>19:00~21:00</td></tr><tr><td>STPP</td><td>388/400=97%</td><td>224/230=97%</td><td>422/440=96%</td></tr><tr><td>OTrack</td><td>352/400=88%</td><td>218/230=95%</td><td>388/440=88%</td></tr><tr><td>G-RSSI</td><td>234/400=59%</td><td>166/230=72%</td><td>226/440=51%</td></tr></table>

Table 3: Accuracy of STPP, OTrack, and G-RSSI

We further examine the ordering latency of OTrack and STPP. In this trial of experiments, we use OTrack and STPP to detect the order of 100 baggages on a moving conveyor. The CDF of the ordering latency incurred by each scheme is shown in Figure 23. As the result indicates, the average latency of STPP is 1.473s, which is slightly hight than that of OTrack.

![](images/20cdf290d703bbc3cd4cbf3e40bc38fecd955e515fa259b3a20736be00a0f5b4.jpg)



Figure 23: Ordering latency of STPP and OTrack

# 6 Limitation and Future Works

Improving accuracy: Our accuracy still has room to improve. One possible direction is to sweep tags multiple times and average their results. In future, we plan to leverage the advanced signal processing techniques to minimize the phase noises and exploit the geometry relationship among tags to improve the localization accuracy.

Enhancing robustness: Currently we require the reader to move along a straight line that crosses the targeting items. However, the line may not be strictly straight in practice. In future, we plan to model the impact of irregular reader motions on the phase profile, and enhance the robustness of our relative localization scheme by filtering out phase values introduce by irregular reader motions.

Extending to 3-Dimensional space: Currently we focus on the relative tag localization in a 2D space. A straightforward approach to handle the 3D space is to move the reader three times, each time along a different dimension in the 3D space. Thus, the reader can obtain the order of the tags along each dimension. In future, we plan to study ways to extend our spatial-temporal phase profiling approach for 3D relative tag localization.

# 7 Related Work

RSSI based approach: Early RF-based localization schemes primarily rely on RSSI information to acquire the absolute location of an object [13, 16, 21, 23]. They typically pre-deploy tags densely on a monitoring region as anchors, and then use the RSSI values of these anchor tags as references to locate a specific tag [13, 23]. Succeeding works explore the anchor-free approach by either modeling the signal propagation process in complex environment [21] or taking a combination of various signal features (e.g. the RSSI and the tag’s reading rate [16]). The major limitation of RSSI-based approaches is that they are highly sensitive to multi-path propagation, and thus difficult to achieve high-precision localization. Furthermore, RSSI is also impacted by antenna gain [8], which adds uncertainty to localization accuracy.

Phase based approach: There is a growing interest in using phase values to estimate the absolute location of an object. Pioneer work uses hyperbolic localization techniques [11, 19] or Angle of Arrival (AoA) information [5,9,14] to locate tags by measuring the phase difference between the received signals at different antennas. To reduce the hardware deployment cost, state-of-the-art systems use synthetic aperture radar (SAR) to simulate multiple antennas to extract RF information [15,18]. For instance, by leveraging antenna motion, PinIt achieves a location accuracy on the order of centimeters [18]. Another line of work employs multiple antennas to construct a hologram for tag localization [12, 20]. Our work is inspired by the above works in phasebased tag localization, but we focus on leveraging reader mobility to generate phase profiles for tag localization. In this setting, PinIt [18] is perhaps most related to ours. It locates RFID tags by analyzing their multi-path profiles collected by a moving antenna. However, the intuition behind PinIt is that nearby RFID tags experience a similar multi-path environment and thus exhibit similar multi-path profiles. In contrast, the intuition behind our scheme is that by analyzing the spatial-temporal dynamics in the phase profiles of a set of tags, we can calculate the spatial ordering among tags. Moreover, PinIt relies on dedicated hardware (i.e., USRP) to capture the multi-path profile of each tag and requires densely deployed reference tags. In contrast, our scheme works on COTS devices and does not rely on any reference tags. Although both PinIt and our scheme leverage DTW metric and optimize its execution for tag localization, the targets of the DTW optimization in these two schemes are different. PinIt leverages derivative DTW (DDTW) technique to handle the power scaling problem, whereas our scheme optimizes the computational efficiency by applying the DTW on the coarse-grained representation of the phase profile.

# 8 Conclusions

In this paper, we propose the phase profiling approach to relative localization of RFID tags by exploiting the spatial-temporal dynamics in tag phase profiles. We show that relative localization can be achieved without the absolute location of tags. Our approach requires neither dedicated infrastructure nor special hardware. We implemented our approach and conducted experiments in two realistic case studies: locating misplaced books in a library and determining baggage ordering in an airport. The result shows that our approach can achieve high accuracy in realistic settings. This paper represents an early comprehensive study of relative localization of RFID tags. Our system can be used in a wide range of applications such as inventory control, asset management, and customer behavior tracking.

# 9 Acknowledge

We would like to thank the anonymous reviewers and our shepherd, Dr.Prabal Dutta, for providing valuable comments. This work is supported in part by the NSFC under grant numbers 61190110, 61171067, 61361166009, 61402338, 61472184, 61321491, 61272546, the NSFC Distinguished Young Scholars Program under Grant number 61125202, the Jiangsu Future Internet Program under Grant Number BY2013095-4-08, and the Jiangsu High-level Innovation and Entrepreneurship (Shuangchuang) Program.

# References

[1] Impinj. http://www.impinj.com.   
[2] The statistics of luggage missing in airport.   
http://gadling.com/2010/03/26/   
airlines-losing-3000-bags-every-hour every-day/.   
[3] Epc radio-frequency identity protocols. class-1 generation-2 uhf rfid. protocol for communications at 860 mhz to 960 mhz. EPC global, Jan 2005.   
[4] Uhf class 1 gen 2 standard v. 1.0.9. EPC global, Jan 2005.   
[5] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie. New measurement results for the localization of uhf rfid transponders using an angle of arrival (aoa) approach. In Proceedings of RFID, 2011.   
[6] D. M. Dobkin. The RF in RFID, Passive UHF RFID in Practice. Elsevier, 2008.   
[7] K. Donald, M. J. H. Jr, and P. Vaughan. Fast pattern matching in strings. SIAM Journal on Computing, 6, 1977.   
[8] J. D. Griffin and G. D. Durgin. Complete link budgets for backscatter-radio and rfid systems. IEEE Antennas and Propagation Magazine, 2009.   
[9] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar. Accurate localization of rfid tags using phase difference. In Proceedings of RFID, 2010.   
[10] C. Law, K. Lee, and K.-Y. Siu. Efficient memoryless protocol for tag identification (extended abstract). In Proceedings of DIALM, 2000.   
[11] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu. Anchor-free backscatter positioning for rfid tags with high accuracy. In Proceedings of INFOCOM, 2014.   
[12] R. Miesen, F. Kirsch, and M. Vossiek. Holographic localization of passive uhf rfid transponders. In Proceedings of RFID, 2011.   
[13] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil. Landmarc: Indoor location sensing using active rfid. Wireless Networks, 2004.   
[14] P. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. V. S. Rao. Phase based spatial identification of uhf rfid tags. In Proceedings of RFID, 2010.

[15] A. Parr, R. Miesen, and M. Vossiek. Inverse sar approach for localization of moving rfid tags. In Procedings of RFID, 2013.   
[16] L. Shangguan, Z. Li, Z. Yang, M. Li, and Y. Liu. Otrack: Order tracking for luggage in mobile rfid -of-\systems. In Proceedings of INFOCOM, 2013.   
[17] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus. Rf-compass: Robot object manipulation using rfids. In Proceedings of MOBICOM, 2013.   
[18] J. Wang and D. Katabi. Dude, where’s my card?: Rfid positioning that works with multipath and nonline of sight. In Proceedings of SIGCOMM, 2013.   
[19] J. Wang, D. Vasisht, and D. Katabi. Rf-idraw: Virtual touch screen in the air using rf signals. In Proceedings of SIGCOMM, 2014.   
[20] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: Real-time tracking of mobile rfid tags to high precision using cots devices. In Proceedings of MOBICOM, 2014.   
[21] L. Yang, Y. Qi, J. Fang, X. Ding, T. Liu, and M. Li. Frogeye: Perception of the slightest tag motion. In Proceedings of INFOCOM, 2014.   
[22] P. Zhang, J. Gummeson, and D. Ganesan. Blink: A high throughput link layer for backscatter communication. In Proceedings of MOBISYS, 2012.   
[23] Y. Zhao, Y. Liu, and L. M. Ni. Vire: Active rfidbased localization using virtual reference elimination. In Proceedings of ICPP, 2007.