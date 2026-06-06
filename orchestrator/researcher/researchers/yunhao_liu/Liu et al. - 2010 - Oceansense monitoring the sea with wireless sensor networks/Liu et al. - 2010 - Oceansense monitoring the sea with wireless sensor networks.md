# MobiCom 2009 Poster: OceanSense: Monitoring the Sea with Wireless Sensor Networks

Kebin Liu†, Zheng Yang†, Mo Li†, Zhongwen Guo‡, Ying Guo‡, Feng Hong‡, Xiaohui Yang‡, Yuan He†, Yuan Feng‡, Yunhao Liu†

†{kebin, yangzh, limo, heyuan, liu}@cse.ust.hk

‡{guozhw, guoying, hongfeng, yangxh, fengyuan}@ouc.edu.cn

†Hong Kong University of Science and Technology ‡Ocean University of China

In this project, we explore the possibility of deploying networked sensors on the Ocean’s surface, to monitor depth and temperature, as well as other valuable environmental parameters. Sea depth monitoring is a critical task to ensure the safe operation of harbors. Traditional schemes largely rely on labor-intensive work and expensive hardware. We present a new solution for measuring the sea depth with Restricted Floating Sensors. To address the problem of node localization on the changeable sea environment, we propose Perpendicular Intersection (PI), a novel mobile-assisted localization scheme. In the OceanSense project, we propose the concept of passive diagnosis as well as the PAD approach which is both lightweight and adaptive to network dynamics. The OceanSense system has been working for over 16 months and provides large amounts of valuable data about the sea.

# I. Motivation

Wireless sensor networks (WSNs) have great potential in various applications such as environment surveillance, scientific observation, monitoring battle fields, and the like. WSNs are urged especially for tasks under changeable or even hostile environments, for example, sea monitoring.

Our OceanSense [2] project was originally motivated by our field study in H. H. Harbor, which is currently the second largest harbor for coal transportation in China. It has developed rapidly in its capability over the past 5 years, however it currently suffers from a severe silt deposition problem along its shipping channel. The H. H. Harbor has a shipping channel 19 nautical miles long and 800m wide at the entrance. The shipping channel includes an inner channel and an outer channel and its depth is around 13.5m. While in operation, the shipping channel has always been threatened by silt movement from the shallow sea area outside the entrance. In the event that the shipping channel becomes silted up, ships would have to wait outside the harbor to prevent being grounded. Figure 1 lists some snapshots we have taken from the H. H. Harbor and the central picture illustrates the waiting ships outside the harbor. In practice, silt dredging can be conducted efficiently using multiple dredgers, however localizing the regions that are silted up in real time is a great challenge. In order to address the siltation problem, currently the harbor administration hires three boats equipped with active sonars to monitor the shallow area around the harbor. It costs more than 18 million US dollars per year to monitor the sea depth.

![](images/f96d4ab909914fbd1b3c9396d4c1913541bf4467aed168ce63990b0c0958abef.jpg)



Figure 1. The H. H. Harbor and waiting ship

We make a pioneering attempt at exploring the possibility of deploying networked sensors on the sea surface for depth measurement which can save more than 95% of the cost of such an operation. Aside from sea depth, our OceanSense project also takes into account other useful environmental parameters such as temperature, luminance, and so on. It is extremely difficult and expensive to chronically obtain these sea surface data manually. Leveraging a wireless sensor network, we can achieve continuous surveillance on the designated area.

The rest of the paper is organized as follows. Section II briefly introduces our OceanSense project, including the hardware encapsulation, protocol design, deployment experiences, and the like. Section III presents our sea depth measurement solution with the floating sensors. Section IV discusses how to accurately localize the sensor nodes on the sea surface. The network management and fault diagnosis issues are presented in Section V.

![](images/750b1e0344a4de362b2b5242df57381b0ef42a8a6d7676412bf56186139fab50.jpg)



![](images/91d051e68841b6a132fcaf94e2a4403e7934ab41b4c3d40d68335914587f16be.jpg)



Figure 2. The campus experiment

# II. OceanSense Project

OceanSense aims to build an integrated sensor network system that can continuously acquire and analyze information about marine environmental factors such as depth, temperature, luminance, and so on. Most current methods are labour-intensive and the data collection lacks both the density and consistency of samplings. By deploying a wireless sensor network, we are able to achieve continuous surveillance.

Different to traditional land-based sensor networks, most of which apply stationary sensor nodes, the sensor network deployed on the sea consists of Restricted Floating Sensors (RFS), anchored to the sea bottom, and floating within a restricted area on the surface. The complex consequences of wind, tides and currents affect the system’s architecture, algorithm design and manufacture of the sensor nodes.

In the first stage, we launch a prototype system off shore of the HKUST campus. We fit each node with a lightweight support shelf, which floats on the sea surface and raises the sensor nodes 150cm high above the sea’s surface. Figure 2 shows the shelf and our experiment area in campus.

In the second stage, we deploy the working system in Tsingtao, China. We use TelosB motes and TinyOS as our development basis. The current system consists of 25 sensor nodes deployed in the field, reporting sensing data continuously to a base station. The complete system is designed to scale to hundreds of sensors.

In order to deal with the changeable conditions at sea, we improve our encapsulations. As shown in Fig.3 (a) and (b), we encase the sensor node in a sealed bottle and raise it further on a long metal pillar. Three plastic foam floats are leveraged to keep the equipment floating on the sea surface. Taking into consideration the most severe conditions possible out at sea, we extend the original sensor radio with an external antenna which significantly improves communication quality. Figure 3 (c) features a snapshot of our node manufacture and Fig.3 (d) shows the anchor for fixing the floating sensor in a restricted area. The encapsulated sensors are shown in Fig.3 (e).

![](images/a11a911f3dfdba3984998a7abb2c522b47f48170471ba49f123deae44fd8d29d.jpg)



![](images/7d5a2bb10427068f3143f62f941ea11eb50a2b1a3120304f5bca09837114a9fe.jpg)



![](images/2dc2278047cf114fcc00b667c17323e88dba49091b4cc7b87564d2a3b680e5cd.jpg)



Figure 3. Encapsulation of sensor nodes

This system has been working for over 16 months and provides large amounts of data which is now available on our data center website [1].

# III. Sea Depth Measurement

In this section, we briefly describe our sea depth measurement approach with the OceanSense system. Different from ground deployments, sensor nodes, in this scenario, will generally not be stationary in their original deployed places, but floating due to many different factors, such as current, wind, and tide and so on. Therefore, we anchor the sensor nodes to the sea bottom by ropes to restrict their movement. We call them Restricted Floating Sensors (RFS) [5]. Figure 4 illustrates an RFS network deployed in an ocean area. As demonstrated, different depths result in different sized floating areas.

The key issue in this design is determining the floating area of each sensor. Traditional localization approaches for stationary sensors do not consider sensor mobility. On the other hand, simply treating the RFS network as a mobile sensor network and blindly applying localization approaches for mobile WSNs does not capture the special nature of the RFS network. By understanding RFS mobility behavior, we can carry out localization at high accuracy and reduced overhead.

By measuring multiple samples of distances between a pair of neighboring sensors, the total drift area the sensor covers can be figured out through linear regression. Accordingly, the sea depth can be inferred as follows. When we use a rope of length L to anchor the sensor node to a sea bed of depth h (L > h), the sensor node floats within the disk area of radius $r = \sqrt { L ^ { 2 } - h ^ { 2 } }$ , as shown in Figure 4. After localization, we obtain the drift area of a node, achieving its center c as well as its radius r. We can then easily calculate the sea depth at position c. This calculation involves neither extra measurement nor hardware costs. In some cases, the movement of the ropes cannot be ignored. When sensor nodes are on the boundaries of their drift areas, ropes become slack and form a curve with a tight upper part and slack lower part. In this situation, the depth can be computed according to the equation of catenary.

![](images/b678f4c3fe8318d0e9878963fd489d76881c0b24f0c7e728945318ccf93a1f3c.jpg)



Figure 4. Sea depth monitoring with Restricted Floating Sensors

# IV. Sensor Nodes Localization

Data without location is meaningless. As sensor nodes are deployed in the wild, a routine localization method such as GPS is not feasible for the cheap and resource constrained sensor nodes, therefore much research effort has been devoted to this topic. Most of these approaches are range-based and their ranging processes rely on mapping metrics like RSSI to physical distances according to some attenuation models. These approaches work well in traditional land-based sensor networks but the signal attenuation process suffers from environmental interference in the ocean. To address these issues, we propose a novel mobile-assisted localization scheme called Perpendicular Intersection (PI) [3]. Instead of directly mapping RSSI values into physical distances, PI uses the geometric relationship of a perpendicular intersection to compute node positions.

![](images/475b97c1148180180eb34c8358c2e71528935d10f63562bc5bdb587a4ff7a4ce.jpg)



Figure 5. An example of PI

Figure 5 shows a sample process of PI. A mobile beacon traverses the region while periodically broadcasting beacons. It starts at point $( x _ { I } , \ y _ { I } )$ , changes direction at point $( x _ { 2 } , y _ { 2 } )$ , and stops at point $( x _ { 3 } , y _ { 3 } )$ . The trajectories of the mobile beacon form a virtual triangle. Assume that we want to localize the sensor node at position (x, y), in which x and y are unknown. The sensor node receives and records the RSSI values of the beacon packets as the mobile beacon moves. As shown in Fig.5, when the mobile beacon is at position $( x ^ { \prime } , \ y ^ { \prime } )$ and $( \mathbf { x } ^ { \prime \prime } , \ \mathbf { y } ^ { \prime \prime } )$ , the recorded RSSI values achieve the local maximum, that is, node $( x , y )$ has the local minimum distances to the mobile sink from these two positions. As the virtual rectangle as well as the coordinates of positions $( x ^ { \prime } , y ^ { \prime } )$ and $( x ^ { \prime \prime } , y ^ { \prime \prime } )$ are known, the (x, y) can be calculated through the geometric relationships.

![](images/5b317e45cab13451a4dc6c2d5212dd80f94219e8be30966b59270445c3e7cad0.jpg)



Figure 6. Framework of PAD approach

# V. Passive Diagnosis for Sensor Networks

During our deployment, we experienced many challenges such as the rapid energy depletion of the sensor nodes, high delivery delay and packet loss. To address these issues, efficient network diagnosis tools are required. Existing works for diagnosing WSNs mainly rely on proactive approaches, which incur high traffic overhead to the resource constrained WSNs. These methods are sensitive to the loss of status information as well.

To address these issues, we propose the concept of passive diagnosis. We report in this research our initial attempt at providing a light-weight network diagnosis mechanism for sensor networks. We present PAD [4], a probabilistic diagnosis approach for inferring the root causes of abnormal phenomena. Figure 6 shows the framework of the PAD design which comprises four components: a packet marking module, a mark parsing module, a probabilistic inference model, and an inference engine. PAD implants a tiny light-weight probe into each sensor node that sporadically marks routine application packets passing by, so that the sink can reassemble the big picture of the network conditions. Our approach does not incur additional traffic overhead for collecting desired information. Instead, we introduce a probabilistic inference model which encodes internal dependencies among different network elements. Such a model is capable of additively reasoning root causes based on passively observed symptoms. We implement the PAD design in our OceanSense project and validate its effectiveness.

# Reference

[1] "OceanSense data center," http://osn.ouc.edu.cn/SensorData/query.jsp   
[2] "OceanSense: Sensor Network for Sea Monitoring," http://www.cse.ust.hk/\~liu/Ocean/index.html   
[3] Z. Guo, Y. Guo, F. Hong, X. Yang, Y. He, and Y. Liu, "Perpendicular Intersection: Locating Wireless Sensors with Mobile Beacon," In Proc. of IEEE RTSS, 2008.   
[4] K. Liu, M. Li, Y. Liu, M. Li, Z. Guo, and F. Hong, "Passive Diagnosis for Wireless Sensor Networks," In Proc. of ACM SenSys, 2008.   
[5] Z. Yang, M. Li, and Y. Liu, "Sea Depth Measurement with Restricted Floating Sensors," In Proc. of IEEE RTSS, 2007.