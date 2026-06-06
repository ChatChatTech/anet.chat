# Perpendicular Intersection: Locating Wireless Sensors with Mobile Beacon

Zhongwen Guo∗, Ying Guo∗, Feng Hong∗, Xiaohui Yang∗, Yuan He† , Yuan Feng∗ and Yunhao Liu† ∗Ocean University of China, † Hong Kong University of Science and Technology {guozhw, guoying, hongfeng, yangxh, fengyuan}@ouc.edu.cn, {heyuan, liu}@cse.ust.hk

# Abstract

Existing localization approaches are divided into two groups: range-based and range-free. The range-free schemes often suffer from poor accuracy and low scalability, while the range-based localization approaches heavily depend on extra hardware capabilities or rely on the absolute RSSI (received signal strength indicator) values, far from practical. In this work, we propose a mobile-assisted localization scheme called Perpendicular Intersection (PI), setting a dedicate tradeoff between range-free and rangebased approaches. Instead of directly mapping RSSI values into physical distances, by contrasting RSSI values from the mobile beacon to a sensor node, PI utilizes the geometric relationship of perpendicular intersection to compute node positions. We have implemented the prototype of PI with 100 TelosB motes. Through comprehensive experiments, we show that PI achieves high accuracy and low overhead, significantly outperforming the existing range-based and the mobile-assisted localization schemes.

# 1. Introduction

Locating sensor nodes is a crucial issue and acts as a fundamental element in wireless sensor network (WSN) applications [2]. Localization can be classified as rangebased and range-free approaches. Range-free approaches do not assume the availability or validity of distance information, and only relies on the connectivity measurements (e.g. hop-count) from undetermined sensors to a number of seeds [4, 5, 12, 9]. Having lower requirements on hardware, the accuracy and precision of range-free approaches are easily affected by the node densities and network conditions, which are often unacceptable for many WSN applications that demand precise localizations. Range-based approaches calculate node distances based on some measured quantity, such as TOA, TODA and AOA [3, 11, 16], while they usually require extra hardware support, thus they are expensive in terms of manufacture cost and energy consumptions.

A popular and widely used ranging technique, sometimes being treated as a “free lunch”, is the received signal strength (RSS) [3, 7], or quantified as received signal strength indicator (RSSI). The fundamental stumbling block of existing RSSI-based approaches is that they rely on the absolute RSSI values to estimate physical distances [14]. Although being easy to implement, RSSI-based approaches face many challenges. First, RSS is sensitive to channel noise, interference, attenuation, and reflection, resulting in irregular propagation in different areas and directions [7]. Second, ratio attenuation greatly varies due to the environmental dynamics [23]. There is not a universal signal propagation model that applies for all cases. As a result, it is often difficult to map the absolute RSSI values to physical distances.

![](images/06973cdb6586531d2b221a0c263991f600d609b6d2dc85767d2d3e4556a90a0d.jpg)



Figure 1. OceanSense Project: The upper left photo shows a floating sensor. The upper right figure is the airscape of 20 floating sensors. The figure at the bottom is a field photo of 20 floating sensors, which are labeled from 1 to 20.

This work is motivated by one of our ongoing WSN projects, OceanSense [1], in which locating sensors is a critical task. As shown in Fig. 1, a number of restricted floating sensors [21] are deployed, usually tens of meters away from each other (sparsely deployed), and their wireless communications are often tampered by the environmental factors, including winds and tides. Due to the aforementioned reasons, the existing approaches cannot well support such a practically complex scenario.

As an early attempt in addressing the problem, we observe the RSSI behaviors of sensor nodes through preliminary experiments, as detailed in Subsection 3.1. We find that although RSSI values are irregular and highly dynamic, the difference in RSSI values consistently reflect the contrast of physical distances. In other words, for the same pair of sensors, a sender and a receiver, when one of them is moving closer to the other, in most cases, if not all, the measured RSSI keeps increasing, although not in a smooth manner. Based on this observation, we propose Perpendicular Intersection (PI), a RSSI-based localization scheme using mobile beacon.

Major contributions of this paper are as follows:

• In order to avoid errors from directly mapping absolute RSSI values to distances, we obtain the geometrical relationship of sensors by contrasting the measured RSSI values. We then design a novel localization scheme, PI, which has better accuracy and low overhead, especially under dynamic and complex environments.   
• We design the optimal trajectory of the mobile beacon in PI and theoretically prove its correctness. Only one mobile beacon is needed to broadcast beacon signals in PI, and other sensor nodes simply listen to the signals, store a few necessary packets, and compute their coordinates without interfering with each other.   
• We implement a prototype of PI with 100 sensors, and evaluate its performance in real environments, including indoor and outdoor spots. We show the advantages of this design through comprehensive experimental results.

The rest of the paper is organized as follows. Section 2 summarizes the related works in localization of WSNs. Section 3 presents our observations of RSSI and elaborates the design of PI. Section 4 theoretically analyzes the performance and the overhead of PI. Section 5 presents our implementation and the experimental results. We conclude the work in Section 6.

# 2. Related Work

Many approaches have been proposed to determine sensor node locations, falling into two categories: range-based approaches and range-free approaches.

# 2.1. Range-Based Approaches

Range-based approaches assume that sensor nodes are able to measure the distance and/or the relative directions of neighbor nodes. Various techniques are employed to measure the physical distance. For examples, Time of Arrival (TOA) obtains range information via signal propagation times [20], and Time Difference of Arrival (TDOA) estimates the node locations by utilizing the time differences among signals received from multiple senders [15, 17]. As an extension of TOA and TDOA, Angle of Arrival (AOA) allows nodes to estimate the relative directions between neighbors by setting an antenna array for each node [11]. All those approaches require expensive hardware.

RSSI is utilized to estimate the distance between two nodes with ordinary hardware [3, 7]. Various theoretical or empirical models of radio signal propagation have been constructed to map absolute RSSI values into estimated distances [14]. The accuracy and precision of such models, however, are far from perfect. Factors like multi-path fading and background interference often result in inaccurate range estimations [7, 23].

Recently, mobile-assisted localization approaches are proposed to improve the efficiency of range-based approaches [18, 13, 19, 10]. The location of a sensor node can be calculated with the range measurements from the mobile beacon to itself, so no interaction is required between nodes, avoiding cumulative errors of coordinate calculations and unnecessary communication overhead. The localization accuracy can also be improved via multiple measurements obtained when the mobile beacons are at different positions.

# 2.2. Range-Free Approaches

Knowing the hardware limitations and energy constraints required by range-based approaches, researchers propose range-free solutions as cost-effective alternatives.

Having no distances among nodes, range-free approaches depend on the connectivity measurements from sensor nodes to a number of reference nodes, called seeds. For example, in Centroid [4], seeds beacon their positions to their neighbor nodes that record all received beacons. Each node estimates its location by calculating the center of all seeds it hears. In APIT [5], each node estimates whether it resides inside or outside several triangular regions bounded by the seeds it hears, and refines the computed location by overlapping the regions the sensors likely reside in. SeR-Loc [8] employs a similar approach while emphasizes a secure mechanism against malicious attacks. As an alternate solution, DV-HOP only makes use of constant number of seeds [12]. Instead of single hop broadcasts, seeds flood their locations throughout the network, maintaining a running hop-count at each node along the path. Nodes calculate their positions based on the received seed locations, the hop-counts from the corresponding anchors, and the average-distance per hop through trilateration.

Instead of using the absolute RSSI values, by contrasting the measured RSSI values from the mobile beacon to a sensor node, our proposed PI utilizes the geometric relationship of perpendicular intersection to compute the position of the node. In this sense, PI is actually between range-based and range-free approaches.

![](images/6db65cc8f3fe4e0ea50c83e6d1492f3887b1fba764ab67fc1d7f1204c0d82a23.jpg)



![](images/1e0dad9c2228f1752c7258ddffd3cd39ecffb417058fc8227ba4f2ea8bd1a1e5.jpg)



Figure 2. Observations of RSSI: (a) deployment sketch (b) RSSI values of the received signals

# 3. Design of PI

In this section, we first describe the experimental observations on RSSI in Subsection 3.1, which motivated this design. Subsection 3.2 presents the overview of the PI design. Subsection 3.3 discusses the optimal trajectory of the mobile beacon for PI. Subsection 3.4 presents our localization scheme in detail. For convenience of expression, the terms “location”, “position” and “coordinates” are used interchangeably in the rest of this paper.

# 3.1. Observations on RSSI

RSSI is initially used for power control in wireless networks [10]. The existing signal propagation models of RSSI, however, are far from perfect, mainly because of the uncertain influences such as background interference, nonuniform spreading, signal fading and reflections. To better understand RSSI patterns, we conduct some initial experiments with 12 TelosB sensors on our campus, as illustrated in Fig. 2(a).

In this set of experiments, node A broadcasts signals, and the rest nodes receive RSSI values from their CC2420 transceivers. Node A moves from 10 meters away from O to 20, 30, 40, and 50 meters. All the measured RSSI values are shown in Fig. 2(b).

With the RSSI values from node A to a node, in ideal sense the distance between other nodes and node A should be calculated according to the log-normal shadowing model in Equation (1), which is widely used in range-based localization approaches [3, 14, 22].

$$
R S S I (d) = P _ {T} - P _ {L} (d _ {0}) - 1 0 \eta l o g _ {1 0} \frac {d}{d _ {0}} + X _ {\sigma} \tag {1}
$$

where $P _ { T }$ is the transmission power, $P _ { L } ( d _ { 0 } )$ is the path loss for a reference distance of $d _ { 0 } ,$ and η is the path loss exponent. The random variation in RSSI is expressed as a Gaussian random variable $X _ { \sigma } = N ( 0 , \sigma ^ { 2 } )$ ). All powers are in dBm and all distances are in meters. η is set between 2 and 5. σ is set between 4 and 10, depending on the specific environment [14].

The real and estimated distances between A and O are compared in Table 1. The average relative error is 9.06%, leading to unacceptable localization errors in WSNs.

Interestingly, we find that, the closer a node is to the signal sender, the larger RSSI value it perceives. This simple observation motivates our design of PI.

# 3.2. Perpendicular Intersection

In our experiment, when the mobile beacon moves along a straight line, the largest RSSI value received by a sensor node often, if not always, corresponds to the point on the line that is closest to the node. Theoretically, this point should be the projection of the node on the line. Given two different projections of the sensor node on the trajectory, this node can be located as the intersection point of two perpendiculars that cross the mobile beacon’s trajectory over the two projections, respectively.

Table 1. Observation results (m) 

<table><tr><td>|AO|</td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td></tr><tr><td>Estimated distance</td><td>9.62</td><td>19.19</td><td>30.41</td><td>34.12</td><td>60.68</td></tr></table>

![](images/fafb0b88a6e00a39c7a76b63ae279f6a2fd172701525c177cce2cdfd32cfd583.jpg)



Figure 3. An example of PI scheme

In order to illustrate how PI works, we show an example in Fig. 3, where a mobile beacon traverses the region while broadcasting beacon packets periodically. A beacon packet contains the coordinates of the position of the mobile beacon. The solid black lines in Fig. 3 form the trajectory of the mobile beacon, with the arrows denoting its moving directions. The mobile beacon (in red) starts at point $P _ { 1 }$ , turns its direction at point $P _ { 2 } { \mathrm { . } }$ , and stops at point $P _ { 3 }$ . By combining the trajectory with the virtual line $P _ { 1 } P _ { 3 }$ , we obtain a virtual triangle $\triangle P _ { 1 } P _ { 2 } P _ { 3 }$ (we call it VT from now on).

Let R be the transmission range of mobile beacon. To ensure that all the nodes in a VT can receive the signals from the beacon, the sides $P _ { 1 } P _ { 2 }$ and $P _ { 2 } P _ { 3 }$ should not be longer than R. Meanwhile, the angle θ between the two lines should satisfy $0 < \theta \leq \pi / 3$ .

Suppose the five nodes (in blue) in Fig. 3 are located using PI. We use node $N ( x , y )$ as an example. The mobile beacon starts at point $P _ { 1 }$ and broadcasts the start signal with its current location. Node N records the start position when it hears the start signal. Along its trajectory from $P _ { 1 } \tan P _ { 2 }$ , the mobile beacon broadcasts beacon packets periodically with its current location. Node N receives all the beacon packets, and records the one with the largest RSSI value. When the mobile beacon arrives at $P _ { 2 }$ , it broadcasts a stop signal with its current location. When node N receives the stop packet, it knows that the mobile beacon has just finished traversing the line from $P _ { 1 }$ to $P _ { 2 }$ . The recorded position is the position where the beacon packet with largest RSSI value is broadcast. We label the recorded position as $A ( x ^ { \prime } , y ^ { \prime } )$ .

According to the observations in SubSection 3.1, line segment N A is the shortest one among all the line segments connecting node N and any point on line $P _ { 1 } P _ { 2 }$ . In other words, Node A is the projection of node N on line $P _ { 1 } P _ { 2 }$ . Hence, line NA is perpendicular to line $P _ { 1 } P _ { 2 } .$ , and we have:

$$
\frac {y _ {2} - y _ {1}}{x _ {2} - x _ {1}} \times \frac {y - y ^ {\prime}}{x - x ^ {\prime}} = - 1 \tag {2}
$$

Similarly, when the mobile beacon moves from $P _ { 2 }$ to $P _ { 3 } ,$ , another position $B ( x ^ { \prime \prime } , y ^ { \prime \prime } )$ is recorded which is the projection of node N on line $P _ { 2 } P _ { 3 }$ . Thus we have:

$$
\frac {y _ {3} - y _ {2}}{x _ {3} - x _ {2}} \times \frac {y - y ^ {\prime \prime}}{x - x ^ {\prime \prime}} = - 1 \tag {3}
$$

By solving Formulas (2) and (3), we can compute the coordinates $( x , y )$ of node N :

$$
\binom {x} {y} = \left( \begin{array}{c c} x _ {2} - x _ {1} & y _ {2} - y _ {1} \\ x _ {3} - x _ {2} & y _ {3} - y _ {2} \end{array} \right) ^ {- 1} \times M \tag {4}
$$

where

$$
M = \left( \begin{array}{c c c c} x _ {2} - x _ {1} & y _ {2} - y _ {1} & 0 & 0 \\ 0 & 0 & x _ {3} - x _ {2} & y _ {3} - y _ {2} \end{array} \right) \left( \begin{array}{c} x ^ {\prime} \\ y ^ {\prime} \\ x ^ {\prime \prime} \\ y ^ {\prime \prime} \end{array} \right)
$$

In the above process, we do not use any absolute RSSI values, so as to avoid the errors brought by the translations from RSSI values to physical distances.

# 3.3. Optimal Trajectory

Clearly, a sensor node can be easily located when it is in the scope of a VT. When the entire deployment area of a sensor network cannot be covered by one VT, however, the trajectory of the mobile beacon to locate all the sensor nodes needs further considerations. We require an optimal trajectory with the following characteristics:

1) The localization latency, defined as the elapsed time from a node receiving the first beacon packet to determining its location, is minimized. Therefore, if a VT covers a node, the node should be located as soon as the beacon traverses along the two sides of the VT.   
2) It is able to locate all the sensor nodes. The optimal trajectory thus consists of multiple joint VTs, which cover the entire deployment area.   
3) It is the shortest trajectory so that the mobile beacon traverses the entire area in the shortest time and consumes the minimum energy cost. Consequently, every VT in the optimal trajectory covers the largest acreage, given its perimeter. We define such a VT as the optimal VT.

Theorem 1: The optimal VT in PI is an equilateral triangle with the lengths of its sides all equal to R, where R is the transmission radius of the mobile beacon.

Proof. A VT of $\Delta A B C$ with its inscribed circle O is shown in Fig.4. The radius of circle O is r. Let S be the acreage of $\triangle A B C$ and L be the perimeter of $\triangle A B C$ .

We define the parameter of $\lambda = S / L$ , which represents the ratio of the acreage to the perimeter of the triangle. Consequently, the optimal VT has the largest value of λ.

$$
\lambda = \frac {S}{L} = \frac {\frac {1}{2} \times L \times r}{L} = \frac {r}{2} \tag {5}
$$

![](images/9f414fa9b4b21b0baa45e1abfddc50616d52aa6e3be14fed72443ca67335aebc.jpg)



Figure 4. A VT with its inscribed circle

Obviously, λ reaches its maximum when the radius r reaches its maximum. Note that $A F = A D , B D = B E$ , $C E = C F$ , because $F , D$ , and E are the intersection points of inscribed circle O with the sides of $\triangle A B C$ . We have:

$$
L = r \times (c t g \frac {A}{2} + c t g \frac {B}{2} + c t g \frac {C}{2})
$$

$$
r = \frac {L}{2 \times (c t g \frac {A}{2} + c t g \frac {B}{2} + c t g \frac {C}{2})}
$$

$$
\leq \frac {L}{2 \times (3 \times \sqrt [ 3 ]{c t g \frac {A}{2} c t g \frac {B}{2} c t g \frac {C}{2}})}
$$

The equality in the above formula is valid iff. $c t g { \frac { A } { 2 } } =$ $\begin{array} { r } { c t g \frac { B } { 2 } = c t g \frac { C } { 2 } } \end{array}$ , which means angles A, B, and $C$ equal to each other. Thus $\triangle A B C$ is an equilateral triangle.

Let a be the side length of equilateral triangle $\triangle A B C$ , we have:

$$
\lambda = \frac {r}{2} = \frac {\sqrt {3} a}{1 2} \tag {6}
$$

That is, λ is proportional to a. From the previous subsection, we know $a { \leq } R ,$ , which ensures all nodes in the VT can be located. Hence, λ of the virtual triangle in PI reaches its maximum, when $a = R$ . □

According to Theorem 1, we can conclude that the trajectory of mobile beacon is optimal, when it consists of multiple joint optimal VTs, as depicted in Fig. 5.

# 3.4. PI Scheme

If a node only receives two pairs of start and stop signals broadcast by the mobile beacon, it knows the three vertices of the VT and then locates itself. Nodes at special positions, however, might receive more than two pairs of start and stop signals and PI needs to deal with this situation.

As illustrated in Fig. 5, nodes $N _ { 1 } , N _ { 2 } , N _ { 3 } , N _ { 4 }$ represent four special cases, where $N _ { 1 }$ can receive three pairs of start and stop signals when the mobile beacon traverses sides $P _ { 1 } P _ { 2 } , \ P _ { 2 } P _ { 3 }$ and $P _ { 3 } P _ { 4 } , \ N _ { 2 }$ receives four pairs of signals when beacon traverses $P _ { 5 } P _ { 6 } , P _ { 6 } P _ { 7 }$ of one VT and $P _ { 8 } P _ { 9 } , P _ { 9 } P _ { 1 0 }$ of another VT. $N _ { 3 }$ receives three pairs of signals when the mobile beacon traverses sides $P _ { 8 } P _ { 9 } , P _ { 9 } P _ { 1 0 }$ and $P _ { 1 0 } P _ { 1 1 } . \ N _ { 4 }$ receives six pairs of signals when the mobile beacon traverses the six sides of four VTs $\triangle P _ { 5 } P _ { 6 } P _ { 7 }$ , $\triangle P _ { 8 } P _ { 9 } P _ { 1 0 } , \triangle P _ { 9 } P _ { 1 0 } P _ { 1 1 }$ and $\triangle P _ { 1 0 } P _ { 1 1 } P _ { 1 2 }$ .

Lemma 1: A node can receive at most 6 pairs of start and stop signals, during the whole localization process of $P I .$ .

It is straightforward to prove Lemma 1 by enumerating all the possible locations of a sensor node. Due to the page limit, we skip the proof. If a node receives start and stop signals from all the three vertices of a VT, we call this VT a locating VT for the node. PI let each node compute the sum of RSSI values from the three vertices of a locating VT, and the locating VT whose vertices have the largest sum of RSSI values is used to calculate the node location.

The pseudo code of the main function on message processing in PI is shown in Fig. 6. We define side(i) (1≤i≤6) as the side from which the node receives the ith pair of start and stop signals. Let cp(i) denote the point on side(i) that is closest to the node. Variable side denotes the current side traversed by the mobile beacon. Variable $r s s i _ { m a x }$ and $p o s i t i o n _ { m a x }$ respectively denote the current largest RSSI value and its corresponding beacon position. Variable loc denotes the location calculated from the current locating VT. The final result of the node coordinates is stored in the variable location. SumRSSI(l) calculates the sum of RSSI values from the three vertices of node l’s locating VT.

PI can address all the special cases. For example, $N _ { 1 }$ receives three pairs of start and stop signals, respectively from the locating $\mathrm { V T s } \triangle P _ { 1 } P _ { 2 } P _ { 3 }$ and $\triangle P _ { 2 } P _ { 3 } P _ { 4 }$ , so the corresponding calculated results by using these two locating VTs are the coordinates of points $N _ { 1 } ^ { \prime }$ and $N _ { 1 }$ . For a node

![](images/de1bc417a42d23f8d48b409efae7e3acfee4f618f4392f4995f54c721a505936.jpg)



Figure 5. A sensor network and its optimal trajectory of the mobile beacon

```lisp
OnMessageReceived(Message m)
{
    if (m.flag=start)
    {
    //start of side(i)
    side.clear(); //clear the variable side(i-1)
    Record(side.start,m);
    //save RSSI and position of the
    //first beacon signal on side(i)
    rssi_max=m.RSSI; position_max=m.position;
    }
    else if ((m.flag=beacon)and(m.RSSI≥rssi))
    {
    //larger RSSI, update current
    //rssi_max and position_max
    rssi_max=m.RSSI; position_max=m.position;
    }
    else if (m.flag=stop)
    {
    //end of side(i)
    Record(side.stop,m);
    side(i)=side; cp(i)=position;
    if (side(i-1).stop=side(i).start)
    {
    loc=calculate(side(i-1),side(i));
    //keep the one with the largest SumRSSI(),
    //if multiple location results exist
    if((loc!=location)and(SumRSSI(loc)
    >SumRSSI(location)))
    location=loc;
    }
    }
} 
```  
Figure 6. PI Algorithm

at point $N _ { 1 } , \triangle P _ { 2 } P _ { 3 } P _ { 4 }$ has larger sum of RSSI values than $\triangle P _ { 1 } P _ { 2 } P _ { 3 }$ . Thus, the coordinates of point $N _ { 1 }$ can be correctly selected in place of the coordinates of $N _ { 1 } ^ { \prime } .$ . Similarly, nodes $N _ { 2 } , N _ { 3 }$ and $N _ { 4 }$ can determine their coordinates from multiple calculated results.

# 4. Discussions

# 4.1. Theoretical Estimation Error

Although the mobile beacon can keep moving in a continuous manner, the beacon packets have to be broadcast periodically, with a specified interval between every two consecutive packets. As a result, the beacon trace is chopped into a series of discrete beacon points. Hence there exists an error between the estimated location by PI and the real location.

![](images/0e67239345f1db66a01355d85760724a74b40af7812b2e97c80479c3124ed251.jpg)



Figure 7. A VT with all beacon positions

Figure 7 shows an example in which $P _ { 1 } , C _ { 1 } , C _ { 2 } , P _ { 2 } , C _ { 3 }$ , $C _ { 4 } .$ , and $P _ { 3 }$ are beacon points. Given the velocity of the mobile beacon as V and the broadcast frequency as $F _ { \ast }$ , the distance between two beacon points is $V / F _ { \ast }$ . With high probability, the closest points to node N on sides $P _ { 1 } P _ { 2 }$ and $P _ { 2 } P _ { 3 }$ (i.e. the theoretical projections of node N on the sides) lie between two beacon points. Accordingly, node N stores the coordinates of $C _ { 2 }$ instead of A in its location computation, as the beacon packet broadcast at $C _ { 2 }$ has the largest RSSI value. Similarly, $C _ { 4 }$ is stored instead of B.

Suppose $| A C _ { 2 } | = d _ { 1 }$ and $| B C _ { 4 } | = d _ { 2 }$ , the distance between the real location of node N and the estimated location

$$
N ^ {\prime} \text {   is:   } | N N ^ {\prime} | = \sqrt {\frac {4}{3} (d _ {1} ^ {2} + d _ {2} ^ {2} + d _ {1} d _ {2})}
$$

If $C _ { 3 }$ is closer to position B than $C _ { 4 }$ ,

$$
| N N ^ {\prime} | = \sqrt {\frac {4}{3} (d _ {1} ^ {2} + d _ {2} ^ {2} - d _ {1} d _ {2})}
$$

Thus the upper bound of theoretical estimation error (T ERR) is given by:

$$
T E R R _ {m a x} = \frac {V}{F} \quad w h e n d _ {1} = d _ {2} = \frac {V}{2 F}
$$

Meanwhile, the theoretical mean estimation error is:

$$
\begin{array}{l} \overline {{T E R R}} = \frac {4 V}{\sqrt {3} F} (\int_ {- \frac {\sqrt {3}}{4}} ^ {\frac {\sqrt {3}}{4}} \int_ {0} ^ {\frac {1}{2}} \sqrt {x ^ {2} + y ^ {2} + x y} d x d y \\ + \int_ {- \frac {\sqrt {3}}{2}} ^ {0} \int_ {- \frac {1}{4}} ^ {\frac {1}{4}} \sqrt {x ^ {2} + y ^ {2} - x y} d x d y) = 0. 8 2 1 8 \frac {V}{F} \\ \end{array}
$$

# 4.2. Trajectory Length and Localization Latency

A rectangle deployment area with length L and width H is shown in Fig. 5. The length of the optimal trajectory labeled as $L _ { M }$ is:

$$
L _ {M} = (\lceil \frac {L}{R} \rceil \times 2 R + R) \times \lceil \frac {H}{\frac {\sqrt {3}}{2} R} \rceil + \lfloor \frac {H}{\frac {\sqrt {3}}{2} R} \rfloor \times \frac {\sqrt {3}}{2} R
$$

Furthermore, sensor locations are calculated when the mobile beacon moves. This process ends when the mobile beacon arrives at the terminal of the trajectory. The latency for locating all the sensors can be calculated by:

$$
T = \frac {L _ {M}}{V}
$$

# 4.3. Overhead

Communication Cost. The communication cost of a sensor node depends on the total number of beacon packets it receives. The number of beacon packets (NBP ) received by a sensor node when the mobile beacon traverses one VT side is:

$$
N B P = \frac {F R}{V}
$$

Meanwhile, a sensor node receives the beacon packets from at most 6 sides according to Lemma 1. Therefore the upper bound of communication cost of a sensor node is 6F $R / V$ .

Computation overhead. From Fig. 6 we can see that the most frequent operation in PI is to compare the recorded RSSI value with the latest RSSI value on one side of VT. The number of beacon packets received by a sensor node on one VT side is $F R / V _ { \mathrm { ~ \normalfont ~ \cdot ~ } }$ , and the sensor node can receive the beacon packets from 6 sides at most. Thus the computation overhead on a sensor node is $O ( F R / V )$ .

Storage overhead. PI only stores two vertices and one point of maximum RSSI value for each VT side. The localization result is achieved based on the information from two joint sides. When a node has two possible location results, it compares the aggregate RSSI values of both locating VTs and only saves one after comparison, as illustrated in Fig. 6. Therefore PI only needs to store at most 14 vertices with their corresponding RSSI values, which costs 70 bytes. In short, both the computation and storage overhead are applicable for the ordinary sensor nodes.

# 5. Performance Evaluation

To better evaluate the PI design, we implement a prototype system of PI with 100 TelosB sensors in various environments, including library hall, laboratory, racket court and parking lots. The mobile beacon is also a TelosB mote which moves manually. A sink is deployed to collect the localization results of all the sensor nodes.

We evaluate the performance of PI in all the four environments, and compare it with other two RSSI-based localization approaches: a range-based approach of trilateration and a mobile-assisted localization approach, which are briefly introduced as follows.

In the range-based approach of trilateration (called TRL in short) [6], beacon packets from the three vertices of the VT where the node resides, are used to calculate its location. As for the mobile-assisted localization approach, it exploits Bayesian inference to improve the estimation accuracy [18]. We call that approach BI. Six beacon packets are used in the computation process of BI. Three of them are sent from the three vertices of the VT where the node resides, while the other three are chosen randomly from the positions on the two sides of the VT. Both approaches rely on the signal propagation model of Equation (1) to transform absolute RSSI values to physical distances.

![](images/e0cf7c7fd474b06defa97605591b97e95feae862b55a42372e9508961c9887af.jpg)



Figure 8. Deployment of hall experiment

# 5.1. Hall Experiment

The first experiment is conducted in a hall of our library, which is about 450m2. 14 sensor nodes are deployed randomly and the side length of a VT is 15m. The moving velocity is 0.1m/s and the broadcast frequency is 1 time per second. The sketch of this deployment is shown in Fig. 8.

Figure 9(a) plots the RSSI values of the beacon packets received by node $N _ { 6 }$ . It is clear that two extrema of the RSSI values exist. Through measurements beforehand, we obtain precise values of the parameters in Equation (1). $\eta =$ 3.4, $P _ { L } ( d _ { 0 } ) = 1 4 5$ . The value of σ is chosen as 4 according to [14].

Figure 9(b) compares the estimation errors of PI, BI, and TRL approaches. The average estimation error of PI is 1.22m and the standard deviation of estimation error is 0.38m. The averages and standard deviations of estimation error of BI and TRL are shown in Table 2.

We repeat the experiments for multiple times and Fig. 9(c) compares the three approaches with the curves of cumulative distribution function (CDF). The results demonstrate that PI outperforms BI and TRL with lower estimation errors and more stable precision.

# 5.2. Laboratory Experiment

In order to examine PI’s performance in a more dynamic complex environment, we perform another experiment in the laboratory of computer software center, which is a room of 324m2 with 120 computers and desks inside. Some people are sitting, standing, or moving in the room. We use 100 sensor nodes. The moving velocity of the mobile beacon is set at 0.1m/s and the broadcast frequency is set at 1 time per second. The side length of a VT is 9m. The sketch of this deployment is plotted in Fig. 10(a). The trajectory length of the mobile beacon is 79.79m and the localization latency of the entire sensor network is $1 3 ^ { \prime } 2 7 ^ { \prime \prime }$ .

![](images/4cd7f25921744b09296a2b9f3849d2759f1d1bd969d950ccd10508188f2498ec.jpg)



(a)

![](images/4a1dbcd1a03a7551393a2192c295a89fcbf5f6f2621aa15adf22992f10ccf490.jpg)



(b)

![](images/0879f80fe3cb46525858b01c9aafe81d61dfcbeea669dbf76aef3eb2b2fb01c9.jpg)



(c)

Figure 9. Results of hall experiment: (a) RSSI values of beacon packets received by node $N _ { 6 }$ (b) estimation errors of 14 nodes (c) CDF of estimation errors of 50 nodes   
![](images/2db8d272696134b74b32d3ab4170839c7d2049b5d71330eedf3feb5c4914b175.jpg)



(a)

![](images/c31966efc8669698fb13d144092c2487f6ba75dc18311fa4f31c4a087ea7d12b.jpg)



(b)

![](images/6cfd5ebbad9a0cbdbf69886381e9cd44f9950bdf17c5cc32c59fa8a3a24602a1.jpg)



(c)   
Figure 10. Results of laboratory experiment: (a) deployment (b) estimation errors of 12 typical nodes (c) CDF of estimation errors of PI compared with BI and TRL

Figure 10(b) plots the estimation errors of 12 nodes using the three approaches. Fig. 10(c) shows the cumulative distribution of estimation errors of all the 100 nodes. The averages and standard deviations of the estimation errors of the three approaches are compared in Table 2. The results demonstrate that PI outperforms BI and TRL with lower estimation errors and more stable precisions, even in a complex environment.

# 5.3. Outdoor Experiments

Now we move the experiments to the outdoor environments: racket court and parking lots. The moving velocity of the mobile beacon is set at 0.1m/s and the broadcast frequency is set at 1 time per second. The localization errors of 4 typical sensor nodes in the two environments are shown in Fig. 11(a) and 11(b) respectively.

The averages and standard deviations of the estimation errors of these three approaches are listed in Table 2. We can see that the three approaches achieve the smallest estimation errors in the hall experiments, similar estimation errors in two outdoor experiments, and the largest estimation errors in the laboratory experiments. This is consistent with the fact that all RSSI-based localization approaches are more or less affected by the interference in wireless signal propagation, and the dynamic of the environments.

We can also see even the worst result of PI (in the laboratory) is better than the best results of BI and TRL. This result again confirms the advantage of PI, which compares the measured RSSI values of beacon packets to calculate the coordinates of the nodes, effectively eliminating the sideeffect of the irregularity of measured RSSI values.

![](images/e322118ea17c3872ac3b6ede1793f28657f023a9642b18f6ae69db75f5829e87.jpg)



![](images/a70929df99f53d7ddd1de3b829fd173f025a3935fa6755135d66746b76bc692f.jpg)



Figure 11. Results of outdoor experiments: (a)racket court (b)parking lots   
![](images/f89b7bee529f1612bbbe0878d49ae19ebc2fd568dc83c41159f46ad9a402f7b5.jpg)



![](images/5685e0c69ac942740841899d1d306292a0d3b3c5f3d5c7a0325f95009ca696d2.jpg)



(b)   
Figure 12. Impact of the velocity and the broadcast frequency: (a) average estimation error (b) average estimation error and communication cost

Table 2. Errors of overland experiments (m) 

<table><tr><td rowspan="2">Results</td><td colspan="2">PI</td><td colspan="2">BI</td><td colspan="2">TRL</td></tr><tr><td>Ave.</td><td>S.D.</td><td>Ave.</td><td>S.D.</td><td>Ave.</td><td>S.D.</td></tr><tr><td>Hall</td><td>1.22</td><td>0.38</td><td>2.49</td><td>0.77</td><td>3.36</td><td>0.95</td></tr><tr><td>Lab</td><td>2.04</td><td>1.05</td><td>2.75</td><td>1.15</td><td>3.97</td><td>1.50</td></tr><tr><td>Racket Court</td><td>1.22</td><td>0.45</td><td>2.23</td><td>0.87</td><td>3.69</td><td>1.45</td></tr><tr><td>Parking Lots</td><td>1.27</td><td>0.52</td><td>2.21</td><td>0.34</td><td>3.73</td><td>0.88</td></tr></table>

# 5.4. Impact of Different Factors

According to the analysis in Section 4, the estimation error and communication cost are affected by the velocity and the broadcast frequency of the mobile beacon. In order to gain insight of their relationship, we conduct several experiments using different settings of the moving velocity and the broadcast frequency. The experiments are similarly deployed as those in Subsection 5.1. The moving velocity is set at 0.05m/s, 0.1m/s, 0.2m/s and 0.4m/s, while the broadcast frequency is set at 0.5, 1, 2, and 4 times per second respectively. Thus we have 16 different combinatorial settings.

Figure 12(a) shows the average estimation error of all the 14 nodes. Due to the irregularity of RSSI values, the experimental average estimation error is slightly larger than the theoretical one. The result indicates that ERR is proportional to both V and $1 / F$ , as is in accordance with the analytical result in Subsection 4.1. Further, Fig. 12(b) shows the curves of the average estimation error (ERR) and the communication cost $( N B P )$ as functions of the ratio of the velocity to the broadcast frequency $( V / F )$ . Clearly ERR is proportional to $V / F$ while N BP is inverse proportional to $V / F$ .

It is also worth noticing that there is an intersection point of the two curves, where V /F =0.1, ERR=1.28, and NBP =300. It represents a good setting in practice, which sets appropriate trade-off between the average estimation error and the communication cost. Specifically, if we deviate V /F away from the point 0.1, e.g. to the left (right), the communication cost (the average estimation error) will remarkably increase, without much benefit in the average estimation error (the communication cost).

# 6. Conclusion

Localization is a crucial issue in wireless sensor network applications. The range-free schemes often suffer from poor accuracy and low scalability, while the range-based localization approaches heavily depend on extra hardware capabilities or rely on the absolute RSSI values, far from practical. In this work, we propose a mobile-assisted localization algorithm called Perpendicular Intersection (PI).

By comparing the received RSSI values on a sensor node, PI exploits the geometric relationship between the node and the trajectory of the mobile beacon, eliminating the side-effect of the irregularity of the RSSI signals. We examine the performance of PI by implementing a prototype system with 100 TelosB motes. Both the analytical and experimental results demonstrate that PI is superior to all the existing approaches with high precision.

We plan to further improve our prototype of PI in all aspects, for example, introducing an automatic mobile beacon. Large-scale field tests of the improved prototype of PI on the OceanSense platform are also in our plan. We will also extend PI in the underwater acoustic sensor networks.

# Acknowledgement

We thank our colleagues Song Xie, Hanjiang Luo, Hao Wu, and Ke Liu who have participated in all the experiments of PI. This work is supported in part by the National High Technology Research and Development Program of China (863 Program) under grant No.2006AA09Z113, the National Basic Research Program of China (973 Program) under grant No. 2006CB303000, NSF China grant No. 60703082, and Hong Kong RGC grant HKUST6169/07E.

# References

[1] Oceansense. https://www.cse.ust.hk/˜liu/Ocean/index.html.   
[2] I. F. Akyildiz, W. Su, Y. Sankarasubramaniam, and E. Cayirci. A survey on sensor networks. IEEE Communications Magazine, 40(8):102–114, August 2002.   
[3] P. Bahl and V. N. Padmanabhan. Radar: An in-building rf-based user location and tracking system. Proceedings of IEEE INFOCOM, 2000.

[4] N. Bulusu, J. Heidemann, and D. Estrin. GPS-less low cost outdoor localization for very small devices. IEEE Personal Communications Magazine, 7(5):28–34, October 2000.   
[5] T. He, C. Huang, B. Blum, J. Stankovic, and T. Abdelzaher. Range free localization schemes in large scale sensor networks. Proceedings of ACM MobiCom, 2003.   
[6] J. Hightower and G. Borriello. Location systems for ubiquitous computing. IEEE Computer, 34(8):57 – 66, August 2001.   
[7] J. Hightower, R. Want, and G. Borriello. Spoton: An indoor 3d location sensing technology based on rf signal strength. UW CSE 00-02-02, 2000.   
[8] L. Lazos and R. Poovendran. Serloc: Secure rangeindependent localization for wireless sensor networks. ACM Transactions on Sensor Networks, 1(1):73–100, August 2005.   
[9] M. Li and Y. Liu. Rendered path: Range-free localization in anisotropic sensor networks with holes. Proceedings of ACM MobiCom, 2007.   
[10] J. Luo, H. V. Shukla, and J. P. Hubaux. Non-interactive location surveying for sensor networks with mobilitydifferentiated toa. Proceedings of IEEE INFOCOM, 2006.   
[11] D. Niculescu and B. Nath. Ad hoc positioning system (aps) using aoa. Proceedings of IEEE INFOCOM, 2003.   
[12] D. Niculescu and B. Nath. Dv based positioning in ad hoc networks. Journal of Telecommunication Systems, 22(1):267–280, January 2003.   
[13] N. B. Priyantha, H. Balakrishnan, E. D. Demaine, and S. Teller. Mobile-assisted localization in wireless sensor networks. Proceedings of IEEE INFOCOM, 2005.   
[14] T. S. Rappaport. Wireless Communications, Principles & Practice. Prentice Hall, 1999.   
[15] A. Savvides, C. Han, and M. B. Srivastava. Dynamic finegrained localization in ad-hoc networks of sensors. Proceedings of ACM MobiCom, 2001.   
[16] A. Savvides, C. Han, and M. B. Strivastava. Dynamic finegrained localization in a ad-hoc networks of sensors. Proceedings of ACM MobiCom, 2001.   
[17] A. Savvides, H. Park, and M. Srivastava. The bits and flops of the n-hop multilateration primitive for node localization problems. Proceedings of ACM WSNA, 2002.   
[18] M. Sichitiu and V. Ramadurai. Localization of wireless sensor networks with a mobile beacon. Proceedings of IEEE MASS, 2004.   
[19] R. Stoleru, T. He, J. A. Stankovic, and D. Luebke. A highaccuracy, low-cost localization system for wireless sensor networks. Proceedings of ACM Sensys, 2005.   
[20] B. H. Wellenhoff, H. Lichtenegger, and J. Collins. Global Positioning System: Theory and Practice. Springer Verlag, 1997.   
[21] Z. Yang, M. Li, , and Y. Liu. Sea depth measurement with restricted floating sensors. Proceedings of IEEE RTSS, 2007.   
[22] K. Yedavalli, B. Krishnamachari, S. Ravula, and B. Srinivasan. Ecolocation: A technique for rf based localization in wireless sensor networks. Proceedings of IEEE IPSN, 2006.   
[23] G. Zhou, T. He, S. Krishnamurthy, and J. A. Stankovic. Models and solutions for radio irregularity in wireless sensor networks. ACM Transactions on Sensor Networks, 2(2):221–262, May 2006.