REGULAR PAPER

Chunming Hu · Yanmin Zhu ·

Jinpeng Huai · Yunhao Liu · Lionel M. Ni

# S-Club: an overlay-based efficient service discovery mechanism in CROWN Grid

Received: 20 October 2005 / Revised: 9 May 2006 / Accepted: 18 August 2006 /

Published online: 21 March 2007

C Springer-Verlag London Limited 2007

Abstract Information service plays a key role in grid system, handles resource discovery and management process. Employing existing information service architectures suffers from poor scalability, long search response time, and large traffic overhead. In this paper, we propose a service club mechanism, called S-Club, for efficient service discovery. In S-Club, an overlay based on existing Grid Information Service (GIS) mesh network of CROWN is built, so that GISs are organized as service clubs. Each club serves for a certain type of service while each GIS may join one or more clubs. S-Club is adopted in our CROWN Grid and the performance of S-Club is evaluated by comprehensive simulations. The results show that S-Club scheme significantly improves search performance and outperforms existing approaches.

Keywords Grid computing · Information service · CROWN · Service discovery · Service club

# 1 Introduction

In the past few years, the grid computing paradigm has emerged, promising to enable resource sharing and collaborating across multiple domains [3, 9, 10, 12, 13]. In the research community, there has been an intense interest in designing and studying of such system. The main goal of our key project, CROWN (China R&D Environment Over Wide-area Network), is to empower in-depth integration of resources and cooperation of researchers nationwide and worldwide. CROWN was started in late 2003. Up until mid 2005, eight universities and institutes across four cities in China have joined CROWN, with each contributing 50–100 computers. And more than 25 universities and institutes are invited to join CROWN Grid by the end of 2005. Lots of applications in different domains have been deployed into CROWN Grid, such as gene comparison in bioinformatics, climates pattern prediction in environment monitoring, etc. The long-range goal for CROWN is to integrate home user resources in a fully decentralized way with a robust, scalable grid middleware infrastructure. Recently, with the evolution of Web services, the service-oriented architecture has become a significant trend for grid computing, with OGSA/WSRF as the de facto standards [11, 21]. CROWN has adopted the service-oriented architecture, connecting large amount of services deployed in universities and institutes.

In a complex grid environment, it is of great importance for users to locate desired services. To this end, grid information services (GISs) are deployed to provide dynamic information of services. In general, there are one or multiple GISs deployed in each domain to provide information about services available within the domain. With the rapid growth of CROWN, more domains join and therefore there will be numerous GISs. Different GISs are connected according to different relations, such as affiliation and cooperation. The GISs comprise a mesh network according to predefined configurations. The evolvement of the mesh network is free and out of our control. To search for services across the existing mesh network, however, suffers from poor performance, i.e., long response time and huge traffic overhead. When users want to find desired services, they have no choice but to flood search request to all of the GISs in the grid network.

Many efforts have been made to improve information service for grid computing. Some centralized approaches, such as MDS-1 [8], Hawkeye [15] and R-GMA [6], have been designed for small-scale grid systems. In these approaches, only one centralized server is deployed to provide information service. They have advantages of simplicity and ease to use, but as the scale of grids is large, they suffer from single-point-of-failure and low scalability. In large-scale grid systems, a large number of GISs are deployed. To provide information service for such grid systems, several solutions, such as MDS-2 [5] and GAIS [16], have been proposed. Most of the solutions have adopted a hierarchical architecture to organize GISs. To search services over the GISs, however, we have to traverse a partial of the hierarchical architecture, which could cause long latency as well as huge search traffic. In summary, no existing approaches can provide efficient information service for CROWN Grid.

In this paper, we propose a service club mechanism, called S-Club, for efficient service discovery, optimizing search performance in the GIS mesh network. The basic idea of S-Club is to build an overlay over the existing GIS mesh network of CROWN. Based on the observation that the end users always want to find services by a certain type or catalogue, an overlay network on existing GIS mesh network is built. We use MST as the overlay topology to get the minimum cost when we transmit messages in the overlay. In S-Club scheme, GISs are organized as service clubs. Each club serves for a certain type of service while each GIS may join one or multiple clubs. When a user wants to find a service, it first issues a query in the overlay. Flooding is restricted in one or several clubs. If the search in the clubs fails, the query will flood over the whole topology. Our later experimental results will show that S-Club significantly improves search response time as well as reduces traffic overhead incurred by search.

The rest of this paper is organized as follows. In Sect. 2, an overview of overlay network is given. In Sect. 3, some related work is introduced. Section 4 presents the design of S-Club and Sect. 5 discusses the implementation of S-Club in Resource Locating and Descripting Service (RLDS), the information service of CROWN Grid. Section 6 presents simulation methodology and the evaluation of the performance of S-Club. Section 7 concludes our work.

# 2 Overlay network

Overlay technique is an effective way to support new applications as well as protocols without any changes in underlying network layer. The basic idea of the overlay network is to build a new network over existing physical network nodes according to some selected logical rules. With the application of new protocols for the added upper network, the performance can be optimized. A typical overlay network is consisted of some overlay nodes and some connections between the overlay nodes, called overlay links. The overlay nodes are selected from the underlying physical network, while the overlay links are always composed of one or more physical links. The message passing between overlay links must be mapped into the physical layer, as shown in Fig. 1. For example, when overlay node ON1 sends a message to ON2, the message will be transmitted along the path with small arrow.

Several different overlay service networks have been proposed, such as Resilient Overlay Network (RON) [2], Service Overlay Network (SON) [7], and

![](images/57fdef92b210ef7622b650018f7a171446e1b94c2c2427b962ef7c3f137cbbf8.jpg)



Fig. 1 An example of overlay network

OverQoS [23]. For example, RON uses overlay network to increase the reliability of Internet routing protocol by providing better overlay paths when default Internet paths get fault. SON purchases bandwidth with certain quality of service (QoS) guarantees from individual network domains via bilateral service level agreement to build an end-to-end service infrastructure on top of existing data transport network.

By reviewing the existing approach of overlay network, we summarize the basic procedure of overlay-based network enhancement technique. First, several physical nodes should be selected according to a set of selected rules; second, a rule of creating the logical links should be identified so as to link the separated physical nodes into a graph with specified topology; third, a routing protocol should be designed to exchange messages alone the overlay network.

To design an overlay network, the first step is to choose an overlay topology to connect all the overlay nodes. There several kinds of topologies which are widely used, such as fully-mesh, K-minimum spanning tree (KMST), topologyaware-KMST, and adjacent connection, etc. Li and Mohapatra [18] did a study on the impact of topology on overlay routing service. Result shows that the overlay topology has significant impact on the overlay routing in terms of routing performance and routing overhead. Moreover, the physical topology information may help a lot when constructing an efficient overlay topology.

# 3 Related work

Monitoring and Directory Service (MDS-1) [8] is the information service of early Globus project [9]. Data in MDS-1 is organized as a directory information tree. Such a centralized solution may suffer performance bottleneck and single-pointof-failure.

MDS-2 [5] provides a configurable information provider component Grid Resource Information Service (GRIS) and an aggregate directory component Grid Index Information Service (GIIS) in a service-oriented architecture [21]. It is a hierarchical infrastructure where each GIIS defines a scope within which search operations taking place, allowing users within a VO to perform efficient search. Response time of querying GIIS grows quickly with the increment of number of GRIS [26].

Hawkeye [15] is developed in Condor project to collect information from each resource in a global resource pool. It uses Condor ClassAd language to identify resources, and ClassAd Matchmaking to find available resources. Hawkeye uses a single component Manager, managing multiple Monitoring Agents. User first asks Manager for the address of one agent, then sends query to it. It is a fixed two-level hierarchical architecture and the Manager may become the single point of failure.

Relational Grid Monitoring Architecture (R-GMA) [6] is an implementation of GMA [24]. It is based on relational data model. Producers push resource information to RDBMS of the centralized GMA Registry. Consumers query the Registry to find out what types of information are available and to locate the corresponding Producers. It is also a centralized architecture.

GAIS [16] is an OGSI-compliant Grid Advanced Information System and conforms to flat and dynamic architecture. It introduces a P2P searching mechanism to exchange VO information between GISs. If the VO does not exist within the

GAIS instance, the GAIS attempts to look it up with other GAIS instance using a flooding mechanism.

UDDIe is the service registry system in the context of the G-QoSM, which is a service-oriented grid framework focusing on QoS guarantee and resource reservation. It is used primarily as a registry to publish QoS attributes of services, and subsequently to search for services based on QoS attributes. In a specified service grid environment, only one UDDIe server is deployed and used to handle service registration and discovery requests.

Enhanced Discovery Server (EDS) [25] proposed a basic service discovery framework for wide area network. EDS adopts a hierarchical architecture to organize multiple EDS servers and providing QoS aware service discovery.

Searching in decentralized GIS architecture in grid environment is similar with content location in peer-to-peer file-sharing applications such as Gnutella, Freenet and Napste. Iamnitchi et al. [17] analysis the correlations between content location in peer-to-peer environment and resource/service discovery in grid environment and proposed a peer-to-peer approach to resource location in grid environment.

Compare to the existing approaches, S-Club adopts a fully decentralized architecture with an unstructured topology. Each GIS keeps the information of services registered to it. To improve the performance, overlay is constructed dynamically and may be changed constantly with the self-organizations of service clubs.

# 4 Design of S-Club

In this section, we first give an overview of our approach, S-Club, an overlaybased GIS topology protocol and then discuss on why a service has a certain type from the perspectives of both application requirement and implementation details. Third, we present service clubs construction in a decentralized manner, as well as dynamic club maintenance. Finally, we explain how users search for services with the help of service clubs built on top of the existing GIS mesh network.

# 4.1 Overview of S-Club

The basic idea of S-Club is to build an overlay over the existing GIS mesh network. In such an overlay, GISs providing the same type of services organized into a service club. An example of such a club overlay is shown in Fig. 2, where nodes C, D, E, G form a club. A search request could be forwarded to the corresponding club first such that search response time and overhead can also be reduced if the desired result is available in the club.

Intuitively, to set up a club requires information exchange, and clubs need to be maintained dynamically because new GISs may join and some existing GISs may leave. Also, it is possible that some types of services become less popular after the club is built. Therefore, we have to be careful on the trade-off between the potential benefit and the cost incurred. In general, the usage of services is not uniformly distributed. Some types of services can be very popular and others may not. When/how clubs are constructed/destroyed will be key issues in S-club scheme.

![](images/e7347e8f7d42168ace4bcf7387622126bb19338f2bda2b9c2a70c70205e425d5.jpg)



Fig. 2 An example of service club

# 4.2 Service type

In a grid application, a service is always deployed onto different hosts, i.e., there are several service instances which are deployed and distributed in the whole Grid environment. When a user wants a kind of service, it always wants to obtain a list of all (or part) of the available services in the grid. Service type is one of the important properties that the user has to specify before a search is performed. It can be either quite general or very specific.

Service type classification also exists in both semantic and syntax level. Existing works on semantic grids and semantic web services focus on building unified service ontology to enable service classification with semantics. Recently, OGSA/WSRF is evolving into the de facto standards for grid computing. OGSA allows us to define service templates formally, which introduces a standard interface definition mechanism for grid services to provide uniform service semantics. A service template is defined by specifying the required port types. Anyone who wants to provide this type of service can implement such service template. A service type is characterized by one or more specified port types. Another advantage of the template-based service type is that, if two service instances share the same type, they can be replaced smoothly without changing the code from client side.

In CROWN, any community is able to create service types of interest. Definition of service types are published in an information server for access by the public. Service providers who have common interest can implement and deploy services according to the type information obtained from the public server.

# 4.3 Selection of overlay topology

To connect all the club members, we have to find out a proper topology with acceptable reliability and minimum service discovery cost. At the same time, a feasible distributed topology creation algorithm is also necessary for the selected topology. At this point, we choose the minimum spanning tree (MST) as the topology of S-Club.

The reason of choosing MST is listed as follows. Firstly, MST topology can make sure that all the overlay nodes are connected; second, MST will get the minimum cost when we transmit messages in the overlay. Secondly, although there is only one available link between any two linked overlay nodes, the absence of any node may divide the topology into two disconnected sub-graph and cause the partition problem, which makes the topology unstable. However, considering the scenario of S-Club, we always choose the RLDS as the S-Club overlay node. In a production grid, we can assume that the RLDS nodes are always severed by some stable grid nodes. So the overlay nodes of S-Club may have better reliability and availability and lower fault possibility than other nodes. Thirdly, a simple failure recovery algorithm (see Sect. 4.5 for details) may bring an acceptable reliability for MST topology. Li and Mohapatra [18] discuss the performance of different topology including fully-mesh, MST, 2MST, T2MST by considering the performance and reliability of the different topologies. Result shows that MST has the best per-node routing overhead and best recovery path hop penalty and acceptable failure recovery ratio when the node failure probability is below than 1% . And finally, MST has lot of distributed creation algorithm [1], which can be used in S-Club scenario without further modification. Based on these considerations, we choose MST as the overlay topology in the S-Club scenario.

# 4.4 Club construction

In S-Club scheme, each GIS maintains usage frequency (UF) of registered service types locally. Given a GIS, UF of a service type, T, is defined by

$$
U F (T) = \frac {N (T)}{M}
$$

where N (S) denotes the number of invocations on services of type T , and M is the total number of invocations of services registered at this GIS. We require every service to report to the GIS where it is registered once it is invoked by users or in a periodical way. In general, UF(T) at a GIS indicates how often services of type $T$ are invoked recently, relative to other types at the same GIS.

Each GIS starts club establishment process periodically. The interval for each GIS is generated randomly by the GIS itself so that the GISs do not start the process simultaneously. The asynchronism among GISs helps to avoid possible conflictions and traffic jam. Once the process is started, the GIS will establish clubs for those service types which have highest UFs but not have a club yet. One key issue here is for how many service types the GIS should establish clubs. We introduce frequency threshold, denoted as α, ranging from 0 to 100. Each GIS tries to establish clubs for the top α% of the service types.

The selection of α directly impacts the number of resulting clubs. Suppose there are in total T service types, and I GISs. We assume service types are uniformly distributed among GISs. Then the expected number of exclusive types in a single GIS is $[ \frac { T } { I } ]$ . On average, each GIS can build at most $[ \frac { T } { I } ] \times \alpha \%$ clubs. Therefore, the total number of clubs is bounded by $( [ \frac { T } { I } ] \times \alpha \% ) \dot { \times } I$ . A larger α results in more clubs. In S-Club, α is tuneable so that a good α can be selected for different network conditions.

![](images/79d918aa6c925cce56a1714a1b1a8c0ee82063d1e4d9dc33f88d02c544db0379.jpg)



（a)

![](images/64d506375b9644b9025a26847d018f79921e65f6a7d515f1be6e63cb7c3b0333.jpg)



（b)  
Fig. 3 Maintenance of a service club

Each GIS checks the set of top α% service types, if it finds a type in the set has not been established as a club, it attempts to initiate club establishing process. For example, if GIS G tries to establish a club for type B. G floods an SETUP-REQUEST announcement for type B throughout the mesh network, consulting the other GISs whether to set up a club for type B. On receiving the announcement, a GIS with type B services first checks its local table. If $U F ( B )$ at this GIS is also within top $\alpha \%$ , it replies $\cdot Y E S '$ to G, otherwise, it replies with $\cdot \cal N O ^ { \prime }$ . After a certain time, G gets all the replies, and then it calculates the support ratio δ,

$$
\delta = \frac {N (Y E S)}{N (Y E S) + N (N O)}
$$

where N (YES) is the number of YES replies, and N (NO) is the number of NO replies. In S-Club, we set a construction threshold. If δ is greater than the threshold, G will build a club for type B; otherwise, G gives up.

If G decides to establish a club for type B, it sends a SET-UP announcement to those GISs which replied previously and now club members. The SET-UP announcement encloses the list of all members, and so we get a virtual complete graph, as illustrated in Fig. 3a. The cost in this graph is probed by each member independently. The next issue is how these members are connected. The objective is to make the club robust while introducing as less maintenance overhead as possible. In S-Club, we build a minimum spanning tree (MST) among club members. We employ the algorithm proposed in Abdel-Wahab et al. [1], where a collection of disjoint trees spanning all the group members is maintained. Every tree independently expands by joining the closest tree, until all nodes are connected in a single tree. It is proved that given a graph with n nodes, the distributed algorithm for constructing MST takes O(n) time. Using this method, a MST among all members is created ass shown in Fig. 3b. G then sends a NEW-CLUB announcement to all GISs with full list of club members.

# 4.5 Club maintenance

Clubs should be dynamically maintained. On one hand, GISs themselves are dynamic. Some may become unavailable because of hardware failure. On the other hand, services registered in a GIS are also dynamic. Some services may be newly registered at the GIS, and existing services could be removed. The consequence is that GISs need to join or leave corresponding clubs.

In our design, the topology in a club is a minimum spanning tree, which suffers from single-point-failure. One node leaving the club may lead to topology disconnection. To solve this problem, we employ a club member management protocol similar to Narada [4]. To this end, each club member maintains a full list of all the members, and every member’s list needs to be updated when a new member join or an existing member leaves. To disseminate the changes, we require that each member periodically generate a refresh message with monotonically increasing sequence number, which is propagated along the MST. On receiving a refresh message from neighbor j, member i updates its table according to the algorithm in Chu et al. [4].

When a GIS is registered with a new type of service, it checks locally whether there exists a club for this type. If yes, it sends a JOIN announcement using the address of the club, which will be flooded within the club. Each club member replies to the new GIS so that the GIS can get the list of the club members. Then the joining member selects a few club members from the list and sends them messages requesting to be added as their neighbor. It repeats the process until it gets a response from one of them. Having joined, the member then starts exchanging refresh messages with its neighbors and propagates the changes of new member joining. Obviously, this method cannot assure the member topology to be a MST, but a spanning tree.

When a member leaves a group purposely, it notifies its neighbors in the spanning tree, linking all its children to its parent. These changes will also be propagated through the exchange of refresh message to the entire club.

We also need to consider another case of abrupt failure. As mentioned above, each member receives refresh messages from its neighbor periodically. If a member does not receive refresh message from its neighbor for a certain period of time, the direct neighbor may be failed. The member sends an announcement to find the neighbor of the failed node along the underlying mesh network. Thus, abrupt failure can be detected and the partition of spanning tree can be repaired. Changes can also be propagated through the exchange of refresh messages.

Member joining and leaving constantly may cause the performance of topology of the club members (i.e., the spanning tree) degraded. To rebuild the MST, the root need to initiate the distributed MST algorithm periodically and propagates the newest member through another NEW-CLUB announcement.

On receiving a NEW-CLUB announcement, every other GISs will choose one of the members from the list as the address of the club. Once this member leaves the club, the GIS may ask their neighbors in underlying mesh network to get another member as the new address. With the periodically reconstruction of member topology, this GIS can refresh their club address constantly. Consequently, any GIS can find an available member as the entry to each service club.

# 4.6 Club deconstruction

It is possible that a previously popular service type become unpopular. If the services of this type are rarely requested, the club maintenance cost may exceed the benefit the club brings. Therefore, in this case, we should close the club. Moreover, closing unpopular clubs allows us to dynamically control the number of clubs in an appropriate level.

The deconstruction process of a club is similar with the construction of a club. Each GIS periodically starts the deconstruction process. Once the process is started, the GIS will try to close clubs for those service types whose UFs are out of the top $\alpha \%$ . We set the Deconstruction Threshold as γ . If close support ratio δ is greater than γ , G will close the club; otherwise, the club remains. If G decides to close the club, it floods a CLOSE announcement throughout the network. For members of this club, they remove relevant club connections. And, for normal GISs, they remove the club record.

# 4.7 Service search with S-Club

Here, we discuss how users search services with the availability of service clubs. To simplify our discussion, we assume a user simply wants to get the list of available services of a specific type. However, the search model can be safely extended to more general cases; for example, the user can specify more constraints based on service properties.

It is assumed that any search request is firstly sent to a GIS close to the user. On receiving a search request for a specific service type, the GIS checks locally whether there has been a club for this type. If yes, the GIS forwards the request to the club, which will be flooded within the club only. Each club member then returns the information of the relevant services to the user. Since the request is strictly restricted within the club and no irrelevant GISs is involved, much traffic is saved. If there is no club for this type, however, the GIS has no choice but to flood the search request throughout the mesh network.

When a new GIS joins the GIS network, it has no idea what clubs are there. But since it has at least one neighbor in the underlying mesh network, it can ask one of its neighbors for the information of existing clubs. Namely, it simply copies the information of clubs from its neighbor.

As the GISs are dynamic, some may become unavailable. AS mentioned previously, the address of a club is denoted by two members in this clubs. For one GIS, the problem arises if the two GISs become unreachable simultaneously. The GIS cannot reach the club when a user wants to search services of this type. In this case, we require that it firstly copy the address (i.e., IPs of two members) of the club from one of its neighbor. Next, it sends an ECHO announcement to the club, for which each club member will reply with its own IP. Then, with the list of club members, the GIS is able to select two best members in terms of round-trip time as the address of the club.

# 5 RLDS: an S-Club implementation in CROWN environment

According to the protocol and search mechanism described above, we designed a modular grid information service architecture for our CROWN Grid, called Resources Locating and Describing Service (RLDS), which allows us to easily test and modify each component separately. This RLDS service is a WSRF service implemented in Java in order to take advantage of great number of code libraries available. Another advantage is this service can be deployed into a Globus Toolkit 4.0 compliant service container with little changes. The architecture of a RLDS (see Fig. 4) is constituted by the following basic modules.

![](images/8a56737bb96b4d5f1cd3557731e87e89dd306e2febb417bec9ae5e4ffbae534e.jpg)



Fig. 4 The RLDS architecture

1. Message Listener and Message Queue: This is the interface part of RLDS service. Message Listener translates all the received SOAP messages into protocol message object and put into the message queue for scheduling.   
2. Message Dispatcher: A module dispatches the message object in the queue to the right processor (i.e, the session management module, the club management module, the club search module and the local search module).   
3. Session Management: Maintain the search session. The RLDS will create a new session for each service request and check the result received by itself.   
4. Club Management Module: Manages all the service clubs which this RLDS service belongs to. Also this module will maintain all the index and pointers to members of other service clubs.   
5. Club Search Module: Forward query messages in the overlay network defined by short-cuts of club members. Once the club search fails, forward in the underlying mesh network.   
6. Local Search Module: Maintain all the information and registered services, response for the local search request and check the user frequency of each type of service.   
7. Logging Module: Log all the events into database. Use frequency is calculated according to the logs.

# 6 Performance evaluation

To evaluate the performance of our proposed S-Club, we designed a simulation tool, in which a certain number of GISs is connected selectively to form an underlying mesh network.

# 6.1 Simulation methodology

To simulate the service discovery process, first we generate the underlying GISs topologies, and distribute service information into each GIS node. When simulation runs, a certain number of service discovery request R(T s, N ) is generated and sent to one of a GIS node, while T s is the service type identifier, and N is the number of available services user wants to get. The request with the address of the first GIS node is propagated along the GISs network, the GIS which has available services of type T s sends reply to the first GIS node. Finally, the first GIS node sends an available service list of N services to end user as the response.In studying the performance of our algorithms, we compare it to the MDS-like System without S-Club mechanism, which using the discovery protocol of MDS2. If a MDS server cannot answer the user request, it sends the request to its direct neighbors. i.e., request is flooded in the mesh network to find available services.

BRITE [20] is a topology generation tool that provides the option to generate topologies based on the AS Model.We generate 10 network topologies with 20,000 nodes. Since the GISs is deployed into some of nodes over internet, the mesh network topologies are generated with a number of nodes ranging from 100 to 1000 selected from the 20000 physical network topologies. We generate the GISs mesh topologies with average two edge connections, means there are four logical neighbors for each GIS. The bandwidth between every two GIS nodes is calculated according to the shortest path along the physical network topologies.

The generation of the service discovery requests is modeled as a Poisson process, and the generation interval of requests is therefore exponentially distributed. In our simulation, each GIS node receives 6.42 queries per minute, which is calculated from the observation data shown in Smith et al. [22], i.e., 143,446 operations, including 7710 query operations, were received by a single MDS server during 20 h.

In our simulation, the requested service type is under the control of Request Distribution, which is defined as the probability of finding a certain type of service. Our observation in CROWN Grid shows that some types of service is much more popular than others. In our simulation, we assure about 70% of requests are searching for 20% type of services. Percentage of Requested Services (PRS) is used to control the required length of the available list. For example, if there are totally m services of type T deployed in the grid, a query request with P RS = k% means a list with at least m × k% available services should be returned. P RS during the simulation is ranging from 10% to 100%.

# 6.2 Metrics

The kernel function of GISs is to answer the user request like “where are available services of type $A ^ { \prime \prime }$ . In order to evaluate S-Club, we use following three performance metrics: average response time, total traffic overhead, and optimization ratio.

Average Response Time of a query is one of the parameters concerned by end users. We define response time of a query as the time period from when the query from end user is received by the first GIS node, and until when this node collects all the response results from other GISs and meets the end user’s demands.

![](images/b0aa100db2078b8c371c81ccfdf0cbaad9bfc912795d4c3375c5566667733d10.jpg)



Fig. 5 Number of clubs vs. frequency threshold α

![](images/17af3c6d0753ccf5b97520d519e064f41a5f07add21d62f5dafeb1a9d2699da1.jpg)



Fig. 6 Total traffic vs. frequency threshold α

Total Traffic Overhead of a query is defined as the length of message sent among GISs to answer the query. If S-Club is adopted, the traffic overhead of creating, maintaining and deleting is also included. We have traced the real message in CROWN Grid, in which GIS is wrapped as an OGSA Grid Service using SOAP messages. Including the head of SOAP message, the size of all related messages is ranging from 1500 to 3000 bytes.

Optimization Ratio shows the benefit of S-Club mechanism with comparison to MDS-like system. The optimization ratio of average response time is defined as

![](images/802a207ecb8e93e64ff2b433aabd43ce28f1774c7dba65f32aece5a4c1dfc60b.jpg)



Fig. 7 Total traffic vs. frequency threshold α

![](images/528e7cb4a456b60b7c375f2d85c90714fc241ba9f58446b6cae55209506197de.jpg)



Fig. 8 Average response time vs. simulation time

follows:

$$
\text { Optimization   ratio } = \frac {A R T _ {M} - A R T _ {S}}{A R T _ {M}}
$$

while $A R T _ { M }$ is the average response time of MDS-like system and $A R T _ { S }$ is the average response time of S-Club system.

![](images/265b0f50538851de3bee3043b74e221f5c75b492db93c24810edc5f3f5d87b0d.jpg)



Fig. 9 Total traffic vs. % of requested services

![](images/3bdba3c2a41dcbddf1021d0682c582a1ec8c5e1a766bc89302a3e196c0335563.jpg)



Fig. 10 Average response time vs. % of requested services

# 6.3 Simulation result analysis

In our first simulation, we study the effectiveness of frequency threshold α in S-Club. Figure 5 shows the frequency threshold affects the total number of clubs remarkably. In Figs. 6 and 7, we see that with the increment of α, total traffic and average response time are not always improved. Intuitively, too many clubs may bring much maintenance overhead. There exists a best value of α to maximize the benefit of S-Club. For example, Fig. 6 shows that in this simulation, 0.5 is the best choice of α.

![](images/f3a96a5d4951576b2f6da4cf66421af03c4401ce5a8fe6222b3def6b6a3b5dbe.jpg)



Fig. 11 Total traffic vs. number of requests

In the second simulation, we compare the S-Club with MDS-like systems. In Fig. 8, the parameter $p$ stands for the percentage of requested services. We see that with the time elapses, average response time of all MDS-like systems is almost a constant while the average response time of S-Club systems is decreasing gradually and finally comes to a stable state. Figures 9 and 10 plot the benefit ${ \bf S } -$ Club mechanism brings with the change of parameter $p$ with a GIS network of 400 nodes. With the increment of $p _ { : }$ , total traffic and average response time increase together. We find that S-Club reduces the total traffic by 46% and average response time by around 7–26%.

In the third simulation, we study the benefit of traffic brought by S-Club. We simulate three groups with scale of 100, 200 and 400 GIS nodes and compare with the MDS-like system. The simulation results in Figs. 11 and 12 show that S-Club reduces total traffic and average response time significantly. For example, when n = 200 and total number of requests is 60,000, S-Club reduces traffic by 55% and average response time by 27%.

![](images/681fa293ec34534e49d539cd4422c0a172eabf73b5afda6aba71ce49d5185cc5.jpg)



Fig. 12 Response time vs. number of requests

![](images/5401e202ea565809dafd520fa4a15b2fa640bc92df2675277660836f65fa8772.jpg)



Fig. 13 Scalability of S-Club, average response time vs. number of GISs

The last simulation studies the scalability of S-Club with the scale of GIS network increases. As illustrated in Fig. 13, we simulate another three groups with scale of 100–1000 GIS nodes and comparison the average response time to MDSlike system. With the number of GIS servers increases, S-Club gives more benefit on average response time. Figure 14 shows the optimization ratio of average response time. Having 1000 GIS nodes, S-Club reduces about 27–35% response time.

![](images/375c0f6c133e2add072beb7ad4d0b8681ed8e9305db242c07930edf982980445.jpg)



Fig. 14 Optimization ratio of average response time (ART)

# 7 Conclusions

Our key project, CROWN, holds the ambitious goal to integrate nationwide and worldwide valuable resources. Efficient information service is fundamentally important in CROWN. In this paper, we proposed the S-Club scheme to improve the performance of information service in CROWN. We build an overlay over the existing mesh network of GISs. For those popular services, we establish service clubs, in which GISs providing the same type of services are closely connected. When a user wants to search a service, the search request is effectively restricted within the small club. Simulation results demonstrate that S-Club significantly improves service search performance and outperforms the existing approaches. S-Club has been successfully implemented in our CROWN Grid environment.

Acknowledgements Part of this work is supported by grants from the China National Science Foundation (No. 91412011), China 863 High-tech Programme (Project No. 2005AA119010), China 973 Fundamental R&D Program (No. 2005CB321803) and National Natural Science Funds for Distinguished Young Scholar (Project No. 60525209). We would also like to thank Hailong Sun, Xianbo Xia and Tianyu Wo at Beihang University for helping us to do the simulation on the cluster.

# References

1. Abdel-Wahab H, Stoica I, Sultan F, Wilson K (1995) A simple and fast distributed algorithm to compute a minimum spanning tree in the internet. In: Proceedings of the joint conference on information sciences’95, North Carolina, pp 429–433   
2. Andersen DG, Balakrishnan H, Kaashoek M, et al (2001) Resilient overlay networks. In: Proceedings of 18th ACM symposium on operating systems principles (SOSP’01), Banff, Canada, pp 131–145   
3. Chapin SJ, Katramatos D, Karpovich J, Grimshaw A (1999) Resource management in Legion. In: Proceedings of workshop on job scheduling strategies for parallel processing, in conjunction with the international parallel and distributed processing symposium   
4. Chu Y-H, Rao SG, Seshan S, Zhang H (2000) A case for end system multicast. In: Proceedings of ACM sigmetrics 2000, Santa Clara, CA   
5. Czajkowski K, Fitzgerald S, Foster I, Kesselman C (2001) Grid information services for distributed resource sharing. In: Proceedings of the 10th IEEE international symposium on high-performance distributed computing (HPDC-10)   
6. DataGrid: DataGrid DataGrid (2003) Information and monitoring services architecture: design, requirements and evaluation criteria. Technical report   
7. Duan Z, Zhang ZL, Hou YT (2002) Service overlay networks: SLAs, QoS and bandwidth provisioning. In: Proceedings of 10th IEEE international conference on network protocol (ICNP’02)   
8. Fitzgerald S, Foster I, Kesselman C, van Laszewski G, Smith W, Tuecke S (2001) A directory service for configuring high-performance distributed computations. In: Proceedings of the 6th IEEE symposium on high-performance distributed computing, pp 365–375   
9. Foster I, Kesselman C (1997) Globus: a metacomputing infrastructure toolkit. Int J Super Comput Appl 11:115–129   
10. Foster I, Kesselman C (2003) The grid 2: blueprint for a new computing infrastructure. Morgan Kaufmann Publishers   
11. Foster I, Kesselman C, Nick J, Tuecke S (2002) Grid services for distributed system integration. IEEE Comput Mag 35:37–46   
12. Foster I, Kesselman C, Tuecke S (2001) The anatomy of the Grid. Int J Super Comput Appl   
13. Frey J, Tannenbaum T (2002) Condor-G: a computation management agent for multiinstitutional grids. J Cluster Comput 5:237

14. Furmento N, Lee W, Mayer A, Newhouse S, Darlington J (2002) ICENI: an open grid service architecture implemented with Jini. Parallel Comput 28:1753–1772   
15. Hawkeye: http://www.cs.wisc.edu/condor/hawkeye (2004)   
16. Hong W, Lim M, Kim E, Lee J, Park H (2004) GAIS: grid advanced information service based on P2P mechanism. In: Proceedings of the 13th IEEE international symposium on high-performance distributed computing (HPDC-13), pp 276–277   
17. Iamnitchi A, Foster I, Nurmi DC (2002) A peer-to-peer approach to resource location in grid environments. In: Proceedings of the 11th IEEE international symposium on highperformance distributed computing (HPDC-11)   
18. Li Z, Mohapatra P (2004) The impact of topology on overlay routing service. In: Proceedings of IEEE INFOCOM 2004   
19. Litzkow M, Livny M, Mutka M (1988) Condor—a hunter of idle workstations. In: Proceedings of the 8th international conference of distributed computing systems, California   
20. Medina A, Lakhina A, Matta I, Byers J (2001) BRITE: an approach to universal topology generation. In: Proceedings of the international workshop on modeling, analysis and simulation of computer and telecommunications systems (MASCOTS)   
21. OGSA (2002) The physiology of the grid: an open grid services architecture for distributed systems integration. http://www.globus.org/research/papers/ogsa.pdf   
22. Smith W, Waheed A, Meyers D, Yan J (2000) An evaluation of alternative designs for a grid information service. In: Proceedings of the 9th IEEE international symposium on highperformance distributed computing (HPDC-9)   
23. Subramanian L, Stoica I, Balakrishnan H, et al (2004) OverQoS: an overlay-based architecture for enhancing internet QoS. In: Proceedings of USENIX 1st symposium on networked system design and implementation (NSDI 2004), pp 71–84   
24. Tierney B, Aydt R, Gunter D, Smith W, Taylor V, Wolski R, Swany M (2003) A grid monitoring architecture. The Global Grid Forum GWD-GP-16-2   
25. Xu D, Nahrstedt K, Wichadakul D (2001) QoS-aware discovery of wide-area distributed services. In: Proceedings of the 1st IEEE/ACM international symposium on cluster computing and the grid (CCGrid 2001), pp 92–99   
26. Zhang X, Freshl JL, Schopf JM (2003) A performance study of monitoring and information services for distributed systems. In: Proceedings of the 12th IEEE international symposium on high-performance distributed computing (HPDC-12)

![](images/8afa57bbc515bf13b1adc6a8c59beddbc533d774312bbafdca6c71c2bd872291.jpg)



Chunming Hu is a research staff in the Institute of Advanced Computing Technology at the School of Computer Science and Engineering, Beihang University, Beijing, China. He received his B.E. and M.E. in Department of Computer Science and Engineering in Beihang University. He received the Ph.D. degree in School of Computer Science and Engineering of Beihang University, Beijing, China, 2005. His research interests include peer-to-peer and grid computing; distributed systems and software architectures.

![](images/58beac5b98fef1d4e66f61331a2c4c76a2bec622899c780411cd2a0af61717a9.jpg)



Yanmin Zhu is a Ph.D. candidate in the Department of Computer Science, Hong Kong University of Science and Technology. He received his B.S. degree in computer science from Xi’an Jiaotong University, Xi’an, China, in 2002. His research interests include grid computing, peer-to-peer networking, pervasive computing and sensor networks. He is a member of the IEEE and the IEEE Computer Society.

![](images/857785cfc2bf2390d9676702eab23bb35989ef580f62035326e6643c4749a482.jpg)



Jinpeng Huai is a Professor and Vice President of Beihang University. He serves on the Steering Committee for Advanced Computing Technology Subject, the National High-Tech Program (863) as Chief Scientist. He is a member of the Consulting Committee of the Central Government’s Information Office, and Chairman of the Expert Committee in both the National e-Government Engineering Taskforce and the National e-Government Standard office. Dr. Huai and his colleagues are leading the key projects in e-Science of the National Science Foundation of China (NSFC) and Sino-UK. He has authored over 100 papers. His research interests include middleware, peer-to-peer (P2P), grid computing, trustworthiness and security.

![](images/f47659b556e292022b62c58c52e443b31e2f22c4087033042cbc619c940f7ad8.jpg)



Yunhao Liu received his B.S. degree in Automation Department from Tsinghua University, China, in 1995, and an M.A. degree in Beijing Foreign Studies University, China, in 1997, and an M.S. and a Ph.D. degree in computer science and engineering at Michigan State University in 2003 and 2004, respectively. He is now an assistant professor in the Department of Computer Science and Engineering at Hong Kong University of Science and Technology. His research interests include peer-to-peer computing, pervasive computing, distributed systems, network security, grid computing, and high-speed networking. He is a senior member of the IEEE Computer Society.

![](images/5a2027fbb58a66b0340900fca6b429bb0de8958450555dad2de4da0e882d3c0b.jpg)



Lionel M. Ni is chair professor and head of the Computer Science and Engineering Department at Hong Kong University of Science and Technology. Lionel M. Ni received the Ph.D. degree in electrical and computer engineering from Purdue University, West Lafayette, Indiana, in 1980. He was a professor of computer science and engineering at Michigan State University from 1981 to 2003, where he received the Distinguished Faculty Award in 1994. His research interests include parallel architectures, distributed systems, high-speed networks, and pervasive computing. A fellow of the IEEE and the IEEE Computer Society, he has chaired many professional conferences and has received a number of awards for authoring outstanding papers.