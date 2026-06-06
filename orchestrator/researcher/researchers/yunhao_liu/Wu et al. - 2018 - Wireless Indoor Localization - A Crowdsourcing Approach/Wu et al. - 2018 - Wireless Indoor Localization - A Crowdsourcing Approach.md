Chenshu Wu Zheng Yang Yunhao Liu

# Wireless Indoor Localization

A Crowdsourcing Approach

# Wireless Indoor Localization

Chenshu Wu • Zheng Yang • Yunhao Liu

# Wireless Indoor Localization

A Crowdsourcing Approach

Chenshu Wu

University of Maryland

College Park, Maryland, USA

Zheng Yang

School of Software

Tsinghua University

Beijing, China

Yunhao Liu

School of Software

Tsinghua University

Beijing, China

ISBN 978-981-13-0355-5

ISBN 978-981-13-0356-2 (eBook)

https://doi.org/10.1007/978-981-13-0356-2

Library of Congress Control Number: 2018948837

© Springer Nature Singapore Pte Ltd. 2018

This work is subject to copyright. All rights are reserved by the Publisher, whether the whole or part of the material is concerned, specifically the rights of translation, reprinting, reuse of illustrations, recitation, broadcasting, reproduction on microfilms or in any other physical way, and transmission or information storage and retrieval, electronic adaptation, computer software, or by similar or dissimilar methodology now known or hereafter developed.

The use of general descriptive names, registered names, trademarks, service marks, etc. in this publication does not imply, even in the absence of a specific statement, that such names are exempt from the relevant protective laws and regulations and therefore free for general use.

The publisher, the authors, and the editors are safe to assume that the advice and information in this book are believed to be true and accurate at the date of publication. Neither the publisher nor the authors or the editors give a warranty, express or implied, with respect to the material contained herein or for any errors or omissions that may have been made. The publisher remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

This Springer imprint is published by the registered company Springer Nature Singapore Pte Ltd.

The registered company address is: 152 Beach Road, #21-01/04 Gateway East, Singapore 189721, Singapore

# Preface

Location-based technology surely ranks as one of the most important breakthrough for modern life. Localization techniques underlie the foundation of Internet of Things, while location information contributes one type of the most critical big data nowadays. With the proliferation of mobile computing, location-based services have shaped and enabled a wide range of applications from vehicle navigation to logistical supply chain management and to personal location sharing. While GPS dominates outdoor localization and becomes an essential element of the global information infrastructure like the Internet, indoor localization also attracts people’s attention. Indoor location holds important values for various applications, including resource and infrastructure management, smart home and smart building monitoring, retails and sports analytics, mall navigation, virtual reality, etc.

The past decades have witnessed the fast conceptualization and development of wireless indoor localization. Among numerous technologies, WiFi fingerprint-based approach has become one of the most popular solutions that attracts immense efforts from both academic and industrial communities. Not only a number of start-ups, but also grand corporations including Google, Apple, Cisco, QualComm, Huawei, etc., have invested in and have been developing indoor localization products.

This book aims to provide a comprehensive and in-depth understanding of wireless indoor localization for ubiquitous applications. Specifically, focusing on WiFi fingerprint based localization via crowdsourcing, the book follows a topdown view and involves the three most important issues of indoor localization: deployment, maintenance, and accuracy. Through extensively reviewing the stateof-the-art literatures, it presents the latest advances in crowdsourcing-enabled WiFi localization.

Crowdsourcing is a recently invented and increasingly hot topic in not only research areas but also enterprise business. It has been widely applied in indoor localization to address several critical bottlenecks. As to WiFi fingerprint based localization, crowdsourcing helps with the issues including significant deployment costs, lack of indoor floorplans, and limited location accuracy. Despite a large number of research outputs, it lacks a representative book that provides an extensive view of crowdsourcing-based indoor localization. This book turns out to be the first of its kind, as far as we are aware of, which introduces WiFi fingerprint based localization from a perspective of crowdsourcing. Hence, we hope the reported latest advances can promote the development of this research area and contribute to the interdisciplinary research areas as well.

# Organization of the Book

The book begins with an introductory Part I. We firstly present the background of location-aware applications, current wireless localization problems, and representative localization systems in Chap. 1. The preliminary introduction in Chap. 2 to the concepts and techniques of crowdsourcing, mobile sensing, etc., would guide the readers to understand. The subsequent parts focus on tackling the critical challenges of WiFi-based localization for ubiquitous applications, each from a distinctive aspect of deployment costs, maintenance overhead, and location errors. In these parts, we present the ideas, methods, and systems for implementing the crowdsourcing approach in localization. Specifically, rapid deployment is the first step to make indoor localization available, which is extensively investigated in Part II. In addition, it is also important to maintain consistent quality of service over long-term running, which is carefully addressed in Part III. Moreover, accuracy acts as the most critical metric to reliable and usable indoor localization, which worths in-depth exploration in Part IV. Finally, we make a summary of this book and discuss several future directions in Part V.

Part II to Part IV consist of the main content of this book, and are further elaborated into seven chapters as follows:

Part II Boosting deployment: making it available

In this part, we consider two deployment issues of WiFi-based localization: radio map construction (Chap. 3) and digital floorplan generation (Chap. 4). Harnessing the power of mobile crowdsourcing, we present techniques that automate these two procedures, which can only be completed by manual efforts previously, and therefore rapidly boost the deployment for WiFi-based location systems in practice.

Part III Facilitating maintenance: making it sustainable

WiFi fingerprints are sensitive to temporal environmental dynamics and vary over time. To tackle this problem, in Chap. 5, we seek for adaptive fingerprint updating techniques to adapt collected fingerprints to environmental changes and to guarantee the performance of deployed location services over time. Furthermore, we introduce a self-deployable approach for indoor navigation, which can work in a peer-to-peer manner with no prior installed location services.

Part IV Enhancing accuracy: making it reliable

Traditional WiFi-based localization suffers from large location errors. Based on in-depth understanding of root causes of its location errors, we present novel approaches to improve accuracy by embracing spatial awareness in the form of fingerprint spatial gradient in Chap. 7. We further present image-assisted WiFi fingerprinting in Chap. 8 and address several practical causes of location errors in Chap. 9.

# Anticipated Audience

The book considers the state-of-the-art research results in many academic journals and conferences during its preparation. Thus, readers can track trends and hot topics in the field. With the detailed introduced techniques for practical localization systems, it would draw attention of scientists and researchers in mobile and ubiquitous computing area and other related areas. The provided techniques would also systematically contribute to the practical applications and well guide the readers. Thus, it can serve as a guide book for the technicians and practitioners in the industry of location-based service and mobile sensing. Moreover, we wish this book can genuinely benefit all levels of readers.

The book intends to fit the audience’s different technical backgrounds and career objectives and provides a balance of localization technology and location-aware applications. It does not require very specific knowledge of location-awareness technology. We kindly suggest the readers should have some basic knowledge of computer algorithms and wireless networks.

Should the readers have any questions or suggestions, please contact the authors by email via wucs32@gmail.com.

College Park, USA

Beijing, China

Beijing, China

March 2018

Chenshu Wu

Zheng Yang

Yunhao Liu

# Acknowledgments

We would like first to thank the China Computer Federation (CCF) for the precious CCF Excellent Doctoral Dissertation Award. To my knowledge, it was this award that led to the chance of publishing a book on my research results with Springer.

We are grateful to many former and present students in our research groups for their contributions to the original research content covered by multiple chapters. In particular, we are most grateful to Dr. Junliang Liu at Google, Dr. Han Xu at Huawei, Dr. Zimu Zhou at ETH Zurich, Chaowei Xiao at University of Michigan, Ann Arbor, Zuwei Yin and Jingao Xu at Tsinghua University. This book would not have been possible without their contributions.

During the past years, I have learned and benefited a lot from many professors. I would like to take this opportunity to record my gratitudes to them. I thank Prof. Mingyan Liu at University of Michigan, Ann Arbor, who offered freedom, trust, and valuable guidance during my visit in her group and provided helpful suggestions and comments on several of my research works. Thanks are also due to Prof. Jiannong Cao at Hong Kong Polytechnic University, who kindly provided me a short-term visit opportunity during my Ph.D. study. In particular, sincere thanks to Prof. Nicholas D. Lane at University of Oxford and Nokia Bell Labs for his kind support and advices on my research. I am also grateful to Prof. Junzhou Luo at Southeast University for his guidance and support in my academic career.

I thank Prof. Kyle Jamieson at Princeton University for kindly hosting a postdoc position. I am grateful to Prof. K. J. Ray Liu at University of Maryland, College Park for providing wonderful research environments.

I wish to express my gratitude to many colleagues, who worked closely with me and inspired me a lot on research: thanks to Kun Qian, Yue Zheng, Junjie Yin, Tianmeng Hang, Xu Wang, Dr. Xinglin Zhang, Dr. Wei Sun, Dr. Yiyang Zhao, Dr. Longfei Shangguan, Dr. Xiaolong Zheng, etc.

I would like to thank the editor Dr. Xiaolan Yao for the careful and considerable efforts in helping with the preparation and timely publication of this book.

Last but by no means least, I am deeply grateful to my family, including my grandmother, my parents, my wife, my brothers and sisters, for their unconditional support and understanding. I affectionately dedicate this book to them.

This book is supported in part by the National Natural Science Foundation of China (NSFC) under grants 61672319, 61522110, and 61632008.

College Park, USA

March 2018

Chenshu Wu

# Contents

# Part I Getting Started

# 1 Background and Overview 3

1.1 Wireless Indoor Localization 3   
1.2 State-of-the-Art Approaches . 4

1.2.1 Infrastructure 4   
1.2.2 General Architecture . 6   
1.2.3 Historical Stages 7

1.3 WiFi Fingerprint-Based Approach 8

1.3.1 General Frameworks 9   
1.3.2 Challenges for Ubiquitous Applications . 10

1.4 Book Organization 11

References . 12

# 2 Mobile Crowdsourcing and Inertial Sensing 17

2.1 Harnessing Crowdsourcing in Mobile Computing 17   
2.2 Embracing Mobility via Inertial Sensing. 18

2.2.1 Sensors Types 19   
2.2.2 Mobility Information 20

References . 26

# Part II Boosting Deployment: Making It Available

# 3 Radio Map Construction Without Site Survey . 33

3.1 Introduction. 33   
3.2 Related Work . 35   
3.3 Overview. 36

3.3.1 Data Collection. 36   
3.3.2 System Architecture 36

3.4 Stress-Free Floor Plan. 37

# 3.5 Fingerprint Space. 39

3.5.1 Fingerprint Collection 39   
3.5.2 Pre-processing. 40   
3.5.3 Fingerprint Space Construction 41

# 3.6 Mapping 42

3.6.1 Feature Extraction. 42   
3.6.2 Space Transformation. 45

# 3.7 Experiments 47

3.7.1 Experiment Design. 47   
3.7.2 Performance Evaluation 47

# 3.8 Conclusion . 55

# References . 55

# 4 Building Tomography: Automatic Floor Plan Generation 59

4.1 Introduction. 59   
4.2 Related Works 61   
4.3 System Overview . 62   
4.4 Trace Collection . 63

4.4.1 User Data Collection . 63   
4.4.2 Dead-Reckoning 64

# 4.5 Trace Realization 66

4.5.1 Entrance Discovery 66   
4.5.2 Reference Point Extraction 67   
4.5.3 Reference Point Matching . 68   
4.5.4 Drift Fixing . 69   
4.5.5 Multi-floor Case. 70

# 4.6 Map Generation 70

4.6.1 Space Regionalization 71   
4.6.2 Functionality Recognition 71

# 4.7 Experiments 75

4.7.1 Experiment Setup 75   
4.7.2 Reference Point Matching Performance 75   
4.7.3 Regionalization Performance . 76   
4.7.4 Functionality Recognition 78

# 4.8 Conclusion . 79

# References . 79

# Part III Facilitating Maintenance: Making It Sustainable

# 5 Adaptive Radio Map Updating 83

5.1 Introduction. 83   
5.2 Related Works 85   
5.3 Preliminaries and Measurements 86

5.3.1 Measurements of RSS Dynamics 86   
5.3.2 Radio Map Updating with Reference Points. 87

# 5.4 Overview. 88

5.5 Method Design . 90

5.5.1 Pin Data Collection 90

5.5.2 Reference Point Estimation. 93

5.5.3 Map Updating . 95

5.6 Implementations and Evaluation 98

5.6.1 Experimental Methodology. 98

5.6.2 Performance Evaluation 99

5.7 Discussions and Limitations 104

5.8 Conclusions. 105

References . 106

6 Self-Deployable Peer-to-Peer Navigation 109

6.1 Introduction. 109

6.2 Related Works . 112

6.3 Motivations and Challenges 113

6.3.1 Model Description 113

6.3.2 Usage Examples. 114

6.3.3 Design Challenges 115

6.4 Overview. 115

6.5 Fingeram Specification. 116

6.5.1 Definition and Generation 116

6.5.2 Radio Features 117

6.5.3 Visual Features . . 119

6.6 ppNav Design 120

6.6.1 Trace Generation . 120

6.6.2 Walking Progress Estimation . 121

6.6.3 Deviation Detection . 123

6.6.4 Path Locking-On . 126

6.7 Implementation and Experiments 128

6.7.1 Experimental Setup 128

6.7.2 Performance Evaluation 128

6.8 Discussion 134

6.9 Conclusion . 135

References . 135

# Part IV Enhancing Accuracy: Making It Reliable

7 Exploiting Spatial Awareness via Fingerprint Spatial Gradient ...... 139

7.1 Introduction. 139

7.2 Related Works . 141

7.3 ViVi Design. . 143

7.4 Understanding Fingerprint Spatial Gradient 144

7.4.1 Limitations of Existing RSS Fingerprints 144

7.4.2 Fingerprint Spatial Gradient . 147

7.5 Exploiting Fingerprint Spatial Gradient . 150

7.5.1 Profiling Fingerprint Spatial Gradient 150

7.5.2 Comparing Fingerprint Spatial Gradient . 154

7.6 Implementations and Evaluation 155

7.6.1 Experimental Methodology. 156

7.6.2 Performance Evaluation 157

7.7 Conclusions. 161

References . 161

# 8 Enhancing WiFi Fingerprinting with Visual Clues . 165

8.1 Introduction. 165

8.2 Related Works 167

8.3 Measurements and Observations 168

8.3.1 Measurements 168

8.3.2 Observations 169

8.4 System Overview . 170

8.4.1 Working Flow from User’s Perspective . 170

8.4.2 Working Flow from Server’s Perspective . 170

8.5 Image Processing Pipeline 171

8.5.1 Image Matching . 171

8.5.2 Relative Geometric Constraint Extraction 171

8.5.3 Supporting Photo Set Selection 173

8.6 WiFi Processing Pipeline 174

8.6.1 Device Calibration 175

8.6.2 WiFi Fingerprinting . 176

8.7 Joint Location Estimation . 177

8.7.1 Problem Formulation 178

8.7.2 Problem Hardness . 179

8.7.3 Two-Tier Shape Matching Heuristic 180

8.8 Evaluation 181

8.8.1 Experimental Methodology. 181

8.8.2 Micro Benchmarks . 182

8.8.3 Overall System Performance 184

8.8.4 Impacting Factors 185

8.9 Discussion 188

8.10 Conclusion . 189

References . 189

# 9 Mitigating Large Errors in Practice . 193

9.1 Introduction. 193

9.2 Related Works 195

9.3 Preliminary and Measurements 196

9.3.1 Problem Statement 196

9.3.2 Observations 197

9.4 Design Methodology 200

9.4.1 Phantom Fingerprints . 201   
9.4.2 Robust Fingerprinting. 204   
9.4.3 Discriminatory Policy. 205   
9.4.4 Localization 207

9.5 Experiments and Evaluation 207

9.5.1 Experimental Methodology. 207   
9.5.2 Performance Evaluation 209

9.6 Conclusions. 213

References . 213

# Part V Conclusions

10 Research Summary and Future Directions . 219

10.1 Research Summary 219   
10.2 Future Directions . 219

# Acronyms

AoA Angle of Arrival

AP Access Point

BLE Bluetooth Low Energy

CSI Channel State Information

FSG Fingerprint Spatial Gradient

FSM Finite State Machine

GPS Global Positioning System

IMU Inertial Measurement Unit

LOS Line of Sight

LDPL Log-Distance Path Loss

MDS Multi-dimensional Scaling

MEMS Micro Electro-Mechanical Systems

mmWave Millimeter Wave

MST Minimum Spanning Tree

PDR Pedestrian Dead Reckoning

PLSR Partial Least Squares Regression

RM Radio Map

RSG RSS Spatial Gradient

RSS Received Signal Strength

SLAM Simultaneous Localization and Mapping

ToA Time of Arrival

TDoA Time Difference of Arrival

# Part I

# Getting Started

Part I consists of two chapters presenting the basis of crowdsourcing-based wireless indoor localization systems. The first chapter introduces location-awareness applications, typical indoor localization systems and the state-of-the-art techniques and summaries the challenges of WiFi-based localization for ubiquitous applications. The second chapter includes the concepts of crowdsourcing and presents basis of mobility monitoring via smartphone sensing, which help readers understand the techniques before going over the subsequent chapters.

# TO INDOOR LOCALIZATION SYSTEMS:

The biggest thing I’ve learned is location.

– Roy Halladay

# Chapter 1 Background and Overview

![](images/614515fecb9d689c138b6064c3b190a6ae3e64a2ab3f9a6d69b9843778f94e35.jpg)

Abstract Location acts as the most important information that bridges the physical world and the cyber space and thus a key enabler for Cyber-Physical Systems (CPS). In this chapter, we first introduce why indoor localization technology is particularly needed and then review the state-of-the-art approaches. In the end, we outline the book structure.

# 1.1 Wireless Indoor Localization

The word “smart” becomes ubiquitous in the era of Internet of Things and big data. If you believe the hype, smart homes will analyze user behaviors in kitchen and bedrooms to improve in-home experience. Smart buildings will collect user trajectories for intelligent analytics to understand user behavior in buildings. Smart cities will monitor the realtime traffics on every street corner. Smart factories will track every robot and object in the facility and further every product they deliver in the coming Industry 4.0. Getting all these to work, however, necessities resolving locations of devices, sensors, machines, and people in the space.

Thanks to the Global Positioning System (GPS), and digital maps freely available online, a smartphone (or any GPS-equipped end devices) is the only thing one needs to pinpoint his/her own location anywhere on the Earth. GPS works by broadcasting precise time and position data using on-board synchronized atomic clocks, allowing a receiver to calculate its location by measuring signals from four or more satellites. Nowadays, GPS dominates the market of outdoor positioning and, together with the proliferation of mobile computing, has enabled a splendiferous paradigm of mobile Internet that profoundly revolutionized people’s life styles.

Unfortunately, GPS doesn’t work indoors. GPS satellite signals cannot penetrate modern building walls. And even in outdoor areas of metropolises like Manhattan and Hong Kong, GPS may not work properly due to the lack of clear Line-of-Sight (LOS) propagation since the satellite signals are also easily blocked by nearby buildings. To enable wireless localization indoors, where modern people spend more than 80% of their time, alternative technologies are needed.

# 1.2 State-of-the-Art Approaches

The past decades have witnessed the conceptualization and development of wireless indoor localization, with research and engineer efforts from both academy side and industry side. Various technologies have been proposed to enable a ubiquitous indoor positioning system.

# 1.2.1 Infrastructure

By now, different signals have been utilized, including WiFi, RFID, UWB, laser, visible light, acoustic signals, and magnetic, etc. We first briefly introduce some of the representative technology as follows.

WiFi-based WiFi-based solutions utilize existing WiFi infrastructure and have been studied since RADAR initialized a very early system [3]. After that, numerous efforts have been devoted to WiFi-based localization in the past decades, both from academic side [6, 7, 20, 40, 42, 49, 60, 62, 66, 70] and from industrial side [5, 9, 12, 19, 32, 58]. Thanks to the ubiquity in deployment of WiFi infrastructure and accessibility on off-the-shelf smartphone, WiFi-based approaches are treated as infrastructure-free and thus turn out to be the most attractive solution for ubiquitous indoor localization. This book mainly focuses on WiFi-based pervasive localization and we will detail its methodology, framework, advantages, and challenges in next section.

RFID-based RFID is an as popular solution to indoor location tracking. Early back to 2004, commercial active RFID tags (powered by a small battery) have been exploited for localization [34]. Recently, passive RFID tags that are battery-free and cheaper draw more attentions [1, 35, 43, 44, 50–52, 55, 67, 68]. With precise phase information available from commercial RFID reader, centimeter-level accuracy can be achieved for tracking [51, 67]. Although passive RFID tags are pretty cheap, the indispensable counterpart readers are quite expensive. And they are not likely to be available on smartphones. Furthermore, the tracking coverage is very limited due to weak backscatter signals from the tags and not suitable for ubiquitous scenarios.

Bluetooth-based Bluetooth, especially the recently released Bluetooth Low Energy (BLE) standard, has also been adopted as a promising approach for practical localization. Bluetooth-based approaches are particularly useful for logical localization, which identifies the room or retail store, rather than the absolute location a user presents. Cheap and energy-efficient BLE beacons are available to be deployed widely, each beacon covering a modest indoor area. By examining the detected beacon ID, one can figure out the location by a beacon or simply a smartphone. Beacons can also be deployed densely for accuracy and robustness gains. Due to limited accuracy, Bluetooth-based methods usually don’t appear as independent solutions, but are combined with other technology like WiFi.

mmWave-based Recently, the progress of millimeter wave (mmWave) communications also promotes its application in wireless tracking and sensing. Working on an ultra-high frequency baseband with ultra-wide bandwidth, mmWave provides the feasibility of an indoor radar with millimeter-level resolution in location tracking and motion sensing [25, 28, 36, 57, 78, 79]. Albeit promising, mmWave technology is still in its early phase and not yet widely available on commercial devices.

Sound-based The Bat [15] and Cricket [38] systems, developed more than 15 years ago, both employed ultrasound for localization with specialized transmitter and receiver devices. With higher computation resources on mobile devices like smartphones, sound-based localization becomes feasible on them. BeepBeep [37] and Guoguo [27] both use microphones and speakers equipped on smartphones for localization. ABS [47] enables room localization by extracting background sound as fingerprints. Recent innovations further enable ultrasonic signal transmission on commercial smartphones and achieve precise tracking, such as AAMouse[71], CAT [31], FingerIO [33], Strata [72], LLAP [54], etc. While audible sound based approaches are intrusive to humans, ultrasound-based methods mainly suits nearfield sensing.

Image-based There has been an increasing research interest in image-based localization with mobile phones, especially when computer vision technologies are more and more mature today. Camera-taken images are used for image matching or structure reconstruction or to extract Place-of-Interests (POIs, e.g., physical features or indoor landmarks like shop logos, statues, and billboards) [11, 30, 48, 64, 65, 74]. The major limitation, however, is that image-based methods usually rely on user cooperation to locate, thus not suitable for continuous back-end localization services.

Visible light positioning Another approach works with existing smartphones is to use visible light of light-emitting diodes (LEDs) that provide normal illumination but also invisible flicker in a unique pattern [22, 24, 41, 61, 69, 73]. Localization is achieved by identifying lamps using smartphone cameras. However most of previous proposals focus on using modulated LEDs as location landmarks and their real life deployment are largely prohibited by high deployment overhead and performance degradation in dynamic environments. A recent work [77] achieves high-precision visible light positioning using conventional LEDs and fluorescent lamps inside today’s buildings, shedding light on practical adoption of this kind of approaches.

Smartphone dead-reckoning Dead-reckoning is a well-known technology used in robot and drone navigation. It becomes applicable to modern smartphones as more and more motion-sensitive sensors including accelerometers and gyroscopes are equipped on today’s mobile phones. By tracking the distinctive motions of human walking, one is able to derive the direction and distance travelled, a common branch of dead-reckoning approaches named as Pedestrian Dead Reckoning (PDR) [4, 10, 13, 13, 14, 18, 23, 76]. Yet due to low resolutions of smartphones sensors, smartphone PDR usually suffer from large drifts and significant accumulative errors over long trajectories. As a result, smartphone dead-reckoning is often integrated with other approaches to improve performance.

Magnetism-based Magnetometer is another sensor on smartphones that is exploited for positioning purpose. The rationale is that modern steel-and-concrete buildings and various steely furnitures inside them disrupt Earth’s magnetic fields that vary subtly over different locations. These distorted magnetism may be measured by magnetometers on smartphones to determine their own locations [8, 17, 45, 46, 75]. Magnetism is a good indicator as it is easily scalable all over the world and is capable of providing location accuracy of less than two meters, as reported by IndoorAtlas [17], a start-up on geomagnetic hybrid indoor positioning technology, once a venue has been surveyed.

There are also many other signals used for localization, including FM signals, ultra-wide band signals, infrared, etc. In practice, a more common case is that multiple technologies are integrated into one system. For example, dead-reckoning almost always comes with other techniques [16, 40, 49]. BLE is often used as a supplementation to WiFi-based solutions, especially in real world systems. Imagebased and sound-based approaches can be combined with WiFi-based methods for better accuracy [26, 64]. While the independent research of each category continuous, a trend for practical systems will be systematic integration of orthogonal and supplementary technologies.

# 1.2.2 General Architecture

Whatever the infrastructure is used, a typical indoor positioning system usually follows the architecture as shown in Fig. 1.1, which consists of infrastructure installed in building, mobile clients, and a position engine. Depending on the specific infrastructure used, the localization clients could be either specialized or commodity hardware. The position engine is usually a cloud service, yet could also be a local server for certain local areas, or even directly the mobile device itself. The core localization algorithm is running on the position engine, which responses user requests and outputs user location, typically together with a digital map. The digital floor plan is not inelastic requirement of an indoor localization system, but has the added benefits of accuracy gain and semantic gain that transforms location coordinates into location contexts.

![](images/cfed5c71920af5b374d2d7610ba4cdc8a76320af28a79852a34ede88d02e47a9.jpg)



Fig. 1.1 A typical architecture of an indoor positioning system

Generally, localization methodologies are divided into two categories: ranging and fingerprinting. (1) Ranging-based algorithms follow the same principle as GPS. Location is determined by the well-known muiltilateration, i.e., calculating the distances (or directions) from the target to multiple anchors (at least three for 2D locations and four for 3D locations). Anchors are also called reference points, which are, e.g., satellites in GPS and Access Point (AP) in WiFi-based approaches. Distances and directions are usually estimated by Time-of-Arrival (ToA) [27, 63], Time-Difference-of-Arrival (TDoA) [37], Angle-of-Arrival (AoA) [20, 21, 62], and Doppler frequency shifts [39, 71], etc. It is also common, although inaccurate, to derive distances from Received Signal Strength (RSS), which is readily accessible on almost all RF radios such as WiFi, Bluetooth, GSM, etc. [7, 42]. Recent advances have exploited physical layer Channel State Information (CSI) for better resolution [20, 21, 62]. Nonetheless, ranging-based approach is more commonly used in acoustic signals and UWB signals that yield precise ranging estimates, yet less frequently in RF signals like WiFi because ranging will be vulnerable and erroneous due to low channel resolution and light speed propagation. (2) Alternatively, fingerprint-based approach is popular for RF signals. Instead of modeling signals and analyzing signal properties to derive distances and directions, fingerprintbased approach explores spatial diversity of signals over different locations and utilizes these distinctive signal patterns as location fingerprints. Such fingerprints are collected for each specific location and then location is determined through pattern matching. Here the fingerprint is not limited to features of RF signals like WiFi and Bluetooth [3, 40, 51, 66, 70], but can also be acoustic signals, images, magnetic fields, etc.

# 1.2.3 Historical Stages

From a historical view, the development of indoor localization roughly undergoes three themes, depending on what device a target user needs to carry on.

1. Sensor-based In its early stage, dedicated sensors are used for localization. Examples include Active Badge [56] and Bat [15], which were proposed around 1990s, using infrared and ultrasonic respectively. The Cricket location system [38] is another pioneering example based on ultrasound sensors. Not only sensors need to be installed in the building, users are required to carry these specialized devices in order to be located. These added ingredients prevent their wide adoption in ubiquitous applications. Yet thanks to their reliable and precise performance, they are valuable in special scenarios, especially critical industrial applications.

2. Smartphone-based The proliferation of mobile computing has promoted mobile phones as the most convenient handsets for ubiquitous localization. With powerful computation capability and various sensors equipped, modern smartphones are capable of running various localization approaches, e.g, WiFi-based, soundbased, image-based, dead-reckoning, etc. [23, 27, 65, 66]. In fact, smartphonebased indoor localization has been the most important theme during the past 10 years and, with smartphone ownership continuously rising, will stand to be the most promising solution in the future.

3. Sensorless Recently, the progresses of wireless communications enable a new paradigm of passive (a.k.a, sensorless, or device-free) localization, where no additional devices are attached to or carried by a user. The key idea is to capture RF or acoustic signals reflected by human motions and derive the information of interests therein [2, 39, 52, 53]. Different from device-based approaches, sensorless localization is especially useful to scenarios like security monitoring, elder care, and in-air interaction, where users are not likely to carry any device for localization.

Each of the three themes has its own advantages and is suitable to different scenarios. For example, industry-level products would prefer sensor-based approaches while ubiquitous applications demand smartphone-based solutions. And indeed the research community is witnessing a concurrent progress of three themes. Different from GPS that dominates outdoor positioning, there will always be multiple competitive technologies in the community of indoor localization, each serving different applications with diverse requirements. In this book, we mainly focus on WiFi fingerprint-based approaches for smartphones.

# 1.3 WiFi Fingerprint-Based Approach

The ideal indoor-location technology for ubiquitous applications would be one that requires no additional hardware to be installed in buildings or added to mobile phones. A promising approach towards this goal is to use widely existing WiFi signals. WiFi-based approach is known to be free of extra infrastructure and specialized hardware. On one hand, WiFi hotspots have been deployed in modern buildings all over the worlds, not only homes and office buildings but also the most common places where people get lost: airports, malls and city centers. On the other hand, smartphones already have the WiFi radio to receive the wireless signals and can readily be used as the localization devices. In addition to a large number of research papers, great companies including Google, Apple, Cisco, Huawei, and Baidu etc. have all built or invested and are still developing related products, using WiFi as infrastructure and smartphones as clients.

As aforementioned, there are also ranging-based and fingerprint-based methods in WiFi-based solutions. However, RSS-based ranging is erroneous, usually producing location error of 5 m to >10 m [7, 26, 29]. Better precision could be achieved by resorting to physical layer CSI, which is however, currently not accessible on most commercial WiFi devices, not to mention smartphones [20, 59, 62]. In the contrast, WiFi fingerprint-based approach has become the mainstream, drawing a lot of attention from both research community and industries.

# 1.3.1 General Frameworks

The rationale behind WiFi fingerprint-based positioning is straight-forward. A mobile device, at somewhere covered by WiFi signal, records the hearable WiFi APs and their corresponding signal strength as the radio signal characteristics (i.e. signal fingerprint) for this specific position. Such a fingerprint, as a location query, is further sent to a location service provider who has a WiFi fingerprint database of a great amount of fingerprints collected at every position within an area of interest. The location service provider then retrieves the database for the most similar fingerprint with respect to the location query, and returns its corresponding recorded location as the location estimation. The uniqueness of WiFi APs (in terms of the MAC addresses) and the signal attenuation across space underlie the principle of WiFi positioning.

From the systematic aspect, WiFi fingerprint-based systems typically consist of two phases: a training phase and a localization phase as illustrated in Fig. 1.2. In the first training phase, fingerprints are collected with known location labels to form a fingerprint database (a.k.a radio map). Conventionally, the training procedure is also known as site survey, which is labour-intensive and time-consuming. Then during the localization stage, user location is determined by matching fingerprint observation against those stored in the fingerprint database.

Formally, the area of interests is sampled as a discrete location space $L \ =$ $\{ l _ { 1 } , l _ { 2 } , \cdots , l _ { n } \}$ where n is the amount of sample locations. For each location $\mathbf { \xi } _ { l _ { i } }$ with coordinates $( x _ { i } , y _ { i } )$ , a corresponding fingerprint is denoted as $\begin{array} { r l } { \boldsymbol { f } _ { i } } & { { } = } \end{array}$ $\{ f _ { i 1 } , f _ { i 2 } , \cdot \cdot \cdot , f _ { i m } \} , 1 \le j \le m$ , where $f _ { i j }$ denotes the mean RSS value (or the RSS distribution in probabilistic algorithms [70]) of the jth AP and m is the total number of APs in the targeted location space. All fingerprints form a fingerprint space $F = \{ f _ { 1 } , f _ { 2 } , \cdot \cdot \cdot , f _ { n } \}$ , corresponding to the location space L. The radio map consists of $< l _ { i } , f _ { i } >$ terms that associate a location $\mathbf { \xi } _ { l _ { i } }$ with a fingerprint $f _ { i }$ . Then location estimation is conducted by retrieving the best match of a query fingerprint f against the whole fingerprint space F , using some specific fingerprint similarity measures such as Euclidean distance. The location $l ^ { * }$ associated with the best matched fingerprint $f ^ { * }$ is then returned as the user’s location estimation.

![](images/19b9935d62cb36bb9d847a225868e962226213c378b74e5d95eedfde05f2471e.jpg)



Fig. 1.2 A common framework of WiFi fingerprint-based localization

# 1.3.2 Challenges for Ubiquitous Applications

WiFi fingerprint-based technology is promising to render a ubiquitous indoorlocation solution that requires no additional hardware. To deliver a truly ubiquitous system, three goals need to be further realized: the systems should be easily deployed at a large scale and run over long terms, with considerable location accuracy. However, several challenges need to be addressed towards these goals.

Deployment costs The procedure of site survey is time-consuming and laborintensive. However, it is inevitable for fingerprint-based approaches, since they require a fingerprint database storing location associated fingerprints from onsite records. The indoor mapping services of Google Map 6.0 was available only at selected airports and shopping malls in several districts at its release time. Later, Google has already surveyed over 10,000 venues, mostly in America, while Nokia has covered more than 5,100 venues in 40 countries. Apple and Baidu are carrying out similar efforts. But it is no small undertaking, because the survey needs to be conducted by professional engineers with specialized devices. Its scalability to broader areas is strangled by the limited quantity and granularity of fingerprint data of building interiors. The world-wide adoption of indoor positioning calls for low deployment costs.

• Maintenance efforts Signal strengths are sensitive to environmental dynamics, either caused by moving subjects or furniture changes. Dense multipath in complex indoor environments exaggerates the RSS temporal fluctuations. Realtime RSS samples measured in localization phase could drastically deviate from those stored in the initial radio map. A static radio map may gradually deteriorate or even break down, especially over long-term deployment, leading to grossly inaccurate location estimation. Regularly repeating the site survey would help overcome the problem, which is, however, too costly in practice. Lightweight automatic updating of fingerprints is needed to allow long-term running of indoor localization service.

• Location errors The indoor attenuation of wireless signals is extraordinarily unpredictable because of complex environmental factors, leading to decreased performance of widely used signal models. For instance, multi-path fading brings about strenuous fluctuation on signal amplitudes in small scale of only several centimeters. Besides, environmental dynamics (such as human movements, door opening and closing, and furniture rearrangement) can also change the signal strength distribution across an area. To make things worse, some researchers observe experimentally that two far-away locations in an open indoor space may have similar signal fingerprints, which, according to the scheme of WiFi positioning, may induce incorrect location estimation. Existing works based on RSS frequency produce location errors up to 5 m or more, still a gap from the accuracy of 1 or 2 m demanded by most of applications.

The research presented in this book aims to tackle the above three issues. The ultimate goal is to shape a WiFi fingerprint-based technology for ubiquitous scenarios, allowing it to be easily deployable over world-wide buildings, and be accurate over long-term running.

# 1.4 Book Organization

Based on in-depth understanding of WiFi signals and smartphone capabilities, we attempt to overcome the drawbacks of previous WiFi fingerprinting from a crowdsourcing perspective, in the hope of achieving performance gains without the pains of adding additional hardware to be installed in building or attached to users.

Our research is promoted by the progress of mobile computing and inspired by the concept of crowdsourcing. As shown in Fig. 1.3, we employ mobile crowdsourcing to solve the three key problems of radio map construction and updating and low location accuracy. In particular, we present the design, implementation and experimental evaluation of a set of novel techniques to eliminate the need of manual site survey for radio map construction, dynamically adapt the radio maps to environmental changes, and achieve considerable accuracy, together enabling a ubiquitous fingerprint-based solution for practical applications.

The main body of this book is organized in five parts, which further include 11 chapters in total. Part I presents an overview of the book and introduces the background on wireless indoor localization (Chap. 1), mobile crowdsourcing and mobile sensing (Chap. 2).

![](images/19fcf6fc5d180c19d785078ff00230a7729ee862073fa32562046e1bc2c4908b.jpg)



Fig. 1.3 An overview of the book content

Part II illustrates how to boost the deployment of indoor positioning systems by reducing the deployment costs. Inspired by mobile crowdsourcing, we design LiFS that eliminates site survey efforts of radio map construction in Chap. 3. Further, we discuss how to generate digital floorplans via crowdsourcing in Chap. 4.

Part III discusses how to facilitate maintenance of indoor positioning services over long-term running. We first introduce AcMu that enables adaptive updating of constructed radio maps to combat temporal environmental dynamics in Chap. 5. Then we present a different design in Chap. 6, which forgoes the design of radio map and resorts to a peer-to-peer manner of navigation, without the need of a prior calibrated radio map.

Part IV introduces several techniques to enhance location accuracy in WiFi fingerprinting. In Chap. 7, we built a novel form of signal feature on top of traditional RSS fingerprints that leverages spatial awareness for more reliable and accurate performance. Further, we incorporate image-based techniques to augment WiFi fingerprinting in Chap. 8. Finally, we show some observations on location errors from our real-world deployment experience and present techniques to address them in Chap. 9.

Finally, in Part V, we conclude this book with a summary of the presented research and discuss the future research directions in Chap. 10.

# References

1. Abari, O., Vasisht, D., Katabi, D., Chandrakasan, A.: Caraoke: an e-toll transponder network for smart cities. In: Proceedings of ACM SIGCOMM (2015)   
2. Adib, F., Katabi, D.: See through walls with WiFi! In: Proceedings of the ACM SIGCOMM, SIGCOMM ’13 (2013)   
3. Bahl, P., Padmanabhan, V.N.: RADAR: an in-building RF-based user location and tracking system. In: Annual Joint Conference of the IEEE Computer and Communications Societies (INFOCOM) (2000)   
4. Brajdic, A., Harle, R.: Walk detection and step counting on unconstrained smartphones. In: ACM International Conference on Ubiquitous Computing (UbiComp) (2013)   
5. Broadcom: Broadcom enables pinpoint indoor location technology with latest 5G WiFi SoC. http://www.broadcom.com/press/release.php?id=s836818 (2014)   
6. Chen, Y., Yang, Q., Yin, J., Chai, X.: Power-efficient access-point selection for indoor location estimation. IEEE Trans. Knowl. Data Eng. 18(7), 877–888 (2006)   
7. Chintalapudi, K., Padmanabha Iyer, A., Padmanabhan, V.N.: Indoor localization without the pain. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2010)   
8. Chung, J., Donahoe, M., Schmandt, C., Kim, I.J., Razavai, P., Wiseman, M.: Indoor location sensing using geo-magnetism. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys), pp. 141–154 (2011)   
9. Cisco Systems: Wi-fi location-based services 4.1 design guide. https://www.cisco.com/c/en/us/ td/docs/solutions/Enterprise/Mobility/WiFiLBS-DG.html (2013)   
10. Constandache, I., Choudhury, R., Rhee, I.: Towards mobile phone localization without wardriving. In: IEEE International Conference on Computer Communications (INFOCOM) (2010)

11. Dong, J., Xiao, Y., Noreikis, M., Ou, Z., Ylä-Jääski, A.: iMoon: using smartphones for image-based indoor navigation. In: Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems, pp. 85–97. ACM, New York (2015)   
12. Ekahau: WiFi design tools. http://www.ekahau.com/ (2015)   
13. Goyal, P., Ribeiro, V., Saran, H., Kumar, A.: Strap-down pedestrian dead-reckoning system. In: International Conference on Indoor Positioning and Indoor Navigation (IPIN) (2011)   
14. Harle, R.: A survey of indoor inertial positioning systems for pedestrians. IEEE Commun. Surv. Tutorials 15(3), 1281–1293 (2013)   
15. Harter, A., Hopper, A., Steggles, P., Ward, A., Webster, P.: The anatomy of a context-aware application. In: ACM/IEEE International Conference on Mobile Computing and Networking (MobiCom) (1999)   
16. Hilsenbeck, S., Bobkov, D., Schroth, G., Huitl, R., Steinbach, E.: Graph-based data fusion of pedometer and WiFi measurements for mobile indoor positioning. In: ACM International Conference on Ubiquitous Computing (UbiComp) (2014)   
17. IndoorAtlas: IndoorAtlas. http://www.indooratlas.com/ (2015)   
18. Jimenez, A., Seco, F., Prieto, C., Guevara, J.: A comparison of pedestrian dead-reckoning algorithms using a low-cost MEMS IMU. In: IEEE International Symposium on Intelligent Signal Processing (WISP) (2009)   
19. Kimmo, K.: Bringing Navigation Indoors: The Way We Live Next 2008. Nokia Research Center (2008)   
20. Kotaru, M., Joshi, K., Bharadia, D., Katti, S.: Spotfi: decimeter level localization using WiFi. In: Proceedings of ACM SIGCOMM (2015)   
21. Kumar, S., Gil, S., Katabi, D., Rus, D.: Accurate indoor localization with zero start-up cost. In: Proceedings of the 20th Annual International Conference on Mobile Computing and Networking, pp. 483–494. ACM, New York (2014)   
22. Kuo, Y.S., Pannuto, P., Hsiao, K.J., Dutta, P.: Luxapose: indoor positioning with mobile phones and visible light. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2014)   
23. Li, F., Zhao, C., Ding, G., Gong, J., Liu, C., Zhao, F.: A reliable and accurate indoor localization method using phone inertial sensors. In: ACM International Conference on Ubiquitous Computing (UbiComp) (2012)   
24. Li, L., Hu, P., Peng, C., Shen, G., Zhao, F.: Epsilon: a visible light based positioning system. In: USENIX Conference on Networked Systems Design and Implementation (NSDI) (2014)   
25. Lien, J., Gillian, N., Karagozler, M.E., Amihood, P., Schwesig, C., Olson, E., Raja, H., Poupyrev, I.: Soli: Ubiquitous gesture sensing with millimeter wave radar. ACM Trans. Graph. (TOG) 35(4), 142 (2016)   
26. Liu, H., Gan, Y., Yang, J., Sidhom, S., Wang, Y., Chen, Y., Ye, F.: Push the limit of WiFi based localization for smartphones. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2012)   
27. Liu, K., Liu, X., Li, X.: Guoguo: enabling fine-grained indoor localization via smartphone. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2013)   
28. Loch, A., Assasa, H., Palacios, J., Widmer, J., Suys, H., Debaillie, B.: Zero overhead device tracking in 60 ghz wireless networks using multi-lobe beam patterns. In: ACM CoNext (2017)   
29. Lymberopoulos, D., Liu, J., Yang, X., Choudhury, R.R., Handziski, V., Sen, S., Lemic, F., Buesch, J., Jiang, Z., Zou, H., Jiang, H., Zhang, C., Ashok, A., Xu, C., Lazik, P., Rajagopal, N., Rowe, A., Ghose, A., Ahmed, N., Xiao, Z., Wen, H., Abrudan, T.E., Markham, A., Schmid, T., Lee, D., Klepal, M., Beder, C., Nikodem, M., Szymczak, S., Hoffmann, P., Selavo, L., Giustiniano, D., Lenders, V., Rea, M., Marcaletti, A., Laoudias, C., Zeinalipour-Yazti, D., Tsai, Y.K., Bestmann, A., Reimann, R., Li, L., Zhao, C., Adler, S., Schmitt, S., Dentamaro, V., Colucci, D., Ambrosini, P., Ferraz, A., Martins, L., Bello, P., Alvino, A., Sark, V., Pirkl, G., Hevesi, P.: A realistic evaluation and comparison of indoor location technologies: experiences and lessons learned. In: ACM/IEEE Conference on Information Processing in Sensor Networks (IPSN) (2015)

30. Manweiler, J.G., Jain, P., Roy Choudhury, R.: Satellites in our pockets: an object positioning system using smartphones. In: Proceedings of the 10th International Conference on Mobile Systems, Applications, and Services, pp. 211–224. ACM, New York (2012)   
31. Mao, W., He, J., Qiu, L.: Cat: high-precision acoustic motion tracking. In: Proceedings of the 22nd Annual International Conference on Mobile Computing and Networking, pp. 69–81. ACM, New York (2016)   
32. Meridian: Indoor GPS. http://meridianapps.com/ (2015)   
33. Nandakumar, R., Iyer, V., Tan, D., Gollakota, S.: Fingerio: using active sonar for fine-grained finger tracking. In: Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems, pp. 1515–1525. ACM, New York (2016)   
34. Ni, L.M., Liu, Y., Lau, Y.C., Patil, A.P.: LANDMARC: indoor location sensing using active RFID. Wirel. Netw. 10(6), 701–710 (2004)   
35. Ni, L.M., Zhang, D., Souryal, M.R.: RFID-based localization and tracking technologies. IEEE Wirel. Commun. 18(2), 45–51 (2011)   
36. Palacios, J., Casari, P., Widmer, J.: Jade: zero-knowledge device localization and environment mapping for millimeter wave systems. In: INFOCOM 2017-IEEE Conference on Computer Communications, IEEE, pp. 1–9. IEEE, Piscataway (2017)   
37. Peng, C., Shen, G., Zhang, Y., Li, Y., Tan, K.: BeepBeep: a high accuracy acoustic ranging system using COTS mobile devices. In: ACM International Conference on Embedded Network Sensor Systems (SenSys), pp. 1–14 (2007)   
38. Priyantha, N.B., Chakraborty, A., Balakrishnan, H.: The cricket location-support system. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2000)   
39. Qian, K., Wu, C., Yang, Z., Liu, Y., Jamieson, K.: Widar: decimeter-level passive tracking via velocity monitoring with commodity wi-fi. In: Proceedings of the 18th ACM International Symposium on Mobile Ad Hoc Networking and Computing, p. 6. ACM, New York (2017)   
40. Rai, A., Chintalapudi, K.K., Padmanabhan, V.N., Sen, R.: Zee: zero-effort crowdsourcing for indoor localization. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2012)   
41. Rajagopal, N., Lazik, P., Rowe, A.: Visual light landmarks for mobile devices. In: Proceedings of the 13th International Symposium on Information Processing in Sensor Networks, pp. 249– 260. IEEE Press, Piscataway (2014)   
42. Sen, S., Lee, J., Kim, K.H., Congdon, P.: Avoiding multipath to revive inbuilding WiFi localization. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys), pp. 249–262 (2013)   
43. Shangguan, L., Jamieson, K.: The design and implementation of a mobile RFID tag sorting robot. In: Proceedings of the 14th Annual International Conference on Mobile Systems, Applications, and Services, pp. 31–42. ACM (2016)   
44. Shangguan, L., Li, Z., Yang, Z., Li, M., Liu, Y., Han, J.: Otrack: towards order tracking for tags in mobile RFID systems. IEEE Trans. Parallel Distrib. Syst. 25(8), 2114–2125 (2014)   
45. Shu, Y., Bo, C., Shen, G., Zhao, C., Li, L., Zhao, F.: Magicol: indoor localization using pervasive magnetic field and opportunistic WiFi sensing. IEEE J. Sel. Areas Commun. 33(7), 1443–1457 (2015)   
46. Subbu, K.P., Gozick, B., Dantu, R.: Locateme: magnetic-fields-based indoor localization using smartphones. ACM Trans. Intell. Syst. Technol. (TIST) 4(4), 73 (2013)   
47. Tarzia, S.P., Dinda, P.A., Dick, R.P., Memik, G.: Indoor localization without infrastructure using the acoustic background spectrum. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys), pp. 155–168 (2011)   
48. Tian, Y., Gao, R., Bian, K., Ye, F., Wang, T., Wang, Y., Li, X.: Towards ubiquitous indoor localization service leveraging environmental physical features. In: Proceedings IEEE INFOCOM, pp. 55–63. IEEE, Piscataway (2014)   
49. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2012)

50. Wang, J., Adib, F., Knepper, R., Katabi, D., Rus, D.: RF-compass: robot object manipulation using RFIDs. In: Proceedings of the 19th Annual International Conference on Mobile Computing & Networking, pp. 3–14. ACM, New York (2013)   
51. Wang, J., Katabi, D.: Dude, where’s my card?: RFID positioning that works with multipath and non-line of sight. In: ACM SIGCOMM, pp. 51–62 (2013)   
52. Wang, J., Vasisht, D., Katabi, D.: RF-IDraw: virtual touch screen in the air using RF signals. In: Proceedings of ACM SIGCOMM (2014)   
53. Wang, W., Liu, A.X., Shahzad, M., Ling, K., Lu, S.: Understanding and modeling of WiFi signal based human activity recognition. In: Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, pp. 65–76. ACM, New York (2015)   
54. Wang, W., Liu, A.X., Sun, K.: Device-free gesture tracking using acoustic signals. In: Proceedings of the 22nd Annual International Conference on Mobile Computing and Networking, pp. 82–94. ACM, New York (2016)   
55. Wang, J., Xiong, J., Jiang, H., Chen, X., Fang, D.: D-watch: embracing “bad” multipaths for device-free localization with cots RFID devices. IEEE/ACM Trans. Netw. 25(6), 3559–3572 (2017)   
56. Want, R., Hopper, A., Falco, V., Gibbons, J.: The active badge location system. ACM Trans. Inf. Syst. 10(1), 91–102 (1992)   
57. Wei, T., Zhang, X.: mtrack: high-precision passive tracking using millimeter wave radios. In: Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, pp. 117–129. ACM, New York (2015)   
58. Wireless, O.: Smart radios for smart life. http://www.originwireless.net (2017)   
59. Wu, K., Xiao, J., Yi, Y., Gao, M., Ni, L.: FILA: fine-grained indoor localization. In: IEEE International Conference on Computer Communications (INFOCOM), pp. 2210–2218 (2012)   
60. Wu, Z.H., Han, Y., Chen, Y., Liu, K.R.: A time-reversal paradigm for indoor positioning system. IEEE Trans. Veh. Technol. 64(4), 1331–1339 (2015)   
61. Xie, B., Tan, G., He, T.: Spinlight: a high accuracy and robust light positioning system for indoor applications. In: Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems, pp. 211–223. ACM, New York (2015)   
62. Xiong, J., Jamieson, K.: Arraytrack: a fine-grained indoor location system. In: Usenix NSDI. Usenix (2013)   
63. Xiong, J., Sundaresan, K., Jamieson, K.: Tonetrack: leveraging frequency-agile radios for timebased indoor wireless localization. In: Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, pp. 537–549. ACM, New York (2015)   
64. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Enhancing WiFi-based localization with visual clues. In: Proceedings of the 2015 ACM International Joint Conference on Pervasive and Ubiquitous Computing, pp. 963–974. ACM, New York (2015)   
65. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Indoor localization via multi-modal sensing on smartphones. In: Proceedings of the 2016 ACM International Joint Conference on Pervasive and Ubiquitous Computing, pp. 208–219. ACM, New York (2016)   
66. Yang, Z., Wu, C., Liu, Y.: Locating in fingerprint space: wireless indoor localization with little human intervention. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2012)   
67. Yang, L., Chen, Y., Li, X.Y., Xiao, C., Li, M., Liu, Y.: Tagoram: real-time tracking of mobile RFID tags to high precision using cots devices. In: Proceedings of the 20th Annual International Conference on Mobile Computing and Networking, pp. 237–248. ACM, New York (2014)   
68. Yang, L., Lin, Q., Li, X., Liu, T., Liu, Y.: See through walls with cots RFID system! In: Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, pp. 487–499. ACM, New York (2015)   
69. Yang, Z., Wang, Z., Zhang, J., Huang, C., Zhang, Q.: Wearables can afford: light-weight indoor positioning with visible light. In: Proceedings of the 13th Annual International Conference on Mobile Systems, Applications, and Services, pp. 317–330. ACM, New York (2015)

70. Youssef, M., Agrawala, A.: The Horus WLAN location determination system. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2005)   
71. Yun, S., Chen, Y.C., Qiu, L.: Turning a mobile device into a mouse in the air. In: Proceedings of the 13th Annual International Conference on Mobile Systems, Applications, and Services, pp. 15–29. ACM, New York (2015)   
72. Yun, S., Chen, Y.C., Zheng, H., Qiu, L., Mao, W.: Strata: fine-grained acoustic-based devicefree tracking. In: Proceedings of the 15th Annual International Conference on Mobile Systems, Applications, and Services, pp. 15–28. ACM, New York (2017)   
73. Zhang, C., Zhang, X.: Litell: robust indoor localization using unmodified light fixtures. In: Proceedings of the 22nd Annual International Conference on Mobile Computing and Networking, pp. 230–242. ACM, New York (2016)   
74. Zheng, Y., Shen, G., Li, L., Zhao, C., Li, M., Zhao, F.: Travi-navi: self-deployable indoor navigation system. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2014)   
75. Zhou, P., Zheng, Y., Li, Z., Li, M., Shen, G.: IODetector: a generic service for indoor outdoor detection. In: ACM International Conference on Embedded Network Sensor Systems (SenSys) (2012)   
76. Zhou, P., Li, M., Shen, G.: Use it free: instantly knowing your phone attitude. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2014)   
77. Zhu, S., Zhang, X.: Enabling high-precision visible light localization in today’s buildings. In: Proceedings of the 15th Annual International Conference on Mobile Systems, Applications, and Services, pp. 96–108. ACM, New York (2017)   
78. Zhu, Y., Zhu, Y., Zhao, B.Y., Zheng, H.: Reusing 60ghz radios for mobile radar imaging. In: Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, MobiCom ’15 (2015)   
79. Zhu, Y., Yao, Y., Zhao, B.Y., Zheng, H.: Object recognition and navigation using a single networking device. In: Proceedings of the 15th Annual International Conference on Mobile Systems, Applications, and Services, MobiSys ’17 (2017)

# Chapter 2 Mobile Crowdsourcing and Inertial Sensing

![](images/efd4932a7a18fe12b14c9cb1b2e24bbb9da3e9a245252cbb52238fd2a2a946a9.jpg)

Abstract This chapter presents the preliminary background on mobile crowdsourcing and inertial sensing, which together have opened the new possibilities for wireless indoor localization, after more than a decade of development. In particular, we first introduce the basic concept of mobile crowdsourcing. Then we study how to measure human mobility using smartphone-based inertial sensing, including what types of sensors we can use and what mobility information we can acquire.

# 2.1 Harnessing Crowdsourcing in Mobile Computing

Mobile crowdsourcing is a recently developed concept in mobile computing area. A large number of mobile users act as basic sensing unit through their mobile phones, pads, and wearables and contribute sensing data via mobile Internet, accomplishing large-scale complicated sensing tasks collectively and cooperatively.

The term crowdsourcing is coined outside computer science area by “Wired” in 2006 to describe a new type of decentralized organization form [22], which sources tasks traditionally performed by specific individuals to a group of people or community (crowd) through an open call. The concept then becomes popular in computing area, attracting research efforts from IoT, data mining, and machine learning areas and fostering a wide range of applications in transportation monitoring [68, 69], map updating [55], network monitoring [10], privacy protection [2], video management [21, 47], etc. Wikipedia1 is one of the best known examples: thousands of Wikipedia users have created a remarkable encyclopedia. Other examples include SETI@home [29] and reCAPTCHA [51]. There are extensive research from different areas on crowdsourcing itself and its applications [13–15, 27, 63, 67]. Interested readers can refer to the literature for more in-depth materials.

The core idea of mobile crowdsourcing is to leverage the collective intelligence of numerous mobile users to resolve complicated sensing and computing tasks that can only be accomplished previously by professionals with significant efforts. For example, SignalGuru leverages mobile phones for collaborative traffic signal schedule advisory [30]. APPJOY automatically rates apps (mobile phone applications) according to aggregated use habits from a large group of users [62]. Crowdsourcing is usually achieved in a “passive” manner, which means the participated users do not need to intentionally cooperate, but merely contribute automatically gathered sensing data, implicitly and unconsciously. Conceptually, crowdsourcing is similar to related terms such as crowd computing, participatory sensing, social sensing, etc. and are sometimes interchangeably used in the literature.

In our research, we focus on how to harness the crowdsourcing power of mobile users for indoor localization. In particularly, borrowing crowdsourcing would help ease the cumbersome radio map construction and digital floorplan generation. Pioneer works including LiFS [64], UnLoc [52], Zee [39], Jigsaw [16] have explored the possibility and exploited the benefits. Regarding industry products, Google and Skyhook Wireless, a mobile location services company based in Boston, are experimenting with crowdsourcing indoor maps and global WiFi data. Particularly, a key enabler for mobile crowdsourcing in indoor localization is the increasingly growing capability of mobile devices, as described in the following section.

# 2.2 Embracing Mobility via Inertial Sensing

Modern smartphones have been equipped with a number of sensors, which make smartphones not only a communication tool, but also a sensing device. A typical smartphone is equipped with various types of sensors (including microphone, camera, proximity sensor, GPS, accelerometer, gyroscope, compass, etc.), through which sound, image, video, location, and mobility information can be measured by phones.

Recently, an increasing number of researchers realize that mobility information, as a new dimension in addition to wireless signals, can be employed to deal with the challenges of WiFi-based localization and consequently upgrade indoor positioning to a higher level [12, 39, 48, 52, 60, 64]. It is easy to understand that being aware of mobility could benefit localization, since location and mobility are by nature related in physical world. The current location of a moving object depends on both its past location and its movements.

In this section, we review the topic of mobility monitoring via inertial sensing based on smartphone sensors, which underlies our research proposals for WiFibased localization in this book.

Note that both inertial sensing and pedestrian dead reckoning (PDR) themselves are hot research topics. While we present a comprehensive review in the subsequent sections for interested readers to get a good understanding of user mobility monitoring, not all of the reviewed techniques will be involved in our research. Readers can skip this part and directly go to following chapters, in each of which we will also cover basic descriptions of inertial sensing techniques used, if necessary.

# 2.2.1 Sensors Types

Among various sensors, inertial measurement unit (IMUs) are one of the most widely adopted to measure mobility. An IMU is an electronic device that measures velocity, orientation, and gravity, and often constitutes of accelerometers and gyroscopes, and magnetometers. IMUs are primarily designed for inertial navigation systems of aircraft, spacecraft, watercraft, and guided missiles by means of dead reckoning, which calculates one’s current position by using a previously determined position, and advancing that position based upon estimated speeds and moving directions.

Modern smartphones are equipped with increasingly powerful sensors of various types at low costs, depending on which novel applications are rising in response. Constrained by cost, size, and power consumption of sensors, however, smartphone IMUs have their own unique characteristics.

Accelerometers An accelerometer is an infrastructure to measure acceleration, which works as “a damped mass on a spring” [57] leveraging Newton’s laws of motion. Modern accelerometers are usually micro electro-mechanical systems (MEMS), and in fact “the simplest MEMS devices possible” [57]. The SI unit of acceleration is meters per second squared $( \mathrm { m } / \mathrm { s } ^ { 2 } )$ , or popularly in terms of g-force (g). In practice, it also requires local gravity to calculate the actual acceleration value w.r.t. the Earth. The value of local gravity can be obtained by device calibration at rest or gravity modeling given the current position [57].

Gyroscopes A gyroscope is an instrument to measure or maintain orientation in principle of angular momentum [58]. It is mechanically “a spinning wheel or disc in which the axle is free to assume any orientation” [58]. Besides applications in general navigation, gyroscopes are often exploited in conjunction with accelerometers to derive robust direction information (e.g. X-, Y-, Z-axis acceleration with the extent and rate of rotation in roll, pitch, and yaw, [58]).

Magnetometers A magnetometer (or magnetic field sensor), is a device that measures the strength and the direction of magnetic fields [59]. The types of magnetometers vary. Magnetoresistive sensors and Hall effect devices are the most popular, yet there is also a huge dispute, both technically and commercially, on the use of the two for consumer devices.

In terms of performance, IMUs are qualified to a large number of services, such as linking movements of the user’s wrist, arm, and hand to applications, navigation with and between pages, the movements of characters in a game, etc. However, researchers and app developers complain the accuracy of smartphone IMUs is insufficient for dead reckoning and other location-based services. In fact, compared with the generally believed accurate IMUs used in Unmanned Aerial Vehicle (UAV) and other industrial application, the smartphone IMUs possess the same or similar core sensing component, but differ in sensor screening, installation error calibration, cross axis error calibration, zero point correction, temperature drift compensation, etc. For instance, ADI’s ADIS16405 and ADIS16400 are based on the same ADI’s low cost sensing elements, but the former is more expensive than the latter. The only two major differences are the bias temperature coefficient and sensitivity temperature coefficient. ADIS16405 is carefully calibrated in various temperatures ranging from −40 to $8 5 ^ { \circ } \mathrm { C } ,$ resulting in an increased cost on testing.

The reduced factory-calibration efforts contribute to the low cost of smartphone IMUs. As gyroscopes have experienced a dramatic drop in cost, the cost of IMUs is basically acceptable by mainstream smartphones. Yet researchers have to avoid the direct use of dead reckoning with low cost sensors, and resort to pedestrian motion modeling for accurate mobility measurements. And with advances in sensor design and manufacturing, the role of mobile devices is expanded beyond a sensor of physical environments, to an actuator that adapts its behaviors accordingly.

# 2.2.2 Mobility Information

The rich inertial sensing modalities on smartphones report numerous instantaneous motion measurements, such as acceleration, angular velocity and absolute direction, via built-in accelerometer, gyroscope and compass, respectively. To assist indoor localization and navigation, these low level physical displacement and directional measurements are integrated over time and augmented with location context into more complex human mobility information, such as walking steps, trajectories, locomotion modalities (e.g., walking and running), virtual landmarks (e.g., stairs and lifts), etc. Figure 2.1 illustrates a typical scenario of indoor inertial sensing as well as types of mobility information derivable from phone sensors. However, assembling human mobility information from phone sensory data is an endeavor fraught with obstacles. We briefly summarize them into three aspects:

• Noisy sensor measurements It is inevitable to induce noise in raw sensory measurements. When integrating these physical measurements over time, even small errors may drift dramatically. For instance, errors accumulate quadratically when derive displacement by twice integrating acceleration.

![](images/6a1d570369b297f38bafbfa7292cb0d1831bb17ada6158ec0ee6ba81993d7c15.jpg)



Fig. 2.1 An illustration of human mobility information derivable from phone sensors

• Unconstrained phone placement Since most inertial sensors measure motion information, these measurements are sensitive to sensor placements [19]. For instance, acceleration traces exhibit more distinctive patterns with foot-mounted accelerometer [3] than phone accelerometer put in a bag due to random bouncing of phones.

• Complex human locomotion Human body can be in various poses, with at least 244 degrees of freedom [66]. Individuals of different heights, weights, ages, health states, etc., can exhibit different motion gaits. Furthermore, people may sometimes behave unpredictably. It it therefore challenging to extract consistent and robust locomotion patterns and accurate mobility information leveraging only phone sensors.

Since most indoor localization and navigation systems target at pedestrians, we mainly focus on step and stride (i.e., two steps) related human mobility information, which is fundamental and specific to pedestrians. In this section, we elaborate the principles to derive displacement and direction information of step vectors, as well as integrated and behavioural human mobility information.

# 2.2.2.1 Displacement Information

Step detection and counting is a basic module in most inertial based pedestrian localization and navigation systems. The physical underpinning is to search for cycles in acceleration traces to capture the repetitive movements during walking. The section summarizes algorithms for step detection and counting using phone accelerometers, followed by a brief discussion on the individual-specific stride length.

Step Detection and Counting When input an acceleration trace, step detection algorithms slice and label the trace into steps exploiting the repetitive patterns of walking, and the labels are then summed into step counts. We roughly group these algorithms as follows:

Temporal Analysis The cyclic property of walking is directly reflected in the acceleration trace in the time domain. Since heel strikes tend to introduce sharp changes, numerous schemes propose to detect magnitude peaks [40, 60], local variance peaks [25, 64], local minima [44, 52], zero-crossings [17], or level-crossings [70] (levels defined by historical mean and variance) from the low-pass filtered acceleration trace. Auto-correlation is a more robust means to magnify periodicity in the time domain regardless of the absolute amplitude of acceleration [39]. Steps can also be recognized by matching with a stride template either linearly (e.g., by cross-correlation [35]) or non-linearly (e.g., by Dynamic Time Warping [42]), yet at a higher cost.

Spectral Analysis When the acceleration trace contains at least two walking cycles, it is possible to identify the repetitive walking patterns in the frequency domain. The rationale is that walking movements would generate dominant frequencies around 2 Hz, a unique spectral characteristic compared with other human activities. Short-Term Fourier Transform (STFT) [8] and wavelet transforms [6, 53] have been employed to extract dominant frequencies, and steps are counted as the sum of the transform coefficients of the walking frequency.

Table 2.1 Recent smartphone based step counting summary 

<table><tr><td>Citation</td><td>Technologies</td><td>Cost</td><td>Error rate</td></tr><tr><td>[70]</td><td>Decide levels upon historical statistics detect level crossings</td><td>Low</td><td>N/A</td></tr><tr><td>[64]</td><td>Threshold on local variance</td><td>Low</td><td>2%</td></tr><tr><td>[44, 52]</td><td>Detect two consecutive local minima check a significant local maxima</td><td>Low</td><td>2%</td></tr><tr><td>[61]</td><td>Detect step starts and ends by threshold identify steps via finite state machine</td><td>Low</td><td>about 2%</td></tr><tr><td>[39]</td><td>Normalized auto-correlation</td><td>Medium</td><td>0.6%</td></tr><tr><td>[8, 42]</td><td>Template matching via DTW</td><td>Medium</td><td>&lt; 2%</td></tr><tr><td>[6, 8]</td><td>Zero CWT coefficients outside walking frequency inverse transform and count mean crossings</td><td>Medium</td><td>about 1.3%</td></tr><tr><td>[33]</td><td>Two-state HMM clustering</td><td>High</td><td>about 1.3%</td></tr></table>

• Feature Clustering Besides the above pattern analysis approaches, research also resorts to machine learning techniques to classify walking steps via features from acceleration traces. Various features have been explored, including statistics [46], entropy [5], as well as temporal correlation [41] and Fourier transform coefficients [28]. Albeit its high computational cost, feature clustering based schemes are more general and are often applied to classify multiple human activities beyond walking.

Table 2.1 summarizes some recent smartphone based step counting schemes in terms of techniques, cost and performance. Although step counting accuracy of above 99% is often reported under laboratory conditions, it remains unsettled whether it would be robust to arbitrary human behaviors, varying walking speeds, rough surfaces, etc. We refer interested readers to [19] for a review on step counting strategies via non-smartphone IMUs (e.g. foot mounted) and non-inertial sensors (e.g. ultrasonic).

Stride Length Estimation Knowing stride length is necessary when converting steps into distance traversed. Pedestrians may exhibit different stride lengths due to variety in height, walking speed and style. According to [56], step length may vary up to 40% at the same walking speed, and 50% with various speeds of the same person. Assuming constant stride length is efficient when frequent landmark calibration is available [52] or when only short walking distance is required [44]. Nevertheless, with the emerging trend of crowdsoucing based indoor localization and navigation [24, 38, 39, 45, 60, 64], walking traces of diverse users are expected to be calibrated and integrated. Therefore, it would boost the quality of the crowdsourced mobility information by considering individual-specific stride length. Some pioneer efforts in stride length estimation are summarized as follows.

• Offline Calibration An intuitive way to estimate user-specific stride length is to divide a known walking distance by measured step counts. However, since the walking patterns may not distribute uniformly, this method may induce bias on dominant walking patterns [9].   
• Online Estimation Some recent systems also propose to simultaneously estimate stride length and user locations via an augmented particle filter [39]. The rationale is to iteratively select the optimal stride length that fits user traces and map constraints.   
• Stride Length Modeling Originated from human kinematics, other studies correlate stride length with step frequency [18, 31, 34]. The key observation is that stride length tends to be shorter when walking slowly than fast [7]. A simple linear relationship suffices [9], yet the model parameters, which are trained offline, are specific to walking conditions, such as wearing sport shoes or high heels [45].

Accurate stride length improves displacement estimation, yet the accuracy increase is often marginal since heading drift typically dominates the errors [19]. Alternatively, when combining wireless and inertial based localization schemes, some novel explorations have partially eliminated the need to estimate user-specific stride length via virtual landmark assisted normalization [45] or error-tolerant transforms [64].

# 2.2.2.2 Direction Information

The direction of steps during walking is usually obtained by phone gyroscope and compass (magnetometer). The former outputs angular velocities in 3D, which are integrated over time into direction change (turning), while the latter directly measures the absolute orientation (heading) of the phone with respect to the magnetic North. Although compasses alone prove to be feasible for outdoor dead reckoning [12, 54], the two modalities often work synergistically in the literature of indoor localization and navigation [32, 39, 52], due to the unique challenges indoors and their complementary error characteristics: (1) The metal and conducting material indoors can significantly disturb compass readings and lead to short-term heading estimation errors of up to 100 ◦ [1]. (2) Gyroscopes remain unaffected by magnetic fields, yet suffer from bias caused by initial direction [52], and the estimated orientation drifts substantially with time [44].

While turning information can be easily measured by gyroscope, accurate heading information estimation by phone compass entails distinctive challenges. The main hurdle lies in two fold:

• Magnetic Offset Metal and conducting material nearby can disturb the perceived north of phone compass, thus leading to offset in heading estimation. Magnetic offset is location specific, and thus unpredictable beforehand [39].

Fig. 2.2 An illustration of magnetic offset and placement offset when estimating heading via phone compass   
![](images/492703f013b01cd490b40835d031963e8bafa6b4d6de902f9018ea16c9014e54.jpg)



Table 2.2 Representative heading estimation approaches 

<table><tr><td>Citation</td><td>Sensors</td><td>Technologies</td><td>Errors</td><td>Limitation</td></tr><tr><td>[65]</td><td>CP</td><td>Time domain averaging</td><td>N/A</td><td>Effective only for temporary magnetic interference</td></tr><tr><td>[52]</td><td>CP + G</td><td>Gyroscope verification magnetic landmark calibration</td><td>within 20° for 90% cases</td><td>Initial heading estimation errors dependence on landmarks</td></tr><tr><td>[32]</td><td>CP + G + A</td><td>Identify inference points particle filter</td><td>23° for 95% cases</td><td>Initial heading estimation errors converge time</td></tr><tr><td>[39]</td><td>CP + G + A</td><td>Estimate offset range via spectral analysis augmented particle filter</td><td>N/A</td><td>Extra spectral processing converge time</td></tr><tr><td>[49]</td><td>CP + CA + A</td><td>Detect visual patterns on ceilings and integrate with compass readings</td><td>1° on average</td><td>High computation overhead fail if unable to take photos</td></tr></table>

CP compass, G gyroscope, A accelerometer, CA camera

• Placement Offset The compass measures the orientation of the phone, while the phone’s heading may not be aligned with the moving direction of the user. Thus placement offset refers to the difference between the phone’s orientation and the moving direction of the user.

Figure 2.2 illustrates the magnetic and placement offset when estimating heading of user motion via phone compass indoors.

Table 2.2 summarizes some representative proposals to enhance heading estimation. While some efforts attempt to filter magnetic offset on consecutive compass readings [65], others fuse multiple sensors to improve estimation accuracy [32, 39, 45, 49, 52]. The rationale is to exploit additional sensors (e.g. gyroscopes) to evaluate the compass readings [32, 52], and rectify heading estimation iteratively during walking (e.g. particle filter) [32, 39]. Despite these explorations, robustness and accuracy of heading estimation still remain a bottleneck for inertial based indoor localization and navigation systems. One recent work [43] reduces heading estimation error to less than $6 ^ { \circ }$ by in-depth video-based human walking pattern analysis and magnetic interference localization and isolation, which is approaching the accuracy of visual reference based methods. The primary hurdle for this bottleneck is that inertial based heading estimation schemes exploit sensors to perceive the relatively unconstrained human behaviours, making precise walking direction a micro-motion that requires subtle identification [43]. In contrast, visual reference based approaches [50] leverage static landmarks such as ceiling edges, yet improve estimation accuracy at the cost of computation and energy consumption.

# 2.2.2.3 Integrated Information

Previous subsections mainly elaborate the principles and methods to derive shortterm displacement and direction information (e.g. steps and turns) from sensory data. In this subsection, we demonstrate how the instantaneous displacement and direction information is integrated into more complex human mobility information.

Trajectory A pedestrian trajectory consists of a sequence of step vectors. While inertial based indoor localization and navigation systems require accurate trajectories to track pedestrians, some recent work [60, 64] also exploit comparatively coarse-grained trajectory information to assist wireless localization. For example, in [60], trajectories are utilized to infer whether the wireless fingerprints from different locations are reachable with each other.

Accurate trajectory estimation still lies in the core of various indoor localization and navigation systems. Besides traditional challenges in calibrating trajectories of a single user, the emerging trend of crowdsoucing based localization also poses new challenges in clustering trajectories from diverse users [39, 45].

Locomotion Modality Awareness of locomotion modalities (e.g. walking or running) and usage behaviours (e.g. text messaging or making a phone call) assists to construct more elaborated motion models (e.g. adjust stride length estimation or step counting according to varying speeds and phone placements), thus holding potential for improving localization and navigation algorithms.

Identifying these behaviours belongs to a subset of the enormous research on activity recognition [41]. Some recent work has already explored to utilize phone accelerometers to distinguish different motion modalities (walking or running) [23, 36], transportation modes (bus or metro) [20], and phone poses (in hand or at ear) [37].

Though promising, it is inevitable to involve relatively complex machine learning techniques to differentiate locomotion modalities and phone placements, which incurs considerable computation and energy overhead. It still lacks comparative studies on the tradeoff between the overhead of distinguishing fine-grained locomotion modalities and the performance gain on indoor localization.

Context Landmarks The mobility information measured by sensors, when combined with location context, can provide unique virtual landmarks, which facilitates re-calibration and thus improves localization accuracy. The key observation is that certain building structures would demonstrate distinctive sensor signatures. For instance, the acceleration readings on an elevator experience a sharp surge and drop at the start and the stop of the elevator. Wang et al. [52] investigate such unique acceleration patterns of stairs, elevators, escalators, walking and standing. If the locations of these structures are known as prior, they would serve as landmarks to rectify dead reckoning drifts.

In case of multiple users, mobility information (e.g. trajectories) of different users can be associated via encounters. These opportunistic encounters (e.g., Alice happened to meet Bob) can also act as virtual landmarks to calibrate dead reckoning drifts [11] (e.g., We can adjust the trajectory of Alice to make her current location consistent with Bob’s location, since Bob just walked out of an elevator whose location is known as prior). Such social encounters also help to refine the plausible locations of users [26] (e.g., if Alice met Bob, then we may safely restrain the potential locations of Alice to the intersection between the potential locations of Alice and those of Bob).

These novel context landmarks stem from user mobility, and are complementary to static landmarks (or fingerprints) such as ambient sound, light and color [4]. While some pioneer work has explored to incorporate the two, (e.g., inertial patterns + WiFi RSS [52], directions + WiFi trend [45], its full potential still remains an open issue.

# References

1. Afzal, M., Renaudin, V., Lachapelle, G.: Assessment of indoor magnetic field anomalies using multiple magnetometers. In: Proceedings of ION International Technical Meeting of the Satellite Division of the Institute of Navigation (GNSS) (2001)   
2. Agarwal, Y., Hall, M.: ProtectMyPrivacy: detecting and mitigating privacy leaks on iOS devices using crowdsourcing. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2013)   
3. Angermann, M., Robertson, P.: FootSLAM: pedestrian simultaneous localization and mapping without exteroceptive sensors hitchhiking on human perception and cognition. Proc. IEEE 100(Special Centennial Issue), 1840–1848 (2012)   
4. Azizyan, M., Constandache, I., Roy Choudhury, R.: SurroundSense: mobile phone localization via ambience fingerprinting. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2009)   
5. Bao, L., Intille, S.: Activity recognition from user-annotated acceleration data. In: Pervasive Computing. Lecture Notes in Computer Science, vol. 3001, pp. 1–17. Springer, Berlin/Heidelberg (2004)   
6. Barralon, P., Vuillerme, N., Noury, N.: Walk detection with a kinematic sensor: frequency and wavelet comparison. In: Proceedings of IEEE International Conference of Engineering in Medicine and Biology Society (EMBS) (2006)   
7. Bertram, J.E., Ruina, A.: Multiple walking speed–frequency relations are predicted by constrained optimization. Elsevier J. Theor. Biol. 209(4), 445–453 (2001)   
8. Brajdic, A., Harle, R.: Walk detection and step counting on unconstrained smartphones. In: Proceedings of ACM International Conference on Ubiquitous Computing (UbiComp) (2013)   
9. Cho, D.K., Mun, M., Lee, U., Kaiser, W., Gerla, M.: AutoGait: a mobile platform that accurately estimates the distance walked. In: Proceedings of IEEE International Conference on Pervasive Computing and Communications (PerCom) (2010)

10. Choffnes, D.R., Bustamante, F.E., Ge, Z.: Crowdsourcing service-level network event monitoring. ACM SIGCOMM Comput. Commun. Rev. 40(4) (2010)   
11. Constandache, I., Bao, X., Azizyan, M., Choudhury, R.R.: Did you see bob?: human localization using mobile phones. In: Proceedings of the Sixteenth Annual International Conference on Mobile computing and networking, pp. 149–160. ACM, New York (2010)   
12. Constandache, I., Choudhury, R., Rhee, I.: Towards mobile phone localization without wardriving. In: Proceedings of IEEE International Conference on Computer Communications (INFOCOM) (2010)   
13. Doan, A., Franklin, M.J., Kossmann, D., Kraska, T.: Crowdsourcing applications and platforms: a data management perspective. Proc. VLDB Endow. 4(12), 1508–1509 (2011)   
14. Franklin, M.J., Kossmann, D., Kraska, T., Ramesh, S., Xin, R.: Crowddb: answering queries with crowdsourcing. In: Proceedings of the 2011 ACM SIGMOD International Conference on Management of Data, pp. 61–72. ACM, New York (2011)   
15. Gao, H., Barbier, G., Goolsby, R.: Harnessing the crowdsourcing power of social media for disaster relief. IEEE Intell. Syst. 26(3), 10–14 (2011)   
16. Gao, R., Zhao, M., Ye, T., Ye, F., Wang, Y., Bian, K., Wang, T., Li, X.: Jigsaw: indoor floor plan reconstruction via mobile crowdsensing. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2014)   
17. Goyal, P., Ribeiro, V., Saran, H., Kumar, A.: Strap-down pedestrian dead-reckoning system. In: Proceedings of International Conference on Indoor Positioning and Indoor Navigation (IPIN) (2011)   
18. Gusenbauer, D., Isert, C., Krosche, J.: Self-contained indoor positioning on off-the-shelf mobile devices. In: Proceedings of International Conference on Indoor Positioning and Indoor Navigation (IPIN) (2010)   
19. Harle, R.: A Survey of indoor inertial positioning systems for pedestrians. IEEE Commun. Surv. Tutorials 15(3), 1281–1293 (2013)   
20. Hemminki, S., Nurmi, P., Tarkoma, S.: Accelerometer-based transportation mode detection on smartphones. In: Proceedings of ACM Conference on Embedded Networked Sensor Systems (SenSys) (2013)   
21. Hoque, M.A., Siekkinen, M., Nurminen, J.K.: Using crowd-sourced viewing statistics to save energy in wireless video streaming. In: ACM International Conference on Mobile Computing and Networking (MobiCom). ACM, New York (2013)   
22. Howe, J.: The rise of crowdsourcing. Wired Mag. 14(6), 1–4 (2006)   
23. Iso, T., Yamazaki, K.: Gait analyzer based on a cell phone with a single three-axis accelerometer. In: Proceedings of ACM Conference on Human-Computer Interaction with Mobile Devices and Services (MobileHCI) (2006)   
24. Jiang, Y., Xiang, Y., Pan, X., Li, K., Lv, Q., Dick, R.P., Shang, L., Hannigan, M.: Hallway based automatic indoor floorplan construction using room fingerprints. In: Proceedings of ACM International Conference on Ubiquitous Computing (UbiComp) (2013)   
25. Jimenez, A., Seco, F., Prieto, C., Guevara, J.: A comparison of pedestrian dead-reckoning algorithms using a low-cost MEMS IMU. In: Proceedings of IEEE International Symposium on Intelligent Signal Processing (WISP) (2009)   
26. Jun, J., Gu, Y., Cheng, L., Lu, B., Sun, J., Zhu, T., Niu, J.: Social-loc: improving indoor localization with social sensing. In: Proceedings of ACM Conference on Embedded Networked Sensor Systems (SenSys) (2013)   
27. Kittur, A., Chi, E.H., Suh, B.: Crowdsourcing user studies with mechanical turk. In: Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, pp. 453–456. ACM, New York (2008)   
28. Kobayashi, T., Hasida, K., Otsu, N.: Rotation invariant feature extraction from 3-D acceleration signals. In: Proceedings of IEEE International Conference on Acoustics Speech and Signal Processing (ICASSP) (2011)   
29. Korpela, E., Werthimer, D., Anderson, D., Cobb, J., Leboisky, M.: SETI@home-massively distributed computing for SETI. Comput. Sci. Eng. 3(1), 78–83 (2001)

30. Koukoumidis, E., Peh, L.S., Martonosi, M.R.: Signalguru: leveraging mobile phones for collaborative traffic signal schedule advisory. In: Proceedings of the 9th International Conference on Mobile Systems, Applications, and Services, pp. 127–140. ACM, New York (2011)   
31. Ladetto, Q.: On foot navigation: continuous step calibration using both complementary recursive prediction and adaptive kalman filtering. In: Proceedings of ION GPS (2000)   
32. Li, F., Zhao, C., Ding, G., Gong, J., Liu, C., Zhao, F.: A reliable and accurate indoor localization method using phone inertial sensors. In: Proceedings of ACM International Conference on Ubiquitous Computing (UbiComp) (2012)   
33. Mannini, A., Sabatini, A.: A hidden Markov model-based technique for Gait segmentation using a foot-mounted gyroscope. In: Proceedings of IEEE International Conference of Engineering in Medicine and Biology Society (EMBS) (2011)   
34. Margaria, R., Margaria, R.: Biomechanics and Energetics of Muscular Exercise. Clarendon Press, Oxford (1976)   
35. Marschollek, M., Goevercin, M., Wolf, K.H., Song, B., Gietzelt, M., Haux, R., Steinhagen-Thiessen, E.: A performance comparison of accelerometry-based step detection algorithms on a large, non-laboratory sample of healthy and mobility-impaired persons. In: Proceedings of IEEE International Conference of Engineering in Medicine and Biology Society (EMBS) (2008)   
36. Miluzzo, E., Lane, N.D., Fodor, K., Peterson, R., Lu, H., Musolesi, M., Eisenman, S.B., Zheng, X., Campbell, A.T.: Sensing meets mobile social networks: the design, implementation and evaluation of the cenceMe application. In: Proceedings of ACM Conference on Embedded Networked Sensor Systems (SenSys) (2008)   
37. Park, J.g., Patel, A., Curtis, D., Teller, S., Ledlie, J.: Online pose classification and walking speed estimation using handheld devices. In: Proceedings of ACM International Conference on Ubiquitous Computing (UbiComp) (2012)   
38. Purohit, A., Sun, Z., Pan, S., Zhang, P.: SugarTrail: indoor navigation in retail environments without surveys and maps. In: Proceedings of IEEE Communications Society Conference on Sensor Mesh and Ad Hoc Communications and Networks (SECON) (2013)   
39. Rai, A., Chintalapudi, K.K., Padmanabhan, V.N., Sen, R.: Zee: zero-effort crowdsourcing for indoor localization. In: Proceedings of ACM International Conference on Mobile Computing and Networking (MobiCom) (2012)   
40. Randell, C., Djiallis, C., Muller, H.: Personal position measurement using dead reckoning. In: Proceedings of IEEE International Symposium on Wearable Computers (ISWC) (2003)   
41. Ravi, N., Dandekar, N., Mysore, P., Littman, M.L.: Activity recognition from accelerometer data. In: Proceedings of AAAI Conference on Innovative Applications of Artificial Intelligence (IAAI) (2005)   
42. Rong, L., Zhiguo, D., Jianzhong, Z., Ming, L.: Identification of individual walking patterns using gait acceleration. In: Proceedings of International Conference on Bioinformatics and Biomedical Engineering (ICBBE) (2007)   
43. Roy, N., Wang, H., Roy Choudhury, R.: I am a smartphone and i can tell my user’s walking direction. In: Proceedings of the 12th Annual International Conference on Mobile Systems, Applications, and Services, pp. 329–342. ACM, New York (2014)   
44. Sen, S., Lee, J., Kim, K.H., Congdon, P.: Back to the basics: avoiding multipath to revive inbuilding WiFi localization. In: Proceedings of ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2013)   
45. Shen, G., Chen, Z., Zhang, P., Moscibroda, T., Zhang, Y.: Walkie-Markie: indoor pathway mapping made easy. In: Proceedings of USENIX Conference on Networked Systems Design and Implementation (NSDI) (2013)   
46. Siirtola, P., Roning, J.: Recognizing human activities user-independently on smartphones based on accelerometer data. Int. J. Interact. Multimed. Artif. Intell. 1(5), 38–45 (2012)   
47. Simoens, P., Xiao, Y., Pillai, P., Chen, Z., Ha, K., Satyanarayanan, M.: Scalable crowdsourcing of video from mobile devices. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2013)

48. Sun, W., Liu, J., Wu, C., Yang, Z., Zhang, X., Liu, Y.: MoLoc: on distinguishing fingerprint twins. In: Proceedings of IEEE International Conference on Distributed Computing Systems (ICDCS) (2013)   
49. Sun, Z., Pan, S., Su, Y.C., Zhang, P.: Headio: zero-configured heading acquisition for indoor mobile devices through multimodal context sensing. In: Proceedings of ACM International Conference on Ubiquitous Computing (UbiComp) (2013)   
50. Sun, Z., Pan, S., Su, Y.C., Zhang, P.: Headio: zero-configured heading acquisition for indoor mobile devices through multimodal context sensing. In: Proceedings of the 2013 ACM International Joint Conference on Pervasive and Ubiquitous Computing, pp. 33–42. ACM, New York (2013)   
51. von Ahn, L., Maurer, B., McMillen, C., Abraham, D., Blum, M.: reCAPTCHA: human-based character recognition via web security measures. Science 321(5895), 1465–1468 (2008)   
52. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: Proceedings of ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2012)   
53. Wang, J.H., Ding, J.J., Chen, Y., Chen, H.H.: Real time accelerometer-based gait recognition using adaptive windowed wavelet transforms. In: Proceedings of IEEE Asia Pacific Conference on Circuits and Systems (APCCAS) (2012)   
54. Wang, H., Wang, Z., Shen, G., Li, F., Han, S., Zhao, F.: WheelLoc: enabling continuous location service on mobile phone for outdoor scenarios. In: Proceedings of IEEE International Conference on Computer Communications (INFOCOM) (2013)   
55. Wang, Y., Liu, X., Wei, H., Forman, G., Chen, C., Zhu, Y.: CrowdAtlas: self-updating maps for cloud and personal use. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys) (2013)   
56. Weinberg, H.: Using the ADXL202 in pedometer and personal navigation applications. Analog Devices AN-602 Application Note (2002)   
57. Wikipedia: http://en.wikipedia.org/wiki/Accelerometer (2014)   
58. Wikipedia: http://en.wikipedia.org/wiki/Gyroscope (2014)   
59. Wikipedia: http://en.wikipedia.org/wiki/Magnetometer (2014)   
60. Wu, C., Yang, Z., Liu, Y., Xi, W.: WILL: wireless indoor localization without site survey. IEEE Trans. Parallel Distrib. Syst. 24(4), 839–848 (2013)   
61. Wu, C., Yang, Z., Zhao, Y., Liu, Y.: Footprints elicit the truth: improving global positioning accuracy via local mobility. In: Proceedings of IEEE International Conference on Computer Communications (INFOCOM) (2013)   
62. Yan, B., Chen, G.: Appjoy: personalized mobile application discovery. In: Proceedings of the 9th International Conference on Mobile Systems, Applications, and Services, pp. 113–126. ACM, New York (2011)   
63. Yang, D., Xue, G., Fang, X., Tang, J.: Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2012)   
64. Yang, Z., Wu, C., Liu, Y.: Locating in fingerprint space: wireless indoor localization with little human intervention. In: Proceedings of ACM International Conference on Mobile Computing and Networking (MobiCom) (2012)   
65. Youssef, M., Yosef, M., El-Derini, M.: GAC: energy-efficient hybrid GPS-accelerometercompass GSM localization. In: Proceedings of IEEE Global Telecommunications Conference (GLOBECOM) (2010)   
66. Zatsiorsky, V.M.: Kinematics of Human Motion. Human Kinetics, Champaign/Leeds (1998)   
67. Zhang, X., Yang, Z., Sun, W., Liu, Y., Tang, S., Xing, K., Mao, X.: Incentives for mobile crowd sensing: a survey. IEEE Commun. Surv. Tutorials 18(1), 54–67 (2016)   
68. Zhao, Y., Zhang, Y., Yu, T., Liu, T., Wang, X., Tian, X., Liu, X.: Citydrive: a map-generating and speed-optimizing driving system. In: IEEE International Conference on Computer Communications (INFOCOM) (2014)

69. Zhou, P., Zheng, Y., Li, M.: How long to wait?: predicting bus arrival time with mobile phone based participatory sensing. In: ACM International Conference on Mobile Systems, Applications, and Services (MobiSys), pp. 379–392 (2012)   
70. Zhu, X., Li, Q., Chen, G.: APT: accurate outdoor pedestrian tracking with smartphones. In: Proceedings of IEEE International Conference on Computer Communications (INFOCOM) (2013)

# Part II

# Boosting Deployment: Making It Available

Part II contains two chapters focusing on how to make fingerprint-based localization easily deployable in practice. The first chapters present how to apply mobile crowdsourcing idea to enable automatic construction of fingerprint database and thus eliminate the time-consuming and labor-intensive site survey. The second chapter further presents how to automatically generate indoor floorplans with rich contexts. With automatically constructed physical floorplans and fingerprint database, WiFi-based localization systems can be rapidly boosted for practical deployment.

# TO MOBILE CROWDSOURCING:

The only difference between you and the star is that you shine below, and the other shines above: Wherever you are located you are a star!

– Michael Bassey Johnson

# Chapter 3 Radio Map Construction Without Site Survey

![](images/8cdcdf44a35f0dea69761140de510832ac7e8ca76a41d1cb23af7ec07d8932ab.jpg)

Abstract Most radio-based indoor localization solutions require a process of site survey, in which radio signatures of an interested area are annotated with their real recorded locations. Site survey involves intensive costs on manpower and time, limiting the applicable buildings of wireless localization worldwide. In this chapter, we investigate, under a crowdsourcing scheme, novel sensors integrated in modern mobile phones and leverage user motions to construct the radio map of a floor plan, which is previously obtained only by site survey. In particular, we design LiFS, an indoor localization system that crowdsources the site survey efforts to mobile users and enables automatic radio map construction.

# 3.1 Introduction

The popularity of mobile and pervasive computing stimulates extensive research on wireless indoor localization. As mentioned in Chap. 1, WiFi fingerprint-based approaches become the mainstream solutions, which is divided into two stages: training and localization. The core of the training stage is a site survey procedure, which acts as a long-standing hurdle to fingerprint-based localization.

Although site survey is time-consuming, labor-intensive, and vulnerable to environmental dynamics, it is inevitable for fingerprinting-based approaches, since the fingerprint database is constructed by locationally labeled fingerprints from onsite records. In the end of 2011, Google released Google Map 6.0 that provides indoor localization and navigation available only at some selected airports and shopping malls in the US and Japan. The enlargement of applicable areas is strangled by pretty limited fingerprint data of building interiors. If ordinary mobile phone users are able to participate in site survey by contributing their data, the burden of indoor map providers like Google will be effectively reduced.

The development of wireless and embedded technology has fostered the flourish of smartphone market. Nowadays mobile phones possess powerful computation and communication capability, and are equipped with various functional built-in sensors. Along with users round-the-clock, mobile phones can be seen as an increasingly important information interface between users and environments. These advances lay solid foundations of breakthrough technology for indoor localization.

On this basis, we reassess existing localization schemes and explore the possibility of using previously unavailable information. Considering user movements in a building, originally separated RSS fingerprints are geographically connected by user moving paths of locations where they are recorded, and they consequently form a high dimension fingerprint space, in which the distances among fingerprints, measured by footsteps, are preserved. In addition, we reform the floor plan of a building to the stress-free floor plan, a high dimension space in which the distance between two locations reflects their walking distance according to the real floor plan. The spatial similarity of stress-free floor plan and fingerprint space enables fingerprints labeled with real locations, which would be done only by site survey previously. These observations motivate us to design practical, flexible, and rapidly deployed localization approaches with little human costs and intervention.

In this chapter, we propose LiFS (Locating in Fingerprint Space), a wireless indoor localization approach. By exploiting user motions from mobile phones, we successfully remove the site survey process of traditional approaches, while at the same time, achieve competitive localization accuracy. The key idea behind LiFS is that human motions can be applied to connect previously independent radio fingerprints under certain semantics. LiFS requires no prior knowledge of AP locations, which is often unavailable in commercial or office buildings where APs are installed by different organizations. In addition, LiFS’ users are in no need of explicit participation to label measured data with corresponding locations, even in the training stage. In all, LiFS transforms the localization problem from 2D floor plan to a high dimension fingerprint space and introduces new prospective techniques for automatic labeling.

To validate this design, we deploy a prototype system and conduct extensive experiments in a middle-size academic building covering over 1600 m2. Experiment results show that LiFS achieves comparable location accuracy to previous approaches even without site survey. The average localization error is 5.8 m and can be reduced to be about 2 m by incorporating trajectory matching, while the room-level localization error is about 11%.

The rest of this chapter is organized as follows. We discuss the related works in Sect. 3.2. Section 3.3 presents the system overview of LiFS. The construction of stress-free floor plan is introduced in Sect. 3.4. Section 3.5 shows how to transform RSS fingerprints into high-dimension fingerprint space. In Sect. 3.6, we promote several techniques to establish the relationship between stress-free floor plan and fingerprint space. The prototype implementation and experiments are discussed in Sect. 3.7. We conclude in Sect. 3.8.

# 3.2 Related Work

Wireless Localization In the literature of indoor localization, many techniques have been proposed in the past two decades. A large body of indoor localization approaches adopt fingerprint matching as the basic scheme of location determination. Researchers have striven to exploit different signatures of the existing devices or reduce the mapping effort. Most of these techniques utilize the RF signals such as RADAR [2], Horus [33], improved upon RADAR, LANDMARC [19], ActiveCampus [11], PlaceLab [15] and OIL [21]. SurroundSense [1] performs logical location estimation based on ambience features including sound, light, color, WiFi, etc. FM radio [5] and CSI [24] are explored to use as fingerprints. All these approaches require site survey over areas of interests to build a fingerprint database. The considerable manual cost and efforts, in addition to the inflexibility to environment dynamics are the main drawbacks of fingerprinting-based methods. Some recent efforts also harness mobile crowdsourcing to automate the site survey procedure to ease deployment, including UnLoc [30], Zee [23] and Walkie-Markie [27], etc.

Simultaneous Localization and Mapping (SLAM) While the robotics and computer vision communities have developed techniques for jointly estimating the locations of a robot and a map of an environment, the nature of wireless signal strength prohibits the use of standard SLAM techniques [18, 28]. These techniques typically depend on two facts: (1) the ability to sense and match discrete entities such as landmarks or obstacles detected by sonar or laser range-finders; (2) precisely controlled movement of robots to depict discovered environments. Both of them are unreasonable for smartphone-based localization [30]. WiFi-SLAM [9] uses the Gaussian process latent variable models to relate RSS fingerprints and models human movements (displacement, direction, etc.) as hidden variables. When a small portion of RSS measurements are tagged with the real coordinates, semi-supervised localization [22] estimate the others’ locations according to RSS dissimilarity. GraphSLAM [12] further improves WiFi-SLAM regarding computing efficiency and relying assumptions.

Multidimensional Scaling Multidimensional scaling (MDS) [4] is a set of related statistical techniques often used in information visualization for exploring similarities or dissimilarities in data. An MDS algorithm starts with a matrix of item-item dissimilarities, then assigns a location to each item in d-dimensional space, where d is specified a priori. For sufficiently small d (d = 2, 3), the resulting locations may be displayed in a 2D graph or a 3D structure.

Seeing inter-device distances as a metric of dissimilarity, many approaches of network localization adopt MDS as a tool for calculating the locations of wireless devices [8, 25]. For example, in wireless sensor networks, sensor nodes are capable of measuring the distances to neighboring nodes by RSS, ToA, TDoA, etc. MDS is used to assign a coordinate to each node such that the measured inter-node distances are as much preserved as possible. Some researchers propose MDS to figure out

WiFi AP locations [14]. In their approach, AP-AP distances are determined by a radio attenuation model. Although being similar to our solution in terms of the usage of MDS, it is neither for user localization nor fingerprinting-based.

# 3.3 Overview

# 3.3.1 Data Collection

User participation is essential in the initial period at the online stage. Untrained users walk in a building following daily activities. Mobile phones, carried by users, collect WiFi RSS characteristics (a.k.a. RSS fingerprints or signatures) at various locations along user movement paths, and the walking distances are also recorded. Walking distances are measured as footsteps from the readings of integrated accelerometers in mobile phones. Similarly, accelerometers also infer the starting and finishing moments of user paths. LiFS harnesses the walking distance between two endpoints (denoted by corresponding fingerprints) along a user path to establish the geographical relationship among fingerprints. During data collection, users can be even unaware of the collection task in which they are actually involved.

# 3.3.2 System Architecture

As shown in Fig. 3.1, the system architecture of LiFS follows the general WiFi fingerprinting framework as presented in Fig. 1.2, but differs significantly in the training phase.

Training Phase The core task of training phase is to build the fingerprint database. We divide this task into 3 steps: (1) transforming floor plan to stress-free floor plan; (2) creating fingerprint space; (3) mapping fingerprints to real locations.

A floor plan shows a view of a building structure from above, including the relationships between rooms, spaces, and other physical features. The geographical distance between two locations in a floor plan is not necessary to be the walking distance between them due to the block of walls and other obstacles. Hence, we propose stress-free floor plan, which puts real locations in a floor plan into a high dimension space by multidimensional scaling (MDS) [4], such that the geometrical distances between the points in the high dimension space reflect their real walking distances. Through stress-free floor plan, the walking distances collected by users can be accurately and carefully utilized.

Fingerprint space is a unique component in LiFS, different from traditional approaches. According to the inter-fingerprint distances, MDS is used to create a high dimension space, in which fingerprints are represented by points, and their mutual distances are preserved. In traditional approaches, fingerprints are geographically unrelated, losing the possibility of building fingerprint space.

![](images/842fda4cb8579d5d411d8159e8cf43cf1fa239fda7fb31aa41a4b23ac890eaa5.jpg)



Fig. 3.1 System architecture

In fingerprint database, fingerprints are associated with their collecting locations (i.e., fingerprints are labeled with locations). Such associations are achieved by mapping fingerprint space (fingerprints) to stress-free floor plan (locations). In LiFS, the fingerprint database is updated continuously according to newly collected data, such that the database reflects the up-to-date radio signal distribution. As shown in Fig. 3.1, fingerprint database, as the core component, connects training and operating phase.

Operating Phase The operating phase follows the same logic as classical WiFi fingerprint-based approaches, which determines a location by searching the best fingerprint matching. Many searching algorithms can be used for this purpose. In LiFS, we adopt a simple one, the nearest neighbor algorithm.

# 3.4 Stress-Free Floor Plan

In architecture and building engineering, a floor plan is a diagram, showing a view from above of the relationships between rooms, spaces, and other physical features at one level of a structure. Dimensions are usually drawn between the walls to specify room size and wall length. The floor plan of our experiment field is shown in Fig. 3.2. The geographical distance between two locations in a floor plan does not necessarily equal to the walking distance between them due to the block of walls and other obstacles. Hence, ground-truth floor plans come into conflict with the measured distances during data collection. Figure 3.2 also illustrates the distance mismatch phenomenon. The walking distance of two marked locations is greatly larger than their straight-line distance since walls are not easily passed through by users.

![](images/738dd6c0b417a349942c54143f85aa5b18baf942058bc5ccf726919662279e16.jpg)



Fig. 3.2 Floor plan with sample locations

![](images/78817362fb3be5de379f4a83ea524c1d4ee0b2cf00a592dedfd54fe0fbd676bd.jpg)



(a)

![](images/4490d794159354b009ecc967a474892d72511ce91667402e8469da4bf20b2c0b.jpg)



(b)   
Fig. 3.3 Stress-free floor plan. (a) 2D stress-free floor plan. (b) 3D stress-free floor plan

To address the distance mismatch problem, we propose the concept of stressfree floor plan. We sample an area of interests at the intersecting locations of a mesh of grids in a floor plan, as shown in Fig. 3.2. The length a of a grid can be 1–3 m according to the general performance of fingerprinting-based localization methods. Overmuch large or small values of a will decrease location accuracy or gain marginally or even scarcely. In our experiment, we set $a = 2 \mathrm { m }$ . By calculating the distances between all pairs of sample locations, we have the distance matrix $D = \left[ d _ { i j } \right]$ , where $d _ { i j }$ is the walking distance between two sample locations $i$ and $l _ { j }$ in the floor plan. Using D as an input, MDS maps all $\vec { l _ { i } \cdot s }$ into a d-dimension Euclidean space. In a stress-free floor plan, the Euclidean distance between a pair of points reflects the walking distance of their corresponding locations in a real floor plan. Stress-free floor plans are often hardly embeddable in a low dimension space due to excessive distance constraints. For the convenience of observation, we set $d = 2 , 3$ and the resulting stress-free floor plans in 2D and 3D visualization are shown in Fig. 3.3a, b, respectively, where points with the same color represent the sample locations from the same area.

# 3.5 Fingerprint Space

This section discusses the techniques for constructing fingerprint space based on the data collected by users.

# 3.5.1 Fingerprint Collection

Suppose m APs in an area A. For each location in A, the RSS fingerprint at this location can be denoted as a vector $\pmb { f } = ( s _ { 1 } , s _ { 2 } , \ldots s _ { m } )$ , where $s _ { i }$ is the RSS of the ith AP and $s _ { i } = 0$ if the signal of the ith AP cannot be detected. Let $d _ { i j } ^ { \prime }$ denote the distance between the positions of $f _ { i }$ and $f _ { j }$ . We set $d _ { i j } ^ { \prime } = + \infty$ temporarily if the distance record between $\boldsymbol { f } _ { i }$ and $f _ { j }$ is not available. We measure $d _ { i j } ^ { \prime }$ as follows. Suppose at somewhere a mobile phone records $f _ { i }$ ; Along with walking users, it moves to another position and records $f _ { j }$ . In this case, $d _ { i j } ^ { \prime }$ is the number of footsteps during the movement.

RSS fingerprints are collected during users’ routine indoor movements. Users walk in a building and their mobile phones record RSS fingerprints along their walking paths, as well as the footsteps between every pairs of two consecutive fingerprints. As illustrated in Fig. 3.4, fingerprints (denoted as squares, circles, or triangles) are recorded along three walking paths and the line segments between fingerprints indicate their distances in terms of footsteps.

After fingerprint collection, we have a set of fingerprints $F = \{ f _ { i } , i = 1 \ldots n \}$ (n is the number of records) and a distance matrix $D ^ { \prime } = \left[ d _ { i j } ^ { \prime } \right]$ , both of which are essential for constructing the fingerprint space.

![](images/c9e979e80f84bac6915de4f448cf1420926711b9a2635397af767a138e4be280.jpg)



Fig. 3.4 Moving trajectory samples

# 3.5.2 Pre-processing

As user movements are usually arbitrary and ruleless, walking paths might be intersectant and accordingly the fingerprints might be overlapped. Hence data preprocessing is necessary to merge similar fingerprints, which means they are likely from the same (or very close) locations in the floor plan.

Generally, for two fingerprints $\pmb { f } _ { i } = ( s _ { 1 } , s _ { 2 } , \dots s _ { m } , s _ { m } )$ and $\pmb { f } _ { j } = ( t _ { 1 } , t _ { 2 } , \dots t _ { * } , t _ { m } )$ , define RSS difference (dissimilarity) δ between $f _ { i } , f _ { j }$ as follows:

$$
\delta_ {i j} = \left\| \boldsymbol {f} _ {i} - \boldsymbol {f} _ {j} \right\| _ {1} = \sum_ {k = 1} ^ {m} \left| s _ {k} - t _ {k} \right| \tag {3.1}
$$

For $f _ { i }$ and $f _ { j }$ , if their dissimilarity $\delta _ { i j }$ is smaller than a predefined threshold , then they are merged as a same point in the fingerprint space to be generated. Otherwise, if $\delta _ { i j } ~ > ~ \epsilon , ~ f _ { i }$ and $f _ { j }$ are treated as two different points. The determination of  is based on the fingerprint samples collected at a given location (when phones are not moving). Several other works like [30, 32] adopt the similar solution as well. Hence,  represents the average maximum dissimilarity of fingerprints from a distinct location, which is then feasible for merging fingerprints from the same (or close) locations and distinguishing fingerprints from different locations. In practice, the calculation of  can be automatically finished by exploiting fingerprint measurements from stationary users, who can be detected via inspecting the inertial sensor data from their mobile phones.

Moreover, the raw data from accelerometer readings are pre-processed to obtain walking distance measurements. Theoretically the distance traveled can be calculated by integrating acceleration twice with respect to time. However due to the presence of noise in accelerometer readings, error accumulates rapidly and can reach up to 100 m after one minute of operation [31].

To avoid accumulation of measurement errors, we adopt the individual step counts as the metric of walking distance instead, like a pedometer. Figure 3.5 shows the magnitude of acceleration during walking for ten steps. We employ a local variance threshold method [13] to detect the number of steps. The method is based on filtering the magnitude of acceleration followed by applying a threshold on the variance of acceleration over a sliding window. Step counting is accurate and in our experiments the measured steps are almost exactly what they actually are.

We understand that stride lengths vary from person to person. Previous solutions like [30] assume a fixed stride length of a person according to his weight and height, and achieve accurate results. In our solution, the variation of stride length can be efficiently alleviated through the fact that non-metric MDS can tolerate measurement errors gracefully, due to its over-determined nature [25, 26]. In addition, recently, robust trajectory estimation schemes have also been proposed for crowdsourcing-based applications, which can be incorporated in LiFS to alleviate the negative influence of crowdsourced abnormal user trajectories from multiple users [34].

![](images/6876ce783278051b3eda4d3ab1ff4353ee1001af07f7ec67d3e7a46e4b8f9ba3.jpg)



Fig. 3.5 The acceleration pattern for 10 steps

# 3.5.3 Fingerprint Space Construction

To construct an accurate and informative fingerprint space, adequate fingerprints and their distance measurements are required. In our experiments, the operating phase of LiFS starts when the number of collected fingerprints reaches 10 times of the number of the sample locations in the construction of stress-free floor plans. Another possible way is to assign the first several days of LiFS’ pilot run for training because routine activities exhibit certain repetitiveness day after day. Actually the running of operating phase does not mean the end of data collection. It is reasonable to select a less conservative starting point and refine the current fingerprint database uninterruptedly in operating phase according to newly coming data.

If no user path passes through a pair of fingerprints $f _ { i }$ and $f _ { j }$ , the direct measurement of the distance $d _ { i j } ^ { \prime }$ is unavailable. However, all user paths constitute a network of fingerprints in which $f _ { i }$ and $f _ { j }$ are connected via more than one user paths. Hence, the value of $d _ { i j } ^ { \prime }$ can be approximated as the length of the shortest path between $f _ { i }$ and $f _ { j }$ by passing several user path segments. Note that some measured values of $d _ { i j } ^ { \prime }$ can also be updated under this intuition. For example, if $d _ { i j } ^ { \prime } > d _ { i k } ^ { \prime } + d _ { k j } ^ { \prime }$ for some $k ,$ , then $d _ { i j } ^ { \prime }$ is updated to $d _ { i k } ^ { \prime } + d _ { k j } ^ { \prime }$ . Such updates can eliminate the negative distance estimates caused by the circuitous paths or the adverse (to LiFS) user habit of pacing back and forth.

We adopt the Floyd-Warshall algorithm [10] to compute all-pair shortest paths of fingerprints. It takes $O ( n ^ { 3 } )$ running time and n is the number of fingerprints. For convenience, we still use $D ^ { \prime }$ to denote the distance matrix after the above-mentioned refinements on the original $D ^ { \prime }$ . So far $D ^ { \prime }$ is dense and meaningful.

![](images/1f2b1238918bc7d3927d121dc58236a4310e91a446d247da5356d9cd8063d737.jpg)



![](images/936705a770ae4f789c9f5cef77f9749727b3eec28a6c9bf6d4d65dbec6b9418b.jpg)



(b)   
Fig. 3.6 Fingerprint space. (a) 2D fingerprint space. (b) 3D fingerprint space

Similar to constructing stress-free floor plan, using $D ^ { \prime }$ as an input, MDS maps all $f _ { i }$ into a d-dimension Euclidean space. Figure 3.6a, b demonstrate the 2D and 3D visualization of fingerprints, respectively.

# 3.6 Mapping

If all fingerprints correspond with the sample locations in the stress-free floor plan, we are able to label each fingerprint with a real location. Such correspondence comes from the spatial similarity between stress-free floor plan and fingerprint space.

# 3.6.1 Feature Extraction

# 3.6.1.1 Corridor Recognition

Generally speaking, corridors in a building connect all other office rooms like hubs in a network. When people walk from one room to another, they need to pass through corridors. Such characteristics in real life are reflected in both stress-free floor plan and fingerprint space, as shown in Figs. 3.3a, b and 3.6a, b. We observe that fingerprints collected at corridors reside in core positions in fingerprint space. In terms of graph centrality [20], these fingerprints have a relatively large centrality values.

In graph theory, vertex centrality can be valued by degree, betweenness, closeness, etc. [20]. In our context, we adopt the betweenness centrality to identify corridor fingerprints. Conceptually, vertices that have a high probability to occur on a randomly chosen shortest path between two randomly chosen nodes have a high betweenness. Formally, in a graph $G = ( V , E )$ of vertices V and edges E, the betweenness centrality of a vertex $v \in V$ is defined as

Fig. 3.7 MST in 3D fingerprint space   
![](images/f82351174c00fb02b6ca6fb288f5bcd570404350173c7bd608d73630dcdbfce9.jpg)



$$
B (v) = \sum_ {s \neq v \neq t \in V} \frac {\sigma_ {s t} (v)}{\sigma_ {s t}}, \tag {3.2}
$$

where $\sigma _ { s t }$ is the number of shortest paths from s to t, and $\sigma _ { s t } ( v )$ is the number of shortest paths from s to t that pass through a vertex v.

Our solution first recognizes the fingerprints collected in corridors in the fingerprint space. According to the distances among fingerprints, we build the Minimum Spanning Tree (MST) [7] T that connects all fingerprints in F , as illustrated in Fig. 3.7. In addition, we compute the vertex betweenness for all vertices (fingerprints) in T and then distinguish fingerprints from corridors and other areas based on a betweenness watershed. The betweenness watershed value is determined by two parameters: (1) the area ratio $r _ { c }$ of corridors to entire floor plan (i.e., $r _ { c }$ = size(corridor)/size(all)), which is available when generating the stress-free floor plan; and (2) the largest gap of betweenness values of fingerprints. The area ratio $r _ { c }$ is used to cut a feasible interval of the betweenness distribution and then the watershed is finally determined by finding the largest gap of betweenness values in the feasible interval. In this sense, the betweenness watershed is an automatically determined value that depends on the specific scenario settings. In our experiment, the resulting cumulative distribution of betweenness is shown in Fig. 3.8. Roughly, nearly 8.6% have their betweenness larger than 8,200; while others all less than 7,000 (shown in Fig. 3.8). Obviously two groups of fingerprints are formed and we regard the one of larger betweenness as coming from corridors considering the structure shown in Fig. 3.2. Let $F _ { c }$ denote the set of fingerprints that are estimated collected from corridors.

# 3.6.1.2 Room Recognition

Removing $F _ { c }$ from the fingerprint space, we observe from both Fig. 3.6a, b that the remaining fingerprints form several clusters that are apparently spatially separated. To gather the fingerprints that are sufficiently close to each other, the k-means algorithm [17] (a classic clustering method) is chosen due to its computational efficiency. Thus all fingerprints in $F - F _ { c }$ are classified into k clusters (denoted by $F _ { R _ { i } } , i = 1 , 2 , \ldots , k )$ and in the k-means algorithm k is set to be the number of rooms in real floor plan. After clustering, all fingerprints of a same $F _ { R _ { i } }$ are considered from the same real rooms, though we cannot tell which specific room they are from. The next subsection focuses on this mapping problem.

![](images/e4f9db0cf4cf807067ebac1192a1631b289191625cfa3a54281f6b03e752ccbf.jpg)



Fig. 3.8 Betweenness distribution

# 3.6.1.3 Reference Point Mapping

After characterizing corridors and rooms, we are able to establish relationships between stress-free floor plan and fingerprint space, and we think doors are the keys. Particularly, we are intended to identify the fingerprints that are collected near doors. We define $\hat { f } _ { i }$ and $\hat { f } _ { i } ^ { \prime }$ as follows:

$$
(\hat {\boldsymbol {f}} _ {i}, \hat {\boldsymbol {f}} _ {i} ^ {\prime}) = \underset {\boldsymbol {f} \in F _ {R _ {i}}, \boldsymbol {f} ^ {\prime} \in F _ {c}} {\arg \min} \| \boldsymbol {f} - \boldsymbol {f} ^ {\prime} \|, \tag {3.3}
$$

where $\| \cdot \|$ denotes the 2-Norm in the fingerprint space.

Specifically, $\hat { \pmb f } _ { i }$ and $\hat { \pmb f } _ { i } ^ { \prime }$ locate as close as possible to a door in the floor plan but in opposite sides $( \hat { f } _ { i }$ inside the room and $\hat { \pmb f } _ { i } ^ { \prime }$ outside the room). Let $F _ { D } = \{ \hat { f } _ { i } ^ { ' } , i =$ $1 , 2 , \ldots , k \}$ denote the set of key corresponding points. Actually, the fingerprints in $F _ { D }$ can be organized in a chain in the MST T , as shown in Fig. 3.7. So we present $F _ { D }$ in a vector form as $F _ { D } = ( f _ { 1 } , f _ { 2 } , \dots , f _ { k } )$ .

# 3.6 Mapping

While in the stress-free floor plan, let $L _ { D } = ( l _ { 1 } , l _ { 2 } , . . . , l _ { k } )$ denote the set of sample locations in the corridor that are the closest to every door. The order of sample locations in $L _ { D }$ are in accord with their appearance from one side to the other side along the corridor. There are two possible ways $( \sigma _ { 1 } , \sigma _ { 2 } : F _ { D }  L _ { D } )$ mapping $F _ { D }$ to $L _ { D }$ :

$$
\sigma_ {1}: f _ {i} \mapsto \boldsymbol {l} _ {i} \tag {3.4}
$$

$$
\sigma_ {2}: f _ {i} \mapsto \boldsymbol {l} _ {k - i + 1}. \tag {3.5}
$$

In fact only one of $\sigma _ { 1 }$ and $\sigma _ { 2 }$ is the ground-truth. We use the distance constraints in both stress-free floor plan and fingerprint space to eliminate the ambiguity. We define $\pmb { p } = ( p _ { 1 } , p _ { 2 } , \dots , p _ { k - 1 } )$ and $p _ { i } = \parallel l _ { i + 1 } - l _ { i }$ . Similarly, $\pmb { p } ^ { \prime }$ is defined as $p ^ { \prime } = ( p _ { 1 } ^ { \prime } , p _ { 2 } ^ { \prime } , \ldots , p _ { k - 1 } ^ { \prime } )$ and $p _ { i } ^ { \prime } \ { = } \parallel \ f _ { i + 1 } - f _ { i } \parallel$ . The values of $p _ { i }$ and $p _ { i } ^ { \prime }$ can −be determined according to the distance matrix $D$ and $D ^ { \prime }$ , respectively. The cosine similarity of $\pmb { p }$ and $\pmb { p } ^ { \prime }$ , denoted by $s _ { 1 }$ , is calculated by

$$
\frac {\boldsymbol {p} \cdot \boldsymbol {p} ^ {\prime}}{\| \boldsymbol {p} \| \| \boldsymbol {p} ^ {\prime} \|}. \tag {3.6}
$$

While the similarity of $p$ and the reverse of $p ^ { \prime }$ , denoted by $s _ { 2 }$ , is also calculated. If $s _ { 1 } \geq s _ { 2 }$ , we adopt $\sigma _ { 1 }$ , otherwise $\sigma _ { 2 }$ . Without loss of generality, $\sigma _ { 1 }$ is chosen in the following discussion.

Up to now, a group of fingerprints $( F _ { D } )$ are labeled with real locations. The relationship between $F _ { D }$ and $L _ { D }$ can be further used to map other fingerprints to real locations.

# 3.6.2 Space Transformation

In this section, we discuss how to map fingerprints (fingerprint space) to locations (stress-free floor plan). We initially try floor-level transformation and then turn to room-level transformation for better accuracy.

# 3.6.2.1 Floor-Level Transformation

From the visualization of the stress-free floor plan and the fingerprint space, we observe that they are structurally similar but under trivial variations, including translation, rotation, or reflection. We use a transform matrix to solve such trivial variations.

Suppose a fingerprint $\begin{array} { r l r } { \boldsymbol { f } _ { i } } & { { } \in } & { \boldsymbol { F } _ { D } } \end{array}$ has its coordinate in the form of $\begin{array} { r l } { \mathbf { { x } } _ { i } } & { { } = } \end{array}$ $[ x _ { i } ^ { 1 } x _ { i } ^ { 2 } \dots x _ { i } ^ { d } ] ^ { \mathrm { T } }$ , where d is the dimension of the fingerprint space. And its corresponding location $\boldsymbol { l } _ { i } ~ \in ~ L _ { D }$ has a coordinate $\mathbf { y } _ { i } = [ y _ { i } ^ { 1 } y _ { i } ^ { 2 } \dots y _ { i } ^ { d } ] ^ { \mathrm { T } }$ in the stress-free floor plan. Let A denote the $d \times d$ transformation matrix and $B \ =$ $[ b _ { 1 } b _ { 2 } \dots b _ { d } ] ^ { \mathrm { T } }$ . We have $k = | F _ { D } |$ following equations

$$
\mathbf {y} _ {i} = A \mathbf {x} _ {i} + B. \tag {3.7}
$$

We re-write the k equations as

$$
H _ {i} z = G _ {i}, \tag {3.8}
$$

where $H _ { i } = [ x _ { i } ^ { \mathrm { T } } 1 ] , z = [ A B ] ^ { \mathrm { T } }$ , and $G _ { i } = y _ { i } ^ { \mathrm { T } }$ . Combining k equations as a matrix equation, we have

$$
H z = G, \tag {3.9}
$$

where $H _ { i }$ and $G _ { i }$ are the ith row of H and G, respectively.

The least square estimation [3] of above k equations gives

$$
\bar {z} = (H ^ {\mathrm{T}} H) ^ {- 1} H ^ {\mathrm{T}} G, \tag {3.10}
$$

which minimizes $\| \ G - H z \ \|$ .

So far, the transformation matrices A and B can be determined by z¯; thus we are able to map any fingerprint to the stress-free floor plan with a fixed location. For a fingerprint f with the coordinate $\pmb { x } = [ x ^ { 1 } x ^ { 2 } . . . \dot { x } ^ { d } ] ^ { \mathrm { T } }$ , the sample location that is closest to $A x + B$ is estimated as the real location of f .

# 3.6.2.2 Room-Level Transformation

From the experiment results, the unsatisfactory performance of floor-level transformation motivated us to design a fine-grained mapping solution. As previously mentioned, doors and fingerprints near doors are related, which further indicates that the rooms and the fingerprints from corresponding rooms are also related since a door belongs to only one room (i.e., the mapping from doors to rooms is injective). This fact enables room-level mapping instead of floor-level mapping.

Using MDS, the fingerprints from one room are transformed to d-dimension space. In the same way, the sample locations from the corresponding room are also mapped to d-dimension stress-free floor plan. Using doors and room corners as reference points, the fingerprints and sample locations are linked determinately by the transformation matrix above discussed. We perform the above step one room by one room and finally achieve a full mapping for all fingerprints after multiple steps of room-level transformation.

# 3.7 Experiments

# 3.7.1 Experiment Design

We develop the prototype of LiFS on the increasingly popular Android OS and on two Google Nexus S phones which support WiFi and accelerometer sensors. We conduct the experiment on one floor of a typical office building covering $1 6 0 0 \mathrm { m } ^ { 2 }$ , with the length of 70 m and width of 23 m. As shown in Fig. 3.2, the building contains 16 office rooms, of which 5 are large rooms of $1 4 2 \mathrm m ^ { 2 }$ , 7 are small ones with different sizes and the other 4 are inaccessible. Totally m 26 APs are installed, of which 15 are with known locations and are denoted in Fig. 3.2.

We sample the experiment floor plan approximately every $4 \mathrm { m } ^ { 2 } \ : ( 2 \times 2 \mathrm { m } \ : \mathrm { g r i d } )$ and obtain 292 sample locations over all accessible areas. Although this density is not a consistently best solution for all situations (including corridors, office rooms, meeting rooms, etc.,) however, it provides reasonable positioning accuracy for general office buildings. Afterwards, we conduct MDS and the results in 2D and 3D are depicted in Fig. 3.3a, b, respectively.

The experiment lasts five hours by four volunteers. Each volunteer holds a mobile phone in hand and walk through areas of interests. LiFS records the accelerometer readings to count walking distances and picks up RSS values along the paths. Fingerprints are recorded every 4∼5 steps during moving, which corresponds 2∼3 m under normal walking styles. Accelerometers work in two different frequencies: when detecting movements, they record sensory data with short intervals; otherwise a relatively long interval is adopted. WiFi is only scanned when the users are detected to be moving at a frequency of about 2 Hz.

Totally 600 user traces along with 16,498 fingerprint records are collected. These traces cover most of the areas of the experimental field. The small and large rooms are covered by at least 5 and 10 paths, respectively. In addition, the corridor is covered by more than 500 paths. Different paths vary not only in the areas they covered but also in lengths. The raw data are preprocessed and refined according to the RSS values and stability over time. After that, we select a half of these data for training and use the rest in operating phase.

# 3.7.2 Performance Evaluation

# 3.7.2.1 Fingerprint Space Generation

Before generating the fingerprint space, we obtain fingerprint points (i.e., points in the fingerprint space) and their pairwise distances from raw sensory data. Each point has a set of fingerprints. Fingerprints are distinguished by their RSS dissimilarities. Fingerprints with similar RSS features are attached to the same fingerprint points while fingerprints with large dissimilarities are sticked to different points. As user traces may be overlapped in the floor plan, fingerprints collected from different traces may be attached to the same point in the fingerprint space. In addition, fingerprints from a same sample location may be bounded to different points due to the RSS fluctuation. Hence, the threshold value of  can affect the fingerprint space generation a lot.

To obtain an appropriate  for generating fingerprint space, we first collect a series of fingerprints from the same location and calculate the maximum dissimilarity of these fingerprints. This procedure is repeated over a set of distinct locations (randomly selected), which results in a set of dissimilarity values. Finally we set the threshold epsilon as the mean value of these dissimilarity values, which is supposed to represent the average maximum dissimilarity of fingerprints from one distinct location.

Location error and room error defined as follows are used to examine the effects of .

$$
\text { Location\_Error } = \left| \left| \boldsymbol {l} (\boldsymbol {f}) - \boldsymbol {l} ^ {\prime} (\boldsymbol {f}) \right| \right|, \tag {3.11}
$$

$$
\text { Room\_Error } = \frac {1}{N} \sum_ {\boldsymbol {f} \in F} I (R (\boldsymbol {f}) \neq R ^ {\prime} (\boldsymbol {f})), \tag {3.12}
$$

where f is a fingerprint, $l ( f ) \left( R ( f ) \right)$ and $l ^ { \prime } ( f ) \left( R ^ { \prime } ( f ) \right)$ represent the ground truth location (room) in floor plan and in fingerprint space respectively, N is the number of fingerprints, F is the set of fingerprints, and I is an indicative function. For each fingerprint, its ground truth location (room) in fingerprint space is determined as the labeled-location of those predominant fingerprints with the same location (room) label.

We plot the cumulative distribution (CDF) of location error in Fig. 3.9. The impact of  on room error and the number of points are illustrated in Fig. 3.10. As from the results, location error and room error both increase when  changes from 10 to 100, while the number of points decreases from about 1,600 to 1. Too small or large values of  deteriorate the performance as fingerprints will be wrongly clustered. We choose $\epsilon = 3 0$ for further experiments, since 80% of fingerprints are accurate when $\epsilon = 3 0$ .

To obtain walking distances of fingerprints, we first evaluate the step counts estimation using the local variance threshold method. Paths with different lengths (from 5 to 200 footsteps) are designed for testing. Experiment results show an error rate of 2% in the number of steps. To further validate the performance under relatively long traces in different scenarios, we collect accelerometer data from different users by letting them walk a 300-step walking with their mobile phones in hand, in pockets, or in bags and perform the step counting algorithm. The results show that errors of 90% of all testing cases are limited within 5 steps, which is fairly accurate and suffices the requirements of distance estimation for LiFS. Although different users have various step sizes which result in different distances of the same number of steps, it will be shown later that MDS has outstanding performance in tolerance to measurement errors. The accumulative error of long paths brings about unobvious performance drop as only path segments (inter-fingerprint distances) are used by MDS and the distance of far-away points are calculated by aggregating many paths.

![](images/804ac14943b171cfc6ab0f683d7791b3f3c73584feb7e41daee5d1928ea47efd.jpg)



Fig. 3.9 CDF of location error on different 

![](images/c7be8612e95194a1bba3e87ce8af4ca61e2dd9ae3cf5fd41c4497f8f63747aaf.jpg)



Fig. 3.10 Room error rate vs. 

Totally, 795 points are generated for fingerprint space when $\epsilon = 3 0$ . First we assign the pairwise distances of these points with their measured walking distances and thus we get a connected network. By performing the Floyd-Warshall algorithm on the network, we obtain all the pairwise distances of 795 points. Finally, we conduct 2D and 3D MDS on these points and the results are shown in Fig. 3.6a, b, where each color denotes one room (or the corridor) in the floor plan. As seen from the figures, real floor plan structure is well reflected by MDS under constraints of walking distances.

# 3.7.2.2 Mapping Performance

We build the MST of the fingerprint points (Fig. 3.7) to calculate the betweenness centrality of each point. We sort all points by betweenness centrality in Fig. 3.8 and select those points with higher betweenness than the watershed value (8,000 in our experiments). All selected points are estimated from the corridor recognition. As illustrated in Fig. 3.11, most of the candidate corridor points are correctly extracted. However, some room points are also mixed among them and on the other hand, some true corridor fingerprints are not included. Hence, we refine the corridor recognition by iteratively performing MST and sifting low betweenness points until the MST of the remaining points form a single line, i.e., each point has at most one parent and one child in the MST. The final corridor points are depicted in Fig. 3.12.

The rest of fingerprint points, most of which are actually collected from rooms, are then clustered into 12 clusters (equal to the room number) using k-Means. The clustering results are shown in Fig. 3.13, where each different color indicates a cluster. The figure shows that most rooms can be recognized correctly while only a small portion of corridor points are mixed.

For each cluster, we identify a point in the corridors that has the shortest distance to all the points in a cluster as the reference point. The 12 reference points for

Fig. 3.11 MST of corridor points extracted using betweenness centrality   
![](images/dcead9e9cb57246b788d57a07fc09ac7c69920879252028d952472f92bc5635b.jpg)



Fig. 3.12 MST of corridor points

![](images/9c4e2dd3a89cce2e8d12c5194cc18f05b1b906f0bc61fe3eb22ac81f9cd20c6f.jpg)



Fig. 3.13 Clustering results by K-means

Fig. 3.14 Floor plan corridor vs. recognized corridor. Points marked with $\mathbf { \delta } ^ { \ast } \mathbf { X } '$ are reference points   
![](images/1d715bb925ad21bf937ade6e6e7ab42566beec10d84057eba569dc3ff148cd9b.jpg)



![](images/12c8661246f4a92522a533dc36c3fd692d4e3c4c7ecd30c5f45275cda2312fa0.jpg)



12 clusters are shown in Fig. 3.14. Some clusters may take the same point as its reference point, which is caused by the clustering errors. The reference points in the floor plan which link rooms to corridors are also presented in Fig. 3.14. The reference point sequences of floor plan and fingerprint space are $l = \{ 2 . 3 7 , 3 . 3 6$ , 9.40, 1.18, 1.16, 8.07, 1.17, 3.82, 2.51, 2.55, 1.25 and $l ^ { \prime } { = } \{ 0 . 3 3 , 2 . 1 2 , 1 2 . 9 8 , 1 , 3 1$ , 1,31, 10.17, 1.24, 10.17, 1.24, 5.99, 3.69, 1.18, 0} respectively. Let $l ^ { \prime \prime }$ be the reverse of $l ^ { \prime } .$ . The cosine similarities of l and $l ^ { \prime }$ and l and $l ^ { \prime \prime }$ are $s _ { 1 } = 0 . 9 7$ and $s _ { 2 } = 0 . 6 7$ , respectively. Since $s _ { 1 } > s _ { 2 } , l ^ { \prime }$ is adopted.

![](images/e097bed9a4e19d678d7398a904d9a6de55f40c943fd8e5d94f87ff793b5dfacd.jpg)  
Fig. 3.15 Fingerprints clusters vs. floor plan rooms

Up to now, the corresponding relationship of clusters to rooms is achieved. We then conduct the room-level transformation below. To understand the clusterroom mapping, we plot the 2D MDS results of each cluster and each room in Fig. 3.15. The mapping relations of 12 clusters and their corresponding rooms are also illustrated in Fig. 3.15. As seen from Fig. 3.15, the stress-free rooms are the same as in the floor plan while the 2D fingerprint points especially those from small rooms are a bit rambling. This is because the points are from multiple rooms and the measured distances are of errors.

We then map the points in each cluster to sample locations in its corresponding room by choosing the nearest neighbor for each point. As shown in Fig. 3.16, the mapping results are satisfactory as the mapping error of up to 96% points is lower than 4 m and the average error of is only 1.33 m.

# 3.7.2.3 Localization Error

Two metrics are designed for localization performance: location error and room error. Location error is defined as the Euclidean distance from the estimated location to the ground truth one. Room error means the error rate of fingerprints that are estimated to be in incorrect rooms. As the final outputs of LiFS, the RSS noises and mapping errors are simultaneously taken into account. We emulate 8,249 queries using real data on LiFS, and integrate all the localization results, as shown in Fig. 3.17. Each query contains a fingerprint and LiFS returns an estimated location.

![](images/b4cf558b14df2fdc4c0a7c96c0d246689b5bede1beacb16567aa833a753a29d3.jpg)



Fig. 3.16 CDF of mapping error   
![](images/2acd9ac7eaf870bb37a3583cc79d354051dcad0448ddc384130b14a7295b766b.jpg)



Fig. 3.17 CDF of localization error

We also implement RADAR [2], a famous and classical fingerprint-based localization system, and compare its performance with LiFS on the same experiment data. The reasons we choose RADAR as our performance reference are that LiFS adopts the standard algorithm of RADAR for fingerprint matching and our main purpose of this part of experiments is to show the location accuracy losses due to crowdsourced site survey, rather than how LiFS outperforms RADAR. As shown in Fig. 3.17, the average localization error of LiFS is 5.88 m, which is larger than RADAR (3.42 m). The performance of LiFS is comparable to the state-of-theart model-based approaches (larger than 5 m) reported in [29] and outperforms EZ (larger than 7 m) [6]. As shown in Fig. 3.17, localization error of 80% of fingerprints is under 9 m while about 60% is under 6 m. Some location errors are caused by the symmetric structure of rooms, but they are relatively small and will not contribute to room error. This accuracy is fairly reasonable, though not much impressive, as LiFS needs no site survey and no specific infrastructure.

While the basic performance of LiFS is as expected to be no better than the classical RADAR since the automatic generated radio map is inevitably less accurate than the manually constructed one, we demonstrate that the accuracy could be enhanced by trajectory matching with fingerprint sequences collected along a user trace, rather than a single fingerprint observation from one querying location. We examine the effect of the trajectory matching scheme by letting a user walk for a certain duration and then stop at a specific spot. The RSS and inertial sensor data along the user’s moving are record and fed to the localization server while the spot which the user stopped at is marked as the ground-truth location of this query. We collect multiple query trajectories from different users and integrate the localization results in Fig. 3.18. As portrayed in Fig. 3.18, the average localization error is about 2 m and the maximum error is bound within 8 m, reduced by more than 60% and 50% respectively compared to the basic localization scheme. The results not only outperform the RADAR but also are comparable to several recent localization schemes [16, 23]. While providing good accuracy, the computing time is no significantly larger than the nearest neighbor algorithm, since the accuracy improvement can be gained by short trajectories of several successive records. We also analyse the room error of all queries on LiFS and find that the room error rate is only 10.91%. As shown in Table 3.1, LiFS requires less sensors (only accelerometer) while produces comparable accuracy compare to a number of other localization methods. Such encouraging results show the benefits of mobility assisted localization and demonstrate the feasibility of LiFS in practical applications.

![](images/a22989efb82b7ee614fe17467a0751b9054056ea39750a5f2948f2b1b87d1539.jpg)



Fig. 3.18 Localization error of trajectory matching scheme (Denoted as LiFS -TM)

Table 3.1 Comparison with other localization systems 

<table><tr><td>Properties</td><td>EZ [6]</td><td>Zee [23]</td><td>Unloc [30]</td><td>LiFS</td></tr><tr><td>Methodology</td><td>Ranging</td><td>Fingerprinting</td><td>Fingerprinting</td><td>Fingerprinting</td></tr><tr><td>Sensors</td><td>GPS</td><td> $A/G/C^a$ </td><td>GPS/A/M/G/C</td><td>A</td></tr><tr><td>Floor plan</td><td>No</td><td>Yes</td><td>No</td><td>Yes</td></tr><tr><td>Device diversity</td><td>Yes</td><td>No</td><td>No</td><td>No</td></tr><tr><td>Experimental areas</td><td>Whole building (Office building)</td><td>Only hallways (Office building)</td><td>Whole building (Office &amp; mall)</td><td>Whole building (Office building)</td></tr><tr><td>Reported median accuracy</td><td>2 m (small area)7 m (large area)</td><td>7 m (using Horus)</td><td>1.7 m</td><td>4.5 m (LiFS)1.5 m (LiFS-TM)</td></tr><tr><td>Reported 80%ile accuracy</td><td>3.3 m (small area)10 m (large area)</td><td>13 m (using Horus)</td><td>3.5 m</td><td>7 m (LiFS)3.5 m(LiFS-TM)</td></tr></table>

aA Accelerometer, G Gyroscope, C Compass, M Magnetometer

# 3.8 Conclusion

By utilizing the spatial relation of RSS fingerprints, we are able to create fingerprint space in which fingerprints are distributed according to their mutual distances in real world. On this basis, we design and implement LiFS, an indoor localization system based on off-the-shelf WiFi infrastructure and mobile phones. The preliminary experiment results show that LiFS achieves low human cost, rapid system deployment, and competitive location accuracy. This work sets up a novel perspective to cut off human intervention of indoor localization approaches.

# References

1. Azizyan, M., Constandache, I., Roy Choudhury, R.: Surroundsense: mobile phone localization via ambience fingerprinting. In: Proceedings of ACM MobiCom, pp. 261–272 (2009)   
2. Bahl, P., Padmanabhan, V.N.: RADAR: an in-building RF-based user location and tracking system. In: Proceedings of IEEE INFOCOM, vol. 2, pp. 775–784 (2000)

3. Björck, Å.: Numerical Methods for Least Squares Problems, vol. 51. Society for Industrial Mathematics, Philadelphia (1996)   
4. Borg, I., Groenen, P.: Modern Multidimensional Scaling: Theory and Applications. Springer, New York (2005)   
5. Chen, Y., Lymberopoulos, D., Liu, J., Priyantha, B.: Fm-based indoor localization. In: Proceedings of the ACM MobiSys 2012, pp. 169–182 (2012)   
6. Chintalapudi, K., Padmanabha Iyer, A., Padmanabhan, V.N.: Indoor localization without the pain. In: Proceedings of ACM MobiCom, pp. 173–184 (2010)   
7. Cormen, T.: Introduction to Algorithms. The MIT Press, Cambridge (2001)   
8. Costa, J., Patwari, N., Hero, A., III: Distributed weighted-multidimensional scaling for node localization in sensor networks. ACM Trans. Sens. Netw. 2(1), 39–64 (2006)   
9. Ferris, B., Fox, D., Lawrence, N.: WiFi-slam using Gaussian process latent variable models. In: Proceedings of IJCAI, pp. 2480–2485 (2007)   
10. Floyd, R.: Algorithm 97: shortest path. Commun. ACM 5(6), 345 (1962)   
11. Griswold, W.G., Shanahan, P., Brown, S.W., Boyer, R., Ratto, M., Shapiro, R.B., Truong, T.M.: ActiveCampus: experiments in community-oriented ubiquitous computing. Computer 37(10), 73–81 (2004)   
12. Huang, J., Millman, D., Quigley, M., Stavens, D., Thrun, S., Aggarwal, A.: Efficient, generalized indoor WiFi graphslam. In: IEEE ICRA 2011, pp. 1038–1043 (2011)   
13. Jiménez, A., Seco, F., Prieto, C., Guevara, J.: A comparison of pedestrian dead-reckoning algorithms using a low-cost MEMS IMU. In: IEEE International Symposium on, Intelligent Signal Processing, pp. 37–42 (2009)   
14. Koo, J., Cha, H.: Autonomous construction of a WiFi access point map using multidimensional scaling. In: Pervasive Computing, pp. 115–132 (2011)   
15. LaMarca, A., Chawathe, Y., Consolvo, S., Hightower, J., Smith, I., Scott, J., Sohn, T., Howard, J., Hughes, J., Potter, F., et al.: Place lab: device positioning using radio beacons in the wild. In: Pervasive Computing, pp. 301–306 (2005)   
16. Liu, H., Jie, Y., Simon, S., Yan, W., Yingying, C., Fan, Y.: Accurate WiFi based localization for smartphones using peer assistance. IEEE Trans. Mobile Comput. 13(10), 2199–2214 (2014)   
17. MacQueen, J., et al.: Some methods for classification and analysis of multivariate observations. In: Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, vol. 1, p. 14 (1967)   
18. Montemerlo, M., Thrun, S., Koller, D., Wegbreit, B.: Fastslam: a factored solution to the simultaneous localization and mapping problem. In: Proceedings of AAAI, pp. 593–598 (2002)   
19. Ni, L.M., Liu, Y., Lau, Y.C., Patil, A.P.: LANDMARC: indoor location sensing using active RFID. Wirel. Netw. 10(6), 701–710 (2004)   
20. Opsahl, T., Agneessens, F., Skvoretz, J.: Node centrality in weighted networks: generalizing degree and shortest paths. Soc. Netw. 32(3), 245–251 (2010)   
21. Park, J., Charrow, B., Curtis, D., Battat, J., Minkov, E., et al.: Growing an organic indoor location system. In: Proceedings of ACM MobiSys, pp. 271–284 (2010)   
22. Pulkkinen, T., Roos, T., Myllymäki, P.: Semi-supervised learning for WLAN positioning. In: Honkela, T. (ed.) Artificial Neural Networks and Machine Learning, pp. 355–362. Springer, Heidelberg (2011)   
23. Rai, A., Sen, R., Chintalapudi, K.K., Padmanabhan, V.: Zee: zero-effort crowdsourcing for indoor localization. In: Proceedings of ACM MobiCom (2012)   
24. Sen, S., Radunovic, B., Choudhury, R.R., Minka, T.: You are facing the Mona Lisa: spot localization using phy layer information. In: Proceedings of the ACM MobiSys, pp. 183–196 (2012)   
25. Shang, Y., Ruml, W.: Improved MDS-based localization. In: Proceedings of IEEE INFOCOM, vol. 4, pp. 2640–2651 (2004)   
26. Shang, Y., Ruml, W., Zhang, Y., Fromherz, M.: Localization from mere connectivity. In: Proceedings of ACM MobiHoc, pp. 201–212 (2003)   
27. Shen, G., Chen, Z., Zhang, P., Moscibroda, T., Zhang, Y.: Walkie-Markie: indoor pathway mapping made easy. In: Proceedings of the USENIX NSDI, pp. 85–98. USENIX Association, Berkeley (2013)

28. Thrun, S., Burgard, W., Fox, D.: Probabilistic Robotics. MIT Press, Cambridge (2005)   
29. Turner, D., Savage, S., Snoeren, A.: On the empirical performance of self-calibrating WiFi location systems. In: 2011 IEEE 36th Conference on Local Computer Networks (LCN), pp. 76– 84 (2011)   
30. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.: No need to war-drive: unsupervised indoor localization. In: Proceedings of ACM MobiSys (2012)   
31. Woodman, O., Harle, R.: Pedestrian localisation for indoor environments. In: Proceedings of ACM UbiComp, pp. 114–123 (2008)   
32. Wu, C., Yang, Z., Liu, Y., Xi, W.: Will: wireless indoor localization without site survey. IEEE Trans. Parallel Distrib. Syst. 24(4), 839–848 (2013)   
33. Youssef, M., Agrawala, A.: The horus WLAN location determination system. In: Proceedings of ACM MobiSys, pp. 205–218 (2005)   
34. Zhang, X., Yang, Z., Wu, C., Sun, W., Liu, Y.: Robust trajectory estimation for crowdsourcingbased mobile applications. In: IEEE Transactions on Parallel and Distributed Systems, pp. 1–1 (2013)

# Chapter 4 Building Tomography: Automatic Floor Plan Generation

![](images/6230cc9ed673927fa8f2d3a007a558b78b260b621c780c2c2126f0d5a09c60ba.jpg)

Abstract Floor plan plays an essential role in many indoor pervasive and mobile applications, but its collection and on-site calibration are inconvenient and usually prohibitively costly for map providers. In this chapter, we explore the possibility of automatically generating floor plans. Based on the thoughts of human-centric sensing and crowdsourcing, the key idea is gathering mobility information from a large amount of contributing users to enrich the records to an applicable level so that the interior layout of a building emerges. An inexpensive and pervasive building tomography system is accordingly designed and implemented. No building knowledge is required and all sensor readings are collected by off-the-shelf smartphones.

# 4.1 Introduction

Building tomography is to explore indoor architectural layouts, usually represented as a floor plan, from outside. Floor plan illustrates a number of key spatial elements like rooms, corridors, walls, and other physical features at one level of a building. Dimensions are also drawn between the walls to specify room sizes and wall lengths. In some cases, spaces are labeled with their functions such as offices, meeting rooms, corridors, stairs, elevators, etc.

Floor plan plays an essential role in many indoor pervasive and mobile applications, such as human localization and navigation, asset management, smart space, etc. In addition, floor plan, attached with semantic meanings, provides basic geographical information for analyzing human mobility and social behavior.

We take indoor localization as an example to show the importance of floor plan. In many cases, the context of a location, mainly from a floor plan, is equally valuable to or even more valuable than location itself. For example, comparing with the absolute X–Y coordinates, it is more meaningful for users inside buildings to know room numbers or room usages such as office rooms, meeting rooms, or corridors. Furthermore, a route in a floor plan towards the nearest printer is more convenient than the printer’s location coordinates. Nevertheless, WiFi positioning is powerless on distinguishing rooms, identifying room usage, generating indoor maps, and characterizing user activities. So far, the acquisition of indoor floor plans mostly relies on human inputs.

However, floor plan collection and on-site calibration require permission and multi-party coordination, which are inconvenient and usually prohibitively costly for map providers. It is no small efforts even for giants like Google and Apple. Recently, researchers pay increasing efforts to leverage user mobility information for reduced dependency of indoor locating systems on site survey. Nevertheless, floor plan, as the ground truth, is still necessary.

The above-mentioned difficulties on cost and practicability of indoor positioning systems motivate us to explore the possibility of automatically generating floor plans. Our idea is based on human-centric sensing and crowdsourcing. The popularity of smartphones, with rich built-in sensors, enables fine-grained sensory records on human mobility and activity, as well as the characteristics of physical environments. Although the records from one user may be less useful, a large amount of contributing users can enrich the records to an applicable level so that the interior layout of a building emerges.

In our solution, people who live in, work in, or just walk through a building are the participants of crowdsourcing. They just behave routinely and the sensory data are recorded automatically by their smartphones. By analyzing user mobility, activity, and environmental signatures, some elements of floor plan can be identified. For example, a turn in a user’s moving trajectory often indicates corners, doors, or changes from one area to another. Climbing indicates stairs while long distance walking indicates corridors. Similarly, user activity like people gathering reflects the division and function of an area. Along with increasing user data, floor plan are gradually sketched out from coarse- to fine-grained.

We name this solution building tomography since the interior layout of a building is characterized from outside. Here “outside” means that third-party map providers are able to explore indoor floor plans without contacting estate management or performing laborious on-site investigation, though the sensory data are actually collected from unaware users inside a building.

To realize this idea, three major challenges remain unaddressed. First, erroneous sensor readings would corrupt user moving trajectory. Second, without ground truth information, how can the data from multiple users be geographically aggregated? Last but not the least, space regionalization and function recognition based on multisensor readings are insufficiently investigated, lacking of well-proven effective methods.

Our main contribution is to design and implement a building tomography system based on nowadays wireless and sensor technology. The system is inexpensive and pervasive. No building knowledge is required and no extra hardware needs to be deployed. All sensor readings are collected by off-the-shelf smartphones, and without user interventions or even attention. To validate this design, we deploy a prototype system and conduct experiments in a middle-size office building covering over 900 m2. The building contains 11 office rooms, one corridor, and two staircases, as shown in Fig. 4.1. Figure 4.2 illustrates the generated floor plan from our experiments. Although some details are necessarily omitted, the generated one accurately reflects real layout and is able to facilitate indoor localization as well as a number of other applications.

![](images/b2687035d10719c65d45c413a40b1fb394f5798035233f87d8e489c736b88dd5.jpg)



Fig. 4.1 Building floor plan   
![](images/54675f0dd1a20530e9d586cbe9c5c7030b5b1b5ad3d6417cedd00a3932019bce.jpg)



Fig. 4.2 Building tomography

The rest of this chapter is organized as follows. We discuss the related works in Sect. 4.2. Section 4.3 presents the system overview. Design details are studied in Sects. 4.4, 4.5 and 4.6. The prototype implementation is evaluated in Sect. 4.7. We conclude the work in Sect. 4.8.

# 4.2 Related Works

Automatic indoor floor plan generation attracts increasingly interests recently. Traditional SLAM technology [14] is a direction of research in robotics for jointly estimating the location of a robot and a map of an environment. However, the nature of wireless signal strength prohibits the use of standard SLAM techniques [9]. SLAM often relies on accurate control of a robot or builds probabilistic models of environments. Human mobility and activity, measured by smartphones, are not the input of SLAM.

With the prevalence of mobile phones, researchers have begun to leverage mobility information assisting localization. Users’ motion trajectories can be revealed through accelerometers, gyroscopes, or compasses [2, 5–7]. Furthermore, it is also possible to recognize user activity by analyzing mobility behaviors [2, 7]. Mobility information, as another dimension of space characterization other than RSS fingerprints, helps to increase location accuracy [2, 7] while reducing human cost [5, 6]. Albeit inspiring, automatic generation of floor plan remains an open issue.

Recently, several works attempt to realize this goal via mobile sensing. Smart-SLAM [17], an indoor tracking system, automatically constructs an indoor floor plan and radio fingerprint map for anonymous buildings using a smartphone. CrowdInside [1] is a crowdsourcing-based system for automatic construction of buildings floorplans using accurate motion traces with the help of points of interest in the indoor environment. A novel smartphone application is designed in [16] to capture, visualize and reconstruct homes, offices and other indoor scenes, leveraging smartphone sensors such as the camera, accelerometer, gyroscope and magnetometer, etc. IndoorCrowd2D [4] presents a smartphone-empowered crowdsourcing system for indoor scene reconstruction, also by utilizing the image information and sensory data in a coordinated way. JigSaw [10] extracts and gathers the position, size and orientation information of individual landmark objects from images taken by users to construct a floor plan. SenseWit [11] explores the possibility of indoor floor plan generation using only inertial sensor data, while additional WiFi fingerprints are combined in [13]. Differently, BatMapper [22] resorts to acoustic sensing on smartphone for floor plan construction, which calculate accurate distance measurements to nearby objects. Wision [12] exploits RF signals for indoor imaging, so as the same for several other works [18, 23]. The limitation, however, is that they usually need a moving robot as SLAM but can not work with smartphones.

# 4.3 System Overview

The basic flow of floor plan generation is as following. Each client (the application installed on user smartphones) collects the readings of built-in sensors. Using these readings, the client can make initiatory analysis on user movement. The client detects elementary motions such as stepping forward, turning, sitting down, and so on. The client records user movement and reports to the server through Internet. Movement traces received from clients are stored into a database at the server end. After collecting sufficient traces, the server aggregates collected traces and realizes an interior trace map. In this map, every turning point is represented as a vertex. An edge between two vertices A and B with weight k indicates that one can straightly walk from location A to B with k distance. The last thing is to recognize the function of different regions, and to mark each location with a tag (e.g. ‘corridor’, ‘room’, ‘stairs’, etc.). This outputs a floor plan of the interior layout of a building.

In practice, the server will receive daily reported data from users. Thus, the digital map is updated routinely to keep it up to date.

Our system is divided into three components:

1. Trace Collection This component is at the client end. It collects sensor readings and performs online analysis on user mobility. Then it first logs the results in smartphone memory, and further uploads to the server when connected to Internet.

![](images/4639d8f8ffdcc6d0983c38c0b58c4b95b2ffa8403283ed481d0b8670a2cbfcc9.jpg)



Fig. 4.3 System architecture

2. Trace Realization This component is at the server end. It aggregates traces collected from many different users, and constructs a trace map of user traces, which reflects the connectivity, geometry, and dimension of building interior.   
3. Map Generation This component is at the server end. It analyzes user actions (and other additional information) to regionalize the trace map into areas and infer the functionality or usage of different areas. It classifies corridors, rooms, stairs, elevators, and so on. It finally yields a map of the building.

Figure 4.3 summarizes the work flow of our system. We will discuss the details of these three components in the following sections.

# 4.4 Trace Collection

# 4.4.1 User Data Collection

Most modern smartphones have built-in sensors that measure motion, orientation, and various environmental conditions. These sensors are capable of providing raw data with medium precision and accuracy. Our system mainly exploits readings from three types of sensors: accelerometer, gyroscope and magnetometer, which provide acceleration, rate of rotation and geomagnetic field strength respectively. Mainstream smartphone operating systems like iOS and Android provide handy APIs to read measures from these sensors. We implement our data collection application on Google Nexus S with Android 2.3.1. The sample rate is 50 Hz.

Sensors use a standard 3-axis coordinate system to express data values. For above-mentioned sensors, the coordinate system is defined relative to the device’s screen when the device is held in its default orientation. The orientation of the cellphone, derived by a geomagnetic field sensor in combination with a accelerometer, is used to convert the readings into the world’s frame of reference. In future discuss, we assume the data are expressed in the world’s frame of reference.

Besides sensor readings, a client application scans WiFi APs every second. Each record contains a list of MAC addresses of overheard APs and their corresponding RSSs. The last available GPS positioning result is queried and attached to a trace for distinguishing which building it lies in.

In summary, a trace reported from a client to the central repository contains: (1) timestamped sensor readings; (2) timestamped WiFi signatures; and (3) last available GPS positioning result.

# 4.4.2 Dead-Reckoning

Accelerometer readings provide basic information of user motion. In principle, the displacement can be calculated by integrating acceleration twice with respect to time. Unfortunately, a critical problem makes this method impractical: errors accumulate rapidly with time. There are two main sources of errors.

1. The accelerometer itself generates noises which are presented in outputs.   
2. Residual component of gravity. Noises in magnetometer readings introduce errors in orientation output. A small orientation error causes a component of gravity to be projected onto the globally horizontal axes.

Such errors in displacement grow cubically in time when double integrated. The drift can reach 100 m after one minute of operation [20].

Several methods are proposed to solve the error accumulation problem in inertial navigation field [3, 8]. However, these methods require equipping inertial sensors on feet, which is not applicable for smartphones. People usually put their cellphones in pockets or hold in hands, but rarely bind them on feet.

Constandache et al. and Evennou and Marx [6, 7] provide the possibility of dead-reckoning based on step counting. We notice that during walking, every step generates a notable impulse in the accelerometer reading along z-axis (perpendicular to horizontal plane). Thus, user steps can be detected by capturing such impulses. We observe that each step begins with a positive acceleration, and reaches a summit soon. Then the acceleration drops down and becomes negative, and reaches a negative summit afterwards. Finally the step ends when the acceleration comes back to around 0. Based on this observation, we implement a finite state machine to detect user steps. Figure 4.4 shows the result of step detection.

Given the displacement and orientation of each step, a user’s movement trajectory can be depicted. The displacement is set to be a normal value of 72 cm in our experiment, which can be refined as a function of user’s height and weight.1 To calculate step orientation, we have two choices.

![](images/0b013bf601983c32f06d0407d4dbbf4342c3ecde2171e7b211280a6f843ed277.jpg)



Fig. 4.4 Accelerometer readings. Blue hollow dots are detected step beginnings, and red solid dots are detected step ends

1. Track a user’s orientation change using gyroscope. Gyroscope provides instantaneous angular velocity, thus integrating its readings with respect to time gives the amount of orientation change. Formally, the orientation $\theta _ { t _ { i } }$ of step i detected at time $t _ { i }$ is computed as:

$$
\theta_ {t _ {i}} = \theta_ {t _ {i - 1}} + \int_ {t _ {i - 1}} ^ {t _ {i}} \omega \mathrm{d} t, \tag {4.1}
$$

where ω is the reading of gyroscope. As a result, error in $\theta _ { t _ { i - 1 } }$ is brought into $\theta _ { t _ { i } }$ . 2. Use cellphone’s compass reading, which is derived by the combination of acceleration and magnetic field strength. Geomagnetic field gets fluctuated indoors, which causes errors in step orientation. Noises in accelerometer and magnetometer outputs contribute to orientation errors, too. Despite of that, the computation of each step is independent, and the error thus grows slower than gyroscope.

We implement both method and compare their deviation. As shown in Fig. 4.5, gyro-based method suffers heavily from accumulated errors, while compass-based method keeps deviation in an acceptable range. For this reason, we adopt the second method in our system.

![](images/19dd3eaa43aeb05990eeff8c8f6cb402cc3a608e6b84882218061427c3bba55c.jpg)



Fig. 4.5 Deviation of gyroscope and compass

# 4.5 Trace Realization

This section describes how to generate a trace map by aggregating user traces assimilated at central repository. For ease of explanation, we first discuss 1-floor building case. At the end of this section, we will discuss how to decompose the task of constructing trace maps of a multi-floor building into multiple 1-floor trace map construction.

Generally, user traces for a certain building can be divided into two types: (1) traces that completely lie inside the building; and (2) traces that contain outdoor part and indoor part. The construction of a trace map is incremental. It begins from a trace of the second type. The location of a building entrance can be extracted once a user passes it, and acts as the first reference point. After that, reference points are extracted from places of interest, such as a corner of a corridor, a door of a room, or the inside part of a room. This creates a base skeleton of the building.

Then other traces are added one by one. Each trace provides additional knowledge to the building interior. New places of interest are discovered and added as reference points, and new routes between two known reference points are learnt. The trace map is updated accordingly. Eventually a complete trace map of the building emerges after sufficient traces are added.

# 4.5.1 Entrance Discovery

To tell apart the two types of user traces, we try to detect the transition from outdoor to indoor (or from indoor to outdoor) at the client side. The difference of GPS signal strength between indoor and outdoor environments is the key. Conservative models and related experiments suggest that the attenuation in buildings can reach levels of 2.9 dB per meter of structure [15].

In experiment we found that GPS signal strength drops about 10 dB when a user enters a building, which can be used to figure out the entrance and/or exit of the building. Such information is reported to center repository together with a trace containing indoor and outdoor parts. A trace without such information attached is considered completely lying indoors. Discovered entrances and exits are ground truth reference points. For this reason, we first process all traces that pass through an entrance/exit of the building. The complete indoor traces are processed afterwards.

# 4.5.2 Reference Point Extraction

Our construction of building trace map is incremental, that is, we begin with a certain trace and merge others into it one by one. Figure 4.6 shows two examples of user traces after dead-reckoning. A user trace contains a series of points denoting user location at each step. The position relationship between any pair of points is known in a same trace. However, the relative position of points in different traces is unknown since they use different coordinate systems. Hence, all user traces need to be mapped to a same coordinate system.

For this purpose, each time a trace is added into the trace map, we first extract some reference points from it. These reference points are then mapped to existing reference points in the trace map. The coordinates of points in the trace are adjusted accordingly. Afterwards, the trace can be added into the trace map with consistent coordinates.

Entrances discovered in Sect. 4.5.1 are good reference points, but insufficient. First, some traces do not pass any entrances of the building, and hence lack such reference points. Second, a trace bias its actual trajectory due to accumulated errors. Middle-way reference points are needed to fix the bias regularly.

A user should make a number of turns while walking inside a building. Most turns are excellent reference points. People seldom make big turns when walking through straight corridors. If a user makes a turn, it is highly possible that s/he is at a place of interest. For example, a user would turn at a corridor corner. Before entering a room (from a corridor), a user would also make a turn if the door is on sidewall. And a user would eventually turn around inside the room before s/he exits.

![](images/77b7b3bb30fb48603da16e72379485d25186e7cc1108db6ac704024bed157540.jpg)



![](images/96c09d169505930b89a3199c97bec673259f575d819e13b273992cb2d611e26e.jpg)



Fig. 4.6 Two examples of user traces

![](images/43c0b4d1c6514ae153a31e6fd865884712ced7b7e30b2f94862a5eb0444719d9.jpg)



Fig. 4.7 Detecting user turns based on gyroscope readings. The red fills represent detected user turns

User turns can be detected by remarkable impulses in the gyroscope reading around z-axis. By integrating the data value of gyroscope reading we can even derive the angle of the turn. A turn is recognized as a valid reference point if its angle of rotation is larger than a threshold. In our implementation, turns larger than $3 0 ^ { \circ }$ are used as reference points. Figure 4.7 shows the result of turning detection.

During a turning, a user might walk several steps. For such cases, the centroid of the steps is taken as the reference point. Note that, a user might turn at a same place for several times. Thus we merge reference points that are close to each other (<5 m).

# 4.5.3 Reference Point Matching

We adopt WiFi fingerprint to match two reference points. During the data collection phase, a client keeps scanning WiFi APs and records their signal strength. The WiFi information during a turning event is used to generate WiFi fingerprint for its corresponding reference point i, represented as $\pmb { f } _ { i } = ( s _ { 1 } , s _ { 2 } , s _ { 3 } , \cdot \cdot \cdot , s _ { n } )$ , where $s _ { k }$ is the RSS for AP k.

For two fingerprints $\pmb { f } _ { i } = ( s _ { 1 } , s _ { 2 } , s _ { 3 } , \dots , s _ { n } )$ and $\pmb { f } _ { j } = ( t _ { 1 } , t _ { 2 } , t _ { 3 } , \dots , t _ { n } )$ , define RSS dissimilarity δ between $f _ { i } , f _ { j } \operatorname { a s } \delta _ { i j } = \| f _ { i } - f _ { j } \|$ , as in Eq. 3.1. Two reference points i, j are considered matched if their dissimilarity $\delta _ { i j }$ is less than a predefined threshold . Reference points not match to any existing reference point are added as new reference points in the trace map.

# 4.5 Trace Realization

It is not easy to find a threshold that suits for all reference points. To address this issue, we use the WiFi fingerprints of every step (and its corresponding point) along a trace. For each reference point i, define its surrounding $N _ { i }$ as

$$
N _ {i} = \{v \in V, \| \overline {{{i v}}} \| <   5 \mathrm{m} \}, \tag {4.2}
$$

where V is the set of every step’s representing point. Then i is assigned with a specific threshold $\epsilon _ { i }$ :

$$
\epsilon_ {i} = \max _ {j \in N _ {i}} \delta_ {i j} \tag {4.3}
$$

# 4.5.4 Drift Fixing

The reference point matching result can be used to fix accumulated drifts in a trace. This is done in an iterative manner. First, the position of every reference point is updated using information in the newly added trace, and then, these positions are used to fix drifts in all added traces.

The newly added trace is decomposed into several segments by reference points. Each segment has three parameters: source, sink, and the displacement from source to sink. The displacement is computed through summing up the displacement of every step between the source and the sink.

Segments of all added traces are put together. For each reference point pair $( i , j )$ , we have a set $S _ { i j }$ including all segments from i to j and those from j to i. The mean displacement from i to j is computed as:

$$
\overrightarrow {i j} = \frac {\sum_ {\mathbf {s} \in S _ {i j}} \mathbf {s}}{\left| S _ {i j} \right|}. \tag {4.4}
$$

The aggregating computation produces a displacement matrix describing the relative position between reference points in the trace map. The position of each reference point can be subsequently computed. A simple way is to assign the coordinate (0, 0) to an entrance point, and then compute its neighbors’ coordinates and extend them iteratively in breadth first search manner.

Now accumulated drifts in a trace can be fixed using the positions of reference points. For each point i in the trace, let $( x _ { i } , y _ { i } )$ denote its coordinate in the trace, and $( x _ { i } ^ { \prime } , y _ { i } ^ { \prime } )$ denote its coordinate in the trace map. Drifts are fixed segment by segment. For each point k in segment $\overrightarrow { i j }$ , its coordinate in trace map is computed as:

$$
\left(x _ {k} ^ {\prime}, y _ {k} ^ {\prime}\right) = \left(x _ {i} ^ {\prime} + \left(x _ {k} - x _ {i}\right) \frac {x _ {j} ^ {\prime} - x _ {i} ^ {\prime}}{x _ {j} - x _ {i}}, y _ {i} ^ {\prime} + \left(y _ {k} - y _ {i}\right) \frac {y _ {j} ^ {\prime} - y _ {i} ^ {\prime}}{y _ {j} - y _ {i}}\right) \tag {4.5}
$$

![](images/c787f3cc8854546ce8bcdab6aeefb6486803dae2bdded1a12269c90aba9ad5c3.jpg)



(a)

![](images/f6e976ff5a9f0fef6c8aacdc98a28b15e49d0a4b5834e9cde1e1fed628a53eb2.jpg)



(b)

![](images/149dd7e291aff3816940e570d2ac9a330c3687311533f2f1fe2f70c42868518e.jpg)



(c)

![](images/3aecd6d1145f79530a6ab126e55f69569c6146b22df8ddcb1c4b71507170f23a.jpg)



(d)

![](images/1dffdc21affc48a0322897134d01dee70349ddeb671d93cebce9f41b4a1401d7.jpg)



![](images/dd5d0af0b3d8e9e262970236aa7fe83a993ce83934ffd5820e53247cf84e8b37.jpg)



Fig. 4.8 A trace map evolves as traces being merged into it. Colored circles represent extracted reference points, and grey stars represent user trajectories. (a) After 1 trace added. (b) After 2 traces added. (c) After 5 traces added. (d) After 10 traces added. (e) After 15 traces added. (f) After 23 traces added

Figure 4.8 displays a typical example of our incremental trace map generation. The trace map evolves each time a new trace is merged into it, and eventually it depicts the layout of building interior.

# 4.5.5 Multi-floor Case

For a multi-floor building, we generate a trace map for each floor. Stairs, elevators and escalators are extracted as special reference points, which play the role of floor interfaces. Trace maps of a multi-floor building can be connected by these floor interfaces.

Skyloc [19] distinguishes different floors by GSM fingerprints. In addition, the combination of floor interfaces and their corresponding WiFi fingerprint forms the signature of a floor. Therefore, different floors can be identified by their signatures.

# 4.6 Map Generation

Once the trace map is constructed by aggregating user traces together, the next step is to recognize different areas and identify their functionality, such as corridors, rooms, stairs, or elevators.

# 4.6.1 Space Regionalization

Points are classified into different clusters (which are treated as areas). We adopt K-means clustering algorithm and use WiFi signals as features. Points can be partitioned into different rooms according to the observation that WiFi signals might encounter significant fluctuation when crossing the walls [21].

We verify our WiFi-based clustering and present the results in Fig. 4.14a where each color marks a cluster. Other clustering techniques such as Expectation Maximization (EM), DBScan, FathestFirst clustering are tried as well, but they are not consistently better than K-means.

After that, clusters are refined by taking point coordinates (which are available from the trace map) into consideration. Our key insights are (1) points distant from each other are unlikely to be grouped together, (2) the group of a point should be consistent with its neighbors, (3) one area should not be covered by multiple groups, and (4) areas generally have regular boundaries. Based on these observations, clustering errors are corrected by (1) assigning a point to the same cluster with the majority of its neighbors; (2) setting an area covered by two or more clusters to be the predominant one; and (3) adjusting boundaries of each area to be rectangular (or straight). Figure 4.14b illustrates the refinement result of Fig. 4.14a.

# 4.6.2 Functionality Recognition

We propose a Bayesian Model based approach for functionality recognition. We first formalize the characteristics of different function areas and present the probability model later. For office buildings, four types of area functionality are considered in our system: room, corridor, elevator, and stairs.

Elevators Elevators are distinctive landmarks in a building because RF signals are blocked and the acceleration patterns are unique in the elevators. The acceleration variance sequence of elevator-taking is defined as follows: a normal walking period, a short dwell time for waiting, walking into the elevator, a weight-loss (or overweight) period, standing statically inside, followed by another over-weight (or weight-loss), and walking out of the elevator. Figure 4.9 shows examples of such elevator motion traces.

Corridors Despite a few users may stop for a while in corridors, most of users are always walking. Consequently, users do not spend long time in the corridor. In addition, user trajectories generated in the corridor are dense, mostly straight and long, and with fewer turns.

Stairs It is a little difficult to differentiate between stairs and corridors. Nevertheless, acceleration patterns provide clues to tell apart two types of traces. For stairs, the variance of acceleration is much larger, which usually varies from 4 to $1 0 \mathrm { m } / \mathrm { s } ^ { 2 }$ as observed from real user traces.

![](images/1cacf9a4b7eea022305508711f9f7c66a8ac6e0aafbd922ff07f2791745992db.jpg)



![](images/512b0b51e4fa56a63329db4528ee594560d920ca52032a470d412e5a08554fe7.jpg)



Fig. 4.9 Accelerometer signature of using the elevator

Rooms User behaviors in office rooms also exhibit particular patterns. Users in rooms stay stationary most of the time. Even when users move inside the room, their trajectories incline to be short and contain more turns. Moreover, detecting colocation of people can also further differentiate semantic functions, such as meeting room, classroom, or normal office room.

Based on above observations, we select the following features.

• $m \in$ {moving, stat ic}: User movement states.   
$a \in$ beElevator, notElevator : Acceleration patterns indicating whether the measurements are from elevator or not.   
• $v \in \{ l a r g e , s m a l l \}$ : Variance of acceleration on direction of gravity.   
• $l \in \{ l o n g , s h o r t \}$ : Trajectory length.   
• $t \in \{ l o n g , s h o r t \}$ : Average stationary time spent in the area.   
• $s \in \{ n o r m a l$ , notDetected}: RF signals, such as WiFi and GSM signals.

All the features from a specific area form an observation $O = ( m , a , v , l , t , s )$ , which represents the signature of this area. With sufficient observations, a Bayesianbased approach is designed to identify functionality. Let $A _ { \mathrm { r } } , A _ { \mathrm { c } } , A _ { \mathrm { e } } .$ , and $A _ { \mathrm { s } }$ denote area functionality of room, corridor, elevator, and stairs, respectively. Define probability $p ( X | O _ { i } )$ as the posterior probability of marking area i with functionality $X$ , where $X \in \mathcal { A } = \{ A _ { \mathrm { r } } , A _ { \mathrm { c } } , A _ { \mathrm { e } } , A _ { \mathrm { s } } \}$ and $O _ { i }$ denotes the feature observation from $i ^ { \mathrm { { t h } } }$ area. Based on Bayesian theory, this posterior probability can be expressed as follows:

# 4.6 Map Generation

$$
p (X | O _ {i}) = \frac {p (O _ {i} | X) p (X)}{p (O _ {i})} = \frac {p (O _ {i} | X) p (X)}{\sum_ {X _ {j} \in \mathscr {A}} p (O _ {i} | X _ {j}) p (X _ {j})}, \tag {4.6}
$$

where $p ( O _ { i } | X )$ means the prior probability of $O _ { i }$ based on area functionality X, $p ( X )$ means the probability of area functionality X. For an observation $o \_ =$ $( m , a , v , l , t , s )$ , assuming that each dimension in O is independent from each other, $p ( O | X )$ can be calculated by the formulae below:

$$
p (O | X) = p (m, a, v, l, t, s | X) = \prod_ {o \in \{m, a, v, l, t, s \}} p (o | X). \tag {4.7}
$$

Then the core task is to calculate $p ( o | X )$ and $p ( X )$ , as presented below.

Every trajectory is divided into several segments based on its acceleration pattern. Each segment corresponds to one kind of motion state. For example, consider a trajectory of one user walking towards her office room from the building entrance, opening the door and entering her room, moving to her seat and sitting down for a while. Then the trajectory will be divided into four segments: the first segment(moving) from entrance to her office door, the second segment(static) when opening the door, the third segment(moving) after opening the door but before sitting down, and the last(static) after sitting down. From previous sections, we have already obtained the following information of each segment: approximate coordinates in the trace map; and segment length, represented by the step counts.

The user movement state m and average stationary time spent t can be easily acquired by above results. If t is longer than a threshold, for example, 15 min, t is assigned as long; otherwise $t = s h o r t$ . Similarly, if RF signals can not be detected or are extremely weak, s is set to be notDetected; otherwise, s is treated as normal. As for the value of variance v on the direction of gravity, it can be directly calculated from the accelerometer readings.

So far, for the observation $\textit { O } ~ = ~ ( m , a , v , l , t , s )$ of a segment, only the acceleration pattern a is unavailable. We design a Finite State Machine (FSM) to detect the specific pattern produced in elevators, depending on the defined acceleration state transition. As illustrated in Fig. 4.10, the FSM consists of seven states: $S _ { 0 }$ is the initial state, $S _ { 3 }$ and $S _ { 4 }$ indicate detected weight-loss and over-weight, respectively. $S _ { 5 }$ suggests that an over-weight or weight-loss is detected following $S _ { 3 }$ or $S _ { 4 } . \ S _ { 6 }$ is the terminal state of walking out of the elevator. If the FSM returns a positive result, then the segment is probably in the elevator and a is assigned the value of beElevator. Otherwise, $a = n o t E l e v a t o r$ .

After quantifying all observation tuples, the final probability distribution of all $p ( o | X )$ is presented in Table 4.1, where probability values are distributed into five levels: very high (VH), high (H), medium (M), low (L), very low (VL). The values of these five levels may vary a little for different environments. In our experiment, we use the values of 0.9, 0.7, 0.5, 0.3, 0.1, respectively.

The values of $p ( X )$ are determined by the counts of corresponding records. Without prior knowledge, we start with equal probability and conduct iterative calculation of $p ( X )$ to achieve more precise values. Concretely, every area gets tagged with a type of functionality in each iteration, so the result can be utilized to revise $p ( X )$ for further iterations. Formally, for each iteration, the $p ( X )$ is assigned as:

![](images/ece039e41cb074d871dc383136b38efaacb6aff021839079e3784aa4bb91789e.jpg)



Fig. 4.10 The finite state machine for detecting elevator acceleration patterns

Table 4.1 Prior probabilities of functionality identification on different observations 

<table><tr><td rowspan="2"></td><td colspan="2">m</td><td colspan="2">a</td><td colspan="2">v</td><td colspan="2">l</td><td colspan="2">t</td><td colspan="2">s</td></tr><tr><td>Moving</td><td>Static</td><td>be-Elevator</td><td>not-Elevator</td><td>Large</td><td>Small</td><td>Short</td><td>Long</td><td>Short</td><td>Long</td><td>Strong</td><td>Weak</td></tr><tr><td>Room</td><td>L</td><td>VH</td><td>L</td><td>M</td><td>VL</td><td>M</td><td>H</td><td>L</td><td>L</td><td>H</td><td>M</td><td>M</td></tr><tr><td>Corridor</td><td>H</td><td>L</td><td>L</td><td>M</td><td>L</td><td>M</td><td>L</td><td>H</td><td>M</td><td>L</td><td>M</td><td>M</td></tr><tr><td>Elevator</td><td>L</td><td>H</td><td>VH</td><td>VL</td><td>L</td><td>M</td><td>M</td><td>L</td><td>M</td><td>L</td><td>VL</td><td>H</td></tr><tr><td>Stairs</td><td>H</td><td>L</td><td>L</td><td>M</td><td>VH</td><td>VL</td><td>L</td><td>M</td><td>M</td><td>L</td><td>M</td><td>M</td></tr></table>

$$
p (X) = \frac {N _ {X}}{N}, \tag {4.8}
$$

where $N _ { X }$ is the number of records tagged with X and N is the total number of records.

In conclusion, given a trajectory segment, we calculate the probability $p ( X | O )$ for all $X ~ \in ~ \mathcal { A } \ = \ \{ A _ { \mathrm { { r } } } , A _ { \mathrm { { c } } } , A _ { \mathrm { { e } } } , A _ { \mathrm { { s } } } \}$ . Then the functionality X which maximizes $p ( X | O )$ is designated as the corresponding functionality of this segment. Formally, the functionality is identified as X where

$$
X = \underset {X \in \mathscr {A}} {\arg \max} p (X | O). \tag {4.9}
$$

When the functionality of all records covering an area is recognized, the functionality of the area can be simply determined by using the most predominant functionality type.

Especially, although beyond the scope of this article, we speculate confidently that the semantic function of the room can be further judged by detecting various human activities. For example, if quite a lot users are detected to be co-located in one room, which can be detected easily by timestamps and user locations, then the room is likely to be a meeting room or a classroom; otherwise, it tends to be a regular office room.

# 4.7 Experiments

# 4.7.1 Experiment Setup

Traces are collected by three volunteers spending three hours in a building, covering about $9 0 0 { \mathrm { m } } ^ { 2 }$ indoor areas. The step length of volunteers is set 0.72 m (derived from their heights). The building has 11 rooms and 2 washrooms and a corridor connecting them. The size of each room is $8 . 5 \times 7 . 5$ m. The trajectories of volunteers cover 9 rooms because the other 2 rooms are not accessible.

# 4.7.2 Reference Point Matching Performance

Reference point matching is an important step in our trace realization. As discussed in Sect. 4.5.3, two reference points are considered matched if their WiFi fingerprint dissimilarity is smaller than a threshold.

Reference points are located at 15 physical positions, and naturally classified into 15 groups $R _ { 1 } , R _ { 2 } , \ldots , R _ { 1 5 }$ . The mean dissimilarity $\bar { \delta } _ { i j }$ between two reference point groups $R _ { i } = \{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } \}$ and $R _ { j } = \{ q _ { 1 } , q _ { 2 } , . . . , q _ { m } \}$ is computed as:

$$
\bar {\delta} _ {i j} = \frac {\sum_ {p \in R _ {i}} \sum_ {q \in R _ {j}} \delta_ {p q}}{| R _ {i} | | R _ {j} |} \tag {4.10}
$$

Figure 4.11 demonstrates the matrix of dissimilarity $\bar { \delta } _ { i j }$ between reference point groups at different physical locations. As groups are ordered based on their physical locations, two groups close in space are also close in the matrix. Generally, co-group dissimilarity is smaller than cross-group dissimilarity. In addition, the dissimilarity grows larger as the physical distance between two reference points gets larger.

The accuracy of reference point matching is evaluated based on its FP (false positive) and FN (false negative) rates. A false positive is that two reference points at different physical location are matched, and a false negative is that two reference points at same physical location are not matched. FP and FN rates are sensitive to the threshold  used in matching determination. Figure 4.12 shows the FP and FN rates when different threshold is taken. Taking larger threshold will reduce FN rate while increasing FP rate, and vice versa. A fixed threshold works well in one physical location may perform poorly in another location. What’s more, it is difficult to find a balance between FP and FN. On contrast, our adaptive threshold can suit most locations and performs better, as shown in Fig. 4.13.

Fig. 4.11 Dissimilarity matrix   
![](images/3b11f8df9a65b5327730f0f05c4613ff07f09a9696daf6f2ed91c8bf2f8ed90f.jpg)



Fig. 4.12 FP/FN using different fixed threshold   
![](images/5866929e7dddf56772a7162f7c6db6a8fb4f6df4859cbc7ef02425ea6895dca6.jpg)



# 4.7.3 Regionalization Performance

We conduct clustering on the trace map using K-means algorithm to regionalize space. We vary the value of K from 11 to 20 and study the performance case by case. The results suggest that K  16 achieves the best performance in outlier rate base.

Fig. 4.13 Tradeoff between FP and FN   
![](images/5dd5d1da066a52831162ccd6b8fbeb0891cddb11dc478830d5821e417d8247d1.jpg)



![](images/a5a7229f25d2a9dfdd1e46818d6bf469adf598703b3ff3d84e44025bcc22ffc8.jpg)



(a)

![](images/3842f5ca583c2d13d22a787ee858653cc82e72cd061265cf48b2d20d79046167.jpg)



Fig. 4.14 Space regionalization. (a) Primary space regionalization. (b) Corrected space regionalization

Hence, $K = 1 6$ is chosen for following analysis. The primary result of K-means on $K = 1 6$ is illustrated in Fig. 4.14a, where some clusters are overlapped, resulting in outlier errors. We correct those outliers by using available location information derived from the trace map. As seen from Fig. 4.14b, space regionalization yields following results: (1) All nine rooms are correctly regionalized. (2) Corridors are divided into four segments. (3) Rooms and corridors are correctly differentiated.

With all areas recognized, the size of each area is estimated as the size of the convex hull of the corresponding cluster. As shown in Fig. 4.15, most of rooms are estimated with errors around $\mathrm { \bar { 7 } m } ^ { 2 }$ . We notice that all estimated room sizes are smaller than the real values. This is caused by (1) users rarely walk close to the walls and corners of the rooms, i.e., user active areas are smaller than the actual size of rooms; and (2) the step lengths vary from user to user. Hence, with a more precise step length, the size estimation will keep with reality better. As for the corridors, the estimated size is much larger than the real one. This is because the joint areas of corridors and rooms are incorporated to corridors. The total size of the building can be derived as well. From the trace map, the length and width of the building are estimated as 50 and 17 m, leading to a total size of $8 5 0 \mathrm { m } ^ { 2 }$ , which is slightly smaller than the real indoor size of about $9 0 0 { \mathrm { m } } ^ { 2 }$ .

![](images/2459844e435bab39eecf9da3e4f99c2bac6c59b1ac65ebbce37d919341da39be.jpg)



Fig. 4.15 Area size estimation

Table 4.2 Confusion matrix for functionality recognition 

<table><tr><td></td><td>Corridor</td><td>Room</td><td>Stairs</td><td>Elevator</td><td>FP (%)</td><td>FN (%)</td><td>Count</td></tr><tr><td>Corridor</td><td>33</td><td>0</td><td>2</td><td>0</td><td>5.7</td><td>5.7</td><td>35</td></tr><tr><td>Room</td><td>1</td><td>28</td><td>0</td><td>0</td><td>0</td><td>3.4</td><td>29</td></tr><tr><td>Stairs</td><td>1</td><td>0</td><td>25</td><td>0</td><td>7.4</td><td>3.8</td><td>26</td></tr><tr><td>Elevator</td><td>0</td><td>0</td><td>0</td><td>11</td><td>0</td><td>0</td><td>11</td></tr><tr><td>Overall</td><td></td><td></td><td></td><td></td><td>4.0%</td><td>4.0%</td><td>101</td></tr></table>

# 4.7.4 Functionality Recognition

To validate the characteristics for functionality recognition, we perform the proposed Bayesian based method and use the following probability settings: VH = 0.9, H = 0.7, M = 0.5, L = 0.3, VL = 0.1. We use an equal probability of 1/4 for initial iteration. Table 4.2 shows the final results on part of our experiment data. As seen from the table, functionality of most traces can be identified correctly, among which some are easier due to distinctive patterns. For example, the false positive and false negative rates of elevator are both zero. In contrast, the stairs are easy to be mixed with corridors, with a false positive rate of 7.4%. Overall, the proposed approach achieves 4.0% false positive and 4.0% false negative rate.

We then conduct the recognition procedure on the regionalized trace map to recognize area functionality. With no elevator in our experiment building, we only consider the rest area functionality, i.e., corridors, stairs, and rooms. The final result is shown in Fig. 4.2, where all areas are successfully identified.

# 4.8 Conclusion

We find that many mobile and pervasive applications rely on indoor floor maps, but it is difficult to obtain a large collection of floor maps worldwide. In this study, we implement a remote building tomography system, which discovers indoor layouts through utilizing user motion information detected by off-the-shelf smartphones. Preliminary results prove the feasibility of our attempt. A direction of the future work is to adapt the techniques to various buildings and environments.

# References

1. Alzantot, M., Youssef, M.: Crowdinside: automatic construction of indoor floorplans. In: Proceedings of the 20th International Conference on Advances in Geographic Information Systems, pp. 99–108. ACM, New York (2012)   
2. Bao, L., Intille, S.S.: Activity recognition from user-annotated acceleration data. In: Pervasive Computing, pp. 1–17 (2004)   
3. Beauregard, S.: Omnidirectional pedestrian navigation for first responders. In: 4th Workshop on Positioning, Navigation and Communication, WPNC ’07, pp. 33–36 (2007)   
4. Chen, S., Li, M., Ren, K., Fu, X., Qiao, C.: Rise of the indoor crowd: reconstruction of building interior view via mobile crowdsourcing. In: Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems, pp. 59–71. ACM, New York (2015)   
5. Constandache, I., Bao, X., Azizyan, M., Choudhury, R.R.: Did you see bob? Human localization using mobile phones. In: Proceedings of the ACM MobiCom, pp. 149–160. ACM, New York (2010)   
6. Constandache, I., Choudhury, R., Rhee, I.: Towards mobile phone localization without wardriving. In: Proceedings of the IEEE INFOCOM, pp. 1–9 (2010)   
7. Evennou, F., Marx, F.: Advanced integration of WiFi and inertial navigation systems for indoor mobile positioning. EURASIP J. Adv. Sig. Process. 2006, 1–12 (2006)   
8. Feliz, R., Zalama, E., Gómez, J.: Pedestrian tracking using inertial sensors. J. Phys. Agents 3(1), 35–42 (2009)   
9. Ferris, B., Fox, D., Lawrence, N.: WiFi-slam using gaussian process latent variable models. In: Proceedings of IJCAI, pp. 2480–2485 (2007)   
10. Gao, R., Zhao, M., Ye, T., Ye, F., Wang, Y., Bian, K., Wang, T., Li, X.: Jigsaw: indoor floor plan reconstruction via mobile crowdsensing. In: ACM International Conference on Mobile Computing and Networking (MobiCom) (2014)   
11. He, Y., Liang, J., Liu, Y.: Pervasive floorplan generation based on only inertial sensing: feasibility, design, and implementation. IEEE J. Sel. Areas Commun. 35(5), 1132–1140 (2017)   
12. Huang, D., Nandakumar, R., Gollakota, S.: Feasibility and limits of Wi-Fi imaging. In: Proceedings of the 12th ACM Conference on Embedded Network Sensor Systems, pp. 266– 279. ACM, New York (2014)   
13. Jiang, Y., Xiang, Y., Pan, X., Li, K., Lv, Q., Dick, R.P., Shang, L., Hannigan, M.: Hallway based automatic indoor floorplan construction using room fingerprints. In: ACM International Conference on Ubiquitous Computing (UbiComp) (2013)

14. Montemerlo, M., Thrun, S., Koller, D., Wegbreit, B.: Fastslam: a factored solution to the simultaneous localization and mapping problem. In: Proceedings of AAAI, pp. 593–598 (2002)   
15. Parsons, J.D.: The Mobile Radio Propagation Channel. Wiley Ltd, Chichester (2000)   
16. Sankar, A., Seitz, S.: Capturing indoor scenes with smartphones. In: Proceedings of the 25th Annual ACM Symposium on User Interface Software and Technology, pp. 403–412. ACM, New York (2012)   
17. Shin, H., Chon, Y., Cha, H.: Unsupervised construction of an indoor floor plan using a smartphone. IEEE Trans. Syst. Man Cybern. C Appl. Rev. C (Appl. Rev.) 42(6), 889–898 (2012)   
18. Tan, B., Chetty, K., Jamieson, K.: Thrumapper: through-wall building tomography with a single mapping robot. In: Proceedings of the 18th International Workshop on Mobile Computing Systems and Applications, pp. 1–6. ACM, New York (2017)   
19. Varshavsky, A., LaMarca, A., Hightower, J., de Lara, E.: The SkyLoc floor localization system. In: Proceedings of the IEEE PerCom, pp. 125–134 (2007)   
20. Woodman, O., Harle, R.: Pedestrian localisation for indoor environments. In: Proceedings of the ACM UbiComp. ACM, New York (2008)   
21. Wu, C., Yang, Z., Liu, Y., Xi, W.: WILL: wireless indoor localization without site survey. In: Proceedings of the IEEE INFOCOM (2012)   
22. Zhou, B., Elbadry, M., Gao, R., Ye, F.: Batmapper: acoustic sensing based indoor floor plan construction using smartphones. In: Proceedings of the 15th Annual International Conference on Mobile Systems, Applications, and Services, pp. 42–55. ACM, New York (2017)   
23. Zhu, Y., Zhu, Y., Zhao, B.Y., Zheng, H.: Reusing 60ghz radios for mobile radar imaging. In: Proceedings of the 21st Annual International Conference on Mobile Computing and Networking, MobiCom ’15 (2015)

# Part III

# Facilitating Maintenance: Making It

# Sustainable

This part consists of two chapters. The first chapter presents an adaptive technique for automatic radio map updating, which guarantees the quality of location services over long-term deployment. The second chapter investigates a peer-to-peer navigation mode that does not rely on any prior installed location services.

# TO RADIO MAP UPDATING:

Beware of little expenses; a small leak will sink a great ship.

– Benjamin Franklin

# Chapter 5 Adaptive Radio Map Updating

![](images/829e61eed1d4daf6a01e1f85c550a8bb7c1e18d63ab7d6a2047c891d3f961aef.jpg)

Abstract A primary concern for WiFi fingerprint-based technologies to be fully practical is to combat harsh indoor environmental dynamics, especially for longterm deployment. Despite numerous research, the problem of radio map adaptation has not been sufficiently studied and remains open. In this chapter, we propose AcMu, an automatic and continuous radio map self-updating service for wireless indoor localization that exploits the static behaviors of mobile devices.

# 5.1 Introduction

Thanks to the wide deployment and availability of WiFi infrastructure, WiFi fingerprint-based indoor localization has become one of the most attractive techniques for ubiquitous applications [15, 18, 19, 24, 31, 36, 41]. Particularly, two key issues of fingerprint-based scheme, site survey (a.k.a. radio map construction or calibration) and localization errors have been extensively studied recently. Many researchers have demonstrated the feasibility of automatic construction of a radio map by crowdsourcing and thus eliminate the cumbersome calibration [18, 19, 31]. As for accuracy, human mobility captured by smartphone built-in inertial sensors has been incorporated to reduce location errors to meter or sub-meter level [24, 25, 37]. Although these innovations have prompted fingerprint-based localization to become the preferred method, a key enabler to make it fully practical still remains unsolved: radio map updating.

It is well-known that RSS is vulnerable to environment dynamics, including transient interferences such as moving subjects, door opening and closing, and prolonged changes like variations of light, temperature, humidity and weather conditions. Dense multipath in complex indoor environments further exaggerates the RSS temporal fluctuations. Hence real-time RSS samples measured in localization phase could drastically deviate from those stored in the initial radio map. As a consequence, a static radio map may gradually deteriorate or even break down, especially over long-term deployment, leading to grossly inaccurate location estimation. To overcome this problem, an intuitive solution is to repeat the site survey procedure, which is, however, labor-intensive and time-consuming. Early efforts resort to a set of fixed reference anchors additionally deployed to draw fresh RSS observations to adapt the radio map [13, 17, 22, 34, 38]. Deploying extra devices, however, is expensive and not scalable, hampering the intrinsic advantages of fingerprint-based localization. Crowdsourced radio maps pave the way for automatic generation, however, most of them are designated for automatic construction instead of continuous adaptation and thus no specific and practical solution has emerged as yet [18, 19, 31].

Nowadays mobile phones possess powerful computing, communicating, and sensing capability, and act as an increasingly important information interface between humans and environments. Thus in this chapter, we investigate the question: Is it possible to automatically and continuously update the radio map using merely mobile devices without additional hardware and extra human intervention? Insights from mobile computing and crowdsourcing shed lights on a promising answer. We notice that most mobile devices (mainly iPads and smartphones) are actually kept static for some time. Particularly, according to our primary tracking of campus users, we find that the percentage of static time can surprisingly exceed 80% for most users. A mobile device, when in static state, can sufficiently serve as a movable reference point to collect abundant fresh RSSs for its current position. Specifically, one device can contribute measurements at multiple locations within a day and numerous ordinary devices can be leveraged. Hence new data can be gathered fast and effectively. A sufficient amount of newly crowdsourced data, distributed at different points, can be fused to adapt the current in-service radio map, provided that adequately accurate locations of these reference points are attained [24, 37]. This essentially means that the radio map is possible to be continuously updated. And if the radio map is up-to-date, the quality of location service can be persistently maintained, even over a long term, which in return enables accurate localization of future reference points from mobile devices for map updating.

Motivated by these observations, we propose AcMu, an Automatic and Continuous radio Map Updating service for wireless indoor localization that exploits the static behavior of mobile devices. AcMu employs ordinary users’ mobile devices as movable reference points to collect the newest fingerprints when the devices are static at specific locations. To accurately locate these reference points, we monitor moving trajectories of mobile users using inertial sensors and propose a novel localization algorithm based on trajectory matching, which superimposes a moving trajectory into the location space with both fingerprints and geometric constraints. Once an enough amount of reference points, attached with estimated locations, are gathered, we trigger a map updating procedure to adapt the current radio map. Specifically, we learn a predictive relationship between RSSs of reference points and other locations from the initial radio map using partial least squares regression (PLSR), and, on this basis, derive new fingerprints at each location with the real-time RSSs from the reference points. The rationale is that the underlying relationship of how RSS depends on its neighbors would be relatively stable over time since neighboring locations probably reflect similar dynamic changes in the surrounding environments, although the RSS values may change for individual locations [22, 34]. Afterwards, the radio map is accordingly adapted using the newly arriving data. The updated radio map then substitutes the previous version for all upcoming location queries thereafter.

We prototype AcMu and conduct experiments in a typical building for 20 days over a period of more than 6 months. Experiment results demonstrate that AcMu outperforms existing approaches and effectively accommodates the RSS variations caused by environmental dynamics, with average prediction error of around 5 dB. Moreover, by maintaining an up-to-date radio map, AcMu provides up to 2× improvement on the localization accuracy for existing localization techniques.

In the rest of the chapter, we first review the related works in Sect. 5.2 and provide the background in Sect. 5.3. A system overview is presented in Sect. 5.4. Then we detail the system design in Sect. 5.5 and present the implementation and evaluation in Sect. 5.6. We discuss some limitations and open issues in Sect. 5.7. We conclude this chapter in Sect. 5.8.

# 5.2 Related Works

Among a large body of works in the literature of indoor localization, the design of AcMu is closely related to the following categories of research.

Radio Map Construction Smartphones with various built-in sensors have been thoroughly exploited to reduce or eliminate site survey efforts of radio map construction. Pioneer works including LiFS [31], Unloc [24], Zee [18], WILL [26], etc., design crowdsourcing approaches to employ mobile users to participate in data collection. Recent innovations such as Walkie-Markie [19], Jigsaw [7] and CrowdInside [1] attempt to further reconstruct an indoor floor plan leveraging crowdsensed data. EZ [6] alternatively attempts to avoid the need of a prior radio maps and AP knowledge by modeling and solving the physical constraints of abundant measurements. These works mainly aim at easing the site survey to construct radio maps in the initializing phase, and typically requires abundant crowdsourced start data [19, 31] or detailed digital floorplans [18]. AcMu is orthogonal to them in focusing on radio map updating during serving phase to cope with fingerprint variations over time and can work with any amount of crowdsourcing data and does not require a digital floorplan. Having said that, AcMu is still compatible to the crowdsourced radio maps constructed by using schemes in these works.

Radio Map Adaptation Considering environmental dynamics, early systems like LANDMARC [17] and LEASE [13] utilize reference anchors intentionally deployed at fixed known locations to adaptively offset the RSS variations. Accurate results can be attained if the reference anchors are densely deployed. To reduce the use of numerous reference anchors, learning-based methods are introduced. LEMT [34] achieves adaptive temporal radio map by learning a functional relationship for one location and its neighbors based on a model tree method. Transfer learning techniques such as manifold alignment [22] and transferred Hidden Markov Model [38] are also applied to transfer RSS measurements over time. Although all relying on additionally deployed referenced points, these methods do reduce the cost and complexity for radio map maintenance and shed lights on more practical solutions. Two recent works, Chameleon [11] and LAAFU [12], both identify any altered APs and filter them out to maintain localization accuracy under altered AP signals, and accordingly update the fingerprint database with the real-time estimation. A conference version of this work can be found in [27]. We specify the typical working flow of radio map adaptation with reference points and provide discussions on the model generality and user intervention issues. We explore alternative solutions to gain precise reference locations in lack of mobility information. In addition to PLSR, we additionally implement a model tree approach and a linear regression method for comparison. We conducted more comprehensive experiments in detail and provide additional results.

Mobility Assisted Localization Recent advances in indoor localization, especially those assisted by smartphones, have enabled meter or sub-meter level accuracy [15, 18, 24]. Unloc [24] and Zee [18] both pinpoint precisely constructed user trajectories with meter-level accuracy by harnessing identifiable indoor landmarks and floor plan imposed constraints, respectively. Liu et al. [15] incorporates acoustic ranging in WiFi fingerprinting to limit the large tail errors. Montage [37] combines acoustic ranging with inertial sensing to provide meter-level tracking of multi-users. A recent work [16] even enables centimeter-level location resolution via opportunistic sensing. Most of these highly accurate systems benefit from smartphone enabled inertial sensing [14, 32], which depicts a trajectory with relative displacement based on step counting and heading estimation with smartphone sensors [4, 40]. These technologies underpin a primary primitive for AcMu, while AcMu in return can fortify them to maintain high accuracy in the long term.

# 5.3 Preliminaries and Measurements

In this section, we first conduct primary measurements to understand the RSS dynamics and then present preliminary background of radio map updating problem.

# 5.3.1 Measurements of RSS Dynamics

While RSS is well known to be susceptible to environmental changes, we conduct a quantitative measurement on the extent of variations and find several interesting observations. (1) As shown in Fig. 5.1a, samples within a short period of time are incapable of depicting the true characteristics of the RSS distribution at a specific location. Hence instant RSS measurements, e.g., those during a moving trace, are insufficient to serve as fingerprints for a location, and that is why a bulk of samples need to be collected at each location during the site survey. (2) As shown in Fig. 5.1b–d, RSS changes are small within a short term of several days, yet disperse to a considerable scale over a longer term. Thus a static radio map poses serious deviations over long-term deployment.

![](images/250a61c34178d1fed7c746465467f0bde45122ba41705d2450a3c8ae97a57528.jpg)



(a)RSS distribution with different amount of measurements.

![](images/c80613a344d870d59452de8cbf069d26eff3f4e4a1c01650c1a7859002d1edcd.jpg)



(b)RSS changes of different APs at a specific location

![](images/bf89b98b0a298ba643a31a760b8e6f87c7d6aa7676b96e0e36d0d27b4b389506.jpg)



(c)RSS changes of one specific AP over differentlocations

![](images/b537d0d1c1cf7555615208435ee8af724acc546e29ef0af23d243c16c94246af.jpg)



(d)RSS changes of different APs over differentlocations   
Fig. 5.1 RSS variations over different time period. (a) Average RSS value with 5 consecutive samples may differ at up to 10 dB from that with 50 samples. (b) (c) (d) RSS changes (compared to the initial measurements) over a long period are remarkably larger than those within a short term of several days

The RSS variations can be caused by either transient interference, such as moving objects, door opening and closing, or prolonged dynamics like light, temperature, and humidity changes and weather changes in the environment. Such dynamics are similar for neighboring locations. Therefore, certain underlying relationship of nearby RSS measurements may exist and remain relatively stable over time, even though the RSSs for every individual location greatly change. This basic intuition underpins the automatic radio map updating with real-time data from a set of reference points [22, 34].

# 5.3.2 Radio Map Updating with Reference Points

Generally, a radio map RM contains tuples of fingerprint-location relationships over all sample points in the region of interests. The physical area of interest is sampled as a finite location space $L ~ = ~ \{ l _ { 1 } , l _ { 2 } , \cdot \cdot \cdot ~ , l _ { n } \}$ where n is the total number of sample locations and each location is attached with coordinates $\begin{array} { r l } { l _ { i } } & { { } = } \end{array}$ $( x _ { i } , y _ { i } ) , 1 ~ \leq ~ i ~ \leq ~ n$ . Correspondingly, the radio fingerprints are modelled as a signal space $F = \{ f _ { 1 } , f _ { 2 } , \cdot \cdot \cdot , f _ { n } \}$ where each $\pmb { f } _ { i } = \{ f _ { i 1 } , f _ { i 2 } , \cdot \cdot \cdot , f _ { i p } \}$ is the fingerprint record corresponding to location $\boldsymbol { l } _ { i } , ~ f _ { i j }$ denote the RSS value of the j th AP, $1 \ \leq \ j \ \leq \ p$ , and $p$ is the total number of APs in the targeted location space. Note that for probabilistic localization methods, RSS distributions, instead of RSS values themselves, are stored as fingerprints. Once constructed in offline stage, either manually or automatically, the radio map is serving for follow-up location queries without adaptation. The contradiction between the static radio map and the dynamic indoor environments, however, seriously challenges the effectiveness of location estimation.

Accounting for environmental dynamics, several radio map updating techniques are introduced. The task of radio map updating is to adapt the radio map $R M _ { i - 1 }$ at time point $t _ { i - 1 }$ to a newer one $R M _ { i }$ at time $t _ { i }$ to accommodate to uncertain environmental changes. Previous works like LANDMARC [17] and LEASE [13] deploy dense reference anchors, i.e., receivers at known and fixed locations, to gather real-time samples to offset the RSS variations. To reduce the required number of anchors, a category of learning-based techniques is introduced [22, 34, 38], which learns a functional relationship between the samples at reference points and other locations with radio map at certain time, and fit the learned relationship to newly collected data from the reference points to predict fresh RSSs at other time instants.

To conclude, a typical radio map updating technique that utilizes new data collected from a set of reference points involves three steps:

1. Data collection: Collect new data from the reference points deployed at known locations;   
2. Model learning: Learn a temporal/spatial relationship between the fingerprints at these reference points and other non-reference locations;   
3. Map updating: Update the radio map based on the learned model with newly collected data as inputs.

In AcMu, we also aim to combat RSS variations and maintain an up-to-date radio map, but remove the requirements of additional reference anchors as well as extra user intervention.

# 5.4 Overview

This section briefly overviews our design. We aim to extend a radio map built at one time point to be adaptable to environmental dynamics and thus usable for other time instants. In AcMu, we accomplish this task by leveraging mobile devices to collect an adequate amount of fresh RSS samples. The key insight is that static mobile devices can be treated as movable reference points that contribute real-time RSS samples for adapting the radio maps. Although previous work has demonstrated the feasibility of learning temporal changes with the help of fixed reference transmitters, to translate such an intuitive idea to a practical system entails distinct challenges.

![](images/6ae41f0d67d7414618c47f082f592005cd9f4cb7861abcec8d3bd84ee7928bde.jpg)



Fig. 5.2 The system architecture of AcMu

1. Different from intentionally deployed anchors that have fixed accurate location information, it is challenging to obtain perfect locations of mobile devices even when they are static at specific points.   
2. Different from fixed reference anchors, the amount and locations of movable reference points based on mobile devices change for every time updating, which increases the difficulty in modelling the relationship between reference points and other locations in the radio maps.   
3. The fundamental relationships between fingerprints of reference points and other locations are non-trivial to acquire due to intangible signal propagation in complex indoor environments.

To address these challenges, AcMu involves three main components, i.e., pin data collection, reference point estimation, and radio map updating, as depicted in Fig. 5.2. Data from mobile users are automatically recorded during their routine work and life in indoor space. Specifically, radio signals are measured when a mobile device stays stationary for a certain duration. When the user is moving, wireless data together with motion data are collected to monitor the walking trajectory. The collected data, referred to pin data, are then uploaded, either in realtime or delayed until appropriate WLANs are available, to the back-end server for further processing. Any users present in the area of interests can participate in the data collection. Also, one user can contribute many groups of data within one day, depending on the mobility behavior and the device status (including battery, usage, motion, etc.).

Data received at the back-end server are then fed to the reference point estimation module to extract reference points for map updating. To locate the static mobile devices as accurate as possible, the accompanied moving trajectories in the pin data are utilized for trajectory matching. Once a sufficient number of reference points are obtained, the radio map is updated with the newly acquired data, based on an underlying relationship between RSSs of the reference points and other locations learned from the initial radio map. The updated radio map, which has been adapted to the environmental changes, is then used for online localization for further location queries.

Note that during the data collection procedure, users are in no need of explicit participation to measure and upload data. All data are automatically and silently collected through a back-end service running on the mobile devices. AcMu does not affect normal localization service since map updating can be executed during out-of-service time, e.g., during the night. Different from previous crowdsourcingbased radio map construction schemes that mostly require accumulation of abundant data as inputs [19, 31], the update operation in AcMu can be carried out gradually in a one-by-one manner with even only a single trajectory. In addition, we do not modify the working flow of classical fingerprint-based localization schemes and thus most of existing indoor localization systems, especially those based on smartphones [15, 18, 19, 31, 36], are compatible to be applied in the location estimation module. Indeed, we do not intend to propose advanced localization algorithm in this chapter. We instead mainly target at adapting the radio map. As in Sect. 5.6, we also validate the performance of our adaptation scheme based upon previous localization algorithms [2, 36].

# 5.5 Method Design

In this section, we first illustrate how to collect mobile data that are feasible for updating the radio map. Then we present how to extract reference point from these data and further how to update the radio map.

# 5.5.1 Pin Data Collection

# 5.5.1.1 Pin Data Specification

While a large body of recent works demonstrate that localization can benefit from user mobility [18, 19, 31], we further investigate and leverage the static behavior of mobile devices. Specifically, data collected when mobile devices are detected to be stationary can serve as referenced data for adapting radio maps. In contrast, data recorded when the user is moving are speculated to be beneficial for accurate localization. Accordingly, we attempt to collect data that contain two parts: a relatively large amount of RSS samples measured at static state and a series of RSS vectors along with mobility data during moving. We refer such data to as pin data since they consist of a bucket of “spot data” and a short tail of “trajectory data”. The reasons why we must collect pin data are that only an abundant amount of RSS samples are capable to describe the wireless channel characteristics while trajectory data with mobility constraints are promising in obtaining sufficient location accuracy for the static points. Neither static nor mobile data alone are capable of finishing the radio map updating task.

# 5.5.1.2 Mobility Monitoring

To collect pin data, a basic task is to monitor the motion states of mobile users. To this end, we conduct a local variance threshold method [31] on the acceleration data reported by the built-in accelerometer sensor to detect whether a mobile device is in motion. While the device is detected to be static, RSS samples over a certain period would be recorded. Then once the user is detected to move, radio signals together with inertial sensor data will be measured for a specific duration.

Mobility information, which provides distance and direction constraints between successive RSS samples, is then derived from the inertial sensor readings using dead-reckoning, which is an extensively studied and well utilized technique in indoor localization [14, 32]. To construct a moving trajectory, three typical steps are employed in smartphone-based dead reckoning, i.e., step counting, orientation reckoning, and stride estimation. Besides the accurately monitored trace structure, another nice feature of dead-reckoning, based upon extensively studied techniques [14, 24], lies in that a user do not need to intentionally hold the phone for inertial sensing. Instead he can hold the phone in hand or put it in a pocket or a bag. We present a brief working flow and omit the details, which can be easily referred in the literature [14, 18, 24, 28].

(i) Step counting Various approaches have been proposed to infer footstep counting from acceleration data [18, 24]. The rationality behind step counting is that the accelerations exhibit periodically repetitive patterns, which arise from the nature rhythmic of human walking. In AcMu, we adopt a finite state machine based algorithm proposed in [28], which can provide step counting as accurate as up to 98%. Figure 5.3 portrays a basic example of the step counting results, where the start and end points of each step are both detected.

![](images/e5e6cda6f84d1797049d8cb666e30c6112c4edad88826f59d75d06a0f7976729.jpg)



Fig. 5.3 An illustration of step counting

Fig. 5.4 An illustration of dead-reckoned trajectory   
![](images/7bd9a39e8ce369220414442f967c345e6bf7ce6eafa24e61eaf808c1237d5c04.jpg)



(ii) Orientation reckoning Regularly, orientation reckoning relies on magnetometer and gyroscope sensors, which provide absolute direction with respect to the earth coordinate system and the relative direction changes with respect to the phone platform, respectively. In AcMu, we employ gyroscope to monitor relative direction, which has been demonstrated to be remarkably accurate as indicated in [24, 28]. Furthermore, we incorporate compass to supply absolute direction of the trajectory in order to reduce the searching space during the trajectory matching module (discussed in the next section). Compass readings, however, can be considerably noisy in indoor environments due to electromagnetic interference. Particularly, single measurement errors could be as large as $2 5 ^ { \circ } { \sim } 5 0 ^ { \circ }$ . In AcMu, we employ a recent innovation of orientation estimation which further incorporates acceleration data and reports error within $2 0 ^ { \circ }$ for each step [37]. To further reduce the error, we derive a central direction of the entire trace (Fig. 5.4), which is the average of direction estimations during each step. Although the central direction is still not perfectly precise, it is sufficient for our trajectory matching algorithm in the subsequent section.

(iii) Stride estimation The footstep counts are typically converted into physical distances by multiplying a certain value of users’ stride lengths. AcMu incorporates the approach proposed in [37], which outputs accurate stride estimation for a variety of users with maximum error of 8.9 cm and mean error of only 4.3 cm. The adverseness of yet existed slight errors will be further mitigated during the trajectory matching algorithm for location estimation by searching for a range of values within the error bound.

For every group of pin data, we divide them into two parts. A sequence of continuously measured RSS samples at a specific spot are averaged to be a representative fingerprint vector, denoted as $\pmb { r } _ { k } ~ = ~ \{ r _ { k 1 } , r _ { k 2 } , \cdot \cdot \cdot ~ , r _ { k p } \}$ where $r _ { k j }$ indicates the mean RSS value of the jth AP at reference spot k (with unknown location $\boldsymbol { l } _ { \boldsymbol { r } _ { k } } )$ and $p$ is the total AP number in the area of interests. These spot data, once the corresponding location is estimated, are used as real-time reference data for map updating. The followed trajectory data are employed to achieve accurate location estimation of the spot. Assuming that totally w samples are included in the trajectory, it can be represented by $J = \{ s _ { 1 } , s _ { 2 } , \cdot \cdot \cdot , s _ { w } \}$ , where $s _ { i } , i =$ $1 , 2 , \cdots , w$ , indicates the ith fingerprint measurement within the trajectory and obviously $s _ { 1 } = r _ { k }$ (assuming that we use data in the form of spot data followed with moving tail; otherwise $\boldsymbol { s } _ { w } = \boldsymbol { r } _ { k } )$ . As above mentioned, the walking distance and orientation between any two consecutive samples have been derived, denoted as $\pmb { d } = \{ d _ { 1 } , d _ { 2 } , \dotsb { } , d _ { w - 1 } \}$ and $\pmb { \phi } = \{ \alpha _ { 1 } , \alpha _ { 2 } , \dotsb { \cdot } \bot , \alpha _ { w - 1 } \}$ respectively, where $d _ { i }$ denotes the distance between the i 1th sample and the ith sample and $\alpha _ { i }$ is the corresponding direction. As illustrated in Fig. 5.4, given these constraints, a rigid trajectory is derived with a central direction of $\begin{array} { r } { \bar { \phi } = \frac { 1 } { w - 1 } \sum _ { i = 1 } ^ { w - 1 } \alpha _ { i } } \end{array}$ .

−One comment we want to make is that there might be no strictly one-to-one correlation between the fingerprint samples and the footsteps detected. To deal with this, we simply align each fingerprint to the closest step, which is clearly identified with a certain timestamp as in Fig. 5.3.

# 5.5.2 Reference Point Estimation

In this subsection, we propose a trajectory matching scheme to precisely estimate the spot locations. The idea is to utilize geometrical constraints reflected by the trajectories to reduce location uncertainties. Although extensive research works have exploited user mobility to enable accurate localization with meter- or submeter-level accuracy [10, 16, 33], we harness a trajectory in a distinctive global optimization manner as follows.

Given trajectories collected at time $t _ { k }$ , our goal is to match them against the latest radio map $R M _ { k - 1 }$ (since $R M _ { k }$ is not available yet) to locate the corresponding referenced spots as accurate as possible. The task of trajectory matching is to find a sequence of location candidates in the location space such that the distances between these candidates are subjected to the distance constraints implied by the trajectory, while the total fingerprint difference is minimized.

A dead-reckoned trajectory with displacement and direction constraints can be treated as a rigid structure, which holds the relative geometry information. Hence, the trajectory matching task can be treated as to superimpose a rigid structure in the location space, which can be done by a sequence of constrained translation and rotation operations as specified by the following steps:

(i) Detecting feasible region from initial WiFi estimation Instead of searching over the whole location space L, we narrow the search space by leveraging the initial pure WiFi-based location estimations. Generally, fingerprints within a trajectory will fall into a limited area, although each location might not be precisely located. We thus sketch a feasible region as a convex closure in the location space that covering all those initial location estimations and only search for optimal candidates within this region.

(ii) Locking feasible orientation from trajectory direction Since we have obtained the estimated central direction $\bar { \phi }$ of the trajectory, it is not necessary to search for all orientations throughout $3 6 0 ^ { \circ }$ . Alternatively, we only search a certain section around the central direction. As shown in Fig. 5.5, we consider the interval of $[ \bar { \phi } - \varDelta \phi , \bar { \phi } + \varDelta \phi ]$ , where $\varDelta \phi$ is supposed to be the maximum direction error. We set $\varDelta \phi$ at $1 0 ^ { \circ }$ since $\bar { \phi }$ is an averaged value of orientation estimations for each step, which are within $2 0 ^ { \circ }$ with high confidence [37].

Fig. 5.5 An illustration of trajectory matching   
![](images/0631ff782c1c1f64326ff99935432c93914a62cb8c96daa79a9af9086200db14.jpg)



(iii) Joint location estimation Finally, we search for optimal locations to superimpose the trajectory against the radio map, with a minor translational step of $\varDelta t$ meters and rotational step of $\varDelta r$ degrees (set to be 0.5 m and $2 ^ { \circ }$ based on the empirical study and environmental settings). The matching algorithm minimizes the sum of square difference over all fingerprint samples within the trajectory $J = \{ s _ { 1 } , s _ { 2 } , \ldots , s _ { w } \}$ with geometrical constraints.

$$
\min _ {\boldsymbol {f} _ {c (j)} \in F} \sum_ {j = 1} ^ {w} | | \boldsymbol {f} _ {c (j)} - \boldsymbol {s} _ {j} | |, \text { s.t. } \tag {5.1}
$$

$$
| | d _ {j} - d _ {j} ^ {\prime} | | \leq \Delta d, j = 1, 2, \dots , w - 1
$$

where $d _ { j } ^ { \prime } = | | l _ { c ( j + 1 ) } - l _ { c ( j ) } | |$ denotes the distance between two candidate locations and $c _ { j }$ is the candidate location for $\boldsymbol { s } _ { j }$ . Δd is a minimum distance constraints that can be set to be, e.g., half of the sampling space interval during the initial site survey. Note that since we do not have perfect stride length, we will try different versions of $d _ { j }$ here (corresponding to different values of possible stride lengths with a smaller increment of $\varDelta s$ cm). For instance, assuming the estimated stride length is 70 cm, we consider a range of value from 60 to 80 cm with a step length of 4 cm or so, which generates five versions of $d _ { j }$ , i.e., five different trajectories for matching. For the final results, we choose the one that produces the minimal fingerprint difference as in Eq. 5.1.

We note that in practice some other localization algorithms could be incorporated to obtain accurate reference locations, e.g., via dynamic warping [33] or contourbased trilateration [10] even in case that the mobility information is occasionally unavailable. Specifically, sequential fingerprints (but not necessarily trajectories with mobility hints) provide promising constraints for precise location estimation [21, 29, 33]. Furthermore, other types of readily accessible fingerprints like magnetism [20] as well as image-based approaches [30] can also be leveraged to enhance location estimation. After the candidate locations are selected, the first location, $l _ { c ( 1 ) }$ , is estimated to be the location of the referenced spot. Fusing all pin data at time point $t _ { k }$ , we obtain a group of reference spots $R _ { k } = \{ l _ { r _ { 1 } } , l _ { r _ { 2 } } , \cdot \cdot \cdot , l _ { r _ { m } } \}$ , each with estimated location $l _ { r _ { i } } = ( x _ { i } , y _ { i } ) , i = 1 , 2 , \cdot \cdot \cdot , m$ . Note that both $R _ { k }$ and m change for every time updating. The following section details how these spot data, given their locations available, are used to accommodate to environmental dynamics.

# 5.5.3 Map Updating

To update a previous radio map with newly collected data from a set of reference points, a critical issue is to identify and model a functional relationship between the RSSs observed at reference points and other locations.

Assuming that a set of reference spots $R _ { k }$ is obtained at time $t _ { k }$ and the j th spot is located at $\boldsymbol { l } _ { \boldsymbol { r } _ { j } }$ , we need to learn a predictive relationship $\mathcal { H }$ between the RSS values of these locations and those of each other location. Consider the j th AP, $1 \le j \le p$ at location $l _ { i } , 1 \le i \le n$ , we aim to learn a functional relationship $\mathcal { H } _ { i j }$ as

$$
f _ {i j} (t _ {0}) = \mathscr {H} _ {i j} \left(f _ {r _ {1} j} (t _ {0}), f _ {r _ {2} j} (t _ {0}), \dots , f _ {r _ {m} j} (t _ {0})\right), \tag {5.2}
$$

which reflects the mapping from RSS values received at the m reference locations to the RSS at location $\mathbf { \xi } _ { l _ { i } }$ . Here $f _ { i j } ( t _ { 0 } )$ and $f _ { r _ { k } j } ( t _ { 0 } )$ denotes the RSS value of the j th AP at location $\mathbf { \xi } _ { l _ { i } }$ and $\boldsymbol { l } _ { \boldsymbol { r } _ { k } }$ respectively, both of the original radio map RM0. Built at time point t0, i.e., the offline stage, the above relationship is expected to be capable of capturing the relationship between RSS values at $\mathbf { \xi } _ { l _ { i } }$ and those measured at $l _ { r _ { k } } ( 1 \le k \le m )$ in the future, regardless of the time point t. Consequently, given the reference data from a set of reference spots at time point t available, we are able to predict the RSS values at other locations using the learned function $\mathcal { H }$ .

# 5.5.3.1 Learning the Regression Model

Ideally, there should exist a linear relationship between the RSS at one location and those received at the reference points, according to theoretical signal propagation models, e.g., the log-distance path loss (LDPL) model. Signal propagation in practice, however, suffer from unpredictable reflections, diffractions, scattering, shadowing, etc., which are generally known as multipath effects, resulting in significant multicollinearity among RSS measurements from different locations. Concretely, as shown in Fig. 5.6b, serious multicollinearity, measured in term of condition number [3], are observed between RSS vectors at different locations based on real-world measurements. In this case, classical multivariate linear regression will result in unstable estimation coefficients and thus produce high variances in prediction. A model tree based approach is employed in [34] to deal with this problem in case of using fixed reference points. In AcMu, we investigate partial least square regression (PLSR) as a superior choice, which yields stable, correct and highly predictive models [8] in such case. Later we will also implement alternative approaches in AcMu for comparison in Sect. 5.6.

![](images/25a007d0a705cce4e5b3f426567b2b679c44613096dd5a278291aecea4f12219.jpg)



![](images/adc836eed709e053ae4cafd5c27ae4347f256a69105fa72e169175443a47fdd5.jpg)



Fig. 5.6 Condition numbers of 140 testing cases and their distribution indicates significant multicollinearity (measured by condition number) among RSS samples from different locations. Generally, a condition number of larger than 10 indicates probable multicollinearity while greater than 30 implies serious multicollinearity [3]

PLS regression generalizes and combines features from principal component analysis (PCA) and multivariate linear regression. It is particularly useful when the number of predictors is comparable to or greater than the number of responses, and when there is multicollinearity among observation variables, which is exactly the case of AcMu. PLS regression finds components from the observation variables X that are also relevant to the responses Y . Specifically, PLS regression works by searching a set of latent vectors that performs a simultaneous decomposition of X and Y with the goal to maximize the covariance between X and Y . This step generalizes PCA and is followed by a regression step where the decomposition of X is used to predict Y . Generally, PLS regression can have the form of multivariate regression of $Y = X B + E$ with $\pmb { { \cal B } } = \bar { X ^ { T } } \pmb { U } ( \pmb { T } ^ { T } X X ^ { T } \pmb { U } ) ^ { - 1 } \pmb { T } ^ { T } \pmb { Y }$ , where T and U are matrices of the extracted latent vectors and E is the residual matrix [8].

In AcMu, $X = [ f _ { r _ { 1 } j } , f _ { r _ { 2 } j } , \cdot \cdot \cdot , f _ { r _ { m } j } ] _ { n \times m }$ is the matrix of RSS observations from m reference points, $\pmb { Y } \doteq [ \pmb { f } _ { i j } ] _ { n \times 1 }$ is RSS measurements from location $\mathbf { \xi } _ { l _ { i } }$ Since Y is a one-dimensional vector (and we denote by y), however, the problem can then be solved by the PLS1 algorithm [5], which is designated for the single response variable case of PLS regression. PLS1 algorithm repeats the following steps to find the first g latent variables. Mathematically, for the j th latent vector, search for $\mathbf { \Psi } _ { t _ { j } } ~ = ~ \mathbf { \Psi } _ { X _ { j } } \mathbf { w } _ { j }$ to maximize the covariance $c o v ( { X } _ { j } { \pmb w } _ { j } , { \pmb y } _ { j } )$ subject to $\boldsymbol { w _ { j } ^ { T } w _ { j } } = 1$ .

$$
\boldsymbol {w} _ {j} = \boldsymbol {X} _ {j} ^ {T} \boldsymbol {y} _ {j} / | | \boldsymbol {X} _ {j} ^ {T} \boldsymbol {y} _ {j} | | \tag {5.3}
$$

$$
\boldsymbol {t} _ {j} = \boldsymbol {X} _ {j} \boldsymbol {w} _ {j} \tag {5.4}
$$

$$
\boldsymbol {p} _ {j} = \boldsymbol {X} _ {j} ^ {T} \boldsymbol {t} _ {j} / \boldsymbol {t} _ {j} ^ {T} \boldsymbol {t} _ {j} \tag {5.5}
$$

$$
\widehat {c} _ {j} = \boldsymbol {t} _ {j} ^ {T} \boldsymbol {y} _ {j} / \boldsymbol {t} _ {j} ^ {T} \boldsymbol {t} _ {j} \tag {5.6}
$$

For the first latent vector, let $X _ { 1 } = X$ and $y _ { 1 } = y$ . To search for the next latent vector $t _ { j + 1 } , X _ { j }$ and $y _ { j }$ are deflated by their regression approximations on $t _ { j }$ , i.e., $X _ { j + 1 } = X _ { j } - t _ { j } p _ { i } ^ { T } , y _ { j + 1 } = y _ { j } - t _ { j } { \widehat c } _ { j }$ , and then repeat the above steps using the deflations.

Hence after g runs, we have two $m \times g$ matrices W and P and an $n \times g$ matrix T with columns ${ \pmb w } _ { j } , { \pmb p } _ { j }$ and $t _ { j }$ respectively, and form a column vector $\widehat { \mathbf { c } }$ with g elements $\widehat { c } _ { j }$ . The number of scores g should, in principle, be chosen such that the  residual matrices of X and y after g runs, i.e., ${ \bf { \bar { X } } } _ { g + 1 } = X - T P ^ { T }$ and $y _ { g + 1 } =$ $\mathbf { \nabla } y - T \widehat { \boldsymbol { c } } ,$ , are approximately uncorrelated with each other. And then we obtain the PLS regression in form of

$$
\widehat {\boldsymbol {y}} = \boldsymbol {T} \widehat {\boldsymbol {c}} = \boldsymbol {X} \boldsymbol {B} = \boldsymbol {X} \boldsymbol {W} (\boldsymbol {P} ^ {T} \boldsymbol {W}) ^ {- 1} \widehat {\boldsymbol {c}} \tag {5.7}
$$

where $\widehat { \mathbf { y } }$ is the predicted values and $\begin{array} { l l l } { { { \pmb B } } } & { { = } } & { { { \pmb W } ( { \pmb P } ^ { T } { \pmb W } ) ^ { - 1 } { \widehat { \pmb c } } } } \end{array}$ is the regression coefficients.

# 5.5.3.2 Updating the Radio Map

Once the regression function has been derived, the remaining task is to update the radio map with the newest measurements from a set of identified referenced spots.

Let $R _ { t }$ be the set of m reference spots at time t. For a non-reference location $\mathbf { \xi } _ { l _ { i } }$ , of which the newest fingerprints are unavailable, we now have learned the relationship $\mathcal { H } _ { i j }$ from the initial radio map $R M _ { 0 }$ based on PLS regression. Then the fingerprint of location $\mathbf { \xi } _ { l _ { i } }$ is updated by

$$
\widehat {f} _ {i j} (t) = \mathscr {H} _ {i j} \left(f _ {r _ {1} j} (t), f _ {r _ {2} j} (t), \dots , f _ {r _ {m _ {t}} j} (t)\right) \tag {5.8}
$$

where $f _ { r _ { k } j } ( t )$ denotes the newest RSS observations of the j th AP at location $l _ { r _ { k } }$ and ${ \widehat { f } } _ { i j } ( t )$ is the predicted fresh RSS of the j th AP at location $l _ { j }$ at time t .

Once a set of sufficient number of referenced spots are available, the update procedure is executed for one time to adapt the current radio map according to the newer measurements. Note that because both the amount of reference points and their corresponding locations vary over each time updating, the regression function needs to be recalculated for each update, as indicated in Algorithm 5.1. By frequently and timely updating, the radio map is almost always up-to-date and thus adaptively adapts to environmental changes. Although the updating task, including trajectory matching and map updating, might be computation-intensive, it does not affect normal localization service since the updating operations can be executed only in off-peak or off-service periods.

Algorithm 5.1: Radio map updating   
Input:
The initial radio map $RM_{0}$ , the newest fingerprint measurements at a set of locations $R_{t}$ Output:
The complete updated radio map $RM_{t}$ 1: for each location $l_{i} \notin R_{t}$ do
2: for each AP j do
3: Calculate function $H_{ij}^{R_{t}}$ as in Eq. 5.2 from $RM_{0}$ 4: Update $f_{ij}(t_{0})$ to $\widehat{f}_{ij}(t)$ according to Eq. 5.8
5: end for
6: end for

# 5.6 Implementations and Evaluation

# 5.6.1 Experimental Methodology

We prototype AcMu on Google Nexus 7 pad and Google Nexus S phone, which both run the popular Android OS and support various types of inertial sensors. We conduct the experiments on one floor of a typical office building covering more than $1 5 0 0 \mathrm { m } ^ { 2 }$ , as illustrated in Fig. 5.7. Specifically, the experimental areas contain a corridor and 14 rooms, including laboratories, offices, and classrooms. The experimental area is crowded with various APs that are readily installed in the environments, some by the university and some by the laboratories. Approximately, there are up to 40 APs in total, among which we chose 16 that keep active throughout the entire experimental period. Several APs with known locations are marked in Fig. 5.7 while others are installed at unknown locations.

We deploy the localization service of AcMu for over 6 months and conduct experiments for 20 days across the 6 months, which include two phases: the initial phase and a phase conducted 6 months later. During the initial phase, we survey the experimental areas with a sampling density of about $2 \times 2 \mathrm { m }$ , producing around 150 sample locations. For each sample location, we collect 60 fingerprints for around 1 min, except for the initial radio map, for which we collect 90 fingerprints at each sample location. Afterwards, we repeat the survey procedure every 2 or 3 days for 2 weeks. The latter phase executes the similar task, yet is 6 month later, when the environment is expected to be changed at a relatively large scale, and lasts for 1 week. During remaining time of the 6 months, AcMu is continuously running, yet we do not collect experimental data for evaluation.

Three volunteer users participate in the data collection procedure. Each user carries a smartphone with him during his daily life. The smartphones are preinstalled with a prototyped App for data collection and are used as their primary phones during the experimental periods. The users, however, do not need to behave intentionally for data collection. They simply work and live routinely as they commonly do. We believe the data gathered in such way are representative for general realistic scenarios.

![](images/a16365c6c928def533378eae41c42350ee3345866d1e9fb6d3eed5e166bc959c.jpg)



Fig. 5.7 Experimental areas

Besides the radio map data, another two categories of data are also collected during each survey:

1. Pin data. We collect pin data by placing a mobile device still for a certain period (ranging from 10 s to 1 min) and then taking it for a short walk, during which the sensor data of accelerometer, gyroscope, and compass are also recorded. We collect 30–80 such traces during each survey, covering different rooms. When collecting pin data, a user needs to take a phone during movements, but does not need to dedicatedly hold the phone at a fixed relative pose (e.g., in front and always facing ground).   
2. Query data. Query data are collected from randomly selected locations during each survey, within a short period of 1 or 2 s, for location query. Moving trajectories are also taken into consideration for query, yet not necessary in the form of pin data (the spot parts are not required).

Pin data are used to evaluate the trajectory matching algorithm as well as extract reference points for map updating. Query data are used to test localization accuracy.

# 5.6.2 Performance Evaluation

# 5.6.2.1 Performance of Trajectory Matching

We first evaluate the localization performance of the proposed trajectory matching algorithm. Most of trajectories involved in the experiments are relatively short with 3–8 RSS samples. As shown in Fig. 5.8, trajectory matching yields average accuracy of about 1.0 m and 95th percentile accuracy of 2.2 m when using a real-time radio map. An average accuracy of 1.4 m and 95th percentile accuracy of 2.6 m are still maintained with a recent radio map (e.g., within 3 days). In contrast, location accuracy degrades heavily to more than 3 m in average error and 5.6 m in 95th percentile error when using a long-outdated radio map (6 months). Given that the sampling density is 2 × 2 m, the delightful accuracy of trajectory matching using a recent radio map demonstrates our basic insight that mobile devices can be used as reference points and lays a firm foundation for the map updating technique.

Fig. 5.8 Performance of trajectory matching   
![](images/9828f51a109f13313c07194a4a396cb99eee4c6b4480ed4a324fca90dac6b399.jpg)



![](images/8264e2b8f6ef5bc2b60f3566bd1bd1b042920e35be78feead27b5786669be808.jpg)



(a)

![](images/e3f058265fd92622d4795ede6828a71ef631dbdad19616ec824b1e975cd78918.jpg)



![](images/cdb78951c71b141b402e919e9701ec4925d10f0d4c649362fe71af521ad30b80.jpg)



(c)   
Fig. 5.9 RSS prediction accuracy with (a) periods of different time lengths, (b) different numbers of reference points, and (c) differently distributed reference points

# 5.6.2.2 Performance of Map Updating

Precision of map updating is the most critical performance metric of AcMu. We use RSS prediction error, i.e., the RSS difference between the predicted values and the ground-truth measurements, to evaluate the performance. Since we do not collect data continuously over the 6 months, we extract reference points to update the radio maps 6 months later using the recently surveyed radio map yet still conduct prediction based on the initial one constructed 6 months ago. And note that we only account for RSS prediction errors of non-reference points, since the “predicted” RSS at a reference point is exactly the real-time measured value and thus the corresponding error equals zero.

As shown in Fig. 5.9a, AcMu produces accurate prediction of real-time RSS samples, regardless of the running time. While the true RSS values deviate more greatly over long periods, AcMu consistently yields accordant prediction, with average RSS residuals of less than 4 dB after 3 and 6 days and around 4 dB on the 9th day while 5.5 dB for 6 months later.

We further examine how many reference points are sufficient to produce accurate prediction. Figure 5.9b illustrates the prediction results with different number of reference points used. As seen, when using 30–60 points over the whole radio map of around 150 sample locations (around 20–40%), the radio map can be gracefully adapted to accommodate environmental dynamics, with average prediction error in RSS values of 6.9, 6.8, 6.2 and 5.4 dB, respectively. The required amount is not too high for practical applications since there are frequent opportunities from numerous mobile devices to collect reference data and thus such movable reference points can accumulate considerably fast (according to one of our primary tracking of campus mobile users, the percentage of time period when the devices are placed still can be up to 80% through the whole day).

Finally, we inspect the performance with reference points that are differently distributed over the location space. We randomly choose four groups of an identical number of reference points and two groups of them are uniformly distributed while another two are clustered. As shown in Fig. 5.9c, better performance will be gained when the locations are evenly distributed over the monitoring area, with around 4 dB enhancement in average prediction error compared to using uneven reference points. Thus in practice, the updating server can be triggered less frequently, only in cases of sufficient number of evenly distributed reference points.

Performance comparison Alternative to PLSR, different effective prediction models could also be applied in AcMu framework as long as they are capable of captureing the intrinsic RSS neighbourhood relationship. To compare the performance of AcMu, we implement two related approaches: (1) a model tree (MT) based approach [34] and (2) a multivariate linear regression (MLR) method extended from [9]. As for the MT method, we apply the M5’ algorithm [23] to induce an effective model tree as done in [34]. We test the performance of each method for prediction after 3 days and 6 months, respectively. We use an identical set of evenly distributed reference points that occupy a moderate ratio of 30%. As seen in Fig. 5.10, AcMu achieves slightly better accuracy than MT method (with incremental gains of around 1 dB in mean and median prediction accuracy), which both considerably outperform the linear approach by about 5 dB. Specifically, MT yields slightly worse but still comparable accuracy with AcMu after 3 days, while MLR induces significant errors for any case. The mean and median prediction errors after 3 days when using AcMu, MT, and MLR are 4.8, 5.5, and 11.6 dB and 3.9, 4.1, and 8.7 dB, respectively. In the case of 6 months, the corresponding metrics are 6.5, 7.3, and 11.5 dB and 4.7, 6.2, and 10.1 dB. In addition to the superior performance of radio map adaptation, the key advantage of AcMu lies in that it enables adaptation without using fixed infrastructure, which is beyond the achievements of previous approaches. In contrast, the comparative approaches MT [34] and MLR [9] are both originally used for infrastructure-based adaptation.

![](images/7f67fef33ebaf12e03e95d426ff6e775d6e951dde761eaad4996de0955c9a857.jpg)



![](images/a75a90883781ad9d09e77069aab129979160ec8a8cb5f98b057fe3cd6dd51808.jpg)



Fig. 5.10 Performance comparison of different prediction models. (a) Prediction after 3 days. (b) Prediction after 6 months

# 5.6.2.3 Localization Performance

As we target at updating the radio map, we actually do not focus much on the accuracy improvement gained by localization algorithms. Nevertheless, for comprehensive understanding of the adaptation effects, we carry out experiments to validate the accuracy and effectiveness by appropriately adapting the original radio maps. We choose and implement the most well-known and typical fingerprintbased localization algorithms, including RADAR [2] and Horus [36], to evaluate the accuracy gains of the predicted radio map for real-time localization. We also compare the performance of the proposed trajectory matching algorithm by implementing it in the localization phase. We employ each localization algorithm against an initially constructed radio map (original), a real-time measured radio map (ground truth), and an updated radio map (predicted), respectively. As we mostly care about the relative accuracy improvement provided by AcMu compared to using a static radio map, we test all algorithms under identical settings and omit the impacts of factors such as the number of APs and the number of RSS samples, which might be critical to common localization algorithms. We argue that the absolute accuracy, based on the adapted radio map, can be further improved by employing more advanced localization algorithms [33] or extra information [15].

As shown in Fig. 5.11a, AcMu provides up to 30% improvements on average localization accuracy by using the updated radio map when deployed for 3 days. Figure 5.11b shows that more than 30% enhancements are still gained using the updated radio map of AcMu after a 6-month running. Similarly in Fig. 5.11c, d, the average location errors are reduced by 28.7% and 31.4% when running Horusbased KNN for 3 days and 6 months, respectively. Furthermore, as shown in Fig. 5.12a, benefiting from the stable performance of trajectory matching based method, similar location accuracy of about 1.4 m in average can be obtained when using either an updated radio map or a recent one (e.g., within 3 days). When the localization service has run for a long term, however, AcMu gains remarkable accuracy improvement of more than 2 , compared to using the static original one (1.4–3 m). In addition, comparing all the results in Fig. 5.12, we observe that the proposed trajectory matching algorithm significantly outperforms RADAR and Horus in any case.

![](images/b7c71cff146e0053c0f883d939703abbadf973d7e2b31c7ce02856f33a9a43f7.jpg)



(a)

![](images/ad4dad2f921efcc68ca3d7fae212015a673f934b0f9511814804add9869b2cd0.jpg)



![](images/c4892412bf2e06a3e4441ed8928b5a53d7f7b3fd536defd26352eede9f00450b.jpg)



(c)

![](images/b4d9d71b721d80c0ce92b82ade55bc21400b43d63e63aaf9f9810aeb3496e8fa.jpg)



Fig. 5.11 Localization accuracy of single location queries for different running periods using static, predicted, and real-time radio map, respectively. (a) RADAR-based KNN for 3 days. (b) RADAR-based KNN for 6 months. (c) Horus-based KNN for 3 days. (d) Horus-based KNN for 6 months   
![](images/68a522ea4b6d3fe52c73fe9f4b6479ed9fde3b77b97759d93670be2a88b5bc05.jpg)



![](images/9b44de01e3d9b43adde20f94cb7910bf38e9a88722d1cbf4c81b415aacfcdd30.jpg)



Fig. 5.12 Localization accuracy of trajectory matching for different running periods using static, predicted, and real-time radio map, respectively. (a) Trajectory matching for 3 days. (b) Trajectory matching for 6 months

Since the ground truth radio map represents exactly the fresh RSS samples, the predicted radio map is of no reason to be better. Nevertheless, comparable accuracy is still achieved. Particularly, the accuracy of using the predicted radio map is extraordinarily close to that of using the real-time measurements, with only a minor gap of 0.34 m in average after a 6 month period. In other words, a continuously updated radio map is capable of maintaining accurate and stable performance for long-term running systems. We envision AcMu as a fundamental and indispensable supplementary for existing localization techniques to cope with fingerprint variations caused by environmental dynamics, by extending a radio map built at one time instant to be adaptable and effective for other time instants.

# 5.7 Discussions and Limitations

Generality of Neighbourhood Relationship The assumption that certain relationships among RSS observations from neighboring locations keep relatively stable over time acts as a fundamental primitive for automatic radio map self-updating [13, 34]. We verify our proposed model via real-world experiments with the following logic: if a model (embodying the relationship) trained at one time slot predicts well for another time slot, we can conclude that the model also holds at the new time slot. In other words, the prediction accuracy serves as a good metric for not only the performance of the updating services but also the rationality of the model itself. Thus if we could find a model that is learned initially while predicts well for any time point, we confidently demonstrate a certain relationship among neighboring RSS observations, which can be described by the derived model.

While we have validated the assumption over a long period of 6 months and previous works also support and build systems upon this assumption [13, 34], we agree that the generality of the time-invariant relationship should be further validated across difference scenarios. The proposed approach has been demonstrated to work well in typical small and medium spaces, which are the majority of indoor scenarios, but still needs to extensively evaluated especially those large spacious areas. In the future, we intend to deploy localization systems in multiple buildings to further verify the practicability.

User Intervention AcMu employs ordinary mobile users to participate in the radio map updating tasks. As we mentioned above, however, these users do not need to intentionally behave in any favourable way for desired data collection. The reasons are two-fold: (1) Standing upon extensive previous research [14, 24, 32], nowadays we are able to monitor user mobility via smartphones efficiently and effectively, e.g., detecting whether a phone is moving or not, reckoning the trajectory of a moving user, or even monitoring the context-aware user activities, etc. Incorporating these proven techniques, we are able to obtain satisfactory trajectories in most scenarios. (2) In case of “bad” trajectories, AcMu can just abandon them. Since the updating task is expected to run every several days or weeks, thus it is probably still promising to collect enough reference points over a accumulative period even if we drop some of them. To identify “bad” trajectories, we can investigate the inconsistency between different dimensions of sensing data, e.g., WiFi observations, acceleration data and gyroscope data, etc., as done in [39, 40]. For instance, if the RSS measurements appear to be stable across a trajectory, it is probably a “bad” one that is mistakenly estimated from user motions at a same location. We leave such quality-aware trajectory monitoring as a valuable and promising future direction.

Practical Deployment In practice, when integrating AcMu into an existing localization system, several practical issues need to be carefully considered and addressed. We discuss some of the major ones in the following.

First, rather than using a fixed period, the radio map updating should better be executed based on specific conditions, for example, when significant biases are observed between the current radio map and the fresh RSS measurements (from the identified reference points) have been accumulated. The detailed values of fingerprint bias and reference point number could be determined by specific application scenarios and requirements.

Considering power management, although inertial sensing has been demonstrated to be energy-efficient, one can still alleviates the power concerns by intelligently selecting appropriate devices and timeslots for data recording. For instance, we notice that mobile devices are common to be charged even in daytime when they are powered up. Thus for these devices, we can gather more data over a longer time window. While it would be better to collect a minimal amount of measurements or even not recording data for low-battery devices. By doing this, we can lessen the negative influence on participants’ daily uses of mobile phones.

Device heterogeneity has also been a long-standing problem in fingerprint-based localization, especially crowdsourcing-based solutions. Different mobile devices might observe diverse RSS values under the same environment, which would also degrade the prediction performance of AcMu. Fortunately, recent innovations [21, 29, 35] that explore differential RSS among neighbouring or sequential locations would provide new insights in dealing with this problem.

Inspired by recent innovations [10, 33], in the future we tend to devise accurate localization algorithms for reference points without using mobility hints in purpose of further liberating any user intervention and mitigating the power concerns.

# 5.8 Conclusions

In this chapter, we present AcMu, an automatic and continuous radio map selfupdating service for wireless indoor localization that exploits the static power of mobile devices. We prototype AcMu and conduct experiments in typical buildings. Experimental results from 20 days across 6 months demonstrate that AcMu effectively accommodates the RSS deviations caused by environmental dynamics, underlying long-term indoor positioning services.

# References

1. Alzantot, M., Youssef, M.: Crowdinside: automatic construction of indoor floorplans. In: Proceedings of the 20th International Conference on Advances in Geographic Information Systems (2012)   
2. Bahl, P., Padmanabhan, V.N.: RADAR: an in-building RF-based user location and tracking system. In: Proceedings of IEEE INFOCOM (2000)   
3. Belsley, D.A., Kuh, E., Welsch, R.E.: Regression Diagnostics: Identifying Influential Data and Sources of Collinearity, vol. 571. Wiley, New York (2005)   
4. Brajdic, A., Harle, R.: Walk detection and step counting on unconstrained smartphones. In: Proceedings of ACM UbiComp (2013)   
5. Bro, R.: Multiway calidration. Multilinear PLS. J. Chemom. 10, 47–61 (1996)   
6. Chintalapudi, K., Padmanabha Iyer, A., Padmanabhan, V.N.: Indoor localization without the pain. In: Proceedings of ACM MobiCom (2010)   
7. Gao, R., Zhao, M., Ye, T., Ye, F., Wang, Y., Bian, K., Wang, T., Li, X.: Jigsaw: indoor floor plan reconstruction via mobile crowdsensing. In: Proceedings of ACM MobiCom (2014)   
8. Geladi, P., Kowalski, B.R.: Partial least-squares regression: a tutorial. Anal. Chim. Acta 185, 1–17 (1986)   
9. Haeberlen, A., Flannery, E., Ladd, A.M., Rudys, A., Wallach, D.S., Kavraki, L.E.: Practical robust localization over large-scale 802.11 wireless networks. In: Proceedings of ACM MobiCom (2004)   
10. He, S., Hu, T., Chan, S.H.G.: Contour-based trilateration for indoor fingerprinting localization. In: Proceedings of the ACM SenSys (2015)   
11. He, S., Ji, B., Chan, S.H.G.: Chameleon: survey-free updating of a fingerprint database for indoor localization. IEEE Pervasive Comput. 15(4), 66–75 (2016)   
12. He, S., Lin, W., Chan, S.H.G.: Indoor localization and automatic fingerprint update with altered AP signals. IEEE Trans. Mob. Comput. 16(7), 1897–1910 (2017)   
13. Krishnan, P., Krishnakumar, A., Ju, W.H., Mallows, C., Gamt, S.: A system for LEASE: location estimation assisted by stationary emitters for indoor RF wireless networks. In: Proceedings of IEEE INFOCOM (2004)   
14. Li, F., Zhao, C., Ding, G., Gong, J., Liu, C., Zhao, F.: A reliable and accurate indoor localization method using phone inertial sensors. In: Proceedings of ACM UbiComp (2012)   
15. Liu, H., Gan, Y., Yang, J., Sidhom, S., Wang, Y., Chen, Y., Ye, F.: Push the limit of WiFi based localization for smartphones. In: Proceedings of ACM MobiCom (2012)   
16. Liu, K., Wu, D., Li, X.: Enhancing smartphone indoor localization via opportunistic sensing. In: Proceedings of IEEE SECON (2016)   
17. Ni, L.M., Liu, Y., Lau, Y.C., Patil, A.P.: LANDMARC: indoor location sensing using active RFID. Wirel. Netw. 10(6), 701–710 (2004)   
18. Rai, A., Chintalapudi, K.K., Padmanabhan, V.N., Sen, R.: Zee: zero-effort crowdsourcing for indoor localization. In: Proceedings of ACM MobiCom (2012)   
19. Shen, G., Chen, Z., Zhang, P., Moscibroda, T., Zhang, Y.: Walkie-Markie: indoor pathway mapping made easy. In: Proceedings of USENIX NSDI (2013)   
20. Shu, Y., Bo, C., Shen, G., Zhao, C., Li, L., Zhao, F.: Magicol: indoor localization using pervasive magnetic field and opportunistic WiFi sensing. IEEE J. Sel. Areas Commun. 33(7), 1443–1457 (2015)   
21. Shu, Y., Huang, Y., Zhang, J., Cou, P., Cheng, P., Chen, J., Shin, K.G.: Gradient-based fingerprinting for indoor localization and tracking. IEEE Trans. Ind. Electron. 63(4), 2424– 2433 (2016)   
22. Sun, Z., Chen, Y., Qi, J., Liu, J.: Adaptive localization through transfer learning in indoor wi-fi environment. In: Proceedings of IEEE ICMLA (2008)   
23. Wang, Y., Witten, I.H.: Inducing model trees for continuous classes. In: Proceedings of the 9th European Conference on Machine Learning, pp. 128–137 (1997)

24. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: Proceedings of ACM MobiSys (2012)   
25. Wen, Y., Tian, X., Wang, X., Lu, S.: Fundamental limits of RSS fingerprinting based indoor localization. In: Proceedings of IEEE INFOCOM (2015)   
26. Wu, C., Yang, Z., Liu, Y., Xi, W.: WILL: wireless indoor localization without site survey. IEEE Trans. Parallel Distrib. Syst. 24(4), 839–848 (2013)   
27. Wu, C., Yang, Z., Xiao, C., Yang, C., Liu, Y., Liu, M.: Static power of mobile devices: selfupdating radio maps for wireless indoor localization. In: Proceedings of IEEE INFOCOM (2015)   
28. Wu, C., Yang, Z., Xu, Y., Zhao, Y., Liu, Y.: Human mobility enhances global positioning accuracy for mobile phone localization. IEEE Trans. Parallel Distrib. Syst. 26(1), 131–141 (2015)   
29. Wu, C., Xu, J., Yang, Z., Lane, N.D., Yin, Z.: Gain without pain: accurate WiFi-based localization with fingerprint spatial gradient. ACM UbiComp 1(2), 29:1–29:19 (2017)   
30. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Enhancing WiFi-based localization with visual clues. In: Proceedings of the 2015 ACM International Joint Conference on Pervasive and Ubiquitous Computing (2015)   
31. Yang, Z., Wu, C., Liu, Y.: Locating in fingerprint space: wireless indoor localization with little human intervention. In: Proceedings of ACM MobiCom (2012)   
32. Yang, Z., Wu, C., Zhou, Z., Zhang, X., Wang, X., Liu, Y.: Mobility increases localizability: a survey on wireless indoor localization using inertial sensors. ACM Comput. Surv. 47(3), 54:1–54:34 (2015)   
33. Ye, X., Wang, Y., Hu, W., Song, L., Gu, Z., Li, D.: Warpmap: accurate and efficient indoor locating by dynamic warping in sequence-type radio-map. In: Proceedings of IEEE SECON (2016)   
34. Yin, J., Yang, Q., Ni, L.M.: Learning adaptive temporal radio maps for signal-strength-based location estimation. IEEE Trans. Mob. Comput. 7(7), 869–883 (2008)   
35. Yin, Z., Wu, C., Yang, Z., Liu, Y.: Peer-to-peer indoor navigation using smartphones. IEEE J. Sel. Areas Commun. 35(5), 1141–1153 (2017)   
36. Youssef, M., Agrawala, A.: The Horus location determination system. Wirel. Netw. 14(3), 357–374 (2008)   
37. Zhang, L., Liu, K., Jiang, Y., Li, X.Y., Liu, Y., Yang, P.: Montage: combine frames with movement continuity for realtime multi-user tracking. In: Proceedings of IEEE INFOCOM (2014)   
38. Zheng, V.W., Xiang, E.W., Yang, Q., Shen, D.: Transferring localization models over time. In: Proceedings of AAAI (2008)   
39. Zheng, Y., Shen, G., Li, L., Zhao, C., Li, M., Zhao, F.: Travi-Navi: self-deployable indoor navigation system. In: Proceedings of ACM MobiCom (2014)   
40. Zhou, P., Li, M., Shen, G.: Use it free: instantly knowing your phone attitude. In: Proceedings of ACM MobiCom (2014)   
41. Zhou, Z., Wu, C., Yang, Z., Liu, Y.: Sensorless sensing with WiFi. Tsinghua Sci. Technol. 20(1), 1–6 (2015)

# Chapter 6 Self-Deployable Peer-to-Peer Navigation

![](images/86648485f99eb829b934fc3d07092db41f1020ecab8e4846632d3aee976adecf.jpg)

Abstract Most of existing indoor navigation systems work in a client/server manner, which needs to deploy comprehensive localization services together with precise indoor maps for a priori. In this chapter, we design and realize a Peer-to-Peer navigation system, named ppNav, on smartphones, which enables the fast-to-deploy navigation services, avoiding the requirements of pre-deployed location services and detailed floorplans. ppNav navigates a user to the destination by tracking user mobility, promoting timely walking tips, and alerting potential deviations, according to a previous traveller’s trace experience.

# 6.1 Introduction

Various approaches based on WiFi [1, 25], GSM [12], Sound [17], etc., have been proposed to enable localization indoors and further provide navigation services to end users, on the basis of path planing algorithms in addition to precise indoor maps.

While qualified of providing navigation service once appropriately deployed, such localization-enabled navigation systems are limited in two folds. First, they highly rely on an accurate and stable localization service pre-deployed by specific provider, which entails great challenges since current indoor localization systems are not yet ready for wide and easy deployment. Despite of numerous efforts on indoor localization, the applicability of previous attempts, either model-based or fingerprint-based, is significantly limited by labor-intensive deployment and insufficient accuracy. For example, WiFi fingerprinting-based localization requires remarkable initial efforts for bootstrapping yet yields pretty mediocre accuracy [1, 20, 25]. Second, a meticulous indoor map is always required to provide precise building structure and semantic place information, yet is hard and costly to acquire. Mainstream map providers such as Google Maps and Baidu Map currently supply indoor maps only in limited areas like large malls and airports. And these maps are generated mainly from manual construction by expert engineers. Despite of some approaches proposed to crowdsource indoor maps [6, 15], a sustainable incentive mechanism is yet required and the quality of the resulting data is not guaranteed. To conclude, previous navigation systems work in a classical client/server (C/S)

![](images/a274af788a34b2c730f06dbb48e53722f75f7b66ce94cdb28ddddd2730620bf6.jpg)



Fig. 6.1 A usage example of ppNav

thinking, which significantly depend on pre-deployed comprehensive location and map services and have yet to be achieved. A lightweight, efficient, and easy-todeploy approach is strongly urged for practical uses.

In this chapter, we specify an alternative Peer-to-Peer (P2P) navigation mode, which enables efficient navigation without resorting to pre-deployed location service or the availability of indoor maps. As shown in Fig. 6.1, the P2P navigation employs a previous traveller (Alice or Bob) to record his/her trace information (e.g., key turning points) along a path and share it with followers (Claire or David) for navigation. The idea is inspired by two fronts. First, people have widely resorted to non-technical solutions through nature navigation descriptions from others or landmarks in surroundings in daily life. It is demonstrated that people are able to navigate themselves to the destinations if provided timely hints, e.g., to take a turn or go upstairs. Second, P2P architecture has been extensively adopted in computer networks where participants (a.k.a peers) voluntarily offer to provide their own resources available to other peers without the need of a central server. Applying a similar thinking in navigation, P2P navigation enables self-motivated users who have travelled through a path to act as leaders , i.e., recording and sharing specific trace information to navigate potential followers. Several pioneer works have conditionally carried out the leader-follower mode for navigation [16, 28]. Such P2P mode advances especially in social and personal scenarios, where, for example, a group of users arrive successively for an appointment at a specific place or a vendor desires to direct customers to his own shop.

Translating the idea into practice, we design ppNav, a Peer-to-Peer indoor Navigation system for smartphones. In ppNav, a leader records trace information along his travel along a path to a specific destination. Such information, including location specific features such as WiFi measurements and user walking events of interests (e.g., headings, turning, going upstairs/downstairs), are fused to form a reference trace that will be later shared to other followers for guidance. When a follower arrives at the same building and demands an identical destination place, ppNav first directs him/her to lock on a certain point (typically yet not necessarily the same starting point as one leader’s) that connects to the leader-provided reference trace. From then on, ppNav continuously measures the navigation trace information and synchronizes the walking progress with the reference trace. Accordingly, ppNav navigates the follower to the destination by promoting timely walking hints (such as directions and turns) at appropriate locations.

ppNav enables P2P navigation on smartphones without resorting to any predeployed services or precise maps, but its realization entails particular challenges. (1) We expect ppNav to alert users timely and properly by providing correct walking hints at the right time and locations. Without comprehensive localization services, however, we are unable to obtain precise location estimations. Thus given the environmental dynamics and the diversity of devices and walking speeds, how to accurately synchronize the follower’s walking progress against the leader’s reference trace turns into the first important problem to address. (2) As users may visit a specific destination from different starting positions, a friendly navigation system should intelligently lead users to splice the closest reference trace before the trace-driven navigation can come into operation. Since the leader’s reference trace only covers the sampled path and we have neither the knowledge of other unknown areas nor the user’s precise locations, how to guide a user to lock on a path connected to a reference trace arises as a key issue for practical uses of P2P navigation. (3) Incorrect and untimely direction hints both lead to wrong paths for a follower. As we only have the knowledge of the sampled path, ppNav should be able to responsively detect the deviation once a follower has walked off a reference path.

To overcome the challenges, we devise several novel techniques. First we propose a novel concept of fingerprint engram, termed as fingeram, which represents a diagrammed form of sequential WiFi fingerprint measurements along a path. We adopt WiFi signals as the basic vehicle due to its ubiquitous availability worldwide. Although WiFi fingerprints are known to be vulnerable to environment dynamics and only produce ordinary location accuracy for indoor localization, we observe that fingeram holds nice properties for precise trace synchronization. As shown in Fig. 6.2, being the diagrammed form of a sequence of fingerprints, certain features of fingeram remain stable in regards to contraction or amplification (caused by different WiFi sample frequency and walking speeds) and noises (induced by environment dynamics and device heterogeneity). We extract both radio and visual features for trace synchronization and deviation detection. Diving into the spatial propagation characteristics of WiFi signals, we further develop a rotation-based direction finding approach to guide a user to a closest starting location.

![](images/de7f9210061a84c94c8d05e28465f0c979f60b29bf26ad08a26095e71d4f6169.jpg)



(a) Normal version

![](images/ecbf91cf62b69caa2be861fac9c2d9ba04c9825532aec79f1f5189f80bc3aa7d.jpg)  
(b) Shrunk version

![](images/13c88dcb6537c256de2c3353cf4022cbd7ad09bfd8746443c6f1e1098af326ef.jpg)



(c) Amplified version

![](images/a3feaf26263a15653ee5ff032b862ac89e27bfcd29e8881d9eb315f7b1e6d81e.jpg)



(d) Noisy version   
Fig. 6.2 Fingerams of the same trace with (a) normal, (b) lower, (c) higher sampling frequency and (d) measurement noises

Unifying the above techniques together, we implement ppNav on Android platform. We conduct extensive experiments in multiple real-world scenarios. Experimental results demonstrate that ppNav yields a 90 percentile spatial error of 1.6 m and an average error of 0.9 m for follower tracking and detects deviations timely within 4.5 s (9 samples at 2 Hz).

The subsequent sections begin with a review of related work in Sect. 6.2. We then present the motivations and challenges in Sect. 6.3, followed by a brief overview and the definition of fingeram in Sect. 6.4. The detailed design, implementation and evaluation of ppNav is then presented in Sects. 6.5, 6.6, and 6.7 respectively. And finally we discuss some open issues in Sect. 6.8 and conclude this work in Sect. 6.9.

# 6.2 Related Works

Indoor localization and navigation have been extensively studied in recent years. Traditional indoor location systems, however, rely on prior deployed localization services to provide navigation to users. Many crowdsourcing-based schemes have been proposed to reduce deployment costs of indoor localization systems by distributing the fingerprint calibration task to a large number of participatory users [13, 19–21]. While facilitating the deployment stage, these works usually assume the availability of precise indoor maps, which, however, are difficult to obtain in practice. Some researchers explore to incorporate inertial sensing and crowdsourcing to construct indoor floorplans for indoor localization and navigation [4, 6, 15, 19]. Appropriate mechanisms need to be designed to guarantee the precision of resulted maps as well as encourage user participation [23, 27]. Different from traditional navigation services, ppNav is an easy-to-deploy system that do not depend on pre-deployed comprehensive location services and precise digital maps.

The leader-follower mode has been referenced in several recent systems [14, 16, 28]. Riehle et al. [14] navigates blind users using customized device for magnetic sensing. Two recent systems, Travi-Navi [28] and FOLLOWME [16], both employ trace-driven navigation on smartphones. Travi-Navi synthesizes vision, WiFi and other inertial information to enable a user to easily bootstrap navigation services without infrastructure support. FOLLOWME exploits magnetic sensing and deadreckoning to achieve last-mile navigation for smartphone users. The design of ppNav is inspired by these systems, but is very different from several aspects. First, both the two systems assume that followers will arrive at the same entrance with previous leaders, which is not realistic in practice. In contrast, ppNav can direct a user to lock on a closest path from a random start point. Second, while vision-based Travi-Navi provide intuitive tips for followers, the image quality is easily impaired by human motions and lighting conditions. To overcome this, users may need to hold smartphone vertically and steadily during walking. ppNav minimizes the cooperation efforts for path locking-on and does not exert any constraints during navigation. Finally, although both Travi-Navi and ppNav exploit WiFi measurements,we exploit sequential fingerprints in a novel diagrammed form, which is demonstrated to be more efficient and could further benefit various other WiFi-based applications, such as indoor localization, frequent trajectory mining, location-based AP access control, etc.

# 6.3 Motivations and Challenges

# 6.3.1 Model Description

In everyday life, users urge for effective navigation in many scenarios. For example, a shop owner would like to deploy a self-owned navigation service to direct a customer to his shop. In contrast, a customer also demands for a navigation service to visit a specific shop in gigantic malls. A meeting coordinator would like to guide other participants smoothly all the way to the gathering place, while one may need a navigation service to help reach a specific appointment location. Furthermore, when a driver parks his car in a large lot and go shopping, a friendly guidance to find his car when he finishes shopping would save much boresome time and thus largely improve the quality of shopping experience.

Due to the lack of pre-deployed comprehensive localization services and precise indoor maps, most of previous navigation based on accurate locations are infeasible for such scenarios. In this work, we attempt to develop an alternative model that does not rely on pre-installed location services and knowledge of indoor maps. Note that in above scenarios, multiple users will traverse the same path. Thus our key idea is nothing more than to leverage the experience of previous travellers, just as we naturally behave in routine life. Specifically, we collect specific trace data from previous travellers and extract appropriate walking hints to navigate others. Every user travelled a path could act as a leader for that path by recording trace information and sharing with others. And one could participate as either a leader or a follower, depending on the specific scenario. The leader and follower could even be the same person in case that one travels a path for multiple times. We term such operational model as Peer-to-Peer navigation, which does not necessarily rely on pre-deployed services and is very different from most conventional localization and navigation systems that work in a client/server mode [1, 13, 18].

# 6.3.2 Usage Examples

As shown in Fig. 6.1, suppose a meeting is arranged in a room marked by the red point. The meeting coordinator Alice arrives earlier at entrance A and walks from there to the meeting place as indicated by the red arrowed line. One participant Bob, who is familiar with the place, arrives at entrance B and travels to the meeting room along the blue arrowed path. To provide P2P navigation services for other participants, Alice and Bob could run the ppNav App during their own walk and generate a corresponding reference trace. Without such services, other participants who visited the meeting location for the first time could only get the directions by themselves or ask for directions step by step from others like property staffs in the building.

Specifically, during Alice and Bob’s walks, the ppNav App running on their smartphones measures WiFi fingerprints and necessary sensor data (including gyroscope, magnetometer, barometer), which will be automatically processed and packed into a reference trace. Guiding information, e.g., turning, walking upstairs/downstairs, are also recognized and recorded in the reference trace for subsequent navigation. When other participant, e.g., David, arrives at the same entrance B with Bob, ppNav locks on to him at entrance B with Bob’s reference trace and delivers the reference information provided by Bob to David. Then ppNav navigates David by estimating the walking progress, i.e., relative locations to Bob’s reference trace. Based on the walking progress estimation, relevant walking hints (e.g., turning) extracted from the reference trace will be timely promoted on David’s phone. In case a participant Claire arrives at a different entrance, e.g., C in Fig. 6.1, ppNav first directs her to the nearest reference trace, i.e., the one provided by Alice, and then perform regular navigation with the reference information from Alice. Similar data are measured using smartphone during a follower’s walk.

During either leading walks or following walks, users need not to intentionally hold the smartphone in hand except that the follower may need to hold the phone in front of the chest when locking on the path of a reference trace since we make use of body blockage effects for this purpose. In general, they merely need to turn on the App and keep it running during a walk. In addition, the reference traces contributed by Alice and Bob to their friends for this meeting can be shared via cloud with the public when authorized. Furthermore, the following trace of Claire, if no deviation occurs during her walk, can also be leveraged as a reference trace for others.

Another attractive potential applications of ppNav is self-navigation for car finding in large indoor parking lots, a well-known annoying and knotty problem in modern society. When one user parks his/her car at a specific pool (denoted as P), he/she can use ppNav to record the trace from P to the parking lot exit/entrance (denoted as E). Then the recorded trace information can be used as the reference trace from E to car pool P (by appropriately reversing it). Later, when he/she comes back to E, ppNav could navigate him/her back to the specific pool with the reference trace collected by him/herself.

# 6.3.3 Design Challenges

ppNav only exploits the sensor data (including WiFi measurements and inertial sensory readings) along the pathways. Instead of accurately locating a user for navigation, we need to track the follower’s relative locations with respect to the leader’s reference trace. We adopt WiFi signals as fingerprints in ppNav thanks to the worldwide availability and easy accessibility on commodity smartphones. Existing fingerprint-based localization, even with a complete radio map of the whole building, yields considerable location errors [8, 10], e.g., >5 m, which easily result in confusions among adjacent pathways in modern buildings. As we do not sample the whole building in ppNav, the accuracy would be even worse. Thus previous localization approaches can not be directly applied to obtain accurate relative locations in ppNav. Existing techniques also fail to detect deviation when a user veers off the correct path. Given that the fingerprints observed by different users differ in sampling frequency, total amount and absolute RSS values, a new model to utilize WiFi measurements for precise trace synchronization and deviation detection needs to be designed.

Moreover, a friendly navigation system does not assume all users destined for a specific place start from the same location. When a follower appears at a position that has not been travelled by any leader, ppNav first needs to direct him to lock on a certain path. As we only sampled specific pathways and most areas are still unexplored, guiding a user from an unknown position to a reference path is like navigation in the dark without global knowledge or precise locations. Novel techniques are needed to shed light on the blinded period before the trace-driven navigation could take over.

# 6.4 Overview

As shown in Fig. 6.3, ppNav consists of two major parts, the trace generation part for the leader application and the navigation part for the followers.

Reference Trace Generation We sample gyroscope, magnetometer and barometer to detect the guider’s motion events during the trip, such as steps, turns, going upstairs/downstairs, walking/stop status, etc. Such motion events, together with a fingeram generated from sequential WiFi measurements, are shaped into a reference trace when the guider finishes the travel. The reference trace can be shared directly to a particular follower or via cloud with other users.

Path Locking-on As a user may appear at a location that is different from the starting point of the leader, we need to direct a user to approach a nearest path that leads to the destination and has been travelled previously. This module designs a simple yet effective method for this purpose. Our method searches for the most likely directions to an estimated target point via easy cooperation of the follower himself.

![](images/1ff8d9b5ca5574a764cd6153711c3f4780795f69e869f4500e9487e4f963ab55.jpg)



Fig. 6.3 System architecture

Walking Progress Estimation When a user is locked on a reference trace, ppNav navigates him to the destination by promoting timely motion hints, according to the synchronous events indicated by the reference trace. To achieve this, ppNav synchronizes the follower’s instantaneous trace with the reference one using specific features extracted from the fingerams.

Deviation Detection This module detects whether a user, after locked on a reference trace, is still on the correct path, in case that he does not follow well, e.g., taking a wrong turn. We propose a novel effective and efficient deviation detection algorithm based on fingerprint distance trend.

Note that the reference trace generation module works only on leaders’ side while some common engines such as motion event detection and fingeram formation run on both the leader and follower applications.

# 6.5 Fingeram Specification

# 6.5.1 Definition and Generation

WiFi fingerprint matching yields only limited location estimation accuracy, we observe that sequential fingerprints along a set of continuous locations (i.e., a path) behave much more stable. Fingerprint matching using sequential or just multiple fingerprints has been demonstrated to improve location accuracy [8, 20, 22]. Since our core task is to synchronize the reference trace and the following one, we naturally adopt sequential fingerprints observed along the path rather than discrete fingerprints of individual locations.

Trace synchronization based on sequential fingerprints is non-trivial. Walking along an identical path with the same starting and ending points, different users can observe different fingerprint sequences due to diverse behaviors and hardware capabilities. As a result, raw fingerprints of different traces could not match each other well. Inspired by advanced image processing techniques [2, 9], we propose to diagram the sequential WiFi fingerprints into a visual image and incorporate imagerelated features for matching. We term the diagrammed sequential fingerprints as fingeram thanks to its connotations of fingerprint diagram in addition to fingerprint engram. The former phrase depicts our core novelty in trace synchronization via fingerprint matching with both radio and visual features. The later embodies the key idea of ppNav to reuse the indications left behind by previous travellers as the term engram means a memory trace stored as biophysical or biochemical changes in the brain.

The fingerprint sequence of a trace can be represented as a matrix ${ \cal F } =$ $[ f ^ { ( i , j ) } ] _ { m \times n }$ , where each column corresponds one fingerprint, $f ^ { ( i , j ) }$ indicates the RSS value of the ith AP in the j th fingerprint measurement, m is the total amount of observed APs and n is the number of samples during the trace. To transform a fingerprint sequence into a fingeram, we map the RSS matrix into an 8-bit grayscale image, which results in a visual form of the fingerprint sequence. Without loss of generality, we still use F to denote the diagrammed fingeram. Figure 6.2a shows an illustrative example of fingeram, where one pixel corresponds an RSS value in the matrix of fingerprint sequence. Note that the AP order affects the image patterns of fingeram but does not pose an issue since the order, once determined, is unchanged throughout the navigation.

Compared to the naive fingerprint sequence [20], the unique advantages of fingeram lie on two fronts. First, although the absolute RSS fingerprints differ from leader’s trace to the follower’s, certain trends may keep stable for a sequence of fingerprints along a spatial path. For example, despite of absolute RSS variations, the RSS trend of each AP along a specific path keeps relatively consistent [15]. Second, the fingerprints, when appropriately visualized, also enjoys graceful image attributes, e.g., different images with similar visual pattern but different sizes, scales, and resolutions could be accurately matched [2, 9]. Recall Fig. 6.2, although fingerprint sequences along the same path may vary due to various distortions such as lower/higher sampling frequency and measurement noises, which result in contracted, amplified and stained images respectively, the internal patterns of corresponding fingeram remain unchanged. These underpin the feasibility of trace synchronization via fingeram matching and encourage us to extract signal-based radio features and image-based visual features to serve trace-driven navigation.

# 6.5.2 Radio Features

As a visual version of sequential fingerprints, fingeram contains internal radio features that keeps stable over different traces along path. Specifically, the RSS changing trend is observed to be relatively stable along a specific path [15, 28]. Taking Fig. 6.4 as an example, suppose a user walks along the pathway. When he walks towards and then away from an AP, the corresponding RSS values may first increase and then decrease, resulting in the trend with a peak. Despite of diverse devices and walking speeds, different users would observe such a similar trend along the same path. Generally, the peak of an AP appears at the closest location on the path to that AP and thus turns out to be a spatially stable marker for a path.

![](images/9ab4c95d3f7affcf0d9a761ae35cba7049d9145fa3b722311595618a9c6419c4.jpg)



Fig. 6.4 Illustrative RSS peaks   
![](images/6000c351670b8a2cdd130fbfb12afd5a8fa9cd47058db5f1082afaac2a0bdbb7.jpg)



Fig. 6.5 RSS trends of 3 APs observed by different users

As shown in Fig. 6.5, the location offsets of the RSS peaks observed by different users are limited within 3.7 m, while the RSS differences can be as large as 10 dBm. In addition, one would encounter multiple RSS peaks from different APs within a path. Thus RSS peaks of all APs observed within a trace, which we term as radio markers hereafter, turn out to be effective alignment anchors for trace synchronization. As shown in Fig. 6.6, consistent radio markers can be detected from the fingerams of the reference trace, even though they are distorted in lengths and noises.

![](images/3e0faeea8853d3d2849fbbf36ff21b4fa249b571a714badfc6b26d8be22aa933.jpg)



Fig. 6.6 Radio markers in fingeram

# 6.5.3 Visual Features

In addition to the inherent radio features, fingeram also shares wonderful advantages of visual images. Various image matching techniques can be utilized for fingeram alignment [2, 9]. In practice, many factors impact the quality of generated fingerams. For example, different device gains lead to biased RSS observations, resulting in fingerams with diverse brightness. In addition, different sampling frequencies and different walking speeds both result in fingerams of different sizes. Yet we argue that certain features constrained by AP distribution and space geometry may keep unchanged under these distortions. Therefore, we can seek distinctive image features and efficient matching methods that are robust to changes in images scale, illumination and noises for precise fingeram alignment.

Specifically, we adopt SURF (Speeded Up Robust Features) [2], a widely used feature detector that can be used for object recognition, registration and classification in computer vision. SURF detects points of interests, usually on high-contrast regions on an image, as “feature descriptors” of the image that are detectable under distortions. Similar features will be identified and matched from other images as long as they preserve similar patterns or contain the same objects. In ppNav, we observe that for fingerams along the same path, the relative positions between a portion of such key points would persist and hence provide another dimension of anchors for fingeram alignment. Similar to radio markers, we term these image-based anchors as visual markers hereafter. As shown in Fig. 6.7, a considerable number of visual markers can be detected from fingerams, from which we can select reliable ones for walking progress estimation.

![](images/dd4872618ed527545e04242bf065d2c4e8848ad1b1136bf9bb1936d2a88ae056.jpg)



Fig. 6.7 Visual markers in fingeram

# 6.6 ppNav Design

# 6.6.1 Trace Generation

When a user takes a walk along a path destined for a place, ppNav can automatically construct a reference trace $J _ { R } \ =  { \cal F } , { \cal E } >$ for that path. Specifically, F is the fingeram of measured WiFi fingerprints along the path, where each column corresponds an individual fingerprint. E marks a series of concomitant motion events such as turning and upstairs/downstairs extracted from inertial sensor data. Without location information, F and E are time-stamped as well as indexed with WiFi samples relative to the starting points. ppNav involves common sensors that are available on commodity smartphones for navigation. Specifically, we employ the following data as system inputs of ppNav. We measure WiFi observations as sequential fingerprints for constructing fingeram, which is used for estimating the follower’s walking progress by fingeram synchronization. Gyroscope and magnetometer are used for detection of turning events while barometer is further leveraged for level-change detection.

As the fingerprints are continuously measured during walking, we employ a low-pass filter to sift out partial uncertain noises before converting them into a fingeram. Considering abundant APs crowded in modern buildings, a portion of low quality APs that appear few times or always hold extremely low RSS values are not necessary for fingeram and can be removed. Specifically, we define a continuous effective sampling rate $r _ { s }$ , defined as follows, to further sift out low-quality APs.

$$
r _ {s} = e _ {s} / c _ {s},
$$

where $c _ { s }$ denotes the max sample amount among all APs within a trace segment, and $e _ { s }$ denotes the amount of detected samples of current APs. We merely select the APs whose $r _ { s } \ge 0 . 6$ to form fingerams in our scenarios, which would hold certain RSS trends with high confidence, although they might still experience missing RSS problem to some extent. We also remove APs with less than 10 samples within the whole trace, since they generally do not exhibit effective trends or peaks.

Considering that one or more APs, e.g., personal hotspots, might appear in the leader’s reference trajectory yet do not present at all in the follower’s trace (and vice versa), we only select the common APs existing in both trajectories when aligning the reference and following traces. There might also be several APs whose locations change between a pair of leading and following traces although they are observed in both traces. The APs may yield radio features with inconsistent relative positions in a pair of traces and thus influence the alignment results. Fortunately, such APs are commonly only a very small portion of detectable APs and we can apply robust techniques to mitigate their impacts (See Sect. 6.6.2).

As for motion event detection, various advanced techniques have been developed and can be used [3, 6, 7, 19]. Hence in this section we mainly focus on the navigation design and leave a brief introduction on motion event detection in the next section.

# 6.6.2 Walking Progress Estimation

Given a reference trace $J _ { R }$ , we first assume a user arrives at the same starting position and discuss navigation in such case.

As mentioned above, the key to provide timely walking tips is to accurately estimate the follower’s walking progress relative to the reference trace. In ppNav, we synchronize the follower’s trace with the reference trace by aligning their fingerams based on their radio and visual features as specified in Sect. 6.5. Suppose a user is locked on to a reference trace $J _ { R } = < F _ { R } , E _ { R } >$ and denote his own navigation trace as $J _ { N } = < F _ { N } , E _ { N } >$ . The trace synchronization problem is to find an optimal alignment between the two fingerams FN = [f (i,j )N ] $F _ { N } = [ f _ { N } ^ { ( i , j ) } ] _ { m \times n _ { N } }$ and $F _ { R } = [ f _ { R } ^ { ( i , j ) }$ ] m×nR . Formally, the alignment of the ith sample in $F _ { N }$ and the kth sample in $F _ { R }$ is represented as follows:

$$
h: \boldsymbol {f} _ {N} ^ {(i)} \mapsto \boldsymbol {f} _ {R} ^ {(k)}, \tag {6.1}
$$

where $\pmb { f } _ { N } ^ { ( i ) }$ and $f _ { R } ^ { ( k ) }$ denote the ith (index of latest sample) and kth column in $F _ { N }$ and $F _ { R }$ , respectively. Since no rotation is involved in the mapping, there are basically scaling and translation operations during the alignment. Hence h can be derived in the form of $h ( i ) = \alpha i + \beta$ , where $\alpha$ and $\beta$ indicates the respective scale and translation factors to align $F _ { N }$ to $F _ { R }$ . Figure 6.8 shows an illustration of alignment by fingeram markers via scaling and shifting. We extract two types of markers, i.e., radio markers and visual markers, for the fingeram alignment thanks to their location stability regarding various distortions. Radio markers of the same AP are observed at close physical locations, while visual markers corresponding to similar pattern generally appear at the same relative locations of a fingeram.

Fig. 6.8 Trace alignment by fingeram markers via scaling and shifting   
![](images/720b829c9bb9902cc58034fbc66b3b7cec76583281bf43025e744d62cace9c86.jpg)



![](images/ee363345508d0dd5348fc9f73a8913b4a0eb225b885c435b62728f1820d67449.jpg)



Fig. 6.9 Visual markers filtered by AP space (markers denoted by hollow circles are omitted)

As shown in Fig. 6.9, each extracted visual marker $\pmb { v } = ( \boldsymbol { v } ^ { ( x ) } , \boldsymbol { v } ^ { ( y ) } )$ corresponds to $v ^ { ( y ) }$ th AP in the $\boldsymbol { v } ^ { ( x ) }$ th sample of the fingeram. Original SURF algorithm outputs a considerable number of such markers, which are not all necessary for alignment since in our case there is no image rotation issue. For all matched visual markers of two fingerams, we only need to consider those having the same y-axis coordinate $v ^ { ( y ) }$ (i.e., corresponding to the same AP), which efficiently reduces the amount of visual markers. Figure 6.9 shows an illustrative example of the visual markers extraction matching results. For the fingeram of a sequence of 250 fingerprints, SURF detector can output as many as >200 visual markers, which can be pruned to around one-fifth. The remained matched visual markers are denoted as $V _ { N } =$ {v(1)N , v(2)N , · $\{ \pmb { v } _ { N } ^ { ( 1 ) } , \pmb { v } _ { N } ^ { ( 2 ) } , \cdots , \pmb { v } _ { N } ^ { ( n _ { v } ) } \}$ , v N (nv ) and $V _ { R } = \{ \pmb { v } _ { R } ^ { ( 1 ) } , \pmb { v } _ { R } ^ { ( 2 ) } , \pmb { \cdot } \pmb { \cdot } , \pmb { \upsilon } _ { R } ^ { ( n _ { v } ) } \}$ {v(1)R , v(2)R , R v(nv ) for the follower’s and the leader’s trace, respectively.

In addition to visual markers, we also identify radio markers once they appear (note that they may not be observed within too few fingerprint samples). Radio markers are recognized by identifying potential RSS peaks of an RSS sequence as done in [15]. Fusing the radio markers contributed by different APs in the navigation fingeram, we obtain a set of radio markers $R _ { N } = \{ \pmb { r } _ { N } ^ { ( 1 ) } , \pmb { r } _ { N } ^ { ( 2 ) } , \cdots , \pmb { r } _ { N } ^ { ( n _ { r } ) } \}$ (nr ) where $\pmb { r } ^ { ( k ) } = ( r _ { N } ^ { ( k , x ) } , r _ { N } ^ { ( k , y ) } )$ (r ) is a radio marker of the r (k,N $r _ { N } ^ { ( k , y ) }$ th AP and is observed at the r (k, $r _ { N } ^ { ( k , x ) }$ N N  th sample. Similarly, we can also extract a series of radio markers of N corresponding APs in the reference trace, denoted as $R _ { R } = \{ \pmb { r } _ { R } ^ { ( 1 ) } , \pmb { r } _ { R } ^ { ( 2 ) } , \pmb { \cdot } \pmb { \cdot } , \pmb { r } _ { R } ^ { ( n _ { r } ) } \}$ · , r rR Only radio markers of APs that are observed in both traces will be considered for alignment.

Integrating all markers, we solve the alignment by minimizing the least square errors as follows via linear regression [5]:

$$
\arg \min _ {\alpha , \beta} \sqrt {\sum_ {k = 1} ^ {n _ {v}} \left(v _ {R} ^ {(k , x)} - h (v _ {N} ^ {(k , x)})\right) ^ {2} + \sum_ {k = 1} ^ {n _ {r}} \left(r _ {R} ^ {(k , x)} - h (r _ {N} ^ {(k , x)})\right) ^ {2}}. \tag {6.2}
$$

To mitigate the influence of abnormal data, caused by unstable WiFi signals or moving personal hotspots, we employ a robust linear model (RLM) [5], which uses iteratively re-weighted least squares with a bisquare weighting function, instead of the ordinary linear model (OLM). Figure 6.10 demonstrates that, with sufficient radio markers, OLM could evidently mitigate the impacts of abnormal data, which will be further validated in Sect. 6.7.

According to the derived $\alpha$ and $\beta _ { : }$ we could scale and shift follower’s trace to map to the reference trace by mapping function $h ( i ) = \alpha i + \beta$ . By doing this, the follower’s latest sampling index is mapped to a specific index in reference trace, which is the follower’s walking progress relative to the reference trace. Then appropriate tips for navigation (e.g. turn or level change) could be promoted to the follower according to the motion events indicated in the reference trace.

# 6.6.3 Deviation Detection

In case the follower deviates from the trace, e.g., taking a wrong turn, we need to intelligently detect whether the user veers off the path or not and alert the user timely if yes. An intuitive way to achieve this is applying a threshold on the optimization errors in Eq. 6.2. However, due to the variant trace lengths and uncertain amounts of markers, a fixed threshold value does not apply to various scenarios. In ppNav, we propose a novel algorithm based on fingerprint distance trend to effectively detect deviation.

Our key observation is that fingerprint similarity roughly decreases over increased distances. Specifically, if we match a fingerprint f against a series of nearby fingerprints observed on its opposite sites along the path, i.e., preceded and posterior fingerprints of $f ,$ , we can obtain a “V”-zone pattern in decrease even to zero and then increases. As we can precisely estimate a user’s walking progress if he is on the path, a “V”-like pattern will be still produced when we compare a fingerprint of the navigation trace to the sequence of nearby fingerprints of its aligned fingerprint in the reference trace. In contrast, fingerprint distances compared to whatever segment of fingerprints on the reference trace only yields random trends if the user deviates the path since the fingerprint is distant to any of those within the reference trace. Inspired by this observation, we devise novel algorithm to detection user deviation by identifying and comparing the fingerprint distance profiles.

Suppose the latest fingerprint observed by the follower is $\pmb { f } ^ { ( k ) }$ , which is mapped to a fingerprint $\pmb { f } ^ { ( k ^ { \prime } ) }$ in the reference trace sampled at $k ^ { \prime } ~ = ~ h ( k )$ . Considering respective d fingerprints preceded and posterior to $\pmb { f } _ { R } ^ { ( k ^ { \prime } ) }$ on the reference trace, we can derive a fingerprint distance profile for $f _ { N } ^ { ( k ) }$ using Euclidean distance as follows:

![](images/3b40b630c1714823addb70d84e9755837a89a9d0657dbbf97731dbfa92d73d34.jpg)



Fig. 6.10 Reduce the influence of abnormal data via robust linear regression

$$
\phi \left(\boldsymbol {f} _ {N} ^ {(k)}, \boldsymbol {f} _ {R} ^ {(k ^ {\prime} + i)}\right) = \| \boldsymbol {f} _ {N} ^ {(k)} - \boldsymbol {f} _ {R} ^ {(k ^ {\prime} + i)} \|, i \in [ - d, d ], \tag {6.3}
$$

which results in a distance profile $P _ { N }$ of $2 d + 1$ items. Note that we only take common APs that appear in both traces into account and typically $\textit { d } \ < \ 1 0$ fingerprints are sufficient, as demonstrated by our experiments. Similarly, we can calculate a profile for $\boldsymbol { f } _ { R } ^ { ( k ^ { \prime } ) }$ , which is supposed to be the aligned fingerprint with $f _ { N } ^ { ( k ) }$ , as $P _ { R } = \{ \phi ( f _ { R } ^ { ( k ^ { \prime } ) } , f _ { R } ^ { ( k ^ { \prime } + i ) } ) , i \in [ - d , d ] \}$ .

We conduct preliminary measurements to validate our observations. As shown in Fig. 6.11, suppose the reference trace should be $\mathrm { ^ { \mathrm { \scriptsize ~ \stackrel {  ~ } { \cdot \mathrm { \scriptsize ~ A - B - C - D - E - F - G - H - I ^ { \prime \prime } } } } } }$ , but the follower turns mistakenly at point A and takes a trace as $\mathrm { \mathrm { \mathrm { \Sigma ^ {  } A - J - K - L - M - N - O - P - Q ^ { \prime \prime } } } }$ . We calculate the distance profile $P _ { N }$ and $P _ { R }$ for each fingerprint sample during the trace from A to I. The results are depicted in order in Fig. 6.12. As seen, when the user does not deviate away, both $P _ { N }$ and $P _ { R }$ exhibit apparent V-pattern, although slight distortions are observed on $P _ { N }$ due to environmental dynamics and device diversity. While the graceful shape of $P _ { R }$ consistently holds (actually for any sample), $P _ { N }$ suffers significant deformation as the user veers off the path. Thus by examining the profile shapes of $P _ { N }$ to $P _ { R }$ , we can confidently identify whether the user deviates from the destined path.

Instead of directly evaluating the absolute $P _ { N }$ distribution, we attempt to compare $P _ { N }$ to $P _ { R }$ for deviation detection in purpose of achieving adaptivity to various scenarios. Specifically, we model the “V”-like distribution as a parabola and apply quadratic model $y = a ( x - b ) ^ { 2 } + c$ to fit the profiles and examine the similarity between them. As shown in Fig. 6.12, we mainly concern coefficient a that embodies the curvature of the output parabola to compare the coupled distance profiles. Concretely, we devise a relative metric for this purpose:

![](images/0b5e52354b94e448485561f51bbf167dcca7cb23c00bd13d8243c1700b9e9cb2.jpg)



Fig. 6.11 Experimental scenario of fingerprint distance profile

![](images/54d25134e53f4fc823c378368299636edfc86d63905bcaa90385db7f7ce8175c.jpg)



![](images/1c79ac5afb1aa99b2f11560131526eca9e08562bddb0313888fa2c1ec7876192.jpg)



![](images/6b2897f453db4b4f0eec48e1459604734b657295cb6e24bb0d62de5620ac1ce2.jpg)



![](images/fe1456ef37e879a26ee91cdf811b6d0838c541afac3e1e3e217ccd4d7771f12d.jpg)



![](images/b7c492e6b0f87f0edde9787f64ae102a36172a4b44636d4dba06c65bfa2f96c4.jpg)



![](images/71cd9d056ba0d9a752595b9bd0848298286ee1744990981b4fc05018785ca434.jpg)



![](images/98a49d2a7fd06fb7f25aaac127a0b8ac954e62ecb12281babbbb7d51d35c0a6b.jpg)



(g)

![](images/e7eb79e808b98409e87c94c6eb5ab057ef434cfa2a817e48f08dd8b9a26225f6.jpg)



Fig. 6.12 Fingerprint distance profiles of different samples from deviation. (a) Offset 0. (b) Offset 1. (c) Offset 2. (d) Offset 4. (e) Offset 5. (f) Offset 6. (g) Offset 7. (h) Offset 8

$$
\tilde {a} = \frac {a _ {N}}{a _ {R}}, \tag {6.4}
$$

where $a _ { N }$ and $a _ { R }$ denote the estimation parameters of $P _ { N }$ and $P _ { R }$ , respectively. Larger a indicates more similar profiles and vice versa. We then apply a thresholdbased method to detect a deviation by examining the estimated $\tilde { a }$ of successive three samples. According to our experiments, we set the threshold of $\tilde { a }$ as 0.6 which balances the detection rate and delay.

# 6.6.4 Path Locking-On

Previously we simply assume that a follower is locked on to the same entrance of a reference trace, which, however, is not guaranteed in practice. Recall Fig. 6.1, a user could arrive at different entrances. In such case, ppNav should direct him to the nearest path covered with at least one reference trace. Without pre-deployed location service and global map knowledge, the task is very difficult to navigate in the unexplored dark area. Previous works [16, 28] merely omits this problem and assumes followers will appear at the same entrance with the leader.

If a user is outside the building, he can navigate to a certain entrance using GPS service, which, however, will be no longer applicable when he has entered the building. We address this challenge in ppNav by exploring and exploiting the characteristics of AP space. The task is divided into two parts: First, we search for a locking-on point on the nearest reference trace. And second, find a direction towards the targeted point and direct the user there.

In ppNav, we seek the closest locking-on point as starting position to save locking-on costs. We observe that closer locations usually observe more common APs. Thus we induce an intuitive metric of common AP amounts to select the point that shares the most common APs with the user’s current location as the targeted starting point. As shown in Fig. 6.13a, we compare the fingerprint measured at the user’s current location to all fingerprints within a reference trace and depict the common AP amounts. As seen, the point that reports the highest common AP amount is pretty close to the spatially nearest point, with only an offset of 6 samples (about 3 m). Although the targeted point selected in this way is not always the closest one, it is acceptable for a follower to take a slightly long walk for initial location.

Once a targeted position is selected, we attempt to guide a user to there with the least efforts and without external location services or map information. The key insight to find the right direction towards targeted starting point is to leverage signal blockage of human body itself, as inspired by [26]. Specifically, when a user turns a circle with his phone, he may observe stronger RSS when facing a certain AP and lower RSS when he turns his back to it. Such phenomenon is leveraged in [26] to find the direction of an AP. In ppNav, we extend to multiple APs for direction finding between two distant locations.

Figure 6.13 demonstrates an illustrative scenario where the user can easily navigate to the targeted starting point with not complex intervention. As shown in Fig. 6.13b, suppose the user is currently at $L _ { C }$ and the targeted point is $L _ { T }$ . We ask the user to turn a circle with a relatively slow speed, with the phone in front of the chest, and record a series of RSSs for each AP. To mitigate the RSS gains brought by device diversity, we only remain those APs that are also observable at $L _ { T }$ , yet with RSS values consistently lower than those measured at $L _ { T }$ . Then for each remained AP, we can estimate its direction $\theta _ { s }$ , which is roughly the direction that observes the strongest RSS (when the user is facing the AP), and direction $\theta _ { w }$ , which is the opposite to the direction that observes the weakest RSS (when the user is backing to the AP) within the circle (Fig. 6.13c). Note that we do not use the APs whose observed RSS values during the turning at $L _ { C }$ are consistently higher than those at $L _ { T }$ , because these APs may lead to wrong direction estimations if they are located between $L _ { C }$ and $L _ { T }$ . Suppose there are k APs involved and the ith AP is in direction $\theta ^ { ( i ) }$ . The forward direction of the user is then derived by synthesizing all these directions as follows.

![](images/a845a827cf28e2312467ebb7e88ba7d0f599ded6df5ba14f12c4094e67a1d8c0.jpg)



(a) Target point locking

![](images/392242fa98ff1ada67d436f03f0a0cf19f1f31b1523d9df276cbd0d5c53e8c6d.jpg)



(b) The user rotates in place

![](images/1686546fa468c8f7bed5350abddbcde1a5b6d9d2d0dcb7b96fb5cad2671a2af6.jpg)



(c) RSS by different direction

![](images/1d33690bcd92f9308524aa0efa3775319e18e20790a6783b821345fdf764d6f5.jpg)



(d) Synthesized direction   
Fig. 6.13 Lock on right direction for target point: (a) The point shares the largest number of common APs is physically close to the nearest location; (b) The user spins around slowly with a smartphone in front of his/her body; (c) Observed RSS values of several APs; (d) Direction synthesization based on estimated APs’ directions

$$
\bar {\theta} = \frac {1}{k} \sum_ {i = 1} ^ {k} \theta^ {(i)}, \tag {6.5}
$$

where $\theta ^ { ( i ) } = ( \theta _ { s } ^ { ( i ) } + \theta _ { w } ^ { ( i ) } ) / 2$ for robustness.

Given an estimated forwarding direction, the user may need to judge the path by himself in the uncharted area before he is locked on. We request the user to iteratively turn a circle to refine the direction, especially when he encounters a crossing or a wall. To determine whether the user is on the path or not, we successively calculate the fingerprint similarity, which is supposed to increase when the user get closer to the path and decrease in contrast, as we have done in the deviation detection module. Hence the point from which the fingerprint similarity starts decreasing from an increasing trend is probably the targeted location where the user gets on the path.

![](images/1314b38cf037572f608251d0896ebfec41ba87f0eb5d00855197d1e16eb57763.jpg)



![](images/6dbebe4b28f33e16bbbf3e58d166a5a4253f931e34196b9116302c22859cc8f1.jpg)



（a)

![](images/a60dba783850b456cdd0326544b960d2bb67a74f6cdac69065e7a2790b85fc30.jpg)

![](images/9f2083548977b18878bfcfa6a14c025ffe436aa209c254ad4da99148ca37fa38.jpg)



(b)   
Fig. 6.14 Experiment environments in (a) academic building and (b) office building

# 6.7 Implementation and Experiments

# 6.7.1 Experimental Setup

To evaluate ppNav, we build a prototype on commodity smartphones (Google Nexus 5 and Nexus 7) running Android platform. We conduct experiments in both (I) an academic building with a testing area of $6 8 { , } 0 0 0 \mathrm { m } ^ { 2 }$ and (II) an office building with an area of $1 1 { , } 0 0 0 \mathrm { m } ^ { 2 }$ , as shown in Fig. 6.14.

We recruit four volunteers to participate in our experiments. As shown in Fig. 6.14, we let the leader travel along the path $\mathrm { \ddot { \vec { A } } \vec { \partial } \vec { \Gamma } \vec { \Lambda } \vec { \partial } \vec { \Gamma } \vec { \Lambda } \vec { \partial } \vec { \Gamma } \vec { \partial } \vec { \Lambda } \vec { \partial } \vec { \Gamma } \vec { \partial } \vec { \Lambda } \vec { \partial } \vec { \Lambda } }$ and $\mathrm { ^ { 6 6 } G {  } A ^ { 5 7 } }$ as the reference trace in both area. Then we employ three followers to walk long the trace with timely tips by ppNav. Specifically, the followers are not informed of the destination and the exact start-point. We let the follower start from “H” if the leader start from “A”, and let the follower start from “E” if the leader start from “G” accordingly. The users naturally hold their smartphones in hand during walking.

# 6.7.2 Performance Evaluation

# 6.7.2.1 Performance of Motion Event Detection

Turning Detection To detect turning events and capture the rotating angle, we employ both magnetometer and gyroscope, which reports the absolute angles and the angular velocity respectively [24, 29]. We acquire the ground truth turning angles from the floor plans. To extensively understand the turning angle estimation error and turning detection delay, we let users manually tag checkpoints at each turning’s starting and ending moments. With such results, the turning hints for a follower should be notified several seconds before the synchronized position of the turning starting events. As shown in Fig. 6.15, ppNav achieves great performance in turning angle estimation with a 90 percentile error of 18◦, which is sufficient enough for turning detection since a turning angle in real buildings is in general greater than 45◦. According to our experiments, turning events typically last for a duration of 2.75 s. Figure 6.16 illustrates the performance of detecting turning position (i.e., turning start points). As seen, ppNav identifies 90% of turning events in 0.5 s after turning starts, which means that the average spatial shift is 0.5 m, assuming a natural walking speed of 1 m/s.

Fig. 6.15 Turning angle accuracy   
![](images/38f8349994b2b468433629e5847160ce4a7b579ec3c6752abeb0a5fc934ef01c.jpg)



Fig. 6.16 Turning detection delay   
![](images/c8fa791858fde4693e59a47d8ae1bdc63d6610d5f2d1427dbc95c3f2fa3d3012.jpg)



Level-change Detection To detect level changes, i.e., going upstairs/downstairs events, we employ the barometer sensor to read the atmospheric pressure data. As shown in Fig. 6.17, the pressure values within the same level are relatively stable (with a maximum variation of 10 Pa as measured in our experiments), yet vary significantly over different floors (with a minimum different between adjacent floors of 44 Pa). Thus it is feasible to perform a threshold-based method to detect the level changes [11]. As a level-change event would typically last for a short period, we claim an event (i.e., the starting of a level change) when the pressure changes for over 12 Pa and confirm the event (i.e., the starting of a level change) when the pressure varies over 40 Pa. We collect 5 traces of going upstairs and downstairs in both experimental buildings, which contain 60 level-change events in total. In our experiments, we successfully detect all upstairs/downstairs events with a sliding window of around 8 s. The sliding window may cause certain delays, but does not affect the navigation performance since the level-change detection module only runs in reference trace generation part.

![](images/8a81c3464db7a25185d00e564b05e263dd4ac2a3c3997737530d21acccf8fe00.jpg)



Fig. 6.17 Level-change detection

Fig. 6.18 Trace alignment errors   
![](images/076a2a1be5bb3b3b23357e2c1e35ff5fa756b3a6d09606e9acafa1b9e186e234.jpg)



# 6.7.2.2 Performance of Trace Synchronization

As ordinary linear model (OLM) is sensitive to outliers caused by interferences such as fragile WiFi signals, we leverage a robust linear model (RLM) to mitigate the effects of noises, which uses iteratively reweighted least squares method [5] to find the maximum likelihood estimates.

To evaluate the performance of trace synchronization in term of physical space errors, we let leaders and followers manually mark a set of checkpoints along the paths as ground truth. Specifically, we set in total 41 and 20 checkpoints on each pathway in area I and area II, respectively. As shown in Fig. 6.18, RLM remarkably outperforms OLM, yielding an average alignment error of 0.9 m and a 90 percentile error of 1.6 m. For comparison, the average and 90 percentile errors of OLM are 1.7 and 4.3 m, respectively. Although RLM produces relatively higher computation costs, we need to perform regression only once and can reserve the regression coefficients for subsequent alignments during the same trace, since the speed differences and starting point offsets between the leader and follower are relatively stable for a specific pair of navigation trace and reference trace.

Fig. 6.19 Alignment error of turning points   
![](images/ea7df8851ade9146889e0020ee185254a613b66f8d7317f9ede94e639eb24041.jpg)



Fig. 6.20 Impacts of different markers   
![](images/ca1a4d611047eab9b0354f5031f2534a4b145a8e3924ed6e0da19369b3a782fc.jpg)



In addition, we particularly test errors of fingeram alignment for the turning points B,C,D,E in both area I and II, which are critical to navigation quality. As shown in Fig. 6.19, the errors are all under 2.5 m and decrease gradually with respect to increasing walking distances. This is because that longer trace yields more fingeram markers, which may lead to more robust trace alignment. The reason that the alignment errors of the turning points are larger than the average ones over the whole trace is that turning detection errors further cause location offsets, which are included in the alignment errors.

We further evaluate the effects of individual type of markers for trace alignment using the same trace data. Figure 6.20 shows the performance of fingeram alignment under three settings: radio markers only, visual markers only, and radio markers and visual markers. As seen, while either type of markers results in considerable accuracy, accounting for both markers yield the best performance. Specifically, the maximum error is limited by 2.1 m, while the average error is about 0.9 m.

Fig. 6.21 Deviation detection rate   
![](images/9b0f00b32b056b144925126a4205471dedc0f93ee40d57711ec91d1e52c3e810.jpg)



Fig. 6.22 Deviation detection delay   
![](images/dd46558fb238c65ea9e7cd2f021d0848f74bf54f6e657961022f317872cbbd4f.jpg)



# 6.7.2.3 Performance of Deviation Detection

Now we evaluate the delay of deviation detection. As deviations usually appear in intersections, we set purposed deviation point at a special intersection of each pathway (point D in both experimental area I and II) and let users mark on smartphone actively when passing the points for ground truth. Figure 6.21 depicts the precision and recall of deviation detection on 50 pairs of normal following traces and 50 pairs of deviated traces with different threshold values. The results show that any threshold within the range of [0.50, 0.64] yields considerable precision and recall on detection. Figure 6.22 plots the delay distributions of deviation detection using these threshold values. As seen, the delays in all cases within different thresholds are all less than 10 samples. Larger thresholds result in smaller delay in detection, yet yields more false alarms. In contrast, smaller threshold values achieves more robust deviation alert, yet lead to larger delay. In our experiments, we adopt an intermediate value of 0.6, which produces balance performance in detection rate (precision of 93% and recall of 92%) and detection delay (with an average delay of 5.6 samples). Considering a typical WiFi sampling frequency of 2 Hz and an average walking speed of 1.0 m/s, the results equivalently indicate that we could detect deviations within a maximum delay of 4.5 s in time and 4.5 m in physical distance.

# 6.7.2.4 Performance of Lock on Direction

To evaluate accuracy of path locking-on, we let followers rotate and move for locking on estimated direction with an interval of 3 m. The users spin around slowly $( 1 8 ^ { \circ } / \mathrm { s } )$ at each stop with smartphone in front of body. We first evaluate the accuracy of finding a locking-on points at different distances by calculating the location errors between the physical closest point on the reference path and the target points estimated at different distances, from 33 to 3 m. As shown in Fig. 6.23, the estimation errors decreased when the user gets closer to the path. Note that results in area II are in average better than those in area I, which is because narrower corridors in area II result in severer changes in amounts of common APs. Figure 6.24 shows the direction errors for the targeted points determined at a distance of 33 m. The average accuracy over all distances is about 29.5◦, which is sufficient for direction guiding in practice since two adjacent pathways are usually $9 0 ^ { \circ }$ connected. In addition, as can be seen, the direction errors first decrease and then increase again when the user iteratively spins and gets closer to the targeted points. The reason is that few common APs are available when the user is too far and no notable RSS difference would be observed if he is too close.

![](images/21c6b0b10fa4aa0b72723d129354bcfaac946c21a33ce9b09298a81dd1343000.jpg)



Fig. 6.23 Target point errors

![](images/d8693b9176561a72fa4eaf79fc70017c6f6e98a9791e4deb702c98f2c67c62eb.jpg)



Fig. 6.24 Target direction error

# 6.8 Discussion

Initial Locking-on If the user is too far away from any reference traces, ppNav fails to guide him to a close path since perhaps no common AP would be observed at the user’s location and any point on the reference trace. Nevertheless, if we gather sufficient leaders’ traces that cover a certain part of the building pathways, such case will be efficiently avoided.

Quality of Traces Although ppNav does not exert any constraints to participants during walking, arbitrary user behaviors, e.g., stop-and-go and scurrying from side to side, will impair the quality of the gathered trace information. Thus to record only the trace information along a path when the user is walking, we could employ inertial sensors (e.g., accelerometer) to detect the walking status of the user. In practice, when a user offers to provide hints for his friend, he will general try the best to provide good quality information. In case of sharing reference trace among strangers, quality control and privacy protection mechanisms need to be developed in the future.

Energy Consumption ppNav calls WiFi interface that generally consumes more energy than the low-power inertial sensors. Yet we argue the power consumption is affordable because the ppNav application only runs during navigation, which usually will not be too long. In addition, compared to computation-hungry visionbased approach [28], our design is actually significantly more energy efficient.

Evolving to Generic Navigation Services ppNav can be extended to progressively construct a generic navigation services by gathering sufficient reference traces and devising effective techniques to splice them to form an accessible roadmap. To achieve this, we need to design path planning algorithms to find the shortest path for friendly navigation [28].

# 6.9 Conclusion

In this chapter, we present ppNav, a Peer-to-Peer navigation system for smartphones, which enables efficient navigation without resorting to pre-deployed location service or the availability of indoor maps. ppNav employs a previous traveller to record the trace information along a path and share them with later users for navigation. We implement ppNav on commercial phones and validate its performance via real experiments. In addition to a fast-to-deploy navigation service, we envision and intend to extend ppNav as an alternative way to progressively crowdsource data for generic localization systems.

# References

1. Bahl, P., Padmanabhan, V.N.: Radar: an in-building RF-based user location and tracking system. In: IEEE INFOCOM (2000)   
2. Bay, H., Ess, A., Tuytelaars, T., Van Gool, L.: Speeded-up robust features (surf). Comput. Vis. Image Underst. 110(3), 346–359 (2008)   
3. Brajdic, A., Harle, R.: Walk detection and step counting on unconstrained smartphones. In: ACM UbiComp (2013)   
4. Chen, S., Li, M., Ren, K., Fu, X., Qiao, C.: Rise of the indoor crowd: reconstruction of building interior view via mobile crowdsourcing. In: ACM SenSys (2015)   
5. Holland, P.W., Welsch, R.E.: Robust regression using iteratively reweighted least-squares. Commun. Stat.-Theory Methods 6(9), 813–827 (1977)   
6. Jiang, Y., Xiang, Y., Pan, X., Li, K., Lv, Q., Dick, R.P., Shang, L., Hannigan, M.: Hallway based automatic indoor floorplan construction using room fingerprints. In: ACM UbiComp (2013)   
7. Li, F., Zhao, C., Ding, G., Gong, J., Liu, C., Zhao, F.: A reliable and accurate indoor localization method using phone inertial sensors. In: ACM UbiComp (2012)   
8. Liu, H., Gan, Y., Yang, J., Sidhom, S., Wang, Y., Chen, Y., Ye, F.: Push the limit of WiFi based localization for smartphones. In: ACM MobiCom (2012)   
9. Lowe, D.G.: Distinctive image features from scale-invariant keypoints. Int. J. Comput. Vis. 60(2), 91–110 (2004)   
10. Lymberopoulos, D., Liu, J., Yang, X., Choudhury, R.R., Handziski, V., Sen, S.: A realistic evaluation and comparison of indoor location technologies: experiences and lessons learned. In: ACM IPSN (2015)   
11. Muralidharan, K., Khan, A.J., Misra, A., Balan, R.K., Agarwal, S.: Barometric phone sensors: more hype than hope! In: ACM HotMobile (2014)   
12. Paek, J., Kim, K.H., Singh, J.P., Govindan, R.: Energy-efficient positioning for smartphones using cell-id sequence matching. In: ACM MobiSys (2011)   
13. Rai, A., Chintalapudi, K.K., Padmanabhan, V.N., Sen, R.: Zee: zero-effort crowdsourcing for indoor localization. In: ACM MobiCom (2012)   
14. Riehle, T.H., Anderson, S.M., Lichter, P.A., Giudice, N.A., Sheikh, S.I., Knuesel, R.J., Kollmann, D.T., Hedin, D.S.: Indoor magnetic navigation for the blind. In: IEEE EMBC (2012)   
15. Shen, G., Chen, Z., Zhang, P., Moscibroda, T., Zhang, Y.: Walkie-markie: indoor pathway mapping made easy. In: USENIX NSDI (2013)   
16. Shu, Y., Shin, K.G., He, T., Chen, J.: Last-mile navigation using smartphones. In: ACM MobiCom (2015)   
17. Tarzia, S.P., Dinda, P.A., Dick, R.P., Memik, G.: Indoor localization without infrastructure using the acoustic background spectrum. In: ACM MobiSys (2011)

18. Wang, J., Katabi, D.: Dude, where’s my card? RFID positioning that works with multipath and non-line of sight. In: ACM SIGCOMM (2013)   
19. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: ACM MobiSys (2012)   
20. Wu, C., Yang, Z., Liu, Y.: Smartphones based crowdsourcing for indoor localization. IEEE Trans. Mob. Comput. 14(2), 444–457 (2015)   
21. Wu, C., Yang, Z., Xiao, C., Yang, C., Liu, Y., Liu, M.: Static power of mobile devices: selfupdating radio maps for wireless indoor localization. In: IEEE INFOCOM (2015)   
22. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Enhancing WiFi-based localization with visual clues. In: ACM UbiComp (2015)   
23. Yang, D., Xue, G., Fang, X., Tang, J.: Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing. In: ACM MobiCom (2012)   
24. Yang, Z., Wu, C., Zhou, Z., Zhang, X., Wang, X., Liu, Y.: Mobility increases localizability: a survey on wireless indoor localization using inertial sensors. ACM Comput. Surv. 47(3), 54:1–54:34 (2015)   
25. Youssef, M., Agrawala, A.: Handling samples correlation in the horus system. In: IEEE INFOCOM (2004)   
26. Zhang, Z., Zhou, X., Zhang, W., Zhang, Y., Wang, G., Zhao, B.Y., Zheng, H.: I am the antenna: accurate outdoor AP location using smartphones. In: ACM MobiCom (2011)   
27. Zhang, X., Yang, Z., Sun, W., Liu, Y., Tang, S., Xing, K., Mao, X.: Incentives for mobile crowd sensing: a survey. IEEE Commun. Surv. Tutorials 18(1), 54–67 (2016)   
28. Zheng, Y., Shen, G., Li, L., Zhao, C., Li, M., Zhao, F.: Travi-Navi: self-deployable indoor navigation system. In: ACM MobiCom (2014)   
29. Zhou, P., Li, M., Shen, G.: Use it free: instantly knowing your phone attitude. In: ACM MobiCom (2014)

# Part IV

# Enhancing Accuracy: Making It Reliable

This part includes three chapters and focuses on techniques proposed to enhance the location accuracy of WiFi fingerprint-based localization. The first chapter presents methods for improving location accuracy from an internal perspective of fingerprint spatial features. The second chapter introduces an image-assisted WiFi fingerprinting approach. The last chapter in this part demonstrates several practical sources of location errors and introduces approaches to overcome them by incorporating external sensor hints.

TO RSS:

Sometimes it lasts in love but sometimes it hurts instead.

– Adele Laurie Blue Adkins

# Chapter 7 Exploiting Spatial Awareness via Fingerprint Spatial Gradient

![](images/21072fcdbdf84342719300b003c9a13ae844ee08a1b551f72ba55342cdc0acdc.jpg)

Abstract Current WiFi fingerprinting suffers from a pivotal problem of RSS fluctuations caused by unpredictable environmental dynamics. The RSS variations lead to severe spatial ambiguity and temporal instability in RSS fingerprinting, both impairing the location accuracy. In this chapter, we introduce fingerprint spatial gradient (FSG), a more stable and distinctive form than RSS fingerprints that overcomes such drawbacks. On this basis, we also present algorithms to construct FSG on top of a general RSS fingerprint database as well as effective FSG matching methods for location estimation. Unlike previous works, the resulting system, named ViVi, yields performance gain without the pains of introducing extra information or additional service restrictions or assuming impractical RSS models.

# 7.1 Introduction

Existing RSS fingerprint-based systems still suffer from several drawbacks, especially in the perspective of localization accuracy. Many applications demand for precise locations for refined advertisements, staff managements, exhibits monitoring, etc. Existing techniques, however, frequently yield large errors of up to 10 m in practice [18].

One major root cause of the locations errors in RSS fingerprinting is the RSS uncertainty of WiFi signals. RSS is known to be vulnerable to unpredictable environmental dynamics, especially in complex indoor environments where signal propagation suffers from severe multipath effects. In addition, automatic power adjustment strategy commonly implemented in modern APs, which monitors surrounding channel conditions and accordingly optimizes the transmitting power, further exaggerates the RSS temporal fluctuations. Device heterogeneity also results in diverse RSS measurements on different devices. Such RSS variations lead to two aspects of significant impacts of RSS fingerprints.

• Spatial ambiguity: fingerprints from different individual locations appear to be similar and thus indistinguishable from each other, giving rise to fingerprint mismatches and therefore inducing notable location errors.

• Temporal instability: fingerprint observations at a specific location would vary over time, making them deviate from and therefore fail to match the one collected during the training phase. Both issues would hurt the location accuracy and reside as two long-standing yet inevitable problems of RSS fingerprinting.

To overcome spatial ambiguity, additional information like digital floorplan [15], acoustic ranging [17], image matching [31] and inertial sensing [10, 25] have been recently incorporated with RSS fingerprinting for improved performance. While these approaches achieved better accuracy, they also degraded the delightful ubiquity and induce additional costs of RSS fingerprinting systems. For example, users need to intentionally take pictures [31] or cooperate with multiple peers [17] for localization. Considering temporal instability, the fingerprint database may need to be periodically calibrated, either reconstructed or updated to adapt to RSS variations [14, 30, 35]; Otherwise an initial fingerprint database may gradually deteriorate, leading to grossly inaccurate location estimations. Although crowdsourcing-based approaches reduce the efforts of fingerprint database construction [21] and adaptation [30], the adaptation costs are still non-negligible and they cannot adapt to transient RSS variations due to limited execution frequency. Since spatial ambiguity and temporal instability arise from the inherent properties of RSS fingerprint, physical layer Channel State Information (CSI) is recently exploited for precise localization [13, 22, 26]. The CSI is only available on specific WiFi devices with slight driver modifications and is not accessible on commodity smartphones. Hence as for practical location services, we believe new promising solutions to overcome these fundamental limitations lie in exploring new forms of fingerprints that is resistant to RSS uncertainty.

To better deal with RSS variations, we exploit the spatial feature of RSS fingerprints and propose Fingerprint Spatial Gradient (FSG), a new form of WiFi fingerprints that turns out to be more spatially distinctive and temporally stable. The key insight is that the spatial relationships of multiple RSS fingerprints from neighbouring locations would be more robust than individual RSS fingerprints from one single location. The FSG profile of one location depicts the differences between its representative RSS fingerprints and those of a set of nearby locations, which would hold specific patterns subjected to the underlying spatial constraints of fingerprints from adjacent locations. For example, considering a location with its surrounding neighbours on two sides along a corridor, the resulted FSG would in principle exhibit a “V”-like pattern, regardless of their own fingerprints. As a relative form, FSG can better mitigate the impacts of variations caused by absolute AP power changes and measurement device diversity. For example, if some AP adjusts its transmission power, the RSS values perceived at multiple neighbouring locations would be all affected, thus keeping the relative FSG less changed than the absolute RSS values (although still changed). As a result, the proposed FSG is more stable and identifiable than plain RSS fingerprints as it gracefully tolerates RSS variations caused by either environmental dynamics or device diversity.

Incorporating FSG in a practical localization system, we present ViVi to interpret the construction, representation, and comparison of FSG with a full functional implementation. We first formally specify FSG with experimental validation. Then FSG profiling is conducted on top of the general RSS fingerprint database. We design novel algorithms to generate optimum FSG of each location by selecting its best nearby fingerprints for FSG profiling. Finally, we propose proper FSG matching measures to compare two FSG profiles for effective location estimation. The design of ViVi follows the classical fingerprinting framework. Its inputs are no more than any traditional RSS fingerprint based systems. Thanks to the superior FSG, ViVi effectively remedies the spatial ambiguity and temporal instability of RSS fingerprints and achieve performance gain without the pains of introducing any extra information (e.g., inertial sensor hints [10], acoustic ranging [17]) or additional service restrictions (e.g., peer cooperation [17], taking images [31], monitoring trajectory [34]) or making strict assumptions on RSS models [29].

To validate the effectiveness and performance of ViVi, we conduct experiments in different buildings. The results demonstrate that ViVi achieves great performance, with a mean accuracy of 3.2 m and a 95th percentile accuracy of 6.4 m, outperforming the best among four comparative approaches by >28% and >19% and exceeding the worst comparative case by 38.5% and 23.8%, respectively. We envision FSG as an effective supplement and alternative to existing RSS fingerprints that sheds a light on practical WiFi-based localization in the future.

The rest of this chapter is organized as follows. We first review the start-ofthe-art in Sect. 7.2. Following an overview in Sect. 7.3, we define the concept of FSG in Sect. 7.4 and present the FSG specification, construction and comparison in Sect. 7.5. We implement and evaluate ViVi in Sect. 7.6. Finally we conclude in Sect. 7.7.

# 7.2 Related Works

Indoor localization has attracted vast research efforts during the past decades. We briefly review the most related latest works that aim at improving location accuracy.

Enhanced Matching Many efforts have been devoted to enable precise location estimation since WiFi-based indoor localization was conceptualized. Early efforts such as the well-known Horus system [36] employ advanced probabilistic methods to enhance the first fingerprinting system RADAR [2]. Various subsequent works tend to utilize complicated pattern matching techniques, investigate advanced similarity metrics, or seek for alternative expressive form of RSS fingerprints [3, 7, 8, 15, 19]. In particular, some recent innovations also explore the spatial/temporal properties of sequential RSSs for localization. Walkie-Markie [23] is the first to explore changing trends of sequential RSSs along pathways. Similar idea is implemented in [11]. Besides both of them are designed for floorplan construction, they are only applicable for mobile trajectories. In contrast, ViVi exploit optimum spatial gradient of fingerprints among surrounding locations, rather than mobile traces, for another goal of location accuracy. WarpMap [34] defines a new type of sequence-based radio map, which replaces traditional point-based radio map, to exploit the benefits of indoor path structure. It yields delightful results for only mobile traces in constrained environments with narrow pathways. INTRI [9] combines RSS contours with traditional fingerprinting for better accuracy. To deal with device heterogeneity, RSS-Ratio [4] is proposed to model the differential RSS of RSSs on two antennas on the receiver device. However, it relies on MIMO systems and is not suitable on commodity smartphones. GIFT [24] defines a binary valued metric for differential RSS, i.e., the difference of RSSs from two adjacent locations, as a replacement of absolute RSSs to deal with signal variations. Relying on differential RSS as query inputs, GIFT can only deal with mobile traces that contain sequential RSS measurements. Differently, ViVi explores the spatial gradient of selected multiple neighbouring fingerprints and is not tied to mobile trajectories.

Sensor-assisted Enhancement Some works resort to extra information sources beyond WiFi measurements to gain better accuracy. Ranging via acoustic signals [17] or WiFi Direct [12] among multiple devices are introduced to alleviate fingerprint ambiguity. Applying a similar idea, Argus [31] makes use of visual images to obtain extra position constraints for fingerprinting. Fusing inertial sensor data also attracts extensive studies. SurroundSense [1] integrates various sensor hints as multi-modal fingerprints for localization. More commonly, motion information is fused to provide relative locations to improve fingerprint-based localization [33]. [10] and [21] utilize geometric constraints imposed by both mobility information and digital floorplan. While remarkable accuracy is gained by these approaches, they generally rely on additional information from extra sensors, multiple devices or many participatory users. To the contrary, ViVi works merely on existing RSS measurements, achieving better accuracy without degrading the ubiquity in pervasive applications.

CSI-based Localization Recently, the Physical layer CSI has been exposed to upper layer for high accuracy location determination. SpotFi [13] achieves decimeter-level location accuracy by accurately computing the angle of arrival (AoA) of multipath components using CSI. Chronus [26] enables a single WiFi access point to localize clients to within tens of centimeters. PinLoc [22] employs CSI as fingerprints and yield remarkable accuracy, yet with significant training costs. FILA [29] extract the direct path components with CSI for accuracy ranging. CSI is also leveraged for passive localization and tracking [16, 28]. LiFS [28] passively localizes a user with multiple links by deliberating qualified subcarriers. Dynamic-Music [16] leverages the incoherence between reflecting signal and static signal to separate reflecting signal and estimate its AoA. Despite of high precision achieved, these works rely on specialized WiFi Network Interface Cards like Intel 5300 to extract CSI, which is not available on commodity smartphones.

To conclude, while most of existing approaches achieve remarkable accuracy for WiFi-based localization, they usually in the meantime introduce additional costs and constraints such as peer cooperation, mobility hints, digital floorplan information, and/or physical layer information, etc., which largely degrades the applicability and ubiquity in practice. In the contrary, our proposed approach is built upon a classical fingerprint-based framework and achieves performance gain without such pains at all, thus holding superior potentials for ubiquitous applications.

Fig. 7.1 Overview of ViVi flow   
![](images/86596300891c27f95dabd6bfbf7e882b52b158e8172ff9c873a8bcda6061ab83.jpg)



# 7.3 ViVi Design

As shown in Fig. 7.1, the design of ViVi follows a classical fingerprinting scheme (as described in Sect. 1.3.1) in consideration of compatibility with existing approaches. Its inputs are no more than any typical RSS fingerprint based localization systems. The core contributions lie in the introduction of an FSG profiling module along with an FSG comparison module.

Specifically, during the training phase, we additionally perform an FSG profiling procedure to build the FSG profiles for all sampling locations on top of the traditional fingerprint database. In the localization stage, when matching a user query $f _ { Q }$ against one candidate sampling location $\iota _ { C }$ , we construct a querying FSG profile $g _ { Q ( C ) }$ tailored to this candidate location based on information of its specific FSG $g _ { C }$ (i.e., the selected nearby locations and corresponding fingerprints). Then we compute the similarity of the two FSG profiles, denoted as $\Gamma ( g _ { Q ( C ) } , g _ { C } )$ , in the FSG comparison module. We employ FSG matching paradigm, instead of a model fitting approach, in purpose of avoiding fragile assumptions on a theoretical FSG model that is vulnerable to practical noises. Thus the final location estimate for a query $f _ { Q }$ is output by location estimation module as the candidate location that reports the minimal FSG dissimilarity (We denote gQ(C) as $g _ { Q }$ for sake of simplicity hereafter):

$$
l _ {Q} ^ {*} = \underset {l _ {C} \in L} {\arg \min} \Gamma (g _ {Q}, g _ {C}). \tag {7.1}
$$

ViVi is also implemented with an AP selection procedure to filter out low quality APs, especially those have extremely low mean RSSs or suffer from significantly high variances at the same location. To further reduce the computation costs, in practice we do not need to consider every sample location, but can efficiently skip those candidates that share too few common APs to reduce the search space.

The proposed ViVi is computation efficient. The only relatively complex FSG profiling procedure is conducted during the offline training phase. And once the FSG profile for each sample location is constructed, it does not need to be recalculated in the future, unless the fingerprint database is reconstructed or adapted. During the online localization, the only extra computation costs, compared to traditional RSS fingerprint-based approaches, lie in the FSG construction for each comparison, which can be fortunately computed in constant time, given that the FSG profile of the candidate location is available.

In the following, we first present the specification and advantages of the proposed FSG and then introduce how to profile and compare them.

# 7.4 Understanding Fingerprint Spatial Gradient

# 7.4.1 Limitations of Existing RSS Fingerprints

Despite of various innovations that have been proposed to ease the fingerprint construction [11, 21, 23, 27] or advance the fingerprint matching [9, 15, 17, 34] in purpose of promoting practical applications, existing RSS fingerprints suffer from several critical limitations due to especially the RSS variations.

RSS is known to be vulnerable to uncertain environmental dynamics and sensitive to hardware models [15, 30, 36]. As shown in Fig. 7.2, we collect about

![](images/71e5dd6d8cfdbc5c563f1e256dadbeda9e9430bdda450722a409bf756f641578.jpg)  
Fig. 7.2 RSS bias over time

1500 RSS samples of different APs and illustrate the RSS distributions of 5 APs with diverse average RSS values. Apparently, such variations cannot be trivially alleviated by cutting off the APs with low RSSs [3, 6] because, as shown in Fig. 7.2, stronger APs do not necessarily suffer smaller variations in RSS. One major cause of such RSS temporal fluctuations is the uncertain dynamics of indoor environments, including instantaneous interferences from human movements and door opening/closing and prolonged changes of temperature, humidity, as well as AP transmission power. Device heterogeneity is another well-known factor that leads to RSS bias [5]. Due to inherent hardware characteristics, different devices may encounter diverse RSSs of a specific AP under even identical wireless conditions. For example, we measure RSSs at 50 different locations using three devices of two different models (two Google Nexus 6p phones and a Nexus 7 phone) simultaneously and compare the differences in Fig. 7.3, which clearly demonstrates the RSS biases of different phones. As seen, even two smartphones of the same model (e.g., the results of two Google Nexus 6p phones) suffer from non-negligible RSS differences.

Evidently, RSS variations may induce two aspects of severe influences, i.e., spatial ambiguity and temporal instability, as also observed and recognized by previous works [5, 17, 36]. We explain the impacts of them concretely with real measurement data as follows.

1. Spatial ambiguity: One fingerprint might be similar to those from two or more (even quite distant) locations, rendering fingerprints over different locations become indistinguishable. Figure 7.4 shows the similarity matrix of fingerprints from 13 locations in corridors, where the three most similar fingerprints in each column with the one on the diagonal line are marked by “1” in black box, “2” in gray box and “3” in white box in sequence. As seen, the most similar fingerprints do not always come from the same nor even close locations.

![](images/789a2950e2f8d4a06f96c18831557a3de3142540e1618009a3006a474ed48324.jpg)



Fig. 7.3 RSS bias over different devices

![](images/44eb8c9dd00620dfc24a3ac321dbbb6fee024629720d7f001d681e8901fd7396.jpg)



Fig. 7.4 Fingerprint spatial ambiguity

![](images/164e99389155577e80c1329a0e0ac4f3dceb274a354227485f11e67e5d9803f5.jpg)



Fig. 7.5 Fingerprint temporal instability

Such phenomenon is recognized as spatial ambiguity that introduces significant fingerprint mismatches [17, 31].

2. Temporal instability: The fingerprint of a location observed at one instant does not match the initially collected training fingerprints from the same location. As shown in Fig. 7.5, although the fingerprints of some locations are relatively stable, the temporal correlations between a sequence of fingerprints successively measured at some other locations may notably decrease with respect to time. Consequently, fingerprints from the same or close locations cannot be successfully matched. Furthermore, severe temporal instability would degrade the performance of originally constructed fingerprint database especially over longterm running [30].

To conclude, both issues can lead to severe fingerprint mismatches and thus impair the localization accuracy and reside as two long-standing yet inevitable problems of conventional RSS fingerprints. The problem, however, is non-trivial and could not be fully addressed by simply applying a outlier detection techniques or increasing AP number. Different approaches have been proposed to deal with the two issues from various perspectives. Early efforts like Horus [36] employ advanced probabilistic models to tolerate RSS variations. Recently, stimulated by mobile phone development, various sensor information are incorporated to enable improved localization, including acoustic ranging [17, 20], image matching [31, 37], inertial sensors [21, 23, 27, 32, 34], etc. All these approaches, as far as we are aware of, are designed with RSS fingerprint as the basic form for location fingerprints. In contrast, we explore and exploit a new form for WiFi fingerprinting by leveraging the spatial gradient of RSS fingerprints. Hence our approach is orthogonal and compatible to existing systems. Several latest innovations [23, 24, 37] also leverage spatial features of RSS, yet in a different manner, as detailed in the next section.

# 7.4.2 Fingerprint Spatial Gradient

Instead of using the RSS fingerprints, we propose FSG to exploit the spatial feature of fingerprints from multiple adjacent locations. The key insight is that certain spatial relationship among multiple adjacent locations’ fingerprints keeps relatively stable against signal variations, although their individual fingerprint might be altered. Specifically, fingerprints collected from closer locations are generally more similar to each other, while distant locations enjoy larger fingerprint differences. Note that we do not assume that every pair of neighbouring fingerprints are similar. Indeed there would be some locations that occasionally hold widely different fingerprints with their neighbours (as shown in Fig. 7.4). Nevertheless, it is promisingly feasible to seek for a set of neighbouring locations among all that hold reasonable and stable fingerprint similarity relationships, even if some of them might suffer from spatial ambiguity. For a specific location, such spatial trend of fingerprint similarity is expected to be stabler than an individual fingerprint of its own. Benefiting multiple fingerprints across different spatial locations, the resulted profiles also would be more distinguishable than a single RSS fingerprint. Hence we explore and exploit such fingerprint spatial gradient as a more favorable feature, compared with the widely adopted original RSS fingerprints, for location mapping.

# 7.4.2.1 FSG Specification

As shown in Fig. 7.6, for a specific location, the FSG profile describes the fingerprint similarity trend between the fingerprint of that location and several of its neighbouring locations. Specifically, the FSG profile for a location $\mathbf { \xi } _ { l _ { i } }$ is defined as

$$
g _ {i} = \{<   d (\boldsymbol {l} _ {i}, \boldsymbol {l} _ {j}), \phi (\boldsymbol {f} _ {i}, \boldsymbol {f} _ {j}) >, i - r \leq j \leq i + r \}, \tag {7.2}
$$

![](images/2d7f49eca0f4b4979cda22fd738cae626181c8fde7762898213e961a48a7dee6.jpg)



Fig. 7.6 Illustration of FSG profile (of the central green sample location)

where $\phi ( f _ { i } , f _ { j } )$ is the similarity of $f _ { i }$ and $f _ { j }$ and each $f _ { j }$ denotes the RSS fingerprint of one of the neighbouring locations $\dot { l } _ { j } . \ d ( l _ { i } , l _ { j } )$ denotes the physical distance between $\mathbf { \xi } _ { l _ { i } }$ and $l _ { j }$ . Locations $\boldsymbol { l } _ { i - 1 }$ to $\mathbf { } l _ { i - r }$ and $\displaystyle l _ { i + 1 }$ to $\displaystyle { l _ { i + r } }$ should appear in the surrounding subspace of $\mathbf { \xi } _ { l _ { i } }$ respectively and are ordered in physical distance to the current location $\mathbf { \xi } _ { l _ { i } }$ . Theoretically the FSG profile exhibits $\mathbf { a } \ ^ { 6 6 } \mathbf { V } ^ { 5 }$ -like shape as the fingerprint similarity would first decrease to zero (at the current location) and then increase, corresponding to the ordered physical distances to the current location, which will be confirmed by the following experimental observations.

Here various similarity measures can be leveraged as the fingerprint similarity $\phi ,$ , such as Euclidean distance [2] and its temporal weighted version [7], probabilistic likelihood [36], and Kullback-Leibler Divergence [19], etc. For simplicity, we first adopt the most common p-norm distance with $p = 2$ as follows and then examine the performance of different metrics in Sect. 7.6.

$$
\phi (\boldsymbol {f} _ {i}, \boldsymbol {f} _ {j}) = (\sum_ {k = 1} ^ {m} | f _ {i k} - f _ {j k} | ^ {p}) ^ {1 / p}. \tag {7.3}
$$

We preliminarily analyze the FSG feature through real-world experimental measurements based on a sample fingerprint database of a campus building by site survey. We first plot the FSG profile of randomly selected locations in Fig. 7.7a, which confirm specific spatial trends of FSG profiles at different locations. Figure 7.7b further demonstrates the FSG profiles when using different number of APs in the RSS fingerprints.

Note we illustrate the “V”-like shape of FSG profiles only for intuitive conceptualization and easy understanding here. As would be explained in Sect. 7.5, our ViVi design will not require a theoretical $\mathbf { \Delta ^ { 6 6 } V } ^ { , 5 }$ shapes (nor any other specific shapes) of FSG profiles for localization because any assumed shapes might be distorted and no longer hold as expected in practice. Instead, our design seeks for the most stable FSG profile as fingerprints.

![](images/550b7dade01ee2c26b65ea6254ab2fce6f77fc368f593370e9a2d280e2fafadb.jpg)



(a)

![](images/983052a09789891490c6ac24b0088b7dd2536883a9777a690c5a07b4e2f22396.jpg)



(b)   
Fig. 7.7 FSG profiles by experimental measurements. (a) Different locations. (b) Different AP number

# 7.4.2.2 FSG Advantages

The proposed FSG appears to be more temporally stable and spatially distinctive for localization than existing RSS fingerprints.

On one hand, FSG exploits the spatial constraints among multiple fingerprints from a set of elected multiple nearby locations and thus turns out to be more stable over time than RSS fingerprints that consist of absolute RSS values observed at a single location. The rationale is that certain spatial neighbouring relationships would be more stable than individual RSS fingerprints [9, 30].

On the other hand, FSG also serves more distinctively in space, although the FSG profiles themselves of different reference locations actually appear to be pretty similar (as the “V”-like patterns shown in Fig. 7.7a). The trick lies in that we generate the FSG of a query according to the profiled neighbouring locations of a reference location when evaluating its probability as the targeted location for this query. In other words, the querying FSG profiles are also constructed based upon the elected neighbouring fingerprints already in the fingerprint database. In addition, a query does not hold a fixed FSG profile, which inversely adapt to each different reference location when matching against it. As a result, if the query fingerprint indeed comes from the same location with the reference one, the generated querying FSG profile tend to be similar with the reference one. Otherwise, if the fingerprint is from a different location, the resulted FSG profile will exhibit significantly different spatial pattern. This is because the query fingerprint does not necessarily hold similar gradients with the reference location’s neighouring fingerprints even if it itself is similar to the reference fingerprint (Two fingerprints that are both similar to a third one are not necessarily similar to each other).

Some previous works have leveraged related features of RSS spatial distribution of individual APs [11, 23, 30]. For example, GIFT [24] employs a binary differential RSS value of two adjacent locations as a replacement of the absolute RSSs. Walkie-Markie [23] and Travi-Navi [37] both observe that the spatial-temporal RSS sequence of a certain AP along a path will exhibit a specific trend from increasing to decreasing. While these works pioneer to leverage spatial features, most of them focus on different targets such as floorplan generation [23], self-navigation [37], and radio map adaptation [30]. Furthermore, all of existing approaches rely on mobile trajectories to extract path-centered spatial features of RSS, which usually requires dead-reckoned traces from users and is not feasible for the widely adopted point-based fingerprinting systems. In this work, we investigate the spatial gradient of nearby locations from a perspective of entire fingerprint and devise a more stable and distinguishable form of WiFi fingerprints. Our design exploits referencepoint-centered spatial features (both the querying and reference FSG profiles are generated based on the nearby fingerprints of a referent point, see Sect. 7.5), which is fully compatible to existing fingerprint-based systems and does not resort to mobile trajectories for either fingerprint database construction or location query.

The above superior properties lay solid foundation for location distinction. In the following, we design and implement a full functional localization system based on the proposed FSG. Unless otherwise mentioned, we still refer fingerprints to traditional RSS fingerprint in the following.

# 7.5 Exploiting Fingerprint Spatial Gradient

# 7.5.1 Profiling Fingerprint Spatial Gradient

FSG profile for each reference location is built upon the original RSS radio map. There are generally multiple neighboring fingerprints for each location. Thus in this section, we first discuss how to form a good FSG profile for each reference location, e.g., how to find a representative set of neighbouring locations and how to appropriately order them. Then we present how to profile a query fingerprint based on a reference location’s FSG.

# 7.5.1.1 Profiling a Reference Location

For a targeted location $\mathbf { \xi } _ { l _ { i } }$ with a fingerprint $f _ { i }$ , we first form a neighbouring set containing all adjacent locations whose distances to the current location are no more than r sample points. Then we calculate the RSS fingerprint similarity between $\mathbf { } l _ { i }$ and locations in the neighbouring set. By default, we adopt the most common Euclidean distance to measure fingerprint similarity. Nevertheless, various fingerprint similarity metrics such as other p-norm distances and Kullback-Leibler divergence can be leveraged, which will be implemented and evaluated in the experiments in Sect. 7.6. Afterwards, we propose different methods to generate an appropriate FSG profile for the current location $\mathbf { \xi } _ { l _ { i } } \mathbf { . }$ : two heuristics based on spatial gradients and one considering temporal variances of spatial gradients.

![](images/3e91588398d5083d4a3e6f566cc52324449a7d987552151b0b4cbfeeab656d7e.jpg)  
Fig. 7.8 Illustration of FSG profiling by (a) minimizing local gradient and (b) maximizing global gradient. Circles with darker color indicate larger fingerprint distances (gradient) to the targeted point marked by empty circles

(1) Minimizing Local Gradient As shown in Fig. 7.8a, the basic idea of minimizing local gradient (MinLG) is to select the next neighbouring location in a greedy way. Starting from $\mathbf { \xi } _ { l _ { i } }$ , we choose the top two adjacent locations that have the smallest fingerprint distances as the two expanding direction. The rationale is that two adjacent locations are more common to share more similar fingerprints. For each following step, we select the location (among all unselected adjacent locations within one-sample-point distance with the current selected location) that yields the shortest fingerprint distance with the current location. We repeat doing this until we gain r locations on each direction. After that, we order the respective set of r neighbouring locations on each direction by physical distance to $\mathbf { \xi } _ { l _ { i } }$ and, together with the fingerprint distances, forming an FSG profile of $\mathbf { \xi } _ { l _ { i } }$ . The complexity of profiling one sample location by MinLG is $O ( 6 r + 4 )$ since fingerprint gradients of three additional neighbours need to be calculated for each of the 2r selected candidates.   
(2) Maximizing Global Gradient An alternative method opts for the top 2r neighbours that share the largest fingerprint distances with the targeted location $\mathbf { \xi } _ { l _ { i } }$ to maximize the global gradient (MaxGG) of the resulted FSG.

To achieve this, we first calculate the fingerprint similarity between $f _ { i }$ and the representative fingerprint of each neighbouring location. As shown in Fig. 7.8b, we increase the distance constraints d to the target point step by step and select two most dissimilar fingerprints for each step. By doing this, we obtain $2 r$ neighbouring points when the distance increases to r sample points. To gain identical number of points on either size of the current locations, we search for a division that passes through the current location in the physical space and cuts the 2r locations into two equal parts. Then we connect the locations in each part in the order of physical distances to the current location, resulting in a legitimate FSG profile. The complexity of profiling one sample location using this MaxGG algorithm is $O ( N _ { r } )$ where $N _ { r }$ is the number of neighbouring sampling locations within the range r of $\mathbf { \xi } _ { l _ { i } }$ . Considering the squared sample grid as illustrated in Fig. 7.8b, the complexity becomes $O ( \frac { 4 } { 3 } ( 4 ^ { r } - 1 ) )$ .

(3) Optimizing Spatial Stability The above two heuristic approaches are efficient but, however, does not necessarily guarantee the best profiles. Recalling that the key insight of FSG is to exploit spatial fingerprint relationships that are stable over time, we propose another algorithm for FSG profiling by choosing a set of neighbouring fingerprints that optimize the spatial stability (OptSS) in terms of fingerprint similarity.

In general, when we mention the (representative) fingerprint of one location, we commonly refer to the averaged vector of multiple raw fingerprints from that location [17, 31, 32, 36]. Different from the above two approaches, we leverage every single fingerprint record here, instead of the averaged one, to output an optimal set of neighbouring fingerprints. We first compute the fingerprint distance between the representative fingerprint $f _ { i }$ of target location $\mathbf { \xi } _ { l _ { i } }$ and every raw fingerprint record of each neighbouring candidate. Then we derive the variances of the resulted fingerprint distances for each neighbour and form a variance matrix. Take Fig. 7.8b as a substitutive illustration and imagine the color of each location indicates the variance of corresponding fingerprint distances. We select two neighbouring locations that have the smallest variances for each step of physical distance d and obtain $2 r$ neighbours in total. After that we generate the FSG of current location $\mathbf { \xi } _ { l _ { i } }$ by dividing the selected neighbours into two parts with identical sizes and connecting them in order of physical distances to $\mathbf { \xi } _ { l _ { i } }$ . By doing this, the acquired FSG is optimized in spatial stability since we always select the spatial neighbours that output the most stable relationships (i.e., minimized variances in fingerprint distances). The complexity of profiling each sample location is $O ( N _ { r } ( m { + } 1 ) )$ , where $N _ { r }$ is the number of neighbouring sampling locations within the range r and m is the number of raw fingerprint records of each sample location. Taking the grid topology in Fig. 7.8b as example, the complexity is $O ( \frac 4 3 ( 4 ^ { r } - 1 ) ( m + 1 ) )$ . Considering that r is generally a small constant number $( \mathrm { e . g . , < 5 ) }$ , the complexity is then linear to m.

# 7.5.1.2 Profiling a Query Fingerprint

The above FSG profiling task is completed in the offline training phase, based upon an ordinary radio map. In the online localization phase, the FSG profile of a query fingerprint is not fixed and depends on the specific targeted reference point. When comparing a query fingerprint $f _ { Q }$ from an unknown location $\iota _ { Q }$ against a specific candidate reference location $\iota _ { C }$ , we construct a FSG profile for the query using the selected neighbours in the FSG profile of $\iota _ { C }$ . For example, if the FSG profile of the candidate $\iota _ { C }$ is $g _ { C } = \{ < d ( l _ { C } , l _ { j } ) , \phi ( f _ { C } , f _ { j } ) > , j \in N ( l _ { C } ) \}$ , then the FSG for the query turns out to be $g _ { Q } = \{ < d ( l _ { C } , l _ { j } ) , \dot { \phi } ( f _ { Q } , f _ { j } ) > , j \in N ( l _ { C } ) \}$ . Note that beside the neighbouring point set $N ( l _ { C } )$ , we also substitute the candidate location coordinates into the query location for FSG profiling. Provided the reference FSG profile, each query FSG profile can be generated in constant time without the need of searching for spatial neighbours.

![](images/bff6f70fbf3252aaabe54d2d39528968b8193e7da8f1862a6e8ecf2c5294f7d0.jpg)



(a)

![](images/54c998f8a1f843e14859f97eb50b657fe940a264ab7a5e01feeeff599e690932.jpg)



![](images/ad94ff91f1cfd9c3e5ae750b5aa8ef38e4a7dd5873ca9a382e165ab51e52cc04.jpg)



![](images/cdfa7224bc24f42e437ee983e5f9aaa59f4fbfd9c99ececa952326ee4b2d87c1.jpg)



Fig. 7.9 FSG profile comparison: (a) reference FSG profiling by minimizing local gradient. FSG comparison against queries from (b) the same location, (c) 1-m neighbour locations, (d) 2-m neighbour locations

The key advantage by doing so is that when the query fingerprint comes from the same location with the reference one, the generated FSG profiles tend to be similar. In contrast, if the fingerprint is from a different location, the FSG profiles will be significantly different since the constructed query FSG profile does not exhibit similar spatial patterns. Take Fig. 7.9 as an example where r 4 and consider the FSG of the location marked by a red circle in Fig. 7.9a. As in Fig. 7.9b, when comparing with different queries collected from the same locations, the generated querying FSG profiles appear to be consistently similar to the reference one. In contrast, as indicated by Fig. 7.9c, different patterns appear in the FSG profiles of queries from neighbouring locations only 1-m away. Such chaotic differences are further significantly aggravated when matching queries from locations that are 2-m away, as shown in Fig. 7.9d.

In addition, the FSG construction strategy also enables us to deal with any single querying fingerprint. This advances many previous approaches that usually require continuous observations along a moving trace with well-monitored inertial sensor hints [23, 24, 34] or resort to information from multiple participatory users [17]. Given the querying and training FSG profiles available, we next discuss how to compare them and further derive the best-matched location candidate.

# 7.5.2 Comparing Fingerprint Spatial Gradient

Fingerprint-based location determination problem is in principle a pattern matching problem, regardless of the specific feature used. Although the FSG normally exhibits specific “V”-like pattern, we employ a pattern matching approach for location estimation, instead of building and fitting a theoretical pattern model, because the “V”-like pattern would be distorted in practice. By FSG matching, we avoid making fragile assumptions on the spatial gradient distribution and gain robustness to uncertain disturbances in FSG profiling in practice.

A FSG profile can be viewed as a point set in the space when treating the physical distance as X-coordinate and the fingerprint distance as Y-coordinate for each neighbour. Let $f _ { Q }$ be the query RSS fingerprint, and let $\iota _ { C }$ be the current candidate location. As mentioned above, we can obtain the query pattern (FSG profile) as $g _ { Q } = \{ < d _ { Q } , \phi _ { Q } > \}$ and the targeted pattern as $g _ { C } = \{ < d _ { C } , \phi _ { C } > \}$ , where both patterns are $2 r + 1$ point sets. Comparison of two FSG profiles can thus be solved by shape matching techniques, of which an effective similarity measure acts as the core. While Euclidean distance is widely used as a similarity metric for traditional RSS fingerprints, we need to develop effective similarity measure for the proposed FSG profile. Our goal is to explore proper similarity measures to recognize the FSG profiles from the same locations while differentiating those of different locations.

# 7.5.2.1 Cosine Similarity

As noticed, the X-coordinates of each pair of $g _ { Q }$ and $g _ { C }$ are the same. Thus we can omit the X-coordinates and apply the well-known cosine similarity on only the $\phi$ parts. Let Γ be the similarity of two FSG profiles, we have

$$
\Gamma (g _ {Q}, g _ {C}) = \frac {\boldsymbol {\phi} _ {Q} \cdot \boldsymbol {\phi} _ {C}}{| | \boldsymbol {\phi} _ {Q} | | | | \boldsymbol {\phi} _ {C} | |}. \tag {7.4}
$$

# 7.5.2.2 Turning Function Distance

The turning function, or cumulative angle function, $\Theta _ { s } ( P )$ of a polyline (or polygon) P depicts the counter-clockwise angle between tangent of each segment and the X-axis as a function the edge length $s . \theta _ { s } ( P )$ starts from a certain point on P and tracks each turning angle that appears. The turning function increases with left hand turns and decreases with clockwise turns.

An FSG profile can be translated into a polyline by connecting each two adjacent points. Thus we can derive the turning function of $g _ { Q }$ and $g _ { C }$ as $\Theta _ { s } ( g _ { Q } )$ and $\Theta _ { s } ( g _ { C } )$ , respectively. Applying $L _ { p }$ Distance to the two turning functions, a dissimilarity measure on $g _ { Q }$ and $g _ { C }$ is given as:

$$
\Gamma (g _ {Q}, g _ {C}) = \left(\int | \Theta_ {s} (g _ {Q}) - \Theta_ {s} (g _ {C}) | ^ {p} d s\right) ^ {1 / p}. \tag {7.5}
$$

# 7.5.2.3 Discrete Fréchet Distance

The Fréchet distance is a popular measure between parametric curves that takes into account the location and ordering of the points. It is intuitively explained by a common analogy of “dog-walking distance”: A person and a dog connected by a leash are walking along two curves (without backtracking) respectively. The shortest length of the leash that is required for traversing the two curves is the Fréchet distance.

The Fréchet distance usually appears in its continuous form for parametric curves. Since we have identical constant points in both FSG profiles $g _ { Q }$ and gC, the discrete version is preferred, which can be solved more efficiently in polynomial time by using dynamic programming:

$$
\Gamma (g _ {Q}, g _ {C}) = \min _ {\delta , \beta : [ 1: n ] \rightarrow [ 1: n ]} \max _ {s \in [ 1: n ]} \left\{d \Big (g _ {Q} (\delta (s)), g _ {C} (\beta (s)) \Big) \right\}, \tag {7.6}
$$

where $d { \big ( } g _ { Q } ( \delta ( s ) ) , g _ { C } ( \beta ( s ) ) { \big ) }$ denotes the Euclidean distance of the two points, δ and $\beta$ range over all discrete non-decreasing surjections of the form $[ 1 : n ] \to$ $[ 1 : n ]$ .

Different from traditional RSS fingerprint, the proposed FSG is a relative spatial feature. Thus pattern matching upon FSG profiles appears to be less susceptible to signal variations caused by temporal changes or device heterogeneity, no matter what similarity measure mentioned above is used.

# 7.6 Implementations and Evaluation

We prototype ViVi on the popular Android OS and conduct experiments using different devices over various scenarios. In this section, we first introduce the experimental settings and then present the detailed evaluation.

Fig. 7.10 Experimental areas in classroom building   
![](images/f745e1b549feefcdb3757a859774aec9484a31c4ff87fbec3f75c3b441f3768b.jpg)



Table 7.1 Data collection in different scenarios 

<table><tr><td>#</td><td>Building type (Areas)</td><td>Size ( $m^{2}$ )</td><td>Density</td><td>Devices</td><td>#Samples</td><td>#Loc</td><td>Duration</td></tr><tr><td>1</td><td>Academic (Public areas)</td><td>600</td><td> $1 \times 1$ m</td><td>Nexus 5/7, two Nexus 6p</td><td>23.4 K</td><td>93</td><td>10 h in 1 day</td></tr><tr><td>2</td><td>Office (Whole floor)</td><td>1,500</td><td> $2 \times 2$ m</td><td>Two Nexus S</td><td>27.2 K</td><td>293</td><td>24 h in 2 days</td></tr><tr><td>3</td><td>Classroom (Public areas)</td><td>3,360</td><td> $1.2 \times 1.2$ m</td><td>Nexus 7, two Nexus 6p</td><td>87.0 K</td><td>460</td><td>12 h in 1 day</td></tr></table>

# 7.6.1 Experimental Methodology

# 7.6.1.1 Experimental Scenarios

We carry out experiments in three buildings with different floor layouts and diverse wireless environments, as shown in Fig. 3.2 (Office building), Fig. 5.7 (Academic building), and Fig. 7.10 (Classroom building), respectively. Although the three buildings are similar on building structure, the user behavior patterns are pretty different. For example, there are many people in the office building in daytime, which will be almost empty in the night. The classroom building are crowded or empty to different extents depending on the course schedule. While there are a reasonable number of users in the academic building most of the time.

The data collection details are summarized in Table 7.1. When collecting fingerprints for training, we employ a typical sampling frequency of around 1Hz.

We employ six phones of four different models that are manufactured by different companies for data collection, including two Samsung Nexus S, one LG Nexus 5, two HUAWEI Nexus 6p and one ASUS Nexus 7 pad, which are equipped with different types of WiFi chips.

# 7.6.1.2 Comparative Methods

To extensively evaluate the performance of ViVi, we additionally implement four different start-of-the-art approaches for comparison, which have been proposed to enhance the primary RSS fingerprinting.

1. Horus (Probabilistic Method) [36] A classical probabilistic algorithm that computes the probability distribution of the RSS values at each location as the fingerprint metric, and retrieves the targets of the maximum likelihood as estimated locations.   
2. TW-KNN (Temporally Weighted KNN) [7] It forms fingerprints with temporally weighted RSS by applying an iterative recursive weighted average filter on training RSS samples.   
3. KLDiv (Kullback-Leibler Divergence) [19] A typical KNN-based localization scheme built upon RSS fingerprints, but using the Kullback-Leibler divergence of two signal distributions as the similarity measure.   
4. GIFT [24] A metric of binary differential value between RSSs observed at two adjacent locations is exploited as replacements to the original RSS values as fingerprints. As GIFT is designed for mobile traces, we combine queries from two adjacent locations as one for GIFT.

We mainly aim to validate the advantages of the proposed FSG over RSS fingerprints. In other words, we focus on the relative accuracy improvement rather than the absolute accuracy achieved by ViVi. Hence we mainly implement the core fingerprinting and matching components of the above systems. For example, we omit the clustering step in Horus [36] and the Particle Filter enhancement of GIFT [24] since similar components could also be incorporated in ViVi. By default, we conduct identical preprocessing (e.g., AP selection) for all methods and implement all of them with KNN with k 3. We mainly focus on the average location errors and the 95th percentile errors as performance metrics for evaluation.

# 7.6.2 Performance Evaluation

We first explore the best FSG profiling approach and the best FSG similarity metric. We integrate the results of different phones from all experimental areas for evaluation. We first use Euclidean distance as the RSS fingerprint similarity for FSG generation and will later improve with different metrics for better accuracy. As shown in Fig. 7.11a, OptSS achieves the best accuracy among the three profiling methods, yielding an average accuracy of 3.5 m and the maximum error of 6.7 m. Using OptSS as the profiling method, we compare the performance with different similarity measures for FSG comparison. As depicted in Fig. 7.11b, Cosine Similarity (CS) produces slight gains in both average accuracy and 95th percentile accuracy than the other two metrics, i.e., turning function distance (TF) and walking dog distance (WD). To conclude, the combination of OptSS and CS yields the best performance with mean accuracy of 3.6 m and 95th percentile error of 6.7 m, when using Euclidean distance for FSG generation. In the following, we use this setting by default, together with r 4 and AP number of 15.

![](images/4b5c80950d17e45fdf5381629c486d17a820649314311abc7c6fb4a5a9997dbd.jpg)



(a)

![](images/6ca5da7ec1b5b0a7682fd60b86ac4ba9eb39fb3e2445a059545b3b9237032284.jpg)



![](images/61ab056eb4738642c7333979ddc42c8e87e96bff57f3e887452db7a7bb01c4b4.jpg)



(c)

![](images/bee7abdb7fad7255eb4c818a6181aea557ad676e5df562a5c5ba783895595d8a.jpg)



(d)   
Fig. 7.11 Overall performance. (a) Three profiling methods. (b) Three FSG similarity. (c) Different areas. (d) Performance comparison

# 7.6.2.1 Performance in Different Areas

We evaluate the performance in three different experimental floors as illustrated in Table 7.1, including a small academic building, a middle office building and a large classroom building with middle. Figure 7.11c shows the performance of ViVi in different areas. As seen, ViVi yields an average accuracy of 3.3 m in the academic building, 4.3 m in the office building and 3.8 m in the classroom building. The corresponding 95th percentile location errors in these three buildings are 6.5, 7.7, and 7.1 m respectively. The results also demonstrate that denser sample locations in smaller areas yield better accuracy, which confirms with various previous works [21, 32].

![](images/a399bddf091948e9fb48a0953d0cfba8c057355b22ae1d9ba4238bd5794fde3c.jpg)



(a)

![](images/708ad5d9f8e3696762be032e42a60fd2b7f4805c8d8525500a7a4f36aeb9690d.jpg)



![](images/5e74bd8720d80245dd9dc2fec4003418abd33888b8dd5aae8f9883eedbd476b6.jpg)



(c)

![](images/59ae46a341cf26a03412582aeefda29b2270de5da3c0e89ee018f05fd2b5e2b2.jpg)



(d)

![](images/fab74410a72486eb6868e06d3dfa106b700b5bbdead37390d9808d692a26d812.jpg)



(e)

![](images/84f25b653eabbdae2367e74296bb6aeea2d271dd818415c20994c801d36528e1.jpg)



(f)   
Fig. 7.12 Parameter study. (a) Impacts of devices. (b) Impacts of devices. (c) Impacts of RFS measures. (d) Impacts of r. (e) Impacts of AP number. (f) Impacts of k

# 7.6.2.2 Performance Comparison

Figure 7.11d depicts the performance of the proposed ViVi as well as the four comparative approaches. As shown, ViVi achieves the best performance among all comparative systems. The average accuracy outperforms Horus by 18.2%, GIFT by about 21.7% and exceeds TW-KNN by 25.0% and KLDiv both by 30.8%. The 95th percentile accuracy outperforms the four comparative approaches by 17.3%, 15.2%, 16.3%, and 20.2%, respectively. Furthermore, as shown in Fig. 7.12c, when employing the TW RSS as the RSS fingerprint similarity measures during FSG generation, the performance gains in average accuracy would increase to 28.6%, 30.4%, 33.3%, and 38.5% respectively and the improvements in 95th percentile errors become 21.0%, 19.0%, 20, and 23.8% respectively, achieving a mean accuracy of 3.2 m and 95th percentile accuracy of 6.4 m. The encouraging performance gains are achieved without introducing any extra costs (except for slightly increased computation overhead). Further improvements could be obtained by incorporating more enhanced techniques like Particle Filter, which we leave as our future work.

# 7.6.2.3 Impacts of Device Diversity

We evaluate the robustness of ViVi by involving diverse devices in training and querying stages. Specifically, we consider the following cases: (1) data from an identical phone for both training and testing; (2) data from one phone for training and data from another phone of the same model for testing; (3) data from phones of one model for training and data from phones of another different model for querying. As shown in Fig. 7.12a, device diversity indeed degrades the localization performance. The average errors increase from 3.7 m (using the same phone) to 4.2 m (using the same model phones) to 4.7 m (using different model phones). We also test the performance of comparative methods using different devices (Nexus 6p vs Nexus 7). As shown in Fig. 7.12b, compared with ViVi, all comparative methods based on RSS fingerprints suffer more significantly from device heterogeneity. The mean accuracy of ViVi exceeds Horus by 17.5%, GIFT by 25.4%, and TW-KNN by 30.9%. The results demonstrate that the proposed FSG tolerate device diversity much better than RSS fingerprints.

# 7.6.2.4 Impacts of RSS Fingerprint Similarity (RFS) Measures

As we have mentioned in Sect. 7.5, different similarity measures for RSS fingerprint comparison can be incorporated in Eq. 7.3 for FSG generation. Thus we employ two additional measures that have been adopted in previous works, i.e., probabilistic likelihood (Horus) as in Horus [36] and temporally weighted Euclidean distance (TW) as in TW-KNN [7]. Figure 7.12c illustrates the similar performance achieved by the above similarity measures. The results demonstrate that, although TW yields better accuracy than the other metrics, ViVi does not rely on complicated RFS measures and yields robust accuracy regarding different measures.

# 7.6.2.5 Impacts of Neighbour Number

In the above, we use 8 neighbours (r 4) to generate FSG profiles. Now we dig into the performance of ViVi when using different numbers of neighbour fingerprints with r ranging from 2 to 5. As shown in Fig. 7.12d, the location errors decrease from 5.1 to 3.6 m when r increases from 2 to 4 and achieves the best case at 4. The results indicate that more neighbouring locations hold more stable spatial constraints, which could not be depicted well by too few neighbouring fingerprints. However, when r further grows to 5, the performance slightly degrades to mean error of 4.1 m. This is because, as r increases, fingerprints from very distant locations will also be involved. These distant fingerprints do not contribute to, but in the contrast will impair, the stableness of the generated FSG.

# 7.6.2.6 Impacts of AP Number

We examine the impacts of AP number involved in the original RSS fingerprints. We evaluated the performance using 5, 15, 20, and all APs without filtering, respectively. As shown in Fig. 7.12e, ViVi achieves the best performance when using 15 APs. The performance degrades with both more or less APs (e.g., the mean errors with 5 and 20 APs are 5.0 and 4.1 m, larger than that with 15 APs by more than 30% and 15% respectively). The reasons are that using too few APs may loss the spatial distinctiveness of fingerprints while using too many of them will as well involve in those low quality APs. Although we filter out some apparently bad APs by signal strengths, the selected APs may not be all superior for location distinction.

# 7.6.2.7 Impacts of k

We choose $k = 3$ by default for KNN. Figure 7.12f portrays the performance when using different values for k. As seen, the best results are achieved with $k = 3$ , which are similar to that when k = 5. The location errors increase no matter larger or smaller k values are adopted since bias exist with too few candidates while too many candidates would involve low confident estimations.

# 7.6.2.8 System Latency

Finally, we test the running latency of ViVi by stimulating consecutive user queries. We randomly select one query fingerprint from a set of queries and ViVi returns the location estimations. Then we average the time delays for 1000 such queries. For each comparative method, we run the same process and calculate the average running time.The average query delay of ViVi is 0.33 s per query, which is similar with or shorter than previous works. As comparison, the per query delays of Horus, GIFT, and TW-KNN are 0.38, 0.77, and 1.04 s, respectively.

# 7.7 Conclusions

In this chapter, we propose a new form of RSS fingerprint termed as fingerprint spatial gradient, which exploits the underlying spatial properties of nearby fingerprints and turns out to be more stable and distinctive than the original RSS fingerprints. Built on top of traditional RSS fingerprint database, ViVi well overcomes the drawbacks of spatial ambiguity and temporal instability adhering to previous RSS fingerprints and achieves performance gain without the pains of resorting to additional information or restrictions or vulnerable RSS model assumptions. We prototype ViVi on smartphones and conduct extensive experiments in different buildings. The results demonstrate that ViVi yields great performance, outperforming start-of-the-art approaches.

# References

1. Azizyan, M., Constandache, I., Roy Choudhury, R.: Surroundsense: mobile phone localization via ambience fingerprinting. In: Proceedings of the ACM MobiCom (2009)

2. Bahl, P., Padmanabhan, V.N.: RADAR: an in-building RF-based user location and tracking system. In: Proceedings of the IEEE INFOCOM (2000)   
3. Chen, Y., Yang, Q., Yin, J., Chai, X.: Power-efficient access-point selection for indoor location estimation. IEEE Trans. Knowl. Data Eng. 18(7), 877–888 (2006)   
4. Cheng, W., Tan, K., Omwando, V., Zhu, J., Mohapatra, P.: Rss-ratio for enhancing performance of rss-based applications. In: Proceedings of the IEEE INFOCOM (2013)   
5. Chintalapudi, K., Padmanabha Iyer, A., Padmanabhan, V.N.: Indoor localization without the pain. In: Proceedings of the ACM MobiCom (2010)   
6. Fang, S.H., Lin, T.: Principal component localization in indoor wlan environments. IEEE Trans. Mob. Comput. 11(1), 100–110 (2012)   
7. Han, D., Jung, S., Lee, M., Yoon, G.: Building a practical wi-fi-based indoor navigation system. IEEE Pervasive Comput. 13(2), 72–79 (2014)   
8. He, S., Chan, S.H.G.: Wi-fi fingerprint-based indoor positioning: recent advances and comparisons. IEEE Commun. Surv. Tutorials 18(1), 466–490 (2016)   
9. He, S., Hu, T., Chan, S.H.G.: Contour-based trilateration for indoor fingerprinting localization. In: Proceedings of the ACM SenSys (2015)   
10. Hilsenbeck, S., Bobkov, D., Schroth, G., Huitl, R., Steinbach, E.: Graph-based data fusion of pedometer and WiFi measurements for mobile indoor positioning. In: Proceedings of the ACM UbiComp (2014)   
11. Jiang, Y., Xiang, Y., Pan, X., Li, K., Lv, Q., Dick, R.P., Shang, L., Hannigan, M.: Hallway based automatic indoor floorplan construction using room fingerprints. In: Proceedings of the ACM UbiComp (2013)   
12. Jun, J., Gu, Y., Cheng, L., Lu, B., Sun, J., Zhu, T., Niu, J.: Social-loc: improving indoor localization with social sensing. In: Proceedings of the ACM SenSys (2013)   
13. Kotaru, M., Joshi, K., Bharadia, D., Katti, S.: Spotfi:decimeter level localization using WiFi. In: Proceedings of the ACM SIGCOMM (2015)   
14. Krishnan, P., Krishnakumar, A., Ju, W.H., Mallows, C., Ganu, S.: A system for lease: location estimation assisted by stationary emitters for indoor rf wireless networks. In: Proceedings of the IEEE INFOCOM (2004)   
15. Li, L., Shen, G., Zhao, C., Moscibroda, T., Lin, J.H., Zhao, F.: Experiencing and handling the diversity in data density and environmental locality in an indoor positioning service. In: Proceedings of the ACM MobiCom (2014)   
16. Li, X., Li, S., Zhang, D., Xiong, J., Wang, Y., Mei, H.: Dynamic-music: accurate device-free indoor localization. In: Proceedings of ACM UbiComp (2016)   
17. Liu, H., Gan, Y., Yang, J., Sidhom, S., Wang, Y., Chen, Y., Ye, F.: Push the limit of WiFi based localization for smartphones. In: Proceedings of the ACM MobiCom (2012)   
18. Lymberopoulos, D., Liu, J., Yang, X., Choudhury, R.R., Handziski, V., Sen, S.: A realistic evaluation and comparison of indoor location technologies: experiences and lessons learned. In: Proceedings of ACM/IEEE IPSN (2015)   
19. Mirowski, P., Whiting, P., Steck, H., Palaniappan, R., MacDonald, M., Hartmann, D., Ho, T.: Probability kernel regression for WiFi localisation. J. Locat. Based Serv. 6(2), 81–100 (2012)   
20. Nandakumar, R., Chintalapudi, K.K., Padmanabhan, V.N.: Centaur: locating devices in an office environment. In: Proceedings of the ACM MobiCom (2012)   
21. Rai, A., Chintalapudi, K.K., Padmanabhan, V.N., Sen, R.: Zee: zero-effort crowdsourcing for indoor localization. In: Proceedings of the ACM MobiCom (2012)   
22. Sen, S., Radunovic, B., Choudhury, R.R., Minka, T.: You are facing the Mona Lisa: spot localization using phy layer information. In: Proceedings of the ACM MobiSys (2012)   
23. Shen, G., Chen, Z., Zhang, P., Moscibroda, T., Zhang, Y.: Walkie-Markie: indoor pathway mapping made easy. In: Proceedings of the USENIX NSDI (2013)   
24. Shu, Y., Huang, Y., Zhang, J., Cou, P., Cheng, P., Chen, J., Shin, K.G.: Gradient-based fingerprinting for indoor localization and tracking. IEEE Trans. Ind. Electron. 63(4), 2424– 2433 (2016)   
25. Sun, W., Liu, J., Wu, C., Yang, Z., Zhang, X., Liu, Y.: MoLoc: on distinguishing fingerprint twins. In: Proceedings of the IEEE ICDCS (2013)

26. Vasisht, D., Kumar, S., Katabi, D.: Decimeter-level localization with a single WiFi access point. In: Proceedings of the USENIX NSDI (2016)   
27. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: Proceedings of the ACM MobiSys (2012)   
28. Wang, J., Jiang, H., Xiong, J., Jamieson, K., Chen, X., Fang, D., Xie, B.: Lifs: low human effort, device-free localization with fine-grained subcarrier information. In: Proceedings of ACM MobiCom (2016)   
29. Wu, K., Xiao, J., Yi, Y., Gao, M., Ni, L.M.: Fila: fine-grained indoor localization. In: Proceedings of the IEEE INFOCOM (2012)   
30. Wu, C., Yang, Z., Xiao, C., Yang, C., Liu, Y., Liu, M.: Static power of mobile devices: selfupdating radio maps for wireless indoor localization. In: Proceedings of the IEEE INFOCOM (2015)   
31. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Enhancing WiFi-based localization with visual clues. In: Proceedings of the ACM UbiComp (2015)   
32. Yang, Z., Wu, C., Liu, Y.: Locating in fingerprint space: wireless indoor localization with little human intervention. In: Proceedings of the ACM MobiCom (2012)   
33. Yang, Z., Wu, C., Zhou, Z., Zhang, X., Wang, X., Liu, Y.: Mobility increases localizability: a survey on wireless indoor localization using inertial sensors. ACM Comput. Surv. 47(3), 54:1–54:34 (2015)   
34. Ye, X., Wang, Y., Hu, W., Song, L., Gu, Z., Li, D.: WarpMap: accurate and efficient indoor location by dynamic warping in sequence-type radio-map. In: Proceedings of the IEEE SECON (2016)   
35. Yin, J., Yang, Q., Ni, L.M.: Learning adaptive temporal radio maps for signal-strength-based location estimation. IEEE Trans. Mob. Comput. 7(7), 869–883 (2008)   
36. Youssef, M., Agrawala, A.: The horus location determination system. Wirel. Netw. 14(3), 357– 374 (2008)   
37. Zheng, Y., Shen, G., Li, L., Zhao, C., Li, M., Zhao, F.: Travi-Navi: self-deployable indoor navigation system. In: Proceedings of the ACM MobiCom (2014)

# Chapter 8 Enhancing WiFi Fingerprinting with Visual Clues

![](images/fd1e9cff94c40dc9e91fcbbb5e209de777101453a563221bbe721ed83e9cc5d3.jpg)

Abstract Pioneer efforts to improve WiFi-based localization have resorted to motion-assisted or peer-assisted localization. They neither work in real time nor work without the help of peer users, which introduces extra costs and constraints, and thus degrades their practicality. To get over these limitations, an image-assisted localization system, named Argus, is introduced for mobile devices. The basic idea of Argus is to extract geometric constraints from crowdsourced photos, and to reduce fingerprint ambiguity by mapping the constraints jointly against the fingerprint space. This chapter describes techniques to offer such an image-assisted localization scheme.

# 8.1 Introduction

As mentioned in previous chapters, one major obstacle against accurate WiFi fingerprinting is “Fingerprint Ambiguity”, where two distant locations may possess similar RSS fingerprints. Thus a user may be mistakenly matched to a position faraway from the true position. The growing of the WiFi fingerprint database and the irregularity of indoor environments also aggravates the problem of fingerprint ambiguity. In fact, it was reported that fingerprint ambiguity is the root cause of large errors in WiFi fingerprinting localization [18].

To address the problem of fingerprint ambiguity, previous research leverages either mobility or peer assistance. Mobility assisted approaches [34] resolve ambiguity by either using particle filters [13] or matching a sequence of fingerprints along a trajectory [35]. Alternatively, peer assisted schemes mitigate ambiguity by imposing extra constraints from other users. Pilot works [12, 18] measure inter-distance among peer users and jointly map their locations subject to the inter-distance constraints so as to reduce fingerprint ambiguity. Others [14] correlate fingerprints utilizing opportunistic encounters between peers to sift location candidates. However, the aforementioned works have the following limitations that impede their practical deployment. (i) Involve user movement, which can induce delay in localization before a sufficient trajectory is recorded [13, 35].

(ii) Require a group of stationary users during inter-distance measurements [18]. (iii) Risk performance degradation if there are insufficient willing peers [18] or encounters [14].

The above limitations motivate us to design and implement Argus,1 an imageassisted positioning scheme. The intuition is simple: recent smart phones are all equipped with powerful cameras and people take photos with their phones anywhere and anytime. It is our vision to reduce the fingerprint ambiguity by extracting geometric constraints by utilizing visual clues beneath those ubiquitous photos. Then by mapping the constraints onto the fingerprint space, we are likely to distinguish multiple locations with similar fingerprints. On this basis, Argus works as follows. When an user wants to know the location, he/she bootstraps Argus app and takes a photo of nearby place of interest (denoted by POI, it can be any physical feature or indoor landmark like shop logos, statues, and billboards). The absolute POI location is not required and users can take photos at a relatively long distance.

The query photo together with his/her current RSS fingerprint will be sent to the server. After matching the query photo to the corresponding POI and handling device heterogeneity, we adopt a photo selection mechanism to choose some supporting photos to assist localization. Then we use a Computer Vision (CV) technique called Structure from Motion (SfM [16]) to generate geometric constraints among those photos. Finally, Argus maps their locations jointly against fingerprint space subjecting the geometric constraints and our cost function.

Despite the simple idea, three major challenges underlie the design of Argus: (1) How to effectively construct the image database? Manual configuration requires a great amount of time and effort, and it is a major obstacle for pure image-based solutions [9]. Instead, we adopt crowdsourcing and extract the geometric constraints without knowing their ground truth locations. (2) How to utilize and evaluate geometric constraints for accurate localization? The key here is that the constraints obtained from photos are relative, unknown scaling, translation, and rotation exist from the corresponding locations in the real world [22]. So we transform the problem into a combinatorial optimization problem, and solve it efficiently by pruning and interpolation. (3) As a mobile application level service, Argus should execute in a real-time and energy-efficient manner. We address these by introducing a module driven structure and a set of efficient algorithms.

To the best of our knowledge, Argus is the first work that provides image-assisted WiFi localization with crowdsourced photos. It combines geometric constraints extracted from images with RSS fingerprints to address fingerprint ambiguity. We adopt a crowdsourcing approach to construct an unlabelled image database and design a combinatorial optimization to evaluate location candidates. Such scheme provides Argus with the following desired properties: (1) One click localization, users can be localized with a single photo, which is natural and easy-to-follow. (2) Highly compatible with existing RSS-based localization systems, only extra effort is to construct an image database, which is crowdsourced and automatic. (3) Fast and accurate, it takes advantage of both the RSS-based method and image-based method, improves localization accuracy while bypassing the huge overhead of pure image-based method.

We fully implemented Argus on smartphones and conducted extensive experiments in two types of large complex indoor environments: shopping mall and food plaza. Argus triples the localization accuracy achieved by the mainstream RSSbased method, and limits the mean localization error to less than 1 m while achieves less than 8 s localization latency.

The rest of the chapter clarifies each of the above contributions, beginning with related works in Sect. 8.2 and observations of using WiFi fingerprint for indoor localization in Sect. 8.3. Following an overview in Sect. 8.4, the design and implementation of Argus are presented in Sects. 8.5, 8.6, and 8.7, with evaluation coming in Sect. 8.8. Finally, we summarize the limitations and point out potential future work.

# 8.2 Related Works

Argus is closely related in the following categories of research.

Enhancing WiFi Fingerprint Localization Due to the ubiquity of WiFi, extensive research efforts utilize it for indoor localization [10, 20]. In particular, WiFi fingerprinting [3, 36] has attracted increasing attention for its applicability in complex indoor environments [11]. To improve location distinction (and thus localization accuracy), pioneer efforts exploit various sensing modalities to enrich WiFi fingerprints from physical layers [26], ambient audio and images [2], inertial features [30], magnetic field [32], to name a few. Orthogonally, Argus improves localization accuracy by imposing geometric constraints on WiFi fingerprints and is compatible with the enriched fingerprints above.

Instead of globally enriching WiFi fingerprints with extra modalities, recent research harnesses local constraints to eliminate fingerprint ambiguity via motion and peer assistance [34]. For instance, MoLoc [29] differentiates locations with similar WiFi fingerprints via walking directions. WarpMap [35] reduces ambiguity by matching WiFi fingerprint sequences along a trajectory. Social-Loc [14] leverages encounters of mobile users to reduce location errors. In [18], the authors measure distances among nearby peers using acoustic sensing to alleviate fingerprint ambiguity of a single device. Wi-Dist [12] designs a general localization framework combining WiFi fingerprints and theri inter-distance bounds. Argus is motivated by this thread of research. Differently, Argus utilizes CV techniques to generate geometric constraints without requiring user movements nor the assistance of nearby peers.

Image-based Indoor Localization The sub-meter accuracy of image-based localization makes it a fit for robot localization and navigation [23]. Adopting imagebased localization to smartphone cameras is non-trivial because the geometric relationships derived from images are relative [16], and it is challenging to extract an accurate mapping from the relative geometric relationships to physical coordinates from a smartphone user. OPS [22] locates remote objects by taking a few photos from different known locations, while in Argus, the user takes one photo and localizes himself/herself. Sextant [8] localizes users by taking three photos annotated with direction for triangulation, while Argus requires one single photo without extra inertial measurements. iMoon [6] integrates photo-generated mesh with user trajectories to construct a floor plan and provide user localization and navigation, but requires large amount of photos to bootstrap. ClickLoc [33] proposes an imagebased user localization scheme by requiring the user to take two photos. Different from the above image-based localization systems where photos are processed to construct a 3D relative model, Argus is an image-assisted localization scheme where photos are used to derive geometric constraints for WiFi fingerprinting. Hence Argus eliminates the need of a mapping between the image space and the physical space, which is difficult to obtain without user intervention.

# 8.3 Measurements and Observations

This section conducts a measurement and error analysis of a WiFi fingerprinting localization system deployed in office environments to motivate the design of Argus.

# 8.3.1 Measurements

As a motivating example, we deploy RADAR [3], a representative RSS fingerprinting based localization system, in an office building of $7 0 \times 2 3 \mathrm { m } \ ( \mathrm { F i g } . 3 . 2 )$ . The building contains 16 offices, of which 5 are large rooms of 142 m2, 7 are small ones of different sizes and the other 4 are inaccessible. A volunteer is asked to record 50 WiFi fingerprints at each of the 279 known locations from 26 APs. Among the 50 fingerprints collected at each location, 20 are used for training and the rest 30 are for testing. Each location can receive signals from 6 to 7 APs on average. We modify the location estimation scheme as [28] to improve the localization accuracy. Specifically, for each location query fingerprint $f _ { i }$ , denote N (i) as the set of fingerprints in the database with the N smallest distances to $f _ { i }$ , and $\left\lceil f _ { i } ^ { \mathbb { N } ( 1 ) } , \dots , f _ { i } ^ { \mathbb { N } ( N ) } \right\rceil$ be the set of N nearest neighbors in the signal space. Then the neighborhood weights of $f _ { i }$ are calculated by:

$$
\text { Minimize } \left| f _ {i} - \sum_ {j \in \mathbb {N} (i)} W _ {i j} f _ {i} ^ {\mathbb {N} (j)} \right| \tag {8.1}
$$

$$
\text { Subject   to } \sum_ {j \in \mathbb {N} (i)} W _ {i j} = 1 \tag {8.2}
$$

![](images/242c106fe1e2f63c0a2890bfae5b12f4b143edada77d1d98929ebf5c5514438a.jpg)



(a) Errors with different sample size

![](images/758aac57019771dc6d6e27a7cb39ee795b8bfa79f3b9993ab852e507149cd21a.jpg)



(b) Large Error Case 1

![](images/e707c44437bcbacd0c499daa27ba7ea92a25ff450c7446b8792e83ef4d21b5c4.jpg)



(c) Large Error Case 2   
Fig. 8.1 Results and observations of measurement study. (a) Error distribution with different number of WiFi samples. (b) An example of two locations faraway that have similar WiFi fingerprints. (c) An example of top five nearest fingerprints that scatter in the physical space

# 8.3.2 Observations

Through an in-depth analysis on the localization errors, we make the following observations.

Observation 1: Collecting more WiFi samples for each location improves the overall localization accuracy, but large errors still exist Intuitively, recording more samples at the same location and averaging the RSSs from the same AP as the fingerprints for both location query and training mitigates random noise and contributes to more robust localization. We plot the cumulative distribution function (CDF) of localization errors with different amounts of WiFi samples averaged as fingerprints in Fig. 8.1a. As shown, more samples result in a higher accuracy. However, even with 10 samples, there is still a considerable amount of large errors (>5 m), as shown in the long tails in the CDFs.

Observation 2: Large errors occur mainly due to the inconsistency of WiFi fingerprints in the physical space and the signal space The key assumption for fingerprinting based localization is that the WiFi fingerprints of nearby locations are similar. However, this assumption may not hold in complex indoor environments. First, locations far away from the true position may possess more similar fingerprints in signal space. Figure 8.1b illustrates an example of this case. The floor plan is divided into grids corresponding to Fig. 3.2. The color of each grid represents its RSS Euclidean distance to the query WiFi fingerprint in signal space (The redder, the closer). A query is sent from location (9, 5) (marked by a dotted circle), and its closest neighbor in signal space is (14, 1) (marked by a dotted rectangle), which leads to an error of 8.6 m. Second, even if the closest fingerprint is correctly matched, the top closest neighbors in signal space may scatter in physical space. Figure 8.1c shows an example, where the query fingerprint is taken at (22, 2), and its top five nearest neighbors in signal space are (22, 2), (32, 5), (23, 1), (24, 4), and (24, 3). With the estimated location as the weighted average of the top five nearest neighbors, the localization error is 6.46 m.

In summary, large errors are mainly caused by WiFi fingerprints that are close in signal space but distant in physical space, i.e., fingerprint ambiguity. Insufficient APs, noisy RSS measurements, and environmental dynamics (e.g. change of furniture or RF interference) are some factors that lead to such ambiguity, which are difficult to eliminate without extra constraints [18]. Thus the aim of Argus is to resolve such fingerprint ambiguity from an orthogonal domain, i.e., by utilizing extra constraints extracted from crowdsourced photos.

# 8.4 System Overview

# 8.4.1 Working Flow from User’s Perspective

When a user needs to be localized, he/she just activates Argus’ app on his/her smartphone. The camera is automatically turned on, along with the WiFi scanning. Then the user is instructed to shoot a POI near the center of his/her viewfinder without walking near it (The user can take a photo at a relatively long distance as long as the POI is clearly taken). Afterwards, Argus will send the photo as well as the RSS fingerprint to the server. After the remote processing, a location tag will be returned to the smart phone, and Argus displays this location to the user.

# 8.4.2 Working Flow from Server’s Perspective

As shown in Fig. 8.2, the input of server side are a query image and its corresponding WiFi fingerprint. The server handles the localization query in a pipeline manner briefed as follows. First of all, the server will figure out which POI the user is shooting for, and the photos for the same POI will be identified by a Image Match module. Then with a Supporting Photo Selection module, it adopts a photo selection mechanism to pick up the most suitable photos (termed as supporting photo) among the photos for the same POI to assist human localization. The mechanism considers both the quality of supporting photos and their WiFi fingerprints. Once the supporting photos are selected, a Geometric Constraint Extraction module applies a CV technique called Structure from Motion [16] in order to obtain the relative locations and orientations of the shooting sites among these photos (supporting photos + query photo), and these form the geometric constraints for a Joint Location Estimation module. At the same time, a rough user localization will be estimated by a WiFi Position Estimation module in the same way as we have introduced in the observation after handling the hardware heterogeneity in a Device Gain Estimation module. Finally, a Joint Location Estimation module estimates user location by considering the WiFi fingerprints and the geometric constraints jointly. We model this joint localization into a combinatorial optimization problem, the position that minimizes the cost function is regarded as the user location.

![](images/406eef2a5cb4f31c1b1b7ccbfb31de904dbf49a76ac922758ac858917d53c788.jpg)



Fig. 8.2 Work flow of Argus

# 8.5 Image Processing Pipeline

The aim of the image processing pipeline is to select multiple supporting photos and generate relative geometric constraints for joint location estimation.

# 8.5.1 Image Matching

The image matching module takes a query image as input, and associates it to the best matched Point Of Interest (POI) in the database.

We implement a direct 2D-to-3D matching framework motivated by the work of [25] using visual words technique for fast image matching. Then, we use a simple threshold-based mechanism to judge whether the POI is correctly identified. If the image matching score is above the threshold, Argus executes the next step directly. However, the photos taken by the users could be unclear, unfocused, blurred, or obstructed. So we adopt an image match correction mechanism when the image matching score is below the threshold.

As illustrated in Fig. 8.3, Argus retrieves the top four candidate POIs and ask the user to identify the correct one by tapping the thumbnail images.

# 8.5.2 Relative Geometric Constraint Extraction

Since each POI normally is associated with multiple photos in the database, these photos can serve as supporting photos (the selection process detailed in Sect. 8.5.3) and generate relative geometric constraint for joint location estimation (Sect. 8.7).

Fig. 8.3 Image match correction   
![](images/f2de237acbdd58d6b7c56392714bc5b6d0be5f11f74e6ac86401e3b7b0684892.jpg)



In Argus, we extract relative geometric constraint from multiple supporting photos via Structure from Motion (SfM). SfM [16] is a computer vision technique to derive the 3D model of an object from multiple photos of the object. It takes multiple photos of an object taken from different locations and angles as input. Then for each photo, it runs a feature detection algorithm (e.g., SIFT [19]) and identifies various keypoints. By matching the sets of keypoints from multiple photos, SfM attempts to reconstruct:

• A sparse 3D point cloud of the geometry captured by those keypoints.   
• The relative positions and orientations of the camera where the original photos were taken [22].

Argus takes both the query photo and multiple supporting photos into SfM, and obtains the relative locations among these photos to form a polygon as the relative geometric constraint.

Note that SfM has been adopted in image-based localization systems [9, 22, 25]. Despite their high accuracy, they usually require hundreds of overlapping photos for each POI to generate a dense point cloud. In addition, image-based localization systems need to collect precise absolute locations of the photos during the training stage, which incurs prohibitive overhead. Instead, Argus utilizes photos as visual clues for WiFi fingerprinting localization. Thus it only needs fewer than five photos to construct a sparse point cloud and merely requires relative geometric constraints.

# 8.5.3 Supporting Photo Set Selection

The rationale to extract visual clues from photos to assist WiFi fingerprinting is that the relative geometric constraint (visual clues) generated from photos are highly accurate. Therefore, instead of selecting supporting photos at random, it is essential to select an efficient set of supporting photos to ensure precise relative geometric constraint generation. An effective supporting photo set satisfies the following two criteria.

1. The photos in the supporting photo set have high similarity scores (Sect. 8.5.1) with the query photo. This is because photos with high similarity scores tend to be photos of the same POI, which are suitable candidates to generate geometric constraints using SfM.

2. The geometric constraint generated by the supporting photo set (excluding the query photo) is highly consistent with ground truth in the database. Such consistency indicates the feasibility of adopting geometric constraint.

The first criterion serves as a coarse-grained filter to sieve out photos of low quality (e.g. blurred, taken faraway or with obstacles). We empirically set a threshold and remove all photos associated with queried POI that exceed the threshold. To meet the second criterion, we examine the combinations of the remaining photos by comparing the shape similarity between the polygon generated by SfM and that formed by the ground truth locations of the photos stored in the database.

To quantify the shape similarity between two polygons (one generated by SfM and the other formed by the absolute inter-distances among supporting photos), we propose a shape similarity score. The shape similarity score should satisfy the following properties: (1) numeric; (2) light-weight; and (3) invariant to scaling, rotation and translation, since the polygon generated by SfM only has relative coordinates. Specifically, we calculate the shape similarity score based on [1] in two steps.

Polygon Representation Similar to [1], we represent a polygon using a turning function $\Theta _ { A } ( s )$ , where A is the simple polygon and s is the arc length. $\Theta _ { A } ( s )$ measures the angle of the counter-clockwise tangent as a function of the arc length s, from some reference point O on $A \ ' s$ boundary. Thus A(0) is the angle v that the tangent at the reference point O makes with some reference orientation associated with the polygon (x-axis in our case). $\Theta _ { A } ( s )$ keeps track of the turning, increasing with left-hand turns and decreasing with right-hand turns as in Fig. 8.4a. Without loss of generality, we rescale each polygon with normalized perimeter length. Note that $\Theta _ { A } ( s )$ is invariant to scaling and translation by definition. The rotation of A corresponds to a simple shift of $\Theta _ { A } ( s )$ in the θ direction.

Polygon Distance Function Assume two polygons A and B and their turning functions $\Theta _ { A } ( s )$ and $\Theta _ { B } ( s )$ ). The shape similarity score between A and B can be measured by the distance between the turning function $\Theta _ { A } ( s )$ and $\Theta _ { B } ( s )$ using $L _ { p }$ distance:

![](images/50336bfa429e0308b4b2b4d47094ea9f9bc4102d800372794e9beb8c10d43bcd.jpg)



(a)

![](images/5758a40535bb13b819e91534455986c2d1fcf43bbb35db3326116d8e2c0f1298.jpg)



(b)   
Score: 0.789   
Score: 0.398   
Score: 0.637

Fig. 8.4 Illustration of shape similarity score. (a) A polygon represented by turning function. (b) Polygon pairs and their shape similarity scores

$$
\delta_ {p} (A, B) = \| \Theta_ {A} - \Theta_ {B} \| _ {p} = \left(\int_ {0} ^ {1} | \Theta_ {A} (s) - \Theta_ {B} (s) | ^ {p} d s\right) ^ {\left(\frac {1}{p}\right)} \tag {8.3}
$$

However, Eq. 8.3 is sensitive to the rotation of A (or B) and the choice of reference point on the boundary of A (or B). Thus we make B stable and find the minimum distance by adjusting A. If we rotate A by an angle θ, then the new turning function is given by $\Theta _ { A } ( s ) + \theta$ . And if we move the reference point along the boundary by a distant t, the new function is given by $\Theta _ { A } ( s + t )$ . Then we can find the minimum distance by adjusting θ and t, and the shape similarity score between A and B is measured by:

$$
d _ {p} (A, B) = \left(\min _ {\theta \in \Re , t \in [ 0, 1 ]} \int_ {0} ^ {1} | \Theta_ {A} (s + t) - \Theta_ {B} (s) + \theta | ^ {p} d s\right) ^ {\left(\frac {1}{p}\right)} \tag {8.4}
$$

For simple polygons, Eq. 8.4 can be further simplified to a one-variable minimization problem which runs in polynomial time [1]. Thus the similarity score can be calculated efficiently. A similarity score below 0.5 usually indicates that two polygons resemble each other [1]. As an illustration, Fig. 8.4b shows several pairs of polygons and the corresponding shape similarity scores.

# 8.6 WiFi Processing Pipeline

The WiFi processing pipeline follows typical WiFi fingerprinting localization systems [3]. Rather than yield the final location, however, the WiFi processing pipeline outputs a rough location as the starting point for joint location estimation (Sect. 8.7).

![](images/cc802ae42d7e75516556d8c2e43f0169c6a3cdf0a706959276c81a991e370eec.jpg)



![](images/b6ce1a03db951cce2d8604008e245531c2000269413511f6771e93872efa6ec3.jpg)



Fig. 8.5 Illustration of device diversity. (a) RSS vectors measured by two phones at one place. (b) Histograms of RSS offset measured by two phones at different locations in a shopping mall

# 8.6.1 Device Calibration

As Argus aims to provide ubiquitous localization serves, it is essential to handle the impact of device diversity on WiFi fingerprints. Due to difference in hardware (e.g., antenna gain), different WiFi modules may report different received signal strength (RSS) even at the same location [21]. As shown in Fig. 8.5a, the RSS vectors (fingerprints) of the same location in a shopping mall recorded by two devices differ. Figure 8.5b further shows the histogram of RSS offsets measured by the two devices at various locations in the same shopping mall. Such a large bias from different devices can lead to significant errors in WiFi fingerprinting.

To compensate for the RSS offset between different devices, various calibration schemes have been proposed. For instance, instead of directly utilizing RSS as fingerprints, RSS deduction [7, 21] or ratio [15] can be adopted. To remain compatible with conventional RSS-based localization systems, Argus employs a learning based online calibration approach similar to [17] to jointly estimate the location and device-specific gain via Expectation Maximization. Specifically, denote the Euclidean distance between two fingerprints collected at $\begin{array} { r } { l } { \ i _ { x } \ \left( \pmb { f } _ { x } \right. = } \end{array}$ $[ f _ { x 1 } , f _ { x 2 } , \ldots , f _ { x m } ] )$ and $l _ { y } ( f _ { y } = \left[ f _ { y 1 } , f _ { y 2 } , \ldots , f _ { y m } \right] )$ as:

$$
\triangle_ {x y} = \sqrt {\sum_ {i = 1} ^ {m} \left| f _ {x i} - f _ {y i} \right| ^ {2}} \tag {8.5}
$$

where m is the number of APs.

Then in the offset estimation, we simplify the transformation between a pair of devices between A and B as $R S S _ { B } = \alpha R S S _ { A } + \delta$ . Furthermore, it was reported that α is close to 1 [24]. So we add a constant δ when calculating the signal space distance, $\begin{array} { r } { \triangle _ { x y } \ = \ \sqrt { \sum _ { i = 1 } ^ { m } | f _ { x i } - f _ { y i } + \delta | ^ { 2 } } } \end{array}$ . By adjusting the value of δ, we can find the minimum signal space distance, the corresponding δ is regarded as the offset. Formally,

$$
O _ {x y} = \underset {\delta} {\arg \min} \triangle_ {x y} \tag {8.6}
$$

$$
\triangle_ {x y} = \sqrt {\sum_ {i = 1} ^ {m} \left| f _ {x i} - f _ {y i} + O _ {x y} \right| ^ {2}} \tag {8.7}
$$

The above mechanism suffices for online calibration, we evaluate it with data collected by three different devices. Its performance will be presented and discussed in the experiment.

# 8.6.2 WiFi Fingerprinting

RSS values is well-known to be vulnerable to complex environmental changes and frequently fluctuate over time, which yields large errors in the initial location estimations by WiFi and further degrade the ultimate performance of Argus. Assume there are k raw samples for each AP at a specific location, denoted as $r =$ $[ r _ { 1 } , \cdot \cdot \cdot , r _ { i } , \cdot \cdot \cdot , r _ { k } ]$ where $r _ { i }$ is observed at time ti. Previous works usually simply average the RSS vector into a mean value or model it as a probabilistic distribution for a fingerprint [3, 36], which may be susceptible to large RSS outliers or require a large number of samples at each location.

Instead, to better tolerate the temporal variations, we employ the filter over the RSS measurements r of each AP to obtain a weighted average version r. We adopt the iterative recursive filter as in [5] to weight a sequence of temporal RSS values. The filter is lightweight and computation efficient while has high smoothness and is applicable when there are only a small number of RSS samples for each location. The iterative filtering procedure is illustrated in Algorithm 8.1.

By iterative recursive filtering, WiFi fingerprinting is expected to yield a reasonable accuracy for the following joint location estimation in most cases. As analyzed in [18], however, extremely large errors still occur. To avoid the influence of such large initial errors, we devise techniques to identify them in the WiFi Position Estimation step and declare their involvement in joint location estimation. Specially, we design two basic principles for quality management of WiFi fingerprinting.

• Top-K candidates dispersion. The rationale lies in that a location estimate tends to be accurate if the corresponding top-K candidates are close to each other. We measure the dispersion of top-K candidates as the mean value of the mutual distances between each pair of them. If the dispersion exceeds a certain value, i.e., the top-K candidate locations distribute two distantly, we discard the current peer for further use. In this work, we set the dispersion threshold equivalent to the radius, i.e., 10 m, we considered in joint location estimation (See Sect. 8.7).

Algorithm 8.1: Iterative filtering   
Input:
The raw RSS values $r = [r_{1}, \cdots, r_{i}, \cdots, r_{k}]$ ;
Weighted coefficients $w_{1}, w_{2}, w_{3}, w_{4}, w_{5}$ .
Output:
The weighted average RSS $\bar{r}$ 1: $R_{1}(t_{1}) = r_{1}$ , $R_{2}(t_{1}) = r_{1}$ , $R_{3}(t_{1}) = r_{1}$ ;
2: if $k \geq 2$ then
3: $R_{1}(t_{2}) = w_{1}r_{1} + w_{2}r_{2}$ ;
4: $R_{2}(t_{2}) = w_{1}R_{1}(t_{1}) + w_{2}R_{1}(t_{2})$ ;
5: $R_{3}(t_{2}) = w_{1}R_{2}(t_{1}) + w_{2}R_{2}(t_{2})$ ;
6: end if
7: for each $2 < i \leq k$ do
8: $R_{1}(t_{i}) = w_{3}r_{i-2} + w_{4}r_{i-1} + w_{5}r_{i}$ ;
9: $R_{2}(t_{i}) = w_{3}R_{1}(t_{i-2}) + w_{4}R_{1}(t_{i-1}) + w_{5}R_{1}(t_{i})$ ;
10: $R_{3}(t_{i}) = w_{3}R_{2}(t_{i-2}) + w_{4}R_{2}(t_{i-1}) + w_{5}R_{2}(t_{i})$ ;
11: end for
12: $\bar{r} = R_{3}(t_{k})$ ;

• Common AP ratio. In principle, two fingerprints observed at closer locations generally share more common APs. In contrast, two fingerprints with few common APs are unlikely to be matched, regardless of their fingerprint similarity. Hence, we exclude location estimates with common AP ratio less than a specific threshold. We examine the common AP ratio distribution based on the fingerprint database of the floorplan in Fig. 3.2 and empirically choose the threshold ratio according to the ratios of all location pairs that are less than 10 m away from each other.

By triggering any of the two rules, we discard the current WiFi estimated location for joint localization.

# 8.7 Joint Location Estimation

The joint location estimation module outputs an accurate location estimate by superimposing the geometric constraint (polygon extracted from supporting photos by SfM) onto the fingerprint space based on the rough location estimated by WiFi fingerprinting. Figure 8.6 illustrates an example of joint location estimation. The inputs of joint location estimation consist of two polygons. The hollow-dot vertices are locations of the query photo and the supporting photos estimated by WiFi fingerprinting, which forms a polygon with dashed-dotted-line edges denoting absolute yet inaccurate inter-distances. The solid-line polygon represents the relative but accurate geometric constraints among the query photo and the supporting photos. By scaling, rotating and translating the solid-line polygon such that the two polygons maximally match with each other, a more accurate location of the query photo is estimated. As is shown, due to the highly accurate geometric constraint, the newly estimated location is closer to the ground truth (the dash-line polygon).

![](images/c07fce2e41c48cb812c4d98ef4bd3402390ff3c7b8737b234140b7693a9dbe70.jpg)



![](images/12e8a772faf82703b9dffc8478b01131ed90c9584e48801cc65ed3ddd48ead4a.jpg)



Fig. 8.6 Illustration of joint location estimation by matching the WiFi estimated and SfM generated polygons

# 8.7.1 Problem Formulation

Mathematically, we formulate the process of joint location estimation as the following optimization problem. Let $A \ = \ \left\{ a _ { 1 } , a _ { 2 } , \ldots , a _ { | V | } \right\}$ denote the WiFi estimated locations of vertices in V , and $B = \left\{ b _ { 1 } , b _ { 2 } , \ldots , b _ { | V | } \right\}$ denote the new location outputs. The aim is to minimize the sum of Euclidean distances between the WiFi fingerprints of location set A and those of location set B, under the SfM generated geometric constraint. We denote the SfM generated geometric constraint by $G ( E , V )$ , where V and E are the vertex and edge sets, and $E _ { i , j } = \left( V _ { i } , V _ { j } \right)$ . Hence the joint location estimation problem can be expressed as:

$$
\text { Minimize } \quad \sum_ {\forall i} [ f (a _ {i}) - f (b _ {i}) ] [ f (a _ {i}) - f (b _ {i}) ] ^ {T} \tag {8.8}
$$

Subject to

$$
\forall i, j: (1 - \alpha) \frac {\left| E _ {i , j} \right|}{\left| E _ {1 , 2} \right|} \leqslant \frac {\left| \left(b _ {i} , b _ {j}\right) \right|}{\left| \left(b _ {1} , b _ {2}\right) \right|} \leqslant (1 + \alpha) \frac {\left| E _ {i , j} \right|}{\left| E _ {1 , 2} \right|} \tag {8.9}
$$

where $f \left( x \right)$ is the WiFi fingerprint at location x, $\big | ( b _ { i } , b _ { j } ) \big |$ is the edge length formed by newly location estimates $b _ { i }$ and $b _ { j }$ . α is used to adjust the weight of the geometric constraint. The cost function evaluates the collective closeness of both the location of the query photo and those of the supporting photos.

# 8.7.2 Problem Hardness

To study the hardness of the above problem, we generalize it into the following problem.

Definition 8.1 (Generalized Problem) Given a set of photos, their WiFi fingerprints, and the geometric constraints among the photos, is there a set of locations in the fingerprint database such that the summation of Euclidean distances between the WiFi fingerprints and the stored radio map is minimized while their relative positions satisfy the geometric constraints?

To show the hardness of the generalized problem in Definition 8.1, we introduce the Quadratic Assignment Problem [4], an NP-hard problem from combinatorial optimization:

Definition 8.2 (Quadratic Assignment Problem) Given a set of n facilities and a set of n locations. For each pair of locations, a distance is specified and for each pair of facilities a weight or flow is specified (e.g., the amount of supplies transported between the two facilities). The quadratic assignment problem is to assign all facilities to different locations with the goal of minimizing the sum of the distances multiplied by the corresponding flows.

Theorem 8.1 The Generalized Problem is at least as computationally hard as Quadratic Assignment Problem. There is no efficient algorithm to solve the Generalized Problem given by Definition 8.1 in polynomial time unless P NP .

Proof We briefly prove the harness of the Generalized Problem by reduction. Suppose there is a polynomial-time algorithm with inputs of the fingerprint database, a set of photos, the corresponding WiFi fingerprints and the geometric constraints among photos. It outputs the location estimates of the photos that minimize the summation of Euclidean distances between the WiFi fingerprints of the photos and those of the location estimates stored in the fingerprint database, without violating the geometric constraints among the photos.

Then this algorithm can be used for solving the Quadratic Assignment Problem by the reductions shown in Table 8.1.

So if we could solve the Generalized Problem in polynomial time, then we would be able to solve the Quadratic Assignment Problem in polynomial time using the reduction, contradicting the fact that Quadratic Assignment Problem is NP-Hard.

Table 8.1 Reduction of quadratic assignment problem to the generalized problem 

<table><tr><td>Quadratic assignment problem</td><td>Generalized problem</td></tr><tr><td>Location</td><td>Candidate location in database</td></tr><tr><td>Facility</td><td>Photo</td></tr><tr><td>Distance among locations</td><td>Euclidian distance of WiFi fingerprints among locations in database</td></tr><tr><td>Flow among facilities</td><td>Geometric constraints among photos</td></tr></table>

![](images/7007fdba2cc7079d01b2867be062be0f9fd006d63a42301a428b29d39fb4ab77.jpg)



![](images/407fae37aaa97c7d52779ac94e95c78ed0f65bf90709bbb4b9c74aa9431e90b5.jpg)



![](images/bf0c7537d33b20b584ffc5ce7511979f0a80892a1bf80d321cb92b72f97f4a13.jpg)



![](images/df8305a05c98430fc479512f10f0c60b09d185925c8bdfe1715fc1fb125b9372.jpg)



(a) Rough Location Estimation by WiFi   
(b) Candidate Polygon Selection by Pruning   
(c) Fine-grained Localization by Interpolation   
Fig. 8.7 Work flow of the two-tier shape matching heuristic algorithm

# 8.7.3 Two-Tier Shape Matching Heuristic

We propose a two-tier shape matching heuristic algorithm to solve the joint location estimation problem. Figure 8.7 shows the work flow of the algorithm. The key steps are summarized as follows:

Step 1: Rough Location Estimation by WiFi Although WiFi fingerprinting cannot provide accurate location estimates, it suffices for a rough location estimate. In most cases, $a _ { i }$ , the location estimated by WiFi, is within a reasonable range (e.g., 10 m) from the true location. Argus utilizes the locations estimated by WiFi fingerprinting as the initial locations for fine-grained localization. Specifically, we assume the true location of i falls into a circle $C _ { i }$ centered at $a _ { i }$ with radius $r _ { i }$ during the searching process in the following steps (Fig. 8.7a). We empirically set $r _ { i }$ the physical distance from $a _ { i }$ to the corresponding fingerprint’s fifth nearest neighbor.

Step 2: Candidate Polygon Selection by Pruning After restricting the search scope of the possible locations for each device, we try every possible combination of training points to form a valid polygon using a pruning strategy (Fig. 8.7b). The criteria for a valid polygon are the same as the constraints of the above optimization, and $\alpha \ = \ 0 . 2$ in this stage. The rationale of the pruning strategy is that, for two combinations of training points $B ^ { * } ~ = ~ \left\{ b _ { 1 } ^ { * } , b _ { 2 } ^ { * } , \ldots , b _ { | V | } ^ { * } \right\}$ and $\boldsymbol { B } ^ { ' } = \left\{ b _ { 1 } ^ { ' } , b _ { 2 } ^ { ' } , \ldots , b _ { | V | } ^ { ' } \right\}$ . If a subset of $B ^ { * }$ already costs more than $B ^ { ' }$ , then the cost of $B ^ { * }$ must be higher than $B ^ { ' }$ . Thus we can sort the training points inside each circle according to its RSS Euclidean distance to the circle center. We try the combination of training points from different circles in a ascending order. Hence we avoid a large amount of impossible polygons and the top 10 polygons are left for fine-grained localization.

Step 3: Fine-grained Localization by Interpolation In practice, the consecutive training points often have a constant interval (e.g., 2 m in our experiment). It is coarse-grained if we limit the user’s position to the training points. So we interpolate the fingerprint space around the top 10 polygons as in Fig. 8.7c. The degree of interpolation depends on specific precision. Then, the newly interpolated points are regarded as the training points and we repeat Step 2 with α = 0.1 to find the polygon minimizing the objective function.

# 8.8 Evaluation

# 8.8.1 Experimental Methodology

Implementation We prototype both the front-end and back-end of Argus. The front-end is implemented as a JAVA extension to the standard Android camera program. The front-end is tested on three types of devices including a Google Nexus 5 phone, a Huawei Honor 2 phone, and a Samsung Note 10.1 tablet. The back-end server is a MacbookPro running Mac OS X 10.9.2, with 2.7 GHz Quad-Core Processor and 16 GB RAM. During the evaluation, the photos and fingerprints are directly uploaded to our server through WiFi connection. We use a mature CV solution SIFT [19] for image feature keypoint extraction. For SfM, we use and modify Bundler [27], an online open source SfM project. Finally we use VisualSFM [31] to validate and visualize the results.

Data Collection We conduct the measurements in two indoor environments including a shopping mall (Fig. 8.8a) and a food plaza (Fig. 8.8b). In each scenario, the WiFi fingerprint database is constructed by on-site survey. We take 10 WiFi fingerprints at each of the training points and the consecutive training points have a distance of 1.8 m. We choose 50 and 41 POIs in the shopping mall and food plaza, respectively, which are marked by pentagrams in Fig. 8.8a, b. For each POI, we take 5–20 photos during the training stage. In total, more than 1000 photos are taken. In addition, we recruit 2 volunteers to take a total of 200 photos from their own perspectives with two guidelines: (1) The POIs should be outstanding physical features that other people may agree with, and (2) the POI should be clearly taken near the middle of viewfinder. The ground truth locations when taking photos were recorded manually.

![](images/47cfa5af6ece21ef99debc140f9a19b39fc82612ce094d9ea9e0c88e43478aca.jpg)



(a)

![](images/35f0ac8c9b7c73e33b01a17ca68cf27109a725ddca13fba1dcef28b71f0ce14e.jpg)



Fig. 8.8 Floor plans of testing scenarios. (a) Shopping mall (b) Food plaza

Table 8.2 Accuracy of image matching 

<table><tr><td>#Candidate POIs</td><td>Shopping mall (%)</td><td>Food plaza (%)</td></tr><tr><td>Top 1</td><td>91.3</td><td>87.2</td></tr><tr><td>Top 2</td><td>95.2</td><td>92.3</td></tr><tr><td>Top 3</td><td>97.4</td><td>94.6</td></tr><tr><td>Top 4</td><td>97.7</td><td>95.8</td></tr><tr><td>Top 5</td><td>97.7</td><td>96.1</td></tr></table>

# 8.8.2 Micro Benchmarks

# 8.8.2.1 Effectiveness of Image Matching

Table 8.2 summarizes the accuracies of image matching. As is shown, although the POI with the highest matching score may not be the correct POI due to e.g. blurred photo or photo taken in dim light, the image matching accuracy boosts significantly if the top 4 POI candidates are returned to the user (97.7% in the mall and 95.8% in the plaza). Therefore, Argus retrieves the top 4 POI candidates and asks the user to identify the correct POI.

# 8.8.2.2 Effectiveness of Geometric Constraint Extraction

To demonstrate the effectiveness of the geometric constraints, we conduct a measurement study in two indoor environments. We take photos of POIs in a shopping mall and a railway station. In each scenario, we choose 7 POIs, and we take 40–120 photos for each POI. We also record the ground truth locations of the photos manually. We randomly pick N photos (3 5) as input for SfM to construct a polygon (geometric constraint), and compare its shape similarity with the ground truth shape. As shown in Fig. 8.9, most shape similarity scores are below 0.5, indicating that the relative positions produced by SfM is qualified for constructing the geometric shape. In addition, note that the shape similarity score distributions of different edges (3, 4 or 5) remain alike. Hence we may extract accurate geometric constraints with few edges (i.e. photos) to reduce computational overhead.

# 8.8.2.3 Effectiveness of Photo Selection

Figure 8.10 shows the distributions of localization errors with and without supporting photo selection. As is shown, the supporting photo selection mechanism constantly picks the more suitable photos for geometric constraint extraction by ensuring that the SfM-generated polygon from supporting photos is highly consistent with the ground truth locations of the supporting photos. Randomly picked photos, in contrast, may not be suitable to be used as a supporting photo either because of the low photo quality or improper shooting angle.

![](images/6fcbf2a3aa6da97884ad3b038916d494ba109f38b78155cf9830c7cb27b3b8f0.jpg)



Fig. 8.9 CDFs of shape similarity score   
![](images/b9886cc98c9260b24046486cffacc4e3b46e8cf94a8d8952bcd4d6c96074a46c.jpg)



(a)

![](images/04ab0dbef637afe618da56f5a6a6766a11cea55addc24ddfcb6cb3cc3b267112.jpg)



Fig. 8.10 Localization accuracy with and w/o photo selection. (a) Shopping mall. (b) Food plaza

# 8.8.2.4 Effectiveness of Device Calibration

Figure 8.11 plots localization accuracy with and without device calibration. As is shown, localization errors reduce by 40% with device calibration to compensate for the difference in RF characteristics among different devices. Hence it is indispensable to take device diversity into account even if WiFi fingerprinting is employed for rough location estimation.

![](images/0ea3233a0102df44d38f5b38607c8a194480d211672b17295536fc756cd25e2d.jpg)



(a)

![](images/7c4eef793b1bb23459669cbb2d3893297804d096d15fc0722d38c9ae475a0893.jpg)



Fig. 8.11 Localization accuracy with and w/o device calibration. (a) Shopping mall. (b) Food plaza   
![](images/48d47b82a5e0fc83943ff132cc5b46e9925d85b4d38979091bb5954f202d213b.jpg)



![](images/6d807fb396ba6111dc82da3899224a099db5bdd4f69127f8702e8188ae49d537.jpg)



(b)   
Fig. 8.12 Overall localization accuracy. (a) Shopping mall. (b) Food plaza

# 8.8.3 Overall System Performance

# 8.8.3.1 Overall Localization Accuracy

To measure the overall localization accuracy, we randomly choose half of the photos taken during the training stage to form the image database and the other half are treated as query images (together with the photos from volunteers). We compare our solution (denoted by Image Assist) with classic RSS-based method RADAR [3] (denoted by WiFi Only and five samples form a query). As shown in Fig. 8.12, the localization accuracy of Argus is consistently tripled. Specifically, the 50-percentile error is reduced from 2.73 to 0.78 m in Mall and from 3.01 to 0.97 m in Plaza. The 80-percentile error is reduced from 4.98 to 1.38 m in Mall and from 5.02 to 2.30 m in Plaza. Such dramatic improvement in localization accuracy demonstrates the effectiveness of geometric constraints extracted from supporting photos in resolving WiFi fingerprint ambiguity.

# 8.8.3.2 System Latency

We evaluate the overall latency by simulating consecutive user queries. We randomly select a photo from the set of query photos and Argus returns the estimated location. Then we average the time delays for 1000 such queries. The time for photo uploading is measured separately by batch. The reason is that we want to measure the time for localization only, without human factors like choosing angle to take photos and checking the localization result. In summary, the file uploading takes 1.8 s and image match module consumes 0.6 s. The photo selection together with constraint generation spends about 3.3 s and the localization algorithm takes another 2.2 s. In parallel, the WiFi fingerprint localization considering the device diversity takes 0.5 s. So in total that is 7.9 s (i.e., 1.8+0.6+max(0.5, 3.3)+2.2). Considering that classic WiFi localization usually takes several samples (e.g., scan 5 WiFi samples in 4.8 s [18]), Argus does not introduce notable latency compared with pure WiFi localization. Eliminating the fingerprint ambiguity by motion usually relies on step detection and particle filter [13], where convergence is not guaranteed.

# 8.8.3.3 Energy Overhead

We evaluate the energy overhead of Argus using the tools and methodology in [37]. We conduct the experiments using Samsung Note 10.1 tablet, and compare the energy consumption in three scenarios: running nothing, WiFi scanning only, and consecutively using Argus. The frequency of WiFi scanning is 2 s, and the screen is active during the experiment to prevent entering the hibernating mode. The power consumptions for the first two modes are 562 and 576 mW, respectively. Then we consecutively use Argus for localization in groups (10 location queries as a group, and 10 groups are measured here). The average lasting time for a group is 159 s and a group consumes 116.6 J, or 733 mW. So Argus consumes 171 mW additional power, which is much less than the average power when the screen is active (562 mW). Since users only activate Argus when in need and the energy consuming operations are left for server, we believe that such overhead has little impact on mobile device’s battery life.

# 8.8.4 Impacting Factors

# 8.8.4.1 Impact of Distance to POIs

As users may take photos from varied distances to the target POI, the distance from the POI when taking the query photo may affect the localization accuracy. Figure 8.13a shows the distances where the photos are taken from the target POIs, which validates the diverse distances when users take photos. Figure 8.13b provides a scatter diagram to illustrate the relationship between the distance and the localization accuracy. As is shown, the distance between the POI and the location where the photo was taken has little impact on the localization accuracy. This is because we only extract relative geometric constraints, which is invariant to scaling.

![](images/6edf4c0bb3f4b5b57ec600031ee99d94992d788a87a515e0e4547a3d3e3fdaf5.jpg)



(a)

![](images/badf4404e9b1593678a5fe75e4e6580f1eba455a0adca75a29f960936afde2ea.jpg)



(b)

Fig. 8.13 Impact of photo distance to POIs. (a) Photo distance distribution. (b) Distance vs. localization error   
![](images/ced5aecedc1536faaed3cc932310b5108c09e7eb90f25cf1e9fed47d63ec94a8.jpg)



(a)

![](images/58f577c027ac133abd9c9bc340a6b3401a97e6d6dd5503c935222627706b591b.jpg)



(b)   
Fig. 8.14 Impact of photo quantity. (a) Shopping mall. (b) Food plaza

# 8.8.4.2 Impact of Quantity of Photos

Intuitively, utilizing more photos of the same POI would contribute to more geometric constraints to eliminate WiFi fingerprint ambiguity. However, more constraints incur more computational overhead to the joint location estimation algorithm. Therefore, we restrict the geometric constraints to polygons with no more than five edges. Figure 8.14 shows the localization accuracy with different number of supporting photos. As expected, more supporting photos result in higher localization accuracy. Yet the gain becomes marginal when the number of edges exceeds five. Therefore we use five-edge polygons as geometric constraints by default.

![](images/6f99c45266529e39547465f38492241b5becf010dbceeada917def0a88b170bb.jpg)



Fig. 8.15 Impact of illumination

# 8.8.4.3 Impact of Illumination

Intuitively, the accuracy of image matching may be sensitive to different illumination conditions. However, according to our experiments, we found that indoor illuminations are relatively stable (since lights are always on). Thus, we simulate illumination change by adjusting the image brightness and contrast. The result is shown in Fig. 8.15. As is shown, Argus is robust to slight illumination change (80% and 120%).

# 8.8.4.4 Impact of Photo Resolution

The cameras on users’ mobile devices may vary in quality and photo resolutions. To emulate the impact of photo resolution, we adjust the level of photographic detail by changing the photo resolution, and repeat the experiment for each resolution level. As shown in Fig. 8.16, Argus is most accurate with original resolution level, with only a slight performance degeneration with fewer photographic detail.

# 8.8.4.5 Impact of Obstacles in Photos

It is unavoidable that the target POI in the photo may be partially sheltered by unexpected obstacles or passengers in a busy indoor environment such as a shopping mall. To evaluate the impact of obstacles, we take 100 photos of a POI, of which 50 are taken when there are passengers passing by the line-of-sight between the user and the POI. As shown in Table 8.3, the mean localization error of Argus degrades from 0.96 to 1.29 m using the 50 photos with human blockage in the photos. A closer analysis of the errors indicate that partially sheltered photos will decrease not only the number of keypoints, but also the number of matched keypoint pairs between the query photo and the supporting photos, thus leading to degradation of localization accuracy. Another finding is that the presence of passengers also affects the accuracy of WiFi fingerprinting, as the movement of passengers will alter the propagations of WiFi signals. However, the degeneration is acceptable as long as the majority of POI is clearly captured.

![](images/3c2f81d4560135e14c48cbd8465a6319f678aed3dfa519b15eab2578d08529c7.jpg)



Fig. 8.16 Impact of resolution

Table 8.3 Impact of humans 

<table><tr><td></td><td>With human</td><td>Without human</td></tr><tr><td>WiFi positioning error</td><td>3.44 m</td><td>2.72 m</td></tr><tr><td>Argus positioning error</td><td>1.29 m</td><td>0.96 m</td></tr><tr><td>Average keypoints</td><td>3995</td><td>4221</td></tr><tr><td>Average matched pairs</td><td>168</td><td>275</td></tr></table>

# 8.9 Discussion

POI Selection In Argus, we assume that users understand which POIs are likely to be selected by the system or other users. During the experiments, we select apparent physical features like logos, shop entrances, and find that 50 POIs are enough for covering the mall and plaza (similar to the result in [8]). However, users may occasionally shoot a POI not in the database and the database may lack of data during the initial stage. In such cases, Argus invites the user as a volunteer to upload photos for the POI (three photos are enough for functioning the POI in Argus), or the user can simply choose to be localized by taking a photo of another POI.

Usage Scenario The design of Argus mainly focuses on large open space (e.g., airports and shopping malls), where most traditional WiFi localization methods provide unsatisfactory performance. Argus may suffer significant performance degradation in boring rooms in office, because we rely on imagery features to extract geometry constraints and it would be difficult for users to select representative POIs inside a boring room. Things may be complicated in campus-like environment. In areas where hallways or small offices dominate, Argus may degenerate to multi-sample WiFi localization. On the other hand, areas where large open space dominates like meeting room and playground are sweet spots for Argus. In addition, Argus relies on established WiFi fingerprint database and does not provide continuous localization when the user is moving. We are seeking the solution to inferring user motion by combining other techniques (e.g., dead-reckoning and particle filter [13, 34]).

Reasons of Large Errors Though Argus triples the localization accuracy of traditional RSS-based localization method, large errors do exist (e.g., 25 queries have error larger than 5 m in Overall Localization Accuracy as in Fig. 8.13b). By examining the 25 queries, we summarize the reasons of large errors as: low quality WiFi sample(14), extreme distances or angles(5), similar appearance of POI(4), and obstruction of POI(2). Low quality WiFi samples and query photos lead to large localization error. However, we believe that some large errors can be avoided when either WiFi sample and query photo is in high quality and we plan to improve our photo selection mechanism in future work.

# 8.10 Conclusion

With the trends towards enhanced wireless connectivity, improved imaging technique, and adoption of the cloud for low-cost, scalable computation, we envision widespread user-friendly indoor location-based service. We developed Argus, an image-assist indoor localization system utilizing geometric constraints from crowdsourced images. Argus makes it possible to localize accurately and efficiently with a single click. Experiments show that Argus localizes users in comparable time with classic RSS-based methodologies while triples the localization accuracy.

# References

1. Arkin, E.M., Chew, L.P., Huttenlocher, D.P., Kedem, K., Mitchell, J.S.: An efficiently computable metric for comparing polygonal shapes. IEEE Trans. Pattern Anal. Mach. Intell. 13(3), 209–216 (1991)   
2. Azizyan, M., Constandache, I., Roy Choudhury, R.: Surroundsense: mobile phone localization via ambience fingerprinting. In: Proceedings of ACM MobiCom (2009)   
3. Bahl, P., Padmanabhan, V.N.: Radar: An in-building RF-based user location and tracking system. In: Proceedings of IEEE INFOCOM (2000)

4. Burkard, R.E., Cela, E., Pardalos, P.M., Pitsoulis, L.S.: The quadratic assignment problem. In: Du, D.-Z., Pardalos, P.M. (eds.) Handbook of Combinatorial Optimization, pp. 1713–1809. Kluwer Academic, Boston (1998)   
5. Cheng, L., Wu, C.D., Zhang, Y.Z.: Indoor robot localization based on wireless sensor networks. IEEE Trans. Consum. Electron. 57(3), 1099–1104 (2011)   
6. Dong, J., Xiao, Y., Noreikis, M., Ou, Z., Ylä-Jääski, A.: iMoon: using smartphones for imagebased indoor navigation. In: Proceedings of ACM SenSys, pp. 85–97 (2015)   
7. Fang, S.H., Wang, C.H., Chiou, S.M., Lin, P.: Calibration-free approaches for robust Wi-Fi positioning against device diversity: a performance comparison. In: Proceedings of IEEE VTC (2012)   
8. Gao, R., Tian, Y., Ye, F., Luo, G., Bian, K., Wang, Y., Wang, T., Li, X.: Sextant: towards ubiquitous indoor localization service by photo-taking of the environment. IEEE Trans. Mob. Comput. 15(2), 460–474 (2016)   
9. Gao, R., Zhao, M., Ye, T., Ye, F., Luo, G., Wang, Y., Bian, K., Wang, T., Li, X.: Multi-story indoor floor plan reconstruction via mobile crowdsensing. IEEE Trans. Mob. Comput. 15(6), 1427–1442 (2016)   
10. Gu, Y., Lo, A., Niemegeers, I.: A survey of indoor positioning systems for wireless personal networks. IEEE Commun. Surv. Tutorials 11(1), 13–32 (2009)   
11. He, S., Chan, S.H.G.: Wi-Fi fingerprint-based indoor positioning: recent advances and comparisons. IEEE Commun. Surv. Tutorials 18(1), 466–490 (2016)   
12. He, S., Chan, S.H.G., Yu, L., Liu, N.: Fusing noisy fingerprints with distance bounds for indoor localization. In: Proceedings of IEEE INFOCOM, pp. 2506–2514 (2015)   
13. Hilsenbeck, S., Bobkov, D., Schroth, G., Huitl, R., Steinbach, E.: Graph-based data fusion of pedometer and WiFi measurements for mobile indoor positioning. In: Proceedings of ACM UbiComp, pp. 147–158 (2014)   
14. Jun, J., Gu, Y., Cheng, L., Lu, B., Sun, J., Zhu, T., Niu, J.: Social-loc: improving indoor localization with social sensing. In: Proceedings of ACM SenSys, pp. 14:1–14:14 (2013)   
15. Kjærgaard, M.B.: Indoor location fingerprinting with heterogeneous clients. Elsevier Trans. Pervasive Mob. Comput. 7(1), 31–43 (2011)   
16. Koenderink, J.J., Van Doorn, A.J., et al.: Affine structure from motion. J. Opt. Soc. Am. A 8(2), 377–385 (1991)   
17. Li, L., Shen, G., Zhao, C., Moscibroda, T., Lin, J.H., Zhao, F.: Experiencing and handling the diversity in data density and environmental locality in an indoor positioning service. In: Proceedings of ACM MobiCom (2014)   
18. Liu, H., Yang, J., Sidhom, S., Wang, Y., Chen, Y., Ye, F.: Accurate WiFi based localization for smartphones using peer assistance. IEEE Trans. Mob. Comput. 13(10), 2199–2214 (2014)   
19. Lowe, D.G.: Distinctive image features from scale-invariant keypoints. Springer Int. J. Comput. Vis. 60(2), 91–110 (2004)   
20. Lymberopoulos, D., Liu, J., Yang, X., Choudhury, R.R., Handziski, V., Sen, S.: A realistic evaluation and comparison of indoor location technologies: experiences and lessons learned. In: Proceedings of ACM IPSN, pp. 178–189 (2015)   
21. Mahtab Hossain, A., Jin, Y., Soh, W.S., Van, H.N.: SSD: a robust RF location fingerprint addressing mobile devices’ heterogeneity. IEEE Trans. Mob. Comput. 12(1), 65–77 (2013)   
22. Manweiler, J.G., Jain, P., Roy Choudhury, R.: Satellites in our pockets: an object positioning system using smartphones. In: Proceedings of the ACM MobiSys (2012)   
23. Mautz, R., Tilch, S.: Survey of optical indoor positioning systems. In: Proceedings of the IPIN (2011)   
24. Park, J.G., Curtis, D., Teller, S., Ledlie, J.: Implications of device diversity for organic localization. In: Proceedings of the IEEE INFOCOM (2011)   
25. Sattler, T., Leibe, B., Kobbelt, L.: Fast image-based localization using direct 2d-to-3d matching. In: Proceedings of the IEEE ICCV (2011)   
26. Sen, S., Radunovic, B., Choudhury, R.R., Minka, T.: You are facing the Mona Lisa: spot localization using phy layer information. In: Proceedings of the ACM MobiSys, pp. 183–196 (2012)

27. Snavely, N., Seitz, S.M., Szeliski, R.: Photo tourism: exploring photo collections in 3D. ACM Trans. Graph. 25(3), 835–846 (2006)   
28. Sorour, S., Lostanlen, Y., Valaee, S., Majeed, K.: Joint indoor localization and radio map construction with limited deployment load. IEEE Trans. Mob. Comput. 14(5), 1031–1043 (2015)   
29. Sun, W., Liu, J., Wu, C., Yang, Z., Zhang, X., Liu, Y.: MoLoc: on distinguishing fingerprint twins. In: Proceedings of the IEEE ICDCS, pp. 226–235 (2013)   
30. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: Proceedings of the ACM MobiSys (2012)   
31. Wu, C.: Towards linear-time incremental structure from motion. In: Proceedings of the IEEE 3DV (2013)   
32. Xie, H., Gu, T., Tao, X., Ye, H., Lv, J.: MaLoc: a practical magnetic fingerprinting approach to indoor localization using smartphones. In: Proceedings of the ACM UbiComp (2014)   
33. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Indoor localization via multi-modal sensing on smartphones. In: Proceedings of the ACM UbiComp, pp. 208–219 (2016)   
34. Yang, Z., Wu, C., Zhou, Z., Zhang, X., Wang, X., Liu, Y.: Mobility increases localizability: a survey on wireless indoor localization using inertial sensors. ACM Comput. Surv. 47(3), 54 (2015)   
35. Ye, X., Wang, Y., Hu, W., Song, L., Gu, Z., Li, D.: Warpmap: accurate and efficient indoor location by dynamic warping in sequence-type radio-map. In: Proceedings of the IEEE SECON, pp. 1–9 (2016)   
36. Youssef, M., Agrawala, A.: The Horus WLAN location determination system. In: Proceedings of the ACM MobiSys (2005)   
37. Zhang, L., Tiwana, B., Qian, Z., Wang, Z., Dick, R.P., Mao, Z.M., Yang, L.: Accurate online power estimation and automatic battery behavior based power model generation for smartphones. In: Proceedings of the IEEE/ACM/IFIP CODES+ISSS (2010)

# Chapter 9 Mitigating Large Errors in Practice

![](images/db4c859f456c911b8e730ed4db9ef88a301099b1cf12ec303b518506e4d09a8c.jpg)

Abstract In this chapter, we reveal crucial observations, through real-world experience, that act as the root causes of localization errors, yet are surprisingly overlooked or not adequately addressed in previous works. Specifically, we recognize Access Points’ diverse discrimination for fingerprinting a specific location, observe the RSS inconsistency caused by signal fluctuations and human body blockages, and uncover the transitional fingerprint problem on commodity smartphones. Inspired by these insights, we devise and evaluated several techniques in a unified system, DorFin, with a novel scheme of fingerprint generation, representation, and matching. Our design provide insights to practical indoor localization system designs.

# 9.1 Introduction

There is generally a tradeoff between accuracy, ubiquity, and cost in designing a pervasive indoor localization system. Accuracy has long been the primary challenge especially in mobile environments. Even schemes that have been reported to have very high accuracy in some instances, e.g., [13, 22, 43], can experience rapid performance degradation in realistic environments, with median error consistently above 5 m [32]. In addition, there are always unacceptably large tail errors, e.g., 10∼20 m or larger. Recent works [16, 32] found that large errors of prior works could range from 12 to around 40 m. Mobility further deteriorates the performance especially for smartphone based methods. Efforts to gain high accuracy include to leverage physical layer information [26] and incorporate acoustic ranging [15, 16], among others. Despite of the notable improvements, these methods typically either rely on information unavailable on commodity smartphones, or resort to unrealistic cooperation among a dense crowd of peers, and WiFi fingerprinting is usually employed as a fundamental module [39]. Hence any improvement on WiFi fingerprinting itself is of great significance and is usually not conflict but complementary to enhancements by additional information [8, 12, 29]. In this chapter, we investigate to mitigate large errors for WiFi fingerprinting and achieve accurate and robust localization, especially for mobile phones, without degrading the ubiquity or increasing the costs.

To investigate the potential causes of limited localization accuracy in practice, we conduct extensive experiments and uncover or revisit the following characteristics of WiFi fingerprint-based localization: (1) APs have different discriminatory capabilities to fingerprint a specific location since RSS changes are inversely proportional to the physical distance, subject to radio signal propagation laws. Intuitively, faraway APs may lead to large location estimation errors while close ones can help mitigate the location uncertainty. (2) Biased RSS measurements caused by signal fluctuation and human body blockage may present themselves as outliers in fingerprint matching. Human body blockage to smartphones can remove line-ofsight and weaken the received signal by up to 10 dB, thus greatly exaggerating the discrepancies of fingerprints measured from the same location. (3) The real-time measured RSS values may be in fact outdated due to incomplete scan by hardware and software limitations of commodity wireless devices. In other words, latest reported RSS values could be cached duplicates of previous scans performed several seconds ago, as we call outdated RSS. Considering user mobility, the outdated RSSs could actually be measurements done at a previous location, which result in transitional fingerprint, i.e., a patchwork of the up-to-date RSSs of the current location and the cached RSSs of the past locations. In overlooking such farraginous information, previous works directly compare the transitional fingerprints with those collected at a single location, incurring frequent fingerprint mismatches. The above are key reasons behind location errors of fingerprint-based schemes, especially in mobile environments; yet surprisingly they have not been adequately addressed in existing works (in spite that some of them, e.g., AP quality and body blockage, have been noticed previously [2, 7]).

With these observations in mind, we design DorFin (named after Discrimination diversity, Outdated RSS, and Fingerprint inconsistency), an accurate and robust fingerprint-based scheme that unleashes the true potential of WiFi-based localization for smartphone applications. DorFin includes three main components. First, we quantitatively differentiate distinct AP’s discriminatory ability w.r.t. a specific location. APs with stronger ability are emphasized with more weights in fingerprint matching, while others are de-emphasized. Second, noting fingerprint inconsistency, we apply a robust regression technique in fingerprint matching identify and mitigate those outlying RSS values, in the hope of ensuring accuracy under noisy measurements. Finally, we propose phantom fingerprints that incorporate multiple normal fingerprints in the fingerprint database to deal with the transitional fingerprints. Phantom fingerprints are assembled according to the specific geometrical constraints of outdated RSSs, which are derived by monitoring user mobility using smartphones’ built-in inertial sensors. Integrating these components, we design a uniform fingerprint similarity metric which further takes account of common AP ratio as a factor to mitigate erroneous matches of distant fingerprints.

To validate our design, we implement DorFin on commodity devices and conduct extensive experiments in three campus buildings. We also employ two classical [1, 43] and two latest [11, 18] approaches for comparison. Experimental results demonstrate competitive performance of DorFin even to solutions based on additional ranging techniques. In addition to the average accuracy of 2.5 m,

DorFin significantly reduces large location errors by limiting the 95 percentile errors in 6.2 m, both outperforming all comparison approaches by at least 34% and 21%, respectively. Using only the most essential RSS, the proposed approach requires no extra hardware and is amendable to general fingerprint-based framework as well as mutually beneficial and complementary to existing or upcoming augmentations based on inertial sensors, acoustics, images or others [16, 34, 39]. We envision our approach as an important step towards accurate location estimation on smartphones with the prevalent WiFi infrastructure.

The rest of the chapter is organized as follows. We discuss the state-of-the-art of indoor localization in Sect. 9.2. Section 9.3 presents our preliminary measurements and basic observations. The method design is detailed in Sect. 9.4, followed with the experiments and performance evaluation in Sect. 9.5. We conclude the chapter in Sect. 9.6.

# 9.2 Related Works

In the literature of indoor localization, many techniques have been proposed in the past two decades. A large body of indoor localization approaches adopts fingerprint matching as the basic scheme for location estimation. Researchers have explored diverse signatures including WiFi [43], RFID [20], acoustic [31], etc. Among various signatures used, WiFi based scheme has been the most attractive.

Smartphones with various built-in sensors have been leveraged in fingerprintbased localization to reduce or eliminate site survey efforts. Examples include LiFS [36], unloc [34], Zee [22], Walkie-Markie [28], etc. They typically combine user mobility with extra information like digital floor plan [22, 36] or indoor landmarks [34] and usually can only handle mobile trajectories [28]. As these works mainly focus on easing the site survey in the training phase, DorFin is orthogonal to them in targeting at fingerprint matching of the online phase to improve localization accuracy. Nevertheless, DorFin is also compatible to crowdsourced fingerprint database constructed via these schemes.

Pursuing better accuracy, sophisticated probability models and advanced machine learning techniques have been employed [42, 44]. The study [32] validates a broad range of approaches in a realistic environments and reports that median errors of prior work are consistently greater than 5 m and, counter-intuitively, that simpler algorithms frequently outperform more sophisticated ones. Realizing that large errors always exist due to possibly faraway locations with similar WiFi signatures, authors in [16, 19] attempt to incorporate acoustic ranging in WiFi fingerprinting to limit the large tail errors. Although significant improvements are achieved, these approaches either rely on ranging among a dense crowd of users or require calibrating additional information. Recent works also explore new fingerprint features such as neighbour relative RSSs [14], neighbour RSS gradient [29] and RSS ratio over multiple antennas [3] for accurate and robust fingerprinting. To completely bypass the instability of RSS, physical layer Channel

State Information (CSI) is recently introduced and achieves an accuracy of 1 m [26], but at the cost of ubiquity degradation (since CSI is unavailable on most commodity smartphones).

To reduce computational complexity, d Different criteria for AP’s discriminatory ability such as InfoGain [2] and MaxMean [44] have been proposed to choose a subset of APs for localization. A more intuitive method called RSS cutoff, i.e., discarding RSS values below a specific threshold, is preferred in commercial products [4]. These methods conduct AP selection mainly to reduce the computational complexity. In contrast, we target at appropriately exploiting all available APs for more accurate fingerprint matching. Accounting for human body blockage, fingerprints are typically collected for multiple directions [21], which may increase labour efforts while offers limited gains. An elaborate model is designed in [6] to compensate for the signal attenuation of human body and thus generate orientationindependent fingerprints from measurements on just one orientation. In contrast to labour-intensive measurements or vulnerable models, we resort to exploit robust regression techniques to achieve effective robustness to RSS uncertainties.

Different from previous works that introduce additional information or extra signal sources for high accuracy, we identify several causes of location errors in practice in WiFi fingerprint-based localization for mobile devices. Specifically, we uncover and solved the transitional fingerprint problem, which has not been noticed in existing works. Aiming at a ubiquitous location service, we follow a typical RSS fingerprint-based scheme to design DorFin, which is thus amendable to integrate with existing approaches and can be easily incorporated in deployed systems with little efforts, making it a promising scheme in practical applications.

# 9.3 Preliminary and Measurements

In this section, we review the classical RSS fingerprinting problem and investigate fundamental characteristics of radio fingerprints through real measurements. Our preliminary results show some crucial features, which, having been largely overlooked in the past, shed light on how to achieve high accuracy of fingerprint-based localization.

# 9.3.1 Problem Statement

The working process of a typical fingerprint-based localization scheme consists of two stages: site survey and fingerprint matching. During site survey, wireless fingerprints (i.e., the set of RSS values from multiple APs) are measured and recorded at every location of interests. A fingerprint database (a.k.a radio map) is accordingly constructed, in which the fingerprint-location relationships are stored. To locate a user who sends a location query with his current RSS fingerprint, localization algorithms retrieve the fingerprint database and return the location of the matched fingerprint as the user’s location estimation.

Denote a fingerprint as $f = [ f _ { i } , i = 1 , \cdots , n ]$ , where $f _ { i }$ is the RSS value of the AP $A _ { i } \in { \mathcal { A } } .$ , the set of n detectable APs appearing in $f .$ . For two fingerprints $f$ and $f ^ { \prime }$ , denote the RSS difference (RSD) vector as $\pmb { \delta } = [ \delta _ { i } , i = 1 , \cdots , p ]$ where $\delta _ { i } = | f _ { i } - f _ { i } ^ { \prime } |$ indicates the RSD of AP $A _ { i } \in \mathcal { A } \cup \mathcal { A } ^ { \prime }$ in the two fingerprints and $p = | \mathcal { A } \cup \mathcal { A } ^ { \prime } |$ . Since the sample fingerprint $f$ and query one $f ^ { \prime }$ do not necessarily contain identical sets of APs, we set $f _ { i } \ ( f _ { i } ^ { \prime } )$ to 100, the default minimum RSS value, if $A _ { i } \notin \mathcal { A } \left( \mathcal { A } ^ { \prime } \right)$ . By doing this, we can always obtain an extended version of fingerprint that contains $p$ effective APs for a couple of any sample and query fingerprint. Let $\phi$ be the dissimilarity between $f$ and $f ^ { \prime }$ , which, if measured by Euclidean distance, can be calculated as $\begin{array} { r } { \phi ( \pmb { f } , \pmb { f ^ { \prime } } ) = \| \pmb { \delta } \| = \sqrt { \sum _ { i = 1 } ^ { p } \delta _ { i } ^ { 2 } } } \end{array}$ . For all fingerprints stored in the fingerprint database $\mathcal { F }$ , the goal of fingerprint matching is to find the fingerprint $f ^ { * }$ that achieves the highest similarity with respect to the query fingerprint $f$ . Formally,

$$
\boldsymbol {f} ^ {*} = \underset {\boldsymbol {f} _ {i} \in \mathcal {F}} {\arg \min} \phi (\boldsymbol {f}, \boldsymbol {f} _ {i}). \tag {9.1}
$$

Then the user’s location is estimated as the corresponding location $l ( f ^ { * } )$ of $f ^ { * }$ . Assuming the true location of $f$ is $l ( f )$ , the location estimation error is given by $\varepsilon = \| l ( f ) - l ( f ^ { * } ) \|$ .

# 9.3.2 Observations

Observation 1 (Discrimination Diversity) APs have diverse discrimination capability to fingerprint a specific location, subject to inherent constraints of radio signal propagation.

We term Discrimination capability as the ability of one AP to distinguish a specific location when including its RSS observations in the location’s fingerprint. Ideally, subject to the propagation law of wireless signals, RSS decays logarithmically with propagation distance $d .$ . More formally, $R S S \propto - \log ( d )$ , indicating that $\frac { \Delta \bar { R } S S } { \Delta d } \propto$ $- { \frac { 1 } { d } }$ , where $\varDelta R S S$ denotes the RSS change and Δd is the corresponding distance change. In other words, an identical $\varDelta R S S$ can imply a smaller distance change $\varDelta d$ at closer locations, or a larger $\varDelta d$ at faraway positions. Figure 9.1a depicts the illustrative RSS spatial distribution of two APs. As seen, an RSS variance of 1 dB in value corresponds to vastly different changes in physical distance, depending on the specific d. Specifically, faraway APs may contain larger uncertainties in location determination than closer APs. In a nutshell, distance changes indicated by RSS variances depend on the transmitter-receiver distance, leading to diverse discrimination capability across different locations.

Several previous works perform AP selection to deal with AP diversity. A subset of APs are chosen for location estimation using either specifically defined complex metrics or just RSS cutoff [2, 4]. As is pointed out in [5], AP selection is data dependent and thus the selected APs may not always be the most discriminative ones due to significant RSS fluctuations indoors. Hence selecting only a portion of APs and discarding the others may not be the best way to deal with the discrimination diversity, leaving a room for further improvements.

![](images/3f246b3e1bc33e1af15b833cc9825764ec049c4937ae0dff73a82ff46f0f3b2e.jpg)



(a)

![](images/337fdef30b2a7320105582acf5bbdece9e9a7f1319d4e5c6e050314593380ddb.jpg)



![](images/86754dd52646d78cc354a0aef51be3db3c1f3470fe1cff134ad79f3fb50da493.jpg)



Fig. 9.1 Observations on sources of large location errors in WiFi fingerprinting. (a) Discrimination diversity. (b) Fingerprint Inconsistency. (c) Transitional fingerprints

Observation 2 (Fingerprint Inconsistency) The majority of APs hold similar RSSs for fingerprints from the same/close locations while a small fraction may exhibit large differences due to environmental dynamics and human body blockages.

Location errors originate from unmatched fingerprints measured from the same/close locations. Our investigation on these fingerprints indicate that a majority of APs exhibit relatively stable RSSs even when these fingerprints are not matched. That is to say, the fingerprint dissimilarity (under certain metric such as Euclidean distance) is primarily produced by the drastically fluctuating RSSs of a small portion of APs, which is, however, obviously not caused by location changes, but probably stems from ambient dynamics and human body blockages [35, 45] especially in mobile environments.

As shown in Fig. 9.1b, signal strengths perceived by smartphones decrease significantly when the human body blocks the direct path of signal propagation, compared to when the user is facing the AP. These weakened RSS observations of blocked APs tend to deviate from the normal profiles, resulting in abnormal RSSs when compared with fingerprints measured during the training phase. Taking Fig. 9.1b as an example, the normal RSS profile absent of body blockage is measured to be $f = [ - 4 0 , - 6 5 , - 5 0 ]$ . When a user is present and faces left, the right AP is blocked, resulting in a biased fingerprint $f _ { \mathrm { l e f t } } = [ - 4 0 , - 6 5 , - 6 5 ]$ (for simplicity, we assume RSSs of unblocked APs remain unchanged). When facing right, the line of sight of the left AP is blocked and its RSS is correspondingly weakened, creating a fingerprint $f _ { \mathrm { r i g h t } } = [ - 5 2 , - 6 5 , - 5 0 ]$ . Then comparing $f _ { \mathrm { l e f t } }$ and $f _ { \mathrm { r i g h t } }$ with the normal f produces inconsistent RSD distributions $\delta _ { \mathrm { l e f t } } = [ 0 , 0 , 1 5 ]$ and $\delta _ { \mathrm { r i g h t } } = [ 1 2 , 0 , 0 ]$ , both generating abnormally larger fingerprint dissimilarity and ultimately leading to greater location uncertainty.

To tackle with such inconsistency, previous works typically collect orientationdependent fingerprints for multiple directions [6, 21], but this requires high labour efforts while offers limited gains. Furthermore, the one-time constructed fingerprints are vulnerable to environmental changes, leading to degraded performance over time. Some recent solutions incorporate direction information in the fingerprint database [30] or resort to peer-assisted acoustic ranging among multiple phones [16, 19]. The former increases the costs of fingerprint constructions, while the latter relies on cooperation among multiple users, rendering it impractical. Probabilistic schemes [42, 44] have been designed to tolerate RSS variations by modeling the RSS distributions from sufficient number of samples. In contrast, we aim to identify and mitigate them.

Observation 3 (Transitional Fingerprint) The real-time reported RSS values might be outdated due to incomplete scanning results, caused by software and hardware restrictions.

The incomplete scan phenomenon is a widely existed yet surprisingly overlooked problem on off-the-shelf devices due to the wireless protocol and hardware capability limitations. Figure 9.1c illustrates a glance of scanning results from mobile devices running the Android OS. Commodity smartphones acquire WLAN information in a passive scanning mode by listening to periodic beacons from surrounding APs on all working channels. In this mode, the time a client stays on a channel is 100 ms by default, which is specified by the 802.11 standard [10] and is equal to the default beacon interval. Consequently, the latency incurred in capturing the AP information for 2.4 GHz WiFi is about 1,100 ms since there are 11 available channels. In practice, it takes about 1 1.5 s for mainstream Android OS to complete a scan with commodity smartphones. Due to beacon conflicts and channel collisions, the beacon interval of 100 ms cannot be always guaranteed, potentially resulting in some missed APs during a scan. However, to maintain quality of service, these missed APs can still appear in the scanning results by duplicating information from last several scans a few seconds ago. As shown in Fig. 9.2, a significant portion of APs experience high outdated rates, ranging from 2% to 25%. In particular, about 60% of the outdated RSSs bear an outdated delay of 1.4 s, while around 20% and 15% has a delay of 2.7 and 4 s, respectively. Translated into fingerprints, Fig. 9.2c indicates that over 80% of fingerprints contain outdated RSSs, and for about 20% the maximum delay time exceeds 4 s. Similar phenomenon is observed on various commodity devices including smartphones and pads such as Google Nexus S and Nexus 4, LG D820, and Samsung T210, and laptops such as Lenovo T430s and X1 Carbon.

![](images/c2c544fd237f778058cbb0b45a730e875657df3b7f3e3fa3b524732619c8f8c7.jpg)



![](images/524e0dc4770676f0acb57cba5b89c680d709d151bc1caa95fed43d4557f2a9de.jpg)



![](images/594ac961131c22884711c81a3e9927a9a11f3d85b2dba34b5ea2274fde9e355b.jpg)



Fig. 9.2 Outdated RSS phenomenon: the real-time reported RSSs in one fingerprint might be outdated due to incomplete scan. (a) Outdated rates over different APs. (b) Time delays of outdated RSS. (c) Time delays in transitional fingerprints

If a user is stationary, such outdated RSS problem has little impact on location fingerprinting since the cached RSSs are also measured from the same position within a short period of time (less than a few seconds). In mobile environments, however, users may have moved several meters away between consecutive scans, resulting in a fingerprint comprised by RSS values that are actually observed at multiple locations, which we call transitional fingerprint. A transitional fingerprint is a patchwork of the up-to-date RSSs of the current location and the cached RSSs of past locations. Previous works treat these spatially mixed fingerprints as normal ones and directly compare them to those stored in the fingerprint database, which are all collected at single locations. Obviously, matching fingerprints mixed from multiple locations to those from single positions may result in frequent fingerprint mismatches or even localization failures.

Note that the transitional fingerprint problem is very different from the conventionally denoted out-of-date fingerprints, which refer to fingerprints that were collected a considerably long period of time ago [41]. The out-of-date fingerprints are typically the results of RSS variants due to environment dynamics and usually will be deprecated or adapted to date for localization [41]. The transitional fingerprint problem, however, is an intrinsic, environment-irrelevant issue subjected to prevalent WiFi and commercial hardware specifications in mobile contexts, which usually occurs within a short time period of a few seconds. To the best of our knowledge, this problem has not been noticed before. Previous solutions [9] for mobile users utilize information from the past to come up with better disambiguation of candidate user locations, which potentially leverage physical constraints imposed by user movements and thus are completely different from and orthogonal to our consideration. More importantly, previous works treat the entire fingerprint as a basic unit and consider only the time domain. In contrast, we focus on each RSS component that composes the fingerprint, and investigate the spatial relationships between them caused by incomplete scan and user mobility.

Either having been noticed or not in the literature, the above-mentioned problems have not been adequately resolved. In this study, we reconsider the RSS fingerprinting scheme based on these significant observations to mitigate large location errors for smartphone localization.

# 9.4 Design Methodology

By designing DorFin, we do not target at providing the most accurate solution for indoor localization among all existing techniques such as those based on RFID [33], PHY layer information [27], acoustic ranging [15], etc., but attempt to explore the true potential of pure WiFi fingerprint based localization scheme. DorFin is designed as an amendable technique that can be widely incorporated in various existing or upcoming WiFi-based solutions. Pursuing this goal, we do not resort to any extra information except for involving inertial sensing for mobility monitoring in DorFin. As illustrated in Fig. 9.3, the proposed solution includes a phantom fingerprint assembling module, a robust regression procedure and a discriminatory policy, unified in a normal fingerprint matching scheme.

Fig. 9.3 System architecture   
![](images/54da381cfecac882bb0bd78c8563ce01a3bbdac7613f9088d43d8beeba733b1c.jpg)



# 9.4.1 Phantom Fingerprints

An intuitive way to overcome transitional fingerprint problem is to recognize and discard the outdated entities before fingerprint matching. However, as indicated in Fig. 9.2, a significant portion of APs bear outdated RSSs. Discarding all of them may degrade the performance of localization since larger number of APs can typically result in better accuracy [5, 30].

In contrast, one query fingerprint consisting of RSSs observed at multiple locations should be matched with fingerprints recombined by measurements from those locations, which, however, are not directly available in the fingerprint database. In this sense, one needs to assemble special fingerprints, i.e., combinations of fingerprints from multiple locations, for matching, as shown in Fig. 9.4. These newly constructed fingerprints do not yet exist in the fingerprint database, and are referred to as phantom fingerprints.

For a fingerprint $f = [ f _ { i } , i = 1 , \cdots , n ]$ , denote the encountered timestamp of each AP $A _ { i }$ in f by $t _ { i }$ . Recall Fig. 9.1c, the scanning delay is typically longer than 1 s by our measurements while the differences of all APs’ detected time in one fingerprint are usually small (indicated by the Time Synchronization Function timestamp provided by the Android OS). Hence, if the time difference between two APs in one fingerprint exceeds a certain value, e.g., 0.5 s, then the earlier one is definitely outdated. In particular, for $\mathsf { A P } A _ { k }$ , the outdated duration $\varDelta t _ { k }$ is computed by $\varDelta t _ { k } = \operatorname* { m a x } _ { i = 1 , \cdots , n } t _ { i } - t _ { k }$ .

Fig. 9.4 Phantom fingerprint   
![](images/1938bdd8262b9d0308f56010731bbb708ac0f161615f0b8ae4cde89d2ccec701.jpg)



As illustrated in Fig. 9.4, assume that $f _ { k }$ is actually the measurement of $A _ { k }$ at a previous location, called bequeathal location (BL), where a user was present $\varDelta t _ { k }$ seconds ago. Further assume that the distance and direction from the BL to the user’s current location is $\ell _ { k }$ and $\theta _ { k }$ , respectively (we will describe how to compute $\ell _ { k }$ and $\theta _ { k }$ shortly). Then when comparing f with a candidate location, say, $l _ { z }$ , instead of directly computing the dissimilarity between $f$ and $f _ { z } ,$ a sample fingerprint of $l _ { z }$ , we match it against the phantom fingerprints $\pmb { \mathscr { f } } _ { z }$ assembled from $f _ { z }$ and $f _ { B L ( z ) }$ , fingerprint from the BL. Concretely, the RSS value $f _ { k }$ in $f$ is replaced by that of the same AP in $f _ { B L ( z ) }$ . Considering there would generally be temporal RSS samples from AP $A _ { k }$ , we replace all its raw RSS observations with those from the BL and then accordingly regenerate a new version of fingerprint. In case of outdated RSSs from multiple APs, all of them are replaced according to their individual BLs, finally resulting in a precise phantom fingerprint $\pmb { \mathscr { f } } _ { z }$ .

The distance offset  and direction θ can be estimated by dead reckoning method using smartphone built-in inertial sensors like accelerometer, gyroscope, and compass [22, 28, 34]. Specifically, we adopt the method proposed in [38], which counts steps as accurately as up to 98%, regardless of the phone attitudes. The footsteps could then be converted to physical displacement by multiplying with the user’s step length, which can be automatically tracked [22]. The direction, on the other hand, is estimated using gyroscope and compass as [22]. In the following, we demonstrate that although dead-reckoning may not always be adequate for localization, it is sufficient for our purpose of estimating  and θ. Note that we merely involve inertial sensing to monitor short distance movements, but do not resort to extra information such as a detailed digital floor plan that is required by previous works like Zee [22].

Due to noisy sensors and arbitrary human behavior,  and θ cannot be 100% accurately computed. To cope with the erroneous estimations, we introduce an error range for each of them, denoted as $\varDelta \ell$ and $\varDelta \theta$ , respectively, and demonstrate that the procedure of choosing BLs can tolerate these errors gracefully. Mathematically, as shown in Fig. 9.5, potential BLs need to satisfy the condition that their distances and directions to the candidate location are bounded in $[ \ell - \varDelta \ell , \ell + \varDelta \ell ]$ and $[ \theta -$ $\varDelta \theta , \theta + \varDelta \theta ]$ , respectively. The size of the shaded area is $S = \varDelta \theta \bigl ( ( \ell + \varDelta \ell ) ^ { 2 } - ( \ell -$ $\Delta \ell ) ^ { 2 } \big ) = 4 \Delta \theta \ell \Delta \ell .$ . Assuming a location sample density of $2 \times 2$ m and $\varDelta \ell \leq 2  { \mathrm { m } }$ , the minimal size $S _ { 0 }$ to cover two sample locations should be at least $4 \varDelta \ell \mathrm { m } ^ { 2 }$ . Thus, if $\varDelta \ell \leq 2$ m and $\varDelta \theta < 1 / \ell$ , we have $S < S _ { 0 }$ , which means the shaded area covers at most one sample location, i.e., there is only one candidate BL. In practice, the maximal value of the missing delay $\varDelta t$ is less than 5 s (APs not seen for more than $5 \mathrm { s }$ would no longer be reported until being detected again next time). Thus, assuming a normal walking speed of $1 . 2 \mathrm { m } / \mathrm { s }$ , the distance offset can be at most 6 m, resulting in a minimum value of $1 / \ell$ of ${ \frac { 1 } { 6 } } .$ . In other words, even though the distance and direction estimations are erroneous, we could identify a suspicious area and, with high probability, there is only one possible BL in the area, as long as the errors are in certain ranges $( \varDelta \ell \leq 2$ m and $\begin{array} { r } { \bar { \Delta } \theta \ < \ \frac { 1 } { 6 } ) } \end{array}$ . In case of multiple BLs (which is rare based on our measurements), the one closest to the center of the suspicious area (the shaded area shown in Fig. 9.5) is selected. Phantom fingerprints are then constructed by combining fingerprints from the candidate location and those from the BLs, i.e., substituting the tuples corresponding to the outdated RSSs, as shown in Fig. 9.4.

Fig. 9.5 Bequeathal locations   
![](images/c9685519e6c8cf0dc3cd35d1082689fb5e44b3d6c2421b7c598f7022babfe6f8.jpg)



According to specific location sampling density, not all outdated RSSs need to be replaced. Only RSSs with distance offsets  exceeding half of the unit length of sampling grids should be replaced. If  is less than half of the sampling distance (including being equal to 0 which means static user), fingerprints are merely treated in the traditional way. Different from existing mobility-assisted approaches [9, 22, 34] that explore spatial mobility constraints, we solely utilize essential mobility hints to amend the transitional fingerprints. Hence DorFin can be further integrated with previous mobility-assisted techniques to achieve better performance.

# 9.4.2 Robust Fingerprinting

As we have observed, RSSs of one pair of fingerprints may contain outliers because of impaired measurements due to human body blockage. Since this is a primary cause of biased RSSs in mobile environments, only RSSs over a small portion of APs (that are blocked) may present outliers while most APs would remain consistent. Thus in this section, we propose to apply robust regression method on the inconsistent fingerprints, in the hope of bounding the influence of outlying measurements.

There are a large body of robust regression techniques, such as M-estimator, Sestimator, L-estimator, etc. [25]. Among them, we choose the most widely adopted Least Median of Squares (LMS) [24] estimator due to its simplicity, effectiveness, and high breakdown point (0.5), which is demonstrated to yield sufficient results with efficient computation (as indicated in Sect. 9.5).

Given a query fingerprint $f _ { s } = [ f _ { s , i } , 1 \le i \le p ]$ and a sample fingerprint $f _ { t } = [ f _ { t , i } , 1 \leq i \leq p ]$ (suppose that both of them have been adjusted to be of $p$ RSS values as introduced in Sect. 9.3.1), we adopt a simple linear regression model as follows:

$$
y _ {i} = \alpha_ {1} x _ {i} + \alpha_ {2} + e _ {i}, i = 1, \dots , p, \tag {9.2}
$$

where the response variables y are given by $f _ { s }$ , while explanatory variables ${ \textbf { \em x } } =$ $\pmb { f } _ { t } . \pmb { e } = [ e _ { 1 } , \cdot \cdot \cdot , e _ { p } ]$ indicates the error term which is assumed to be normally distributed with zero mean and an unknown standard deviation $\sigma$ .

As the AP number $p$ is usually small, applying robust regression on insufficient observations does not always produce convincing statistical results. To obtain sufficient data for regression, we propose to compare the query fingerprint against all sample fingerprints corresponding to a candidate location, instead of a single averaged fingerprint. Specifically, for the candidate location $L = l ( f _ { t } )$ with sample fingerprints $\mathcal { \bar { F } } ^ { \bar { L } } = \{ f _ { k } ^ { \bar { L } } , k = 1 , \cdots , m \}$ , we simultaneously match $f _ { s }$ to all records in $\bar { \mathcal { F } } ^ { \bar { L } }$ . In doing so, we acquire mp observations, which can achieve the scale of hundreds since there are generally at least dozens of sample fingerprints for one location in the fingerprint database, and thus are sufficient for LMS regression. In this case, the explanatory variables x becomes $\pmb { x } ~ = ~ [ \pmb { f } _ { 1 } ^ { L } , \cdot \cdot \cdot , \pmb { f } _ { m } ^ { L } ] _ { 1 \times m p } ^ { \bar { T } }$ and correspondingly y is expanded as $\mathbf { \boldsymbol { y } } = [ \mathbf { \boldsymbol { f } } _ { s } , \cdots , \mathbf { \boldsymbol { f } } _ { s } ] _ { 1 \times m p } ^ { T }$ . The regression model is thus rewritten as

$$
y _ {k, i} = \alpha_ {1} x _ {k, i} + \alpha_ {2} + e _ {k, i}, \tag {9.3}
$$

where $i = 1 , \cdots , p , k = 1 , \cdots , m$ , and $x _ { k , i }$ and $y _ { k , i }$ indicate the value of $f _ { i }$ in $\boldsymbol { f } _ { k } ^ { L }$ and $f _ { s }$ , respectively. Applying LMS to the data x y yields $\hat { \pmb { \alpha } } = [ \hat { \alpha } _ { 1 } , \hat { \alpha } _ { 2 } ]$ where the estimates $\hat { \alpha } _ { i }$ denote the regression coefficients. Multiplying x with these $\hat { \alpha } _ { i }$ , we obtain the estimated values of $y _ { i }$ as

$$
\hat {y} _ {k, i} = \hat {\alpha} _ {1} x _ {k, i} + \hat {\alpha} _ {2}. \tag {9.4}
$$

# 9.4 Design Methodology

The LMS estimator is given by minimizing the median of squares of residuals as follows:

$$
\min _ {\hat {\alpha}} \operatorname * {m e d} _ {i, k} (y _ {k, i} - \hat {y} _ {k, i}) ^ {2}. \tag {9.5}
$$

To determine whether a value $y _ { k , i }$ is an outlier among all elements in y, we compare the residual $\boldsymbol { r } _ { k , i } = y _ { k , i } - \hat { y } _ { k , i }$ to the scale estimate $\sigma ^ { * }$ defined by [25]. Then each $y _ { k , i }$ is adjusted to $\tilde { y } _ { k , i }$ as follows:

$$
\tilde {y} _ {k, i} = \left\{ \begin{array}{l l} y _ {k, i} & \text { if   } | r _ {k, i} / \sigma^ {*} | \leq 2. 5 \\ \hat {y} _ {k, i} & \text { otherwise } \end{array} \right. \tag {9.6}
$$

where

$$
\sigma^ {*} = \sqrt {\frac {\sum_ {k = 1} ^ {m} \sum_ {i = 1} ^ {p} w _ {k , i} r _ {k , i} ^ {2}}{\sum_ {k = 1} ^ {m} \sum_ {i = 1} ^ {p} w _ {k , i}}},
$$

$$
w _ {k, i} = \left\{ \begin{array}{l} 1 \text {   if   } | r _ {k, i} / s ^ {0} | \leq 2. 5 \\ 0 \text {   otherwise } \end{array} \right.,
$$

$$
s ^ {0} = 1. 4 8 2 6 * (1 + \frac {5}{n}) \sqrt {\mathrm{med} _ {k , i} r _ {k , i} ^ {2}}.
$$

The involved constant values are widely recognized factors that has been suggested by preliminary experience in the literature [25] and can generalize to difference scenarios. Accordingly, the RSS values of the query fingerprint $f _ { s }$ are regulated as $\begin{array} { r } { \tilde { f } _ { s , i } = \frac { 1 } { m } \sum _ { k } \tilde { y } _ { k , i } } \end{array}$ and the RSDs $\pmb { \delta } _ { s t }$ between $f _ { s }$ and $\pmb { f } _ { t }$ are thus tuned as $\tilde { \delta } _ { s t , i } =$ $| \tilde { f } _ { s , i } - f _ { t , i } |$ .

# 9.4.3 Discriminatory Policy

Given that APs have diverse discrimination capability to fingerprint a specific location, it is inappropriate, and also unnecessary, to match two fingerprints with all APs equally involved. More accurate location estimations can be achieved by relying more on the discriminative APs, and limiting the influence of those fluctuating and distant ones. Different from previous works that select a subset of APs for localization [2, 4], we attempt to appropriately assess and leverage each AP by seeking a discrimination metric that complies with physical constraints of signal propagation and simultaneously stays robust to RSS fluctuations.

To quantitatively differentiate each AP for a specific location, we define a discrimination factor according to the physical distance estimation between the AP and the mobile client using the widely adopted Log-Distance Path Loss (LDPL) model [23]:

$$
P _ {d} = P _ {d _ {0}} - 1 0 \gamma \lg (\frac {d}{d _ {0}}), \tag {9.7}
$$

where $P _ { d _ { 0 } }$ denotes the received power at a distance $d _ { 0 }$ (which usually takes the value of 1 m), $\gamma$ is the path loss exponent, and $P _ { d }$ is the RSS in decibel measured at a distance of $d$ (in meters). Generally, $P _ { d _ { 0 } }$ is a constant empirical value given the AP transmitting power. Although $\gamma$ can change between each pair of AP-client, there are a lot of works targeting at adaptively estimating its value [27], which is not within the scope of this chapter. In the prototyped DorFin, we determine $P _ { d _ { 0 } }$ and $\gamma$ by empirical values and experimental measurements, as detailed in Sect. 9.5.

Deriving the distance to AP $A _ { i }$ from the LDPL model, we calculate its discrimination factor in fingerprint $\boldsymbol { f } _ { u }$ to location $L _ { u }$ as follows:

$$
\rho_ {i} ^ {u} = \frac {1}{d _ {i} ^ {u}} = 1 0 ^ {\frac {f _ {u , i} - P _ {d _ {0}}}{1 0 \gamma}}, \tag {9.8}
$$

where $d _ { i } ^ { u }$ is the estimated distance between $A _ { i }$ and $L _ { u }$ . The rationale of using the reciprocal of physical distance lies in that it is consistent with the derivative of the LDPL equation, which indicates the RSS change $\begin{array} { l } { \Delta R S S { \mathrm { ~ \propto ~ } } { - \frac { 1 } { d } } } \end{array}$ . More generally speaking, the basic rule is to emphasize closer APs with stronger RSSs.

While the exponential $\rho _ { i } ^ { u }$ effectively discriminates different APs, it may also induce unnecessary matching errors in case of fluctuating RSSs, which may lead to significant distance estimation errors. Consider one of the APs in a fingerprint that fluctuates to a very large value (e.g., 45 dBm). In this case, the effects of other representative APs, which could hold considerable RSSs (e.g., up to 60 dBm) and are thus discriminative, may become negligible since they can only get inappreciable factors three or four times smaller than the fluctuating AP. Hence to cope with noisy RSSs, we additionally incorporate a sigmoid function to retain the effects of most discriminative APs. Mathematically, $\rho _ { i } ^ { u }$ is adjusted as follows:

$$
\rho_ {i} ^ {u} = \left\{ \begin{array}{l l} 1 0 ^ {\frac {f _ {u , i} - P _ {d _ {0}}}{1 0 \gamma}} & \text { if } f _ {u, i} \leq f _ {0} \\ \frac {1}{a} \left(1 + e ^ {- 2 \left(\frac {f _ {u , i} + 1 0 0}{1 0} - c\right)}\right) ^ {- 1} & \text { otherwise } \end{array} \right. \tag {9.9}
$$

where the watershed RSS value $f _ { 0 }$ can be a flexible empirical value, e.g., 55 dBm. Then the constant parameters $a$ and $c$ need to be determined based on the specific value of $\gamma$ such that $\rho _ { i } ^ { u }$ is continuous at $f _ { 0 }$ . When applying to different location systems, $\gamma$ can be derived by empirical values and experimental measurements [27]. As shown in Sect. 9.5, empirical values based on real measurements yield grateful performance in practice, better than previous AP section policy [4]. $\rho _ { i } ^ { u }$ then serves as a differential weight which will be attached to the regressed RSD of $A _ { i }$ between $\scriptstyle f _ { u }$ and another fingerprint when computing their dissimilarity, as detailed in Sect. 9.4.4. Note that the discrimination factor will be normalized as $\textstyle \sum _ { k = 1 } ^ { n } \rho _ { k } ^ { u } = 1$ to keep the total power of a weighted fingerprint unchanged.

# 9.4.4 Localization

Integrating all of the above components in a unified solution, we define a new metric as follows for uniform fingerprint dissimilarity judgment.

$$
h (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) = \left(\sum_ {i = 1} ^ {p _ {s t}} (\rho_ {i} ^ {s t} \cdot \tilde {\delta} _ {s t, i}) ^ {2}\right) ^ {\frac {1}{2}}, \tag {9.10}
$$

where $p _ { s t } = | \mathcal { A } _ { s } \cup \mathcal { A } _ { t } |$ is the total number of distinctive APs in $f _ { s }$ and $\pmb { f } _ { t }$ , and $\rho _ { i } ^ { s t } = $ max $\{ \rho _ { i } ^ { s } , \rho _ { i } ^ { t } \}$ denotes the discrimination capability of AP $A _ { i }$ for matching $f _ { s }$ and $\boldsymbol { f } _ { t }$ , which is calculated based on the regressed fingerprints. Note that the RSD $\tilde { \delta } _ { s t , i }$ i could also be given by other suitable metrics such as a probability estimation. Realizing that fingerprints from closer locations share more common APs (or equivalently, fingerprints with very few common APs is unlikely to be from adjacent or same locations), the ultimate form of dissimilarity between two fingerprints $f _ { s }$ and $\pmb { f } _ { t }$ is expanded as follows:

$$
\phi (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) = h (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) \cdot \frac {p _ {s t}}{q _ {s t}}, \tag {9.11}
$$

where $q _ { s t } ~ = ~ | { \mathcal { A } } _ { s } \cap { \mathcal { A } } _ { t } |$ denotes the number of common APs in $f _ { s }$ and $\boldsymbol { f } _ { t }$ . With the above metric, the dissimilarity of two fingerprints with fewer common discriminative APs will be amplified. In case of no common APs $( q _ { s t } ~ = ~ 0 )$ , the dissimilarity will go to infinity, which eradicates the mismatch of two completely irrelevant fingerprints.

# 9.5 Experiments and Evaluation

# 9.5.1 Experimental Methodology

Data Collection We develop an application for site survey and implement DorFin on Google Nexus S and Nexus 4 phones, which both run the mainstream Android OSs (with Android API level 16 and 17, respectively). The two models are equipped with different WiFi chipsets, the former with Broadcom BCM4329 and the later with Qualcomm Atheros WCN3660. We treat the two models equally and interchangeably for training and testing during evaluation and examine the integrated performance.

We conduct experiments in three campus buildings, as shown in Figs. 9.6, 5.7, and 3.2 (denoted as Area #1, Area #2 and Area #3, respectively). We manually sample areas of interests in all buildings (corridors in Area #1 and #2, while corridors and rooms in Area #3). To construct the fingerprint database, we collect around 30–60 sample records at each location (which typically takes about 1 min).

Fig. 9.6 Experiment areas in an academic building   
![](images/9e0980dc35d3984d9c7576bad97df6ab687bb6d040034f9b5e87bf46200cc743.jpg)



In Area #1 and #2, we collect RSS data by putting the phone on a portable desk. To get rid of human body effects, user does not present around the desk when the mobile phone is collecting data (but there are passengers passing through the corridors). A high sampling density of 1 1 m is used for extensive evaluation. Sparser data are then derived from these densely surveyed samples. In total, we obtain 90 locations in Area #1 and 83 sample locations in Area #2. In Area #3 where we sample the whole floor, we hold the phone in hand for collection. We use a sampling density of 2 2 m and survey 293 locations in total, for each we gather at least 60 RSS samples. Two hundred and ninety-three sample locations are gathered in Area #3. Note that the training data collection can be also done via crowdsourcing-based mechanisms [22, 34, 36]. However, we currently still conduct in manual manner in purpose of obtaining qualified and reliable ground truths for evaluation. Our future work includes building a real system that integrates automatic techniques for fingerprint collection and adaptation.

We consider both static and mobile cases for testing. For stationary cases, we collect query data by letting users record measurements at each location with their smartphones held in hand. For a mobile user, the smartphone measures RSSs while the user is walking at a constant speed along a designated path with predefined start and end points. Note that the individual walking speed varies from user to user and from trace to trace. To obtain the ground truth locations of fingerprint records along the moving trace, we compute user’s walking speed by dividing the path length to the total time, and accordingly interpolate between the start and end points to obtain the location corresponding to each measurement based on their timestamps. The data are all collected at different time (mostly from afternoon to the night) over two days. When collecting data, people are working routinely in their offices or labs and some will occasionally walking around and pass through the corridors. Users hold their phones in hand naturally with free styles during collection. In total, we collect static queries from around 200 locations in Area #1 and #2 and all 293 locations in Area #3. We gather over 20 mobile traces reported from different pathways.

Methods We compare DorFin with two classical and two state-of-the-art schemes for fingerprint-based localization. Despite of numerous fingerprint-based approaches built upon RADAR and Horus, we still include them in purpose of confirming the performance improvements of DorFin over pure RSS fingerprintbased schemes.

• Enhanced RADAR (RADAR)[1]: RADAR is one of the most classical and widely adopted fingerprinting scheme, upon which a large body of algorithms are built [40]. We enhance RADAR by integrating the proposed common AP (CA) factor and using K-nearest neighbours for location estimation.   
• Enhanced Horus (Horus)[43]: A classical probabilistic algorithm that computes the probability distribution of the RSS values at each location as the fingerprint metric, and retrieves the targets of the maximum likelihood as estimated locations. Horus is also implemented with the CA factor and KNN scheme.   
• Temporally weighted KNN (TW-KNN) [11]: TW-KNN forms fingerprints with temporally weighted RSS by applying an iterative recursive weighted average filter on training RSS samples. Only a set of “important” APs are selected according to RSS values.   
• Kullback-Leibler Divergence (KLDiv) [17, 18]: A fingerprint-based localization scheme that utilizes the Kullback-Leibler divergence distance between two signal distributions as the similarity measure.

# 9.5.2 Performance Evaluation

# 9.5.2.1 Overall Performance

Figure 9.7a illustrates the localization error distributions seen by DorFin in different areas. DorFin achieves mean accuracy of around 1.7 m in both Area #1 and #2, while the mean error in the larger Area #3 appears to be higher, achieving 3.8 m. Besides the promising average accuracy, DorFin significantly reduces large localization errors. In all experimental areas, DorFin decreases the 95th percentile errors to less than 7.0 m.

To examine the performance in mobile scenarios, we test the proposed approach on the mobile traces and report the integrated results. As illustrated in Fig. 9.7b, despite slight drop in accuracy compared to the static cases, DorFin maintains graceful performance in mobile cases, far superior to Horus and RADAR. Specifically, the average and 95th errors are about 3.0 and 8.5 m, respectively. In comparison with RADAR and Horus, DorFin decreases both errors by nearly 50%. Even though the performance in mobile cases is not as good as static cases, the achieved accuracy remains comparable and promising. In addition, other complementary techniques such as path matching [36] can be integrated to further improve the accuracy for continuous localization.

![](images/3bb555c1a2f8c85b71187fdebe66027dc7675dab8ec9834e8cd3f21a5ecc532f.jpg)



(a)

![](images/49f5c9fa798030589cf11d0932c595058e770bb902f21f2be38d824844ace9f6.jpg)



(b)

![](images/e2fcd60ec16a55f151f24630fd169a27ecd6046fe41af3e00801c604a3e42e09.jpg)



(c)

![](images/13c54c04ebd8a1a7dbe833fac00975d2a056a443364f499bcb02909357baeee9.jpg)



(d)   
Fig. 9.7 Accuracy of DorFin. (a) Accuracy in different areas. (b) Accuracy in mobile cases. (c) Accuracy comparison. (d) Impact of sample number

Performance comparison Integrating all results in Fig. 9.7c, DorFin consistently surpasses comparison methods. Specifically, DorFin achieves an average accuracy of 2.5 m and 95th percentile accuracy of 6.2 m. TW-KNN and Horus achieve the most comparable performance, with mean and 95th percentile errors of 3.8, 3.9, 8.0 and 7.8 m, respectively. Among all approaches, RADAR yields the worst results with a mean error of 4.5 m. KLDiv suffers from remarkable large errors, with 95th percentile error of 19.8 m, although it achieves a slightly better median accuracy of 2.6 m than DorFin. In addition, DorFin significantly mitigates the large errors by around 40%, limiting the max location errors within 10 m, while all comparative methods produce max errors up to at least 16 m.

Impact of training RSS samples Due to the instability of RSS measurements, we are interested in whether and how the localization accuracy of DorFin would be affected by different sizes of training RSS samples for each location. Hence we tried DorFin with different number of training samples respectively and illustrate the results in Fig. 9.7d. As seen, it yields only marginal differences in performance when using 20, 40, and 60 RSS samples for training. When shrinking the training sizes from 60 to 20 samples, the mean and 95th percentile errors merely increase by 2.4% and 6.4%. The results demonstrate the graceful robustness of DorFin to RSS variations.

![](images/df6e566398a31ab904d69ce402ce7e2cf15060fd369ac4c6ce04a97b05eb9a83.jpg)



![](images/f9898fb4108ddf3eff372e733a881abfdf4acd8b96355ceee5ed6b918716598f.jpg)



![](images/1a0d173eb27bb820866d89563aecfcf5764fafd037340d8be55d718bab7bf86d.jpg)



![](images/8fc28291358ffafab455b5d3ce51af95dccc0b6d97ef555a5d4dd85bc401d956.jpg)



Fig. 9.8 Impacts of (a) sample density, (b) individual modules, (c) DF, (d) PF (mobile scenarios)

Impact of sample density As mentioned above, we sample the areas of interests with a density of $1 \times 1 \mathrm { m }$ , which is relatively high for practical operations. To examine the performance with sparser sample locations, we perform DorFin with training data of different sample densities (sample density is adjusted by sifting parts of the samples according to their locations). As shown in Fig. 9.8a, DorFin preserves excellent accuracy even with sample densities of $2 \times 2$ m and $3 \times 3 \mathrm { m }$ . Specifically, with density of $2 \times 2 \mathrm { m }$ , the mean and 95th percentile errors are still limited at 2.5 and 7.0 m respectively, both better than those of Horus and RADAR with density of $1 \times 1 \mathrm { m }$ .

In conclusion, DorFin achieves remarkable performance in both stationary and mobile cases, with reasonable sample densities. To understand how each module of DorFin contributes to the integral accuracy, we next perform an analysis across different modules.

# 9.5.2.2 Effect of Individual Modules

We separately employ each module of DorFin, i.e., the discrimination factor (DF) module, the robust regression (RR) module, the common AP constraints (CA) module, and the phantom fingerprint (PF) module on the most basic nearest neighbor method (denoted as Basic) described in Sect. 9.3.1 and evaluate the individual performance.

Effect of DF We evaluate the impact of DF by using a set of empirical parameters to calculate the discrimination factor. Specifically, the path loss exponent is set to a typical value of 3 in indoor environments while the referenced received power $P _ { d _ { 0 } }$ is determined as −40 dB by some on-site measurements. The sigmoid function parameters a and c accordingly adopts the values of 4 and 4.3, respectively. As shown in Fig. 9.8b, DF limits the 95th percentile estimation error by about 40%, while the average error is 1.5 m lower than the Basic scheme, which has mean and 95th percentile errors of 5 and 17.5 m. By placing more weight on more discriminatory APs and limiting those of the others, DF achieves the improvement by ensuring the similarity between fingerprints of close locations. In addition, results from different buildings indicate that discrimination factors with uniform parameter settings can generate satisfactory results in different scenarios. Previous works employ RSS cutting method based on a simple threshold to select a subset of APs for localization. We also implement this scheme in our settings and compare its performance with DF. As shown in Fig. 9.8c, by exploiting potentials of all valuable APs, the proposed DF achieves better performance than the simple RSS cutting methods, no matter what thresholds are used.

Effect of RR As shown in Fig. 9.8b, by employing RR over the Basic scheme, an average accuracy of 2.2 m is achieved, with the corresponding 95th percentile accuracy of only 6 m. Evidently, the advantages of RR are the most significant among all modules by reducing the mean and 95th percentile errors by about 56% and 65% compared with the Basic scheme, respectively. Such results on RR confirm our observation that fingerprint inconsistency counts as a major cause of localization errors of fingerprint-based methods especially for smartphones.

Effect of CA Figure 9.8b also demonstrates that the CA module is simple yet effective. Incorporating the CA module with Basic scheme, the average and 95th percentile localization errors are reduced by about 27% and 40%, turning into 3.6 and 11.2 m, respectively. Dissimilarity of fingerprints from faraway locations is largely enlarged by the common AP ratio, while that of fingerprints from close locations is hardly affected (since close locations share more common APs).

Effect of PF To examine the effectiveness of phantom fingerprints in dealing with outdated RSS measurements, we compare the performance of the Basic method on mobile data with and without constructing phantom fingerprints. As depicted in Fig. 9.8d, the average and 95th percentile errors decrease from 3.9 and 10.4 m to 2.4 and 6.9 m respectively when the sample fingerprints are appropriately replaced with phantom fingerprints. With these results, it is of interests to examine to what extent the measured RSSs and further the entire fingerprints are outdated. As we observed, over 11% of RSS measurements are outdated in our experiment data. Furthermore, almost every fingerprint undergoes outdated RSSs. In particular, there frequently exist large offset distances ranging from 2 to 6 m in most fingerprints. The effectiveness of the PF convincingly validates our observation that the transitional fingerprint problem can lead to location errors in mobile environments.

Building upon these components, DorFin produces promising accuracies that are competitive with those achieved by leveraging physical layer information [26, 27] or introducing extra ranging techniques [16, 19] (both with mean accuracy of about 1 3 m). Without degrading the ubiquity nor increasing the costs, we believe the performance achieved by DorFin outperforms most of existing approaches and demonstrates promising potentials in serving as a practical scheme for worldwide deployment.

Considering potential RSS variations over long-term running, the radio map of some locations will change over time and lead to higher localization errors. Accounting this, self-calibration techniques for radio map updating [34, 37, 41], which tackle the RSS temporal variations to maintain an up-to-date database, could be incorporated for practical deployment and usage.

# 9.6 Conclusions

While WiFi fingerprint-based localization acts as the dominant scheme in indoor localization, the accuracy challenge remains a primary concern. In this chapter, we identify several crucial causes of localization errors in fingerprint-based schemes. These observations then lead us to the design of a new WiFi fingerprinting scheme which successfully reduces location errors without degrading ubiquity nor increasing the costs. Our approach marks a significant progress in RSS fingerprintbased indoor localization, especially for smartphones.

# References

1. Bahl, P., Padmanabhan, V.N.: RADAR: an in-building RF-based user location and tracking system. In: Proceedings of IEEE INFOCOM (2000)   
2. Chen, Y., Yang, Q., Yin, J., Chai, X.: Power-efficient access-point selection for indoor location estimation. IEEE Trans. Knowl. Data Eng. 18(7), 877–888 (2006)   
3. Cheng, W., Tan, K., Omwando, V., Zhu, J., Mohapatra, P.: RSS-ratio for enhancing performance of RSS-based applications. In: Proceedings of IEEE INFOCOM (2013)   
4. Cisco Systems, I.: Wi-Fi location-based services 4.1 design guide (2013)   
5. Fang, S.H., Lin, T.N.: Principal component localization in indoor wlan environments. IEEE Trans. Mob. Comput. 11(1), 100–110 (2012)   
6. Fet, N., Handte, M., Marrón, P.J.: A model for WLAN signal attenuation of the human body. In: Proceedings of ACM UbiComp (2013)   
7. Haeberlen, A., Flannery, E., Ladd, A.M., Rudys, A., Wallach, D.S., Kavraki, L.E.: Practical robust localization over large-scale 802.11 wireless networks. In: Proceedings of ACM MobiCom (2004)   
8. He, S., Hu, T., Chan, S.H.G.: Contour-based trilateration for indoor fingerprinting localization. In: Proceedings of ACM SenSys (2015)   
9. Hilsenbeck, S., Bobkov, D., Schroth, G., Huitl, R., Steinbach, E.: Graph-based data fusion of pedometer and WiFi measurements for mobile indoor positioning. In: Proceedings of ACM UbiComp, pp. 147–158 (2014)

10. IEEE: IEEE 802.11, part11: wireless LAN medium access control (MAC) and physical layer (PHY) specifications (2012)   
11. Jiang, P., Zhang, Y., Fu, W., Liu, H., Su, X.: Indoor mobile localization based on Wi-Fi fingerprints important access point. Int. J. Distrib. Sens. Netw. 2015, 45 (2015)   
12. Li, L., Shen, G., Zhao, C., Moscibroda, T., Lin, J.H., Zhao, F.: Experiencing and handling the diversity in data density and environmental locality in an indoor positioning service. In: Proceedings of ACM MobiCom (2014)   
13. Lim, H., Kung, L.C., Hou, J.C., Luo, H.: Zero-configuration indoor localization over IEEE 802.11 wireless infrastructure. Wirel. Netw. 16(2), 405–420 (2010)   
14. Lin, K., Chen, M., Deng, J., Hassan, M.M., Fortino, G.: Enhanced fingerprinting and trajectory prediction for IoT localization in smart buildings. IEEE Trans. Autom. Sci. Eng. 13(3), 1294–1307 (2016)   
15. Liu, K., Liu, X., Li, X.: Guoguo: enabling fine-grained indoor localization via smartphone. In: Proceedings of ACM MobiSys (2013)   
16. Liu, H., Yang, J., Sidhom, S., Wang, Y., Chen, Y., Ye, F.: Accurate WiFi based localization for smartphones using peer assistance. IEEE Trans. Mob. Comput. 13(10), 2199–2214 (2014)   
17. Mirowski, P., Steck, H., Whiting, P., Palaniappan, R., MacDonald, M., Ho, T.K.: Kl-divergence kernel regression for non-Gaussian fingerprint based localization. In: Proceedings of IEEE IPIN, pp. 1–10 (2011)   
18. Mirowski, P., Milioris, D., Whiting, P., Kam Ho, T.: Probabilistic radio-frequency fingerprinting and localization on the run. Bell Labs Tech. J. 18(4), 111–133 (2014)   
19. Nandakumar, R., Chintalapudi, K.K., Padmanabhan, V.N.: Centaur: locating devices in an office environment. In: Proceedings of ACM MobiCom (2012)   
20. Ni, L.M., Liu, Y., Lau, Y.C., Patil, A.P.: LANDMARC: indoor location sensing using active RFID. Wirel. Netw. 10(6), 701–710 (2004)   
21. Paul, A.S., Wan, E.: RSSI-based indoor localization and tracking using sigma-point Kalman smoothers. IEEE J. Sel. Top. Sign. Proces. 3(5), 860–873 (2009)   
22. Rai, A., Chintalapudi, K.K., Padmanabhan, V.N., Sen, R.: Zee: zero-effort crowdsourcing for indoor localization. In: Proceedings of ACM MobiCom (2012)   
23. Rappaport, T.S., et al.: Wireless Communications: Principles and Practice, vol. 2. Prentice Hall PTR, New Jersey (1996)   
24. Rousseeuw, P.J.: Least median of squares regression. J. Am. Stat. Assoc. 79(388), 871–880 (1984)   
25. Rousseeuw, P.J., Leroy, A.M.: Robust regression and outlier detection. Wiley, Hoboken (2005)   
26. Sen, S., Radunovic, B., Choudhury, R.R., Minka, T.: You are facing the Mona Lisa: spot localization using PHY layer information. In: Proceedings of ACM MobiSys (2012)   
27. Sen, S., Lee, J., Kim, K.H., Paul, C.: Avoiding multipath to revive inbuilding WiFi localization. In: Proceedings of ACM MobiSys (2013)   
28. Shen, G., Chen, Z., Zhang, P., Moscibroda, T., Zhang, Y.: Walkie-Markie: indoor pathway mapping made easy. In: Proceedings of USENIX NSDI (2013)   
29. Shu, Y., Huang, Y., Zhang, J., Cou, P., Cheng, P., Chen, J., Shin, K.G.: Gradientbased fingerprinting for indoor localization and tracking. IEEE Trans. Ind. Electron. 63(4), 2424–2433 (2016)   
30. Sun, W., Liu, J., Wu, C., Yang, Z., Zhang, X., Liu, Y.: MoLoc: on distinguishing fingerprint twins. In: Proceedings of IEEE ICDCS (2013)   
31. Tarzia, S.P., Dinda, P.A., Dick, R.P., Memik, G.: Indoor localization without infrastructure using the acoustic background spectrum. In: Proceedings of ACM MobiSys (2011)   
32. Turner, D., Savage, S., Snoeren, A.C.: On the empirical performance of self-calibrating WiFi location systems. In: Proceedings of IEEE Conference on Local Computer Networks (LCN) (2011)   
33. Wang, J., Katabi, D.: Dude, where’s my card? RFID positioning that works with multipath and non-line of sight. In: Proceedings of ACM SIGCOMM (2013)   
34. Wang, H., Sen, S., Elgohary, A., Farid, M., Youssef, M., Choudhury, R.R.: No need to wardrive: unsupervised indoor localization. In: Proceedings of ACM MobiSys (2012)

35. Welch, T.B., Musselman, R.L., Emessiene, B.A., Gift, P.D., Choudhury, D.K., Cassadine, D.N., Yano, S.M.: The effects of the human body on UWB signal propagation in an indoor environment. IEEE J. Sel. Areas Commun. 20(9), 1778–1782 (2002)   
36. Wu, C., Yang, Z., Liu, Y.: Smartphones based crowdsourcing for indoor localization. IEEE Trans. Mob. Comput. 14(2), 444–457 (2015)   
37. Wu, C., Yang, Z., Xiao, C., Yang, C., Liu, Y., Liu, M.: Static power of mobile devices: selfupdating radio maps for wireless indoor localization. In: Proceedings of IEEE INFOCOM, pp. 2497–2505 (2015)   
38. Wu, C., Yang, Z., Xu, Y., Zhao, Y., Liu, Y.: Human mobility enhances global positioning accuracy for mobile phone localization. IEEE Trans. Parallel Distrib. Syst. 26(1), 131–141 (2015)   
39. Xu, H., Yang, Z., Zhou, Z., Shangguan, L., Yi, K., Liu, Y.: Enhancing WiFi-based localization with visual clues. In: Proceedings of ACM UbiComp, pp. 963–974 (2015)   
40. Yang, Z., Wu, C., Zhou, Z., Zhang, X., Wang, X., Liu, Y.: Mobility increases localizability: a survey on wireless indoor localization using inertial sensors. ACM Comput. Surv. 47(3), 54:1–54:34 (2015)   
41. Yin, J., Yang, Q., Ni, L.M.: Learning adaptive temporal radio maps for signal-strength-based location estimation. IEEE Trans. Mob. Comput. 7(7), 869–883 (2008)   
42. Youssef, M., Agrawala, A.: Handling samples correlation in the Horus system. In: Proceedings of IEEE INFOCOM (2004)   
43. Youssef, M., Agrawala, A.: The Horus location determination system. Wirel. Netw. 14(3), 357–374 (2008)   
44. Youssef, M.A., Agrawala, A., Udaya Shankar, A.: WLAN location determination via clustering and probability distributions. In: Proceedings of IEEE PerCom (2003)   
45. Zhang, Z., Zhou, X., Zhang, W., Zhang, Y., Wang, G., Zhao, B.Y., Zheng, H.: I am the antenna: accurate outdoor AP location using smartphones. In: Proceedings of ACM MobiCom (2011)

# Part V

# Conclusions

Part V concludes this book and lists possible future works of LBSs.

# TO FUTURE INDOOR LOCALIZATION:

We can only see a short distance ahead, but we can see plenty there that needs to be done.

– Alan Turing

# Chapter 10 Research Summary and Future Directions

![](images/353adb85232a78bd8410f1ed46af887e3616c2b1bcc6f6e05aa45b48df90222c.jpg)

Abstract In this chapter, we summarize this book and, more importantly, present a vision on future directions. The research on wireless indoor localization continues growing and we foresee a prime time of indoor localization in the near future.

# 10.1 Research Summary

This book presents a summary of our research results in the area of wireless indoor localization during the past several years. Briefly, we present a set of novel technologies to tackle the key limitations that hinder the practical usage of WiFibased indoor localization, mainly from the perspective of mobile crowdsourcing.

We started from a comprehensive review of typical indoor localization systems and state-of-the-art technologies, and pointed out the bottlenecks of current WiFibased localization technologies. We then introduced some preliminaries on mobile crowdsourcing and inertial sensing. Afterwards, we presented novel techniques to boost the deployment, ease the maintenance, and enhance location accuracy, together aiming at creating an advanced indoor localization system, one that promotes the ubiquitous adoption of WiFi-based localization.

The presented content provides a good view of recent advances in the literature. While pioneer research demonstrates the feasibility and privilege of employing crowdsourcing in localization, to translate the research results into practical systems still requires significant efforts. For example, it is not a small undertaking to design a functional crowdsourcing service and popularize it to a large number of users for data collection. Even with the crowdsourcing data available, it is non-trivial to guarantee quality of crowdsourced radio maps and floorplans over a large scale.

# 10.2 Future Directions

The realm of wireless indoor localization is still in a boom and continues to develop from diverse perspectives. We summarize some of the interesting and attractive ones as follows.

Crowdsourcing Quality Management When crowdsourcing is widely adopted for localization, including radio map construction and floorplan generation, a reliable scheme to evaluate and guarantee the quality of crowdsourced data quality is demanded. Certain data verification scheme and error control would be helpful.

Seamless Outdoor/Indoor Services If indoor localization become a ubiquitous service, then it should be integrated with outdoor positioning system to form a seamless outdoor/indoor location service, allowing a user to walk in a mall from the entrance, a car to drive into the garage, a drone to get into buildings to deliver a package, etc. In addition, as multiple localization technologies might co-exist indoors for different scenarios, accuracy-aware switching between them will be another issue that needs to be addressed.

Physical Layer Information Physical layer information of WiFi, in particular the CSI, has been extensively exploited for finer-grained indoor localization. A number of research works have demonstrated not only localization but also a wide range of sensing applications like gesture recognition, vital signs monitoring, activity recognition, etc. Future research is envisioned to dive deeper into physical layer information and develop methods for ubiquitous end devices like smartphone and wearables.

The Rise of Imaging Image-based localization has been used in virtual reality and in-air interaction. As cameras have become one of the most important module of a smartphone, they also gain increasing attention for indoor localization in recent years. Image-based localization is completely infrastructure free and turns out to be an attractive solution, among many emerging techniques like visible light. The combination of image and WiFi/inertial sensing will also open new potentials. Not only localization, user-taken images can also be leveraged for indoor floorplan generation, which will provide richer contexts since images themselves are consumable to human.

Location Analytics Machine learning and big data are the hottest words in today’s world. Location data act as one of the most important and valuable type of big data, among others. Location data gathered from different scenarios would support variously purposed physical analytics. For example, location data from malls and stores support retail analytics; data from athletes underpin sports analytics; data from the whole buildings cement smart buildings; and data from an individual over time would underlie a new paradigm of smart life. All these data together will shape the big data era of location for unimagined applications with unprecedented values.