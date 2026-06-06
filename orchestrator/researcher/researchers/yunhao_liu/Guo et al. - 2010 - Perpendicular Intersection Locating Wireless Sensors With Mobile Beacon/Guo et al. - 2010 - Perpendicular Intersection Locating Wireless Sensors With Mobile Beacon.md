# Perpendicular Intersection: Locating Wireless Sensors With Mobile Beacon

Zhongwen Guo, Member, IEEE, Ying Guo, Student Member, IEEE, Feng Hong, Member, IEEE, Zongke Jin, Yuan He, Student Member, IEEE, Yuan Feng, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Existing localization approaches are divided into two groups: 1) range based and 2) range free. The range-free schemes often suffer from poor accuracy and low scalability, whereas the range-based localization approaches heavily depend on extra hardware capabilities or on the absolute received signal strength indicator (RSSI) values, which is far from practical. In this paper, we propose a mobile-assisted localization scheme called Perpendicular Intersection (PI), setting up a delicate tradeoff between range-free and range-based approaches. Instead of directly mapping RSSI values into physical distances, by contrasting RSSI values from the mobile beacon to a sensor node, PI utilizes the geometric relationship of a perpendicular intersection to compute node positions. We have implemented the prototype of PI with 100 TelosB motes and evaluated PI in both indoor and outdoor environments. Through comprehensive experiments, we show that PI achieves high accuracy, significantly outperforming the existing range-based and the mobile-assisted localization schemes.

Index Terms—Localization, mobile beacon, Perpendicular Intersection (PI), wireless sensor network (WSN).

# I. INTRODUCTION

L OCATING sensor nodes is a crucial issue and acts as afundamental element in wireless sensor network (WSN) / fundamental element in wireless sensor network (WSN) applications [1]. Localization can be classified as range-based and range-free approaches. Range-free approaches do not assume the availability or validity of distance information and only rely on the connectivity measurements (e.g., hop count) from undetermined sensors to a number of seeds [2]–[5]. Having lower requirements on hardware, the accuracy and precision of range-free approaches are easily affected by the node densities and network conditions, which are often unacceptable for many WSN applications that demand precise localizations. Range-based approaches calculate node distances based on some measured quantity, e.g., time of arrival (TOA),

Manuscript received August 6, 2009; revised December 25, 2009 and March 1, 2010; accepted April 9, 2010. Date of publication April 29, 2010; date of current version September 17, 2010. This work was supported in part by the National Science Foundation of China under Grant 60703082, Grant 60873248, and Grant 60933011 and by the National Basic Research Program of China (973 Program) under Grant 2006CB303000. The review of this paper was coordinated by Dr. Y. Gao.

Z. Guo, Y. Guo, F. Hong, Z. Jin, and Y. Feng are with the Department of Computer Science and Engineering, Ocean University of China, Qingdao 266003, China (e-mail: guozhw@ouc.edu.cn; guoying@ouc.edu.cn; hongfeng@ouc.edu.cn; jinzongke@ouc.edu.cn; fengyuan@ouc.edu.cn).

Y. He and Y. Liu are with the Key Lab for Information System Security of MOE, Tsinghua National Lab for Information Science and Technology, School of Software, Tsinghua University, Beijing 100084, China (e-mail: heyuan@cse.ust.hk; yunhao@mail.tsinghua.edu.cn).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TVT.2010.2049391

![](images/dd96a34b856995b16a6a41433d7826012f2889974f0e6ca4898b0ffc8f94401b.jpg)



Fig. 1. OceanSense Project. (Upper left) Floating sensor. (Upper right) Airscape of 20 floating sensors. (Bottom) Field photo of 20 floating sensors, labeled from 1 to 20.

time difference of arrival (TDOA), and angle of arrival (AOA) [6]–[8], whereas they usually require extra hardware support; thus, they are expensive in terms of manufacturing cost and energy consumption.

A popular and widely used ranging technique, which is sometimes treated as a “free lunch,” is the received signal strength (RSS) [6], [9] or quantified as the received signal strength indicator (RSSI). The fundamental stumbling block of existing RSSI-based approaches is that they rely on the absolute RSSI values to estimate physical distances [10]. Although RSSI-based approaches are easy to implement, they face many challenges. First, RSS is sensitive to channel noise, interference, attenuation, and reflection, resulting in irregular propagation in different areas and directions [9]. Second, radio attenuation greatly varies due to the environmental dynamics [11]. There is no universal signal propagation model that applies for all cases. As a result, it is often difficult to map the absolute RSSI values to physical distances.

This paper is motivated by one of our ongoing WSN projects, i.e., OceanSense [12], in which locating sensors is a critical task. As shown in Fig. 1, a number of restricted floating sensors [13] are deployed; they are usually tens of meters away from each other (sparsely deployed), and their wireless communications are often tampered by the environmental factors, including wind and tides.

As an early attempt in addressing the problem, we observe the RSSI behavior of sensor nodes through preliminary experiments, as detailed in Section III-A. We find that, although RSSI values are irregular and highly dynamic, the difference in RSSI values consistently reflect the contrast of physical distances. In other words, for the same pair of sensors, i.e., sender and a receiver, when one of them moves closer to the other, in most cases, if not all, the measured RSSI keeps increasing, although not in a smooth manner. Based on this observation, we propose Perpendicular Intersection (PI), which is an RSSIbased localization scheme using mobile beacon [14].

Major contributions of this paper are as listed follows.

• To avoid errors from directly mapping absolute RSSI values to distances, we obtain the geometrical relationship of sensors by contrasting the measured RSSI values. We then design a novel localization scheme, i.e., PI, which has better accuracy and low overhead, particularly under dynamic and complex environments.   
• We design the optimal trajectory of the mobile beacon in PI and theoretically prove its correctness. Only one mobile beacon is needed to broadcast beacon signals in PI, and other sensor nodes simply listen to the signals, store a few necessary packets, and compute their coordinates without interfering with each other.   
• We implement a prototype of PI with 100 sensors and evaluate its performance in real environments, including indoor and outdoor spots. We show the advantages of this design through comprehensive experimental results.

The rest of this paper is organized as follows. Section II summarizes the related works in the localization of WSNs. Section III presents our observations of RSSI and elaborates on the design of PI. Section IV presents our implementation and the experimental results. We conclude this paper in Section V.

# II. RELATED WORK

Many approaches have been proposed to determine sensor node locations, falling into two categories: 1) range-based approaches and 2) range-free approaches.

# A. Range-Based Approaches

Range-based approaches assume that sensor nodes can measure the distance and/or the relative directions of neighbor nodes. Various techniques are employed to measure the physical distance. For example, TOA obtains range information through signal propagation times [6], and TDOA estimates the node locations by utilizing the time differences among signals that are received from multiple senders [7]. As an extension of TOA and TDOA, AOA allows nodes to estimate the relative directions between neighbors by setting an antenna array for each node [8]. All those approaches require expensive hardware. For example, TDOA needs at least two different signal generators [7]. AOA needs antenna arrays and multiple ultrasonic receivers [8].

RSSI is utilized to estimate the distance between two nodes with ordinary hardware [6], [9]. Various theoretical or empirical models of radio signal propagation have been constructed to map absolute RSSI values into estimated distances [10]. The accuracy and precision of such models, however, are far from perfect. Factors such as multipath fading and background interference often result in inaccurate range estimations [9], [11].

Recently, mobile-assisted localization approaches have been proposed to improve the efficiency of range-based approaches [15], [16]. The location of a sensor node can be calculated with the range measurements from the mobile beacon to itself; therefore, no interaction is required between nodes, avoiding cumulative errors of coordinate calculations and unnecessary communication overhead. The localization accuracy can also be improved by multiple measurements that are obtained when the mobile beacons are at different positions.

# B. Range-Free Approaches

Knowing the hardware limitations and energy constraints required by range-based approaches, researchers propose rangefree solutions as cost-effective alternatives.

Having no distances among nodes, range-free approaches depend on the connectivity measurements from sensor nodes to a number of reference nodes, called seeds. For example, in Centroid [2], seeds broadcast their positions to their neighbor nodes that record all received beacons. Each node estimates its location by calculating the center of all seeds that it hears. In Approximate Point-in-Triangulation Test (APIT) [3], each node estimates whether it resides inside or outside several triangular regions bounded by the seeds that it hears and refines the computed location by overlapping such regions. As an alternate solution, DV-Hop only makes use of a constant number of seeds [4]. Instead of single-hop broadcasts, seeds flood their locations throughout the network, maintaining a running hop count at each node along the path. Nodes calculate their positions based on the received seed locations, the hop counts from the corresponding anchors, and the average distance per hop through trilateration.

Instead of using the absolute RSSI values, by contrasting the measured RSSI values from the mobile beacon to a sensor node, our proposed PI utilizes the geometric relationship of perpendicular intersection to compute the position of the node. In this sense, PI is actually between range-based and range-free approaches.

# III. DESIGN OF PERPENDICULAR INTERSECTION

In this section, we first describe the experimental observations on RSSI, which motivated this design. Section III-B presents the overview of the PI design. Section III-C discusses the optimal trajectory of the mobile beacon for PI. Section III-D presents our localization scheme in detail. Section III-E further introduces the extended design of PI, using random mobile trajectories for localization. For convenience of expression, the terms location, position, and coordinates are used interchangeably in the rest of this paper.

# A. Observations on RSSI

RSSI is initially used for power control in wireless networks. The existing signal propagation models of RSSI, however, are far from perfect, mainly because of the uncertain influences, e.g., background interference, nonuniform spreading, signal fading, and reflections. To better understand RSSI patterns, we conduct initial experiments with 12 TelosB sensors on our campus, as illustrated in Fig. 2(a).

In the first group of experiments, node A broadcasts signals, and the rest of the nodes receive RSSI values from their CC2420 transceivers. Node A moves from 10 m away from O to 20, 30, 40, and 50 m. All the measured RSSI values are shown in Fig. 2(b).

![](images/7d6d52eed13929055ac25470083fe8c4ebeb46c1938b7ea657fa40ebcffe1d8d.jpg)



![](images/de92913c3220f56724919ad780e2cd5714ae48dd02b4f2b0e197caf4c48743ea.jpg)



Fig. 2. Observations of RSSI outdoor. (a) Deployment sketch. (b) RSSI values of the received signals.

TABLE I RESULTS OF OUTDOOR OBSERVATION (IN METERS) 

<table><tr><td>|AO|</td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td></tr><tr><td>Estimated distance</td><td>9.62</td><td>19.19</td><td>30.41</td><td>34.12</td><td>60.68</td></tr></table>

TABLE II RESULTS OF INDOOR OBSERVATION (IN METERS) 

<table><tr><td>|AO|</td><td>4</td><td>8</td><td>12</td><td>16</td></tr><tr><td>Estimated distance</td><td>4.76</td><td>6.66</td><td>11.27</td><td>17.94</td></tr></table>

With the RSSI values from node A to a node, in an ideal sense, the distance between other nodes and node A should be calculated according to the log-normal shadowing model in (1), which is widely used in range-based localization approaches [6], [10], i.e.,

$$
\mathrm{RSSI} (d) = P _ {T} - P _ {L} (d _ {0}) - 1 0 \eta \log_ {1 0} \frac {d}{d _ {0}} + X _ {\sigma} \tag {1}
$$

where $P _ { T }$ is the transmission power, $P _ { L } ( d _ { 0 } )$ is the path loss for a reference distance of $d _ { 0 }$ ( ), and η is the path-loss exponent. The random variation in RSSI is expressed as a Gaussian random variable $X _ { \sigma } = N ( 0 , \sigma ^ { 2 } )$ . All powers are in given in decibels = (0 )relative to 1 mW, and all distances are given in meters. η is set between 2 and 5. σ is set between 4 and 10, depending on the specific environment [10].

In Table I, we compare the real distances between nodes A and O with those estimated ones using (1). The average relative error of estimation is 9.06%.

Similar results are observed in an indoor environment. We conduct the second group of experiments in our laboratory. Node A moves from 4 m away from O to 8, 12, and 16 m. Table II lists the real distances between A and O and those estimated ones using (1). The average relative error of estimation is 10.09%.

The aforementioned observations reveal that distance estimations based on the log-normal shadowing model and absolute RSSI values have very poor accuracy, which results in unacceptable localization errors in WSNs.

Interestingly, we find that the closer a node is to the signal sender, the larger the RSSI value that it perceives. In other words, although RSSI is irregular in practice, it is usually a fact that the RSSI between two nodes monotonically decreases as the nodes move further away from each other. This simple observation motivates our design of PI. Instead of directly mapping RSSI values into physical distances, PI locates the nodes by contrasting the RSSI values and utilizing the geometric relationship among the nodes.

![](images/f937e8af704be848757ed1b61f5b0708af6e965cfcde7dd425daaa8aae3fa3d3.jpg)



Fig. 3. Example of the PI scheme.

# B. PI

In our experiment, when the mobile beacon moves along a straight line, the largest RSSI value received by a sensor node often, if not always, corresponds to the point on the line that is closest to the node. Theoretically, this point should be the projection of the node on the line. Given two different projections of the sensor node on the trajectory, this node can be located as the intersection point of two perpendiculars that cross the mobile beacon’s trajectory over the two projections, respectively.

To illustrate how PI works, we show an example in Fig. 3, where a mobile beacon traverses the region while periodically broadcasting beacon packets. A beacon packet contains the coordinates of the position of the mobile beacon. The solid black lines in Fig. 3 form the trajectory of the mobile beacon, with the arrows denoting its moving directions. The mobile beacon (in red) starts at point $P _ { 1 }$ , changes its direction at point $P _ { 2 }$ , and stops at point $P _ { 3 }$ . By combining the trajectory with the virtual line $P _ { 1 } P _ { 3 }$ , we obtain a virtual triangle $\triangle P _ { 1 } P _ { 2 } P _ { 3 }$ (we call it VT from now on).

Let R be the transmission range of the mobile beacon. To ensure that all the nodes in a VT can receive the signals from the beacon, the sides $P _ { 1 } P _ { 2 }$ and $P _ { 2 } P _ { 3 }$ should not be longer than R. Meanwhile, the angle θ between the two lines should satisfy $0 < \theta \leq \pi / 3$ .

0 3Suppose that the five nodes (in blue) in Fig. 3 are located using PI. We use node $N ( x , y )$ as an example. The mobile beacon starts at point $P _ { 1 }$ ( )and broadcasts the start signal with its current location. Node N records the start position when it hears the start signal. Along its trajectory from $P _ { 1 }$ to $P _ { 2 } { \mathrm { . } }$ , the mobile beacon periodically broadcasts beacon packets with its current location. Node N receives all the beacon packets and records the beacon packet with the largest RSSI value. When the mobile beacon arrives at $P _ { 2 }$ , it broadcasts a stop signal with its current location. When node N receives the stop packet, it knows that the mobile beacon has just finished traversing the line from $P _ { 1 }$ to $P _ { 2 }$ . The recorded position is the position where the beacon packet with the largest RSSI value broadcast. We label the recorded position as $A ( x ^ { \prime } , y ^ { \prime } )$ .

( )According to the observations in Section III-A, line segment NA is the shortest among all the line segments that connect node N and any point on line $P _ { 1 } P _ { 2 }$ . In other words, point A is the projection of node N on line $P _ { 1 } P _ { 2 }$ . Hence, line NA is perpendicular to line $P _ { 1 } P _ { 2 }$ , and we have

$$
\frac {y _ {2} - y _ {1}}{x _ {2} - x _ {1}} \times \frac {y - y ^ {\prime}}{x - x ^ {\prime}} = - 1. \tag {2}
$$

Similarly, when the mobile beacon moves from $P _ { 2 }$ to $P _ { 3 } ,$ , another position $B ( x ^ { \prime \prime } , y ^ { \prime \prime } )$ is recorded, which is the projection of node N on line $P _ { 2 } P _ { 3 }$ ). Thus, we have

$$
\frac {y _ {3} - y _ {2}}{x _ {3} - x _ {2}} \times \frac {y - y ^ {\prime \prime}}{x - x ^ {\prime \prime}} = - 1. \tag {3}
$$

By solving (2) and (3), we can compute the coordinates $( x , y )$ of node N as follows:

$$
\binom {x} {y} = \left( \begin{array}{c c} x _ {2} - x _ {1} & y _ {2} - y _ {1} \\ x _ {3} - x _ {2} & y _ {3} - y _ {2} \end{array} \right) ^ {- 1} \times M \tag {4}
$$

where

$$
M = \left( \begin{array}{c c c c} x _ {2} - x _ {1} & y _ {2} - y _ {1} & 0 & 0 \\ 0 & 0 & x _ {3} - x _ {2} & y _ {3} - y _ {2} \end{array} \right) \left( \begin{array}{c} x ^ {\prime} \\ y ^ {\prime} \\ x ^ {\prime \prime} \\ y ^ {\prime \prime} \end{array} \right).
$$

In the aforementioned process, we only contrast the RSSI values and utilize the geometric relationship among the nodes and the beacon to conduct localization. The location calculation requires no absolute values of RSSI nor is it based on any signal propagation model. This way, PI is expected to avoid the potential errors generated from the translations from RSSI to distances.

# C. Optimal Trajectory

Clearly, a sensor node can easily be located when it is in the scope of a VT. When the entire deployment area of a sensor network cannot be covered by one VT, however, the trajectory of the mobile beacon to locate all the sensor nodes needs further considerations. We require an optimal trajectory with the following characteristics.

1) Assuming that all the beacon packets are received, the trajectory can locate all the sensor nodes in a deployment area. The optimal trajectory thus consists of multiple joint VTs, which cover the entire deployment area.

![](images/685308bcb42f7bf31b46b21ce5110faeb94089b3e8a1bd5424b16eca98231c00.jpg)



Fig. 4. Sensor network and its optimal trajectory of the mobile beacon.

2) It is the shortest trajectory so that the mobile beacon traverses the entire area in the shortest time. Consequently, every VT in the optimal trajectory covers the largest area, given its perimeter. We define such a VT as the optimal VT.

To use PI, the trajectory should include at least two intersecting lines, which are not longer than R, and the angle between them satisfies $0 < \theta \leq \pi / 3$ . The two lines can form a triangle, 0 3and we only consider the triangle here.

Theorem 1: The optimal VT in PI is an equilateral triangle, with the lengths of its sides all equal to R, where R is the transmission radius of the mobile beacon.

This theorem can directly be proven, because the equilateral triangle will minimize the trajectory while maximizing the area for a given perimeter. According to Theorem 1, we can conclude that the trajectory of a mobile beacon is optimal when it consists of multiple joint optimal VTs, as depicted in Fig. 4.

# D. PI Scheme

If a node only receives two pairs of start and stop signals broadcast by the mobile beacon, it knows the three vertices of the VT and then locates itself. Nodes at special positions, however, might receive more than two pairs of start and stop signals, and PI needs to deal with this situation.

As illustrated in Fig. 4, nodes $N _ { 1 } , N _ { 2 } , N _ { 3 }$ , and $N _ { 4 }$ represent four special cases, where $N _ { 1 }$ can receive three pairs of start and stop signals when the mobile beacon traverses sides $P _ { 1 } P _ { 2 }$ , $P _ { 2 } P _ { 3 } .$ , and $P _ { 3 } P _ { 4 } . \ N _ { 2 }$ receives four pairs of signals when a beacon traverses $P _ { 5 } P _ { 6 } , P _ { 6 } P _ { 7 }$ of one VT, and $P _ { 8 } P _ { 9 } , P _ { 9 } P _ { 1 0 }$ of another VT. $N _ { 3 }$ receives three pairs of signals when the mobile beacon traverses sides $P _ { 8 } P _ { 9 } , P _ { 9 } P _ { 1 0 }$ and $P _ { 1 0 } P _ { 1 1 } . \ N _ { 4 }$ receives six pairs of signals when the mobile beacon traverses the six sides of four VTs $\triangle P _ { 5 } P _ { 6 } P _ { 7 } , \triangle P _ { 8 } P _ { 9 } P _ { 1 0 } , \triangle P _ { 9 } P _ { 1 0 } P _ { 1 1 }$ , and $\triangle P _ { 1 0 } P _ { 1 1 } P _ { 1 2 }$ .

If a node receives start and stop signals from all the three vertices of a VT, we call this VT a locating VT for the node. For example, in Fig. 4, -P2P3P4 is the locating VT for node $N _ { 1 }$ , because node $N _ { 1 }$ can receive start and stop signals from $P _ { 2 } , P _ { 3 }$ , and $P _ { 4 }$ . PI lets each node compute the sum of RSSI values from the three vertices of a locating VT, and the locating VT whose vertices have the largest sum of RSSI values is used to calculate the node location.

OnMessageReceived(Message m){
    if (m.flag==start){//start of side(i)
    side.clear(); //clear the variable side(i-1)
    Record(side.start,m);
    //save RSSI and position of the
    //first beacon signal on side(i)
    rssi $_{max}$ =m.RSSI; position $_{max}$ =m.position;
} else if ((m.flag==beacon)and(m.RSSI≥rssi $_{max}$ )){
    //larger RSSI, update current
    //rssi $_{max}$ and position $_{max}$ rssi $_{max}$ =m.RSSI; position $_{max}$ =m.position;
} else if (m.flag==stop){//end of side(i)
    Record(side.stop,m);
    side(i)=side; cp(i)=position $_{max}$ ;
    if (side(i-1).stop==side(i).start){
    loc=calculate(side(i-1),side(i));
    //keep the one with the largest SumRSSI(),
    //if multiple location results exist
    if((loc!=location) and (SumRSSI(loc)
    >SumRSSI(location)))
    location=loc;
    }
    }
}   
Fig. 5. PI algorithm.

The pseudocode of the main function on message processing in PI is shown in Fig. 5. We define $s i d e ( i ) ( 1 \leq i \leq 6 )$ as the ( )(1 6)side from which the node receives the ith pair of start and stop signals. Let $c p ( i )$ denote the point on side i that is closest ( ) ( )to the node. Variable side denotes the current side traversed by the mobile beacon. Variables $r s s i _ { \mathrm { m a x } }$ and $p o s i t i o n \mathrm { _ { m a x } } ,$ respectively, denote the current largest RSSI value and its corresponding beacon position. Variable loc denotes the location calculated from the current locating VT. The final result of the node coordinates is stored in the variable location. $S u m R S S I ( p )$ calculates the sum of RSSI values from the ( )three vertices of the position $p \mathrm { ^ { \circ } s }$ locating VT.

PI can address all the special cases. For example, $N _ { 1 }$ receives three pairs of start and stop signals, respectively, from the locating VTs $\triangle P _ { 1 } P _ { 2 } P _ { 3 }$ and $\triangle P _ { 2 } P _ { 3 } P _ { 4 } ;$ therefore, the corresponding calculated results by using these two locating VTs are the coordinates of points $N _ { 1 } ^ { \prime }$ and $N _ { 1 }$ . For a node at point $N _ { 1 } , \triangle P _ { 2 } P _ { 3 } P _ { 4 }$ has a larger sum of RSSI values than $\triangle P _ { 1 } P _ { 2 } P _ { 3 }$ . Thus, the coordinates of point $N _ { 1 }$ can correctly be selected in place of the coordinates of $N _ { 1 } ^ { \prime } .$ . Similarly, nodes $N _ { 2 } , N _ { 3 }$ , and $N _ { 4 }$ can determine their coordinates from multiple calculated results. In practice, there will be too many special cases to enumerate; thus, we omit the enumeration here and choose to validate the performance of PI with real-world experiments.

# E. Extended Design of PI

The practical application scenarios often restrict the use of line trajectories of PI. Thus, we extend the design of PI, which is applicable with random trajectories in a certain deployment area. A new mobile beacon is used in the extended design, which is made up of a beacon node, a rotating arm, and the associated mobile device (wheels). Taking one end of the arm as the center, the beacon node that is mounted on the other end can rotate around it. It is assumed that the beacon node knows not only its own coordinates but the angle between the arm and the east direction as well. When the arm is not rotating, it is always oriented to the east. Given the angular velocity of the beacon node as a constant, the direction of the arm can be obtained by recording the rotating angle when the beacon node rotates. Fig. 6 shows the sketch of a mobile beacon and the mobile trajectory in the extended design. The length of the rotating arm is denoted by l, the direction angle is denoted by ω, and the current position of the beacon node is denoted by x, y .

![](images/f9aee3716b3a335688d2791c54496247234e71062fd5e917f3211df25550108f.jpg)



Fig. 6. Extended PI trajectory.

( )When there is not any obstacle on the way, the mobile beacon follows the basic scheme of PI and moves along the line trajectory in Fig. 4. Otherwise, it adopts the extended scheme as follows.

When the line trajectory of PI cannot be achieved in a certain area of the physical environment, e.g., in Fig. 6, the mobile beacon stops at a vertex of the corresponding locating VT, e.g., point $A _ { 1 }$ in Fig. 6. The beacon node then starts to rotate for 360◦. The beacon node first calculates the coordinates of the center of its rotating circle, i.e., the other end of the arm, by $( x - l , y )$ . The coordinates of the center stay unchanged during ( )the whole cycle of rotation, because the center is stationary. Meanwhile, the beacon node broadcasts its current coordinates and the coordinates of the center at a specified frequency during the rotation process. The beacon node stops broadcasting when the rotating arm finishes the whole cycle, and the whole mobile beacon moves to the next vertex of the corresponding locating VT, e.g., point $A _ { 2 }$ in Fig. 6.

The other sensor nodes receive the beacon packets from the mobile beacon and contrast the RSSI values of the beacon packets when the arm rotates around the center. It records the position that corresponds to the strongest RSSI. The strongest RSSI theoretically corresponds to a point on the circle, which is closest to the node to be located. In other words, the circle center, the beacon node at that point, and the node to be located are collinear.

For example, node $N ( x , y )$ is a node to be located in Fig. 6. ( )When the center of the rotation circle is $A _ { 1 } ( x _ { 1 } , y _ { 1 } )$ , node N ( )records the strongest RSSI when the beacon node is at position $B ( x _ { b } , y _ { b } )$ . Thus, we have

$$
\frac {y - y _ {1}}{y _ {b} - y _ {1}} = \frac {x - x _ {1}}{x _ {b} - x _ {1}}. \tag {5}
$$

Similarly, when the center of the rotation circle is $A _ { 2 } ( x _ { 2 } , y _ { 2 } )$ , the strongest RSSI corresponds to position $C ( x _ { c } , y _ { c } )$ ). We

TABLE III PARAMETER SETTINGS OF THE LOG-NORMAL SHADOWING MODEL FOR DIFFERENT ENVIRONMENTS OF HL, LABORATORY, RC, PLS, GP, AND OS 

<table><tr><td>Environment</td><td>HL</td><td>LA</td><td>RC</td><td>PL</td><td>GP</td><td>OS</td></tr><tr><td> $\eta$ </td><td>2.9</td><td>3.6</td><td>2.7</td><td>3.1</td><td>3.0</td><td>3.4</td></tr><tr><td> $P_{L}(d_{0})[dBm]$ </td><td>41</td><td>44</td><td>41</td><td>42</td><td>42</td><td>43</td></tr><tr><td> $\sigma$ </td><td>4</td><td>5</td><td>4</td><td>5</td><td>5</td><td>4</td></tr></table>

have

$$
\frac {y - y _ {2}}{y _ {c} - y _ {2}} = \frac {x - x _ {2}}{x _ {c} - x _ {2}}. \tag {6}
$$

By solving (5) and (6), we get the coordinates of node N. We have

$$
\binom {x} {y} = \left( \begin{array}{c c} y _ {1} - y _ {b} & x _ {1} - x _ {b} \\ y _ {2} - y _ {c} & x _ {2} - x _ {c} \end{array} \right) ^ {- 1} \times M \tag {7}
$$

where

$$
M = \left( \begin{array}{c c c c} y _ {1} - y _ {b} & x _ {1} - x _ {b} & 0 & 0 \\ 0 & 0 & y _ {2} - y _ {c} & x _ {2} - x _ {c} \end{array} \right) \left( \begin{array}{c} x _ {1} \\ y _ {1} \\ x _ {2} \\ y _ {2} \end{array} \right).
$$

# IV. PERFORMANCE EVALUATION

To better evaluate the PI design, we implement a prototype system of PI with 100 TelosB sensors in various environments, including a library hall (HL), a laboratory, a racket court (RC), parking lots (PLs), a grassplot (GP), and a sea surface/offshore (OS). The mobile beacon is also a TelosB mote that manually moves. The beacon node keeps recording the movement speed (a constant in our experiments) and the amount of time it has run, which can be used to calculate its own current position. A sink is deployed to collect the localization results of all the sensor nodes.

We evaluate the performance of PI in six different environments and compare it with two other RSSI-based localization approaches—a range-based approach of trilateration (TRL) and a mobile-assisted localization approach—which are briefly introduced as follows.

In TRL [17], beacon packets from the three vertices of the locating VT where the node resides are used to calculate its location. As for the mobile-assisted localization approach, it exploits Bayesian inference to improve the estimation accuracy [15]. We call that approach BI. Six beacon packets are used in the computation process of BI. Three of them are sent from the three vertices of the locating VT at which the node resides, whereas the other three are randomly chosen from the positions on the two sides of that VT. Both approaches rely on the signal propagation model of (1) to transform absolute RSSI values to physical distances.

We obtain the appropriate settings of the parameters in (1) through measurements beforehand [10]. All the parameter settings used by BI and TRL in the following experiments are listed in Table III.

![](images/a743a3693930cbe24c9bf286fbb2686d140c939fe4f59a60516b60cf42b10fb0.jpg)



(a）  
![](images/42cfcbe3370052aec55eaa882faad2ad644aecb22f6da2cc085597d9d327c0fc.jpg)



![](images/f6ec76cf1a18da4bdd2c073573a452dbac79c0be2556365730af0fa57bf170bb.jpg)



(c)   
Fig. 7. HL experiment. (a) Deployment sketch map. (b) RSSI values of beacon packets received by node ${ \dot { N } } _ { 6 }$ . (c) Estimation error of 14 nodes.

# A. HL Experiment

The first experiment is conducted in the HL of our library. Fourteen sensor nodes are randomly deployed, and the side length of a VT is 15 m. The moving velocity is 0.1 m/s, and the broadcast frequency is 1 Hz. The sensor nodes to be localized are put on the ground. The sink is the laptop linked to one TelosB mote. The sketch of this deployment is described in Fig. 7(a).

Fig. 7(b) plots the RSSI values of the beacon packets received by node $N _ { 6 }$ . We can clearly see two extrema of the RSSI values on the curve. Fig. 7(c) compares the estimation errors of the PI,

TABLE IV ERRORS OF OVERLAND EXPERIMENTS (IN METERS) 

<table><tr><td rowspan="2">Results</td><td colspan="2">PI</td><td colspan="2">BI</td><td colspan="2">TRL</td></tr><tr><td>Ave.</td><td>S.D.</td><td>Ave.</td><td>S.D.</td><td>Ave.</td><td>S.D.</td></tr><tr><td>HL</td><td>1.22</td><td>0.38</td><td>2.49</td><td>0.77</td><td>3.36</td><td>0.95</td></tr><tr><td>LA</td><td>2.04</td><td>1.05</td><td>2.75</td><td>1.15</td><td>3.97</td><td>1.50</td></tr><tr><td>RC</td><td>1.22</td><td>0.45</td><td>2.23</td><td>0.87</td><td>3.69</td><td>1.45</td></tr><tr><td>PL</td><td>1.29</td><td>0.31</td><td>2.21</td><td>0.34</td><td>3.73</td><td>0.88</td></tr></table>

BI, and TRL approaches. The average estimation error of PI is 1.22 m, and the standard deviation of estimation error is 0.38 m. The average and standard deviation of the estimation errors of BI and TRL are shown in Table IV.

# B. Laboratory Experiment

To examine PI’s performance in a more dynamic complex environment, we perform another experiment in the laboratory of a computer center, which is a room of 324 m2 with 120 computers and desks inside. Some people are sitting, standing, or moving in the room. We use 100 sensor nodes, which are randomly scattered in the whole room. The moving velocity of the mobile beacon is set at 0.1 m/s, and the broadcast frequency is set at 1 Hz. The side length of a VT is 9 m. The sketch of this deployment is plotted in Fig. 8(a).

Fig. 8(b) shows the cumulative distribution of estimation errors of all the 100 nodes. The average and standard deviation of the estimation errors of the three approaches are compared in Table IV. The results demonstrate that PI outperforms BI and TRL with lower estimation errors and more stable precisions, even in a complex environment.

Moreover, BI and TRL can adjust their parameter settings of the log-normal shadow model to make themselves more adaptive to the environment of the laboratory, as shown in Table III. PI’s parameters are the speed of mobile beacon and the broadcast frequency, which do not change with environments. Due to such facts, PI’s performance more apparently decreases than those of BI and TRL when comparing the HL and the laboratory. Nevertheless, the location accuracy of PI is still clearly better than those of BI and TRL.

# C. Outdoor Experiments

Now, we move the experiments to the outdoor environments, i.e., the RC and PLs. The moving velocity of the mobile beacon is set at 0.1 m/s, and the broadcast frequency is set at 1 Hz. The side lengths of the locating VT are both 15 m. The localization errors of four typical sensor nodes in the two environments are shown in Fig. 9(a) and (b), respectively.

Table IV compares the estimation errors of the three approaches in the previous four overland experiments. We can see that PI outperforms BI and TRL in all cases, with lower estimation errors and more stable precision. Even the worst result of PI (in the laboratory) is better than the best results of BI and TRL.

We further find that the three approaches achieve the lowest estimation errors in the HL experiments, similar estimation errors in two outdoor experiments, and the largest estimation errors in the laboratory experiments. This result is consistent with the fact that all RSSI-based localization approaches are more or less affected by the interference in wireless signal propagation and the dynamics of the environments. This result again confirms the advantage of PI, which compares the measured RSSI values of beacon packets to calculate the coordinates of the nodes, tolerating the irregularity of the RSSI signals to a certain degree.

# D. Extended PI Algorithm

We also carry out experiments to analyze the performance of the extended PI algorithm. The experimental area is a GP of 13.2 m ∗ 6.6 m, as shown in Fig. 10(a). The angular velocity of the mobile beacon is set at 30◦/s, and the broadcast frequency is set at 15 Hz. The mobile beacon moves and stops in a random fashion.

The localization errors of nine sensor nodes are shown in Fig. 10(b). We also compare the estimation errors of the extended PI algorithm with BI and TRL.

# E. OS Experiment

We have implemented PI in the OceanSense platform. Two typical floating sensor nodes are selected as the targets to be located. Prior to the experiments, we obtain the precise locations of these nodes with a Global Positioning System (GPS) equipment. In the experiments, a boat carries the mobile beacon and traverses the deployment field along a predefined mobile trajectory, which imitates the optimal one that contains these two sensor nodes inside, as shown in Fig. 11(a).

The localization results of PI, BI, and TRL are shown in Fig. 11(b). For PI, the estimation error is of 7.33 m, on average, which is much larger than the results of overland experiments. There are two reasons for this: 1) Our GPS equipment itself has an average estimation error of 3–4 m, and 2) compared with the optimal trajectory of the mobile beacon, the trajectory of the boat is anamorphic, because the boat does not have a precise steering device. Considering this problem, we will improve the OS implementation of PI by introducing an automatic mobile beacon.

Reason 1 has an equivalent effect on the location precision of all the three localization approaches. However, the precision of BI and TRL approaches is clearly not affected by reason 2. Nevertheless, Fig. 11(b) demonstrates that PI is still more accurate than BI and TRL, even with such an erratic trajectory. Although the average estimation error of PI is only 7.7% lower than that of BI in this experiment, we would emphasize that PI has much lower computation complexity than BI. Moreover, PI is still 24.8% more accurate than TRL.

# V. CONCLUSION

In this paper, we have proposed a mobile-assisted localization algorithm called PI. By comparing the received RSSI values on a sensor node, PI exploits the geometric relationship between the node and the trajectory of the mobile beacon, tolerating the irregularity of the RSSI signals. We have further designed the optimal trajectory of the mobile beacon with

![](images/d182f4ae29dc8f4cf72108dcf9c5eb1cf5d6c4fa4070f5c9624ab69bf5099118.jpg)



![](images/0c9c2f5515917818b44883991c4f94d517d5ef42ced0daa9f1ed9b696b3e3036.jpg)



Fig. 8. Laboratory experiment. (a) Deployment sketch map. (b) Cumulative distribution function (cdf) of estimation errors.   
![](images/4777dc7ef5cfe672793625a95a3b57b4ffa40283b1951eea8a5ee4e33001f824.jpg)



![](images/bfa49486eb03b6c1eed0d8841b547a5c4736f7cf6bd8a5581022faa406497633.jpg)



Fig. 9. Outdoor experiments. (a) RC results. (b) PL results.   
![](images/88637ac070b6300acbcf188754280367a8ea7bc9eef2eb810f4d120980eead89.jpg)



![](images/009e36eb0c4800e6340651a4fd56fa85151b86fa8f58436587c0984ced45de91.jpg)



Fig. 10. GP experiment. (a) Deployment sketch map. (b) GP results.   
![](images/e67bd89e0525837c301718ecf90a34173c46c53a77ed992a700f28583a9b53a2.jpg)



![](images/1d974780fe167026b244702ef63157283d2947c92f603e5c97f635bda2825613.jpg)



Fig. 11. OS experiment. (a) Trajectory of the mobile beacon. (b) OS experiment result.

respect to localization latency. We have implemented a prototype system of PI with 100 TeloB motes and evaluated its performance in various practical environments. All the experimental results demonstrate that PI is superior to all the existing approaches with high precision.

# REFERENCES

[1] I. F. Akyildiz, W. Su, Y. Sankarasubramaniam, and E. Cayirci, “A survey on sensor networks,” IEEE Commun. Mag., vol. 40, no. 8, pp. 102–114, Aug. 2002.   
[2] N. Bulusu, J. Heidemann, and D. Estrin, “GPS-less low-cost outdoor localization for very small devices,” IEEE Pers. Commun., vol. 7, no. 5, pp. 28–34, Oct. 2000.   
[3] T. He, C. Huang, B. M. Blum, J. A. Stankovic, and T. F. Abdelzaher, “Range-free localization schemes in large-scale sensor networks,” in Proc. ACM MobiCom, 2003, pp. 81–95.   
[4] D. Niculescu and B. Nath, “DV-based positioning in ad hoc networks,” J. Telecommun. Syst., vol. 22, no. 1–4, pp. 267–280, Jan. 2003.   
[5] M. Li and Y. Liu, “Rendered path: Range-free localization in anisotropic sensor networks with holes,” in Proc. ACM MobiCom, 2007, pp. 51–62.   
[6] P. Bahl and V. N. Padmanabhan, “RADAR: An in-building RF-based user location and tracking system,” in Proc. IEEE INFOCOM, 2002, pp. 775–784.   
[7] A. Savvides, C. Han, and M. B. Srivastava, “Dynamic fine-grained localization in ad hoc networks of sensors,” in Proc. ACM MobiCom, 2001, pp. 166–179.   
[8] D. Niculescu and B. Nath, “Ad hoc positioning system (APS) using AoA,” in Proc. IEEE INFOCOM, 2003, pp. 1734–1743.   
[9] J. Hightower, R. Want, and G. Borriello, “SpotON: An indoor 3-D location sensing technology based on RF signal strength,” Univ. Washington, Seattle, WA, UW CSE 00-02-02, 2000.   
[10] T. S. Rappaport, Wireless Communications: Principles and Practice. Englewood Cliffs, NJ: Prentice-Hall, 1999.   
[11] G. Zhou, T. He, S. Krishnamurthy, and J. A. Stankovic, “Models and solutions for radio irregularity in wireless sensor networks,” ACM Trans. Sensor Netw., vol. 2, no. 2, pp. 221–262, May 2006.   
[12] OceanSense. [Online]. Available: http://osn.ouc.edu.cn   
[13] Z. Yang, M. Li, and Y. Liu, “Sea depth measurement with restricted floating sensors,” in Proc. IEEE RTSS, 2007, pp. 469–478.   
[14] Z. Guo, Y. Guo, F. Hong, X. Yang, Y. He, Y. Feng, and Y. Liu, “Perpendicular intersection: Locating wireless sensors with mobile beacon,” in Proc. IEEE RTSS, 2008, pp. 93–102.   
[15] M. Sichitiu and V. Ramadurai, “Localization of wireless sensor networks with a mobile beacon,” in Proc. IEEE MASS, 2004, pp. 174–183.   
[16] N. B. Priyantha, H. Balakrishnan, E. D. Demaine, and S. Teller, “Mobile-assisted localization in wireless sensor networks,” in Proc. IEEE INFOCOM, 2005, pp. 172–183.   
[17] J. Hightower and G. Borriello, “Location systems for ubiquitous computing,” Computer, vol. 34, no. 8, pp. 57–66, Aug. 2001.

![](images/092b5890af89efb071cdae9985a5bb3cbeb3f41326245d162faf6575cb1171e9.jpg)



Zhongwen Guo (M’08) received the B.E. degree from Tongji University, Shanghai, China, in 1987 and the M.S. degree in applied mathematics and the Ph.D. degree in detection and processing of marine information from the Ocean University of China, Qingdao, China, in 1996 and 2005, respectively.

He is currently with the Department of Computer Science and Technology, Ocean University of China. His research interests include distributed oceanography information processing and network computing.

![](images/f19eed7953e2620e6c5a2c65f9b3a44a5601ee23729663a4c27794631e760c21.jpg)



Ying Guo (S’08) received the B.E. and M.E. degrees from Qingdao University of Science and Technology, Qingdao, China, in 2004 and 2007, respectively. She is currently pursuing the Ph.D. degree with the Department of Computer Science and Technology, Ocean University of China, Qingdao.

Her research interests include wireless sensor networks and underwater acoustic networks.

![](images/b6f622a54c259daee22785ff8b0dd6f22ee5b519043efc4cd5a6342c10a481a2.jpg)



Feng Hong (M’08) received the B.E. degree from the Ocean University of China, Qingdao, China, in 2000 and the Ph.D. degree in computer science and engineering from Shanghai Jiao Tong University, Shanghai, China, in 2006.

He is currently with the Department of Computer Science and Technology, Ocean University of China. His research interests include sensor networks, delay-tolerant networks, and peer-to-peer computing.

![](images/ababf4ad799a85a9c29f327b5da2695d07c13ea957aad6c6687ab0d6270d9572.jpg)



Zongke Jin received the B.E. degree from Qingdao University of Science and Technology, Qingdao, China. He is currently pursuing the M.E. degree with Department of Computer Science and Technology, Ocean University of China, Qingdao, China.

His research interests include sensor networks and delay-tolerant networks.

![](images/1c464492bff64ae0cf0e6510da15456ee95d7a3b2580a819dd4b4d0625ebc264.jpg)



Yuan He (S’09) received the B.E. degree from the University of Science and Technology of China in 2003, the M.E. degree from the Institute of Software, Chinese Academy of Sciences, in 2006, and the Ph.D. degree from the Hong Kong University of Science and Technology in 2010.

He is now a member of the Tsinghua National Lab for Information Science and Technology and a PostDoctoral Fellow with the Department of Computer Science and Engineering of the Hong Kong University of Science and Technology. His research

interests include wireless sensor networks, peer-to-peer computing, and pervasive computing.

![](images/68e10a558e5d4cb2f331249762f98abbc3a23b2486c5214353624859133ad04a.jpg)



Yuan Feng (M’08) received the B.S. degree in automation from Tsinghua University, China, in 1995, the M.A. degree from the Beijing Foreign Studies University, China, in 1997, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, in 2003 and 2004, respectively.

He is now a member of Tsinghua National Lab for Information Science and Technology and a faculty with the Department of Computer Science and Engineering of the Hong Kong University of Science and

Technology. His research interests include wireless sensor networks, peer-topeer computing, and pervasive computing.

![](images/d35b086e7f2c5e92a934f4d8f845a6d00666d2adfb34aabe01d5c2bba27e8dcf.jpg)



Yunhao Liu (SM’06) received the B.S. degree in automation from Tsinghua University, China, in 1995, the M.A. degree from the Beijing Foreign Studies University, China, in 1997, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, in 2003 and 2004, respectively.

He is now a member of Tsinghua National Lab for Information Science and Technology and a faculty member with the Department of Computer Science and Engineering of the Hong Kong University of Sci-

ence and Technology. His research interests include wireless sensor networks, peer-to-peer computing, and pervasive computing.