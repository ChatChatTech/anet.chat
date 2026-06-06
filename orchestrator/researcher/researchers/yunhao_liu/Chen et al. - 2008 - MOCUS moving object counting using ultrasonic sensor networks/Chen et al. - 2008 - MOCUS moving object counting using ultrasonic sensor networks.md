# MOCUS: moving object counting using ultrasonic sensor networks

Quanbin Chen,\* Min Gao, Jian Ma, Dian Zhang, Lionel M. Ni and Yunhao Liu

Department of Computer Science and Engineering,

The Hong Kong University of Science and Technology,

Clear Water Bay, Kowloon, Hong Kong, PR China

E-mail: chenqb@cse.ust.hk

E-mail: mgao@cse.ust.hk

E-mail: majian@cse.ust.hk

E-mail: zhangd@cse.ust.hk

E-mail: ni@cse.ust.hk

E-mail: liu@cse.ust.hk

\*Corresponding author

Abstract: Counting the number of moving objects in a given area has many practical applications. By investigating a series of state-of-the-art technologies, we propose a Moving Object Counting approach using Ultrasonic Sensor networks (MOCUS). In MOCUS, we deploy a network of three-node ultrasound sensor clusters, with each cluster having one ultrasound transmitting node and two ultrasound receiving nodes. Such three-node sensor clusters can successfully offset interference problems and accurately detect the direction of moving objects. In order to cover a wide area, MOCUS employs multiple sensor clusters, forming a wireless sensor network. To alleviate the impact of object moving velocity, shape of objects and distinguish closely tied multiple objects, we introduce intra-cluster analysis and inter-cluster cooperation techniques. We deploy a MOCUS prototype in our lab and evaluate the design through extensive experiments.

Keywords: moving object counting; wireless sensor networks; ultrasound; clustering.

Reference to this paper should be made as follows: Chen, Q., Gao, M., Ma, J., Zhang, D., Ni, L.M. and Liu, Y. (2008) ‘MOCUS: moving object counting using ultrasonic sensor networks’, Int. J. Sensor Networks, Vol. 3, No. 1, pp.55–65.

Biographical notes: Quanbin Chen received his BE in Computer Science and Technology from Tsinghua University, Beijing, China in 2004. He is currently a PhD Candidate in the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology (HKUST). His current research interests include reliable transmission, routing and applications in wireless sensor networks.

Min Gao received his Masters in the Department of Computer Science and Engineering, at HKUST in 2005. He is currently a Project Manager at HKUST. His research interests include applications and manufacture in wireless sensor networks.

Jian Ma received his BSc in Computer Science from Peking University, Beijing, China in 2002. He is currently a PhD Candidate in the Department of Computer Science and Engineering at HKUST. His current research interests include topology control and localisation in wireless sensor networks.

Dian Zhang received her BE in Computer Science from Wuhan University of Technology, Wuhan, China in 1996 and earned a Masters in Computer Science and Engineering at HKUST in 2006. She is currently a PhD student in the Department of Computer Science and Engineering at HKUST. Her current research interests include localisation and applications in wireless sensor networks.

Lionel M. Ni earned the PhD in Electrical and Computer Engineering from Purdue University, USA, in 1980. He is Chair Professor and Head of the Computer Science and Engineering Department at HKUST. His current research interests cover all the aspects in wireless sensor networks.

Yunhao Liu earned the PhD in Computer Science and Engineering from Michigan State University, USA in 2004. He is currently an Assistant Professor in the Department of Computer Science and Engineering at HKUST. His current research interests include peer-to-peer computing, grid computing and sensor networks.

# 1 Introduction

A moving object counting system is intended to be a smart system, which is capable of recording information on how many objects, such as pedestrians or cars, have passed through a given area, such as a gate, a tunnel or an intersection. Such a system is also responsible for analysing the direction of each moving object.

There are numerous existing or proposed applications which need to count moving objects. For example, merchants are interested in the number of customers entering or leaving their shopping mall during a certain period. In crowded cities, the number of moving cars and moving people in each block and each street can help the traffic control centre to avoid traffic jams in advance. In a coal mine, it is necessary to determine the number of miners in each tunnel for safety reasons. Indeed, the number of moving objects, which we try to obtain in this work, is basic information required by most environmental monitoring systems.

The most popular technology used in current moving object counting systems is video analysis by computer vision algorithms. However, it cannot work in a dark environment like an underground coal mine. Using video also brings up the critical consideration of privacy concerns. Besides video, active infrared sensors can also detect moving objects by receiving the reflected infrared waves, but the detection range is limited. The use of pressure sensors requires predeployment in surface, which is impractical and costly.

After evaluating a variety of state-of-the-art technologies, we believe that ultrasound is the most appropriate sensing technology for counting moving objects based on the following observations. Firstly, it can work both indoors and outdoors, and in both sunlight and dark. Secondly, by not identifying individuals, privacy can be protected. Thirdly, the information retrieved by ultrasound sensors is relatively simple, so very few processing and communication resources are needed. Finally, the deployment of ultrasound sensors is much easier compared with pressure sensors, and the power requirement is much lower than that of infrared.

In this work, we propose a Moving Object Counting approach using Ultrasonic Sensor networks (MOCUS). Instead of using typical ultrasound sensor nodes, where each node has one ultrasound transmitter and one ultrasound receiver, MOCUS employs three-node ultrasound sensor clusters. Each cluster has one ultrasound transmitting node and two ultrasound receiving nodes. Such a three-node cluster approach can successfully offset interference problems and accurately detect the direction of moving objects. In order to cover a wide area, multiple three-node sensor clusters work together, forming a wireless sensor network. By intra-cluster analysis and inter-cluster cooperation, MOCUS works well with nearly 90% accuracy.

The rest of the paper is organised as follows. Section 2 highlights related work on moving object counting. We introduce preliminary ideas as well as basic tests in Section 3. Section 4 proposes the three-node sensor cluster approach. Ultrasound sensor network is introduced in Section 5. Implementation experiments and results are discussed in Section 6. Section 7 concludes the paper and lists some future work.

# 2 Related work

Moving object counting usually goes with moving object tracking. Intuitively, if we can track each of the moving objects, certainly we can count them. Moving object tracking, especially people tracking, is a hot area in the field of computer vision. For years, many researchers have focused on this topic. The basic idea is to track moving people by applying computer vision algorithms on sequences of images from a camera or synchronised images captured from multiple cameras (Cai and Aggarwal, 1998).

These video-based algorithms focus on distinguishing individuals rather than counting them, so that they always require huge computation and communication resources. Moreover, such algorithms usually fail when there is a crowd. Yang has proposed an alternative approach which directly estimates the number of people (Yang et al., 2003). In this system, groups of image sensors segment foreground objects from the background, aggregate the resulting silhouettes over a network, and compute a planar projection of the scene’s visual hull. Then, a geometric algorithm is employed to calculate the bounds on the number of people in each region of the projection. Although the authors claim that the image sensors rather than cameras can be attached on wireless sensor nodes, no results have been reported yet.

Commercial products on moving object counting have been released recently. Acorel, a French company, provides people counting systems in several areas. Their system provides a fully automatic solution to record how many people enter or exit a restricted area, such as the door of a bus. They adopt both active and passive infrared sensors. Active infrared sensors are used to determine the presence of a person, while passive infrared sensors are used to detect the infrared generated by the human body in order to differentiate the direction. A Swiss company, Dilax, also has similar products. These systems, both in Dilax and Acorel, are based on infrared technology, which requires higher voltage and consumes more power than ultrasound sensors in order to achieve the same coverage. Furthermore, many different devices such as centralised data analysis device, data transmitting devices and cables are required in their architectures.

Recently, wireless sensor networks have a wide range of applications (Dutta et al., 2005; Mainwaring et al., 2002; Ni et al., 2003; Singhvi et al., 2005; Xu et al., 2004), most of which are aimed at environment monitoring, object localisation and tracking.

# 3 Hardware and preliminary tests

In this section, we first introduce the hardware used in MOCUS, and then show some preliminary feasibility tests.

# 3.1 Hardware specification

MOCUS utilises the popular sensor node hardware, Mica2 mote. Each Mica2 mote performs wireless communication and data processing, and the tiny mote also has an extension interface where the ultrasonic sensor resides. Besides the hardware, the particular operating system TinyOS (Hill et al., 2000) is specifically designed for these tiny nodes, and a component-based programming language called nesC (Gay et al., 2003) is used in this system.

The ultrasonic sensor board we are using is designed by the Institute of Computing Technology, Chinese Academy of Sciences (Ni et al., 2005). There are two transducers, one for transmitting ultrasonic waves and the other for receiving waves. Both transducers are mounted on the tiny sensor board. In order to simplify the circuit design, we utilise only one phase loop lock connecting two transducers to the microcontroller on Mica2 mote, rather than having a separate microcontroller for two transducers. Therefore, the clock of the microcontroller on Mica2 mote is employed to generate a 40 kHz electric wave, which has exactly the same frequency as the predefined ultrasonic wave. Due to the simple design, the sensor board suffers a long latency introduced by phase loop lock.

# 3.2 Preliminary tests

One of the transducers on the ultrasound sensor board sends out the ultrasound wave continuously. Once the other transducer receives the reflected waves, we can record this detection event and put a timestamp on it.

In ideal cases, one moving object corresponds to exactly one detection event, so that we can obtain the number of moving objects by counting the number of detection events. However, one moving object often causes multiple detection events, because several different reflected waves can be generated due to the irregular surface of the moving object. As shown in the example in Figure 1(a), a moving object results in four detections. To address this issue, a straightforward approach is that we assume a threshold $T _ { \mathrm { m i n I t v } }$ and when the current detection has an interval bigger than $T _ { \mathrm { m i n I t v } }$ with last detection, it is counted as a new object. For example, in Figure 1(a), the result of counting analysis on this sequence of detections will be one, if $T _ { \mathrm { m i n I t v } }$ is 0.4 sec as depicted in Figure 1(b). If $T _ { \mathrm { m i n I t v } }$ is 0.35 sec, the counting result will be two as shown in Figure 1 (c). Clearly, the threshold $T _ { \mathrm { m i n I t v } }$ has a significant impact on the counting accuracy. If it is too high, two near-by fore-and-aft moving objects may be counted as one object, while one slowly moving object may lead to replicate counting when $T _ { \mathrm { m i n I t v } }$ TminItv is too small. We carefully select this parameter based on experimental results.

Figure 1 (a) the sequence of detection events caused by one moving object; (b) one count when $T _ { \mathrm { m i n I t } }$ is set to be 0.4 sec and (c) two counts when $T _ { \mathrm { m i n I t v } }$ TminItv is set to be 0.35 sec   
![](images/68f030289e0883cf7ecb2d8cdfeb4f176bb07907028e38c001a356f3ba892193.jpg)



![](images/1700ecb80c7eb551ce5cc8ec84af67584246c7138229a61810de10d968d6b318.jpg)



(b)

![](images/a5ee2f439aca1fec1f4c825d2c59a54fcb1bbe1403476e400fe1746035048e1a.jpg)



(c)

# 4 Ultrasonic sensor cluster

The preliminary tests show that we can only get a sequence of timestamps of detection events from each node. Based on this information, MOCUS can count the moving objects in ultrasound’s sensing range. One challenge is how to determine the direction of the moving object by analysing the detection events. We define the ultrasonic sensor cluster as a group of multiple sensor nodes combined together, which not only detects moving objects, but also estimates the directions of motion. In MOCUS, an ultrasonic sensor cluster is the basic functional unit. In this section, we will first introduce the node pairing approach. The three-node sensor cluster, used in MOCUS, will be described later. Lastly, we extend the three-node sensor cluster to high fidelity sensor clusters.

# 4.1 Node pairing approach

Intuitively adopting a pair of nodes, which are standing fore-and-aft, we can detect a moving object as well as its direction by comparing the detection timestamps of the pairing nodes. We call this simple approach, the node pairing approach, as depicted in Figure 2(a). In this approach, two sensor nodes are involved, each of which can detect the moving object in its sensitivity range independently by sending out ultrasound waves and receiving it. By cooperating with each other, they can easily tell the direction of the moving object.

Although straightforward, node pairing approach works well in simple situations. However, it fails to handle complex situations. For example, in Figure 2(a), an object moves from the left side to the right side, but it changes the direction when it just passes the detection region of the left-side sensor node. We call this a turn-around problem. As a result, the left-side sensor node will detect the object twice, while the right-side sensor node detects nothing. It is difficult for the system to make a decision on whether to count or not. In order to alleviate this exception, we can set them up close to each other. However, the unpredictable interference introduced by multiple ultrasound transmitters arises if they are too close to each other. What is worse, since the transmitting and receiving devices are on the same tiny board, it is inevitable that there may be some noise at the receiver side.

Figure 2 (a) node pairing approach and (b) three-node sensor cluster approach for moving object counting   
![](images/c077a5d9316afbcc805f7087074f918fecf3161cac22edcabdc97055a4b4749b.jpg)



# 4.2 Three-node sensor cluster

In order to solve those problems presented above, we propose a three-node sensor cluster approach, shown in Figure 2(b). In this approach, three sensor nodes are closely deployed. One sensor node acts as the ultrasound transmitting node, and the other two nodes play the role of ultrasound receivers. In other words, only one transducer on each board is adopted as either the transmitter or receiver. Differing from node pairing approach, there is only one ultrasound transmitter in the three-node sensor cluster approach. As a result, there is no unpredictable interference introduced by multiple nearby transmitters. Furthermore, because three transducers reside on three different sensor boards, less noise is introduced on the receiver side.

As depicted in Figure 3, when an object is moving from the left side to the right side, we can get two sequences of detection timestamps from those two ultrasound receiver nodes, node 1 and node 2. We name the receiver node 1 as $R _ { \mathrm { 1 } }$ , and the receiver node 2 as $R _ { 2 } .$ Without losing generality, the detection timestamps retrieved from $R _ { \mathrm { 1 } }$ and R2 are denoted as: $t _ { 1 } ^ { R _ { 1 } } , t _ { 2 } ^ { R 2 } , . . . , t _ { N 1 } ^ { R _ { 1 } }$ and $t _ { 1 } ^ { R _ { 2 } } , t _ { 2 } ^ { R _ { 2 } } , . . . . , t _ { N _ { 2 } } ^ { R _ { 1 } }$ , respectively, where $N _ { \mathrm { _ { 1 } } }$ and $N _ { _ 2 }$ are the numbers of timestamps.

Figure 3 Simple case when using three-node sensor cluster   
![](images/4db4f3b24c3e56d6246ce9402985a036b2b237efaff274c70c06d05233f8ed0d.jpg)



Upon getting a sequence of timestamps on a receiver node, the first step is to differentiate timestamps caused by different moving objects. Applying the idea introduced in Section 3, we make use of a threshold $T _ { \mathrm { m i n I t v } }$ as shown in Equation (2). After separating sequences of timestamps according to different objects, the receiver node will calculate a diagnostic value based on each timestamp sequence. For example, the diagnostic value of a sequence of timestamps can be the average time of all the timestamps, shown in Equation (1). Instead of transmitting the whole sequence of timestamps, the receiver nodes are only required to report the diagnostic value. Based on these two diagnostic values from two ultrasound receivers, motion direction can be determined by a simple comparison. However, we still need to make sure whether these two diagnostic values from two nodes originate from the same object. Thus, another condition should be satisfied, that is, the difference between the two diagnostic values cannot exceed a threshold $T _ { \mathrm { m a x G a p } } ,$ maxGap, as described in Equation (3). Since the two ultrasound receiver nodes are close to each other in the three-node sensor cluster, it is impossible for node 2 to detect a regular moving object much later, say 5 sec, than node 1 does. Usually, the detection periods from two nodes overlap with each other as depicted in Figure 4.

$$
D \left(t _ {1} ^ {R _ {i}},..., t _ {N _ {i}} ^ {R _ {i}}\right) = \frac {1}{N _ {i}} \sum_ {j = 1} ^ {N _ {i}} t _ {j} ^ {R _ {i}}, \quad i = 1, 2 \tag {1}
$$

$$
t _ {j + 1} ^ {R _ {i}} - t _ {j} ^ {R _ {i}} \leq T _ {\min \text { Itv }}, \quad i = 1, 2 \quad 0 <   j <   N _ {i} \tag {2}
$$

$$
\left| D \left(t _ {1} ^ {R _ {1}},..., t _ {N _ {1}} ^ {R _ {1}}\right) - D \left(t _ {1} ^ {R _ {2}},..., t _ {N _ {2}} ^ {R _ {2}}\right) \right| \leq T _ {\max \text { Gap }} \tag {3}
$$

We call the Equations (1)–(3) as the temporal correlation in our counting analysis, which differentiate multiple moving objects in some period. The temporal correlation holds in most of common situations, but it implies that a moving object cannot move too slowly in order to be correctly estimated by the three-node sensor cluster, which is determined by the threshold $T _ { \mathrm { m a x G a p } } .$

Figure 4 An instance of object detection timestamps recorded by two receiver nodes in three-node sensor cluster   
![](images/2f4843c08ada4c20ff0d6f93705916afd722707fc16012fdffe8ce4555a80b54.jpg)



Deployment of sensor nodes is another issue beyond theory in order to achieve high accuracy. A well-tuned ultrasound receiver can cover the expected region. The overlap of sensing areas between two receivers also needs to be considered carefully. As the surface of a moving object cannot always be flat, it is possible that the reflected wave will first reach the receiver on the other side of the direction of motion as illustrated in Figure 5. In this case, a wrong direction would be determined. Besides the irregular surface of the moving object, another reason may be due to the overlap of the sensing areas of the two receivers’. From our experience, we validate that the wrong direction determination caused by irregular surface of moving objects can be alleviated by controlling the overlap between the sensing areas of the two receivers.

Figure 5 Irregular surface of moving object can lead to wrong determination of direction. Node 2 detects the object earlier than node 1   
![](images/aca6bb1be6211244b302cf6fe9556eba6d4fd672cf3a56536aff706cfc72caa6.jpg)



# 4.3 High fidelity sensor cluster

The three-node sensor cluster can function as a basic unit to count moving objects in two opposite directions, which are parallel to the line passing through the two receivers, shown in Figure 6(a). In practice, two-direction analysis is enough in many situations, such as for an entrance, a door or a corridor. In complex cases, however, we have to analyse more than two directions.

Figure 6 Three different sensor clusters for basic moving object counting (a) three-node sensor cluster (b) four-node sensor cluster and (c) seven-node sensor cluster   
![](images/812645e20c1efa3484e1c39cb2652dc8e50858dc50ceb3324b2d1c57cbe6d8c6.jpg)



In Figure 6(b), the four-node sensor cluster, can analyse at least six directions, two opposite directions for each receiver pair. Actually, by applying some analysis methods on all the three receivers, we can get a much more accurate direction result rather than just those six fixed ones. In principle, more the receivers, more the accurate direction we can obtain. Ideally, the seven-node sensor cluster, shown in Figure 6(c), can achieve more accurate orientation analysis. However, the analysis method in seven-node sensor cluster is more complicated than the four-node sensor cluster for the same accuracy.

# 5 Ultrasound sensor network

Since the coverage of ultrasound sensors is limited, the proposed ultrasound sensor cluster cannot cover a wide area. To solve this problem, we extend the ultrasound sensor cluster to ultrasound sensor network in this section. We will first give the overview of our system, and then describe the intra-cluster analysis to get the local counting result. Lastly, intercluster cooperation will be introduced.

# 5.1 System overview

MOCUS aims to estimate the number of moving objects, especially the pedestrians, at some restricted areas, such as an entrance, an exit or a corridor. Usually, pedestrians only have two possible directions in a restricted area, moving in or moving out. Roughly, we can set up nodes with ultrasound sensors above the pedestrians, such as the ceiling, as illustrated in Figure 7. According to our preliminary tests, each node can detect moving objects in its coverage independently.

Figure 7 System overview of moving object counting system based on ultrasonic sensor networks   
![](images/75f1b897d4a78077237bdfe5a9fe10c3f95230526cd37502d8372af5cab433d1.jpg)



We employ the three-node sensor cluster as our basic detection unit. In order to cover a large area, multiple three-node sensor clusters are used, as depicted in Figure 8. These three-node sensor clusters should cover all the possible paths of moving objects. Considering the possible applications, we assume that the moving objects only have two possible directions as shown in Figure 8.

Figure 8 The projective figure for the ultrasound sensor network   
![](images/03c8d19521be34f2dc6de6ae8855a9eeeecc80b89abbb23b4eed797711cda1ca.jpg)



The system functions as follows. Initially, each ultrasound receiver node will process intra-cluster analysis with its receiving partner in the three-node sensor cluster. Based on this, the direction of individual moving object can be estimated. However, the same object may be detected by other clusters, so subsequently, the counting should be estimated through inter-cluster cooperation and each cluster will make a local decision on counting. Finally, these counting results will be aggregated.

# 5.2 Intra-cluster analysis

We name the ith three-node sensor cluster as $C _ { i } ,$ as shown in Figure 9. The ultrasound transmitter in $C _ { i }$ is $S _ { i } { : }$ , while the two ultrasound receivers are $R _ { 2 i }$ and $R _ { 2 i ^ { + } 1 } ,$ respectively. For receiver $R _ { _ { 2 i } } ,$ , the timestamps for each detected reflected wave are denoted as:

$$
t _ {1} ^ {R _ {2 i}}, t _ {2} ^ {R _ {2 i}}, \dots , t _ {N _ {2 i}} ^ {R _ {2 i}}
$$

where $N _ { { _ { 2 i } } }$ denotes the number of reflected ultrasound waves detected by $R _ { 2 i }$ .

Figure 9 Intra-cluster analysis and intercluster cooperation algorithm   
![](images/3713ec48220f6ab4d7dd2904cad51d623b84245ce737f5b7c5c1fc9aa6dc2389.jpg)



In order to simplify the analysis, we assign an ultrasound receiver node in each three-node sensor cluster as the coordinator node. The other ultrasound receiver node will send the diagnostic value of a timestamp sequence to the coordinator. These timestamps should be caused by a single pedestrian, satisfying Equation (2). The number of these timestamps will also be sent to the coordinator node for inter-cluster cooperation. On the coordinator node, the same analysis will be processed on its own detection timestamps. By applying the temporal correlation Equation (3) on these diagnostic values, the coordinator node will try to match them with those caused by the same pedestrian. Without generating any result at the current stage, the coordinator node just stores the matched or unmatched diagnostic values as well as the number of timestamps for each diagnostic value.

# 5.3 Inter-cluster cooperation

Recall that we assume the direction of motion is mainly along each three-node sensor cluster. Another assumption is that a regularly moving pedestrian can only be detected by one three-node sensor cluster or two adjacent clusters if we properly deploy the ultrasound sensor network. This is the case in most situations such as a wide entrance, a wide corridor or a road. Here, regularly moving refers to moving with an ordinary speed along the two directions mentioned above.

We propose a distributed algorithm to let the coordinator node in each sensor cluster make an independent decision on whether to count the detection as a pedestrian or not, by comparing the detection information from its neighbouring coordinators. Before we go into the details of the algorithm, we give a simple example to explain the basic idea. As shown in Figure 9, a moving object is passing the area along the arrow, and nodes $R _ { { \scriptscriptstyle 2 i \mathrm { ~ - ~ } 2 } } , R _ { { \scriptscriptstyle 2 i \mathrm { ~ - ~ } 1 } } , R _ { { \scriptscriptstyle 2 i } }$ and $R _ { 2 i } +$ will detect a series of reflected waves, the numbers of which are denoted as $N _ { 2 i \mathrm { ~ - ~ } 2 } , \ N _ { 2 i \mathrm { - } 1 } , \ N _ { 2 } i$ and $N _ { { _ { 2 i + 1 } } }$ , respectively. We have the timestamps of each detected reflected wave. In one test in this scenario, $N _ { 2 i \textrm { - } 2 , } N _ { 2 i \textrm { - } 1 } , N _ { 2 i }$ and $N _ { 2 i ^ { + } I }$ are 2, 4, 7 and 8, respectively. In other words, both of these two sensor clusters can detect the moving object and determine the direction of motion. However, only one moving object exists. How can these two clusters cooperate with each other to give the correct result? A straightforward observation is that the ith sensor cluster in Figure 9 has detected nine more reflected waves than the (I – 1)th sensor cluster, because the moving path is closer to the ith sensor cluster. Therefore, when the (i – 1)th sensor cluster found its detected reflected waves are fewer than its neighbour’s, the ith sensor cluster, which has the same detection information at the same time period, will in high probability not count this moving object. On the other hand, for the ith sensor cluster, when it found that it has detected much more reflected waves than its neighbour, the (i – 1)th sensor cluster, it will in high probability count this moving object.

According to our basic observation, that the nearer the path of the moving object is to the sensor cluster, the more reflected waves should be detected by that cluster, we develop a probabilistic algorithm for this distributed system. After $C _ { i }$ estimates the direction of the moving object, it queries its two neighbouring clusters for the number of detected reflected waves which satisfy the temporal correlation and motion direction condition. Temporal correlation requires that the detection at a neighbour cluster side must happen in the same period, and motion direction condition refers to the same result of motion direction. $C _ { i }$ may get response information from one, both or neither of its neighbours. If $C _ { i }$ has no response from neighbours, it counts the moving object with a probability 1.0. If it gets the number of detected reflected waves from one or both of its neighbours, the probability of getting a single count on $C _ { i }$ is shown in Equation (4).

$$
P _ {\text { count }} ^ {C _ {i}} = \left\{ \begin{array}{l l} 1. 0 & \Delta N \geq N _ {\text { thr } - A} \text {   or   } N _ {2 i} + N _ {2 i + 1} \geq N _ {\text { thr } - B} \\ 0 & \Delta N \leq - N _ {\text { thr } - A} \\ \max \left(\operatorname{Frac} \left(1 + \frac {\Delta N}{N _ {\text { thr } - A}}\right), \frac {N _ {2 i} + N _ {2 i + 1}}{N _ {\text { thr } - B}}\right), & \text { others } \end{array} \right. \tag {4}
$$

where

$$
\Delta N = \left\{ \begin{array}{l} N _ {2 i} + N _ {2 i + 1} - N _ {2 i - 1} - N _ {2 i - 2} \\ 2 (N _ {2 i} + N _ {2 i + 1}) - N _ {2 i - 1} - N _ {2 i - 2} - N _ {2 i + 3} - N _ {2 i + 2} \end{array} \right. \tag {5}
$$

This probabilistic method is only initialised when the cluster receives the response information from at least one of its neighbouring clusters. Either one-neighbour response or two-neighbour responses are distinguished by Equation (5). The function Frac() is to get the fraction part of the floating number. $N _ { { \mathrm { u r } } _ { \perp } }$ A and $N _ { { \mathrm { u h r } } \_ B }$ are two thresholds. This probabilistic method tries to include the basic concept that the farther the moving path is away from the three-node sensor cluster, the smaller is the number of reflected waves detected by that cluster. From the equation, if the ith sensor cluster has enough reflected waves, above the threshold $N _ { \mathfrak { q } _ { \mathrm { t h r } _ { - } B } , }$ in the period, it will count the moving object once. If it has many more reflected waves than that of its neighbours, above the threshold $N _ { \mathrm { t h r } \_ A } ,$ it will also count the moving object with a probability 1.0 and vice versa. Otherwise, we will get the probability according to the ratio of the two thresholds.

Sometimes, intra-cluster analysis cannot be successfully done in estimating the motion direction, when only one ultrasound receiver has detection information. In other words, there will be unmatched diagnostic values stored in the coordinator nodes of each cluster. Actually, even when only one ultrasound receiver in the sensor cluster has detected the moving object, it can collaborate with neighbouring clusters by using their detection information. For example, the moving object is detected by $R _ { 2 i - 2 }$ 2 and $R _ { 2 i + 1 } ,$ , the correct result can still be made by intercluster cooperation.

# 5.4 Synchronisation

Time synchronisation among sensor nodes is necessary in MOCUS system. Clusters should be synchronised at least with its two neighbouring clusters. Many synchronisation algorithms have been proposed in wireless sensor networks, such as RBS (Elson et al., 2002), TPSN (Ganeriwal et al., 2003) and FTSP (Maroti et al., 2004), all of which can achieve high resolution, even at 1µs. However, the overhead is rather high due to heavy computation and communication involved.

In MOCUS, as we target to count moving objects, especially pedestrians, we do not need to synchronise the sensor nodes at the microsecond level due to pedestrians’ velocity. Instead, millisecond level synchronisation is enough. Another characteristic of MOCUS is that it is usually deployed locally to monitor a restricted area, so we can use a server node, such as the gateway node, with a high transmission power setting that can be heard by all the other nodes directly, to synchronise other nodes by broadcasting its own time periodically.

# 6 Experiments

In this section, we will first introduce our experiment environment, the setup of our experiment and our evaluation metrics. Then, a series of experiments are conducted to verify the concept of three-node sensor clusters. Finally, we present a testbed of an ultrasound sensor network based on several three-node sensor clusters.

# 6.1 Experiment setup

We conduct our experiments in our lab. The sensor nodes are attached to the ceiling of the lab at a height of 2.5 m from the ground to the ultrasound transducers. People of different heights are employed as our pedestrians. In every experiment, we measure each case 80 times and report the average.

Several performance evaluation metrics are adopted in this section. Correct refers to the percentage of the correct counts with correct direction result. Wrong Direction means the percentage of correct counts, but with wrong direction result. Replicate and Miss refers to the percentage of replicate counts and missing counts, respectively. Actually, most of the replicates are duplicates, only a few are triplicates. All of these four metrics are based on each moving object, while Overall means the overall accuracy during a certain period.

# 6.2 Three-node sensor cluster

Aiming to explore the capability of a single three-node sensor cluster, we try to measure the accuracy under different situations.

The first important factor which will affect the accuracy is the velocity of moving objects. Intuitively, a fast moving object has a high probability to be missed by the ultrasound sensor cluster. As we described before, we have to separate each single pedestrian from multiple pedestrians according to the timestamp sequence. The parameter $T _ { \mathrm { m i n I t v } }$ is responsible for differentiating pedestrians on each receiver, while the parameter $T _ { \mathrm { m a x G a p } }$ is responsible for differentiating pedestrians in intra-cluster analysis. In our experiments, we adjust these two parameters manually to achieve high accuracy in common situations. As shown in Figure 10, for the moving velocity between 0.5 and 2 m/sec, we almost have 100% accuracy. The setting of $T _ { \mathrm { m i n I v } }$ and $T _ { \mathrm { m a x G a p } }$ maxGap are 0.35 and 0.5 sec,, respectively. For the two objects moving fore-and-aft case, we can differentiate them as two objects successfully when the distance between them is more than 20 cm. However, different moving velocities have different lower bounds, and 20 cm is the lower bound for the velocity of 1 m/sec.

A fast moving object may be undetected by the ultrasound sensor cluster. We solve this by adding an additional redundant three-node sensor cluster along the direction of motion. Indeed, a fast moving object problem rarely occurs in our proposed applications, particularly indoors. At very low velocities, there are replicate countings when the object moves slowly, such as 0.25 m/sec.

Figure 10 Counting accuracy according to different moving velocities   
![](images/a40540fa7aaec33dc813013eb601156b4be8ad924a30a100e60c0fd866e8144d.jpg)



The ceiling placement of a three-node sensor cluster cannot differentiate one slowly moving pedestrian from two close fore-and-aft moving pedestrians, because the sequences of detection timestamps produced in these two cases can be identical. For most cases, one moving object can lead to multiple detections on one ultrasound receiver. However, it is reasonable to assume that these multiple detections would occur in a very short restricted period, which implies that each object moves with a regular speed, not too slowly, for example.

Other than the velocity of moving objects, the height of moving objects also influences the accuracy. In second experiment, three pedestrians of different heights pass right under the ultrasound sensor cluster with a speed of 1 m/sec. As shown in Figure 11, taller pedestrians are detected with higher accuracy. The explanation for this is quite straightforward. The ultrasound wave will attenuate during the propagation. The higher the object is, the shorter the propagation path of the ultrasound wave is. In this case, the reflected wave from a taller object has more energy than that from a shorter object. Due to the sensitivity of the ultrasound receiver, there is a higher probability that the reflected wave from a shorter object will not be intercepted by the receiver.

Figure 11 Counting accuracy according to different pedestrians’ heights   
![](images/24dec0b513acf4488112f71bb877d4e82b405c3e631a5485d400377b05a866fa.jpg)



The experiments above have the assumption that all the moving objects pass right under the ultrasound sensor cluster. The third experiment studies the area covered by a three-node sensor cluster. As shown in Figure 12, a pedestrian might pass under the sensor cluster at a distance from the projective line of the sensor cluster. According to the results shown in Figure 13, the coverage of the three-node sensor cluster is rather small, no more than 40 cm wide. In practice, it can adequately cover a common door or a narrow corridor with a width of around 1 m. That is because the target objects have their own width, typically more than a 60 cm width for a person. The mid-line of the moving object usually lies within the coverage of the three-node sensor cluster.

Figure 12 Coverage measurement of three-node sensor cluster. d denotes the distance between the sensor cluster and the midline of the moving object (b) is the projective figure of (a)   
![](images/49fa2e238b666901032ace17d6e1b02d0e748ce3547e6b80b80db36d5fdfbf13.jpg)



Figure 13 Counting accuracy according to different distance between moving path and sensor cluster

![](images/403a173c9a7546046c2e0c759216c435d6b17ab3fd03a8403068ae749e6e5844.jpg)



# 6.3 Ultrasound sensor network

An ultrasound sensor network is set up to verify the characteristics described in the previous section as depicted in Figure 14(a). The ultrasound sensor network is a prototype, which involves only three three-node sensor clusters and one gateway, 10 Mica2 nodes in total. However, we believe that the prototype of ultrasound sensor network would have the same features as large-scale ultrasound sensor networks in the application of counting moving objects, since the analysis algorithm has nothing to do with the scale of the network.

Figure 14 (a) MOCUS system in small scale and (b) seven regular moving paths in the ultrasound sensor network   
![](images/4434a332e91eb0635c89fd06ecce17c2f873bb1e12ae24f3bd80a4ef42c44dcc.jpg)



One basic assumption of our ultrasound sensor network targeted at moving object counting is that each object with a regularly moving path can only be caught by at the most two adjacent clusters. This assumption is the precondition of our counting analysis algorithm. Therefore, we check first whether this assumption holds true in real systems. We can adjust the sensitivity of ultrasound receivers and the interval between three-node sensor clusters L to satisfy our requirements. Another objective in adjusting these parameters is that we must eliminate the noise caused by multiple ultrasound transmitters. In other words, ultrasound receivers should detect nothing if there is no moving object passing through. By setting the value of L to be 30 cm while adjusting the sensitivity of each ultrasound receiver, we found the basic assumption can be satisfied. In this experiment, pedestrians move along the seven regular paths depicted in Figure 14(b), and the average number of reflected waves detected by each ultrasound receiver node is recorded. Shown in Figure 15, in most cases, only one or two clusters will detect the moving person when a pedestrian passes through the sensing field of the ultrasound sensor network. Very few cases violate our basic assumption.

Figure 15 Number of reflected waves on each node under different regular moving paths   
![](images/f1ae3e354221a7ff9095c170660680c46d4a503d76002409d2e9b1f7ac04a437.jpg)



We further check the counting accuracy and the direction analysis of objects moving along these regular paths. According to Figure 16, the average accuracy of counting moving people in a period along the regular paths reaches 94.5%, although the accuracy of each motion determination stays around 87.9%. When the moving person passes the sensor field through the interval of the two adjacent sensor clusters, the accuracy is less than 80% because two clusters have detected the same object. The probabilistic algorithm determines the accuracy of counting results.

We deploy the system for several hours at a wide door to count the pedestrians while determining the direction. We classify the moving events roughly into S.P., S.B.S. and H.O. which refer to single pedestrian case, two side-by-side pedestrians case and two head-on pedestrians case, respectively. In H.O., two pedestrians are passing through the sensor field at the same time in opposite directions. The moving paths are arbitrary, even including the path which crosses the detection range of all the ultrasound receiver nodes. Although the accuracy for each detection is not high, around 50–70%, the total accuracy during the deployment period reaches 90%, shown in Figure 17 Most of the replicates occur when the moving person moves slowly, or the path crosses several clusters, not on a regular path parallel with each cluster. Miss detection is often caused by fast moving or short persons. In the case of side-by-side persons and head-on persons, solving the replication problem highly relies on the inter-cluster cooperation algorithm.

Figure 16 Counting and direction analysis results for regular moving pedestrians   
![](images/aa29ad36b3f282ecd0010883949d59e7fe1dcf7628b766ff0637e924712330ec.jpg)



Figure 17 Counting and direction analysis results for real deployment   
![](images/431b06e411c145cd1da840ce96abe1e3ba902265c82c1f4da4009f870bd2c130.jpg)



From the results, we found that the algorithm is inclined to count more on some three-node sensor clusters, while some other three-node sensor clusters tend to miss counting. That is because the ultrasound receivers have different sensitivities. However, the inter-cluster cooperation algorithm assumes that the ultrasound receivers have uniform sensitivity. Optimisation of receiver sensitivity is carried out by applying linear calibration algorithm on the sensitivities of ultrasound receivers according to feasibility tests shown in Figure 15, the optimised results are shown in Figure 18. The replicate and miss counts have been reduced compared with the analysis algorithm without calibration of ultrasound receiver sensitivities.

Figure 18 Counting and direction analysis results for real deployment with calibration of receivers’ sensitivity   
![](images/835af71b7728dac9d206fa66fd085426e3c7ee8a6a9d2123856e27b7ed0e53a2.jpg)



# 7 Conclusions and future work

We presented a moving object counting system, targeted to count moving objects, especially pedestrians in restricted area while determining their direction. After analysing the current technologies, such as video and infrared, we adopted ultrasound sensing and we made use of wireless sensor networks as our data collection and analysis platform. The three-node sensor cluster is the basic functional unit we developed for counting pedestrians. We extended the three-node sensor cluster to an ultrasound sensor network. Using intra-cluster analysis and inter-cluster cooperation, our experiments showed that the counting and motion direction analysis can reach 90% accuracy.

In future work, we will concentrate on the following aspects. As this is our prototype work, we focus on counting the pedestrians in some restricted area. Counting moving objects in an open area is extremely hard, because the direction of motion may be more arbitrary as well as the moving velocity especially in a crowded space. Intra-cluster analysis and inter-cluster cooperation algorithm should be improved to solve the replicate, miss and wrong direction problems in these complicated scenarios. Since always-on ultrasound sensor boards are power consuming, we should schedule the sensing term. Both network aggregation (Madden et al., 2002) and sleep algorithms (Ramanathan et al., 2005) need to be introduced to further reduce the power consumption. Targeting at mitigating the noise, properly adjusting the sensitivity of ultrasound receivers and sensing more useful data, we are designing new ultrasound boards. Finally, restricted by hardware at hand, we are only able to deploy a small-scale prototype of ultrasound sensor network. Large-scale deployments are needed to further exploit our ideas.

# Acknowledgement

This work was supported in part by the Hong Kong RGC Grant HKUST6183/05E, CAG Grant HKBU 1/05C, the Key Project of China NSFC Grant 60533110 and the National Basic Research Programme of China (973 Programme) under Grant No. 2006CB303000. We also wish to thank the anonymous reviewers for their valuable comments on our work.

# References

Cai, Q. and Aggarwal, J. (1998) ‘Automatic tracking of human motion in indoor scenes across multiple synchronized video streams’, Procedings of the 6th International Conference on Computer Vision, Bombay, India, January.   
Dutta, P., Grimmer, M., Arora, A., Bibyk, S. and Culler, D. (2005) ‘Design of a wireless sensor network platform for detecting rare, random, and ephemeral events’, Proceedings of the Fourth International Symposium on Information Processing in Sensor Networks, UCLA, Los Angeles, California, USA, April.   
Elson, J., Girod, L. and Estrin, D. (2002) ‘Fine-grained network time synchronization using reference broadcasts’, Proceedings of the 5th Symposium on Operating System Design and Implementation, Boston, USA, December.   
Ganeriwal, S., Kumar, R. and Srivastava, M. (2003) ‘Timing-sync protocol for sensor networks’, Proceedings of the 1st International Conference on Embedded Networked Sensor Systems, Los Angeles, California, USA, November.   
Gay, D., Levis, P., Behren, R., Welsh, M., Brewer, E. and Culler, D. (2003) ‘The NesC language: a holistic approach to networked embedded systems’, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation, San Diego, USA, June.   
Hill, J., Szewczyk, R., Woo, A., Hollar, S., Culler, D. and Pister, K. (2000) ‘System architecture directions for network sensors’, Proceedings of the 9th International Conference on Architectural Support for Programming Languages and Operating Systems, MA, USA: Cambridge, November.   
Madden, S., Franklin, M., Hellerstein, J. and Hong, W. (2002) ‘TAG: a tiny aggregation service for Ad-Hoc sensor networks’, Proceedings of the 5th Symposium on Operating System Design and Implementation, Boston, Massachusetts, USA, December.   
Mainwaring, A., Polastre, J., Szewczyk, R. and Culler, D. (2002) ‘Wireless sensor networks for habitat monitoring’, Proceedings of the First ACM International Workshop on Wireless Sensor Networks and Applications, Atlanta, Georgia, USA, September.   
Maroti, M., Kusy, B., Simon, G. and Ledeczi, A. (2004) ‘The flooding time synchronization protocol’, Proceedings of the 2nd International Conference on Embedded Networked Sensor Systems, Baltimore, MD, USA, November.   
Ni, L., Cui, L., Luo, Q., Ngan, H. and Zhao, Z. (2005) ‘Status of the CAS/HKUST joint project BLOSSOMS’, Proceedings of the 11th IEEE International Conference on Embedded and Real-Time Computing Systems and Applications, Hong Kong, China, August.

Ni, L., Liu, Y., Lau, Y. and Patil A. (2003) ‘LANDMARC: indoorlocation sensing using active RFID’, Proceedings of the first IEEE International Conference on Pervasive Computing and Communications, Dallas, USA, March.   
Ramanathan, N., Yarvis, M., Chhabra, J., Kushalnagar, N., Krishnamurthy, L. and Estrin, D. (2005) ‘A stream-oriented power management protocol for low duty cycle sensor network applications’, Proceedings of 2nd IEEE Workshop on Embedded Networked Sensors, Sydney, Australia, May.   
Singhvi, V., Krause, A., Guestrin, C., Garrett, J. and Matthews, S. (2005) ‘Intelligent light control using sensor networks’, Proceedings of the 3rd International Conference on Embedded Networked Sensor Systems, San Diego, USA, November.

Xu, N., Rangwala, S., Chintalapudi, K., Ganesan, D., Broad, A., Govindan, R. and Estrin, D. (2004) ‘A wireless sensor network for structural monitoring’, Proceedings of the 2nd International Conference on Embedded Networked Sensor Systems, Baltimore, MD, USA, November.   
Yang, D., Gonzalez-Banos, H. and Guibas, L. (2003) ‘Counting people in crowds with a real-time network of simple image sensors’, Procedings of the 9th IEEE International Conference on Computer Vision, Nice, France, October.   
Zhang, X. and Wicker, S. (2005) ‘Robustness VS. efficiency in sensor networks’, Proceedings of the Fourth International Symposium on Information Processing in Sensor Networks, UCLA, Los Angeles, California, USA, April.