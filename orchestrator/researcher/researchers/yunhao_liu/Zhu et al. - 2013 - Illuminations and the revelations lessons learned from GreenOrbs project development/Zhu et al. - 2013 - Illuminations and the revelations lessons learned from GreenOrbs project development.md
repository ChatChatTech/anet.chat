# Illuminations and the Revelations : Lessons Learned from GreenOrbs Project Development

Tong Zhu Zhichao Cao Wei Gong Yuan He Yunhao Liu

{zhutong,caozc,gongwei,heyuan,yunhao}@greenorbs.com

School of Software and TNList, Tsinghua University

Wireless sensor networks (WSNs) are developed in an accelerated pace during the past years. Motivated by the need of closely monitoring the forest and urban environments and accurately measuring carbon sequestration and emission, we launched two long-term large-scale WSNs: “GreenOrbs” in 2009 and “CitySee” in 2011, respectively. This paper presents our recent advances and experience on how to implement the two WSNs with stable and high performance. Some research directions are also discussed based on our observations and measurements.

# I. Introduction

Recent several years have witnessed the prosperous development of Wireless Sensor Networks (WSNs). Many projects have been launched for various applications, such as environmental surveillance, event detection, target tracking, and habitat monitoring. Those projects, however, do not emphasize long-term operations and large-scale deployments, as shown in Table 1. To reveal the difficulties of large-scale and long-term implementation of WSNs, we launched “GreenOrbs” $^{1}$ in 2009, to support a series of forestry applications, such as canopy closure estimation [7] and carbon sink estimation.

In 2011, we extended the GreenOrbs system and deployed “CitySee” with 1196 sensor nodes and 4 mesh nodes in Wuxi city of China for urban sensing. CitySee aims at continuously measuring air quality and carbon emissions in the urban area. The reasons why we extend our system from forest to urban area are two-fold. 1) for the completion of carbon monitoring. In the forest we focus on carbon sink measurement while in urban area we turn to monitor and measure carbon emissions. The combination of those two works facilitates us build a complete framework for monitoring carbonnitrogen cycle. 2) to broaden our research on WSNs. We have collected a series of new techniques through our two-year research experience in GreenOrbs. We are interested to know whether such ideas, techniques and approaches still work and what unique research challenges appear in urban deployments.

In this paper, we will briefly review our recent advances and experience on GreenOrbs and CitySee, and discuss some research directions based on our measurement results.

Table 1: Sensor network deployments 

<table><tr><td>System</td><td>Deployment</td><td>Scale</td><td>Duration</td></tr><tr><td>VigilNet</td><td>Outdoor</td><td>200</td><td>3~6 months</td></tr><tr><td>Motelab</td><td>Indoor</td><td>190</td><td>N/A</td></tr><tr><td>SensorScope</td><td>Outdoor</td><td>97</td><td>6 months</td></tr><tr><td>Trio</td><td>Outdoor</td><td>557</td><td>4 months</td></tr><tr><td>ExScal</td><td>Outdoor</td><td>1200</td><td>14 days</td></tr></table>

# II. GreenOrbs Project Development

Figure 1 shows the overview of development of GreenOrbs project. GreenOrbs prototype system was initially deployed at university woodland in Lin'an in May 2009. The network scale was expanded to 330 nodes in November 2009 and the mountain deployment includes 200 nodes which covers $0.2\ km^2$ forestry area since August 2009. CitySee, as the second phase of the GreenOrbs Project, was deployed in the Wuxi High-tech Development Zone. The initial prototype of CitySee was deployed on 30 May 2011, and this network includes 100 nodes. In early July 2011, we expanded the system scale to 300 nodes. The system's scale reached 700 nodes on 13 July 2011. In early August 2011, the system reached its current scale, 1196 nodes and 4 mesh nodes. The current deployment of CitySee covers $1.12\ km^2$ urban areas. We are now trying to deploy up to 4,000 sensor nodes in a larger area in Wuxi.

GreenOrbs leverages a single-layer network architecture. Each node samples certain environmental conditions, such as temperature, humidity, light and so on. The sensed data are delivered to the sink through this ad-hoc network using Collection Tree Protocol [2]. As an extension of GreenOrbs from forest to the urban area, CitySee, uses a multi-subnet layered structure. Sensor nodes deliver data to the mesh node using the same subnet; and 4 mesh nodes deliver gathered data to the data center through mesh networks.

![](images/65cfca894cc1dbc5d3a1e13c7bda761829164f1f4388436ee30762ace332a153.jpg)



![](images/955d7b97fd43982abdd591f1fe051ff43bebf18358bf169e4e71acb07fd3f711.jpg)



Figure 1: The development of GreenOrbs project. 1) Overview of the development of GreenOrbs project. 2) The bird's-eye picture of GreenOrbs prototype system. 3) The satellite picture of deployed areas in Timu mountain. 4) Real deployed scenario in CitySee. 5) The topology of CitySee. 6) The bird's-eye picture of one of subnetworks in CitySee.

![](images/ac8b4da613f37e477fe4da45922a34675c677408c4e8dd20cea5345c4c6da711.jpg)



(a)

![](images/eeae0aee53faf43e718097aaf25f298f89f6d24cbb414fd5834739aa3fbb262b.jpg)



(b)

![](images/8865bebb1dfdb9370d5a3a8245bb4c17d6b8db61333ef43f61b1df22ffc1b1f2.jpg)



(c)   
Figure 2: Spatial distribution of network metrics: (a) # of packets transmitted (b) radio duty cycle (c) # of parent changes

# III. Research Efforts

# III.A. Spatial & Temporal Properties

We first have a look at the spatial and temporal properties of some network metrics in our WSNs. This statistical information bring us intuitions that how our network performs. Figure 2 shows the spatial distributions of the three network metrics, including the number of parent changes, radio duty cycle and the number of packets transmitted in one subnet of “City-See” from August 3 through August 9. In Figure 2, we can see that different metrics show diverse patterns though the data are evenly collected from sensor nodes in the network. As illustrated in Figure 2b, some sensor nodes close to the sink experience high radio duty cycles while the other nodes maintain low power consumption. Intuitively, high radio duty cycle is due to heavy traffic load. In practice, however, the results in Figure 2a and Figure 2b describe that not all sensor nodes carrying heavy traffic load have high radio duty cycles. Parent-change is also regarded as a good indicator of routing performance. As shown in Figure 2c, parent-change events happen unevenly in the network. Many nodes switch their parents frequently, which reflects highly dynamic link quality to some degree.

![](images/a366b3a18991dc654f179fd716ab11abb2f2d6750df2ae9552e02d0ab9ed6112.jpg)



(a)

![](images/9b97d2fc7d134feab1db226501a89a0db597a0c70eec750e942209a6ebf347a1.jpg)



(b)   
Figure 3: Traffic trends in two subnetworks of CitySee

Figure 3 is a streamgraph, showing traffic trends for each node in two subnets of CitySee over one week. Each color layer represents a node and the height of each layer refers to aggregated traffic loads within one hour. Notably, even with similar network configurations (e.g., network scale, diameter, sample rate), two subnets exhibit diverse traffic patterns. In Figure 3a, some nodes always carry heavy traffic (large height layer), while the traffic distributes more uniformly in Figure 3b.

# III.B. Measurement Results & Findings on Protocol Designs

Based on the initial efforts and early experience in GreenOrbs, we propose and validate three conjectures which cover some fundamental issues: the distribution of critical nodes, dynamics of network behaviors and the impact of varied environments $[5]$ . Furthermore, to figure out why packet reception ratio cannot reach 100% in our system, we correlate system and environment events with packet loss events based on temporal and spatial relationship. Totally we correlated 66.57% of packet losses with different root causes. The results are shown in Figure 4. In City-See, we conduct extensive experiments to study the link-level behaviors. The measurement results primarily show temporal-spatial characteristics of links, the reasons of link performance degradation, and the impact of link performance on wireless ad hoc routing. Guided by these observations, we revisit traditional network metrics and design novel protocols for large-scale WSNs, e.g., cross-layer bursty-aware forwarding technique, comprehensive metric of wireless path quality, duty-cycle controlling technique to achieve min-max energy-fairness in asynchronous WSNs, etc.

Besides, compared to GreenOrbs deployed in the forest, the deployment of large-scale WSNs in urban areas faces more challenges. For example, the buildings, which block or reflect wireless signals, play a key role in the deployment. Hence, how to minimize the number of deployed sensor nodes to guarantee sensing data collection from predefined locations is a critical task. Our study on this issue is presented in $[6]$ .

# III.C. Diagnosis

According to the management experience from GreenOrbs and CitySee, we propose some requirements for the diagnosis in large-scale WSNs:

\- Self/local judgement. Coarse-grain diagnosis can be completed with symptom observations, while fine-grained diagnosis needs to analyze detailed in-network information. Here we discuss two ways to collect evidences. Similar to SNMP, an Internet-standard protocol for managing devices on IP networks, sink-based diagnosis requires the sensor nodes to send their status information to the sink. Therefore, the managers are able to apply comprehensive diagnosis algorithms to find out the root causes based on a big picture of the network. In practice, however, leaving aside the huge overhead required in the collection, sink often fails to obtain complete and credible information from a problematic region. To solve this issue, self/local-diagnosis claims that diagnosis process can be conducted by one or more nodes within a local area. This approach largely reduces the overhead and delay, but suffers from limited knowledge and resources. Hence, to obtain diagnosis results in a timely way, self-diagnosis and local-decision schemes are necessary complementarities to traditional sink-based approaches.

![](images/adcaad902477ff1e55188b97daacd3ef01703da2039597cc3bf5d882bd869cce.jpg)



Figure 4: Root causes of packet loss   
![](images/63fa31c75ca7544eda45ab38ed5e4232d0b5f99c4d60b2540ad630158293d19f.jpg)



Figure 5: PRR vs entropy of packet delivery

![](images/b95f8ea2043c27a8b1df36dbcd66ed3c187ff42b44af88a87dec2946bbe22443.jpg)



Figure 6: CDF of Routing and non-routing link PRR

\- On-demand diagnosis. Besides the retrieval of related evidences, different algorithms also impact the granularity and accuracy of diagnosis results. Many rule-based algorithms define the relationship between root causes and symptoms by setting heuristic thresholds. Inference-based approaches design some certain metrics which are able to reflect network events. Then these metrics embedded into nodes can be combined to explain network performances. The former approach aims to give a global diagnosis for the network, while the latter one is always used to focus on specific issues. Hence, we propose two management layers. The first layer consists of extremely lightweight anomaly detectors for routine maintenance management. If any indicator of faults occurs, fine-grained diagnosis tools in the second layer are triggered to localize and characterize various faults.

\- Mobile diagnosis. In cases of large correlated sensor failures and network partitions, mobile diagnosis devices and methods are of great importance since no information about “incorrect” sensors can be acquired through other “correct” sensors and sink. What information needs to be collected and how to collect are two major issues in those fault-masked situations.

# IV. Future Directions

# IV.A. Network Architecture

Traffic load imbalance is a common phenomenon in large-scale WSNs, especially in urban areas where the geographical deployment environments are always non-uniform. In Figure 3, we find that some sensor nodes with high traffic loads locate at “critical regions” like the crossroads. There are few alternative relaying nodes for routing selections in those areas. Besides, low-cost sensor nodes are prone to failure and commonly we deploy in higher than necessary densities to guarantee routing redundancy and operational functions. It wastes lots of energy on maintaining connected network topology [4]. Facing those challenges, we propose some questions: should we reconsider a new network architecture to provide the routing redundancy by increasing more relay choices? Do those nodes in “critical regions” have great impact on routing performance? Can we achieve higher system performances, e.g., maximal throughput and maximal lifetime, simultaneously.

# IV.B. Routing

Dynamic routings are affected by environmental dynamics, such as weather changes, static or moving obstructions and WiFi interferences $[3]$ . These dynamics have great impact on predicting the quality of wireless links. It leads to unstable routing decisions and fluctuating system performances. Figure 5 shows the scatter plot of Packet Reception Ratio (PRR) and the entropy of packet delivery. We see that high-quality links have more predictable performance while intermediate links are less predictable. We know that high dynamics of wireless conditions incur heavy overhead on maintenance of tree-based routing structures. The key problem is how to adaptively estimate the time-varying link quality. Neither the long-term nor short-term link qualities reflect the dynamics of wireless channel conditions accurately. Figure 6 shows the CDF of PRR of the routing and non-routing links. Though average routing link performance is better than non-routing link, there are still over 20% routing links whose PRRs are less than 0.9. Do such routing links actually provide benefits to routing performance? Or can we find some alternative links to achieve higher PRR for each node?

# IV.C. Reprogramming

Wireless sensor networks are always deployed where frequently collecting sensor nodes is infeasible. Wireless reprogramming techniques provide significant convenience for the WSN developers. Considering the limited resources on sensor nodes, wireless reprogramming faces several challenges including reduction of transferred code size, minimization of new code loading cost and avoiding flash writes which needs higher voltage than normal operations for common sensor nodes, such as TelosB. Besides, a safe update process of the program is very important. Some critical parts, as system kernel and system interfaces cannot be touched in reprogramming process, otherwise occasional errors will be incurred unconsciously.

# IV.D. Debugging

Software debugging of WSNs is difficult compared with debugging general purpose computer systems. Debugging processes are always done by wiring hardware or using a certain debugging language $[1]$ . The former one needs special equipments and becomes infeasible for debugging at large-scale. The latter one is expensive in terms of memory, energy and communication bandwidth. In large-scale WSN, the debugging technique is expected to provide remote source-level debugging service. Being a potential solution, remote source-level debugging still faces many challenges, such as source-level debugging of symbols and efficient remote control of the debugging process. Regarding the long-term operations of WSNs, there is substantial need of updating the software. Sustainable online debugging is thus a significant issue but does not have an affordable and effective solution so far.

# IV.E. Interaction with Smartphones

Within the development of large-scale WSNs in urban areas, interactions among WSNs and other smart devices, e.g., smartphones, become more and more frequent. In one aspect, people can use smart phones as mobile sinks to access WSNs and fetch informative and interesting data in a timely manner. For example, according to the local temperature and the air quality, smartphone may offer a real-time running path for people in morning exercises. In the other aspect, smart devices, as communication devices, provide potential communication ability to bridge WSNs in physically disconnected areas. It avoids relaying on powerful but expensive communication hardware e.g. WiMAX equipments. Many research problems are proposed in those interactions, e.g. simple and convenient interaction interfaces, the utilization of those interaction data for each platform, and efficient storage and processing of the dynamic heterogeneous data.

# V. Acknowledgement

This work is supported in part by the NSFC Major Program under Grants No. 61190110, National Basic Research Program (973 program) under Grant of 2014CB347800, NSFC under Grants No. 61170213, the NSFC Young Scholar 61103187, and China Postdoctoral Science Foundation No.2013M540950.

# References

[1] Qing Cao, Tarek F. Abdelzaher, John A. Stankovic, Kamin Whitehouse, and Liqian Luo. Declarative tracepoints: a programmable and application independent debugging system for wireless sensor networks. In Proceedings of ACM SenSys, pages 85–98, 2008.   
[2] Omprakash Gnawali, Rodrigo Fonseca, Kyle Jamieson, David Moss, and Philip Levis. Collection tree protocol. In Proceedings of ACM SenSys, pages 1–14, 2009.   
[3] Jun Huang, Guoliang Xing, Gang Zhou, and Ruogu Zhou. Beyond co-existence: Exploiting wifi white space for zigbee performance assurance. In Proceedings of IEEE ICNP, pages 305–314, 2010.   
[4] Rajagopal Iyengar, Koushik Kar, and Suman Banerjee. Low-coordination topologies for redundancy in sensor networks. In Proceedings of ACM MOBIHOC, pages 332–342, 2005.   
[5] Yunhao Liu, Yuan He, Mo Li, Jiliang Wang, Kebin Liu, Lufeng Mo, Wei Dong, Zheng Yang, Min Xi, Jizhong Zhao, and Xiang-Yang Li. Does wireless sensor network scale? a measurement study on greenorbs. In Proceedings of IEEE INFOCOM, pages 873–881, 2011.   
[6] XuFei Mao, Xin Miao, Yuan He, Xiang-Yang Li, and Yunhao Liu. Citysee: Urban co2 monitoring with sensors. In Proceedings of IEEE INFOCOM, pages 1611-1619, 2012.   
[7] Lufeng Mo, Yuan He, Yunhao Liu, Jizhong Zhao, ShaoJie Tang, Xiang-Yang Li, and Guojun Dai. Canopy closure estimates with greenorbs: sustainable sensing in the forest. In Proceedings of ACM SenSys, pages 99–112, 2009.