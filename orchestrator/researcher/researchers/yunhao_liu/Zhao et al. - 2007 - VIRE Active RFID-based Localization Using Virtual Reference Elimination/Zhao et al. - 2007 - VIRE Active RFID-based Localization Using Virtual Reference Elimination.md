# VIRE: Active RFID-based Localization Using Virtual Reference Elimination

Yiyang Zhao, Yunhao Liu and Lionel M. Ni

Department of Computer Science and Engineering

The Hong Kong University of Science and Technology, Hong Kong

{zhaoyy,liu,ni}@cse.ust.hk

# Abstract

RFID technologies are gaining much attention as they are attractive solutions to many application domains. Localization based on active RFID technologies provides a much needed added-value to further expand the application domain. LANDMARC was the first attempt using active RFID for indoor location sensing with satisfactory results. However, the LANDMARC approach suffers from two drawbacks. First, it does not work well in a closed area with severe radio signal multi-path effects. Second, to further improve the localization accuracy, more reference tags are needed which is costly and may trigger the RF interference phenomenon. The proposed VIRE approach can overcome the above drawbacks without additional cost. Based on the concept of virtual reference tags, a proximity map is maintained by each reader. An elimination algorithm is used to eliminate those unlikely locations to reduce the estimation error. Our experimental results show that the new method consistently enhances the precision of indoor localization from 17 to 73 percent over the LANDMARC approach at different tag locations in different environments.

# 1. Introduction

The localization problem has received considerable attention in the areas of pervasive computing and wireless networks as many applications need to know where objects are, and hence various location-based services are being created. Undoubtedly, the Global Positioning System (GPS) is the most well-known location service in use today. However, GPS is unsuitable for use in indoor environments. Some other technologies, such as infrared, ultrasonic, video cameras, and electro-magnetic field strength, are possible solutions with their own respective limitation and constraints [1]. Radio frequency (RF) is another promising technology, which utilizes Received Signal Strength Indicator (RSSI) to track moving objects if both moving objects and some reference objects are using RF signals to communicate. In theory, the RSSI obtained by the receiver is a function of the distance between the transmitter and the receiver as indicated in many propagation models [15]. However, in practice, there are many problems in applying these models. The indoor layout structure and moving objects can cause reflection, refraction, diffraction, dead-spots, and absorption of radio signals. Therefore, severe multipath phenomenon will occur and affect the accuracy of indoor location sensing. Moreover, many other factors also influence the RSSI, such as temperature, orientation of antenna, and height to the ground [2]. Nevertheless, since RSSI is readily available in wireless communication without additional cost, RF-based localization has become a hot research issue [3].

In RF-based localization, there are four basic models [7]. The first model is where the tracking object is attached to a transmitter (e.g., active RFID tags) and the location system calculates the object's position by information gathered from receivers deployed in known locations [11]. In the second model, the target object has to carry a receiver (e.g., 802.11x detectors). The tracking object is able to receive RSSI information from nearby transmitters (e.g., 802.11x access points) and compute its current position [4, 5]. The objects of the third model carry a transceiver (e.g., sensor nodes) and exchange information with other objects. In the fourth model called ‘transceiver-free’ technology, the tracking carries neither a transmitter nor a receiver. The position of the target object is obtained by comparing the changing RSSI characteristics [6, 7] in the environment. In order to improve the localization accuracy, many techniques have been proposed and this subject remains a hot research issue.

The paper will focus on the first model in which each object carries a transmitter, such as an active RFID tag. An active RFID tag can generate beacons independently. The read range of an RFID reader is typically 100 meters. The LANDMARC approach is one of the most popular indoor-localization technologies using active RFID tags [11]. It introduces the concept of reference tags with known locations to adapt to the environmental dynamics to enhance the accuracy of location estimation. As pointed out in [11], the implementation of LANDMARC did not work well due to the constraints of the equipment (different behaviors of tags), the long latency of feedback, the inability to provide accurate RSSI readings, and the low density of reference tags. Recently, the vendor has improved the functionality of the equipments by directly providing the RSSI readings, shortening the beaconing interval, and making all tags to have a similar behavior. From our experiments with the new equipments, we observe that the LANDMARC approach suffers from two drawbacks. First, it does not work well in a closed area with severe radio signal multi-path effects. Second, to further improve the localization accuracy, more reference tags are needed which is costly and may cause RF interference phenomenon. This has triggered the development of a new indoor localization technology using active RFID.

Our objective is to demonstrate a novel approach for providing high accuracy indoor localization using active RFID. The new system can be implemented at low cost without additional tags and readers. In this paper, we present and implement a novel method using active RFID called ‘Virtual Reference Elimination’ (VIRE). It allows efficient and accurate estimation of objection locations in indoor environments. In VIRE, instead of using many real reference RFID tags deployed in the sensing area, we employ the concept of virtual reference tags to provide denser reference coverage in the sensing area. To alleviate the effects of uncharacteristic signal behavior, each reader generates a proximity map formed by virtual tags. To estimate the possible position of an object, we can eliminate those unlikely positions based on the information from different maps with certain design parameters. Our experimental measurements show that the tracking accuracy can be improved by using VIRE over LANDMARC from 17% to 73%. The VIRE works well in complicated and closed indoor environments.

The rest of this paper is organized as follows. We give a brief overview of some related technologies in Section 2. In Section 3 we revisit the LANDMARC approach and point out some interesting observations. Our new approach, VIRE, is detailed in Section 4. In Section 5, we show results from system implementation and measurements. Finally, we conclude our work in Section 6.

# 2. Related Work

The RFID technology has been applied in many applications. A standard RFID system consists of three parts: RFID tags, readers, and middleware software [8]. The RFID tag is a mandatory part of an RFID system. It can convey information that is stored in an internal memory. Although there are many types of RFID tags in existence, we can distinguish them into two classes: active and passive [9]. Passive tags do not have any on-board power source, such as a battery or solar power, and they are very small and cheap. The transmission range of passive RFID tags is typically limited to less than 10 feet.

Unlike passive RFID tags, active RFID tags carry a power source which can power an integrated circuit to generate emitting beacons. The advantages of active RFID tags include longer working range, higher data bandwidth, automatically determining the best communication path, and stable performance within crowded environments [10].

Due to the benefits of active RFID mentioned above, some researchers have started to explore indoor localization using active RFID. Theoretically, in an open space the relationship between the distance and signal strength should be inversely squared. However, the relationship may change to a three or four power depending on the environment in a real situation. Furthermore, other factors may also affect this relationship. Therefore, we cannot find the position of one tag by calculating the signal strength directly. The LANDMARC approach was one of the effective methods [11]. It obtains the coordinates of tracking tags at different locations by comparing their RSSI values with those of reference tags at known locations. Basically, each reader can measure the RSSI readings from a tracking tag as well as those reference tags. A number of readers can then coordinate their readings of the tracking tag to identify some nearby reference tags. Based on the known locations of these reference tags, the location of the tracking tag can be estimated. The performance of LANDMARC based on the new equipments will be reported in Section 3. Some researchers have tried to improve upon the LANDMARC approach. For example, in [12], the authors proposed a triangulation mechanism to compute an additional coordinate. This approach can reduce the latency by decreasing the computing workload and enhance the location accuracy

Based on the RF technology, Bluetooth provides a way to connect and exchange information between portable and mobile devices. As a transmitter, Bluetooth devices work well in localization sensing. The BLN system $[13]$ composed by mobile badges and static Bluetooth nodes is proposed for indoor positioning service to locate users who carry Bluetooth devices inside a building. This method builds a cooperative location network in every room. It uses Bluetooth and Ethernet to cover a building. Based on the slave-master model, this system solves the tracking problem according to three phases: inquiry, page and connection, and slave-master tracking. If the tracking object moves to a region where a static node (SN) is deployed, the master node can estimate the location of the target, using the information combined by SN address and tracking address. It provides the room-scale precision for localization. The scalability of this system is limited by the transmission traffic. BIPS $[14]$ is another tracking system for mobile users at low speed like walking in a room. This system achieves about 3 or 4 meters of precision without considering the link setup delay.

# 3. LANDMARC: Revisited

# 3.1. Pitfalls of LANDMARC

The LANDMARC system consists of two parts: active RFID tags and RFID readers. Although LANDMARC is an effective location sensing system, as we mentioned earlier, it faces some constrained problems, such as no direct signal strength reading, long latency of reporting the location, varying behaviors of tags, and the low density of reference tags.

![](images/b23fdf97f0e972c1e6a938c80a0e48a07db08dec0a393876548ba3ce07c7afb6.jpg)



(a) Environment 1

![](images/df30237fc260bc9eed732602529b13322b7f349de10963b7a2828c2870360ee6.jpg)



(b) Environment 2

![](images/7dc3ab540345834b2196c56c9baa13fd5ceee39028cf422d6a2ad05da7aa4d3e.jpg)



(c) Environment 3   
Figure 1: The layout of the three different environments

In the original LANDMARC implementation, tags emit beacons, in average, every 7.5 sec. The long time interval of emitting two consecutive beacons from an active tag induces a long feedback time for localization, which severely limits the domain of application. Instead of reporting the exact RSSI value, the reader only provides eight discrete power levels which are used to control the transmission distance between the tags and the reader. The farthest power level is level 8 and the nearest is 1. The authors used power levels to estimate the RSSI which caused unnecessary localization inaccuracy. The third shortcoming of the LANDMARC system is the varying behavior of individual tags. Thus an expensive and time-consuming individual tag calibration has to be performed to reduce localization error. The localization accuracy can be improved by placing more reference tags which is costly. The first three pitfalls were mainly caused by the limitation of the equipments used in [11].

# 3.2. Facilities Improvement

Our new system uses equipments manufactured by RF Code $[16]$ , the same vendor as the equipment used in the original LANDMARC implementation but with improved hardware and software. The information of tags received by readers is gathered to a central processing server. The readers detect and interpret the radio frequency data emitted by active RFID tags, which can be read at distances of more than 1,000 feet depending on the antenna configuration. Through the software middleware program, we can directly obtain the useful information of reference tags and tracking tags including the tag ID, the reader ID, and RSSI values. At the suggestion of the authors, the new system not only solved the direct RSSI reading problem; it also reduced the beacon emitting interval to 2 seconds. Even better, all tags show very similar behavior.

# 3.3. Environmental Factors

Since the signal strength may differ at the same or similar distances between tags and readers when the system operates in different environments, we need to design experiments that work in different places. To measure the effectiveness of the tracking positions, we repeat the LANDMARC approach and gather measurement data from three quite different environments (Env1, Env2, and Env3) in our university. Env1 (Fig. 1(a)) is a semi-closed area which is not surrounded by concrete walls and furniture. Env2 (Fig. 1(b)) is a spacious closed area with not too many metallic objects near the sensing area. Env3 (Fig. 1(c)) is a typical office of our university which is a small room with many office desks and chairs. For each locale, we deploy tags and readers using the same placement called sensing area in Fig. 1. The distance between two adjacent tags is one meter. The readers are placed in the four corners of the sensing area.

Figure 2(a) shows the positions of the 9 tracking tags. The estimation errors of these tracking tags in Env1 and Env2 are much smaller than that in Env3. The main problem is the setting of Env3 which is susceptible to reflection of signals and filled with radio waves of similar wavelength. In Env1, the electromagnetic wave reflection property exerted a lesser influence hence a better result. In Env2, as the room size is larger, the concrete walls are further away from the tags. Therefore, the reflection influence is smaller.

Clearly the estimation error is depending on the location of the tracking tag. For Tag 1 which is well covered by four nearby reference tags, the estimation error is almost negligible in Env1 and Env2. Those tags in the boundary of the sensing area are encountered with much larger estimation errors. This is mainly due to the incomplete coverage of the nearby reference tags. Tag 9 has the worst location accuracy as it is slightly placed outside the boundary of the edge reference tags. The boundary problem can be overcome as we can put a much larger area of reference tags to cover the intended sensing area. The most important problem is the inaccuracy caused by a closed and complicate environment with severe radio signal multi-path effects.

![](images/40c9866667eca4231aa87b28754d9ff9e1d90c0fe0ee67428c9336727b19d132.jpg)



(a) Placement of the 9 tracking tags

![](images/de2f8cc299b64e1b9aa44589441bcb16d5431bbde5a806d43b64675fa89c6c60.jpg)



(b) Estimation error of the 9 tracking tags   
Figure 2: Localization results using the LANDMARC approach

# 4. The VIRE Approach

The key idea of the proposed VIRE approach is to gain more accurate positions of tracking objects by filtering out those unlikely positions without adding extra reference tags. In this section, we first discuss the relationship between the RSSI and the estimated position. Then, we describe our new approach in detail.

One of possible solutions to increase the precision is to put more reference tags. However, having a dense deployment of reference tags, the system will be more costly. More seriously, more reference tags will cause radio signal interference and affect the reading of RSSI values. Consequently, a bigger-than-estimated error for LANDMARC will occur. The motivation behind the new method is to improve the accuracy under the same situation as LANDMARC. The new method will generate higher accuracy without deploying additional reference tags.

The proposed VIRE approach has the following advantages. First, additional readers and tags are not required. Thus the hardware cost is the same as the LANDMARC approach. Second, the estimated position of a tracking object is more accurate and simple to calculate. Third, the new approach is more adaptive than LANDMARC in dynamic indoor scenarios. Thus, the VIRE approach can be easily adopted in real environments.

# 4.1. Interference of RSSI Values due to Excessive RFID Tags

From our experiments, we observed that the active tags placed in the same position have similar RSSI values from a given fixed reader when other environmental factors remain unchanged. Thus, when a tag is placed close enough to another tag whose position is known, their RSSI values are considered the same. Thus, the concept of reference tags proposed in LANDMARC is still used in our approach. An allowable difference of the RSSI values between the reference tag and tracking tag is defined as a threshold. If we can obtain the exact RSSI value for every place in the sensing region, the accurate position of the tracking tag can be discovered by looking for the same RSSI value. In order to obtain veracious RSSI values of different positions, we need to place more reference tags in the sensing area.

Theoretically, tags from different distances to a reader would give different RSSI values. Figure 3 shows the practical and the theoretical relationship between the RSSI value and the distance. For a given distance between the tag and the reader, the RSSI value is measured 20 times. In Fig. 3, in addition to the mean value, both maximum and minimum values are also shown. As the distance becomes greater, the change of RSSI values is not as smooth as expected. The zigzag behavior of RSSI values within proximity of tags does introduce some estimation error.

There are two other factors that influence the RSSI values of the proximity of tags. First, radio signal interference may occur when the distribution of tags is too dense. An interesting phenomenon is discovered during our experiments. When we put active RFID tags in the same position in sequence independently, the RSSI values of them are very similar. However, if we put more than 10 reference tags very closely together, those values become quite different as shown in Fig. 4 with 20 active tags 2 meters away from the reader. In Fig. 4, the 20 active tags are distinctly labeled from 1 to 20. When they are placed in sequence, their RSSI values are about the same. If they are placed together, the phenomenon of RF interference appears. Figure 4 also shows one snapshot of the RSSI values of the 20 tags with RF interference. This means that the density of the tags cannot be too dense if we want to deploy more reference tags to increase the location accuracy.

![](images/e4a20c587e89685d356ad469d104e840769234f0978fff69883815f2908c11b0.jpg)



Figure 3: The relationship of distance and RSSI

![](images/5f6426a00dc2ad03dd8396a545698969f1fc9fb402860ed439dbf26a0b6438ad.jpg)



Figure 4: Interference of tags

The second factor influencing the RSSI values of tags is that the surrounding disturbance comes mainly from human movement across the readers and tags while collecting data. The RSSI value is stable for a period of time if there is no moving object in the sensing area. Our experiments show that a sudden change of the RSSI value occurred when a person walked through the testing region. This will bring unexpected results and increases the estimation error. Such a factor should be avoided or filtered out when designing the location sensing system.

# 4.2. Virtual Grid Coordinate Determination

In VIRE, the real reference tags are properly placed to form a 2D regular grid. Tracking tags can be placed anywhere within the grid. The grid is further divided into a finer grid based on the concept of virtual reference tags for the sake of improving precision. Each physical grid cell covered by 4 real reference tags is further divided into n×n equal sized virtual grid cells. Each virtual grid cell can be considered as covered by four virtual reference tags. Since the coordinates of the four real reference tags are known, the coordinates of the virtual reference tags can be easily calculated. The concept of virtual reference tags can increase the accuracy of location estimation without additional cost and without causing RF interference.

The remaining challenge is to determine the RSSI value of each virtual reference tag to each reader. Our approach suggests that the RSSI values of virtual reference tags can be calculated by the linear interpolation algorithm. The n-1 virtual reference tags are equally placed between two adjacent real tags. The total number of reference tags will be increased to $(n+1)^{2}-4$ for every physical cell with four real tags. The RSSI values of those virtual tags can be obtained by the formulas shown below.

For the horizontal lines, the RSSI values of virtual tags are interpolated by the formula:

$$
S _ {k} \left(T _ {p, b}\right) = S _ {k} \left(T _ {a, b}\right) + p \times \frac {S _ {k} \left(T _ {a + n , b}\right) - S _ {k} \left(T _ {a , b}\right)}{n + 1}
$$

$$
= \frac {p \times S _ {k} \left(T _ {a + n , b}\right) + (n + 1 - p) \times S _ {k} \left(T _ {a , b}\right)}{n + 1}
$$

For the vertical lines, the RSSI values of virtual tags are interpolated by following formula:

$$
S _ {k} \left(T _ {a, q}\right) = S _ {k} \left(T _ {a, b}\right) + q \times \frac {S _ {k} \left(T _ {a , b + n}\right) - S _ {k} \left(T _ {a , b}\right)}{n + 1}
$$

$$
= \frac {q \times S _ {k} \left(T _ {a , b + n}\right) + (n + 1 - q) \times S _ {k} \left(T _ {a , b}\right)}{n + 1}
$$

where $\mathrm{S}_{\mathrm{k}}(\mathrm{T}_{\mathrm{i},\mathrm{j}})$ represents the RSSI value of the virtual reference tag located at the coordinate (i,j) for the k-th reader. The values of parameters are $a=\left\lfloor i/n\right\rfloor$ , $b=\left\lfloor j/n\right\rfloor,0\leq p=i\bmod n\leq n-1$ and $0\leq q=j\bmod n\leq n-1$ respectively. Assuming there are N×N virtual reference tags, the complexity of the interpolation algorithm is $\mathrm{O}(\mathrm{N}^{2})$ .

# 4.3. Elimination of Unlikely Positions

After the virtual reference grid is established, the RSSI value of each virtual reference tag can be calculated for each given reader. The RSSI value of the tracking tag can also be obtained by each reader. As discussed before, many places may correspond to a given RSSI value. The positions which have similar RSSI values are considered as possible location areas. We introduce the concept called proximity map which covers the whole sensing area and is divided into a number of regions, where the center of each region corresponds to a virtual reference tag. Thus the corresponding RSSI value of each region can be obtained. Each reader will maintain its own proximity map and the RSSI value of each region in the map can be calculated based on the RSSI readings of those real reference tags and be updated if the RSSI reading of a real reference tag is changed.

When the RSSI value of a tracking tag is obtained, the reader will mark those regions as '1' (or highlighted) if the difference of RSSI values between the region and tracking tag is smaller than a threshold as illustrated in Fig. 5. Suppose there are K readers. Thus, after obtaining K proximity maps from the K readers, an intersection function is applied to indicate the most probable regions from the K readers. We call this process as elimination as unlikely positions are eliminated. The threshold is used as an indicator to check for the existence of nearby tags. Finding an appropriate threshold is an important design parameter in VIRE. To reduce the detected area, a reduction of the threshold can be employed. We use an algorithm to adaptively reduce the threshold so as to find the minimum possible area. The algorithm works as follows:

![](images/d77afc94a7763c845d6dbf60a14b66beb767bb1658764f9a73908bc1c446907f.jpg)



Figure 5: Elimination Process

1. For each reader, we choose a threshold based on getting the largest area in the proximity map as the initial threshold.   
2. Reduce the chosen reader's threshold step by step until that particular area is reserved using this threshold.   
3. Choose the second largest area reader and repeat the reduction process.

At the last, the same threshold will be selected. If we choose an appropriate threshold, the accuracy will improve. The algorithm will give the smallest area formed by the smallest threshold available.

The results of the most probable regions are shown as black regions in Fig. 5. Since the total running time is $K^{2}$ , the computational complexity of the elimination algorithm is O(1). When the interpolation and elimination processes are finished, we can obtain a set of possible positions.

To improve the accuracy of VIRE, we introduce two weighting factors $w_{1i}$ and $w_{2i}$ . The weighting factor $w_{1i}$ demonstrates the discrepancy of RSSI values between the selected virtual reference tags and the tracking tag. This weighting factor is a function which depends on the difference of RSSI values.

$$
w _ {1 i} = \sum_ {k = 1} ^ {K} \frac {\left| S _ {k} (T _ {i}) - S _ {k} (R) \right|}{K \times S _ {k} (T _ {i})}
$$

The weighting factor $w_{2i}$ is a function related to the density of selected virtual reference tags (or regions). It can reduce the estimation error, which means the densest area has the largest weight. For example, four adjacent black regions in the lower part of Fig. 5 have a larger weight than the upper part (only two possible regions). We use $p_{i}$ to denote the ratio of conjunctive possible regions to the whole sensing area. The factor $w_{2i}$ can be obtained as follows.

$$
w _ {2 i} = \frac {p _ {i}}{\sum_ {i = 1} ^ {n _ {a}} p _ {i}} = \frac {n _ {c i}}{\sum_ {i = 1} ^ {n _ {a}} n _ {c i}}
$$

where $n_{ci}$ is the number of conjunctive regions, $n_{a}$ is the number of total regions in the whole sensing area. When we compute the coordinate of a tracking tag, the two weighting factors should be considered. We suggest an assorted weight $w_{i}$ as $w_{i}=w_{1i}\times w_{2i}$ . The calculated coordinate is given by

$$
(x, y) = \sum_ {i = 1} ^ {n _ {a}} w _ {i} (x _ {i}, y _ {i})
$$

Let $(x_{0},y_{0})$ denote the actual coordinate of the tracking tag. To analyze the performance of VIRE, we define the estimation error e using the following equation:

$$
e = \sqrt {\left(x - x _ {o}\right) ^ {2} + \left(y - y _ {o}\right) ^ {2}}
$$

# 5. System Implementation and Experimental Evaluation

In this section, we present the implementation of the VIRE approach and evaluate the VIRE approach by measuring different factors which influence the location errors, such as different testing environments, the density of virtual reference tags, and the threshold. The key metric to estimate a localization technique is the accuracy of the location. We evaluate our new algorithm on a real test-bed consisting of 16 reference tags and 4 readers. The distance between two adjacent tags in a row or in a column is 1 meter. The distance between the reader and the nearby edge tag is also 1 meter.

# 5.1. Effect of Experimental Environments

With the same three environments as we used in Fig. 1, we repeat the experiments using the VIRE approach. Figure 6 shows the comparison between the LANDMARC approach and the VIRE approach for the 9 different locations of the tracking tags in different environments (Fig. 2). Note that the scale of Y-axis is different in the three figures in Fig. 6 in order to show the improvement of VIRE over LANDMARC. The reduction in estimation error for VIRE is from 28% to 72% over LANDMARC for all 9 locations in Env1. For those non-boundary tags (Tag 1 to Tag 5), the worst estimation error is 0.21m and the average estimation error is 0.14m. For the case of Env2, the reduction in estimation error for VIRE is from 17% to 69% over LANDMARC for all 9 locations. For those non-boundary tags, the worst estimation error is 0.23m and the average estimation error is 0.17m. In Env3, the reduction in estimation error for VIRE is from 27% to 73% over LANDMARC for all 9 locations. The worst estimation error is 0.47m and the average estimation error is 0.29m for those non-boundary tags. Clearly, the VIRE approach provides a higher degree of accuracy than that of LANDMARC in all environments and at all locations.

![](images/fbd991dc670a94a19a0525e7d3e80cbd43523eaf5abdfa645268d993c05873ce.jpg)



(a) Env1

![](images/728dbd98a97fff8c88ce4e69a4074d1de0daf2fec04fc95d32479bb6e3eabb7c.jpg)



(b) Env2

![](images/048c6069454fbebd0841e33f0e86414e3763610914cc514137dd2348f258b773.jpg)



(c) Env3   
Figure 6: Comparison of VIRE and LANDMARC in three different environments

# 5.2. Effect of the Density of Virtual Reference Tags

The advantages of using virtual reference tags were discussed earlier. Here we evaluate the effect of the density of virtual reference tags on the localization accuracy. In theory, the higher the density of virtual reference tags, the greater the location sensing precision. Since there is no additional cost involved in having more virtual reference tags, how large should the number of virtual reference tags be? Obviously, the positioning accuracy will not improve as the number of virtual reference tags is beyond a certain number.

We use Env3 as an example. Figure 7 illustrates that there is a tradeoff between the average estimation error of those non-boundary tags and the number of virtual reference tags. Let $N^{2}$ be the total number of real and virtual reference tags. When the value of $N^{2}$ is increased up to 600, the accuracy does improve sharply. When the value of $N^{2}$ is between 600 and 900, the improvement is very small. When the value of $N^{2}$ is greater than 900, no further improvement is achieved and the estimation error is about 0.5 meters. In our other experiments, the value of $N^{2}=900$ is used.

# 5.3. The Impact of the Threshold

We must consider choosing an appropriate threshold to eliminate those unlikely positions as the threshold selection has a tremendous effect on the performance of VIRE. Actually, if the threshold is too big, many noisy virtual reference tags will be selected. Consequently, the average estimation error of VIRE will increase. On the contrary, if the threshold is too small, the real positions may be swept and the average error will also increase.

Figure 8 shows the relationship between the average estimation error of those non-boundary tags and the threshold for the case of Env3 with $N^{2}=900$ . When the threshold is near 1 or 1.5, the estimation error is the lowest.

# 6. Conclusion and Future Work

This paper presented a novel indoor localization approach – Virtual Reference elimination (VIRE). Indoor location sensing using active RFID is cost effective. It provides highly accurate results. The system, rather than requiring a large number of expensive RF readers, uses cheaper RF tags. It is effective for locating indoor objects. Both the LANDMARC and VIRE approaches employ the idea of having extra fixed reference tags to help location calibration. The LANDMARC approach uses an algorithm looking for the 4 nearest tags to calculate the coordinates of tracking tags. To provide better location sensing results, the VIRE approach which employs the interpolation and the elimination algorithm can significantly improve the accuracy over the LANDMARC approach without additional cost. To alleviate the large estimation error for those tags in the boundary of the sensing area, we recommend putting more reference tags in a large area to cover the sensing area. Thus each tracking tag can be well-covered by reference tags in all surrounding directions. If it is physically infeasible to put more reference tags beyond the sensing area, it will be an interesting future study to investigate how to identify such boundary tags and to compensate their localization accuracy.

Due to the limitation on the number of tags and readers we have, we are unable to provide a larger scale system performance study. As the future work, we would like to build a much larger reference tag array in a much larger sensing area to study the effects of different grid spacing distances and the size of boundary regions that should be avoided. Also if we have more readers, we would like to study the effects with more reader and the placement of these readers to the performance of VIRE. More performance data will be reported when more tags and readers are acquired.

In VIRE, we calculate the RSSI values of virtual reference tags using a linear interpolation algorithm. Linear interpolation is fast and easy. But it is not very precise in complex situations. Based on the observation mentioned before, the relationship between the RSSI value and the distance from a reader to a tag is a polynomial relation. If a suitable interpolation algorithm is used, the localization precision could be more accurate. However, polynomial interpolation also has some disadvantages. Calculating the interpolating polynomial is relatively very computationally expensive. Furthermore, polynomial interpolation may not be so exact after all, especially at the end points [17]. It may be interesting to study how much accuracy can be further achieved by using some novel nonlinear interpolation algorithms.

![](images/ee35a75cea96a360a64e097202b6945b303859db0121c6b08e48a7a40e7ce1f6.jpg)



Figure 7: The Number of Virtual Reference Tags vs. Accuracy

![](images/263493ce2c071647e64c40230ec3946a587acb6a59de1a31531b73e54a239c4f.jpg)



Figure 8: The Threshold vs. Accuracy

The requirement of having a square real grid is not necessary as long as we can systematically partition a real grid to a much finer virtual grid. For a closed and complex environment, we may put real reference tags around those obstacles. Then we can construct a virtual grid for each real grid cell with different granularity to potentially achieve a better accuracy. More investigation is underway in this direction. Further studies are required to consider more complex dynamic factors such as mobility and unstable obstacles in some real environments.

# Acknowledgement

This research was supported in part by Hong Kong RGC Grant HKUST6183/05E, the Key Project of Guangzhou Municipal Government Guangdong/Hong Kong Critical Technology grant 2006Z1-D6131, and the HKUST Nansha Research Fund NRC06/07.EG01.

# References

[1] J. Hightower and G. Borriello, "Location Systems for Ubiquitous Computing", IEEE Computer, vol. 34, pp. 57-66, 2001.   
[2] J. Ma, Q. Chen, D. Zhang, and L. M. Ni, "An Empirical Study of Radio Signal Strength in Sensor Networks", Technical Report, Dept. of Computer Science and Engineering, Hong Kong University of Science and Technology, March 25, 2006.   
[3] D. Moore, J. Leonard, D. Rus, and S. Teller, "Robust distributed network localization with noisy range measurements", in Proceedings of the Second International Conference on Embedded Networked Sensor Systems, 2004.   
[4] P. Bahl and V. N. Padmanabhan, "RADAR: An In-Building RF-based User Location and Tracking System", in Proceedings of IEEE INFOCOM, 2000.   
[5] J. Yin, Q. Yang and L.M. Ni, “Adaptive Temporal Radio Maps for Indoor Location Estimation,” Proc. of the 2005 IEEE Annual Conference on Pervasive Computing and Communications (PerCom 2005), Hawaii, pp. 85-94, March 2005.   
[6] Y. Liu, L. Chen, J. Pei, Q. Chen, and Y. Zhao, "Mining Frequent Trajectory Patterns for Activity Monitoring Using Radio Frequency Tag Arrays", in Proceedings of Percom, 2007.   
[7] D. Zhang, J. Ma, Q. Chen, and L. M. Ni, "An RF-based System for Tracking Transceiver-free Objects", in Proceedings of Percom, 2007.   
[8] S. Lahiri, "RFID Sourcebook": IBM Press, 2005.   
[9] R. Want, "An Introduction to RFID Technology", IEEE Pervasive Computing, vol. 06, 2006.   
[10] T. Hassan and S. Chatterjee, "A taxonomy for RFID", in Proceedings of Hawaii International Conference on System Sciences, 2006.   
[11] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, "LANDMARC: Indoor Location Sensing Using Active RFID", in Proceedings of PerCom, 2003.   
[12] G. Y. Jin, X. Y. Lu, and M. S. Park, "An Indoor Localization Mechanism Using Active RFID Tag", in Proceedings of the IEEE International Conference on Sensor Networks, Ubiquitous, and Trustworthy Computing, 2006.   
[13] F. J. Gonzalez-Castano and J. Garcia-Reinoso, "Bluetooth location networks", in Proceedings of Global Telecommunications Conference(GLOBECOM '02), 2002.   
[14] R. Bruno and F. Delmastro, "Design and Analysis of a Bluetooth-based Indoor Localization System", in Proceedings of Personal Wireless Communications, 2003.   
[15] T. S. Rappaport, "Wireless Communications Principles and Practice": Prentice-Hall PTR, 1996.   
[16] RF Code Corporation, http://www.rfcode.com/.   
[17] Wikipedia Encyclopedia, http://www.wikipedia.org