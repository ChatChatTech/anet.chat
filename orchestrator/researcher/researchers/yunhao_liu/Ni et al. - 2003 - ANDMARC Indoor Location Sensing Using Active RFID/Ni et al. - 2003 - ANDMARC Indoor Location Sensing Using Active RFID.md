# LANDMARC: Indoor Location Sensing Using Active RFID\*

Lionel M. Ni $^{1,2}$ , Yunhao Liu $^{1}$ , Yiu Cho Lau $^{1}$ and Abhishek P. Patil $^{1}$

$^{1}$ Dept. of Computer Science & Engineering
Michigan State University
East Lansing, Michigan, USA
{ni,liuyun,lauyiuch,patilabh}@msu.edu

# Abstract

Growing convergence among mobile computing devices and embedded technology sparks the development and deployment of “context-aware” applications, where location is the most essential context. In this paper we present LANDMARC, a location sensing prototype system that uses Radio Frequency Identification (RFID) technology for locating objects inside buildings. The major advantage of LANDMARC is that it improves the overall accuracy of locating objects by utilizing the concept of reference tags. Based on experimental analysis, we demonstrate that active RFID is a viable and cost-effective candidate for indoor location sensing. Although RFID is not designed for indoor location sensing, we point out three major features that should be added to make RFID technologies competitive in this new and growing market.

# 1. INTRODUCTION

The proliferation of wireless technologies, mobile computing devices, and the Internet has fostered a growing interest in location-aware systems and services. Many applications need to know the physical location of objects. Over the years, many systems have addressed the problem of automatic location-sensing. Triangulation, scene analysis, and proximity are the three principal techniques for automatic location-sensing $[1]$ . One of the most well known location-based systems is the Global Positioning System (GPS) $[2]$ . However, GPS, as it is satellite dependent, has an inherent problem of accurately determining the location of objects located inside buildings. Different approaches have been proposed and

$^{2}$ Department of Computer Science
Hong Kong Univ. of Science and Technology
Kowloon, Hong Kong, China SAR
ni@cs.ust.hk

tested for their effectiveness and utilities in order to achieve the ability to locate objects within buildings.

The objective of our research is to develop an indoor location-sensing system for various mobile commerce applications. Our goal is to implement a prototype indoor location-sensing system using easily accessible wireless devices so that we can make use of existing infrastructures. At present, there are several types of location-sensing systems, each having their own strengths as well as limitations. Infrared, 802.11, ultrasonic, and RFID are some examples of these systems. Section 2 will give a comparative overview of these technologies and some related work. We are interested in using commodity off-the-shelf products. The results of our comparative studies reveal that there are several advantages of the RFID technology. The no contact and non-line-of-sight nature of this technology are significant advantages common among all types of RFID systems. They can work at remarkable speeds. In some cases, RF tags can be read in less than a 100 milliseconds. The other advantages are their promising transmission range and cost-effectiveness. Section 3 will give an overview of the RFID technology.

Section 4 introduces LANDMARC, a location-sensing prototype system based on RFID technologies. Since RFID is not designed for location sensing, the purpose of our prototype indoor location-sensing system is to investigate whether the RFID technology is suitable for locating objects with accuracy and cost-effectiveness. In Section 5, we present the experimental results of the LANDMARC system. Based on the analysis of this study, suggestions are given for manufacturers of RFID products to use these products in alternative and viable ways. Section 6 concludes the paper and describes future research.

# 2. RELATED WORK

A number of wireless technologies have been used for indoor location sensing.

Infrared. Active Badge, developed at Olivetti Research Laboratory (now AT&T Cambridge), used diffuse infrared technology [4] to realize indoor location positioning. The line-of-sight requirement and short-range signal transmission are two major limitations that suggest it to be less than effective in practice for indoor location sensing.

IEEE 802.11. RADAR is an RF based system for locating and tracking users inside buildings [3], using a standard 802.11 network adapter to measure signal strengths at multiple base stations positioned to provide overlapping coverage in a given area. This system combines empirical measurements and signal propagation modeling in order to determine user location thereby enabling location-aware services and applications. The major strengths of this system are that it is easy to set up, requires few base stations, and uses the same infrastructure that provides general wireless networking in the building. In most cases to date, the overall accuracy of the systems, using 802.11 technologies, is not as optimal as desired. For example, RADAR's implementation can place objects to within about 3 meters of their actual position with 50 percent probability, while the signal strength lateration implementation has 4.3-meter accuracy at the same probability level [1].

Ultrasonic. The Cricket Location Support System $[10]$ and Active Bat location system $[12]$ are two primary examples that uses the ultrasonic technology. Normally, these systems use an ultrasound time-of-flight measurement technique to provide location information. Most of them share a significant advantage, which is the overall accuracy. Cricket for example can accurately delineate 4x4 square-feet regions within a room while Active Bat can locate Bats to within 9cm of their true position for 95 percent of the measurements. However, the use of ultrasonic this way requires a great deal of infrastructure in order to be highly effective and accurate, yet the cost is so exorbitant that it is inaccessible to most users.

RFID. One well-known location sensing systems using the RFID technology is SpotON [13]. SpotON uses an aggregation algorithm for three dimensional location sensing based on radio signal strength analysis. SpotON researchers have designed and built hardware that will serve as object location tags. In the SpotON approach, objects are located by homogenous sensor nodes without central control. SpotOn tags use received radio signal strength information as a sensor measurement for estimating inter-tag distance. However, a complete system has not been made available as of yet. The above are popular technologies for indoor location sensing. Some other technologies, such as ultra-wideband $[15]$ , are also being investigated. The choice of technique and technology significantly affects the granularity and accuracy of the location information. There are some other projects using the above technologies. Due to the lack of availability of cost-effective indoor location sensing products, we have tried both infrared and 802.11b products. Neither was satisfactory for the above reasons. We do not intend to build our own devices due to cost constraint. We selected commercially available RFID devices as our prototyping technology, which is described below.

# 3. RFID TECHNOLOGY AND OUR FIRST ATTEMPT

RFID (RF Identification) is a means of storing and retrieving data through electromagnetic transmission to an RF compatible integrated circuit and is now being seen as a radical means of enhancing data handling processes $[14]$ . An RFID system has several basic components including a number of RFID readers, RFID tags, and the communication between them.

The RFID reader can read data emitted from RFID tags. RFID readers and tags use a defined radio frequency and protocol to transmit and receive data. RFID tags are categorized as either passive or active. Passive RFID tags operate without a battery. They reflect the RF signal transmitted to them from a reader and add information by modulating the reflected signal. Passive tags are mainly used to replace the traditional barcode technology and are much lighter and less expensive than active tags, offering a virtually unlimited operational lifetime. However, their read ranges are very limited.

Active tags contain both a radio transceiver and a button-cell battery to power the transceiver. Since there is an onboard radio on the tag, active tags have more range than passive tags. Active tags are ideally suited for the identification of high-unit-value products moving through a tough assembly process. They also offer the durability essential for permanent identification of captive product carriers.

After looking into the specifications of different available systems, we have chosen the Spider System manufactured by RF Code $[8]$ to implement the prototype framework. Their active tags have a read range of 150 feet. If necessary, this range can be increased to 1000 feet with the addition of a special antenna. The range that can be achieved in an RFID system is essentially determined by $[7]$ :

- The power available at the reader/interrogator to communicate with the tag(s).   
- The power available within the tag to respond.

\- The environmental conditions and structures (the former being more significant at higher frequencies including signal to noise ratio).

The field or wave delivered from an antenna extends into the space surrounding it and its strength diminishes with respect to distance. The antenna design will determine the shape of the field or propagation wave delivered, so that range will also be influenced by the angle subtended between the tag and antenna. In space free of any obstructions or absorption mechanisms, the strength of the field reduces in inverse proportion to the square of the distance.

In our system, the RFID Reader's operating frequency is 308 MHz. It also has an 802.11b interface to communicate with other machines. The detection range is 150 feet. The reader provides digital control of read range via providing configuration software and API with 8 incremental read ranges. Each reader can detect up to 500 tags in 7.5 seconds. Each RFID tag is pre-programmed with a unique 7-character ID for identification by readers. Its battery life is 3-5 years. Tags send their unique ID signal in random with an average of 7.5 seconds. Note that the RFID reader has 8 different power levels. Based on the signal strength received by the RFID reader, the reader will report or ignore the received ID, where power level 1 has the shortest range and level 8 has the longest range.

Our first attempt is to install a number of readers as shown in Fig. 1. Each reader has a pre-determined power level, thus defining a certain range in which it can detect RFID tags. By properly placing the readers in known locations, the whole region can be divided into a number of sub-regions, where each sub-region can be uniquely identified by the subset of readers that cover that sub-region. Given an RFID tag, based on the subset of readers that can detect it, we should be able to associate that tag with a known sub-region. The accuracy of this approach is then determined by the number of readers required, the placement of these readers, and the power level of each reader. Such a nicely formulated optimization problem turns out to be useless because the range in which a reader can detect a tagged object is not just due to the power level (similar to signal strength). There are many factors that will affect the range including both static obstructions and dynamic human movement. Due to these dynamic interferences, even a static object could be reported in different sub-regions from time to time. This is the same reason why approaches based on the signal strength of 802.11b are not very useful.

# 4. LANDMARC APPROACH

In order to increase accuracy without placing more readers, the LANDARC (LocAtioN iDentification based on dynaMic Active Rfid Calibration) system employs the idea of having extra fixed location reference tags to help location calibration. These reference tags serve as reference points in the system (like landmarks in our daily life). The proposed approach has three major advantages. First, there is no need for a large number of expensive RFID readers. Instead we use extra, cheaper RFID tags. Second, the environmental dynamics can easily be accommodated. Our approach helps offset many environmental factors that contribute to the variations in detected range because the reference tags are subject to the same effect in the environment as the tags to be located. Thus, we can dynamically update the reference information for lookup based on the detected range from the reference tags in real-time. Third, the location information is more accurate and reliable. The LANDMARC approach is more flexible and dynamic and can achieve much more accurate and close to real-time location sensing. Obviously, the placement of readers and reference tags is very important to the overall accuracy of the system.

![](images/8de24fe2608246c93748faa3241ffe3ce4782cd49ed62289eddd1b27ab4c7500.jpg)



Figure 1: Placement of 9 readers with two different ranges and the sub-regions.

The LANDMARC approach does require signal strength information from each tag to readers, if it is within the detectable range. However, the current RFID system does not provide the signal strength of tags directly to readers. Readers only report the power level (1 to 8 in our system) of the tag detected. We might do a preliminary measurement to know which power level corresponds to what distance. However, this may work only in free space. As indicated earlier, the power level distribution is dynamic in a complicated indoor environment. Thus, the physical distance cannot be computed accurately by using power levels directly. We have to develop an algorithm to reflect the relations of signal strengths by power levels.

# A. System Setup

The prototype environment consists of a sensing network that helps the location tracking of mobile users/objects within certain granularity and accuracy, and a wireless network that enables the communication between mobile devices and the Internet. The sensing network primarily includes the RF readers and RF Tags as mentioned earlier. The other major part of the infrastructure is the wireless network that allows wireless communication between mobile devices like PDAs and the Internet. In addition, it also acts as a bridge between the sensing network and the other part of the system. As the reader is equipped with the capability of communicating wirelessly using IEEE 802.11b wireless network, all the tag information gathered from readers is sent over to the supplied API sitting on a specific server (the location server). This feature does not have the problem of having a wire-connection to the readers, thus reducing the possible restrictions of where the readers could be placed. In addition, the wireless network will serve as the fundamental framework of all the communications in the infrastructure.

To be able to track an object's location, the location information received from the RF Readers has to be processed before being useful. After the signal is received by the RF readers, the readers then report the information to “TagTracker Concentrator LI” (a software program/API provided by RF Code, Inc.) via a wired or wireless network. Moreover, the software also acts as a central configuration interface for the RF readers. For example, it can be used to adjust the detection range and rate of the readers. After the information from the readers is processed by the TagTracker Concentrator LI, the processed location information can be buffered locally as a file on the same machine or transmitted via a network socket (configurable in the API).

# B. Methodology

Suppose we have $n$ RF readers along with $m$ tags as reference tags and $u$ tracking tags as objects being tracked. The readers are all configured with continuous mode (continuously reporting the tags that are within the specified range) and a detection-rang of 1-8 (meaning the reader will scan from range 1 to 8 and keep repeating the cycle with a rate of 30 seconds per range). We define the Signal Strength Vector of a tracking/moving tag as $\vec{S} = (S_1, S_2, \dots, S_n)$ where $S_i$ denotes the signal strength of the tracking tag perceived on reader $i$ , where $i \in (1, n)$ . For the reference tags, we denote the corresponding Signal Strength vector as $\vec{\theta} = (\theta_1, \theta_2, \dots, \theta_n)$ where $\theta_i$ denotes the signal strength. We introduce the Euclidean distance in signal strengths. For each individual tracking tag $p$ , where $p \in (1, u)$ , we define: $E_{j} = \sqrt{\sum_{i=1}^{n} (\theta_{i} - S_{i})^{2}}$

where $j \in (1, m)$ , as the Euclidean distance in signal strength between a tracking tag and a reference tag $r_{j}$ . Let E denotes the location relationship between the reference tags and the tracking tag, i.e., the nearer reference tag to the tracking tag is supposed to have a smaller E value. When there are m reference tags, a tracking tag has its E vector as $\vec{E} = (E_{1}, E_{2}, \ldots, E_{m})$

This algorithm is to find the unknown tracking tags' nearest neighbors by comparing different E values. Since these E values are only used to reflect the relations of the tags, we use the reported value of the power level to take the place of the value of signal strength in the equation.

There are three key issues we examine through the process of locating the unknown tracking tags. The first issue is the placement of the reference tags. Since the unknown tag is ultimately located in a cell surrounded by some reference tags, the layout of reference tags may significantly affect the location accuracy of an algorithm. The second issue is to determine the number of reference tags in a reference cell that are used in obtaining the most accurate approximate coordinate for each unknown tracking tag. For example, the simplest way to find the nearest reference tag to the tracking tag is to use the coordinate of the reference tag with the smallest E value as the unknown tag's coordinate. We call this as 1-nearest neighbor algorithm. Or, we can choose a tracking tag's two nearest neighbors and call it 2-nearest neighbor algorithm. When we use k nearest reference tags' coordinates to locate one unknown tag, we call it k-nearest neighbor algorithm. The unknown tracking tag' coordinate $(x, y)$ is obtained by:

$$
(x, y) = \sum_ {i = 1} ^ {k} w _ {i} (x _ {i}, y _ {i})
$$

where $w_{i}$ is the weighting factor to the i-th neighboring reference tag. The choice of these weighting factors is another design parameter. Giving all k nearest neighbors with the same weight (i.e., $w_{i} = 1/k$ ) would make a lot of errors. Thus, the third issue is to determine the weights assigned to different neighbors. Intuitively, $w_{i}$ should depend on the E value of each reference tag in the cell, i.e., $w_{i}$ is a function of the E values of k-nearest neighbors. Empirically, in LANDMARC, weight is given by:

$$
w _ {j} = \frac {\frac {1}{E _ {i} ^ {2}}}{\sum_ {i = 1} ^ {k} \frac {1}{E _ {i} ^ {2}}}
$$

This means the reference tag with the smallest E value has the largest weight. Note that our approach can be easily extended to a 3-dimensional coordinate.

# 5. EXPERIMENTAL RESULTS AND PERFORMANCE EVALUATION

We conduct a series of experiments to evaluate performance of the positioning of the LANDMARC System. In the standard setup, we place 4 RF readers (n=4) in our lab and 16 tags (m=16) as reference tags while the other 8 tags (u=8) as objects being tracked, as illustrated in Figure 2a.

With the setup, the data are collected via the socket from the TagTracker Concentrator LI in groups of a one-hour period and the system will compute the coordinates of the tracking tags based on each group of data. To quantify how well the LANDMARC system performs, the error distance is used as the basis for the accuracy of the system. We define the location estimation error, e, to be the linear distance between the tracking tag's real coordinates $(x_{0}, y_{0})$ and the computed coordinates $(x, y)$ , given by

$$
e = \sqrt {(x - x _ {0}) ^ {2} + (y - y _ {0}) ^ {2}}
$$

With the placement of the reference tags and the tracking tags shown in Figure 2 for over 48 hours, we keep collecting data of the power levels from 4 RF readers continuously. Thus we obtain 48 groups of one-hour data. For each of 8 tracking tags per hour, the system computes the coordinates of this tag by using the algorithm discussed in Section 4. We then compute the location error e for each tracking tag. Thus, we have 48 groups of 8 e values. We may examine the location accuracy by analyzing the distribution of these e values under different conditions. Note that we have repeated the experiments many times to avoid statistical errors.

# A. Effect of the Number of Nearest Neighbors

One of the key issues is to find a best k value in the algorithm. We choose different k values as k=1, 2, 3, 4, and 5 and compute the coordinates of the tracking tags, respectively. Figure 3 shows the results of using different k values in the formula.

As shown in Fig. 3, k=4 works the best and the positioning accuracy does not improve as the k value further increases.

Keeping the same placement, we repeat the process for another 48 hours. Though the positioning error distribution changes, k=4 still gives the best location information. In fact, in all the later experiments except on a few occasions that k=3 and k=5 worked better, in most cases k=4 is the best choice Hence, we set 4 as the value of k in our formula in the following experiments.

Based on the statistics, it can be seen that the 50 percentile has an error distance of around 1 meter while the maximum error distances are less than 2 meters. This is very promising because the 50 percentile of the RADAR project is around 2.37m-2.65m and its 90 percentile is around 5.93m-5.97m [9].

![](images/4b0a795a5ad972ab2d9de1f7fc13953caf6753554bd973e259cb0f711d6d51fd.jpg)



Figure 2a: Placement of RF readers and tags (standard placement)

![](images/29f782d3bbe1fde6251355cb66f04ee3a9a7a73fadea4afd1f724fea84e26562.jpg)



Figure 2b: Placement of RF readers and tags (placement configuration 2)

![](images/0d20bd640faf8a934f4e2eb907bcb67131f52bd964f8f05d790fc240ad177aac.jpg)



Figure 3: Cumulative percentile of error distance for k from 2 to 5.

# B. Influence of the Environmental Factors

In order to see how well the LANDMARC approach works in different environments, we collect 10 groups of data from midnight to early morning (during which time there is little movement) and another 10 groups of data from 10 AM to 3:00 PM (at which time varying level of activities that would result in variations in transmission of the tags). Figure 4 shows the comparison.

We know that during the daytime, the lab is very busy with many people so there is more interference than at night. From the results, we do not see much difference in the overall accuracy. This shows that our reference tag approach can successfully offset the dynamics of interference.

As the positions of tracking tags in the real world would be unpredictable, we change the placements of tracking tags randomly and expect the distribution of e could be changed but the accuracy of the system should be at the same level. We change the placement of the tracking tags as shown in Fig. 2b with the reference tags' placement unchanged and repeat the process.

![](images/2038d137c53f88727378117bede79e29e718db42f02c53efcd0944118c2e27f2.jpg)



Figure 4: Cumulative percentile of error distance in the daytime and at night.

![](images/6bad26a4fe10cf68f6bc0c03e6aa4373c475bf05df9d5bc92ca170f2c73a318b.jpg)



Figure 5: Cumulative percentile of error distance between two tracking tag placement configurations in Fig 2.

Figure 5 is the comparison of the results between the two tracking tag placements shown in Fig. 2. As we expected, the distribution is changed but the overall accuracy is at the same level. Figures 4 and 5 show that the approach of using reference tags effectively helps offset some of the environmental factors that contribute to the variations in a detected range. Since the reference tags are subject to the same effect in the environment as the tags to be located, we can dynamically update the reference information for lookup, based on the detected range from the reference tags in real-time.

# C. Effect of the Number of Readers

One of the problems of using RF to locate objects is the inconsistency of the signal strength reception. This can primarily be due to the environment and the device itself. In most cases, the environmental factors always have the most impact on the accuracy and maximum detectable range. These include issues like furniture placement, people's movement, and so on. Besides, non-line of sight (NLOS) is another source of reducing the location sensing accuracy. Even NLOS does not prohibit RF transmission as that of infrared, it does create the multi-path problem, meaning the signal can possibly take different paths to reach the receiver and result in interference among the received signals.

![](images/49109dc275138afc74e99967dfad1ba4d7cb8de3c396801121366bcc61929aeb.jpg)



Figure 6: Cumulative percentile of error distance for 3 and 4 RF readers.

To better deal with the problem, we can use more RF readers to improve the accuracy. With more RF readers, a better decision can be made for location sensing because more data can be gathered by having extra readers to do the sensing as shown in Fig. 6. However, the RF readers are usually quite expensive so placing more readers means extra costs for the whole system. Due to budget constraints, we have only four RF readers. Adding more readers may not necessary significantly increase the accuracy. It does increase the processing overhead.

# D. Effect of Placement of Reference Tags

Intuitively, placement of reference tags should have an effect on the measurement accuracy. Consider the two configurations shown in Fig. 7.

In the case of Fig 7a, where there is not any obstacle, it is probable that the system can easily find the tracking tag's four nearest neighbors which are tags e, f, h, and i by comparing the reported signal strengths and $E_{f}$ could be the smallest in this tracking tag's E vector. Thus, the tracking tag could be located among the four reference tags. However, sometimes the environment could be more complicated. Suppose there is a partition (or sometimes even a person standing like the partition) as shown in Fig. 7b. Under these circumstances, it is possible that the reception of the signal strength from the reference tag f is influenced by the partition (or the unexpected people). Consequently, the readers will report a weaker signal strength from tag f so that tag f could fail to be included in the four neighbors of the tracking tag. Instead, tag k may become one of the four reported nearest neighbors to the tracking tag as shown in Fig. 7b. Using e, h, i, k as the four reported neighbors, the position of the tracking tag is likely to be computed as indicated in Fig. 7b. Thus, more error occurs.

![](images/57d5e46139020847c4da3b0c4a1371bae1b9aa88e9963cd5ed69ffe4a684e0b0.jpg)



(a) without a physical partition

![](images/4c0d4c6af38d8d6d1521bf8eb2dc02644a09a4760f32f66aa1a550fa53652912.jpg)



(b) with a physical partition   
Figure 7: A physical partition to separate reference tags c and f from others.

Things will change if we place more reference tags as illustrated in Figure 8. Around the tracking tag, now we have placed more reference tags (the green ones in the Figure). Together with the tag i, tags m,n,o could be included in the four reported nearest neighbors of the tracking tag. Thus, better location information will be provided.

In our next experiment, we place all of the reference tags with a higher density as shown in Figure 9. In the first 48 hours we keep the original positions of all the tracking tags unchanged (case Near 1 in Fig. 9). In the next 48 hours we move the positions of the tracking tags as indicated in the case of Near 2 in Fig. 9.

It can be seen in Fig. 10 that the accuracy of the LANDMARC System is improved with a higher reference tag density, as we have discussed. However, the improvement is not as great as we expected. We will discuss this point later.

Figure 11 shows two configurations of a lower reference tag density. The corresponding distribution of error distance is shown in Fig. 12. As expected, the accuracy has dropped quite significantly.

![](images/de5d923de3aa6f804341033c01b7d6133725cd0e71db61f4ed62512c212b1cf2.jpg)



Figure 8: More reference tags are used.

![](images/6e3aea7b38214b3abd328a1db9933f8eaad70f5d1b7d6611e2d07228cffef6d6.jpg)



Figure 9: Two higher density, comparing with those in Fig. 2, placements of reference tags

![](images/ce62e665c3afd831d90451f2687dbbaedcadedb19daf37a761de19dc20fba739.jpg)



Figure 10: Cumulative percentile of error distance with a higher reference tag density

It is obvious that the accuracy of the LANDMARC approach decreases greatly with a lower density of reference tags. Thus, there is a tradeoff between the accuracy and the number of reference tags. Conceivably, we can improve the accuracy of the LANDMARC System by placing as many reference tags as we can, for example, even in every cubic square centimeter of the space where we want to locate objects. This does not make much sense due to the increased complexity, overheads, inherent device error, and measurement error. The experimental results have indicated that the LANDMARC approach works well. Using 4 RF readers in our lab, we roughly need one reference tag per square meter to accurately locate the objects within the error distance such that the worst error is 2 meters and the average is about 1 meter.

![](images/37cd28a878908023e00546bffc0f6793b3feb9cec7ff452d77b63d132478207d.jpg)



Figure 11: Two lower density, comparing with those in Fig. 2, placements of reference tags

![](images/d404d6387792cb7bbb89c95b34f57b16a9c585fecc159f20ca05e8b3d525340a.jpg)



Figure 12: Cumulative percentile of error distance with a lower reference tag density

We believe that the accuracy can be greatly improved if RFID vendors can make some design changes to be discussed in the next section.

# 6. CONCLUSIONS AND FUTURE RESEARCH

This paper has presented a prototype indoor location sensing system using active RFID. Although RFID is not designed for indoor location sensing, the proposed LANDMARC approach does show that active RFID is a viable cost-effective candidate for indoor location sensing. However, there are three problems that RFID vendors have to overcome in order to compete in a new and growing market.

The first problem is that none of the currently available RFID products provides the signal strength of tags directly. Instead, the reader reports “detectable” or “not detectable” in a given range. This forces LANDMARC to spend approximately one minute each time to scan the 8 discrete power levels and to estimate the signal strength of tags. By sending the signal strength information directly from readers, it will not only eliminate unnecessary processing time, but also reduce errors. This feature can easily be added as readers do have the signal strength information from tags.

The second problem is the long latency between a tracking tag being physically placed to its location being computed by the location server. There are two factors contributing to this long latency. One is the scanning time of different power levels as indicated above. This factor can be eliminated by sending the signal strength directly. The second factor is the time interval of emitting two consecutive IDs from an active tag. Our product has an average interval of 7.5 seconds in order to avoid signal collision for handling up to 500 tags. Depending on the total number of tags expected in a detectable area, this time interval can be further reduced. RFID vendors should provide a mechanism to allow users to reconfigure the time interval.

The third problem is the variation of the behavior of tags. When employing the LANDMARC approach, the basic assumption is that all tags have roughly the same signal strength in emitting the RF signal. In our experiments we found that the power level detected by the same reader from two tags in an identical location may be different. A possible explanation for the difference may be due to the variation of the chips and circuits, as well as batteries. In fact, before our experiments, we had conducted a series of pre-tests to classify tags based on their signal strength. Repeated experiments are needed to classify these tags due to the potential signal collision causing a detectable tag not detectable. This is another factor decreasing the accuracy of the system.

If all the above problems can be overcome, the accuracy and latency will be greatly improved. However, the error due to the dynamics of the environment can hardly be alleviated. A major advantage of LANDMARC is to help offset some of the environmental factors that contribute to the variation of accuracy of locating objects.

However, the dynamic environment is still one of the main reasons for increasing measurement errors, as we can never guarantee all the nearest neighbors and the tracking tag itself are always influenced equally. Sometimes a person standing in front of a tracking tag may greatly increase the error distance of locating this tag and such an error is often unpredictable.

In our experiments all reference tags are organized in a grid array. This may explain the reason of using 4 nearest neighbors. The influence of having other shapes of reference tags to the selection of the number of nearest neighbors will be investigated. Our methodology can easily be applied to 3D coordinates. The accuracy of the 3D case will also be studied. We are also investigating the use of Bluetooth for location sensing based on the same methodology. Each Bluetooth device emits a 48-bit unique ID, but with a shorter range of up to 10 meters. As Bluetooth, like RFID, is not designed for location sensing, it also has some inherent problems. The implementation of a location-sensing system based on Bluetooth is currently taking place in our lab.

# REFERENCES

[1] Jeffrey Hightower and Gaetano Borriello, “A Survey and Taxonomy of Location Sensing Systems for Ubiquitous Computing,” CSE 01-08-03, University of Washington, Department of Computer Science and Engineering, Seattle, WA, Aug 2001, http://www.cs.washington.edu/homes/jeffro/pubs/hightower2001survey/hightower2001survey.pdf.   
[2] Garmin Corporation. About GPS. Website, 2001, http://www.garmin.com/aboutGPS/   
[3] P. Bahl and V. N. Padmanabhan, RADAR: An Inbuilding RF-based User Location and Tracking System, Proceedings of IEEE INFOCOM 2000, Tel-Aviv, Israel (March 2000), http://www.research.microsoft.com/\~padmanab/papers/infocom2000.pdf.   
[4] R. Want et al., “The Active Badge Location System,” ACM Trans. Information Systems, Jan. 1992, pp. 91-102.   
[5] The BAT Ultrasonic Location System. http://www.uk.research.att.com/bat/.   
[6] Radio Frequency Identification (RFID) home page. http://www.aimglobal.org/technologies/rfid/   
[7] AIM (Automatic Identification Manufacturers), the trade association for the Automatic Identification and Data Collection (AIDC) industry, Getting Started in RFID - A Step approach, 2002,

http://www.aimglobal.org/technologies/rfid/resources/papers/rfid\_basics\_primer.htm   
[8] RF Code, Inc., http://rfcode.com/ProductsFrame.asp.   
[9] P. Bahl, V. N. Padmanabhan, and A. Balachandran, "Enhancements to the RADAR User Location and Tracking System," Microsoft Research Technical Report, February 2000, http://research.microsoft.com/\~bahl/papers/pdf/msr-tr-2000-12.pdf.   
[10] Nissanka B. Priyantha, Anit Chakraborty, and Hari Balakrishnan. The cricket location-support system. In Proceedings of MOBICOM 2000, pages32-43, Boston, MA, August 2000. ACM, ACM Press.   
[11] Jeffrey Hightower, Roy Want, and Gaetano Borriello, "SpotON: An Indoor 3D Location Sensing Technology Based on RF Signal Strength," UW CSE 00-02-02, University of Washington, Department of Computer Science and Engineering, Seattle, WA, Feb 2000, http://www.cs.washington.edu/homes/jeffro/pubs/hightower2000indoor/hightower2000indoor.pdf.   
[12] Andy Harter, Andy Hopper, Pete Steggles, Any Ward, and Paul Webster. The anatomy of a context-aware application. In Proceedings of the 5th Annual ACM/IEEE International Conference on Mobile Computing and Networking (Mobicom 1999), pages 59-68, Seattle, WA, August 1999, ACM Press.   
[13] Jeffrey Hightower, Chris Vakili, Caetano Borriello, and Roy Want, “Design and Calibration of the SpotON AD-Hoc Location Sensing System”, UW CSE 00-02-02, University of Washington, Department of Computer Science and Engineering, Seattle, http://www.cs.washington.edu/homes/jeffro/pubs/hightower2001design/hightower2001design.pdf   
[14] Mario Chiesa, Ryan Genz, Franziska Heubler, Kim Mingo, Chris Noessel, Natasha Sopieva, Dave Slocombe, Jason Tester, “RFID”, March 04, 2002, http://people.interaction-ivrea.it/c.noessel/RFID/research.html   
[15] AEtherwire. http://www.aetherwire.com/   
[16] Jeffrey Hightower, Roy Want, and Gaetano Borriello, "SpotON: An Indoor 3D Location Sensing Technology Based on RF Signal Strength," UW CSE 2000-02-02, University of Washington, Seattle, WA, Feb. 2000.