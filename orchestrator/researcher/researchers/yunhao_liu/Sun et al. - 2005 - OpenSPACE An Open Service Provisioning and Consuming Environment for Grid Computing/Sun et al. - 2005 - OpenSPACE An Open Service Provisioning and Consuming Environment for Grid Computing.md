# OpenSPACE: An Open Service Provisioning and Consuming Environment for Grid Computing

Hailong Sun $^{+}$ , Liang Zhong $^{+}$ , Jinpeng Huai $^{+}$ , Yunhao Liu $^{*}$

$^{+}$ School of Computer Science, Beihang University, {SunHL,Zhongl,HuaiJP}@act.buaa.edu.cn

\*Department of Computer Science, HongKong University of Science & Technology, liu@cs.ust.hk

# Abstract

Our key project, CROWN (China Research and Development Environment Over Wide-area Network), aims to empower in-depth integration of resources and cooperation of researchers nationwide and worldwide using grid technologies. It adopts service oriented architecture. Current service grids do not consider the separation of services and underlying resources, potentially causing low job processing efficiency and resource utilization. In this paper, we propose a novel architecture for grid systems, called Open Service Provisioning and Consuming Environment (OpenSPACE). OpenSPACE is adopted by CROWN and is evaluated by prototype implementation based on real applications.

Keywords: OpenSPACE, DSR, Service Explorer, ROST, service grid

# 1. Introduction

Grid computing promises to enable coordinated resource sharing and problem solving in dynamic, multi-institutional virtual organizations $[1]$ . Current grid systems utilize many techniques of web services. OGSA $[2]$ $[3]$ is a typical combination of web service and grid technology. Service grid, which is widely considered as the future of grid computing $[4]$ , is generally based on SOA (Service Oriented Architecture).

As illustrated in Fig. 1, three basic entities including provider, registry and consumer are involved in SOA. Providers provide services for problem solving. Registries are used to facilitate service discovery. Providers register meta-information of the services to registries, then consumers look up registries for desired services and interact with potential providers to consume services. To a significant extent, running of services is dependent on the underlying resources including clusters, PCs and workstations.

![](images/4e2f5342a7718e89d5f50480118cc1be9532f5e0fa17288cc7a496bd6b3f6b10.jpg)



Figure1. Service oriented architecture

In most of current service grid systems, such as Globus Toolkit 3 or Globus Toolkit 4 [5], we do not see the separation of services and underlying resources, which means what consumers find in registries are the services that have been deployed onto specific underlying resources. Why is this separation such a fundamental concern in our CROWN grid [6]? Our observations show that the binding of services and underlying resources has following disadvantages.

First, job processing efficiency and resource utilization are limited. Service providers have to provide consumers with resources as well as services, however, during our implementation of CROWN grid, there are many cases that some organizations are professional on service development, but do not own resources for computation. On the other hand, many powerful resources are idle because their owners are not experts at service development. Consumers have no choice but to use the resources of service providers even if more powerful resources are available.

Second, potential higher costs are required for consuming services. Grid economy $[7]$ has become a hot research issue, which considers the profits of providers and costs of consumers in grid computing. The binding of services and underlying resources does not allow users to choose inexpensive services and underlying resources independently.

Third, great security challenges are faced. Grids span multiple autonomous security domains. As both services and underlying resources are provided by same providers, complex security mechanisms from providers are required. And it is often difficult to establish trust relationship dynamically between a consumer and a provider. However, the separation of services and underlying resources allows services to be run on consumers' own resources or other trusted resources.

OpenSPACE proposed in this paper is indeed motivated by the above mentioned real problems. OpenSPACE considers services and underlying resources separately. It is adopted by CROWN grid which aims to provide a resource sharing and cooperating environment using grid technologies. In this work, we focus on job processing efficiency and resource utilization issues. We evaluate OpenSPACE performance by prototype implementation and comprehensive experiments with real applications.

The rest of the paper is organized as follows. The architecture and key technologies of OpenSPACE are presented in section 2. In section 3, we describe the implementation experiences. Performance evaluation is presented in section 4. We discuss related work in section 5 and conclude this research in section 6.

# 2. OpenSPACE Architecture and Design

# 2.1. Conventions and terms

To make our discussion clear, we use the following two conventions:

1) Services. Here, a service represents an entity that implements some specific functions. For example, a blast service provides gene analysis function for biologists.   
2) Underlying resources. The running of services needs the support of underlying resources, such as clusters, workstations and PCs.

We further define two terms for services as (a) Raw service, which is a service not deployed. GAR files which are adopted by Globus Toolkit can be seen as a form of raw services. A raw service cannot be accessed by consumers. (b) Deployed service, which is a service deployed onto specific resources, and can be consumed by users.

# 2.2 Architecture overview

Figure 2 illustrates the architecture of OpenSPACE. In this architecture, providers are divided into service providers and resource providers. Service providers provide raw services and do not need to consider underlying resources for service running. Underlying resources are provided by resource providers. The deployment of raw services onto underlying resources is left to users, schedulers or middlewares.

OpenSPACE defines raw services (RS), deployed services (DS) and underlying resources (UR). Only DS can be directly used for problem solving. Usually, a DS runs in a service container, while a UR that joins in OpenSPACE needs to install a service container.

DSR (Distributed Service Repository), the key component of OpenSPACE, plays the role of registry in SOA, providing registering and access of resource information. Providers publish their services or resources through DSR and consumers lookup DSR to find desired UR, RS or DS.

To facilitate service provisioning and consuming, we design SE (Service Explorer) component, an IE (Microsoft Internet Explorer) like client middleware or tool. With SE, both service providers and underlying resource providers can publish their services or resources to grid environment conveniently. Consumers can easily locate and consume services as well. In short, SE acts as a broker between users and DSR. SE is also an optional component. Providers and consumers can interact with DSR directly.

# 2.3 Service provisioning and consuming model

In order to provide services or underlying resources, providers need to register the related meta-information to DSR. Moreover, raw service providers should also upload their raw services to DSR. OpenSPACE allows providers to update or unregister the meta-information and raw services from DSR. All such functions can be achieved with SE.

![](images/b89b76727245bd110f3a8387b3827646f514b968818bd29c7edb1cde73910309.jpg)



Figure2. Architecture of OpenSPACE

The consuming of services includes service selection, UR selection, service deployment, service invocation, and post invocation. In service selection phase, the consumer searches DSR with SE to find the desired RS. Then the consumer selects appropriate UR for running the service. In service deployment phase, the selected RS is deployed onto the selected UR. SE generates a GUI interface of the service for the consumer, and the consumer inputs its parameters to invoke the service. SE will present the result in an appropriate form. Finally, the consumer can choose whether to undeploy the service from UR in post invocation phase.

Note that in the service selection phase, the consumer also has the choice to find a DS, not a RS, such that the UR selection and service deployment can be ignored.

In the process of service consuming, a price or QoS negotiation process may be involved before service invocation.

# 2.4 Distributed service repository

As resources are highly distributed and dynamic in grid environments, DSR is designed to deal with locating and organizing resources.

Traditionally, grid information services (GIS), e.g. MDS [8], are used to handle resource organization and discovery in grid environments. The resources in OpenSPACE include raw services, deployed services, and underlying resources, which are distributed across a wide-area network. As a result, DSR is quite different from GIS in existing grids.

First, DSR provides basic information models for raw services, deployed services and underlying resources. These information models specify the format of meta-information of the three types of resources. At the same time, we allow users to define their own information models according to specific application requirements.

Second, the meta-information of resources and the raw services are maintained and provided to users. Usually, the data size of the information is not very large, so that it is reasonable to transfer this information through HTTP/SOAP protocols. However, the size of raw services depends on the implementation of service logic, ranging from several KBytes to GBytes. Therefore, we need to choose more efficient data transfer protocols other than HTTP/SOAP for service deliveries. At the same time, DSR should support storage of raw service.

Third, based on the advantages of hierarchical and P2P resource organization, DSR adopts a hybrid structure of resource organization, as illustrated in Fig. 3. Resources are organized as many regions. Resources inside a region are geographically close to each other. A region is composed of multiple domains which are formed based on specific considerations such as the structures of social organizations. With regions and domains, resources in a region are organized hierarchically as a tree structure. Each region has a region switch for sharing information with other regions. The communication between region switch adopts P2P approach.

![](images/b1968a85e0c4845e1f86c464984fd0d91b49cdf0d3093b0bd0ed97b107455011.jpg)



Figure 3. Resource organization in DSR

Fourth, DSR itself is a distributed system. Each domain of a region has one DSR node at least, thus many DSR nodes exist in the whole DSR system. Because the joining and leaving of DSR nodes are also dynamic, we need to provide a mechanism to maintain the tree based topology of DSR nodes.

# 2.5 Service container

In service grid, various resources are encapsulated as services. As we mentioned above, only deployed services can participate in the problem solving process. This means we must provide a service running environment for deployed services. Service container is such a component to solve this problem. WSRF [9] specifications, which replace the OGSI specification and make best use of existing web services technologies, are widely accepted in service grids. In OpenSPACE, services follow WSRF specifications.

Each UR that wants to join in OpenSPACE should install a service container. Apart from supporting the running of services, service containers also collect static information and dynamic status of UR. Such information is important for users to determine which UR is most appropriate to run their services.

The separation of raw services and underlying resources makes it critical for service container to provide good service deployment function which we will discuss in the following sections.

# 2.6 Service deployment

Raw services must be deployed before they are used. When a raw service is deployed onto a container, we hope to avoid restarting the service container to make the service available because we do not want other users to be interrupted. In other words, we need a hot service deployment.

In grid environment, deployers and service containers are usually distributed. Therefore, remote service deployment is highly desirable.

Furthermore, there exist many autonomous domains in grid environments. Not all raw services, deployers and underlying resources are in the same domain. Security is a big challenge when raw services are deployed on un-trusted underlying resources in different security domains. It is possible a raw service is malicious, or the target container is rogue or fragile. To provide security during the process of service deployment, trustworthiness is necessary. In CROWN, we employ ROST scheme $[10]$ to address this issue.

# 2.7 Service explorer

SE is designed to facilitate service provisioning and consuming. It provides visual user interfaces for the registering and maintaining of UR, RS and DS, generating service invoking interface, invoking services on behalf of consumers and presenting of service execution result. SE works as a broker between users, DSR, and service containers.

# 3. Implementation experience

In this section, we introduce our early experience with OpenSPACE implementation.

# 3.1 Node server

CROWN Node Server is the basic environment for running services. It provides multiple functions, such as service container, service deployment, resource monitoring, access to legacy applications, etc. Every computing node to join CROWN System needs to install this middleware. The service container in CROWN Node Server is implemented based on Globus Toolkit 4.0 core, which follows the OGSA/WSRF specification. It is the basis for the interoperation between heterogeneous resources. The raw services in our implementation are in the form of GAR files.

CROWN Node Server provides the function of resource monitoring. Both static information like computing capability, storage capability, operating system, and the dynamic information like CPU load, free memory, free disk space through a bunch of sensors, are monitored.

Another major function of Node Server is service deployment. CROWN Node Server provides remote and hot deploy service with trustworthiness (ROST). Service deployers can deploy their services to remote containers. After deployment, the user can access the grid service without restarting Node Server. For more details, please refer to [10].

# 3.2 CROWN DSR

The goal of CROWN DSR is to provide a global and abstract view of resources for the development and running of grid applications, and to enable the access to RS, DS and UR in CROWN environment. As shown in Fig. 4, this middleware consists of three parts: GIMS, DSR service, and GIQL. The information providers are the source of meta-information of raw services, deployed services, and underlying resources.

![](images/82b19b65c2c0a57529c9d9471ca6cd0df533037c3db223d3f0b9c8c70331486f.jpg)



Figure 4. Components of DSR

# 3.2.1 GIMS

GIMS (Grid Information Model Service) is a fundamental service to provide management of information models. An information model specifies the format of resource description. In DSR, the description of resources is based on attributes. Each attribute, which has attributed name, type, value and other constraints, is like a data field in relational database. We use MySQL database as the fundamental technology to store resource information. An information model is implemented as a data table in MySQL database.

We define three basic information models for raw services, deployed services, and underlying resources. GIMS is able to support the definition of new information models to satisfy special requirements. In addition, GIMS supports inheritance of information models, such that users can define new information models based on the extension of existing ones.

As DSR is a distributed system, to keep the consistence of information format, we require only one GIMS be installed in DSR. The information format of every DSR node should be consistent with those in GIMS.

# 3.2.2 DSR service

DSR service is a fundamental service deployed in every DSR node.

As discussed in section 2.4, DSR adopts a hybrid structure of resource organization. Our current implementation of resource organization is region based. All DSR nodes in one region are organized as a tree topology. Each DSR node has one parent node and multiple child nodes. As a DSR node can join and leave dynamically, the tree topology must be maintained adaptively. This is done through communication between DSR services deployed in DSR nodes.

Two key issues of DSR services deserve some discussions. First, a DSR service maintains and provides resource information of local DSR nodes. It is actually a WSRF compliant service which exposes several interfaces including register, unregister, find, and update. With these interfaces, information of resources can be registered, unregistered, located and updated. The information maintained by a DSR service is stored in a local MySQL database. When information is added or modified, the DSR service automatically accesses the global GIMS to guarantee the consistence with relevant information models. The DSR service also provides functions of storage and transferring of raw services. Currently, we choose FTP (File Transfer Protocol) as transfer protocol for raw services. Raw services are stored in the local file system of DSR nodes.

Second, a DSR service needs to communicate with other DSR services in other DSR nodes to maintain the tree topology, including node joining and leaving. When a DSR node joins in, the DSR service at that node will register itself to the DSR service at the parent node. Such information is transmitted recursively to parent nodes until the information arrives at the root of the tree.

OpenSPACE adopts a soft-state[8] based mechanism to deal with node leaving. Each DSR service sends keep-alive message periodically to its parent, notifying its aliveness. Meanwhile, each DSR service gets to know whether its child DSR services are alive by checking keep-alive messages periodically. When a DSR service does not receive keep-alive message from a child node for a given time period, it assumes that the child node has left. The current DSR service will remove related information and notify its parent node recursively until the root of the tree. Eventually, the child tree of the node that left will be connected to the leaving node's parent.

# 3.2.3 GIQL language

GIQL (Grid Information Query Language), a SQL-like data manipulation language, is used to manipulate information models and resource information.

Both GIMS and DSR service provide an executeGIQL interface for the process of information models and information. OpenSPACE provides a GIQL parser to transform the GIQL statements to corresponding SQL statements. Table 1 shows GIQL language definition for GIMS.

Table 1. Definition of GIQL for GIMS 

<table><tr><td>(a) CREATE IM im_name (col_name type [PRIMARY KEY][NOT NULL | NULL] [UNIQUE][DESCRIPTION description]) [DESCRIPTION description ];</td></tr><tr><td>(b) ALTER IM im_name MODIFY COLUMN column_name column_type;</td></tr><tr><td>(c) ALTER IM im_name ADD COLUMN column_name column_type;</td></tr><tr><td>(d) ALTER IM im_name DROP COLUMN column_name</td></tr><tr><td>(e) ALTER IM im_name CHANGE COLUMN old_name new_name new_type</td></tr><tr><td>(f) DROP IM IM_Name[,im_name,...];</td></tr><tr><td>(g) SHOW IMs;</td></tr></table>

In table 1, (a) is used for creating a new information model; (b)-(e) are used for modifying an existing information model; (f) is used to delete an information model; and (g) is used to know all information models supported by DSR.

The definition of GIQL for DSR services is similar to select, insert, delete and update in SQL language. Users need to specify the target table name as the target information model name in a data manipulation.

# 3.3 CROWN SE

Service explorer aims at helping providers and consumers to provide or consume services conveniently. We envision two kinds of service explorers: web-based and GUI-based. The web-based service explorer is an extension of a portal, which can be used through web browsers. The GUI-based service explorer is implemented as a standalone client tools, installed by providers and consumers. Current CROWN service explorer is implemented as an extension of CROWN portal.

The functions of CROWN SE include acquiring raw services, provisioning resources, invoking deployed services, generating service interface, monitoring user jobs, and presenting the execution results.

Among these functions, acquiring raw services and provisioning resources are dependent on DSR. A client program of DSR is embedded into the service explorer to implement the functions.

Here we focus on generating service interfaces and presenting execution results. CROWN SE adopts a rendering based approach to handle the service presentation. Each service has an input renderer and an output renderer which are provided by service providers. The input renderer of a service is used to generate visual service invoking interface automatically. The output renderer of a service is used for appropriate presentation of execution result. We define the following two interfaces respectively for an input renderer and output renderer.

1) getHTMInputRendering()   
2) getHTMLOutputRendering(Object result)

The result parameter of the output renderer is a Java Object instance representing the execution result of a service.

Through these two interfaces, SE can automatically generate the HTML-based user interface of a service and render the execution result appropriately for consumers.

# 4. Experiments and evaluation

The core idea of OpenSPACE is to separate the services and underlying resources. In this section, we present three set of experiments to evaluate the job processing efficiency and resource utilization of OpenSPACE implementation.

![](images/6a74cdcf627bcc7c2fe10ecdbc96d3ae4c591682977dc1e5f980b89e9b85c395.jpg)



Figure 5. Processing time v.s. initial number of DS   
![](images/55fc6c1f65a7ec8f1c967a6ae711e232f4a788fc7f78a1edb860d41c0754f054.jpg)



Figure 6. Processing time v.s. number of jobs

# 4.1 Experiment setup

The experiments are conducted across four domains connected by CERNET (China Education and Research Network) including Tsinghua University, Beijing University, CNIC (Network Information Center of CAS) and Beihang University. Two PCs (Pentium III 1.6GHz CPU, 512MB memory) in Tsinghua domain, one LangChao server (Itanium 2 1.3GHz \* 4 CPU, 2GB memory) in Beijing University domain, two Lenovo servers (Itanium 2 1.3GHz \* 4 CPU, 8GB memory) in CNIC domain, seven DELL PE2650 servers (Intel Xeon 3.0GHz \* 2 CPU, 2GB memory), two HP rx5690 servers (Itanium 2 1.3GHz \* 4, 4GB memory) and sixteen LangChao Yingxin Servers (Intel Xeon 2.8GHz \*2, 2GB memory) in Beihang University domain. Totally thirty computing nodes are involved, and a CROWN Node Server is installed at each computing node. The four domains are organized as a single region, while the Beihang University domain is the parent domain of the other three. In each domain, there is a DSR service, and the participating computing nodes are registered to the DSR service of local domain.

![](images/82bb1a0ed6378d025704cf3c08708d73280833879843e756002b404a3bd7ff98.jpg)



Figure 7. Processing time v.s. number of underlying resources

The application we use in experiments is a Blast service which is commonly used by biologists to identify unknown gene sequences. A user job is an invoking of the Blast service. In each experiment, we compare OpenSPACE with existing schemes in which underlying resources and services are not considered separately. In existing schemes, even some powerful underlying resources are idle, these resources cannot be utilized dynamically to process users' jobs. In OpenSPACE, when services are mapped to underlying resources, it is able to select the most powerful ones to process jobs.

# 4.2 Evaluation results

In the first experiment, 30 computing nodes are involved and 150 concurrent jobs are generated with

Java threads. Not all computing nodes are deployed with Blast services at the beginning. We measure the job processing time with different numbers of initial deployed Blast services.

As Fig. 5 shows, with the increase of initial deployed services, the job processing time of the two scheme decreases respectively. The average processing time of OpenSPACE is much shorter than that of the scheme without OpenSPACE.

In the second experiment, with the increase of the number of current user jobs, we evaluate the job processing time under different initial numbers of deployed Blast services. Figure 6 plots the distribution of job processing time of 10, 20 and 25 initial deployed Blast services. The improvement of job processing efficiency becomes more obvious with the increase of concurrent jobs. However, as the initial number of deployed services increases, the advantages of OpenSPACE are shrinking.

We believe this is caused by the time consumed on deploying raw services to underlying resources. When the time consumed on deployment is equal or greater than the time gained on the job processing, there will be less advantages for OpenSPACE, as shown in Fig. 6 in which the two curves of 20 initial DS's and 25 initial DS's are almost overlapped.

In the third set of experiment, we first define service coverage rate scr as

$$
scr = \frac {N _ {ds}}{N _ {ur}} \times 100 \%
$$

where $N_{ds}$ represents the number of initial deployed services and $N_{ur}$ denotes the number of total available underlying resources. With the increase of number of computing nodes, we evaluate the processing time of 100 concurrent jobs under different scr.

Figure 7 plots the result. We can see OpenSPACE outperforms the previous scheme with different number of underlying resources. However, when scr reaches 80%, the two schemes almost get the same result, indicating that OpenSPACE helps more with lower scr.

# 5. Related work

As one important result of service grid, OGSA is proposed by GGF (Global Grid Forum) in 2001. In 2003, the Globus Alliance released Globus Toolkit 3 which is based on OGSI specifications. Recently, Globus Toolkit 4 based on WSRF was released. Both of the two versions provide a bunch of middleware for constructing service grid. At the same time, OMII (Open Middleware Infrastructure Institute) [14] from UK e-science project envisions to become the source for reliable, interoperable and open-source Grid middleware to support building of e-Science applications. The most updated OMII 1.2 is a suite of middleware based on web service technologies for building grid applications. There are many other service grid middleware, such as ICENI [15], VGE [16], and SODA [17]. Compared with OpenSPACE, the middleware mentioned above does not address the issue of separation services from underlying resources. Although the Globus Toolkit defines GAR files which we adopt as raw services, it does not provide remote and hot service deployment support for dynamically deploy the raw services to underlying resources. A dynamic service deployment scheme is proposed in [18] allowing new GT3 services to be added or replaced dynamically. This is similar to our idea of hot service deployment, but the authors adopt a WAR to further wrap a grid service, which is technically different from our approach. Moreover, to our knowledge, there is no DSR like implementation to maintain and provide acquirement of raw services.

# 6. Conclusions and future work

Current grids do not separate services and underlying resources, causing low job processing efficiency, resource utilization, and severe security challenges. To address this issue, we propose OpenSPACE architecture for grid systems. We implement key components of OpenSPACE in our CROWN grid, including CROWN Node Server, DSR, and CROWN Service Explorer. With real grid environment and applications, we evaluate the improvement of job processing efficiency and resource utilization by adaptively deploying services to most powerful available underlying resources.

Our future work will lead to the following directions. First, we will investigate more strategies for mapping services to resources. Second, we will develop the resource organization across regions. Third, we will introduce economic models to provide support for the economic benefits of both providers and consumers. Finally, we are going to improve efficiency of composed services based on OpenSPACE.

# Acknowledgement

We thank the anonymous reviewers for their suggestions that help to improve the quality of this paper. This work is partially supported by the National Science Foundation of China under grant 90412011 and 60573053, the 863 High-tech program under grant 2003AA119030 from MOST (Ministry of Science and Technology) of China, and China Ministry of Education under grant CG2003-CG004&GP004&GA004.

# References

[1] I. Foster and C. Kesselman, The Grid: Blueprint for a New Computing Infrastructure, 2004.

[2] I. Foster, C. Kesselman, J. M. Nick, and S. Tuecke, "Grid Services for Distributed System Integration," IEEE Computer, 2002.   
[3] I. Foster, C. Kesselman, J. Nick, and S. Tuecke, "The physiology of the Grid: An Open Grid Services Architecture for distributed systems integration," 2002.   
[4] I. Foster and C. Kesselman, The Grid 2: Blueprint for a New Computing Infrastructure: Morgan Kaufmann Publishers, 2003.   
[5] The Globus Toolkit: http://www.globus.org/toolkit/.   
[6] CROWN Grid:http://www.crown.org.cn.   
[7] R. Buyya, D. Abramson, and S. Venugopal, "The grid economy," Proceedings of the IEEE, 2005.   
[8] k. Czajkowski, S. Fitzgerald, I. Foster, and C. Kesselman, "Grid information services for distributed resource sharing," presented at 10th IEEE International Symposium on High Performance Distributed Computing (HPDC2001), 2001.   
[9]WSRFSpecifications: http://www.oasis-open.org/committees/tc\_home.php.   
[10] H. Sun, J. Huai, Y. Liu, and J. Li, "Early Experience of Remote & Hot Service Deployment with Trustworthiness in CROWN Grid," accepted by 6 $^{th}$ International Workshop on Advanced Parallel Processing Technologies, 2005.   
[11] W. H. Winsborough, K. E. Seamons, and V. E. Jones, "Automated Trust Negotiation," presented at DARPA Information Survivability Conference and Exposition, 2000.

[12] W. H. Winsborough and N. Li, "Towards Practical Automated Trust Negotiation," presented at the 3rd International Worship on Policies for Distributed Systems and Networks (POLICY 2002), 2002.   
[13] W. H. Winsborough and N. Li, "Safety in Automated Trust Negotiation," presented at IEEE Symposium on Security and Privacy, 2004.   
[14] OMII: http://www.omii.ac.uk/.   
[15] W. L. Nathalie Furmento, Anthony Mayer, Steven Newhouse, John Darlington, "ICENI: An Open Grid Service Architecture Implemented with Jini," presented at IEEE/ACM SC2002 Conference, 2002.   
[16] S. Benkner, I. Brandic, G. Engelbrecht, and R. Schmidt, "VGE-A Service-Oriented Grid Environment for On-Demand Supercomputing," presented at 5th IEEE/ACM International Workshop on Grid Computing (Grid 2004), 2004.   
[17] X. Jiang and D. Xu, "SODA: a Service-On-Demand Architecture for Application Service Hosting Utility Platforms," presented at High Performance Distributed Computing (HPDC 2003), 2003.   
[18] J. B. Weissman, Seonho Kim, and Darin England, "Supporting the Dynamic Grid Service Lifecycle", CCGrid2005