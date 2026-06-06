# Content Distribution for Mobile Internet: A Cloud-based Approach

# Content Distribution for Mobile Internet: A Cloud-based Approach

Second Edition

Zhenhua Li D

Tsinghua University

Beijing, Beijing, China

Guihai Chen

Shanghai Jiao Tong University

Shanghai, Shanghai, China

Yafei Dai

Peking University

Beijing, Beijing, China

Yunhao Liu

Tsinghua University

Beijing, Beijing, China

ISBN 978-981-19-6981-2

ISBN 978-981-19-6982-9 (eBook)

https://doi.org/10.1007/978-981-19-6982-9

© The Editor(s) (if applicable) and The Author(s), under exclusive license to Springer Nature Singapore Pte Ltd. 2023

This work is subject to copyright. All rights are solely and exclusively licensed by the Publisher, whether the whole or part of the material is concerned, specifically the rights of translation, reprinting, reuse of illustrations, recitation, broadcasting, reproduction on microfilms or in any other physical way, and transmission or information storage and retrieval, electronic adaptation, computer software, or by similar or dissimilar methodology now known or hereafter developed.

The use of general descriptive names, registered names, trademarks, service marks, etc. in this publication does not imply, even in the absence of a specific statement, that such names are exempt from the relevant protective laws and regulations and therefore free for general use.

The publisher, the authors, and the editors are safe to assume that the advice and information in this book are believed to be true and accurate at the date of publication. Neither the publisher nor the authors or the editors give a warranty, expressed or implied, with respect to the material contained herein or for any errors or omissions that may have been made. The publisher remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

This Springer imprint is published by the registered company Springer Nature Singapore Pte Ltd.

The registered company address is: 152 Beach Road, #21-01/04 Gateway East, Singapore 189721, Singapore

# Preface

Content distribution (also known as content delivery) is among the most fundamental functions of the Internet, i.e., distributing digital content from one node to another node or multiple nodes. Here digital content can be in the form of a web page, an image, software, audio, video, big data, etc.; a node can be a large server cluster, a personal computer, a smartphone, a small sensor, a tiny RFID (radio frequency identification device) tag, and so on.

Typical content distribution paradigms include Client/Server (C/S) over TCP/IP connections, Content Delivery Network (CDN) like Akamai and ChinaCache, Peerto-Peer (P2P) like BitTorrent and eMule, Super Node Relay (SNR) like KaZaa and Skype, and Peering via Internet eXchange (PIX) that is adopted by many Internet Service Providers (ISPs) to overcome the traditional Transit-Stub architecture’s shortcomings. They each have specific merits and drawbacks, targeting distinct application scenarios such as file download, media streaming, real-time interaction, and AR/VR.

Since Amazon’s launch of Elastic Compute Cloud (EC2) in 2006 and Apple’s release of iPhone in 2007, Internet content distribution has illustrated a strong trend of polarization. On one hand, great fortune has been invested by those “content hypergiants” (e.g., Google and Netflix) in building heavyweight and integrated data centers across the world, in order to achieve the economies of scale and the high flexibility/efficiency of content distribution. On the other hand, end-user devices have become increasingly lightweight, mobile, and heterogeneous, thus posing rigorous and volatile requirements on the bandwidth, latency, traffic usage, energy consumption, service reliability, and security/privacy of content distribution.

Through comprehensive real-world measurements, unfortunately, we observe that existing content distribution techniques often exhibit undesirable or even poor performance under the above-described new settings. Motivated by the trend of “heavy-cloud vs. light-end,” this book is dedicated to uncovering the root causes of today’s mobile networking problems and designing innovative cloud-based solutions to practically address such problems, in terms of four key metrics: Speed (Part II), Cost (Part III), Reliability (Part IV), and Security (Part V).

Our work included in this book has led to not only academic papers published in prestigious conferences like SIGCOMM, NSDI, MobiCom, and MobiSys, but also actual effect on industrial systems such as Xiaomi Mobile, MIUI OS, Tencent App Store, Baidu PhoneGuard, UUTest.cn, and WiFi.com. In addition, the included work has won several academic awards, e.g., Best Student Paper Award of the ACM MMSys 2017 conference, Excellent Paper Award of the Tsinghua Science and Technology 2019 journal, Best Demo Award of the ACM MobiCom 2019 conference, and Best Student Paper Award of the ACM SIGCOMM 2021 conference (the first time Asian scholars get this award from SIGCOMM).

In this book, we provide a series of insightful measurement findings and firsthand system experiences to researchers and practitioners working on mobile Internet and cloud computing/storage. Additionally, we have released as much code and data used in our work as possible to benefit the community. Should you have any questions or suggestions, please contact the four authors (in particular the first author) via lizhenhua1983@gmail.com, dyf@pku.edu.cn, gchen@cs.sjtu.edu.cn, and yunhaoliu@gmail.com.

Finally, we sincerely appreciate the professional assistance from Celine Chang, Jingying Chen, Lenold Esithor, Christina Fehling, Ramesh Marimuthu, and Ellen Seo at Springer Press. Also, we would like to thank the following people for their contributions to this book: Sen Bai, Jian Chen, Qi Chen, Yan Chen, Fan Dang, Di Gao, Liangyi Gong, Taeho Jung, Xiangyang Li, Yang Li, Hao Lin, Zhen Lu, Kebin Liu, Wei Liu, Yao Liu, Rui Miao, Chen Qian, Feng Qian, Zhiyun Qian, Weiwei Wang, Xianlong Wang, Yinlong Wang, Christo Wilson, Ao Xiao, Xianlong Xin, Tianyin Xu, Jinyu Yang, Xinlei Yang, Ennan Zhai, Lan Zhang, Ben Zhao, and Xin Zhong. In particular, we are grateful for Yannan Zheng’s helping typeset several chapters of this book.

Beijing, China

Beijing, China

Shanghai, China

Beijing, China

December 2021

Zhenhua Li

Yafei Dai

Guihai Chen

Yunhao Liu

# Acknowledgments

This work is supported in part by the National Key R&D Program of China under grant 2022YFB4500703; the National Natural Science Foundation of China (NSFC) under grants 61902211 and 62202266; and Microsoft Research Asia.

# Contents

# Part I Get Started

# 1 Background and Overview 3

1.1 Internet Content Distribution 3   
1.2 Cloud Computing and Mobile Internet . 7   
1.3 Frontier Techniques 8   
1.4 Overview of the Book Structure . 13   
References . 14

# Part II Metric 1 Speed: Bandwidth Is the First

# 2 Fast and Light Bandwidth Testing for Mobile Internet 19

2.1 Introduction. 19   
2.2 Understanding State-of-the-Art BTSes. 22   
2.2.1 Methodology 22   
2.2.2 Analyzing Deployed BTSes 23   
2.2.3 Measurement Results 24   
2.2.4 Case Studies . 25

2.3 Design of FastBTS 28

2.3.1 Crucial Interval Sampling (CIS) 29   
2.3.2 Elastic Bandwidth Probing (EBP). 32   
2.3.3 Data-Driven Server Selection (DSS) 36   
2.3.4 Adaptive Multi-Homing (AMH) 37

2.4 Implementation . 38

2.5 Evaluation 38

2.5.1 Experiment Setup 38   
2.5.2 End-to-End Performance 40   
2.5.3 Individual Components 42

2.6 Concluding Remarks 45

References . 46

# 3 Offline Downloading via Cloud and/or Smart APs 49

3.1 Introduction. 49   
3.2 Related Work 53   
3.3 System Overview . 55

3.3.1 Overview of Xuanfeng. 55

3.3.2 Overview of the Smart AP Systems . 56

3.4 Workload Characteristics 58   
3.5 Performance of the Cloud-Based System 61

3.5.1 Pre-downloading Performance 61   
3.5.2 Fetching Performance. 63   
3.5.3 End-to-End Performance 66

3.6 Performance of the Smart APs. 66

3.6.1 Methodology 66   
3.6.2 Benchmark Results 68

3.7 The ODR Middleware. 71

3.7.1 Design and Implementation 71   
3.7.2 Performance Evaluation 74

3.8 Conclusion . 75

References . 76

# Part III Metric 2 Cost: Never Waste on Traffic Usage

# 4 Cross-Application Cellular Traffic Optimization 81

4.1 Introduction. 81   
4.2 State-of-the-Art Systems . 84   
4.3 Measuring Cellular Traffic . 86

4.3.1 Dataset Collection. 87   
4.3.2 Content Analysis . 88

4.4 System Overview . 91   
4.5 Mechanisms 94

4.5.1 Image Compression 94   
4.5.2 Content Validation 96   
4.5.3 Traffic Filtering 97   
4.5.4 Value-Based Web Caching (VBWC). 98

4.6 Evaluation 99

4.6.1 Data Collection and Methodology 99   
4.6.2 Traffic Reduction. 100   
4.6.3 System Overhead 102   
4.6.4 Latency Penalty 107

4.7 Conclusion . 108

References . 109

# 5 Boosting Mobile Virtual Network Operator . 111

5.1 Introduction. 111   
5.2 Background . 114   
5.3 Measurement Data Collection 116

5.4 Data Usage Characterization. 117   
5.5 Network Performance . 122   
5.6 Data Usage Prediction and Data Reselling Optimization 124

5.6.1 Data Usage Prediction and Modeling 124   
5.6.2 Data Reselling Optimization 128

5.7 Customer Churn Profiling and Mitigation. 130   
5.8 Inaccurate Billing in MVNO 134   
5.9 Related Work . 136   
5.10 Concluding Remarks 136

References . 137

# Part IV Metric 3 Reliability: Stay Connected All the Time

# 6 Enhancing Nationwide Cellular Reliability. 143

6.1 Introduction. 143   
6.2 Study Methodology 146

6.2.1 Limitations of Vanilla Android . 146   
6.2.2 Continuous Monitoring Infrastructure 148   
6.2.3 Large-Scale Deployment 150

6.3 Measurement Results 150

6.3.1 General Statistics. 151   
6.3.2 Android Phone Landscape. 153   
6.3.3 ISP and Base Station Landscape 159

6.4 Enhancements 162

6.4.1 Guidelines in Principle. 162   
6.4.2 Real-World Practices 163   
6.4.3 Deployment and Evaluation 168

6.5 Conclusion . 170

References . 170

# 7 Legal Internet Access Under Extreme Censorship 173

7.1 Introduction. 173   
7.2 Extreme Internet Censorship. 175   
7.3 The ScholarCloud System 177   
7.4 Measurement Study 179

7.4.1 Common Practices 179   
7.4.2 Methodology 180   
7.4.3 Measurement Results 181

7.5 Related Work 185   
7.6 Limitation and Discussion 185

References . 186

# Part V Metric 4 Security: Do Not Relax Our Vigilance

# 8 Combating Nationwide WiFi Security Threats 191

8.1 Introduction. 191

8.2 Study Methodology 195

8.2.1 WiSC System Overview 195   
8.2.2 LAN Attack Detection . 196   
8.2.3 WAN Attack Detection 199   
8.2.4 Evaluation 203   
8.2.5 Large-Scale Deployment and Field Survey 204

8.3 Measurement Results 205

8.3.1 Prevalence of WiFi Attacks. 205   
8.3.2 WiFi-Based Attack Techniques 207   
8.3.3 Malicious Behaviors and Objectives . 209   
8.3.4 Fundamental Motives Behind the Attacks 211

8.4 Undermining the Attack Ecosystem . 214

8.4.1 Uncovering the Underground Ecosystem 215   
8.4.2 Interplay and Weakness. 216   
8.4.3 Real-World Active Defense Practices . 216

8.5 Conclusion . 217

References . 218

9 Understanding IoT Security with HoneyCloud 221

9.1 Introduction. 221   
9.2 Honeypot Deployment 224

9.2.1 Overview 225   
9.2.2 Hardware IoT Honeypots 227   
9.2.3 Software IoT Honeypots . 229

9.3 Findings and Implications 233

9.3.1 General Characteristics and Statistics . 233   
9.3.2 Malware-Based Attacks 236   
9.3.3 Fileless Attack Taxonomy 237   
9.3.4 Key Insights for Fileless Attacks 241   
9.3.5 New Security Challenges and Defense Directions 242

9.4 Conclusion . 243

References . 244

# Part VI Last Thoughts

10 Concluding Remarks . 247

10.1 Emerging Techniques 247   
10.2 Future Work 249

References . 251

# About the Authors

Zhenhua Li is an associate professor at the School of Software, Tsinghua University. He obtained his PhD degree in Computer Science from Peking University in 2013. His research interests are chiefly in mobile networking, cloud computing, and big data analysis. His work focuses on understanding realistic problems in today’s large-scale mobile (cellular, WiFi, and IoT) systems, and on developing innovative solutions to practically address them. His research has produced not only academic papers published in prestigious conference proceedings like SIGCOMM, NSDI, MobiCom, and MobiSys, but also concrete effects on industrial systems such as Xiaomi Mobile, MIUI OS, Tencent App Store, Baidu PhoneGuard, and WiFi.com, benefiting hundreds of millions of mobile users.

Yafei Dai is a full professor at the School of Electronics Engineering and Computer Science (EECS), Peking University. Before joining Peking University, she held positions as a full professor, associate professor, and assistant professor at the Department of Computer Science and Technology, Harbin Institution of Technology (HIT) in China starting in 1987. She obtained PhD degree, MS degree, and BE degree from HIT in 1993, 1986, and 1982, respectively. Her research interests are mainly in distributed systems, storage systems, and social networks. She has published over 100 academic papers in competitive conference proceedings and journals.

Guihai Chen is a distinguished professor at the Department of Computer Science and Engineering, Shanghai Jiao Tong University. He earned his PhD degree in Computer Science from the University of Hong Kong in 1997 and has served as a visiting professor at Kyushu Institute of Technology in Japan, the University of Queensland in Australia, and Wayne State University in the USA. He has a wide range of research interests in parallel computing, wireless networks, peer-to-peer computing, high-performance computer architecture, and so on. He has published more than 200 papers in competitive conference proceedings and journals. He has won many honors and awards, in particular the First Prize of Natural Sciences by the Ministry of Education of China.

Yunhao Liu is a Changjiang professor and dean of Global Innovation Exchange at Tsinghua University. He received his PhD degree and MS degree in Computer Science from Michigan State University in 2003 and 2004, respectively, and his BS degree from the Automation Department of Tsinghua University in 1995. His research interests include distributed systems, wireless sensor networks/RFID, Internet of Things (IoT), etc. He has published over 300 papers in prestigious conference proceedings and journals, as well as two books: “Introduction to IoT” and “Location, Localization, and Localizability.” He is currently the Editor-in-Chief of ACM Transactions on Sensor Networks and Communications of China Computer Federation. He is a fellow of the ACM and IEEE.

# Acronyms

ABR Adaptive bitrate streaming

AMH Adaptive multi-homing

AP Access point, or WiFi home router

ARF Acceptance-rejection function

BCCH Broadcast control channel

BTS Bandwidth testing service

C/S Client/Server content distribution

CCN Content centric networking

CDN Content distribution (delivery) network

CIS Crucial interval sampling

CSP Cloud services provider

DPDK Data plane development kit

DSS Data-driven server selection

DTN Delay-tolerant networking

EBP Elastic bandwidth probing

EC2 Elastic compute cloud

GFW Great firewall

HLS HTTP live streaming

ICN Information centric networking

IoT Internet of Things

IRB Institutional review board

ISP Internet service provider

IXP Internet eXchange point

LAN Local area network

LTE Long term evolution

MVNO Mobile virtual network operator

NDN Named data networking

NIC Network interface controller

ODR Offline downloading redirector

P2P Peer-to-peer content distribution

P2SP Peer-to-server and Peer content distribution

<table><tr><td>PAC</td><td>Proxy auto-config</td></tr><tr><td>PIX</td><td>Peering via Internet eXchange</td></tr><tr><td>QoS</td><td>Quality of service</td></tr><tr><td>RAT</td><td>Radio access technology</td></tr><tr><td>RDMA</td><td>Remote direct memory access</td></tr><tr><td>RFID</td><td>Radio frequency identification device</td></tr><tr><td>RSS</td><td>Received signal strength</td></tr><tr><td>SDN</td><td>Software-defined networking</td></tr><tr><td>SNR</td><td>Super node relay</td></tr><tr><td>SPDK</td><td>Storage performance development kit</td></tr><tr><td>SUR</td><td>State update report</td></tr><tr><td>TIMP</td><td>Time-inhomogeneous Markov process</td></tr><tr><td>UHD</td><td>Ultra high definition</td></tr><tr><td>UIO</td><td>User-space I/O framework</td></tr><tr><td>VNO</td><td>Virtual network operator</td></tr><tr><td>WAN</td><td>Wide area network</td></tr><tr><td>WWW</td><td>World wide web, or “world wide wait”</td></tr></table>