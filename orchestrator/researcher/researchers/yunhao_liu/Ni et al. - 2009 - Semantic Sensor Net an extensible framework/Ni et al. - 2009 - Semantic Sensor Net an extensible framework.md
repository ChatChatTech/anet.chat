# Semantic Sensor Net: an extensible framework

# Lionel M. Ni

Department of Computer Science, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong Fax: +852-2358-1477 E-mail: ni@cs.ust.hk

# Yanmin Zhu\*

Department of Computer Science and Engineering Shanghai Jiao Tong University, Shanghai, PR China E-mail: zhuyanmin@gmail.com \*Corresponding author

# Jian Ma, Qiong Luo, Yunhao Liu, S.C. Cheung and Qiang Yang

Department of Computer Science, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong Fax: +852-2358-1477 E-mail: majian@cs.ust.hk E-mail: luo@cs.ust.hk E-mail: liu@cs.ust.hk E-mail: scc@cs.ust.hk E-mail: qyang@cs.ust.hk

# Minglu Li and Min-you Wu

Department of Computer Science and Engineering, Shanghai Jiao Tong University, Shanghai, P.R. China E-mail: li-ml@cs.sjtu.edu.cn E-mail: wu-my@cs.sjtu.edu.cn

Abstract: Existing approaches for sensor networks suffer from a number of serious drawbacks, including assumption of homogeneous sensor nodes, application-dependency, engineering-orientation, and lack of interoperability. To overcome these drawbacks, we propose an extensive framework: Semantic Sensor Net (SSN). It is a framework catering for heterogeneous sensor networks, which enables dynamic tagging of semantic information to sensory data to allow more efficient and systematic monitoring and handling of environmental dynamics to provide diverse services. Semantics refers to the important meaning of sensory data, sensor nodes and application requirements. Essential semantics enables integration, exchange, and reuse of sensory data across various applications.

Keywords: sensor networks; semantic; data processing; framework; architecture.

Reference to this paper should be made as follows: Ni, L.M., Zhu, Y., Ma, J., Luo, Q., Liu, Y., Cheung, S.C., Yang, Q., Li, M. and Wu, M-y. (2009) ‘Semantic Sensor Net: an extensible framework’, Int. J. Ad Hoc and Ubiquitous Computing, Vol. 4, Nos. 3/4, pp.157–167.

Biographical notes: Lionel M. Ni received his PhD Degree in Electrical and Computer Engineering from Purdue University, West Lafayette, Indiana, in 1980. He is a Professor and the Head of the Computer Science Department of the Hong Kong University of Science and Technology. He was a Professor of Computer Science and Engineering at Michigan State University from 1981 to 2003, where he received the Distinguished Faculty Award in 1994. His research interests include parallel architectures, distributed systems, high-speed networks, and pervasive computing. A fellow of the IEEE and the IEEE Computer Society, he has chaired many professional conferences and has received a number of awards for authoring outstanding papers.

Yanmin Zhu is a PhD candidate in the Department of Computer Science, Hong Kong University of Science and Technology. He received his BS Degree in Computer Science from Xi’an Jiaotong University, Xi’an, China, in 2002. His research interests are grid computing, peer-to-peer networking, pervasive computing and sensor networks. He is a member of the IEEE and the IEEE Computer Society.

Jian Ma is a PhD student in the Department of Computer Science, Hong Kong University of Science and Technology. He received his BS Degree in Computer Science from Beijing University, Beijing, China, in 2002. His research interests are in networking, in particular, ad hoc networks, sensor networks, and power-aware communication.

Qiong Luo is an Assistant Professor in the Computer Science Department, Hong Kong University of Science and Technology. She received her PhD in Computer Sciences from the University of Wisconsin-Madison in 2002. Her research interests are database systems, with focus on data management and analysis techniques related to network applications.

Yunhao Liu is an Assistant Professor in the Computer Science Department, Hong Kong University of Science and Technology. He received his BS Degree in Automation from the Tsinghua University, and a MA Degree in Beijing Foreign Studies University, China. He received an MS and a PhD Degree in Computer Science and Engineering from Michigan State University, USA, in 2003. His research interests include peer-to-peer and grid computing; pervasive computing; distributed systems; network security; internet and e-commerce technologies.

S.C. Cheung is an Associate Professor in the Computer Science Department, Hong Kong University of Science and Technology. His research interests include software engineering issues related to services computing, object design patterns, testing, pervasive computing, wireless sensor networks, RFID systems, embedded systems, and digital rights management.

Qiang Yang is a Professor in the Computer Science Department, Hong Kong University of Science and Technology. He received his PhD Degree from the Department of Computer Science, University of Maryland, 1989. His research interests are data mining and machine learning with applications to web and wireless problems, artificial intelligence: planning, machine learning and case based reasoning.

Minglu Li is a Professor in the Department of Computer Science, Shanghai Jiaotong University. He is also the Director of the Grid Computing Centre. His research interests are grid computing, web services, etc.

Min-you Wu is a Professor in the Department of Computer Science, Shanghai Jiaotong University. He received his MS Degree from the Graduate School of Academia Sinica, Beijing, China, and his PhD Degree from Santa Clara University, California. His research interests include multimedia systems, multimedia networking, parallel and distributed systems, compilers for parallel computers, programming tools, and VLSI design. He has published over 90 journal and conference papers in the above areas and edited two special issues on parallel operating systems. He is a member of ACM and a senior member of IEEE.

# 1 Introduction

Recent advances in wireless communications and MicroElectroMechanical Systems (MEMS) have led to the wide deployment of large-scale Wireless Sensor Networks (WSN), which promises to revolutionise the way we monitor and control environments of interest (Akyildiz et al., 2002; Pottie and Kaiser, 2000). MIT Technology Review identified WSN as one of the ten emerging technologies that will change the world. A wide variety of attractive applications (Estrin et al., 2001) will come into reality, such as habitat monitoring (Mainwaring et al., 2002), search and rescue, disaster relief, target tracking, precision agriculture and smart environments.

A sensor node is a low-cost and typically battery-powered device that integrates micro-sensing, onboard processing and wireless communication. A WSN is a self-organising network composed of a large number of sensor nodes, tightly interacting with the physical world. Such a self-organising network is able to not only disseminate sensory data across the network, but also provide in-networking real-time processing capability. WSN is a promising technology that effectively bridges the physical world and the digital world, by which we can extract critical information from physical environments, and therefore better monitor and control dynamics of environments.

Distinct from traditional computer networks, each sensor node in a sensor network plays a minor role. We are, however, more interested in sensory data. The data-centric nature of sensor networks provides an innovative approach to solve a greater class of applications. However, current work in WSNs suffers some major drawbacks:

most solutions are based on homogeneous sensor array   
each solution is usually for a specific application   
the solution is usually an engineering approach without a common framework   
there is no standard to allow communication among different sensors at different levels.

This paper proposes a new concept called Semantic Sensor Net (SSN) to alleviate the above drawbacks. A SSN is a heterogeneous sensor network which enables dynamic tagging of semantic information to sensory data to allow more efficient and systematic monitoring and handling of the environmental dynamics to provide demanded services. SSN has the following advantages

the tagging of semantic information to sensory data allows efficient handling of large-scale distributed heterogeneous sensory data   
SSN can provide a sound theoretical foundation to research in WSNs at different levels   
SSN can help develop a semantic-based framework to systematically support various applications.

The rest of the paper is organised as follows. Section 2 discusses the characteristics and challenges of WSNs. We review the existing approaches and discuss their limitations in Section 3. In Section 4, we give an overview of SSN. Some of our preliminary results are presented in Section 5. Finally, Section 6 concludes the paper and introduces the directions of future work.

# 2 Characteristics and research challenges of WSNs

Compared with traditional computer networks and Mobile Ad-hoc Networks (MANET) sharing more similarities, sensor networks present many unique characteristics. Every sensor node is highly resource-constrained, with limited computational capability and small storage. The wireless communication is unreliable. Each sensor node is typically powered by battery and usually not rechargeable. Sensor nodes may be deployed in unattended environments, exposed to unpredictable damages from environments, and hence any sensor node is prone to failure.

Unlike computers in traditional computer networks, most sensor nodes have no global ID due to low-cost mass production. In addition, global IDs introduce too much overhead which is not affordable by resource-constrained sensor nodes. Because of the lack of global IDs, traditional networking methodologies are not appropriate for WSNs. Since any sensor node may become unavailable at any time and wireless communications are unreliable, the network topology may change constantly over time. Thus, the capability of self-organising and self-configuring is fundamentally important. In many applications, senor nodes are usually deployed without per-node placements (e.g., dropping sensor nodes from a flying airplane). Given the dynamic nature of sensor nodes, it is essential that these sensor nodes be able to cooperate with each other, form a network automatically, and work as a whole without human intervention.

With the rapid development of WSNs and its growing commercialisation, it is probable that in an environment of interest different types of sensor nodes are deployed. Therefore, a sensor network could be very heterogeneous. Heterogeneity exists in both individual sensor nodes and sensor networks as a whole. So far there have been few standards available for WSNs. Different manufacturers produce distinct sensor network systems, adopting different hardware and software components. For example, Berkeley MOTE (Chen et al., 2002) has been available in the educational market. The Institute of Computing Technology of Chinese Academy of Sciences (CAS/ICT) (Gao et al., 2005) also releases their sensor products. Even if we do not consider the heterogeneity caused by different manufacturers, sensor nodes from the same manufacture can still be very heterogeneous in terms of function, capability, and so on. Sensors with different functions have been available, such as temperature, pressure, light, motion, and their combinations. Sensor networks, as a whole, can also be heterogeneous, since different sensor networks may employ different network-organising strategies, routing algorithms, and aggregation methods. How to integrate heterogeneous sensor nodes to develop various flexible and extensible applications has been a great challenge.

Performance goals of WSNs could be very application-specific. However, some of them are commonly desirable. For a sensor network, one of the greatest concerns is how long it can work effectively, i.e., the network lifetime. Each sensor node is powered by a battery and, hence, short-lived. It has been a great research challenge to prolong network lifetime. Many approaches have been proposed to minimise power consumption, e.g., MAC mechanisms, topology control methods and resource aware routing. Other performance goals include maximum sensing coverage, shorter message delay, data reliability, and lower deployment cost.

# 3 Existing approaches and their limitations

In the past several years, sensor networks have received considerable research efforts, covering different aspects of design. In this section, we give an overview of the existing approaches and study their limitations.

Because of resource constraint, the popular layered architectures used in traditional system design are not appropriate for sensor networks. Although a layered architecture can provide better organisation and is more extensible, it introduces too much overhead, since a packet may be added multiple headers of protocols, dominating the size of a packet. Existing research on sensor networks can still be roughly classified into several categories according to their functions.

Hardware and Wireless Communication include sensor architecture, radio module design (Rakhmatov and Vrudhula, 2003), MAC (Sohrabi et al., 2000; Shih et al., 2001; Ye et al., 2002) and power control (Kubisch et al., 2003).   
Infrastructure Establishment includes deployment (Meguerdichian et al., 2001), localisation (Doherty et al., 2001), time synchronisation (Elson and Estrin, 2001), ID assignment and calibration (Krishnamachari and Iyengar, 2004), and middleware (Xu et al., 2004a).   
Network Organisation includes topology control (Cerpa and Estrin, 2002; Chen et al., 2002; Salhieh et al., 2001), density control and cluster management.   
Data Dissemination includes routing (Shurgers and Srivastava, 2001; Intanagonwiwat et al., 2000), aggregation (Madden et al., 2002), compression, diffusion and query processing (Madden et al., 2003).   
Applications such as habitat monitoring (Mainwaring et al., 2004), target tracking, battlefield surveillance, pollution monitoring (Ngan et al., 2005), industry control, and so on.

Although extensive research has been conducted and some real applications have been in place, existing approaches suffer from several critical drawbacks which have significantly restricted the wide deployment of sensor networks in practical applications.

Homogeneous sensors have usually been assumed. In a small-scale sensor network, it may be reasonable to have homogeneous sensors which are usually identical or similar in terms of function, node architecture and software. With the homogeneous assumption, solutions can be greatly simplified. However, on the one hand, with the rapid development, sensor networks could be very large-scale and many different sensor nets could be deployed into the same area; on the other hand, with the increasing demand of applications accessing to various sensory data, an application environment could be deployed with highly heterogeneous sensor nodes. Existing solutions based on the homogeneous assumption can hardly work in such heterogeneous systems.

Existing solutions have been very applicationdependent. The applications of sensor networks are very diverse and could have very different requirements and objectives. For example, the battle field surveillance application requires sensor nodes report to the gateway only when some events are detected. In contrast, for a building temperature monitoring application, sensor nodes report to the gateway regularly. Given two such distinct application scenarios, the respective designs have been very different. Such application-specific solutions are not

extensible and cannot be reused. Most existing applications of sensor networks adopted tailor-made designs.

Existing solutions are engineering-oriented. In contrast to traditional computer networks, so far there have been few standards, like TCP/IP, available for WSNs. Due to the lack of widely-accepted standards, we have to re-design most building blocks when developing a new sensor network, such as topology control, routing algorithm, compression and query processing. Such engineering-oriented approaches are particularly inflexible, and pose developers a big burden of reengineering. In order to avoid unnecessary reengineering, it is essentially important to develop core standards for sensor networks.

Besides the above, existing solutions are not extensible in the sense that once a sensor network for a specific application has been deployed, it is extremely hard to accommodate application dynamics and new application additions over the same sensor network. There are two reasons for this. First, the current hardware limitation does not allow frequent updates of software burned in sensor nodes, as it leads to unreliability and high power overhead. Second, there is no effective mechanism to support such application dynamics and new application additions which, in practice, are very desirable to make applications better meet real needs.

Having suffered much from these major drawbacks, we come to realise that a solid foundation and framework for WSNs is very necessary, through which we can overcome these drawbacks, and hence promote the further development of sensor networks.

# 4 Semantic Sensor Net: an overview

To alleviate the drawbacks experienced by existing approaches, we propose an extensible systematic framework: SSN. In brief, a SSN is a heterogeneous sensor network which enables dynamic tagging of semantic information to sensory data to allow more efficient and systematic monitoring and handling of the environmental dynamics to provide demanded services. The important concept semantics is introduced to address various challenges, which exists in different levels of designs of sensor networks, effectively enabling the integration, exchange, and reuse of sensory data across various applications and multiple sensor nets.

As mentioned in the previous section, any single sensor node is of negligible importance and, instead, sensory data are what we are concerned with the most. It suggests the data-centric principle, which is fundamentally different from the node-centric principle for traditional computer networks. The data-centric principle should be incorporated throughout designs of sensor networks. However, it is very challenging. Sensory data have unique characteristics and can be utilised in very different ways. High level applications usually require the integration of various sensory data. We believe the semantics-based framework can well address these challenges, and provide a solid foundation for WSN. Although sensory data can be very diverse, semantics inherently associated with sensory data can enable the integration and exchange of various sensory data, and accommodate different requirements of high-level applications.

The concept of semantics has been successfully introduced in the semantic web, which is an extension of the current web in which information is given well-defined meaning, better enabling computers and people to work in cooperation (Berners-Lee et al., 2001). Traditionally, web pages are composed mainly for human comprehension. Being intelligent, human beings have the ability to understand web information. However, it is difficult for digital computers to understand the meaning behind web pages. The semantic web brings structure to the meaningful content of web pages, so called semantics, enabling computers to carry out sophisticated tasks for users.

In SSN, semantics presents more flexible usage, which not only allows sensory data to be shared and integrated across various applications, but also provides a powerful framework for designs of sensor networks. Basically, semantics refers to the critical meaning of sensory data, senor nodes and application requirements, which we believe can help better decision making in various designs of sensor networks. Within SSN, semantics can exist in different levels from bottom to top, as shown in Figure 1. Semantics in sensory data is the most basic, effectively supporting the realisation of semantics in upper levels. Semantics in various applications is the most complex and can be factorised into much simpler forms. Semantics can be converted and form new semantics, and support efficient operations in different levels.

Figure 1 Semantics exists in different levels of sensor networks (see online version for colours)   
![](images/e10c24ecae9cafe2da38036ebb1d3de77586bc5f3d656b8f1a50a3a02e0a5219.jpg)



To demonstrate how semantics helps, let us take an example. Suppose, in a building, a large number of heterogeneous sensor nodes are deployed for monitoring the environment inside the building. Examples of sensors include temperature, light and humidity. Now we may be concerned with whether there is a fire emergency inside the building. The ‘fire emergency’ certainly encompasses much semantics that can only be understood by humans, and it resides on the service level. A fire can be roughly interpreted as a combination of strong light detections and high temperature detections in the same area. So the fire emergency is converted to a query with more specific semantics,

“a strong light detection (>= 10 candlepower) plus a high temperature detection (>= 80°C) in the same region (distance <= 1 m) within 10 s.”

The query is then sent across the sensor network. On receiving the query, a sensor node will be able to interpret and then set up new routing rules. The basic semantics of the new routing rule, which resides on the data dissemination level, may act like the following. This query is prioritised to be forwarded to temperature and light neighbours such that other sensors can avoid being involved, which is a power-efficient design. And, if a neighbour within ten metres reports a strong light detection and the node itself detects a high temperature event, it will form a fire alarm event and report it to the gateway.

Besides semantics in the upper levels, semantics in the lower levels are also essential. A sensor node must maintain its own semantics, such as ID, location, sensing type, and sensing accuracy. When sensory data are available for transmission, the semantics should be enclosed, enabling other sensors to interpret it; otherwise, other sensors may have no idea what the received data are. The semantic is on the bottom sensory data level. Given the high heterogeneous sensors in the environment, an integrated network is expected to be set up, including all possible sensors. Since different sensors may adopt different wireless technologies, direct communication between some sensors may not be possible. In this case, some nodes should act as bridges for these sensors. Bridges are on the networking level, and may require new semantics to annotate for themselves.

The success of SSN requires that the following be well addressed.

Semantic sensory data modelling. Sensory data can be very diverse. To enable the integration and exchange of various sensory data, an expressive data model is very necessary.   
Semantic Sensor Network system architecture. In facilitating the development of sensor network systems, extensible system architecture plays a fundamental role.   
Semantic-based data dissemination. Data dissemination is at the core of sensor networks. Semantic-based data dissemination protocols are able to enable dissemination of various sensory data over heterogeneous sensor networks.   
Semantic query processing. With the unique abilities of built-in computation and data storage, sensor networks are very promising in data management. Queries are the effective way to acquire useful information from sensor networks. Due to sensory data distributed across the whole sensor network, as well as the heterogeneity

of sensory data, query processing is challenging. The semantics-based framework could help more efficient query processing.

Services. We need abstract and form services, based on which various applications can be built conveniently.

# 5 Some preliminary work of SSN

In this section, we present some of our preliminary work in SSN. More advanced and detailed work will be carried out in future work.

# 5.1 SSN architecture from data perspective

As is well-known, the success behind the internet should be attributed to the hourglass architecture. The main idea is everything is over IP and IP is over all underlying things. With in-depth understanding of this, we propose an hourglass-based architecture for SSN. The architecture is depicted in Figure 2. The core is the Semantic Sensory Data (SSD), as is also on the data-centric principle of sensor networks. Various applications are over SSD, and SSD is over heterogeneous sensor networks. This architecture is very advantageous in the sense that it is able to achieve interconnecting heterogeneous sensors and provide upper applications with uniform interfaces to interpret sensory data.

Figure 2 Hourglass-based architecture from data perspective   
![](images/8fa7a5c5be61558a8c9546f7a905bc59180dae9e7cf681d9a427bc5aef835f34.jpg)



We consider the architecture only from the data perspective. It should be clarified that this architecture is for presenting our idea only and is still very conceptual. It does not address how sensors are connected from the networking perspective. There are certainly more detailed architectures from other perspectives.

# 5.2 Semantic sensory data modelling

With the growing number of ubiquitous sensor networks, a very large amount of sensory data will become available. Sensory data have very unique characteristics, which greatly add to the challenges in the integration and reuse of sensory data across various applications.

Sensory data can be highly heterogeneous. Various sensors may be deployed, differing in functions, capabilities, and sensing contexts. For example, some sensors are deployed for monitoring temperature, while some are for sensing humidity. Even if two sensors are both for sensing temperature, their sensory data can still be quite different. One may have better accuracy and a wider range of allowed temperatures over the other. In addition, data representation could be different as well. Thus, data generated by different sensors can be highly heterogeneous.

Sensory data are usually unreliable, error-prone, and inconsistent. In general, sensors are low-cost devices, vulnerable to unpredictable failure. Moreover, sensors may be deployed to an unattended environment, and can easily be affected by environmental damages.

Sensory data are widely distributed. For most applications, the deployed sensor networks can be very large-scale. Sensory data are widely distributed across the sensor networks.

Before the great potential of sensor networks is realised true, the issue of how to effectively aggregate, integrate and enable exchange of these sensory data with the above unique characteristics should be addressed. The heterogeneity of sensory data results from various semantics associated with sensory data. We plan to propose an expressive framework to model sensory data. The basic idea is to dynamically tag sensory data with semantics so that sensory data can be well interpreted when being utilised.

# 5.2.1 Semantics of sensory data

Each sensor generates some kind of raw data. To make the raw data meaningful, we have to tag the data, i.e., we should attach the semantics to it. The semantics of sensory data is the necessary description about the data generation environment where the raw data was generated. The description should include:

Meta data. These are the necessary description about the raw data. Take raw data produced by a temperature sensor, for example. We have to make it clear that the raw data are a temperature measurement, how accuracy it is, and in what conditions it is valid. Meta data usually depend on the capability of sensing devices. Different sensing devices may have different kinds of meta data.   
Context information. These are about the contextual information in which the raw data were generated, which is usually related to the sensor node which the sensing device is attached to Xu et al. (2004a). Take the above, for example. In general, it should be made clear where the temperature measurement was made (i.e., location of sensor node), which node took the measurement if applicable (i.e., ID of sensor node), and when it was captured (i.e., timestamp).

Without these necessary descriptions, raw data itself are meaningless. Therefore, raw data should be attached with the respective semantics. Semantics are dynamic and can be changed. For example, the location of a mobile sensor is changing constantly. Then apparently, the semantics of the sensory data produced by the sensor are changing accordingly.

For sensory data, their semantics are managed by the respective sensor nodes. On the one hand, sensor nodes are responsible for forming sensory data and dynamically setting current semantics for raw data. On the other hand, sensor nodes themselves should be attached with the semantics, such as location and ID; otherwise they cannot be distinguished from each other. Therefore, it is natural and advantageous that sensor nodes manage the semantics of sensory data.

The inherent heterogeneity of sensory data poses great challenges for applications to aggregate and integrate various sensory data. Most existing application-specific approaches treat semantics of sensory data implicitly. They commonly assume that the application developers know well semantics of sensory data. It is feasible if sensory data are simple and have a few kinds only. However, it would be hardly feasible if there is a large amount of various sensory data. The situation would become even much tougher if some sensory data are beyond the control of the developers, e.g., part of sensory data are from sensor networks developed by others. Thus, it is desirable to propose a uniform framework to dynamically tag sensory data with semantics so that the sensory data can be well-interpreted. Based on the useful information provided by the semantics, proper actions could be performed on the sensory data.

# 5.2.2 Semantic modelling framework

A complete piece of sensory data consists of the raw data and the semantics. The problem is how to present the semantics. While we have made some preliminary study of the semantics of context information encountered in web services (Xu et al., 2004b), the semantics of sensory data is likely more complex. Different sensory data may have very different semantics, even for two identical sensors. However, we have the intuition that the sensory data produced by two identical sensors should have the same presentation pattern of semantics. We term the presentation pattern as schema. The same type of sensory data follow the same schema and different types of sensory data follow different schemas. As long as one has the right schemas, he is able to dynamically interpret the sensory data for various usages, despite how heterogeneous these sensory data are.

We plan to propose an expressive Sensory-data Semantic Modelling Framework (SSMF), as depicted in Figure 3. Sensor-data Semantic Description Language (SSDL) is the language for defining schemas. Such a framework is very expressive and extensible. Users can conveniently define customised schemas using SSDL. No centralised storage of schemas is needed. Given an application, only those schemas which the corresponding sensory data are using should be included.

The size of packets transmitted in sensor networks is usually very small. Such a design results from the consideration of unreliable communication conditions between sensors. In general, the longer a packet is, the higher is the probability that the packet encounters a collision. Moreover, there is usually no retransmission mechanism to guarantee the reliability of data transfer. To allow automatic interpretation of sensory data, on the one hand, we have to make the corresponding schema available; on the other hand, we should have the semantic values. However, it is certainly not a wise design to enclose the complete semantics data in every packet. To achieve flexible interpretation of sensory data while introducing less communication overhead, much research effort should be made. Actually, some of semantics data are relatively static, e.g., ID and location information. It is not necessary to transmit these static data again and again if the destination of the packets remains the same. Only dynamic semantic data, such as timestamp, needs to be enclosed in each packet. In addition, a schema rarely changes, and therefore it needs to be sent once, or it can be retrieved from a centralised server when needed. In short, semantics may cause additional communication overhead, but many techniques, such as caching, can help reduce much of these overhead.

Figure 3 Sensory-data Semantic Modelling Framework (SSMF)   
![](images/41dbad95b950aa4f876bee0ab7bdbac9e487979e2295d14ae7a1a55016d3d5d6.jpg)



# 5.3 Semantic-based data dissemination

Data dissemination plays a major role in enabling commands to be propagated from gateway nodes to sensor nodes and collecting sensed data of interest from sensor nodes back to the gateway nodes for further study. It is very challenging, however, to design effective data dissemination protocols for sensor networks. It would become even more difficult if we consider the heterogeneity in both sensors and sensor networks as a whole. Heterogeneous sensors in a sensor network produce heterogeneous sensory data. Based on the sensory data, different actions may be required. For example, some sensory data may be required to be routed back to the gateway as soon as possible, while some other sensory data should be sent to another sensor node for data aggregation. Such semantic-based routing requirements make the design of data dissemination protocols greatly complicated. In addition, heterogeneous sensor networks may deploy different network operators and network organisation.

Some applications may require cooperation among these networks. Such inter-network heterogeneity makes the design of data dissemination protocols even more challenging.

Data dissemination protocols need to be able to deal with heterogeneity of sensor networks. They should work robustly and be able to deal with unpredictable changes in sensor networks. The most important performance goal of data dissemination protocols is to minimise the power consumption and, hence, postpone the lifetime of sensor networks.

Although data dissemination protocols are largely application-dependent, it is unwise to support a different communication protocol for each application. Efficient routing is fundamentally important in order to realise efficient data dissemination. With the availability of semantics information in sensory data, we plan to propose a set of semantics-based routing algorithms. The objectives are as follows. First, the semantics-based routing algorithms can hide the heterogeneity based on the semantics in sensory data and sensor nodes. Second, the set of routing algorithms can provide various applications with an extensible routing framework, by which specific application requirements can be incorporated into data routing.

The design of routing algorithms relies on the availability of semantics in both sensory data and sensor nodes, such as global ID, physical location, and power measurement. The availability of semantics makes it possible to develop efficient routing algorithms. Some of them are described in the following.

IP-like routing. If every sensor node is assigned a globally unique ID, it is possible to employ IP-like routing algorithms in sensor networks. Many mature techniques can be utilised. However, studies have shown that it is too costly for tiny sensors to have a globally unique ID. In additional, the data centric principle imply that any individual sensor node is no longer important compared to a traditional computer in the internet. Therefore, routing algorithms based on locally unique IDs have become highly desirable.   
Geographic routing. If sensor nodes have the knowledge of their physical locations, geographic routing is very attractive, which makes for routing decisions based on geographical information. With geographic routing, a destination is identified as an area instead of a single ID or address. Additionally, routing paths are established dynamically, based on the location information of sensor nodes along the path to the destination.   
Energy-aware routing. To prolong the lifetime of sensor networks as much as possible, it is of great importance for sensor nodes to be aware of its remaining energy when routing data. We hold the intuition that a sensor node with limited energy should forward fewer packets from other sensors. Without energy-awareness, some critical sensor nodes may

die fast, which lead to possible partitions of the sensor network and the consequent failure of the network.

Interest-centric routing. The data-centric principle of sensor networks suggests the tight coupling of application interests and sensory data. The publish/subscribe paradigm (Eugster et al., 2003) is very suitable for sensor networks. With this paradigm, different sensor nodes can publish different types of sensory data, and interested nodes can subscribe to specific events of sensory data. For example, a node could subscribe to events like ‘report me all events that the temperature exceeds 50°. The frequently referred work ‘Directed Diffusion’ (Intanagonwiwat et al., 2000) is one successful example of the publish/subscribe paradigm.

In the above, we discussed some advantageous routing mechanisms based on a specific semantics of sensor nodes. For more complex situations where a sensor network consists of heterogeneous sensor nodes, routing is greatly complicated because semantics of sensor nodes can be very different. For example, some sensors may have location information but have no global ID, while some other sensors may have global IDs but have no location information. In this case, neither IP-like routing nor geographic routing can simply applied. To conquer this challenge, we need to propose semantics-aware routing. It is not a specific routing algorithm. Instead, it is a framework, which aims to enable efficient data dissemination over large-scale heterogeneous sensor networks. Despite the heterogeneity, it is certainly desirable that all of the sensor nodes work as a whole network, instead of several separate networks working independently. Working as a whole can provide longer network lifetime, more efficient data dissemination, more complete sensory data and a more flexible application environment.

Built over various existing routing algorithms, semantics-based routing should be extensible, in the sense that it can address new emerging semantics possibly added to the sensor networks. It should take the advantage of available semantics in both sensory data and sensor nodes. Some possible scenarios are summarised as follows.

Semantics in sensor node. After receiving a packet from its neighbours, the sensor node should take proper actions based on its capability (one kind of semantics). Suppose the destination of the packet is defined by a geographic region, and the node has no knowledge of this physical location. In this case, the sensor node should forward the packet to one of its neighbours which knows its physical location, or simply drop the packet.   
Semantics in sensory data. To save energy, data aggregation is a popular technique associated with routing in sensor networks. Rather than routing back every piece of sensory data, some sensory data are aggregated at some nodes, and the resulting data are then routed back to the gateway. For example, a sensor

network consists of two types of sensors, temperature and light. After receiving a packet, a sensor node is able to interpret the sensory data enclosed in the packet. Suppose the sensor node is a temperature sensor. If the sensory data received happen to be a temperature measurement about the same region, it can firstly take the average of this measurement and its own measurement, and then forward the resulting data onwards. By this simple means, a packet transmission is saved.

Semantics in query. In general, queries are about some specific kind of sensory data. If a sensor node is able to interpret semantics in queries, irrelevant sensor nodes can avoid being involved so that more power can be saved. For example, if a query is issued to ask about temperature information, it is desirable that light sensors are not involved. After receiving a query, a sensor node can selectively forward the query to those neighbours which are also temperature sensors. By this means, light sensors will less be involved, and therefore such a query is more power-efficient.

From these scenarios, we see three types of semantics: semantics of sensors and sensor nets, semantics of sensory data, and semantics of queries. Thus, we propose to have three description languages:

Semantic Sensor Net Description Language (SSNDL) to define the semantics description format of sensors and sensor nets   
Sensor-data Semantic Description Language (SSDL) mentioned before   
Semantic Sensor Net Query Language (SSNQL).

When processing the original sensory data, the aggregated semantics of sensory data will be generated. The aggregated semantics will enable efficient querying by matching the query semantics and sensory data semantics. Different from the original semantics of sensory data which depend on physical setting only and is application-independent, the aggregated semantics depend on queries, and consequently, on applications.

# 5.4 Semantic query processing

The advent of WSNs provides a unique distributed platform to acquire and query streams of data. Traditional computational models transmit and process the data at each time instant and each individual record at a time. These models can no longer hold true for sensor networks, where the sensor nodes have limited and varying amount of power, the communication bandwidth is limited to local neighbours, and the information acquired from sensor nodes can be stochastic in nature. Furthermore, each sensor node only provides a small piece of the picture. To obtain an overall picture of the area and objects covered by the sensors and to understand the patterns that are of a temporal-spatial nature, we must be prepared to answer queries about high-level patterns in place, instead of answering queries that concern low-level information that concerns only limited space and time (Deshpande et al., 2004). In other words, we must be able to provide semantic-level answers to pattern-related queries.

Semantic queries distinguish themselves from the traditional queries with two major characteristics:

queries can involve aggregated environmental conditions, are location-context dependent and related to the tracking and monitoring of moving objects   
queries are answered by taking into consideration of the device semantics on sensor-distribution topology, state and capabilities and answers can depend on power, sensors, and levels of confidence.

Equipped with a variety of sensors, a WSN could make semantic inference about its environment, with queries on such conditions as the overall temperature, humidity, vibration, sound and lighting. All these queries can be answered depending on location context (Deshpande et al., 2004). For example, a query might ask about the temperature of a region. It takes a scheduling algorithm to determine which group of sensors should be responsible for answering the queries. This selected group may not consist of all sensors in that geographical region, because some sensors in that region provide inconsistent, noisy information. Others may be limited by power, communication bottleneck or be redundant. Therefore, the query planning system must be intelligent in order to provide timely and confident answers using a minimum amount of energy.

Sensor networks can be used to track one or more objects that move within the network. Take localisation of a moving object as an example, where the aim is to determine the physical position with uncertain sensors (Zhao et al., 2002; Intanagonwiwat et al., 2000; Byers and Nasser, 2000; Eugster et al., 2001; Li et al., 2002; Liu et al., 2003, 2004). However, algorithms in this field could not be directly applied to sensor networks. Sensor nodes may work in a large-scale distributed and dynamic environment. Therefore, it is difficult to build up a robust positioning model when compared to a robot, which always works in a fixed scenario in general. Furthermore, each sensor node may have only limited power and computation capability, which makes it necessary for the reasoning algorithm to probe them with different level of frequency and purpose. A related issue is localisation of a moving object. To sense the location of an object surrounded by a sensor network, many sensor nodes should work cooperatively. When a person is passing by, some nearby sensors may wake up while the rest are asleep for the sake of saving energy. For example, the alert sensors could detect different signal strengths from ultrasonic sensors and then locate and recognise the behaviour and objective of the person being tracked.

# 6 Conclusions and future work

For WSNs, any individual sensor node is, by itself, unimportant. Instead, sensory data collected from a group of sensors are what we are most concerned about. This suggests a data-centric principle in data processing, which is distinct from the node-centric principle in traditional computer networks. In response to the new challenges posed by the sensor networks, in this paper we have proposed an extensible framework known as Semantic Sensor Networks. By explicitly exploiting the semantic information, which uncovers the machine-understandable meaning embedded in low-level sensory data, sensor nodes and application requirements, SSN enables the integration, reuse, and exchange of sensory data across various applications. We believe that SSNs provide a sound foundation to develop in WSNs at different levels, as well as to facilitate various new applications.

In this paper, we have just begun to touch the tip of the iceberg in SSN research. Our future work aims to make SSN practical for real developments of sensor networks, especially for large-scale heterogeneous sensor networks. To this end, a wide range of topics should be extensively studied, including an extensible architecture to address the highly heterogeneous nature of WSNs used in practice, the practical semantics-based data dissemination protocols, the semantics-based query processing methods and service methodologies for developing sophisticated applications.

# References

Akyildiz, I.F., Su, W., Sankarasubramaniam, Y. and Cayirci, E. (2002) ‘Wireless sensor networks: a survey’, Computer Networks, Vol. 38, pp.393–422.   
Berners-Lee, T., Hendler, J. and Lassila, O. (2001) ‘The semantic web’, Scientific American, pp.34–43.   
Byers, J. and Nasser, G. (2000) ‘Utility-based decision making in wireless sensor networks’, IEEE MobiHo’00, Boston, MA, pp.143, 144.   
Cerpa, A. and Estrin, D. (2002) ‘ASCENT: adaptive self-configuring sensor networks topologies’, 21 Annual Joint Conference of the IEEE Computer and Communications Societies, pp.1278–1287.   
Chen, B., Jamieson, K., Balakrishnan, H. and Morris, R. (2002) ‘Span: an energy-efficient coordination algorithm for topology maintenance in ad hoc wireless networks’, ACM Wireless Networks Journal, Vol. 8, pp.481–494.   
Deshpande, A., Guestrin, C., Madden, S., Hellerstein, J.M. and Hong, W. (2004) ‘Model-driven data acquisition in sensor networks’, VLDB’04, Toronto, Canada, pp.588–599.   
Doherty, L., Pister, K.S.J. and Ghaoui, L.E. (2001) ‘Convex position estimation in wireless sensor networks’, IEEE INFOCOM, Anchorage, AK, pp.1655–1663.   
Elson, J. and Estrin, D. (2001) ‘Time synchronization for wireless sensor networks’, The 15th International Parallel and Distributed Processing Symposium, pp.1965–1970.

Estrin, D., Girod, G.P.L. and Srivastava, M. (2001) ‘Instrumenting the world with wireless sensor networks’, ICASSP, Salt Lake City, UT, pp.2033–2036.   
Eugster, P.T., Felber, P., Guerraoui, R. and Kermarrec, A-M. (2001) ‘The many faces of publish/subscribe’, EPFL Lausanne.   
Eugster, P.T., Felber, P., Guerraoui, R. and Kermarrec, A-M. (2003) ‘The many faces of publish/subscribe’, ACM Computing Surveys, Vol. 35, pp.114–131.   
Gao, W., Ni, L.M., Xu, Z., Cheung, S.C., Cui, L. and Luo, Q. (2005) ‘BLOSSOMS: building lightweight optimized sensor systems on a massive scale’, Journal of Computer Science and Technology, Vol. 20, pp.105–117.   
Intanagonwiwat, C., Govindan, R. and Estrin, D. (2000) ‘Directed diffusion: a scalable and robust communication paradigm for sensors networks’, The Sixth Annual ACM/IEEE International Conference on Mobile Computing and Networking, Boston, MA, pp.56–67.   
Krishnamachari, B. and Iyengar, S. (2004) ‘Distributed Bayesian algorithms for fault-tolerant event region detection in wireless sensor networks’, IEEE Transactions on Computers, Vol. 53, pp.241–250.   
Kubisch, M., Karl, H., Wolisz, A., Zhong, L.C. and Rabaey, J. (2003) ‘Distributed algorithms for transmission power control in wireless sensor networks’, Wireless Communications and Networking (WCNC), pp.558–563.   
Li, D., Wong, K.D., Hu, Y.H. and Sayeed, A.M. (2002) ‘Detection, classification and tracking of targets in distributed sensor networks’, IEEE Signal Processing Magazine, Vol. 19, pp.17–29.   
Liu, J., Chu, M., Liu, J., Reich, J. and Zhao, F. (2004) ‘Distributed state representation for tracking problems in sensor networks’, ACM/IEEE IPSN, pp.234–242.   
Liu, J., Reich, J. and Zhao, F. (2003) ‘Collaborative in-network processing for target tracking’, Journal of Applied Signal Processing, pp.378–381.   
Madden, S., Franklin, M.J., Hellerstein, J.M. and Hong, W. (2002) ‘TAG: a Tiny AGgregation Service for ad-hoc sensor networks’, 5th Symposium on Operating System Design and Implementation (OSDI), Boston, Massachusetts, pp.136–141.   
Madden, S., Franklin, M.J., Hellerstein, J.M. and Hong, W. (2003) ‘The design of an acquisitional query processor for sensor networks’, ACM SIGMOD, San Diego, CA, pp.491–502.   
Mainwaring, A., Culler, D., Polastre, J., Szewczyk, R. and Anderson, J. (2002) ‘Wireless sensor networks for habitat monitoring’, The 1st ACM International Workshop on Wireless Sensor Networks and Applications, pp.88–97.   
Mainwaring, A., Polastre, J., Szewczyk, R., Culler, D. and Anderson, J. (2004) ‘Wireless sensor networks for habitat monitoring’, Communications of the ACM, Vol. 47, pp.34–40.   
Meguerdichian, S., Koushanfar, F., Qu, G. and Potkonjak, M. (2001) ‘Exposure in wireless ad hoc sensor networks’, International Conference on Mobile Computing and Networking (ACM MobiCom), Rome, Italy, pp.139–150.   
Ngan, H., Zhu, Y., Ni, L.M. and Xiao, R. (2005) ‘SAS: Stimulus-based adaptive sleeping for wireless sensor networks’, The 34th International Conference on Parallel Processing (ICPP), Norway, pp.381–388.   
Pottie, G.J. and Kaiser, W.J. (2000) ‘Wireless integrated network sensors’, ACM Communications, Vol. 43, pp.51–58.

Rakhmatov, D. and Vrudhula, S. (2003) ‘Energy management for battery-powered embedded systems’, ACM Transactions on Embedded Computing Systems, Vol. 2, pp.277–324.   
Salhieh, A., Weinmann, J., Kochhal, M. and Schwiebert, L. (2001) ‘Power efficient topologies for wireless sensor networks’, International Conference on Parallel Processing (ICPP), Valencia, Spain, pp.156–163.   
Shih, E., Cho, S.H., Ickes, N., Min, R., Sinha, A., Wang, A. and Chandrakasan, A. (2001) ‘Physical layer driven protocol and algorithm design for energy-efficient wireless sensor net-works’, 7th Annual International Conference on Mobile Computing and Networking (ACM MOBICOM), pp.272–287.   
Shurgers, C. and Srivastava, M.B. (2001) ‘Energy efficient routing in wireless sensor networks’, MILCOM, Vienna, VA, pp.357–361.   
Sohrabi, K., Gao, J., Ailawadhi, V. and Pottie, G.J. (2000) ‘Protocols for self-organization of a wireless sensor network’, IEEE Personal Communications, Vol. 7, pp.16–27.

Xu, C., Cheung, S.C. and Xiao, X. (2004b) ‘Semantic interpretation and matching of web services’, The 23rd International Conference on Conceptual Modeling, Shanghai, China, pp.542–554.   
Xu, C., Cheung, S.C., Lo, C., Leung, K.C. and Wei, J. (2004a) ‘Cabot: on the ontology for the middleware support of context-aware pervasive applications’, Building Intelligent Sensor Networks (BISON’04), pp.568–575.   
Ye, W., Heidemann, J. and Estrinf, D. (2002) ‘An energy-efficient MAC protocol for wireless sensor networks’, International Annual Joint Conference of the IEEE Computer and Communications Societies (IEEE INFOCOM), New York, NY, pp.1567–1576.   
Zhao, F., Shin, J. and Reich, J. (2002) ‘Information-driven dynamic sensor collaboration for tracking applications’, IEEE Signal Processing Magazine, pp.61–72.