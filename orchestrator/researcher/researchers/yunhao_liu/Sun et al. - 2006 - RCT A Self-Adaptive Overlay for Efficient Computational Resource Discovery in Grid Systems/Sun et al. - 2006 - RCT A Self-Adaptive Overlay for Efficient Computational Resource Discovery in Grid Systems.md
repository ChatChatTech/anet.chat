# RCT: A Self-adaptive Overlay for Efficient Computational Resource Discovery in Grid Systems

Hailong Sun $^{1}$ , Jinpeng Huai $^{2}$ , Gongwei Fu $^{1}$ , Yunhao Liu $^{3}$

$^{1,2}$ School of Computer Science, Beihang University, Beijing, China

$^{3}$ Department of Computer Science, Hong Kong University of Science and Technology

$^{1}$ {sunhl, fugw}@act.buaa.edu.cn, $^{2}$ huai@buaa.edu.cn, $^{3}$ liu@cs.ust.hk

# Abstract

Computational resource discovery is of great importance in grid environments. Existing approaches do not consider the characteristics of application resource requirements. We propose, Resource Category Tree (RCT), which organizes computational resources based on their characteristics represented by primary attributes (PA). RCT adopts a structure of AVL tree, with each node representing a specific range of PA values. Though RCT adopts a hierarchical structure, it does not require nodes in higher levels maintain more information than those in lower levels, which makes RCT highly scalable. RCT is featured by self-organization, load-aware self-adaptation and fault tolerance. Based on RCT, commonly used queries, such as range queries and multi-attribute queries, are well supported. We conduct performance evaluations through comprehensive simulations.

# 1. Introduction

Grid computing [1] aims at wide-area resource sharing and coordinated problem solving. Resource discovery is of paramount importance for achieving this goal. Grid information service (GIS) [2] is proposed to address resource discovery. Due to the large-scale, highly distributed and heterogeneous natures of grid environments, GIS faces many challenges. During the past years, several popular GIS systems have been designed, such as Globus MDS [3] and Condor gang-matchmaking [4]. P2P [5] and semantic-based [6] search are also introduced to deal with resource discovery.

Among various grid resources, computational resources provide underlying running support for services in both system and application levels. By computational resources, we mean underlying hardware resources with capacity of supporting computation, such as clusters, storage, super computers and PCs. And in our previous work [7, 8] we present the advantages of separating underlying computational resources from services by hot service deployment in a service grid [9]. With this separation, underlying resources and services from different providers are discovered and obtained respectively, thus dynamic service deployment onto underlying resources can be performed to meet specific non-functional requirements, such as low costs or high resource usage. This work is devoted to addressing the computational resource discovery in grid environments.

Existing GIS systems like MDS $^{[3]}$ also support discovery of computational resources. However, most GISs simply organize resources based on some overlay, while information about all resources is treated equally without any categorizing mechanisms. This leads to traversing the whole overlay in order to search for desired resources. If resources can be categorized by some characteristics, we can further organize resources with similar characteristics by particular overlay. By this means, queries can be processed by searching a subset out of a large number of accessible resources. This is believed to be able to reduce the overhead greatly and improve resource discovery efficiency.

In CROWN project [10], we develop many applications based on CROWN middleware. One of them is developed to factorize huge integers, which can be categorized as a computing intensive one because powerful CPU resources are urgently required while storage requirement is trivial. Another one is DSS (Digital Sky Survey) that retrieves data from a space telescope and provides a GUI interface for end users to query the star graph of a specified region. DSS needs at least 60GB storage to store the data from the space telescope while processing of user queries does not require powerful computing power. With this experience, we observe that applications can be characterized by their requirements for computational resources. Intuitively the resource discovery efficiency will be improved if we can organize resources according to the characteristics of application resource requirements. For example, resources with powerful CPU capacity are organized as a category to serve computing intensive applications. This is how our idea is motivated.

Computational resources are usually described by a set of attribute-value pairs. Among all attributes of a computational resource, we choose one or several attributes that can best characterize the resource capacity of meeting application resource requirements as primary attributes (PA). We propose an overlay, RCT (Resource Category Tree), to organize computational resources based on PAs. In the rest of this paper, we refer to computational resources as resources for simplicity, by which we mean the same thing.

Our major contributions are as follows:

- We identify the necessity to organize computational resources according to application resource requirement.   
- We propose an effective overlay, RCT, to organize computational resources in a self-organizing, self-adaptive and fault tolerant manner. With RCT, commonly used queries, such as range queries and multi-attribute queries, are well supported.   
- We evaluate the performance of RCT through comprehensive simulations.

The rest of this paper is organized as follows. Section 2 presents related work. We give an overview of RCT definition and resource organization based on RCT in section 3. Section 4 presents the design details. We describe the evaluation methodology and results in section 5 and conclude this paper in section 6.

# 2. Related work

Resource discovery is an important issue in grid environments. Two protocols (GRIP and GRRP) and two components (GIIS and GRIS) are proposed in Globus MDS $[3]$ to construct a hierarchical grid information service. Condor $[4]$ leverages ClassAd language to describe both queries and resources, and gang-matchmaking is proposed to match user queries with appropriate resources. In $[11]$ , a thorough performance evaluation of MDS and Condor is provided. P2P search technologies have also been adopted to address resource discovery in grids $[5]$ . The above mentioned approaches mainly focus on how to route user requests to target nodes, and the characteristics of application resource requirement are not considered.

Through mapping resource key to resource locations, DHT (Distributed Hash Table) technologies, such as Chord $[12]$ and CAN $[13]$ , can effectively address target resource by searching a limited number of nodes. But to support range and multi-attribute queries, additional efforts are needed.

For computational resource discovery, [14] presents a DHT-based peer-to-peer approach. The static and dynamic parts of resource attributes are combined into a Resource ID that serves as a key in a Pastry-based system. The resources are represented as overlapping arcs on a Pastry ring. The beginning of an arc represents the static attribute set and the length represents the spectrum of dynamic states. However, no mechanisms of load-aware adaptation are provided to eliminate possible bottlenecks caused by hot spot query.

The authors in [15] propose an overlay SOG to organize resources based on similarities of specific resource characteristics, using a hybrid P2P structure. A group is formed by a collection of nodes with some similarities in their characteristics and a leader is elected through gossip protocol. A group in SOG is similar to an RCT, but they are different in that resources in an RCT are further organized according to the value of primary attributes. Additionally, RCT considers application resource requirement when defining an RCT.

The authors in [16] propose a logical binary tree RST (Range Search Tree) on the basis of DHT infrastructure to support range queries. One advantage of RST is that it does not need to maintain the tree structure dynamically because the domain of an attribute is split into $2^{n}$ sub ranges beforehand and each node can deduct the tree structure locally. The dynamic RST is adaptive to the query and registration load. However, RST requires resources to register with many nodes whose responsible ranges cover the resource attribute value, incurring huge overhead in dynamic grid systems where resources need to frequently update status.

# 3. RCT overview

In this section, we describe RCT definition and the architecture of resource organization based on RCT.

# 3.1. Resource description

The attribute-based approach is widely adopted for describing resources in grid computing environments.

In this paper, we also choose this approach to describe computational resources. Each computational resource is characterized by a set of attribute-value pairs. In practice, we mainly concern on dynamic attributes (e.g. CPU load) of a resource in a real computing environment because dynamic status represents available capacity of a resource.

# 3.2. RCT-Resource Category Tree

Grid applications can be characterized by their requirements for computational resources, e.g computing intensive and data intensive applications. In turn, we can categorize computational resources based on certain resource characteristics that can meet application resource requirements. By doing so, resource discovery is performed on specific resource categories efficiently. For example, we know that resources with huge storage can better serve a data intensive application, thus we can organize them together based on an overlay structure.

Furthermore, we observe that values of most resource attributes are numerical, e.g. values of disk size. And attributes whose values are not numerical can be converted to be numerical through certain mathematical methods. Based on this consideration, RCT adopts an AVL tree (or balanced binary search tree) overlay structure to organize resources with similar characteristics. The attribute that can best describe the characteristic of resources organized by an RCT is named a primary attribute or PA. Figure 1 is an example of RCT. The chosen PA is available memory size, and the value domain of available memory ranges from 0MB to 1000MB.

Compared with traditional AVL, each node of RCT manages a range of values, instead of a single value. Each node only needs to maintain its connection with direct child nodes and parent, and operations like registration, updating and query can start from any node. Unlike in traditional AVL structure, higher-level nodes of RCT are not required to maintain more information or bear more load than those in lower levels, which provides the basis for RCT to scale easily.

![](images/d9ec3229900e6da65db4197892d80f9c94fcb393872295004113ba27f687365c.jpg)



Figure1. An example of RCT

Suppose D is the value domain of the PA of an RCT. Each node n of an RCT is responsible for a sub range of D, or $D_{n}$ . All resources with PA values belonging to $D_{n}$ register themselves to node n. We name each RCT node an HR (Head of a sub Range). And terms of “HR n” and “node n” will be used interchangeably in the rest of this paper. In Figure 1, the circles denote HRs, while the squares below an HR denote computational resources registered with an HR.

Suppose N is the total number of HRs in an RCT, $lc(n)$ and $rc(n)$ are the left and right child nodes of HR n respectively. Since an RCT is a binary search tree, we have the following observations.

$$
\bigcup_ {i = 1} ^ {N} D _ {i} = D, \tag {1}
$$

$$
D _ {i} \cap D _ {j} = \phi , \forall i, j \in [ 1, N ] \tag {2}
$$

$$
D _ {l c (i)} <   D _ {i} <   D _ {r c (i)}, \forall i \in [ 1, N ] \tag {3}
$$

We say $D_{i} < D_{j}$ if the upper bound of $D_{i}$ is less than the lower bound of $D_{j}$ , e.g. [1, 2] $< [3, 4]$ .

If the ranges of node i and node j, i.e. $D_{i}$ and $D_{j}$ , are adjacent, node i is referred to as a neighbor of node j, and vice versa. If node i is a neighbor of node j and $D_{i} < D_{j}$ , node i is called left neighbor of node j (denoted by L-neighbor(j)); node j is called right neighbor of node i (denoted by R-neighbor(i)). Note there are two exceptions: the leftmost HR and the rightmost HR, the former has no left neighbor and the latter has no right neighbor.

As shown in Figure1, C2 and B2 are neighbors of A, while C2 is L-neighbor of A and B2 is R-neighbor of A. Note that C1 does not have left neighbor and B2 has no right neighbor.

# 3.3. Organizing resources with RCT

As resources are owned and managed by different resource providers, providers may define different PAs for their resources, which results in constructing multiple RCTs. In Figure 2, we present a 2-layer architecture for organizing resources across resource providers by using RCT. In the lower layer, each resource provider defines a set of PAs that can best describe their resources. Based on PAs, resources are organized through a certain number of RCTs. To enable wide area resource discovery across different providers, an RCT index service (RIS) is deployed by each service provider in the upper layer. RIS is a basic service that stores information about PAs of a provider and entry points of RCTs. RISs can be implemented, e.g., as web services or grid services, and find each other using services like UDDI.

![](images/8c94b06e3831305e24db7a8735c65062d39a6684a77ac835be6a5d4b2c5deb1c.jpg)



Figure 2. Resource organization with RCT

In practice, a resource may have many attributes, but only a few of them are chosen as primary attributes. So there will not be too many RCTs. When a query request cannot be satisfied by a resource provider, the RIS will contact other RISs to recommend another resource provider for further discovery operations.

# 4. Design of RCT

Three goals are considered in RCT design: (1) self-organization, which is very important for dynamic grid environment. Manual operations should be as few as possible so as to allow resources to join or leave freely and keep the system scale easily. (2) load-aware self-adaptation, which is necessary to improve the availability and scalability when load of registration, query and updating is not balanced among HR nodes. (3) fault-tolerance, which is critical to handle unexpected failures of RCT nodes. In this section, we present how the design of RCT achieves these three goals. Following that, we describe the resource searching algorithm based on RCT.

# 4.1. Bootstrapping an RCT

As an RCT consists of a set of HRs, before building an RCT we need to consider how an HR is set up. To make RCT a self-organizing system, we require HRs be chosen automatically from resources themselves.

At first thought, it is a simple way to choose an HR randomly from resources. Nevertheless, if the chosen HRs are unstable or weak in capacity, the instability will affect the availability of RCT, and the weak capacity will lead to bottlenecks. Hence, we need to consider both availability and capacity when choosing a qualified HR. A resource with long online time means that it is much stable and available. Additionally, a resource with powerful capacity can ensure that it is capable to serve as an HR to manage a set of resources. The availability of a resource is defined as its online probability $p(p=t_{\mathrm{on}}/(t_{\mathrm{on}}+t_{\mathrm{off}}))$ , $t_{on}$ and $t_{off}$ are the online and offline time during a past period of time respectively); the capacity is measured by the computing power c (e.g. c=CPU Frequency).

At the beginning of the initialization stage, no RCTs or HRs exist in grid environment. An RCT index service (RIS) is configured and deployed to maintain the RCT information including primary attributes, their value domains, and entry points of at least one HR. The procedure of building an RCT is as follows.

(1) A resource queries RIS to get information about RCT configurations of PAs.   
(2) The resource checks whether it can satisfy the condition of being an HR of an RCT. If yes, go to step (3); else, the resource is not qualified to be organized.   
(3) The resource sends an HR-application request to RIS. The request contains information about which RCT it aims to build and data of its availability and capacity.   
(4) The RIS stores the data of the candidate resources. When the candidates for an RCT reach a certain number, RIS will compare the data of availability and capacity to select the most qualified one as the first HR of the relevant RCT. Then the RIS notifies other candidate resources to register with the selected HR.

The RIS serves as the bootstrapping service for building an RCT. After an RCT is built, resources can get an entry point to the RCT from RIS, but this is not the only approach. The information can be cached locally for later use, and a resource may get this information from other resources. Note that RIS is only responsible for building the first HR of an RCT, and the building of other HRs leaves to the RCT itself, which will be introduced in next section.

# 4.2. Load-aware self-adaptation

4.2.1. Resource maintenance. Due to the dynamic nature of resources, we need to address resource joining, leaving and status changing.

When a computational resource connects to a grid system, it will first try to find an RCT to register itself. This can be done through RCT index service. Eventually a resource will know the address of at least one HR, then sends its joining request to the HR. According to the PA value of the resource, the HR checks if it should manage the incoming resource. If yes, the resource is registered with the HR; otherwise, the HR will traverse RCT to find the HR that the resource should register with. After registration, a resource will periodically update its status including PA value to the corresponding HR.

A resource can leave without any notification. An HR should recognize the leaving of a resource as early as possible. For this purpose, a resource is required to send updating message to its HR periodically even its status is unchanged. The updating message is empty in case of unchanged resource status. On the other side, an HR will remove the related resource information if it has not received updating message from a resource for a period of time.

An HR only manages resources whose PA values belong to the HR's responsible range. When the PA value of a resource is out of an HR's range due to dynamic changes, the HR will traverse RCT to find a proper HR to transfer the resource to. For the transferred resources, this is similar to a re-registration to a new HR.

Note that the resource status of an HR itself also changes dynamically. One interesting question: when an HR's PA value no longer belongs to the sub range it is responsible for, will the HR be degraded to be a common computational resource? The answer is no, otherwise it will cause RCT to be instable. A resource that serves as an HR also serves as a common resource as well. Therefore, as a resource, an HR is also managed by another HR that is not necessary to be itself.

4.2.2. Load-aware adaptation. There are several cases in which an HR can be overloaded. For example, if an HR is responsible for a big range of PA values or the range of an HR is a “hot spot”, a large number of messages of registration, updating and query will overwhelm the relevant HR. Therefore if no appropriate measures are taken, the overloaded HRs will become the bottlenecks. On the one hand, when an HR is overloaded, its sub range should be split, which results in that new HRs are chosen or some resources are transferred to others. On the other hand, when an HR is light-loaded and no other HRs transfer resources to it as well, we should consider to delete it and merge its range with other HRs responsible for adjacent ranges. Deleting a light-loaded HR and merging corresponding sub ranges can reduce the average search length. In all, RCT must have the ability to adapt according to load state.

Before going further, a metric should be defined to represent an HR's load $l$ . As the data for describing a resource is only a few attribute-value pairs, managing resources will not consume much storage of an HR. We use CPU load to represent an HR's load. Light-loaded threshold $l_{\text{light}}$ and overloaded threshold $l_{\text{over}}$ are defined respectively. Additionally, a warning threshold $l_{\text{warning}}$ is defined ( $l_{\text{light}} < l_{\text{warning}} < l_{\text{over}}$ ) to avoid oscillation problems, i.e. a node easily may become overloaded after receiving load from others. When the load of an HR is above $l_{warning}$ and below $l_{over}$ , it indicates that the HR is near to be overloaded and can not accept new load transferred from other HRs. For example, when l is greater than 90% ( $l_{over}=90\%$ ), an HR is considered as overloaded; when l is less than 10% ( $l_{light}=10\%$ ), an HR is light-loaded; when l is less than 80% ( $l_{warning}=80\%$ ) and greater than 10%, an HR is ready to help its neighbors to balance load.

Note that an HR is also a computational resource that is used to process user jobs. To ensure the user job processing will not affect an HR's organizing resources in RCT, a resource reservation mechanism is needed. For example, if a resource acts as an HR, 20% of CPU time will be reserved for its responsibility in RCT. This will rely on resource manager's reservation functionality. Hence the definitions of $l_{\text{light}}$ , $l_{\text{over}}$ and $l_{\text{warning}}$ are based on the reserved capacity for organizing resources.

Suppose $D_{n}$ is the range an HR n is responsible for and HR n becomes overloaded. According to the above analysis, $D_{n}$ will be split to balance the load. We design two policies for splitting a range: Average Split (AS) and Analysis of Variance-based Split (AVS). With AS, $D_{n}$ is split evenly into two or three sub ranges; AVS considers load distribution across $D_{n}$ based on analysis of variance. For example, suppose [10,100] is a range, and load is mainly distributed in [80,100]. With AS, the range may be split into [10,55) and [55,100]; while with AVS, the splitting results can be [10,90) and [90,100]. In order to be consistent with the three observations presented in section 3.2, an HR only transfers load to two neighbors, which means $D_{n}$ is split at most into three sub ranges for each time.

To balance an overloaded HR, we first initialize the splitting policy as AVS; then the load of two neighbors is obtained; according to the load status of neighbors, the range is split and load is transferred to relevant neighbors; in case that both of neighbors are not available, a new HR is selected to balance the load, and in that case RCT itself needs to be balanced using existing tree balancing algorithms.

In contrast to the overloaded case, when HR n is light loaded, it will try to merge itself with its neighbors and resign the HR post so as to reduce the average search length. As the average search length of RCT has great impact on searching efficiency, the merge of light-loaded HRs will lead to higher efficiency of resource discovery.

Here the splitting policy is set as AS, because the whole range of current HR has light load; then the neighbors' load is obtained; if both of neighbors' load are above warning threshold, it has to wait for next period to try again; the load is transferred to left neighbor and/or right neighbor; eventually the HR resigns and some tree balancing algorithm is performed to keep RCT balanced.

# 4.2.3. HR failures. The leaving of an HR can be categorized as normal leaving and abrupt failures without notification.

If an HR leaves normally, it will choose a new HR from resources it manages to replace itself. However, the unexpected failure of an HR is much complicated, which makes the child trees of the failed HR disconnected with the other HRs of the relevant RCT. Therefore, it is desirable to have a fault-tolerant design to handle such failures.

We detect an HR's failure by sending keep-alive messages periodically between a node and its parent. As a result, the parent node or direct child nodes of a failed HR will first notice the failure of an HR. One straightforward way of recovering RCT is to locate the disconnected child trees and assign new parent HRs for them. This procedure is much complex if several HRs fail simultaneously. In that case, an HR is required to maintain information of either all of predecessors or offspring, which means an HR's leaving or joining has to be notified to many other HRs. In case of frequent HR's joining or leaving, this will definitely incur large overhead to the whole system.

Instead we choose a rather simple but effective approach that is based on redundancy. Note that the online time is an important factor in defining the criteria for selecting an HR. Therefore, an HR has better availability than other resources. And the probability of the simultaneous failure of multiple HRs will be small. Based on the above analysis, we require each HR should have an alternate backup. When the primary HR crashes, the backup HR will be activated to work as primary HR and a new backup is selected at the same time. Even in case that both HRs fail, the disconnected resources can join the RCT again later after they realize this.

![](images/ace58e3bfb80e1212b374a7962a34639435de386e951bfffe6e25a2d58b7c3fc.jpg)  
Figure 3. Four types of commonly used queries

# 4.3. Searching with RCT

The ultimate goal of RCT design is to process resource queries and return resources that best meet users' query requirements. Given the resource organization defined by RCT, we present the search mechanisms in this section.

First, we identify four types of commonly used queries from two dimensions, as shown in Figure 3. Here we provide examples for these four types of queries: Q1: “Available storage = 90GB”; Q2: “CPU load < 50%”; Q3: “Available storage = 100GB AND OS = Windows XP”; Q4: “Available memory > 256 MB AND CPU load < 80%”. We refer to searches corresponding to the four types of queries as Q1-search, Q2-search, Q3-search and Q4-search respectively.

RCT supports all these four types of queries while we only present searching algorithm for Q2-search and give description to show how Q2-search can be extended easily to support the other three. In order to balance the query load, the algorithm is designed to allow a query starting from any node of an RCT, instead of only from the root node.

We suppose $D_{q}$ to be the range of a user query for a primary attribute (PA). $D_{l-childT(n)}$ and $D_{r-childT(n)}$ are ranges that the left child tree and right child tree of n are responsible for respectively. The algorithm is designed as a recursive function, and we omit the pseudo code for the space limitation. The query results will be aggregated in a data structure called ResultSet. We first split $D_{q}$ into 3 sub ranges: $D_{0}, D_{1}$ and $D_{2}$ . $D_{0}$ is the intersection of $D_{n}$ and $D_{q}$ ; $D_{1}$ and $D_{2}$ are sub ranges of $D_{q}$ that are adjacent to the left and right ends of $D_{0}$ respectively. If $D_{0}$ is not empty, search is performed locally for the range of $D_{0}$ ; if $D_{1}$ is not empty, search is performed in left child tree and/or at parent node depending on the relationship of $D_{1}$ and $D_{l-childT(n)}$ ; if $D_{2}$ is not empty, search is performed in right child tree and/or at parent node depending on the relationship of $D_{2}$ and $D_{r-childT(n)}$ .

To implement the above algorithm, each HR n is required to know the total range that its child tree is responsible for. With this information, $D_{r-childT(n)}$ and $D_{l-childT(n)}$ can be calculated. To achieve this, when load is transferred to/from a node, the node will not only update range information of its child trees but also notify relevant child nodes to update range information of their respective child trees.

With the Q2-search algorithm, Q1-search is much simple because Q1-search is indeed a Q2-search with the $D_{q}$ of only one element.

Q4-search is the most complicated among the four types of searches. Based on Q2 search, it can be dealt with in following three steps. (1) We first identify a PA in query constraints. (2) Then based on Q2-search algorithm, searching is performed with the query range of selected PA. (3) If a node satisfies the constraints on selected PA, further search will be performed at current node on constraints of other attributes. For example, if a query is “Available storage > 70G AND CPU Load < 20%” and “Available storage” is identified as PA, search will be performed on an RCT whose PA is “Available storage”. If HR n satisfies the constraint of “Available storage >70G”, the resources managed by HR n will be searched further based on “CPU Load < 20%”.

And Q3-search, which is multi-attribute and point search, is a simplified version of Q4-search.

As a query can start from any node, the search length of a point query will be $2^{*}\log N$ at most. For the range query, the complexity is highly dependent on the length of a query range.

One thing to note is that an incentive mechanism is introduced to the HR's local search. Considering that HRs contribute their capacity for RCT, we increase their priority to be searched. That means if two resources including an HR meet user query requirements and the user only need a limited number of resources, the HR will be returned to a user with a higher priority.

# 4.4. Parallel Search

AS each HR is responsible for a different range of value domain of a PA, the bigger length of a query range means more hops are needed for processing a query. Thus the proposed algorithms could be inefficient if the length of a query range is very large. If the ranges of all HRs are known beforehand, we can split the query range into multiple sub-ranges so that each sub-range matches an HR exactly. Thus searches can be performed in parallel for each sub range. In section 4.2, we mention that in order to maintain parent-child relationship of HRs, a child is required to send keep-alive message to its parent periodically. An HR can utilize this message to piggyback information about the HRs and their responsible ranges. In this way, each HR will know others' ranges, and parallel search can be implemented. When the range of an HR changes due to self-adaptation, the change will be known to all HRs after at most $\log_{2}N$ keep-alive periods. Before receiving notification about range changes, using stale information can cause some parallel searches to fail. In such a case, the search algorithms presented in section 4.3 will be used.

# 5. Performance evaluation

# 5.1. Simulation methodology

The RCT algorithms are simulated through event-driven approach with Java codes. The simulated RCT has 100 nodes (HRs), each of which manages 20 resources. The value domain D of selected PA is [0,100], and D is evenly split across the HRs, which means the length of an HR's sub range is 1. The query arrival is modeled as a Poisson distribution.

The metrics we use are as follows. (a) Average Search Length (ASL). ASL indicates the average number of HRs that a request is passed before being processed. (b) Standard deviation of query load. As RCT has the ability of load-aware adaptation, this metric is used to evaluate how load is balanced across HRs. The smaller value of this metric indicates a better balancing effect.

# 5.2. Evaluation Results

In our first experiment, we evaluate RCT performance in terms of metric (a) through varying query rate. The query rate varies from 500 per second to 10,000 per second, and queries are distributed equally to 100 HRs. The queries in this experiment are Q1 queries that are single attribute and point queries. Figure 4 shows the ASL with RCT scheme is between 8.6 and 9 (see proof in [17]) under different query rates.

![](images/cc3aecf8b5b130a5efdad61d5341d34ccddf9e9d3d696629c7df7db9e1331824.jpg)



Figure 4. Query rate vs. ASL

![](images/200771ef644b49b4963f1fa0dd4d6684683bce45e117a6e45832cf54fd68a098.jpg)



Figure 5. Standard deviation of query load

![](images/cd904b40cec0ad12a621b37d3fd6ca981e522361a87af3e62326feba492c61be.jpg)



Figure 6. Number of HRs during adaptation

Since RCT is designed to be adaptive based on its load status, we design the second experiment to evaluate how RCT adapt in over-loaded and light-loaded situations. In practice, the aforementioned thresholds of $l_{over}$ , $l_{light}$ and $l_{warning}$ can be defined as number of queries to process per second. In this experiment, they are set to be 50, 25 and 40 respectively. We let 90 HRs work normally with a load of 40 queries per second. The load of other 10 HRs varies from 1 to 120, which is a process of transition between being light-loaded, normal and overloaded. Figure 5 shows that the load-aware adaptation mechanism of RCT can balance the query load effectively in both overloaded and light-loaded cases and greatly reduces the risk of system bottleneck. Figure 6 plots the total number of HRs during adaptation according to the changing load of the selected 10 HRs. When the selected 10 HRs are light-loaded, they will merge with other HRs, and the number of HRs reduces. While in overloaded situation of the 10 selected HRs, new HRs are born to share the load, resulting in an increase of HR number. From Figure 5 and Figure 6, we can observe that not only load of each HR but also the RCT structure adapts automatically along with load status of HRs.

# 6. Conclusion

In our CROWN project $[10]$ , we observe that applications can be characterized by their requirement for resources. We then propose RCT for effective computational resource discovery in grid. RCT leverages application resource requirement to organize resources based on AVL tree. Although RCT is hierarchical, nodes in higher levels need not maintain more information than those in lower levels, which makes RCT very scalable. RCT is designed to be self-organizing, self-adaptive and fault-tolerant. Commonly used queries such as range queries and multi-attribute queries are well supported by RCT. We conduct extensive evaluations through simulations.

Future work will lead into three directions. First, we will further study how to RCT adapts to the lengths of query ranges so as to further improve the discover efficiency. Second, we will implement RCT with a service-oriented approach in our CROWN grid project. Third, we will conduct more experiments to evaluate RCT performance with real implementations.

# Acknowledgement

We thank anonymous reviewers for their valuable comments. This work was supported in part by the NSF of China under Grant 90412011 and by China National Natural Science Funds for Distinguished Young Scholar under Grant 60525209, partly by National Basic Research Program of China 973 under Grant 2005CB321803.

# References

[1] I. Foster, C. Kesselman, and S. Tuecke, "The Anatomy of the Grid: Enabling Scalable Virtual Organization," The International Journal of High Performance Computing Applications, vol. 15, pp. 200-222, 2001.   
[2] B. Plale, P. Dinda, and G. v. Laszewski, "Key Concepts and Services of a Grid Information Service," 15th International Conference on Parallel and Distributed Computing Systems (PDCS), 2002.   
[3] K. Czajkowski, S. Fitzgerald, I. Foster, and C. Kesselman, "Grid Information Services for Distributed Resource Sharing," HPDC 2001   
[4] R. Raman, "Matchmaking Frameworks for Distributed Resource Management," PhD Thesis: University of Wisconsin-Madison, 2001.   
[5] A. Iamnitchi, I. Foster, and D. C. Nurmi, "A Peer-to-Peer Approach to Resource Location in Grid Environments," HPDC 2002.   
[6] F. Heine, M. Hovestadt, and O. Kao, "Towards Ontology-Driven P2P Grid Resource Discovery," Grid 2004.   
[7] H. Sun, L. Zhong, J. Huai, and Y. Liu, "OpenSPACE: An Open Service Provisioning and Consuming Environment for Grid Computing," e-Science 2005.   
[8] H. Sun, Y. Zhu, C. Hu, J. Huai, Y. Liu, and J. Li, "Early Experience of Remote & Hot Service Deployment with Trustworthiness in CROWN Grid," APPT 2005.   
[9] I. Foster, C. Kesselman, J. M. Nick, and S. Tuecke, "Grid Services for Distributed System Integration," IEEE Computer, 2002.   
[10] CROWN Project: http://www.crown.org.cn/en.   
[11] X. Zhang, J. L. Freschl, and J. M. Schopf, "A Performance Study of Monitoring and Information Service for Distributed Systems," HPDC 2003.   
[12] I. Stoica, R. Morris, D. Karger, F. Kaashoek, and H. Balakrishnan, "Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications," ACM SIGCOMM, 2001.   
[13] S. Ratnasamy, P. Francis, M. Handley, R. Karp, and S. Shenker, "A Scalable Content-addressable Network," SIGCOMM, 2001.   
[14] A. S. Cheema, M. Muhammad, and I. Gupta, "Peer-to-peer Discovery of Computational Resources for Grid Applications," Grid 2005.   
[15] A. Padmanabhan, S. Wang, S. Ghosh, and R. Briggs, "A Self-Organized Grouping (SOG) Method for Efficient Grid Resource Discovery," Grid 2005.   
[16] J. Gao and P. Steenkiste, "An Adaptive Protocol for Efficient Support of Range Queries in DHT-based Systems," ICNP 2004.   
[17] G. Fu and H. Sun, "Complexity Analysis of Random Search with AVL Tree,   
"http://www.crown.org.cn/downloads/AVLComplexity.pdf, Technical Report: TR-BUAA-ACT-06-01, 2006.