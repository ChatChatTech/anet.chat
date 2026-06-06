# S-Club: An Overlay based Efficient Service Discovery Mechanism in CROWN Grid

Chunming Hu $^{+}$ , Yanmin Zhu $^{*}$ , Jinpeng Huai $^{+}$ , Yunhao Liu $^{*}$ , Lionel M. Ni $^{*}$

$^{+}$ School of Computer Science
Beihang University,
Beijing, China
{hucm, huaijp}@act.buaa.edu.cn

# Abstract

Information service plays a key role in Grid system, handles resource discovery and management process. Employing existing information service architectures suffers from poor scalability, long search response time, and large traffic overhead. In this paper, we propose a service club mechanism, called S-Club, for efficient service discovery. In S-Club, an overlay based on existing GIS mesh network of CROWN is built, so that GISs are organized as service clubs. Each club serves for a certain type of service while each GIS may join one or more clubs. S-Club is adopted in RLDS as the information service in CROWN Grid and the performance of S-Club is evaluated by comprehensive simulations. The results show that S-Club scheme significantly improves search performance and outperforms existing approaches.

Keyword: Grid Computing, Information Service, CROWN, Service Discovery, Service Club

# 1. Introduction

In the past few year, the Grid computing paradigm has emerged, promising to enable resource sharing and collaborating across multiple domains $[4, 8, 9, 12, 13]$ . In the research community there has been an intense interest in designing and studying of such system. The main goal of our key project, CROWN (China R&D Environment Over Wide-area Network), is to empower in-depth integration of resources and cooperation of researchers nationwide and worldwide. CROWN was started in late 2003. Up until mid 2005, 8 universities and institutes across 4 cities in China have joined CROWN, with each contributing 50-100 computers. And more than twenty-five universities and institutes are invited to join CROWN Grid by the end of 2005. Lots of applications in different domains have been deployed into CROWN grid, such as gene comparison in bioinformatics, climates pattern prediction in envi-\* Department of Computer Science,
Hong Kong University of Science & Technology,
Hong Kong, China
{zhuym, liu}@cs.ust.hk

ronment monitoring, etc. The long-range goal for CROWN is to integrate home user resources in a fully decentralized way with a robust, scalable grid middleware infrastructure. Recently, with the evolution of Web services, the service-oriented architecture has become a significant trend for grid computing, with OGSA/ WSRF as the de facto standards [10, 11]. CROWN has adopted the service-oriented architecture, connecting large amount of services deployed in universities and institutes.

In a complex grid environment, it is of great importance for users to locate desired services. To this end, grid information servers (GIS) are deployed to provide dynamic information of services. In general, there are one or multiple GISs deployed in each domain to provide information about services available within the domain. With the rapid growth of CROWN, more domains join and therefore there will be numerous GISs. Different GISs are connected according to different relations, such as affiliation and cooperation. The GISs comprise a mesh network passively. The evolvement of the mesh network is free and out of our control. To search for services across the existing mesh network, however, suffers from poor performance, i.e., long response time and huge traffic overhead. When users want to find desired services, they have no choice but to flood search request to all of the GISs in the grid network.

Many efforts have been made to improve information service for grid computing. Some centralized approaches, such as MDS-1 [7], Hawkeye [1] and R-GMA [2], have been designed for small-scale grid systems. In these approaches, only one centralized server is deployed to provide information service. They have advantages of simplicity and ease to use, but as the scale of grids is large, they suffer from single point of failure and low scalability. In large-scale grid systems, a large number of GISs are deployed. To provide information service for such grid systems, several solutions, such as MDS-2 [6] and GAIS [15], have been proposed. Most of the solutions have adopted a hierarchical architecture to organize GISs. To search services over the GISs, however, we have to traverse a partial of the hierarchical architecture, which could cause long latency as well as huge search traffic. In summary, no existing approaches can provide efficient information service for CROWN Grid.

In this paper, we propose a service club mechanism, called S-Club, for efficient service discovery, optimizing search performance in the GIS mesh network. The basic idea of S-Club is to build an overlay over the existing GIS mesh network of CROWN. Based on the observation that the end users always want to find services by a certain type or catalogue, an overlay network on existing GIS mesh network is built. In S-Club scheme, GISs are organized as service clubs. Each club serves for a certain type of service while each GIS may join one or multiple clubs. When a user wants to find a service, it first issues a query in the overlay. Flooding is restricted in one or several clubs. If the search in the clubs fails, the query will flood over the whole topology. Our later experimental results will show that S-Club significantly improves search response time as well as reduces traffic overhead incurred by search.

The rest of this paper is organized as follows. In section 2, some related work is introduced. Section 3 presents the design of S-Club and section 4 discuss the implementation of S-Club in RLDS. Section 5 presents simulation methodology and the evaluation of the performance of S-Club. Section 6 concludes our work.

# 2. Related Work

Directory Service (MDS-1) [7] is the information service of early Globus project [8]. Data in MDS-1 is organized as a directory information tree. Such a centralized solution may suffer performance bottleneck and single-point-of-failure.

MDS-2 [6] provides a configurable information provider component Grid Resource Information Service (GRIS) and an aggregate directory component Grid Index Information Service (GIIS) in a service-oriented architecture [10]. It is a hierarchical infrastructure where each GIIS defines a scope within which search operations taking place, allowing users within a VO to perform efficient search. Response time of querying GIIS grows quickly with the increment of number of GRIS [21].

Hawkeye [1] is developed in Condor project to collect information from each resource in a global resource pool. It uses Condor ClassAd language to identify resources, and ClassAd Matchmaking to find available resources. Hawkeye uses a single component Manager, managing multiple Monitoring Agents. User first asks Manager for the address of one agent, then sends query to it. It is a half-centralized architecture.

Relational Grid Monitoring Architecture (R-GMA) [2] is an implementation of GMA [20]. It is based on relational data model. Producers push resource information to RDBMS of the centralized GMA Registry. Consumers query the Registry to find out what types of information are available and to locate the corresponding Producers. It is also a centralized architecture.

GAIS [15] is an OGSI-compliant Grid Advanced Information System and conforms to flat and dynamic architecture. It introduces a P2P searching mechanism to exchange VO information between GISs. If the VO does not exist within the GAIS instance, the GAIS attempts to look it up with other GAIS instance using a flooding mechanism.

Searching in decentralized GIS architecture in grid environment is similar with content location in peer-to-peer file-sharing applications such as Gnutella, Freenet and Napste. [16] analysis the correlations between content location in peer-to-peer environment and resource/service discovery in grid environment and proposed a peer-to-peer approach to resource location in grid environment.

Compare to the existing approaches, S-Club adopts a fully decentralized architecture with an unstructured topology. Each GIS keeps the information of services registered to it. To improve the performance, overlay is constructed dynamically and may be changed constantly with the self-organizations of service clubs.

# 3. Design of S-Club

# 3.1 Overview of S-Club

The basic idea of S-Club is to build an overlay over the existing GIS mesh network. In such an overlay, GISs providing the same type of services organized into a service club. An example of such a club overlay is shown in Figure 1, where nodes C, D, E, G form a club. A search request could be forwarded to the corresponding club first such that search response time and overhead can also be reduced if the desired result is available in the club.

![](images/012e2bd128bf0b06582672ce71dab2d35ed3de3b63772e4cd44912951517a937.jpg)



Figure 1: An example of service club

Intuitively, to set up a club requires information exchange, and clubs need to be maintained dynamically because new GISs may join and some existing GISs may leave. Also, it is possible that some types of services become less popular after the club is built. Therefore, we have to be careful on the trade-off between the potential benefit and the cost incurred. In general, the usage of services is not uniformly distributed. Some types of services can be very popular and others may not. When/how clubs are constructed/destroyed will be key issues in S-club scheme.

# 3.2 Service Type

When a user wants a proper service, it actually wants to obtain the list of the corresponding services available in the grid. Service type is one of the important properties that the user has to specify before a search is performed. It can be either quite general or very specific.

Service type classification also exists in both semantic and syntax level. Existing works on semantic grids and semantic web services focus on building unified service ontology to enable service classification with semantics. Recently, OGSA/WSRF is evolving into the de facto standards for grid computing. OGSA allows us to define service templates formally, which introduces a standard interface definition mechanism for grid services to provide uniform service semantics. A service template is defined by specifying the required portTypes. Anyone who wants to provide this type of service can implement such service template. A service type is characterized by one or more specified portTypes.

In CROWN, any community is able to create service types of interest. Definition of service types are published in an information server for access by the public. Service providers who have common interest can implement and deploy services according to the type information obtained from the public server.

# 3.3 Club Construction

In S-Club scheme, each GIS maintains usage frequency (UF) of registered service types locally, as shown in Table 1. Given a GIS, UF of a service type, T, is defined by

$$
U F (T) = \frac {N (T)}{M}, \tag {1}
$$

where $N(S)$ denotes the number of invocations on services of type T, and M is the total number of invocations of services registered at this GIS. We require every service to report to the GIS where it is registered once it is invoked by users. In general, $\mathrm{UF}(T)$ at a GIS indicates how often services of type T are invoked recently, relative to other types at the same GIS.

Each GIS starts club establishment process periodically. Note that GISs do not start the process simultaneously. The asynchronism among GISs helps to avoid possible conflicts and traffic jam. Once the process is started, the GIS will establish clubs for those service types which have highest UFs but not have a club yet. One key issue here is for how many service types the GIS should establish clubs. We introduce Frequency Threshold, denoted as $\alpha$ , ranging from 0 to 100. Each GIS tries to establish clubs for the top $\alpha\%$ of the service types.

Table 1: Dynamic Type Statistics 

<table><tr><td>Service Type</td><td>UF of Service Type</td></tr><tr><td>Type K</td><td>3.56%</td></tr><tr><td>Type B</td><td>3.24%</td></tr><tr><td>Type M</td><td>2.72%</td></tr><tr><td>Type Y</td><td>2.12%</td></tr><tr><td>......</td><td>......</td></tr><tr><td>Type Z</td><td>0.17%</td></tr></table>

The selection of $\alpha$ directly impacts the number of resulting clubs. Suppose there are in total T service types, and I GISs. We assume service types are uniformly distributed among GISs. Then the expected number of exclusive types in a single GIS is $[T/I]$ . On average, each GIS can build at most $[T/I]\times\alpha\%$ clubs. Therefore, the total number of clubs is bounded by $\{[T/I]\times\alpha\%\}\times I=\alpha\%T$ . A larger $\alpha$ results in more clubs. In S-Club, $\alpha$ is tuneable so that a good $\alpha$ can be selected for different network conditions.

Each GIS checks the set of top $\alpha\%$ service types, if it finds a type in the set has not been established as a club, it attempts to initiate club establishing process. For example, if GIS G tries to establish a club for Type B. G floods an SETUP-REQUEST announcement for type B throughout the mesh network, consulting the other GISs whether to set up a club for type B. On receiving the announcement, a GIS with type B services first checks its local table. If $UF(B)$ at this GIS is also within top $\alpha\%$ , it replies ‘YES’ to G, otherwise, it replies with ‘NO’. After a certain time, G gets all the replies, and then it calculates the support ratio $\delta$ ,

$$
\delta = \frac {N (Y E S)}{N (Y E S) + N (N O)} \tag {2}
$$

where $N(YES)$ is the number of YES replies, and $N(NO)$ is the number of NO replies. In S-Club, we set a Construction Threshold. If $\delta$ is greater than the threshold, $G$ will build a club for type $B$ ; otherwise, $G$ gives up.

If G decides to establish a club for type B, it sends a SET-UP announcement to those GISs which replied previously and now club members. The SET-UP announcement encloses the list of all members, and so we get a virtual complete graph, as illustrated in Fig. 3(a). The cost in this graph is probed by each member independently. The next issue is how these members are connected. The objective is to make the club robust while introducing as less maintenance overhead as possible. In S-Club, we build a minimum spanning tree (MST) among club members. The reason we adapt

MST as the topology of a club is that a MST may assure all the club members are connected while get minimum traffic cost when flooding requests along the club. We employ the algorithm proposed in $[3]$ , where a collection of disjoint trees spanning all the group members is maintained. Every tree independently expands by joining the closest tree, until all nodes are connected in a single tree. It is proved that given a graph with n nodes, the distributed algorithm for constructing MST takes $O(n)$ time. Using this method, a MST among all members is created as shown in Fig.3(b). G then sends a NEW-CLUB announcement to all GISs with full list of club members.

![](images/cabc683aecbbdd2e53ab8054e3dca5699588299db3d914e46f393e7966a0bfef.jpg)



(a)

![](images/b1b53abb94f0d768c97c691a5fbdc81f40aee6c13791533590a7a7f16a2a64ce.jpg)



(b)   
Figure 2: Maintenance of a service club

# 3.4 Club Maintenance

Clubs should be dynamically maintained. On one hand, GISs themselves are dynamic. Some may become unavailable because of hardware failure. On the other hand, services registered in a GIS are also dynamic. Some services may be newly registered at the GIS, and existing services could be removed. The consequence is that GISs need to join or leave corresponding clubs.

In our design, the topology in a club is a minimum spanning tree, which suffers from single-point-failure. One node leaving the club may lead to topology disconnection. To solve this problem, we employ a club member management protocol similar to Narada [5]. To this end, each club member maintains a full list of all the members, and every member's list needs to be updated when a new member join or an existing member leaves. To disseminate the changes, we require that each member periodically generate a refresh message with monotonically increasing sequence number, which is propagated along the MST. On receiving a refresh message from neighbour $j$ , member $i$ updates its table according to the algorithm in [5].

When a GIS is registered with a new type of service, it checks locally whether there exists a club for this type. If yes, it sends a JOIN announcement using the address of the club, which will be flooded within the club. Each club member replies to the new GIS so that the GIS can get the list of the club members. Then the joining member selects a few club members from the list and sends them messages requesting to be added as their neighbour. It repeats the process until it gets a response from one of them. Having joined, the member then starts exchanging refresh messages with its neighbours and propagates the changes of new member joining. Obviously this method can not assure the member topology to be a MST, but a spanning tree.

When a member leaves a group purposely, it notifies its neighbours in the spanning tree, linking all its children to its parent. These changes will also be propagated through the exchange of refresh message to the entire club.

We also need to consider another case of abrupt failure. As mentioned above, each member receives refresh messages from its neighbour periodically. If a member does not receive refresh message from its neighbour for a certain period of time, the direct neighbour may be failed. The member sends an announcement to find the neighbour of the failed node along the underlying mesh network. Thus, abrupt failure can be detected and the partition of spanning tree can be repaired. Changes can also be propagated through the exchange of refresh messages.

Member joining and leaving constantly may cause the performance of topology of the club members (i.e., the spanning tree) degraded. To rebuild the MST, the root need to initiate the distributed MST algorithm periodically and propagates the newest member through another NEW-CLUB announcement.

On receiving a NEW-CLUB announcement, every other GISs will choose one of the members from the list as the address of the club. Once this member leaves the club, the GIS may ask their neighbours in underlying mesh network to get another member as the new address. With the periodically reconstruction of member topology, this GIS can refresh their club address constantly. Consequently, any GIS can find an available member as the entry to each service club.

# 3.5 Club Deconstruction

It is possible that a previously popular service type become unpopular. If the services of this type are rarely requested, the club maintenance cost may exceed the benefit the club brings. Therefore, in this case, we should close the club. Moreover, closing unpopular clubs allows us to dynamically control the number of clubs in an appropriate level.

The deconstruction process of a club is similar with the construction of a club. Each GIS periodically starts the deconstruction process. Once the process is started, the GIS will try to close clubs for those service types whose UFs are out of the top $\alpha\%$ . We set the Deconstruction Threshold as $\gamma$ . If close support ratio $\delta$ is greater than $\gamma$ , G will close the club; otherwise, the club remains. If G decides to close the club, it floods a CLOSE announcement throughout the network. For members of this club, they remove relevant club connections. And, for normal GISs, they remove the club record.

# 3.6 Service Search with S-Club

Here we discuss how users search services with the availability of service clubs. To simplify our discussion, we assume a user simply wants to get the list of available services of a specific type. However, the search' model can be safely extended to more general cases; for example, the user can specify more constraints based on service properties.

It is assumed that any search request is firstly sent to a GIS close to the user. On receiving a search request for a specific service type, the GIS checks locally whether there has been a club for this type. If yes, the GIS forwards the request to the club, which will be flooded within the club only. Each club member then returns the information of the relevant services to the user. Since the request is strictly restricted within the club and no irrelevant GISs is involved, much traffic is saved. If there is no club for this type, however, the GIS has no choice but to flood the search request throughout the mesh network.

When a new GIS joins the GIS network, it has no idea what clubs are there. But since it has at least one neighbour in the underlying mesh network, it can ask one of its neighbours for the information of existing clubs. Namely, it simply copies the information of clubs from its neighbour.

As the GISs are dynamic, some may become unavailable. AS mentioned previously, the address of a club is denoted by two members in this clubs. For one GIS, the problem arises if the two GISs become unreachable simultaneously. The GIS can not reach the club when a user wants to search services of this type. In this case, we require that it firstly copy the address (i.e., IPs of two members) of the club from one of its neighbour. Next, it sends an ECHO announcement to the club, for which each club member will reply with its own IP. Then, with the list of club members, the GIS is able to select two best members in terms of roundtrip time as the address of the club.

# 4. RLDS: An S-Club Implementation in CROWN Grid

According to the protocol and search mechanism described above, we designed a modular Grid information service architecture for our CROWN Grid, called RLDS (Resources Locating and Describing Service), which allows us to easily test and modify each component separately. This RLDS service is a WSRF service implemented in Java in order to take advantage of great number of code libraries available. Another advantage is this service can be deployed into a GT 4.0 compliant service container with little changes. The architecture of a RLDS (see Figure 3) is constituted by the following basic modules.

![](images/67ffca636792003b7d559befee2b6a532815842d6550739b3fbf38c805720c96.jpg)



Figure 3: The RLDS Architecture

1) Message Listener and Message Queue: This is the interface part of RLDS service. Message Listener translates all the received SOAP messages into protocol message object and put into the message queue for scheduling.   
2) Message Dispatcher: A module dispatches the message object in the queue to the right processor (i.e., the session management module, the club management module, the club search module and the local search module).   
3) Session Management: Maintain the search session. The RLDS will create a new session for each service request and check the result received by   
4) Club Management Module: Manages all the service clubs which this RLDS service belongs to. Also this module will maintain all the index and pointers to members of other service clubs.   
5) Club Search Module: Forward query messages in the overlay network defined by short-cuts of club members. Once the club search fails, forward in the underlying mesh network.   
6) Local Search Module: Maintain all the information and registered services, response for the local search request and check the user frequency of each type of service.   
7) Logging Module: Log all the events into database. Use frequency is calculated according to the logs.

# 5. Performance Evaluation

To evaluate the performance of our proposed S-Club, we designed a simulation tool, in which a certain number of GISs is connected selectively to form an underlying mesh network.

# 5.1 Simulation Methodology

To simulate the service discovery process, first we generate the underlying GISs topologies, and distribute service information into each GIS node. When simulation runs, a certain number of service discovery request $R(Ts, N)$ is generated and sent to one of a GIS node, while Ts is the service type identifier, and N is the number of available services user wants to get. The request with the address of the first GIS node is propagated along the GISs network, the GIS which has available services of type Ts sends reply to the first GIS node. Finally, the first GIS node sends an available service list of N services to end user as the response. In studying the performance of our algorithms, we compare it to the MDS-like System without S-Club mechanism, which using the discovery protocol of MDS2. If a MDS server can't answer the user request, it sends the request to its direct neighbours. i.e., request is flooded in the mesh network to find available services.

BRITE [18] is a topology generation tool that provides the option to generate topologies based on the AS Model. We generate 10 network topologies with 20,000 nodes. Since the GISs is deployed into some of nodes over internet, the mesh network topologies are generated with a number of nodes ranging from 100 to 1000 selected from the 20000 physical network topologies. We generate the GISs mesh topologies with average 2 edge connections, means there are 4 logical neighbours for each GIS. The bandwidth between every two GIS nodes is calculated according to the shortest path along the physical network topologies.

The generation of the service discovery requests is modeled as a Poisson process, and the generation interval of requests is therefore exponentially distributed. In our simulation, each GIS node receives 6.42 queries per minute, which is calculated from the observation data shown in [19], i.e., 143,446 operations, including 7710 query operations, were received by a single MDS server during 20 hours.

In our simulation, the requested service type is under the control of Request Distribution, which is defined as the probability of finding a certain type of service. Our observation in CROWN Grid shows that some types of service is much more popular than others. In our simulation, we assures about 70% of requests are searching for 20% type of services. In each request, the number of required available services is generated under the control of Percentage of Requested Services, which is tunable during the simulation ranging from 10% to 100%.

# 5.2 Metrics

We use following three performance metrics: average response time, total traffic overhead, and optimization ratio.

Average Response Time of a query is one of the parameters concerned by end users.

Total Traffic Overhead of a query is defined as the length of message sent among GISs to answer the query. We have traced the real message in CROWN Grid, in which GIS is wrapped as an OGSA Grid Service using SOAP messages. Including the head of SOAP message, the size of all related messages is ranging from 1500 bytes to 3000 bytes.

Optimization Ratio shows the benefit of S-Club mechanism with comparison to MDS-like system. The optimization ratio of average response time is defined as follows,

$$
\text { OptimizationRatio } = \frac {A R T _ {M} - A R T _ {S}}{A R T _ {M}} \tag {3}
$$

While $ART_{M}$ is the average response time of MDS-like system and $ART_{S}$ is the average response time of S-Club system.

![](images/da47c3fb52b2391cf698390dcc5a172807926795de3c69f3008fd6b088901eed.jpg)



Figure 4: Number of clubs v.s. frequency threshold $\alpha$   
![](images/9058207afde44bc2ddd63f20d9665716eba63ebb152c2a946d0bc9d97c498441.jpg)



Figure 7: Average response time v.s. simulation time

![](images/fa76a64d6e0dd96c832987308f0926e82db2339fca58d6ec34af168a6631c414.jpg)



Figure 5: Total traffic v.s. frequency threshold $\alpha$   
![](images/3c190653ef2aeb4ae41385344cd45665be5bae76c12eccb53c1e177c9c3820bf.jpg)



Figure 8: Total traffic v.s. % of requested services

![](images/0fe794aa53d27ceb9017ff5855c3ce230627526440dcd2f85ba841ecd14e7bbf.jpg)



Figure 6: Average response time v.s. frequency threshold $\alpha$   
![](images/7330b056dec76a87680d84a51282318f535a412749c331b2ad2f8500143f71b3.jpg)



Figure 9: Average response time v.s. % of requested services

# 5.3 Simulation Result Analysis

In our first simulation, we study the effectiveness of frequency threshold $\alpha$ in S-Club. Figure 4 shows the frequency threshold affects the total number of clubs remarkably. In Figure 5 and Figure 6, we see that with the increment of $\alpha$ , total traffic and average response time are not always improved. Intuitively, too many clubs may bring much maintenance overhead. There exists a best value of $\alpha$ to maximize the benefit of S-Club. For example, Figure 5 shows that in this simulation, 0.5 is the best choice of $\alpha$ .

In the second simulation, we compare the S-Club with MDS-like systems. In Figure 7, the parameter p stands for the percentage of requested services. We see that with the time elapses, average response time of all MDS-like systems is almost a constant while the average response time of S-Club systems is decreasing gradually and finally comes to a stable state. Figure 8 and Figure 9 plot the benefit S-Club mechanism brings with the change of parameter p with a GIS network of 400 nodes. With the increment of p, total traffic and average response time increase together. We find that S-Club reduces the total traffic by 46% and average response time by around 7-26%.

In the third simulation, we study the benefit of traffic brought by S-Club. We simulate 3 groups with scale of 100, 200 and 400 GIS nodes and compare with the MDS-like system. The simulation results in Figure 10 and Figure 11 show that S-Club reduces total traffic and average response time significantly. For example, when n=200 and total number of requests is 60000, S-Club reduces traffic by 55% and average response time by 27%.

The last simulation studies the scalability of S-Club with the scale of GIS network increases. As illustrated in Figure 12, we simulate another 3 groups with scale of 100 to 1000 GIS nodes and comparison the average response time to MDS-like system. With the number of GIS servers increases, S-Club gives more benefit on average response time. Figure 13 shows the optimization ratio of average response time. Having 1000 GIS nodes, S-Club reduces about 27% to 35% response time.

# 6. Conclusions

Our key project, CROWN, holds the ambitious goal to integrate nationwide and worldwide valuable resources. Efficient information service is fundamentally important in CROWN. In this paper, we proposed the S-Club scheme to improve the performance of information service in CROWN. We build an overlay over the existing mesh network of GISs. For those popular services, we establish service clubs, in which GISs providing the same type of services are closely connected. When a user wants to search a service, the search request is effectively restricted within the small club. Simulation results demonstrate that S-Club significantly improves service search performance and outperforms the existing approaches. S-Club has been successfully implemented in our CROWN Grid environment.

![](images/7f913f054050c488768c349f3e564f4add2b82c8d742a5d7e15969795a6209e3.jpg)



Figure 10: Total traffic v.s. number of requests   
![](images/607b90e3ed23e18f497a75eae5c55bc849dbecb92025cc5352fe324c54168d69.jpg)



Figure 12: Scalability of S-Club, average response time vs. Number of GISs

![](images/c24db1fbef092c9706d9c10af2d81bc3632eb135748743aa536029fbe20554ed.jpg)



Figure 11: Response time v.s. number of requests   
![](images/531289bbc9bd276491aca54584a923a98783f8ec381157fcb38fec5930829a38.jpg)



Figure 13: Optimization ratio of average response time (ART)

Acknowledgements Part of this work is supported by grants from the China National Science Foundation (Project No.91412011), China 863 High-tech Programme (Project No.2003AA119030, 2003AA115420, 2002AA113030) and China Ministry of Education (Project No. CG2003-CG004, GP004, GA004). We would also like to thank Hailong Sun, Xianbo Xia and Tianyu Wo at Beihang University for helping us to do the simulation on the cluster.

# References

[1]"Hawkeye: http://www.cs.wisc.edu/condor/hawkeye."   
[2]"DataGrid Information and Monitoring Services Architecture: Design, Requirements and Evaluation Criteria, Technical Report.," DataGrid.   
[3]H. Abdel-Wahab, I. Stoica, F. Sultan, and K. Wilson, "A Simple and Fast Distributed Algorithm to Compute a Minimum Spanning Tree in the Internet," in Joint Conference on Information Sciences '95. North Carolina, 1995, pp. 429-433.   
[4]S. J. Chapin, D. Katramatos, J. Karpovich, and A. Grimshaw, "Resource management in Legion," in proceedings of Workshop on Job Scheduling Strategies for Parallel Processing, in conjunction with the International Parallel and Distributed Processing Symposium, 1999.   
[5] Y.-h. Chu, S. G. Rao, S. Seshan, and H. Zhang, "A Case for End System Multicast," in proceedings of ACM Sigmetrics 2000, Santa Clara, CA, 2000.   
[6]K. Czajkowski, S. Fitzgerald, I. Foster, and C. Kesselman, "Grid Information Services for Distributed Resource Sharing," in proceedings of the 10th IEEE International Symposium on High-Performance Distributed Computing (HPDC-10), 2001.   
[7]S. Fitzgerald, I. Foster, C. Kesselman, G. v. Laszewski, W. Smith, and S. Tuecke, "A Directory Service for Configuring High-Performance Distributed Computations," in proceedings of the 6th IEEE symposium on High-Performance Distributed Computing, 1997, pp. 365-375.   
[8]I. Foster and C. Kesselman, "Globus: A metacomputing infrastructure toolkit," in International Journal of Super-computer Applications, vol. 11, 1997, pp. 115-129.   
[9]I. Foster, C. Kesselman, and S. Tuecke, "The anatomy of the Grid," International Journal of Super-computer Applications, 2001.

[10]"The physiology of the Grid: An Open Grid Services Architecture for distributed systems integration," http://www.globus.org/research/papers/ogsa.pdf   
[11]I. Foster, C. Kesselman, J. Nick, and S. Tuecke, "Grid Services for distributed system integration," in IEEE Computer Magazine, vol. 35, 2002, pp. 37-46.   
[12]I. Foster and C. Kesselman, The Grid 2: Blueprint for a New Computing Infrastructure: Morgan Kaufmann Publishers, 2003.   
[13]J. Frey and T. Tannenbaum, "Condor-G: A computation Management Agent for multi-Institutional Grids," Journal of Cluster Computing, vol. 5, pp. 237, 2002.   
[14]N. Furmento, W. Lee, A. Mayer, S. Newhouse, and J. Darlington, "ICENI: An Open Grid Service Architecture Implemented with Jini," in Parallel Computing, vol. 28, 2002, pp. 1753-1772.   
[15]W. Hong, M. Lim, E. Kim, J. Lee, and H. Park, "GAIS: Grid Advanced Information Service based on P2P Mechanism," in proceedings of the 13th IEEE International Symposium on High Performance Distributed Computing (HPDC-13), 2004, pp. 276-277.   
[16]A. Iamnitchi, I. Foster, and D. C. Nurmi, "A Peer-to-Peer Approach to Resource Location in Grid Environments," in proceedings of the 11th IEEE International Symposium on High Performance Distributed Computing (HPDC-11), 2002.   
[17]M. Litzkow, M. Livny, and M. Mutka, "Condor - A Hunter of Idle Workstations," in proceedings of the 8th International Conference of Distributed Computing Systems, California, 1988.   
[18]A. Medina, A. Lakhina, I. Matta, and J. Byers, "BRITE: An Approach to Universal Topology Generation," in proceedings of the International Workshop on Modeling, Analysis and Simulation of Computer and Telecommunications Systems (MASCOTS), 2001.   
[19]W. Smith, A. Waheed, D. Meyers, and J. Yan, "An Evaluation of Alternative Designs for a Grid Information Service," in proceedings of the 9th IEEE International Symposium on High Performance Distributed Computing (HPDC-9), 2000.   
[20]B. Tierney, R. Aydt, D. Gunter, W. Smith, V. Taylor, R. Wolski, and M. Swany, "A Grid Monitoring Architecture," The Global Grid Forum GWD-GP-16-2.   
[21]X. Zhang, J. L. Freshl, and J. M. Schopf, "A Performance Study of Monitoring and Information Services for Distributed Systems," in proceedings of the 12th IEEE International Symposium on High Performance Distributed Computing (HPDC-12), 2003.