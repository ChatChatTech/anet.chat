RESEARCH ARTICLE

# Long-term large-scale sensing in the forest: recent advances and future directions of GreenOrbs

Yunhao LIU1,2, Guomo ZHOU3 , Jizhong ZHAO4 , Guojun DAI5 , Xiang-Yang LI1 , Ming GU1 , Huadong MA6 , Lufeng MO3 , Yuan HE (✉) 1,2, Jiliang WANG1,2, Mo LI1,2, Kebin LIU1,2, Wei DONG7 , Wei XI4

1 National Lab for Information Science and Technology, School of Software, Tsinghua University, Beijing 100084, China   
2 Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong, China   
3 School of Information Science and Technology, Zhejiang A&F University, Hangzhou 311300, China   
4 Department of Computer Science and Technology, Xi’an Jiao Tong University, Xi’an 710049, China   
5 Computer School, Hangzhou Dianzi University, Hangzhou 310018, China   
6 School of Computer Science and Technology, Beijing University of Posts and Telecommunications, Beijing 100876, China   
7 College of Computer Science and Technology, Zhejiang University, Hangzhou 310027, China

© Higher Education Press and Springer-Verlag Berlin Heidelberg 2010

Abstract We introduce GreenOrbs, our recent effort in exploring the fundamental challenges and future direction of long-term large-scale applications of wireless sensor networks. An integrated framework with more than 1000 sensors has been implemented, including the indoor test bed, prototype systems, and forest deployment: comprehensively supporting research, development, and forestry applications.

Keywords sensor network, large-scale, long-term

# 1 Introduction

Since they were first proposed a decade ago, wireless sensor networks (WSNs) have been applied to a wide variety of fields, such as environmental surveillance, industrial control, traffic monitoring, home automation, and safeguarding, etc.

There have been a number of well-known WSN systems and deployments. By far the largest deployment called ExScal [1] included more than 1000 nodes, but it was kept in operation for only a few days. A SensorScope [2] deployment is the longest living project of all previous deployments, lasting for around 6 months, but the system consists of no more than 97 nodes. Trio [3] realized a

continuous outdoor deployment of 557 nodes for 4 months. It employed solar-powered sensor motes, however, which avoids the energy constraints on system design.

Do WSNs really scale? What are the fundamental challenges in deploying long-term large-scale WSNs?

To explore the answers to the above questions, we launched GreenOrbs [4], a collaborative research project to study long-term large-scale WSNs in a forest environment. The early experiences of GreenOrbs deliver many lessons on deploying a long-term large-scale WSN in wild environments. In this paper we present our findings so far and discuss our future research directions.

Section 2 briefly introduces the forestry applications of GreenOrbs. In Section 3, we present the latest advances on forest deployment, prototype system, and, indoor test bed, respectively. Section 4 discusses the future research directions and presents the observations and experimental results obtained by far, followed by the conclusion in Section 5.

# 2 GreenOrbs applications

“The world has just ten years to bring greenhouse gas emissions under control before the damage they cause becomes irreversible” [5]. This is a famous prediction recently made by climate scientists and environmentalists. It reflects the increasing attention from human beings in the past decade on global climate change and environmental pollution. On the other hand, forests, which are regarded as the earth’s lungs, are a critical component in the global carbon cycle. They are able to absorb 10%– 30% of $\mathrm { C O } _ { 2 }$ from industrial emissions. Moreover, they have large capacity for water conservation, preventing water and soil loss, hence reducing the chance of natural disasters like mud-rock flows and floods. Regarding the above points, forest management and surveillance become more and more important.

Forestry applications usually require long-term, largescale, continuous, and synchronized surveillance of huge measurement areas with diverse creatures and complex terrains. The state-of-the-art forestry techniques, however, support only small-scale, discontinuous, asynchronous, and coarse-grained measurements, which at the same time incur large amount of cost with respect in terms of human resources and equipment.

WSNs have great potential in resolving the challenges in forestry. The information GreenOrbs offers can be used as evidence, reference, and provides scientific tools for human beings in the battle against global climate changes and environmental pollution. GreenOrbs currently supports a variety of applications.

Carbon sequestration To maximize the utility of forest carbon sequestration, the capacity of carbon sequestration of different tree species needs to be accurately measured. This can be realized using carbon dioxide sensors in three-dimensional forest space.

Canopy closure estimates It is defined as the percentage of ground area vertically shaded by overhead foliage. It is a widely-used significant forestry indicator. However, traditional measurement techniques have either poor accuracy or prohibitive cost. Using WSN as a quantitative measurement technique, GreenOrbs realizes accurate canopy closure estimates at low cost [6].

Study of biodiversity The sensor readings of temperature, humidity, and illuminance precisely characterize the microclimate in the forest. Compared to traditional forestry approaches, GreenOrbs have apparent advantages. Surveillance can be long-term and continuous, while the measurement is generally inexpensive and fine-grained.

Fire risk prediction Traditional techniques provide only inaccurate forecasts according to the macroscopic weather conditions, such as temperature, humidity, and wind force. The real fire risks, however, are indeed closely related to the microscopic ground conditions and human activities. GreenOrbs is able to monitor the local environmental factors, namely temperature and humidity. Those data act as important input elements of fine-grained real-time fire risk prediction [7].

# 3 Recent advances

We use TelosB [8] motes with MSP430 F1611 processor and CC2420 radio. The software on the sensor nodes is developed on top of TinyOS 2.1 [9].

Collection Tree Protocol CTP [10] is adopted for multihop sensor data collection, wherein the beacon frequency is reduced to save communication cost. Data dissemination from the base station is able to control the nodes’ operational parameters, such as transmission power, sampling frequency, and duty cycle. Table 1 lists the functions and supporting software components of the sensors. The manufacturing cost of a GreenOrbs node is 50 US dollars.

Table 1 Sensors on a GreenOrbs node 

<table><tr><td>Sensor</td><td>Function</td><td>*Software</td></tr><tr><td>Sensirion Sht11</td><td>Temp. &amp; humidity</td><td>SensirionSht11C</td></tr><tr><td>Hamamatsu S1087</td><td>Illuminance</td><td>HamamatsuS1087ParC</td></tr><tr><td>Voltage sensor</td><td>Battery voltage</td><td>VoltageC</td></tr><tr><td>GE Telaire 6004</td><td>Content of CO2</td><td>Self-developed</td></tr></table>

So far we have implemented three deployments of GreenOrbs, including the forest deployment in the Tianmu Mountain, the prototype systems on campus hills, and the indoor test bed. Table 2 summarizes the current information of our three deployments. We carry out debugging tests for GreenOrbs programs and protocols on the test bed, so as to ensure the correctness and efficiency of our design. The prototypes provide real contexts for outdoor experiments and observations on the networking system, while the Tianmu mountain deployment focuses on supporting real applications. As of April 2010, we have collected more than 5240000 valid data packets from GreenOrbs, which accounts for over 600 MB.

Table 2 Information of typical GreenOrbs deployments 

<table><tr><td>Deployment</td><td>Scale</td><td>Duration</td><td>Power</td></tr><tr><td>Tianmu Mount.</td><td>200</td><td>8 months</td><td>~8000 mAh D batteries</td></tr><tr><td>Prototype</td><td>400</td><td>12 months</td><td>~8000 mAh D batteries</td></tr><tr><td>Test bed</td><td>160</td><td>2 months</td><td>AC/USB/AA Batteries</td></tr></table>

The indoor test bed is shown in Fig. 1. It supports experiments with up to 150 nodes. The sensor data can be collected wirelessly and through wired USB communication. Sensor nodes are mapped to their serial port numbers to enable simultaneous high-speed reprogramming of the sensor nodes. The test bed nodes can use AC, USB, or AA batteries as the power supply. By incorporating a set of functions for online configuration, the test bed flexibly supports a wide variety of network experiments.

![](images/752ab56b3ce6f6bfdcaa4e71025e4d599cc851c20132ad1132af7fc98d242cf6.jpg)



Fig. 1 Picture of GreenOrbs testbed

The prototype systems are deployed in the campus woodland of Zhejiang A&F University. Figure 2 shows the bird's-eye picture of the current largest one. The deployment area is around $4 0 0 0 0 { \mathrm { m } } ^ { 2 }$ . It has been deployed since May 2009 and initially included 50 nodes. In November 2009 it was expanded to include 330 nodes. The system scale reaches 400 in April 2010. The duty cycle of nodes is set at 8%. The network diameter measured by hop-count is 12. The sensor data are published via the official GreenOrbs website [1].

The Tianmu Mountain deployment includes 200 + nodes and has been in continuous operation since August 2009. The deployment area is around $2 0 0 0 0 0 \ \mathrm { m } ^ { 2 } .$ , as shown in Fig. 3. The duty cycle of nodes is set at 5%. The network diameter measured by hop-count is 20.

# 4 Research focus

# 4.1 WSN management

Diagnosis and visibility The unreliable nature of wireless communications in WSNs makes it extremely challenging to ensure complete data collection. When network faults are present, diagnosis based on incomplete knowledge of the network often has poor accuracy and efficiency. Figure 4 shows the observations on three typical good links in GreenOrbs. We find that the link loss rate fluctuates with time and it seems independent of the traffic load. An immediate conjecture is that it is due to the environmental dynamics. But we can neither validate nor refute this point, because the limited network visibility with the current design of GreenOrbs disables a deterministic answer.

Based on the above observation, one of our future directions is to study and develop an easy-to-use diagnosis tool for WSNs [11]. The tool should be light-weight, universally applicable to mainstream WSN platforms, and efficient in providing powerful visualized diagnostic information for WSN developers. Another potential research issue is how to improve the visibility of protocol behavior, eliminating the irresolvable network faults during operations.

Wireless reprogramming The programs on the sensor nodes often need to be upgraded or replaced after deployment for various reasons, such as fixing bugs, patching security holes, and upgrading program functions. Collecting all nodes back, reprogramming using wired connection, and redistributing the nodes is extremely wasteful of human resources. Reprogramming over the air is a crucial technique to support long-term continuous deployment of WSNs. Due to the limited storage on each node and the unreliable nature of the asynchronous data transmissions, it is very difficult to maintain network consistency while reprogramming a WSN with numerous sensor nodes [12].

![](images/45fa7a55bef9d0267f1dbed96d4b9acf77d40cf006067a29cd038d98924c8530.jpg)



Fig. 2 Bird's-eye picture of a GreenOrbs prototype (each blue point denotes a sensor node)

![](images/442bb578e59ca1ce54970b72d44b5a646827d559b6ddb8d5e56f0f46cfa49899.jpg)  
Fig. 3 Tianmu Mountain deployment

# 4.2 Data collection

Figure 5 shows eight network snapshots of eight consecutive operational periods of GreenOrbs. A higher color depth indicates a larger number of transmissions by a node. Intuitively the network traffic is unevenly distributed, while the distribution is relatively stable. This indicates the network has potential vulnerability to single point failure, while the energy consumption among the nodes is not well balanced. Another finding is that packet drops due to faulty node behavior account for nearly 39% of packet loss. Meanwhile, there are a non-negligible amount of outliers in the collected sensor data. To address these issues, our future research on data collection mainly includes three aspects, namely comprehensive characterization of routing path quality, efficient outlier detection, and assessment of topological resiliency [13,14].

![](images/f0fb90f57b48edce682efa4b65bda554a4d9eb2245a1253619d46915e479ef2d.jpg)  
Fig. 4 Traffic and loss rates on three typical links

# 4.3 Localization

Localization is a crucial task for GreenOrbs because the sensor data becomes useless unless the corresponding location information of nodes is present [15–18]. It is a very challenging issue, however, due to the non-uniform deployment of nodes, irregular and fluctuating signal strengths, and the influence from the complex terrain and obstacles in the forest. A potential approach for resolving the above challenges is to carefully manage the ranging quality during the localization process. Geometric methods can be utilized to sift the noisy measurements, while statistical methods can be used to realize robust location estimation against diverse ranging errors.

![](images/cabbc09786015ae9d47f40d0de4646e16087ec997f42eb22ea7d6ade41a0c13e.jpg)  
Fig. 5 Network traffic distribution over time

For better integration of forestry and WSN techniques, there are many other interdisciplinary issues to be studied, such as manufacture of inexpensive and precise sensors for $\mathrm { C O } _ { 2 }$ sensing, and the interoperability between Green-Orbs and forestry techniques.

# 5 Conclusion

This paper presents our recent advances with GreenOrbs, an interdisciplinary research project for long-term largescale sensing in the forest. GreenOrbs is established in China and involves the collaboration of a number of universities. Based on the early experience with Green-Orbs, we have discussed the future research directions, such as WSN management, wireless reprogramming, data collection, localization, and interdisciplinary issues.

Acknowledgements We would thank all the people who have contributed to GreenOrbs.

The principal investigators of GreenOrbs are Dr. Yunhao Liu, Dr. Jizhong Zhao, Dr. Guomo Zhou, Dr. Xiangyang Li, Dr. Guojun Dai, Dr. Ming Gu, Dr. Huadong Ma, and Dr. Mo Li.

Dr. Yuan He and Lufeng Mo are the project team leaders. The other team members mainly include Jiliang Wang, Zheng Yang, Xin Miao, and Zhichao Cao from Hong Kong University of Science and Technology, Kebin Liu from Shanghai Jiao Tong University, Wei Dong from Zhejiang University, Min Xi, Wei Xi, Shuo Lian, Rui Li, and Long Liu from Xi’an Jiao Tong University, Xingfa Shen from Hangzhou Dianzi University, Chao Wang from Beijing University of Posts and Telecommunications, Xufei Mao and Shaojie Tang from Illinois Institute of Technology, Shuo Liu from Zhejiang A&F University, Shuguang Xiong from Harbin Institute of Technology, Tao Chen from Nation University of Defense Technology, Danning Chen and Guowei Zou from Tsinghua University, Dongxu Duan and Xubao Jiang from Tongji University, and Zhenge Guo from Yanshan University.

# References

1. Arora A, Ramnath R, Ertin E, et al. ExScal: Elements of an extreme scale wireless sensor network. In: Proceedings of IEEE RTCSA, 2005

2. Barrenetxea G, Ingelrest F, Schaefer G, Vetterli M. The Hitchhiker’s Guide to Successful Wireless Sensor Network Deployments. In: ACM SenSys, 2008   
3. Dutta P, Hui J, Jeong J, et al. Trio: Enabling sustainable and scalable outdoor wireless sensor network deployments. In: Proceedings of ACM/IEEE IPSN, 2006   
4. GreenOrbs. http://www.greenorbs.org/   
5. MET office. http://www.australianclimatemadness.com/?p = 2213   
6. Mo L, He Y, Liu Y, Zhao J, Tang S, Li X Y, Dai G. Canopy closure estimates with GreenOrbs: Sustainable sensing in the forest. In: Proceedings of ACM SenSys, 2009   
7. Li M, Liu Y, Chen L. Nonthreshold-based event detection for 3D environment monitoring in sensor networks. IEEE TKDE, 2008, 20 (12): 1699–1711   
8. Polastre J, Szewczyk R, Culler D. Telos: enabling ultra-low power wireless research. In: Proceedings of ACM/IEEE IPSN, 2005   
9. Tiny O S. http://www.tinyos.net   
10. Gnawali O, Fonseca R, Jamieson K, Moss D, Levis P. Collection tree protocol. In: Proceedings of ACM SenSys, 2009   
11. Liu K, Li M, Liu Y, Li M, Guo Z, Hong F. Passive Diagnosis for Wireless Sensor Networks. In: Proceedings of ACM SenSys, 2008   
12. Dong W, Liu Y, Wu X, Gu L, Chen C. Elon: Enabling Efficient and Long-Term Reprogramming in Wireless Sensor Networks. In: Proceedings of ACM SIGMETRICS, 2010   
13. Lian J, Naik K, Liu Y, Chen L. Virtual surrounding face geocasting with guaranteed message delivery for Ad Hoc and sensor networks. In: Proceedings of IEEE ICNP, 2006   
14. Dong W, Chen C, Liu X, He Y, Chen G, Liu Y, Bu J. DPLC: Dynamic packet length control in wireless sensor networks. In: Proceedings of IEEE INFOCOM, 2010   
15. Yang Z, Liu Y. Understanding node localizability of wireless Adhoc networks. In: Proceedings of IEEE INFOCOM, 2010   
16. Yang Z, Liu Y, Li X. Beyond trilateration: On the localizability of wireless Ad-hoc networks. In: Proceedings of IEEE INFOCOM, 2009   
17. Li M, Liu Y. Rendered path: Range-free localization in anisotropic sensor networks with holes. In: Proceedings of ACM MobiCom, 2007   
18. Yang Z, Liu Y. Quality of trilateration: Confidence-based iterative localization. IEEE TPDS, 2010, 21: 631–640