# RollCaller: User-Friendly Indoor Navigation System Using Human-Item Spatial Relation

Yi Guo $^{*}$ , Lei Yang $^{\dagger}$ , Bowen Li $^{\dagger}$ , Tianci Liu $^{\dagger}$ , Yunhao Liu $^{\dagger}$

\* Hong Kong University of Science and Technology, Hong Kong

$^{\dagger}$ School of Software and TNLIST, Tsinghua University, China

{yi, young, bowen, tian}@tagsys.org, yunhao@greenorbs.com

Abstract—Indoor navigation has received much attention in academics and industry in recent years. Previous methods often attempt to locate users with various localization algorithms in combination with an indoor map, so they need expensive infrastructures deployed in advance. In this study, we propose to utilize existing indoor objects attached RFID tags and the reader to navigate the user to the destination, without need of any extra hardware. The key insight is that the personal movement takes an impact on the Doppler frequency shift values collected from the indoor objects when getting close to the tag. Such local human-item spatial relation is leveraged to infer the users position and further navigate user to destination step by step. We implement a prototype navigation system, called RollCaller, and conduct comprehensive experiments to examine its performance.

Keywords—RFID, Doppler Frequency Shift, Human-Item Spatial Relation, Indoor Navigation

# I. INTRODUCTION

Have you ever searched a specific book in a huge book shelf? Have you been exhausted to seek a product in a shopping mall as finding a needle in a haystack? It is not a big deal if all books or products on the shelf are in order. However, things always go athwart. Books are always out of the order after someone takes them off the shelf, takes a look, and then puts back. The same problem occurs frequently in supermarket commodity. In this case, it is not easy to find or sort items properly.

Thanks to the rapid development of Internet of Things [1]–[3], RFID technique is widely deployed in many areas, like Wal-Marts and university libraries [4]–[10]. Before putting on the shelves, items in these places are attached with passive RFID tags, which can be identified by passive RFID reader in a distance. Each tag has a globally unique ID, and the mapping relation between each tag and item is recorded in the backend database.

Assisted by RFID technique, items can be located using RFID-based localization algorithms. Traditional RFID-based localization algorithms use the “present or absent” fashion in which the item can be recognized only when it is in the readers interrogation range. Being suitable for warehouse inventory, however, those methods are unsuitable for the above mentioned scenarios, because the coarse-grained localization can only tell which shelf the item is on, or even only tell whether the item is in the room. It is helpless when you want to find an item from tightly placed items.

Most RFID-based localization algorithms utilize some inherent attribute, like the received signal strength (RSS) of the backscattered signals from RFID tags, to achieve fine-granted localization. Using these algorithms, the localization accuracy 978-1-4799-3360-0/14/\$31.00 © 2014 IEEE

can be improved to an incredible level, where a specific item can be located within several centimeters. The question is: how can the user be navigated to the item he wants? Knowing the location information of the item, the user still has no idea of the path to the item since his location is unknown yet. A simple solution is to locate himself with the help of another localization algorithms. For example, we can facilitate WiFi-based localization technique, or even utilize the existing RFID system to perform RFID-based tag-free localization technique. However, using WiFi-based localization technique or similar techniques requires extra hardware deployment consuming extra system overhead. Due to the mobility of items on shelves, using RFID-based tag-free localization technique is also unrealistic. What was worse, the asynchronization and error superposition may lead to a totally wrong navigation.

Therefore, it is essential to develop a method which can directly measure the real-time human-item spatial relation without measuring the location of a person and the item separately. In this paper, we first develop a method to measure this local spatial relation between a person and an item by using the Doppler frequency shift in an RFID system. We then propose a fine-grained indoor navigation system, named RollCaller, to provide indoor navigation service for a user to find the desired item. The function of our RollCaller system is like its name: when a person wants to find an item, he then “calls” the items “name”. Then the RollCaller system navigates him to the item he is looking for. When the person walks right next to the item, the item “answers” the roll call immediately.

To design such a system, the most essential challenge is how to mine the human-item spatial relation between a person and an item without knowing their location information. We observe a phenomenon that the Doppler frequency shift of signals backscattered from RFID tags to reader antenna has a significant change when obstacle moves across the line of sight between the tag and the reader antenna. This phenomenon inspires us to depict the human-item spatial relation with the help of Doppler frequency shift.

Our major contribution may be summarized as follows:

- We propose to depict the spatial relation between person and item using Doppler frequency shift in RFID system. Compared with existing localization methods, our method can work in real time, and achieve the spatial relation between person and item without measuring their locations separately. This can greatly reduce the system overhead.   
- We propose an RFID reader antenna allocation method to estimate the RFID reader antennas using the human-item spatial relation measurement and IMU-based displacement measurement. Using this method, the relative locations of reader antennas can be achieved without pre-knowing the reader antennas' locations.

\- We implement an indoor navigation system. The comprehensive experimental results show that our navigation system works accurately and it is user-friendly.

The rest of this paper is structured as follows. We state the problem in Section II. The method we develop to measure the human-item spatial relation is described in details in Section III. After that, the RollCaller system design is presented in Section IV and the experiment results are evaluated in Section V. We introduce the related work in Section VI. Section VII concludes the paper.

# II. PROBLEM STATEMENT

The scenarios of library and supermarket we mentioned in the Introduction Section can be normally described as follow: a large amount of items, which are hard to distinguish at a glance, are tightly placed on huge shelves. Among these items, there exists a specific item that someone is looking for. This person will search such item on the shelves, reach the nearest position next to it beside the shelf, and take it off.

This searching process can be formalized as a localization problem accurately locating the specific item on the shelves. Attached with passive RFID tags, items on the shelves can be identified by RFID readers. We can apply the up-to-date localization methods using RFID technique, whose localization accuracy have been improved to an incredible level (centimeter level). However, in above scenarios, knowing the accurate location of the specific item is unnecessary and even wasteful. In fact, the person doesn't care about the exact coordination of the item he wants. To the contrary, he is more concerned about how he can be navigated to the rough location of that item, saying the shelf it is on. And while he is walking through the shelf passage, he can be noticed in time when he is exactly next to that item. In other words, the relative location between the person and the item he wants can help more in these scenarios.

In this paper, we no longer deal with the global location (like the coordination of the item in the library or supermarket) of an item, but facilitate the motion of the person, who is looking for the specific item through the shelf passage, to “discover” the item he wants. Our goal is to find a solution that can locate an item related to person in motion. Specifically, we aim at discovering the nearest location of a person in motion through the shelf passage to a specific item. The only devices we can utilize are a commercial smart phone and implemented RFID reader with multiple reader antennas inventorying the RFID tags on the items.

# III. HUMAN-ITEM SPATIAL RELATION

To achieve the goal in Section II, the first and most important problem to solve is how we can associate the location of the person and the item he wants, namely human-item spatial relation. The human-item spatial relation cannot be achieved by separately measuring the location of person and location of the item due to extra hardware requirements and system overhead. Besides, the superposed localization errors from either part will lead to non-ignorable composed error, neither does the asynchronization of the different parts of location measurements. What was worse, the mobility of the attached items even makes it hard to achieve the person's location. Therefore, a method which can directly describe the human-item spatial relation is necessary.

In our experiment, we observe a phenomenon that when a person moves across the line of sight between a passive RFID tag and an RFID reader antenna identifying that tag, the received reader carrier signal suffers a significant Doppler frequency shift event. It is enlightening that we can utilize this phenomenon to capture the spatial relation between the person and the attached item. The time stamp when this Doppler frequency shift event occurs is defined as Anchor Time Stamp. The formal definition and details will be shown in this section. We use the Anchor Time Stamp to describe the human-item spatial relation in the further design of our system.

# A. Doppler Frequency Shift in RFID System

Doppler frequency shift in RFID system is defined as the frequency change of the received reader carrier signal due to relative motion between the transmitter (RFID tag or the attached object) and the receiver (reader antenna) [11]. Generally, except for the scenario of using mobile reader, the antenna of the reader is reasonable to be simplified as static. Therefore, the major factor of Doppler frequency shift is the motion of the tag.

In our implementation, the Doppler frequency shift is calculated using phase-difference method within the duration of receiving one packet from a tag. This is because by using more than one packet, the phase difference can likely arise from the antenna switching during inventory, channel hopping, and etc, which strongly affects the accuracy of the measured Doppler frequency shift.

The measured Doppler frequency shift is susceptible by the environment. Besides the thermal noise of the environment, the other source of noise comes from the multipath effect. In fact, the reader carrier signal received by the reader antenna from the tag is always a composition of the main path signal (line-of-sight signal) and some multipath signals (reflection from surroundings). Even though the reader antenna and the tag are static, the reflector of the multipath signals may not be static. By this way, the phase differences of such multipath signals during the measuring period are nonzero. Therefore, the composed reader carrier signal received by the reader antenna has slight phase difference across the measured packet and hence causes slight Doppler frequency shift. The Doppler frequency shift of a static tag and static reader antenna in a room is shown in figure 1(a).

In order to distinguish the noise and the valuable Doppler frequency shift to be mentioned below, we set a noise level $f_{noise}$ to describe the boundary of Doppler frequency shift value for noise. In this example, the $\pm0.000005\%$ value is set as the noise level.

As we mentioned above, multipath effect can influence the measurement of Doppler frequency shift. However, the influence is slight if there is no obstacle between the reader antenna and the tag. This can be explained as the reason that the main path signal from line of sight is much stronger than the multipath signals from reflection of surroundings. And the phase difference introduced by the relatively weak multipath signals can only raise a little change on the composed reader carrier signal. Figure 1(b) shows the Doppler frequency shift result of a scenario that people walking in the surrounding of an on-working RFID system, but not directly going across the line of sight between the tag and reader antenna. Not surprisingly, the overall Doppler frequency shift is more variant but still in a limited range (bounded by $\pm 0.000005\%$ level of base frequency), which is ignorable comparing to the large change of Doppler frequency shift in our next experiment.

![](images/dbba105ce9b9cb9320fadaf4f09fc146ce120f35cb823cbeb35cb140d7191443.jpg)



(a) Doppler Frequency Shift without Human Walking around

![](images/082facc3d2dde660ef350474f0c6e46405f55cd32bbfb8df5300428d1d94a195.jpg)



(b) Doppler Frequency Shift with Human Walking around

![](images/e2bc08fa0e13ba9a32a150c18459557ffa249c0c8817e742061084e4dbb04963.jpg)



(c) Tag Diversity   
Fig. 1. Noise on Doppler Frequency Shift with Static Tags

Therefore, the Doppler frequency shift is insensitive to the surrounding. This result has a significance on the applications with noisy environment, like libraries and supermarkets.

As we can see, the values of Doppler frequency shift can be positive and negative. To simplify the expression, in the rest of this paper, all the Doppler frequency shift values are the absolute value of the measured data, and the noise level is therefore using the positive one.

Although the surroundings makes limited effect on the Doppler frequency shift of tags, it requires special notice that the noise level is not unique. In fact, it exists tag diversity on Doppler frequency shift noise for different tags. Figure 1(c) displays the experiment result of 14 different tags. In this experiment, the Doppler frequency shift of each tag is collected without obstacles between or across the middle of the tag and reader antenna. This figure shows the tag diversity of Doppler frequency shift whose average noise value varies from less than 10Hz to about 40Hz, and the maximum value varies from 15Hz to less than 70Hz. Despite the variant of average and maximum noise value, the noise value of all tags are bounded on reasonable level. We consider the 95% of maximum value of Doppler frequency shift of a tag to be its noise level.

# B. Observation: human Impact on Doppler Frequency Shift

Things are totally different when people are performing their action (walking, running or jumping) between the tag and the reader antenna. A person is walking normally across line of sight between the tag and the reader antenna, and the affected Doppler frequency shift of the reader carrier signal during this whole process is plotted in Figure 2. As shown in Figure 2, the Doppler frequency shift in this scenario experiences several periods: the Doppler frequency shift is initially oscillating below the noise level as the previous experiments. Then the Doppler frequency shift starts to go beyond the noise level and reaches the maximal point(s), as the center part in Figure 2.

![](images/fd040c91d4f66a82b2547e73ffe27f2827fa13d3ead72ed61e9c5c07eb7315ea.jpg)



Fig. 2. Effect on Doppler Frequency Shift when Human Walk across Line of Sight between Tag and Reader Antenna

After that, the Doppler frequency shift goes down and finally returns to the noise level again as we get at the beginning.

The different periods presented in Figure 2 is corresponding to different periods when the person walks across the line of sight between the tag and the reader antenna. They can be classified into following stages.

- Noise Stage: This stage occurs in the beginning and the ending of the person's walking behavior. In this stage, the person is away from the line of sight between the tag and the reader antenna. In other words, the person is not in the range that can affect the Doppler frequency shift of reader carrier signal.   
- Peak Stage: This stage occurs when the person finally reaches the line of sight between the tag and the reader antenna. The line-of-sight reader carrier signal is obstructed and the reader carrier signal from main path is suddenly disappeared. Meanwhile, if the reader antenna is receiving a packet and calculating the Doppler frequency shift via the phase difference, it will receive an initial phase mostly caused by the main path signal and a terminal phase caused without the main path. In this case, the phase difference is much larger than the value we get previously, reaching a local maximum. A similar maximum value can be achieved when the person is leaving the line-of-sight of tag and reader antenna, making an initial phase without main path signal and a terminal phase with main path signal.

It is unreasonable to assume that, each time a person reaches the line of sight between the tag and the reader antenna, the reader antenna happens to be receiving a part of a tag packet, where the reader antenna can receive a packet that partially contains main path signal and partially excludes the main path signal. In fact, it exists the situation that the person obstruct a complete packet's main path signal. Even though we cannot raise the Doppler frequency shift value to maximum value from the scenario with and without main path signal in a single tag packet receiving process, we can still identify the peak stage. This owes to the noisy surrounding. By obstructing the main path signal, the multipath signals can take place of the main path signal in the composition of the receiving reader carrier signal. Therefore, unlike the uninfluential multipath noise mentioned above, this time the Doppler frequency shift of multipath signals caused by reflecting objects in surrounding raise the Doppler frequency shift of the composed receiving reader carrier signal to value over noise level.

# C. Anchor Time Stamp

Based on the observation and analysis above, we can now define the Anchor Time Stamp mentioned in the beginning of this section as follow:

Definition 1: An Anchor Time Stamp $H_{i,j}$ is the time stamp when the human is on the line of sight between the reader antenna i and the tag j.

According to this definition, the Anchor Time Stamp can be narrowed to the interval of the peak stage mentioned above. However, The Anchor Time Stamp cannot be simply regarded as the time stamp of the maximal value occurs. Since the duration when a human obstructs the line of sight between human and item is pretty short (generally less than 400ms), the velocity during this period can be approximately assumed as constant. Therefore, a more reasonable choose to measure the Anchor Time Stamp is calculating the mean value of the peak stage time period.

Let $f_{D}(t)$ donates the Doppler frequency shift at time stamp t, and let the notation mean(·) donates the mean value calculation. The Anchor Time Stamp can be achieved by:

$$
H _ {i, j} = \text { mean } \{t \in T \mid | f _ {D} (t) | \geq \max | f _ {D} (t) | \cdot \beta \} \tag {1}
$$

where $\beta$ donates a confident level of the selected time stamp with the Doppler frequency shift that can be regarded as belonging to the peak stage. And the time interval T in Equation 1 meets the following condition:

$$
\operatorname{card} \{t \in T \mid | f _ {D} (t) | > f _ {\text { noise }} \} \geq C _ {0} \tag {2}
$$

where $C_{0}$ is a constant to measure whether a peak stage exists in time interval T. Equation 2 also works as a detection tool of Anchor Time Stamp event. When a time interval meets this equation, the system assumes that a person has go across the line of sight of the tag and reader antenna, and the Anchor Time Stamp is calculated. Furthermore, to raise the accuracy of Anchor Time Stamp event detection, a constraint should be added to limit the time interval T. Let w donates the reasonable time interval size of a human passing line of sight between tag and reader antenna. Suppose a human is with width 0.25m and walking in a speed of 0.5m/s, which is very slow, the size of T can be set as $w = 0.25/0.5 = 0.5s$ .

# IV. ROLLCALLER

With Anchor Time Stamp defined in Section III-C, we have the tool to describe the spatial relation between the moving person and the items attached with passive RFID tags. This helps us propose our system called RollCaller. Our RollCaller system is designed to navigate a person to the specific item he wants. Specifically, the RollCaller system can navigate a user to the shelf the wanted item is on. The user then walks through the passage beside that shelf. When the RollCaller system detects that the user is exactly next to that item, it announces the user to stop and take the item off the shelf.

![](images/0001cfd01c27f3f39794bd0a11662401f677fc58bdc274e85da0118dffd67133.jpg)



Fig. 3. System Architecture

# A. System Overview

The architecture of the RollCaller system is shown in Figure 3. To implement our RollCaller system, the following hardware is indispensable: (1) Passive RFID tags. Attached by RFID tag, items become recognizable by contact free RFID readers. (2) Passive RFID reader, along with multiple reader antennas for each. These readers transmit reader carrier signal and receive backscatter reader carrier signal from RFID tags, which can be used to identify the RFID tag and obtain Doppler frequency shift value. The Doppler frequency shift value can be further utilized to achieve Anchor Time Stamps. The reader antennas are deployed one by one on the opposite of the attached items across the passage (3) Back-end server. The back-end server runs back-end services to query data from RFID reader and perform calculation for our RollCaller system. (4) Smart phone, equipped with accelerometer and magnetometer and running a RollCaller client connecting with the back-end server. It is carried by the user to measure the displacement of himself using IMU-based displacement measurement [12], [13], [24]. Also, it acts as an interface to acquire the information of the item the user wants, and remind the user to stop to take that item.

The work flow of the RollCaller system can be separated into two periods: antenna allocation period and user navigation period. The antenna allocation period is designed to generate a relation map of the reader antennas. This map contains the spatial information of each antenna, including the shelf it is on and the spatial relation with the reader antennas on the same shelf. This map is used to detect the human-item spatial relation in the user navigation period. In user navigation period, the RollCaller system produces a navigation service to the user. According to the user's input information of item, the relation map of reader antennas, and the database recording the mapping of item information to tag information, the RollCaller leads him to the closest position to the item he wants. These two periods are activated by different conditions. The antenna allocation period is triggered once our RollCaller system is activated. After it starts, the relation map of the reader antennas keeps updating until the system is turned off. Unlikely to the antenna allocation period, the user navigation period is triggered when the user runs his client on the smart phone, inputs the information of the item he wants (like the item's name), and waits for the navigation service.

# B. Antenna Allocation Period

In RFID-based localization systems, the location of reader antennas are normally assumed to be pre-known. This is feasible in labs or testbeds. However, applying this assumption in the scenarios of libraries or supermarkets is far from practical: works of deployment of reader and reader antennas is always done by nonprofessional workers, who cannot help to configure the reader antenna deployment in the system. Besides, movement of shelves is possible, which will change the past deployment of reader antennas. Therefore, updating the reader antenna location message is necessary in our RollCaller system. Specifically, unlike other localization system, there is no need to know the reader antenna location in our RollCaller system. Instead, the RollCaller system only needs the spatial relation among reader antennas. In antenna allocation period, our goal is to generate a reader antenna relation map, which can be updated on time to guarantee the accuracy of the navigation.

The antenna allocation algorithm works as follow: suppose that there are M attached items on a shelf and N reader antennas on the opposite side across the passage facing the attached items. The items are assigned with IDs from $TAG_{0}$ to $TAG_{M-1}$ and the reader antennas are assigned with IDs from $ANT_{0}$ to $ANT_{N-1}$ . Specially, antenna $ANT_{0}$ is deployed at one end of the passage, playing the role as reference antenna. When a user walks in the passage, the passage, applying the Anchor Time Stamp detection algorithm we mentioned in Section III-C, the back-end server can obtain a sequence of Anchor Time Stamps $\{H_{ANT_{i},TAG_{j}} \mid i = 0, 1, \ldots, N - 1; j = 0, 1, \ldots, M - 1\}$ . Let $\vec{I}_{t_{1},t_{2}}$ donates the displacement of user from time stamp $t_{1}$ to $t_{2}$ measured by IMU-based tracking method using the smart phone carried by user, and $\vec{R}_{ANT_{i},ANT_{j},TAG_{k}}$ donates the calculated directed distance from reader antennas $ANT_{i}$ to $ANT_{j}$ using Anchor Time Stamps $H_{ANT_{i},TAG_{k}}$ and $H_{ANT_{j},TAG_{k}}$ . We can obtain the distance between antennas $ANT_{i}$ and $ANT_{j}$ using the property of similar triangles as follow:

$$
\left| \vec {R} _ {A N T _ {i}, A N T _ {j}, T A G _ {k}} \right| = \frac {\left| \vec {I} _ {H _ {A N T _ {i} , T A G _ {k}} , H _ {A N T _ {j} , T A G _ {k}}} \right|}{\gamma} \tag {3}
$$

where $\gamma \in (0,1]$ relates to the ratio of similitude. However, this parameter does not simply equal to the ratio of similitude since the direction of the user walking does not strictly parallel to the shelf. The value of this parameter will be discussed in Section V. Besides, the direction of $\vec{R}_{ANT_i,ANT_j,TAG_k}$ is the component of the direction of $\vec{I}_{H_{ANT_i},TAG_k,H_{ANT_j},TAG_k}$ along the passage.

Obviously, not all M tags can be recognized by every reader antenna due to the limited transmitting power and angle. Besides, the total number of tags M on the shelf is not fixed since the attached items may be taken away from the shelf, or new attached items may be put on the shelf. Therefore, in order to facilitate our description, the Anchor Time Stamp $H_{ANT_{i},TAG_{k}}$ is marked as N/A (not applicable) if antenna $ANT_{i}$ cannot recognize tag $TAG_{k}$ . The IMU-based displacement measurement and the reader antennas distance related to an Anchor Time Stamp marked as N/A are also N/A.

When the user walks in the passage, a set of antenna directed distances are obtained. Once the antenna directed distances in this set cover all the reader antennas along the passage, the relation map of these reader antennas can be generated like this: initially we select all the directed distances starting or ending with antenna $ANT_{0}$ . Since antenna $ANT_{0}$ is fixed at the end of the passage, these selected antennas can be marked on the relation map of reader antennas. After that, we select all the directed distances starting or ending with the antennas we have just marked on the relation map. Then we perform this process iteratively until all the antenna along the passage are marked on the relation map. Finally, the relation map of reader antennas is generated and applied in user navigation period to be mentioned in Section IV-C.

The IMU-based displacement measurements used to generate this map exists inaccuracy due to errors in stride length, direction estimation and etc. In order to improve the confidence of the reader antenna position map, we apply the minimal composition constraint [14] to compensate the errors above. The minimal composition constraint in RollCaller works like this: initially, we assign all the nodes' coordination to the reference reader antenna. Let $\hat{p}_i$ be the current coordination of reader antenna $i$ , and let $\vec{d}_{i,j} = \hat{p}_i - \hat{p}_j$ be the current displacement vector between reader antenna $i$ and a neighboring reader antenna $j$ . Suppose that the most recent $K_{i,j}$ displacement measurement between reader antenna $i$ and $j$ are used to adjust the antenna position, and let $\vec{r}_{i,j,k}$ be the $k^{th}$ measured displacement among these $K_{i,j}$ measurements. Then the adjustment vector $\vec{\epsilon}_i$ of reader antenna $i$ can be generated as:

$$
\vec {\epsilon} _ {i} = \frac {\sum_ {j = 0} ^ {N} \sum_ {k = 0} ^ {K _ {i , j}} (\vec {R} _ {i , j , k} - \vec {d} _ {i , j})}{\sum_ {j = 0} ^ {N} K _ {i , j , t}} \tag {4}
$$

This adjustment vector describes the composed effect of multiple displacement measurements to the reader antenna position. The precision of position $\hat{p}_{i}$ of the reader antenna i can be improved with the adjustment vector:

$$
\hat {p} _ {i} = \hat {p} _ {i} + \vec {\epsilon} _ {i} \tag {5}
$$

All the adjustment vectors in the passage should update once a new displacement vector is obtained in the passage. This is because for each position of reader antenna is changed, all the position of reader antennas in that passage should change since the displacement and adjustment vector calculated relate to all the reader antennas. In order to ensure the sensitivity of the user's displacement measurement characteristics (like the user's displacement error or the antennas' unexpected movement), the $K_{i,j}$ should be limited to a reasonable size.

It requires special attention that this relation map of reader antennas can be reused when the RollCaller system is restarted. This means that not each time the RollCaller system starts we should spend time to build this relation map. It can automatically adjust to the current map allocation using the past relation map as basic map. Of course, if the reader antennas location has significant changes, such as redecoration of library, this used relation map should be emptied and reconstructed.

# C. User Navigation Period

After the relation map of reader antennas is generated, the RollCaller system can begin to provide user navigation service. In user navigation period, when the RollCaller system receives a navigation request, it navigates the user to the input item in two steps: rough navigation and accurate navigation. In rough navigation step, the back-end server queries the item in the database. The corresponding RFID tag ID is then achieved and the rough location of this attached item (the shelf it is placed on) is measured by querying which antennas can inventory this item. According to this rough location information, the RollCaller system can first navigate the user to the passage beside the shelf which the item is on and start accurate navigation step immediately. Since the shelves are generally deployed sparsely enough to be found in a short time by humans, the navigation process in rough navigation step is therefore simple and will not be discussed in this paper.

The accurate navigation step starts immediately when the user has reached the shelf which the wanted item is on. It requires an event to transit from rough navigation step to accurate navigation step. Recalling the deployment of our reader antennas mentioned in Section IV-B, the reader antenna $ANT_{0}$ is deployed at the end of the passage. Similarly, an extra passive RFID tag $TAG_{ref}$ is attached on the shelf at the same end of the passage facing the reader antenna $ANT_{0}$ . Moreover, the virtual connection between tag $TAG_{ref}$ and reader antenna $ANT_{0}$ satisfies the requirement of perpendicular to the passage. Utilizing this special deployment, the Anchor Time Stamp $H_{ANT_{0},TAG_{ref}}$ is set to be the event that triggers the accurate navigation step. Also, this Anchor Time Stamp is used as a reference time stamp to assist the accurate navigation.

When the user enters this passage, the Anchor Time Stamp $H_{ANT_{0},TAG_{ref}}$ is obtained and the accurate navigation service starts. Suppose the RFID tag attached on the designated item is labeled $TAG_{s}$ , we can calculate the remainder displacement $\Delta D$ the user should move to reach the item by:

$$
\Delta D = \frac {\left(\vec {I} _ {H _ {A N T _ {0}} , T A G _ {r e f}} , H _ {A N T _ {i} , T A G _ {s}} - \vec {d} _ {A N T _ {i} , A N T _ {0}}\right) \cdot \gamma}{1 - \gamma} \tag {6}
$$

Equation 6 can be applied when the first Anchor Time Stamp relates to tag $TAG_{s}$ is detected. Since the accuracy of Anchor Time Stamp grows when the reader antenna is closer to the tag (this will be further evaluated in Section V), $\Delta D$ will keep updating while the user walking closer to the designated attached item. Finally, at the moment our RollCaller system considering to be the closest location of the user to the designated item, it reminds the user to stop via the client running on the smart phone. Till now, the user is successfully navigated to the item he wants, and the user navigation period is terminated.

# V. IMPLEMENTATION AND EVALUATION

In this section, we implement the RollCaller system and evaluate the performance.

# A. Implementation

We implement the RollCaller system in the laboratory environment. In our implementation, an Impinj Speedway Revolution RFID reader is used to transmit carrier signal to passive RFID tags, and receive backscattered carrier signal from tags. The reader is loaded with software version Octane 4.8 and equips 4 directional reader antennas. Besides, 9 Alien ALN-9634 passive RFID tags are used to evaluate our system. Both tags and reader antennas are placed in lines. The “tags line” and the “reader antennas line” form a passage with the width of 100cm. The deployment is shown in Figure 4. The reader antennas are labeled Antenna A, Antenna B, Antenna C and Antenna D from left to right, respectively. Similarly, the labels of tags from left to right are set from Tag 0 to Tag 8, respectively.

![](images/4e98e42f6bc4098a9e6cf8208e546c3fbfde024f5e6307c2e667185265a3e7cf.jpg)



Fig. 4. Experiment Scene

Besides the implemented RFID part, another important device required in the RollCaller system is a smart phone equipped accelerometer and magnetometer. We select HTC One to play this role. In our experiments, we choose a simple frequency-based model [15] for the smart phone to measure the displacement of the user when walking. In this model, the step length of the user $L_{step}$ is calculated by $L_{step} = a \cdot f + b$ , where f is the walking frequency of the user and the parameter a and b are trained off-line before our experiment for each person.

The last point we mentioned here is about the data we measured for ground truth in this paper. To make things simpler, the position of an object (reader antenna, tag or human) is measured as the central point of that object. Specially, middle point of a human's shoes is regarded as his central point.

# B. Evaluation of Anchor Time Stamp

As the foundation, the performance of Anchor Time Stamp measurement will affect the whole RollCaller system. Therefore, before evaluating the performance of other aspects in RollCaller system, we should first evaluate the accuracy and stability of the Anchor Time Stamp.

Distance drift is the most important metric used to evaluate the performance of Anchor Time Stamp measurement. The distance drift of an Anchor Time Stamp is set as the distance between the expected position and the actual position where the Anchor Time Stamp is measured. With smaller distance drift, the measurement of Anchor Time Stamp is more accurate.

1) Accuracy of Anchor Time Stamp: First of all, we evaluate the accuracy of Anchor Time Stamp measurement using general settings. In this experiment, all the reader antennas but the Antenna A are turned off, and all the tags but Tag 1 are removed from the identifying range of Antenna A. The connection of Antenna A and Tag 1 is perpendicular to the passage. A human walks through the passage for 35 times with normal velocity. Each time the system detects an Anchor Time Stamp, he stops and measures the distance from his position to the line of sight between the antenna and the tag as the distance drift.

The statistical analysis of these 35 times of Anchor Time Stamp measurement is shown in Figure 5. From the CDF curve, we can figure out that 80% of the Anchor Time Stamps are measured within a 25cm distance drift. This is a tolerable error when applying the Anchor Time Stamp in real application. In fact, the thickness of a human can normally be greater than 20cm, which makes the distance drift of our Anchor Time Stamp measurement more negligible. Besides, the bars of PDF shown in Figure 5 further illustrate that most of the distance drift is concentrated in the interval of 10cm to 25cm. This means the extreme case of error occurs rarely, which makes the Anchor Time Stamp measurement more trustworthy.

![](images/75adb290a6cc79ca4cae526d003f376ea68674f05ae108fbc57b011d49f89734.jpg)



Fig. 5. Anchor Time Stamp Measurement

![](images/3b6cdb1693f9a5ae71b7f86f75acd993eead81e2dde5e62a03c615c154438eb5.jpg)



Fig. 6. Doppler Frequency Shift Data

![](images/3ddcd6b8d72e2ccf603dfa2b480a0075778ac3a41642a13ccf5707b3f9b4fcbd.jpg)



Fig. 7. Distance Drift

2) Impact of Human Velocity: When considering the Doppler frequency shift, velocity of the mobile item (receiver or transmitter) is the first concerned factor. In our RollCaller system, the human walking through the passage plays this roll. Therefore, in the first experiment, we evaluate the impact of the human velocity. The settings in this experiment are the same to the last experiment.

The bars in Figure 6 shows the maximum values of Doppler frequency shift measured when the human walks through the passage with velocity from 0.8m/s to 1.5m/s. This velocity range corresponds to the velocity from wandering to fast walking. This figure illustrates that the maximum values of Doppler frequency shift remain stable during the variation velocity. This is not surprising due to the inconspicuous velocity changes limited by human walking velocity. But the more direct reason is considered as the special cause of the Doppler frequency shift in our RollCaller system: the maximum values of the Doppler frequency shift is calculated by phase-difference method resulting from the obstruction of the main path signal. In this case, the moving human only acts as an obstacle and the velocity does not affect the initial and terminal phase of measured packets for maximum value significantly. Therefore, the velocity of the human can only have an ignorable effect on the Doppler frequency shift.

However, it does not mean that the velocity of the walking human is totally unprevailing in our RollCaller system. The curve in Figure 6 informs that with a faster velocity, the sample points collected for Anchor Time Stamp measurement are fewer. This results from the duration which the human obstructs the line of sight of tag and reader. Since the Anchor Time Stamp is calculated as the mean value of these sample points, it will necessary affect the accuracy of the Anchor Time Stamp. Figure 7 shows the statistical data of the measured distance drift with variant human velocity. The distance drift keeps growing when the human walks faster. This can be accused to the few sample points used for calculation. With fewer sample points, it is more likely to set the Anchor Time Stamp to the beginning or ending of the obstruction, but not the line of sight point.

3) Impact of Tag Status: In this part of section, we evaluate the impact of two factors caused by the deployment of tag and reader antenna.

Attached items on the shelves are always placed irregularly, which makes the direction of the tags are unpredictable. Therefore, we should evaluate the Anchor Time Stamp measurement to find whether our method still does well with various tag directions. Figure 9 shows the impact of the tag direction. In this experiment, the tag rotates along its central axis by angles $45^{\circ}$ , $0^{\circ}$ and $-45^{\circ}$ . From this figure, we can say that the rotation of the tag has a very slight effect on the Anchor Time Stamp measurement. Hence, this Anchor Time Stamp measurement approach can be adopted to the situation with irregular tag placement.

The angle between the tag-antenna connection and the passage (shortly tag-antenna angle) is another influent factor that can affect the accuracy of Anchor Time Stamp measurement. Figure 10 shows the relation between this angle and the distance drift of Anchor Time Stamp measurement. Although the distance drift is still in acceptable range, it is increasing when the tag-antenna angle grows. This can be imputed to the transmitting range of the directional reader antenna. The transmitting range of directional reader antenna can be described as a fusiform main lobe and several side lobes, where tags can receive and backscatter stronger carrier signal in the main lobe. When the tags are placed close to the edge of the main lobe, or outside the main lobe, the line of sight signal is not as strong as we wish, Therefore, it result for an larger distance drift in Anchor Time Stamp measurement.

# C. Performance of Reader Antenna Relation Map Generation

The reader antenna relation map generated in antenna allocation period plays an important role in our RollCaller system. The accuracy of this map can strongly affect the performance of our user navigation service. In this part of section, we evaluate the performance of the generated relation map.

In Equation 3, the parameter $\gamma$ is still undetermined. In this evaluation section, we design an experiment to estimate this parameter by statistical analysis. In this experiment, all the reader antennas but the antenna A and B are turned off. And all the tags but tag 1 are removed. In this situation, our system can only receive backscattered signal from tag 1 by antenna A and B. Tag 1 is facing the middle point of antenna A and B, and the distance between these two antennas is 40cm. During this experiment, 100 times of walking behaviors passing the passage are recorded. The displacement of the human is measured using the carried smart phone.

Figure 8 shows the results of these 100 times of tests. This PDF bars show that more than 90% of these tests have results in the interval of 0.1m to 0.4m, and about 40% are among 0.2m to 0.3m. The mean value of these 100 tests are 0.2137.

![](images/d193f72b927d34a11cb70cfb2852fdfbdbe8bc1b5ba0e036267337931566ba16.jpg)



![](images/724df84a6c109ee200f0d2491b99da252b0940f075e48ecd704a769f0f186391.jpg)



![](images/5a94e7e3383ab3018eb2811fa00164c8afa241e89890ada4055d0a2a41188e85.jpg)



Fig. 10. Impact of Tag-Antenna Angle

Fig. 8. Measured Distance between Two Reader Antennas
Fig. 9. Impact of Tag Self-Rotation Angle   
![](images/21c19b2da6a35de9c90fadb3f3005d0e9f78192b71297de0be810d6e494e74e7.jpg)



Fig. 11. Reader Antenna Map Generation

Therefore, we apply the value of $\gamma$ as 0.2137/0.4 = 0.5343 in our evaluation of relation map generation and further experiments of our RollCaller system.

We can see from Figure 8 that there exists the situation that the measured antenna distance has a negative value. This is reasonable because Antenna A has a possibility to detect the Anchor Time Stamp later than Antenna B does due to the distance drift of Anchor Time Stamp measurement.

After achieving the $\gamma$ value, we can now evaluate the accuracy of our generated reader antenna relation map. This time the reader antennas and tags are all on working. The reader antennas are placed with a distance of 40cm to their neighboring antennas, and the tags are placed in a distance of 20cm to their neighboring tags. Figure 11 shows the result of our relation map generation. The ground truth is that Antenna A/B/C/D are placed in a line where each two neighboring antennas are separated in a distance of 40cm. In our relation map generation process, the initial relative position of these antennas to their neighboring antennas are all set as 0cm. When a human moves from one end to another end of the passage, the system calculates the relative positions of antennas using the recorded Anchor Time Stamps and the measured displacement of human uploaded from the smart phone. In this experiment, the relative position of these four antennas to Antenna A is calculated as 0cm, 21.7cm, 52.4cm and 97.3cm. The relation map keeps updating and when the times of passing the passage increases to 10, the relative position is estimated as 37.3cm, 73.5cm and 111.9cm, where the relative distance between two neighboring antennas is measured as 37.3cm, 36.2cm and 38.4cm. That means, after 10 times of passing the passage, the relation map can reach a measurement error less than 5cm, which is very low.

# D. Performance of User Navigation Service

With stable Anchor Time Stamp measurement and accurate reader antenna relation map generation, we can finally evaluate

![](images/d38596cb9b4c67452ac9eea2c9b6ee13dd3a712d836f6be384cbff2094e97d35.jpg)



Fig. 12. Stop Points of Navigation Service

the user navigation service of the RollCaller system. In this experiment, 7 tags and all the 4 reader antennas are used. Among these 7 tags, Tag 0 is assigned to act as the reference tag, which is mentioned in Section IV-C. Antennas A/B/C/D are placed in line with distance 40cm to their neighboring antenna. Tags are also placed in line with 20cm to each neighboring tag. The relation map of reader antennas is generated and the human walks from the end of the passage with reference tag to the other end.

This navigation experiment performs 120 times. For Tag 1 to Tag 6, each tag is searched for 20 times. When the RollCaller system judges that the human is right next to the tag he is searching, it announces the user. Then the user stops and the stop point is marked. These 120 marked points are plotted in Figure 12. Notice that the vertical difference in Figure 12 it only used to separate the marks for searching different tags, but not represent the walking trace closer to tags or antennas. From Figure 12, we can tell that most of the stop points are near the searching tag. The closer to the tag, the higher density of stop points. Figure 13 further analyzes the performance of the user navigation service. In this figure, we can find that the average of the stop points has a nearly perfect position. Besides nearly 90% stop points are located less than 20cm to the real position of the searching tag. This means our RollCaller can navigate the user well to the tag he wants.

Even though the evaluation shows an impressive result of our RollCaller system, we can still find that, for searching tags further to the reference tag, the navigation result is worse, results for the maximum navigation error with near 40cm when searching T 6. The reason leads to this result is that the IMU-based displacement measurement performs worse for longer distance due to accumulated error. Despite of this defect, the navigation result still has profound significance.

![](images/6eab9af673d3a57de57531e4b803f86ef8f12f88638d48ebd7964f674103471e.jpg)



Fig. 13. Statistic Analysis on Navigation Error

# VI. RELATED WORK

Two major types of localization approaches are applied in RFID-based localization systems: tagged approaches [16]–[19] and tag-free approaches [20], [21]. In tagged approaches, the object which requires a localization service is attached with an RFID tag. To localize this object, the reader fetches the valuable attributes from the signal transmitted or backscattered from the RFID tag on the object. These attributes include the carried tag information and other physical aspects such as received signal strength (RSS) and phase. According to the utilized attribute, the localization accuracy varies from room-level to centimeter-level. Even though tagged approaches can achieve an impressive localization accuracy, it is not suitable in the scenarios we stated in Section II since it cannot provide the human-item spatial relation.

Tag-free approaches provide another way to achieve the goal of localization. In tag-free approaches, the tags are no longer attached on the object waiting for localization, but distributed in the environment. Applying tag-free approaches, the object that requires localization service no longer needs to be recognized before localization. This advantage enables the tag-free approaches to be installed in some condition that is impossible to attach the RFID tag on the object to be identified, such as halls. This kind of approaches seem adoptable to the scenarios we stated in Section II, but existing tag-free approaches do not satisfy our demand in these scenarios because the localization accuracy of tag-free approaches in RFID-based localization, especially in passive RFID systems, is too low. This is why tag-free approaches in RFID systems are more likely to be used as intrusion detection or trajectory discovery. What was worse, if we use location fingerprint in our localization approaches $[22]$ , $[23]$ , it suffers a lot since the tags in these scenarios are always moved by people. It is hardly to achieve and maintain a stable and reliable location fingerprint database in such a scenario.

# VII. CONCLUSION

In this paper, we design a user-friendly indoor navigation system, called RollCaller, to solve the problem of searching specific items among large amount of distinguished items on shelves. We propose a novel approach using Doppler frequency shift to measure the human-item spatial relation and apply this approach in RollCaller system. Using this human-item spatial relation measuring approach and the generated reader antenna relation map, RollCaller system can accurately navigate a user to the item he wants. Experiment results show that our RollCaller system can accurately navigate user to the item he wants with an average distance error less than 20cm.

# VIII. ACKNOWLEDGEMENT

This work is supported in part by the NSF China Major Program under grant No. 61190110, the National High-Tech R&D Program of China (863) under grant No. 2011AA010100, the National Basic Research Program of China (973) under grant No. 2012CB316200, the NSFC\RGC Joint Research Scheme under grant No. 61361166009, and the RFDP under grant No. 20121018430. We also acknowledge the support from the codes of USRP2reader from the Open RFID Lab (ORL) project [25].

# REFERENCES

[1] J. Zhou, L. Hu and et al, “An efficient multidimensional fusion algorithm for iot data based on partitioning,” IEEE Tsinghua Science and Technology, 2013.   
[2] Y. Liu, Q. Zhang and et al, "Opportunity-based topology control in wireless sensor networks," IEEE Transactions on Parallel and Distributed Systems, 2010.   
[3] Y. Tong, L. Chen and B. Ding, “Discovering threshold-based frequent closed itemsets over probabilistic data,” in Proc. of IEEE ICDE, 2012.   
[4] Y. Zheng and M. Li, “Fast tag searching protocol for large-scale rfid systems,” IEEE/ACM Transactions on Networking, 2013.   
[5] Y. Zheng and M. Li, “Pet: probabilistic estimating tree for large-scale rfid estimation,” IEEE Transactions on Mobile Computing, 2012.   
[6] L. Xie, B. Sheng, and et al, “Efficient tag identification in mobile rfid systems,” in Proc. of IEEE INFOCOM, 2013.   
[7] B. Sheng, C. C. Tan, and et al, “Finding popular categories for rfid tags,” in Proc. of ACM MobiHoc, 2008.   
[8] Y. Qiao, S. Chen, and et al, “Energy-efficient polling protocols in rfid systems,” in Proc. of ACM MobiHoc, 2011.   
[9] L. Yang, J. Han, and et al, “Season: shelving interference and joint identification in large-scale rfid systems,” in Proc. of IEEE INFOCOM, 2011.   
[10] L. Yang, J. Han, and et al, “Identification-free batch authentication for rfid tags,” in Proc. of IEEE ICNP, 2010.   
[11] D. M. Dobkin, “The rf in rfid: passive uhf rfid in practice,” 2008.   
[12] F. Li, C. Zhao, and et al, “A reliable and accurate indoor localization method using phone inertial sensors,” in Proc. of ACM Ubicomp, 2012.   
[13] A. Rai, K. K. Chintalapudi, and et al, “Zee: zero-effort crowdsourcing for indoor localization,” in Proc. of ACM Mobicom, 2012.   
[14] G. Shen, Z. Chen, and et al, “Walkie-markie: indoor pathway mapping made easy,” in Proc. of USENIX NSDI, 2013.   
[15] D. Cho, M. Mun, and et al, "Autogait: a mobile platform that accurately estimates the distance walked," in Proc. of IEEE PerCom, 2010.   
[16] L. M. Ni, Y. Liu, and et al, “Landmarc: indoor location sensing using active rfid,” ACM Wireless Networks, 2004.   
[17] C. Hekimian-Williams, B. Grant, and et al, “Accurate localization of rfid tags using phase difference,” in Proc. of IEEE RFID, 2010.   
[18] P. V. Nikitin, R. Martinez, and et al., "Phase based spatial identification of uhf rfid tags," in Proc. of IEEE RFID, 2010.   
[19] S. Azzouzi, M. Cremer, and et al., “New measurement results for the localization of uhf rfid transponders using an angle of arrival (aoa) approach,” in Proc. IEEE RFID, 2011.   
[20] Y. Liu, Y. Zhao, and et al, “Mining frequent trajectory patterns for activity monitoring using radio frequency tag arrays,” IEEE Transactions on Parallel and Distributed Systems, 2012.   
[21] D. Zhang, J. Zhou, and et al, T. Li, “Tasa: tag-free activity sensing using rfid tag arrays,” IEEE Transactions on Parallel and Distributed Systems, 2011.   
[22] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in Proc. of ACM Mobicom, 2012   
[23] J. Wang and D. Katabi, “Dude, where’s my card? rfid positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[24] P. Robertson, M. Angermann, and B. Krach, “Simultaneous localization and mapping for pedestrians using only foot-mounted inertial sensors,” in Proc. of ACM Ubicomp, 2009.   
[25] “Open RFID Lab”, http://pdcc.ntu.edu.sg/wands/ORL