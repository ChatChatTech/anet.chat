Location, Localization, and Localizability

# Location, Localization, and Localizability

Location-awareness Technology for Wireless Networks

Second Edition

ISBN 978-981-97-3175-6

ISBN 978-981-97-3176-3 (eBook)

https://doi.org/10.1007/978-981-97-3176-3

© The Editor(s) (if applicable) and The Author(s), under exclusive license to Springer Nature Singapore Pte Ltd. 2011, 2024

This work is subject to copyright. All rights are solely and exclusively licensed by the Publisher, whether the whole or part of the material is concerned, specifically the rights of translation, reprinting, reuse of illustrations, recitation, broadcasting, reproduction on microfilms or in any other physical way, and transmission or information storage and retrieval, electronic adaptation, computer software, or by similar or dissimilar methodology now known or hereafter developed.

The use of general descriptive names, registered names, trademarks, service marks, etc. in this publication does not imply, even in the absence of a specific statement, that such names are exempt from the relevant protective laws and regulations and therefore free for general use.

The publisher, the authors and the editors are safe to assume that the advice and information in this book are believed to be true and accurate at the date of publication. Neither the publisher nor the authors or the editors give a warranty, expressed or implied, with respect to the material contained herein or for any errors or omissions that may have been made. The publisher remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

This Springer imprint is published by the registered company Springer Nature Singapore Pte Ltd.

The registered company address is: 152 Beach Road, #21-01/04 Gateway East, Singapore 189721, Singapore

If disposing of this product, please recycle the paper.

# Preface to the Second Edition

Time flies since the debut of this book. In the past 10 years, localization technology has evolved from small saplings into towering trees. Robots and drones with autonomous positioning and navigation capabilities, once considered unreachable fantasies, have gradually become a reality. However, while we are being amazed at the groundbreaking changes brought about by technology, as researchers, we still need to remain acutely attentive to the current limitations of localization. Some significant challenges still impede the widespread deployment. For example, traditional Wi-Fi fingerprint-based wireless localization, due to various challenges in fingerprint database collection and maintenance, has remained stay in the laboratory, and even when using smartphones for localization in malls, we still cannot achieve the outdoor GPS-like experience. The list goes on and on.

Against this backdrop, the reissue of this book aims to more comprehensively reflect the latest developments in localization technology. We have added introductions to emerging technologies such as passive high-precision localization based on wireless signal CSI and autonomous localization for smart devices. Additionally, we have integrated and further streamlined technical chapters that now appear outdated, adapting to the pace of the times. We hope this book will provide inspiration and reflection for new students, technology enthusiasts, and expert scholars who have been working in this field for many years, helping them make progress in algorithm design, system deployment, and technological innovation.

Beyond the development of technology itself, location-based services (LBS) have truly evolved from a few specialized applications into a ubiquitous service. Almost all applications request our location information to provide services that better cater to personal needs. This change is, to some extent, a gift from information technology. At the same time, deeper scientific understanding of localization itself deserves more attention.

As Leonardo da Vinci said, “Science is the observation of things possible, whether present or past.” The accumulation of scientific knowledge is a necessary prerequisite for scientific development, whether it is technology close at hand but not yet realized or dreams suddenly coming true on the distant horizon; scientific progress is always an accumulative gradient. Therefore, this book hopes to not only record the self-development of localization technology but also reflect the evolution of human understanding.

A decade is but a fleeting moment, and as the author, we are also experiencing changes. The reissue of this book is likewise a reflection of our personal growth and contemplation. If this book can stimulate everyone’s imagination about the future or inspire people to delve into the vast sea of knowledge, it will be the greatest honor of our lives.

Beijing, China

Beijing, China

2024-03-30

Yunhao Liu

Zheng Yang

# Preface

With the popularity of wireless networks, location-based service (LBS) has quickly entered people’s daily life. In practice, LBS has a large range of applications and often manifests in various forms in different types of networks. For example, E-911 in the USA, or corresponding E-112 in Europe, offers timely and accurate assistance to the emergency callers by locating them through mobile communication networks or global positioning system (GPS). Location information also plays a major role in modern asset management. Some companies, in particular hospitals, have deployed the Wi-Fi-based solutions for real-time equipment locating and tracking, in order to increase equipment utilization and reduce over purchasing costs. In addition, sensor network, a typical type of wireless ad hoc networks, has shown its great prospects of environmental monitoring, industrial sensing and diagnosis, battlefield surveillance, context-aware computing, and more. Autonomous localization of sensor nodes is essential since location makes the sensory data geographically meaningful. In all, many applications and services of wireless networks directly or indirectly rely on location information.

This book aims to provide a comprehensive and in-depth view of locationawareness technology in today’s popular wireless networks. However, the obvious diversity of networks, from short-range Bluetooth to long-range telecommunication network, makes it very challenging to organize materials. Although general principles exist, the implementation differs from network to network and application to application.

When composing the text, we have been thinking a lot about what materials to include and how to organize them. Our thoughts come to the following two decisions. First, from the perspective of application, this book focuses on wireless ad hoc and sensor networks, in which the overwhelming majority of localization techniques are involved. Indeed, the techniques discussed in this book are quite versatile. Other types of networks, such as WLAN and 3G mobile network, are also mentioned. Second, to make it better understood, this book is basically organized around three step-by-step themes: location, localization, and localizability. Locationbased applications are close to daily life and accordingly presented at the beginning. Afterward, as the major part of this book, localization approaches are discussed in-depth. Other advanced topics, such as localizability and location privacy, are studied at last.

Beijing, China

Beijing, China

2010-06-24

Yunhao Liu

Zheng Yang

# Book Organization

To begin with, the background of LBS and localization for wireless networks is presented in Chap. 1. Localization relies on the knowledge of physical world, in particular, the geometric relationship of network nodes. Chapter 2 discusses some popular ranging methods, including radio signal strength (RSS), time of arrival (ToA), time difference of arrival (TDoA), and hop counts. According to the physical measurements, one-hop positioning, as well as the related mathematical techniques of location computation, is presented in Chap. 3. Chapters 4 and 5 discuss the rangebased and range-free localization approaches, respectively. Chapter 6 studies a key factor, error control, which determines the success of a localization approach in practice. Typically, location errors come from two sources: ranging noises and algorithm design, both of which are explained in detail. Chapter 7 presents the localization approaches for mobile networks, in which network nodes physically move and their locations change continuously. As we know, different approaches have different capabilities in terms of the number of nodes whose locations can be determined by a particular approach. Chapter 8 studies the issue of localizability that characterizes such capability in theory. With the development of LBS, location privacy is becoming crucial, which is discussed in Chap. 9.

This book discusses many up-to-date localization algorithms in considerable depth, yet makes their design and analysis accessible to all levels of readers. We emphasize the basic concepts and designs while keep the completeness. Each chapter presents a related topic and is independent of each other. When finishing the first two chapters, readers can select the remaining ones by their own interests. Each chapter ends with a summary or a comparative study, which provides a big picture and facilitates understanding.

# Anticipated Audience

This book can serve as a guide book for the technicians and practitioners in the industry of real-time location systems (RTLS) and wireless networks. They can expect to obtain a comprehensive understanding of the field through reading this book, in order to compare and select localization solutions fulfilling various application requirements. Abundant references of this book open up a broader domain for advanced study. In addition, this book is tailored toward a textbook for college researchers and graduate students. For a one-semester graduate course, the main part includes three chapters (Chaps. 3, 4, and 5) about one-hop positioning and multi-hop network localization. Chapter 6 can be used as a follow-on topic. When there is time, three independent chapters (Chaps. 7, 8, and 9) can be added to course materials with freedom of choice. This book includes the state-of-the-art research results in many technical journals and conferences during its preparation. Readers can track trends and hot topics in the field.

Last but not least, this book purposefully accommodates the different backgrounds and career objectives of its reader. Specifically, it does not require a background of location-awareness technology. But as a technical book, we hope the readers have a basic knowledge of computer algorithms and networks.

# Acknowledgments

During almost 10 years working on the topic of location system, we have benefited a great lot from our friends and colleagues. We wish to take this opportunity to thank them.

Many former and present graduate students have contributed greatly to this book. Some chapters are based entirely on their writing. We particularly thank Xiaoping Wang, Lirong Jian, and Junliang Liu. They have done great jobs. We are grateful to many colleagues and peer researchers who shared with us exciting information. Especially, we thank Guohong Cao, Jiannong Cao, Guihai Chen, Tolga Eren, Jie Gao, David Goldenberg, Tian He, Jennifer Hou, Bill Jackson, Weijia Jia, Xiaohua Jia, Tibor Jordan, Wang-Chien Lee, Jianzhong Li, Qun Li, Xiang-Yang Li, Chenyang Lu, Guoqiang Mao, Abhishek Patil, Chunyi Peng, Yang Richard Yang, John Stankovic, Ivan Stojmenovic, Peng-Jun Wan, Jie Wu, Li Xiao, Dong Xuan, Baijian Yang, Yuanyuan Yang, Xiaodong Zhang, Tarek Abdelzaher, and Feng Zhao.

We thank all of those who have played in part in the preparation of this text. They include Prof. Lionel Ni, Prof. Renyi Xiao, Prof. Lei Chen, Dr. Mo Li, Dr. Jinsong Han, Dr. Yuan He, and Dr. Kebin Liu. The editor of this book, Brett Kurzman, of Springer provided many aspects of editorial support.

Finally, Yunhao Liu thanks his wife Jingyao Dai, and their parents Kai Liu, Yonghua Zhu, and Jianhua Zhang, for their unconditional support. Zheng Yang wishes to thank Chao Zhang, and his parents Aiguo Yang and Yajuan Gong, and his grandparents Jinggui Gong and Fenglan Niu, for their understanding and encouragement. We affectionately dedicate this book to them.

Beijing, China

Beijing, China

Yunhao Liu

Zheng Yang

# Contents

# 1 Introduction 1

1.1 Location-Based Services . . 1

1.1.1 Location-Based Applications .

1.1.2 Location-Aided Network Functions . 4

1.1.3 Topology Control . 4

1.2 Introduction to Localization . . 5

1.3 Book Organization . 6

References . 7

# 2 Physical Measurements . 9

2.1 Distance Measurements . 9

2.1.1 Radio Signal Strength . 10

2.1.2 Time of Arrival (ToA) . 11

2.1.3 Time Difference of Arrival (TDoA) . 18

2.1.4 Channel State Information (CSI) . 19

2.2 Angle Measurement . 25

2.3 Area Measurement . 26

2.3.1 Single Reference Area Estimation . 26

2.3.2 Multi-Reference Area Estimation . 27

2.4 Hop Count Measurements . 28

2.5 Neighborhood Measurement . 29

2.6 Summary 30

References . 31

# 3 One-Hop Location Estimation . 33

3.1 Distance-Based Positioning Techniques . 33

3.2 TDoA-Based Positioning Techniques . 35

3.3 AoA-Based Positioning Techniques . 38

3.4 RSS-Profiling-Based Positioning Techniques . 39

3.4.1 Offline Profiling Scheme . 40

3.4.2 Online Profiling Scheme . 40

References . 42

xv

# 4 Range-Based Network Localization 45

4.1 Computation Organization . 45   
4.2 Centralized Localization Approaches . 46

4.2.1 Multidimensional Scaling (MDS) . 46   
4.2.2 Semidefinite Programming (SDP) . 48

4.3 Distributed Localization Approaches . . 51

4.3.1 Beacon-Based Localization . 51   
4.3.2 Coordinate System Stitching . 55

4.4 Summary 60

4.4.1 Beacon Nodes . 60   
4.4.2 Node Density 60   
4.4.3 Accuracy 61   
4.4.4 Cost . 61

References . 63

# 5 Range-Free Network Localization . 65

5.1 Basic Hop-Based Algorithms . 65

5.1.1 DV-Hop . 65   
5.1.2 Amorphous 66

5.2 Improved Hop-Based Algorithms for Anisotropic Networks . . . . 66

5.2.1 PDM-Based Localization in Anisotropic Networks . . . 67   
5.2.2 Rendered Path in Networks with Holes . . 69   
5.2.3 Delaunay Complex-Based Localization . . 72

5.3 Proximity-Based Algorithms . 77

5.3.1 Point-in-Triangulation Test . 77   
5.3.2 Perpendicular Intersection . 78   
5.3.3 Relative Distance Estimation . 81

5.4 Summary 84

References . 84

# 6 Error Control . 85

6.1 Measurement Errors . 85

6.1.1 Errors in Distance Measurements . 85   
6.1.2 Negative Impact of Noisy Ranging Results . . . 86

6.2 Error Characteristics 87

6.2.1 What Is CRLB . 87   
6.2.2 CRLB for Multihop Localization . . 88   
6.2.3 CRLB for One-Hop Localization . 88

6.3 Localization Ambiguities . 89

6.4 Location Refinement . 92

6.4.1 A Framework of Location Refinement . 93   
6.4.2 Metrics for Location Refinement . 94

6.5 Outlier-Resistant Localization . 98

6.5.1 Explicitly Sifting . 99   
6.5.2 Implicitly De-Emphasizing . 103

6.6 Summary 107

References . 108

# 7 Localizability . 111

7.1 Network Localizability 111   
7.2 Graph Rigidity 112

7.2.1 Globally Rigid Graphs . 112   
7.2.2 Conditions for Network Localizability . 114

7.3 Inductive Construction of Globally Rigid Graphs . . 115

7.3.1 Trilateration . 115   
7.3.2 Wheel . 115

7.4 Node Localizability . 121   
7.5 Summary 127

References . 130

# 8 Robust Indoor Localization 131

8.1 Introduction . 131   
8.2 Overview . 135

8.2.1 Classical Fingerprinting Framework . 135   
8.2.2 ViViPlus Overview . 135

8.3 Spatial Awareness of RSS Fingerprints . 136

8.3.1 Limitations of RSS Fingerprints . 136   
8.3.2 RSS Spatial Gradient . . 138

8.4 ViViPlus Design . 142

8.4.1 Realization of RSS Spatial Gradient . 142   
8.4.2 Localization with RSG Matrices . . 145

8.5 Implementations and Evaluation . 147

8.5.1 Experiment Methodology . 147   
8.5.2 Overall Performance . 150   
8.5.3 Impact of Parameters . 154   
8.5.4 ViViPlus in Mobile Tracking . . . 156

8.6 Related Works . 157   
8.7 Summary 159

References . 159

# 9 Automatic Fingerprint Database Update . . 163

9.1 Introduction 163   
9.2 System Overview . 167   
9.3 Adversarial Learning-Based Robust Localization . . 168

9.3.1 Fingerprint-Image Transformer . 169   
9.3.2 Feature Extractor . 170   
9.3.3 Location Predictor . 170   
9.3.4 Domain Discriminator . 171   
9.3.5 Spatial Constraint . 172   
9.3.6 Objective and Training . 172

9.4 Cotraining-Based Reliable Model Update . 173

9.4.1 Reliable Fingerprint Selection . 174   
9.4.2 Diversity Augmentation . 174   
9.4.3 Rationale Behind Reliable Model Update . . 175

9.5 Implementation and Evaluation . . 176

9.5.1 Experimental Methodology . 176   
9.5.2 Performance Evaluation . 178   
9.5.3 Study of Core Components . . . 180

9.6 Related Work . 182   
9.7 Summary 183

References . 183

10 Location Privacy 187

10.1 Introduction . 187   
10.2 Threats . 188

10.2.1 How Can the Adversary Obtain Location Information of Others? . 188   
10.2.2 What Is the Negative Consequence of a Location Leak? . 188

10.3 Protection Strategies . . 189

10.3.1 Regulatory Approaches . 189   
10.3.2 Privacy Policies . 190   
10.3.3 Anonymity 191   
10.3.4 Obfuscation . 192

10.4 Anonymity-Based Approaches . 192

10.4.1 k-Anonymity 193   
10.4.2 Mix Zone . 194   
10.4.3 Using Dummies . . . 196   
10.4.4 Path Confusion . 197   
10.4.5 Comparison . 198

10.5 Summary 200

References . 201

# About the Authors

![](images/c98a6ee043cbd92c7d94b3bca167280bb959bd24f9ed8e31de80882a6f490b38.jpg)



Yunhao Liu is Chair Professor at Tsinghua University. He received his BS degree in Automation Department from Tsinghua University, an MS and a Ph.D. degree in Computer Science and Engineering in Michigan State University. He is a fellow of ACM and IEEE. He is now serving as the Editor-in-Chief of ACM Transactions on Sensor Networks and Honorary Chair of ACM China.

![](images/fb245955c10ee16b5e731f468d3912576b24a37716cb3039abe87b9c0b718179.jpg)



Zheng Yang is an Associate Professor at Tsinghua University. His research interests include Internet of Things and Industrial Internet. He received his B.E. degree from the Department of Computer Science, Tsinghua University, and his Ph.D. degree from the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. He is a fellow of IEEE and a member of ACM.