# Full-Dimension Relative Positioning for RFID-Enabled Self-Checkout Services

CHUNHUI DUAN, School of Software, Tsinghua University, China and School of Computer Science and Technology, Beijing Institute of Technology, China

JIAJUN LIU, School of Software, Tsinghua University, China

XUAN DING, School of Software, Tsinghua University, China

ZHENHUA LI , School of Software, Tsinghua University, China

YUNHAO LIU, School of Software, Tsinghua University, China

Self-checkout services in today’s retail stores are well received as they set free the labor force of cashiers and shorten conventional checkout lines. However, existing self-checkout options either require customers to scan items one by one, which is troublesome and ine!cient, or rely on deployments of massive sensors and cameras together with complex tracking algorithms. On the other hand, RFID-based item-level tagging in retail o"ers an extraordinary opportunity to enhance current checkout experiences. In this work, we propose Taggo, a lightweight and e!cient self-checkout schema utilizing well-deployed RFIDs. Taggo attaches a few anchor tags on the four upper edges of each shopping cart, so as to #gure out which cart each item belongs to, through relative positioning among the tagged items and anchor tags without knowing their absolute positions. Speci#cally, a full-dimension ordering technique is devised to accurately determine the order of tags in each dimension, as well as to address the negative impacts from imperfect measurements in indoor surroundings. Besides, we design a holistic classifying solution based on probabilistic modeling to map each item to the correct cart that carries it. We have implemented Taggo with commercial RFID devices and evaluated it extensively in our lab environment. On average, Taggo achieves 90% ordering accuracy in real-time, eventually producing 95% classifying accuracy.

CCS Concepts: • Networks → Location based services; Mobile networks; • Human-centered computing → Ubiquitous and mobile computing.

Additional Key Words and Phrases: RFID, relative positioning, self-checkout

# ACM Reference Format:

Chunhui Duan, Jiajun Liu, Xuan Ding, Zhenhua Li, and Yunhao Liu. 2021. Full-Dimension Relative Positioning for RFID-Enabled Self-Checkout Services. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 5, 1, Article 7 (March 2021), 23 pages. https://doi.org/10.1145/3448094

∗Corresponding author

Authors’ addresses: Chunhui Duan, duanch09@gmail.com, School of Software, Tsinghua University, Beijing, China, School of Computer Science and Technology, Beijing Institute of Technology, Beijing, China; Jiajun Liu, jj-liu16@mails.tsinghua.edu.cn, School of Software, Tsinghua University, Beijing, China; Xuan Ding, School of Software, Tsinghua University, Beijing, China, dingxuan@tsinghua.edu.cn; Zhenhua Li, School of Software, Tsinghua University, Beijing, China, lizhenhua1983@tsinghua.edu.cn; Yunhao Liu, School of Software, Tsinghua University, Beijing, China, yunhao@tsinghua.edu.cn.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for pro#t or commercial advantage and that copies bear this notice and the full citation on the #rst page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior speci#c permission and/or a fee. Request permissions from permissions@acm.org.

© 2021 Association for Computing Machinery.

2474-9567/2021/3-ART7 \$15.00

https://doi.org/10.1145/3448094

# 1 INTRODUCTION

# 1.1 Background and Motivation

The concept of checkout-free or self-checkout shopping has swept the retail market in the past few years [3, 31]. It opens up a frictionless retail experience where customers no longer have to spend too much time waiting in a long checkout line during peak hours even for a bottle of water. It is also attractive to store owners because the labor costs for cashiering can thus be greatly saved. Furthermore, self-checkout service provides a bit of extra privacy – no sta" directly sees what or how much the customer is buying. Such unique advantages draw much attention from researchers and a range of checkout-free options have been explored, from self-scanning items via a smartphone, to more complex solutions that use sensors and cameras to track shoppers’ and goods’ movements in the store. However, the former requires shoppers to scan the barcode on each item one by one, which is still time-consuming, while the latter relies on the deployment of a great many high-cost devices.

We turn our attention to the Radio Frequency Identi#cation (RFID) technology that has progressed to a remarkable state recently with broad applications in everyday life, such as product monitoring, goods tracking and item identi#cation [20, 34, 40]. As a key enabler of automatic identi#cation technology, RFID o"ers an appealing alternative when compared against traditional barcodes, given the merits of non-contact communication, reading ability of fast-moving objects and multiple objects, larger data storage capacity, etc. Recent years have also witnessed the cost of RFID tags be brought down dramatically from several dollars to one tenth of a dollar. In a number of today’s bookstores and supermarkets, items have already been attached with passive RFID tags for identi#cation [5, 6]. We believe or envision that RFID would facilitate existing barcode-based services in the near future.

To enable automatic checkout, there are some existing demonstrations that let consumers move the shopping carts into a specialized RFID gateway [4], or walk the bag of products to buy through a pre-installed channel [6]. Nevertheless, such schema requires customized hardware e"orts, and thus is inconvenient to generalize, let alone the considerable costs. Another feasible solution is to localize tags with a #ne granularity – if we can obtain all tags’ absolute positions precisely, the shopping carts they belong to could then be inferred. Unfortunately, accurate tag localization in itself is a challenging task, and state-of-the-art methods [33, 34, 40] require dedicated devices (like USRP) or relatively large deployment costs (for reference tags and antennas) in order to achieve high precision.

# 1.2 Our Schema

In this work, we introduce Taggo, a lightweight and e!cient self-checkout schema. Di"erent from the abovementioned attempts, we try to o"er a more generic option with purely commercial o"-the-shelf (COTS) devices. As shown in Fig. 1, a conveyor belt is deployed in the checkout region, moving at a uniform speed to propel the shopping carts of users. Items inside the carts are the products consumers would like to buy, while those outside on the belt are unwanted ones dropped by consumers. In terms of deployment cost, Taggo only adopts two properly arranged RFID antennas connecting to the same reader. In terms of working e!ciency, Taggo wants to allow multiple users to check out simultaneously. In other words, there could be several shopping carts on the belt at the same time, placed in either a back-to-back or a side-by-side manner. Then, it is crucial to determine which cart an item belongs to.

Taggo resolves the checkout problem through relative positioning among RFID tags, which is an emerging technique put forward in recent years [22, 30]. Concretely, we attach a few anchor tags on the front, back, left, and right edges of each shopping cart. To determine whether one tagged object belongs to a speci#c cart, Taggo tries to get the relative location (or says the order) of this tagged object with respect to the anchor tags without knowing their absolute positions.

![](images/883c4a40ea26c634381cf7c16a609b97c1243b5fb49b1853a9b093a283aac565.jpg)



Fig. 1. Architectural overview of Taggo. Shopping carts are propelled by a conveyor belt moving at a uniform speed. We establish the coordinate system regarding the plane of the conveyor with the X-axis parallel to the moving direction. Each item is a!ached with a passive RFID tag, and anchor tags are deployed on the four surrounding (i.e. front, back, le", and right) edges of each cart.

# 1.3 Challenges and Solutions

Putting this idea into practice, the challenges we face are mainly the following folds. First, state-of-the-art studies in the relative positioning domain [22, 30] mainly focus on the ordering of tags in one dimension, which apparently cannot meet the needs in our checkout scene. As a user-friendly schema, Taggo should not have restrictions on the displacement of users’ shopping carts. In other words, di"erent carts may not be placed in a strictly sequential way along the moving direction of the conveyor. Therefore, to infer which cart an item belongs to without ambiguity, we need to perform full-dimension relative positioning along both X- and Y- axes. Second, for ordering purposes, previous work [30] uses Dynamic Time Warping (DTW) algorithm to #nd the “V-zone” in a tag’s phase sequence, which is costly in both time and space. To meet the real-time checkout demand, we wish to reduce the time complexity as much as possible. DTW also requires a reference phase pro#le generated with a known tag layout as input, which is di!cult to obtain in our scenario. Third, the RF phase is a sensitive metric that is easily a"ected by the environment. A more robust approach is in need to further reinforce the ordering accuracy. Fourth, even with the above considerations, the ordering results among tags would still contain more or less unanticipated errors, which had better be alleviated.

To address these challenges, we #rst develop a fast V-zone extraction method for tag ordering along Xdimension, which is time-e!cient for its only one run of scanning the whole phase sequence. Then, we propose the concept of overall phase changing rate and leverage it to order tags along Y-dimension. Theoretical analyses are given to demonstrate its feasibility (more details will be presented in Section 5). Besides, to combat indoor ambient noise, we #gure out an e"ective solution which combines the measurements of two antennas and utilizes their relative value to mitigate the e"ect of imperfect signals. Finally, to correctly determine each tag’s host (i.e. the real cart that carries the target tag), we design a holistic item classifying mechanism by incorporating a probabilistic model. The eventual classifying accuracy can then be further enhanced.

# 1.4 Contributions

This paper presents a comprehensive study of RFID-enabled self-checkout services. Speci#cally, it makes the following contributions.

• We propose a full-dimension relative positioning schema to essentially improve today’s checkout-free experi ences (particularly in retail stores). It works based on the phase information acquired from deployed RFIDs, and the accompanying challenges are comprehensively analyzed.   
• We design a series of algorithms to accurately determine the tag order in each dimension, as well as to overcome the negative impacts from imperfect measurements, with a"ordable computation overhead.   
• We present a holistic item classifying solution based on probabilistic modeling to map each item to the correct cart that carries it, which can tolerate tag ordering errors to a great extent.   
• We implement a prototype system for Taggo with COTS RFID devices and evaluate its performance with extensive experiments. The average ordering and classifying accuracies reach as high as 90% and 95%, which are su!cient for most practical applications.

Roadmap. The rest of the paper is organized as follows. The main design of Taggo is overviewed in Section 3. We introduce the technical details of the tag ordering algorithms along both X- and Y-dimensions in Section 4 and Section 5. The item classifying method of Taggo is elaborated in Section 6. More feasible solutions to enhance Taggo’s applicability are presented in Section 7. We describe the implementation and evaluation of our system in Section 8. We review related work in Section 2, and #nally conclude this paper in Section 9.

# 2 RELATED WORK

We brie%y review the related literature in this section.

# 2.1 RF-based Localization

Localization problem has been well studied in the RFID #eld, which can be mainly categorized into absolute positioning and relative positioning.

Absolute positioning: Early attempts try to use the RSSI information as #ngerprint or distance metric for acquiring location information [9, 25, 26, 32, 41, 43]. LandMarc [25] #rst employs the idea of reference tags with #xed locations to help infer a target tag’s location. There are also growing interests in exploiting phase measurements to locate tags. Angle of Arrival (AoA) is a typical solution, which works by measuring the phase di"erence between the received signals at di"erent antennas [7, 8, 20, 33, 35]. PinPoint [18] proposes a novel algorithm that accurately computes the angle of arrival, allowing multiple collaborating access points to localize interfering transmitters on the order of centimeters even under strong multi-path propagations. The concept of Synthetic Aperture Radar (SAR), which is #rst used in military radar systems, is also borrowed to the wireless localization domain in recent years [19, 20, 23, 28, 42]. PinIt [34] leverages the SAR technique to extract the multipath pro#le of RFID tags for tag localization in non-line-of-sight scenarios. Other approaches try to incorporate di"erent mathematic models to infer the target’s location [12, 16, 24, 39]. Tagoram [40] presents the concept of hologram, which successfully handles the thermal noise and device diversity and realizes real-time tracking with high precision in a 2D plane.

Relative positioning: In addition to the absolute location, relative locations among a set of objects are also important in many applications. As pioneer work in RFID-based relative positioning area, OTrack [29] #gures out the order of luggage on the conveyor belt using RSSI trends of tags. However, RSSI can not be considered as a reliable metric because it is seriously a"ected by the indoor multi-path e"ect, and thus hard to achieve high accuracy. Another standard work in relative positioning is STPP [30], which proposes the concept of V-zone in the phase pro#le and utilizes it to infer the order of tags. However, it uses the DTW algorithm to extract V-zone from the phase sequence, which is time-consuming, and to apply DTW, it needs to generate a reference phase pro#le beforehand with known tag layout, which is hard to achieve in many practical scenarios. The authors in [22] incorporate a dedicated robot to localize the order of books and detect lying-down books in the library. It still focuses on relative positioning along one dimension.

![](images/5867e47929720b1b1d3b78290e9ffee150e3a8a5d6bbba83c0f668f828b936cc.jpg)



Fig. 2. Workflow overview of Taggo

Our work is inspired by the above works that leverage the RF phase for localization purposes. Although some state-of-the-arts could demonstrate quite small error margins such as [40] and [35], they require dedicated devices (like USRP) or massive deployment costs (for reference tags or antennas) in order to achieve high precision. Other ones demand extra information as a priori, including the moving speed of a conveyor ([10]), the relative trajectory of a tag ([28]), or the locations of several antennas ([27]), to generate an (inverse) synthetic aperture that is necessary for localization purposes. However, in our work, centered around the self-checkout context, we aim to provide a more lightweight and e!cient schema that is capable of acquiring the order of tags with neither the need to know their absolute locations nor requiring too much prior knowledge.

# 2.2 Intelligent Self-Checkout Studies

Early researchers in [44] introduce a new form of supermarkets: smart markets, in which customers can acquire detailed product information with easy access and expedite the checkout process without human intervention. A POS (Point of Sale) zone with a shielding door is designed. Each time one user with a shopping cart enters the POS zone, inside which an RFID reader starts to read RFID tags attached to items in the shopping cart.

Recently, the rapid development of computer vision technology facilitates new kinds of self-checkout systems. [38] proposes an intelligent system embedded with a single camera to detect multiple products without any labels (barcodes, RFID tags, or QR codes) in real-time performance. To achieve this, deep learning skill is applied, and data mining techniques construct the image database employed as the training dataset. The authors in [36] analyze the “Just Walk-Out” technology in Amazon Go.With sensors and cameras placed all around the surveillance region, the system can keep track of the products in a virtual cart for each user by utilizing amalgamative technologies of deep learning, computer vision, and sensor fusion.

# 3 OVERVIEW OF TAGGO

This section brie%y describes the work%ow of Taggo. As demonstrated in Fig. 1, there is one conveyor belt that could carry multiple users’ shopping carts. Di"erent carts may be placed in a back-to-back (i.e., along X-dimension) or side-by-side (i.e., along Y-dimension) manner, and people can also drop the goods they decide not to buy at the last minute onto the belt (of course, outside the carts). There are two types of tags, i.e., anchor tags which are attached on four surrounding edges of each cart to represent the cart, and item tags which are attached to the goods for identi#cation purpose. Taggo decomposes the self-checkout problem into relative positioning among tags inside the carts, tags outside the carts, and anchor tags on the carts, in order to #nally separate those goods that need to be checked out with regard to a speci#c cart/customer. Without loss of generality, we establish the coordinate system with regard to the plane of the conveyor, and assume the tags/conveyor move(s) along X-axis (i.e., X-dimension) from left to right in our scene. Taggo deploys two reader antennas at each side of the conveyor to read the tags. Its infrastructure also includes a central server which stores system parameters (e.g. locations of antennas, IDs of the anchor tags), as well as runs the relative positioning algorithms. To accomplish the goal of automatic checkout, Taggo goes through the following steps at a high level:

![](images/b4077ba4097ae0993601178129489a68360afe574b0814ebb173b8c7da42d001.jpg)



Fig. 3. Relationship of tag and antenna. Tag’s distance to the antenna first increases and then decreases.

• Step 1: Data collection. We #rst collect phase data of all the tags (including item tags and anchor tags) with the deployed RFID devices.   
• Step 2: Tag ordering along X-dimension. With each tag’s phase pro#le, we detect the V-zone with a lightweight method described in Section 4. Then we order tags according to the time when their bottom points in the detected V-zones occur.   
• Step 3: Tag ordering along Y-dimension. For each tag, we compute an overall relative phase changing rate as proposed in Section 5. Then we order tags according to the computed rate.   
• Step 4: Item-cart association. For every item tag, we select a few candidate carts with the ordering result along X-dimension in Step 2. Further by combining results in Step 3, we assign a possibility to each candidate cart, which describes how likely it carries the item tag. Finally, the item tag is associated with (or classi#ed to) the cart with the highest possibility.

The whole procedure is summarized in Fig. 2. We will elaborate on the technical details of the above steps in the next few sections.

# 4 ORDERING ALONG X-DIMENSION

In this section, we #rst introduce some preliminary knowledge on relative positioning, and then describe how Taggo works to obtain the order of tags along X-dimension.

# 4.1 V-zone Pa!ern of Phase Sequence

The RF phase is a basic attribute of a signal and can be reported by commercial RFID readers [11]. Let 𝑑 be the distance between a pair of tag and antenna. Since the signal traverses a total distance of 2𝑑 in backscatter communication, the phase rotation output by the reader can be expressed as [15]:

$$
\theta = \left(\frac {2 \pi}{\lambda} \times 2 d + \mu\right) \bmod 2 \pi \tag {1}
$$

where 𝜆 is the wavelength, and the term 𝜇 describes the constant phase shift caused by the device’s hardware characteristics.

As Fig. 3 illustrates, when a tagged item moves with the conveyor belt along X-dimension, its distance to the reader increases at #rst until the reader is right above the tag (when $A L _ { 2 }$ is perpendicular to $L _ { 1 } L _ { 2 } )$ , then decreases.

![](images/251ac77c71ed31b920847ef9a5126ba8c842fbe062fefb556d1c63cc8bd3f9be.jpg)



(a) Original phase sequence

![](images/0a08a7d02e0c0a0438ee1f9a1cd48b275457cf1c1f35f2ff3479f423f5a25aa4.jpg)



(b) Sliding window

![](images/735511bce6de1289cb876238a677d2f97b8f38018d05478ee8f3dc79d73b4eae.jpg)



(c) Smoothed phase sequence   
Fig. 4. V-zone pa!ern of phase profile. (a) An example of the collected phase sequence, which contains a “V-zone” pa!ern. (b) We search the phase profile using a sliding window. (c) We smooth the original phase sequence by splicing adjacent split parts together.

According to Eqn. 1, the raw phase (without modulo operation) will also #rst descend to a valley and then go up. In practice, the measured phase value jumps when it approaches 0 or 2𝜋 due to the mod operation. Fig. 4(a) shows an example of the collected phase sequence in our experiment. As we can see, there exists a “V-zone” shaped like the alphabet “V” around the valley in the curve. And the bottom of the V-zone, exactly occurs at the time when the reader is closest to the tag. If the moving speed of the tag/conveyor is constant, the phase pro#le will be symmetric around the bottom point.

Once the V-zone is detected, we are able to tell which tag passes the antenna earlier and which passes later. Tags’ order can then be inferred.

# 4.2 Limitations of Prior Art

To extract the V-zone in a phase pro#le, prior work STPP [30] utilizes the Dynamic Time Warping (DTW) technique. A reference phase pro#le is pre-calculated and the measured phase pro#le is then matched against the reference one through DTW to #nd where the V-zone appears. However, DTW has the following two drawbacks. 1) It requires a reference phase pro#le, which is generated by knowing the layout of tags and reader, and the moving speed of the reader. But in our situation, it is not feasible to assume such prior knowledge when our goal is to #gure out the layout of tags. 2) DTW is time-consuming just to search for a V-zone. In STPP, time complexity reaches $\begin{array} { r } { O ( \frac { N M } { w ^ { 2 } } ) } \end{array}$ , where 𝑁 and 𝑀 are lengths of reference and measured phase pro#le, while 𝑤 is the length of segment divided into for calculation. 𝑤 should not be large as a bigger 𝑤 will cause loss of information in phase pro#le and reduce the accuracy.

Therefore, to deal with the above limitations and meet the real-time demand in self-service applications, here in this work, we aim to propose a more practical and e!cient V-zone detection approach.

# 4.3 Fast V-zone Detection

How to detect the #xed pattern V-zone in an acquired phase pro#le with high accuracy and e!ciency is a critical task in relative localization. Recall prior work STPP [30], since it moves the reader manually to interrogate the tags, the corresponding phase pro#le will be stretched because of the unstable moving speed of the reader. That is also the reason why it utilizes DTW to detect a V-zone. Here in our scenario, since we use a uniformly moving conveyor to transport shopping carts and items, the stretch and compression of the phase pro#le can be negligible. Looking back at Fig. 4(a), we have the following key observation.

Observation 4.1. If a V-zone appears in a phase pro"le, because of modulo operation, the phase values on the two edges of the V-zone approach 2𝜋, which means a jump from 0 to 2𝜋 (or 2𝜋 to 0) must have happened at such edge point and its adjacent point. And within the whole V-zone, there are no other jumping points except the two edges.

Motivated by the above observation, to detect a V-zone, we only need to detect the jumping points in phase pro#le and then check whether the section between two adjacent jumping points conforms to the feature of V-zone.

As we know, the RF phase is a sensitive metric whose value is easily a"ected by surrounding environment. Thus, as a preprocessing process, we #rst put a median #lter on the raw phase sequence to eliminate noisy points while preserving the lowest point in V-zone. Denote the #ltered phase sequence as $\Theta = \{ \theta _ { 1 } , \theta _ { 2 } , \dots , \theta _ { N } \}$ . We use a sliding window 𝑤 $( w \subset \Theta )$ to search from the beginning of Θ. Inside the window, if either of the following conditions is satis#ed, we consider 𝑤 as a jumping window:

$$
\max (w) - \min (w) > \eta \quad \text { or }
$$

$$
\left| \text { last } (w) - \text { first } \left(w _ {\text { next }}\right) \right| > \eta \tag {2}
$$

where functions 𝑓 𝑖𝑟𝑠𝑡 () and 𝑙𝑎𝑠𝑡 () de#ne the #rst and last element of 𝑤 respectively, $w _ { \mathrm { n e x t } }$ is the window right following 𝑤, and 𝜂 is a pre-de#ned threshold (we choose 𝜂 to be 𝜋 in our experimentation). Fig. 4(b) illustrates an example of sliding windows, we can easily #nd that inside a window or between windows there may exist a jump, and with the above two conditions such a jump can be detected.

Once we get all the jumping windows and corresponding jumping points inside, according to Observation 4.1, the sections between two consecutive jumping points become the candidates of V-zone. The next step is to #nd out the real V-zone from all the candidates. We observe when a tag is actually not passing through the antenna, its phase value normally goes up from 0 to 2𝜋 or down from 2𝜋 to 0 for a V-zone candidate, like section A and B in Fig. 4(a). Then we can #lter out these sections with their edge features. Suppose 𝑠 represents a candidate section. 𝑠 is determined as a V-zone if the following two conditions are both satis#ed:

$$
2 \pi - f i r s t (s) \leq \epsilon \quad \text { and }
$$

$$
2 \pi - \text { last } (s) \leq \epsilon \tag {3}
$$

Here 𝜖 is a user-de#ned small threshold. These conditions ensure that the two edges of the section approach 2𝜋 and there is no sharp jump from 0 to 2𝜋 or 2𝜋 to 0 during this section, which exactly suits the feature of a V-zone. Thus, when Eqn. 3 holds, we can con#dently state that the speci#c candidate section is a V-zone.

Based on the aforementioned principle, we can detect all the V-zones with only one run of scanning the whole phase sequence. To put it simply, when we slide the window 𝑤, we #rst check whether it is a jumping window according to Eqn. 2; then after attaining two consecutive jumping points we further check if the section between them satis#es the edge condition in Eqn. 3 to determine a V-zone. Through this procedure, we achieve a time complexity of 𝑂 (𝑁 ) and a space complexity of 𝑂 (1) for V-zone searching, which is a signi#cant improvement compared against the $\begin{array} { r } { O ( \frac { N \hat { M } } { w ^ { 2 } } ) } \end{array}$ time complexity (almost the square of 𝑁 ) in prior art [30]. This also ensures our approach to work in real-time for self-checkout scenarios.

# 5 ORDERING ALONG Y-DIMENSION

As we have no restriction on the placement of users’ shopping carts, di"erent carts may keep abreast with each other, which means they have similar or overlapped X-coordinates while varies in Y-dimension, as shown in Fig. 1. Therefore, in addition to the X-dimension, we also need to determine the order of tags along Y-dimension.

![](images/0e8fd93a1ee8839a5eebcd59bc077c6459e7e71bf1bf7ed889a2aff37a92bca6.jpg)



(a) One antenna scenario

![](images/00a3e2d8102a9c4bcb0dd848af83e2b65f5cb384dba7a4377b765c840a5a5d78.jpg)



(b) Two antenna scenario   
Fig. 5. Geometric relationship between tags and antenna(s). (a) The antenna is located at the origin (0, 0). The tag moves horizontally with speed 𝑣 from initial position $( x _ { 0 } , y _ { 0 } )$ . When a tag is closer to the antenna, it shall observe a larger velocity 𝑣 cos 𝛼 towards the antenna. (b) The coordinates of two antennas are $( 0 , Y _ { 1 } )$ and (0, 𝑌2) respectively. If tag 𝑗 is closer to antenna 1 than tag 𝑘 is, then we can easily infer tag 𝑗 is farther from antenna 2 than tag 𝑘 is.

# 5.1 Utilizing One Antenna

We begin to illustrate our design with one antenna adopted. The more complicated two-antenna approach is discussed in the following part.

As mentioned before, the measured phase sequence is split into many short discontinuous parts due to the mod operation. For better illustration, we #rst smooth the curve by splicing adjacent split sub-sequences together, through the following equation:

$$
\theta_ {i} = \left\{ \begin{array}{l l} \theta_ {i} - \lceil \frac {\left| \theta_ {i} - \theta_ {i - 1} \right|}{2 \pi} \rceil 2 \pi , & \text { if } \theta_ {i} - \theta_ {i - 1} > \eta \\ \theta_ {i} + \lceil \frac {\left| \theta_ {i} - \theta_ {i - 1} \right|}{2 \pi} \rceil 2 \pi , & \text { if } \theta_ {i - 1} - \theta_ {i} > \eta \\ \theta_ {i}, & \text { otherwise } \end{array} \right. \tag {4}
$$

where $i > 1 ,$ . Here the basic rationale is that if the di"erence between two adjacent phase values exceeds a big threshold 𝜂 $( e . g . , \eta = \pi )$ , we should compensate an integral multiple of 2𝜋 for the current value. An example of the smoothed curve is shown in Fig. 4(c).

We further compare phase pro#les of tags with di"erent Y-coordinates, and comes to the following observation:

Observation 5.1. When a tag is closer to the antenna in Y-dimension (or in other words, has a smaller Ycoordinate), its phase pro"le will show a faster changing rate on the whole.

This observation can be mathematically proven as below. For ease of description, suppose the antenna is located at (0, 0) in the coordinate system, as shown in Fig. 5(a). Let $\left( x _ { 0 } , y _ { 0 } \right)$ be the initial position of the tag, and 𝑣 be its moving speed. As the tag moves along X-axis, its X-coordinate 𝑥 (𝑡) equals 𝑥0 + 𝑣𝑡 at time 𝑡 while Y-coordinate 𝑦(𝑡) do not change over time, $i . e . , y ( t ) = y _ { 0 }$ . So the distance between the tag and antenna is $d = { \sqrt { x ^ { 2 } + y ^ { 2 } } } = { \sqrt { ( x _ { 0 } + v t ) ^ { 2 } + y _ { 0 } ^ { 2 } } } .$ . Then, we can rewrite the phase expression in Eqn. 1 as below:

$$
\theta = \left(\frac {4 \pi}{\lambda} \sqrt {(x _ {0} + v t) ^ {2} + y _ {0} ^ {2}} + \mu\right) \bmod 2 \pi \tag {5}
$$

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 1, Article 7. Publication date: March 2021.

So the changing rate 𝑟 of phase over time is theoretically given by

$$
r = \frac {\mathrm{d} \theta}{\mathrm{d} t} = \frac {4 \pi}{\lambda} \cdot \frac {v ^ {2} t + v x _ {0}}{\sqrt {(x _ {0} + v t) ^ {2} + y _ {0} ^ {2}}} \tag {6}
$$

Apparently, the changing rate 𝑟 is inversely proportional to tag’s Y-coordinate $y _ { 0 }$ given a speci#c time 𝑡 and initial position $x _ { 0 } .$ A larger 𝑟 means a smaller Y-coordinate, which is also in accord with our observation. We can also understand this from another intuitive perspective. Like Fig. 5(a) shows, as a tag moves horizontally, it will possess a velocity component of 𝑣 cos 𝛼 towards the antenna. So when it situates at a longer distance from the antenna along Y-dimension, a larger 𝛼 would be observed, and thus a lower 𝑣 cos 𝛼, which further leads to a smaller changing rate in phase.

Based on Eqn. 6, assuming all tags maintain the same $x _ { 0 } .$ , to obtain the order of tags along Y-dimension, one straight-forward method is to calculate their phase changing rates at a speci#c time point $t _ { i } ,$ and order the results in an inverted manner. To be speci#c, given a measured phase pro#le $\{ < t _ { 1 } , \theta _ { 1 } > , < t _ { 2 } , \theta _ { 2 } > , . . . , < t _ { N } , \theta _ { N } > \}$ , then the phase changing rate $r ( t _ { i } )$ at time $t _ { i } \left( i > 1 \right)$ is computed as

$$
r (t _ {i}) = \left| \frac {\theta_ {i} - \theta_ {i - 1}}{t _ {i} - t _ {i - 1}} \right| \tag {7}
$$

However, this naive method can not directly work in our case because of the following two challenges. First, we know the phase is a sensitive metric and practical measurements are easily a"ected by surrounding noise even though the tag’s position keeps invariant. Hence, it is far from accurate to utilize only one sampled changing rate for tag ordering. Second, also the most important, the assumption that all tags maintain the same $x _ { 0 }$ , which means they have the same X-coordinate, can hardly hold in practical situations. We also cannot have such strong constraints on tag’s relations along X-axis when our #nal goal is to order them on the full X-Y dimensions.

Concerning the #rst challenge, we #nd that even though the phase value may exhibit some noise at some time points, the overall changing trend of the phase pro#le agrees with our theoretical analysis. Based on this, we propose to integrate the phase changing rate over a chosen time window, and then exploit the integrated value, which we also call the overall changing rate, as a metric for ordering tags. As for the second challenge, without the assumption on $x _ { 0 } ,$ tags may hold various X-values. Recall Eqn. 6, it is apparent that the phase changing rate is not only determined by the tag’s Y-coordinate, but also related to its initial X-position 𝑥0 and time 𝑡. Thus, we cannot simply apply a #xed/absolute time window for all the tags as the computed changing rates in this way may not conform to tags’ real order. The key issue here is how to choose appropriate time windows that suit di"erent tags.

We already know that all tags’ phase pro#les demonstrate similar V-zone patterns. Suppose there are total 𝑀 tags on the conveyor. Then for the $j ^ { t h } \left( 1 \leq j \leq M \right)$ identi#ed tag, we can extract the bottom point of its V-zone leveraging the technique proposed in Section 4. Let $\tau _ { j }$ be the time of the bottom point, which exactly depicts when the tag passes the antenna. Formally, we set the time window as the interval below:

$$
[ \tau_ {j} - T / 2, \tau_ {j} + T / 2 ], \tag {8}
$$

$$
0 <   T \leq \min \{2 \tau_ {1}, 2 \tau_ {2}, \dots , 2 \tau_ {M} \}
$$

where 𝑇 denotes the window size. Intuitively, for each tag, the above equation selects a time interval that is symmetric around the bottom point of its V-zone, as the integrating range. Fig. 6 gives an illustrative example considering two tags. The time window corresponds to an overlapped moving range of the two tags. Eqn. 8 guarantees that the chosen 𝑇 would suit all the tags. Apparently, the upper bound of 𝑇 is related to the smallest time 𝜏 among all the tags. In our experiment, the carts/tags are driven by a robot with a slow speed (about $0 . 1 5 m / s )$ moving along a line with a length larger than 1𝑚, so the window size could be a few seconds, which is su!cient for integration purposes. We then integrate the phase changing rate over the above time window through the following expression:

![](images/a7000add7ac845eab801dff73ffb85b5f97c59520e1743469da7db0f18d4cc3a.jpg)



(a) Overlapped range

![](images/70ed67b02328e03591a1fd67ce3ec3b6aa129ab7b047f2c262fc4aa93532eab4.jpg)



(b) Window symetric around the bottom point   
Fig. 6. Choosing a proper time window. (a) When two tags move along the conveyor, they share some overlapped moving range. (b) We integrate tag’s phase changing rate over a time window, which is symmetric around the bo!om point of V-zone and corresponds to an overlapped moving range.

$$
\hat {r} _ {j} = \int_ {\tau_ {j} - \frac {T}{2}} ^ {\tau_ {j} + \frac {T}{2}} r _ {j} (t) \mathrm{d} t \tag {9}
$$

𝑟 (𝑡) is computed with Eqn. 7 for every possible 𝑡 falling in the chosen time window. Once we get all 𝑀 tags’ overall changing rates $\hat { r } _ { 1 } , \hat { r } _ { 2 } , \dots , \hat { r } _ { M }$ , by sorting them in descending order we can obtain the order of tags with their Y-coordinate increasing along Y-dimension. The time complexity of our ordering algorithm is 𝑂 (𝑁 ).

# 5.2 Extending to Two-Antenna Scenario

5.2.1 Motivation. It is known that in real indoor environments, due to the multi-path e"ect and ambient noise, tag’s phase pro#le can be easily a"ected and deviate from the theoretical pattern. As we utilize the measured phase as a basis to order tags, such imperfect measurements could directly impair the accuracy of our approach. To deal with this problem and increase the #nal positioning accuracy, one intuitive choice is to deploy multiple antennas along X-axis to form an antenna array. For each antenna, we can repeat our algorithm to output a candidate result of ordering. Further, by incorporating all candidates through a voting schema, the order of tags can be #nally determined. However, this straight-forward method requires three antennas at least for voting, which would increase both economic and space costs. Besides, more antennas along the X-axis mean to deploy a longer conveyor belt, so that commodities travel longer time on it, which is also more time-consuming for users’ checkout experience.

5.2.2 Our Schema. We propose a lightweight schema that can mitigate the e"ect of imperfect measurements to a certain extent by using only two antennas.

As Fig. 5(b) depicts, we arrange the two antennas at both sides of the conveyor along Y-axis while facing each other, which means the antennas are placed perpendicular to the conveyor instead of along it. Let $d _ { i , j }$ be the distance between the $i ^ { t h } \left( i = 1 , 2 \right)$ antenna and the $j ^ { t h } \left( 1 \leq j \leq M \right)$ tag. $r _ { i , j }$ denotes the phase changing rate of tag 𝑗 with respect to antenna 𝑖. Given two tags, tag 𝑗 and tag 𝑘, assuming their X-coordinates are the same, if tag 𝑗 is closer to antenna 1 than tag 𝑘 is, then we can easily infer that tag 𝑗 is farther from antenna 2 than tag 𝑘 is. More formally, we have

$$
d _ {1, j} <   d _ {1, k} \& d _ {2, j} > d _ {2, k}
$$

According to Observation 5.1, the following derivation holds:

$$
\begin{array}{l} d _ {1, j} <   d _ {1, k} \& d _ {2, j} > d _ {2, k} \\ \Rightarrow r _ {1, j} > r _ {1, k} \& r _ {2, j} <   r _ {2, k} \tag {10} \\ \Rightarrow r _ {1, j} - r _ {2, j} > r _ {1, k} - r _ {2, k} \\ \end{array}
$$

Apparently, the above derivation demonstrates that for a speci"c tag, the di#erence of its phase changing rate between two antennas would be enlarged compared against that when only one antenna is adopted. So we raise our question: can we use the di"erence of phase changing rate between two antennas as the metric for tags’ order? The answer is yes, and below gives the theoretical proof.

As shown in Fig 5(b), suppose the two antennas are located at $( 0 , Y _ { 1 } )$ and $( 0 , Y _ { 2 } )$ . Without loss of generality, here we assume $Y _ { 2 } > Y _ { 1 } \ge 0 .$ . Let $\left( x _ { 0 } , y _ { 0 } \right)$ be the initial position of the tag, and 𝑣 be its moving speed. De#ne $r _ { 1 } , r _ { 2 }$ as the phase changing rates reported by the two antennas respectively, and $\Delta r$ as their di"erence. $\Delta r$ is also called relative phase changing rate. Similar to Eqn. 6, we have

$$
\Delta r = r _ {1} - r _ {2} = \frac {4 \pi}{\lambda} \left[ \frac {v ^ {2} t + v x _ {0}}{\sqrt {\left(x _ {0} + v t\right) ^ {2} + \left(Y _ {1} - y _ {0}\right) ^ {2}}} - \frac {v ^ {2} t + v x _ {0}}{\sqrt {\left(x _ {0} + v t\right) ^ {2} + \left(Y _ {2} - y _ {0}\right) ^ {2}}} \right] \tag {11}
$$

Obviously, the value of $y _ { 0 }$ falls in the interval of $[ Y _ { 1 } , Y _ { 2 } ]$ with the assumption $Y _ { 2 } > Y _ { 1 } \ge 0$ . According to the above equation, the relative phase changing rate Δ𝑟 would decrease monotonically with the increase of tag’s Y-coordinate 𝑦0.

Here in two-antenna scenario, for one speci#c tag, we have two phase pro#les measured by two antennas respectively. Similar to the approach adopted in Section 5.1, for the $j ^ { t h }$ tag, we integrate the relative phase changing rate over a pre-de#ned time window as below

$$
\Delta \hat {r} _ {j} = \int_ {\tau_ {j} - \frac {T}{2}} ^ {\tau_ {j} + \frac {T}{2}} \Delta r _ {j} (t) d t = \int_ {\tau_ {j} - \frac {T}{2}} ^ {\tau_ {j} + \frac {T}{2}} r _ {1, j} (t) d t - \int_ {\tau_ {j} - \frac {T}{2}} ^ {\tau_ {j} + \frac {T}{2}} r _ {1, j} (t) d t \tag {12}
$$

Since we arrange the two antennas along the Y-axis, the bottoms of their V-zones would occur at nearly the same point in time for one tag. So here we can use the same time interval $[ \tau _ { j } - T / 2 , \tau _ { j } + T / 2 ]$ (see Eqn 8) for the two antennas for simplicity. $r _ { 1 } ( t )$ and $r _ { 2 } ( t )$ are also computed through Eqn 7 in a similar way. After we get all 𝑀 tags’ overall relative changing rates $\Delta \hat { r } _ { 1 } , \Delta \hat { r } _ { 2 } , . . . , \Delta \hat { r } _ { M }$ , by sorting them in descending order we can obtain the order of tags with their Y-coordinate increasing along Y-dimension. In addition to resisting measurement errors, the adoption of two antennas can also reduce the negative e"ect of tag’s height to a certain extent, as we soon will discuss in the later section.

# 6 SYSTEM WORKFLOW

Remember that our #nal goal is to determine which cart a tagged item belongs to. So far we have realized tag ordering along both X-dimension and Y-dimension. In reality, sometimes we need not know the exact order of all tags. For example, the order among tags inside the same shopping cart is not so important compared with the order of tags near the anchors, since we mainly focus on the relative position between anchor tags and item tags. Next in this section, we will introduce the overall work%ow of Taggo in self-checkout context.

# 6.1 Acquiring Relationship of Anchor Tags

As Fig. 1 shows, every shopping cart has four anchor tags on its four sides. When placed on the conveyor belt, we have no idea about which two tags are along X-axis and which are along Y-axis. The #rst thing is to #gure out the geometric relation between anchor tags. Without loss of generality, suppose anchor tags are arranged in a clockwise manner, with tag 1 sitting opposite to tag 3 and tag 2 opposite to tag 4. We #nd that if tags are along

Y-axis, the time they pass through the antenna would be similar, whereas a large di"erence would appear if tags are along X-axis. Therefore, to infer one group of tags belong to which axis, we utilize the bottom point in phase pro#le to calculate the following di"erence:

$$
\left\{ \begin{array}{l} \delta_ {1} = \tau_ {1} - \tau_ {3} \\ \delta_ {2} = \tau_ {2} - \tau_ {4} \end{array} \right. \tag {13}
$$

As illustrated in Section $5 . 1 , \tau _ { i }$ denotes the time of anchor tag $i ^ { \prime } s$ bottom point, which we also call “D-time” for short. If $\delta _ { 1 } > \delta _ { 2 }$ , tag 1, tag 3 are supposed to be along X-dimension and tag 2, tag 4 are along Y-dimension, and vice versa. Further, through our proposed ordering method we can also #nd out the relative positions of tags along the same dimension.

# 6.2 Classifying Item Tags

Now that we get the geometric relation among anchor tags, to determine which cart an item tag belongs to, the #rst thing is to obtain the full-dimension relative positions among the tag and all carts’ anchor tags. Ideally, the location of the target tag should exactly fall into the region formed by four anchor tags of a speci#c cart. However, due to the instability of phase measurements and indoor environment, the ordering result we get could involve unknown errors, so that the target tag may not even fall into any feasible cart area. To address this issue, we propose to incorporate a probabilistic model. Our basic idea is if the ordering algorithm infers that one item tag has a similar position with not only one anchor tags, we should include all these anchor tags/carts as candidates.

To be more concrete, let 𝜏 be the D-time of the target tag, and $\Delta \hat { r }$ be its overall relative phase changing rate. For every possible cart $C _ { i } { \mathrm { . } }$ suppose it carries four anchor tags $I _ { 1 } , I _ { 2 } , I _ { 3 } , I _ { 4 }$ with $I _ { 1 } , I _ { 3 }$ along X-dimension and $I _ { 2 } , I _ { 4 }$ along Y-dimension. Let us #rst consider the X-dimension. If $\tau _ { I _ { 1 } } < \tau < \tau _ { I _ { 3 } }$ , then cart $C _ { i }$ is obviously a candidate host of the item tag. Moreover, if $| \tau - \tau _ { I _ { 1 } } | < \varepsilon \ \mathrm { o r } | \tau - \tau _ { I _ { 3 } } | < \varepsilon \ ( \varepsilon$ is a pre-de#ned small threshold), or in other words, the item tag is very close to one of the anchor tags along X-dimension, we should also include $C _ { i }$ as a candidate. By traversing all the carts, suppose we have selected 𝐿 candidates $C _ { 1 } , C _ { 2 } , \dots , C _ { L }$ in total. Then we turn our attention to Y-dimension. For every candidate cart $C _ { i } ,$ , we give it a score $\mathbf { \nabla } \mathcal { P } i$ to measure the probability that it indeed carries the target tag. $\mathbf { \nabla } \mathcal { P } i$ is computed through the following probabilistic model:

$$
p _ {i} = \frac {e ^ {z _ {i}}}{\sum_ {l = 1} ^ {L} e ^ {z _ {l}}} \tag {14}
$$

where

$$
z _ {i} = - \big (| \Delta \hat {r} - \Delta \hat {r} _ {I _ {2}} | + | \Delta \hat {r} - \Delta \hat {r} _ {I _ {4}} | \big)
$$

$\mathbf { \nabla } \mathcal { P } i$ is essentially a softmax function, also known as the normalized exponential function. Softmax is a generalization of the logistic function to multiple dimensions, and is commonly used in neural networks to normalize a given vector. $\Delta \hat { r }$ is computed with Eqn. 12. Here, since $z _ { i } = - ( | \Delta \hat { r } - \Delta \hat { r } _ { I _ { 2 } } | + | \Delta \hat { r } - \Delta \hat { r } _ { I _ { 4 } } | )$ , it is easy to #gure out that if a tag indeed belongs to the candidate cart $C _ { i } , \Delta \hat { r }$ would take a value between $\Delta \hat { r } _ { I _ { 2 } }$ and $\Delta \hat { r } _ { I _ { 4 } }$ , thus resulting in a relatively big $z _ { i }$ and $p _ { i } . \boldsymbol { \mathrm { A } }$ higher $\mathbf { \nabla } \mathcal { P } i$ also indicates the item tag is more likely to belong to that candidate cart. Eventually, by traversing all the candidate carts, the target tag is supposed to be carried by the cart which has the highest score $\mathbf { \nabla } \mathcal { P } i$ , or in other words, the tagged item is classi#ed to the cart that has the highest $\mathbf { \nabla } \mathcal { P } i$ . In case that the target tag is dropped by customers, which means it does not belong to any cart, we judge each computed score with an empirical threshold. If all scores are below this threshold, we infer that the item is a dropped one.

# 6.3 Considering Item’s Height

Our analyses in Section 4 and 5 only consider the X-Y plane, which have an implied assumption that all tags have the same height. But in real-world retail applications, commodities could have quite di"erent heights, and we can not strictly require users to keep the tags on their purchases along the same height. In this part, we further discuss the in%uence of tag’s height on our result.

![](images/fbc7f5f92cde880563e3070dc055b8c8b696805c3bc592da29c5786308568765.jpg)



(a) One antenna

![](images/b784a7a2fe00af51ae5229db0079982894132a1790e4a3d2e13897be1c3c3e7b.jpg)



(b) Two antennas   
Fig. 7. Ambiguity caused by tag’s height. (a) Tag 1 has a bigger Y-coordinate than Tag 2, but Tag 2 is farther to the antenna because it has a larger height “H”. (b) For every point on the hyperbola, the di#erence of its distances to Antenna 1 and Antenna 2 is constant.

Even if di"erent tags may get various heights, their V-zone patterns still hold and the relative time order of their bottom points remains unchanged as long as they maintain the same X-coordinates. So the ordering result along X-dimension is independent of tag’s height.

We now consider the Y-dimension. Recall that we use tag’s phase changing rate to infer its relative location along Y-dimension, as a larger Y-coordinate means a longer distance between the tag and antenna, which results in a smaller phase changing rate. However, such theory could be untenable if we take tag’s height (i.e., Z-coordinate) into account. Fig. 7(a) shows an illustrative example, which gives a side view of Y-Z plane. Tag 1 has a bigger Y-coordinate than Tag 2, but Tag 2 has a height of “H”. As a result, compared to Tag 1, Tag 2 is farther to the antenna $( i . e . , d _ { 2 } > d _ { 1 } )$ , and thus gets a smaller phase changing rate. Mathematically, if two adjacent items are Δ𝑦 apart along Y-axis, then they could be mistakenly ordered if their height di"erence exceeds Δ𝑦.

Since we utilize two antennas to deal with measurement errors, we will demonstrate that this can also mitigate ordering mistakes in Y-dimension caused by tag’s height. As described in Fig. 7(b) (Y-Z coordinate system), the green and yellow squares denote two item tags and the grey ones represent anchor tags. For the sake of presentation, here we assume all tags have the same X-coordinate. Suppose Tag 1, Tag 2 and the two antennas are located at $( a , 0 ) , ( a + \Delta a , h )$ and $( \pm Y _ { 0 } , 0 )$ respectively. We draw a branch of a hyperbola with Antenna 1 and Antenna 2 as foci and (𝑎, 0) as vertex. In other words, for every point on the hyperbola, the di"erence of its distances to Antenna 1 and Antenna 2 is #xed, which can be expressed as

$$
\frac {y ^ {2}}{a ^ {2}} - \frac {z ^ {2}}{b ^ {2}} = 1 \tag {15}
$$

where $b ^ { 2 } = Y _ { 0 } ^ { 2 } - a ^ { 2 }$ . Theoretically, points on the hyperbola should have identical relative phase changing rate Δ𝑟 as they always maintain the same relative distance to the two antennas. If Tag 2 is located on the hyperbola, then according to Eqn. 15, its height should satisfy

$$
h = \frac {\sqrt {Y _ {0} ^ {2} - a ^ {2}}}{a} \sqrt {(2 a + \Delta a) \Delta a} \tag {16}
$$

In such a case, item Tag 2 could be ambiguously ordered as Tag 1, and thus be classi#ed into the wrong cart. Here gives an illustrative example, if $Y _ { 0 } = 1 0 0 c m , a = 6 0 c m$ , and the spacing Δ𝑎 between the two item tags equals

![](images/5b721ac15e4c8971015193200fa92be198bae414b1af21cdf83bb1dd1627b8df.jpg)



Fig. 8. Scenario where carts are not placed in parallel to the axes. Then item tags inside a cart may not strictly satisfy the relative position constraints with regard to the four anchor tags. The blue item tag may be falsely classified outside carts.

10𝑐𝑚, then ℎ is about 48𝑐𝑚 by calculating through the above equation. Namely, Tag 2 should be at least 48𝑐𝑚 higher than Tag 1, then their order could be a"ected. Considering the checkout scenario, this height restriction (< 48𝑐𝑚) can be easily met if we guide the users to place their shopping items properly. Besides, since di"erent carts are naturally separated by a distance (often > 10𝑐𝑚), this further makes it harder to classify items into false carts. We will give more experimental evaluations in the next section.

# 7 ENHANCING TAGGO’S PRACTICAL APPLICABILITY

In this section, we present more feasible solutions to enhance Taggo’s applicability to various real-world circumstances, and give useful strategies to guide the con#gurations of crucial thresholds involved in our algorithms.

# 7.1 Cart Placement

In practical applications, users may not place their carts in the desired manner that is parallel to the moving direction of the conveyor (i.e., X-axis). Then item tags inside a cart may not strictly satisfy the relative position constraints with regard to the four anchor tags. Fig. 8 shows an illustrative example. The blue tag in the #gure observes a slightly larger relative position along Y-dimension than the anchor tag 1, while its relative position should lie between anchor tag 1 and 3, in an ideal situation where the cart is placed parallelly to X-axis. So the blue item tag could be falsely classi#ed in theory. But recalling Section 6.2, since we have employed a probabilistic model to classify tags by incorporating measurements from both X- and Y-dimension, generally speaking, the blue tag in Fig. 8 still gets more chance to be classi#ed into the correct cart (cart 2). Besides, to better deal with such cases, we suggest that a feasible solution is to deploy an extra pair of anchor tags onto the two diagonal positions of each shopping cart. Then the relative position of an arbitrary item tag inside the cart should de#nitely lie between the two diagonal anchor tags. We can utilize this constraint to make a further validation on which cart (if any) one item tag belongs to.

# 7.2 Undesired Se!ings

Multi-path e!ect. In indoor environments, there exists multi-path e"ect, especially when people moving around, making the #nal received phase a combination of multiple copies of RF signals and thus deviate from the theoretical value. As demonstrated in Section 5.2, we have combined measurements from two properly deployed antennas, which can mitigate the impact from the multi-path e"ect to a certain extent. In addition, we would suggest utilizing more antennas to further reduce the negative impact from multi-path and enhance the #nal accuracy.

![](images/4922aabb6c1b1829cc645c0eead7bd52bbea4f34a7c83e078cff6cc091d0cdda.jpg)



Fig. 9. Experiment setup. We build a prototype and evaluate Taggo using commercial RFID devices.

Liquid/metal objects. If tags are attached on metallic (or liquid) surfaces or surrounded by such objects, their replies will be drawn in the re%ections from these materials. Apparently, our solution fails to work if the reader cannot receive replies from tags. In such situations, we would suggest using the anti-metal (or anti-water) RFID tags [14, 21]. These tags are made of special materials like ceramics and trickily designed in circuits. Even when there exist strong interferences from surrounding objects, the reader can still receive tags’ replies.

# 7.3 User-Defined Thresholds

𝜂 in Section 4.3 and Section 5.1. As we know, the measured phase has a range of [0, 2𝜋], and thus jumps when it approaches 0 or 2𝜋 due to the mod operation. The threshold 𝜂 is used to determine whether there exists such a phase jump. So we should set 𝜂 to a relatively large value. According to our empirical study, it is feasible that 𝜂 falls into $[ \pi / 3 , 5 \pi / 3 ]$ . So without loss of generality, we choose 𝜂 to be 𝜋 by default. Besides, as 𝜂 inherently results from the tag’s phase attribute, it is independent of other system settings such as item size and orientation.   
𝜖 in Section 4.3. The threshold 𝜖 is used to check whether a phase measurement approaches 2𝜋. So it should be set to a small value. Besides, the measured RF phase also follows a typical Gaussian distribution with a standard deviation of about 0.1 radians, a"ected by basic thermal noise at the receiver side [40]. Considering this, 𝜂 should be several times greater than 0.1. With our empirical study, we select 𝜖 as 𝜋/3 by default.   
𝜀 in Section 6.2. The threshold 𝜀 is utilized to determine whether two points are close to each other in time domain. Essentially, our algorithm wants to tolerate the scene that two tags get similar locations along Xdimension. Considering the size of practical shopping carts, we think that if two tags get a distance fewer than 3 centimeters, then they can be regarded to have ‘similar’ locations. In our experimentation, the tags move at a uniform speed of about 0.15 m/s. Then 3 cm distance corresponds to a time duration of about 0.2 seconds. Thus, a reasonable value of threshold 𝜀 can be set to 0.2 s. According to the above analysis, 𝜀 is apparently related to the moving speed of the conveyor that drives tags. If the tags move faster, 𝜀 should be tuned to a smaller value, and vice versa.

# 8 IMPLEMENTATION & EVALUATION

We have implemented Taggo using COTS UHF RFID devices and conducted performance evaluation in our lab environment as shown in Fig. 9.

![](images/7427d98b472791579a9be22ac5cfdd3adb39f770f03100f06b8b3c1c40c8b548.jpg)



Fig. 10. Ordering accuracy

![](images/32bd2f8850de91af5ff3fb385ac2a05d54306eec36e524a09fba66134e8d6a38.jpg)



Fig. 11. Accuracy vs. antenna number

# 8.1 Prototype

Hardware: Taggo adopts an ImpinJ Speedway Revolution R420 reader [2], compatible with EPC Gen2 standard and operating in the frequency band of 920.5 ∼ 924.5MHz by default. The reader is connected to our host end through Ethernet. We employ two antennas with circular polarization and 8dBi gain, whose sizes are 22.5 cm × 22.5 cm × 4 cm. Four types of tags from Alien Corp, modeled ${ } ^ { * } 2 \times 2 { } ^ { * } ;$ , “Square”, “Squig” and “Squiggle” are employed. Each tag only costs about 7 cents on average [1], which is cost-competitive in the manufacture of commodities.

Software: We adopt the Low Level Reader Protocol (LLRP) [13] to communicate with the reader. ImpinJ reader extends this protocol for supporting the phase report. We adjust the con#guration of the reader to immediately report its readings whenever tags are detected. The software of Taggo is implemented using Java language. We use a MacBook Pro laptop to run all our programs, as well as connecting to the reader under LLRP. The machine equips Int el Core i7 CPU at 16GB memory.

System Settings: In our experimentation, we utilize a robot car to simulate a conveyor belt (see Fig. 9). The mobile robot can be programmable to run in a linear track at di"erent speeds. On the robot car, we install a few plastic baskets, with RFID tags attached on their four sides. Two types of baskets are adopted, with sizes of 29 cm × 21 cm × 12 cm and 22 cm × 15 cm × 10.5 cm respectively. We also put some tagged items inside and outside the baskets on the robot platform. Two antennas are deployed on the two sides of our experimental desktop, perpendicular to the moving track of the robot. Ground truth locations of antennas and tags are measured by a laser range #nder with a supposed error of ±0.1𝑚𝑚. Other system settings, such as the distance between baskets, positions of antennas, types of tags, are tunable parameters, which we will evaluate later.

# 8.2 Ordering Accuracy

The ordering accuracy among tags plays a key role in Taggo’s performance. Note that a tag is correctly localized if and only if the detected order of the tag is equal to the actual order of it. We de#ne the ordering accuracy $R _ { o }$ as the ratio below

$$
R _ {o} = \frac {\# \text { of tags ordered correctly}}{\# \text { of tags in total}} \times 100 \%
$$

We deploy up to 20 tags with various X- and Y- coordinates on the robot platform and manipulate the robot to move with a uniform speed of about 0.15𝑚/𝑠. We compare Taggo with other four state-of-the-art relative positioning schemas: a) OTrack [29]: leverages RSSI trends and reading rates of tags to infer their order along Xaxis; b) STPP [30]: utilizes the spatial-temporal dynamics in phase pro#les to infer the order of tags; c) RF-Scanner [22]: exploits phase characteristics of RFID tags and incorporate a robot to localize books and detect lying-down books. We conduct experiments under various settings with di"erent numbers of tags and layouts. For each setting, we repeat the experiment 50 times. Fig. 10 plots the average accuracy ratio along both X-dimension and Y-dimension.

![](images/bcedb9b6ab73bc4d304b7fdd3825c1ea0f67f25d6ecfcbbcdd962f0c7899099c.jpg)



Fig. 12. Baskets are placed in a front-to-back or sideby-side way

![](images/ca31e1d1e54a45140b74d603167bfaf71da46fbd5231a344061f8087859049c5.jpg)



Fig. 13. Classifying accuracy vs. # of baskets

X-dimension accuracy: From Fig. 10 we #nd that Taggo has competitive accuracy with STPP and RF-Scanner, while the accuracy of OTrack is signi#cantly lower than the other three. This is easy to understand because OTrack utilizes RSSI as the ordering metric, which is highly sensitive to multi-path propagation and antenna gain, and thus prone to be unreliable compared against the phase attribute. With the complex DTW method, the precision of STPP can reach 88%. RF-Scanner also achieves an average accuracy of 91% with a self-designed robot component. Compared to OTrack which requires a reference phase pro#le and RF-Scanner which incorporates dedicated hardware, Taggo is more time-e!cient and light-weighted. Overall, our schema achieves a mean ordering accuracy of 93% with a standard deviation of 5% along X-dimension, which is fairly good for most applications.

Y-dimension accuracy: Since OTrack and RF-Scanner only focus on positioning in X-axis, we compare Taggo with STPP which reports Y-dimension results. As shown in Fig 10, Taggo achieves a mean accuracy of 89% with a standard deviation of 4% along Y-dimension. Since we propose to leverage the overall phase changing rate and combine measurements of two antennas to handle negative impacts from environmental noise, Taggo proves to be robust and has very small variances in di"erent settings. The #nal ordering accuracy in the combined dimension reaches 90% on average.

E!ectiveness of utilizing two antennas: To intuitively validate Taggo’s performance under two-antenna scenario, we further make a controlled study with only one antenna adopted and compare their results in Fig. 11. We vary the distance between antenna and conveyor from 0.3 m to 1.5 m. It can be seen that in either of these settings, the errors among various distances have little di"erence. The ordering accuracy along Y-dimension with two antennas increases up to 92% while that with one antenna is only 87%. Clearly, our idea to utilize two antennas is feasible and can directly promote the #nal accuracy in indoor environments. The straight-line distance between either of the antennas and the conveyor is set to 1.2 m as default in our experiments.

# 8.3 Classifying Accuracy

Targeting at the self-checkout context, whether an item can be classi#ed into the cart that really carries it with high accuracy is of great importance. For one item tag, it is correctly classi#ed if and only if the detected host of the tag is identical to the real host of it. Consequently, we de#ne the classifying accuracy $R _ { c }$ as below

![](images/cc40e50a65aee03f64e67b88a7f6ab3aaee744b6c8547214a9ea0840247f7a6a.jpg)



Fig. 14. Classifying accuracy vs. basket distance

![](images/15c19595185fb271a7e0f340365e797698a2a8b916f0c4098a138e4f76c89411.jpg)



Fig. 15. Classifying accuracy vs. item height

$$
R _ {c} = \frac {\# \text { of item tags classified correctly}}{\# \text { of item tags in total}} \times 100 \%
$$

To evaluate Taggo’s classifying accuracy, we deploy several plastic baskets on the experimental platform. Some of these baskets are placed in a front-to-back manner along X-dimension and some are placed side-by-side along Y-dimension (see Fig. 12). Anchor tags are attached on the edges of each basket. We run our classifying algorithm mentioned in Section 6 to give predictions on item tags’ hosts, and compute the corresponding classifying accuracy.

Number of baskets. To simulate real physics in checkout circumstance, we #rst vary the number of baskets from 2 to 5, and study the in%uence from basket population. Fig. 13 presents the average classifying accuracies with di"erent numbers of baskets. We observe that the mean errors among various basket populations are slightly di"erent, from the minimum of 95% to the maximum of 98%. And the result is more errorless when the basket population is small. This is reasonable because interference among baskets would be larger when there are more baskets.

Distance between baskets. Then, to check Taggo’s e"ectiveness when baskets are compactly placed, we change the distances between adjacent baskets from 3 cm to 15 cm with four levels while keeping the same basket population. As shown in Fig. 14, the average classifying accuracies are 93%, 95%, 97% and 98% when basket intervals are 3 cm, 6 cm, 10 cm and 15 cm respectively. We observe from the #gure that the mean error degrades a little with the interval between baskets decreases. This is easy to understand because when two adjacent baskets get too close, an item tag between them would be more likely to be mistakenly classi#ed.

Item height. We further study the e"ect of item’s height on Taggo’s classifying accuracy. We vary the height of di"erent items and make the maximum height di"erence between tags as 0, 10 cm, 20 cm and 30 cm respectively. We also utilize one and two antennas to perform experiments to make a comparison study. Fig. 15 plots the #nal item classifying accuracies. The mean accuracies are 97%, 95%, 90% and 87% respectively in the case with two antennas, while decrease to 93%, 88%, 80% and 68% in the case with only one antenna. We also come to the following two #ndings from our evaluation results. 1) With the height di"erence becoming larger, the accuracies in both cases drop to a certain extent. It is reasonable because when there exist higher items, adjacent tags become more easier to be ambiguously ordered. 2) The overall performance in two-antenna case is apparently better than that in single antenna case, which means our approach with two antennas can reduce the negative impact from item height e"ectively.

![](images/020b2560eae57135fbac0f565044007bc825ed02b1b07ba841c03fa212a58e55.jpg)



Fig. 16. Impact of tag distance

![](images/0969e4a9ee1fbd1d2d46e8389fca639f07fcfaeca19487c9d6be9984edaf771a.jpg)



Fig. 17. Impact of tag population

Tag orientation. As commodities in shopping carts may be placed randomly in real-world scenarios, then tags attached may have various orientations. Here we de#ne the orientation of a tag as the angle between its polarization direction and the X-axis. We conduct four groups of experiments with two di"erent types of tags (model “2×2” and “Squiggle”) in a less controlled environment where item tags could maintain di"erent orientations. In the four settings, we make the biggest orientation among item tags as 30◦, 60◦, 90◦ and $1 5 0 ^ { \circ }$ respectively. Table 1 compares the averaged classifying accuracies with regard to tag orientations. We get the following two observations from this table. 1) For the same tag model, the orientation has a slight impact on the #nal classifying accuracy, and generally speaking, when tag’s orientation di"erence gets bigger, the accuracy decreases a little bit. This is understandable because it has been demonstrated that tag’s orientation would have a certain e"ect on its measured phase even though its location remains invariant [17, 37]. But in our checkout scenario, although di"erent item tags may get diverse orientations, when they move with the conveyor, their orientations actually do not change with time. So the impact of tag orientation is very small. 2) For di"erent tag types, “2×2” tends to be more robust to orientation than “Squiggle”. This can be explained by the shape of tags, because 2×2 has a square shape while Squiggle is rectangle. So Squiggle is easier to be a"ected by the orientation.

To summarize, the overall classifying accuracy of Taggo reaches as high as 95% on average, which is noticeably better than the ordering accuracy. This validates the e!ciency of our proposed classifying schema.

# 8.4 Tuning Parameters

We further discuss the following factors that may have an in%uence on Taggo’s performance. We mainly focus on the metric of ordering accuracy in this part.

8.4.1 Tag Distance. We #rst examine the e"ect from distance between adjacent tags. We range the interval from 3 cm to 12 cm with a step length of 3 cm and carries experiments in each setting. As revealed in Fig. 16, when adjacent tags are placed very close (e.g., 3 cm apart), the mean accuracy drops to only 84%. And with their distance increasing, the accuracy also shows a rising trend, which is also consistent with our expectation. When tags are placed 12 cm apart, the mean accuracy reaches 92%.

Table 1. Classifying accuracy vs. tag orientation 

<table><tr><td>Maximum tag orientation</td><td>30°</td><td>60°</td><td>90°</td><td>150°</td></tr><tr><td>Accuracy (Squiggle)</td><td>97%</td><td>96%</td><td>95%</td><td>96%</td></tr><tr><td>Accuracy (2×2)</td><td>97%</td><td>97%</td><td>97%</td><td>96%</td></tr></table>

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 1, Article 7. Publication date: March 2021.

![](images/1ad60104dc647cee4a901387e79541df29efd911c193ca2c630478777d55410b.jpg)



Fig. 18. Impact of tag diversity

![](images/b7ae6800381f8dec2a340d187d876b0a6bd537f8adcc43c3d767af65e4d07a7f.jpg)



Fig. 19. System latency

8.4.2 Tag Population. In practical deployments, there could be multiple tagged items in one cart. We then evaluate Taggo’s performance under multi-tag scenario. We change the number of tags from 5 to 20 within the reading zone of antennas. The distance between adjacent tags is randomly chosen from the range of [3 cm, 10 cm]. The results are plotted in Fig. 17. We have the following observations from the #gure: a) When there are a small number of tags detected in the reading zone, e.g., 5 tags, Taggo achieves excellent performance with ordering error less than 10%. b) With the tag population gets bigger, the error also grows gradually, to 86% when there are 20 tags. c) Even when there are an adequate number of tags, e.g., over 20 tags, the performance of Taggo still maintains at a moderate level, with about 86% accuracy.   
8.4.3 Tag Diversity. We experiment on four models of tags, namely $^ { 6 6 } 2 \times 2 ^ { 5 5 }$ , “Square”, “Squig” and “Squiggle” to study Taggo’s robustness when di"erent types of tags are adopted. All these tag types have diverse antenna sizes and shapes as depicted in Fig.18. For each tag model, the result is averaged from 50 experiments with the same setting. We #nd that although the errors of all models maintain at a small value (less than 15%), there exist some di"erences among them. To be speci#c, 2×2, Sguig and Squiggle have very close accuracy (i.e., 89%, 89% and 88% respectively), while the Square model observes a lower accuracy of 85% with a higher standard deviation of 9%. This can be explained by the size of tag’s antenna, because Square has a more compact volume (with a size of only 22.5 mm × 22.5 mm) compared with the other three types. Generally speaking, the tag with a larger antenna could absorb more energy from the reader, making its backscattered signal stronger (i.e., higher SNR). The ordering accuracy is thereby higher. In our experimentation, we choose the “Squiggle” model as default.   
8.4.4 System Latency. In previous sections, we analytically suggest that the time complexity of Taggo is 𝑂 (𝑁 ) along both X- and Y- dimensions. Now we conduct experimental measurements to examine the latency of our system. Total 100 trials are carried out and we compare the ordering latency of Taggo with STPP. The CDF of the result is plotted in Fig. 19. The mean time consumed in Taggo is 0.15 s, about 10× faster than STPP which achieves a latency of 1.47 s on average. Besides, for Taggo, the standard deviation of system latency is 0.05 s, and 90% of the ordering is #nished within 0.22 s. Generally speaking, the accuracy and e!ciency of our system are high enough to meet most demands in relative positioning domain.

# 9 CONCLUSION

In this work, we present a lightweight and e!cient self-checkout system based on commercial RFID products. Our key innovation is to deploy a few anchor tags on the four edges of each shopping cart and perform relative positioning among tagged items and anchor tags without knowing their absolute locations. Putting our idea into practice, we propose a full-dimension relative positioning schema utilizing the phase pro#le acquired from RFID tags, and design a holistic item classifying mechanism to assign each item to the correct cart in a probabilistic way. Experimental results demonstrate that Taggo can achieve fairly high accuracy and e!ciency while maintaining robustness in various settings. We believe our system will promote more possibilities of the RFID-enabled self-checkout solution in real deployments.

# ACKNOWLEDGMENTS

This research is supported in part by the National Key R&D Program of China under grant 2018YFB1004700, the National Natural Science Foundation of China under grants 61902212, 61822205, 61632020 and 61632013, the China Postdoctoral Science Foundation under grant 2019M650683, and the Beijing National Research Center for Information Science and Technology.

# REFERENCES

[1] 2019. Alien Tag Family Product Brief. http://www.alientechnology.com/wp-content/uploads/Tag.   
[2] 2019. ImpinJ Speedway R420 RFID Reader. https://www.impinj.com/platform/connectivity/speedway-r420/.   
[3] 2019. Self-Checkout Technology. http://web.mit.edu/2.744/www/Project/Assignments/humanUse/aychen/references.html.   
[4] 2020. Fujitsu Demonstrates New Technologies at NRF That Address Pain Point for Retailers: Improve Retail Self-Checkout Experience. https://www.fujitsu.com/us/about/resources/news/press-releases/2019/"na-20190110.html.   
[5] 2020. Nordic ID has set out to eliminate checkout queues - releases ground-breaking solution at NRF. https://www.nordicid.com/resources/news/nordic-id-has-set-out-to-eliminate-checkout-queues-releases-ground-breaking-solutionat-nrf/.   
[6] 2020. RFID Based Walk-through Checkout Solution for Future Retail. https://news.panasonic.com/global/topics/2018/55288.html.   
[7] Salah Azzouzi, Markus Cremer, Uwe Dettmar, Thomas Knie, and Rainer Kronberger. 2011. Improved AoA Based Localization of UHF RFID Tags Using Spatial Diversity. In Proceedings of the IEEE International Conference on RFID-Technologies and Applications. 174–180.   
[8] Salah Azzouzi, Markus Cremer, Uwe Dettmar, Rainer Kronberger, and Thomas Knie. 2011. New Measurement Results for the Localization of UHF RFID Transponders Using an Angle of Arrival (AoA) Approach. In Proceedings of the IEEE International Conference on RFID. 91–97.   
[9] Mathieu Bouet and Aldri L Dos Santos. 2008. RFID tags: Positioning principles and localization techniques. In Proceedings of the 1st IFIP Wireless Days. 1–5.   
[10] Alice Bu!, Paolo Nepa, and Fabrizio Lombardini. 2015. A Phase-Based Technique for Localization of UHF-RFID Tags Moving on a Conveyor Belt: Performance Analysis and Test-Case Measurements. IEEE Sensors Journal 15, 1 (2015), 387–396.   
[11] Daniel M Dobkin. 2012. The RF in RFID: UHF RFID in Practice. Newnes.   
[12] Chunhui Duan, Xing Rao, Lei Yang, and Yunhao Liu. 2017. Fusing RFID and Computer Vision for Fine-Grained Object Tracking. In Proceedings of the IEEE International Conference on Computer Communications (INFOCOM). 1–9.   
[13] EPCglobal. 2010. Low Level Reader Protocol (LLRP).   
[14] Yejun He and Huaxia Zhang. 2013. A New UHF Anti-Metal RFID Tag Antenna Design With Open-Circuited Stub Feed. In Proceedings of the IEEE International Conference on Communications (ICC). 5809–5813.   
[15] ImpinJ. 2010. Speedway Revolution Reader Application Note: Low Level User Data Support.   
[16] Nanda Gopal Jeevarathnam and Ismail Uysal. 2018. Grid-Based RFID Localization Using Tag Read Count And Received Signal Strength. In Proceedings of the International Joint Conference on Neural Networks (IJCNN). 1–8.   
[17] Chengkun Jiang, Yuan He, Xiaolong Zheng, and Yunhao Liu. 2018. Orientation-Aware RFID Tracking with Centimeter-Level Accuracy. In Proceedings of the International Conference on Information Processing in Sensor Networks (IPSN). 290–301.   
[18] Kiran Raj Joshi, Steven Siying Hong, and Sachin Katti. 2013. PinPoint: Localizing Interfering Radios. In Proceedings of the USENIX Symposium on Networked Systems Design and Implementation (NSDI). 241–253.   
[19] Rainer Kronberger, Thomas Knie, Roberto Leonardi, Uwe Dettmar, Markus Cremer, and Salah Azzouzi. 2011. UHF RFID Localization System Based on a Phased Array Antenna. In Proceedings of the IEEE International Symposium on Antennas and Propagation (APSURSI). 525–528.

[20] Swarun Kumar, Stephanie Gil, Dina Katabi, and Daniela Rus. 2014. Accurate Indoor Localization with Zero Start-up Cost. In Proceedings of the ACM International Conference on Mobile Computing and Networking (MobiCom). 483–494.   
[21] Laijun Li and Wang He. 2018. Anti-Water UHF RFID Tag Antenna with Multi-Loop Structure for Impedance Matching. In Proceedings of the Progress in Electromagnetics Research Symposium (PIERS-Toyama). 1805–1808.   
[22] Jia Liu, Feng Zhu, Yanyan Wang, Xia Wang, Qingfeng Pan, and Lijun Chen. 2017. RF-Scanner: Shelf Scanning with Robot-assisted RFID Systems. In Proceedings of the IEEE International Conference on Computer Communications (INFOCOM). 1–9.   
[23] Robert Miesen, Fabian Kirsch, and Martin Vossiek. 2013. UHF RFID Localization Based on Synthetic Apertures. IEEE Transactions on Automation Science and Engineering 10, 3 (2013), 807–815.   
[24] Andrea Motroni, Paolo Nepa, Valerio Magnago, Alice Bu!, Bernardo Tellini, Daniele Fontanelli, and David Macii. 2018. SAR-Based Indoor Localization of UHF-RFID Tags via Mobile Robot. In Proceedings of the International Conference on Indoor Positioning and Indoor Navigation (IPIN). 1–8.   
[25] Lionel M. Ni, Yunhao Liu, Yiu Cho Lau, and Abhishek P. Patil. 2003. LANDMARC: Indoor Location Sensing Using Active RFID. In Proceedings of the IEEE International Conference on Pervasive Computing and Communications (PerCom). 407–415.   
[26] Lionel M. Ni, Dian Zhang, and Michael R. Souryal. 2011. RFID-Based Localization and Tracking Technologies. IEEE Wireless Communications 18, 2 (2011), 45–51.   
[27] Pavel V. Nikitin, Rene Martinez, Shashi Ramamurthy, Hunter Leland, Gary Spiess, and K. V. S. Rao. 2010. Phase Based Spatial Identi#cation of UHF RFID Tags. In Proceedings of the IEEE International Conference on RFID. 102–109.   
[28] Andreas Parr, Robert Miesen, and Martin Vossiek. 2013. Inverse SAR Approach for Localization of Moving RFID Tags. In Proceedings of the IEEE International Conference on RFID. 104–109.   
[29] Longfei Shangguan, Zhenjiang Li, Zheng Yang, Mo Li, Yunhao Liu, and Jinsong Han. 2014. OTrack: Towards Order Tracking for Tags in Mobile RFID Systems. IEEE Transactions on Parallel and Distributed Systems 25, 8 (2014), 2114–2125.   
[30] Longfei Shangguan, Zheng Yang, Alex X. Liu, Zimu Zhou, and Yunhao Liu. 2015. Relative Localization of RFID Tags using Spatial-Temporal Phase Pro#ling. In Proceedings of the USENIX Symposium on Networked Systems Design and Implementation (NSDI). 251–263.   
[31] Christian Tellkamp, Thomas Wiechert, Frédéric Thiesse, and Elgar Fleisch. 2006. The Adoption of RFID-based Self-Check-Out-Systems at the Point-of-Sale. In Proceedings of the IFIP International Conference on e-Commerce, e-Business, and e-Government (I3E). 153–165.   
[32] Chong Wang, Hongyi Wu, and Nian-Feng Tzeng. 2007. RFID-Based 3-D Positioning Schemes. In Proceedings of the IEEE International Conference on Computer Communications (INFOCOM). 1235–1243.   
[33] Jue Wang, Fadel Adib, Ross Knepper, Dina Katabi, and Daniela Rus. 2013. RF-Compass: Robot Object Manipulation Using RFIDs. In Proceedings of the ACM International Conference on Mobile Computing and Networking (MobiCom). 3–14.   
[34] Jue Wang and Dina Katabi. 2013. Dude, Where’s My Card? RFID Positioning That Works with Multipath and Non-Line of Sight. In Proceedings of the ACM SIGCOMM Conference. 51–62.   
[35] Jue Wang, Deepak Vasisht, and Dina Katabi. 2014. RF-IDraw: Virtual Touch Screen in the Air Using RF Signals. In ACM SIGCOMM Computer Communication Review, Vol. 44. 235–246.   
[36] Kirti Wankhede, Bharati Wukkadada, and Vidhya Nadar. 2018. Just Walk-Out Technology and its Challenges: A Case of Amazon Go. In Proceedings of the International Conference on Inventive Research in Computing Applications (ICIRCA). 254–257.   
[37] Teng Wei and Xinyu Zhang. 2016. Gyro in the Air: Tracking 3D Orientation of Batteryless Internet-of-Things. In Proceedings of the ACM International Conference on Mobile Computing and Networking (MobiCom). 55–68.   
[38] Bing-Fei Wu, Wan-Ju Tseng, Yung-Shin Chen, Shih-Jhe Yao, and Po-Ju Chang. 2016. An Intelligent Self-Checkout System for Smart Retail. In Proceedings of the International Conference on System Science and Engineering (ICSSE). 1–4.   
[39] Fu Xiao, Zhongqin Wang, Ning Ye, Ruchuan Wang, and Xiang-Yang Li. 2018. One More Tag Enables Fine-Grained RFID Localization and Tracking. IEEE/ACM Transactions on Networking 26, 1 (2018), 161–174.   
[40] Lei Yang, Yekui Chen, Xiang-Yang Li, Chaowei Xiao, Mo Li, and Yunhao Liu. 2014. Tagoram: Real-Time Tracking of Mobile RFID Tags to High Precision Using COTS Devices. In Proceedings of the ACM International Conference on Mobile Computing and Networking (MobiCom). 237–248.   
[41] Zheng Yang, Chenshu Wu, and Yunhao Liu. 2012. Locating in Fingerprint Space: Wireless Indoor Localization with Little Human Intervention. In Proceedings of the ACM International Conference on Mobile Computing and Networking (MobiCom). 269–280.   
[42] Yimin Zhang, Moeness G Amin, and Shashank Kaushik. 2007. Localization and Tracking of Passive RFID Tags Based on Direction Estimation. International Journal of Antennas and Propagation 2007 (2007).   
[43] Yiyang Zhao, Yunhao Liu, and Lionel M. Ni. 2007. VIRE: Active RFID-based Localization Using Virtual Reference Elimination. In Proceedings of the IEEE International Conference on Parallel Processing (ICPP). 56–56.   
[44] Fangwei Zheng, Je"rey Huang, and Mark Meagher. 2009. The Introduction and Design of a New Form of Supermarket: Smart Market. In Proceedings of the International Symposium on Information Engineering and Electronic Commerce. 608–611.